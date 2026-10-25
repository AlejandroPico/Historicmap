# Entrega 0.12.1 · 25 de octubre de 2026

Correcciones solicitadas después de confirmar la publicación de 0.12.0. Se aplaza expresamente la ampliación a 1880. Rama de trabajo: `codex/fix-wwii-partitions`, desde `dec2e81685f5776bd99a8107bfae643b1962ad16`.

## Resultado

- Particiones políticas de 1940–1944 sobre una malla terrestre compartida, con sustitución de los territorios afectados. Las manchas remotas no se ocultan con pintura: desaparecen del inventario seleccionable. Una sola geometría alimenta mapa, fronteras, búsqueda y clic.
- Franjas opcionales recortadas al controlador final. Se separan incorporación, ocupación y régimen cliente; el control comunista chino sustituye su porción de China sin duplicarla.
- Misma plantilla de autoridades en todas las épocas. Notas documentales extensas en Contexto, inicialmente plegadas; fechas y límites de cobertura/cese conservados. Cabecera y pestañas fijas.
- 34 originales suizos recuperados, 194 etiquetas institucionales corregidas, presidencia anual y pertenencia al Consejo Federal diferenciadas. Su adquisición preserva todos los mandatos y fechas.
- Continuidad de Eslovaquia 1940–1944, incluidos Tiso, el relevo Tuka/Štefan Tiso de septiembre de 1944 y un retrato adicional. Se mantienen las declaraciones de 1939 y los límites de cobertura explícitos.

Detalle y reglas editoriales: [WWII-PARTITIONS](WWII-PARTITIONS.md), [auditoría geométrica](WWII-PARTITIONS-AUDIT.json), [diagnóstico y fuentes](WWII-CONTROL-RESEARCH.md), [retratos y permisos](PORTRAITS-0.12.1-RESEARCH.md). Totales: 302 claves, 10.246 declaraciones de mandatos; 5.297 medios (499 SVG y 4.798 fotografías), 45 recursos de datos y 11 franjas tipográficas. El catálogo conserva 2.792 carpetas y extensiones manuales. Los recursos geográficos originales no cambian.

## Comprobaciones locales

- 147 pruebas unitarias en 33 archivos y tipos correctos. Regresiones para los cinco años, lugares negativos y positivos, islas, clientes, incorporación/ocupación, China, identificadores, plantilla uniforme, cargos suizos y sucesión eslovaca.
- Auditoría de preparación: conservación de la tierra de entrada, sin tierra añadida ni nuevos solapamientos; áreas protegidas sin intersección alemana salvo redondeo; franjas contenidas en su controlador final. Las tolerancias y magnitudes reales figuran en el JSON, sin presentarse como superficies nacionales.
- Verificación SHA-256 de datos, letras y todos los medios. Adquisición suiza pura/idempotente, 34 originales decodificados, 33 autorizaciones positivas y 198 variantes negativas. Curador eslovaco puro/idempotente; fuera de CHE y SVK-1939, las identidades anteriores permanecen iguales.
- Compilación de producción correcta en `.cache/build-0121-verified`. Se usa una carpeta nueva para evitar el bloqueo local previo de `dist/media`. Tras resolver el hueco eslovaco sólo cambiaron datos estáticos, sincronizados al mismo build con SHA comprobado; el código compilado permanece igual.
- Navegador: **siete recorridos distintos correctos**. Incluyen 1939, 1900–1919, 1950, los dos recorridos políticos previos y los dos nuevos de particiones/presentación. La primera pasada completó seis y detectó falta de autoridades eslovacas posteriores a 1939 en el séptimo; se corrigió el dato. La repetición confirmó 1939 y la carga de GIF/formato italiano; una expectativa nueva intentaba buscar un territorio independiente eslovaco en 1944, cuando su geometría pertenece al controlador alemán. Se corrigió esa expectativa para conservar su ficha abierta desde 1943, sin reintroducir un país ficticio. La ruta final 1940–1944 pasa en 1,3 min, con clics reales neutrales, franjas, cliente eslovaco y sus gobiernos de 1944. Revisión visual de capturas de 1942 con selección/franjas: sin las manchas denunciadas en Suecia/Italia y fronteras compartidas.
- Los bytes preparados en Git de **5.353 recursos** (45 datos, 11 franjas y 5.297 medios) coinciden con sus huellas. Las comprobaciones no esperan un despliegue remoto.

La primera suite unitaria se ejecutó antes de regenerar el catálogo y señaló su desfase. Otra repetición, simultánea a la compilación, superó el límite de 5 segundos en una prueba antigua de suplementos. Con catálogo actualizado y sin esa competencia de recursos, las suites completas posteriores pasan. No se retiraron aserciones históricas para ocultar esos fallos.

## Comprobación de la publicación anterior

Se consultaron los archivos públicos tras el aviso del propietario. Manifiesto y fuentes de controles coincidían byte por byte con 0.12.0, confirmando que el error seguía en esa versión:

| Recurso | SHA-256 público de 0.12.0 |
| --- | --- |
| data/manifest.json | a163f537fcbf4513bc337b052b57d06b4fcf33abaf848024ca14e051ee709e11 |
| data/historical-control.geojson | b22616faaa36ac5c39908ab13f3b6aedafca02bff4bb823932bcdc018755e682 |
| data/central-europe-1939.geojson | 000574cce08be157112f6c5f536631eb4d8f58e31da854e280878e271bc9e718 |

## Límites y siguiente paso

La corrección resuelve artefactos y composición, no reconstruye todos los frentes diarios. Persisten las fases desiguales de las síntesis de 1942–1944, liberaciones, RSI, partisanos y la frontera eslovaca de referencia. La nueva plantilla y los retratos no validan todas las fechas ni completan el colegio suizo; sus carencias precisas quedan en `tareas.md`. No se amplía a 1880 ni se da por corregido cada conflicto del atlas.

La autorización es comprobar localmente y subir a main. Terminar al confirmar el envío, sin consultar ni esperar Actions/Pages. El propietario notificará el despliegue o un error; una subida correcta no acredita publicación de 0.12.1.
