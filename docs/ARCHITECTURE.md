# Arquitectura y evolución

## Ampliación 0.6 · datos temporales

`historical-affiliations.ts` consume el catálogo local `affiliations.json`; `historical-context.ts` consume `historical-context.json`. Se importan como metadatos locales del build; no consultan proveedores al navegar. Membresías y eventos usan fin exclusivo; mandatos mantienen fin inclusivo. Las membresías del mapa se observan al cierre anual y las de Datos conservan todas las relaciones del año. Los eventos son fichas relacionadas, no beligerantes para una pintura automática.

`entityCode` permite unir entidades históricas a relaciones sin reutilizar códigos estadísticos de sucesores. `history.ts` conserva identidades YUG/FRY/SCG/CSK/SUN y selecciona la base de Crimea de 2013 para Rusia/Ucrania desde 2014; la ocupación es independiente. `data.ts` añade los contornos de referencia declarados y la ocupación anual de Kuwait. Cada recurso registra su transformación y licencia separadamente.

El buscador usa un panel no modal como las fuentes; sólo fecha y Acerca de usan el diálogo modal. La disposición, selección común de país, reloj local y control temporal se conservan. La deduplicación prioriza curación, precisión y título, mantiene renovaciones y separa cargos de partido de jefaturas nacionales.

## Aplicación inicial

Aplicación estática distribuida por CDN. El navegador mantiene fecha consultada, proyección y capas; el fragmento URL permite compartir fecha y vista. No se requiere servidor ni base de datos. Vite empaqueta TypeScript, estilos y worker de MapLibre. El worker se sirve desde el mismo origen que la aplicación.

`time.ts` es la lógica temporal pura. La posición del eje recorre tramos con distintas escalas, por lo que distancias iguales en pantalla no equivalen a duraciones iguales. La selección utiliza intervalos Cliopatria 1789–1885, CShapes 1886–2019, referencia contemporánea desde 2020 e instantáneas discretas antes de 1789. El máximo temporal procede del reloj del dispositivo; la fecha de referencia de los datos se conserva. Un periodo sin datos no hereda fronteras contemporáneas.

Desde 0.2.0 la rueda sobre la superficie de la regla sólo modifica su escala, anclada a la fecha central. El arrastre y el teclado recorren fechas. Los eventos de rueda se consumen dentro de esa superficie, mientras MapLibre conserva sus gestos sobre el mapa. Las marcas usan intervalos legibles por tramo y se generan para la ventana visible con margen; durante el arrastre se reutilizan hasta cambiar de bloque visible. El control fijo de fecha y reproducción es hermano del slider, evitando anidar botones interactivos dentro del rol ARIA de slider.

La colección superior contiene búsqueda, proyección, capas, fuentes/base de datos, pantalla completa e información. El panel de capas es no modal, con foco inicial en cerrar, Escape y cierre exterior. Los diálogos completos comparten contenedor; `about.ts` aporta la identidad, ficha e historial del proyecto siguiendo la estructura de las otras aplicaciones del autor. La versión procede de `package.json`.

`main.ts` coordina interfaz y fuentes del motor. `data.ts` comparte descargas en curso/caché, conserva los recursos recientes y limita a tres las instantáneas antiguas/geológicas. `history.ts` selecciona periodos inclusivos, decodifica TopoJSON sin cuantización y reutiliza geometrías por fid; mantiene gwcode, estatus, administrador, capital y fechas. `profiles.ts` selecciona observaciones no futuras, temas y formato. `recent-context.ts` separa contexto documental del renderizado.

La aplicación **conserva el mapa anterior durante la carga**, con mensaje explícito, `aria-busy` y `data-loaded-year` diferenciados de la fecha solicitada. Un contador creciente descarta respuestas obsoletas; una cola ordena los commits al worker. No abortar una descarga temporal reutilizable al cambiar de año. La firma de territorios evita reenviar la misma geometría/propiedades cuando un periodo no cambia. `data-rendered` identifica el estado aplicado y visible, no sólo la descarga.

La reproducción espera la preparación y aplicación del estado antes de programar el siguiente año (850 ms de lectura entre pasos recientes). Pausa invalida la generación del reproductor, de modo que una espera pendiente no provoca otro avance. En épocas anteriores se conservan pasos por la escala adaptativa. Reproducir desde el presente comienza en 1900; las escenas anteriores siguen accesibles por la regla/épocas.

