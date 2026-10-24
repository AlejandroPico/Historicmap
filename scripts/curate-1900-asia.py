"""Bounded Asian authority review for 1900–1919; no network or media writes.

Run after curate-1900-authorities.py. See docs/AUTHORITIES-1900-ASIA.md.
The pure curate function preserves every flag and every term reaching 1920.
Coverage limits and documentary observations are not fabricated appointments.
"""
import argparse
import copy
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'curated-1900-asia-0.12'
FIRST, LAST = '1900-01-01', '1919-12-31'


def curate(incoming):
    data = copy.deepcopy(incoming)
    cs = data['countries']
    portraits = {l['person']: copy.deepcopy(l['portrait'])
                 for c in cs.values() for l in c['leaders'] if l.get('portrait')}
    for c in cs.values():
        c['leaders'] = [l for l in c['leaders'] if l.get('acquisition') != TAG]
    cs.setdefault('KEM', dict(qid='Q28233', name='Imperio de Corea', flags=[], leaders=[]))
    cs['KEM'].update(qid='Q28233', name='Imperio de Corea')

    def term(key, q, name, role, start, end, source, note='', precision=11,
             start_coverage=False, end_coverage=False, replace_generic=True):
        if replace_generic:
            # Crossing records are evidence for later years and stay identical.
            # The resolver gives this curated interval priority for that person.
            kept = []
            for old in cs[key]['leaders']:
                if not (old['person'] == q and not old.get('curated')
                        and old['start'] >= FIRST and old['end'] <= LAST
                        and old['start'] <= end and old['end'] >= start):
                    kept.append(old)
                    continue
                if old['start'] < start:
                    before = copy.deepcopy(old)
                    before.update(end=(datetime.date.fromisoformat(start) - datetime.timedelta(days=1)).isoformat(), endIsCoverageBoundary=True)
                    kept.append(before)
                if old['end'] > end:
                    after = copy.deepcopy(old)
                    after.update(start=(datetime.date.fromisoformat(end) + datetime.timedelta(days=1)).isoformat(), startIsCoverageBoundary=True)
                    kept.append(after)
            cs[key]['leaders'] = kept
        row = dict(person=q, name=name, role=role, start=start, end=end,
                   source=source, note=note, precision=precision, curated=True,
                   acquisition=TAG)
        if start_coverage:
            row['startIsCoverageBoundary'] = True
        if end_coverage:
            row['endIsCoverageBoundary'] = True
        if start_coverage or end_coverage:
            row['note'] += ' Los límites de cobertura delimitan el tramo documentado por esta revisión, no un nombramiento o una dimisión.'
        if q in portraits:
            row['portrait'] = copy.deepcopy(portraits[q])
        cs[key]['leaders'].append(row)

    # The January 1907 succession is secure; consulted catalogues disagree on
    # the day (3/8). Keep year precision rather than manufacturing a daily claim.
    iran = 'https://www.iranicaonline.org/articles/russia-iv-russians-at-the-court-of-mohammad-ali-shah/'
    term('IRN', 'Q467021', 'Mozaffar al-Din Shah Qajar', 'Shah de Persia · dinastía Qajar',
         FIRST, '1907-01-01', iran,
         'Reinado iniciado en1896; fallece y es sucedido en enero1907. Se conserva precisión anual ante la discrepancia del día en los repertorios consultados; el extremo normalizado no afirma muerte el1de enero.',
         precision=9, start_coverage=True, end_coverage=True)
    term('IRN', 'Q355603', 'Mohammad Ali Shah Qajar', 'Shah de Persia · dinastía Qajar',
         '1907-01-01', '1909-07-16',
         'https://www.iranicaonline.org/articles/ahmad-shah-qajar-1909-1925-the-seventh-and-last-ruler-of-the-qajar-dynasty/',
         'Sucede a su padre en enero1907; depuesto16/7/1909. Inicio normalizado a precisión anual, sin afirmar acceso el1de enero.',
         precision=9, start_coverage=True)
    term('IRN', 'Q317799', 'Ahmad Shah Qajar', 'Shah de Persia · monarca menor bajo regencia hasta1914',
         '1909-07-16', LAST,
         'https://www.iranicaonline.org/articles/ahmad-shah-qajar-1909-1925-the-seventh-and-last-ruler-of-the-qajar-dynasty/',
         'Proclamado16/7/1909; coronación y fin de la regencia21/7/1914. La continuidad de su reinado después de1919 conserva los registros posteriores existentes.', end_coverage=True)
    term('IRN', 'Q2646732', 'Ali Reza Khan Azod al-Molk', 'Regente de Persia · ejercicio durante la minoría de Ahmad Shah',
         '1909-07-16', '1910-09-23',
         'https://www.iranicaonline.org/articles/azod-al-molk-ali-reza/',
         'Elegido tras la deposición del padre de Ahmad; fallece23/9/1910. No se confunde su retrato de Kamal-ol-Molk con otra persona del mismo título.')
    term('IRN', 'Q322765', 'Abolqasem Naser ol-Molk', 'Regente de Persia · ejercicio durante la minoría de Ahmad Shah',
         '1911-03-31', '1914-07-20',
         'https://www.iranicaonline.org/articles/naser-al-molk-abul-qasem/',
         'Elegido tras la muerte de Azod en1910, pero sólo jura en marzo1911. La ventana empieza al cierre de ese mes, sin inventar el día del juramento; la elección y el ejercicio efectivo no son el mismo hito.', start_coverage=True)

    nepal_king = 'https://giwmscdntwo.gov.np/media/pdf_upload/ancient_nepal_151_full_1498631152_1593684369.pdf'
    term('NPL', 'Q886987', 'Prithvi Bir Bikram Shah', 'Rey de Nepal · jefatura formal bajo el Gobierno Rana',
         FIRST, '1911-12-11', nepal_king,
         'La inscripción original de su estatua transcrita por el Departamento de Arqueología fecha la muerte11/12/1911. La monarquía formal se distingue del poder gubernamental Rana.', start_coverage=True)
    term('NPL', 'Q381928', 'Tribhuvan', 'Rey de Nepal · jefatura formal bajo el Gobierno Rana',
         '1911-12-31', LAST, 'https://tile.loc.gov/storage-services/master/frd/copr/Nepal.pdf',
         'Reinado1911–1955. La ventana al cierre1911 no pretende fechar su acceso ni coronación. El poder efectivo del Gobierno Rana continuaba; la restauración de poder regio de1951 es posterior.',
         start_coverage=True, end_coverage=True)
    term('NPL', 'Q2267679', 'Dev Shumsher Jung Bahadur Rana', 'Primer ministro Rana · ejercicio efectivo del Gobierno',
         '1901-05-15', '1901-06-26', 'https://www.np.emb-japan.go.jp/100th/pic2.html',
         'Ventana interior de ejercicio documentado. Los repertorios discrepan entre marzo y mayo para el inicio; esta ficha no convierte15/5 en fecha contrastada de nombramiento. Chandra lo sustituye en junio.',
         start_coverage=True, end_coverage=True)
    term('NPL', 'Q1061786', 'Chandra Shumsher Jung Bahadur Rana', 'Primer ministro Rana · ejercicio efectivo del Gobierno',
         '1901-06-27', LAST, 'https://nepalica.hadw-bw.de/nepal/ontologies/viewitem/306',
         'Documenta Nepalica registra el mandato27/6/1901–26/11/1929. Se conserva el mandato posterior a1919 y no se atribuye a Chandra el título de rey.', end_coverage=True)

    korea = 'https://contents.history.go.kr/resources/common/pdf/A%20History%20of%20Korea_The%20Understanding%20Korea%20Series.pdf'
    term('KEM', 'Q257425', 'Gojong', 'Emperador de Corea · jefatura formal del Estado',
         FIRST, '1907-07-20', korea,
         'Abdicación forzada20/7/1907, distinta de la proclamación de sustitución del príncipe19/7. El protectorado impuesto en1905 limita su soberanía sin convertirlo aún en una colonia anexionada.', start_coverage=True)
    term('KEM', 'Q334111', 'Sunjong', 'Emperador de Corea · jefatura formal bajo protectorado japonés',
         '1907-07-20', '1910-08-28', korea,
         'Sucesión forzada en julio1907; ceremonia de entronización27/8 posterior. Firma del tratado22/8/1910 y promulgación de la anexión29/8 son hechos distintos. No se prolonga su autoridad estatal hasta su muerte1926.')

    term('TIB', 'Q25238', 'Thubten Gyatso · XIII Dalái Lama', 'Autoridad temporal y espiritual del Gobierno tibetano de facto',
         '1913-01-01', LAST, 'https://web.prm.ox.ac.uk/tibet/biography_336.html',
         'Volvió al Tíbet en1912 tras el exilio en la India; esta revisión cubre la entidad cartográfica desde1913. Gobierno de facto y soberanía internacional disputada son cuestiones distintas.',
         start_coverage=True, end_coverage=True)
    term('YMK', 'Q163945', 'Yahya Muhammad Hamid ed-Din', 'Imán del Yemen · autoridad temporal y religiosa',
         '1918-01-01', LAST, 'https://history.state.gov/historicaldocuments/frus1950v05/d755',
         'Imán desde1904, autoridad independiente tras la retirada otomana en1918. El comienzo es el límite anual de esta entidad cartográfica; no una proclamación fechada el1de enero ni el comienzo de su imamato. No se anticipa el título monárquico posterior.',
         precision=9, start_coverage=True, end_coverage=True)

    # A short rival succession must not disappear from the annual country card.
    # Documentary observation avoids falsely resolving the February 25/28
    # consolidation dispute into an unsupported daily appointment.
    afghan = 'https://islamansiklopedisi.org.tr/habibullah-han'
    term('AFG', 'Q31649', 'Abdur Rahman Khan', 'Emir de Afganistán · autoridad interna bajo restricción exterior británica',
         FIRST, '1901-10-01', afghan,
         'Gobernante1880–1901. La biografía institucional de su sucesor fecha la designación de éste28/9/1901 y la muerte del padre tres días después. La influencia británica sobre las relaciones exteriores no suprime la jefatura afgana.', start_coverage=True)
    term('AFG', 'Q334869', 'Habibullah Khan', 'Emir de Afganistán',
         '1901-10-01', '1919-02-20', afghan,
         'Designado heredero28/9/1901; sucede al padre tres días después según el estudio biográfico de Recep Uslu. Asesinado20/2/1919. La tutela exterior británica no lo convierte en un gobernador colonial ni borra su autoridad interna.')
    term('AFG', 'Q983049', 'Nasrullah Khan', 'Emir proclamado · autoridad rival en la sucesión afgana',
         '1919-02-27', '1919-02-27',
         'https://api.parliament.uk/historic-hansard/lords/1919/feb/27/the-late-amir-of-afghanistan',
         'Observación documental del27/2: el Gobierno británico informa al Parlamento de su proclamación tras la muerte de Habibullah. No fue un mandato de un solo día: el registro acota la evidencia consultada, sin fijar por ello todas las fechas de su disputa con Amanullah.',
         start_coverage=True, end_coverage=True)
    term('AFG', 'Q153620', 'Amanullah Khan', 'Emir de Afganistán · consolidación tras la sucesión disputada',
         '1919-03-01', LAST, 'https://oar.princeton.edu/bitstream/88435/pr1sr7w/1/afgh_barry2011.pdf',
         'Ventana desde la declaración de independencia del1/3, posterior a las proclamaciones rivales de febrero. El título de rey sólo se adopta en1926; la revisión no inventa un día de acceso entre las fechas discutidas de febrero.',
         start_coverage=True, end_coverage=True)

    # Remove only generic copies of the four reviewed northern presidents.
    # The full Xu1918–1922 assertion remains intact for later coverage.
    for q in ['Q210329', 'Q716136', 'Q700576', 'Q702428']:
        cs['ROC']['leaders'] = [l for l in cs['ROC']['leaders']
            if not (l['person'] == q and l['end'] <= LAST and l['role'] == 'Jefatura del Estado'
                    and (not l.get('curated') or l.get('acquisition') == 'curated-1900-0.12'))]
    term('ROC', 'Q210329', 'Yuan Shikai', 'Presidente de la República de China · Gobierno de Pekín',
         '1912-03-10', '1915-12-11', 'https://history.state.gov/historicaldocuments/frus1913/d89',
         'Investidura10/3/1912, distinta de su elección en febrero y de la presidencia constitucional posterior. La tentativa imperial de finales1915–1916 se distingue en otro registro.')
    term('ROC', 'Q210329', 'Yuan Shikai · Hongxian', 'Jefe del régimen de Pekín · tentativa de restauración imperial',
         '1915-12-12', '1916-03-22', 'https://history.state.gov/historicaldocuments/frus1916/d73',
         'Acepta la oferta del trono en diciembre1915 e inicia la era Hongxian en1916, sin coronación efectiva. La tentativa no restauró la dinastía Qing; anuncia su cancelación22/3, publicada23/3. El control provincial estaba fragmentado.')
    term('ROC', 'Q210329', 'Yuan Shikai', 'Presidente de la República de China · tras la cancelación de la monarquía',
         '1916-03-22', '1916-06-06', 'https://history.state.gov/historicaldocuments/frus1916/d71',
         'Anuncio de cancelación22/3; conserva la presidencia hasta su muerte6/6. La publicación al día siguiente no equivale a una nueva elección.')
    term('ROC', 'Q716136', 'Li Yuanhong', 'Presidente de la República de China · Gobierno de Pekín',
         '1916-06-07', '1917-07-01', 'https://history.state.gov/historicaldocuments/frus1916/d113',
         'Carta autógrafa de Li: asume las funciones7/6/1916, no6/6. La restauración manchú de julio1917 interrumpe su ejercicio; las pretensiones jurídicas posteriores no se convierten en control continuo.')
    term('ROC', 'Q700576', 'Feng Guozhang', 'Presidente interino de la República de China · Gobierno de Pekín',
         '1917-07-06', '1918-10-10', 'https://history.state.gov/historicaldocuments/frus1917/d121',
         'Notificación diplomática17/7 comunica ejercicio interino desde6/7, distinto de la llegada a Pekín/investidura de agosto. Se distingue la actuación inicial en Nankín del control efectivo de toda China.')
    term('ROC', 'Q702428', 'Xu Shichang', 'Presidente de la República de China · Gobierno de Pekín',
         '1918-10-10', LAST, 'https://history.state.gov/historicaldocuments/frus1918/d95',
         'Acceso10/10 confirmado por el telegrama presidencial contemporáneo. Su mandato continúa en1920–1922 sin modificación; no se confunde el Gobierno de Pekín con el Gobierno rival del sur.', end_coverage=True)

    # An annual1912 card includes the preceding Qing court without pretending
    # the child emperor or the dowager belonged to the republican government.
    for old in cs.get('QING', {}).get('leaders', []):
        if old['person'] in ['Q185152', 'Q1370907'] and old['start'] <= '1912-02-12' and old['end'] >= '1912-01-01':
            term('ROC', old['person'], old['name'], 'Autoridad predecesora · ' + old['role'],
                 '1912-01-01', '1912-02-12', old['source'],
                 'Corte Qing hasta la abdicación12/2/1912; no formó parte del Gobierno republicano. La ficha anual conserva las autoridades del cambio de entidad y la coexistencia inicial, sin enlazar este reinado con la restauración limitada de1917.',
                 start_coverage=True, replace_generic=False)

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
    print('Prepared', sum(l.get('acquisition') == TAG for c in result['countries'].values() for l in c['leaders']), 'Asian1900–1919 records.')
