# Historicmap · Plan maestro

Documento único para saber **en qué punto está el proyecto y qué queda por hacer**. Lo puede leer el propietario o cualquier asistente que retome el trabajo. Cada casilla `[x]` está terminada y entregada; cada casilla `[ ]` está pendiente.

- **Actualizado:** 29 de noviembre de 2026.
- **Versión:** 0.78.0.
- **Enciclopedia:** 497 páginas, ≈ 1,78 millones de palabras y ≈ 13.600 enlaces internos. Además, 178 unidades geológicas, 12.606 dirigentes y 2.423 entidades indexados.
- **Documentos relacionados:**
  - [`enciclopedia/PLAN.md`](enciclopedia/PLAN.md): plan rector original, con el diagnóstico, la arquitectura y la norma editorial.
  - [`tareas.md`](tareas.md): historial detallado de tareas y continuidad.
  - [`agentes.md`](agentes.md): notas técnicas por versión, en las secciones numeradas.
  - [`CHANGELOG.md`](CHANGELOG.md): versiones.
  - [`AGENTS.md`](AGENTS.md): reglas del repositorio.
  - [`enciclopedia/README.md`](enciclopedia/README.md): formato de las páginas.

---

## 0. Resumen del estado

| Bloque | Fases | Estado |
|---|---|---|
| Arquitectura y componentes | P00–P02 | ✅ |
| 1 · La Tierra antes de la vida compleja | P03–P04 | ✅ |
| 2 · Fanerozoico y procesos | P05–P08 | ✅ |
| 3 · Humanidad prehistórica | P09 ✅ · P10 | 🟡 P10 en curso (faltan G y H) |
| 4 · Historia (3500 a. C.–2026) | P11–P21 | ⬜ Pendiente |
| 5 · Cobertura total, temas y cierre | P22–P24 | ⬜ Pendiente |
| Opcionales | PX1, PX2 | 🟡 PX2 empezada (1.ª parte) |

**Siguiente paso:** P10-G y P10-H (apartado 4), entrega 0.79.0, que cierra P10.

---

## 1. Reglas de trabajo (para cualquier asistente)

1. **Norma editorial:**
   - Nivel universitario o de doctorado.
   - Mínimo 1.500 palabras de cuerpo por página. Las unidades amplias, las monografías mayores y los panoramas, 2.000–3.000 o más.
   - Etimología; límites y criterios; dónde se observa; cifras con fuente; debates; tablas, gráficos, mapas y líneas de tiempo.
   - Imagen libre propia y no repetida.
   - Sin texto de plantilla ni retórica defensiva.
   - No repetir: se enlaza.
2. **Formato** (detalle en `enciclopedia/README.md`):
   - Páginas Markdown con cabecera YAML.
   - Enlaces internos `[[id|texto]]`.
   - Enlaces al mapa `[[@CLAVE año|texto]]`, que llevan a un punto de yacimiento en su época.
   - Componentes `:::componente …`, `:::grafico`, `:::linea-tiempo`, `:::mapa` y `:::galeria`, y recuadros `:::nota`, `:::debate`, `:::clave`, `:::curiosidad` y `:::datos`.
   - Las páginas que sustituyen un artículo heredado usan su mismo id.
3. **Textos de la interfaz:** siempre en `i18n/es/*.json`, leídos con `tx('espacio.clave')`. Nunca texto visible en el código.
4. **Validación antes de cada entrega:**
   - `node scripts/build-encyclopedia.mjs --check`, sin errores ni avisos de extensión.
   - `npx tsc --noEmit -p .`
   - `npm run i18n:check`
   - `npx vitest run`
   - `python3 -m unittest discover -s tests/research -p 'test_*.py'`
   - `npm run data:verify`
   - `npm run earth:audit`
   - `python3 scripts/prepare-human-knowledge.py --check`
   - `npm run build`
   - Pruebas de navegador de la enciclopedia: hominin-tree, earth-integration, human-expansion, review-050, review-051, phanerozoic y precambrian.
