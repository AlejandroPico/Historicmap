"""Pure, incremental context/institution/relationship additions for1880–1899.

prepare(affiliations, context, history) never writes or accesses the network.
The CLI checks in memory by default; output requires an explicit destination.
Existing1900+ records, organizations and contemporary reference dates survive.
"""
import argparse
import copy
import datetime
import json
import pathlib

PREFIX = 'extension-1880-'
FIRST, STOP = '1880-01-01', '1900-01-01'
ROOT = pathlib.Path(__file__).resolve().parents[1] / 'public/data'
WINDOW = ('Intervalo documental con inicio inclusivo y fin exclusivo. Los cortes de cobertura no son'
          ' declaraciones, tratados de paz ni cambios de frontera. Las claves enlazan fichas;'
          ' no proporcionan geometrías, frentes ni una lista completa de beligerantes.')
LABEL = 'Fuente institucional o documento primario · investigación1880–1899'
TRIPLE = 'https://worldjpn.net/documents/texts/docs/18820520.T1E.html'
TRIPLE_RATIFICATIONS = 'https://mek.oszk.hu/07100/07162/pdf/secret01pribuoft.pdf'
DUAL = 'https://avalon.law.yale.edu/19th_century/dualalli.asp'
FR_RU = 'https://avalon.law.yale.edu/19th_century/frrumil.asp'
FR_RU_RATIFICATION = 'https://catalogue.bnf.fr/ark:/12148/cb11979428z'
BERLIN = 'https://archiv.diplo.de/arc-en/the-political-archive/general-act-2684414'
PACIFIC = 'https://www.memoriachilena.gob.cl/602/w3-article-693.html'
CHILE = 'https://www.memoriachilena.gob.cl/602/w3-article-706.html'
BOER_ONE = 'https://www.nam.ac.uk/explore/transvaal-war'
BOER_TWO = 'https://www.nam.ac.uk/explore/boer-war'
SUDAN = 'https://www.nam.ac.uk/explore/egypt-and-sudan'
SINO_JAPAN = 'https://jacar.go.jp/english/exhibition/jacarbl-fsjwar-e/about/p002.html'
SHIMONOSEKI = 'https://www.jacar.go.jp/english/exhibition/jacarbl-fsjwar-e/glossary/g004.html'
FR_CHINA = 'https://library.law.fsu.edu/Digital-Collections/LimitsinSeas/pdf/ibs038.pdf'
SPAIN_US = 'https://history.state.gov/milestones/1866-1898/spanish-american-war'
SPAIN_DATES = 'https://guides.loc.gov/chronicling-america-spanish-american-war'
PHILIPPINES = 'https://history.state.gov/milestones/1899-1913/war'
ADWA = 'https://archivio.quirinale.it/aspr/gianni-bisiach/AV-002-000186/1-marzo-1896-battaglia-adua'
MADAGASCAR = 'https://mjp.univ-perp.fr/constit/mg1896.htm'
MADAGASCAR_CAMPAIGN = 'https://www.servicehistorique.sga.defense.gouv.fr/sites/default/files/notices_files/SHDGR_INV_8H.pdf'
CHINA_REFORM = 'https://www.da.gd.gov.cn/portal_home/wap/archivesDetail/4040'
CHINA_COUP = 'https://www.jacar.go.jp/english/exhibition/nichiro/18980921.htm'
BRAZIL = 'https://www2.camara.leg.br/legin/fed/decret/1824-1899/decreto-1-15-novembro-1889-532625-norma-pe.html'
KOREA = 'https://www.korea.net/Events/Exhibitions/view?articleId=7830'
HAWAII_1893 = 'https://ags.hawaii.gov/archives/online-exhibitions/1894-constitutional-convention/'
HAWAII_1894 = 'https://libweb.hawaii.edu/digicoll/annexation/blount/br1374.php'
HAWAII_1898 = 'https://history.state.gov/countries/hawaii'
HAWAII_ARCHIVE = 'https://digitalarchives.hawaii.gov/item/ark:70111/1zSZ'


def _bounded(start, end):
    if not (FIRST <= start < end <= STOP):
        raise ValueError(f'New interval outside1880–1899: {start}..{end}')


