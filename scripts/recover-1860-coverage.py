"""Recover explicitly recorded source starts clipped by the previous1880 coverage.

Requires structured sourceStart and coverage flag; never guesses from a name,
birth date, modern office, or absence of a successor. Keeps all1880+ terms.
"""
import pathlib,json,copy
ROOT=pathlib.Path(__file__).resolve().parents[1];path=ROOT/'public/data/identities.json'
def curate(data):
 data=copy.deepcopy(data);count=0
 for country in data['countries'].values():
  country['leaders']=[l for l in country['leaders'] if l.get('acquisition')!='recovered-source-start-0.14']
  recovered=[]
  for l in country['leaders']:
   if l['start']!='1880-01-01' or not l.get('startIsCoverageBoundary') or not l.get('sourceStart') or l['sourceStart']>='1880-01-01':continue
   start=max('1860-01-01',l['sourceStart'])
   if any(a['person']==l['person'] and a['role']==l['role'] and a['start']<=start and a['end']>='1879-12-31' for a in country['leaders']):continue
   a=copy.deepcopy(l);a.update(start=start,end='1879-12-31',startIsCoverageBoundary=start!=l['sourceStart'],endIsCoverageBoundary=True,acquisition='recovered-source-start-0.14',note='Inicio real conservado explícitamente como sourceStart en la adquisición anterior. Ventana recuperada antes de1880; el final1879 es cobertura, no un cese. '+l.get('note',''));recovered.append(a);count+=1
  country['leaders'].extend(recovered)
 return data
if __name__=='__main__':
 old=json.loads(path.read_text(encoding='utf8'));data=curate(old);assert curate(data)==data
 path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
 print('Recovered structured earlier coverage; existing offices unchanged')