5. **Entrega:**
   - Actualizar `CHANGELOG.md`, `agentes.md` (sección nueva), `tareas.md`, este `PLAN.md`, `enciclopedia/PLAN.md`, `AGENTS.md`, la versión de `package.json` y `public/data/manifest.json`, y el «Acerca de» (`i18n/es/acerca.json` y `src/about.ts`).
   - Dar al propietario los comandos de PowerShell para subir (él sube; el asistente no hace push) y los de ejecución local.
6. **Agentes:** uno o dos a la vez como máximo, con 5–8 páginas cada uno.
7. **Imágenes:** Wikimedia Commons limita las peticiones desde el entorno en la nube. En ese caso se descarga con `node scripts/fetch-encyclopedia-media.mjs --lista lista.txt` desde el equipo local, que registra autor y licencia en `enciclopedia/medios/creditos.json`.

---

## 2. Fases terminadas

### Arquitectura

- [x] **P00 · Diagnóstico y plan** (7/11/2026).
- [x] **P01 · Arquitectura y lector nuevo** (0.57.0): carpeta `enciclopedia/`, compilador con validación, índice por ramas, composición jerárquica, historial y búsqueda.
- [x] **P02 · Componentes visuales e integración con el mapa** (0.58.0): escala geológica interactiva, gráficos, líneas de tiempo, mapas, galerías, sucesiones y entradas desde el mapa.

### Bloque 1 · La Tierra antes de la vida compleja

- [x] **P03 · Formación de la Tierra, Hádico y Arcaico** (0.59.0, reescrita en 0.60.0).
- [x] **P04 · Proterozoico** (0.61.0): 28 páginas, ≈ 95.600 palabras.

### Bloque 2 · Fanerozoico

- [x] **P05 · Paleozoico** (0.62.0–0.64.0): 100 páginas, ≈ 319.000 palabras.
- [x] **P06 · Mesozoico** (0.67.0): 57 páginas, ≈ 224.600 palabras.
- [x] **P07 · Cenozoico** (0.68.0): 47 páginas, ≈ 167.200 palabras.
- [x] **P08 · Procesos transversales y bestiario** (0.69.0): 96 páginas, ≈ 259.000 palabras.
  - [x] 14 síntesis: tectónica (con componente interactivo), extinciones, glaciaciones, supercontinentes, impactos, nivel del mar, atmósfera, océanos, fósiles, paleoclima, biodiversidad, escala del tiempo, incertidumbre y neblina arcaica.
  - [x] Bestiario de 82 especies, del Ediacárico al Pleistoceno.

### Bloque 3 · Humanidad prehistórica

- [x] **P10-0 y P10-A** (0.76.0): desplegable y portada de la Prehistoria reciente, enlaces a culturas del mapa y 11 páginas del Paleolítico superior (ver apartado 4).
- [x] **P10-B, C y D** (0.77.0): Último Máximo Glacial, poblamiento de los continentes, Epipaleolítico y Mesolítico (21 páginas).
- [x] **P10-E y F** (0.78.0): Neolítico por focos y megalitismo (18 páginas).

- [x] **P09 · Evolución humana** (0.70.0–0.75.0): 81 páginas, ≈ 403.000 palabras.
  - [x] P09-0 · Árbol evolutivo interactivo de los 39 linajes (0.70.0).
  - [x] P09-A1 · Primeros homininos, 6 linajes (0.71.0).
  - [x] P09-A2 · Diversidad australopitecina, 8 linajes (0.71.0).
  - [x] P09-A3 · Parántropos y *Homo* temprano, 10 linajes (0.71.0).
  - [x] P09-A4 · Pleistoceno medio, 10 linajes (0.72.0).
  - [x] P09-A5 · Neandertales, denisovanos, *floresiensis*, *luzonensis* y *sapiens* (0.72.0).
  - [x] P09-B · 15 páginas de procesos (0.73.0).
  - [x] P09-C · 16 yacimientos y enlaces de la enciclopedia a los puntos del mapa (0.74.0).
  - [x] P09-D · 10 páginas de tecnologías de la piedra, del Lomekwiense al Magdaleniense (0.75.0).
  - [x] Portada «Evolución humana» y desplegable unificado (0.71.2).

