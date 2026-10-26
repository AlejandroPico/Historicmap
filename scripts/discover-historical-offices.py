"""Discover explicit historical office identities; never guess a QID from a title.

Research output only. Exact English labels and existing office identities are
retained for review before dated holders are integrated.
"""
import importlib.util,pathlib,json,urllib.parse,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
ROWS=[('PRUSSIA','King of Prussia'),('HIST-Q154195','King of Bavaria'),('HIST-Q153015','King of Saxony'),('HIST-Q159631','King of Württemberg'),('HIST-Q164079','King of Hanover'),('HIST-Q186320','Grand Duke of Baden'),('HIST-Q20135','Grand Duke of Hesse'),('HIST-Q326029','Duke of Brunswick'),('HIST-Q836680','Duke of Nassau'),('HIST-Q697084','Grand Duke of Oldenburg'),('HIST-Q155570','Grand Duke of Saxe-Weimar-Eisenach'),('HIST-Q639100','Prince of Reuss-Gera'),('HIST-Q708821','Prince of Schwarzburg-Sondershausen'),('HIST-Q165763','Prince of Waldeck and Pyrmont'),('HIST-Q14551680','Prince of Lippe'),('HIST-Q252580','Duke of Modena and Reggio'),('HIST-Q165040','Duke of Parma'),('HIST-Q154849','Grand Duke of Tuscany'),('TWO-SICILIES','King of the Two Sicilies'),('HAW-KINGDOM','King of Hawaii'),('NPL','Prime Minister of Nepal'),('HIST-Q1071439','King of Madagascar'),('HIST-Q6500483','Emperor of Vietnam'),('EGY','Khedive of Egypt'),('JPN','shogun'),('QING','Emperor of China'),('SAR','King of Sardinia'),('PAPAL-STATES','pope')]
KNOWN=[('JOS','Q22304810','King of Joseon Dynasty'),('ETH','Q10962705','Emperor of Ethiopia'),('AUSTRIAN-EMPIRE','Q166877','Emperor of Austria'),('NPL','Q19700527','King of Nepal'),('IRN','Q184299','Shah'),('PRT','Q58800860','Monarca de Portugal'),('MAR','Q14566713','Sultán de Marruecos'),('MMR','Q27334179','Rey de Birmania'),('AFG','Q17323614','Emir de Afganistán'),('SWE','Q1268572','Rey de Suecia'),('DNK','Q18341329','Rey de Dinamarca'),('GRC','Q87071077','Rey de los helenos'),('NLD','Q2045066','Rey de los Países Bajos'),('BEL','Q13592862','Rey de los belgas')]
def discover(row):
 key,title=row;url='https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='wbsearchentities',search=title,language='en',limit=8,format='json'))
 d=h.get(url,'office-discovery-'+title.lower().replace(' ','-'));results=d.get('search',[])
 exact=[r for r in results if r.get('label','').casefold()==title.casefold()]
 return dict(key=key,requested=title,matches=[dict(qid=r['id'],label=r.get('label'),description=r.get('description','')) for r in results],office=exact[0]['id'] if len(exact)==1 else None)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:found=list(p.map(discover,ROWS))
 for key,qid,title in KNOWN:found.append(dict(key=key,requested=title,office=qid,matches=[dict(qid=qid,label=h.label(h.entity(qid)),description='Previously verified explicit office')]))
 path=ROOT/'.cache/offices-1840.json';h.save(path,found)
 for r in found:print(r['key'],r['requested'],r['office'],flush=True)
