# Tareas y continuidad

## Encargo vigente · 0.46.0 · 2000–1001 a. C.

- [x] Comprobar base e42ebc88f, árbol limpio y coincidencia con origin/main. Congelar conservación en .cache/baseline046.json.
- [x] Inventario político: 21 nombres y 80 componentes originales fijados.
- [x] Investigar cronologías y autoridades; distinguir redes palaciales, ciudades, reinos y tradiciones no acreditadas como Estados.
- [x] Preparar tres tramos internos: 2000–1601, 1600–1201 y 1200–1001 a. C.; culturas junto a política, en español y con colores estables.
- [x] Revisar representaciones, títulos, fuentes y licencias; conservar todos los originales en Países.
- [x] Integrar navegación anual hasta 2000 a. C., continuidad con 1000 y todas las fases anteriores.
- [x] Compilar, registrar y sincronizar catálogo antes de pruebas; verificar conservación, tipos, build y navegador.
- [x] Documentar resultados reales y pendientes; subir a main sin esperar Actions/Pages.

No repetir las curaciones045. Esta tanda no equivale a mil mapas observados independientemente ni demuestra menor diversidad humana. Mantener aparte los pendientes de Asiria/Egipto650 y Babilonia626/600, sin darlos por corregidos al ampliar el pasado.

Resultado: 43 dossiers, 247 ventanas de autoridad, 84 copias de80 componentes políticos, 113 grupos culturales/146 fases. Revisión visual125 candidatos:52 adoptados,73 descartados. Conservación:20.262 cargos y10.006 fases anteriores intactos. Compilación y catálogo sincronizados.342 pruebas generales/72 suites,25Python,14 focales finales y8 después de regenerar, cinco recorridos finales de navegador, integridad, tipos y producción correctos. Regeneración:343 archivos idénticos; sólo orden de entradas del manifiesto, contenido idéntico. Capturas revisadas; rótulo deAsiria antigua y orden de nombres/fechas en imágenes completas corregidos. Entrega preparada en este commit; al reanudar, comparar HEAD yorigin/main antes de repetir el envío.

Pendiente del propietario: comprobar Actions/Pages. No esperar ni sondear el despliegue. Pendientes históricos:RESEARCH-bc2000 e inventario anual; continúan Asiria/Egipto650 yBabilonia626/600. No iniciar otra tanda sin encargo.

## Entrega anterior · 0.45.0 · 1000–601a.C., colores y rótulos

- [x] Diagnosticar el gris inicial879a9a ydar colores culturales estables sin modificar evidencia original.
- [x] Curar54 dossiers/301 ventanas,112 componentes,37 centros,20 contextos y11 puntos. Variantes yautoridades no identificadas documentadas.
- [x] Integrar142 originales culturales/144 fases; conservar9.862 fases anteriores.
- [x] Revisar98 candidatos visuales:50 aceptados/48 descartados, créditos ycaption; recuperar19 falsos rechazos por precisión de siglo.
- [x] Rótulos españoles propios por entidad, títulos comunes ybúsqueda por originales.
- [x] Cierre: compilación/registro final, batería general, Python, integridad, tipos ybuild.
- [x] Navegador, conservación, idempotencia ydocumentación.
- [x] Preparar entrega y envío a main; no esperar Actions/Pages.

Base d8baefc85,0.44.1. Curación y validación completadas; entrega preparada en este commit. Al reanudar, cotejar HEAD y origin/main antes de repetir el envío. No repetir las curaciones de una sola ejecución enumeradas enagentes.md sección60, incluida zhou045.

336 pruebas generales/71 suites correctas en dos hilos locales;25 comprobaciones Python correctas. Después del ajuste final de comparaciones,15 focales correctas, incluido catálogo ylos400 años nuevos. Tipos ycompilación de producción correctos; la última interfaz vuelve a comprobarse con tipos yVite sobre los datos de producción. Integridad142 recursos de datos/11 franjas tipográficas/9.106 medios porSHA-256.

Ocho recorridos únicos de navegador correctos: tres nuevos ycinco regresiones (Brasil real tras facción española, fecha exacta117, continuidad1a.C./1d.C., comparación entre países/fechas ypaneles persistentes). Los nuevos se repiten; las capturas esperan al renderizado real al reactivar culturas. Tres capturas revisadas en escritorio yglobo móvil. No se ejecutan localmente los126 recorridos completos; se conservan cuatro grupos deCI.

Conservación:1.531 identidades,19.961 cargos,1.040 símbolos y9.862 fases previas;142 originales culturales cotejados.135 recursos anteriores retenidos,127 idénticos ysiete nuevos. Tras normalizar el orden del manifiesto en la primera pasada, una regeneración completa sin red deja567 archivos comprobados sin diferencias. VéanseCONSERVATION-bc1000 eIDEMPOTENCE-bc1000.

Pendientes reales: partición del contorno imperial asirio enEgipto650, remisión babilónica626/600, variantes deAlyattes, contornos urbanos/dinásticos, archivos visuales ybibliografía regional acreditados. Notas concretas dentro de las carpetas deAsiria yBabilonia; carencias nominales enREVIEW-bc1000-bc601 yRESEARCH-bc1000. No confundir consulta anual con400 mapas medidos independientemente. No iniciar otra tanda sin encargo.

## Entrega anterior · 0.44.1 · fallo de catálogo comunicado

- [x] Reproducir el fallo original y una regresión que fuerza una ficha desactualizada.
- [x] Encadenar registro y actualización del catálogo; conservar el control que compara todas las fichas con sus identidades.
- [x] Regenerar las vistas, ejecutar la batería completa antes del build y verificar integridad/tipos/compilación.
- [x] Documentar resultados finales y preparar el envío a main sin esperar Actions/Pages.

Partida e0d0841f7. CI:328/329 correctas. La corrección tardía de Huiwen llegó a los datos y no a su entidad/índice; la pasada general local había precedido a ese ajuste. Nuevo test reproduce el defecto del flujo y comprueba idempotencia, carpeta estable y propagación de errores. No revertir Huiwen ni descartar los tres siglos. No repetir adquisiciones ni curaciones044. Publicación pendiente de confirmación del propietario.

Cierre local0.44.1:330 pruebas/70 suites correctas sobre los archivos sincronizados, antes de ejecutar el build de producción. npm run build completo (catálogo, tipos y Vite) correcto; otras dos pruebas del catálogo correctas después del build. Integridad135 recursos de datos/11 franjas tipográficas/9.060 medios correcta. Los135 recursos conservan sus SHA y metadatos anteriores salvo la versión; datos, geometrías y medios públicos no cambian. La ficha e índice deQin coinciden con sus22 registros y las dos etapas canónicas deHuiwen. Evidencia en CATALOG-FIX-0441.json. No se vuelven a adquirir datos ni se afirma haber ejecutado localmente los123 recorridos de navegador; se mantienen los cuatro grupos deCI.

Contenido terminado; verificar HEAD/origin/main y árbol limpio al retomar antes de repetir operaciones. El propietario confirma publicación.

## Entrega anterior · 0.44.0 · 600–301 a. C.

- [x] Inventario, fuentes y cronologías de los tres siglos.
- [x] Dossiers políticos y culturales, autoridades y representaciones acreditadas en Países.
- [x] Integración anual, sucesiones y continuidad con300a.C.; preservar toda la información previa.
- [x] Pruebas locales, cotejo final del índiceGit y preparación del envío a main sin esperar Actions/Pages.

Partida: cad30c9fa, árbol limpio.86 nombres políticos/296 componentes originales. No asumir que el pasado contiene menos sociedades: distinguir densidad documental de ocupación humana. Datos, pruebas, conservación e idempotencia terminados. Al reanudar, cotejar HEAD/origin/main y cambios pendientes antes de repetir trabajos o declarar el envío confirmado.

Progreso0.44:87 dossiers/427 autoridades/296 componentes;47 centros,44 contextos,34 puntos.223 originales culturales,290 fases nuevas/9.862 totales.107 imágenes inspeccionadas:66 aceptadas/41 rechazadas.329 pruebas generales/70 suites correctas; tras las últimas revisiones, otras25 focales,22Python, tipos y compilación correctos. Seis recorridos únicos de navegador correctos: tres regresiones y los tres nuevos; estos últimos se repiten sobre la compilación definitiva y pasan. Tres capturas revisadas en escritorio/móvil. CI123 casos31/31/31/30 sin omisiones ni duplicados; no se afirma ejecución local completa. Integridad135 datos/11 glifos/9.060 medios. Idempotencia229 archivos sin diferencias.

La comprobación visual descubrió que Atenas heredaba el nombre de una confederación posterior, impidiendo buscarla como ciudad en otras fechas. Corregidos cuatro nombres canónicos con fuente/motivo explícitos; Atenas/Esparta/Tebas yCirenaica conservan carpetas registradas. Tebas no recibe falsa monarquía por un mando militar; fin de la realeza batíada440 y fase republicana posterior. Conservación:1.482 identidades,19.534 cargos,1.040 símbolos y9.572 fases previas;130 recursos anteriores retenidos,118 idénticos y cinco nuevos.39 vistas generadas consolidadas conservan53 registros territoriales.

Fuentes y carencias enRESEARCH-bc600; cierre enDELIVERY-0.44.0. No repetir seed/supplement/curate/support/adopt/finaldata044: duplicarían fases o sobrescribirían revisiones. Antígono/Demetrio disponen de centro sin inventar polígono; el agregado315–308 no prueba un control único. Pendientes: partición especializada macedonia, contornos de ciudades y estados, cronologías locales, cargos completos, símbolos/retratos acreditados y bibliografía cultural regional. Continúan pendientes Xinzheng230, Copán, dependencia etolia, títulos heredados de fases culturales anteriores y frentes modernos. Revisar el restablecimiento del resaltado cultural al reactivar sus capas: la ficha sigue abierta, pero la captura no muestra el contorno seleccionado. No iniciar antes600 sin encargo. El propietario comprueba publicación; no esperar ni sondear Actions/Pages.

ÍndiceGit final: 1034 archivos nuevos/modificados cotejados con sus bytes locales; 9206 recursos de manifiestos verificados porSHA-256 yblobGit (9129 blobs de recursos anteriores sin cambios); 1229 originales canónicos de símbolos/representaciones comprobados directamente en el índice. Los cuatro documentos de cierre se cotejan otra vez después de incorporar estas cifras. No se espera ni sondea Actions/Pages.

## Entrega anterior · 0.43.0 · 300–201 a. C.

- [x] Inventariar originales políticos/culturales y revisar cronologías, especialmente sucesores de Alejandro y unificación Qin/Han.
- [x] Autoridades, representaciones revisadas, centros, contexto y conflictos dentro de las carpetas de cada entidad.
- [x] Integración anual y continuidad con200a.C.; conservación literal de lo anterior y calendario sin cero.
- [x] Pruebas, fuentes, documentación y preparación del envío a main sin esperar Actions/Pages.

Comienzo desde fa7b6805a,0.42.0 enviada y árbol limpio. No repetir los generadores iniciales de entregas anteriores ni confundir candidatos con autoridades verificadas. Registrar carencias y fechas alternativas; conservar las áreas culturales junto a la cartografía política. El propietario comprueba el despliegue.

Progreso0.43:83 dossiers,220 registros de autoridades,319 componentes originales de80 nombres/78 grupos canónicos,30 centros,23 contextos y17 referencias regionales de conflictos.73 originales culturales:59 referencias y14 remisiones,70 fases nuevas y9.572 totales.83 candidatos visuales inspeccionados:49 aceptados,34 apartados y dos alternativas identificadas (AshokaKanaganahalliGODL y moneda póstuma dePtolomeoIII emitida porIV).165 candidatos humanos resueltos de182,148 evidencias de reinado, sin errores de adquisición; no equivale a validación humana de todos.

Carencia cartográfica concreta detectada: en230a.C. el punto histórico deXinzheng113.74/34.40 cae enel componenteChu de la fuente, aunqueHan fue conquistado porQin. La fuente no conserva un componenteHan propio ese año. Se mantienen originales, sin inventar polígonos superpuestos; queda pendiente una partición histórica especializada de esa región. Las pruebas de título imperial usan el núcleoQin deXianyang y las de conquistas compruebanLu→Chu ySong→Qi, sin fingir que validan todos los puntos deChina. También faltan contornos documentados devarias entidades coreanas/japonesas y deotros ámbitos que la fuente no representa.

Corregidos cinco identificadores de estados antiguos compartidos conCaoWei,Qi delNorte,Yan anterior,HanZhao yAqQoyunlu. Reinos de la partición tienen claves propias; ZhangEr no recibe identidad/foto de una poeta contemporánea yShenYang no es la ciudad. Qin no adquiere título imperial antes221; Lu249 se incorpora aChu ySong286 aQi. Correcciones de continuidad200: Kalinga sigue bajoMaurya hasta185 yMinyue mantiene vinculaciónHan desde202. Lanka usa secuencia tradicional larga para no mezclarla conGeiger ni romperElara205–161; alternativas explícitas. No repetir seed/curate/support/adopt043: sobrescribiría revisiones posteriores. 25 pruebas focales y323 generales correctas;22 pruebasPython, tipos y compilación correctos. Conservación de1.440 identidades,19.314 cargos,1.040 símbolos y9.502 fases previas;220 archivos recompilados sin diferencias. Cierre de navegador e índiceGit enDELIVERY-0.43.0. Seis recorridos únicos de navegador correctos: los tres nuevos de0.43 y tres regresiones (selector exacto117, ciudades/fecha deBorodinó1812 y continuidad1a.C./1d.C.). Los tres nuevos se repiten tras ajustar la comprobación al retrato del rey local: la imagen legítima del hegemónXiangYu se conserva por separado. Tres capturas revisadas, escritorio y móvil. ÍndiceGit:607 archivos cotejados con sus bytes locales,9.141 recursos de manifiestos verificados (9.088 blobs previos sin cambios) y1.167 originales canónicos de símbolos/representaciones. Los cuatro documentos de cierre se cotejan de nuevo tras incorporar estas cifras. Contenido terminado; al reanudar, comprobar HEAD/origin/main antes de repetir trabajos.

Pendiente adicional de presentación detectado: revisar títulos heredados de fichas culturales; Sámi en200a.C. conserva un encabezado que menciona el mapa de1a.C., aunque la referencia espacial y la ventana indican200a.C. No se altera ahora la evidencia anterior.

## Entrega anterior · 0.42.0 · 200–101a.C. y corrección del despliegue

- [x] Restaurar fechas de episodios con día/mes de dos cifras y repetir el recorrido1812 comunicado.
- [x] Política, autoridades, culturas y representaciones200–101a.C.; conservar etapas anteriores.
- [x] Continuidad200/100a.C., pruebas, conservación y documentación.
- [x] Preparación del envío conjunto a main; el propietario comprueba Actions/Pages.

Estado de cierre:57 dossiers,180 registros de autoridades,158 componentes originales,32 centros,23 contextos y12 puntos regionales.85 candidatos visuales aceptados de115,30 descartados y alternativaSlodtz1704 paraAníbal. Wuzhu deMinyue se separa del homónimo jurchen del sigloXII; Bhadraka no hereda la identidad deBhagabhadra.85 originales culturales y98 fases nuevas;9.502 fases totales, sin retirar las9.404 anteriores. Las instituciones deCartago y la fase política aquea no se prolongan después146a.C.; la pervivencia cívica etolia no se presenta como soberanía continua. Las imágenes conservan el formato compacto habitual.

Ver docs/DELIVERY-0.42.0.md y RESEARCH-bc200.md para resultados finales, fuentes, conservación y límites. La pasada general final da317 correctas; la primera dio316 y un tiempo agotado en la auditoría900–1905. Se optimizó esa comparación manteniendo todos sus1.006 años y controles; repetición de24 casos correcta. Se pasan nueve recorridos únicos de navegador, incluido el fallo comunicado; los tres nuevos se repiten al ajustar las imágenes.22 pruebasPython, tipos y compilación correctos. No se afirma haber ejecutado los117 recorridos deCI en local: reparto30/29/29/29 sin omisiones. Los ajustes institucionales finales se comprueban otra vez al cerrar.

Conservación:1.424 identidades,19.134 registros previos de autoridades,1.040 símbolos y9.404 fases anteriores preservados;124 recursos previos retenidos,114 idénticos y tres nuevos. Cinco vistas anónimas generadas consolidadas conservan24 registros territoriales.191 archivos recompilados sin red, sin diferencias.127 recursos de datos,11 rangos de glifos y8.962 medios verificados;4.204 carpetas de entidades y1.440 identidades históricas. Cotejos finales del índiceGit registrados en DELIVERY. Al reanudar, comprobar primero HEAD/origin/main y cambios pendientes; no repetir adquisiciones si ya está enviado. No repetir seed/curate/support/adopt: sobrescribiría correcciones. No esperar ni sondear Actions/Pages.

Último cierre:19 pruebas focales y el recorrido deCartago correctos tras los ajustes institucionales. Registro de manifiesto sin reescritura de bytes idénticos; idempotencia final191 archivos sin diferencias. ÍndiceGit:615 archivos,9.100 recursos de manifiestos y1.128 originales canónicos de símbolos/representaciones cotejados. Los cuatro documentos de cierre se cotejan otra vez tras incorporar estas cifras.

Pendientes reales: consulados completos y autoridades menores; cronologías alternativas dePartia, Bactria, India yKush; representaciones individuales y símbolos acreditados; bibliografía y límites culturales locales. Contrastar el contorno etolio y su dependencia desde189/146 frente a la restauración de asociaciones cívicas: un polígono no acredita soberanía. Copán y frentes militares modernos anteriores siguen pendientes. No iniciar otro tramo anterior200a.C. sin encargo.

## Entrega anterior · 0.41.0 · 100–1 a.C.

