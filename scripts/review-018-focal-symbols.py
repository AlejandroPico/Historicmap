"""Inspect historical symbol variants of focal1800 entities; no adoption."""
import pathlib,importlib.util,json,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
SEARCHES=[('PRUSSIA-EARLY','intitle:"Flag of the Kingdom of Prussia" 1750'),('SAR-EARLY','intitle:"Flag of the Kingdom of Sardinia"'),('PORTUGAL-EARLY','intitle:"Flag of Portugal (1707)"'),('RAGUSA','intitle:"Flag of the Republic of Ragusa"'),('TOKUGAWA','intitle:"Flag of the Tokugawa"'),('JOSEON','intitle:"Flag of the king of Joseon"'),('MOROCCO','intitle:"Flag of Morocco (1666"'),('BATAVIA','intitle:"Flag of the Batavian Republic"')]
titles=[]
for key,q in SEARCHES:
 params=dict(action='query',list='search',srnamespace=6,srlimit=3,srsearch=q,format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'focal018-search-'+key);found=[r['title'] for r in d.get('query',{}).get('search',[])];titles.extend(found);print(key,found,flush=True)
params=dict(action='query',titles='|'.join(titles),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'focal018meta-'+hashlib.sha256('|'.join(titles).encode()).hexdigest()[:16]);p=ROOT/'.cache/symbols018-pages.json';pages={x['title']:x for x in json.loads(p.read_text(encoding='utf8'))};pages.update({x['title']:x for x in d.get('query',{}).get('pages',{}).values()});h.save(p,list(pages.values()))
for page in d.get('query',{}).get('pages',{}).values():
 print(page['title'],page.get('imageinfo',[{}])[0].get('extmetadata',{}).get('LicenseShortName',{}).get('value'));print(page.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')[:900],flush=True)
