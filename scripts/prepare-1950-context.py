"""Incremental 1950–1959 institutions and context. Annual observations are not daily fronts.

Run after prepare-1960-context.py if rebuilding older stages. Preserves unrelated records.
"""
import copy
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1] / 'public/data'
PREFIX = 'extension-1950-'
def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf8'))
def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

d = read('affiliations.json')
orgs = {o['id']: o for o in d['organizations']}
annual = 'Observación al cierre del año documentado; no fecha jurídica diaria de adhesión.'
boundary = 'Pertenencia anterior al inicio de la revisión de 1950; no fecha jurídica de adhesión.'
arab_source = 'https://unterm.un.org/unterm2/view/38727503-9e12-41bd-9e0b-ccb02590ec3c'
for oid in ('arabLeague', 'comecon', 'oas'):
    for m in orgs[oid]['memberships']:
        if m['start'] != '1960-01-01':
            continue
        m['start'] = '1950-01-01'
        m['note'] = boundary
        m['startIsCoverageBoundary'] = True
        if oid == 'arabLeague':
            joined = {'LBY': '1953-12-31', 'SDN': '1956-12-31', 'MAR': '1958-12-31', 'TUN': '1958-12-31'}
            if m['code'] in joined:
                m.update(start=joined[m['code']], note=annual, source=arab_source)
                m.pop('startIsCoverageBoundary', None)
        if oid == 'comecon' and m['code'] == 'DDR':
            m.update(start='1950-12-31', note='La RDA se incorpora en septiembre de 1950; observación al cierre anual, no día jurídico.', source='https://www.marxists.org/history/ussr/government/foreign-relations/sovietforeignpolicy-vol2-1945-80.pdf')
            m.pop('startIsCoverageBoundary', None)

def membership(oid, code, start, end=None, category='member', note='', source=None, coverage=False):
    m = dict(code=code, start=start, category=category, source=source or orgs[oid]['source'])
    if end:
        m['end'] = end
    if note:
        m['note'] = note
    if coverage:
        m['startIsCoverageBoundary'] = True
    if not any((x['code'], x['start'], x['category']) == (code, start, category) for x in orgs[oid]['memberships']):
        orgs[oid]['memberships'].append(m)

# Ratification/entry into force, distinct from the signature on 14 May.
warsaw_source = 'https://treaties.un.org/pages/showDetails.aspx?objid=08000002801488a3'
for m in orgs['warsaw']['memberships']:
    if m['start'] in ('1960-01-01', '1955-06-06'):
        m.update(start='1955-06-06', source=warsaw_source, note='Tratado firmado el 14/5/1955, en vigor el 6/6/1955 según el registro depositario de Naciones Unidas. La RDA es signataria; su integración militar posterior no es otra adhesión estatal.')
        m.pop('startIsCoverageBoundary', None)

# The 1962 exclusion concerns the Government, not expulsion of the Cuban State.
oas_source = 'https://www.oas.org/en/media_center/press_release.asp?sCodigo=GA-12-09'
for m in orgs['oas']['memberships']:
    if m['code'] == 'CUB' and m['category'] == 'suspended' and m['start'] < '1962-01-31':
        m.update(start='1962-01-31', source=oas_source, note='Exclusión del Gobierno cubano de la participación, resolución VI de 31/1/1962; no expulsión del Estado. Resolución dejada sin efecto el 3/6/2009, sin reincorporación automática.')
        m.pop('startIsCoverageBoundary', None)
membership('oas', 'CUB', '1950-01-01', '1962-01-31', source=oas_source, note=boundary, coverage=True)

# One political union, not two independent countries in 1958–1960.
uar_source = 'https://www.un.org/en/about-us/growth-in-un-membership'
for code in ('EGY', 'SYR'):
    rows = orgs['arabLeague']['memberships']
    for m in list(rows):
        if m['code'] == code and m['start'] == '1950-01-01':
            former_end = m.get('end')
            m['end'] = '1958-02-22'
            membership('arabLeague', code, '1961-09-28', former_end, note='Continuidad tras terminar la unión territorial de Egipto y Siria; Egipto conservó el nombre RAU. No es una nueva adhesión a la Liga.', source=arab_source)
