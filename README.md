# Historicmap

**El tiempo tiene un lugar.** Atlas interactivo de la evolución de la Tierra y de las sociedades humanas, con mapa 2D, globo 3D y navegación temporal.

Versión actual: **0.5.0** · 22 de octubre de 2026. Autor del proyecto: Alejandro Pico.

**[Abrir el atlas publicado](https://alejandropico.github.io/Historicmap/)**

## Empezar

Usar **Node.js 26.12.1 o posterior**; la versión de referencia está en `.nvmrc`.

```sh
npm ci
npm run dev
```

Abrir la dirección local que indique Vite. Para generar la aplicación estática: `npm run build`. El resultado se guarda en `dist/`; `npm run preview` permite revisarlo. Las rutas relativas permiten alojarla bajo `/Historicmap/`.

## Funciones

- Mapa vectorial 2D y globo 3D con zoom, selección y búsqueda local.
- Regla temporal arrastrable con indicador, fecha y reproducción centrados. La rueda sobre la regla cambia la escala sin desplazar la fecha; sobre el mapa hace zoom geográfico. Las teclas más/menos ajustan la escala y las flechas recorren el tiempo.
- Mapa a pantalla completa con siete herramientas en la esquina superior derecha, sin cabecera ni franjas de controles alrededor de la regla. Capas en un panel desplegable.
- Navegación entre 4.540 Ma y el año del dispositivo, con escala adaptativa no uniforme y años introducidos por el usuario.
- Cronología anual desde 1789: Cliopatria hasta 1885 y CShapes 1886–2019, con dependencias coloniales y capitales históricas cuando están documentadas. Reproducción reciente anual que espera la carga y conserva el mapa anterior mientras llega el siguiente.
- Control territorial opaco por potencia; colores específicos de regímenes, clientes y bandos. Primera y Segunda Guerra Mundial, Guerra Civil española 1936–1939 y control comunista chino, además de Sinaí, Golán y Crimea. Fuentes anuales y frente de octubre de 1937 identificados con su precisión.
- Banderas históricas, autoridades y retratos en las fichas. Catálogo de mandatos para 267 claves de entidad, con series focales y cobertura mundial desigual; cada imagen conserva su licencia y autoría.
- Base contemporánea desde 2020 y 26 instantáneas originales conservadas para historia anterior/geología y trazabilidad.
- Fichas a la izquierda con pestañas Autoridades, Datos, Contexto y Conflictos; todos los mandatos documentados del año. Fuentes en un panel compacto y leyenda a la derecha.
- Apariencia mañana/tarde/noche/automático según hora local, con preferencia conservada.
- Agrupaciones2026 de OTAN, UE, BRICS y Tres Mares, con categorías distintas y fuentes oficiales. Contextos de conflictos parciales y fechados.
- Fichas con capital, situación política, administración y hasta seis indicadores WDI fechados. Colores temáticos de PIB total, PIB por habitante y población.
- Relieve contemporáneo de referencia apagado al abrir y disponible desde 10.000 a. C., 323 capitales/grandes ciudades actuales y capitales históricas por periodo, enlaces compartibles y diseño adaptable.
- Ventana «Acerca de» con favicon, identidad, versión e historial, portfolio del autor y repositorio.

**La revisión anual no es una certificación exhaustiva de todas las fronteras.** [El informe 1789–año actual](docs/ANNUAL-REVIEW.md) registra cada selección, cambios y límites. CShapes termina en 2019, omite ocupaciones temporales y cambios pequeños. Desde 2020 se utiliza una referencia contemporánea incorporada en 2026, no una reconstrucción independiente de cada año. Faltan los frentes actuales, fases del Sinaí y otros detalles. La costa Natural Earth 1:10m todavía no alcanza el objetivo final de máxima definición. No se interpolan fronteras ni se inventan cambios futuros al avanzar el reloj.

Para etapas anteriores a 1.800 Ma, y para la prehistoria entre 1 Ma y 10.000 a. C., no se inventan mapas. La aplicación indica la ausencia de datos e incluye contexto. El efecto de la Tierra primitiva es conceptual, no una simulación física. Homininos, migraciones, glaciaciones, atmósfera, biomas, impactos y la cobertura mundial completa de conflictos requieren nuevas capas documentadas.

## Calidad y publicación

```sh
npm run data:verify
npm run data:audit
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

GitHub Actions valida datos, pruebas temporales/históricas/estadísticas, compilación y recorridos de navegador: años 1789–actualidad, reproducción y pausa, peticiones lentas, fichas, ciudades, economía, cartografía anterior/geológica, zoom y móvil. `Publish atlas` publica únicamente después de `Quality` correcto en `main`. No contiene secretos ni necesita un servidor propio. Las versiones exactas de dependencias figuran en `package-lock.json`.

## Datos y continuidad

Consultar **[agentes.md](agentes.md)** antes de modificar el proyecto. Contiene la visión completa, decisiones, arquitectura, roadmap, reglas de colaboración y estado real. [AGENTS.md](AGENTS.md) es el punto de entrada para asistentes que detectan ese nombre automáticamente.

Las fuentes, licencias, atribuciones y límites se documentan en [docs/SOURCES.md](docs/SOURCES.md). `public/data/manifest.json` registra los 35 recursos locales, versiones, URLs, transformaciones y SHA-256. `npm run data:fetch` actualiza explícitamente las 26 instantáneas originales, conservando las nuevas capas. La adquisición y reconstrucción de las capas recientes se explica en SOURCES. No se descargan datos nuevos durante la compilación ni desde las fichas.

La cartografía funciona sin API key. Las geometrías, perfiles, series y letras del mapa utilizadas son locales. El relieve (AWS) y las fuentes tipográficas de interfaz (Google Fonts) requieren conexión. La aplicación no envía búsquedas a servicios externos ni incorpora analítica. No está implementada como aplicación instalable o completamente offline.

El código original no tiene todavía una licencia de distribución elegida por el titular. Los datos de terceros conservan sus propias licencias; ver [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Cobertura del año vigente y medios: [CURRENT-AUTHORITIES](docs/CURRENT-AUTHORITIES.md). Agrupaciones, conflictos y fuentes: [CURRENT-LAYERS](docs/CURRENT-LAYERS.md).
