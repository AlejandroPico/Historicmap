"""Frozen thirteenth-century office and noble-title evidence; review required."""
import pathlib,importlib.util,json,urllib.parse,urllib.request,hashlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-018-german-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r);h=r.h
EXTRA_GROUPS={'PAPAL-STATES': ('Papa · soberano temporal', ['Pope Innocent III', 'Pope Honorius III', 'Pope Gregory IX', 'Pope Celestine IV', 'Pope Innocent IV', 'Pope Alexander IV', 'Pope Urban IV', 'Pope Clement IV', 'Pope Gregory X', 'Pope Innocent V', 'Pope Adrian V', 'Pope John XXI', 'Pope Nicholas III', 'Pope Martin IV', 'Pope Honorius IV', 'Pope Nicholas IV', 'Pope Celestine V', 'Pope Boniface VIII']), 'DNK': ('Rey de Dinamarca', ['Canute VI of Denmark', 'Valdemar II of Denmark', 'Eric IV of Denmark', 'Abel, King of Denmark', 'Christopher I of Denmark', 'Eric V of Denmark', 'Eric VI of Denmark']), 'NORWAY-KINGDOM': ('Rey de Noruega', ['Sverre of Norway', 'Haakon III of Norway', 'Guttorm of Norway', 'Inge II of Norway', 'Haakon IV of Norway', 'Magnus VI of Norway', 'Eric II of Norway', 'Haakon V of Norway']), 'SWE': ('Rey de Suecia', ['Sverker II of Sweden', 'Eric X of Sweden', 'John I of Sweden', 'Eric XI of Sweden', 'Valdemar, King of Sweden', 'Magnus III of Sweden', 'Birger of Sweden']), 'HESSE-UNITED': ('Landgrave de Hesse', ['Henry I, Landgrave of Hesse']), 'SAXONY-DUCHY': ('Duque de Sajonia', ['Bernhard, Count of Anhalt', 'Albert I, Duke of Saxony', 'Albert II, Duke of Saxony']), 'SAXONY-ELECTORATE': ('Duque de Sajonia-Wittenberg', ['Albert II, Duke of Saxony']), 'ELECTORATE-BRANDENBURG': ('Margrave de Brandeburgo', ['Otto II, Margrave of Brandenburg', 'Albert II, Margrave of Brandenburg', 'John I, Margrave of Brandenburg', 'Otto III, Margrave of Brandenburg', 'Otto IV, Margrave of Brandenburg-Stendal']), 'BAVARIA-DUCHY': ('Duque de Baviera · ramas territoriales', ['Louis I, Duke of Bavaria', 'Otto II, Duke of Bavaria', 'Louis II, Duke of Bavaria', 'Henry XIII, Duke of Bavaria']), 'BOHEMIA': ('Rey de Bohemia', ['Ottokar I of Bohemia', 'Wenceslaus I of Bohemia', 'Ottokar II of Bohemia', 'Wenceslaus II of Bohemia']), 'SICILY-KINGDOM': ('Rey de Sicilia', ['Frederick II, Holy Roman Emperor', 'Conrad IV of Germany', 'Conradin', 'Manfred, King of Sicily', 'Charles I of Anjou', 'Peter III of Aragon', 'James II of Aragon', 'Frederick III of Sicily']), 'NAPLES-KINGDOM': ('Rey de Nápoles', ['Charles I of Anjou', 'Charles II of Naples']), 'CHAGATAI': ('Khan de Chagatai', ['Chagatai Khan', 'Qara Hülëgü', 'Yesü Möngke', 'Mubarak Shah (Chagatai Khanate)', 'Ghiyas-ud-din Baraq', 'Duwa']), 'CHAGATAI-REGENTS': ('Regencia del kanato de Chagatai', ['Orghana']), 'ABBASID': ('Califa abasí en Bagdad', ['Al-Nasir', 'Al-Zahir bi-Amr Allah', 'Al-Mustansir (Abbasid caliph of Baghdad)', "Al-Musta'sim"]), 'EPIRUS': ('Soberano de Epiro', ['Michael I Komnenos Doukas', 'Theodore Komnenos Doukas', 'Michael II Komnenos Doukas', 'Nikephoros I Komnenos Doukas', 'Thomas I Komnenos Doukas']), 'KHMER-EXTRA': ('Autoridad regional jemer', []), 'JPN': ('Shikken Hōjō · regente de Kamakura', ['Hōjō Tokimasa', 'Hōjō Yoshitoki', 'Hōjō Yasutoki', 'Hōjō Tsunetoki', 'Hōjō Tokiyori', 'Hōjō Nagatoki', 'Hōjō Masamura', 'Hōjō Tokimune', 'Hōjō Sadatoki']), 'GORYEO-MILITARY': ('Dirigente militar de Goryeo', ['Choe Chung-heon', 'Choe U', 'Choe Hang (military official)', 'Choe Ui', 'Im Yeon', 'Im Yumu'])}
EXTRA=[(k,role,t)for k,(role,titles)in EXTRA_GROUPS.items() for t in titles]
EXTRA+=[('LATIN-EMPIRE', 'Emperador latino de Constantinopla', 'Peter II of Courtenay'), ('SWE', 'Rey de Suecia', 'Birger, King of Sweden'), ('DELHI-MAMLUK', 'Sultán de Delhi', 'Mahmud I of Delhi'), ('ABBASID', 'Califa abasí en Bagdad', 'Al-Mustansir I'), ('TREBIZOND', 'Emperador de Trebisonda', 'George, Emperor of Trebizond'), ('HIST-Q184536', 'Mansa de Mali', 'Uli I of Mali'), ('CHAGATAI', 'Khan de Chagatai', 'Mubarak Shah, Chagatai Khan'), ('ALMOHAD', 'Califa almohade', 'Abu al-Hasan as-Said al-Mutadid'), ('ALMOHAD', 'Califa almohade', 'Abu Hafs Umar al-Murtada'), ('MONGOL-EMPIRE', 'Regente del Imperio mongol', 'Tolui'), ('HIST-Q12548', 'Rey de Romanos · pretensión rival', 'Philip of Swabia'), ('HIST-Q12548', 'Rey de Romanos', 'Henry (VII) of Germany'), ('ENGLAND', 'Regente de Inglaterra', 'William Marshal, 1st Earl of Pembroke'), ('SCOTLAND', 'Guardián de Escocia', 'William Wallace')]
EXTRA+=[('MAMLUKS', 'Sultán de Egipto', 'Al-Adil Kitbugha'), ('GORYEO', 'Rey rival de Goryeo', 'Yeongjong of Goryeo'), ('SAXONY-DUCHY', 'Duque de Sajonia', 'John I, Duke of Saxony'), ('BOSNIA-BANATE', 'Ban de Bosnia', 'Kulin'), ('BOSNIA-BANATE', 'Ban de Bosnia', 'Stephen, Ban of Bosnia'), ('BOSNIA-BANATE', 'Ban de Bosnia', 'Matej Ninoslav')]
base=json.loads((ROOT/'.cache/rulers024-candidates.json').read_text(encoding='utf8'));rows={v['title']:v for v in base['records']}
# Retry metadata, not the HTML requests which received service back pressure.
spec=importlib.util.spec_from_file_location('g',ROOT/'scripts/review-024-rulers.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
missing=[(k,role,t) for k,role,ts in g.r.GROUPS for t in ts if t in {e['title'] for e in base['errors']}]
for k,role,t in EXTRA+missing:rows.setdefault(t,dict(key=k,role=role,title=t,requestedTitle=t,source='https://en.wikipedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_')),fields=[],parsed=[]))
titles=list(rows)
for off in range(0,len(titles),20):
 ts=titles[off:off+20];p=dict(action='wbgetentities',sites='enwiki',titles='|'.join(ts),props='labels|claims|sitelinks',redirects='yes',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'024-offices-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:18])
 for q,e in d.get('entities',{}).items():
  if 'missing' in e:continue
  canonical=e.get('sitelinks',{}).get('enwiki',{}).get('title');h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}))
  for t in ts:
   if canonical==t or rows[t].get('person')==q:rows[t].update(person=q,name=h.label(e),human=any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)))
