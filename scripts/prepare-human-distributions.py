from pathlib import Path
import json,hashlib,math,argparse
from shapely.geometry import shape,box,mapping
from shapely.ops import unary_union
from pyproj import Geod
parser=argparse.ArgumentParser(description='Compile canonically sourced human distributions and climate references.')
parser.add_argument('--check',action='store_true',help='Verify reproducibility without writing any file.')
check=parser.parse_args().check
R=Path('.');read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d):
 data=(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8')
 if check:
  if Path(p).read_bytes()!=data:raise ValueError('Stale compiled resource: '+str(p))
 else:Path(p).write_bytes(data)
manifest=read('public/data/manifest.json');version=read('package.json')['version'];policy=read('Tierra/Humanidad/metodologia.json')
def register(file,data,format,source,url,license,**extra):
 # Product-only patches do not change the declared version of scientific data.
 previous=next((e for e in manifest['entries'] if e['file']==file),None)
 resource_version=previous['version'] if check and previous else version
 write('public/data/'+file,data);b=Path('public/data/'+file).read_bytes();e={'file':file,'format':format,'version':resource_version,'source':source,'url':url,'license':license,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),**extra};manifest['entries']=[x for x in manifest['entries'] if x['file']!=file]+[e]
coasts=read('Tierra/Paleogeografia/CAO2024/fuentes.json')['originals']
assert len(coasts)==6
for s in coasts:
 raw=read(s['file']);out={'type':'FeatureCollection','features':[]}
 for i,f in enumerate(raw['features']):out['features'].append({'type':'Feature','id':i,'geometry':f['geometry'],'properties':{'name':'Masa continental reconstruida','code':'','color':i%12,'plateId':f.get('properties',{}).get('PLATEID1')}})
 register('coastlines-'+str(s['ma'])+'.geojson',out,'paleogeographic-reference','GPlates / Cao et al.2024',s['url'],'CC-BY-4.0',features=len(out['features']),year=-s['ma']*1000000)
