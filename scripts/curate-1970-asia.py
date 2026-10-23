"""Dated focal corrections, 1970s–1980s: Bulgaria, Mongolia and Asian states.

Default: print proposed terms without changing published JSON. Pass --apply only
after other acquisition writers have finished. Entity metadata is CC0; this
script does not download photographs or change the contemporary reference date.
The generic office import misses historical offices and undated P39 assertions.
An authority, party office and territorial control are separate statements.
"""
import argparse
import copy
import importlib.util
import json
import pathlib
import re

ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('historical',ROOT/'scripts/enrich-historical-authorities.py')
h=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(h)
TAG='manual-asia-bulgaria-0.8'
UNIFIED='1976-07-02'

# Verified historical offices useful for explicit P39 acquisition; current
# country P1906/P1313 alone does not enumerate these predecessor institutions.
OFFICES={
 'BGR':{'headState':'Q15893498','presidium':'Q12291358','headGovernment':'Q83529115'},
 'MNG':{'headGovernment':'Q903751','party':'Q5532176'},
 'NPL':{'monarch':'Q19700527'},
 'IRN':{'monarch':'Q184299','headGovernment':'Q13561063'},
 'MMR':{'headGovernment':'Q63212','president':'Q887124','party':'Q2464703'},
 'VDR':{'headState':'Q866680','headGovernment':'Q1043568'},
}
ARCHIVE='https://politburo.archives.bg/bg/2013-04-24-11-12-48/'
ZHIVKOV=ARCHIVE+'sekretnidokumenti/1950-1959/151'
TODOROV=ARCHIVE+'dokumenti/1950-1959/144'
FILIPOV=ARCHIVE+'dokumenti/1970-1979/110'
ATANASOV='https://politburo.archives.bg/en/2013-04-24-11-12-48/sekretnidokumenti/1980-1989/105'
MONGOLIA='https://tile.loc.gov/storage-services/public/gdcmassbookdig/mongoliacountrys00word_0/mongoliacountrys00word_0.pdf'
NEPAL='https://tile.loc.gov/storage-services/master/frd/copr/Nepal.pdf'
NEPALPM='https://opmcm.gov.np/pages/former-prime-ministers/'
NEPALARCHIVE='https://repository.narchives.gov.np/bitstreams/2c183c5a-e1d7-47a0-be68-790d210a8e8b/download'
IRAN='https://history.state.gov/historicaldocuments/frus1969-76v27/persons'
VIETNAM='https://history.state.gov/historicaldocuments/frus1969-76v10/persons'
TERMS=[]
def term(key,q,name,role,start,end,source,precision=11,note='',office=None,**extra):
    value=dict(person=q,name=name,role=role,start=start,end=end,source=source,
               precision=precision,curated=True,acquisition=TAG)
    if note:value['note']=note
    if office:value['office']=office
    value.update(extra)
    TERMS.append((key,value))

# The Bulgarian state archive dates Council-of-Ministers appointments several
# days differently from some secondary lists; its dates are preserved explicitly.
term('BGR','Q1811651','Georgi Traykov','Presidente del Presídium de la Asamblea Nacional · jefatura del Estado','1964-04-23','1971-07-07','https://www.wikidata.org/wiki/Q1811651',office='Q12291358',note='Jefatura formal anterior al Consejo de Estado de1971; no confundir con la presidencia parlamentaria posterior de Traykov.')
term('BGR','Q28517','Todor Zhivkov','Presidente del Consejo de Ministros · jefatura del Gobierno','1962-11-27','1971-07-09',ZHIVKOV,office='Q83529115')
term('BGR','Q28517','Todor Zhivkov','Presidente del Consejo de Estado · jefatura del Estado','1971-07-07','1989-11-17','https://www.bta.bg/en/news/archives/1199269-september-7-2026-115th-birth-anniversary-of-todor-zhivkov',office='Q15893498',note='BTA y el archivo estatal acreditan1971–17-11-1989. El día inicial procede deP39 Wikidata; otras tablas difieren algunos días. La salida de la jefatura del partido fue10-11, una función distinta.')
term('BGR','Q28517','Todor Zhivkov','Primer secretario / secretario general del Partido Comunista Búlgaro','1970-01-01','1989-11-10',ZHIVKOV,9,note='Ejercicio anterior a1970: el inicio es el límite de esta revisión, no su acceso al liderazgo. La secretaría general sucede al título de primer secretario en1981; el cese partidario no coincide con el de la jefatura del Estado.',startIsCoverageBoundary=True)
term('BGR','Q508037','Stanko Todorov','Presidente del Consejo de Ministros · jefatura del Gobierno','1971-07-09','1981-06-18',TODOROV,office='Q83529115')
term('BGR','Q939749','Grisha Filipov','Presidente del Consejo de Ministros · jefatura del Gobierno','1981-06-18','1986-03-24',FILIPOV,office='Q83529115',note='El archivo estatal fija el cese24-03-1986; la afirmación P39 con junio1986 no se reutiliza como mandato verificado.')
term('BGR','Q669384','Georgi Atanasov','Presidente del Consejo de Ministros · jefatura del Gobierno','1986-03-24','1990-02-08',ATANASOV,office='Q83529115',note='Fechas del archivo estatal. Q669384 es el político; Q5547103 corresponde a un homónimo y no debe usarse.')

