"""Pure extraction of Pacific island components already present in Cliopatria.

Natural Earth is used only as a local identification envelope. No NE coordinates
are rendered, no polygon is clipped, and the extracted components are removed
from the aggregate source feature. This module never writes public/ or src/.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from typing import Any
import json
from pathlib import Path


SPLITS = {
    'GUM': {
        'name': 'Guam', 'ownerName': 'España',
        'sourceNames': {'Spanish Empire', 'First Spanish Republic', 'Kingdom of Spain'},
        'padding': 0.25,
    },
    'NCL': {
        'name': 'Nueva Caledonia', 'ownerName': 'Francia',
        'sourceNames': {'French Indochina'}, 'padding': 0.25,
    },
}


def _polygons(geometry: dict[str, Any]) -> list:
    if geometry['type'] == 'MultiPolygon':
        return geometry['coordinates']
    if geometry['type'] == 'Polygon':
        return [geometry['coordinates']]
    return []


def _bbox(polygons: list) -> tuple[float, float, float, float]:
    points = [point for polygon in polygons for ring in polygon for point in ring]
    return (min(p[0] for p in points), min(p[1] for p in points),
            max(p[0] for p in points), max(p[1] for p in points))


def _geometry(polygons: list) -> dict:
    # Coordinates and ring ordering remain exactly the source coordinates.
    return {'type': 'Polygon', 'coordinates': polygons[0]} if len(polygons) == 1 else {
        'type': 'MultiPolygon', 'coordinates': polygons}


def _components(data: dict) -> Counter:
    return Counter(json.dumps(p, separators=(',', ':'))
                   for f in data['features'] for p in _polygons(f['geometry']))


def split_source_components(data: dict, year: int | None, refs: dict[str, dict]) -> dict:
    """Return a deep copy with GUM/NCL source components assigned local identity.

    `refs` maps GUM/NCL to contemporary NE GeoJSON features. `year` is the active
    year (1840–1885); None prepares all source snapshots intersecting this range.
    The feature collection may be a single active snapshot or the full source.
    Derived feature IDs are unique; sourceFeatureId retains the exact source ID.
    """
    result = deepcopy(data)
    if year is not None and not 1840 <= year <= 1885:
        return result
    envelopes = {}
    for code, spec in SPLITS.items():
        if code not in refs:
            continue
        lo, la, hi, ha = _bbox(_polygons(refs[code]['geometry']))
        pad = spec['padding']
        envelopes[code] = (lo-pad, la-pad, hi+pad, ha+pad)

    out = []
    for feature in result['features']:
        p = feature.get('properties') or {}
        start, end = int(p.get('start', -999999)), int(p.get('end', 999999))
        active = start <= year <= end if year is not None else end >= 1840 and start <= 1885
        if not active or p.get('sourceComponentExtraction'):
            out.append(feature)
            continue
        polys = _polygons(feature['geometry'])
        extracted: dict[str, list[tuple[int, list]]] = {}
        kept = []
        source_name = p.get('originalName') or p.get('name')
        for index, polygon in enumerate(polys):
            a,b,c,d = _bbox([polygon])
            matches = [code for code,box in envelopes.items()
                       if source_name in SPLITS[code]['sourceNames']
                       and box[0] <= a <= c <= box[2]
                       and box[1] <= b <= d <= box[3]]
            if len(matches) > 1:
                raise ValueError(f'Ambiguous Pacific component: {feature.get("id")}:{index}')
            if matches:
                extracted.setdefault(matches[0], []).append((index,polygon))
            else:
                kept.append(polygon)
        if not extracted:
            out.append(feature)
            continue
        source_id = feature.get('id')
        if source_id is None:
            raise ValueError('Source feature ID required for provenance')
        if kept:
            feature['geometry'] = _geometry(kept)
            out.append(feature)
        for code, components in extracted.items():
            spec = SPLITS[code]
            properties = deepcopy(p)
            properties.update(
                name=spec['name'], originalName=spec['name'], code='',
                entityCode=code, identityKey=code, status='colony',
                ownerName=spec['ownerName'], parentName=source_name,
                politicalStatus='Dependencia colonial · componente de la geometría histórica',
                sourceFeatureId=source_id, sourceOriginalName=source_name,
                sourceComponentIndexes=[i for i,_ in components],
                sourceComponentExtraction=True, sourceGeometryUnchanged=True,
                territorialReference=False,
                componentIdentificationSource='Natural Earth 1:10m · envolvente local; no geometría de sustitución',
                note='Componente extraído del agregado histórico y retirado de él, conservando sus coordenadas. La envolvente contemporánea sólo identifica la isla; no proyecta fronteras ni autoridades actuales.')
            out.append({'type':'Feature','id':f'{source_id}::pacific::{code}',
                        'geometry':_geometry([poly for _,poly in components]),'properties':properties})
    result['features'] = out
    if _components(data) != _components(result):
        raise AssertionError('Polygon components changed during source partition')
    ids=[f.get('id') for f in out if f.get('id') is not None]
    if len(ids) != len(set(ids)):
        raise AssertionError('Duplicate source/derived feature IDs')
    return result


if __name__ == '__main__':
    root=Path(__file__).resolve().parents[1]
    read=lambda file:json.loads((root/'public/data'/file).read_text(encoding='utf8'))
    refs={f['properties']['code']:f for f in read('countries.geojson')['features']
          if f['properties'].get('code') in SPLITS}
    result=split_source_components(read('early-modern.geojson'),None,refs)
    target=root/'.cache/pacific-014-clio-components.geojson'
    target.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8')
    summary=[{'id':f['id'],**{k:f['properties'][k] for k in ['entityCode','start','end','sourceFeatureId','sourceOriginalName','sourceComponentIndexes']}}
             for f in result['features'] if f['properties'].get('sourceComponentExtraction')]
    (root/'.cache/pacific-014-clio-component-index.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
