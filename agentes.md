# Historicmap · Manual de continuidad del proyecto

Documento canónico para colaboradores humanos y asistentes de cualquier proveedor. Su propósito es permitir continuar el trabajo sin depender de una conversación previa. Fecha inicial: **21 de octubre de 2026**. Última actualización: **22 de octubre de 2026**. Versión del producto: **0.5.0**.

## 1. Identidad y visión

Propietario y autor del proyecto: Alejandro Pico. Repositorio: https://github.com/AlejandroPico/Historicmap. Nombre del producto: Historicmap. Idioma inicial: español. Frase de identidad: «El tiempo tiene un lugar».

Construir un atlas temporal riguroso de la Tierra, desde su formación hace unos 4.540 millones de años hasta el presente, con énfasis creciente en la aparición, expansión y organización de las sociedades humanas. El producto debe permitir explorar el planeta en dos dimensiones y como globo tridimensional, manteniendo una experiencia visual cuidada, moderna y profesional.

El horizonte completo incluye evolución continental, océanos, glaciaciones, relieve, atmósfera, nacimiento y evolución de la vida, homininos y migraciones, primeros asentamientos, ciudades, reinos, imperios, fronteras, guerras y batallas. Son líneas de desarrollo, no una afirmación de que todo pueda reconstruirse con certeza.

## 2. Requisitos explícitos del propietario

1. El proyecto comienza desde un repositorio vacío y debe producir versiones utilizables.
2. La calidad cartográfica contemporánea debe aspirar al máximo detalle disponible. No dibujar costas manualmente ni sustituir datos por siluetas decorativas. El pasado admite reconstrucciones aproximadas, identificadas como tales.
3. Mapa 2D y globo 3D. En etapas futuras, estudiar relieve tridimensional real y un sistema de iluminación y materiales más avanzado; el globo inicial no equivale a una simulación geológica o atmosférica.
4. La regla inferior debe ser más ancha que la pantalla. **Se desplaza la regla; el cursor temporal queda fijo en el centro inferior.** Debe poder arrastrarse en ambas direcciones. Desde el rediseño del 22/10/2026, la rueda sobre la regla cambia exclusivamente su escala sin cambiar la fecha; la rueda sobre el mapa hace zoom geográfico. La fecha y reproducción/saltos forman un solo grupo central. No restaurar las franjas superior e inferior, «Viaja en el tiempo», «Volver al presente», el texto de extensión temporal o el enlace de metodología al pie.
5. Cubrir todas las edades humanas y etapas geológicas, no solamente época contemporánea.
6. Incorporar progresivamente las distintas especies de homininos, incluidos neandertales y Homo floresiensis; diferenciar evidencia fósil, distribución inferida y migración.
7. Menú flotante compacto en la esquina superior derecha, sin cabecera permanente: búsqueda, botón único que alterna 2D/3D, capas, base de datos/fuentes, pantalla completa e información. Eliminar los botones laterales de zoom y restablecimiento. Identidad, favicon, enlaces al proyecto/portfolio, versión e historial se integran en «Acerca de». Referencias visuales autorizadas: Sizes y Lector; conservar la paleta del atlas.
8. Tecnologías actuales: verificar las versiones estables disponibles al adoptarlas; fijarlas y registrar decisiones. No usar versiones experimentales por el simple hecho de ser más nuevas.
9. SQLite es admisible si ayuda; no es obligatorio ni debe añadirse sin necesidad.
10. Este archivo debe registrar visión, planes, tecnologías, funciones, decisiones y continuidad entre asistentes. La documentación debe ser profesional, sin comparaciones con productos de entretenimiento ni referencias promocionales a modelos.

## 3. Base de la versión 0.4.0 y actualización 0.5.0

### Implementado

