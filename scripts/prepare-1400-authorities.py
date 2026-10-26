"""Frozen reviewed offices1400–1499, with explicit calendars and scope."""
import pathlib,json,copy,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1400-0.22'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
INDICES={('HIST-Q12548','Q152148'):1,('HIST-Q12548','Q57124'):1,('HIST-Q12548','Q157112'):2,('HIST-Q12548','Q150966'):1,('HIST-Q12548','Q150726'):1,('POLAND-KINGDOM','Q53459'):1,('NAVARRE-KINGDOM','Q312328'):2,('SAVOY-DUCHY','Q312636'):1}
MANUAL={
 ('FRA','Q8058'):[('1461-07-22','1483-08-30')],
 ('ENGLAND','Q160337'):[('1422-09-01','1461-03-04'),('1470-10-03','1471-04-11')],
 ('ENGLAND','Q160341'):[('1461-03-04','1470-10-03'),('1471-04-11','1483-04-09')],
 ('OTT','Q131394'):[('1421-05-26','1444-08-31'),('1446-09-01','1451-02-03')],
 ('OTT','Q34503'):[('1444-08-01','1446-09-30'),('1451-02-03','1481-05-03')],
 ('MING','Q9983'):[('1435-01-31','1449-09-22'),('1457-02-11','1464-02-23')],
 ('KALMAR','Q161958'):[('1400-01-01','1439-12-31')],
 ('AZTEC','Q351751'):[('1469-01-01','1481-12-31')],('AZTEC','Q336816'):[('1481-01-01','1486-12-31')],('AZTEC','Q351758'):[('1486-01-01','1502-12-31')],
 ('INCA','Q213758'):[('1438-01-01','1471-12-31')],('TIMURID','Q1192519'):[('1451-01-01','1469-12-31')],
 ('JPN','Q466287'):[('1394-01-01','1423-12-31')],('JPN','Q465901'):[('1423-01-01','1425-12-31')],('JPN','Q239170'):[('1429-01-01','1441-12-31')],('JPN','Q455351'):[('1442-01-01','1443-12-31')],('JPN','Q447034'):[('1449-01-01','1473-12-31')],('JPN','Q447639'):[('1474-01-01','1489-12-31')],('JPN','Q708527'):[('1490-01-01','1493-12-31')],('JPN','Q466281'):[('1494-01-01','1508-12-31')],
 ('WURTTEMBERG-DUCHY','Q61671'):[('1498-01-01','1519-12-31')],
 ('ETH','Q713338'):[('1478-11-08','1494-05-07')],
 ('OTT','Q1095044'):[('1402-01-01','1411-12-31')],('OTT','Q1095287'):[('1411-01-01','1413-12-31')],('OTT','Q1085744'):[('1402-01-01','1403-12-31')]}

