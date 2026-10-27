"""Frozen twelfth-century office and noble-title evidence; review required."""
import pathlib,importlib.util,json,urllib.parse,urllib.request,hashlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-018-german-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r);h=r.h
EXTRA_GROUPS={'PAPAL-STATES': ('Papa · soberano temporal', ['Pope Paschal II', 'Pope Gelasius II', 'Pope Callixtus II', 'Pope Honorius II', 'Pope Innocent II', 'Pope Celestine II', 'Pope Lucius II', 'Pope Eugene III', 'Pope Anastasius IV', 'Pope Adrian IV', 'Pope Alexander III', 'Pope Lucius III', 'Pope Urban III', 'Pope Gregory VIII', 'Pope Clement III', 'Pope Celestine III', 'Pope Innocent III']), 'DNK': ('Rey de Dinamarca', ['Eric I of Denmark', 'Niels of Denmark', 'Eric II of Denmark', 'Eric III of Denmark', 'Sweyn III of Denmark', 'Canute V of Denmark', 'Valdemar I of Denmark', 'Canute VI of Denmark']), 'NORWAY-KINGDOM': ('Rey de Noruega', ['Magnus Barefoot', 'Sigurd the Crusader', 'Eystein I of Norway', 'Olaf Magnusson of Norway', 'Harald Gille', 'Magnus IV of Norway', 'Sigurd II of Norway', 'Inge I of Norway', 'Eystein II of Norway', 'Haakon II of Norway', 'Magnus V of Norway', 'Sverre of Norway']), 'SWE': ('Rey de Suecia', ['Inge the Elder', 'Philip of Sweden', 'Inge the Younger', 'Sverker I of Sweden', 'Eric IX of Sweden', 'Magnus II of Sweden', 'Charles VII of Sweden', 'Canute I of Sweden', 'Sverker II of Sweden']), 'BOHEMIA-DUCHY': ('Duque de Bohemia', ['Bretislav II', 'Bořivoj II', 'Svatopluk, Duke of Bohemia', 'Vladislaus I, Duke of Bohemia', 'Soběslav I', 'Vladislaus II, Duke of Bohemia', 'Frederick, Duke of Bohemia', 'Soběslav II', 'Conrad II, Duke of Bohemia', 'Wenceslaus II, Duke of Bohemia', 'Ottokar I of Bohemia', 'Henry Bretislaus', 'Vladislaus III, Duke of Bohemia']), 'BOHEMIA': ('Rey de Bohemia', ['Vladislaus II, Duke of Bohemia', 'Ottokar I of Bohemia']), 'SAXONY-STEM': ('Duque de Sajonia', ['Magnus, Duke of Saxony', 'Lothair III, Holy Roman Emperor', 'Henry the Proud', 'Albert the Bear', 'Henry the Lion']), 'SAXONY-DUCHY': ('Duque de Sajonia · dominios ascanios', ['Bernhard, Count of Anhalt']), 'BAVARIA-DUCHY': ('Duque de Baviera', ['Welf I, Duke of Bavaria', 'Welf II, Duke of Bavaria', 'Henry IX, Duke of Bavaria', 'Henry the Proud', 'Leopold, Duke of Bavaria', 'Henry II, Duke of Austria', 'Henry the Lion', 'Otto I, Duke of Bavaria', 'Louis I, Duke of Bavaria']), 'ELECTORATE-BRANDENBURG': ('Margrave de Brandeburgo', ['Albert the Bear', 'Otto I, Margrave of Brandenburg', 'Otto II, Margrave of Brandenburg']), 'SERBIA-PRINCIPALITY': ('Gran príncipe de Serbia', ['Vukan, Grand Prince of Serbia', 'Uroš I, Grand Prince of Serbia', 'Uroš II, Grand Prince of Serbia', 'Desa of Serbia', 'Tihomir of Serbia', 'Stefan Nemanja', 'Stefan the First-Crowned']), 'CILICIA-PRINCIPALITY': ('Príncipe de Cilicia', ['Thoros I, Prince of Armenia', 'Leo I, Prince of Armenia', 'Thoros II, Prince of Armenia', 'Ruben II, Prince of Armenia', 'Mleh, Prince of Armenia', 'Ruben III, Prince of Armenia', 'Leo II, King of Armenia']), 'CILICIA-KINGDOM': ('Rey de Cilicia', ['Leo II, King of Armenia']), 'GORYEO-MILITARY': ('Dirigente militar de Goryeo', ['Jeong Jung-bu', 'Gyeong Dae-seung', 'Yi Ui-min', 'Choe Chung-heon']), 'JPN-INSEI': ('Emperador retirado · gobierno de claustro', ['Emperor Shirakawa', 'Emperor Toba', 'Emperor Go-Shirakawa']), 'HIST-Q1050942': ('Dirigente de los Fujiwara del norte', ['Fujiwara no Kiyohira', 'Fujiwara no Motohira', 'Fujiwara no Hidehira', 'Fujiwara no Yasuhira']), 'KHWAREZM': ('Shah jorezmita', ['Qutb al-Din Muhammad', 'Atsiz', 'Il-Arslan', 'Sultan Shah', 'Ala ad-Din Tekish']), 'KIEVAN-RUS': ('Gran príncipe de Kiev', ['Sviatopolk II of Kiev', 'Vladimir II Monomakh', 'Mstislav I of Kiev', 'Yaropolk II of Kiev', 'Vsevolod II of Kiev', 'Iziaslav II of Kiev', 'Yuri Dolgorukiy', 'Rostislav I of Kiev', 'Mstislav II of Kiev', 'Sviatoslav III of Kiev', 'Rurik Rostislavich']), 'FATIMID-VIZIER': ('Visir del régimen fatimí', ['Al-Afdal Shahanshah', 'Shawar', 'Shirkuh', 'Saladin']), 'SICILY-KINGDOM': ('Rey de Sicilia', ['Roger II of Sicily', 'William I of Sicily', 'William II of Sicily', 'Tancred of Sicily', 'William III of Sicily', 'Henry VI, Holy Roman Emperor', 'Frederick II, Holy Roman Emperor'])}
EXTRA_GROUPS.update({'NORTHERN-SONG':('Emperador Song del Norte',['Emperor Huizong of Song']),'AYYUBID':('Sultán de Egipto',['Al-Mansur Nasir al-Din Muhammad']),'BOSNIA-BANATE':('Ban de Bosnia',['Ban Kulin']),'BOHEMIA-DUCHY-CORRECTION':('Duque de Bohemia',['Bretislav III'])})
EXTRA=[(k,role,t)for k,(role,titles)in EXTRA_GROUPS.items()for t in titles]
base=json.loads((ROOT/'.cache/rulers025-candidates.json').read_text(encoding='utf8'));rows={v['title']:v for v in base['records']}
# Retry metadata, not the HTML requests which received service back pressure.
spec=importlib.util.spec_from_file_location('g',ROOT/'scripts/review-025-rulers.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
missing=[(k,role,t) for k,role,ts in g.r.GROUPS for t in ts if t in {e['title'] for e in base['errors']}]
for k,role,t in EXTRA+missing:rows.setdefault(t,dict(key=k,role=role,title=t,requestedTitle=t,source='https://en.wikipedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_')),fields=[],parsed=[]))
titles=list(rows)
for off in range(0,len(titles),20):
 ts=titles[off:off+20];p=dict(action='wbgetentities',sites='enwiki',titles='|'.join(ts),props='labels|claims|sitelinks',redirects='yes',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'025-offices-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:18])
 for q,e in d.get('entities',{}).items():
  if 'missing' in e:continue
  canonical=e.get('sitelinks',{}).get('enwiki',{}).get('title');h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}))
  for t in ts:
   if canonical==t or rows[t].get('person')==q:rows[t].update(person=q,name=h.label(e),human=any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)))
