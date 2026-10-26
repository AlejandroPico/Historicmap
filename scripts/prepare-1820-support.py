"""Extend only unadministered local-reference windows and original island indexes."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
p=OUT/'pacific-components.json';d=read(p);d['records']=read(ROOT/'.cache/pacific-014-clio-component-index.json');save(p,d)
p=OUT/'pacific-references.geojson';d=read(p)
for f in d['features']:
 p=f['properties']
 if p['start']=='1840-01-01' and not p.get('administratorKey'):p['start']='1820-01-01'
save(OUT/'pacific-references.geojson',d)
p=OUT/'portrait-series.json';d=read(p)
def extend(value):
 if isinstance(value,dict):
  if value.get('start')=='1840-01-01' and '1838' in json.dumps(value,ensure_ascii=False):value['start']='1838-01-01'
  for v in value.values():extend(v)
 elif isinstance(value,list):
  for v in value:extend(v)
extend(d);save(p,d)
print('Prepared original components, local references and dated1838 portrait')
