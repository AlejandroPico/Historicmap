# Precámbrico y enciclopedia · entrega0.53.0

Encargo: tercera parte de la ampliación terrestre y nueva enciclopedia contextual. Base77cf39202. La etapa desarrolla la formación terrestre y el Precámbrico, con navegación general a las otras épocas. No completa por anticipado las partes4–6.

## Cambios visibles

- Botón de libro en segundo lugar. Enciclopedia de pantalla completa, cierre y regreso al mapa, búsqueda sin conexión externa, índice temporal, historial anterior/siguiente, referencias y artículos relacionados.311 entradas:21 artículos temáticos,177 fichas/unidades geológicas,23 referencias humanas y90 revisiones audiovisuales, con su clase identificada. Abre según la fecha consultada; navegar por artículos no cambia el mapa hasta pulsar «Ver en el mapa».
- Contenido temático inicial: formación, Theia, Hádico, Arcaico, microbios, LUCA, atmósfera, océanos, oxigenación, glaciaciones, albedo, Proterozoico, eucariotas, Rodinia, tectónica, interior terrestre, Matachewan, Oklo, Ediacárico, incertidumbres y distinción Jurásico/K–Pg.
- Apartados explicativos, esquemas propios, imagen actual de Jack Hills e imagen de una simulación lunar, con crédito. Vídeo de referencia cargado únicamente a petición, situado en el segmento relacionado. Interacciones de albedo e impacto, declaradas como esquemas simplificados.
-15 escenarios de superficie: acreción incandescente, enfriamiento, mares/cortezas tempranos, intervalos arcaicos, oxigenación, paleoglaciaciones y continentes proterozoicos. El mismo mapa soporta2D/3D y gestos de cámara, incluido orientar al norte.
- Bandas antiguas más extensas mediante anclas cada150Ma, además de conservar las anteriores. Paleta precámbrica editorial diversa; la carta ICS canónica y sus colores permanecen intactos. No imprimir nombres cortados; los intervalos demasiado pequeños conservan nombre accesible, tooltip y entrada enciclopédica. Pulsar una banda abre su ficha; arrastrarla sigue desplazando la regla.

## Fuentes, cantidades y límites

Los materiales propios están en [Tierra/Precambrico](../Tierra/Precambrico/README.md). Se mantienen modelos, especies, culturas y medios anteriores. Desde1,8Ga las formas disponibles proceden de las instantáneas CAO2024 existentes. Antes son ilustraciones, no posiciones continentales recuperadas. Texturas, color del agua y hielo antiguo expresan escenarios, no fotografías ni observaciones globales.

Se incorporan dos referencias antiguas de día solar: Lantink et al.2022 a2,46Ga y Williams2000 a620Ma, con errores y ventanas editoriales explícitas. No se interpolan todos los días del Precámbrico. La composición atmosférica y temperatura no cuantificadas se describen cualitativamente; se mantienen nulos en los campos numéricos, sin convertir muestras OCR en mediciones.

El inventario de parte3 contiene90 observaciones/candidatos. Se registran las decisiones, discrepancias y referencias de contexto, incluidos los casos no adoptados como efectos fechados. Ejemplos: LUCA no es la primera vida, el Hádico no permanece enteramente fundido, el comienzo de tectónica/núcleo interno no tiene una fecha única probada, Pongola/Gaskiers no demuestran un manto global, y un océano rojo/púrpura mundial o incendios a580Ma no se adoptan. La Marinoana termina cerca de635Ma; el impacto de Chicxulub es del límite K–Pg, no del final jurásico.

## Arquitectura y conservación

`deep-earth.ts` resuelve intervalos y paleta; `deep-surface.ts` produce texturas deterministas en un CanvasSource nativo de MapLibre. Se recalculan por escenario, hielo o instantánea, no en cada movimiento de cámara. Los conceptos vacían las fuentes geográficas por la cola existente para evitar países actuales superpuestos; al volver se reinvalidan firmas y se recargan las fuentes requeridas. La selección documental existente se conserva con su propia fecha.

`encyclopedia-model.ts` consulta artículos y genera fichas cronológicas. `encyclopedia.ts` se importa al abrir: no descarga vídeos ni solicita servicios externos al recorrer el mapa. Diálogo nativo, foco, Escape, historial y desplazamiento interno; el contenido de Países no se traslada. Dos imágenes nuevas se acreditan y verifican por SHA; no se publican fotogramas privados del vídeo. No se añaden dependencias ni se cambia la partición de CI.

## Verificación y continuidad

Tipos y producción correctos.29 pruebas focales en cinco archivos correctas, más repetición final de las siete nuevas tras los ajustes. Nueve recorridos pertinentes de navegador correctos, incluida la colección completa de instantáneas, controles, ficha persistente, base planetaria y enciclopedia. Última repetición conjunta de los dos archivos de Tierra/enciclopedia: cuatro correctos en2,4min, con descarga retrasada y cambio de capa, limpieza de filtros y restauración del hielo. Capturas revisadas. Recopilación152 casos en63 archivos. No se afirma que se hayan ejecutado completos esos152 casos.

Integridad:283 recursos,11 franjas de glifos y9179 medios anteriores correctos por SHA; dos imágenes nuevas verificadas por sus hashes. Originales de investigación e ICS177 reproducibles intactos. La tentativa inicial de batería completa, simultánea con generación/construcción, se interrumpió tras un timeout de recursos; después review-051 y los focales pasan en serie. No se registra aquella tentativa como batería completa correcta. Detalle en [tareas.md](../tareas.md) y agentes.md§73.

No esperar Actions/Pages tras subir. Los siguientes trabajos son las reconstrucciones del Fanerozoico, ampliación de contenidos y nuevas curvas/modelos físicos cuando se identifiquen fuentes apropiadas. La enciclopedia tiene estructura extensible; no se declara que todas las monografías del mundo ya estén redactadas.
