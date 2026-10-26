"""Pure institutional/conflict additions for 1860–1879; no geometry or media.

prepare(affiliations, context, history) returns independent copies. Existing
organizations and all non-owned observations, including every 1880+ row, survive
exactly. CLI validation is read-only unless a distinct output directory is given.
See docs/CONTEXT-1860-RESEARCH.md for precision and unresolved coverage.
"""
import argparse
import copy
import datetime
import json
import pathlib

PREFIX = 'extension-1860-'
FIRST, STOP = '1860-01-01', '1880-01-01'
ROOT = pathlib.Path(__file__).resolve().parents[1] / 'public/data'
LABEL = 'Fuente institucional o documento primario · investigación 1860–1879'
WINDOW = ('Inicio inclusivo y fin exclusivo. Las fronteras de cobertura no son fechas'
          ' de fundación, paz o disolución. El registro no proporciona geometrías de frentes'
          ' ni una lista completa de beligerantes o instituciones.')
ITALY = 'https://archiviodistatotorino.cultura.gov.it/iorestoacasa-nascita-regno-italia/'
GERMAN_1866 = 'https://www.dhm.de/lemo/kapitel/reaktionszeit/deutscherbund/deutschekrieg'
GERMAN_1871 = 'https://www.dhm.de/lemo/biografie/wilhelm-i'
FRANCO_PRUSSIAN = 'https://www.dhm.de/lemo/kapitel/kaiserreich/reich/krieg1870'
AUSTRIA = 'https://www.parlament.gv.at/verstehen/historisches/1848-1918/abschied-kaiserreich'
CIVIL_WAR = 'https://home.nps.gov/gett/learn/historyculture/civil-war-timeline.htm'
CIVIL_WAR_END = 'https://www.archives.gov/publications/prologue/2015/spring/images/cw-surrenders.html'
MEXICO = 'https://history.state.gov/milestones/1861-1865/french-intervention'
MAXIMILIAN = 'https://www.gob.mx/defensa/documentos/19-de-junio-de-1867-fusilamiento-de-maximiliano-de-habsburgo-y-los-generales-miramon-y-mejia'
SPAIN = 'https://www.congreso.es/es/web/guest/cem/sexrevol'
SPAIN_REPUBLIC = 'https://pares.cultura.gob.es/ParesBusquedas20/catalogo/autoridad/101210'
JAPAN = 'https://www.ndl.go.jp/modern/e/cha1/index.html'
BOSHIN = 'https://id.ndl.go.jp/auth/ndlsh/001102364'
PARAGUAY = 'https://www.senado.leg.br/publicacoes/anais/pdf/ACE/ATAS7-Terceiro_Conselho_de_Estado_1867-1868.pdf'
BRAZIL = 'https://www2.camara.leg.br/legin/fed/leimp/1824-1899/lei-2040-28-setembro-1871-538828-norma-pl.html'
FIJI = 'https://www.foreignaffairs.gov.fj/fiji-high-commission-new-zealand/history/'
ZULU = 'https://www.nam.ac.uk/explore/zulu-war'
AFGHAN = 'https://www.nam.ac.uk/explore/second-afghan-war'
BERLIN = 'https://www.dhm.de/lemo/kapitel/kaiserreich/aussenpolitik/berliner-kongress-1878'


def _bounded(start, end):
    datetime.date.fromisoformat(start)
    datetime.date.fromisoformat(end)
    if not FIRST <= start < end <= STOP:
        raise ValueError(f'Observation outside 1860–1879: {start}..{end}')


def _without_own(rows):
    kept = []
    for row in rows:
        if not row.get('id', '').startswith(PREFIX):
            kept.append(row)
            continue
        start = row.get('start', row.get('date'))
        if not start or not FIRST <= start < STOP or row.get('end', STOP) > STOP:
            raise ValueError(f'Refusing to remove out-of-window owned ID: {row["id"]}')
    return kept


