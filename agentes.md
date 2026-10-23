# Historicmap · Manual de continuidad del proyecto

Documento canónico para colaboradores humanos y asistentes de cualquier proveedor. Su propósito es permitir continuar el trabajo sin depender de una conversación previa. Fecha inicial: **21 de octubre de 2026**. Última actualización: **23 de octubre de 2026**. Versión del producto: **0.8.1**.

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

Validación final y publicación se registran en DELIVERY-0.8.1 cuando se hayan ejecutado. Las pruebas cubren el motor de teselas, clics reales ida/vuelta, recorte de administración, gobiernos autónomos, ausencia de extrapolación y persistencia de fichas al independizarse. El año1954 es una reproducción del error estructural, no una ampliación de la tanda bibliográfica anterior a1970.
