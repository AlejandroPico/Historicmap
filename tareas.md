# Tareas y continuidad

Actualizado: 23/10/2026, 21:16 Madrid. Rama: main. Aplicación 0.9.1 subida en c42531df6fafe5fdd9c6fc999a80741aa1829076 (candidato anterior; sustituido por el siguiente commit con cinco retratos adicionales).

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
- [ ] Quality 0.9.1 completo. Run 40009382574: instalación, integridad, unitarias y build superados; navegador en curso.
- [ ] Pages de 0.9.1 y cotejo de los bytes públicos con c42531df6fafe5fdd9c6fc999a80741aa1829076 (candidato anterior; sustituido por el siguiente commit con cinco retratos adicionales).
- [ ] Cierre documental con SHA, resultados, evidencia y árbol de trabajo limpio. No afirmar que 0.9.1 está publicada sólo porque lo esté 0.9.0.

## Pendientes reales de investigación y siguientes etapas

- [ ] Recuperar y cotejar el CSV original. La ruta C:/Users/darim/Downloads/lista_imperios_completa_v3.csv no existe en las comprobaciones realizadas; no se ha importado ni reconstruido como si se hubiese leído.
- [ ] 91 personas u órganos sin retrato: 76 sin P18 en la fuente consultada, 12 candidatos pendientes de identificación/licencia/adquisición y tres órganos o identificadores documentales. No son 96 países ni imágenes aprobadas. Conservar las exclusiones de retratos incorrectos.
- [ ] Variantes históricas de Andorra y San Marino: 20 país-años de 1960–1969 sin bandera. No rellenar con diseños modernos sin cotejo de la variante.
- [ ] Relevos diarios, suplencias, gobernadores generales y cargos secundarios identificados en las investigaciones, incluido enero de 1966 en Nigeria. Una ventana documental no es un nombramiento o una dimisión.
- [ ] Frentes mensuales y control detallado de Congo, Biafra, Vietnam y Levante; sectores aliados de Alemania y control reciente completo. Mantener los límites de resolución de cada fuente.
- [ ] Fichas tempranas que aún no se abren y ampliación de familias/regímenes fuera de los casos revisados. Revisar por etapas; no declararlo resuelto por ampliar una década.

## Cómo retomar

Consultar primero Git, esta pizarra y docs/DELIVERY-0.9.1.md. El código de aplicación está subido; falta cerrar el flujo de publicación indicado arriba. No repetir adquisiciones ni curaciones a ciegas. La última repetición de la curación de 1960 conservó todos los bytes y retratos; no hay adquisición de medios activa.

Servidor de preview propio: sesión 84360, puerto 5174. Navegador CUA: browser 2/tab 2 temporal. La compilación local de 0.9.1 contiene index-B6vtP2_U.js; no cambiar rama ni recompilar mientras otra prueba use ese directorio. La referencia contemporánea sigue siendo 22/10/2026; investigar el pasado no avanza esa referencia.

Si se interrumpe la sesión, registrar el último paso terminado, procesos activos, fallos concretos y siguiente acción antes de cerrar. No confundir el SHA de aplicación publicado con un commit posterior sólo documental.