- Aplicación estática TypeScript/Vite/MapLibre, mapa Mercator y globo, worker local explícito, selección/búsqueda local. Sin backend, cuentas, claves privadas, analítica ni SQLite. La actualización 0.5 sustituye el contexto izquierdo por la ficha de país con pestañas y añade la séptima herramienta de apariencia. Se conservan la regla desplazable, cursor fijo y zoom temporal independiente.
- Año máximo del dispositivo, con referencia contemporánea incorporada en 2026; no se inventan datos al cambiar el reloj. Cronología y saltos/reproducción anuales desde **1789**. La reproducción comparte descargas, espera el mapa y conserva la geometría anterior durante la carga; pausa y contador impiden avances/respuestas obsoletos.
- **1789–1885:** 1.715 registros componentes Cliopatria, intervalos inclusivos y coordenadas intactas, sin uniones agregadas duplicadas. Síntesis anuales sin día uniforme. Áreas sin entidad en el inventario en gris sobre costa contemporánea de referencia; no equivalen a territorios vacíos de población o sin organización política. Nombre original, Wikidata y MemberOf conservados.
- **1886–2019:** los **710 registros** CShapes 2.0 GW con dependencias del paquete R, conservando geometrías, administrador, capital, estatus y fechas; selección **31 de diciembre**. No sustituir por el GeoJSON directo que omite estatus/administración.
- **2020–año del dispositivo:** Natural Earth 1:10m, 258 entidades, referencia incorporada en 2026; no serie independiente de cada año ni mapa diario del control militar. Continúan los 26 snapshots originales para trazabilidad y los dominios anteriores/geológicos. Antes de 1789 la selección histórica sigue siendo aproximada.
- **Control territorial:** 57 registros Cliopatria de potencias centrales 1914–1918, Alemania/Japón/Italia/URSS durante WWII, Croacia, Vichy y control comunista chino. Capas separadas de la base; activadas comparten color opaco por potencia, desactivadas recuperan los territorios. Países aliados no se convierten automáticamente en títeres; Croacia y Vichy se diferencian con tonos claros. Hungría anterior a 1944 no se representa como ocupación alemana de 1944.
- **Guerra Civil española:** siete registros (dos bandos en 1936, 1937 y 1938; resultado franquista de 1939), península y Baleares. Frentes Cliopatria de 1936/1938 y frente vectorial de **octubre de 1937** de Tyk / Té y kriptonita georreferenciado con 15 puntos, residuo medio 4.954 m, máximo 7.385 m e incertidumbre mínima declarada **10 km**. Exterior Natural Earth PD, particiones complementarias sin solapamientos/huecos. No son frentes diarios/de fin de año. Véase SPANISH-CIVIL-WAR.
- **Colores por régimen:** Alemania nazi gris oscuro, URSS roja, EEUU azul, familias chinas amarillas/ocres y Japón distinguible; Francia monárquica, republicana, napoleónica y restaurada diferenciadas; bandos españoles distintos y cambio al vencedor. Colonias de CShapes comparten color del administrador. Es una convención editorial, no un hecho que se deduzca de la bandera. Otros regímenes aún necesitan curación específica; la arquitectura admite ampliarlos.
- **Fichas integradas:** bandera/símbolo histórico junto al nombre, dirigente y retrato antes de hechos/contexto; mismas fichas en clic y búsqueda, incluidos bandos/ocupaciones. Catálogo de **267 claves y 2.859 registros de autoridades**, no 267 series completas ni igual número de personas. Se distinguen jefe de Estado/Gobierno, partido y autoridades rivales. Se consolidan duplicados de la misma persona y se prioriza la autoridad principal según el sistema político focal.
- Banderas auténticas, incluida Alemania 1935–1945; variantes RFA/RDA por fecha, sin bandera nacional inventada en la ocupación anterior a 1949. Francia de 1789 usa **estandarte real** identificado. Presidencias de EEUU con mandatos reales y periodos no consecutivos; sucesión española, incluido Fernando de Santiago en funciones en julio de 1976. Azaña/Negrín o Largo Caballero en la zona republicana, Franco en el otro bando. Autoridades colectivas francesas sin retrato individual inventado.
- Símbolos al cierre anual y, desde 0.5, autoridades de todos los mandatos del año, limitadas a adquisición/día del dispositivo en presente; un futuro reloj no extrapola dirigentes/símbolos. Declaraciones sin fecha no se proyectan al pasado; colonias sin identidad documentada no heredan dirigentes de la independencia. Imagen ausente se omite conservando el nombre; autoridad no documentada se indica. Metadatos Wikidata CC0 e imágenes con **licencia propia**, locales, sin consultas al proveedor durante la visita. Detalles y fuentes en IDENTITIES.
- Crimea, Sinaí y Golán mantienen sus cinco registros contextuales y notas; la base egipcia/israelí/siria desde 1967 conserva geometría de 1966 para separar ocupación/incorporación. No resuelve por sí sola todo el Levante. Crimea se contextualiza conforme a A/RES/68/262, no como anexión reconocida.
- Fichas con capital, estatus, administrador, contexto y seis indicadores WDI desde 1960: población, PIB, PIB/habitante, superficie, esperanza de vida, porcentaje urbano. Último dato no futuro con retraso máximo cinco años y año visible; sin extrapolar ni asignar URSS/Yugoslavia/RDA a sus sucesores. Temas de PIB/PIB-habitante/población aplicados sólo a pintura con feature-state; no se reteselan costas por indicador. Índice de códigos NE/WDI evita fusionar entidades con `-99`.
- 323 capitales/grandes ciudades actuales desde 2020 y capitales de cada registro CShapes en 1886–2019. Los tres puntos introductorios permanecen sólo en dominios históricos anteriores. Antes de 1886 no se inventan capitales ausentes. Relieve AWS Terrarium apagado al abrir; referencia contemporánea disponible desde 10.000 a. C., sin afirmar reconstrucción de altitudes/costas antiguas. Se desactiva en geología y escenas sin cartografía.
- Datos y medios con versiones, atribución, transformaciones y SHA-256: **35 recursos geográficos/estadísticos/de identidad**, 11 franjas Noto Sans PBF OFL y manifiesto separado de medios. Los SVG/fotografías originales se tratan como binarios en Git para mantener sus huellas; JSON preparado usa LF explícito. CShapes/derivados NC-SA separados de Cliopatria BY y frente 1937 BY-SA; no mezclar licencias en un derivado.
- Auditoría automática **1789–año del dispositivo**, cambios y excepciones en ANNUAL-REVIEW. No se presenta como cotejo manual exhaustivo. Pruebas geográficas de localidades, bandos, imperios, identidades y periodos, además de navegador. Quality/Pages conservan el flujo y permisos. Estado de entrega final en DELIVERY-0.4.0.
- About con identidad/favicon/versión/historial y enlaces confirmados al repositorio y https://alejandropico.github.io/Portfolio/ . Sin publicidad de proveedores ni comparaciones de entretenimiento.

