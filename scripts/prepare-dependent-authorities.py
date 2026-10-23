"""Dated territorial administration, distinct from sovereignty or succession.

Primary sources and scope in docs/DEPENDENCY-AUTHORITIES-RESEARCH.md.
Current reference stays fixed: researching history never extends incumbents.
"""
import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf8'))
def save(p,d):(root/p).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
records=[]
def relation(id,names,codes,admin,local,end,label,note,source,state_only=False):
 records.append(dict(id=id,names=names,codes=codes,admin=admin,localKey=local,start='1960-01-01',startIsCoverageBoundary=True,end=end,label=label,note=note,source=source,headOfStateOnly=state_only))
relation('angola',['Angola'],['AGO'],'PRT','AGO','1975-11-11','Administración portuguesa','Autoridades estatales portuguesas, distintas del gobernador general. Independencia el 11/11/1975; la transición de 1975 no se atribuye retrospectivamente al Gobierno independiente.','https://diariodarepublica.pt/dr/detalhe/acordo/1975-319897')
relation('mozambique',['Mozambique'],['MOZ'],'PRT','MOZ','1975-06-25','Administración portuguesa','Autoridades estatales portuguesas hasta la independencia del 25/6/1975. No equivalen a una presidencia mozambiqueña anterior a la independencia.','https://www.defesa.gov.pt/pt/defesa/organizacao/comissoes/cphm/rphm/edicoes/ano5/9_2025/3')
relation('guinea-bissau',['Guinea-Bissau'],['GNB'],'PRT','GNB','1974-09-10','Administración portuguesa · autoridad disputada desde 1973','La independencia se declaró el 24/9/1973; Portugal la reconoció el 10/9/1974. Las autoridades portuguesas aquí listadas no acreditan control de todo el territorio ni anulan las autoridades independentistas.','https://uniogbis.unmissions.org/pt-pt/chronology-events-3')
relation('namibia',['Namibia'],['NAM'],'ZAF','NAM','1990-03-21','Administración sudafricana efectiva · presencia declarada ilegal por la ONU','No es soberanía sudafricana reconocida. Las autoridades estatales sudafricanas se distinguen de la representación de SWAPO y del Estado namibio independiente desde el 21/3/1990.','https://www.unmissions.org/sites/default/files/past/untagFT.htm')
namibia=records[-1]
earlier=dict(namibia,id='south-west-africa-mandate',end='1966-10-27',label='África Sudoccidental · mandato administrado por Sudáfrica',note='Administración sudafricana bajo mandato anterior a su terminación por la Asamblea General el 27/10/1966. No es soberanía sudafricana ni se retroproyecta a 1960 la calificación jurídica posterior.',source='https://digitallibrary.un.org/record/660461?ln=en')
namibia.update(start='1966-10-27',startIsCoverageBoundary=False)
records.append(earlier)
relation('spanish-sahara',['Spanish Sahara','Sáhara Español'],['SAH','ESH'],'ESP','SAH','1976-02-27','Administración española · transición en 1975–1976','España comunicó el fin de su presencia el 26/2/1976. Los acuerdos de 1975 abrieron una administración temporal. Franco es autoridad estatal española, no gobernador local. No se proyecta automáticamente una autoridad marroquí sobre toda la superficie.','https://www.un.org/dppa/decolonization/es/nsgt/western-sahara')
relation('surinam',['Surinam','Suriname'],['SUR'],'NLD','SUR','1975-11-25','País autónomo del Reino de los Países Bajos','La jefatura del Estado del Reino se muestra junto al Gobierno surinamés. El primer ministro neerlandés no sustituye al Gobierno autónomo. Independencia el 25/11/1975.','https://www.royal-house.nl/members-royal-house/in-memoriam/queen-juliana/queen-of-the-netherlands',True)
relation('bahamas',['Bahamas'],['BHS'],'GBR','BHS','1973-07-10','Territorio con autogobierno interno bajo la Corona británica','Se distingue el Gobierno bahameño de la Corona. Desde la independencia del 10/7/1973, compartir monarca no implica dependencia británica.','https://www.legislation.gov.uk/uksi/1973/1080/article/1/made',True)
bahamas=records[-1]
records.append(dict(bahamas,id='bahamas-before-self-government',end='1964-01-07',headOfStateOnly=False,label='Bahamas · administración colonial británica',note='Etapa anterior al autogobierno interno de 1964. Las autoridades estatales británicas no sustituyen un inventario completo de gobernadores y órganos locales.',source='https://www.bahamashclondon.net/default/political/'))
bahamas.update(start='1964-01-07',startIsCoverageBoundary=False)
for id,names,codes in [('french-guiana',['French Guyana','French Guiana','Guayana Francesa'],['GUF']),('guadeloupe',['Guadeloupe','Guadalupe'],['GLP']),('martinique',['Martinique','Martinica'],['MTQ'])]:
 relation(id,names,codes,'FRA',codes[0],None,'Departamento / colectividad territorial de Francia','Forma parte de la República Francesa; la categoría cartográfica heredada «colonia» no describe por sí sola su estatus jurídico. Presidente y primer ministro franceses son autoridades estatales, distintas de prefectos y autoridades electas territoriales. Guayana pasa a colectividad territorial única en 2016.','https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000868445/2026-01-28')
