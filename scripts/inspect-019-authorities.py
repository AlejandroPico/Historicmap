import pathlib,json,importlib.util,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
d=json.loads((ROOT/'public/data/identities.json').read_text(encoding='utf8'))['countries']
for k in ['FRA','ESP','PRT','GBR','ENGLAND','SCOTLAND','RUSSIA-TSARDOM','RUE','IRN','SAFAVID','AFSHARID','ZAND','QING','JPN','JOS','THA','AYUTTHAYA','THONBURI','DUTCH-REPUBLIC','POLISH-LITHUANIAN','DENMARK-NORWAY','SWE','HIST-Q33296','HIST-Q83618']:
 c=d.get(k)
 if not c:continue
 e=h.entity(c['qid']);terms=[l for l in c['leaders'] if l['start']<'1800-01-01' and l['end']>='1700-01-01'];print(k,c['qid'],h.label(e),[(l['name'],l['start'],l['end']) for l in terms],flush=True)
for name in ['Simon Henry Adolph','Simon August Lippe','Augustus William Brunswick','Francis I Holy Roman Emperor']:
 q=h.get('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(dict(action='wbsearchentities',search=name,language='en',limit=4,format='json')),'person019-'+name.replace(' ','-'));print('SEARCH',name,[(r['id'],r.get('label'),r.get('description')) for r in q.get('search',[])],flush=True)
