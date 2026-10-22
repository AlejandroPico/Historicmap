"""Repair the 0.4 metadata join without regenerating unrelated geometries.

Statistics already have World Bank entity keys; only the Natural Earth naming
and lookup overlay was corrupted by ISO_A3_EH values shared across polities.
The normal prepare-history.py import uses the same explicit alias contract.
"""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
path=root/'public/data/profiles.json';data=read(path)
aliases={'PSX':'PSE','SDS':'SSD','SAH':'ESH','KOS':'XKX','ALD':'ALA'}
codes={}
for f in read(root/'.cache/natural-countries.json')['features']:
    p=f['properties'];code=p['ADM0_A3'];key=aliases.get(code,code);codes[code]=key
    profile=data['countries'].setdefault(key,dict(name=p['NAME'],capital='',series={}))
    profile.update(name=p.get('NAME_ES') or p['NAME'],englishName=p['ADMIN'],official=p.get('FORMAL_ES') or p.get('FORMAL_EN') or p['ADMIN'],continent=p['CONTINENT'],subregion=p['SUBREGION'],territoryType=p['TYPE'],sovereign=p.get('SOVEREIGNT'))
data['codes']=codes
path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
manifestPath=root/'public/data/manifest.json';manifest=read(manifestPath)
entry=next(e for e in manifest['entries'] if e['file']=='profiles.json')
entry.update(bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),transform='Preserve dated World Bank series. Join Natural Earth ADM0_A3 using only equivalent-entity aliases PSX/PSE, SDS/SSD, SAH/ESH, KOS/XKX, ALD/ALA. Dependencies and disputed territories retain their own metadata; never overwrite a sovereign profile through ISO_A3_EH.')
manifestPath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Repaired profiles:',len(data['countries']),'map entity keys:',len(codes))
