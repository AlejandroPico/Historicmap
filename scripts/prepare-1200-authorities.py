"""Selected offices1200–1299; freeze decisions and preserve all earlier releases."""
import pathlib,json,copy,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1200-0.24'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
PATTERNS={
 'PAPAL-STATES':'^Papa$','ARAGON':'Corona de Aragón','PRT':'rey de Portugal|monarca de Portugal','JPN':'^emperador de Japón$|^shōgun$|^Shikken$',
 'DNK':'monarca de Dinamarca','SWE':'monarca de Suecia','NORWAY-KINGDOM':'Monarca de Noruega','HESSE-UNITED':'landgrave','ELECTORATE-BRANDENBURG':'Brandeburgo',
 'BAVARIA-DUCHY':'Duque de Baviera|duke of Lower Bavaria','BOHEMIA':'Rey de Bohemia','DELHI-MAMLUK':'Sultán de Delhi','DELHI-KHALJI':'Sultán de Delhi',
 'AYYUBID':'Sultán de Egipto','MAMLUKS':'Sultán de Egipto','KHWAREZM':'Khwarazmshah','ALMOHAD':'califa almohade','ABBASID':'califa abasí',
 'ILKHANATE':'Ilkhan|^kan$','CHAGATAI':'^kan$','CHAGATAI-REGENTS':'khatun','ETH':'Emperador de Etiopía','KHM':'Rey de Camboya',
 'HIST-Q6806806':'Chola king','HIST-Q844910':'Pandya King','SAVOY-COUNTY':'conde de Saboya','EPIRUS':'Déspota de Epiro','NAPLES-KINGDOM':'rey de Nápoles',
 'SCOTLAND':'Guardián de Escocia','SECOND-BULGARIA':'Zar de Bulgaria','TREBIZOND':'emperador de Trebisonda','HIST-Q184536':'Mansa de Malí','HIST-Q140446':'Emperador de Etiopía'}
