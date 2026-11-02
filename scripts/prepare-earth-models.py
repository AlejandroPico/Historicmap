"""Compile pinned PhanDA data and selected audiovisual scenario reference points.

The video reference is deliberately separate from published reconstructions.
No gas closure normalization, invented ocean fractions or unbounded extrapolation.
"""
from pathlib import Path
import csv,json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Tierra/Fanerozoico';OUT.mkdir(exist_ok=True)
def dump(name,value): (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raw=OUT/'originales/PhanDA_GMSTandCO2_percentiles.csv'
rows=list(csv.DictReader(raw.open(encoding='utf-8-sig')))
bins=[]
for r in rows:
 bins.append({'youngestMa':float(r['UpperAge']),'oldestMa':float(r['LowerAge']),'referenceMa':float(r['AverageAge']),'stage':r['Stage'],'temperature':{p:float(r['GMST_'+p])for p in ['05','16','50','84','95']},'co2ppm':{p:float(r['CO2_'+p])for p in ['05','16','50','84','95']}})
dump('phanda.json',{'schemaVersion':1,'source':'Judd et al.2024 · PhanDA','doi':'https://doi.org/10.1126/science.adk3705','url':'https://github.com/EJJudd/PhanDA','commit':'9f06c0d9764f3da77cb0819e0ac87c01182ba341','original':raw.name,'sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'scope':'Published temperature/CO2 percentile reconstruction in its own stratigraphic bins; not annual observations. Atlas uses bins older than7Ma.','bins':bins})
samples=list(csv.DictReader((ROOT/'Tierra/Investigacion/parte-1/muestras-indicadores-video.csv').open(encoding='utf-8-sig')))
video_bytes=(ROOT/'Tierra/Investigacion/parte-1/muestras-indicadores-video.csv').read_bytes()
# This is a Git-managed text CSV, unlike the byte-preserved PhanDA original.
# Match the repository's LF representation even in a Windows CRLF checkout.
video_sha=hashlib.sha256(video_bytes.replace(b'\r\n',b'\n')).hexdigest()
targets=[16,20,24,28,36,56,80,120,160,200,240,250,258,270,300,350,400,450,500,550,580,590,600,610,620,630,640,650,660,670,680]
records=[]
for t in targets:
 r=min(samples,key=lambda r:abs(float(r['video_seconds'])-t));seconds=float(r['video_seconds'])
 temp=r['temperatureC_parsed'];day=r['day_raw'].replace('l','1');m=re.search(r'(\d+)\s*h(?:r)?\s*(\d+)\s*m',day)
 gases={};rawgas={}
 if seconds<19:gases['rockVapor']=100
 else:
  for k in ['nitrogen','oxygen','argon','carbonDioxide','waterVapor','methane','ammonia','hydrogen','helium']:
   v=r[k+'_raw'];rawgas[k]=v
   if re.fullmatch(r'\s*\d+(?:\.\d+)?%\s*',v):gases[k]=float(v.strip().strip('%'))
 records.append({'ageMa':float(r['age_ma_parsed']),'seconds':seconds,'temperatureC':float(temp) if temp else None,'solarDayHours':int(m[1])+int(m[2])/60 if m else None,'dayRaw':r['day_raw'],'gases':gases,'gasLabels':rawgas,'temperatureRaw':r['temperatureC_raw']})
records.sort(key=lambda r:r['ageMa'])
dump('referencia-audiovisual.json',{'schemaVersion':1,'transcriptionSha256':video_sha,'transcriptionHashBasis':'UTF-8 source bytes with LF line endings (CRLF normalized)','source':'Algol · History of the Earth, escenario audiovisual solicitado por el propietario','url':'https://www.youtube.com/watch?v=Q1OreyX0-fw','sourceKind':'author-illustrative-scenario','meaning':'Selected numerical reference points transcribed from the video. Not a consensus reconstruction or continuous measurements. Nearest sample is used; no hidden interpolation.','checks':'Initial layout/anchors visually checked against archived frames; selected other values checked against structured transcription. Remaining uncertainty is explicit.','mixtureBasis':'Video does not specify wet/dry basis or total pressure. Rounded percentages are not normalized; 0.00% is displayed as below0.005%, not absolute absence.','samples':records})
print('Compiled',len(bins),'PhanDA intervals and',len(records),'separate audiovisual reference points')
