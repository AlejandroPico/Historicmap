# Símbolos documentados · 1920–1949

Investigación del 24/10/2026 para 0.11. Preparador: `scripts/curate-1920-symbols.py`. **69 ventanas propuestas, 47 claves**, no 69 países ni un catálogo mundial exhaustivo. Los metadatos de los 69 registros superaron la consulta real de Commons: imagen existente, revisión de descripción, licencia admitida y ausencia de marcas de diseño ficticio o reconstrucción discutida. Esto acredita archivos y procedencia; no equivale a confirmar exhaustivamente cada adopción legal.

Al redactar este documento el preparador **no se ha ejecutado contra `public/`**. Se verificaron sintaxis y una ejecución aislada de las 69 ventanas en un directorio temporal, con adquisición simulada para los archivos nuevos: repetición idéntica, dirigentes conservados y selección de símbolos de todos los años 1950–2026 sin cambios. La prueba reutilizó 51 referencias a SVG reales del inventario anterior; las 18 referencias restantes representan 17 archivos distintos potencialmente nuevos. La adquisición real, sus cantidades y cualquier rechazo se deben registrar en la entrega y en el informe que produzca el responsable; no confundir esta comprobación con archivos ya descargados.

## Método y ejecución

1. Preparar primero las identidades históricas RSR, ROC, YKM, RSI, DAN y TIB y las curaciones generales. Este script no crea autoridades, entidades ni fronteras.
2. `python -X utf8 scripts/curate-1920-symbols.py --check-sources` consulta sólo metadatos y escribe `.cache/identities/symbols-1920-sources-*.json` y `symbols-1920-source-audit.json`; no escribe bajo `public/`.
3. La ejecución sin esa opción adquiere las ventanas. Primero comprueba todas las fuentes y las claves; después adquiere todos los símbolos, y sólo entonces modifica identidades y manifiesto. Ante un fallo de fuente no elimina curaciones anteriores. El resultado queda en `.cache/identities/symbols-1920-audit.json`.
4. Cuando encuentra un SVG local con el mismo título, comprueba SHA-256, bytes y seguridad del SVG y conserva íntegro su registro de autoría, licencia y atribución. Para archivos nuevos llama a `acquire` de `curate-1970-symbols.py`: conserva sus comprobaciones, créditos, licencia y huella. No altera fotografías ni el horizonte contemporáneo de adquisición.
5. Sustituye únicamente intervalos revisados y conserva los fragmentos anteriores/posteriores. La etiqueta `curated-symbols-0.11` permite repetir la curación. Conserva la selección de símbolos posterior a1949; debe ejecutarse después de importadores genéricos que puedan reintroducir diseños erróneos.

Los extremos como `1928-12-31` son ventanas documentales para el cierre anual. No se afirman como días de adopción. Cuando un texto primario aporta un día concreto se conserva el hecho y se distingue de la ventana de cobertura. La bandera identifica a una entidad o autoridad: su presencia no demuestra control sobre cada punto de una geometría, independencia plena ni reconocimiento internacional. Colonias y dependencias necesitan relaciones administrativas documentadas; no reciben automáticamente banderas nacionales de su independencia posterior.

## Fuentes y discrepancias focales