### Trabajos transversales hechos

- [x] Renovación gráfica del tiempo profundo con WebGL2 (0.65.0).
- [x] PX2, 1.ª parte: carpeta `i18n/` con todos los textos de la interfaz (0.66.0).
- [x] Lectura en voz alta con reproductor en la cabecera (0.60.0–0.61.0).
- [x] Navegación con atrás y adelante del navegador; portadas de desplegable (0.71.2).
- [x] Corrección de los fallos de despliegue y espera de 20 s en las pruebas de navegador (0.71.1).

---

## 3. Volumen pendiente estimado

| Fase | Contenido | Páginas temáticas | Anales anuales |
|---|---|---|---|
| P10 | Paleolítico superior → Neolítico y culturas | ~60 monografías + ~120 fichas de culturas | — |
| P11 | 3500–1200 a. C. | ~140 | 1.800 (3000–1201 a. C.) |
| P12 | 1200–500 a. C. | ~130 | 700 |
| P13 | 500 a. C.–1 d. C. | ~180 | 500 |
| P14 | 1–600 | ~200 | 600 |
| P15 | 600–1000 | ~180 | 400 |
| P16 | 1000–1450 | ~250 | 450 |
| P17 | 1450–1650 | ~260 | 200 |
| P18 | 1650–1789 | ~220 | 139 |
| P19 | 1789–1914 | ~280 | 125 |
| P20 | 1914–1945 | ~260 | 31 |
| P21 | 1945–2026 | ~300 | 82 |
| P22 | Fichas de dirigentes y entidades | miles de fichas generadas | — |
| P23 | Temas transversales | ~80 | — |
| P24 | Revisión y cierre | — | — |

Los anales del 3000 a. C. al 2026 suman 5.026 páginas. En la Antigüedad remota se agrupan apoyándose en el panorama de su década o siglo y sin inventar hechos.

---

## 4. P10 · Del Paleolítico superior al Neolítico 🟡

**Objetivo:** cerrar la Prehistoria. El Paleolítico superior como sociedad y arte (la tecnología ya está en P09-D); el Último Máximo Glacial; el poblamiento de los continentes; el Mesolítico; el Neolítico por focos; el megalitismo; los primeros metales; y las 503 culturas del mapa.

**Carpetas:** `enciclopedia/prehistoria/{paleolitico-superior, glaciar, poblamiento, mesolitico, neolitico, megalitismo, metales, culturas}` (cada una es un subdesplegable de «Prehistoria reciente»). Decisión: las 503 culturas se agrupan en ~120 fichas por familias afines.

- [x] **P10-0 · Infraestructura** (0.76.0)
  - [x] Desplegable «Prehistoria reciente» en el índice, con portada y subgrupos.
  - [x] Enlaces `[[@CLAVE año|…]]` hacia las culturas y regiones culturales del mapa, validados contra `public/data/cultural-index.json`.
  - [x] Página portada «Prehistoria reciente», con una línea de tiempo comparada por continentes.
  - [x] Sustituir el tema heredado `neolithic-transition` (hecho en P10-E, 0.78.0).
- [x] **P10-A · Paleolítico superior: sociedad y arte** (0.76.0, 11 páginas)
  - [x] Arte rupestre (síntesis), Chauvet, Lascaux, Altamira, arte al aire libre (Côa, Siega Verde).
  - [x] Arte mueble: venus, hombre león, propulsores.
  - [x] Música y ornamentos.
  - [x] Enterramientos y vida social; sociedad, demografía y redes.
  - [x] Economía: caza especializada, pesca, recolección, perros.
  - [x] Arte paleolítico de la península ibérica.
- [x] **P10-B · Último Máximo Glacial y refugios** (0.77.0, 5 páginas)
  - [x] El UMG: clima, paisaje y nivel del mar.
  - [x] Refugios: franco-cantábrico, ibérico, italiano y balcánico, ucraniano y siberiano.
  - [x] Beringia.
  - [x] Recolonización tardiglaciar (Bølling-Allerød).
  - [x] Dryas Reciente.
