"""Research candidates only; no public data writes or automatic first-result adoption."""
import importlib.util,urllib.parse,json,pathlib,collections,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
def searches():
 names=['Leopold II Lippe','Adolphe Nassau','Louis II Hesse','Ernest I Saxe Coburg','Günther Friedrich Carl Schwarzburg','Bernardo O Higgins','Abd al Karim Sabun','Muhammadu Bello','Rabah Zubayr','Shehu al Kanemi']
 out=[]
 for name in names:
  d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='wbsearchentities',search=name,language='en',limit=3,format='json')),'review018-search-'+name.replace(' ','-'))
  r=[dict(qid=r['id'],label=r.get('label'),description=r.get('description')) for r in d.get('search',[])];out.append(dict(name=name,matches=r));print(name,r,flush=True)
 h.save(ROOT/'.cache/review018-searches.json',out)
def governance():
 d=json.loads((ROOT/'public/data/identities.json').read_text(encoding='utf8'));freq=collections.Counter();items=[];errors=[]
 for k,c in d['countries'].items():
  if not c.get('qid'):continue
  try:e=h.entity(c['qid'])
  except Exception as ex:errors.append(dict(key=k,error=str(ex)));continue
  claims=[]
  for p in ['P122','P31']:
   for st in e.get('claims',{}).get(p,[]):
    q=st['mainsnak'].get('datavalue',{}).get('value',{}).get('id')
    if q and st.get('rank')!='deprecated':claims.append(dict(property=p,qid=q,start=h.qual(st,'P580'),end=h.qual(st,'P582')));freq[q]+=1
  items.append(dict(key=k,qid=c['qid'],claims=claims))
 h.save(ROOT/'.cache/governance018-candidates.json',dict(items=items,errors=errors))
 print('Most frequent classifications',[(q,h.label(h.entity(q)),n) for q,n in freq.most_common(55)],flush=True)
if __name__=='__main__':
 {'search':searches,'governance':governance}[sys.argv[1]]()
