# Historicmap · Manual de continuidad del proyecto

Documento canónico para colaboradores humanos y asistentes de cualquier proveedor. Su propósito es permitir continuar el trabajo sin depender de una conversación previa. Fecha inicial: **21 de octubre de 2026**. Última actualización: **22 de octubre de 2026**. Versión del producto: **0.3.0**.

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

## 3. Estado real de la versión 0.3.0

### Implementado

- Aplicación estática TypeScript/Vite/MapLibre con mapa Mercator y globo, worker local explícito, búsqueda y selección. No hay backend, cuentas, claves privadas, analítica ni SQLite.
- Se conserva el diseño compacto 0.2: herramientas superiores, capas desplegables, contexto izquierdo, regla desplazable con cursor fijo y zoom temporal independiente. No restaurar franjas o controles retirados.
- Año máximo obtenido mediante `new Date().getFullYear()`; no confundir extremo dinámico con conocimiento de fronteras futuras. La referencia contemporánea se incorporó en 2026.
- **1900–2019**: periodos activos de CShapes 2.0, edición GW **con dependencias** del paquete R. 640 registros relevantes, conservando coordenadas, estatus, administrador, capital y fechas inclusivas. Se selecciona el **31 de diciembre** de cada año. El GeoJSON directo de ETH pierde propiedades de administración; no sustituir por él la fuente del paquete R.
- Colores políticos por potencia administradora: las colonias mantienen ficha y entidad propias, compartiendo color con su administrador. Nombres contextuales de imperio ruso/URSS/Rusia, Alemania nazi, zonas de ocupación de 1945 y RFA/RDA desde 1949.
- **1938–1944**: 20 registros Cliopatria de Alemania, Japón e Italia, superpuestos como extensión territorial/ocupación. La fuente proporciona síntesis anual sin día uniforme; no denominarla frente exacto de fin de año. 1942 ya no utiliza 1945.
- Ocupaciones/disputas: cinco registros de Crimea desde 2014, Sinaí 1956, Sinaí 1967–1978, zona de retirada parcial 1979–1981 y Golán desde 1967. Geometrías derivadas por diferencias entre registros CShapes. Desde 1967 la base de Egipto/Israel/Siria utiliza sus geometrías de 1966 para no equiparar ocupación a incorporación soberana. Las notas explican alcance y excepciones.
- **2020–año del dispositivo**: referencia contemporánea Natural Earth 1:10m, 258 entidades; NO instantáneas históricas independientes por año. Se identifica el año de incorporación (2026), sin atribuir vigencia diaria. Las geometrías base de Natural Earth no han cambiado.
- Fichas ampliadas, iguales al pulsar y buscar: capital/sede, estatus histórico, potencia administradora, registro temporal, contexto focal y datos económicos/demográficos cuando existe correspondencia fiable. Estados Unidos actual incluye información federal y hasta seis indicadores.
- Banco Mundial WDI local: población, PIB nominal, PIB por habitante, superficie, esperanza de vida y porcentaje urbano, desde 1960. Última observación no posterior al año consultado, retraso máximo cinco años, año mostrado por cifra. Sin extrapolar, ni confundir URSS/Yugoslavia/RDA con estadísticas actuales de sucesores. Las series son de economías publicadas, no de una integración espacial recalculada sobre fronteras pasadas.
- Capas temáticas de PIB, PIB por habitante y población, con leyenda de fechas realmente presentes y gris para ausencia. Antes de 1960 se restablece el color político; no quedan mapas grises por una selección económica heredada.
- 323 capitales y grandes ciudades contemporáneas, de Natural Earth. POP_MAX sólo filtra/ordena, no se publica como población urbana fechada. Para 1900–2019, capitales del registro CShapes; para épocas anteriores se conservan los tres lugares introductorios. No llevar capitales modernas al pasado.
- Conservadas las 13 instantáneas Historical Basemaps y 12 CAO2024 originales. Los años posteriores a 1900 de la colección antigua dejan de elegirse en navegación normal. Antes de 1900 se mantiene selección aproximada; geología y escenas sin cartografía siguen señaladas.
- Reproducción reciente anual: espera descarga/aplicación antes de avanzar, pausa invalida la continuación y se conserva la geometría anterior mientras carga, con indicador explícito. Las solicitudes comparten caché y descargas en curso; una cola y contador descartan fechas obsoletas. No cancelar/repetir un archivo temporal durante cada paso.
- La caché conserva el archivo temporal/perfiles/ciudades/capas y limita a tres las instantáneas antiguas/geológicas retenidas. Las geometrías temporales se decodifican/reutilizan por fid. No se reenvía la fuente territorial si su firma no cambia. La URL se actualiza como máximo cuatro veces por segundo.
- 31 recursos en el manifiesto, con versiones, transformaciones, licencias y SHA-256. Archivos de origen R/zip con huellas verificadas. CShapes y derivados **CC BY-NC-SA 4.0**, Cliopatria **CC BY 4.0**, WDI **CC BY 4.0 con términos adicionales**, recursos originales conservan sus licencias; no atribuir automáticamente estas licencias al código del propietario.
- `docs/ANNUAL-REVIEW.md`: inventario de cada año 1900–actualidad, cambios de registros, fuentes, huellas y excepciones. Auditoría automática de cobertura/identidad + contrastes focales; **no revisión manual exhaustiva de todas las coordenadas de 127 mapas**.
- Relieve actual opcional de AWS Terrarium, desactivado en el pasado; no reconstruye altitudes antiguas. Diseño móvil, teclado, foco, diálogos y enlaces compartibles.
- «Acerca de» mantiene favicon, versión procedente de package.json, historial y enlaces confirmados a repositorio y portfolio: https://alejandropico.github.io/Portfolio/ .
- GitHub Actions valida e instala la aplicación; Pages publica sólo tras Quality correcto de main. Estado final de esta entrega en `docs/DELIVERY-0.3.0.md`.

