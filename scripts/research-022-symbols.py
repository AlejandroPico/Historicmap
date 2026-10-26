"""Symbol candidates and Commons source descriptions; no automatic adoption."""
import pathlib,importlib.util,json,concurrent.futures,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('s',ROOT/'scripts/research-019-symbols.py');s=importlib.util.module_from_spec(s);spec=importlib.util.spec_from_file_location('s',ROOT/'scripts/research-019-symbols.py');spec.loader.exec_module(s);h=s.h
QUERIES=[('BYZANTINE','intitle:"Byzantine" "imperial flag"'),('GRANADA','intitle:"Royal Standard" Granada'),('PORTUGAL','intitle:"Flag of Portugal" 1385'),('BURGUNDY','intitle:"Banner" Burgundy'),('NAVARRE','intitle:"Banner" Navarre'),('SAVOY','intitle:"Flag of Savoy"')]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as p:rows=list(p.map(s.search,QUERIES))
pages={p['title']:p for p in json.loads((ROOT/'.cache/symbols021-pages.json').read_text(encoding='utf8'))};titles=list(dict.fromkeys(t for r in rows for t in r['titles'] if t.lower().endswith(('.svg','.png','.jpg'))))
for i in range(0,len(titles),15):
 ts=titles[i:i+15];p=dict(action='query',titles='|'.join(ts),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(p),'022-symbolmeta-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:18]);pages.update({p['title']:p for p in d.get('query',{}).get('pages',{}).values()})
h.save(ROOT/'.cache/symbols022-pages.json',list(pages.values()));h.save(ROOT/'.cache/symbols022-searches.json',rows)
for r in rows:print(r['key'],r['titles'],flush=True)
