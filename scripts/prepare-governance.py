"""Dated constitutional forms and separately licensed regime observations.

Undated current claims apply only to the reference year. Historical undated
claims provide broad institutional forms, never a retrospective democracy score.
"""
import pathlib,json,importlib.util,csv,collections
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
def save(name,data):h.save(OUT/name,data)
TAXONOMY=[
 ('parliamentary-system','Sistemas parlamentarios','Forma política',[]),('monarchy','Monarquías','Forma política',[]),('absolute-monarchy','Monarquías absolutas','Forma política',['monarchy']),('constitutional-monarchy','Monarquías constitucionales','Forma política',['monarchy']),('parliamentary-monarchy','Monarquías parlamentarias','Forma política',['constitutional-monarchy']),('elective-monarchy','Monarquías electivas','Forma política',['monarchy']),('dual-monarchy','Monarquías duales','Forma política',['monarchy']),('regency','Regencias','Forma política',[]),
 ('republic','Repúblicas','Forma política',[]),('presidential-republic','Repúblicas presidenciales','Forma política',['republic']),('parliamentary-republic','Repúblicas parlamentarias','Forma política',['republic']),('semi-presidential-republic','Repúblicas semipresidenciales','Forma política',['republic']),('directorial','Directorios','Forma política',['republic','collective']),('consulate','Consulados','Forma política',['republic']),('collective','Gobiernos colegiados','Forma política',[]),('junta','Juntas de gobierno','Forma política',['collective']),('theocracy','Teocracias','Forma política',[]),('tribal','Organizaciones políticas tribales','Forma política',[]),('chiefdom','Jefaturas','Forma política',['tribal']),('transitional','Gobiernos de transición','Forma política',[]),
 ('empire','Imperios','Organización territorial',[]),('kingdom','Reinos','Organización territorial',['monarchy']),('duchy','Ducados y grandes ducados','Organización territorial',['monarchy']),('principality','Principados','Organización territorial',['monarchy']),('county','Condados','Organización territorial',['monarchy']),('electorate','Electorados','Organización territorial',['monarchy']),('sultanate','Sultanatos','Organización territorial',['monarchy']),('emirate','Emiratos','Organización territorial',['monarchy']),('caliphate','Califatos','Organización territorial',['theocracy']),('khanate','Kanatos','Organización territorial',['monarchy']),('city-state','Ciudades-Estado','Organización territorial',[]),('federal','Federaciones','Organización territorial',[]),('confederal','Confederaciones','Organización territorial',[]),('unitary','Estados unitarios','Organización territorial',[]),('dynastic-union','Uniones dinásticas','Organización territorial',['monarchy']),('feudal','Organizaciones feudales','Organización territorial',[]),
 ('democracy','Democracias','Evaluación del régimen',[]),('electoral-democracy','Democracias electorales','Evaluación del régimen',['democracy']),('liberal-democracy','Democracias liberales','Evaluación del régimen',['democracy']),('direct-democracy','Democracias directas','Evaluación del régimen',['democracy']),('representative-democracy','Democracias representativas','Evaluación del régimen',['democracy']),('autocracy','Autocracias','Evaluación del régimen',[]),('closed-autocracy','Autocracias cerradas','Evaluación del régimen',['autocracy']),('electoral-autocracy','Autocracias electorales','Evaluación del régimen',['autocracy']),('dictatorship','Dictaduras','Evaluación del régimen',['autocracy']),('military-dictatorship','Dictaduras militares','Evaluación del régimen',['dictatorship']),('personalist-dictatorship','Dictaduras personalistas','Evaluación del régimen',['dictatorship']),('communist-dictatorship','Dictaduras comunistas','Evaluación del régimen',['dictatorship','communist-state']),('fascist-dictatorship','Dictaduras fascistas','Evaluación del régimen',['dictatorship','fascist-state']),('oligarchy','Oligarquías','Evaluación del régimen',[]),('one-party','Sistemas de partido único','Evaluación del régimen',[]),('communist-state','Estados comunistas','Orientación política',[]),('socialist-state','Estados socialistas','Orientación política',[]),('fascist-state','Estados fascistas','Orientación política',[]),
 ('dependency','Territorios dependientes','Situación territorial',[]),('colony','Colonias','Situación territorial',['dependency']),('protectorate','Protectorados','Situación territorial',['dependency']),('mandate','Mandatos y fideicomisos','Situación territorial',['dependency']),('company-rule','Gobiernos de compañías','Situación territorial',['dependency']),('military-administration','Administraciones militares','Situación territorial',[]),('occupation','Territorios ocupados','Situación territorial',[]),('unclassified','Sin clasificación documentada','Cobertura',[])]
