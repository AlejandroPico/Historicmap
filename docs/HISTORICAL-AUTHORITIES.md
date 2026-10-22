# Autoridades históricas · 1990–2026

Esta ampliación incorpora mandatos de jefatura de Estado y de Gobierno desde 1990 hasta la fecha de adquisición. Se distingue la cobertura de una compilación de una comprobación primaria mundial: Wikidata puede contener huecos, cargos omitidos, fechas imprecisas y afirmaciones antiguas todavía abiertas. Las curaciones nacionales de la entrega anterior se conservan.

## Preparación reproducible

`scripts/enrich-historical-authorities.py` es una adquisición incremental de preparación; la aplicación publicada no consulta Wikidata ni Commons. Parte del catálogo local, lee P35/P6 fechados del país y los cargos P1906/P1313, y recupera los mandatos P39 de sus titulares. Descarga nombres y P18 de los individuos, conservando créditos, licencia, origen y SHA-256 de cada imagen. Usa `.cache/identities/` para no repetir peticiones. `--skip-media` permite adquirir y auditar los mandatos sin descargar medios.

Los mandatos con inicio y cese se conservan con su precisión de origen. Un inicio sin cese no acredita vigencia hasta 2026: si existe otro titular posterior del mismo cargo, se fija un **límite superior**, identificado con `endIsUpperBound`, al día anterior al nuevo inicio. Eso no acredita la continuidad durante todo el intervalo. Si no hay sucesor, sólo se admite hasta la adquisición cuando la afirmación nacional actual documenta a esa persona como titular o una curación primaria previa ya lo hace. Los casos restantes se registran como pendientes y no se prolongan automáticamente.

Las afirmaciones preferidas prevalecen como prueba de incumbencia. Si no hay ninguna preferida, se considera el último inicio fechado y abierto de esa propiedad, evitando tratar dos gobiernos sucesivos como simultáneos por una omisión de cese. Los ceses P39 coincidentes corrigen afirmaciones nacionales más amplias; las curaciones primarias no se sobrescriben. Los mandatos históricos generados se reconstruyen de forma idempotente sin eliminar el resto del catálogo.

Las entidades desaparecidas tienen claves y fechas propias: URSS, RDA, Checoslovaquia, Yugoslavia socialista, República Federal de Yugoslavia, Serbia y Montenegro y Yemen del Norte/Sur. Los cargos se limitan a la vida de la entidad correspondiente. No se asignan los gobernantes de los sucesores a sus predecesores ni se deducen fechas por ciclos electorales.

## Sáhara Occidental

