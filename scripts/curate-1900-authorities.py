"""Focal imperial and revolutionary authorities,1900–1919, for0.12.

Pure curate(data): no network, files, media acquisition or manifest mutations.
CLI --input/--output is explicit. Read docs/AUTHORITIES-1900-RESEARCH.md before
integration. All dates below are Gregorian unless a note identifies the source
calendar. Documentary windows are not manufactured appointments or resignations.
"""
import argparse
import copy
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'curated-1900-0.12'
FIRST, LAST = '1900-01-01', '1919-12-31'


def adjacent(day, delta):
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=delta)).isoformat()


def curate(data):
    data = copy.deepcopy(data)
    cs = data['countries']
    # Capture before removing regenerated records, including sole references.
    portraits = {l['person']: copy.deepcopy(l['portrait'])
                 for c in cs.values() for l in c['leaders'] if l.get('portrait')}
    for c in cs.values():
        c['leaders'] = [l for l in c['leaders'] if l.get('acquisition') != TAG]
    for key, q, name in [
        ('RUE', 'Q34266', 'Imperio ruso'),
        ('RPR', 'Q139319', 'Gobierno Provisional / República Rusa'),
        ('AUT-HUN', 'Q28513', 'Austria-Hungría · monarquía dual'),
        ('OTT', 'Q12560', 'Imperio otomano'),
        ('QING', 'Q8733', 'Imperio de la dinastía Qing'),
    ]:
        cs.setdefault(key, dict(flags=[], leaders=[]))
        cs[key].update(qid=q, name=name)

    def replace(key, q, start=FIRST, end=LAST):
        """Bounded correction; records exercising in1920+ remain byte-identical.

        A surviving crossing generic term is superseded in the reviewed annual
        window by the resolver's curated priority, rather than mutilating its
        later evidence. Genuine later mandates and curations are never removed.
        """
        kept = []
        for old in cs[key]['leaders']:
            if old['person'] != q or old['end'] >= '1920-01-01' or old['start'] > end or old['end'] < start:
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

    def term(key, q, name, role, start, end, source, note='', precision=11,
             start_coverage=False, end_coverage=False):
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
        return record

    def clone(record, target, start, end, predecessor=False):
        new = copy.deepcopy(record)
        new.update(start=max(start, record['start']), end=min(end, record['end']), acquisition=TAG)
        if new['start'] > new['end']:
            return
        if new['start'] != record['start']:
            new['startIsCoverageBoundary'] = True
        if new['end'] != record['end']:
            new['endIsCoverageBoundary'] = True
        if predecessor:
            new['role'] = 'Autoridad predecesora · ' + record['role']
            new['note'] = (new.get('note', '') + ' No integró el Gobierno soviético; mostrado por haber ejercido durante el mismo año, antes del cambio de entidad.').strip()
        else:
            new['note'] = (new.get('note', '') + ' Copia documental con ámbito histórico explícito; no añade un contraste independiente del mandato.').strip()
        signature = (new['person'], new['role'], new['start'], new['end'])
        if not any((l['person'], l['role'], l['start'], l['end']) == signature for l in cs[target]['leaders']):
            cs[target]['leaders'].append(new)

    # Russian imperial, provisional and Soviet authorities remain distinct.
    # March/July/September/November conversions use Julian+13 days in1917.
    abdication = 'https://lenin.rusarchives.ru/fevralskaya-revolyuciya-v-rossii'
    replace('RUE', 'Q40787')
    nicholas = term('RUE', 'Q40787', 'Nicolás II', 'Emperador de Rusia · monarquía imperial',
        FIRST, '1917-03-15', abdication,
        'Acta original de abdicación2/3juliano=15/3gregoriano. El asesinato de1918 no es el final de su reinado. Miguel condicionó la aceptación del trono a una futura decisión constituyente; no se inventa un reinado efectivo posterior.', start_coverage=True)
    provisional = 'https://statearchive.ru/1016'
    replace('RPR', 'Q297032')
    lvov = term('RPR', 'Q297032', 'Gueorgui Lvov', 'Ministro-presidente del Gobierno Provisional de Rusia',
        '1917-03-15', '1917-07-20', provisional,
        'Gobierno Provisional desde2/3juliano. Dimisión7/7juliano y sucesión de Kerenski8/7juliano; la composición del gabinete cambia también el24/7juliano. Antes14/9gregoriano no se titula presidente de una república ya proclamada.')
    replace('RPR', 'Q48211')
    kerensky = term('RPR', 'Q48211', 'Aleksandr Kerenski', 'Ministro-presidente del Gobierno Provisional / República Rusa',
        '1917-07-21', '1917-11-07', 'https://www.prlib.ru/history/619540',
        'Comienza8/7juliano=21/7gregoriano. Proclamación republicana1/9juliano=14/9gregoriano. El Gobierno es derrocado25/10juliano=7/11gregoriano; no se confunde este hito con la constitución del Sovnarkom al día siguiente.')
    replace('RSR', 'Q1394', '1917-11-08', LAST)
    term('RSR', 'Q1394', 'Vladímir Lenin', 'Presidente del Consejo de Comisarios del Pueblo · Gobierno soviético ruso',
        '1917-11-08', LAST, 'https://lenin.rusarchives.ru/node/977',
        'Decreto de creación del Gobierno26/10juliano=8/11gregoriano, publicado27/10=9/11. La toma del poder y el nombramiento gubernamental son hechos distintos; la Constitución de la RSFSR es posterior. No acredita control de toda la guerra civil.', end_coverage=True)
    for record in [nicholas, lvov, kerensky]:
        clone(record, 'RSR', '1917-01-01', '1917-12-31', predecessor=True)

    # Dual monarchy: the shared sovereign is distinct from Austrian/Hungarian
    # governments. Charles relinquished participation, not dynastic rights.
    replace('AUT-HUN', 'Q51056')
    term('AUT-HUN', 'Q51056', 'Francisco José I', 'Emperador de Austria y rey de Hungría · soberano de la monarquía dual',
        FIRST, '1916-11-21', 'https://www.habsburger.net/en/persons/habsburg-emperor/franz-joseph-i',
        'Fallece21/11/1916; la monarquía dual no es una única cancillería nacional ni el Estado austríaco contemporáneo.', start_coverage=True)
    replace('AUT-HUN', 'Q51068')
    charles = term('AUT-HUN', 'Q51068', 'Carlos I de Austria / IV de Hungría', 'Emperador de Austria y rey de Hungría · soberano de la monarquía dual',
        '1916-11-21', '1918-11-11', 'https://www.parlament.gv.at/dokument/unterlagen/Stenographische_Protokolle_geheime__Sitzungen_Juli1918_gesamt.pdf',
        'Sucesión21/11/1916; coronación húngara30/12. Renuncia a participar en asuntos austríacos11/11/1918 y húngaros13/11. La disolución territorial de la monarquía no ocurrió toda en un único día y no se llama abdicación formal a estas declaraciones.')
    clone(charles, 'AUT', '1918-01-01', '1918-11-11')
    replace('HUN', 'Q51068', '1918-01-01', '1918-11-13')
    term('HUN', 'Q51068', 'Carlos IV', 'Rey de Hungría · ejercicio de funciones monárquicas',
        '1918-01-01', '1918-11-13', 'https://mnl.gov.hu/a_het_dokumentuma/iv_karoly_eckartsaui_nyilatkozata.html',
        'Declaración de Eckartsau13/11: abandona participación en asuntos del Estado, sin renuncia dinástica formal. La República se proclama16/11. El comienzo1918 es una ventana de la transición, no nuevo acceso al trono.', start_coverage=True)
    term('AUT', 'COLLECTIVE-AUT-STATE-COUNCIL-1918', 'Directorio del Consejo de Estado · presidencia colegiada',
        'Jefatura colegiada de Austria Alemana · Seitz, Dinghofer y Hauser', '1918-10-30', '1919-03-14',
        'https://www.archivinformationssystem.at/detail.aspx?ID=5464',
        'Órgano colegiado anterior a la jefatura individual de Seitz. El Consejo se suprime por ley14/3/1919; no se inventa una fotografía individual del órgano. La sucesión interna inicial Fink/Hauser sigue pendiente.', end_coverage=True)
    replace('AUT', 'Q11726', '1918-10-31', LAST)
    term('AUT', 'Q11726', 'Karl Renner', 'Canciller de Estado de Austria Alemana / Austria',
        '1918-10-31', LAST, 'https://austriaca.at/8403-4',
        'Juramento y primera sesión del gabinete31/10/1918; la designación política se fecha30/10 en el Landtag. Renovación gubernamental15/3/1919 distinta de una desaparición personal; no se altera su mandato de1920.', end_coverage=True)
    replace('HUN', 'Q346703', '1918-10-31', '1919-03-21')
    term('HUN', 'Q346703', 'Mihály Károlyi', 'Primer ministro de Hungría',
        '1918-10-31', '1919-01-10', 'https://mnl.gov.hu/mnl/tml/az_oszirozsas_forradalom_es_a_tanacskoztarsasag_tolna_megyeben',
        'Encargo31/10/1918 y formación ministerial1/11 son hechos distintos. Desde11/1/1919 pasa a jefatura provisional del Estado, no permanece primer ministro.')
    term('HUN', 'Q346703', 'Mihály Károlyi', 'Presidente provisional de la República de Hungría',
        '1919-01-11', '1919-03-21', 'https://mnl.gov.hu/mnl/tml/az_oszirozsas_forradalom_es_a_tanacskoztarsasag_tolna_megyeben',
        'Investido jefe provisional11/1; poder revolucionario21/3. Garbai y Kun, la ocupación y los gobiernos posteriores requieren su propio inventario y no se atribuyen automáticamente a Károlyi.')

    # Germany:9November proclamation,28November signed abdication, the council,
    # presidential election and cabinet appointments are separate events.
    replace('DEU', 'Q2677')
    term('DEU', 'Q2677', 'Guillermo II', 'Emperador alemán y rey de Prusia',
        FIRST, '1918-11-09', 'https://www.bundestag.de/dokumente/textarchiv/1918-11-09-revolutionskalender-38-091118-574088',
        'Cesa el ejercicio del poder en la revolución de9/11; anuncio de Max von Baden sin autorización del monarca. Firma de abdicación28/11 posterior; no se extiende el ejercicio hasta1941 por su muerte.', start_coverage=True)
    replace('DEU', 'Q76908', '1918-10-03', '1918-11-09')
    term('DEU', 'Q76908', 'Max von Baden', 'Canciller del Reich · último Gobierno imperial',
        '1918-10-03', '1918-11-09', 'https://www.dhm.de/lemo/biografie/max-baden',
        'Entrega la cancillería a Ebert9/11 sin base constitucional para esa transferencia. No es emperador ni presidente de la República.')
    term('DEU', 'COLLECTIVE-DEU-PEOPLES-DEPUTIES-1918', 'Consejo de Representantes del Pueblo',
        'Gobierno revolucionario colegiado · presidencia inicial de Ebert y Haase', '1918-11-10', '1919-02-12',
        'https://www.dhm.de/lemo/kapitel/weimarer-republik/revolution-191819/rat-der-volksbeauftragten',
        'Se forma10/11; SPD y USPD inicialmente paritarios. Los miembros de USPD abandonan el Consejo28/12/1918. La elección presidencial de Ebert11/2/1919 precede al gabinete Scheidemann13/2; no se inventa un presidente nacional individual para todo el periodo colegiado.')
    replace('DEU', 'Q70581', '1919-02-13', '1919-06-20')
    term('DEU', 'Q70581', 'Philipp Scheidemann', 'Presidente del Ministerio del Reich · jefatura del Gobierno',
        '1919-02-13', '1919-06-20', 'https://aktenreichskanzlei.bundesarchiv.de/',
        'Gobierno desde13/2; anuncio de dimisión19/6, crisis20/6 y nombramiento del sucesor21/6 se distinguen. Su proclamación de la República9/11/1918 no lo convirtió entonces en presidente del Reich.')
    replace('DEU', 'Q57159', '1919-06-21', LAST)
    term('DEU', 'Q57159', 'Gustav Bauer', 'Presidente del Ministerio del Reich; después canciller del Reich',
        '1919-06-21', LAST, 'https://weimar.bundesarchiv.de/WEIMAR/DE/Content/Dokumente-zur-Zeitgeschichte/1919-06-19_ruecktritt_scheidemann.html',
        'Nombramiento del gabinete21/6/1919; el título cambia con la Constitución en agosto. La curación no recorta su ejercicio posterior en1920.', end_coverage=True)

    # Ottoman sovereigns are distinct from the CUP government and the emerging
    # national representative movement. No1923 republican presidency in1919.
    ottoman_archive = 'https://www.devletarsivleri.gov.tr/yayinlar/45318a6a-b112-4d50-ac54-e820c07cde79.pdf'
    for q, name, start, end in [
        ('Q134817', 'Abdülhamid II', FIRST, '1909-04-26'),
        ('Q151494', 'Mehmed V Reşad', '1909-04-27', '1918-07-03'),
        ('Q162543', 'Mehmed VI Vahdeddin', '1918-07-04', '1922-11-01'),
    ]:
        replace('OTT', q)
        term('OTT', q, name, 'Sultán otomano · jefatura formal del Estado', start, end, ottoman_archive,
            'Guía de los Archivos Otomanos, cuadro de soberanos y grandes visires. La jefatura formal del sultán no equivale a todos los poderes del Comité de Unión y Progreso ni a control intacto de territorios ocupados.',
            start_coverage=start == FIRST, end_coverage=end == LAST)
        if q == 'Q162543':
            cs['OTT']['leaders'][-1]['note'] += ' Sultanato abolido por decisión parlamentaria1/11/1922, distinto de la dimisión del último gabinete4/11. Continuidad completa autorizada en esta nueva identidad; no modifica mandatos de TUR.'
            cs['OTT']['leaders'][-1]['source'] = 'https://www.ktb.gov.tr/TR-96329/1922.html'
    replace('OTT', 'Q315888', '1917-02-04', '1918-10-08')
    term('OTT', 'Q315888', 'Mehmed Talat Paşa', 'Gran visir · jefatura del Gobierno otomano',
        '1917-02-04', '1918-10-08', ottoman_archive,
        'Cuadro de grandes visires de la guía archivística,pp523–524. Cargo distinto del sultanato; las fechas de anuncio, dimisión y sustitución no siempre coinciden en otras compilaciones.')
    term('OTT', 'Q5152', 'Mustafa Kemal Paşa', 'Presidente del Comité Representativo · movimiento nacional rival',
        '1919-09-11', LAST, 'https://ata.msb.gov.tr/Sayfa/SayfaGoster/ataturk-kronolojisi',
        'Ventana desde el cierre del Congreso de Sivas: autoridad del movimiento de defensa nacional, distinta del Gobierno de Constantinopla. No se denomina presidente de Turquía antes de1923 ni presidente de la Asamblea antes de1920.',
        start_coverage=True, end_coverage=True)
    term('OTT', 'Q5152', 'Mustafa Kemal Paşa', 'Autoridad rival · presidente de la Gran Asamblea Nacional de Ankara',
        '1920-04-24', '1921-12-31', 'https://www.tbmm.gov.tr/baskan/meclis-baskanlari',
        'La Asamblea elige a Mustafa Kemal24/4/1920, al día siguiente de su apertura. Copia contextual para los años de coexistencia de Ankara y Constantinopla; no fue sultán ni miembro del Gobierno imperial. El cargo continuó hasta29/10/1923. No modifica los registros propios de TUR.', end_coverage=True)

    # Qing court: a reigning emperor, a dominant dowager, and a prince-regent
    # are different offices. The1917 restoration is local and short-lived.
    palace = 'https://www.dpm.org.cn/court/lineage/226255.html'
    replace('QING', 'Q299710')
    term('QING', 'Q299710', 'Guangxu', 'Emperador Qing · soberano nominal bajo tutela efectiva',
        FIRST, '1908-11-14', 'https://www.dpm.org.cn/classify_detail/180655.html',
        'El Museo del Palacio fecha la muerte14/11/1908. Después de1898 el poder efectivo de Cixi y el confinamiento del emperador se distinguen de su titularidad formal.', start_coverage=True)
    replace('QING', 'Q47842')
    term('QING', 'Q47842', 'Cixi', 'Emperatriz viuda · autoridad dominante de facto',
        FIRST, '1908-11-15', 'https://www.dpm.org.cn/classify_detail/180655.html',
        'Muere al día siguiente de Guangxu. No se la titula emperatriz reinante ni se oculta al emperador formal por identificar su poder efectivo.', start_coverage=True)
    replace('QING', 'Q185152', '1908-11-15', '1912-02-12')
    term('QING', 'Q185152', 'Puyi · emperador Xuantong', 'Emperador Qing · monarca menor bajo regencia',
        '1908-11-15', '1912-02-12', palace,
        'Designación y sucesión en noviembre1908 distintas de la ceremonia de entronización2/12 y del comienzo de la era Xuantong en1909. La abdicación12/2/1912 no termina por sí sola todos los privilegios cortesanos.')
    replace('QING', 'Q144348', '1908-12-02', '1911-12-06')
    term('QING', 'Q144348', 'Zaifeng · príncipe Chun', 'Príncipe regente · ejercicio del Gobierno durante la minoría de Puyi',
        '1908-12-02', '1911-12-06', 'https://img.dpm.org.cn/Uploads/pdf/2824/T00024_00.pdf',
        'Ventana de ejercicio desde la ceremonia de diciembre; la designación regencial se hizo antes de la muerte de Cixi. El estudio del Museo del Palacio fecha la renuncia6/12/1911.', start_coverage=True)
    replace('QING', 'Q1370907', '1911-12-07', '1912-02-12')
    term('QING', 'Q1370907', 'Longyu', 'Emperatriz viuda · autoridad cortesana en la abdicación del monarca menor',
        '1911-12-07', '1912-02-12', 'https://www.dpm.org.cn/Uploads/pdf/6156/T00199_00.pdf',
        'Ventana posterior al retiro de Zaifeng. Promulga la abdicación en nombre de Puyi12/2/1912; no se inventa una coronación ni un nuevo título de emperatriz reinante.', start_coverage=True)
    term('QING', 'Q185152', 'Puyi · emperador Xuantong', 'Emperador restaurado en Pekín · autoridad rival de alcance limitado',
        '1917-07-01', '1917-07-12', 'https://history.state.gov/historicaldocuments/frus1917/d128',
        'Restauración de Zhang Xun documentada por despacho contemporáneo y edictos. No se extiende a toda China ni se enlaza como reinado continuo con1912 o Manchukuo.')

    # Reuse the acquired northern republican series without inheriting PRC
    # authorities. Keep1920+source records untouched, including Xu's full term.
    for old in list(cs['TWN']['leaders']):
        if old['start'] <= LAST and old['end'] >= '1912-01-01':
            clone(old, 'ROC', '1912-01-01', LAST)
    replace('ROC', 'Q8573', '1912-01-01', '1912-03-09')
    term('ROC', 'Q8573', 'Sun Yat-sen', 'Presidente provisional de la República de China · Gobierno de Nankín',
        '1912-01-01', '1912-03-09', 'https://history.state.gov/historicaldocuments/frus1913/d89',
        'Elegido29/12/1911 e investido1/1/1912. Su dimisión se hace efectiva al jurar Yuan en Pekín10/3; las autoridades Qing todavía coexistieron hasta la abdicación de febrero.')
    replace('ROC', 'Q210329', '1912-03-10', '1916-06-06')
    term('ROC', 'Q210329', 'Yuan Shikai', 'Presidente de la República de China; promotor de la monarquía Hongxian',
        '1912-03-10', '1916-06-06', 'https://history.state.gov/historicaldocuments/frus1916/d73',
        'Juramento10/3/1912 acreditado en FRUS1913/d89. El proyecto imperial de1915–1916 se declara aparte en esta nota: acepta la propuesta monárquica en diciembre1915 y cancela sus preparativos22/3/1916. No se inventa una coronación consumada ni se trata como restauración Qing. Falta separar con actas toda la transición de títulos.')
    # Feng's assumption is already reported by July9–12, before the later
    # Beijing ceremony and the generic July17 assertion. Avoid false precision.
    replace('ROC', 'Q700576', '1917-07-01', '1918-10-10')
    term('ROC', 'Q700576', 'Feng Guozhang', 'Presidente interino de la República de China · Gobierno septentrional',
        '1917-07-12', '1918-10-09', 'https://history.state.gov/historicaldocuments/frus1917/papers',
        'El índice diplomático registra confirmación9/7 y ejercicio presidencial12/7; la ceremonia de Pekín fue posterior. Inicio como ventana ya documentada, no afirmación de investidura ese día. El reconocimiento por el sur no fue uniforme.', start_coverage=True)
    # The restoration remains visible in the annual1917 republican card, with
    # its own scope rather than as a country-wide change of every boundary.
    restoration = next(l for l in cs['QING']['leaders'] if l.get('acquisition') == TAG and l['person'] == 'Q185152' and l['start'] == '1917-07-01')
    clone(restoration, 'ROC', '1917-07-01', '1917-07-12')

    # Japan's acquired cabinet list is retained. Distinguish sovereign access
    # from era names and later enthronement ceremonies.
    replace('JPN', 'Q174231', FIRST, '1912-07-30')
    term('JPN', 'Q174231', 'Mutsuhito · emperador Meiji', 'Emperador de Japón',
        FIRST, '1912-07-30', 'https://www.npb.go.jp/en/products/gazette/books/kanpo_history.html',
        'Muerte y cambio a la era Taishō30/7/1912; no se trata al primer ministro como monarca.', start_coverage=True)
    replace('JPN', 'Q157052', '1912-07-30', LAST)
    term('JPN', 'Q157052', 'Yoshihito · emperador Taishō', 'Emperador de Japón',
        '1912-07-30', LAST, 'https://www.npb.go.jp/en/products/gazette/books/kanpo_history.html',
        'Sucesión1912 y ceremonia1915 son hitos distintos; la regencia de Hirohito no comienza hasta1921. Se conservan íntegros los registros de1920 en adelante.', end_coverage=True)

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
    print('Prepared', sum(l.get('acquisition') == TAG for c in result['countries'].values() for l in c['leaders']), 'focal/copied1900–1919 records.')
