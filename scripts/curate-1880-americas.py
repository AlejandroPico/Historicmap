"""Bounded, sourced American authority corrections, 1880–1899.

Pure curate(data), with no network or file writes. Explicit CLI input/output.
Sources, uncertain transitions and map integration: docs/AUTHORITIES-1880-AMERICAS.md.
"""
import argparse
import copy
import datetime
import json
import pathlib

TAG = 'curated-1880-americas-0.13'
FIRST, LAST = '1880-01-01', '1899-12-31'
MAPA = 'https://mapa.an.gov.br/index.php/assuntos/79-producao/80-cronologia/509-periodo-imperial-1822-a-1889'
BRA = 'https://www.biblioteca.presidencia.gov.br/presidencia/ex-presidentes/'
ARG = 'https://www.bna.com.ar/Downloads/Aniversario_BNA_125.pdf'
CHL = 'https://www.bcn.cl/historiapolitica/presidentes_de_la_republica/index.html'
PER = 'https://www3.congreso.gob.pe/biblioteca/presidentes/1850-1900'
URY = 'https://www.embajadadeuruguay.org/pages/acerca-de-uruguay/sistema-de-gobierno.php'
CRI = 'https://www.presidencia.go.cr/expresidencias'
DOM = 'https://catalogo.academiadominicanahistoria.org.do/opac-tmpl/files/ppcodice/Clio-1948-016-082-097-105.pdf'

