"""Focal party and de facto leadership curation for the 1970–1989 review.

Party leadership is distinct from head of state and head of government. Human
identities and dated P39 claims are checked against the cached Wikidata entities;
primary institutional biographies fill offices missing from P39. No portraits
are downloaded. --apply must be coordinated with other identities.json writers.
"""
import argparse
import copy
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('historical', ROOT / 'scripts/enrich-historical-authorities.py')
h = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(h)
TAG = 'manual-party-leaders-0.8'
TERMS = []

NEB_KADAR = 'https://neb.hu/asset/phph9pkfx.pdf'
NEB_NYERS = 'https://neb.hu/asset/phpxRHHpu.pdf'
NEB_PARTY = 'https://neb.hu/ismeretterjesztes/articles/show/mszmp-magyar-szocialista-munkaspart'
ALBANIA = 'https://tile.loc.gov/storage-services/master/frd/frdcstdy/al/albaniacountryst00zick/albaniacountryst00zick.pdf'
CZECH_ARCHIVE = 'https://www.soapraha.cz/files/publikace/8626.pdf'
PARTY_VIETNAM = 'https://tulieuvankien.dangcongsan.vn/lanh-dao-dang-nha-nuoc/tong-bi-thu'


def term(key, person, name, role, start, end, source, office=None, precision=11, note='', **extra):
    leader = dict(person=person, name=name, role=role, start=start, end=end,
                  source=source, precision=precision, curated=True, acquisition=TAG)
    if office:
        leader['office'] = office
    if note:
        leader['note'] = note
    leader.update(extra)
    TERMS.append((key, leader))


# Kádár, Grósz and Nyers have Politburo P39 claims, not dated claims for
# the principal party office. Those Politburo dates are deliberately not used.
term('HUN', 'Q200850', 'János Kádár', 'Primer secretario del Partido Socialista Obrero Húngaro',
     '1957-06-29', '1985-03-28', NEB_KADAR,
     note='Fechas de la ficha del Comité de Memoria Nacional húngaro. El cargo cambia de denominación en marzo de 1985; la pertenencia al Politburó no se utiliza como mandato de dirección.')
term('HUN', 'Q200850', 'János Kádár', 'Secretario general del Partido Socialista Obrero Húngaro',
     '1985-03-28', '1988-05-22', NEB_KADAR,
     note='Después del 22 de mayo de 1988 conservó una presidencia honorífica hasta mayo de 1989, sin mantener la secretaría general. No se prolonga su dirección efectiva por ese título honorífico.')
term('HUN', 'Q1028400', 'Károly Grósz', 'Secretario general del Partido Socialista Obrero Húngaro',
     '1988-05-22', '1989-10-07', NEB_PARTY,
     note='La elección de mayo de 1988 también está documentada por el Archivo Nacional húngaro. Desde junio de 1989 coexistió con la presidencia del partido de Nyers; no son dos nombramientos al mismo cargo.',
     corroboratingSources=['https://www.oktatolapok.mnl.gov.hu/grosz-karoly-1988-szeptemberi-targyalasa-erich-honeckerrel'])
term('HUN', 'Q281741', 'Rezső Nyers', 'Presidente del Partido Socialista Obrero Húngaro',
     '1989-06-24', '1989-10-07', NEB_NYERS,
     note='Cargo distinto de la secretaría general de Grósz durante la dirección colegiada final. La presidencia posterior del Partido Socialista Húngaro pertenece al sistema pluralista y no se presenta como liderazgo estatal exclusivo.')

# Albania: use a flagged coverage start instead of assigning the later title
# "First Secretary of the Party of Labour" retrospectively to November 1941.
term('ALB', 'Q53783', 'Enver Hoxha', 'Primer secretario del Partido del Trabajo de Albania',
     '1970-01-01', '1985-04-11', 'https://digitallibrary.un.org/record/79256/files/A_39_PV.107-EN.pdf',
     office='Q60286737', precision=9, startIsCoverageBoundary=True,
     note='Liderazgo anterior a 1970: el inicio es el límite de esta revisión, no su nombramiento. El homenaje de la Asamblea General de la ONU identifica su cargo partidario y fallecimiento en abril de 1985; P39 acredita el final el 11 de abril. No se le asigna la presidencia formal del Estado.')
