"""Stage licensed portrait candidates for visual review; never adopt on P18 alone."""
from pathlib import Path
import json,urllib.request,urllib.parse,hashlib,re,html,argparse,concurrent.futures,importlib.util,time
ROOT=Path(__file__).resolve().parents[1];UA={'User-Agent':'Historicmap/0.32 (https://github.com/AlejandroPico/Historicmap; educational atlas)'};read=lambda f:json.loads(f.read_text(encoding='utf8'))
def main(century,review,selected_people=None):
 spec=importlib.util.spec_from_file_location('fetch',ROOT/'scripts/acquire-century-evidence.py');api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
 docs=[(f,read(f))for f in sorted((ROOT/'Países').glob(f'*/periodos/{century:04d}-{century+99:04d}.json'))];people={l['person']:l['name']for f,d in docs for l in d['leaders']};ids=read(ROOT/'public/data/identities.json');known={l['person']:l['portrait']for c in ids['countries'].values()for l in c['leaders']if l.get('portrait')};existing={m['title']:m for m in read(ROOT/'public/media/manifest.json')['entries']};titles={};missing=[]
 if selected_people:people={q:name for q,name in people.items()if q in selected_people}
 for q,name in people.items():
  f=ROOT/'.cache/identities'/('historical-entity-'+q+'.json')
  if q in known:titles[q]=known[q]['title'];continue
  if not f.exists():missing.append(dict(person=q,name=name,reason='No human-item image metadata; do not invent a portrait.'));continue
  e=read(f)['entities'][q];images=[c['mainsnak']['datavalue']['value']for c in e.get('claims',{}).get('P18',[])if c.get('rank')!='deprecated'and'datavalue'in c['mainsnak']]
  if images:titles[q]=images[0]
  else:missing.append(dict(person=q,name=name,reason='No image candidate in the resolved metadata.'))
 previous=ROOT/'.cache'/('photo-review'+review+'.json')
 if previous.exists():
  for row in read(previous):
   m=row['media']
   if m.get('stagedFile')and(ROOT/m['stagedFile']).exists():existing.setdefault(m['title'],m)
 infos={};ts=sorted(set(titles.values())-existing.keys())
 for i in range(0,len(ts),20):
  batch=ts[i:i+20]
  try:
   data=api.request(dict(action='query',titles='|'.join('File:'+t for t in batch),redirects=1,prop='imageinfo',iiprop='url|size|extmetadata',iiurlwidth=330,format='json'),'https://commons.wikimedia.org/w/api.php',f'portrait-info{review}-330-'+hashlib.sha256('|'.join(batch).encode()).hexdigest()[:18]);query=data.get('query',{});aliases={r['from'].removeprefix('File:'):r['to'].removeprefix('File:')for r in query.get('normalized',[])+query.get('redirects',[])};pages={v['title'].removeprefix('File:'):v.get('imageinfo',[{}])[0]for v in query.get('pages',{}).values()}
   for title in batch:
    canonical=title
    for _ in range(8):
     if canonical not in aliases:break
     canonical=aliases[canonical]
    if pages.get(canonical):infos[title]=pages[canonical]
  except Exception as e:print('Media metadata unavailable',i,str(e),flush=True)
 stage=ROOT/'.cache'/('portraits'+review);stage.mkdir(exist_ok=True)
 def get(title):
  if title in existing:return existing[title]
  info=infos.get(title);meta=info.get('extmetadata',{})if info else{};license=meta.get('LicenseShortName',{}).get('value','');clean=lambda k:html.unescape(re.sub('<[^>]*>','',meta.get(k,{}).get('value','')))
  if not info or not any(t in license.lower()for t in['public domain','cc0','cc by','cc-by']):return None
  url=info['url']if info.get('size',9999999)<1000000 else info.get('thumburl')or info['url'];digest=hashlib.sha256(title.encode()).hexdigest()[:20];target=stage/(digest+'.bin')
  try:
   if target.exists():raw=target.read_bytes()
   else:
    time.sleep(1.3)
    with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=25)as response:raw=response.read(5000001)
    if len(raw)>5000000:raise ValueError('Image exceeds acquisition bound')
    target.write_bytes(raw)
   ext='.jpg'if raw.startswith(b'\xff\xd8')else'.png'if raw.startswith(b'\x89PNG')else'.svg'if b'<svg'in raw[:2000]else None
   if not ext:return None
   if ext=='.svg'and re.search(rb'<script|javascript:|\bonload\s*=',raw,re.I):return None
   return dict(file='media/portrait-'+digest+ext,title=title,url=info['descriptionurl'],sourceUrl=url,artist=clean('Artist'),license=license,licenseUrl=clean('LicenseUrl')or info['descriptionurl']+'#Licensing',attribution=clean('Attribution'),attributionRequired=True,credit=clean('Credit'),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),stagedFile=target.relative_to(ROOT).as_posix())
  except Exception as e:print('Image unavailable',title,str(e),flush=True);return None
 with concurrent.futures.ThreadPoolExecutor(max_workers=1)as pool:media=dict(zip(sorted(set(titles.values())),pool.map(get,sorted(set(titles.values())))))
 rows=[]
 for q,title in titles.items():
  m=known.get(q)or media.get(title)
  if not m:missing.append(dict(person=q,name=people[q],title=title,reason='Licensed candidate could not be retrieved.'));continue
  rows.append(dict(person=q,name=people[q],media=m,dossiers=[f.relative_to(ROOT).as_posix()for f,d in docs if any(l['person']==q for l in d['leaders'])]))
 api.save(ROOT/'.cache'/('photo-review'+review+'.json'),rows);api.save(ROOT/'.cache'/('photo-missing'+review+'.json'),missing);print('Visual candidates',len(rows),'missing or unavailable',len(missing),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--century',type=int,required=True);p.add_argument('--review',required=True);p.add_argument('--people',nargs='+',help='Stage only these already documented authority identifiers.');a=p.parse_args();main(a.century,a.review,a.people)
