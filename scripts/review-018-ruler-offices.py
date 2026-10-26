"""Resolve exact encyclopedia sitelinks and retain office statements for review."""
import importlib.util,urllib.parse,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
titles=['Leopold II, Prince of Lippe','Adolphe, Grand Duke of Luxembourg','Louis II, Grand Duke of Hesse','Ernest I, Duke of Saxe-Coburg and Gotha','Günther Friedrich Karl II, Prince of Schwarzburg-Sondershausen','Charles Frederick, Grand Duke of Baden','Frederick William, Elector of Hesse','Abd al-Karim Sabun','Muhammad al-Amin al-Kanemi','Supreme Director of Chile']
params=dict(action='wbgetentities',sites='enwiki',titles='|'.join(titles),props='labels|descriptions|claims|sitelinks',redirects='yes',format='json')
d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'review018-person-sitelinks-v2')
if 'error' in d:raise ValueError(d['error'])
out=[]
for q,e in d.get('entities',{}).items():
 if 'missing' in e:continue
 h.save(h.CACHE/('historical-entity-'+q+'.json'),dict(entities={q:e}));claims=[]
 for p in ['P39','P97']:
  for st in e.get('claims',{}).get(p,[]):
   v=st['mainsnak'].get('datavalue',{}).get('value',{});office=v.get('id') if isinstance(v,dict) else None
   if office:claims.append(dict(property=p,office=office,label=h.label(h.entity(office)),start=h.qual(st,'P580'),end=h.qual(st,'P582')))
 out.append(dict(qid=q,label=h.label(e),claims=claims));print(q,h.label(e),claims,flush=True)
h.save(ROOT/'.cache/review018-ruler-offices.json',out)