### Límites y trabajo restante

- **No afirmar exactitud política mundial exhaustiva 1789–actualidad ni fichas completas de todos los países/épocas.** Los registros de fuente y los contrastes focales se distinguen de una validación historiográfica integral. El inventario de autoridades tiene vacíos, fechas de precisión desigual y registros globales aún sin contraste primario.
- CShapes omite cambios pequeños, muchos frentes temporales y Estados; Cliopatria es una reconstrucción con periodización y resolución desiguales. Las extensiones anuales pueden representar momentos distintos dentro del año. La costa contemporánea de máxima resolución sigue pendiente; no degradar coordenadas para ocultar fallos.
- Guerra Civil: faltan frentes mensuales/diarios, cierre exacto de diciembre de 1936/1938, ofensiva de Cataluña, fases de Teruel, enclaves pequeños, Canarias y control colonial completo. El frente de octubre de 1937 conserva incertidumbre ≥10 km además de la de la fuente.
- Faltan delimitación completa de administraciones de ocupación, cuatro zonas aliadas individuales y sectores de Berlín; la base occidental sigue agrupada. Faltan partición germano-soviética detallada de Polonia, muchos frentes de ambas guerras mundiales y guerra civil rusa. Las fichas no acreditan geometría ausente.
- Sin serie verificada de control efectivo mundial desde 2020, frentes Donbás/Ucrania desde 2022, fases geométricas del Sinaí y Taba 1982–1989, ni resolución exhaustiva de armisticios/estatus del Levante y cambios recientes del Golán. No inferirlos de los polígonos existentes.
- Completar banderas, autoridades coloniales, predecesores y regímenes por regiones con bibliografía; no toda persona tiene retrato ni todo país una serie continua. Los retratos identifican a la persona y no son fotografías correspondientes a cada año.
- CAO2024 no reconstruye clima, atmósfera, hielo, biomas, relieve ni paleocosta exacta. Antes de 1.800 Ma y en intervalos prehistóricos sin geometría se mantienen escenas/contexto declarados. Homininos, migraciones, glaciaciones, Theia/impactos, vida y simulaciones físicas siguen pendientes.
- Guerras y batallas como **eventos puntuales con categoría propia**, actores, fechas y precisión, siguen en roadmap para siguiente entrega; los frentes/control no sustituyen batallas documentadas. Relieve y tipografías de UI requieren conexión; medios y datos locales no implican PWA/offline completo.

## 4. Tecnologías y estructura

Versiones adoptadas el 21/10/2026, contrastadas con registros oficiales: Node.js **26.12.1**, TypeScript **7.0.2**, Vite **8.3.5**, MapLibre GL JS **6.15.0**, Lucide **1.61.0**, Vitest **5.0.5**, Playwright **1.64.1**. `package-lock.json` es la referencia exacta, incluidas dependencias transitivas. El equipo inicial tenía Node 24; se utilizó un ejecutable portátil oficial Node 26 en `.tools/`, ignorado por Git. No subirlo ni modificar instalaciones del usuario.

```text
src/main.ts                interfaz, mapa, interacción y estado de aplicación
src/about.ts               identidad, ficha del proyecto e historial visible
src/time.ts                cronología, año del dispositivo y selección por dominio
src/history.ts             periodos, identidades, dependencias, geometrías y capitales
src/data.ts                caché compartida, carga temporal y capas
src/profiles.ts            observaciones fechadas, temas, formato y leyenda
src/political.ts           familias y colores políticos/de control
src/identities.ts          símbolos, dirigentes y selección temporal
src/country-card.ts        ficha integrada común a búsqueda y mapa
src/appearance.ts          apariencia y reloj local
src/current-affiliations.ts membresías 2026 y contextos parciales de conflictos
src/recent-context.ts      contexto focal 1900–actualidad y fuentes
src/catalog.ts             contexto de épocas y lugares introductorios
src/style.css              sistema visual, disposiciones y adaptación
public/data/*.geojson      instantáneas con geometrías de origen
public/data/manifest.json  URLs, versiones, licencia, entidades y SHA-256
public/data/LICENSE-*.txt  licencias completas de datos redistribuidos
scripts/fetch-data.mjs     actualización explícita de fuentes
scripts/verify-data.mjs    comprobación de integridad y procedencia
tests/time.test.ts         invariantes y dominios temporales
tests/browser/atlas.spec.ts recorridos del producto y adaptación
.github/workflows/ci.yml   validación de cada push y pull request
.github/workflows/pages.yml publicación tras validación en main
docs/SOURCES.md            fuentes, atribución, límites y candidatos futuros
docs/ARCHITECTURE.md       decisiones, modelos propuestos y evolución
CHANGELOG.md               historial del producto
AGENTS.md                  entrada automática hacia este documento
```

