# Homininos y distribuciones regionales

Catálogo natural del atlas, separado de los países y sus autoridades.35 entradas taxonómicas o genéticas; no35 especies aceptadas independientes.24 entradas tienen áreas de consulta;11 alternativas o atribuciones discutidas se documentan sin duplicar poblaciones.

| Entrada | Clasificación | Áreas |
| --- | --- | --- |
| [Paranthropus aethiopicus](linajes/aethiopicus/linaje.json) | especie de referencia | 1 |
| [Australopithecus afarensis](linajes/afarensis/linaje.json) | especie de referencia | 1 |
| [Australopithecus africanus](linajes/africanus/linaje.json) | especie de referencia | 1 |
| [Australopithecus anamensis](linajes/anamensis/linaje.json) | especie de referencia | 1 |
| [Homo antecessor](linajes/antecessor/linaje.json) | especie de referencia | 1 |
| [Australopithecus bahrelghazali](linajes/bahrelghazali/linaje.json) | clasificación alternativa discutida | 0 |
| [Homo bodoensis](linajes/bodoensis/linaje.json) | clasificación alternativa discutida | 0 |
| [Paranthropus boisei](linajes/boisei/linaje.json) | especie de referencia | 1 |
| [Homo cepranensis](linajes/cepranensis/linaje.json) | clasificación alternativa discutida | 0 |
| [Denisovanos](linajes/denisovan/linaje.json) | linaje genético | 3 |
| [Australopithecus deyiremeda](linajes/deyiremeda/linaje.json) | clasificación alternativa discutida | 0 |
| [Homo erectus](linajes/erectus/linaje.json) | especie de referencia | 4 |
| [Homo ergaster](linajes/ergaster/linaje.json) | clasificación alternativa discutida | 0 |
| [Homo floresiensis](linajes/flores/linaje.json) | especie de referencia | 1 |
| [Australopithecus garhi](linajes/garhi/linaje.json) | especie de referencia | 1 |
| [Homo georgicus](linajes/georgicus/linaje.json) | clasificación alternativa discutida | 0 |
| [Homo habilis](linajes/habilis/linaje.json) | especie de referencia | 1 |
| [Homo heidelbergensis](linajes/heidelbergensis/linaje.json) | especie de referencia | 2 |
| [Homo helmei](linajes/helmei/linaje.json) | clasificación alternativa discutida | 0 |
| [Homo juluensis](linajes/juluensis/linaje.json) | clasificación alternativa discutida | 0 |
| [Ardipithecus kadabba](linajes/kadabba/linaje.json) | especie de referencia | 1 |
| [Homo longi](linajes/longi/linaje.json) | clasificación alternativa discutida | 0 |
| [Homo luzonensis](linajes/luzon/linaje.json) | especie de referencia | 1 |
| [Homo naledi](linajes/naledi/linaje.json) | especie de referencia | 1 |
| [Homo neanderthalensis](linajes/neanderthal/linaje.json) | especie de referencia | 3 |
| [Orrorin tugenensis](linajes/orrorin/linaje.json) | especie de referencia | 1 |
| [Kenyanthropus platyops](linajes/platyops/linaje.json) | especie de referencia | 1 |
| [Australopithecus prometheus](linajes/prometheus/linaje.json) | clasificación alternativa discutida | 0 |
| [Ardipithecus ramidus](linajes/ramidus/linaje.json) | especie de referencia | 1 |
| [Homo rhodesiensis](linajes/rhodesiensis/linaje.json) | clasificación alternativa discutida | 0 |
| [Paranthropus robustus](linajes/robustus/linaje.json) | especie de referencia | 1 |
| [Homo rudolfensis](linajes/rudolfensis/linaje.json) | especie de referencia | 1 |
| [Sahelanthropus tchadensis](linajes/sahelanthropus/linaje.json) | especie de referencia | 1 |
| [Homo sapiens](linajes/sapiens/linaje.json) | especie de referencia | 19 |
| [Australopithecus sediba](linajes/sediba/linaje.json) | especie de referencia | 1 |

[Método y límites](../../docs/RESEARCH-HUMAN-DISTRIBUTIONS.md) · [Política cartográfica](metodologia.json).

Las cronologías se expresan en ka BP1950 y ventanas aproximadas, no fechas anuales de aparición o extinción. Las envolventes son editoriales, recortadas sobre costa de referencia; no fronteras biológicas publicadas ni ocupación uniforme. Los fósiles conservan coordenadas actuales, sin rotación individual de placa.

`linajes/<clave>/linaje.json` conserva fuentes, color, fases y referencias fósiles. `fossiles/timmermann2022-anteriores.json` conserva982 intervalos anteriores al tramo0.50, con filas originales, URL/hash del libro, atribuciones y licenciaCC-BY-4.0. No modificar los2820 registros anteriores para añadir estos intervalos.

Compilar desde la raíz con `python scripts/prepare-human-distributions.py` (Shapely y pyproj disponibles). El compilador lee solamente fuentes canónicas del repositorio y recursos incorporados; no depende de descargas o archivos privados de caché. No escribir a mano los GeoJSON derivados.

Usar `python scripts/prepare-human-distributions.py --check` para comprobar reproducción byte a byte sin escribir archivos.
