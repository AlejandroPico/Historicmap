"""Compile entity-owned regional evidence; never infer dates or sovereignty.

Inputs: Países/<entity>/poblamiento/*.json and credited original geometries.
Public output is a separate reference dataset, never a political border merge.
"""
import pathlib,json,hashlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf8'))
def main():
 features=[];seen=set();reviews=[];ranges=[]
 for path in sorted((ROOT/'Países').glob('*/poblamiento/*.json')):
  d=read(path);key=d['key']
  if key in seen:raise ValueError('Duplicate cultural key '+key)
  seen.add(key);reviews.append(dict(key=key,ownerKey=d['ownerKey'],name=d['name'],kind=d['kind'],file=path.relative_to(ROOT).as_posix(),originalNames=d['originalNames'],decision=d['decision'],reviewStatus=d.get('reviewStatus'),note=d['interpretation']))
  ranges.append(d['reviewedRange'])
  if d['decision']=='excluded':continue
  if not d['references']or not d['spatialUncertainty']or not d['temporalUncertainty']:raise ValueError('Missing evidence '+key)
  if not re.fullmatch(r'[A-Z0-9-]+\.geojson',d['geometryFile']):raise ValueError('Invalid original path')
  geometry=read(path.parent/d['geometryFile']);provenance=d['geometryProvenance']
  if hashlib.sha256((path.parent/d['geometryFile']).read_bytes()).hexdigest()!=d['geometrySha256']:raise ValueError('Original checksum '+key)
  for i,phase in enumerate(d['phases']):
   if phase['start']>phase['end']or not phase['dateBasis']or phase['start']<d['reviewedRange'][0]or phase['end']>d['reviewedRange'][1]:raise ValueError('Invalid cultural phase '+key)
   props={k:d[k]for k in ['key','ownerKey','name','originalNames','kind','region','interpretation','spatialUncertainty','temporalUncertainty','references','politicalKeys','color','focus','reviewStatus','pending','sourceGrouping']}
   props.update(phase,contextKey=key,entityType=d['kind'],source=provenance['url'],sourceYear=provenance['year'],sourceFeatureIds=provenance['featureIds'],sourceLicense=provenance['license'],canonicalFile=path.relative_to(ROOT).as_posix(),code='')
   props['name']=phase.get('label',d['name']);features.append(dict(type='Feature',id=f'{key}:{i}',geometry=geometry['geometry'],properties=props))
 output=ROOT/'public/data/cultural-regions.geojson';raw=(json.dumps(dict(type='FeatureCollection',features=features),ensure_ascii=False,separators=(',',':'))+'\n').encode();output.write_bytes(raw)
 manifest=read(ROOT/'public/data/manifest.json');entry=dict(file=output.name,format='dated-cultural-regions',source='Entity-owned documentary review; Historical Basemaps source polygons',version='Historicmap 0.28.0; review 2026-10-27',url='https://github.com/AlejandroPico/Historicmap/blob/main/docs/CULTURAL-COVERAGE.md',license='GPL-3.0 (Historical Basemaps geometry); original editorial metadata',features=len(features),coverageStart=min(f['properties']['start']for f in features),coverageEnd=max(f['properties']['end']for f in features),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),transform='Original source polygons/components retained as approximate regional references, with explicit temporal consultation windows; separate from political sovereignty. Decisions and sources owned by each entity in Países.')
 manifest['entries']=[e for e in manifest['entries']if e['file']!=entry['file']]+[entry];(ROOT/'public/data/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 windows=[]
 for a,b in sorted(ranges):
  if windows and a<=windows[-1]['end']+1:windows[-1]['end']=max(windows[-1]['end'],b)
  else:windows.append(dict(start=a,end=b))
 index=dict(format='cultural-coverage-index',reviewedThrough=max(b for a,b in ranges),windows=windows,records=[{k:f['properties'][k]for k in ['contextKey','ownerKey','name','originalNames','kind','start','end','canonicalFile']}for f in features])
 index['excluded']=[{k:r[k]for k in ['key','ownerKey','name','file','decision']}for r in reviews if r['decision']=='excluded']
 ip=ROOT/'public/data/cultural-index.json';ir=(json.dumps(index,ensure_ascii=False,separators=(',',':'))+'\n').encode();ip.write_bytes(ir)
 ie=dict(file=ip.name,format=index['format'],source='Entity-owned regional coverage inventory',version='Historicmap 0.28.0; review 2026-10-27',url=entry['url'],license='Original editorial metadata; linked source geometry licensed separately',records=len(index['records']),bytes=len(ir),sha256=hashlib.sha256(ir).hexdigest())
 manifest['entries']=[e for e in manifest['entries']if e['file']!=ie['file']]+[ie];(ROOT/'public/data/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 report=dict(scope='Regional coverage, documentary review and consultation windows; not an annually surveyed cultural atlas.',windows=windows,entities=reviews,phases=len(features))
 report['snapshotInventory']=[]
 for year in [500,1000,1492]:
  source=ROOT/f'public/data/world_{year}.geojson';snapshot=read(source)
  names=sorted({f['properties']['name']for f in snapshot['features']if f['properties']['name']!='Masa continental'})
  report['snapshotInventory'].append(dict(year=year,file=source.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),names=[dict(name=name,decisions=[r['key']for r in reviews if name in r['originalNames']],geometryPolicy='Only an explicitly reviewed entity dossier can adopt this geometry; an anchor snapshot is not annual evidence.')for name in names]))
 (ROOT/f'docs/CULTURAL-REVIEW-{min(a for a,b in ranges)}-{index["reviewedThrough"]}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('Regional dossiers',len(reviews),'compiled phases',len(features))
if __name__=='__main__':main()