La interfaz utiliza una base oscura azul verdosa, acento dorado, tipografía sans para controles y serif para fechas/contexto. El mapa ocupa toda la pantalla. La ficha del país se superpone a la izquierda, siete herramientas flotan arriba a la derecha y la regla se superpone al pie sin franjas adicionales. El punto fijo central integra fecha, reproducción y saltos. Se retiran Explorar épocas y la etiqueta «Escala adaptativa» por instrucción del propietario. La leyenda ocupa la derecha sobre la regla; escala geográfica y atribución compacta se sitúan abajo a la izquierda. No degradar la cartografía por comodidad estética. Mantener contraste, foco y accesibilidad.

MapLibre 6 utiliza módulos ESM y worker externo. El worker se importa explícitamente con `?url` y se configura con `setWorkerUrl` **antes de crear el mapa**. No eliminarlo: el fallo puede dibujar un globo vacío aunque el archivo GeoJSON se haya descargado. Las pruebas esperan evidencia de geometrías renderizadas, no sólo el mensaje de descarga.

El renderizador usa tolerancia de teselación de 0,2 píxeles y zoom de fuente máximo 7. Es una generalización subpíxel para la pantalla, no una modificación de los archivos de origen. La tolerancia cero en geometrías globales muy densas provocaba segmentos por encima del límite de vértices del motor. Las pruebas de navegador detectan ese aviso para evitar regresiones. Mantener el detalle de origen y evaluar teselas de alta resolución en la próxima etapa.

La regla reutiliza sus marcas durante el movimiento y las reconstruye al cambiar la escala, el tamaño o el bloque visible. Sólo genera marcas del área visible y un margen, evitando miles de nodos al ampliar mucho. La fecha permanece anclada al centro al hacer zoom, independientemente de la posición del ratón. La URL compartible se actualiza como máximo cuatro veces por segundo, con escritura final diferida de la fecha más reciente. No volver a escribir el historial en cada fotograma: durante una reproducción prolongada se observó que el navegador dejaba el enlace desfasado respecto al año visible. La prueba de reproducción comprueba pausa y regreso al presente con URL coherente.

## 5. Contrato de datos y rigor

Toda nueva capa debe registrar al menos: identificador, tipo de fenómeno, fuente primaria o compilación identificada, licencia, versión/DOI, fecha de consulta, ámbito espacial y temporal, escala/resolución, incertidumbre, método de transformación y estado de revisión. No deducir soberanía por ausencia de datos. No colorear áreas sin documentación como si fueran fronteras determinadas.

Separar cuatro conceptos: fecha consultada, intervalo de validez, fecha de la observación/reconstrucción y fecha de publicación del conjunto. Las fronteras disputadas y las alternativas historiográficas deben poder coexistir, con fuente y explicación. El índice ordinal de precisión de un proveedor no es una probabilidad científica.

En datos futuros, usar intervalos con extremos definidos y fechas inciertas; distinguir «atestiguado», «inferido», «reconstruido», «hipotético» y «desconocido». Para geología usar Ma antes del presente como eje propio; para historia, una representación civil sin año cero y conversiones explícitas. No interpolar polígonos entre reinos o modelos tectónicos con identidades incompatibles.

No importar imágenes, vídeo, datasets o texturas porque sean accesibles: verificar licencia y atribución. Un vídeo aportado por el propietario puede orientar la investigación; no autoriza automáticamente reutilizar sus gráficos. No raspar atlas comerciales como fuente de geometrías.

## 6. Roadmap priorizado

### 0.2 · Interfaz compacta — implementada

- Cabecera y franjas de la cronología eliminadas; menú superior compacto, capas desplegables, identidad en «Acerca de» y controles integrados en el centro fijo.
- Zoom independiente: rueda sobre mapa para geografía, rueda sobre regla para escala temporal. Arrastre para desplazamiento temporal.
- Esta entrega no amplía ni modifica la cartografía o sus fuentes. Las prioridades científicas y de resolución siguen pendientes.

### 0.3 · Datos recientes y reproducción — implementada con límites

Entrega priorizada por solicitud del propietario: intervalos territoriales 1900–2019, revisión anual de cobertura hasta el año del dispositivo, capas de guerra/ocupaciones, fichas, ciudades e indicadores. Los límites de la sección 3 siguen abiertos. La fase anterior de máxima resolución se desplaza, sin considerarla realizada.

### Próxima fase · Calidad cartográfica contemporánea

- Evaluar teselas vectoriales abiertas de alta resolución, costa detallada y actualización reproducible, por ejemplo con un paquete PMTiles propio o proveedor documentado.
- Resolver nombres, etiquetas, detalles costeros, lagos, ríos, países pequeños, antimeridiano y polos, con generalización dependiente del zoom y pruebas geográficas.
- Modelar fronteras disputadas y fecha de vigencia, sin una falsa etiqueta universal de «exactitud».
- Mejorar materiales de superficie y relieve, iluminación, batimetría y transiciones, manteniendo legibilidad política y rendimiento.
- Módulos separados para motor cartográfico, aplicación de capas, UI, cronología y repositorios de datos; el archivo inicial `main.ts` es deliberadamente compacto y debe separarse antes de ampliarlo mucho.