def prepare(affiliations, context, history):
    d, c, h = copy.deepcopy((affiliations, context, history))
    c['events'] = _without_own(c['events'])
    h['records'] = _without_own(h['records'])
    h['relations'] = _without_own(h['relations'])

    def event(ident, title, kind, start, end, keys, text, source, precision=11,
              start_coverage=False, end_coverage=False):
        _bounded(start, end)
        row = dict(id=PREFIX + 'event-' + ident, title=title, type=kind,
                   start=start, end=end, countries=keys.split(), text=text,
                   source=source, sourceLabel=LABEL, note=WINDOW, precision=precision)
        if start_coverage:
            row['startIsCoverageBoundary'] = True
        if end_coverage:
            row['endIsCoverageBoundary'] = True
        c['events'].append(row)

    event('us-civil-war', 'Estados Unidos · guerra de Secesión', 'conflict',
          '1861-04-12', '1866-01-01', 'USA CSA',
          'El ataque a Fort Sumter abre la guerra. La rendición de Lee en Appomattox el 9 de abril de 1865 afecta a su ejército, no a todas las fuerzas confederadas: otras rendiciones continúan durante el año. El cierre de este registro es cobertura anual; la declaración presidencial del fin de la guerra es posterior.',
          CIVIL_WAR, end_coverage=True)
    event('italian-kingdom', 'Italia · proclamación del Reino', 'transition',
          '1861-03-17', '1862-01-01', 'SAR ITA',
          'La ley 4671 atribuye a Víctor Manuel II el título de rey de Italia. El reino de Cerdeña es el antecedente institucional; no existía una Italia unificada en 1860. Venecia y Roma se incorporan mediante procesos posteriores, no por esta ley.', ITALY, end_coverage=True)
    event('german-war', 'Guerra de 1866 y disolución de la Confederación Germánica', 'conflict',
          '1866-06-01', '1866-08-24', 'PRUSSIA AUSTRIAN-EMPIRE ITA',
          'El conflicto enfrenta a Prusia y sus aliados con Austria y sus aliados alemanes; Italia interviene contra Austria. Königgrätz se libra el 3 de julio. La paz de Praga del 23 de agosto deshace la Confederación y prepara la primacía prusiana. El inicio mensual no pretende fijar una declaración única que la fuente distingue de las notificaciones de guerra.',
          GERMAN_1866, precision=10, start_coverage=True)
    event('franco-prussian', 'Guerra franco-prusiana', 'conflict',
          '1870-07-19', '1871-05-11', 'FRA PRUSSIA NGC DEU',
          'Francia declara la guerra a Prusia; participan la Confederación Alemana del Norte y los Estados aliados del sur. Tras Sedán cae el régimen de Napoleón III, pero el conflicto continúa con el Gobierno de Defensa Nacional. El Tratado de Fráncfort se firma el 10 de mayo de 1871. La cesión territorial no se convierte en un frente interpolado.', FRANCO_PRUSSIAN)
    event('german-empire', 'Alemania · proclamación imperial', 'transition',
          '1871-01-18', '1872-01-01', 'PRUSSIA NGC DEU',
          'Guillermo I es proclamado emperador en Versalles. La proclamación, la entrada en vigor de acuerdos constitucionales y la continuidad del reino de Prusia son cuestiones distintas. Prusia continúa como Estado integrante; no desaparece por la proclamación.', GERMAN_1871, end_coverage=True)
    event('ausgleich', 'Monarquía de los Habsburgo · compromiso austrohúngaro', 'transition',
          '1867-01-01', '1868-01-01', 'AUSTRIAN-EMPIRE AUT-HUN HUN',
          'El compromiso reorganiza la monarquía en dos mitades con gobiernos y parlamentos distintos. La negociación, la coronación húngara y la legislación de diciembre son actos diferentes. Se registra el proceso anual de 1867 sin inventar un único día de nacimiento del conjunto.', AUSTRIA,
          precision=9, start_coverage=True, end_coverage=True)
    event('mexico-intervention', 'México · intervención francesa y resistencia republicana', 'conflict',
          '1862-01-01', '1868-01-01', 'MEX MEX-EMPIRE FRA',
          'La intervención francesa favorece un gobierno imperial, mientras la República de Juárez mantiene una autoridad itinerante y la resistencia. La retirada francesa y la caída de Maximiliano culminan en 1867. La expedición tripartita de 1861 es un antecedente; España y Reino Unido no son beligerantes continuos de toda esta ventana.',
          MEXICO, precision=9, start_coverage=True, end_coverage=True)
    event('sexenio', 'España · Sexenio Democrático', 'transition',
          '1868-09-18', '1874-12-30', 'ESP',
          'La revolución de septiembre precede al Gobierno provisional, la regencia de Serrano y el reinado parlamentario de Amadeo I. En 1873 se suceden cuatro presidentes del Ejecutivo republicano; en 1874 sigue una etapa distinta bajo Serrano antes de la restauración monárquica. No son un único gobierno estable.', SPAIN)
    event('boshin', 'Japón · guerra Boshin', 'conflict',
          '1868-01-01', '1870-01-01', 'JPN',
          'La Biblioteca Nacional de Japón delimita la guerra Boshin en 1868–1869. La devolución de poder del shogunato y el nuevo gobierno imperial no eliminan de inmediato la resistencia. Se usa cobertura anual: no se inventan fechas gregorianas a partir de fechas de era japonesa ni áreas controladas por cada bando.',
          BOSHIN, precision=9, start_coverage=True, end_coverage=True)
    event('meiji-institutions', 'Japón · reorganización política de comienzos de Meiji', 'transition',
          '1867-01-01', '1869-01-01', 'JPN',
          'La devolución formal de la autoridad del shogunato de 1867 y el Juramento de los Cinco Artículos de 1868 abren una reorganización del gobierno imperial. No equivalen a la creación de un primer ministro moderno ni a la entrada en vigor inmediata de una constitución parlamentaria.',
          JAPAN, precision=9, start_coverage=True, end_coverage=True)
    event('paraguay-war', 'Guerra del Paraguay y Triple Alianza', 'conflict',
          '1864-01-01', '1871-01-01', 'PRY BRA-EMPIRE ARG URY',
          'La guerra de 1864–1870 y la alianza firmada en Buenos Aires el 1 de mayo de 1865 son cronologías distintas. Brasil, Argentina y Uruguay suscriben el tratado contra el Gobierno paraguayo. No se incluye a Paraguay como miembro de esa alianza ni se supone que los tres aliados entraron en guerra al mismo tiempo.',
          PARAGUAY, precision=9, start_coverage=True, end_coverage=True)
    event('brazil-free-womb', 'Brasil · Ley del Vientre Libre', 'transition',
          '1871-09-28', '1872-01-01', 'BRA-EMPIRE',
          'La ley 2.040 declara libres a los hijos de mujeres esclavizadas nacidos desde su fecha y establece condiciones de tutela y servicios. Es una emancipación parcial, no la abolición general de la esclavitud. La regente Isabel sanciona la ley en nombre del emperador.', BRAZIL, end_coverage=True)
    event('fiji-cession', 'Fiyi · cesión a la Corona británica', 'transition',
          '1874-10-10', '1875-01-01', 'FJI GBR',
          'La cesión del 10 de octubre de 1874 establece el dominio colonial británico. La institución monárquica y las autoridades locales anteriores no se equiparan al Gobierno de la república contemporánea. El cierre anual no supone el fin de la colonia.', FIJI, end_coverage=True)
    event('anglo-zulu', 'Guerra anglo-zulú · invasión británica y resistencia', 'conflict',
          '1879-01-01', STOP, 'GBR ZAF',
          'Las fuerzas británicas invaden el reino zulú en enero de 1879. La victoria zulú en Isandlwana y la posterior campaña británica son fases diferentes. La clave sudafricana enlaza el área; no atribuye a una Unión Sudafricana todavía inexistente la condición de beligerante. No se deducen frentes de este resumen.',
          ZULU, precision=9, start_coverage=True, end_coverage=True)
    event('second-afghan', 'Segunda guerra anglo-afgana · fase de 1878–1879', 'conflict',
          '1878-11-01', STOP, 'AFG GBR IND',
          'Fuerzas británico-indias invaden Afganistán en noviembre de 1878. Gandamak, firmado en mayo de 1879, no pone fin duradero al conflicto: la crisis de la residencia británica y nuevas operaciones siguen ese año. La guerra continúa después de 1879; el límite de esta observación no es un armisticio ni una retirada.',
          AFGHAN, precision=10, start_coverage=True, end_coverage=True)
    event('berlin-congress', 'Congreso de Berlín de 1878', 'transition',
          '1878-06-13', '1878-07-14', 'DEU AUT-HUN GBR FRA ITA RUE OTT BGR ROU SRK MNK',
          'El congreso revisa los acuerdos de San Stefano y firma el Tratado de Berlín el 13 de julio. Modifica el arreglo balcánico y reconoce o redefine estatutos distintos. La ocupación administrativa de Bosnia-Herzegovina no equivale a su anexión inmediata a Austria-Hungría; Bulgaria tampoco se convierte en reino independiente en 1878.', BERLIN)

    def record(ident, keys, section, title, start, end, text, source, precision=11,
               start_coverage=False, end_coverage=False):
        _bounded(start, end)
        row = dict(id=PREFIX + 'record-' + ident, keys=keys.split(), section=section,
                   title=title, start=start, end=end, text=text, source=source,
                   sourceLabel=LABEL, note=WINDOW, precision=precision)
        if start_coverage or start == FIRST:
            row['startIsCoverageBoundary'] = True
        if end_coverage or end == STOP:
            row['endIsCoverageBoundary'] = True
        h['records'].append(row)

    record('us-federal-continuity', 'USA CSA', 'institutions', 'Unión federal y Confederación secesionista',
           '1861-01-01', '1866-01-01',
           'La Confederación se constituye por secesión de Estados; no sustituye al Gobierno federal estadounidense en todo el territorio. La derrota militar tiene rendiciones sucesivas en 1865. El país federal no vuelve a fundarse después de la guerra.', CIVIL_WAR_END, precision=9, start_coverage=True, end_coverage=True)
    record('us-war-end', 'USA', 'defense', 'Fin militar y declaración formal de paz',
           '1865-04-09', '1867-01-01',
           'Appomattox no termina todas las hostilidades ni todas las rendiciones confederadas. La declaración presidencial de fin de guerra se produce el 20 de agosto de 1866. Se distinguen ese acto y la posterior Reconstrucción.', CIVIL_WAR_END, end_coverage=True)
    record('italian-institutions', 'SAR ITA', 'institutions', 'Del Reino de Cerdeña al Reino de Italia',
           '1861-03-17', STOP,
           'La nueva denominación institucional conserva al soberano y su ordinal, Víctor Manuel II. La unificación territorial y la integración administrativa son procesos graduales; la ley del título real no incorpora de una vez todos los territorios pretendidos.', ITALY)
    record('prussian-continuity', 'PRUSSIA NGC DEU', 'institutions', 'Prusia, federación e Imperio son ámbitos distintos',
           '1867-01-01', STOP,
           'La Confederación Alemana del Norte precede al Imperio. La proclamación de 1871 cambia el ámbito federal, mientras Prusia subsiste como reino integrante. El rey de Prusia, la presidencia federal y el título imperial no se confunden en un único cargo retrospectivo.', GERMAN_1871, precision=9, start_coverage=True)
    record('dual-monarchy', 'AUSTRIAN-EMPIRE AUT-HUN HUN', 'institutions', 'Dos mitades, gobiernos propios y asuntos comunes',
           '1867-01-01', STOP,
           'El compromiso de 1867 reorganiza la monarquía en las mitades austríaca y húngara. Las instituciones compartidas no crean un primer ministro único de todo el conjunto. La legislación de diciembre y la coronación húngara son fases del proceso, no fechas intercambiables.', AUSTRIA, precision=9, start_coverage=True)
    record('mexican-parallel-governments', 'MEX MEX-EMPIRE', 'institutions', 'República e Imperio: gobiernos concurrentes',
           '1864-01-01', '1868-01-01',
           'La autoridad imperial apoyada por Francia coexiste con el Gobierno republicano de Juárez y resistencias regionales. No se presenta a Juárez como inexistente durante la intervención ni se asigna control uniforme a Maximiliano. Tras la derrota imperial continúa la República, que no se funda en 1867.', MEXICO, precision=9, start_coverage=True, end_coverage=True)
    record('spanish-regimes', 'ESP', 'institutions', 'Gobierno provisional, regencia, monarquía y República',
           '1868-09-18', '1874-12-30',
           'Cada etapa del Sexenio mantiene instituciones y titulares propios. La regencia de Serrano no es un reinado; Amadeo jura en enero de 1871; la Primera República comienza en febrero de 1873. La fase de Serrano de 1874 se distingue de los cuatro presidentes del Ejecutivo de 1873.', SPAIN)
    record('spanish-restoration', 'ESP', 'institutions', 'Restauración de la monarquía de Alfonso XII',
           '1874-12-29', STOP,
           'La restauración monárquica de diciembre de 1874 pone fin al régimen republicano. No es una independencia nueva del territorio español ni convierte a sus jefes anteriores en titulares del nuevo régimen.', SPAIN_REPUBLIC)
    record('japanese-transformation', 'JPN', 'institutions', 'Devolución de autoridad y reorganización Meiji',
           '1867-01-01', STOP,
           'La devolución formal de poder de 1867, la guerra Boshin y las reformas imperiales tienen cronologías distintas. El Juramento de 1868 enuncia principios del nuevo gobierno, sin equivaler al parlamentarismo posterior. No se llama primer ministro a todos los cargos del Daijō-kan.', JAPAN, precision=9, start_coverage=True)
    record('paraguay-alliance', 'BRA-EMPIRE ARG URY PRY', 'defense', 'Tratado de la Triple Alianza de 1865',
           '1865-05-01', '1871-01-01',
           'El tratado reúne al Imperio del Brasil, Argentina y Uruguay contra el Gobierno paraguayo. El protocolo y los compromisos de la alianza no constituyen la Triple Alianza europea de 1882. La cobertura de la guerra no acredita automáticamente la duración de cada obligación posterior del tratado.', PARAGUAY, end_coverage=True)
    record('brazil-slavery', 'BRA-EMPIRE', 'institutions', 'Emancipación parcial y persistencia de la esclavitud',
           '1871-09-28', STOP,
           'La Ley del Vientre Libre declara libres a los hijos nacidos desde su fecha, con condiciones sobre tutela, indemnización y servicios. La esclavitud de sus madres y la de gran parte de la población esclavizada no desaparece con esa ley. No se anticipa a 1871 la abolición general.', BRAZIL)
    record('fiji-colonial', 'FJI GBR', 'institutions', 'Cesión de Fiyi y administración colonial',
           '1874-10-10', STOP,
           'La cesión a la Corona británica de 1874 se distingue de la independencia de 1970. La autoridad británica y las instituciones locales tienen ámbitos diferentes; esta ventana no proporciona una serie completa de gobernadores o jefes locales.', FIJI)
    record('zulu-war', 'ZAF GBR', 'defense', 'Reino zulú y expansión imperial británica',
           '1879-01-01', STOP,
           'El reino zulú de Cetshwayo es el adversario de la invasión británica, no la Sudáfrica contemporánea. Las campañas de 1879 y la reorganización posterior del territorio requieren fechas propias; la victoria militar no se presenta como incorporación administrativa instantánea.', ZULU, precision=9, start_coverage=True)
    record('afghan-relations', 'AFG IND GBR', 'defense', 'Invasión, Gandamak y continuación de la guerra',
           '1878-11-01', STOP,
           'La campaña británico-india intenta imponer influencia sobre la política exterior afgana. El tratado de 1879 y el ataque posterior a la residencia abren fases distintas. El registro se interrumpe al terminar 1879 y no adelanta las campañas y acuerdos posteriores.', AFGHAN, precision=10, start_coverage=True)
    record('berlin-territories', 'BGR ROU SRK MNK OTT AUT-HUN RUE', 'territory', 'Estatutos balcánicos después del Tratado de Berlín',
           '1878-07-13', STOP,
           'Serbia, Montenegro, Rumanía y Bulgaria reciben tratamientos jurídicos diferentes. Bulgaria queda como principado autónomo bajo soberanía otomana; Bosnia-Herzegovina se coloca bajo ocupación y administración austrohúngaras. No se adelantan a 1878 la anexión de Bosnia ni la independencia y el rango real búlgaros de 1908.', BERLIN)

    def relation(ident, a, b, date, label, source, note, precision=11, coverage=False):
        if not FIRST <= date < STOP:
            raise ValueError('Transition outside 1860–1879')
        row = dict(id=PREFIX + 'relation-' + ident,
                   **{'from': dict(key=a[0], name=a[1], year=a[2]),
                      'to': dict(key=b[0], name=b[1], year=b[2])},
                   date=date, type='transition', label=label, source=source,
                   sourceLabel=LABEL, note=note, precision=precision)
        if coverage:
            row['dateIsCoverageBoundary'] = True
        h['relations'].append(row)

    relation('sardinia-italy', ('SAR', 'Reino de Cerdeña', 1860), ('ITA', 'Reino de Italia', 1862),
             '1861-03-17', 'Cambio de título estatal: Reino de Italia', ITALY,
             'Enlace institucional y de navegación; no afirma que todos los territorios italianos se incorporen en esta fecha.')
    relation('austrian-dual', ('AUSTRIAN-EMPIRE', 'Imperio austríaco', 1866), ('AUT-HUN', 'Monarquía austrohúngara', 1868),
             '1867-12-31', 'Reorganización dual de 1867 · referencia anual', AUSTRIA,
             'Fecha de observación al cierre de 1867, no supuesto día único de creación. Se distinguen negociación, coronación y legislación.', precision=9, coverage=True)
    relation('prussia-german-empire', ('PRUSSIA', 'Reino de Prusia', 1870), ('DEU', 'Imperio alemán', 1872),
             '1871-01-18', 'Prusia como núcleo del nuevo Imperio', GERMAN_1871,
             'Prusia no se extingue: el enlace permite pasar del reino al ámbito imperial, sin fingir una sustitución territorial completa.')
    relation('north-german-empire', ('NGC', 'Confederación Alemana del Norte', 1870), ('DEU', 'Imperio alemán', 1872),
             '1871-01-18', 'De la federación septentrional al ámbito imperial', GERMAN_1871,
             'Se ancla la navegación en la proclamación imperial. La entrada en vigor de los acuerdos constitucionales es un acto distinto.')
    relation('mexican-republic', ('MEX-EMPIRE', 'Segundo Imperio mexicano', 1866), ('MEX', 'República mexicana', 1868),
             '1867-06-19', 'Caída del régimen imperial y continuidad republicana', MAXIMILIAN,
             'Ancla documental: ejecución de Maximiliano. No supone que la República dejara de existir antes ni que su control de todo México cambiara ese mismo día.')
    relation('confederacy-union', ('CSA', 'Confederación secesionista', 1864), ('USA', 'Estados Unidos', 1866),
             '1865-12-31', 'Derrota confederada de 1865 · enlace anual', CIVIL_WAR_END,
             'Observación anual de rendiciones sucesivas, no fecha legal única de disolución ni nueva fundación de Estados Unidos. La declaración presidencial de paz es de 1866.', precision=9, coverage=True)

    c['startYear'] = min(c.get('startYear', 1860), 1860)
    h['coverageStart'] = min(h.get('coverageStart', 1860), 1860)
    # No organizations or memberships are created: military event context does
    # not certify the complete legal lifetime of alliance obligations.
    return d, c, h