# Dates selected for the intended office, never for another crown or the lifetime.
MANUAL={
 ('CASTILE-KINGDOM','Q232323'):[('1217-06-06','1217-08-31')],
 ('LEON-KINGDOM','Q243122'):[('1230-09-24','1230-12-31')],('CASTILE','Q243122'):[('1230-09-24','1252-05-30')],
 ('ARAGON','Q312735'):[('1291-06-18','1327-11-02')],
 ('BYZANTINE','Q37076'):[('1204-01-27','1204-04-12')],('BYZANTINE','Q200033'):[('1261-07-25','1282-12-11')],
 ('NICAEA','Q200033'):[('1259-01-01','1261-07-24')],('NICAEA','Q37088'):[('1258-08-16','1261-12-25')],
 ('LATIN-EMPIRE','Q269573'):[('1228-01-01','1261-07-25')],('LATIN-EMPIRE','Q332704'):[('1231-01-01','1237-03-23')],('LATIN-EMPIRE','Q354672'):[('1217-01-01','1217-12-31')],
 ('TREBIZOND','Q452041'):[('1280-01-01','1284-12-31'),('1285-01-01','1297-08-16')],
 ('HUNGARY-KINGDOM','Q158038'):[('1270-05-03','1272-08-06')],
 ('HIST-Q12548','Q151457'):[('1198-01-01','1209-10-03'),('1209-10-04','1215-12-31')],
 ('HIST-Q12548','Q130221'):[('1212-01-01','1220-11-22'),('1220-11-23','1250-12-13')],
 ('HIST-Q12548','Q47595'):[('1257-01-01','1275-12-31')],('HIST-Q12548','Q163102'):[('1220-01-01','1235-12-31')],
 ('MONGOL-EMPIRE','Q1072396'):[('1241-12-11','1246-08-24')],('MONGOL-EMPIRE','Q2450507'):[('1248-04-20','1251-07-01')],
 ('MONGOL-EMPIRE','Q470293'):[('1260-01-01','1264-08-21')],('YUAN','Q7523'):[('1271-12-18','1294-02-18')],
 ('JIN-JURCHEN','Q5069'):[('1234-02-09','1234-02-09')],('GOLDEN-HORDE','Q982456'):[('1257-01-01','1257-12-31')],
 ('GOLDEN-HORDE','Q19489'):[('1256-01-01','1256-12-31')],
 ('DELHI-MAMLUK','Q2410810'):[('1246-01-01','1266-02-18')],('DELHI-MAMLUK','Q3826620'):[('1242-01-01','1246-12-31')],
 ('AYYUBID','Q285133'):[('1200-01-01','1218-08-31')],('AYYUBID','Q327189'):[('1250-01-01','1250-05-02')],
 ('MAMLUKS','Q327441'):[('1250-07-01','1257-12-31')],
 ('GORYEO','Q493930'):[('1197-01-01','1204-12-31')],('GORYEO','Q493946'):[('1204-01-01','1211-12-31')],('GORYEO','Q704280'):[('1211-01-01','1213-12-31')],
 ('GORYEO','Q368892'):[('1213-01-01','1259-12-31')],('GORYEO','Q493978'):[('1260-01-01','1269-12-31'),('1269-01-01','1274-07-23')],
 ('GORYEO','Q493993'):[('1274-07-23','1298-01-01'),('1298-12-31','1308-07-30')],('GORYEO','Q494012'):[('1298-01-01','1298-12-30')],
 ('GORYEO-MILITARY','Q712012'):[('1196-01-01','1219-12-31')],('GORYEO-MILITARY','Q704283'):[('1219-01-01','1249-12-31')],('GORYEO-MILITARY','Q2369258'):[('1249-01-01','1257-12-31')],('GORYEO-MILITARY','Q6811500'):[('1257-01-01','1258-12-31')],
 ('JPN','Q586532'):[('1266-01-01','1289-12-31')],('JPN','Q431052'):[('1202-01-01','1203-12-31')],
 ('HESSE-UNITED','Q76968'):[('1264-01-01','1308-12-21')],
 ('SAXONY-DUCHY','Q565737'):[('1180-01-01','1212-02-02')],('SAXONY-DUCHY','Q674931'):[('1212-01-01','1260-12-31')],('SAXONY-DUCHY','Q661181'):[('1260-01-01','1296-12-31')],
 ('SAXONY-ELECTORATE','Q661181'):[('1296-01-01','1298-12-31')],
 ('ELECTORATE-BRANDENBURG','Q706797'):[('1184-01-01','1205-07-04')],('ELECTORATE-BRANDENBURG','Q641895'):[('1220-01-01','1266-12-31')],('ELECTORATE-BRANDENBURG','Q672163'):[('1220-01-01','1267-12-31')],('ELECTORATE-BRANDENBURG','Q62568'):[('1266-01-01','1308-12-31')],
 ('SICILY-KINGDOM','Q130221'):[('1198-01-01','1250-12-13')],('SICILY-KINGDOM','Q157179'):[('1250-12-13','1254-05-21')],('SICILY-KINGDOM','Q158246'):[('1254-05-21','1258-12-31')],('SICILY-KINGDOM','Q164889'):[('1258-01-01','1266-02-26')],
 ('SICILY-KINGDOM','Q203829'):[('1266-01-01','1282-12-31')],('SICILY-KINGDOM','Q312311'):[('1282-09-04','1285-11-01')],('SICILY-KINGDOM','Q312735'):[('1285-11-02','1295-06-20')],('SICILY-KINGDOM','Q367226'):[('1295-01-01','1337-12-31')],
 ('NAPLES-KINGDOM','Q203829'):[('1282-01-01','1285-01-07')],
 ('EPIRUS','Q441429'):[('1205-01-01','1215-12-31')],('EPIRUS','Q371668'):[('1215-01-01','1230-12-31')],('EPIRUS','Q729407'):[('1230-01-01','1268-12-31')],
 ('HIST-Q863279','Q887310'):[('1238-01-01','1270-12-31')],('HIST-Q863279','Q2881860'):[('1270-01-01','1279-12-31')],('HIST-Q863279','Q349249'):[('1279-01-01','1298-12-31')],
 ('HIST-Q844910','Q3536291'):[('1250-01-01','1268-12-31')],('HIST-Q844910','Q6755090'):[('1268-01-01','1308-12-31')],
 ('ENGLAND','Q348911'):[('1216-01-01','1219-12-31')],
 ('SERBIA-KINGDOM','Q290786'):[('1276-01-01','1282-12-31')],('HIST-Q12548','Q121130'):[('1198-09-15','1208-06-21')],('MONGOL-EMPIRE','Q7517'):[('1227-08-25','1229-09-13')],
 ('SAXONY-DUCHY','Q567387'):[('1260-01-01','1282-12-31')],
}
NOTES={
 'HIST-Q12548':'Rey de Romanos, emperador coronado y candidatos rivales son dignidades distintas. Los territorios imperiales no pertenecen todos a un Estado nacional único.',
 'MONGOL-EMPIRE':'Regencias y pretensiones rivales conservan su función. Después de1260 el título de gran khan no demuestra administración uniforme de todos los kanatos.',
 'YUAN':'La proclamación dinástica de1271 es distinta del acceso deKublai al título de gran khan en1260 y de la conquista final Song de1279.',
 'NICAEA':'Poder imperial en el exilio, separado del gobierno latino deConstantinopla. JuanIV mantiene titularidad hasta su deposición en1261; no gobierna como adulto todo el contorno.',
 'LATIN-EMPIRE':'Gobierno deConstantinopla limitado a1204–1261. Títulos posteriores en exilio no equivalen a control territorial. PedroII nunca llegó a gobernar en la capital; su datación final presenta variantes.',
 'BYZANTINE':'Sin continuidad de gobierno enConstantinopla durante1204–1261. Recaptura de la ciudad y entrada ceremonial deMiguelVIII tienen fechas distintas.',
 'TREBIZOND':'Serie distinta deConstantinopla; JuanII yTeodora alternan el poder hacia1284–1285.',
 'GORYEO':'Realeza, gobierno militar y dependencia mongola no son el mismo cargo. Restauraciones y el breve gobierno rival de1269 se distinguen; precisión anual, no calendario diario certificado.',
 'GORYEO-MILITARY':'Dirigencia militar bajo la monarquía deGoryeo, no un título real ni un Estado distinto. Intervalos anuales; la serie de regímenes militares posteriores continúa incompleta.',
 'JPN':'Emperador,shogun yshikken son cargos distintos. No se transforma una regenciaHōjō en un shogunato propio ni un emperador depuesto en monarca activo.',
 'SICILY-KINGDOM':'El reino deSicilia no equivale a los títulos imperiales o deJerusalén del mismo soberano. Desde1282 distinguir la isla, el continente angevino y las pretensiones rivales.',
 'NAPLES-KINGDOM':'Fase continental después de lasVísperas Sicilianas; no implica gobierno sobre la isla disputada.',
 'HESSE-UNITED':'Ventana conservadora de reconocimiento efectivo desde1264. Las pretensiones sucesorias de1247 y el reconocimiento de príncipe imperial en1292 son hitos distintos.',
 'SAXONY-DUCHY':'Dominio ascanio reducido y cogobiernos; no todo el antiguo ducado raíz ni todas las ramas sajonas son un territorio nacional uniforme.',
 'SAXONY-ELECTORATE':'Rama deSajonia-Wittenberg desde la división de1296; no se anticipa a todo el siglo la regulación electoral de1356.',
 'BAVARIA-DUCHY':'Tras1255 distinguir las ramas deAlta yBaja Baviera; sus titulares no gobiernan cada uno toda la geometría agregada.',
 'ELECTORATE-BRANDENBURG':'Margraves y ramas corregentes; no reino dePrusia ni gobierno de todas las posesiones ascanias.',
 'HIST-Q863279':'Cronología deSukhothai aproximada; se distingue el reinado deRamkhamhaeng desde1279 de sus fechas personales. Hay variantes en los primeros accesos.',
 'HIST-Q140446':'Cronología Zagüe con variantes importantes; las fechas de esta serie son una tradición documental, no una datación absoluta independiente.',
 'HIST-Q184536':'Cronología temprana deMalí aproximada y dependiente de tradiciones y crónicas; no se deducen fechas diarias de las biografías.',
 'PAPAL-STATES':'Pontificado distinto del cardenalato, elección y consagración pueden tener fechas distintas. Sede vacante no se rellena con otro titular.',
 'ARAGON':'Cargo aragonés distinto del siciliano; unión dinástica no significa gobierno único de todas las coronas.',
 'ENGLAND':'Rey y regente conservan funciones distintas. El reinado francés deLuisVIII no se utiliza como período de rey inglés.',
}

