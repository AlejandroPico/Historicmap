# Enciclopedia de Historicmap · Plan de proyecto

Documento rector de la reconstrucción completa de «la enciclopedia». Redactado en la fase **P00** (7 de noviembre de 2026, sobre la versión 0.56.0, commit `8004e266f`). Cada fase se ejecuta solo cuando el propietario la ordena («empieza la P0X»). Al cerrar cada fase se actualizan este plan, `tareas.md`, `agentes.md` y `CHANGELOG.md`, y se entregan los comandos de Git para que el propietario suba el resultado.

---

## 1. Diagnóstico de partida (P00)

### Lo que existe hoy

| Pieza | Estado |
|---|---|
| Lector | `src/encyclopedia.ts` (13 KB), `encyclopedia-model.ts`, `human-encyclopedia.ts`, `encyclopedia-diagrams.ts`, `encyclopedia.css`. Diálogo a pantalla completa, búsqueda local, historial, «Ver en el mapa», carga diferida (chunk de 167 KB). |
| Contenido | 291 entradas: 91 artículos (21 Precámbrico, 20 Fanerozoico, 1 Cuaternario, 49 de humanidad), 177 unidades geológicas ICS y 23 edades humanas. En total unos **77 KB de texto** de artículos geológicos: el artículo «Jurásico» tiene 4 párrafos y no menciona sus tres series ni sus once edades. |
| Unidades geológicas | Las 177 unidades (4 eones, 10 eras, 22 periodos, 37 épocas, 101 edades) solo muestran una plantilla genérica («X se consulta para…») sin contenido propio. |
| Historia | **Nada**. No existe ninguna página de contexto mundial, entidad política, dirigente, guerra, pandemia ni monumento. |
| Datos aprovechables | 5.290 expedientes en `Países/` (3.995 entidades políticas, 503 culturas, 792 yacimientos) y **12.606 dirigentes distintos**, el 97 % con identificador Wikidata (QID). Distribución: 10 antes de 2500 a.C., ~1.400 en la Antigüedad, ~2.600 entre 500 y 1500, ~6.000 entre 1500 y 2000. |
| Estilo | Texto burocrático y defensivo («no certifica», «no equivale a», «referencia editorial»). Los avisos metodológicos se comen el contenido. |

### Hallazgos colaterales