Ampliar política y culturas100–1a.C., preservar todo lo anterior y comprobar expresamente continuidad1a.C./1d.C., sin año cero ni cambios artificiales al cambiar de fuente. Fechas, mandatos, imágenes y contexto con fuentes y carencias explícitas. Subir tras comprobaciones locales sin esperar Actions/Pages.

- [x] Fechas civiles anteriores a nuestra era y continuidad de navegación/fichas; pruebas focales correctas.
- [x] Inventarios, culturas, autoridades, imágenes y contextos.
- [x] Conservación, pruebas y documentación.
- [x] Preparación del envío a main y cotejo del índiceGit.

Estado de cierre local:63 dossiers,172 cargos,190 componentes,30 centros,24 contextos y ocho referencias de conflictos; diez registros de continuidad en nueve complementos.157 fases culturales nuevas(9.404 totales) y163 originales nominales.111 candidatos visuales inspeccionados:92 aceptados,19 apartados y alternativa monetaria deMusa. Todos los contextos/geometrías culturales de1a.C./1d.C. y colores/clasificación de44 entidades comunes pasan los cotejos. Cinco cambios de contorno proceden de la fuente: no certificarlos como hechos exactos al cambiar de era; ver ERA-CONTINUITY-041 y RESEARCH-bc100.

Conservación:1.410 identidades,18.952 cargos,1.040 símbolos y9.247 fases previas;121 recursos retenidos,111 idénticos y tres nuevos.203 archivos recompilados sin diferencias. Cuatro vistas anónimas consolidadas conservan ocho registros. Pasada general311 casos con dos incidencias corregidas; repetición14, después34, y13 tras armonizar entre eras.22 pruebasPython, tipos y build correctos. Ocho recorridos únicos de navegador pasan; los tres nuevos se repiten tras los últimos cambios y pasan. ÍndiceGit:873 archivos,9.021 recursos y1.052 originales canónicos cotejados correctamente. Contenido terminado y preparado para main; la publicación queda para confirmación del propietario. Al reanudar, cotejar primero HEAD/origin/main: si coinciden y no hay cambios, no repetir la adquisición o compilación. No contar repeticiones como pruebas únicas. No repetir seed/curation/adoption.

Pendientes documentales reales: consulados completos y autoridades menores, cronologías indopartas/indoescitas/kushitas alternativas, representaciones individuales y símbolos acreditados, bibliografía/costas/fronteras culturales locales, fechas cercanas al límite0 de la fuente, SwiftCreek antiguo, Copán y frentes militares modernos. Una ventana documental no es extinción. No iniciar otro tramo anterior100a.C. sin encargo. No esperar Actions/Pages.

## Entrega anterior · 0.40.0 · 1–99 d.C.

Ampliar política y culturas1–99, sin año cero. Conservar todas las etapas anteriores, revisar dinastías, autoridades, representaciones y fuentes. Subir tras comprobaciones locales sin esperar Actions/Pages.

- [x] Inventario, autoridades y cronologías contrastadas.
- [x] Culturas, imágenes inspeccionadas, centros y contextos.
- [x] Integración, conservación, pruebas y documentación. Búsqueda Han25–29 corregida y recorrido móvil repetido correctamente.
- [x] Preparación del envío a main; cotejo final del índice y remoto al cerrar.

Resultados en docs/DELIVERY-0.40.0.md:62 dossiers,119 cargos,141 componentes políticos,30 centros,20 contextos,68 fases culturales nuevas y57 imágenes aceptadas tras inspección (siete apartadas).38 comprobaciones únicas de lógica/datos,17 del lector Python, tipos/compilación y seis recorridos únicos de navegador correctos; los tres nuevos se repiten juntos. El recorrido antiguo de publicación117 ya pasa. Se conserva1.393 identidades,18.833 cargos,1.040 símbolos y9.179 fases anteriores;190 archivos recompilados sin diferencias.121 recursos de datos,11 rangos y8.800 medios verificados. CI111 recorridos28/28/28/27; no se ha ejecutado todo CI localmente. Índice Git:580 archivos y8.932 recursos cotejados;963 originales canónicos verificados. Publicación pendiente de confirmación del propietario; no esperar Actions/Pages.

Pendientes reales: autoridades menores, cronologías alternativas, representaciones/símbolos identificados, bibliografía y límites culturales locales, Copán y frentes militares modernos. Antes1d.C. permanece cobertura anterior aproximada; no iniciar otra regresión sin nuevo encargo.

Incidencia adicional del propietario: el navegador1/4 esperaba el snapshot100 al consultar117. Corregida la expectativa para exigir history-117 renderizado y fecha cargada; el recorrido informado ya pasó localmente. No esperar despliegue.

## Entrega anterior · 0.39.0 · 100–199

Ampliar el sigloII con política y culturas, preservar todo lo anterior, distinguir dignidades y cronologías, revisar imágenes. Mantener controles, colores romanos y franjas documentales. Validar localmente, subir a main sin esperar Actions/Pages.

- [x] Inventario, adquisición y revisión de autoridades y cronologías.
- [x] Imágenes inspeccionadas, culturas, centros y contexto.
- [x] Integración anual, conservación, pruebas y documentación.
- [x] Preparación del envío a main y comprobación de archivos.

Resultados en docs/DELIVERY-0.39.0.md:55 dossiers,111 cargos,126 componentes políticos,24 centros,18 contextos y71 fases culturales nuevas de83 originales.50 imágenes aceptadas y diez apartadas tras inspección.38 comprobaciones de datos/lógica,17 del lector Python, tipos/compilación y cinco recorridos únicos de navegador correctos. Conservar1.386 identidades,18.722 cargos,1.040 símbolos y9.108 fases anteriores; segunda compilación de180 archivos sin diferencias.118 datos,11 rangos de glifos y8.750 medios verificados.108 pruebas deCI repartidas27/27/27/27; no se ha ejecutado toda la batería localmente. Envío a main sin esperar publicación; Pages pendiente de confirmación del propietario.

Pendientes reales: sucesiones menores, administraciones, cronologías alternativas, signos/representaciones identificados y bibliografía cultural local. Permanecen los pendientes anteriores de Copán y frentes militares. No continuar antes de100 sin nuevo encargo.

## Entrega anterior · 0.38.0 · 200–299, continuidad romana y relaciones de control

Ampliar política/culturas200–299 manteniendo todo lo anterior. Corregir el salto cromático romano399/400 y estudiar Afganistán/Irak con el mismo criterio aplicado a todas las potencias: ocupación, intervención, apoyo y soberanía diferenciados. Mantener monedas y representaciones revisadas. Validar y subir; no esperar Actions/Pages.

- [x] Inventario200–299 y cronologías/autoridades documentadas.
- [x] Representaciones revisadas, centros, culturas y contexto.
- [x] Continuidad de colores romanos y revisión documentada de Afganistán/Irak.
- [x] Regla con marcas habituales cada50años desde el primer siglo, marca del año1 sin cero y botones manuales anuales.
- [x] Integración, conservación, comprobaciones y documentación.
- [x] Preparación del envío a main y cotejo de los bytes finales.

Resultados finales en docs/DELIVERY-0.38.0.md:67 dossiers,186 cargos,153 componentes políticos,29 centros,25 contextos y58 fases culturales nuevas.112 candidatos visuales aceptados y seis apartados.53 comprobaciones finales de datos/lógica, cinco Python, tipos/compilación y siete recorridos únicos de navegador correctos; repeticiones focales de franjas y cronología. Conservación de1.368 identidades,18.536 cargos,1.040 símbolos y9.050 fases previas; segunda compilación sin diferencias en189 archivos.115 datos,11 rangos y8.707 medios verificados. CI mantiene105 pruebas repartidas27/26/26/26; no se ha ejecutado toda esa batería localmente.867 originales canónicos cotejados en Git. Publicación de Pages pendiente de confirmación del propietario; no esperar Actions.

Pendientes: sucesiones menores, insignias y representaciones identificadas, cronologías culturales locales, frentes de Afganistán/Irak y fases iraquíes desde2014, además de los pendientes anteriores de Copán. Fuentes y límites en RESEARCH-200.md. No continuar antes de200 sin nuevo encargo.

## Entrega anterior · 0.37.0 · 300–399 y encuadre de representaciones

Ampliación300–399 con política y culturas. Petición adicional incorporada: corregir monedas cortadas y priorizar representaciones identificadas. Mantener cuatro máquinas para CI; el propietario comunica unos25 minutos. Envío a main tras validar, sin esperar Actions/Pages.

- [x] Inventario político/cultural y cronologías300–399.
- [x] Autoridades, imágenes, centros documentales, contextos y revisión de identidades.
- [x] Integración anual, culturas y continuidad con400.
- [x] Monedas con cara completa, busto de ValentinianoIII y atribuciones revisadas.
- [x] Conservación, comprobaciones, documentación y preparación del envío.

Resultados:80 dossiers de periodo,220 registros de autoridades,232 componentes políticos originales,41 centros,20 contextos y cinco referencias de conflictos.71 dossiers culturales originales:58 referencias adoptadas,12 remisiones políticas y Mill Creek excluido con original conservado. Catálogo4.092 carpetas/1.368 identidades. Consulta anual300–399 y continuidad con400; ambos controles activos al iniciar.

Augustos/césares, marco romano común y cortes de395 diferenciados. Jin occidental/oriental y título de príncipe317 frente a emperador318; Qin de Fú Jiān no es su principado anterior. Sasánidas/kushanshahs homónimos separados. Ezana y cronologías asiáticas aproximadas; testimonios mayas no generan mandatos completos. Fuentes y límites en RESEARCH-300.md, carencias en REVIEW-300-399.json. Datos y originales dentro de Países/<entidad>.

Imágenes:81 candidatos inspeccionados,73 aceptados y ocho rechazados. Moneda de Diocleciano con leyenda explícita; busto de atribución por corroborar apartado, sin usar automáticamente P18.44 imágenes monetarias antiguas inspeccionadas,46 correcciones por persona en ocho dossiers visuales. Se respeta el rechazo previo de TeodebertoII. ValentinianoIII tiene cabeza del Louvre425–450, con restauraciones modernas explícitas; Juan mantiene su moneda válida. Reversos con efigie imperial usados cuando el anverso muestra otra figura. Los originales y créditos se conservan; coinFace sólo cambia la presentación. Véanse MEDIA-REVIEW-300.json y COIN-FRAMING-037.json.

Conservación:1.345 identidades,18.316 cargos,1.040 símbolos y8.992 fases anteriores preservados;58 fases nuevas.109 recursos previos,101 idénticos y tres nuevos;71 originales regionales y232 componentes políticos cotejados. Regeneración de199 archivos sin diferencias. Dos vistas anónimas consolidadas conservan dos registros territoriales; ninguna tenía autoridades o símbolos propios. Ver CONSERVATION-300, CATALOG-CONSERVATION-300 e IDEMPOTENCE-300.

Validación:56 comprobaciones únicas en ocho suites correctas tras las correcciones y repeticiones focales(17 casos); seis nuevas repetidas tras la moneda final.15 pruebas Python, tipos y compilación correctos. Cinco recorridos únicos de navegador correctos; recorrido romano repetido después de la última imagen. Capturas de Roma, Jin móvil, Marciano y Valentiniano inspeccionadas.112 recursos de datos,11 rangos de glifos y8.603 medios licenciados verificados por SHA-256. No se ejecutó localmente la matriz completa de101 casos. Auditoría de reparto:26/25/25/25, cada caso exactamente una vez. No esperar Actions/Pages después del envío.

Pendientes reales: completar sucesiones menores/administraciones, cronologías alternativas, imágenes individuales fiables, símbolos con vigencia y función, cronología local cultural y contornos desfasados. Continúa pendiente conciliar las cronologías tempranas de Copán5/6 de0.35/0.36. Un hueco no es acefalía ni territorio vacío;399 no es extinción. Siguiente regresión anterior a300 sólo tras otro encargo. Mantener culturas, originales y decisiones de rechazo en todas las ampliaciones.

## Entrega anterior · 0.36.0 · 400–499 y correcciones de publicación

Entrega única: ampliar400–499 con política y culturas; corregir los fallos de0.34/0.35 y reducir el tiempo de GitHub conservando todas las pruebas. Envío a main tras validar, sin esperar Actions/Pages; el propietario comprobará el resultado remoto.

- [x] Corregir expectativas antiguas y validar los tres recorridos que fallaron, primero en0.35 y después con400–499.
- [x] Distribuir el inventario completo entre cuatro máquinas; compilar una vez y reutilizar en Pages el resultado de la revisión validada.
- [x] Inventario político/cultural400–499, originales, autoridades, representaciones, contextos y continuidad con500.
- [x] Auditoría de conservación, pruebas, documentación y preparación del envío conjunto.

Resultados: 82 dossiers de periodo, 227 registros de autoridades, 305 componentes políticos originales, 42 centros documentales, 20 contextos y siete referencias de conflictos. Culturas: 79 dossiers originales, 70 fases adoptadas, ocho remisiones a la base política y Mill Creek excluido por anacronismo conservando su original. Catálogo4.067 carpetas/1.345 identidades.

Roma occidental/Nepote dálmata/Odoacro, Jin oriental/Liu Song/Qi, dos Liang occidentales y dos Xia diferenciados. Hunos434–453 distintos de la referencia regional más amplia. Kavad restaurado y testimonios mayas con límites explícitos. Sedes documentales sin polígonos inventados. Véase RESEARCH-400.md; todos los datos nuevos en Países/<entidad>.

111 candidatos visuales inspeccionados: 91 adoptados y20 rechazados, con licencias, originales y pies. Las representaciones retrospectivas no se presentan como retratos contemporáneos. La efigie deConstancioIII no se atribuye aConstantinoIII. No se crean banderas modernas para el sigloV. Las carencias permanecen nominalmente en REVIEW-400-499.json y MEDIA-REVIEW-400.json.

Conservación: 1.320 identidades, 18.089 cargos, 1.040 símbolos y8.922 fases culturales anteriores conservados literalmente, más70 fases nuevas. Se mantienen106 recursos anteriores,98 idénticos, yse añaden tres. Coordenadas e índices cotejados:79 originales culturales y305 componentes políticos. Regeneración de198 archivos sin diferencias. Nueve vistas anónimas generadas se consolidan conservando12 registros territoriales; ninguna tenía autoridades/símbolos propios. Ver CONSERVATION-400, CATALOG-CONSERVATION-400 e IDEMPOTENCE-400.

Validación: 273 casos unitarios cubiertos por la ejecución completa y repetición de las cuatro suites corregidas (25 casos correctos). Fallos iniciales: expectativa fija499 sin contexto, comparación pesada de geometrías y dos barridos repetidos de miles de carpetas; se corrigen sin reducir los datos cotejados. Tipos, compilación y14 pruebas Python correctos. Seis recorridos únicos de navegador correctos: tres reportados y tres nuevos; los tres nuevos se repiten juntos al cierre (3 correctos/2,6min). Capturas deOdoacro, Wei móvil yCopán inspeccionadas. No se ejecutó localmente la matriz completa de98 casos. Verificados109 datos,11 rangos deglifos y8.538 medios licenciados por SHA-256.

CI: los registros adjuntos muestran0.34 con90 casos correctos ydos expectativas fallidas, y0.35 con92 correctos ylas mismas dos másworld_500. Ahora las pruebas derivan límites del catálogo. Inventario completo98, reparto25/25/24/24, cada caso exactamente una vez. Quality compila una vez; Pages automático reutiliza el artefacto del workflow_run validado ycomprueba su revisión. Auditoría local del YAML ydel verificador real: revisión correcta aceptada, revisión incorrecta e índice ausente rechazados. Ruta manual conservada. No hay medición remota ni promesa de duración concreta. Ver CI-PUBLICATION.md, CI-SHARDS-036.json yCI-PROVENANCE-036.json.

Pendientes reales, no tareas completadas: conciliar la cronología de los gobernantes5/6 deCopán (ventanas antiguas conservadas vs testimonios FAMSI), completar sucesiones menores/administraciones, cronologías alternativas deAsia/África, imágenes individuales ysímbolos acreditados, cronología local cultural ycontornos desfasados. Las faltas de datos no son acefalía;499 no demuestra extinción. Siguiente regresión anterior a400 sólo tras nuevo encargo. Mantener siempre pueblos/culturas junto a los poderes políticos ysus dos controles activados inicialmente.

## Entrega anterior · 0.35.0 · ampliación 500–599

Mantener entidades políticas, culturas, originales y controles independientes activados inicialmente. Investigar autoridades, transiciones y representaciones con fechas y fuentes; no inventar banderas, fronteras ni identidades. Validar localmente, subir y no esperar Actions/Pages.

- [x] Inventario político/cultural y cronologías de la fuente.
- [x] Autoridades, imágenes, cortes, formas políticas y contextos por entidad.
- [x] Culturas y continuidad con600; navegación anual y selección.
- [x] Auditoría, conservación, pruebas, documentación y preparación del envío.

Resultados 0.35: 108 dossiers 500–599, 272 registros de autoridades, 270 componentes políticos originales, 43 centros documentales, 21 contextos y ocho puntos regionales de conflicto. Referencia cultural500: 87 dossiers originales, 73 fases adoptadas, 12 remisiones políticas y dos etiquetas anacrónicas apartadas conservando originales. Cortes propias de Palenque, Tikal y Copán con tres dossiers adicionales de continuidad600–699 (sólo dos reinados que cruzan el límite; resto de sucesiones pendiente). Catálogo 4.024 carpetas/1.320 identidades.

Conservación: 1.290 identidades anteriores, 17.815 cargos, 1.040 símbolos y 8.849 fases culturales preservados; 73 fases nuevas. Los 103 recursos previos permanecen, 95 idénticos y tres recursos nuevos. Se cotejan 87 originales regionales y los 270 componentes políticos con sus fuentes. Regeneración sin red: 221 archivos sin diferencias después de completar la propagación de retratos a registros anteriores de la misma persona. Véanse CONSERVATION-500 e IDEMPOTENCE-500.

