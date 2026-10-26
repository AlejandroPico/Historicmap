"""Pure, bounded authority supplements for 1860–1879.

Sources and deliberately unresolved offices: docs/AUTHORITIES-1860-RESEARCH.md.
No network, media downloads, flag changes or implicit output. This is a curated
supplement, not a claim that every cabinet or colonial administration is known.
"""
import argparse
import copy
import datetime
import json
import pathlib

FIRST, LAST = '1860-01-01', '1879-12-31'
TAG = 'curated-1860-authorities-0.14'
SEEDS = [
    ('PRUSSIA', 'Q27306', 'Reino de Prusia'),
    ('NGC', 'Q150981', 'Confederación Alemana del Norte'),
    ('AUSTRIAN-EMPIRE', 'Q131964', 'Imperio austríaco'),
    ('AUT-HUN', 'Q28513', 'Austria-Hungría'),
    ('RUE', 'Q34266', 'Imperio ruso'),
    ('OTT', 'Q12560', 'Imperio otomano'),
    ('QING', 'Q8733', 'Imperio Qing'),
    ('BRA-EMPIRE', 'Q217230', 'Imperio del Brasil'),
    ('MEX-EMPIRE', 'Q371334', 'Segundo Imperio mexicano'),
    ('SAR', 'Q165154', 'Reino de Cerdeña'),
]


