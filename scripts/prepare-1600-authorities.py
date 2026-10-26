"""Explicit office selection1600–1699, with frozen research and rejected homonyms.

No prior facts are replaced. Annual observations never pretend calendar conversion.
"""
import pathlib,json,copy,sys,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1600-0.20'
s=importlib.util.spec_from_file_location('h',ROOT/'scripts/enrich-1970-authorities.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
read=lambda p:json.loads(p.read_text(encoding='utf8'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
INDICES={('ENGLAND','Q79972'):1,('ELECTORATE-BRANDENBURG','Q151826'):1,('RUSSIA-TSARDOM','Q8479'):1,('DUTCH-REPUBLIC','Q129987'):1,('LATER-JIN','Q296367'):1,('BAVARIA-ELECTORATE','Q57206'):1,('PRT','Q691402'):1,('SAVOY-DUCHY','Q209579'):2,('POLISH-LITHUANIAN','Q53437'):1}
MANUAL={
 'Q44279':('1653-12-16','1658-09-03',9),'Q203980':('1658-09-03','1659-05-25',9),
 'Q505548':('1656-10-08','1680-08-22',9),'Q164062':('1585-11-14','1625-04-23',9),'Q167236':('1625-04-23','1647-03-14',9),
 'Q171977':('1603-01-01','1605-12-31',9),'Q314464':('1605-01-01','1623-12-31',9),'Q314481':('1623-01-01','1651-12-31',9),'Q323422':('1651-01-01','1680-12-31',9),'Q313745':('1680-01-01','1699-12-31',9),
 'Q882744':('1605-01-01','1610-12-31',9),'Q889158':('1610-01-01','1611-12-31',9),'Q561528':('1611-01-01','1628-12-31',9),'Q718197':('1656-01-01','1688-12-31',9),'Q52934':('1697-01-01','1699-12-31',9),
 'Q2840566':('1587-01-01','1614-12-31',9),'Q2840567':('1615-01-01','1622-12-31',9),'Q3095344':('1624-01-01','1626-12-31',9),'Q2842433':('1626-01-01','1631-12-31',9),'Q2840564':('1631-01-01','1636-12-31',9),'Q2840574':('1636-01-01','1636-12-31',9),'Q2720222':('1636-01-01','1641-12-31',9),'Q3095343':('1641-01-01','1661-12-31',9),
 'Q182021':('1610-01-01','1617-12-31',9),'Q151209':('1643-01-01','1651-12-31',9),'Q233987':('1682-01-01','1689-12-31',9),'Q241206':('1656-01-01','1662-12-31',9),'Q311469':('1665-01-01','1675-12-31',9),'Q318362':('1653-01-01','1672-12-31',9)}

def research():
 candidates=read(ROOT/'.cache/rulers020-candidates.json');extra=read(ROOT/'.cache/rulers020-extra-candidates.json');accepted=[];rejected=[]
 def add(k,q,name,role,a,b,p,source,note=''):
  if a>'1699-12-31' or b<'1600-01-01':return
  accepted.append(dict(key=k,term=dict(person=q,name=name,role=role,start=max(a,'1600-01-01'),end=min(b,'1699-12-31'),precision=p,source=source,curated=True,note=note,startIsCoverageBoundary=a<'1600-01-01' or p<11,endIsCoverageBoundary=b>='1699-12-31' or p<11)))
 for row in candidates['records']+extra['records']:
  q=row.get('person');key=row['key'];role=row['role']
  if not row.get('human'):rejected.append(dict(candidate=row,reason='Not a verified human; disambiguation cannot become a ruler'));continue
  if key=='SWE' and q=='Q52940':continue # Swedish reign ended1599, Polish reign is a different office.
  dates=MANUAL.get(q)
  if not dates and row['parsed']:
   v=row['parsed'][INDICES.get((key,q),0)];dates=(v['start'],v['end'],v['precision'])
  if not dates:rejected.append(dict(candidate=row,reason='Office interval unresolved'));continue
  a,b,precision=dates;note='Cargo histórico fechado; las autoridades rivales y las regencias no implican control uniforme de toda la geometría anual.'
  if key in ['ENGLAND','SCOTLAND','ENGLISH-COMMONWEALTH','RUSSIA-TSARDOM','SWE']:
   precision=9;note+=' Observación anual: fechas de estilo antiguo/conversión de calendario todavía no contrastadas día a día.'
  if key=='PRT' and q=='Q34464':role='Felipe II de Portugal · unión dinástica';note+=' Misma persona que FelipeIIIdeEspaña, coronas y administraciones distintas.'
  if key=='PRT' and q=='Q691402':role='Felipe III de Portugal · unión dinástica'
  if key=='RUSSIA-TSARDOM' and q in ['Q183698','Q8479']:note+=' IvánV y PedroI son cozares; la regencia deSofía se indica por separado.'
  if key in ['LATER-JIN','QING'] and q=='Q296367':note+=' El título imperial Qing de1636 es distinto del khanato Jin anterior.'
  if key=='SOUTHERN-MING':note+=' Pretensión Ming del Sur; no se atribuye soberanía efectiva sobre el imperio Qing ni sobre todaChina.'
  if key=='DUTCH-REPUBLIC':note+=' Cargo provincial, distinto de la soberanía de los Estados Generales.'
  if key=='HIST-Q796583':note+=' La guerra civil posterior a1665 requiere autoridades por facción; no se extiende un rey por interpolación.'
  if q in ['Q61169','Q61362','Q61557','Q702876','Q60438','Q472186','Q355755']:note+=' La titularidad puede comenzar durante la minoría; no equivale a gobierno personal adulto.'
  add(key,q,row['name'],role,a,b,precision,row['source'],note)
  if key=='BAVARIA-ELECTORATE' and q=='Q57206':
   v=row['parsed'][0];add('BAVARIA-DUCHY',q,row['name'],'Duque de Baviera',v['start'],v['end'],v['precision'],row['source'],'Dignidad ducal anterior a la elevación electoral de1623.')
  if key=='ELECTORATE-BRANDENBURG':
   # The union with Prussia begins1618. The earlier electoral title remains separate.
   if b>='1618-01-01':add('HIST-Q157367',q,row['name'],'Elector de Brandeburgo y duque de Prusia',max(a,'1618-01-01'),b,9,row['source'],'Unión dinástica, no reino dePrusia antes de1701.')
  if key=='HIST-Q12548':
   add('HABSBURG-MONARCHY',q,row['name'],'Autoridad de la rama imperial de Habsburgo',a,b,9,row['source'],'Referencia de la rama imperial, no un gobernante único de todos los dominios y ramas de la casa. Las cesiones entreRodolfo yMatías y los territorios hereditarios requieren detalle regional; la dignidad imperial es distinta.')
 # Corrections verified independently: the same names first matched disambiguations.
 for k,q,role,a,b in [('HIST-Q157367','Q152727','Elector de Brandeburgo y duque de Prusia','1640-01-01','1688-12-31'),('ELECTORATE-BRANDENBURG','Q152727','Elector de Brandeburgo','1640-01-01','1688-12-31'),('OTT','Q172061','Sultán otomano','1687-01-01','1691-12-31')]:
  e=h.entity(q);assert any(v.get('id')=='Q5' for v in h.values(e,'P31') if isinstance(v,dict));add(k,q,h.label(e),role,a,b,9,'https://www.wikidata.org/wiki/'+q,'Identidad humana contrastada; se rechaza la página de desambiguación homónima. Observación anual.')
 add('OTT','Q174798','Mustafá I','Sultán otomano','1617-11-22','1618-02-26',11,'https://en.wikipedia.org/wiki/Mustafa_I','Primer reinado, separado de su restauración.')
 add('OTT','Q174798','Mustafá I','Sultán otomano','1622-05-20','1623-09-10',11,'https://en.wikipedia.org/wiki/Mustafa_I','Segundo reinado; no un mandato continuo1617–1623.')
 add('SCOTLAND','Q122553','Carlos II','Rey de Escocia','1649-01-01','1651-12-31',9,'https://en.wikipedia.org/wiki/Charles_II_of_England','Realeza escocesa anterior a la incorporación a laCommonwealth; no rey efectivo deInglaterra durante el interregno.')
 add('SWE','Q52939','Carlos IX','Regente de Suecia','1600-01-01','1603-12-31',9,'https://en.wikipedia.org/wiki/Charles_IX_of_Sweden','Autoridad regente, distinta del título real desde1604.')
 add('PRT','Q156190','Pedro de Braganza','Regente de Portugal','1668-01-01','1683-12-31',9,'https://en.wikipedia.org/wiki/Peter_II_of_Portugal','Gobierno regente durante la incapacidad deAfonsoVI; rey desde1683, no desde1668.')
 for a,b,name in [('1649-01-01','1653-12-31','Parlamento y Consejo de Estado'),('1659-01-01','1660-12-31','Parlamento restablecido y Consejo de Estado')]:add('ENGLISH-COMMONWEALTH','COMMONWEALTH-COUNCIL-'+a[:4],name,'Autoridad colegiada',a,b,9,'https://www.royal.uk/interregnum-1649-1660','Ventana anual del gobierno republicano, con reorganizaciones internas pendientes de detalle; sin retrato individual ficticio.')
 add('RUSSIA-TSARDOM','SEVEN-BOYARS','Consejo de los siete boyardos','Gobierno provisional · control disputado','1610-01-01','1612-12-31',9,'https://en.wikipedia.org/wiki/Seven_Boyars','No se presenta como una monarquía estable ni como control uniforme; ocupación y pretendientes requieren detalle independiente.')
 return dict(records=accepted,rejected=rejected,candidates=candidates,extraCandidates=extra,polityEvidence=read(ROOT/'.cache/polities020-verified.json'),scope='Reviewed subset of offices; not an exhaustive world census or a daily-calendar verification.')

def prepare(old,r):
 d=copy.deepcopy(old);cs=d['countries'];images={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for key,q,name in [('SHUN','Q2370784','Régimen Shun · Li Zicheng'),('IBERIAN-UNION','Q377350','Unión Ibérica'),('ENGLISH-COMMONWEALTH','Q330362','Commonwealth de Inglaterra'),('EASTERN-MOGHULISTAN','','Mogulistán oriental · referencia de fuente'),('WESTERN-MOGHULISTAN','','Mogulistán occidental · referencia de fuente')]:cs.setdefault(key,dict(qid=q,name=name,leaders=[],flags=[]))
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 for row in r['records']:
  k=row['key'];l=copy.deepcopy(row['term']);l['acquisition']=TAG
  if l['person'] in images:l['portrait']=images[l['person']]
  cs[k]['leaders']=[o for o in cs[k]['leaders'] if not(o.get('acquisition')=='historical-0.20' and o['person']==l['person'] and o['start']<=l['end'] and o['end']>=l['start'])]
  cs[k]['leaders'].append(l)
 # The union is dynastic; show the monarch without asserting a merged bureaucracy.
 cs['IBERIAN-UNION']['leaders']=[l for l in cs['IBERIAN-UNION']['leaders'] if l.get('acquisition')!=TAG]
 for l in cs['ESP']['leaders']:
  if l.get('acquisition')==TAG and l['person'] in ['Q34464','Q691402']:
   v=copy.deepcopy(l);v.update(end=min(v['end'],'1640-12-01'),role='Soberano de la unión dinástica',note='Coronas deEspaña yPortugal con instituciones distintas; FelipeII yIIIdePortugal son FelipeIII yIVdeEspaña.');cs['IBERIAN-UNION']['leaders'].append(v)
 # Correct the source's use of a person as the polity item.
 q='Q333567';cs['SHUN']['leaders']=[l for l in cs['SHUN']['leaders'] if l.get('acquisition')!=TAG];cs['SHUN']['leaders'].append(dict(person=q,name='Li Zicheng',role='Emperador Shun · pretensión rival',start='1644-01-01',end='1645-12-31',precision=9,source='https://en.wikipedia.org/wiki/Shun_dynasty',curated=True,acquisition=TAG,startIsCoverageBoundary=True,endIsCoverageBoundary=True,note='No se convierte aLiZicheng en una entidad territorial personal ni se le atribuye todaChina.',**({'portrait':images[q]} if q in images else {})))
 return d

if __name__=='__main__':
 p=ROOT/'scripts/historical-offices-020-research.json';r=research() if not p.exists() or '--research' in sys.argv else read(p);save(p,r);old=read(OUT/'identities.json');d=prepare(old,r);assert prepare(d,r)==d
 for k,c in old['countries'].items():assert all(l in d['countries'][k]['leaders'] for l in c['leaders'] if l.get('acquisition') not in [TAG,'historical-0.20']),k
 save(OUT/'identities.json',d);print('Reviewed office intervals',len(r['records']),'rejected/unresolved',len(r['rejected']))
