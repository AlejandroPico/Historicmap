"""Incremental dated authorities, 1970–1989 expansion; preserves the 1990–acquisition catalogue. Preparation only, no runtime API.

Country P35/P6 assertions and office P1906/P1313 → individual P39 terms are
kept distinct from sovereignty and territorial control. Missing resignation dates
are never silently promoted to incumbency. Existing curated records and licensed
media (including the unchanged Mozambique full-frame photograph) are preserved.
"""
import argparse, concurrent.futures, datetime, hashlib, html, json, pathlib, re, time, threading
import urllib.request, urllib.parse

ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'public'; CACHE=ROOT/'.cache/identities'
TODAY=datetime.date.today().isoformat(); START='1970-01-01'; PERIOD_END='1989-12-31'; ACQUISITION='historical-0.8'
UA={'User-Agent':'Historicmap/0.8 (https://github.com/AlejandroPico/Historicmap; educational atlas)'}
EXCLUDED_MEDIA={(r['person'],r['title']) for r in json.loads(pathlib.Path(__file__).with_name('media-exclusions.json').read_text(encoding='utf8'))}
DOWNLOAD_LOCK=threading.Lock();LAST_DOWNLOAD=0
def download(url):
    """Pace shared thumbnail acquisition and respect service back pressure."""
    global LAST_DOWNLOAD
    for attempt in range(3):
        with DOWNLOAD_LOCK:
            time.sleep(max(0,1.2-(time.monotonic()-LAST_DOWNLOAD)));LAST_DOWNLOAD=time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60) as response:return response.read()
        except urllib.error.HTTPError as error:
            if error.code!=429 or attempt==2:raise
            retry=error.headers.get('Retry-After','60');time.sleep(min(120,int(retry) if retry.isdigit() else 60))
LIFETIMES={'YUG':('1945-11-29','1992-04-26'),'FRY':('1992-04-27','2003-02-03'),'SCG':('2003-02-04','2006-06-05'),'CSK':('1918-10-28','1992-12-31'),'YAR':('1962-09-26','1990-05-21'),'YPR':('1967-11-30','1990-05-21'),'DDR':('1949-10-07','1990-10-02'),'USSR':('1922-12-30','1991-12-26'),'VDR':('1945-09-02','1976-07-01'),'RVN':('1955-10-26','1975-04-30'),'VSR':('1969-06-08','1976-07-01'),'RHO':('1965-11-11','1980-04-17')}
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
def get(url,key):
    path=CACHE/(key+'.json')
    if path.exists():return json.loads(path.read_text(encoding='utf8'))
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=90) as response:data=json.load(response)
            save(path,data);return data
        except Exception:
            if attempt==3:raise
            time.sleep(2+attempt*3)
def entity(q):
    for key in [q,'person-current-'+q,'historical-entity-'+q]:
        path=CACHE/(key+'.json')
        if path.exists():return json.loads(path.read_text(encoding='utf8'))['entities'][q]
    return get('https://www.wikidata.org/wiki/Special:EntityData/'+q+'.json','historical-entity-'+q)['entities'][q]
def label(e):return next((e['labels'][lang]['value'] for lang in ['es','en','mul'] if lang in e.get('labels',{})),e['id'])
def values(e,p):return [s['mainsnak']['datavalue']['value'] for s in e.get('claims',{}).get(p,[]) if s.get('rank')!='deprecated' and 'datavalue' in s['mainsnak']]
def qual(s,p):
    v=s.get('qualifiers',{}).get(p,[{}])[0].get('datavalue',{}).get('value',{})
    return (v['time'].lstrip('+')[:10].replace('-00','-01'),v.get('precision',11)) if isinstance(v,dict) and 'time' in v else None
def query(q,key):return get('https://query.wikidata.org/sparql?'+urllib.parse.urlencode({'query':q,'format':'json'}),key)['results']['bindings']
def parallel(fn,items,workers=3):
    def safe(item):
        try:return item,fn(item)
        except Exception as error:print('Unavailable',str(item)[:80],str(error)[:100],flush=True);return item,None
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:return list(pool.map(safe,items))

