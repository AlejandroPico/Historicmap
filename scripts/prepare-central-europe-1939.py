"""Prepare explicit inputs for the1939 Central European composition.

Natural Earth Slovak reference is NOT presented as an independent1939 survey.
Runtime composition clips it to CShapes Czechoslovakia and dated Hungarian/
German extents. The original datasets remain unchanged and separately licensed.
"""
import copy,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
clio=read(next((ROOT/'.cache/cliopatria').glob('*.geojson')))
row=next(f for f in clio['features'] if f['properties']['Name']=='Hungarian Republic' and f['properties']['FromYear']==1939 and not f['properties']['Components'])
hungary=copy.deepcopy(row)
hungary.update(id='central-hungary-1939',properties=dict(uid='central-hungary-1939',name='Reino de Hungría',originalName='Hungary',sourceName=row['properties']['Name'],controller='HUN',identityKey='HUN',entityCode='HUN',code='',kind='war',relation='territorial-extension',start=1939,end=1939,source='https://github.com/Seshat-Global-History-Databank/cliopatria',note='Extensión anual húngara de1939, incluyendo cambios posteriores al primer arbitraje deViena. La etiqueta Republic del original no se adopta como régimen. Composición acotada a los componentes húngaro y checoslovaco deCShapes; no un frente diario.'))
hungary['properties']['relation']='incorporation'
world=read(OUT/'countries.geojson');slovakia=copy.deepcopy(next(f for f in world['features'] if f['properties']['code']=='SVK'))
slovakia.update(id='central-slovakia-reference-1939',properties=dict(uid='central-slovakia-reference-1939',name='Eslovaquia · República Eslovaca',originalName='Slovak Republic (1939–1945)',controller='SVK-1939',identityKey='SVK-1939',entityCode='SVW',code='',kind='war',relation='client',status='client',politicalStatus='Estado cliente de Alemania · soberanía restringida',start=1939,end=1939,capname='Bratislava',capital='Bratislava',caplong=17.1077,caplat=48.1486,territorialReference=True,referenceYear=2026,geometrySource='https://www.naturalearthdata.com/about/terms-of-use/',source='https://wwv.yadvashem.org/YV/en/exhibitions/communities/bratislava/during_holocaust.asp',dominantPower='DEU',influenceKind='client',influenceSource='https://encyclopedia.ushmm.org/content/en/article/jozef-tiso-1',influenceNote='Estado cliente, distinto de la ocupación alemana deBohemia yMoravia. No se convierte en territorio nacional alemán.',note='Contorno contemporáneo de referencia para separar la parte eslovaca, recortado conChecoslovaquia deCShapes, Hungría1939 y las incorporaciones alemanas1938. No es un levantamiento exacto de la frontera eslovaca1939 ni certifica ajustes municipales posteriores. La corrección cartográfica se limita a1939.'))
hungary['properties']['wikidata']='Q28'
slovakia['properties']['wikidata']='Q154401'
path=OUT/'central-europe-1939.geojson';path.write_text(json.dumps(dict(type='FeatureCollection',features=[hungary,slovakia]),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
manifest=read(OUT/'manifest.json');template=copy.deepcopy(next(e for e in manifest['entries'] if e['file']=='historical-control.geojson'))
template.update(file=path.name,features=2,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source='Cliopatria and Natural Earth, with explicit reference/derivation metadata',license='CC-BY-4.0 (Cliopatria); public domain (Natural Earth)',coverage='1939',transform='Unchanged Hungarian1939 source and contemporary Slovak reference input. Runtime clipping uses separately licensed CShapes baseline, German1938 incorporation and Hungarian1939 extent. Not a surveyed Slovak1939 boundary; no current statistics transferred.')
manifest['entries']=[e for e in manifest['entries'] if e['file']!=path.name]+[template];manifest['entries'].sort(key=lambda e:e['file'])
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Prepared1939 Hungarian extent and explicit Slovak reference input.')
