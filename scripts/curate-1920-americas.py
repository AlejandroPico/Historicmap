"""Bounded American authority gaps from the 1920/1930/1940 coverage audits.

Offline, idempotent curate(data) -> a copied catalogue. No media acquisition.
CLI requires --input and --output; public data is never an implicit destination.
Documentary windows marked precision9 are not invented appointment dates.
"""
import argparse
import copy
import datetime
import json
from pathlib import Path

TAG = 'curated-1920-americas-0.11'
NOTE = ('Ventana documental de esta revisión: los extremos de cobertura no son '
        'nombramientos ni dimisiones. No constituye un censo de todas las suplencias del año. ')
PAN = 'https://www.govinfo.gov/content/pkg/GOVPUB-W79-ad59626cf1c66b2408af30aa698366f9/pdf/GOVPUB-W79-ad59626cf1c66b2408af30aa698366f9.pdf'
ECU = 'https://educacion.gob.ec/wp-content/uploads/downloads/2014/06/TEXTO-DE-ESTUDIANTE-SOCIALES-7mo-EGB.pdf'
URY = 'https://archivo.presidencia.gub.uy/_web/noticias/2010/02/2010022810.htm'
CUB = 'https://tile.loc.gov/storage-services/master/frd/frdcstdy/cu/cubacountrystudy00huds/cubacountrystudy00huds.pdf'
SLV = 'https://www.mined.gob.sv/descarga/cipotes/historia_ESA_TomoII_0_.pdf'

