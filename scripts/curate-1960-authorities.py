"""Review and import focal documentary intervals; uncertain ends never become resignations.

Research proposals are input data, not execution instructions. Keep coverage
windows distinct from terms, reject invalid intervals and preserve existing media.
"""
import copy,json,pathlib,datetime
root=pathlib.Path(__file__).resolve().parents[1];path=root/'public/data/identities.json'
d=json.loads(path.read_text(encoding='utf8'));countries=d['countries'];tag='curated-1960-0.9'
read=lambda f:json.loads((root/f).read_text(encoding='utf8'))
for key,name in [('YMK','Reino Mutawakkilita de Yemen'),('TAN','Tanganica'),('ZAN','Zanzíbar'),('UAR','República Árabe Unida')]:countries.setdefault(key,dict(qid='',name=name,flags=[],leaders=[]))
countries.setdefault('UNTEA',dict(qid='',name='Autoridad Ejecutiva Temporal de las Naciones Unidas',flags=[],leaders=[]))
portraits={l['person']:l['portrait'] for c in countries.values() for l in c['leaders'] if l.get('portrait')}
for c in countries.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=tag]
proposals=read('docs/reference/authorities-1960-proposals.json')['records']
accepted=[]
for index,p in enumerate(proposals):
 term={k:p[k] for k in ['name','role','start','end','precision','source','note']}
 term.update(person=p['person'] or f'COLLECTIVE-{p["key"]}-{index}',curated=True,acquisition=tag)
 coverage=p['intervalKind']=='documented-coverage'
 if p['status']=='needs-date-review':
  # Use an interior documentary window, excluding uncertain boundary months.
  a=datetime.date.fromisoformat(p['start']);b=datetime.date.fromisoformat(p['end'])
  a=(a.replace(day=28)+datetime.timedelta(days=4)).replace(day=1)
  b=b.replace(day=1)-datetime.timedelta(days=1)
  if a>b:continue
  term.update(start=a.isoformat(),end=b.isoformat(),precision=10)
  term['note']+=' Ventana interior de ejercicio documentado. Las fechas de nombramiento/cese y suplencias limítrofes siguen pendientes; no se presentan como días exactos.'
  coverage=True
 if coverage:term.update(startIsCoverageBoundary=True,endIsCoverageBoundary=True)
 if term['start']>term['end']:raise ValueError('Invalid interval '+term['name'])
 if term['person'] in portraits:term['portrait']=portraits[term['person']]
 countries[p['key']]['leaders'].append(term);accepted.append(dict(key=p['key'],**term))
for person,name,start,end in [('Q19593788','José Rolz-Bennett','1962-10-01','1962-11-14'),('Q5955377','Djalal Abdoh','1962-11-15','1963-04-30')]:
 term=dict(person=person,name=name,role='Administrador de Naciones Unidas · UNTEA',start=start,end=end,precision=11,source='https://digitallibrary.un.org/record/860188/files/1122901-EM.pdf',curated=True,acquisition=tag,note='Intervalo efectivo. Abdoh fue nombrado el 22/10/1962 y asumió en el territorio el 15/11; los extremos finales inclusivos se convierten del relevo y transferencia del día siguiente. La administración se transfiere a Indonesia el 1/5/1963, no en la firma de agosto de 1962.')
 if person in portraits:term['portrait']=portraits[person]
 countries['UNTEA']['leaders'].append(term)
# National monarchies are not continuing colonial administration after independence.
for key,start,end,source in [
 ('TAN','1961-12-09','1962-12-08','https://www.tanzania.go.tz/topics/policy-coordination-and-parliament'),
 ('KEN','1963-12-12','1964-12-11','https://www.mod.go.ke/history-of-our-leaders/'),
 ('SLE','1961-04-27','1971-04-18','https://www.parliament.gov.sl/history-of-parliament.html')]:
 term=dict(person='Q9682',name='Isabel II',role='Reina · jefatura del Estado del país independiente',start=start,end=end,precision=11,source=source,curated=True,acquisition=tag,note='Compartir monarca no equivale a seguir bajo administración británica. La monarquía formal se distingue de la autoridad efectiva y del Gobierno local.')
 if 'Q9682' in portraits:term['portrait']=portraits['Q9682']
 countries[key]['leaders'].append(term)
# Nigeria's First Republic had a parliamentary president and a prime minister.
# The generic Q500282 office assertions duplicated Azikiwe as head of government.
countries['NGA']['leaders']=[l for l in countries['NGA']['leaders'] if not (l['person']=='Q181782' and l['role']=='Jefatura del Gobierno' and l.get('office')=='Q500282')]
for leader in countries['NGA']['leaders']:
 if leader['person']=='Q181782' and leader['start']=='1963-10-01':
  leader.update(role='Presidencia parlamentaria · jefatura del Estado',roleSource='https://sccr.gov.ng/?page_id=119',note='Presidente de la Primera República parlamentaria; la jefatura del Gobierno corresponde a Abubakar Tafawa Balewa. La fecha presidencial no debe retrotraerse al mandato de gobernador general. Fechas del catálogo de mandatos; el relevo de enero de 1966 requiere contraste diario específico.')
# Entity scope: Nasser governed the union; this is not a Syrian presidency.
for leader in countries['EGY']['leaders']:
 if leader['start']<='1960-12-31' and leader['end']>='1960-01-01':
  term=copy.deepcopy(leader);term.update(start=max(leader['start'],'1958-02-22'),end=min(leader['end'],'1961-09-28'),acquisition=tag,curated=True)
  term['note']='Mandato en la República Árabe Unida, unión de Egipto y Siria hasta septiembre de 1961; no presidencia siria independiente. '+term.get('note','')
  if term['start']<=term['end']:countries['UAR']['leaders'].append(term)
for country in countries.values():country['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
path.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
(root/'.cache/identities/curation-1960-accepted.json').write_text(json.dumps(accepted,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Imported',len(accepted),'reviewed focal intervals; documentary windows explicitly labelled.')
