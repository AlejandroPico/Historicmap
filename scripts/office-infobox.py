"""Extract only explicit reigns/paired office dates from the outer infobox.

Nested personal-name infoboxes and bibliographic titles cannot replace the
office heading. Birth/death fields are never selected as office dates.
"""
import re,html,datetime
MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']
def parameters(text,pattern=r'\{\{\s*infobox\b'):
 m=re.search(pattern,text,re.I)
 if not m:return {}
 i=m.end();curly=1;square=0;start=i;parts=[]
 while i<len(text):
  pair=text[i:i+2]
  if pair=='{{':curly+=1;i+=2;continue
  if pair=='}}':
   curly-=1
   if not curly:parts.append(text[start:i]);break
   i+=2;continue
  if pair=='[[':square+=1;i+=2;continue
  if pair==']]':square=max(0,square-1);i+=2;continue
  if text[i]=='|'and curly==1 and square==0:parts.append(text[start:i]);start=i+1
  i+=1
 return {p.split('=',1)[0].strip():p.split('=',1)[1].strip()for p in parts if '='in p}
def clean(raw):
 raw=html.unescape(raw)
 raw=re.sub(r'<ref\b[^>]*>.*?</ref>|<ref\b[^>]*/>','',raw,flags=re.I|re.S)
 raw=re.sub(r'\{\{(?:efn|sfn|refn|harvnb)\b[^{}]*\}\}','',raw,flags=re.I|re.S)
 raw=re.sub(r'\[\[(?:[^]|]*\|)?([^]]*)\]\]',r'\1',raw)
 raw=re.sub(r'\{\{(?:snd|ndash|mdash)\}\}','–',raw)
 raw=re.sub(r'\{\{circa\|(\d{3,4})\|(\d{3,4})(?:\s*CE)?\}\}',r'\1–\2',raw,flags=re.I)
 raw=re.sub(r'\{\{circa\|([^{}]*)\}\}',r'\1',raw,flags=re.I);raw=re.sub(r'\{\{circa\}\}','c. ',raw,flags=re.I)
 raw=re.sub(r'\b(?:CE|AD)\b','',raw)
 raw=re.sub(r'\{\{(?:nowrap|nobr|small)\|([^{}]*)\}\}',r'\1',raw)
 def date_template(m):
  v=re.findall(r'\|\s*(\d+)\s*(?=\||\}\})',m.group(0))
  if not v:return m.group(0)
  return v[0].zfill(4)+(('-'+v[1].zfill(2))if len(v)>1 else'')+(('-'+v[2].zfill(2))if len(v)>2 else'')
 raw=re.sub(r'\{\{(?:start date|end date|date|dts)[^{}]*\}\}',date_template,raw,flags=re.I)
 raw=re.sub('<[^>]*>',' ',raw);raw=re.sub(r'(?<!\d)(\d{3})(?!\d)',r'0\1',raw)
 for month in MONTHS:raw=re.sub(r'\b'+month[:3]+r'\.?\b',month,raw)
 return re.sub(r'\s+',' ',raw).strip()
def parse_date(raw,end=False):
 text=clean(raw);text=re.sub(r'\([^)]*\)','',text).strip();text=re.sub(r'^(?:c\.?|circa|from)\s*','',text)
 for fmt,p in [('%Y-%m-%d',11),('%d %B %Y',11),('%B %d, %Y',11),('%B %Y',10),('%Y',9)]:
  try:
   d=datetime.datetime.strptime(text,fmt).date()
   if p==9 and end:d=d.replace(month=12,day=31)
   return d.isoformat(),p
  except ValueError:pass
 raise ValueError('Unresolved explicit office date '+text)
def extract(text,include_succession=False):
 p=parameters(text);out=[]
 for field,raw in p.items():
  m=re.fullmatch(r'(?:reign|tenure)(\d*)',field)
  if not m:continue
  suffix=m.group(1);office=p.get('succession'+suffix,p.get('title'+suffix,p.get('succession',p.get('title',''))))
  parts=re.split(r'<br\s*/?>',raw,flags=re.I)
  # A line break may separate the two ends of one reign, not two reigns.
  if len(parts)>1 and any(re.search(r'[–—-]\s*$',clean(v))for v in parts[:-1]):parts=[re.sub(r'<br\s*/?>',' ',raw,flags=re.I)]
  for part in parts:
   value=clean(part);pair=re.split(r'\s*[–—]\s*|\s+-\s+|(?<=\d{4})-(?=\d{4}(?!\d))',value,maxsplit=1);parsed=None
   if len(pair)==2:
    try:
     # Conventional abbreviated end years (953–77), not personal life dates.
     if re.fullmatch(r'\d{4}',pair[0])and re.fullmatch(r'\d{2}',pair[1]):pair[1]=pair[0][:2]+pair[1]
     a,pa=parse_date(pair[0]);b,pb=parse_date(pair[1],True)
     if a<=b:parsed=dict(start=a,end=b,precision=min(pa,pb))
    except ValueError:pass
   out.append(dict(field=field,office=clean(office),raw=part,parsed=parsed))
 for field,raw in p.items():
  m=re.fullmatch(r'term_start(\d*)',field)
  if not m:continue
  suffix=m.group(1);end=p.get('term_end'+suffix);office=p.get('office'+suffix,p.get('order'+suffix,''))
  if not end or not office:continue
  parsed=None
  try:
   a,pa=parse_date(raw);b,pb=parse_date(end,True)
   if a<=b:parsed=dict(start=a,end=b,precision=min(pa,pb))
  except ValueError:pass
  out.append(dict(field=field,office=clean(office),raw=raw+' – '+end,parsed=parsed))
 if include_succession:
  for match in re.finditer(r'\{\{\s*s-ttl\b',text,re.I):
   fields=parameters(text[match.start():],r'\{\{\s*s-ttl\b');office=fields.get('title','');years=fields.get('years','')
   if not office or not years:continue
   # Only explicit office succession templates; personal dates/citations never qualify.
   parsed=extract('{{Infobox royalty|succession='+office+'|reign='+years+'}}')
   for row in parsed:out.append({**row,'field':'succession-template'})
 return out
