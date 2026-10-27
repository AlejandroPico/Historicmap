"""Bounded API fallback: only explicit infobox reigns, never birth/death dates."""
import pathlib,json,importlib.util,urllib.parse,urllib.request,hashlib,re,concurrent.futures,html,calendar
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-018-german-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r);h=r.h
bs=importlib.util.spec_from_file_location('box',ROOT/'scripts/office-infobox.py');box=importlib.util.module_from_spec(bs);bs.loader.exec_module(box)

def fetch(row):
 v=row['candidate'];title=v.get('identityResolution',{}).get('canonical',v['requestedTitle']);p=ROOT/'.cache'/('reign027-'+hashlib.sha256(title.encode()).hexdigest()[:18]+'.json')
 try:
  if p.exists():data=json.loads(p.read_text(encoding='utf8'))
  else:
   url='https://en.wikipedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='parse',page=title,prop='wikitext',format='json',redirects=1))
   with urllib.request.urlopen(urllib.request.Request(url,headers=h.UA),timeout=20)as resp:data=json.load(resp)
   h.save(p,data)
  text=data.get('parse',{}).get('wikitext',{}).get('*','');fields=box.extract(text)
  return dict(person=v.get('person'),title=title,source='https://en.wikipedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_')),reignFields=fields)
 except Exception as e:return dict(person=v.get('person'),title=title,error=str(e),reignFields=[])
if __name__=='__main__':
 rows=json.loads((ROOT/'.cache/rulers027-office-evidence.json').read_text(encoding='utf8'));targets=[v for v in rows if v['candidate'].get('human')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:out=list(pool.map(fetch,targets))
 h.save(ROOT/'.cache/rulers027-reign-evidence.json',out);print('Explicit reign-field evidence',sum(bool(v['reignFields'])for v in out),'/',len(out),'API errors',sum('error'in v for v in out))
