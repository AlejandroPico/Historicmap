# Entrada para agentes y colaboradores

Antes de trabajar, leer íntegramente **[agentes.md](agentes.md)**, documento canónico solicitado por el propietario. Sus decisiones y requisitos forman parte de las instrucciones del proyecto.

Leer también **[tareas.md](tareas.md)** y actualizar la pizarra al avanzar o interrumpir trabajo. Conservar comprobaciones, carencias y siguiente paso; no confundir una reanudación de sesión con haber terminado pendientes.

Actualizar `agentes.md`, `CHANGELOG.md` y la documentación pertinente en toda entrega que cambie funcionalidad, arquitectura, datos, alcance o limitaciones. No duplicar la especificación en este archivo. No confundir planes con funciones implementadas.

Estado vigente 0.61: enciclopedia por fases (enciclopedia/PLAN.md); P00–P08 cerradas, ver secciones 82–90 de agentes.md.

Internacionalización (desde 0.66): ningún texto visible se escribe en el código. Todo texto nuevo de la interfaz va a `i18n/es/<área>.json` y se usa con `tx('modulo.clave')` (con `{marcadores}` para datos); `npm run i18n:check` debe pasar. Formatos de número y fecha con `language` de `src/i18n.ts`, nunca `'es'` fijo. Ver `i18n/README.md`.