relation('puerto-rico',['Puerto Rico'],['PRI'],'USA','PRI',None,'Estado Libre Asociado · territorio de Estados Unidos','Gobernador territorial y presidente de Estados Unidos tienen ámbitos distintos. El Commonwealth de 1952 no es independencia.','https://blogs.loc.gov/law/2022/11/the-commonwealth-of-puerto-rico-and-its-government-structure/')
records.append(dict(id='untea',names=['West Irian (Dutch New Guinea)'],codes=[],admin='UNTEA',localKey='',start='1962-10-01',end='1963-05-01',label='Nueva Guinea Occidental · administración temporal de la ONU',note='UNTEA ejerce desde el 1/10/1962 hasta la transferencia a Indonesia el 1/5/1963. La firma de agosto no es el inicio efectivo. Se distinguen Rolz-Bennett y Abdoh y sus fechas de ejercicio.',source='https://digitallibrary.un.org/record/860188/files/1122901-EM.pdf',headOfStateOnly=False))
for code,name,end,slug in [('KWT','Kuwait','1961-06-19','kuwait'),('BHR','Bahrain','1971-08-15','bahrain'),('QAT','Qatar','1971-09-03','qatar'),('BRN','Brunei','1984-01-01','brunei')]:
 records.append(dict(id='protected-'+code,names=[name],codes=[code],admin='GBR',localKey=code,start='1960-01-01',startIsCoverageBoundary=True,end=end,label='Estado protegido · gobernante local y protección británica diferenciados',note='Se conserva el gobernante local documentado. Las autoridades británicas figuran como autoridades externas del Estado protector, no como soberanos o primeros ministros del país protegido. Las series locales y las fechas de cada cargo deben contrastarse por separado.',source='https://history.state.gov/countries/'+slug,headOfStateOnly=False))
data=read('public/data/identities.json');countries=data['countries'];tag='dependent-authorities-0.8.1'
for c in countries.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=tag]
portraits={l['person']:l['portrait'] for c in countries.values() for l in c['leaders'] if l.get('portrait')}
terms=[
 ('ZAF','Q886942','Jacobus Johannes Fouché','Presidente del Estado · jefatura del Estado','1968-04-10','1975-04-09',11,'https://www.presidency.gov.za/history','Jefatura del Estado sudafricano; no es presidente de Namibia.'),
 ('SUR','Q333129','Johan Ferrier','Gobernador de Surinam','1968-03-15','1975-11-24',11,'https://gov.sr/archief-dr-johan-h-e-ferrier-overgedragen-aan-het-nas-op-de-46ste-verjaardag-van-de-republiek-suriname/','El 25/11/1975 pasa a presidente del Estado independiente: es otro cargo. El retrato disponible identifica a Ferrier y no representa su apariencia en 1970.'),
 ('SUR','Q924337','Jules Sedney','Primer ministro de Surinam · Gobierno autónomo','1969-11-20','1973-12-31',9,'https://gov.sr/wp-content/uploads/2025/01/AWJ-Nieuwsbrief-46ste-editie-01-2025.pdf','El boletín oficial acredita la toma de posesión del gabinete el 20/11/1969. El final se conserva con precisión anual 1973; no se afirma un cese el 31 de diciembre.'),
 ('BHS','Q920953','Lynden Pindling','Primer ministro de Bahamas · autogobierno anterior a la independencia','1970-01-01','1973-07-09',11,'https://www.bahamashclondon.net/default/political/','Autoridad ya en ejercicio al inicio de la revisión de 1970. El 10/7/1973 cambia el marco constitucional, sin afirmar dimisión personal.'),
 ('SAH','Q24279111','José María Pérez de Lema Tejero','Gobernador general del Sáhara bajo administración española','1970-01-01','1971-03-04',11,'https://www.boe.es/boe/dias/1971/03/05/','Ya ejercía antes de 1970. Su nombramiento consta en Decreto 135/1967 de 2 de febrero; no se confunde con la fecha posterior de toma de posesión. Cese por Decreto 348/1971 de 4 de marzo. No corresponde a una autoridad de la RASD.'),
]
for key,q,name,role,start,end,precision,source,note in terms:
 leader=dict(person=q,name=name,role=role,start=start,end=end,precision=precision,source=source,note=note,curated=True,acquisition=tag)
 if q=='Q924337':leader['endIsUpperBound']=True
 if key=='BHS':leader['startIsCoverageBoundary']=True;leader['endIsCoverageBoundary']=True
 if q=='Q24279111':leader['startIsCoverageBoundary']=True
 if q in portraits:leader['portrait']=portraits[q]
 countries[key]['leaders'].append(leader)
for c in countries.values():c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
save('public/data/identities.json',data)
save('public/data/territorial-administrations.json',dict(referenceDate=data['retrieved'],coverageStart='1960-01-01',intervals='Relation start inclusive, end exclusive; office intervals inclusive; include every relationship intersecting selected year.',license='Original factual compilation; individual documentary sources retained.',records=records))
print('Prepared',len(records),'territorial relationships and',len(terms),'sourced local/national offices.')
