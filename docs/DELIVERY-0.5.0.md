# Entrega 0.5.0 · actualidad, identidades y espacio de exploración

Fecha: 22/10/2026. Cambios de la entrega y decisiones en agentes.md; cobertura y pendientes en CURRENT-AUTHORITIES; fuentes de agrupaciones/conflictos en CURRENT-LAYERS.

## Implementación

Se corrigen el emparejamiento de QID vacío con España republicana y la unión de metadatos que sobrescribía países con territorios asociados. No se modifican coordenadas para ocultar el problema. La ficha común de búsqueda/clic usa pestañas a la izquierda y todos los mandatos documentados del año. Autoridades en funciones a la referencia se señalan y priorizan dentro de su tipo.

Se incorporan 413 archivos de retrato adicionales: 488 retratos totales y 342 banderas/símbolos. En 2026 hay 508 registros de autoridad, 413 personas u órganos y 402 con imagen en 231 claves. Once ausencias quedan descritas por persona y ámbito, sin usar fotografías ficticias o imágenes de redistribución no acreditada. Las fotos del monarca actual/anterior españoles y Franco están adjuntas a todos sus registros focales.

Temas mañana/tarde/noche/automático con hora local y océano más claro que fondo. Relieve apagado inicialmente, ampliado como referencia moderna desde 10.000 a. C. y excluido de geología. Leyenda a la derecha, escala e información de atribución abajo a la izquierda. Fuentes pasa a panel breve no modal; desaparecen Explorar épocas y el rótulo Escala adaptativa, conservando el zoom de la regla.

Agrupaciones 2026 de OTAN, UE, BRICS y Tres Mares con categorías separadas; rampa estadística verde y siete contextos parciales de conflictos. No hay clasificación mundial exhaustiva de guerra/paz ni ranking de capacidad militar. Esos ámbitos y el detalle cartográfico/histórico pendiente permanecen en roadmap.

## Validación local

- Integridad de 35 recursos, 11 franjas tipográficas y 830 medios mediante SHA-256; 488 retratos raster decodificados correctamente.
- Suite unitaria final: **42 pruebas correctas**, incluidas las correcciones finales de Nauru, Corea y los nombramientos separados de Lecornu.
- 13 recorridos de navegador correctos en 8 minutos, incluidos móvil, temas, panel de fuentes, fichas de ocho países, clic real en Brasil 1947 tras España, indicadores, agrupaciones, fuentes lentas, reproducción, guerras y proyecciones. Dos recorridos exhaustivos (238 años y todos los snapshots) se ejecutan en Quality junto al resto de la suite completa.
- Comprobación focal final de PIB→OTAN→el mismo PIB correcta: no permanece pintura de agrupación al reutilizar datos. Compilación de producción correcta.

## Publicación

Pendiente: documentar el SHA final validado, Quality, checkout de Pages y comprobación de la página pública. No se considera publicada esta versión por haber compilado localmente.
