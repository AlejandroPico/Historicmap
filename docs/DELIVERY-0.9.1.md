# Entrega 0.9.1 · cierre de la ampliación a 1960

Estado: **publicada y comprobada** en https://alejandropico.github.io/Historicmap/. Aplicación: **f67f8aecf9acc19e51e7f49648ea81e12008b34d**. El commit posterior de cierre documental y aserciones no cambia la aplicación publicada.

## Cambios de la entrega

La base 0.9.0 integra el control en la geometría seleccionable, franjas opcionales de ocupación, tierra de referencia y una paleta editorial de 33 familias. La ampliación documental llega a 1960, con Estados históricos, dependencias, autoridades, símbolos, membresías, contexto y relaciones navegables. Detalle y comprobación de la primera publicación en DELIVERY-0.9.0.

La corrección 0.9.1 conserva los retratos antes de regenerar mandatos curados. Recupera 26 retratos ya acreditados en el inventario y añade una regresión para Abdoh. Repetir la preparación conserva exactamente los bytes del catálogo. No son 26 archivos nuevos.

Se distingue la presidencia parlamentaria de Azikiwe del Gobierno de Balewa. La consolidación no recupera cargos descartados por una corrección revisada. Los extremos de enero de 1966 siguen pendientes de contraste diario.

El filtro de licencias confundía las letras «nd» de India con la marca NoDerivatives. Ahora distingue el token ND e incorpora cinco archivos históricos con GODL-India, conservando créditos, exclusiones y el límite de lectura. No se amplía la lista de licencias aceptadas.

Quality limita concurrencia por rama. Pages sólo publica el éxito de push correspondiente al commit vigente y mantiene el checkout fijado a la revisión verificada. El candidato c42531d queda sustituido por f67f8ae; un resultado de la revisión anterior no acredita publicar la actual.

## Cobertura y pendientes reales

Catálogo: **283 claves y 7.480 mandatos**, **3.793 medios** (439 SVG y 3.354 fotografías). Auditoría de **1.693 país-años de 1960–1969**, sin huecos de resolución de autoridad. No certifica todos los cargos, suplencias, retratos, días de mandato ni frentes del mundo.

Quedan **91 personas u órganos sin retrato**: 76 sin P18 en la fuente consultada, 12 candidatos pendientes y tres órganos o identificadores documentales. Nombres, años y pistas en REVIEW-1960.json y reference/portrait-1960-pending-research.json. Una candidatura no equivale a una imagen aprobada.

También quedan 20 país-años sin bandera (Andorra y San Marino), relevos diarios y cargos secundarios identificados en las investigaciones, frentes detallados, sectores aliados de Alemania y fichas tempranas fuera de la ventana revisada.

El CSV original C:/Users/darim/Downloads/lista_imperios_completa_v3.csv no estaba disponible y no se ha importado ni reconstruido como si se hubiese leído. POLITICAL-PALETTE.csv es una exportación editorial propia de las 33 familias implementadas.

## Verificación

115 pruebas unitarias locales en 23 archivos, tipos y compilación correctos. Integridad de 43 recursos, 11 franjas tipográficas y 3.793 medios, incluidos los bytes registrados en Git. Los cinco retratos de India y los 26 recuperados conservan licencia/crédito individual.

La comprobación manual del navegador muestra Nigeria con imágenes y funciones separadas, la transición TAN→TZA con la ficha abierta y reproducción con franjas. Los fallos de las primeras pasadas locales se documentan en DELIVERY-0.9.0; no se declaran correctas todas las ejecuciones locales.

La 0.9.0 superó [Quality 40005916966](https://github.com/AlejandroPico/Historicmap/actions/runs/40005916966): 114 unitarias y 28 recorridos. [Pages 40008258279](https://github.com/AlejandroPico/Historicmap/actions/runs/40008258279) publicó ba7eb3b8ab505a277f5fb5f59c6e18eeb06084af. Se cotejaron cuatro archivos de aplicación, tres manifiestos, siete conjuntos de datos y nueve medios focales en reference/public-verification-0.9.0.json. Ese cierre no sustituye al pendiente de f67f8ae.

## Cierre comprobado

- [Quality 40011433956](https://github.com/AlejandroPico/Historicmap/actions/runs/40011433956): integridad de 43 recursos, 11 franjas y 3.793 medios; 115 pruebas unitarias/23 archivos y 28 recorridos de navegador correctos. El recorrido anual 1789–2026 tardó 2,6 minutos; la suite de navegador, 13,5 minutos.
- [Pages 40013402559](https://github.com/AlejandroPico/Historicmap/actions/runs/40013402559): build y deploy correctos; el log confirma checkout de f67f8ae.
- Cotejo público de cuatro archivos de aplicación, tres manifiestos, siete conjuntos de datos y 16 medios focales, incluidos los cinco nuevos retratos de India. Huellas en reference/public-verification-0.9.1.json.
- Prueba del sitio público en el navegador integrado: India de 1966 muestra Indira Gandhi, Shastri, Nanda y Radhakrishnan con sus cargos, fechas y cuatro imágenes cargadas de 330 px. Sin errores de consola; script index-B6vtP2_U.js. Captura local: .cache/public-0.9.1-india1966.png.
- Regresión geográfica suplementaria local: París, Viena, Innsbruck, Salzburgo, Graz y Linz pertenecen al inventario controlador de 1942; Viena sin franjas de ocupación y Oslo con ellas. Cuatro pruebas focales correctas. Estas aserciones se conservan en el cierre posterior con [skip ci], sin cambiar aplicación o datos.

El candidato anterior c42531d superó sus 115 unitarias y 28 recorridos, pero [Pages 40011732004](https://github.com/AlejandroPico/Historicmap/actions/runs/40011732004) se omitió al existir f67f8ae. La protección evita publicar esa revisión superada. Continuidad y pendientes en ../tareas.md.
