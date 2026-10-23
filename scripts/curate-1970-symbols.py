"""Curate bounded 1970s/1980s flag designs from licensed, unchanged Commons SVGs.

Fetches source metadata explicitly; a missing filename or unlicensed/fictitious
design is rejected. Preserves the existing authority/reference horizon and every
unrelated record. Run after the generic flag importer, never before it.
"""
from pathlib import Path
import hashlib, html, json, re, time, urllib.parse, urllib.request

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public'
CACHE=ROOT/'.cache/identities'
TAG='curated-symbols-0.8'
UA={'User-Agent':'Historicmap/0.8 (https://github.com/AlejandroPico/Historicmap)'}
CHRONOLOGY='https://commons.wikimedia.org/wiki/Data:FlagsData.tab'
TERMS=[
 ('BGR','Flag of Bulgaria (1967–1971).svg','1967-06-14','1971-05-20',
  'Emblema de la República Popular. La galería de Commons sitúa este diseño desde junio de 1967; la descripción del archivo también menciona 1968. El contraste focal acredita el diseño de 1970, no resuelve esa discrepancia anterior.'),
 ('BGR','Flag of Bulgaria (1971–1990).svg','1971-05-21','1990-11-21',
  'Emblema con las fechas 681 y 1944. Fin limitado por el intervalo contemporáneo previamente documentado; no se presenta el tricolor sin emblema como bandera de 1970.'),
 ('LAO','Flag of Laos (1952–1975).svg','1952-01-01','1975-12-01',
  'Bandera del Reino de Laos con elefantes. Inicio de año como límite de la familia representada, no afirmación de día exacto de adopción.'),
 ('IRN','State flag of Iran 1964-1979 (alternate).svg','1964-01-01','1979-12-31',
  'Variante histórica del león y sol conservada en Commons desde 2011, sin aplicar la estandarización digital de 2026. El periodo usa resolución anual; la continuidad del símbolo durante la transición de 1979 no acredita continuidad de la monarquía durante todo ese año.'),
 ('AFG','Flag of Afghanistan (1973–1974).svg','1973-07-17','1974-05-08',
  'Primer diseño republicano posterior a la monarquía.'),
 ('AFG','Flag of Afghanistan (1974–1978).svg','1974-05-09','1978-04-26',
  'Diseño de la República de Afganistán anterior a la Revolución de Saur.'),
 ('AFG','Flag of Afghanistan (1978).svg','1978-04-27','1978-10-18',
  'Diseño transitorio de 1978, distinto del posterior campo rojo con emblema Khalq.'),
 ('AFG','Flag of Afghanistan (1978–1980).svg','1978-10-19','1980-04-21',
  'Campo rojo con emblema e inscripción Khalq; no se prolonga al nuevo diseño de 1980.'),
 ('AFG','Flag of Afghanistan (1980–1987).svg','1980-04-22','1987-11-29',
  'Tricolor con emblema de la República Democrática; imagen de origen enlazada a la Biblioteca Digital Mundial por su autor.'),
 ('MNG',"Flag of the Mongolian People's Republic (1945–1992).svg",'1945-01-01','1991-12-31',
  'Soyombo con estrella del periodo de la República Popular. Límite anual del inventario; 1992 emplea el diseño siguiente. El archivo genérico Flag of Mongolia (1945–1992).svg no existía; se utiliza el título real acreditado.'),
 ('MMR','Flag of Burma (1948–1974).svg','1948-01-04','1974-01-02',
  'Diseño de la Unión de Birmania anterior a la bandera socialista de 1974.'),
]

def save(path,data):
 path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')

def clean(value):return html.unescape(re.sub('<[^>]*>','',value)).strip()

def cached_pages():
 pages={}
 for name in ['symbols-1970-review.json','symbols-1970-review-extra.json','symbols-1970-iran-review.json']:
  path=CACHE/name
  if path.exists():
   for p in json.loads(path.read_text(encoding='utf8')).get('query',{}).get('pages',{}).values():
    if p.get('imageinfo'):pages[p['title']]=p
 return pages

def acquire(filename,pages):
 title='File:'+filename
 page=pages.get(title)
 digest=hashlib.sha256(filename.encode()).hexdigest()[:20]
 metadata_path=CACHE/('symbols-curated-'+digest+'.json')
 if not page and metadata_path.exists():page=json.loads(metadata_path.read_text(encoding='utf8'))
 if not page:
  params=dict(action='query',titles=title,redirects=1,prop='imageinfo|revisions',iiprop='url|extmetadata',rvprop='content',rvslots='main',format='json')
  with urllib.request.urlopen(urllib.request.Request('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),headers=UA),timeout=40) as response:
   result=json.load(response)
  page=next(iter(result.get('query',{}).get('pages',{}).values()),{})
 if not page.get('imageinfo'):raise ValueError('Missing source image: '+filename)
 wiki=page.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')
 if re.search(r'\{\{\s*Fictitious flag',wiki,re.I):raise ValueError('Fictitious/modern proposed design rejected: '+filename)
 ii=page['imageinfo'][0];meta=ii.get('extmetadata',{})
 license=clean(meta.get('LicenseShortName',{}).get('value',''))
 if not any(v in license.lower() for v in ['public domain','cc0','cc by-sa','cc-by-sa','cc by','cc-by']):raise ValueError('Unverified license: '+filename+' '+license)
 url=ii.get('url','').split('?')[0]
 if not url.startswith('https://upload.wikimedia.org/') or not url.endswith('.svg'):raise ValueError('Unexpected source URL')
 dest=OUT/'media'/('flag-'+digest+'.svg')
 if not dest.exists():
  with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=40) as response:raw=response.read()
  if b'<svg' not in raw or re.search(rb'<script|javascript:|\bonload\s*=',raw,re.I):raise ValueError('Unsafe SVG: '+filename)
  dest.write_bytes(raw);time.sleep(1.2)
 raw=dest.read_bytes()
 save(metadata_path,page)
 m=dict(file='media/'+dest.name,title=page['title'].removeprefix('File:'),url=ii['descriptionurl'],
        artist=clean(meta.get('Artist',{}).get('value','')),
        license=license,licenseUrl=meta.get('LicenseUrl',{}).get('value',''),
        attribution=clean(meta.get('Attribution',{}).get('value','')),
        attributionRequired=meta.get('AttributionRequired',{}).get('value')=='true',
        credit=clean(meta.get('Credit',{}).get('value','')),
        sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),sourceUrl=url)
 return m

