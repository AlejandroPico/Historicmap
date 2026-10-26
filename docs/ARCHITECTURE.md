# Arquitectura y evolución

## Ampliación1920–1949 · 0.11

Adquisición incremental `enrich-1920-authorities.py`; curaciones puras y reproducibles en `curate-1920-authorities.py`, `curate-1920-europe-asia.py`, `curate-1920-americas.py` y `curate-1920-regions.py`. Guardan retratos antes de regenerar sus registros; sus ventanas no alteran automáticamente mandatos fuera del intervalo revisado. RSR/ROC/YKM/DAN/TIB/RSI distinguen entidades, no sólo etiquetas. La retirada de una afirmación genérica falsa de doble cargo no elimina el cargo presidencial real.

`periodsAt` corrige la validez observada de Danzig sin cambiar el archivo original CShapes. En1938 `composeControl` resta el contorno documental de Danzig a los demás componentes, después de integrar controles, y lo añade una sola vez como DAN. Sin esa partición, extender la fecha produciría dos propietarios superpuestos. Se conserva la atribución y licencia original; no hay un mapa mundial fusionado redistribuido con una licencia inventada. La corrección no certifica todas las fronteras de1938 ni otras omisiones del inventario.

Administraciones desde1920, suplementos contemporáneos con fecha de cobertura explícita y Vaticano desde7/6/1929. Auditoría `coverage-1920.test.ts`: cada entidad/año de fuente, suplemento y control activo; no sustituye la prueba puntual de geometría compuesta, ni es censo de todos los cargos. Registra símbolos y personas/órganos sin retrato, deduplicados entre décadas en `REVIEW-1920-1949.json`. El registrador actualiza huellas de seis recursos; después se sincroniza Países. El constructor no consulta servicios históricos en tiempo real.

El resaltado de selección utiliza `feature-state.selected` y opacidad de pintura. No aplicar `setFilter` al contorno seleccionado al cambiar de fecha: provoca reanálisis de la fuente compartida y el recorrido Rusia1920→1921 reprodujo índices de tesela incoherentes durante esa transición. La pintura por estado evita esa segunda actualización de geometría; el estado anterior se limpia al cerrar o cambiar el año. Se mantienen los diffs incrementales y las guardas de renderizado/clic existentes.

## Catálogo por entidad y ficha fija · 0.10

`Países/` es la vista de consulta por entidad de las colecciones preparadas. `scripts/prepare-country-catalog.mjs` genera `indice.json`, `INDICE.md` y `entidad.json` por carpeta. Las identidades históricas con QID distinto no se fusionan por similitud de nombres. Los datos científicos y sus licencias permanecen separados en `public/data`; las imágenes compartidas se referencian desde `public/media`. No editar el resumen generado ni mantener dos fuentes de verdad independientes. Regenerar después de adquirir/curar y antes de compilar.

Las entradas editables `recursos.json` y `archivos/` permiten incorporar audio/PDF por clave y vigencia. El preparador exige archivo real, fechas, fuente y licencia; el importador de Vite los descubre y `entity-resources.ts` los filtra por año para Datos. No hay reproducción automática ni descargas de proveedores durante la consulta. Las carpetas sin recursos no incorporan reproductores vacíos.

La ficha es una columna de altura limitada: identidad y pestañas quedan fuera de `.country-content`, único desplazamiento vertical interior. `main.ts` conserva/restaura la posición de ese contenedor al cambiar la fecha, no el scroll de toda la tarjeta. Cambiar de pestaña inicia su contenido arriba. Comparaciones permanecen dentro de su panel y conservan la misma delegación de eventos y guardas de solicitudes anteriores.

## Ampliación 0.6 · datos temporales

`historical-affiliations.ts` consume el catálogo local `affiliations.json`; `historical-context.ts` consume `historical-context.json`. Se importan como metadatos locales del build; no consultan proveedores al navegar. Membresías y eventos usan fin exclusivo; mandatos mantienen fin inclusivo. Las membresías del mapa se observan al cierre anual y las de Datos conservan todas las relaciones del año. Los eventos son fichas relacionadas, no beligerantes para una pintura automática.

`entityCode` permite unir entidades históricas a relaciones sin reutilizar códigos estadísticos de sucesores. `history.ts` conserva identidades YUG/FRY/SCG/CSK/SUN y selecciona la base de Crimea de 2013 para Rusia/Ucrania desde 2014; la ocupación es independiente. `data.ts` añade los contornos de referencia declarados y la ocupación anual de Kuwait. Cada recurso registra su transformación y licencia separadamente.