membership('arabLeague', 'UAR', '1958-02-22', '1961-09-28', note='Clave cartográfica de la unión Egipto–Siria. No asigna sus relaciones a dos Estados independientes durante la unión ni confunde esta continuidad con la de Naciones Unidas.', source=arab_source)

def organization(oid, label, kind, description, formed, source, dissolved=None):
    o = dict(id=oid, label=label, type=kind, description=description, formed=formed, source=source, memberships=[])
    if dissolved:
        o['dissolved'] = dissolved
    orgs[oid] = o
    return o

six = ('BEL', 'DEU', 'FRA', 'ITA', 'LUX', 'NLD')
ecs_source = 'https://www.consilium.europa.eu/en/schuman-declaration/'
organization('ecsc', 'Comunidad Europea del Carbón y del Acero · CECA', 'economic', 'Tratado sectorial en vigor desde1952 hasta2002, distinto de la CEE creada en1958. Incluye ampliaciones documentadas de las Comunidades; no convierte toda la UE actual en miembro de1952.', '1952-07-23', ecs_source, '2002-07-23')
for m in orgs['eu']['memberships']:
    if m.get('territorialApplication') or m['start'] >= '2002-07-23':
        continue
    membership('ecsc', m['code'], '1952-07-23' if m['code'] in six else m['start'], min(m.get('end', '2002-07-23'), '2002-07-23'), m['category'], 'Los seis fundadores desde la entrada en vigor del Tratado de París; las ampliaciones posteriores siguen las fechas comunitarias.', ecs_source if m['code'] in six else m['source'])

eur_source = 'https://www.consilium.europa.eu/en/documents/treaties-agreements/agreement/?id=1957003'
organization('euratom', 'Comunidad Europea de la Energía Atómica · Euratom', 'economic', 'Comunidad para cooperación nuclear civil, en vigor desde1958. Separada de la CECA y de la CEE/UE; compartir miembros no implica una alianza militar.', '1958-01-01', eur_source)
orgs['euratom']['memberships'] = [copy.deepcopy(m) for m in orgs['eu']['memberships'] if not m.get('territorialApplication')]
for m in orgs['euratom']['memberships']:
    if m['code'] in six:
        m['source'] = eur_source

anzus_source = 'https://nzhistory.govt.nz/anzus-comes-into-force'
organization('anzus', 'Tratado ANZUS', 'military', 'Tratado Australia–Nueva Zelanda–Estados Unidos, firmado1951 y en vigor1952. La suspensión estadounidense de obligaciones hacia Nueva Zelanda desde1986 se distingue de una expulsión o extinción formal del tratado.', '1952-04-29', anzus_source)
for code in ('AUS', 'USA'):
    membership('anzus', code, '1952-04-29')
membership('anzus', 'NZL', '1952-04-29', '1986-12-31')
membership('anzus', 'NZL', '1986-12-31', category='suspended', source='https://history.state.gov/milestones/1945-1952/anzus', note='Observación al cierre de1986, no fecha diaria: Estados Unidos suspende sus obligaciones hacia Nueva Zelanda; no equivale a expulsión del tratado ni a interrupción de la relación Australia–Nueva Zelanda. Esta categoría resume una relación bilateral asimétrica.')

seato_source = 'https://www.treaties.mfat.govt.nz/search/details/t/799/2870'
organization('seato', 'Organización del Tratado del Sudeste Asiático · SEATO', 'military', 'Ocho partes del Tratado de Manila; firma1954 y entrada en vigor1955. Laos, Camboya y Vietnam protegido por protocolo no se cuentan como miembros. La disolución de la organización en1977 no equivale a extinción del tratado.', '1955-02-19', seato_source, '1977-07-01')
for code in ('AUS', 'FRA', 'GBR', 'NZL', 'PAK', 'PHL', 'THA', 'USA'):
    membership('seato', code, '1955-02-19', '1973-12-31' if code == 'PAK' else '1977-07-01', note=('Salida pakistaní durante1973; cierre anual usado como observación, no día jurídico.' if code == 'PAK' else 'La participación militar francesa se redujo antes del cierre de la organización; no se interpreta como otra fecha de adhesión.' if code == 'FRA' else ''), source='https://history.state.gov/milestones/1953-1960/seato' if code in ('PAK', 'FRA') else seato_source)

