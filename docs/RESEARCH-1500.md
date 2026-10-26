# Ampliación 1500–1599 · versión 0.21.0

La navegación anual llega a 1500. Esta entrega amplía los registros disponibles, sin afirmar que estén completas las fronteras, autoridades, regencias o banderas mundiales del siglo XVI. Una entidad cartográfica puede ser un agregado de muchos poderes; su inventario no equivale a un censo de países soberanos.

## Cartografía e identidades

`early-modern-1500.geojson` contiene 826 intervalos componentes de la revisión fijada de [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), con licencia CC BY 4.0. Se conservan las coordenadas y los índices del original. Los ocho recursos geográficos anteriores comparados con la entrega 0.20 permanecen idénticos byte a byte. No se dibujan polígonos de conquista a partir de puntos de batallas.

65 reglas en `historical-1500-entities.json` distinguen Castilla/Aragón/monarquía hispánica, Moscovia/zarato, Florencia republicana/ducado/Toscana y las uniones de Kalmar, Polonia-Lituania e Iberia. La unión de Lublin no se anticipa a 1569; el agregado jagellón no recibe un único rey polaco como soberano de todas sus coronas. Las familias de Habsburgo, Borbón y Saboya no se convierten en personas gobernantes ni en países nacionales uniformes.

Se mantiene la corrección Joseon frente a Gojoseon, la extinción de Urgell independiente en 1413 y la conquista portuguesa de Malaca en 1511. Ming no se sustituye por Qing. Los Estados mayas y los contornos de Mogulistán compartidos conservan advertencias sobre sus agregados y series locales pendientes.

El antiguo imperio inca y el reino resistente de Vilcabamba tienen fichas distintas. Si la fuente conserva un contorno amplio anterior, la etiqueta y la nota explican que **no acredita los límites precisos de Vilcabamba**. Cambiar la identidad no crea una cartografía regional que falte. La datación de las sucesiones incas y los años de transición sigue necesitando cotejo adicional.

## Autoridades y medios

`historical-offices-021-research.json` congela 224 intervalos seleccionados, candidatos, evidencia de cargos y rechazos. La adquisición aislada aporta otros 153 registros, que no equivalen a una revisión individual de todas sus fuentes. Se conservan los hechos de mandatos y símbolos anteriores; se permite completar sus retratos.