### 0.4 · Historia política verificable — primera ampliación implementada, contrastes regionales pendientes

- Extender los contrastes focales 0.3 a una revisión historiográfica por regiones y conflictos; completar 2020–actualidad y corregir las excepciones del informe anual. Incorporar fuentes de mayor detalle donde CShapes omite cambios.
- Modelo de entidades persistentes con nombres e identidades históricas, relaciones de dependencia y periodos de validez.
- Cambios fechados de fronteras, ciudades, capitales, redes comerciales y primeros Estados. Trabajar por entregas geográficas revisadas, no prometer todos los años de todo el planeta de una vez.
- Fichas de entidad con bibliografía, precisión y alternativas, comparación entre fechas y búsqueda en español.

### 0.5 · Actualidad, fichas y apariencia — implementada con límites

Identidades y uniones de metadatos corregidas, fichas por pestañas, ampliación de autoridades/retratos actuales, apariencia por hora y agrupaciones de 2026. Estado, fuentes, cobertura y validación en sección 13 y CURRENT-AUTHORITIES/CURRENT-LAYERS. La siguiente prioridad continúa siendo completar los vacíos del año vigente antes de retroceder.

### Fase posterior · Prehistoria y evolución humana

- Catálogo de yacimientos y fósiles con evidencia primaria; especies, rangos temporales inciertos y ocupación documentada.
- Homo sapiens, neandertales, denisovanos, Homo erectus, Homo floresiensis y otros taxones cuando los datos lo permitan. No homogeneizar «homininos» con «humanos modernos».
- Migraciones como hipótesis con rutas/áreas de incertidumbre y fechas, nunca como trayectorias GPS exactas.
- Paleocostas, cambios del nivel del mar y extensión de hielo para el Cuaternario.

### Fase posterior · Tierra profunda, clima y vida

- Ampliar y densificar reconstrucciones tectónicas dentro del alcance de modelos elegidos; ofrecer comparación y trazabilidad del modelo.
- Incorporar superficies paleogeográficas revisadas, paleoaltitud/batimetría cuando existan, hielo, biomas y evidencia fósil.
- Atmósfera y estado superficial como capas específicas con unidades, intervalos e incertidumbre; evitar codificar composiciones o colores ficticios.
- Historia de formación planetaria e hipótesis lunar mediante escenas explicativas claramente marcadas y bibliografía, diferenciadas de simulaciones físicas.

### Etapas posteriores

- Guerras y batallas como eventos con fuentes, alcance temporal, actores y precisión geográfica; nunca inferidas automáticamente de cambios de color.
- Relatos guiados, comparación sincronizada, exportación con citas, soporte multilingüe y preferencias locales.
- PWA y paquetes offline, búsqueda indexada y eventual SQLite para producción/compilación de catálogos; estudiar SQLite WASM/FTS sólo al justificar volumen y consultas.
- Métricas y presupuestos de rendimiento, optimización de teselas, acceso móvil, teclado, lectores de pantalla y soporte de distintos dispositivos gráficos.

## 7. Cómo trabajar y entregar

1. Leer este archivo y comprobar la rama, cambios locales, `package.json`, fuentes y versión. No tocar proyectos hermanos del directorio del propietario.
2. Para trabajo nuevo usar ramas `codex/...` salvo instrucción distinta. La primera entrega de un repositorio vacío puede inaugurar `main`; no requiere fabricar una pull request contra una rama inexistente.
3. Hacer cambios concretos, reversibles y limitados. No reemplazar datos científicos por geometría generada sin etiqueta.
4. Ejecutar las comprobaciones que correspondan, revisar visualmente mapa actual, histórico, geológico y móvil si cambia el renderizado, y registrar resultados reales. Una compilación correcta no demuestra que el worker o los polígonos se dibujen.
5. Actualizar versión con SemVer cuando corresponda, `CHANGELOG.md`, este archivo y documentación de datos/arquitectura si cambian.
6. Registrar: realizado, validado, problemas conocidos, siguiente paso, fuentes nuevas y decisiones. Identificar resultados locales, subidos y publicados por separado. No anunciar publicación basándose sólo en un workflow escrito.
7. No guardar tokens, credenciales, ejecutables locales, node_modules, informes temporales o datos privados en Git. No modificar permisos o audiencias sin autorización.
8. En `Acerca de`, usar enlaces confirmados. El portfolio del autor ya está confirmado en la sección 3; no sustituirlo por el perfil de GitHub. No introducir contenido sobre el proveedor de IA en la experiencia del usuario.

## 8. Ejecución y despliegue

Requisitos: Node de `.nvmrc` o posterior compatible y navegador moderno con WebGL. Comandos: `npm ci`, `npm run dev`, `npm run data:verify`, `npm test`, `npm run build`, `npx playwright install chromium`, `npm run test:e2e`.