CShapes se consulta al 31 de diciembre; Cliopatria es una síntesis anual sin día uniforme. El frente español de 1937 corresponde a octubre. Las capas de control tienen fuente, nota, intervalo y controlador; se dibujan opacas con color compartido por potencia, ocultando el relleno y líneas inferiores. Los clientes conservan tonos distintos de los aliados. Desactivarlas recupera la base territorial. Pulsarlas abre autoridad y explicación, sin convertir control en soberanía reconocida. No se interpolan polígonos. Ver ANNUAL-REVIEW para excepciones específicas.

Las estadísticas se enlazan sólo cuando existe correspondencia de entidad; colonias, URSS, Yugoslavia y RDA no heredan cifras de sucesores. Última observación hasta el año consultado y retraso máximo cinco años; cada cifra/leyenda declara años. La serie estadística conserva geografía de publicación, sin recalcular agregados por geometría histórica. Antes de 1960 se restablece el tema político. Los puntos actuales (323) sólo se muestran desde 2020; 1886–2019 usa capitales de cada registro.

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


## Identidades y control desde 0.4

`political.ts` resuelve familias políticas y colores de régimen; `politicalData` agrega identidad/color conservando geometrías e identificadores. Las firmas incluyen color e identidad para que un cambio de régimen sin cambio de costa se comunique al worker. La extensión anual anterior a 1886 filtra componentes Cliopatria y excluye agregados `Components`; los prefijos de sus IDs evitan colisiones con CShapes. El fondo gris usa costa contemporánea como referencia para áreas sin entidad en el inventario; no añade soberanía ni desplaza fronteras históricas.

`identities.ts` selecciona símbolos y autoridades por intervalos inclusivos y fecha de adquisición. `country-card.ts` produce la ficha común a selección y búsqueda, con identidad y retratos antes de indicadores/contexto. Desde 0.5, fuentes se resume en un panel no modal y enlaza el catálogo documental; se retira el módulo del antiguo diálogo largo. Identidades y medios se almacenan localmente; cada imagen mantiene su licencia, autoría y huella. Las autoridades repetidas de una misma persona se consolidan sin fusionar personas rivales. Los códigos coloniales no heredan dirigentes contemporáneos. Consultar IDENTITIES y SPANISH-CIVIL-WAR para semántica, preparación y límites.

Los frentes españoles son particiones complementarias del mismo exterior, con las fuentes de cada año y registro de georreferenciación. No se mezclan derivaciones BY-SA con CShapes NC-SA. Los recursos originales `ww2.geojson` y snapshots se conservan para trazabilidad aunque la selección actual use `historical-control.geojson` y la cronología ampliada. Las pruebas geográficas verifican lugares concretos en los polígonos, además de cobertura/IDs y recorridos del navegador.


## Separación de identidades, aspecto y agrupaciones en 0.5

El identificador vacío nunca se compara con un QID de entidad. El índice NE/WDI sólo acepta equivalencias de entidad explícitas: ISO_A3_EH puede representar una asociación territorial y no constituye una clave única. Los perfiles de BRI, CLP, KAB, IOA, CSI y ATC no sobrescriben BRA, FRA, KAZ o AUS. Pruebas de todos los territorios en años focales y un clic real en Brasil tras España evitan la regresión.

Autoridades se filtra por intersección con el año, no sólo por quien termina diciembre. Se conservan periodos no consecutivos. La precisión y los límites superiores inciertos no se convierten en fechas exactas. La ficha común crea tablist/tabpanel con foco por teclado, de forma independiente de selección de búsqueda o mapa.

appearance.ts resuelve una preferencia manual o la hora local. Cambiar aspecto sólo actualiza CSS/pintura/cielo; no reemplaza fuentes ni geometrías. El océano mantiene luminancia mayor que el fondo. El modo automático se revisa cada minuto y al recuperar visibilidad.

current-affiliations.ts es una instantánea de hechos de pertenencia con fuente y fecha por organización, válida únicamente para 2026. El color se aplica mediante expresión de pintura por código, sin redibujar costas ni inferir membresía de dependencias. La leyenda distingue categorías. Las cifras WDI siguen en feature-state; agrupaciones/estadísticas ocultan la pintura de control para no mezclar lecturas. Los conflictos son contextos parciales fechados por país, nunca una clasificación global de guerra/paz.

El medio oficial de Mozambique utiliza `Media.display: full-frame`: la imagen conserva todo su encuadre, con pie identificativo y vínculo directo a la licencia. El verificador exige este modo para medios ND; no aplicarles el recorte visual de los retratos. El archivo WebP se conserva sin transformaciones.
