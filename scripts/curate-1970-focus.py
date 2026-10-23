"""Source-bounded corrections for historical offices absent from current office lists.

Keeps party leadership, formal offices and effective control distinct. Media are
reused from the licensed catalogue; new photographs are acquired separately.
"""
import importlib.util, json, pathlib
spec=importlib.util.spec_from_file_location('h',pathlib.Path(__file__).with_name('enrich-1970-authorities.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
data=json.loads((h.OUT/'data/identities.json').read_text(encoding='utf8'))
c=data['countries'];tag='curated-focus-0.8'
for country in c.values():country['leaders']=[l for l in country['leaders'] if l.get('acquisition')!=tag]
terms=[
 ('YUG','Q9161','Josip Broz Tito','Presidente de la República','1953-01-14','1980-05-04',11,'https://arhivyu.rs/en/novosti/iz-rada-arhiva/preuzet-arhiv-josipa-broza-tita-od-muzeja-istorije-jugoslavije','El archivo del gabinete presidencial acredita la etapa 1953–1980; los días del mandato corresponden al registro biográfico P39 de Wikidata Q9161. La presidencia rotatoria posterior se documenta por separado.'),
 ('CHL','Q368','Augusto Pinochet','Presidente de la Junta Militar · autoridad de facto','1973-09-11','1974-12-16',11,'https://www.bcn.cl/conmemoracion50-septiembre-1973/golpe_estado.html','Jefatura de la Junta desde el golpe; la denominación Presidente de la República se adopta en diciembre de 1974.'),
 ('CHL','Q368','Augusto Pinochet','Presidente de la República · dictadura militar','1974-12-17','1990-03-11',11,'https://www.memoriachilena.gob.cl/602/w3-article-92413.html','La etapa anterior a la entrada en vigor constitucional de 1981 también pertenece a su presidencia; no debe dejar vacía la ficha de 1974–1980.'),
 ('AFG','Q299559','Nur Muhammad Taraki','Presidente del Consejo Revolucionario · jefatura del Estado','1978-04-30','1979-09-14',11,'https://www.wikidata.org/wiki/Q299559','Consejo creado tras el golpe de abril de 1978, contextualizado por la Biblioteca del Congreso: https://tile.loc.gov/storage-services/service/ll/llglrd/2019669455/2019669455.pdf . Fechas del mandato en la afirmación biográfica fechada.'),
 ('AFG','Q63827','Babrak Karmal','Presidente del Consejo Revolucionario · jefatura del Estado','1979-12-27','1986-11-24',11,'https://www.wikidata.org/wiki/Q63827','Se distingue la presidencia del Consejo de su mandato más corto como primer ministro. Su instalación tras la intervención soviética se documenta en https://history.state.gov/milestones/1977-1980/soviet-invasion-afghanistan . No implica control efectivo de todo el territorio.'),
 ('KHM','Q379197','Heng Samrin','Presidente del Consejo Popular Revolucionario · Gobierno de Phnom Penh','1979-01-01','1981-05-31',10,'https://mofa.gov.vn/tin-chi-tiet/chi-tiet/chu-tich-qh-vuong-quoc-campuchia-samdech-heng-samrin-tham-huu-nghi-chinh-thuc-nuoc-ta--589.html','La biografía institucional fecha enero de 1979 y junio de 1981 con precisión mensual. Los límites de mes son representación del intervalo documentado, no días exactos de nombramiento. Existían autoridades rivales y una disputa de representación internacional.'),
 ('KHM','Q39464','Pol Pot','Secretario del Partido Comunista de Kampuchea · autoridad de facto','1975-04-17','1979-01-07',11,'https://www.eccc.gov.kh/en/directory/khmer-rouge-profile/saloth-sar','Se registra la dirección efectiva del régimen entre la toma y la pérdida de Phnom Penh, sin confundirla con el cargo de primer ministro, que tuvo una interrupción en 1976. Su actividad insurgente posterior no equivale a gobernar todo Camboya.'),
 ('KHM','Q379197','Heng Samrin','Presidente del Consejo de Estado · Gobierno de Phnom Penh','1981-06-01','1989-12-31',10,'https://mofa.gov.vn/tin-chi-tiet/chi-tiet/chu-tich-qh-vuong-quoc-campuchia-samdech-heng-samrin-tham-huu-nghi-chinh-thuc-nuoc-ta--589.html','Elección al Consejo de Estado documentada en junio de 1981 con precisión mensual. Aquí se acredita la fase hasta el límite de la revisión de 1989, no una dimisión en diciembre. El poder de este Gobierno y su dependencia vietnamita durante la década se contrastan en https://2009-2017.state.gov/outofdate/bgn/cambodia/124187.htm ; no equivale a reconocimiento internacional o control uniforme de todo el país.'),
 ('NPL','Q313110','Mahendra Bir Bikram Shah','Rey de Nepal · jefatura del Estado','1955-03-13','1972-01-31',11,'https://www.wikidata.org/wiki/Q313110','Cronología del reinado P39, distinta de la presidencia republicana posterior y del reinado de Birendra.'),
 ('LAO','Q379797','Sisavang Vatthana','Rey de Laos · jefatura del Estado','1959-10-29','1975-12-02',11,'https://www.wikidata.org/wiki/Q379797','Cronología del cargo monárquico P39. La monarquía termina en 1975; no se le atribuye la jefatura de la república posterior.'),
]
portraits={l['person']:l['portrait'] for country in c.values() for l in country['leaders'] if l.get('portrait')}
for key,q,name,role,start,end,precision,source,note in terms:
 term=dict(person=q,name=name,role=role,start=start,end=end,precision=precision,source=source,note=note,curated=True,acquisition=tag)
 if key=='KHM' and q=='Q379197' and start=='1981-06-01':term['endIsCoverageBoundary']=True
 if q in portraits:term['portrait']=portraits[q]
 c[key]['leaders'].append(term)
for country in c.values():country['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
h.save(h.OUT/'data/identities.json',data)
print('Applied',len(terms),'bounded focal historical offices.')
