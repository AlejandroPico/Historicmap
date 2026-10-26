"""Symbols: search and retain descriptions/revisions before dated adoption."""
import pathlib,importlib.util,urllib.parse,hashlib,json,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
QUERIES=[('RUSSIA','intitle:"Flag of Russia.svg"'),('RUSSIA-ROYAL','Tsar Muscovy flag 1693'),('QAJAR','Fath Ali Shah flag'),('SAFAVID','Safavid flag 1736'),('AFSHARID','Afsharid flag'),('ZAND','Zand flag'),('MUGHAL','Mughal flag'),('MARATHA','intitle:"Flag of the Maratha Empire.svg"'),('SIAM','Thailand flag Ayutthaya'),('BURMA','intitle:"National flag of the Konbaung Empire.svg"'),('KHIVA','Khiva Khanate flag'),('BUKHARA','Bukhara Khanate flag'),('KOKAND','intitle:"Banner of the Kokand Khans.svg"'),('TOKUGAWA','intitle:"Tokugawa family crest.svg"'),('JOSEON','Daehwanggi'),('JOSEON-DRAGON','Hwangnyonggi'),('QING-CEREMONIAL','Qing ceremonial flag'),('QING-MANUSCRIPT','Huangchao liqi tushi'),('BAVARIA','Electorate Bavaria flag'),('SAXONY','Saxony flag 1700'),('HANOVER','intitle:"Flag of Hanover (1692).svg"'),('HESSE','Hesse Darmstadt flag 1700'),('HESSE-KASSEL','Hesse Kassel flag 1700'),('WURTTEMBERG','Duchy Wurttemberg flag'),('BADEN','Margraviate Baden flag'),('BRUNSWICK','Brunswick Wolfenbuttel flag'),('MECKLENBURG','Mecklenburg Schwerin flag'),('LIPPE','County Lippe flag'),('MOLDAVIA','Moldavia before 1834'),('WALLACHIA','Wallachia banner 1700')]
def search(row):
 key,q=row;params=dict(action='query',list='search',srnamespace=6,srlimit=4,srsearch=q,format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'symbol019-search-'+key);return dict(key=key,query=q,titles=[r['title'] for r in d.get('query',{}).get('search',[])])
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(search,QUERIES))
 for r in rows:print(r['key'],r['titles'],flush=True)
 titles=list(dict.fromkeys(t for r in rows for t in r['titles'] if t.lower().endswith(('.svg','.png','.jpg','.jpeg','.gif'))));pages=[]
 for offset in range(0,len(titles),20):
  group=titles[offset:offset+20];params=dict(action='query',titles='|'.join(group),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json');d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'symbol019-meta-'+hashlib.sha256('|'.join(group).encode()).hexdigest()[:18]);pages.extend(d.get('query',{}).get('pages',{}).values())
 h.save(ROOT/'.cache/symbols019-pages.json',pages);h.save(ROOT/'.cache/symbols019-searches.json',rows)
 print('Symbol candidates',len(pages),flush=True)
