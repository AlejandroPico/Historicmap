"""Build dated political profiles from cached Wikidata CC0 and licensed Commons files.
Explicit focal intervals override broad source statements. No undated current leader
or flag is carried backwards. Run with Python 3; network only during preparation.
"""
import concurrent.futures, datetime, hashlib, html, json, pathlib, re, sys, time
import urllib.request, urllib.parse

ROOT=pathlib.Path(__file__).resolve().parents[1]
CACHE=ROOT/'.cache/identities'; CACHE.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'public'; MEDIA=OUT/'media'; MEDIA.mkdir(exist_ok=True)
TODAY=datetime.date.today().isoformat()
UA={'User-Agent':'Historicmap/0.4 (https://github.com/AlejandroPico/Historicmap; educational historical atlas)'}
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
def get(url,key):
    path=CACHE/(key+'.json')
    if path.exists():return json.loads(path.read_text(encoding='utf8'))
    for i in range(3):
        try:
            req=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(req,timeout=45) as r:d=json.load(r)
            save(path,d);return d
        except urllib.error.HTTPError as error:
            if error.code==429:raise
            if i==2:raise
            time.sleep(1+i)
        except Exception:
            if i==2:raise
            time.sleep(1+i)
def entity(q):
    d=get('https://www.wikidata.org/wiki/Special:EntityData/'+q+'.json',q)
    return d['entities'][q]
def values(e,p):return [s['mainsnak']['datavalue']['value'] for s in e.get('claims',{}).get(p,[]) if s.get('rank')!='deprecated' and 'datavalue' in s['mainsnak']]
def label(e):return e.get('labels',{}).get('es',e.get('labels',{}).get('en',{'value':e['id']}))['value']
def qualifier(s,p):
    a=s.get('qualifiers',{}).get(p,[])
    if not a or 'datavalue' not in a[0]:return None
    v=a[0]['datavalue']['value']
    if not isinstance(v,dict) or 'time' not in v:return None
    t=v['time'].lstrip('+')[:10]
    # A year-only assertion does not establish the exact day; retain source precision.
    return t.replace('-00','-01'),v.get('precision',11)
def safe(call,value):
    try:return call(value)
    except Exception as error:print('Unavailable',value,str(error)[:100],flush=True);return None
def parallel(fn,items,workers=6):
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:return list(pool.map(lambda x:safe(fn,x),items))

natural=json.loads((ROOT/'.cache/natural-countries.json').read_text(encoding='utf8'))
qid_codes={}
for f in natural['features']:
    p=f['properties'];q=p.get('WIKIDATAID','')
    if q.startswith('Q'):qid_codes.setdefault(q,[]).append(p['ADM0_A3'])
special={'USA':'Q30','ESP':'Q29','DEU':'Q183','DDR':'Q16957','USSR':'Q15180','RUS':'Q159','FRA':'Q142','CHN':'Q148','TWN':'Q865','JPN':'Q17','ITA':'Q38','GBR':'Q145'}
for key,q in special.items():qid_codes.setdefault(q,[]).append(key)
entities={}
for result in parallel(entity,list(qid_codes)):
    if result:entities[result['id']]=result
print('Country entities',len(entities),flush=True)
countries={}; persons={}; statements=[]
for q,e in entities.items():
    for key in set(qid_codes[q]):countries[key]={'qid':q,'name':label(e),'flags':[],'leaders':[]}
    for prop,role in [('P6','Jefatura del Gobierno'),('P35','Jefatura del Estado')]:
        for s in e.get('claims',{}).get(prop,[]):
            if s.get('rank')=='deprecated' or 'datavalue' not in s['mainsnak']:continue
            v=s['mainsnak']['datavalue']['value']
            if not isinstance(v,dict) or 'id' not in v:continue
            start=qualifier(s,'P580');end=qualifier(s,'P582')
            # An undated incumbent is valid only at the retrieval date.
            statements.append(dict(keys=list(set(qid_codes[q])),person=v['id'],role=role,start=start[0] if start else TODAY,end=end[0] if end else TODAY,precision=start[1] if start else 11,source='https://www.wikidata.org/wiki/'+q,sourceStatement=s.get('id',''),current=not end))