term('MNG','Q275025','Yumjaagiin Tsedenbal','Presidente del Presídium del Gran Jural Popular · jefatura del Estado','1974-06-11','1984-08-23',MONGOLIA,10,note='La cronología de la Biblioteca del Congreso acredita el cambio de cargo en junio1974 y su retirada23-08-1984. El día inicial11 procede de la cronología de mandatos; se muestra precisión mensual.')
term('MNG','Q275025','Yumjaagiin Tsedenbal','Primer secretario del Partido Revolucionario del Pueblo Mongol','1970-01-01','1984-08-23',MONGOLIA,9,note='Liderazgo anterior a1970; inicio recortado a la revisión, no fecha de acceso. El cambio del Gobierno al Presídium en1974 no terminó la jefatura partidaria.',office='Q5532176',startIsCoverageBoundary=True)
term('MNG','Q558706','Jambyn Batmönkh','Presidente del Consejo de Ministros · jefatura del Gobierno','1974-06-11','1984-12-12',MONGOLIA,10,note='La fuente documenta el relevo del Gobierno en junio1974 y su elección al Presídium12-12-1984. Precisión mensual de la serie.',office='Q903751')
term('MNG','Q558706','Jambyn Batmönkh','Presidente del Presídium del Gran Jural Popular · jefatura del Estado','1984-12-12','1990-03-21',MONGOLIA,note='La elección12-12-1984 está documentada por la Biblioteca del Congreso; el cese1990 se conserva de la cronología P39 Wikidata.')

term('NPL','Q162306','Birendra Bir Bikram Shah','Rey de Nepal · jefatura del Estado','1972-01-31','2001-06-01',NEPALARCHIVE,note='Acceso31-01-1972 documentado en publicación conservada por el Archivo Nacional; reinado1972–2001 contrastado por la Biblioteca del Congreso. La coronación de1975 no es el comienzo del reinado.',office='Q19700527')
term('NPL','Q767596','Nagendra Prasad Rijal','Primer ministro · jefatura del Gobierno','1973-07-16','1975-12-01',NEPALPM,note='La oficina del primer ministro registra los periodos en calendarioBikramSambat; límites gregorianos cotejados con la cronología individual Wikidata. No se usan las fechas de la cartera de Defensa como si fueran otro nombramiento de primer ministro.')
term('NPL','Q983444','Surya Bahadur Thapa','Primer ministro · jefatura del Gobierno','1979-05-30','1983-07-12',NEPALPM,note='Periodo registrado en la lista gubernamental en calendarioBikramSambat; conversión y límites gregorianos proceden de la cronología individual Wikidata. La Biblioteca del Congreso también documenta su gobierno y caída en1983.')
term('NPL','Q767596','Nagendra Prasad Rijal','Primer ministro · jefatura del Gobierno','1986-03-21','1986-06-18',NEPALPM,note='Segundo mandato, distinto del de1973–1975. Lista gubernamental en calendarioBikramSambat, límites gregorianos de la cronología individual Wikidata.')
term('NPL','Q1113976','Marich Man Singh Shrestha','Primer ministro · jefatura del Gobierno','1986-06-18','1990-04-06',NEPALPM,note='La lista gubernamental y la Biblioteca del Congreso acreditan la llegada al Gobierno en1986; límites gregorianos de la cronología individual Wikidata.')