# enwiki title redirects are different from Wikidata item redirects. Resolve
# aliases explicitly so an easily found sovereign is not silently dropped.
unresolved=[t for t,row in rows.items() if not row.get('person')]
for offset in range(0,len(unresolved),40):
 ts=unresolved[offset:offset+40];params=dict(action='query',titles='|'.join(ts),redirects=1,prop='pageprops',ppprop='wikibase_item',format='json');url='https://en.wikipedia.org/w/api.php?'+urllib.parse.urlencode(params);path=ROOT/'.cache'/('redirect024-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:16]+'.json')
 try:
  if path.exists():redirects=json.loads(path.read_text(encoding='utf8'))
  else:
   with urllib.request.urlopen(urllib.request.Request(url,headers=h.UA),timeout=20) as response:redirects=json.load(response)
   h.save(path,redirects)
  query=redirects.get('query',{});aliases={v['from']:v['to'] for v in query.get('normalized',[])+query.get('redirects',[])};pages={p['title']:p.get('pageprops',{}).get('wikibase_item') for p in query.get('pages',{}).values()};resolved={}
  for title in ts:
   canonical=title
   for _ in range(8):
    if canonical not in aliases:break
    canonical=aliases[canonical]
   q=pages.get(canonical)
   if q:resolved[title]=(q,canonical)
  qs=sorted({v[0] for v in resolved.values()})
  if qs:
   p=dict(action='wbgetentities',ids='|'.join(qs),props='labels|claims|sitelinks',format='json');entities=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'024-redirect-persons-'+hashlib.sha256('|'.join(qs).encode()).hexdigest()[:16])['entities']
   for title,(q,canonical) in resolved.items():
    e=entities[q];h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}));rows[title].update(person=q,name=h.label(e),human=any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)),identityResolution=dict(requested=title,canonical=canonical,qid=q,source=url))
 except Exception as error:print('Alias metadata unavailable',str(error),flush=True)
