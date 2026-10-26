"""Search historical symbol candidates; results are evidence, not approval."""
import pathlib,importlib.util,json,concurrent.futures,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('s',ROOT/'scripts/research-019-symbols.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);h=s.h
QUERIES=[('FRANCE','intitle:"Pavillon royal" France 1500'),('FRANCE-LILIES','intitle:"Banner" France fleurs lis'),('CASTILE','intitle:"Royal Banner" Castile'),('ARAGON','intitle:"Royal Banner" Aragon'),('PORTUGAL','intitle:"Flag of Portugal" 1495'),('PORTUGAL1521','intitle:"Flag of Portugal" 1521'),('PRUSSIA','intitle:"Flag of Ducal Prussia"'),('ASHIKAGA','intitle:"Ashikaga" mon'),('JOSEON','intitle:"Joseongukwangjiin" 1401'),('BAVARIA','intitle:"Bavaria" lozenges flag'),('FLORENCE','intitle:"Flag of Florence"')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(s.search,QUERIES))
for row in rows:print(row['key'],row['titles'],flush=True)
pages={p['title']:p for p in json.loads((ROOT/'.cache/symbols020-pages.json').read_text(encoding='utf8'))}
titles=list(dict.fromkeys(t for row in rows for t in row['titles'] if t.lower().endswith(('.svg','.jpg','.png'))))
for i in range(0,len(titles),15):
 ts=titles[i:i+15];params=dict(action='query',titles='|'.join(ts),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'021-symbolmeta-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:18]);pages.update({p['title']:p for p in d.get('query',{}).get('pages',{}).values()})
h.save(ROOT/'.cache/symbols021-pages.json',list(pages.values()));h.save(ROOT/'.cache/symbols021-searches.json',rows)