- Castilla distingue a Isabel, Juana, Felipe y Carlos, junto a las regencias de Fernando y Cisneros. El reinado legal de Juana no implica gobierno personal continuo; Carlos no gobierna en 1500.
- Portugal conserva numeración y cargos propios durante la unión: Felipe I de Portugal es Felipe II de España. No se adelanta la unión a los reinados anteriores.
- Inglaterra distingue la sucesión Tudor y la proclamación disputada de Juana Grey. [Historic Royal Palaces](https://www.hrp.org.uk/hampton-court-palace/history-and-stories/henry-viiis-children/) y la [Casa Real](https://www.royal.uk/henry-viii) documentan las sucesiones principales. Las fechas de calendario no verificadas día a día se presentan con precisión anual.
- Sacro Imperio: dignidad imperial, electores, duques y landgraves separados. Maximiliano es rey de Romanos antes de su título imperial de 1508; la abdicación de Carlos en 1556 y el reconocimiento de Fernando en 1558 son hitos distintos. La partición de Hesse de 1567 y la transferencia electoral sajona de 1547 no se convierten en una monarquía alemana nacional.
- Wurtemberg separa el exilio de Ulrico de sus períodos de control; Humayun tiene dos reinados separados por el poder surí. No se interpola un gobierno continuo a través del exilio.
- Estados Pontificios: se seleccionan los pontificados, evitando confundir un cargo anterior de cardenal o una coronación con el acceso al pontificado. Las vacantes intranuales no se rellenan con una persona ficticia.
- Japón diferencia emperador, shogun y dirigentes Oda/Toyotomi. No se llama shogun a estos últimos ni se atribuye a un cargo control de todos los dominios rivales. Ming, Joseon, safávidas, mogoles, Lodi, suríes y soberanos del sudeste asiático tienen intervalos propios, todavía parciales.
- América: la autoridad mexica se limita a la caída de Tenochtitlan, no a la ejecución posterior de Cuauhtémoc. [The Metropolitan Museum of Art](https://www.metmuseum.org/essays/tenochtitlan) documenta la transformación de la ciudad. Incas y Vilcabamba se distinguen del poder colonial posterior. No se considera territorio deshabitado por faltar una autoridad en el catálogo.
- África: autoridades etíopes, Kongo, wattasíes, saadíes, mamelucos y Songhai. Las disputas y poderes sucesores no se resuelven interpolando un gobernante único de toda la región.

Se rechazan las desambiguaciones homónimas de Muhammad Adil Shah, Yaqob y otros candidatos. La persona verificada Muhammad Adil Shah Suri y Yaqob de Etiopía tienen identificadores distintos; los rechazos se conservan para no reintroducirlos en futuras adquisiciones.

192 retratos adicionales y siete archivos de símbolos nuevos se guardan localmente con autor, licencia, procedencia y hash. Un retrato representativo puede ser una interpretación histórica posterior: no acredita la apariencia exacta de cada año. Continúan pendientes variantes por décadas y retratos ausentes.

## Símbolos fechados

21 ventanas de símbolos distinguen armas, estandartes, enseñas militares y mon dinásticos. No todos son banderas nacionales modernas. Se conservan nueve casos no adoptados/pendientes en `review-021-symbols.json`.

- Francia Valois utiliza armas de azur y tres flores de lis; la [BnF](https://expositions.bnf.fr/livres/armorial/grand/ars_4790_047v.htm) explica su evolución. El estandarte blanco borbónico no se anticipa a esa dinastía.
- Castilla y Aragón conservan enseñas territoriales distintas. La cruz de Borgoña llega en 1506, pero el paño blanco con cruz roja utilizado aquí se limita desde 1530, conforme a la [guía del IHCM](https://ejercito.defensa.gob.es/Galerias/Descarga_pdf/Unidades/Madrid/Ihcm/2018/20180227-expo-banderas-ihcm.pdf).
- Portugal distingue variantes de 1495, 1521 y 1578. El [catálogo histórico conservado por la Biblioteca Nacional de Portugal](https://purl.pt/37813) sirve de referencia iconográfica, sin afirmar un pabellón reglamentario idéntico en todos los buques.
- Prusia ducal no recibe símbolos de un reino posterior; Wurtemberg conserva su bandera de armas. El mon Ashikaga no se sustituye por el Tokugawa en 1500.
- No se impone la bandera mexicana actual a la Triple Alianza ni el arcoíris municipal contemporáneo de Cusco a los incas. Ming, safávidas y mogoles siguen necesitando testimonio material suficiente para los diseños concretos. El sello coreano de 1637 y el tricolor ruso de 1705 no se retrotraen.

## Contexto, filtros y alcance verificado

39 registros institucionales, 37 referencias de cortes/sedes y 17 fases documentales adicionales, con 11 puntos regionales de conflictos. Las sedes de Estados germanos agrupados abren su ficha independiente sin inventar sus contornos. Las guerras de Italia, Reforma, revuelta neerlandesa, guerras francesas, conquistas americanas, partición húngara, transición mogola, invasiones de Corea y conquista de Songhai tienen referencias fechadas. Los puntos regionales **no son frentes ni superficies ocupadas**. V-Dem/OWID sigue desde 1789; no se inventan evaluaciones democráticas para 1500 ni se retrotraen organizaciones contemporáneas.

[REVIEW-1500-1599.json](REVIEW-1500-1599.json) ejecuta la ruta real de resolución para los cien años: 11.630 entidades/año, 7.611 casos sin autoridad, 9.955 sin símbolo y 60 personas/órganos sin retrato entre las autoridades disponibles. Cuenta las sedes agrupadas aparte. Mide disponibilidad, no exactitud historiográfica, fronteras diarias ni exhaustividad mundial.

Preparación reproducible: `prepare-1500-geometry.py`, `enrich-1500-authorities.py`, `review-021-rulers.py`, `review-021-additional.py`, `prepare-1500-authorities.py`, `prepare-1500-entities.py`, `prepare-1500-support.py`, `prepare-1500-symbols.py`, `register-review-021.mjs`. Los datos de investigación aceptados están congelados; la compilación no consulta proveedores históricos. Regenerar `Países` después de todas las escrituras de identidades y medios. Mantener un solo escritor de esos archivos.

La pizarra de continuidad está en [tareas.md](../tareas.md). Los vacíos, geometrías regionales, símbolos sin evidencia, regencias y variantes de retratos continúan pendientes; una entrega no cierra esos inventarios.

Comprobaciones locales: 190 pruebas en 45 archivos correctas, tipos y compilación correctos, dos recorridos de navegador correctos tras ajustar una prueba que buscaba una categoría sin entidades. Imágenes cargadas y revisión visual en mapa y globo móvil. Integridad SHA-256 de 67 datos, 11 franjas tipográficas y 6.893 medios; catálogo regenerado con 2.961 carpetas. No se espera ni se comprueba el despliegue remoto en esta entrega.