### Límites y trabajo restante

- **No afirmar exactitud política exhaustiva 1900–2026.** CShapes omite cambios menores de 10.000 km², algunas ocupaciones temporales, Estados pequeños y límites inciertos; fechas convencionales en algunos registros. 2020–actualidad mantiene una base contemporánea, sin serie global de control efectivo verificada.
- Faltan frentes diarios de ambas guerras mundiales, delimitación completa de administraciones de ocupación, partición germano-soviética de Polonia de 1939, frentes del Donbás y de la invasión de Ucrania desde 2022, control militar reciente mundial, fases geométricas de retirada del Sinaí y Taba (1982–1989). Los polígonos de extensión de Cliopatria no sustituyen una cartografía militar detallada.
- Crimea se explica como territorio ucraniano bajo ocupación y anexión reclamada por Rusia desde 2014 conforme al contexto de A/RES/68/262, nunca como transferencia de soberanía reconocida por esa resolución. El contorno discontinuo no actualiza los demás frentes. El Golán no lleva una reconstrucción de cambios de control desde 2024.
- La base de 1966 para Egipto/Israel/Siria separa ocupación de incorporación, pero no resuelve por sí sola todas las controversias de soberanía, líneas de armisticio, Jerusalén, Gaza y Cisjordania. No denominarla atlas jurídico exhaustivo.
- Natural Earth 1:10m es generalización mundial; el objetivo de máxima resolución costera sigue pendiente. La teselación de 0,2 píxeles evita desbordes GPU y no modifica las coordenadas base. No aumentar la generalización para ocultar un problema.
- No hay fronteras históricas continuas antes de 1900; las instantáneas antiguas pueden ser aproximadas/anacrónicas y no están auditadas exhaustivamente.
- CAO2024 representa reconstrucciones continentales, no paleocostas exactas ni biomas, clima, atmósfera, nivel del mar o relieve. Antes de 1.800 Ma y entre 1 Ma y 10.000 a. C. se sigue indicando falta de geometría y escena conceptual/contexto.
- No se implementan áreas de homininos, migraciones, glaciaciones, animación de Theia/formación lunar, vida, batallas o simulaciones físicas. No trasladar estas aspiraciones a funciones completadas.
- Relieve y fuentes tipográficas de interfaz requieren conexión. Las letras del mapa utilizadas se alojan localmente, 11 franjas Noto Sans PBF con licencia OFL y huellas en public/fonts/manifest.json. No PWA ni garantía offline completa. Las fichas/series y geometrías nuevas son locales, sin llamadas al Banco Mundial durante la visita.

## 4. Tecnologías y estructura

