"""Dated1820–1839 identity resolution; source coordinates stay intact."""
import pathlib,json,copy
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
read=lambda f:json.loads((OUT/f).read_text(encoding='utf8'))
def prepare(base,identities):
 d=copy.deepcopy(base);d.update(coverageStart=1820,coverageEnd=1839,referenceDate='2026-10-26')
 remove={'FRA','ESP','HTI','IND','TEXAS','COL','MEX'}
 d['records']=[dict(r,start=1820,end=1839) for r in d['records'] if r['start']==1840 and r['end']==1859 and r['key'] not in remove]
 for k,c in identities['countries'].items():
  if c.get('qid'):d['qidKeys'].setdefault(c['qid'],k)
 d['names'].update({k:c['name'] for k,c in identities['countries'].items()})
 def row(names,key,label,a=1820,b=1839,status='independent',admin='',note=''):
  d['records'].append(dict(names=names,key=key,label=label,entityCode=key,start=a,end=b,status=status,admin=admin,source='https://github.com/Seshat-Global-History-Databank/cliopatria',note=note+' Contorno de síntesis anual de la fuente; no frontera diaria reconstruida.'))
 row(['Bourbon Kingdom of France','France'],'FRA','Francia · Restauración borbónica',b=1829)
 row(['Bourbon Kingdom of France','France'],'FRA','Francia · Monarquía de Julio',a=1830,note='Cambio de régimen en julio-agosto de 1830; las autoridades del año se conservan en la ficha.')
 row(['Kingdom of Spain','Spanish Empire'],'ESP','España · Trienio Liberal',b=1822,note='Fernando VII conserva el trono bajo la Constitución restaurada.')
 row(['Kingdom of Spain','Spanish Empire'],'ESP','España · restauración absolutista',a=1823,b=1832,note='La intervención francesa y el final constitucional ocurren durante 1823.')
 row(['Kingdom of Spain','Spanish Empire'],'ESP','España · regencia de María Cristina',a=1833,note='Isabel II es la soberana menor; María Cristina ejerce la regencia. No se inventa un frente carlista.')
 row(['Empire of Haiti','Haiti'],'HTI','República de Haití',note='El QID imperial de 1804 es anacrónico. 1820 contiene la reunificación tras el fin del reino septentrional; Boyer no fue emperador.')
 row(['British Raj','India'],'IND','India británica · gobierno de la Compañía',status='company-rule',admin='GBR')
 row(['Republic of Texas'],'TEXAS','República de Texas',a=1836)
 row(['First Mexican Empire'],'HIST-Q285658','Primer Imperio mexicano',a=1822,b=1823,note='Entidad distinta del Segundo Imperio de 1864.')
 row(['Federated Republic of Mexico'],'MEX','México · República Federal',a=1824)
 row(['Centralist Mexico'],'MEX','México · República Centralista',a=1835)
 row(['Gran Colombia'],'HIST-Q199821','Gran Colombia',b=1830)
 row(['Gran Colombia'],'COL','Nueva Granada · contorno de fuente pendiente',a=1831,b=1833,note='La persistencia hasta 1833 de la geometría Gran Colombia no acredita la continuidad de la unión. Falta mejorar las fronteras sucesoras.')
 row(['New Granada','Republic of New Granada'],'COL','República de Nueva Granada',a=1831)
 row(['First Hellenic Republic'],'GRC','Grecia · república y transición monárquica',a=1822,note='La etiqueta republicana de la fuente no fecha todas las fases posteriores de Otón. Independencia, reconocimiento y monarquía son procesos distintos.')
 return d
if __name__=='__main__':
 d=prepare(read('historical-1840-entities.json'),read('identities.json'))
 (OUT/'historical-1820-entities.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
 print('Prepared',len(d['records']),'dated identity rules')
