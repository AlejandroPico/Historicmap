"""Rebuild local historical assets from identified sources, preserving source coordinates.
Requires Python and shapely==2.2.0. See docs/SOURCES.md for acquisition and licenses.
"""
import hashlib, json, pathlib, sys, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / '.cache/python-packages'))
from shapely.geometry import shape, mapping
from shapely import make_valid

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE, OUT = ROOT/'.cache', ROOT/'public/data'
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
manifest = read(OUT/'manifest.json')
entries = manifest['entries']
def save(file, data, **meta):
    path=OUT/file
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf8', newline='\n')
    entry=dict(file=file, bytes=path.stat().st_size, sha256=digest(path), **meta)
    if data.get('type')=='FeatureCollection': entry['features']=len(data['features'])
    entries[:]=[e for e in entries if e['file']!=file]
    entries.append(entry)
    print(file, path.stat().st_size, entry.get('features',''))

topology=read(CACHE/'cshapes-topology.json')
def arc(n):
    a=topology['arcs'][n if n>=0 else ~n]
    return a if n>=0 else a[::-1]
def ring(arcs):
    coords=[]
    for n in arcs: coords.extend(arc(n) if not coords else arc(n)[1:])
    return coords
def geometry(g):
    if g['type']=='MultiPolygon': return dict(type=g['type'],coordinates=[[ring(r) for r in p] for p in g['arcs']])
    if g['type']=='Polygon': return dict(type=g['type'],coordinates=[ring(r) for r in g['arcs']])
    raise ValueError(g['type'])
cs=[]
for g in topology['objects']['cshapes_2_gw']['geometries']:
    p=g['properties']
    if p['end']<'1900-01-01': continue
    cs.append(dict(type='Feature',id=p['fid'],properties=p,geometry=geometry(g)))
cmeta=dict(source='CShapes 2.0 · Schvitz et al. (2022), GW including dependencies',version='R package 2.0; 2020-06-07',url='https://icr.ethz.ch/data/cshapes/cshapes_2.0.tar.gz',license='CC-BY-NC-SA-4.0',sourceSha256=digest(CACHE/'cshapes.tar.gz'),transform='Decode unquantized TopoJSON; keep intervals ending in/after 1900. Coordinates retained; source attributes retained.',coverage='1900-01-01/2019-12-31')
entries[:]=[e for e in entries if e['file']!='history.geojson']
history=dict(type='Topology',arcs=topology['arcs'],objects={'countries':dict(type='GeometryCollection',geometries=[g for g in topology['objects']['cshapes_2_gw']['geometries'] if g['properties']['end']>='1900-01-01'])})
save('history.topojson',history,**cmeta,format='unquantized-topology',records=len(cs))

# Derived geometries stay separately licensed CC BY-NC-SA; no handmade outlines.
def at(name,date): return next(f for f in cs if f['properties']['country_name']==name and f['properties']['start']<=date<=f['properties']['end'])
def valid(f): return make_valid(shape(f['geometry']))
ukraine_before=valid(at('Ukraine','2013-12-31'))
crimea=ukraine_before.difference(valid(at('Ukraine','2014-12-31')))
egypt_before=valid(at('Egypt','1966-12-31'))
sinai=egypt_before.difference(valid(at('Egypt','1968-12-31')))
golan=valid(at('Syria','1966-12-31')).difference(valid(at('Syria','1968-12-31')))
overlays=[]
for uid,geom,name,start,end,note,source in [
 ('crimea',crimea,'Crimea y Sebastopol',2014,9999,'Territorio de Ucrania según A/RES/68/262. Ocupación y anexión reclamada por Rusia desde marzo de 2014; no equivale a soberanía reconocida. Esta capa no representa los demás frentes de la guerra de Ucrania.','https://press.un.org/en/2014/ga11493.doc.htm'),
 ('sinai-1956',sinai,'Sinaí · ocupación de 1956',1956,1956,'Ocupación israelí durante la crisis de Suez. La retirada se completó en marzo de 1957.','https://history.state.gov/milestones/1953-1960/suez'),
 ('sinai',sinai,'Sinaí · ocupación israelí',1967,1978,'Territorio egipcio ocupado por Israel tras la guerra de junio de 1967. No representa una transferencia de soberanía.','https://history.state.gov/milestones/1961-1968/arab-israeli-war-1967'),
 ('sinai-withdrawal',sinai,'Sinaí · retirada por fases',1979,1981,'Zona de retirada parcial israelí conforme al tratado de 1979. Contorno de referencia de 1967: NO delimita las fases intermedias. Retirada principal completada el 25 de abril de 1982; Taba se devolvió en 1989.','https://history.state.gov/milestones/1977-1980/camp-david'),
 ('golan',golan,'Altos del Golán · ocupación israelí',1967,9999,'Territorio sirio ocupado por Israel desde 1967. La resolución 497 del Consejo de Seguridad declaró sin efecto jurídico internacional la imposición israelí de sus leyes en 1981. No se cartografían aquí las variaciones de control posteriores a 2024.','https://docs.un.org/en/S/RES/497(1981)')
]:
    overlays.append(dict(type='Feature',id=len(overlays),properties=dict(uid=uid,name=name,start=start,end=end,note=note,source=source,kind='dispute'),geometry=mapping(geom)))
save('territorial-overlays.geojson',dict(type='FeatureCollection',features=overlays),**{**cmeta,'transform':'Polygon differences of dated CShapes geometries (Crimea, Sinai, Golan); contextual source notes; no invented intermediate withdrawal lines.'})

