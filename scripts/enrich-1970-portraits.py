"""Acquire licensed portraits for dated 1970–1989 authorities without altering terms.

Non-human collective authorities retain their names without invented photographs.
The final merge rereads identities, preserving independent preparation work.
"""
import importlib.util,pathlib,json,re,hashlib,urllib.parse,html,argparse
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--people',nargs='+',help='Only acquire these existing human identifiers');parser.add_argument('--start',default='1970-01-01');parser.add_argument('--end',default='1990-01-01');parser.add_argument('--image',nargs=2,action='append',metavar=('PERSON','COMMONS_TITLE'),help='Explicitly reviewed alternative photograph; retains the same identity and license checks');parser.add_argument('--original',action='store_true',help='Try the original published image when thumbnail acquisition failed; retain the 5 MB file limit and license checks');parser.add_argument('--countries',nargs='+',help='Only update these country catalogues, preserving every other country');parser.add_argument('--replace-reviewed',action='store_true',help='Replace existing portraits only for exact reviewed candidates');args=parser.parse_args()
review_file=pathlib.Path(__file__).with_name('media-corrections-013.json')
reviews=json.loads(review_file.read_text(encoding='utf8')) if review_file.exists() else []
reviewed_records={r['person']:r for r in reviews if r.get('status')=='candidate-verified-metadata'}
pending_provenance={r['person'] for r in reviews if r.get('status')=='needs-provenance-verification'}
reviewed_images={q:r['title'] for q,r in reviewed_records.items()};reviewed_images.update(dict(args.image or []))
swiss_reviews=json.loads(pathlib.Path(__file__).with_name('swiss-portrait-reviews.json').read_text(encoding='utf8'))['portraits']
swiss_reviews={(r['qid'],r['title']):r for r in swiss_reviews}
spec=importlib.util.spec_from_file_location('h',pathlib.Path(__file__).with_name('enrich-1970-authorities.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
excluded={(r['person'],r['title']) for r in json.loads(pathlib.Path(__file__).with_name('media-exclusions.json').read_text(encoding='utf8'))}
data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'))
def selected_countries(data):
 return [c for key,c in data['countries'].items() if not args.countries or key in args.countries]
for country in selected_countries(data):
 for leader in country['leaders']:
  if leader.get('portrait') and (leader['person'],leader['portrait']['title']) in excluded:leader.pop('portrait')
terms=[l for c in selected_countries(data) for l in c['leaders'] if l['start']<args.end and l['end']>=args.start]
existing={l['person']:l['portrait'] for c in data['countries'].values() for l in c['leaders'] if l.get('portrait')}
targets=sorted({l['person'] for l in terms if re.fullmatch(r'Q\d+',l['person']) and (l['person'] not in existing or args.replace_reviewed and l['person'] in reviewed_images)})
if args.people:targets=[q for q in targets if q in args.people]
manifest=json.loads((h.OUT/'media/manifest.json').read_text(encoding='utf8'))
media={m['file']:m for m in manifest['entries']};portraits={};missing=[]
def swiss_permission(q,filename,lic,credit,page):
 """A reviewed pair plus the exact public VRT declaration, never a CFU wildcard."""
 review=swiss_reviews.get((q,filename))
 if not review or review['license']!='Copyrighted free use' or lic!=review['license']:return None
 revision=page.get('revisions',[{}])[0]
 wiki=revision.get('slots',{}).get('main',{}).get('*','')
 official=lambda value:bool(re.search(r'https?://(?:www\.)?admin\.ch/',html.unescape(value),re.I))
 if page.get('title')!='File:'+filename or revision.get('revid')!=review['revision']:return None
 if not official(credit) or not re.search(r'(?im)^\|Source\s*=\s*https?://(?:www\.)?admin\.ch/',wiki):return None
 if not re.search(r'\{\{\s*PermissionTicket\s*\|\s*id\s*=\s*'+re.escape(review['ticket'])+r'\s*\}\}',wiki,re.I):return None
 if not re.search(r'\{\{\s*copyrighted free use\s*\}\}',wiki,re.I):return None
 return dict(ticket=review['ticket'],revision=review['revision'],source=review['source'],reviewUrl='https://commons.wikimedia.org/w/index.php?oldid='+str(review['revision']))
def acquire(q):
 if q in pending_provenance and q not in dict(args.image or []):return None
 e=h.entity(q)
 if not any(isinstance(v,dict) and v.get('id')=='Q5' for v in h.values(e,'P31')):return None
 for filename in ([reviewed_images[q]] if q in reviewed_images else h.values(e,'P18')):
  if (q,filename) in excluded:continue
  if not isinstance(filename,str) or filename.lower().endswith('.svg'):continue
  if re.search(r'AI.generated|Pope Trump AI|Ngultrum|banknote',filename,re.I):continue
  digest=hashlib.sha256(filename.encode()).hexdigest()[:20]
  params=dict(action='query',titles='File:'+filename,redirects=1,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=320,format='json')
  info=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'commons-'+digest)
  page=next(iter(info.get('query',{}).get('pages',{}).values()),{});ii=page.get('imageinfo',[{}])[0];meta=ii.get('extmetadata',{});lic=meta.get('LicenseShortName',{}).get('value','')
  accepted=any(v in lic.lower() for v in ['public domain','cc0','cc by','cc-by','pd-']) or lic in ['Attribution','OGL 3','OGL v1.0','GODL-India','European Parliament','KOGL Type 1','PDM-owner']
  # French public-data Open Licence permits reuse with source attribution;
  # accept its exact label and official licence URL, not an arbitrary free-use claim.
  open_licence=lic=='Licence Ouverte' and urllib.parse.urlparse(meta.get('LicenseUrl',{}).get('value','')).hostname in ['www.etalab.gouv.fr','etalab.gouv.fr','www.data.gouv.fr','data.gouv.fr']
  accepted=accepted or open_licence
  # Match the NoDerivatives token, not the letters "nd" inside "India".
  permission=None
  review=swiss_reviews.get((q,filename))
  if not accepted and review:
   params=dict(action='query',revids=review['revision'],prop='revisions',rvprop='ids|content',rvslots='main',format='json')
   revision_info=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'swiss-vrt-'+q)
   revision_page=next(iter(revision_info.get('query',{}).get('pages',{}).values()),{})
   permission=swiss_permission(q,filename,lic,meta.get('Credit',{}).get('value',''),revision_page)
  if not (accepted or permission) or re.search(r'(?<![a-z])nd(?![a-z])',lic,re.I):continue
  # Original GIFs remain GIFs; requesting raster thumbnails can fail or change format.
  original=args.original or filename.lower().endswith('.gif') or bool(review)
  url=((ii.get('url') if original else ii.get('thumburl') or ii.get('url')) or '').split('?')[0]
  if not url:continue
  extension=pathlib.PurePosixPath(urllib.parse.urlparse(url).path).suffix.lower()
  if extension not in ['.png','.jpg','.jpeg','.gif']:continue
  if extension=='.jpeg':extension='.jpg'
  relative='media/portrait-'+digest+extension;dest=h.OUT/relative
  if relative in media and dest.exists():return media[relative]
  if not dest.exists():
   raw=h.download(url,max_bytes=5_000_000)
   signatures={'.jpg':(b'\xff\xd8',),'.png':(b'\x89PNG\r\n\x1a\n',),'.gif':(b'GIF87a',b'GIF89a')}
   if len(raw)>5_000_000 or not raw.startswith(signatures[extension]):continue
   dest.write_bytes(raw)
  clean=lambda value:html.unescape(re.sub('<[^>]*>','',value))
  result=dict(file=relative,title=filename,url=ii.get('descriptionurl',''),artist=clean(meta.get('Artist',{}).get('value','')),license=lic,licenseUrl=meta.get('LicenseUrl',{}).get('value','') or ii.get('descriptionurl','')+'#Licensing',attribution=clean(meta.get('Attribution',{}).get('value','')),attributionRequired=lic=='Attribution' or open_licence or meta.get('AttributionRequired',{}).get('value')=='true',credit=clean(meta.get('Credit',{}).get('value','')),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,sourceUrl=url)
  if q in reviewed_records:result.update(reviewedSource=reviewed_records[q]['source'],photoDate=reviewed_records[q].get('photoDate',''))
  if open_licence and not result['attribution']:result['attribution']=' · '.join(filter(None,[result['artist'],result['credit'],'Licence Ouverte']))
  if permission:result['permission']=permission
  return result
 return None
