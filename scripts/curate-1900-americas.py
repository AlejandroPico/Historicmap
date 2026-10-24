"""Bounded American authority corrections for1900–1919.

Pure curate(data), no network or public writes on import. Sources and documentary
limits: docs/AUTHORITIES-1900-AMERICAS.md. Annual coverage is not an appointment.
"""
import argparse
import copy
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'curated-1900-americas-0.12'
FIRST, LAST = '1900-01-01', '1919-12-31'
DOM = 'https://www.usni.org/magazines/proceedings/1921/february/operations-ashore-dominican-republic'
PAN = 'https://www.govinfo.gov/content/pkg/GOVPUB-W79-ad59626cf1c66b2408af30aa698366f9/pdf/GOVPUB-W79-ad59626cf1c66b2408af30aa698366f9.pdf'
URY = 'https://www.embajadadeuruguay.org/pages/acerca-de-uruguay/sistema-de-gobierno.php'
VEN = 'https://history.state.gov/historicaldocuments/frus1917Supp01v01/d377'

# key, QID, person, office, interval, source, precision, coverage edges, note.
ROWS = [
 ('DOM','Q887824','Juan Isidro Jimenes','Presidente constitucional de la República','1900-01-01','1902-03-31','https://revistas.uasd.edu.do/index.php/ecos/article/download/324/482?inline=1',10,True,True,'Ventana interior de su primer mandato1899–1902, contrastada con mensajes originales al Congreso. El límite de marzo evita fingir resuelta la diferencia entre levantamiento, pérdida del poder y salida del país en abril/mayo1902.'),
 ('DOM','Q436482','Horacio Vásquez','Presidente provisional · ejercicio del Ejecutivo','1902-06-01','1903-02-28',DOM,10,True,True,'Ventana interior del Gobierno provisional1902–1903; no fija el comienzo del levantamiento de abril ni el día de la sustitución por Woss y Gil.'),
 ('DOM','Q887708','Alejandro Woss y Gil','Presidente · Gobierno provisional y posterior fase constitucional','1903-06-20','1903-10-31',DOM,10,True,True,'La relación naval contemporánea fecha la investidura constitucional20/6; otras cronologías distinguen elección e investidura de modo diferente. Se conserva una ventana interior anterior a su caída de noviembre, sin certificar todos los días del Gobierno provisional.'),
 ('DOM','Q887654','Carlos Felipe Morales Languasco','Presidente · Gobierno revolucionario y posterior fase constitucional','1903-12-02','1906-01-11','https://colecciones.agn.gob.do/opac/ficha.php?codopac=OP003&idpag=0046152027&informatico=00096097PI&presenta=digitaly2p&suposi=2',11,True,False,'Circular original2/12/1903 comunica un Gobierno ya constituido. El extremo inicial es evidencia documental, no inicio de la revolución24/10 ni una investidura nacional ese día. La renuncia12/1/1906 se distingue de la pérdida práctica de autoridad en diciembre1905.'),
 ('DOM','Q887835','Eladio Victoria','Presidente provisional; después presidente constitucional','1911-12-06','1912-11-26',DOM,11,False,False,'La relación naval fecha la entrada6/12/1911 y renuncia26/11/1912. La elección de febrero1912 no se retrotrae a la entrada provisional.'),
 ('DOM','Q163612','Adolfo Alejandro Nouel','Presidente provisional de la República','1912-12-01','1913-02-28',DOM,10,False,True,'Investido1/12/1912. La ventana termina en febrero como cobertura: las fuentes distinguen anuncio de dimisión, aceptación y sustitución de marzo/abril1913; aquí no se fabrica una fecha final única.'),
 ('DOM','COLLECTIVE-DOM-US-MILITARY','Gobierno militar de Estados Unidos','Autoridad ejecutiva militar de ocupación','1916-11-29','1919-12-31','https://history.state.gov/historicaldocuments/frus1918/d402',11,False,True,'La proclamación de ocupación29/11/1916 establece el Gobierno militar. No es una presidencia dominicana electa ni una anexión a Estados Unidos. La continuidad posterior se conserva en sus registros propios; no se inventa un retrato de este órgano.'),
 ('CRI','Q889083','Rafael Iglesias Castro','Presidente de la República · segundo mandato','1900-01-01','1901-12-31','https://www.presidencia.go.cr/expresidencias',9,True,True,'Ventana interior del mandato1898–1902. La fuente presidencial acredita ambos periodos1894–1898 y1898–1902; no se presenta el cierre1901 como dimisión ni se omiten por ello las suplencias de1902 que siguen pendientes.'),
 ('URY','Q600875','Juan Lindolfo Cuestas','Presidente de la República · mandato constitucional','1900-01-01','1903-02-28',URY,11,True,False,'Mandato constitucional desde1/3/1899 al relevo1/3/1903; extremo inclusivo anterior al sucesor. Se distingue de su etapa provisional y del interinato de Batlle de febrero1899.'),
 ('URY','Q887389','Claudio Williman','Presidente de la República','1907-03-01','1911-02-28',URY,11,False,False,'Mandato1/3/1907–1/3/1911; extremo inclusivo anterior a la segunda presidencia de Batlle. No se fusiona con esta.'),
 ('PAN','Q558309','Manuel Amador Guerrero','Presidente de la República · primer mandato constitucional','1904-03-01','1908-09-30','https://history.state.gov/historicaldocuments/frus1904/d551',10,True,False,'Ventana desde marzo, posterior a la investidura de febrero1904. El despacho22/2 dice sábado19 aunque el sábado fue20; no se convierte esa discrepancia del original en una precisión diaria ficticia. Se conserva la sucesión de Obaldía1/10/1908.'),
 ('PAN','Q887762','José Domingo de Obaldía','Presidente de la República','1908-10-01','1910-03-01',PAN,11,False,False,'La tabla distingue el mandato presidencial de sus suplencias previas como designado. Fallece en el cargo1/3/1910; la sucesión de Mendoza se registra aparte.'),
 ('PAN','Q887762','José Domingo de Obaldía','Primer designado · encargado del Poder Ejecutivo','1907-06-24','1907-12-29',PAN,11,False,False,'Suplencia durante la primera presidencia de Amador; no adelanta su mandato presidencial propio de1908.'),
 ('PAN','Q322239','Belisario Porras','Presidente de la República · primer mandato','1912-10-01','1916-09-30',PAN,11,False,False,'Mandato constitucional anterior a Valdés; no continuidad presidencial entre1916 y1918.'),
 ('PAN','Q321934','Ramón Maximiliano Valdés','Presidente de la República','1916-10-01','1918-06-03',PAN,11,False,False,'Fallece en ejercicio3/6/1918. No confundir el periodo para el que fue elegido con el que realmente ejerció.'),
 ('PAN','Q322244','Ciro Luis Urriola','Primer designado · encargado del Poder Ejecutivo','1918-06-03','1918-09-30',PAN,11,False,False,'Sucesión tras la muerte de Valdés; el cargo de designado y las controversias electorales no lo convierten en presidente electo para un cuatrienio nuevo.'),
 ('PAN','Q322227','Pedro Antonio Díaz','Segundo designado · encargado del Poder Ejecutivo','1918-10-01','1918-10-11',PAN,11,False,False,'Interregno hasta la llegada de Porras desde Washington, que asume12/10/1918.'),
 ('PAN','Q322239','Belisario Porras','Primer designado · encargado del Poder Ejecutivo','1918-10-12','1919-12-31',PAN,11,False,True,'Asume durante el periodo originalmente correspondiente a Valdés. La revisión termina1919; su ejercicio continuó en1920 y se conserva en el registro posterior.'),
 ('COL','Q887907','Rafael Reyes','Presidente de la República · régimen del Quinquenio','1904-12-31','1908-12-31','https://enciclopedia.banrepcultural.org/index.php?title=Rafael_Reyes',9,True,True,'Ventana interior del mandato1904–1909; no fija aquí la toma de posesión ni la renuncia. La suplencia de Angulo en1908 permanece separada y exige no confundir titularidad con ejercicio diario continuo.'),
 ('COL','Q3138725','Ramón González Valencia','Presidente de la República · conclusión del periodo de Reyes','1909-08-03','1910-08-06','https://www.policia.gov.co/sites/default/files/publicaciones-institucionales/cuaderno-historico-edicion-4.pdf',11,False,False,'Elección por el Congreso3/8/1909; entrega el mando a Restrepo7/8/1910. La suplencia previa de Jorge Holguín no se atribuye a González Valencia.'),
 ('COL','Q2939346','Carlos Eugenio Restrepo','Presidente de la República','1910-08-07','1914-08-06','https://enciclopedia.banrepcultural.org/index.php/Carlos_Eugenio_Restrepo_Restrepo',11,False,False,'Elegido15/7/1910 y recibe el mando7/8; elección e investidura son hechos distintos. Extremo inclusivo anterior al relevo de Concha.'),
 ('CUB','Q888706','Charles Edward Magoon','Gobernador provisional de Cuba · administración estadounidense','1906-10-13','1909-01-28','https://www.archives.gov/research/guide-fed-records/groups/199.html',11,False,False,'Sucede al gobernador provisional Taft13/10/1906; el Gobierno provisional termina28/1/1909. No es presidente cubano ni se confunde esta segunda intervención con la ocupación anterior a1902.'),
 ('VEN','Q1157551','Victorino Márquez Bustillos','Presidente provisional · jefatura formal del Estado','1915-01-01','1919-12-31',VEN,9,True,True,'Ventana interior del ejercicio1914–1922. El mensaje al Congreso de1917 acredita el título provisional. No se transforma el poder dominante de Gómez en la ocupación simultánea de esta presidencia formal.'),
 ('VEN','Q317990','Juan Vicente Gómez','Autoridad militar y poder de facto · fuera de la presidencia formal','1915-01-01','1919-12-31','https://www.govinfo.gov/content/pkg/GPO-CRECB-1930-pt9-v72/pdf/GPO-CRECB-1930-pt9-v72-12.pdf',9,True,True,'Ventana interior de la estructura de poder dominada por Gómez; el testimonio parlamentario distingue el mando del Ejército de la presidencia provisional de Márquez Bustillos. La terminología política del testimonio no se reproduce como clasificación jurídica del atlas.'),
 ('MEX','Q313122','Venustiano Carranza','Primer Jefe del Ejército Constitucionalista · encargado del Poder Ejecutivo','1914-08-20','1917-04-30','https://www.gob.mx/segob/articulos/conoce-mas-acerca-de-venustiano-carranza',11,False,False,'Entrada20/8/1914 con título de Primer Jefe; desde la ruptura con la Convención mantuvo un Gobierno rival, inicialmente en Veracruz. No se afirma control nacional uniforme ni presidencia constitucional antes de la protesta1/5/1917.'),
]