def research():
 base=read(ROOT/'.cache/rulers024-candidates.json');evidence=read(ROOT/'.cache/rulers024-office-evidence.json');rows=list(base['records']);seen={(r['key'],r.get('person'),r['title'])for r in rows}
 for v in evidence:
  r=v['candidate'];sig=(r['key'],r.get('person'),r['title'])
  if sig not in seen:rows.append(r);seen.add(sig)
 accepted=[];rejected=[];dedup=set()
 def add(k,row,role,a,b,note):
  if a>'1299-12-31' or b<'1200-01-01' or a>b:return
  first,last=max(a,'1200-01-01'),min(b,'1299-12-31');sig=(k,row['person'],role,first,last)
  if sig in dedup:return
  dedup.add(sig)
  clean=lambda s:re.sub(r'(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ0-9])',' ',s)
  accepted.append(dict(key=k,term=dict(person=row['person'],name=row.get('name',row['title']),role=clean(role),start=first,end=last,precision=9,source=row['source'],curated=True,acquisition=TAG,note=clean(note)+' Síntesis anual; calendario histórico y dominio territorial no certificados día a día.',startIsCoverageBoundary=a<'1200-01-01',endIsCoverageBoundary=b>'1299-12-31')))
 for row in rows:
  k=row['key'];q=row.get('person');role=row['role'];note=NOTES.get(k,'La dignidad no acredita control uniforme de toda la geometría de fuente.')
  if not row.get('human') or (k,q)==('MAMLUKS','Q602993'):
   rejected.append(dict(candidate=row,reason='Unresolved/nonhuman identity or homonymous Mongol commander, not the Mamluk sultan'));continue
  ev=next((v for v in evidence if v['candidate'].get('person')==q),dict(claims=[]));dates=MANUAL.get((k,q));pattern=PATTERNS.get(k)
  if not dates and pattern:
   dates=list(dict.fromkeys((c['start'],c['end'][:4]+'-12-31'if c['precision']<11 else c['end'])for c in ev['claims']if re.search(pattern,c.get('label',''),re.I)))
  if not dates and row.get('parsed'):
   pars=row['parsed'];dates=[(pars[0]['start'],pars[0]['end'])]
   if k=='BYZANTINE'and q=='Q37135':dates=[(p['start'],p['end'])for p in pars]
  if not dates:
   # Explicit single-day Jin accession is not obtained from a person's lifetime.
   rejected.append(dict(candidate=row,reason='Intended office dates unresolved; not inferred from birth/death or a different title'));continue
  for index,(a,b)in enumerate(dates):
   key=k;actualRole=role
   if k=='CASTILE-KINGDOM':b=min(b,'1229-12-31')
   if k=='LEON-KINGDOM':b=min(b,'1230-12-31')
   if k=='CASTILE':a=max(a,'1230-01-01')
   if k=='SERBIA-KINGDOM'and q=='Q24445':
    add('SERBIA-PRINCIPALITY',row,'Gran príncipe de Serbia','1196-01-01','1202-12-31','Gobierno anterior a la coronación;interrupción porVukan hacia1202–1204.');add('SERBIA-PRINCIPALITY',row,'Gran príncipe de Serbia','1204-01-01','1216-12-31','Restauración anterior a la coronación real de1217.');a=max(a,'1217-01-01')
   if k=='SERBIA-KINGDOM'and q=='Q290786':a,b='1276-01-01','1282-12-31'
   if k=='BYZANTINE':
    if a<'1204-04-13':b=min(b,'1204-04-12')
    else:a=max(a,'1261-07-25')
   if k=='LATIN-EMPIRE':a=max(a,'1204-04-13');b=min(b,'1261-07-25')
   if k=='LATIN-EMPIRE'and q=='Q232147':actualRole='Regente del Imperio latino'
   if k=='LATIN-EMPIRE'and q=='Q354672':actualRole='Emperador elegido · sin gobierno en Constantinopla'
   if k=='LATIN-EMPIRE'and q=='Q332704':actualRole='Coemperador y regente latino'
   if k=='HIST-Q12548':
    actualRole='Rey de Romanos · pretensión rival'if q in ['Q47595','Q121130','Q77255']else'Rey de Romanos'
    if q=='Q151457'and a>='1209-10-04'or q=='Q130221'and a>='1220-11-23':actualRole='Emperador del Sacro Imperio'
   if k=='MONGOL-EMPIRE'and q in ['Q1072396','Q2450507','Q7517']:actualRole='Regente del Imperio mongol'
   if k=='MONGOL-EMPIRE'and q=='Q470293':actualRole='Gran khan · pretensión rival'
   if k=='MONGOL-EMPIRE':a=max(a,'1206-01-01')
   if k=='YUAN':a=max(a,'1271-12-18')
   if k=='GOLDEN-HORDE':a=max(a,'1242-01-01')
   if k=='ILKHANATE':a=max(a,'1256-01-01')
   if k=='DELHI-MAMLUK':a=max(a,'1206-01-01');b=min(b,'1290-06-13')
   if k=='DELHI-KHALJI':a=max(a,'1290-06-13')
   if k=='ETH':a=max(a,'1270-01-01')
   if k=='GORYEO-MILITARY':key='GORYEO'
   if k=='CHAGATAI-REGENTS':key='CHAGATAI';actualRole='Regente del kanato de Chagatai'
   if k=='JPN':
    if re.search('Shikken',role)or any(c['label']=='Shikken'for c in ev['claims']):actualRole='Shikken Hōjō · regente de Kamakura'
    elif 'Shogun'in role:actualRole='Shogun de Kamakura'
   if k=='BAVARIA-DUCHY'and q=='Q61467'and a>='1253':actualRole='Duque de Alta Baviera desde1255'
   if k=='BAVARIA-DUCHY'and q=='Q61154':actualRole='Duque de Baja Baviera desde1255'
   if k=='HESSE-UNITED':row={**row,'source':'https://hessen.de/wissen/geschichte-des-landes/die-geburtsstunde-des-landes-hessen'}
   add(key,row,actualRole,a,b,note)
 return dict(records=accepted,rejected=rejected,candidates=base,evidence=evidence,seeds=read(ROOT/'.cache/seeds024.json'),polityEvidence=read(ROOT/'.cache/polities024-verified.json'),scope='Selected office and title evidence1200–1299; partial series, rival claims and source chronology defects remain explicit.')

