# Historicmap · Manual de continuidad del proyecto

Documento canónico para colaboradores humanos y asistentes de cualquier proveedor. Su propósito es permitir continuar el trabajo sin depender de una conversación previa. Fecha inicial: **21 de octubre de 2026**. Última actualización: **25 de octubre de 2026**. Versión del producto: **0.12.1**.

**Continuidad operativa obligatoria:** leer y actualizar también [tareas.md](tareas.md). Contiene el encargo vigente, comprobaciones, tareas completadas, huecos concretos y siguiente paso. Una interrupción de sesión no convierte tareas pendientes en terminadas. Estado vigente de0.12.1 en la sección24; las decisiones más recientes prevalecen sobre las descripciones históricas anteriores.

## 1. Identidad y visión

**Encargo vigente0.12.1 (25/10/2026):** corregir manchas y particiones1940–1944, formato de autoridades y retratos suizos antes de ampliar a1880. El propietario confirma publicación0.12.0; comprobar localmente y subir sin esperar ni consultar Actions/Pages. Distinguir subida de publicación comprobada. Detalle en sección24 y tareas.md.

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

## 3. Base histórica 0.4.0–0.5.0; ampliación vigente en la sección 14

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
src/current-affiliations.ts observaciones parciales de conflictos de 2026
src/historical-affiliations.ts membresías fechadas de organizaciones 1990–2026
src/historical-context.ts fases históricas, conflictos y transiciones por año
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

Cobertura final de 0.5: **2.858 registros**; en 2026, **508 registros/413 personas u órganos/403 con fotografía**, en 231 claves. **831 medios** (342 símbolos y 489 fotografías (488 retratos y una escena institucional)); diez autoridades sin imagen acreditada se enumeran en CURRENT-AUTHORITIES. Se verifican SHA de los 831 medios y decodificación de 489 fotografías. Nauru pierde dos titulares antiguos incorrectamente abiertos y Corea del Sur conserva el relevo Kim/Han dentro de 2026.

La ampliación oficial final añade una foto de Mozambique bajo CC BY-NC-ND 3.0 RS, íntegra y sin recortes, con título/fotógrafo/fuente/licencia. `Media.display=full-frame` es un contrato que se preserva en CSS y pruebas. Preparación: tras `enrich-current-authorities.py`, ejecutar `fetch-official-portrait.py`. Ver CURRENT-AUTHORITIES.

### Cierre verificado de 0.5.0