def validate(original, result):
    assert prepare(*result) == result, 'Non-idempotent extension'
    assert original[0] == result[0], 'Affiliation corpus changed'
    all_ids = [r['id'] for r in result[2]['records'] + result[2]['relations']]
    assert len(all_ids) == len(set(all_ids)), 'Global history record/relation ID collision'
    own_ids = [r['id'] for r in result[1]['events'] + result[2]['records'] + result[2]['relations']
               if r['id'].startswith(PREFIX)]
    assert len(own_ids) == len(set(own_ids)), 'New event/record/relation ID collision'
    for before, after in zip(original, result):
        for key in ('referenceDate', 'retrieved', 'expandedReferenceDate'):
            assert before.get(key) == after.get(key), ('Reference metadata changed', key)
    for before, after, field in [(original[1], result[1], 'events'),
                                 (original[2], result[2], 'records'),
                                 (original[2], result[2], 'relations')]:
        rows = {row['id']: row for row in after[field]}
        for old in before[field]:
            if not old['id'].startswith(PREFIX):
                assert rows.get(old['id']) == old, ('Previous row changed', field, old['id'])
        for row in after[field]:
            if row['id'].startswith(PREFIX):
                start = row.get('start', row.get('date'))
                datetime.date.fromisoformat(start)
                assert FIRST <= start < STOP
                if row.get('end'):
                    _bounded(start, row['end'])
                assert not any(key in row for key in ('geometry', 'coordinates', 'polygon', 'front'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=pathlib.Path, default=ROOT)
    parser.add_argument('--output-dir', type=pathlib.Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check and args.output_dir:
        parser.error('--check cannot be combined with --output-dir')
    if args.output_dir and args.output_dir.resolve() == args.input_dir.resolve():
        parser.error('Use a distinct output directory; integration is a later explicit step.')
    names = ('affiliations.json', 'historical-context.json', 'country-history.json')
    original = [json.loads((args.input_dir / name).read_text(encoding='utf-8')) for name in names]
    result = prepare(*original)
    validate(original, result)
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, data in zip(names, result):
            (args.output_dir / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(events=sum(r['id'].startswith(PREFIX) for r in result[1]['events']),
                          records=sum(r['id'].startswith(PREFIX) for r in result[2]['records']),
                          relations=sum(r['id'].startswith(PREFIX) for r in result[2]['relations']),
                          idempotent=True, previousRowsUnchanged=True,
                          output=str(args.output_dir) if args.output_dir else 'in-memory validation only')))


if __name__ == '__main__':
    main()
