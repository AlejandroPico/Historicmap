"""Reviewed sixteenth-century offices; frozen evidence, no inferred reigns.

Source-coordinate coverage is not the ruler's actual extent of control. Years
with uncertain calendars/dates remain annual observations. Earlier facts stay.
"""
import pathlib,json,copy,re,sys,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1500-0.21'
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-018-german-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
INDICES={('PRT','Q34417'):1,('HIST-Q12548','Q150726'):1,('PRUSSIA-DUCHY','Q40433'):1,('NEO-INCA','Q332049'):0,('INCA','Q332049'):1}
MANUAL={
 ('CASTILE','Q157098'):('1506-07-12','1506-09-25',11),
 ('HIST-Q12548','Q32500'):('1519-01-01','1556-12-31',9),
 ('ENGLAND','Q38370'):('1509-01-01','1547-12-31',9),
 ('BAVARIA-DUCHY','Q60942'):('1500-01-01','1508-12-31',9),
 ('BAVARIA-DUCHY','Q61496'):('1516-01-01','1545-12-31',9),
 ('BAVARIA-DUCHY','Q60568'):('1579-01-01','1597-12-31',9),
 ('HESSE-UNITED','Q567043'):('1500-01-01','1509-12-31',9),
 ('HESSE-KASSEL','Q696040'):('1567-01-01','1592-12-31',9),
 ('AZTEC','Q351758'):('1486-01-01','1502-12-31',9),
 ('AZTEC','Q141791'):('1502-01-01','1520-12-31',9),
 ('AZTEC','Q315628'):('1520-01-01','1520-12-31',9),
 ('AZTEC','Q297050'):('1521-01-01','1521-08-13',9),
 ('HIST-Q796583','Q383455'):('1509-01-01','1543-12-31',9),
 ('HIST-Q796583','Q2412791'):('1543-01-01','1545-12-31',9),
 ('HIST-Q796583','Q3084933'):('1545-01-01','1545-12-31',9),
 ('HIST-Q796583','Q2839850'):('1561-01-01','1561-12-31',9),
 ('HIST-Q796583','Q2709636'):('1561-01-01','1567-12-31',9),
 ('HIST-Q796583','Q3010364'):('1567-01-01','1568-12-31',9),
 ('HIST-Q796583','Q2840568'):('1568-01-01','1587-12-31',9),
 ('HIST-Q796583','Q2840566'):('1587-01-01','1614-12-31',9),
 ('SUR','Q167184'):('1554-11-22','1554-11-25',11)}

