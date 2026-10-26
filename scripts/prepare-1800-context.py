"""Sourced documentary phases; preserved prior context and no invented fronts."""
import pathlib,json,copy
OUT=pathlib.Path(__file__).resolve().parents[1]/'public/data';PREFIX='extension-1800-'
FR='https://www.assemblee-nationale.fr/gouv_parl/fiches_personnalites/Bonaparte.asp'
SHD='https://www.servicehistorique.sga.defense.gouv.fr/ark/41452'
ROWS=[
 ('consulate','Francia · Consulado','transition','1800-01-01','1804-05-18',['FRA'],'Napoleón es primer cónsul antes de la proclamación imperial. El consulado vitalicio de1802 no es todavía una monarquía imperial.',FR,'institutions'),
 ('empire','Francia · Primer Imperio','transition','1804-05-18','1814-04-06',['FRA'],'Proclamación imperial de mayo1804 y coronación de diciembre son hitos distintos; el primer reinado termina en1814.',FR,'institutions'),
 ('restoration-one','Francia · Primera Restauración','transition','1814-04-06','1815-03-20',['FRA'],'La primera restauración borbónica queda interrumpida por el regreso de Napoleón; no es una continuidad imperial.',SHD,'institutions'),
 ('hundred-days','Francia · Cien Días','transition','1815-03-20','1815-06-22',['FRA'],'Regreso y segunda abdicación de Napoleón. Las fases del año no se convierten en una única persona o un único frente anual.',FR,'institutions'),
 ('restoration-two','Francia · Segunda Restauración','transition','1815-07-08','1820-01-01',['FRA'],'El retorno de Luis XVIII es posterior a la segunda abdicación. El corte de cobertura no es el fin de su reinado.',SHD,'institutions'),
 ('peninsular','Guerra de la Independencia · campaña peninsular','conflict','1808-01-01','1815-01-01',['ESP','PRT','GBR','FRA'],'La invasión francesa y la resistencia española y portuguesa se combinan con la intervención británica. Los combates peninsulares de1808–1814 no justifican colorear todo el territorio como control uniforme.','https://www.nam.ac.uk/explore/peninsular-war','defense'),
 ('cadiz','España · Constitución de Cádiz','transition','1812-03-19','1814-05-04',['ESP'],'La Constitución reconoce a Fernando VII ausente y a la Regencia. La monarquía josefina y las instituciones fernandinas representan poderes rivales.','https://www.congreso.es/constitucion/ficheros/historicas/cons_1812.pdf','institutions'),
 ('louisiana','Compra de Luisiana','transition','1803-04-30','1804-01-01',['USA','FRA'],'Tratado de compra y transferencia territorial no son el mismo acto. La ausencia de pueblos indígenas en el inventario no implica tierra deshabitada.','https://www.archives.gov/milestone-documents/louisiana-purchase-treaty','territory'),
 ('war1812','Guerra angloestadounidense de1812','conflict','1812-01-01','1816-01-01',['USA','GBR','CAN'],'Conflicto iniciado en1812; paz de Gante firmada en diciembre1814 y ratificaciones en1815. Los extremos anuales son cobertura, no fechas diarias de declaración o paz.','https://www.archives.gov/milestone-documents/treaty-of-ghent','defense'),
 ('vienna','Congreso de Viena','transition','1814-01-01','1816-01-01',['FRA','GBR','RUE','AUSTRIAN-EMPIRE','PRUSSIA'],'En1814–1815 las potencias negocian el orden europeo. La participación diplomática no equivale a un bloque militar permanente ni aporta por sí misma geometría para cada Estado.','https://www.bundeskanzleramt.gv.at/en/federal-chancellery/visit-us/history/the-congress-of-vienna.html','relations'),
 ('haiti','Haití · independencia y división política','transition','1804-01-01','1820-01-01',['HTI','FRA'],'La declaración de independencia de1804 no es la proclamación imperial posterior. Tras Dessalines existen poderes del norte y del sur; la geometría de fuente no resuelve esa partición.','https://pegasus.law.columbia.edu/record/127791','institutions'),
 ('egypt','Egipto · gobierno de Muhammad Alí','transition','1805-01-01','1820-01-01',['EGY','OTT'],'Desde1805 Muhammad Alí establece su gobierno en Egipto. La autonomía efectiva no equivale a una república moderna ni elimina automáticamente la soberanía nominal otomana.','https://sis.gov.eg/en/egypt/history/egypts-history/modern-era/','institutions')]
def prepare(context,history):
 c,h=copy.deepcopy((context,history))
 for d,k in [(c,'events'),(h,'records'),(h,'relations')]:d[k]=[r for r in d[k] if not r['id'].startswith(PREFIX)]
 for ident,title,kind,a,b,keys,text,url,section in ROWS:
  common=dict(title=title,start=a,end=b,text=text,source=url,sourceLabel='Fuente documental · investigación1800–1819',precision=9 if a.endswith('-01-01') else 11,startIsCoverageBoundary=a.endswith('-01-01'),endIsCoverageBoundary=b.endswith('-01-01'),note='Observación documental. No reconstruye frentes; los límites de cobertura no son fechas de acceso, cese o paz.')
  c['events'].append(dict(id=PREFIX+ident,type=kind,countries=keys,**common));h['records'].append(dict(id=PREFIX+'record-'+ident,keys=keys,section=section,**common))
 for y,z,date,label in [(1803,1804,'1804-05-18','Del Consulado al Imperio'),(1813,1814,'1814-04-06','Del Imperio a la Primera Restauración'),(1814,1815,'1815-03-20','Regreso de Napoleón y sucesiones de1815')]:
  h['relations'].append(dict(id=PREFIX+str(z),type='regime-transition',label=label,date=date,**{'from':dict(key='FRA',name='Francia',year=y),'to':dict(key='FRA',name='Francia',year=z)},source=FR,sourceLabel='Asamblea Nacional francesa'))
 c['startYear']=1800;h['coverageStart']='1800-01-01';return c,h
if __name__=='__main__':
 files=['historical-context.json','country-history.json'];old=[json.loads((OUT/f).read_text(encoding='utf8')) for f in files];new=prepare(*old);assert prepare(*new)==new
 for before,after,k in [(old[0],new[0],'events'),(old[1],new[1],'records'),(old[1],new[1],'relations')]:
  lookup={r['id']:r for r in after[k]}
  for r in before[k]:
   if not r['id'].startswith(PREFIX):assert lookup[r['id']]==r
 for f,d in zip(files,new):(OUT/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 print('Prepared12 phases,12 records and3 links')