def rows():
    """Return records, with explicit observation bounds for year-only sources."""
    result = []

    def term(key, person, name, role, start, end, source, note='', precision=11,
             start_coverage=False, end_coverage=False):
        if not FIRST <= start <= end <= LAST:
            raise ValueError('Curation must remain within 1860–1879')
        record = dict(person=person, name=name, role=role, start=start, end=end,
                      source=source, note=note, precision=precision, curated=True,
                      acquisition=TAG)
        if start_coverage or start == FIRST:
            record['startIsCoverageBoundary'] = True
        if end_coverage or end == LAST:
            record['endIsCoverageBoundary'] = True
        if record.get('startIsCoverageBoundary') or record.get('endIsCoverageBoundary'):
            record['note'] += (' Los límites de cobertura delimitan una observación documental;'
                               ' no representan un nombramiento ni una dimisión.')
        result.append((key, record))

    france = 'https://www.elysee.fr/'
    term('FRA', 'Q7721', 'Napoleón III', 'Emperador de los franceses', FIRST, '1870-09-04',
         'https://catalogue.bnf.fr/ark:/12148/cb15503306b',
         'El Segundo Imperio termina con la proclamación de la República; el Gobierno de Defensa Nacional es una institución distinta.')
    term('FRA', 'Q441235', 'Louis Jules Trochu', 'Presidente del Gobierno de Defensa Nacional',
         '1870-09-04', '1870-12-31', 'https://catalogue.bnf.fr/ark:/12148/cb15503306b',
         'Preside un gobierno colectivo; no es presidente de la República. La transición interna de enero-febrero de 1871 requiere revisión separada.', end_coverage=True)
    term('FRA', 'Q5738', 'Adolphe Thiers', 'Jefe del Poder Ejecutivo de la República francesa',
         '1871-02-17', '1871-08-30', france + 'adolphe-thiers',
         'El título de presidente de la República se adquiere el 31 de agosto, no al comenzar el Poder Ejecutivo en febrero.')
    term('FRA', 'Q5738', 'Adolphe Thiers', 'Presidente de la República',
         '1871-08-31', '1873-05-24', france + 'adolphe-thiers')
    term('FRA', 'Q158838', 'Patrice de Mac Mahon', 'Presidente de la República',
         '1873-05-24', '1879-01-30',
         'https://www.interieur.gouv.fr/archive/annexe-n-13-les-presidents-de-la-iieme-a-la-veme-republique')
    term('FRA', 'Q296083', 'Jules Grévy', 'Presidente de la República',
         '1879-01-30', LAST, france + 'jules-grevy')

    spain = 'https://www.congreso.es/es/web/guest/cem/sexrevol'
    cabinets = 'https://www.lamoncloa.gob.es/presidente/presidentes-desde-1823/Paginas/index.aspx'
    term('ESP', 'Q183085', 'Isabel II', 'Reina de España', FIRST, '1868-09-30',
         'https://coleccion.bde.es/wca/es/secciones/coleccion/obras/isabel-ii-p_140.html',
         'Se fecha el fin del ejercicio por su salida al exilio; la abdicación dinástica posterior de 1870 es un acto distinto.')
    term('ESP', 'Q515741', 'Francisco Serrano', 'Jefe del Gobierno provisional',
         '1868-10-31', '1869-06-17', spain,
         'Observación desde el cierre de octubre: el Congreso sitúa su encargo a comienzos de octubre; no se equipara el encargo a la fecha de constitución ministerial.',
         precision=10, start_coverage=True)
    term('ESP', 'Q515741', 'Francisco Serrano', 'Regente del Reino de España',
         '1869-06-18', '1871-01-01', spain,
         'Regencia tras la Constitución de 1869, antes del juramento de Amadeo; no equivale a un reinado personal.')
    term('ESP', 'Q379787', 'Juan Prim', 'Presidente del Consejo de Ministros',
         '1869-06-18', '1869-08-25', cabinets)
    term('ESP', 'Q379787', 'Juan Prim', 'Presidente del Consejo de Ministros',
         '1869-09-21', '1870-12-27', cabinets,
         'El intervalo de Topete y el relevo tras el atentado no se ocultan mediante un mandato continuo de Prim.')
    term('ESP', 'Q32432', 'Amadeo I', 'Rey de España', '1871-01-02', '1873-02-11', spain,
         'Juramento y proclamación el 2 de enero de 1871; elección parlamentaria el 16 de noviembre de 1870.')
    for q, name, start, end in [
        ('Q553120', 'Estanislao Figueras', '1873-02-11', '1873-06-11'),
        ('Q450271', 'Francisco Pi y Margall', '1873-06-11', '1873-07-18'),
        ('Q742660', 'Nicolás Salmerón', '1873-07-18', '1873-09-07'),
        ('Q718209', 'Emilio Castelar', '1873-09-07', '1874-01-03'),
    ]:
        term('ESP', q, name, 'Presidente del Poder Ejecutivo de la Primera República', start, end,
             spain if q == 'Q553120' else cabinets,
             'La presidencia del Poder Ejecutivo no se confunde con una jefatura de Estado parlamentaria moderna. Figueras es elegido el 11 de febrero; la tabla de gabinetes fecha el inicio ministerial el día 12.')
    term('ESP', 'Q515741', 'Francisco Serrano', 'Jefe del Poder Ejecutivo de la República',
         '1874-01-03', '1874-12-29', 'https://pares.cultura.gob.es/ParesBusquedas20/catalogo/autoridad/101210',
         'La etapa de 1874 se distingue de los cuatro presidentes de 1873; la presidencia del Consejo tiene sus propios relevos.')
    term('ESP', 'Q32347', 'Alfonso XII', 'Rey de España', '1874-12-29', LAST,
         'https://www.congreso.es/en/cem/alfonsoxii',
         'Restauración de la monarquía a finales de 1874; la llegada del rey a España en 1875 es posterior.')

    italy = 'https://archiviodistatotorino.cultura.gov.it/iorestoacasa-nascita-regno-italia/'
    term('SAR', 'Q168691', 'Víctor Manuel II', 'Rey de Cerdeña', FIRST, '1861-03-16', italy,
         'Estado predecesor de Italia; no se proyecta retrospectivamente la unificación sobre 1860.')
    term('ITA', 'Q168691', 'Víctor Manuel II', 'Rey de Italia', '1861-03-17', '1878-01-01', italy,
         'Ley 4671 de 17 de marzo de 1861. La observación final con precisión anual no afirma el día de la sucesión de 1878.',
         precision=9, end_coverage=True)
    term('ITA', 'Q153688', 'Umberto I', 'Rey de Italia', '1878-12-31', LAST,
         'https://palazzo.quirinale.it/luoghi/pdf/it/sala-regno-italia.pdf',
         'La fuente institucional consultada ofrece el reinado desde 1878. Se usa el cierre del año como observación, pendiente de contraste del día.',
         precision=9, start_coverage=True)

    german = 'https://www.dhm.de/lemo/biografie/wilhelm-i'
    term('PRUSSIA', 'Q57180', 'Federico Guillermo IV', 'Rey de Prusia · bajo regencia',
         FIRST, '1861-01-02', german,
         'Guillermo ejerce la regencia por la incapacidad del rey; la coronación posterior no es el comienzo del reinado siguiente.')
    term('PRUSSIA', 'Q150652', 'Guillermo I', 'Regente de Prusia', FIRST, '1861-01-02', german)
    term('PRUSSIA', 'Q150652', 'Guillermo I', 'Rey de Prusia', '1861-01-02', LAST, german,
         'Prusia no desaparece al crearse el Imperio alemán; continúa como reino integrante.')
    term('NGC', 'Q150652', 'Guillermo I', 'Titular de la Presidencia federal',
         '1867-12-31', '1870-12-31', german,
         'Confederación Alemana del Norte desde 1867; observación anual, no un nombramiento el 31 de diciembre.', precision=9, start_coverage=True, end_coverage=True)
    term('DEU', 'Q150652', 'Guillermo I', 'Emperador alemán', '1871-01-18', LAST, german,
         'Se fecha la proclamación imperial de Versalles; la entrada en vigor constitucional y la continuidad de la Presidencia federal requieren distinguir actos.')
    term('DEU', 'Q8442', 'Otto von Bismarck', 'Canciller del Imperio alemán',
         '1871-12-31', LAST, 'https://www.dhm.de/lemo/biografie/otto-bismarck',
         'Observación anual de la cancillería imperial desde 1871; la presidencia del Gobierno prusiano es un cargo distinto.', precision=9, start_coverage=True)

    habsburg = 'https://www.habsburger.net/de/kapitel/franz-josephs-kroenung-zum-koenig-von-ungarn'
    term('AUSTRIAN-EMPIRE', 'Q51056', 'Francisco José I', 'Emperador de Austria',
         FIRST, '1866-12-31', habsburg,
         'La transformación en monarquía dual se produce en 1867; no se inventa un día único a partir de la coronación húngara.', precision=9, end_coverage=True)
    term('AUT-HUN', 'Q51056', 'Francisco José I', 'Emperador de Austria y rey de Hungría · soberano común',
         '1867-12-31', LAST, habsburg,
         'Observación desde el cierre de 1867. Coronación húngara el 8 de junio; Austria y Hungría tienen gobiernos propios, no un primer ministro único.', precision=9, start_coverage=True)
    term('RUE', 'Q83171', 'Alejandro II', 'Emperador de Rusia', FIRST, LAST,
         'https://imperialhouse.ru/rus/imperialhouse/succession/monarh/aleksandr-ii-nikolaevich-osvoboditel-1855-1881.html',
         'Reinado 1855–1881; no se mezclan fechas de calendario juliano y gregoriano en los límites de esta ventana.')
    term('GBR', 'Q9439', 'Victoria', 'Reina del Reino Unido', FIRST, LAST,
         'https://api.parliament.uk/regnal-years/reigns/6',
         'La soberana se distingue del primer ministro. Los títulos coloniales y las autoridades locales necesitan registros propios.')

    ottoman = 'https://ttk.gov.tr/osmanli-padisahlari/'
    for q, name, start, end in [
        ('Q174772', 'Abdülmecid I', FIRST, '1861-06-25'),
        ('Q151500', 'Abdülaziz', '1861-06-25', '1876-05-30'),
        ('Q199827', 'Murad V', '1876-05-30', '1876-08-31'),
        ('Q134817', 'Abdülhamid II', '1876-08-31', LAST),
    ]:
        term('OTT', q, name, 'Sultán del Imperio otomano', start, end, ottoman,
             'La secuencia de 1876 conserva sus tres sultanes; la deposición de Abdülaziz precede a su muerte.')

    qing = 'https://www.dpm.org.cn/court/lineage/226248.html'
    term('QING', 'Q334452', 'Xianfeng', 'Emperador Qing', FIRST, '1861-01-01', qing,
         'Ventana anual; pendiente el contraste del día gregoriano de sucesión de 1861.', precision=9, end_coverage=True)
    term('QING', 'Q318811', 'Tongzhi', 'Emperador Qing', '1861-12-31', '1875-01-01', qing,
         'Accede en 1861, mientras la era Tongzhi comienza en 1862. El año lunar Tongzhi 13 cruza el año gregoriano 1875; la observación final no afirma un fallecimiento el 1 de enero.',
         precision=9, start_coverage=True, end_coverage=True)
    term('QING', 'Q299710', 'Guangxu', 'Emperador Qing · menor bajo regencia',
         '1875-12-31', LAST, 'https://www.dpm.org.cn/court/lineage/226254.html',
         'Observación anual desde 1875. Las emperatrices viudas Ci’an y Cixi ejercen la regencia; no se atribuye el gobierno efectivo personal al emperador niño.',
         precision=9, start_coverage=True)
    # Komei/Meiji's existing Gregorian records are retained; the Imperial Household
    # chronology uses Japanese era years and is not silently converted here.
    term('JPN', 'Q287657', 'Tokugawa Yoshinobu', 'Shōgun · autoridad del bakufu',
         '1866-12-31', '1867-01-01', 'https://www.ndl.go.jp/en/jikihitsu/part1/s1_3/',
         'La Biblioteca Nacional fecha el acceso en 1866 y la devolución del poder en 1867. Observación de años, pendiente de conversión de calendario; no es un primer ministro moderno.',
         precision=9, start_coverage=True, end_coverage=True)
    term('JPN', 'Q516646', 'Sanjō Sanetomi', 'Daijō-daijin · jefe del Daijō-kan',
         '1871-12-31', LAST, 'https://www.ndl.go.jp/portrait/e/datas/97/?lang=en',
         'Observación anual desde 1871. El cargo de primer ministro moderno no se crea hasta 1885.', precision=9, start_coverage=True)

    presidents = 'https://www.archives.gov/research/census/presidents'
    for q, name, start, end in [
        ('Q12325', 'James Buchanan', FIRST, '1861-03-04'),
        ('Q91', 'Abraham Lincoln', '1861-03-04', '1865-04-15'),
        ('Q8612', 'Andrew Johnson', '1865-04-15', '1869-03-04'),
        ('Q34836', 'Ulysses S. Grant', '1869-03-04', '1877-03-04'),
        ('Q35686', 'Rutherford B. Hayes', '1877-03-04', LAST),
    ]:
        term('USA', q, name, 'Presidente de los Estados Unidos · jefatura del Estado y del Gobierno', start, end, presidents)

    mexico = 'https://www.constitucion1917.gob.mx/es/inehrm/juarez'
    term('MEX', 'Q182276', 'Benito Juárez', 'Presidente de la República · gobierno republicano',
         FIRST, '1872-07-18', mexico,
         'El Gobierno republicano continúa de forma itinerante durante la intervención francesa; no desaparece por la proclamación imperial.')
    term('MEX', 'Q316210', 'Sebastián Lerdo de Tejada', 'Presidente de la República',
         '1872-07-18', '1876-01-01', 'https://nuevaescuelamexicana.sep.gob.mx/contenido/coleccion/18741/',
         'Sucesión tras la muerte de Juárez; el límite final anual mantiene explícitamente pendiente el calendario de gobiernos rivales de 1876.', precision=9, end_coverage=True)
    term('MEX', 'Q150688', 'Porfirio Díaz', 'Presidente de la República', '1877-12-31', LAST,
         'https://www.loc.gov/exhibits/mexican-revolution-and-the-united-states/porfiriato-sp.html',
         'Observación estable desde el cierre de 1877; no se ocultan las interinidades de 1876–1877 ni se afirma un único relevo en noviembre de 1876.', precision=9, start_coverage=True)
    term('MEX-EMPIRE', 'Q84192', 'Maximiliano I', 'Emperador de México · gobierno imperial',
         '1864-04-10', '1867-06-19',
         'https://www.gob.mx/cultura/prensa/reflexionaran-en-torno-al-segundo-imperio-a-160-anos-de-la-llegada-de-maximiliano-de-habsburgo-a-mexico?idiom=es-MX',
         'Aceptación de la Corona en Miramar, anterior a su llegada a Veracruz; el fin se vincula a su ejecución. Gobierno concurrente con la República de Juárez, sin afirmar control territorial uniforme.')
    term('BRA-EMPIRE', 'Q156774', 'Pedro II', 'Emperador del Brasil', FIRST, LAST,
         'https://bndigital.bn.gov.br/dossies/periodicos-literatura/personagens-periodicos-literatura/dom-pedro-ii/',
         'El emperador se distingue de los presidentes del Consejo de Ministros. La regencia termina en 1840 y la coronación de 1841 no es un nuevo comienzo del reinado.')
    brazil_cabinets = 'https://mapa.an.gov.br/images/publicacoes/CadernoMAPA2/files/assets/basic-html/page-77.html'
    for q, name, start, end in [
        ('Q1791359', 'José Maria da Silva Paranhos', '1871-03-07', '1875-06-25'),
        ('Q712089', 'Luís Alves de Lima e Silva', '1875-06-25', '1878-01-05'),
        ('Q1791206', 'João Lins Vieira Cansanção de Sinimbu', '1878-01-05', LAST),
    ]:
        term('BRA-EMPIRE', q, name, 'Presidente del Consejo de Ministros del Brasil',
             start, end, brazil_cabinets,
             'Se usa la columna de presidencia del Consejo, distinta de los titulares de Justicia y sus interinidades mostrados en la misma tabla. Los gabinetes anteriores quedan pendientes de una lectura completa de la serie.')

    portugal = 'https://www.parquesdesintra.pt/media/upzl30vk/colecoesemfoco_pnsintra_ebook_2_lq.pdf'
    term('PRT', 'Q156048', 'Pedro V', 'Rey de Portugal', FIRST, '1861-01-01', portugal,
         'Observación anual anterior a la sucesión de 1861; no se identifica acceso al trono con aclamación ceremonial.', precision=9, end_coverage=True)
    term('PRT', 'Q156175', 'Luis I', 'Rey de Portugal', '1861-12-31', LAST, portugal,
         'Observación anual desde el cierre de 1861; el día de la sucesión requiere contraste específico.', precision=9, start_coverage=True)

    dutch = 'https://www.koninklijkhuis.nl/onderwerpen/koninklijk-huis/geschiedenis/koningen-en-koninginnen/koning-willem-3-1849-1890'
    for key, role in [('NLD', 'Rey de los Países Bajos'), ('LUX', 'Gran duque de Luxemburgo · unión personal')]:
        term(key, 'Q125649', 'Guillermo III', role, FIRST, LAST, dutch,
             'La unión personal no constituye anexión ni elimina la administración separada de Luxemburgo.')
    belgium = 'https://www.monarchie.be/en/royal-family/history'
    term('BEL', 'Q12971', 'Leopoldo I', 'Rey de los belgas', FIRST, '1865-12-10', belgium)
    term('BEL', 'Q12967', 'Leopoldo II', 'Rey de los belgas', '1865-12-31', LAST, belgium,
         'Observación anual de la sucesión; pendiente distinguir fallecimiento, asunción constitucional y juramento.', precision=9, start_coverage=True)
    denmark = 'https://www.kongehuset.dk/monarkiet-i-danmark/kongerakken'
    term('DNK', 'Q94941', 'Federico VII', 'Rey de Dinamarca', FIRST, '1863-11-15', denmark)
    term('DNK', 'Q151305', 'Cristián IX', 'Rey de Dinamarca', '1863-12-31', LAST, denmark,
         'Observación anual después de la sucesión de 1863.', precision=9, start_coverage=True)
    sweden = 'https://historiska.se/en/list-of-swedish-monarchs/'
    for key in ['SWE', 'NOR']:
        term(key, 'Q52925', 'Carlos XV de Suecia · Carlos IV de Noruega', 'Rey de Suecia y Noruega · unión personal', FIRST, '1872-01-01', sweden,
             'La unión personal no se equipara a un Estado unitario. Límite anual de observación del relevo de 1872.', precision=9, end_coverage=True)
        term(key, 'Q52924', 'Óscar II', 'Rey de Suecia y Noruega · unión personal', '1872-12-31', LAST, sweden,
             'Observación desde el cierre de 1872; el fin de la unión en 1905 queda fuera de esta ventana.', precision=9, start_coverage=True)
    return result


