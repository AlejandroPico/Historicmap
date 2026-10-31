from civil_dates import period_name
"""Compile original entity-owned political components and dated identity rules.

Source acquisition is separate. No remote reads or country inventories here.
"""
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf8'))
def main(start,end):
 asset=str(start)if start>0 else'bc'+str(-start)
 dossiers=sorted((ROOT/'Países').glob(f'*/periodos/{period_name(start,end)}.json'));features=[];seen=set();ids=read(ROOT/'public/data/identities.json')['countries'];resolution=dict(format='dated-entity-resolution',coverageStart=start,coverageEnd=end,referenceDate='2026-10-28',qidKeys={},names={},records=[])
 for path in dossiers:
  d=read(path)
  if d.get('identity'):
   resolution['names'][d['key']]=d['identity']['name']
   if d['identity'].get('qid'):resolution['qidKeys'][d['identity']['qid']]=d['key']
  for ref in d.get('geography',[]):
   original=(path.parent/ref['file']).resolve()
   if not original.is_relative_to((ROOT/'Países').resolve()):raise ValueError('Original outside entity tree')
   raw=original.read_bytes()
   if hashlib.sha256(raw).hexdigest()!=ref['sha256']:raise ValueError('Original checksum '+str(original))
   for f in json.loads(raw)['features']:
    p=f['properties'];index=f['sourceIndex'];fid=f'clio-{index}'
    if p['Components'] or fid in seen:raise ValueError('Duplicate or aggregate component '+fid)
    seen.add(fid);resolution['qidKeys'][p['Wikidata']]=d['key']
    features.append(dict(type='Feature',id=fid,geometry=f['geometry'],properties=dict(identityKey=d['key'],entityCode=d['key'],name=p['Name'],originalName=p['Name'],wikidata=p['Wikidata'],start=max(start,p['FromYear']),end=min(end,p['ToYear']),parentName=p['MemberOf'].strip('()'),code='',source=ref['source'],precision='annual-synthesis',politicalStatus='Entidad histórica · reconstrucción anual')))
  for fix in d.get('entityRules',[]):
   if f'historical-{asset}-entities.json'in fix['files']:
    r=dict(fix['record'],key=d['key'],entityCode=d['key'],acquisition=d['acquisition']);r.update(start=max(start,r['start']),end=min(end,r['end']));resolution['records'].insert(0,r)
 # Only referenced external administrators need the existing catalogue. Copying
 # every runtime identity made these assets depend on which period compiled first.
 for r in resolution['records']:
  admin=r.get('admin')
  if admin and admin not in resolution['names']:resolution['names'][admin]=ids[admin]['name']
 features.sort(key=lambda f:int(f['id'][5:]));out=ROOT/'public/data';manifest=read(out/'manifest.json');template=next(e for e in manifest['entries']if e['file']=='early-modern.geojson')
 for name,data in[(f'early-modern-{asset}.geojson',dict(type='FeatureCollection',features=features)),(f'historical-{asset}-entities.json',resolution)]:
  raw=(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n').encode();(out/name).write_bytes(raw)
  if name.endswith('.geojson'):
   entry={k:v for k,v in template.items()if k not in['file','features','bytes','sha256','coverage','transform']};entry.update(file=name,features=len(features),coverage=f'{start}/{end}',sourceVersion=template['version'],transform='Original leaf components from entity-owned credited Cliopatria copies; coordinates and original index IDs retained. Annual synthesis, not daily surveyed borders.')
  else:entry=dict(file=name,format=resolution['format'],records=len(resolution['records']),source='Entity-owned dated identity review',url=f'https://github.com/AlejandroPico/Historicmap/blob/main/docs/RESEARCH-{asset}.md',license='CC0-1.0 (editorial resolution); geometry separately licensed',coverageStart=start,coverageEnd=end)
  entry.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),version='Historicmap '+read(ROOT/'package.json')['version']);manifest['entries']=[e for e in manifest['entries']if e['file']!=name]+[entry]
 (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('Original components',len(features),'identity rules',len(resolution['records']))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True);a=p.parse_args();main(a.start,a.end)