def main():
 CACHE.mkdir(parents=True,exist_ok=True)
 pages=cached_pages();acquired=[(key,start,end,note,acquire(filename,pages)) for key,filename,start,end,note in TERMS]
 path=OUT/'data/identities.json';data=json.loads(path.read_text(encoding='utf8'))
 manifest_path=OUT/'media/manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf8'));media={m['file']:m for m in manifest['entries']}
 before=len(media)
 for country in data['countries'].values():country['flags']=[f for f in country['flags'] if f.get('acquisition')!=TAG]
 for key,start,end,note,m in acquired:
  media[m['file']]=m
  data['countries'][key]['flags'].append(dict(start=start,end=end,source=m['url'],media=m,acquisition=TAG,intervalSource=CHRONOLOGY,note=note))
 # Generic design-family inception dates must not claim continuous national use.
 for f in data['countries']['BGR']['flags']:
  if f['media']['title']=='Flag of Bulgaria (digital).svg' and f['start']<'1947':
   f['end']='1947-12-06';f['note']='No se prolonga el tricolor sin emblema durante los diseños de la República Popular.'
 for f in data['countries']['LAO']['flags']:
  if f['media']['title']=='Flag of Laos.svg':
   f['start']='1975-12-02';f['note']='Readopción como bandera nacional de la República Democrática Popular. La existencia del diseño en 1945 no prueba uso nacional continuo hasta 1975.'
 # This upload describes an early republican design photographed in 1980, not
 # the imperial flag used in 1970 or a design dated to 1 January 1979.
 flags=data['countries']['IRN']['flags']
 flags[:]=[f for f in flags if not (f['media']['title']=='State flag of Iran (1964–1980).svg' and f['start']==f['end'] and f['start']>='2026')]
 for f in flags:
  if f['media']['title']=='First Flag of I.R.Iran.svg':
   f['start']='1980-01-01';f['end']='1980-07-28';f['note']='Ventana de 1980: la descripción del autor y la fotografía de Banisadr acreditan ese año; el 1 de enero es un límite de resolución anual, no un día de adopción certificado.'
 for f in data['countries']['AFG']['flags']:
  if f['media']['title']=='Flag of Afghanistan (1931–1973).svg':f['end']='1973-07-16'
  if f['media']['title']=='Flag of Afghanistan (1987–1992).svg':f['start']='1987-11-30'
 for f in data['countries']['MMR']['flags']:
  if f['media']['title']=='Flag of Myanmar (1974–2010).svg':f['start']='1974-01-03'
 removed=0
 # A design family must not outlive the historical state it identifies. The
 # generic importer retained some annual file ranges after these states ended.
 for key,start,end in [('VDR','1945-09-02','1976-07-01'),('RVN','1955-10-26','1975-04-30'),('VSR','1969-06-08','1976-07-01')]:
  unique={}
  for flag in data['countries'][key]['flags']:
   flag['start']=max(flag['start'],start);flag['end']=min(flag['end'],end)
   if flag['start']<=flag['end']:unique[(flag['start'],flag['end'],flag['media']['file'])]=flag
  data['countries'][key]['flags']=list(unique.values())
 for country in data['countries'].values():
  for leader in country['leaders']:
   if leader['person']=='Q1811651':
    if leader.pop('portrait',None):removed+=1
    note='Retrato pendiente de identificación: la imagen adquirida presenta una atribución ambigua y se omite hasta contrastarla. No se concluye que represente a otra persona.'
    if note not in leader.get('note',''):leader['note']=(leader.get('note','')+' '+note).strip()
  country['flags'].sort(key=lambda f:(f['start'],f['end'],f['media']['title']))
 # This newly acquired image has no confirmed identification and is not part
 # of the earlier release. Remove it only after every identity reference is gone.
 ambiguous='media/portrait-389f4f3e50740758c03a.jpg'
 if ambiguous not in json.dumps(data):
  media.pop(ambiguous,None)
  target=OUT/ambiguous
  if target.exists():target.unlink()
 save(path,data);manifest['entries']=sorted(media.values(),key=lambda m:m['file']);save(manifest_path,manifest)
 print(f'{len(acquired)} sourced flag intervals; {len(media)-before} new media; {removed} ambiguous portrait references removed; {len(media)} media total.',flush=True)

if __name__=='__main__':main()