Imágenes: 125 candidatos inspeccionados, 95 aceptados y 30 rechazados. No usar glifos nominativos como fotos, mapas, cascos, escenas sin identificación adecuada, la efigie imperial de una moneda como retrato del rey emisor local ni objetos sasánidas con atribución individual insegura. MediaReview, originales, licencias y pies dentro de cada entidad. No inventar banderas del sigloVI. Las carencias concretas están en REVIEW-500-599 y MEDIA-REVIEW-500.

Correcciones documentales: césar no equivale a emperador; regencias de TiberioII y Amalasunta separadas del reinado. Kavad restaurado presente en500, CosroesII con fases no consecutivas, rivales con límites explícitos. Proclamación Sui581 distinta de reunificación589. B’alam Nehn524–532 y Wi’l Ohl K’inich532–551 contrastados con epigrafía; gobernantes anteriores de Copán con lecturas parciales. Vainyagupta regional507–508, no emperador gupta genérico543–548. Poverty Point y Mill Creek excluidos de la visualización500 por anacronismo; sus originales permanecen. Método y fuentes en RESEARCH-500.

Pendientes reales de investigación, sin convertirlos en tareas terminadas: ampliar sucesiones menores/administraciones locales, resolver cronologías alternativas del sigloVI, completar las sucesiones mayas posteriores a600, imágenes individuales fiables, símbolos con función y vigencia acreditadas, cronología local de regiones culturales y nuevas fuentes geométricas para contornos desfasados. Las ventanas599/699 no prueban extinción. Siguiente regresión anterior a500 sólo por nuevo encargo del propietario. Mantener siempre pueblos/culturas junto a los poderes políticos.

Revisión visual: se corrigen 17 encabezados regionales nuevos que arrastraban la fecha600/700/800 al reutilizar una descripción; ahora indican la referencia500. Las geometrías y fases anteriores se conservan. No confundir el área geográfica de una región con el año de procedencia de su contorno.

Validación local: 64 comprobaciones correctas en diez suites, 13 pruebas Python del lector y cinco recorridos únicos de navegador. Tras las aclaraciones de dignidad túrquica/rótulos, los tres recorridos del sigloVI se repiten correctamente; tras corregir los encabezados culturales se repiten las seis comprobaciones de datos nuevas y el recorrido de cortes mayas/culturas. Tipos y compilación correctos. Verificados 106 recursos de datos, 11 rangos de glifos y 8.454 medios licenciados por SHA-256. Capturas de Justiniano, Sui móvil y Sámi500 revisadas. No se ejecutó ni esperó la matriz completa de Actions/Pages.

31 vistas anónimas generadas se consolidan, conservando literalmente sus 47 registros territoriales en las vistas actuales; ninguna tenía autoridades o símbolos propios. Véase CATALOG-CONSERVATION-500. El envío se prepara para main/origin/main; comprobar coincidencia de la referencia remota al terminar y dejar al propietario la verificación del despliegue.

## Entrega anterior · 0.34.0 · ampliación 600–699

Mantener entidades políticas y áreas culturales, controles independientes activados inicialmente, selección coincidente y todo lo anterior. Investigar cambios de poder, mandatos e imágenes sin inventar banderas, fronteras ni certezas. Subir tras validar localmente sin esperar Actions/Pages.

- [x] Inventario político y cultural con originales y anacronismos.
- [x] Autoridades, imágenes documentadas, formas políticas, cortes y contextos por entidad.
- [x] Culturas y continuidad con700; navegación y reproducción anuales.
- [x] Auditoría, conservación, pruebas focales, documentación y preparación del envío.

Resultados 0.34: 425 componentes políticos originales, 112 dossiers de periodo, 294 registros de autoridades, 36 cortes/centros, 17 contextos y siete puntos de conflictos. Referencia cultural600: 83 dossiers originales, 68 fases adoptadas y 15 remisiones políticas. Catálogo: 3.987 carpetas y 1.290 identidades. Navegación anual600–699, sucesiones y fichas persistentes; controles de política/culturas activados inicialmente y sincronizados entre Capas/Filtros.

Conservación: 1.253 identidades anteriores, 17.521 autoridades, 1.040 símbolos y 8.781 fases culturales conservados. Los 100 recursos previos permanecen; 92 idénticos y tres recursos nuevos. Se cotejan83 originales regionales con la fuente fijada. Repetición del compilador:222 archivos sin diferencias. Seis vistas anónimas generadas se consolidan conservando literalmente sus registros territoriales; ninguna tenía autoridades/símbolos propios. Véanse CONSERVATION-600, IDEMPOTENCE-600 y CATALOG-CONSERVATION-600.

Validación local focal:49 comprobaciones/8 suites correctas,11 pruebas del lector de mandatos ycinco recorridos únicos de navegador. Los tres recorridos del sigloVII se repiten correctamente tras la última aclaración deHimyar/lajmíes/Armenia. Tipos y compilación correctos. Verificados103 datos,11 rangos deglifos y8.365 medios porSHA-256. Capturas deZhou, comunidad deMedina yAsuka móvil revisadas. No se ejecuta ni se espera la matriz completa deActions/Pages desde esta entrega local.

Imágenes:135 candidatos inspeccionados,98 aceptados y37 rechazados, con pies ylicencias. No usar la piezaLACMA dePerozII325–330 para el pretendiente del sigloVII, la moneda con efigie masculina deAzarmidokht como retrato suyo, ni textos/mapas/edificios. La pintura deClovisIII691–695 del catálogo deVersalles corresponde aClodoveoIV según numeración moderna y conserva advertencia de imagen imaginaria. Las carencias deautoridades/símbolos/retratos están inventariadas nominalmente enREVIEW-600-699.json; no afirmar censo mundial completo. Pendientes: más cronología local, cortes mayas delClásico, imágenes individuales ysucesiones de poderes menores, insignias documentales ycontinuidad de referencias sin fase equivalente700. El fin699 deventana no es extinción.

Incidencias resueltas:66 respuestas429 se recuperan antes decompilar; nombres ambiguos se resuelven por artículo/identidad humana. Una aserción antigua esperaba inicio700 en el inventario contextual: actualizada a600, conservando el resto delas comprobaciones yrepitiendo las ocho suites. Sui/Tang yotros contornos con desfase no fechan automáticamente la dinastía; sedes documentales eidentificación decontornos heredados permiten consultar sin inventar fronteras. Mantener culturas yprioridad política en futuras regresiones. Preparado para main yorigin/main; confirmar coincidencia remota ydejar al propietario la verificación deldespliegue.

## Entrega anterior · 0.33.0 · ampliación700–799 y visibilidad sincronizada

Ampliar el sigloVIII conservando pueblos y culturas, cartografía política y todas las fases previas. El propietario añade dos controles independientes en Capas y Filtros: Cartografía política / Pueblos y áreas culturales. Ambos activados por defecto y sincronizados entre paneles; mantener elecciones al navegar años/proyecciones. Subir tras validar localmente, sin esperarActions/Pages.

- [x] Inventariar originales políticos/regionales y anacronismos de la fuente700.
- [x] Autoridades, representaciones documentales, centros, formas institucionales y contextos con evidencia por entidad.
- [x] Culturas/regiones700–799, continuidad con800, prioridad y selección coincidente, sin borrar originales.
- [x] Dos controles sincronizados en ambos paneles; independientes, activados inicialmente, sin perder fichas ni elecciones al viajar.
- [x] Auditoría anual, conservación, pruebas focales/navegador, documentación y envío.

Validación final 0.33: 255 pruebas en 58 archivos, nueve pruebas del lector de mandatos y ocho recorridos de navegador correctos. Tipos y compilación correctos; 100 recursos de datos, 11 rangos de glifos y 8.279 medios verificados por SHA-256. Capturas revisadas en escritorio y móvil, con espera hasta el renderizado de la combinación visible. Los controles arrancan ambos activados; conservar elecciones durante cambios de año y proyección, mantener fichas abiertas y excluir de búsqueda/selección las cartografías ocultas.

Conservación: 1.225 identidades previas, 17.273 registros de autoridades, 1.040 símbolos y 8.682 fases culturales anteriores conservados; 126 originales regionales cotejados con la fuente fijada. Recompilación de 213 archivos sin diferencias. Catálogo: 3.946 carpetas y 1.253 identidades. La vista generada anónima «Maya states» se consolida en REFERENCE-MAYA-CITY-STATES: conserva el registro world_500.geojson/10 y los originales; no es una eliminación de documentación.

Alcance nuevo: 106 dossiers políticos, 359 componentes originales, 248 registros de autoridades, 99 fases regionales, 42 centros fechados, 21 contextos y siete puntos de conflictos. Revisión visual de 117 candidatos: 76 representaciones adoptadas y 41 rechazadas. Las carencias nominales permanecen en REVIEW-700-799.json; falta contrastar más autoridades menores, insignias, imágenes individuales y continuidad cultural hacia800 de nuevas referencias sin equivalente. No confundir fin de revisión799 con extinción ni inventar banderas medievales.

Correcciones de validación: un clic en el mapa heredaba data-government-filter y reactivaba la política; restringido a botones explícitos. La carga contemporánea en emulación gráfica superó la espera inicial; espera de renderizado ampliada, después correcta. Las primeras capturas se tomaban antes del repintado; ahora los controles se comprueban tras la confirmación visual del mapa. Piluoge conserva la misma identidad antes y después de la unión de Nanzhao. Se regeneran además los informes anuales de 1000–1799, que conservaban recuentos de símbolos anteriores a las revisiones; no se alteran sus hechos históricos. Verificados 433 originales únicos dentro de sus carpetas de entidad en los bytes preparados para Git. Entrega preparada para main y origin/main; confirmar coincidencia remota, sin esperar Actions/Pages.

## Entrega anterior · 0.32.0 · ampliación800–899

El propietario solicita retroceder desde900 hasta800 manteniendo pueblos, culturas y áreas de poblamiento junto a los poderes políticos. Conservar fases, originales y selección política prioritaria. Nuevos hechos y originales dentro de la carpeta de cada entidad. Comprobar localmente, subir y no esperarActions/Pages.

- [x] Inventariar geometrías políticas y fuentes culturales del sigloIX, con fechas, procedencia y límites explícitos.
- [x] Incorporar identidades, autoridades, imágenes y contexto; revisar símbolos sin anticipar enseñas, reinos o títulos posteriores.
- [x] Incorporar culturas y poblamiento; evitar huecos por no disponer de organización estatal y conservar los datos900–2027.
- [x] Navegación/reproducción anual, selección coincidente, persistencia, filtros y auditoría de carencias800–899.
- [x] Pruebas, revisión visual2D/globo/móvil, documentación, versión, conservación y preparación del envío.

Resultados:528 componentes políticos,139 reglas,137 dossiers de periodo;85 fases regionales nuevas y32 remisiones políticas. Se conservan exactamente8.597 fases culturales previas,1.204 identidades,16.975 cargos y1.040 registros de símbolos.117 originales regionales cotejados con la fuente800. Catálogo ampliado:3.870 carpetas y1.225 identidades.123 imágenes aceptadas y43 descartadas; quedan carencias nominales, no afirmar cobertura mundial exhaustiva.

Incidencia añadida por el propietario:Quality0.31.1 falló sólo en screenshot deSong1128 por límite15segundos, tras82 recorridos correctos. Corregir las tres capturas de review-025 a45segundos/animaciones desactivadas, mantener aserciones y repetir ese recorrido antes de subir. No esperar el nuevo despliegue.

Cronología carolingia revisada: la fuente conserva el agregado hasta849; desde843 se muestra como referencia anterior al reparto y se añaden tres centros de corona seleccionables hasta849. No se adelantan las fronteras850. Repetir el recorrido nuevo tras esta corrección; el recorrido deSong informado por el propietario ya pasó.

Pendientes documentales para siguientes entregas: autoridades de poderes menores, contraste de límites locales, insignias de función/fecha acreditadas, representaciones individuales adecuadas y calendarios. Continuar las culturas en futuras regresiones anteriores a800. Véase docs/RESEARCH-800.md y los inventarios nominales; no dar esos huecos por resueltos al reanudar una sesión.

Cierre local:247 pruebas generales/57 archivos, siete del parser y12 focales tras revisarVerdún. Ocho recorridos de navegador distintos correctos, incluido el deSong1128 que había fallado enGitHub; el móvil de800 se repitió de nuevo con los dos retratos de regentes y pasó en32s. Tipos, compilación e integridad correctos:97 datos,11 franjas y8.215 medios. Segunda compilación sin red:241 archivos idénticos.8.323 recursos cotejados porSHA-256/objetoGit y367 originales por entidad cotejados contra los bytes preparados. Cinco vistas generadas obsoletas consolidadas en carpetas canónicas, con todos sus registros anteriores conservados. Confirmar origin/main y el identificador al cerrar el envío; no esperarActions/Pages.

## Entrega anterior · 0.31.1

La entrega0.31.0 ya se envió a main en cf816799. Durante el cierre, el propietario pide corregir el retrato deGabriel Terra enUruguay1933 y añadir doble clic derecho con ratón para orientar el norte arriba. No esperarActions/Pages.

- [x] Revisar ambas imágenes, adoptar fotografía de asunción1931 y conservar original/procedencia enPaíses/URY-Uruguay. El cartel queda acreditado pero no se usa como retrato.
- [x] Corrección canónica de retrato sin alterar cargos, fechas ni fuentes.93 recursos de datos previos y8.108 medios anteriores conservados; tres recursos idempotentes. Resultado específico dentro deUruguay/revision-retrato-validacion.json.
- [x] Doble clic derecho con ratón: orientación norte, sin alterar centro/zoom/inclinación. Excluir arrastres y gestos táctiles; conservar el giro con arrastre derecho.
- [x] Comprobar foto en la ficha y gesto real enMercator/globo: dos recorridos correctos, con centro/zoom/inclinación preservados y clic aislado/arrastre diferenciados. Captura deUruguay1933 inspeccionada. Doce pruebas focales correctas; tipos, compilación e integridad correctos. Preparar/verificar bytes deGit y confirmar main remoto al enviar, sin esperar publicación.

Integridad del cierre:94 datos,11 franjas y8.109 medios. La corrección de retrato conserva las1.204 identidades y todos los campos de cargos salvo la imagen deGabriel Terra. El nuevo dossier incluye las colecciones vacías symbols/leaders del formato común y portraitCorrections; se amplía el cotejo canónico de las revisiones para comprobar estos originales. Las242 pruebas generales y la revisión cultural completadas en0.31.0 quedan registradas abajo; este cierre adicional se verifica con12 pruebas focales y dos recorridos de navegador, sin repetir toda aquella batería.

Git0.31.1:21 archivos nuevos/modificados preparados coinciden con los bytes locales;8.214 recursos verificados porSHA-256 y objetoGit,8.212 objetos de recursos anteriores iguales. Sin archivos eliminados. Preparar esta nota final y confirmar main remoto al cerrar; no esperar publicación.

## Entrega anterior · 0.31.0 · continuidad cultural 1905–presente

Completar la revisión posterior a1905 hasta el año vigente, preparando2027 como horizonte de consulta de referencias conocidas, sin inventar observaciones futuras ni alterar el máximo del reloj. Mantener pueblos/culturas en toda ampliación posterior, también antes de900. Subir después de comprobar localmente; no esperarActions/Pages.

- [x] Inventariar los contextos activos en1905, distinguir referencias históricas de poblaciones actuales y conservar las fases anteriores.1.769 contextos culturales retenidos;49 referencias políticas no prorrogadas automáticamente.
- [x] Añadir continuidad documentada, hitos institucionales fechados y fuentes locales; no prolongar automáticamente reinos extintos o confundir cultura, reserva y soberanía.1.782 fases nuevas y nueve contrastes focales, con extensión contemporánea aún pendiente de delimitación.
- [x] Auditar todas las selecciones1900–2026 y el horizonte2027, prioridad política, selección coincidente y cambios de contexto.128 selecciones con la misma fuente histórica/contemporánea utilizada por la aplicación;2027 sólo consulta referencias conocidas.
- [x] Revisar mapa/globo/móvil, cargas y protección de fronteras/autoridades previas.242 pruebas/56 archivos correctos; cuatro recorridos de navegador finales correctos, incluidas selección coincidente, persistencia, móvil, reloj2027 y descarga obsoleta. Capturas sámi y burarra revisadas.
- [x] Registrar alcance, límites, conservación, versión y entrega preparada para origin/main. Confirmar coincidencia remota al cerrar el envío; no esperar publicación. Después queda pendiente la siguiente regresión anterior a900.

Conservación0.31:90 recursos anteriores idénticos,6.815 fases previas exactas y1.769 dossiers con todos sus campos/fases anteriores conservados. Cero originales espaciales modificados y cero polígonos nuevos. Preparación repetida con16 recursos idénticos. Catálogo:3.823 carpetas y1.204 identidades políticas. Tipos y compilación correctos;94 datos,11 franjas y8.108 medios verificados. El archivo publicado1900–1905 conserva URL/huella; no se usa como segmento actual.

Comprobaciones iniciales ajustadas: la prueba nueva consultaba annualData después de2019, fuera de su cobertura, en vez de countries.geojson/perfiles como hace la aplicación; corregida y repetida con cinco comprobaciones correctas, confirmada después por las242 pruebas generales. La espera de fecha de la prueba de descarga obsoleta usaba cinco segundos; se igualó a la espera habitual de carga del mapa y pasó. No se corrigieron geometrías por esos fallos de las pruebas.

Investigación todavía abierta: residencia contemporánea, diásporas, desplazamientos, cambios de denominación y delimitaciones jurídicas/locales. Las1.769 referencias retenidas no certifican que todas las identidades antiguas persistan sin transformación ni que sus habitantes actuales residan dentro de esos contornos. Véanse modernConsultationReview y pendientes por entidad, docs/CULTURAL-MODERN-REVIEW.md e informes asociados. Las carencias anteriores0.30 siguen vigentes.

