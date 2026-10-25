"""Pure, bounded European authority corrections for1880–1899.

No network or implicit output. See docs/AUTHORITIES-1880-EUROPE.md.
This supplements acquisition; it does not certify every cabinet or council.
"""
import argparse
import copy
import datetime
import json
import pathlib

FIRST, LAST = '1880-01-01', '1899-12-31'
TAG = 'curated-1880-europe-0.13'


def curate(incoming):
    data = copy.deepcopy(incoming)
    countries = data['countries']
    portraits = {leader['person']: copy.deepcopy(leader['portrait'])
                 for country in countries.values() for leader in country.get('leaders', [])
                 if leader.get('portrait')}
    for country in countries.values():
        country['leaders'] = [leader for leader in country.get('leaders', [])
                              if leader.get('acquisition') != TAG]
    for key, qid, name in [
        ('RUE', 'Q34266', 'Imperio ruso'),
        ('AUT-HUN', 'Q28513', 'Austria-Hungría'),
        ('SRK', 'Q241748', 'Reino de Serbia'),
        ('MNK', 'Q386496', 'Principado de Montenegro'),
    ]:
        country = countries.setdefault(key, dict(flags=[], leaders=[]))
        country.setdefault('qid', qid)
        country.setdefault('name', name)

    def cut(key, person, start, end):
        kept = []
        for old in countries[key]['leaders']:
            # A crossing term exercising authority in1900+ is immutable. The
            # resolver's curated priority chooses the bounded correction.
            if (old['person'] != person or old['end'] >= '1900-01-01'
                    or old['start'] > end or old['end'] < start):
                kept.append(old)
                continue
            if old['start'] < start:
                before = copy.deepcopy(old)
                before.update(end=(datetime.date.fromisoformat(start)
                                   - datetime.timedelta(days=1)).isoformat(),
                              endIsCoverageBoundary=True)
                kept.append(before)
            if old['end'] > end:
                after = copy.deepcopy(old)
                after.update(start=(datetime.date.fromisoformat(end)
                                    + datetime.timedelta(days=1)).isoformat(),
                             startIsCoverageBoundary=True)
                kept.append(after)
        countries[key]['leaders'] = kept

    def term(key, person, name, role, start, end, source, note='',
             start_coverage=False, end_coverage=False):
        if not (FIRST <= start <= end <= LAST):
            raise ValueError('European curation must remain within1880–1899')
        cut(key, person, start, end)
        record = dict(person=person, name=name, role=role, start=start, end=end,
                      source=source, note=note, precision=11, curated=True,
                      acquisition=TAG)
        if start_coverage:
            record['startIsCoverageBoundary'] = True
        if end_coverage:
            record['endIsCoverageBoundary'] = True
        if start_coverage or end_coverage:
            record['note'] += (' Los límites marcados como cobertura delimitan la ventana'
                               ' documental; no son nombramientos ni dimisiones.')
        if person in portraits:
            record['portrait'] = copy.deepcopy(portraits[person])
        countries[key]['leaders'].append(record)
        return record

    germany = 'https://www.dhm.de/lemo/bestand/objekt/tragbare-medaille-auf-das-dreikaiserjahr-1888'
    for q, name, start, end in [
        ('Q150652', 'Guillermo I', FIRST, '1888-03-09'),
        ('Q58600', 'Federico III', '1888-03-09', '1888-06-15'),
        ('Q2677', 'Guillermo II', '1888-06-15', LAST),
    ]:
        term('DEU', q, name, 'Emperador alemán · jefatura imperial', start, end, germany,
             'La sucesión por fallecimiento se distingue de una coronación;1888 tuvo tres emperadores.',
             start_coverage=start == FIRST, end_coverage=end == LAST)
    term('DEU', 'Q8442', 'Otto von Bismarck', 'Canciller del Imperio alemán',
         FIRST, '1890-03-20', 'https://www.dhm.de/lemo/biografie/otto-bismarck',
         'La solicitud de dimisión de18/3 se distingue de la destitución de20/3/1890.', start_coverage=True)
    chancellors = 'https://artsandculture.google.com/story/lQWRwGN7YRIA8A?hl=de'
    term('DEU', 'Q10873', 'Leo von Caprivi', 'Canciller del Imperio alemán',
         '1890-03-20', '1894-10-28', chancellors,
         'Serie de cancilleres de la exposición del Bundesarchiv. El relevo de octubre se fecha según esa serie; véase la nota documental sobre dimisión y nombramiento sucesor.')
    term('DEU', 'Q77166', 'Chlodwig zu Hohenlohe-Schillingsfürst', 'Canciller del Imperio alemán',
         '1894-10-29', LAST, chancellors, end_coverage=True)

    alexander_ii = 'https://igardens.ru/en/убийство-императора-александра-ii-и-ист/'
    term('RUE', 'Q83171', 'Alejandro II', 'Emperador de Rusia', FIRST, '1881-03-13', alexander_ii,
         'Asesinato13/3/1881 gregoriano,1/3 juliano. La ventana1880 no es el inicio del reinado de1855.', start_coverage=True)
    russia = 'https://guides.loc.gov/chronicling-america-czar-nicholas-ii'
    term('RUE', 'Q120180', 'Alejandro III', 'Emperador de Rusia',
         '1881-03-13', '1894-11-01', russia,
         'Fallecimiento1/11/1894 gregoriano,20/10 juliano. En el sigloXIX la diferencia entre calendarios era de12 días, no13.')
    term('RUE', 'Q40787', 'Nicolás II', 'Emperador de Rusia', '1894-11-01', LAST, russia,
         'Acceso por muerte del predecesor1/11/1894; coronación26/5/1896. No se confunde la coronación con el inicio del reinado.', end_coverage=True)

    spain = 'https://www.congreso.es/en/cem/regmariacristina'
    term('ESP', 'Q32347', 'Alfonso XII', 'Rey de España · monarquía constitucional',
         FIRST, '1885-11-25', 'https://www.congreso.es/en/cem/alfonsoxii', start_coverage=True)
    term('ESP', 'Q538125', 'María Cristina de Habsburgo-Lorena', 'Reina regente de España · ejercicio de la Corona',
         '1885-11-25', LAST, spain,
         'Asume la regencia al morir AlfonsoXII; juramento ante las Cortes30/12/1885. Después del nacimiento de AlfonsoXIII ejerce la Corona durante su minoría. No se introduce un reinado de María de las Mercedes.', end_coverage=True)
    term('ESP', 'Q18363', 'Alfonso XIII', 'Rey de España · menor de edad, bajo regencia',
         '1886-05-17', LAST, spain,
         'Rey desde su nacimiento; el ejercicio de funciones corresponde a la regente. La mayoría de edad de1902 queda fuera de esta ventana.', end_coverage=True)

    term('GBR', 'Q9439', 'Victoria', 'Reina del Reino Unido · jefatura de la Corona',
         FIRST, LAST, 'https://api.parliament.uk/regnal-years/reigns/6',
         'Reinado20/6/1837–22/1/1901; la monarca no sustituye al primer ministro ni dirige por sí sola el Gobierno.',
         start_coverage=True, end_coverage=True)

    # Presidents: use the presidency's chronology, rather than changing the
    # general cabinet acquisition series into an unsupported daily audit.
    for q, name, start, end, slug in [
        ('Q296083', 'Jules Grévy', FIRST, '1887-12-02', 'jules-grevy'),
        ('Q215778', 'Sadi Carnot', '1887-12-03', '1894-06-25', 'sadi-carnot'),
        ('Q315656', 'Jean Casimir-Perier', '1894-06-27', '1895-01-16', 'jean-casimir-perier'),
        ('Q296076', 'Félix Faure', '1895-01-17', '1899-02-16', 'felix-faure'),
        ('Q169502', 'Émile Loubet', '1899-02-18', LAST, 'emile-loubet'),
    ]:
        note = 'Presidencia de la Tercera República; el presidente del Consejo dirige el Gobierno.'
        if q == 'Q215778':
            note += ' Atentado24/6/1894 y muerte pasada medianoche25/6 son fechas diferentes, confirmadas por el acta y la Asamblea Nacional.'
        if q == 'Q315656':
            note += ' Se sigue la cronología del Elíseo: elección27/6/1894 y dimisión16/1/1895; existen tablas oficiales resumidas discrepantes.'
        term('FRA', q, name, 'Presidente de la República', start, end,
             'https://www.elysee.fr/' + slug, note,
             start_coverage=start == FIRST, end_coverage=end == LAST)
    term('FRA', 'Q358452', 'Pierre Waldeck-Rousseau', 'Presidente del Consejo de Ministros',
         '1899-06-22', LAST, 'https://www.elysee.fr/emile-loubet',
         'Gabinete de defensa republicana; su nombre de uso es Pierre, no el primer nombre civil René.', end_coverage=True)

    italy = 'https://palazzo.quirinale.it/luoghi/pdf/it/sala-regno-italia.pdf'
    term('ITA', 'Q153688', 'Umberto I', 'Rey de Italia · monarquía de Saboya', FIRST, LAST, italy,
         'Reinado iniciado en1878 y continuado hasta1900; el soberano se distingue del presidente del Consejo.',
         start_coverage=True, end_coverage=True)
    # These two premieres and the dated Senate records are independently
    # verified here. Other cabinets remain in the acquisition series.
    term('ITA', 'Q356711', 'Agostino Depretis', 'Presidente del Consejo de Ministros',
         '1885-06-29', '1887-07-29', 'https://www.senato.it/legislature/regno/italia/16/resoconti-elenco-cronologico',
         'GabinetesVII yVIII, con renovación4/4/1887 sin cambio de presidente del Consejo.')
    term('ITA', 'Q534227', 'Luigi Pelloux', 'Presidente del Consejo de Ministros',
         '1898-06-29', LAST, 'https://www.senato.it/legislature/regno/italia/20/resoconti-elenco-cronologico?session=1',
         'Primer gabinete29/6/1898–14/5/1899 y segundo desde14/5/1899. El acta del Senado30/6/1898 reproduce el decreto de nombramiento29/6.', end_coverage=True)

    habsburg = 'https://www.habsburger.net/de/personen/habsburger-herrscher/franz-joseph-i'
    term('AUT-HUN', 'Q51056', 'Francisco José I', 'Emperador de Austria y rey de Hungría · soberano común',
         FIRST, LAST, habsburg,
         'Monarquía dual: Austria y Hungría conservan gobiernos propios; no existió un primer ministro único de toda Austria-Hungría. La coronación húngara de1867 no reinicia el reinado austríaco de1848.',
         start_coverage=True, end_coverage=True)
    # Identified people already in the acquired corpus; preserve their images.
    # The paired governments are explicitly scoped to the respective half.
    term('HUN', 'Q254737', 'Kálmán Tisza', 'Primer ministro de Hungría · parte húngara de la monarquía dual',
         FIRST, '1890-03-13', 'https://mta.hu/data/dokumentumok/egyeb_dokumentumok/2025/Tisza_K%C3%A1lm%C3%A1n_KOI_MTA_2025.pdf',
         'Fin de su ejercicio personal13/3/1890; el repertorio del Archivo Nacional extiende la composición del gabinete hasta15/3. No se equiparan ambos hechos.', start_coverage=True)
    term('AUT-HUN', 'Q550748', 'Eduard Taaffe', 'Ministro presidente de Austria · parte cisleitana de la monarquía dual',
         FIRST, '1893-11-11', 'https://www.parlament.gv.at/recherchieren/personen/parlamentarierinnen-ab-1848/parlamentarier-1848-1918/taaffe',
         'Jefe del Gobierno de la mitad austríaca, no de toda la monarquía dual ni de la mitad húngara. Nombrado12/8/1879 y destituido11/11/1893.', start_coverage=True)
    term('AUT-HUN', 'Q254737', 'Kálmán Tisza', 'Primer ministro de Hungría · parte transleitana de la monarquía dual',
         FIRST, '1890-03-13', 'https://mta.hu/data/dokumentumok/egyeb_dokumentumok/2025/Tisza_K%C3%A1lm%C3%A1n_KOI_MTA_2025.pdf',
         'Jefe del Gobierno húngaro, distinto del Gobierno austríaco y de los ministerios comunes. La mitad húngara conserva su propia administración.', start_coverage=True)

    portugal = 'https://www.parquesdesintra.pt/media/upzl30vk/colecoesemfoco_pnsintra_ebook_2_lq.pdf'
    term('PRT', 'Q156175', 'Luis I', 'Rey de Portugal · monarquía constitucional', FIRST, '1889-10-19', portugal,
         'Fallece19/10/1889; no se confunde esta fecha con su cumpleaños31/10.', start_coverage=True)
    term('PRT', 'Q158874', 'Carlos I', 'Rey de Portugal · monarquía constitucional', '1889-10-19', LAST,
         'https://hemerotecadigital.cm-lisboa.pt/obras/ocidente/1908/N1048/N1048_master/N1048.pdf',
         'Sucesión19/10/1889; la aclamación28/12/1889 es un acto posterior.', end_coverage=True)
    term('BEL', 'Q12967', 'Leopoldo II', 'Rey de los belgas · monarquía constitucional', FIRST, LAST,
         'https://www.monarchie.be/en/royal-family/history/king-leopold-ii',
         'Jefatura de la monarquía belga; su soberanía personal sobre el Estado Independiente del Congo desde1885 es jurídicamente distinta de una colonia belga antes de1908.',
         start_coverage=True, end_coverage=True)

    dutch = 'https://www.koninklijkhuis.nl/onderwerpen/koninklijk-huis/geschiedenis/koningen-en-koninginnen/'
    term('NLD', 'Q125649', 'Guillermo III', 'Rey de los Países Bajos', FIRST, '1890-11-23',
         dutch + 'koning-willem-3-1849-1890', start_coverage=True)
    term('NLD', 'Q150747', 'Guillermina', 'Reina de los Países Bajos · bajo regencia hasta1898',
         '1890-11-23', LAST, dutch + 'koningin-wilhelmina-1890-1948',
         'Menor de edad hasta31/8/1898. La entronización ceremonial6/9/1898 no es el inicio del reinado.', end_coverage=True)
    term('NLD', 'Q57664', 'Emma de Waldeck-Pyrmont', 'Reina regente · incapacidad de Guillermo III',
         '1890-11-20', '1890-11-23', dutch + 'koningin-wilhelmina-1890-1948',
         'La Casa Real neerlandesa distingue esta breve regencia del marido de la posterior regencia de su hija.')
    term('NLD', 'Q57664', 'Emma de Waldeck-Pyrmont', 'Reina regente · minoría de Guillermina',
         '1890-12-08', '1898-08-31', dutch + 'koningin-wilhelmina-1890-1948',
         'Ventana de ejercicio publicada por la Casa Real neerlandesa. El intervalo desde la sucesión23/11 hasta8/12 requiere precisar investidura y ejercicio provisional; no se rellena por inferencia.')
    lux = 'https://monarchie.lu/fr/la-monarchie/lhistoire-de-la-dynastie-de-nassau'
    term('LUX', 'Q125649', 'Guillermo III', 'Gran duque de Luxemburgo · unión personal con los Países Bajos',
         FIRST, '1890-11-23', lux, start_coverage=True)
    for start, end in [('1889-04-08', '1889-05-03'), ('1890-11-04', '1890-11-23')]:
        term('LUX', 'Q57302', 'Adolfo de Nassau', 'Regente de Luxemburgo · incapacidad de Guillermo III', start, end,
             'https://sip.gouvernement.lu/dam-assets/publications/brochure-livre/minist-etat/sip/livre/famille_grand-ducale/La_famille_grand-ducale-FR.pdf',
             'Fechas jurídicas del decreto de regencia; los juramentos11/4/1889 y6/11/1890 no sustituyen el inicio legal.')
    term('LUX', 'Q57302', 'Adolfo de Nassau', 'Gran duque de Luxemburgo', '1890-11-23', LAST, lux,
         'Fin de la unión personal: GuillermoIII no es sucedido en Luxemburgo por Guillermina. Juramento9/12/1890, distinto de la sucesión23/11.', end_coverage=True)

    term('DNK', 'Q151305', 'Cristián IX', 'Rey de Dinamarca', FIRST, LAST,
         'https://www.kongehuset.dk/en/the-monarchy-in-denmark/the-royal-lineage/',
         'Reinado1863–1906; no se atribuye al monarca la jefatura cotidiana del gabinete.', start_coverage=True, end_coverage=True)
    term('SWE', 'Q52924', 'Óscar II', 'Rey de Suecia · unión personal con Noruega', FIRST, LAST,
         'https://www.kungahuset.se/english/royal-house/the-bernadotte-dynasty/oskar-ii',
         'Soberano desde1872; la unión personal no convierte Noruega en una provincia sueca.', start_coverage=True, end_coverage=True)
    term('NOR', 'Q52924', 'Óscar II', 'Rey de Noruega · unión personal con Suecia', FIRST, LAST,
         'https://www.regjeringen.no/en/the-government/previous-governments/historiske-artikler/offices/the-establishing-of-the-norwegian-state/norways-monarch-since-1814/id449228/',
         'Noruega conserva Constitución y Gobierno propios. La ruptura de1905 queda fuera de esta ventana.', start_coverage=True, end_coverage=True)

    term('GRC', 'Q17142', 'Jorge I', 'Rey de los helenos · monarquía constitucional', FIRST, LAST,
         'https://www.hellenicparliament.gr/Vouli-ton-Ellinon/To-Politevma/Syntagmatiki-Istoria',
         'Reinado1863–1913; desde1875 la confianza parlamentaria condiciona la formación de Gobierno.', start_coverage=True, end_coverage=True)
    romania = 'https://www.mnir.ro/carol-i/'
    term('ROU', 'Q57146', 'Carol I', 'Príncipe de Rumanía', FIRST, '1881-03-25', romania,
         'El Museo Nacional distingue14/26 de marzo1881: proclamación del reino en fecha gregoriana26/3.', start_coverage=True)
    term('ROU', 'Q57146', 'Carol I', 'Rey de Rumanía', '1881-03-26', LAST, romania,
         'La proclamación del reino se distingue de la coronación10/22 de mayo1881. No se trata de dos monarcas diferentes.', end_coverage=True)
    serbia = 'https://digitalna.nb.rs/attach/NBS/Periodika/SD_FFAB6B516AB99742A20B7C790616A239/1903/b001/output.pdf'
    term('SRK', 'Q313829', 'Milan Obrenović', 'Príncipe de Serbia', FIRST, '1882-03-05', serbia,
         'El Calendario del Estado serbio ofrece22/2/1882 juliano:6/3/1882 gregoriano para el cambio de rango.', start_coverage=True)
    term('SRK', 'Q313829', 'Milan I Obrenović', 'Rey de Serbia', '1882-03-06', '1889-03-06', serbia,
         'Abdica22/2/1889 juliano,6/3 gregoriano; la misma conversión de12 días se aplica al cambio de rango de1882.')
    term('SRK', 'Q297547', 'Alejandro I Obrenović', 'Rey de Serbia · bajo regencia hasta1893',
         '1889-03-06', LAST, serbia,
         'Menor bajo regencia hasta la proclamación anticipada de mayoría1/4/1893 juliano,13/4 gregoriano. La composición cambiante de la regencia se documenta como pendiente; no se asigna un retrato colectivo ficticio.', end_coverage=True)
    term('MNK', 'Q283255', 'Nicolás I Petrović-Njegoš', 'Príncipe de Montenegro', FIRST, LAST,
         'https://dacg.me/zvanicne-cestitke-nikoli-i-povodom-jubilarnih-svecanosti-1910-godine/',
         'Príncipe desde1860; el título de rey se adquiere en1910 y no se proyecta retrospectivamente.', start_coverage=True, end_coverage=True)

    bulgaria = "https://en.wikisource.org/wiki/Page:Statesman's_Year-Book_1913.djvu/820"
    for start, end in [(FIRST, '1886-08-20'), ('1886-08-29', '1886-09-07')]:
        term('BGR', 'Q159591', 'Alejandro I de Battenberg', 'Príncipe de Bulgaria', start, end, bulgaria,
             'Se interrumpe el ejercicio en el golpe de agosto1886; retorno17/8 juliano=29/8 gregoriano y abdicación definitiva26/8 juliano=7/9 gregoriano. El Museo de Sofía publica los días en calendario juliano; el anuario contemporáneo usa fechas gregorianas.',
             start_coverage=start == FIRST)
    term('BGR', 'Q313833', 'Stefan Stambolov', 'Miembro del Consejo de Regencia de Bulgaria',
         '1886-09-07', '1887-08-14', bulgaria,
         'Regencia colectiva tras la abdicación; no equivale a una presidencia personal. Los otros miembros y sus cambios requieren entradas individuales contrastadas; esta ficha no afirma enumerar el Consejo completo.')
    term('BGR', 'Q151667', 'Fernando I de Bulgaria', 'Príncipe de Bulgaria · ejercicio efectivo del Gobierno',
         '1887-08-14', LAST, bulgaria,
         'Elegido7/7/1887 gregoriano; asume el Gobierno14/8, distinto de la elección. Reconocimiento internacional en1896. No se anticipa a1887 el título de rey adquirido en1908.', end_coverage=True)

    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Use a distinct output path; integration is an explicit later step.')
    source = json.loads(args.input.read_text(encoding='utf-8'))
    args.output.write_text(json.dumps(curate(source), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
