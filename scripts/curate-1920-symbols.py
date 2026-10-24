"""Reviewed 1920–1949 symbol windows; source checks never modify public data.

Run after preparing RSR, ROC, YKM and RSI identities and generic imports.
--check-sources records Commons metadata only. Normal execution reuses licensed,
unchanged local SVGs before calling the existing 1970 acquisition helper.
"""
import argparse
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('symbols1970', ROOT / 'scripts/curate-1970-symbols.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
TAG = 'curated-symbols-0.11'
START, END = '1920-01-01', '1949-12-31'
ANNUAL = ('Ventana documental para la selección al cierre anual, no fecha exacta de adopción o derogación. '
          'El símbolo no acredita fronteras, control efectivo ni reconocimiento diplomático. ')
SOURCES = {
 'de': 'https://www.bundestag.de/dokumente/textarchiv/1919-07-03-schwarz-rot-gold-649430',
 'es': 'https://www.lamoncloa.gob.es/lang/en/espana/statesymbols/paginas/index.aspx',
 'it': 'https://acs.cultura.gov.it/festa-del-tricolore-2022/',
 'ca': 'https://www.gg.ca/en/heraldry/public-register/project/1146',
 'au': 'https://www.naa.gov.au/help-your-research/fact-sheets/australian-flag',
 'in': 'https://knowindia.india.gov.in/my-india-my-pride/indian-tricolor.php',
 'ie': 'https://www.gov.ie/en/department-of-the-taoiseach/publications/the-national-flag/',
 'prc': 'https://www.chnmuseum.cn/zp/zpml/gshww/201812/t20181218_28794.shtml',
 'tib': 'https://tibetmuseum.org/tibetan-national-flag/',
 'dan': 'https://edukacja.ipn.gov.pl/edu/materialy-edukacyjne/infografiki-historyczn/ii-rzeczpospolita/140545,Wolne-Miasto-Gdansk.html',
}

# Real titles discovered through the Commons API and existing credited manifest.
# source=None means the linked file description supports the design window;
# this is distinct from a primary legal instrument confirming an adoption day.
ROWS = [
 ('DEU', 'Flag of Germany (3-2 aspect ratio).svg', '1920-01-01', '1932-12-31', 'de', 'República de Weimar; negro, rojo y oro.'),
 ('DEU', 'Flag of the German Empire.svg', '1933-12-31', '1934-12-31', None, 'Negro, blanco y rojo; coexistió con la bandera con esvástica en1933–1935. La ficha muestra un símbolo, no niega ese uso simultáneo.'),
 ('DEU', 'Flag of Germany (1935–1945).svg', '1935-12-31', '1945-05-08', None, 'Bandera nacional nazi. No se prolonga durante la ocupación aliada.'),
 ('DEU', 'Flag of Germany.svg', '1949-05-23', '1949-12-31', None, 'República Federal de Alemania; no se proyecta sobre1945–1948.'),
 ('DDR', 'Flag of Germany.svg', '1949-10-07', '1949-12-31', None, 'La RDA utiliza inicialmente el tricolor sin el emblema añadido en1959.'),
 ('ESP', 'Flag of Spain (1785–1873, 1875–1931).svg', '1920-01-01', '1930-12-31', None, 'Monarquía de AlfonsoXIII; diseño con escudo real.'),
 ('ESP', 'Flag of Spain (1931–1939).svg', '1931-12-31', '1938-12-31', 'es', 'Segunda República; no identifica al bando sublevado.'),
 ('ESP', 'Flag of Spain (1938–1945).svg', '1939-04-01', '1945-10-10', 'es', 'Diseño franquista tras la victoria; no es bandera de la España republicana.'),
 ('ESP', 'Flag of Spain (1945–1977).svg', '1945-10-11', '1949-12-31', 'es', 'Reglamento de1945; conservar la variante posterior fuera de esta ampliación.'),
 ('ESP-REPUBLIC', 'Flag of Spain (1931–1939).svg', '1936-01-01', '1939-03-31', 'es', 'Zona republicana; la ficha no transforma el frente anual en un frente diario.'),
 ('ESP-NATIONALIST', 'Bandera del bando sublevado (1936-1938).svg', '1936-08-29', '1938-02-01', 'es', 'Bicolor con escudo republicano sin corona real; no reutilizar el escudo monárquico como si fuese esta variante.'),
 ('ESP-NATIONALIST', 'Flag of Spain (1938–1945).svg', '1938-02-02', '1939-03-31', 'es', 'Águila de SanJuan en el bando sublevado.'),
 ('ITA', 'Flag of Italy (1861–1946).svg', '1920-01-01', '1945-12-31', 'it', 'Reino de Italia; el símbolo no representa el control de toda Italia durante la guerra.'),
 ('ITA', 'Flag of Italy.svg', '1946-12-31', '1949-12-31', 'it', 'Tricolor republicano sin escudo; el decreto provisional es de19/6/1946.'),
 ('RSI', 'War flag of the Italian Social Republic.svg', '1943-12-31', '1945-04-25', None, 'Bandera DE GUERRA de la República Social Italiana, identificada como tal; no bandera civil ni prueba de geometría independiente.'),
 ('JPN', 'Flag of Japan (1870–1999).svg', '1920-01-01', '1949-12-31', None, 'Variante histórica7:10 y disco desplazado; no se sustituye por el Sol Naciente militar. Durante la ocupación hubo restricciones de exhibición: no equivale a permiso de uso continuo.'),
 ('ROC', 'Flag of China (1912–1928).svg', '1920-01-01', '1927-12-31', None, 'Cinco franjas de la República de China; no bandera imperial ni de la RPC.'),
 ('ROC', 'Flag of the Republic of China.svg', '1928-12-31', '1949-12-31', None, 'República de China: cielo azul, sol blanco y tierra roja. Su uso no supone control efectivo continuo sobre todo el territorio reclamado.'),
 ('TWN', 'Flag of the Republic of China.svg', '1949-12-31', '1949-12-31', None, 'Símbolo de la República de China en Taiwán al cierre1949; no se proyecta sobre el Taiwán japonés de1920–1944.'),
 ('CHN', "Flag of the People's Republic of China.svg", '1949-10-01', '1949-12-31', 'prc', 'RPC proclamada1/10/1949; diseño acordado27/9. No retrotraer a los soviets chinos anteriores.'),
 ('RSR', 'Flag of the Russian Soviet Federative Socialist Republic (1918–1925).svg', '1920-01-01', '1922-12-29', None, 'Rusia soviética anterior a la URSS; la inscripción RSFSR no se cambia por el símbolo de1954.'),
 ('USSR', 'Flag of the Soviet Union (1924–1936).svg', '1924-12-31', '1935-12-31', None, 'Variante temprana de martillo, hoz y estrella; faltan pruebas suficientes para dar por usado el proyecto con escudo central de1922–1923.'),
 ('USSR', 'Flag of the Soviet Union (1936 – 1955).svg', '1936-12-31', '1949-12-31', None, 'Variante documental1936–1955; se conserva la serie acreditada posterior a1949.'),
 ('GBR', 'Flag of the United Kingdom.svg', '1920-01-01', '1949-12-31', None, 'Union Flag; las colonias sólo la muestran como símbolo del administrador cuando la relación está documentada.'),
 ('CAN', 'Flag of Canada (1868–1921).svg', '1920-01-01', '1921-12-31', 'ca', 'Red Ensign anterior a las nuevas armas; uso en tierra no equivale a bandera nacional legal exclusiva.'),
 ('CAN', 'Flag of Canada (1921–1957).svg', '1922-12-31', '1949-12-31', 'ca', 'El archivo se titula1921, pero el Gobernador General fecha su introducción en1922. Se conserva la divergencia, sin afirmar día exacto. El UnionJack seguía siendo bandera nacional.'),
 ('AUS', 'Flag of Australia (converted).svg', '1920-01-01', '1949-12-31', 'au', 'Commonwealth Blue Ensign con estrella de siete puntas desde1908; no se afirma que la declaración legal de1954 ya hubiese ocurrido.'),
 ('NZL', 'Flag of New Zealand.svg', '1920-01-01', '1949-12-31', None, 'Blue Ensign de NuevaZelanda; la continuidad gráfica no equivale a independencia jurídica plena durante toda la ventana.'),
 ('ZAF', 'Red Ensign of South Africa (1912–1951).svg', '1920-01-01', '1927-12-31', None, 'Enseña roja de Sudáfrica empleada como símbolo nacional; no la bandera nacional de1928.'),
 ('ZAF', 'Flag of South Africa (1928–1994).svg', '1928-12-31', '1949-12-31', None, 'Bandera de la Unión de Sudáfrica de1928, con tres pequeñas banderas.'),
 ('IND', 'British Raj Red Ensign.svg', '1920-01-01', '1946-12-31', None, 'Enseña del Raj británico, identificada como símbolo colonial; no una bandera nacional india moderna.'),
 ('IND', 'Flag of India.svg', '1947-08-15', '1949-12-31', 'in', 'Dominio de India desde15/8/1947; la Asamblea adoptó el diseño22/7/1947, no1946.'),
 ('PAK', 'Flag of Pakistan.svg', '1947-08-14', '1949-12-31', None, 'Pakistán independiente; no símbolo retroactivo de las provincias del Raj.'),
 ('MMR', 'Flag of Burma (1948–1974).svg', '1948-01-04', '1949-12-31', None, 'Unión de Birmania desde la independencia.'),
 ('LKA', 'Flag of Ceylon (1948–1951).svg', '1948-02-04', '1949-12-31', None, 'Dominio de Ceilán; no usar antes las bandas laterales introducidas en1951.'),
 ('IDN', 'Flag of Indonesia.svg', '1945-08-17', '1949-12-31', None, 'República proclamada17/8/1945; no confundir proclamación, reconocimiento neerlandés de1949 y control efectivo de cada isla.'),
 ('IRL', 'Flag of Ireland.svg', '1922-12-31', '1936-12-31', 'ie', 'Estado Libre Irlandés: el Gobierno irlandés acredita su uso desde1922.'),
 ('IRL', 'Flag of Ireland.svg', '1937-12-29', '1949-12-31', 'ie', 'Constitución de1937, artículo7; cambio institucional sin cambio de tricolor.'),
 ('FRA', 'Flag of France (1794–1815, 1830–1974).svg', '1920-01-01', '1949-12-31', None, 'Tricolor francés; no se representa la francisca personal de Pétain como bandera nacional.'),
 ('FRA-VICHY', 'Flag of France (1794–1815, 1830–1974).svg', '1940-07-11', '1944-08-20', None, 'El régimen de Vichy conservó el tricolor; la francisca era un emblema y estandarte personal distinto.'),
 ('FRA-FREE', 'Flag of Free France (1940–1944).svg', '1940-07-03', '1944-08-24', None, 'Cruz de Lorena de la FranciaLibre; no se aplica a Vichy ni a toda Francia ocupada.'),
 ('YKM', 'Flag of Yugoslavia (1918–1941).svg', '1920-01-01', '1940-12-31', None, 'Reino de los Serbios,Croatas y Eslovenos, llamado Yugoslavia desde1929; tricolor sin estrella.'),
 ('YKM', 'Flag of Yugoslavia (1918–1941).svg', '1941-01-01', '1945-11-28', None, 'Símbolo del Reino y de su gobierno en el exilio tras la invasión de1941; no acredita control del territorio ocupado. No sustituye a la estrella federal al cierre1945.'),
 ('YUG', 'Flag of SFR Yugoslavia.svg', '1945-11-29', '1949-12-31', None, 'Tricolor federal con estrella; no se asigna a la monarquía interbélica.'),
 ('CROATIA-CLIENT', 'Flag of Independent State of Croatia.svg', '1941-04-10', '1945-05-08', None, 'Estado Independiente de Croacia, régimen cliente; no bandera de Croacia contemporánea.'),
 ('EGY', 'Flag of Egypt (1882–1922).svg', '1920-01-01', '1921-12-31', None, 'Símbolo del sultanato; la transición de1922 no se convierte en un día de diseño certificado.'),
 ('EGY', 'Flag of Egypt (1922-1958).svg', '1923-12-31', '1949-12-31', None, 'Reino de Egipto: se usa desde el cierre1923, pues el título1922–1958 no demuestra por sí solo adopción del diseño en1922.'),
 ('IRQ', 'Flag of Iraq (1924–1959).svg', '1924-12-31', '1949-12-31', None, 'Monarquía iraquí; comienzo con precisión anual.'),
 ('IRN', 'State flag of Iran (1933–1964).svg', '1933-12-31', '1949-12-31', None, 'Bandera estatal con león y sol; no se atribuye la variante a años anteriores.'),
 ('SAU', 'Flag of Saudi Arabia (1938–1973).svg', '1938-12-31', '1949-12-31', None, 'Diseño histórico con espada; no se retrotrae a reinos saudíes predecesores.'),
 ('YMK', 'Flag of the Mutawakkilite Kingdom of Yemen.svg', '1927-12-31', '1949-12-31', None, 'Reino de Yemen, diseño con cinco estrellas; no se retrotrae a su diseño rojo anterior.'),
 ('POL', 'Flag of Poland (1919–1928).svg', '1920-01-01', '1927-12-31', None, 'Variante de rojo anterior a1928; no reconstruye banderas de administraciones ocupantes.'),
 ('POL', 'Flag of Poland (1928–1980).svg', '1928-12-31', '1949-12-31', None, 'Símbolo polaco que también identifica autoridades en el exilio; no acredita Estado polaco independiente en cada polígono de1939–1944.'),
 ('HUN', 'Flag of Hungary (1915-1918, 1919-1946).svg', '1920-01-01', '1945-12-31', None, 'Escudo coronado del reino; el expediente incluye normas y fotografías históricas.'),
 ('HUN', 'Flag of Hungary (1946-1949, 1956-1957).svg', '1946-12-31', '1948-12-31', None, 'Diseño republicano de Kossuth; no se prolonga al escudo socialista de1949.'),
 ('HUN', 'Flag of Hungary (1949-1956).svg', '1949-12-31', '1949-12-31', None, 'Diseño con escudo socialista al cierre1949.'),
 ('ROU', 'Flag of Romania (1867–1948).svg', '1920-01-01', '1947-12-31', None, 'Tricolor anterior a la incorporación del emblema de la RepúblicaPopular.'),
 ('ROU', 'Flag of Romania (1948–1952).svg', '1948-12-31', '1949-12-31', None, 'Variante al cierre1948; no representa la efímera versión enero–marzo1948.'),
 ('BGR', 'Flag of Bulgaria.svg', '1920-01-01', '1946-12-31', None, 'Tricolor anterior a los emblemas de la RepúblicaPopular.'),
 ('BGR', 'Flag of Bulgaria (1946–1948).svg', '1947-12-31', '1947-12-31', None, 'El título dice1946, pero la descripción del archivo fecha1947–1948: cobertura limitada al cierre1947, sin certificar adopción en1946.'),
 ('BGR', 'Flag of Bulgaria (1948–1967).svg', '1948-12-31', '1949-12-31', None, 'Variante posterior de1948; la versión transitoria titulada1948 no se extiende al cierre del año.'),
 ('CSK', 'Flag of Czechoslovakia.svg', '1920-12-31', '1949-12-31', None, 'Triángulo azul de1920; símbolo de la entidad checoslovaca, incluida su representación en el exilio, no de los ocupantes.'),
 ('USA', 'Flag of the United States (1912-1959).svg', '1920-01-01', '1949-12-31', None, '48 estrellas; no se utiliza el diseño contemporáneo de50.'),
 ('BRA', 'Flag of Brazil (1889–1960).svg', '1920-01-01', '1949-12-31', None, '21 estrellas, anteriores a los cambios de1960.'),
 ('PRY', 'Flag of Paraguay (1842–1954).svg', '1920-01-01', '1949-12-31', None, 'Anverso histórico; Paraguay tiene reverso distinto, que no se representa en esta ficha.'),
 ('THA', 'Flag of Thailand.svg', '1920-01-01', '1949-12-31', None, 'Tricolor de Siam/Tailandia adoptado en1917; no se impone el nombre Tailandia antes de su cambio.'),
 ('NPL', 'Flag of Nepal (1743–1962).svg', '1920-01-01', '1949-12-31', None, 'Variante anterior a la estandarización de1962.'),
 ('DAN', 'Flag of the Free City of Danzig.svg', '1920-11-15', '1939-08-31', 'dan', 'CiudadLibre de Danzig, dos cruces y corona; el archivo cita el Flaggenbuch histórico y advierte variantes de detalle sin estandarización. No usar la bandera municipal contemporánea.'),
 ('TIB', 'Flag of Tibet (1916-1951).svg', '1920-01-01', '1949-12-31', 'tib', 'Ilustración del diseño histórico con leones: el Museo del Tíbet, vinculado a la administración en el exilio, fecha el origen en1916. Su posición política es explícita y no se usa como prueba de reconocimiento internacional. No se emplea la variante discutida1920–1925 ni una bandera autonómica moderna.'),
]

EXCLUDED = [
 {'file': 'Flag of the Soviet Union (1922–1923).svg', 'reason': 'Escudo central: no se ha acreditado que el diseño se fabricase/utilizase como bandera nacional. No basta una reconstrucción publicada en Commons.'},
 {'file': 'Flag of the Soviet Union (1923, unofficial).svg', 'reason': 'El propio archivo lo califica de no oficial y no documenta su final; no usar como símbolo nacional al cierre.'},
 {'key': 'DEU', 'start': '1945-05-09', 'end': '1949-05-22', 'reason': 'Sin bandera nacional alemana inventada durante la ocupación. La enseña marítima C no equivale a una bandera nacional.'},
 {'key': 'CHN-COMMUNIST', 'start': START, 'end': '1949-09-30', 'reason': 'No convertir la bandera de la RPC de1949 en símbolo genérico de todos los soviets/fuerzas comunistas anteriores.'},
]


def source_pages():
    """Fetch real metadata in bounded API batches; cache is documentary evidence."""
    h.CACHE.mkdir(parents=True, exist_ok=True)
    result = {}
    names = list(dict.fromkeys(row[1] for row in ROWS))
    for offset in range(0, len(names), 10):
        requested = names[offset:offset + 10]
        params = dict(action='query', titles='|'.join('File:' + n for n in requested), redirects=1,
                      prop='imageinfo|revisions', iiprop='url|extmetadata', rvprop='content', rvslots='main', format='json')
        url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)
        with urllib.request.urlopen(urllib.request.Request(url, headers=h.UA), timeout=45) as response:
            payload = json.load(response)
        h.save(h.CACHE / f'symbols-1920-sources-{offset // 10}.json', payload)
        pages = {p['title']: p for p in payload.get('query', {}).get('pages', {}).values()}
        redirects = {r['from']: r['to'] for r in payload.get('query', {}).get('redirects', [])}
        redirects.update({r['from']: r['to'] for r in payload.get('query', {}).get('normalized', [])})
        for name in requested:
            title = 'File:' + name
            seen = set()
            while title in redirects and title not in seen:
                seen.add(title)
                title = redirects[title]
            if title in pages:
                result['File:' + name] = pages[title]
    return result