# Fetch complete office-holder histories for focal offices. P39 start/end qualifiers
# are linked to each individual, not inferred from a four-year election cycle.
office_map={
 'Q11696':('USA','Presidente de los Estados Unidos'),
 'Q844587':('ESP','Presidente del Gobierno'),
 'Q4970706':('DEU','Canciller federal'),
 'Q14211':('GBR','Primer ministro'),
 'Q191954':('FRA','Presidente de la República'),
 'Q1587677':('FRA','Primer ministro'),
 'Q274948':('JPN','Primer ministro'),
 'Q208233':('JPN','Emperador'),
 'Q192711':('IND','Primer ministro'),
 'Q796897':('ITA','Presidente del Consejo de Ministros'),
 'Q218295':('RUS','Presidente'),
 'Q655407':('CHN','Presidente de la República Popular China'),
}
for office,(key,role) in office_map.items():
    query=f'SELECT ?person ?start ?end WHERE {{ ?person p:P39 ?s; wdt:P31 wd:Q5. ?s ps:P39 wd:{office}; pq:P580 ?start. OPTIONAL {{?s pq:P582 ?end}} }}'
    url='https://query.wikidata.org/sparql?'+urllib.parse.urlencode({'query':query,'format':'json'})
    result=safe(lambda _:get(url,'office-'+office),office)
    if not result:continue
    for row in result['results']['bindings']:
        start=row['start']['value'][:10];end=row.get('end',{}).get('value',TODAY)[:10]
        if end<'1789-01-01' or start>TODAY or end<start:continue
        statements.append(dict(keys=[key],person=row['person']['value'].rsplit('/',1)[-1],role=role,start=start,end=end,precision=11,source='https://www.wikidata.org/wiki/'+office,current='end' not in row))
    print('Office',office,len(result['results']['bindings']),flush=True)

# Focal political authorities, including de facto leadership. Titles remain
# distinct: a party leader is never silently relabelled president.
focal=[]
def term(key,person,name,role,start,end,source,note=''):
    if source.startswith('https://www.wikidata.org/wiki/'):source='https://www.wikidata.org/wiki/'+person
    focal.append(dict(keys=[key],person=person,name=name,role=role,start=start,end=min(end,TODAY),precision=11,source=source,note=note,curated=True))
