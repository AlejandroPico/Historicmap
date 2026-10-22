"""Documented annual-close occupation, separately licensed from modern reference outlines."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'public/data'
t=json.loads((root/'history.topojson').read_text(encoding='utf-8'))
g=next(g for g in t['objects']['countries']['geometries'] if g['properties']['country_name']=='Kuwait' and g['properties']['start']<='1990-12-31'<=g['properties']['end'])
def ring(indices):
    out=[]
    for n in indices:
        a=t['arcs'][n if n>=0 else ~n];a=a if n>=0 else a[::-1]
        out.extend(a if not out else a[1:])
    return out
geometry={'type':g['type'],'coordinates':[ring(r) for r in g['arcs']] if g['type']=='Polygon' else [[ring(r) for r in p] for p in g['arcs']]}
f={'type':'Feature','id':910000,'geometry':geometry,'properties':{'uid':'kuwait-1990','name':'Kuwait · ocupación iraquí','originalName':'Kuwait','code':'KWT','entityCode':'KWT','controller':'IRQ','identityKey':'IRQ','start':1990,'end':1990,'kind':'war','note':'Kuwait permanece ocupado por Irak al cierre de 1990, tras la invasión del 2 de agosto. La base conserva Kuwait separado; esta capa muestra ocupación, no soberanía reconocida. En el cierre de 1991 ya no se aplica esta ocupación. Contorno CShapes vigente en 1990, sin sustituirlo por la demarcación posterior.','source':'https://peacekeeping.un.org/sites/default/files/past/unikom/background.html','geometrySource':'https://icr.ethz.ch/data/cshapes/','license':'CC-BY-NC-SA-4.0'}}
(root/'recent-control.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[f]},ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
print('Prepared Kuwait occupation at annual close 1990; source geometry unchanged.')
