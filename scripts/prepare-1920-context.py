"""Incremental, offline 1920–1949 institutional/context curation.

Run after prepare-1950-context.py when rebuilding. Only this prefix is replaced;
later coverage and contemporary reference dates are preserved. Ends are exclusive.
Sources were checked 2026-10-24; no conflict record creates a geographic front.
"""
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1] / 'public/data'
PREFIX = 'extension-1920-'


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf8'))


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')


d = read('affiliations.json')
orgs = {o['id']: o for o in d['organizations']}


def organization(oid, label, formed, source, description, dissolved=None):
    o = dict(id=oid, label=label, type='political', formed=formed, source=source, description=description, memberships=[])
    if dissolved:
        o['dissolved'] = dissolved
    orgs[oid] = o
    return o


def member(oid, code, start, end=None, note='', source=None, category='member'):
    m = dict(code=code, category=category, start=start, source=source or orgs[oid]['source'])
    if end:
        m['end'] = end
    if note:
        m['note'] = note
    orgs[oid]['memberships'].append(m)
    return m


LON = 'https://treaties.un.org/Pages/Content.aspx?path=DB/LoNOnline/pageIntro_en.xml'
organization('leagueOfNations', 'Sociedad de Naciones', '1920-01-10', LON,
             'Membresía jurídica de la Sociedad de Naciones; no implica control efectivo ni reconocimiento de anexiones. Las retiradas notificadas en1933 por Alemania y Japón se hacen efectivas en1935. Estados Unidos nunca fue miembro. El cierre institucional es18/4/1946, distinto de la fundación de la ONU.', '1946-04-18')
# Surviving roster transcribed from the UN Treaty Collection. Ireland and Egypt
# contain errors in that web table; contemporary national delegation records win.
league_rows = '''
AFG 1934-09-17
ALB 1920-12-17
ARG 1920-01-10
AUS 1920-01-10
BEL 1920-01-10
BOL 1920-01-10
BGR 1920-12-16
CAN 1920-01-10
CHN 1920-07-16
COL 1920-02-16
CUB 1920-03-08
CSK 1920-01-10
DNK 1920-03-08
DOM 1924-09-29
ECU 1934-09-28
EGY 1937-05-26
EST 1921-09-22
ETH 1923-09-28
FIN 1920-12-16
FRA 1920-01-10
GRC 1920-03-30
IND 1920-01-10
IRN 1920-01-10
IRQ 1932-10-03
IRL 1923-09-10
LVA 1921-09-22
LBR 1920-06-30
LTU 1921-09-22
LUX 1920-12-16
MEX 1931-09-12
NLD 1920-03-09
NZL 1920-01-10
NOR 1920-03-09
PAN 1920-11-25
POL 1920-01-10
PRT 1920-04-08
THA 1920-01-10
SWE 1920-03-09
CHE 1920-03-08
TUR 1932-07-18
ZAF 1920-01-10
GBR 1920-01-10
URY 1920-01-10
YUG 1920-02-10
'''
for row in league_rows.splitlines():
    if not row.strip():
        continue
    code, start = row.split()
    source = None
    note = 'La continuidad en el registro jurídico no acredita soberanía efectiva o ausencia de ocupación durante la guerra.'
    if code == 'CHN':
        note = 'China está representada por la República de China; no atribuir este ingreso a la República Popular proclamada en1949.'
    if code == 'IRL':
        source = 'https://www.difp.ie/volume-2/1923/outlines-events-at-the-1923-league-of-nations-assembly/470/'
        note = 'El informe de la delegación irlandesa fecha la admisión el10/9/1923; corrige el año1920 de la tabla web de UNTC.'
    if code == 'EGY':
        source = 'https://paperspast.natlib.govt.nz/parliamentary/AJHR1937-I.2.1.2.4'
        note = 'El informe parlamentario neozelandés de la sesión extraordinaria fecha la admisión el26/5/1937; corrige marzo en la tabla web de UNTC.'
    member('leagueOfNations', code, start, '1946-04-18', note, source)
# Focal terminated memberships. For remaining departed Latin-American members,
# entry is explicitly an annual observation, not an invented day of accession.
for code, start, end in [
    ('AUT','1920-12-16','1938-03-18'), ('BRA','1920-01-10','1928-06-13'),
    ('CHL','1920-01-10','1940-06-01'), ('CRI','1920-12-31','1927-01-01'),
    ('DEU','1926-09-08','1935-10-19'), ('GTM','1920-01-10','1938-05-25'),
    ('HTI','1920-12-31','1944-04-08'), ('HND','1920-01-10','1938-07-09'),
    ('HUN','1922-09-18','1941-04-10'), ('ITA','1920-01-10','1939-12-10'),
    ('JPN','1920-01-10','1935-03-27'), ('NIC','1920-01-10','1938-06-16'),
    ('PRY','1920-01-10','1937-02-23'), ('PER','1920-01-10','1941-04-08'),
    ('ROU','1920-01-10','1942-07-10'), ('SLV','1920-12-31','1939-08-09'),
    ('ESP','1920-01-10','1941-05-08'), ('SUN','1934-09-18','1939-12-14'),
    ('VEN','1920-12-31','1940-07-11')]:
    note = 'Fin efectivo de membresía según UNTC; no confundir con anuncio o notificación de retirada.'
    if start.endswith('12-31'):
        note += ' Inicio: observación al cierre de1920, pues la tabla de miembros retirados sólo da el año; pendiente cotejo del día de ingreso.'
    if code == 'SUN':
        note = 'URSS admitida el18/9/1934 y expulsada el14/12/1939 tras la invasión de Finlandia; no es una retirada voluntaria ni una membresía rusa retrospectiva.'
    member('leagueOfNations', code, start, end, note)

NATO = 'https://nato.int/en/about-us/official-texts-and-resources/official-texts/1949/04/04/the-north-atlantic-treaty'
orgs['nato']['formed'] = '1949-08-24'
for m in orgs['nato']['memberships']:
    if m['start'] in ('1949-04-04', '1949-08-24'):
        m.update(start='1949-08-24', source=NATO, note='Firma del Tratado de Washington:4/4/1949. Entrada en vigor para los doce fundadores:24/8/1949; se usa esta última para el intervalo jurídico.')

