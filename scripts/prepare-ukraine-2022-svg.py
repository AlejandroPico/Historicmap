"""Extract dated Russian-control candidates from archived CC BY-SA Commons SVGs.

Research preparer only: no downloads, imports have no side effects, no public/
writes. Required inputs and explicit output keep this separate from atlas builds.
Dependencies: numpy, pyproj, shapely>=2, svgpathtools==1.8.0 (+svgwrite).
See docs/UKRAINE-2022-RESEARCH.md before integrating the output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.cache/ukraine-014/python-deps'),
                str(ROOT / '.cache/python-packages')]
import numpy as np
from pyproj import Transformer
from shapely import make_valid
from shapely.geometry import Polygon, Point, mapping
from shapely.ops import unary_union, polygonize, transform as geometry_transform
from svgpathtools import parse_path, Line

PAGE = 'https://commons.wikimedia.org/wiki/File:2022_Russian_invasion_of_Ukraine.svg'
LICENSE = 'https://creativecommons.org/licenses/by-sa/4.0/'
PROJECTION = '+proj=eqc +lat_ts=49 +datum=WGS84 +units=m +no_defs'
OCCUPATION_FILL = '#ebc0b3'
GCP = [
    ('Kyiv', 'Q1899', 'circle2201', 'city-kiev-g'),
    ('Donetsk', 'Q43070', 'circle1031', 'city-donetsk-g'),
    ('Luhansk', 'Q134279', 'circle1033', 'city-lugansk-g'),
    ('Kharkiv', 'Q42308', 'circle2241', 'city-kharkiv-g'),
    ('Sumy', 'Q156752', 'circle2795', 'city-sumy-g'),
    ('Chernihiv', 'Q157053', 'circle1251', 'city-chernihiv-g'),
    ('Poltava', 'Q156747', 'circle1275', 'city-poltava-g'),
    ('Odesa', 'Q1874', 'circle1581', 'city-odesa-g'),
    ('Vinnytsia', 'Q157144', 'circle1707', 'city-vinnytsia-g'),
    ('Mykolaiv', 'Q41572', 'circle2709', 'city-mykolaiv-g'),
    ('Zaporizhzhia', 'Q157835', 'circle1715', 'city-zaporizhzhia-g'),
    ('Lviv', 'Q36036', 'circle1727', 'city-lviv-g'),
    ('Uzhhorod', 'Q156711', 'circle1765', 'city-uzhhorod-g'),
    ('Chernivtsi', 'Q157725', 'circle1845', 'city-chernivtsi-g'),
    ('Sevastopol', 'Q7525', 'circle2023', 'city-sevastopol-g'),
    ('Simferopol', 'Q19566', 'circle2025', 'city-simferopol-g'),
]


# Wikidata P625, CC0; verified labels/coordinates on 25 October2026.
GCP_COORDINATES = {'Kyiv': [30.523611111111, 50.45],
 'Donetsk': [37.80277777777778, 48.01583333333333],
 'Luhansk': [39.2973153, 48.5717084],
 'Kharkiv': [36.23111111111111, 49.9925],
 'Sumy': [34.799166666666665, 50.906666666666666],
 'Chernihiv': [31.294722222222223, 51.49388888888889],
 'Poltava': [34.55138888888889, 49.589444444444446],
 'Odesa': [30.7325, 46.48416666666667],
 'Vinnytsia': [28.467222222222, 49.237222222222],
 'Mykolaiv': [31.995, 46.975],
 'Zaporizhzhia': [35.1175, 47.85],
 'Lviv': [24.0315921, 49.841952],
 'Uzhhorod': [22.295, 48.623888888889],
 'Chernivtsi': [25.934444444444, 48.290833333333],
 'Sevastopol': [33.5225, 44.605],
 'Simferopol': [34.100039, 44.948376]}

# Exact archive revisions and editorial history; immutable file hashes.
SNAPSHOTS = [{'selected': '2022-12-31',
  'url': 'https://upload.wikimedia.org/wikipedia/commons/archive/4/4f/20230101030508%212022_Russian_invasion_of_Ukraine.svg',
  'size': 2482257,
  'license': 'CC BY-SA 4.0',
  'sourceRevisionTimestamp': '2022-12-31T15:23:30Z',
  'geometryReferenceDate': '2022-12-31',
  'reportedAssessmentDate': None,
  'lastControlUpdateRevision': '2022-12-31T00:37:41Z',
  'dateEvidence': 'Small counterattack south of Bakhmut per ISW',
  'sha256': '6d6a2922027bccbc025d7aa2bdc02e9a02a6fcba7489888ffcf9d51ec9e26d70'},
 {'selected': '2023-12-31',
  'url': 'https://upload.wikimedia.org/wikipedia/commons/archive/4/4f/20240101094640%212022_Russian_invasion_of_Ukraine.svg',
  'size': 3443521,
  'license': 'CC BY-SA 4.0',
  'sourceRevisionTimestamp': '2023-12-30T11:58:26Z',
  'geometryReferenceDate': '2023-12-27',
  'reportedAssessmentDate': None,
  'lastControlUpdateRevision': '2023-12-27T10:03:14Z',
  'dateEvidence': 'Mark Marinka as Russian controlled per the ISW & the detailed map',
  'sha256': '0293f2bc570e7922e1bee381b82e81c0eef7d01262e88e17a220fcd66ecc40c1'},
 {'selected': '2024-12-31',
  'url': 'https://upload.wikimedia.org/wikipedia/commons/archive/4/4f/20250106023609%212022_Russian_invasion_of_Ukraine.svg',
  'size': 4570028,
  'license': 'CC BY-SA 4.0',
  'sourceRevisionTimestamp': '2024-12-29T02:09:21Z',
  'geometryReferenceDate': '2024-12-29',
  'reportedAssessmentDate': None,
  'lastControlUpdateRevision': '2024-12-29T02:09:21Z',
  'dateEvidence': 'Updates per the ISW & the detailed map',
  'sha256': '078c17f41da3f438fb942c96c7d857d478d510ba77753c0b8addea077fde8971'},
 {'selected': '2025-12-31',
  'url': 'https://upload.wikimedia.org/wikipedia/commons/archive/4/4f/20260104065832%212022_Russian_invasion_of_Ukraine.svg',
  'size': 4309132,
  'license': 'CC BY-SA 4.0',
  'sourceRevisionTimestamp': '2025-12-22T16:50:45Z',
  'geometryReferenceDate': '2025-12-17',
  'reportedAssessmentDate': '2025-12-17',
  'lastControlUpdateRevision': '2025-12-20T18:05:26Z',
  'dateEvidence': 'updated using ISW 17 Dec',
  'sha256': '60ab8c5a018b484bc8ddcb26ac944a146f95263dfcfcf5da0cae3caf01cf7bd6'},
 {'selected': '2026-10-22',
  'url': 'https://upload.wikimedia.org/wikipedia/commons/archive/4/4f/20261024034822%212022_Russian_invasion_of_Ukraine.svg',
  'size': 4352401,
  'license': 'CC BY-SA 4.0',
  'sourceRevisionTimestamp': '2026-04-24T01:38:26Z',
  'geometryReferenceDate': '2025-12-17',
  'reportedAssessmentDate': '2025-12-17',
  'lastControlUpdateRevision': '2025-12-20T18:05:26Z',
  'dateEvidence': 'Control paths identical to December2025 version; updated using ISW 17 Dec',
  'sha256': 'cf05b54d007ddaded71abcaf7f3b7c2b8abc7753069a1885045718568f1b4e46'}]

def style(node):
    return dict(p.strip().split(':', 1) for p in node.get('style', '').split(';')
                if ':' in p)


def inherited(node, key, parents, default=None):
    while node is not None:
        value = style(node).get(key, node.get(key))
        if value is not None:
            return value
        node = parents.get(node)
    return default


def matrix(text):
    """SVG column-vector transform, in specified SVG transform-list order."""
    result = np.eye(3)
    number = r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?'
    for kind, raw in re.findall(r'([A-Za-z]+)\s*\(([^)]*)\)', text or ''):
        v = list(map(float, re.findall(number, raw)))
        m = np.eye(3)
        if kind == 'matrix':
            a, b, c, d, e, f = v
            m = np.array([[a, c, e], [b, d, f], [0, 0, 1]])
        elif kind == 'translate':
            m[:2, 2] = [v[0], v[1] if len(v) > 1 else 0]
        elif kind == 'scale':
            m[0, 0], m[1, 1] = v[0], v[1] if len(v) > 1 else v[0]
        elif kind == 'rotate':
            a = math.radians(v[0]); c, s = math.cos(a), math.sin(a)
            m[:2, :2] = [[c, -s], [s, c]]
            if len(v) == 3:
                m = matrix(f'translate({v[1]},{v[2]})') @ m @ matrix(f'translate({-v[1]},{-v[2]})')
        elif kind in ('skewX', 'skewY'):
            m[0 if kind == 'skewX' else 1, 1 if kind == 'skewX' else 0] = math.tan(math.radians(v[0]))
        else:
            raise ValueError(f'Unsupported SVG transform {kind}')
        result = result @ m
    return result


def world_matrix(node, parents):
    result = matrix(node.get('transform'))
    while node in parents:
        node = parents[node]
        result = matrix(node.get('transform')) @ result
    return result


def polygons(geometry):
    if geometry.geom_type == 'Polygon':
        return [geometry]
    return [p for child in getattr(geometry, 'geoms', ()) for p in polygons(child)]


def curve_points(segment, a=0, b=1, depth=0):
    """Adaptive chord error <=0.2 original path units, then full SVG transform."""
    start, end = segment.point(a), segment.point(b)
    midpoint = segment.point((a + b) / 2)
    # Additional quarter samples avoid missing inflected cubic curves.
    error = max(abs(segment.point(a + (b-a)*t) - (start+(end-start)*t))
                for t in (.25, .5, .75))
    if isinstance(segment, Line) or error <= .2 or depth >= 14:
        return [end]
    return (curve_points(segment, a, (a+b)/2, depth+1) +
            curve_points(segment, (a+b)/2, b, depth+1))


def path_geometry(node, parents):
    transform = world_matrix(node, parents)
    rings = []
    for subpath in parse_path(node.get('d', '')).continuous_subpaths():
        if not subpath:
            continue
        points = [subpath[0].start]
        for segment in subpath:
            points.extend(curve_points(segment))
        xy = (transform @ np.array([[p.real, p.imag, 1] for p in points]).T).T[:, :2]
        if len(xy) < 3:
            continue
        if not np.allclose(xy[0], xy[-1], rtol=0, atol=1e-9):
            xy = np.vstack([xy, xy[0]])  # SVG fills implicitly close subpaths.
        signed_area = np.sum(xy[:-1, 0]*xy[1:, 1]-xy[1:, 0]*xy[:-1, 1]) / 2
        if abs(signed_area) <= 1e-10:
            continue
        body = make_valid(Polygon(xy))
        for p in polygons(body):
            rings.append((p, 1 if signed_area > 0 else -1))
    if not rings:
        return Polygon()
    fill_rule = inherited(node, 'fill-rule', parents, 'nonzero')
    # Polygonize all ring boundaries; preserve holes using the SVG fill rule.
    faces = polygonize(unary_union([p.boundary for p, _ in rings]))
    filled = []
    for face in faces:
        sample = face.representative_point()
        winding = sum(sign for p, sign in rings if p.covers(sample))
        include = winding % 2 != 0 if fill_rule == 'evenodd' else winding != 0
        if include:
            filled.append(face)
    return unary_union(filled)


def registration(root, parents):
    by_id = {n.get('id'): n for n in root.iter() if n.get('id')}
    controls = []
    for name, qid, circle_id, group_id in GCP:
        node = by_id.get(circle_id)
        if node is not None:
            position = world_matrix(node, parents) @ [float(node.get('cx')), float(node.get('cy')), 1]
        else:
            node = by_id[group_id]
            position = world_matrix(node, parents) @ [0, 0, 1]
        longitude, latitude = GCP_COORDINATES[name]
        controls.append(dict(name=name, qid=qid, svgNode=node.get('id'),
                             svgX=float(position[0]), svgY=float(position[1]),
                             longitude=longitude, latitude=latitude,
                             source='https://www.wikidata.org/wiki/' + qid))
    projector = Transformer.from_crs('EPSG:4326', PROJECTION, always_xy=True)
    design = np.array([[c['svgX'], c['svgY'], 1] for c in controls])
    target = np.array([projector.transform(c['longitude'], c['latitude']) for c in controls])
    coefficients = np.linalg.lstsq(design, target, rcond=None)[0]
    residuals = np.linalg.norm(design @ coefficients-target, axis=1)
    holdout = []
    for i in range(len(controls)):
        mask = np.arange(len(controls)) != i
        fit = np.linalg.lstsq(design[mask], target[mask], rcond=None)[0]
        holdout.append(float(np.linalg.norm(design[i] @ fit-target[i])))
    for i, c in enumerate(controls):
        c.update(residualMetres=round(float(residuals[i]), 2),
                 leaveOneOutMetres=round(holdout[i], 2))
    return coefficients, dict(projection=PROJECTION,
        projectionStatus='Fitted model; original SVG does not declare geographic CRS.',
        coefficients=coefficients.tolist(), controls=controls,
        meanResidualMetres=float(residuals.mean()), maxResidualMetres=float(residuals.max()),
        maxLeaveOneOutMetres=max(holdout))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    # This research preparer must never silently overwrite the atlas inputs.
    if (ROOT / 'public').resolve() in output.parents or (ROOT / 'src').resolve() in output.parents:
        parser.error('Research output must be outside public/ and src/.')
    snapshots = SNAPSHOTS
    inverse = Transformer.from_crs(PROJECTION, 'EPSG:4326', always_xy=True)
    features, audit = [], []
    common_coefficients, common_controls = None, None
    for snapshot in snapshots:
        source = args.input_dir/(snapshot['selected']+'.svg')
        raw = source.read_bytes()
        assert len(raw) == snapshot['size'], 'Unexpected archived SVG size'
        assert hashlib.sha256(raw).hexdigest() == snapshot['sha256'], 'Unexpected archived SVG revision'
        root = ET.fromstring(raw)
        parents = {c: p for p in root.iter() for c in p}
        coefficients, fit = registration(root, parents)
        if common_coefficients is None:
            common_coefficients = coefficients
            common_controls = np.array([[c['svgX'],c['svgY']] for c in fit['controls']])
        controls = np.array([[c['svgX'],c['svgY']] for c in fit['controls']])
        frame_deviation = float(np.max(np.linalg.norm(controls-common_controls, axis=1)))
        assert frame_deviation < .1, 'City scaffold changed: source needs independent registration'
        # Same verified source frame: prevent tiny city-label reorganisation from
        # masquerading as territorial change in otherwise identical control paths.
        coefficients = common_coefficients
        selected = []
        for n in root.iter():
            if n.tag.rsplit('}', 1)[-1] != 'path':
                continue
            ancestors, parent = [], n
            while parent is not None:
                ancestors.append(parent.tag.rsplit('}', 1)[-1]); parent = parents.get(parent)
            if any(t in ancestors for t in ('defs', 'clipPath', 'marker', 'pattern')):
                continue
            if inherited(n, 'fill', parents, 'black').lower() != OCCUPATION_FILL:
                continue
            if inherited(n, 'display', parents) == 'none':
                continue
            selected.append(n)
        pixel_geometry = unary_union([path_geometry(n, parents) for n in selected])
        def project(x, y, z=None):
            x, y = np.asarray(x), np.asarray(y)
            return (coefficients[0, 0]*x+coefficients[1, 0]*y+coefficients[2, 0],
                    coefficients[0, 1]*x+coefficients[1, 1]*y+coefficients[2, 1])
        projected = geometry_transform(project, pixel_geometry)
        geographical = unary_union(polygons(make_valid(geometry_transform(inverse.transform, projected))))
        assert geographical.is_valid and not geographical.is_empty
        year = int(snapshot['selected'][:4])
        uncertainty = max(5000, math.ceil(fit['maxLeaveOneOutMetres']/1000)*1000)
        properties = dict(uid=f'ukraine-russian-control-{year}', identityKey='RUS',
            controller='RUS', occupiedKey='UKR', kind='war', relation='occupation',
            start=year, end=year, observationDate=snapshot['geometryReferenceDate'],
            observationKind='cartographic-source-reference',
            reportedAssessmentDate=snapshot['reportedAssessmentDate'],
            sourceRevisionTimestamp=snapshot['sourceRevisionTimestamp'],
            dateEvidence=snapshot['dateEvidence'], selectedCut=snapshot['selected'],
            source=PAGE, sourceDownload=snapshot['url'], license='CC-BY-SA-4.0',
            licenseUrl=LICENSE, attribution='Viewsridge and Wikimedia Commons contributors; '
                'based on Rr016 and YakivGluck. Historicmap: extraction and georeferencing.',
            registrationUncertaintyMetres=uncertainty,
            note='Dated cartographic observation, not exact daily front; clip to Ukraine land before display. '
                 'No administrative claims or unobserved later front inferred.',
            sourcePathIds=[n.get('id') for n in selected])
        features.append(dict(type='Feature', properties=properties, geometry=mapping(geographical)))
        test_coordinates = [
            ('Kyiv', 30.5236, 50.45), ('Kharkiv', 36.2311, 49.9925),
            ('Odesa', 30.7325, 46.4842), ('Kherson', 32.6169, 46.6354),
            ('Zaporizhzhia', 35.1396, 47.8388), ('Sevastopol', 33.5254, 44.6167),
            ('Simferopol', 34.1000, 44.9484), ('Mariupol', 37.5494, 47.0971),
            ('Melitopol', 35.3675, 46.8489), ('Bakhmut', 38.0025, 48.5944),
            ('Avdiivka', 37.7427, 48.1399)]
        projector = Transformer.from_crs('EPSG:4326', PROJECTION, always_xy=True)
        tests = {}
        for name, lon, lat in test_coordinates:
            point = Point(*projector.transform(lon, lat))
            distance = projected.boundary.distance(point)
            tests[name] = dict(rawRussianControl=bool(geographical.covers(Point(lon, lat))),
                boundaryDistanceMetres=round(distance),
                withinRegistrationUncertainty=distance <= uncertainty)
        assert not any(tests[n]['rawRussianControl'] for n in ('Kyiv','Kharkiv','Odesa','Zaporizhzhia'))
        assert not tests['Kherson']['rawRussianControl'] or tests['Kherson']['withinRegistrationUncertainty']
        assert all(tests[n]['rawRussianControl'] for n in ('Sevastopol','Simferopol','Mariupol','Melitopol'))
        audit.append(dict(snapshot=snapshot, sha256=hashlib.sha256(raw).hexdigest(),
            selectedPathIds=properties['sourcePathIds'], registration=fit,
            appliedCommonCoefficients=coefficients.tolist(),
            maxCommonFrameCityDeviationPixels=frame_deviation,
            registrationUncertaintyMetres=uncertainty, polygonCount=len(polygons(geographical)),
            bounds=geographical.bounds, projectedAreaKm2=projected.area/1e6,
            sanityPointRussianControl=tests))
        print(year, snapshot['geometryReferenceDate'], properties['sourcePathIds'],
              'max error', round(fit['maxResidualMetres']), 'm', 'uncertainty', uncertainty,
              'area km2', round(projected.area/1e6))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(dict(type='FeatureCollection', features=features), ensure_ascii=False,
                                 separators=(',', ':')), encoding='utf-8')
    output.with_suffix('.audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Wrote research candidates:', output)


if __name__ == '__main__':
    main()