out=[]
for row in rows.values():
 q=row.get('person');claims=[];fields=[]
 if q and row.get('human'):
  e=h.entity(q)
  for prop in ['P39','P97']:
   for c in e.get('claims',{}).get(prop,[]):
    a=h.qual(c,'P580');b=h.qual(c,'P582');office=c.get('mainsnak',{}).get('datavalue',{}).get('value',{}).get('id')
    if c.get('rank')!='deprecated' and a and b and a[0]<'1300' and b[0]>='1200':claims.append(dict(property=prop,office=office,start=a[0],end=b[0],precision=min(a[1],b[1]),statement=c.get('id')))
 p=ROOT/'.cache'/('ruler018-'+hashlib.sha256(row['requestedTitle'].encode()).hexdigest()[:16]+'.html')
 if p.exists():
  raw=p.read_text(encoding='utf8');box=re.search(r'<table\b[^>]*class="[^"]*infobox[^>]*>(.*?)</table>',raw,re.S);fields=[r.clean(t) for t in re.findall(r'<tr\b[^>]*>(.*?)</tr>',box.group(1) if box else '',re.S)]
 out.append(dict(candidate=row,claims=claims,fields=fields))
offices=sorted({v['office'] for row in out for v in row['claims'] if v.get('office')});labels={}
for off in range(0,len(offices),40):
 qs=offices[off:off+40];p=dict(action='wbgetentities',ids='|'.join(qs),props='labels',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'024-office-labels-'+hashlib.sha256('|'.join(qs).encode()).hexdigest()[:16]);labels.update({q:h.label(e) for q,e in d.get('entities',{}).items() if 'missing' not in e})
for row in out:
 for c in row['claims']:c['label']=labels.get(c['office'],'')
h.save(ROOT/'.cache/rulers024-office-evidence.json',out)
for row in out:
 v=row['candidate'];print(v['key'],v.get('person'),v.get('human'),v.get('name',v['title']),row['claims'] if not v['parsed'] else [],flush=True)
