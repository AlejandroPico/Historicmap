"""Bounded1840–1879 authority curation; existing1880+ statements stay intact.

Research candidates are individually reviewed: generic titles are not automatically
national offices. Hong Xiuquan belongs to the Taiping polity, not the Qing court.
Coarse observations keep explicit coverage flags, never fabricated accession days.
"""
import pathlib,json,copy,datetime,argparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
FIRST,LAST,TAG='1840-01-01','1879-12-31','curated-1840-0.15'
def additions(research):
 rows=[]
 titles={'PRUSSIA':'Rey de Prusia','HIST-Q154195':'Rey de Baviera','HIST-Q165763':'Príncipe de Waldeck y Pyrmont','JOS':'Rey de Joseon','ETH':'Emperador de Etiopía','AUSTRIAN-EMPIRE':'Emperador de Austria','NPL':'Rey de Nepal','IRN':'Shah de Persia · dinastía Qajar','QING':'Emperador de la dinastía Qing','SAR':'Rey de Cerdeña y duque de Saboya','BRA-EMPIRE':'Emperador del Brasil','EGY':'Jedive de Egipto'}
 for item in research['records']:
  key=item['key'];r=copy.deepcopy(item['term']);r['acquisition']=TAG
  if key in titles and not (key=='NPL' and r['office']=='Q30100626'):r['role']=titles[key]
  if key=='AUSTRIAN-EMPIRE':r['end']=min(r['end'],'1867-05-28')
  if r['person']=='Q334732':key='HIST-Q3486676';r['role']='Rey celestial · autoridad Taiping';r['name']='Hong Xiuquan'
  if r['person']=='Q257425':r['name']='Gojong'
  if r['person']=='Q315659':r.update(start='1872-12-31',precision=9,startIsCoverageBoundary=True,source='https://betamasaheft.awhamburg.de/persons/PRS10378Yohanne/main',note='Observación desde el cierre de1872, distinta de la conquista del poder de1871 y la coronación. Se conserva precisión anual de la fuente institucional, sin convertir el cierre en acceso al trono.')
  if key=='HIST-Q1071439':r['role']='Reina de Imerina'
  if key=='PRUSSIA' and r['person']=='Q37134':r.update(end='1840-06-07',precision=11,source='https://www.dhm.de/lemo/biografie/friedrich-wilhelm-iv',note='Fallecimiento de Federico Guillermo III el7/6/1840; no el1de enero del dato de precisión anual.')
  if r['start']<=r['end']:rows.append((key,r))
 def term(key,q,name,role,a,b,source,note='',precision=11,coverage=False):
  assert FIRST<=a<=b<=LAST,(key,name,a,b)
  r=dict(person=q,name=name,role=role,start=a,end=b,source=source,note=note,precision=precision,curated=True,acquisition=TAG)
  if coverage or a==FIRST:r['startIsCoverageBoundary']=True
  if coverage or b in (LAST,'1859-12-31'):r['endIsCoverageBoundary']=True
  rows.append((key,r))
 term('GBR','Q9439','Victoria','Reina del Reino Unido',FIRST,LAST,'https://api.parliament.uk/regnal-years/monarchs/6','Ventana interior de un reinado iniciado20/6/1837; los extremos de cobertura no son accesión ni fallecimiento.')
 term('RUE','Q130734','Nicolás I','Emperador de Rusia',FIRST,'1855-03-02','https://www.wikidata.org/wiki/Q130734','Fechas gregorianas: el18de febrero juliano y el2de marzo gregoriano no son dos ceses distintos.')
 term('RUE','Q83171','Alejandro II','Emperador de Rusia','1855-03-02','1859-12-31','https://www.wikidata.org/wiki/Q83171','Sucesión expresada en calendario gregoriano; no se duplica con la fecha juliana de la misma transición.')
 term('ESP','Q230566','María Cristina de Borbón-Dos Sicilias','Regente',FIRST,'1840-10-12','https://ocw.uc3m.es/pluginfile.php/7622/mod_page/content/25/T2-1-1-6_Regencia-Espartero.pdf','Renuncia y exilio diferenciados del nombramiento parlamentario posterior de Espartero.')
 term('ESP','MINISTRY-REGENCY-1840','Ministerio-regencia','Regencia provisional colectiva','1840-10-13','1841-05-09','https://ocw.uc3m.es/pluginfile.php/7622/mod_page/content/25/T2-1-1-6_Regencia-Espartero.pdf','Órgano colectivo de transición; no se inventa un retrato individual.')
 term('ESP','Q434529','Baldomero Espartero','Regente','1841-05-10','1843-07-31','https://www.congreso.es/ca/cem/regespartero','Nombramiento parlamentario de1841, separado del liderazgo político de1840. Final observado con resolución mensual, sin afirmar cese el31de julio.',precision=10)
 term('FRA','Q2309694',"Jacques-Charles Dupont de l’Eure",'Presidente del Gobierno provisional','1848-02-24','1848-05-09','https://www.elysee.fr/la-presidence/la-constitution-du-4-novembre-1848','El primer presidente de la República elegido bajo la Constitución de1848 fue Luis Napoleón; presidir el Gobierno provisional es otro cargo.')
 term('FRA','FRENCH-EXECUTIVE-COMMISSION-1848','Comisión Ejecutiva','Poder Ejecutivo colegiado','1848-05-10','1848-06-24','https://www.assemblee-nationale.fr/dyn/histoire-et-patrimoine/histoire-de-l-assemblee-nationale/la-deuxieme-republique','Órgano colegiado anterior a la presidencia constitucional; sin fotografía individual inventada.')
 term('FRA','Q379702','Louis-Eugène Cavaignac','Jefe del Poder Ejecutivo','1848-06-28','1848-12-20','https://www.elysee.fr/la-presidence/la-constitution-du-4-novembre-1848','No presidente electo de la Segunda República. Las jornadas de junio y la delegación extraordinaria de poderes necesitan cronología propia.')
 term('FRA','Q7721','Luis Napoleón Bonaparte','Presidente de la República','1848-12-20','1852-12-01','https://www.elysee.fr/louis-napoleon-bonaparte','Elección10/12/1848 y juramento20/12/1848 separados. El golpe de1851 no es todavía la proclamación imperial.')
 term('FRA','Q7721','Napoleón III','Emperador de los franceses','1852-12-02','1859-12-31','https://www.elysee.fr/louis-napoleon-bonaparte','Segundo Imperio desde2/12/1852; continúa en la ventana ya documentada desde1860.')
 term('BRA-EMPIRE','Q1797348','Pedro de Araújo Lima','Regente del Imperio',FIRST,'1840-07-22','https://www.senado.leg.br/senado/hotsites/histsf/O-Senado-no-2o-Reinado.asp','La mayoría anticipada de Pedro II el23/7/1840 termina la regencia; no debe confundirse con su coronación de1841.')
 term('PRUSSIA','Q150652','Guillermo de Prusia','Príncipe regente','1858-10-07','1859-12-31','https://www.dhm.de/lemo/biografie/friedrich-wilhelm-iv','Delegación del Gobierno por enfermedad de Federico Guillermo IV; no acceso de Guillermo al trono en1858.')
 hawaii='https://digitalarchives.hawaii.gov/item/ark%3A70111/51NQ'
 term('HAW-KINGDOM','Q455795','Kamehameha III','Rey de Hawái',FIRST,'1854-12-15',hawaii,'Proclamación archivada de muerte y sucesión; no se confunde la toma de posesión posterior con la sucesión.')
 term('HAW-KINGDOM','Q470398','Kamehameha IV','Rey de Hawái','1854-12-15','1863-11-30',hawaii,'Inicio confirmado por proclamación contemporánea. El fallecimiento limita la observación; no una prolongación del reinado por ausencia de sucesor.')
 term('HAW-KINGDOM','Q887354','Kamehameha V','Rey de Hawái','1863-11-30','1872-12-11','https://history.state.gov/historicaldocuments/frus1873p1v1/d231','La documentación de1873 distingue su muerte sin heredero de la elección parlamentaria del nuevo monarca.')
 term('HAW-KINGDOM','Q499103','Lunalilo','Rey de Hawái','1873-01-08','1874-02-03','https://www.lunalilo.org/king-lunalilo/history-of-king-lunalilo-trust','Elección legislativa8/1/1873 y ceremonia9/1/1873 son acontecimientos distintos.')
 nepal='https://opmcm.gov.np/pages/former-prime-ministers/'
 term('NPL','Q2355896','Jung Bahadur Rana','Primer ministro','1847-01-01','1855-12-31',nepal,'Observación interior de su primer mandato: la lista oficial usa Bikram Sambat. No se inventa una conversión diaria ni se rellena automáticamente la transición1856–1857.',precision=9,coverage=True)
 term('NPL','Q2355896','Jung Bahadur Rana','Primer ministro','1858-01-01','1876-12-31',nepal,'Observación interior de su segundo mandato; separados los dos periodos y conservada la laguna del relevo.',precision=9,coverage=True)
 term('NPL','Q593609','Ranodip Singh Kunwar','Primer ministro','1877-12-31',LAST,nepal,'Observación anual tras el relevo de1877; no nombramiento el31de diciembre.',precision=9,coverage=True)
 term('EGY','Q182781','Muhammad Alí','Valí de Egipto',FIRST,'1848-01-01','https://www.wikidata.org/wiki/Q182781','Observación interior del gobierno iniciado1805. El extremo1848 es cobertura, no fecha de cese certificada.',precision=9,coverage=True)
 term('EGY','Q311789','Ibrahim Bajá','Valí de Egipto','1848-11-01','1848-11-10','https://www.wikidata.org/wiki/Q311789','Observación acotada de1848, limitada por su fallecimiento; el inicio de noviembre no se presenta como acceso al gobierno.',precision=10,coverage=True)
 term('EGY','Q305882','Abbás I','Valí de Egipto','1848-11-24','1854-01-01','https://www.presidency.eg/EN/مصر/الحكام/عباس-باشا-الأول/','Inicio según la Presidencia egipcia. Observación hasta comienzos de1854; las fuentes difieren en el día del relevo de julio, que no se resuelve con un día inventado.',precision=9,coverage=True)
 term('EGY','Q366744','Saíd Bajá','Valí de Egipto','1854-12-31','1863-01-01','https://www.wikidata.org/wiki/Q366744','Ventana interior documentada de su gobierno1854–1863; los extremos son observaciones, no fechas de acceso y cese.',precision=9,coverage=True)
 term('HTI','Q560853','Faustin Soulouque · Faustino I','Emperador de Haití','1849-12-31','1859-01-15','https://www.wikidata.org/wiki/Q560853','Observación interior desde el cierre de1849; el25/26de agosto requiere cotejo antes de fijar un día de acceso. El cargo imperial se distingue de la presidencia anterior y del primer Imperio de1804.',precision=9,coverage=True)
 return rows
