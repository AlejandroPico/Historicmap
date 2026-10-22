"""Incremental, repeatable acquisition of licensed portraits for annual authorities.

Preserves all existing identities/media. No synthetic pictures, namesake search,
unlicensed official-site images, or arbitrary country/portrait limit. Preparation
only: the application never contacts Wikidata or Commons at runtime.
"""
import concurrent.futures, datetime, hashlib, html, json, pathlib, re, time
import urllib.request, urllib.parse, urllib.error

ROOT=pathlib.Path(__file__).resolve().parents[1]
CACHE=ROOT/'.cache/identities'; OUT=ROOT/'public'; TODAY=datetime.date.today().isoformat()
YEAR=TODAY[:4]; START=YEAR+'-01-01'
UA={'User-Agent':'Historicmap/0.5 (https://github.com/AlejandroPico/Historicmap; educational atlas)'}
def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
def get(url,key):
    path=CACHE/(key+'.json')
    if path.exists():return json.loads(path.read_text(encoding='utf8'))
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=45) as response:data=json.load(response)
            save(path,data); return data
        except Exception:
            if attempt==4:raise
            time.sleep(min(30,2**attempt*2))
def entity(q):
    data=get('https://www.wikidata.org/wiki/Special:EntityData/'+q+'.json','person-current-'+q)
    return data['entities'][q]
def date_qualifier(s,key):
    v=s.get('qualifiers',{}).get(key,[{}])[0].get('datavalue',{}).get('value',{})
    if not isinstance(v,dict) or 'time' not in v:return None
    return v['time'].lstrip('+')[:10].replace('-00','-01'),v.get('precision',11)
def text_label(e):return e.get('labels',{}).get('es',e.get('labels',{}).get('en',e.get('labels',{}).get('mul',{'value':e['id']})))['value']
def parallel(fn,items,workers=3):
    def safe(item):
        try:return fn(item)
        except Exception as error:
            print('Unavailable',item,str(error)[:110],flush=True);return item,None
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:return list(pool.map(safe,items))

data=json.loads((OUT/'data/identities.json').read_text(encoding='utf8'))
manifest=json.loads((OUT/'media/manifest.json').read_text(encoding='utf8'))
media_by_file={m['file']:m for m in manifest['entries']}
countries=data['countries']; corrections=[]; unresolved=[]

# A normal-ranked, undated historical assertion alongside a preferred incumbent
# never establishes an incumbent at retrieval. For dated terms, use an exact
# P39 end from the person's item rather than infer resignation from a successor.
for key,country in countries.items():
    q=country.get('qid',''); path=CACHE/(q+'.json')
    if not q or not path.exists():continue
    e=json.loads(path.read_text(encoding='utf8'))['entities'][q]
    for prop in ['P6','P35']:
        statements=e.get('claims',{}).get(prop,[])
        if not any(s.get('rank')=='preferred' for s in statements):continue
        for s in statements:
            if s.get('rank')!='normal' or date_qualifier(s,'P582'):continue
            affected=[l for l in country['leaders'] if l.get('sourceStatement')==s.get('id') and l['end']>=START]
            for leader in affected:
                if not date_qualifier(s,'P580'):
                    country['leaders'].remove(leader)
                    corrections.append(dict(country=key,person=leader['person'],reason='Undated non-preferred statement is not evidence of an incumbent.'))
                    continue
                person=entity(leader['person']); ends=[]
                for office in person.get('claims',{}).get('P39',[]):
                    start=date_qualifier(office,'P580');end=date_qualifier(office,'P582')
                    if start and end and start[0]==leader['start'] and end[1]>=11:ends.append(end[0])
                if ends:
                    end=min(ends)
                    if end<leader['end']:
                        leader['end']=end;leader['source']='https://www.wikidata.org/wiki/'+leader['person']
                        corrections.append(dict(country=key,person=leader['person'],end=end,reason='Exact matching individual P39 term.'))
                else:unresolved.append(dict(country=key,person=leader['person'],start=leader['start'],reason='Open non-preferred term requires a primary-source end-date check.'))

