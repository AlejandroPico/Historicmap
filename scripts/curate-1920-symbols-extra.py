"""Additional conservative1920–1949 symbol windows; no generated artwork.

--check-sources writes only metadata/audit cache. Normal invocation reuses
credited local SVGs and the established acquire helper, then updates identities.
Run after the principal1920 symbol curator. This module is safe to import.
"""
import argparse
import copy
import importlib.util
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('symbols1920base', ROOT / 'scripts/curate-1920-symbols.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
h = base.h
TAG = 'curated-symbols-1920-extra-0.11'
PREFIX = 'symbols-1920-extra'
SOURCES = {
 'mx': 'https://www.archivos.gob.mx/transparencia/pdf/SimbolosPatrios.pdf',
 'hn': 'https://dnh.gob.hn/diario/de-franjas-azules-y-blancas-a-cinco-estrellas-asi-nacio-la-bandera-de-honduras',
 'ni': 'https://www.mined.gob.ni/fiestas-patrias/2024/07/29/el-significado-del-escudo-nacional/',
 'ec': 'https://www.presidencia.gob.ec/presidencia-de-la-republica-conmemorara-el-dia-de-la-bandera-nacional/',
 'ar': 'https://www.argentina.gob.ar/pais/simbolos/bandera',
 'lu': 'https://sip.gouvernement.lu/dam-assets/publications/brochure-livre/minist-etat/sip/brochure/a-propos/A_propos_Symboles/A_propos_Symboles_de_l_Etat_et_de_la_nation.pdf',
 'gr': 'https://www.presidency.gr/en/presidency/the-flag/',
 'lt': 'https://www.lrs.lt/pls/inter/w5_show?p_b=3804&p_d=49324&p_k=2&p_r=4056',
}
ROWS = [
 ('MEX','Flag of Mexico (1916–1934).svg','1920-01-01','1933-12-31','mx','Diseño del águila de perfil del periodo1916–1934, acreditado por el Archivo General de la Nación. No se retrotrae el modelo de1934 ni el escudo de1968.'),
 ('MEX','Flag of Mexico (1934-1968).svg','1934-12-31','1949-12-31','mx','Familia del escudo estandarizado en1934; extremo inicial anual, no día exacto del decreto ni certificación de tonos digitales históricos.'),
 ('HND','Flag of Honduras (1890s yellow star variant).svg','1920-01-01','1948-12-31','hn','Variante histórica de uso con estrellas doradas, descrita por el Diario Nacional hondureño para1898–1949. No se presenta como única bandera legal: las normas anteriores hablaban de estrellas azules y hubo falta de uniformidad.'),
 ('HND','Flag of Honduras (1949–2022, 2026–present).svg','1949-12-31','1949-12-31','hn','Diseño de cinco estrellas azules al cierre1949; no se proyecta sobre los años anteriores. Los tonos digitales no equivalen a la normalización material uniforme de todas las banderas.'),
 ('NIC','Flag of Nicaragua (1908–1971).svg','1920-01-01','1949-12-31','ni','Diseño anterior a la regulación detallada de1971. El Ministerio de Educación fecha el decreto de origen en5/9/1908; no confundir el número1908 del decreto de1971 con su año.'),
 ('VEN','Flag of Venezuela (1905–1930).svg','1920-01-01','1929-12-31',None,'Variante nacional/civil con siete estrellas en círculo, anterior a su disposición en arco. No se usa el diseño de ocho estrellas de2006 ni se afirma que esta imagen incluya el escudo de la bandera estatal.'),
 ('VEN','Flag of Venezuela (1930–2006).svg','1930-12-31','1949-12-31',None,'Variante nacional/civil con siete estrellas en arco; el emblema estatal con escudo tenía usos distintos. La ventana no aplica la reforma heráldica de1954 ni las ocho estrellas de2006.'),
 ('ECU','Flag of Ecuador.svg','1920-01-01','1949-12-31','ec','Familia estatal con escudo y franja amarilla doble, regulada en1900. Es una representación gráfica del símbolo; no certifica que los detalles de la ilustración digital estuviesen normalizados en1920.'),
 ('ARG','Flag of Argentina.svg','1920-01-01','1949-12-31','ar','Bandera mayor/oficial con Sol de Mayo, incorporado en1818. Antes de1985 el uso civil sin sol se distinguía del estatal/militar; no se proyecta retroactivamente la libertad de uso general ni los parámetros técnicos de2010.'),
 ('LUX','Flag of Luxembourg.svg','1920-01-01','1949-12-31','lu','Tricolor histórico rojo-blanco-azul. La definición/protección legal de1972 y cromática posterior son distintas de su uso anterior: no se afirma adopción en1920 ni normalización Pantone de esa época. El símbolo de la nación no acredita libertad de exhibición durante la ocupación alemana.'),
 ('GRC','Flag of Greece (1822-1978).svg','1920-01-01','1949-12-31','gr','Bandera terrestre/civil de cruz blanca sobre azul. No es el estandarte real ni una reconstrucción de las insignias de cada ejército o marina; la bandera nacional rayada actual no se impone a todos los usos anteriores.'),
 ('LTU','Flag of Lithuania (1918–1940).svg','1920-01-01','1939-12-31','lt','Tricolor interbélico separado del SVG contemporáneo y de las banderas de la RSS. Termina antes de las ocupaciones de1940; no resuelve símbolos del exilio ni de las administraciones ocupantes.'),
 ('ALB','Flag of Albania (1926–1928).svg','1926-12-31','1927-12-31',None,'Familia republicana documentada en el archivo para1926–1928. No se certifica un cambio diario en1926.'),
 ('ALB','Flag of Albania (1928–1934).svg','1928-12-31','1933-12-31',None,'Variante monárquica de la familia1928–1934; no se transforma el nombre del archivo en un instrumento legal de adopción.'),
 ('ALB','Flag of Albania (1934–1939).svg','1934-12-31','1938-12-31',None,'Variante monárquica posterior, sin prolongarla a la ocupación italiana. La descripción también alude a la familia1928–1939: el corte1934 es documental, pendiente de contraste normativo.'),
 ('ALB','Flag of Albania (1939–1943).svg','1939-12-31','1942-12-31',None,'Símbolo del reino bajo ocupación/protectorado italiano con fasces. No se presenta como símbolo de soberanía plena ni se le aplica automáticamente al control alemán posterior.'),
 ('ALB','Flag of Albania (1943–1944).svg','1943-12-31','1943-12-31',None,'Variante de la autoridad albanesa bajo ocupación alemana, acreditada al cierre1943. No se certifica aquí el día del relevo comunista de1944 ni control de cada localidad.'),
 ('ALB','Flag of Albania (1944–1946).svg','1944-12-31','1945-12-31',None,'Diseño provisional con hoz y martillo de la etapa comunista, separado del diseño con estrella de1946. Inicio al cierre anual; no día de adopción acreditado.'),
]
EXCLUDED = [
 dict(key='LTU',start='1940-01-01',end='1949-12-31',reason='No rellenar las ocupaciones con el tricolor de la República interbélica ni con el diseño contemporáneo de2004.'),
 dict(key='ALB',reason='La curación documenta familias y ventanas, no normalización exhaustiva de cada águila, corona, fasces o día de transición.'),
]


def source_pages():
    h.CACHE.mkdir(parents=True, exist_ok=True)
    names = list(dict.fromkeys(row[1] for row in ROWS))
    result = {}
    for offset in range(0, len(names), 10):
        requested = names[offset:offset + 10]
        params = dict(action='query',titles='|'.join('File:' + n for n in requested),redirects=1,
                      prop='imageinfo|revisions',iiprop='url|extmetadata',rvprop='content',rvslots='main',format='json')
        with urllib.request.urlopen(urllib.request.Request('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params),headers=h.UA),timeout=45) as response:
            payload = json.load(response)
        h.save(h.CACHE / f'{PREFIX}-sources-{offset // 10}.json', payload)
        query = payload.get('query', {})
        pages = {p['title']: p for p in query.get('pages', {}).values()}
        redirects = {r['from']:r['to'] for r in query.get('redirects', []) + query.get('normalized', [])}
        for name in requested:
            title, seen = 'File:' + name, set()
            while title in redirects and title not in seen:
                seen.add(title)
                title = redirects[title]
            if title in pages:
                result['File:' + name] = pages[title]
    return result


def curate(incoming, acquired):
    """Pure catalogue application, separable from acquisition for isolated checks."""
    data = copy.deepcopy(incoming)
    for country in data['countries'].values():
        country['flags'] = [f for f in country['flags'] if f.get('acquisition') != TAG]
    for key, media, start, end, source, note in acquired:
        flags = base.subtract(data['countries'][key]['flags'], start, end)
        flags.append(dict(start=start,end=end,media=media,source=media['url'],acquisition=TAG,
                          intervalSource=SOURCES.get(source,media['url']),note=base.ANNUAL + note))
        data['countries'][key]['flags'] = flags
    for country in data['countries'].values():
        country['flags'].sort(key=lambda f:(f['start'],f['end'],f['media']['title']))
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-sources',action='store_true')
    args = parser.parse_args()
    pages = source_pages()
    rejected = []
    for key, filename, start, end, source, note in ROWS:
        try:
            assert base.START <= start <= end <= base.END
            base.validate_page(filename,pages.get('File:' + filename))
        except Exception as error:
            rejected.append(dict(key=key,file=filename,reason=str(error)))
    audit = dict(tag=TAG,proposed=len(ROWS),verified=len(ROWS)-len(rejected),accepted=[],rejected=rejected,
                 excluded=EXCLUDED,mode='source-check' if args.check_sources else 'acquire',
                 sources=[dict(key=k,requested=f,canonicalTitle=pages.get('File:' + f,{}).get('title'),start=s,end=e)
                          for k,f,s,e,source,note in ROWS])
    if args.check_sources or rejected:
        h.save(h.CACHE / (PREFIX + '-source-audit.json'),audit)
        print(json.dumps(audit,ensure_ascii=False,indent=2))
        return 1 if rejected else 0
    path, manifest_path = h.OUT / 'data/identities.json', h.OUT / 'media/manifest.json'
    incoming = json.loads(path.read_text(encoding='utf8'))
    missing = {r[0] for r in ROWS} - incoming['countries'].keys()
    if missing:
        raise ValueError('Missing identities: ' + ', '.join(sorted(missing)))
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    media_by_file, acquired = {m['file']:m for m in manifest['entries']}, []
    # Do not touch identities until every acquisition has succeeded.
    for key, filename, start, end, source, note in ROWS:
        media, reused = base.acquire_reusing(filename,pages,list(media_by_file.values()))
        media_by_file[media['file']] = media
        acquired.append((key,media,start,end,source,note))
        audit['accepted'].append(dict(key=key,requested=filename,file=media['file'],start=start,end=end,reused=reused))
        print('Reused' if reused else 'Acquired',key,filename,flush=True)
    h.save(path,curate(incoming,acquired))
    manifest['entries'] = sorted(media_by_file.values(),key=lambda m:m['file'])
    h.save(manifest_path,manifest)
    h.save(h.CACHE / (PREFIX + '-audit.json'),audit)
    print(f'{len(acquired)} additional documentary windows; no portraits changed.',flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
