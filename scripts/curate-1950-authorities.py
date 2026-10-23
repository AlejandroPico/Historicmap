"""Focal correction of1950s offices. Documentary coverage is never a fabricated term."""
import json,pathlib,copy
root=pathlib.Path(__file__).resolve().parents[1];path=root/'public/data/identities.json'
d=json.loads(path.read_text(encoding='utf8'));cs=d['countries'];tag='curated-1950-0.10'
portraits={l['person']:l['portrait'] for c in cs.values() for l in c['leaders'] if l.get('portrait')}
for c in cs.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=tag]
cs.setdefault('VSV',dict(qid='Q1193879',name='Estado de Vietnam',flags=[],leaders=[]))
cs.setdefault('MAL',dict(qid='Q1479726',name='Federación de Malaya',flags=[],leaders=[]))
def term(key,q,name,role,start,end,source,coverage=False,note='',precision=11):
 l=dict(person=q,name=name,role=role,start=start,end=end,source=source,precision=precision,curated=True,acquisition=tag,note=note)
 if coverage:l.update(startIsCoverageBoundary=True,endIsCoverageBoundary=True,note=note+' Ventana documental de ejercicio: sus extremos delimitan cobertura, no nombramiento ni dimisión. Los relevos diarios no contrastados siguen pendientes.')
 if q in portraits:l['portrait']=portraits[q]
 cs[key]['leaders'].append(l)
 return l
