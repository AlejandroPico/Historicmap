"""Isolated1700–1799 acquisition; existing1800+ statements and symbols preserved."""
import copy,pathlib,json,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('previous',ROOT/'scripts/enrich-1800-authorities.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
FIRST,LAST,TAG='1700-01-01','1799-12-31','historical-0.19'
SEEDS={**p.SEEDS,'RUSSIA-TSARDOM':('Q186096','Zarato de Rusia'),'ENGLAND':('Q179876','Reino de Inglaterra'),'SCOTLAND':('Q230791','Reino de Escocia'),'DENMARK-NORWAY':('Q62651','Dinamarca-Noruega'),'SAFAVID':('Q161205','Persia safávida'),'AFSHARID':('Q388739','Persia afshárida'),'ZAND':('Q97629053','Persia zand'),'AYUTTHAYA':('Q841364','Reino de Ayutthaya'),'THONBURI':('Q1115291','Reino de Thonburi'),'DUTCH-REPUBLIC':('Q170072','República de las Provincias Unidas'),'POLISH-LITHUANIAN':('Q172107','Mancomunidad de Polonia-Lituania'),'SAVOY-DUCHY':('Q426025','Ducado de Saboya')}
read=lambda f:json.loads(f.read_text(encoding='utf8'))
if __name__=='__main__':
 current=read(ROOT/'public/data/identities.json');data=copy.deepcopy(current);qids={c['qid'] for c in data['countries'].values()}
 for key,(q,name) in SEEDS.items():data['countries'].setdefault(key,dict(qid=q,name=name,leaders=[],flags=[]));qids.add(q)
 excluded={'Q3037','Q1514510','Q382593','Q66504140','Q46652','Q201705','Q148540','Q4807130','Q28405'}
 for file in ['early-modern-1700.geojson','early-modern.geojson']:
  for f in read(ROOT/'public/data'/file)['features']:
   v=f['properties'];q=v.get('wikidata','')
   if v['start']>1799 or v['end']<1700 or not q.startswith('Q') or q in qids or q in excluded:continue
   data['countries'].setdefault('HIST-'+q,dict(qid=q,name=v['name'],leaders=[],flags=[]));qids.add(q)
 staging=ROOT/'.cache/acquire-1700/public'
 for folder in ['data','media']:(staging/folder).mkdir(parents=True,exist_ok=True)
 h.save(staging/'data/identities.json',data);h.save(staging/'media/manifest.json',read(ROOT/'public/media/manifest.json'));h.OUT=staging;h.START=FIRST;h.PERIOD_END=LAST;h.ACQUISITION=TAG
 # Separate historical states rather than projecting modern institutions backwards.
 h.LIFETIMES.update({'PRUSSIA':('1701-01-18','1918-11-09'),'RUSSIA-TSARDOM':('1547-01-16','1721-11-01'),'RUE':('1721-11-02','1917-03-15'),'AUSTRIAN-EMPIRE':('1804-08-11','1867-05-28'),'AUT-HUN':('1867-05-29','1918-11-12'),'BRA-EMPIRE':('1822-09-07','1889-11-14'),'ENGLAND':('927-01-01','1707-04-30'),'SCOTLAND':('843-01-01','1707-04-30'),'SAFAVID':('1501-01-01','1736-12-31'),'AFSHARID':('1736-01-01','1796-12-31'),'ZAND':('1751-01-01','1794-12-31'),'AYUTTHAYA':('1351-01-01','1767-12-31'),'THONBURI':('1767-01-01','1782-12-31'),'SAR':('1720-01-01','1861-03-16'),'JOS':('1392-01-01','1897-10-11'),'QING':('1644-01-01','1912-02-12'),'HAW-KINGDOM':('1795-01-01','1893-01-17')})
 h.acquire(skip_media=True)
 staged=read(staging/'data/identities.json');result=copy.deepcopy(current);images={l['person']:l['portrait'] for c in current['countries'].values() for l in c['leaders'] if l.get('portrait')}
 for c in result['countries'].values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for key,c in staged['countries'].items():
  target=result['countries'].setdefault(key,dict(qid=c['qid'],name=c['name'],leaders=[],flags=[]))
  for old in c['leaders']:
   if old.get('acquisition')!=TAG or old['start']>LAST or old['end']<FIRST:continue
   l=copy.deepcopy(old);l.update(start=max(FIRST,l['start']),end=min(LAST,l['end']))
   if l['start']!=old['start']:l.update(startIsCoverageBoundary=True,sourceStart=old['start'])
   if l['end']!=old['end']:l.update(endIsCoverageBoundary=True,sourceEnd=old['end'])
   if l['person'] in images:l['portrait']=images[l['person']]
   target['leaders'].append(l)
 for k,c in current['countries'].items():
  assert all(l in result['countries'][k]['leaders'] for l in c['leaders'] if l['end']>='1800-01-01'),k
  assert result['countries'][k]['flags']==c['flags'],k
 h.save(ROOT/'public/data/identities.json',result);print('Merged1700–1799; all pre-existing1800+ authorities and flags preserved.',flush=True)