def research():
 base=read(ROOT/'.cache/rulers022-candidates.json');evidence=read(ROOT/'.cache/rulers022-office-evidence.json');extra=[v['candidate'] for v in evidence if v['candidate']['title'] not in {r['title'] for r in base['records']}];accepted=[];rejected=[]
 def add(k,q,name,role,a,b,source,note=''):
  if a>'1499-12-31' or b<'1400-01-01':return
  if len(a)==4:a+='-01-01'
  if len(b)==4:b+='-12-31'
  text=lambda s:re.sub(r'(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])',' ',s)
  accepted.append(dict(key=k,term=dict(person=q,name=text(name),role=text(role),start=max(a,'1400-01-01'),end=min(b,'1499-12-31'),precision=9,source=source,curated=True,note=text(note+' Observación anual; calendario histórico y control regional no acreditados día a día.'),startIsCoverageBoundary=True,endIsCoverageBoundary=True)))
 def note(k,q):
  n='La titularidad no acredita control uniforme de toda la geometría de fuente.'
  if k=='HIST-Q12548':n+=' La monarquía deRomanos se distingue de la coronación imperial. Segismundo es emperador desde1433,Federico desde1452; AlbertoII yMaximiliano antes de1508 no son emperadores coronados. Los miembros conservan soberanías propias.'
  if k=='BYZANTINE':n+='Constantinopla cae en1453; no se prolonga un emperador sobreTrebisonda o elPeloponeso después de esa fecha.'
  if k=='BURGUNDY-DUCHY':n+='El ducado francés es ocupado en1477; los otros dominios borgoñones y las reclamaciones dinásticas no prueban continuidad de control en el ducado.'
  if k=='KALMAR':n+='Unión disputada; las regencias y reinados deSuecia,Noruega yDinamarca no coinciden en todos los años.'
  if k=='SAXONY-ELECTORATE':n+='Cambio de dinastía en1423 y partición deLeipzig en1485; el elector no es soberano de todos los dominios sajones.'
  if k in ['POLAND-KINGDOM','LITHUANIA-DUCHY']:n+='Corona polaca y gran ducado tienen cargos e intervalos distintos; no se anticipa la unión deLublin de1569.'
  if k=='MUSCOVY':n+='Guerra sucesoria y pretendientes durante el reinado deBasilioII; no se afirma un control personal continuo sin rivales.'
  if k=='TIMURID':n+='Ámbito timúrida regional y sucesión disputada; la rama deHerat no controla automáticamente todos los dominios deTimur.'
  if k=='JPN':n+='Emperador,shogun y dirigentes retirados son funciones distintas. No se confunde la sucesión nominal con unificación de todos los dominios.'
  if k=='INCA':n+='Cronología tradicional Rowe/Pachacuti1438–1471; existen dataciones alternativas y debate arqueológico, no fechas absolutas indiscutidas.'
  if k=='AZTEC':n+='Gobierno mexica en una alianza de ciudades y tributos; no un Estado nacional moderno de soberanía uniforme.'
  if k=='PAPAL-STATES':n+='Cargo pontificio, no cardenalicio. ElCisma deOccidente incluye obediencias rivales; no se afirma que un papa controle toda la geometría o toda la cristiandad.'
  if k=='OTT' and q in ['Q1095044','Q1095287','Q1085744']:n+='Interregno otomano: poder regional y pretensión rival, no sultanato unificado. Ventanas anuales orientativas; no una certificación diaria del gobierno.'
  return n
 for row in base['records']+extra:
  q=row.get('person');k=row['key'];role=row['role']
  if not row.get('human'):rejected.append(dict(candidate=row,reason='Not a verified human or unresolved canonical article'));continue
  ev=next((v for v in evidence if v['candidate'].get('person')==q),dict(claims=[],fields=[]));dates=MANUAL.get((k,q))
  if not dates and row['parsed']:
   p=row['parsed'][INDICES.get((k,q),0)];dates=[(p['start'],p['end'])]
   if k=='PRT' and q in ['Q299119','Q217637']:dates=[(p['start'],p['end']) for p in row['parsed']]
  if k=='PAPAL-STATES':dates=[(v['start'],v['end']) for v in ev['claims'] if v['office']=='Q19546']
  if not dates:
   patterns={'SAXONY-ELECTORATE':'elector de Sajonia','ELECTORATE-BRANDENBURG':'elector de Brandeburgo','MUSCOVY':'Príncipe Moscovita|Sovereign of all Russia','ETH':'Emperador de Etiopía','GRANADA-EMIRATE':'sultán de Granada','WURTTEMBERG-DUCHY':'Duque de Württemberg','HESSE-UNITED':'Landgrave|landgrave','SAVOY-DUCHY':'Duke of Savoy|duque de Saboya|Duque de Saboya'}
   pattern=patterns.get(k);dates=[(c['start'],c['end'][:4]+'-12-31' if c['precision']<11 else c['end']) for c in ev['claims'] if pattern and re.search(pattern,c.get('label',''),re.I)]
  if not dates:rejected.append(dict(candidate=row,reason='Office dates unresolved; no interpolation from life dates'));continue
  if k=='HIST-Q12548':role='Rey de Romanos / dignidad imperial fechada'
  if k=='SAVOY-DUCHY' and q=='Q312636':
   add('SAVOY-COUNTY',q,row['name'],'Conde de Saboya','1400-01-01','1415-12-31',row['source'],'Elevación a ducado en1416, no antes.')
  for a,b in dates:
   if k=='SAVOY-DUCHY':a=max(a,'1416-01-01')
   if k=='AZTEC':a=max(a,'1428-01-01')
   add(k,q,row['name'],role,a,b,row['source'],note(k,q))
  # Exact offices in the union, never the entire Danish reign projected toSweden.
  if k=='KALMAR':
   for c in ev['claims']:
    target='SWE' if 'Suecia' in c.get('label','') else 'NORWAY-KINGDOM' if 'Noruega' in c.get('label','') else 'DNK' if 'Dinamarca' in c.get('label','') else None
    if target:add(target,q,row['name'],c['label'],c['start'],c['end'][:4]+'-12-31' if c['precision']<11 else c['end'],row['source'],'Cargo de esta corona; no implica los mismos años en los otros miembros de la unión.')
 corrections=read(ROOT/'.cache/people022-corrections.json')
 for k,q,role,dates,source in [
  ('ELECTORATE-BRANDENBURG','Q61336','Elector de Brandeburgo',[('1415-01-01','1440-12-31')],'https://ikmk.smb.museum/ndp/person/656'),
  ('SAVOY-DUCHY','Q373236','Duque de Saboya',[('1465-01-01','1472-12-31')],'https://www.wikidata.org/wiki/Q373236'),
  ('GRANADA-EMIRATE','Q335624','Emir nazarí · reinados separados',[('1464-01-01','1482-12-31'),('1483-01-01','1485-12-31')],'https://www.wikidata.org/wiki/Q335624'),
  ('GRANADA-EMIRATE','Q312763','Emir nazarí · Boabdil',[('1482-01-01','1483-12-31'),('1487-01-01','1492-01-02')],'https://en.wikipedia.org/wiki/Boabdil')]:
  e=corrections['entities'][q];assert any(c.get('mainsnak',{}).get('datavalue',{}).get('value',{}).get('id')=='Q5' for c in e['claims'].get('P31',[]));name=e.get('labels',{}).get('es',e['labels'].get('en'))['value']
  for a,b in dates:add(k,q,name,role,a,b,source,'Identidad humana contrastada de forma independiente ante variantes de título o redirecciones. '+note(k,q))
 return dict(records=accepted,rejected=rejected,candidates=base,evidence=evidence,identityCorrections=corrections,polityEvidence=read(ROOT/'.cache/polities022-verified.json'),scope='Partial reviewed office inventory; annual calendar precision, not certification of all source boundaries.')

