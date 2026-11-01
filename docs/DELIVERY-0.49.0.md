# Entrega 0.49.0 · 1 de noviembre de 2026

## Resultado y alcance

Consulta ampliada a **10.000–6.001 a. C.**, enlazada con el contenido ya publicado. Se añaden 20 expedientes arqueológicos —15 identidades nuevas y cinco ampliaciones— y 27 referencias culturales de las fuentes de 10.000 y 8.000 a. C. Las ventanas permiten consultar 4.000 fechas civiles, sin afirmar observación anual independiente, ocupación continua, Estados, banderas o gobernantes no acreditados.

Nueva capa opcional de mantos de hielo **PaleoMIST 1.0**, desactivada al iniciar: 24 originales geográficos, cuatro regiones y seis muestras cada 2.500 años BP1950. Se muestran edad y fecha reales de la muestra; polos, antimeridiano, huecos y componentes solapados se resuelven sin simplificar los contornos. Se diferencian BP1950, b2k y cronología civil. **Las costas y el relieve siguen siendo referencias contemporáneas**, expresamente indicadas.

La cartografía política y las áreas culturales siguen activadas al iniciar e independientes en Capas y Filtros. Los nuevos puntos se consultan en búsqueda y en la capa de capitales, ciudades y yacimientos. Fichas, pestañas y contexto permanecen al cambiar de fecha. La carga de hielo participa en el indicador del botón de reproducción y sólo se confirma la última fecha solicitada.

## Conservación y organización

- Autoridades: los 20.559 registros anteriores permanecen íntegros. Símbolos anteriores conservados; no se añaden retratos o banderas supuestos a los yacimientos.
- Culturas: las 10.277 fases anteriores conservan su checksum semántico completo. Total: **10.304 fases**.
- Se conservan todos los registros anteriores de contexto, lugares, gobernanza e historial. Véanse [conservación](CONSERVATION-bc10000.json) y [referencias anteriores](CONSERVATION-REFERENCES-bc10000.json).
- Total: **1.621 identidades históricas y 4.448 carpetas catalogadas**. Datos de entidades dentro de `Países/`; nuevos expedientes por tramo en `arqueologia/`. Originales naturales y cronología en `Tierra/`, sin convertir hielo en países.
- Regeneración completa de hielo, culturas, entidades y registro idéntica en datos, semántica del manifiesto e índice de países. Tras la revisión visual se unen los solapamientos originales del hielo y se comprueba separadamente que sus siete recursos vuelven a producir los mismos bytes. [Informe](REGENERATION-bc10000.json).

## Comprobaciones locales

- Serie general: **367 pruebas correctas en 76 archivos**. Las comprobaciones antiguas del límite inferior se actualizan para no exigir una instantánea histórica donde corresponde contexto conceptual; se admiten años civiles de cinco cifras en el validador de prueba.
- Ajuste visual final del hielo: **28 pruebas focales correctas**, con una prueba adicional de unión geométrica; las siete pruebas del hielo también pasan tras comprobar el solapamiento real de componentes norteamericanos. El inventario actual de la suite general contiene 368 pruebas; no se presenta una repetición focal como una segunda ejecución general.
- **32 pruebas Python correctas**, incluido el formato arqueológico independiente del límite político de 400 años.
- Tipos y compilación de producción correctos. Seis recorridos de navegador sobre producción aislada correctos antes del ajuste visual; los tres recorridos finales de la versión con hielo unido también pasan, con capturas revisadas en mapa y globo.
- Integridad: **253 recursos de datos, 11 franjas tipográficas y 9.179 medios con licencia**, comprobados con SHA-256. Los 24 originales del hielo se verifican contra sus hashes propios. Los 244 archivos preparados coinciden con sus objetos Git; los 9.443 recursos también se verifican contra sus objetos y SHA-256. De ellos, 9.389 conservan el objeto anterior.

## Pendientes explícitos

Paleocostas y paleorrelieve coherentes con nivel del mar y ajustes glacioisostáticos; rutas y áreas de dispersión humana, otros homininos, vegetación y clima detallados; validación regional independiente de las áreas de compilación; más yacimientos y fases dentro y fuera del tramo. No se da por investigada ninguna fase anterior a 10.000 a. C. La [ruta terrestre](ROADMAP-EARTH-HISTORY.md) conserva el desarrollo hasta la formación del planeta.

Se envía a `main` sin esperar Actions ni Pages. El propietario verifica el despliegue; estas comprobaciones locales no equivalen a confirmar la publicación remota.
