"""Acquire reviewed original symbols and dated Victoria portraits; preserve bytes.

Reads Commons metadata and description revisions, rejects fictitious/disputed
designs and unsafe SVG. No generated artwork or no-derivatives crops.
"""
import pathlib,json,importlib.util,urllib.parse,hashlib,html,re,copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
TAG='curated-symbols-1840-0.15'
ROWS=[('AUSTRIAN-EMPIRE','Flag of the Habsburg Monarchy.svg',1840,1859),('PRUSSIA','Flag of the Kingdom of Prussia (1803-1892).svg',1840,1859),('SAR','Flag of the Kingdom of Sardinia (1848-1851).svg',1848,1850),('TWO-SICILIES','Flag of the Kingdom of the Two Sicilies (1816).svg',1840,1859),('PAPAL-STATES','Flag of the Papal States (1825-1870).svg',1840,1859),('TEXAS','Flag of Texas.svg',1840,1845),('HTI','Flag of Haiti (1849–1859).svg',1849,1858)]
REUSE=[('BRA-EMPIRE','Flag of Brazil (1822–1853).svg',1840,1852),('BRA-EMPIRE','Flag of Brazil (1853-1889).svg',1853,1859),('PRT','Flag of Portugal (1830–1910).svg',1840,1859),('OTT','Flag of the Ottoman Empire (1844–1922).svg',1844,1859),('HAW-KINGDOM','Flag of Hawaii.svg',1845,1859)]
PORTRAITS=[('Queen Victoria (1838) by Thomas Sully.jpg',1840,1853,'1838','Retrato pintado en1838'),('Queen Victoria in court dress 1854.jpg',1854,1859,'1854-05-11','Fotografía del11/5/1854')]
def main():
 data=json.loads((ROOT/'public/data/identities.json').read_text(encoding='utf8'));manifest=json.loads((ROOT/'public/media/manifest.json').read_text(encoding='utf8'));media={m['file']:m for m in manifest['entries']};by_title={m['title']:m for m in media.values()}
 titles=[r[1] for r in ROWS]+[r[0] for r in PORTRAITS]
 params=dict(action='query',titles='|'.join('File:'+t for t in titles),redirects=1,prop='imageinfo|revisions',rvprop='content',rvslots='main',iiprop='url|extmetadata',iiurlwidth=400,format='json')
 info=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'media1840-reviewed-'+hashlib.sha256('|'.join(titles).encode()).hexdigest()[:12]);pages={p['title'][5:]:p for p in info.get('query',{}).get('pages',{}).values()}
 def acquire(title):
  page=pages.get(title,{});ii=page.get('imageinfo',[{}])[0];m=ii.get('extmetadata',{});lic=m.get('LicenseShortName',{}).get('value','');wiki=page.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')
  if not ii.get('url') or not wiki or re.search(r'\{\{\s*(Fictitious|Fictional|Fact disputed|Disputed|Inaccurate)\b',wiki,re.I):raise ValueError('Unverified or disputed design: '+title)
  if not any(x in lic.lower() for x in ['public domain','cc0','cc by','cc-by']) and not (title=='Flag of the Kingdom of Prussia (1803-1892).svg' and lic=='Attribution'):raise ValueError('Unverified license: '+title)
  if title in by_title:return by_title[title]
  url=(ii['url'] if title.endswith('.svg') else ii.get('thumburl') or ii['url']).split('?')[0];raw=h.download(url,max_bytes=5000000)
  ext='.svg' if title.endswith('.svg') else '.jpg' if raw.startswith(b'\xff\xd8') else '.png' if raw.startswith(b'\x89PNG') else None
  if not ext or len(raw)>5000000 or ext=='.svg' and (b'<svg' not in raw or re.search(rb'<script|javascript:|\bonload\s*=',raw,re.I)):raise ValueError('Invalid image bytes')
  file='media/'+('flag-' if ext=='.svg' else 'portrait-')+hashlib.sha256(title.encode()).hexdigest()[:20]+ext;(ROOT/'public'/file).write_bytes(raw)
  clean=lambda key:html.unescape(re.sub('<[^>]*>','',m.get(key,{}).get('value','')))
  result=dict(file=file,title=title,url=ii.get('descriptionurl',''),sourceUrl=url,artist=clean('Artist'),license=lic,licenseUrl=clean('LicenseUrl') or ii['descriptionurl']+'#Licensing',attribution=clean('Attribution'),attributionRequired=True,credit=clean('Credit'),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw));media[file]=result;by_title[title]=result;return result
 pending=[]
 for c in data['countries'].values():c['flags']=[f for f in c['flags'] if f.get('acquisition')!=TAG]
 for key,title,a,b in ROWS+REUSE:
  try:m=by_title[title] if (key,title,a,b) in REUSE else acquire(title)
  except Exception as e:pending.append(dict(key=key,title=title,reason=str(e)));continue
  # Bounded design references, not alleged legal dates of adoption.
  data['countries'][key]['flags'].append(dict(start=f'{a}-12-31' if a!=1840 else '1840-01-01',end=f'{b}-12-31',media=m,source=m['url'],acquisition=TAG,note='Familia gráfica histórica representativa con ventana anual conservadora; no acredita uniformidad de cada ejemplar o una norma digital de colores.'))
 series=json.loads((ROOT/'public/data/portrait-series.json').read_text(encoding='utf8'));series['records']=[r for r in series['records'] if r.get('acquisition')!=TAG]
 for title,a,b,date,label in PORTRAITS:
  try:m=acquire(title)
  except Exception as e:pending.append(dict(person='Q9439',title=title,reason=str(e)));continue
  series['records'].append(dict(person='Q9439',start=a,end=b,photoDate=date,dateLabel=label,media=m,source=m['url'],note='Imagen de la etapa correspondiente; el retrato pintado no se presenta como fotografía.',acquisition=TAG))
 h.save(ROOT/'public/data/identities.json',data);manifest['entries']=sorted(media.values(),key=lambda m:m['file']);h.save(ROOT/'public/media/manifest.json',manifest);h.save(ROOT/'public/data/portrait-series.json',series);h.save(ROOT/'.cache/media1840-audit.json',dict(pending=pending,windows=sum(f.get('acquisition')==TAG for c in data['countries'].values() for f in c['flags'])))
 print('Symbols and dated portraits integrated; pending',pending,flush=True)
if __name__=='__main__':main()