- [x] **P10-C · Poblamiento de los continentes** (0.77.0, 8 páginas)
  - [x] Sahul (Australia y Nueva Guinea; Madjedbebe y su debate).
  - [x] Wallacea y sudeste asiático.
  - [x] Asia oriental y Japón paleolítico.
  - [x] Ártico (Paleoesquimales, Dorset y Thule).
  - [x] América: síntesis y genética; yacimientos anteriores a Clovis; Clovis y Paleoindio.
  - [x] El Pacífico remoto (avance para las fases históricas).
- [x] **P10-D · Epipaleolítico y Mesolítico** (0.77.0, 8 páginas)
  - [x] Epipaleolítico del Próximo Oriente, Natufiense y Göbekli Tepe.
  - [x] Mesolítico europeo (Star Carr, Ertebølle, Lepenski Vir) y Mesolítico ibérico (Muge, Asturiense, La Braña).
  - [x] Jōmon.
  - [x] Edad de Piedra Tardía africana.
  - [x] Arte levantino y esquemático ibérico.
- [x] **P10-E · Neolítico y domesticación por focos** (0.78.0, 12 páginas)
  - [x] Revolución neolítica (sustituye `neolithic-transition`).
  - [x] Creciente Fértil y Çatalhöyük.
  - [x] China, Mesoamérica, Andes y Amazonía.
  - [x] Sahara y Sahel; Nueva Guinea y Asia meridional.
  - [x] Neolítico europeo e ibérico.
  - [x] Genética de la expansión neolítica.
  - [x] Animales domésticos.
- [x] **P10-F · Megalitismo** (0.78.0, 6 páginas): síntesis, Stonehenge, Carnac y Bretaña, megalitismo ibérico (Antequera), Malta, Newgrange.
- [ ] **P10-G · Primeros metales** (~6)
  - [ ] Calcolítico: Varna, Ötzi, Los Millares, cultura campaniforme.
  - [ ] Bronce antiguo: El Argar, Únětice.
  - [ ] Metalurgia en Anatolia y el Cáucaso.
  - [ ] Estepas: Yamna e indoeuropeos.
- [ ] **P10-H · Culturas del mapa** (~120 fichas que agrupan las 503 `CULTURE-*` por familias afines)
  - [ ] Fichas B/C con ámbito, cronología, rasgos, yacimientos y enlace al mapa.
  - [ ] Agrupación por continentes y épocas en el índice.
- [ ] **Entregas previstas:**
  - 0.76.0: P10-0 y P10-A ✅ (28/11/2026).
  - 0.77.0: P10-B, P10-C y P10-D ✅ (28/11/2026).
  - 0.78.0: P10-E y P10-F ✅ (29/11/2026).
  - 0.79.0: P10-G, P10-H y cierre.

---

## 5. Bloque 4 · Historia: estructura común de P11–P21

Cada fase histórica entrega para su intervalo:

1. **Anales:** una página «El mundo en *año*» por cada año, con política, guerras, economía, sociedad, religión, ciencia, cultura, clima y catástrofes, desglosado por regiones. Ruta: `enciclopedia/contextos/anales/<siglo>/<año>.md`, id `anales-<año>`, tipo `contexto`.
2. **Contextos:** panoramas de década, siglo y época por regiones (Europa, Mediterráneo, Oriente Próximo, África, Asia meridional, Asia oriental, América y Oceanía).
3. **Entidades:** imperios, reinos y estados del mapa del intervalo, enlazados a sus claves de `Países/`.
4. **Personas:** biografías de dirigentes y de figuras imprescindibles, nombradas por QID de Wikidata.
5. **Eventos y obras:** guerras, batallas, revoluciones, pandemias, tratados y monumentos.

**Infraestructura previa a P11** (dentro de P11-0):
- [ ] Plantilla y compilador de anales: componentes «dirigentes activos ese año», «entidades del mapa ese año» y «eventos fechados».
- [ ] Enlace desde las fichas de país del mapa (dirigente, entidad) a su página.
- [ ] Generación de borradores de anales a partir de los datos (dirigentes, entidades y eventos), revisados y redactados después.
- [ ] Desplegable «Historia» en el índice, por épocas, regiones y tipos.

