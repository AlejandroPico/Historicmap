"""Offline incremental context, institutions and coalitions for 1900–1919.

Run after prepare-1920-context.py. --check validates in memory without writing.
Existing organizations, memberships, later phases and referenceDate are preserved.
The new war coalitions are explicitly focal observations, not legal organizations
or complete lists of belligerents. No event supplies geographic front geometry.
"""
import argparse
import copy
import datetime
import json
import pathlib

PREFIX = 'extension-1900-'
ROOT = pathlib.Path(__file__).resolve().parents[1] / 'public/data'
STATE = 'https://history.state.gov/'
NAM = 'https://ww1.nam.ac.uk/timeline/'
RUSSIA = 'https://www.dhm.de/lemo/kapitel/erster-weltkrieg/kriegsverlauf/russische-revolution'
CHINA = STATE+'milestones/1899-1913/chinese-rev'
MEXICO = 'https://www.loc.gov/exhibits/mexican-revolution-and-the-united-states/constitution-of-1917.html'
MEX_CONSTITUTION = 'https://www.ordenjuridico.gob.mx/Documentos/Federal/html/wo14166.html'
AUSTRIA = 'https://www.parlament.gv.at/verstehen/historisches/1918-1945/ausrufung-republik'
PCA = 'https://pca-cpa.org/en/about/introduction/contracting-parties/'
ITU = 'https://www.itu.int/en/history/Pages/ITUBorn1865.aspx'
UPU = 'https://www.upu.int/UPU/media/upu/files/UPU/aboutUpu/acts/manualsInThreeVolumes/actInThreeVolumesConstitutionAndGeneralRegulationsEn.pdf'
ALLIANCE = 'https://worldjpn.net/documents/texts/docs/18820520.T1E.html'
ITALY_BREAK = 'https://goriziagrandeguerra.cultura.gov.it/timeline-1915/'
ITALY_WAR = 'https://www.senato.it/application/xmanager/projects/leg18/file/repository/relazioni/biblioteca/emeroteca/Il_Giornale_dei_giornali/0009GdG.pdf'
ARMISTICE = 'https://api.parliament.uk/historic-hansard/commons/1918/nov/11/prime-ministers-statement'
PEACE = 'https://www.archives.gov/files/research/foreign-policy/related-records/rg-256-inventory.pdf'
SERBIA = 'https://www.parlament.gov.rs/narodna-skupstina-/istorijat/istorijat-1804---1918.937.html'
CALENDAR = 'Las fechas rusas se expresan en calendario gregoriano; febrero y octubre son los nombres históricos según el calendario juliano.'
WINDOW = 'Ventana documental con fin exclusivo. Los cortes anuales no son declaraciones de guerra, dimisiones o tratados de paz. Las claves vinculan fichas; no generan frentes ni forman un censo de beligerantes.'