# key, Wikidata QID or explicit collective identifier, name, role, start, end,
# source, precision, coverage boundary flags, factual/contextual note.
# QIDs were searched through wbsearchentities, Spanish labels/descriptions,
# on24/10/2026; the local search results are research evidence, not authority dates.
ROWS = [
 ('PAN','Q721734','Ernesto Tisdel Lefevre','Tercer designado · encargado del Poder Ejecutivo','1920-01-30','1920-09-30',PAN,11,False,False,'Interregno anterior al tercer mandato de Porras; no presidente elegido para un mandato propio.'),
 ('PAN','Q322239','Belisario Porras','Presidente de la República · mandato titular','1920-10-01','1924-09-30',PAN,11,False,False,'La fuente distingue una suplencia de Rodolfo Chiari del6 al10/6/1923; esta fila conserva el mandato titular y no niega esa suplencia.'),
 ('PAN','Q338900','Florencio Harmodio Arosemena','Presidente de la República','1929-01-01','1930-12-31',PAN,9,True,True,'Cobertura interior del mandato1928–1931; no se resuelve aquí la discrepancia diaria del golpe de enero1931.'),
 ('PAN','Q708308','Juan Demóstenes Arosemena','Presidente de la República','1936-10-01','1939-12-16',PAN,11,False,False,'La fuente fecha el final en16/12/1939; se conservan los designados de la sucesión.'),
 ('PAN','Q721723','Ezequiel Fernández Jaén','Segundo designado · encargado del Poder Ejecutivo','1939-12-16','1939-12-17',PAN,11,False,False,'Tramo inclusivo hasta el día anterior al relevo del18/12; no mandato electoral.'),
 ('PAN','Q769758','Augusto Samuel Boyd','Primer designado · encargado del Poder Ejecutivo','1939-12-18','1940-09-30',PAN,11,False,False,'Ejerce tras la muerte de Juan Demóstenes Arosemena.'),
 ('PAN','Q338961','Ricardo Adolfo de la Guardia','Encargado de la Presidencia · ejercicio del Ejecutivo','1942-01-01','1944-12-31','https://bdigital.binal.ac.pa/bdp/older/republicano14.pdf',9,True,True,'Ventana interior del ejercicio iniciado9/10/1941; termina aquí por cobertura, antes de la transferencia de1945.'),
 ('VEN','Q1157551','Victorino Márquez Bustillos','Presidente provisional · jefatura formal del Estado','1920-01-01','1921-12-31','https://history.state.gov/historicaldocuments/frus1921v02/d896',9,True,True,'El despacho distingue al presidente provisional de Juan Vicente Gómez, interlocutor que determina decisiones de Gobierno.'),
 ('VEN','Q317990','Juan Vicente Gómez','Autoridad militar y poder de facto · fuera de la presidencia formal','1920-01-01','1921-12-31','https://history.state.gov/historicaldocuments/frus1921v02/d896',9,True,True,'No se le atribuye la presidencia formal ocupada por Márquez Bustillos. El despacho de1921 documenta su intervención decisiva en la política petrolera.'),
 ('DOM','COLLECTIVE-DOM-US-MILITARY','Gobierno militar de Estados Unidos','Autoridad ejecutiva militar de ocupación','1920-01-01','1922-10-20','https://2001-2009.state.gov/r/pa/ho/time/wwi/108649.htm',9,True,True,'Órgano ocupante, no presidente dominicano ni retrato individual. La instalación del Gobierno provisional en1922 no puso fin a la ocupación, que continuó hasta1924.'),
 ('DOM','Q1710374','Juan Bautista Vicini Burgos','Presidente provisional · autoridad civil dominicana','1922-10-21','1923-12-31','https://2001-2009.state.gov/r/pa/ho/time/wwi/108649.htm',9,False,True,'Investido21/10/1922; el límite1923 es cobertura de este hueco y no fin del Gobierno. El gobernador militar conservó facultades presupuestarias durante la transición.'),
 ('DOM','Q1496510','Jacinto Bienvenido Peynado','Presidente de la República · jefatura formal del Estado','1939-01-01','1939-12-31','https://history.state.gov/historicaldocuments/frus1939v02/d50',9,True,True,'Presidencia formal acreditada por correspondencia de1939. La dictadura y el poder de Trujillo no convierten a este en presidente formal durante esta ventana.'),
 ('DOM','Q436078','Manuel de Jesús Troncoso de la Concha','Presidente de la República · jefatura formal del Estado','1940-01-01','1941-12-31','https://colecciones.agn.gob.do/opac/ficha.php?informatico=00103214',9,True,True,'El AGN documenta el paso de vicepresidente a presidente tras la muerte de Peynado y el periodo1940–1942; el inicio de año representa resolución anual y no una investidura el1deenero. El día del relevo requiere cotejo adicional y el cierre1941 no es cese.'),
 ('ECU','Q3510130','José Luis Tamayo','Presidente constitucional de la República','1921-01-01','1923-12-31',ECU,9,True,True,'Ventana interior del mandato1920–1924, sin inventar investidura enenero1921.'),
 ('ECU','Q2026643','Alfredo Baquerizo Moreno','Presidente del Senado · encargado del Poder Ejecutivo','1931-10-15','1932-08-27',ECU,11,False,False,'Encargo distinto de su presidencia1916–1920; no se fusionan los dos periodos.'),
 ('ECU','Q2888186','Juan de Dios Martínez Mera','Presidente constitucional de la República','1932-12-05','1933-10-19',ECU,11,False,False,'Sucesión según la tabla presidencial del Ministerio de Educación.'),
 ('ECU','Q3509006','Abelardo Montalvo','Ministro de Gobierno · encargado del Poder Ejecutivo','1933-10-20','1934-08-31',ECU,11,False,False,'Encargo provisional; no un mandato electoral independiente.'),
 ('ECU','Q707171','José María Velasco Ibarra','Presidente constitucional de la República · primer mandato','1934-09-01','1935-08-20',ECU,11,False,False,'Extremo inclusivo anterior al relevo del21/8/1935 por Antonio Pons.'),
 ('ECU','Q440524','Alberto Enríquez Gallo','Jefe supremo · ejercicio del Ejecutivo','1937-10-23','1938-08-09',ECU,11,False,False,'No se le atribuye una presidencia constitucional electa; el relevo interino se documenta10/8/1938.'),
 ('ECU','Q434918','Manuel María Borrero','Presidente constitucional interino','1938-08-10','1938-12-01',ECU,11,False,False,'Interinato separado de Enríquez Gallo y Mosquera.'),
 ('ECU','Q253787','Aurelio Mosquera Narváez','Presidente constitucional de la República','1938-12-02','1939-11-17',ECU,11,False,False,'Mandato que resuelve la referencia al cierre1938.'),
 ('ECU','Q707171','José María Velasco Ibarra','Presidente de la República · segundo mandato y fase de facto','1944-08-10','1947-08-22',ECU,11,False,False,'La fuente distingue etapa constitucional1944–1946, ruptura del30/3/1946 y nueva etapa constitucional. Se conserva el ejercicio de la misma persona con esa diferencia explícita; no se afirma legalidad constitucional continua.'),
 ('ECU','Q434552','Carlos Mancheno Cajas','Presidente de facto · ejercicio del Ejecutivo','1947-08-23','1947-09-01',ECU,11,False,False,'Tramo inclusivo anterior al relevo de2/9/1947; no presidente constitucional electo.'),
 ('ECU','Q434753','Mariano Suárez Veintimilla','Presidente constitucional de la República','1947-09-02','1947-09-15',ECU,11,False,False,'Tramo inclusivo anterior al relevo de16/9/1947.'),
 ('ECU','Q338942','Carlos Julio Arosemena Tola','Presidente constitucional de la República','1947-09-16','1948-08-31',ECU,11,False,False,'Se mantiene separado de Arosemena Monroy y de Galo Plaza.'),
 ('URY','Q887720','José Serrato','Presidente de la República · Ejecutivo compartido','1924-01-01','1926-12-31',URY,9,True,True,'Mandato1923–1927. Compartía el Poder Ejecutivo con el Consejo Nacional de Administración; no se le presenta como su único titular.'),
 ('URY','Q887743','Juan Campisteguy','Presidente de la República · Ejecutivo compartido','1927-01-01','1930-12-31',URY,9,True,True,'Mandato1927–1931; los límites anuales de cobertura no afirman investidura el1deenero. El Consejo Nacional de Administración tenía atribuciones ejecutivas propias.'),
 ('URY','Q277922','Gabriel Terra','Presidente de la República · régimen autoritario desde1933','1931-01-01','1937-12-31',URY,9,True,True,'La fuente presidencial distingue el Ejecutivo compartido anterior al golpe de1933 del régimen posterior. No se extiende la revisión hasta el relevo diario de1938.'),
 ('CUB','Q879932','Carlos Mendieta','Presidente provisional de la República','1934-01-18','1935-12-10','https://newspapers.swco.ttu.edu/server/api/core/bitstreams/7137d741-c38b-4f07-aaa7-b7a783ec48f4/content',11,False,False,'La prensa contemporánea de18/1/1934 documenta la designación; la cronología deLibraryofCongress fecha la dimisión11/12/1935. El poder militar deBatista no le convierte aquí en presidente formal.'),
 ('CUB','Q888658','José Agripino Barnet','Presidente provisional de la República','1935-12-11','1935-12-31',CUB,11,False,True,'Sucesión interina tras la renuncia deMendieta. La revisión se detiene al cierre1935; Barnet continuó en1936 y no se le atribuye una dimisión en diciembre.'),
 ('CUB','Q318294','Federico Laredo Brú','Presidente de la República · jefatura formal del Estado','1937-01-01','1939-12-31',CUB,9,True,True,'Ventana interior del mandato1936–1940. No se sustituye su presidencia formal por el mando militar deBatista.'),
 ('COL','Q727099','Alfonso López Pumarejo','Presidente de la República · primer mandato','1935-01-01','1937-12-31','https://enciclopedia.banrepcultural.org/Alfonso_L%C3%B3pez_Pumarejo',9,True,True,'Ventana interior del mandato1934–1938. Su segundo mandato1942–1945 no se fusiona con este.'),
 ('CRI','Q886923','Rafael Ángel Calderón Guardia','Presidente de la República','1941-01-01','1943-12-31','https://www.presidencia.go.cr/node/142',9,True,True,'Ventana interior del mandato1940–1944. No es Rafael Calderón Muñoz: la suplencia de este del25/1al4/2/1943 figura en la Asamblea y queda pendiente de incorporación individual.'),
 ('SLV','Q887328','Salvador Castaneda Castro','Presidente de la República','1945-03-01','1948-12-13',SLV,11,False,False,'La fuente acredita la investidura1/3/1945 y el golpe del14/12/1948; extremo inclusivo anterior al relevo.'),
 ('SLV','COLLECTIVE-SLV-1950','Consejo de Gobierno Revolucionario','Órgano colegiado · ejercicio del Ejecutivo','1948-12-14','1949-12-31','https://www.csj.gob.sv/seccion-de-probidad-generalidades/',9,False,True,'Órgano colegiado militar y civil, no un presidente individual ni un retrato inventado. El Consejo continuó después de1949; no se afirma cese al cierre de esta ventana.'),
]