### P11 · 3500–1200 a. C. ⬜ (~140 páginas + 1.800 anales)

- [ ] P11-0 · Infraestructura de historia (lo anterior).
- [ ] P11-A · Mesopotamia: Uruk y la escritura, ciudades sumerias, Acad (Sargón), Ur III, Babilonia (Hammurabi), Asiria antigua, Mitanni y Kasitas.
- [ ] P11-B · Egipto: predinástico, Imperio Antiguo (Keops, pirámides de Guiza), primer periodo intermedio, Imperio Medio (Amenemhat I, Sesostris I), hicsos, Imperio Nuevo (Hatshepsut, Tutmosis III, Akenatón, Tutankamón, Ramsés II).
- [ ] P11-C · Indo, China y Asia: Harappa y Mohenjo-Daro, Erlitou, Shang (Anyang, oráculos), Bactria-Margiana.
- [ ] P11-D · Anatolia, Egeo y Mediterráneo: hititas, minoicos, micénicos, Ugarit, El Argar, colapso de la Edad del Bronce y Pueblos del Mar.
- [ ] P11-E · América y resto: Caral, primeros olmecas, Sahara y Nubia (Kerma).
- [ ] P11-F · Anales 3000–2001 a. C.
- [ ] P11-G · Anales 2000–1201 a. C.
- [ ] P11-H · Personas y eventos clave (Gilgamesh como figura literaria, Kadesh…).

### P12 · 1200–500 a. C. ⬜ (~130 + 700 anales)

- [ ] P12-A · Imperio neoasirio, Neobabilonia (Nabucodonosor II), Urartu, Elam.
- [ ] P12-B · Fenicia, Cartago arcaica, Israel y Judá, filisteos.
- [ ] P12-C · Grecia oscura y arcaica, colonización, Etruria, Roma de los reyes, Tartessos e iberos.
- [ ] P12-D · Persia aqueménida (Ciro, Cambises, Darío), Lidia y Media.
- [ ] P12-E · Zhou, Primaveras y Otoños; India védica y los mahajanapadas; Kush (dinastía XXV).
- [ ] P12-F · Olmecas y Chavín.
- [ ] P12-G · Anales 1200–501 a. C.
- [ ] P12-H · Personas: Homero (figura), Zoroastro, Buda, Confucio, Lao-Tse, Solón.

### P13 · 500 a. C.–1 d. C. ⬜ (~180 + 500 anales)

- [ ] P13-A · Guerras Médicas, Atenas clásica, Esparta, Guerra del Peloponeso.
- [ ] P13-B · Macedonia, Alejandro Magno, reinos helenísticos y diádocos.
- [ ] P13-C · República romana, Guerras Púnicas, Hispania romana (Numancia), guerras civiles, Julio César, Augusto.
- [ ] P13-D · Maurya (Chandragupta, Ashoka), Reinos Combatientes, Qin Shi Huang, Han occidental.
- [ ] P13-E · Partia, Nabatea, Meroe, Axum temprano; mesoamericanos preclásicos.
- [ ] P13-F · Anales 500–1 a. C.
- [ ] P13-G · Personas y obras: Pericles, Sócrates, Platón, Aristóteles, Aníbal, Escipión; Partenón, Gran Muralla, guerreros de terracota.

### P14 · 1–600 ⬜ (~200 + 600 anales)

- [ ] P14-A · Alto Imperio romano (Julio-Claudios, Flavios, Antoninos: Tiberio, Trajano, Adriano, Marco Aurelio).
- [ ] P14-B · Crisis del siglo III, Diocleciano, Constantino, cristianismo, caída de Occidente.
- [ ] P14-C · Pueblos germánicos y reinos sucesores (visigodos en Hispania, francos, ostrogodos).
- [ ] P14-D · Han oriental, Tres Reinos, Jin, dinastías del Norte y del Sur; Kushán; Gupta.
- [ ] P14-E · Sasánidas, Axum, reinos árabes preislámicos.
- [ ] P14-F · Teotihuacán, maya clásico temprano, Moche, Nazca.
- [ ] P14-G · Justiniano y la plaga de Justiniano.
- [ ] P14-H · Anales 1–600.