moncloa='https://www.lamoncloa.gob.es/presidente/presidentes/Paginas/index.aspx'
paress='https://pares.cultura.gob.es/ParesBusquedas20/catalogo/description/12967950'
german='https://www.bundeskanzler.de/bk-en/federal-chancellery/federal-chancellors-since-1949'
terms=[
 ('ESP','Q365172','Carlos Arias Navarro','Presidente del Gobierno','1973-12-31','1976-07-01',paress),
 ('ESP','Q547426','Fernando de Santiago','Presidente del Gobierno en funciones','1976-07-02','1976-07-05','https://www.boe.es/buscar/doc.php?id=BOE-A-1976-13037'),
 ('ESP','Q214367','Adolfo Suárez','Presidente del Gobierno','1976-07-05','1981-02-26',moncloa),
 ('ESP','Q273129','Leopoldo Calvo-Sotelo','Presidente del Gobierno','1981-02-26','1982-12-02',moncloa),
 ('ESP','Q156799','Felipe González','Presidente del Gobierno','1982-12-02','1996-05-05',moncloa),
 ('ESP','Q55637','José María Aznar','Presidente del Gobierno','1996-05-05','2004-04-17',moncloa),
 ('ESP','Q41395','José Luis Rodríguez Zapatero','Presidente del Gobierno','2004-04-17','2011-12-21',moncloa),
 ('ESP','Q10819','Mariano Rajoy','Presidente del Gobierno','2011-12-21','2018-06-02',moncloa),
 ('ESP','Q6070218','Pedro Sánchez','Presidente del Gobierno','2018-06-02',TODAY,moncloa),
 ('ESP','Q29179','Francisco Franco','Jefe del Estado · dictadura','1939-04-01','1975-11-20',paress),
 ('ESP-REPUBLIC','Q203708','Manuel Azaña','Presidente de la República','1936-05-11','1939-02-27','https://www.congreso.es/es/cem/recconst'),
 ('ESP-REPUBLIC','Q312040','Francisco Largo Caballero','Presidente del Consejo de Ministros','1936-09-04','1937-05-17','https://pares.cultura.gob.es/'),
 ('ESP-REPUBLIC','Q312757','Juan Negrín','Presidente del Consejo de Ministros','1937-05-17','1939-03-31','https://pares.cultura.gob.es/'),
 ('ESP-NATIONALIST','Q29179','Francisco Franco','Jefe del Estado del bando sublevado','1936-10-01','1939-04-01',paress),
 ('DEU','Q352','Adolf Hitler','Dictador · Führer y canciller','1934-08-02','1945-04-30','https://encyclopedia.ushmm.org/content/en/article/adolf-hitler-1933-1939'),
 ('DEU','Q352','Adolf Hitler','Canciller del Reich','1933-01-30','1934-08-02','https://encyclopedia.ushmm.org/content/en/article/adolf-hitler-1933-1939'),
 ('DEU','Q2677','Guillermo II','Emperador alemán','1888-06-15','1918-11-09','https://www.dhm.de/lemo/biografie/wilhelm-ii'),
 ('DEU','Q150652','Guillermo I','Emperador alemán','1871-01-18','1888-03-09','https://www.dhm.de/lemo/biografie/wilhelm-i'),
 ('DEU','Q58600','Federico III','Emperador alemán','1888-03-09','1888-06-15','https://www.dhm.de/lemo/biografie/friedrich-iii'),
 ('DEU','Q2646','Friedrich Ebert','Presidente del Reich','1919-02-11','1925-02-28','https://www.dhm.de/lemo/biografie/friedrich-ebert'),
 ('DEU','Q2667','Paul von Hindenburg','Presidente del Reich','1925-05-12','1934-08-02','https://www.dhm.de/lemo/biografie/paul-von-hindenburg'),
 ('DDR','Q2628','Walter Ulbricht','Dirigente del SED','1950-07-25','1971-05-03','https://www.hdg.de/lemo/biografie/walter-ulbricht.html'),
 ('DDR','Q2607','Erich Honecker','Dirigente del SED','1971-05-03','1989-10-18','https://www.hdg.de/lemo/biografie/erich-honecker.html'),
 ('DDR','Q2602','Egon Krenz','Secretario general del SED','1989-10-18','1989-12-03','https://www.hdg.de/lemo/biografie/egon-krenz.html'),
 ('DDR','Q57241','Hans Modrow','Presidente del Consejo de Ministros','1989-11-13','1990-04-12','https://www.hdg.de/lemo/biografie/hans-modrow.html'),
 ('DDR','Q57412','Lothar de Maizière','Presidente del Consejo de Ministros','1990-04-12','1990-10-02','https://www.hdg.de/lemo/biografie/lothar-de-maiziere.html'),
 ('USSR','Q1394','Vladímir Lenin','Presidente del Consejo de Comisarios del Pueblo','1922-12-30','1924-01-21','https://www.wikidata.org/wiki/Q1394'),
 ('USSR','Q855','Iósif Stalin','Secretario general del Partido Comunista','1922-04-03','1952-10-16','https://www.wikidata.org/wiki/Q855'),
 ('USSR','Q855','Iósif Stalin','Secretario del Comité Central','1952-10-16','1953-03-05','https://www.wikidata.org/wiki/Q855'),
 ('USSR','Q35314','Nikita Jrushchov','Primer secretario del Partido Comunista','1953-09-14','1964-10-14','https://www.wikidata.org/wiki/Q35314'),
 ('USSR','Q765165','Leonid Brézhnev','Dirigente del Partido Comunista','1964-10-14','1982-11-10','https://www.wikidata.org/wiki/Q765165'),
 ('USSR','Q44071','Yuri Andrópov','Secretario general del Partido Comunista','1982-11-12','1984-02-09','https://www.wikidata.org/wiki/Q1273'),
 ('USSR','Q127442','Konstantín Chernenko','Secretario general del Partido Comunista','1984-02-13','1985-03-10','https://www.wikidata.org/wiki/Q1275'),
 ('USSR','Q30487','Mijaíl Gorbachov','Secretario general del Partido Comunista','1985-03-11','1991-08-24','https://www.wikidata.org/wiki/Q30487'),
 ('USSR','Q30487','Mijaíl Gorbachov','Presidente de la URSS','1990-03-15','1991-12-25','https://www.wikidata.org/wiki/Q30487'),
 ('FRA','Q7732','Luis XVI','Rey de Francia','1774-05-10','1792-09-21','https://www.elysee.fr/la-presidence/louis-xvi'),
 ('FRA','Q517','Napoleón Bonaparte','Primer cónsul','1799-11-10','1804-05-18','https://www.napoleon.org/histoire-des-2-empires/biographies/napoleon-bonaparte/'),
 ('FRA','Q517','Napoleón I','Emperador de los franceses','1804-05-18','1814-04-06','https://www.napoleon.org/histoire-des-2-empires/biographies/napoleon-bonaparte/'),
 ('FRA','Q517','Napoleón I','Emperador · Cien Días','1815-03-20','1815-06-22','https://www.napoleon.org/histoire-des-2-empires/biographies/napoleon-bonaparte/'),
 ('FRA','Q7750','Luis XVIII','Rey de Francia','1814-04-06','1815-03-20','https://www.wikidata.org/wiki/Q7759'),
 ('FRA','Q7750','Luis XVIII','Rey de Francia','1815-07-08','1824-09-16','https://www.wikidata.org/wiki/Q7759'),
 ('FRA','Q7758','Carlos X','Rey de Francia','1824-09-16','1830-08-02','https://www.wikidata.org/wiki/Q7762'),
 ('FRA','Q7771','Luis Felipe I','Rey de los franceses','1830-08-09','1848-02-24','https://www.wikidata.org/wiki/Q7771'),
 ('FRA','Q7721','Napoleón III','Emperador de los franceses','1852-12-02','1870-09-04','https://www.napoleon.org/histoire-des-2-empires/biographies/napoleon-iii/'),
 ('CHN','Q16574','Chiang Kai-shek','Presidente del Gobierno nacional · República de China','1928-10-10','1931-12-15','https://www.wikidata.org/wiki/Q17427'),
 ('CHN','Q16574','Chiang Kai-shek','Presidente de la Comisión de Asuntos Militares','1931-12-15','1943-08-01','https://www.wikidata.org/wiki/Q17427'),
 ('CHN','Q16574','Chiang Kai-shek','Presidente del Gobierno nacional','1943-08-01','1948-05-20','https://www.wikidata.org/wiki/Q17427'),
 ('CHN','Q16574','Chiang Kai-shek','Presidente de la República de China','1948-05-20','1949-01-21','https://www.wikidata.org/wiki/Q17427'),
 ('CHN','Q5816','Mao Zedong','Dirigente del Partido Comunista de China','1949-10-01','1976-09-09','https://www.wikidata.org/wiki/Q5816'),
 ('ITA','Q23559','Benito Mussolini','Jefe del Gobierno · dictadura fascista','1922-10-31','1943-07-25','https://www.wikidata.org/wiki/Q23559'),
 ('JPN','Q160847','Hideki Tōjō','Primer ministro','1941-10-18','1944-07-22','https://japan.kantei.go.jp/rekidainaikaku/index_e.html'),
 ('JPN','Q34479','Hirohito','Emperador Shōwa','1926-12-25','1989-01-07','https://www.kunaicho.go.jp/e-about/history/history01.html'),
 ('FRA-VICHY','Q5721','Philippe Pétain','Jefe del Estado francés · régimen de Vichy','1940-07-11','1944-08-20','https://encyclopedia.ushmm.org/content/en/article/france'),
 ('FRA-FREE','Q2042','Charles de Gaulle','Dirigente de la Francia Libre','1940-06-18','1944-08-25','https://www.charles-de-gaulle.org/lhomme/biographie/'),
 ('FRA-FREE','Q2042','Charles de Gaulle','Presidente del Gobierno Provisional','1944-08-25','1946-01-20','https://www.charles-de-gaulle.org/lhomme/biographie/'),
 ('FRA','Q5721','Philippe Pétain','Jefe del Estado francés · régimen de Vichy','1940-07-11','1944-08-20','https://encyclopedia.ushmm.org/content/en/article/france'),
 ('FRA','Q2042','Charles de Gaulle','Dirigente de la Francia Libre · autoridad rival','1940-06-18','1944-08-25','https://www.charles-de-gaulle.org/lhomme/biographie/'),
 ('FRA','Q2042','Charles de Gaulle','Presidente del Gobierno Provisional','1944-08-25','1946-01-20','https://www.charles-de-gaulle.org/lhomme/biographie/'),
 ('CROATIA-CLIENT','Q36965','Ante Pavelić','Poglavnik · Estado cliente del Eje','1941-04-10','1945-05-08','https://encyclopedia.ushmm.org/content/en/article/croatia'),
 ('CHN-COMMUNIST','Q5816','Mao Zedong','Dirigente del Partido Comunista de China','1935-01-15','1976-09-09','https://www.wikidata.org/wiki/Q5816'),
 ('FRA','Q219825','Convención Nacional','Autoridad republicana colectiva','1792-09-21','1795-11-02','https://www.assemblee-nationale.fr/histoire/7ed.asp'),
 ('FRA','Q219817','Directorio','Poder ejecutivo colegiado','1795-11-02','1799-11-10','https://www.assemblee-nationale.fr/histoire/7ed.asp'),
]
for args in terms:term(*args)
statements.extend(focal)

