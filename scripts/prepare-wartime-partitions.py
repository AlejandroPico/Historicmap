"""Build one land ownership partition for each1940–1944 annual selection.

Run export-wartime-inputs.ts first. CShapes coast/borders are the common mesh;
Cliopatria supplies interior control cuts, never an independent coastline.
Source files remain immutable. No Spanish BY-SA fronts enter this derivative.
Requires Shapely2.2 in the local preparation runtime. See WWII-PARTITIONS.md.
"""
import hashlib
import json
import pathlib
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.cache/python-packages'))
from shapely import make_valid
from shapely.geometry import shape, mapping, GeometryCollection
from shapely.ops import unary_union

OUT = ROOT / 'public/data'
TAG = 'shared-land-partition-0.12.1'
SOURCE = 'https://github.com/Seshat-Global-History-Databank/cliopatria'

def polygons(g):
    if g.is_empty:
        return []
    if g.geom_type == 'Polygon':
        return [g]
    return [p for child in getattr(g, 'geoms', []) for p in polygons(child)]

def valid(g):
    return unary_union(polygons(make_valid(g)))

def union(gs):
    return valid(unary_union(list(gs)))

def geometry(g):
    # Keep all original vertices; no simplification, smoothing or grid snapping.
    return mapping(g)

def prepare(year):
    incoming = json.loads((ROOT / f'.cache/wartime/input-{year}.json').read_text(encoding='utf8'))
    base = incoming['base']['features']
    originals = {f['id']: valid(shape(f['geometry'])) for f in base}
    properties = {f['id']: dict(f['properties']) for f in base}
    states = dict(originals)
    key_ids = {p['identityKey']: i for i,p in properties.items()}
    land = union(originals.values())
    # Components of the *whole land mesh*, not country fragments. A little
    # landlocked state is never mistaken for an island. Retain small sourced
    # pieces only on actual offshore land; never delete all small polygons.
    offshore = union(p for p in polygons(land) if p.area < 2)
    controls = [f for f in incoming['controls']['features'] if f['properties']['kind'] != 'annexation-mask']
    audits = []
    incorporation = GeometryCollection()

    def land_for(keys):
        return union(g for i,g in originals.items() if properties[i]['identityKey'] in keys)

    def transfer(mask, p):
        nonlocal incorporation
        controller = p['controller']
        anchor = key_ids.get(controller)
        if anchor is None:
            anchor = 6200000 + len(key_ids)
            key_ids[controller] = anchor
            properties[anchor] = dict(p, identityKey=controller)
            states[anchor] = GeometryCollection()
        acquired = []
        for i,g in list(states.items()):
            if i == anchor or g.is_empty or not g.intersects(mask):
                continue
            cut = valid(g.intersection(mask))
            if cut.is_empty:
                continue
            states[i] = valid(g.difference(cut))
            acquired.append(cut)
        states[anchor] = union([states[anchor], *acquired])
        q = properties[anchor]
        q.update(identityKey=controller, controller=controller,
                 controlComponent=True, controlName=p['name'],
                 controlRecord=p.get('uid', TAG), controlNote=p['note'],
                 controlSource=p['source'], controlCorrection=TAG)
        q.pop('uid', None)

    # Extend the documented1939 Czech/Slovak split; reuse the same reference
    # interior cut, clipped to CShapes, rather than drawing a second coastline.
    reference = json.loads((OUT / 'central-europe-1939.geojson').read_text(encoding='utf8'))
    slovak_source = next(f for f in reference['features'] if f['properties']['controller'] == 'SVK-1939')
    hungarian_source = next(f for f in reference['features'] if f['properties']['controller'] == 'HUN')
    czech = land_for({'CSK'})
    hungarian = valid(czech.intersection(shape(hungarian_source['geometry'])).difference(shape(slovak_source['geometry'])))
    slovakia = valid(czech.intersection(shape(slovak_source['geometry'])).difference(hungarian))
    slovak_props = dict(slovak_source['properties'], start=year, end=year,
                        note='Continuidad del Estado eslovaco cliente desde1939. Corte interior de referencia, no frontera municipal exacta. ' + slovak_source['properties']['note'])
    transfer(slovakia, slovak_props)
    if not hungarian.is_empty:
        transfer(hungarian, dict(hungarian_source['properties'], start=year, end=year))
    czech_occupied = valid(czech.difference(union([slovakia, hungarian])))

    # Resolve documentary control first, then clients/local institutions. This
    # ordering is explicit; optional hatch visibility never changes ownership.
    order = {'USSR': 0, 'JPN': 1, 'DEU': 2, 'ITA': 3, 'FRA-VICHY': 4,
             'CROATIA-CLIENT': 5, 'CHN-COMMUNIST': 6}
    for source in sorted(controls, key=lambda f: order[f['properties']['controller']]):
        p = dict(source['properties'])
        key = p['controller']
        raw = valid(shape(source['geometry']))
        parts = polygons(raw)
        # Large connected source regions retain their interior fronts. Small
        # disconnected cells must be supported by offshore land, not be merely
        # valid quadrilaterals in Karelia, Sweden, Syria or the Italian mainland.
        core = union(g for g in parts if g.area >= .25)
        islands = union(g.intersection(offshore) for g in parts if g.area < .25)
        mask = union([core, islands])
        if key == 'DEU':
            allowed = {'DEU','AUT','CSK','POL','DNK','NOR','NLD','BEL','LUX','FRA','USSR'}
            if year >= 1941:
                allowed |= {'YKM','YUG','GRC'}
            if year in (1941,1942,1943):
                allowed |= {'Libya','Tunisia'}
            if year >= 1943:
                allowed.add('ITA')
            if year == 1944:
                allowed |= {'HUN','SVK-1939'}
            mask = valid(mask.intersection(land_for(allowed)))
            # Complete, documented occupations use the original dated coast.
            whole = {'AUT','DNK'} | ({'NOR','NLD','BEL','LUX'} if year <= 1943 else set())
            mask = union([mask, land_for(whole), czech_occupied])
            if year <= 1943:
                mask = valid(mask.difference(slovakia))
            # Austria is incorporation; remaining Czech lands are occupation.
            incorporation = land_for({'DEU','AUT'})
            original1938 = next(f for f in incoming['controls']['features'] if f['properties']['kind'] == 'annexation-mask')
            sudeten_core = union(g for g in polygons(valid(shape(original1938['geometry']))) if g.area >= .25)
            incorporation = union([incorporation, sudeten_core.intersection(land_for({'CSK'})).difference(czech)])
        elif key == 'ITA':
            mask = valid(mask.intersection(land_for({'ITA','ALB','YKM','YUG','GRC','FRA','Libya','Ethiopia','Eritrea','Italian Somaliland'})))
        elif key == 'USSR':
            mask = valid(mask.intersection(land_for({'USSR','POL','FIN','EST','LVA','LTU','ROU'})))
        elif key == 'CROATIA-CLIENT':
            mask = valid(core.intersection(land_for({'YKM','YUG'})))
        elif key == 'CHN-COMMUNIST':
            mask = valid(core.intersection(land_for({'ROC','CHN'})))
        elif key == 'FRA-VICHY':
            # Retain the source's annual phase, without relabelling it as an
            # exact31December front. November1942 needs an independent phase.
            mask = valid(mask.intersection(union(g for i,g in originals.items() if properties[i].get('administratorKey') == 'FRA' or properties[i]['identityKey'] == 'FRA')))
        else:  # Japanese cuts retain their source theatre and original islands.
            mask = valid(mask.intersection(land))
        p['note'] += ' Costa y límites compartidos con la base terrestre fechada; control anual de fuente, no frente exacto del31 de diciembre.'
        p['start'] = p['end'] = year
        audits.append(dict(controller=key, rawComponents=len(parts), coreComponents=len(polygons(core)),
                           rawArea=raw.area, transferredMaskArea=mask.area,
                           outsideLandArea=mask.difference(land).area))
        transfer(mask, p)

    # Exact complements can still leave zero-area GEOS boundary remnants in
    # the predecessor. Assign its remaining land to the Czech occupation,
    # rather than retaining a selectable Czechoslovakia made of roundoff.
    if 'CSK' in key_ids:
        old, german = key_ids['CSK'], key_ids['DEU']
        states[german] = union([states[german], states[old]])
        states[old] = GeometryCollection()

    # Generate hatching only after the final partition. A Croatian client or
    # a later transfer cannot retain an earlier German hatch above its geometry.
    occupations = []
    control_by_key = {f['properties']['controller']: f['properties'] for f in controls}
    for key,p in control_by_key.items():
        if p.get('relation') in ('client','civil-war','incorporation'):
            continue
        target = states[key_ids[key]]
        for i,g in originals.items():
            q = properties[i]
            if q['identityKey'] == key or q.get('administratorKey') == key:
                continue
            cut = valid(target.intersection(g))
            if key == 'DEU':
                cut = valid(cut.difference(incorporation))
            if cut.is_empty:
                continue
            occupations.append(dict(type='Feature', id=7400000+len(occupations), geometry=geometry(cut),
                                    properties=dict(p, start=year,end=year,occupiedKey=q['identityKey'],
                                                    occupiedName=q['name'],occupiedColor=q['politicalColor'],
                                                    controlCorrection=TAG)))

    replaced = [i for i,g in originals.items() if not g.equals(states[i]) or properties[i].get('controlCorrection') == TAG]
    features = [dict(type='Feature',id=i,properties=properties[i],geometry=geometry(g)) for i,g in states.items()
                if not g.is_empty and (i in replaced or i not in originals)]
    final = union(states.values())
    overlap = sum(g.area for g in states.values()) - final.area
    missing, extra = land.difference(final).area, final.difference(land).area
    # GEOS roundoff is tolerated, but no missing country or unbounded overlay.
    assert missing < 1e-7 and extra < 1e-7, (year,missing,extra)
    # Existing CShapes tiny seams may already overlap; the derivative must not
    # create a new overlap. Do not silently delete licensed baseline detail.
    baseline_overlap = sum(g.area for g in originals.values()) - land.area
    assert overlap <= baseline_overlap + 1e-7, (year,overlap,baseline_overlap)
    german = states[key_ids['DEU']]
    protected = {key: german.intersection(land_for({key})).area for key in ('SWE','CHE','FIN','TUR','Syria','IRQ','IRN')}
    if year <= 1942:
        protected['ITA'] = german.intersection(land_for({'ITA'})).area
    assert all(a < 1e-8 for a in protected.values()), (year,protected)
    hatch_leaks = sum(shape(f['geometry']).difference(states[key_ids[f['properties']['controller']]]).area for f in occupations)
    assert hatch_leaks < 1e-8, (year,hatch_leaks)
    return dict(replaceIds=replaced, territories=dict(type='FeatureCollection',features=features),
                occupations=dict(type='FeatureCollection',features=occupations)), dict(year=year,controls=audits,
                replaced=len(replaced),features=len(features),hatches=len(occupations),
                missingLandArea=missing,extraLandArea=extra,newOverlapArea=max(0,overlap-baseline_overlap),
                protectedGermanIntersectionArea=protected,hatchOutsideFinalControllerArea=hatch_leaks)

def main():
    years, audit = {}, []
    for year in range(1940,1945):
        years[str(year)], report = prepare(year)
        audit.append(report)
        print(year,report['features'],'replacement territories;',report['hatches'],'final hatches',flush=True)
    result = dict(format='dated-control-partitions',version=TAG,years=years,
                  source=SOURCE,license='CC BY-NC-SA 4.0 (CShapes derivative); Cliopatria attribution CC BY 4.0; Natural Earth public domain',
                  method='Shared dated land mesh; source interior cuts; bounded remote-component rejection; final-owner hatching. Annual synthesis, not daily fronts.')
    path = OUT / 'wartime-partitions.json'
    path.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    (ROOT/'docs/WWII-PARTITIONS-AUDIT.json').write_text(json.dumps(dict(version=TAG,years=audit),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(path.name,path.stat().st_size,'bytes',hashlib.sha256(path.read_bytes()).hexdigest())

if __name__ == '__main__':
    main()