Git preparado0.31:3.566 archivos nuevos/modificados coinciden con sus bytes locales por huella del objetoGit. Los8.213 recursos de los manifiestos coinciden además porSHA-256;8.209 objetos de recursos anteriores permanecen idénticos. Sin eliminaciones de archivos. La auditoría final registra258 componentes políticos y1.769 referencias culturales en2026;2027 repite referencias conocidas con marca prospectiva, sin observaciones futuras. Preparar estas notas finales y confirmar main con origin/main antes del cierre; no esperarActions/Pages.

Plan futuro: representar expansiones humanas, glaciaciones y cambios ambientales/extinciones con cronologías científicas, capas separadas y evidencia propia. No adoptar la cifra «13 glaciaciones» como un catálogo científico ya validado; distinguir grandes glaciaciones, ciclos glaciales y avances regionales. Esta entrega no implementa todavía esas reconstrucciones.

## Entrega anterior · 0.30.0 · partes cinco y seis

Ampliación regional 1701–1905 y revisión conjunta 900–1905. Conservar las evidencias previas y la prioridad política; recuperar continuidad cultural sin confundir áreas tradicionales con fronteras anuales. Guardar decisiones y originales en las carpetas de Países. Comprobar localmente, subir y terminar sin esperar Actions/Pages.

- [x] Inventariar las fuentes intermedias hasta 1905, sus nombres y tipos de representación: siete instantáneas y 2.513 pares nombre/instantánea, con originales por entidad.
- [x] Incorporar fases documentales y continuidad de pueblos y regiones después de 1700; distinguir pueblos, poderes, territorios tradicionales y administraciones coloniales. 6.657 dossiers y 6.815 fases acumuladas; las referencias anteriores siguen identificadas como históricas.
- [x] Revisión global de identidades, fases, duplicados, nombres omitidos, saltos de fuente y remisiones a la base política sin enlace resuelto. Auditoría técnica de 1.006 selecciones anuales y estados de enlace por entidad; no certifica todas las cronologías ni fronteras locales.
- [x] Contrastes focales y exclusiones razonadas; conservar las carencias locales como pendientes explícitos. Véase docs/CULTURAL-GLOBAL-REVIEW.md.
- [x] Auditoría anual 900–1905, conservación de datos y originales anteriores, selección real de entidades coincidentes y revisión visual en mapa/globo/móvil. Cinco recorridos de navegador correctos; capturas de Sámi, Australia y Aotearoa móvil inspeccionadas. Aclarada la etiqueta de área histórica de la Unión de Kalmar al revisar las capturas.
- [x] Documentación, versión, catálogo e integridad; entrega preparada para origin/main. Confirmar coincidencia remota al cerrar el envío, sin sondear el despliegue.

Comprobaciones locales 0.30: 236 pruebas correctas en la ejecución general y un único agotamiento del tiempo límite de la lectura masiva de originales; repetida esa prueba junto con sus seis compañeras con margen adecuado, siete correctas. Total de 237 pruebas distintas/55 archivos verificadas. Las cinco de revisión global se repiten después de la aclaración de Kalmar y pasan. Tipos, compilación e integridad: 92 datos, 11 franjas tipográficas y 8.108 medios correctos. Once segmentos por siglo, mismas geometrías y fases que el export completo.

Conservación final: 79 recursos de datos anteriores idénticos, 4.139 originales regionales anteriores idénticos y 4.139 dossiers conservados con sus fases previas. 3.366 fases previas preservadas, con una corrección explícita de entityType songhay acorde con su kind cultural. 2.516 originales nuevos contrastados con coordenadas fuente. Idempotencia: quince recursos idénticos después de la última aclaración de Kalmar. El primer cotejo de idempotencia coincidió con esa edición local; se repitió la generación una vez terminada, sin rehacer la lectura masiva de preservación ya completada. Informe docs/CULTURAL-VALIDATION-0.30.json.

Catálogo final: 3.823 carpetas y 1.204 identidades políticas. Al resolver alias de Tasmania y Rapa Nui se retiran dos vistas generadas entidad.json duplicadas; todos los dossiers y originales previos siguen conservados. Comprobación de Git: 9.641 archivos nuevos/modificados preparados coinciden byte a byte con los locales mediante la huella del objeto Git; 8.211 recursos de los manifiestos comprobados también por SHA-256, de los cuales 8.198 conservan el objeto de la entrega anterior. Tras esta nota, preparar de nuevo sólo la documentación y confirmar el envío de main.

Pendientes de investigación tras 0.30: cronología local de 3.830 fases tradicionales, desplazamientos y subdivisiones omitidas; 1.755 fases de contexto histórico no prueban residencia constante. Enlaces con la base política: 219 explícitos presentes, 51 propietarios con relación pendiente, 73 candidatos nominales y 1.173 no resueltos. Un enlace no resuelto no es un país ausente. Conservar pendientes y evidencias en el dossier de cada entidad; no resolverlos mediante semejanza de nombre o posición. Véase docs/CULTURAL-GLOBAL-REVIEW.md.

## Entrega anterior · 0.29.0 · revisión conjunta 1200–1700

El propietario agrupa los puntos 3 y 4 en una entrega. Conservar los registros 900–1200 y la cartografía política; ampliar pueblos, regiones y referencias con fases, fuentes y grados de incertidumbre. Las geometrías tradicionales sin datación local no son fronteras soberanas de un año concreto. Subir tras validar localmente, sin esperar Actions/Pages.

- [x] Inventario de las diez instantáneas intermedias: 4.000 pares nombre/instantánea con decisiones, procedencia, coordenadas y originales dentro de Países.
- [x] Fases regionales y continuidad 1201–1700. Correcciones focales de Funj, Songhay, Aotearoa, comanches, etiquetas seminolas y otras referencias anacrónicas; las áreas tradicionales sin cronología local siguen señaladas como tales.
- [x] Varias geometrías documentadas de una misma región, identidad de selección estable, fases sin solapamiento y carpetas canónicas conservadas.
- [x] Contrastes focales de América, África, Siberia, Asia y Oceanía; pendientes de contraste local dentro de cada dossier. No se certifican fronteras culturales anuales exactas.
- [x] Disponibilidad y conservación, pruebas de selección y persistencia y revisión visual en mapa/globo/móvil. Corregido bloqueo real al cambiar de año sin un polígono político visible.
- [x] Versión, documentación, catálogo, integridad y entrega preparada para origin/main. Confirmar bytes preparados y coincidencia remota al cerrar; no sondear el despliegue.

El alcance siguiente de aquella entrega, 1700–1905 y revisión global, se atiende en 0.30 arriba. Las carencias independientes de investigación local continúan registradas.

Resultado acumulado: 4.139 dossiers; 3.365 adoptados, 703 remitidos a la base política y 71 exclusiones. 3.366 fases (3.225 culturales/geográficas y 141 referencias políticas), no países independientes. 2.304 fases tienen datación tradicional local pendiente: esa carencia permanece abierta y visible, no se convierte en una validación independiente por estar representada.

Conservación: 79 recursos anteriores, 127 referencias previas y 258 archivos canónicos previos idénticos. 4.010 originales nuevos contrastados con las coordenadas de fuente; preparación repetida con cuatro recursos idénticos. Catálogo: 3.692 carpetas y 1.204 identidades políticas. Integridad: 81 datos, 11 recursos tipográficos y 8.108 medios acreditados.

Comprobaciones: 232 pruebas/54 archivos correctas, más 14 comprobaciones focales finales tras las correcciones. Cuatro recorridos finales de navegador correctos (atlas general, continuidad sámi, América/Australia y Aotearoa/Siberia móvil); los cuatro previos de coexistencia también pasan. Capturas revisadas, tipos y compilación correctos. El primer recorrido móvil detectó el bloqueo de selección descrito arriba; corregido y repetido con resultado favorable. Catálogo protegido contra reescrituras idénticas y bloqueos transitorios de Windows/OneDrive.

Preparación de Git comprobada: 8.200 recursos de ejecución, 4.139 originales regionales y 253 originales visuales previos coinciden con sus huellas. Confirmar main con origin/main al cerrar el envío; la publicación la verifica el propietario.

### Pendientes de investigación tras 0.29

- [ ] Cronología local independiente de las áreas tradicionales y revisión de desplazamientos; no extrapolar una atribución del mapa editorial a todos los años de su ventana.
- [ ] Pueblos y subdivisiones omitidos por las compilaciones, contactos y superficies con fecha propia. Las notas concretas permanecen en cada carpeta de Países.
- [x] Ampliación posterior a 1700 hasta 1905 y comprobación global: atendidas en la entrega 0.30, con los límites de investigación declarados.
- [ ] Confirmación de publicación por el propietario, sin esperar Actions/Pages.

## Entrega anterior · 0.28.0 · integración cultural y revisión900–1200

El propietario autoriza los encargos1 y2: preparación general y revisión900–1200. El horizonte posterior1200–1905 se mantiene pendiente. Entrega con resultados visuales, selección simultánea de poderes políticos y regiones culturales, prioridad política y fechas/fuentes/incertidumbre explícitas. No confundir gris con despoblación. Comprobar localmente y subir sin esperarActions/Pages.

- [x] Inventariar los nombres de las instantáneas relevantes y documentar adopciones, exclusiones y límites temporales por entidad en Países. Los 129 nombres de 1000 tienen decisión; 500 y 1492 quedan inventariados sin trasplante automático.
- [x] Contraste focal de regiones culturales y poderes omitidos de 900–1200: 56 referencias con bibliografía adicional y correcciones de anacronismos; conservar las carencias de las otras 71, sin presentar sus contornos como verificados independientemente.
- [x] Integración general: fondo cultural, prioridad de la representación política y selección de ambas entidades donde coincidan.
- [x] Búsqueda y fichas propias, fuentes, fechas, incertidumbre, persistencia temporal y cobertura visible.
- [x] Pruebas de no desaparición, cambios de fuente, solapamientos y carga obsoleta; 79 archivos anteriores e identidades políticas conservados byte a byte.
- [x] Revisión visual en 2D/globo/móvil, manifiestos, versión, documentación y catálogo.
- [x] Comprobar los bytes preparados en Git: 8.200 recursos de ejecución, 129 originales regionales y 253 originales visuales previos correctos. Entrega preparada para origin/main; confirmar coincidencia remota al cerrar, sin esperar Actions/Pages.

No marcar como completa una reconstrucción exhaustiva mundial por incorporar una referencia de1000. Separar fechas de existencia, testimonio espacial e intervalo de consulta; conservar los casos no resueltos en la auditoría nominal.

Resultado local: 127 referencias (61 culturales/geográficas y 66 políticas), dos exclusiones justificadas; 225 pruebas en 53 archivos correctas y cinco recorridos de navegador correctos, incluidos cuatro culturales finales. Capturas de escritorio, solapamiento real y móvil revisadas. Tipos, compilación y preparación reproducible correctos. Fuentes, decisiones y límites en [CULTURAL-COVERAGE.md](docs/CULTURAL-COVERAGE.md), [auditoría nominal](docs/CULTURAL-REVIEW-900-1200.json) y [validación](docs/CULTURAL-VALIDATION-0.28.json).

### Continuidad cultural pendiente

- [ ] Contraste regional independiente de las 71 referencias basadas todavía sólo en la compilación; las tareas concretas permanecen en cada dossier de poblamiento.
- [ ] Subdivisiones locales, pueblos ausentes de las fuentes, fases de contacto y contornos propios con fecha; la ventana 900–1200 no demuestra límites constantes durante tres siglos.
- [ ] Siguiente encargo: revisión 1200–1500, seguida por 1500–1700 y 1700–1905, y comprobación global final. No dar estas ampliaciones por realizadas.
- [ ] Confirmación de publicación por el propietario; no esperar ni sondear el despliegue.

## Entrega preparada · 0.27.0 · ampliación hasta 900

- [x] Geometría anual900–999:531 intervalos originales,77 reglas y conservación de48 geografías previas; puntos anteriores de conflictos conservados.
- [x] 78 dossiers por entidad enPaíses,313 intervalos seleccionados y86 regionales; todos los hechos previos de mandatos y símbolos conservados.
- [x] 177 pares persona/imagen inspeccionados:135 adoptados y42 rechazados;176 archivos nuevos, diez pies aclaratorios y exclusiones persistentes.
- [x] 52 formas institucionales,59 sedes/cortes,17 contextos y seis puntos regionales. Agregados y cronologías de fuente advertidos.
- [x] Auditoría de cien años y pruebas locales:219 pruebas en52 archivos, cinco pruebas del lector de oficios, tipos, compilación e integridad correctos. Compilación canónica repetida: diez recursos idénticos byte a byte.
- [x] Selector de fecha compacto: campo y confirmación, sin título grande ni fondo oscurecido; teclado, validación y cierre conservados.
- [x] Entrega preparada:8.198 recursos y253 originales de entidades comprobados en los bytes deGit. Confirmar coincidencia demain conorigin/main al cerrar, sin esperarActions/Pages.

Catálogo:1.204 claves,16.975 mandatos,3.411 carpetas y8.108 medios. Integridad SHA-256 de79 datos,11 franjas tipográficas y8.108 medios. Cinco recorridos finales de navegador correctos: sigloX en escritorio/globo móvil, selector compacto, carga demorada/pausa, recuperación tras error y persistencia de ficha/pestaña/lectura. Capturas revisadas. [Fuentes, alcance y pendientes](docs/RESEARCH-900.md); [auditoría nominal](docs/REVIEW-900-999.json):11.709 entidades/año,8.467 sin autoridad,11.636 sin símbolo,158 personas/órganos sin retrato entre activos y173 en el catálogo ampliado. No son un censo mundial completo.

### Pendientes delimitados del siglo X

- [ ] Completar las carencias nominales de la auditoría, especialmente pequeños poderes, Asia interior, África y América; cinco identidades/cargos candidatos deKhotan no resueltos.
- [ ] Completar reproducciones acreditadas y testimonios coetáneos de símbolos. CarlosIII tiene evidencia sigilar903/912/921, pendiente de reproducción de licencia verificada. El sello deRobertoII mostrado en996–999 es una referencia posterior de1006–1030, no una bandera adoptada entonces.
- [ ] Afinar fragmentación y control territorial: culturas, asentamientos y agregados no equivalen a Estados nacionales. Sedes no inventan límites; puntos regionales no son frentes ni batallas continuas.
- [ ] Mantener exclusiones visuales: objetos sin efigie, escenas sin figura individual y retratos de otra persona no deben volver a las fichas. Las decisiones están en cada dossier.
- [ ] Esperar el aviso del propietario sobre la publicación; no sondearActions/Pages.
- [ ] Continuar antes de900 sólo por nuevo encargo; siguen siendo instantáneas aproximadas.

## Entrega anterior · 0.26.0 · ampliación hasta 1000

- [x] Cartografía e identidades anuales1000–1099; conservar datos posteriores.
- [x] Autoridades, imágenes y símbolos documentados, sin anacronismos.
- [x] Instituciones, sedes y contextos del sigloXI.
- [x] Auditoría nominal, pruebas, conservación y documentación.
- [x] Entrega preparada enmain y8.020 recursos verificados; confirmar coincidencia conorigin/main en el cierre, sin esperarActions/Pages.


Cierre local: 210 pruebas en50 archivos, tipos, compilación e integridad correctos. Cinco recorridos focales de navegador correctos; dos del sigloXI repetidos tras ajustar la disposición de retratos con pie de imagen. Capturas de escritorio, móvil y créditos revisadas. Hechos anteriores conservados, trece geografías idénticas y713 componentes contrastados con fuente.

## Revisión solicitada después de1000 · 0.26.1

Revisar todos los rangos de existencia; los años citados son observaciones, no límites de corrección. Evidencia y contenido por entidad dentro de su carpeta dePaíses, respetando la compilación y los medios con licencia.

- [x] ProvinciasUnidas neerlandesas: bandera y estatúderes con ese título, períodos sin estatúder y cargos provinciales distintos.
- [x] Luisiana francesa: símbolo adecuado por fechas y administración, incluida la situación de1802.
- [x] ProvinciasUnidas delRío de laPlata: banderas, juntas, triunviratos, directorio, presidencia y períodos sin autoridad nacional.
- [x] Paraguay yUniónSuecia/Noruega: símbolos por fechas y función; no copiar la enseña de1844 a1830.
- [x] Urgel,Empúries,Portugal,UniónIbérica,Georgia yNóvgorod: buscar bandera/armas con testimonio temporal. No convertir una reconstrucción o una imagen posterior en uso probado del siglo citado.
- [x] Pruebas y fichas por rango completo; documentación y catálogo porPaíses actualizados.

Comprobaciones:215 pruebas/51 archivos y tres recorridos de navegador correctos; dieciséis comprobaciones focales finales correctas tras completar ventanas paraguayas. Tipos y compilación correctos. Preparación repetida con nueve recursos idénticos byte a byte; originales de entidades y sus copias comprobados. Integridad final:77 datos,11 franjas y7.932 medios. 8.020 recursos preparados enGit comprobados; 70 originales únicos comprobados enGit y protegidos contra normalización. Confirmar coincidencia remota al cerrar; no esperarActions/Pages.

Pendientes delimitados: ampliar el resto de principados rusos y encontrar testimonios de uso coetáneo donde ahora sólo hay atribuciones o reconstrucciones. La candidata paraguaya1970–2013 sin fuente de insignia se mantiene excluida. No se ha certificado continuidad de banderas nacionales en todas las entidades medievales.

## Entrega anterior · 0.25.0 · ampliación hasta 1100

