"""Focal American availability gaps1880–1899; pure, additive and idempotent.

Documentary windows do not certify a complete daily census. No network/public
writes; CLI requires separate explicit input/output. See the American authority
research document for sources and remaining transitions.
"""
import argparse
import copy
import json
import pathlib

TAG = 'curated-1880-americas-gaps-0.13'
# key, person, name, office, inclusive interval, source, precision,
# coverage-only start/end, factual note.
ROWS = [
 ('ECU','Q2943435','Ignacio de Veintemilla','Presidente constitucional del Ecuador','1880-01-01','1881-12-31','https://www.planificacion.gob.ec/wp-content/uploads/downloads/2014/06/Los-Constructores-del-Estado-Nacional.pdf',9,True,True,'Ventana interior del periodo constitucional1878–1882. No se identifica este ejercicio con el título de Jefe Supremo proclamado en marzo1882.'),
 ('ECU','Q2943435','Ignacio de Veintemilla','Jefe Supremo · dictadura de Veintemilla','1882-03-26','1882-12-31','https://libros.uasb.edu.ec/index.php/publicaciones/es/catalog/book/14',11,False,True,'La investigación institucional inventaría el impreso original de la Imprenta Nacional26/3/1882 que lo proclama Jefe Supremo. Ventana hasta el cierre1882; no afirma que el régimen terminase ese día ni que controlara homogéneamente todo el país.'),
 ('ECU','Q2163197','José María Plácido Caamaño','Presidente constitucional del Ecuador','1884-02-10','1888-06-30','https://www.casadelacultura.gob.ec/lotaip/2/2020/Junio/T1.pdf',11,False,False,'La investigación de la Casa de la Cultura distingue el interinato1883–1884 de la presidencia constitucional10/2/1884–30/6/1888. Este registro no suple ni elimina los gobiernos rivales y Juntas de1883.'),
 ('CRI','Q440671','Tomás Guardia Gutiérrez','Presidente de Costa Rica · titular de facto','1880-01-01','1882-07-05','https://www.dgan.go.cr/ran/index.php/RAN/issue/download/45/17',11,True,False,'Retorna al poder11/9/1877; fallece6/7/1882. La revista del Archivo Nacional documenta separaciones temporales; se incorpora aparte a Lara y no se presenta titularidad como ejercicio diario continuo.'),
 ('CRI','Q1602983','Salvador Lara Zamora','Designado · encargado del Poder Ejecutivo','1881-06-10','1882-01-23','https://www.dgan.go.cr/ran/index.php/RAN/issue/download/45/17',11,False,False,'La relación histórica del Archivo Nacional fecha su suplencia durante el viaje de salud de Guardia10/6/1881–23/1/1882. No es un nuevo presidente elegido ni sucesión por fallecimiento.'),
 ('GTM','Q679362','Justo Rufino Barrios','Presidente de Guatemala','1880-01-01','1885-04-02','https://banguat.gob.gt/sites/default/files/banguat/Publica/libros/05.pdf',11,True,False,'El Banco de Guatemala fecha el gobierno desde1873 y su muerte2/4/1885 en Chalchuapa. El intento de unión centroamericana no equivale a control nacional efectivo de todas las repúblicas vecinas.'),
 ('GTM','Q712945','Manuel Lisandro Barillas','Presidente de Guatemala · gobierno provisional y posterior fase constitucional','1885-12-01','1892-02-29','https://repositorio.uvg.edu.gt/bitstreams/a9d29a95-0237-49dc-b4e2-28454c7033b4/download',10,True,True,'Ventana interior de su gobierno1885–1892, documentado mediante memorias de Hacienda originales. No fija la sucesión inmediata de abril1885 ni confunde toma provisional y mandato constitucional. El relevo de Reina se documenta por separado15/3/1892.'),
 ('GTM','Q888406','José María Reina Barrios','Presidente de Guatemala','1892-03-15','1897-12-31','https://biblioteca.usac.edu.gt/EPS/07/07_6134.pdf',11,False,True,'El material del Museo Nacional de Historia conservado porUSAC fecha la toma15/3/1892 y el periodo1892–1898. Esta ventana termina1897 por cobertura; no fecha allí su muerte ni adelanta la presidencia de Estrada Cabrera.'),
 ('VEN','Q602420','Antonio Guzmán Blanco','Presidente de Venezuela · Quinquenio','1880-01-01','1883-12-31','https://bibliofep.fundacionempresaspolar.org/dhv/entradas/g/guzman-blanco-antonio/',9,True,True,'Ventana interior del segundo gobierno1879–1884, denominado Quinquenio por el Diccionario de Historia de Venezuela. La alocución original26/2/1879 acredita el retorno. No se fusiona con sus etapas anteriores ni con el Bienio posterior.'),
 ('VEN','Q2497570','Raimundo Andueza Palacio','Presidente de Venezuela','1891-01-01','1891-12-31','https://mppre.gob.ve/publicacion/1642-0',9,True,True,'Ventana interior del mandato1890–1892, acreditado por la investigación institucional de la Casa Amarilla y su mobiliario presidencial. No resuelve las divergencias entre elección, investidura y entrega durante la Revolución Legalista1892.'),
 ('COL','Q683532','Rafael Núñez','Presidente de los Estados Unidos de Colombia · primer mandato','1880-04-08','1882-03-31','https://banrep.gov.co/en/publications-research/books/economic-writings-rafael-nunez',11,False,False,'La investigación del Banco de la República fecha8/4/1880–1/4/1882; se usa extremo inclusivo anterior al sucesor. No se prolonga esta presidencia sobre el periodo de Zaldúa/Otálora.'),
 ('COL','Q683532','Rafael Núñez','Presidente de los Estados Unidos de Colombia · segundo mandato','1884-09-01','1885-12-31','https://babel.banrepcultural.org/digital/collection/p17054coll26/id/4239/',10,True,True,'Ventana posterior a la entrada de agosto1884, documentada en la ficha de prensa original de1885; no se fija el día exacto de posesión. Su jefatura durante la guerra civil no equivale a control territorial uniforme. Se preservan las suplencias y los registros1886+ del catálogo.'),
]