def prepare(affiliations, context, history):
    d, c, h = copy.deepcopy((affiliations, context, history))
    new_org_ids = {'tripleAlliance', 'centralPowersWW1', 'alliesWW1'}
    d['organizations'] = [o for o in d['organizations'] if o['id'] not in new_org_ids]
    c['events'] = [e for e in c['events'] if not e['id'].startswith(PREFIX)]
    h['records'] = [r for r in h['records'] if not r['id'].startswith(PREFIX)]
    h['relations'] = [r for r in h['relations'] if not r['id'].startswith(PREFIX)]

    def organization(oid, label, formed, dissolved, source, description):
        o = dict(id=oid,label=label,type='military',formed=formed,dissolved=dissolved,source=source,description=description,memberships=[])
        d['organizations'].append(o)
        return o

    def member(org, code, start, end, note, source, category='member', coverage=False):
        m = dict(code=code,start=start,end=end,category=category,note=note,source=source)
        if coverage:
            m['startIsCoverageBoundary'] = True
        org['memberships'].append(m)

    triple = organization('tripleAlliance','Triple Alianza · tratado defensivo','1882-05-20','1915-05-03',ALLIANCE,'Tratado defensivo firmado en 1882 y renovado sucesivamente; observaciones desde 1900. Italia sigue vinculada durante su neutralidad de 1914 y denuncia la alianza el 3/5/1915. La firma original no se confunde con un día de ratificación aquí no contrastado. Termina esta configuración tripartita, no toda relación austro-alemana.')
    for code in ('DEU','AUH','ITA'):
        member(triple,code,'1900-01-01','1915-05-03','En vigor al inicio de la revisión de 1900; no fecha de adhesión. El tratado se firmó el 20/5/1882. La neutralidad italiana de 1914 no equivale a retirada ni beligerancia automática. Fin: denuncia italiana de 3/5/1915.',ITALY_BREAK,coverage=True)

    central = organization('centralPowersWW1','Potencias Centrales · coalición de guerra','1914-07-28','1918-11-11',NAM,'Coalición de guerra, distinta del tratado de la Triple Alianza. Cuatro potencias documentadas; los intervalos siguen entrada y cese operativo por armisticio, no un registro completo del estado jurídico de guerra. Las fechas no codifican horas dentro del día ni fronteras de ocupación.')
    for code,start,end,source,note in [
        ('AUH','1914-07-28','1918-11-04','https://nationalarchives.gov.fk/jdownloads/Gazettes%20Proclamations%20Notices/1918%20to%201921.%20R27%20to%20R30.pdf','Declaración contra Serbia el 28/7/1914. Armisticio de Villa Giusti firmado el 3/11/1918 y efectivo el 4/11; no fecha única de disolución territorial de la monarquía.'),
        ('DEU','1914-08-01','1918-11-11',NAM,'Entrada contra Rusia el 1/8/1914; armisticio con los Aliados efectivo el 11/11/1918. No tratado de paz.'),
        ('OTT','1914-11-02','1918-10-31','https://nzhistory.govt.nz/war/ottoman-empire-facts','Se sigue la declaración rusa de 2/11/1914, posterior al ataque naval otomano de octubre; no firma de la alianza germano-otomana. Mudros se firma el 30/10/1918 y el cese es efectivo el 31/10.'),
        ('BGR','1915-10-14','1918-09-30','https://nzhistory.govt.nz/war/bulgaria-facts','Declaración contra Serbia el 14/10/1915. Armisticio de Salónica firmado el 29/9/1918 y efectivo el 30/9; el tratado de paz es posterior.')]:
        member(central,code,start,end,note,source)

    allies = organization('alliesWW1','Aliados y asociados · Primera Guerra Mundial (focal)','1914-07-28','1918-11-11',NAM,'Cobertura parcial de siete potencias principales y las autoridades rusas sucesivas. Coalición operativa, no adhesión a una organización ni lista mundial completa: faltan aquí Japón, China, Portugal, Rumanía, Grecia y otros participantes. Reino Unido representa su entrada imperial; los dominios no se duplican como miembros de un tratado. Estados Unidos es potencia asociada, no parte de los acuerdos aliados previos.')
    for code,start,end,source,note,category in [
        ('SRK','1914-07-28','1918-11-11',NAM,'Serbia entra tras la declaración austrohúngara. La ocupación posterior no extingue automáticamente al Gobierno o la participación serbia.','member'),
        ('RUE','1914-08-01','1917-03-15','https://nzhistory.govt.nz/war/russian-empire-facts','Rusia imperial, no Federación de Rusia actual. Fin por cambio de autoridad tras la abdicación, no retirada rusa de la guerra en marzo.','member'),
        ('RPR','1917-03-15','1917-11-07',RUSSIA,'El Gobierno provisional continúa la guerra; no nueva adhesión. Fecha gregoriana de relevo, distinta de la proclamación republicana formal de septiembre.','member'),
        ('RSR','1917-11-07','1917-12-15','https://nzhistory.govt.nz/war/russian-empire-facts','Autoridad soviética hasta el armisticio de 15/12/1917. Este fin indica cese operativo; la paz de Brest-Litovsk se firma el 3/3/1918 y no se anticipa a 1917.','member'),
        ('FRA','1914-08-03','1918-11-11',NAM,'Entrada tras la declaración alemana de guerra; fin operativo por armisticio con Alemania, no tratado de paz.','member'),
        ('BEL','1914-08-04','1918-11-11',NAM,'La invasión alemana incorpora a Bélgica a la guerra; el Gobierno conserva una condición distinta de país totalmente anexionado.','member'),
        ('GBR','1914-08-04','1918-11-11',NAM,'Entrada del Imperio británico: no se atribuye a cada dominio una adhesión independiente al mismo acuerdo.','member'),
        ('ITA','1915-05-24','1918-11-11',ITALY_WAR,'La denuncia de la Triple Alianza el 3/5 precede a la declaración contra Austria-Hungría de 23/5 y al estado de guerra desde 24/5. No era beligerante en 1914.','member'),
        ('USA','1917-04-06','1918-11-11',STATE+'milestones/1914-1920/paris-peace','Potencia asociada desde su declaración contra Alemania de 6/4/1917; no se obliga automáticamente por los acuerdos secretos anteriores de los Aliados.','associate')]:
        member(allies,code,start,end,note,source,category)

    def event(ident,title,kind,start,end,keys,text,source,note=WINDOW):
        c['events'].append(dict(id=PREFIX+ident,title=title,type=kind,start=start,end=end,countries=keys.split(),text=text,source=source,sourceLabel='Archivo o institución responsable · investigación 1900–1919',note=note))

    events = [
        ('boer','Guerra sudafricana · fase de 1900–1902','conflict','1900-01-01','1902-06-01','GBR ZAF','La guerra iniciada en 1899 continúa con ocupaciones, resistencia guerrillera y campos de concentración. El tratado de Vereeniging se firma el 31/5/1902. Inicio 1900: límite de esta revisión, no inicio del conflicto.','https://www.nam.ac.uk/explore/boer-war'),
        ('philippines','Guerra filipino-estadounidense','conflict','1900-01-01','1902-07-05','PHL USA','La fase guerrillera iniciada en 1899 continúa hasta la declaración estadounidense de final del 4/7/1902. Persisten resistencias posteriores; el anuncio no certifica paz o control uniforme de todo el archipiélago.',STATE+'milestones/1899-1913/war'),
        ('boxers','China · rebelión bóxer e intervención extranjera','conflict','1900-01-01','1901-09-08','QNG JPN RUE GBR FRA DEU USA','El asedio de las legaciones y la intervención de una coalición extranjera desembocan en el protocolo firmado el 7/9/1901. La ventana anual no afirma combate continuo desde enero ni contiene la delimitación de cada concesión.',STATE+'historicaldocuments/frus1901China/d178'),
        ('australia','Federación de Australia','transition','1901-01-01','1902-01-01','AUS GBR','Seis colonias se federan como Commonwealth of Australia. La ley británica y su asentimiento son de 1900, mientras la federación se hace efectiva el 1/1/1901. No equivale a independencia exterior plena.','https://peo.gov.au/understand-our-parliament/history-of-parliament/federation/federation'),
        ('cuba','República cubana y fin de la primera ocupación','transition','1902-05-20','1903-01-01','CUB USA','El Gobierno republicano se inaugura el 20/5/1902 tras la ocupación estadounidense. Las condiciones de intervención y arrendamiento de bases limitan la relación posterior; no se confunden con la soberanía colonial española. ',STATE+'countries/cuba'),
        ('panama','Separación de Panamá de Colombia','transition','1903-11-03','1904-01-01','PAN COL USA','Panamá proclama su separación el 3/11; el reconocimiento estadounidense llega el 6/11. El territorio de la futura zona del canal tiene un régimen diferente del resto de Panamá.',STATE+'countries/panama'),
        ('russo-japanese','Guerra ruso-japonesa','conflict','1904-02-01','1905-10-01','RUE JPN QNG','Las operaciones en Corea, Manchuria y el mar preceden a la paz de Portsmouth de septiembre 1905. El inicio y fin son ventanas mensuales; la firma del tratado no es la fecha de todos los relevos locales de control.',STATE+'milestones/1899-1913/portsmouth-treaty'),
        ('herero-nama','Guerra colonial y genocidio herero y nama','conflict','1904-01-12','1909-01-01','NAM DEU','La guerra colonial alemana incluye exterminio, expulsión al desierto e internamiento. Las resistencias y los campos se prolongan hasta 1908; el cierre 1909 es límite anual. No se añade una cifra de víctimas o un frente sin fuente específica.','https://www.dhm.de/archiv/ausstellungen/namibia/rooms/02.htm'),
        ('russia-1905','Revolución y reformas en el Imperio ruso','transition','1905-01-01','1907-01-01','RUE','Protestas, huelgas y violencia revolucionaria acompañan la crisis de la monarquía y las reformas parlamentarias. Ventana 1905–1906: no fecha jurídica de la Duma ni fin definitivo del autoritarismo.','https://www.prlib.ru/node/619233'),
        ('iran-constitution','Persia · revolución constitucional y Asamblea','transition','1906-08-06','1908-01-01','IRN','El decreto de agosto dispone una Asamblea y el texto constitucional de 30/12/1906 regula sus funciones. La monarquía continúa; no se atribuyen al sah todas las funciones parlamentarias ni se anticipan las normas suplementarias.','https://irandataportal.syr.edu/wp-content/uploads/iran1906.pdf'),
        ('new-zealand','Nueva Zelanda adopta el título de dominio','transition','1907-09-26','1908-01-01','NZL GBR','El cambio de colonia a dominio entra en efecto el 26/9/1907. No concede por sí solo independencia diplomática plena ni cambia instantáneamente todas las instituciones.','https://www3.parliament.nz/en/pb/research-papers/document/00PLLawRP07041/new-zealand-sovereignty-1857-1907-1947-or-1987/'),
        ('congo','Del Estado Independiente del Congo al Congo Belga','transition','1908-11-15','1909-01-01','COD BEL','La ley de gobierno colonial votada el 18/10/1908 entra en efecto el 15/11. La administración belga sustituye al Estado ligado a Leopoldo II; no se presenta esa entidad como la república congoleña contemporánea.','https://www.arch.be/index.php?a=2022-09-27-traite-de-cession-de-l-etat-independant-du-congo-a-la-belgique&l=fr&m=actualites&r=toutes-les-actualites'),
        ('south-africa','Constitución de la Unión Sudafricana','transition','1910-05-31','1911-01-01','ZAF GBR','La Unión reúne cuatro colonias bajo un Gobierno de dominio. Su sistema político excluye a la mayor parte de la población negra; federación imperial, igualdad cívica y soberanía exterior plena son cuestiones distintas.','https://www.concourt.org.za/index.php/constitution/history'),
        ('portugal','Portugal · proclamación republicana','transition','1910-10-05','1911-08-22','PRT','La revolución del 5/10/1910 abre un Gobierno provisional. La Constitución se aprueba el 21/8/1911 y el primer presidente constitucional se elige después: no son el mismo cargo o hito.','https://www.parlamento.pt/Parlamento/Paginas/120A-SSessoes-IRepublica.aspx'),
        ('mexico-1910','Revolución mexicana · levantamiento y caída de Díaz','conflict','1910-01-01','1912-01-01','MEX','La crisis electoral y los levantamientos de 1910 desembocan en la salida de Díaz en 1911. Inicio anual de cobertura; no se atribuye a una facción todo el territorio ni se identifica la renuncia con el final de la revolución.','https://www.loc.gov/exhibits/mexican-revolution-and-the-united-states/'),
        ('china-revolution','Revolución china y caída de los Qing','transition','1911-10-01','1912-02-13','QNG ROC','Las rebeliones del otoño de 1911 preceden a la República proclamada en 1912 y a la abdicación imperial. Presidencia republicana y corte Qing se superponen brevemente; la República Popular no existe en este periodo.',CHINA),
        ('italo-turkish','Guerra ítalo-otomana y ocupación italiana','conflict','1911-09-29','1912-10-19','ITA OTT LBY','Italia declara la guerra el 29/9/1911. La paz de Lausana de 18/10/1912 no garantiza el cumplimiento inmediato de las retiradas pactadas ni control colonial italiano uniforme.','https://www.senato.it/legislature/regno/italia/23/resoconti-elenco-cronologico'),
        ('balkan-one','Primera guerra balcánica','conflict','1912-10-01','1913-06-01','OTT SRK MNK BGR GRC ALB','La coalición balcánica combate al Imperio otomano y altera su presencia europea. Las fechas son ventanas mensuales; no afirman un único frente ni el reconocimiento simultáneo de todas las reivindicaciones.','https://militarymuseum.bg/en/exhibitions/chronological-exhibition/the-bulgarian-army-in-the-balkan-wars-1912-1913/'),
        ('balkan-two','Segunda guerra balcánica','conflict','1913-06-01','1913-09-01','BGR SRK GRC ROU OTT','Los antiguos aliados disputan los territorios de la primera guerra. Ventana de junio a agosto: la paz y los acuerdos bilaterales no se convierten en un mismo día de control efectivo.','https://militarymuseum.bg/en/exhibitions/chronological-exhibition/the-bulgarian-army-in-the-balkan-wars-1912-1913/'),
        ('mexico-1913','México · golpe de 1913 y guerra de facciones','conflict','1913-02-01','1917-01-01','MEX USA','El golpe de Huerta y su posterior caída son seguidos por lucha entre constitucionalistas y convencionistas. La ventana termina por cobertura; la Constitución de 1917 no elimina de inmediato la violencia regional.',MEXICO),
        ('ww1-1914','Primera Guerra Mundial · crisis y campañas de 1914','conflict','1914-07-28','1915-01-01','AUH SRK RUE DEU FRA BEL GBR','La guerra austro-serbia se amplía mediante declaraciones sucesivas. La invasión de Bélgica y las campañas iniciales no implican que todos los aliados o imperios entrasen el 28/7.',NAM),
        ('ww1-1915','Primera Guerra Mundial · ampliación en 1915','conflict','1915-01-01','1916-01-01','DEU AUH RUE OTT BGR ITA GBR FRA','Se amplían los frentes y participantes. Italia entra contra Austria-Hungría y Bulgaria contra Serbia. El comienzo de año es una ventana documental, no nueva declaración colectiva.',NAM),
        ('gallipoli','Campaña de Gallípoli','conflict','1915-04-25','1916-01-10','OTT GBR FRA AUS NZL','Los desembarcos aliados del 25/4/1915 son seguidos por combates y evacuaciones escalonadas hasta enero 1916. Esta fase no aporta líneas de trinchera ni equivale al conjunto de la guerra otomana.','https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/426255/GallipoliCommemoration_London.pdf'),
        ('armenians','Genocidio de los armenios otomanos','conflict','1915-04-01','1917-01-01','OTT ARM','Las autoridades otomanas organizan deportaciones y matanzas masivas de la población armenia. Abril es una ventana de fase; no pretende que toda la persecución comenzara el mismo día o terminara con el corte de 1917.','https://www.ushmm.org/genocide/armenia'),
        ('haiti','Ocupación estadounidense de Haití','conflict','1915-07-01','1920-01-01','HTI USA','Los marines intervienen tras la crisis presidencial de julio. La ocupación y el control financiero continúan después de 1919, hasta 1934; el final 1920 es únicamente el límite de esta ampliación.',STATE+'milestones/1914-1920/haiti'),
        ('ww1-1916','Primera Guerra Mundial · campañas de 1916','conflict','1916-01-01','1917-01-01','DEU AUH RUE OTT GBR FRA ITA','La guerra de desgaste se intensifica en varios teatros. Las campañas del Somme y Verdún no se interpolan como frentes diarios sobre los contornos de país.',NAM),
        ('ireland','Alzamiento de Pascua en Irlanda','conflict','1916-04-24','1917-01-01','IRL GBR','La proclamación republicana acompaña al alzamiento de Dublín del 24/4/1916. Su derrota no equivale a independencia irlandesa en 1916; el cierre anual no es la duración exacta del combate.','https://www.gov.ie/en/department-of-the-taoiseach/publications/the-1916-rising/'),
        ('dominican','Ocupación de la República Dominicana','conflict','1916-01-01','1920-01-01','DOM USA','La intervención militar y el régimen de ocupación de 1916 reciben protestas dominicanas. Inicio y fin son límites de cobertura anual; no se asigna a Estados Unidos soberanía por el hecho de ocupar.',STATE+'historicaldocuments/frus1916/comp11'),
        ('ww1-1917','Primera Guerra Mundial · cambios de 1917','conflict','1917-01-01','1918-01-01','DEU AUH RUE RPR RSR GBR FRA ITA USA','La entrada estadounidense y las revoluciones rusas alteran la coalición. Una potencia asociada no está obligada automáticamente por los tratados previos de los Aliados.','https://www.archives.gov/topics/wwi'),
        ('russia-february','Revolución de Febrero y Gobierno provisional','transition','1917-03-08','1917-11-07','RUE RPR','La crisis desemboca en la abdicación de Nicolás II el 15/3 gregoriano y en un Gobierno provisional que continúa la guerra. El cambio de Gobierno no establece inmediatamente una república constitucional consolidada.',RUSSIA),
        ('russia-october','Revolución de Octubre y poder soviético','transition','1917-11-07','1918-01-01','RPR RSR','Los bolcheviques desplazan al Gobierno provisional. La toma de poder inicia otra fase institucional y no constituye la fundación de la URSS, que es posterior.',RUSSIA),
        ('finland','Finlandia · declaración de independencia','transition','1917-12-06','1918-01-01','FIN RSR','El Parlamento adopta la declaración de independencia el 6/12. El reconocimiento soviético llega el 31/12; declaración, reconocimiento y control territorial no son el mismo hecho.','https://valtioneuvosto.fi/en/-/finland-s-centenary-is-filled-with-joy-and-dignity'),
        ('mexico-constitution','México · Constitución de 1917','transition','1917-02-05','1918-01-01','MEX','La Constitución se promulga el 5/2 y comienza a regir en general el 1/5/1917, con la excepción prevista para disposiciones electorales. El hito no termina todos los conflictos revolucionarios.',MEX_CONSTITUTION),
        ('brest-litovsk','Paz de Brest-Litovsk','transition','1918-03-03','1919-01-01','RSR DEU AUH OTT BGR','El tratado se firma el 3/3/1918. Su artículo 14 prevé ratificación: la firma no se sustituye por una entrada en vigor supuesta. La cesión de pretensiones territoriales no reconstruye los frentes o las autoridades locales.','https://avalon.law.yale.edu/20th_century/bl34.asp'),
        ('ww1-1918','Primera Guerra Mundial · campañas y armisticios de 1918','conflict','1918-01-01','1918-11-12','DEU AUH OTT BGR GBR FRA ITA USA','Ofensivas y contraofensivas culminan en armisticios separados. El cese con Alemania del 11/11 no significa paz inmediata en todos los territorios ni el fin de las guerras surgidas del colapso imperial.',ARMISTICE),
        ('russian-civil','Guerra civil y desintegración del espacio imperial ruso','conflict','1918-01-01','1920-01-01','RSR RUE FIN UKR EST LVA LTU','Autoridades soviéticas, fuerzas antibolcheviques, movimientos nacionales e intervenciones extranjeras disputan el poder. La guerra continúa después de 1919. La ventana no equipara todas las fuerzas blancas a un Estado o Gobierno único.','https://nzhistory.govt.nz/war/russian-empire-facts'),
        ('lithuania','Acta de independencia lituana','transition','1918-02-16','1920-01-01','LTU DEU','El Consejo declara la restauración de un Estado independiente mientras persiste la ocupación alemana. El acta no certifica por sí sola la aplicación inmediata de todas las fronteras reclamadas.','https://www.lrs.lt/pls/inter/w5_show?p_k=2&p_r=5691'),
        ('estonia','Proclamación de la República de Estonia','transition','1918-02-24','1920-01-01','EST DEU RSR','El manifiesto proclama la República el 24/2/1918. La proclamación, la ocupación y la guerra posterior se distinguen; el intervalo no equivale a soberanía efectiva ininterrumpida.','https://www.riigikantselei.ee/en/national-holiday'),
        ('czechoslovakia','Proclamación de Checoslovaquia','transition','1918-10-28','1920-01-01','CSK AUH','La proclamación del 28/10 precede a la elección de Masaryk y al Gobierno de noviembre. La formación del Estado no resuelve de inmediato todas sus fronteras o minorías.','https://vlada.gov.cz/cz/urad-vlady/historie/kalendarium-1918---1989-50555'),
        ('poland','Restablecimiento del Estado polaco','transition','1918-11-11','1920-01-01','POL RUE DEU AUH','Piłsudski recibe el mando militar el 11/11 y las atribuciones civiles después. La fecha conmemora un proceso de reconstrucción estatal; no fija todas las fronteras ni significa fin de las guerras regionales.','https://www.gov.pl/web/diplomacy/national-independence-day'),
        ('austrian-republic','República de Austria tras la monarquía','transition','1918-11-12','1920-01-01','AUT AUH','La Asamblea proclama la república el 12/11. La renuncia imperial a participar en asuntos de Estado del 11/11 no se presenta como una abdicación formal equivalente. El tratado de 1919 y sus límites territoriales son posteriores.',AUSTRIA),
        ('latvia','Proclamación de la República de Letonia','transition','1918-11-18','1920-01-01','LVA RSR DEU','El Consejo Popular proclama la República y aprueba el Gobierno provisional. La guerra retrasa la Asamblea Constituyente hasta 1920; este registro no presume control completo desde la proclamación.','https://www.president.lv/en/history'),
        ('south-slav','Reino de los Serbios, Croatas y Eslovenos','transition','1918-12-01','1920-01-01','YKM SRK MNK AUH','La unión crea una monarquía nueva el 1/12/1918. El reconocimiento y las fronteras se negocian después. No se confunde con la Yugoslavia socialista ni se transfieren retrospectivamente sus estadísticas.',SERBIA),
        ('german-revolution','Revolución alemana y final de la monarquía','transition','1918-11-09','1919-01-01','DEU','La proclamación republicana y la transferencia de Gobierno preceden al armisticio. El anuncio de la abdicación del 9/11 y el documento formal posterior son hechos diferentes.',NAM),
        ('weimar','Constitución de Weimar','transition','1919-08-14','1920-01-01','DEU','La Asamblea aprueba el texto el 31/7, Ebert firma el 11/8 y la promulgación y entrada en vigor son el 14/8. No se utiliza la conmemoración del 11/8 como fecha de vigencia.','https://weimar.bundesarchiv.de/WEIMAR/DE/Content/Dokumente-zur-Zeitgeschichte/1919-08-11_Verfassung.html'),
        ('versailles','Conferencia de París y firma de Versalles','transition','1919-01-18','1920-01-01','DEU GBR FRA ITA USA','La conferencia abre el 18/1 y el tratado alemán se firma el 28/6/1919. La entrada en vigor es de 1920; ni el armisticio de 1918 ni la firma de 1919 activan anticipadamente todas las cláusulas de la Sociedad de Naciones.',PEACE),
        ('influenza','Pandemia de gripe de 1918–1919','transition','1918-01-01','1920-01-01','USA GBR FRA ESP DEU IND','La pandemia se extiende por poblaciones civiles y militares durante varias oleadas. Las fechas son una ventana anual; no se inventa un origen español, una fecha mundial única de final ni cifras nacionales sin serie contrastada.','https://www.archives.gov/news/topics/flu-pandemic-1918'),
        ('ilo','Primeras instituciones de la OIT','transition','1919-04-01','1920-01-01','GBR FRA USA ITA','La comisión de paz redacta la constitución laboral en 1919 y la primera conferencia se reúne ese año. Su estructura tripartita no equivale a una alianza de Estados ni a membresía de la ONU, aún inexistente.','https://www.ilo.org/static/english/lib/century/index.htm'),
    ]
    for args in events:
        note = CALENDAR+' '+WINDOW if args[0] in ('russia-february','russia-october') else WINDOW
        event(*args,note=note)

    def record(ident,keys,section,title,start,end,text,source):
        h['records'].append(dict(id=PREFIX+ident,keys=keys.split(),section=section,title=title,start=start,end=end,text=text,source=source,sourceLabel='Archivo o institución responsable · investigación 1900–1919'))

    records = [
        ('pca','DEU AUT-HUN RUE QING ROC GBR FRA USA ITA JPN','relations','La Haya y la Corte Permanente de Arbitraje','1900-09-04','1920-01-01','La Convención de 1899, firmada el 29/7, entra en vigor el 4/9/1900. La de 1907 es otro instrumento, no una nueva admisión idéntica para todos. Las claves señalan fichas relacionadas, no certifican que todas sean partes desde 1900. El listado actual contiene continuidades y fechas distintas de informes antiguos; falta una serie histórica completa por entidad.','https://www.ministeriopublico.pt/instrumento/convencao-para-solucao-pacifica-dos-conflitos-internacionais-1899-0'),
        ('itu','AUT-HUN DEU RUE OTT GBR FRA ITA BEL DNK ESP GRC NLD PRT SWE NOR CHE','relations','Unión Telegráfica Internacional','1900-01-01','1920-01-01','La cooperación telegráfica creada en 1865 continúa durante este periodo. Los participantes fundadores incluyen imperios y Estados distintos de sus sucesores actuales. Inicio 1900 y fin 1920 son límites de revisión; las claves no afirman adhesiones ni un roster completo en cada año.',ITU),
        ('upu','GBR FRA DEU RUE AUT-HUN OTT ITA USA','relations','Unión Postal Universal y convenios postales','1900-01-01','1920-01-01','El Tratado de Berna se firma el 9/10/1874 y entra en vigor el 1/7/1875; la denominación Unión Postal Universal se adopta en 1878. Las reformas de 1906 no son una fundación nueva. Las claves vinculan la cooperación postal sin atribuir a sucesores las adhesiones imperiales ni cerrar la vigencia en 1920.',UPU),
        ('entente','GBR FRA RUE RPR','relations','Entente: entendimientos y alianzas diferentes','1907-08-31','1918-01-01','Los acuerdos franco-británicos de 1904 y anglo-rusos de 1907 completan un entendimiento diplomático, junto a compromisos franco-rusos previos. No existe un único tratado tripartito de 1907 con adhesiones homogéneas. Firma y ratificación de cada convenio deben distinguirse.','https://www.parliament.uk/about/living-heritage/transformingsociety/private-lives/yourcountry/collections/the-outbreak-of-the-first-world-war/anglo-french-relations/'),
        ('triple','DEU AUT-HUN ITA','defense','Triple Alianza y neutralidad italiana','1900-01-01','1915-05-03','El tratado impone obligaciones condicionadas y prevé también neutralidad benévola. Su existencia no obliga a pintar a Italia como beligerante con Alemania en 1914. La denuncia del 3/5/1915 precede a la guerra italiana contra Austria-Hungría.',ALLIANCE),
        ('us-associated','USA','relations','Potencia asociada en la guerra mundial','1917-04-06','1919-01-01','Estados Unidos combate junto a los Aliados como potencia asociada y conserva una posición distinta frente a sus compromisos previos. La categoría del mapa no constituye una adhesión a todos los tratados secretos.','https://www.abmc.gov/wordpress-uploads/Section14.pdf'),
        ('russia-calendars','RUE RPR RSR','institutions','Monarquía, Gobierno provisional y poder soviético','1917-03-08','1920-01-01',CALENDAR+' La abdicación de Nicolás II precede al Gobierno provisional, y el relevo bolchevique es en noviembre gregoriano. Rusia soviética no equivale todavía a la URSS fundada en 1922. Fin 1920: cobertura.',RUSSIA),
        ('china-regimes','QING ROC','institutions','Imperio Qing y República de China','1911-10-01','1920-01-01','El Gobierno republicano se proclama antes de la abdicación Qing. La concentración de poder de Yuan y su ensayo monárquico no justifican proyectar la presidencia de la República Popular al periodo. El control provincial exige datos propios.',CHINA),
        ('mexico-law','MEX','institutions','Promulgación y vigencia de la Constitución mexicana','1917-02-05','1920-01-01','El artículo primero transitorio distingue publicación y protesta del texto de su vigencia general desde 1/5/1917. Las disposiciones electorales son una excepción expresamente inmediata. No se infiere estabilidad territorial o fin de todas las facciones.',MEX_CONSTITUTION),
        ('austrian-republic','AUT-HUN AUT','institutions','Disolución imperial y república austríaca','1918-11-11','1920-01-01','Carlos renuncia a participar en los asuntos de Estado, sin abdicar formalmente. La república se proclama el 12/11. La Austria sucesora no se confunde con la totalidad de Austria-Hungría ni con un Gobierno imperial conservado después de 1918.',AUSTRIA),
        ('germany-law','DEU','institutions','Revolución, Constituyente y Constitución','1918-11-09','1920-01-01','La proclamación de 1918 precede al proceso constituyente. La Constitución de 1919 se firma el 11/8 y entra en vigor al promulgarse el 14/8. Los cargos de presidente del Reich y canciller deben mantenerse separados.','https://weimar.bundesarchiv.de/WEIMAR/DE/Content/Dokumente-zur-Zeitgeschichte/1919-08-11_Verfassung.html'),
        ('colonial-cuts','NAM COD LBY PHL HTI DOM','territory','Conquista, ocupación y administración colonial','1900-01-01','1920-01-01','Las independencias posteriores no se retrotraen a 1900. Declarar una anexión, administrar una colonia, ocupar militarmente y ejercer control local son hechos distintos. Los cortes 1900/1920 delimitan esta revisión, no una cronología jurídica uniforme.','https://www.archives.gov/files/research/foreign-policy/related-records/rg-256-inventory.pdf'),
        ('postwar-treaties','DEU AUT HUN OTT YKM CSK POL','territory','Armisticios y tratados después de 1918','1918-11-11','1920-01-01','Los armisticios no fijan definitivamente todas las fronteras. Versalles, Saint-Germain y Neuilly se firman en 1919; sus fechas de entrada en vigor y los tratados húngaro y otomano son posteriores. No se aplica en 1918 una configuración de fronteras de 1920.',PEACE),
        ('british-vote','GBR','society','Reforma del sufragio de 1918','1918-02-06','1920-01-01','La ley recibe asentimiento el 6/2/1918 y amplía el sufragio masculino y el femenino bajo condiciones de edad y propiedad. No establece todavía igualdad completa del sufragio entre hombres y mujeres.','https://www.parliament.uk/about/living-heritage/transformingsociety/electionsvoting/womenvote/parliamentary-collections/speakers-conference/representation-of-the-people-act/'),
        ('pandemic','USA GBR FRA ESP DEU IND','society','Gripe de 1918: documentos y alcance','1918-01-01','1920-01-01','Las fuentes documentan medidas sanitarias y varias oleadas de pandemia. La denominación gripe española no demuestra origen español; no se añaden indicadores o cifras nacionales sin procedencia específica. Ventana editorial hasta 1919.','https://www.archives.gov/news/topics/flu-pandemic-1918'),
        ('ilo','GBR FRA ITA USA','institutions','OIT: constitución y primeras sesiones','1919-04-01','1920-01-01','La organización se establece en el marco de los acuerdos de paz de 1919 y celebra su primera Conferencia Internacional del Trabajo en Washington. El intervalo comienza por cobertura mensual; no atribuye a todas las fichas igual día de adhesión ni vigencia anticipada de Versalles.','https://www.ilo.org/static/english/lib/century/sources/sources1919.htm'),
    ]
    for args in records:
        record(*args)

    def relation(ident,a,b,date,label,source,note):
        h['relations'].append(dict(id=PREFIX+ident,**{'from':dict(key=a[0],name=a[1],year=a[2]),'to':dict(key=b[0],name=b[1],year=b[2])},date=date,type='transition',label=label,note=note,source=source,sourceLabel='Fuente institucional o documento de la transición'))

    relation('qing-republic',('QING','Imperio Qing',1911),('ROC','República de China',1912),'1912-01-01','Proclamación republicana',CHINA,'La proclamación republicana precede a la abdicación de 12/2/1912; no se transfiere retrospectivamente a la República Popular toda la historia de China.')
    relation('russia-provisional',('RUE','Imperio ruso',1916),('RPR','Gobierno provisional ruso',1917),'1917-03-15','Abdicación y Gobierno provisional',RUSSIA,CALENDAR+' El relevo de autoridad no significa independencia de todos los territorios imperiales ni retirada de la guerra.')
    relation('russia-soviet',('RPR','Gobierno provisional ruso',1917),('RSR','Rusia soviética',1918),'1917-11-07','Toma de poder bolchevique',RUSSIA,CALENDAR+' No es la creación de la URSS; el año del enlace permite navegar a una representación posterior al relevo.')
    relation('austria-hungary-austria',('AUT-HUN','Austria-Hungría',1917),('AUT','República de Austria',1919),'1918-11-12','Proclamación de la república austríaca',AUSTRIA,'El Estado austríaco sucesor no equivale al imperio multinacional completo ni hereda automáticamente sus estadísticas o cargos.')
    relation('austria-hungary-csk',('AUT-HUN','Austria-Hungría',1917),('CSK','Checoslovaquia',1919),'1918-10-28','Proclamación de Checoslovaquia','https://vlada.gov.cz/cz/urad-vlady/historie/kalendarium-1918---1989-50555','La proclamación, el reconocimiento y la fijación posterior de fronteras son hechos distintos.')
    relation('serbia-yugoslavia',('SRK','Reino de Serbia',1917),('YKM','Reino de los Serbios, Croatas y Eslovenos',1919),'1918-12-01','Unión sudeslava',SERBIA,'Enlace entre entidades separadas. Las funciones dinásticas continúan, sin convertir la unión en una anexión de todos los territorios por un Estado moderno.')
    relation('panama',('COL','Colombia',1902),('PAN','Panamá',1904),'1903-11-03','Separación de Panamá',STATE+'countries/panama','El reconocimiento estadounidense del 6/11 y el régimen de la Zona del Canal son hechos posteriores y distintos.')
    relation('australia',('GBR','Imperio británico',1900),('AUS','Commonwealth of Australia',1901),'1901-01-01','Federación australiana','https://peo.gov.au/understand-our-parliament/history-of-parliament/federation/federation','Enlace al marco imperial anterior, sin afirmar que todas las colonias fueran un mismo territorio metropolitano o que la federación otorgara soberanía exterior plena.')
    relation('finland',('RUE','Imperio ruso',1916),('FIN','Finlandia',1918),'1917-12-06','Declaración de independencia de Finlandia','https://valtioneuvosto.fi/en/-/finland-s-centenary-is-filled-with-joy-and-dignity','La declaración parlamentaria y el reconocimiento soviético del 31/12 son distintos. El enlace no acredita la posterior cartografía de la guerra civil.')

    d['organizations'].sort(key=lambda o:o['id'])
    for o in d['organizations']:
        if o['id'] in new_org_ids:
            o['memberships'].sort(key=lambda m:(m['code'],m['start'],m['category']))
    d['coverageStart'] = 1900
    d['expandedReferenceDate'] = '2026-10-24'
    c['startYear'] = 1900
    c['coverageNote'] = 'Focal, sourced phases from 1900 onward; partial worldwide. Codes link cards, not a belligerent register. Review windows are explicit and do not supply front geometry.'
    h['coverageStart'] = 1900
    return d,c,h


