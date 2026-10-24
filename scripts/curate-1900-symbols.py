"""Conservative1900–1919 symbol windows, with unchanged licensed Commons SVGs.

--check-sources only writes metadata/audit cache; normal execution applies after
historical identities have been prepared. Does not alter1920+ symbols, portraits,
the contemporary retrieval horizon, geometries or the missing imperial CSV.
"""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('symbol_engine1900', ROOT / 'scripts/curate-1920-symbols-extra.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
TAG = 'curated-symbols-1900-0.12'
FIRST, LAST = '1900-01-01', '1919-12-31'
SOURCES = {
 **engine.SOURCES,
 'ru': 'https://www.prlib.ru/node/659469',
 'rpr': 'https://ivarh.ru/vse-novosti-i-publikacii/den-flaga-1223',
 'au': 'https://www.naa.gov.au/help-your-research/fact-sheets/australian-flag',
 'nz': 'https://nzhistory.govt.nz/page/new-zealand-flag-confirmed',
 'ca': 'https://www.canada.ca/en/canadian-heritage/services/flag-canada-history.html',
 'no': 'https://www.stortinget.no/no/Stortinget-og-demokratiet/Historikk/stortinget-og-unionen-med-sverige/i-unionen/det-rene-norske-handelsflagget/',
 'se': 'https://www.nordiskamuseet.se/utforska/hogtider/sveriges-nationaldag/',
 'pt': 'https://www.presidencia.pt/presidente-da-republica/a-presidencia/simbolos-nacionais/',
 'fi': 'https://finland.fi/facts-stats-and-info/the-finnish-flag/',
 'cz': 'https://vlada.gov.cz/assets/clenove-vlady/historie-minulych-vlad/historie-statni-vlajky/sedlacek-symboly-katalog_1.pdf',
 'de': 'https://www.bundestag.de/dokumente/textarchiv/1919-07-03-schwarz-rot-gold-649430',
 'th': 'https://www.thailand.go.th/page/flag',
}

# Exact file titles were discovered/checked with the Commons API. Annual-close
# dates are coverage boundaries, not fabricated days of legal adoption.
ROWS = [
 ('CFS','Flag of the Congo Free State.svg','1900-01-01','1908-11-14',None,'Campo azul con estrella dorada central, anterior a la anexión belga. La declaración original de1884 se reproduce en Belgian Congo, Foreign Office, apéndiceI; la imagen no acredita legitimidad del régimen ni una costa histórica exacta.'),
 ('COD','Flag of the Congo Free State.svg','1908-11-15','1919-12-31',None,'Símbolo territorial delCongoBelga, conservado tras la transferencia de1908; no es bandera delEstado belga ni delCongo independiente de1960.'),
 ('TON','Flag of Tonga.svg','1900-01-01','1919-12-31',None,'Símbolo propio de la monarquía tongana; el acuerdo británico de protección de1900 no convirtió al monarca británico en rey deTonga.'),
 ('RUE','Flag of Russia.svg','1900-01-01','1917-03-14','ru','Tricolor blanco-azul-rojo del Imperio, confirmado como nacional en1896. No se sustituye por el estandarte del zar ni por el distintivo de uso privado de1914. Los tonos digitales ilustran la familia; no equivalen a una norma Pantone imperial.'),
 ('RPR','Flag of Russia.svg','1917-03-15','1917-11-07','rpr','Tricolor conservado durante elGobiernoProvisional, separado delestandarte zarista; no se inventa un nuevo decreto de adopción. Antes de la proclamación republicana de14/9/1917 se identifica elGobiernoProvisional, sin retrotraer elnombreRepúblicaRusa ni prolongar elImperio. Fechasgregorianas coordinadas con laidentidad deautoridades.'),
 ('RSR','Flag of the Russian Soviet Federative Socialist Republic (1918–1925).svg','1918-12-31','1919-12-31',None,'Diseño RSFSR documentado en1918. No se proyectan el símbolo soviético de1924 ni la variante rusa de1954 sobre1917–1919.'),
 ('QING','Flag of China (1889–1912).svg','1900-01-01','1911-12-31',None,'Dragón de la dinastía Qing, diseño rectangular histórico. No bandera de la RPC ni de la República de China. La ventana no pretende fijar un frente diario de la revolución1911.'),
 ('ROC','Flag of China (1912–1928).svg','1912-12-31','1919-12-31',None,'Cinco franjas republicanas; no se usa el cielo azul/sol blanco adoptado como bandera nacional en1928. La restauración imperial breve de1917 no se convierte en continuidad jurídica del imperio.'),
 ('AUT-HUN','Ensign of Austro-Hungarian civil fleet (1869-1918).svg','1900-01-01','1918-11-02',None,'PABELLÓN MERCANTE común de la monarquía dual, no bandera nacional única inventada ni estandarte del emperador. Archivo distinto de las reconstrucciones marcadasInaccurate. Su uso no hace de Austria y Hungría un único sistema interno de Gobierno.'),
 ('OTT','Flag of the Ottoman Empire (1844–1922).svg','1900-01-01','1919-12-31',None,'Media luna y estrella de cinco puntas del periodo otomano; el archivo cita fotografías contemporáneas. No se equipara este diseño a la normalización geométrica republicana de1936 ni al estandarte personal del sultán.'),
 ('DEU','Flag of the German Empire.svg','1900-01-01','1918-12-31',None,'Negro-blanco-rojo del periodo imperial, conservado en la transición anterior a la definición de los nuevos colores en1919. Mostrar esta familia gráfica al cierre1918 no prolonga la monarquía después de noviembre.'),
 ('DEU','Flag of Germany (3-2 aspect ratio).svg','1919-12-31','1919-12-31','de','Negro-rojo-oro de Weimar al cierre1919; no una enseña mercante negro-blanco-roja ni bandera nazi posterior.'),
 ('GBR','Flag of the United Kingdom.svg','1900-01-01','1919-12-31',None,'Union Flag de1801: la sucesión Victoria/EduardoVII/JorgeV no exige cambiarla por un estandarte real. Las colonias sólo la reciben como símbolo de administrador mediante relación documentada.'),
 ('CAN','Flag of Canada (1868–1921).svg','1900-01-01','1919-12-31','ca','Red Ensign anterior a las nuevas armas de1921/1922. Uso representativo en tierra, sin afirmar que fuese la única bandera nacional legal: también se utilizaba la Union Flag.'),
 ('AUS','Flag of Australia (1901–1903).svg','1901-12-31','1902-12-31','au','Diseño inicial del Commonwealth Blue Ensign: estrella federal de seis puntas y estrellas de la Cruz del Sur de varias puntas. No se proyecta sobre1900, anterior a la federación.'),
 ('AUS','Flag of Australia (1903–1908).svg','1903-12-31','1907-12-31','au','Cruz del Sur simplificada y estrella federal aún de seis puntas; distinto del modelo de siete puntas posterior.'),
 ('AUS','Flag of Australia (converted).svg','1908-12-31','1919-12-31','au','Commonwealth Blue Ensign con estrella federal de siete puntas. No se afirma que su declaración legal como bandera nacional de1954 ya estuviese en vigor.'),
 ('NZL','Flag of the United Kingdom.svg','1900-01-01','1901-12-31','nz','Bandera legal en tierra anterior a1902. Coexistían enseñas marítimas locales; el disco blanco de señales no se impone como única bandera nacional.'),
 ('NZL','Flag of New Zealand.svg','1902-12-31','1919-12-31','nz','Blue Ensign con estrellas rojas bordeadas de blanco: proclamación y especificaciones de junio1902. No se asigna al año1900 la redistribución de estrellas de1902.'),
 ('IND','British Raj Red Ensign.svg','1900-01-01','1919-12-31',None,'Enseña colonial del Raj, identificada como tal; no tricolor del Congreso ni bandera nacional de la India independiente.'),
 ('FRA','Flag of France (1794–1815, 1830–1974).svg','1900-01-01','1919-12-31',None,'Tricolor francés de la Tercera República; puede representar al administrador de colonias documentadas, sin inventarles símbolos nacionales independientes.'),
 ('ESP','Flag of Spain (1785–1873, 1875–1931).svg','1900-01-01','1919-12-31',None,'Diseño con escudo monárquico, anterior a la Segunda República y a la dictadura deFranco.'),
 ('ITA','Flag of Italy (1861–1946).svg','1900-01-01','1919-12-31',None,'Reino de Italia con escudo deSaboya; no se utiliza el tricolor republicano sin escudo de1946.'),
 ('JPN','Flag of Japan (1870–1999).svg','1900-01-01','1919-12-31',None,'Variante histórica7:10 delHinomaru, distinta de la enseña militar delSolNaciente.'),
 ('PRT','Flag of Portugal (1830–1910).svg','1900-01-01','1910-10-04',None,'Bandera monárquica azul-blanca de uso terrestre; no se usa el verde-rojo republicano antes de la revolución.'),
 ('PRT','Flag of Portugal (official).svg','1910-12-31','1919-12-31','pt','Diseño republicano aprobado29/11/1910 y ratificado19/6/1911. El cierre1910 no convierte la ratificación posterior en un hecho anterior.'),
 ('BEL','Flag of Belgium.svg','1900-01-01','1919-12-31',None,'Tricolor belga; no convierte al EstadoLibre delCongo, patrimonio separado deLeopoldoII hasta1908, en colonia delEstado belga antes de esa transferencia.'),
 ('NLD','Flag of the Netherlands.svg','1900-01-01','1919-12-31',None,'Familia histórica rojo-blanco-azul delReino. La ilustración no afirma una estandarización cromática contemporánea en1900.'),
 ('SWE','Swedish civil ensign (1844–1905).svg','1900-01-01','1904-12-31','no','Enseña civil/mercante sueca con marca de unión; no se sustituye por el estandarte de mando ni por el pabellón militar de tres puntas.'),
 ('SWE','Flag of Sweden (pre-1906).svg','1905-12-31','1905-12-31','no','Cruz sueca sin marca de unión al cierre1905, tras la disolución. No se afirma uniformidad de todos los usos durante el año.'),
 ('SWE','Flag of Sweden.svg','1906-12-31','1919-12-31','se','Familia regulada por la ley de1906, separada de los colores/proporciones anteriores.'),
 ('NOR','Flag of Norway.svg','1900-01-01','1919-12-31','no','Bandera civil sin marca de unión, legal desde15/12/1899. La marina conservó su marca hasta1905; este símbolo no implica independencia noruega en1900.'),
 ('FIN','Flag of Finland.svg','1918-12-31','1919-12-31','fi','Bandera civil de cruz azul desde1918. No se extiende alGranDucado ruso ni se reemplaza su uso inicial de bandera roja con león en1917.'),
 ('LTU','Flag of Lithuania (1918–1940).svg','1918-12-31','1919-12-31','lt','Tricolor interbélico desde la nueva entidad de1918; no versión soviética ni normalización digital de2004.'),
 ('POL','Flag of Poland (1919–1928).svg','1919-12-31','1919-12-31',None,'Blanco-rojo de laRepública al cierre1919; no se retrotrae a las particiones imperiales anteriores.'),
 ('CSK','Flag of Bohemia.svg','1918-12-31','1919-12-31','cz','Bicolor blanco-rojo usado por la nuevaChecoslovaquia, gráficamente coincidente con la enseña bohemia. El triángulo azul se aprobó30/3/1920 y no se proyecta sobre1918–1919.'),
 ('HUN','Flag of Hungary (1896-1915).svg','1900-01-01','1914-12-31',None,'Símbolo de la parte húngara de la monarquía dual, con su escudo propio. No acredita independencia plena ni es una bandera nacional única deAustria-Hungría.'),
 ('HUN','Flag of Hungary (1915-1918, 1919-1946).svg','1915-12-31','1917-12-31',None,'Variante coronada de1915, anterior al final de la monarquía en1918.'),
 ('HUN','Flag of Hungary (1918–1919).svg','1918-12-31','1918-12-31',None,'Variante de laRepública al cierre1918; no se transforma en símbolo continuo del régimen soviético de1919.'),
 ('HUN','Flag of Hungary (1915-1918, 1919-1946).svg','1919-12-31','1919-12-31',None,'Variante coronada readoptada tras el final de laRepúblicaSoviética en1919; el símbolo del cierre no representa todos los Gobiernos del año.'),
 ('AUT','Flag of Austria.svg','1919-12-31','1919-12-31',None,'Rojo-blanco-rojo de laAustria republicana al cierre1919, no pabellón de todos los territorios de la antigua monarquía.'),
 ('ROU','Flag of Romania (1867–1948).svg','1900-01-01','1919-12-31',None,'Tricolor de laRumanía monárquica anterior a los emblemas socialistas de1948.'),
 ('BGR','Flag of Bulgaria.svg','1900-01-01','1919-12-31',None,'Familia de tricolor blanco-verde-rojo anterior a laRepúblicaPopular. El cambio de principado a reino no impone el emblema socialista posterior.'),
 ('SRK','Flag of Serbia (1882–1918).svg','1900-01-01','1918-11-30',None,'Símbolo delReino deSerbia. El ejercicio en el exilio durante laocupación no equivale al control de cada punto del territorio.'),
 ('MNK','Flag of Montenegro (1905–1918, 1941–1944).svg','1905-12-31','1918-11-25',None,'Tricolor nacional/civil montenegrino. No se usa el archivo1905–1918 con armas que describe en realidad la bandera delrey; el símbolo no acredita control durante laocupación.'),
 ('YKM','Flag of Yugoslavia (1918–1941).svg','1918-12-31','1919-12-31',None,'Reino de losSerbios,Croatas yEslovenos, anterior al nombreYugoslavia de1929. Tricolor sin estrella; no símbolo socialista.'),
 ('KEM','Flag of Korea (1899).svg','1900-01-01','1909-12-31',None,'Ilustración delTaegeukgi de laépoca imperial, basada enFlags of Maritime Nations1899,atlasnaval contemporáneo. Existían variantes y no se impone la normalización surcoreana de1949; no se extiende a laanexión japonesa de1910.'),
 ('GRC','Flag of Greece (1822-1978).svg','1900-01-01','1919-12-31','gr','Bandera terrestre/civil de cruzblanca sobreazul; no equivale alestandarte real ni a todos lospabellones navales y militares.'),
 ('LUX','Flag of Luxembourg.svg','1900-01-01','1919-12-31','lu','Tricolor histórico, sin afirmar que la protección legal de1972 o la definición cromática posterior existieran ya en1900.'),
 ('USA','Flag of the United States (1896-1908).svg','1900-01-01','1907-12-31',None,'45estrellas; no se usa la bandera contemporánea de50.'),
 ('USA','Flag of the United States (1908-1912).svg','1908-12-31','1911-12-31',None,'46estrellas al cierre1908; la ventana no afirma adopción el31de diciembre.'),
 ('USA','Flag of the United States (1912-1959).svg','1912-12-31','1919-12-31',None,'48estrellas, antes de la incorporación deAlaska yHawái.'),
 ('MEX','Flag of Mexico (1893–1916).svg','1900-01-01','1915-12-31',None,'Águila frontal anterior al modelo carrancista de perfil; no escudo de1934 o1968.'),
 ('MEX','Flag of Mexico (1916–1934).svg','1916-12-31','1919-12-31','mx','Diseño carrancista de perfil de1916, separado del modelo anterior. No es una bandera imperial mexicana.'),
 ('NIC','Flag of Nicaragua (1896–1908).svg','1900-01-01','1907-12-31',None,'Diseño anterior al decreto de1908, con las características descritas por su expediente histórico deCommons.'),
 ('NIC','Flag of Nicaragua (1908–1971).svg','1908-12-31','1919-12-31','ni','Diseño originado en1908; no se interpreta el decreto número1908 de1971 como si su número fuese el año de adopción.'),
 ('ARG','Flag of Argentina.svg','1900-01-01','1919-12-31','ar','Bandera mayor/oficial conSoldeMayo desde1818. La libertad de uso civil de1985 y los parámetros técnicos de2010 no se proyectan hacia1900.'),
 ('ECU','Civil flag and ensign of Ecuador.svg','1900-01-01','1900-10-30','ec','Tricolor sin escudo anterior a laregulación de1900, identificado como enseña civil. La ventana se detiene antes de la nueva regulación.'),
 ('ECU','Flag of Ecuador.svg','1900-12-31','1919-12-31','ec','Familia estatal conescudo yamarillo doble al cierre1900; no afirma normalización digital retrospectiva de cada detalle de lailustración.'),
 ('VEN','Flag of Venezuela (1863–1905).svg','1900-01-01','1904-12-31',None,'Sieteestrellas anteriores a ladisposición en círculo del diseño de1905. Variante nacional/civil sin atribuirle elescudo de la estatal.'),
 ('VEN','Flag of Venezuela (1905–1930).svg','1905-12-31','1919-12-31',None,'Sieteestrellas en círculo; no arco de1930, reforma heráldica de1954 ni ochoestrellas de2006.'),
 ('HND','Flag of Honduras (1890s yellow star variant).svg','1900-01-01','1919-12-31','hn','Variante histórica deuso conestrellas doradas, sin afirmar exclusividad legal: la legislación anterior hablaba deestrellas azules y hubo faltadeuniformidad.'),
 ('PRY','Flag of Paraguay (1842–1954).svg','1900-01-01','1919-12-31',None,'Anverso histórico; Paraguaytiene un reverso distinto que esta ficha no representa.'),
 ('BRA','Flag of Brazil (1889–1960).svg','1900-01-01','1919-12-31',None,'Diseño republicano con21estrellas, anterior a los cambios de1960.'),
 ('CUB','Flag of Cuba.svg','1902-12-31','1919-12-31',None,'Familia de laCuba republicana desde1902; no se asigna por esta fila a la administración estadounidense de1900–1901.'),
 ('LBR','Flag of Liberia.svg','1900-01-01','1919-12-31',None,'Familia histórica liberiana conunaestrella; no variante de la bandera estadounidense de45/46/48estrellas.'),
 ('ETH','Flag of Ethiopia (1897–1974).svg','1900-01-01','1919-12-31',None,'Estandarte imperial conLeóndeJudá, identificado como tal; no se afirma que fuese la única variante nacional/civil. El expediente remite a un ejemplar delBritishMuseum; no acredita uniformidad material de cada ilustración del león.'),
 ('EGY','Flag of Egypt (1882–1922).svg','1900-01-01','1919-12-31',None,'Enseña egipcia delperiodo deljedivato y sultanato, anterior a la bandera verde delReino. No se usa el águila republicana de1952.'),
 ('AFG','Flag of Afghanistan (1880–1901).svg','1900-01-01','1900-12-31',None,'Diseño de laetapa deAbdurRahman; no se proyectan variantes republicanas o talibanes posteriores.'),
 ('AFG','Flag of Afghanistan (1901–1919).svg','1901-12-31','1918-12-31',None,'Familia deHabibullah, con su emblema histórico; el título yla descripción delimitan diseño, no un censo devariantes materiales.'),
 ('AFG','Flag of Afghanistan (1909–1926).svg','1919-12-31','1919-12-31',None,'El título dice1909–1926, pero la descripción inglesa delarchivo acredita1919–1921. Se limita al cierre1919; no se transforma el título en uso anterior a1919 ni en día de adopción.'),
 ('IRN','State flag of Persia (1907–1933).svg','1907-12-31','1919-12-31',None,'Bandera estatal persa conleón ysol en laetapa constitucional; no se retrotrae la reforma de1933 ni el emblema de1980.'),
 ('NPL','Flag of Nepal (1743–1962).svg','1900-01-01','1919-12-31',None,'Familia nepalí anterior a laestandarización de1962.'),
 ('THA','Flag of Siam (1855).svg','1900-01-01','1915-12-31',None,'Elefante blanco sobrecampo rojo delSiam anterior a lasfranjas; no es la enseña naval contemporánea usada como bandera nacional retrospectiva.'),
 ('THA','Flag of Siam (1916).svg','1916-12-31','1916-12-31',None,'Diseño de cincofranjas rojas yblancas de laetapa transitoria de1916, antes de labanda azul. No resuelve la coexistencia del elefante en todos los usos.'),
 ('THA','Flag of Thailand.svg','1917-12-31','1919-12-31','th','Tricolor deSiam desde1917, anterior alnombreTailandia. No se certifican tonos digitales actuales como parámetros técnicos de1917.'),
]

EXCLUDED = [
 dict(file='Civil Ensign of Austria-Hungary (1869–1918).svg',reason='Commons marcaInaccurate porcoronas yproporciones; se usa otro archivo mercante acreditado, no se recrea el escudo.'),
 dict(file='Civil ensign of Austria-Hungary (1869-1918).svg',reason='También marcadoInaccurate; no se confunde con el título alternativo seleccionado.'),
 dict(file='Flag of Russia (1896–1918).svg',reason='MarcadoInaccurate porazul históricamente discutido; se usa representación geométrica deltricolor con fuente institucional y nota de límites.'),
 dict(key='KEM',start='1910-01-01',end=LAST,reason='No proyectar Taegeukgi nacional delImperio sobre elcontrol/anexión japonesa; símbolos de laresistencia requieren registros propios.'),
 dict(key='MNK',start=FIRST,end='1905-12-30',reason='Los archivos disponibles anteriores a1905 describen banderas militares/personales; no se presentan como bandera nacional general.'),
 dict(key='RSR',start='1917-11-08',end='1918-12-30',reason='No inventar una bandera nacional soviética para todos los cierres de1917: el diseño coninscripción se incorpora desde la ventana documental delcierre1918, no desde la creación delSovnarkom.'),
 dict(key='CSK',file='Flag of Czechoslovakia.svg',start='1918-01-01',end=LAST,reason='Retirar delintervalo1900–1919 la importación genérica deltriánguloazul adoptado en1920, conservando los registros posteriores.'),
]


# Reuse the proven bounded engine without editing older preparers or their data.
# Its mutable module configuration is private to this import; no public writes
# occur until main() is explicitly called without --check-sources.
engine.ROWS, engine.SOURCES, engine.EXCLUDED = ROWS, SOURCES, EXCLUDED
engine.TAG, engine.PREFIX = TAG, 'symbols-1900'
engine.base.START, engine.base.END = FIRST, LAST
engine.__doc__ = __doc__
original_validate = engine.base.validate_page


def validate_page(filename, page):
    original_validate(filename, page)
    wiki = page.get('revisions', [{}])[0].get('slots', {}).get('main', {}).get('*', '')
    if re.search(r'\{\{\s*Inaccurate\b', wiki, re.I):
        raise ValueError('Historically inaccurate reconstruction requires review: ' + filename)


engine.base.validate_page = validate_page
source_pages = engine.source_pages
original_curate = engine.curate


def curate(incoming, acquired):
    data = original_curate(incoming, acquired)
    # The earlier generic source associated the later blue triangle with the
    # state founded1918. Correct that known anachronism without touching1920+.
    if 'CSK' in data['countries']:
        corrected = []
        for flag in data['countries']['CSK']['flags']:
            if flag['media']['title'] in ['Flag of Czechoslovakia.svg', 'Flag of the Czech Republic.svg']:
                corrected.extend(engine.base.subtract([flag], FIRST, LAST))
            else:
                corrected.append(flag)
        data['countries']['CSK']['flags'] = sorted(corrected,key=lambda f:(f['start'],f['end'],f['media']['title']))
    return data


engine.curate = curate


if __name__ == '__main__':
    raise SystemExit(engine.main())