- [x] 541 intervalos originales,65 reglas e identidades anuales1100–1199. Doce geografías previas idénticas byte a byte y541 coordenadas/índices nuevos contrastados con la fuente fijada.
- [x] 357 intervalos de cargos seleccionados,67 de adquisición regional y196 retratos/efigies adoptados. 228 archivos recuperados;32 pares rechazados tras inspección visual,14 efigies rotuladas y decisiones persistentes.
- [x] Cinco ventanas de símbolos y siete casos pendientes documentados; sin retrotraer emblemas modernos o sin testimonio suficiente.
- [x] 39 registros institucionales,51 sedes/cortes y18 contextos con nueve puntos regionales. Transiciones de fuente y agregados explicados, sin inventar fronteras.
- [x] Auditoría nominal del siglo, conservación y catálogo regenerado:1.074 claves,16.165 mandatos,3.285 carpetas y7.715 medios.
- [x] 206 pruebas/49 archivos correctos, con17 comprobaciones focales finales tras corregir un final de precisión anual de1146. Tipos y compilación correctos. Cuatro recorridos de navegador correctos: dos históricos y dos de carga/pausa/error, incluido1100. Capturas de escritorio, globo y móvil revisadas.
- [x] Integridad SHA-256 de75 datos,11 franjas tipográficas y7.715 medios; hechos previos de mandatos y símbolos conservados, permitiendo añadir retratos.
- [x] 7.801 recursos preparados enGit comprobados byte a byte. Entrega0.25.0 preparada paraorigin/main; confirmar la coincidencia del envío al cerrar, sin esperar ni sondearActions/Pages.

Fuentes y alcance: [RESEARCH-1100.md](docs/RESEARCH-1100.md). [REVIEW-1100-1199.json](docs/REVIEW-1100-1199.json):13.847 entidades/año,9.833 sin autoridad,13.767 sin símbolo y113 personas/órganos sin retrato entre los activos. Inventario ampliado del catálogo:121 personas sin retrato; sedes adicionales aparte. Disponibilidad, no censo mundial exhaustivo.

### Pendientes explícitos del siglo XII

- [ ] Completar las carencias nominales de la auditoría y los candidatos aún sin fechas del oficio. Incluye IngeI/SverkerI deSuecia, Fujiwara delnorte, príncipes deKiev con reinados interrumpidos y algunas series guríes, chaulukya/chahamana y zanguíes. No obtener mandatos del nacimiento/muerte ni de otra dignidad.
- [ ] Completar bibliografía y retratos individuales acreditados. No volver a mostrar la moneda deBohemundoV paraBohemundoIV, templos, placas, caligrafía, monedas no identificadas o escenas sin figura individual. Conservar las exclusiones025 y las anteriores.
- [ ] Resolver las siete referencias de símbolos pendientes enreview-025-symbols.json: Francia, águila imperial, Portugal, Song, Jin, papado yJapón. No confundir un testimonio de flor de lis con un paño azul uniforme, ni el monHōjō con el gobiernoTaira/Minamoto.
- [ ] Obtener contornos propios: Song1127–1138, Egipto1171–1176, condado portugués, Sicilia temprana, Sajonia/Bohemia, Edesa después de1144 y reino costero después de1187. Sedes y reglas no sustituyen a superficies documentadas. Resolver fragmentación selyúcida y remanentes almorávides.
- [ ] Afinar fases y frentes de los conflictos; los puntos regionales no son batallas continuas durante todo su intervalo. Completar rivales pontificios, ramas territoriales y cronologías con variantes.
- [ ] Continuar hacia1000 sólo por nuevo encargo; las instantáneas anteriores a1100 no son revisión anual terminada.
- [ ] Publicación remota pendiente del aviso del propietario, sin esperar ni sondearActions/Pages.

El aro de carga y todos los pendientes anteriores se conservan.

## Entrega anterior · 0.24.0 · ampliación hasta 1200 y aro de carga

- [x] 862 intervalos originales y 84 reglas de identidad; navegación anual hasta 1200. Once geografías anteriores idénticas byte a byte.
- [x] 336 intervalos de cargos seleccionados, 118 de adquisición regional y 237 retratos/efigies adoptados. Diez monedas sin retrato individual acreditado retiradas; dos efigies suecas rotuladas como numismáticas.
- [x] Diez ventanas de símbolos, tres archivos nuevos y nueve candidatos pendientes/no adoptados.
- [x] 44 registros institucionales, 45 sedes/cortes y 19 contextos con 13 puntos regionales.
- [x] Auditoría nominal del siglo y conservación de hechos anteriores. Catálogo regenerado: 1.020 claves, 15.741 mandatos y 3.232 carpetas.
- [x] Aro de carga en reproducción, incluso para saltos manuales; ficha estable durante la espera, última petición prioritaria, pausa y recuperación tras error comprobadas. Movimiento reducido y anuncio accesible.
- [x] 202 pruebas/48 archivos correctos, tipos y compilación correctos. Cinco recorridos de navegador: dos históricos, dos de carga/errores y uno de persistencia durante reproducción. Capturas de escritorio, globo móvil y aro revisadas.
- [x] Integridad SHA-256 de 73 datos, 11 franjas tipográficas y 7.487 medios. Hechos anteriores conservados y once geografías previas idénticas byte a byte; documentación actualizada.
- [x] 7.571 recursos de datos, tipografías y medios comprobados byte a byte en Git. Entrega 0.24.0 preparada para origin/main; confirmar la coincidencia del envío al cerrar, sin esperar Actions/Pages.

Fuentes y alcance: [RESEARCH-1200.md](docs/RESEARCH-1200.md). Auditoría [REVIEW-1200-1299.json](docs/REVIEW-1200-1299.json): 13.172 entidades/año, 9.283 sin autoridad, 12.458 sin símbolo y 95 personas/órganos sin retrato entre los activos del mapa. Inventario ampliado del catálogo: 109 personas sin retrato. Sedes adicionales aparte; no es un censo mundial exhaustivo.

### Pendientes explícitos del siglo XIII

- [ ] Completar inventarios nominales de autoridades, símbolos y retratos; regencias, ramas locales, obediencias y candidatos rivales todavía parciales. No sustituir imágenes ausentes por objetos sin un retrato individual acreditado.
- [ ] Obtener contornos propios y frentes: agregado mongol tardío, etiquetas latinas/nicenas prolongadas hasta 1278, transiciones Jin/Jorezm y Sicilia/Nápoles siguen condicionados por la periodización de fuente. Sedes y reglas de identidad no inventan sus superficies.
- [ ] Resolver los nueve casos de símbolos pendientes/no adoptados, con testimonio temporal y función; no retrotraer diseños nacionales o emblemas tardíos.
- [ ] Contrastar variantes cronológicas Zagüe, Malí, Sukhothai y primeros poderes americanos; completar Goryeo y su gobierno rival de 1269. No deducir mandatos de fechas de nacimiento/muerte.
- [ ] Afinar puntos de conflicto y fases: referencias regionales no significan batalla continua ni frente exacto durante todo el intervalo del contexto.
- [ ] Completar variantes por edad de los retratos e identificar materialmente sellos, efigies y pinturas posteriores.
- [ ] Continuar hacia 1100 sólo por nuevo encargo; las instantáneas previas a 1200 no constituyen una revisión anual completada.
- [ ] Publicación remota pendiente del aviso del propietario; no esperar ni sondear Actions/Pages.

Los pendientes anteriores continúan abiertos.

## Entrega anterior · 0.23.0 · ampliación hasta 1300

Continuar con 1300–1399, conservando datos y funciones posteriores. Autoridades, símbolos y contexto fechados; auditar huecos. Comprobar localmente y subir sin esperar Actions/Pages.

- [x] Geometría e identidades anuales: 774 intervalos originales y 70 reglas; diez geografías previas idénticas.
- [x] 241 intervalos de cargos seleccionados, 154 de adquisición regional y 192 retratos adicionales. 11 ventanas de símbolos, tres archivos nuevos y nueve casos pendientes/no adoptados.
- [x] 34 registros institucionales, 35 sedes/cortes, 16 contextos y siete puntos regionales de conflictos. Ming y Goryeo seleccionables por sede sin inventar contornos ausentes.
- [x] Auditoría nominal de los cien años y conservación de todos los hechos previos de mandatos y símbolos. Alias de artículos resueltos antes de verificar identidades humanas.
- [x] 198 pruebas/47 archivos correctos, con repeticiones focales; tipos y compilación correctos. Dos recorridos de navegador en 2D/globo móvil correctos y capturas revisadas con retratos cargados y cámara en reposo.
- [x] Integridad SHA-256 de 71 datos, 11 franjas tipográficas y 7.237 medios. Límites de cobertura de los mandatos nuevos diferenciados de fechas documentadas de acceso o cese.
- [x] 7.319 recursos de datos, tipografías y medios comprobados byte a byte en Git. Entrega 0.23.0 preparada para origin/main; confirmar coincidencia del envío al cerrar, sin esperar Actions/Pages.

Auditoría: [REVIEW-1300-1399.json](docs/REVIEW-1300-1399.json), 14.747 entidades/año, 10.961 casos sin autoridad, 13.984 sin símbolo y 65 personas/órganos sin retrato entre los registros activos. Sedes adicionales contadas aparte. No equivale a un censo mundial exhaustivo. Fuentes y preparación: [RESEARCH-1300.md](docs/RESEARCH-1300.md).

### Pendientes explícitos del siglo XIV

- [ ] Completar los inventarios nominales de autoridades, símbolos y retratos; regencias, poderes locales, ramas germanas y obediencias pontificias rivales todavía parciales.
- [ ] Acreditar los nueve casos de símbolos pendientes/no adoptados; no quitar avisos para forzar una bandera.
- [ ] Obtener contornos regionales y frentes propios. Fuente Yuan prolongada hasta 1374, Goryeo sin contorno separado antes de 1363 y etiqueta Kenmu prolongada hasta 1343: sedes y resolución de identidad no corrigen por sí solas toda la geografía.
- [ ] Completar variantes cronológicas de retratos, regencias, sedes itinerantes y fuentes divergentes de fechas; no tratar un retrato de época como imagen exacta de cada edad.
- [ ] Resolver agregados dinásticos, mayas, nórdicos y arqueológicos; no convertirlos en un país de un solo gobernante ni interpretar el nombre Aztec Regional System como imperio mexica.
- [x] Nuevo encargo hasta 1200 atendido en 0.24; las instantáneas anteriores a 1200 siguen fuera de la revisión anual.
- [ ] Publicación remota pendiente del aviso del propietario; no esperar ni sondear Actions/Pages.

Los pendientes anteriores continúan abiertos.

## Entrega anterior · 0.22.0 · ampliación hasta 1400

Continuar con1400–1499, conservando los datos posteriores. Autoridades y símbolos fechados, formas políticas, sedes y contexto; auditar carencias. Comprobar localmente y subir sin esperar Actions/Pages.

- [x] Geometría e identidades anuales:880 intervalos originales y60 reglas; nueve geografías previas idénticas.
- [x] 206 intervalos seleccionados,94 de adquisición regional y147 retratos nuevos.13 ventanas de símbolos, dos archivos nuevos y siete casos no adoptados/pendientes.
- [x] 30 registros institucionales,33 sedes/cortes y16 contextos con10 puntos regionales de conflictos.
- [x] Auditoría, conservación, pruebas y documentación:194 pruebas/46archivos, tipos y compilación correctos. Dos recorridos de navegador correctos; repetición móvil esperando a la cámara en reposo para revisar el territorio visible.
- [x] Integridad SHA-256 de69datos,11franjas tipográficas y7.042medios. Hechos previos conservados y nueve geografías anteriores idénticas. Catálogo regenerado:3.050carpetas.
- [x] 7.122 recursos de datos, tipografías y medios preparados en Git comprobados byte a byte. Entrega0.22.0 preparada para origin/main; confirmar el resultado del envío al cerrar, sin esperar Actions/Pages.

Los pendientes anteriores continúan abiertos.

Auditoría: [REVIEW-1400-1499.json](docs/REVIEW-1400-1499.json),13.350 entidades/año,10.075 casos sin autoridad,12.288 sin símbolo y38personas/órganos sin retrato entre las fichas disponibles. No equivale a un censo mundial exhaustivo. Fuentes y preparación en [RESEARCH-1400.md](docs/RESEARCH-1400.md).

### Pendientes explícitos del siglo XV

- [ ] Completar el inventario nominal de autoridades y símbolos; regencias, obediencias pontificias rivales, ramas germanas y administraciones locales todavía parciales.
- [ ] Obtener contornos regionales y frentes; resolver agregados dinásticos, persistencias de fuente y etiquetas anacrónicas sin fabricar límites. Los puntos y sedes no son superficies.
- [ ] Acreditar los siete casos de símbolos no adoptados/pendientes; no quitar avisos de fuente insuficiente para forzar una bandera.
- [ ] Completar retratos y variantes por edades. Las51 personas no recuperadas en la adquisición y las38referencias finales del mapa son inventarios distintos.
- [ ] Revisar la publicación cuando el propietario avise; no esperar Actions/Pages.

## Entrega anterior ·0.21.0 · ampliación hasta 1500

El propietario solicita continuar con 1500–1599. Mantener datos y funciones posteriores, ampliar autoridades y símbolos con fechas y fuentes, contexto y formas políticas, y auditar los huecos. Comprobar localmente y subir sin esperar Actions/Pages.

- [x] Geometría e identidades 1500–1599: 826 intervalos originales y 65 reglas; ocho recursos geográficos anteriores idénticos.
- [x] 224 intervalos de cargos revisados, otros 153 de adquisición regional y 192 retratos nuevos. No censo mundial exhaustivo.
- [x] 21 ventanas de símbolos, 39 registros institucionales, 37 sedes/cortes y 17 contextos con 11 puntos regionales de conflictos.
- [x] Auditoría, conservación, pruebas y documentación. 190 pruebas en 45 archivos, tipos y compilación correctos; dos recorridos de navegador correctos tras ajustar la fecha de una prueba de filtros. Revisión visual de mapa y globo móvil, con imágenes cargadas.
- [x] Integridad de 67 datos, 11 franjas tipográficas y 6.893 medios por SHA-256; hechos anteriores de mandatos/símbolos conservados y ocho geografías anteriores idénticas. Catálogo regenerado: 2.961 carpetas.
- [x] 6.971 recursos preparados en Git comprobados byte a byte. Entrega 0.21.0 preparada para origin/main; confirmar el resultado del envío al cerrar. Publicación pendiente del aviso del propietario, sin esperar Actions/Pages.

Auditoría: [REVIEW-1500-1599.json](docs/REVIEW-1500-1599.json), 11.630 entidades/año, 7.611 casos sin autoridad, 9.955 sin símbolo y 60 personas/órganos sin retrato en los registros disponibles. Catálogo: 752 claves y 14.592 mandatos. Fuentes y procedimientos en [RESEARCH-1500.md](docs/RESEARCH-1500.md).

### Pendientes explícitos del siglo XVI

- [ ] Completar autoridades y símbolos del inventario nominal; más regentes, ramas germanas, gobiernos locales y cronologías intranuales. No asumir ausencia histórica por ausencia de datos.
- [ ] Geometrías individuales de Estados agrupados, reino de Vilcabamba y poderes sucesores de Songhai; cortes itinerantes y exilios. Las notas no sustituyen fronteras regionales que faltan.
- [ ] Resolver los nueve casos de símbolos no adoptados/pendientes; no retrotraer banderas Qing, coreanas, rusas, mexicanas o municipales modernas.
- [ ] Completar retratos y variantes por etapas; las 86 personas no recuperadas por la adquisición no equivalen al inventario final de 60 referencias sin retrato en las fichas activas del mapa.
- [ ] Comprobar la publicación solamente cuando el propietario avise del despliegue. No esperar ni sondear Actions/Pages.

Los pendientes de versiones anteriores siguen abiertos.


## Entrega anterior ·0.20.0 · ampliación hasta1600

El propietario solicita continuar con1600–1699. Mantener filtros, fichas persistentes y datos posteriores. Incorporar cartografía anual, identidades, autoridades con títulos y retratos, símbolos documentados, contexto y formas políticas; registrar carencias reales. Comprobar localmente y subir sin esperarActions/Pages.

- [x] Navegación anual 1600–1699: 783 intervalos componentes originales y 67 reglas de resolución; archivos anteriores conservados.
- [x] 196 intervalos de cargos revisados, adquisición regional y 143 retratos acreditados. Títulos, regencias, autoridades rivales y precisión explícitos; no censo mundial completo.
- [x] 31 ventanas de símbolos, 37 registros institucionales, 30 sedes/capitales y 15 contextos, con siete puntos regionales de conflictos. No se inventan frentes ni símbolos nacionales.
- [x] Auditoría nominal [REVIEW-1600-1699.json](docs/REVIEW-1600-1699.json): 11.079 entidades/año, 7.540 casos sin autoridad, 8.643 sin símbolo y 58 personas/órganos sin retrato entre los registros disponibles.
- [x] Conservación de todos los hechos previos de mandatos y símbolos, permitiendo completar imágenes; siete recursos geográficos anteriores idénticos. Administradores de respaldo limitados al intervalo de fuente, sin retroyección colonial.
- [x] 186 pruebas en 44 archivos, tipos y compilación correctos. Dos recorridos de navegador correctos en 1,9 min; repetición focal final de 42 s tras limitar administradores, con imágenes portuguesas cargadas y revisión visual.
- [x] Integridad local: 65 datos, 11 franjas tipográficas y 6.694 medios verificados por SHA-256. Documentación y versión 0.20.0 preparadas.
- [x] 6.770 recursos de datos, tipografías y medios preparados en Git comprobados byte a byte. Entrega 0.20.0 preparada para origin/main; el resultado del envío se confirma al cerrar. No esperar Actions/Pages; publicación pendiente del aviso del propietario.

### Pendientes que no se dan por completados

