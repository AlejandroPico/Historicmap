"""Extend existing administrative relations, distinguishing constitutional changes."""
import json,pathlib,copy
root=pathlib.Path(__file__).resolve().parents[1]/'public/data'
data=json.loads((root/'territorial-administrations.json').read_text(encoding='utf8'))
data['coverageStart']='1950-01-01'
for r in data['records']:
 if r['start']=='1960-01-01':r['start']='1950-01-01'
 r['note']=r['note'].replace('retroproyecta a 1960','retroproyecta a 1950')
for ident,boundary,label,note,source,stateOnly in [
 ('puerto-rico','1952-07-25','Puerto Rico · territorio de Estados Unidos anterior al Commonwealth','La Constitución del Estado Libre Asociado entra en vigor el25/7/1952. Antes conserva condición territorial estadounidense; no es un Estado independiente.','https://blogs.loc.gov/law/2022/11/the-commonwealth-of-puerto-rico-and-its-government-structure/',False),
 ('surinam','1954-12-15','Surinam · administración neerlandesa anterior a la Carta de1954','La Carta del Reino de15/12/1954 establece el nuevo marco del Reino. La administración anterior no se etiqueta retroactivamente como la autonomía de1954.','https://www.royal-house.nl/topics/royal-house-and-history/history',False),
]:
 current=next(r for r in data['records'] if r['id']==ident)
 if not any(r['id']==ident+'-before-charter' for r in data['records']):
  earlier=copy.deepcopy(current);earlier.update(id=ident+'-before-charter',start='1950-01-01',end=boundary,label=label,note=note,source=source,headOfStateOnly=stateOnly)
  data['records'].append(earlier)
 current.update(start=boundary,startIsCoverageBoundary=False)
(root/'territorial-administrations.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
print('Extended administrative coverage to1950:',len(data['records']),'relations.')