state='https://history.state.gov/'
term('YMK','Q400961','Ahmad bin Yahya','Imán y rey de Yemen','1950-01-01','1959-12-31',state+'historicaldocuments/frus1950v05/d755',True)
term('SLV','COLLECTIVE-SLV-1950','Consejo de Gobierno Revolucionario','Órgano colegiado de gobierno','1950-01-01','1950-08-31','https://commons.wikimedia.org/wiki/Presidents_of_El_Salvador',True)
term('SLV','Q293400','Óscar Osorio','Presidente de la República','1950-09-14','1956-09-13',state+'historicaldocuments/frus1955-57v07/d10',note='La entrega a Lemus se documenta el14/9/1956. El extremo final inclusivo es el día anterior a esa sucesión; los periodos de junta se mantienen separados.')
term('SLV','Q637768','José María Lemus','Presidente de la República','1956-09-14','1959-12-31',state+'historicaldocuments/frus1955-57v07/d10',True,note='Toma posesión el14/9/1956; el cierre1959 limita esta ampliación. No sustituye al mandato posterior curado de1960.')
term('BGR','Q460416','Valko Chervenkov','Presidente del Consejo de Ministros · jefatura del Gobierno','1950-02-03','1956-04-17','https://politburo.archives.bg/bg/2013-04-24-11-12-48/sekretnidokumenti/1944-1949/159',note='Fechas de los Archivos Estatales búlgaros; el18/4/1956 comienza la vicepresidencia del Consejo y deja la jefatura del Gobierno.')
term('LBY','Q116430','Idris I','Rey de Libia · jefatura del Estado','1951-12-24','1959-12-31','https://2001-2009.state.gov/p/nea/ci/ly/109175.htm',True,note='Rey desde la independencia del24/12/1951. La ventana termina al cierre de la nueva década, no con el fin de la monarquía.')
term('LBY','Q708587','Mahmud al-Muntasir','Primer ministro de Libia','1951-12-24','1953-12-31','https://2001-2009.state.gov/p/nea/ci/ly/109174.htm',True,note='Designado al independizarse y documentado como primer ministro en la visita de Dulles de28/5/1953. La fecha diaria del relevo de1954 continúa pendiente.')
term('PAN','Q887946','José Antonio Remón Cantera','Presidente de Panamá','1952-10-01','1955-01-02','https://colegioremoncantera.edu.pa/history-details.html',note='La institución panameña acredita1952–1955; el registro del Congreso estadounidense de2/4/1958 acredita el asesinato de2/1/1955 pero contiene una errata1951 en la investidura. No se adopta esa errata.',precision=9)
term('COL','Q734862','Roberto Urdaneta Arbeláez','Presidente designado · ejercicio de la jefatura del Estado','1951-11-05','1953-06-13','https://www.senalmemoria.co/la-voz-del-poder/laureano-eleuterio-gomez-castro',note='Sustituye a Laureano Gómez por enfermedad, hasta el golpe de Rojas Pinilla. Cargo de ejercicio, distinto de un mandato electoral propio.')
term('DOM','Q573982','Héctor Bienvenido Trujillo','Presidente de la República · jefatura formal del Estado','1952-08-16','1959-12-31','https://colecciones.agn.gob.do/opac/ficha.php?codopac=OPPUB&idpag=0554301467&informatico=00101663PI&suposi=4',True,note='El Archivo General de la Nación acredita la presidencia1952–1960. Se conserva resolución anual y un límite documental en1959; no se afirma cese en ese año.',precision=9)
term('ECU','Q707171','José María Velasco Ibarra','Presidente constitucional de Ecuador','1952-09-01','1956-08-31','https://www.vicepresidencia.gob.ec/wp-content/uploads/2018/12/Historial-Vicepresidentes-final.pdf')
term('URY','Q522975','Andrés Martínez Trueba','Presidente del Consejo Nacional de Gobierno · ejecutivo colegiado','1952-03-01','1955-02-28','https://archivo.presidencia.gub.uy/_web/noticias/2010/02/2010022810.htm',note='No es una presidencia unipersonal. El órgano colegiado se distingue de la presidencia de la República anterior.')
term('URY','Q728925','Luis Batlle Berres','Presidente del Consejo Nacional de Gobierno · ejecutivo colegiado','1955-03-01','1956-02-29','https://archivo.presidencia.gub.uy/_web/noticias/2010/02/2010022810.htm')
term('LAO','Q379794','Sisavang Vong','Rey de Laos · jefatura del Estado','1950-01-01','1959-10-28','https://www.wikidata.org/wiki/Q379794',True,note='Se mantiene el monarca anterior a Sisavang Vatthana. El inicio1950 es cobertura de esta revisión; no fecha de comienzo de la monarquía.')
term('SDN','Q255545','Ismail al-Azhari','Primer ministro de Sudán','1956-01-01','1956-06-30','https://reed.dur.ac.uk/xtf/view?docId=ark%2F32150_s10g354f257.xml',True,note='Primer ministro en la ceremonia de independencia. El relevo de julio se conserva sin asignar un día no contrastado.')
term('SDN','Q317595','Abdallah Khalil','Primer ministro de Sudán','1956-07-01','1958-11-16',state+'historicaldocuments/frus1958-60v14/d41',True,note='Gobierno anterior al golpe de17/11/1958; el inicio de julio es una ventana mensual de documentación, no fecha diaria de investidura.',precision=10)
# Wrong offices must be removed, not simply hidden by a competing duplicate.
cs['TWN']['leaders']=[l for l in cs['TWN']['leaders'] if not(l['person']=='Q699698' and l['start']<'1960')]
term('TWN','Q699698','Yan Xishan','Primer ministro de la República de China','1950-01-01','1950-02-28','https://english.culture.gov.taipei/News_Content.aspx?n=546DBBFFD75F4602&s=DDD335E7567F8B4A&sms=6606BE5E67AD9F4D',True,note='No fue presidente de la República. Chiang reanuda la presidencia el1/3/1950; el relevo gubernamental tiene fecha propia.')
for l in cs['DDR']['leaders']:
 if l['person']=='Q77210' and l['start']=='1949-10-07':l.update(start='1949-10-12',source='https://www.hdg.de/lemo/jahreschronik/1949.html',curated=True,note='Gobierno confirmado el12/10/1949; fundación de la RDA el7/10 no equivale a investidura de Grotewohl.')
for l in cs['GIN']['leaders']:
 if l['person']=='Q155402' and l['start']=='1958-01-01':l.update(start='1958-10-02',precision=11,source='https://documents.un.org/api/symbol/access?l=fr&s=S%2F2009%2F693&t=pdf',curated=True,note='Presidencia del Estado independiente desde2/10/1958, distinta de cargos territoriales anteriores.')
for l in cs['PRK']['leaders']:
 if l['person']=='Q41117' and l['start']=='1948-09-09' and 'Estado' in l['role']:
  l.update(role='Primer ministro · dirigente dominante',end=min(l['end'],'1972-12-27'),curated=True,note='Kim dirige el Gobierno antes de la presidencia creada en1972. La jefatura formal del Estado recae en el Presídium; no se retrotrae el título presidencial.')
