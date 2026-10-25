"""Keep dated predecessor offices visible in annual transition cards.

No predecessor is assigned a successor's government. These records are marked
as preceding authorities and retain their own real interval and source.
"""
import copy,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
TAG='curated-1880-predecessors-0.13'
def curate(incoming):
 d=copy.deepcopy(incoming);cs=d['countries']
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for source,target,year,cutoff in [('BRA-EMPIRE','BRA',1889,'1889-11-14'),('HAW-KINGDOM','HAW-PROVISIONAL',1893,'1893-01-17'),('HAW-PROVISIONAL','HAW-REPUBLIC',1894,'1894-07-03'),('JOS','KEM',1897,'1897-10-11')]:
  for old in cs[source]['leaders']:
   if old['start']>cutoff or old['end']<str(year)+'-01-01':continue
   l=copy.deepcopy(old);l.update(end=min(l['end'],cutoff),role='Autoridad predecesora · '+l['role'],curated=True,acquisition=TAG)
   l['note']=(l.get('note','')+' Autoridad de la entidad predecesora durante este año, no integrante del Gobierno sucesor.').strip()
   cs[target]['leaders'].append(l)
 for c in cs.values():c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
 return d
if __name__=='__main__':
 p=ROOT/'public/data/identities.json';d=curate(json.loads(p.read_text(encoding='utf8')))
 assert curate(d)==d
 p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
