"""Bounded metadata view used during manual symbol review."""
import json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
pages=json.loads((ROOT/'.cache/symbols018-pages.json').read_text(encoding='utf8'))
for p in pages:
 if any(x in p['title'] for x in ['Kingdom of Naples.svg','Kingdom of Naples (1808)','Kingdom of Naples (1811)','Wallachia 1834','Ottoman Empire (also','Gran Colombia.svg','Papal States (1808','Hessen ohne','Lippe (1815','Sachsen-Weimar','Württemberg (1806','Saxony before','Nassau.gif','Sokoto Caliphate.svg']):
  print(p['title'],p.get('imageinfo',[{}])[0].get('extmetadata',{}).get('LicenseShortName',{}).get('value'),flush=True)
  print(p.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')[:1250],flush=True)
