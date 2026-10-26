"""Read named rulers' reign fields and canonical article identities for review.

Dates come only from Reign fields, never birth/death. Ambiguous/missing fields
remain rejected candidates. Public integration is a separate explicit step.
"""
import pathlib,importlib.util,urllib.request,urllib.parse,re,html,datetime,json,hashlib,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
GROUPS=[
 ('HIST-Q14551680','Príncipe de Lippe',['Leopold I, Prince of Lippe','Leopold II, Prince of Lippe','Leopold III, Prince of Lippe','Woldemar, Prince of Lippe','Alexander, Prince of Lippe']),
 ('HIST-Q836680','Duque de Nassau',['Frederick Augustus, Duke of Nassau','William, Duke of Nassau','Adolphe, Grand Duke of Luxembourg']),
 ('HIST-Q20135','Gran duque de Hesse',['Louis I, Grand Duke of Hesse','Louis II, Grand Duke of Hesse','Louis III, Grand Duke of Hesse','Louis IV, Grand Duke of Hesse','Ernest Louis, Grand Duke of Hesse']),
 ('HIST-Q186320','Gran duque de Baden',['Charles Frederick, Grand Duke of Baden','Charles, Grand Duke of Baden','Louis I, Grand Duke of Baden','Leopold, Grand Duke of Baden','Louis II, Grand Duke of Baden','Frederick I, Grand Duke of Baden']),
 ('HIST-Q3462133','Duque de Sajonia-Coburgo-Gotha',['Ernest I, Duke of Saxe-Coburg and Gotha','Ernest II, Duke of Saxe-Coburg and Gotha','Alfred, Duke of Saxe-Coburg and Gotha']),
 ('HIST-Q159631','Rey de Wurtemberg',['Frederick I of Württemberg','William I of Württemberg','Charles I of Württemberg','William II of Württemberg']),
 ('HIST-Q153015','Rey de Sajonia',['Frederick Augustus I of Saxony','Anthony of Saxony','Frederick Augustus II of Saxony','John, King of Saxony','Albert, King of Saxony']),
 ('HIST-Q155570','Gran duque de Sajonia-Weimar-Eisenach',['Charles Augustus, Grand Duke of Saxe-Weimar-Eisenach','Charles Frederick, Grand Duke of Saxe-Weimar-Eisenach','Charles Alexander, Grand Duke of Saxe-Weimar-Eisenach'])]
def clean(text):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',text))).strip()
def date(text,end=False):
 text=re.sub(r'\[[^]]*\]|\([^)]*\)','',text).strip().replace('\xa0',' ')
 text=re.sub(r'^(?:c\.?|circa)\s*','',text)
 for fmt,p in [('%d %B %Y',11),('%B %d, %Y',11),('%B %Y',10),('%Y',9)]:
  try:
   d=datetime.datetime.strptime(text,fmt).date()
   if p==9 and end:d=d.replace(month=12,day=31)
   return d.isoformat(),p
  except ValueError:pass
 raise ValueError('Unparsed reign date: '+text)
def fetch(row):
 key,role,title=row;url='https://en.wikipedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_'),safe=',()_');p=ROOT/'.cache'/('ruler018-'+hashlib.sha256(title.encode()).hexdigest()[:16]+'.html')
 if not p.exists():
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Historicmap/0.18 educational atlas research'}),timeout=40) as r:p.write_bytes(r.read())
 raw=p.read_text(encoding='utf8');canonical=clean(re.search(r'<title>(.*?)</title>',raw,re.S).group(1)).removesuffix(' - Wikipedia')
 # An infobox can contain separate offices. Preserve every Reign field for review.
 infobox=re.search(r'<table\b[^>]*class="[^"]*infobox[^>]*>(.*?)</table>',raw,re.S)
 fields=[]
 for fragment in re.findall(r'<tr\b[^>]*>(.*?)</tr>',infobox.group(1) if infobox else '',re.S):
  if not re.search(r'<th[^>]*>\s*Reign\s*</th>',fragment,re.I):continue
  td=re.search(r'<td[^>]*>(.*?)</td>',fragment,re.S)
  if td:fields.append(clean(td.group(1)))
 parsed=[]
 for field in fields:
  parts=re.split(r'\s*[–—]\s*',field,maxsplit=1)
  if len(parts)!=2:continue
  try:a,pa=date(parts[0]);b,pb=date(parts[1],True);parsed.append(dict(start=a,end=b,precision=min(pa,pb),raw=field))
  except ValueError:continue
 return dict(key=key,role=role,requestedTitle=title,title=canonical,source=url,fields=fields,parsed=parsed)
def main():
 rows=[(key,role,t) for key,role,titles in GROUPS for t in titles];out=[];errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for row,result in zip(rows,pool.map(lambda row:safe(row),rows)):
   if isinstance(result,dict):out.append(result)
   else:errors.append(dict(key=row[0],title=row[2],error=result))
 for offset in range(0,len(out),20):
  group=out[offset:offset+20];params=dict(action='wbgetentities',sites='enwiki',titles='|'.join(r['title'] for r in group),props='labels|claims|sitelinks',format='json')
  d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'ruler018-identities-'+hashlib.sha256('|'.join(r['title'] for r in group).encode()).hexdigest()[:18])
  for q,e in d.get('entities',{}).items():
   if 'missing' in e:continue
   title=e.get('sitelinks',{}).get('enwiki',{}).get('title');h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}))
   for r in group:
    if r['title']==title:r.update(person=q,name=h.label(e),human=any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)))
 for r in out:
  if r['title']=='Louis II of Hesse':r.update(person='Q166701',name='Luis II de Hesse-Darmstadt',human=True,identityCorrection='Article item rejected; human identity checked independently')
 for r in out:print(r['key'],r.get('person'),r['title'],r['parsed'],flush=True)
 h.save(ROOT/'.cache/german018-rulers.json',dict(records=out,errors=errors));print('Candidate errors',errors,flush=True)
def safe(row):
 try:return fetch(row)
 except Exception as e:return str(e)
if __name__=='__main__':main()
