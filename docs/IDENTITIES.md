# Identidades políticas, banderas y autoridades

## Catálogo y alcance

La entrega 0.4 incorpora `public/data/identities.json`, consultado el **22 de octubre de 2026**: 267 claves de entidad y 2.859 registros de autoridades. Son registros de mandatos, cargos y procedencias, no 2.859 personas diferentes ni 267 series históricas completas. Se incluyen metadatos de Estados y territorios de Natural Earth, entidades históricas focales y los dos bandos españoles. La cobertura temporal mundial es desigual: no se ha validado manualmente cada titular de todos los países desde 1789.

Las banderas y retratos se guardan en `public/media/`, con autoría, título, página original, licencia, tamaño y SHA-256 en su manifiesto. Esta adquisición incorpora **417 archivos: 342 banderas/símbolos y 75 retratos**, con 374 intervalos de símbolos en el catálogo (un archivo puede servir a varios periodos). No hay consultas a Wikidata o Commons durante una visita: la aplicación utiliza los datos locales. Las imágenes ausentes no se sustituyen por fotografías generadas ni por la de otra persona.

## Selección temporal

`src/identities.ts` resuelve la identidad a partir de la clave política, el código del territorio, el nombre de origen o Wikidata. Selecciona mandatos y símbolos por intervalos inclusivos. Desde 0.5 los mandatos se seleccionan si intersectan el año completo, hasta el día del dispositivo/adquisición en el presente. El símbolo sigue correspondiendo al 31 de diciembre o fecha de referencia. Se prioriza dentro de cada tipo de autoridad a quien seguía en funciones a esa referencia, con etiqueta explícita; se conservan los anteriores del mismo año. Un reloj futuro amplía la navegación, pero no fabrica titulares o banderas futuras.

Las declaraciones actuales sin fecha inicial sólo se admiten en la fecha de consulta; no se trasladan a todo el pasado. Las declaraciones con precisión de año o mes se conservan como tales. Los mandatos históricos obtenidos de las consultas de cargos conservan las fechas publicadas por la fuente; no se deducen de ciclos electorales. Las fuentes con periodos incompletos pueden dejar vacíos. La ausencia se indica en la ficha.

Se distinguen jefatura del Estado, del Gobierno y autoridad efectiva. Se consolidan las declaraciones duplicadas de la misma persona para evitar repetir un retrato por cada propiedad de Wikidata; un mandato focal documentado tiene prioridad sobre uno genérico. Autoridades distintas permanecen separadas: Azaña/Negrín en la zona republicana, monarca/presidente del Gobierno cuando corresponde, o Pétain/de Gaulle como autoridades rivales. Los dos bandos españoles tienen fichas propias; Franco no se atribuye a una zona republicana.

Un código de Estado contemporáneo no acredita el gobernador de una colonia. Los registros de colonia, protectorado y mandato sin identidad colonial documentada no heredan automáticamente dirigentes del Estado independiente actual. Los polígonos de ocupación muestran la autoridad de la potencia controladora y su contexto; no afirman reconocimiento de soberanía.

## Fuentes