OAS = 'https://cidh.oas.org/Basicos/English/Basic22b.CharterOAS_ratif.htm'
orgs['oas']['description'] = 'Organización constituida por la firma de Bogotá el30/4/1948; Carta en vigor desde13/12/1951. Miembro fundador del sistema no equivale a fecha individual de ratificación de la Carta. Se conservan por separado las suspensiones de participación y las retiradas posteriores.'
for m in orgs['oas']['memberships']:
    if m['start'] in ('1950-01-01', '1948-04-30'):
        m.update(start='1948-04-30', source=OAS, note='Estado signatario fundador en Bogotá el30/4/1948. La Carta entra en vigor el13/12/1951; este registro de fundador no es una afirmación de ratificación individual en1948.')
        m.pop('startIsCoverageBoundary', None)

# Albania's admission was announced with its application/reply on25February.
CAME = 'https://history.state.gov/historicaldocuments/frus1949v05/d2'
for m in orgs['comecon']['memberships']:
    if m['code'] == 'ALB' and m['start'] in ('1950-01-01','1949-02-25'):
        m.update(start='1949-02-25', source=CAME, note='Anuncio de la solicitud y respuesta soviética favorable en el boletín albanés del25/2/1949, documentado por FRUS. Observación de admisión publicada; no se inventa fecha anterior del efecto jurídico.')
        m.pop('startIsCoverageBoundary', None)

ARAB = 'https://treaties.un.org/pages/showDetails.aspx?objid=080000028015a44b'
arab_effect = {'EGY':'1945-05-10','IRQ':'1945-05-10','LBN':'1945-06-01','JOR':'1945-05-10','SAU':'1945-05-10','SYR':'1945-06-04','YMK':'1946-02-24'}
for m in orgs['arabLeague']['memberships']:
    if m['code'] in arab_effect and m['start'] in ('1950-01-01', arab_effect[m['code']]):
        m.update(start=arab_effect[m['code']], source=ARAB, note='Pacto concluido el22/3/1945, en vigor general el10/5/1945. Inicio individual según efecto de la ratificación en el registro depositario; Yemen sur no es fundador.')
        m.pop('startIsCoverageBoundary', None)
# CAME started in1949: only the six founders are extended, not every later member.
for m in orgs['comecon']['memberships']:
    if m['code'] in ('SUN','BGR','CSK','HUN','POL','ROU') and m['start'] in ('1950-01-01','1949-01-25'):
        m.update(start='1949-01-25', source=CAME, note='Comunicado de creación publicado el25/1/1949 tras reuniones de enero. La fecha corresponde al anuncio institucional, no a una supuesta adhesión en1950.')
        m.pop('startIsCoverageBoundary', None)

# UN_ROWS is an offline transcription of dates in the UN Library membership
# guide, cross-checked against its separate founders table (which corrects
# typographical errors in several individual country boxes).
UN_SOURCE = 'https://research.un.org/en/unmembers/currentmembers'
UN_FOUNDERS = 'https://research.un.org/en/unmembers/founders'
UN_GROWTH = 'https://www.un.org/en/about-us/growth-in-un-membership'
UN_ROWS = '''
AFG 1946-11-09
AGO 1976-12-01
ALB 1955-12-14
AND 1993-07-28
ARE 1971-12-09
ARG 1945-10-24
ARM 1992-03-02
ATG 1981-11-11
AUS 1945-11-01
AUT 1955-12-14
AZE 1992-03-02
BDI 1962-09-18
BEL 1945-12-27
BEN 1960-09-20
BFA 1960-09-20
BGD 1974-09-17
BGR 1955-12-14
BHR 1971-09-21
BHS 1973-09-18
BIH 1992-05-22
BLR 1945-10-24
BLZ 1981-09-25
BOL 1945-11-14
BRA 1945-10-24
BRB 1966-12-09
BRN 1984-09-21
BTN 1971-09-21
BWA 1966-10-17
CAF 1960-09-20
CAN 1945-11-09
CHE 2002-09-10
CHL 1945-10-24
CHN 1945-10-24
CIV 1960-09-20
CMR 1960-09-20
COD 1960-09-20
COG 1960-09-20
COL 1945-11-05
COM 1975-11-12
CPV 1975-09-16
CRI 1945-11-02
CUB 1945-10-24
CYP 1960-09-20
CZE 1993-01-19
DEU 1973-09-18
DJI 1977-09-20
DMA 1978-12-18
DNK 1945-10-24
DOM 1945-10-24
DZA 1962-10-08
ECU 1945-12-21
EGY 1945-10-24
ERI 1993-05-28
ESP 1955-12-14
EST 1991-09-17
ETH 1945-11-13
FIN 1955-12-14
FJI 1970-10-13
FRA 1945-10-24
FSM 1991-09-17
GAB 1960-09-20
GBR 1945-10-24
GEO 1992-07-31
GHA 1957-03-08
GIN 1958-12-12
GMB 1965-09-21
GNB 1974-09-17
GNQ 1968-11-12
GRC 1945-10-25
GRD 1974-09-17
GTM 1945-11-21
GUY 1966-09-20
HND 1945-11-17
HRV 1992-05-22
HTI 1945-10-24
HUN 1955-12-14
IDN 1950-09-28
IND 1945-10-30
IRL 1955-12-14
IRN 1945-10-24
IRQ 1945-12-21
ISL 1946-11-09
ISR 1949-05-11
ITA 1955-12-14
JAM 1962-09-18
JOR 1955-12-14
JPN 1956-12-18
KAZ 1992-03-02
KEN 1963-12-16
KGZ 1992-03-02
KHM 1955-12-14
KIR 1999-09-14
KNA 1983-09-23
KOR 1991-09-17
KWT 1963-05-14
LAO 1955-12-14
LBN 1945-10-24
LBR 1945-11-02
LBY 1955-12-14
LCA 1979-09-18
LIE 1990-09-18
LKA 1955-12-14
LSO 1966-10-17
LTU 1991-09-17
LUX 1945-10-24
LVA 1991-09-17
MAR 1956-11-12
MCO 1993-05-28
MDA 1992-03-02
MDG 1960-09-20
MDV 1965-09-21
MEX 1945-11-07
MHL 1991-09-17
MKD 1993-04-08
MLI 1960-09-28
MLT 1964-12-01
MMR 1948-04-19
MNE 2006-06-28
MNG 1961-10-27
MOZ 1975-09-16
MRT 1961-10-27
MUS 1968-04-24
MWI 1964-12-01
MYS 1957-09-17
NAM 1990-04-23
NER 1960-09-20
NGA 1960-10-07
NIC 1945-10-24
NLD 1945-12-10
NOR 1945-11-27
NPL 1955-12-14
NRU 1999-09-14
NZL 1945-10-24
OMN 1971-10-07
PAK 1947-09-30
PAN 1945-11-13
PER 1945-10-31
PHL 1945-10-24
PLW 1994-12-15
PNG 1975-10-10
POL 1945-10-24
PRK 1991-09-17
PRT 1955-12-14
PRY 1945-10-24
QAT 1971-09-21
ROU 1955-12-14
RUS 1945-10-24
RWA 1962-09-18
SAU 1945-10-24
SDN 1956-11-12
SEN 1960-09-28
SGP 1965-09-21
SLB 1978-09-19
SLE 1961-09-27
SLV 1945-10-24
SMR 1992-03-02
SOM 1960-09-20
SRB 2000-11-01
SSD 2011-07-14
STP 1975-09-16
SUR 1975-12-04
SVK 1993-01-19
SVN 1992-05-22
SWE 1946-11-09
SWZ 1968-09-24
SYC 1976-09-21
SYR 1945-10-24
TCD 1960-09-20
TGO 1960-09-20
THA 1946-12-15
TJK 1992-03-02
TKM 1992-03-02
TLS 2002-09-27
TON 1999-09-14
TTO 1962-09-18
TUN 1956-11-12
TUR 1945-10-24
TUV 2000-09-05
TZA 1961-12-14
UGA 1962-10-25
UKR 1945-10-24
URY 1945-12-18
USA 1945-10-24
UZB 1992-03-02
VCT 1980-09-16
VEN 1945-11-15
VNM 1977-09-20
VUT 1981-09-15
WSM 1976-12-15
YEM 1947-09-30
ZAF 1945-11-07
ZMB 1964-12-01
ZWE 1980-08-25
'''
organization('un', 'Naciones Unidas · ONU', '1945-10-24', UN_SOURCE,
             'Miembros desde1945 con admisiones y continuidades documentadas. Incluye las repúblicas soviéticas de Ucrania y Bielorrusia como miembros originales; no las convierte en Estados independientes de la URSS. La representación de China cambia en1971 sin una nueva adhesión. No se incluyen observadores como miembros plenos.')