cento_source = 'https://history.state.gov/historicaldocuments/frus1955-57v12/d1'
organization('cento', 'Pacto de Bagdad / CENTO', 'military', 'Pacto firmado en1955 y renombradoCENTO en1959 tras la retirada iraquí. Estados Unidos apoyó y participó en comités, pero no fue miembro pleno. Fuentes discrepan en alguna fecha iraní: el catálogo sigue la cronología FRUS indicada.', '1955-02-24', cento_source, '1979-09-26')
for code, date in [('IRQ', '1955-04-15'), ('TUR', '1955-04-15'), ('GBR', '1955-04-05'), ('PAK', '1955-09-23'), ('IRN', '1955-11-03')]:
    end = '1959-12-31' if code == 'IRQ' else '1979-01-01' if code in ('PAK', 'IRN') else '1979-09-26'
    # Iran/Pakistan's 1979 withdrawal requires a daily review: stop this observation
    # at its last fully covered annual close, without inventing the legal date.
    note = 'Fecha de adhesión según FRUS; Reino Unido adhiere antes del canje bilateral de ratificaciones de15/4.'
    if code == 'IRQ':
        note += ' Retirada en1959; observación al cierre anual, no fecha diaria. Al cierre de1959 ya no es miembro.'
    elif code in ('IRN', 'PAK'):
        note += ' Fin de cobertura al comenzar1979: no fecha jurídica de retirada, ocurrida durante ese año. Pendiente contraste diario.'
    membership('cento', code, date, end, note=note)

for o in orgs.values():
    o['memberships'].sort(key=lambda m: (m['code'], m['start'], m['category']))
d['organizations'] = sorted(orgs.values(), key=lambda o: o['id'])
d.update(coverageStart=1950, expandedReferenceDate='2026-10-23')
save('affiliations.json', d)

c = read('historical-context.json')
c['events'] = [e for e in c['events'] if not e['id'].startswith(PREFIX)]
def event(ident, title, kind, start, end, keys, text, source, note=''):
    c['events'].append(dict(id=PREFIX + ident, title=title, type=kind, start=start, end=end, countries=keys, text=text, source=source, sourceLabel='Fuente institucional o documento del periodo', note=note))

state = 'https://history.state.gov/countries/'
for code, name, date, source in [
    ('LBY', 'Libia', '1951-12-24', 'https://digitallibrary.un.org/record/228971/files/E_2508-EN.pdf'),
    ('SDN', 'Sudán', '1956-01-01', state+'sudan'),
    ('MAR', 'Marruecos', '1956-03-02', state+'morocco'),
    ('TUN', 'Túnez', '1956-03-20', 'https://www.justice.gov.tn/index.php?L=3&id=435'),
    ('GHA', 'Ghana', '1957-03-06', state+'ghana'),
    ('MAL', 'Federación de Malaya', '1957-08-31', state+'malaysia'),
]:
    event('independence-'+code, 'Independencia de '+name, 'transition', date, str(int(date[:4])+1)+'-01-01', [code], name+' accede a la independencia. El cierre cartográfico anual no reproduce cada fase del relevo; independencia, reconocimiento exterior y adhesión a la ONU son hechos distintos.', source)

