"""Commons symbol candidates and provenance, never automatic adoption."""
import pathlib,importlib.util,urllib.parse,hashlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
QUERIES=[('HRE','Holy Roman Emperor banner'),('HELVETIC','Helvetic Republic flag'),('MOLDAVIA','Moldavia flag 1834'),('WALLACHIA','Wallachia flag 1834'),('OTTOMAN','Ottoman Empire flag 1793'),('NAPLES','Kingdom Naples Bourbon flag'),('PAPAL','Papal States flag 1808'),('PAPAL-EARLY','Papal States flag pre 1808'),('GRAN-COLOMBIA','Gran Colombia flag'),('PERU','Peru flag 1822'),('RIO','Argentina flag 1818'),('SOKOTO','Sokoto Caliphate flag'),('WADAI','Wadai flag'),('BORNU','Bornu Empire flag'),('LIPPE','Lippe flag'),('NASSAU','Nassau flag'),('HESSE','Grand Duchy Hesse flag'),('BADEN','Baden flag 1871'),('GOTHA','Saxe Coburg Gotha flag'),('WEIMAR','Saxe Weimar Eisenach flag'),('WURTTEMBERG','Wurttemberg flag 1816'),('SAXONY','Saxony flag 1815'),('HANOVER','Hanover flag'),('SCHWARZBURG','Schwarzburg Sondershausen flag')]
def search(row):
 key,q=row;params=dict(action='query',list='search',srnamespace=6,srlimit=4,srsearch=q,format='json')
 d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'symbols018-search-'+key)
 return dict(key=key,query=q,titles=[r['title'] for r in d.get('query',{}).get('search',[])])
def main():
 QUERIES.extend([('NAPLES-EXACT','intitle:"Flag of the Kingdom of Naples"'),('NASSAU-EXACT','intitle:"Flag of the Duchy of Nassau"'),('GOTHA-EXACT','intitle:"Flag of Saxe-Coburg"')])
 result=[]
 for row,r in h.parallel(search,QUERIES):
  if r:result.append(r);print(r['key'],r['titles'],flush=True)
 h.save(ROOT/'.cache/symbols018-searches.json',result)
 titles=list(dict.fromkeys(t for r in result for t in r['titles'] if t.lower().endswith(('.svg','.png','.jpg'))));pages=[]
 for offset in range(0,len(titles),20):
  group=titles[offset:offset+20];params=dict(action='query',titles='|'.join(group),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json')
  d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'symbols018-meta-'+hashlib.sha256('|'.join(group).encode()).hexdigest()[:18])
  pages.extend(d.get('query',{}).get('pages',{}).values())
 h.save(ROOT/'.cache/symbols018-pages.json',pages)
 print('Symbol descriptions retained',len(pages),flush=True)
if __name__=='__main__':main()
