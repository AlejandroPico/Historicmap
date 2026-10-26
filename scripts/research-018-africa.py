"""Retain named African sovereigns and their reviewed chronology as candidates."""
import pathlib,json,importlib.util,urllib.parse,hashlib,re,html
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
ROWS=[
 ('HIST-Q600524','Usman dan Fodio','Q380452','1804-12-31','1816-12-31',9),
 ('HIST-Q600524','Muhammed Bello','Q608989','1817-04-21','1837-10-25',11),
 ('HIST-Q600524','Abubakar I Atiku',None,'1837-10-26','1842-11-23',11),
 ('HIST-Q600524','Ali Babba bin Bello',None,'1842-11-30','1859-10-21',11),
 ('HIST-Q600524','Ahmadu Atiku',None,'1859-10-24','1866-11-02',11),
 ('HIST-Q600524','Aliyu Karami',None,'1866-11-06','1867-10-18',11),
 ('HIST-Q600524','Ahmadu Rufai','Q21039531','1867-10-21','1873-03-12',11),
 ('HIST-Q600524','Abubakar II Atiku',None,'1873-03-16','1877-03-28',11),
 ('HIST-Q600524',"Mu'azu",None,'1877-04-06','1881-09-26',11),
 ('HIST-Q600524','Umaru bin Ali',None,'1881-10-03','1891-03-25',11),
 ('HIST-Q600524','Abdur Rahman Atiku','Q21039523','1891-03-25','1900-12-31',11),
 ('HIST-Q1139762','Muhammad al-Amin al-Kanemi','Q341882','1814-12-31','1836-12-31',9),
 ('HIST-Q1132786','Abd al-Karim Sabun','Q16157327','1805-12-31','1814-12-31',9),
]

def main():
 path=ROOT/'scripts/review-018-authorities.json';d=json.loads(path.read_text(encoding='utf8'));records=[];pending=[]
 raw=(ROOT/'.cache/Sultan-of-Sokoto018.html').read_text(encoding='utf8')
 # Resolve names from the actual succession table, never an unexamined first search hit.
 links={html.unescape(re.sub('<[^>]*>','',label)).strip():urllib.parse.unquote(title) for title,label in re.findall(r'<a[^>]*href="(?:https://en.wikipedia.org/wiki/|\./|/wiki/)([^"?#]+)"[^>]*>(.*?)</a>',raw,re.S)}
 titles=[]
 for k,name,q,a,b,p in ROWS:
  if q:continue
  title=links.get(name)
  if not title:
   title=next((t for n,t in links.items() if n.startswith(name) or name.startswith(n) and len(n)>6),None)
  titles.append((name,title))
 print('Resolved table links',titles,flush=True)
 found={}
 for name,title in titles:
  if not title:pending.append(dict(name=name,reason='No exact succession table link'));continue
  params=dict(action='wbgetentities',sites='enwiki',titles=title,props='labels|claims',format='json')
  result=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'africa018-sitelink-'+hashlib.sha256(title.encode()).hexdigest()[:16])
  for q,e in result.get('entities',{}).items():
   if any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)):found[name]=q;h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}))
 for key,name,q,a,b,p in ROWS:
  q=q or found.get(name)
  if not q and name in ['Aliyu Karami','Abubakar II Atiku']:
   # A verified succession-table person does not require a Wikidata item.
   q='SOKOTO-'+('ALIYU-KARAMI' if name=='Aliyu Karami' else 'ABUBAKAR-II')
   records.append(dict(key=key,term=dict(person=q,name=name,role='Sultán / califa de Sokoto',start=a,end=b,precision=p,source='https://en.wikipedia.org/wiki/Sultan_of_Sokoto',note='Nombre e intervalo en la tabla de sucesión; identificador local, sin retrato acreditado.')))
   continue
  if not q:pending.append(dict(name=name,reason='No verified human identity'));continue
  e=h.entity(q)
  if not any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict)):pending.append(dict(name=name,reason='Human check failed'));continue
  sokoto=key=='HIST-Q600524'
  role='Sultán / califa de Sokoto' if sokoto else 'Dirigente de facto de Bornu' if key=='HIST-Q1139762' else 'Sultán de Wadai'
  source='https://en.wikipedia.org/wiki/Sultan_of_Sokoto' if sokoto else 'https://en.wikipedia.org/wiki/Bornu_Empire' if key=='HIST-Q1139762' else 'https://en.wikipedia.org/wiki/Abd_al-Karim_Sabun'
  records.append(dict(key=key,term=dict(person=q,name=h.label(e),role=role,start=a,end=b,precision=p,source=source,note='Cronología del gobernante; no certifica control uniforme sobre todas las comunidades del contorno. Ventanas anuales conservadoras cuando no hay día acreditado.')))
 d['africanRecords']=records;d['africanPending']=pending;h.save(path,d);print('African reviewed intervals',len(records),'pending',pending,flush=True)
if __name__=='__main__':main()
