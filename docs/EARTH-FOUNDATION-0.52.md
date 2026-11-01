# Parte2/6 · panel planetario y cronograma · 0.52.0

Base: `f813686674cd0768eb6e8866ee8f73ef2dafecb9`. Fecha:1/11/2026. Esta entrega incorpora la infraestructura de información y navegación; las nuevas reconstrucciones físicas siguen en las partes3–5.

## Uso

El botón orbital **Planeta y cronología**, junto a Capas, abre un panel compacto con tres pestañas: Planeta, Cronología y Fuentes. Permanece abierto al cambiar de fecha, reproducir o alternar2D/3D; conserva pestaña, posición de lectura y detalles de indicadores que continúan existiendo. La ficha de país se conserva de forma independiente. Los otros desplegables de herramientas comparten el espacio derecho por apertura voluntaria; los cambios temporales no los cierran.

El panel tiene cabecera y pestañas fijas, contenido desplazable sin barra visible, navegación por flechas/Home/End entre pestañas, y cierre con Escape que devuelve el foco al botón sin cerrar la ficha de país. No hay modal ni velo de fondo.

Las bandas se desplazan con la regla y el cursor central permanece fijo. Tres niveles visibles se adaptan a la escala; las jerarquías completas están en el panel. Precámbrico se identifica como agrupación contextual de sus eones. Las bandas se sitúan encima de los trazos/números para no taparlos. Al consultar con detalle el Cuaternario, la geología se atenúa y las periodizaciones humanas ganan presencia; el intervalo geológico sigue vigente en la ficha. La superposición de transformaciones humanas se resuelve por prioridad visual, conservando todos los contextos activos en la ficha.

**Capas → Colores del cronograma** permite activar/desactivar la paleta, conservando la preferencia local. Colores geológicos de referencia ICS y paleta editorial humana; ninguna cambia el color físico de océanos/atmósfera ni el tema mañana/tarde/noche.

## Fuentes y datos

- [Vocabulario geológico](../Tierra/Cronologia/README.md):177 unidades ICS2026/06, nombres españoles, jerarquía, colores, incertidumbre numérica y estado del GSSP. RDF y PDF declaradamente2026/06; se resolvió la advertencia de cabecera antigua de la auditoría.
- Se preservan los límites GSSP del Holoceno en b2k2000, sin confundirlos con BP1950. No hay año cero ni hueco artificial al cambiar de Pleistoceno a Holoceno.
- Las23 referencias humanas son regionales/editoriales, no edades oficiales de todo el mundo. Incluyen prehistoria, divisiones paleolíticas francesas, Mesolítico/Neolítico/metales, edades históricas europeas y transformaciones industrial/digital/espacial. No son catálogo mundial exhaustivo.
- [Modelo planetario](../Tierra/Planeta/README.md): valor/rango/nulo, unidad, base temporal, intervalo, fuente, método y certeza. Siete referencias iniciales; incertidumbre publicada y desconocidos explícitos.
- [NASA](https://science.nasa.gov/earth/facts/): composición superficial aproximada78%N₂/21%O₂/1%resto, rotación sidérea23.9h y superficie oceánica próxima71%; referencias contemporáneas redondeadas consultadas2026.
- [OMM2024](https://wmo.int/publication-series/state-of-global-climate/state-of-global-climate-2024) y [OMM2025](https://wmo.int/news/media-centre/earths-climate-swings-increasingly-out-of-balance): anomalías anuales1.55±0.13°C y1.43±0.13°C respecto a1850–1900. No temperatura absoluta ni observación automática2026/2027.
- LR04/PaleoMIST conservan contexto y fecha propia; la ficha distingue edad del cursor y fecha nominal de la instantánea paleogeográfica disponible. No se generan nuevos contornos ni temperaturas desde esos proxies.

La extracción OCR y los acontecimientos/candidatos de la parte1 siguen como investigación, sin importarse en producción. Datos antiguos aún no curados aparecen como desconocidos. No se añaden escenas de magma, atmósfera, deriva, glaciaciones antiguas, biología o impactos por dar por ciertas todas las afirmaciones del vídeo.

## Arquitectura y conservación

`src/earth-chronology.ts`: consulta geológica y regional; `src/chronology-bands.ts`: proyección de intervalos sobre la regla existente; `src/planet.ts`: referencias fechadas y valores; `src/planet-card.ts`: ficha; `src/planet.css`: presentación. Se usan componentes y dependencias ya existentes, sin bibliotecas nuevas ni backend.

La preparación geológica es reproducible con `scripts/prepare-earth-chronology.py --check`; la prueba Python contrasta el vocabulario publicado con el original fijado. JSON importado declara `with {type:'json'}` para evitar el fallo de recopilación anterior.

Se conservan geometrías, topologías, referencias culturales/humanas, hielo, estadísticas, autoridades y medios anteriores. Los generadores existentes pueden actualizar metadatos de versión del manifiesto durante la construcción; no supone adquirir cartografía nueva. La batería de ocho grupos de navegador y el barrido anual separado no cambian.

## Comprobaciones

390 pruebas completas y23 focales tras ajustes correctas; tipos, producción y reproducción Python correctos. Cinco recorridos pertinentes de navegador correctos, incluidos los dos nuevos, persistencia de ficha, autoridades/fotos y herramientas/zoom independiente.150 casos recopilados en62 archivos; no se ha repetido toda la batería de navegador. Integridad de283 recursos,11 franjas tipográficas y9179 medios correcta.

Las pruebas nuevas cubren jerarquía y transiciones, b2k y ausencia de cero, intervalos/regiones, bandas sin colisiones, datos nulos y referencias fechadas, pestañas persistentes, color local, teclado, móvil vertical/horizontal y proyección. Capturas revisadas. La lista exacta de herramientas incorpora Planeta sin reducir la prueba de zoom. El estado de envío queda en tareas.md y agentes.md§72; no se espera Actions/Pages después de subir.

## Siguiente parte

Parte3: formación terrestre y Precámbrico. Revisar los segmentos del vídeo y sus fuentes, adoptar modelos y geometrías con alcance identificado, incorporar sólo curvas justificadas y producir escenas propias con su incertidumbre. La existencia del panel no significa que esa reconstrucción ya esté realizada.
