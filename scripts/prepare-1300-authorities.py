"""Reviewed offices1300–1399; source offices, rival claims and calendars stay explicit."""
import pathlib,json,copy,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1300-0.23'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
INDICES={('NAVARRE-KINGDOM','Q8384'):1,('HIST-Q12548','Q152717'):1,('HIST-Q12548','Q155669'):1,('HIST-Q12548','Q152148'):1,('POLAND-MEDIEVAL','Q54040'):2,('POLAND-MEDIEVAL','Q53998'):1,('SERBIA-EMPIRE','Q207303'):1,('SERBIA-EMPIRE','Q279693'):1,('BOSNIA-KINGDOM','Q319605'):1,('GOLDEN-HORDE','Q309585'):1,('CILICIA-KINGDOM','Q887899'):2}
MANUAL={
 ('FRA','Q8404'):[('1316-11-15','1316-11-20')],('NAVARRE-KINGDOM','Q8404'):[('1316-11-15','1316-11-20')],
 ('ARAGON','Q312735'):[('1291-01-01','1327-12-31')],('ARAGON','Q380088'):[('1327-01-01','1336-12-31')],
 ('BYZANTINE','Q37074'):[('1390-04-14','1390-09-17')],
 ('OTT','Q83100'):[('1299-01-01','1324-12-31')],('OTT','Q133168'):[('1324-01-01','1362-12-31')],
 ('POLAND-MEDIEVAL','Q155581'):[('1300-01-01','1305-12-31')],
 ('LITHUANIA-DUCHY','Q54049'):[('1377-01-01','1381-12-31'),('1382-01-01','1392-12-31')],('LITHUANIA-DUCHY','Q355869'):[('1381-01-01','1382-12-31')],('LITHUANIA-DUCHY','Q218186'):[('1392-01-01','1430-12-31')],
 ('BOSNIA-BANATE','Q319605'):[('1353-01-01','1366-12-31'),('1367-01-01','1377-12-31')],('BOSNIA-KINGDOM','Q2578848'):[('1398-01-01','1404-12-31')],
 ('JPN','Q313942'):[('1318-01-01','1331-12-31'),('1333-01-01','1336-12-31'),('1336-01-01','1339-12-31')],
 ('GORYEO','Q494012'):[('1308-01-01','1313-12-31')],('GORYEO','Q487766'):[('1330-01-01','1332-12-31'),('1339-01-01','1343-12-31')],('GORYEO','Q494056'):[('1344-01-01','1348-12-31')],('GORYEO','Q485495'):[('1348-01-01','1351-12-31')],('GORYEO','Q302096'):[('1374-01-01','1388-12-31')],('GORYEO','Q485504'):[('1388-01-01','1389-12-31')],
 ('HIST-Q184536','Q309333'):[('1312-01-01','1337-12-31')],('HIST-Q184536','Q3028531'):[('1340-01-01','1359-12-31')]}
