# Arquitectura y evolución

## Aplicación inicial

Aplicación estática distribuida por CDN. El navegador mantiene fecha consultada, proyección y capas; el fragmento URL permite compartir fecha y vista. No se requiere servidor ni base de datos. Vite empaqueta TypeScript, estilos y worker de MapLibre. El worker se sirve desde el mismo origen que la aplicación.

`time.ts` es la lógica temporal pura. La posición del eje recorre tramos con distintas escalas, por lo que distancias iguales en pantalla no equivalen a duraciones iguales. La selección utiliza intervalos vigentes 1900–2019, referencia contemporánea desde 2020 e instantáneas discretas antes de 1900. El máximo temporal procede del reloj del dispositivo; la fecha de referencia de los datos se conserva. Un periodo sin datos no hereda fronteras contemporáneas.

Desde 0.2.0 la rueda sobre la superficie de la regla sólo modifica su escala, anclada a la fecha central. El arrastre y el teclado recorren fechas. Los eventos de rueda se consumen dentro de esa superficie, mientras MapLibre conserva sus gestos sobre el mapa. Las marcas usan intervalos legibles por tramo y se generan para la ventana visible con margen; durante el arrastre se reutilizan hasta cambiar de bloque visible. El control fijo de fecha y reproducción es hermano del slider, evitando anidar botones interactivos dentro del rol ARIA de slider.

La colección superior contiene búsqueda, proyección, capas, fuentes/base de datos, pantalla completa e información. El panel de capas es no modal, con foco inicial en cerrar, Escape y cierre exterior. Los diálogos completos comparten contenedor; `about.ts` aporta la identidad, ficha e historial del proyecto siguiendo la estructura de las otras aplicaciones del autor. La versión procede de `package.json`.

`main.ts` coordina interfaz y fuentes del motor. `data.ts` comparte descargas en curso/caché, conserva los recursos recientes y limita a tres las instantáneas antiguas/geológicas. `history.ts` selecciona periodos inclusivos, decodifica TopoJSON sin cuantización y reutiliza geometrías por fid; mantiene gwcode, estatus, administrador, capital y fechas. `profiles.ts` selecciona observaciones no futuras, temas y formato. `recent-context.ts` separa contexto documental del renderizado.

La aplicación **conserva el mapa anterior durante la carga**, con mensaje explícito, `aria-busy` y `data-loaded-year` diferenciados de la fecha solicitada. Un contador creciente descarta respuestas obsoletas; una cola ordena los commits al worker. No abortar una descarga temporal reutilizable al cambiar de año. La firma de territorios evita reenviar la misma geometría/propiedades cuando un periodo no cambia. `data-rendered` identifica el estado aplicado y visible, no sólo la descarga.

La reproducción espera la preparación y aplicación del estado antes de programar el siguiente año (850 ms de lectura entre pasos recientes). Pausa invalida la generación del reproductor, de modo que una espera pendiente no provoca otro avance. En épocas anteriores se conservan pasos por la escala adaptativa. Reproducir desde el presente comienza en 1900; las escenas anteriores siguen accesibles por la regla/épocas.

La base histórica se consulta al 31 de diciembre. La capa Cliopatria 1938–1944 tiene su propia semántica: síntesis anual sin día uniforme. No mezclar silenciosamente ambos criterios. Las capas de guerra/disputa tienen fuente, nota y rango anual y se renderizan por separado con borde discontinuo; pulsarlas abre su explicación. No se interpolan polígonos. Ver ANNUAL-REVIEW para excepciones específicas.

Las estadísticas se enlazan sólo cuando existe correspondencia de entidad; colonias, URSS, Yugoslavia y RDA no heredan cifras de sucesores. Última observación hasta el año consultado y retraso máximo cinco años; cada cifra/leyenda declara años. La serie estadística conserva geografía de publicación, sin recalcular agregados por geometría histórica. Antes de 1960 se restablece el tema político. Los puntos actuales (323) sólo se muestran desde 2020; 1900–2019 usa capitales de cada registro.