def _remove_own(rows):
    kept = []
    for row in rows:
        if not row.get('id', '').startswith(PREFIX):
            kept.append(row)
            continue
        start = row.get('start', row.get('date'))
        end = row.get('end')
        if not (start and FIRST <= start < STOP and (not end or end <= STOP)):
            raise ValueError(f'Refusing to replace an out-of-window owned ID: {row["id"]}')
    return kept


def prepare(affiliations, context, history):
    d, c, h = copy.deepcopy((affiliations, context, history))
    c['events'] = _remove_own(c['events'])
    h['records'] = _remove_own(h['records'])
    h['relations'] = _remove_own(h['relations'])

    # Extend the established organization, without regenerating its metadata or
    # memberships in1900+. The earlier preparer would destroy this extension.
    triple = next((o for o in d['organizations'] if o['id'] == 'tripleAlliance'), None)
    if triple is None:
        raise ValueError('Input must contain the established tripleAlliance organization; it is not regenerated here.')
    for organization in d['organizations']:
        kept = []
        for member in organization['memberships']:
            if member.get('acquisition') == PREFIX + 'memberships':
                _bounded(member['start'], member['end'])
            else:
                kept.append(member)
        organization['memberships'] = kept
    for code in ('AUH', 'DEU', 'ITA'):
        gaps = [('1882-05-30', STOP)]
        for old in triple['memberships']:
            if old['code'] != code:
                continue
            left, right = old['start'], old.get('end', '9999-12-31')
            remaining = []
            for a, b in gaps:
                if b <= left or a >= right:
                    remaining.append((a, b))
                else:
                    if a < left:
                        remaining.append((a, left))
                    if b > right:
                        remaining.append((right, b))
            gaps = remaining
        for start, end in gaps:
            _bounded(start, end)
            row = dict(code=code, start=start, end=end, category='member', source=TRIPLE_RATIFICATIONS,
                       acquisition=PREFIX + 'memberships', endIsCoverageBoundary=True,
                       note=('Tratado firmado20/5/1882; el canje de ratificaciones en Viena30/5/1882'
                             ' figura en la edición documental de Pribram, con referencia al original'
                             ' archivístico. La fecha inicial sigue ese canje, conforme al artículoVII.'
                             ' Cierre1/1/1900: cobertura de esta ampliación,'
                             ' no retirada ni disolución. Se conserva literalmente la observación posterior.'))
            if start != '1882-05-30':
                row['startIsCoverageBoundary'] = True
            triple['memberships'].append(row)

    def event(ident, title, kind, start, end, keys, text, source):
        _bounded(start, end)
        c['events'].append(dict(id=PREFIX + ident, title=title, type=kind,
                               start=start, end=end, countries=keys.split(), text=text,
                               source=source, sourceLabel=LABEL, note=WINDOW))

    events = [
        ('pacific', 'Guerra del Pacífico · campañas y acuerdos de1880–1884', 'conflict', FIRST, '1885-01-01',
         'CHL PER BOL', 'Continúa la guerra iniciada en1879: campañas contra Perú y Bolivia, ocupación de Lima y resistencia posterior. El Tratado de Ancón de1883 y la tregua chileno-boliviana de1884 son acuerdos distintos. Los extremos de este registro son cobertura anual y no un único final jurídico para los tres Estados.', PACIFIC),
        ('boer-one', 'Primera guerra bóer · rebelión del Transvaal', 'conflict', '1880-12-13', '1881-03-24',
         'GBR TRV ZAF', 'La restauración republicana proclamada13/12/1880 abre el conflicto contra la anexión británica. El National Army Museum distingue armisticio6/3/1881 y paz23/3. La clave territorial sudafricana enlaza el área actual; no atribuye a la Unión Sudafricana, aún inexistente, participación en la guerra.', BOER_ONE),
        ('egypt', 'Egipto · intervención y ocupación británica', 'conflict', '1882-07-01', '1883-01-01',
         'EGY GBR OTT', 'El bombardeo de Alejandría y la campaña contra las fuerzas de Urabi desembocan en una ocupación británica. El jedivato mantiene un vínculo nominal otomano; ocupación militar y anexión no son equivalentes. Intervalo mensual/anual: no fecha jurídica exacta del inicio o fin de la ocupación.', SUDAN),
        ('mahdist-rise', 'Sudán · levantamiento mahdista y caída de Jartum', 'conflict', '1881-01-01', '1886-01-01',
         'SDN EGY GBR', 'El levantamiento iniciado en1881 derrota fuerzas egipcias y toma Jartum en1885. Se distinguen autoridad egipcia, intervención británica y Estado mahdista; la claveSudán no convierte a su república contemporánea en beligerante. Ventana anual, sin un frente de control inferido.', SUDAN),
        ('mahdist-return', 'Sudán · reconquista anglo-egipcia y resistencia mahdista', 'conflict', '1896-01-01', STOP,
         'SDN EGY GBR', 'La expedición anglo-egipcia culmina en Omdurmán en1898; la resistencia y nuevas operaciones continúan en1899. El final de la ventana no afirma extinción instantánea de toda resistencia ni resuelve por sí solo la administración del condominio.', SUDAN),
        ('franco-chinese', 'Guerra franco-china y acuerdos sobre Tonkín', 'conflict', '1884-01-01', '1886-01-01',
         'FRA QNG VNM', 'La guerra y las operaciones en Tonkín se cierran mediante acuerdos y retiradas, no por un cambio simultáneo de todas las fronteras. El tratado franco-chino de Tianjin se firma9/6/1885 y se canjean ratificaciones28/11. La convención fronteriza posterior es de1887. Los extremos son cobertura anual.', FR_CHINA),
        ('berlin', 'Conferencia de Berlín y Acta General', 'transition', '1884-11-15', '1885-02-27',
         'DEU AUT-HUN AUH BEL DNK ESP FRA GBR ITA NLD OTT PRT RUE SWE NOR COD', 'La conferencia se celebra15/11/1884–26/2/1885 y establece reglas coloniales de navegación, comercio y reclamación. No dibuja todas las fronteras de África ni equivale a consentimiento africano. La claveCongo señala una región afectada y no una participación del Estado congoleño actual.', BERLIN),
        ('chile-civil', 'Chile · guerra civil de1891', 'conflict', '1891-01-07', '1891-08-30',
         'CHL', 'La ruptura entre Balmaceda y el Congreso provoca una guerra civil con autoridades y fuerzas enfrentadas. Tras Concón y Placilla, Balmaceda entrega el mando a Baquedano29/8/1891. No se deduce de estas fases la geometría de las zonas de cada bando.', CHILE),
        ('sino-japanese', 'Primera guerra sino-japonesa', 'conflict', '1894-07-25', '1895-05-09',
         'QNG JPN JOS KEM', 'Los combates comienzan antes de las declaraciones formales1/8/1894: el archivo japonés documenta la decisión de reconocer25/7 como inicio. Shimonoseki se firma17/4/1895 y se ratifica8/5; la retrocesión de Liaodong es posterior. Joseon existe entonces; KEM sólo enlaza la posterior ficha sucesora.', SINO_JAPAN),
        ('madagascar-campaign', 'Madagascar · conquista francesa y resistencias', 'conflict', '1894-01-01', '1897-01-01',
         'MDG FRA', 'La expedición francesa de1894–1896 impone un protectorado y precede a la declaración colonial. El inventario militar documenta operaciones y ocupación; no se interpreta la legislación colonial como control local uniforme o desaparición inmediata de la resistencia. Cobertura anual de la campaña.', MADAGASCAR_CAMPAIGN),
        ('madagascar-colony', 'Madagascar · declaración colonial francesa', 'transition', '1896-08-06', '1897-01-01',
         'MDG FRA', 'La ley6/8/1896 declara colonia a Madagascar y sus dependencias. El tratado de1885, su aprobación de1886 y la imposición de1895 son antecedentes jurídicamente diferentes. El corte de fin de año no termina el dominio colonial.', MADAGASCAR),
        ('adwa', 'Adwa · victoria etíope frente a la invasión italiana', 'conflict', '1896-03-01', '1896-03-02',
         'ETH ITA ERI', 'La batalla1/3/1896 derrota al ejército invasor italiano. El posterior acuerdo de Addis Abeba reconoce la soberanía etíope. Este registro representa el acontecimiento documentado, no una reconstrucción de todos los frentes de la guerra ni una anexión italiana de Etiopía.', ADWA),
        ('cuba', 'Cuba · guerra de independencia y crisis colonial', 'conflict', '1895-01-01', '1899-01-01',
         'CUB ESP USA', 'La lucha independentista cubana precede tres años a la intervención estadounidense de1898. No se presenta a Estados Unidos como beligerante desde1895 ni se equipara la retirada española con el inmediato funcionamiento del Gobierno republicano cubano. Inicio y fin: cobertura anual.', SPAIN_US),
        ('spain-us', 'Guerra hispano-estadounidense y protocolo de paz', 'conflict', '1898-04-25', '1898-08-13',
         'ESP USA CUB PRI GUM PHL', 'Se sigue la declaración del Congreso estadounidense25/4 para este intervalo; el bloqueo y la ruptura diplomática son anteriores. El protocolo12/8 suspende hostilidades. La firma de París10/12/1898 y su ratificación posterior no se anticipan al armisticio.', SPAIN_DATES),
        ('paris-1898', 'Tratado de París · firma y ratificaciones distintas', 'transition', '1898-12-10', '1899-01-01',
         'ESP USA CUB PRI GUM PHL', 'La firma dispone la renuncia española sobre Cuba y cesiones a Estados Unidos. No hace de Cuba un Estado anexionado ni convierte10/12 en el día de todas las transferencias de administración. El tratado necesita ratificaciones, posteriores a esta firma.', SPAIN_US),
        ('philippines', 'Guerra filipino-estadounidense · fase de1899', 'conflict', '1899-02-04', STOP,
         'PHL USA', 'Los combates4/2/1899 entre fuerzas estadounidenses e independentistas filipinos anteceden a la ratificación del Senado de Estados Unidos6/2. La lucha pasa a una fase guerrillera en noviembre y continúa después de1899. El cierre1900 es cobertura, no un final de guerra.', PHILIPPINES),
        ('boer-two', 'Segunda guerra bóer · apertura de1899', 'conflict', '1899-10-11', STOP,
         'GBR TRV ORF ZAF', 'El ultimátum de las repúblicas bóeres expira11/10 y sus tropas cruzan las fronteras coloniales12/10. Los sitios y derrotas británicas de diciembre abren una guerra que continúa en1900–1902. No se atribuye la condición de beligerante a una Unión Sudafricana todavía inexistente.', BOER_TWO),
        ('china-reform', 'Imperio Qing · Reforma de los Cien Días', 'transition', '1898-06-11', '1898-09-22',
         'QNG', 'El edicto11/6/1898 impulsa reformas de administración, educación y economía bajo Guangxu. El golpe de Cixi21/9 frena el programa y altera el ejercicio del poder sin crear una nueva dinastía ni la República Popular. El inicio está documentado por el Archivo de Guangdong; el golpe por JACAR.', CHINA_REFORM),
        ('brazil-republic', 'Brasil · proclamación republicana', 'transition', '1889-11-15', '1890-01-01',
         'BRA BRA-EMPIRE', 'El decreto1 de15/11/1889 proclama provisionalmente la república federativa. El cambio de régimen no es una nueva fundación del territorio brasileño ni la Constitución definitiva, que llegará después. Se distinguen el Gobierno provisional y la presidencia constitucional.', BRAZIL),
        ('korean-empire', 'Joseon · proclamación del Imperio de Corea', 'transition', '1897-10-12', '1898-01-01',
         'JOS KEM', 'Gojong declara el Imperio de Corea12/10/1897 y asume título imperial. Es una transición institucional de Joseon; no una anexión japonesa ni la fundación retrospectiva de las repúblicas coreanas contemporáneas.', KOREA),
        ('hawaii-overthrow', 'Hawái · derrocamiento de la monarquía', 'transition', '1893-01-17', '1894-07-04',
         'HAW-KINGDOM HAW-PROVISIONAL USA', 'La proclamación17/1/1893 abroga la monarquía e instaura un Gobierno provisional. El intento inicial de anexión a Estados Unidos no culmina entonces. La legitimidad del derrocamiento y la oposición hawaiana deben distinguirse de los hechos administrativos posteriores.', HAWAII_1893),
        ('hawaii-republic', 'Hawái · proclamación de la República', 'transition', '1894-07-04', '1895-01-01',
         'HAW-PROVISIONAL HAW-REPUBLIC', 'La nota diplomática4/7/1894 comunica la proclamación republicana y la sucesión al Gobierno provisional, bajo Sanford Dole. El fin de la ventana anual no termina la República, cuya continuidad se documenta en la ficha institucional.', HAWAII_1894),
        ('hawaii-annexation', 'Hawái · anexión y administración estadounidense', 'transition', '1898-08-12', STOP,
         'HAW-REPUBLIC HAW USA', 'La transferencia formal se realiza12/8/1898 tras la resolución estadounidense de julio. Se distingue la anexión de la posterior organización del territorio por ley. No se llama a este régimen Estado federado ni se retrotrae a1893 la anexión de1898.', HAWAII_1898),
    ]
    for args in events:
        event(*args)

    def record(ident, keys, section, title, start, end, text, source):
        _bounded(start, end)
        h['records'].append(dict(id=PREFIX + ident, keys=keys.split(), section=section,
                                 title=title, start=start, end=end, text=text,
                                 source=source, sourceLabel=LABEL))

    records = [
        ('triple', 'DEU AUT-HUN ITA', 'defense', 'Triple Alianza · signatarios y obligaciones condicionadas',
         '1882-05-20', STOP, 'Alemania, Austria-Hungría e Italia firman el tratado defensivo20/5/1882. Los artículos diferencian asistencia y neutralidad según el ataque y fijan la vigencia desde el canje de ratificaciones. La capa usa30/5/1882, fecha del canje documentada por Pribram; esta ficha incluye la firma anterior. Las renovaciones no convierten a estos Estados en beligerantes permanentes.', TRIPLE),
        ('dual', 'DEU AUT-HUN', 'defense', 'Doble Alianza austro-alemana',
         FIRST, STOP, 'El tratado7/10/1879 obliga a asistencia en caso de ataque ruso y contempla neutralidad benévola frente a otras potencias bajo determinadas condiciones. Inicio1880 y cierre1900 delimitan esta revisión, no firma o extinción. No se transforma la alianza en anexión ni se asigna a Rusia una membresía inexistente.', DUAL),
        ('franco-russian', 'FRA RUE', 'defense', 'Acercamiento franco-ruso, convención y ratificación',
         '1894-02-01', STOP, 'La convención militar se negocia en1892 y ambas partes completan su aprobación entre diciembre1893 y enero1894, según el catálogo de la BnF. El inicio1/2/1894 es cobertura posterior a ese intervalo; no una fecha de firma inventada. Las cláusulas de asistencia están en el documento militar. No se incluye al Reino Unido ni se crea anticipadamente una Triple Entente.', FR_RU_RATIFICATION),
        ('berlin', 'DEU AUT-HUN BEL FRA GBR PRT ESP COD', 'territory', 'Berlín y el marco de expansión colonial',
         '1884-11-15', STOP, 'La conferencia de1884–1885 establece un marco de comercio, navegación y reclamaciones coloniales. Su Acta General no aporta una delimitación completa de África; los acuerdos bilaterales, conquistas y resistencias requieren cronologías y cartografía propias. Las entidades africanas actuales son enlaces geográficos de contexto, no partes consentidoras de ese reparto.', BERLIN),
        ('pacific', 'CHL PER BOL', 'territory', 'Guerra del Pacífico y acuerdos territoriales diferentes',
         FIRST, '1885-01-01', 'Las campañas iniciadas en1879 incluyen la ocupación de Lima y resistencia peruana. Ancón1883 y la tregua con Bolivia1884 no resuelven a la vez todos los desacuerdos fronterizos. No se aplican los tratados bilaterales posteriores como si ya estuvieran vigentes en1880.', PACIFIC),
        ('chile', 'CHL', 'institutions', 'Ruptura entre Ejecutivo y Congreso en1891',
         '1891-01-07', '1892-01-01', 'El enfrentamiento por presupuesto y facultades públicas deriva en dos autoridades rivales y guerra civil. Tras la derrota militar, Balmaceda entrega el mando29/8/1891. La sucesión constitucional y la distribución territorial de cada facción se investigan de forma independiente.', CHILE),
        ('egypt', 'EGY GBR OTT', 'institutions', 'Jedivato, ocupación y soberanía nominal',
         '1882-07-01', STOP, 'La presencia militar británica posterior a la campaña de1882 coexiste con el jedivato y el vínculo nominal otomano. Esas funciones no se reducen a un único presidente nacional ni prueban una anexión británica formal en1882.', SUDAN),
        ('sudan', 'SDN EGY GBR', 'institutions', 'Autoridad mahdista e intervención anglo-egipcia',
         '1881-01-01', STOP, 'El levantamiento mahdista altera el dominio egipcio y crea una autoridad propia. La reconquista anglo-egipcia de finales de siglo y sus operaciones de1899 no autorizan a representar un Estado sudanés contemporáneo ni control extranjero homogéneo durante todo el intervalo. Cobertura anual, no duración jurídica de un solo régimen.', SUDAN),
        ('madagascar', 'MDG FRA', 'institutions', 'Monarquía merina, protectorado y colonia',
         '1885-12-17', STOP, 'El tratado de1885 y la ley francesa de aprobación6/3/1886 preceden a la declaración colonial6/8/1896. La monarquía merina y las administraciones impuestas no desaparecen por una supuesta fecha colonial única. La normativa se distingue de la imposición militar y de la resistencia local.', MADAGASCAR),
        ('ethiopia', 'ETH ITA', 'defense', 'Adwa y soberanía etíope',
         '1896-03-01', STOP, 'La derrota italiana en Adwa1/3/1896 y el posterior acuerdo de Addis Abeba desmienten la aplicación unilateral de un protectorado italiano sobre toda Etiopía. No se trasladan a esta época las conquistas italianas posteriores. Cierre1900: cobertura.', ADWA),
        ('shimonoseki', 'QING JPN JOS KEM', 'territory', 'Shimonoseki y la Triple Intervención',
         '1895-04-17', STOP, 'Shimonoseki se firma17/4/1895 y se ratifica8/5. Alemania, Rusia y Francia presionan por la retrocesión de Liaodong, ejecutada mediante otro acuerdo en noviembre. La guerra, la cesión y la devolución no constituyen un solo cambio territorial ni la anexión de toda Corea.', SHIMONOSEKI),
        ('china-reform', 'QING', 'institutions', 'Reformas imperiales y poder efectivo de Cixi',
         '1898-06-11', STOP, 'El edicto de junio abre el programa reformista de Guangxu; el golpe21/9/1898 impone el confinamiento del emperador y restablece el control efectivo de Cixi. No se extingue por ello la dinastía Qing. La fecha del golpe procede de informes diplomáticos conservados por JACAR.', CHINA_COUP),
        ('brazil-monarchy', 'BRA-EMPIRE', 'institutions', 'Monarquía constitucional antes de la ruptura republicana',
         FIRST, '1889-11-15', 'El decreto republicano15/11/1889 pone término al régimen imperial y anuncia un Gobierno provisional. Esta ventana identifica la entidad precedente sin convertir1880 en su fecha de fundación ni proyectar cargos republicanos sobre PedroII.', BRAZIL),
        ('brazil-republic', 'BRA', 'institutions', 'Gobierno provisional y república federativa',
         '1889-11-15', STOP, 'El decreto1 proclama provisionalmente la república federativa y regula la transición de las provincias a Estados. No es la Constitución definitiva ni prueba continuidad personal del emperador en la jefatura republicana. Los gobiernos y constituciones posteriores necesitan fechas propias.', BRAZIL),
        ('joseon', 'JOS', 'institutions', 'Reino de Joseon y cambio de título de Gojong',
         FIRST, '1897-10-12', 'El reino precede a la proclamación imperial12/10/1897. El cambio de título y denominación del Estado se distingue de la posterior imposición de un protectorado japonés. No se asignan al período los gobiernos de Corea del Norte o del Sur.', KOREA),
        ('korean-empire', 'KEM', 'institutions', 'Imperio de Corea',
         '1897-10-12', STOP, 'Gojong declara el Imperio de Corea y asume el rango imperial12/10/1897, según el Museo Nacional del Palacio. Joseon y el Imperio mantienen una sucesión institucional; no son territorios modernos distintos con fronteras inventadas para esa fecha.', KOREA),
        ('hawaii-monarchy', 'HAW-KINGDOM', 'institutions', 'Monarquía hawaiana y derrocamiento de1893',
         FIRST, '1893-01-17', 'La monarquía es derrocada17/1/1893 y sustituida por un Gobierno provisional. La nueva autoridad busca una anexión que no se consuma ese año; sus proclamaciones no demuestran consentimiento de toda la población hawaiana.', HAWAII_1893),
        ('hawaii-provisional', 'HAW-PROVISIONAL', 'institutions', 'Gobierno provisional de Hawái',
         '1893-01-17', '1894-07-04', 'El régimen provisional pretende mantenerse hasta una anexión estadounidense; al no completarse el tratado inicial, convoca una convención constitucional. Es una autoridad distinta del Reino derrocado y de la República proclamada4/7/1894.', HAWAII_1893),
        ('hawaii-republic', 'HAW-REPUBLIC', 'institutions', 'República de Hawái y proyecto de anexión',
         '1894-07-04', '1898-08-12', 'La comunicación diplomática4/7/1894 declara que la República sucede al Gobierno provisional, con Sanford Dole como presidente. Se diferencia de la administración estadounidense que sigue a la transferencia formal12/8/1898.', HAWAII_1894),
        ('hawaii-annexed', 'HAW USA', 'institutions', 'Hawái tras la transferencia de1898',
         '1898-08-12', STOP, 'Tras la resolución estadounidense de julio, la transferencia formal ocurre12/8/1898. La organización territorial posterior por una ley orgánica es un acto distinto. La fichaHAW conserva la identidad del archipiélago bajo esta administración sin fingir un Estado independiente nuevo ni un Estado federado en1898.', HAWAII_1898),
    ]
    for args in records:
        record(*args)

    def relation(ident, a, b, date, label, source, note):
        if not FIRST <= date < STOP:
            raise ValueError('New transition date outside1880–1899')
        h['relations'].append(dict(id=PREFIX + 'relation-' + ident,
                                  **{'from': dict(key=a[0], name=a[1], year=a[2]),
                                     'to': dict(key=b[0], name=b[1], year=b[2])},
                                  date=date, type='transition', label=label, source=source,
                                  note=note, sourceLabel=LABEL))

    relation('brazil', ('BRA-EMPIRE', 'Imperio del Brasil', 1888), ('BRA', 'República del Brasil', 1890),
             '1889-11-15', 'Proclamación republicana', BRAZIL,
             'Enlace entre regímenes del mismo país; decreto provisional15/11, distinto de la Constitución posterior. Los años ancla permiten navegar a ambos lados del cambio.')
    relation('korea', ('JOS', 'Reino de Joseon', 1896), ('KEM', 'Imperio de Corea', 1898),
             '1897-10-12', 'Proclamación del Imperio de Corea', KOREA,
             'Cambio institucional y de título de Gojong; no anexión japonesa ni división en dos repúblicas modernas.')
    relation('hawaii-provisional', ('HAW-KINGDOM', 'Reino de Hawái', 1892), ('HAW-PROVISIONAL', 'Gobierno provisional de Hawái', 1893),
             '1893-01-17', 'Derrocamiento de la monarquía', HAWAII_1893,
             'Se registra la sustitución administrativa y su carácter controvertido; el proyecto de anexión no equivale a anexión efectiva en1893.')
    relation('hawaii-republic', ('HAW-PROVISIONAL', 'Gobierno provisional de Hawái', 1893), ('HAW-REPUBLIC', 'República de Hawái', 1895),
             '1894-07-04', 'Proclamación republicana', HAWAII_1894,
             'La nota diplomática distingue la nueva República del Gobierno provisional y la fecha de su proclamación.')
    relation('hawaii-annexation', ('HAW-REPUBLIC', 'República de Hawái', 1897), ('HAW', 'Hawái bajo administración estadounidense', 1899),
             '1898-08-12', 'Transferencia formal tras la resolución de anexión', HAWAII_ARCHIVE,
             'La ceremonia12/8 es distinta de la resolución de julio y de la ley orgánica territorial posterior; no demuestra consentimiento general hawaiano.')
    relation('hawaii-us', ('HAW', 'Hawái bajo administración estadounidense', 1899), ('USA', 'Estados Unidos', 1899),
             '1898-08-12', 'Vínculo con la administración estadounidense', HAWAII_1898,
             'Es el vínculo de dependencia tras la misma transferencia, no una segunda anexión posterior ni la admisión de un Estado federado.')

    # Only documentary coverage metadata changes. All contemporary dates,
    # reference values and existing records are preserved verbatim.
    d['coverageStart'] = min(d.get('coverageStart', 1880), 1880)
    c['startYear'] = min(c.get('startYear', 1880), 1880)
    h['coverageStart'] = min(h.get('coverageStart', 1880), 1880)
    return d, c, h


