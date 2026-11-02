# Quinta parte · humanidad, hielo y transición cultural

Entrega 0.55.0. Base: 58135d26a (0.54.1). La sexta parte, revisión integral, sigue pendiente de encargo. Se conserva la separación entre datos publicados, síntesis editoriales y observaciones del vídeo.

## Qué se puede consultar

- La enciclopedia abre por el contexto humano de la fecha: primeros homininos, australopitecos, Homo temprano, diversidad pleistocena, dispersiones o transición neolítica. Añade diez artículos de procesos y 39 fichas de linajes, propuestas o poblaciones, con fuentes, relaciones, diagramas y doce fotografías originales acreditadas. No son 39 especies aceptadas independientes ni una monografía exhaustiva de todas ellas.
- Las manchas humanas y los yacimientos enlazan con esas fichas. Las fotografías se muestran completas, con `object-fit: contain`; se distingue fósil, réplica y lugar de hallazgo. No se fabrican rostros para especies sin retrato.
- Un comparador permite elegir dos entradas y contrastar sus intervalos, clasificación y disponibilidad cartográfica. Una coincidencia temporal no demuestra contacto, parentesco directo, conflicto ni dominación.
- El artículo de clima incluye la curva de CO₂ de los testigos antárticos y un explorador de muestras. Planeta muestra la misma referencia con su edad del gas, ppm, porcentaje y error declarado, dentro de la consulta prehistórica correspondiente.
- En Capas, «Márgenes mínimo y máximo» permite añadir los dos contornos de incertidumbre de las hipótesis antiguas. Se descargan al activarlos; por defecto sólo se carga la estimación central. Los nuevos recursos están comprimidos sin pérdida y tienen caché acotada.

## Catálogo humano y evidencia

Propietarios canónicos: `Tierra/Humanidad/linajes/<clave>/linaje.json`, `articulo.json` y, cuando existe imagen, `medios.json`. Los artículos de procesos pertenecen a `Tierra/Humanidad/temas`. Las correspondencias y las revisiones contextuales están en `Tierra/Humanidad/revisiones/parte5`.

Las 38 entradas de la lista aportada tienen correspondencia y decisión explícita. El catálogo anterior de 35 se amplía a 39 con gautengensis, Australopithecus sin especie asignada de Ledi-Geraru, Homo temprano sin especie asignada de Ledi-Geraru y la población de Nesher Ramla. No se dibujan cuatro expansiones adicionales: las propuestas alternativas y los conjuntos sin distribución independiente conservan su documentación sin duplicar evidencias.

Se incorporan dos fases regionales a linajes existentes: sapiens en la región de Ranis y contexto denisovano de Harbin. Son envolventes editoriales con incertidumbre espacial de 200 km, no límites biológicos publicados. Se conserva el resto de la geometría anterior, sin simplificar coordenadas. Las 66 geometrías anteriores siguen idénticas; el inventario pasa a 68 ventanas geométricas.

Hay siete referencias fósiles nuevas: tres de Ledi-Geraru, Pink/ATE7-1, Harbin, el molar de Laos y el individuo MZR de Maludong. Se mantienen los 1.000 puntos anteriores y los 982 registros originales de Timmermann sin reescribir sus edades, nombres o atribuciones. El total de esta colección es 1.007; no sustituye la colección arqueológica anterior de 2.820 registros. Las ventanas editoriales alrededor de edades redondeadas se identifican como tales, sin llamarlas errores estadísticos.

Las fichas de Nesher Ramla, Herto, Sima de los Huesos y Denisova añaden contexto de revisión junto a las atribuciones originales. No se asigna a todos los niveles de un yacimiento la especie de un único individuo. Harbin tiene afinidad denisovana molecular; longi se conserva como nombre documentado, sin otra expansión duplicada. Pink se presenta como Homo aff. erectus y no se confunde con antecessor de Gran Dolina.

Las franjas representan solapamiento de áreas reconstruidas. Se mantienen seleccionables todos los grupos. Su grosor puede destacar el filtro activo; no expresa superioridad ni convierte contacto evolutivo en guerra. Denisova 11 sirve como ejemplo documentado de madre neandertal y padre denisovano, separado de la mera coincidencia cartográfica.

## Hielo anterior a PaleoMIST

