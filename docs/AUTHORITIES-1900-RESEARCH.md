# Autoridades imperiales y transiciones, 1900–1919 · revisión 0.12

Investigación focal preparada el 24 de octubre de 2026. Su complemento es `scripts/curate-1900-authorities.py`; no sustituye al inventario mundial adquirido. El curador no ha sido ejecutado sobre datos públicos por el investigador. La integración, la comparación de 1920+ y la prueba de idempotencia corresponden al proceso principal.

## Identidades acordadas

| Clave de ficha | Wikidata | Alcance |
| --- | --- | --- |
| RUE | [Q34266](https://www.wikidata.org/wiki/Q34266) | Imperio ruso; Nicolás II termina con su abdicación de marzo de 1917. |
| RPR | [Q139319](https://www.wikidata.org/wiki/Q139319) | Gobierno Provisional / República Rusa. Antes del 14 de septiembre de 1917 se dice Gobierno Provisional, pues la proclamación republicana es posterior. |
| RSR | Q2184, existente | Gobierno soviético ruso desde noviembre de 1917; no hereda autoridades de la Federación Rusa contemporánea. |
| AUT-HUN | [Q28513](https://www.wikidata.org/wiki/Q28513) | Soberano de Austria-Hungría; código de organizaciones AUH. No se crea otra ficha AUH. |
| OTT | [Q12560](https://www.wikidata.org/wiki/Q12560) | Sultanato otomano y, con rótulos expresos, autoridades rivales de Ankara. |
| QING | [Q8733](https://www.wikidata.org/wiki/Q8733) | Dinastía Qing; código de organizaciones QNG. Restauración de Pekín de julio de 1917 con alcance limitado. |
| ROC | Q13426199, existente | República de China; se reutiliza la serie septentrional adquirida en TWN, sin autoridades de la RPC. |

Los identificadores de personas se comprobaron mediante páginas de Wikidata y fuentes institucionales; no se dedujeron por aproximación numérica. Las dos claves `COLLECTIVE-*` representan órganos y deliberadamente no simulan QID de persona ni retrato individual.

## Rusia: tres fases y dos calendarios

Todos los valores almacenados de 1917 son gregorianos. El desfase con el calendario juliano usado en las actas rusas es de trece días.

* Nicolás II, Q40787: ventana desde 1900 hasta el 15 de marzo de 1917. El [acta original de abdicación en el archivo ruso](https://lenin.rusarchives.ru/fevralskaya-revolyuciya-v-rossii) está fechada el 2 de marzo juliano. La muerte de 1918 no prolonga el reinado. La aceptación condicionada de Miguel no se convierte en un reinado efectivo inventado.
* Gueorgui Lvov, Q297032: Gobierno Provisional, 15 de marzo–20 de julio de 1917; Aleksandr Kerenski, Q48211: 21 de julio–7 de noviembre. El [GARF sobre la crisis de julio](https://statearchive.ru/1016) distingue dimisión de Lvov el 7 de julio juliano, sucesión y reorganización ministerial. La [Biblioteca Presidencial, con texto del decreto republicano](https://www.prlib.ru/history/619540), fecha la República el 1/14 de septiembre y el derrocamiento el 25 de octubre/7 de noviembre.
* Lenin, Q1394: presidente del Sovnarkom desde el 8 de noviembre de 1917 hasta el límite documental de 1919. El [decreto original de creación del Gobierno](https://lenin.rusarchives.ru/node/977) es del 26 de octubre/8 de noviembre y su publicación del día siguiente. La toma del poder, la designación gubernamental y la Constitución de 1918 son hitos distintos.

Por decisión de integración, la ficha anual RSR de 1917 también recibe copias de las ventanas de Nicolás, Lvov y Kerenski dentro de ese año. Sus cargos empiezan por «Autoridad predecesora» y dicen expresamente que no integraron el Gobierno soviético. Es una solución de acceso anual a los cambios, no una asignación de esos hombres a la entidad soviética. No se copian banderas entre las tres identidades.

## Austria-Hungría y sus sucesores

Francisco José I, Q51056, se conserva hasta su muerte el 21 de noviembre de 1916; Carlos I/IV, Q51068, le sucede. La institución museística [Habsburger.net](https://www.habsburger.net/en/persons/habsburg-emperor/franz-joseph-i) documenta al primero, y su [historia de Carlos](https://www.habsburger.net/en/chapter/karl-i-peace-emperor) distingue abandono del ejercicio y abdicación formal.

El [Parlamento austríaco, edición de actas](https://www.parlament.gv.at/dokument/unterlagen/Stenographische_Protokolle_geheime__Sitzungen_Juli1918_gesamt.pdf) recoge las fechas del soberano. El [Archivo Nacional Húngaro conserva la declaración de Eckartsau](https://mnl.gov.hu/a_het_dokumentuma/iv_karoly_eckartsaui_nyilatkozata.html): 13 de noviembre de 1918 para Hungría, dos días después de la declaración austríaca. La disolución territorial tampoco fue un acto simultáneo único. Se ofrece Carlos en AUT para la transición de 1918 y, separadamente, como rey en HUN hasta el 13 de noviembre.

En AUT, el Consejo de Estado y su directorio se representan como órgano colegiado desde el 30 de octubre de 1918; su supresión legal es del 14 de marzo de 1919. El [registro archivístico del Staatsrat](https://www.archivinformationssystem.at/detail.aspx?ID=5464) documenta el órgano y su fin. La [edición documental de la Academia Austríaca](https://austriaca.at/0xc1aa5572_0x004012b8.pdf) distingue a Seitz, Dinghofer y Hauser como presidencia compartida. Queda pendiente precisar la breve sustitución inicial Fink/Hauser; no se inventan días personales para resolverla. El directorio no se presenta como una presidencia individual de Seitz durante todo el intervalo.

Karl Renner, Q11726: primera sesión y juramento del gabinete el 31 de octubre de 1918 según la [edición de protocolos ministeriales](https://austriaca.at/8403-4). El [Landtag de Baja Austria](https://noe-landtag.gv.at/personen/karl_renner) fecha la designación el 30 de octubre y la renovación del cargo el 15 de marzo de 1919. La ventana del curador empieza en el ejercicio documentado, explica la diferencia y no altera su mandato posterior. La presentación editorial de austriaca.at contiene un lapsus «11 October» al mencionar a Carlos: no se adopta esa fecha.

Mihály Károlyi, Q346703: primer ministro desde el encargo del 31 de octubre de 1918 hasta el 10 de enero de 1919; presidente provisional desde el 11 de enero hasta el 21 de marzo. El [Archivo Nacional Húngaro](https://mnl.gov.hu/mnl/tml/az_oszirozsas_forradalom_es_a_tanacskoztarsasag_tolna_megyeben) distingue encargo, formación del gabinete y nueva jefatura. Garbai, Kun y los gobiernos de la segunda mitad de 1919 requieren otra revisión; esta entrega no convierte su ausencia en una vacancia afirmada.

## Alemania: soberanía, órgano revolucionario y gabinete

Guillermo II, Q2677, deja de ejercer el poder el 9 de noviembre de 1918. El [Bundestag](https://www.bundestag.de/dokumente/textarchiv/1918-11-09-revolutionskalender-38-091118-574088) documenta el anuncio unilateral de Max von Baden y la transferencia irregular de la cancillería a Ebert. La firma posterior de abdicación no se confunde con ese cese efectivo.

Max von Baden, Q76908, canciller del 3 de octubre al 9 de noviembre: [biografía del Deutsches Historisches Museum](https://www.dhm.de/lemo/biografie/max-von-baden). El [DHM sobre el Consejo de Representantes del Pueblo](https://www.dhm.de/lemo/kapitel/weimarer-republik/revolution-191819/rat-der-volksbeauftragten) explica su constitución el 10 de noviembre, copresidencia inicial Ebert/Haase y salida de la USPD el 28 de diciembre. Se representa el órgano, no una presidencia nacional personal inventada. La elección de Ebert del 11 de febrero de 1919 y la formación del siguiente gabinete son hechos separados.

Philipp Scheidemann, Q70581, preside el Ministerio del Reich del 13 de febrero al 20 de junio de 1919. Gustav Bauer, Q57159, le sucede el 21 de junio. El [portal de protocolos del Bundesarchiv](https://aktenreichskanzlei.bundesarchiv.de/) y la [carta de nombramiento de Bauer](https://weimar.bundesarchiv.de/WEIMAR/DE/Content/Dokumente-zur-Zeitgeschichte/1919-06-19_ruecktritt_scheidemann.html) permiten distinguir anuncio de dimisión, crisis y sustitución. El [DHM enumera los gabinetes](https://www.dhm.de/lemo/kapitel/weimarer-republik/innenpolitik/kabinette), incluido el cambio del título gubernamental en agosto. No se reescribe aquí toda la serie de cancilleres imperiales.

## Imperio otomano y Ankara

La [guía de los Archivos Estatales, cuadros de sultanes y grandes visires, páginas impresas 523–524](https://www.devletarsivleri.gov.tr/yayinlar/45318a6a-b112-4d50-ac54-e820c07cde79.pdf), sirve de base a Abdülhamid II Q134817, Mehmed V Q151494 y Mehmed VI Q162543. Mehmed V accede el 27 de abril de 1909 y muere el 3 de julio de 1918; el cuadro sitúa la sucesión de Mehmed VI el día 4. No se confunde el poder formal del sultán con el Comité de Unión y Progreso. Talat Paşa, Q315888, se añade como gran visir entre el 4 de febrero de 1917 y el 8 de octubre de 1918 según el mismo cuadro, no como soberano ni dirigente de una república posterior.

Mustafa Kemal, Q5152, aparece en OTT en una ventana desde el cierre del Congreso de Sivas, 11 de septiembre de 1919, como autoridad nacional rival. La [cronología del Ministerio de Defensa](https://ata.msb.gov.tr/Sayfa/SayfaGoster/ataturk-kronolojisi) y los [documentos diplomáticos originales de 1919](https://diad.mfa.gov.tr/diad/kutuphane/100_Yilinda_1919_Arsivimizden_Belgeler_v2024.pdf) acreditan el Comité Representativo. Ese comienzo es documental, no fecha inventada de acceso al cargo.

Excepción de continuidad autorizada para la nueva clave OTT: Mehmed VI alcanza el 1 de noviembre de 1922, fecha de abolición del sultanato; la [cronología institucional de 1922](https://www.ktb.gov.tr/TR-96329/1922.html) distingue este acto de la dimisión del último gabinete el 4 de noviembre. No se modifica TUR. Además se añade a OTT una copia contextual de la presidencia de la Gran Asamblea de Ankara, 24 de abril de 1920–fin documental de 1921; la [lista oficial del Parlamento](https://www.tbmm.gov.tr/baskan/meclis-baskanlari) da su mandato completo hasta el 29 de octubre de 1923. No se le atribuye el sultanato ni una presidencia republicana antes de 1923. La identidad cartográfica de cierre de 1922 debe mostrar el Gobierno de Ankara, no un sultanato vigente.

No se completan todos los grandes visires de 1900–1919 en esta investigación focal; la tabla citada permite una ampliación posterior.

## Qing y República de China

El [Museo del Palacio](https://www.dpm.org.cn/classify_detail/180655.html) fecha la muerte de Guangxu Q299710 el 14 de noviembre de 1908 y la de Cixi Q47842 el día siguiente. Se distinguen soberanía nominal y poder de facto. La [ficha institucional de Puyi Q185152](https://www.dpm.org.cn/court/lineage/226255.html) permite separar sucesión de noviembre, ceremonia de diciembre y nombre de era de 1909.

Zaifeng Q144348, príncipe regente: ventana desde la ceremonia de diciembre de 1908 hasta su renuncia del 6 de diciembre de 1911, documentada en un [estudio del Museo del Palacio](https://img.dpm.org.cn/Uploads/pdf/2824/T00024_00.pdf). El inicio de la ventana no es su anterior designación. Longyu Q1370907 se muestra como autoridad cortesana posterior al retiro del regente; el [texto del Museo con el decreto de abdicación](https://www.dpm.org.cn/Uploads/pdf/6156/T00199_00.pdf) acredita que lo promulgó en nombre del emperador menor el 12 de febrero de 1912. No se inventa una emperatriz reinante.

Para Sun Yat-sen Q8573, el [documento diplomático contemporáneo FRUS 1913, 89](https://history.state.gov/historicaldocuments/frus1913/d89) distingue elección de diciembre de 1911, investidura del 1 de enero de 1912 y relevo por Yuan Shikai Q210329 el 10 de marzo. Los últimos meses Qing coexistieron con el Gobierno de Nankín.

La ficha de Yuan explicita el proyecto Hongxian, sin inventar una coronación consumada ni identificarlo con los Qing. El [despacho FRUS 1916, 73](https://history.state.gov/historicaldocuments/frus1916/d73) transmite la cancelación del proyecto de marzo de 1916. Queda pendiente separar con las actas completas cada fase de su título: la fila actual es una síntesis biográfica del mandato, con esa limitación declarada, no una cronología jurídica diaria resuelta.

La restauración de Puyi en Pekín del 1 al 12 de julio de 1917 se añade a QING y, con ámbito expreso, a la ficha anual ROC. El [despacho contemporáneo FRUS 1917, 128](https://history.state.gov/historicaldocuments/frus1917/d128) documenta su alcance local y la derrota. Los edictos restauracionistas alegaron consentimiento de Li Yuanhong; el mismo conjunto documental recoge su desmentido. No se trata la propaganda del edicto como prueba del consentimiento.

Feng Guozhang Q700576 se encuentra ejerciendo ya el 12 de julio según el [índice de telegramas y despachos contemporáneos](https://history.state.gov/historicaldocuments/frus1917/papers); la confirmación figura el día 9 y la ceremonia en Pekín es posterior. Se usa el 12 como inicio de cobertura documentada, sin pretender que sea una investidura. El relevo de Xu Shichang Q702428 queda en la serie adquirida. Li Yuanhong Q716136 se mantiene como dato adquirido: su final genérico durante la restauración, las ceremonias de Feng y la competencia entre autoridades del norte y sur requieren una revisión posterior más granular. La copia no aumenta la calidad de evidencia de esas filas.

## Japón

Meiji Q174231 y Taishō Q157052 se separan el 30 de julio de 1912, fecha acreditada por la [historia de la Gaceta Oficial de la Oficina Nacional de Impresión](https://www.npb.go.jp/en/products/gazette/books/kanpo_history.html). La entronización ceremonial posterior de Taishō no retrasa su sucesión; la regencia de Hirohito es de 1921, fuera de la ventana focal.

Se conserva la serie de primeros ministros adquirida. La [lista oficial de gabinetes de la Kantei](https://japan.kantei.go.jp/past_cabinet/index.html) permite su contraste; esta entrega no afirma haber resuelto todas las interinidades breves, incluida la de 1901.

## Contrato de integración y comprobaciones

`curate(data)` hace copia profunda de la entrada, no toca archivos y devuelve el resultado. La CLI solo lee y escribe cuando se invoca expresamente; permite `--input` y `--output`. Captura los retratos antes de retirar su propia etiqueta `curated-1900-0.12`, no elimina otras curaciones ni modifica sus banderas. Las correcciones están acotadas por persona y periodo; las filas originales que alcanzan 1920+ se conservan íntegras. Las copias limitadas a 1919 indican fronteras de cobertura. La nueva continuidad OTT hasta 1922 es la excepción explícita anterior y no modifica mandatos existentes de TUR.

Hay 33 ventanas focales generadas directamente (31 llamadas, una de ellas para tres sultanes), más copias explícitas de predecesores rusos, Carlos, la restauración de Pekín y la serie ROC disponible. El número final de copias depende de la entrada. No deben contarse las copias como nuevas verificaciones independientes. Las fechas de ventana documental tienen indicadores de cobertura; las fechas exactas de actos conservan precisión diaria. No se fabrican nombramientos de 1 de enero.

Validación realizada sin importar ni ejecutar el curador: análisis sintáctico AST correcto. Pendiente para integración: aplicación aislada, doble aplicación idéntica, conservación por campos de los originales 1920+, ausencia de duplicados de ventanas, resolución anual de las nuevas identidades y comprobación de retratos. La prioridad de curación del resolver debe ocultar la parte focal de un mandato genérico que cruza 1920 sin mutilar su tramo posterior.