def validate_page(filename, page):
    if not page or not page.get('imageinfo'):
        raise ValueError('Missing source image: ' + filename)
    wiki = page.get('revisions', [{}])[0].get('slots', {}).get('main', {}).get('*', '')
    if not wiki:
        raise ValueError('Missing description/revision; cannot check fictitious designs: ' + filename)
    if re.search(r'\{\{\s*(?:Fictitious flag|Fictional flag|Fictitious)', wiki, re.I):
        raise ValueError('Fictitious/fictional design rejected: ' + filename)
    if re.search(r'\{\{\s*(?:Fact disputed|Disputed|Accuracy)', wiki, re.I):
        raise ValueError('Disputed reconstruction requires additional review: ' + filename)
    meta = page['imageinfo'][0].get('extmetadata', {})
    licence = h.clean(meta.get('LicenseShortName', {}).get('value', ''))
    if not any(value in licence.lower() for value in ['public domain', 'cc0', 'cc by-sa', 'cc-by-sa', 'cc by', 'cc-by']):
        raise ValueError('Unverified licence: ' + filename + ' ' + licence)


def acquire_reusing(filename, pages, existing):
    """Keep original credited bytes, authors, licences and hashes when available."""
    validate_page(filename, pages.get('File:' + filename))
    for media in existing:
        if media['title'] != filename or not media['file'].endswith('.svg'):
            continue
        path = h.OUT / media['file']
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != media['sha256'] or len(raw) != media['bytes']:
            raise ValueError('Existing media integrity mismatch: ' + media['file'])
        if b'<svg' not in raw or re.search(rb'<script|javascript:|\bonload\s*=', raw, re.I):
            raise ValueError('Unsafe existing SVG: ' + media['file'])
        return copy.deepcopy(media), True
    return h.acquire(filename, pages), False


