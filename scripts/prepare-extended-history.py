"""Select Cliopatria leaf polities for 1789–1885 and dated control overlays.

Source coordinates retained, no contemporary polygons retrojected. Composite
records are omitted to avoid drawing both a polity and the union of its members.
Requires cached sources from acquire-history.py. CC BY 4.0, separate from CShapes.
"""
import datetime, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
CACHE,OUT=ROOT/'.cache',ROOT/'public/data'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
clio=read(next((CACHE/'cliopatria').glob('*.geojson')))
manifest=read(OUT/'manifest.json')
sha=(CACHE/'cliopatria-sha.txt').read_text(encoding='utf-8-sig').strip()
meta=dict(source='Cliopatria · Seshat Global History Databank',version=sha,url=f'https://raw.githubusercontent.com/Seshat-Global-History-Databank/cliopatria/{sha}/cliopatria.geojson.zip',sourceSha256=hashlib.sha256((CACHE/'cliopatria.zip').read_bytes()).hexdigest(),license='CC-BY-4.0')
SOURCE='https://github.com/Seshat-Global-History-Databank/cliopatria'
def save(file,features,**details):
    path=OUT/file
    path.write_text(json.dumps(dict(type='FeatureCollection',features=features),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    entry=dict(file=file,features=len(features),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**meta,**details)
    manifest['entries'][:]=[e for e in manifest['entries'] if e['file']!=file]
    manifest['entries'].append(entry)
    print(file,len(features),entry['bytes'])
early=[]
for i,f in enumerate(clio['features']):
    p=f['properties']
    if p['Components'] or p['FromYear']>1885 or p['ToYear']<1789:continue
    early.append(dict(type='Feature',id=f'clio-{i}',geometry=f['geometry'],properties=dict(name=p['Name'],originalName=p['Name'],wikidata=p['Wikidata'],start=max(1789,p['FromYear']),end=min(1885,p['ToYear']),parentName=p['MemberOf'].strip('()'),code='',source=SOURCE,precision='annual-synthesis',politicalStatus='Entidad histórica · reconstrucción anual')))
save('early-modern.geojson',early,coverage='1789/1885',transform='Select inclusive intervals intersecting 1789–1885. Exclude records with Components (aggregate unions); keep leaf polities and MemberOf relation. Original coordinates, source names and Wikidata IDs retained. Not a uniform December 31 reconstruction; uncovered areas remain uncovered.')

# The source is an annual reconstruction. Client regimes are distinct from allies.
configs={
 'German Empire':('DEU','Imperio alemán · extensión durante la guerra',1914,1918,'occupation'),
 'Austria-Hungary':('AUT-HUN','Austria-Hungría · extensión durante la guerra',1914,1918,'occupation'),
 'Ottoman Empire':('OTT','Imperio otomano · extensión durante la guerra',1914,1918,'occupation'),
 'Nazi Germany':('DEU','Alemania nazi · territorios incorporados y ocupados',1938,1944,'occupation'),
 'Empire of Japan':('JPN','Imperio del Japón · territorios incorporados y ocupados',1931,1945,'occupation'),
 'Kingdom of Italy':('ITA','Italia · extensión y ocupaciones',1935,1943,'occupation'),
 'Union of Soviet Socialist Republics':('USSR','Unión Soviética · extensión territorial',1939,1945,'occupation'),
 'Independent State of Croatia':('CROATIA-CLIENT','Estado Independiente de Croacia · régimen dependiente',1941,1944,'client'),
 'Vichy France':('FRA-VICHY','Francia de Vichy · régimen colaboracionista',1940,1942,'collaboration'),
 'Communist Party of China':('CHN-COMMUNIST','China · control comunista',1927,1949,'civil-war'),
}
controls=[]
for i,f in enumerate(clio['features']):
    p=f['properties'];cfg=configs.get(p['Name'])
    if not cfg:continue
    key,name,start,end,relation=cfg
    if p['Components'] or p['FromYear']>end or p['ToYear']<start:continue
    note='Síntesis anual de Cliopatria, sin día uniforme dentro del año. El color identifica extensión y control territorial, no soberanía reconocida ni un frente militar diario.'
    if relation=='client':note+=' Régimen dependiente creado en 1941 bajo patrocinio del Eje; no se equipara a los aliados del Eje que conservaron gobiernos propios.'
    if relation=='collaboration':note+=' Gobierno colaboracionista de Vichy; la zona no ocupada fue invadida en noviembre de 1942.'
    controls.append(dict(type='Feature',id=f'control-{i}',geometry=f['geometry'],properties=dict(uid=f'control-{i}',name=name,originalName=p['Name'],identityKey=key,controller=key,relation=relation,start=max(start,p['FromYear']),end=min(end,p['ToYear']),kind='civil-war' if relation=='civil-war' else 'war',note=note,source=SOURCE)))
# Order large extents first, clients and local factions last. No reclassification of Romania as a puppet.
controls.sort(key=lambda f:({'occupation':0,'collaboration':1,'client':2,'civil-war':3}[f['properties']['relation']],f['properties']['start']))
save('historical-control.geojson',controls,coverage='1914/1949',transform='Central Powers annual WWI extents; Germany, Japan, Italy, USSR annual WWII extents; Croatia client state; Vichy annual extent 1940–1942 (southern occupation from November 1942); Chinese communist controlled areas. Omit composite unions, preserve geometry. Relations documented separately; Romania/Hungary not classified as puppets. No daily-front claim.')
manifest['entries'].sort(key=lambda e:e['file'])
manifest['importedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