def curate(incoming,research):
 d=copy.deepcopy(incoming);countries=d['countries'];portraits={l['person']:l['portrait'] for c in countries.values() for l in c['leaders'] if l.get('portrait')}
 for c in countries.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 countries['JOS']['qid']='Q28179'
 countries.setdefault('HIST-HUNGARY-1848',dict(qid='',name='Hungría · Gobierno revolucionario',flags=[],leaders=[],territoryStatus=dict(start='1848-01-01',end='1849-12-31',text='Identidad revolucionaria distinta de Austria-Hungría, creada en1867. Autoridades y fases territoriales pendientes de contraste; no se asigna al emperador posterior como jefe de la insurrección.',source='https://github.com/Seshat-Global-History-Databank/cliopatria')))
 if 'HIST-Q151624' in countries:countries['HIST-Q151624']['territoryStatus']=dict(start=FIRST,end='1866-12-31',text='Confederación de Estados, sin un soberano nacional único. La Asamblea Federal, la presidencia austríaca y el poder central revolucionario de1848–1849 son instituciones diferentes; falta completar su serie. El agregado cartográfico no es un reino de Prusia.',source='https://www.dhm.de/lemo/kapitel/vormaerz-und-revolution/revolution-1848')
 duplicate=countries.pop('HIST-Q28179',None)
 if duplicate:
  for l in duplicate['leaders']:
   if l not in countries['JOS']['leaders']:countries['JOS']['leaders'].append(l)
 # Substantive French office correction, scoped before1860 only.
 for l in countries['FRA']['leaders']:
  if l['end']<'1860-01-01' and l['person'] in ['Q2309694','Q379702'] and l['role']=='Presidente de la República':l['role']='Presidente del Gobierno provisional' if l['person']=='Q2309694' else 'Jefe del Poder Ejecutivo'
 for key,r in additions(research):
  c=countries.setdefault(key,dict(qid='',name=key,flags=[],leaders=[]))
  if r['person'] in portraits:r['portrait']=copy.deepcopy(portraits[r['person']])
  c['leaders'].append(r)
 return d
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--input',type=pathlib.Path,required=True);parser.add_argument('--research',type=pathlib.Path,required=True);parser.add_argument('--output',type=pathlib.Path,required=True);args=parser.parse_args()
 if args.input.resolve()==args.output.resolve():parser.error('Use a distinct output path')
 incoming=json.loads(args.input.read_text(encoding='utf8'));research=json.loads(args.research.read_text(encoding='utf8'));d=curate(incoming,research);assert curate(d,research)==d
 args.output.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n');print('Prepared',len(additions(research)),'reviewed historical office observations')