def acquire(skip_media=False):
    data=json.loads((OUT/'data/identities.json').read_text(encoding='utf8')); countries=data['countries']
    for country in countries.values():
        for leader in country['leaders']:
            if leader.get('portrait') and (leader['person'],leader['portrait']['title']) in EXCLUDED_MEDIA:leader.pop('portrait')
    manifest=json.loads((OUT/'media/manifest.json').read_text(encoding='utf8')); media={m['file']:m for m in manifest['entries']}
    additions={'VDR':('Q172640','República Democrática de Vietnam'),'RVN':('Q180573','República de Vietnam'),'YUG':('Q83286','República Federativa Socialista de Yugoslavia'),'FRY':('Q838261','República Federal de Yugoslavia'),'SCG':('Q37024','Serbia y Montenegro'),'CSK':('Q33946','Checoslovaquia'),'YAR':('Q267584','República Árabe de Yemen'),'YPR':('Q199841','República Democrática Popular del Yemen'),'RASD':('Q40362','República Árabe Saharaui Democrática')}
    for key,(q,name) in additions.items():countries.setdefault(key,dict(qid=q,name=name,flags=[],leaders=[]))
    countries['YUG']['qid']='Q83286'
    for country in countries.values():country['leaders']=[l for l in country['leaders'] if l.get('acquisition') not in [ACQUISITION,'sahara-parties-0.8']]
    entities={q:e for q,e in parallel(entity,sorted({c['qid'] for c in countries.values() if re.fullmatch(r'Q\d+',c.get('qid',''))})) if e}
    office_map={}; current={}; unresolved=[]; fixes=[]; candidates=[]
    for key,country in countries.items():
        e=entities.get(country['qid'],{}); current[key]=set()
        for prop in ['P6','P35']:
            assertions=e.get('claims',{}).get(prop,[])
            latest=max((qual(s,'P580')[0] for s in assertions if s.get('rank')!='deprecated' and qual(s,'P580')),default='')
            preferred=any(s.get('rank')=='preferred' for s in assertions)
            for s in assertions:
                if s.get('rank')=='deprecated':continue
                person=s.get('mainsnak',{}).get('datavalue',{}).get('value',{}).get('id')
                start=qual(s,'P580');end=qual(s,'P582')
                if not person:continue
                if not end and (s.get('rank')=='preferred' or not preferred and start and start[0]==latest):current[key].add(person)
                effective_end=end or ((TODAY,11) if person in current[key] else None)
                if start and effective_end and effective_end[0]>=START and start[0]<=PERIOD_END:
                    candidates.append(dict(key=key,person=person,role='Jefatura del Gobierno' if prop=='P6' else 'Jefatura del Estado',start=start[0],end=min(effective_end[0],TODAY),precision=min(start[1],effective_end[1]),source='https://www.wikidata.org/wiki/'+country['qid'],sourceStatement=s.get('id',''),acquisition=ACQUISITION))
        for prop,role in [('P1906','Jefatura del Estado'),('P1313','Jefatura del Gobierno')]:
            for v in values(e,prop):
                if isinstance(v,dict) and v.get('id'):office_map.setdefault(v['id'],[]).append((key,role))
    # These dissolved entities do not expose their historical offices through
    # P1906/P1313. Explicit office identities are not aliases to successor states.
    for office,key,role in [('Q16761225','YUG','Presidencia colectiva · presidencia rotatoria'),('Q1419999','YUG','Jefatura del Gobierno'),('Q24944206','YUG','Jefatura del Gobierno'),('Q61039224','FRY','Jefatura del Estado'),('Q24944203','FRY','Jefatura del Estado'),('Q1419999','FRY','Jefatura del Gobierno'),('Q3921795','FRY','Jefatura del Gobierno'),('Q865728','YAR','Jefatura del Estado'),('Q137449192','YPR','Jefatura del Gobierno')]:office_map.setdefault(office,[]).append((key,role))
    offices=sorted(office_map); rows=[]
    for offset in range(0,len(offices),25):
        group=offices[offset:offset+25]; digest=hashlib.sha256('|'.join(group).encode()).hexdigest()[:16]
        q='SELECT ?office ?person ?statement ?start ?end ?precision WHERE { VALUES ?office { '+' '.join('wd:'+o for o in group)+' } ?person p:P39 ?statement. ?statement ps:P39 ?office; pq:P580 ?start; wikibase:rank ?rank. FILTER(?rank != wikibase:DeprecatedRank) OPTIONAL {?statement pq:P582 ?end} OPTIONAL {?statement pqv:P580/wikibase:timePrecision ?precision} FILTER(?start <= "'+TODAY+'T23:59:59Z"^^xsd:dateTime && (!BOUND(?end) || ?end >= "'+START+'T00:00:00Z"^^xsd:dateTime)) }'
        try:rows.extend(query(q,'historical-offices-'+START+'-'+digest))
        except Exception as error:unresolved.append(dict(offices=group,reason='Office query unavailable: '+str(error)))
        print('Office batch',offset+len(group),'/',len(offices),'terms',len(rows),flush=True)
    starts={}
    for row in rows:starts.setdefault(row['office']['value'].rsplit('/',1)[-1],set()).add(row['start']['value'][:10])
    for row in rows:
        office=row['office']['value'].rsplit('/',1)[-1]; person=row['person']['value'].rsplit('/',1)[-1]; start=row['start']['value'][:10]
        end=row.get('end',{}).get('value','')[:10]; upper=False
        for key,role in office_map[office]:
            actual_end=end
            if not actual_end:
                successors=[s for s in starts[office] if s>start]
                if successors:actual_end=(datetime.date.fromisoformat(min(successors))-datetime.timedelta(days=1)).isoformat();upper=True
                elif person in current[key] or any(l['person']==person and l.get('curated') and l['end']>=TODAY for l in countries[key]['leaders']):actual_end=TODAY
                else:unresolved.append(dict(country=key,person=person,office=office,start=start,reason='Undated end without documented current country assertion; not extended to acquisition.'));continue
            if actual_end<START or start>PERIOD_END or start>actual_end:continue
            term=dict(key=key,person=person,role=role,start=start,end=min(actual_end,TODAY),precision=int(row.get('precision',{}).get('value',11)),source='https://www.wikidata.org/wiki/'+person,sourceStatement=row['statement']['value'].rsplit('/',1)[-1],office=office,acquisition=ACQUISITION)
            if upper:term.update(endIsUpperBound=True,note='La fuente no fecha el cese. Se limita, como máximo, al inicio del siguiente titular documentado del mismo cargo; puede existir un intervalo sin documentar.')
            candidates.append(term)
    # Two federal Yugoslav prime ministers lack dated P39 statements. Their
    # appointments are documented by contemporary institutional publications;
    # the end remains an explicitly bounded interval, not an invented dismissal.
    for person,name,start,end,source in [('Q280605','Zoran Žižić','2000-11-04','2001-07-23','https://www.ohr.int/ohr_archive/ohr-rtrs-news-summary-5-november-2000-2/'),('Q3503970','Dragiša Pešić','2001-07-24','2003-02-03','https://www.ecoi.net/en/file/local/1235973/1329_1200477622_fry-assessment-october-2002.pdf')]:
        candidates.append(dict(key='FRY',person=person,name=name,role='Jefatura del Gobierno',start=start,end=end,precision=11,source=source,curated=True,endIsUpperBound=True,note='El inicio se contrasta en publicaciones institucionales contemporáneas. El cese es un límite superior por la sucesión o el final de esta entidad federal; no acredita un día exacto de dimisión.',acquisition='historical-0.8'))
    # Exact P39 resignations correct broad imported country statements. Do not
    # rewrite primary-source curations or genuine non-consecutive mandates.
    for key,country in countries.items():
        for old in country['leaders']:
            if old.get('curated') or old['end']<START or old['person'] in current[key]:continue
            matches=[t for t in candidates if t['key']==key and t['person']==old['person'] and t['start']==old['start'] and t['end']<old['end']]
            if matches:
                t=min(matches,key=lambda t:t['end']);fixes.append(dict(country=key,person=old['person'],fromEnd=old['end'],toEnd=t['end']));old['end']=t['end']
                if t.get('endIsUpperBound'):old['endIsUpperBound']=True;old['note']=t['note']
    targets={t['person'] for t in candidates}|{l['person'] for c in countries.values() for l in c['leaders'] if l['end']>=START and l['start']<=PERIOD_END}
    people={}; images={}
    for path in CACHE.glob('people-*.json'):
        for row in json.loads(path.read_text(encoding='utf8')).get('results',{}).get('bindings',[]):
            person=row['person']['value'].rsplit('/',1)[-1]
            if person not in targets:continue
            people[person]=row.get('personLabel',{}).get('value',person)
            if row.get('image'):images[person]=urllib.parse.unquote(row['image']['value'].rsplit('/',1)[-1])
    for person,e in parallel(entity,sorted(q for q in targets if people.get(q,q)==q or q not in images)):
        if e:
            people[person]=label(e); photos=values(e,'P18')
            if photos:images[person]=photos[0]
    # A retrieval-only, undated legacy assertion cannot place a deceased former
    # holder in the current year's authorities. Keep the actual historical terms.
    for key,country in countries.items():
        for old in list(country['leaders']):
            if old.get('curated') or old['start']!=TODAY or old['end']!=TODAY:continue
            try:death=[v['time'].lstrip('+')[:10].replace('-00','-01') for v in values(entity(old['person']),'P570') if isinstance(v,dict) and v.get('time')]
            except Exception:continue
            if death and max(death)<TODAY[:4]+'-01-01':country['leaders'].remove(old);fixes.append(dict(country=key,person=old['person'],reason='Removed undated retrieval-only legacy assertion after documented death before current year.'))
    for term in candidates:
        key=term.pop('key');term['name']=people.get(term['person'],term['person'])
        if key in LIFETIMES:
            lo,hi=LIFETIMES[key];term['start']=max(term['start'],lo);term['end']=min(term['end'],hi)
            if term['start']>term['end']:continue
        existing=countries[key]['leaders']
        if not any(l['person']==term['person'] and l['start']==term['start'] and l['end']==term['end'] and (l['role']==term['role'] or l.get('curated')) for l in existing):existing.append(term)
    portraits={l['person']:l['portrait'] for c in countries.values() for l in c['leaders'] if l.get('portrait')}
    # Persist acquired terms before network media work so an interruption cannot
    # discard successful history acquisition; subsequent runs are idempotent.
    data['historicalRetrieved']=TODAY;data['retrieved']=data.get('currentReferenceDate',data['retrieved']);save(OUT/'data/identities.json',data)
    if not skip_media:
        filenames=sorted({images[q] for q in targets if q in images and q not in portraits and not images[q].lower().endswith('.svg')})
        for offset in range(0,len(filenames),35):
            group=filenames[offset:offset+35];missing=[f for f in group if not (CACHE/('commons-'+hashlib.sha256(f.encode()).hexdigest()[:20]+'.json')).exists()]
            if not missing:continue
            params=dict(action='query',titles='|'.join('File:'+f for f in missing),redirects=1,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=320,format='json')
            try:info=get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'historical-commons-'+hashlib.sha256('|'.join(missing).encode()).hexdigest()[:16])
            except Exception as error:print('Commons batch unavailable',error,flush=True);continue
            pages={p.get('title',''):p for p in info.get('query',{}).get('pages',{}).values()};aliases={p['from']:p['to'] for section in ['normalized','redirects'] for p in info.get('query',{}).get(section,[])}
            for f in missing:
                title='File:'+f
                for _ in range(3):title=aliases.get(title,title)
                if title in pages:save(CACHE/('commons-'+hashlib.sha256(f.encode()).hexdigest()[:20]+'.json'),{'query':{'pages':{'0':pages[title]}}})
        def portrait(q):
            if (q,images[q]) in EXCLUDED_MEDIA:return None
            f=images[q];digest=hashlib.sha256(f.encode()).hexdigest()[:20];path=CACHE/('commons-'+digest+'.json')
            if not path.exists():return None
            info=json.loads(path.read_text(encoding='utf8'));page=next(iter(info.get('query',{}).get('pages',{}).values()),{});ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{});lic=meta.get('LicenseShortName',{}).get('value','')
            if not (any(s in lic.lower() for s in ['public domain','cc0','cc by','cc-by','pd-']) or lic in ['Attribution','OGL 3','OGL v1.0','OGL-om 1.0','GODL-India','European Parliament','KOGL Type 1','PDM-owner']):return None
            # ND originals require a separate full-frame acquisition contract.
            if 'nd' in lic.lower():return None
            url=(ii.get('thumburl') or ii.get('url') or '').split('?')[0]
            if not url or f.lower().endswith('.svg'):return None
            ext='.png' if '.png' in url.lower() else '.jpg';relative='media/portrait-'+digest+ext;dest=OUT/relative
            if relative in media and dest.exists():return media[relative]
            if not dest.exists():
                raw=download(url)
                if len(raw)>5_000_000 or not raw.startswith((b'\xff\xd8',b'\x89PNG')):return None
                dest.write_bytes(raw);time.sleep(.3)
            clean=lambda v:html.unescape(re.sub('<[^>]*>','',v))
            return dict(file=relative,title=f,url=ii.get('descriptionurl','https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(f)),artist=clean(meta.get('Artist',{}).get('value','')),license=lic,licenseUrl=meta.get('LicenseUrl',{}).get('value','') or ii.get('descriptionurl','')+'#Licensing',attribution=clean(meta.get('Attribution',{}).get('value','')),attributionRequired=lic=='Attribution' or meta.get('AttributionRequired',{}).get('value')=='true',credit=clean(meta.get('Credit',{}).get('value','')),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,sourceUrl=url)
        for q,result in parallel(portrait,sorted(q for q in targets if q in images and q not in portraits)):
            if result:portraits[q]=result;media[result['file']]=result
    # The territory's two parties are explicitly labelled. These are political
    # authorities, not a declaration of sovereignty or a control-boundary map.
    sah=countries['SAH'];sah['leaders']=[l for l in sah['leaders'] if l.get('acquisition')!='sahara-parties-0.8']
    for party,role,note in [('RASD','Autoridad saharaui / RASD','Autoridad de la RASD y del Frente POLISARIO; no equivale a una administración de todo el territorio.'),('MAR','Autoridad marroquí · zona bajo su control','Autoridad nacional de Marruecos, cuya administración controla parte del territorio. No se atribuye soberanía sobre el Sáhara Occidental.')]:
        for leader in countries[party]['leaders']:
            if leader['end']<('1976-02-27' if party=='RASD' else '1975-11-14'):continue
            term=dict(leader);term['start']=max(term['start'],'1976-02-27' if party=='RASD' else '1975-11-14');term['role']=role+' · '+leader['role'];term['note']=note;term['acquisition']='sahara-parties-0.8';sah['leaders'].append(term)
    sah['territoryStatus']=dict(start='1975-11-14',end=TODAY,text='El Sáhara Occidental figura en la lista de territorios no autónomos de la ONU desde 1963. Se distinguen las autoridades saharauis de la RASD/Frente POLISARIO y las autoridades de Marruecos para la zona bajo su control; listar estas autoridades no resuelve la soberanía ni representa una frontera de control diario.',source='https://www.un.org/dppa/decolonization/en/nsgt/western-sahara')
    if not skip_media:
        flag_names={'YUG':'Flag of SFR Yugoslavia.svg','FRY':'Flag of Serbia and Montenegro (1992–2006).svg','SCG':'Flag of Serbia and Montenegro (1992–2006).svg','CSK':'Flag of Czechoslovakia.svg','YAR':'Flag of North Yemen.svg','YPR':'Flag of South Yemen.svg','RASD':'Flag of the Sahrawi Arab Democratic Republic.svg'}
        for key,filename in flag_names.items():
            if countries[key]['flags']:continue
            try:
                digest=hashlib.sha256(filename.encode()).hexdigest()[:20];params=dict(action='query',titles='File:'+filename,redirects=1,prop='imageinfo',iiprop='url|extmetadata',format='json');info=get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'commons-'+digest);page=next(iter(info.get('query',{}).get('pages',{}).values()),{});ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{});lic=meta.get('LicenseShortName',{}).get('value','')
                if not any(v in lic.lower() for v in ['public domain','cc0','cc by','cc-by','pd-']):continue
                relative='media/flag-'+digest+'.svg';dest=OUT/relative;url=ii.get('url','')
                if not url:continue
                if not dest.exists():
                    with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60) as response:raw=response.read()
                    if b'<svg' not in raw or b'<script' in raw.lower() or b'javascript:' in raw.lower():continue
                    dest.write_bytes(raw)
                clean=lambda v:html.unescape(re.sub('<[^>]*>','',v));m=dict(file=relative,title=filename,url=ii.get('descriptionurl',''),artist=clean(meta.get('Artist',{}).get('value','')),license=lic,licenseUrl=meta.get('LicenseUrl',{}).get('value',''),attribution=clean(meta.get('Attribution',{}).get('value','')),attributionRequired=meta.get('AttributionRequired',{}).get('value')=='true',credit=clean(meta.get('Credit',{}).get('value','')),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,sourceUrl=url);media[relative]=m
                lo,hi=LIFETIMES.get(key,('1976-02-27',TODAY));countries[key]['flags'].append(dict(start=lo,end=min(hi,TODAY),media=m,source='https://www.wikidata.org/wiki/'+countries[key]['qid']))
            except Exception as error:print('Flag unavailable',key,str(error)[:100],flush=True)
    for c in countries.values():
        for l in c['leaders']:
            if l['person'] in portraits:l['portrait']=portraits[l['person']]
            if re.fullmatch(r'Q\d+',l['name']) and l['person'] in people:l['name']=people[l['person']]
        c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
    save(OUT/'data/identities.json',data);manifest['retrieved']=TODAY;manifest['entries']=sorted(media.values(),key=lambda m:m['file']);save(OUT/'media/manifest.json',manifest)
    annual=[]
    for year in range(int(START[:4]),int(PERIOD_END[:4])+1):
        first=f'{year}-01-01';last=min(f'{year}-12-31',TODAY);terms=[l for c in countries.values() for l in c['leaders'] if l['start']<=last and l['end']>=first];persons={l['person'] for l in terms};withphoto={l['person'] for l in terms if l.get('portrait')}
        annual.append(dict(year=year,countryKeys=sum(any(l['start']<=last and l['end']>=first for l in c['leaders']) for c in countries.values()),terms=len(terms),people=len(persons),peopleWithPortrait=len(withphoto)))
    unverified=[dict(country=key,person=l['person'],name=l['name'],start=l['start'],role=l['role']) for key,c in countries.items() for l in c['leaders'] if l['end']==TODAY and not l.get('curated') and l['person'] not in current.get(key,set()) and l.get('acquisition')!='sahara-parties-0.8']
    audit=dict(retrieved=TODAY,countryKeys=len(countries),terms=sum(len(c['leaders']) for c in countries.values()),people=len(targets),media=len(media),annual=annual,corrections=fixes,unresolvedOpenTerms=unresolved,unverifiedCurrentTerms=unverified,missingPortraits=[dict(person=q,name=people.get(q,q),hasP18=q in images) for q in sorted(targets) if q not in portraits],licenseCounts=dict(__import__('collections').Counter(m['license'] for m in media.values())))
    save(CACHE/('authorities-'+START[:4]+'-audit.json'),audit);print(json.dumps({k:v for k,v in audit.items() if k not in ['annual','unresolvedOpenTerms','missingPortraits','corrections']},ensure_ascii=False),flush=True)
    return audit

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--skip-media',action='store_true');args=parser.parse_args();acquire(args.skip_media)