def prepare(old,research):
 d=copy.deepcopy(old);cs=d['countries'];images={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for k,q,n in [('SAVOY-COUNTY','Q1232887','Condado de Saboya'),('NORWAY-KINGDOM','Q2196956','Reino de Noruega'),('URGELL-COUNTY','Q1514510','Condado de Urgell'),('TENOCHTITLAN','Q13695','México-Tenochtitlan'),('CUSCO-KINGDOM','Q5582862','Reino de Cusco'),('LUXEMBOURG-DOMAINS','','Dominios de Luxemburgo · agregado'),('OLDENBURG-DOMAINS','','Dominios de Oldemburgo · agregado'),('ASCANIA-DOMAINS','','Dominios ascanios · agregado'),('VALOIS-ANJOU-DOMAINS','','Dominios Valois-Anjou · agregado'),('TOCCO-DOMAINS','','Dominios de Tocco · agregado'),('UNRESOLVED-ARAB-SOURCE','','Territorio árabe · referencia sin resolver'),('UNRESOLVED-VIET-SOURCE','','Territorio vietnamita · referencia sin resolver')]:cs.setdefault(k,dict(qid=q,name=n,leaders=[],flags=[]))
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for row in research['records']:
  k=row['key'];l=copy.deepcopy(row['term']);l['acquisition']=TAG
  if l['person'] in images:l['portrait']=images[l['person']]
  cs[k]['leaders']=[o for o in cs[k]['leaders'] if not(o.get('acquisition')=='historical-0.22' and o['person']==l['person'] and o['start']<=l['end'] and o['end']>=l['start'])];cs[k]['leaders'].append(l)
 return d
if __name__=='__main__':
 p=ROOT/'scripts/historical-offices-022-research.json';rs=research() if not p.exists() or '--research' in sys.argv else read(p);save(p,rs);old=read(OUT/'identities.json');d=prepare(old,rs);assert prepare(d,rs)==d
 for k,c in old['countries'].items():assert all(l in d['countries'][k]['leaders'] for l in c['leaders'] if l.get('acquisition') not in [TAG,'historical-0.22']),k
 save(OUT/'identities.json',d);print('Reviewed office intervals',len(rs['records']),'rejected/unresolved',len(rs['rejected']))
