"""Focal 1920–1949 corrections; run after enrich-1920-authorities.py.

No network or media acquisition. Portraits are captured before removing this
script's own records. --input/--output support review on a disposable catalogue.
See docs/AUTHORITIES-1920-RESEARCH.md for scope, sources and unresolved dates.
"""
import argparse
import copy
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'curated-1920-0.11'
FIRST, LAST = '1920-01-01', '1949-12-31'


def adjacent(day, delta):
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=delta)).isoformat()


def curate(data):
    cs = data['countries']
    # Must precede removal: some portraits occur only in regenerated records.
    portraits = {l['person']: copy.deepcopy(l['portrait'])
                 for c in cs.values() for l in c['leaders'] if l.get('portrait')}
    for c in cs.values():
        c['leaders'] = [l for l in c['leaders'] if l.get('acquisition') != TAG]
    for key, qid, name in [
        ('RSR', 'Q2184', 'Rusia soviética · RSFSR'),
        ('ROC', 'Q13426199', 'República de China · etapa continental'),
        ('YKM', 'Q191077', 'Monarquía serbocroataeslovena / Reino de Yugoslavia'),
    ]:
        cs.setdefault(key, dict(flags=[], leaders=[]))
        cs[key].update(qid=qid, name=name)

    def cut(key, predicate, start=FIRST, end=LAST):
        """Remove only an explicitly reviewed interval, preserving both tails."""
        kept = []
        for old in cs[key]['leaders']:
            if not predicate(old) or old['end'] < start or old['start'] > end:
                kept.append(old)
                continue
            if old['start'] < start:
                before = copy.deepcopy(old)
                before.update(end=adjacent(start, -1), endIsCoverageBoundary=True)
                kept.append(before)
            if old['end'] > end:
                after = copy.deepcopy(old)
                after.update(start=adjacent(end, 1), startIsCoverageBoundary=True)
                kept.append(after)
        cs[key]['leaders'] = kept

    def person(key, q, start=FIRST, end=LAST, predicate=lambda l: True):
        cut(key, lambda l: l['person'] == q and predicate(l), start, end)

    def term(key, q, name, role, start, end, source, note='',
             start_coverage=False, end_coverage=False, precision=11):
        record = dict(person=q, name=name, role=role, start=start, end=end,
                      source=source, note=note, precision=precision,
                      curated=True, acquisition=TAG)
        if start_coverage:
            record['startIsCoverageBoundary'] = True
        if end_coverage:
            record['endIsCoverageBoundary'] = True
        if start_coverage or end_coverage:
            record['note'] += ' Los extremos señalados como cobertura delimitan esta revisión o entidad; no son nombramientos ni dimisiones.'
        if q in portraits:
            record['portrait'] = copy.deepcopy(portraits[q])
        cs[key]['leaders'].append(record)

    def clone_window(source, target, start, end, predicate=lambda l: True):
        """Copy evidence to a historical key; never invent additional terms."""
        existing = {(l['person'], l['role'], l['start'], l['end']) for l in cs[target]['leaders']}
        for old in list(cs[source]['leaders']):
            if not predicate(old) or old['start'] > end or old['end'] < start:
                continue
            new = copy.deepcopy(old)
            new.update(start=max(start, old['start']), end=min(end, old['end']), acquisition=TAG)
            signature = (new['person'], new['role'], new['start'], new['end'])
            if signature in existing:
                continue
            if new['start'] != old['start']:
                new['startIsCoverageBoundary'] = True
            if new['end'] != old['end']:
                new['endIsCoverageBoundary'] = True
            new['note'] = (new.get('note', '') + ' Copia documental a la clave histórica; no añade contraste independiente del mandato.').strip()
            cs[target]['leaders'].append(new)
            existing.add(signature)

    # China: preserve the acquired Beiyang series, then separate formal office
    # from military/party dominance. The PRC is not the 1920s republic.
    clone_window('TWN', 'ROC', FIRST, LAST)
    for key in ['ROC', 'TWN']:
        person(key, 'Q16574', '1943-08-01', LAST)
        person(key, 'Q20297', '1949-01-21', LAST)
    person('CHN', 'Q16574')
    post = 'https://subservices.post.gov.tw/post/internet/W_stamphouse/index_en.jsp?ID=2807&file_name=B110&stamp_cat_standard=Commemorative+Stamps&type=2805'
    person('ROC', 'Q705872')
    term('ROC', 'Q705872', 'Lin Sen', 'Presidente del Gobierno Nacional · jefatura formal del Estado', '1931-12-15', '1943-08-01', post,
         'Correos de la República de China acredita elección en1931 y fallecimiento el1/8/1943; el día inicial procede de la serie estructurada y sigue pendiente de acta.', precision=9)
    frus_chiang = 'https://history.state.gov/historicaldocuments/frus1943China/d288'
    for key in ['ROC', 'TWN']:
        term(key, 'Q16574', 'Chiang Kai-shek', 'Presidente del Gobierno Nacional en funciones', '1943-08-01', '1943-10-09', frus_chiang,
             'Tramo interino tras la muerte de Lin Sen; el juramento como titular se documenta el10/10. Inicio diario del interinato pendiente de decreto.', start_coverage=True)
        term(key, 'Q16574', 'Chiang Kai-shek', 'Presidente del Gobierno Nacional', '1943-10-10', '1948-05-19', frus_chiang,
             'El despacho diplomático describe el juramento del10/10/1943; distinto de la presidencia constitucional inaugurada en1948.')
        term(key, 'Q16574', 'Chiang Kai-shek', 'Presidente de la República de China', '1948-05-20', '1949-01-20', 'https://english.president.gov.tw/Page/83',
             'Se retira el21/1/1949; se conserva aparte la reanudación presidencial de1/3/1950.')
        term(key, 'Q20297', 'Li Zongren', 'Presidente de la República de China en funciones', '1949-01-21', LAST, 'https://english.president.gov.tw/Page/82',
             'Sustituye a Chiang, sin convertirse en dirigente de la República Popular. El cierre1949 sólo limita la ampliación.', end_coverage=True)
    person('CHN', 'Q5816', '1949-10-01', LAST, lambda l: 'Estado' in l['role'])
    term('CHN', 'Q5816', 'Mao Zedong', 'Presidente del Gobierno Popular Central · jefatura del Estado', '1949-10-01', LAST, 'https://english.scio.gov.cn/featured/chinakeywords/2022-07/13/content_78321957.htm',
         'Título institucional de1949, distinto de presidente de la República creado por la Constitución de1954 y de la dirección del partido.', end_coverage=True)

    # France: no president of the Republic from Vichy to Auriol; provisional
    # government chairs have their own office. Sources disagree on some days.
    elysee = 'https://www.elysee.fr/charles-de-gaulle'
    gallery = 'https://www.presidence-de-la-republique.fr/hist/10/ang/elysee/gale.html'
    for key in ['FRA', 'FRA-FREE']:
        person(key, 'Q2042', '1940-06-18', '1947-01-15')
        term(key, 'Q2042', 'Charles de Gaulle', 'Dirigente de la Francia Libre · autoridad rival', '1940-06-18', '1944-06-02', elysee,
             'La Francia Libre no es el régimen de Vichy; desde junio1943 se organiza mediante el CFLN. Su continuidad no implica controlar toda Francia.')
        term(key, 'Q2042', 'Charles de Gaulle', 'Presidente del Gobierno Provisional de la República Francesa', '1944-06-03', '1946-01-20', elysee,
             'Transformación del CFLN en GPRF el3/6/1944. La ficha parlamentaria comienza otra fase territorial el25/8; dimite el20/1/1946, antes del nombramiento de Gouin.')
    for key in ['FRA', 'FRA-VICHY']:
        person(key, 'Q5721', '1940-07-11', '1944-08-20')
        term(key, 'Q5721', 'Philippe Pétain', 'Jefe del Estado francés · régimen de Vichy', '1940-07-11', '1944-08-20', 'https://www.defense.gouv.fr/chemins-memoire/histoire-memoires/personnalites/personnalites-lettre-n-lettre-w/philippe-petain',
             'Gobierno autoritario colaboracionista. El traslado forzado a Alemania en agosto no convierte a de Gaulle en subordinado de Vichy; el extremo diario requiere cotejo del acta de traslado.', precision=10)
    person('FRA', 'Q381187', '1946-01-21', '1946-06-23')
    person('FRA', 'Q312026', '1946-06-24', '1946-12-15')
    term('FRA', 'Q381187', 'Félix Gouin', 'Presidente del Gobierno Provisional', '1946-01-27', '1946-06-23', gallery,
         'El archivo de la Presidencia da27/1; otras series distinguen elección26/1 y formación del gabinete. No es presidente de la República.')
    term('FRA', 'Q312026', 'Georges Bidault', 'Presidente del Gobierno Provisional', '1946-06-24', '1946-12-15', gallery,
         'Corrección del título genérico de presidente de la República. Final inclusivo previo al nombramiento de Blum del16/12, contrastado en la ficha parlamentaria; la galería antigua ofrece18/12.')
    person('FRA', 'Q18434', '1946-12-16', '1947-01-15')
    term('FRA', 'Q18434', 'Léon Blum', 'Presidente del Gobierno Provisional · jefatura del Estado', '1946-12-16', '1947-01-15', 'https://www.assemblee-nationale.fr/gouv_parl/fiches_personnalites/Blum.asp',
         'La jefatura del Estado termina al asumir Auriol el16/1; el Gobierno de Blum continúa hasta el22/1. Son funciones y extremos distintos.')

    # Spain: retain ESP for external administration; the republican map key
    # receives the same bounded documentary evidence, never Franco's mandate.
    person('ESP', 'Q18363')
    term('ESP', 'Q18363', 'Alfonso XIII', 'Rey de España · ejercicio de la jefatura del Estado', FIRST, '1931-04-13', 'https://www.congreso.es/en/cem/vidparl1931-11',
         'La transferencia del poder y salida de España son del14/4/1931; no se etiqueta ese hecho como abdicación dinástica.', start_coverage=True)
    person('ESP', 'Q313785')
    term('ESP', 'Q313785', 'Niceto Alcalá-Zamora', 'Presidente del Gobierno Provisional de la República', '1931-04-14', '1931-10-14', 'https://www.congreso.es/es/historico-diputados?_historicodiputados_mvcRenderCommandName=mostrarDetalle&_historicodiputados_nume=51194&p_p_id=historicodiputados&p_p_lifecycle=0&p_p_state=normal',
         'Jefatura provisional distinta de la presidencia constitucional de diciembre.')
    term('ESP', 'Q313785', 'Niceto Alcalá-Zamora', 'Presidente de la República', '1931-12-10', '1936-04-07', 'https://www.boe.es/gazeta/dias/1931/12/11/pdfs/GMD-1931-345.pdf',
         'Elección10/12, juramento11/12; destitución7/4/1936 publicada al día siguiente. No se extiende por defecto durante el interinato de Martínez Barrio.')
    person('ESP', 'Q203708', '1936-05-11', '1939-03-03')
    term('ESP', 'Q203708', 'Manuel Azaña', 'Presidente de la República', '1936-05-11', '1939-02-27', 'https://www.bne.es/es/autores/azana-manuel',
         'Dimisión firmada27/2/1939; aceptación parlamentaria3/3 y salida territorial5/2 son hechos distintos. Se conserva la fecha de firma empleada por el catálogo.')
    person('ESP', 'Q29179', '1936-10-01', '1939-03-31')
    clone_window('ESP', 'ESP-REPUBLIC', '1931-04-14', '1939-03-31', lambda l: l['person'] != 'Q29179')

    # Soviet Russia is not the USSR before the union treaty. The initial
    # government of the USSR is distinguished from the RSFSR government.
    term('RSR', 'Q1394', 'Vladímir Lenin', 'Presidente del Consejo de Comisarios del Pueblo de la RSFSR', FIRST, '1922-12-29', 'https://docs.historyrussia.org/ru/indexes/values/973636',
         'Cobertura de la Rusia soviética antes del tratado de30/12/1922; no fecha de cese personal en el cargo de la república rusa.', start_coverage=True, end_coverage=True)
    person('USSR', 'Q1394', '1922-12-30', '1924-01-21')
    term('USSR', 'Q1394', 'Vladímir Lenin', 'Presidente del Consejo de Comisarios del Pueblo de la URSS', '1923-07-06', '1924-01-21', 'https://www.wikidata.org/wiki/Q1394',
         'Consejo federal constituido en julio1923. No se retrotrae este cargo a la firma del tratado de diciembre1922; fecha de nombramiento pendiente de cotejo del acta original.')

    # Japan: official cabinet chronology agrees with acquired PM dates. Keep
    # those other cabinets; review the monarchs and decisive 1941/1945 changes.
    kantei = 'https://japan.kantei.go.jp/past_cabinet/index.html'
    person('JPN', 'Q157052')
    term('JPN', 'Q157052', 'Yoshihito · emperador Taishō', 'Emperador de Japón', FIRST, '1926-12-25', 'https://www.npb.go.jp/en/products/gazette/books/kanpo_history.html',
         'Cambio de era el25/12/1926; Hirohito ejerce la regencia desde1921 sin ser aún emperador.', start_coverage=True)
    person('JPN', 'Q34479', '1926-12-25', LAST)
    term('JPN', 'Q34479', 'Hirohito · emperador Shōwa', 'Emperador de Japón', '1926-12-25', LAST, 'https://f-showa.or.jp/museum/about_emperor_showa/',
         'Accede en1926; la ceremonia de entronización de1928 es un hecho distinto. La ocupación aliada posterior a1945 no suprime la institución imperial.', end_coverage=True)
    for q, name, start, end in [
        ('Q160847', 'Hideki Tōjō', '1941-10-18', '1944-07-22'),
        ('Q335198', 'Kantarō Suzuki', '1945-04-07', '1945-08-17'),
    ]:
        person('JPN', q)
        term('JPN', q, name, 'Primer ministro de Japón', start, end, kantei,
             'Fechas de la Oficina del Primer Ministro; no confundir jefe del Gobierno con emperador o comandante de ocupación.')

    # Italian crown survives the fall of Mussolini. The lieutenant is not king
    # until May1946; the provisional head of state is not president until1948.
    person('ITA', 'Q150642')
    term('ITA', 'Q150642', 'Víctor Manuel III', 'Rey de Italia · jefatura formal del Estado', FIRST, '1946-05-08', 'https://arch.iss.it/detail/IT-ISS-EACCPF0001-000033/vittorio-emanuele-iii-savoia',
         'Abdica el9/5/1946. Desde5/6/1944 las funciones reales se delegan en Humberto; la caída de Mussolini en1943 no elimina la monarquía.', start_coverage=True)
    person('ITA', 'Q187149')
    term('ITA', 'Q187149', 'Humberto de Saboya', 'Lugarteniente general del Reino · ejercicio de funciones reales', '1944-06-05', '1946-05-08', 'https://www.senato.it/node/85466/printable/print')
    term('ITA', 'Q187149', 'Humberto II', 'Rey de Italia', '1946-05-09', '1946-06-12', 'https://palazzo.quirinale.it/luoghi/pdf/it/sala-regno-italia.pdf',
         'De Gasperi ejerce las funciones de jefe del Estado desde13/6; referéndum2/6 y proclamación definitiva18/6 no son el mismo relevo.')
    person('ITA', 'Q23559', '1922-10-31', '1943-07-25')
    term('ITA', 'Q23559', 'Benito Mussolini', 'Jefe del Gobierno · dictadura fascista', '1922-10-31', '1943-07-25', 'https://www.senato.it/legislature/regno/italia/30/resoconti-elenco-cronologico',
         'La destitución del25/7/1943 se distingue de su posterior autoridad en la República Social Italiana, no proyectada sobre todo el Reino.')
    person('ITA', 'Q200085', '1943-07-25', '1944-06-17')
    term('ITA', 'Q200085', 'Pietro Badoglio', 'Jefe del Gobierno del Reino de Italia', '1943-07-25', '1944-06-17', 'https://archiviodistatotorino.beniculturali.it/pdf/Governo_alte-cariche_ecc_Sussidi_2a.pdf',
         'Nombrado25/7; ministros designados26/7. Dos gabinetes; Bonomi forma Gobierno18/6/1944. No acredita control del norte ocupado.')
    person('ITA', 'Q1245', '1946-07-01', '1948-05-11')
    term('ITA', 'Q1245', 'Enrico De Nicola', 'Jefe provisional del Estado', '1946-07-01', '1947-12-31', 'https://presidenti.quirinale.it/page/1/den-elezione.html',
         'Elegido28/6 y toma posesión1/7. Dimisión25/6/1947 y reelección26/6 requieren todavía separar las horas del relevo.')
    term('ITA', 'Q1245', 'Enrico De Nicola', 'Presidente de la República', '1948-01-01', '1948-05-11', 'https://presidenti.quirinale.it/page/1/den-elezione.html',
         'El título presidencial comienza con la Constitución el1/1/1948; Einaudi asume el12/5.')

    # Occupation administrations: documentary windows on the existing western
    # and eastern geometry, not an invented unified German national government.
    term('DEU', 'COLLECTIVE-DEU-ALLIED-OCCUPATION', 'Potencias aliadas · administraciones de ocupación', 'Autoridad de ocupación · zona occidental agrupada', '1945-06-05', '1949-09-20', 'https://digitallibrary.un.org/record/669294/files/E_CN.4_W.19-EN.pdf?ln=en',
         'La declaración de5/6 asume autoridad suprema sin anexión. El Consejo de Control deja de funcionar conjuntamente en1948; no se presenta una institución colegiada operativa durante toda la ventana. La Alta Comisión occidental inicia21/9/1949.', end_coverage=True)
    term('DDR', 'COLLECTIVE-DDR-SOVIET-OCCUPATION', 'Administración Militar Soviética en Alemania', 'Autoridad soviética de ocupación · zona oriental', '1945-06-09', '1949-10-06', 'https://www.berlin.de/landesdenkmalamt/denkmale/highlight-denkmale-der-alliierten/udssr/mitte/dienststelle-der-smad-648085.php',
         'Tramo anterior a la RDA. El límite6/10 separa la ficha estatal de7/10, no fecha de disolución de la administración militar soviética.', end_coverage=True)

    # Dominion constitutional offices do not become republican presidencies.
    term('IND', 'Q157068', 'Louis Mountbatten', 'Gobernador general de la India independiente · representante de la Corona', '1947-08-15', '1948-06-20', 'https://www.parliament.uk/about/living-heritage/evolutionofparliament/legislativescrutiny/parliament-and-empire/collections1/collections2/mountbatten-the-last-viceroy/',
         'Cargo de dominio independiente distinto del virreinato anterior. Nehru documenta la jura de Rajagopalachari el21/6/1948.')
    term('IND', 'Q378404', 'C. Rajagopalachari', 'Gobernador general de la India · representante de la Corona', '1948-06-21', LAST, 'https://nehruarchive.in/documents/to-lord-mountbatten-21-june-1948-nd5yl',
         'La carta del mismo día confirma su juramento; no se convierte en presidente de la República antes de26/1/1950.', end_coverage=True)
    term('PAK', 'Q160554', 'Muhammad Ali Jinnah', 'Gobernador general de Pakistán · representante de la Corona', '1947-08-15', '1948-09-11', 'https://na.gov.pk/en/print_list.php?type=governers',
         'La Asamblea distingue transferencia de poder14/8 y juramento15/8; no es presidente republicano ni primer ministro.')
    person('IDN', 'Q76127', '1945-08-18', LAST)
    term('IDN', 'Q76127', 'Sukarno', 'Presidente de Indonesia · República y transición federal', '1945-08-18', LAST, 'https://www.anri.go.id/publikasi/berita/menelusuri-jejak-konstitusi-indonesia-melalui-pameran-arsip',
         'Elegido el18/8, un día después de proclamar la independencia. El reconocimiento neerlandés27/12/1949 y el paso federal son hechos distintos. No es primer ministro durante todos estos años; Assaat representa la república constituyente, no la presidencia federal.', end_coverage=True)
    person('IDN', 'Q4808308', '1949-12-27', LAST)
    person('ISR', 'Q172183', '1948-05-16', LAST)
    term('ISR', 'Q172183', 'Jaim Weizmann', 'Presidente del Consejo Provisional del Estado', '1948-05-16', '1949-02-16', 'https://www.president.gov.il/institution/',
         'Cargo provisional creado tras la declaración de independencia, distinto de la presidencia constitucional.')
    term('ISR', 'Q172183', 'Jaim Weizmann', 'Presidente de Israel', '1949-02-17', LAST, 'https://pop.education.gov.il/tchumey_daat/moledet_hevra_ezrahut/yesodi/noseem_nilmadim/chaim-vaizman',
         'Jura17/2; la Knéset fecha la elección16/2. Se utiliza la toma de posesión, sin trasladar la presidencia al Mandato británico ni a Palestina entera.', end_coverage=True)

    term('GBR', 'Q269412', 'Jorge V', 'Rey del Reino Unido · jefatura del Estado', FIRST, '1936-01-20', 'https://api.parliament.uk/regnal-years/reigns', start_coverage=True)
    for q, name, start, end in [
        ('Q10664', 'Neville Chamberlain', '1937-05-28', '1940-05-10'),
        ('Q8016', 'Winston Churchill', '1940-05-10', '1945-07-26'),
        ('Q129006', 'Clement Attlee', '1945-07-26', LAST),
    ]:
        person('GBR', q)
        term('GBR', q, name, 'Primer ministro del Reino Unido', start, end, 'https://www.gov.uk/government/history/past-prime-ministers',
             'Se sustituyen rangos genéricos anuales incompatibles con el relevo documentado; los mandatos posteriores a1949 se conservan.', end_coverage=end == LAST)
    term('IRL', 'Q237951', 'Douglas Hyde', 'Presidente de Irlanda', '1938-06-25', '1945-06-24', 'https://president.ie/en/the-president/douglas-hyde',
         'Presidencia creada bajo la Constitución de1937. La proclamación republicana de1949 y las relaciones exteriores de la Corona son asuntos distintos.')

    # The monarchy must not inherit Tito's later socialist presidency.
    royal = 'https://royalfamily.org/dinasty/hm-king-alexander-i-of-yugoslavia/'
    term('YKM', 'Q211827', 'Pedro I', 'Rey de los serbios, croatas y eslovenos', FIRST, '1921-08-16', royal,
         'Alejandro ejerce la regencia antes de sucederlo; la denominación Yugoslavia se adopta en1929.', start_coverage=True)
    term('YKM', 'Q207384', 'Alejandro I', 'Rey de los serbios, croatas y eslovenos / Yugoslavia', '1921-08-16', '1934-10-09', 'https://muzej-jugoslavije.org/en/biography-of-king-alexander-i-karadjordjevic/',
         'Cambio de denominación estatal en1929, no sucesión personal; asesinado9/10/1934.')
    term('YKM', 'Q223183', 'Pedro II', 'Rey de Yugoslavia · menor bajo regencia; después en el exilio', '1934-10-09', '1944-12-31', 'https://kraljevskafondacija.rs/en/dynasty/his-majesty-king-peter-ii/',
         'Regencia hasta27/3/1941; en el exilio desde abril1941. La ventana termina1944 para separar la transición de1945, no por abdicación ni control efectivo nacional.', end_coverage=True)
    term('YKM', 'Q313128', 'Pablo de Yugoslavia', 'Primer regente · ejercicio colegiado de funciones reales', '1934-10-09', '1941-03-26', 'https://royalfamily.org/hrh-prince-paul-of-yugoslavia-regent-3/',
         'El consejo tenía tres miembros; no convertirlo en rey. Apartado por el golpe27/3/1941.')

    for c in cs.values():
        c['leaders'].sort(key=lambda l: (l['start'], l['name'], l['role']))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, default=ROOT / 'public/data/identities.json')
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    result = curate(json.loads(args.input.read_text(encoding='utf8')))
    output = args.output or args.input
    output.write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf8', newline='\n')
    print('Prepared', sum(l.get('acquisition') == TAG for c in result['countries'].values() for l in c['leaders']), 'focal/copied 1920–1949 records.')
