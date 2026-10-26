"""Idempotent documentary context1820–1839; no inferred military fronts."""
import pathlib,json,copy
OUT=pathlib.Path(__file__).resolve().parents[1]/'public/data';PREFIX='extension-1820-'
FR='https://www.assemblee-nationale.fr/dyn/histoire-et-patrimoine/monarchie-de-juillet/l-insurrection-des-trois-glorieuses'
ES='https://www.congreso.es/en/web/guest/cem/trielib';REG='https://www.congreso.es/en/web/guest/cem/regmcris';BR='https://www12.senado.leg.br/senado200anos/passado'
ROWS=[
 ('france-restoration','Francia · Restauración borbónica','transition','1820-01-01','1830-08-09',['FRA'],'Luis XVIII y Carlos X preceden a Luis Felipe. Las jornadas de julio y el juramento de agosto de 1830 son fases distintas.',FR,'institutions'),
 ('france-july','Francia · Monarquía de Julio','transition','1830-08-09','1840-01-01',['FRA'],'Luis Felipe jura la Carta revisada. El cambio de dinastía y régimen no constituye una república.',FR,'institutions'),
 ('triennium','España · Trienio Liberal','transition','1820-01-01','1824-01-01',['ESP'],'Fernando VII conserva el trono bajo la Constitución restaurada. La intervención francesa termina el periodo constitucional durante 1823.',ES,'institutions'),
 ('spain-intervention','Intervención francesa en España de 1823','conflict','1823-01-01','1824-01-01',['ESP','FRA'],'Los Cien Mil Hijos de San Luis restauran el absolutismo. No se convierte todo el país en una anexión francesa.',ES,'defense'),
 ('spain-regency','España · sucesión y regencia de 1833','transition','1833-01-01','1840-01-01',['ESP'],'Tras la muerte de Fernando VII, Isabel II es soberana menor y María Cristina regente. Estatuto Real de 1834 y Constitución de 1837 son instrumentos distintos. Falta completar las autoridades carlistas.',REG,'institutions'),
 ('portugal-war','Portugal · guerra civil liberal','conflict','1832-01-01','1835-01-01',['PRT'],'Liberales y absolutistas combaten entre 1832 y 1834. La paz de Évora-Monte no proporciona por sí misma un frente militar anual.','https://app.parlamento.pt/publicacoesonline/palacio.pdf','defense'),
 ('brazil-independence','Brasil · independencia y Primer Reinado','transition','1822-01-01','1831-04-07',['BRA-EMPIRE','PRT'],'Independencia de 1822, Constitución de 1824 y abdicación de 1831 son momentos distintos. El título honorífico de Juan VI no es gobierno efectivo del Brasil.',BR,'institutions'),
 ('brazil-regencies','Brasil · periodo de regencias','transition','1831-04-07','1840-01-01',['BRA-EMPIRE'],'Durante la minoría de Pedro II gobiernan regencias colegiadas y unipersonales. El corte de cobertura precede a la mayoría anticipada de 1840.',BR,'institutions'),
 ('belgium','Bélgica · independencia y Constitución','transition','1830-01-01','1832-01-01',['BEL','NLD'],'Independencia proclamada el 4 de octubre de 1830; Constitución y acceso de Leopoldo I en 1831. No se asigna su reinado al Gobierno provisional de 1830.','https://www.belgium.be/en/about_belgium/country/history/belgium_from_1830','institutions'),
 ('mexico','México · Primer Imperio y transición federal','transition','1822-01-01','1825-01-01',['HIST-Q285658','MEX'],'Iturbide es proclamado en 1822; la caída de 1823 precede a la Constitución federal de 1824. No se confunde este Imperio con el de Maximiliano.','https://www.gob.mx/agn/articulos/agnrecuerda-al-primer-imperio-mexicano','institutions'),
 ('monroe','Doctrina Monroe · declaración de 1823','transition','1823-12-02','1824-01-01',['USA'],'El mensaje presidencial advierte contra nuevas intervenciones europeas. Es una posición diplomática, no una alianza ni una anexión continental.','https://www.archives.gov/milestone-documents/monroe-doctrine','relations'),
 ('removal','Estados Unidos · desplazamiento forzoso indígena','transition','1830-01-01','1840-01-01',['USA'],'La Indian Removal Act de 1830 y los desplazamientos posteriores afectan a pueblos indígenas. La ausencia de entidades en la geometría no significa tierra deshabitada.','https://www.archives.gov/milestone-documents/jacksons-message-to-congress-on-indian-removal','society'),
 ('afghan','Primera guerra anglo-afgana · fase de 1839','conflict','1839-01-01','1840-01-01',['AFG','GBR','IND'],'La expedición británico-india instala a Shah Shuja tras la salida de Dost Mohammad. La guerra continúa hasta 1842; esta ventana sólo cubre su primera fase.','https://www.nam.ac.uk/explore/first-afghan-war','defense'),
 ('opium','Primera guerra del Opio · inicio de 1839','conflict','1839-01-01','1840-01-01',['QING','GBR','IND'],'Las confiscaciones y los primeros combates preceden a las campañas de 1840. El corte documental no es el final de la guerra.','https://www.nam.ac.uk/explore/first-china-war-1839-1842','defense')]
def prepare(context,history):
 c,h=copy.deepcopy((context,history))
 for d,field in [(c,'events'),(h,'records'),(h,'relations')]:d[field]=[r for r in d[field] if not r['id'].startswith(PREFIX)]
 for key,title,kind,a,b,keys,text,url,section in ROWS:
  common=dict(title=title,start=a,end=b,text=text,source=url,sourceLabel='Fuente institucional · investigación 1820–1839',precision=9 if a.endswith('-01-01') else 11,startIsCoverageBoundary=a.endswith('-01-01'),endIsCoverageBoundary=b.endswith('-01-01'),note='Ventana documental; los límites de cobertura no son fechas de acceso, cese o paz. No aporta geometría de frentes.')
  c['events'].append(dict(id=PREFIX+key,type=kind,countries=[{'QING':'QNG'}.get(k,k) for k in keys],**common))
  h['records'].append(dict(id=PREFIX+'record-'+key,keys=keys,section=section,**common))
 for key,name,y,z,date,label,url in [('FRA','Francia',1829,1830,'1830-08-09','De la Restauración a la Monarquía de Julio',FR),('BRA-EMPIRE','Imperio del Brasil',1830,1831,'1831-04-07','Del gobierno de Pedro I a las regencias',BR),('ESP','España',1832,1833,'1833-09-29','Sucesión y regencia',REG)]:
  h['relations'].append(dict(id=PREFIX+key,type='regime-transition',label=label,date=date,**{'from':dict(key=key,name=name,year=y),'to':dict(key=key,name=name,year=z)},source=url,sourceLabel='Fuente institucional'))
 c['startYear']=1820;h['coverageStart']='1820-01-01';return c,h
if __name__=='__main__':
 files=['historical-context.json','country-history.json'];old=[json.loads((OUT/f).read_text(encoding='utf8')) for f in files];new=prepare(*old);assert prepare(*new)==new
 for before,after,field in [(old[0],new[0],'events'),(old[1],new[1],'records'),(old[1],new[1],'relations')]:
  lookup={r['id']:r for r in after[field]}
  for r in before[field]:
   if not r['id'].startswith(PREFIX):assert lookup[r['id']]==r
 for f,d in zip(files,new):(OUT/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('Prepared14 phases,14 records and3 links')