def prepare(old,rs):
 d=copy.deepcopy(old);cs=d['countries'];images={l['person']:l['portrait']for c in cs.values()for l in c['leaders']if l.get('portrait')}
 seeds=dict(rs['seeds'])
 seeds.update({'SAXONY-DUCHY':('Q164092','Ducado de Sajonia · dominios ascanios'),'SERBIA-PRINCIPALITY':('Q1311990','Gran Principado de Serbia'),'NAPLES-KINGDOM':('Q173065','Reino de Nápoles')})
 for k,(q,name)in seeds.items():cs.setdefault(k,dict(qid=q,name=name,leaders=[],flags=[]))
 for c in cs.values():c['leaders']=[l for l in c['leaders']if l.get('acquisition')!=TAG]
 for row in rs['records']:
  k=row['key'];l=copy.deepcopy(row['term'])
  if l['person']in images:l['portrait']=images[l['person']]
  cs[k]['leaders']=[v for v in cs[k]['leaders']if not(v.get('acquisition')=='historical-0.24'and v['person']==l['person']and v['start']<=l['end']and v['end']>=l['start'])];cs[k]['leaders'].append(l)
 return d
if __name__=='__main__':
 p=ROOT/'scripts/historical-offices-024-research.json';rs=research()if not p.exists()or'--research'in sys.argv else read(p);save(p,rs);old=read(OUT/'identities.json');d=prepare(old,rs);assert prepare(d,rs)==d
 for k,c in old['countries'].items():assert all(l in d['countries'][k]['leaders']for l in c['leaders']if l.get('acquisition')not in[TAG,'historical-0.24']),k
 save(OUT/'identities.json',d);print('Reviewed office intervals',len(rs['records']),'unresolved/rejected',len(rs['rejected']))