- **Alemania:** [Bundestag, artículo3 de la Constitución de Weimar](https://www.bundestag.de/dokumente/textarchiv/1919-07-03-schwarz-rot-gold-649430) confirma negro-rojo-oro y distingue la enseña mercante. El tricolor imperial coexistió con la esvástica en1933–1935; el símbolo único de la ficha no agota esa coexistencia. Entre9/5/1945 y22/5/1949 se retira cualquier bandera nacional alemana genérica. La señal marítima C de la ocupación no se presenta como bandera nacional. RFA y RDA reciben tricolor sin emblema en1949; el emblema de la RDA corresponde a1959.
- **España:** [Gaceta de28/4/1931, decreto del27](https://www.boe.es/gazeta/dias/1931/04/28/pdfs/GMD-1931-118.pdf) y [Constitución de1931, artículo1](https://www.congreso.es/constitucion/ficheros/historicas/cons_1931.pdf) documentan el tricolor republicano. [Moncloa](https://www.lamoncloa.gob.es/lang/en/espana/statesymbols/paginas/index.aspx) distingue restauración bicolor de29/8/1936 y reglamento de11/10/1945. La nueva imagen real `Bandera del bando sublevado (1936-1938).svg` evita conservar la corona real de la bandera anterior a1931 como si fuese el diseño con escudo republicano empleado por el bando sublevado. La variante de1938 y la de1945 permanecen separadas.
- **Italia:** el [Archivio Centrale dello Stato](https://acs.cultura.gov.it/festa-del-tricolore-2022/) publica el decreto provisional de19/6/1946 y recuerda la norma monárquica de1925. Se distinguen Reino y República. RSI incorpora una **bandera de guerra**, explícitamente rotulada: el [propio archivo](https://commons.wikimedia.org/wiki/File:War_flag_of_the_Italian_Social_Republic.svg) distingue ese uso del tricolor civil. Incorporarla al registro no crea un frente del norte de Italia ni un polígono de RSI.
- **Canadá y otros dominios:** el [Gobernador General](https://www.gg.ca/en/heraldry/public-register/project/1146) sitúa la introducción del Red Ensign con las nuevas armas en1922, mientras [Canadian Heritage](https://www.canada.ca/en/canadian-heritage/services/flag-canada-history.html) y el título del archivo usan1921. Se conserva la variante antigua al cierre1921 y se limita la siguiente desde el cierre1922; no se resuelve la divergencia mediante una fecha diaria inventada. El Red Ensign era un símbolo reconocido y la Union Flag seguía siendo bandera nacional. Los [Archivos Nacionales de Australia](https://www.naa.gov.au/help-your-research/fact-sheets/australian-flag) acreditan la estrella de siete puntas desde1908 y distinguen la declaración legal posterior de1954 del uso anterior del Blue Ensign.
- **India:** [portal del Gobierno](https://knowindia.india.gov.in/my-india-my-pride/indian-tricolor.php): diseño adoptado22/7/1947, uso del Dominio desde15/8/1947. Se corrige el comienzo genérico erróneo de1946. Las enseñas del Raj no se presentan como una bandera nacional de India o Pakistán independientes. Ceilán1948 usa el león sin las bandas de1951; Birmania1948 conserva su diseño anterior a1974.
- **Irlanda:** el [Departamento del Taoiseach](https://www.gov.ie/en/department-of-the-taoiseach/publications/the-national-flag/) distingue uso por el Estado Libre desde1922 y confirmación constitucional en1937. Son dos ventanas institucionales del mismo tricolor; no se inventa un cambio gráfico en1937.
- **China:** el archivo real de [cinco franjas1912–1928](https://commons.wikimedia.org/wiki/File:Flag_of_China_(1912%E2%80%931928).svg) se asigna a ROC, seguido por el diseño de cielo azul y sol blanco. TWN no recibe una bandera de la República de China antes de su ventana separada al cierre1949. El [Museo Nacional de China](https://www.chnmuseum.cn/zp/zpml/gshww/201812/t20181218_28794.shtml) documenta acuerdo de27/9/1949 y ceremonia de1/10; la RPC no se proyecta sobre1920–1948 ni sobre todos los soviets chinos anteriores. El diseño no resuelve los frentes de la guerra civil.
- **Rusia y URSS:** RSR utiliza el archivo con inscripción de la RSFSR, separado de la URSS fundada30/12/1922. La variante soviética1924–1936 tiene expediente de licencia y remite a normativa histórica; se separa del diseño1936–1955. El título antes adquirido `Flag of the Soviet Union (1924–1955).svg` redirige ahora al archivo1936–1955, de modo que no se usa esa redirección como prueba de una imagen válida para todo1923–1935. Las referencias locales y créditos anteriores se preservan fuera de las ventanas reemplazadas.
- **Yugoslavia:** YKM conserva el tricolor monárquico, con la etapa del gobierno en el exilio explícita desde1941; YUG usa la estrella federal al cierre1945. El nombre Reino de los Serbios,Croatas y Eslovenos antes de1929 no exige cambiar la imagen. Croacia cliente permanece separada de la Croacia actual.
- **Danzig:** el [IPN polaco](https://edukacja.ipn.gov.pl/edu/materialy-edukacyjne/infografiki-historyczn/ii-rzeczpospolita/140545,Wolne-Miasto-Gdansk.html) documenta la CiudadLibre desde15/11/1920; su bandera tiene dos cruces y corona. El [archivo de Commons](https://commons.wikimedia.org/wiki/File:Flag_of_the_Free_City_of_Danzig.svg) cita el Flaggenbuch histórico y advierte que existían diferencias de detalle. La ventana termina antes de la invasión de septiembre1939; no se traslada la bandera municipal contemporánea al pasado.
- **Tíbet:** el [Museo del Tíbet](https://tibetmuseum.org/tibetan-national-flag/), ligado a la administración en el exilio, fecha el diseño en1916. Es fuente primaria de su propia tradición simbólica y posición política; sus afirmaciones de reconocimiento no se adoptan como conclusión del atlas. Se usa la ilustración histórica [1916–1951](https://commons.wikimedia.org/wiki/File:Flag_of_Tibet_(1916-1951).svg), sin fijar colores normalizados en1920. El archivo alternativo1920–1925 lleva marca `Fact disputed` y queda excluido, al igual que el diseño ficticio anterior a1912.

Para las demás ventanas, la descripción de Commons acredita la familia gráfica y su licencia; no se presenta como un instrumento primario de adopción. Los días no contrastados y las variantes de detalle continúan pendientes. Los títulos históricos ya adquiridos pueden tener redirecciones actuales: se conservan sus bytes locales acreditados, sin reemplazarlos silenciosamente por la última revisión de otro título.

## Exclusiones y huecos que se conservan

- URSS1922–1923 con escudo central: no se ha acreditado uso material como bandera nacional. El diseño de1923 descrito como no oficial tampoco aporta una ventana nacional al cierre. No se rellena ese hueco con un proyecto reconstruido.
- Alemania durante la ocupación1945–1948: sin bandera nacional inventada. Faltan símbolos/administraciones individuales de las zonas y sectores de Berlín.
- Fuerzas comunistas chinas anteriores a octubre1949: no reciben por herencia la bandera de la RPC. Faltan variantes de soviets y fuerzas concretas.
- Egipto1922: el título1922–1958 no basta para acreditar el día o año de cambio del diseño verde; comienza al cierre1923 y deja1922 pendiente.
- Días exactos de reformas de Polonia1928, Hungría1946/1949, Bulgaria1947/1948 y otras transiciones anuales; no transformar sus extremos de cobertura en adopciones legales.
- Protectorados, dominios, colonias y regímenes no incluidos, banderas durante ocupaciones, variantes militares y civiles, AND/SMR y representaciones de cambios internos de1939–1945 siguen necesitando investigación. Este inventario no amplía geometrías ni crea frentes.

## Ventanas propuestas

Las fechas siguientes son límites inclusivos de cobertura para el preparador. La nota completa de cada fila se conserva en el script y en la identidad preparada tras su ejecución.

| Clave | Cobertura | Archivo acreditado |
|---|---|---|
| DEU | 1920-01-01 — 1932-12-31 | [Flag of Germany (3-2 aspect ratio).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Germany_(3-2_aspect_ratio).svg) |
| DEU | 1933-12-31 — 1934-12-31 | [Flag of the German Empire.svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_German_Empire.svg) |
| DEU | 1935-12-31 — 1945-05-08 | [Flag of Germany (1935–1945).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Germany_(1935%E2%80%931945).svg) |
| DEU | 1949-05-23 — 1949-12-31 | [Flag of Germany.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Germany.svg) |
| DDR | 1949-10-07 — 1949-12-31 | [Flag of Germany.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Germany.svg) |
| ESP | 1920-01-01 — 1930-12-31 | [Flag of Spain (1785–1873, 1875–1931).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Spain_(1785%E2%80%931873%2C_1875%E2%80%931931).svg) |
| ESP | 1931-12-31 — 1938-12-31 | [Flag of Spain (1931–1939).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Spain_(1931%E2%80%931939).svg) |
| ESP | 1939-04-01 — 1945-10-10 | [Flag of Spain (1938–1945).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Spain_(1938%E2%80%931945).svg) |
| ESP | 1945-10-11 — 1949-12-31 | [Flag of Spain (1945–1977).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Spain_(1945%E2%80%931977).svg) |
| ESP-REPUBLIC | 1936-01-01 — 1939-03-31 | [Flag of Spain (1931–1939).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Spain_(1931%E2%80%931939).svg) |
| ESP-NATIONALIST | 1936-08-29 — 1938-02-01 | [Bandera del bando sublevado (1936-1938).svg](https://commons.wikimedia.org/wiki/File:Bandera_del_bando_sublevado_(1936-1938).svg) |
| ESP-NATIONALIST | 1938-02-02 — 1939-03-31 | [Flag of Spain (1938–1945).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Spain_(1938%E2%80%931945).svg) |
| ITA | 1920-01-01 — 1945-12-31 | [Flag of Italy (1861–1946).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Italy_(1861%E2%80%931946).svg) |
| ITA | 1946-12-31 — 1949-12-31 | [Flag of Italy.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Italy.svg) |
| RSI | 1943-12-31 — 1945-04-25 | [War flag of the Italian Social Republic.svg](https://commons.wikimedia.org/wiki/File:War_flag_of_the_Italian_Social_Republic.svg) |
| JPN | 1920-01-01 — 1949-12-31 | [Flag of Japan (1870–1999).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Japan_(1870%E2%80%931999).svg) |
| ROC | 1920-01-01 — 1927-12-31 | [Flag of China (1912–1928).svg](https://commons.wikimedia.org/wiki/File:Flag_of_China_(1912%E2%80%931928).svg) |
| ROC | 1928-12-31 — 1949-12-31 | [Flag of the Republic of China.svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_Republic_of_China.svg) |
| TWN | 1949-12-31 — 1949-12-31 | [Flag of the Republic of China.svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_Republic_of_China.svg) |
| CHN | 1949-10-01 — 1949-12-31 | [Flag of the People's Republic of China.svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_People%27s_Republic_of_China.svg) |
| RSR | 1920-01-01 — 1922-12-29 | [Flag of the Russian Soviet Federative Socialist Republic (1918–1925).svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_Russian_Soviet_Federative_Socialist_Republic_(1918%E2%80%931925).svg) |
| USSR | 1924-12-31 — 1935-12-31 | [Flag of the Soviet Union (1924–1936).svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_Soviet_Union_(1924%E2%80%931936).svg) |
| USSR | 1936-12-31 — 1949-12-31 | [Flag of the Soviet Union (1936 – 1955).svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_Soviet_Union_(1936_%E2%80%93_1955).svg) |
| GBR | 1920-01-01 — 1949-12-31 | [Flag of the United Kingdom.svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_United_Kingdom.svg) |
| CAN | 1920-01-01 — 1921-12-31 | [Flag of Canada (1868–1921).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Canada_(1868%E2%80%931921).svg) |
| CAN | 1922-12-31 — 1949-12-31 | [Flag of Canada (1921–1957).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Canada_(1921%E2%80%931957).svg) |
| AUS | 1920-01-01 — 1949-12-31 | [Flag of Australia (converted).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Australia_(converted).svg) |
| NZL | 1920-01-01 — 1949-12-31 | [Flag of New Zealand.svg](https://commons.wikimedia.org/wiki/File:Flag_of_New_Zealand.svg) |
| ZAF | 1920-01-01 — 1927-12-31 | [Red Ensign of South Africa (1912–1951).svg](https://commons.wikimedia.org/wiki/File:Red_Ensign_of_South_Africa_(1912%E2%80%931951).svg) |
| ZAF | 1928-12-31 — 1949-12-31 | [Flag of South Africa (1928–1994).svg](https://commons.wikimedia.org/wiki/File:Flag_of_South_Africa_(1928%E2%80%931994).svg) |
| IND | 1920-01-01 — 1946-12-31 | [British Raj Red Ensign.svg](https://commons.wikimedia.org/wiki/File:British_Raj_Red_Ensign.svg) |
| IND | 1947-08-15 — 1949-12-31 | [Flag of India.svg](https://commons.wikimedia.org/wiki/File:Flag_of_India.svg) |
| PAK | 1947-08-14 — 1949-12-31 | [Flag of Pakistan.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Pakistan.svg) |
| MMR | 1948-01-04 — 1949-12-31 | [Flag of Burma (1948–1974).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Burma_(1948%E2%80%931974).svg) |
| LKA | 1948-02-04 — 1949-12-31 | [Flag of Ceylon (1948–1951).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Ceylon_(1948%E2%80%931951).svg) |
| IDN | 1945-08-17 — 1949-12-31 | [Flag of Indonesia.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Indonesia.svg) |
| IRL | 1922-12-31 — 1936-12-31 | [Flag of Ireland.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Ireland.svg) |
| IRL | 1937-12-29 — 1949-12-31 | [Flag of Ireland.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Ireland.svg) |
| FRA | 1920-01-01 — 1949-12-31 | [Flag of France (1794–1815, 1830–1974).svg](https://commons.wikimedia.org/wiki/File:Flag_of_France_(1794%E2%80%931815%2C_1830%E2%80%931974).svg) |
| FRA-VICHY | 1940-07-11 — 1944-08-20 | [Flag of France (1794–1815, 1830–1974).svg](https://commons.wikimedia.org/wiki/File:Flag_of_France_(1794%E2%80%931815%2C_1830%E2%80%931974).svg) |
| FRA-FREE | 1940-07-03 — 1944-08-24 | [Flag of Free France (1940–1944).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Free_France_(1940%E2%80%931944).svg) |
| YKM | 1920-01-01 — 1940-12-31 | [Flag of Yugoslavia (1918–1941).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Yugoslavia_(1918%E2%80%931941).svg) |
| YKM | 1941-01-01 — 1945-11-28 | [Flag of Yugoslavia (1918–1941).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Yugoslavia_(1918%E2%80%931941).svg) |
| YUG | 1945-11-29 — 1949-12-31 | [Flag of SFR Yugoslavia.svg](https://commons.wikimedia.org/wiki/File:Flag_of_SFR_Yugoslavia.svg) |
| CROATIA-CLIENT | 1941-04-10 — 1945-05-08 | [Flag of Independent State of Croatia.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Independent_State_of_Croatia.svg) |
| EGY | 1920-01-01 — 1921-12-31 | [Flag of Egypt (1882–1922).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Egypt_(1882%E2%80%931922).svg) |
| EGY | 1923-12-31 — 1949-12-31 | [Flag of Egypt (1922-1958).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Egypt_(1922-1958).svg) |
| IRQ | 1924-12-31 — 1949-12-31 | [Flag of Iraq (1924–1959).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Iraq_(1924%E2%80%931959).svg) |
| IRN | 1933-12-31 — 1949-12-31 | [State flag of Iran (1933–1964).svg](https://commons.wikimedia.org/wiki/File:State_flag_of_Iran_(1933%E2%80%931964).svg) |
| SAU | 1938-12-31 — 1949-12-31 | [Flag of Saudi Arabia (1938–1973).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Saudi_Arabia_(1938%E2%80%931973).svg) |
| YMK | 1927-12-31 — 1949-12-31 | [Flag of the Mutawakkilite Kingdom of Yemen.svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_Mutawakkilite_Kingdom_of_Yemen.svg) |
| POL | 1920-01-01 — 1927-12-31 | [Flag of Poland (1919–1928).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Poland_(1919%E2%80%931928).svg) |
| POL | 1928-12-31 — 1949-12-31 | [Flag of Poland (1928–1980).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Poland_(1928%E2%80%931980).svg) |
| HUN | 1920-01-01 — 1945-12-31 | [Flag of Hungary (1915-1918, 1919-1946).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Hungary_(1915-1918%2C_1919-1946).svg) |
| HUN | 1946-12-31 — 1948-12-31 | [Flag of Hungary (1946-1949, 1956-1957).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Hungary_(1946-1949%2C_1956-1957).svg) |
| HUN | 1949-12-31 — 1949-12-31 | [Flag of Hungary (1949-1956).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Hungary_(1949-1956).svg) |
| ROU | 1920-01-01 — 1947-12-31 | [Flag of Romania (1867–1948).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Romania_(1867%E2%80%931948).svg) |
| ROU | 1948-12-31 — 1949-12-31 | [Flag of Romania (1948–1952).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Romania_(1948%E2%80%931952).svg) |
| BGR | 1920-01-01 — 1946-12-31 | [Flag of Bulgaria.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Bulgaria.svg) |
| BGR | 1947-12-31 — 1947-12-31 | [Flag of Bulgaria (1946–1948).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Bulgaria_(1946%E2%80%931948).svg) |
| BGR | 1948-12-31 — 1949-12-31 | [Flag of Bulgaria (1948–1967).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Bulgaria_(1948%E2%80%931967).svg) |
| CSK | 1920-12-31 — 1949-12-31 | [Flag of Czechoslovakia.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Czechoslovakia.svg) |
| USA | 1920-01-01 — 1949-12-31 | [Flag of the United States (1912-1959).svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_United_States_(1912-1959).svg) |
| BRA | 1920-01-01 — 1949-12-31 | [Flag of Brazil (1889–1960).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Brazil_(1889%E2%80%931960).svg) |
| PRY | 1920-01-01 — 1949-12-31 | [Flag of Paraguay (1842–1954).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Paraguay_(1842%E2%80%931954).svg) |
| THA | 1920-01-01 — 1949-12-31 | [Flag of Thailand.svg](https://commons.wikimedia.org/wiki/File:Flag_of_Thailand.svg) |
| NPL | 1920-01-01 — 1949-12-31 | [Flag of Nepal (1743–1962).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Nepal_(1743%E2%80%931962).svg) |
| DAN | 1920-11-15 — 1939-08-31 | [Flag of the Free City of Danzig.svg](https://commons.wikimedia.org/wiki/File:Flag_of_the_Free_City_of_Danzig.svg) |
| TIB | 1920-01-01 — 1949-12-31 | [Flag of Tibet (1916-1951).svg](https://commons.wikimedia.org/wiki/File:Flag_of_Tibet_(1916-1951).svg) |


## Integración en0.11.0

Aplicado al catálogo público local por el responsable de integración el24/10/2026, después de comprobar la repetibilidad y conservar los retratos. El estado «no aplicado» de la preparación aislada describe el relevo inicial, no la entrega final. Resultados efectivos, adquisición de medios y límites conjuntos en [DELIVERY-0.11.0](DELIVERY-0.11.0.md) y [REVIEW-1920-1949.json](REVIEW-1920-1949.json). Publicación pendiente del aviso del propietario.
