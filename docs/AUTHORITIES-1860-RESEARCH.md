# Autoridades 1860–1879: suplemento documental

Preparación de investigación para la ampliación 0.14. El archivo `scripts/curate-1860-authorities.py` es una transformación pura e idempotente; no descarga imágenes, no cambia banderas, no escribe durante su importación y exige una salida distinta en su uso por consola. La integración del catálogo y de la cartografía corresponde al proceso principal.

## Alcance y precisión

Este suplemento corrige instituciones y documenta sucesiones seleccionadas. **No acredita una revisión mundial completa de todos los gabinetes, regencias, gobiernos rivales o administraciones coloniales.** La presencia de un soberano tampoco certifica el control de cada territorio representado.

Los registros nuevos están acotados a 1860-01-01–1879-12-31. Todo registro original que alcance 1880 o una fecha posterior se conserva exactamente, aun si cruza esta ventana. Los retratos existentes se reutilizan por identificador humano; las banderas, otros medios y metadatos del catálogo no se modifican. Las partes de registros anteriores que queden fuera de una observación curada se conservan, salvo la atribución incorrecta de la presidencia de la República a Trochu.

`precision=9` indica información anual y `precision=10` información mensual. Los límites marcados `startIsCoverageBoundary` o `endIsCoverageBoundary` son observaciones documentales interiores: por ejemplo, 31 de diciembre de un año conocido de acceso **no afirma que la persona fuera nombrada ese día**. No se deben presentar como un relevo diario certificado. Las fuentes orientales que usan años de era o calendario lunar requieren conversión contrastada, no sustitución mecánica de año lunar por gregoriano.

Todos los identificadores personales del núcleo inicial se contrastaron con la instancia humana y su etiqueta en Wikidata. Ejemplos que evitan errores por homónimos: Juárez es Q182276 (Q80047 corresponde a Brighton, Alabama); Serrano es Q515741; Salmerón Q742660; Francisco José Q51056; Alejandro II Q83171; Umberto I Q153688. La comprobación material queda en `.cache/1860-authority-entity-checks.json`; el caché no constituye fuente de fechas de mandato.

## Entidades separadas que necesita la integración

| Clave | QID | Uso |
| --- | --- | --- |
| SAR | Q165154 | Reino de Cerdeña antes de Italia; Víctor Manuel II no es rey de Italia en 1860. |
| PRUSSIA | Q27306 | Prusia; subsiste como reino integrante del Imperio alemán después de 1871. |
| NGC | Q150981 | Confederación Alemana del Norte, distinta del Imperio alemán. |
| AUSTRIAN-EMPIRE | Q131964 | Imperio austríaco anterior a la transformación dual de 1867. |
| AUT-HUN | Q28513 | Monarquía dual, con gobiernos austríaco y húngaro separados. |
| MEX-EMPIRE | Q371334 | Segundo Imperio mexicano; no sustituye documentalmente la continuidad republicana de Juárez. |
| BRA-EMPIRE | Q217230 | Brasil imperial; soberano y presidente del Consejo son cargos diferentes. |
| RUE / OTT / QING | Q34266 / Q12560 / Q8733 | Imperios ruso, otomano y Qing, sin proyectar instituciones contemporáneas. |

Semillas adicionales comprobadas para investigar: Estados Confederados Q81931; Dos Sicilias Q180393; Estados Pontificios Q170174. Son claves propuestas, no fronteras o gobiernos ya integrados. No debe equipararse Toscana de 1860 a una continuidad efectiva del gran duque depuesto en 1859.

## Fuentes y decisiones

### Francia