Los 26 snapshots originales mantienen coordenadas e identificadores locales. CShapes tiene identificadores persistentes de entidad y registros temporales, no equivalentes a los índices de Natural Earth/Ourednik. La colección conserva licencias por recurso y transformaciones por entrada; las diferencias geométricas de Crimea/Sinaí/Golán se identifican como derivados NC-SA.

La teselación utiliza tolerancia de 0,2 píxeles y zoom máximo de fuente 7 para evitar superar límites de segmentos GPU con las costas globales densas. Los datos originales no cambian. Las pruebas de navegador consideran regresión los avisos de exceso de vértices; aumentar la tolerancia arbitrariamente no sustituye incorporar una fuente multirresolución adecuada.

## Separación futura

La entrega 0.3 separa tiempo, repositorio de datos, periodos, perfiles y contexto. Extraer después el renderizador y componentes de interfaz de main.ts, sin alterar el contrato temporal ni las capas de evidencia. Mantener el motor de renderizado detrás de una interfaz para cambiar proveedores o añadir PMTiles sin acoplar cronología y fuentes.

Modelo objetivo orientativo:

| Objeto | Campos principales |
| --- | --- |
| Source | id, citation, DOI/URL, license, version, retrievedAt |
| Dataset | id, sourceId, layerType, temporalExtent, spatialExtent, resolution, model |
| Entity | id persistente, tipo, nombres por idioma/intervalo, relaciones |
| Observation | entityId, geometryRef, validFrom/Until, evidenceFrom/Until, precision, confidenceClass, sourceId |
| Event | id, participantes, lugar/área, fecha/intervalo, tipo, fuentes |
| Reconstruction | modelId, geologicalTimeMa, anchorReference, transform, uncertainty |

No asignar puntuaciones numéricas de confianza sin una metodología. Distinguir incertidumbre espacial y temporal. Las relaciones de poder no se reducen siempre a un polígono exclusivo. Una compilación puede contener solapamientos legítimos y vacíos documentales.

SQLite/FTS puede servir para preparar catálogos y consultas. PMTiles o teselas vectoriales pueden distribuir geometrías grandes. Evaluar el volumen antes de adoptar SQLite WASM en cliente. No introducir infraestructura sólo para parecer más avanzado.

## Despliegue

`base: './'` mantiene rutas de recursos relativas. Los datos se resuelven con `import.meta.env.BASE_URL`; el estado usa fragmento, por lo que no necesita reescrituras del servidor. `dist/` es un artefacto generado, no código fuente.

GitHub Pages se publica después de Quality, haciendo checkout del SHA que pasó las pruebas. No aceptar artefactos de PR externos para despliegues privilegiados. Las acciones de publicación tienen permisos mínimos de Pages/OIDC, sin tokens persistentes. No hay política de backend porque no hay backend.

## Comprobaciones relevantes

Las pruebas unitarias cubren monotonía del tiempo, extremos, ausencia de año cero, round-trip de anclas y separación de dominios cartográficos. Las de navegador comprueban recorridos del producto, geometrías visibles, fecha de snapshot distinta de consulta y disposición móvil. La verificación de datos detecta cambios de bytes/procedencia, no errores históricos o topológicos; la auditoría de contenido es trabajo adicional.

Desde 0.3 se aplica updateData con diferencias por identificador en cambios entre periodos anuales o temas contemporáneos. source-diff.ts calcula altas, bajas y modificaciones; geometrías/propiedades sin cambios no se reenvían al worker. Las capas contextuales también se reutilizan si sus registros no cambian. Las pruebas de navegador se ejecutan contra vite preview de la compilación de producción (5174), con un worker para evitar competencia de GPU por software.

Los indicadores económicos se aplican mediante `feature-state` a la pintura, conservando los valores fechados en memoria para leyenda/fichas. Cambiar un indicador no modifica ni vuelve a teselar la geometría. Los códigos especiales de Natural Earth se traducen a los del Banco Mundial mediante un índice explícito; `-99` nunca agrupa territorios sin identidad común. Abrir una ficha pausa la reproducción para permitir leerla.
