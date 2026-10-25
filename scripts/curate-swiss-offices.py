"""Correct Swiss office labels using explicit office identifiers, not dates.

Pure/idempotent curate(data). No network or media operations. The three office
identities were checked against Wikidata and the Swiss Federal Council's own
description of collegiality and the annual presidency. Existing statements,
mandate dates, source precision and credited portraits remain unchanged.
"""
import argparse
import copy
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'swiss-office-labels-0.12.1'
SOURCE = 'https://www.admin.ch/en/federal-presidency-role'
HISTORY = 'https://www.admin.ch/en/history-of-the-federal-council'
OFFICES = {
    'Q11811941': ('Miembro del Consejo Federal · órgano colegiado', 'council-member'),
    'Q688230': ('Presidente de la Confederación · presidencia anual', 'annual-presidency'),
}


def curate(incoming):
    """Only CHE labels/provenance change; no calendar-duration heuristics."""
    data = copy.deepcopy(incoming)
    country = data.get('countries', {}).get('CHE')
    if not country:
        return data
    for leader in country['leaders']:
        office = OFFICES.get(leader.get('office'))
        if office:
            role, authority_class = office
        elif leader['person'] == 'Q30917':
            role = 'Consejo Federal · jefatura colegiada del Estado y del Gobierno'
            authority_class = 'collective'
        else:
            # The existing, specifically curated2026 presidency has no office
            # identifier and already uses a correct precise label. Preserve it.
            continue
        leader.setdefault('sourceRole', leader['role'])
        leader.update(role=role, authorityClass=authority_class,
                      roleSource=SOURCE, roleHistorySource=HISTORY,
                      roleCuration=TAG)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, default=ROOT / 'public/data/identities.json')
    parser.add_argument('--output', type=pathlib.Path, required=True,
                        help='Explicit output path. Research never writes public data implicitly.')
    args = parser.parse_args()
    data = curate(json.loads(args.input.read_text(encoding='utf8')))
    args.output.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n',
                           encoding='utf8', newline='\n')
    print('Corrected Swiss labels:', sum(l.get('roleCuration') == TAG for l in data['countries']['CHE']['leaders']))
