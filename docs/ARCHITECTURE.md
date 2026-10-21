# Arquitectura y evolución

## Aplicación inicial

Aplicación estática distribuida por CDN. El navegador mantiene fecha consultada, proyección y capas; el fragmento URL permite compartir fecha y vista. No se requiere servidor ni base de datos. Vite empaqueta TypeScript, estilos y worker de MapLibre. El worker se sirve desde el mismo origen que la aplicación.

`time.ts` es la lógica temporal pura. La posición del eje recorre tramos con distintas escalas, por lo que distancias iguales en pantalla no equivalen a duraciones iguales. La selección de cartografía utiliza instantáneas discretas por dominio. Un periodo sin datos no hereda fronteras contemporáneas.

Desde 0.2.0 la rueda sobre la superficie de la regla sólo modifica su escala, anclada a la fecha central. El arrastre y el teclado recorren fechas. Los eventos de rueda se consumen dentro de esa superficie, mientras MapLibre conserva sus gestos sobre el mapa. Las marcas usan intervalos legibles por tramo y se generan para la ventana visible con margen; durante el arrastre se reutilizan hasta cambiar de bloque visible. El control fijo de fecha y reproducción es hermano del slider, evitando anidar botones interactivos dentro del rol ARIA de slider.

La colección superior contiene búsqueda, proyección, capas, fuentes/base de datos, pantalla completa e información. El panel de capas es no modal, con foco inicial en cerrar, Escape y cierre exterior. Los diálogos completos comparten contenedor; `about.ts` aporta la identidad, ficha e historial del proyecto siguiendo la estructura de las otras aplicaciones del autor. La versión procede de `package.json`.

`main.ts` coordina interfaz, diálogo, búsqueda y mapa. La descarga de cada instantánea es cancelable; un identificador creciente impide que una respuesta antigua reemplace el estado más reciente. Se borra la geometría al iniciar el cambio para evitar mostrar mapas anteriores bajo una fecha nueva. `data-rendered` se actualiza al quedar el mapa inactivo con geometrías visibles y sirve para las pruebas de integración.

Los GeoJSON se importan manteniendo sus coordenadas; se reducen sus propiedades al contrato `{name, group, precision, code, color}`. Los identificadores de entidad de esta versión son locales a cada archivo, no identidades persistentes entre épocas. El importador no realiza simplificación de geometría. El motor sí tesela/recorta para visualizar; no prometer fidelidad catastral.

La teselación utiliza tolerancia de 0,2 píxeles y zoom máximo de fuente 7 para evitar superar límites de segmentos GPU con las costas globales densas. Los datos originales no cambian. Las pruebas de navegador consideran regresión los avisos de exceso de vértices; aumentar la tolerancia arbitrariamente no sustituye incorporar una fuente multirresolución adecuada.

## Separación futura

Antes de añadir grandes funcionalidades, separar control temporal, repositorio de snapshots, renderizador, catálogo de fuentes y componentes de interfaz. Mantener el motor de renderizado detrás de una interfaz para cambiar proveedores o añadir PMTiles sin acoplar cronología y fuentes.

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