- [ ] Completar inventario mundial 1600–1699, gobiernos regionales y administraciones locales; regencias, calendarios y fechas intranuales aún parciales.
- [ ] Acreditar símbolos Ming, safávidas, mogoles, africanos y otros diseños pendientes. No sustituirlos por banderas posteriores ni aceptar obras propias sin testimonio de uso.
- [ ] Obtener fronteras individuales de Estados germanos, frentes de guerras y facciones del Kongo, y resolver identificadores/cronologías compartidos como Mogulistán. Los puntos no son frentes.
- [ ] Ampliar retratos por edades/décadas y completar ausencias. Un retrato representativo no acredita apariencia exacta en cada año.
- [ ] Revisar publicación cuando el propietario confirme el despliegue.

Fuentes y preparación en [RESEARCH-1600.md](docs/RESEARCH-1600.md); continuidad en sección 32 de agentes.md.

Los pendientes de0.19 y anteriores continúan abiertos.


## Entrega anterior · 0.19.0 · ampliación hasta 1700 y filtros separados

El propietario solicita ampliar 1700–1799, priorizando símbolos y soberanos de los Estados germanos y de Asia, y corregir huecos de símbolos todavía presentes en1800. Añadir un botón de embudo a la izquierda deCapas; trasladar allí forma política/régimen, alianzas/organizaciones y color del mapa. Ocultar categorías con cero entidades en el año consultado. Conservar el filtro activo entre fechas mediante un aviso y opción de quitarlo si deja de tener resultados, sin llenar el selector de opciones vacías. Mantener comprobaciones locales y envío sin esperarActions/Pages.

- [x] Separar Filtros yCapas; opciones positivas, aviso/reset del filtro vacío, foco y móvil comprobados.
- [x] Geometría anual1700–1799:853 intervalos adicionales y58 reglas de identidad; conservación de los archivos anteriores comprobada.
- [x] Ampliar autoridades:242 intervalos revisados más33 deIndia/Siam, adquisición general y retratos disponibles. Títulos y precisión explícitos; no un censo mundial completo.
- [x]39 ventanas de símbolos;6.540 medios totales,236 adicionales. Mon, sellos, armas y pabellones identificados; nueve candidatos pendientes/rechazados. Fragmento deSunjo sin rostro excluido como retrato identificativo, con fuente.
- [x]29 formas institucionales,32 referencias urbanas y15 contextos nuevos; seis puntos regionales de conflictos.16 sedes soberanas de Estados germanos agrupados son buscables y abren ficha; no aportan fronteras individuales.
- [x] Auditoría anual por ruta real en[REVIEW-1700-1799.json](docs/REVIEW-1700-1799.json):12.659 entidades/año;8.747 casos sin autoridad,9.945 sin símbolo y81 personas/órganos sin retrato.
- [x]182 pruebas/43 archivos y tipos correctos. Cuatro recorridos de navegador correctos en3,8min: filtros, cero resultados, móvil, sedes germanas, fichas persistentes, autoridades y símbolos; revisión visual. La prueba antigua de inicio1800 se actualizó a1700 y el recorrido completo final pasó.
- [x] Integridad local:63 recursos de datos,11 franjas tipográficas y6.540 medios conSHA-256 correctos. Compilación final correcta. Repetición focal del nuevo siglo después del ajuste documental de imágenes:1 recorrido correcto en45,7s.
- [x]6.614 recursos de datos, tipografías y medios preparados enGit comprobados byte a byte. Entrega0.19.0 preparada paraorigin/main; el resultado del envío se confirma al cerrar. Publicación pendiente del aviso del propietario; no esperarActions/Pages.

### Pendientes de investigación que siguen abiertos

- [ ] Completar el inventario mundial1700–1799: autoridades regionales, regencias, banderas/estandartes documentados, fechas intranuales y calendarios. Un hueco no demuestra ausencia de gobernante o de símbolo.
- [ ] Obtener contornos individuales fechados para los Estados germanos agrupados. No convertir las sedes en fronteras ni extrapolar un mapa de1783 a todo el siglo.
- [ ] Cotejar símbolos safávidas/afsháridas/zand, mogoles y dekanatos, así como numerosos Estados africanos. No aceptar categorías ficticias, archivos con fecha sólo en el título o diseños posteriores sin prueba de continuidad.
- [ ] Completar control territorial de guerras delXVIII con fuentes geométricas; los puntos regionales no sustituyen frentes. Mantener las carencias previas1800–1900.
- [ ] Revisar la publicación sólo cuando el propietario confirme el despliegue.

Preparadores, fuentes y límites en[RESEARCH-1700.md](docs/RESEARCH-1700.md); continuidad en sección31 deagentes.md.

## Entrega anterior · 0.18.0 · revisión de1800–1900 y formas de gobierno

Revisar banderas y autoridades, especialmente los ejemplos señalados de Europa, América y África. Incorporar clasificación política fechada y filtro de capas, y corregir/ampliar capitales, ciudades y presentación de ocupaciones/conflictos. No dar por completados huecos no investigados. Mantener la instrucción de subir tras comprobar localmente sin esperar Actions/Pages.

- [x] Corregir Habsburgo, Río de la Plata y prolongación de Helvética; relaciones administrativas de agregados coloniales.47 ventanas de símbolos revisadas con su tipo, fechas, autor y licencia. No equivale a completar todas las banderas.
- [x]70 intervalos revisados europeos/americanos y23 observaciones africanas, más correcciones focales y autoridades administrativas. Títulos soberanos, regencias y poder provincial diferenciados.60 retratos añadidos;546 claves y12.978 registros totales, no fichas completas.
- [x]62 categorías,509 registros de formas institucionales y filtro persistente deCapas/Instituciones. Serie separada V-Dem/OWID:209 claves y30.851 observaciones anuales1789–2025; no extrapolación2026 ni evaluación colonial heredada.
- [x]68 referencias urbanas fechadas anteriores a1886 y sedes regionales, además de las fuentes existentes. Corregida la selección de puntos con IDs transformados por el renderizador.
- [x]32 puntos de episodios y referencias regionales de conflictos; selección y ficha persistente. Franjas existentes disponibles también con organizaciones o colores económicos. No se han inventado frentes nuevos.
- [x] Auditoría anual1800–1900, catálogoPaíses, procedencia y documentación.61 recursos de datos,11 franjas tipográficas y6.304 medios verificados conSHA-256.
- [x] Tipos y compilación local correctos. Tres recorridos finales de navegador correctos en2,5min: móvil/globo, símbolos y títulos, filtro sin resultados y persistencia, clic real de ciudad y batalla, episodio inactivo, fuentes compactas y combinación de capas. Las comprobaciones se corrigieron para respetar queWDI empieza en1960.
- [x]179 pruebas en42 archivos correctas en el recorrido final completo. Siete comprobaciones focales adicionales correctas después de precisar límites de cobertura de mandatos. Tipos y compilación final correctos.
- [x]6.376 recursos de datos, tipografías y medios preparados enGit comprobados byte a byte. Entrega preparada paraorigin/main; confirmar el resultado delpush al cerrar, sin esperarActions/Pages. La publicación permanece pendiente del aviso del propietario.
- [ ] Revisar la publicación cuando el propietario confirme el despliegue.

### Revisión documental que continúa abierta

La disponibilidad anual está en[docs/REVIEW-1800-1900.json](docs/REVIEW-1800-1900.json). En1800 hay139 componentes/territorios,29 con símbolo y42 con autoridad; en1824 son164,36 y64; en1900 son176,164 y174. Los agregados de fuente no son un censo de Estados independientes. No llamar a estos años «completos».

- [ ] Completar el inventario mundial1800–1900 por regiones, priorizando los huecos nominales de la auditoría. Persisten7.362 casos anuales sin autoridad,9.914 sin símbolo y118 personas/órganos sin retrato dentro de los registros disponibles. Un retrato ausente no acredita inexistencia de imágenes históricas.
- [ ] Contrastar Wadai con bibliografía independiente: las fechas de varias sucesiones difieren, especialmente1834–1843. Se añadieron observaciones interiores sin rellenar años dudosos. Conseguir prueba histórica del diseñoWadai.png antes de incorporarlo.
- [ ] Bornu: no retrotraer al sigloXIX el símbolo descrito para1439. Sokoto: conseguir ejemplares militares documentados y distinguirlos de la bandera uniforme sin fuente. Valáquia anterior a1834: candidata ficticia rechazada. Registros de símbolos aceptados/rechazados en scripts/review-018-symbols.json.
- [ ] Completar otros Estados germanos, regentes y administraciones territoriales. Las fechas importadas de Moldavia/Valaquia requieren más contraste intranual y de calendarios; las fuentes de observaciones secundarias conservan su condición.
- [ ] Ampliar fases institucionales de las entidades todavía sin clasificación documentada y revisar los cruces no emparejados deV-Dem; no deducir ideología de colores ni usar etiquetas actuales retrospectivamente. La taxonomía es ampliable, no un listado exhaustivo de toda forma histórica.
- [ ] Ampliar capitales, ciudades y conflictos por época/región, con fuentes y precisión. Los32 puntos no cubren todas las guerras y no sustituyen geometría de control militar ausente. Completar frentes y ocupaciones sólo con límites acreditados.

Preparadores y alcance en[docs/REVIEW-0.18.md](docs/REVIEW-0.18.md); continuidad en sección30 deagentes.md. Las tareas anteriores abiertas siguen vigentes.

## Entrega anterior · 0.17.0 · ampliación hasta 1800

Se solicita ampliar 1800–1819 reduciendo uso de sesión. El propietario insiste en que siguen faltando fotos y banderas fácilmente localizables en diversas épocas: no dar por resuelto ese trabajo pendiente. Mantener las comprobaciones locales y terminar al confirmar el push, sin esperar Actions/Pages.

- [x] Adquisición aislada,543 claves y12879 registros; resolución anual1800–1819 y estados italianos propios. Conservados los hechos anteriores salvo el intervalo condensado erróneo dePitt, corregido con fuente institucional.
- [x] 49 imágenes raster y3SVG nuevos; símbolos reutilizados y omisión prusiana1820–1839 corregida. Doce fases de contexto, tres enlaces y colores franceses para estados clientes, sin convertirlos en colonias.
- [x] Auditoría nominal REVIEW-1800-1819.json:2958 entidades/año;2116 casos anuales sin autoridad,20 personas/órganos sin retrato y2668 sin símbolo.
- [x] 173 pruebas/41 archivos, tipos y compilación correctos. Un recorrido de navegador correcto en1,2min: Consulado/Imperio/Restauraciones, Italia y símbolos, España1812, ficha persistente hasta1820; globo y móvil.
- [x] Integridad de57 datos,11 franjas tipográficas y6201 medios verificada;6269 recursos preparados en Git comprobados. Entrega0.17 preparada para main; confirmar push al cerrar, sin esperar Actions/Pages.
- [ ] Revisar publicación cuando el propietario confirme el despliegue.
- [ ] Corrección transversal posterior de fotos y banderas de todas las épocas, incluidos casos fácilmente localizables. No limitarla a la última franja.

## Entrega anterior · 0.16.0 · ampliación hasta 1820

El propietario acepta posponer correcciones de huecos anteriores y solicita ampliar 1820–1839 con uso mínimo de sesión. Reutilizar los preparadores, documentar carencias reales y verificar localmente antes de subir. No esperar Actions/Pages.

- [x] Adquisición aislada, cargos históricos y comprobación de todos los hechos anteriores de mandatos/símbolos. 492 claves y12.621 registros; series parciales.
- [x] Resolución anual1820–1839, regímenes, sucesiones y regencias. Gran Colombia1831–1833 y Grecia conservan advertencias de geometría/denominación pendiente.
- [x] Símbolos disponibles,95 imágenes adicionales,14 fases documentales y3 enlaces. Pacífico: componentes originales y ventanas locales desde1820; sin anticipar administradores.
- [x] Auditoría nominal docs/REVIEW-1820-1839.json;170 pruebas/40 archivos, tipos y compilación correctos. Un recorrido de navegador correcto en1,1min: Francia1820/1830, España1833, México1822 yQing1839→1840; globo y móvil.
- [x] Integridad de56 datos,11 franjas tipográficas y6149 medios verificada;6216 recursos preparados en Git comprobados. Entrega preparada para main; confirmar push al cerrar y no esperar Actions/Pages.
- [ ] Completar los huecos nominales después, como ha indicado el propietario.
- [ ] Revisar publicación cuando el propietario confirme el despliegue.

## Entrega anterior · 0.15.0 · ampliación hasta 1840

El propietario solicita avanzar hasta 1840 con el uso de sesión disponible. Esta petición sustituye la recomendación previa de cerrar primero todos los huecos de 1860, sin convertirlos en completados. Subir tras comprobaciones locales, sin esperar Actions/Pages.

- [x] Adquisición aislada de 1840–1859 y consultas de cargos históricos para recuperar monarquías de 1840–1879. Se conservan candidatos y declaraciones en scripts/historical-offices-015-research.json; 101 observaciones revisadas.
- [x] Joseon corregido a Q28179; el Q28405 original se conserva como dato erróneo de fuente, referido a Gojoseon antiguo. Hong Xiuquan asignado al Taiping, no al Qing.
- [x] Ventanas de identidad de Francia, España, Cerdeña, Dos Sicilias, Estados Pontificios, India, Egipto, Haití y otras entidades. Hungría revolucionaria separada del QID anacrónico austrohúngaro, con autoridades todavía pendientes.
- [x] Regencias, Ejecutivo provisional francés, sucesiones hawaianas y fechas gregorianas rusas distinguidas. Precisión anual/mensual respetada también en la cronología.
- [x] Doce ventanas de símbolos, siete SVG nuevos y 180 imágenes raster adicionales, incluidos dos retratos fechados de Victoria. 6.054 medios acreditados en total.
- [x] Diecisiete fases de contexto, diecisiete registros históricos y cuatro enlaces completos de navegación. No se inventan frentes de guerras o rebeliones ausentes en la fuente.
- [x] Referencias del Pacífico y trece periodos de separación de componentes desde 1840; mismas coordenadas, sin duplicación ni atribuir colonizadores posteriores a los tramos locales anteriores.
- [x] Auditoría nominal por la ruta real: 1840–1859 incluye 3.308 entidades/año, 2.003 casos anuales sin autoridad documentada, 18 personas/órganos sin retrato y 2.637 casos anuales sin símbolo. Ver docs/REVIEW-1840-1859.json.
- [x] Nueva auditoría de 1860–1879: casos anuales sin autoridad reducidos de 1.646 a 1.467. No equivale a una revisión mundial cerrada.
- [x] Tipos, 167 pruebas, sintaxis de preparadores y conservación de los hechos de mandatos/símbolos de 1880+ verificados. 55 recursos, 11 franjas tipográficas y 6.054 medios con huellas comprobadas. Compilación correcta en .cache/build-015-final.
- [x] Dos recorridos finales de navegador correctos: Francia1840–1855, regímenes, conflictos, Joseon, globo, retratos fechados, regencias, Hawái y Rusia; revisión visual móvil.
- [x] Límites de observación1859 señalados en los tres mandatos manuales que continúan fuera de esa ventana.
- [x] Comprobaciones cerradas y entrega preparada para origin/main. Confirmación del push en el cierre de la entrega; no esperar al despliegue.
- [ ] Revisar el despliegue público cuando el propietario confirme Actions/Pages.
- [ ] Completar los huecos nominales de Estados germanos, gobiernos locales, regentes, África y Asia; no sustituirlos automáticamente por el jefe de un país actual.
- [ ] Completar variantes de símbolos y retratos por etapas de los soberanos incorporados; las imágenes disponibles no acreditan cobertura visual de cada lustro.
- [ ] Contrastar fechas intranuales texanas, proclamación imperial haitiana y calendarios orientales. Las observaciones conservadoras no son fechas de acceso completas.
- [ ] Resolver geometrías de Prusia y otros Estados agrupados, frentes bélicos y de rebeliones y pueblos omitidos. No dibujar un contorno moderno superpuesto para simular una solución.

El catálogo contiene 465 claves y 12.170 registros de mandatos, no 465 fichas completas. Fuentes, preparación y límites en docs/RESEARCH-1840.md. Los pendientes de Mozambique, variantes tempranas de Franco y actualización del frente ucraniano siguen abiertos en el encargo anterior.

## Encargo vigente · 0.14.0 · correcciones y ampliación parcial hasta 1860

Cierre preparado el 26/10/2026. Comprobar localmente, enviar y terminar sin esperar ni consultar Actions/Pages. El propietario verificará la publicación.