term('ALB', 'Q156833', 'Ramiz Alia', 'Primer secretario del Partido del Trabajo de Albania',
     '1985-04-13', '1991-05-04', 'https://www.wikidata.org/wiki/Q156833', office='Q64139028',
     note='Mandato partidario fechado en P39, separado de sus cargos estatales. La elección del 13 de abril de 1985 consta en el comunicado del XI Pleno del Comité Central; la síntesis histórica de la Biblioteca del Congreso documenta la sucesión.',
     corroboratingSources=[ALBANIA, 'https://bannedthought.net/Albania/ForeignSupport/Canada/Marxist-Leninist-Canada-V15N32-1985.pdf'])

POL_ROLE = 'Primer secretario del Partido Obrero Unificado Polaco'
term('POL', 'Q159603', 'Władysław Gomułka', POL_ROLE, '1956-10-21', '1970-12-20',
     'https://edukacja.ipn.gov.pl/download/84/416568/PRL.pdf', office='Q11710857',
     note='Cronología del Instituto de la Memoria Nacional polaco. Su P39 no contiene un mandato partidario fechado utilizable; no se deduce de cargos parlamentarios.')
term('POL', 'Q312185', 'Edward Gierek', POL_ROLE, '1970-12-20', '1980-09-06',
     'https://ipn.gov.pl/download.php?id=48577&s=1', office='Q11710857',
     note='Inicio documentado por el IPN y límites diarios de P39 del cargo de primer secretario.')
term('POL', 'Q318370', 'Stanisław Kania', POL_ROLE, '1980-09-06', '1981-10-18',
     'https://archiwum.ipn.gov.pl/download/1/18823/1-18693.pdf', office='Q11710857',
     note='Fechas de la cronología del IPN, coincidentes con el mandato partidario P39.')
term('POL', 'Q55834', 'Wojciech Jaruzelski', POL_ROLE, '1981-10-18', '1989-07-29',
     'https://ipn.gov.pl/download/1/1231946/RozliczeniazekipaGierka.pdf', office='Q11710857',
     note='Elección del 18 de octubre de 1981 acreditada por el IPN; cese de P39 partidario. La jefatura del partido, la presidencia del Gobierno y sus posteriores cargos estatales son funciones distintas.')
term('POL', 'Q559771', 'Mieczysław Rakowski', POL_ROLE, '1989-07-29', '1990-01-29',
     'https://archiwum.ipn.gov.pl/download/1/18144/1-8534.pdf', office='Q11710857',
     note='P39 fecha el mandato diario; el IPN documenta la última secretaría de 1989–1990 y la disolución del partido durante la noche del 28 al 29 de enero de 1990.',
     corroboratingSources=['https://archiwum.ipn.gov.pl/download/1/938157/BIULETYN1-22021dointernetu.pdf'])

term('CSK', 'Q157651', 'Gustáv Husák', 'Primer secretario / secretario general del Partido Comunista de Checoslovaquia',
     '1969-04-17', '1987-12-17', CZECH_ARCHIVE, office='Q12018139',
     note='Mandato partidario P39 contrastado con el archivo estatal checo. El título cambia de primer secretario a secretario general en 1971; la presidencia de la República desde 1975 es otro cargo.',
     corroboratingSources=['https://www.ustrcr.cz/wp-content/uploads/2017/10/Demonstrace-v-Ceskoslovensku.pdf'])
term('CSK', 'Q551665', 'Miloš Jakeš', 'Secretario general del Partido Comunista de Checoslovaquia',
     '1987-12-17', '1989-11-24', CZECH_ARCHIVE, office='Q12018139')
term('CSK', 'Q939404', 'Karel Urbánek', 'Secretario general del Partido Comunista de Checoslovaquia',
     '1989-11-24', '1989-12-20', CZECH_ARCHIVE, office='Q12018139')

