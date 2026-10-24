# Tareas y continuidad

## Encargo vigente · 0.11.1 · corrección de pruebas de publicación

El propietario comunica tres fallos de los 30 recorridos de Quality de0.11.0; los otros27 han pasado según el registro aportado. Corregir y subir sin esperar ni consultar Actions/Pages. No retirar datos históricos válidos para satisfacer expectativas antiguas.

- [x] Revisar las tres causas: organizaciones disponibles en1947, autoridad colectiva alemana en1946 y varios mandatos españoles en1939.
- [x] Actualizar las comprobaciones con condiciones positivas y negativas: ONU1947/OTAN aún inactiva, límite1919, órgano aliado sin bandera/retrato personal ficticios y Franco/Azaña con fecha del mandato.
- [x] Corregir la ayuda de cobertura de organizaciones a1920; versión0.11.1 y documentación.
- [x] Ejecutar las comprobaciones locales y los tres recorridos afectados; registrar resultados reales y preparar entrega a main.
- [ ] Revisar despliegue únicamente cuando el propietario confirme su terminación o aporte otro error.

Estado: corrección preparada desde 8990dcc en codex/fix-011-e2e para entrega a main. 129 pruebas unitarias/28 archivos, tipos y compilación correctos; los tres recorridos afectados pasan en 2,6 minutos. Confirmado que datos, catálogo Países y flujos de CI no cambian. Detalle en docs/DELIVERY-0.11.1.md. Tras confirmar el envío, el único siguiente paso operativo es el aviso del propietario sobre el despliegue; no afirmar que esté publicado por adelantado.

## Registro de la entrega · 0.11.0 · ampliación hasta1920

Petición24/10/2026: ampliar globalmente1920–1949 conservando1950–actualidad, la organización Países y la ficha fija. Mantener el flujo: comprobaciones locales y subida; NO esperar ni consultar el despliegue hasta aviso del propietario.

- [x] Adquisición incremental mundial y auditoría nominal por década1920/1930/1940.
- [x] Curaciones focales de autoridades, regímenes, símbolos, fuentes y retratos; conservar los vacíos reales. Cuatro preparadores de mandatos aplicados, 774 fotografías netas y 87 ventanas de símbolo contrastadas.
- [x] Revisar identidades predecesoras, dependencias y fronteras de la fuente; no inventar frentes diarios.
- [x] Organizaciones, instituciones, conflictos y contexto fechados; no retrotraer datos actuales ni membresías posteriores.
- [x] Sincronizar Países, documentación, manifiestos y versión; corregir fecha visible de Acerca de.
- [x] Pruebas locales apropiadas, compilación y navegador; entrega comprobada para subir y terminar sin espera de Actions/Pages.

Estado inicial: rama codex/1920-history desde45721b4, aplicación publicada0.10.0(fe3676c). Investigación acotada de autoridades y contexto en curso; root gestiona adquisición, medios, aplicación, validación y subida. No considerar esta ampliación terminada por reanudar sesión.

Punto de continuidad del 24/10: 290 claves, 9.485 mandatos; 4.863 medios. Auditoría de 5.294 entidades/año y 70 controles/año: cero huecos de resolución de alguna autoridad; quedan 122 personas/órganos sin retrato y 165 casos anuales sin símbolo, incluidos cuatro cierres alemanes de ocupación sin bandera nacional. No son series diarias completas. Tipos, 129 pruebas/28 archivos, integridad de 43 datos/11 franjas/4.863 medios y compilación correctos; bytes preparados en Git de 4.917 recursos comprobados. La primera suite detectó expectativas antiguas sobre símbolos/ocupación, un límite de tiempo del inventario y una afirmación genérica de Yan que reaparecía en 1950; corrección documentada y suite completa posterior correcta. Danzig1938 comprobado con punto real único, ficha visual y topología original intacta. La prueba de navegador reprodujo un atasco de resaltado Rusia1920→1921, corregido mediante estado de pintura; también se evita representar las tres zonas occidentales alemanas como administradas sólo por Estados Unidos. Los cuatro recorridos finales son correctos (3,3 minutos), incluida la regresión de1950 y la vista móvil. Entrega lista para main, sin sondeos remotos. Siguiente tras confirmar el envío: esperar el aviso del propietario para revisar la publicación.

