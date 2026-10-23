# Entrega 0.7.0 · fichas persistentes y herramientas de investigación

Fecha de preparación: 23/10/2026. Solicitud: desplegar los apartados y herramientas acordados, mantener fichas/paneles abiertos durante cambios de año y preparar la ampliación anual de datos sobre un concepto más completo.

## Realizado

Doce apartados con datos y fuentes; selección estable entre periodos, controles por UID y ciudades por nombre/identidad; ausencia explícita de entidades desaparecidas y navegación dirigida. Pestaña y lectura conservadas durante fecha/carga/reproducción. Búsqueda, capas y fuentes también persisten. Comparación de dos fechas y hasta cuatro entidades fijadas, gráficos con tablas accesibles, cronología filtrada/navegable y relación entre entidades históricas. Descripción y contratos en COUNTRY-WORKSPACE.

Datos adicionales: 22 indicadores, 217 economías, 175.996 observaciones de 1960–2025; 33 relaciones y 28 registros con 36 fuentes institucionales. Manifiesto pasa a 41 recursos; no hay nuevos retratos ni cambios de coordenadas. Alcance y licencias en COUNTRY-INDICATORS y COUNTRY-HISTORY.

## Verificación local

Integridad de 41 recursos, 11 franjas tipográficas y 2.871 medios correcta. 58 pruebas unitarias en 13 archivos correctas; TypeScript y compilación correctos. Siete recorridos focales correctos antes del pulido final de capitales/fechas/campos. El recorrido completo incorpora una antigua comprobación que exigía cerrar la ficha al pasar de 1937 a 1947: se actualiza al nuevo contrato (ficha del bando republicano conservada como ausente, sin contaminar Brasil). Una comprobación adicional valida diferencias de porcentajes del PIB en puntos porcentuales. Recorrido completo: 20/22 correctos en 15,7 minutos. Las dos comprobaciones pendientes eran contratos anteriores: cerrar la ficha al cambiar de año y exigir la ausencia de la etiqueta «PIB nominal» en todo el DOM de 1942. Se actualizan para conservar la ficha y comprobar ausencia de valores/años futuros en Datos y Economía, manteniendo el clic real de Brasil y el recorrido WWII. La compilación final supera las seis pruebas focales (2,4 minutos): persistencia/reproducción/lectura, entidad desaparecida y sucesor, comparación/teclado del gráfico, paneles abiertos, clic real en Brasil y recorrido WWII. Compilación: JS `index-DWRzUWMW.js`, CSS `index-b0OcPlkX.css`. Se comprueban también los bytes preparados en Git de los 2.923 recursos de datos/tipografías/medios. Registrar Quality del SHA publicado.

## Publicación

Publicado **d6a8cfb4119edcf77d50f2133de46111aa5472bb** en [Historicmap](https://alejandropico.github.io/Historicmap/), comprobado el 23/10/2026 desde las 01:08 UTC.

- [Quality 39881593494](https://github.com/AlejandroPico/Historicmap/actions/runs/39881593494): correcto; logs con 41 recursos, 11 franjas y 2.871 medios íntegros, **58 pruebas unitarias en 13 archivos y 22 recorridos de navegador correctos en 4,8 minutos** sobre el SHA final, incluidos todos los años 1789–2026 y los dos contratos actualizados.
- [Publish atlas 39882159743](https://github.com/AlejandroPico/Historicmap/actions/runs/39882159743): correcto; checkout real y despliegue de **d6a8cfb4119edcf77d50f2133de46111aa5472bb** confirmados en logs. Se canceló la validación intermedia de 864b4d4 para evitar publicar una revisión anterior tras la final; no se eludió la validación de d6a8cfb.
- Web pública: JS `assets/index-DWRzUWMW.js` y CSS `assets/index-b0OcPlkX.css`, con bytes idénticos al build final. Tres manifiestos idénticos a los locales; descargas completas de `country-indicators.json` (3.567.821 bytes) y `country-history.json` (45.459 bytes) con SHA-256 coincidente. Informe local ignorado: `.cache/public-verification-0.7.0.json`.
- Revisión visual pública de España: doce apartados; la ficha Economía permanece abierta al cambiar 2026→2000 y muestra bandera/observaciones/fecha de 2000. Evidencia local ignorada: `.cache/release-0.7.0-public-2000.jpg`. Revisión local final de comparación de España 2016/2026 con créditos de ambas banderas, autoridades, tabla y gráfico.
- La pestaña de entrega se recarga en la web pública conservando 1999 y globo. Se cierra la pestaña temporal y se detiene el servidor local propio. El cierre documental usa `[skip ci]` sin modificar la aplicación validada.

## Límites

Instituciones, contextos y relaciones siguen siendo inventarios parciales. Las categorías y los campos ampliables no son datos adquiridos de todas las constituciones, idiomas, religiones, sanciones, socios comerciales, bases o lugares históricos. Personal militar sólo hasta 2020; gasto SIPRI no redistribuido. Observaciones de indicadores conservan sus años y ámbito de fuente, no se recalculan sobre polígonos históricos ni son vintages de publicación. Entidades desaparecidas no heredan datos de sucesores. Continúan las carencias de retratos, etiquetas repetidas al ampliar y cartografía documentadas en versiones anteriores.

La última compilación añade créditos de autor/licencia a cada bandera de comparación y proveedor/licencia a los gráficos. Conserva las 58 pruebas unitarias correctas; el SHA final supera Quality completo según los resultados anteriores.
