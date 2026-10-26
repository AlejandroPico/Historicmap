"""Bounded1800–1819 office curation; keep all previously published facts."""
import pathlib,json,copy
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1800-0.17'
read=lambda f:json.loads((OUT/f).read_text(encoding='utf8'))
def combined_pitt(l):return l['person']=='Q128902' and l['start'] in ['1783-12-19','1800-01-01'] and l['end']=='1806-01-23'
def prepare(incoming,research):
 d=copy.deepcopy(incoming);cs=d['countries'];images={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 # Reject the condensed interval across Addington; retain the two real terms.
 cs['GBR']['leaders']=[l for l in cs['GBR']['leaders'] if not combined_pitt(l)]
 for k in ['RUE','HTI']:
  cs[k]['leaders']=[l for l in cs[k]['leaders'] if not(l.get('acquisition')=='historical-0.17' and (k=='RUE' and l['person'] in ['Q15189','Q15193'] or k=='HTI' and l['person']=='Q353464'))]
 titles={'PRUSSIA':'Rey de Prusia','SAR':'Rey de Cerdeña','QING':'Emperador de la dinastía Qing','JOS':'Rey de Joseon','IRN':'Shah de Persia · dinastía Qajar','AUSTRIAN-EMPIRE':'Emperador de Austria','PAPAL-STATES':'Papa · soberano de los Estados Pontificios','JPN':'Shogun · Gobierno militar'}
 for item in research['records']:
  k=item['key'];l=copy.deepcopy(item['term']);l['acquisition']=TAG;l['role']=titles.get(k,l['role'])
  if l['person'] in images:l['portrait']=copy.deepcopy(images[l['person']])
  cs.setdefault(k,dict(qid='',name=k,flags=[],leaders=[]))['leaders'].append(l)
 if 'HIST-Q12548' in cs:
  for l in cs['HIST-Q12548']['leaders']:
   if l.get('acquisition')=='historical-0.17':l.update(role='Emperador del Sacro Imperio',name='Francisco II')
  cs['HIST-Q12548']['territoryStatus']=dict(start='1800-01-01',end='1806-12-31',text='Agregado de Estados del Sacro Imperio en la fuente, no un Estado nacional unitario. El emperador no sustituye a todos sus gobernantes locales.',source='https://github.com/Seshat-Global-History-Databank/cliopatria')
 def term(k,q,name,role,a,b,url='',precision=11,note=''):
  cs.setdefault(k,dict(qid='',name=k,flags=[],leaders=[]))
  l=dict(person=q,name=name,role=role,start=a,end=b,source=url or 'https://www.wikidata.org/wiki/'+q,precision=precision,curated=True,acquisition=TAG,note=note)
  if a=='1800-01-01' or precision<11:l['startIsCoverageBoundary']=True
  if b=='1819-12-31' or precision<11:l['endIsCoverageBoundary']=True
  if q in images:l['portrait']=copy.deepcopy(images[q])
  cs[k]['leaders'].append(l)
 term('RUE','Q15189','Pablo I','Emperador de Rusia','1800-01-01','1801-03-24',note='Fecha gregoriana. Se rechaza la fecha divergente de marzo de la otra declaración; no representa una segunda sucesión.')
 term('RUE','Q15193','Alejandro I','Emperador de Rusia','1801-03-24','1819-12-31',note='Fecha gregoriana; el extremo de cobertura no es un cese.')
 term('GBR','Q127318','Jorge III','Rey del Reino Unido','1800-01-01','1819-12-31',note='En1800 es rey de Gran Bretaña e Irlanda, coronas todavía distintas; Reino Unido desde1801. La enfermedad no convierte al regente en rey.')
 term('GBR','Q130586','Jorge, príncipe de Gales','Príncipe regente','1811-12-31','1819-12-31',precision=9,note='Observación anual de la regencia iniciada1811; no accede al trono hasta1820.')
 term('ESP','Q186256','Fernando VII','Rey ausente reconocido por las Cortes','1812-03-19','1813-12-31','https://www.congreso.es/constitucion/ficheros/historicas/cons_1812.pdf',note='Soberano reconocido por las instituciones fernandinas durante su cautividad; no gobierno efectivo sobre el territorio josefino.')
 term('ESP','REGENCY-CADIZ-1812','Regencia del Reino','Ejecutivo fernandino en ausencia del rey','1812-03-19','1813-12-31','https://www.congreso.es/constitucion/ficheros/historicas/cons_1812.pdf',note='Órgano colectivo descrito por la Constitución; observación desde su promulgación, no fecha de creación de todas las regencias.')
 term('IRN','Q175299','Fath Alí Shah','Shah de Persia · dinastía Qajar','1800-01-01','1819-12-31')
 term('EGY','Q182781','Muhammad Alí','Valí de Egipto','1805-12-31','1819-12-31','https://sis.gov.eg/en/egypt/history/egypts-history/modern-era/',9,'Observación desde1805; no se proyecta su gobierno sobre la ocupación francesa anterior.')
 term('HAW-KINGDOM','Q214910','Kamehameha I','Rey de Hawái','1800-01-01','1819-01-01',precision=9,note='Observación anual interior del reinado. No convierte todas las relaciones insulares anteriores en administración uniforme.')
 term('ITALIAN-REPUBLIC-1802','Q517','Napoleón Bonaparte','Presidente de la República Italiana','1803-01-01','1804-12-31',precision=9,note='Ventana anual interior; presidencia distinta del consulado francés.')
 term('NAPOLEONIC-ITALY','Q517','Napoleón I','Rey de Italia','1805-12-31','1813-12-31',precision=9,note='Reino napoleónico, distinto del Estado italiano de1861. Ventana conservadora; falta detallar virreinato y disolución.')
 term('NAPLES-BOURBON','Q312325','Fernando IV de Nápoles','Rey de Nápoles','1800-01-01','1805-12-31',precision=9,note='El mismo protagonista será Fernando I de las Dos Sicilias desde1816; no anticipar ese Estado.')
 term('NAPOLEONIC-NAPLES','Q7726','José Bonaparte','Rey de Nápoles','1806-12-31','1808-01-01',precision=9,note='Ventana interior de su gobierno napolitano, distinta de su posterior reinado español.')
 term('NAPOLEONIC-NAPLES','Q151173','Joaquín Murat','Rey de Nápoles','1808-12-31','1814-12-31',precision=9,note='Observación interior; la caída y restauración de1815 requieren una fase propia.')
 term('HTI','Q212068','Jean-Jacques Dessalines','Emperador Jacques I','1804-12-31','1806-01-01','https://pegasus.law.columbia.edu/record/127791',9,'Observación anual. La independencia del1/1/1804 y la proclamación imperial posterior son hitos distintos; falta separar sus cargos intranuales.')
 term('HTI','Q353464','Alexandre Pétion','Presidente de la república del sur','1807-12-31','1818-03-29',precision=9,note='Se rechaza la declaración de inicio1806; ventana interior de la presidencia iniciada1807. No soberano de toda la isla.')
 term('HTI','Q353458','Henri Christophe','Presidente del Estado del norte','1807-12-31','1810-12-31',precision=9,note='Agregado de fuente sin partición norte-sur resuelta; observación interior anterior a la monarquía.')
 term('HTI','Q353458','Henri I · Henri Christophe','Rey del norte de Haití','1811-12-31','1819-12-31',precision=9,note='Observación interior desde el año de la proclamación monárquica; no soberano de la república del sur.')
 names={'ITALIAN-REPUBLIC-1802':'República Italiana napoleónica','NAPOLEONIC-ITALY':'Reino de Italia napoleónico','NAPLES-BOURBON':'Reino de Nápoles borbónico','NAPOLEONIC-NAPLES':'Reino de Nápoles napoleónico'}
 for k,name in names.items():cs[k]['name']=name
 return d
if __name__=='__main__':
 old=read('identities.json');research=json.loads((ROOT/'.cache/historical-offices-017.json').read_text(encoding='utf8'));d=prepare(old,research);assert prepare(d,research)==d
 for k,c in old['countries'].items():assert all(l in d['countries'][k]['leaders'] for l in c['leaders'] if l.get('acquisition') not in [TAG,'historical-0.17'] and not combined_pitt(l)),k
 (OUT/'identities.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
 (ROOT/'scripts/historical-offices-017-research.json').write_text(json.dumps(research,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('Curated dated offices; later records preserved and condensed Pitt interval rejected')
