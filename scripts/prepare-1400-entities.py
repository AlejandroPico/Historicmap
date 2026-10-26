"""Canonical identities1400–1499 over original source geometry."""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
def prepare(ids):
 cs=ids['countries'];d=dict(format='dated-entity-resolution',coverageStart=1400,coverageEnd=1499,referenceDate='2026-10-26',qidKeys={},names={k:c['name'] for k,c in cs.items()},records=[])
 for k,c in cs.items():
  if c.get('qid'):d['qidKeys'].setdefault(c['qid'],k)
 for k in ['CASTILE','ARAGON','MUSCOVY','AZTEC','INCA','KALMAR','WATTASID','MAMLUKS','LODI','TIMURID','MING','JOS','SAXONY-ELECTORATE','ELECTORATE-BRANDENBURG','HUNGARY-KINGDOM','BOHEMIA','POLAND-KINGDOM','LITHUANIA-DUCHY','BYZANTINE','TREBIZOND','GRANADA-EMIRATE','BURGUNDY-DUCHY','NAVARRE-KINGDOM','MARINID','FLORENCE-REPUBLIC']:
  if cs.get(k,{}).get('qid'):d['qidKeys'][cs[k]['qid']]=k
 def rule(names,key,a=1400,b=1499,label=None,admin='',status='independent',note=''):
  d['records'].append(dict(names=names.split('|'),key=key,label=label or cs[key]['name'],entityCode=key,start=a,end=b,admin=admin,status=status,source='https://github.com/AlejandroPico/Historicmap/blob/main/docs/RESEARCH-1400.md',note=note+' Síntesis anual de fuente, sin contorno diario acreditado.'))
 for n,k in [('Kingdom of France','FRA'),('Crown of Castile','CASTILE'),('Crown of Aragon','ARAGON'),('Kingdom of Portugal','PRT'),('Kingdom of England','ENGLAND'),('Kingdom of Scotland','SCOTLAND'),('Grand Principality of Moscow','MUSCOVY'),('Ming Dynasty','MING'),('Timurid Empire','TIMURID'),('Ottoman Empire','OTT'),('Empire of Trebizond','TREBIZOND'),('Emirate of Granada','GRANADA-EMIRATE'),('Kingdom of Navarre','NAVARRE-KINGDOM'),('Grand Duchy of Lithuania','LITHUANIA-DUCHY'),('Marinid Sultanate','MARINID'),('Wattasid dynasty','WATTASID'),('Mamluk Sultanate','MAMLUKS'),('Lodi Dynasty','LODI'),('Kingdom of Hungary','HUNGARY-KINGDOM'),('Kingdom of Bohemia','BOHEMIA'),('Electorate of Saxony','SAXONY-ELECTORATE'),('Electorate of Brandenburg|Margraviate of Brandenburg','ELECTORATE-BRANDENBURG'),('Republic of Florence','FLORENCE-REPUBLIC'),('Republic of Venice','HIST-Q4948'),('Republic of Genoa','HIST-Q174306'),('Republic of Ragusa','HIST-Q208169'),('Papal States|Comtat Venaissin','PAPAL-STATES')]:rule(n,k)
 rule('Kingdom of Poland','POLAND-KINGDOM',note='Se corrige la referencia al reino anterior a1385. La unión dinástica no equivale a laMancomunidad formada en1569.')
 rule('Byzantine Empire','BYZANTINE',b=1453,note='Imperio restaurado con autoridad enConstantinopla. Trebisonda y los gobiernos delPeloponeso no son automáticamente el mismo ámbito de control.')
 rule('Byzantine Empire','BYZANTINE',a=1454,label='Dominios bizantinos residuales · referencia de fuente',status='source-reference',note='Constantinopla cae en1453. Una geometría residual posterior no acredita continuidad de un emperador ni de su control sobre el antiguo imperio.')
 rule('Holy Roman Empire|Holy Roman Empire Minor States','HIST-Q12548',label='Estados agrupados del Sacro Imperio',note='La dignidad imperial y las soberanías territoriales no son un país nacional único. Las sedes documentadas abren sus propias fichas.')
 rule('Habsburg Monarchy|House of Habsburg','HABSBURG-MONARCHY',status='source-reference',note='Casa y dominios con ramas distintas. El emperador no se convierte por su título en un gobernante único de todas las posesiones familiares.')
 rule('House of Jagiellon','JAGIELLON-DOMAINS',status='source-reference',note='Dinastía y múltiples coronas, no un único gobierno uniforme dePolonia,Lituania,Hungría yBohemia.')
 rule('House of Bourbon','BOURBON-DUCHY',note='Se conserva el dominio ducal de fuente; no se atribuye el reino francés a la dinastía borbónica antes de1589.')
 rule('County of Savoy|House of Savoy','SAVOY-COUNTY',b=1415)
 rule('County of Savoy|Duchy of Savoy|House of Savoy','SAVOY-DUCHY',a=1416,note='La dignidad ducal comienza en1416; no se anticipa al condado.')
 rule('Duchy of Burgundy','BURGUNDY-DUCHY',b=1476,note='El ducado francés y los otros dominios borgoñones tienen ámbitos distintos; no se deducen todas sus fronteras de la persona del duque.')
 rule('Duchy of Burgundy','BURGUNDY-DUCHY',a=1477,status='source-reference',label='Dominios borgoñones · sucesión y disputa',note='El ducado es ocupado porFrancia en1477; María conserva otros dominios y reclamaciones. El contorno persistente no acredita control continuo sobre el ducado francés.')
 rule('Duchy of Bavaria','BAVARIA-DUCHY',note='Varios ducados y ramas,Múnich,Landshut eIngolstadt. No se atribuye todo el contorno a un solo duque de una rama.')
 rule('County of Urgell','URGELL-COUNTY',b=1413)
 rule('County of Urgell','ARAGON',a=1414,label='Urgell · incorporado a la Corona deAragón',note='La soberanía condal independiente termina en1413.')
 rule('Joseon','JOS',note='JoseonQ28179, noGojoseon antiguoQ28405 de la fuente.')
 rule('Ashikaga Shogunate|Warring States Japan','JPN',label='Japón · shogunato y corte imperial',note='Corte,shogunes y poderes regionales coexisten. La guerra deŌnin no acredita una frontera nacional diaria entre facciones.')
 rule('Khmer Empire','KHM',label='Camboya · transición postangkoriana',note='La caída deAngkor y las continuidades regionales no se resuelven prolongando automáticamente una etiqueta imperial medieval.')
 rule('Kalmar Union','KALMAR',note='La unión tiene regencias y soberanos rivales. Un rey danés no controla continuamenteSuecia ni se convierte en monarca nacional de un Estado escandinavo uniforme.')
 rule('Old Kingdom of Norway','NORWAY-KINGDOM',note='ElQIDde fuente identifica aMargaritaI, una persona. La entidad correcta es el reinoQ2196956; los cargos noruegos no se infieren de todo el reinado danés.')
 rule('Aztec Triple Alliance','AZTEC',a=1428,note='Triple Alianza desde1428; los titulares mexicas no son un gobierno nacional uniforme de todas las ciudades tributarias.')
 rule('Aztec Triple Alliance','TENOCHTITLAN',b=1427,label='México-Tenochtitlan · antes de laTripleAlianza',note='No se anticipa la alianza de1428 a las fases previas.')
 rule('Tenochtitlan','TENOCHTITLAN',note='Ciudad-Estado mexica; no es automáticamente idéntica a toda laTripleAlianza.')
 rule('Cuzco','CUSCO-KINGDOM',note='Reino deCusco y cronología tradicional anterior a la expansión imperial; no se usa una bandera municipal contemporánea.')
 rule('Inca Empire','INCA',a=1438,note='Cronología tradicional de la expansión imperial. La datación arqueológica y las sucesiones tienen incertidumbres; no son fronteras diarias.')
 rule('Inca Empire','CUSCO-KINGDOM',b=1437,note='La fase imperial tradicional de1438 no se anticipa al reino anterior.')
 rule('Later Mayan City-States','HIST-Q28567',status='source-reference',label='Estados mayas · agregado de fuente',note='Civilización y múltiples ciudades, no un país de gobernante único.')
 for n,k in [('House of Luxembourg','LUXEMBOURG-DOMAINS'),('House of Oldenburg','OLDENBURG-DOMAINS'),('House of Ascania','ASCANIA-DOMAINS'),('House of Valois-Anjou','VALOIS-ANJOU-DOMAINS'),('House of Tocco','TOCCO-DOMAINS')]:rule(n,k,status='source-reference',note='ElQIDde una familia no acredita un solo Estado ni un único gobernante de todo el contorno. Serie territorial pendiente.')
 rule('Hashemite Arab Federation','UNRESOLVED-ARAB-SOURCE',status='source-reference',label='Territorio árabe · identidad de fuente sin resolver',note='La federación de1958 es anacrónica en este siglo. Se rechaza su identidad moderna y no se importan sus dirigentes; el contorno se mantiene sólo como referencia pendiente.')
 rule('Ngô Dynasty','UNRESOLVED-VIET-SOURCE',status='source-reference',label='Territorio vietnamita · referencia sin resolver',note='La dinastíaNgô del sigloX no acredita esta cronología de fuente delXV. No se asigna su gobernante por homonimia.')
 return d
if __name__=='__main__':
 d=prepare(json.loads((OUT/'identities.json').read_text(encoding='utf8')));(OUT/'historical-1400-entities.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n');print('Dated rules',len(d['records']))
