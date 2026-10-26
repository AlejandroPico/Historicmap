"""Additional Cliopatria leaf intervals1700–1788; retain existing assets and IDs."""
import pathlib,json,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';CACHE=ROOT/'.cache'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
raw=read(next((CACHE/'cliopatria').glob('*.geojson')));features=[];SOURCE='https://github.com/Seshat-Global-History-Databank/cliopatria'
for i,f in enumerate(raw['features']):
 p=f['properties']
 if p['Components'] or p['FromYear']>1788 or p['ToYear']<1700:continue
 features.append(dict(type='Feature',id=f'clio-{i}',geometry=f['geometry'],properties=dict(name=p['Name'],originalName=p['Name'],wikidata=p['Wikidata'],start=max(1700,p['FromYear']),end=min(1788,p['ToYear']),parentName=p['MemberOf'].strip('()'),code='',source=SOURCE,precision='annual-synthesis',politicalStatus='Entidad histórica · reconstrucción anual')))
path=OUT/'early-modern-1700.geojson';path.write_text(json.dumps(dict(type='FeatureCollection',features=features),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
manifest=read(OUT/'manifest.json');base=next(e for e in manifest['entries'] if e['file']=='early-modern.geojson');entry={k:v for k,v in base.items() if k not in ['file','features','bytes','sha256','coverage','transform']};entry.update(file=path.name,features=len(features),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),coverage='1700/1788',transform='Select inclusive intervals intersecting1700–1788 from the same pinned Cliopatria source; omit aggregate Components and preserve original coordinate arrays, names, QIDs, MemberOf and source-index identifiers. Existing1789+ geometry assets untouched; annual synthesis has no uniform reference day.')
manifest['entries']=[e for e in manifest['entries'] if e['file']!=path.name]+[entry];(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('Additional source intervals',len(features),'bytes',path.stat().st_size,flush=True)