### Pendientes documentales de esta ampliación

- [ ] Revisar las 118 personas sin fotografía; cuatro órganos colectivos no requieren retrato personal. Lista exacta en docs/REVIEW-1920-1949.json.
- [ ] Revisar los 165 casos anuales sin símbolo y variantes diarias de las banderas ya inventariadas, distinguiendo ausencias correctas de faltas documentales; no inventar una bandera alemana para la ocupación ni usar diseños posteriores.
- [ ] Completar suplencias y regencias diarias, autoridades coloniales locales y gobiernos breves, incluido Yemen1948 y Forster en Danzig1939.
- [ ] Contrastar frentes y fases territoriales omitidas por los inventarios, incluyendo la geometría propia de laRSI; una ficha de conflicto no proporciona un frente.
- [ ] Recuperar y conciliar el CSV original del propietario, aún ausente. Mantener los pendientes de entregas anteriores.
- [ ] Revisar la publicación de0.11.0 cuando el propietario avise de que el despliegue terminó; no consultar Actions/Pages entretanto.

## Registro de la entrega0.10.0

## Encargo vigente · 0.10.0 · ampliación a 1950

**Instrucción del propietario:** comprobar localmente y subir una entrega coherente; NO esperar ni consultar Actions/Pages después de subir. El propietario comprobará el despliegue y pedirá la revisión pública cuando corresponda. Una subida correcta no equivale a despliegue confirmado.

- [x] Adquisición incremental de autoridades de 1950–1959 sin perder curaciones ni fotografías posteriores.
- [x] Contrastes focales de sucesiones, dependencias, independencias, símbolos, fronteras de la fuente, organizaciones y conflictos; auditoría mundial de huecos.
- [x] Catálogo legible en Países: una carpeta por entidad, resumen y referencias a datos/medios; conservar licencias y evitar copias redundantes.
- [x] Entrada extensible para archivos propios de entidades (incluidos futuros himnos), con detección y procedencia explícita.
- [x] Cabecera, bandera y pestañas fijas; contenido interior desplazable sin barra visible; comparación dentro de Comparar y crédito de bandera sin el desplegable anterior.
- [x] Actualizar documentación, versión y comprobaciones locales para la entrega autorizada a main.
- [x] Confirmación del propietario y revisión pública de0.10.0:26 archivos idénticos, versión visible, retratos, cabecera fija y ficha persistente1952→1953.

Estado24/10/2026: rama main. Aplicación0.10.0 publicada en fe3676cb8f2dfa164466eae5f4050b2006b54492; cierre documental posterior separado. Adquisición y curación guardadas:285 claves/7.985 mandatos,4.062 medios(451 SVG/3.611 fotografías). Auditoría:1.753 territorio-años1950–1959, cero huecos de resolución de autoridad;69 personas/órganos sin retrato y23 territorio-años sin símbolo(AND/SMR y Túnez1956–1958). Fuentes y nombres en RESEARCH-1950 y REVIEW-1950. No equivale a series exhaustivas de todos los cargos ni frentes.

122 pruebas/26 archivos correctos, integridad de43 datos/11 franjas/4.062 medios y tipos correctos; compilación final correcta y5 recorridos de navegador correctos(2,5min), incluida vista móvil y ficha anclada. Revisión visual adicional en navegador integrado: Egipto1952 con retratos, cabecera y pestañas fijas. Catálogo:2.783 entidades de las fuentes,285 con inventario de autoridades; no todas tienen ficha completa. No hay himnos adquiridos. No hay agentes de investigación activos ni adquisiciones pendientes en segundo plano. La investigación interrumpida se ha retomado con contraste y scripts propios; no marcar vacíos bibliográficos como resueltos.

