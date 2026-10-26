"""Isolated source-polity acquisition1400–1499; preserve all previously shipped facts."""
import pathlib,json,copy,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('previous',ROOT/'scripts/enrich-1700-authorities.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p);h=p.h
FIRST,LAST,TAG='1400-01-01','1499-12-31','historical-0.22'
SEEDS={**p.SEEDS,'MING':('Q9903','Imperio Ming'),'SOUTHERN-MING':('Q1198163','Ming del Sur'),'LATER-JIN':('Q1062546','Jin posterior · Estado manchú'),'ENGLISH-COMMONWEALTH':('Q330362','Commonwealth de Inglaterra'),'SAADI':('Q1136188','Sultanato saadí'),'ELECTORATE-BRANDENBURG':('Q148499','Electorado de Brandeburgo'),'BAVARIA-DUCHY':('Q47261','Ducado de Baviera'),'PRUSSIA-DUCHY':('Q153091','Ducado de Prusia')}
SEEDS.update({'CASTILE':('Q217196','Corona de Castilla'),'ARAGON':('Q204920','Corona de Aragón'),'MUSCOVY':('Q170770','Gran Principado de Moscú'),'AZTEC':('Q2608489','Triple Alianza mexica'),'INCA':('Q28573','Imperio inca'),'SUR':('Q373650','Imperio surí'),'KALMAR':('Q62623','Unión de Kalmar'),'WATTASID':('Q970799','Sultanato wattasí'),'MAMLUKS':('Q282428','Sultanato mameluco'),'LODI':('Q11709','Sultanato de Delhi · dinastía Lodi'),'TIMURID':('Q484195','Dominios timúridas'),'JAGIELLON-DOMAINS':('Q194355','Dominios jagellones · agregado de fuente'),'HUNGARY-KINGDOM':('Q171150','Reino de Hungría'),'EAST-HUNGARY':('Q625380','Reino húngaro oriental'),'BOHEMIA':('Q42585','Reino de Bohemia')})
SEEDS.update({'BYZANTINE':('Q12544','Imperio bizantino'),'TREBIZOND':('Q178913','Imperio de Trebisonda'),'GRANADA-EMIRATE':('Q238445','Emirato de Granada'),'BURGUNDY-DUCHY':('Q4712','Ducado de Borgoña'),'NAVARRE-KINGDOM':('Q200262','Reino de Navarra'),'LITHUANIA-DUCHY':('Q49683','Gran Ducado de Lituania'),'MARINID':('Q582861','Sultanato meriní')})
read=lambda p:json.loads(p.read_text(encoding='utf8'))
if __name__=='__main__':
 current=read(ROOT/'public/data/identities.json');cs=copy.deepcopy(current['countries']);source=read(ROOT/'public/data/early-modern-1400.geojson');qs={f['properties']['wikidata'] for f in source['features']};active={}
 excluded={'Q3037','Q382593','Q66504140','Q201705','Q148540','Q4807130','Q28405','Q333567','Q200229','Q58389','Q65968','Q112039853','Q6000379','Q122293','Q155594','Q168352','Q1716871','Q149846','Q13695','Q1178043','Q703919','Q2288','Q83546'}
 for key,c in cs.items():
  if c['qid'] in qs and c['qid'] not in excluded:active[key]=c
 for key,(q,name) in SEEDS.items():
  if q in qs or key in ['BYZANTINE','POLAND-KINGDOM','HABSBURG-MONARCHY','JOS','PAPAL-STATES','SAVOY-DUCHY']:
   active[key]=cs.get(key,dict(qid=q,name=name,leaders=[],flags=[]))
 for f in source['features']:
  v=f['properties'];q=v['wikidata']
  if q.startswith('Q') and q not in excluded and q not in {c['qid'] for c in active.values()}:active['HIST-'+q]=dict(qid=q,name=v['name'],leaders=[],flags=[])
 # Explicit corrected states and shared national rulers, without modern institutions.
 for k in ['SAH','MAR','FRA','ESP','PRT','ENGLAND','SCOTLAND','HABSBURG-MONARCHY','PAPAL-STATES','JOS','JPN','QING','RUSSIA-TSARDOM','DUTCH-REPUBLIC','DENMARK-NORWAY','SAFAVID','POLISH-LITHUANIAN','SAVOY-DUCHY']:
  if k in cs:active[k]=cs[k]
 staging=ROOT/'.cache/acquire-1400/public'
 for folder in ['data','media']:(staging/folder).mkdir(parents=True,exist_ok=True)
 h.save(staging/'data/identities.json',{**current,'countries':active});h.save(staging/'media/manifest.json',read(ROOT/'public/media/manifest.json'));h.OUT=staging;h.START=FIRST;h.PERIOD_END=LAST;h.ACQUISITION=TAG
 h.LIFETIMES.update({'MING':('1368-01-01','1644-12-31'),'SOUTHERN-MING':('1644-01-01','1662-12-31'),'LATER-JIN':('1616-01-01','1635-12-31'),'QING':('1636-01-01','1912-02-12'),'PRUSSIA':('1701-01-18','1918-11-09'),'RUE':('1721-11-02','1917-03-15'),'RUSSIA-TSARDOM':('1547-01-01','1721-11-01'),'ENGLISH-COMMONWEALTH':('1649-01-01','1660-12-31'),'SAADI':('1510-01-01','1659-12-31'),'MAR':('1666-01-01','9999-12-31'),'HIST-Q83618':('1674-01-01','1818-12-31')})
 h.LIFETIMES.update({'MUSCOVY':('1283-01-01','1546-12-31'),'AZTEC':('1428-01-01','1521-12-31'),'INCA':('1438-01-01','1533-12-31'),'SUR':('1540-01-01','1556-12-31'),'WATTASID':('1472-01-01','1554-12-31'),'MAMLUKS':('1250-01-01','1517-12-31'),'LODI':('1451-01-01','1526-12-31'),'TIMURID':('1370-01-01','1507-12-31'),'KALMAR':('1397-01-01','1523-12-31'),'POLISH-LITHUANIAN':('1569-01-01','1795-12-31'),'HIST-Q33296':('1526-01-01','1857-12-31'),'SAFAVID':('1501-01-01','1736-12-31'),'DUTCH-REPUBLIC':('1579-01-01','1795-12-31'),'HIST-Q521263':('1642-01-01','9999-12-31')})
 h.LIFETIMES.update({'BYZANTINE':('1261-01-01','1453-05-29'),'TREBIZOND':('1204-01-01','1461-12-31'),'GRANADA-EMIRATE':('1238-01-01','1492-01-02'),'MARINID':('1244-01-01','1465-12-31'),'HIST-Q157367':('1618-01-01','1701-01-17'),'ESP':('1516-01-01','9999-12-31')})
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
 h.save(ROOT/'public/data/identities.json',result);print('Merged1400–1499; every prior authority fact and symbol preserved.',flush=True)
