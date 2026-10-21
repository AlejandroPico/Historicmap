# Historicmap · Manual de continuidad del proyecto

Documento canónico para colaboradores humanos y asistentes de cualquier proveedor. Su propósito es permitir continuar el trabajo sin depender de una conversación previa. Fecha inicial: **21 de octubre de 2026**. Última actualización: **22 de octubre de 2026**. Versión del producto: **0.2.0**.

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

## 3. Estado real de la versión 0.2.0

### Implementado

- Aplicación web estática con TypeScript estricto y Vite; sin cuentas, backend ni claves privadas.
- MapLibre GL JS 6.15.0: proyección Mercator en 2D y globo en 3D. Cambio de proyección conserva la época.
- Países y territorios de Natural Earth Admin 0 1:10m: 258 entidades, que **no equivalen a 258 Estados soberanos**. Las coordenadas originales se conservan; se seleccionan propiedades y se añaden identificadores y colores. MapLibre realiza teselación y recorte para renderizar.
- 13 instantáneas de Historical Basemaps: −10000, −3000, −1000, −500, 100, 500, 1000, 1492, 1800, 1914, 1945, 1994 y 2010.
- 12 reconstrucciones GPlates CAO2024 a 1, 20, 66, 100, 200, 300, 400, 541, 750, 1000, 1500 y 1800 Ma.
- Total: 26 archivos GeoJSON locales; unos 50 MiB sin comprimir. Carga diferida de una instantánea cada vez.
- Clasificación visual por territorios con paleta discreta; líneas de límites, selección resaltada y etiquetas desde determinado nivel de zoom.
- Relieve mediante hillshade Terrarium de Mapzen/AWS para el presente. No reconstruye altitudes pasadas. Se desactiva en épocas históricas y geológicas.
- Tres marcadores introductorios con intervalos temporales: Uruk, Roma y Çatalhöyük. No es un catálogo de ciudades completo.
- Cronología por tramos lineales de escala adaptativa, 20 anclas de densidad deliberadamente desigual. Arrastre por puntero/táctil y flechas para desplazamiento; rueda o teclas más/menos para zoom temporal manteniendo fecha y cursor. Inicio/fin, saltos y reproducción. Marcas con intervalos legibles según el zoom, generadas sólo para el área visible y su margen. La escala va de 96 a 4800 píxeles por intervalo de anclas.
- Introducción de año concreto. No se utiliza año cero civil. Ma/Ga se muestran como antigüedades aproximadas; no son fechas con precisión anual.
- Fecha consultada separada de la instantánea seleccionada. Se utiliza la instantánea más cercana **dentro del dominio correspondiente**; no se inventan estados intermedios.
- Buscador local de nombres del archivo cargado. La cartografía contemporánea utiliza nombres españoles cuando existen; el pasado conserva nombres originales.
- Herramientas superiores compactas; cambio de proyección en un único botón con icono y nombre accesible de la acción siguiente. Capas en panel desplegable, cierre con Escape, pulsación exterior o su botón de cierre.
- Fuentes y metodología accesibles desde el icono de base de datos superior. Contexto por época a la izquierda, sin las capas ni fecha duplicada.
- «Acerca de» rediseñado con favicon, identidad, ficha de versión, instrucciones del atlas e historial. Versión obtenida de `package.json` para evitar discrepancias.
- Portfolio confirmado: https://alejandropico.github.io/Portfolio/ . Recuperado de los proyectos de referencia del autor y comprobado HTTP 200 el 22/10/2026. Enlazado junto al repositorio del proyecto.
- Estado compartible en fragmento URL `#year=100&view=globe`, pantalla completa cuando el navegador la admite, adaptación a móvil, foco visible, diálogo nativo, teclado y preferencia de movimiento reducido.
- Importador de datos con reintentos, validación de procedencia y SHA-256; datos distribuidos localmente para no depender de GPlates en cada visita.
- GitHub Actions: validación, pruebas, compilación y publicación en GitHub Pages tras superar calidad.

### Ausencias y límites que deben seguir visibles

- No hay continuidad histórica anual, mensual ni diaria. No presentar la cercanía de una instantánea como exactitud para la fecha solicitada. Un año 2025 utiliza la instantánea 2010 y lo indica; 2026 utiliza la referencia contemporánea Natural Earth, que tampoco certifica vigencia diaria.
- Natural Earth 1:10m es cartografía generalizada para escala mundial. **La exigencia final de máxima definición costera todavía no está satisfecha.** Limitar zoom inicial a 7 evita sugerir detalle de calle. La próxima mejora debe incorporar teselas vectoriales de mayor resolución y gestionar generalización, licencias y actualización.
- Las fuentes históricas contienen áreas culturales, aproximaciones y posibles errores/anacronismos. No están revisadas de forma exhaustiva por Historicmap.
- GPlates reconstruye posiciones de geometrías continentales; no demuestra la costa inundada exacta, el relieve, color, bioma ni clima de esa fecha. El modelo debe citarse siempre.
- Antes de 1.800 Ma se muestra un efecto esférico conceptual sin continentes inventados. La Tierra primitiva no fue necesariamente un océano de lava continuo durante todo el Hádico o Arcaico: el efecto no debe interpretarse así.
- Entre 1 Ma y 10.000 a. C. se muestra ausencia de cartografía, con contexto documental. Aún no hay reconstrucciones de paleocostas recientes ni capas de hielo.
- El catálogo menciona el origen humano, pero **no representa áreas, fósiles o rutas de homininos**. No tratar «pendiente» como «implementado».
- No hay animación del impacto de Theia, simulación física, formación lunar, atmósferas, evolución oceánica, líquidos alternativos, vida, extinciones visualizadas, batallas o guerras. Theia es un cuerpo hipotético de la hipótesis dominante del gran impacto; no un hecho observado y totalmente determinado.
- El relieve y las fuentes/etiquetas externas necesitan conexión. No hay service worker, instalación PWA ni garantía de modo offline completo.
- No hay datos persistidos del usuario, ni SQLite, ni API, ni analítica.
- El zoom del mapa se controla mediante sus gestos nativos; la rueda en la regla nunca lo modifica. Las escenas conceptuales son ilustraciones sin navegación cartográfica.

