"""Frozen fourteenth-century office and noble-title evidence; review required."""
import pathlib,importlib.util,json,urllib.parse,urllib.request,hashlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-018-german-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r);h=r.h
EXTRA=[('PAPAL-STATES','Papa · soberano temporal',t) for t in ['Pope Boniface VIII','Pope Benedict XI','Pope Clement V','Pope John XXII','Pope Benedict XII','Pope Clement VI','Pope Innocent VI','Pope Urban V','Pope Gregory XI','Pope Urban VI','Pope Boniface IX']]
EXTRA += [('DNK','Rey de Dinamarca',t) for t in ['Eric VI of Denmark','Christopher II of Denmark','Valdemar IV of Denmark','Olaf II of Denmark','Margaret I of Denmark']]
EXTRA += [('NORWAY-KINGDOM','Rey de Noruega',t) for t in ['Haakon V of Norway','Magnus VII of Norway','Haakon VI of Norway','Olaf IV of Norway','Margaret I of Denmark']]
EXTRA += [('SWE','Rey de Suecia',t) for t in ['Birger of Sweden','Magnus IV of Sweden','Albert, King of Sweden','Margaret I of Denmark']]
EXTRA += [('HESSE-UNITED','Landgrave de Hesse',t) for t in ['Henry I, Landgrave of Hesse','Otto I, Landgrave of Hesse','Henry II, Landgrave of Hesse','Hermann II, Landgrave of Hesse']]
EXTRA += [('SAXONY-ELECTORATE','Duque de Sajonia-Wittenberg · dignidad electoral',t) for t in ['Rudolf I, Duke of Saxe-Wittenberg','Rudolf II, Duke of Saxe-Wittenberg','Wenceslaus I, Duke of Saxe-Wittenberg','Rudolf III, Duke of Saxe-Wittenberg']]
EXTRA += [('ELECTORATE-BRANDENBURG','Margrave de Brandeburgo',t) for t in ['Otto IV, Margrave of Brandenburg-Stendal','Waldemar, Margrave of Brandenburg-Stendal','Louis V, Duke of Bavaria','Louis II, Elector of Brandenburg','Otto V, Duke of Bavaria','Sigismund, Holy Roman Emperor','Jobst of Moravia']]
EXTRA += [('JPN','Shikken Hōjō · regencia militar',t) for t in ['Hōjō Sadatoki','Hōjō Morotoki','Hōjō Takatoki']]
EXTRA += [('YUAN','Emperador Yuan','Khutughtu Khan Kusala')]
base=json.loads((ROOT/'.cache/rulers023-candidates.json').read_text(encoding='utf8'));rows={v['title']:v for v in base['records']}
# Retry metadata, not the HTML requests which received service back pressure.
spec=importlib.util.spec_from_file_location('g',ROOT/'scripts/review-023-rulers.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
missing=[(k,role,t) for k,role,ts in g.r.GROUPS for t in ts if t in {e['title'] for e in base['errors']}]
for k,role,t in EXTRA+missing:rows.setdefault(t,dict(key=k,role=role,title=t,requestedTitle=t,source='https://en.wikipedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_')),fields=[],parsed=[]))
titles=list(rows)
for off in range(0,len(titles),20):
 ts=titles[off:off+20];p=dict(action='wbgetentities',sites='enwiki',titles='|'.join(ts),props='labels|claims|sitelinks',redirects='yes',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'023-offices-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:18])
 for q,e in d.get('entities',{}).items():
  if 'missing' in e:continue
  canonical=e.get('sitelinks',{}).get('enwiki',{}).get('title');h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}))
  for t in ts:
   if canonical==t or rows[t].get('person')==q:rows[t].update(person=q,name=h.label(e),human=any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)))
# enwiki title redirects are different from Wikidata item redirects. Resolve
# aliases explicitly so an easily found sovereign is not silently dropped.
unresolved=[t for t,row in rows.items() if not row.get('person')]
for offset in range(0,len(unresolved),40):
 ts=unresolved[offset:offset+40];params=dict(action='query',titles='|'.join(ts),redirects=1,prop='pageprops',ppprop='wikibase_item',format='json');url='https://en.wikipedia.org/w/api.php?'+urllib.parse.urlencode(params);path=ROOT/'.cache'/('redirect023-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:16]+'.json')
 try:
  if path.exists():redirects=json.loads(path.read_text(encoding='utf8'))
  else:
   with urllib.request.urlopen(urllib.request.Request(url,headers=h.UA),timeout=20) as response:redirects=json.load(response)
   h.save(path,redirects)
  query=redirects.get('query',{});aliases={v['from']:v['to'] for v in query.get('normalized',[])+query.get('redirects',[])};pages={p['title']:p.get('pageprops',{}).get('wikibase_item') for p in query.get('pages',{}).values()};resolved={}
  for title in ts:
   canonical=title
   for _ in range(8):
    if canonical not in aliases:break
    canonical=aliases[canonical]
   q=pages.get(canonical)
   if q:resolved[title]=(q,canonical)
  qs=sorted({v[0] for v in resolved.values()})
  if qs:
   p=dict(action='wbgetentities',ids='|'.join(qs),props='labels|claims|sitelinks',format='json');entities=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'023-redirect-persons-'+hashlib.sha256('|'.join(qs).encode()).hexdigest()[:16])['entities']
   for title,(q,canonical) in resolved.items():
    e=entities[q];h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}));rows[title].update(person=q,name=h.label(e),human=any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)),identityResolution=dict(requested=title,canonical=canonical,qid=q,source=url))
 except Exception as error:print('Alias metadata unavailable',str(error),flush=True)
out=[]
for row in rows.values():
 q=row.get('person');claims=[];fields=[]
 if q and row.get('human'):
  e=h.entity(q)
  for prop in ['P39','P97']:
   for c in e.get('claims',{}).get(prop,[]):
    a=h.qual(c,'P580');b=h.qual(c,'P582');office=c.get('mainsnak',{}).get('datavalue',{}).get('value',{}).get('id')
    if c.get('rank')!='deprecated' and a and b and a[0]<'1400' and b[0]>='1300':claims.append(dict(property=prop,office=office,start=a[0],end=b[0],precision=min(a[1],b[1]),statement=c.get('id')))
 p=ROOT/'.cache'/('ruler018-'+hashlib.sha256(row['requestedTitle'].encode()).hexdigest()[:16]+'.html')
 if p.exists():
  raw=p.read_text(encoding='utf8');box=re.search(r'<table\b[^>]*class="[^"]*infobox[^>]*>(.*?)</table>',raw,re.S);fields=[r.clean(t) for t in re.findall(r'<tr\b[^>]*>(.*?)</tr>',box.group(1) if box else '',re.S)]
 out.append(dict(candidate=row,claims=claims,fields=fields))
offices=sorted({v['office'] for row in out for v in row['claims'] if v.get('office')});labels={}
for off in range(0,len(offices),40):
 qs=offices[off:off+40];p=dict(action='wbgetentities',ids='|'.join(qs),props='labels',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'023-office-labels-'+hashlib.sha256('|'.join(qs).encode()).hexdigest()[:16]);labels.update({q:h.label(e) for q,e in d.get('entities',{}).items() if 'missing' not in e})
for row in out:
 for c in row['claims']:c['label']=labels.get(c['office'],'')
h.save(ROOT/'.cache/rulers023-office-evidence.json',out)
for row in out:
 v=row['candidate'];print(v['key'],v.get('person'),v.get('human'),v.get('name',v['title']),row['claims'] if not v['parsed'] else [],flush=True)
