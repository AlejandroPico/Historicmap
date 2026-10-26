"""Inspect independently dated basemaps for finer German entities; no adoption."""
import pathlib,json,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1];manifest=json.loads((ROOT/'public/data/manifest.json').read_text(encoding='utf8'));entry=next(e for e in manifest['entries'] if e['file']=='world_1800.geojson')
print('Existing source',entry,flush=True)
for year in [1700,1715,1783,1800]:
 p=ROOT/'.cache'/f'german-019-world-{year}.geojson'
 if not p.exists():
  url=entry['url'].replace('world_1800.geojson',f'world_{year}.geojson')
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Historicmap/0.19 research'}),timeout=60) as r:p.write_bytes(r.read())
 d=json.loads(p.read_text(encoding='utf8'));print(year,'features',len(d['features']),flush=True)
 for f in d['features']:
  prop=f['properties'];name=str(prop)
  if any(s.casefold() in name.casefold() for s in ['Bavaria','Saxony','Hanover','Hesse','Hannover','Brunswick','Baden','Württemberg','Wurtemberg','Prussia','Waldeck','Lippe','Mecklenburg','Palatinate','Anhalt','Saxe','Würzburg','Schwarzburg','Mainz','Trier','Cologne']):print(prop,flush=True)