# Country, person identifier, name, office, first/last included day, source,
# date precision, coverage-only start/end, factual note. Coverage is not accession.
ROWS = [
 ('BRA-EMPIRE','Q156774','Pedro II','Emperador de Brasil','1880-01-01','1889-11-14','https://bndigital.bn.gov.br/dossies/periodicos-literatura/personagens-periodicos-literatura/dom-pedro-ii/',11,True,False,'Titular de la Corona durante el periodo; la regencia por ausencia se registra aparte. La proclamación republicana del15/11/1889 pone fin al Imperio.'),
 ('BRA-EMPIRE','Q464449','Isabel de Brasil','Princesa imperial · regente en ausencia del emperador','1887-07-01','1888-07-31','https://brasilianafotografica.bn.gov.br/?paged=2&tag=princesa-isabel',10,True,True,'Ventana interior de la tercera regencia, junio1887–agosto1888. La prensa de1889 y la revista institucional difieren en el cierre21/22 de agosto; esta ventana no decide entre esas fechas.'),
 ('BRA-EMPIRE','Q1791206','João Lins Vieira Cansanção de Sinimbu','Presidente del Consejo de Ministros del Imperio','1880-01-01','1880-03-27',MAPA,11,True,False,'Gabinete iniciado en1878. Se distingue la dirección ministerial de la titularidad imperial.'),
 ('BRA-EMPIRE','Q1791287','José Antônio Saraiva','Presidente del Consejo de Ministros del Imperio','1880-03-28','1882-01-20',MAPA,11,False,False,'Primer gabinete de Saraiva en esta revisión.'),
 ('BRA-EMPIRE','Q1797172','Martinho Álvares da Silva Campos','Presidente del Consejo de Ministros del Imperio','1882-01-21','1882-07-02',MAPA,11,False,False,'Gabinete distinto del posterior gabinete Paranaguá.'),
 ('BRA-EMPIRE','Q1791210','João Lustosa da Cunha Paranaguá','Presidente del Consejo de Ministros del Imperio','1882-07-03','1883-05-23',MAPA,11,False,False,'Gabinete Paranaguá.'),
 ('BRA-EMPIRE','Q1791397','Lafayette Rodrigues Pereira','Presidente del Consejo de Ministros del Imperio','1883-05-24','1884-06-05',MAPA,11,False,False,'Gabinete Lafayette.'),
 ('BRA-EMPIRE','Q1797496','Manuel Pinto de Sousa Dantas','Presidente del Consejo de Ministros del Imperio','1884-06-06','1885-05-05',MAPA,11,False,False,'Gabinete Dantas.'),
 ('BRA-EMPIRE','Q1791287','José Antônio Saraiva','Presidente del Consejo de Ministros del Imperio','1885-05-06','1885-08-19',MAPA,11,False,False,'Segundo gabinete; no se fusiona con su ejercicio1880–1882.'),
 ('BRA-EMPIRE','Q1791225','João Maurício Wanderley, barón de Cotegipe','Presidente del Consejo de Ministros del Imperio','1885-08-20','1888-03-09',MAPA,11,False,False,'Gabinete Cotegipe.'),
 ('BRA-EMPIRE','Q1791187','João Alfredo Correia de Oliveira','Presidente del Consejo de Ministros del Imperio','1888-03-10','1889-06-06',MAPA,11,False,False,'Gabinete João Alfredo; no equivale a la regencia de Isabel.'),
 ('BRA-EMPIRE','Q932350','Afonso Celso de Assis Figueiredo, vizconde de Ouro Preto','Presidente del Consejo de Ministros del Imperio','1889-06-07','1889-11-14',MAPA,11,False,False,'Último gabinete imperial, depuesto con el fin del régimen el15/11/1889.'),
 ('BRA','Q200812','Deodoro da Fonseca','Jefe del Gobierno provisional republicano','1889-11-15','1891-02-24','https://mapa.an.gov.br/index.php/dicionario-primeira-republica/1661-presidente-presidencia-da-republica-1889-1930',11,False,False,'La jefatura provisional precede a la presidencia constitucional; no es una continuidad de la Corona.'),
 ('BRA','Q200812','Deodoro da Fonseca','Presidente constitucional de la República','1891-02-25','1891-11-22','https://atom-museurepublica.museus.gov.br/index.php/actor/browse?entityType=132&page=1&sort=lastUpdated&sortDir=desc',11,False,False,'Tras la fase provisional y la elección constitucional; renuncia23/11/1891. Extremo inclusivo anterior a la sucesión de Floriano.'),
 ('BRA','Q238688','Floriano Peixoto','Vicepresidente en ejercicio de la Presidencia de la República','1891-11-23','1894-11-14',BRA+'floriano-peixoto',11,False,False,'Sucede a Deodoro tras su renuncia; completa el periodo hasta el relevo de1894.'),
 ('BRA','Q310230','Prudente de Morais','Presidente de la República · titular','1894-11-15','1898-11-14','https://www.gov.br/secretariageral/pt-br/centrais-de-conteudo/biblioteca-da-pr/galeria-dos-ex-presidentes/prudente/biografia-completa',11,False,False,'Titularidad presidencial. La licencia de noviembre1896 a marzo1897 no se oculta: se incorpora aparte al vicepresidente en ejercicio.'),
 ('BRA','Q771263','Manuel Vitorino','Vicepresidente · encargado de la Presidencia','1896-12-01','1897-02-28','https://www25.senado.leg.br/web/atividade/pronunciamentos/-/p/pronunciamento/328033',10,True,True,'Ventana interior de la suplencia durante la enfermedad de Prudente. La fuente senatorial sitúa el traspaso11/11; otras cronologías usan10/11. Prudente retoma el ejercicio4/3/1897; no se inventan aquí los días discutidos.'),
 ('BRA','Q382919','Campos Sales','Presidente de la República','1898-11-15','1899-12-31',BRA+'campos-salles',11,False,True,'Mandato iniciado15/11/1898 y continuado en1902; el corte1899 es solamente cobertura de esta ampliación.'),
 ('ARG','Q441371','Nicolás Avellaneda','Presidente de la Nación','1880-01-01','1880-10-11',ARG,11,True,False,'Última parte del mandato iniciado1874; fecha de relevo12/10/1880.'),
 ('ARG','Q356659','Julio Argentino Roca','Presidente de la Nación · primer mandato','1880-10-12','1886-10-11',ARG,11,False,False,'Primer mandato, separado de la presidencia iniciada1898.'),
 ('ARG','Q438892','Miguel Juárez Celman','Presidente de la Nación','1886-10-12','1890-08-05',ARG,11,False,False,'Renuncia6/8/1890, después de la Revolución del Parque; el relevo se registra ese día.'),
 ('ARG','Q270446','Carlos Pellegrini','Vicepresidente en ejercicio de la Presidencia de la Nación','1890-08-06','1892-10-11',ARG,11,False,False,'Sucesión tras la renuncia de Juárez Celman, hasta el relevo constitucional.'),
 ('ARG','Q455709','Luis Sáenz Peña','Presidente de la Nación','1892-10-12','1895-01-22',ARG,11,False,False,'La cronología del Banco de la Nación fecha el traspaso a Uriburu23/1/1895.'),
 ('ARG','Q270348','José Evaristo Uriburu','Vicepresidente en ejercicio de la Presidencia de la Nación','1895-01-23','1898-10-11',ARG,11,False,False,'Completa el periodo presidencial tras la renuncia de Luis Sáenz Peña.'),
 ('ARG','Q356659','Julio Argentino Roca','Presidente de la Nación · segundo mandato','1898-10-12','1899-12-31',ARG,11,False,True,'Segundo mandato, continuado hasta1904; no se confunde con su primer mandato.'),
 ('MEX','Q380975','Manuel González Flores','Presidente constitucional de México','1880-12-01','1884-11-30','https://cdigital.cabu.uanl.mx/fpm/33/1020132543/1020132543_019.pdf',11,False,False,'El compendio histórico digitalizado por la Universidad Autónoma de Nuevo León fecha expresamente el mandato; no es una suplencia de Díaz.'),
 ('MEX','Q150688','Porfirio Díaz','Presidente constitucional de México · segundo mandato','1884-12-01','1888-11-30','https://www.amabpac.org.mx/wp/wp-content/uploads/2023/06/Memorias-del-Congreso-Morelos-y-Diaz.pdf',11,False,False,'La investigación archivística reproduce la protesta del1/12/1884 ante el Congreso. El periodo posterior se registra aparte.'),
 ('MEX','Q150688','Porfirio Díaz','Presidente de México · mandatos sucesivos del Porfiriato','1888-12-01','1899-12-31','https://libros.colmex.mx/wp-content/plugins/documentos/descargas/nhmi.pdf',11,False,True,'Reelecciones para1888–1892,1892–1896 y1896–1900. Continuidad personal no significa un único mandato constitucional; el corte1899 es cobertura.'),
 ('CHL','Q1324','Aníbal Pinto','Presidente de la República','1880-01-01','1881-09-17',CHL,11,True,False,'Última parte del mandato iniciado1876; presidencia durante la Guerra del Pacífico.'),
 ('CHL','Q1323','Domingo Santa María','Presidente de la República','1881-09-18','1886-09-17',CHL,11,False,False,'Relevo constitucional; no confundir con la fecha de final de las operaciones militares.'),
 ('CHL','Q1322','José Manuel Balmaceda','Presidente de la República · Ejecutivo en la guerra civil','1886-09-18','1891-08-28',CHL,11,False,False,'En1891 el Ejecutivo compite con la Junta congresista. Entrega el mando29/8; su muerte posterior no prolonga el ejercicio presidencial.'),
 ('CHL','Q880764','Manuel Baquedano','General · encargado provisional del Gobierno','1891-08-29','1891-08-30','https://obtienearchivo.bcn.cl/obtienearchivo?id=documentos%2F10221.1%2F21834%2F1%2F215158.pdf&origen=BDigital',11,False,False,'Proclamación original de29/8/1891. Interregno hasta la entrada de la Junta; no mandato presidencial electivo.'),
 ('CHL','Q1320','Jorge Montt','Presidente de la Junta de Gobierno congresista','1891-04-12','1891-12-25','https://www.memoriachilena.gob.cl/archivos2/pdfs/MC0014668.pdf',11,False,False,'Junta rival del Ejecutivo desde12/4/1891; después de la victoria y la entrada a Santiago31/8, autoridad nacional. No se atribuye control uniforme durante la guerra civil.'),
 ('CHL','Q1320','Jorge Montt','Presidente constitucional de la República','1891-12-26','1896-09-17',CHL,11,False,False,'Presidencia constitucional posterior a la Junta, registrada como fase distinta.'),
 ('CHL','Q1319','Federico Errázuriz Echaurren','Presidente de la República','1896-09-18','1899-12-31',CHL,11,False,True,'Mandato iniciado1896, continuado hasta1901. No elimina ni altera sus suplencias posteriores al corte.'),
 ('PER','Q599651','Antonio Arenas','Presidente del Consejo de Ministros · encargado del Poder Ejecutivo','1885-12-03','1886-06-02',PER,11,False,False,'Ejecutivo de transición tras la renuncia de Iglesias; no se transforma en una presidencia elegida para un nuevo periodo.'),
 ('PER','Q170059','Manuel Candamo','Presidente de la Junta de Gobierno','1895-03-20','1895-09-07',PER,11,False,False,'Gobierno de transición tras la caída de Cáceres; distinto de su presidencia constitucional de1903.'),
 ('URY','Q885848','Lorenzo Latorre','Presidente de la República','1880-01-01','1880-03-14',URY,11,True,False,'Última parte de su presidencia, hasta la renuncia y sustitución de marzo1880.'),
 ('URY','Q879038','Francisco Antonino Vidal','Presidente de la República · primer periodo','1880-03-15','1882-02-27','https://www.cervantesvirtual.com/research/coleccion-legislativa-de-la-republica-oriental-del-uruguay-o-sea-recopilacion-cronologica--por-matias-alonso-criado--tomo-8/7e6477db-3341-415d-8456-01bfcd43ba3d.pdf',11,False,False,'La aceptación original de su renuncia por la Asamblea está fechada28/2/1882. La tabla diplomática que imprime1/2 es un error; se prefiere el acto legislativo original.'),
 ('URY','Q885853','Miguel Alberto Flangini Ximénez','Presidente del Senado · encargado del Poder Ejecutivo','1882-02-28','1882-02-28','https://www.cervantesvirtual.com/research/coleccion-legislativa-de-la-republica-oriental-del-uruguay-o-sea-recopilacion-cronologica--por-matias-alonso-criado--tomo-8/7e6477db-3341-415d-8456-01bfcd43ba3d.pdf',11,False,False,'La comunicación original de la Asamblea de28/2/1882 acepta la renuncia de Vidal y encarga el Ejecutivo al presidente del Senado. El nuevo presidente Santos asume1/3; no fue un mes entero de presidencia ni se trata del poeta homónimo.'),
 ('URY','Q879048','Máximo Santos','Presidente de la República · primer periodo','1882-03-01','1886-02-28',URY,11,False,False,'Primer periodo, separado del retorno al poder en mayo1886.'),
 ('URY','Q879038','Francisco Antonino Vidal','Presidente de la República · segundo periodo','1886-03-01','1886-05-23',URY,11,False,False,'Breve segundo periodo; no continuidad desde1880.'),
 ('URY','Q879048','Máximo Santos','Presidente de la República · segundo periodo','1886-05-24','1886-11-17',URY,11,False,False,'Segundo periodo, previo a la presidencia de Tajes.'),
 ('URY','Q879013','Máximo Tajes','Presidente de la República','1886-11-18','1890-02-28',URY,11,False,False,'Sucesión posterior a Santos.'),
 ('URY','Q885858','Julio Herrera y Obes','Presidente de la República','1890-03-01','1894-02-28',URY,11,False,False,'Periodo anterior al interinato de Stewart.'),
 ('URY','Q885877','Duncan Stewart','Presidente del Senado · encargado del Poder Ejecutivo','1894-03-01','1894-03-20',URY,11,False,False,'Interinato mientras la Asamblea elige al siguiente presidente; no se atribuye un cuatrienio electivo.'),
 ('URY','Q500362','Juan Idiarte Borda','Presidente de la República','1894-03-21','1897-08-25',URY,11,False,False,'Muere asesinado en ejercicio25/8/1897. El día del fallecimiento y la sucesión puede figurar en ambos registros.'),
 ('URY','Q600875','Juan Lindolfo Cuestas','Presidente provisional y de facto','1897-08-25','1899-02-14',URY,11,False,False,'La fase provisional deriva en Gobierno de facto en1898; se distingue del mandato constitucional iniciado1899.'),
 ('URY','Q15145','José Batlle y Ordóñez','Presidente del Senado · encargado del Poder Ejecutivo','1899-02-15','1899-02-28',URY,11,False,False,'Suplencia anterior a sus dos presidencias constitucionales del sigloXX.'),
 ('URY','Q600875','Juan Lindolfo Cuestas','Presidente constitucional de la República','1899-03-01','1899-12-31',URY,11,False,True,'Inicio del mandato constitucional1899–1903; no se fusiona con su ejercicio provisional.'),
 ('CRI','Q449450','Bernardo Soto Alfaro','Presidente de la República','1885-03-12','1889-11-06',CRI,11,False,False,'La entrega del ejercicio a Durán7/11/1889 se distingue de una nueva elección presidencial.'),
 ('CRI','Q440376','Carlos Durán Cartín','Tercer designado · encargado del Poder Ejecutivo','1889-11-07','1890-05-07','https://pani.go.cr/dia-nacional-de-la-democracia/',11,False,False,'Ejercicio por designación tras la crisis electoral, hasta la investidura del presidente electo Rodríguez.'),
 ('CRI','Q880720','José Joaquín Rodríguez Zeledón','Presidente de la República','1890-05-08','1894-05-07','https://www.presidencia.go.cr/node/128',11,False,False,'El sitio presidencial fecha8/5/1890–8/5/1894; extremo inclusivo anterior al relevo.'),
 ('CRI','Q889083','Rafael Iglesias Castro','Presidente de la República · periodos consecutivos','1894-05-08','1899-12-31','https://www.asamblea.go.cr/sd/Memoriasgobierno/Memoria%20Ministerio%20de%20Educaci%C3%B3n%20P%C3%BAblica%201939-1940-3.pdf',11,False,True,'La memoria oficial acredita8/5/1894–8/5/1902; la galería presidencial distingue los periodos1894–1898 y1898–1902. La reelección no se interpreta como cambio de persona.'),
 ('DOM','Q437144','Fernando Arturo de Meriño','Presidente de la República','1880-09-01','1882-08-31',DOM,11,False,False,'Periodo constitucional anterior a la primera presidencia de Heureaux.'),
 ('DOM','Q722921','Ulises Heureaux','Presidente de la República · primer periodo','1882-09-01','1884-08-31',DOM,11,False,False,'Primer periodo, separado de su retorno en1887.'),
 ('DOM','Q436216','Francisco Gregorio Billini','Presidente de la República','1884-09-01','1885-05-15',DOM,11,False,False,'Renuncia16/5/1885; sucesión de Woss y Gil, no retorno inmediato de Heureaux.'),
 ('DOM','Q887708','Alejandro Woss y Gil','Presidente de la República · sucesión vicepresidencial','1885-05-16','1887-01-05','https://bibliotecadelcongreso.gob.do/Libros/0008586.pdf',11,False,False,'Ejecutivo posterior a Billini y anterior al regreso de Heureaux.'),
 ('DOM','Q722921','Ulises Heureaux','Presidente de la República · mandatos sucesivos','1887-01-06','1899-07-26',DOM,11,False,False,'Regresa en1887; sucesivas reelecciones hasta su asesinato26/7/1899. No equivale a un único mandato constitucional de doce años.'),
 ('HTI','Q886204','Lysius Salomon','Presidente de Haití','1880-01-01','1888-08-09','https://archives.nypl.org/scm/20733',11,True,False,'El inventario de correspondencia presidencial fecha23/10/1879–10/8/1888; extremo inclusivo anterior al relevo. La sucesión provisional se conserva separada.'),
 ('HTI','Q886431','François Denys Légitime','Presidente de Haití · Gobierno en la guerra civil','1888-12-01','1889-06-30','https://ambassadehaiti-france.org/galerie-des-chefs-detat-haitiens/',10,True,True,'Ventana interior de la presidencia1888–1889 durante la guerra civil. La galería no resuelve todos los días de la autoridad provisional; no se convierte en control uniforme del país.'),
 ('HTI','Q886457','Florvil Hyppolite','Presidente de Haití','1889-11-01','1896-02-29','https://ambassadehaiti-france.org/galerie-des-chefs-detat-haitiens/',10,True,True,'Ventana interior de la presidencia de octubre1889 a marzo1896. Los extremos de la ventana no son investidura ni fallecimiento.'),
]