CLASS={'Q7269':['monarchy'],'Q41614':['constitutional-monarchy'],'Q184558':['absolute-monarchy'],'Q3330103':['parliamentary-monarchy'],'Q2994894':['dual-monarchy'],'Q7270':['republic'],'Q4198907':['parliamentary-republic'],'Q49892':['presidential-republic'],'Q49890':['semi-presidential-republic'],'Q512187':['republic','federal'],'Q43702':['federal'],'Q179164':['unitary'],'Q1520223':['republic'],'Q12759805':['sultanate'],'Q208500':['principality'],'Q48349':['empire'],'Q417175':['kingdom'],'Q1250464':['kingdom'],'Q188759':['representative-democracy'],'Q465613':['republic'],'Q50686':['one-party'],'Q842112':['socialist-state'],'Q133442':['city-state'],'Q166747':['parliamentary-system'],'Q5255892':['republic'],'Q133156':['colony'],'Q161243':['dependency'],'Q1351282':['colony']}
PARENTS={k:p for k,_,_,p in TAXONOMY}
def expanded(tags):
 result=set(tags)
 for t in list(tags):result.update(expanded(PARENTS.get(t,[])))
 return result
def year(value):
 if not value:return None
 return int(value['time'].lstrip('+').rsplit('-',2)[0])
