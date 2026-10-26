# Ampliación 1600–1699 · versión 0.20.0

La navegación anual llega a 1600. Se amplía la documentación sin afirmar que estén completas las fronteras, banderas, autoridades o regencias de todo el mundo. Los inventarios de componentes cartográficos no son censos de Estados soberanos.

## Cartografía y resolución temporal

`early-modern-1600.geojson` incorpora 783 intervalos componentes de la misma revisión fijada de[Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria),CCBY4.0. Se conservan matrices de coordenadas e identificadores del índice de origen. Los archivos de 1700 y posteriores no se reconstruyen. La selección es una síntesis anual sin día uniforme, no una frontera diaria de campaña.

67 reglas en`historical-1600-entities.json` distinguen monarquías y repúblicas, uniones dinásticas, administraciones y regímenes rivales. Se separan ducado/electorado bávaro, electorado de Brandeburgo/unión con Prusia, Ming/Mingdel Sur/Jinposterior/Qing/Shun, monarquía inglesa/Commonwealth/Restauración y coronas ibéricas. No se anticipa el reino de Prusia de 1701 ni la unión política británica de 1707.

La fuente identifica al régimen Shun con la persona Li Zicheng Q333567; se resuelve a la entidad Q2370784. Joseon conserva la corrección Q28179 frente a Gojoseon antiguo. La etiqueta republicana de Florencia no prolonga ese régimen sobre la Toscana del XVII. Malaca distingue administraciones portuguesa y neerlandesa, sin prolongar el sultanato independiente después de 1511. Urgell no se presenta como un Estado independiente después de 1413.

Mogulistán oriental y occidental comparten un QID en la fuente. Se mantienen referencias locales separadas, sin atribuir automáticamente un mismo khan a ambos ámbitos. Los agregados y cronologías defectuosas se señalan; las reglas de identidad no aportan contornos que falten.

## Autoridades, regencias y retratos

La adquisición está aislada y se limita a las entidades de la fuente y correcciones explícitas. Conserva todos los hechos de mandatos y símbolos anteriores. El registro congelado`historical-offices-020-research.json` contiene 196 intervalos revisados, sus candidatos, fuentes y rechazos; la adquisición general aporta otros registros que no equivalen a una revisión historiográfica individual.