### P15 · 600–1000 ⬜ (~180 + 400 anales)

- [ ] P15-A · Mahoma, califato ortodoxo, omeyas, Al-Ándalus, abasíes.
- [ ] P15-B · Bizancio medio, búlgaros, Rus de Kiev.
- [ ] P15-C · Carolingios y Carlomagno, vikingos, reinos cristianos peninsulares.
- [ ] P15-D · Sui y Tang, Silla, Nara y Heian, Tíbet, imperios de las estepas.
- [ ] P15-E · Ghana, Swahili, Kanem; maya clásico tardío, Tiahuanaco y Wari.
- [ ] P15-F · Anales 600–1000.

### P16 · 1000–1450 ⬜ (~250 + 450 anales); posible división en P16a y P16b

- [ ] P16-A · Cruzadas, Sacro Imperio, papado, Francia e Inglaterra.
- [ ] P16-B · Península ibérica: reinos de taifas, Castilla, Aragón, Navarra, Portugal, Granada nazarí.
- [ ] P16-C · Imperio mongol (Gengis Kan, Kublai), Yuan, Ilkanato, Horda de Oro, Timur.
- [ ] P16-D · Song, Jin, Japón de Kamakura y Muromachi, Jemeres (Angkor), Delhi.
- [ ] P16-E · Mali (Mansa Musa), Gran Zimbabue, Etiopía salomónica.
- [ ] P16-F · Peste Negra, Guerra de los Cien Años.
- [ ] P16-G · Mexicas (Tenochtitlan), incas tempranos, Cahokia.
- [ ] P16-H · Anales 1000–1450.

### P17 · 1450–1650 ⬜ (~260 + 200 anales); posible división

- [ ] P17-A · Caída de Constantinopla, Imperio otomano (Mehmed II, Solimán).
- [ ] P17-B · Reyes Católicos, Monarquía Hispánica (Carlos V, Felipe II), Portugal.
- [ ] P17-C · Colón, exploraciones, conquista de México y Perú, intercambio colombino.
- [ ] P17-D · Renacimiento, Reforma y Contrarreforma, Guerra de los Treinta Años.
- [ ] P17-E · Ming, Japón Sengoku y Tokugawa, Mogoles (Babur, Akbar), Safávidas.
- [ ] P17-F · Songhai, Kongo, trata atlántica.
- [ ] P17-G · Anales 1450–1650.

### P18 · 1650–1789 ⬜ (~220 + 139 anales)

- [ ] P18-A · Luis XIV y el absolutismo, Revolución Gloriosa, Guerra de Sucesión española.
- [ ] P18-B · Rusia de Pedro I y Catalina II, Prusia, Austria.
- [ ] P18-C · Ilustración, revolución científica (Newton).
- [ ] P18-D · Guerra de los Siete Años; independencia de EE. UU.
- [ ] P18-E · Qing (Kangxi, Qianlong), Mogoles tardíos, Japón Edo.
- [ ] P18-F · América colonial, Oceanía (Cook).
- [ ] P18-G · Anales 1650–1789.

### P19 · 1789–1914 ⬜ (~280 + 125 anales); posible división

- [ ] P19-A · Revolución francesa, Napoleón, Congreso de Viena.
- [ ] P19-B · Independencias americanas y repúblicas.
- [ ] P19-C · Revolución industrial y movimientos sociales.
- [ ] P19-D · Unificaciones de Italia y Alemania; Imperio austrohúngaro.
- [ ] P19-E · Restauración Meiji; China Qing tardía (guerras del Opio, Taiping).
- [ ] P19-F · Imperialismo y reparto de África; India británica.
- [ ] P19-G · España del siglo XIX.
- [ ] P19-H · Anales 1789–1914.

### P20 · 1914–1945 ⬜ (~260 + 31 anales muy detallados)

