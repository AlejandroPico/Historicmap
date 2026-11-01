# Indicadores del planeta · base 0.52.0

`indicadores.json` es el catálogo científico canónico inicial. Se incorpora localmente en la aplicación; la visita no consulta servicios remotos. No incluye la extracción OCR del vídeo ni curvas antiguas aprobadas.

Cada registro contiene:

- Identidad del indicador, cantidad física, valor numérico/rango/nulo y unidad.
- Referencia temporal discriminada: año civil, edad BP1950, b2k2000 o Ma con época nominal explícita.
- Intervalo de consulta (`availableFromYear` y `validUntilYear` opcional/inclusivo); fecha del dato siempre conservada.
- Fuente, versión, fecha de consulta, alcance, método, tipo de evidencia e incertidumbre.
- Política explícita sin interpolación. Un desconocido se muestra como tal, nunca se sustituye por0.

Las primeras siete referencias cubren composición atmosférica superficial aproximada, rotación sidérea y superficie oceánica contemporáneas de NASA (consulta2026), más anomalías térmicas globales OMM2024 y2025. Las fechas de observación no se convierten en observaciones del cursor: en2026 se puede consultar el dato2025 con su año visible. No se proyectan estas referencias hacia el pasado.

Se separan temperatura absoluta y anomalía respecto a1850–1900, y día solar y rotación sidérea. Tampoco se trata el porcentaje redondeado de otros gases como desglose químico completo, ni se infieren presiones parciales de una composición divulgativa. La incertidumbre térmica publicada se conserva; las aproximaciones NASA no reciben un margen numérico inventado.

La consulta muestra explícitamente la falta de series antiguas. Las nuevas estimaciones de partes3–5 deberán añadirse con ventanas temporales y fuentes propias. Un modelo con intervalo limitado debe declarar `validUntilYear`; el lector no rellena automáticamente huecos ni extrapola una muestra a todas las épocas.

Las referencias PaleoMIST y LR04 que ya existen se consultan para contexto y fecha del modelo, sin convertir δ¹⁸O en temperatura superficial ni en contornos nuevos de hielo. Sus archivos no cambian.