- Inglaterra: reyes, corregencia Guillermo/María, autoridades colectivas y dos Lord Protectors. Oliver y Richard Cromwell no se convierten en reyes. Carlos II no recibe el gobierno efectivo de Inglaterra durante todo el interregno. Referencias:[Casa Real británica](https://www.royal.uk/interregnum-1649-1660),[Parlamento](https://www.parliament.uk/about/living-heritage/evolutionofparliament/parliamentaryauthority/civilwar/overview/end-of-the-protectorate/).
- Portugal: Felipe II/IIIde Portugal son Felipe III/IVde España. João IV pertenece a la Restauración de 1640; el reconocimiento de 1668 es un hecho distinto. Afonso VI y las regencias de Luisa/Pedro se distinguen del reinado posterior de Pedro II.
- Francia: reyes y regencias de Maríade Médici/Anade Austria; el acceso de Luis XIV de 1643 no es su gobierno personal de 1661. España distingue la minoría de Carlos II y la regencia de Marianade Austria.
- Sacro Imperio y territorios: emperador, autoridad de la rama imperial de Habsburgo, electores, duques y landgraves. Las cesiones entre ramas y gobernantes requieren más detalle; la autoridad imperial no se equipara a una jefatura nacional única de todos los miembros. Se mantienen las advertencias sobre minorías y exilios.
- Rusia: soberanos rivales, consejo provisional, cozares y regencia de Sofía. Se conserva precisión anual donde los calendarios no se han cotejado día a día. La elección de Miguel Románov de 1613 tiene referencia documental propia:[carta reproducida en laLibraryofCongress](https://www.loc.gov/item/2021666631/).
- Asia: emperadores Ming y pretendientes del Sur, khanes Jin y emperadores Qing, regencia de Dorgon, corte imperial y shogunes japoneses, reyes de Joseon/Ayutthaya, mogoles, chhatrapatis y shahs safávidas. Los regímenes rivales no controlan automáticamente toda China; la titularidad imperial no demuestra dominio uniforme del subcontinente indio.
- África: se amplían soberanos de Etiopía y Kongo y registros de adquisición regional. La guerra civil del Kongo posterior a 1665 no se rellena interpolando un rey único para todo el territorio.

Los candidatos homónimos Q1463281 y Q2364427 son desambiguaciones; se rechazan en favor de las personas verificadas Q152727 y Q172061. Los cargos provinciales neerlandeses y el gran pensionario de Holanda se identifican como tales, no como monarcas nacionales.

Se añaden 143 retratos acreditados, con autor, licencia y archivo local. Una reproducción histórica identifica a una persona, no acredita su aspecto exacto en todas las décadas: ampliar variantes por etapas sigue pendiente. No se fabrican fotografías de órganos colectivos ni se restituye el fragmento sin rostro de Sunjo excluido en 0.19.

La conservación de una ficha colonial no prueba que existiera esa administración antes de su intervalo de fuente. El administrador de respaldo sólo se aplica dentro de ese intervalo; un cambio de fecha no proyecta automáticamente hacia atrás el soberano de una colonia posterior.

## Símbolos

31 ventanas revisadas, con tipos visibles y procedencia individual. Se añaden 11 archivos de símbolos; el inventario completo llega a 6.694 medios acreditados. Archivos originales y ventanas anteriores conservados.

- Commonwealth: variantes 1649–1651,1651 y 1658, sin prolongarlas sobre la monarquía restaurada al cierre de 1660.
- Portugal: variantes 1578,1616,1640 y 1667, distinguidas de las españolas. La variante naval 1616 remite al catálogo histórico de la Biblioteca Nacional de Portugal descrito en su ficha de Commons.
- España: cruz de Borgoña identificada como enseña militar, no como bandera nacional uniforme de todos los dominios. No se inventa una bandera nacional única para la unión ibérica.
- Países Bajos: enseña del príncipe y pabellón rojo posterior, con coexistencia y transición de colores señaladas. No se retrotrae automáticamente el tricolor rojo de la etapa posterior a 1600.
- Sacro Imperio, Baviera, Sajonia, Wurtemberg y Brandeburgo: enseñas o armas fechadas. El Bindenschild austriaco es blasón dinástico, no bandera nacional uniforme de todos los dominios Habsburgo.
- Japón: mon Tokugawa desde la etapa shogunal; Qing: enseña institucional de una de las Ocho Banderas; Joseon: sellos reales desde 1637 y 1653. No se presentan como banderas nacionales modernas.
- Ayutthaya: ventana interior del pabellón marítimo rojo desde 1680, sin inventar una adopción en 1600. Saadíes: referencia blanca simplificada documentada para Ahmadal Mansur; no reconstruye bordados ni se aplica automáticamente a todos sus sucesores. El rojo alauí comienza en su propia fase.

`review-020-symbols.json` conserva seis candidatos no adoptados o pendientes. Se rechaza el diseño Ming subido como obra propia en 2026 sin testimonio del uso histórico, el alam mogol marcado como ficticio, la retroproyección del tricolor mercante ruso de 1705 y las armas de Hesse de 1736 sobre 1600. Persia, Ming, numerosos Estados africanos y otras variantes continúan pendientes de cotejo material: un resultado de búsqueda no acredita autenticidad histórica.

## Formas, sedes y contexto

37 registros institucionales,30 referencias de sedes/capitales/cortes y 15 fases documentales adicionales. Seis registros de sedes de Estados germanos sólo aparecen cuando la cartografía los agrupa y no hay contorno propio; abren la ficha correcta sin inventar fronteras. Se distinguen Edo/corte de Kioto, Ming/Pekín y Qing/Shenyang/Pekín según fecha.

Siete puntos regionales de conflictos contextualizan las guerras del período. No son frentes ni superficies de ocupación. Los cambios de régimen y los colores no permiten deducir campañas ausentes. La evaluación V-Dem/OWID mantiene su inicio 1789; las organizaciones conservan sus fechas y no se extrapolan a 1600.

## Auditoría y pendientes

[REVIEW-1600-1699.json](REVIEW-1600-1699.json) recorre los 100 años por la ruta real de producción:11.079 entidades/año,7.540 casos anuales sin autoridad documentada,8.643 sin símbolo y 58 personas/órganos sin retrato entre los registros disponibles. En 1600 hay 97 componentes,32 con autoridad y 16 con símbolo; en 1648,117/38/25; en 1699,108/36/32. Las sedes de Estados agrupados se cuentan aparte. No son un censo completo ni una certificación de exactitud mundial.

Pendiente: inventario regional y regencias completos, cronologías intranuales y calendarios, geometrías de Estados germanos individuales, autoridades locales coloniales, Mogulistán y otros QIDs compartidos, frentes y facciones, símbolos con testimonio verificable y retratos por etapas. Los huecos anteriores a esta entrega siguen abiertos; reanudar sesión no los convierte en terminados.

## Preparación y validación

Orden: prepare-1600-geometry → enrich-1600-authorities → review-020-rulers/review-020-extra → prepare-1600-authorities → adquisición de retratos → prepare-1600-symbols → prepare-1600-entities/prepare-1600-support → register-review-020 → prepare-country-catalog. Los registros revisados se congelan; la investigación se renueva explícitamente. Un solo escritor deidentidades/medios a la vez. La compilación y las fichas no consultan proveedores históricos.

Resultados locales y comprobación del envío en `tareas.md`. Subir tras verificar y terminar al confirmar el push, sin esperar ni sondear Actions/Pages; la publicación la comprueba el propietario.

Validación local final: 186 pruebas en 44 archivos, tipos y compilación correctos. Dos recorridos de navegador en 1,9 min y repetición focal de 42 s, con retrato y pabellón portugués cargados y revisión visual. 65 recursos de datos, 11 franjas tipográficas y 6.694 medios íntegros por SHA-256; 6.770 recursos preparados en Git comprobados byte a byte. No se ha repetido toda la batería de navegador ni se ha verificado la publicación remota.
