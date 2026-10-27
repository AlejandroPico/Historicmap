"""Freeze selected1000–1099 offices from dated claims and explicit reign fields."""
import pathlib,json,copy,re,calendar,importlib.util,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1000-0.26'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
ALIASES={'GREAT-SELJUK':'HIST-Q3708094','ALMORAVID':'HIST-Q75613','JERUSALEM':'HIST-Q55502','ANTIOCH':'HIST-Q235030','GEORGIA-MEDIEVAL':'HIST-Q154667','KIEVAN-RUS':'HIST-Q1108445','NOVGOROD':'HIST-Q151536','JPN-INSEI':'JPN','JPN-REGENTS':'JPN'}
SEEDS={'BUYID':('Q273874','Poderes buyíes'),'CASTILE-COUNTY':('Q179293','Condado de Castilla · fase anterior a1065'),'NORMANDY-DUCHY':('Q842091','Ducado de Normandía'),'SICILY-COUNTY':('Q1917014','Condado de Sicilia'),'HIST-Q171740':('Q171740','Califato de Córdoba'),'HIST-Q203817':('Q203817','Primer Imperio búlgaro'),'HIST-Q2622868':('Q2622868','Armenia bagrátida')}
PATTERNS={
 'FRA':'rey de Francia|rey de los francos','ENGLAND':'monarca de Inglaterra','SCOTLAND':'monarca de Escocia|rey de Escocia','LEON-KINGDOM':'monarca del Reino de León|rey de León','CASTILE-COUNTY':'conde de Castilla','CASTILE-KINGDOM':'monarca del Reino de Castilla',
 'ARAGON-KINGDOM':'monarca del reino de Aragón','NAVARRE-KINGDOM':'Rey de Pamplona|monarca del Reino de Navarra|rey de Navarra','BARCELONA-COUNTY':'conde de Barcelona','PORTUGAL-COUNTY':'conde de Portugal',
 'BOHEMIA-DUCHY':'Duque de Bohemia','BOHEMIA':'Rey de Bohemia','SAXONY-STEM':'duque de Sajonia','BAVARIA-DUCHY':'Duque de Baviera','HUNGARY-KINGDOM':'rey de Hungría|Rey Apostólico de Hungría',
 'DNK':'monarca de Dinamarca','NORWAY-KINGDOM':'monarca de Noruega|rey de Noruega','SWE':'monarca de Suecia','PAPAL-STATES':'^Papa$',
 'BYZANTINE':'emperador bizantino|emperatriz bizantina','NORTHERN-SONG':'Emperador de China','LIAO':'Emperador de China','WESTERN-XIA':'^emperador$|Emperador de China','JPN':'^emperador de Japón$','JPN-REGENTS':'^kanpaku$|^sesshō$',
 'FATIMID':'califa fatimí','ABBASID':'califa abasí','HIST-Q3708094':'Sultán del Imperio selyúcida|^sultán$','SELJUK-RUM':'Sultán de Rum','HIST-Q75613':'emir almorávide',
 'HIST-Q154667':'King of Georgia|Reino de Georgia','HIST-Q1108445':'Príncipe de Kiev','HIST-Q6806806':'Chola king','KHM':'Rey de Camboya','HIST-Q888574':'King of Burma','CILICIA-PRINCIPALITY':'príncipe de Armenia','SAVOY-COUNTY':'conde de Saboya|count of Maurienna',
 'NORMANDY-DUCHY':'duque de Normandía','SICILY-COUNTY':'conde de Sicilia','HIST-Q171740':'Califa de Córdoba','HIST-Q203817':'zar de Bulgaria','HIST-Q2622868':'rey de Armenia',
}
PATTERNS['HIST-Q12844800']='Sultan of the Ghaznavid Empire'
# Regnal dates, title phases and restorations selected explicitly for this office.
MANUAL={
 ('ENGLAND','Æthelred the Unready'):[('0978','1013'),('1014','1016-04-23')],('ENGLAND','Edmund Ironside'):[('1016-04-23','1016-11-30')],('ENGLAND','Harold Harefoot'):[('1035','1040-03-17')],('ENGLAND','Harold Godwinson'):[('1066-01-05','1066-10-14')],('ENGLAND','Edgar Ætheling'):[('1066-10-15','1066-12-24')],('ENGLAND','William the Conqueror'):[('1066-12-25','1087-09-09')],
 ('LEON-KINGDOM','Alfonso VI of León and Castile'):[('1065','1072-01-01'),('1072-10-13','1109-07-01')],('LEON-KINGDOM','Sancho II of Castile and León'):[('1072-01-01','1072-10-07')],
 ('CASTILE-COUNTY','Sancho García of Castile'):[('0995','1017')],('CASTILE-COUNTY','Ferdinand I of León'):[('1029','1065')],
 ('HIST-Q12548','Otto III, Holy Roman Emperor'):[('0996-05-21','1002-01-23')],('HIST-Q12548','Henry II, Holy Roman Emperor'):[('1002-06-07','1014-02-13'),('1014-02-14','1024-07-13')],('HIST-Q12548','Conrad II, Holy Roman Emperor'):[('1024-09-08','1027-03-25'),('1027-03-26','1039-06-04')],('HIST-Q12548','Henry III, Holy Roman Emperor'):[('1028-04-14','1046-12-24'),('1046-12-25','1056-10-05')],('HIST-Q12548','Henry IV, Holy Roman Emperor'):[('1054','1083-12-31'),('1084','1105-12-31')],('HIST-Q12548','Rudolf of Rheinfelden'):[('1077','1080')],('HIST-Q12548','Hermann of Salm'):[('1081','1088')],
 ('JPN-INSEI','Emperor Shirakawa'):[('1087-01-03','1129')],
 ('BOHEMIA-DUCHY','Vratislaus II of Bohemia'):[('1061','1084-12-31')],('BOHEMIA','Vratislaus II of Bohemia'):[('1085','1092')],
 ('HIST-Q55502','Godfrey of Bouillon'):[('1099-07-22','1100-07-18')],('EDESSA','Baldwin I of Jerusalem'):[('1098','1100')],('HIST-Q235030','Bohemond I of Antioch'):[('1098','1111')],
}
MANUAL.update({
 ('BYZANTINE','Zoe Porphyrogenita'):[('1042-04-21','1042-06-11'),('1028','1041'),('1042-06-11','1050')],
 ('BYZANTINE','Theodora Porphyrogenita'):[('1042-04-21','1042-06-11'),('1042-06-11','1055-01-10'),('1055-01-11','1056-08-31')],
 ('BYZANTINE','Eudokia Makrembolitissa'):[('1067-05-23','1067-12-31'),('1071-10-01','1071-11-01')],
 ('BYZANTINE','Michael VII Doukas'):[('1067-05-22','1071-09-30'),('1071-10-01','1078-03-31')],
 ('POLAND-MEDIEVAL','Bolesław I the Brave'):[('0992','1024'),('1025','1025')],
 ('POLAND-MEDIEVAL','Mieszko II Lambert'):[('1025','1031'),('1032','1034')],
 ('POLAND-MEDIEVAL','Bolesław II the Bold'):[('1058','1075'),('1076','1079')],
 ('CILICIA-PRINCIPALITY','Constantine I, Prince of Armenia'):[('1095','1100')],
})
MANUAL[('JPN-REGENTS','Fujiwara no Yorimichi')]=[('1017','1019'),('1020','1068')]
MANUAL[('GORYEO','Mokjong of Goryeo')]=[('0997','1009-03-02')]
MANUAL[('HIST-Q171740','Hisham III of Córdoba')]=[('1027','1031')]
NOTES={
 'ENGLAND':'Restauraciones, conquista y pretensiones tienen intervalos propios. Edgar fue elegido/pretendiente sin coronación; no gobernó todaInglaterra. Los reinados danés, inglés y noruego de un mismo monarca no comienzan simultáneamente.',
 'HIST-Q12548':'Realeza germánica/deRomanos, corregencia y coronación imperial son dignidades distintas. EnriqueIII fue corregente antes de1039 yEnriqueIV antes de1056. Candidatos rivales no controlan todo el agregado imperial.',
 'CASTILE-COUNTY':'Condado y realeza leonesa deFernando son funciones distintas. La historiografía presenta variantes para el origen del título castellano; se usa una fase condal conservadora antes del reino separado de1065.',
 'LEON-KINGDOM':'Sucesión leonesa distinta de la castellana; restauración deAlfonsoVI e incorporación deGalicia yToledo no se convierten en un solo acceso uniforme.',
 'NAVARRE-KINGDOM':'Pamplona yAragón conservan dignidades distintas. Las cronologías deGarcíaSánchezII ySanchoIII presentan variantes hacia1000–1004.',
 'BYZANTINE':'Emperatrices, emperadores y regentes tienen funciones distintas. La deposición no prolonga un gobierno efectivo ni el título hereditario demuestra control de todo el contorno.',
 'JPN':'Emperador reinante, regentesFujiwara y gobierno de claustro desde1086 son funciones distintas. No se anticipa el shogunato deKamakura.',
 'GORYEO':'Reinados y soberanos retirados se distinguen. La regencia militar de1170 no se anticipa al sigloXI; fechas de precisión anual y variantes de calendario declaradas.',
 'HIST-Q171740':'Califas, autoridades amiríes y poderes rivales de lafitna no equivalen a control uniforme del califato. Su abolición de1031 no se prolonga en las taifas.',
 'HIST-Q2622868':'Reino bagrátida, ramas armenias y posterior principado deCilicia son entidades distintas. La conquista deAni de1045 no se convierte en continuidad territorial deCilicia.',
 'HIST-Q3708094':'Soberanía selyúcida y gobiernos regionales tienen ámbitos distintos; no se atribuye la misma fecha a todas las campañas y territorios.',
 'HIST-Q12844800':'Dinastía gaznávida, soberanos y control territorial no son idénticos; la derrota deDandanaqan de1040 no extingue inmediatamente todos sus dominios.',
 'POLAND-MEDIEVAL':'Duque, rey coronado y gobierno restaurado son dignidades distintas. Las crisis de1031–1039 no se rellenan con un monarca continuo ni la coronación de1025 se anticipa a992.',
}
FIELD_PATTERNS={
 'FRA':'King.*Franc|King.*France|King.*Frank','ENGLAND':'King.*Engl|English throne','SCOTLAND':'King.*Alba|King.*Scot','LEON-KINGDOM':'King.*Le[oó]n','CASTILE-COUNTY':'Count.*Castile','CASTILE-KINGDOM':'King.*Castile','NAVARRE-KINGDOM':'King.*Pamplona|King.*Navarre','ARAGON-KINGDOM':'King.*Aragon',
 'BARCELONA-COUNTY':'Count.*Barcelona','PORTUGAL-COUNTY':'Count.*Portugal','BOHEMIA-DUCHY':'Duke.*Bohemia','BOHEMIA':'King.*Bohemia','SAXONY-STEM':'Duke.*Saxony','BAVARIA-DUCHY':'Duke.*Bavaria','NORMANDY-DUCHY':'Duke.*Normandy','SICILY-COUNTY':'Count.*Sicily','SAVOY-COUNTY':'Count.*Savoy',
 'DNK':'King.*Denmark','NORWAY-KINGDOM':'King.*Norway','SWE':'King.*Sweden','HUNGARY-KINGDOM':'King.*Hungary','GORYEO':'King.*Goryeo','JPN':'Emperor.*Japan','JPN-REGENTS':'Kampaku|Kanpaku|Sessh',
 'HIST-Q203817':'Emperor.*Bulgaria','HIST-Q2622868':'King.*Armenia','POLAND-MEDIEVAL':'King.*Poland|Duke.*Poland',
}
def research():
 spec=importlib.util.spec_from_file_location('g',ROOT/'scripts/review-026-rulers.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 evidence=read(ROOT/'.cache/rulers026-office-evidence.json');fields=read(ROOT/'.cache/rulers026-reign-evidence.json');accepted=[];rejected=[];seen=set()
 def add(k,row,role,a,b,note,ev):
  a=a+'-01-01'if len(a)==4 else a;b=b+'-12-31'if len(b)==4 else b
  if a>b or a>'1099-12-31'or b<'1000-01-01':return
  first,last=max(a,'1000-01-01'),min(b,'1099-12-31');k=ALIASES.get(k,k);sig=(k,row['person'],role,first,last)
  if sig in seen:return
  seen.add(sig);clean=lambda s:re.sub(r'(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ0-9])',' ',s)
  accepted.append(dict(key=k,term=dict(person=row['person'],name=row.get('name',row['requestedTitle']),role=clean(role),start=first,end=last,precision=9,source=row['source'],curated=True,acquisition=TAG,note=clean(note)+' Síntesis anual; no calendario diario ni certificación de todo el contorno.',startIsCoverageBoundary=a<'1000-01-01',endIsCoverageBoundary=b>'1099-12-31'),selectionEvidence=ev))
 for k,role,titles in g.GROUPS:
  for title in titles:
   e=next((e for e in evidence if title in[e['candidate'].get('requestedTitle'),e['candidate'].get('title')]),None)
   if not e or not e['candidate'].get('human'):rejected.append(dict(key=k,title=title,reason='Canonical human identity unresolved/nonhuman'));continue
   row=e['candidate'];q=row['person'];note=NOTES.get(ALIASES.get(k,k),'La dignidad documentada no acredita dominio uniforme de todo el contorno de fuente.');manual=MANUAL.get((k,title));dates=[]
   if manual:dates=[(a,b,'Explicit office-phase review')for a,b in manual]
   elif PATTERNS.get(k):
    for c in e['claims']:
     if re.search(PATTERNS[k],c.get('label',''),re.I):
      end=c['end'][:4]+'-12-31'if c['precision']==9 and c['end'].endswith('-01-01')else c['end']
      dates.append((c['start'],end,c))
   if not dates:
    f=next((f for f in fields if f.get('person')==q),{})
    for z in f.get('reignFields',[]):
     office=re.sub('<[^>]*>','',z.get('office',''));pattern=FIELD_PATTERNS.get(k)
     if z['parsed']and(pattern is None or re.search(pattern,office,re.I))and not re.search('Retired|Taishang|Emeritus',office,re.I):dates.append((z['parsed']['start'],z['parsed']['end'],z))
   if not dates:rejected.append(dict(key=k,title=title,person=q,reason='Intended office dates unresolved, not inferred from lifetime or another crown'));continue
   for index,(a,b,ev)in enumerate(dates):
    actual=role
    if k=='JPN-REGENTS'and title=='Fujiwara no Yorimichi':actual='Sesshō Fujiwara · regente'if index==0 else'Kanpaku Fujiwara · regente'
    if k=='BYZANTINE'and title=='Zoe Porphyrogenita':actual='Emperatriz reinante · con Teodora'if index==0 else'Emperatriz consorte / Augusta'
    if k=='BYZANTINE'and title=='Theodora Porphyrogenita':actual='Coemperatriz'if index==1 else'Emperatriz reinante'
    if k=='BYZANTINE'and title=='Eudokia Makrembolitissa':actual='Emperatriz regente'
    if k=='BYZANTINE'and title=='Michael VII Doukas':actual='Coemperador · bajo regencia y régimen de RomanoIV'if index==0 else'Emperador bizantino'
    if k=='POLAND-MEDIEVAL':actual='Rey de Polonia'if title=='Bolesław I the Brave'and index==1 or title=='Mieszko II Lambert'and index==0 or title=='Bolesław II the Bold'and index==1 else'Duque de Polonia'
    if k=='HIST-Q12548':actual='Rey de Romanos · candidato rival'if title in['Rudolf of Rheinfelden','Hermann of Salm']else'Emperador del Sacro Imperio'if title.startswith('Otto III')or index==1 else'Rey germánico / de Romanos'
    if k=='ENGLAND'and title=='Edgar Ætheling':actual='Elegido / pretendiente · sin coronación'
    if k=='BOHEMIA-DUCHY'and title=='Vratislaus II of Bohemia':b=min(b,'1084-12-31')
    if k=='BOHEMIA':a=max(a,'1085-01-01')
    if k=='CASTILE-COUNTY':b=min(b,'1065-12-31')
    if k=='CASTILE-KINGDOM':a=max(a,'1065-01-01')
    if k=='ARAGON-KINGDOM':a=max(a,'1035-01-01')
    if k=='HUNGARY-KINGDOM':a=max(a,'1000-01-01')
    if k=='WESTERN-XIA':a=max(a,'1038-01-01')
    if k=='HIST-Q171740':b=min(b,'1031-12-31')
    if k=='CILICIA-PRINCIPALITY':a=max(a,'1080-01-01')
    if k=='HIST-Q203817':b=min(b,'1018-12-31')
    add(k,row,actual,a,b,note,ev)
 return dict(records=accepted,rejected=rejected,seeds=SEEDS,aliases=ALIASES,evidence=evidence,reignEvidence=fields,polityEvidence=read(ROOT/'.cache/polities026-verified.json'),scope='Selected1000–1099 offices, partial series, explicit regnal fields and chronology variants. No invented daily territorial control.')
def prepare(old,rs):
 d=copy.deepcopy(old);cs=d['countries'];images={l['person']:l['portrait']for c in cs.values()for l in c['leaders']if l.get('portrait')}
 for alias,target in rs['aliases'].items():
  if alias in cs and alias!=target and target in cs and not cs[alias]['flags']and all(l.get('acquisition')in[TAG,'historical-0.26']for l in cs[alias]['leaders']):cs[target]['leaders'].extend(cs[alias]['leaders']);del cs[alias]
 for k,(q,name)in rs['seeds'].items():cs.setdefault(k,dict(qid=q,name=name,leaders=[],flags=[]))
 for k,end in {'HIST-Q171740':'1031-12-31','HIST-Q203817':'1018-12-31','HIST-Q2622868':'1045-12-31'}.items():
  if k not in cs:continue
  terms=[]
  for l in cs[k]['leaders']:
   if l.get('acquisition')=='historical-0.26':
    if l['start']>end:continue
    if l['end']>end:l={**l,'end':end,'note':'Título de fuente limitado al final del gobierno territorial; no se prolonga una pretensión posterior como control efectivo.'}
   terms.append(l)
  cs[k]['leaders']=terms
 for c in cs.values():c['leaders']=[l for l in c['leaders']if l.get('acquisition')!=TAG]
 for r in rs['records']:
  k=r['key'];l=copy.deepcopy(r['term']);assert k in cs,k
  if l['person']in images:l['portrait']=images[l['person']]
  cs[k]['leaders']=[v for v in cs[k]['leaders']if not(v.get('acquisition')=='historical-0.26'and v['person']==l['person']and v['start']<=l['end']and v['end']>=l['start'])];cs[k]['leaders'].append(l)
 return d
if __name__=='__main__':
 p=ROOT/'scripts/historical-offices-026-research.json';rs=research()if not p.exists()or'--research'in sys.argv else read(p);save(p,rs);old=read(OUT/'identities.json');d=prepare(old,rs);assert prepare(d,rs)==d
 for k,c in old['countries'].items():
  if k in d['countries']:assert all(l in d['countries'][k]['leaders']for l in c['leaders']if l.get('acquisition')not in[TAG,'historical-0.26']),k
 save(OUT/'identities.json',d);print('Selected office intervals',len(rs['records']),'not selected/unresolved',len(rs['rejected']))
