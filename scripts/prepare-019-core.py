"""Explicit supplement to the frozen1700 review; no prior1800+ facts removed.

Run after prepare-1700-authorities. Calendar-ambiguous Russian source duplicates
are retained as annual observations, not fabricated Gregorian accession dates.
"""
import pathlib,json,copy,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('p',ROOT/'scripts/prepare-1700-authorities.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
read=p.read;save=p.save

def build():
 frozen=read(ROOT/'scripts/historical-offices-019-research.json');rows=[r for r in frozen['records'] if not r.get('core019')]
 candidates=read(ROOT/'.cache/core019-rulers.json') if (ROOT/'.cache/core019-rulers.json').exists() else frozen['coreCandidates'];selected={
  'FRA':[('Q7742',0),('Q7738',0)],'ESP':[('Q36174',0)],
  'PRT':[('Q156190',0),('Q299650',0),('Q1058391',0),('Q773874',0)],
  'ENGLAND':[('Q129987',0),('Q119702',0)],'GBR':[('Q119702',1),('Q130805',0),('Q127318',0)],
  'RUSSIA-TSARDOM':[('Q8479',1)],'SAFAVID':[('Q446965',0),('Q374516',0),('Q281336',0)],
  'AFSHARID':[('Q192868',0),('Q197881',0)],'ZAND':[('Q332583',0),('Q73103',0),('Q81023',0),('Q81098',0),('Q15859',0)],
  'IRN':[('Q175299',0)],'THONBURI':[('Q320097',0)],'THA':[('Q310992',0)],
  'POLISH-LITHUANIAN':[('Q53437',1),('Q53437',2),('Q53438',0),('Q54019',0)],
  'HIST-Q154849':[('Q47292',0),('Q256580',0)],
  'DENMARK-NORWAY':[('Q161059',0),('Q154993',0),('Q156187',0),('Q156572',0)],
  'DUTCH-REPUBLIC':[('Q129987',1),('Q380949',1),('Q312215',1)]}
 def add(k,q,name,role,a,b,source,precision=11,note=''):
  if a>'1799-12-31' or b<'1700-01-01':return
  rows.append(dict(core019=True,key=k,term=dict(person=q,name=name,role=role,start=max(a,'1700-01-01'),end=min(b,'1799-12-31'),precision=precision,source=source,curated=True,note=note,startIsCoverageBoundary=a<'1700-01-01' or precision<11,endIsCoverageBoundary=b>'1799-12-31' or precision<11)))
 for key,items in selected.items():
  for q,idx in items:
   row=next(r for r in candidates['records'] if r['key']==key and r.get('person')==q);dates=row['parsed'][idx];a,b=dates['start'],dates['end'];precision=dates['precision'];role=row['role'];note='Cargo histórico contrastado por su reinado; no derivado de una institución moderna.'
   if key=='GBR' and q=='Q119702':a='1707-05-01'
   if key=='ENGLAND' and q=='Q119702':b='1707-04-30'
   if key in ['ENGLAND','GBR'] and q!='Q127318':
    precision=9;note+=' Calendario británico anterior a1752: observación anual; no se convierte automáticamente una fecha de estilo antiguo a gregoriano.'
   if key=='ZAND' and q=='Q332583':role='Vakil · gobernante de Persia';note+=' Título de representante/regente; no se le atribuye el de shah.'
   if key=='SAFAVID':note+=' Reclamación dinástica; después de1722 no implica control continuo de Isfahán ni de toda Persia.'
   if key=='DUTCH-REPUBLIC':note+=' Estatúder, distinto de la soberanía de los Estados Generales; no monarca nacional.'
   add(key,q,row['name'],role,a,b,row['source'],precision,note)
 manual=[
  ('ESP','Q170467','Felipe V','Rey de España','1700-11-01','1724-01-14','Philip_V_of_Spain'),
  ('GBR','Q131981','Jorge II','Rey de Gran Bretaña','1727-01-01','1760-12-31','George_II_of_Great_Britain'),
  ('SCOTLAND','Q129987','Guillermo II','Rey de Escocia','1700-01-01','1702-12-31','William_III_of_England'),
  ('SCOTLAND','Q119702','Ana','Reina de Escocia','1702-01-01','1707-12-31','Anne,_Queen_of_Great_Britain'),
  ('POLISH-LITHUANIAN','Q54022','Estanislao I Leszczyński','Rey de Polonia · reinado disputado','1704-01-01','1709-12-31','Stanisław_Leszczyński'),
  ('POLISH-LITHUANIAN','Q54022','Estanislao I Leszczyński','Rey electo de Polonia · reclamación disputada','1733-01-01','1736-12-31','Stanisław_Leszczyński'),
  ('HIST-Q12548','Q76736','Carlos VII','Emperador del Sacro Imperio','1742-01-24','1745-01-20','Charles_VII,_Holy_Roman_Emperor'),
  ('HIST-Q157367','Q151826','Federico III','Elector de Brandeburgo y duque de Prusia','1688-04-29','1701-01-18','Frederick_I_of_Prussia'),
  ('IRN','Q324974','Agha Mohammad Khan','Shah Qajar','1796-01-01','1797-12-31','Agha_Mohammad_Khan_Qajar'),
  ('AFSHARID','Q197731','Ebrahim Afshar','Shah afshárida · reclamación rival','1748-01-01','1748-12-31','Ebrahim_Afshar'),
  ('AFSHARID','Q197884','Shahrokh','Shah afshárida · dominio regional en Jorasán','1748-01-01','1796-12-31','Shahrokh_Shah'),
 ]
 import urllib.parse
 for k,q,n,role,a,b,title in manual:add(k,q,n,role,a,b,'https://en.wikipedia.org/wiki/'+urllib.parse.quote(title),9 if k in ['GBR','SCOTLAND','IRN','AFSHARID','POLISH-LITHUANIAN'] else 11,'Ventana del cargo indicada; precisión anual cuando el día o el calendario no están contrastados. Los reinados rivales no implican control uniforme.')
 # Correct the Lippe title on promotion without inventing its exact day.
 for r in rows:
  if r['key']=='LIPPE-COUNTY' and r['term']['person']=='Q67043':r['term'].update(end='1788-12-31',endIsCoverageBoundary=True)
 add('HIST-Q14551680','Q67043','Leopoldo I','Príncipe de Lippe','1789-01-01','1802-11-05','https://en.wikipedia.org/wiki/Leopold_I,_Prince_of_Lippe',9,'Elevación principesca de1789; la fecha diaria no se supone.')
 frozen['records']=rows;frozen['coreCandidates']=candidates
 return frozen

if __name__=='__main__':
 file=ROOT/'scripts/historical-offices-019-research.json';r=build();save(file,r)
 file=ROOT/'public/data/identities.json';d=read(file)
 # Consolidate only the newly imported Russian calendar variants to honest
 # year-level observations, preserving their raw claims in the research record.
 russian=r.get('russianSourceClaims') or [l for l in d['countries']['RUE']['leaders'] if l.get('acquisition')=='historical-0.19']
 r['russianSourceClaims']=russian;save(ROOT/'scripts/historical-offices-019-research.json',r)
 d=p.prepare(d,r)
 for k in ['ESP','RUE']:
  if k=='ESP':d['countries'][k]['leaders']=[l for l in d['countries'][k]['leaders'] if not(l.get('acquisition')=='historical-0.19' and l['person']=='Q170467' and l['start']<'1724-01-01')]
  else:
   d['countries'][k]['leaders']=[l for l in d['countries'][k]['leaders'] if l.get('acquisition')!='historical-0.19']
   groups={}
   for l in russian:groups.setdefault((l['person'],l['role'],l['start'][:4],l['end'][:4]),l)
   for (_,_,a,b),raw in groups.items():
    l=copy.deepcopy(raw);l.update(start=a+'-01-01',end=b+'-12-31',precision=9,startIsCoverageBoundary=True,endIsCoverageBoundary=True,note='Observación anual del reinado. Las declaraciones de origen ofrecen variantes de calendario; no se publican como días gregorianos de acceso/cese.');d['countries'][k]['leaders'].append(l)
 save(file,d);print('Frozen reviewed intervals',len(r['records']),'Russian observations',len(groups))
