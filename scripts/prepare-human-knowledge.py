"""Compile entity-owned human articles, media and primary ice-core CO2; offline by default."""
from pathlib import Path
import argparse,json,hashlib,math

ROOT=Path(__file__).resolve().parents[1]
check=argparse.ArgumentParser()
check.add_argument('--check',action='store_true')
check=check.parse_args().check
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def encoded(d):return (json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8')
def save(p,b):
 target=ROOT/p
 if check:
  if target.read_bytes()!=b:raise ValueError('Stale compiled resource: '+p)
 else:target.write_bytes(b)
manifest=read('public/data/manifest.json')
def register(file,data,source,url,license,**extra):
 b=encoded(data);save('public/data/'+file,b)
 entry=dict(file=file,format=data['format'],version='Historicmap0.55',source=source,url=url,license=license,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),**extra)
 found=next((i for i,e in enumerate(manifest['entries'])if e['file']==file),None)
 if found is None:manifest['entries'].append(entry)
 else:manifest['entries'][found]=entry

owner=ROOT/'Tierra/Humanidad'
articles=[];images=[]
for path in sorted((owner/'linajes').glob('*/articulo.json')):
 article=json.loads(path.read_text(encoding='utf-8'));article['canonicalFile']=path.relative_to(ROOT).as_posix();articles.append(article)
for path in sorted(owner.glob('**/medios.json')):
 for image in json.loads(path.read_text(encoding='utf-8'))['images']:
  b=(ROOT/'public'/image['file']).read_bytes()
  if hashlib.sha256(b).hexdigest()!=image['sha256']or len(b)!=image['bytes']:raise ValueError('Original media checksum '+image['file'])
  images.append({**image,'canonicalFile':path.relative_to(ROOT).as_posix()})
topics=read('Tierra/Humanidad/temas/articulos.json')['articles']
articles=topics+articles
assert len({a['id']for a in articles})==len(articles)
sources=read('Tierra/Humanidad/fuentes-parte5.json')
if 'sources'in sources:sources=sources['sources']
for article in articles:
 for key in article['sourceIds']:
  if key not in sources:raise ValueError('Unregistered article source '+key)
 for key in article['related']:
  if key not in {a['id']for a in articles}|{'uncertainty','ice','climate-proxies','geo-Quaternary'}:raise ValueError('Unknown related article '+key)
data={'format':'human-knowledge','articles':articles,'sources':sources,'images':images,'siteReviews':read('Tierra/Humanidad/revisiones/parte5/contextos.json'),'videoReview':read('Tierra/Humanidad/revisiones/parte5/revision-video.json'),'inputReview':read('Tierra/Humanidad/revisiones/parte5/correspondencias.json')}
register('human-knowledge.json',data,'Historicmap · homininos, arqueología y clima','https://github.com/AlejandroPico/Historicmap/tree/main/Tierra/Humanidad','CC0-1.0 (textos); fotografías con sus licencias originales',records=len(articles))

original='Tierra/Clima/CO2-Antartida/originales/antarctica2015co2composite-noaa.txt'
raw=(ROOT/original).read_bytes();rows=[]
for line in raw.decode('utf-8-sig').splitlines():
 if not line.strip()or line.startswith('#'):continue
 cells=line.split()
 try:age,value,error=map(float,cells[:3])
 except ValueError:continue
 if not all(math.isfinite(x)for x in [age,value,error])or value<=0 or error<0:raise ValueError('Invalid ice-core observation')
 rows.append({'ageBP':age,'co2ppm':value,'sigmaPpm':error})
assert len(rows)>1000 and max(r['ageBP']for r in rows)>800000
rows.sort(key=lambda r:r['ageBP'])
data={'format':'ice-core-co2','source':'https://doi.org/10.25921/n8y4-bp27','paper':'https://doi.org/10.1002/2014GL061957','url':'https://www.ncei.noaa.gov/access/paleo-search/study/17975','originalUrl':'https://www.ncei.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2composite-noaa.txt','originalFile':original,'originalSha256':hashlib.sha256(raw).hexdigest(),'referenceEpoch':1950,'units':'ppm','error':'one standard deviation; source substitutes the record mean uncertainty where individual errors were unavailable','ageBasis':'Published gas ages, calendar years BP1950; AICC2012 except the constituent recent Law Dome, WAIS and Siple Dome records. Not ice ages.','selection':'Nearest actual sample, with its own gas age visible; no interpolation or extrapolation. Application scope: prehistoric consultation through10001BCE; later published records retain precedence.','rows':rows}
register('ice-core-co2.json',data,'Bereiter et al.2015 · Antarctic ice-core composite / NOAA NCEI',data['source'],'NOAA/WDS public scientific data; retain original author attribution',records=len(rows))
save('public/data/manifest.json',encoded(manifest))
print('Prepared',len(articles),'human articles,',len(images),'original images and',len(rows),'CO2 observations')