# enwiki title redirects are different from Wikidata item redirects. Resolve
# aliases explicitly so an easily found sovereign is not silently dropped.
unresolved=[t for t,row in rows.items() if not row.get('person')]
for offset in range(0,len(unresolved),40):
 ts=unresolved[offset:offset+40];params=dict(action='query',titles='|'.join(ts),redirects=1,prop='pageprops',ppprop='wikibase_item',format='json');url='https://en.wikipedia.org/w/api.php?'+urllib.parse.urlencode(params);path=ROOT/'.cache'/('redirect025-'+hashlib.sha256('|'.join(ts).encode()).hexdigest()[:16]+'.json')
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
   p=dict(action='wbgetentities',ids='|'.join(qs),props='labels|claims|sitelinks',format='json');entities=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'025-redirect-persons-'+hashlib.sha256('|'.join(qs).encode()).hexdigest()[:16])['entities']
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
    if c.get('rank')!='deprecated' and a and b and a[0]<'1200' and b[0]>='1100':claims.append(dict(property=prop,office=office,start=a[0],end=b[0],precision=min(a[1],b[1]),statement=c.get('id')))
 p=ROOT/'.cache'/('ruler018-'+hashlib.sha256(row['requestedTitle'].encode()).hexdigest()[:16]+'.html')
 if p.exists():
  raw=p.read_text(encoding='utf8');box=re.search(r'<table\b[^>]*class="[^"]*infobox[^>]*>(.*?)</table>',raw,re.S);fields=[r.clean(t) for t in re.findall(r'<tr\b[^>]*>(.*?)</tr>',box.group(1) if box else '',re.S)]
 out.append(dict(candidate=row,claims=claims,fields=fields))
offices=sorted({v['office'] for row in out for v in row['claims'] if v.get('office')});labels={}
for off in range(0,len(offices),40):
 qs=offices[off:off+40];p=dict(action='wbgetentities',ids='|'.join(qs),props='labels',format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),'025-office-labels-'+hashlib.sha256('|'.join(qs).encode()).hexdigest()[:16]);labels.update({q:h.label(e) for q,e in d.get('entities',{}).items() if 'missing' not in e})
for row in out:
 for c in row['claims']:c['label']=labels.get(c['office'],'')
h.save(ROOT/'.cache/rulers025-office-evidence.json',out)
for row in out:
 v=row['candidate'];print(v['key'],v.get('person'),v.get('human'),v.get('name',v['title']),row['claims'] if not v['parsed'] else [],flush=True)