# Deng's undated "paramount leader" P39 cannot establish a formal appointment.
# Annual historiographical dating and a marked review boundary stay explicit.
term('CHN', 'Q16977', 'Deng Xiaoping', 'Dirigente de facto · liderazgo predominante',
     '1978-01-01', '1989-12-31',
     'https://www.govinfo.gov/content/pkg/GOVPUB-D5-PURL-gpo58263/pdf/GOVPUB-D5-PURL-gpo58263.pdf',
     office='Q50684', precision=9, endIsCoverageBoundary=True,
     note='La síntesis de la Universidad de Defensa Nacional estadounidense sitúa su liderazgo predominante en 1978–1992. El inicio expresa precisión anual, no una investidura el 1 de enero. El final es el límite de la revisión de 1970–1989, no su retirada. La afirmación P39 de dirigente predominante no tiene fechas; no se usa para atribuirle la presidencia del Estado.')
term('CHN', 'Q16977', 'Deng Xiaoping', 'Presidente de la Comisión Militar Central del Partido Comunista de China',
     '1981-06-28', '1989-11-09', 'https://cpc.people.com.cn/GB/64162/139962/8437272.html',
     office='Q20792297', precision=10,
     note='Cargo formal distinto de su liderazgo de facto y de la comisión militar estatal. Fechas diarias de P39; la relación institucional oficial confirma el inicio en junio de 1981.')
term('CHN', 'Q41570', 'Hua Guofeng', 'Presidente del Partido Comunista de China',
     '1976-10-07', '1981-06-28', 'https://cpc.people.com.cn/daohang/n/2013/0226/c357263-20607201.html',
     office='Q2708520', precision=10,
     note='Biografía institucional de Xinhua: presidencia del partido desde octubre de 1976 y sustitución en junio de 1981. Los extremos diarios proceden de P39; la precisión visible es mensual por la diferencia entre elección plenaria y anuncio.')
term('CHN', 'Q99850', 'Hu Yaobang', 'Presidente del Partido Comunista de China',
     '1981-06-28', '1982-09-11', 'https://fuwu.12371.cn/2012/06/12/ARTI1339491581487568.shtml',
     office='Q2708520', precision=10,
     note='La biografía oficial acredita junio de 1981–septiembre de 1982. Extremos diarios de P39, con precisión mensual; es un cargo distinto de la secretaría general posterior.')
term('CHN', 'Q99850', 'Hu Yaobang', 'Secretario general del Partido Comunista de China',
     '1982-09-12', '1987-01-15', 'https://fuwu.12371.cn/2012/06/12/ARTI1339491581487568.shtml',
     office='Q849418', precision=10,
     note='La biografía oficial confirma septiembre de 1982–enero de 1987; los límites diarios se conservan del mandato P39. No se confunde la secretaría del Secretariado de 1980 con esta secretaría general principal.')
term('CHN', 'Q99829', 'Zhao Ziyang', 'Secretario general interino del Partido Comunista de China',
     '1987-01-16', '1987-11-01', 'https://www.cppcc.gov.cn/2011/09/28/ARTI1317197350703283.shtml',
     office='Q849418', precision=10,
     note='La biografía de la Conferencia Consultiva distingue la interinidad desde enero de 1987 de la elección formal en noviembre. Se divide el P39 general para evitar dos mandatos superpuestos del mismo cargo.')
term('CHN', 'Q99829', 'Zhao Ziyang', 'Secretario general del Partido Comunista de China',
     '1987-11-01', '1989-06-24', 'https://www.cppcc.gov.cn/2011/09/28/ARTI1317197350703283.shtml',
     office='Q849418', precision=10,
     note='Elección formal en noviembre de 1987 y destitución en junio de 1989 acreditadas por la biografía institucional. P39 contiene finales el 23 y el 24 de junio; se conserva el 24, fecha del relevo por Jiang Zemin, con precisión mensual. El mandato existente de Jiang no se modifica.')

term('VDR', 'Q466001', 'Lê Duẩn', 'Primer secretario del Partido de los Trabajadores de Vietnam',
     '1960-09-10', '1976-07-02', PARTY_VIETNAM, office='Q848786',
     note='Tramo de Vietnam del Norte del mandato P39 de 1960–1986. La unificación divide la entidad territorial; no fue una dimisión personal ni una nueva elección de Lê Duẩn.')