# Fetch labels and portrait filenames in parallel; all runtime content is local.
# Reuse already acquired labels when adding a few focal statements.
for path in CACHE.glob('people-*.json'):
    for row in json.loads(path.read_text(encoding='utf8'))['results']['bindings']:
        q=row['person']['value'].rsplit('/',1)[-1]
        image=urllib.parse.unquote(row['image']['value'].rsplit('/',1)[-1]) if 'image' in row else None
        persons.setdefault(q,dict(name=row.get('personLabel',{}).get('value',q),image=image,qid=q))
person_ids=sorted({s['person'] for s in statements}-set(persons))
for offset in range(0,len(person_ids),80):
    ids=person_ids[offset:offset+80]
    query='SELECT ?person ?personLabel ?image WHERE { VALUES ?person {'+' '.join('wd:'+q for q in ids)+'} OPTIONAL {?person wdt:P18 ?image} SERVICE wikibase:label {bd:serviceParam wikibase:language "es,en"}}'
    url='https://query.wikidata.org/sparql?'+urllib.parse.urlencode({'query':query,'format':'json'})
    result=get(url,'people-'+hashlib.sha256(query.encode()).hexdigest()[:16])
    for row in result['results']['bindings']:
        q=row['person']['value'].rsplit('/',1)[-1]
        if q in persons:continue
        image=urllib.parse.unquote(row['image']['value'].rsplit('/',1)[-1]) if 'image' in row else None
        persons[q]=dict(name=row.get('personLabel',{}).get('value',q),image=image,qid=q)