PATTERNS={'PAPAL-STATES':'^Papa$','CASTILE':'Castilla|Castile','ARAGON':'Corona de Aragón','BYZANTINE':'emperador bizantino','OTT':'sultán del Imperio Otomano','JPN':'emperador de Japón|pretendiente al trono|shōgun|Shikken','GORYEO':'monarca|wang','JOS':'Joseon|Corea','MARINID':'sultán','MAMLUKS':'Sultán de Egipto|Sultán mameluco','ETH':'Emperador de Etiopía','SAVOY-COUNTY':'conde de Saboya','HESSE-UNITED':'landgrave','SAXONY-ELECTORATE':'Sajonia|Saxe-Wittenberg','ELECTORATE-BRANDENBURG':'Brandeburgo|príncipe elector','DNK':'Dinamarca','NORWAY-KINGDOM':'Noruega','SWE':'Suecia'}
def research():
 base=read(ROOT/'.cache/rulers023-candidates.json');evidence=read(ROOT/'.cache/rulers023-office-evidence.json');extra=[v['candidate'] for v in evidence if v['candidate']['title'] not in {r['title'] for r in base['records']}];accepted=[];rejected=[]
 def add(k,q,name,role,a,b,source,note):
  if a>'1399-12-31' or b<'1300-01-01':return
  if a>b:return
  clean=lambda s:re.sub(r'(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])',' ',s)
  accepted.append(dict(key=k,term=dict(person=q,name=clean(name),role=clean(role),start=max(a,'1300-01-01'),end=min(b,'1399-12-31'),precision=9,source=source,curated=True,note=clean(note+' Observación anual; calendario histórico y control territorial no acreditados día a día.'),startIsCoverageBoundary=a<'1300-01-01',endIsCoverageBoundary=b>'1399-12-31')))
 for row in base['records']+extra:
  k=row['key'];q=row.get('person');role=row['role'];source=row['source'];note='El título no acredita control uniforme de toda la geometría de fuente.'
  if not row.get('human'):rejected.append(dict(candidate=row,reason='Unresolved human identity or ambiguous item'));continue
  ev=next((v for v in evidence if v['candidate'].get('person')==q),dict(claims=[],fields=[]));dates=MANUAL.get((k,q))
  if k=='YUAN' and row['title']=='Khutughtu Khan Kusala':dates=[('1329-02-27','1329-08-30')];note+='Identidad específica contrastada frente a la desambiguación «Kusala»; no se elimina este breve reinado por el homónimo.'
  if not dates and k in ['PAPAL-STATES','CASTILE','JPN','BYZANTINE','ARAGON']:
   pattern=PATTERNS[k];dates=[(c['start'],c['end'][:4]+'-12-31' if c['precision']<11 else c['end']) for c in ev['claims'] if re.search(pattern,c.get('label',''),re.I)]
   if k=='BYZANTINE' and q=='Q37084':dates=None # Independently attested coronation, not the converted claim date.
  if not dates and row['parsed']:
   p=row['parsed'][INDICES.get((k,q),0)];dates=[(p['start'],p['end'])]
   if k in ['GORYEO','YUAN']:dates=[(p['start'],p['end']) for p in row['parsed']]
  if not dates:
   pattern=PATTERNS.get(k);dates=[(c['start'],c['end'][:4]+'-12-31' if c['precision']<11 else c['end']) for c in ev['claims'] if pattern and re.search(pattern,c.get('label',''),re.I)]
  if not dates:rejected.append(dict(candidate=row,reason='Office interval unresolved; not inferred from birth or death'));continue
  if k=='SCOTLAND' and q=='Q310065':continue # Exile is not effective rule in1300.
  if k=='HIST-Q12548':note+='Rey de Romanos y emperador son dignidades distintas: EnriqueVII emperador desde1312,LuisIV desde1328,CarlosIV desde1355; Wenceslao no fue emperador coronado. Los miembros conservan soberanías propias.'
  if k=='BYZANTINE':note+='Reinados interrumpidos,coemperadores y guerras civiles; no se transforma una pretensión o gobierno deTesalónica en control continuo deConstantinopla.'
  if k=='OTT':note+='Los primeros accesos otomanos tienen dataciones aproximadas; la sucesión deOsmán/Orhan se sitúa hacia1323–1326, no un día universalmente acreditado.'
  if k=='GORYEO':note+='Reinados separados cuando se documenta una restauración; no se confunden realeza deGoryeo y título deShen. Las fuentes difieren en algunos cierres intranuales1339–1344.'
  if k=='POLAND-MEDIEVAL' or k=='POLAND-KINGDOM':note+='La coronación polaca es distinta de los títulos húngaros y bohemios. La unión dinástica no anticipa laMancomunidad de1569.'
  if k=='LITHUANIA-DUCHY':note+='Gran ducado distinto de la corona polaca. La autoridad regional deVitautas desde1392 no se reduce a su reconocimiento de1401; su autonomía y las pretensiones deJogaila requieren contexto.'
  if k=='YUAN':note+='Imperio Yuan enChina; el título de gran khan no demuestra gobierno administrativo uniforme de todos los poderes mongoles. La sucesión norteña posterior a1368 tiene ficha propia.'
  if k=='ILKHANATE':note+='La crisis de1335 abre regímenes rivales y poderes regionales. Un título ilkaní no acredita control continuo de todo el contorno.'
  if k=='GOLDEN-HORDE':note+='Los poderes rivales de laGranTurbulencia no se rellenan por interpolación entre khanes.'
  if k=='MAMLUKS':note+='Restauraciones separadas; un cargo enEgipto no implica por sí solo control permanente de todas las regiones mamelucas.'
  if k=='HIST-Q184536':note+='Cronología aproximada;Musa suele fecharse1312–hacia1337. No se presenta un día exacto de acceso ni se rellena la sucesión regional por deducción.'
  if k=='JPN':note+='Cortes delNorte ySur,shogun y regenciaHōjō son funciones distintas. La titularidad y el reconocimiento retrospectivo no equivalen a control de todos los dominios.'
  if k in ['DNK','SWE','NORWAY-KINGDOM']:note+='Cada corona tiene fechas propias; la unión deKalmar comienza en1397 y no se anticipa a todo el siglo.'
  if k=='PAPAL-STATES':note+='Pontificado, no cargo previo de cardenal. Aviñón y elCisma deOccidente distinguen sede,obediencia y control territorial.'
  for a,b in dates:
   key=k;newRole=role
   if k=='POLAND-MEDIEVAL':b=min(b,'1384-12-31')
   if k=='POLAND-KINGDOM':a=max(a,'1385-01-01')
   if k=='SERBIA-KINGDOM':b=min(b,'1346-04-15')
   if k=='SERBIA-EMPIRE':a=max(a,'1346-04-16');note+='Realeza y título imperial serbio tienen fechas distintas; no se prolonga una soberanía nacional uniforme después de1371.'
   if k=='BOSNIA-BANATE':b=min(b,'1377-09-30');note+='El título de ban precede al real;Tvrtko pierde temporalmente el poder en1366–1367.'
   if k=='BOSNIA-KINGDOM':a=max(a,'1377-10-01')
   if k=='YUAN' and a>='1368-09-10':key='NORTHERN-YUAN';newRole='Emperador Yuan · poder norteño';note+='No se le atribuye por este título el gobierno deChina Ming.'
   elif k=='YUAN':b=min(b,'1368-09-09')
   if k=='GORYEO':b=min(b,'1392-12-31')
   if k=='JOS':a=max(a,'1392-01-01')
   if k=='JPN':
    if q in ['Q555520','Q471888','Q555465','Q471799'] or q=='Q123052' and a<'1392':newRole='Emperador · corte del Norte'
    if q in ['Q440447','Q464039','Q451864'] or q=='Q313942' and a>='1336':newRole='Emperador · corte del Sur'
    if 'Ashikaga' in row.get('title','') or any(c['label']=='shōgun' for c in ev['claims']) and 'Emperor' not in row['title']:newRole='Shogun Ashikaga'
   if k=='JPN' and q=='Q313942' and a.startswith('1318'):note+='El exilio y gobierno rival de1331–1333 se separan del gobierno deKioto.'
   if k=='MING':a=max(a,'1368-01-01')
   add(key,q,row['name'],newRole,a,b,source,note)
 # Same person can have different titles behind several article redirects.
 # Add only genuinely missing crown series, selecting that crown's own claims.
 seen={(r['key'],r['term']['person']) for r in accepted}
 for ev in evidence:
  row=ev['candidate'];q=row.get('person')
  if row['key'] not in ['DNK','NORWAY-KINGDOM','SWE'] or not row.get('human'):continue
  for c in ev['claims']:
   target='DNK' if 'Dinamarca' in c.get('label','') else 'NORWAY-KINGDOM' if 'Noruega' in c.get('label','') else 'SWE' if 'Suecia' in c.get('label','') else None
   if target and (target,q) not in seen:add(target,q,row['name'],c['label'],c['start'],c['end'][:4]+'-12-31' if c['precision']<11 else c['end'],row['source'],'Cargo propio de esta corona, distinto de los intervalos de las otras coronas escandinavas.')
 return dict(records=accepted,rejected=rejected,candidates=base,evidence=evidence,polityEvidence=read(ROOT/'.cache/polities023-verified.json'),scope='Partial reviewed offices and noble titles; annual synthesis, not certification of all state boundaries.')