def research():
 candidates=read(ROOT/'.cache/rulers021-candidates.json');extra=read(ROOT/'.cache/rulers021-extra.json');additional=read(ROOT/'.cache/rulers021-office-evidence.json');accepted=[];rejected=[]
 def add(k,q,name,role,a,b,p,source,note=''):
  if a>'1599-12-31' or b<'1500-01-01':return
  accepted.append(dict(key=k,term=dict(person=q,name=name,role=role,start=max(a,'1500-01-01'),end=min(b,'1599-12-31'),precision=p,source=source,curated=True,note=note or 'Cargo fechado; la titularidad no acredita control uniforme de toda la geometría de fuente.',startIsCoverageBoundary=a<'1500-01-01' or p<11,endIsCoverageBoundary=b>='1599-12-31' or p<11)))
 for row in candidates['records']:
  q=row.get('person');k=row['key'];role=row['role'];note=''
  if not row.get('human'):rejected.append(dict(candidate=row,reason='Not a verified human; homonym/disambiguation rejected'));continue
  if (k,q) in [('WURTTEMBERG-DUCHY','Q61671'),('HIST-Q33296','Q486188'),('JPN','Q187550'),('JPN','Q171411')]:continue # Explicitly split offices below.
  dates=MANUAL.get((k,q))
  if not dates and row['parsed']:
   v=row['parsed'][INDICES.get((k,q),0)];dates=(v['start'],v['end'],v['precision'])
  if not dates:rejected.append(dict(candidate=row,reason='Office interval unresolved; candidate not published'));continue
  a,b,p=dates
  if k in ['ENGLAND','SCOTLAND','MUSCOVY','RUSSIA-TSARDOM','JPN','MING','JOS','HIST-Q12548','SAXONY-ELECTORATE','BAVARIA-DUCHY','HESSE-UNITED','HESSE-KASSEL','HESSE-DARMSTADT','WURTTEMBERG-DUCHY','ELECTORATE-BRANDENBURG','PRUSSIA-DUCHY']:p=9;note='Observación anual; conversión de calendarios históricos no acreditada día a día. '
  if k=='HIST-Q12548':note+='Dignidad imperial distinta de la soberanía territorial de cada Estado miembro. En1500 Maximiliano es rey deRomanos; el título de emperador electo comienza en1508.';role='Rey de Romanos / emperador electo' if q=='Q150726' else role
  if k=='HIST-Q12548' and q=='Q150611':note+=' Abdicación deCarlosV en1556; reconocimiento imperial deFernando en1558.'
  if k=='CASTILE' and q=='Q171136':note+='Reina titular; regencias y co-reinado se muestran por separado. No se presume gobierno personal continuo.'
  if k=='CASTILE' and q=='Q32500':role='Carlos I · co-rey de Castilla';note+='Co-reinado conJuanaI hasta1555.'
  if k=='ARAGON' and q=='Q32500':role='Carlos I · rey de Aragón';note+='Las coronas conservan instituciones distintas.'
  if k=='PRT' and q=='Q34417':role='Felipe I de Portugal · unión dinástica';note+='Misma persona queFelipeIIdeEspaña; administraciones distintas.'
  if k=='PRT' and q=='Q34464':role='Felipe II de Portugal · unión dinástica'
  if k=='SAXONY-ELECTORATE':note+='La dignidad electoral pasa de la rama ernestina a la albertina en1547.'
  if k=='BAVARIA-DUCHY' and q=='Q60942':note+='Duque deBaviera-Múnich antes de la reunificación de1505; no todaBaviera desde1500.'
  if k=='BAVARIA-DUCHY' and q=='Q61496':role='Duque de Baviera · co-gobierno regional'
  if k=='ENGLAND' and q=='Q162356':role='Reina proclamada · sucesión disputada';note+='Nueve días de1553; no gobierno anual exclusivo.'
  if k=='AZTEC':note+='Autoridad mexica en una alianza tributaria, no un Estado nacional moderno. La caída deTenochtitlan en1521 limita el control; no se prolonga hasta la ejecución deCuauhtémoc en1525.'
  if k=='INCA':note+='Cronología anual con dataciones debatidas y guerra sucesoria; no acredita un único control efectivo de todo el contorno.'
  if k=='INCA' and q=='Q332049':b='1536-12-31';note+='El reino resistente deVilcabamba desde1537 se registra aparte.'
  if k=='NEO-INCA':note+='Reino resistente deVilcabamba; no se le atribuye todo el antiguo imperio ni el virreinato colonial.'
  if k=='HIST-Q796583' and q=='Q383455':note+='Fin datado entre1542 y1543; ventana anual, no una fecha exacta.'
  add(k,q,row['name'],role,a,b,p,row['source'],note)
 # Additional verified humans and independently selected offices, never consort
 # tenures, births or deaths repurposed as a political mandate.
 extras={v.get('person'):v for v in extra if v.get('human')}
 for k,q,role,a,b in [
  ('ETH','Q324688','Emperador de Etiopía','1494-01-01','1507-12-31'),('ETH','Q725222','Emperador de Etiopía','1597-01-01','1603-12-31'),('HIST-Q796583','Q1522957','Rey del Kongo','1470-01-01','1509-12-31'),('SUR','Q3348692','Soberano surí · sucesión disputada','1554-01-01','1555-12-31'),
  ('FRA','Q131552','Regente de Francia','1560-01-01','1563-12-31'),
  ('CASTILE','Q12860','Fernando V · co-rey de Castilla','1500-01-01','1504-12-31'),('CASTILE','Q12860','Regente de Castilla','1507-01-01','1516-12-31'),('CASTILE','Q342392','Regente de Castilla','1516-01-01','1517-12-31'),
  ('HIST-Q33296','Q486188','Emperador mogol · primer reinado','1530-12-26','1540-05-17'),('HIST-Q33296','Q486188','Emperador mogol · restauración','1555-06-22','1556-01-27'),
  ('WURTTEMBERG-DUCHY','Q61671','Duque de Wurtemberg','1498-01-01','1519-12-31'),('WURTTEMBERG-DUCHY','Q61671','Duque de Wurtemberg · restauración','1534-01-01','1550-12-31'),
  ('JPN','Q466281','Shogun Ashikaga','1494-01-01','1508-12-31'),('JPN','Q708527','Shogun Ashikaga · restauración','1508-01-01','1521-12-31'),('JPN','Q536313','Shogun Ashikaga','1521-01-01','1546-12-31'),('JPN','Q447066','Shogun Ashikaga','1546-01-01','1565-12-31'),('JPN','Q541037','Shogun Ashikaga · sucesión disputada','1568-01-01','1568-12-31'),('JPN','Q434415','Shogun Ashikaga · gobierno en Kioto','1568-01-01','1573-12-31'),
  ('JPN','Q171411','Dirigente Oda · poder regional y consolidación','1568-01-01','1582-12-31'),('JPN','Q187550','Kanpaku · regente imperial','1585-01-01','1591-12-31'),('JPN','Q187550','Taikō · dirigente retirado','1591-01-01','1598-12-31'),
  ('HIST-Q202687','Q2866677','Askia · soberano de Songhai','1537-01-01','1539-12-31')]:
  v=extras[q];note='Observación anual contrastada por cargo. '
  if k=='JPN':note+='El emperador, el shogun y los dirigentes militares son cargos distintos. No se denomina shogun aOda oToyotomi ni se afirma unificación territorial completa. La pretensión deYoshiaki después de1573 no equivale a gobierno efectivo enKioto.'
  if k=='WURTTEMBERG-DUCHY':note+='Exilio1519–1534 separado del control ducal; no se interpola como gobierno efectivo continuo.'
  if k=='HIST-Q33296':note+='Reinados separados por el poder surí; no se interpola un mandato continuo1530–1556.'
  add(k,q,v['name'],role,a,b,9,v['source'],note)
 # IvanIV has two different offices; the Muscovy lookup failed on an HTML
 # response, but his canonical human identity is independently in the candidates.
 v=next(v for v in candidates['records'] if v.get('person')=='Q7996' and v.get('human'))
 add('MUSCOVY','Q7996',v['name'],'Gran príncipe de Moscú','1533-01-01','1546-12-31',9,v['source'],'Minoría y regencias; el título de zar comienza en1547 y no se anticipa a1533.')
 for v in additional:
  row=v['candidate'];k=row['key'];q=row['person'];dates=[];note='Observación anual del cargo; no certifica fechas diarias ni control territorial uniforme.'
  if k=='PAPAL-STATES':
   a=next((f.removeprefix('Papacy began ') for f in v['fields'] if f.startswith('Papacy began ')),None);b=next((f.removeprefix('Papacy ended ') for f in v['fields'] if f.startswith('Papacy ended ')),None)
   if a and b:
    dates=[(r.date(a)[0],r.date(b,True)[0])];note+=' Se utiliza el pontificado, no un cargo anterior de cardenal ni la fecha de coronación. Calendario histórico, precisión anual.'
  elif k=='HIST-Q4948':
   dates=[(c['start'],c['end']) for c in v['claims'] if c['office']=='Q858316']
   if q=='Q1348814':dates=[('1539-01-01','1545-12-31')]
   note+='Dux elegido, distinto de un monarca hereditario; cargos delSenado yConsejo no se convierten en un gobierno personal absoluto.'
  elif q=='Q335546':dates=[('1526-01-01','1545-12-31'),('1547-01-01','1549-12-31')]
  elif k=='POLAND-KINGDOM' and q=='Q54056':dates=[('1506-01-01','1548-12-31')]
  elif k=='POLAND-KINGDOM' and q=='Q54058':dates=[('1530-01-01','1568-12-31')];note+='Coronado co-rey dePolonia en1530; gobierno personal desde1548. El gran ducado lituano y la unión deLublin tienen cronologías distintas.'
  elif k=='EAST-HUNGARY' and q=='Q313396':dates=[('1540-01-01','1551-12-31'),('1556-01-01','1570-12-31')];note+='Realeza disputada y regencia deIsabelJagellón; el título de príncipe deTransilvania desde1570 es distinto. No se usa ese título como comienzo del reinado húngaro.'
  elif row['parsed']:
   i=1 if k=='POLAND-KINGDOM' and q=='Q53450' else 0;p=row['parsed'][i];dates=[(p['start'],p['end'])]
  if not dates:rejected.append(dict(candidate=row,reason='Additional office dates unresolved'));continue
  for a,b in dates:
   if k=='POLAND-KINGDOM':b=min(b,'1568-12-31')
   add(k,q,row['name'],row['role'],a,b,9,row['source'],note)
  if k=='DENMARK-NORWAY':
   for a,b in dates:
    if a<'1524':add('KALMAR',q,row['name'],'Rey de Dinamarca y Noruega · unión deKalmar disputada',a,min(b,'1523-12-31'),9,row['source'],'El gobierno enSuecia no fue continuo; las regencias y la independencia suecas se distinguen del cargo danés-noruego.')
  if k=='FLORENCE-DUCHY' and q=='Q48547':
   p=row['parsed'][1];add('HIST-Q154849',q,row['name'],'Gran duque de Toscana',p['start'],p['end'],9,row['source'],'Elevación a gran ducado en1569, distinta del título ducal desde1537.')
 for row in read(ROOT/'.cache/rulers021-additional.json')['records']:
  if not row.get('human'):rejected.append(dict(candidate=row,reason='Not a verified human; ambiguous item excluded'))
 return dict(records=accepted,rejected=rejected,candidates=candidates,extraCandidates=extra,additionalEvidence=additional,polityEvidence=read(ROOT/'.cache/polities021-verified.json'),scope='Partial reviewed offices, annual dates; source polygon extents are not independently certified.')