La compilación no necesita credenciales ni acceso a las fuentes científicas: GeoJSON, TopoJSON y series se guardan en Git. `data:fetch` sí consulta fuentes, fija sus commits actuales cuando son repositorios, solicita explícitamente CAO2024 y actualiza el manifiesto. El servicio puede cambiar resultados del mismo nombre de modelo: las huellas del snapshot importado permiten detectar cambios.

`Quality` valida pushes y PR. `Publish atlas` sólo responde a `Quality` correcto en `main` tras un push, o a una ejecución manual autorizada. Hace checkout del commit validado, compila y publica en GitHub Pages. Requiere Source=GitHub Actions ya seleccionado en ajustes. La autorización del usuario para iniciar el proyecto no debe confundirse con permitir cambiar visibilidad, dominio, facturación o accesos.

## 9. Registro de decisiones iniciales

- **2026-10-21:** adoptar aplicación estática TypeScript + MapLibre para tener un único motor 2D/3D y distribución simple; posponer backend, cuentas y SQLite hasta necesitar consultas persistentes.
- **2026-10-21:** incorporar datos locales con procedencia y licencias para que el atlas no dependa del tiempo de respuesta de servicios científicos en cada navegación.
- **2026-10-21:** utilizar 26 instantáneas explícitas, no morphing ficticio ni mapas contemporáneos retrotraídos como si fueran históricos.
- **2026-10-21:** usar CAO2024 por su cobertura de 1.800 Ma y citar el modelo; no usar el modelo predeterminado mutable del servicio.
- **2026-10-21:** comenzar con Natural Earth 1:10m preservando geometrías; reconocer que no alcanza el objetivo final de máxima resolución.
- **2026-10-21:** escenas conceptuales sin continentes inventados en dominios sin datos; contexto separado de cartografía.
- **2026-10-21:** `agentes.md` es el documento canónico solicitado; `AGENTS.md` sirve como enlace de entrada automática.
- **2026-10-22:** por solicitud del propietario, retirar cabecera, franjas y controles laterales. Seguir la colección de iconos de Sizes y la estructura de identidad/ficha de Lector en «Acerca de». Unificar fecha y reproducción en el centro de la regla, y separar zoom geográfico/temporal por la superficie bajo el cursor.
- **2026-10-22:** mantener los datos intactos. La versión 0.2.0 corresponde a interfaz y navegación; la fase de alta resolución cartográfica pasa a 0.3.

- **2026-10-22, 0.3:** priorizar historia reciente y reproducción a petición del propietario. Adoptar CShapes GW con dependencias por intervalos y Cliopatria como capa anual contextual. No confundir síntesis de guerra con día exacto; fecha base histórica al cierre del año.
- **2026-10-22, 0.3:** separar ocupación/incorporación soberana en Sinaí, Golán y Crimea. Documentar vacíos y no dibujar fases o frentes sin fuente.
- **2026-10-22, 0.3:** sustituir el máximo hardcodeado por reloj local. Mantener fecha de referencia de la cartografía y observaciones, sin inventar datos futuros. Reproducción con espera y caché compartida, no cancelar por fotograma.
- **2026-10-22, 0.3:** ampliar fichas y ciudades, añadir seis indicadores WDI y tres temas; mantener licencia NC-SA de CShapes separada de las demás fuentes y del código.

## 10. Validación y relevo

La entrega 0.3 comprobó los 31 recursos y sus huellas, invariantes temporales y año dinámico, selección de cada año 1900–2019, ausencia de identidades duplicadas, Alemania anterior/posterior a 1945/1949, dependencia/independencia de India y Argelia, Egipto/Siria/Israel, activación de Crimea, ciudades, capitales y ausencia de estadísticas futuras. En navegador se comprueban todos los años 1900–actualidad, reproducción/pausa, peticiones lentas y fechas obsoletas, fichas, economía, móvil, cartografía antigua/geológica, GPU y controles compactos. Registrar resultados finales reales en `docs/DELIVERY-0.3.0.md`, sin dar por superado un test que sólo se ha escrito.

Para reconstruir datos: consultar `docs/SOURCES.md`, `scripts/acquire-history.py`, `scripts/fetch-modern.mjs`, `scripts/prepare-history.py` y `scripts/build-review.mjs`. Shapely 2.2.0 es herramienta de preparación, no dependencia del navegador. `.cache/` y `.tools/` son locales ignorados. `npm run data:audit` regenera el inventario hasta el año del sistema; `data:verify` no certifica exactitud histórica.

Siguiente prioridad: **completar excepciones históricas y control efectivo reciente, con mejores fuentes**, y avanzar después en costa contemporánea de alta resolución. No ampliar indiscriminadamente la cronología sin resolver errores concretos. Conservar la distinción entre ambición, cobertura de fuente, contraste focal y validación exhaustiva.

La actualización incremental de fuentes se implementa en source-diff.ts y se comprueba con pruebas de diferencias; sólo se envían entidades modificadas al worker. Las pruebas de navegador usan la compilación de producción en el puerto 5174, con un único worker para no saturar el renderizado por software; compilar antes de ejecutarlas.