- [ ] P20-A · Primera Guerra Mundial (frentes, batallas, tratados).
- [ ] P20-B · Revolución rusa y URSS; gripe de 1918.
- [ ] P20-C · Entreguerras: crisis de 1929, fascismos, Guerra Civil española.
- [ ] P20-D · Segunda Guerra Mundial, año a año y por frentes; Holocausto.
- [ ] P20-E · Asia: China republicana, Japón imperial, guerra del Pacífico.
- [ ] P20-F · Anales 1914–1945.

### P21 · 1945–2026 ⬜ (~300 + 82 anales); posible división

- [ ] P21-A · Guerra Fría, bloques, OTAN y Pacto de Varsovia.
- [ ] P21-B · Descolonización de Asia y África.
- [ ] P21-C · China maoísta y reformas; Corea, Vietnam.
- [ ] P21-D · Carrera espacial (Luna 1969).
- [ ] P21-E · Fin de la URSS; Europa (UE); España de la Transición.
- [ ] P21-F · Globalización, siglo XXI, conflictos y crisis hasta 2026.
- [ ] P21-G · Anales 1945–2026.

---

## 6. Bloque 5 · Cobertura total, temas y cierre

### P22 · Cobertura completa de dirigentes y entidades ⬜

- [ ] P22-A · Generador de fichas B/C de dirigentes (12.606) desde Wikidata: fechas, cargos, predecesor y sucesor, dinastía, con resumen redactado.
- [ ] P22-B · Fichas de entidades políticas (≈ 3.995 en `Países/`) sin monografía.
- [ ] P22-C · Fichas de yacimientos (`ARCH-*`, 792) sin página propia.
- [ ] P22-D · Comprobación de que ningún nombre de una ficha del mapa queda sin página.

### P23 · Temas transversales ⬜ (~80)

- [ ] Pandemias a lo largo de la historia.
- [ ] Religiones del mundo.
- [ ] Escritura y alfabetos.
- [ ] Ciencia y técnica.
- [ ] Comercio y rutas (Ruta de la Seda, especias).
- [ ] Exploraciones.
- [ ] Maravillas del mundo.
- [ ] Demografía mundial, con gráfico.
- [ ] Formas de gobierno.
- [ ] Clima histórico (Óptimo medieval, Pequeña Edad de Hielo).

### P24 · Revisión integral y cierre ⬜

- [ ] Auditoría de enlaces, repeticiones, fechas y fuentes, incluida la revisión de las dudas factuales anotadas en `agentes.md` §90–98.
- [ ] Rendimiento (tamaño del índice, carga diferida) y accesibilidad (teclado, lectores de pantalla, móvil).
- [ ] Documentación completa y versión mayor 1.0.0.

---

## 7. Fases opcionales

- [ ] **PX1 · Fichas de país simplificadas:** nombre, bandera, dirigentes enlazados, capital y datos clave; lo técnico pasa a la enciclopedia.
- [ ] **PX2 · Idiomas**
  - [x] 1.ª parte (0.66.0): carpeta `i18n/`, cargador, detección de idioma y comprobador de claves.
  - [ ] 2.ª parte: textos de los datos (nombres de países, unidades y fichas), selector de idioma y traducción de la interfaz a ca, en, fr, de, pt e it.
  - [ ] 3.ª parte: zh, ja, hi, ru y ar (con escritura de derecha a izquierda).
  - [ ] 4.ª parte: traducción por niveles de la enciclopedia, empezando por portadas y fichas.

---

## 8. Deuda y mejoras anotadas

- [ ] Revisar las dudas factuales que listan los agentes en `agentes.md` (P08 y P09), como cifras de estudios 2024–2026 sin DOI y algunas edades y medidas.
- [ ] Unificar la fecha del montaje del Megatherium de Madrid entre la ficha y la página de fósiles.
- [ ] Imagen de Jebel Irhoud en *Homo sapiens*: buscar una de más resolución.
- [ ] Imágenes más específicas para las industrias de transición (Châtelperroniense).
- [ ] Imagen de la recolectora de miel de la Araña para el arte levantino (la de Commons es GPL).
- [ ] Imagen más grande de arpones Saqqaq en la página del Ártico.
- [ ] Al escribir Los Millares (P10-G), enlazarla desde `prehistoria-megalitismo-iberico`.
