"""Focal Estonia, Ireland and Mongolia supplements for0.11.

Independent incremental curator, after the generic1920 acquisition and focal
curate-1920-authorities.py. No network access, media acquisition or manifest edit.
Mongolian annual windows are documentary coverage, never fabricated January1
appointments. See docs/AUTHORITIES-1920-RESEARCH.md, follow-up section.
"""
import argparse
import copy
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'curated-1920-europe-asia-0.11'
EST_SOURCE = 'https://president.ee/eesti-riigipeade-loetelu'
IRL_SOURCE = 'https://www.gov.ie/en/department-of-the-taoiseach/publications/'


def previous(day):
    return (datetime.date.fromisoformat(day) - datetime.timedelta(days=1)).isoformat()


def following(day):
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat()


def curate(data):
    cs = data['countries']
    # Capture first: a person may have a portrait only on this script's records.
    portraits = {l['person']: copy.deepcopy(l['portrait'])
                 for country in cs.values() for l in country['leaders'] if l.get('portrait')}
    for country in cs.values():
        country['leaders'] = [l for l in country['leaders'] if l.get('acquisition') != TAG]

    def add(key, q, name, role, start, end, source, note='', precision=11,
            start_coverage=False, end_coverage=False):
        # Replace only this reviewed person's overlapping window. Keep other
        # people, genuinely separate terms and every record after1949 intact.
        kept = []
        for old in cs[key]['leaders']:
            if old['person'] != q or old['start'] > end or old['end'] < start:
                kept.append(old)
                continue
            if old['start'] < start:
                tail = copy.deepcopy(old)
                tail.update(end=previous(start), endIsCoverageBoundary=True)
                kept.append(tail)
            if old['end'] > end:
                tail = copy.deepcopy(old)
                tail.update(start=following(end), startIsCoverageBoundary=True)
                kept.append(tail)
        record = dict(person=q, name=name, role=role, start=start, end=end,
                      source=source, note=note, precision=precision,
                      acquisition=TAG, curated=True)
        if start_coverage:
            record['startIsCoverageBoundary'] = True
        if end_coverage:
            record['endIsCoverageBoundary'] = True
        if q in portraits:
            record['portrait'] = copy.deepcopy(portraits[q])
        cs[key]['leaders'] = kept + [record]

    # Full daily list in the presidential source, below its annual summary.
    # Source handover dates are converted to inclusive last days of the former
    # term. Päts's constitutional offices change in1934 and1937, not in1938 only.
    elders = [
        ('Q887682', 'Ants Piip', '1920-12-20', '1921-01-25'),
        ('Q299114', 'Konstantin Päts', '1921-01-25', '1922-11-21'),
        ('Q887260', 'Juhan Kukk', '1922-11-21', '1923-08-02'),
        ('Q299114', 'Konstantin Päts', '1923-08-02', '1924-03-26'),
        ('Q571670', 'Friedrich Karl Akel', '1924-03-26', '1924-12-16'),
        ('Q887247', 'Jüri Jaakson', '1924-12-16', '1925-12-15'),
        ('Q887238', 'Jaan Teemant', '1925-12-15', '1927-12-09'),
        ('Q710956', 'Jaan Tõnisson', '1927-12-09', '1928-12-04'),
        ('Q725322', 'August Rei', '1928-12-04', '1929-07-09'),
        ('Q887019', 'Otto Strandman', '1929-07-09', '1931-02-12'),
        ('Q299114', 'Konstantin Päts', '1931-02-12', '1932-02-19'),
        ('Q887238', 'Jaan Teemant', '1932-02-19', '1932-07-19'),
        ('Q126704', 'Kaarel Eenpalu', '1932-07-19', '1932-11-01'),
        ('Q299114', 'Konstantin Päts', '1932-11-01', '1933-05-18'),
        ('Q710956', 'Jaan Tõnisson', '1933-05-18', '1933-10-21'),
        ('Q299114', 'Konstantin Päts', '1933-10-21', '1934-01-24'),
    ]
    for q, name, start, handover in elders:
        add('EST', q, name, 'Riigivanem · jefatura del Estado y del Gobierno',
            start, previous(handover), EST_SOURCE,
            'Cargo constitucional estonio de1920, distinto de la presidencia de la República de1938. Último día inclusivo anterior al relevo fechado por la Presidencia.')
    add('EST', 'Q299114', 'Konstantin Päts', 'Primer ministro en funciones de riigivanem',
        '1934-01-24', '1937-09-02', EST_SOURCE,
        'Funciones bajo la reforma constitucional de1934; estado de excepción desde12/3/1934. No se retrotrae a este periodo el título de presidente de1938.')
    add('EST', 'Q299114', 'Konstantin Päts', 'Riigihoidja · regente del Estado',
        '1937-09-03', '1938-04-23', EST_SOURCE,
        'Título transitorio desde3/9/1937; presidente de la República desde24/4/1938, cuyo mandato adquirido se conserva aparte.')

    # Ireland: the1937 title Taoiseach must not be projected onto the Free
    # State or the revolutionary Dáil. The1922 dual system is explicit.
    add('IRL', 'Q173347', 'Éamon de Valera', 'Presidente de Dáil Éireann · autoridad republicana',
        '1921-01-01', '1921-08-25', 'https://www.nationalarchives.ie/wp-content/uploads/2021/09/2021-Commemoration-Programme-as-part-of-the-Decade-of-Centenaries-2012-2023-EN-REDUX.pdf',
        'Elegido presidente de Dáil Éireann el1/4/1919. El inicio1921 limita esta revisión, no es un nombramiento ni una soberanía aceptada por el Reino Unido.', start_coverage=True)
    add('IRL', 'Q173347', 'Éamon de Valera', 'Presidente de la República irlandesa · autoridad revolucionaria',
        '1921-08-26', '1922-01-09', IRL_SOURCE + 'second-d%C3%A1il/',
        'Título del ministerio del Segundo Dáil anterior al Tratado; dimite9/1/1922. No es la presidencia constitucional creada en1937.')
    add('IRL', 'Q342765', 'Arthur Griffith', 'Presidente de Dáil Éireann',
        '1922-01-10', '1922-08-12', IRL_SOURCE + 'second-d%C3%A1il/',
        'Jefatura del ejecutivo del Dáil, simultánea al Gobierno Provisional de Collins; fallece12/8/1922.')
    add('IRL', 'Q173196', 'Michael Collins', 'Presidente del Gobierno Provisional',
        '1922-01-16', '1922-08-22', IRL_SOURCE + 'second-d%C3%A1il/',
        'Gobierno constituido14/1, toma de posesión y elección de presidente16/1; transferencia de funciones1/4. No confundir esos tres hitos ni la presidencia de Griffith. Muere22/8/1922.')
    add('IRL', 'Q465770', 'W. T. Cosgrave', 'Presidente del Gobierno Provisional y de Dáil Éireann',
        '1922-09-09', '1922-12-05', IRL_SOURCE + 'second-d%C3%A1il/',
        'Fusión del sistema dual con el Tercer Dáil9/9; el Consejo Ejecutivo del Estado Libre comienza6/12. El interinato de agosto1922 sigue pendiente.')
    add('IRL', 'Q465770', 'W. T. Cosgrave', 'Presidente del Consejo Ejecutivo del Estado Libre Irlandés',
        '1922-12-06', '1932-03-08', IRL_SOURCE + 'sixth-d%C3%A1il/',
        'Continuidad de la jefatura de Gobierno a través de sucesivos consejos. Inicio del Estado Libre documentado en la historia del Segundo Dáil; el Quinto Consejo concluye al relevo9/3/1932. No se titula Taoiseach.')
    add('IRL', 'Q173347', 'Éamon de Valera', 'Presidente del Consejo Ejecutivo del Estado Libre Irlandés',
        '1932-03-09', '1937-12-28', IRL_SOURCE + 'ninth-d%C3%A1il/',
        'El Sexto Consejo comienza9/3/1932; las fuentes del Séptimo y Octavo conservan la continuidad. La Constitución cambia el título a Taoiseach el29/12/1937 sin sustitución personal; el mandato posterior adquirido permanece.')

    # Mongolia: only bounded documentary windows supported by institutional
    # annual biographies. January1 is a coverage marker, not appointment day.
    annual_note = ('Ventana documental de cobertura con precisión anual. Los extremos no son fechas de nombramiento o cese; los relevos diarios siguen pendientes. ')
    mongolia = [
        ('Q353547', 'Bogd Khan', 'Kan de Mongolia · monarca bajo gobierno limitado',
         '1923-01-01', '1923-12-31', 'https://nli.gov.mn/wp-content/uploads/2023/09/SE.2021.7.pdf',
         'El Instituto Jurídico Nacional distingue el sistema dual limitado desde1921 y el fallecimiento del monarca en1924. Sólo se documenta aquí1923, sin adjudicarle gobierno republicano.'),
        ('Q2672415', 'Balingiin Tserendorj', 'Primer ministro de Mongolia',
         '1924-01-01', '1927-12-31', 'https://www.mongoltoli.mn/history/h/693',
         'La biografía histórica acredita1923–1928. Se limita a los años interiores1924–1927; ni los cambios constitucionales de1924 ni la muerte de1928 se fechan por el cierre de esta ventana.'),
        ('Q45281', 'Anandyn Amar · Agdanbuugyn Amar', 'Primer ministro de Mongolia',
         '1928-12-31', '1929-12-31', 'https://www.mongoltoli.mn/history/h/713',
         'La biografía acredita1928–1930. Se documenta el cierre de1928 y1929, sin inventar una investidura el1/1/1928 ni el día del relevo de1930.'),
        ('Q2353321', 'Tsengeltiin Jigjidjav', 'Primer ministro de Mongolia',
         '1930-12-31', '1931-12-31', 'https://catalog.num.edu.mn/cgi-bin/koha/opac-detail.pl?biblionumber=23185',
         'El catálogo de la Universidad Nacional identifica su ejercicio1930–1932. Se documentan los cierres1930–1931; no se extiende hasta final1932 sobre el mandato adquirido de Genden.'),
        ('Q45281', 'Anandyn Amar · Agdanbuugyn Amar', 'Primer ministro de Mongolia',
         '1937-01-01', '1938-12-31', 'https://www.mongoltoli.mn/history/h/713',
         'Segundo mandato acreditado1936–1939. Se conserva una ventana interior1937–1938, sin deducir el día de su detención o relevo en1939.'),
    ]
    for q, name, role, start, end, source, note in mongolia:
        add('MNG', q, name, role, start, end, source, annual_note + note,
            precision=9, start_coverage=True, end_coverage=True)

    for country in cs.values():
        country['leaders'].sort(key=lambda l: (l['start'], l['name'], l['role']))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, default=ROOT / 'public/data/identities.json')
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    result = curate(json.loads(args.input.read_text(encoding='utf8')))
    output = args.output or args.input
    output.write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf8', newline='\n')
    print('Prepared', sum(l.get('acquisition') == TAG for c in result['countries'].values() for l in c['leaders']), 'Estonia/Ireland/Mongolia records.')