## 11. Cierre verificado de 0.3.0 (histórico)

Código publicado: **6952e1baf384bc0c75a59dcf7bf6dc2cff9cc882**. [Quality 39693996198](https://github.com/AlejandroPico/Historicmap/actions/runs/39693996198) correcto: 31 recursos y 11 franjas de letras íntegros, **16 pruebas unitarias y 9 recorridos de navegador** correctos, compilación correcta. [Publish atlas 39694346487](https://github.com/AlejandroPico/Historicmap/actions/runs/39694346487) correcto. Comprobada la web pública: versión 0.3.0, mapa de 1942 con 169 territorios y capa de guerra, manifiesto remoto idéntico a las 31 huellas locales y letras locales disponibles. Detalle en `docs/DELIVERY-0.3.0.md`.

Las estadísticas modifican sólo la pintura mediante `feature-state`; no se reenvían ni teselan costas al cambiar PIB/población. Un índice explícito resuelve códigos Natural Earth/Banco Mundial, evitando fusionar territorios con código desconocido `-99`. Abrir una ficha pausa la reproducción. Los datos preparados usan LF explícito y los archivos PBF son binarios en Git; no eliminar esta protección de integridad entre plataformas.

El último commit de documentación registra el cierre con `[skip ci]`, sin alterar la aplicación validada. La auditoría anual y los contrastes focales no certifican exactitud exhaustiva: completar frentes y control efectivo reciente, detalles territoriales omitidos y resolución de costa sigue siendo la siguiente prioridad.


## 12. Decisiones y relevo de 0.4.0

Por solicitud del propietario: guerras civiles territoriales, banderas auténticas, régimen/colores de potencia y dirigentes con retratos, cronología anual hasta 1789. El trabajo utiliza fuentes separadas y no convierte mapas anuales de campaña en fronteras exactas de fin de año. Las autoridades se consultan al cierre anual, en presente hasta fecha de adquisición. La ampliación respeta el diseño compacto y los controles del mapa/regla.

Se extraen political, identities, country-card y methodology para no seguir concentrando lógica en main. La firma territorial incluye color/identidad; el ID no cambia por color. Control por potencia se aplica en capa opaca por encima de líneas y relleno base; desactivarla devuelve los territorios. Buscar incluye los bandos y áreas controladas visibles. Los aliados no reciben automáticamente color de ocupación.

Preparación: acquire-history → prepare-history → prepare-extended-history → prepare-spanish-fronts → prepare-identities → register-political-data → data:audit → data:verify. Shapely/NumPy/pyproj son preparación local, no runtime. La compilación y navegación no requieren fuentes remotas. Detalles: SOURCES, IDENTITIES, SPANISH-CIVIL-WAR, REVIEW-METHOD e informe anual.

Validación local: 35 recursos, 11 franjas de letras y 417 medios íntegros; 31 pruebas unitarias y recorrido completo de 11 pruebas de navegador, incluida selección de todos los 238 años. Compilación final y repetición focal posterior de las dos pruebas nuevas correctas. Publicación se registrará con resultados y SHA reales en docs/DELIVERY-0.4.0.md. No dar por publicadas funciones sólo porque se haya creado el código. Prioridad siguiente: contraste regional de frentes/autoridades, completar los vacíos expresos y desarrollar categoría de guerras/batallas documentadas antes de declarar cobertura mundial integral.


### Cierre verificado de 0.4.0

Publicado **681f71e040d8b7d07677f30b3189f50bfdf4f44d**. [Quality 39719656269](https://github.com/AlejandroPico/Historicmap/actions/runs/39719656269) correcto: 35 recursos, 11 franjas y 417 medios íntegros; **31 pruebas unitarias y 11 recorridos de navegador** correctos, incluidos los 238 años. [Publish atlas 39720348133](https://github.com/AlejandroPico/Historicmap/actions/runs/39720348133) correcto, checkout final confirmado en logs. La página pública sirve `assets/index-BSZARU0D.js`, coincide con el build final y conserva versión 0.4.0; manifiesto público idéntico a las 35 huellas locales. Verificación de cuatro medios históricos por HTTP y mapa/ficha pública de 1942 con bandera, retrato y control opaco. Detalles en DELIVERY-0.4.0.

Las últimas correcciones vinculan First Spanish Republic/Spanish Empire con ESP y distinguen Alemania republicana al cierre de 1918, Consulado/Imperio y Francia desde julio de 1830. Mantener semántica de cierre anual frente a reconstrucciones de campaña sin día uniforme. El cierre de documentación se guarda con `[skip ci]`, sin alterar la aplicación. Los pendientes regionales y límites expresos continúan abiertos; no convertir cobertura de fuente, automatización o un retrato en garantía historiográfica mundial.


## 13. Actualización 0.5.0 · prioridad al año vigente

Solicitud del propietario: resolver identidades mezcladas y datos contemporáneos antes de seguir retrocediendo por la historia; fotos globales, mandatos de todo el año, ficha por pestañas y una superficie cartográfica más despejada.

### Correcciones de identidad y datos

Dos causas independientes explicaban la contaminación: el resolver de identidades comparaba QID vacío con fichas históricas que también lo tenían vacío, eligiendo ESP-REPUBLIC; además, la unión de metadatos usaba ISO_A3_EH aunque identificara un país distinto del polígono. BRI sobrescribía BRA (Brasil), CLP sobrescribía FRA, KAB a KAZ e IOA/CSI/ATC a AUS. Se rechazan QID vacíos/no válidos y se conserva ADM0_A3 salvo equivalencias explícitas PSX/PSE, SDS/SSD, SAH/ESH, KOS/XKX y ALD/ALA. Dependencias/disputas tienen metadatos propios y no heredan estadísticas estatales. Se corrige la importación normal y se añade reparación incremental reproducible. Las coordenadas no cambian.

La ficha resuelve todos los mandatos que intersectan el año seleccionado, hasta la fecha de adquisición/del dispositivo en el presente. No elimina mandatos no consecutivos de una misma persona. El símbolo corresponde al cierre/fecha de consulta, no a cada uno de los gobiernos listados. Los límites superiores de cese sin día confirmado se etiquetan «hasta, como máximo»; no convertirlos en fechas exactas. Se conservan ocupaciones/autoridades colectivas sin crear personas o retratos ficticios.

La ampliación de retratos y contraste del año vigente se registra en CURRENT-AUTHORITIES. No confundir una foto disponible con validación de cada fecha. Lista ONU y Wikidata también pueden arrastrar errores: las excepciones se contrastan con fuentes nacionales y se documentan. Metadatos e imágenes siguen locales, con licencia/autoría/huella individuales. No volver a ejecutar la adquisición inicial limitada a 80 retratos como si fuera la actualización completa.

### Interfaz actual

- Ficha a la izquierda con Autoridades (predeterminada), Datos, Contexto y Conflictos. Bandera/nombre permanecen sobre las pestañas; navegación por flechas, Home/End, roles ARIA y foco. Datos WDI conservan año de observación; contexto identifica el año y autoridades documentadas. Conflictos es un inventario parcial con fuentes, no garantía de paz si está vacío.
- Se elimina Explorar épocas y su panel; el acceso a fechas permanece en el control central. Se quita «Escala adaptativa» sin quitar el zoom temporal.
- Leyenda abajo a la derecha sobre la regla. Escala métrica y atribución abajo a la izquierda; icono de atribución sin caja/relleno, plegado inicialmente y con créditos accesibles.
- Fuentes deja de usar el diálogo modal: panel pequeño junto al botón de base de datos, sin oscurecer fondo, con referencia cartográfica, adquisición de autoridades, estado, enlaces y metodología completa aparte. Cierre por botón, Escape o exterior. No restaurar la barra flotante de procedencia.
- Apariencia con botón cíclico mañana/sol, tarde/atardecer, noche/luna y automático/contraste. Preferencia local; automático usa hora local (07–13 mañana, 13–20 tarde, 20–07 noche), revisa cada minuto y al volver a la pestaña. No solicita ubicación. Océano más claro que fondo en las tres paletas, UI y controles con variables coherentes.
- Relieve desactivado de inicio. Referencia moderna admisible desde 10.000 a. C. en cartografía histórica; excluida de geología/concepto. No representa cambios del nivel del mar ni altitudes antiguas.

### Capas actuales y continuidad

Cuatro agrupaciones con membresía exclusiva de referencia 2026: OTAN 32, UE 27, BRICS 11 miembros + 10 socios y Tres Mares 13 miembros + 4 asociados + 6 países socios estratégicos. Categorías distintas, sin heredar membresía desde un Estado a dependencias. Fuentes/fechas/discrepancias en CURRENT-LAYERS. No se retroproyectan a 2025 ni a un futuro reloj. No son un mapa diario de altas/bajas del propio 2026.

Los temas estadísticos usan rampa verde y conservan WDI/fechas. Al elegir agrupación o estadísticas se oculta la pintura de control territorial para que no tape la lectura; al volver al tema político se respeta el conmutador de ocupaciones. Se añaden siete contextos de conflictos documentados, expresamente parciales. Ranking de capacidad militar, gasto y capa mundial exhaustiva de conflictos requieren fuentes, términos de reutilización y metodología; no inferir capacidad sólo de gasto ni participación bélica de una alianza.

Archivos nuevos: appearance.ts, current-affiliations.ts, reparación del índice de perfiles, enriquecimiento/auditoría de autoridades y pruebas de selección real de mapa, uniones de metadatos, mandatos anuales, apariencia y agrupaciones. Los detalles finales de cobertura/validación/publicación se registrarán en DELIVERY-0.5.0 con resultados y SHA reales.

Cobertura final de 0.5: **2.858 registros**; en 2026, **508 registros/413 personas u órganos/402 con retrato**, en 231 claves. **830 medios** (342 símbolos y 488 retratos); once autoridades sin imagen acreditada se enumeran en CURRENT-AUTHORITIES. Se verifican SHA de los 830 medios y decodificación de 488 fotografías. Nauru pierde dos titulares antiguos incorrectamente abiertos y Corea del Sur conserva el relevo Kim/Han dentro de 2026.