def subtract(flags, start, end):
    """Replace just the reviewed interval, preserving previous/later curations."""
    output = []
    for flag in flags:
        if flag['end'] < start or flag['start'] > end:
            output.append(flag)
            continue
        if flag['start'] < start:
            earlier = copy.deepcopy(flag)
            earlier['end'] = (dt.date.fromisoformat(start) - dt.timedelta(days=1)).isoformat()
            output.append(earlier)
        if flag['end'] > end:
            later = copy.deepcopy(flag)
            later['start'] = (dt.date.fromisoformat(end) + dt.timedelta(days=1)).isoformat()
            output.append(later)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-sources', action='store_true', help='Only metadata/source checks; no writes under public/')
    args = parser.parse_args()
    pages = source_pages()
    rejected, verified = [], []
    for key, filename, start, end, source, note in ROWS:
        try:
            assert START <= start <= end <= END, (key, start, end)
            validate_page(filename, pages.get('File:' + filename))
            verified.append((key, filename, start, end, source, note))
        except Exception as error:
            rejected.append(dict(key=key, file=filename, reason=str(error)))
    audit = dict(mode='source-check' if args.check_sources else 'acquire', tag=TAG,
                 verified=len(verified), proposed=len(ROWS),
                 sources=[dict(key=k, requested=f, canonicalTitle=pages['File:' + f]['title'], start=s, end=e)
                          for k, f, s, e, source, note in verified],
                 accepted=[], rejected=rejected, excluded=EXCLUDED)
    if args.check_sources:
        h.save(h.CACHE / 'symbols-1920-source-audit.json', audit)
        print(json.dumps(audit, ensure_ascii=False, indent=2))
        return 1 if rejected else 0
    # A failed source preflight must not remove valid previously curated flags.
    if rejected:
        h.save(h.CACHE / 'symbols-1920-audit.json', audit)
        raise RuntimeError('Source preflight failed; public identities and manifest were not modified.')
    path = h.OUT / 'data/identities.json'
    manifest_path = h.OUT / 'media/manifest.json'
    data = json.loads(path.read_text(encoding='utf8'))
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    missing = sorted({r[0] for r in verified} - data['countries'].keys())
    if missing:
        raise RuntimeError('Prepare historical identity keys before symbol acquisition: ' + ', '.join(missing))
    existing = manifest['entries']
    media_by_file = {m['file']: m for m in existing}
    acquired = []
    # Finish acquisition before mutating any identity. Unrelated portraits never change.
    for key, filename, start, end, source, note in verified:
        media, reused = acquire_reusing(filename, pages, existing)
        acquired.append((key, media, start, end, source, note))
        media_by_file[media['file']] = media
        audit['accepted'].append(dict(key=key, requested=filename, file=media['file'], start=start, end=end, reused=reused))
        print('Reused' if reused else 'Acquired', key, filename, flush=True)
    for country in data['countries'].values():
        country['flags'] = [f for f in country['flags'] if f.get('acquisition') != TAG]
    for key, media, start, end, source, note in acquired:
        country = data['countries'][key]
        country['flags'] = subtract(country['flags'], start, end)
        country['flags'].append(dict(start=start, end=end, media=media, source=media['url'],
                                     acquisition=TAG, intervalSource=SOURCES.get(source, media['url']), note=ANNUAL + note))
    # Explicitly remove misleading importer ranges, also on repeat runs.
    for country in ['DEU']:
        data['countries'][country]['flags'] = subtract(data['countries'][country]['flags'], '1945-05-09', '1949-05-22')
    data['countries']['CHN']['flags'] = subtract(data['countries']['CHN']['flags'], START, '1949-09-30')
    if 'CHN-COMMUNIST' in data['countries']:
        data['countries']['CHN-COMMUNIST']['flags'] = subtract(data['countries']['CHN-COMMUNIST']['flags'], START, '1949-09-30')
    data['countries']['TWN']['flags'] = subtract(data['countries']['TWN']['flags'], START, '1949-12-30')
    for flag in data['countries']['IND']['flags']:
        if flag['media']['title'] == 'Flag of India.svg' and flag['start'] < '1947-07-22':
            flag['start'] = '1947-07-22'
            flag['note'] = 'Diseño adoptado22/7/1947 por la Asamblea Constituyente;1946 era una fecha errónea. ' + flag.get('note', '')
    # The broad former title1924–1955 redirects today to a1936 design; do not
    # preserve an unreviewed fragment of that generic record in1923/early1924.
    data['countries']['USSR']['flags'] = subtract(data['countries']['USSR']['flags'], '1922-12-30', '1924-12-30')
    for country in data['countries'].values():
        country['flags'].sort(key=lambda f: (f['start'], f['end'], f['media']['title']))
    h.save(path, data)
    manifest['entries'] = sorted(media_by_file.values(), key=lambda m: m['file'])
    h.save(manifest_path, manifest)
    h.save(h.CACHE / 'symbols-1920-audit.json', audit)
    print(f"{len(acquired)} windows; {sum(a['reused'] for a in audit['accepted'])} reused SVG references; no portraits changed.", flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