def curate(incoming):
    data = copy.deepcopy(incoming)
    countries = data['countries']
    portraits = {leader['person']: copy.deepcopy(leader['portrait'])
                 for country in countries.values() for leader in country.get('leaders', [])
                 if leader.get('portrait')}
    for country in countries.values():
        country['leaders'] = [leader for leader in country.get('leaders', [])
                              if leader.get('acquisition') != TAG]
    for key, qid, name in SEEDS:
        country = countries.setdefault(key, dict(flags=[], leaders=[]))
        country.setdefault('qid', qid)
        country.setdefault('name', name)
    additions = rows()
    targets = {(key, leader['person']) for key, leader in additions}
    for key, person in targets:
        country = countries.setdefault(key, dict(flags=[], leaders=[]))
        intervals = [(leader['start'], leader['end']) for candidate, leader in additions
                     if candidate == key and leader['person'] == person]
        # The acquired Trochu record labels him President of the Republic. This
        # is a substantive office error, including the unaudited January tail.
        if key == 'FRA' and person == 'Q441235':
            intervals = [(FIRST, LAST)]
        kept = []
        for old in country['leaders']:
            # Exact immutable preservation of every term crossing into 1880+.
            if (old['person'] != person or old['end'] >= '1880-01-01'
                    or old['start'] > LAST or old['end'] < FIRST):
                kept.append(old)
                continue
            chunks = [copy.deepcopy(old)]
            for start, end in intervals:
                pending = []
                for chunk in chunks:
                    if chunk['start'] > end or chunk['end'] < start:
                        pending.append(chunk)
                        continue
                    if chunk['start'] < start:
                        before = copy.deepcopy(chunk)
                        before.update(end=(datetime.date.fromisoformat(start) - datetime.timedelta(days=1)).isoformat(),
                                      endIsCoverageBoundary=True)
                        pending.append(before)
                    if chunk['end'] > end:
                        after = copy.deepcopy(chunk)
                        after.update(start=(datetime.date.fromisoformat(end) + datetime.timedelta(days=1)).isoformat(),
                                     startIsCoverageBoundary=True)
                        pending.append(after)
                chunks = pending
            kept.extend(chunks)
        country['leaders'] = kept
    for key, leader in additions:
        if leader['person'] in portraits:
            leader['portrait'] = copy.deepcopy(portraits[leader['person']])
        countries[key]['leaders'].append(leader)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Use a distinct output path; integration is an explicit later step.')
    incoming = json.loads(args.input.read_text(encoding='utf-8'))
    args.output.write_text(json.dumps(curate(incoming), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