Publicado **f58550940607362a7c0fa86769ca8edd6097d5ba**. [Quality 39814653054](https://github.com/AlejandroPico/Historicmap/actions/runs/39814653054) correcto: 35 recursos, 11 franjas y 831 medios íntegros; **43 pruebas unitarias y 15 recorridos de navegador** correctos. Suite local final completa también correcta (15 recorridos/14 minutos), incluidos todos los 238 años y las instantáneas distribuidas. [Publish atlas 39816246238](https://github.com/AlejandroPico/Historicmap/actions/runs/39816246238) correcto, checkout f585509 confirmado en logs. Se supera el retraso por incidencia de Actions sin saltar validaciones.

Web pública comprobada: `assets/index-BsMTmP3r.js`, `assets/index-DuODX5wW.css`; manifiestos públicos de 35 recursos y 831 medios con huellas idénticas a las locales; bytes de la nueva fotografía de Mozambique íntegros. Ficha pública de España con bandera, Sánchez, Felipe VI y pestañas, imágenes cargadas y nueva disposición verificada. Detalles y evidencia en DELIVERY-0.5.0. El cierre documental usa `[skip ci]` y conserva la aplicación validada.

Prioridad de continuidad: completar los diez retratos acreditados pendientes y contrastar las sucesiones anuales aún no certificadas; no declarar cobertura mundial exhaustiva ni extender automáticamente membresías de referencia 2026 a otro año. El detalle histórico regional y las futuras capas militares/conflictos siguen los límites documentados de CURRENT-AUTHORITIES y CURRENT-LAYERS.

## 14. Actualización 0.6.0 · retroceso hasta 1990

La nueva prioridad del propietario es ampliar mundialmente autoridades, imágenes, banderas, fronteras, contexto y conflictos de 1990–2026, y buscar más organizaciones con sus adhesiones históricas. También solicita una búsqueda menos invasiva y sugiere una tarde más cálida. Esta sección sustituye el alcance exclusivamente 2026 de las capas de 0.5, sin convertir los límites previos en trabajo completado.

### Identidades, mandatos y medios

`enrich-historical-authorities.py` amplía la adquisición desde cargos nacionales P1906/P1313 y mandatos P39, junto a P35/P6 fechados. Conserva curaciones anteriores, precisión, créditos/licencias y la foto íntegra de Mozambique. No mantiene abierto por defecto un cargo antiguo sin prueba de incumbencia. Los límites superiores inferidos se indican y no se publican como ceses exactos. Las banderas históricas nuevas usan identidad P163, fecha documentada y coincidencia del archivo; los rangos incompatibles se rechazan. Se añaden cambios focales de bandera y excepciones institucionales con fuente.

Claves históricas separadas: YUG (R. F. Socialista), FRY (R. F. Yugoslavia 1992–2002), SCG (Serbia y Montenegro 2003–2006), CSK, YAR, YPR y RASD, además de USSR/DDR existentes. En la cartografía, `entityCode` es distinto de `code` estadístico: SUN, CSK y SCG no heredan PIB ni autoridades de un sucesor. Los alias explícitos BIH, KOS y SSD/SDS resuelven nombres/códigos de fuentes sin comparar identificadores vacíos.

El resolver prefiere curación antes que precisión, y después precisión antes que título. No descartar una fecha diaria bien documentada por una afirmación anterior sólo anual. Se conservan renovaciones con la misma fecha de relevo en ambos extremos; las jefaturas de Estado y Gobierno con persona e intervalo idénticos se indican conjuntamente sin repetir la misma foto. Una foto identifica a la persona, no su apariencia exacta en cada año.

Sáhara Occidental mantiene identidad territorial SAH y estatus de territorio no autónomo de la ONU; las autoridades RASD/saharauis y marroquíes se rotulan con su ámbito. Su símbolo se identifica como RASD y no acredita soberanía o control de toda la superficie. `territoryStatus` aporta contexto institucional sin ocultar símbolos ni inventar titulares. También permite explicar la ausencia de Gobierno central efectivo en Somalia en los años noventa. La ausencia institucional documentada es distinta de un hueco de adquisición.

### Organizaciones y contexto temporal

`public/data/affiliations.json` es la única fuente de membresía usada por la interfaz: 27 organizaciones, 474 intervalos y fuentes por relación. `historical-affiliations.ts` resuelve categorías al cierre anual, con fecha máxima de adquisición en 2026. La ficha Datos lista las relaciones que intersectan el año, de modo que el Reino Unido puede figurar con fecha de salida en 2020 mientras el mapa al cierre ya no lo colorea como miembro. Fuera de 1990–2026 no se extrapola. Las dependencias no heredan relaciones de la metrópoli.

Se distinguen miembro, socio, asociado y participación suspendida; las suspensiones históricas UA/CEDEAO siguen siendo focales. Las fechas de resolución anual y los límites recortados se explican en notas. CE/UE, OUA/UA y TLCAN/T-MEC conservan su continuidad o sucesión explícita; Pacto de Varsovia y CAME terminan en 1991. La relación UA de ESH corresponde a la RASD, sin resolver el estatus territorial ante la ONU. Contextos actuales de conflictos permanecen en `current-affiliations.ts`, que ya no contiene un catálogo de membresías paralelo.

`historical-context.json` / `historical-context.ts` seleccionan fases de conflictos y transiciones por intervalos; fin exclusivo en esos eventos y en las membresías, frente al fin inclusivo del catálogo de mandatos. La pestaña Contexto incorpora hechos del año y la de Conflictos los registros asociados a la entidad. Las claves son fichas vinculadas, no un listado formal de beligerantes. Nunca pintar automáticamente una capa de países en guerra a partir de ellas. La cobertura sigue siendo parcial; falta de registro no significa paz ni estabilidad.

### Territorio e interfaz

Desde 2014, Rusia/Ucrania usan la base CShapes de 2013 para mantener Crimea en territorio ucraniano reconocido y su ocupación separada. Se añaden 23 contornos contemporáneos Natural Earth de referencia para omisiones de CShapes en 1990–2019; no se presentan como levantamientos históricos. Palau sólo aparece como independiente desde 1994. Marruecos y Sáhara se separan mediante contornos de referencia, sin inventar el muro o las líneas de control. Los registros y las fichas identifican estas transformaciones.

`recent-control.geojson` representa Kuwait bajo ocupación iraquí al cierre de 1990, con el contorno CShapes de ese año. Al cierre de 1991 ya no se muestra ocupado por Irak. La base y la ocupación se alternan con el control existente; no es una anexión reconocida ni un frente interpolado. Se mantiene la licencia NC-SA de esa geometría separada de los contornos PD de referencia.

El buscador pasa a panel no modal de 340 px junto a la lupa, sin oscurecer el mapa: nombres alternativos, teclado, Escape/exterior y cierre al cambiar fecha. No se altera el diálogo Acerca de/fecha. La tarde usa cobre/ámbar; mañana, noche y reloj automático se conservan. Océano siempre más claro que fondo. Las organizaciones se agrupan por ámbito en el selector, que permanece utilizable al recorrer 1990–2026.

### Preparación, validación y continuidad

Orden incremental: `enrich-historical-authorities.py` → `enrich-historical-flags.py` → `curate-historical-authorities.py` → `curate-recent-exceptions.py` → `prepare-recent-supplements.py` → `prepare-recent-control.py` → registros político/reciente → verificación → auditoría anual → pruebas → compilación → navegador. No ejecutar reconstrucciones iniciales destruyendo curaciones. `register-recent-data.mjs` registra las cuatro nuevas fuentes; `verify-data.mjs` comprueba formatos, referencias y huellas. Las preparaciones requieren acceso a fuentes, nunca la visita ordinaria al atlas.

La prueba de cobertura recorre cada año 1990–2019 con el resolver real de identidades de los Estados independientes CShapes: comprueba una autoridad o una ausencia institucional documentada, no precisión historiográfica completa. Otras pruebas cubren sucesores, Crimea, Kuwait, altas/bajas, huecos de fecha, renovaciones, búsqueda y fichas. Cifras finales, excepciones, resultados y SHA publicado se anotan en HISTORICAL-AUTHORITIES y DELIVERY-0.6.0. No dar por publicado un build local. Siguiente prioridad: los vacíos expresos de fotos/cargos, cobertura regional de conflictos y cartografía de control verificada; no ampliar años ocultando las limitaciones conocidas.

Cobertura final de adquisición 0.6: **274 claves/5.781 mandatos** en todas las épocas; en 1990–22/10/2026, **2.925 personas u órganos, 2.432 con imagen y 493 sin ella**. **2.871 medios**: 376 símbolos SVG y 2.495 fotografías (2.494 retratos y una escena completa). En 2026: 666 registros/437 personas u órganos/422 con imagen en 233 claves. Banderas fechadas en 197 claves de 1990 y 242 de 2026. Las cifras no equivalen a Estados soberanos ni gobiernos simultáneos. Datos y medios adquiridos el 22; cierre de entrega el 23/10/2026.

La validación de bytes de todo el catálogo se mantiene en `data:verify`; la prueba unitaria de la ficha comprueba los archivos que realmente utiliza esa ficha y la procedencia del manifiesto, evitando repetir dentro del test una lectura completa de 120 MB que puede agotar el tiempo en almacenamiento sincronizado. No eliminar por ello la comprobación global SHA del flujo Quality. Las autoridades de facto se priorizan y los alias estadísticos/políticos se normalizan para conservar el color de la misma entidad entre fuentes.


### Cierre verificado de 0.6.0

Publicado **085b2d2bcc380c4696a0a64f1518ca02f5d27a1e**. [Quality 39874774724](https://github.com/AlejandroPico/Historicmap/actions/runs/39874774724) correcto: 39 recursos, 11 franjas y 2.871 medios con SHA-256; **51 pruebas unitarias y 18 recorridos de navegador** correctos. [Publish atlas 39875297617](https://github.com/AlejandroPico/Historicmap/actions/runs/39875297617) correcto; checkout real del mismo SHA confirmado en logs. Comprobación pública del 23/10/2026: JS `index-znTYbs7F.js`, CSS `index-CCx2Aqy8.css`, tres manifiestos idénticos byte por byte a los locales y bytes de los nuevos retratos de Collor/Gadafi verificados por HTTP. Revisión visual pública de Brasil 1990 con Collor/Sarney, fechas y fotos cargadas; evidencia local ignorada `.cache/release-0.6.0-public-1990.jpg`. Detalles en DELIVERY-0.6.0.

El commit documental posterior usa `[skip ci]` y no altera la aplicación validada. Mantener separados los resultados de cobertura automática y el contraste historiográfico: faltan 493 imágenes en la ventana 1990–2026 y cobertura regional de cargos, banderas, conflictos y control efectivo. Se observa repetición de algunas etiquetas nacionales al acercar el mapa; pendiente revisar su colocación entre teselas sin reducir el detalle de las geometrías.


## 15. Actualización 0.7.0 · ficha como espacio de investigación

Solicitud del propietario: incorporar todos los apartados y herramientas acordados, preparando el concepto amplio antes de continuar adquisiciones anuales. Al cambiar de año, ninguna ficha o panel abierto debe cerrarse por el cambio temporal; se actualiza su contenido. Se conservan las cuatro pestañas previas y se añaden Territorio, Instituciones, Sociedad, Economía, Relaciones, Defensa, Historia y Comparar: doce apartados visibles en una cuadrícula compacta, accesible por teclado. Ficha izquierda de 420 px, limitada al ancho disponible, tablas internas desplazables en móvil; no se añaden cabeceras permanentes.

### Persistencia temporal

`selection.ts` crea un ancla de entidad separada del identificador del polígono/periodo. Se resuelve contra los datos comprometidos de la nueva fecha; ID de periodo distinto no implica país distinto. Los controles territoriales usan UID propio, los lugares nombre normalizado e identidad territorial cuando está disponible. No se selecciona el primer sucesor ni el polígono más cercano. Si la entidad no tiene representación activa, la ficha conserva el nombre y la pestaña, explica la ausencia y mantiene cronología, relaciones y comparación. Volver a una fecha válida recupera su representación. Si hay mandatos documentados durante un año cuya instantánea de cierre ya no contiene la entidad (URSS en 1991), se conservan esos mandatos del propio inventario; nunca los de un sucesor. Las ciudades sin registro en la nueva capa no conservan silenciosamente un dato actual como histórico.

Durante la carga, cabecera y contenido anterior conservan su año y aparece «Actualizando a…»; al terminar se actualizan juntos. Se mantienen pestaña, filtros, métricas y posición de lectura, sin mover la cámara automáticamente. Una carga fallida deja explícito que se conserva la ficha anterior. Cerrar o Escape son acciones del usuario; el Escape de un diálogo no cierra además la ficha. Los paneles búsqueda/fuentes/capas se mantienen al usar regla, reproducción, saltos o diálogo de fecha; búsquedas abiertas vuelven a resolver el texto sobre los nuevos territorios. Las futuras fichas deben seguir este contrato: el refresco de fecha actualiza contenido, no visibilidad.

### Apartados y herramientas

`country-card.ts` conserva Autoridades/Datos/Contexto/Conflictos y añade territorio, instituciones, sociedad, economía, relaciones, defensa e historia. Relaciones permite pintar la organización elegida en el mapa. No atribuir a una alianza beligerancia ni inferir régimen jurídico sólo por nombres de cargos. Territorio distingue capital/contorno de referencia actual frente a capital y base anual. Los estados ausentes no reciben datos de sus sucesores.

`country-workspace.ts` reúne definiciones, series, observaciones, formato y gráficos. Catálogo: seis indicadores existentes más 22 adicionales; `profile.codes` resuelve equivalencias explícitas. Último dato <= año consultado y antigüedad máxima cinco años, con año real visible; sin dato no es cero. Los gráficos conservan todo el histórico disponible hasta la fecha, cortan líneas en años ausentes y ofrecen tabla, fuente y fechas navegables por teclado/ratón. No recortar signos negativos legítimos, porcentajes >100 ni índices a una escala inventada. PIB nominal no equivale a crecimiento real; deuda central no equivale a deuda pública total.

`country-history.ts` resuelve registros por fecha (fin exclusivo), enlaces dirigidos y cronología. Integra mandatos, banderas, contextos, participación en organizaciones y el nuevo inventario. El filtro permite mostrar registros posteriores al año consultado explícitamente; por defecto sólo hasta ese año. Fechas que son límites de cobertura no se presentan como fundación/adhesión. La fecha del evento de una relación es distinta de sus anclas navegables. El modelo `CountryRecord` admite secciones institutions/history/territory/society/economy/defense/relations, campos con etiqueta/valor/unidad/fecha/fuente y lugares con coordenadas/fuente. Permite añadir constituciones, elecciones, coaliciones, idiomas/religiones, recursos, comercio, sanciones, bases, servicio militar o patrimonio mediante registros fechados, sin reformar la navegación ni fabricar contenido pendiente.

`country-comparison.ts` muestra dos fechas de la misma entidad (−10000 a año del dispositivo, sin año cero) o hasta cuatro entidades fijadas en el año del mapa. Ofrece autoridades, símbolos, estatus, tabla de magnitudes con años, diferencia B−A y gráficos. «Ver en el mapa» alterna las fechas/entidades conservando el apartado. Compara contornos de la fuente como iguales/diferentes; no certifica exhaustivamente cambios de fronteras o frentes. No fusiona Estados antiguos con sucesores. Las entidades fijadas sobreviven a cambios de fecha y cierre de ficha durante la sesión; recargar la página reinicia esas selecciones.

### Datos, preparación y límites

`country-indicators.json`: 22 indicadores adicionales, 217 claves de economías y 175.996 observaciones 1960–2025. No hay valores 2026 en la descarga. Adquisición/condiciones/atribución individual en COUNTRY-INDICATORS; no extender datos al pasado como si fueran vintages publicados entonces. Las series militares terminan en 2020 y no constituyen una clasificación de poder militar actual. El gasto militar SIPRI se excluye por sus condiciones específicas; no suponer que toda API pública permite redistribuir todas sus series. Una observación negativa inesperada de deuda central se conserva apartada con explicación, no sustituida por cero.

`country-history.json`: 33 relaciones, 28 registros (15 institucionales, 12 históricos y uno territorial), 55 claves y 36 fuentes oficiales. No equivale a 55 constituciones completas o una cronología mundial terminada. Faltan numerosas descripciones institucionales, campos demográficos/culturales, acuerdos/sanciones bilaterales, recursos, socios comerciales, bases y patrimonio. Su estructura ya está integrada; ampliar con fecha, fuente y alcance antes de mostrar valores. Las carencias de medios y cartografía anteriores siguen abiertas.

Preparación: `enrich-country-indicators.mjs` (adquisición explícita con comprobación de licencia/caché) y `prepare-country-history.py` (inventario editorial reproducible), después `register-country-workspace.mjs` para las dos huellas nuevas, `data:verify`, pruebas, compilación y navegador. Hay 41 recursos de datos, 11 franjas de letras y 2.871 medios; no se modifican coordenadas cartográficas en esta versión. Los archivos existentes de autoridades y sus 493 imágenes ausentes no se sustituyen ni se declaran completados.

### Validación y entrega

Publicado **d6a8cfb4119edcf77d50f2133de46111aa5472bb**. [Quality 39881593494](https://github.com/AlejandroPico/Historicmap/actions/runs/39881593494) correcto: **58 pruebas unitarias/13 archivos y 22 recorridos de navegador**, integridad de 41 recursos/11 franjas/2.871 medios y compilación. [Publish atlas 39882159743](https://github.com/AlejandroPico/Historicmap/actions/runs/39882159743) correcto, con checkout real del mismo SHA confirmado en logs.

Verificación pública del 23/10/2026: JS `index-DWRzUWMW.js`, CSS `index-b0OcPlkX.css`, tres manifiestos idénticos byte por byte a los locales y bytes de ambos conjuntos nuevos con SHA-256 correcto. La ficha pública de España conserva Economía al pasar de 2026 a 2000, con contenido/fecha actualizados. Evidencia local ignorada `.cache/release-0.7.0-public-2000.jpg`; informe `.cache/public-verification-0.7.0.json`. Los gráficos y todas las banderas de comparación conservan créditos/proveedores/licencias visibles.

Los resultados locales intermedios, actualización de dos comprobaciones antiguas al nuevo contrato y seis pruebas focales finales se registran en DELIVERY-0.7.0; Quality valida la suite completa sobre la revisión final con créditos. También se verifican los bytes preparados en Git de los 2.923 recursos. El cierre documental usa `[skip ci]` y no cambia la aplicación validada. No confundir apartados disponibles con cobertura completa: siguientes ampliaciones deben rellenar campos/fechas con fuentes, sin perder estas herramientas ni restaurar cierres automáticos de fichas. Las carencias de datos, medios y cartografía previas continúan expresas.


## 16. Ampliación 0.8.0 · historia mundial hasta 1970

El propietario pide continuar la ampliación mundial desde 1990 hasta **1970**, manteniendo todas las herramientas de investigación incorporadas en 0.7. Durante esta entrega añade un requisito permanente: los países/territorios bajo dominio, dependencia o tutela de una potencia deben mostrar **matices de su color principal**, fechados y documentados. La URSS conserva rojo y sus satélites tonos rojizos. El criterio debe poder aplicarse a cualquier potencia/conflicto; no se deduce subordinación de una simple alianza ni de compartir ideología.

### Datos e identidades

Adquisición incremental de cargos nacionales e históricos 1970–1989, preservando curaciones anteriores, licencias, fotografías y precisión. Las oficinas actuales no bastan para jefaturas disueltas; las curaciones focales completan Bulgaria, Mongolia, Nepal, Irán, Birmania, Vietnam, Yugoslavia y regímenes/juntas de América y África. No usar el primer resultado de una búsqueda como identificación: se corrigen homónimos de Ian Smith y Georgi Atanasov mediante identidad humana y biografía. Los órganos colectivos conservan nombre, composición cuando está documentada y ausencia de retrato individual inventado.

Claves nuevas VDR (Vietnam del Norte), RVN (República de Vietnam), VSR (Gobierno Revolucionario Provisional/República de Vietnam del Sur) y RHO. VNM sólo identifica la entidad unificada desde 1976; mandatos continuados se parten por cambio de entidad con nota, sin fingir dimisión o nuevo nombramiento. VSR tiene inventario y navegación explícita, pero CShapes no ofrece contorno separado de su administración en 1975. Se conservan sus mandatos propios en una ficha ausente del mapa. RHO no hereda estadísticas de Zimbabue; 1979 explica la administración británica de transición. Los dos Yemen conservan identidades propias y estadísticas sucesoras vacías.

**Referencia contemporánea: 22/10/2026**; adquisición histórica: 23/10/2026. Se guardan separadamente `retrieved`/`currentReferenceDate` y `historicalRetrieved` en identidades. No avanzar el tope de actualidad por investigar el pasado: las banderas y mandatos actuales estaban acreditados al 22, y cambiarlo al 23 los dejaría sin referencia válida o extrapolaría vigencias. Los límites de cobertura de cargos/organizaciones se rotulan como tales; no son fechas reales de nombramiento/adhesión.

### Cartografía, contexto y relaciones

CShapes ya contenía el periodo. Se conservan sus coordenadas y se corrigen nombres, identidad y unión estadística. Vietnam norte/sur separados hasta 1974; el contorno agrupado de 1975 se declara como control anterior a la unificación formal del 2/7/1976. Salisbury se mantiene hasta 1981. Bangladesh, colonias portuguesas y otras independencias se consultan en sus intervalos de fuente.

Los 23 suplementos Natural Earth son referencias contemporáneas explícitas, con fechas individuales: no admitir todos los pequeños Estados desde 1970 ni confundir admisión ONU con independencia. Marruecos y Mauritania usan contornos CShapes de 1974 en los periodos indicados para evitar incluir los sectores reclamados del Sáhara en la base. La ficha identifica CShapes como su fuente, sin atribuirlos a Natural Earth. Sáhara Español previo y territorio no autónomo posterior conservan la distinción; no se dibuja el muro ni el control diario.

Organizaciones: 31/546 intervalos desde 1970; `startIsCoverageBoundary` sustituye la comparación hardcodeada con 1990. Aplicación territorial CE de Groenlandia no se cuenta como otro Estado miembro. EAC original, cooperación intermedia y comunidad actual conservan discontinuidades. Contexto: 205 fases; inventario institucional/histórico: 50 relaciones y 49 registros. Se separan anticipaciones de Alvor, Constituyente portuguesa, retirada española y pronunciamientos posteriores. `recordsFor` no extiende registros abiertos más allá de `referenceDate`. Fuentes y límites en HISTORICAL-AFFILIATIONS, HISTORICAL-CONTEXT, COUNTRY-HISTORY y ANNUAL-REVIEW.

### Color político

`political-influence.json` y `political.ts` añaden relaciones fechadas de satélite, cliente, bloque con autonomía e intervención. Las colonias/protectorados/mandatos usan la identidad real del administrador del mismo inventario, resolviendo nombre frente a código antes de colorear. Mantener fronteras, entidades y datos propios; sólo cambia pintura. La Rumanía autónoma usa un matiz más suave; Albania después de 1961 y Yugoslavia de 1970 no se convierten en satélites soviéticos. Las transiciones de 1989 cierran relaciones según su fuente, sin deducirlas de la extinción posterior del Pacto de Varsovia.

Las relaciones de ocupación/intervención usan `controlInfluenceColor` y siguen «Ocupaciones y disputas»; el color soberano se recupera al desactivar. Los controles territoriales ya documentados conservan color sólido por potencia y matices de cliente. No inventar influencia mundial completa, porcentajes de dominio o frentes por un parentesco cromático. Fuentes visibles en Territorio/Relaciones y explicación en leyenda. Contrato y pendientes en POLITICAL-COLORS.

### Preparación y validación

Orden: `enrich-1970-authorities.py` → `curate-1970-focus.py` → `curate-1970-americas-africa.py --apply` → `curate-1970-asia.py --apply` → `curate-1970-party-leaders.py --apply` → `enrich-1970-portraits.py` → `enrich-1970-flags.py` → `curate-1970-symbols.py` → `prepare-recent-supplements.py` y `prepare-country-history.py` → `register-1970-data.mjs` → verificación/auditoría/pruebas/compilación/navegador. Los scripts de autoridades recientes 0.6 se conservan para trazabilidad; no sustituir esta ampliación por una reconstrucción inicial que elimine curaciones. Las consultas de cargos incluyen el límite temporal en la clave de caché para no reutilizar accidentalmente resultados recortados a 1990.

Estado de entrega y cifras finales en DELIVERY-0.8.0. No presentar código local como ya publicado. Persisten falta de imágenes, variantes de bandera, autoridades coloniales/secundarias, reconstrucción de control y frentes del Levante, entre otros límites previos. Conservar ficha y herramientas al ampliar los datos; la siguiente ampliación anual debe contrastar fuentes por región antes de afirmar exactitud exhaustiva.


Inventario final de 0.8: 278 claves/6.945 mandatos; en 1970–1989, 1.852 registros/1.144 personas u órganos, 867 con imagen/277 sin ella. 3.474 medios (395 SVG + 3.079 fotografías), 150.116.391 bytes, 603 medios netos más que 0.7. Se adquirieron once diseños focales de bandera; la identificación ambigua de Traykov se omite y se excluye de posteriores adquisiciones. El símbolo de una entidad no puede superar su existencia por el rango anual de un nombre de archivo. Cifras con denominadores y límites en HISTORICAL-AUTHORITIES/SYMBOLS-1970.


La curación adicional de partido incorpora 25 mandatos; los reyes Mahendra y Sisavang Vatthana y el Consejo de Estado de Heng Samrin completan las fichas focales. Los fines de cobertura de Deng y Heng no se presentan como ceses. Mantener precisión anual/mensual en tarjetas, instituciones y cronología; la insignia de titular al cierre sólo procede con fechas diarias acreditadas. Las dependencias actuales clasificadas explícitamente por Natural Earth también reciben matices de su soberano; no aplicar esta regla a simples reclamaciones o territorios disputados, ni retroproyectar perfiles de 2026 al periodo histórico.

### Entrega publicada y comprobada

Aplicación publicada **a5d1c022334a32ccaf67b09d2da5829841293aaa**. [Quality 39976077710](https://github.com/AlejandroPico/Historicmap/actions/runs/39976077710): 97 pruebas/18 archivos y **24 recorridos de navegador**, integridad de 42 datos/11 franjas/3.474 medios, compilación correctas. [Publish atlas 39977495176](https://github.com/AlejandroPico/Historicmap/actions/runs/39977495176) correcto, checkout real del mismo SHA confirmado en logs. La primera ejecución pasó 23/24 recorridos: la comprobación antigua de ocupaciones aún esperaba ocultar toda la leyenda. Ahora comprueba que desaparece sólo la leyenda de control y permanece la explicación de familias; al reactivar vuelve el control. No se debilitó el criterio ocultando la nueva explicación.

Verificación pública del 23/10/2026 a las 17:22 (Madrid): JS `index-mYYkwgiZ.js`, CSS `index-b0OcPlkX.css`, tres manifiestos y seis conjuntos históricos idénticos, cinco retratos y bandera búlgara comprobados por SHA-256. Evidencia de navegador `.cache/release-0.8.0-public-1970.png`: Bulgaria, emblema histórico y Zhivkov; matices rojos visibles en el bloque soviético. Informe `.cache/public-verification-0.8.0.json`. También se comprobó la pintura sobre los datos cartográficos reales de POL/HUN/CSK/BGR/DDR en 1970/1980/1988. El cierre documental `[skip ci]` no cambia la aplicación validada.


## 17. Corrección 0.8.1 · estabilidad de datos y autoridades de dependencias

El propietario reproduce pérdida de datos al ir de 1970 a 1954 y volver: Francia/España pasan a «Área del mapa». No es falta de descarga. El test de clic real reproduce el problema y el motor instalado geojson-vt6.3.0 confirma la causa: `removeAllProperties` retorna un objeto vacío antes de procesar `addOrUpdateProperties`. El hilo principal conserva datos que las teselas pierden. `sourceDiff` ahora elimina claves de forma explícita y añade propiedades sin ese indicador. Mantener resolución, geometrías y actualización incremental; no sustituir esta corrección por recargas completas o modificaciones de node_modules. `canonicalFeature` consulta los registros activos por ID para clics de territorios, controles y lugares; una ficha no se construye con propiedades parciales de teselas.

Segundo problema independiente: `identityKey` descartaba colonias para evitar heredar el Gobierno de un Estado sucesor, dejando vacíos cargos de metrópoli y locales. `territorial-administrations.ts`/JSON contienen once relaciones fechadas y un fallback de administrador documental de la fuente. `administratorKey` es distinto de `dominantPower`: una alianza/satélite coloreado no implica que se deban heredar autoridades. La relación colonial permite identidad territorial estable y autoridades locales fechadas; el Gobierno independiente posterior no aparece en 1970.

Las autoridades del territorio y las estatales externas se presentan separadas, con ámbito, fechas y fuente. Autonomía de Surinam/Bahamas: heredar únicamente la jefatura del Estado de la Corona y conservar el Gobierno propio. Independencia cierra la relación sin afirmar dimisión nacional; las fichas mantienen ambos tramos del año y sobreviven a cambios de fecha. Namibia requiere explicar administración efectiva ilegal, no soberanía reconocida. Departamentos franceses no se rotulan simplemente colonia por la categoría general de CShapes. Sáhara conserva transición española hasta febrero de1976, sin prolongar Franco ni asignar Marruecos automáticamente a todo el territorio. Un símbolo de metrópoli se identifica como tal; jamás copiar sus estadísticas o alianzas al territorio.

Preparación incremental: `prepare-dependent-authorities.py` añade cinco cargos focales (Fouché, Ferrier gobernador, Sedney, Pindling preindependencia, Pérez de Lema). `enrich-1970-portraits.py --people Q886942 Q924337` limita adquisición a dos retratos pendientes; manteniendo P18 humano/licencia/huella. `register-dependent-authorities.mjs` registra identidades y el nuevo conjunto. Referencia contemporánea22/10/2026 conservada; no avanzar el horizonte de cargos actuales al investigar el pasado. Son43 recursos/11 franjas/3.476 medios. Fuentes primarias, fechas y pendientes en DEPENDENCY-AUTHORITIES-RESEARCH y DELIVERY-0.8.1. La serie completa de autoridades territoriales/rivales aún es parcial; el fallback no la acredita completa.

Validación final y publicación verificadas en DELIVERY-0.8.1. Las pruebas cubren el motor de teselas, clics reales ida/vuelta, recorte de administración, gobiernos autónomos, ausencia de extrapolación y persistencia de fichas al independizarse. El año1954 es una reproducción del error estructural, no una ampliación de la tanda bibliográfica anterior a1970.


### Cierre público de 0.8.1

Publicado **911f7c3c55466e4f757a271ec8f5ee740e5eea1b**. [Quality 39984546199](https://github.com/AlejandroPico/Historicmap/actions/runs/39984546199) correcto: 103 pruebas/19 archivos, integridad de 43 recursos/11 franjas/3.476 medios, compilación y **26 recorridos de navegador** correctos (12min). [Publish atlas 39986404919](https://github.com/AlejandroPico/Historicmap/actions/runs/39986404919) correcto, checkout real del mismo SHA confirmado en logs. No dar por válida una fecha sólo por `data-loaded-year`: esperar también `data-rendered`, comprobar ausencia de error y consultar con clic real.

La revisión visual encontró una segunda causa: `queryRenderedFeatures` inmediatamente tras actualizar la fuente podía consultar teselas anteriores contra el nuevo índice y lanzar `feature index out of bounds`. Se elimina esa consulta prematura; el siguiente idle con mapa no ocupado acredita el dibujo y se solicita repintado. Los clics esperan esa acreditación. No ocultar la excepción ni recuperar a ciegas propiedades de otra entidad. La revisión posterior de los dos recorridos y la suite completa confirma que no reaparece el aviso.

Verificación pública 23/10/2026, 18:25 Madrid: JS `index-BA5eVcf8.js`, CSS `index-b0OcPlkX.css`, tres manifiestos idénticos, siete conjuntos y cinco retratos más símbolo portugués verificados por SHA-256. Informe `.cache/public-verification-0.8.1.json`. Se verifican públicamente Francia 1970→1954→1970 y posterior clic real (bandera, Pompidou/Chaban-Delmas, color y nombre); Surinam con Sedney/Ferrier/Juliana; Angola con Caetano/Tomás. Evidencias reales `.cache/release-0.8.1-public-france-return.png` y`.cache/release-0.8.1-public-angola-1970.png`. La ficha pública queda abierta en Angola 1970. El cierre documental `[skip ci]` no cambia aplicación/datos. Los mandatos se recortan a la relación administrativa y al horizonte documental, no al final del año consultado: conservar fechas de cese reales aunque sean posteriores al año de vista.


## 18. Ampliación 0.9.0 · control integrado y década de 1960

El propietario cambia expresamente la representación anterior: el mapa político debe representar el control territorial en sus propias formas y seleccionar al controlador. «Ocupaciones y disputas» pasa a ser un resaltado opcional con franjas; **no restaura soberanía/control alternativos** al apagarse. Queda apagado al abrir. Franjas gruesas del controlador y finas del territorio ocupado, proporción 3:1. Una anexión/incorporación documentada no recibe franjas de ocupación ordinaria; las reclamaciones contemporáneas no se convierten en soberanía reconocida.

`control-map.ts` realiza particiones, diferencias y uniones; `control-worker.ts` las calcula fuera del hilo de interfaz y `control-loader.ts` mantiene como máximo tres resultados recientes. `polygon-clipping` **0.15.7**, MIT, añadido tras verificar la versión del registro y documentación primaria. No se cambian archivos de coordenadas originales ni se exporta una geometría mundial con licencia ficticia. CShapes y componentes de control Cliopatria BY4 conservan atribución/limitaciones; la partición española BY-SA3 sobre Natural Earth se incorpora como colección independiente reemplazando componentes cubiertos, sin recortar CShapes NC-SA con esa geometría incompatible. Componentes españoles fuera de la cobertura se conservan. No eliminar esta distinción por comodidad.

El ámbito alemán documentado de 1938 se usa como máscara de incorporación para evitar marcar Austria/Sudetes como ocupaciones posteriores; no inventa todas las anexiones parciales posteriores. Los contornos contextuales de retirada del Sinaí 1979–1981 no se usan como si representaran una fase geométrica acreditada. Crimea/Golán/Sinaí/Kuwait conservan identidad del territorio ocupado documentada, incluso cuando una referencia moderna incorpore el contorno al controlador de facto. Las fases y límites diarios que las fuentes no contienen siguen pendientes.

Se conservan las correcciones 0.8.1: borrados explícitos de propiedades, registro canónico por ID, guardas de peticiones y de renderizado, consultas de teselas sólo después de idle y persistencia de fichas. Las franjas no alteran el país seleccionable. Las capas estadísticas y de organizaciones conservan sus escalas; un matiz de tutela no acredita control de cada punto del país ni beligerancia automática.

El fondo Natural Earth queda bajo todo el dominio cartográfico histórico, excluidos geología/concepto. Distingue tierra y océano cuando falta una entidad en el inventario, incluidos África 1889 y Arabia 1918. **No significa tierra despoblada, sin soberanía o sin conocimiento local**. Es costa contemporánea de referencia, no paleocosta. La leyenda y fuentes explican esa diferencia.

### Paleta y entrada del propietario

`historical-palette.ts` contiene 33 familias editoriales con alias explícitos: Roma púrpura, Bizancio violeta distinto, imperio español dorado, Francia napoleónica azul, Alemania nazi gris, URSS roja y Reino Unido rosa malva para mantener contraste. Dependencias documentadas comparten matices de la potencia; alianzas e ideologías semejantes no bastan para inferir subordinación. Regímenes focales y Portugal cambian de color por etapas. La paleta no clasifica Roma como socialista ni pretende colores oficiales de todos los Estados históricos.

`docs/POLITICAL-PALETTE.csv`, generado por `scripts/export-palette.mjs`, permite revisar la convención implementada. **No es el CSV adjunto original**: `C:/Users/darim/Downloads/lista_imperios_completa_v3.csv` no estaba disponible y no se localizó. No afirmar que se importó, atribuirle filas no leídas ni considerar conciliados todos los imperios. La conciliación queda pendiente de recuperar ese archivo. Se utilizan las preferencias verbales y decisiones editoriales explícitas.

### Ampliación documental

Adquisición incremental 1960–1969: `enrich-1960-authorities.py` parametriza el motor anterior con etiqueta propia, conserva adquisiciones 0.8 y curaciones, incluye el suelo temporal en la caché y no avanza la referencia actual del 22/10/2026. `curate-1960-authorities.py` importa propuestas investigadas tras revisión del responsable; son datos de entrada, no instrucciones externas. Distingue mandatos y ventanas interiores, sin presentar sus límites como nombramiento/dimisión. Se mantienen órganos colectivos sin retratos inventados y los huecos de suplencias como pendientes.

Identidades YMK (reino yemení), TAN, ZAN y UAR evitan heredar datos sucesores. Egipto/Siria se agrupan durante la unión hasta el cierre de 1960 y se separan desde 1961; Egipto conservó el nombre RAU sin prolongar la unión. UNTEA distingue Rolz-Bennett y Abdoh: nombramiento de Abdoh 22/10/1962, ejercicio efectivo desde15/11; administración transferida a Indonesia1/5/1963. El resolver conserva ambas administraciones dentro del año de transferencia y el símbolo del administrador al cierre. No confundir la firma del acuerdo de agosto con comienzo efectivo.

Capitales/topónimos corregidos: Dar es Salaam antes de la designación de Dodoma, Salisbury en la federación rodesiana, Santa Isabel antes de1973. Las excepciones diarias aún no contrastadas de la fuente, periodización de Zanzíbar y disolución federal se registran en RESEARCH-1960 y no se dan por resueltas mediante una foto. Los suplementos son25 contornos contemporáneos de referencia, con suelo1960, Samoa/Nauru desde sus fechas propias y Kuwait/Bahréin protegidos antes de independencia, sin dibujar Estados sucesores retroactivamente.

Catálogo final local: **283 claves/7.481 mandatos**, **3.788 medios** (439 SVG y3.349 fotografías), 43 recursos/11 franjas tipográficas. Son268 archivos fotográficos adicionales y312 medios netos frente a0.8.1; no equivale a312 países ni a fotografías de todos los titulares. Auditoría del resolver: **1.693 país-años**, cero huecos de resolución, **122 personas/órganos sin imagen** y**20 país-años sin símbolo** en la ventana revisada. La lista durable `docs/REVIEW-1960.json` conserva nombres/años: no confundir resolución de una autoridad con todas las jefaturas, mandatos, sucesiones y frentes exhaustivamente contrastados.

El preparador de retratos reutiliza medios ya acreditados para nuevos mandatos de la misma persona sin reemplazar imágenes curadas existentes. `--image QID COMMONS_TITLE` permite una alternativa contrastada, manteniendo identificación humana, exclusiones y comprobación de licencia. En esta entrega se incorpora `De_Gaulle-OWI.jpg` (OWI/Library of Congress, dominio público; [ficha](https://commons.wikimedia.org/wiki/File:De_Gaulle-OWI.jpg)), porque el P18 principal no superaba el criterio de licencia automática. No se amplía globalmente la lista de licencias aceptadas.

El worker clona objetos al comunicarse con la interfaz. `sourceDiff` compara el valor de geometrías que no comparten referencia para evitar reprocesar costas idénticas durante cada salto anual; la composición conserva entidades sin intersección. Mantener la prueba de clon estructurado y los recorridos de todos los años y reproducción: una regresión aquí vuelve a introducir retrasos aunque los nombres y colores sean correctos.

Organizaciones:31/549 intervalos desde1960; fases contextuales:258; historia/instituciones:59 relaciones/53 registros. Altas, bajas, categorías, ruptura albanesa, asociación yugoslava y entrada mongola se distinguen de límites de cobertura. Conflictos contextualizados no generan frentes ficticios. Fuentes primarias y discrepancias en RESEARCH-1960 y AUTHORITIES-1960-RESEARCH.

### Preparación y relevo

Orden incremental: adquisición1960 → curación asiática anterior para recortar mandatos vietnamitas a sus entidades → administraciones dependientes → curación1960 → retratos por ventana → importación genérica de símbolos1960 → curación1970 (preserva variantes/exclusiones) → curación de símbolos1960 → suplementos/contexto → pruebas de cobertura → `register-1960-data.mjs` → integridad/tipos/pruebas/build/navegador. Si se repite una curación de autoridades después de símbolos, ejecutar de nuevo la exclusión de la imagen ambigua de Traykov: el test lo exige. Nunca sustituir adquisición incremental por inicialización destructiva ni mover el tope de actualidad por investigar el pasado.

Validación y publicación finales se registran en DELIVERY-0.9.0 y tareas.md con resultados/SHA reales. No dar esta entrega por publicada por tener versión/build local. Los huecos de retratos, variantes, suplencias, regímenes, fronteras y frentes siguen abiertos, con inventario; el CSV original sigue pendiente. Las fichas anteriores a la ventana revisada que no se pueden seleccionar permanecen en backlog explícito, no se declaran corregidas al retroceder una década.

## 19. Corrección0.9.1 · conservación de medios y cargos revisados

0.9.0 publicada en `ba7eb3b8ab505a277f5fb5f59c6e18eeb06084af`; Quality40005916966 superó114 unitarias y28 recorridos, Pages40008258279 terminó correctamente y se verificaron bytes públicos. La corrección0.9.1 se registra aparte; su cierre efectivo corresponde a DELIVERY-0.9.1 y tareas, no a una suposición por haber pasado la versión anterior.

El preparador de1960 ahora obtiene los retratos **antes** de retirar sus mandatos regenerables. De otro modo desaparecía la referencia al medio de personas que sólo figuraban en esos registros. La recuperación focal devuelve26 retratos acreditados que ya existían en el inventario; no son archivos nuevos. Se conserva una regresión para el retrato de Abdoh. El adquiridor permite `--original` para probar el original publicado cuando procede, manteniendo licencia, identificación, exclusiones y lectura limitada a5MB; no se convierten candidatos sin aprobar en retratos válidos.

Azikiwe queda como presidente parlamentario de Nigeria y Balewa como jefe del Gobierno. Una afirmación genérica duplicada de Q500282 no convierte a ambos en primeros ministros. La consolidación utiliza las declaraciones que sobreviven a la curación, evitando recuperar cargos descartados al fusionar duplicados. Las fechas del relevo de enero1966 siguen pendientes de contraste diario; fuente institucional de la distinción en AUTHORITIES-1960-RESEARCH.

Cifras posteriores a esta corrección: **283 claves/7.480 mandatos**, **3.793 medios** (439 SVG/3.354 fotografías); **1.693 país-años1960–1969**, sin huecos de resolución, **91 personas/órganos sin retrato** y**20 país-años sin símbolo**. Sustituyen las cifras de122 vacíos/7.481 mandatos del estado0.9.0. `docs/REVIEW-1960.json` identifica los vacíos; `docs/reference/portrait-1960-pending-research.json` conserva pistas:76 sin P18,12 candidatos pendientes y tres órganos/identificadores documentales. No certificar completitud mundial a partir de cobertura del resolver.

Pendientes obligatorios: recuperar el CSV original ausente y cotejarlo, resolver imágenes/variantes AND-SMR sin inventar diseños, completar relevos diarios y mandatos secundarios, frentes detallados y entidades tempranas. Seguir la pizarra, conservar SHA de aplicación y evidencia de Quality/Pages/publicación separados del último commit documental. No recompilar ni cambiar rama mientras se prueba el directorio servido. Un fallo local por mezcla de archivos no justifica omitir el siguiente recorrido ni atribuirlo sin cotejar los bytes.

La revisión final de0.9.1 incorpora cinco retratos de India con GODL-India: el adquiridor confundía la subcadena «nd» dentro de «India» con la marca NoDerivatives. La comprobación ahora exige el token ND y conserva la lista de licencias, créditos, exclusiones y límite de lectura. No se amplían por ello otras licencias. El inventario queda en3.793 medios/439 SVG/3.354 fotografías y91 vacíos de retrato. El candidato c42531d queda sustituido por el siguiente commit de0.9.1.

Publicación: Quality limita concurrencia por rama y cancela ejecuciones superadas del mismo grupo. Pages sólo publica un éxito de push cuyo head_sha coincida con github.sha, el último commit de la rama predeterminada en workflow_run; el checkout sigue fijado a la revisión verificada. Una ejecución anterior puede finalizar correctamente y omitir publicación por haber sido superada. Esperar Pages y bytes públicos antes del commit documental de cierre, que se sube con [skip ci]. Referencias: [evento workflow_run](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run), [concurrencia](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).

Cierre efectivo de0.9.1: aplicación f67f8aecf9acc19e51e7f49648ea81e12008b34d, Quality40011433956 (115 unitarias/23 archivos y28 recorridos), Pages40013402559 con build/deploy correctos y checkout de ese SHA. Bytes públicos cotejados:4 archivos de aplicación,3 manifiestos,7 conjuntos de datos y16 medios, incluidos los5 de India. Evidencia durable en docs/reference/public-verification-0.9.1.json y DELIVERY-0.9.1. Vista pública comprobada: India1966, cuatro retratos cargados y sin errores de consola. El candidato c42531d pasó sus comprobaciones pero Pages40011732004 se omitió correctamente por estar superado.

El cierre posterior conserva documentación y aserciones geográficas adicionales verificadas localmente (4 pruebas), sin cambiar la aplicación ni los datos publicados. Se usa [skip ci] únicamente para ese cierre: no reproducirlo si se modifica código de aplicación, datos, dependencias o flujos de publicación. La web publicada y el último commit documental tienen SHA distintos de forma deliberada. No hay tareas operativas de publicación pendientes; las carencias de investigación permanecen en tareas.md.


## 20. Ampliación0.10 · década de1950 y organización por entidades

Encargo del propietario: ampliar a1950, organizar las entidades en carpetas y dejar fija la parte superior de la ficha. **La instrucción vigente de Git sustituye el cierre automático anterior:** comprobar localmente, subir y terminar sin esperar ni consultar Actions/Pages. El propietario notificará despliegue o errores y solicitará revisión pública. No cambiar los controles de Quality/Pages ni presentar una subida como publicación comprobada.

Adquisición incremental con enrich-1950-authorities.py, curación propia con curate-1950-authorities.py, retratos por ventana y curate-1950-symbols.py. Conservar retratos antes de retirar registros regenerables. No ejecutar adquisiciones iniciales destructivas ni avanzar la referencia contemporánea22/10/2026. prepare-1950-dependencies.py extiende relaciones a1950, separando Surinam antes/después de1954 y Puerto Rico antes/después de1952. prepare-1950-context.py añade organismos/contextos conservando lo posterior; las fechas de cobertura no son adhesiones o ceses jurídicos.

VSV es Estado de Vietnam, anterior aRVN; MAL es Federación de Malaya, anterior aMYS. No heredan automáticamente estadísticas sucesoras. Transiciones navegables fechadas en country-history. Se corrigen jefaturas formales/efectivas focales de Corea/Taiwán, presidencia colegiada uruguaya, monarquía/regencia egipcia, independencia de Guinea y confirmación del Gobierno de Grotewohl. La corrección de Kim anterior a1972 conserva su presidencia posterior. Una cobertura resuelta no certifica todas las autoridades locales, suplencias diarias ni frentes.

Países contiene un índice y resumen generado por entidad incorporada en las fuentes. Identidades con QID distintos se mantienen separadas. Los resúmenes incluyen banderas, mandatos y referencias territoriales; los medios y geometrías siguen en sus colecciones originales sin duplicarse ni mezclar licencias. El preparador del catálogo sincroniza esta vista desde public/data, que conserva la adquisición/curación. No editar entidad.json: editar la fuente preparada con su script. recursos.json y archivos/ son entradas manuales que se conservan; la compilación detecta audio/PDF con clave, fechas, autoría/fuente y licencia. No hay himnos adquiridos ni reproducción automática por defecto. Instrucciones en Países/README.md.

La ficha fija identidad/título y pestañas; sólo country-content se desplaza. Conservar/restaurar ese scroll al actualizar el año; no volver a usar el scroll de selection como posición de lectura. Las acciones de comparar quedan dentro de Comparar. Se retira el desplegable de fuente de bandera, manteniendo un enlace accesible desde el símbolo a autoría/licencia. La X permanece. Mantener las pruebas de persistencia y comparación en escritorio/móvil.

Cifras y resultados efectivos se registran en DELIVERY-0.10.0 y tareas.md. Fuentes y limitaciones en RESEARCH-1950 y REVIEW-1950. Mantener pendientes de medios/variantes, autoridades secundarias, fechas diarias, Sarre/Berlín y frentes detallados. El CSV original ausente sigue pendiente; no se ha importado. No borrar esos pendientes por finalizar el código de esta ampliación.


Cierre público de0.10.0 tras aviso del propietario: aplicación fe3676cb8f2dfa164466eae5f4050b2006b54492 comprobada en GitHub Pages el24/10/2026. Coinciden26 archivos(HTML/JS/CSS, tres manifiestos, seis conjuntos y14 medios). En navegador: versión0.10.0 visible, Egipto1952 con nueve referencias de retrato cargadas, cabecera/pestañas inmóviles al desplazar, ficha conservada al pasar a1953 y comparación en su pestaña; sin errores de consola observados. Evidencia en docs/reference/public-verification-0.10.0.json y DELIVERY-0.10.0. No se sondearon Actions/Pages ni se repitió la suite completa; el cotejo público no certifica exactitud histórica exhaustiva. La etiqueta Actualización de Acerca de conserva23/10 frente al historial de24/10: pendiente cosmético para una próxima entrega, registrado en tareas. Cierre posterior sólo documental con[skip ci], separado del SHA de aplicación.

## 21. Ampliación 0.11.0 · 1920–1949

Encargo del propietario: continuar hasta 1920, conservando lo ya incorporado. Sigue vigente la instrucción de comprobar localmente y subir una sola entrega coherente, **sin esperar ni consultar Actions/Pages**. Sólo revisar la versión pública tras su aviso. No confundir subida con despliegue comprobado.

Adquisición incremental `enrich-1920-authorities.py`, sin cambiar la referencia contemporánea del 22/10/2026. Los registros históricos se preparan el 24/10. Cuatro curadores separados: autoridades focales, Europa/Asia, Américas y regiones. Se comprobaron en copias dos aplicaciones idénticas; capturar retratos antes de eliminar registros regenerables. Preservar exclusiones y la fotografía íntegra de Mozambique. No volver a una inicialización destructiva ni usar límites de cobertura como investiduras o dimisiones.

RSR distingue Rusia soviética antes de la URSS; ROC la República de China continental; YKM la monarquía yugoslava; DAN la Ciudad Libre de Danzig; TIB el Gobierno tibetano de facto con soberanía disputada; RSI la República Social Italiana. No transferir estadísticas de Estados sucesores. RSI tiene inventario documental y símbolos, pero no un frente propio validado en esta entrega. Mantener separación de jefatura formal, poder efectivo, regencia, Gobierno en el exilio y control territorial. Las administraciones alemanas de ocupación son órganos, no presidentes ficticios; no hay bandera nacional alemana inventada para 1945–1949.

La adquisición reintrodujo una atribución falsa de presidencia de Yan Xishan y un intervalo anual cuyo extremo el 1/1/1950 sobrevivía junto a la curación. El archivo del Ejecutivo acredita su mandato de primer ministro del 13/6/1949 al 10/3/1950; se sustituyen esas afirmaciones y se amplía la antigua ventana conservadora de febrero de 1950. No recuperar esos cargos al regenerar. La fuente distingue ejercicio, nombramiento y gabinete. Las presidencias turcas no se duplican automáticamente como jefaturas de Gobierno.

Corrección cartográfica acotada: CShapes termina Danzig en agosto de 1938, un año antes. `periodsAt` conserva el registro original y ajusta la validez observada a 15/11/1920–31/8/1939. `composeControl` resta su contorno de los demás componentes después de integrar controles en 1938 y lo añade una sola vez como DAN. Sin esa resta habría dos propietarios superpuestos. Puntos de Danzig/Berlín/Viena comprobados; no se modifica `history.topojson`. Atribución y licencias originales permanecen separadas. Esta excepción no certifica otras fronteras o fases omitidas.

La revisión en navegador reproduce otro atasco en Rusia 1920→1921 con ficha abierta: se alcanza el año nuevo pero aparecen excepciones de índice de tesela y no se acredita el renderizado. El resaltado de selección usaba `setFilter`, que reanaliza las mismas teselas durante la actualización incremental de fronteras. Se sustituye únicamente ese resaltado por `feature-state.selected` en la opacidad del contorno; cerrar/actualizar la ficha limpia el estado anterior. Mantener las diferencias incrementales, los borrados explícitos de propiedades, la resolución canónica y la acreditación posterior en idle; no usar recargas globales ni ocultar excepciones para superar la prueba. El recorrido incluye ficha persistente y clic real sobre Rusia después del cambio de año.

Administraciones desde 1920: 24 relaciones, diferenciando colonias/departamentos franceses desde 1946 y Austria bajo control alemán. La continuidad de títulos etíopes durante el exilio no implica control del territorio ocupado. Suplementos de referencia desde 1920 para omisiones de las fuentes; Vaticano sólo desde el 7/6/1929. No son paleocostas ni geometrías históricas independientes. Se conserva el fondo continental, el mapa de control integrado y las franjas opcionales apagadas por defecto.

38 organizaciones y 887 intervalos de membresía; Sociedad de Naciones y ONU añadidas con sucesión, representación, retirada e ingreso gradual. La OTAN entra en vigor el 24/8/1949; firma, ratificación y entrada en vigor no son siempre la misma fecha. Los fundadores de la OEA desde 1948 se identifican como signatarios, sin afirmar que la Carta estuviese ya en vigor antes de diciembre de 1951. 329 fases contextuales, 80 registros históricos/institucionales y 76 enlaces de entidades. No deducir subordinación ni beligerancia de una membresía.

Catálogo local: 290 claves y 9.485 mandatos; 4.863 medios (478 SVG y 4.385 fotografías), incremento neto de 774 fotografías y 27 SVG. Se preparan 87 ventanas adicionales de símbolos; un intervalo no equivale a un archivo nuevo. 2.787 carpetas en Países, 290 con inventario de autoridades. Las variantes heráldicas, usos civiles/estatales y límites de normalización quedan en SYMBOLS-1920 y SYMBOLS-1920-EXTRA; no retroproyectar diseños posteriores por comodidad.

Auditoría: 5.294 entidades/año de fuente y suplementos, más 70 controles/año activos. Cero huecos de **resolución de alguna autoridad**; quedan 122 personas/órganos sin retrato (118 personas y cuatro órganos) y 165 casos anuales sin símbolo, incluidos cuatro cierres de ocupación alemana sin bandera nacional. No es un censo exhaustivo de cargos, suplencias, administradores locales o frentes. Listas nominales en REVIEW-1920-1949.json, fuentes en RESEARCH-1920 y los tres documentos de autoridades. Mantener pendientes de regímenes breves, fechas diarias, regencias, símbolos, fronteras detalladas y CSV original ausente. Cifras de pruebas, compilación, navegador y entrega efectiva en DELIVERY-0.11.0 y tareas.md.

La agrupación occidental alemana de CShapes1945–1948 no se interpreta como administración exclusiva de Estados Unidos: `collectiveAdministration` conserva el propietario original en sourceOwnerName y documenta las tres potencias; se excluye el fallback a un único Gobierno/bandera. Los cargos de ocupación conjuntos se mantienen en la identidad alemana; no se crea una bandera nacional común.


## 22. Corrección0.11.1 · coherencia de pruebas y cobertura

El registro de Quality aportado por el propietario para0.11.0 muestra27 recorridos correctos y tres fallidos. Las tres aserciones suponían la cobertura anterior: selector desactivado en1947, ausencia de cualquier autoridad alemana en1946 y una única persona en España1939. El contrato actual exige organizaciones desde1920, administraciones colectivas documentadas y todos los mandatos que intersectan el año. No alterar datos válidos para recuperar esos supuestos.

Los recorridos comprueban ONU1947 con57miembros, OTAN todavía inactiva y selector desactivado en1919; autoridad aliada colectiva sin bandera alemana ni retrato personal ficticio o atribución exclusiva aTruman; Franco yAzaña en1939 con fin del mandato deAzaña27/2/1939. Los selectores personales son explícitos y no presuponen una única jefatura. Se espera renderizado además de descarga en los dos archivos de pruebas afectados. No se omiten pruebas, no se activan reintentos ni se modifican los flujos deQuality/Pages.

La ayuda visible de organizaciones todavía indicaba1960 y se corrige a1920. Los datos históricos, sus manifiestos, geometrías y medios no cambian. Versión0.11.1, resultados efectivos y continuidad en DELIVERY-0.11.1 y tareas.md. Comprobar localmente, subir y terminar sin esperar ni sondear el despliegue; revisión pública sólo tras aviso del propietario.

Validación local de0.11.1:129 pruebas/28 archivos, tipos y compilación correctos; los tres recorridos afectados pasan en2,6min, incluida la parte móvil. Los otros27 recorridos constan como correctos únicamente en el registro de0.11.0 que aportó el propietario; no se han repetido localmente. `public/`, `Países/` y `.github/` idénticos respecto a8990dcc. Entrega preparada a main; el flujo termina al confirmar el envío, con revisión pública pendiente del aviso del propietario.

## 23. Ampliación0.12 ·1900–1919

La prioridad vigente es ampliar hasta1900 y conservar1920–actualidad. Mantener la instrucción del propietario: comprobaciones locales, subida y fin; no esperar ni consultar Actions/Pages. La entrega y evidencia efectivas se registran en DELIVERY-0.12.0 y tareas.md. El despliegue sólo se revisará tras su aviso.

`enrich-1900-authorities.py` ejecuta el motor anterior sobre una copia temporal y fusiona únicamente la ventana1900–1919. No usar el motor genérico directamente sobre el catálogo final: puede reintroducir afirmaciones posteriores ya rechazadas. La fusión es idempotente y comprueba conservación de todas las banderas y mandatos que alcanzan1920. Curaciones separadas: autoridades focales, Europa/África, Américas, Asia y regiones. Sus funciones son puras e idempotentes y capturan retratos antes de retirar sus propios registros. La adquisición de imágenes se ejecuta entre mutaciones, nunca junto a otro preparador que escriba identidades/medios.

Claves propias: RUE, RPR, AUT-HUN, OTT, QING, SRK, MNK, KEM, TRV, ORF yCFS. RUE yQING se distinguen de sus sucesores; RPR es una identidad documental sin polígono propio al cierre de1917. Las autoridades imperiales/provisionales aparecen como predecesoras en las fichas anuales de transición, sin hacerlas integrantes del Gobierno sucesor. GuillermoII, NicolásII, Carlos, sultanes, regentes y Gobiernos rivales no se confunden con sus títulos posteriores o con poder efectivo homogéneo. Las fechas rusas usan calendario gregoriano y explican la conversión del juliano. El breve restablecimiento de Puyi1917 no es una continuidad imperial hasta Manchukuo.

Las claves monárquicas serbia/montenegrina y la exclusión de estadísticas sucesoras están limitadas al periodo anterior a1918. Una primera prueba detectó que se aplicaban también a las repúblicas surgidas en2006: quedó corregido, con regresiones positivas de nombre, clave, estadísticas y resolución de autoridades actuales. La navegación checoslovaca distingue enlaces salientes a sucesores de la nueva relación entrante desdeAustria-Hungría; no eliminar un predecesor válido para satisfacer el recuento antiguo.

Correcciones de metadatos, sin modificar `history.topojson`: Corea pasa de imperio a protectorado impuesto1905 y colonia1910; Transvaal/Orange son colonias británicas tras la paz de1902; CFS es soberanía personal deLeopoldoII antes15/11/1908, separada del Gobierno belga; el N/A deMarruecos1904–1911 no borra su sultanato. La ficha marroquí mantiene al sultán junto a autoridades externas francesas. Tonga protegido se añade como contorno contemporáneo de referencia, con su propia monarquía, distinta de una anexión. Afganistán conserva a sus emires durante la tutela británica de relaciones exteriores. Los inicios de cobertura no son fechas de fundación. Son32 relaciones administrativas y26 referencias geográficas; no son fronteras militares nuevas.

El resolver de símbolos contempla una transición bajo el mismo administrador durante un año: enCorea1910 el fin de la relación de protectorado no elimina el símbolo japonés de la etapa colonial al cierre. Los cargos anteriores siguen rotulados con su tramo de cobertura, no se inventa una nueva investidura del emperador japonés. El pabellón mercante austrohúngaro se identifica en la cabecera como tal: no existe aquí una bandera nacional común inventada.

Catálogo0.12:302 claves/10.244 mandatos;5.262 medios(499SVG y4.763 fotografías), incremento neto378 fotografías/21SVG. Son76 ventanas nuevas de símbolos1900–1919 y una adicional eslovaca1939; no equivalen a77 archivos. Países:2.792 carpetas,302 con inventario de autoridades. Se conserva la referencia contemporánea22/10/2026 y la imagen íntegra acreditada deMozambique. Los retratos identifican personas, no necesariamente su aspecto exacto en cada año.

Organizaciones:41 grupos/903 intervalos; TripleAlianza, PotenciasCentrales y Aliados/asociados añadidos a las38 organizaciones anteriores. Italia neutral1914 mantiene el tratado sin convertirse por ello en beligerante central; EEUU es asociado desde1917. Las observaciones de coalición son focales, no una lista exhaustiva de todos los beligerantes. PCA/ITU/UPU/OIT tienen registros institucionales, sin inventar membresías históricas desde listados actuales. Contexto:378 fases,97 registros de ficha y86 enlaces. Se separan firma, vigencia, proclamación y reconocimiento.

Auditoría1900–1919:3.167 entidades/año y15 controles/año; ninguna sin alguna autoridad resuelta o ausencia central documentada(Albania1917). Quedan66 personas/órganos sin fotografía(63humanos/3órganos) y165 casos anuales sin símbolo. Inventario nominal en REVIEW-1900-1919.json. No certifica todos los cargos, suplencias diarias, administradores locales ni fronteras. Faltan muchos frentes de laPrimeraGuerraMundial y guerra civil rusa, regencias, poderes regionales y símbolos. El CSV original sigue ausente.

Orden reproducible: adquisición aislada → curación focal → Europa/África → Américas → Asia → regiones → dependencias y suplementos → contexto → símbolos1900 → retratos por ventana → auditorías → register-1900-data → catálogoPaíses/inventario anual → integridad/tipos/pruebas/compilación/navegador. No volver a ejecutar preparadores iniciales destructivos. Fuentes, discrepancias y límites en RESEARCH-1900, AUTHORITIES-1900-* ySYMBOLS-1900. Registrar todo pendiente en tareas.md y no dar por finalizada una entrega tras una interrupción.

### Corrección adicional deAlemania1938–1939

Petición recibida después de integrar1900: manchas alemanas remotas y aspecto de parche enChecoslovaquia. Se confirma que el originalCliopatria1939 contiene187 componentes, incluidos numerosos cuadriláteros ajenos al teatro y atribución de parte deEslovaquia al controlador alemán. `central-europe.ts` normaliza únicamente1938/1939 antes de `composeControl`: componentes conectados con el ámbito documentado, vecinos protegidos por sus contornos fechados yAustria incorporada completa. No usar filtros globales por área; las islas reales se conservan en la base alemana. Los archivos originales no se modifican.

`central-europe-1939.geojson` aporta la extensión húngara anual y una referencia eslovaca deNaturalEarth, con procedencias separadas. Se recorta la referencia contraChecoslovaquia, el primer arbitraje deViena deCShapes y las incorporaciones alemanas1938; la ampliación húngara oriental no permite que el contorno grueso deCliopatria atribuyaBratislava aHungría. Alemania ocupaBohemia/Moravia como parte de su única entidad seleccionable. Eslovaquia tiene claveSVK-1939/SVW, color de cliente, bandera y autoridades propias; no estadísticas sucesoras. No queda una fichaCSK residual hecha de restos numéricos. Las franjas opcionales distinguen ocupación de incorporación.

La geometría eslovaca es una **referencia recortada**, no una frontera exacta de1939; faltan ajustes locales, la franja oriental de marzo y extensión de la corrección a1940–1944 con ocupación de1944. No se cambia silenciosamente toda la guerra. Fuentes, método, licencias y puntos en CENTRAL-EUROPE-1939. Preparar inputs y curación central después de los preparadores1900, adquirir símbolo/retrato focales, registrar manifiestos y regenerarPaíses. Los preparadores anteriores regenerables no deben borrar la corrección central: aplicarla después.

Validación local final:137 pruebas/31 archivos, tipos e integridad de44 datos/11 franjas/5.262 medios correctos. La compilación de producción se valida en la carpeta nueva `.cache/build-012-final-map` porque Windows bloqueó el vaciado de `dist/media`; no ocultar ese fallo ni servir el `dist` incompleto. El navegador usa exclusivamente el build nuevo con preview propio en5174 y `reuseExistingServer`. No se modifica CI por un bloqueo local. Resultados de navegador y envío efectivos en DELIVERY-0.12.0 y tareas.md.


## 24. Corrección0.12.1 · particiones1940–1944 y autoridades

El propietario confirma publicación0.12.0 y reproduce manchas alemanas enItalia, Suecia, Karelia yOrientePróximo durante1941–1944. La corrección previa sólo cubría1938–1939. Se verificaron los bytes públicos de manifiesto y ambas fuentes de controles: coincidían con0.12.0; no era una caché anterior.1880 se aplaza por instrucción expresa.

La nueva preparación exporta la base real de la aplicación y construye `wartime-partitions.json`: cinco sustituciones del inventario político, con identificadores a retirar, territorios finales y franjas ya recortadas a su controlador final. El cargador debe comprobar `controls.partition` ANTES del atajo de `features.length===0`; las entradas preparadas no contienen controles opacos que volver a componer. Mapa, clic y búsqueda utilizan las mismas entidades y geometrías. La carga compartida reutiliza el archivo; este tramo no hace booleanas geográficas en cada salto. Los recursos originales permanecen intactos.

CShapes aporta la malla terrestre fechada, Cliopatria cortes interiores y las referencias existentes los cortes eslovacos. El saneamiento elimina componentes remotos sin borrar globalmente islas, protege ámbitos neutrales por año, ajusta ocupaciones completas documentadas a la costa común y separaCroacia/Eslovaquia.China deja de duplicarse bajo su facción. Ningún control añade tierra fuera de la base. Las franjas opcionales son una lectura del inventario final; ocultarlas no recupera fronteras anteriores. Procedimiento, reglas editoriales, licencias, tolerancias y límites en [WWII-PARTITIONS](docs/WWII-PARTITIONS.md) y su auditoríaJSON. Nunca mezclar los frentes españolesBY-SA3.0 en este derivadoCShapesNC-SA.

Las fuentes anuales no acreditan un frente del31/12. Persisten fases pendientes1942–1944 —zonaVichy, liberaciones,RSI, partisanos— y la frontera eslovaca sigue siendo referencia recortada, no levantamiento municipal. La interfaz identifica1940–1944 como síntesis anual. Los controles fuera del tramo conservan límites anteriores; no anunciar un arreglo mundial de todos los conflictos.

Autoridades conserva siempre retrato/cargo/nombre/fechas y créditos. Las notas documentales extensas se consultan enContexto, dentro de un bloque inicialmente cerrado; cobertura y límites máximos siguen etiquetados junto al intervalo, sin presentarse como nombramientos o ceses. El encabezado y las pestañas permanecen fijos. El resolver suizo distingue por `authorityClass`/`office` la pertenencia alConsejoFederal y la presidencia anual, aun siendo la misma persona; da prioridad visual a esta última sin borrar el mandato colegiado.

Se recuperan34 retratos suizos(33GIF originales y1PNG),559.639bytes, con pareja exacta QID/título y permiso individual:HauserPD y33 declaracionesVRT/admin.ch contrastadas. No se autoriza globalmente la etiquetaCFU ni se convierten imágenes; se conservan bytes, créditos y huellas.194 etiquetas suizas se corrigen mediante identificadores de cargo, sin modificar fechas, otros países o fotografías previas. Esto no certifica todos los mandatos colegiados/presidencias; carencias precisas en tareas.md y [PORTRAITS-0.12.1-RESEARCH](docs/PORTRAITS-0.12.1-RESEARCH.md).

Preparación: export-wartime-inputs.ts → prepare-wartime-partitions.py → adquisición/curación suiza acotada → register-wartime-data.mjs → prepare-country-catalog.mjs → tipos/verificación/pruebas/compilación/navegador. El manifiesto fija las huellas de los cuatro insumos y el verificador rechaza una preparación obsoleta. CatálogoPaíses incluye referencias anuales sin duplicar geometría y preserva extensiones manuales. Versión de referencia contemporánea22/10/2026 sin cambio. Comprobaciones finales y estado de subida se registran en DELIVERY-0.12.1 y tareas.md; no confundir build local con publicación.


La prueba de navegador0.12.1 detectó un hueco no cubierto por la revisión geométrica: SVK-1939 sólo tenía autoridades/símbolo1939. Se incorporó continuidad documental1940–1944 con fuentesUSHMM/UPN y sucesiónTuka/ŠtefanTiso5/9/1944, retrato adicional y extremos de cobertura explícitos. Curador puro/idempotente, declaraciones1939 y fotos previas conservadas. SóloCHE ySVK-1939 difieren del inventario0.12.0; total302 claves/10.246 mandatos y5.297 medios(499SVG/4.798 fotografías).147 pruebas/33 archivos correctos tras esta corrección. La ficha eslovaca previamente abierta1943→1944 permanece aunque el controlador alemán sustituya su geometría independiente. No reintroducir una ficha territorial activa para satisfacer una búsqueda de1944.


Cierre local0.12.1:147 pruebas/33 archivos y siete recorridos distintos de navegador correctos; tipos, compilación,45 datos/11 franjas/5.297 medios íntegros y5.353 recursos preparados enGit comprobados. Se revisaron capturas deEuropa1942. Se corrigieron el hueco eslovaco descubierto en navegador y una expectativa de búsqueda incompatible con su ocupación1944, conservando la ficha desde1943. Detalle en DELIVERY-0.12.1. Tras confirmar el push, terminar sin sondear Actions/Pages; la revisión pública depende del aviso del propietario.
