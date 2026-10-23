"""Acquire licensed portraits for dated 1970–1989 authorities without altering terms.

Non-human collective authorities retain their names without invented photographs.
The final merge rereads identities, preserving independent preparation work.
"""
import importlib.util,pathlib,json,re,hashlib,urllib.parse,html,argparse
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--people',nargs='+',help='Only acquire these existing human identifiers');parser.add_argument('--start',default='1970-01-01');parser.add_argument('--end',default='1990-01-01');parser.add_argument('--image',nargs=2,action='append',metavar=('PERSON','COMMONS_TITLE'),help='Explicitly reviewed alternative photograph; retains the same identity and license checks');parser.add_argument('--original',action='store_true',help='Try the original published image when thumbnail acquisition failed; retain the 5 MB file limit and license checks');args=parser.parse_args()
reviewed_images=dict(args.image or [])
spec=importlib.util.spec_from_file_location('h',pathlib.Path(__file__).with_name('enrich-1970-authorities.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
excluded={(r['person'],r['title']) for r in json.loads(pathlib.Path(__file__).with_name('media-exclusions.json').read_text(encoding='utf8'))}
data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'))
for country in data['countries'].values():
 for leader in country['leaders']:
  if leader.get('portrait') and (leader['person'],leader['portrait']['title']) in excluded:leader.pop('portrait')
terms=[l for c in data['countries'].values() for l in c['leaders'] if l['start']<args.end and l['end']>=args.start]
existing={l['person']:l['portrait'] for c in data['countries'].values() for l in c['leaders'] if l.get('portrait')}
targets=sorted({l['person'] for l in terms if re.fullmatch(r'Q\d+',l['person']) and l['person'] not in existing})
if args.people:targets=[q for q in targets if q in args.people]
manifest=json.loads((h.OUT/'media/manifest.json').read_text(encoding='utf8'))
media={m['file']:m for m in manifest['entries']};portraits={};missing=[]
def acquire(q):
 e=h.entity(q)
 if not any(isinstance(v,dict) and v.get('id')=='Q5' for v in h.values(e,'P31')):return None
 for filename in ([reviewed_images[q]] if q in reviewed_images else h.values(e,'P18')):
  if (q,filename) in excluded:continue
  if not isinstance(filename,str) or filename.lower().endswith('.svg'):continue
  digest=hashlib.sha256(filename.encode()).hexdigest()[:20]
  params=dict(action='query',titles='File:'+filename,redirects=1,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=320,format='json')
  info=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'commons-'+digest)
  page=next(iter(info.get('query',{}).get('pages',{}).values()),{});ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{});lic=meta.get('LicenseShortName',{}).get('value','')
  accepted=any(v in lic.lower() for v in ['public domain','cc0','cc by','cc-by','pd-']) or lic in ['Attribution','OGL 3','OGL v1.0','GODL-India','European Parliament','KOGL Type 1','PDM-owner']
  if not accepted or 'nd' in lic.lower():continue
  url=((ii.get('url') if args.original else ii.get('thumburl') or ii.get('url')) or '').split('?')[0]
  if not url:continue
  relative='media/portrait-'+digest+('.png' if '.png' in url.lower() else '.jpg');dest=h.OUT/relative
  if relative in media and dest.exists():return media[relative]
  if not dest.exists():
   raw=h.download(url,max_bytes=5_000_000)
   if len(raw)>5_000_000 or not raw.startswith((b'\xff\xd8',b'\x89PNG')):continue
   dest.write_bytes(raw)
  clean=lambda value:html.unescape(re.sub('<[^>]*>','',value))
  return dict(file=relative,title=filename,url=ii.get('descriptionurl',''),artist=clean(meta.get('Artist',{}).get('value','')),license=lic,licenseUrl=meta.get('LicenseUrl',{}).get('value','') or ii.get('descriptionurl','')+'#Licensing',attribution=clean(meta.get('Attribution',{}).get('value','')),attributionRequired=lic=='Attribution' or meta.get('AttributionRequired',{}).get('value')=='true',credit=clean(meta.get('Credit',{}).get('value','')),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,sourceUrl=url)
 return None
for offset in range(0,len(targets),25):
 for q,result in h.parallel(acquire,targets[offset:offset+25]):
  if result:portraits[q]=result
  else:missing.append(q)
 print('Portrait review',min(offset+25,len(targets)),'/',len(targets),'accepted',len(portraits),flush=True)
data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'))
available={**existing,**portraits}
reused=0
for c in data['countries'].values():
 for leader in c['leaders']:
  if leader.get('portrait') and (leader['person'],leader['portrait']['title']) in excluded:leader.pop('portrait')
  if not leader.get('portrait') and leader['person'] in available:
   leader['portrait']=available[leader['person']]
   if leader['person'] in existing:reused+=1
manifest=json.loads((h.OUT/'media/manifest.json').read_text(encoding='utf8'))
media={m['file']:m for m in manifest['entries']};media.update({m['file']:m for m in portraits.values()})
h.save(h.OUT/'data/identities.json',data);manifest['entries']=sorted(media.values(),key=lambda m:m['file']);h.save(h.OUT/'media/manifest.json',manifest)
h.save(h.CACHE/('portraits-'+args.start[:4]+'-curation-audit.json'),dict(retrieved=h.TODAY,reviewed=len(targets),added=len(portraits),reusedTerms=reused,missing=missing))
print('Portraits added',len(portraits),'reused terms',reused,'remaining',len(missing),flush=True)