def prepare_forms():
 ids=json.loads((OUT/'identities.json').read_text(encoding='utf8'))['countries'];records=[];lifetimes={};audit=[]
 candidates=json.loads((ROOT/'scripts/research/governance-018-candidates.json').read_text(encoding='utf8'))['items']
 broad={'monarchy','republic','empire','kingdom','duchy','principality','county','electorate','sultanate','emirate','caliphate','khanate','city-state','confederal','federal','unitary','dynastic-union','dependency','colony'}
 for c in candidates:
  key,q=c['key'],c['qid'];e=h.entity(q)
  if any(v.get('id')=='Q4167410' for v in h.values(e,'P31') if isinstance(v,dict)):audit.append(dict(key=key,reason='Disambiguation source identifier'));continue
  born=[year(v) for v in h.values(e,'P571') if isinstance(v,dict) and 'time' in v];died=[year(v) for v in h.values(e,'P576') if isinstance(v,dict) and 'time' in v]
  first=min(born) if born else None;last=max(died) if died else None;lifetimes[key]=[first,last]
  stable=set();current=set()
  for claim in c['claims']:
   tags=CLASS.get(claim['qid'],[])
   if not tags:continue
   a=claim.get('start');b=claim.get('end')
   if a or b:
    start=int(a[0][:4]) if a and not a[0].startswith('-') else first
    end=int(b[0][:4]) if b and not b[0].startswith('-') else last or 2026
    if start is not None and start<=end:records.append(dict(keys=[key],start=start,end=end,tags=tags,source='https://www.wikidata.org/wiki/'+q,sourceLabel='Clasificación institucional fechada',note='Extremos anuales de una declaración; los cambios intranuales requieren su propia fase.'))
   elif last is not None and first is not None:stable.update(expanded(tags)&broad)
   else:current.update(tags)
  if stable:records.append(dict(keys=[key],start=first,end=last,tags=sorted(stable),source='https://www.wikidata.org/wiki/'+q,sourceLabel='Forma general de la entidad histórica',note='Forma amplia; no acredita el mismo régimen constitucional o electoral durante toda su existencia.'))
  if current:records.append(dict(keys=[key],start=2026,end=2026,tags=sorted(current),source='https://www.wikidata.org/wiki/'+q,sourceLabel='Referencia institucional de2026',note='Declaración actual sin vigencia histórica acreditada; no se proyecta a años anteriores.'))
 def add(keys,a,b,tags,url,note=''):
  records.append(dict(keys=keys.split(),start=a,end=b,tags=tags.split(),source=url,sourceLabel='Fase institucional documentada',priority=10,note=note))
 fr='https://www.assemblee-nationale.fr/gouv_parl/fiches_personnalites/Bonaparte.asp';es='https://www.senado.es/web/conocersenado/senadohistoria/periodosconstitucionales/index.html'
 for a,b,t in [(1789,1791,'monarchy'),(1792,1794,'republic'),(1795,1799,'directorial'),(1800,1803,'consulate'),(1804,1813,'monarchy empire'),(1814,1847,'constitutional-monarchy'),(1848,1851,'presidential-republic'),(1852,1869,'monarchy empire'),(1870,1939,'parliamentary-republic'),(1945,1957,'parliamentary-republic'),(1958,2026,'semi-presidential-republic')]:add('FRA',a,b,t,fr,'Lectura de la forma al cierre anual;1814,1815,1848,1852 y1870 contienen transiciones intranuales.')
 for a,b,t in [(1800,1811,'monarchy'),(1812,1813,'constitutional-monarchy regency'),(1814,1819,'absolute-monarchy'),(1820,1822,'constitutional-monarchy'),(1823,1832,'absolute-monarchy'),(1833,1867,'constitutional-monarchy'),(1868,1868,'transitional collective'),(1869,1872,'constitutional-monarchy'),(1873,1873,'republic'),(1874,1930,'constitutional-monarchy'),(1931,1935,'republic'),(1936,1975,'dictatorship'),(1976,1977,'monarchy transitional'),(1978,2026,'parliamentary-monarchy')]:add('ESP',a,b,t,es,'Las autoridades rivales de la guerra civil tienen identidades y clasificaciones propias.')
 for k,a,b,t in [('ESP-REPUBLIC',1936,1939,'republic'),('ESP-NATIONALIST',1936,1939,'military-dictatorship'),('DEU',1871,1917,'monarchy empire federal'),('DEU',1918,1932,'parliamentary-republic federal'),('DEU',1933,1945,'fascist-dictatorship'),('DEU',1949,2026,'parliamentary-republic federal'),('DDR',1949,1989,'communist-dictatorship republic'),('USSR',1922,1989,'communist-dictatorship republic federal'),('USSR',1990,1991,'socialist-state republic federal'),('PRUSSIA',1800,1847,'absolute-monarchy kingdom'),('PRUSSIA',1848,1918,'constitutional-monarchy kingdom'),('RUE',1721,1904,'monarchy empire'),('QING',1644,1911,'monarchy empire'),('OTT',1800,1875,'absolute-monarchy empire sultanate'),('OTT',1876,1877,'constitutional-monarchy empire sultanate'),('OTT',1878,1900,'absolute-monarchy empire sultanate'),('AUSTRIAN-EMPIRE',1804,1866,'monarchy empire'),('AUT-HUN',1867,1918,'dual-monarchy empire'),('HABSBURG-MONARCHY',1800,1804,'dynastic-union monarchy'),('GBR',1800,1900,'constitutional-monarchy empire'),('USA',1789,2026,'presidential-republic federal'),('BRA-EMPIRE',1822,1889,'constitutional-monarchy empire'),('HIST-Q206696',1798,1803,'directorial unitary'),('CHE',1804,1847,'republic confederal'),('CHE',1848,2026,'republic federal'),('HIST-Q10957559',1800,1858,'principality'),('HIST-Q171393',1800,1858,'principality'),('HIST-Q600524',1804,1903,'caliphate'),('HIST-Q1132786',1800,1909,'sultanate'),('HIST-Q1139762',1800,1893,'sultanate'),('ITALIAN-REPUBLIC-1802',1802,1804,'presidential-republic'),('NAPOLEONIC-ITALY',1805,1814,'kingdom'),('NAPLES-BOURBON',1800,1805,'kingdom'),('NAPOLEONIC-NAPLES',1806,1814,'kingdom'),('PAPAL-STATES',1800,1870,'theocracy elective-monarchy'),('HIST-Q199821',1819,1830,'presidential-republic unitary'),('RIO-DE-LA-PLATA',1811,1819,'collective republic'),('RIO-DE-LA-PLATA',1820,1825,'republic confederal'),('RIO-DE-LA-PLATA',1826,1827,'presidential-republic'),('RIO-DE-LA-PLATA',1828,1831,'republic confederal')]:
  add(k,a,b,t,('https://www.wikidata.org/wiki/'+ids[k]['qid']) if ids.get(k,{}).get('qid') else 'https://github.com/AlejandroPico/Historicmap/blob/main/docs/SOURCES.md','Clasificación editorial de la forma; no se deduce democracia de la existencia de una república. Consulte los registros institucionales de la ficha.')
 for k,a,b,t in [('HIST-Q836680',1806,1866,'duchy'),('HIST-Q20135',1806,1918,'duchy'),('HIST-Q186320',1806,1918,'duchy'),('HIST-Q637238',1803,1806,'electorate'),('HIST-Q529605',1803,1866,'electorate'),('HIST-Q14551680',1789,1918,'principality'),('HIST-Q708821',1697,1918,'principality'),('HIST-Q3462133',1826,1918,'duchy'),('HIST-Q155570',1815,1918,'duchy'),('HIST-Q164079',1814,1866,'kingdom'),('HIST-Q159631',1806,1918,'kingdom'),('HIST-Q153015',1806,1918,'kingdom'),('HIST-Q154195',1806,1918,'kingdom')]:
  if k in ids:add(k,a,b,t,'https://www.wikidata.org/wiki/'+ids[k]['qid'])
 records=[r for r in records if not('HIST-Q206696' in r['keys'] and r.get('priority'))]
 add('HIST-Q206696',1798,1799,'directorial unitary','https://hls-dhs-dss.ch/fr/articles/009797/2011-01-27/')
 add('HIST-Q206696',1800,1803,'republic collective unitary','https://hls-dhs-dss.ch/fr/articles/009797/2011-01-27/','El Directorio es abolido en enero1800; los ejecutivos colegiados posteriores son distintos.')
 save('governance.json',dict(format='dated-government-forms',referenceDate='2026-10-26',license='CC0 factual metadata and editorial taxonomy',taxonomy=[dict(id=k,label=l,group=g,parents=p) for k,l,g,p in TAXONOMY],records=records,lifetimes=lifetimes,audit=audit,note='Las formas, la organización territorial y la evaluación del régimen son dimensiones distintas. Desconocido no significa ausencia de gobierno.'))
 print('Government form records',len(records),flush=True)