def adjacent(day, delta):
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=delta)).isoformat()


def curate(incoming):
    data = copy.deepcopy(incoming)
    countries = data['countries']
    portraits = {l['person']: copy.deepcopy(l['portrait'])
                 for c in countries.values() for l in c['leaders'] if l.get('portrait')}
    for country in countries.values():
        country['leaders'] = [l for l in country['leaders'] if l.get('acquisition') != TAG]
    for key, qid, name, role, start, end, source, precision, start_boundary, end_boundary, note in ROWS:
        assert FIRST <= start <= end <= LAST
        kept = []
        for old in countries[key]['leaders']:
            # Every pre-existing record intersecting1920+ remains exactly intact.
            if old['person'] != qid or old['end'] >= '1920-01-01' or old['end'] < start or old['start'] > end:
                kept.append(old)
                continue
            if old['start'] < start:
                earlier = copy.deepcopy(old)
                earlier.update(end=adjacent(start,-1),endIsCoverageBoundary=True)
                kept.append(earlier)
            if old['end'] > end:
                later = copy.deepcopy(old)
                later.update(start=adjacent(end,1),startIsCoverageBoundary=True)
                kept.append(later)
        record = dict(person=qid,name=name,role=role,start=start,end=end,source=source,
                      precision=precision,curated=True,acquisition=TAG,note=note)
        if start_boundary:
            record['startIsCoverageBoundary'] = True
        if end_boundary:
            record['endIsCoverageBoundary'] = True
        if start_boundary or end_boundary:
            record['note'] += ' Los extremos marcados como cobertura no son nombramientos ni dimisiones.'
        if qid in portraits:
            record['portrait'] = copy.deepcopy(portraits[qid])
        countries[key]['leaders'] = kept + [record]
    for country in countries.values():
        country['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=pathlib.Path,default=ROOT/'public/data/identities.json')
    parser.add_argument('--output',type=pathlib.Path)
    args = parser.parse_args()
    result = curate(json.loads(args.input.read_text(encoding='utf8')))
    (args.output or args.input).write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    print('Prepared',sum(l.get('acquisition')==TAG for c in result['countries'].values() for l in c['leaders']),'American1900–1919 authority windows.')