for line in UN_ROWS.splitlines():
    if not line.strip():
        continue
    code, date = line.split()
    member('un', code, date, source=UN_FOUNDERS if date < '1946-01-01' else None)


def replace_un(code, rows):
    orgs['un']['memberships'] = [m for m in orgs['un']['memberships'] if m['code'] != code]
    for new_code, start, end, note in rows:
        member('un', new_code, start, end, note, UN_GROWTH)


replace_un('CHN', [('CHN','1945-10-24','1949-10-01','China: representación de la República de China, miembro original. El corte1949 separa claves cartográficas; no cambia la membresía jurídica.'),('TWN','1949-10-01','1971-10-25','Clave de la República de China tras1949; conserva la representación de China hasta la resolución2758. No es una adhesión independiente de Taiwán.'),('CHN','1971-10-25',None,'Resolución2758: representantes de la República Popular reconocidos como los únicos representantes legítimos de China. Continuidad del miembro China, sin nueva adhesión.')])
replace_un('RUS', [('SUN','1945-10-24','1991-12-24','Miembro original: Unión Soviética, no Federación de Rusia.'),('RUS','1991-12-24',None,'Continuidad de la membresía de la URSS comunicada por la Federación de Rusia el24/12/1991; no nueva admisión.')])
replace_un('EGY', [('EGY','1945-10-24','1958-02-22','Miembro original; unión con Siria en1958.'),('UAR','1958-02-22','1961-09-28','Un solo miembro tras la unión de Egipto y Siria. El corte corresponde a la clave territorial; Egipto continúa con el nombre RAU hasta1971.'),('EGY','1961-09-28',None,'Continuidad del miembro egipcio/RAU después de la separación territorial; no nueva admisión.')])
replace_un('SYR', [('SYR','1945-10-24','1958-02-22','Miembro original; unido a Egipto en1958.'),('SYR','1961-10-13',None,'Siria reanuda su membresía separada el13/10/1961, después de recuperar su independencia en septiembre.')])
replace_un('MYS', [('MAL','1957-09-17','1963-09-16','Admisión de la Federación de Malaya.'),('MYS','1963-09-16',None,'Continuidad como Malasia tras la federación de1963; no nueva admisión.')])
replace_un('YEM', [('YMK','1947-09-30','1962-09-27','Admisión del Reino Mutawakkilita de Yemen; no del Estado meridional de1967.'),('YAR','1962-09-27','1990-05-22','Continuidad del miembro Yemen bajo autoridades republicanas; el corte corresponde a la clave institucional del atlas, no a una nueva admisión.'),('YEM','1990-05-22',None,'Unificación de los dos Yemen, ambos miembros antes de la unión.')])
member('un','YPR','1967-12-14','1990-05-22','Admisión del Yemen meridional; termina como miembro separado al unificarse.',UN_GROWTH)
replace_un('TZA', [('TAN','1961-12-14','1964-04-26','Admisión de Tanganyika.'),('TZA','1964-04-26',None,'Unión de Tanganyika y Zanzíbar: un solo miembro.')])
member('un','ZAN','1963-12-16','1964-04-26','Admisión de Zanzíbar antes de la unión.',UN_GROWTH)
replace_un('SRB', [('FRY','2000-11-01','2003-02-04','La República Federativa de Yugoslavia fue admitida en2000; no se le atribuye continuidad automática de la membresía yugoslava original.'),('SCG','2003-02-04','2006-06-05','Cambio a Serbia y Montenegro; continuidad del miembro admitido en2000.'),('SRB','2006-06-05',None,'Serbia continúa la membresía de Serbia y Montenegro tras la independencia montenegrina.')])
member('un','YUG','1945-10-24','2000-11-01','Yugoslavia original; desintegración y reclamación de continuidad controvertida desde1992. No afirma existencia territorial continua ni participación regular hasta2000; se conserva hasta su retirada del registro oficial.',UN_GROWTH)
member('un','CSK','1945-10-24','1993-01-01','Checoslovaquia original; las dos repúblicas fueron admitidas por separado el19/1/1993.',UN_GROWTH)
member('un','DDR','1973-09-18','1990-10-03','Admisión separada de la RDA; incorporación a la RFA el3/10/1990.',UN_GROWTH)
replace_un('IDN', [('IDN','1950-09-28','1965-01-20','Admisión de Indonesia.'),('IDN','1966-09-28',None,'Reanudación de participación tras la retirada temporal anunciada en1965; no nueva admisión.')])

