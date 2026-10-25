# Partición territorial compartida1940–1944 ·0.12.1

Corrección del25/10/2026. La publicación0.12.0 reproducía los errores: sus bytes públicos de manifiesto, controles y referencia1939 coincidían con los locales. El arreglo anterior1938–1939 no corregía1940–1944.

## Causas y solución

Los contornos originales de control contienen celdas y grupos de celdas remotos, incluidos puntos enSuecia, Karelia, Italia y Oriente Próximo. Además, unir directamente toda su geometría al país introducía una segunda costa, independiente deCShapes. Las franjas se generaban antes de terminar las transferencias y podían seguir cubriendo un régimen cliente posterior. Diagnóstico y fuentes institucionales en [WWII-CONTROL-RESEARCH](WWII-CONTROL-RESEARCH.md).

`wartime-partitions.json` contiene cinco sustituciones anuales del inventario político. Cada sustitución elimina los identificadores afectados e incorpora sus nuevas geometrías. **Clic, búsqueda, relleno y fronteras usan ese único inventario.** Ningún relleno opaco de ocupación se superpone al país anterior. Las franjas opcionales se generan después, intersectando únicamente territorio del controlador final con el territorio documental ocupado. Desactivarlas no cambia fronteras ni selección.

Los controles transfieren exclusivamente tierra de la mallaCShapes fechada, con las referencias ya incorporadas para sus omisiones. No aportan costa nueva. Se conservan Alemania/Prusia oriental e islas originales; Austria se incorpora completa. Dinamarca1940–1944 y Noruega/Benelux1940–1943 utilizan sus contornos terrestres fechados para evitar cintas costeras de un país completamente ocupado; colonias, Groenlandia y Svalbard no se heredan por esa regla. Los demás cortes interiores proceden de la síntesis original. Croacia queda recortada aYugoslavia; Eslovaquia utiliza el corte interior de referencia1939 recortado aCShapes y mantiene su identidad. También se elimina el doble inventario deChina bajo el control comunista: una guerra civil transfiere tierra, no duplicaChina.

## Preparación reproducible

1. Compilar `scripts/export-wartime-inputs.ts` conVite en modoSSR y ejecutarlo desde la raíz. Exporta la misma base y metadatos resueltos por la aplicación, sin alterar fuentes.
2. Ejecutar `scripts/prepare-wartime-partitions.py` conPython3.12 yShapely2.2.0. La copia local ignorada puede cargarse desde`.cache/python-packages`; no se instala nada en el navegador.
3. Ejecutar `scripts/register-wartime-data.mjs`, verificación de datos, pruebas y `scripts/prepare-country-catalog.mjs`. El registro es idempotente y conserva el año de referencia contemporánea22/10/2026.

La limpieza distingue regiones fuente conectadas de celdas aisladas: componentes de al menos0,25 grados cuadrados conservan sus cortes interiores; los menores necesitan respaldo de islas en la malla terrestre completa, no de un pequeño país sin costa. Después se aplican ámbitos documentales por controlador/año y las ocupaciones completas contrastadas. No es un umbral para borrar islas globalmente ni una estimación de superficie física. La clasificación de componente es una regla editorial de saneamiento, no una prueba histórica de ocupación. No se simplifican ni suavizan coordenadas. Las operaciones booleanas añaden intersecciones y reparan geometrías inválidas; las fuentes originales permanecen intactas.

Se comprueba conservación de toda la tierra de entrada, ausencia de tierra añadida y de nuevos solapamientos sobre los ya presentes en la base, intersecciones nulas salvo redondeo con países protegidos y contención de cada franja en su controlador final. El registro [WWII-PARTITIONS-AUDIT.json](WWII-PARTITIONS-AUDIT.json) conserva las magnitudes geométricas en grados cuadrados —diagnóstico, no estadísticas nacionales—. La tolerancia es1e-7 para conservación/solapamientos y1e-8 para áreas protegidas/franjas. Las pruebas adicionales consultan lugares negativos y positivos, islas, cliente croata, Austria incorporada, Praga ocupada y selecciónChina, además de la ruta real del cargador.

## Licencias y límites

El derivado mantiene **CC BY-NC-SA4.0 deCShapes**, con atribución deCliopatriaCC BY4.0 y referenciasNaturalEarth de dominio público. No contiene frentes españolesBY-SA3.0; esos siguen separados. El manifiesto fija las huellas de los cuatro insumos geográficos y el verificador rechaza una preparación obsoleta. Cada carpetaPaíses enlaza sus registros anuales sin duplicar la geometría.

Esto corrige partición y artefactos; **no certifica todos los frentes militares ni su fecha diaria**. Cliopatria1944 contiene fases que no equivalen al cierre del año: por ejemplo, parte deFrancia aún está en la extensión alemana de la síntesis. La zonaVichy1942 tampoco describe por sí sola la invasión de noviembre. No extender automáticamente una ocupación completa aNoruega/Benelux1944 ni convertir aliados en anexiones. Pendientes: fases fechadas1942–1944, liberaciones, control partisano,RSI, sectores de ocupación y frontera eslovaca de fuente propia. El mapa y el registro territorial identifican este tramo como síntesis anual. Las áreas sin registro político siguen sobre la referencia terrestre, sin transformarse en océano.

La corrección está acotada a1940–1944. El saneamiento1938–1939 permanece; los otros controles históricos conservan sus límites previos. No presentar esta entrega como una revisión mundial de todos los conflictos.

## Continuidad de la ficha eslovaca

La primera prueba de navegador detectó que la identidad creada para 1939 no tenía mandatos ni símbolo después de ese año. Se ha completado su ventana documental hasta 1944, manteniendo las declaraciones anteriores. El [USHMM documenta la continuidad presidencial de Jozef Tiso](https://encyclopedia.ushmm.org/content/en/article/jozef-tiso-1); los extremos de la ampliación se etiquetan como cobertura, no como nombramiento o cese. El fin de Tuka el 5/9/1944 se contrasta con [UPN, Pamäť národa 3/2017](https://www.upn.sk/publikacie_web/pamat-naroda/pamat-naroda-03-2017.pdf). La [edición institucional del diario de Štefan Tiso, 4/2006](https://www.upn.gov.sk/publikacie_web/pamat-naroda/pamat-naroda-04-2006.pdf) reproduce su nombramiento y juramento ese día. Ambas jefaturas del Gobierno aparecen en la ficha de 1944, con fechas y retratos distintos.

`curate-slovak-continuity.py` es puro e idempotente, preserva medios e incorpora sólo esa identidad. Se añade un original acreditado de Štefan Tiso, separado de los 34 retratos suizos. Si al cierre de la partición1944 Eslovaquia está bajo control alemán, la ficha previamente abierta se mantiene con sus autoridades documentadas y explicación de ausencia cartográfica; la búsqueda no inventa un territorio independiente activo.