event('guinea', 'Independencia de Guinea', 'transition', '1958-12-31', '1959-01-01', ['GIN', 'FRA'], 'Guinea se independiza en1958 al separarse del marco francés; Estados Unidos reconoce al nuevo Estado el1/11. La fecha de este registro es una observación al cierre anual, no la proclamación de independencia.', state+'guinea', 'La fecha diaria de proclamación requiere fuente nacional adicional; no se sustituye por la de reconocimiento estadounidense.')
events = [
('korea','Guerra de Corea','conflict','1950-06-25','1953-07-28',['KOR','PRK','CHN','USA'],'La invasión norcoreana abre la guerra. El armisticio de27/7/1953 suspende hostilidades y establece una línea de demarcación; no es un tratado de paz ni convierte la frontera de1950 en frente permanente.','https://www.unc.mil/History/1951-1953-Armistice-Negotiations/'),
('korea-armistice','Armisticio y división de Corea','transition','1953-07-27','1960-01-01',['KOR','PRK'],'La zona desmilitarizada se define a partir del armisticio, no de una anexión reconocida. El corte1960 limita esta ampliación documental; el armisticio no termina ese año.','https://www.unc.mil/History/1951-1953-Armistice-Negotiations/'),
('indochina','Primera guerra de Indochina y acuerdos de Ginebra','conflict','1950-01-01','1954-08-02',['VDR','RVN','VNM','FRA','LAO','KHM'],'La guerra iniciada antes de1950 concluye con acuerdos y ceses del fuego escalonados en1954. El reagrupamiento vietnamita no constituye dos Estados definitivos acordados ni delimita todos los frentes anteriores.','https://history.state.gov/milestones/1953-1960/dien-bien-phu'),
('vietnam-division','Vietnam tras los acuerdos de1954','transition','1954-07-21','1960-01-01',['VDR','RVN','VNM'],'El norte y el sur desarrollan autoridades rivales. El Estado de Vietnam precede a la República proclamada en1955: no se debe mostrar a su presidente republicano en1954.','https://visit.archives.gov/whats-on/explore-exhibits/episode-2-eisenhower-backs-diem'),
('suez','Crisis de Suez','conflict','1956-07-26','1957-04-01',['EGY','ISR','FRA','GBR'],'La nacionalización del canal es seguida por la ofensiva israelí y la intervención franco-británica. Las retiradas posteriores no equivalen a anexión reconocida de Egipto; este intervalo contextual no acredita frentes diarios.','https://history.state.gov/milestones/1953-1960/suez'),
('hungary','Revolución húngara e intervención soviética','conflict','1956-10-23','1957-01-01',['HUN','SUN'],'La revolución y la declaración de neutralidad de Nagy preceden a la intervención soviética de4/11. Kádár encabeza un Gobierno rival respaldado por Moscú; el mapa anual no reconstruye el combate urbano.','https://november4.kormany.hu/about-the-memorial-day'),
('east-germany','Levantamiento en la RDA','conflict','1953-06-16','1954-01-01',['DDR','SUN'],'Las protestas de junio se extienden y son reprimidas con intervención soviética. El registro de país no representa los sectores de Berlín ni el control de cada calle.','https://history.state.gov/milestones/1953-1960/east-german-uprising'),
('taiwan-one','Primera crisis del estrecho de Taiwán','conflict','1954-09-01','1956-01-01',['CHN','TWN','USA'],'Bombardeos y operaciones sobre islas del estrecho agravan el enfrentamiento entre la República Popular China y la República de China. Las islas y su control requieren cartografía específica.','https://history.state.gov/milestones/1953-1960/taiwan-strait-crises'),
('taiwan-two','Segunda crisis del estrecho de Taiwán','conflict','1958-01-01','1959-01-01',['CHN','TWN','USA'],'Nuevos bombardeos sobre Jinmen y Mazu y apoyo estadounidense a su abastecimiento. La ventana es anual: no afirma un año entero de combate continuo.','https://history.state.gov/milestones/1953-1960/taiwan-strait-crises'),
('cuba','Cambio de Gobierno en Cuba','transition','1959-01-01','1960-01-01',['CUB'],'La caída de Batista abre una sucesión de autoridades revolucionarias durante1959. No se atribuye a Fidel Castro toda jefatura estatal o gubernamental desde el primer día.','https://1997-2001.state.gov/regions/wha/cuba_chronology.html'),
('bandung','Conferencia afroasiática de Bandung','transition','1955-04-01','1956-01-01',['IDN','IND','CHN','PAK','MMR','LKA','EGY'],'Reunión afroasiática de abril sobre soberanía, cooperación y descolonización. Participar en una conferencia no equivale a una alianza militar ni a pertenecer ya a una organización posterior.','https://history.state.gov/milestones/1953-1960/bandung-conf'),
('uar','Constitución de la República Árabe Unida','transition','1958-02-22','1960-01-01',['UAR','EGY','SYR'],'La unión de Egipto y Siria constituye una entidad común. La ventana documental termina al comenzar1960; la unión continúa hasta septiembre1961.','https://www.un.org/en/about-us/growth-in-un-membership'),
('nato','Ampliaciones de la OTAN','transition','1952-02-18','1956-01-01',['GRC','TUR','DEU'],'Grecia y Turquía ingresan el18/2/1952; la República Federal de Alemania lo hace el6/5/1955. La RDA no pertenece a la OTAN.','https://www.nato.int/cps/en/natohq/news_84445.htm'),
('europe','CECA y Tratados de Roma','transition','1952-07-23','1960-01-01',['BEL','DEU','FRA','ITA','LUX','NLD'],'Los seis fundadores integran la CECA desde1952; la CEE y Euratom entran en vigor en1958. No se proyecta la Unión Europea actual a1950.','https://europa.eu/abc/12lessons/key_dates_en.htm'),
]
for args in events:
    event(*args, note='Síntesis focal, no censo mundial ni reconstrucción de frentes. Los límites1950/1960 y cierres anuales pueden delimitar cobertura, no inicio o final jurídico del fenómeno.')
