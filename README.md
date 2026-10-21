# Historicmap

**El tiempo tiene un lugar.** Atlas interactivo de la evolución de la Tierra y de las sociedades humanas, con mapa 2D, globo 3D y navegación temporal.

Versión inicial: **0.1.0** · 21 de octubre de 2026. Autor del proyecto: Alejandro Pico.

## Empezar

Usar **Node.js 26.12.1 o posterior**; la versión de referencia está en `.nvmrc`.

```sh
npm ci
npm run dev
```

Abrir la dirección local que indique Vite. Para generar la aplicación estática: `npm run build`. El resultado se guarda en `dist/`; `npm run preview` permite revisarlo. Las rutas relativas permiten alojarla bajo `/Historicmap/`.

## Primera versión

- Mapa vectorial 2D y globo 3D con zoom, selección y búsqueda local.
- Regla temporal arrastrable: se mueve la regla y el indicador permanece centrado. Teclado, rueda, escala ajustable, reproducción y saltos de época.
- Navegación entre 4.540 Ma y 2026 con escala adaptativa no uniforme y fechas exactas introducidas por el usuario.
- 26 instantáneas incorporadas: una contemporánea, trece históricas y doce tectónicas.
- Contexto documental, fuentes, fecha de la instantánea y límites de precisión visibles.
- Relieve contemporáneo opcional, tres lugares de referencia, enlaces compartibles y diseño adaptable.
- Ventana «Acerca de», versión e historial inicial.

**Esto es una base funcional, no un atlas exhaustivo.** La cartografía contemporánea es Natural Earth 1:10 millones, generalizada para escala mundial; no satisface todavía el objetivo final de máxima definición ni certifica fronteras a fecha de hoy. Las instantáneas históricas son aproximadas y necesitan revisión. No se interpolan fronteras entre años.

Para etapas anteriores a 1.800 Ma, y para la prehistoria entre 1 Ma y 10.000 a. C., no se inventan mapas. La aplicación indica la ausencia de datos e incluye contexto. El efecto de la Tierra primitiva es conceptual, no una simulación física. Homininos, migraciones, glaciaciones, atmósfera, biomas, impactos y conflictos requieren nuevas capas documentadas.

## Calidad y publicación

```sh
npm run data:verify
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

GitHub Actions ejecuta validación de datos, pruebas de cronología, compilación y pruebas de navegador. El flujo `Publish atlas` publica en GitHub Pages únicamente tras una ejecución correcta de `Quality` en `main`. Requiere que **Settings → Pages → Source** esté configurado como **GitHub Actions**. No contiene secretos ni necesita un servidor propio. Las acciones están fijadas a su versión mayor; `package-lock.json` fija dependencias de npm.

## Datos y continuidad

Consultar **[agentes.md](agentes.md)** antes de modificar el proyecto. Contiene la visión completa, decisiones, arquitectura, roadmap, reglas de colaboración y estado real. [AGENTS.md](AGENTS.md) es el punto de entrada para asistentes que detectan ese nombre automáticamente.

Las fuentes, licencias, atribuciones y límites se documentan en [docs/SOURCES.md](docs/SOURCES.md). `public/data/manifest.json` contiene versiones de origen, URLs, fechas de descarga, número de entidades y huellas SHA-256. Los datos se distribuyen dentro del repositorio; `npm run data:fetch` realiza una **actualización explícita** desde las fuentes y modifica ese manifiesto. No se descarga cartografía nueva durante la compilación.

La cartografía local funciona sin API key. El relieve (AWS), las etiquetas cartográficas (servidor de demostración MapLibre) y las fuentes tipográficas (Google Fonts) requieren conexión. La aplicación no envía búsquedas a servicios externos ni incorpora analítica. No está implementada como aplicación instalable o completamente offline.

El código original no tiene todavía una licencia de distribución elegida por el titular. Los datos de terceros conservan sus propias licencias; ver [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