for o in orgs.values():
    o['memberships'].sort(key=lambda m: (m['code'], m['start'], m['category']))
    for m in o['memberships']:
        datetime.date.fromisoformat(m['start'])
        if m.get('end'):
            datetime.date.fromisoformat(m['end'])
            assert m['end'] > m['start'], (o['id'], m)
d['organizations'] = sorted(orgs.values(), key=lambda o: o['id'])
d.update(coverageStart=1920, expandedReferenceDate='2026-10-24')

c = read('historical-context.json')
c['events'] = [e for e in c['events'] if not e['id'].startswith(PREFIX)]
h = read('country-history.json')
h['relations'] = [r for r in h['relations'] if not r['id'].startswith(PREFIX)]
h['records'] = [r for r in h['records'] if not r['id'].startswith(PREFIX)]


def event(ident, title, kind, start, end, keys, text, source, note=''):
    c['events'].append(dict(id=PREFIX+ident, title=title, type=kind, start=start, end=end, countries=keys.split(), text=text, source=source, sourceLabel='Archivo o institución responsable · investigación1920–1949', note=note or 'Intervalo contextual con fin exclusivo. Las claves vinculan fichas; no son una lista exhaustiva de beligerantes ni generan frentes.'))


def record(ident, keys, section, title, start, end, text, source):
    h['records'].append(dict(id=PREFIX+ident, keys=keys.split(), section=section, title=title, start=start, end=end, text=text, source=source, sourceLabel='Archivo o institución responsable · investigación1920–1949'))


def relation(ident, a, b, date, label, source, note):
    h['relations'].append(dict(id=PREFIX+ident, **{'from':dict(key=a[0],name=a[1],year=a[2]),'to':dict(key=b[0],name=b[1],year=b[2])},date=date,type='transition',label=label,note=note,source=source,sourceLabel='Documento de la transición'))

STATE = 'https://history.state.gov/'
WW2 = 'https://encyclopedia.ushmm.org/content/en/article/world-war-ii-key-dates'
SPAIN = 'https://www.cultura.gob.es/cultura/mc/incautaciones-guerra-civil/guerra-civil.html'
CHINA = STATE+'milestones/1945-1952/chinese-rev'
PAL = 'https://www.un.org/unispal/document/auto-insert-179951/'
JAPAN = STATE+'milestones/1945-1952/japan-reconstruction'
FRANCE = 'https://www.elysee.fr/la-presidence/la-constitution-du-27-octobre-1946'
ITALY = 'https://www.senato.it/CESUS/2026/2giugno/'
INDIA = 'https://www.legislation.gov.uk/ukpga/Geo6/10-11/30'
DEPRESSION = STATE+'milestones/1921-1936/great-depression'
BERLIN = STATE+'milestones/1945-1952/berlin-airlift'