for offset in range(0,len(targets),25):
 for q,result in h.parallel(acquire,targets[offset:offset+25]):
  if result:portraits[q]=result
  else:missing.append(q)
 print('Portrait review',min(offset+25,len(targets)),'/',len(targets),'accepted',len(portraits),flush=True)
data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'))
available={**existing,**portraits}
reused=0
for c in selected_countries(data):
 for leader in c['leaders']:
  if leader.get('portrait') and (leader['person'],leader['portrait']['title']) in excluded:leader.pop('portrait')
  if args.replace_reviewed and leader['person'] in portraits:leader['portrait']=portraits[leader['person']]
  elif not leader.get('portrait') and leader['person'] in available:
   leader['portrait']=available[leader['person']]
   if leader['person'] in existing:reused+=1
manifest=json.loads((h.OUT/'media/manifest.json').read_text(encoding='utf8'))
media={m['file']:m for m in manifest['entries']};media.update({m['file']:m for m in portraits.values()})
h.save(h.OUT/'data/identities.json',data);manifest['entries']=sorted(media.values(),key=lambda m:m['file']);h.save(h.OUT/'media/manifest.json',manifest)
h.save(h.CACHE/('portraits-'+args.start[:4]+'-curation-audit.json'),dict(retrieved=h.TODAY,reviewed=len(targets),added=len(portraits),reusedTerms=reused,missing=missing))
print('Portraits added',len(portraits),'reused terms',reused,'remaining',len(missing),flush=True)
