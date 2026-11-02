"""Author-supplied Batchelor2019 ice hypotheses; no interpolated chronology.

Use --fetch once for pinned binary originals, --check for offline reproduction.
Requires Shapely, pyproj and pyshp only during data preparation.
"""
from pathlib import Path
import argparse, hashlib, json, math, time, urllib.request, logging, gzip
from concurrent.futures import ThreadPoolExecutor
import shapefile
from pyproj import CRS, Transformer
from shapely.geometry import Polygon, MultiPolygon, Point, box, mapping, shape
from shapely.ops import unary_union,transform
from shapely.affinity import translate
from shapely.validation import make_valid

ROOT=Path(__file__).resolve().parents[1]
OWNER=ROOT/'Tierra/Cuaternario/Batchelor2019'
parser=argparse.ArgumentParser();parser.add_argument('--fetch',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
if args.fetch and args.check:parser.error('--fetch and --check are separate operations')
logging.getLogger('shapefile').setLevel(logging.ERROR)
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def serial(data):return (json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8')
def save(p,b):
 p=Path(p)
 if args.check:
  if p.read_bytes()!=b:raise ValueError('Stale resource '+str(p))
 else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def get(url):
 for attempt in range(4):
  try:return urllib.request.urlopen(url,timeout=60).read()
  except Exception:
   if attempt==3:raise
   time.sleep(1+attempt)
def listing(url):
 out=[]
 while url:
  data=json.loads(get(url));out+=data['data'];url=data['links'].get('next')
 return out
plan=read(OWNER/'plan.json')
api='https://api.osf.io/v2/nodes/7jen3/files/osfstorage/'
if args.fetch:
 root=listing(api+'?page%5Bsize%5D=100');jobs=[]
 for s in plan['slices']:
  folder=next(e for e in root if e['attributes']['name']==s['folder'])
  sub=listing(api+folder['attributes']['path'].lstrip('/')+'?page%5Bsize%5D=100')
  recon=next(e for e in sub if 'hypothesised' in e['attributes']['name'])
  files=listing(api+recon['attributes']['path'].lstrip('/')+'?page%5Bsize%5D=100')
  for e in files:
   name=e['attributes']['name']
   if Path(name).suffix.lower() not in ['.shp','.shx','.dbf','.prj','.cpg']:continue
   jobs.append((s['id'],name,e))
 def acquire(job):
  sid,name,e=job;p=OWNER/'originales'/sid/name
  b=p.read_bytes() if p.exists() else get(e['links']['download'])
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  return {'slice':sid,'file':p.relative_to(ROOT).as_posix(),'url':e['links']['download'],'osfId':e['id'],'version':e['attributes'].get('current_version'),'sha256':sha(b),'bytes':len(b)}
 with ThreadPoolExecutor(max_workers=6)as pool:originals=list(pool.map(acquire,jobs))
 entry=next(e for e in root if e['attributes']['name']=='README.txt');b=get(entry['links']['download']);p=OWNER/'originales/README.txt';p.write_bytes(b)
 originals.append({'slice':'documentation','file':p.relative_to(ROOT).as_posix(),'url':entry['links']['download'],'osfId':entry['id'],'sha256':sha(b),'bytes':len(b)})
 save(OWNER/'fuentes.json',serial({'model':plan['model'],'source':plan['source'],'repository':plan['repository'],'rightsNote':plan['rightsNote'],'retrieved':'2026-11-02','originals':originals}))
 print('Original files',len(originals),flush=True)
sources=read(OWNER/'fuentes.json')
for e in sources['originals']:
 if sha((ROOT/e['file']).read_bytes())!=e['sha256']:raise ValueError('Original checksum '+e['file'])

def ring(points,transformer):
 out=[]
 for x,y,*_ in points:
  lon,lat=transformer.transform(x,y)
  if not math.isfinite(lon)or not math.isfinite(lat):raise ValueError('Coordinate outside the source projection domain')
  if out:
   while lon-out[-1][0]>180:lon-=360
   while lon-out[-1][0]<-180:lon+=360
  out.append([lon,min(90,max(-90,lat))])
 # Polar rings, if any, must close at the pole rather than across the world.
 if abs(out[-1][0]-out[0][0])>180:out.extend([[out[-1][0],90],[out[0][0],90],out[0]])
 else:out[-1]=out[0]
 return out
def polygon_parts(g):
 if g.geom_type=='Polygon':return [g]
 return [part for child in getattr(g,'geoms',[]) for part in polygon_parts(child)]
def converted(geometry,transformer):
 polygons=geometry['coordinates'] if geometry['type']=='MultiPolygon' else [geometry['coordinates']]
 pieces=[]
 for poly in polygons:
  shell=ring(poly[0],transformer);holes=[]
  for raw in poly[1:]:
   hole=ring(raw,transformer);offset=360*round((shell[0][0]-hole[0][0])/360);holes.append([[x+offset,y]for x,y in hole])
  g=make_valid(Polygon(shell,holes))
  for k in range(math.floor((g.bounds[0]+180)/360),math.floor((g.bounds[2]+180)/360)+1):
   cut=g.intersection(box(-180+360*k,-90,180+360*k,90))
   if not cut.is_empty:pieces.append(translate(cut,xoff=-360*k))
 g=make_valid(unary_union(pieces));parts=polygon_parts(g)
 return MultiPolygon(parts)

manifest=read(ROOT/'public/data/manifest.json');index=[];audit=[]
projected=CRS.from_user_input('ESRI:102017')
to_geo=Transformer.from_crs(projected,'EPSG:4326',always_xy=True)
equator_radius=abs(Transformer.from_crs(4326,projected,always_xy=True).transform(0,0)[1])
# Several minimum templates include present-day global glacier polygons, including Antarctica.
# Retain originals, but expose only the Northern Hemisphere covered by this synthesis.
hemisphere=Point(0,0).buffer(equator_radius,quad_segs=4096)
def upsert(entry):
 old=next((i for i,e in enumerate(manifest['entries'])if e['file']==entry['file']),None)
 if old is None:manifest['entries'].append(entry)
 else:manifest['entries'][old]=entry
for s in plan['slices']:
 features=[];folder=OWNER/'originales'/s['id']
 for shp in sorted(folder.glob('*.shp')):
  variant='best' if 'best' in shp.stem.lower() else 'minimum' if '_min' in shp.stem.lower() else 'maximum' if '_max' in shp.stem.lower() else None
  if not variant:raise ValueError('Unknown estimate '+str(shp))
  source_crs=CRS.from_wkt(shp.with_suffix('.prj').read_text())
  normalize=None if source_crs.equals(projected)else Transformer.from_crs(source_crs,projected,always_xy=True)
  reader=shapefile.Reader(str(shp),encoding='utf-8',encodingErrors='replace')
  valid=[];degenerate=[];source_area=0;outside_area=0;outside_records=[]
  for i,row in enumerate(reader.iterShapeRecords()):
   raw=shape(row.shape.__geo_interface__)
   if normalize:raw=transform(normalize.transform,raw)
   repaired=make_valid(raw)
   parts=polygon_parts(repaired)
   if not parts or sum(p.area for p in parts)==0:degenerate.append(i);continue
   source_area+=sum(p.area for p in parts)
   for part in parts:
    kept=part.intersection(hemisphere);excluded=max(0,part.area-kept.area);outside_area+=excluded
    if excluded>1:outside_records.append(i)
    valid.extend(polygon_parts(kept))
  merged=unary_union(valid);geom=converted(mapping(merged),to_geo)
  if geom.is_empty or not geom.is_valid:raise ValueError('Invalid reconstruction '+str(shp))
  audit.append({'file':shp.relative_to(ROOT).as_posix(),'sourceCRS':source_crs.to_string(),'workingCRS':projected.to_string(),'sourceRecords':len(reader),'zeroAreaRecordIndices':degenerate,'sourceAreaM2':source_area,'outsideNorthernHemisphereAreaM2':outside_area,'outsideNorthernHemisphereRecords':sorted(set(outside_records)),'projectedAreaM2':merged.area,'meaning':'Original CRS respected, including WGS84 MIS16 maximum. Valid polygon parts intersected with Northern Hemisphere scope; Antarctic/global-template remnants excluded explicitly, not treated as dated southern ice. All original files retained. No simplification.'})
  props={'model':plan['model'],'slice':s['id'],'variant':variant,'youngestKa':s['youngestKa'],'oldestKa':s['oldestKa'],'character':s['character'],'scope':plan['coverage'],'source':plan['source'],'canonicalFile':shp.relative_to(ROOT).as_posix(),'sourceRecords':len(reader),'zeroAreaRecords':len(degenerate)}
  features.append({'type':'Feature','id':s['id']+'-'+variant,'geometry':mapping(geom),'properties':props})
 if set(f['properties']['variant']for f in features)!={'best','minimum','maximum'}:raise ValueError('Missing uncertainty variant '+s['id'])
 files={}
 for f in features:
  file='ice-batchelor-'+s['id']+'-'+f['properties']['variant']+'.geojson.gz'
  raw=serial({'type':'FeatureCollection','features':[f]});compressed=gzip.compress(raw,mtime=0);b=compressed[:9]+bytes([255])+compressed[10:]
  save(ROOT/'public/data'/file,b);files[f['properties']['variant']]=file
  e={'file':file,'format':'dated-ice-hypothesis-gzip','version':'Batchelor2019 · Historicmap0.55','source':plan['model'],'url':plan['source'],'license':plan['license'],'features':1,'bytes':len(b),'uncompressedBytes':len(raw),'sha256':sha(b),'transform':'Original shapefile CRS respected, repaired and reprojected to WGS84, clipped to declared Northern Hemisphere scope, split at antimeridian; no simplification. Scope exclusions audited. One variant per lossless gzip resource; deterministic OS-neutral header. Not annual margins.'}
  upsert(e)
 age=round((s['youngestKa']+s['oldestKa'])*500)
 index.append({**s,'file':files['best'],'uncertaintyFiles':[files['minimum'],files['maximum']],'ageBP':age,'referenceYear':1949-age,'features':1,'scope':plan['coverage'],'model':plan['model'],'source':plan['source']})
 # Remove only this compiler's obsolete, unpublished uncompressed projection.
 oldfile='ice-batchelor-'+s['id']+'.geojson';oldpath=ROOT/'public/data'/oldfile
 if not args.check and oldpath.exists():oldpath.unlink()
 manifest['entries']=[x for x in manifest['entries']if x['file']!=oldfile]
 print(s['id'],[(f['properties']['variant'],files[f['properties']['variant']])for f in features],flush=True)
data={'format':'quaternary-ice-synthesis-index','model':plan['model'],'source':plan['source'],'repository':plan['repository'],'license':plan['license'],'coverage':plan['coverage'],'selection':plan['selection'],'samples':index}
b=serial(data);file='ice-synthesis-index.json';save(ROOT/'public/data'/file,b)
e={'file':file,'format':data['format'],'version':'Historicmap0.55','source':plan['model'],'url':plan['source'],'license':plan['license'],'records':len(index),'bytes':len(b),'sha256':sha(b)}
upsert(e)
save(ROOT/'public/data/manifest.json',serial(manifest))
save(OWNER/'auditoria-geometrias.json',serial({'model':plan['model'],'noSimplification':True,'records':audit}))
