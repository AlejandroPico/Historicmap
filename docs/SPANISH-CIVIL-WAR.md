# Guerra Civil española · control territorial

`public/data/spanish-civil-war.geojson` contiene **siete registros**: dos bandos para 1936, 1937 y 1938 y una zona bajo control franquista en 1939. Se limita a **España peninsular e islas Baleares**. No atribuye automáticamente el mismo control al Sáhara, Guinea, el Protectorado de Marruecos o Canarias.

## Fuentes y precisión temporal

- **1936 y 1938:** [Cliopatria / Seshat Global History Databank](https://github.com/Seshat-Global-History-Databank/cliopatria), versión `5f433377139a6eeaeacbdc894b70f8805b72c8b5`, CC BY 4.0. Se utilizan los frentes compartidos entre `Spanish Nationalists` y `Second Spanish Republic`. Los intervalos son anuales, sin un día de observación uniforme. En concreto, el registro original agrupa **1936–1937**: no debe presentarse como un frente exacto de diciembre de 1936.
- **1937:** [Tyk / Té y kriptonita, «GCE-Frente en oct 1937.svg»](https://commons.wikimedia.org/wiki/File:GCE-Frente_en_oct_1937.svg), septiembre de 2009, versión de archivo restituida el 21 de diciembre de 2016. Se elige la licencia [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). El frente corresponde a **octubre de 1937**, después de la caída del frente norte, y conserva Málaga en la zona sublevada. No es una reconstrucción diaria ni del 31 de diciembre. El control de las Baleares se conserva según los registros de Cliopatria del periodo.
- **1939:** cierre de la guerra el 1 de abril y control franquista en todo el ámbito representado. El registro corresponde al resultado de la guerra, no a todos los días del año.
- **Costa y límite exterior:** [Natural Earth 1:10m](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/), dominio público, archivo `countries.geojson` ya conservado en el proyecto. La costa europea y las fronteras terrestres exteriores españolas utilizadas son aplicables a los cuatro años. No se transfiere al pasado la posición de un frente contemporáneo. No se utiliza CShapes para este derivado: así no se mezclan las condiciones NC-SA de su licencia con las de BY-SA del SVG.

El archivo conserva las referencias, fechas de observación, atribución y licencia por registro. **1936, 1938 y 1939:** CC BY 4.0 para la adaptación de los frentes de Cliopatria, con costa Natural Earth de dominio público. **1937:** adaptación de Tyk bajo CC BY-SA 3.0, incorporando atribución de Cliopatria y Natural Earth. Mantener estas condiciones al redistribuir los polígonos; el resto del repositorio no cambia de licencia.

## Transformación reproducible

Ejecutar `scripts/prepare-spanish-fronts.py` desde el repositorio con Python, Shapely 2.2.0, NumPy 2 o posterior compatible y pyproj 3.7.2. Son herramientas de preparación, no dependencias del navegador.

1. Cargar los registros originales de Cliopatria adquiridos por `scripts/acquire-history.py`. Conservar los puntos interiores de los frentes comunes entre los bandos; no sustituirlos por provincias.
2. Partir el exterior europeo de Natural Earth con esos frentes. Conectar cada extremo de desembocadura del frente a su punto más cercano del límite exterior, sin suavizar ni desplazar las coordenadas interiores. Esta adaptación evita que la costa muy generalizada de Cliopatria deje franjas falsas o excluya Barcelona y Málaga. No aumenta la precisión histórica del frente.
3. Para octubre de 1937, descargar y verificar el SVG publicado (`9688ac765cfe53a1883db122fe0de956a0ba35edfe03dc126b730a0ec2bba83b`, SHA-256). Extraer el frente interior de la ruta `path8971`, con ocho muestras por tramo Bézier.
4. Georreferenciar el SVG mediante una transformación afín en un marco Lambert conforme cónico explícito (`lat_1=40`, `lat_2=43`, `lon_0=-3`, WGS84). **Este marco se adopta para el registro; no se afirma que sea el sistema original del autor.** Los 15 puntos de control —11 marcadores urbanos y cuatro cabos— y sus coordenadas están escritos en el script. Residuo medio: **4.954 m**; máximo: **7.385 m**. Se declara una incertidumbre de registro **mínima de 10 km**, además de la incertidumbre de la propia reconstrucción. Los residuos de ajuste no son una certificación independiente de exactitud.
5. Cerrar la máscara más allá de los límites españoles y recortarla por el exterior de Natural Earth. El frente publicado, no esa prolongación exterior, divide el territorio. La otra zona es el complemento: no hay solapamientos ni huecos interiores entre bandos.

No se utiliza interpolación entre frentes, inferencia por población o asignación de provincias modernas. Se mantienen las coordenadas publicadas de los frentes de Cliopatria, aunque sean aproximadas. Los colores son convenciones del atlas: violeta republicano `#9b688f` y ocre sublevado `#b7914e`.

## Comprobaciones y límites

El preparador comprueba geometrías válidas, dos particiones sin solapamiento en 1936–1938 y un solo resultado en 1939. Comprueba Madrid y Barcelona republicanas durante 1936–1938, el paso de Bilbao y Gijón a control sublevado en 1937, Málaga republicana en 1936 y sublevada en 1937, y Madrid bajo control franquista en 1939. Son contrastes geográficos concretos, no una auditoría de cada localidad.

La superficie planar del ámbito de la fuente atribuida al bando sublevado pasa aproximadamente de **41,6 %** (1936) a **62,0 %** (1937), **68,6 %** (1938) y **100 %** (resultado de 1939). Estos porcentajes sólo comprueban progresión y partición; **no se publican como estadísticas históricas de superficie** porque no son medidas geodésicas ni fechas homogéneas.

Pendientes: mapas fechados dentro de cada año, cierre exacto de diciembre de 1936 y diciembre de 1938, ofensiva de Cataluña de 1938–1939, Teruel por fases, enclaves pequeños, frente norte por meses, particularidades de los distintos gobiernos y fuerzas republicanos, control colonial e insular completo y contraste con cartografía primaria de mayor resolución. La capa deja de congelar un mismo frente para 1936 y 1937, pero no equivale a una animación continua de toda la guerra.
