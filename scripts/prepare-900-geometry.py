"""Additional900–999 leaf intervals from the same pinned Cliopatria source.

Coordinates and source-index IDs are kept verbatim; no previous asset rewritten.
"""
import pathlib,json,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
raw=read(ROOT/'.cache/cliopatria/cliopatria_polities_only_v021.geojson');features=[]
for i,f in enumerate(raw['features']):
 p=f['properties']
 if p['Components'] or p['FromYear']>999 or p['ToYear']<900:continue
 features.append(dict(type='Feature',id=f'clio-{i}',geometry=f['geometry'],properties=dict(name=p['Name'],originalName=p['Name'],wikidata=p['Wikidata'],start=max(900,p['FromYear']),end=min(999,p['ToYear']),parentName=p['MemberOf'].strip('()'),code='',source='https://github.com/Seshat-Global-History-Databank/cliopatria',precision='annual-synthesis',politicalStatus='Entidad histórica · reconstrucción anual')))
path=OUT/'early-modern-900.geojson';path.write_text(json.dumps(dict(type='FeatureCollection',features=features),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
m=read(OUT/'manifest.json');base=next(e for e in m['entries'] if e['file']=='early-modern.geojson');e={k:v for k,v in base.items() if k not in ['file','features','bytes','sha256','coverage','transform']};e.update(file=path.name,features=len(features),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),coverage='900/999',transform='Select leaf intervals intersecting900–999 from pinned Cliopatria; original coordinate arrays and source-index IDs preserved. Annual synthesis without uniform day. Existing1100+ geometry files untouched.')
m['entries']=[v for v in m['entries'] if v['file']!=path.name]+[e];(OUT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Additional source intervals',len(features),'bytes',path.stat().st_size)
for y in [900,950,999]:
 fs=[f for f in features if f['properties']['start']<=y<=f['properties']['end']];print(y,len(fs))
(ROOT/'.cache/polities027.json').write_text(json.dumps(sorted({(f['properties']['wikidata'],f['properties']['name']) for f in features}),ensure_ascii=False)+'\n',encoding='utf8')