El buscador usa un panel no modal como las fuentes; sólo fecha y Acerca de usan el diálogo modal. La disposición, selección común de país, reloj local y control temporal se conservan. La deduplicación prioriza curación, precisión y título, mantiene renovaciones y separa cargos de partido de jefaturas nacionales.

## Aplicación inicial

Aplicación estática distribuida por CDN. El navegador mantiene fecha consultada, proyección y capas; el fragmento URL permite compartir fecha y vista. No se requiere servidor ni base de datos. Vite empaqueta TypeScript, estilos y worker de MapLibre. El worker se sirve desde el mismo origen que la aplicación.

`time.ts` es la lógica temporal pura. La posición del eje recorre tramos con distintas escalas, por lo que distancias iguales en pantalla no equivalen a duraciones iguales. La selección utiliza intervalos Cliopatria1700–1885, CShapes 1886–2019, referencia contemporánea desde 2020 e instantáneas discretas antes de1700. El máximo temporal procede del reloj del dispositivo; la fecha de referencia de los datos se conserva. Un periodo sin datos no hereda fronteras contemporáneas.

Desde 0.2.0 la rueda sobre la superficie de la regla sólo modifica su escala, anclada a la fecha central. El arrastre y el teclado recorren fechas. Los eventos de rueda se consumen dentro de esa superficie, mientras MapLibre conserva sus gestos sobre el mapa. Las marcas usan intervalos legibles por tramo y se generan para la ventana visible con margen; durante el arrastre se reutilizan hasta cambiar de bloque visible. El control fijo de fecha y reproducción es hermano del slider, evitando anidar botones interactivos dentro del rol ARIA de slider.

La colección superior contiene búsqueda, proyección, filtros, capas, fuentes/base de datos, pantalla completa, apariencia e información. El panel de capas es no modal, con foco inicial en cerrar, Escape y cierre exterior. Los diálogos completos comparten contenedor; `about.ts` aporta la identidad, ficha e historial del proyecto siguiendo la estructura de las otras aplicaciones del autor. La versión procede de `package.json`.

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


## Espacio de investigación de países · 0.7

La selección conserva un ancla semántica (`selection.ts`), no el ID de un polígono de un periodo. El commit del mapa vuelve a resolverla y renderiza la ficha con pestaña, filtros y lectura anteriores. Una entidad ausente conserva su ficha explicada; no se aproxima a un sucesor. La fecha no controla la visibilidad de paneles; sólo contenido/estado de carga. Comparaciones y cronologías tienen módulos separados y generación de solicitudes para descartar respuestas obsoletas.

Los dos inventarios nuevos se cargan por la caché compartida de assets, sin consultas al proveedor durante la visita. Se separan indicadores numéricos con unidades/definiciones/signos de registros editoriales fechados y relaciones dirigidas. Los gráficos son SVG accesibles con tablas y fechas navegables; no hay biblioteca de gráficos ni backend nuevos. Detalles en COUNTRY-WORKSPACE, COUNTRY-INDICATORS y COUNTRY-HISTORY.


## Particiones de control0.12.1

1940–1944 usa sustituciones preparadas del inventario político mediante wartime-partition.ts. CShapes aporta la tierra compartida; Cliopatria sólo cortes interiores. Una sola propiedad/control final alimenta mapa, fronteras, clic y búsqueda. Las franjas se recortan después de todas las transferencias, sin cambiar geometrías al activarlas. El loader atiende la partición antes de su atajo de controles vacíos; las visitas no hacen booleanas en ese tramo. Preparación y límites en [WWII-PARTITIONS](WWII-PARTITIONS.md).

Las notas largas de mandatos están enContexto, conservando una plantilla común de Autoridades. Suiza distingue office/authorityClass para colegio y presidencia anual; no fusionar esos cargos aunque coincida la persona. LosGIF originales son medios acreditados locales, verificados igual que los otros formatos.

## Filtros y sedes soberanas ·0.19

Filtros reúne forma/régimen, color y organizaciones, separado de Capas. Las opciones se derivan del inventario completo del año, antes de aplicar el filtro, y omiten recuentos cero. Un filtro activo sin coincidencias se conserva en el estado, con aviso externo al selector y acción de quitarlo. Los paneles conservan la fecha y accesibilidad de teclado.

`historical-places.ts` incorpora sedes soberanas cuando la fuente sólo ofrece un agregado imperial. Son puntos documentales separados de los polígonos; `sovereignSeat` permite abrir una ficha de entidad, comparar fechas y persistir al navegar. Su posición no se envía como geometría territorial ni como resaltado de polígono. Búsqueda y recuentos incorporan estas referencias sin duplicar una entidad con contorno propio.