Fuente: Batchelor et al.2019, [artículo](https://doi.org/10.1038/s41467-019-11601-2), [repositorio original OSF](https://osf.io/7jen3/). Sus 181 archivos originales se conservan con tamaño, SHA-256, procedencia y metadatos en `Tierra/Cuaternario/Batchelor2019`.

Se añaden doce ventanas con tres variantes separadas, para un total de 36 recursos comprimidos:

| Ventana | Edad aproximada ka BP1950 | Activación automática |
| --- | --- | --- |
| MIS 5a | 72–86 | No; síntesis del momento cálido |
| MIS 5b | 86–92 | Sí |
| MIS 5c | 92–108 | No; síntesis del momento cálido |
| MIS 5d | 108–117 | Sí |
| MIS 6 | 132–190 | Sí |
| MIS 8 | 243–279 | Sí; fuente muy incierta |
| MIS 10 | 337–365 | Sí; fuente muy incierta |
| MIS 12 | 429–477 | Sí |
| MIS 16 | 622–677 | Sí |
| MIS 20–24 | 790–928 | Sí; síntesis de varios ciclos |
| Matuyama temprano | 1.780–2.600 | Sólo manual; crono amplio |
| Gauss tardío | 2.600–3.590 | Sólo manual; crono amplio |

PaleoMIST conserva precedencia y geometría hasta su límite real de 80.000 BP. Los huecos entre intervalos no se interpolan ni se rellenan con el contorno vecino. Una síntesis del máximo dentro de MIS6 no representa el frente de cada año de ese intervalo. Las hipótesis mínima y máxima no son percentiles estadísticos universales. Las reconstrucciones MIS8/MIS10 tienen advertencia especial de la fuente.

El alcance de esta nueva síntesis es el hemisferio norte. No se incorpora una Antártida antigua a partir de una plantilla contemporánea, ni se representa hielo marino o la totalidad de los glaciares de montaña. Los shapefiles mínimos contienen algunas geometrías globales de referencia: el compilador conserva esos originales y recorta explícitamente la salida al hemisferio norte. Las exclusiones y sus áreas se registran; no se eliminan polígonos silenciosamente por tamaño.

Cada archivo utiliza su CRS real: la variante máxima de MIS16 viene en WGS84, aunque la mayoría usa la proyección polar Lambert. Se normalizan las coordenadas para reparar/disolver únicamente dentro de la misma variante, recortar el alcance y separar el antimeridiano. No se simplifican vértices. La auditoría conserva los registros degenerados sin área y las exclusiones de alcance. La comparación local de áreas tras reproyección encuentra una diferencia relativa máxima aproximada de 0,0151 %, no un margen de exactitud científica del modelo.

El artículo es CC BY4.0; el repositorio OSF no ofrece una licencia separada en sus metadatos. `rightsNote` conserva esta distinción. Se usan las hipótesis de los autores que acompañan al artículo abierto, con atribución; no se redistribuyen como propias todas las capas empíricas de terceros que las sustentaron.

## CO₂ atmosférico observado

Fuente: Bereiter et al.2015, [colección NOAA/WDS](https://doi.org/10.25921/n8y4-bp27), [artículo original](https://doi.org/10.1002/2014GL061957). Se conservan íntegros el archivo original y sus 1.901 observaciones de edad del gas, CO₂ ppm y error 1σ. La colección emplea edades de calendario BP1950; no se confunden con la edad del hielo ni con b2k2000.

La consulta usa la muestra real más cercana, muestra su propia edad y no extrapola fuera del registro de aproximadamente 806 ka. En el atlas se ofrece como referencia prehistórica hasta 10001 a.C.; no sustituye las observaciones contemporáneas ni rellena las fichas de países con valores de otro periodo. CO₂ ppm/10.000 equivale a porcentaje. Se conserva la precisión original; la presentación en ppm evita redondear incertidumbres pequeñas a cero.

LR04 sigue siendo un contexto isotópico bentónico: combina volumen de hielo y temperatura oceánica profunda. No se convierte en temperatura media global ni en contornos de mantos. Tampoco se reconstruye una paleocosta detallada a partir de la extensión del hielo.

## Reproducción y límites

`scripts/prepare-human-distributions.py --human-only` compila exclusivamente catálogo, distribuciones y referencias humanas; admite `--check`. `scripts/prepare-human-knowledge.py` reúne artículos y medios de sus propietarios y compila el CO₂ original; admite `--check` sin red. `scripts/prepare-quaternary-synthesis.py` transforma los originales del hielo; `--fetch` es una adquisición explícita y `--check` verifica reproducibilidad sin escribir. Sólo la preparación GIS necesita Shapely, pyproj y pyshp; la aplicación y las comprobaciones ordinarias de CI no los necesitan.

Se conservan países, culturas, costas anteriores, modelos PaleoMIST, PhanDA, muestras audiovisuales y la corrección LF/CRLF de 0.54.1. Los cinco candidatos audiovisuales restantes de esta parte se contrastan como contexto: aparición de Homo y sapiens corregidas, crisis mesiniense e inundación zancliense separadas de sus cursores del vídeo, transformación reciente sin una nueva época ratificada supuesta. No se afirma que todos ellos tengan ya geometría regional incorporada.

Pendientes para la revisión integral y ampliaciones posteriores: paleocostas cuaternarias con nivel del mar/isostasia, espesores y animación física de mantos, intervalos glaciales sin reconstrucción, comprobación de más hipótesis regionales de distribución, mejores fotografías donde aún faltan y monografías más extensas. Las áreas humanas actuales son síntesis regionales de consulta, no un modelo demográfico o una simulación de rutas. Parte6 no se inicia automáticamente.