def prepare_regimes():
 ids=json.loads((OUT/'identities.json').read_text(encoding='utf8'))['countries'];series=collections.defaultdict(dict);unmatched=set()
 historical={'Baden':'HIST-Q186320','Bavaria':'HIST-Q154195','Duchy of Nassau':'HIST-Q836680','Wurttemberg':'HIST-Q159631','Saxony':'HIST-Q153015','Hanover':'HIST-Q164079','Hesse Grand Ducal':'HIST-Q20135','Hesse Electoral':'HIST-Q529605','Modena':'HIST-Q252580','Parma':'HIST-Q165040','Tuscany':'HIST-Q154849','Two Sicilies':'TWO-SICILIES','Oldenburg':'HIST-Q697084','Brunswick':'HIST-Q326029','Saxe-Weimar-Eisenach':'HIST-Q155570','East Germany':'DDR','West Germany':'DEU','Republic of Vietnam':'RVN','Democratic Republic of Vietnam':'VDR','Yemen Arab Republic':'YAR',"Yemen People's Republic":'YPR','Zanzibar':'ZAN','Kosovo':'KOS'}
 for r in csv.DictReader((ROOT/'scripts/research/regimes-of-world-2026.csv').open(encoding='utf8')):
  name,code,y,value=r['Entity'],r['Code'],int(r['Year']),int(r['Political regime']);key=historical.get(name,code)
  if name=='Germany':key='PRUSSIA' if y<=1866 else 'NGC' if y<=1870 else 'DEU'
  if name=='Russia':key='RUE' if y<=1916 else 'RSR' if y<=1921 else 'USSR' if y<=1991 else 'RUS'
  if name=='Austria':key='HABSBURG-MONARCHY' if y<=1803 else 'AUSTRIAN-EMPIRE' if y<=1866 else 'AUT-HUN' if y<=1917 else 'AUT'
  if name=='Italy' or name=='Piedmont-Sardinia':key='SAR' if y<=1860 else 'ITA'
  if name=='China':key='QING' if y<=1911 else 'ROC' if y<=1948 else 'CHN'
  if name=='Czechia':key='CSK' if y<=1992 else 'CZE'
  if name=='Argentina' and 1811<=y<=1831:key='RIO-DE-LA-PLATA'
  if key not in ids:unmatched.add(name);continue
  # Do not backfill Canadian sovereignty from OWID's colonial imputation.
  if key=='CAN' and y<1867:continue
  series[key][y]=value
 compact={}
 for key,values in series.items():
  runs=[]
  for y,v in sorted(values.items()):
   if runs and runs[-1][1]==y-1 and runs[-1][2]==v:runs[-1][1]=y
   else:runs.append([y,y,v])
  compact[key]=runs
 metadata=json.loads((ROOT/'scripts/research/regimes-of-world-2026.metadata.json').read_text(encoding='utf8'))
 save('regimes-of-world.json',dict(format='dated-regime-observations',startYear=1789,endYear=2025,referenceDate='2026-03-17',retrieved='2026-10-26',license='CC BY-SA4.0 (V-Dem); OWID processing attributed',citation='Coppedge et al.2026, V-Dem Dataset v16, DOI10.23696/vdemds26; Lührmann, Tannenberg and Lindberg2018; processing Our World in Data.',source='https://ourworldindata.org/grapher/political-regime',methodology='https://www.v-dem.net/data/the-v-dem-dataset/',metadata=metadata,series=compact,unmatched=sorted(unmatched),note='Exact annual observations only; no extrapolation to2026. OWID imputes some colonial and predecessor series; application excludes local colonial assessment and preserves historical entity crosswalks.'))
 print('Regime series',len(compact),'annual rows',sum(len(v) for v in series.values()),flush=True)
if __name__=='__main__':prepare_forms();prepare_regimes()