# Extend the previously reviewed Algerian conflict without creating two copies
# for 1960–1962, preserving its source and subsequent chronology.
for e in c['events']:
    if e['id'] == 'extension-1960-algeria':
        e['start'] = '1954-11-01'
        e['text'] = 'La insurrección iniciada el1/11/1954 abre la guerra de independencia. La administración francesa y las autoridades independentistas no equivalen a un control uniforme de cada punto. Los acuerdos e independencia de1962 cierran el proceso; no hay frentes diarios en este inventario.'
        e['source'] = 'https://www.cheminsdememoire.gouv.fr/fr/la-guerre-dalgerie-1954-1962'
c.update(startYear=1950, retrieved='2026-10-23')
save('historical-context.json', c)

h = read('country-history.json')
h['relations'] = [r for r in h['relations'] if not r['id'].startswith(PREFIX)]
h['records'] = [r for r in h['records'] if not r['id'].startswith(PREFIX)]
for code, name, date, source in [('GHA','Ghana','1957-03-06',state+'ghana'),('MAL','Federación de Malaya','1957-08-31',state+'malaysia'),('SDN','Sudán','1956-01-01',state+'sudan'),('MAR','Marruecos','1956-03-02',state+'morocco'),('TUN','Túnez','1956-03-20','https://www.justice.gov.tn/index.php?L=3&id=435')]:
    owner = 'FRA' if code in ('MAR','TUN') else 'GBR'
    owner_name = 'Francia' if owner == 'FRA' else 'Reino Unido'
    h['relations'].append(dict(id=PREFIX+'independence-'+code, **{'from':dict(key=owner,name=owner_name,year=int(date[:4])-1),'to':dict(key=code,name=name,year=int(date[:4]))}, date=date, type='transition', label='Independencia de '+name, note='Enlace al administrador principal; no afirma que el territorio fuese parte metropolitana ni excluye otras autoridades. Sudán era un condominio anglo-egipcio y Marruecos también tenía zona española.', source=source, sourceLabel='Documento institucional de la independencia'))
for code in ('EGY','SYR'):
    h['relations'].append(dict(id=PREFIX+'uar-'+code, **{'from':dict(key=code,name='Egipto' if code=='EGY' else 'Siria',year=1957),'to':dict(key='UAR',name='República Árabe Unida',year=1958)}, date='1958-02-22', type='transition', label='Unión en la República Árabe Unida', note='La unión territorial no transfiere retrospectivamente estadísticas modernas ni prolonga su alcance tras la separación siria.', source=uar_source, sourceLabel='Naciones Unidas · continuidad de los miembros'))