Cierre y evidencia en docs/DELIVERY-0.10.0.md y docs/reference/public-verification-0.10.0.json. El propietario confirmó la subida y se revisó después la web pública, sin esperar ni sondear Actions/Pages. HTML/JS/CSS, tres manifiestos, seis conjuntos y14 medios coinciden byte a byte:26 archivos. Versión0.10.0 visible, nueve referencias de retrato cargadas en Egipto1952, cabecera fija, entidad EGY retenida al pasar a1953 y comparación dentro de su pestaña. No se observaron errores de consola. No se repitió toda la suite de navegador ni se certifican por ello todos los datos históricos.

- [ ] Detalle menor detectado en la revisión: la etiqueta Actualización de Acerca de aún muestra23/10 y el historial de0.10.0 muestra24/10; ajustar junto con la siguiente entrega de código. No requiere repetir el despliegue para validar esta versión.

No quedan operaciones de publicación pendientes. Continuar por los huecos de investigación o siguiente encargo. La pestaña de entrega utiliza la URL pública; el preview local ya no es necesario.

Idea futura: separar progresivamente módulos y carga de catálogos para reducir el paquete principal, cuya compilación advierte de tamaño; no reducir el detalle geográfico.

Idea futura: incorporar himnos y otros documentos por entidad y periodo; no descargar grabaciones sin revisar derechos. Mantener esta idea y la cobertura pendiente al retomar.

## Registro de la entrega anterior0.9.1

Actualizado: 23/10/2026, 21:48 Madrid. Rama: main. Aplicación 0.9.1 subida en f67f8aecf9acc19e51e7f49648ea81e12008b34d.

Leer también [agentes.md](agentes.md). Esta pizarra distingue implementación, investigación, validación y publicación. Una sesión recuperada no convierte los pendientes en terminados.

## Funcionalidad solicitada

- [x] Paleta editorial de 33 familias, regímenes focales y matices de dependencia, con contraste entre las familias británica y soviética. Exportación propia en docs/POLITICAL-PALETTE.csv; el CSV del propietario sigue pendiente.
- [x] El control territorial modifica el inventario del mapa y se selecciona como controlador, con las franjas encendidas o apagadas.
- [x] Franjas opcionales, desactivadas inicialmente: tres cuartos del controlador y un cuarto del territorio ocupado. La incorporación documentada se distingue de ocupación; Viena y Oslo tienen regresiones específicas.
- [x] Tierra de referencia bajo los huecos del inventario político, incluida África 1889 y Arabia 1918. Separa tierra y mar; no atribuye ausencia de población ni reconstruye costas históricas.
- [x] Conservar actualizaciones incrementales al recibir geometrías clonadas, sin reprocesar las costas idénticas.

## Ampliación a 1960

- [x] Auditoría de 1.693 país-años de 1960–1969, con suplementos y sin huecos de resolución de autoridad. No certifica todos los cargos, suplencias o días de mandato.
- [x] Revisión focal de UAR, Yemen, Tanganyika/Zanzíbar, UNTEA, protectorados, Namibia, descolonización y estados omitidos. No equivale a reconstruir todos los frentes del mundo.
- [x] Ampliar autoridades, banderas, retratos y contexto: 283 claves, 7.480 mandatos, 3.793 medios; 31 organizaciones/549 intervalos, 258 fases y 59 relaciones/53 registros históricos e institucionales.
- [x] Conservar los medios antes de regenerar mandatos curados. Recuperados 26 retratos acreditados; repetir la curación conserva exactamente los bytes del catálogo.
- [x] Separar la presidencia parlamentaria de Azikiwe del Gobierno de Balewa y evitar que la consolidación recupere cargos descartados por una corrección revisada.
- [x] Registrar nombres, años y pistas de los vacíos en docs/REVIEW-1960.json y docs/reference/portrait-1960-pending-research.json.

## Cierre de la entrega