clio_path=next((CACHE/'cliopatria').glob('*.geojson'))
clio=read(clio_path)
sha=(CACHE/'cliopatria-sha.txt').read_text(encoding='utf-8-sig').strip()
war=[]
names={'Nazi Germany':'Alemania nazi · extensión y ocupaciones','Empire of Japan':'Imperio del Japón · extensión y ocupaciones','Kingdom of Italy':'Reino de Italia · extensión y ocupaciones'}
for f in clio['features']:
    p=f['properties']
    if p['Name'] in names and p['FromYear']<=1944 and p['ToYear']>=1938:
        war.append(dict(type='Feature',id=len(war),geometry=f['geometry'],properties=dict(uid='war-'+str(len(war)),name=names[p['Name']],originalName=p['Name'],start=max(1938,p['FromYear']),end=min(1944,p['ToYear']),kind='war',note='Síntesis anual de extensión territorial de Cliopatria. Incluye territorios incorporados y ocupados; no es un frente militar diario ni una afirmación de soberanía reconocida. La fuente no fija un día uniforme dentro del año.',source='https://github.com/Seshat-Global-History-Databank/cliopatria')))
save('ww2.geojson',dict(type='FeatureCollection',features=war),source='Cliopatria · Seshat Global History Databank',version=sha,url=f'https://raw.githubusercontent.com/Seshat-Global-History-Databank/cliopatria/{sha}/cliopatria.geojson.zip',sourceSha256=digest(CACHE/'cliopatria.zip'),license='CC-BY-4.0',coverage='1938/1944',transform='Select Germany, Japan and Italy polity records for 1938–1944; original coordinates retained, Spanish labels and scope notes added. Annual source has no uniform day of year.')

natural=read(CACHE/'natural-countries.json')
nm=next(e for e in entries if e['file']=='countries.geojson')
profiles={}
country_codes={}
countries=read(CACHE/'wb-countries.json')[1]
for p in countries:
    if p['region']['id']=='NA': continue
    profiles[p['id']]=dict(name=p['name'],capital=p['capitalCity'],region=p['region']['value'],income=p['incomeLevel']['value'],coordinates=[float(p['longitude'] or 0),float(p['latitude'] or 0)],series={})
indicator_names={'SP.POP.TOTL':'population','NY.GDP.MKTP.CD':'gdp','NY.GDP.PCAP.CD':'gdpPerCapita','SP.DYN.LE00.IN':'lifeExpectancy','SP.URB.TOTL.IN.ZS':'urban','AG.SRF.TOTL.K2':'area'}
sources=[]
for code,key in indicator_names.items():
    data=read(CACHE/f'wb-{code}.json')
    sources.append(read(CACHE/f'wb-{code}.json.source.json'))
    for obs in data[1]:
        iso=obs['countryiso3code']
        if iso not in profiles or obs['value'] is None: continue
        profiles[iso]['series'].setdefault(key,[]).append([int(obs['date']),obs['value']])
for f in natural['features']:
    p=f['properties']; iso=p.get('ISO_A3_EH')
    if not iso or iso=='-99': iso=p['ADM0_A3']
    iso={'KOS':'XKX'}.get(iso,iso)
    country_codes[p['ADM0_A3']]=iso
    profile=profiles.setdefault(iso,dict(name=p.get('NAME_ES') or p['NAME'],capital='',series={}))
    profile.update(name=p.get('NAME_ES') or p['NAME'],englishName=p['ADMIN'],official=p.get('FORMAL_ES') or p.get('FORMAL_EN') or p['ADMIN'],continent=p['CONTINENT'],subregion=p['SUBREGION'],territoryType=p['TYPE'],sovereign=p.get('SOVEREIGNT'))
for f in read(CACHE/'natural-places.json')['features']:
    p=f['properties']; iso=country_codes.get(p['ADM0_A3'])
    if p['ADM0CAP']==1 and iso in profiles and not profiles[iso].get('capital'):
        profiles[iso].update(capital=p.get('NAME_ES') or p['NAME'],coordinates=f['geometry']['coordinates'])
save('profiles.json',dict(retrieved=datetime.date.today().isoformat(),source='World Bank · World Development Indicators',indicators=indicator_names,sources=sources,codes=country_codes,countries=profiles),source='World Bank WDI + Natural Earth names',version='WDI API v2; source=2; '+','.join(sorted(set(s['version'] for s in sources))),url='https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?source=2&date=1960:2026&format=json&per_page=24000',license='CC-BY-4.0 with World Bank additional terms; Natural Earth public domain',format='country-indicator-series',transform='Exclude aggregates/nulls; preserve year/value; join country metadata and Natural Earth names/capital fallback. Map ADM0_A3 to ISO_A3_EH, with KOS to World Bank XKX. Invalid -99 never joins unrelated territories. Embedded sources identify six indicator URLs.')

places=[]
for f in read(CACHE/'natural-places.json')['features']:
    p=f['properties']
    if p['ADM0CAP']==1 or p['POP_MAX']>=2500000 or p['WORLDCITY']==1:
        places.append(dict(type='Feature',id=len(places),geometry=f['geometry'],properties=dict(name=p.get('NAME_ES') or p['NAME'],capital=bool(p['ADM0CAP']),country=p['ADM0NAME'],code=p['ADM0_A3'],rank=p['SCALERANK'],population=p['POP_MAX'],source='https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/')))
save('cities.geojson',dict(type='FeatureCollection',features=places),source='Natural Earth · populated places 1:10m',version=nm['version'],url=read(CACHE/'natural-places.json.source.json')['url'],license='Public domain',transform='Select national capitals, world cities, and urban places with POP_MAX >= 2.5 million. Preserve coordinates; city population used only for label ranking, not shown as a dated statistic.',coverage='Contemporary reference only; historical capitals come from dated CShapes records.')
manifest.update(importedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),transform='Per-entry transformations and licenses; original 26 snapshots unchanged.')
entries.sort(key=lambda e:e['file'])
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
