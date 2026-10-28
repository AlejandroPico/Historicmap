"""Explicit, bounded acquisition for entity-owned named office candidates.

Never called by the build. Missing metadata stays pending, not inferred.
"""
from pathlib import Path
import json,urllib.request,urllib.parse,urllib.error,hashlib,concurrent.futures,importlib.util,argparse,re,time,threading
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'.cache';UA={'User-Agent':'Historicmap/0.32 (https://github.com/AlejandroPico/Historicmap; historical research)'}
read=lambda f:json.loads(f.read_text(encoding='utf8'))
_REQUEST_LOCK=threading.Lock()
_NEXT_REQUEST=0.0
def save(f,d):f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def request(params,host,key):
 global _NEXT_REQUEST
 f=CACHE/(key+'.json')
 if f.exists():return read(f)
 url=host+'?'+urllib.parse.urlencode(params)
 for attempt in range(3):
  # All acquisition workers share the same rate limit; cached evidence is free.
  with _REQUEST_LOCK:
   time.sleep(max(0,_NEXT_REQUEST-time.monotonic()));_NEXT_REQUEST=time.monotonic()+1.2
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=25)as r:d=json.load(r)
   break
  except urllib.error.HTTPError as e:
   if e.code not in [429,503]or attempt==2:raise
   delay=e.headers.get('Retry-After','')
   delay=float(delay)if delay.isdigit()else 4*(attempt+1)
   if delay>60:raise
   with _REQUEST_LOCK:_NEXT_REQUEST=max(_NEXT_REQUEST,time.monotonic()+delay)
 if 'error'in d:raise ValueError(str(d['error']))
 save(f,d);return d
