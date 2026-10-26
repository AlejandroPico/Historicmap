"""Dated1840–1859 identity corrections on the unchanged Cliopatria inventory."""
import pathlib,json,copy
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
read=lambda f:json.loads((OUT/f).read_text(encoding='utf8'))
def prepare(base,identities):
 d=copy.deepcopy(base);d.update(coverageStart=1840,coverageEnd=1859,referenceDate='2026-10-26')
 remove={'FRA','ESP','JPN','ITA','DEU','AUT-HUN','AUSTRIAN-EMPIRE','BGR','HTI','IND'}
 d['records']=[dict(r,start=1840,end=1859) for r in d['records'] if r['start']==1860 and r['end']==1879 and r['key'] not in remove]
 for k,c in identities['countries'].items():
  if c.get('qid'):d['qidKeys'].setdefault(c['qid'],k)
 d['qidKeys'].update(Q28179='JOS',Q28405='JOS',Q2577303='SAR',Q165154='SAR',Q170588='TEXAS',Q180393='TWO-SICILIES',Q170174='PAPAL-STATES',Q3057606='EGY',Q189326='IRN',Q205662='JPN',Q832554='ARG',Q630882='COL',Q1141215='COL',Q1109279='MEX',Q5062192='MEX')
 d['names'].update({k:c['name'] for k,c in identities['countries'].items()})
 def row(names,key,label,a=1840,b=1859,status='independent',admin='',source='https://github.com/Seshat-Global-History-Databank/cliopatria',note=''):
  d['records'].append(dict(names=names,key=key,label=label,entityCode=key,status=status,admin=admin,start=a,end=b,source=source,note=note+' Contorno original de síntesis anual; no todas las transiciones tienen una fase geométrica independiente.'))
 french=['Bourbon Kingdom of France','French Second Republic','Second French Empire','France']
 row(french,'FRA','Francia · Monarquía de Julio',b=1847,source='https://www.elysee.fr/louis-napoleon-bonaparte',note='Luis Felipe de Orleans, no una restauración borbónica como sugiere la etiqueta de fuente.')
 row(french,'FRA','Francia · Segunda República',a=1848,b=1851,source='https://www.elysee.fr/la-presidence/la-constitution-du-4-novembre-1848')
 row(french,'FRA','Francia · Segundo Imperio',a=1852,source='https://www.elysee.fr/louis-napoleon-bonaparte',note='La proclamación imperial es2/12/1852; el golpe de1851 no se confunde con ella.')
 row(['Kingdom of Spain','Spanish Empire'],'ESP','España · monarquía de Isabel II',source='https://www.congreso.es/ca/cem/regespartero',note='Las regencias y la mayoría de edad son instituciones distintas, reflejadas en las autoridades y el contexto.')
 row(['Austrian Empire'],'AUSTRIAN-EMPIRE','Imperio austríaco',note='No la monarquía dual austrohúngara de1867.')
 row(['Hungarian Nationalists'],'HIST-HUNGARY-1848','Hungría · gobierno revolucionario',a=1848,b=1849,status='revolutionary-government',note='El QID austrohúngaro de la fuente es anacrónico; no se asigna aFrancisco José como líder de la insurrección.')
 row(['Tokugawa Shogunate'],'JPN','Japón · shogunato Tokugawa',note='Emperador y gobierno del shogun conservan cargos distintos; no se anticipa la restauración de1868.')
 row(['Joseon'],'JOS','Reino de Joseon',source='https://www.wikidata.org/wiki/Q28179',note='Corrección explícita del QID de fuenteQ28405, que corresponde aGojoseon antiguo. Se conserva en sourceWikidata para trazabilidad.')
 row(['British Raj','India'],'IND','India británica · gobierno de la Compañía',b=1857,status='company-rule',admin='GBR',source='https://www.royal.uk/encyclopedia/victoria-r-1837-1901',note='El nombreRaj de la fuente anterior a1858 es anacrónico. Las autoridades británicas no sustituyen una serie completa de gobernadores generales o de Estados principescos.')
 row(['British Raj','India'],'IND','India británica · gobierno de la Corona',a=1858,status='colony',admin='GBR',source='https://www.royal.uk/encyclopedia/victoria-r-1837-1901',note='Gobierno de la Corona desde1858; Victoria no es emperatriz deIndia en1840.')
 row(['Empire of Brazil'],'BRA-EMPIRE','Imperio del Brasil',source='https://www.senado.leg.br/senado/hotsites/histsf/O-Senado-no-2o-Reinado.asp')
 row(['Kingdom of Sardinia'],'SAR','Reino de Cerdeña-Piamonte',note='No se atribuye a este Estado el título de Reino deItalia, establecido en1861.')
 row(['Kingdom of the Two Sicilies'],'TWO-SICILIES','Reino de las Dos Sicilias')
 row(['Papal States'],'PAPAL-STATES','Estados Pontificios',note='La República Romana de1849 no queda geométricamente separada en este registro; el contexto no inventa ese frente.')
 row(['German Confederation'],'HIST-Q151624','Confederación Germánica',status='confederation',note='Agregado de la fuente, no un reino alemán unitario ni una anexión prusiana. Los Estados separados sólo se muestran donde existe su geometría.')
 row(['Muhammad Ali dynasty'],'EGY','Egipto · dinastía de Muhammad Alí',status='autonomous-polity',note='Autonomía y soberanía nominal otomana no equivalen a una república egipcia moderna.')
 row(['Qajar Dynasty'],'IRN','Persia · dinastía Qajar')
 row(['Centralist Mexico'],'MEX','México · República Centralista',b=1846)
 row(['Federated Republic of Mexico','Mexico'],'MEX','México · República Federal')
 row(['Republic of Texas'],'TEXAS','República de Texas',b=1845,note='Síntesis de fuente del año de la anexión, no garantía de un cierre uniforme el31de diciembre.')
 row(['Empire of Haiti','Haiti'],'HTI','República de Haití',b=1848,note='La etiqueta imperial anterior a1849 del inventario no se acepta como régimen vigente.')
 row(['Empire of Haiti','Haiti'],'HTI','Segundo Imperio de Haití',a=1849,b=1858,note='Faustino I; distinto del primer Imperio de1804, cuyo QID aparece erróneamente en la fuente.')
 row(['Empire of Haiti','Haiti'],'HTI','Haití · transición republicana',a=1859)
 return d
if __name__=='__main__':
 d=prepare(read('historical-1860-entities.json'),read('identities.json'))
 (OUT/'historical-1840-entities.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n');print('Prepared',len(d['records']),'bounded identity rules')