events = [
('league','Comienza la Sociedad de Naciones','transition','1920-01-10','1921-01-01','GBR FRA ITA JPN CHN IND','El sistema de seguridad colectiva entra en actividad con el Tratado de Versalles. Estados Unidos no se incorpora. Mandatos y miembros son categorías distintas.','https://www.ungeneva.org/en/about/league-of-nations/background'),
('italy-fascism','Mussolini al frente del Gobierno italiano','transition','1922-10-31','1923-01-01','ITA','Mussolini forma Gobierno tras la marcha sobre Roma. La monarquía continúa: jefatura de Estado y presidencia del Gobierno son cargos diferentes.','https://www.senato.it/legislature/regno/italia/26/resoconti-elenco-cronologico'),
('depression','Crisis internacional de1929 y Gran Depresión','transition','1929-10-01','1940-01-01','USA DEU GBR FRA JPN','La crisis financiera y económica se transmite internacionalmente durante los años treinta, con respuestas nacionales distintas. Ventana contextual desde octubre; no una fecha única de comienzo o recuperación mundial. No se incorporan estadísticas retrospectivas sin serie acreditada.',DEPRESSION),
('spanish-republic','Segunda República y Constitución española','transition','1931-04-14','1932-01-01','ESP','La proclamación republicana del14/4 precede a la Constitución aprobada el9/12. No se atribuyen al Gobierno provisional todos los cargos constitucionales posteriores.','https://www.cultura.gob.es/gl/cultura/areas/archivos/mc/archivos/cdmh/exposiciones-y-actividades/echa-un-vistazo/constitucion-1931.html'),
('manchuria','Invasión japonesa de Manchuria','conflict','1931-09-18','1933-06-01','CHN JPN','El incidente de Mukden sirve de pretexto para la conquista japonesa; Manchukuo es una entidad dependiente del ejército japonés. La condena internacional y la retirada japonesa de la Sociedad no crean un frente cartográfico.',STATE+'milestones/1921-1936/mukden-incident'),
('iraq','Irak sale del marco del mandato','transition','1932-10-03','1933-01-01','IRQ GBR','La admisión de Irak en la Sociedad de Naciones acompaña el fin del mandato británico. Las obligaciones y relaciones posteriores con Reino Unido no equivalen a mantener sin cambios el mandato.','https://iraqiembassy.us/press-statement-16/'),
('germany-dictatorship','Destrucción de la democracia de Weimar','transition','1933-01-30','1934-01-01','DEU','Hindenburg nombra canciller a Hitler. El decreto de febrero y la ley de plenos poderes de marzo desmantelan las garantías y el papel parlamentario; un nombramiento formal no equivale a continuidad democrática.','https://www.bundestag.de/parlament/geschichte/100-jahre-weimar/machtuebergabe-972588'),
('ethiopia','Invasión italiana de Etiopía','conflict','1935-10-03','1937-01-01','ETH ITA','Italia invade Etiopía y la Sociedad de Naciones adopta sanciones. La posterior proclamación imperial italiana no certifica control uniforme ni aceptación internacional de la conquista. El corte1937 es cobertura de esta fase.','https://www.senato.it/legislature/regno/italia/29/resoconti-elenco-cronologico'),
('spain-1936','Guerra Civil española · sublevación y división','conflict','1936-07-17','1937-01-01','ESP','La sublevación contra la República desemboca en guerra y autoridades rivales. Esta fase termina por corte anual; el conflicto continúa. El inventario de control existente conserva su propia fecha e incertidumbre.',SPAIN),
('spain-1937','Guerra Civil española · fase de1937','conflict','1937-01-01','1938-01-01','ESP','Continúan la guerra y la división de autoridades. Ventana anual de contexto: el frente incorporado al atlas para1937 corresponde a octubre, con incertidumbre declarada, y no al31 de diciembre.',SPAIN),
('spain-1938','Guerra Civil española · fase de1938','conflict','1938-01-01','1939-01-01','ESP','La guerra continúa durante1938. Este corte editorial anual no documenta frentes diarios, Teruel, Ebro ni la ofensiva de Cataluña con geometrías nuevas.',SPAIN),
('spain-1939','Derrota republicana y dictadura franquista','transition','1939-01-01','1940-01-01','ESP','La fase final de la guerra termina con el parte franquista del1/4/1939. La dictadura, la represión y el exilio prosiguen después del fin militar; el cierre1940 sólo limita esta observación.',SPAIN),
('sino-japanese','Guerra chino-japonesa desde1937','conflict','1937-07-01','1945-09-03','CHN JPN','Los enfrentamientos de julio escalan a guerra a gran escala. La administración nacionalista, las bases comunistas y la ocupación japonesa no se reducen a un control chino uniforme. Inicio mensual, no día del primer combate.',STATE+'milestones/1937-1945/pearl-harbor'),
('austria','Anexión de Austria por la Alemania nazi','transition','1938-03-12','1939-01-01','AUT DEU','La entrada militar alemana abre la anexión de Austria. El registro no la trata como una alianza voluntaria.',WW2),
('munich','Múnich y desmembramiento de Checoslovaquia','transition','1938-09-29','1939-03-16','CSK DEU','La cesión de los Sudetes precede a la ocupación alemana de las tierras checas y la separación eslovaca en marzo1939.',WW2),
('poland','Invasiones de Polonia y guerra europea','conflict','1939-09-01','1939-10-07','POL DEU SUN GBR FRA','Alemania invade Polonia; Reino Unido y Francia declaran la guerra. La URSS invade desde el este el17/9.','https://encyclopedia.ushmm.org/content/en/article/invasion-of-poland-fall-1939'),
('winter-war','Guerra de Invierno','conflict','1939-11-30','1940-03-14','FIN SUN','La URSS invade Finlandia; la paz de marzo1940 impone cesiones territoriales. No constituye anexión de toda Finlandia.',WW2),
('west-1940','Ofensivas alemanas en Europa occidental','conflict','1940-04-09','1940-07-01','DEU DNK NOR NLD BEL LUX FRA GBR','Las ofensivas alcanzan Escandinavia y Europa occidental. La derrota francesa no pone fin a la guerra británica.',WW2),
('france-1940','Vichy y Francia Libre','transition','1940-07-10','1944-08-26','FRA','Pétain recibe plenos poderes; Francia Libre sostiene la continuación de la lucha. Sus legitimidades, administraciones y territorios difieren.','https://www.assemblee-nationale.fr/histoire/7da.asp'),
('barbarossa','Invasión alemana de la Unión Soviética','conflict','1941-06-22','1942-01-01','DEU SUN','Alemania invade la URSS. Esta fase cubre1941; la guerra oriental continúa.','https://encyclopedia.ushmm.org/content/en/article/the-soviet-union-and-the-eastern-front'),
('pacific','Pearl Harbor y guerra del Pacífico','conflict','1941-12-07','1942-01-01','JPN USA GBR CHN','El ataque japonés a Pearl Harbor precipita la entrada estadounidense en guerra. El corte1942 es editorial; no cese de hostilidades.','https://www.history.navy.mil/research/library/online-reading-room/title-list-alphabetically/c/cincpac-report.html'),
('ww2-1942','Segunda Guerra Mundial · fase de1942','conflict','1942-01-01','1943-01-01','DEU SUN JPN USA GBR ITA','Las campañas continúan en Europa, África y el Pacífico. Ventana anual, sin interpolación de frentes ni control diario.',WW2),
('holocaust','Deportación y exterminio de los judíos europeos','conflict','1942-01-01','1945-05-09','DEU POL SUN','La fase de1942–1945 documenta la expansión del exterminio y las deportaciones nazis. La persecución y las matanzas habían comenzado antes; no se presenta1942 como origen del Holocausto.','https://www.auschwitz.org/en/history/before-the-extermination/the-final-solution'),
('italy-1943','Italia · caída de Mussolini y división','transition','1943-07-25','1944-01-01','ITA DEU','La destitución de Mussolini y el armisticio preceden a ocupación alemana, resistencia y autoridades rivales. La monarquía no termina en1943.','https://www.senato.it/legislature/regno/italia/30/resoconti-elenco-cronologico'),
('normandy','Desembarco aliado en Normandía','conflict','1944-06-06','1944-09-01','FRA DEU GBR USA CAN','El desembarco del6/6 abre la campaña de Normandía. La fase no equivale a liberación inmediata de toda Francia.','https://www.archives.gov/research/military/ww2/d-day'),
('germany-surrender','Capitulación militar alemana','transition','1945-05-07','1946-01-01','DEU FRA GBR USA SUN','La firma de Reims del7/5 ordena cesar operaciones el8/5; el acto de Berlín sigue el8/5. Capitulación militar y tratado de paz no son equivalentes.','https://www.archives.gov/milestone-documents/surrender-of-germany'),
('japan-surrender','Rendición de Japón','transition','1945-09-02','1946-01-01','JPN USA CHN SUN GBR','El instrumento del2/9 formaliza la rendición japonesa y somete su Gobierno al mando aliado. El anuncio de agosto y las rendiciones locales son hitos distintos.','https://www.archives.gov/milestone-documents/surrender-of-japan'),
('germany-occupation','Alemania bajo ocupación aliada','transition','1945-05-08','1949-05-23','DEU SUN USA GBR FRA','Las potencias vencedoras administran zonas de ocupación y sectores de Berlín. Esta nota no aporta polígonos individuales de las cuatro zonas; el corte1949 abre otra fase sin extinguir todos los derechos aliados.',BERLIN),
('german-states','Formación de los dos Estados alemanes','transition','1949-05-23','1950-01-01','DEU DDR','La RFA se constituye en mayo y la RDA en octubre. La división institucional no extingue los derechos de las potencias ocupantes ni convierte Berlín en una ciudad de estatus ordinario.',BERLIN),
('japan-occupation','Ocupación y reformas en Japón','transition','1945-09-02','1950-01-01','JPN USA','El mando aliado dirigido por Estados Unidos supervisa reformas y reconstrucción. La monarquía conserva al emperador con funciones transformadas; el corte1950 limita esta ampliación, no termina la ocupación.',JAPAN),
('un','Carta de las Naciones Unidas','transition','1945-10-24','1946-01-01','USA GBR FRA CHN SUN IND','La Carta entra en vigor el24/10. Los miembros originales ratifican en fechas distintas durante1945; la India británica, Ucrania y Bielorrusia son casos de membresía que no equivalen a independencia nacional.',UN_FOUNDERS),
('france-constitution','Francia · Constitución de la Cuarta República','transition','1946-10-27','1947-01-01','FRA','La promulgación de la Constitución sigue al referéndum de octubre. El Gobierno provisional y la presidencia de la República no son cargos intercambiables.',FRANCE),
('italy-republic','Italia · referéndum republicano','transition','1946-06-02','1947-01-01','ITA','El referéndum y la elección constituyente abren la transición republicana. La proclamación de resultados y los relevos de jefatura estatal se fechan por separado.',ITALY),
('italy-constitution','Italia · Constitución republicana','transition','1948-01-01','1949-01-01','ITA','Entra en vigor la Constitución aprobada en diciembre1947. El presidente provisional de1946 y el presidente elegido en1948 pertenecen a fases institucionales distintas.','https://www.gazzettaufficiale.it/dettaglio/codici/costituzione'),
('japan-constitution','Japón · Constitución de posguerra','transition','1947-05-03','1948-01-01','JPN','La Constitución entra en vigor el3/5/1947 tras su promulgación de3/11/1946. Establece soberanía popular, emperador simbólico y gobierno parlamentario.','https://www.shugiin.go.jp/internet/itdb_english.nsf/html/statics/english/constitution_e.htm'),
('india-partition','Partición e independencia de India y Pakistán','transition','1947-08-15','1948-01-01','IND PAK GBR','La ley británica fija el15/8 para dos dominios independientes. La conmemoración pakistaní del14/8, la partición administrativa, el desplazamiento de población y las adhesiones a la ONU son hechos diferentes.',INDIA),
('philippines','Independencia de Filipinas','transition','1946-07-04','1947-01-01','PHL USA','Filipinas alcanza la independencia el4/7/1946. Su condición de miembro original de la ONU desde1945 precede a la independencia.','https://digitallibrary.un.org/record/3940161/files/Survey1948.pdf'),
('burma','Independencia de Birmania','transition','1948-01-04','1949-01-01','MMR GBR','La Unión de Birmania accede a la independencia el4/1/1948. El Gobierno provisional había establecido relaciones exteriores antes de la independencia plena.',STATE+'countries/burma'),
('ceylon','Independencia de Ceilán','transition','1948-02-04','1949-01-01','LKA GBR','Ceilán se convierte en dominio independiente el4/2/1948. La monarquía y la jefatura gubernamental se distinguen de la república posterior.','https://digitallibrary.un.org/record/3940161/files/Survey1948.pdf'),
('indonesia','Indonesia · revolución y transferencia de soberanía','conflict','1945-08-17','1949-12-28','IDN NLD','La proclamación indonesia de1945 precede a una guerra y negociaciones. La transferencia neerlandesa de27/12/1949 reconoce a los Estados Unidos de Indonesia; Nueva Guinea occidental queda fuera de ese acuerdo.',STATE+'historicaldocuments/frus1949v07p1/d413'),
('china-civil-war','China · reanudación de la guerra civil','conflict','1946-01-01','1949-10-01','CHN TWN','Tras los intentos de negociación de1945–1946, nacionalistas y comunistas vuelven a la guerra a gran escala. Inicio anual de cobertura, no día único de ruptura de la tregua.',CHINA),
('china-1949','República Popular y continuidad de la República de China','transition','1949-10-01','1950-01-01','CHN TWN','Mao proclama la República Popular el1/10; el Gobierno de la República de China se repliega a Taiwán. No termina toda la guerra ni se transfiere la representación china en la ONU en1949.',CHINA),
('palestine-mandate','Mandato británico de Palestina','transition','1923-09-29','1947-11-29','PSE ISR JOR GBR','El mandato aprobado por la Sociedad en1922 entra en vigor en1923. Administración mandataria no equivale a soberanía británica; las claves actuales sólo vinculan la historia territorial.','https://untso.unmissions.org/en/node/14110'),
('palestine-partition','Palestina · recomendación de partición','transition','1947-11-29','1948-05-15','PSE ISR GBR','La resolución181 recomienda dos Estados y un régimen internacional para Jerusalén. Es una propuesta de organización, sin acreditar que las fronteras propuestas se implantaran sobre el terreno.',PAL),
('arab-israeli-war','Guerra árabe-israelí de1948','conflict','1948-05-14','1949-07-21','ISR PSE EGY JOR SYR LBN IRQ','La proclamación israelí y el fin del mandato son seguidos por guerra interestatal. Se producen expulsiones y huidas de población palestina; ni las propuestas de1947 ni los contornos modernos reconstruyen esos frentes.',STATE+'milestones/1945-1952/arab-israeli-war'),
('armistices-1949','Armisticios árabe-israelíes de1949','transition','1949-02-24','1950-01-01','ISR PSE EGY JOR SYR LBN','Acuerdos separados con Egipto, Líbano, Jordania y Siria fijan líneas de armisticio durante1949. No son tratados de paz ni por sí mismos fronteras definitivas.',STATE+'milestones/1945-1952/arab-israeli-war'),
('korea-1948','Constitución de dos Estados en Corea','transition','1948-08-15','1950-01-01','KOR PRK','La República de Corea se establece el15/8 y la RPDC el9/9/1948 tras administraciones de ocupación separadas. Ninguna es miembro de la ONU en1948.','https://1997-2001.state.gov/regions/eap/fs_us_so_korea_relations.html'),
('truman','Doctrina Truman y ayuda a Grecia y Turquía','transition','1947-03-12','1948-01-01','GRC TUR USA GBR','El mensaje de Truman solicita ayuda para Grecia y Turquía tras el anuncio británico de retirada de apoyo. Una política de asistencia no equivale a adhesión anticipada a la OTAN.','https://www.archives.gov/milestone-documents/truman-doctrine'),
('marshall','Programa de recuperación europea','transition','1948-04-03','1950-01-01','USA GBR FRA ITA DEU','La ley estadounidense abre el programa de recuperación conocido como Plan Marshall. La ventana termina con esta ampliación documental, sin afirmar que el programa termine en1950.','https://www.archives.gov/milestone-documents/marshall-plan'),
('berlin','Bloqueo de Berlín y puente aéreo','conflict','1948-06-24','1949-05-13','DEU SUN USA GBR FRA','El bloqueo soviético del acceso terrestre a los sectores occidentales es respondido con un puente aéreo. Se levanta en mayo1949. La ficha no aporta los límites geométricos de cada sector.',BERLIN),
]
for args in events:
    event(*args)