- [x] Identificadores históricos de texto conservados con promoción en el renderizador. Clic real sobre Francia en 1885 y cambio 1885/1886; no se simplifican coordenadas.
- [x] Autoridades ordenadas por inicio más reciente; cargos y presidencia anual suiza conservados.
- [x] 32 ventanas de retratos por etapas: Franco desde 1950, Putin, Isabel II, Trump y mandatos no consecutivos. Fechas y licencias visibles; cobertura ausente rotulada.
- [x] Retratos de Vietnam 2007 y Sadi Carnot en Francia 1888. Sharma 1992 con encuadre de su juramento y retrato individual desde 1993, sin el sello postal.
- [x] Cinco observaciones de control ruso en Ucrania desde 2022, integradas en el mapa seleccionable; franjas opcionales, costa compartida Natural Earth, sin la antigua máscara CShapes Crimea en esa ventana. Fecha e incertidumbre visibles.
- [ ] Actualizar la observación de Ucrania a una fuente de control más reciente con licencia reutilizable. La referencia de 2026 es 17/12/2025; no afirmar que es el frente de octubre de 2026. Kherson 2022 está dentro de la incertidumbre mínima de 7 km; no inferir su control municipal del polígono.
- [x] Referencias fechadas del Pacífico y nombres históricos canónicos. Guam y Nueva Caledonia separados del agregado sin duplicar ni modificar componentes. Los suplementos de independencia ya disponibles tienen prioridad sobre referencias de omisiones.
- [ ] Completar autoridades locales, condominios, fechas intranuales y referencias de otros archipiélagos. La selección de una referencia contemporánea no acredita fronteras insulares históricas exactas.
- [ ] Mozambique: continúa pendiente un retrato individual reutilizable de Maria Benvinda Levi. No recortar la escena ND con Macut. Daniel Chapo ya tiene imagen individual.
- [ ] Acreditar variantes tempranas de Franco, especialmente 1936–1949. Las dos candidatas investigadas con advertencias de derechos no se incorporan automáticamente.
- [x] Incorporación aislada 1860–1879: 425 claves y 11.555 mandatos totales del catálogo, curador inicial, recuperación de inicios explícitos, 225 retratos adquiridos y siete ventanas adicionales de símbolos. Preservados mandatos 1880+.
- [x] Contexto: 16 fases, 15 registros históricos y seis relaciones, sin modificar eventos anteriores ni inventar geometrías de frentes.
- [ ] **La revisión mundial 1860–1879 sigue incompleta.** Auditoría nominal en docs/REVIEW-1860-1879.json: 2804 entidades/año; 1646 casos anuales sin autoridad; 17 personas u órganos sin imagen; 2023 casos anuales sin símbolo.
- [ ] Prusia 1860: la fuente Clio la agrupa en la Confederación Germánica; no existe un polígono prusiano separado en esa fecha. Tener autoridades PRUSSIA no resuelve la frontera. No asignar toda la Confederación a Prusia ni superponer un contorno moderno. Investigación CShapes Europa en docs/EUROPE-1860-GEOMETRY-RESEARCH.md; no autoriza una sustitución global automática.
- [ ] Completar las monarquías y autoridades locales pendientes de África, Asia, América y Oceanía; entre otros, las ventanas anteriores a 1880 de Irán, Etiopía, Joseon, Hawái y Nepal. No bajar todavía otra tanda dando esta por cerrada mundialmente.
- [x] Versión 0.14.0, manifiestos, catálogo Países con variantes de retratos, documentación y preparadores registrados. 54 recursos, 11 franjas tipográficas y 5.867 medios con huellas comprobadas.
- [x] Tipos y 160 pruebas correctas. Scripts de preparación analizados sin errores de sintaxis. Compilación local correcta en .cache/build-014-final.
- [x] Navegador: clic real1885, inversión1885/1886, globo, selecciónGuam2016, autoridadesUSA1860/Francia1871 y retratosCarnot/Vietnam/Sharma/Trump; fecha deUcrania y franjas verificadas. Dos recorridos focales correctos.
- [x] Cambios preparados y verificados para su envío a origin/main en esta entrega; el resultado de Git se confirma en el mensaje de cierre. La publicación sigue pendiente del aviso del propietario.

La mejora de selección no transforma la geometría Clio anterior a 1886 en una costa más detallada. Mantener separados fallo de identificación, resolución de la fuente y falta de un territorio en el inventario. Las carencias no se convierten en completadas al reanudar una sesión. Detalle: docs/DELIVERY-0.14.0.md.

## Encargo vigente · 0.13.0 · ampliación hasta 1880 y correcciones notificadas

El propietario confirma la publicación anterior y la considera válida. Ampliar1880–1899, conservar1900–actualidad y las particiones1940–1944. Añade errores de retratos/identidades y selección histórica deGroenlandia. Comprobar localmente, subir y terminar sin esperar ni sondearActions/Pages.

- [x] Adquisición aislada1880–1899 y tres curadores regionales; dos curadores adicionales de huecos, fuentes y precisión explícitas. No equivale a un censo completo de autoridades mundiales.
- [x] Resolver el cambio de fuente1885/1886, nombres/QID anacrónicos, imperios y colonias; no heredar estadísticas actuales ni políticos sucesores.
- [x] Símbolos acreditados:52 ventanas conservadoras. Transiciones deBrasil, Hawái yCorea con autoridades predecesoras rotuladas. Contexto23 fases,20 registros/seis enlaces y tres membresías tempranas deTripleAlianza.
- [x] Auditar la ruta real por año y conservar las carencias nominales:2.723 entidades/año,123 casos anuales sin autoridad,40 personas/órganos sin foto y530 casos anuales sin símbolo. Documentación enRESEARCH-1880 yREVIEW-1880-1899.json.
- [x] Francia1900:ÉmileLoubet con retrato acreditado; comprobado en la ficha real.
- [x] Irak2026: retiradoPopeTrump y adquirido retrato real deAliAlZaidi; elección deNizar y acceso deAli fechados por fuentes parlamentarias.
- [x] Tayikistán2026: retrato individual de mayor resolución deRasulzoda, comprobado en navegador.
- [x] Bután1970: billete sustituido por reproducción acreditada del retrato deJigmeDorjiWangchuck; no se presenta la foto del objeto2013 como foto del soberano vivo.
- [x] EEUU2020: eliminadoPhilBaker ficticio, preservadoTrump con foto; también retiradoDavid ficticio deGBR. Filtro humano/exclusiones antes de inferir sucesores; cinco regresiones sin conexión correctas.
- [x] Bangladesh/Vietnam2016: retratos acreditados, ambos presidentes vietnamitas y cese deSang2/4/2016; comprobados en ficha real.
- [x] Groenlandia: referenciaNaturalEarth1886–2019 por omisión deCShapes, ámbitos/etapas danesas diferenciados. Clic real2016→1970→1942→2016 correcto; no se atribuye al controlador alemán.
- [x] India:12 personas antes sin retrato ya incorporadas, incluidosSingh/Patil2011. Ningún titular sin imagen en el catálogo disponible; no acredita que estén todos los cargos posibles.
- [x] Nepal: siete personas antes sin retrato incorporadas, incluyendo la nueva ventana1880; comprobadas las fichas actuales/históricas focales.
- [x] Mozambique: comprobado visualmente queDanielChapo ya tiene retrato individual correcto; la imagen grupal corresponde aMariaLevi. Fecha de nombramiento deLevi corregida17/1/2025 con posesión18/1 explicada.
- [ ] Mozambique: conseguir un retrato individual deMariaBenvindaLevi con licencia reutilizable acreditada. Se conserva la escenaND íntegra y rotulada conMacut; no recortarla ni darla por solución individual. Investigación enMEDIA-CORRECTIONS-0.13.
- [ ] Nepal:Rijal continúa sin integrar. CandidatoCommons con atribución genérica aOficina delPrimerMinistro, procedencia institucional exacta aún no confirmada. No reintroducirlo automáticamente como candidato verificado.
- [x] Manifiestos, versión0.13.0, catálogoPaíses, fuentes, manual yregistro de continuidad actualizados.366 claves/10.916 mandatos;5.613 medios(507SVG/5.106 raster),2.779 carpetas.
- [x] Tipos,154 pruebas/35 archivos, siete curadores puros/idempotentes y conservación de10.016 registros1900+ salvo correcciones explícitas. Originales cartográficos y particiones bélicas idénticos byte a byte.
- [x] Integridad49 datos/11 franjas/5.613 medios y compilación correcta en.cache/build-013-final.
- [x] Navegador: cuatro recorridos distintos correctos, repetición final1880 con bandera decodificada y captura móvil revisada. Entrega preparada para main; confirmar envío efectivo en el registro de cierre.
- [ ] Revisión pública sólo tras aviso del propietario. No esperar ni consultarActions/Pages al terminar la subida.

Continuidad: tres de los cuatro recorridos focales iniciales correctos: fuentes/capas, todos los retratos solicitados disponibles y clic real deGroenlandia. El recorrido1880 eligióBrasil al buscar«EstadosUnidos», contenido también en su nombre histórico; selector de prueba corregido para elegir el resultado exacto, sin alterar los nombres válidos. Repeticiones correctas, incluida decodificación de la bandera. No recompilar ni mezclar el directorio servido mientras se comprueba. La primera suite detectó expectativas anteriores a1880 y el verificador detectóIDs compartidos entre relaciones/registros deHawái; corregidos y repetición completa154/154 correcta. La regresión territorial detectó doble referencia deHawái1898: ahora sóloCShapes y transferencia exacta; no sobrecapas de costas diferentes.

Cierre: aplicación0.13.0 enviada correctamente aorigin/main en33637c5.5673 recursos de datos/fuentes/medios preparados enGit verificados porSHA antes del envío. No se ha esperado ni consultado el despliegue; pendiente únicamente el aviso del propietario. Los huecos documentales anteriores permanecen abiertos.

### Investigación pendiente de1880–1899

- [ ] Completar los123 huecos anuales nominales. Entre ellos: Wadai, Sokoto, Champasak, JabalShammar, Terengganu, Kelantan, Bornu, Lunda, Bima, Aceh yotras entidades;Bhután con gobierno dual anterior a1907. No inventar monarquía hereditaria ni Estado unitario para rellenar una celda.
- [ ] Resolver contornos ambiguos de«GermanAfrica» anterior a1884 y«TalpurDynasty»/Sindh-Khairpur. Son referencias de fuente, no territorios sin habitantes ni prueba de un soberano uniforme.
- [ ] Completar las40 imágenes y530 casos anuales sin símbolo del inventario, variantesQing anteriores a1889 y usos imperiales/civiles rusos diferenciados.
- [ ] Contrastar regencias, gobernadores y mandatos breves; regencia suazi, otros integrantes del triunviratoTRV, relevos deKedah yfechas americanas de precisión aún anual/mensual. Fuentes y límites enAUTHORITIES-1880-*.md.
- [ ] Fronteras propias de Estados omitidos, frentes coloniales/bélicos ylas carencias documentadas de entregas previas; los contextos nuevos no dibujan esos frentes.

## Encargo vigente · 0.12.1 · correcciones antes de ampliar fechas

El propietario confirma la publicación de0.12.0 y reproduce artefactos alemanes en1941–1944. Corregir primero particiones, fichas y retratos; **1880 queda aplazado**. Comprobar localmente, subir y terminar sin esperar Actions/Pages.

- [x] Verificar que los datos publicados coinciden con0.12.0: manifiesto y controles idénticos por SHA-256; no es una caché antigua.
- [x] Diagnosticar componentes remotos, costas independientes y franjas generadas antes de resolver el controlador final. Investigación en docs/WWII-CONTROL-RESEARCH.md.
- [x] Preparar instrucciones de transferencia1940–1944 sobre la misma tierra fechada; descartar celdas remotas y proteger países neutrales, conservar islas reales y estados clientes.
- [x] Garantizar una sola partición política y franjas recortadas al control final; regresiones geográficas. Navegador en curso, no marcado como terminado.
- [x] Unificar Autoridades: retrato, cargo, nombre y fechas; trasladar notas documentales extensas a Contexto sin perder fuentes ni incertidumbre.
- [x] Integrar los34 retratos suizos contrastados y corregir etiquetas de cargos colegiados/presidencia anual sin alterar mandatos.
- [x] Regenerar manifiestos/catálogo, actualizar versión/documentación y comprobaciones locales.
- [x] Preparar entrega a main con comprobaciones locales y registro de continuidad. La confirmación del envío corresponde al resultado de Git y al mensaje final.
- [ ] Revisar la publicación de0.12.1 sólo cuando el propietario confirme el despliegue o aporte un error; no sondear Actions/Pages.

Continuidad: rama codex/fix-wwii-partitions. Particiones generadas y conectadas a la ruta real del cargador, sin recalcular booleanas durante la visita. Auditoría GEOS: tierra conservada, sin nuevas áreas/solapamientos y franjas dentro de su controlador; regresiones1940–1944 incluidas.147 pruebas/33 archivos correctos y compilación correcta en .cache/build-0121-verified.34/34 retratos suizos adquiridos,194 etiquetas corregidas; fechas suizas conservadas. El navegador detectó la falta de autoridades1940+ en la nueva entidad eslovaca: corregida continuidadTiso/Tuka y sucesiónŠtefanTiso5/9/1944, con otro retrato acreditado y fuentesUSHMM/UPN. En total302 claves/10.246 mandatos/5.297 medios; sóloCHE ySVK-1939 cambian identidades. CatálogoPaíses generado; siete recorridos distintos correctos, incluida repetición final1940–1944(1,3min), datos/medios íntegros y5.353 recursos preparados enGit verificados. Revisadas capturas1942 con fronteras compartidas. Entrega local preparada para main; confirmar el resultado de Git en el mensaje final, sin confundirlo con despliegue. La suite inicial precedió a la regeneración del catálogo; una repetición simultánea a la compilación excedió5s en una prueba antigua de suplementos. Repetición completa posterior, sin esa competencia de recursos:147/147 correctas. Seis recorridos iniciales pasaron y uno detectó el hueco eslovaco; no se dio por terminado.

### Pendientes que esta corrección no convierte en completados

- [ ]1880: aplazado expresamente hasta corregir los errores actuales.
- [ ] Frentes con fecha propia1942–1944: invasión de la zonaVichy, liberación deFrancia/Benelux/Finnmark,RSI y control partisano. Las particiones corrigen artefactos, no la periodización desigual del inventario anual.
- [ ] Fuente propia para la frontera eslovaca, municipios/enclaves y corte1944; se mantiene la referencia1939 recortada y declarada.
- [ ] Completar series diarias suizas: faltan miembros en algunos años(por ejemplo, el mandato colegiado deMaxPetitpierre1950 en el inventario) y hay un intervalo genérico de presidenciaSchulthess1921–1931 que exige contraste y desglose. Los retratos y las etiquetas no validan esas fechas; no se han modificado sin fuente.
- [ ] Aplicar saneamiento equivalente a otros controles fuera de1940–1944 cuando se revisen; no afirmar corrección global de todos los conflictos.

## Encargo vigente · 0.12.0 · ampliación hasta1900

Ampliar mundialmente1900–1919 y conservar1920–actualidad. Comprobar localmente, subir y terminar sin esperar ni consultar Actions/Pages; el propietario notificará despliegue o errores.

- [x] Adquisición incremental aislada y fusión exclusiva de1900–1919, sin reintroducir afirmaciones rechazadas de años posteriores.
- [x] Autoridades, retratos y símbolos; separar imperios, repúblicas y sucesores sin estadísticas anacrónicas.
- [x] Dependencias, transiciones, Primera Guerra Mundial, revoluciones y contexto institucional con fechas/fuentes.
- [x] Auditoría nominal por décadas y conservación de los huecos reales; sincronizar Países y manifiestos.
- [x] Actualizar versión/documentación y todas las expectativas temporales afectadas, incluidas las pruebas antiguas.
- [x] Pruebas locales apropiadas y navegador; preparar la entrega autorizada a main, sin sondeos remotos.

Estado: rama codex/1900-history desde d7f683c. Adquisición y cinco curadores1900 integrados, más corrección adicional1939:302 claves/10.244 mandatos;5.262 medios(499SVG/4.763 fotografías),378 fotografías y21SVG netos adicionales. 76 ventanas de símbolos1900 y una adicional1939,41 agrupaciones/903 membresías,378 fases y97 registros/86 enlaces. Catálogo:2.792 carpetas. Se comprobó pureza/idempotencia de los cinco curadores y conservación de todas las afirmaciones1920+ previas, permitiendo añadir retratos acreditados. La referencia contemporánea sigue en22/10/2026.

Auditoría1900–1919:3.167 entidades/año y15 controles/año. Sin huecos de resolución de alguna autoridad o ausencia central documentada(Albania1917);66 personas/órganos sin imagen(63personas y3órganos),165 casos anuales sin símbolo después de corregir Corea1910. Listas nominales en REVIEW-1900-1919.json. No equivale a un censo completo de todos los cargos, regencias, gobernadores o frentes. Las correcciones de estatus no modifican history.topojson.

Comprobaciones:137 pruebas/31 archivos correctos, integridad de44 datos/11 franjas/5.262 medios y tipos correctos. La primera suite detectó claves monárquicas aplicadas a Serbia/Montenegro modernos y una expectativa de sucesores que no contemplaba el nuevo predecesor deChecoslovaquia; corregidos con aserciones positivas. Regresión adicional deCorea1910: mismo administrador al cambiar el régimen de dependencia mantiene su símbolo al cierre. Compilación final correcta en `.cache/build-012-final-map`; Windows bloqueó el vaciado de `dist/media`, por lo que el navegador usa exclusivamente la carpeta nueva y un preview propio en5174. No servir el `dist` incompleto sin regenerarlo. Cinco recorridos iniciales correctos(5,2min), cuatro tras la corrección central(3,9min) y repeticiones finales de1920–1949 y1939 correctas después deMoravia. La prueba nueva espera cámara quieta hasta30s en vez de los5s predeterminados, sin quitar renderizado, clic real ni control de errores. Revisadas capturas de móvil y1939;5.317 recursos preparados enGit íntegros. Entrega local lista para main; la confirmación del envío corresponde al resultado deGit y al mensaje final. No confundirla con despliegue. No hay investigadores ni adquisiciones de medios activos.

### Petición adicional · Alemania1939 y desmembración checoslovaca

- [x] Diagnosticar geometría fuente: componentes aislados e intrusiones vecinas, no sólo pintura/GPU.
- [x] Composición acotada1938–1939: país alemán único, vecinos protegidos, islas reales conservadas, Austria incorporada completa yBohemia/Moravia separadas del cliente eslovaco.
- [x] IdentidadSVK-1939, símbolo, autoridades/retrato, contexto, fuente/referencia y catálogo; sin estadísticas actuales.
- [x] Regresiones de puntos negativos/positivos, fases1938/1939, ocupación/incorporación, identificadores y fuentes inmutables.
- [x] Navegador y revisión visual de la compilación nueva; preparar su envío junto con1900 sin sondeos deActions/Pages.
- [ ] Investigación futura: frontera eslovaca1939 de fuente propia, detalles dePetržalka/Devín y franja oriental de marzo; extender la corrección a1940–1944 y distinguir la ocupación alemana desde1944. No presentar la referencia recortada como delimitación exacta.

### Pendientes documentales de1900–1919

