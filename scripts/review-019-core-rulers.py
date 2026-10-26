"""Core historical sovereigns: research reign fields, not modern office guesses."""
import pathlib,importlib.util,concurrent.futures,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-018-german-rulers.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r);h=r.h
GROUPS=[('FRA','Rey de Francia',['Louis XIV','Louis XV']),('ESP','Rey de España',['Charles II of Spain','Philip V of Spain']),('PRT','Rey / reina de Portugal',['Peter II of Portugal','John V of Portugal','Joseph I of Portugal','Maria I of Portugal']),('ENGLAND','Rey / reina de Inglaterra',['William III of England','Anne, Queen of Great Britain']),('GBR','Rey / reina de Gran Bretaña',['Anne, Queen of Great Britain','George I of Great Britain','George II of Great Britain','George III']),('RUSSIA-TSARDOM','Zar de Rusia',['Peter the Great']),('SAFAVID','Shah safávida',['Sultan Husayn','Tahmasp II','Abbas III']),('AFSHARID','Shah afshárida',['Nader Shah','Adil Shah','Ebrahim Afshar','Shahrokh Shah']),('ZAND','Gobernante de la dinastía Zand',['Karim Khan Zand','Abu al-Fath Khan Zand','Sadeq Khan Zand','Ali-Morad Khan Zand','Jafar Khan Zand','Said-Murad Khan Zand','Lotf Ali Khan Zand']),('IRN','Shah Qajar',['Agha Mohammad Khan Qajar','Fath-Ali Shah Qajar']),('THONBURI','Rey de Thonburi',['Taksin']),('THA','Rey de Siam',['Rama I']),('POLISH-LITHUANIAN','Rey de Polonia y gran duque de Lituania',['Augustus II the Strong','Stanisław Leszczyński','Augustus III of Poland','Stanisław August Poniatowski']),('HIST-Q154849','Gran duque de Toscana',['Cosimo III de Medici','Gian Gastone de Medici']),('DENMARK-NORWAY','Rey de Dinamarca y Noruega',['Frederick IV of Denmark','Christian VI of Denmark','Frederick V of Denmark','Christian VII of Denmark']),('DUTCH-REPUBLIC','Estatúder · cargo provincial de la República',['William III of England','William IV, Prince of Orange','William V, Prince of Orange'])]
def main():
 rows=[(key,role,title) for key,role,ts in GROUPS for title in ts];out=[];errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for row,v in zip(rows,pool.map(r.safe,rows)):
   if isinstance(v,dict):out.append(v)
   else:errors.append(dict(title=row[2],error=v))
 titles=list(dict.fromkeys(v['title'] for v in out))
 for offset in range(0,len(titles),20):
  group=titles[offset:offset+20];params=dict(action='wbgetentities',sites='enwiki',titles='|'.join(group),props='labels|claims|sitelinks',redirects='yes',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'core019meta-'+hashlib.sha256('|'.join(group).encode()).hexdigest()[:18])
  for q,e in d.get('entities',{}).items():
   if 'missing' in e:continue
   title=e.get('sitelinks',{}).get('enwiki',{}).get('title');h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}))
   for v in out:
    if v['title']==title:v.update(person=q,name=h.label(e),human=any(t.get('id')=='Q5' for t in h.values(e,'P31') if isinstance(t,dict)))
 for v in out:print(v['key'],v.get('person'),v['title'],v['parsed'],flush=True)
 h.save(ROOT/'.cache/core019-rulers.json',dict(records=out,errors=errors));print('Errors',errors,flush=True)
if __name__=='__main__':main()
