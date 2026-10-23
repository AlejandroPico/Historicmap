"""Incremental sourced memberships and focal context, 1960–1969. Not a global conflict census."""
import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]/'public/data'
read=lambda f:json.loads((root/f).read_text(encoding='utf8'))
def save(f,d):(root/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
d=read('affiliations.json');orgs={o['id']:o for o in d['organizations']}
def add(oid,code,start,end=None,category='member',note='',source=None,boundary=False):
 o=orgs[oid];m=dict(code=code,start=start,category=category,source=source or o['source'])
 if end:m['end']=end
 if note:m['note']=note
 if boundary:m['startIsCoverageBoundary']=True
 if not any(x['code']==code and x['start']==start and x['category']==category for x in o['memberships']):o['memberships'].append(m)

for oid,o in orgs.items():
 for m in o['memberships']:
  if m['start']!='1970-01-01':continue
  code=m['code'];start='1960-01-01';boundary=True
  note='Pertenencia anterior al inicio de la serie de 1960; no fecha jurídica de adhesión.'
  if oid=='arabLeague':
   dates={'DZA':'1962-12-31','KWT':'1961-12-31','YAR':'1962-09-26','YPR':'1967-12-31'}
   if code in dates:start=dates[code];boundary=False;note='Ingreso o continuidad de entidad durante el año indicado; observación al cierre anual cuando falta día jurídico. No se asigna al Estado sucesor antes de su existencia.'
  elif oid=='au' and code=='MUS':start='1968-12-31';boundary=False;note='Ingreso documentado en agosto de 1968; observación al cierre anual, sin inventar día jurídico.'
  elif oid=='efta' and code=='FIN':start='1961-12-31';boundary=False;note='Asociación desde 1961; observación al cierre anual, distinta de la membresía plena desde 1986.'
  elif oid=='comecon':
   dates={'MNG':'1962-12-31','YUG':'1964-12-31','ALB':'1961-12-31'}
   if code in dates:start=dates[code];boundary=False;note='Observación al cierre del año documentado: admisión de Mongolia, asociación sectorial yugoslava o inactividad albanesa, según categoría; no día jurídico exacto.'
  elif oid=='oas':
   dates={'BRB':'1967-12-31','TTO':'1967-12-31','JAM':'1969-12-31'}
   if code in dates:start=dates[code];boundary=False;note='Ingreso en el año documentado por la OEA; observación al cierre anual, no día jurídico.'
  m['start']=start;m['note']=note
  if boundary:m['startIsCoverageBoundary']=True
  else:m.pop('startIsCoverageBoundary',None)
add('comecon','ALB','1960-01-01','1961-12-31',note='Actividad anterior a la ruptura de 1961; límite de cobertura inicial. La categoría posterior distingue inactividad, no una expulsión formal.',boundary=True)
add('warsaw','ALB','1960-01-01','1968-09-13',note='Membresía formal hasta retirada de 13/9/1968; participación inactiva desde 1961. No equivale a tutela soviética después de la ruptura.',source='https://www.nato.int/cps/en/natohq/declassified_138294.htm',boundary=True)
add('arabLeague','YMK','1960-01-01','1962-09-26',note='Reino de Yemen: identidad anterior a la república, sin proyectar la jefatura republicana al reino.',boundary=True)
for o in orgs.values():o['memberships'].sort(key=lambda m:(m['code'],m['start'],m['category']))
d['coverageStart']=1960;d['expandedReferenceDate']='2026-10-23';save('affiliations.json',d)

c=read('historical-context.json');c['events']=[e for e in c['events'] if not e['id'].startswith('extension-1960-')]
def event(id,title,kind,start,end,countries,text,source,note=''):
 c['events'].append(dict(id='extension-1960-'+id,title=title,type=kind,start=start,end=end,countries=countries,text=text,source=source,sourceLabel='Fuente institucional / documento del periodo',note=note))
state='https://history.state.gov/countries/'
independences=[('CMR','Camerún','1960-01-01','cameroon'),('TGO','Togo','1960-04-27','togo'),('MDG','Madagascar','1960-06-26','madagascar'),('COD','Congo-Léopoldville','1960-06-30','congo-democratic-republic'),('SOM','Somalia','1960-07-01','somalia'),('BEN','Dahomey','1960-08-01','benin'),('NER','Níger','1960-08-03','niger'),('BFA','Alto Volta','1960-08-05','burkina-faso'),('CIV','Costa de Marfil','1960-08-07','cote-divoire'),('TCD','Chad','1960-08-11','chad'),('CAF','República Centroafricana','1960-08-13','central-african-republic'),('COG','Congo-Brazzaville','1960-08-15','congo-republic'),('GAB','Gabón','1960-08-17','gabon'),('NGA','Nigeria','1960-10-01','nigeria'),('MRT','Mauritania','1960-11-28','mauritania'),('SLE','Sierra Leona','1961-04-27','sierra-leone'),('KWT','Kuwait','1961-06-19','kuwait'),('TAN','Tanganica','1961-12-09','tanzania'),('RWA','Ruanda','1962-07-01','rwanda'),('BDI','Burundi','1962-07-01','burundi'),('JAM','Jamaica','1962-08-06','jamaica'),('TTO','Trinidad y Tobago','1962-08-31','trinidad-and-tobago'),('UGA','Uganda','1962-10-09','uganda'),('KEN','Kenia','1963-12-12','kenya'),('MWI','Malaui','1964-07-06','malawi'),('MLT','Malta','1964-09-21','malta'),('ZMB','Zambia','1964-10-24','zambia'),('MDV','Maldivas','1965-07-26','maldives'),('GUY','Guyana','1966-05-26','guyana'),('BWA','Botsuana','1966-09-30','botswana'),('LSO','Lesoto','1966-10-04','lesotho'),('BRB','Barbados','1966-11-30','barbados'),('YPR','Yemen del Sur','1967-11-30','yemen'),('MUS','Mauricio','1968-03-12','mauritius'),('SWZ','Suazilandia','1968-09-06','swaziland'),('GNQ','Guinea Ecuatorial','1968-10-12','equatorial-guinea')]
for code,name,date,slug in independences:
 event('independence-'+code,'Independencia de '+name,'transition',date,str(int(date[:4])+1)+'-01-01',[code],f'{name} accede a la independencia. La ficha distingue los mandatos del año y la base territorial muestra el cierre anual; esta fecha no acredita por sí sola todos los límites o autoridades locales.',state+slug)
event('mali','Disolución de la Federación de Malí','transition','1960-06-20','1961-01-01',['MLI','SEN','FRA'],'La federación accede a la independencia el 20 de junio; Senegal se separa el 20 de agosto y la República Sudanesa adopta el nombre de Malí el 22 de septiembre. El cierre anual muestra los dos Estados.',state+'mali')
event('tanzania','Unión de Tanganica y Zanzíbar','transition','1964-04-26','1965-01-01',['TAN','ZAN','TZA'],'La unión se constituye el 26 de abril de 1964. El nombre Tanzania se adopta durante ese año; las instituciones autónomas de Zanzíbar requieren registros propios.','https://www.un.org/en/node/122916')
event('singapore','Independencia de Singapur','transition','1965-08-09','1966-01-01',['SGP','MYS'],'Singapur se separa de Malasia el 9 de agosto de 1965; su incorporación a Malasia en septiembre de 1963 no se proyecta a toda la década.','https://www.nas.gov.sg/archivesonline/government_records/record-details/3b0762b7-1159-11e3-83d5-0050568939ad')
event('uar','Separación de Siria de la República Árabe Unida','transition','1961-09-28','1962-01-01',['UAR','SYR','EGY'],'Siria sale de la unión en septiembre de 1961. Egipto conserva el nombre República Árabe Unida durante años; esto no prolonga la unión territorial.','https://untreaty.un.org/ilc/documentation/english/a_cn4_210.pdf')
conflicts=[
 ('congo','Crisis del Congo','1960-07-01','1965-11-25',['COD','BEL','USA','SUN'],'La independencia va seguida de intervención, secesiones y disputa de autoridades. El contorno nacional no reconstruye los frentes de Katanga ni otras administraciones rivales.','https://peacekeeping.un.org/mission/past/onucB.htm'),
 ('algeria','Guerra de independencia de Argelia','1960-01-01','1962-07-03',['DZA','FRA'],'Continúa la guerra hasta los acuerdos y la independencia de 1962. El inventario de control no ofrece una línea de frente diaria.','https://history.state.gov/milestones/1961-1968/algerian-independence'),
 ('yemen','Guerra civil de Yemen del Norte','1962-09-26','1970-12-31',['YMK','YAR','EGY','SAU'],'La revolución republicana desencadena una guerra entre republicanos y realistas con intervención exterior. Se distinguen ambos marcos políticos; no se inventa una partición territorial constante.','https://police.un.org/sites/default/files/past/unyombackgr.html'),
 ('vietnam','Guerra de Vietnam','1960-01-01','1970-01-01',['VDR','RVN','VSR','USA'],'Durante la década se intensifica la guerra entre los gobiernos vietnamitas y sus aliados. Las autoridades rivales y los mandatos se distinguen de los frentes, cuya reconstrucción detallada sigue pendiente.','https://history.state.gov/milestones/1961-1968/gulf-of-tonkin'),
 ('biafra','Guerra de Nigeria y secesión de Biafra','1967-05-30','1970-01-16',['NGA'],'La proclamación de Biafra el 30 de mayo de 1967 da paso al conflicto; el mapa no debe presentar una región oriental fija como frente de toda la guerra.','https://history.state.gov/historicaldocuments/frus1964-68v24/d386'),
 ('sixday','Guerra de junio de 1967 y ocupaciones','1967-06-05','1970-01-01',['ISR','EGY','SYR','JOR'],'La guerra modifica el control de Sinaí, Golán, Gaza, Cisjordania y Jerusalén Oriental. Ocupación y soberanía se mantienen separadas; los polígonos existentes sólo cubren parte de esos cambios.','https://history.state.gov/milestones/1961-1968/arab-israeli-war-1967'),
 ('cuba','Crisis de los misiles de Cuba','1962-10-16','1962-10-29',['CUB','USA','SUN'],'La crisis de octubre enfrenta a Estados Unidos y la Unión Soviética por el despliegue de misiles en Cuba; no constituye anexión territorial.','https://history.state.gov/milestones/1961-1968/cuban-missile-crisis'),
 ('berlin','Construcción del Muro de Berlín','1961-08-13','1962-01-01',['DDR','DEU','SUN','USA'],'El cierre de la frontera de Berlín profundiza la división alemana. Los sectores urbanos requieren una cartografía propia, no un cambio de color de toda Alemania.','https://history.state.gov/milestones/1961-1968/berlin-crises'),
 ('prague','Intervención en Checoslovaquia','1968-08-20','1969-01-01',['CSK','SUN'],'La intervención de agosto de 1968 termina la Primavera de Praga. La familia cromática de tutela no acredita un mapa diario de despliegues.','https://history.state.gov/milestones/1961-1968/soviet-invasion-czechoslavkia'),
 ('indo-pak','Guerra indo-pakistaní de 1965','1965-08-01','1966-01-01',['IND','PAK'],'La guerra de 1965 incluye operaciones en Cachemira y otros sectores. La base anual no sustituye una reconstrucción de líneas de frente.','https://history.state.gov/milestones/1961-1968/india-pakistan-war'),
 ('angola','Guerra en Angola','1961-01-01','1970-01-01',['AGO','PRT'],'Durante la década se desarrolla la guerra contra la administración portuguesa. La etiqueta administrativa no acredita control uniforme ni excluye las autoridades independentistas.','https://history.state.gov/milestones/1961-1968/portuguese-africa'),
 ('guinea','Guerra en Guinea portuguesa','1963-01-01','1970-01-01',['GNB','PRT'],'El conflicto de independencia se desarrolla antes de la proclamación de 1973; no se inventan frentes ni se atribuye el Gobierno independiente a toda la década.','https://history.state.gov/milestones/1961-1968/portuguese-africa'),
 ('mozambique','Guerra en Mozambique','1964-01-01','1970-01-01',['MOZ','PRT'],'La lucha independentista comienza durante la década bajo administración portuguesa; sus frentes y autoridades rivales requieren fuentes propias.','https://history.state.gov/milestones/1961-1968/portuguese-africa')]
for id,title,start,end,keys,text,source in conflicts:event(id,title,'conflict',start,end,keys,text,source,'Síntesis de contexto; fechas de precisión desigual. Los límites 1960/1970 pueden delimitar esta ampliación, no el comienzo o final completo del conflicto.')
for e in c['events']:
 if e['id'].startswith('extension-1960-'):
  if e['source'].endswith('/portuguese-africa'):e['source']='https://history.state.gov/historicaldocuments/frus1964-68v24/ch11'
  if e['source'].endswith('/algerian-independence'):e['source']=state+'algeria'
  if e['id']=='extension-1960-singapore':e['source']='https://www.parliament.gov.sg/history/historical-development'
c['startYear']=1960;c['retrieved']='2026-10-23';save('historical-context.json',c)
h=read('country-history.json');h['relations']=[r for r in h['relations'] if not r['id'].startswith('extension-1960-')];h['records']=[r for r in h['records'] if not r['id'].startswith('extension-1960-')]
for id,a,an,ay,b,bn,by,date,source,note in [
 ('uar-egy','UAR','República Árabe Unida',1960,'EGY','Egipto',1961,'1961-09-28','https://untreaty.un.org/ilc/documentation/english/a_cn4_210.pdf','Egipto conserva durante años el nombre RAU; la unión territorial con Siria termina en 1961.'),
 ('uar-syr','UAR','República Árabe Unida',1960,'SYR','Siria',1961,'1961-09-28','https://untreaty.un.org/ilc/documentation/english/a_cn4_210.pdf','Separación de Siria; no transferencia automática de estadísticas o autoridades.'),
 ('ymk-yar','YMK','Reino Mutawakkilita de Yemen',1961,'YAR','República Árabe de Yemen',1963,'1962-09-26','https://police.un.org/sites/default/files/past/unyombackgr.html','Revolución y guerra civil: la proclamación republicana no elimina inmediatamente al bando realista ni acredita control uniforme.'),
 ('tan-tza','TAN','Tanganica',1963,'TZA','Tanzania',1964,'1964-04-26','https://www.un.org/en/node/122916','Unión; el nombre Tanzania se adopta más tarde en 1964.'),
 ('zan-tza','ZAN','Zanzíbar',1963,'TZA','Tanzania',1964,'1964-04-26','https://www.un.org/en/node/122916','Unión posterior a la revolución de enero; no elimina las instituciones autónomas zanzibaríes.'),
 ('mys-sgp','MYS','Malasia',1964,'SGP','Singapur',1965,'1965-08-09','https://www.parliament.gov.sg/history/historical-development','Separación del Estado de Singapur de la federación.'),
 ('fra-dza','FRA','Francia',1961,'DZA','Argelia',1962,'1962-07-03',state+'algeria','Reconocimiento francés tras referéndum de 1/7; la conmemoración nacional es 5/7.'),
 ('gbr-jam','GBR','Reino Unido',1961,'JAM','Jamaica',1962,'1962-08-06',state+'jamaica','Independencia; compartir monarca no implica dependencia.'),
 ('gbr-zmb','GBR','Reino Unido',1963,'ZMB','Zambia',1964,'1964-10-24',state+'zambia','Independencia tras la disolución de la federación; no continuidad del régimen rodesiano.'),
]:
 h['relations'].append(dict(id='extension-1960-'+id,**{'from':dict(key=a,name=an,year=ay),'to':dict(key=b,name=bn,year=by)},date=date,type='transition',label=an+' → '+bn,note=note,source=source,sourceLabel='Fuente institucional de la transición'))
for key,title,start,end,text,source in [
 ('UAR','Unión de Egipto y Siria','1958-02-22','1961-09-28','La República Árabe Unida reúne Egipto y Siria. Las provincias no son dos Estados independientes durante la unión; la salida siria de septiembre de 1961 termina su alcance territorial conjunto.','https://untreaty.un.org/ilc/documentation/english/a_cn4_210.pdf'),
 ('TAN','Monarquía y república de Tanganica','1961-12-09','1964-04-26','El Estado independiente comienza como monarquía con Isabel II y Gobierno propio. Se constituye en república el 9/12/1962 y se une con Zanzíbar el 26/4/1964.','https://www.tanzania.go.tz/topics/policy-coordination-and-parliament'),
 ('YMK','Monarquía yemení y revolución','1960-01-01','1962-09-26','Reinado del imam Ahmad y sucesión de Muhammad al-Badr en septiembre de 1962. La revolución republicana abre una guerra civil con autoridades rivales. El inicio 1960 delimita esta revisión, no la fundación del reino.','https://police.un.org/sites/default/files/past/unyombackgr.html'),
 ('NGA','Monarquía independiente y república','1960-10-01','1966-01-16','Nigeria es independiente desde 1/10/1960 y república desde 1/10/1963. Balewa dirige el Gobierno; Azikiwe es gobernador general y posteriormente presidente. El golpe de enero de 1966 cambia el marco político.','https://statehouse.gov.ng/past-heads-of-state-and-presidents/')]:
 h['records'].append(dict(id='extension-1960-institution-'+key,keys=[key],start=start,end=end,section='institutions',title=title,text=text,source=source,sourceLabel='Fuente institucional del marco político'))
save('country-history.json',h)
print('Prepared',len(c['events']),'context phases;',sum(len(o['memberships']) for o in orgs.values()),'membership intervals.')
