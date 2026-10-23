# Entrega 0.8.1 · estabilidad temporal y autoridades dependientes

El propietario detectó fichas sin nombre o datos después de viajar a una fecha anterior a 1970 y volver, y autoridades vacías en varios territorios dependientes. Son dos causas distintas.

## Corrección estructural

El recorrido de clics reales Francia/España 1970 → 1954 → 1970 → 1980 reproduce «Área del mapa». No faltaba el fichero de autoridades: la tesela perdía sus propiedades. `sourceDiff` enviaba `removeAllProperties` junto a `addOrUpdateProperties`. El código instalado de `@maplibre/geojson-vt` 6.3.0 retorna inmediatamente `{}` ante el primer indicador, omitiendo las adiciones; el modelo GeoJSON del hilo principal sí las conserva. Esto explicaba la divergencia entre búsqueda y clic, y los cambios de color erróneos.

Se envían eliminaciones explícitas de claves obsoletas, manteniendo actualizaciones incrementales, geometrías y resolución. `canonicalFeature` resuelve el clic por identificador contra la colección activa de territorios, controles o ciudades. Las teselas dibujadas no se utilizan como ficha bibliográfica. No se modifican bibliotecas instaladas ni se depende de parches locales de node_modules.

La prueba unitaria ejecuta las diferencias sobre el motor de teselas real y comprueba nombre, identidad, color y eliminación de metadatos obsoletos en ambos sentidos. La prueba de navegador reproduce la vuelta desde 1954 con clics reales y cambios de fuente actual/histórica. El año 1954 sirve para reproducir el error; no se declara ampliación bibliográfica de esa tanda.

La revisión visual detectó además un aviso de fallo que la comprobación del año cargado no veía. La excepción `feature index out of bounds` procedía de consultar polígonos inmediatamente después de actualizar la fuente, cuando aún había teselas del índice anterior. Se elimina esa consulta prematura: sólo el siguiente `idle` acredita geometría renderizada, se solicita repintado y los clics requieren esa acreditación. Las pruebas esperan dibujo y ausencia del estado de error, además del año. No se oculta una excepción con un valor genérico ni se confunde completar la descarga con completar el dibujo.

## Autoridades y territorio

Once relaciones fechadas en `territorial-administrations.json` complementan la cartografía. Se resuelve también el administrador documental de otras dependencias de la fuente. Una alianza o relación cromática de influencia no activa esta herencia. Las autoridades se separan entre territorio y Estado administrador; una presidencia portuguesa nunca se renombra como presidencia de Angola de 1970.

Se conservan gobiernos autónomos: Surinam muestra Sedney/Ferrier y la jefatura del Reino, sin sustituir su Gobierno por el primer ministro neerlandés. Bahamas muestra Pindling y la Corona antes de 1973; compartir monarca tras la independencia no activa dependencia. Puerto Rico mantiene su gobernador junto al presidente estadounidense. Los departamentos franceses muestran las autoridades francesas con su ámbito explícito. Namibia conserva la ilegalidad de la presencia sudafricana según ONU y no presenta reconocimiento de soberanía. Sáhara distingue autoridad estatal española, gobernador y la retirada de 1976; Franco no se prolonga después de su muerte.

Las relaciones que terminaron durante el año siguen visibles con su tramo y fuente. Recortar una autoridad al fin de administración no significa que dimitiera entonces en la metrópoli. Los límites de cobertura se rotulan. Si se usa un símbolo del Estado administrador por faltar el territorial histórico, el rótulo y el texto alternativo lo indican. Nunca se heredan PIB, población o alianzas de la metrópoli como si fueran datos territoriales.

Cinco mandatos focales: Fouché (Sudáfrica), Ferrier y Sedney (Surinam), Pindling anterior a la independencia y Pérez de Lema (Sáhara). Fouché y Sedney incorporan retratos con licencia propia; se reutilizan los otros medios disponibles sin atribuirles apariencia de 1970. La precisión anual del final de Sedney permanece explícita. Fuentes y series locales pendientes en DEPENDENCY-AUTHORITIES-RESEARCH.

Preparación: `prepare-dependent-authorities.py`, adquisición acotada `enrich-1970-portraits.py --people Q886942 Q924337`, `register-dependent-authorities.mjs`. No se reconstruye ni reemplaza el catálogo mundial. Referencia contemporánea conservada 22/10/2026. Inventario: 43 recursos de datos y 3.476 medios.

## Verificación y publicación

El primer recorrido de reproducción falla contra 0.8.0 y pasa después de corregir la actualización. El cierre público comprobado se detalla a continuación; no confundir resultados locales intermedios con la publicación.

Verificaciones locales de datos: 43 recursos, 11 franjas y 3.476 medios íntegros por SHA-256; 103 pruebas en 19 archivos y tipos correctos. La auditoría de autoridades comprueba también todas las colonias/protectorados/mandatos CShapes, año por año en 1970–2019. Esto acredita resolución de una autoridad estatal o local, no una serie completa de prefectos, gobernadores o autoridades rivales.

Los dos recorridos reforzados pasan tras corregir la consulta prematura: fichas dependientes/independencia y clics Francia/España de ida y vuelta. El refinamiento final conserva el fin documental completo de cada mandato, sin recortarlo innecesariamente al año consultado: pasan las cinco pruebas de dependencias y se repite correctamente su recorrido de navegador sobre la compilación final. Tipos/compilación correctos; 3.530 recursos preparados en Git verificados por SHA-256. La captura local de Angola ya no muestra aviso de carga fallida.

### Publicación verificada · 23/10/2026

Publicado **911f7c3c55466e4f757a271ec8f5ee740e5eea1b**. [Quality 39984546199](https://github.com/AlejandroPico/Historicmap/actions/runs/39984546199) correcto: 103 pruebas unitarias en 19 archivos, integridad, compilación y **26 recorridos de navegador** (12 minutos), incluidos los dos nuevos. [Publish atlas 39986404919](https://github.com/AlejandroPico/Historicmap/actions/runs/39986404919) correcto, checkout real del mismo SHA confirmado en el log de build.

Verificación pública a las 18:25 (Madrid): JS `index-BA5eVcf8.js`, CSS `index-b0OcPlkX.css`, tres manifiestos idénticos byte por byte, siete conjuntos históricos y cinco retratos más el símbolo portugués de referencia comprobados por SHA-256. Informe local ignorado `.cache/public-verification-0.8.1.json`. Incluye los dos retratos nuevos y la relación territorial que utiliza la ficha.

Revisión visual pública: Francia abierta en 1970 → 1954 → 1970 recupera Pompidou/Chaban-Delmas; cerrar y hacer clic real sobre Francia abre de nuevo su ficha completa y conserva color/nombre. Sin aviso de error. Surinam muestra Sedney/Ferrier y Juliana con ámbitos distintos; Angola muestra Caetano/Tomás como autoridades portuguesas. Evidencias reales `.cache/release-0.8.1-public-france-return.png` y `.cache/release-0.8.1-public-angola-1970.png`. La pestaña queda preparada con Angola en 1970. El cierre documental `[skip ci]` no modifica la aplicación o los datos validados.

## Límites

La sucesión completa de gobernadores/prefectos, autoridades rivales y todos los cargos secundarios sigue siendo parcial. La ficha lo explica; la ausencia de una autoridad local no oculta las estatales documentadas. La relación administrativa no certifica control efectivo sobre cada punto. Las limitaciones cartográficas y bibliográficas previas siguen vigentes.
