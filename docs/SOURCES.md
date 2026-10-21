# Fuentes y política cartográfica

Fecha de investigación inicial: 21 de octubre de 2026. Las URLs y revisiones concretas de las descargas se registran en `public/data/manifest.json`. Las coordenadas se conservan; se filtran propiedades y se añaden identificadores y color.

## Datos incorporados

| Fuente | Uso | Licencia | Límites |
| --- | --- | --- | --- |
| [Natural Earth Admin 0, 10m](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/) | Referencia contemporánea: 258 entidades | [Dominio público](https://www.naturalearthdata.com/about/terms-of-use/) | 1:10 millones, generalización global, no vigencia diaria ni precisión local máxima |
| [Natural Earth Vector](https://github.com/nvkelso/natural-earth-vector) | Distribución GeoJSON del origen anterior | Dominio público | Commit de importación fijado en manifiesto |
| [Historical Basemaps, A. Ourednik y colaboradores](https://github.com/aourednik/historical-basemaps) | 13 instantáneas entre 10.000 a. C. y 2010 | GPL-3.0, licencia íntegra en `public/data/LICENSE-historical-basemaps.txt` | Compilación en desarrollo, áreas culturales y políticas, límites difusos/solapados y errores posibles; escala mundial/continental; precisa revisión independiente |
| [GPlates Web Service](https://gwsdoc.gplates.org/reconstruction/reconstruct-coastlines/) | Motor de reconstrucción consultado durante la importación | Servicio de EarthByte / Universidad de Sídney | No se consulta en tiempo de ejecución; se fija el nombre de modelo explícitamente |
| [Cao et al., 2024](https://doi.org/10.1016/j.gsf.2024.101922) · [Datos Zenodo](https://doi.org/10.5281/zenodo.11536686) | Modelo CAO2024, 12 instantáneas entre 1 y 1800 Ma | CC BY 4.0 según registro Zenodo; texto íntegro incorporado | Geometrías reconstruidas en el marco del modelo; no son paleocostas exactas ni superficies climáticas |

Cita del modelo: Cao, X., Collins, A. S., Pisarevsky, S., Flament, N., Li, S., Hasterok, D., and Müller, R. D. (2024). *Earth’s tectonic and plate boundary evolution over 1.8 billion years*. Geoscience Frontiers 15, 101922. DOI: 10.1016/j.gsf.2024.101922.

Las descargas GPlates solicitan `model=CAO2024&wrap=true`, ancla predeterminada 0. No utilizar el modelo predeterminado mutable del servicio. La forma reconstruida no implica una tierra emergida idéntica a esa forma: inundaciones, erosión, acreción, deformaciones y nivel del mar requieren datos específicos.

No se atribuye a Natural Earth una observación de 2026. Ese año es el extremo contemporáneo de la interfaz. El commit y momento de descarga del dataset se encuentran en el manifiesto. Los territorios en disputa necesitan un modelo específico de representación y versiones, pendiente.

## Servicios opcionales en línea

- [Mapzen Terrain Tiles / AWS](https://registry.opendata.aws/terrain-tiles/): mosaicos Terrarium para sombreado topográfico actual, con atribución visible. El registro enlaza a las fuentes de elevación y sus condiciones; no se redistribuyen los tiles en Git. Mantener atribución y revisar condiciones/capacidad antes de tráfico importante.
- MapLibre demo glyphs: fuentes para etiquetas, servicio público de demostración sin garantía de servicio. Migrar a fuentes propias/infraestructura controlada en la siguiente etapa de producción.
- Google Fonts: DM Sans y Libre Caslon Display, cargadas por CSS con alternativas locales. Para soporte offline, obtener versiones con sus licencias OFL y alojarlas localmente.

Las consultas del buscador permanecen en memoria del navegador; sólo hay búsqueda sobre la instantánea cargada. Las conexiones externas anteriores reciben metadatos de conexión normales. No hay analítica, geolocalización ni cuenta de usuario.

## Fuentes del contexto introductorio

- [NASA · Earth facts](https://science.nasa.gov/earth/facts/): formación de la Tierra, antigüedad aproximada.
- [NASA · Moon formation](https://science.nasa.gov/moon/formation/): hipótesis dominante del gran impacto y Theia; no equivale a conocer con certeza la fecha o dinámica de la colisión.
- [NASA · Astrobiology](https://astrobiology.nasa.gov/research/life-detection/about/): contexto de búsqueda e interpretación de evidencias de vida. La versión inicial no atribuye un mapa de vida temprana.
- [International Commission on Stratigraphy](https://www.stratigraphy.org/chart): marco de periodos geológicos; umbrales de interfaz redondeados. No presentar las cifras redondeadas como la tabla estratigráfica oficial completa.
- [Smithsonian Human Origins · Homo sapiens](https://humanorigins.si.edu/evidence/human-fossils/species/homo-sapiens): contexto del origen de la especie; distribución y rutas pendientes.
- UNESCO: [Ahwar y ciudades del sur de Mesopotamia](https://whc.unesco.org/en/list/1481/), [Roma](https://whc.unesco.org/en/list/91/), [Çatalhöyük](https://whc.unesco.org/en/list/1405/). Los marcadores son ubicaciones orientativas del lugar, no perímetros ni fechas exactas de fundación.

## Política de ampliación

Priorizar organismos científicos, repositorios académicos y conjuntos con licencia inequívoca, resolución y cronología documentadas. Fuentes candidatas **no incorporadas ni auditadas aún**: cartografía vectorial detallada derivada de OSM para costa actual, CShapes para fronteras recientes, catálogos arqueológicos/fósiles, modelos de hielo y nivel del mar, Paleobiology Database y modelos paleogeográficos publicados. Verificar cobertura y condiciones vigentes antes de adoptar cada una.

No reutilizar sin licencia mapas de atlas comerciales o imágenes/vídeos de terceros. No equiparar varias representaciones coincidentes con certeza; registrar dependencias entre fuentes y su procedencia original.