term('PRK','Q334326','Kim Tu-bong','Presidente del Presídium · jefatura formal del Estado','1950-01-01','1957-09-19','https://beyondparallel.csis.org/wp-content/uploads/2017/03/China-DPRK-High-Level-Officials-Reference-List_FINAL_170315.pdf',True,note='Inventario documental de altos cargos; diferente del primer ministro Kim Il-sung.')
term('PRK','Q379667','Choe Yong-gon','Presidente del Presídium · jefatura formal del Estado','1957-09-20','1959-12-31','https://beyondparallel.csis.org/wp-content/uploads/2017/03/China-DPRK-High-Level-Officials-Reference-List_FINAL_170315.pdf',True)
term('PRK','Q41117','Kim Il-sung','Presidente de la República · jefatura del Estado','1972-12-28','1994-07-08','https://www.wikidata.org/wiki/Q41117',note='La presidencia se crea en1972. Se conserva el mandato posterior al corregir su atribución retrospectiva al periodo del primer ministro.')
# A republican president is not projected into the predecessor State of Vietnam.
term('VSV','Q223771','Bảo Đại','Jefe del Estado de Vietnam','1950-01-01','1955-10-25','https://avalon.law.yale.edu/20th_century/inch036.asp',True,note='Entidad asociada dentro del marco francés antes de la república de26/10/1955. El referéndum fue el23/10; no son la misma fecha.')
term('VSV','Q192502','Ngô Đình Diệm','Primer ministro del Estado de Vietnam','1954-07-07','1955-10-25','https://www.archives.gov/exhibits/remembering-vietnam-online-exhibit-episodes-1-4',True,note='Jefatura del Gobierno anterior a la presidencia republicana; no se presenta como presidente en1954.')
for l in cs['EGY']['leaders']:
 if l['start']<='1959-12-31' and l['end']>='1958-02-22':
  t=copy.deepcopy(l);t.update(start=max(t['start'],'1958-02-22'),end=min(t['end'],'1959-12-31'),acquisition=tag,curated=True,endIsCoverageBoundary=True)
  if t['start']<=t['end']:cs['UAR']['leaders'].append(t)
term('EGY','COLLECTIVE-EGY-RCC','Consejo del Mando de la Revolución · Gamal Abdel Nasser','Autoridad de facto y órgano de gobierno','1954-11-14','1956-06-22','https://sis.gov.eg/en/egypt/egyptian-figures/the-egyptian-revolutionary-command-council/',note='La presidencia electa de Nasser comienza después de esta etapa. La autoridad revolucionaria no se confunde con su posterior título presidencial. El organismo oficial sitúa el fin del Consejo el24/6; los días del relevo siguen sujetos a contraste.')
term('EGY','Q213001','Farouk I','Rey de Egipto · jefatura del Estado','1950-01-01','1952-07-25','https://sis.gov.eg/en/egypt/history/egypts-history/modern-era/',True,note='Abdica el26/7/1952 a favor de su hijo. El inicio1950 es cobertura; la monarquía de Farouk comenzó en1936.')
term('EGY','Q311796','Fuad II','Rey de Egipto · monarca menor bajo regencia','1952-07-26','1953-06-17','https://sis.gov.eg/en/egypt/history/egypts-history/modern-era/',note='Rey menor bajo regencia, distinto de la autoridad efectiva de los Oficiales Libres. La república se proclama el18/6/1953.')
for l in cs['MYS']['leaders']:
 if l['start']<='1963-09-15' and l['end']>='1957-08-31':
  t=copy.deepcopy(l);t.update(start=max(t['start'],'1957-08-31'),end=min(t['end'],'1963-09-15'),curated=True,acquisition=tag,note='Mandato en la Federación de Malaya antes de la formación de Malasia. El límite de entidad no es una dimisión personal.')
  if l['start']<'1957-08-31':t['startIsCoverageBoundary']=True
  if l['end']>'1963-09-15':t['endIsCoverageBoundary']=True
  cs['MAL']['leaders'].append(t)
for c in cs.values():c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
path.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
print('Prepared',sum(l.get('acquisition')==tag for c in cs.values() for l in c['leaders']),'focal1950 records.')
