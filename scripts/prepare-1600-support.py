"""Institutional phases, sovereign seats, context and regional conflicts1600–1699."""
import pathlib,json,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='support-1600-0.20'
read=lambda f:json.loads((OUT/f).read_text(encoding='utf8'))
save=lambda f,d:(OUT/f).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
wiki=lambda t:'https://en.wikipedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_'))
def main():
 forms=read('governance.json');forms['records']=[r for r in forms['records'] if r.get('acquisition')!=TAG]
 def form(keys,a,b,tags,title,note=''):
  forms['records'].append(dict(keys=keys.split('|'),start=a,end=b,tags=tags.split('|'),source=wiki(title),sourceLabel='Forma institucional fechada · sigloXVII',priority=15,note=note or 'Forma institucional, no una evaluación democrática ni una ideología deducida del color.',acquisition=TAG))
 for keys,tags,title in [
 ('FRA','monarchy|kingdom','Ancien Régime'),('ESP|PRT','monarchy|kingdom','Iberian Union'),('IBERIAN-UNION|HABSBURG-MONARCHY|HIST-Q157367','monarchy|dynastic-union','Personal union'),
 ('ENGLAND|SCOTLAND','monarchy|kingdom','Union of the Crowns'),('DENMARK-NORWAY','monarchy|dynastic-union','Denmark–Norway'),('RUSSIA-TSARDOM','monarchy|kingdom','Tsardom of Russia'),('SWE','monarchy|kingdom','Swedish Empire'),
 ('SAXONY-ELECTORATE|ELECTORATE-BRANDENBURG','monarchy|electorate|feudal','Prince-elector'),('BAVARIA-DUCHY|SAVOY-DUCHY|WURTTEMBERG-DUCHY','monarchy|duchy|feudal','Duchy'),('HESSE-KASSEL|HESSE-DARMSTADT','monarchy|principality|feudal','Landgrave'),
 ('HIST-Q12548','elective-monarchy|empire|feudal','Holy Roman Empire'),('POLISH-LITHUANIAN','elective-monarchy|confederal','Polish–Lithuanian Commonwealth'),('DUTCH-REPUBLIC','republic|confederal|oligarchy','Dutch Republic'),('CHE','confederal','Old Swiss Confederacy'),
 ('HIST-Q4948|HIST-Q174306|HIST-Q208169','republic|oligarchy|city-state','Maritime republics'),('PAPAL-STATES','elective-monarchy|theocracy','Papal States'),
 ('MING|SOUTHERN-MING|QING','monarchy|empire','Ming–Qing transition'),('LATER-JIN','monarchy|khanate','Later Jin (1616–1636)'),('SHUN','monarchy|empire','Shun dynasty'),
 ('JPN','monarchy|feudal','Tokugawa shogunate'),('JOS|AYUTTHAYA','monarchy|kingdom','Early modern period'),('HIST-Q33296','monarchy|empire','Mughal Empire'),('SAFAVID','monarchy|empire','Safavid Iran'),('SAADI|OTT','monarchy|sultanate','Sultanate'),('ETH','monarchy|empire','Ethiopian Empire'),('HIST-Q796583','monarchy|kingdom','Kingdom of Kongo')]:form(keys,1600,1699,tags,title)
 form('BAVARIA-ELECTORATE',1623,1699,'monarchy|electorate|feudal','Electorate of Bavaria')
 form('ENGLISH-COMMONWEALTH',1649,1652,'republic|collective','Commonwealth of England')
 form('ENGLISH-COMMONWEALTH',1653,1658,'republic|military-administration','The Protectorate','LordProtector no es rey. La forma del Ejecutivo no equivale por sí sola a una puntuación democrática.')
 form('ENGLISH-COMMONWEALTH',1659,1659,'republic|collective','Rump Parliament')
 form('ENGLAND|SCOTLAND',1689,1699,'constitutional-monarchy|kingdom','Bill of Rights 1689')
 form('FRA',1661,1699,'absolute-monarchy','Louis XIV')
 form('PRT',1656,1662,'regency','Luisa de Guzmán')
 form('PRT',1668,1683,'regency','Peter II of Portugal')
 form('ESP',1665,1675,'regency','Mariana of Austria')
 form('RUSSIA-TSARDOM',1682,1689,'regency','Sophia Alekseyevna')
 form('HIST-Q83618',1674,1699,'monarchy|kingdom','Maratha Empire')
 save('governance.json',forms)
 cs=read('identities.json')['countries'];places=read('historical-places.json');places['records']=[r for r in places['records'] if r.get('acquisition')!=TAG]
 def city(k,n,xy,a=1600,b=1699,aggregate=False):
  r=dict(id='seat020-'+k+'-'+str(a),keys=[k],name=n,coordinates=xy,start=a,end=b,capital=True,role='Sede soberana · Estado agrupado' if aggregate else 'Capital o corte histórica',source='https://www.wikidata.org/wiki/'+cs[k]['qid'],note='Coordenada de una sede, no del perímetro urbano ni de un frente. No acredita presencia continua del gobernante durante ocupaciones o exilios.',acquisition=TAG)
  if aggregate:r.update(aggregateKey='HIST-Q12548',entityName=cs[k]['name'],note='El contorno de fuente agrupa este Estado dentro del Sacro Imperio. La sede abre su propia ficha; no inventa una frontera individual ni atribuye a su soberano todo el contorno imperial.')
  places['records'].append(r)
 for k,n,xy,a,b in [('HESSE-KASSEL','Kassel',[9.4797,51.3127],1600,1699),('HESSE-DARMSTADT','Darmstadt',[8.6512,49.8728],1600,1699),('SAXONY-ELECTORATE','Dresde',[13.7373,51.0504],1600,1699),('BAVARIA-DUCHY','Múnich',[11.582,48.1351],1600,1622),('BAVARIA-ELECTORATE','Múnich',[11.582,48.1351],1623,1699),('WURTTEMBERG-DUCHY','Stuttgart',[9.1829,48.7758],1600,1699)]:city(k,n,xy,a,b,True)
 for k,n,xy,a,b in [
 ('FRA','París',[2.3522,48.8566],1600,1699),('ESP','Madrid',[-3.7038,40.4168],1600,1699),('PRT','Lisboa',[-9.1393,38.7223],1600,1699),('IBERIAN-UNION','Lisboa · instituciones portuguesas',[-9.1393,38.7223],1600,1639),
 ('ENGLAND','Londres',[-.1278,51.5074],1600,1648),('ENGLAND','Londres',[-.1278,51.5074],1660,1699),('ENGLISH-COMMONWEALTH','Londres',[-.1278,51.5074],1649,1659),('SCOTLAND','Edimburgo',[-3.1883,55.9533],1600,1651),('SCOTLAND','Edimburgo',[-3.1883,55.9533],1660,1699),
 ('RUSSIA-TSARDOM','Moscú',[37.6173,55.7558],1600,1699),('PAPAL-STATES','Roma',[12.4964,41.9028],1600,1699),('HABSBURG-MONARCHY','Viena',[16.3738,48.2082],1600,1699),('DUTCH-REPUBLIC','La Haya',[4.3007,52.0705],1600,1699),
 ('MING','Pekín',[116.4074,39.9042],1600,1643),('QING','Shenyang',[123.4315,41.8057],1636,1643),('LATER-JIN','Shenyang',[123.4315,41.8057],1625,1635),('QING','Pekín',[116.4074,39.9042],1644,1699),('SOUTHERN-MING','Nankín',[118.7969,32.0603],1644,1645),('JOS','Hanseong',[126.978,37.5665],1600,1699),
 ('JPN','Kioto · corte imperial',[135.7681,35.0116],1600,1699),('JPN','Edo · Gobierno shogunal',[139.7528,35.6852],1603,1699),('SAFAVID','Isfahán',[51.6776,32.6546],1600,1699),('AYUTTHAYA','Ayutthaya',[100.5574,14.3532],1600,1699),('OTT','Constantinopla',[28.9784,41.0082],1600,1699)]:city(k,n,xy,a,b)
 save('historical-places.json',places)
 context=read('historical-context.json');history=read('country-history.json');points=read('conflict-points.geojson')
 context['events']=[e for e in context['events'] if not e['id'].startswith('review020-')];history['records']=[e for e in history['records'] if not e['id'].startswith('review020-')];points['features']=[e for e in points['features'] if not str(e['id']).startswith('review020-')]
 rows=[
 ('thirty','conflict','HIST-Q12548|HABSBURG-MONARCHY|FRA|SWE|ESP|BAVARIA-ELECTORATE|SAXONY-ELECTORATE',1618,1648,'Guerra de los Treinta Años','Múltiples guerras, alianzas y ocupaciones dentro y fuera del Sacro Imperio. La paz deWestfalia no convierte todos los Estados miembros en una nación única. El punto es regional; no reconstruye campañas ni fronteras de ocupación.','Thirty Years War',[12,49]),
 ('dutch','conflict','DUTCH-REPUBLIC|ESP',1600,1648,'Guerra de los Ochenta Años · tramo observado','El conflicto de independencia neerlandés comienza antes de1600. La tregua de1609–1621 y el reconocimiento de1648 son fases distintas; la continuidad de este registro no significa combates constantes.','Eighty Years War',[4.5,51.5]),
 ('english','conflict','ENGLAND|SCOTLAND|ENGLISH-COMMONWEALTH',1642,1651,'Guerras civiles e interregno británico','Parlamentarios y realistas, las guerras deEscocia eIrlanda y el establecimiento de la república son procesos relacionados. No se anticipa laCommonwealth antes de1649 ni laRestauración antes de1660.','English Civil War',[-1.5,52]),
 ('commonwealth','transition','ENGLAND|SCOTLAND|ENGLISH-COMMONWEALTH',1649,1660,'Commonwealth, Protectorado y Restauración','La abolición de la monarquía, los dosLordProtectors y el retorno deCarlosII son fases distintas. La lista anual puede incluir varios titulares; no asigna aCarlosII el gobierno efectivo inglés durante todo el interregno.','The Protectorate',None),
 ('iberian','transition','ESP|PRT|IBERIAN-UNION',1600,1640,'Unión ibérica · coronas e instituciones','El mismo monarca ocupa las coronas española y portuguesa, con numeración regia y administraciones distintas. No es una anexión uniforme dePortugal ni de todas sus colonias. La unión comienza en1580, antes de esta ventana.','Iberian Union',None),
 ('portugal','conflict','PRT|ESP|IBERIAN-UNION',1640,1668,'Restauración portuguesa','La proclamación deJoãoIV de1640 y el reconocimiento de la independencia en1668 son hechos distintos. No se prolonga la unión dinástica hasta1668 por confundir reconocimiento con gobierno.','Portuguese Restoration War',[-8,39]),
 ('russia','conflict','RUSSIA-TSARDOM|POLISH-LITHUANIAN|SWE',1600,1613,'Rusia · Tiempo de las Turbulencias','Sucesiones disputadas, pretendientes e intervención extranjera impiden representar este período como un mandato continuo estable. La elección deMiguelRománov de1613 no borra los gobiernos y reclamaciones anteriores.','Time of Troubles',[37,56]),
 ('ming','conflict','MING|SOUTHERN-MING|LATER-JIN|QING|SHUN',1618,1683,'Transición Ming–Qing y regímenes rivales','El acceso de losQing aPekín en1644 no es una sustitución instantánea de todos los gobiernos chinos. Ming delSur, Shun y otras resistencias tienen ámbitos y cronologías diferentes; no se asigna una bandera nacional tardía a todo el siglo.','Transition from Ming to Qing',[114,32]),
 ('japan','transition','JPN',1600,1615,'Japón · Sekigahara y consolidación Tokugawa','Sekigahara en1600, el nombramiento shogunal de1603 y la caída deOsaka en1615 son eventos diferentes. El emperador y el shogun conservan fichas de cargos distintos; los contornos de fuente no representan todos los dominios feudales.','Tokugawa shogunate',None),
 ('france','transition','FRA',1643,1661,'Francia · regencia, Fronda y gobierno personal','La minoría deLuisXIV incluye regencia y conflicto interno. Su acceso al trono en1643 no es el comienzo de su gobierno personal de1661.','Louis XIV',None),
 ('safavid','transition','SAFAVID|OTT|HIST-Q33296',1600,1699,'Persia safávida · soberanía y rivalidades','Los reinados safávidas y sus conflictos con otomanos y mogoles no se deducen de una simple sucesión de colores. Las enseñas y los frentes necesitan evidencia propia; no se retrotraen banderas persas posteriores.','Safavid Iran',None),
 ('maratha','transition','HIST-Q83618|HIST-Q33296',1674,1699,'Poder maratha y monarquía mogola','La coronación deShivaji en1674 se distingue de su poder militar previo. La expansión regional y las reclamaciones imperiales coexisten; un título no acredita control uniforme sobre todo el subcontinente.','Maratha Empire',None),
 ('kongo','conflict','HIST-Q796583|PRT',1665,1699,'Kongo · guerra civil y autoridades rivales','La batalla deMbwila y la crisis sucesoria abren una guerra civil con facciones y poderes regionales. No se interpola un único rey de todo el territorio después de1665. Este registro termina en el límite de cobertura, no en la fecha de paz.','Kongo Civil War',[14, -6]),
 ('ethiopia','transition','ETH|HIST-Q207521',1632,1667,'Etiopía · reinado deFasilides','Cambios religiosos y consolidación deGondar durante el reinado deFasilides. La ventana de un gobernante no equivale a fronteras de control territorial exactas.','Fasilides',None),
 ('westphalia','transition','HIST-Q12548|DUTCH-REPUBLIC|CHE|HABSBURG-MONARCHY',1648,1648,'Paz deWestfalia','Los tratados reconocen y reorganizan relaciones de soberanía; las identidades neerlandesa, confederal suiza e imperial no son intercambiables. No se reemplaza retrospectivamente todo el mapa europeo por las fronteras de1648.','Peace of Westphalia',None)]
 for id,kind,keys,a,b,title,text,ref,xy in rows:
  e=dict(id='review020-'+id,type=kind,countries=keys.split('|'),title=title,start=f'{a}-01-01',end=f'{b+1}-01-01',text=text,source=wiki(ref),sourceLabel='Referencia documental · sigloXVII',precision=9,startIsCoverageBoundary=True,endIsCoverageBoundary=True,note='Síntesis anual y documental parcial. No acredita una geometría diaria de control.')
  if id=='commonwealth':e['source']='https://www.royal.uk/interregnum-1649-1660'
  if id=='russia':e['source']='https://www.loc.gov/item/2021666631/'
  context['events'].append(e);history['records'].append(dict(id=e['id'],keys=e['countries'],section='history' if kind=='conflict' else 'institutions',**{k:v for k,v in e.items() if k not in ['id','countries','type']}))
  if xy:points['features'].append(dict(type='Feature',id=e['id'],geometry=dict(type='Point',coordinates=xy),properties=dict(name=title,countries=e['countries'],kind='regional-conflict',start=e['start'],end=f'{b}-12-31',precision=9,source=e['source'],sourceLabel=e['sourceLabel'],note=text+' Referencia regional; no representa un frente ni superficie ocupada.')))
 context['startYear']=1600;history['coverageStart']=1600;save('historical-context.json',context);save('country-history.json',history);save('conflict-points.geojson',points)
 print('Forms',len(forms['records']),'places',len(places['records']),'new context',len(rows))
if __name__=='__main__':main()
