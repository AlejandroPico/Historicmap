"""Reviewed 1800–1900 authorities and source-identity repairs.

This is an explicit curator, not an automatic adoption of search results.
The retained research file records accepted reigns and rejected candidates.
"""
import pathlib,json,copy,importlib.util,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='review-1800-1900-0.18'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')

def reviewed_candidates():
 german=read(ROOT/'.cache/german018-rulers.json');offices=read(ROOT/'.cache/offices018-candidates.json');accepted=[];rejected=[]
 for r in german['records']:
  if not r.get('human'):rejected.append(dict(candidate=r,reason='Not a verified human'));continue
  q=r['person'];idx=1 if q in ['Q57302','Q58770'] else 0
  if not r['parsed']:
   if q!='Q67043':rejected.append(dict(candidate=r,reason='No reviewed reign interval'));continue
   dates=dict(start='1800-01-01',end='1802-11-05',precision=11)
  else:dates=copy.deepcopy(r['parsed'][idx])
  role=r['role'];note='Soberano territorial; su título no se sustituye por una jefatura presidencial moderna.';source=r['source']
  if q=='Q57508':dates['start']='1848-06-16';note+=' El5/3/1848 es el inicio de la corregencia, no la sucesión soberana.'
  if q=='Q60604':dates['end']='1856-09-04';source='https://digital.blb-karlsruhe.de/id/124866';note+=' El traspaso del título a Federico es de1856, no1858.'
  if q=='Q57483':dates['start']='1856-09-05';source='https://digital.blb-karlsruhe.de/id/124866';note+=' Proclamación del título gran ducal de5/9/1856; regencia anterior distinta.'
  if q=='Q170179':dates['start']='1806-01-01';note+=' Rey desde1806; el intervalo ducal anterior no se convierte en reinado.'
  if q=='Q213671':dates['start']='1807-01-01';note+=' Ventana interior desde1807; la elevación de1806 se conserva como cobertura pendiente de fecha ceremonial.'
  accepted.append(dict(key=r['key'],term=dict(person=q,name=r['name'],role=role,source=source,note=note,**{k:v for k,v in dates.items() if k!='raw'})))
  if q=='Q53444':accepted.append(dict(key=r['key'],term=dict(person=q,name=r['name'],role='Elector de Sajonia',start='1800-01-01',end='1806-12-20',precision=11,source=source,note='Título electoral anterior al reino.')))
 for r in offices['records']:
  l=copy.deepcopy(r['term']);key=r['key']
  if key=='HIST-Q600524':continue # replaced by separately reviewed chronological table
  if key=='CHL':
   if l['person'] in ['Q9025015','Q734977']:rejected.append(dict(candidate=r,reason='Placeholder dates or exile mistaken for effective government'));continue
   if l['person']=='Q1332':l.update(start='1823-04-04',source='https://www.memoriachilena.gob.cl/602/w3-article-92159.html',note='Director supremo; presidencia de1827 distinta.')
  # Do not accept day-long placeholders extracted from year/month-only claims.
  if l['start']==l['end'] and l.get('precision',9)<11:rejected.append(dict(candidate=r,reason='Unresolved placeholder interval'));continue
  if key=='HIST-Q171393' and l['person']=='Q790321':l.update(start='1849-06-20',note='Designación posterior al interinato de1848; gobierno interrumpido por ocupaciones extranjeras, no control continuo acreditado.',source='https://en.wikipedia.org/wiki/Barbu_Dimitrie_%C8%98tirbei')
  if key=='HIST-Q171393' and l['person']=='Q2272090' and l['start']=='1806-01-01':rejected.append(dict(candidate=r,reason='Condensed reign incorrectly extends to1812'));continue
  accepted.append(dict(key=key,term=l))
 return dict(records=accepted,rejected=rejected,note='Explicitly reviewed subset; dates of concurrent regencies and imperial authority are not modern presidential terms.')

