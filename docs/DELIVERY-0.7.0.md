# Entrega 0.7.0 · fichas persistentes y herramientas de investigación

Fecha de preparación: 23/10/2026. Solicitud: desplegar los apartados y herramientas acordados, mantener fichas/paneles abiertos durante cambios de año y preparar la ampliación anual de datos sobre un concepto más completo.

## Realizado

Doce apartados con datos y fuentes; selección estable entre periodos, controles por UID y ciudades por nombre/identidad; ausencia explícita de entidades desaparecidas y navegación dirigida. Pestaña y lectura conservadas durante fecha/carga/reproducción. Búsqueda, capas y fuentes también persisten. Comparación de dos fechas y hasta cuatro entidades fijadas, gráficos con tablas accesibles, cronología filtrada/navegable y relación entre entidades históricas. Descripción y contratos en COUNTRY-WORKSPACE.

Datos adicionales: 22 indicadores, 217 economías, 175.996 observaciones de 1960–2025; 33 relaciones y 28 registros con 36 fuentes institucionales. Manifiesto pasa a 41 recursos; no hay nuevos retratos ni cambios de coordenadas. Alcance y licencias en COUNTRY-INDICATORS y COUNTRY-HISTORY.

## Verificación local

Integridad de 41 recursos, 11 franjas tipográficas y 2.871 medios correcta. 58 pruebas unitarias en 13 archivos correctas; TypeScript y compilación correctos. Siete recorridos focales correctos antes del pulido final de capitales/fechas/campos. El recorrido completo incorpora una antigua comprobación que exigía cerrar la ficha al pasar de 1937 a 1947: se actualiza al nuevo contrato (ficha del bando republicano conservada como ausente, sin contaminar Brasil). Una comprobación adicional valida diferencias de porcentajes del PIB en puntos porcentuales. Recorrido completo: 20/22 correctos en 15,7 minutos. Las dos comprobaciones pendientes eran contratos anteriores: cerrar la ficha al cambiar de año y exigir la ausencia de la etiqueta «PIB nominal» en todo el DOM de 1942. Se actualizan para conservar la ficha y comprobar ausencia de valores/años futuros en Datos y Economía, manteniendo el clic real de Brasil y el recorrido WWII. La compilación final supera las seis pruebas focales (2,4 minutos): persistencia/reproducción/lectura, entidad desaparecida y sucesor, comparación/teclado del gráfico, paneles abiertos, clic real en Brasil y recorrido WWII. Compilación: JS `index-C1Vn9tE5.js`, CSS `index-b0OcPlkX.css`. Se comprueban también los bytes preparados en Git de los 2.923 recursos de datos/tipografías/medios. Registrar Quality del SHA publicado.

## Publicación

Pendiente de registrar SHA publicado, Quality, checkout real de Pages, manifiestos y comprobación visual pública. Un resultado local no equivale a publicación.

## Límites

Instituciones, contextos y relaciones siguen siendo inventarios parciales. Las categorías y los campos ampliables no son datos adquiridos de todas las constituciones, idiomas, religiones, sanciones, socios comerciales, bases o lugares históricos. Personal militar sólo hasta 2020; gasto SIPRI no redistribuido. Observaciones de indicadores conservan sus años y ámbito de fuente, no se recalculan sobre polígonos históricos ni son vintages de publicación. Entidades desaparecidas no heredan datos de sucesores. Continúan las carencias de retratos, etiquetas repetidas al ampliar y cartografía documentadas en versiones anteriores.
