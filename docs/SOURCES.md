# Fuentes y política cartográfica

Ampliación0.11 a1920: [contexto y organismos](RESEARCH-1920.md), [autoridades focales y Europa/Asia](AUTHORITIES-1920-RESEARCH.md), [Américas](AUTHORITIES-1920-AMERICAS.md), [monarquías y territorios](AUTHORITIES-1920-REGIONS.md), [símbolos](SYMBOLS-1920.md) y [auditoría nominal](REVIEW-1920-1949.json). La corrección documental de Danzig conserva el contorno CShapes y corrige su validez observada; no modifica la topología original ni acredita todas las fronteras de entreguerras. Vaticano sólo desde7/6/1929. Las fotografías mantienen sus licencias individuales. Las fuentes de compilación e investigación se identifican como tales, separadas de actas, tratados y registros contemporáneos.

Ampliación 0.10 a1950: [fuentes, decisiones y límites](RESEARCH-1950.md), [auditoría nominal](REVIEW-1950.json). Se conservan CShapes, coordenadas y licencias de origen; los suplementos modernos son contornos de referencia identificados. Autoridades, ventanas documentales, imágenes y diseños históricos tienen procedencias individuales. El catálogo [Países](../Países/README.md) referencia esos medios; no cambia sus licencias ni crea una colección cartográfica fusionada.

## Ampliación 0.6 · 1990–2026

