"""Frozen P39 and full infobox evidence; never automatically assign all offices."""
import pathlib,importlib.util,json,urllib.parse,hashlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-018-german-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r);h=r.h
EXTRA=[
 ('PAPAL-STATES','Papa · soberano temporal',t) for t in ['Pope Boniface IX','Pope Innocent VII','Pope Gregory XII','Pope Martin V','Pope Eugene IV','Pope Nicholas V','Pope Callixtus III','Pope Pius II','Pope Paul II','Pope Sixtus IV','Pope Innocent VIII','Pope Alexander VI']]
EXTRA += [('OTT','Pretendiente otomano · interregno',t) for t in ['Süleyman Çelebi','Musa Çelebi','İsa Çelebi']]
EXTRA += [('MUSCOVY','Gran príncipe · sucesión disputada',t) for t in ['Yury of Zvenigorod','Vasily Kosoy','Dmitry Shemyaka']]
base=json.loads((ROOT/'.cache/rulers022-candidates.json').read_text(encoding='utf8'));rows={v['title']:v for v in base['records']}
# Retry metadata, not the HTML requests which received service back pressure.
spec=importlib.util.spec_from_file_location('g',ROOT/'scripts/review-022-rulers.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
missing=[(k,role,t) for k,role,ts in g.r.GROUPS for t in ts if t in {e['title'] for e in base['errors']}]
for k,role,t in EXTRA+missing:rows.setdefault(t,dict(key=k,role=role,title=t,requestedTitle=t,source='https://en.wikipedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_')),fields=[],parsed=[]))
titles=list(rows)
for off in range(0,len(titles),20):
 ts=titles[off:off+20];p=dict(action='wbgetentities',sites='enwiki',titles='|'.join(ts),props='labels|claims|sitelinks',redirects='yes',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'022-offices-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:18])
 for q,e in d.get('entities',{}).items():
  if 'missing' in e:continue
  canonical=e.get('sitelinks',{}).get('enwiki',{}).get('title');h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}))
  for t in ts:
   if canonical==t or rows[t].get('person')==q:rows[t].update(person=q,name=h.label(e),human=any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)))
out=[]
for row in rows.values():
 q=row.get('person');claims=[];fields=[]
 if q and row.get('human'):
  e=h.entity(q)
  for prop in ['P39','P97']:
   for c in e.get('claims',{}).get(prop,[]):
    a=h.qual(c,'P580');b=h.qual(c,'P582');office=c.get('mainsnak',{}).get('datavalue',{}).get('value',{}).get('id')
    if c.get('rank')!='deprecated' and a and b and a[0]<'1500' and b[0]>='1400':claims.append(dict(property=prop,office=office,start=a[0],end=b[0],precision=min(a[1],b[1]),statement=c.get('id')))
 p=ROOT/'.cache'/('ruler018-'+hashlib.sha256(row['requestedTitle'].encode()).hexdigest()[:16]+'.html')
 if p.exists():
  raw=p.read_text(encoding='utf8');box=re.search(r'<table\b[^>]*class="[^"]*infobox[^>]*>(.*?)</table>',raw,re.S);fields=[r.clean(t) for t in re.findall(r'<tr\b[^>]*>(.*?)</tr>',box.group(1) if box else '',re.S)]
 out.append(dict(candidate=row,claims=claims,fields=fields))
offices=sorted({v['office'] for row in out for v in row['claims'] if v.get('office')});labels={}
for off in range(0,len(offices),40):
 qs=offices[off:off+40];p=dict(action='wbgetentities',ids='|'.join(qs),props='labels',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'022-office-labels-'+hashlib.sha256('|'.join(qs).encode()).hexdigest()[:16]);labels.update({q:h.label(e) for q,e in d.get('entities',{}).items() if 'missing' not in e})
for row in out:
 for c in row['claims']:c['label']=labels.get(c['office'],'')
h.save(ROOT/'.cache/rulers022-office-evidence.json',out)
for row in out:
 v=row['candidate'];print(v['key'],v.get('person'),v.get('human'),v.get('name',v['title']),row['claims'] if not v['parsed'] else [],flush=True)
