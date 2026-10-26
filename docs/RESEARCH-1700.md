# Ampliación1700–1799 y separación de filtros ·0.19.0

La navegación anual alcanza1700. Esta entrega incorpora registros documentales y una auditoría nominal; **no declara completas las fronteras, autoridades o banderas de todos los Estados del sigloXVIII**. El inventario de polígonos tampoco equivale a un censo de Estados soberanos.

## Cartografía e identidades

`early-modern-1700.geojson` contiene853 intervalos componentes de1700–1788 de la misma revisión fijada de[Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria),CCBY4.0. Los índices de origen y las matrices de coordenadas se conservan. Desde1789 se sigue leyendo el archivo anterior. No se han modificado las geometrías ya publicadas ni se han superpuesto contornos modernos para simular fronteras antiguas.

`historical-1700-entities.json` contiene58 reglas de resolución fechadas: zarato/Imperio ruso, Inglaterra/Gran Bretaña y agregados coloniales, electorados y ducados germanos, monarquía de Habsburgo, fases persas, Joseon, Qing y las etapas de Siam, entre otras. Se corrigen identificadores inicialmente candidatos: AfsháridasQ388739, ZandQ97629053, ThonburiQ1115291 y ducado deSaboyaQ426025. La existencia de una regla no aporta un polígono ausente en la fuente.

**Estados germanos:** la fuente agrupa numerosos territorios dentro del Sacro Imperio. Se añaden16 referencias fechadas de sedes soberanas —entre ellas Kassel, Darmstadt, Detmold, Weimar, Hannover y Wolfenbüttel— que sólo aparecen cuando existe el agregado y no hay un polígono propio. Son seleccionables desde Capitales/ciudades y desde Buscar, abren la ficha del Estado y conservan identidad al cambiar año. No atribuyen el contorno imperial a un landgrave ni inventan fronteras individuales. La referencia explica expresamente esta limitación enTerritorio. Se revisaron también mapas fijados de1700,1715 y1783 deA.Ourednik; no se adoptó un contorno de una fecha como si acreditase todas las fechas del siglo.

## Autoridades

La adquisición aislada evita reescribir hechos anteriores. El registro congelado`historical-offices-019-research.json` incluye242 intervalos revisados y sus candidatos;`indian-siam-offices-019-research.json` conserva33 más. Se distinguen emperador, soberano hereditario, elector, landgrave, duque, margrave, conde, príncipe, estatúder, shogun, shah, vakil, chhatrapati y peshwa. Los títulos no se sustituyen por presidencias modernas.

La revisión incluye Francia, España, Gran Bretaña, Portugal, Polonia-Lituania, Habsburgo, Estados germanos, Qing, Japón, Joseon, fases persas, emperadores mogoles, autoridades marathas y Siam. RajaramIIdeSatara no se confunde con el Rajaram deKolhapur del sigloXIX. El peshwa y el chhatrapati son cargos distintos; la titularidad nominal no demuestra control de todas las regiones. Las regencias y minorías se señalan, aunque su inventario continúa incompleto.

Las variantes de calendario rusas de la nueva adquisición se consolidan en observaciones anuales, conservando las declaraciones originales en el registro de investigación. No se presentan días de estilo antiguo como fechas gregorianas verificadas. Las fechas británicas anteriores a1752 de esta revisión mantienen también precisión anual cuando no se ha cotejado la conversión. Los límites de observación no son accesos o ceses.

