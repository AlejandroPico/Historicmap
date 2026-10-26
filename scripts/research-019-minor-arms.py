"""Read historical polity emblems and retain Commons metadata for manual review."""
import pathlib,importlib.util,urllib.parse,hashlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
qs=['Q168651','Q693551','Q650370','Q560771','Q157367','Q830084','Q11024667','Q2751106','Q315667']
params=dict(action='wbgetentities',ids='|'.join(qs),props='claims|labels',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'arms019-polities')
titles=[]
for q,e in d['entities'].items():
 names=h.values(e,'P94')+h.values(e,'P41');print(q,h.label(e),names,flush=True);titles.extend('File:'+t for t in names if isinstance(t,str))
titles+=['File:Banner of Baden (3^2).svg','File:Flag of Great Britain (1707–1800).svg','File:Flag of Cross of Burgundy.svg']
pages=json.loads((ROOT/'.cache/symbols019-pages.json').read_text(encoding='utf8'));by={p['title']:p for p in pages}
for i in range(0,len(titles),15):
 group=titles[i:i+15];params=dict(action='query',titles='|'.join(group),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'arms019-meta-'+hashlib.sha256('|'.join(group).encode()).hexdigest()[:18]);by.update({p['title']:p for p in d.get('query',{}).get('pages',{}).values()})
h.save(ROOT/'.cache/symbols019-pages.json',list(by.values()))
