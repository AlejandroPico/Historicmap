"""Freeze reviewed offices1100–1199; preserve earlier facts and entity continuity."""
import pathlib,json,copy,re,sys,ast,importlib.util,calendar
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1100-0.25'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
ALIASES={'QARA-KHITAI':'HIST-Q862304','GREAT-SELJUK':'HIST-Q3708094','ZENGID':'HIST-Q189545','ALMORAVID':'HIST-Q75613','JERUSALEM':'HIST-Q55502','ANTIOCH':'HIST-Q235030','TRIPOLI':'HIST-Q272033','GHURID':'HIST-Q199443','GEORGIA-MEDIEVAL':'HIST-Q154667','KIEVAN-RUS':'HIST-Q1108445','NOVGOROD':'HIST-Q151536','BOHEMIA-DUCHY-CORRECTION':'BOHEMIA-DUCHY','JPN-MILITARY':'JPN','JPN-INSEI':'JPN','GORYEO-MILITARY':'GORYEO','FATIMID-VIZIER':'FATIMID'}
PATTERNS={'PAPAL-STATES':'^Papa$','DNK':'monarca de Dinamarca','NORWAY-KINGDOM':'Monarca de Noruega','SWE':'monarca de Suecia','BOHEMIA-DUCHY':'Duque de Bohemia','BOHEMIA-DUCHY-CORRECTION':'Duque de Bohemia','BOHEMIA':'Rey de Bohemia','SAXONY-STEM':'duque de Sajonia','SAXONY-DUCHY':'duque de Sajonia','BAVARIA-DUCHY':'Duque de Baviera','ELECTORATE-BRANDENBURG':'margrave de Brandeburgo','FRA':'rey de Francia','PRT':'rey de Portugal|monarca de Portugal','JPN':'^emperador de Japón$','AYYUBID':'Sultán de Egipto','FATIMID':'califa fatimí','ABBASID':'califa abasí','SELJUK-RUM':'Sultán de Rum','ALMOHAD':'califa almohade','SAVOY-COUNTY':'conde de Saboya','NORTHERN-SONG':'Emperador de China','SOUTHERN-SONG':'Emperador de China','JIN-JURCHEN':'Emperador de China','KHWAREZM':'Khwarazmshah','SICILY-KINGDOM':'Rey de Sicilia','HUNGARY-KINGDOM':'rey de Hungría'}
PATTERNS.update({'TRIPOLI':'conde de Tripoli','NORWAY-KINGDOM':'Monarca de Noruega|rey de Noruega','ALMORAVID':'emir almorávide','LIAO':'Emperador de China','QARA-KHITAI':'^emperador$|^regente$','WESTERN-XIA':'^emperador$','GHURID':'^sultán$','HIST-Q6806806':'Chola king','HIST-Q18211496':'^rey$','HIST-Q466581':'Hoysala king','KHM':'Rey de Camboya','HIST-Q888574':'King of Burma','KIEVAN-RUS':'Príncipe de Kiev','FATIMID-VIZIER':'visir del Califato Fatimí','GEORGIA-MEDIEVAL':'King of Georgia|Reino de Georgia','ELECTORATE-BRANDENBURG':'margrave de Brandeburgo|marqués de Brandeburgo'})
# Each override refers to the intended office, not the sovereign's lifetime or another crown.
MANUAL={
 ('CASTILE-KINGDOM','Q235080'):[('1072','1109-07-01')],('LEON-KINGDOM','Q235080'):[('1072','1109-07-01')],
 ('CASTILE-KINGDOM','Q128701'):[('1109-07-01','1126-03-08')],('LEON-KINGDOM','Q128701'):[('1109-07-01','1126-03-08')],
 ('CASTILE-KINGDOM','Q312767'):[('1126-03-08','1157-08-21')],('LEON-KINGDOM','Q312767'):[('1126-03-08','1157-08-21')],
 ('PORTUGAL-COUNTY','Q319625'):[('1096','1112')],('PORTUGAL-COUNTY','Q237987'):[('1112','1128')],('PORTUGAL-COUNTY','Q587697'):[('1112-05-22','1139-07-25')],('PRT','Q587697'):[('1139-07-26','1185-12-06')],
 ('ARAGON-KINGDOM','Q379748'):[('1094','1104-09-28')],('ARAGON-KINGDOM','Q81833'):[('1104-09-28','1134-09-07')],('ARAGON-KINGDOM','Q316194'):[('1134-09-29','1137-11-12')],
 ('ARAGON','Q235409'):[('1137-11-13','1164-07-18')],('ARAGON','Q299156'):[('1164-07-18','1196-04-25')],('BARCELONA-COUNTY','Q299156'):[('1162-08-06','1196-04-25')],
 ('NAVARRE-KINGDOM','Q379748'):[('1094','1104-09-28')],('NAVARRE-KINGDOM','Q81833'):[('1104-09-28','1134-09-07')],
 ('ENGLAND','Q150872'):[('1139','1148')],('ENGLAND','Q235238'):[('1170-06-14','1183-06-11')],
 ('HIST-Q12548','Q60094'):[('1084','1105-12-31')],('HIST-Q12548','Q151707'):[('1106','1111-04-12'),('1111-04-13','1125-05-23')],
 ('HIST-Q12548','Q77189'):[('1125','1133-06-03'),('1133-06-04','1137-12-04')],('HIST-Q12548','Q157133'):[('1138-03-07','1152-02-15')],
 ('HIST-Q12548','Q79789'):[('1152-03-04','1155-06-17'),('1155-06-18','1190-06-10')],('HIST-Q12548','Q150953'):[('1169-08-15','1191-04-14'),('1191-04-15','1197-09-28')],
 ('HIST-Q12548','Q121130'):[('1198-03-08','1208-06-21')],('HIST-Q12548','Q151457'):[('1198','1209-10-03')],
 ('BOHEMIA-DUCHY','Q367578'):[('1140','1157-12-31')],('BOHEMIA','Q367578'):[('1158','1172')],('BOHEMIA','Q312938'):[('1198','1230')],('BOHEMIA-DUCHY','Q312938'):[('1192','1193'),('1197-12-06','1197-12-31')],
 ('SAXONY-DUCHY','Q565737'):[('1180','1212-02-02')],
 ('JERUSALEM','Q76721'):[('1099-07-22','1100-07-18')],('JERUSALEM','Q51717'):[('1100','1118-04-02')],('JERUSALEM','Q51718'):[('1118-04-02','1131-08-21')],
 ('JERUSALEM','Q232151'):[('1131','1152')],('JERUSALEM','Q312904'):[('1131','1143')],('JERUSALEM','Q146465'):[('1143','1163')],('JERUSALEM','Q311808'):[('1163','1174')],
 ('JERUSALEM','Q296850'):[('1174','1185')],('JERUSALEM','Q345687'):[('1183','1186')],('JERUSALEM','Q234782'):[('1186','1190')],('JERUSALEM','Q294192'):[('1186','1192')],
 ('JERUSALEM','Q235629'):[('1190','1205')],('JERUSALEM','Q169329'):[('1190','1192-04-28')],('JERUSALEM','Q354422'):[('1192','1197')],('JERUSALEM','Q453325'):[('1197','1205')],
 ('ANTIOCH','Q51720'):[('1101','1103'),('1104','1112')],('ANTIOCH','Q550310'):[('1112','1119')],('ANTIOCH','Q333884'):[('1111','1130')],('ANTIOCH','Q437271'):[('1136','1149')],('ANTIOCH','Q316831'):[('1153','1160')],
 ('EDESSA','Q51717'):[('1098','1100')],('EDESSA','Q51718'):[('1100','1118')],('EDESSA','Q51719'):[('1119','1131')],('EDESSA','Q55503'):[('1131','1150')],
 ('TRIPOLI','Q547970'):[('1109','1112')],('TRIPOLI','Q349097'):[('1189','1233')],
 ('AYYUBID','Q8581'):[('1171-09-26','1193-03-04')],('FATIMID-VIZIER','Q8581'):[('1169-03-26','1171-09-26')],
 ('GREAT-SELJUK','Q337506'):[('1118','1157')],('GREAT-SELJUK','Q1658770'):[('1118','1131')],
 ('GORYEO','Q493830'):[('1095','1105')],('GORYEO','Q493852'):[('1105','1122')],('GORYEO','Q493874'):[('1122','1146')],('GORYEO','Q493893'):[('1146','1170')],('GORYEO','Q493913'):[('1170','1197')],('GORYEO','Q493930'):[('1197','1204')],
 ('GORYEO-MILITARY','Q6180265'):[('1170','1179')],('GORYEO-MILITARY','Q5624052'):[('1179','1183')],('GORYEO-MILITARY','Q484824'):[('1183','1196')],('GORYEO-MILITARY','Q712012'):[('1196','1219')],
 ('JPN-MILITARY','Q281833'):[('1160','1181')],('JPN-MILITARY','Q2420085'):[('1181','1185')],('JPN-MILITARY','Q242800'):[('1180','1192-08-20'),('1192-08-21','1199-02-09')],('JPN-MILITARY','Q431052'):[('1199','1202')],
 ('JPN-INSEI','Q60949'):[('1086','1129')],('JPN-INSEI','Q349284'):[('1129','1156')],('JPN-INSEI','Q317984'):[('1158','1179'),('1180','1192')],
 ('SERBIA-PRINCIPALITY','Q1359954'):[('1083','1112')],('SERBIA-PRINCIPALITY','Q2142592'):[('1112','1145')],('SERBIA-PRINCIPALITY','Q1932643'):[('1145','1162')],('SERBIA-PRINCIPALITY','Q16901299'):[('1162','1166')],('SERBIA-PRINCIPALITY','Q1359011'):[('1166','1166')],('SERBIA-PRINCIPALITY','Q298612'):[('1166','1196-03-25')],('SERBIA-PRINCIPALITY','Q24445'):[('1196-03-25','1202')],
 ('CILICIA-PRINCIPALITY','Q2422946'):[('1100','1129')],('CILICIA-PRINCIPALITY','Q2299801'):[('1129','1137')],('CILICIA-PRINCIPALITY','Q960183'):[('1144','1169')],('CILICIA-PRINCIPALITY','Q614187'):[('1169','1170')],('CILICIA-PRINCIPALITY','Q962744'):[('1170','1175')],('CILICIA-PRINCIPALITY','Q992945'):[('1175','1187')],('CILICIA-PRINCIPALITY','Q743783'):[('1187','1198-01-05')],('CILICIA-KINGDOM','Q743783'):[('1198-01-06','1219')],
 ('KHWAREZM','Q7273010'):[('1097','1127')],('BOSNIA-BANATE','Q389903'):[('1180','1204')],
 ('SICILY-KINGDOM','Q150953'):[('1194-12-25','1197-09-28')],('SICILY-KINGDOM','Q130221'):[('1198','1250')],
}
MANUAL.update({
 ('SAXONY-STEM','Q503687'):[('1072','1106')],('SAXONY-STEM','Q77189'):[('1106','1137')],('SAXONY-STEM','Q156041'):[('1138','1142')],
 ('BAVARIA-DUCHY','Q280495'):[('1139','1141-10-18')],('BAVARIA-DUCHY','Q168647'):[('1141','1156')],('BAVARIA-DUCHY','Q60563'):[('1180','1183')],('ELECTORATE-BRANDENBURG','Q706797'):[('1184','1205')],
 ('GEORGIA-MEDIEVAL','Q266754'):[('1155','1155')],
 ('SICILY-KINGDOM','Q193901'):[('1130-12-25','1154-02-26')],('SICILY-KINGDOM','Q367415'):[('1154-02-26','1166-05-07')],('SICILY-KINGDOM','Q367387'):[('1166-05-07','1189-11-11')],('SICILY-KINGDOM','Q468653'):[('1189','1194-02-20')],('SICILY-KINGDOM','Q560005'):[('1194-02-20','1194-12-24')],
})
NOTES={
 'HIST-Q12548':'Realeza de Romanos y coronación imperial son dignidades distintas. Elecciones rivales y cogobiernos no equivalen a un Estado nacional uniforme.',
 'ENGLAND':'Esteban y Matilde disputan la sucesión; Matilde no fue reina coronada ni gobernó toda Inglaterra. Enrique el Joven fue coronado en vida de su padre sin gobierno independiente.',
 'ARAGON':'Pacto dinástico de1137, herencia de1162 y abdicación dePetronila en1164 son hitos distintos. Ramón BerenguerIV es príncipe deAragón, no rey.',
 'PORTUGAL-COUNTY':'Condado dependiente deLeón. Teresa ejerce gobierno y regencia desde1112; Alfonso hereda siendo menor, con gobierno personal desde1128. Proclamación real1139 y reconocimiento1143/1179 son hitos distintos.',
 'PRT':'Proclamación real1139, pacto deZamora1143 y reconocimiento pontificio1179 son fases diferentes.',
 'JERUSALEM':'El título no acredita posesión deJerusalén después de1187. Regencias, corregencias y candidaturas de1190–1192 se distinguen; las fechas sucesorias tienen variantes.',
 'ANTIOCH':'Regentes y príncipes conservan funciones distintas. BohemundoII hereda menor en1111 y ejerce personalmente desde1126; no todo título acredita control efectivo.',
 'GREAT-SELJUK':'Poderes regionales en fragmentación; Sanjar gobierna el ámbito oriental yMahmudII el iraquí-iraní. No son soberanos uniformes de todo el agregado.',
 'JPN':'Corte imperial, emperadores retirados y dirigencia militar son cargos distintos. Los emperadores rivales de1183–1185 no equivalen a gobierno simultáneo de todo el archipiélago.',
 'GORYEO':'Monarquía y régimen militar desde1170 tienen autoridades distintas; no convertir dirigentes militares en reyes.',
 'CILICIA-PRINCIPALITY':'Principado anterior a la coronación deLeón en1198; hay interrupción bizantina desde1137 hasta1144.',
 'BOHEMIA':'VladislaoII recibe título real personal en1158; no implica una monarquía hereditaria continua antes de1198.',
 'SERBIA-PRINCIPALITY':'Gran principado, no reino antes de1217. Cronologías de los primeros grandes príncipes y los rivales tienen variantes.',
 'BOSNIA-BANATE':'Ban, no rey. La ventana deKulin comienza hacia1180; no se infiere de una entidad geográfica homónima.',
}
def research():
 base=read(ROOT/'.cache/rulers025-candidates.json');evidence=read(ROOT/'.cache/rulers025-office-evidence.json');rows=[];seen=set()
 for r in base['records']+[v['candidate']for v in evidence]:
  sig=(r['key'],r.get('person'),r['title'])
  if sig not in seen:rows.append(r);seen.add(sig)
 # A person may hold several offices; the acquisition cache is keyed by article.
 spec=importlib.util.spec_from_file_location('g',ROOT/'scripts/review-025-rulers.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 tree=ast.parse((ROOT/'scripts/review-025-offices.py').read_text(encoding='utf8'));groups=next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='EXTRA_GROUPS'for t in n.targets))
 for k,role,ts in g.r.GROUPS+[(k,v[0],v[1])for k,v in groups.items()]:
  for title in ts:
   r=next((r for r in rows if r.get('human')and title in[r.get('requestedTitle'),r.get('title')]),None)
   if r and not any(v['key']==k and v.get('person')==r['person']for v in rows):rows.append({**r,'key':k,'role':role})
 # Explicit reuse of the same verified person for another historically documented office.
 for k,q in [('CASTILE-KINGDOM','Q128701'),('LEON-KINGDOM','Q235080'),('CASTILE-KINGDOM','Q235080'),('LEON-KINGDOM','Q312767'),('CASTILE-KINGDOM','Q312767'),('PORTUGAL-COUNTY','Q587697'),('BARCELONA-COUNTY','Q299156'),('NAVARRE-KINGDOM','Q379748'),('NAVARRE-KINGDOM','Q81833')]:
  r=next((v for v in rows if v.get('person')==q and v.get('human')),None)
  if r and not any(v['key']==k and v.get('person')==q for v in rows):rows.append({**r,'key':k,'role': 'Conde de Portugal' if k=='PORTUGAL-COUNTY' else 'Conde de Barcelona' if k=='BARCELONA-COUNTY' else 'Rey / reina de Navarra' if k=='NAVARRE-KINGDOM' else 'Rey / reina de Castilla' if k=='CASTILE-KINGDOM' else 'Rey / reina de León'})
 accepted=[];rejected=[];dedup=set()
 def add(k,row,role,a,b,note):
  a=a+'-01-01'if len(a)==4 else a;b=b+'-12-31'if len(b)==4 else b
  if a>'1199-12-31'or b<'1100-01-01'or a>b:return
  first,last=max(a,'1100-01-01'),min(b,'1199-12-31');key=ALIASES.get(k,k);sig=(key,row['person'],role,first,last)
  if sig in dedup:return
  dedup.add(sig);clean=lambda s:re.sub(r'(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ0-9])',' ',s)
  accepted.append(dict(key=key,term=dict(person=row['person'],name=row.get('name',row['title']),role=clean(role),start=first,end=last,precision=9,source=row['source'],curated=True,acquisition=TAG,note=clean(note)+' Síntesis anual; no calendario diario ni certificación del dominio de todo el contorno.',startIsCoverageBoundary=a<'1100-01-01',endIsCoverageBoundary=b>'1199-12-31')))
 for row in rows:
  k=row['key'];q=row.get('person');role=row['role'];note=NOTES.get(k,'El cargo documentado no acredita control uniforme de toda la geometría de fuente.')
  if not row.get('human'):rejected.append(dict(candidate=row,reason='Unresolved or nonhuman identity'));continue
  ev=next((v for v in evidence if v['candidate'].get('person')==q),dict(claims=[]));dates=MANUAL.get((k,q));pattern=PATTERNS.get(k)
  if dates is None and pattern:dates=list(dict.fromkeys((c['start'],c['end'][:4]+'-12-31'if c['precision']==9 and c['end'].endswith('-01-01')else c['end'][:7]+'-'+str(calendar.monthrange(int(c['end'][:4]),int(c['end'][5:7]))[1])if c['precision']==10 and c['end'].endswith('-01')else c['end'])for c in ev['claims']if re.search(pattern,c.get('label',''),re.I)))
  if not dates and row.get('parsed') and k not in ['JPN-INSEI','JPN-MILITARY','BOHEMIA','BOHEMIA-DUCHY','SAXONY-STEM','BAVARIA-DUCHY','ELECTORATE-BRANDENBURG']:
   dates=[(p['start'],p['end'])for p in row['parsed']] if k in ['BYZANTINE','SOUTHERN-SONG']else[(row['parsed'][0]['start'],row['parsed'][0]['end'])]
  if not dates:rejected.append(dict(candidate=row,reason='Intended office dates unresolved; no inference from lifetime or another title'));continue
  for index,(a,b)in enumerate(dates):
   actual=role
   if q=='Q266754':row={**row,'source':'https://georgianencyclopedia.ge/ka/form/27302'}
   if k=='HIST-Q12548':actual='Emperador del Sacro Imperio'if q=='Q60094'or q=='Q151707'and index==1 or q=='Q77189'and index==1 or q=='Q79789'and index==1 or q=='Q150953'and index==1 else'Rey de Romanos · elección rival'if q in ['Q121130','Q151457']else'Rey de Romanos'
   if k=='ENGLAND'and q=='Q150872':actual='Matilde · pretendiente al trono y señora de los ingleses'
   if k=='ENGLAND'and q=='Q235238':actual='Rey joven coronado · sin gobierno independiente'
   if k=='JERUSALEM'and q=='Q76721':actual='Defensor del Santo Sepulcro'
   if k=='JERUSALEM'and q=='Q169329':actual='Pretendiente desde1190 · rey elegido en1192'
   if k=='ANTIOCH'and q in ['Q51720','Q550310']:actual='Regente de Antioquía'
   if k=='JPN-MILITARY':actual='Shogun de Kamakura'if q=='Q242800'and index==1 else'Dirigente militar · todavía sin título de shogun'if q in ['Q242800','Q431052']else'Principal dirigente Taira'
   if k=='QARA-KHITAI'and q in ['Q6713105','Q8005268']:actual='Regente de Liao Occidental'
   if k=='SOUTHERN-SONG':a=max(a,'1127-06-12');b=min(b,'1199-12-31')
   if k=='NORTHERN-SONG':b=min(b,'1127-03-20')
   if k=='FATIMID':b=min(b,'1171-09-26')
   if k=='ALMORAVID':b=min(b,'1147-12-31')
   if k=='SAXONY-STEM':b=min(b,'1179-12-31')
   if k=='BOHEMIA-DUCHY-CORRECTION':actual='Duque de Bohemia'
   add(k,row,actual,a,b,note)
  if k=='BARCELONA-COUNTY'and q=='Q319439':add('ARAGON',row,'Príncipe de Aragón · conde de Barcelona','1137','1162-08-06',NOTES['ARAGON'])
 return dict(records=accepted,rejected=rejected,aliases=ALIASES,seeds=read(ROOT/'.cache/seeds025.json'),polityEvidence=read(ROOT/'.cache/polities025-verified.json'),candidates=base,evidence=evidence,scope='Selected office evidence1100–1199. Partial series and source chronology defects remain explicit.')
def prepare(old,rs):
 d=copy.deepcopy(old);cs=d['countries'];images={l['person']:l['portrait']for c in cs.values()for l in c['leaders']if l.get('portrait')}
 for alias,target in rs['aliases'].items():
  if alias in cs and alias!=target and target in cs:
   c=cs[alias]
   if all(l.get('acquisition')in['historical-0.25',TAG]for l in c['leaders'])and not c['flags']:
    cs[target]['leaders'].extend(c['leaders']);del cs[alias]
 seeds={ALIASES.get(k,k):v for k,v in rs['seeds'].items()}
 seeds.update({'BOHEMIA-DUCHY':('Q2162698','Ducado de Bohemia'),'SAXONY-STEM':('Q164092','Ducado raíz de Sajonia'),'CILICIA-PRINCIPALITY':('Q335088','Principado armenio de Cilicia · antes de1198')})
 for k,(q,name)in seeds.items():cs.setdefault(k,dict(qid=q,name=name,leaders=[],flags=[]))
 for c in cs.values():
  for l in c['leaders']:
   if l.get('acquisition')=='historical-0.25'and l['start']>l['end']and l['start'][:4]==l['end'][:4]and l.get('precision')==9:
    l['end']=l['end'][:4]+'-12-31';l['note']='Fin de mandato documentado sólo por año; el1 deenero del dato de origen no es una fecha diaria de cese.'
 for c in cs.values():c['leaders']=[l for l in c['leaders']if l.get('acquisition')!=TAG]
 for row in rs['records']:
  k=row['key'];l=copy.deepcopy(row['term'])
  if k not in cs:continue
  if l['person']in images:l['portrait']=images[l['person']]
  cs[k]['leaders']=[v for v in cs[k]['leaders']if not(v.get('acquisition')=='historical-0.25'and v['person']==l['person']and v['start']<=l['end']and v['end']>=l['start'])];cs[k]['leaders'].append(l)
 return d
if __name__=='__main__':
 p=ROOT/'scripts/historical-offices-025-research.json';rs=research()if not p.exists()or'--research'in sys.argv else read(p);save(p,rs);old=read(OUT/'identities.json');d=prepare(old,rs);assert prepare(d,rs)==d
 for k,c in old['countries'].items():
  if k not in d['countries']:continue
  assert all(l in d['countries'][k]['leaders']for l in c['leaders']if l.get('acquisition')not in[TAG,'historical-0.25']),k
 save(OUT/'identities.json',d);print('Reviewed intervals',len(rs['records']),'unresolved/rejected',len(rs['rejected']))
