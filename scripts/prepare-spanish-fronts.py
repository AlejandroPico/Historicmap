"""Prepare sourced Spanish Civil War control, without using provincial proxies.

Requires shapely==2.2.0, numpy>=2 and pyproj==3.7.2.
1936/1938: Cliopatria. 1937: Tyk's October 1937 SVG, georeferenced
against explicit city markers and coastal landmarks. See docs/SPANISH-CIVIL-WAR.md.
This script deliberately does not modify the global data manifest.
"""
import hashlib
import json
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.cache/python-packages'))
import numpy as np
from pyproj import Transformer
from shapely import make_valid
from shapely.geometry import Polygon, LineString, Point, shape, mapping
from shapely.ops import unary_union, linemerge, nearest_points, split

CACHE = ROOT / '.cache'
SVG_URL = 'https://upload.wikimedia.org/wikipedia/commons/e/eb/GCE-Frente_en_oct_1937.svg'
SVG_SHA = '9688ac765cfe53a1883db122fe0de956a0ba35edfe03dc126b730a0ec2bba83b'
SVG_PAGE = 'https://commons.wikimedia.org/wiki/File:GCE-Frente_en_oct_1937.svg'
CLIO_PAGE = 'https://github.com/Seshat-Global-History-Databank/cliopatria'
SVG = CACHE / 'spanish-front-1937.svg'
if not SVG.exists():
    request = urllib.request.Request(SVG_URL, headers={'User-Agent': 'Historicmap/0.4 (historical atlas)'})
    SVG.write_bytes(urllib.request.urlopen(request, timeout=60).read())
assert hashlib.sha256(SVG.read_bytes()).hexdigest() == SVG_SHA, 'Unexpected historical SVG revision'

clio_path = next((CACHE / 'cliopatria').glob('*.geojson'))
clio = json.loads(clio_path.read_text(encoding='utf8'))['features']
clio_sha = (CACHE / 'cliopatria-sha.txt').read_text(encoding='utf-8-sig').strip()

def polity(name, year):
    return next(f for f in clio if f['properties']['Name'] == name
                and f['properties']['FromYear'] <= year <= f['properties']['ToYear'])

def polygons(g):
    if g.geom_type == 'Polygon':
        return [g]
    return [p for child in getattr(g, 'geoms', []) for p in polygons(child)]

def european(g):
    # Explicit spatial scope: mainland Spain and Balearic Islands. Neither the
    # Canary inset in the SVG nor colonial areas are transferred into Europe.
    return unary_union([p for p in polygons(g) if 36 < p.centroid.y < 44.5 and -11 < p.centroid.x < 5])

natural = json.loads((ROOT / 'public/data/countries.geojson').read_text(encoding='utf8'))
spain = next(f for f in natural['features'] if f['properties'].get('code') == 'ESP')
# European Spanish exterior boundaries are stable over the four displayed years.
# Use the unmodified Natural Earth coastline (public domain), rather than the
# extremely coarse Cliopatria coast that excludes several actual coastal cities.
europe = european(make_valid(shape(spain['geometry'])))
mainland = max(polygons(europe), key=lambda p: p.area)
islands = europe.difference(mainland)

def coastal_front_partition(year):
    national = make_valid(shape(polity('Spanish Nationalists', year)['geometry']))
    republic = make_valid(shape(polity('Second Spanish Republic', year)['geometry']))
    shared = linemerge(national.boundary.intersection(republic.boundary))
    lines = list(shared.geoms) if hasattr(shared, 'geoms') else [shared]
    parts = polygons(europe)
    for line in lines:
        coords = list(line.coords)
        # Transfer ONLY published internal front lines. Join each source landfall
        # to the nearest point on the finer exterior boundary; no province proxy,
        # no displacement or smoothing of the interior front coordinates.
        ends = []
        for endpoint in (coords[0], coords[-1]):
            q = nearest_points(Point(endpoint), mainland.boundary)[1]
            distance = Point(endpoint).distance(q)
            assert distance < .3, (year, endpoint, 'source landfall too far from exterior')
            delta = np.array(q.coords[0]) - np.array(endpoint)
            length = np.linalg.norm(delta)
            # Continue a tiny distance outside the exterior so the split is robust
            # to floating-point boundary intersection precision.
            ends.append(tuple(np.array(q.coords[0]) + delta / max(length, 1e-9) * .001))
        cut = LineString([ends[0], *coords, ends[1]])
        parts = [p for previous in parts for p in polygons(split(previous, cut))]
    controlled = []
    for part in parts:
        point = part.representative_point()
        if point.distance(national) < point.distance(republic):
            controlled.append(part)
    result = unary_union(controlled)
    assert not result.is_empty
    return result

