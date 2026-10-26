# Ucrania: control territorial ruso desde 2022

Investigación y preparación: 25/10/2026. Referencia contemporánea del atlas: 22/10/2026. Este documento describe candidatos cartográficos y sus límites; la existencia del preparador no implica que estén publicados.

## Resultado utilizable y límite temporal

Se han recuperado cinco revisiones originales del [mapa vectorial de Wikimedia Commons](https://commons.wikimedia.org/wiki/File:2022_Russian_invasion_of_Ukraine.svg), con licencia **CC BY-SA 4.0** declarada en la ficha. Se extraen sus superficies sólidas de control ruso, incluida Crimea, y se georreferencian. No se convierten las reclamaciones administrativas rusas en control efectivo ni se dibujan óblasts completos por el mero hecho de estar reclamados.

**No hay aquí un frente verificado de octubre 2026.** Los siete trazados de control de la revisión de 24/4/2026 son idénticos a los de la revisión de 22/12/2025. La actualización territorial documentada en su historial utiliza la evaluación de **17/12/2025**. El archivo de 2026 sirve para comprobar esa continuidad editorial, no para afirmar que el frente permaneció inmóvil durante 2026.

| Año consultado | Archivo SVG archivado | Última actualización cartográfica territorial identificada | Fecha de evaluación indicada por el editor |
| --- | --- | --- | --- |
|2022|31/12/2022,15:23 UTC|31/12/2022,00:37 UTC; contraataque al sur de Bakhmut|No expresa un día independiente de evaluación|
|2023|30/12/2023,11:58 UTC|27/12/2023; control de Marinka|No expresa un día independiente de evaluación|
|2024|29/12/2024,02:09 UTC|29/12/2024; actualización territorial|No expresa un día independiente de evaluación|
|2025|22/12/2025,16:50 UTC|20/12/2025,18:05 UTC|17/12/2025, indicada expresamente en el comentario|
|2026|24/4/2026,01:38 UTC|Mismos trazados que diciembre 2025|17/12/2025; referencia heredada, no observación nueva|

El corte anual, la revisión del archivo, la actualización del dibujo y la fecha de evaluación son campos distintos. `observationDate` en el candidato significa **referencia de la fuente cartográfica** (`observationKind=cartographic-source-reference`); `reportedAssessmentDate` sólo se rellena cuando el comentario editorial expresa una fecha. Los comentarios y respuestas de la API originales se conservan localmente para auditoría. Los nombres de archivo del servidor de Commons contienen la fecha de sustitución de una versión, que puede ser posterior al corte: **no es la fecha del frente**.

Para 2026 debe mostrarse «Última referencia cartográfica disponible: 17/12/2025». No presentar estos datos como una reconstrucción diaria ni como control militar actual. Para los primeros tres años la fecha sólo acredita una actualización del mapa, no una observación militar independiente tomada ese día.

## Archivos y reproducción

- Preparador independiente: `scripts/prepare-ukraine-2022-svg.py`.
- Originales sin modificar: `.cache/ukraine-014/2022-12-31.svg` y equivalentes 2023,2024,2025 y `2026-10-22.svg`.
- Candidato: `.cache/ukraine-014/control-candidates.geojson`, cinco entidades anuales.
- Auditoría: `.cache/ukraine-014/control-candidates.audit.json`, con huellas, trazados, ajuste, controles, incertidumbre y puntos de comprobación.
- Descargas y metadatos originales: `.cache/ukraine-014/commons-*.json`, `commons-revisions-2022.json`, `commons-revisions-2023.json`, `commons-revisions-2024.json` y `commons-recent-revisions.json`.
- Copia del contenido de Wikidata usado para comprobar nombres/coordenadas: `.cache/ukraine-014/landmark-entities.json`. El preparador fija las 16 coordenadas verificadas y sus QID; no necesita consultar Wikidata al reconstruir.

El preparador incluye las cinco URL archivadas, tamaños y SHA-256 esperados. Exige archivos originales exactos, no descarga nada, no ejecuta trabajo al importarse y rechaza salidas en `public/` o `src/`. Sus dependencias de preparación son NumPy, pyproj, Shapely 2, svgpathtools 1.8.0 y svgwrite; no añade dependencias al navegador.

```powershell
python scripts/prepare-ukraine-2022-svg.py --input-dir .cache/ukraine-014 --output .cache/ukraine-014/control-candidates.geojson
```

Después de clonar sin caché, recuperar los cinco originales de las URL fijadas en `SNAPSHOTS` y conservar exactamente los nombres indicados. Las huellas impiden confundir una versión posterior o un resultado HTTP con el SVG esperado. La adquisición y el preparado son pasos separados.

## Extracción y registro geográfico

1. Leer el SVG con un analizador XML. Resolver todos los cambios de coordenadas del elemento y sus antecesores, incluida la reorganización de grupos introducida en 2025/2026.
2. Seleccionar únicamente trazados visibles con relleno sólido **`#ebc0b3`**. Las propiedades `style` prevalecen sobre atributos XML. Se excluyen definiciones, leyendas, marcadores, flechas, gradientes y trazados sin relleno. En 2023–2026 `path453` conserva un atributo de color antiguo pero declara `style=fill:none`: **no es una superficie adicional**.
3. Interpretar todos los comandos de trazado SVG con svgpathtools. Aproximar las curvas con error de cuerda adaptativo de 0,2 unidades del trazado original; cerrar subtrazados como prescribe el relleno SVG. Respetar `evenodd`/`nonzero` y los huecos, sin sustituir regiones por envolventes convexas.
4. Ajustar una transformación afín desde la cuadrícula SVG a una proyección cilíndrica equidistante con paralelo 49° (`+proj=eqc +lat_ts=49 +datum=WGS84`). Es un **modelo de registro ajustado**, no un sistema de referencia declarado por el autor. En la comparación ensayada, Mercator, cilíndrica equivalente y Lambert ofrecían mayor residuo con los mismos puntos.
5. Usar 16 centros de marcadores urbanos, desde Uzhhorod/Lviv hasta Luhansk y desde Chernihiv/Sumy hasta Sevastopol/Simferopol. Las coordenadas geográficas se verificaron en P625 de Wikidata, CC0. El informe conserva nombre, QID, coordenada SVG, coordenada geográfica, residuo y validación dejando cada punto fuera del ajuste.
6. Comprobar que las 16 posiciones permanecen en la misma cuadrícula entre revisiones: el desplazamiento máximo aceptado es 0,1 píxeles. Aplicar **el mismo ajuste a todos los archivos**, evitando convertir cambios mínimos en posiciones de etiquetas en falsos movimientos territoriales. Los dos candidatos 2025/2026 tienen geometría idéntica.

Resultado: residuo medio aproximado **2,16 km**, máximo **5,02 km**, máximo de validación cruzada **6,3 km**. Se declara **incertidumbre mínima 7 km**. No es un intervalo estadístico de confianza ni cuantifica todo el error del frente: también hay generalización, selección editorial y desfases de las fuentes.

El control se valida como ruso en Simferopol, Sevastopol, Mariupol y Melitopol y como ucraniano en Kyiv, Kharkiv, Odesa y Zaporizhzhia. Bakhmut/Avdiivka cambian según las versiones. Los puntos próximos al borde no son pruebas fiables de control urbano: **Kherson 2022 queda a unos 276 m del borde transformado y puede caer en el lado ocupado por el error de registro**, aunque el propio SVG identifica la ciudad como ucraniana. La auditoría lo marca dentro de la incertidumbre. No usar el candidato para afirmar la ocupación de Kherson en diciembre 2022 ni para localizar una línea exacta sobre el Dniéper.

## Integración geográfica y licencias

Los trazados de color del SVG incluyen agua situada bajo las máscaras marinas del dibujo original. **El candidato bruto no puede pintarse directamente.** Como control de magnitud, antes del recorte arroja unos 137.616 km² en 2022; al intersectarlo sólo con la tierra contemporánea Natural Earth de UKR/RUS queda aproximadamente 105.236 km². Es una medida de diagnóstico en la proyección de registro, no una estadística oficial de superficie ocupada. El mismo diagnóstico para 2025 da unos 114.088 km².

La integración debe:

- Recortar contra una costa común de **Natural Earth, dominio público**, con un ámbito ucraniano explícito. La geometría NE actual coloca Crimea en RUS; conservar Crimea dentro del ámbito de investigación no implica aceptar su anexión. No dejar que el uso de una máscara RUS completa introduzca territorios remotos ni confundir incursiones en Rusia con ocupación de Ucrania.
- Sustituir la partición política: restar el área ocupada al área ucraniana visible y asignar al controlador la misma superficie exacta, con una sola frontera compartida. La trama opcional representa ocupación, no crea otra geometría política incompatible.
- Conservar la identidad del territorio ocupado y su fuente. El color/control ruso **no significa incorporación soberana reconocida**. No atribuir un país aliado a Rusia por una alianza.
- No mezclar este derivado CC BY-SA con la máscara histórica Crimea de CShapes NC-SA. Para 2022+ utilizar una rama moderna PD + CC BY-SA y suprimir el duplicado anterior de Crimea sólo durante esos años. Mantener intacta la fuente 2014–2021.
- Conservar atribución, aviso de transformación, URL, revisión y licencia; publicar el derivado geográfico bajo CC BY-SA 4.0. No confundir la licencia de estos datos con la del código del proyecto ni sublicenciar todo el atlas automáticamente.

Atribución propuesta: «Viewsridge y colaboradores de Wikimedia Commons, a partir de Rr016 y YakivGluck. Extracción y georreferenciación: Historicmap. CC BY-SA 4.0». Incluir enlace a la [ficha e historial de colaboradores](https://commons.wikimedia.org/wiki/File:2022_Russian_invasion_of_Ukraine.svg#filehistory), [licencia](https://creativecommons.org/licenses/by-sa/4.0/) e indicar el recorte sobre Natural Earth. La ficha acredita también el mapa administrativo base y las compilaciones territoriales empleadas por sus autores. Esta vía reutiliza el dibujo con licencia de Commons; no descarga ni redistribuye la geodatabase de ISW.

## Fuentes alternativas revisadas

| Fuente | Hallazgo | Decisión |
| --- | --- | --- |
|[DeepState, términos oficiales](https://deepstatemap.live/license.html)|Permite ciertos usos visuales atribuidos y acceso API bajo condiciones; prohíbe redistribuir/publicar/proxificar datos API sin autorización. La gratuidad para algunos usos no es una licencia general del dataset.|No importar su API como fuente redistribuible sin aclaración expresa.|
|[cyterat/deepstate-map-data](https://github.com/cyterat/deepstate-map-data)|Repositorio con GPL 3 y GeoJSON diarios; no demuestra por sí solo que el proveedor haya autorizado la redistribución de la geometría original.|Candidato técnico, derechos de origen pendientes.|
|[ISW, elemento ArcGIS](https://www.arcgis.com/home/item.html?id=733fe90805894bfc8562d90b106aa895)|La ficha reserva la geodatabase y exige consentimiento escrito para usarla.|No importar los polígonos API por el hecho de que una consulta responda.|
|[OCHA, servicio de 18/8/2025](https://gis.unocha.org/server/rest/services/Hosted/Front_Line_as_of_18_August_2025/FeatureServer/0)|Frente lineal acreditado a ISW; además aclara que no es control territorial.|No convertirlo sin más en polígonos ni presuponer una licencia abierta de ISW.|
|[VIINA](https://github.com/zhukovyuri/VIINA)|ODbL explícita para la base y DbCL para contenidos. Serie diaria de localidades y clases UA/RU/CONTESTED desde 2022, con teselaciones de referencia.|Vía viable para una futura capa de **localidades**. Unir sus celdas no convierte una estimación de influencia en frente observado.|
|[Cartoteca SciencesPo](https://www.sciencespo.fr/cartographie/en/cartotheque/la-guerre-en-ukraine-en-quatre-cartes-fevrier-2022-fevrier-2-2062)|CC BY-NC-ND 4.0.|No extraer/adaptar las líneas de una obra ND.|

## Pendientes expresos

- Obtener una actualización geográfica autorizada con evaluación real de 2026; el candidato actual permanece en 17/12/2025.
- Reducir el error de registro y contrastar curvas del Dniéper, Kherson, islas, frentes próximos a poblaciones y detalles limítrofes. No resolverlos pintando óblasts enteros ni inventando sectores.
- Si se desea navegar por fechas dentro de cada año, adquirir observaciones adicionales fechadas: los cinco candidatos no constituyen una serie diaria ni representan todas las fases de 2022.
- Mantener los originales, huellas y atribución al integrar y publicar. La caché local es ignorada por Git; una entrega reproducible debe conservar los datos preparados y la documentación de adquisición que el integrador decida registrar.

## Comprobación local de la preparación

El preparador se ejecutó correctamente para las cinco revisiones fijadas: geometrías válidas y no vacías, huellas exactas, comprobaciones urbanas y registro cruzado conservados en la auditoría. Se confirmó igualdad exacta entre las geometrías de 2025 y 2026. Se inspeccionó visualmente el diagnóstico `.cache/ukraine-014/registration-land-check.png`, que compara 2022,2024 y 2025 después de un recorte de prueba a la tierra NE. Esta comprobación no modifica los datos públicos ni sustituye la revisión visual que necesita la integración del atlas.