El catálogo pasa a629 claves y13.881 registros de mandatos en todas las épocas; no equivale a629 fichas completas. Los retratos se amplían con autor, licencia y archivo local. Se excluye como retrato identificativo el fragmento atribuido aSunjo sin rostro reconocible, documentado en el[catálogo del Museo Nacional del Palacio deCorea](https://www.gogung.go.kr/ebook/access/ecatalogt.jsp?Dir=45&callmode=admin&catimage=&eclang=ko&start=64&um=s). Se conserva la procedencia del archivo y el nombre del soberano; no se reconstruye su cara.

## Símbolos

39 ventanas revisadas y6.540 medios acreditados totales,236 más que0.18. Cada ventana distingue bandera, pabellón, estandarte, armas dinásticas, mon o sello. El encabezado muestra el tipo; Contexto conserva la explicación. Archivos originales, autor y licencia individual permanecen disponibles.

- Rusia: tricolor mercante desde1705 y durante el Imperio, disponible también en1800. No es la bandera imperial negra/amarilla/blanca posterior. La[Biblioteca Presidencial](https://www.prlib.ru/news/1163137) conserva el decreto y los antecedentes.
- Japón1700–1853: mon de losTokugawa, identificado como emblema dinástico. Se rechaza para1700 el supuesto pabellón shogunal cuya propia descripción lo sitúa a finales de1860. El[catálogo delMuseo Edo-Tokyo](https://www.edo-tokyo-museum.or.jp/assets/img/2021/07/oedo_list_E.pdf) documenta las hojas de malva en objetos del periodo.
- Qing1700–1861: reproducción representativa de la Bandera Amarilla, **enseña institucional de las Ocho Banderas**, no bandera nacional uniforme. La variante nacional de dragón de finales delXIX no se retrotrae.
- Joseon: sellos reales1653–1776 y1776–1876, reproducidos desde documentos identificados en las fichas deCommons. No se convierten en banderas nacionales ni se adelanta elTaegeukgi.
- Persia1800: pabellón diplomático atribuido aFathAlí, con ventana interior y explicación; no un supuesto diseño único de todos los ejércitos. Marco histórico en[EncyclopaediaIranica](https://www.iranicaonline.org/articles/flags-i/).
- Siam: pabellón marítimo rojo anterior a los diseños nacionales posteriores. Marathas: enseña azafrán de cola de golondrina con ventana interior desde1710, sin inventar una adopción exacta. La[monografía dePhilipMacDougall](https://www.cambridge.org/core/books/abs/naval-resistance-to-britains-growing-power-in-india-16601800/introduction/8AF86A549E63B833D45579154D4CB2F3) describe el uso naval y su datación incierta.
- Baviera, Sajonia, Hannover, Wurtemberg y Prusia reciben enseñas fechadas; Hesse yMecklemburgo usan armas con tipo explícito. La variante deBrandeburgo anterior a1701 mantiene gorro electoral.

`review-019-symbols.json` conserva aceptados y nueve candidatos pendientes/rechazados. Un nombre de archivo o un resultado de búsqueda no prueba su uso histórico. Quedan pendientes los símbolos safávidas, afsháridas y zand que todavía no tienen un diseño cotejado, variantes de kanatos y numerosas entidades africanas. No se ha adoptado el diseño mogol marcado como ficticio ni se ha proyectado automáticamente una ilustración de1840 al año1700.

## Filtros y contexto

Embudo a la izquierda deCapas. Filtros reúne forma política/régimen, color del mapa y organizaciones; Capas conserva territorios, relieve, lugares y ocupaciones/conflictos. Los dos paneles son independientes y compactos. El selector de formas sólo contiene categorías con entidades documentadas; si el filtro activo queda vacío al viajar, permanece aplicado con aviso y acciónQuitar filtro. No se añade una opción de cero resultados. Escape devuelve el foco al embudo y conserva la ficha.

Se añaden29 registros institucionales,32 referencias urbanas y15 fases documentales, con seis puntos **regionales** de conflictos. Los puntos no son frentes ni áreas ocupadas. La evaluaciónV-Dem/OWID conserva su inicio1789; no se inventan puntuaciones para1700. Las organizaciones mantienen sus propias fechas, sin extrapolación al nuevo siglo.

## Auditoría y continuidad

[REVIEW-1700-1799.json](REVIEW-1700-1799.json) recorre la ruta real de resolución de los100 años.12.659 entidades/año,8.747 casos anuales sin autoridad documentada,9.945 sin símbolo y81 personas/órganos sin retrato dentro de las autoridades disponibles. Las sedes germanas adicionales se cuentan aparte. En1700, de107 componentes hay36 con autoridad y23 con símbolo; en1750, de132 hay37 y26; en1799, de124 hay38 y27. La ausencia de documentación no significa ausencia de gobierno, símbolos o población.

Pendiente: ampliar el inventario mundial y gobiernos regionales, completar regencias, contraste intranual/calendarios, fuentes cartográficas para Estados germanos individuales, símbolos todavía no acreditados, frentes históricos y variantes de retrato por época. No convertir estas tareas en terminadas al reanudar sesión.

## Preparación y comprobación

Orden: prepare-1700-geometry → enrich-1700-authorities (aislado) → acquire-1700-offices/review-019-rulers (candidatos) → prepare-1700-authorities → prepare-019-core → prepare-1700-entities → prepare-019-indian-siam → adquisición de retratos → prepare-019-symbols → review-019-media → prepare-1700-support → register-review-019 → prepare-country-catalog. Un solo escritor de identidades/medios a la vez. Los registros congelados permiten conservar los contrastes; la investigación se renueva explícitamente. La compilación no consulta proveedores históricos.

Las comprobaciones de conservación comparan todos los mandatos y símbolos anteriores, permitiendo añadir retratos; seis archivos geográficos anteriores mantienen exactamente sus bytes. La revisión visual detectó el fragmento no identificable deSunjo y se retiró de la ficha con fuente explícita. Resultados de cierre en`tareas.md`. Subir tras comprobaciones locales y terminar al confirmar el envío; el propietario compruebaActions/Pages.

Validación local final:182 pruebas en43 archivos, tipos y compilación correctos. Cuatro recorridos de navegador correctos en3,8min, más repetición focal final de45,7s tras la revisión documental de imágenes. Integridad de63 datos,11 franjas tipográficas y6.540 medios porSHA-256. No se ha ejecutado otra vez toda la batería de navegador ni se ha comprobado el despliegue público.