def prepare(old,rs):
 d=copy.deepcopy(old);cs=d['countries'];images={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for k,q,n in [('WITTELSBACH-DOMAINS','','Dominios Wittelsbach · agregado'),('PUEBLO-REGIONAL','Q478805','Pueblos ancestrales · sistema regional de Aztec'),('VIKING-SETTLEMENTS','','Asentamientos nórdicos · agregado')]:cs.setdefault(k,dict(qid=q,name=n,leaders=[],flags=[]))
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for row in rs['records']:
  k=row['key'];l=copy.deepcopy(row['term']);l['acquisition']=TAG
  if l['person'] in images:l['portrait']=images[l['person']]
  cs[k]['leaders']=[o for o in cs[k]['leaders'] if not(o.get('acquisition')=='historical-0.23' and o['person']==l['person'] and o['start']<=l['end'] and o['end']>=l['start'])];cs[k]['leaders'].append(l)
 return d
if __name__=='__main__':
 p=ROOT/'scripts/historical-offices-023-research.json';rs=research() if not p.exists() or '--research' in sys.argv else read(p);save(p,rs);old=read(OUT/'identities.json');d=prepare(old,rs);assert prepare(d,rs)==d
 for k,c in old['countries'].items():assert all(l in d['countries'][k]['leaders'] for l in c['leaders'] if l.get('acquisition') not in [TAG,'historical-0.23']),k
 save(OUT/'identities.json',d);print('Reviewed office intervals',len(rs['records']),'rejected/unresolved',len(rs['rejected']))