def adjacent(date, delta):
    return (datetime.date.fromisoformat(date) + datetime.timedelta(days=delta)).isoformat()


def curate(incoming):
    data = copy.deepcopy(incoming)
    countries = data['countries']
    missing = {row[0] for row in ROWS} - countries.keys()
    if missing:
        raise ValueError('Missing catalogue identities: ' + ', '.join(sorted(missing)))
    # Portraits may only survive in a record bearing our own previous tag.
    portraits = {l['person']: copy.deepcopy(l['portrait'])
                 for c in countries.values() for l in c['leaders'] if l.get('portrait')}
    for country in countries.values():
        country['leaders'] = [l for l in country['leaders'] if l.get('acquisition') != TAG]
    for key, qid, name, role, start, end, source, precision, start_coverage, end_coverage, note in ROWS:
        assert '1920-01-01' <= start <= end <= '1949-12-31'
        # Only replace overlapping statements of this same person/organ; retain
        # other officers, different reigns and both tails, especially1950+.
        kept = []
        for old in countries[key]['leaders']:
            if old['person'] != qid or old['end'] < start or old['start'] > end:
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
        record = dict(person=qid, name=name, role=role, start=start, end=end, source=source,
                      precision=precision, curated=True, acquisition=TAG, note=note)
        if start_coverage:
            record['startIsCoverageBoundary'] = True
        if end_coverage:
            record['endIsCoverageBoundary'] = True
        if start_coverage or end_coverage:
            record['note'] = NOTE + record['note']
        if qid in portraits and not qid.startswith('COLLECTIVE-'):
            record['portrait'] = copy.deepcopy(portraits[qid])
        kept.append(record)
        countries[key]['leaders'] = kept
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = curate(json.loads(args.input.read_text(encoding='utf8')))
    args.output.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n',
                           encoding='utf8', newline='\n')
    print(f'{len(ROWS)} documentary authority records; no symbols or media modified.')


if __name__ == '__main__':
    main()
