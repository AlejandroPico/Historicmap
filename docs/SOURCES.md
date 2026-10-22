# Fuentes y política cartográfica

Fecha de investigación inicial: 21 de octubre de 2026. Ampliación histórica/económica: 22 de octubre de 2026. URLs, revisiones y transformaciones concretas en `public/data/manifest.json`. Se conservan las coordenadas de las bases; los polígonos contextuales derivados se identifican expresamente.

## Ampliación 0.4

- `early-modern.geojson`: 1.715 registros componentes de Cliopatria para 1789–1885, coordenadas originales, sin duplicar las uniones agregadas. Intervalos inclusivos y MemberOf conservado; sin fecha diaria uniforme. CC BY 4.0. Las áreas no cubiertas tienen fondo costero contemporáneo gris sin identidad política atribuida.
- `history.topojson`: incorpora ahora todos los 710 registros CShapes desde 1886; cambia el filtro temporal, no las coordenadas ni la licencia NC-SA.
- `historical-control.geojson`: 57 registros Cliopatria para potencias centrales en 1914–1918, extensiones de Alemania/Japón/Italia/URSS, Croacia, Vichy y control comunista chino. Colores opacos por potencia, relaciones diferenciadas; aliados no clasificados automáticamente como clientes. CC BY 4.0. Sustituye en navegación a `ww2.geojson`, que se conserva como fuente de la entrega anterior.
- `spanish-civil-war.geojson`: siete registros 1936–1939. Frentes Cliopatria y vector de octubre de 1937 de Tyk / Té y kriptonita, georreferenciado, con exterior Natural Earth. [Transformación, incertidumbre ≥10 km y atribución](SPANISH-CIVIL-WAR.md). CC BY 4.0 para 1936/1938/1939, CC BY-SA 3.0 para 1937, costa en dominio público. No mezcla con geometrías NC-SA de CShapes.
- `identities.json` y `media/manifest.json`: [autoridades, banderas y retratos](IDENTITIES.md), con intervalos y licencias por imagen. Wikidata CC0 para metadatos no implica CC0 para las imágenes. Sin sustitutos actuales en épocas no documentadas.

Reconstruir con `scripts/acquire-history.py`, `scripts/prepare-history.py`, `scripts/prepare-extended-history.py`, `scripts/prepare-spanish-fronts.py` y `scripts/prepare-identities.py`; después `node scripts/register-political-data.mjs`, `npm run data:audit` y `npm run data:verify`. La preparación de frentes requiere Shapely 2.2.0, NumPy y pyproj 3.7.2; son herramientas de construcción, no dependencias del navegador. No se consulta ninguna fuente remota al compilar.

## Base de datos conservada y ampliada

Ver [ANNUAL-REVIEW.md](ANNUAL-REVIEW.md): inventario de **todos los años 1789–año del dispositivo**, diferencias y excepciones. No se considera certificación manual exhaustiva.

