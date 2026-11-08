"""Prepare the dated ICS vocabulary from the byte-pinned, attributed research input."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'Tierra/Investigacion/parte-1/originales/ics-chart.ttl'
TARGET = ROOT / 'Tierra/Cronologia/ics-2026-06.json'


def prepare():
    raw = SOURCE.read_bytes()
    text = raw.decode('utf-8')
    assert 'owl:versionInfo "2026-06"' in text
    ranks = {'Eon': 'eon', 'Era': 'era', 'Period': 'period', 'Epoch': 'epoch', 'Age': 'age', 'Sub': 'subperiod', 'Super': 'group'}
    units = []
    for key, block in re.findall(r'(?ms)^gtsd:([^\s]+)\n(.*?)(?=^\S|\Z)', text):
        rank_list = re.search(r'gts:rank\s+((?:rank:\w+\s*,\s*)*rank:\w+)', block)
        if not rank_list:
            continue
        found = re.findall(r'rank:(\w+)', rank_list[1])
        # Přídolí figura a la vez como serie y piso (no tiene pisos): se clasifica como serie.
        rank = [None, 'Epoch' if 'Epoch' in found else found[0]]
        ages = re.findall(r'gtsd:inMYA ([\d.]+)', block)
        assert len(ages) == 2, key
        pref = re.search(r'skos:prefLabel\s+(.*?);', block, re.S)
        label = re.search(r'"([^"]+)"@es(?=\s|,)', pref[1]) if pref else None
        parent = re.search(r'skos:broader gtsd:([^ ;]+)', block)
        color = re.search(r'schema:color "(#[\dA-Fa-f]{6})"', block)
        def uncertainty(edge):
            value = re.search(r'time:has' + edge + r'\s*\[(.*?)\]', block, re.S)
            error = re.search(r'schema:marginOfError ([\d.]+)', value[1]) if value else None
            return float(error[1]) if error else None
        units.append({'id': key, 'name': label[1] if label else '', 'rank': ranks[rank[1]], 'parent': parent[1] if parent else None,
                      'oldestMa': float(ages[0]), 'youngestMa': float(ages[1]), 'color': color[1] if color else '#a7b2ab',
                      'formal': rank[1] != 'Super' and key not in ['UpperPleistocene', 'CambrianStage2', 'CambrianStage3', 'CambrianStage4', 'CambrianStage10', 'CambrianSeries2'],
                      'gsspRatified': 'gts:ratifiedGSSP true' in block,
                      'numericalUncertaintyMa': {'oldest': uncertainty('Beginning'), 'youngest': uncertainty('End')},
                      'source': 'https://stratigraphy.org/ICSchart/ChronostratChart2026-06.pdf'})
    by_id = {unit['id']: unit for unit in units}
    for unit in units:
        if not unit['name']:
            for prefix, word in [('Lower', 'inferior'), ('Middle', 'medio'), ('Upper', 'superior')]:
                if unit['id'].startswith(prefix):
                    unit['name'] = by_id[unit['id'][len(prefix):]]['name'] + ' ' + word
                    break
        assert unit['name'], unit['id']
        assert unit['oldestMa'] > unit['youngestMa'] >= 0, unit['id']
        unit['timeBasis'] = 'Ma · eje nominal BP1950; edades numéricas aproximadas'
        unit['axisOldestYear'] = 1949 - round(unit['oldestMa'] * 1e6)
        unit['axisEndYear'] = 1949 - round(unit['youngestMa'] * 1e6) if unit['youngestMa'] else None
    # Keep GSSP ages already curated in the project, rather than treating rounded
    # chart labels (4.2/8.2ka) as more precise values with a different epoch.
    precise = {'Holocene': (11700, 0), 'Greenlandian': (11700, 8236), 'Northgrippian': (8236, 4250), 'Meghalayan': (4250, 0)}
    for key, (start, end) in precise.items():
        unit = by_id[key]
        unit.update({'axisOldestYear': 1999 - start, 'axisEndYear': 1999 - end if end else None,
                     'timeBasis': 'GSSP · años b2k2000; no BP1950', 'axisSource': 'https://doi.org/10.1002/jqs.3097'})
    for unit in units:
        if unit['youngestMa'] == .0117:
            unit['axisEndYear'] = by_id['Holocene']['axisOldestYear']
            unit['axisEndSource'] = 'https://doi.org/10.1002/jqs.3097'
    # El RDF oficial 2026-06 da al Ludlow el techo del Přídolí (419,62 Ma); la carta lo cierra en la base
    # del Přídolí (422,7 Ma), que es también el techo del Ludfordiense.
    if by_id['Ludlow']['youngestMa'] == by_id['Pridoli']['youngestMa']:
        ludlow = by_id['Ludlow']
        ludlow['youngestMa'] = by_id['Pridoli']['oldestMa']
        ludlow['numericalUncertaintyMa']['youngest'] = by_id['Pridoli']['numericalUncertaintyMa']['oldest']
        ludlow['axisEndYear'] = by_id['Pridoli']['axisOldestYear']
    for unit in units:
        parent = by_id.get(unit['parent'])
        if parent:
            assert parent['axisOldestYear'] <= unit['axisOldestYear'], unit['id']
            assert parent['axisEndYear'] is None or (unit['axisEndYear'] is not None and parent['axisEndYear'] >= unit['axisEndYear']), unit['id']
    assert len(units) == 178
    return {'schemaVersion': 1, 'version': '2026/06', 'license': 'CC-BY-4.0',
            'attribution': 'International Commission on Stratigraphy · Cohen, Harper, Gibbard & Car (2025, actualizado2026/06)',
            'sourceSha256': hashlib.sha256(raw).hexdigest(), 'rdfVersion': '2026-06', 'rdfModified': '2026-06-20',
            'reconciliation': 'La cita inglesa Modified2024-12 es antigua; owl:versionInfo y versionIRI identifican2026-06. El límite Hádico/Arcaico4031Ma y demás valores proceden de esta versión. Holoceno usa edades GSSP b2k ya curadas, conservando cifras redondeadas de carta por separado. Přídolí, serie y piso a la vez en el RDF, se clasifica como serie; el techo del Ludlow, que el RDF iguala al del Přídolí (419,62 Ma), se corrige a 422,7 Ma como en la carta.',
            'axisConvention': 'Intervalos [inicio,fin), presente abierto. Ma se sitúa nominalmente respecto1950; no es precisión calendárica. Holoceno/GSSP tiene base2000 explícita. Sin año cero.',
            'units': sorted(units, key=lambda u: (-u['oldestMa'], u['rank'], u['id']))}


if __name__ == '__main__':
    result = prepare()
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if '--check' in sys.argv:
        assert TARGET.read_text(encoding='utf-8') == serialized, 'Chronology is out of date'
        print('ICS2026/06:178 units, hierarchy and b2k reconciliation verified')
    else:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(serialized, encoding='utf-8', newline='\n')
        print('Prepared', TARGET.relative_to(ROOT))
