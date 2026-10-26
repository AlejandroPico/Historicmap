"""Inventory of source polities and dated symbol candidates for1700–1800."""
import pathlib,json,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
raw=json.loads(next((ROOT/'.cache/cliopatria').glob('*.geojson')).read_text(encoding='utf8'))
print('Original feature example',raw['features'][0]['properties'],flush=True)
for y in [1700,1750,1789,1799]:
 selected=[f for f in raw['features'] if f['properties']['FromYear']<=y<=f['properties']['ToYear'] and not f['properties'].get('Components')]
 print('YEAR',y,'leaf records',len(selected),[(f['properties'].get('Name'),f['properties'].get('Wikidata')) for f in selected],flush=True)
ids=json.loads((ROOT/'public/data/identities.json').read_text(encoding='utf8'))['countries']
for key in ['RUE','IRN','QING','JPN','JOS','THA','HIST-Q33296','HIST-Q83618','HIST-Q746558','HIST-Q491106','HIST-Q696241','HIST-Q1062422']:
 c=ids.get(key)
 if not c:continue
 try:e=h.entity(c['qid']);print('SYMBOLS',key,c['qid'],h.values(e,'P41'),flush=True)
 except Exception as ex:print(key,str(ex),flush=True)
