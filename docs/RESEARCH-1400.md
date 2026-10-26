# Ampliación 1400–1499 · 0.22.0

La navegación anual llega a 1400. Esta entrega amplía autoridades, retratos, símbolos e instituciones; no certifica una revisión mundial exhaustiva de todos los límites y gobernantes. Los vacíos continúan identificados por nombre y año.

## Cartografía e identidad

880 intervalos componentes adicionales de la revisión fijada de [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria), CC BY 4.0, en `early-modern-1400.geojson`. Se mantienen coordenadas e índices originales. Los nueve recursos geográficos anteriores comprobados con 0.21 se conservan byte a byte. Las áreas grises representan ausencia de una entidad en el inventario, no agua, despoblación o ausencia histórica de organización.

60 reglas fechadas corrigen identidades y ámbitos: Bizancio/Trebisonda, coronas ibéricas, Kalmar y coronas escandinavas, Polonia/Lituania, condado/ducado de Saboya y poderes americanos anteriores a la conquista. El imperio restaurado de Constantinopla no continúa como si conservara un mismo emperador después de 1453. Trebisonda tiene su propia serie hasta 1461. [The Metropolitan Museum of Art](https://www.metmuseum.org/essays/byzantium-ca-330-1453) distingue las continuidades regionales bizantinas; las fichas no fabrican una frontera ausente.

La fuente usa Q202266, que identifica a Margarita I, como identificador del antiguo reino noruego. Se resuelve al reino Q2196956, conservando cargos noruegos separados de los daneses y suecos. Los agregados de casas dinásticas y ciudades mayas no reciben un gobernante único por defecto. Las etiquetas anacrónicas «Hashemite Arab Federation» y «Ngô Dynasty» del inventario se conservan sólo como referencias sin identidad resuelta: no importan sus autoridades del siglo XX o X al XV. Corregir una etiqueta no acredita todos los límites del contorno heredado.

## Autoridades y retratos

`historical-offices-022-research.json` congela 206 intervalos seleccionados, evidencia y candidatos rechazados o no resueltos. Otros 94 registros proceden de adquisición aislada y no equivalen a 94 revisiones historiográficas individuales. La lectura distingue cargos P39 y títulos nobiliarios P97 fechados, evitando convertir fechas de nacimiento o muerte en mandatos.

- Francia y coronas ibéricas conservan sucesiones independientes; matrimonio y unión dinástica no significan administración nacional única.
- Inglaterra separa los dos reinados de Enrique VI y Eduardo IV. Su título reclamado de Francia no se utiliza como reinado inglés. Eduardo V, Ricardo III y Enrique VII se distinguen dentro de 1483–1485.
- Sacro Imperio: reyes de Romanos y dignidad imperial tienen fechas distintas. Los electores, landgraves y duques no son autoridades nacionales de una Alemania unificada. Las ramas de Hesse y las particiones sajonas requieren más detalle regional.
- Interregno otomano: Süleyman, Musa, İsa y Mehmed tienen poderes regionales y pretensiones rivales después de Ankara. Murad II y Mehmed II conservan reinados interrumpidos; no se interpolan períodos de control estable.
- Ming distingue los dos reinados de Yingzong, separados por Jingtai. Japón distingue emperador, shogun y poder regional. Los mandatos de las coronas de Kalmar se contrastan por cargo; no se extiende todo reinado danés a Suecia.
- Granada distingue Muley Hacén, El Zagal y Boabdil; las restauraciones y la entrega de enero de 1492 no se confunden con un gobierno continuo.
- Etiopía: se evita usar el nacimiento de Eskender en 1471 como acceso al trono. Su reinado comienza en 1478, según la sucesión documentada. Continúan vacíos y autoridades locales pendientes.
- América: Triple Alianza desde 1428 y fase imperial inca según cronología tradicional desde 1438. El estudio de [datación por radiocarbono](https://www.cambridge.org/core/journals/radiocarbon/article/when-did-the-incas-build-machu-picchu-and-its-satellite-sites-new-approches-based-on-radiocarbon-dating/10254F52B68EAC0960DB85D91BB66593) explica los límites de usar las cronologías de crónicas como fechas absolutas. La autoridad mexica tampoco equivale a soberanía nacional uniforme sobre cada ciudad tributaria.

147 retratos adicionales con procedencia, licencia y hash locales. Una reproducción identifica a una persona; no garantiza parecido exacto en cada año. Continúan pendientes retratos, variantes por edad, regencias y autoridades rivales. No se fabrican imágenes para llenar huecos.

## Símbolos, instituciones y contexto

13 ventanas de símbolos representativos, con dos archivos nuevos. Armas Valois, estandartes castellano y aragonés, Dannebrog, enseña imperial, giglio florentino y mon Ashikaga se identifican por su función. La variante portuguesa de 1495 y la bandera de armas ducal de Wurtemberg desde 1495 no se anticipan a períodos anteriores.

La enseña paleóloga se reproduce a partir del [Atlas catalán de 1375 conservado por la BnF](https://www.bnf.fr/fr/mediatheque/atlas-catalan-1375), como referencia dinástica, sin afirmar una norma textil uniforme de cada año. El estandarte nazarí rojo con divisa en oro se documenta en [El señal del rey de Aragón: historia y significado](https://ifc.dpz.es/recursos/publicaciones/19/73/_ebook.pdf), p. 92. El archivo es una reconstrucción representativa, no fotografía de un tejido original.

Siete casos no adoptados/pendientes en `review-022-symbols.json`. Los estandartes navarros candidatos llevan aviso de falta de fuente de insignia y no se adoptan. La obra propia de Saboya sin atribución cronológica, banderas nacionales Ming no acreditadas, el arcoíris municipal moderno de Cusco y símbolos coreanos posteriores tampoco se retrotraen.

30 registros institucionales, 33 sedes/cortes y 16 contextos, con 10 puntos regionales de conflictos: Cien Años, Dos Rosas, interregno otomano, Constantinopla, Trebisonda, Granada, guerras borgoñonas, husitas, Ōnin y sucesión moscovita. Los puntos no son frentes ni superficies de ocupación. Las sedes de Estados germanos agrupados abren sus fichas sin inventar límites propios. V-Dem/OWID conserva su inicio en 1789 y las organizaciones mantienen sus fechas originales.

## Auditoría y continuidad

[REVIEW-1400-1499.json](REVIEW-1400-1499.json) ejecuta la ruta real de producción para los cien años: 13.350 entidades/año, 10.075 casos sin autoridad, 12.288 sin símbolo y 38 personas/órganos sin retrato entre los registros activos. Las sedes agrupadas se cuentan aparte. Es una auditoría de disponibilidad, no un censo exhaustivo ni una certificación de fronteras diarias.

Preparadores específicos de `1400`/`022`; candidatos y aceptaciones congelados. La compilación no consulta proveedores históricos. Mantener un solo escritor de identidades/medios y regenerar `Países` tras las escrituras. Catálogo final: 832 claves, 14.892 registros de mandatos y 3.050 carpetas. Continuidad y pendientes en [tareas.md](../tareas.md). La publicación remota queda a la comprobación del propietario, sin espera de Actions/Pages.

Comprobaciones locales:194 pruebas en46archivos, tipos y compilación correctos; dos recorridos de navegador correctos y revisión visual de escritorio/móvil con imágenes cargadas. La captura móvil espera a que la cámara y el dibujo del globo estén en reposo, evitando confundir una transición de dibujo con ausencia de territorio. Integridad SHA-256 de69datos,11franjas tipográficas y7.042medios; conservación de hechos previos y nueve recursos geográficos anteriores comprobada.
