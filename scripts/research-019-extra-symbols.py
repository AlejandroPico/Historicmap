"""Broader names without assumed adoption years; retain exact descriptions."""
import pathlib,importlib.util,urllib.parse,hashlib,json,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('s',ROOT/'scripts/research-019-symbols.py');s=importlib.util.module_from_spec(s);spec=importlib.util.spec_from_file_location('s',ROOT/'scripts/research-019-symbols.py');spec.loader.exec_module(s);h=s.h
QUERIES=[('QING-BANNER','Plain Yellow Banner flag'),('QING-DRAGON','Qing emperor dragon banner'),('JOSEON-KOREAN','교룡기'),('JOSEON-CHINESE','交龍旗'),('JOSEON-SEAL','Joseon royal seal'),('MUGHAL-ORIGINAL','Mughal emperor ceremonial procession Id'),('SAFAVID-EARLY','Safavid flag'),('HESSE-ARMS','Hesse Darmstadt banner'),('KASSEL-ARMS','Hesse Kassel flag'),('BADEN-ARMS','Banner Baden'),('MECKLENBURG-ARMS','Mecklenburg Schwerin coat arms duchy'),('LIPPE-ARMS','Lippe county coat arms'),('KOKAND-ARMS','Kokand banner'),('KHIVA-EARLY','Khiva khan flag'),('ZAND-EARLY','Zand Ya Karim'),('JOSEON-ROYAL','Gyoryong'),('PRUSSIA-EARLY','Prussia 1701 flag')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(s.search,QUERIES))
for r in rows:print(r['key'],r['titles'],flush=True)
titles=list(dict.fromkeys([t for r in rows for t in r['titles'] if t.lower().endswith(('.svg','.png','.jpg','.jpeg'))]+['File:Flag of Russia.svg','File:Flag of Portugal (1667).svg','File:Flag of Denmark.svg','File:Flag of England.svg','File:Flag of Scotland.svg','File:Banner of the Holy Roman Emperor without haloes (1400-1806).svg','File:Flag of the Dutch East India Company.svg']))
p=ROOT/'.cache/symbols019-pages.json';pages={r['title']:r for r in json.loads(p.read_text(encoding='utf8'))}
for offset in range(0,len(titles),20):
 group=titles[offset:offset+20];params=dict(action='query',titles='|'.join(group),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'symbol019-extra-'+hashlib.sha256('|'.join(group).encode()).hexdigest()[:18]);pages.update({r['title']:r for r in d.get('query',{}).get('pages',{}).values()})
h.save(p,list(pages.values()));h.save(ROOT/'.cache/symbols019-extra-searches.json',rows);print('Additional candidate descriptions retained',len(pages),flush=True)