El [Elíseo, Thiers](https://www.elysee.fr/adolphe-thiers) distingue jefe del Poder Ejecutivo desde 17-02-1871 y presidente de la República desde 31-08-1871. La primera observación termina el 30 de agosto para evitar duplicar cargos el mismo día. La [cronología del Ministerio del Interior](https://www.interieur.gouv.fr/archive/annexe-n-13-les-presidents-de-la-iieme-a-la-veme-republique) sitúa la sucesión de Mac Mahon el 24-05-1873 y la de Grévy el 30-01-1879; la [ficha de Grévy del Elíseo](https://www.elysee.fr/jules-grevy) confirma la segunda transición.

La [autoridad institucional de la BnF sobre el Gobierno de Defensa Nacional](https://catalogue.bnf.fr/ark:/12148/cb15503306b) fecha su formación el 04-09-1870 y distingue un gobierno colectivo presidido por Trochu. **Trochu no fue presidente de la República.** Se documenta su presidencia gubernamental en 1870; queda pendiente resolver con actas el reparto de funciones de Trochu, Favre y las delegaciones en enero-febrero de 1871. La cesión del mando militar de París no equivale automáticamente a la dimisión de toda función gubernamental. No se inventa un presidente individual para rellenar ese hueco.

### España

El [Congreso, Sexenio Revolucionario](https://www.congreso.es/es/web/guest/cem/sexrevol) documenta el exilio de Isabel II el 30-09-1868, la regencia de Serrano desde el 18-06-1869, la elección de Amadeo el 16-11-1870 y su juramento el 02-01-1871. El [Banco de España](https://coleccion.bde.es/wca/es/secciones/coleccion/obras/isabel-ii-p_140.html) separa el exilio de la abdicación dinástica de 1870. No se prolonga el ejercicio de Isabel II hasta su abdicación formal.

La [serie de presidentes de la Moncloa](https://www.lamoncloa.gob.es/presidente/presidentes-desde-1823/Paginas/index.aspx) proporciona los relevos de Prim, Pi y Margall, Salmerón y Castelar. Se conservan las interrupciones de Prim: no se absorben interinidades en un mandato continuo. La elección de Figueras el 11 de febrero de 1873 difiere del comienzo ministerial fechado el 12 en esa tabla; se usa el 11 para la presidencia del Ejecutivo. [PARES](https://pares.cultura.gob.es/ParesBusquedas20/catalogo/autoridad/101210) delimita la Primera República y la fase posterior a los cuatro presidentes de 1873. La fase de Serrano de 1874 no es su breve presidencia del Consejo de enero-febrero. La [ficha parlamentaria de Alfonso XII](https://www.congreso.es/en/cem/alfonsoxii) permite distinguir restauración y llegada posterior del rey.

Pendientes: los gabinetes completos anteriores a 1868, Topete y todos los relevos de 1871–1879, carlismo y cantonalismo como autoridades rivales con ámbito territorial propio. No se infieren de la jefatura de Estado.

### Italia, Alemania y Austria

El [Archivio di Stato di Torino](https://archiviodistatotorino.cultura.gov.it/iorestoacasa-nascita-regno-italia/) reproduce la ley 4671 del 17-03-1861: Víctor Manuel II pasa de rey de Cerdeña a rey de Italia conservando el ordinal. El [Quirinal](https://palazzo.quirinale.it/luoghi/pdf/it/sala-regno-italia.pdf) documenta Umberto I desde 1878; el curador utiliza observaciones anuales mientras se contrasta el día exacto. Los gabinetes italianos y los Estados anteriores a la unificación necesitan registros propios.

El [DHM, Guillermo I](https://www.dhm.de/lemo/biografie/wilhelm-i) separa regencia, acceso al trono prusiano el 02-01-1861, coronación posterior y proclamación imperial el 18-01-1871. La Confederación de 1867 no se convierte retroactivamente en Alemania imperial. El [DHM, Bismarck](https://www.dhm.de/lemo/biografie/otto-bismarck) permite una observación anual de la cancillería imperial; su cargo prusiano es distinto y falta completar su calendario.

[Habsburger.net, coronación húngara](https://www.habsburger.net/de/kapitel/franz-josephs-kroenung-zum-koenig-von-ungarn) sitúa la transformación dual en 1867 y la coronación en Hungría el 8 de junio. Esta ceremonia no se usa como supuesto día único de creación legal de la monarquía dual. Se mantienen observaciones anuales conservadoras y gobiernos separados pendientes de completar.

Para Estados italianos faltantes: el [Archivo de Estado de Florencia](https://sias-archivi.cultura.gov.it/cgi-bin/pagina.pl?Chiave=112&RicProgetto=as-firenze&TipoPag=contesto) distingue plebiscito toscano 11–12 de marzo de 1860, promulgación el 15 y acto de anexión el 22. El [boletín oficial de Toscana](https://www.giustizia.it/resources/cms/documents/Bollettino_Toscana_18602.pdf) conserva decretos firmados por Bettino Ricasoli como presidente del Consejo en marzo; es una fuente para la autoridad efectiva, frente a un supuesto reinado efectivo de Leopoldo II en 1860. Ricasoli es Q519900, identificado también por el [catálogo de la Universidad de Trieste](https://www.biblio.units.it/SebinaOpac/agent/TSA00335934). Francisco II de las Dos Sicilias es Q206223, humano; falta cerrar su calendario efectivo y el gobierno en el exilio con fuente primaria. [Vaticano, Pío IX](https://www.vatican.va/content/pius-ix/en.html) fecha el pontificado hasta 1878; [Estado Vaticano](https://www.vaticanstate.va/en/component/content/article/7-february-blessed-pius-ix.html?Itemid=216&catid=51) distingue la toma de Roma el 20-09-1870: el pontificado posterior no acredita la continuación del Estado territorial.

### Rusia, Reino Unido y monarquías europeas

La [Casa Imperial rusa](https://imperialhouse.ru/rus/imperialhouse/succession/monarh/aleksandr-ii-nikolaevich-osvoboditel-1855-1881.html) delimita el reinado de Alejandro II entre 1855 y 1881. Aquí sólo se registra la ventana interior, evitando trasladar días julianos como gregorianos. El [Parlamento británico](https://api.parliament.uk/regnal-years/reigns/6) documenta a Victoria; no se equipara soberana, primer ministro y autoridades coloniales.

Fuentes institucionales de las observaciones de soberanos: [Casa Real neerlandesa, Guillermo III](https://www.koninklijkhuis.nl/onderwerpen/koninklijk-huis/geschiedenis/koningen-en-koninginnen/koning-willem-3-1849-1890), [Casa Real belga](https://www.monarchie.be/en/royal-family/history), [Casa Real danesa](https://www.kongehuset.dk/monarkiet-i-danmark/kongerakken), [Museo Histórico sueco](https://historiska.se/en/list-of-swedish-monarchs/) y [Parques de Sintra](https://www.parquesdesintra.pt/media/upzl30vk/colecoesemfoco_pnsintra_ebook_2_lq.pdf). Las uniones personales neerlandesa-luxemburguesa y sueca-noruega no son anexiones. No se ha certificado la sucesión diaria completa en estas observaciones anuales.

### Imperio otomano, Qing y Japón

La [Türk Tarih Kurumu](https://ttk.gov.tr/osmanli-padisahlari/) documenta los cuatro sultanes que intervienen en esta ventana: Abdülmecid, Abdülaziz, Murad V y Abdülhamid II. En 1876 se conservan los tres sucesivos sultanes, sin confundir deposición y fallecimiento.

El [Museo del Palacio, Tongzhi](https://www.dpm.org.cn/court/lineage/226248.html) distingue acceso de 1861 y era iniciada en 1862. Su fecha lunar de muerte pertenece al año Tongzhi 13, que cruza 1875 gregoriano: no se afirma una muerte en diciembre de 1874 por la etiqueta resumida de la era. La [ficha de Guangxu](https://www.dpm.org.cn/court/lineage/226254.html) permite la observación de 1875–1879 y documenta la regencia de Ci’an y Cixi. Faltan registros individuales contrastados para ambas regentes, el Consejo de ocho regentes de 1861 y su relevo; no se reduce esa estructura a un primer ministro actual.

La [Biblioteca Nacional de Japón](https://www.ndl.go.jp/en/jikihitsu/part1/s1_3/) fecha el shogunato de Yoshinobu en 1866–1867, sin fingir conversión diaria; su [ficha de Sanjō Sanetomi](https://www.ndl.go.jp/portrait/e/datas/97/?lang=en) documenta el Daijō-daijin desde 1871. El primer ministro moderno aparece en 1885. Se preserva la adquisición existente de Kōmei y Meiji: la [Casa Imperial japonesa](https://www.kunaicho.go.jp/e-about/genealogy/pdf/keizu-e.pdf) usa cronología de era/calendario japonés y no basta por sí sola para recalcular días gregorianos.

### Estados Unidos, México y Brasil

Los [National Archives](https://www.archives.gov/research/census/presidents) confirman las sucesiones de Lincoln, Johnson, Grant y Hayes; se mantiene la diferencia entre elecciones y comienzo del mandato. La Confederación requiere una entidad separada: la [Cámara de Representantes](https://history.house.gov/People/Listing/D/DAVIS%2C-Jefferson-%28D000113%29/) distingue inauguración provisional de Jefferson Davis el 18-02-1861, constitucional de 1862 y captura en mayo de 1865. Captura no se convierte automáticamente en fecha legal de terminación de todas sus funciones. Davis Q162269 no es el general unionista Jefferson C. Davis Q2525166.

El [INEHRM sobre Juárez](https://www.constitucion1917.gob.mx/es/inehrm/juarez) documenta continuidad republicana e itinerancia durante la intervención francesa. La [SEP](https://nuevaescuelamexicana.sep.gob.mx/contenido/coleccion/18741/) sitúa la muerte de Juárez el 18-07-1872 y la sucesión de Lerdo. El [Ministerio de Cultura mexicano](https://www.gob.mx/cultura/prensa/reflexionaran-en-torno-al-segundo-imperio-a-160-anos-de-la-llegada-de-maximiliano-de-habsburgo-a-mexico?idiom=es-MX) distingue aceptación de Maximiliano en Miramar el 10-04-1864 y llegada a Veracruz el 28 de mayo; [Defensa](https://www.gob.mx/defensa/documentos/19-de-junio-de-1867-fusilamiento-de-maximiliano-de-habsburgo-y-los-generales-miramon-y-mejia) documenta la ejecución el 19-06-1867.

Pendiente mexicano: el gobierno rival de Iglesias, la interinidad de Méndez y las fases de Díaz de 1876–1877. La [Library of Congress](https://www.loc.gov/exhibits/mexican-revolution-and-the-united-states/porfiriato-sp.html) resume su ascenso con una fecha que difiere de la SEP y omite interinidades. El curador sólo incorpora una observación estable desde el cierre de 1877, sin elegir arbitrariamente entre fechas de noviembre de 1876. Semillas personales verificadas para continuar: Iglesias Q1196814, Méndez Q519806 y Díaz Q150688.

La [Biblioteca Nacional del Brasil](https://bndigital.bn.gov.br/dossies/periodicos-literatura/personagens-periodicos-literatura/dom-pedro-ii/) distingue mayoría anticipada y coronación de Pedro II. El [Caderno MAPA n.º 2, tabla de la página 77 digital](https://mapa.an.gov.br/images/publicacoes/CadernoMAPA2/files/assets/basic-html/page-77.html) documenta las presidencias del Consejo junto a los ministros de Justicia. **No se convierten titulares o interinos de Justicia en presidentes del Consejo.** Se incorporan Paranhos (desde 07-03-1871), Caxias (25-06-1875) y Sinimbu (05-01-1878). La [ficha del Archivo Nacional sobre Paranhos](https://mapa.an.gov.br/index.php/ultimas-noticias/645-jose-maria-da-silva-paranhos-visconde-do-rio-branco) confirma su presidencia y diferencia al padre del hijo diplomático homónimo.

Pendientes brasileños: tabla completa de gabinetes anteriores a 1871 y regencias por viajes. Parte del portal MAPA respondió con bloqueo de acceso institucional; no se eludió. La tabla digital accesible distingue su numeración impresa de la digital. Es necesario leer ambas columnas antes de ampliar, especialmente el relevo de marzo de 1861 que aparece con variantes de día en repertorios.

## Trabajo que sigue abierto

1. Integrar estas semillas con resolución territorial fechada; no usar fronteras actuales como sustituto de Cerdeña, Prusia, los gobiernos mexicanos rivales o Estados italianos.
2. Completar autoridades soberanas y gobiernos de Asia, África, América Latina, Oceanía y territorios dependientes. El núcleo presente no acredita cobertura de esos países por ausencia de filas.
3. Contrastar los días pendientes y completar regentes, gabinetes cortos, autoridades rivales y autoridades externas/locales de colonias.
4. Resolver medios con licencia y retratos contemporáneos de la época a través del proceso de adquisición; este curador sólo reutiliza los ya disponibles.
5. Auditar las banderas por régimen y fecha en un paso separado. Una bandera existente posterior no se retrocede por comodidad.
6. Validar en la aplicación los cambios de entidad, los relevos dentro del año y la continuidad de la ficha abierta. Un recuento positivo de líderes no prueba que el país seleccionado sea el correcto.