for ident,a,b,date,label,source in [
    ('malaya-malaysia',('MAL','Federación de Malaya',1962),('MYS','Malasia',1963),'1963-09-16','Formación de Malasia',state+'malaysia'),
    ('vietnam-republic',('VSV','Estado de Vietnam',1954),('RVN','República de Vietnam',1955),'1955-10-26','Proclamación de la República de Vietnam','https://avalon.law.yale.edu/20th_century/inch036.asp')]:
    h['relations'].append(dict(id=PREFIX+ident,**{'from':dict(key=a[0],name=a[1],year=a[2]),'to':dict(key=b[0],name=b[1],year=b[2])},date=date,type='transition',label=label,note='Transición entre entidades, sin transferir automáticamente estadísticas ni todos los cargos de una a otra.',source=source,sourceLabel='Fuente de la transición'))
records = [
('MAL','Federación de Malaya, anterior a Malasia','1957-08-31','1963-09-16','La Federación de Malaya obtiene independencia en1957. Malasia se forma en1963 con Singapur, Sarawak y Borneo Septentrional; no se atribuye esa composición a1957.',state+'malaysia'),
('SDN','Independencia tras el condominio','1950-01-01','1957-01-01','Sudán permanece bajo un condominio anglo-egipcio hasta la independencia de1/1/1956. El administrador principal del inventario no elimina el papel egipcio. El inicio1950 es cobertura, no fundación del condominio.',state+'sudan'),
('LAO','Reino asociado y soberanía laosiana','1950-01-01','1960-01-01','Laos tiene instituciones monárquicas propias dentro de la Unión Francesa al iniciarse la década. Reconocimiento exterior, transferencia de competencias y acuerdos de1954 son hitos distintos.',state+'laos'),
('KHM','Monarquía camboyana y fin del protectorado','1950-01-01','1960-01-01','El reino conserva instituciones propias y una trayectoria escalonada desde el marco de la Unión Francesa. No se sustituye su soberano por el presidente de Francia ni se confunde reconocimiento estadounidense con independencia plena.',state+'cambodia'),
('KOR','División coreana y armisticio','1950-06-25','1960-01-01','La guerra transforma el control territorial y termina en armisticio militar en1953. La línea de demarcación difiere del paralelo38; no hay tratado de paz en esta década.','https://www.unc.mil/History/1951-1953-Armistice-Negotiations/'),
('PRK','División coreana y armisticio','1950-06-25','1960-01-01','La República Popular Democrática de Corea y la República de Corea mantienen autoridades separadas. El armisticio de1953 no implica reconocimiento mutuo ni reunificación.','https://www.unc.mil/History/1951-1953-Armistice-Negotiations/'),
('VDR','Reagrupamiento vietnamita','1954-07-21','1960-01-01','Los acuerdos de1954 delimitan zonas de reagrupamiento militar. Un polígono anual del norte no reconstruye toda la implantación territorial de las autoridades antes ni después del alto el fuego.','https://history.state.gov/milestones/1953-1960/dien-bien-phu'),
('RVN','Estado de Vietnam y República de Vietnam','1954-07-21','1960-01-01','El Estado de Vietnam con Bảo Đại precede a la proclamación republicana de1955. Ngô Đình Diệm dirige el Gobierno antes de ser presidente; no son cargos intercambiables.','https://visit.archives.gov/whats-on/explore-exhibits/episode-2-eisenhower-backs-diem'),
('CUB','Sucesión revolucionaria de1959','1959-01-01','1960-01-01','Durante1959 cambian las presidencias y la jefatura del Gobierno. La caída de Batista no hace de Castro presidente de la República; las fechas de cada cargo deben mantenerse separadas.','https://1997-2001.state.gov/regions/wha/cuba_chronology.html'),
]
for key,title,start,end,text,source in records:
    h['records'].append(dict(id=PREFIX+'institution-'+key,keys=[key],start=start,end=end,section='institutions',title=title,text=text,source=source,sourceLabel='Fuente institucional del marco político'))
save('country-history.json',h)
print('Prepared',len(d['organizations']),'organizations;',sum(len(o['memberships']) for o in d['organizations']),'membership intervals;',len(c['events']),'context phases;',len(h['relations']),'relations;',len(h['records']),'institutional records.')
