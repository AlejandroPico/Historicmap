# Sexta parte · revisión integral de la Tierra

Versión0.56.0, base ef86e0967 (0.55.0). Revisión de integración de las seis partes: continuidad temporal, cartografía, selección, capas, enciclopedia, fuentes, conservación y comprobaciones del producto. No certifica que todos los países, gases atmosféricos, especies o acontecimientos tengan documentación exhaustiva.

## Corrección del despliegue comunicado

El caso móvil de `review-050` conservaba una expectativa anterior a la quinta parte: al llegar a100.000a.C. debía desaparecer todo el hielo. La incorporación de Batchelor2019 añadió la hipótesis del intervalo MIS5c, disponible en modo manual. No corresponde retirar ese modelo para satisfacer una prueba antigua.

El recorrido ahora exige explícitamente PaleoMIST en sus muestras de65/80ka; después comprueba archivo, modelo y explicación MIS5c. Conserva la ausencia de extrapolación comprobando120kaBP1950, un hueco real entre intervalos incorporados, incluso con el modo manual activado. Se mantienen el clic real sobre un yacimiento, la ficha fósil y su persistencia, imágenes y anchura móvil. No se aumenta el tiempo límite ni se omiten aserciones. Las pruebas del módulo PaleoMIST siguen exigiendo su límite propio de80ka. En review-051 se mantiene la ausencia visual automática de MIS5c cálido, y Fuentes comprueba la hipótesis disponible pero no activada, en lugar de una explicación anterior a la ampliación.

## Mejoras encontradas durante la revisión

- La enciclopedia conserva la fecha de consulta cuando pertenece al linaje, unidad geológica o periodo humano seleccionado. Antes podía devolver el mapa a la fecha editorial media de la entrada, aunque el contexto actual fuera válido. Los artículos ajenos a esa fecha conservan su referencia temática; no se trasladan datos fósiles al presente.
- El Cuaternario y sus subdivisiones enlazan con un capítulo desarrollado, con seis apartados sobre escala temporal, ciclos glaciales, curvas, modelos, humanidad y transición cultural. El explorador de CO₂ identifica su ventana aproximada800–12ka: no se presenta como una curva de todo el Cuaternario.
- Fuentes distingue referencia reciente oculta, hipótesis antigua oculta y fecha sin contorno. La ausencia de geometría no significa ausencia de hielo. El ámbito de las síntesis antiguas se explica en español; los originales no se traducen ni se reescriben.
- Las fichas políticas conservadas fuera de su existencia mantienen el aviso de ausencia territorial, sin describir una escena geológica como un cierre de año político.
- La regla conserva todas las marcas y sus fechas accesibles, pero oculta rótulos que se solaparían usando su anchura real en pantalla. La marca1d.C. tiene prioridad. No se introduce año cero ni se cambia el cursor fijo, el calendario o el zoom.
- Se corrige la asociación de la fotografía del arrecife pérmico a una clave de artículo inexistente; enlaza con el artículo real de extinciones, conservando los bytes de la fotografía.
- Se añaden seis imágenes originales acreditadas para africanus, rudolfensis, sediba, heidelbergensis, antecessor y luzonensis. Se inspeccionaron las fotografías; las réplicas se identifican como tales. Se conserva el encuadre original y la presentación completa. Cada medio pertenece a su carpeta natural en `Tierra/Humanidad/linajes`, con autor, página, licencia y huella binaria. No se inventan retratos individuales ni se presenta una réplica como fósil original.

## Inventario reproducible

`npm run earth:audit` comprueba el inventario congelado en `Tierra/Investigacion/parte-6/integracion.json`. El generador es `scripts/audit-earth-integration.mjs`, sin conexión ni dependencias nuevas. También se ejecuta al principio de Quality para detectar asociaciones y referencias internas inválidas antes de las pruebas de navegador. El preparador de etiquetas conserva el formato compacto canónico del manifiesto; Quality vuelve a comprobar la reproducción humana después de construir, para detectar alteraciones introducidas por la propia construcción.

El índice ordinario contiene291 entradas de distintas clases:91 artículos temáticos,177 unidades geológicas y23 periodizaciones humanas. El archivo separado conserva198 candidatos audiovisuales con disposición editorial; que estén contabilizados no implica validación científica individual de sus fechas. Se revisan309 relaciones internas y105 referencias registradas. La comprobación de URLs valida sintaxis y registro local, no disponibilidad HTTP de cada sitio.

Hay25 medios originales de estas partes,18 humanos. Permanecen22 expedientes de linajes/propuestas sin fotografía propia; sus nombres y clasificaciones están en el inventario. No todos tienen un espécimen ilustrable o una especie independiente aceptada. El catálogo conserva39 entradas documentales,24 con áreas propias,68 ventanas geométricas,1.007 puntos fósiles y1.901 observaciones de CO₂. Estos números no equivalen a especies aceptadas, poblaciones simultáneas o registros anuales.

La revisión de conservación contra0.55 mantiene los330 recursos del manifiesto sin pérdidas. Sólo cambia el contenido de `human-knowledge.json` para añadir los seis medios; sus49 artículos y12 imágenes anteriores se preservan exactamente. La versión de metadatos de compilación se actualiza sin modificar las observaciones de CO₂. Países, culturas, fósiles, áreas humanas, costas, hielo y originales de investigación anteriores se conservan.

## Límites contrastados y siguientes ampliaciones

El hielo boreal antiguo aporta doce ventanas y36 variantes; no una serie completa de contornos anuales. No se deducen mantos antárticos antiguos, hielo marino, espesores ni paleocostas del valor deCO₂ oδ18O. Las escenas antiguas documentadas son ilustraciones, no una simulación espectral exacta del color del planeta. Las reconstrucciones costeras conservan la edad nominal de su fuente; antes de las referencias disponibles no se fabrican costas exactas.

Siguen pendientes paleocostas cuaternarias detalladas, más geometría antártica/espesores modelados, curvas publicadas adicionales de temperatura y gases, fotografías adecuadas para las fichas restantes, mayor profundidad monográfica por etapa y contraste individual de los candidatos del archivo audiovisual. El informe no transforma esos huecos en resultados concluidos. Se conservan en tareas.md para siguientes encargos.

## Verificación y publicación

Los resultados efectivos de esta versión se cierran en tareas.md, junto con cualquier fallo detectado y su corrección. La entrega conserva ocho grupos de navegador y el barrido anual independiente. Se prepara una única subida con la corrección comunicada y la sexta parte. El propietario verifica después Actions/Pages; no se espera ni se sondea el despliegue remoto.


Cierre local:416 pruebas/83 archivos,40 pruebas de investigación y38 recorridos de navegador distintos correctos. Repetición final de ficha/Tierra/review-051:10/10 correctos sobre la última construcción;20 focales y cuatro pruebas de reproducción adicionales correctos. Tipos, producción, inventario,330 recursos/11 franjas/9179 medios anteriores y25 medios de estas partes verificados. Capturas revisadas. La tentativa con dos navegadores locales se interrumpió por recursos; la tanda dirigida inicial dio33/34 antes de recargar la expectativa editada. No se ejecutaron completos los164 casos recopilados; el archivo afectado se repitió completo correctamente.