def svg_paths(d):
    """Decode the actual SVG commands; cubic curves sampled at eight steps.

    The front is a schematic historical reconstruction. Curve sampling does not
    represent additional historical precision and is not a coast replacement.
    """
    tokens = re.findall(r'[MLCz]|[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?\d+)?', d)
    cursor = 0
    line, lines, point = [], [], 0j
    while cursor < len(tokens):
        command = tokens[cursor]
        cursor += 1
        if command == 'z':
            if line:
                lines.append(line)
                line = []
        elif command in ('M', 'L'):
            point = complex(float(tokens[cursor]), float(tokens[cursor + 1]))
            cursor += 2
            if command == 'M' and line:
                lines.append(line)
                line = []
            line.append((point.real, point.imag))
        elif command == 'C':
            b, c, end = [complex(float(tokens[cursor + j]), float(tokens[cursor + j + 1])) for j in (0, 2, 4)]
            cursor += 6
            for t in (j / 8 for j in range(1, 9)):
                q = (1-t)**3 * point + 3*(1-t)**2*t*b + 3*(1-t)*t*t*c + t**3*end
                line.append((q.real, q.imag))
            point = end
        else:
            raise ValueError(f'Unsupported source command {command}')
    if line:
        lines.append(line)
    return lines

# Pixel positions are the centres of named city markers in the source SVG,
# after its ancestor transforms. Landmark coordinates are independently stated
# control points, not a purported CRS supplied by the historical map author.
CONTROL_POINTS = [
    ('Madrid', 311.429, 233.557, -3.7038, 40.4168),
    ('Bilbao', 342.857, 57.129, -2.935, 43.263),
    ('Oviedo', 207.5, 51.771, -5.8494, 43.361),
    ('Barcelona', 585, 169.271, 2.1734, 41.3851),
    ('Sevilla', 189.286, 419.986, -5.9845, 37.3891),
    ('Valencia', 468.571, 292.843, -.3763, 39.4699),
    ('Málaga', 267.857, 464.986, -4.4213, 36.7213),
    ('Zaragoza', 439.213, 160.973, -.8891, 41.6488),
    ('Murcia', 437.143, 388.557, -1.1307, 37.9922),
    ('Granada', 315.168, 435.965, -3.5986, 37.1773),
    ('Gijón', 215.714, 35.7, -5.6611, 43.5357),
    ('Cabo da Roca', 25.524582, 326.85174, -9.5001, 38.7806),
    ('Cap de Creus', 637.27982, 105.62061, 3.3249, 42.3189),
    ('Estaca de Bares', 130.14086, 18.38259, -7.6888, 43.7917),
    ('Tarifa', 210.19574, 510.87666, -5.6109, 36.0004),
]
LCC = '+proj=lcc +lat_1=40 +lat_2=43 +lon_0=-3 +datum=WGS84'
project = Transformer.from_crs(4326, LCC, always_xy=True)
unproject = Transformer.from_crs(LCC, 4326, always_xy=True)
pixels = np.array([[x, y, 1] for _, x, y, _, _ in CONTROL_POINTS])
world = np.array([project.transform(lon, lat) for _, _, _, lon, lat in CONTROL_POINTS])
affine = np.linalg.lstsq(pixels, world, rcond=None)[0]
residuals = np.linalg.norm(pixels @ affine - world, axis=1)
registration = dict(method='affine in stated LCC frame; 15 city/coastal control points',
                    meanResidualMetres=round(float(residuals.mean())),
                    maxResidualMetres=round(float(residuals.max())),
                    minimumRegistrationUncertaintyMetres=10000,
                    sourceDate='1937-10', sourceSha256=SVG_SHA)

root = ET.parse(SVG).getroot()
front_element = next(e for e in root.iter() if e.attrib.get('id') == 'path8971')
source_ring = max(svg_paths(front_element.attrib['d']), key=len)
# Ancestor translations cancel: -12.33713 -89.805734 +90.467805 +11.675059 = 0.
# Vertical sum is -0.000004 pixels; retained explicitly.
source_ring = [(x, y - .000004) for x, y in source_ring]
assert len(source_ring) == 4852
# Internal front, from its Mediterranean landfall to the Pyrenean border.
# Indices refer to the fixed source and the documented curve sampling above.
internal_front = source_ring[2893:3414]
front = []
for x, y in internal_front:
    px, py = np.array([x, y, 1]) @ affine
    front.append(unproject.transform(px, py))
# Close outside the European land area, avoiding registration artefacts along
# coasts. Only the published internal front divides the two land control areas.
mask = make_valid(Polygon(front + [(front[-1][0], 47), (-15, 47), (-15, 33), (front[0][0], 33)]))
national_38 = coastal_front_partition(1938)
national_37 = mask.intersection(mainland).union(national_38.intersection(islands))

