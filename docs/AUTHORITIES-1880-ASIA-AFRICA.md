# Autoridades, identidades y dependencias de Asia, África y Oceanía · 1880–1899

Estado de investigación: 25 de octubre de 2026. Integración prevista: 0.13. Documento de evidencia y límites; no certifica exactitud universal de las geometrías ni cobertura exhaustiva de todas las instituciones locales.

## Contrato de integración

`scripts/curate-1880-asia-africa.py` ofrece `curate(data)` puro e idempotente. No hace peticiones, descarga imágenes, escribe el catálogo público ni modifica manifiestos. La CLI exige `--output` explícito. Recoge los retratos existentes por identificador de persona antes de regenerar sus propios registros. Aporta 50 mandatos/observaciones de 21 identidades, todos dentro de 1880–1899. Conserva los mandatos que alcanzan 1900 o años posteriores y las banderas existentes.

Las fechas limitadas por la investigación llevan `startIsCoverageBoundary` o `endIsCoverageBoundary`. La precisión 9 significa anual, 10 mensual y 11 diaria. Un extremo normalizado a 1 de enero o 31 de diciembre **no es una fecha de nombramiento o fallecimiento**. Las notas identifican explícitamente estas observaciones. No se debe presentar precisión diaria derivada artificialmente de estas fechas.

Claves acordadas: JOS hasta 11/10/1897; KEM desde 12/10/1897; ZAN para el sultanato; ETH para el imperio etíope; ZUL para la región zulú fragmentada; HIST-Q1071439 para la monarquía merina. Hawái se divide en HAW-KINGDOM, HAW-PROVISIONAL, HAW-REPUBLIC y HAW. Las fichas de los años de transición deben mostrar los predecesores del mismo año con su institución y fechas, sin atribuirles el Gobierno de la entidad sucesora.

Identificadores comprobados: Reino de Hawái Q156418; República de Hawái Q1057542; región Zululandia Q13558877; reino merina Q1071439. El Gobierno provisional de Hawái y la administración de 1898–1899 no reciben un QID sin verificar. Q165903 es un asteroide, no Zululandia; Q34439 no se utiliza para Hawái. Estos identificadores son enlaces de identidad, no pruebas suficientes de cronología política.

## Asia

### Qing

Guangxu (Q299710) es soberano formal de toda esta ventana. Su Gobierno personal de 1889–1898 y el poder de Cixi (Q47842) son funciones distintas. Se incluyen dos observaciones acotadas de regencia/control de Cixi, con precisión anual. No se inventa una regencia ininterrumpida ni una fecha exacta para la transferencia de 1889 o el golpe de 1898.

