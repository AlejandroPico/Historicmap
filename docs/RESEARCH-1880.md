# Ampliación 1880–1899 y correcciones notificadas

Preparación: 25/10/2026. La referencia contemporánea sigue siendo 22/10/2026. Esta ampliación incorpora fuentes y contraste focal; no acredita una reconstrucción diaria mundial completa.

## Cartografía e identidad

Cliopatria aporta el inventario 1880–1885; CShapes comienza en 1886. Los archivos originales permanecen intactos. `historical-1880-entities.json` corrige nombres y QID anacrónicos, incluidos Haití, Dinamarca, Zanzíbar, Serbia, Brasil y Joseon. Un nombre corregido no valida todas las fronteras de su fuente. No se asignan indicadores actuales a imperios o entidades predecesoras.

Nueve referencias separadas completan omisiones. Hawái usa el contorno Cliopatria de 1885 únicamente hasta 1897. Desde 1898 existe un registro CShapes: su geometría exacta se transfiere a la entidad estadounidense. Se evita intersectar dos costas distintas, que dejaban fragmentos residuales. La transferencia de agosto de 1898 es distinta de la fecha de inicio del registro de fuente y de la admisión como Estado en 1959. No hay una sobrecapa opaca.

Groenlandia se añade como contorno contemporáneo Natural Earth de referencia en 1886–2019, porque CShapes la omite. Sigue siendo una entidad seleccionable propia vinculada a Dinamarca. Las notas distinguen las etapas de 1953, 1979 y 2009, sin inventar independencia ni ocupación alemana al ocupar Dinamarca. Antes de 1886 se mantiene la geometría disponible en Cliopatria.

## Autoridades, medios y contexto

La adquisición aislada sólo fusiona 1880–1899. Se aplican curadores regionales puros e idempotentes; los retratos se reutilizan por persona sin modificar fechas posteriores. Las fichas anuales de Brasil 1889 y Hawái 1893/1894 conservan las autoridades predecesoras con etiqueta explícita. Joseon y el Imperio coreano no se confunden.

Fuentes y límites: [Europa](AUTHORITIES-1880-EUROPE.md), [Américas](AUTHORITIES-1880-AMERICAS.md), [Asia y África](AUTHORITIES-1880-ASIA-AFRICA.md), [huecos regionales](AUTHORITIES-1880-GAPS.md), [contextos](CONTEXT-1880-RESEARCH.md). Se añaden 23 fases, 20 registros y seis enlaces, preservando los existentes. La Triple Alianza añade sus tres intervalos anteriores a 1900; intercambio de ratificaciones y firma son actos distintos. No se deduce subordinación de una alianza.

52 ventanas conservadoras de símbolos usan SVG originales con licencia individual y prevalidación de metadatos. Se mantienen diferencias entre banderas nacionales, civiles y enseñas mercantes. Las variantes Qing anteriores a 1889 y varios usos imperiales rusos siguen pendientes; no se rellenan automáticamente con banderas contemporáneas. Fuentes americanas: `scripts/symbols-1880-research.json`; otras familias continúan la investigación documentada en SYMBOLS-1900.

## Correcciones solicitadas fuera de la nueva ventana

Se retiran Phil Baker de EEUU y David del Reino Unido: son personajes ficticios asociados por la fuente a cargos reales. El motor exige clasificación humana y excluye personajes ficticios antes de inferir sucesores. Se conserva una lista explícita de exclusiones y pruebas sin conexión.

Se sustituye la imagen generada ajena de Ali al-Zaidi, el billete de Bután y el retrato anterior de Rasulzoda. Se incorporan los retratos de Bangladesh/Vietnam 2016, Francia 1900, siete personas de la serie nepalí y todos los huecos detectados de India. Las imágenes se guardan con licencia y huella; las rechazadas sin referencias se retiran del inventario de medios. Irak, Mozambique y Vietnam conservan correcciones temporales separadas y documentadas.

El presidente mozambiqueño Daniel Chapo ya tiene un retrato individual correcto. La escena con dos personas corresponde a Maria Benvinda Levi, primera ministra, con Đuro Macut. Sigue pendiente una imagen individual reutilizable; no se recorta su fotografía con licencia sin modificaciones. También queda pendiente confirmar la procedencia institucional exacta del candidato de Nagendra Prasad Rijal. Ver [investigación de imágenes](MEDIA-CORRECTIONS-0.13.md). La ausencia de imágenes verificadas no se resuelve con retratos generados.

## Auditoría nominal y pendientes

La ruta real del cargador, composición territorial y resolver recorre 2.723 entidades/año. Quedan 123 casos anuales sin autoridad resuelta, 40 personas u órganos sin retrato y 530 casos anuales sin símbolo. El inventario nominal se conserva en [REVIEW-1880-1899.json](REVIEW-1880-1899.json). Los casos sin autoridad se concentran en las entidades regionales del inventario temprano; algunos son faltas investigables y otros contornos compuestos cuya atribución homogénea sería falsa. No equivalen a territorios sin población ni gobierno.

La lista incluye Wadai, Sokoto, Champasak, Jabal Shammar, Terengganu, Kelantan, Bornu, Lunda, Bima, Aceh y otras entidades; también Bhután antes de la monarquía hereditaria y referencias coloniales de cronología ambigua. Las series locales, regencias y titulares breves requieren más investigación. Conservar estos pendientes al continuar, junto a los frentes y límites territoriales ya documentados en entregas anteriores.

## Orden reproducible

Adquisición aislada → curadores regionales → curadores de huecos → correcciones notificadas → retratos → símbolos → predecesores → preparadores de entidades/referencias/contexto → `prepare-1880-islands.ts` → auditoría de producción → registro de manifiestos → catálogo Países → integridad/tipos/pruebas/compilación/navegador. Ejecutar los escritores de identidades/medios secuencialmente. Los preparadores anteriores no deben borrar correcciones posteriores.

La entrega termina al confirmar el envío a Git; el propietario verifica después el despliegue. No sondear Actions/Pages.