def adjacent(day, delta):
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=delta)).isoformat()


def curate(incoming):
    data = copy.deepcopy(incoming)
    countries = data['countries']
    portraits = {leader['person']: copy.deepcopy(leader['portrait'])
                 for country in countries.values() for leader in country.get('leaders', [])
                 if leader.get('portrait')}
    countries.setdefault('BRA-EMPIRE', dict(qid='Q217230', name='Imperio de Brasil', flags=[], leaders=[]))
    targeted = {(row[0], row[1]) for row in ROWS}
    imperial_people = {row[1] for row in ROWS if row[0] == 'BRA-EMPIRE'}
    for key, country in countries.items():
        kept = []
        for old in country.get('leaders', []):
            if old.get('acquisition') == TAG:
                continue
            # Keep every original record touching1900+ literally unchanged,
            # even when it began inside the curation window.
            if old['end'] >= '1900-01-01':
                kept.append(old)
                continue
            start, end = FIRST, LAST
            selected = (key, old['person']) in targeted
            if key == 'BRA' and old['person'] in imperial_people:
                selected, end = True, '1889-11-14'
            if not selected or old['end'] < start or old['start'] > end:
                kept.append(old)
                continue
            if old['start'] < start:
                earlier = copy.deepcopy(old)
                earlier.update(end=adjacent(start, -1), endIsCoverageBoundary=True)
                kept.append(earlier)
            if old['end'] > end:
                later = copy.deepcopy(old)
                later.update(start=adjacent(end, 1), startIsCoverageBoundary=True)
                kept.append(later)
        country['leaders'] = kept
    for key, person, name, role, start, end, source, precision, first_boundary, last_boundary, note in ROWS:
        assert FIRST <= start <= end <= LAST
        record = dict(person=person, name=name, role=role, start=start, end=end,
                      source=source, precision=precision, curated=True, acquisition=TAG, note=note)
        if first_boundary:
            record['startIsCoverageBoundary'] = True
        if last_boundary:
            record['endIsCoverageBoundary'] = True
        if first_boundary or last_boundary:
            record['note'] += ' Los extremos marcados como cobertura no son nombramientos ni dimisiones.'
        if person in portraits:
            record['portrait'] = copy.deepcopy(portraits[person])
        countries[key]['leaders'].append(record)
    # Stable sorting only affects presentation order, never record contents.
    for country in countries.values():
        country['leaders'].sort(key=lambda leader: (leader['start'], leader['name'], leader['role']))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Use an explicit separate output file; the input catalogue is preserved.')
    result = curate(json.loads(args.input.read_text(encoding='utf8')))
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf8', newline='\n')
    print('Prepared', len(ROWS), 'bounded American authority records; original1900+ records preserved.')
