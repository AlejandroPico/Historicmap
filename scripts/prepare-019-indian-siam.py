"""Reviewed reign/office fields; reject the nineteenth-century Kolhapur homonym."""
import pathlib,json,copy
ROOT=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
TAG='reviewed-india-siam-0.19'
MANUAL={
 'Q3236324':[('1719-02-28','1719-06-06',11)],'Q3238719':[('1719-06-06','1719-09-17',11)],
 'Q719449':[('1760-10-10','1788-07-31',11),('1788-10-16','1799-12-31',11)],
 'Q4849857':[('1713-11-16','1720-04-12',11)],'Q2514706':[('1720-04-17','1740-04-28',11)],
 'Q3629888':[('1740-08-01','1761-06-23',10)],'Q5971343':[('1761-06-23','1772-11-18',11)],
 'Q6002978':[('1772-12-13','1773-08-30',11)],'Q7283047':[('1773-12-05','1774-05-28',11)],
 'Q6727333':[('1774-05-28','1795-10-27',11)],'Q4848887':[('1796-12-06','1802-10-25',11)],
 'Q889151':[('1758-01-01','1758-12-31',9),('1760-01-01','1762-12-31',9)],
 'Q779323':[('1758-01-01','1759-12-31',9),('1762-01-01','1767-12-31',9)]}
def main():
 incoming=read(ROOT/'public/data/identities.json');d=copy.deepcopy(incoming);research=read(ROOT/'.cache/indian-siam019-rulers.json') if (ROOT/'.cache/indian-siam019-rulers.json').exists() else read(ROOT/'scripts/indian-siam-offices-019-research.json')['candidates'];accepted=[];rejected=[]
 for c in d['countries'].values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 images={l['person']:l['portrait'] for c in d['countries'].values() for l in c['leaders'] if l.get('portrait')}
 for row in research['records']:
  q=row.get('person');k=row['key']
  if not row.get('human') or q=='Q7285779':rejected.append(dict(candidate=row,reason='Wrong Kolhapur nineteenth-century homonym or unverified human'));continue
  dates=MANUAL.get(q) or [(v['start'],v['end'],v['precision']) for v in row['parsed'][:1]]
  if not dates:rejected.append(dict(candidate=row,reason='No reviewed office interval'));continue
  for a,b,precision in dates:
   note='Reinado o cargo documentado por separado. El título imperial o confederal no implica control uniforme de todos los Estados regionales.'
   if q=='Q13811044':note+=' Hijo de Rajaram bajo regencia de Tarabai; no se prolonga su posterior realeza de Kolhapur sobre toda la confederación.'
   if q=='Q6727333':note+=' Nombramiento durante la minoría; la acción del Gobierno corresponde a la regencia y al consejo, no a un gobernante adulto en1774.'
   if k=='AYUTTHAYA' and q in ['Q889151','Q779323']:note+=' Relevos y restablecimientos de datación divergente; observaciones anuales, no días exactos.'
   l=dict(person=q,name=row['name'],role=row['role'],start=max(a,'1700-01-01'),end=min(b,'1799-12-31'),precision=precision,source=row['source'],note=note,curated=True,acquisition=TAG,startIsCoverageBoundary=a<'1700-01-01' or precision<11,endIsCoverageBoundary=b>='1799-12-31' or precision<11)
   if l['start']>l['end']:continue
   if q in images:l['portrait']=images[q]
   d['countries'][k]['leaders'].append(l);accepted.append(dict(key=k,term=l))
 save(ROOT/'public/data/identities.json',d);save(ROOT/'scripts/indian-siam-offices-019-research.json',dict(accepted=accepted,rejected=rejected,candidates=research));print('Reviewed Indian/Siam offices',len(accepted),'unresolved',len(rejected))
if __name__=='__main__':main()