write('Tierra/Paleogeografia/CAO2024/fuentes.json',{'model':'CAO2024','source':'https://doi.org/10.1016/j.gsf.2024.101922','license':'CC-BY-4.0','originals':coasts,'note':'Original geometry retained. Rotated continental coastlines, not bathymetry-derived Quaternary shorelines. Fossil coordinates retain their present-day reference.'})
# Resolve land masks once, without simplifying source vertices.
land={}
def coast_for(y):return 'countries.geojson' if y> -500000 else 'coastlines-'+str(min(7,max(1,int((-y+500000)//1000000))))+'.geojson'
def mask(file):
 if file not in land:land[file]=unary_union([shape(f['geometry']).buffer(0) for f in read('public/data/'+file)['features'] if f['geometry']['type'] in ['Polygon','MultiPolygon']])
 return land[file]
taxa=[];features=[];sites=[]
for p in sorted(Path('Tierra/Humanidad/linajes').glob('*/linaje.json')):
 d=read(p);d['canonicalFile']=p.as_posix();taxa.append(d)
 for reg in d['regions']:
  a,b=1949-round(reg['oldestKa']*1000),1949-round(reg['youngestKa']*1000)
  if d['key']=='sahelanthropus':a=-7000000 # Nominal7Ma consultation edge; source precision is~1Ma.
  assert a<=b<=-10001 and all(reg.get(x) is not None for x in ['source','spatialUncertaintyKm'])
  cuts=sorted(set([a,b+1]+[c+1 for c in range(-6500000,-499999,1000000) if a<c+1<=b]))
  for start,end in zip(cuts,cuts[1:]):
   cf=coast_for(start);west,south,east,north=reg['bounds'];radius=min(east-west,north-south)*policy['envelopeCornerFraction'];envelope=box(west,south,east,north).buffer(-radius).buffer(radius,quad_segs=12);geom=envelope.intersection(mask(cf)).buffer(0)
   if geom.is_empty:raise ValueError('Empty region '+reg['id'])
   if geom.geom_type=='GeometryCollection':geom=unary_union([g for g in geom.geoms if g.geom_type in ['Polygon','MultiPolygon']])
   props={'name':d['name'],'contextKey':'HUMAN-RANGE-'+d['key'].upper(),'lineage':d['key'],'group':d['group'],'color':d['color'],'start':start,'end':end-1,'phase':reg['id'],'regionLabel':reg['label'],'source':reg['source'],'canonicalFile':p.as_posix(),'coastFile':cf,'kind':'human-range','focus':d['focus'],'spatialUncertaintyKm':reg['spatialUncertaintyKm'],'note':reg.get('note',d['note'])}
   features.append({'type':'Feature','id':reg['id']+'@'+str(start),'geometry':mapping(geom),'properties':props})
 for f in d['fossils']:
  # Record approximate source windows, not a point's continuous occupation.
  a,b=1949-round(f['oldestKa']*1000),1949-round(f['youngestKa']*1000)
  record={'id':f['id'],'name':f['name'],'identityKey':f['id'],'entityCode':f['id'],'taxon':d['name'],'culture':'','start':a,'end':b,'ageMaxBP':round(f['oldestKa']*1000),'ageMinBP':round(f['youngestKa']*1000),'source':f['source'],'sourceLabel':'Registro de homininos · referencia regional','citation':d['name']+' · '+f['name'],'dateBasis':d['dateBasis']+' '+f['note'],'dateQuality':'reference-window','attributionBasis':d['classification']+'. '+d['note'],'locationBasis':'Referencia regional WGS84 actual, no GPS ni coordenada paleorreconstruida.','canonicalFile':p.as_posix(),'license':'CC0-1.0 (síntesis de hechos con atribución)','kind':'archaeological-reference','referenceKind':'archaeological-site'}
  sites.append({'type':'Feature','id':f['id'],'geometry':{'type':'Point','coordinates':f['coordinates']},'properties':record})
for source in sorted(Path('Tierra/Humanidad/fossiles').glob('*.json')):
 extra=read(source);assert extra['format']=='additional-hominin-evidence';sites.extend(extra['records'])
assert len({f['id'] for f in sites})==len(sites)
register('human-ranges.geojson',{'type':'FeatureCollection','features':features},'human-range-geometries','Historicmap · síntesis regional con fuentes taxonómicas','https://github.com/AlejandroPico/Historicmap/tree/main/Tierra/Humanidad','CC0-1.0 (envolventes); Natural Earth PD; Cao2024 CC-BY-4.0',features=len(features))
register('human-lineages.json',{'format':'human-lineage-catalogue','taxa':taxa,'policy':read('Tierra/Humanidad/metodologia.json')},'human-lineage-catalogue','Síntesis taxonómica con fuentes primarias e institucionales','https://humanorigins.si.edu/evidence/human-fossils/species','CC0-1.0 (síntesis editorial)',records=len(taxa))
register('hominin-sites.geojson',{'type':'FeatureCollection','features':sites},'dated-human-evidence','Referencias fósiles regionales, taxonomía documentada','https://github.com/AlejandroPico/Historicmap/tree/main/Tierra/Humanidad','CC0-1.0 (referencias editoriales); CC-BY-4.0 (Timmermann2022)',features=len(sites),records=len(sites))
# Quantify excess area relative to each region at0BP; display policy is editorial, not a climatic diagnosis.
ice=read('public/data/ice-model-index.json');geod=Geod(ellps='WGS84')
def areas(file):
 result={}
 for f in read('public/data/'+file)['features']:
  g=shape(f['geometry']);area=abs(geod.geometry_area_perimeter(g)[0])/1e6
  key=str(f.get('properties',{}).get('region','all'));result[key]=result.get(key,0)+area
 return result
baseline=areas(ice['samples'][0]['file']);samples=[]
for s in ice['samples']:
 a=areas(s['file']);extra=sum(max(0,v-baseline.get(k,0)) for k,v in a.items());samples.append({**s,'excessAreaKm2':round(extra),'autoVisible':extra>=1000000})
auto={'format':'ice-automatic-policy','thresholdKm2':1000000,'baselineBP':0,'meaning':'Umbral cartográfico editorial de variación visible a escala global; no fecha científica de comienzo de una glaciación.','samples':samples,'coverageStart':ice['consultationStart']}
write('Tierra/Cuaternario/hielo-automatico.json',auto)
register('ice-automatic-index.json',auto,auto['format'],'PaleoMIST original margins; editorial global display threshold','https://doi.org/10.1594/PANGAEA.905800','CC-BY-4.0',records=len(samples))
# LR04 keeps its measured isotopic values. This is climatic context, not an ice-outline generator.
p=Path('Tierra/Clima/LR04/originales/LR04.tab');text=p.read_text(encoding='utf-8');lines=text.split('*/',1)[-1].strip().splitlines();rows=[]
for line in lines[1:]:
 cells=line.split('\t')
 try:rows.append({'ageKa':float(cells[0])*1000,'delta18O':float(cells[1])})
 except (ValueError,IndexError):pass
# PANGAEA age column is ka BP; inspect original header before allowing scale.
print('LR04 HEADER',lines[0], 'first',lines[1],flush=True)
if '[ka BP]' in lines[0]:
 for r in rows:r['ageKa']/=1000
assert len(rows)>2000 and 5300<=max(r['ageKa'] for r in rows)<=5400
climate={'format':'benthic-isotope-context','source':'https://doi.org/10.1594/PANGAEA.701576','license':'CC-BY-3.0','rows':rows,'note':'LR04 δ18O combina señal del volumen de hielo y temperatura oceánica profunda. No delimita por sí solo mantos o paleocostas.','originalFile':p.as_posix(),'originalSha256':hashlib.sha256(p.read_bytes()).hexdigest()}
register('climate-lr04.json',climate,climate['format'],'Lisiecki & Raymo2005 LR04','https://doi.org/10.1594/PANGAEA.701576','CC-BY-3.0',records=len(rows))
write('public/data/manifest.json',manifest)
print('Prepared',len(taxa),'taxa',len(features),'range windows',len(sites),'reference points; ice automatic',[(s['ageBP'],s['autoVisible']) for s in samples],flush=True)
