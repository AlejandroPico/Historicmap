"""Do not present the damaged Sunjo painting as an identifiable face portrait."""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
source='https://www.gogung.go.kr/ebook/access/ecatalogt.jsp?Dir=45&callmode=admin&catimage=&eclang=ko&start=64&um=s'
if __name__=='__main__':
 p=ROOT/'scripts/media-exclusions.json';rows=read(p);rows=[r for r in rows if not(r['person']=='Q459964' and r['title']=='순조어진.jpg')];rows.append(dict(person='Q459964',title='순조어진.jpg',reviewed='2026-10-26',reason='Damaged attributed royal painting without a recognisable face; retained in provenance but excluded as the identifying leader portrait.',sources=[source]));save(p,rows)
 p=ROOT/'public/data/identities.json';d=read(p)
 for c in d['countries'].values():
  for l in c['leaders']:
   if l['person']=='Q459964' and l.get('portrait',{}).get('title')=='순조어진.jpg':
    l.pop('portrait');l['note']=(l.get('note','')+' El retrato real conservado es fragmentario y no permite identificar el rostro; no se utiliza como fotografía identificativa. Catálogo del Museo Nacional del Palacio de Corea: '+source).strip()
 save(p,d)
