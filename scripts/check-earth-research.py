"""Validate the published part-1 research ledger without private media or extra packages."""
from pathlib import Path
import csv
import hashlib
import json
import re


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'Tierra' / 'Investigacion' / 'parte-1'


def read(name):
    return json.loads((AUDIT / name).read_text(encoding='utf-8'))


def check(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = read('procedencia.json')
    for entry in manifest['inputs']:
        path = AUDIT / entry['file']
        check(path.stat().st_size == entry['bytes'], 'Original size: ' + entry['file'])
        check(digest(path) == entry['sha256'], 'Original checksum: ' + entry['file'])
    chronology = manifest['officialChronology']
    for file_key, hash_key in [('chartSnapshot', 'chartSha256'), ('rdfSnapshot', 'rdfSha256')]:
        check(digest(AUDIT / chronology[file_key]) == chronology[hash_key], 'ICS checksum: ' + file_key)

    sources = read('fuentes.json')['sources']
    source_ids = {source['id'] for source in sources}
    check(len(source_ids) == len(sources), 'Duplicate source identifier')
    check(all(source['url'].startswith('https://') for source in sources), 'Source URL')

    def check_refs(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == 'sourceId':
                    check(child in source_ids, 'Unknown reference: ' + child)
                elif key == 'sourceIds':
                    check(set(child) <= source_ids, 'Unknown references: ' + str(child))
                check_refs(child)
        elif isinstance(value, list):
            for child in value:
                check_refs(child)

    hominins = read('comparacion-homininos.json')
    names = re.findall(r'^\* \*\*(.*?)\*\*', (AUDIT / 'originales/homininos-gemini.md').read_text(encoding='utf-8'), re.M)
    entries = hominins['entries']
    check(len(entries) == hominins['inputEntryCount'] == len(names) == 38, 'Incomplete input crosswalk')
    check([row['inputLabel'] for row in entries] == [name.rstrip(':') for name in names], 'Input order/name drift')
    check([row['inputIndex'] for row in entries] == list(range(1, 39)), 'Input index coverage')
    current_keys = {json.loads(p.read_text(encoding='utf-8'))['key'] for p in (ROOT / 'Tierra/Humanidad/linajes').glob('*/linaje.json')}
    check(all(row['canonicalKey'] is None or row['canonicalKey'] in current_keys for row in entries), 'Missing lineage reference')
    check(all(row['implementedHere'] is False for row in entries), 'Research advertised as implementation')
    check_refs(hominins)

    ice = read('comparacion-glaciaciones.json')
    check(len(ice['entries']) == ice['inputEntryCount'] == 11, 'Incomplete glaciation crosswalk')
    check(ice['fixedNumberOfEarthIceAges'] is None, 'Unjustified fixed count of ice ages')
    check_refs(ice)

    video = read('inventario-video.json')
    check(len(video['events']) == video['eventCount'] == 198, 'Event count drift')
    check(len({event['id'] for event in video['events']}) == len(video['events']), 'Duplicate event IDs')
    for event in video['events']:
        check(0 <= event['firstObservedSeconds'] <= event['lastObservedSeconds'] < 695, 'Event time range: ' + event['id'])
        check(event['authorEventAgeMa'] is None, 'Cursor sample misrepresented as event date: ' + event['id'])
        check(event['implementationPart'] in [3, 4, 5], 'Implementation routing')
    check(len(video['additionalCaptionCues']) == 13, 'Caption cue coverage')
    check_refs(video)

    indicators = read('indicadores-video.json')
    with (AUDIT / indicators['sampleFile']).open(encoding='utf-8', newline='') as file:
        rows = list(csv.DictReader(file))
    check(len(rows) == indicators['sampleCount'] == 754, 'Indicator sample count')
    check(len({row['sample_index'] for row in rows}) == len(rows), 'Duplicate numerical sample')
    check(all(16 <= float(row['video_seconds']) <= 682 for row in rows), 'Indicator time range')
    check(all(0 <= float(row['age_ma_parsed']) <= 4540 for row in rows), 'Indicator age range')
    early = [row for row in rows if float(row['video_seconds']) < 19]
    check(early and all(row['atmosphere_layout'] == 'rock-vapor' and row['nitrogen_parsed'] == '' for row in early), 'Rock vapor incorrectly assigned to nitrogen')

    coverage = read('cobertura-video.json')
    hashes = coverage['frameHashes']
    check(coverage['extractedFrames'] == coverage['hudRecognizedFrames'] == len(hashes) == 950, 'Frame coverage drift')
    check([frame['index'] for frame in hashes] == list(range(950)), 'Frame index coverage')
    check(all(re.fullmatch(r'[0-9a-f]{64}', frame['sha256']) for frame in hashes), 'Invalid frame hash')
    check(all(a['seconds'] < b['seconds'] for a, b in zip(hashes, hashes[1:])), 'Unordered sample times')
    bibliography = read('bibliografia-video.json')
    check(bibliography['referenceCount'] == len(bibliography['entries']) == 29, 'Bibliography coverage')
    print('OK: 2 originals + ICS hashes; 38 hominin and 11 ice entries; 198 event candidates; 754 indicator samples; 950 frames; 29 credit references. Research only.')


if __name__ == '__main__':
    main()