La [ONU incluye al Sáhara Occidental entre los territorios no autónomos desde 1963](https://www.un.org/dppa/decolonization/en/nsgt/western-sahara). La [MINURSO describe el proceso, las partes y la interrupción del alto el fuego en noviembre de 2020](https://minurso.unmissions.org/en/node/520). Por ello SAH conserva la identidad territorial Q6250 y se distingue de RASD Q40362. Se muestran las autoridades saharauis de la RASD/Frente POLISARIO y las autoridades nacionales marroquíes para la zona administrada por Marruecos con roles expresamente distintos. Su presencia en la ficha no adjudica soberanía, reconocimiento internacional ni control de toda la superficie.

Como contraste focal de las sucesiones saharauis: la [ONU comunicó la muerte de Mohamed Abdelaziz el 31 de mayo de 2016](https://www.un.org/sg/en/content/former-secretary-general/statement/2016-05-31/statement-attributable-the-spokesman-for-the-secretary-general-the-death-of-mohamed-abdelaziz); la [presidencia argelina, publicada por su radio pública, felicitó la elección de Brahim Ghali en julio de 2016](https://radioalgerie.dz/news/fr/node/83043). La [Embajada de Argelia recoge el comunicado de nombramiento de Bouchraya Hamoudi Beyoun y el cese de Mohamed El-Ouali Akeik del 13 de enero de 2020](https://www.emb-argelia.pt/sahara-occidental-le-president-ghali-nomme-bouchraya-hamoudi-beyoun-premier-ministre/). Elección, toma de posesión y mandato son fechas diferentes; los registros preservan la fecha de la afirmación concreta.

## Medios y límites

Se reutilizan los medios locales existentes antes de descargar nuevas fotografías. Sólo se aceptan licencias identificadas y compatibles con su reproducción, con atribución individual. La fotografía institucional de Mozambique con licencia sin obras derivadas conserva su archivo original, formato completo, crédito y enlace de licencia; esta adquisición no la transforma ni sustituye. Una imagen P18 ilustra a la persona, no necesariamente la apariencia que tenía durante el año consultado. La ausencia de imagen se conserva como tal y no se reemplaza por personas homónimas ni imágenes generadas.

El informe de adquisición local `historical-authorities-audit.json` contiene métricas por cada año, correcciones, ceses abiertos no resueltos, personas sin retrato y distribución de licencias. Las cifras y comprobaciones finales de la adquisición se registran a continuación. No equivalen a una validación historiográfica exhaustiva de todos los cargos, administraciones coloniales, poderes de facto, gobiernos rivales o cambios ocurridos dentro del año.


## Cierre de adquisición · 22 de octubre de 2026

Catálogo final: **274 claves y 5.781 registros de mandato** de todas las épocas. En el intervalo 1990–22/10/2026 aparecen **2.925 personas o autoridades colectivas distintas**, de las que **2.432 tienen imagen y 493 no**. No son 2.925 series nacionales completas. El manifiesto contiene **2.871 medios**: 376 banderas/símbolos SVG y 2.495 fotografías raster (2.494 retratos y una fotografía institucional completa). Suman 121.844.024 bytes. Los archivos pueden ilustrar a más de un mandato y los registros pueden citar a la misma persona varias veces.

En 2026 la ampliación recoge **437 autoridades distintas durante el año, 422 con imagen**, en 233 claves del catálogo. El número incluye mandatos breves, entidades colectivas, territorios y autoridades rivales; no equivale a 437 gobernantes actuales simultáneos ni a 233 Estados soberanos. Cambia el alcance respecto al inventario de 0.5: no comparar las cifras como si fueran el mismo conjunto fijo. Quedan sin foto en esa referencia anual: Gervais Ndirakobuca, Vladimiro Selva, Italo Righi, Lindsay de Sausmarez, Nestor Ntahontuye, Herintsalama Rajaonarivelo, Alice Mina, William Casali, Gerardo Giovagnoli, Shawn Christian, Konstantín Busygin, Haibatulá Ajundzadá, Denise Bronzetti, Rui Duarte de Barros y Charlene Warren-Peu. Baikonur y Pitcairn son las únicas claves con mandatos en 2026 sin ninguna imagen anual.

La adquisición recuperó 3.521 filas P39 de 425 cargos, además de afirmaciones nacionales. El primer pase corrigió 131 registros importados con ceses más precisos; no son 131 personas ni países. Se elimina también una afirmación sin fechas que situaba a Edgar Lungu, fallecido antes de 2026, en el presente. El último inventario conserva **39 mandatos abiertos no extendidos** por falta de prueba de incumbencia y **38 afirmaciones heredadas de vigencia que requieren contraste**. Estas últimas incluyen cargos colectivos, duplicados y afirmaciones sin inicio, por lo que no constituyen 38 errores acreditados. Los casos sin inicio permanecen limitados a la adquisición y no se proyectan a 1990.

La ausencia de imagen comprende 416 personas sin P18 documentado en la adquisición y 77 con candidato P18 sin reproducción utilizable incorporada (licencia, tipo de archivo o descarga). Commons respondió con límites de tasa durante la adquisición; se hizo un reintento pausado y se cerró con los vacíos expresos. No se reintenta indefinidamente ni se considera que P18 otorgue una licencia por sí solo.

### Curaciones focales y reproducción

Orden incremental de esta entrega: `enrich-historical-authorities.py` → `enrich-historical-flags.py` → `curate-historical-authorities.py` → registro de manifiesto → verificación. Los informes de adquisición en `.cache/` son diagnósticos locales; la evidencia pública se conserva en identidades y manifiesto de medios. No ejecutar únicamente la adquisición inicial como sustitución del catálogo ampliado.

El tercer script repara catorce etiquetas QID sin texto que ocultaban nombres válidos, entre ellos Felipe Calderón; contrasta que las entidades curadas sean personas Q5 antes de adquirir su retrato; completa Brunei desde 1967/1984, Rodríguez–Wasmosy–Cubas en Paraguay, las administraciones interina/transitoria y la presidencia de Hamid Karzai, y las jefaturas de partido de Jiang Zemin, Hu Jintao y Xi Jinping. También distingue el título de State President de Frederik de Klerk, que concentraba Estado y Gobierno. El archivo original de Mozambique permanece byte a byte y con los mismos metadatos que en 0.5.

Contrastes focales: [Brunei, Ministerio de Finanzas](https://www.mof.gov.bn/minister-of-finance/), [Oficina del Primer Ministro](https://www.pmo.gov.bn/prime-minister/), [Acuerdo de Bonn y transferencia del 22/12/2001](https://2001-2009.state.gov/p/sca/rls/6675.htm), [Gobierno británico, sucesión afgana del 29/9/2014](https://www.gov.uk/government/news/foreign-secretary-welcomes-inauguration-of-new-president-of-afghanistan), [Presidencia sudafricana, historia institucional](https://www.presidency.gov.za/history), [Gobierno chino, biografía de Jiang Zemin](https://english.www.gov.cn/news/topnews/202212/02/content_WS6389d626c6d0a757729e3f58.html). Los restantes mandatos procedentes de Wikidata conservan su referencia de compilación y no se presentan como contraste primario individual exhaustivo.

### Cierre de los vacíos focales

Se añaden nueve registros focales tras comprobar la selección cartográfica anual. Sassou-Nguesso conserva separada su primera etapa presidencial y André Milongo aparece como primer ministro de transición en los años 1991–1992; las fuentes son la [cronología de la Embajada del Congo](https://ambacongogabon.wordpress.com/chronologie-des-presidents-du-congo/) y el [informe contemporáneo del Banco Mundial](https://documents1.worldbank.org/curated/en/925951511187348004/pdf/multi0page.pdf). Donde sólo se acredita el año se usa `precision:9` y se indica que el extremo de calendario no es un nombramiento/cese exacto ni presencia durante el año completo.

Rabbani conserva la presidencia documentada por P39 entre el 28/6/1992 y el 22/12/2001. Desde 1996 su ficha distingue Gobierno reconocido internacionalmente/control variable de las autoridades talibanes que también se muestran; no se representa como dirigente efectivo de toda la superficie. Hekmatyar se documenta en 1993–1994 con precisión anual a partir de la [publicación institucional canadiense](https://publications.gc.ca/collections/collection_2016/grc-rcmp/PS64-129-2016-eng.pdf), sin confundir acuerdo de designación de marzo con investidura posterior ni inventar aquí un día de comienzo.

La [biografía del Ministerio de Exteriores tayiko](https://www.mfa.tj/en/main/view/2422/the-founder-of-peace-and-national-unity-leader-of-the-nation-president-of-the-republic-of-tajikistan) acredita la elección de Rahmon como presidente del Consejo Supremo el 19/11/1992. La [conmemoración oficial de ese Ministerio](https://mfa.tj/tg/main/view/1808/ruzi-prezidenti-jumhurii-tojikiston) acredita el juramento presidencial del 16/11/1994; se separa de la elección del 6/11/1994 y se prefiere al 19/11 consignado en P39. La continuidad posterior procede del catálogo vigente. Se incluye a Pérez Balladares entre el 1/9/1994 y el 1/9/1999 con referencia a la [publicación del INED del Tribunal Electoral panameño](https://libros.ined.ac.pa/index.php/eined/catalog/download/3/3/22).

Gadafi aparece como dirigente **de facto**, separado del secretario general del Congreso General del Pueblo, la jefatura formal de Zanati. El final de facto del 23/8/2011 corresponde a la caída del poder en Trípoli, no a su muerte en octubre. Para Zanati se conserva precisión anual al inicio porque la afirmación P39 dice enero de 1992 y otras cronologías sitúan el nombramiento en noviembre; no se presenta ese día como verificado. Estas dos referencias siguen siendo compilaciones Wikidata identificadas. Las curaciones focales reutilizan las fotografías ya incorporadas y se hizo un último intento acotado sobre los cinco candidatos P18 identificados: Gadafi (CC BY-SA 3.0), Milongo, Hekmatyar, Zanati y Pérez Balladares (dominio público) ya tienen fotografía local, autoría y licencia en el manifiesto. No se repitió la adquisición mundial. La opción `--bounded-media` limita cada descarga focal a un intento y veinte segundos; `--reuse-media-only` conserva exclusivamente las imágenes ya disponibles.

### Banderas

El importador complementario usa P163/P18 y fechas de adopción/inicio, sigue diseños predecesores explícitos y conserva por delante los intervalos P41 ya fechados. Rechaza intervalos de fuente contradictorios. Para diseños históricos no cubiertos por la identidad genérica se incorporan archivos específicos de Commons: Sudáfrica anterior a 1994, Zaire/Congo, Siria, Libia, Irak, Afganistán, Mongolia, Camboya, Albania y Birmania. Los rangos de archivo que sólo acreditan años se usan como **periodización anual**, no como fecha exacta de adopción; un diseño posterior con día documentado tiene precedencia. El catálogo cubre 197 claves con símbolo al cierre de 1990 y 242 a la referencia de 2026; persisten variantes históricas sin documentar y países sin bandera para ciertos años.

### Cobertura por año

Las claves son entradas de identidad con algún mandato; incluyen territorios, entidades desaparecidas y bandos. Personas y fotografías se deduplican por QID dentro de cada año. Los registros conservan cargos distintos y fuentes paralelas, de ahí que su número supere el de personas. Las banderas corresponden al cierre anual o a la fecha de adquisición en 2026.

| Año | Claves con mandato | Registros | Personas/autoridades | Con imagen | Claves con bandera |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1990 | 215 | 524 | 352 | 294 | 197 |
| 1991 | 221 | 571 | 398 | 322 | 199 |
| 1992 | 222 | 571 | 398 | 326 | 203 |
| 1993 | 221 | 603 | 410 | 337 | 203 |
| 1994 | 221 | 595 | 406 | 334 | 203 |
| 1995 | 222 | 569 | 386 | 322 | 204 |
| 1996 | 222 | 610 | 418 | 344 | 206 |
| 1997 | 223 | 608 | 418 | 347 | 207 |
| 1998 | 222 | 608 | 409 | 350 | 209 |
| 1999 | 224 | 623 | 436 | 373 | 214 |
| 2000 | 225 | 615 | 428 | 370 | 214 |
| 2001 | 224 | 607 | 426 | 353 | 215 |
| 2002 | 226 | 602 | 421 | 360 | 218 |
| 2003 | 227 | 638 | 433 | 374 | 218 |
| 2004 | 226 | 634 | 446 | 385 | 221 |
| 2005 | 227 | 627 | 428 | 381 | 222 |
| 2006 | 227 | 614 | 430 | 387 | 223 |
| 2007 | 226 | 637 | 432 | 388 | 224 |
| 2008 | 226 | 619 | 425 | 389 | 225 |
| 2009 | 226 | 619 | 428 | 385 | 226 |
| 2010 | 226 | 622 | 423 | 387 | 227 |
| 2011 | 227 | 643 | 440 | 406 | 229 |
| 2012 | 228 | 659 | 454 | 419 | 229 |
| 2013 | 228 | 636 | 430 | 399 | 231 |
| 2014 | 228 | 681 | 450 | 420 | 231 |
| 2015 | 227 | 657 | 431 | 401 | 231 |
| 2016 | 227 | 669 | 441 | 414 | 231 |
| 2017 | 228 | 660 | 428 | 402 | 232 |
| 2018 | 227 | 676 | 432 | 401 | 232 |
| 2019 | 228 | 694 | 447 | 419 | 232 |
| 2020 | 228 | 691 | 437 | 414 | 232 |
| 2021 | 228 | 713 | 448 | 429 | 233 |
| 2022 | 228 | 726 | 444 | 423 | 232 |
| 2023 | 228 | 668 | 423 | 409 | 233 |
| 2024 | 227 | 699 | 442 | 424 | 233 |
| 2025 | 227 | 676 | 440 | 420 | 233 |
| 2026 | 233 | 666 | 437 | 422 | 242 |

### Auditoría vinculada a la cartografía

No se usa 274 como denominador de Estados visibles: el catálogo incluye otras entidades y épocas. La comprobación con el resolver efectivo de identidad encuentra una autoridad para **150/150 Estados independientes representados por CShapes en 1990, 170/170 en 2000 y 173/173 en 2010** tras los alias de Bosnia y Kosovo. CShapes omite Estados pequeños y no representa todos los poderes rivales, por lo que esta cifra no certifica cobertura política mundial completa. En Natural Earth, 2026 tiene 232 de 258 entidades territoriales con autoridad; las 26 restantes comprenden áreas disputadas, bases, territorios deshabitados y algunas administraciones dependientes, no 26 Estados sin gobernante. Antártida o Bir Tawil no deben recibir un presidente ficticio para subir un porcentaje.

La auditoría detectó vacíos puntuales en Congo 1991; Afganistán y Tayikistán 1993–1995; Panamá 1995–1998; Libia 1995–1996 y Somalia 1998–1999. Los cinco primeros se completan mediante las curaciones focales descritas. Somalia se resuelve mediante una explicación institucional documentada de ausencia de Gobierno central en la ficha y el contexto, sin inventar un presidente. La prueba final recorre todos los Estados independientes CShapes en cada año de 1990 a 2019 y exige autoridad o ausencia institucional documentada. Estos contrastes evitan fichas nacionales vacías, sin certificar todos los titulares secundarios de cada año. También quedan administraciones de territorios dependientes, dirigentes de facto, imágenes y banderas históricas sin resolver. No declarar revisados manualmente los 37 años de todos los países por haber adquirido un lote de cargos o superado las pruebas.

### Comprobaciones de datos realizadas

Se comprobaron SHA-256 y tamaño de los 2.871 medios, los 2.495 raster con Pillow, todos los intervalos y referencias a archivo de autoridades/banderas y la conservación exacta de la fotografía institucional de Mozambique. Los tres scripts nuevos pasan compilación de Python. Las pruebas de aplicación, representación cartográfica y publicación se registran separadamente en la entrega general.

### Licencias del manifiesto final

| Licencia | Archivos |
| --- | ---: |
| Attribution | 128 |
| CC BY 2.0 | 244 |
| CC BY 2.0 cl | 1 |
| CC BY 2.5 | 11 |
| CC BY 2.5 ar | 3 |
| CC BY 2.5 bg | 7 |
| CC BY 2.5 br | 1 |
| CC BY 2.5 dk | 20 |
| CC BY 3.0 | 113 |
| CC BY 3.0 au | 1 |
| CC BY 3.0 br | 41 |
| CC BY 3.0 cl | 9 |
| CC BY 3.0 de | 5 |
| CC BY 3.0 it | 2 |
| CC BY 3.0 pl | 4 |
| CC BY 3.0 th | 1 |
| CC BY 4.0 | 475 |
| CC BY-NC-ND 3.0 RS | 1 |
| CC BY-SA 2.0 | 140 |
| CC BY-SA 2.0 fr | 2 |
| CC BY-SA 2.5 | 11 |
| CC BY-SA 3.0 | 202 |
| CC BY-SA 3.0 at | 1 |
| CC BY-SA 3.0 au | 2 |
| CC BY-SA 3.0 de | 15 |
| CC BY-SA 3.0 hr | 1 |
| CC BY-SA 3.0 nl | 6 |
| CC BY-SA 3.0 pl | 12 |
| CC BY-SA 4.0 | 233 |
| CC0 | 80 |
| European Parliament | 24 |
| GODL-India | 15 |
| KOGL Type 1 | 10 |
| OGL 3 | 19 |
| OGL v1.0 | 26 |
| OGL-om 1.0 | 2 |
| PDM-owner | 1 |
| Public domain | 1002 |