- Autoridades, medios y banderas: [HISTORICAL-AUTHORITIES](HISTORICAL-AUTHORITIES.md). Adquisición incremental de cargos nacionales P1906/P1313 y mandatos P39/P35/P6 con fechas; curaciones primarias previas conservadas, sin extender afirmaciones abiertas por defecto. Banderas identificadas por P163 y adopción documentada cuando coincide el archivo. Las licencias de cada medio permanecen en su manifiesto.
- Organizaciones: [HISTORICAL-AFFILIATIONS](HISTORICAL-AFFILIATIONS.md), 27 organizaciones y 474 intervalos. Cierre anual, fin exclusivo; fechas recortadas o de precisión anual identificadas. No equivale a una lista exhaustiva de organizaciones ni de suspensiones. Fuentes por relación.
- Contextos: [HISTORICAL-CONTEXT](HISTORICAL-CONTEXT.md), síntesis editoriales de transiciones y conflictos por fases, con fuentes primarias. Índice de fichas asociadas, sin convertirlo en lista formal de beligerantes ni geometría militar.
- Suplementos cartográficos: `historical-supplements.geojson`, 23 contornos contemporáneos Natural Earth conservados sin cambios para omisiones de CShapes. Uso explícito como referencia 1990–2019; no observación costera de cada año. [Palau independiente desde 01/10/1994](https://history.state.gov/countries/palau); los demás inicios 01/01/1990 son un límite de cobertura. No equiparar fecha de ingreso en la ONU e independencia.
- Sáhara Occidental: [ONU, territorio no autónomo](https://www.un.org/dppa/decolonization/en/nsgt/western-sahara). Se separa de la geometría marroquí de referencia y se distinguen autoridades con ámbitos diferentes. La membresía UA asociada a ESH corresponde a la RASD, sin afirmar soberanía resuelta ni control de todo el territorio.
- Crimea: [A/RES/68/262](https://press.un.org/en/2014/ga11493.doc.htm). CShapes incorpora el área a Rusia en 2014; la base del atlas mantiene para ambos países el registro de 2013, con ocupación en capa separada. No reconstruye los frentes posteriores a 2022.
- Kuwait: [ONU/UNIKOM](https://peacekeeping.un.org/sites/default/files/past/unikom/background.html). `recent-control.geojson` conserva el contorno CShapes vigente en 1990, sin sustituirlo por la demarcación posterior. Ocupación iraquí al cierre de 1990, separada de la base; no se mantiene al cierre de 1991. Licencia geométrica NC-SA explícita.
- Somalia: [Oficina Política de la ONU, septiembre de 1999](https://press.un.org/en/1999/19990902.stephen.doc.html). Ausencia de Gobierno central efectivo explicada como situación institucional, conservando autoridades regionales/reivindicadas sin atribuirles control nacional. `curate-recent-exceptions.py` registra esa nota y la ventana contextual de 1998–1999.

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


## Ampliación 0.5 · año 2026

Autoridades actuales y retratos: ver [CURRENT-AUTHORITIES](CURRENT-AUTHORITIES.md), con contraste de Protocolo ONU y fuentes nacionales, mandatos breves, cobertura de medios y vacíos. Fotografías Commons con licencia propia y atribución individual; no se generan imágenes de dirigentes.

Agrupaciones y conflictos: ver [CURRENT-LAYERS](CURRENT-LAYERS.md) para OTAN, UE, BRICS, Tres Mares y siete contextos parciales de conflictos. Las listas sólo se aplican a 2026; no son reconstrucciones de todas las fechas del año ni se proyectan hacia otros años. La cartografía no cambia al seleccionar estos colores.

El relieve Terrarium/Mapzen de AWS puede activarse desde 10.000 a. C. como **topografía contemporánea de referencia**. No se presenta como DEM antiguo ni reconstruye costas, nivel del mar o cambios locales históricos. Se inicia apagado y queda excluido de geología/escenas sin cartografía.

La reparación de perfiles conserva intactas las seis series WDI y corrige exclusivamente la unión de nombres/metadatos: ADM0_A3 con equivalencias explícitas, sin usar ISO_A3_EH como si toda asociación territorial fuera la misma entidad.

Se incorpora una fotografía oficial de Maria Benvinda Levi con Đuro Macut, © Slobodan Miljević / Gobierno serbio, bajo CC BY-NC-ND 3.0 RS: archivo original completo, sin recortes ni transformaciones, para uso no comercial y con atribución/licencia visibles. Procedencia y condiciones en CURRENT-AUTHORITIES.


## Fichas de investigación · 0.7

Se añaden `country-indicators.json` (World Bank WDI, licencias CC BY comprobadas individualmente, proveedores y metadatos por indicador; no gasto militar SIPRI) y `country-history.json` (síntesis originales con fuentes institucionales, relaciones dirigidas y vigencia). Integridad/procedencia en el manifiesto. Ver COUNTRY-INDICATORS y COUNTRY-HISTORY para cobertura, transformaciones y límites. El formato de fichas y comparaciones se documenta en COUNTRY-WORKSPACE.


## Ampliación 0.8 · 1970–1989 y familias de color

Se conservan las fuentes cartográficas originales y se amplían identidades, medios, organizaciones, contexto y registros institucionales desde 1970. Las entidades vietnamitas y Rodesia se separan de sucesores; suplementos insulares y Sáhara llevan fechas y procedencia explícitas. `political-influence.json` añade relaciones de tutela con fuentes, intervalos y una convención de matices sin alterar geometría o soberanía. Ver HISTORICAL-AUTHORITIES, HISTORICAL-AFFILIATIONS, HISTORICAL-CONTEXT, REVIEW-METHOD y POLITICAL-COLORS. La adquisición histórica del 23/10 no amplía la referencia contemporánea del 22/10.


## Autoridades territoriales 0.8.1

Once relaciones de administración, gobiernos autónomos y cierres de independencia se documentan en DEPENDENCY-AUTHORITIES-RESEARCH. Los mandatos estatales existentes se reutilizan con su ámbito y se añaden cinco cargos focales de fuente primaria. Dos retratos nuevos conservan autor, licencia, origen y SHA en el manifiesto de medios. La relación no equivale a soberanía reconocida, control diario ni serie completa de gobernadores.


## Ampliación 0.9 · 1960 y representación del control

Las fuentes primarias de la ampliación, sus discrepancias y las propuestas revisadas figuran en RESEARCH-1960 y AUTHORITIES-1960-RESEARCH. Los nuevos registros conservan fuente, fechas y precisión. Los inventarios anteriores permanecen; no se avanza la referencia contemporánea por investigar el pasado. Los medios nuevos conservan autor, licencia, URL y SHA individual.

Control integrado: composición temporal con polygon-clipping0.15.7 (MIT, https://github.com/mfogel/polygon-clipping), en worker; las entradas originales permanecen separadas por licencia. La Guerra Civil española usa una colección de sus particiones independientes para no recortar CShapes NC-SA con un derivado BY-SA3 incompatible. El mapa no ofrece un nuevo archivo global sin restricciones de licencia. Los contornos de retirada sin fases acreditadas no se convierten en frentes.

Natural Earth de referencia bajo todo el dominio histórico separa tierra de océano donde el inventario político está incompleto. No representa una paleocosta ni ausencia de población/organización política. Las familias cromáticas son convenciones editoriales; el CSV propio POLITICAL-PALETTE no se atribuye al adjunto original no disponible del propietario.

REVIEW-1960 conserva auditoría y huecos con nombres y años; DELIVERY-0.9.0 diferencia implementación, contraste focal, validación y publicación. No interpretar una autoridad resuelta como inventario exhaustivo de todos los mandatos, administradores o frentes.

La corrección0.9.1 conserva las referencias de imágenes al regenerar mandatos y distingue el token ND del nombre GODL-India. Los cinco medios incorporados retienen los créditos y declaraciones de licencia de cada archivo; los candidatos pendientes no se consideran autorizados. La separación constitucional de cargos en Nigeria se documenta en AUTHORITIES-1960-RESEARCH, incluida una errata de la fuente institucional.


## Corrección1940–1944 y retratos suizos ·0.12.1

Nuevo derivado [particiones compartidas](WWII-PARTITIONS.md),CShapesNC-SA con atribuciónCliopatriaBY4.0 y cortes de referenciaNaturalEarthPD. No incorpora frentes españolesBY-SA3.0. Fuentes originales inalteradas y huellas de insumos registradas. Las reglas de saneamiento y las áreas protegidas no certifican frentes diarios.

[Retratos suizos y permisos](PORTRAITS-0.12.1-RESEARCH.md):34 originales individualmente identificados,33GIF/1PNG;HauserPD y33 permisosCFU/VRT exactos. Etiquetas institucionales verificadas conFederalCouncil; no se infieren fechas del retrato ni se da por completa la serie colegiada.


## Ampliación1880 y correcciones0.13

Fuentes, licencias, resolución de identidades, referencias geográficas y límites en[RESEARCH-1880](RESEARCH-1880.md), documentos regionales y[revisión de imágenes](MEDIA-CORRECTIONS-0.13.md). Los originales cartográficos y las particiones1940–1944 permanecen intactos. Groenlandia usa referenciaNaturalEarth; Hawái anterior a1898 referenciaCliopatria y desde1898 geometría exactaCShapes. No mezclar ambas costas ni sus condiciones de reutilización en una geometría nueva sin declaración. Fichas de los medios conservan autor, licencia, fuente ySHA. Auditoría nominal enREVIEW-1880-1899.json.


## Ampliación1840–1859 · 0.15

Cargos históricos explícitos, metadatosWikidataCC0 y curaciones institucionales complementan la geometríaCliopatria sin modificar sus coordenadas. Símbolos e imágenes conservan licencia propia, autoría y huellas en el manifiesto. [Investigación, enlaces primarios y limitaciones](RESEARCH-1840.md). No se afirma cobertura mundial exhaustiva ni reconstrucción diaria de frentes.

## Ampliación1820–1839 · 0.16

Consultas históricas aisladas, símbolos ya acreditados, nuevos retratos con licencia propia y14 fases documentales institucionales. No se adquieren datos durante la compilación. Fuentes y límites en [DELIVERY-0.16.0.md](DELIVERY-0.16.0.md); candidatos y declaraciones en scripts/historical-offices-016-research.json.

## Ampliación1800–1819 · 0.17

Adquisición aislada, cargos explícitos y52 medios nuevos con licencia propia. Doce fases documentales; originales geográficos intactos. Fuentes, correcciones y límites en [DELIVERY-0.17.0.md](DELIVERY-0.17.0.md). Los estados clientes no se convierten en colonias por compartir familia de color.

## Revisión0.18 ·1800–1900 y formas de gobierno

Autoridades y símbolos revisados con fuentes por intervalo. Taxonomía institucional CC0 y serie separada V-Dem2026v16/OWID,1789–2025,CCBY-SA4.0, DOI10.23696/vdemds26. La serie no se extrapola a2026 ni se atribuye a colonias a través de sus administradores.68 referencias urbanas y32 puntos de conflictos; estos puntos no son frentes. [Fuentes, transformaciones y límites](REVIEW-0.18.md); [licencia de la serie](../public/data/LICENSE-REGIMES-CC-BY-SA-4.0.txt).

## Ampliación1700–1799 ·0.19

853 intervalos Cliopatria adicionales con los mismos identificadores y coordenadas de origen, sin sustituir los archivos anteriores.275 intervalos de cargos revisados,39 ventanas de símbolos con tipo explícito y referencias seleccionables de sedes germanas agrupadas. Las enseñas institucionales Qing, el mon Tokugawa y los sellos Joseon no se presentan como banderas nacionales modernas. Los diseños posteriores y ficticios se rechazan. [Investigación y licencias individuales](RESEARCH-1700.md), [auditoría anual y huecos nominales](REVIEW-1700-1799.json). La evaluación política V-Dem conserva su cobertura1789–2025.