term('IRN','Q128245','Mohammad Reza Pahlavi','Shah de Irán · jefatura del Estado','1941-09-16','1979-02-11',IRAN,office='Q184299',note='FRUS identifica al shah durante el periodo; límites del reinado conservados del registro individual Wikidata. Su salida de Irán en enero1979 no equivale por sí sola al fin jurídico inmediato de la monarquía.')
term('IRN','Q471970','Amir-Abbas Hoveyda','Primer ministro · jefatura del Gobierno','1965-01-26','1977-08-07',IRAN,office='Q13561063',note='FRUS acredita ejercicio hasta agosto1977; límites diarios deP39 Wikidata. No confundir su nombramiento posterior como ministro de la Corte con continuidad de la jefatura del Gobierno.')
term('IRN','Q1442594','Jamshid Amouzegar','Primer ministro · jefatura del Gobierno','1977-08-07','1978-08-27','https://www.wikidata.org/wiki/Q1442594',office='Q13561063',note='La afirmaciónP39 del ítem está sin fechas; se completa con la cronología del gabinete, sin deducir incumbencia indefinida de esa afirmación.')
term('IRN','Q951044','Jafar Sharif-Emami','Primer ministro · jefatura del Gobierno','1978-08-27','1978-11-06','https://www.ojp.gov/pdffiles1/Digitization/77843NCJRS.pdf',office='Q13561063',note='La cronología diplomática publicada por el Departamento de Estado y preservada enNCJRS fecha la sustitución el6 de noviembre; P39 consigna5, por lo que se conserva la discrepancia de un día.')
term('IRN','Q700668','Gholam Reza Azhari','Primer ministro del Gobierno militar','1978-11-06','1979-01-05','https://www.ojp.gov/pdffiles1/Digitization/77843NCJRS.pdf',office='Q13561063',note='Nombramiento observado6-11-1978 y sustitución porBakhtiar en la cronología diplomática de5-01-1979. Otras cronologías sitúan dimisión y nombramiento entre31-12 y4-01; el extremo final se expresa como límite superior, no como un día de ejercicio confirmado.',endIsUpperBound=True)

term('MMR','Q315522','Ne Win','Presidente del Consejo Revolucionario · jefatura del Estado','1962-03-02','1974-03-02','https://www.wikidata.org/wiki/Q315522',note='Jefatura de la junta anterior al sistema constitucional de1974, distinta de la posterior presidencia de la República. No se proyecta la Constitución de1974 sobre1970–1973.')
term('MMR','Q315522','Ne Win','Primer ministro · jefatura del Gobierno','1962-03-02','1974-03-02','https://www.wikidata.org/wiki/Q315522',office='Q63212')
term('MMR','Q315522','Ne Win','Presidente del Partido del Programa Socialista de Birmania','1962-07-04','1988-07-23','https://www.wikidata.org/wiki/Q315522',office='Q2464703',note='La jefatura del partido se mantiene después del cese presidencial de1981; no equivale a continuar como presidente de la República.')

term('VDR','Q724317','Tôn Đức Thắng','Presidente de la República Democrática de Vietnam · jefatura del Estado','1969-09-23',UNIFIED,'https://www.wikidata.org/wiki/Q724317',note='Vietnam del Norte: entidad distinta de Vietnam unificado. Las fuentes vietnamitas de síntesis asocian su sucesión a la muerte deHồChíMinh el2-09; el mandato formalP39 conserva23-09. No se confunde unificación con una nueva elección de la misma persona.',office='Q866680')
term('VDR','Q358051','Phạm Văn Đồng','Primer ministro de la República Democrática de Vietnam','1955-09-20',UNIFIED,'https://web.mofa.gov.vn/vi/web/guest/tin-chi-tiet/chi-tiet/thu-tuong-bo-truong-pham-van-dong-tu-091954-den-021961--4902-167.html',note='Mandato de Vietnam del Norte. Continúa al frente del Gobierno tras la unificación; el corte de identidad no afirma una dimisión personal.',office='Q1043568')
term('RVN','Q313707','Nguyễn Văn Thiệu','Presidente de la República de Vietnam · jefatura del Estado','1967-10-31','1975-04-21',VIETNAM,note='Gobierno de Saigón, distinto del Gobierno Revolucionario Provisional. FRUS documenta su salida21-04-1975; el día inicial corresponde a su toma de posesión constitucional, distinta de la jefatura militar previa.')
term('RVN','Q1936777','Trần Văn Hương','Presidente de la República de Vietnam · jefatura del Estado','1975-04-21','1975-04-28',VIETNAM)
term('RVN','Q334419','Dương Văn Minh','Presidente de la República de Vietnam · jefatura del Estado','1975-04-28','1975-04-30',VIETNAM,note='Último Gobierno de la República de Vietnam; rendición30-04-1975. No se identifica con el Gobierno Revolucionario Provisional posterior.')
term('RVN','Q1937110','Trần Thiện Khiêm','Primer ministro de la República de Vietnam','1969-08-23','1975-04-05','https://www.wikidata.org/wiki/Q1937110')
term('RVN','Q1387616','Nguyễn Bá Cẩn','Primer ministro de la República de Vietnam','1975-04-05','1975-04-28','https://www.wikidata.org/wiki/Q1387616')
term('RVN','Q1924279','Vũ Văn Mẫu','Primer ministro de la República de Vietnam','1975-04-28','1975-04-30','https://www.wikidata.org/wiki/Q1924279')
term('VSR','Q337811','Huỳnh Tấn Phát','Presidente del Gobierno Revolucionario Provisional de la República de Vietnam del Sur','1969-06-08',UNIFIED,'https://nvsk.vnanet.vn/huynh-tan-phat-4462.vna',10,note='Gobierno revolucionario rival antes de la caída deSaigón y administración sureña después. VNA documenta junio1969–julio1976; precisión mensual. No acredita control de todo el territorio durante toda esa etapa.')
term('VSR','Q983839','Nguyễn Hữu Thọ','Presidente del Consejo Consultivo del Gobierno Revolucionario Provisional','1969-06-08',UNIFIED,'https://www.wikidata.org/wiki/Q983839',note='Órgano consultivo de la autoridad revolucionaria sureña, separado de su presidencia del Gobierno; no es la presidencia de la República de Vietnam deSaigón.')