- [Wikidata](https://www.wikidata.org/), metadatos **CC0**: declaraciones P6/P35 con fechas, P39 de titulares de cargos seleccionados, P41 de símbolos y P18 de imágenes. La preparación conserva cargos, intervalos, precisión y enlaces; no adopta sin revisión una etiqueta actual para una época anterior. Los datos importados no son una fuente primaria homogénea y requieren contraste por regiones.
- [La Moncloa, presidentes del Gobierno](https://www.lamoncloa.gob.es/presidente/presidentes/Paginas/index.aspx), nombramientos del BOE enlazados y archivos del Ministerio de Cultura: sucesión española reciente y Transición. Se conserva también el breve periodo en funciones de Fernando de Santiago en julio de 1976; al consultar el cierre de 1976 aparece Adolfo Suárez.
- [Casa Blanca, Donald J. Trump](https://www.whitehouse.gov/administration/donald-j-trump/): contraste del titular actual. La serie histórica estadounidense se obtiene de mandatos fechados, desde Washington, y conserva las presidencias no consecutivas y los relevos por fallecimiento o dimisión.
- [Cancillería federal alemana](https://www.bundeskanzler.de/bk-en/federal-chancellery/federal-chancellors-since-1949), Deutsches Historisches Museum, Haus der Geschichte y [USHMM](https://encyclopedia.ushmm.org/content/en/article/adolf-hitler-1933-1939): dirigentes, régimen nazi, división y posguerra. Se conserva la bandera alemana de 1935–1945 como documento histórico auténtico. En 1945–1948 no se muestra una bandera nacional de una RFA/RDA todavía inexistente; la ficha explica la administración militar aliada.
- Asamblea Nacional francesa y Fondation Napoléon: autoridad colectiva de la Convención y el Directorio, Consulado e Imperios; no se inventa un presidente individual para órganos colegiados. La monarquía anterior a la Revolución se representa con un **estandarte real**, identificado como tal, no con la bandera tricolor posterior.
- Gobierno e institución imperial japoneses: denominaciones y mandatos de la época. Para China se distinguen República de China, liderazgo comunista y República Popular; la jefatura del partido no se renombra automáticamente como presidencia.
- [Wikimedia Commons](https://commons.wikimedia.org/): archivos originales de banderas y miniaturas de fotografías/retratos reales. Cada archivo conserva su licencia propia (dominio público, CC BY o CC BY-SA, entre las admitidas), autoría y página de descripción. **CC0 de Wikidata no se aplica a las imágenes.** Los SVG se conservan sin estilización; las fotografías son miniaturas servidas por Commons, sin generación artificial.

## Reconstrucción y verificación

Ejecutar `scripts/prepare-identities.py` con Python. Descarga y conserva en `.cache/identities/` las entidades, consultas de cargos, nombres/imágenes y metadatos de Commons; las descargas existentes se reutilizan. Los cargos focales y sus fuentes explícitas se mantienen en el preparador. Las consultas en lote reducen solicitudes; los medios sin licencia identificada o no disponibles se omiten y registran en la salida. Los límites de servicio pueden impedir una descarga y no deben convertirse en un marcador ficticio.

Después ejecutar `node scripts/register-political-data.mjs` y `npm run data:verify`. El segundo valida huellas, referencias de imágenes y coherencia de intervalos. `tests/identities.test.ts` comprueba presidencias estadounidenses, sucesión española, Alemania/ocupación/RDA, bandos españoles, Francia revolucionaria/Napoleón, Stalin, China y ausencia de extrapolación. No certifica todos los registros globales.

## Límites y prioridades

Completar gobernadores y autoridades de dependencias, predecesores de Estados modernos, autoridades territoriales rivales y todas las variantes de símbolos; contrastar las declaraciones globales con archivos institucionales por regiones. Los retratos no están disponibles para todos los dirigentes. El atlas mantiene el nombre cuando hay documentación y omite la imagen cuando falta. La fecha de la fotografía puede diferir de la fecha consultada: el retrato identifica a la persona, no pretende mostrarla fotografiada cada año.

La geometría de cuatro zonas aliadas individuales, Berlín y otras administraciones de ocupación sigue pendiente; una ficha correcta no acredita esa geometría. Las fechas de autoridades al cierre del año y los frentes anuales sin día uniforme son evidencias distintas y se explican por separado.


## Ampliación 0.5

El inventario se actualiza a **2.858 registros de autoridades** y **830 medios** (342 banderas/símbolos y 488 retratos). Para 2026 hasta el 22 de octubre: 508 registros, 413 personas u órganos y 402 con foto en 231 claves. Son recuentos de fuente antes de consolidar declaraciones repetidas en la ficha. Se añaden 413 retratos respecto a 0.4. Felipe VI, Juan Carlos I y Franco disponen de imagen adjunta en todos sus registros focales.

El procedimiento, contraste primario de actualidad, once personas pendientes de imagen y fuentes figuran en [CURRENT-AUTHORITIES](CURRENT-AUTHORITIES.md). No confundir archivos, personas, cargos y países. Las correcciones cierran declaraciones obsoletas; los ceses conocidos sólo por límite superior se señalan expresamente y no se presentan como dimisiones exactas.

Un QID vacío/no válido no identifica a nadie. Esto corrige la contaminación con España republicana cuando una entidad carecía de código reconocido. La ficha por pestañas utiliza el mismo resolver para clic cartográfico y búsqueda. El índice de perfiles separa además territorios asociados de Estados: Brasil no es Isla Brasilera, ni Francia Clipperton.
