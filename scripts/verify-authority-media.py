"""Preparation-time byte and raster validation (Pillow; no file mutations)."""
import hashlib,json,pathlib
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[1]/'public'
manifest=json.loads((root/'media/manifest.json').read_text(encoding='utf8'))
data=json.loads((root/'data/identities.json').read_text(encoding='utf8'))
bad=[];rasters=0
for media in manifest['entries']:
    path=root/media['file']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=media['sha256']:bad.append(media['file']+': hash mismatch')
    if path.suffix.lower() in ['.jpg','.png','.webp']:
        rasters+=1
        try:
            with Image.open(path) as image:image.verify()
        except Exception as error:bad.append(media['file']+': '+str(error))
reference=data['retrieved'];year_start=reference[:4]+'-01-01'
annual=[leader for country in data['countries'].values() for leader in country['leaders'] if leader['start']<=reference and leader['end']>=year_start]
print(json.dumps(dict(keys=len(data['countries']),terms=sum(len(c['leaders']) for c in data['countries'].values()),annualRecords=len(annual),annualPeople=len({l['person'] for l in annual}),annualPhotoPeople=len({l['person'] for l in annual if l.get('portrait')}),media=len(manifest['entries']),rasters=rasters,bad=bad),ensure_ascii=True),flush=True)
for q in ['Q191045','Q19943','Q29179']:
    records=[l for c in data['countries'].values() for l in c['leaders'] if l['person']==q]
    print(q,'records',len(records),'portraits',sum(bool(l.get('portrait')) for l in records),flush=True)
if bad:raise SystemExit(1)