def main(century,review,end_year=None):
 end_year=century+99 if end_year is None else end_year
 if not 1<=century<=end_year<=century+99:raise ValueError('Invalid common-era acquisition window')
 spec=importlib.util.spec_from_file_location('box',ROOT/'scripts/office-infobox.py');box=importlib.util.module_from_spec(spec);spec.loader.exec_module(box)
 eligible=importlib.util.spec_from_file_location('eligible',ROOT/'scripts/authority-eligibility.py');elig=importlib.util.module_from_spec(eligible);eligible.loader.exec_module(elig)
 paths=sorted((ROOT/'Países').glob(f'*/periodos/{century:04d}-{end_year:04d}.json'));dossiers={f:read(f)for f in paths};titles=sorted({t for d in dossiers.values()for c in d.get('candidates',[])for t in c['titles']});resolved={};entities={};errors=[]
 for i in range(0,len(titles),40):
  ts=titles[i:i+40]
  try:
   data=request(dict(action='query',titles='|'.join(ts),redirects=1,prop='pageprops',ppprop='wikibase_item',format='json'),'https://en.wikipedia.org/w/api.php',f'titles{review}-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:18]);q=data.get('query',{});aliases={v['from']:v['to']for v in q.get('normalized',[])+q.get('redirects',[])};pages={v['title']:v.get('pageprops',{}).get('wikibase_item')for v in q.get('pages',{}).values()}
   for t in ts:
    name=t
    for _ in range(10):
     if name not in aliases:break
     name=aliases[name]
    if pages.get(name):resolved[t]=(pages[name],name)
  except Exception as e:errors.append(str(e));print('Title metadata unavailable',i,str(e),flush=True)
 qs=sorted({q for q,t in resolved.values()})
 for i in range(0,len(qs),40):
  batch=qs[i:i+40]
  try:
   data=request(dict(action='wbgetentities',ids='|'.join(batch),props='labels|claims|sitelinks',format='json'),'https://www.wikidata.org/w/api.php',f'people{review}-'+hashlib.sha256('|'.join(batch).encode()).hexdigest()[:18]);entities.update({q:e for q,e in data.get('entities',{}).items()if 'missing'not in e})
  except Exception as e:errors.append(str(e));print('Person metadata unavailable',i,str(e),flush=True)
 def label(e):return next((e['labels'][l]['value']for l in['es','en','mul']if l in e.get('labels',{})),e.get('id',''))
 def qual(c,prop):
  v=c.get('qualifiers',{}).get(prop,[{}])[0].get('datavalue',{}).get('value',{});t=v.get('time','').lstrip('+')
  if not re.match(r'\d{4}-',t):return None
  return t[:10].replace('-00','-01'),v.get('precision',11)
 out=[]
 for t in titles:
  q,canonical=resolved.get(t,('',t));e=entities.get(q,{});human=elig.real_authority(e);row=dict(requestedTitle=t,title=t,person=q,name=label(e)or t,human=human,source='https://en.wikipedia.org/wiki/'+urllib.parse.quote(canonical.replace(' ','_')),identityResolution=dict(requested=t,canonical=canonical,qid=q));claims=[]
  if q and e:
   cache=ROOT/'.cache/identities'/('historical-entity-'+q+'.json');cache.parent.mkdir(exist_ok=True);save(cache,dict(entities={q:e}))
  if human:
   for prop in['P39','P97']:
    for c in e.get('claims',{}).get(prop,[]):
     a,b=qual(c,'P580'),qual(c,'P582');office=c.get('mainsnak',{}).get('datavalue',{}).get('value',{}).get('id')
     if c.get('rank')!='deprecated'and a and b and a[0][:4]<=str(end_year).zfill(4)and b[0][:4]>=str(century).zfill(4):claims.append(dict(property=prop,office=office,start=a[0],end=b[0],precision=min(a[1],b[1]),statement=c.get('id')))
  out.append(dict(candidate=row,claims=claims,fields=[]))
 offices=sorted({c['office']for r in out for c in r['claims']if c['office']});labels={}
 for i in range(0,len(offices),40):
  batch=offices[i:i+40]
  try:
   data=request(dict(action='wbgetentities',ids='|'.join(batch),props='labels',format='json'),'https://www.wikidata.org/w/api.php',f'office-labels{review}-'+hashlib.sha256('|'.join(batch).encode()).hexdigest()[:18]);labels.update({q:label(e)for q,e in data.get('entities',{}).items()if 'missing'not in e})
  except Exception as e:errors.append(str(e))
 for r in out:
  for c in r['claims']:c['label']=labels.get(c['office'],'')
 def reign(r):
  v=r['candidate'];title=v['identityResolution']['canonical']
  try:
   data=request(dict(action='parse',page=title,prop='wikitext',format='json',redirects=1),'https://en.wikipedia.org/w/api.php',f'reign{review}-'+hashlib.sha256(title.encode()).hexdigest()[:18]);text=data.get('parse',{}).get('wikitext',{}).get('*','');return dict(person=v['person'],title=title,source=v['source'],reignFields=box.extract(text,include_succession=True))
  except Exception as e:return dict(person=v['person'],title=title,source=v['source'],reignFields=[],error=str(e))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:fields=list(pool.map(reign,[r for r in out if r['candidate']['human']]))
 save(CACHE/f'rulers{review}-office-evidence.json',out);save(CACHE/f'rulers{review}-reign-evidence.json',fields)
 bytitle={r['candidate']['requestedTitle']:r for r in out};byq={r['person']:r for r in fields}
 for path,d in dossiers.items():
  names={t for c in d.get('candidates',[])for t in c['titles']};d['candidateEvidence']=[dict(**bytitle[t],reignEvidence=byq.get(bytitle[t]['candidate'].get('person')))for t in sorted(names)if t in bytitle];save(path,d)
 print('Named candidates',len(titles),'resolved humans',sum(r['candidate']['human']for r in out),'reign-field records',sum(bool(r['reignFields'])for r in fields),'metadata errors',len(errors),'reign errors',sum('error'in r for r in fields),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--century',type=int,required=True);p.add_argument('--review',required=True);p.add_argument('--end-year',type=int);a=p.parse_args();main(a.century,a.review,a.end_year)
