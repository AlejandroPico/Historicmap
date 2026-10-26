"""Dated holders of explicitly reviewed offices,1800–1900; candidates only."""
import importlib.util,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
OFFICES={'HIST-Q10957559':('Q27569220','Príncipe de Moldavia'),'HIST-Q171393':('Q673697','Príncipe de Valaquia'),'HIST-Q600524':('Q28064643','Sultán / califa de Sokoto'),'CHL':('Q7155734','Director supremo de Chile')}
def acquire():
 out=[];audit=[]
 for key,(office,role) in OFFICES.items():
  query='SELECT ?person ?statement ?start ?end ?precision ?endPrecision WHERE { ?person p:P39 ?statement . ?statement ps:P39 wd:'+office+'; pq:P580 ?start; pq:P582 ?end; wikibase:rank ?rank . FILTER(?rank != wikibase:DeprecatedRank) OPTIONAL { ?statement pqv:P580/wikibase:timePrecision ?precision } OPTIONAL { ?statement pqv:P582/wikibase:timePrecision ?endPrecision } FILTER(?start <= "1900-12-31T23:59:59Z"^^xsd:dateTime && ?end >= "1800-01-01T00:00:00Z"^^xsd:dateTime) }'
  try:rows=h.query(query,'offices018-'+hashlib.sha256(query.encode()).hexdigest()[:20])
  except Exception as e:audit.append(dict(key=key,error=str(e)));continue
  for row in rows:
   q=row['person']['value'].rsplit('/',1)[-1]
   if not h.eligible_person(q):continue
   originalStart=row['start']['value'][:10];originalEnd=row['end']['value'][:10];a=max(originalStart,'1800-01-01');b=min(originalEnd,'1900-12-31')
   if a>b:continue
   l=dict(person=q,name=h.label(h.entity(q)),role=role,start=a,end=b,precision=min(int(row.get('precision',{}).get('value',11)),int(row.get('endPrecision',{}).get('value',11))),source='https://www.wikidata.org/wiki/'+q,sourceStatement=row['statement']['value'],office=office,acquisition='reviewed-offices-0.18',startIsCoverageBoundary=a!=originalStart,endIsCoverageBoundary=b!=originalEnd)
   out.append(dict(key=key,term=l))
  print(key,len(rows),'dated office statements',flush=True)
 h.save(ROOT/'.cache/offices018-candidates.json',dict(records=out,audit=audit))
if __name__=='__main__':acquire()
