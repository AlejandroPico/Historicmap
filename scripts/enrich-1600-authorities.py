"""Isolated source-polity acquisition1600–1699; preserve all previously shipped facts."""
import pathlib,json,copy,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('previous',ROOT/'scripts/enrich-1700-authorities.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p);h=p.h
FIRST,LAST,TAG='1600-01-01','1699-12-31','historical-0.20'
SEEDS={**p.SEEDS,'MING':('Q9903','Imperio Ming'),'SOUTHERN-MING':('Q1198163','Ming del Sur'),'LATER-JIN':('Q1062546','Jin posterior · Estado manchú'),'ENGLISH-COMMONWEALTH':('Q330362','Commonwealth de Inglaterra'),'SAADI':('Q1136188','Sultanato saadí'),'ELECTORATE-BRANDENBURG':('Q148499','Electorado de Brandeburgo'),'BAVARIA-DUCHY':('Q47261','Ducado de Baviera'),'PRUSSIA-DUCHY':('Q153091','Ducado de Prusia')}
read=lambda p:json.loads(p.read_text(encoding='utf8'))
if __name__=='__main__':
 current=read(ROOT/'public/data/identities.json');cs=copy.deepcopy(current['countries']);source=read(ROOT/'public/data/early-modern-1600.geojson');qs={f['properties']['wikidata'] for f in source['features']};active={}
 excluded={'Q3037','Q1514510','Q382593','Q66504140','Q46652','Q201705','Q148540','Q4807130','Q28405','Q333567','Q200229'}
 for key,c in cs.items():
  if c['qid'] in qs and c['qid'] not in excluded:active[key]=c
 for key,(q,name) in SEEDS.items():
  if q in qs or key in ['HABSBURG-MONARCHY','JOS','PAPAL-STATES','SAVOY-DUCHY','HIST-Q157367']:
   active[key]=cs.get(key,dict(qid=q,name=name,leaders=[],flags=[]))
 for f in source['features']:
  v=f['properties'];q=v['wikidata']
  if q.startswith('Q') and q not in excluded and q not in {c['qid'] for c in active.values()}:active['HIST-'+q]=dict(qid=q,name=v['name'],leaders=[],flags=[])
 # Explicit corrected states and shared national rulers, without modern institutions.
 for k in ['SAH','MAR','FRA','ESP','PRT','ENGLAND','SCOTLAND','HABSBURG-MONARCHY','PAPAL-STATES','JOS','JPN','QING','RUSSIA-TSARDOM','DUTCH-REPUBLIC','DENMARK-NORWAY','SAFAVID','POLISH-LITHUANIAN','SAVOY-DUCHY']:
  if k in cs:active[k]=cs[k]
 staging=ROOT/'.cache/acquire-1600/public'
 for folder in ['data','media']:(staging/folder).mkdir(parents=True,exist_ok=True)
 h.save(staging/'data/identities.json',{**current,'countries':active});h.save(staging/'media/manifest.json',read(ROOT/'public/media/manifest.json'));h.OUT=staging;h.START=FIRST;h.PERIOD_END=LAST;h.ACQUISITION=TAG
 h.LIFETIMES.update({'MING':('1368-01-01','1644-12-31'),'SOUTHERN-MING':('1644-01-01','1662-12-31'),'LATER-JIN':('1616-01-01','1635-12-31'),'QING':('1636-01-01','1912-02-12'),'PRUSSIA':('1701-01-18','1918-11-09'),'RUE':('1721-11-02','1917-03-15'),'RUSSIA-TSARDOM':('1547-01-01','1721-11-01'),'ENGLISH-COMMONWEALTH':('1649-01-01','1660-12-31'),'SAADI':('1549-01-01','1659-12-31'),'MAR':('1666-01-01','9999-12-31'),'HIST-Q83618':('1674-01-01','1818-12-31')})
 print('Acquiring only active/corrected polity catalogues',len(active),flush=True);h.acquire(skip_media=True)
 acquired=read(staging/'data/identities.json');result=copy.deepcopy(current);images={l['person']:l['portrait'] for c in current['countries'].values() for l in c['leaders'] if l.get('portrait')}
 for c in result['countries'].values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for k,c in acquired['countries'].items():
  target=result['countries'].setdefault(k,dict(qid=c['qid'],name=c['name'],leaders=[],flags=[]))
  for old in c['leaders']:
   if old.get('acquisition')!=TAG or old['start']>LAST or old['end']<FIRST:continue
   l=copy.deepcopy(old);l.update(start=max(FIRST,l['start']),end=min(LAST,l['end']))
   if l['start']!=old['start']:l.update(startIsCoverageBoundary=True,sourceStart=old['start'])
   if l['end']!=old['end']:l.update(endIsCoverageBoundary=True,sourceEnd=old['end'])
   if l['person'] in images:l['portrait']=images[l['person']]
   target['leaders'].append(l)
 for k,c in current['countries'].items():
  assert all(l in result['countries'][k]['leaders'] for l in c['leaders'] if l.get('acquisition')!=TAG),k
  assert c['flags']==result['countries'][k]['flags'],k
 h.save(ROOT/'public/data/identities.json',result);print('Merged1600–1699; every prior authority fact and symbol preserved.',flush=True)