print('People',len(persons),flush=True)

media={}
def prewarm_commons(filenames):
    files=sorted(set(filenames))
    for offset in range(0,len(files),40):
        group=files[offset:offset+40]
        params={'action':'query','titles':'|'.join('File:'+f for f in group),'redirects':1,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':320,'format':'json'}
        url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)
        digest=hashlib.sha256('|'.join(group).encode()).hexdigest()[:16]
        info=get(url,'commons-batch-'+digest)
        pages={p.get('title',''):p for p in info.get('query',{}).get('pages',{}).values()}
        normalized={p['from']:p['to'] for p in info.get('query',{}).get('normalized',[])}
        redirects={p['from']:p['to'] for p in info.get('query',{}).get('redirects',[])}
        for filename in group:
            title=normalized.get('File:'+filename,'File:'+filename)
            title=redirects.get(title,title)
            if title in pages:
                key=hashlib.sha256(filename.encode()).hexdigest()[:20]
                save(CACHE/('commons-'+key+'.json'),{'query':{'pages':{'0':pages[title]}}})
        time.sleep(.6)
def commons(filename,kind):
    key=hashlib.sha256(filename.encode()).hexdigest()[:20]
    params={'action':'query','titles':'File:'+filename,'redirects':1,'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':320,'format':'json'}
    info=get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'commons-'+key)
    page=next(iter(info.get('query',{}).get('pages',{}).values()),{})
    ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{})
    license=meta.get('LicenseShortName',{}).get('value','')
    if not any(s in license.lower() for s in ['public domain','cc0','cc by','cc-by','pd-']):return None
    url=ii.get('url') if kind=='flag' and filename.lower().endswith('.svg') else ii.get('thumburl') or ii.get('url')
    if url:url=url.split('?')[0] # Canonical asset URL; omit tracking parameters.
    if not url:return None
    ext='.svg' if kind=='flag' and filename.lower().endswith('.svg') else ('.png' if '.png' in url.lower() else '.jpg')
    relative=f'media/{kind}-{key}{ext}';path=OUT/relative
    if not path.exists():
        for attempt in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url+('?download=1' if kind=='flag' else ''),headers=UA),timeout=45) as r:raw=r.read()
                if len(raw)>5_000_000:return None
                if ext=='.svg' and (b'<script' in raw.lower() or b'javascript:' in raw.lower()):return None
                path.write_bytes(raw);break
            except urllib.error.HTTPError as error:
                if error.code==429:
                    print('Media rate limit',filename,flush=True);return None
                if attempt==2:
                    print('Media unavailable',filename,str(error)[:90],flush=True);return None
                time.sleep(attempt+1)
            except Exception as error:
                if attempt==2:
                    print('Media unavailable',filename,str(error)[:90],flush=True);return None
                time.sleep(attempt+1)
        time.sleep(.5)
    clean=lambda v:html.unescape(re.sub('<[^>]*>','',v))
    return dict(file=relative,title=filename,url=ii['descriptionurl'],artist=clean(meta.get('Artist',{}).get('value','')),license=license,attribution=clean(meta.get('Attribution',{}).get('value','')),attributionRequired=meta.get('AttributionRequired',{}).get('value')=='true',licenseUrl=meta.get('LicenseUrl',{}).get('value',''),credit=clean(meta.get('Credit',{}).get('value','')),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,sourceUrl=url)

