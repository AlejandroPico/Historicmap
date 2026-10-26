"""Idempotent, bounded1820–1839 identity and historical-office preparation."""
import pathlib,json,copy
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'public/data';TAG='curated-1820-0.16'
read=lambda f:json.loads((OUT/f).read_text(encoding='utf8'))
save=lambda f,d:(OUT/f).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
def prepare(incoming,research):
 d=copy.deepcopy(incoming);cs=d['countries'];portraits={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
 for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
 # Rejected source claims are scoped to this new acquisition, never later terms.
 for k in ['RUE','ESP']:
  cs[k]['leaders']=[l for l in cs[k]['leaders'] if not(l.get('acquisition')=='historical-0.16' and (k=='RUE' or l['person']=='Q183085'))]
 titles={'PRUSSIA':'Rey de Prusia','SAR':'Rey de Cerdeña','BRA-EMPIRE':'Emperador del Brasil','QING':'Emperador de la dinastía Qing','JOS':'Rey de Joseon','IRN':'Shah de Persia · dinastía Qajar','AUSTRIAN-EMPIRE':'Emperador de Austria','PAPAL-STATES':'Papa · soberano de los Estados Pontificios'}
 for item in research['records']:
  k=item['key'];l=copy.deepcopy(item['term'])
  if k=='SAR' and l['person']=='Q168691':continue # source typo1839 instead of1849
  if k=='BRA-EMPIRE' and l['person']=='Q676301':continue # honorary title, not governing Brazil
  l['acquisition']=TAG;l['role']=titles.get(k,l['role'])
  if k=='JPN':l['role']='Shogun · Gobierno militar'
  if k=='BRA-EMPIRE' and l['person']=='Q156774':l['role']='Emperador del Brasil · minoría de edad'
  if l['person'] in portraits:l['portrait']=copy.deepcopy(portraits[l['person']])
  cs.setdefault(k,dict(qid='',name=k,flags=[],leaders=[]))['leaders'].append(l)
 def term(k,q,name,role,a,b,url,precision=11,note=''):
  l=dict(person=q,name=name,role=role,start=a,end=b,source=url,precision=precision,curated=True,acquisition=TAG,note=note)
  if a=='1820-01-01' or precision<11:l['startIsCoverageBoundary']=True
  if b=='1839-12-31' or precision<11:l['endIsCoverageBoundary']=True
  if q in portraits:l['portrait']=copy.deepcopy(portraits[q])
  cs[k]['leaders'].append(l)
 term('RUE','Q15193','Alejandro I','Emperador de Rusia','1820-01-01','1825-12-01','https://www.wikidata.org/wiki/Q15193',note='Fecha gregoriana; no duplicar el19de noviembre juliano como otra sucesión.')
 term('RUE','Q130734','Nicolás I','Emperador de Rusia','1825-12-01','1839-12-31','https://www.wikidata.org/wiki/Q130734',note='Fecha gregoriana retrospectiva del reinado; interregno y juramento de diciembre requieren contexto propio.')
 term('ESP','Q183085','Isabel II','Reina de España · minoría de edad','1833-09-29','1839-12-31','https://www.congreso.es/en/web/guest/cem/regmcris')
 term('ESP','Q230566','María Cristina de Borbón-Dos Sicilias','Regente','1833-09-29','1839-12-31','https://www.congreso.es/en/web/guest/cem/regmcris')
 term('GBR','Q127318','Jorge III','Rey del Reino Unido','1820-01-01','1820-01-29','https://www.royal.uk/encyclopedia/george-iv-r-1820-1830')
 term('GBR','Q130586','Jorge IV','Rey del Reino Unido','1820-01-29','1830-06-26','https://www.royal.uk/encyclopedia/george-iv-r-1820-1830')
 term('GBR','Q130822','Guillermo IV','Rey del Reino Unido','1830-06-26','1837-06-20','https://www.wikidata.org/wiki/Q130822')
 term('GBR','Q9439','Victoria','Reina del Reino Unido','1837-06-20','1839-12-31','https://api.parliament.uk/regnal-years/monarchs/6')
 term('EGY','Q182781','Muhammad Alí','Valí de Egipto','1820-01-01','1839-12-31','https://sis.gov.eg/en/egypt/history/egypts-history/modern-era/')
 term('IRN','Q175299','Fath Alí Shah','Shah de Persia · dinastía Qajar','1820-01-01','1834-01-01','https://www.wikidata.org/wiki/Q175299',9,'Observación anual interior de su reinado; no son fechas de acceso o de fallecimiento.')
 term('HAW-KINGDOM','Q455795','Kamehameha III','Rey de Hawái','1825-01-01','1839-12-31','https://www.wikidata.org/wiki/Q455795',9,'Observación anual; las regencias y ceremonias no se confunden con la sucesión.')
 term('BRA-EMPIRE','BRA-TRINA-1831','Regencia Trina','Regencia colegiada','1831-04-07','1835-01-01','https://www12.senado.leg.br/senado200anos/passado',9,'El extremo1835 es observación anual, no fecha diaria de relevo; falta detallar las fases provisional y permanente.')
 term('BRA-EMPIRE','Q1791593','Diogo Antônio Feijó','Regente','1835-12-31','1837-01-01','https://www12.senado.leg.br/senado200anos/passado',9,'Observación interior del mandato1835–1837; extremos de cobertura.')
 term('BRA-EMPIRE','Q1797348','Pedro de Araújo Lima','Regente','1837-12-31','1839-12-31','https://www12.senado.leg.br/senado200anos/passado',9,'Observación interior; la regencia continúa hasta1840.')
 for k in ['HIST-Q199821','HIST-Q285658']:
  if k in cs:cs[k]['name']='Gran Colombia' if k.endswith('199821') else 'Primer Imperio mexicano'
 # Reuse only already acquired symbols with explicitly compatible historical use.
 windows=[('BRA-EMPIRE','1823-01-01','1839-12-31','Flag of Brazil (1822–1853).svg'),('PRT','1835-01-01','1839-12-31','Flag of Portugal (1830–1910).svg'),('PRUSSIA','1820-01-01','1839-12-31','Flag of Prussia (1803–1892).svg'),('PAPAL-STATES','1826-01-01','1839-12-31','Flag of the Papal States (1825-1870).svg')]
 for k,a,b,title in windows:
  media=next((f['media'] for c in cs.values() for f in c['flags'] if f['media']['title']==title),None)
  if media:
   f=dict(start=a,end=b,media=copy.deepcopy(media),source=media['url'],note='Ventana de observación conservadora; no fecha de adopción.')
   if f not in cs[k]['flags']:cs[k]['flags'].append(f)
 cs.setdefault('HIST-Q285658',dict(qid='Q285658',name='Primer Imperio mexicano',flags=[],leaders=[]))
 term('HIST-Q285658','Q133808','Agustín de Iturbide','Emperador de México','1822-12-31','1823-01-01','https://www.gob.mx/agn/articulos/agnrecuerda-al-primer-imperio-mexicano',9,'Observación interior del reinado; elección, proclamación, coronación y abdicación son hitos diferentes.')
 term('TWO-SICILIES','Q312325','Fernando I','Rey de las Dos Sicilias','1820-01-01','1825-01-01','https://www.wikidata.org/wiki/Q312325',9,'Observación anual, no fecha diaria de sucesión.')
 term('TWO-SICILIES','Q312305','Francisco I','Rey de las Dos Sicilias','1825-12-31','1830-01-01','https://www.wikidata.org/wiki/Q312305',9,'Observación interior del reinado1825–1830.')
 if 'HIST-Q199821' in cs:cs['HIST-Q199821']['leaders']=[l for l in cs['HIST-Q199821']['leaders'] if not(l.get('acquisition')=='historical-0.16' and l['start']>='1832-01-01')]
 return d
if __name__=='__main__':
 old=read('identities.json');research=json.loads((ROOT/'.cache/historical-offices-016.json').read_text(encoding='utf8'));d=prepare(old,research);assert prepare(d,research)==d
 for k,c in old['countries'].items():assert [l for l in c['leaders'] if l['end']>='1840-01-01']==[l for l in d['countries'][k]['leaders'] if l['end']>='1840-01-01'],k
 save('identities.json',d);print('Curated bounded offices; all1840+ statements preserved')
 (ROOT/'scripts/historical-offices-016-research.json').write_text(json.dumps(research,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