term('VNM', 'Q466001', 'Lê Duẩn', 'Primer secretario / secretario general del Partido Comunista de Vietnam',
     '1976-07-02', '1986-07-10', 'https://baochinhphu.vn/tong-bi-thu-le-duan-tu-1976-den-1986-10256731.htm',
     office='Q848786',
     note='Continúa al frente del partido después de la unificación; la denominación y el título cambian en el IV Congreso de diciembre de 1976. La biografía gubernamental confirma el fallecimiento el 10 de julio de 1986. El inicio de este tramo es la unificación, no un nombramiento personal.')
term('VNM', 'Q545539', 'Trường Chinh', 'Secretario general del Partido Comunista de Vietnam',
     '1986-07-14', '1986-12-18',
     'https://baochinhphu.vn/tong-bi-thu-truong-chinh-nha-ly-luan-xuat-sac-nha-lanh-dao-kiet-xuat-mot-nhan-cach-lon-cua-cach-mang-viet-nam-102216361.htm',
     office='Q848786', note='El Gobierno vietnamita fecha su elección el 14 de julio de 1986 tras la muerte de Lê Duẩn. El mandato partidario es distinto de la presidencia del Consejo de Estado que ya ejercía.')
term('VNM', 'Q739795', 'Nguyễn Văn Linh', 'Secretario general del Partido Comunista de Vietnam',
     '1986-12-18', '1991-06-28', 'https://vietnamnet.vn/en/the-general-secretaries-of-the-communist-party-of-vietnam-E150327.html',
     office='Q848786', note='La serie institucional vietnamita proporciona el 18 de diciembre de 1986–28 de junio de 1991; la biografía gubernamental confirma diciembre de 1986–junio de 1991. Su P39 solo contiene pertenencia al Politburó sin fechas: no se convierte esa afirmación en mandato de secretario general.',
     corroboratingSources=['https://baochinhphu.vn/tong-bi-thu-nguyen-van-linh-tu-thang-12-1986-den-thang-6-1991-10256774.htm'])


def apply():
    path = ROOT / 'public/data/identities.json'
    data = json.loads(path.read_text(encoding='utf8'))
    countries = data['countries']
    for key, leader in TERMS:
        if key not in countries:
            raise ValueError('Missing historical identity: ' + key)
        if not leader['start'] < leader['end']:
            raise ValueError('Invalid term: ' + leader['name'])
    people = {q: e for q, e in h.parallel(h.entity, sorted({l['person'] for _, l in TERMS})) if e}
    for q in {l['person'] for _, l in TERMS}:
        if not any(isinstance(v, dict) and v.get('id') == 'Q5' for v in h.values(people.get(q, {}), 'P31')):
            raise ValueError('Authority is not a verified human entity: ' + q)
    portraits = {l['person']: l['portrait'] for c in countries.values() for l in c['leaders'] if l.get('portrait')}
    # Remove only this acquisition's earlier run. Existing state, government,
    # military and other curated party records remain untouched.
    for key in {key for key, _ in TERMS}:
        countries[key]['leaders'] = [l for l in countries[key]['leaders'] if l.get('acquisition') != TAG]
    for key, original in TERMS:
        leader = copy.deepcopy(original)
        if leader['person'] in portraits:
            leader['portrait'] = portraits[leader['person']]
        countries[key]['leaders'].append(leader)
    for key in {key for key, _ in TERMS}:
        countries[key]['leaders'].sort(key=lambda l: (l['start'], l['name'], l['role']))
    # Contemporary symbols retain their own 22 October reference date.
    data['historicalRetrieved'] = h.TODAY
    h.save(path, data)
    print(json.dumps(dict(terms=len(TERMS), people=len(people), countries=sorted({key for key, _ in TERMS}),
                          portraitsReused=sum(l['person'] in portraits for _, l in TERMS),
                          retrieved=data['retrieved'], historicalRetrieved=data['historicalRetrieved']), ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.apply:
        apply()
    else:
        print(json.dumps(dict(terms=len(TERMS), people=len({l['person'] for _, l in TERMS}),
                              countries=sorted({key for key, _ in TERMS})), ensure_ascii=False))
