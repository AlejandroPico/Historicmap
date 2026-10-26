"""Reviewed offices, sovereign titles and identity rules for1700–1799.

Uses a frozen reviewed record by default. Research regeneration is explicit.
Existing1800+ facts are preserved; new German identities may carry their own
continuous mandates across1800 without rewriting previously shipped records.
"""
import pathlib,json,copy,sys,importlib.util,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1700-0.19'
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
INDEX={'Q53438':1,'Q53444':2,'Q76736':2,'Q44961':1,'Q44319':2,'Q52932':1,'Q213527':1,'Q213671':3,'Q213533':2,'Q58025':1,'Q150494':3,'Q150665':1,'Q131706':2,'Q76555':3,'Q151321':1,'Q130834':1,'Q130805':1}
MISSING={'Q58020':('1763-10-05','1763-12-17',11),'Q62231':('1700-01-01','1709-06-25',11),'Q58755':('1700-01-01','1707-01-04',11),'Q85473':('1700-01-01','1718-12-31',9),'Q319161':('1718-01-01','1734-12-31',9),'Q76100':('1734-01-01','1782-12-31',9),'Q67043':('1782-01-01','1802-11-05',9),'Q64086':('1714-03-27','1731-03-23',11),'Q552274':('1700-01-01','1713-07-31',11),'Q664223':('1747-11-28','1756-05-30',11),'Q361682':('1708-05-12','1752-12-11',11),'Q131981':('1727-06-11','1760-10-25',11)}

def research():
 r=read(ROOT/'.cache/rulers019-candidates.json');offices=read(ROOT/'.cache/historical-offices-019.json');accepted=[];rejected=[]
 for row in r['records']:
  q=row.get('person');key=row['key']
  if not row.get('human'):rejected.append(dict(candidate=row,reason='No verified human identity'));continue
  dates=row['parsed'][INDEX.get(q,0)] if row['parsed'] else dict(zip(['start','end','precision'],MISSING[q])) if q in MISSING else None
  if not dates:rejected.append(dict(candidate=row,reason='Reign/tenure not yet resolved'));continue
  a,b,precision=dates['start'],dates['end'],dates['precision'];note='Cargo soberano territorial; las dignidades posteriores se conservan separadas.'
  if q=='Q213610':a='1768-10-17';note+=' Sucesión tras LuisVIII; se rechaza el inicio divergente del12/10.'
  if q=='Q170179':b='1803-02-24';note+=' Título ducal anterior a su elevación electoral.'
  if q=='Q682701':b='1727-12-31';note+=' Ventana anterior a la suspensión imperial de1728; no se equipara la titularidad nominal posterior con poder efectivo.';precision=9
  if q=='Q213671':b='1771-10-20';note+=' Margraviato de Baden-Durlach antes de reunificar Baden.'
  if key=='HANOVER-ELECTORATE' and q=='Q372190':continue # died before1700
  if q=='Q213533':note+=' Minoría y regencia de AnaAmalia hasta1775, no un reinado personal adulto desde1758.'
  accepted.append(dict(key=key,term=dict(person=q,name=row['name'],role=row['role'],start=max(a,'1700-01-01'),end=min(b,'1806-12-19' if key=='SAXONY-ELECTORATE' else '1808-12-31' if key=='SAXE-WEIMAR' else '1806-12-31'),precision=precision,source=row['source'],curated=True,note=note,startIsCoverageBoundary=a<'1700-01-01' or a=='1700-01-01' or precision<11,endIsCoverageBoundary=b>'1806-12-31' or precision<11)))
  # Imperial office and hereditary Habsburg domains are different identities.
  if key=='HABSBURG-MONARCHY' and q!='Q131706':
   idx=1 if q=='Q76555' else 0;imperial=row['parsed'][idx]
   accepted.append(dict(key='HIST-Q12548',term=dict(person=q,name=row['name'],role='Emperador del Sacro Imperio',start=max('1700-01-01',imperial['start']),end=min('1799-12-31',imperial['end']),precision=imperial['precision'],source=row['source'],curated=True,note='Dignidad imperial distinta de las soberanías territoriales; no convierte los Estados miembros en un Estado nacional unitario.',startIsCoverageBoundary=imperial['start']<'1700-01-01',endIsCoverageBoundary=imperial['end']>'1799-12-31')))
 # Only office statements with explicit dates; country scope retained.
 titles={'PRUSSIA':'Rey de Prusia','JPN':'Shogun · Gobierno militar','QING':'Emperador Qing','JOS':'Rey de Joseon','PAPAL-STATES':'Papa · soberano de los Estados Pontificios','SAR':'Rey de Cerdeña','ETH':'Emperador de Etiopía','PRT':'Rey / reina de Portugal','SWE':'Rey / reina de Suecia','DNK':'Rey de Dinamarca y Noruega','IRN':'Shah de Persia'}
 for item in offices['records']:
  k=item['key'];l=copy.deepcopy(item['term'])
  if k in ['AUSTRIAN-EMPIRE','BRA-EMPIRE','GRC','NLD','BEL','TWO-SICILIES']:continue
  if k=='IRN':l['start']=max(l['start'],'1796-01-01')
  if l['start']>l['end']:continue
  l['role']=titles.get(k,l['role']);l['curated']=True
  accepted.append(dict(key=k,term=l))
 return dict(records=accepted,polities=r['entities'],rejected=rejected,source='Reviewed named reigns and explicit historical office statements; observations are not an exhaustive worldwide census.')

def prepare(incoming,r):
 d=copy.deepcopy(incoming);cs=d['countries'];images={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for c in r['polities']:cs.setdefault(c['key'],dict(qid=c['qid'],name=c['name'],leaders=[],flags=[]));cs[c['key']].update(qid=c['qid'],name=c['name'])
 for k,q in [('AFSHARID','Q388739'),('ZAND','Q97629053'),('THONBURI','Q1115291'),('SAVOY-DUCHY','Q426025')]:
  cs[k]['qid']=q;cs[k]['leaders']=[l for l in cs[k]['leaders'] if l.get('acquisition')!='historical-0.19']
 for row in r['records']:
  l=copy.deepcopy(row['term']);k=row['key'];l['acquisition']=TAG
  if l['start']>l['end']:continue
  if l['person'] in images:l['portrait']=images[l['person']]
  cs[k]['leaders']=[old for old in cs[k]['leaders'] if not(old.get('acquisition')=='historical-0.19' and old['person']==l['person'] and old['start']<=l['end'] and old['end']>=l['start'])]
  cs[k]['leaders'].append(l)
 return d

if __name__=='__main__':
 p=ROOT/'scripts/historical-offices-019-research.json';r=research() if '--research' in sys.argv or not p.exists() else read(p);save(p,r);old=read(OUT/'identities.json');d=prepare(old,r);assert prepare(d,r)==d
 for k,c in old['countries'].items():assert all(l in d['countries'][k]['leaders'] for l in c['leaders'] if l['end']>='1800-01-01' and l.get('acquisition') not in [TAG,'historical-0.19']),k
 save(OUT/'identities.json',d);print('Reviewed offices',len(r['records']),'polity identities',len(r['polities']),'rejected',len(r['rejected']),flush=True)
