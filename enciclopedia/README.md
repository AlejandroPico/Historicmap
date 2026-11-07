# enciclopedia/ · guía editorial y de formato

Contenido canónico de la enciclopedia de Historicmap. Cada página es un archivo Markdown con una cabecera YAML. El compilador `scripts/build-encyclopedia.mjs` valida las páginas, comprueba los enlaces y genera `enciclopedia/_generado/`. Esa carpeta no se edita a mano ni se sube a Git: se regenera sola al arrancar `npm run dev` o `npm run build`. Plan general y estado de las fases: [PLAN.md](PLAN.md).

## Carpetas

| Carpeta | Contenido | Prefijo de identificador habitual |
|---|---|---|
| `general/` | portada, guía de uso, páginas de marco | libre (`portada`, `guia-…`) |
| `geologia/` | eones, eras, periodos, épocas y edades de la carta ICS | `geo-<idICS>` (p. ej. `geo-Jurassic`, `geo-Tortonian`) |
| `tierra/` | formación, interior, atmósfera, océanos, tectónica, supercontinentes, impactos | `tierra-…` |
| `clima/` | glaciaciones, invernaderos, hipertermales, ciclos orbitales | `clima-…` |
| `vida/` | origen y evolución de la vida, extinciones, bestiario | `vida-…`, `especie-…` |
| `humanidad/` | homininos, migraciones, yacimientos, tecnologías | `humanidad-…` (los linajes heredados usan `hominin-…`) |
| `culturas/` | culturas y comunidades prehistóricas y protohistóricas | `cultura-…` |
| `contextos/` | «El mundo en…»: panoramas de un intervalo | `contexto-…` |
| `entidades/` | estados, reinos, imperios (clave de `Países/`) | `entidad-<CLAVE>` |
| `personas/` | biografías (QID de Wikidata) | `persona-<QID>` |
| `eventos/` | guerras, batallas, revoluciones, pandemias, tratados, hitos | `evento-…` |
| `obras/` | monumentos y grandes obras | `obra-…` |
| `temas/` | conceptos transversales | `tema-…` |
| `medios/` | imágenes con su ficha de licencia (`medios/creditos.json`) | — |

**Panoramas por fecha.** Al abrir la enciclopedia desde el mapa se muestra «El mundo en *año*». Esa página reúne, de lo más concreto a lo más general, todas las páginas `tipo: contexto` cuyo intervalo contiene el año: los **anales** de ese año (`contextos/anales/<siglo>/<año>.md`, `id: anales-1943`, `inicio: 1943`, `fin: 1943`), el panorama de su década o siglo (`id: contexto-1940s`, `inicio: 1940`, `fin: 1949`) y los panoramas de época más amplios. Después añade automáticamente las unidades geológicas, las periodizaciones humanas, todos los dirigentes del mundo ese año y las páginas fechadas que lo incluyen. Los anales anuales cubrirán, como mínimo, desde el 3000 a. C. hasta hoy.

El identificador manda, no la carpeta: una página `geo-Jurassic` sustituye la ficha automática de esa unidad aunque viva en cualquier subcarpeta. Las personas y entidades del atlas ya tienen ficha automática (cargos y sucesiones); al escribir `persona-Q1407.md` la biografía se antepone a esos datos.

## Cabecera

```yaml
---
id: geo-Jurassic            # obligatorio, único, letras, números y guiones
tipo: geologia              # obligatorio: portada, guia, geologia, tierra, clima, vida, especie, humanidad,
                            #   cultura, contexto, entidad, persona, evento, obra, tema, lista
titulo: Jurásico            # obligatorio
alias: [Jurasico, Edad de los dinosaurios]
resumen: Una frase que aparece bajo el título y en los índices.
inicio: 201.4 Ma            # años civiles (1943, -490, "1943-05-01") o edades ("201.4 Ma", "4.54 Ga", "11.7 ka")
fin: 143.1 Ma
anclaMapa: 150 Ma           # fecha que abre «Ver en el mapa» (opcional)
padre: geo-Mesozoic         # página que la contiene: se usa para componer «Leer completo»
orden: 2                    # posición entre hermanas (opcional)
relacionados: [vida-dinosaurios, clima-invernaderos]
ficha:                      # ficha lateral; valores con Markdown y enlaces
  Duración: 58 Ma
  Clima: cálido, sin casquetes polares
fuentes:
  - titulo: Comisión Internacional de Estratigrafía
    url: https://stratigraphy.org/chart
---
```