record('soviet-federation','USSR','institutions','Unión soviética y repúblicas constituyentes','1922-12-31','1950-01-01','La URSS se forma en1922. El inicio es una observación al cierre de ese año, no la fecha jurídica diaria de constitución. Rusia no equivale al conjunto de la federación; Ucrania y Bielorrusia tienen membresía propia en la ONU desde1945 sin dejar por ello de ser repúblicas soviéticas. Fin1950: límite de esta revisión.','https://www.gov.uk/government/publications/country-names/timeline-of-country-name-changes-in-hmg-use-1919-to-present')
record('weimar','DEU','institutions','Weimar, presidencia y cancillería','1920-01-01','1933-01-30','Inicio1920: límite de revisión de una república fundada antes. El presidente del Reich y el canciller son jefaturas distintas; desde1930 los gabinetes presidenciales debilitan el funcionamiento parlamentario.','https://www.bundestag.de/en/parliament/history/parliamentarism/weimar')
record('german-dictatorship','DEU','institutions','Cancillería y dictadura nazi','1933-01-30','1945-05-09','El nombramiento de Hitler precede al desmantelamiento democrático de1933. La concentración posterior de funciones no convierte la presidencia de Hindenburg en cancillería ni anticipa la ocupación de1945.','https://www.bundestag.de/parlament/geschichte/100-jahre-weimar/machtuebergabe-972588')
record('german-occupation','DEU DDR','territory','Zonas aliadas y derechos de ocupación','1945-05-08','1950-01-01','La ocupación se organiza en cuatro zonas y Berlín en sectores. Los Estados creados en1949 no obtienen inmediatamente soberanía plena. Este inventario contextual no acredita que los cuatro polígonos de las zonas o sectores estén disponibles.',BERLIN)
record('italy-kingdom','ITA','institutions','Monarquía italiana y Gobierno fascista','1922-10-31','1943-07-26','Durante el Gobierno de Mussolini continúa la monarquía de Víctor Manuel III. Rey y jefe del Gobierno son autoridades diferentes; la destitución de julio1943 no termina por sí sola la monarquía.','https://www.senato.it/legislature/regno/italia/30/resoconti-elenco-cronologico')
record('italy-republic','ITA','institutions','Transición republicana y Constitución','1946-06-02','1950-01-01','El voto de junio1946 precede a la proclamación de resultados y al jefe provisional del Estado. La Constitución entra en vigor el1/1/1948. La ventana1950 sólo limita esta revisión.',ITALY)
record('france-rival','FRA FRA-VICHY FRA-FREE','institutions','Vichy y autoridades de la Francia Libre','1940-07-10','1944-08-26','El régimen de Vichy y las autoridades de la Francia Libre mantienen pretensiones de legitimidad rivales. Las claves separadas conservan mandatos propios; no se atribuye a Pétain la presidencia republicana de posguerra.','https://www.assemblee-nationale.fr/histoire/7da.asp')
record('france-fourth','FRA','institutions','De Gobierno provisional a Cuarta República','1944-08-25','1950-01-01','La Liberación y el Gobierno provisional preceden a la Constitución de1946 y a la elección presidencial de1947. Fin1950: corte de cobertura, no final del régimen.',FRANCE)
record('spain-republic','ESP ESP-REPUBLIC','institutions','Constitución republicana de1931','1931-12-09','1939-04-02','La Constitución distingue presidencia de la República y presidencia del Gobierno. Durante la guerra su autoridad territorial está disputada. La derrota militar no elimina la existencia posterior de instituciones republicanas en el exilio.','https://www.boe.es/gazeta/dias/1931/12/09/pdfs/D00001-00014.pdf')
record('spain-control','ESP ESP-REPUBLIC ESP-NATIONALIST','territory','Guerra Civil: resolución y fechas de los frentes','1936-07-17','1939-04-02','El atlas conserva las particiones documentadas existentes;1937 corresponde a octubre, no al cierre anual. Este contexto no añade frentes, enclaves ni control colonial que las fuentes geométricas no proporcionan.',SPAIN)
record('japan-parliament','JPN','institutions','Emperador simbólico y gabinete parlamentario','1947-05-03','1950-01-01','La Constitución establece soberanía popular y un emperador sin poderes de gobierno. La Dieta designa al primer ministro. El mando aliado conserva autoridad de ocupación; la ventana1950 no lo extingue.','https://www.shugiin.go.jp/internet/itdb_english.nsf/html/statics/english/constitution_e.htm')
record('china-representation','ROC CHN TWN CHN-COMMUNIST','relations','China: autoridades rivales y representación internacional','1945-10-24','1950-01-01','La República de China es miembro original de la ONU. Proclamar la República Popular en1949 no le transfiere entonces el asiento: la representación cambia con la resolución2758 de1971. La clave cartográfica no resuelve por sí sola legitimidad, control o reconocimiento.',CHINA)
record('india-dominion','IND PAK','institutions','Dominios de India y Pakistán','1947-08-15','1950-01-01','La independencia establece dos dominios. La India continúa la membresía original de1945; Pakistán ingresa el30/9/1947. Los jefes de Estado, gobernadores generales y primeros ministros se conservan como funciones distintas.',INDIA)
record('mandates','PSX JOR IRQ SYR LBN NAM TAN','territory','Mandatos: administración y soberanía','1920-01-01','1947-01-01','Inicio1920: cobertura temática, no fecha uniforme de creación de los mandatos. Cada territorio requiere su instrumento y administrador. Un mandato de la Sociedad y una tutela de la ONU no son categorías intercambiables; no todos los mandatos pasaron al régimen de tutela.','https://www.icj-cij.org/case/10')
record('palestine-status','PSX ISR JOR','territory','Palestina: mandato, partición propuesta y armisticios','1923-09-29','1950-01-01','El mandato es administración, sin transferencia de soberanía al mandatario. La resolución181 recomienda una organización territorial; las líneas de1949 son de armisticio. Las referencias a entidades actuales no las convierten en Estados existentes durante todo el mandato.',PAL)
record('depression-economy','USA DEU GBR FRA JPN','economy','Gran Depresión sin series inventadas','1929-10-01','1940-01-01','Crisis financiera y contracción internacional, con políticas y recuperaciones desiguales. El registro es cualitativo: no asigna PIB, desempleo o población sin fuente estadística propia. Octubre1929 y el fin1939 delimitan esta fase editorial; no son límites universales del fenómeno.',DEPRESSION)
record('oas-charter','ARG BOL BRA CHL COL CRI CUB DOM ECU SLV GTM HTI HND MEX NIC PAN PRY PER USA URY VEN','relations','OEA: firma constitutiva y vigencia de la Carta','1948-04-30','1952-01-01','La OEA se constituye mediante la firma de Bogotá de30/4/1948. La Carta entra en vigor el13/12/1951 y las ratificaciones estatales tienen fechas diferentes. El intervalo de fundador del catálogo no afirma ratificación individual en1948.',OAS)
record('arab-pact','EGY IRQ LBN JOR SAU SYR YMK','relations','Liga Árabe: firma y ratificaciones','1945-03-22','1947-01-01','El pacto se firma el22/3/1945 y entra en vigor el10/5. El registro depositario distingue efectos para Líbano1/6, Siria4/6 y Yemen24/2/1946; no se proyecta el Yemen unificado ni el Yemen meridional a los fundadores.',ARAB)