# Portraits are best-effort. Missing/unclear licenses never become placeholders.
portrait_ids={s['person'] for s in focal}|{s['person'] for s in statements if 'USA' in s['keys']}
# Cap images to focal series and current governments; names retain full data coverage.
portrait_candidates=[(q,p['image']) for q,p in persons.items() if q in portrait_ids and p.get('image')]
portrait_candidates=[(q,file) for q,file in portrait_candidates if q not in {'Q219825','Q219817'}]
priority={s['person'] for s in focal}|{s['person'] for s in statements if 'USA' in s['keys'] and s['start']>='1900-01-01'}
portrait_candidates.sort(key=lambda item:(item[0] not in priority,item[0]))
portrait_candidates=portrait_candidates[:80]
prewarm_commons([file for _,file in portrait_candidates])
def portrait(arg):
    q,file=arg; m=commons(file,'portrait');return(q,m)
for result in parallel(portrait,portrait_candidates,workers=2):
    if result and result[1]:media[result[0]]=result[1]
print('Portraits',len(media),flush=True)

for s in statements:
    person=persons.get(s['person'])
    if not person or s['end']<s['start']:continue
    record={k:v for k,v in s.items() if k not in ['keys','current']}
    record['name']=s.get('name',person['name'])
    if s['person'] in media:record['portrait']=media[s['person']]
    for key in s['keys']:
        countries.setdefault(key,{'qid':'','name':key,'flags':[],'leaders':[]})['leaders'].append(record)