- **Clon roto en Windows**: 21 rutas de `Países/` superan los 260 caracteres de Windows (la más larga mide 244 + `D:\Proyectos\Historicmap\`). La descarga fue completa, pero el checkout se abortó y el índice de Git quedó vacío; por eso `git status` muestra los 40.404 archivos como «borrados». Solución en el apartado 6.
- **Carpeta duplicada**: `EGYPT-HERACLEOPOLITAN-POWERS-…-nort` y `…-norte` coexisten (la primera es un nombre truncado). Pendiente de revisar con los datos de países; no se toca en la enciclopedia.
- **Idiomas**: la aplicación solo está en español. La arquitectura nueva admite traducciones por archivo, pero traducir una enciclopedia de este tamaño a 7–12 idiomas es una decisión aparte (fase opcional P-X2).
- **Despliegue**: la compilación pura (`vite build`) tarda unos 3 s; lo lento es la batería de navegador (8 grupos + barrido anual). La enciclopedia nueva solo añadirá **pruebas unitarias rápidas** (Vitest) y como mucho un recorrido de navegador, para no alargar Actions.

---

## 2. Visión

Historicmap tiene dos caras: la **sencilla** (moverse en el tiempo, pulsar un país y ver quién mandaba) y la **técnica**, que es la enciclopedia. La enciclopedia debe ser:

1. **Monumental y rigurosa**: cantidad sin perder calidad, sin repetir contenido entre páginas (se enlaza en vez de repetir).
2. **Autocompositiva**: una unidad superior se lee como un documento que **incluye a sus hijas**. «Jurásico» = introducción propia + Jurásico Inferior (Hettangiense, Sinemuriense, Pliensbachiense, Toarciense) + Medio + Superior (Oxfordiense… Titoniense). «Titoniense» se lee solo. Lo mismo para eras, eones, imperios con sus dinastías, guerras con sus batallas.
3. **Contextual por fecha**: al abrirla desde el mapa en el año X se muestra **«El mundo en X»**: panorama global y por regiones (continentes, culturas, imperios), unidad geológica vigente, eventos del año y dirigentes activos. La granularidad se adapta: miles de millones de años en el Hádico, milenios en el Paleolítico, siglos/décadas en la Antigüedad, años en la Edad Contemporánea.
4. **Hipervinculada**: todo nombre propio relevante enlaza (personas, entidades, eventos, eras, especies, conceptos). Enlaces que viajan por el tiempo; historial adelante/atrás.
5. **Visual**: gráficos (temperatura, CO₂, O₂, nivel del mar, biodiversidad, población), líneas de tiempo interactivas, esquemas SVG propios, tablas comparativas, fotografías y reconstrucciones con licencia y crédito.
6. **Conectada al mapa**: la regla cronológica (nombres de eras clicables), las fichas de país (icono «consultar» junto a cada dirigente), las manchas de homininos y culturas, y los yacimientos abren su página.
7. **Escrita con voz enciclopédica**: clara y técnica; la incertidumbre se explica una vez, donde importa (apartado «Evidencias y debate»), no en cada frase.

---

## 3. Arquitectura propuesta

### Carpeta raíz `enciclopedia/`

```text
enciclopedia/
  PLAN.md                 este documento
  README.md               guía editorial y de formato (P01)
  esquema/                tipos de página, campos obligatorios, validador
  geologia/               eones, eras, periodos, épocas y edades (177 unidades ICS + informales)
  tierra/                 formación, atmósfera, océanos, tectónica, supercontinentes, impactos
  clima/                  glaciaciones (todas), invernaderos, eventos hipertermales
  vida/                   origen y evolución de la vida, extinciones, bestiario (dinosaurios, megafauna…)
  humanidad/              homininos, migraciones, yacimientos clave, tecnologías prehistóricas
  culturas/               culturas y comunidades prehistóricas y protohistóricas (las 503 de Países/)
  contextos/              «El mundo en…»: panoramas por intervalo, con desglose regional
  entidades/              imperios, reinos, repúblicas, estados (vinculados a las claves de Países/)
  personas/               biografías, nombradas por QID de Wikidata (Q1407-tiberio.md)
  eventos/                guerras, batallas, revoluciones, pandemias, tratados, hitos (Luna 1969…)
  obras/                  monumentos y grandes obras (pirámides, Gran Muralla…)
  temas/                  conceptos transversales (religiones, escritura, imprenta, metalurgia…)
  medios/                 imágenes con ficha de licencia, autor y fuente
  _generado/              índice, búsqueda y relaciones compilados (no se edita a mano)
```

### Formato de una página

Markdown con cabecera YAML, para poder escribir textos largos con comodidad:

```markdown
---
id: persona/Q1407
tipo: persona
titulo: Tiberio
alias: [Tiberio Julio César Augusto]
fechas: { inicio: -42-11-16, fin: 37-03-16 }
anclaMapa: 33            # año que abre «Ver en el mapa»
entidades: [ROMAN-EMPIRE-CLASSICAL]
padre: null              # o la unidad/entidad que lo contiene (composición)
relacionados: [persona/Q1405, entidad/ROMAN-EMPIRE-CLASSICAL]
fuentes: [wp-es-tiberio, suetonio-vidas]
infobox: { ... }         # datos de la ficha lateral
---
## Infancia y familia
Texto con enlaces internos: [[persona/Q1405|Augusto]], [[evento/batalla-teutoburgo]].
```

- Un compilador (`scripts/build-encyclopedia.mjs`, Node puro, sin dependencias nuevas) valida las páginas, resuelve enlaces, detecta enlaces rotos y genera `_generado/` (índice, búsqueda, árbol de composición, índice temporal). Se ejecuta antes de `vite build` y tarda segundos.
- Cada página se carga **bajo demanda** (fragmento propio). El peso del programa principal no crece aunque la enciclopedia ocupe decenas de MB.
- Lo ya existente en `Tierra/` (ICS, curvas PhanDA, CO₂, LR04, linajes, fotos) se **reutiliza por referencia**, sin duplicar datos científicos.
- Los dirigentes de `Países/` se enlazan por QID: si existe `personas/Q….md` se abre la biografía; si no, una **ficha mínima generada** con lo que ya sabemos (cargos, fechas, entidad, retrato) y la marca «biografía en preparación».

### Niveles de profundidad

| Nivel | Qué es | Volumen orientativo |
|---|---|---|
| **A · Monografía** | Página extensa escrita a mano, con gráficos, imágenes y esquemas | 600–900 páginas |
| **B · Artículo** | Página completa pero más breve (3–8 apartados) | 2.500–4.000 páginas |
| **C · Ficha generada** | Datos estructurados + resumen breve, a partir de Wikidata/Wikipedia y los propios datos | el resto de los 12.606 dirigentes y entidades |

### Fuentes, licencias y estilo

- Wikipedia (es/en) como base principal, contrastada con fuentes especializadas (ICS, USGS, NASA, Smithsonian, Britannica, artículos científicos). Los textos se **redactan de nuevo**, no se copian; se citan las fuentes en cada página.
- Imágenes solo de Wikimedia Commons u otras fuentes con licencia libre verificada, con autor, licencia y URL registrados (como ya se hace con los retratos).
- Sin repetir: una idea vive en una sola página; las demás enlazan.

---

## 4. Fases

Cada fase indica objetivo, entregables y criterio de cierre. Las fases de contenido incluyen siempre: texto, enlaces internos, gráficos/esquemas, imágenes cuando existan, fuentes y pruebas del compilador.

### Bloque 0 · Cimientos

**P00 · Análisis, diagnóstico y plan** ✅ *(esta entrega)*
Descarga y diagnóstico del clon, lectura de `agentes.md`, `tareas.md`, código y datos, prueba de compilación, capturas de la enciclopedia actual y este plan.

**P01 · Arquitectura y lector nuevo**
Carpeta `enciclopedia/` con esquema y guía editorial; compilador con validación y detección de enlaces rotos; lector nuevo: índice lateral por ramas (Tierra, Vida, Humanidad, Historia, Personas, Eventos), ficha lateral (infobox), tabla de contenidos, **composición jerárquica** con secciones plegables (“leer completo” incluye a las hijas), historial, búsqueda con acentos y alias, apertura por fecha. Migración de lo aprovechable de los 91 artículos actuales (quitando la retórica defensiva). Pruebas unitarias rápidas. Instrucciones para ejecutar en local.
*Cierre:* el lector nuevo abre las páginas migradas, compone una unidad con sus hijas y no aumenta el tiempo de Actions de forma apreciable.

**P02 · Componentes visuales e integración con el mapa**
Biblioteca de componentes: gráficos de series (temperatura, CO₂, O₂, nivel del mar, biodiversidad, población), línea de tiempo interactiva, mapa en miniatura de localización, esquemas SVG reutilizables, tablas comparativas, galerías con créditos, árboles genealógicos y de sucesión. Puntos de entrada: nombres de la regla cronológica, icono «consultar en la enciclopedia» junto a cada dirigente y entidad en las fichas, manchas de homininos, culturas y yacimientos. Canal de medios de Commons con licencias.
*Cierre:* desde cualquier dirigente, era o cultura del mapa se llega a su página (real o ficha generada).

### Bloque 1 · La Tierra antes de la vida compleja

**P03 · Formación de la Tierra, Hádico y Arcaico**
Nebulosa solar, acreción, Theia y la Luna, océano de magma, primeras aguas y circones de Jack Hills, Bombardeo Intenso Tardío, Eoarcaico→Neoarcaico, cratones, primeras evidencias de vida (LUCA, estromatolitos), atmósfera reductora, día de pocas horas.
*Volumen:* ~35 páginas (A/B).

**P04 · Proterozoico**
Paleo-, Meso- y Neoproterozoico con todos sus periodos (Sideriano → Ediacárico); Gran Oxigenación; formaciones de hierro bandeado y océanos ferruginosos/«rojos»; glaciación Huroniana; «mil millones aburridos»; eucariotas; Columbia y Rodinia; Tierra bola de nieve (Esturtiana, Marinoana, Gaskiers); biota de Ediacara.
*Volumen:* ~35 páginas.

### Bloque 2 · Fanerozoico, unidad por unidad

**P05 · Paleozoico**: Cámbrico → Pérmico con todas sus épocas y edades (~50 unidades ICS): explosión cámbrica, Burgess y Chengjiang, GOBE, extinción Ordovícico-Silúrico, conquista de la tierra, peces y tetrápodos, Devónico tardío, bosques y oxígeno del Carbonífero (artrópodos gigantes), Pangea, glaciación karoo, **la Gran Mortandad** (Trampas Siberianas, hipótesis).
*Volumen:* ~70 páginas.

**P06 · Mesozoico**: Triásico, Jurásico y Cretácico con sus series y 30 edades: origen y radiación de los dinosaurios, extinción Triásico-Jurásico, ruptura de Pangea, aves, plantas con flor, reptiles marinos, **impacto de Chicxulub y extinción K-Pg** (y Trampas del Decán).
*Volumen:* ~55 páginas.

**P07 · Cenozoico**: Paleógeno, Neógeno y Cuaternario con todas sus épocas y edades (Tortoniense incluido): radiación de mamíferos, PETM, glaciación antártica, crisis del Mesiniense e inundación zancliense, cierre de Panamá, megalodón, ciclos glaciales, megafauna y su extinción, Holoceno y sus tres edades, debate del Antropoceno.
*Volumen:* ~55 páginas.

**P08 · Grandes procesos transversales del tiempo profundo**
Páginas resumen con listados enlazados: **las extinciones masivas** (las cinco grandes y las menores), **todas las glaciaciones** (de Pongola a la última; cuántas hay según el criterio), supercontinentes (Vaalbará → Pangea → Pangea Última), grandes impactos, historia del oxígeno y del CO₂, color y química de los océanos, evolución del día y de la Luna. Más el **bestiario**: ~80 fichas de animales y plantas emblemáticas en su época (Tyrannosaurus, Triceratops, Giganotosaurus, Megalodon, Anomalocaris, Meganeura, Dimetrodon, mamut…).
*Volumen:* ~110 páginas.

### Bloque 3 · Humanidad prehistórica

**P09 · Evolución humana**
Ampliación profunda de los 39 linajes (Sahelanthropus → Homo sapiens, pasando por Lucy, *H. heidelbergensis*, neandertales, denisovanos, *floresiensis*, *luzonensis*, *naledi*…), procesos (bipedismo, fuego, lenguaje, cerebro), migraciones fuera de África, yacimientos clave (Atapuerca, Olduvai, Denisova…), tecnologías líticas (Olduvayense → Magdaleniense), mezcla genética. Árbol evolutivo interactivo.
*Volumen:* ~80 páginas.

**P10 · Del Paleolítico superior al Neolítico**
Paleolítico superior y arte rupestre, Último Máximo Glacial, poblamiento de América por Beringia, Mesolítico, Holoceno temprano, Neolítico y domesticación por focos (Creciente Fértil, China, Mesoamérica, Andes, Sahel, Nueva Guinea), megalitismo, primeros metales. Páginas para las **culturas del mapa** (las 503 de `Países/CULTURE-*`, agrupadas por familias cuando sean muy afines), p. ej. «Tierras bajas aluviales · comunidades mesolíticas».
*Volumen:* ~60 monografías + fichas B/C de culturas.

### Bloque 4 · Historia: «El mundo en…», entidades, personas y eventos

Cada fase histórica entrega cuatro cosas para su intervalo:
1. **Contextos** «El mundo en…» con desglose por regiones (Europa, Mediterráneo, Oriente Próximo, África, Asia meridional, Asia oriental, América, Oceanía).
2. **Entidades**: imperios, reinos y estados del mapa en ese intervalo.
3. **Personas**: biografías A/B de los dirigentes y figuras clave (no solo gobernantes: también Aristóteles, Confucio, Colón, Newton… cuando sean imprescindibles para el contexto).
4. **Eventos y obras**: guerras, batallas, revoluciones, pandemias, tratados, monumentos.

| Fase | Intervalo | Ejemplos de contenido | Volumen orientativo |
|---|---|---|---|
| **P11** | 3500–1200 a.C. | Sumer, Acad, Egipto (Reinos Antiguo, Medio y Nuevo; Sesostris I, Amenemhat I, Keops, Hatshepsut, Ramsés II), pirámides de Guiza, Harappa, Shang, Hititas, Babilonia y Hammurabi, colapso de la Edad del Bronce | ~140 |
| **P12** | 1200–500 a.C. | Asiria, Neobabilonia, Fenicia, Israel y Judá, Zhou, Olmecas, Grecia arcaica, Persia aqueménida (Ciro, Darío) | ~130 |
| **P13** | 500 a.C.–1 d.C. | Guerras Médicas, Atenas, Alejandro Magno, Diádocos, República romana, Cartago y Guerras Púnicas, Maurya y Ashoka, Qin Shi Huang, Han, Julio César, Augusto | ~180 |
| **P14** | 1–600 | Imperio romano (Tiberio, Trajano, Constantino…), Han y Tres Reinos, Kushán, Sasánidas, Gupta, Teotihuacán, maya clásico, caída de Occidente, Justiniano y **plaga de Justiniano** | ~200 |
| **P15** | 600–1000 | Mahoma y expansión del islam, califatos omeya y abasí, Tang, Carlomagno, vikingos, Bizancio, Ghana, Tiahuanaco | ~180 |
| **P16** | 1000–1450 | Cruzadas, Sacro Imperio, Castilla y Aragón, Song, **Imperio mongol** y Yuan, Mali y Mansa Musa, **Peste Negra**, Guerra de los Cien Años, Tenochtitlan, Inca | ~250 |
| **P17** | 1450–1650 | Caída de Constantinopla, Reyes Católicos, Colón y la era de los descubrimientos, Imperios español y portugués, Otomano (Solimán), Ming, Mogol (Akbar), Reforma, Guerra de los Treinta Años | ~260 |
| **P18** | 1650–1789 | Absolutismo (Luis XIV), Qing, Revolución Gloriosa, Guerra de Sucesión española, Ilustración, Guerra de los Siete Años, independencia de EE. UU. | ~220 |
| **P19** | 1789–1914 | Revolución francesa, Napoleón, independencias americanas, Revolución industrial, unificaciones de Italia y Alemania, Meiji, reparto de África, imperialismo | ~280 |
| **P20** | 1914–1945 | Primera Guerra Mundial, Revolución rusa, gripe de 1918, entreguerras, Guerra Civil española, **Segunda Guerra Mundial** con contexto **año a año** | ~260 |
| **P21** | 1945–2026 | Guerra Fría, descolonización, China maoísta, carrera espacial (**Luna 1969**, Nixon), fin de la URSS, globalización, siglo XXI hasta 2026 | ~300 |

### Bloque 5 · Cobertura total e integración

**P22 · Cobertura completa de dirigentes y entidades**
Fichas B/C para todos los dirigentes y entidades que no tengan monografía: compilación desde Wikidata (fechas, cargos, predecesor/sucesor, dinastía) más resumen redactado, con enlaces. Objetivo: que **ningún nombre de una ficha** quede sin página.

**P23 · Temas transversales**
Pandemias a lo largo de la historia (lista y páginas), religiones, escritura, ciencia y técnica, comercio (Ruta de la Seda…), exploraciones, maravillas del mundo, demografía mundial con gráfico de población, evolución de las formas de gobierno.

**P24 · Revisión integral y cierre**
Auditoría de enlaces, repeticiones, fechas y fuentes; rendimiento; accesibilidad y móvil; actualización completa de `agentes.md`, `tareas.md`, `CHANGELOG.md`; versión mayor.

### Fases opcionales (a decidir)

- **P-X1 · Fichas de país simplificadas**: fichas del mapa escuetas y elegantes (nombre, bandera, dirigentes con enlace a la enciclopedia, capital, dos datos), con lo técnico movido a la enciclopedia. Puede adelantarse si se prefiere.
- **P-X2 · Idiomas**: traducción de la interfaz y, por niveles, de la enciclopedia (ca, es, en, fr, de, pt, it y los idiomas de ampliación).

**Total: 25 fases (P00–P24) + 2 opcionales.** Volumen estimado al final: ~3.000–4.500 páginas escritas (A/B) más fichas generadas para todos los dirigentes y entidades restantes.

---

## 5. Forma de trabajo en cada fase

1. Investigar primero (Wikipedia y fuentes especializadas), redactar después.
2. Escribir en `enciclopedia/`; tocar `src/` solo cuando la fase lo requiera.
3. Ejecutar compilador, `tsc`, pruebas unitarias y una comprobación visual propia en navegador.
4. Actualizar este plan (estado de la fase), `tareas.md`, `agentes.md` y `CHANGELOG.md`.
5. Entregar los comandos de Git y de ejecución local. El propietario sube; no se esperan ni sondean Actions/Pages.

## 6. Comandos útiles

**Reparar el clon actual (Windows, PowerShell):**

```powershell
cd D:\Proyectos\Historicmap
git config --global core.longpaths true
git reset --hard HEAD
git status
```

**Ver el proyecto en local mientras Actions despliega:**

```powershell
cd D:\Proyectos\Historicmap
npm ci
npm run dev
```

Abrir http://127.0.0.1:5173/ . Para pararlo, `Ctrl+C`. No ejecutar `npm run build` para ver en local: regenera archivos preparados y puede dejar cambios en el árbol de trabajo.

## 7. Estado de las fases

| Fase | Estado |
|---|---|
| P00 | ✅ Completada (7/11/2026) |
| P01–P24 | Pendientes |