- [ ] Contrastar los63 titulares sin fotografía y los165 casos anuales sin símbolo; conservar los3 órganos sin retrato individual inventado. Algunos vacíos son exclusiones históricas justificadas, otros faltas de investigación.
- [ ] Completar gabinetes secundarios, regencias y gobernadores locales; crisis de1907–1908 en Marruecos, mandatos y Gobiernos chinos meridionales, fragmentación albanesa, regencias etíopes y suplencias breves americanas.
- [ ] Incorporar geometría acreditada de frentes diarios/mensuales de la Primera Guerra Mundial y guerra civil rusa, concesiones, zonas coloniales y Estados efímeros omitidos; las fases contextuales no dibujan esos frentes.
- [ ] Reconstruir membresías históricas dePCA/ITU/UPU/OIT antes de ofrecer capas mundiales; sus fichas institucionales no son listas de miembros.
- [ ] Recuperar el CSV original aún ausente; mantener pendientes de entregas anteriores y revisar errores de metadatos de las fuentes tempranas sin fusionar identidades por un QID mal atribuido.
- [ ] Revisar la publicación sólo tras aviso del propietario; terminar el flujo operativo al confirmar el push.


## Registro · 0.11.1 · corrección de pruebas de publicación

El propietario comunica tres fallos de los 30 recorridos de Quality de0.11.0; los otros27 han pasado según el registro aportado. Corregir y subir sin esperar ni consultar Actions/Pages. No retirar datos históricos válidos para satisfacer expectativas antiguas.

- [x] Revisar las tres causas: organizaciones disponibles en1947, autoridad colectiva alemana en1946 y varios mandatos españoles en1939.
- [x] Actualizar las comprobaciones con condiciones positivas y negativas: ONU1947/OTAN aún inactiva, límite1919, órgano aliado sin bandera/retrato personal ficticios y Franco/Azaña con fecha del mandato.
- [x] Corregir la ayuda de cobertura de organizaciones a1920; versión0.11.1 y documentación.
- [x] Ejecutar las comprobaciones locales y los tres recorridos afectados; registrar resultados reales y preparar entrega a main.
- [ ] Revisar despliegue únicamente cuando el propietario confirme su terminación o aporte otro error.

Estado: corrección preparada desde 8990dcc en codex/fix-011-e2e para entrega a main. 129 pruebas unitarias/28 archivos, tipos y compilación correctos; los tres recorridos afectados pasan en 2,6 minutos. Confirmado que datos, catálogo Países y flujos de CI no cambian. Detalle en docs/DELIVERY-0.11.1.md. Tras confirmar el envío, el único siguiente paso operativo es el aviso del propietario sobre el despliegue; no afirmar que esté publicado por adelantado.

## Registro de la entrega · 0.11.0 · ampliación hasta1920

Petición24/10/2026: ampliar globalmente1920–1949 conservando1950–actualidad, la organización Países y la ficha fija. Mantener el flujo: comprobaciones locales y subida; NO esperar ni consultar el despliegue hasta aviso del propietario.

- [x] Adquisición incremental mundial y auditoría nominal por década1920/1930/1940.
- [x] Curaciones focales de autoridades, regímenes, símbolos, fuentes y retratos; conservar los vacíos reales. Cuatro preparadores de mandatos aplicados, 774 fotografías netas y 87 ventanas de símbolo contrastadas.
- [x] Revisar identidades predecesoras, dependencias y fronteras de la fuente; no inventar frentes diarios.
- [x] Organizaciones, instituciones, conflictos y contexto fechados; no retrotraer datos actuales ni membresías posteriores.
- [x] Sincronizar Países, documentación, manifiestos y versión; corregir fecha visible de Acerca de.
- [x] Pruebas locales apropiadas, compilación y navegador; entrega comprobada para subir y terminar sin espera de Actions/Pages.

Estado inicial: rama codex/1920-history desde45721b4, aplicación publicada0.10.0(fe3676c). Investigación acotada de autoridades y contexto en curso; root gestiona adquisición, medios, aplicación, validación y subida. No considerar esta ampliación terminada por reanudar sesión.

Punto de continuidad del 24/10: 290 claves, 9.485 mandatos; 4.863 medios. Auditoría de 5.294 entidades/año y 70 controles/año: cero huecos de resolución de alguna autoridad; quedan 122 personas/órganos sin retrato y 165 casos anuales sin símbolo, incluidos cuatro cierres alemanes de ocupación sin bandera nacional. No son series diarias completas. Tipos, 129 pruebas/28 archivos, integridad de 43 datos/11 franjas/4.863 medios y compilación correctos; bytes preparados en Git de 4.917 recursos comprobados. La primera suite detectó expectativas antiguas sobre símbolos/ocupación, un límite de tiempo del inventario y una afirmación genérica de Yan que reaparecía en 1950; corrección documentada y suite completa posterior correcta. Danzig1938 comprobado con punto real único, ficha visual y topología original intacta. La prueba de navegador reprodujo un atasco de resaltado Rusia1920→1921, corregido mediante estado de pintura; también se evita representar las tres zonas occidentales alemanas como administradas sólo por Estados Unidos. Los cuatro recorridos finales son correctos (3,3 minutos), incluida la regresión de1950 y la vista móvil. Entrega lista para main, sin sondeos remotos. Siguiente tras confirmar el envío: esperar el aviso del propietario para revisar la publicación.

### Pendientes documentales de esta ampliación

- [ ] Revisar las 118 personas sin fotografía; cuatro órganos colectivos no requieren retrato personal. Lista exacta en docs/REVIEW-1920-1949.json.
- [ ] Revisar los 165 casos anuales sin símbolo y variantes diarias de las banderas ya inventariadas, distinguiendo ausencias correctas de faltas documentales; no inventar una bandera alemana para la ocupación ni usar diseños posteriores.
- [ ] Completar suplencias y regencias diarias, autoridades coloniales locales y gobiernos breves, incluido Yemen1948 y Forster en Danzig1939.
- [ ] Contrastar frentes y fases territoriales omitidas por los inventarios, incluyendo la geometría propia de laRSI; una ficha de conflicto no proporciona un frente.
- [ ] Recuperar y conciliar el CSV original del propietario, aún ausente. Mantener los pendientes de entregas anteriores.
- [ ] Revisar la publicación de0.11.0 cuando el propietario avise de que el despliegue terminó; no consultar Actions/Pages entretanto.

## Registro de la entrega0.10.0

## Encargo vigente · 0.10.0 · ampliación a 1950

**Instrucción del propietario:** comprobar localmente y subir una entrega coherente; NO esperar ni consultar Actions/Pages después de subir. El propietario comprobará el despliegue y pedirá la revisión pública cuando corresponda. Una subida correcta no equivale a despliegue confirmado.

- [x] Adquisición incremental de autoridades de 1950–1959 sin perder curaciones ni fotografías posteriores.
- [x] Contrastes focales de sucesiones, dependencias, independencias, símbolos, fronteras de la fuente, organizaciones y conflictos; auditoría mundial de huecos.
- [x] Catálogo legible en Países: una carpeta por entidad, resumen y referencias a datos/medios; conservar licencias y evitar copias redundantes.
- [x] Entrada extensible para archivos propios de entidades (incluidos futuros himnos), con detección y procedencia explícita.
- [x] Cabecera, bandera y pestañas fijas; contenido interior desplazable sin barra visible; comparación dentro de Comparar y crédito de bandera sin el desplegable anterior.
- [x] Actualizar documentación, versión y comprobaciones locales para la entrega autorizada a main.
- [x] Confirmación del propietario y revisión pública de0.10.0:26 archivos idénticos, versión visible, retratos, cabecera fija y ficha persistente1952→1953.

Estado24/10/2026: rama main. Aplicación0.10.0 publicada en fe3676cb8f2dfa164466eae5f4050b2006b54492; cierre documental posterior separado. Adquisición y curación guardadas:285 claves/7.985 mandatos,4.062 medios(451 SVG/3.611 fotografías). Auditoría:1.753 territorio-años1950–1959, cero huecos de resolución de autoridad;69 personas/órganos sin retrato y23 territorio-años sin símbolo(AND/SMR y Túnez1956–1958). Fuentes y nombres en RESEARCH-1950 y REVIEW-1950. No equivale a series exhaustivas de todos los cargos ni frentes.

122 pruebas/26 archivos correctos, integridad de43 datos/11 franjas/4.062 medios y tipos correctos; compilación final correcta y5 recorridos de navegador correctos(2,5min), incluida vista móvil y ficha anclada. Revisión visual adicional en navegador integrado: Egipto1952 con retratos, cabecera y pestañas fijas. Catálogo:2.783 entidades de las fuentes,285 con inventario de autoridades; no todas tienen ficha completa. No hay himnos adquiridos. No hay agentes de investigación activos ni adquisiciones pendientes en segundo plano. La investigación interrumpida se ha retomado con contraste y scripts propios; no marcar vacíos bibliográficos como resueltos.

Cierre y evidencia en docs/DELIVERY-0.10.0.md y docs/reference/public-verification-0.10.0.json. El propietario confirmó la subida y se revisó después la web pública, sin esperar ni sondear Actions/Pages. HTML/JS/CSS, tres manifiestos, seis conjuntos y14 medios coinciden byte a byte:26 archivos. Versión0.10.0 visible, nueve referencias de retrato cargadas en Egipto1952, cabecera fija, entidad EGY retenida al pasar a1953 y comparación dentro de su pestaña. No se observaron errores de consola. No se repitió toda la suite de navegador ni se certifican por ello todos los datos históricos.

- [ ] Detalle menor detectado en la revisión: la etiqueta Actualización de Acerca de aún muestra23/10 y el historial de0.10.0 muestra24/10; ajustar junto con la siguiente entrega de código. No requiere repetir el despliegue para validar esta versión.

No quedan operaciones de publicación pendientes. Continuar por los huecos de investigación o siguiente encargo. La pestaña de entrega utiliza la URL pública; el preview local ya no es necesario.

Idea futura: separar progresivamente módulos y carga de catálogos para reducir el paquete principal, cuya compilación advierte de tamaño; no reducir el detalle geográfico.

Idea futura: incorporar himnos y otros documentos por entidad y periodo; no descargar grabaciones sin revisar derechos. Mantener esta idea y la cobertura pendiente al retomar.

## Registro de la entrega anterior0.9.1

Actualizado: 23/10/2026, 21:48 Madrid. Rama: main. Aplicación 0.9.1 subida en f67f8aecf9acc19e51e7f49648ea81e12008b34d.

Leer también [agentes.md](agentes.md). Esta pizarra distingue implementación, investigación, validación y publicación. Una sesión recuperada no convierte los pendientes en terminados.

## Funcionalidad solicitada

- [x] Paleta editorial de 33 familias, regímenes focales y matices de dependencia, con contraste entre las familias británica y soviética. Exportación propia en docs/POLITICAL-PALETTE.csv; el CSV del propietario sigue pendiente.
- [x] El control territorial modifica el inventario del mapa y se selecciona como controlador, con las franjas encendidas o apagadas.
- [x] Franjas opcionales, desactivadas inicialmente: tres cuartos del controlador y un cuarto del territorio ocupado. La incorporación documentada se distingue de ocupación; Viena y Oslo tienen regresiones específicas.
- [x] Tierra de referencia bajo los huecos del inventario político, incluida África 1889 y Arabia 1918. Separa tierra y mar; no atribuye ausencia de población ni reconstruye costas históricas.
- [x] Conservar actualizaciones incrementales al recibir geometrías clonadas, sin reprocesar las costas idénticas.

## Ampliación a 1960

- [x] Auditoría de 1.693 país-años de 1960–1969, con suplementos y sin huecos de resolución de autoridad. No certifica todos los cargos, suplencias o días de mandato.
- [x] Revisión focal de UAR, Yemen, Tanganyika/Zanzíbar, UNTEA, protectorados, Namibia, descolonización y estados omitidos. No equivale a reconstruir todos los frentes del mundo.
- [x] Ampliar autoridades, banderas, retratos y contexto: 283 claves, 7.480 mandatos, 3.793 medios; 31 organizaciones/549 intervalos, 258 fases y 59 relaciones/53 registros históricos e institucionales.
- [x] Conservar los medios antes de regenerar mandatos curados. Recuperados 26 retratos acreditados; repetir la curación conserva exactamente los bytes del catálogo.
- [x] Separar la presidencia parlamentaria de Azikiwe del Gobierno de Balewa y evitar que la consolidación recupere cargos descartados por una corrección revisada.
- [x] Registrar nombres, años y pistas de los vacíos en docs/REVIEW-1960.json y docs/reference/portrait-1960-pending-research.json.

## Cierre de la entrega

- [x] Publicación 0.9.0: Quality 40005916966, 114 unitarias y 28 recorridos correctos; Pages 40008258279 correcto. Bytes públicos cotejados, con evidencia en docs/reference/public-verification-0.9.0.json.
- [x] Corrección 0.9.1: 115 unitarias/23 archivos, tipos y build locales correctos. Integridad de 43 recursos, 11 franjas tipográficas y 3.793 medios, incluidos los bytes registrados en Git.
- [x] Comprobación manual del navegador integrado: Nigeria con retratos y cargos separados; TAN→TZA conserva la ficha; reproducción y franjas. Fallos y límites de las primeras pasadas locales registrados en DELIVERY-0.9.0.
- [x] Quality definitivo 40011433956 para f67f8ae: integridad, 115 unitarias/23 archivos, tipos, build y 28 recorridos de navegador correctos.
- [x] Pages 40013402559: build y deploy correctos, checkout f67f8ae confirmado. Cotejo público de cuatro archivos de aplicación, tres manifiestos, siete conjuntos de datos y 16 medios; evidencia en docs/reference/public-verification-0.9.1.json.
- [x] Registrar cierre, SHA y pendientes; commit posterior de documentación y aserciones focales con [skip ci]. El SHA de aplicación publicado es f67f8ae, separado de ese cierre.

## Pendientes reales de investigación y siguientes etapas

- [ ] Recuperar y cotejar el CSV original. La ruta C:/Users/darim/Downloads/lista_imperios_completa_v3.csv no existe en las comprobaciones realizadas; no se ha importado ni reconstruido como si se hubiese leído.
- [ ] 91 personas u órganos sin retrato: 76 sin P18 en la fuente consultada, 12 candidatos pendientes de identificación/licencia/adquisición y tres órganos o identificadores documentales. No son 96 países ni imágenes aprobadas. Conservar las exclusiones de retratos incorrectos.
- [ ] Variantes históricas de Andorra y San Marino: 20 país-años de 1960–1969 sin bandera. No rellenar con diseños modernos sin cotejo de la variante.
- [ ] Relevos diarios, suplencias, gobernadores generales y cargos secundarios identificados en las investigaciones, incluido enero de 1966 en Nigeria. Una ventana documental no es un nombramiento o una dimisión.
- [ ] Frentes mensuales y control detallado de Congo, Biafra, Vietnam y Levante; sectores aliados de Alemania y control reciente completo. Mantener los límites de resolución de cada fuente.
- [ ] Fichas tempranas que aún no se abren y ampliación de familias/regímenes fuera de los casos revisados. Revisar por etapas; no declararlo resuelto por ampliar una década.

## Cómo retomar

La entrega 0.9.1 está publicada y comprobada. Aplicación: f67f8aecf9acc19e51e7f49648ea81e12008b34d. Evidencia de Quality, Pages, bytes y vista pública en docs/DELIVERY-0.9.1.md. El candidato c42531d también pasó 115 unitarias y 28 recorridos, pero Pages 40011732004 se omitió por estar superado: no se publicó como entrega final.

Continuar por los pendientes de investigación anteriores o por el siguiente encargo del propietario. No repetir adquisiciones ni curaciones a ciegas. La última repetición del preparador conservó los bytes y retratos. No hay adquisición activa de medios. El servidor de preview de esta entrega se cierra al terminar; la pestaña de salida usa la web pública (browser 2/tab 2). La referencia contemporánea sigue siendo 22/10/2026.

El cierre añade comprobaciones locales de París, Viena, Innsbruck, Salzburgo, Graz y Linz a la regresión de control de 1942; cuatro pruebas focales correctas, sin modificar el código de aplicación ni sus datos publicados. El cierre con [skip ci] no sustituye Quality cuando cambien código, datos o publicación.

Si se interrumpe la sesión, registrar el último paso terminado, procesos activos, fallos concretos y siguiente acción antes de cerrar. No confundir el SHA de aplicación publicado con un commit posterior sólo documental.


Cierre local0.12.1:147 pruebas/33 archivos, siete recorridos de navegador distintos correctos, tipos/compilación e integridad de45 datos/11 franjas/5.297 medios. La segunda pasada detectó una expectativa nueva de buscarEslovaquia como territorio activo1944; se comprueba correctamente persistencia desde1943 y autoridades1944, sin volver a introducir una geometría independiente ficticia. La ruta final pasa con clics neutrales, franjas y una sola descarga compartida. El siguiente paso operativo es confirmar el envío, no esperar un despliegue.


Corrección de publicación25/10/2026: Quality40208104708 pasó para33637c5; Publish40209978935 se omitió porque el cierre documental3f2c2f5 adelantómain y la condición comparaba ambosSHA. Se elimina esa igualdad y se conserva checkout delSHA validado, con éxito/push/main/mismo repositorio. Reejecutar un workflow_run conserva su evento antiguo; usar una ejecución manual nueva. No se cambian datos ni aplicación. No esperar despliegue.

Cotejo final del índice Git: 1.067 archivos nuevos/modificados coinciden con sus bytes locales; 9.259 recursos de manifiestos verificados por SHA-256 y blob Git (9.198 blobs previos intactos); 1.292 originales canónicos propios comprobados directamente en el índice. Se retira una vista automática duplicada de Urartu; las fuentes originales se conservan. Dos pruebas finales del catálogo correctas después de la regeneración. Los cuatro documentos de cierre se cotejan otra vez tras incorporar estas cifras. No se espera ni se sondea Actions/Pages.
