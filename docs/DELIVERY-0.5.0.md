# Entrega 0.5.0 · actualidad, identidades y espacio de exploración

Fecha: 22/10/2026. Cambios de la entrega y decisiones en agentes.md; cobertura y pendientes en CURRENT-AUTHORITIES; fuentes de agrupaciones/conflictos en CURRENT-LAYERS.

## Implementación

Se corrigen el emparejamiento de QID vacío con España republicana y la unión de metadatos que sobrescribía países con territorios asociados. No se modifican coordenadas para ocultar el problema. La ficha común de búsqueda/clic usa pestañas a la izquierda y todos los mandatos documentados del año. Autoridades en funciones a la referencia se señalan y priorizan dentro de su tipo.

Se incorporan 414 fotografías adicionales: 413 retratos y una escena institucional completa. El catálogo contiene 488 retratos, esa escena y 342 banderas/símbolos. En 2026 hay 508 registros de autoridad, 413 personas u órganos y 403 con imagen en 231 claves. Diez ausencias quedan descritas por persona y ámbito, sin usar fotografías ficticias o imágenes de redistribución no acreditada. Las fotos del monarca actual/anterior españoles y Franco están adjuntas a todos sus registros focales.

Temas mañana/tarde/noche/automático con hora local y océano más claro que fondo. Relieve apagado inicialmente, ampliado como referencia moderna desde 10.000 a. C. y excluido de geología. Leyenda a la derecha, escala e información de atribución abajo a la izquierda. Fuentes pasa a panel breve no modal; desaparecen Explorar épocas y el rótulo Escala adaptativa, conservando el zoom de la regla.

Agrupaciones 2026 de OTAN, UE, BRICS y Tres Mares con categorías separadas; rampa estadística verde y siete contextos parciales de conflictos. No hay clasificación mundial exhaustiva de guerra/paz ni ranking de capacidad militar. Esos ámbitos y el detalle cartográfico/histórico pendiente permanecen en roadmap.

## Validación local

- Integridad de 35 recursos, 11 franjas tipográficas y 831 medios mediante SHA-256; 489 imágenes raster decodificadas correctamente.
- Suite unitaria final: **43 pruebas correctas**, incluidas las correcciones finales de Nauru, Corea y los nombramientos separados de Lecornu.
- Suite final completa de navegador: **15 recorridos correctos en 14 minutos** sobre la compilación final, incluidos los 238 años 1789–2026 y todas las instantáneas cartográficas distribuidas. También comprueba móvil, temas, fuentes, fichas de nueve países y fotografía íntegra de Mozambique, clic real en Brasil 1947 tras España, indicadores, agrupaciones, cargas lentas, reproducción, guerras y proyecciones.
- Comprobación focal final de PIB→OTAN→el mismo PIB correcta: no permanece pintura de agrupación al reutilizar datos. Compilación de producción correcta.

## Publicación

Publicado **f58550940607362a7c0fa86769ca8edd6097d5ba** en [Historicmap](https://alejandropico.github.io/Historicmap/), comprobado el 22/10/2026 hacia las 16:52 UTC.

- [Quality 39814653054](https://github.com/AlejandroPico/Historicmap/actions/runs/39814653054): correcto; 43 pruebas unitarias, 15 recorridos de navegador, verificación de recursos y compilación. Logs comprobados, no sólo estado general.
- [Publish atlas 39816246238](https://github.com/AlejandroPico/Historicmap/actions/runs/39816246238): compilación y despliegue correctos. Checkout de f585509 confirmado en logs.
- Página pública con `assets/index-BsMTmP3r.js` y `assets/index-DuODX5wW.css`, coincidentes con la compilación final. Manifiestos públicos: 35 recursos y 831 medios, todas las huellas coincidentes con las locales. Bytes de la fotografía nueva de Mozambique comprobados por HTTP y SHA-256.
- Ficha pública de España verificada en navegador: pestañas, bandera, Sánchez y Felipe VI, tres imágenes cargadas, disposición a la izquierda, leyenda a la derecha, escala/atribución a la izquierda y tema automático. Evidencia local ignorada en `.cache/release-0.5.0-public-2026.jpg`.

La incidencia de Actions anunciada por GitHub retrasó el cierre de Quality; no se eludió la validación ni se publicó un SHA distinto. El commit de cierre documental usa `[skip ci]` y no modifica la aplicación validada. La cobertura histórica y los diez retratos ausentes continúan abiertos según CURRENT-AUTHORITIES; estos resultados no certifican exactitud historiográfica mundial.