- [x] Publicación 0.9.0: Quality 40005916966, 114 unitarias y 28 recorridos correctos; Pages 40008258279 correcto. Bytes públicos cotejados, con evidencia en docs/reference/public-verification-0.9.0.json.
- [x] Corrección 0.9.1: 115 unitarias/23 archivos, tipos y build locales correctos. Integridad de 43 recursos, 11 franjas tipográficas y 3.793 medios, incluidos los bytes registrados en Git.
- [x] Comprobación manual del navegador integrado: Nigeria con retratos y cargos separados; TAN→TZA conserva la ficha; reproducción y franjas. Fallos y límites de las primeras pasadas locales registrados en DELIVERY-0.9.0.
- [x] Quality definitivo 40011433956 para f67f8ae: integridad, 115 unitarias/23 archivos, tipos, build y 28 recorridos de navegador correctos.
- [x] Pages 40013402559: build y deploy correctos, checkout f67f8ae confirmado. Cotejo público de cuatro archivos de aplicación, tres manifiestos, siete conjuntos de datos y 16 medios; evidencia en docs/reference/public-verification-0.9.1.json.
- [x] Registrar cierre, SHA y pendientes; commit posterior de documentación y aserciones focales con [skip ci]. El SHA de aplicación publicado es f67f8ae, separado de ese cierre.

## Pendientes reales de investigación y siguientes etapas

- [ ] Recuperar y cotejar el CSV original. La ruta C:/Users/darim/Downloads/lista_imperios_completa_v3.csv no existe en las comprobaciones realizadas; no se ha importado ni reconstruido como si se hubiese leído.
- [ ] 91 personas u órganos sin retrato: 76 sin P18 en la fuente consultada, 12 candidatos pendientes de identificación/licencia/adquisición y tres órganos o identificadores documentales. No son 96 países ni imágenes aprobadas. Conservar las exclusiones de retratos incorrectos.
- [ ] Variantes históricas de Andorra y San Marino: 20 país-años de 1960–1969 sin bandera. No rellenar con diseños modernos sin cotejo de la variante.
- [ ] Relevos diarios, suplencias, gobernadores generales y cargos secundarios identificados en las investigaciones, incluido enero de 1966 en Nigeria. Una ventana documental no es un nombramiento o una dimisión.
- [ ] Frentes mensuales y control detallado de Congo, Biafra, Vietnam y Levante; sectores aliados de Alemania y control reciente completo. Mantener los límites de resolución de cada fuente.
- [ ] Fichas tempranas que aún no se abren y ampliación de familias/regímenes fuera de los casos revisados. Revisar por etapas; no declararlo resuelto por ampliar una década.

## Cómo retomar

La entrega 0.9.1 está publicada y comprobada. Aplicación: f67f8aecf9acc19e51e7f49648ea81e12008b34d. Evidencia de Quality, Pages, bytes y vista pública en docs/DELIVERY-0.9.1.md. El candidato c42531d también pasó 115 unitarias y 28 recorridos, pero Pages 40011732004 se omitió por estar superado: no se publicó como entrega final.

Continuar por los pendientes de investigación anteriores o por el siguiente encargo del propietario. No repetir adquisiciones ni curaciones a ciegas. La última repetición del preparador conservó los bytes y retratos. No hay adquisición activa de medios. El servidor de preview de esta entrega se cierra al terminar; la pestaña de salida usa la web pública (browser 2/tab 2). La referencia contemporánea sigue siendo 22/10/2026.

El cierre añade comprobaciones locales de París, Viena, Innsbruck, Salzburgo, Graz y Linz a la regresión de control de 1942; cuatro pruebas focales correctas, sin modificar el código de aplicación ni sus datos publicados. El cierre con [skip ci] no sustituye Quality cuando cambien código, datos o publicación.

Si se interrumpe la sesión, registrar el último paso terminado, procesos activos, fallos concretos y siguiente acción antes de cerrar. No confundir el SHA de aplicación publicado con un commit posterior sólo documental.
