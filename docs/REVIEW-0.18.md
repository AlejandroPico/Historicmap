# Revisión1800–1900 y clasificación política ·0.18.0

El encargo combina corrección documental y herramientas de consulta. Esta entrega amplía las series disponibles y conserva una auditoría anual de los huecos; no declara completo el inventario mundial de banderas, gobernantes o fronteras.

## Identidades y autoridades

- Monarquía de Habsburgo: el Q66504140 de la fuente es una desambiguación. Se resuelve aQ153136, con FranciscoII en1800 y el Imperio de Austria desde1804. La proclamación de11/8/1804 y la abdicación imperial de6/8/1806 son hechos distintos. Referencia: [Die Welt der Habsburger](https://www.habsburger.net/en/persons/habsburg-emperor/franz-ii-i).
- Río de la Plata: Q35827 identifica al río, no a las Provincias UnidasQ738144. Se incorpora una identidad propia. En1820–1825 no se inventa una presidencia nacional: Las Heras figura como autoridad **provincial de Buenos Aires**, con observaciones interiores y alcance explícito. [Archivo General de la Nación](https://www.argentina.gob.ar/sites/default/files/junta_de_representantes.pdf), [Registro Nacional1824](https://cdi.mecon.gov.ar/greenstone/collect/registr1/index/assoc/HASH01ac.dir/doc.pdf).
- República Helvética: símbolo y Ejecutivo colegiado de1800; la denominación de la fuente no prolonga el régimen hasta1814. Desde1803 se resuelve aSuiza bajo la Mediación. [Diccionario Histórico de Suiza](https://hls-dhs-dss.ch/fr/articles/009797/2011-01-27/).
- El agregado colonial británico muestra autoridades del Estado administrador, distinguidas de los cargos locales. No se convierte el territorio metropolitano en colonia ni se inventa un gobernador único para todas las posesiones. [Canadian Heritage](https://www.canada.ca/en/canadian-heritage/services/crown-canada/governor-general.html). También se explicita la relación portuguesa en su agregado colonial.
- Revisión de títulos y sucesiones deLippe, Nassau, Hesse, Baden, Sajonia-Coburgo-Gotha, Wurtemberg, Sajonia y Sajonia-Weimar-Eisenach; recuperación de cargos moldavos y valacos. Las regencias y títulos electorales no se convierten en reinados. LuisIIdeHesse es la personaQ166701; se rechaza el objeto no humano de la página homónima. FedericoIdeBaden adquiere el título en1856, no1858: [proclamación de5/9/1856](https://digital.blb-karlsruhe.de/id/124866).
- Chile1824: Ramón Freire como director supremo, con su presidencia posterior separada. [Biblioteca Nacional de Chile](https://www.memoriachilena.gob.cl/602/w3-article-92159.html). Paraguay: Francia como dictador perpetuo desde30/5/1816, sin confundirlo con la dictadura temporal anterior: [Ministerio de Economía y Finanzas](https://www.mef.gov.py/sites/default/files/2024-07/pub007_0.pdf).
- Sokoto: sucesión de sultanes/califas, con identificadores locales para personas documentadas sin un enlace Wikidata verificado. Bornu distingue poder de facto y título deshehu. Wadai incorpora observaciones interiores de gobernantes; no rellena por interpolación las sucesiones contradictorias, especialmente1834–1843. Las tablas secundarias se conservan como tales, pendientes de contraste bibliográfico adicional.

El registro revisado conserva70 intervalos de cargos europeos/americanos y23 observaciones africanas, además de correcciones focales y autoridades administrativas heredadas con ámbito explícito. Son intervalos, no personas diferentes. Se adquirieron60 retratos adicionales. Las imágenes ausentes y los cargos locales pendientes siguen identificados en la auditoría.

## Símbolos

Las variantes tienen ventanas fechadas, licencia, autor y huellaSHA-256. El encabezado diferencia bandera, pabellón mercante, pabellón naval, colores dinásticos y estandarte. Las notas documentales quedan enContexto, sin alterar el formato común deAutoridades. Se conservan originales raster cuando una vectorización publicada advierte de calidad sin verificar.

Incluye los ejemplos señalados deHabsburgo, Sacro Imperio, Helvética, Papado, Imperio otomano, Nápoles, Gran Colombia, Perú y Río de la Plata, junto con Estados germanos y otras variantes. El ejemplar militar deGranColombia, ca1824, tiene [referencia material enICOM](https://icom.museum/es/object/bandera-de-la-gran-colombia-del-batallon-de-husares-del-centro-ca-1824-73-x-78-cm/).

Las candidatas no se adoptan sólo porque aparezcan enCommons:

- Wadai.png no aporta un testimonio histórico independiente que acredite su uso en1800–1900.
- La candidata deBornu describe una reconstrucción del atlas deVallseca de1439; no demuestra continuidad hasta el sigloXIX.
- El paño verde atribuido aSokoto tiene un aviso de fuente de insignia ausente. Los estandartes militares documentados no prueban una bandera nacional uniforme.
- La candidata valaca anterior a1834 está marcada como ficticia.

Estos casos permanecen abiertos; no se copian símbolos deDarfur o de un Estado vecino para ocultar el hueco. Aceptadas y rechazadas en[scripts/review-018-symbols.json](../scripts/review-018-symbols.json).

## Clasificación política

`governance.json` contiene una taxonomía ampliable y registros por entidad/intervalo. Separa forma institucional, organización territorial, evaluación del régimen, orientación y dependencia. Contempla monarquías, repúblicas, directorios, regencias, teocracias, organizaciones tribales, imperios, ducados, principados, electorados, sultanatos, califatos, dictaduras y sistemas electorales, entre otras categorías. No se afirma que esa lista sea exhaustiva de toda forma histórica.

El selector deCapas filtra entidades y ciudades, muestra cantidades, mantiene la categoría al viajar en el tiempo y admite cero resultados. Las etiquetas deInstituciones también permiten activar el filtro. Las entidades sin evidencia conservan «Sin clasificación documentada»: no se confunde ausencia de datos con ausencia de gobierno. Los polígonos y los colores históricos no cambian por esta clasificación.

La evaluación comparada se conserva aparte, en`regimes-of-world.json`: V-Dem2026v16, procesamientoOurWorldinData, observaciones1789–2025,209claves y30.851valores anuales comprimidos sin pérdida. [Fuente y metodología](https://ourworldindata.org/grapher/political-regime), [V-Dem](https://v-dem.net/data/the-v-dem-dataset/), DOI10.23696/vdemds26. LicenciaCCBY-SA4.0, independiente de las geometrías. Los ficheros de investigación conservanCSV y metadatos originales. Se documentan los cruces de entidades históricas y se excluye la evaluación heredada para colonias. **No se extrapola a2026.** Una república no se clasifica automáticamente como democracia.

## Ciudades, conflictos y selección

68referencias urbanas fechadas añaden capitales, cortes, sedes coloniales regionales y grandes ciudades anteriores a1886. Complementan las capitalesCShapes y las323ciudades contemporáneas. Se comprueba que la entidad exista en la fecha; no se proyectanTokio oBrasilia retrospectivamente. Las coordenadas son anclajes de referencia, no perímetros ni censos históricos.

32puntos añaden episodios documentados y referencias regionales de conflictos. Se distinguen visualmente las batallas de los anclajes regionales, con fecha, fuente y precisión. Son seleccionables y conservan su ficha al cambiar de año, indicando cuando el episodio deja de estar activo. Se corrigió la resolución de identificadores de puntos transformados por el renderizador, tanto para lugares como para conflictos.

«Ocupaciones y disputas» conserva las franjas de control existentes y añade esos puntos. Funciona también con colores económicos u organizaciones seleccionadas. Un punto de conflicto **no es un frente**: no se han inventado nuevas superficies de ocupación. Las geometrías originales y las particiones bélicas anteriores permanecen intactas.

## Continuidad y comprobación

Preparadores en `scripts/prepare-review-018.py`, `prepare-review-018-symbols.py`, `prepare-governance.py`, `prepare-historical-places.py` y `prepare-conflict-points.py`. Los datos revisados de autoridades/símbolos se conservan en JSON junto a los preparadores; las búsquedas y descargas no se ejecutan en la compilación ni durante la visita. El preparador de autoridades utiliza por defecto el registro revisado fijado; `--rebuild-research` reconstruye los candidatos europeos desde la caché. Si se renueva la investigación africana, ejecutar después `curate-018-african-observations.py` antes de integrar, para conservar las observaciones interiores. Ejecutar los escritores de autoridades, retratos y símbolos secuencialmente, nunca a la vez.

Validación final: 179 pruebas en 42 archivos, siete comprobaciones focales adicionales tras precisar límites de cobertura, tipos y compilación correctos. Tres recorridos de navegador en 2,5 minutos, con clics reales, globo, móvil, persistencia, filtros y capas combinadas. Integridad de 61 recursos de datos, 11 franjas tipográficas y 6.304 medios verificada. La compilación local usa el mismo código de producción con copia incremental de los recursos estáticos ya verificados.

La auditoría[REVIEW-1800-1900.json](REVIEW-1800-1900.json) recorre101años por la misma ruta de identidad que usa el mapa. Registra disponibilidad y huecos, no certifica todas las fronteras ni la corrección exhaustiva de cada declaración heredada. Las comprobaciones finales y el siguiente paso están en[tareas.md](../tareas.md). Publicación: comprobar localmente y subir, sin esperarActions/Pages, según instrucción del propietario.
