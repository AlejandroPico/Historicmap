"""Bounded European monarchies and southern African authorities,1900–1919.

Pure curate(data), no network/media/manifest writes. See the accompanying
AUTHORITIES-1900-EUROPE-AFRICA research note before integration. This is a
focal correction, not a claim to have reconstructed every cabinet or governor.
"""
import argparse
import copy
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIRST, LAST = '1900-01-01', '1919-12-31'
TAG = 'curated-1900-europe-africa-0.12'


def curate(incoming):
    data = copy.deepcopy(incoming)
    cs = data['countries']
    portraits = {l['person']: copy.deepcopy(l['portrait'])
                 for c in cs.values() for l in c['leaders'] if l.get('portrait')}
    for c in cs.values():
        c['leaders'] = [l for l in c['leaders'] if l.get('acquisition') != TAG]
    for key, q, name in [
        ('SRK', 'Q241748', 'Reino de Serbia'),
        ('MNK', 'Q386496', 'Montenegro · principado y reino'),
        ('TRV', 'Q550374', 'República Sudafricana / Transvaal'),
        ('ORF', 'Q218023', 'Estado Libre de Orange / colonia del río Orange'),
    ]:
        cs.setdefault(key, dict(flags=[], leaders=[]))
        cs[key].update(qid=q, name=name)

    def cut(key, q, start, end):
        # Never touch a record continuing in1920+, even when it crosses this
        # interval. Annual curated priority resolves the bounded correction.
        kept = []
        for old in cs[key]['leaders']:
            if old['person'] != q or old['end'] >= '1920-01-01' or old['start'] > end or old['end'] < start:
                kept.append(old)
                continue
            if old['start'] < start:
                before = copy.deepcopy(old)
                before.update(end=(datetime.date.fromisoformat(start)-datetime.timedelta(days=1)).isoformat(), endIsCoverageBoundary=True)
                kept.append(before)
            if old['end'] > end:
                after = copy.deepcopy(old)
                after.update(start=(datetime.date.fromisoformat(end)+datetime.timedelta(days=1)).isoformat(), startIsCoverageBoundary=True)
                kept.append(after)
        cs[key]['leaders'] = kept

    def term(key, q, name, role, start, end, source, note='', start_coverage=False, end_coverage=False, precision=11):
        cut(key, q, start, end)
        record = dict(person=q, name=name, role=role, start=start, end=end,
                      source=source, note=note, precision=precision, curated=True, acquisition=TAG)
        if start_coverage:
            record['startIsCoverageBoundary'] = True
        if end_coverage:
            record['endIsCoverageBoundary'] = True
        if start_coverage or end_coverage:
            record['note'] += ' Los límites marcados como cobertura delimitan la ventana documental; no son nombramientos ni dimisiones.'
        if q in portraits:
            record['portrait'] = copy.deepcopy(portraits[q])
        cs[key]['leaders'].append(record)
        return record

    pt_archives = 'https://antt.dglab.gov.pt/exposicoes-virtuais-2/nascimento-do-rei-d-carlos-i/'
    term('PRT', 'Q158874', 'Carlos I', 'Rey de Portugal · monarquía constitucional',
         FIRST, '1908-02-01', pt_archives,
         'Reina desde1889; asesinado1/2/1908. La aclamación de diciembre1889 es distinta de la sucesión de octubre. No se atribuye el Gobierno cotidiano al monarca.', start_coverage=True)
    term('PRT', 'Q154308', 'Manuel II', 'Rey de Portugal · monarquía constitucional',
         '1908-02-01', '1910-10-05', 'https://ahm-exercito.defesa.gov.pt/details?id=254493',
         'Sucesión tras el regicidio; proclamación pública2/2 y aclamación parlamentaria6/5 son hechos distintos. El Archivo Histórico Militar fecha el fin con la proclamación republicana5/10/1910. Su exilio no prolonga el Gobierno monárquico.')

    italy = 'https://www.quirinale.it/allegati_statici/ebookapp/italiaunita.pdf'
    term('ITA', 'Q153688', 'Umberto I', 'Rey de Italia · monarquía de Saboya',
         FIRST, '1900-07-29', italy,
         'Asesinado en Monza29/7/1900. El comienzo de la ventana1900 no sustituye el acceso al trono de1878.', start_coverage=True)
    term('ITA', 'Q150642', 'Víctor Manuel III', 'Rey de Italia · monarquía de Saboya',
         '1900-07-29', LAST, italy,
         'Sucesor de UmbertoI; juramento parlamentario11/8/1900, distinto del comienzo sucesorio. El término continuó después de1919; no se añaden títulos imperiales adquiridos posteriormente.', end_coverage=True)

    serbia = 'https://nzhistory.govt.nz/war/kingdom-of-serbia-facts'
    term('SRK', 'Q297547', 'Alejandro I Obrenović', 'Rey de Serbia · dinastía Obrenović',
         FIRST, '1903-06-11', serbia,
         'Final de la dinastía en el golpe y asesinato de11/6gregoriano,29/5juliano. La elección y confirmación parlamentaria del sucesor se distinguen de ese cambio de poder.', start_coverage=True)
    term('SRK', 'Q211827', 'Pedro I Karađorđević', 'Rey de Serbia · dinastía Karađorđević',
         '1903-06-11', '1918-12-01', serbia,
         'Cronología del Ministerio de Cultura de NuevaZelanda. La confirmación por la Asamblea se fecha15/6 en el Ministerio de Defensa serbio. Desde1914 el príncipeAlejandro ejerce la regencia; el Gobierno y la corte siguen en el exilio durante la ocupación, sin atribuirles control intacto del territorio.')
    term('SRK', 'Q207384', 'Alejandro Karađorđević', 'Príncipe regente de Serbia · ejercicio de funciones reales',
         '1914-06-24', '1918-12-01', serbia,
         'Regencia por enfermedad de PedroI. El nuevo Reino de los Serbios,Croatas yEslovenos sucede a Serbia1/12/1918; no es una coronación del regente como rey.')

    montenegro = 'https://dacg.me/zvanicne-cestitke-nikoli-i-povodom-jubilarnih-svecanosti-1910-godine/'
    term('MNK', 'Q283255', 'Nicolás I Petrović-Njegoš', 'Príncipe de Montenegro',
         FIRST, '1910-08-27', montenegro,
         'Soberano desde1860. La proclamación del reino15/8juliano=28/8gregoriano cambia el rango de la misma persona, no su identidad.', start_coverage=True)
    term('MNK', 'Q283255', 'Nicolás I Petrović-Njegoš', 'Rey de Montenegro · después en el exilio',
         '1910-08-28', '1918-11-26', 'https://maticacrnogorska.me/wp-content/uploads/2016/07/Matica-br.-66.pdf',
         'La reproducción de las resoluciones de la Asamblea dePodgorica fecha26/11/1918 el destronamiento y unión conSerbia. Legitimidad controvertida y resistencia posterior: no equivale a consentimiento unánime ni a renuncia voluntaria. La monarquía estuvo exiliada desde la ocupación de1916.')

    british = 'https://api.parliament.uk/regnal-years/kingdoms/5'
    for q, name, start, end in [
        ('Q9439', 'Victoria', FIRST, '1901-01-22'),
        ('Q20875', 'Eduardo VII', '1901-01-22', '1910-05-06'),
        ('Q269412', 'Jorge V', '1910-05-06', LAST),
    ]:
        term('GBR', q, name, 'Soberano del Reino Unido · jefatura de la Corona',
             start, end, british,
             'Serie regnal oficial del Parlamento británico. La sucesión por muerte se distingue de la proclamación y de la coronación; la Corona no sustituye al primer ministro.',
             start_coverage=start == FIRST, end_coverage=end == LAST)
    term('ZAF', 'Q269412', 'Jorge V', 'Rey · jefatura formal de la Unión Sudafricana',
         '1910-05-31', LAST, british,
         'La Unión comienza31/5/1910, después del acceso al trono británico6/5. La monarquía se distingue de las funciones del gobernador general y del primer ministro. El límite1919 no termina el reinado.', start_coverage=True, end_coverage=True)
    term('ZAF', 'Q159397', 'Louis Botha', 'Primer ministro de la Unión Sudafricana',
         '1910-05-31', '1919-08-27', 'https://www.nationalarchives.gov.za/leaders-past-present',
         'Encargo de formar Gobierno21/5/1910 distinto de la entrada en vigor de la Unión31/5. Fallece27/8/1919; Smuts le sucede en septiembre. No se inventa un primer ministro para el intervalo intermedio no contrastado.')

    memoir = 'https://projekt-gutenberg.org/authors/paul-krueger/books/lebenserinnerungen-des-praesidenten-paul-krueger/chapter/14/?gl_reading_mode=1'
    term('TRV', 'Q244407', 'Paul Kruger', 'Presidente de la República Sudafricana · después representante en el exilio',
         FIRST, '1902-05-31', memoir,
         'Sus memorias reproducen la decisión del Consejo Ejecutivo10/9/1900: licencia para Europa y sustitución por el vicepresidenteBurger. Desde entonces no se le atribuye dirección presencial ni control de toda la república; las proclamaciones de anexión británicas y la resistencia coexistieron hasta la paz.', start_coverage=True)
    term('TRV', 'Q282482', 'Schalk Willem Burger', 'Vicepresidente y presidente interino · Gobierno bóer en campaña',
         '1900-09-10', '1902-05-31', memoir,
         'Decisión10/9 reproducida en las memorias deKruger; Ditsong fecha la partida física11/9. Es sustitución en el ejercicio, no dos presidentes con idéntico poder ni territorio bajo control íntegro. El tratado deVereeniging31/5/1902 pone fin a la resistencia gubernamental.')
    term('ORF', 'Q2355196', 'Marthinus Theunis Steyn', 'Presidente del Estado Libre de Orange · Gobierno en campaña',
         FIRST, '1902-05-15', 'https://www.dbnl.org/tekst/wet_004stri01_01/wet_004stri01_01_0038.php',
         'Las memorias deC.R.deWet documentan la presencia deSteyn enVereeniging15/5 y su enfermedad. La ventana se detiene en esa constatación; no se inventa una dimisión ese día ni se prolonga su ejercicio hasta la firma que él no realizó. El relevo final porDeWet queda pendiente de fecha diaria contrastada.', start_coverage=True, end_coverage=True)
    # External Crown after settlement: the cartographic source incorrectly
    # retains the republics as independent until1909. Root integration must also
    # correct metadata/administrative relations; these entries are not fronts.
    for key in ['TRV', 'ORF']:
        term(key, 'Q20875', 'Eduardo VII', 'Soberano británico · autoridad externa de la colonia',
             '1902-05-31', '1909-12-31', 'https://www.nam.ac.uk/explore/boer-war',
             'Vereeniging31/5/1902 reconoce la soberanía británica. La colonia continúa hasta la Unión de1910; la ventana cierra1909 por el ámbito de estos polígonos anuales, no por muerte ni fin del reinado. Los frentes militares1900–1902 no se reconstruyen a partir de este registro.', end_coverage=True)
    term('TRV', 'Q159397', 'Louis Botha', 'Primer ministro local · colonia británica del Transvaal',
         '1907-12-31', '1909-12-31', 'https://teara.govt.nz/en/photograph/33219/colonial-conference-1907',
         'Documentado como primer ministro delTransvaal en la ConferenciaColonial de1907 y enHansard4/6/1907. Se usa el cierre1907 como ventana de presencia acreditada; no como nombramiento. Gobierno responsable colonial distinto de independencia.', start_coverage=True, end_coverage=True)
    term('ORF', 'Q2821830', 'Abraham Fischer', 'Primer ministro local · colonia británica del río Orange',
         '1908-12-31', '1909-12-31', 'https://dspace.gipe.ac.in/xmlui/bitstream/handle/10973/18781/GIPE-007150-Contents.pdf?isAllowed=y&sequence=2',
         'Actas oficiales de la ConvenciónNacional1908–1909, lista de representantes y cargos. Su ejercicio comenzó en1907; la ventana interior no convierte el cierre1908 en nombramiento ni pretende fechar el primer gabinete.', start_coverage=True, end_coverage=True)

    for c in cs.values():
        c['leaders'].sort(key=lambda l: (l['start'], l['name'], l['role']))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, default=ROOT/'public/data/identities.json')
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    result = curate(json.loads(args.input.read_text(encoding='utf8')))
    (args.output or args.input).write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf8', newline='\n')
    print('Prepared', sum(l.get('acquisition') == TAG for c in result['countries'].values() for l in c['leaders']), 'European/southern African1900–1919 records.')
