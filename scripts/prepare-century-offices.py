"""Freeze reviewed offices in their entity-owned century dossiers.

Consumes acquired office claims and explicit reign-field evidence. It never
derives a mandate from birth/death or a different crown. No ruler lists here.
"""
import pathlib,json,re,argparse,copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def main(century,review):
 first,last=f'{century:04d}-01-01',f'{century+99:04d}-12-31'
 evidence=read(ROOT/f'.cache/rulers{review}-office-evidence.json');fields=read(ROOT/f'.cache/rulers{review}-reign-evidence.json')
 by_title={r['candidate']['requestedTitle']:r for r in evidence};by_person={r.get('person'):r for r in fields}
 ids=read(ROOT/'public/data/identities.json');baseline=read(ROOT/f'.cache/baseline{review}.json');tag='historical-0.'+str(int(review))
 aliases={}
 # A dossier may explicitly retain a previously shipped canonical identity.
 dossiers={read(p)['key']:p for p in (ROOT/'Países').glob(f'*/periodos/{century:04d}-{century+99:04d}.json')}
 for key,path in dossiers.items():
  d=read(path)
  for q in d.get('sourceKeys',[]):aliases[q]=key
 records=0;unresolved=0
 for key,c in ids['countries'].items():
  terms=[r for r in c['leaders']if r.get('acquisition')==tag and r['start']<=last and r['end']>=first]
  if not terms:continue
  target=aliases.get(key,key);path=dossiers.get(target)
  if not path:
   import unicodedata
   name=c['name'];slug=re.sub('[^a-zA-Z0-9]+','-',unicodedata.normalize('NFD',name).encode('ascii','ignore').decode()).strip('-')[:65]
   folder=next((p.parent for p in (ROOT/'Países').glob('*/entidad.json')if read(p)['key']==target),ROOT/'Países'/(target+'-'+slug))
   path=folder/f'periodos/{century:04d}-{century+99:04d}.json';path.parent.mkdir(parents=True,exist_ok=True)
   save(path,dict(key=target,identity=dict(qid=c['qid'],name=c['name']),revision=f'0.{int(review)}.0',acquisition=f'century-{century}-0.{int(review)}',coverageStart=century,coverageEnd=century+99,candidates=[],leaders=[],symbols=[],institutions=[],governance=[]));dossiers[target]=path
  d=read(path);d['acquiredLeaders']=[{k:v for k,v in r.items()if k not in ['acquisition','portrait']}for r in terms];save(path,d)
 for key,path in dossiers.items():
  d=read(path);accepted=[];pending=[];frozen=[];seen=set();bounds=d.get('officeBounds',[first,last])
  def add(row,role,a,b,ev,note='',precision=9):
   if a>b or a>last or b<first:return
   start,end=max(a,first,bounds[0]),min(b,last,bounds[1])
   if start>end:return
   sig=(row['person'],role,start,end)
   if sig in seen:return
   seen.add(sig);l=dict(person=row['person'],name=row.get('name',row['requestedTitle']),role=role,start=start,end=end,precision=precision,source=row['source'],note=note or 'Dignidad histórica documentada; la ficha no acredita control uniforme de todo el contorno de fuente.')
   if start>a:l['startIsCoverageBoundary']=True
   if end<b:l['endIsCoverageBoundary']=True
   accepted.append(l);frozen.append(dict(person=row['person'],title=row['requestedTitle'],source=row['source'],selectionEvidence=ev))
  for group in d.get('candidates',[]):
   pattern=group.get('officePattern')
   for title in group['titles']:
    ev=by_title.get(title);row=ev['candidate']if ev else{}
    if not row.get('human'):pending.append(dict(title=title,reason='Identidad humana canónica no resuelta; no usar homónimo ni primer resultado sin verificar.'));continue
    dates=[];phases=group.get('reviewedPhases',{}).get(title,[])
    if phases:
     for p in phases:add({**row,'source':p.get('source',row['source'])},p['role'],p['start'],p['end'],dict(type='explicit-office-phase',source=p.get('source',row['source'])),p.get('note',d.get('officeNote','')))
     continue
    # Prefer evidence for this precise dignity; never another crown.
    if pattern:
     for c in ev['claims']:
      if re.search(pattern,c.get('label',''),re.I):dates.append((c['start'],c['end'][:4]+'-12-31'if c['precision']==9 and c['end'].endswith('-01-01')else c['end'],c,c['precision']))
    if not dates or d.get('preferExplicitReignFields'):
     explicit=[]
     for f in by_person.get(row['person'],{}).get('reignFields',[]):
      if f['parsed']and (not pattern or re.search(pattern,f.get('office','')+' '+f.get('reignType',''),re.I))and not re.search('Retired|Emeritus|Taishang|consort',f.get('office',''),re.I)and not(re.search('Caesar',f.get('reignType',''),re.I)and not re.search('Caesar',pattern or '',re.I)):explicit.append((f['parsed']['start'],f['parsed']['end'],f,f['parsed']['precision']))
     if explicit:
      primary=[v for v in explicit if v[2].get('field')!='succession-template']
      # A later restoration may appear only in the explicit succession table.
      # Retain non-overlapping table intervals without duplicating alternative
      # dates for the same reign already described in the primary infobox.
      dates=[*primary,*[v for v in explicit if v[2].get('field')=='succession-template'and not any(v[0]<=p[1]and p[0]<=v[1]for p in primary)]]if primary else explicit
    if not dates:pending.append(dict(title=title,person=row['person'],reason='Fechas de la dignidad prevista no resueltas; no inferidas de la biografía ni de otro cargo.'));continue
    for a,b,why,precision in dates:add(row,group['role'],a,b,why,d.get('officeNote',''),precision)
  generic=[]
  for l in d.get('acquiredLeaders',[]):
   if any(r['person']==l['person']and r['start']<=l['end']and l['start']<=r['end'] for r in accepted):continue
   if l['start']>bounds[1]or l['end']<bounds[0]:continue
   l={**l,'start':max(l['start'],bounds[0]),'end':min(l['end'],bounds[1])};generic.append(l)
  d['leaders']=[*generic,*accepted,*d.get('documentedAuthorities',[])];d['officeResearch']=dict(selected=len(accepted),acquiredRetained=len(generic),documentaryLocalAuthorities=len(d.get('documentedAuthorities',[])),evidence=frozen,pending=pending)
  save(path,d);records+=len(accepted);unresolved+=len(pending)
 # Retire only the temporary acquisition additions, keeping every prior fact.
 for key,c in ids['countries'].items():c['leaders']=[l for l in c['leaders']if l.get('acquisition')!=tag]
 for k,c in baseline['countries'].items():
  fact=lambda l:{a:b for a,b in l.items() if a!='portrait'}
  current_facts=[fact(l) for l in ids['countries'][k]['leaders']]
  assert all(fact(l) in current_facts for l in c['leaders']),k
 (ROOT/'public/data/identities.json').write_text(json.dumps(ids,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
 print('Entity dossiers',len(dossiers),'selected offices',records,'unresolved candidates',unresolved)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--century',type=int,required=True);p.add_argument('--review',required=True);a=p.parse_args();main(a.century,a.review)