features = []
for year in (1936, 1937, 1938, 1939):
    if year == 1937:
        national = national_37
    elif year == 1939:
        national = europe
    else:
        national = coastal_front_partition(year)
    republic = europe.difference(national)
    for key, name, original_name, colour, geom in [
        ('ESP-NATIONALIST', 'España · zona sublevada' if year < 1939 else 'España · victoria franquista', 'Spanish Nationalists' if year < 1939 else 'Francoist Spain', '#b7914e', national),
        ('ESP-REPUBLIC', 'España · zona republicana', 'Second Spanish Republic', '#9b688f', republic),
    ]:
        if geom.is_empty:
            continue
        props = dict(uid=f'spain-{year}-{key}', name=name, originalName=original_name,
                     identityKey=key if year<1939 else 'ESP', controller=key, controlColor=colour, kind='civil-war',
                     start=year, end=year, source=SVG_PAGE if year == 1937 else CLIO_PAGE,
                     license='CC-BY-SA-3.0' if year == 1937 else 'CC-BY-4.0',
                     sourceDate='1937-10' if year == 1937 else f'{year} (síntesis anual)',
                     note=('Control territorial aproximado en octubre de 1937: caída del frente norte y de Málaga. '
                           'Georreferenciación del mapa de Tyk; incertidumbre de registro de al menos 10 km. '
                           'No es un frente diario ni una instantánea exacta del 31 de diciembre.' if year == 1937 else
                           'Síntesis territorial anual de Cliopatria, sin día uniforme. ' +
                           ('La guerra termina el 1 de abril de 1939 con la victoria del bando sublevado.' if year == 1939 else
                            'La fuente original agrupa 1936–1937; aquí el año 1937 tiene una reconstrucción propia.')),
                     spatialScope='España peninsular e islas Baleares; sin colonias ni Canarias',
                     attribution=('Tyk / Té y kriptonita, 2009, CC BY-SA 3.0; georreferenciado y recortado para Historicmap. '
                                  'Control insular: Cliopatria / Seshat, CC BY 4.0. Costa: Natural Earth, dominio público.' if year == 1937 else
                                  'Frentes: Cliopatria / Seshat Global History Databank, CC BY 4.0; costa: Natural Earth, dominio público. Adaptación cartográfica europea.'))
        features.append(dict(type='Feature', id=800000 + len(features), geometry=mapping(geom), properties=props))

out = dict(type='FeatureCollection', features=features,
           metadata=dict(cliopatriaVersion=clio_sha, cliopatriaSha256=hashlib.sha256(clio_path.read_bytes()).hexdigest(),
                         svgUrl=SVG_URL, svgPage=SVG_PAGE, registration=registration,
                         naturalEarthCoastSha256=hashlib.sha256((ROOT / 'public/data/countries.geojson').read_bytes()).hexdigest(),
                         transformation='European Natural Earth exterior; published Cliopatria internal fronts and source internal front for October 1937; source landfalls joined to nearest finer coastline; no provincial proxies.'))
path = ROOT / 'public/data/spanish-civil-war.geojson'
path.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf8', newline='\n')
assert len(features) == 7
print(path.name, path.stat().st_size, 'bytes;', len(features), 'records;', registration)
for year in (1936, 1937, 1938, 1939):
    fs = [f for f in features if f['properties']['start'] == year]
    assert all(shape(f['geometry']).is_valid for f in fs)
    if len(fs) == 2:
        assert shape(fs[0]['geometry']).intersection(shape(fs[1]['geometry'])).area < 1e-8
    area = shape(fs[0]['geometry']).area / europe.area
    print(year, 'nationalist share of source extent', round(area * 100, 1), '%')

# Geographic regression checks use inland points to avoid coastline tolerance.
def controller(year, coordinate):
    return next(f['properties']['controller'] for f in features
                if f['properties']['start'] == year and shape(f['geometry']).covers(Point(coordinate)))

for year in (1936, 1937, 1938):
    assert controller(year, (-3.7038, 40.4168)) == 'ESP-REPUBLIC'  # Madrid
    assert controller(year, (2.1734, 41.3851)) == 'ESP-REPUBLIC'   # Barcelona
assert controller(1936, (-2.935, 43.263)) == 'ESP-REPUBLIC'        # Bilbao
assert controller(1937, (-2.935, 43.263)) == 'ESP-NATIONALIST'
assert controller(1936, (-5.6611, 43.5357)) == 'ESP-REPUBLIC'      # Gijón
assert controller(1937, (-5.6611, 43.5357)) == 'ESP-NATIONALIST'
assert controller(1936, (-4.4213, 36.7213)) == 'ESP-REPUBLIC'      # Málaga
assert controller(1937, (-4.4213, 36.7213)) == 'ESP-NATIONALIST'
assert controller(1939, (-3.7038, 40.4168)) == 'ESP-NATIONALIST'
print('Spanish control geography and non-overlapping partitions verified.')