Versiones adoptadas el 21/10/2026, contrastadas con registros oficiales: Node.js **26.12.1**, TypeScript **7.0.2**, Vite **8.3.5**, MapLibre GL JS **6.15.0**, Lucide **1.61.0**, Vitest **5.0.5**, Playwright **1.64.1**. `package-lock.json` es la referencia exacta, incluidas dependencias transitivas. El equipo inicial tenía Node 24; se utilizó un ejecutable portátil oficial Node 26 en `.tools/`, ignorado por Git. No subirlo ni modificar instalaciones del usuario.

```text
src/main.ts                interfaz, mapa, interacción y estado de aplicación
src/about.ts               identidad, ficha del proyecto e historial visible
src/time.ts                cronología, año del dispositivo y selección por dominio
src/history.ts             periodos, identidades, dependencias, geometrías y capitales
src/data.ts                caché compartida, carga temporal y capas
src/profiles.ts            observaciones fechadas, temas, formato y leyenda
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

### 0.3 · Datos recientes y reproducción — implementada con límites

Entrega priorizada por solicitud del propietario: intervalos territoriales 1900–2019, revisión anual de cobertura hasta el año del dispositivo, capas de guerra/ocupaciones, fichas, ciudades e indicadores. Los límites de la sección 3 siguen abiertos. La fase anterior de máxima resolución se desplaza, sin considerarla realizada.

### Próxima fase · Calidad cartográfica contemporánea

- Evaluar teselas vectoriales abiertas de alta resolución, costa detallada y actualización reproducible, por ejemplo con un paquete PMTiles propio o proveedor documentado.
- Resolver nombres, etiquetas, detalles costeros, lagos, ríos, países pequeños, antimeridiano y polos, con generalización dependiente del zoom y pruebas geográficas.
- Modelar fronteras disputadas y fecha de vigencia, sin una falsa etiqueta universal de «exactitud».
- Mejorar materiales de superficie y relieve, iluminación, batimetría y transiciones, manteniendo legibilidad política y rendimiento.
- Módulos separados para motor cartográfico, aplicación de capas, UI, cronología y repositorios de datos; el archivo inicial `main.ts` es deliberadamente compacto y debe separarse antes de ampliarlo mucho.

### 0.4 · Historia política verificable

- Extender los contrastes focales 0.3 a una revisión historiográfica por regiones y conflictos; completar 2020–actualidad y corregir las excepciones del informe anual. Incorporar fuentes de mayor detalle donde CShapes omite cambios.
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

La entrega comprueba los 31 recursos y sus huellas, invariantes temporales y año dinámico, selección de cada año 1900–2019, ausencia de identidades duplicadas, Alemania anterior/posterior a 1945/1949, dependencia/independencia de India y Argelia, Egipto/Siria/Israel, activación de Crimea, ciudades, capitales y ausencia de estadísticas futuras. En navegador se comprueban todos los años 1900–actualidad, reproducción/pausa, peticiones lentas y fechas obsoletas, fichas, economía, móvil, cartografía antigua/geológica, GPU y controles compactos. Registrar resultados finales reales en `docs/DELIVERY-0.3.0.md`, sin dar por superado un test que sólo se ha escrito.

Para reconstruir datos: consultar `docs/SOURCES.md`, `scripts/acquire-history.py`, `scripts/fetch-modern.mjs`, `scripts/prepare-history.py` y `scripts/build-review.mjs`. Shapely 2.2.0 es herramienta de preparación, no dependencia del navegador. `.cache/` y `.tools/` son locales ignorados. `npm run data:audit` regenera el inventario hasta el año del sistema; `data:verify` no certifica exactitud histórica.

Siguiente prioridad: **completar excepciones históricas y control efectivo reciente, con mejores fuentes**, y avanzar después en costa contemporánea de alta resolución. No ampliar indiscriminadamente la cronología sin resolver errores concretos. Conservar la distinción entre ambición, cobertura de fuente, contraste focal y validación exhaustiva.

La actualización incremental de fuentes se implementa en source-diff.ts y se comprueba con pruebas de diferencias; sólo se envían entidades modificadas al worker. Las pruebas de navegador usan la compilación de producción en el puerto 5174, con un único worker para no saturar el renderizado por software; compilar antes de ejecutarlas.