def prepare(old,research):
 d=copy.deepcopy(old);cs=d['countries'];images={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for k,q,name in [('HESSE-UNITED','Q695322','Landgraviato de Hesse'),('NEO-INCA','Q10715354','Reino de Vilcabamba'),('FLORENCE-REPUBLIC','Q148540','República de Florencia'),('FLORENCE-DUCHY','Q2252973','Ducado de Florencia'),('POLAND-KINGDOM','Q1649871','Reino de Polonia'),('BOURBON-DUCHY','','Borbón · dominio ducal'),('EASTERN-MOGHULISTAN','','Mogulistán oriental · referencia de fuente'),('WESTERN-MOGHULISTAN','','Mogulistán occidental · referencia de fuente')]:
  cs.setdefault(k,dict(qid=q,name=name,leaders=[],flags=[]))
  if k=='FLORENCE-DUCHY':cs[k]['qid']=q
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for row in research['records']:
  k=row['key'];l=copy.deepcopy(row['term']);l['acquisition']=TAG
  if l['person'] in images:l['portrait']=images[l['person']]
  cs[k]['leaders']=[o for o in cs[k]['leaders'] if not(o.get('acquisition')=='historical-0.21' and o['person']==l['person'] and o['start']<=l['end'] and o['end']>=l['start'])];cs[k]['leaders'].append(l)
 # Same monarch, distinct crowns. No union before1580, no shared administration.
 for l in cs['PRT']['leaders']:
  if l.get('acquisition')==TAG and l['person'] in ['Q34417','Q34464']:
   v=copy.deepcopy(l);v['role']='Monarca de la unión dinástica';v['note']='España yPortugal conservan instituciones distintas.';cs['IBERIAN-UNION']['leaders'].append(v)
 return d

if __name__=='__main__':
 p=ROOT/'scripts/historical-offices-021-research.json';rs=research() if not p.exists() or '--research' in sys.argv else read(p);save(p,rs);old=read(OUT/'identities.json');d=prepare(old,rs);assert prepare(d,rs)==d
 for k,c in old['countries'].items():assert all(l in d['countries'][k]['leaders'] for l in c['leaders'] if l.get('acquisition') not in [TAG,'historical-0.21']),k
 save(OUT/'identities.json',d);print('Reviewed office intervals',len(rs['records']),'rejected/unresolved',len(rs['rejected']))
