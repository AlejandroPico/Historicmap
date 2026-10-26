"""Inspect dated symbols and missing authorities without modifying public data."""
import json,pathlib,importlib.util,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
d=json.loads((ROOT/'public/data/identities.json').read_text(encoding='utf8'))['countries'];out=[]
for k,c in d.items():
 if not k.startswith('HIST-') or c['flags']:continue
 q=c.get('qid','');p=h.CACHE/('historical-entity-'+q+'.json')
 if not p.exists():continue
 e=json.loads(p.read_text(encoding='utf8')).get('entities',{}).get(q,{})
 flags=h.values(e,'P41')
 if flags:out.append(dict(key=k,name=c['name'],flags=flags))
print(json.dumps(out,ensure_ascii=False,indent=1))
h.save(ROOT/'.cache/missing-flags018-candidates.json',out)
