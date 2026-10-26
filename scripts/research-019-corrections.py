"""Verify uncertain polity items and exact human homonyms before integration."""
import pathlib,importlib.util,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
params=dict(action='wbgetentities',ids='Q208068|Q208069|Q310673',props='labels|descriptions',languages='en|es',format='json',redirects='yes');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'019-verify-polity-items');print('POLITIES',[(q,h.label(e),e.get('descriptions')) for q,e in d.get('entities',{}).items()],flush=True)
for name in ['Simon Henry Adolph','Simon August Lippe','Augustus William Brunswick','Francis I Holy Roman Emperor','Afsharid dynasty','Zand dynasty','Gyoryonggi','교룡기','皇帝大纛']:
 params=dict(action='wbsearchentities',search=name,language='en',limit=3,format='json');d=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(params),'019-correction-'+name.replace(' ','-'));print(name,[(r['id'],r.get('label'),r.get('description')) for r in d.get('search',[])],flush=True)