# File names and ranges for core regimes. Flag geometry comes from the original
# Commons SVG, never a censored/stylised substitute.
flag_ranges={
 'DEU':[
 ('1871-01-18','1918-11-09','Flag of the German Empire.svg'),
 ('1919-08-14','1933-03-12','Flag of Germany (3-2 aspect ratio).svg'),
 ('1933-03-13','1935-09-14','Flag of the German Empire.svg'),
 ('1935-09-15','1945-05-08','Flag of Germany (1935–1945).svg'),
 ('1949-05-23',TODAY,'Flag of Germany.svg')],
 'DDR':[('1949-10-07','1959-09-30','Flag of Germany.svg'),('1959-10-01','1990-10-02','Flag of East Germany.svg')],
 'USSR':[('1923-11-12','1955-08-18','Flag of the Soviet Union (1924–1955).svg'),('1955-08-19','1991-12-25','Flag of the Soviet Union.svg')],
 'RUS':[('1991-12-26',TODAY,'Flag of Russia.svg')],
 'ESP-REPUBLIC':[('1931-04-14','1939-04-01','Flag of Spain (1931–1939).svg')],
 'ESP-NATIONALIST':[('1936-08-29','1938-02-01','Flag of Spain (1785–1873, 1875–1931).svg'),('1938-02-02','1939-04-01','Flag of Spain (1938–1945).svg')],
 'ESP':[('1785-05-28','1873-02-11','Flag of Spain (1785–1873, 1875–1931).svg'),('1873-02-12','1874-12-28','Flag of the First Spanish Republic.svg'),('1874-12-29','1931-04-13','Flag of Spain (1785–1873, 1875–1931).svg'),('1931-04-14','1939-03-31','Flag of Spain (1931–1939).svg'),('1939-04-01','1945-10-10','Flag of Spain (1938–1945).svg'),('1945-10-11','1977-01-20','Flag of Spain (1945–1977).svg'),('1977-01-21','1981-10-04','Flag of Spain (1977–1981).svg'),('1981-10-05',TODAY,'Flag of Spain.svg')],
 'FRA':[('1774-05-10','1790-12-31','Royal Standard of the King of France.svg'),('1794-02-15','1814-04-05','Flag of France (1794–1815, 1830–1974).svg'),('1814-04-06','1815-03-19','Flag of the Kingdom of France (1814-1830).svg'),('1815-03-20','1815-07-07','Flag of France (1794–1815, 1830–1974).svg'),('1815-07-08','1830-08-08','Flag of the Kingdom of France (1814-1830).svg'),('1830-08-09','1974-12-31','Flag of France (1794–1815, 1830–1974).svg'),('1975-01-01',TODAY,'Flag of France.svg')],
 'CHN':[('1928-10-10','1949-09-30','Flag of the Republic of China.svg'),('1949-10-01',TODAY,'Flag of the People\'s Republic of China.svg')],
 'TWN':[('1928-10-10',TODAY,'Flag of the Republic of China.svg')],
 'JPN':[('1870-02-27',TODAY,'Flag of Japan.svg')],
 'GBR':[('1801-01-01',TODAY,'Flag of the United Kingdom.svg')],
 'ITA':[('1861-03-17','1946-06-17','Flag of Italy (1861–1946).svg'),('1946-06-18',TODAY,'Flag of Italy.svg')],
 'ROC':[('1928-10-10','1949-12-31','Flag of the Republic of China.svg')],
 'CROATIA-CLIENT':[('1941-04-10','1945-05-08','Flag of Independent State of Croatia.svg')],
 'FRA-VICHY':[('1940-07-11','1944-08-20','Flag of France (1794–1815, 1830–1974).svg')],
 'FRA-FREE':[('1940-07-03','1944-08-25','Flag of Free France (1940–1944).svg'),('1944-08-25','1946-01-20','Flag of France (1794–1815, 1830–1974).svg')],
}
# US star counts are historically meaningful; use the documented national flag
# for each admission era, rather than carrying today's fifty stars to 1789.
us=[('1777-06-14',13),('1795-05-01',15),('1818-07-04',20),('1819-07-04',21),('1820-07-04',23),('1822-07-04',24),('1836-07-04',25),('1837-07-04',26),('1845-07-04',27),('1846-07-04',28),('1847-07-04',29),('1848-07-04',30),('1851-07-04',31),('1858-07-04',32),('1859-07-04',33),('1861-07-04',34),('1863-07-04',35),('1865-07-04',36),('1867-07-04',37),('1877-07-04',38),('1890-07-04',43),('1891-07-04',44),('1896-07-04',45),('1908-07-04',46),('1912-07-04',48),('1959-07-04',49),('1960-07-04',50)]
flag_ranges['USA']=[]
for i,(start,stars) in enumerate(us):
    end=(datetime.date.fromisoformat(us[i+1][0])-datetime.timedelta(days=1)).isoformat() if i+1<len(us) else TODAY
    filename='Flag of the United States.svg' if stars==50 else f'Flag of the United States ({start[:4]}-{us[i+1][0][:4]}).svg'
    flag_ranges['USA'].append((start,end,filename))