Fuente institucional: [Beijing, historia de Guangxu y Cixi](https://english.visitbeijing.com.cn/article/47ON76ql8M0). Pendiente: documentar con mejor precisión el reparto de la primera regencia con Ci’an (Q1150358) y su fallecimiento de 1881. La ausencia de este registro es un hueco de investigación, no prueba de que no ejerciera autoridad.

### Japón

Meiji/Mutsuhito (Q174231) se mantiene como emperador; las jefaturas del Gobierno son independientes. Sanjō Sanetomi aparece como daijō-daijin antes del establecimiento del gabinete moderno el 22/12/1885. Se registran las sucesivas presidencias del gabinete de Itō, Kuroda, Yamagata, Matsukata y Ōkuma, y las suplencias de Sanjō de 1889 y Kuroda de 1896. La numeración de un gabinete y la persona que despacha provisionalmente no son categorías equivalentes.

Fuentes: [cronología de la Agencia de la Casa Imperial](https://www.kunaicho.go.jp/kunaicho/kunaicho/kunaicho-nenpyo.html), [lista oficial de gabinetes](https://japan.kantei.go.jp/past_cabinet/index.html), [Biblioteca Nacional de la Dieta: Sanjō](https://www.ndl.go.jp/portrait/e/datas/97/?lang=en). El antiguo índice japonés `/jp/rekidainaikaku/index.html` devuelve 404; se emplea el índice inglés vigente. La lista oficial sitúa el cierre del segundo gabinete Itō en 31/8/1896, no en el nombramiento posterior de Matsukata.

Pendiente de refuerzo: documento institucional específico para el despacho interino de Kuroda 31/8–18/9/1896. No confundir al político Kuroda Kiyotaka con el pintor Kuroda Seiki.

### Corea

Gojong (Q257425) figura como rey de Joseon en JOS y como emperador en KEM desde 12/10/1897. La adopción de la era Gwangmu, el rito imperial y el primer edicto con el nombre estatal tienen fechas próximas pero distintas. La dominación japonesa de 1905/1910 no se retrotrae a esta década.

Fuentes: [Museo de Historia de Seúl, exposición del Imperio](https://museum.seoul.go.kr/eng/board/NR_boardView.do?bbsCd=1044&seq=20170222133346596), [Comité Nacional de Historia de Corea](https://contents.history.go.kr/front/kc/printViewPopup.do?levelId=kc_i401000). La autoridad de la reina Myeongseong, Daewongun y las intervenciones extranjeras requiere una serie adicional de poder efectivo; no se reduce toda la historia a una sola persona.

### Siam, Birmania y Afganistán

Chulalongkorn/Rama V (Q158861) conserva el trono de Siam durante toda la ventana. Las presiones coloniales y cesiones territoriales no equivalen a anexión completa. Fuente: [UNESCO, archivos de la transformación de Siam](https://www.unesco.org/en/memory-world/archival-documents-king-chulalongkorns-transformation-siam-1868-1910).

Thibaw (Q470986) deja de gobernar tras la toma de Mandalay el 28/11/1885. El traslado al exilio del día siguiente, la anexión proclamada en 1886 y su fallecimiento de 1916 son sucesos diferentes. La Baja Birmania ya era británica antes de 1885. Fuentes: [Ministerio de Información de Myanmar](https://www.moi.gov.mm/moi:eng/index.php/article/16549), [National Army Museum: captura de Thibaw](https://collection.nam.ac.uk/detail.php?acc=1974-03-148-5). No atribuir al rey toda la silueta moderna de Myanmar ni prolongar el mandato hasta su muerte.

Abdur Rahman (Q31649) es observado desde el cierre de julio de 1880, con precisión mensual, a partir del ofrecimiento del trono documentado ese mes. El acuerdo restringía las relaciones exteriores; no lo convertía en gobernador colonial británico. Ayub Khan y los conflictos de 1880 requieren registro rival y cobertura regional propios. Fuente: [National Army Museum, segunda guerra angloafgana](https://www.nam.ac.uk/explore/second-afghan-war).

### Persia y otomanos

Naser al-Din (Q159416) muere asesinado el 1/5/1896; Mozaffar al-Din (Q467021) le sucede. Su llegada posterior a Teherán y las ceremonias no sustituyen la fecha de sucesión. Fuente: [Encyclopaedia Iranica, período Qajar](https://www.iranicaonline.org/articles/iran-ii2-islamic-period-page-5/).

Abdülhamid II (Q134817) es sultán otomano durante toda la ventana. Los protectorados, provincias y relaciones de vasallaje precisan metadatos territoriales propios: no asignar independencia ni anexión homogéneas a todos ellos. Fuente: [Instituto de Historia de Turquía, sultanes](https://ttk.gov.tr/osmanli-padisahlari/).

### Camboya y Vietnam

Norodom I (Q559803) mantiene el título real de Camboya bajo protección francesa. Las reformas impuestas de 1884 y el poder del residente desde 1897 restringen su autoridad. Fuentes: [Library of Congress, estudio institucional de Camboya](https://tile.loc.gov/storage-services/master/frd/frdcstdy/ca/cambodiacountrys00ross/cambodiacountrys00ross.pdf), [biblioteca gubernamental NCDD, tratado de 1863](https://library.ncdd.gov.kh/detail/11814/download).

La Unión Indochina se constituye en 1887; su contorno o nombre en 1880 no acredita la misma institución ni control francés uniforme de Annam/Tonkin. Cochinchina era colonia de administración directa; Camboya, Annam y Tonkin tenían protectorados y autoridades locales diferentes. Laos se incorpora en 1893 y Kouang-Tchéou-Wan en 1899. Fuente preferida: [Archives nationales d’outre-mer, fondos de Indochina](https://archives-nationales-outre-mer.culture.gouv.fr/faire-une-recherche/indochine). Una cronología divulgativa del Ministerio de Defensa francés incluye Laos retrospectivamente en 1887; prevalece aquí la descripción archivística desglosada.

Vietnam queda **sin nueva serie manual completa** en este curador: Tu Duc Q466976; Duc Duc Q534019; Hiep Hoa Q465598; Kien Phuc Q465593; Ham Nghi Q447616; Dong Khanh Q342476; Thanh Thai Q465059 son candidatos de identidad. No convertir fechas procedentes de resúmenes contradictorios en precisión diaria verificada. Se conservarán los registros genéricos que pasen la validación temporal. Fuente primaria institucional para fases: [Gobierno de Hue, caída de la corte en julio de 1885 y entronización de Dong Khanh el 19/9/1885](https://hue.gov.vn/Du-dia-chi/tb/Thua-Thien-Hue-dau-tranh-chong-thuc-dan-Phap-1885-1916-516945). Ham Nghi pasa a encabezar resistencia y no debe tratarse como si su captura y la instalación del monarca respaldado por Francia fueran un único hito.

## África

### Congo

Leopoldo II (Q12967) figura como soberano del Estado Libre del Congo desde una observación al cierre de 1885. El Estado separado en unión personal no era aún colonia del Estado belga; la anexión belga corresponde a 1908. La autorización parlamentaria de 30/4/1885, los reconocimientos y la notificación de 1/8 son documentos distintos; no se inventa una fundación el 31/12 ni Congo Libre en 1880.

Fuentes: [Archivos del Estado belga, inventario institucional](https://agatha.arch.be/data/ead/BE-A0545_724272_807520/annexes/BE-A0545_724272_807520_fre.ead.pdf), [boletín oficial de 1885–1886 con la notificación](https://www.memoiresducongo.be/wp-content/uploads/2019/01/BOEIC1885-86.-acte-g%C3%A9n%C3%A9ral-de-Berlin.pdf). Esta autoridad central no borra las entidades africanas previas ni acredita control uniforme del territorio que se dibuja.

### Etiopía

Yohannes IV (Q315659) y Menelik II (Q244748) se separan en 1889 con precisión anual en el curador. La fecha diaria de Matamma/Metemma y las distintas fechas de proclamación, reconocimiento y coronación merecen una revisión posterior antes de elevar la precisión. El tratado de Wuchale/Ucciali de 2/5/1889 tenía interpretaciones incompatibles sobre relaciones exteriores; no debe pintarse como anexión italiana aceptada de Etiopía. Adwa y el tratado de Addis Abeba de 29/10/1896 terminan esa reclamación.

Fuentes: [Universidad de Hamburgo, corpus de manuscritos sobre Yohannes](https://betamasaheft.awhamburg.de/persons/PRS10378Yohanne/main), [Archivos Diplomáticos franceses, correspondencia de 1888–1889](https://archivesdiplomatiques.diplomatie.gouv.fr/ark:/14366/zr6j7qsh920n), [manual diplomático británico de 1919 digitalizado por LOC](https://tile.loc.gov/storage-services/service/gdc/gdclccn/a2/20/00/96/6/a22000966/a22000966.pdf).

### Madagascar

Los mandatos de Ranavalona II (Q240168), Ranavalona III (Q233326) y el primer ministro Rainilaiarivony (Q528996) van en HIST-Q1071439. La ocupación de 1895 y anexión francesa de 1896 no eliminan instantáneamente el título real: la monarquía se suprime por decreto de 28/2/1897. Exilio, cambio de soberanía y abolición no son intercambiables.

Fuentes: archivos institucionales de la Iglesia malgache [Ranavalona II](https://www.fjkm.mg/ny-fjkm/tantara-sy-arsiva/histoire-ranavalona-ii/), [Ranavalona III](https://www.fjkm.mg/synodamparitany/vaovao-farany/biographie-ranavalona-iii/); [reproducción de documentos originales de 1897](https://www.bibliothequemalgache.com/pdf/BME45.pdf); [estudio institucional IRD](https://horizon.documentation.ird.fr/exl-doc/pleins_textes/divers19-04/34354.pdf). La biografía institucional de la reina contiene otros detalles discordantes; se toman las fechas de reinado corroboradas, no se valida todo su relato. Fin de Rainilaiarivony: precisión anual 1895, pendiente detalle de exilio/cese.

### Zululandia

Cetshwayo (Q380403) aparece como rey depuesto/reclamante en 1880–1882, no gobernante de un reino intacto. La partición de 1879 en jefaturas, su restitución parcial de 1883, los conflictos internos y su muerte de 8/2/1884 son fases distintas. Dinuzulu (Q888215), proclamado 20/5/1884, representa autoridad disputada; la anexión británica de 1887 impide prolongar independencia hasta 1913. No se equipara un contorno de fuente al área efectiva de mando de ninguno de ellos.

Fuentes: [National Army Museum, guerra zulú y consecuencias](https://www.nam.ac.uk/explore/zulu-war), [South African History Online, Cetshwayo](https://sahistory.org.za/people/king-cetshwayo). Pendiente: las jefaturas de los trece territorios y la extensión diaria del territorio restaurado. No se reemplazan por el monarca británico como si fuese una autoridad local única.

### Repúblicas boer

Orange: Brand Q1390594 hasta 14/7/1888; Reitz **Q726327** desde 10/1/1889 hasta 11/12/1895; Steyn Q2355196 observado desde el cierre de 1896. Falta completar las suplencias entre estas presidencias. El padre homónimo de Reitz, Q110611557, no es el presidente.

Fuentes: [biografía de Brand, SAHO](https://sahistory.org.za/people/johannes-henricus-brand), [investigación doctoral de la Universidad del Estado Libre, fechas de Reitz](https://scholar.ufs.ac.za/server/api/core/bitstreams/6759bbf2-4445-49d8-83a5-58847e574705/content), [museos provinciales, Antigua Presidencia](https://www.sacr.fs.gov.za/wp-content/uploads/2012/07/Provincial-Museums-brochure.pdf).

Transvaal: no se añade una presidencia continua de Paul Kruger desde 1880. Había anexión británica de 1877 y después triunvirato/restitución antes de la presidencia de 1883. Sus fases deben respetarse en TRV; la segunda guerra boer empieza en 1899. Las memorias de Kruger son testimonio primario con perspectiva política propia, no árbitro neutral de todas las disputas.

### Zanzíbar

Seis sultanes identificados: Barghash Q703018; Khalifa Q924354; Ali Q423643; Hamad Q561747; Khalid Q470598 y Hamoud Q928434. La candidatura oficial de Tanzania acredita la secuencia anual. Para los primeros relevos se conservan límites anuales expresamente normalizados; no se presentan las fechas diarias de un catálogo secundario como verificadas por el expediente patrimonial. La sucesión de 25–27/8/1896 sí distingue muerte de Hamad, Gobierno disputado de Khalid, bombardeo y acceso de Hamoud. Protectorado desde 1890, no república popular anterior a 1964.

Fuentes: [expediente oficial UNESCO](https://whc.unesco.org/uploads/nominations/173rev.pdf), [SAHO, guerra anglozanzibarí](https://sahistory.org.za/article/anglo-zanzibar-war-1896). Pendiente: fuente primaria diaria para cada relevo de 1888, 1890 y 1893 y la serie de representantes británicos.

## Oceanía

Hawái: Kalākaua Q163080 muere el 20/1/1891; Liliʻuokalani Q107288 le sucede entonces, distinta de su proclamación pública del 29/1. Su Gobierno termina con el golpe del 17/1/1893, no con la abdicación forzada posterior. Sanford Dole Q333691 preside el Gobierno provisional hasta 3/7/1894 y la república desde 4/7/1894. Desde la transferencia de 12/8/1898 continúa administración local bajo Estados Unidos, no soberanía independiente ni todavía el cargo de gobernador territorial, creado en 1900.

Fuentes: [Palacio Iolani](https://www.iolanipalace.org/history/), [NARA, resolución de anexión y cronología](https://www.archives.gov/milestone-documents/joint-resolution-for-annexing-the-hawaiian-islands), [documento de protesta de la reina reproducido por el Congreso](https://www.govinfo.gov/content/pkg/CHRG-106shrg36384/pdf/CHRG-106shrg36384.pdf), [Universidad de Hawái, prensa y república](https://libweb.hawaii.edu/digicoll/nupepa_kuokoa/kuokoa_htm/Kuokoa_Essay.pdf). No se utiliza la guía divulgativa de Chronicling America para días exactos: contiene fechas incompatibles con los documentos originales.

Tonga: George Tupou I Q379840 y George Tupou II Q379844 se separan en 1893 con precisión anual. El protectorado británico de 1900 no se retrotrae. Fuente: [documentación patrimonial gubernamental](https://www.tongatourism.travel/wp-content/uploads/2022/09/Tongatapu-Heritage-Sites.pdf). Pendiente: verificación institucional diaria de la sucesión de febrero de 1893.

## Anacronismos del inventario cartográfico temprano

| Registro de fuente | Tratamiento editorial necesario |
| --- | --- |
| People’s Republic of Zanzibar / Q157535 en 1880 | Corregir identidad a sultanato; guardar nombre de fuente como procedencia, no como régimen. |
| Natalia Republic / Q1029847 | La república terminó con la anexión de 1843. En 1880 el contorno sólo puede ser referencia de Natal; no crear presidencia republicana. [Parlamento británico](https://www.parliament.uk/about/living-heritage/evolutionofparliament/legislativescrutiny/parliament-and-empire/parliament-and-the-american-colonies-before-1765/the-settler-colonies-south-africa/). |
| German Africa antes de 1884 | Referencia de fuente anacrónica; no colorear por dominación alemana en 1880. [Bundesarchiv fecha su período colonial en 1884–1918](https://www.bundesarchiv.de/im-archiv-recherchieren/archivgut-recherchieren/nach-themen/kolonialgeschichte/). Falta reconstruir las entidades africanas y tratados de cada región. |
| French Indochina antes de 1887 | Referencia agrupada, con fases de colonia/protectorados; no retrotraer la Unión ni Laos. Véanse ANOM arriba. |
| Talpur Dynasty / Q19569014 en 1885 | No igualar dinastía con un Estado de todo Sindh. La conquista de 1843 no eliminó automáticamente toda autoridad Talpur: Khairpur conservó una rama principesca. La geometría debe clasificarse como referencia hasta acreditar qué territorio reproduce. Falta fuente primaria/institucional definitiva y serie de Khairpur. |
| Ethiopian Empire, Zululand, Merina | El contorno no demuestra soberanía uniforme ni vacío político fuera del catálogo. Registrar disputas, jefaturas y autoridades locales como tales. |

## Símbolos e imágenes: candidatos, no descargas realizadas

Este curador **no descarga ni incorpora banderas**. El integrador de símbolos debe verificar cada imagen, licencia, fechas y uso; los nombres siguientes son candidatos para localizar originales, no especificaciones oficiales universales.

- Qing: banderas del dragón, distinguiendo variante triangular anterior a 1889 y rectangular posterior; no retrotraer la republicana de 1912.
- Japón: Hinomaru para representación estatal, diferenciada del estandarte imperial y los pabellones militares/navales.
- Corea: variantes iniciales del Taegukgi de 1882/1883 y emblemas imperiales posteriores a 1897; no fingir un diseño oficial idéntico en 1880.
- Siam: elefante blanco sobre rojo; Birmania Konbaung: pabellón del pavo real sujeto a contexto real/estatal; monarquías vietnamitas: no usar la bandera roja actual.
- Madagascar: símbolos de Ranavalona II/III y de la monarquía, no pabellón francés antes de documentar su uso; Zululandia: evitar banderas modernas inventadas retrospectivamente.
- Zanzíbar: rojo sultánico; diferenciación de protectorados mediante metadatos y no sustitución automática por Union Jack.
- Congo: estrella amarilla sobre azul para el Estado Libre, sin bandera belga antes de 1908.
- Hawái: bandera del reino retenida en etapas posteriores no implica continuidad del régimen. Tonga: distinguir pabellón estatal de estandartes reales.

Los retratos deben corresponder a la persona, no necesariamente a la fecha exacta de una fotografía posterior. La ficha debe poder explicar si usa retrato oficial, fotografía de archivo o imagen histórica. Si no hay reproducción comprobada, el hueco se declara y no se rellena con una imagen generada o un homónimo. El curador reutiliza por persona todos los retratos ya adquiridos.

## Pendientes explícitos

1. Completar series locales y metropolitanas de colonias, residentes y triunviratos; este archivo no afirma que las 21 entidades cubran todo el mundo.
2. Vietnam 1883–1889, Nepal, Mascate/Omán, Marruecos, poderes efectivos Qing y jefaturas regionales africanas: revisión documental adicional antes de llamarlos completos.
3. Precisiones diarias de las observaciones anuales de Etiopía, Zanzíbar, Tonga, Steyn y Rainilaiarivony.
4. Verificar los símbolos candidatos y adquirir retratos por el proceso único de medios, preservando licencias y evitando búsquedas homónimas. Reitz padre/hijo y Kuroda político/pintor son casos comprobados de riesgo.
5. El catálogo no sustituye geografía efectiva: no extrapolar una reclamación imperial al control total del contorno ni una ausencia de registros a ausencia de sociedad, administración o Estado.

Validación realizada en memoria sobre el catálogo de trabajo: entrada intacta; segunda aplicación idéntica; todos los mandatos con fin desde 1900 idénticos; todas las listas de banderas intactas. No se ha ejecutado el curador sobre `public/`.
