"""Focal1939 Slovak client identity; later offices/geometry remain separate."""
import copy,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data'
TAG='curated-central-europe-1939-0.12'
SOURCE='https://www.nrsr.sk/dl/Browser/Document?documentId=135163'
def curate(incoming):
 d=copy.deepcopy(incoming);cs=d['countries'];photos={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 c=cs.setdefault('SVK-1939',dict(qid='Q154401',name='Eslovaquia · República Eslovaca de1939',flags=[],leaders=[]))
 c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for q,name,role,start,note in [
  ('Q154346','Jozef Tiso','Primer ministro; presidente desde26/10/1939','1939-03-14','Gobierno tras la proclamación14/3. Presidencia desde26/10, distinta del cargo gubernamental anterior; el Parlamento documenta el nombramiento del nuevo gabinete deTuka28/10. El límite de diciembre sólo delimita esta corrección, no su cese en1945.'),
  ('Q367181','Vojtech Tuka','Primer ministro de la República Eslovaca','1939-10-28','El acta original del Parlamento atribuye el nombramiento del gabinete al28/10/1939. No se retrotrae su jefatura del Gobierno a la proclamación de marzo. El cargo continuó después de1939; este extremo es sólo cobertura.'),
 ]:
  l=dict(person=q,name=name,role=role,start=start,end='1939-12-31',source=SOURCE,note=note,precision=11,curated=True,acquisition=TAG,endIsCoverageBoundary=True)
  if q in photos:l['portrait']=copy.deepcopy(photos[q])
  c['leaders'].append(l)
 c['leaders'].sort(key=lambda l:(l['start'],l['name']))
 return d
if __name__=='__main__':
 p=OUT/'identities.json';p.write_text(json.dumps(curate(json.loads(p.read_text(encoding='utf8'))),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
 p=OUT/'country-history.json';h=json.loads(p.read_text(encoding='utf8'));prefix='central-europe-1939-'
 h['records']=[r for r in h['records'] if not r['id'].startswith(prefix)]
 h['relations']=[r for r in h['relations'] if not r['id'].startswith(prefix)]
 h['records'].append(dict(id=prefix+'slovak-state',keys=['SVK-1939','CSK'],start='1939-03-14',end='1940-01-01',section='history',title='Desmembración checoslovaca y Estado eslovaco',text='Los Sudetes se incorporaron aAlemania en1938. En marzo1939 el Estado eslovaco se separó bajo tutela alemana, mientras Bohemia yMoravia quedaron bajo ocupación alemana y régimen de protectorado. La Constitución eslovaca se aprobó21/7; Tiso asumió la presidencia en octubre yTuka el nuevo gabinete28/10. No equivale a anexión alemana deEslovaquia ni a continuidad territorial deChecoslovaquia en el cierre1939.',source='https://www.nrsr.sk/dl/Browser/Document?documentId=135154',sourceLabel='Parlamento eslovaco · acta constitucional21/7/1939'))
 h['relations'].append(dict(id=prefix+'csk-slovakia',**{'from':dict(key='CSK',name='Checoslovaquia',year=1938)},to=dict(key='SVK-1939',name='Eslovaquia · República Eslovaca',year=1939),date='1939-03-14',type='secession',label='Proclamación eslovaca y desmembración deChecoslovaquia',note='Separación bajo tutela alemana, distinta del protectorado deBohemia yMoravia. El contorno eslovaco de apoyo es una referencia recortada, no una frontera diaria certificada.',source='https://encyclopedia.ushmm.org/content/en/article/jozef-tiso-1',sourceLabel='USHMM · historia deTiso y del Estado eslovaco'))
 p.write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 p=OUT/'historical-context.json';h=json.loads(p.read_text(encoding='utf8'));h['events']=[e for e in h['events'] if e['id']!=prefix+'partition']
 h['events'].append(dict(id=prefix+'partition',title='Ocupación deBohemia yMoravia y Estado eslovaco',type='transition',start='1939-03-14',end='1940-01-01',countries=['DEU','CSK','SVW','HUN'],text='En marzo1939 se desmiembra laChecoslovaquia restante: territorio checo bajo ocupación alemana y protectorado, Estado eslovaco cliente y expansión húngara oriental. Se distingue de la incorporación de losSudetes de1938. La geometría eslovaca utiliza un contorno de referencia recortado; no certifica todos los ajustes de frontera de1939.',source='https://encyclopedia.ushmm.org/content/en/article/jozef-tiso-1',sourceLabel='USHMM · Estado eslovaco y tutela alemana'))
 p.write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('Prepared Slovak1939 identity, offices and dated context.')
