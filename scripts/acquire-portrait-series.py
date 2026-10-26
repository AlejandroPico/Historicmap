"""Acquire exact researched files and a dated portrait index, without rewriting offices.

Original/Commons thumbnail bytes stay intact. CSS framing of freely reusable
group photographs is declared separately; ND photographs are never framed.
"""
import hashlib,importlib.util,json,pathlib,re,urllib.parse,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
read=lambda p:json.loads(p.read_text(encoding='utf8'))
research=read(ROOT/'scripts/portrait-series-014-research.json');manifest=read(ROOT/'public/media/manifest.json')
by_file={m['file']:m for m in manifest['entries']}
old={m['title']:m for m in manifest['entries']}
rows=[r for r in research['portraits'] if r.get('priority')=='recommended' and not r.get('rightsReviewRequired')]
def acquire(r):
 title=r['fileTitle']
 if title in old:return r,old[title]
 if re.search(r'(?<![a-z])nd(?![a-z])',r['license'],re.I):return r,None
 url=r['originalUrl'] if r['bytes']<2000000 else r['thumbnailUrl']
 raw=h.download(url,max_bytes=5000000)
 extension='.png' if raw.startswith(b'\x89PNG') else '.jpg' if raw.startswith(b'\xff\xd8') else '.gif' if raw.startswith(b'GIF8') else None
 if not extension or len(raw)>5000000:raise ValueError('Invalid researched photo '+title)
 file='media/portrait-'+hashlib.sha256(title.encode()).hexdigest()[:20]+extension
 (ROOT/'public'/file).write_bytes(raw)
 return r,dict(file=file,title=title,url=r['commonsUrl'],sourceUrl=url,artist=r['author'],license=r['license'],licenseUrl=r.get('licenseUrl') or r['commonsUrl']+'#Licensing',attribution=r.get('attribution') or '',attributionRequired=True,credit=r.get('sourceStatement',''),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
records=[];missing=[]
for r in rows:
 try:
  r,m=acquire(r)
  if not m:missing.append(r['fileTitle']);continue
  old[r['fileTitle']]=m
  label=('Fotografía de '+r['photoDate']) if r.get('photoDate') else 'Retrato de época · toma sin fecha confirmada'
  if 'approximate' in r.get('photoDatePrecision',''):label+=' · fecha aproximada'
  m=dict(m)
  if r['person']=='Q332157' and r['fromYear']==1992:m.update(focalScale=2.1,focalPosition='60% 10%',presentationNote='Encuadre de la fotografía original del juramento de1992.')
  if r['person']=='Q9682' and r['fromYear']==1999:m.update(focalScale=2.1,focalPosition='50% 10%',presentationNote='Encuadre de la fotografía original de1999.')
  records.append(dict(person=r['person'],start=r['fromYear'],end=r['toYear'] or 9999,media=m,photoDate=r.get('photoDate'),dateLabel=label,source=r['commonsUrl'],note=r.get('note','')))
  print('Portrait',r['person'],r['fromYear'],r['fileTitle'],flush=True)
 except Exception as e:missing.append(dict(file=r['fileTitle'],reason=str(e)));print('Unavailable',r['fileTitle'],str(e)[:100],flush=True)
h.save(ROOT/'public/data/portrait-series.json',dict(format='dated-portrait-series',referenceDate='2026-10-26',records=records))
by_file.update({m['file']:m for m in old.values()})
manifest['entries']=sorted(by_file.values(),key=lambda m:m['file']);h.save(ROOT/'public/media/manifest.json',manifest)
h.save(ROOT/'.cache/portrait-series-014-acquisition.json',dict(records=len(records),missing=missing,rightsPending=[r['fileTitle'] for r in research['portraits'] if r.get('rightsReviewRequired')]))
print('Dated portraits',len(records),'unavailable',len(missing),flush=True)