def validate(original,result):
    d,c,h = result
    assert prepare(*result)==result,'Non-idempotent preparation'
    for before,after,field in [(original[1],c,'events'),(original[2],h,'records'),(original[2],h,'relations')]:
        rows={r['id']:r for r in after[field]}
        assert len(rows)==len(after[field]),('Duplicate ID',field)
        for row in before[field]:
            if not row['id'].startswith(PREFIX):
                assert rows.get(row['id'])==row,('Changed prior row',row['id'])
        for row in after[field]:
            date=row.get('start',row.get('date'))
            datetime.date.fromisoformat(date)
            if row.get('end'):
                datetime.date.fromisoformat(row['end'])
                assert row['end']>date,row['id']
    old={o['id']:o for o in original[0]['organizations']}
    new={o['id']:o for o in d['organizations']}
    for oid,row in old.items():
        if oid not in ('tripleAlliance','centralPowersWW1','alliesWW1'):
            assert new[oid]==row,('Changed prior organization',oid)
    for o in d['organizations']:
        for i,m in enumerate(o['memberships']):
            datetime.date.fromisoformat(m['start'])
            if m.get('end'):
                assert m['end']>m['start'],(o['id'],m)
            assert not any(n['code']==m['code'] and max(n['start'],m['start'])<min(n.get('end','9999'),m.get('end','9999')) for n in o['memberships'][i+1:]),('Membership overlap',o['id'],m)
    for before,after in zip(original,result):
        assert before['referenceDate']==after['referenceDate'],'Contemporary reference changed'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Prepare twice and validate in memory without writing public files.')
    args=parser.parse_args()
    names=['affiliations.json','historical-context.json','country-history.json']
    original=[json.loads((ROOT/name).read_text(encoding='utf8')) for name in names]
    result=prepare(*original)
    validate(original,result)
    if not args.check:
        for name,value in zip(names,result):
            (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    d,c,h=result
    print('CHECK ONLY; no public files written.' if args.check else 'Prepared files.')
    print('Totals:',len(d['organizations']),'organizations;',sum(len(o['memberships']) for o in d['organizations']),'membership intervals;',len(c['events']),'phases;',len(h['records']),'records;',len(h['relations']),'links.')
    print('1900 extension:',sum(e['id'].startswith(PREFIX) for e in c['events']),'phases;',sum(r['id'].startswith(PREFIX) for r in h['records']),'records;',sum(r['id'].startswith(PREFIX) for r in h['relations']),'links.')


if __name__=='__main__':
    main()