| Recurso | Origen y alcance | Transformación y licencia |
| --- | --- | --- |
| `history.topojson` | [CShapes 2.0, ETH Zürich](https://icr.ethz.ch/data/cshapes/), GW con dependencias, 710 registros que alcanzan 1886–2019 | TopoJSON no cuantizado del paquete R 2.0, coordenadas intactas; se conservan estatus, administrador y capital. [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), texto local LICENSE-CShapes.txt. |
| `ww2.geojson` | [Cliopatria, Seshat](https://github.com/Seshat-Global-History-Databank/cliopatria), 20 registros de Alemania/Japón/Italia para 1938–1944 | Selección temporal, nombres en español y notas; coordenadas intactas. CC BY 4.0. No fija un día uniforme dentro del año ni distingue exhaustivamente anexión, influencia y ocupación. |
| `territorial-overlays.geojson` | Diferencias espaciales de CShapes: Ucrania 2013/2014, Egipto 1966/1968 y Siria 1966/1968 | Cinco registros, polígonos calculados con Shapely y notas documentales. Derivados CC BY-NC-SA 4.0. Sin dibujar a mano la costa ni inventar fases de retirada. |
| `cities.geojson` | [Natural Earth populated places 1:10m](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/), mismo commit de países | 323 capitales nacionales, world cities o lugares con POP_MAX ≥ 2,5 millones. Dominio público. POP_MAX sólo filtra/ordena: **no se publica como población urbana fechada**. Uso contemporáneo desde 2020; antes se extraen capitales históricas del registro CShapes. |
| `profiles.json` | [Banco Mundial WDI](https://data.worldbank.org/), API v2 `source=2`, seis indicadores desde 1960 y metadatos de países; nombres de Natural Earth | Sin agregados regionales ni valores nulos, observaciones conservan año. CC BY 4.0 y [términos adicionales del Banco Mundial](https://datacatalog.worldbank.org/public-licenses). URLs y versiones de las seis consultas en el propio recurso. |

CShapes: Schvitz, G., Rüegger, S., Girardin, L., Cederman, L.-E., Weidmann, N., Gleditsch, K. S. (2022), *Mapping the International System, 1886–2019: The CShapes 2.0 Dataset*, Journal of Conflict Resolution 66(1), 144–161. DOI [10.1177/00220027211013563](https://doi.org/10.1177/00220027211013563). Se usa el archivo del paquete R porque el GeoJSON publicado por el proveedor omite propiedades de administración/estatus. Los SHA-256 de ambos archivos de origen adoptados (R y zip Cliopatria) se registran en el manifiesto; la adquisición rechaza cambios de bytes no revisados.

El [codebook de CShapes](https://icr.ethz.ch/data/cshapes/CShapes-2.0_Codebook.pdf) excluye cambios pequeños y muchas ocupaciones reversibles durante guerras. Algunos límites se retrotraen cuando no hay evidencia de cambio, algunas fechas son convencionales y sus casos no equivalen siempre a soberanía universalmente reconocida. No basta con añadir este conjunto para declarar correctos todos los frentes del siglo XX.

Correcciones de aplicación: desde 1967, la base de Egipto, Israel y Siria usa su contorno de 1966 para separar ocupación de incorporación soberana; los polígonos de Sinaí/Golán superpuestos explican la situación. En 1979–1981 se señala retirada parcial sin atribuir una línea exacta. La retirada principal del Sinaí se completa en 1982, Taba en 1989; el contorno de Taba no está incorporado. Crimea aparece diferenciada desde 2014 con soberanía ucraniana según [A/RES/68/262](https://press.un.org/en/2014/ga11493.doc.htm). Los frentes de Ucrania de 2022 en adelante no se deducen de ese polígono.

Indicadores: `SP.POP.TOTL` (habitantes), `NY.GDP.MKTP.CD` (PIB en US$ corrientes), `NY.GDP.PCAP.CD` (US$/habitante), `SP.DYN.LE00.IN` (esperanza de vida, años), `SP.URB.TOTL.IN.ZS` (porcentaje urbano), `AG.SRF.TOTL.K2` (superficie, km²). Se selecciona la última observación **no posterior** al año consultado y con retraso máximo de cinco años. No interpolar, extrapolar ni convertir ausencias en ceros. Cada indicador muestra su año; las series se refieren a las economías del proveedor, no a cálculos espaciales sobre cada frontera histórica. Las entidades sin correspondencia fiable (URSS, Yugoslavia, RDA, dependencias históricas) no heredan estadísticas de sus sucesoras.

### Reproducción de la importación reciente

La compilación y CI sólo utilizan archivos locales. Para reconstruir explícitamente:

1. `python scripts/acquire-history.py`: descarga las versiones fijadas, verifica sus huellas y extrae exclusivamente los archivos de datos nombrados.
2. `npm run data:fetch:modern`: obtiene países/ciudades Natural Earth del commit ya fijado y WDI. Usa caché `.cache/`; para actualizar deliberadamente WDI, retirar sólo sus archivos `wb-*` de la caché. Revisar cambios y años de observación antes de publicar.
3. Preparar Shapely **2.2.0** en un entorno Python o `.cache/python-packages`: `python -m pip install --target .cache/python-packages shapely==2.2.0`.
4. `python scripts/prepare-history.py`: construye recursos y actualiza manifiesto. No simplifica las coordenadas base; calcula diferencias para las capas contextuales.
5. `npm run data:verify`, `npm run data:audit`, `npm test`, compilación y recorridos de navegador. Revisar el informe anual y los casos de conflicto manualmente.

`npm run data:fetch` sigue gestionando sólo las 26 instantáneas originales y conserva las capas nuevas. Los datos derivados no cambian de licencia por formar parte del mismo sitio; la colección mantiene separados los recursos NC-SA, BY, GPL y dominio público.

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

No se atribuye a Natural Earth una observación diaria de 2026: es el año en que se incorporó esta referencia al atlas. El extremo de la interfaz procede del dispositivo. Desde 2020 se usa esa base contemporánea, no instantáneas históricas independientes. Las capas de disputa incorporadas son parciales; el registro completo de control efectivo mundial está pendiente.

## Servicios opcionales en línea

- [Mapzen Terrain Tiles / AWS](https://registry.opendata.aws/terrain-tiles/): mosaicos Terrarium para sombreado topográfico actual, con atribución visible. El registro enlaza a las fuentes de elevación y sus condiciones; no se redistribuyen los tiles en Git. Mantener atribución y revisar condiciones/capacidad antes de tráfico importante.
- Letras del mapa: Noto Sans Regular PBF de [MapLibre demo tiles](https://github.com/maplibre/demotiles), generadas con OpenMapTiles/fonts, **SIL OFL 1.1**. Desde 0.3 se redistribuyen localmente las 11 franjas BMP usadas por las etiquetas incorporadas, sin modificar los archivos PBF. Commit/huellas en `public/fonts/manifest.json`, licencia íntegra junto a los archivos. `node scripts/fetch-glyphs.mjs` reconstruye esta selección. No se llama al servidor demo durante la visita; ampliar la selección y verificar escrituras al añadir nombres nuevos. No garantiza todas las escrituras ni resuelve la composición compleja de texto antiguo.
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

Priorizar organismos científicos, repositorios académicos y conjuntos con licencia inequívoca, resolución y cronología documentadas. Fuentes candidatas **no incorporadas ni auditadas aún**: cartografía vectorial detallada derivada de OSM para costa actual, catálogos arqueológicos/fósiles, modelos de hielo y nivel del mar, Paleobiology Database y modelos paleogeográficos publicados. CShapes, Cliopatria y WDI ya se incorporan con el alcance indicado arriba.

No reutilizar sin licencia mapas de atlas comerciales o imágenes/vídeos de terceros. No equiparar varias representaciones coincidentes con certeza; registrar dependencias entre fuentes y su procedencia original.