flag_files={filename for ranges in flag_ranges.values() for _,_,filename in ranges}
# Current flags for all remaining documented country entities. Undated claims
# remain at retrieval date; source-qualified dates retain their own precision.
focal_flags=set(flag_ranges)
for q,e in entities.items():
    for s in e.get('claims',{}).get('P41',[]):
        if s.get('rank')=='deprecated' or 'datavalue' not in s['mainsnak']:continue
        filename=s['mainsnak']['datavalue']['value'];start=qualifier(s,'P580');end=qualifier(s,'P582')
        key_hash=hashlib.sha256(filename.encode()).hexdigest()[:20]
        # Retain cached historical symbols; prioritize current symbols for broad
        # coverage instead of downloading every historical variant in one run.
        if end and end[0]<TODAY and not (MEDIA/('flag-'+key_hash+'.svg')).exists():continue
        for key in set(qid_codes[q]):
            if key not in focal_flags:
                flag_ranges.setdefault(key,[]).append((start[0] if start else TODAY,end[0] if end else TODAY,filename));flag_files.add(filename)
def flag(file):return(file,commons(file,'flag'))
flag_media={}
prewarm_commons(flag_files)
core_files={filename for key,ranges in flag_ranges.items() if key in focal_flags for _,_,filename in ranges}
ordered_flags=sorted(flag_files,key=lambda file:(file not in core_files,file))
for result in parallel(flag,ordered_flags,workers=1):
    if result and result[1]:flag_media[result[0]]=result[1]
for key,ranges in flag_ranges.items():
    for start,end,filename in ranges:
        if filename in flag_media and start<=end:
            countries.setdefault(key,{'qid':'','name':key,'flags':[],'leaders':[]})['flags'].append(dict(start=start,end=min(end,TODAY),media=flag_media[filename],source='https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(filename.replace(' ','_'))))

# Never identify the pre-1949 occupation administrations as the FRG/GDR.
for key in ['DEU','DDR']:
    countries[key]['notes']=[dict(start='1945-05-09',end='1949-05-22' if key=='DEU' else '1949-10-06',text='Administración militar aliada. No existía todavía este Estado alemán ni una bandera nacional oficial. Las zonas occidentales estaban administradas por Estados Unidos, Reino Unido y Francia; la zona oriental, por la Unión Soviética.',source='https://history.state.gov/milestones/1945-1952/germany')]
    countries[key]['leaders']=[s for s in countries[key]['leaders'] if not ('1945-05-09'<=s['start']<'1949-05-23')]
countries['ESP-REPUBLIC']['name']='España · zona republicana'
countries['ESP-NATIONALIST']['name']='España · bando sublevado'
countries.setdefault('ROC',{'qid':'Q865','name':'República de China','flags':[],'leaders':[]})['leaders']=[s for s in countries['CHN']['leaders'] if s['start']<'1949-10-01' and s['person']=='Q16574']

# Preserve names where the label service lacks a label, without substituting
# portraits from a namesake. Collective authorities have no portrait.
for s in focal:
    for key in s['keys']:
        if not any(l['person']==s['person'] and l['start']==s['start'] for l in countries[key]['leaders']):
            countries[key]['leaders'].append({k:v for k,v in s.items() if k not in ['keys']})

for key,c in countries.items():
    unique={}
    for s in c['leaders']:
        # Curated records take precedence over repeated equivalent source terms.
        signature=(s['person'],s['role'],s['start'],s['end']);unique[signature]=s
    c['leaders']=sorted(unique.values(),key=lambda x:(x['start'],x['name']))
payload=dict(retrieved=TODAY,license='CC0-1.0 (Wikidata metadata); each image retains its own license',source='https://www.wikidata.org/',format='dated-political-identities',reference='31 December of past years; retrieval date for the current or future year; no extrapolation beyond retrieval',countries=countries)
save(OUT/'data/identities.json',payload)
used={m['file']:m for m in [*media.values(),*flag_media.values()]}
save(MEDIA/'manifest.json',dict(retrieved=TODAY,entries=list(used.values())))
for path in MEDIA.glob('*'):
    if path.is_file() and path.name.startswith(('portrait-','flag-')) and 'media/'+path.name not in used:path.unlink()
print('Identities',len(countries),'leaders',sum(len(c['leaders']) for c in countries.values()),'flags',len(flag_media),'portraits',len(media),flush=True)