## 4. Tecnologías y estructura

Versiones adoptadas el 21/10/2026, contrastadas con registros oficiales: Node.js **26.12.1**, TypeScript **7.0.2**, Vite **8.3.5**, MapLibre GL JS **6.15.0**, Lucide **1.61.0**, Vitest **5.0.5**, Playwright **1.64.1**. `package-lock.json` es la referencia exacta, incluidas dependencias transitivas. El equipo inicial tenía Node 24; se utilizó un ejecutable portátil oficial Node 26 en `.tools/`, ignorado por Git. No subirlo ni modificar instalaciones del usuario.

```text
src/main.ts                interfaz, mapa, interacción y estado de aplicación
src/about.ts               identidad, ficha del proyecto e historial visible
src/time.ts                cronología pura y elección de instantánea
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

La interfaz utiliza una base oscura azul verdosa, acento dorado, tipografía sans para controles y serif para fechas/contexto. El mapa ocupa toda la pantalla. El contexto se superpone a la izquierda, las seis herramientas flotan arriba a la derecha y la regla se superpone al pie sin franjas adicionales. El punto fijo central integra fecha, reproducción y saltos; la etiqueta «Escala adaptativa» se mantiene discretamente a la derecha. No degradar la cartografía por comodidad estética. Mantener contraste, foco y accesibilidad.

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

### 0.3 · Calidad cartográfica contemporánea

- Evaluar teselas vectoriales abiertas de alta resolución, costa detallada y actualización reproducible, por ejemplo con un paquete PMTiles propio o proveedor documentado.
- Resolver nombres, etiquetas, detalles costeros, lagos, ríos, países pequeños, antimeridiano y polos, con generalización dependiente del zoom y pruebas geográficas.
- Modelar fronteras disputadas y fecha de vigencia, sin una falsa etiqueta universal de «exactitud».
- Mejorar materiales de superficie y relieve, iluminación, batimetría y transiciones, manteniendo legibilidad política y rendimiento.
- Módulos separados para motor cartográfico, aplicación de capas, UI, cronología y repositorios de datos; el archivo inicial `main.ts` es deliberadamente compacto y debe separarse antes de ampliarlo mucho.

### 0.4 · Historia política verificable

- Auditoría de las 13 instantáneas actuales; incorporar un segundo conjunto con cobertura y licencia verificadas, comenzando por regiones/periodos acotados.
- Modelo de entidades persistentes con nombres e identidades históricas, relaciones de dependencia y periodos de validez.
- Cambios fechados de fronteras, ciudades, capitales, redes comerciales y primeros Estados. Trabajar por entregas geográficas revisadas, no prometer todos los años de todo el planeta de una vez.
- Fichas de entidad con bibliografía, precisión y alternativas, comparación entre fechas y búsqueda en español.

### 0.5 · Prehistoria y evolución humana

- Catálogo de yacimientos y fósiles con evidencia primaria; especies, rangos temporales inciertos y ocupación documentada.
- Homo sapiens, neandertales, denisovanos, Homo erectus, Homo floresiensis y otros taxones cuando los datos lo permitan. No homogeneizar «homininos» con «humanos modernos».
- Migraciones como hipótesis con rutas/áreas de incertidumbre y fechas, nunca como trayectorias GPS exactas.
- Paleocostas, cambios del nivel del mar y extensión de hielo para el Cuaternario.

### 0.6 · Tierra profunda, clima y vida

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

La compilación no necesita credenciales ni acceso a las fuentes científicas: los GeoJSON se guardan en Git. `data:fetch` sí consulta fuentes, fija sus commits actuales cuando son repositorios, solicita explícitamente CAO2024 y actualiza el manifiesto. El servicio puede cambiar resultados del mismo nombre de modelo: las huellas del snapshot importado permiten detectar cambios.

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

## 10. Validación y relevo

Las comprobaciones incluyen integridad SHA-256 de las 26 instantáneas, seis pruebas de cronología, compilación TypeScript/Vite y cuatro recorridos de navegador: búsqueda/selección/proyecciones/reproducción; cursor fijo/fecha exacta/móvil/diálogos; renderizado de las 26 instantáneas sin exceso de vértices GPU; y herramientas compactas/zoom independiente de regla y mapa/capas/fuentes. El recorrido de todas las instantáneas usa la vista plana para incluir masas continentales que, en el globo, quedarían en el hemisferio opuesto. Se esperan polígonos renderizados, no sólo un canvas presente. El informe inicial está en `docs/DELIVERY.md`; el del rediseño se registra en `docs/DELIVERY-0.2.0.md`.

Siguiente trabajo recomendado: **alta resolución contemporánea y auditoría de datos históricos**, antes de añadir grandes cantidades de contenido. Mantener explícita la distinción entre la ambición del producto y su cobertura comprobada.