def prepare(incoming,research):
 d=copy.deepcopy(incoming);cs=d['countries'];images={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 def country(k,q,name):
  cs.setdefault(k,dict(qid=q,name=name,leaders=[],flags=[]));cs[k].update(qid=q,name=name)
 def term(k,q,name,role,a,b,source,precision=11,note='',**extra):
  # Replace overlapping source duplicates only for this person and reviewed office.
  c=cs[k];c['leaders']=[l for l in c['leaders'] if not(l['person']==q and l['start']<=b and l['end']>=a and l['end']<='1900-12-31')]
  l=dict(person=q,name=name,role=role,start=max(a,'1800-01-01'),end=min(b,'1900-12-31'),precision=precision,source=source,curated=True,acquisition=TAG,note=note,**extra)
  if a<='1800-01-01' or precision<11:l['startIsCoverageBoundary']=True
  if b>='1900-12-31' or precision<11:l['endIsCoverageBoundary']=True
  if q in images:l['portrait']=copy.deepcopy(images[q])
  if l['start']<=l['end']:c['leaders'].append(l)
 for row in research['records']:
  l=copy.deepcopy(row['term']);term(row['key'],l.pop('person'),l.pop('name'),l.pop('role'),l.pop('start'),l.pop('end'),l.pop('source'),l.pop('precision',11),l.pop('note',''),**{k:v for k,v in l.items() if k not in ['acquisition','curated']})
 country('HABSBURG-MONARCHY','Q153136','Monarquía de Habsburgo')
 term('HABSBURG-MONARCHY','Q130834','Francisco II','Soberano de los dominios de los Habsburgo','1800-01-01','1804-08-10','https://www.habsburger.net/en/persons/habsburg-emperor/franz-ii-i',note='Emperador del Sacro Imperio hasta1806 y emperador de Austria desde11/8/1804; cargos y conjuntos territoriales distintos.',startIsCoverageBoundary=True)
 country('RIO-DE-LA-PLATA','Q738144','Provincias Unidas del Río de la Plata')
 for l in list(cs['ARG']['leaders']):
  if l['start']<='1831-12-31' and l['end']>='1810-05-25':
   t=copy.deepcopy(l);t['acquisition']=TAG
   if t['end']>'1831-12-31':t.update(end='1831-12-31',endIsCoverageBoundary=True)
   cs['RIO-DE-LA-PLATA']['leaders'].append(t)
 term('RIO-DE-LA-PLATA','Q1710498','Juan Gregorio de Las Heras','Gobernador de Buenos Aires · autoridad provincial','1824-12-31','1825-12-31','https://www.argentina.gob.ar/sites/default/files/junta_de_representantes.pdf',9,'No presidente de todas las Provincias Unidas. La ley de elección es del2/4/1824; observación anual interior del gobierno provincial. Entre1820 y1825 no existe un ejecutivo nacional permanente unificado.')
 cs['RIO-DE-LA-PLATA']['territoryStatus']=dict(start='1820-01-01',end='1825-12-31',text='Autonomías provinciales sin ejecutivo nacional permanente. La autoridad porteña se presenta con su alcance provincial, no como un jefe de Estado de toda la unión.',source='https://cdi.mecon.gov.ar/greenstone/collect/registr1/index/assoc/HASH01ac.dir/doc.pdf')
 term('PRY','Q34063','José Gaspar Rodríguez de Francia','Dictador perpetuo de Paraguay','1816-05-30','1840-09-20','https://www.mef.gov.py/sites/default/files/2024-07/pub007_0.pdf',note='La dictadura temporal de1814 precede a este mandato perpetuo.')
 term('HIST-Q206696','HELVETIC-EXECUTIVE-1800','Consejo Ejecutivo','Ejecutivo colegiado de la República Helvética','1800-08-08','1800-12-31','https://hls-dhs-dss.ch/fr/articles/009797/2011-01-27/',note='Consejo de siete miembros después del golpe de agosto; no una presidencia individual.',endIsCoverageBoundary=True)
 country('BRITISH-COLONIES','Q8680','Colonias del Imperio británico')
 cs['BRITISH-COLONIES']['territoryStatus']=dict(start='1800-01-01',end='1885-12-31',text='Agregado colonial de la fuente. Se muestran las autoridades del Estado administrador; no un único gobernador local para todas las colonias.',source='https://www.canada.ca/en/canadian-heritage/services/crown-canada/governor-general.html')
 for row in research.get('africanRecords',[]):
  l=copy.deepcopy(row['term']);term(row['key'],l.pop('person'),l.pop('name'),l.pop('role'),l.pop('start'),l.pop('end'),l.pop('source'),l.pop('precision',9),l.pop('note',''))
 return d

def resolutions(ids):
 for a in [1800,1820,1840,1860,1880]:
  p=OUT/f'historical-{a}-entities.json';d=read(p);lo,hi=d['coverageStart'],d['coverageEnd']
  d['qidKeys'].update(Q66504140='HABSBURG-MONARCHY',Q153136='HABSBURG-MONARCHY',Q35827='RIO-DE-LA-PLATA',Q738144='RIO-DE-LA-PLATA')
  d['names'].update({k:ids['countries'][k]['name'] for k in ['HABSBURG-MONARCHY','RIO-DE-LA-PLATA','BRITISH-COLONIES']})
  d['records']=[r for r in d['records'] if r.get('acquisition')!=TAG]
  def rule(names,key,label,start,end,admin='',status='independent',note=''):
   if max(start,lo)>min(end,hi):return
   d['records'].insert(0,dict(names=names,key=key,label=label,entityCode=key,start=max(start,lo),end=min(end,hi),admin=admin,status=status,note=note,source='https://github.com/AlejandroPico/Historicmap/blob/main/docs/REVIEW-0.18.md',acquisition=TAG))
  rule(['Habsburg Monarchy'],'HABSBURG-MONARCHY','Monarquía de Habsburgo',1800,1803,note='Se rechaza el Q66504140 de desambiguación de la fuente; entidad histórica Q153136.')
  rule(['Habsburg Monarchy'],'AUSTRIAN-EMPIRE','Imperio de Austria',1804,1806,note='Proclamación imperial11/8/1804; contorno anual de fuente.')
  rule(['Río de la Plata','Rio de la Plata'],'RIO-DE-LA-PLATA','Provincias Unidas del Río de la Plata',1810,1831,note='Se rechaza Q35827, que identifica al río, no al Estado.')
  rule(['Helvetic Republic'],'HIST-Q206696','República Helvética',1800,1802)
  rule(['Helvetic Republic'],'CHE','Confederación Suiza · Acta de Mediación',1803,1813,note='La República Helvética termina en1803; la etiqueta más larga de la fuente no prolonga su régimen.')
  rule(['British Colonial Empire'],'BRITISH-COLONIES','Colonias del Imperio británico',1800,1885,'GBR','colony','Agregado colonial, con autoridades británicas externas; no gobernador local único.')
  rule(['Portuguese Colonies'],'HIST-Q200464','Colonias portuguesas · agregado de fuente',1800,1885,'PRT','colony','Se diferencian los cargos de la monarquía portuguesa de los gobiernos territoriales pendientes de documentación.')
  save(p,d)

if __name__=='__main__':
 p=ROOT/'scripts/review-018-authorities.json'
 research=read(p) if p.exists() and '--rebuild-research' not in sys.argv else reviewed_candidates()
 if p.exists() and '--rebuild-research' in sys.argv:research['africanRecords']=read(p).get('africanRecords',[])
 save(p,research);d=prepare(read(OUT/'identities.json'),research);assert prepare(d,research)==d
 save(OUT/'identities.json',d);resolutions(d)
 print('Integrated',len(research['records']),'reviewed office intervals;',len(research.get('africanRecords',[])),'African intervals; rejected',len(research['rejected']))
