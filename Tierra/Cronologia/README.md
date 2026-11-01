# Cronología de referencia · 0.52.0

`ics-2026-06.json` contiene177 unidades:4 eones,10 eras,22 periodos,2 subperiodos,37 épocas,101 edades y la agrupación contextual Precámbrico. Procede del RDF oficial archivado en `../Investigacion/parte-1/originales/ics-chart.ttl`, identificado por hash y versión. Etiquetas españolas preferidas de la ICS; para subdivisiones sin etiqueta se construye nombre español del padre + inferior/medio/superior.

La versión del RDF **sí es2026-06** (`owl:versionInfo`, `versionIRI`, modificación20/06/2026). La mención2024-12 en una cita inglesa es texto antiguo. Esto resuelve la duda anotada en la parte1 sin alterar los originales archivados. Carta PDF2026/06 y RDF tienen la misma edición declarada. Valores de ejemplo contrastados: Hádico/Arcaico4031Ma, inicio Fanerozoico538.8Ma, Cuaternario2.58Ma.

Los intervalos del eje son `[axisOldestYear, axisEndYear)`; `null` significa abierto hasta el presente. Las edades Ma de la carta se sitúan **nominalmente** sobre BP1950, sin darles precisión calendárica. No hay año cero. Los márgenes numéricos de la fuente se conservan por extremo. Ausencia de GSSP ratificado no convierte automáticamente una unidad geológica en informal; el estado del GSSP se guarda por separado. Precámbrico y denominaciones provisionales se identifican como contextuales/informales.

Holoceno y sus edades conservan los GSSP ya curados del proyecto:11700,8236 y4250 años **b2k2000**, según [Walker et al.](https://doi.org/10.1002/jqs.3097). Se mantienen también las cifras redondeadas originales de la carta. El mismo límite se aplica al final del Pleistoceno para no crear un hueco de50 años. No se modifica `Tierra/Cuaternario/cronologia.json`.

`edades-humanas.json` inicia23 referencias editoriales/regionales en tres familias: visión general, subdivisiones regionales y transformaciones parcialmente superpuestas. No es una clasificación formal mundial ni un inventario exhaustivo de todas las sociedades. El Neolítico de Francia, por ejemplo, no fecha el comienzo de la agricultura en todo el planeta. Pueblos, culturas y entidades políticas siguen en sus datos propios. La lista admite nuevas regiones y periodizaciones; su ampliación documental corresponde a la parte5.

Preparación y comprobación, desde la raíz del repositorio:

```text
python scripts/prepare-earth-chronology.py
python scripts/prepare-earth-chronology.py --check
```

El segundo comando no escribe. El primer comando sólo produce el vocabulario geológico; las referencias humanas son curación editorial independiente. No consulta la red ni copia curvas del vídeo.

Fuente y licencia: International Commission on Stratigraphy, [carta2026/06](https://stratigraphy.org/ICSchart/ChronostratChart2026-06.pdf), Cohen, Harper, Gibbard & Car (2025, actualizado2026/06), CC BY4.0. Mantener atribución y procedencia al modificar la síntesis.
