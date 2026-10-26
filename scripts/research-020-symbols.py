"""Candidate search and full Commons descriptions, not automatic adoption."""
import pathlib,importlib.util,json,concurrent.futures,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('s',ROOT/'scripts/research-019-symbols.py');s=importlib.util.module_from_spec(s);spec=importlib.util.spec_from_file_location('s',ROOT/'scripts/research-019-symbols.py');spec.loader.exec_module(s);h=s.h
QUERIES=[('COMMONWEALTH','Commonwealth England flag 1649'),('PROTECTORATE','Protectorate flag 1653'),('PORTUGAL','intitle:"Flag of Portugal" 1640'),('PORTUGAL-EARLY','intitle:"Flag of Portugal" 1578'),('SAVOY','intitle:"Flag of Savoy"'),('SPAIN','intitle:"Cross of Burgundy" flag'),('HESSE','intitle:"Arms" "Hesse"'),('BRANDENBURG','intitle:"Flag of Brandenburg"'),('MING','Ming dynasty imperial seal'),('MING-FLAG','Ming dynasty flag'),('KOREA','Joseongukwangjiin 1637'),('MARATHA','Shivaji royal seal'),('SAADI','Saadi flag'),('DUTCH','Prince flag Netherlands'),('AUSTRIA','Archduchy Austria coat arms')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(s.search,QUERIES))
for r in rows:print(r['key'],r['titles'],flush=True)
titles=list(dict.fromkeys(t for r in rows for t in r['titles'] if t.lower().endswith(('.svg','.jpg','.png'))));pages={p['title']:p for p in json.loads((ROOT/'.cache/symbols019-pages.json').read_text(encoding='utf8'))} if (ROOT/'.cache/symbols019-pages.json').exists() else {}
for i in range(0,len(titles),15):
 group=titles[i:i+15];params=dict(action='query',titles='|'.join(group),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'020-symbolmeta-'+hashlib.sha256('|'.join(group).encode()).hexdigest()[:18]);pages.update({p['title']:p for p in d.get('query',{}).get('pages',{}).values()})
h.save(ROOT/'.cache/symbols020-pages.json',list(pages.values()));h.save(ROOT/'.cache/symbols020-searches.json',rows)