for _,leader in TERMS:
    if leader.get('note'):
        leader['note']=re.sub(r'(?<=[a-zA-Záéíóúñ])(?=[0-9])|(?<=[0-9])(?=[a-zA-Záéíóúñ])',' ',leader['note'])
        for joined,separated in [('deP39','de P39'),('deHồChíMinh','de Hồ Chí Minh'),('formalP39','formal P39'),('deSaigón','de Saigón'),('porBakhtiar','por Bakhtiar'),('enNCJRS','en NCJRS'),('calendarioBikramSambat','calendario Bikram Sambat')]:
            leader['note']=leader['note'].replace(joined,separated)

def apply():
    path=ROOT/'public/data/identities.json'
    data=json.loads(path.read_text(encoding='utf8'))
    countries=data['countries']
    if 'VSR' not in countries:countries['VSR']=dict(qid='Q1072362',name='República de Vietnam del Sur · Gobierno Revolucionario Provisional',leaders=[],flags=[])
    for key in {key for key,_ in TERMS}:
        if key not in countries:raise ValueError('Missing curated identity: '+key)
    # Keep the post-unification portion of any continuous personal mandate.
    for leader in list(countries['VNM']['leaders']):
        if leader['start']>=UNIFIED:continue
        earlier=copy.deepcopy(leader)
        earlier['end']=min(earlier['end'],UNIFIED)
        earlier['note']=(earlier.get('note','')+' Tramo anterior a la unificación; pertenece a Vietnam del Norte.').strip()
        if earlier['start']<earlier['end']:countries['VDR']['leaders'].append(earlier)
        if leader['end']>UNIFIED:
            leader['start']=UNIFIED
            leader['note']=(leader.get('note','')+' Continuidad personal después de la unificación; el corte de entidad no afirma un nuevo nombramiento.').strip()
        else:countries['VNM']['leaders'].remove(leader)
    portraits={l['person']:l['portrait'] for c in countries.values() for l in c['leaders'] if l.get('portrait')}
    people={q:e for q,e in h.parallel(h.entity,sorted({l['person'] for _,l in TERMS})) if e}
    for q in {l['person'] for _,l in TERMS}:
        if not any(isinstance(v,dict) and v.get('id')=='Q5' for v in h.values(people.get(q,{}),'P31')):raise ValueError('Authority is not a verified human entity: '+q)
    for c in countries.values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
    for key,original in TERMS:
        leader=copy.deepcopy(original)
        # Replace matching generic assertions, retaining other governments and
        # previous curations. This avoids duplicate cards for the same office.
        countries[key]['leaders']=[l for l in countries[key]['leaders'] if not (
            not l.get('curated') and l['person']==leader['person'] and
            l['start']==leader['start'] and l['end']==leader['end'])]
        if leader['person'] in portraits:leader['portrait']=portraits[leader['person']]
        countries[key]['leaders'].append(leader)
    for c in countries.values():c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
    # Do not change retrieved/currentReferenceDate: contemporary symbols are
    # bounded by their own acquisition. This is historical enrichment only.
    data['historicalRetrieved']=h.TODAY
    h.save(path,data)
    print('Applied focal terms:',len(TERMS),'portraits reused:',sum(l['person'] in portraits for _,l in TERMS))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    if args.apply:apply()
    else:
        print(json.dumps({'terms':len(TERMS),'countries':sorted({key for key,_ in TERMS}),'offices':OFFICES},ensure_ascii=False,indent=2))
        print('Dry run only. Published JSON unchanged; use --apply after coordinating writers.')
