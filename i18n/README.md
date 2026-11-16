# Internacionalización (i18n)

Todos los textos de la **interfaz** de Historicmap están aquí, separados del código, para poder traducir la aplicación
entera de una vez (por ejemplo, entregando esta carpeta a una IA) sin tocar ningún archivo de `src/`.

## Estructura

```
i18n/
├── idiomas.json        ← idioma base y lista de idiomas (código, nombre propio, estado, dirección de escritura)
├── README.md           ← este documento
└── es/                 ← español: idioma original y de reserva
    ├── interfaz.json   ← barra de herramientas, capas, filtros, regla temporal, búsqueda, fuentes, avisos
    ├── fichas.json     ← fichas de países y entidades: dirigentes, gobierno, afiliaciones, comparaciones
    ├── historia.json   ← contextos históricos fechados, catálogo de ciudades y yacimientos, notas de fronteras
    ├── tierra.json     ← tiempo profundo, planeta, hielo, homininos, culturas y cronología geológica
    ├── enciclopedia.json ← lector de la enciclopedia: índice, buscador, reproductor de voz, componentes
    └── acerca.json     ← panel «Acerca de» e historial de versiones
```

Cada archivo agrupa los textos por módulo del código y por clave:

```json
{ "main": { "verMapa2d": "Ver mapa 2D", "cargandoMapa": "Cargando mapa de {year}…" } }
```

El código pide el texto con `tx('main.verMapa2d')`; los datos variables van entre llaves (`{year}`) y se rellenan al
mostrarlo (`tx('main.cargandoMapa', { year })`).

## Cómo traducir a un idioma nuevo

1. Copia la carpeta `es/` con el código del idioma (`en/`, `fr/`, `ca/`, `zh/`…), el mismo de `idiomas.json`.
2. Traduce **solo los valores**. Nunca cambies:
   - las claves (`"verMapa2d"`) ni los nombres de módulo (`"main"`);
   - los marcadores entre llaves (`{year}`, `{n}`…): pueden cambiar de posición, pero deben seguir todos;
   - las etiquetas HTML (`<strong>`, `<a …>`), las entidades (`&nbsp;`), los símbolos (`↗`, `→`, `·`) ni los espacios
     iniciales o finales, que unen el texto con lo que lo rodea en pantalla.
3. En `idiomas.json`, cambia el `estado` del idioma a `"traducido"`.
4. Comprueba con `npm run i18n:check`: indica las claves que faltan, las que sobran y los marcadores perdidos.

La aplicación elige sola el idioma del sistema si está traducido (si no, español). Un texto que falte en un idioma se
muestra en español. La elección manual se guarda en el navegador (`historicmap-idioma`).

Instrucción sugerida para una IA: *«Traduce al <idioma> los valores de todos los JSON de `i18n/es/` y guárdalos en
`i18n/<código>/` con los mismos nombres de archivo. No cambies claves, marcadores `{…}`, etiquetas HTML, símbolos ni
espacios iniciales o finales. Mantén nombres propios, siglas y cifras.»*

## Lo que no está en esta carpeta

| Contenido | Dónde está | Cómo se traducirá |
|---|---|---|
| Enciclopedia (≈ 540.000 palabras en Markdown) | `enciclopedia/` (original en español) | Copia traducida en `i18n/<código>/enciclopedia/` con la misma estructura de carpetas y los mismos `id` en la cabecera. Hay que pasar a la IA `enciclopedia/` además de `i18n/es/`. |
| Nombres de unidades geológicas | `Tierra/Cronologia/ics-2026-06.json` (campo `name`, de la ICS) | La carta ICS publica nombres oficiales en muchos idiomas: se tomarán de la fuente. |
| Escenas, culturas, homininos, contextos fechados de los datos | `Tierra/**/*.json`, `public/data/*.json` | Fase PX2: extraer sus textos a `i18n/<código>/datos/`. |
| Nombres de países, entidades y dirigentes | `public/data/identities.json`, `Países/` | Fase PX2 (los nombres propios suelen conservarse o tienen forma establecida por idioma). |
| Reglas de pronunciación de la voz | `src/encyclopedia/speech-text.ts` | Son propias del español (Ma → «millones de años»…); cada idioma necesitará las suyas. |

Mensajes internos de error, URL, siglas y nombres de datos usados como claves de búsqueda se quedan en el código a
propósito: no se muestran al usuario o deben coincidir con los datos.
