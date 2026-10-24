"""1920 coverage of existing administrations; do not erase constitutional transitions."""
import json,pathlib,copy
root=pathlib.Path(__file__).resolve().parents[1]/'public/data'
d=json.loads((root/'territorial-administrations.json').read_text(encoding='utf8'));d['coverageStart']='1920-01-01'
if not any(r['id']=='austria-annexation-1938' for r in d['records']):
 d['records'].append(dict(id='austria-annexation-1938',names=['Austria'],codes=['AUT'],admin='DEU',localKey='AUT',start='1938-03-12',end='1945-04-27',headOfStateOnly=False,label='Austria bajo control alemán tras el Anschluss',note='Entrada de tropas12/3/1938 y ley de incorporación13/3; no existe un Gobierno austríaco independiente durante esa fase. Se distinguen los cargos alemanes de los austríacos. La declaración de independencia de27/4/1945 abre la transición; no acredita control militar simultáneo de toda Austria.',source='https://www.oesta.gv.at/veroeffentlichungen/archivale-des-monats/volksbefragung-und-anschluss-im-marz-1938.html'))
for r in d['records']:
 if r['start']=='1950-01-01':r.update(start='1920-01-01',startIsCoverageBoundary=True)
 r['note']=r['note'].replace('retroproyecta a 1950','retroproyecta a 1920')
# The French departments did not have that constitutional status before1946.
for ident in ['french-guiana','guadeloupe','martinique']:
 current=next(r for r in d['records'] if r['id']==ident)
 if not any(r['id']==ident+'-before-department' for r in d['records']):
  earlier=copy.deepcopy(current);earlier.update(id=ident+'-before-department',start='1920-01-01',end='1946-03-19',label='Administración colonial francesa anterior a la departamentalización',note='La ley de19/3/1946 cambia el estatuto a departamento. No se aplica ese estatuto retrospectivamente al periodo colonial. Los cargos estatales y los territoriales son ámbitos distintos.',source='https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000868445/')
  d['records'].append(earlier)
 current.update(start='1946-03-19',startIsCoverageBoundary=False)
(root/'territorial-administrations.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
print('Prepared1920 administrations:',len(d['records']))