relation('republic-to-prc',('ROC','República de China',1948),('CHN','República Popular China',1949),'1949-10-01','Proclamación de la República Popular',CHINA,'Autoridades rivales: no implica extinción de la República de China, cesión jurídica de todo el territorio ni transferencia de representación ONU en1949.')
relation('roc-taiwan',('ROC','República de China en el continente',1948),('TWN','República de China en Taiwán',1949),'1949-12-31','Repliegue de las autoridades de la República de China',CHINA,'Observación al cierre de1949, no día de traslado de todas las oficinas; continuidad de autoridades, no creación de un miembro independiente nuevo de la ONU.')
relation('germany-east',('DEU','Alemania bajo ocupación',1948),('DDR','República Democrática Alemana',1949),'1949-10-07','Constitución de la RDA','https://www.bundestag.de/en/parliament/history/parliamentarism/gdr','La fecha del evento es distinta del año de navegación; no se atribuyen a la RDA todos los territorios o autoridades de Alemania anterior.')
for code,name,date,source in [('PAK','Pakistán','1947-08-15',INDIA),('MMR','Unión de Birmania','1948-01-04',STATE+'countries/burma'),('LKA','Ceilán','1948-02-04','https://digitallibrary.un.org/record/3940161/files/Survey1948.pdf')]:
    relation('independence-'+code,('GBR','Reino Unido',int(date[:4])-1),(code,name,int(date[:4])),date,'Independencia de '+name,source,'Enlace al administrador colonial: no supone que el territorio fuese parte metropolitana ni transfiere estadísticas o autoridades sucesoras al pasado.')
