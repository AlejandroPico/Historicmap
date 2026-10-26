"""Extend only unadministered local-reference windows and original island indexes."""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
p=OUT/'pacific-components.json';d=read(p);d['records']=read(ROOT/'.cache/pacific-014-clio-component-index.json');save(p,d)
p=OUT/'pacific-references.geojson';d=read(p)
for f in d['features']:
 p=f['properties']
 if p['start']=='1820-01-01' and not p.get('administratorKey'):p['start']='1800-01-01'
save(OUT/'pacific-references.geojson',d)
print('Prepared original components and local references from1800')

p=OUT/'political-influence.json';d=read(p);d['records']=[r for r in d['records'] if not r['id'].startswith('extension-1800-')]
for key,a,b in [('ITALIAN-REPUBLIC-1802','1802-01-01','1805-01-01'),('NAPOLEONIC-ITALY','1805-01-01','1814-01-01'),('NAPOLEONIC-NAPLES','1806-01-01','1815-01-01')]:
 d['records'].append(dict(id='extension-1800-'+key,keys=[key],power='FRA',start=a,end=b,kind='client',source='https://www.servicehistorique.sga.defense.gouv.fr/ark/41452',note='Órbita napoleónica, con autoridad e identidad propias; no anexión ni administración colonial. Ventana anual conservadora.'))
save(p,d)
