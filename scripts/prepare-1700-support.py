"""Dated forms, courts, German sovereign seats and context1700–1799.

Seats disclose source aggregation; they do not invent individual state borders.
Context points identify episodes, never military control polygons.
"""
import pathlib,json,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='review-1700-0.19'
read=lambda f:json.loads((OUT/f).read_text(encoding='utf8'))
save=lambda f,d:(OUT/f).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
wiki=lambda t:'https://en.wikipedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_'))
def main():
 forms=read('governance.json');forms['records']=[r for r in forms['records'] if r.get('acquisition')!=TAG]
 def form(keys,a,b,tags,source,note=''):
  forms['records'].append(dict(keys=keys.split('|'),start=a,end=b,tags=tags.split('|'),source=wiki(source),sourceLabel='Forma institucional fechada · investigación1700',priority=15,note=note or 'Clasificación institucional; no evaluación democrática ni ideología deducida del color.',acquisition=TAG))
 for keys,tags,title in [
 ('BAVARIA-ELECTORATE|SAXONY-ELECTORATE|HANOVER-ELECTORATE','monarchy|electorate|feudal','Electorate'),
 ('HESSE-KASSEL|HESSE-DARMSTADT','monarchy|principality|feudal','Landgrave'),
 ('WURTTEMBERG-DUCHY|SAXE-WEIMAR|BRUNSWICK-WOLFENBUTTEL|MECKLENBURG-SCHWERIN','monarchy|duchy|feudal','Holy Roman Empire'),
 ('BADEN-DURLACH|BADEN-BADEN','monarchy|principality|feudal','Margraviate of Baden'),
 ('HABSBURG-MONARCHY|HIST-Q157367','monarchy|dynastic-union','Habsburg monarchy'),
 ('HIST-Q12548','elective-monarchy|empire|feudal','Holy Roman Empire'),
 ('RUSSIA-TSARDOM','absolute-monarchy|kingdom','Tsardom of Russia'),
 ('RUE','absolute-monarchy|empire','Russian Empire'),
 ('QING','monarchy|empire','Qing dynasty'),
 ('JPN','monarchy|feudal','Tokugawa shogunate'),
 ('JOS','monarchy|kingdom','Joseon'),
 ('SAFAVID|AFSHARID|ZAND|IRN','monarchy|dynastic-union','History of Iran'),
 ('HIST-Q33296','monarchy|empire','Mughal Empire'),
 ('HIST-Q83618','monarchy|confederal','Maratha Confederacy'),
 ('OTT','monarchy|empire|sultanate','Ottoman Empire'),
 ('PRT|ESP','absolute-monarchy|kingdom','Enlightened absolutism'),
 ('DENMARK-NORWAY','absolute-monarchy|dynastic-union','Denmark–Norway'),
 ('POLISH-LITHUANIAN','elective-monarchy|confederal','Polish–Lithuanian Commonwealth'),
 ('DUTCH-REPUBLIC','republic|confederal|oligarchy','Dutch Republic'),
 ('PAPAL-STATES','elective-monarchy|theocracy','Papal States'),
 ('HIST-Q208169|HIST-Q47261','republic|oligarchy|city-state','Republic of Ragusa'),
 ('SAVOY-DUCHY','monarchy|duchy','Duchy of Savoy'),
 ('SAR','monarchy|kingdom','Kingdom of Sardinia'),
 ('AYUTTHAYA|THONBURI|THA','monarchy|kingdom','History of Thailand'),
 ('ENGLAND|SCOTLAND|GBR','constitutional-monarchy|kingdom','Acts of Union 1707')]:form(keys,1700,1799,tags,title)
 form('MECKLENBURG-STRELITZ',1701,1799,'monarchy|duchy|feudal','Duchy of Mecklenburg-Strelitz')
 form('LIPPE-COUNTY',1700,1788,'monarchy|county|feudal','County of Lippe')
 form('HIST-Q14551680',1789,1799,'monarchy|principality','Principality of Lippe')
 form('FRA',1700,1788,'absolute-monarchy|kingdom','Ancien Régime')
 # Existing dated revolutionary records1789+ take over without a competing broad tag.
 save('governance.json',forms)
 places=read('historical-places.json');places['records']=[r for r in places['records'] if r.get('acquisition')!=TAG];cs=read('identities.json')['countries']
 def city(key,name,coord,a=1700,b=1799,aggregate=False,title=None):
  id='seat019-'+key+'-'+str(a)
  r=dict(id=id,keys=[key],name=name,coordinates=coord,start=a,end=b,capital=True,role='Sede soberana · Estado agrupado en la fuente' if aggregate else 'Capital o corte histórica',source=wiki(title) if title else 'https://www.wikidata.org/wiki/'+cs[key]['qid'],note='La coordenada localiza una sede, no una frontera ni la extensión urbana.',acquisition=TAG)
  if aggregate:r.update(aggregateKey='HIST-Q12548',entityName=cs[key]['name'],note='La fuente agrupa este Estado dentro del Sacro Imperio. La ficha documenta su soberano y símbolo; el punto localiza su sede, sin atribuirle el contorno imperial ni inventar límites particulares.')
  places['records'].append(r)
 for k,n,xy,a,b in [
 ('SAXONY-ELECTORATE','Dresde',[13.7373,51.0504],1700,1799),('BAVARIA-ELECTORATE','Múnich',[11.582,48.1351],1700,1799),
 ('HESSE-KASSEL','Kassel',[9.4797,51.3127],1700,1799),('HESSE-DARMSTADT','Darmstadt',[8.6512,49.8728],1700,1799),
 ('WURTTEMBERG-DUCHY','Stuttgart',[9.1829,48.7758],1700,1799),('SAXE-WEIMAR','Weimar',[11.329,50.98],1700,1799),
 ('BRUNSWICK-WOLFENBUTTEL','Wolfenbüttel',[10.5344,52.163],1700,1752),('BRUNSWICK-WOLFENBUTTEL','Braunschweig',[10.5268,52.2689],1753,1799),
 ('HANOVER-ELECTORATE','Hannover',[9.732,52.3759],1700,1799),('LIPPE-COUNTY','Detmold',[8.8815,51.9385],1700,1788),('HIST-Q14551680','Detmold',[8.8815,51.9385],1789,1799),
 ('MECKLENBURG-SCHWERIN','Schwerin',[11.407,53.6355],1700,1799),('MECKLENBURG-STRELITZ','Neustrelitz',[13.069,53.361],1733,1799),
 ('BADEN-DURLACH','Durlach',[8.4708,48.999],1700,1714),('BADEN-DURLACH','Karlsruhe',[8.4037,49.0069],1715,1770),('BADEN-BADEN','Rastatt',[8.2,48.857],1705,1770)]:city(k,n,xy,a,b,True)
 for k,n,xy,a,b in [
 ('FRA','París',[2.3522,48.8566],1700,1799),('ESP','Madrid',[-3.7038,40.4168],1700,1799),('PRT','Lisboa',[-9.1393,38.7223],1700,1799),
 ('RUSSIA-TSARDOM','Moscú',[37.6173,55.7558],1700,1711),('RUSSIA-TSARDOM','San Petersburgo',[30.3351,59.9343],1712,1720),('RUE','San Petersburgo',[30.3351,59.9343],1721,1799),
 ('JPN','Edo',[139.7528,35.6852],1700,1799),('JOS','Hanseong',[126.978,37.5665],1700,1799),('QING','Pekín',[116.4074,39.9042],1700,1799),
 ('SAFAVID','Isfahán',[51.6776,32.6546],1700,1721),('ZAND','Shiraz',[52.5311,29.5918],1762,1793),('THONBURI','Thonburi',[100.4764,13.7292],1767,1781),('THA','Bangkok',[100.5018,13.7563],1782,1799),
 ('ENGLAND','Londres',[-.1278,51.5074],1700,1706),('GBR','Londres',[-.1278,51.5074],1707,1799),('PAPAL-STATES','Roma',[12.4964,41.9028],1700,1799)]:city(k,n,xy,a,b)
 save('historical-places.json',places)
 history=read('historical-context.json');workspace=read('country-history.json');points=read('conflict-points.geojson')
 history['events']=[e for e in history['events'] if not e['id'].startswith('review019-')];workspace['records']=[e for e in workspace['records'] if not e['id'].startswith('review019-')];points['features']=[e for e in points['features'] if not str(e['id']).startswith('review019-')]
 rows=[
 ('succession','conflict','ESP|FRA|ENGLAND|GBR|HABSBURG-MONARCHY',1701,1714,'Guerra de Sucesión española','Conflicto dinástico y europeo por la sucesión de Carlos II. Felipe V y el archiduque Carlos sostienen pretensiones rivales; los tratados de1713–1714 redistribuyen dominios, sin convertir la síntesis anual en un frente diario.','War of the Spanish Succession',[4.35,50.85]),
 ('northern','conflict','RUSSIA-TSARDOM|RUE|SWE|POLISH-LITHUANIAN|DENMARK-NORWAY',1700,1721,'Gran Guerra del Norte','La guerra altera el equilibrio báltico y concluye con la expansión rusa. La localización es regional, no una superficie de ocupación.','Great Northern War',[24.1,57]),
 ('union','transition','ENGLAND|SCOTLAND|GBR',1707,1707,'Unión de Inglaterra y Escocia','La unión parlamentaria forma el Reino de Gran Bretaña en1707. La unión personal de las coronas anterior no era todavía este mismo Estado.','Acts of Union 1707',None),
 ('russian','transition','RUSSIA-TSARDOM|RUE',1721,1721,'Del zarato al título imperial ruso','Pedro I adopta el título imperial. El cambio de denominación no implica que todas las posesiones aparecieran de una vez en1721.','Peter the Great',None),
 ('austrian','conflict','HABSBURG-MONARCHY|PRUSSIA|BAVARIA-ELECTORATE|FRA|GBR',1740,1748,'Guerra de Sucesión austriaca','María Teresa disputa la conservación de sus dominios. La dignidad imperial de Carlos VII y la monarquía de Habsburgo son cargos y conjuntos distintos.','War of the Austrian Succession',[16,49]),
 ('seven','conflict','PRUSSIA|GBR|FRA|HABSBURG-MONARCHY|RUE',1756,1763,'Guerra de los Siete Años','Guerra europea y colonial de múltiples escenarios. No se deducen ocupaciones locales únicamente de que una potencia participe en el conflicto.','Seven Years War',[13,51]),
 ('india','transition','HIST-Q33296|HIST-Q83618|GBR',1757,1799,'India · soberanía imperial y poderes regionales','La autoridad mogola, la expansión maratha y el poder de compañías europeas se solapan con numerosos Estados regionales. La existencia de un título imperial no acredita control homogéneo.','History of India',None),
 ('japan','transition','JPN',1700,1799,'Japón · corte imperial y shogunato Tokugawa','La corte imperial y el Gobierno militar de Edo son instituciones diferentes. El mon Tokugawa se identifica como emblema dinástico, sin presentar un pabellón naval del sigloXIX como bandera nacional delXVIII.','Tokugawa shogunate',None),
 ('china','transition','QING',1700,1799,'Qing · monarquía y Ocho Banderas','Los emperadores Qing gobiernan un imperio multiétnico. Las enseñas de las Ocho Banderas pertenecen a instituciones militares; no equivalen a una bandera nacional uniforme con dragón del sigloXIX.','Eight Banners',None),
 ('korea','transition','JOS',1700,1799,'Joseon · monarquía e investidura','Los sellos reales acreditan la autoridad monárquica y sus relaciones de investidura. Se distinguen de la bandera nacional coreana desarrollada a finales del sigloXIX.','Joseon',None),
 ('persia','conflict','SAFAVID|AFSHARID|ZAND|IRN',1722,1794,'Persia · caída safávida y poderes sucesores','Las fases hotaki, afshárida, zand y qajar no forman una sucesión pacífica uniforme. Varias reclamaciones y dominios regionales coinciden; las ventanas documentales no acreditan control de toda Persia.','History of Iran',[54,32]),
 ('america','conflict','USA|GBR|FRA|ESP',1775,1783,'Guerra de Independencia estadounidense','La declaración de1776 y el reconocimiento de1783 son hitos distintos. Las fronteras anuales de fuente no reconstruyen cada campaña.','American Revolutionary War',[-75,40]),
 ('partitions','transition','POLISH-LITHUANIAN|PRUSSIA|RUE|HABSBURG-MONARCHY',1772,1795,'Particiones de Polonia-Lituania','Las particiones de1772,1793 y1795 reducen y finalmente extinguen la Mancomunidad. El filtro institucional no debe prolongarla como un Estado moderno sucesor.','Partitions of Poland',None),
 ('siam','transition','AYUTTHAYA|THONBURI|THA',1767,1782,'Siam · de Ayutthaya a Thonburi y Bangkok','La caída de Ayutthaya, el reino de Taksin y la dinastía Chakri son etapas distintas. El pabellón rojo es una referencia marítima, no una afirmación de normalización nacional moderna.','History of Thailand',None),
 ('hre','transition','HIST-Q12548|BAVARIA-ELECTORATE|SAXONY-ELECTORATE|HANOVER-ELECTORATE|HESSE-KASSEL|HESSE-DARMSTADT|WURTTEMBERG-DUCHY|SAXE-WEIMAR|BRUNSWICK-WOLFENBUTTEL|LIPPE-COUNTY|MECKLENBURG-SCHWERIN|MECKLENBURG-STRELITZ|BADEN-DURLACH|BADEN-BADEN',1700,1799,'Sacro Imperio · soberanías territoriales y dignidad imperial','Los Estados imperiales conservan autoridades particulares. La fuente cartográfica agrupa numerosos Estados; sus sedes permiten abrir fichas documentadas, sin atribuirles el contorno de todo el Imperio.','Holy Roman Empire',None)]
 for id,kind,keys,a,b,title,text,source,xy in rows:
  e=dict(id='review019-'+id,type=kind,countries=keys.split('|'),title=title,start=f'{a}-01-01',end=f'{b+1}-01-01',text=text,source=wiki(source),sourceLabel='Referencia histórica · investigación1700–1799',precision=9,startIsCoverageBoundary=True,endIsCoverageBoundary=True,note='Síntesis anual; cobertura documental parcial. No acredita una frontera o un frente exactos.')
  history['events'].append(e);workspace['records'].append(dict(id=e['id'],keys=e['countries'],section='history' if kind=='conflict' else 'institutions',**{k:v for k,v in e.items() if k not in ['id','countries','type']}))
  if xy:points['features'].append(dict(type='Feature',id=e['id'],geometry=dict(type='Point',coordinates=xy),properties=dict(name=title,countries=e['countries'],kind='regional-conflict',start=e['start'],end=f'{b}-12-31',precision=9,source=e['source'],sourceLabel=e['sourceLabel'],note=text+' Punto regional orientativo; no representa un frente ni una ocupación.')))
 history['startYear']=1700;workspace['coverageStart']=1700
 save('historical-context.json',history);save('country-history.json',workspace);save('conflict-points.geojson',points)
 print('Forms',len(forms['records']),'urban references',len(places['records']),'new context',len(rows))
if __name__=='__main__':main()