def validate(original, result):
    assert prepare(*result) == result, 'Non-idempotent extension'
    ids=[r['id'] for r in result[2]['records']+result[2]['relations']]
    assert len(ids)==len(set(ids)), 'Country history record/relation ID collision'
    for before, after in zip(original, result):
        for key in ('referenceDate', 'retrieved', 'expandedReferenceDate'):
            assert before.get(key) == after.get(key), ('Reference metadata changed', key)
    for before, after, field in [(original[1], result[1], 'events'),
                                  (original[2], result[2], 'records'),
                                  (original[2], result[2], 'relations')]:
        rows = {r['id']: r for r in after[field]}
        assert len(rows) == len(after[field]), ('Duplicate IDs', field)
        for old in before[field]:
            if not old['id'].startswith(PREFIX):
                assert rows.get(old['id']) == old, ('Prior row changed', field, old['id'])
        for row in after[field]:
            if row['id'].startswith(PREFIX):
                start = row.get('start', row.get('date'))
                datetime.date.fromisoformat(start)
                assert FIRST <= start < STOP
                if row.get('end'):
                    _bounded(start, row['end'])
                assert not any(k in row for k in ('geometry', 'coordinates', 'polygon', 'front'))
    old_orgs = {o['id']: o for o in original[0]['organizations']}
    new_orgs = {o['id']: o for o in result[0]['organizations']}
    assert old_orgs.keys() == new_orgs.keys(), 'Organization list changed'
    for oid, before in old_orgs.items():
        after = new_orgs[oid]
        assert {k: v for k, v in before.items() if k != 'memberships'} == {
            k: v for k, v in after.items() if k != 'memberships'}, ('Organization metadata changed', oid)
        for row in before['memberships']:
            if row.get('acquisition') != PREFIX + 'memberships':
                assert row in after['memberships'], ('Previous membership changed', oid, row)
        for i, row in enumerate(after['memberships']):
            if row.get('acquisition') == PREFIX + 'memberships':
                _bounded(row['start'], row['end'])
                assert not any(other['code'] == row['code'] and max(row['start'], other['start']) <
                               min(row['end'], other.get('end', '9999-12-31'))
                               for j, other in enumerate(after['memberships']) if j != i), ('Membership overlap', oid, row)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=pathlib.Path, default=ROOT)
    parser.add_argument('--output-dir', type=pathlib.Path)
    parser.add_argument('--check', action='store_true', help='Validate in memory; never write files.')
    args = parser.parse_args()
    if args.check and args.output_dir:
        parser.error('--check cannot be combined with --output-dir')
    if args.output_dir and args.output_dir.resolve() == args.input_dir.resolve():
        parser.error('Output must be distinct from input; integration is an explicit later step.')
    names = ['affiliations.json', 'historical-context.json', 'country-history.json']
    original = [json.loads((args.input_dir / name).read_text(encoding='utf-8')) for name in names]
    result = prepare(*original)
    validate(original, result)
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, data in zip(names, result):
            (args.output_dir / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Validated1880 extension; input and public files untouched.' if not args.output_dir else 'Validated; wrote explicit output directory.')
    print(json.dumps(dict(events=sum(r['id'].startswith(PREFIX) for r in result[1]['events']),
                          records=sum(r['id'].startswith(PREFIX) for r in result[2]['records']),
                          relations=sum(r['id'].startswith(PREFIX) for r in result[2]['relations']),
                          memberships=sum(m.get('acquisition') == PREFIX + 'memberships'
                                          for o in result[0]['organizations'] for m in o['memberships']))))


if __name__ == '__main__':
    main()
