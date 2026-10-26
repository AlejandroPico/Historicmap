"""Fetch exact-file descriptions for a second, manually reviewed symbol batch."""
import pathlib,json,importlib.util,urllib.parse,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
TITLES=['Flag of Kingdom of Naples (1759-1806; 1815-1816).png','Flag of Kingdom of Naples (1806-1808).svg','Flag of the Kingdom of Naples (1808).svg','Flag of the Kingdom of Naples (1811).svg','Flag of Ethiopia (1897–1974).svg','Flag of the Merina Kingdom.svg','Old Flag of Brunei.svg','Flag of Sarawak (1870–1946, 1963–1973).svg','Jack of Sweden and Norway (1844–1905).svg','Flag of the Septinsular Republic.svg','Etrurian Kingdom and War Flag with lesser coat of arms.svg','Flag of the Grandduchy of Wurzburg.svg','Flag of Kingdom of Westphalia.svg','Flag of Hanover (1692).svg']
params=dict(action='query',titles='|'.join('File:'+t for t in TITLES),redirects=1,prop='imageinfo|revisions',rvprop='content|ids',rvslots='main',iiprop='url|extmetadata',format='json')
d=h.get('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params),'extra018review-'+hashlib.sha256('|'.join(TITLES).encode()).hexdigest()[:16]);p=ROOT/'.cache/symbols018-pages.json';pages={x['title']:x for x in json.loads(p.read_text(encoding='utf8'))};pages.update({x['title']:x for x in d.get('query',{}).get('pages',{}).values()});h.save(p,list(pages.values()))
for page in d.get('query',{}).get('pages',{}).values():
 print(page['title'],page.get('imageinfo',[{}])[0].get('extmetadata',{}).get('LicenseShortName',{}).get('value'));print(page.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')[:1200],flush=True)
