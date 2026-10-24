"""Bounded African sovereigns and a documented absence of central rule.

Pure, repeatable transformation. Calendar-year precision is intentional where
the consulted evidence does not establish an exact transition day.
"""
import argparse,copy,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
TAG='curated-1900-regions-0.12'
FIRST,LAST='1900-01-01','1919-12-31'
ETH='https://tile.loc.gov/storage-services/service/gdc/gdclccn/a2/20/00/98/6/a22000986/a22000986.pdf'
COUP='https://tarihtetkikleri.com/index.php/pub/article/view/31'
MAR='https://history.state.gov/historicaldocuments/frus1908/papers'
BO='https://archive.gazettes.africa/archive/ma/1912/ma-bulletin-officiel-dated-1912-11-01-no-1.pdf'
CONGO='https://www.arch.be/index.php?a=2022-09-26-opnieuw-op-zijn-plaats-het-verdrag-tot-afstand-van-de-onafhankelijke-congostaat-aan-belgie&l=nl&m=nieuws&r=alle-nieuwsberichten'

def curate(incoming):
 d=copy.deepcopy(incoming);cs=d['countries']
 photos={l['person']:copy.deepcopy(l['portrait']) for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 cs.setdefault('CFS',dict(qid='Q76048',name='Estado Libre del Congo',flags=[],leaders=[]))
 def term(key,q,name,role,start,end,source,note,precision=11,start_boundary=False,end_boundary=False):
  record=dict(person=q,name=name,role=role,start=start,end=end,source=source,note=note,precision=precision,curated=True,acquisition=TAG)
  if start_boundary:record['startIsCoverageBoundary']=True
  if end_boundary:record['endIsCoverageBoundary']=True
  if q in photos:record['portrait']=copy.deepcopy(photos[q])
  cs[key]['leaders'].append(record)
 term('ETH','Q244748','Menelik II','Emperador de Etiopía · soberano formal',FIRST,'1913-12-31',ETH,
      'La síntesis contemporánea del Foreign Office, Abyssinia, n.º129, distingue la enfermedad del soberano, la regencia y su muerte en1913. Precisión anual: el extremo1913 no afirma que muriese el31de diciembre. La autoridad efectiva pasó progresivamente a la regencia.',9,True,True)
 term('ETH','Q379889','Lij Iyasu','Sucesor designado y gobernante efectivo · sin coronación imperial','1911-12-31','1916-09-27',COUP,
      'Ejercicio efectivo tras la regencia de Tesemma, antes de la muerte de Menelik en1913. Sucesor nunca coronado; depuesto por la proclamación de27/9/1916. La ventana inicial1911 es anual, no fecha de acceso al título imperial.',9,True)
 term('ETH','Q148524','Zewditu','Emperatriz de Etiopía','1916-09-27',LAST,COUP,
      'Proclamación tras la deposición de Iyasu; coronación posterior en febrero1917. Se conserva la distinción entre soberana y regente.',11,False,True)
 term('ETH','Q41178','Tafari Makonnen · futuro Haile Selassie','Regente y heredero · autoridad de Gobierno','1916-09-27',LAST,COUP,
      'Regencia junto a Zewditu, distinta del título de negus de1928 y de la coronación imperial de1930. No se retrotrae su presidencia ni su título imperial.',11,False,True)
 term('MAR','Q307132','Abd al-Aziz','Sultán de Marruecos · soberano disputado durante la crisis sucesoria',FIRST,'1908-12-31',MAR,
      'Reinado desde1894; en1907–1908 su hermano reclama el sultanato. La documentación diplomática de1908 distingue proclamaciones, derrota y reconocimiento exterior de Hafid. El último extremo tiene precisión anual y no afirma ejercicio hasta31/12.',9,True,True)
 term('MAR','Q276936','Abd al-Hafid','Sultán de Marruecos · inicialmente autoridad rival','1908-01-01','1912-08-12',MAR,
      'Ventana anual de1908, no día de proclamación: las proclamaciones regionales comenzaron antes y el reconocimiento diplomático se negoció durante1908. Firma el tratado de Fès30/3/1912; el protectorado no suprime automáticamente el sultanato. Sucesión de Yusef documentada en el primer Bulletin Officiel.',9,True)
 term('MAR','Q276937','Moulay Yusef','Sultán de Marruecos bajo protectorado francés','1912-08-13',LAST,BO,
      'El primer Bulletin Officiel reproduce la proclamación13/8/1912 y el tratado que conserva al sultán mientras somete relaciones exteriores y reformas al protector. No sustituye la autoridad francesa por una soberanía local plena.',11,False,True)
 term('CFS','Q12967','Leopoldo II','Soberano del Estado Libre del Congo · unión personal con la Corona belga',FIRST,'1908-11-14',CONGO,
      'Entidad separada del Estado belga, bajo soberanía personal de LeopoldoII. La ley colonial entró en vigor15/11/1908; no se atribuye el Gobierno del Congo a los ministros belgas antes de la anexión.',11,True)
 term('YKM','Q211827','Pedro I','Rey de los serbios, croatas y eslovenos','1918-12-01',LAST,'https://royalfamily.org/dinasty/hm-king-peter-i-of-serbia/',
      'La unión se proclama1/12/1918; no se titula rey de Yugoslavia antes del cambio de nombre de1929. Su enfermedad y la regencia de Alejandro se distinguen de la jefatura formal.',11,False,True)
 term('YKM','Q207384','Alejandro','Príncipe regente · ejercicio de funciones reales','1918-12-01',LAST,'https://royalfamily.org/dinasty/hm-king-alexander-i-of-yugoslavia/',
      'Ejercía la regencia serbia desde1914; esta ventana comienza con la unión de1918, no con su acceso a la regencia. No sucede como rey hasta1921.',11,True,True)
 cs['ALB']['territoryStatus']=dict(start='1917-01-01',end='1917-12-31',text='Albania estaba fragmentada por ocupaciones y administraciones locales durante la Primera Guerra Mundial; no existía un Gobierno central efectivo que gobernase todo el contorno. Las autoridades locales y los pretendientes requieren registros propios. No es ausencia de población ni una presidencia nacional vacante inventada.',source='https://punetejashtme.gov.al/en/historiku-i-krijimit-te-institucionit-te-ministrise-se-puneve-te-jashtme-te-shtetit-shqiptar/')
 for c in cs.values():c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
 return d

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=pathlib.Path,default=ROOT/'public/data/identities.json');p.add_argument('--output',type=pathlib.Path);a=p.parse_args()
 d=curate(json.loads(a.input.read_text(encoding='utf8')))
 (a.output or a.input).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
 print('Prepared African sovereigns and Albania1917 institutional status.')
