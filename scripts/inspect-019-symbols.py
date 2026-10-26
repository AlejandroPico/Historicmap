"""Compact manual-review view; no public data changes."""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];pages=json.loads((ROOT/'.cache/symbols019-pages.json').read_text(encoding='utf8'))
for p in pages:
 title=p['title']
 if any(t in title for t in ['Fath','Afsharid','Zand','Mughal','Maratha','Ayutthaya period','Konbaung','Khiva','Bukhara','Kokand','Tokugawa family','Electorate of Bavaria','Wappenflagge','Brunswick before']):
  print(title,p.get('imageinfo',[{}])[0].get('extmetadata',{}).get('LicenseShortName',{}).get('value'));print(p.get('revisions',[{}])[0].get('slots',{}).get('main',{}).get('*','')[:1700],flush=True)
