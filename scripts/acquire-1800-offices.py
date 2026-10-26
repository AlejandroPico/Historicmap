"""Acquire dated holders of explicitly reviewed historical offices,1800–1819.

Writes a research candidate file only. No public catalogue mutation. Fictional
holders are rejected before interval inference. No missing end is promoted to
incumbency; all candidates have dated ends and preserve precision/source IDs.
"""
import pathlib,json,importlib.util,hashlib,copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
REVIEWED={'PRUSSIA':'Q3240735','JPN':'Q131767','QING':'Q268218','PAPAL-STATES':'Q19546','HAW-KINGDOM':'Q12097','HIST-Q1071439':'Q65556515','SAR':'Q111730452','BRA-EMPIRE':'Q106547235','EGY':'Q127878'}
def acquire():
 registry=json.loads((ROOT/'.cache/offices-1840.json').read_text(encoding='utf8'))
 rows=[(r['key'],r['office'],r['requested']) for r in registry if r['office']]
 for key,office in REVIEWED.items():rows.append((key,office,h.label(h.entity(office))))
 result=[];audit=[]
 # Country scope is essential for the generic king title: King of Hawaii is
 # not a dedicated office in the source. Never assign every world king there.
 for key,office,label in rows:
  scope='?person wdt:P27 wd:Q156418 .' if key=='HAW-KINGDOM' else ''
  query='SELECT ?person ?statement ?start ?end ?precision ?endPrecision WHERE { ?person p:P39 ?statement . ?statement ps:P39 wd:'+office+'; pq:P580 ?start; pq:P582 ?end; wikibase:rank ?rank. '+scope+' FILTER(?rank != wikibase:DeprecatedRank) OPTIONAL { ?statement pqv:P580/wikibase:timePrecision ?precision } OPTIONAL { ?statement pqv:P582/wikibase:timePrecision ?endPrecision } FILTER(?start <= "1819-12-31T23:59:59Z"^^xsd:dateTime && ?end >= "1800-01-01T00:00:00Z"^^xsd:dateTime) }'
  try:terms=h.query(query,'offices-1800-1819-'+hashlib.sha256(query.encode()).hexdigest()[:20])
  except Exception as e:audit.append(dict(key=key,office=office,error=str(e)));continue
  for row in terms:
   q=row['person']['value'].rsplit('/',1)[-1]
   if not h.eligible_person(q):continue
   entity=h.entity(q);start=row['start']['value'][:10];end=row['end']['value'][:10]
   if start>end:continue
   # Generic Shah source encompasses different lands. Its recorded citizenship
   # must explicitly identify Iran; unrelated Afghan shahs remain excluded.
   citizenship={v.get('id') for v in h.values(entity,'P27') if isinstance(v,dict)}
   if key=='IRN' and not citizenship.intersection({'Q794','Q189326','Q18234383','Q63158027'}):audit.append(dict(key=key,person=q,reason='Generic Shah title without an Iranian citizenship link'));continue
   a=max(start,'1800-01-01');b=min(end,'1819-12-31')
   if key=='PAPAL-STATES':b=min(b,'1870-09-20')
   if a>b:continue
   role='Shogun · Gobierno militar' if key=='JPN' else 'Primer ministro' if key=='NPL' and office=='Q30100626' else label
   term=dict(person=q,name=h.label(entity),role=role,start=a,end=b,precision=min(int(row.get('precision',{}).get('value',11)),int(row.get('endPrecision',{}).get('value',11))),office=office,source='https://www.wikidata.org/wiki/'+q,sourceStatement=row['statement']['value'],acquisition='historical-offices-0.17',startIsCoverageBoundary=a!=start,endIsCoverageBoundary=b!=end,note='Mandato de un cargo histórico explícito; no se deriva de la jefatura contemporánea del país. Los límites de cobertura no son nombramientos o dimisiones.')
   result.append(dict(key=key,term=term))
  print(key,office,len(terms),'source rows',flush=True)
 h.save(ROOT/'.cache/historical-offices-017.json',dict(records=result,audit=audit))
 print('Dated candidates',len(result),flush=True)
if __name__=='__main__':acquire()