# Explicit royal dates, checked against Casa de S. M. el Rey biographies. Keep
# existing records; only add a missing historically necessary term.
for q,name,start,end in [('Q19943','Juan Carlos I','1975-11-22','2014-06-18'),('Q191045','Felipe VI','2014-06-19',TODAY)]:
    if not any(l['person']==q and l['start']==start for l in countries['ESP']['leaders']):
        countries['ESP']['leaders'].append(dict(person=q,name=name,role='Rey de España · jefatura del Estado',start=start,end=end,precision=11,curated=True,source='https://www.casareal.es/ES/FamiliaReal/'+('rey/Paginas/rey_biografia.aspx' if q=='Q19943' else 'ReyFelipe/Paginas/biografia.aspx')))

# The president represents the collective Federal Council; it is not a separate
# executive presidency. The Council's collective identity remains in the data.
if not any(l['person']=='Q121160' and l['start']=='2026-01-01' for l in countries['CHE']['leaders']):
    countries['CHE']['leaders'].append(dict(person='Q121160',name='Guy Parmelin',role='Presidente de la Confederación · primero entre iguales',start='2026-01-01',end=min(TODAY,'2026-12-31'),precision=11,curated=True,source='https://www.wbf.admin.ch/en/guy-parmelin-president-of-the-swiss-confederation-2026',note='El Consejo Federal ejerce colegiadamente el Gobierno y la jefatura del Estado. La presidencia anual tiene funciones de representación.'))

targets={l['person'] for c in countries.values() for l in c['leaders'] if l['start']<=TODAY and l['end']>=START}
targets|={'Q191045','Q19943','Q29179'}
people={}
for path in CACHE.glob('people-*.json'):
    for row in json.loads(path.read_text(encoding='utf8')).get('results',{}).get('bindings',[]):
        q=row['person']['value'].rsplit('/',1)[-1]; image=urllib.parse.unquote(row['image']['value'].rsplit('/',1)[-1]) if 'image' in row else None
        if q not in people or image and not people[q].get('image'):
            people[q]=dict(name=row.get('personLabel',{}).get('value',q),image=image)
for q in sorted(targets):
    person=people.get(q,{})
    if not person.get('image') or person.get('name',q)==q:
        try:
            e=entity(q);images=[s['mainsnak']['datavalue']['value'] for s in e.get('claims',{}).get('P18',[]) if s.get('rank')!='deprecated' and 'datavalue' in s['mainsnak']]
            person['name']=text_label(e);person['image']=images[0] if images else None;people[q]=person
        except Exception as error:print('Person unavailable',q,str(error)[:80],flush=True)
print('Annual target people',len(targets),'with P18',sum(bool(people.get(q,{}).get('image')) for q in targets),flush=True)
overrides=ROOT/'scripts/current-portrait-overrides.json'
if overrides.exists():
    for q,filename in json.loads(overrides.read_text(encoding='utf8')).items():
        if q in targets:people.setdefault(q,dict(name=q))['image']=filename

files=sorted({people[q]['image'] for q in targets if people.get(q,{}).get('image')})
for offset in range(0,len(files),35):
    group=files[offset:offset+35]
    uncached=[f for f in group if not (CACHE/('commons-'+hashlib.sha256(f.encode()).hexdigest()[:20]+'.json')).exists()]
    if not uncached:continue
    params=dict(action='query',titles='|'.join('File:'+f for f in uncached),redirects=1,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=320,format='json')
    info=get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'commons-current-batch-'+hashlib.sha256('|'.join(uncached).encode()).hexdigest()[:16])
    pages={p.get('title',''):p for p in info.get('query',{}).get('pages',{}).values()}
    aliases={p['from']:p['to'] for section in ['normalized','redirects'] for p in info.get('query',{}).get(section,[])}
    for filename in uncached:
        title='File:'+filename
        for _ in range(3):title=aliases.get(title,title)
        if title in pages:save(CACHE/('commons-'+hashlib.sha256(filename.encode()).hexdigest()[:20]+'.json'),{'query':{'pages':{'0':pages[title]}}})
    time.sleep(.5)