relation('philippine-independence',('USA','Estados Unidos',1945),('PHL','Filipinas',1946),'1946-07-04','Independencia de Filipinas','https://digitallibrary.un.org/record/3940161/files/Survey1948.pdf','Independencia posterior a su condición de miembro original de la ONU; no fecha de adhesión a esa organización.')
relation('indonesian-sovereignty',('NLD','Países Bajos',1948),('IDN','Estados Unidos de Indonesia',1949),'1949-12-27','Transferencia neerlandesa de soberanía',STATE+'historicaldocuments/frus1949v07p1/d413','La proclamación indonesia fue en1945. La transferencia de1949 deja fuera Nueva Guinea occidental y no unifica por sí sola todas las fases administrativas.')

# Extend the one existing phase instead of duplicating its1950–1954 coverage.
for e in c['events']:
    if e['id'] == 'extension-1950-indochina':
        e.update(start='1946-12-19', countries=['VDR','VSV','RVN','VNM','FRA','LAO','KHM'], source='https://www.archives.gov/exhibits/remembering-vietnam-online-exhibit-episodes-1-4', text='Tras violencia y negociaciones desde1945, los combates de Hanoi del19/12/1946 abren la guerra a gran escala. La República Democrática proclamada en1945 y el Estado de Vietnam asociado de1949 tienen autoridades rivales. Los acuerdos y ceses del fuego escalonados de1954 no convierten retrospectivamente sus áreas de implantación en dos Estados definitivos ni aportan frentes diarios.')
        e['note'] = 'La extensión a1946 conserva el final ya documentado de1954. Las fechas de proclamación, asociación, reconocimiento y control territorial son distintas.'

c.update(startYear=1920, retrieved='2026-10-24')
save('affiliations.json', d)
save('historical-context.json', c)
save('country-history.json', h)
print('Prepared',len(d['organizations']),'organizations;',sum(len(o['memberships']) for o in d['organizations']),'membership intervals;',len(c['events']),'context phases;',len(h['relations']),'relations;',len(h['records']),'country records.')
print('1920 extension:',sum(e['id'].startswith(PREFIX) for e in c['events']),'phases;',sum(r['id'].startswith(PREFIX) for r in h['relations']),'links;',sum(r['id'].startswith(PREFIX) for r in h['records']),'records; League',len(orgs['leagueOfNations']['memberships']),'intervals; UN',len(orgs['un']['memberships']),'intervals.')