def curate(incoming):
    data = copy.deepcopy(incoming)
    countries = data['countries']
    portraits = {leader['person']: copy.deepcopy(leader['portrait'])
                 for country in countries.values() for leader in country.get('leaders', [])
                 if leader.get('portrait')}
    for country in countries.values():
        country['leaders'] = [leader for leader in country.get('leaders', [])
                              if leader.get('acquisition') != TAG or leader['end'] >= '1900-01-01']
    for key, person, name, role, start, end, source, precision, start_boundary, end_boundary, note in ROWS:
        assert '1880-01-01' <= start <= end <= '1899-12-31'
        record = dict(person=person, name=name, role=role, start=start, end=end,
                      source=source, precision=precision, curated=True, acquisition=TAG, note=note)
        if start_boundary:
            record['startIsCoverageBoundary'] = True
        if end_boundary:
            record['endIsCoverageBoundary'] = True
        if start_boundary or end_boundary:
            record['note'] += ' Los extremos marcados como cobertura no son nombramientos ni dimisiones.'
        if person in portraits:
            record['portrait'] = copy.deepcopy(portraits[person])
        countries[key]['leaders'].append(record)
    for country in countries.values():
        country['leaders'].sort(key=lambda leader: (leader['start'], leader['name'], leader['role']))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, required=True)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Provide a separate output file; the input catalogue remains intact.')
    result = curate(json.loads(args.input.read_text(encoding='utf8')))
    args.output.write_text(json.dumps(result, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf8', newline='\n')
    print('Prepared', len(ROWS), 'focal American availability windows.')