def portrait(q):
    filename=people.get(q,{}).get('image')
    if not filename:return q,None
    digest=hashlib.sha256(filename.encode()).hexdigest()[:20]
    params=dict(action='query',titles='File:'+filename,redirects=1,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=320,format='json')
    info=get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'commons-'+digest)
    page=next(iter(info.get('query',{}).get('pages',{}).values()),{});ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{})
    license=meta.get('LicenseShortName',{}).get('value','')
    accepted=any(v in license.lower() for v in ['public domain','cc0','cc by','cc-by','pd-']) or license in ['Attribution','OGL 3','OGL v1.0','OGL-om 1.0','GODL-India','European Parliament','KOGL Type 1','PDM-owner']
    if not accepted:return q,None
    url=(ii.get('thumburl') or ii.get('url') or '').split('?')[0]
    if not url:return q,None
    # Portrait candidates must be raster images. A symbol/group SVG is not a
    # substitute for an individual likeness.
    if filename.lower().endswith('.svg'):return q,None
    ext='.png' if '.png' in url.lower() else '.jpg';relative='media/portrait-'+digest+ext;path=OUT/relative
    if relative in media_by_file and path.exists():return q,media_by_file[relative]
    if not path.exists():
        for attempt in range(5):
            try:
                with urllib.request.urlopen(urllib.request.Request(url+('?download=1' if attempt else ''),headers=UA),timeout=45) as response:raw=response.read()
                if len(raw)>5_000_000:return q,None
                if not raw.startswith((b'\xff\xd8',b'\x89PNG')):return q,None
                path.write_bytes(raw);break
            except Exception:
                if attempt==4:raise
                time.sleep(min(30,2**attempt*2))
        time.sleep(.4)
    clean=lambda value:html.unescape(re.sub('<[^>]*>','',value))
    result=dict(file=relative,title=filename,url=ii.get('descriptionurl','https://commons.wikimedia.org/wiki/File:'+urllib.parse.quote(filename)),artist=clean(meta.get('Artist',{}).get('value','')),license=license,licenseUrl=meta.get('LicenseUrl',{}).get('value','') or ii.get('descriptionurl','')+'#Licensing',attribution=clean(meta.get('Attribution',{}).get('value','')),attributionRequired=license=='Attribution' or meta.get('AttributionRequired',{}).get('value')=='true',credit=clean(meta.get('Credit',{}).get('value','')),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,sourceUrl=url)
    return q,result

portraits={}
for q,result in parallel(portrait,sorted(targets),workers=3):
    if result:portraits[q]=result;media_by_file[result['file']]=result
for country in countries.values():
    for leader in country['leaders']:
        q=leader['person']
        if q in portraits:leader['portrait']=portraits[q]
        if q in people and leader['name']==q:leader['name']=people[q]['name']
    country['leaders'].sort(key=lambda l:(l['start'],l['name']))
data['retrieved']=TODAY
data['reference']='All documented terms intersecting the selected civil year, capped at acquisition/device date; each term retains source precision.'
save(OUT/'data/identities.json',data)
manifest['retrieved']=TODAY;manifest['entries']=sorted(media_by_file.values(),key=lambda m:m['file']);save(OUT/'media/manifest.json',manifest)
missing=[dict(person=q,name=people.get(q,{}).get('name',q),image=people.get(q,{}).get('image'),reason='No P18 portrait documented' if not people.get(q,{}).get('image') else 'No usable licensed raster/download') for q in sorted(targets) if q not in portraits]
audit=dict(retrieved=TODAY,year=int(YEAR),targetPeople=len(targets),portraitPeople=len(portraits),mediaTotal=len(media_by_file),countriesWithAnnualTerms=sum(any(l['start']<=TODAY and l['end']>=START for l in c['leaders']) for c in countries.values()),missing=missing,corrections=corrections,unresolvedOpenTerms=unresolved)
save(CACHE/'current-authorities-audit.json',audit)
print(json.dumps({k:v for k,v in audit.items() if k not in ['missing','corrections','unresolvedOpenTerms']},ensure_ascii=False),flush=True)
print('Missing',json.dumps(missing,ensure_ascii=True),flush=True)