Las unidades geológicas no necesitan `padre`, `inicio` ni `fin`: los toma de la carta ICS (`Tierra/Cronologia/ics-2026-06.json`).

Un artículo temático con `padre: geo-<unidad>` forma parte de esa unidad: aparece en su «Contenido» y se lee dentro de ella con «Leer completo», antes de sus subdivisiones. El campo `reemplaza: [id-heredado]` retira un artículo antiguo de `Tierra/` y redirige sus enlaces a la página nueva. Si una página nueva usa el mismo identificador que un artículo heredado (p. ej. `theia`), lo sustituye conservando sus imágenes, esquemas interactivos y vídeos.

## Cuerpo

- Títulos `##`, `###`, `####` (el título principal sale de la cabecera).
- **Negrita**, *cursiva*, `código`, enlaces externos `[texto](https://…)`.
- Enlaces internos: `[[geo-Triassic]]` o `[[geo-Triassic|el Triásico]]`. El compilador falla si el destino no existe.
- Listas, tablas con `|`, citas con `>`, imágenes `![texto alternativo](medios/carpeta/archivo.jpg "Pie con autor y licencia")`.
- Bloques especiales:

```markdown
:::clave
Idea principal en dos líneas.
:::

:::debate Hipótesis sobre su causa
Texto con las posturas y las evidencias.
:::

:::cronologia
252 Ma | Comienza el vulcanismo de las Trampas Siberianas
251,9 Ma | Extinción masiva del final del Pérmico
:::

:::datos
Oxígeno: 35 %
CO₂: 800 ppm
:::

:::componente escala-geologica Phanerozoic
:::
```

Otros tipos de recuadro: `nota`, `curiosidad`, `cita`.

Componentes sin datos (`:::componente nombre argumentos` + `:::`): `escala-geologica [idICS]` (interactiva, se amplía al pulsar), `reloj-geologico`, `curva-temperatura-fanerozoico`, `atmosfera [fecha]`.

Componentes con datos en el bloque:

```markdown
:::grafico linea | Población mundial | millones | año
año; población
1800; 990
1900; 1650
2000; 6150
:::

:::linea-tiempo Hitos del Proterozoico
2.43 Ga / 2.2 Ga | Gran Oxigenación
717 Ma / 660 Ma | Glaciación Esturtiana
1492 | Llegada de Colón a América | texto opcional
:::

:::mapa Yacimientos
-26.6, 116.5 | Jack Hills
países: AUS
:::

:::galeria Título
medios/carpeta/imagen.jpg | Pie de foto
:::
```

`grafico` admite `linea`, `area` y `barras`; separador `;`, `,` o tabulador. En `linea-tiempo`, un intervalo se escribe `inicio / fin`.

**Imágenes.** Se descargan con `node scripts/fetch-encyclopedia-media.mjs "File:Nombre.jpg" carpeta/archivo.jpg --pie "texto"` (o `--lista archivo.txt`), que solo admite licencias libres y registra autor, licencia y fuente en `medios/creditos.json`. El compilador rechaza imágenes sin crédito.

## Estilo

1. Voz enciclopédica, clara y técnica. Frases completas; nada de telegrafía.
2. La incertidumbre se explica una vez, donde importa (bloque `debate` o apartado «Evidencias»), no en cada frase.
3. No repetir: cada idea vive en una página y las demás enlazan.
4. Cifras con su unidad y, si es una estimación, con su margen o su fuente.
5. Textos redactados de nuevo a partir de las fuentes (Wikipedia, ICS, artículos científicos…); nunca copiados. Cada página lista sus fuentes.
6. Imágenes solo con licencia libre verificada y crédito completo.
7. Fechas: años civiles sin año cero (`-1` = 1 a. C.); edades geológicas en Ma/Ga antes de 1950.

## Comprobar

```powershell
node scripts/build-encyclopedia.mjs --check
```
