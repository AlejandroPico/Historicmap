# Auditoría de huecos1880–1899: Asia, África y dependencias

Fecha:25/10/2026. Entrada analizada: `.cache/review-1880.json` y catálogo de identidades de trabajo. Esta revisión se limita a los huecos comunicados y a una selección de entidades regionales. No constituye un censo exhaustivo de cargos de cada Estado.

## Entrega reproducible

`scripts/curate-1880-asia-africa-gaps.py` contiene `curate(data)` puro e idempotente. La CLI exige un archivo `--output` explícito; no hace peticiones, descargas ni escrituras en `public/`. Recoge los retratos existentes por identificador de persona antes de regenerar sus31 registros, distribuidos en14 claves. No modifica banderas ni mandatos ajenos, incluidos todos los que alcanzan1900 o fechas posteriores.

Validación realizada en memoria sobre el catálogo actual: entrada intacta; segunda aplicación idéntica; banderas intactas; todos los mandatos cuyo fin es desde1900 idénticos y con el mismo orden. El integrador debe aplicar la función de forma secuencial con las demás curaciones y ejecutar después la auditoría de disponibilidad. El número de huecos no se puede considerar corregido sólo porque el script exista.

La precisión9 es anual,10 mensual,11 diaria. Los extremos de cobertura no son accesos o ceses. Se conservaron explícitamente las limitaciones documentales; no convertir una fecha normalizada de enero/diciembre en una fecha diaria en la ficha.

## Huecos principales y resultado

| Clave de producción | Resultado del curador | Límite explícito |
| --- | --- | --- |
| NPL | Surendra; Prithvi Bir Bikram; Ranodip Singh | El relevo real de mayo1881 se representa con precisión mensual; el cargo Rana es distinto de la monarquía. Bir Shumsher1885–1899 ya existía y se conserva. |
| MAR | HassanI y Abdelaziz | Precisión anual en la sucesión de1894; queda pendiente la regencia efectiva deBaAhmed. No se retrotrae el protectorado de1912. |
| OMN | Turki bin Said hasta4/6/1888 | Se conserva la serie ya existente deFaisal desde1888. Reconocimiento británico y sucesión local son procesos distintos. |
| HIST-Q6500483 y VNM | Siete emperadoresNguyễn, con fases de tutela/resistencia | Doble clave deliberada: la fuente temprana usa dinastía y CShapes usaVNM. No implica que la monarquía administrara uniformemente la colonia deCochinchina. |
| TRV | Kruger como integrante del triunvirato desde13/12/1880; presidente desde9/5/1883 | No se le representa como presidente individual en1880. Faltan los otros dos integrantes y la administración colonial británica de1880–1881. |
| SWZ | Sin nueva fila inventada | El catálogo ya contiene autoridades bajoSWZ. Los cinco huecos de fuente dicenSwaziland(Eswatini) y tienen clave vacía: el arreglo necesario es el alias de resolución. |

### Nepal

La sucesión de Surendra por Prithvi se sitúa en **mayo1881** en la investigación basada en correspondencia diplomática conservada en [SOAS, Political Relations between India and Nepal1877–1923, página59](https://eprints.soas.ac.uk/33911/1/11015636.pdf). El extremo31/5 utilizado en la observación es el cierre del mes de evidencia, no una fecha exacta de muerte o acceso. La [British Library, fotografíaEAP838/1/5/1/38](https://searcharchives.bl.uk/catalog/041-003939737) acredita el reinado1881–1911 dePrithvi, y el [Museo de Arqueología y Antropología deCambridge](https://collections.maa.cam.ac.uk/objects/557260/?page=14138) identifica aSurendra como rey1847–1881.

Ranodip Singh corresponde al período1877–1885. La [oficina del primer ministro](https://opmcm.gov.np/pages/former-prime-ministers/) lo enumera en calendarioBikramSambat; la [British Library, álbumEAP166/2/1/1/2](https://searcharchives.bl.uk/?q=036-002742769&sort=hierarchy) identifica ese mandato. La fila se acota con precisión anual, sin fingir cese el1de enero1885. El catálogo ya contiene la fila posterior deBir Shumsher desde22/11/1885; este curador no la sustituye ni cambia la documentación de1900 en adelante.

Identidades humanas utilizadas: SurendraQ2523476; PrithviQ886987; RanodipQ593609.

### Marruecos

La [Embajada de Marruecos enFrancia](https://fr.diplomatie.ma/fr/histoire-du-maroc-rois-et-dynasties) identifica la sucesión deHassanI(Q496845) porAbdelaziz(Q307132) en1894. No se adopta una fecha exacta a partir de resúmenes que discrepan entre día de muerte, anuncio y proclamación. Los [Archivos del Alto Comisariado deMarruecos, inventario de expedientes debay‘a](https://hcar.gov.ma/wp-content/uploads/2025/01/repertoireDoc.pdf) conservan expedientes1873–1894 y1894–1907, así como informes de6–22/6/1894, útiles para una revisión diaria posterior.

Pendiente: mandato y papel deBaAhmed en el gobierno cotidiano del joven sultán. El soberano nominal y la figura que dirige el Gobierno no son intercambiables.

### Omán

La fuente contemporánea [Persian Gulf Administration Reports1883/84–1904/05, folio89r, British Library/QDL](https://www.qdl.qa/en/archive/81055/vdc_100023373225.0x0000b7) fecha la muerte deTurki binSaid(Q580930) el **4/6/1888**. Se añade ese soberano para cubrir1880–1887 y la transición1888.

El expediente original [IOR/R/15/6/50, sucesión y reconocimiento deFaisal1888–1890](https://www.qdl.qa/en/archive/81055/vdc_100045025652.0x00000e) permite separar sucesión local y reconocimiento británico, que aún se negociaba en1889. No se mueve el comienzo del mandato deFaisal a la fecha en que Londres decide reconocerlo, ni se interpreta el sultanato como control uniforme del interior omaní.

### Vietnam/Đại Nam

Las clavesHIST-Q6500483 yVNM reciben los mismos personajes sólo dentro de su tramo de revisión: la temprana termina en1885 yVNM conserva la continuidad hasta1899. Esto resuelve el cambio de identidad entre fuentes sin copiar líderes modernos retrospectivamente.

La [cronología del Comité Estatal para los Vietnamitas en el Exterior](https://scov.gov.vn/dat-nuoc-con-nguoi/tom-tat-bien-nien-su-vn/xxii.-nha-nguyen-143-nam-1802-1945-quoc-hieu-viet-nam-tu-minh-mang-la-dai-nam-kinh-do-hue-thua-thien-phan-2-.html) acredita la sucesión breve de1883–1884, aunque mezcla expresiones de meses lunares y resúmenes que no permiten convertir todas las fechas sin reconciliación. Por elloTựĐức(Q466976), DụcĐức(Q534019), HiệpHòa(Q465598) yKiếnPhúc(Q465593) reciben **precisión anual**, con el carácter breve indicado y extremos marcados como cobertura. La ficha no debe presentar que todos reinaron durante doce meses ni interpretar una observación1883–1884 como un mandato de dos días.

El [Gobierno deHuế](https://hue.gov.vn/Du-dia-chi/tb/Thua-Thien-Hue-dau-tranh-chong-thuc-dan-Phap-1885-1916-516945) documenta la caída de la corte y la resistencia deHàmNghi(Q447616), además de la entronización deĐồngKhánh(Q342476) el **19/9/1885**. No se prolonga el Gobierno de la capital deHàmNghi hasta el fin de la resistencia. El [Museo Nacional deHistoria](https://vnmh.com.vn/vi/Articles/3098/15571/hoang-dje-thanh-thai-vi-vua-yeu-nuoc-cua-vuong-trieu-nguyen.html) fecha la muerte deĐồngKhánh en **28/1/1889** y el reinado deThànhThái(Q465059) en1889–1907. El nuevo tramo deThànhThái se observa desde el cierre1889, sin atribuir al31/12 una entronización exacta.

Pendiente: resolver calendarios y documentación diaria de los cambios breves1883–1884, regencias y autoridades francesas separadas. La disponibilidad de un emperador no certifica una frontera de control ni administración uniforme sobreAnnam/Tonkin/Cochinchina.

### Transvaal

[South African History Online](https://sahistory.org.za/article/first-anglo-boer-war) documenta la restauración proclamada el **13/12/1880** y el poder compartido dePaulKruger, PietJoubert yM.W.Pretorius frente a la anexión británica de1877. El curador incluye sólo aKruger(Q244407), con cargo de **miembro del triunvirato**, hasta8/5/1883. La [ley de1882 digitalizada por la Universidad dePretoria](https://repository.up.ac.za/bitstreams/8e327641-632a-4b0d-8f3c-120a4cdf10f9/download) contiene la fórmula de representación por el triunvirato y la firma deKruger como vicepresidente: fuente contemporánea independiente de su posterior autobiografía.

[La cronología institucional de su elección](https://sahistory.org.za/dated-event/paul-kruger-elected-president) distingue voto16/4/1883 y juramento **9/5/1883**. Desde ese último día se registra la presidencia; la ventana termina1899 sin tocar la fila1900+. Falta completarJoubert/Pretorius y la administración deOwenLanyon; una ficha conKruger no equivale a un censo íntegro de autoridades.

## Entidades regionales tempranas cubiertas

| Clave exacta | Persona y ventana | Fuente y precisión política |
| --- | --- | --- |
| HIST-Q1658411 | CharlesBrookeQ1065104,1880–1885 | [Museo deSarawak](https://museum.sarawak.gov.my/web/subpage/webpage_view/290) acredita1868–1917. La ventana temprana no es el fin del reinado. Las adquisiciones deBaram1881 yLimbang1890 no se retrotraen. |
| HIST-Q1150344 | AbuBakarQ2637695,1880–1885 | [CasaReal deJohor](https://royal.johor.my/salasilah-kesultanan-johor/): maharajá durante la mayor parte de la ventana; título sultánico reconocido11/12/1885, proclamación13/2/1886 y coronación29/7/1886. Se distinguen esos actos. |
| HIST-Q1317579 | AbdulHamidHalimQ4207009,1882–1885 | [Asamblea deKedah](https://mmk.kedah.gov.my/sejarah/) fecha1882–1943; [consejo religioso](https://maik.kedah.gov.my/wp-content/uploads/2026/01/Pelan-Strategik-MAIK-2026-2030.pdf) usa1881–1943. Se toma una ventana segura desde1882, sin fabricar día de acceso. |
| HIST-Q213467 | SyedAhmadJamalullailQ12710154,1880–1885 | [CasaReal dePerlis](https://dymm.perlis.gov.my/index.php/info-diraja/salasilah-diraja?start=2):1873–1897. La clave del catálogo diceKedah-PerlisDistrict y corresponde alQID dePerlis; no se crea un nuevoEstado regional arbitrario. |
| HIST-Q2571484 | RanbirSinghQ3694970 hasta12/9/1885; PratapSinghQ2842349 observado desde14/9 | Cartas/despachos originales de1885: [muerte comunicada12/9](https://ikashmir.net/historicaldocuments/14.html), [reconocimiento14/9](https://ikashmir.net/historicaldocuments/9.html). El segundo comienzo es observación documental, no afirmación de que la sucesión sólo sucediera el14. Q15675481 redirige al identificador canónicoQ2842349. |
| HIST-Q722071 | MensaBonsuQ1920707,1880–8/3/1883 | [Investigación biográfica deIvorWilks](https://encyclopaediaafricana.com/mensa-bonsu/) fecha deposición8/3/1883. No se prolonga hasta su muerte1896 ni se inventa monarca continuo1883–1885. |
| HIST-Q1679856 | ThahaSyaifuddinQ12521177,1880–1885 | [BPSDM del Gobierno deJambi](https://portalbpsdm.jambiprov.go.id/artikel/buku-sastra/sejarah-sultan-thaha-saifuddin-pahlawan-nasional-jambi/) documenta retirada al interior tras la toma de1858 y resistencia hasta1904. Se etiqueta como sultán depuesto/resistencia, no Gobierno uniforme de todoJambi. Contrastar además la [monografía original del Ministerio deEducación de1979](https://id.wikisource.org/wiki/Sultan_Thaha_Syaifuddin). |
| HIST-Q190165 | OunKhamQ962950,1880–1885 | [Investigación de la Universidad deChiangMai](https://archive.lib.cmu.ac.th/full/T/2011/sudev21111cl_ch2.pdf) sitúa al rey en la fase previa al saqueo de1887. Se evita adoptar sus extremos globales1871–1889 porque otras fuentes separan reinado y regencia de otra manera; la ventana1880–1885 es la fase estable compartida. |

## Pendientes nominales concretos, sin relleno ficticio

| Entidad de auditoría | Evidencia localizada | Pendiente que impide cerrar el hueco |
| --- | --- | --- |
| HIST-Q600524,Sokoto | MuazuDanBello1877–1881; Umaru/Umoru binAli1881–1891; AbdulrahmanDanAtiku1891–1902. [Investigación publicada por AIOU, tabla de sultanes](https://iri.aiou.edu.pk/wp-content/uploads/2016/06/23-the-establishment-of-the-Nigerian.pdf), cotejable con [genealogía histórica digitalizada porGIPE](https://dspace.gipe.ac.in/xmlui/bitstream/handle/10973/34017/GIPE-008078-Contents.pdf?isAllowed=y&sequence=2). | Identificadores humanos no verificados; no se utiliza alMuhammaduBello fallecido en1837 como soberano de1880 ni alAbubakarAtiku de otra generación. Relevo1881 requiere precisión anual o documento diario. |
| HIST-Q1132786,Wadai | Yusuf ibnMuhammadSharif, gobernante desde1874, estable en1880–1885. [Artículo académico con cartas deYusuf de1891/1895 y discusión de1874–1899](https://brill.com/view/journals/wdi/64/2-3/article-p227_005.pdf). | QID humano sin verificar y divergencia1898/1899 en el final del reinado; puede añadirse después una ventana1880–1885 sin decidir ese final. No confundir conYusufII deGranada ni con el califa almohade. |
| HIST-Q403369,Champasak | KhamSouk, corte deBasak, abuelo deBounOum y gobernante frente a las expediciones francesas. [Investigación deKyoto basada en testimonio y documentos deArchaimbault](https://repository.kulib.kyoto-u.ac.jp/dspace/bitstream/2433/250914/1/sas_9_1_99.pdf). | Falta identidad humana inequívoca y fuente institucional que fije toda la ventana1880–1885. No extrapolar automáticamente los extremos1863–1899/1900 de repertorios no corroborados. |
| HIST-Q5362837,JabalShammar | Muhammad binAbdullahAlRashid1872–1897; fuente contemporánea: [tabla deLorimer conservada enQDL](https://www.qdl.qa/download/pdf/81055_vdc_100000000193.0x000307_en.pdf). | QID humano no verificado; ventana1880–1885 documentalmente viable tras resolverlo. No confundir miembros homónimos deAlRashid. |
| HIST-Q1317579,Kedah1880–1881 | ZainalRashidMu‘adzamShahII1879–1881; [investigación universitariaUPSI distingue alprimero1843–1854 delsegundo1879–1881](https://ejournal.upsi.edu.my/index.php/PERS/article/download/1747/1273/2898). | QID humano delsegundo no verificado; el curador empieza conAbdulHamid en1882. No asignar alpadre fallecido1879 ni alprimerZainalRashid. |
| HIST-Q722071,Ashanti1883–1885 | DeposiciónMensaBonsu1883, KwakuDuaII durante unas semanas de1884, consejos/interregno hastaPrempehI1888. [InvestigaciónKNUST basada enPalacio/Manhyia](https://ir.knust.edu.gh/server/api/core/bitstreams/f6b779be-44bf-4e8b-8193-60b26dafc54e/content). | Fechas y autoridades de los consejos; no inventar continuidad monárquica para eliminar un aviso. |
| Jambi,sultanes apoyados porPaísesBajos | La resistencia deThaha no equivale a toda la administración; existieron gobernantes reconocidos porPaísesBajos. | Añadir seriesJamaluddin/Muhieddin y resolver jurisdicciones; la fila deThaha está expresamente calificada. |
| TRV1880–1883 | Triunvirato documentado y ocupación colonial previa. | IncorporarJoubert/Pretorius yOwenLanyon con cargos y fechas verificados. |
| SWZ1889–1895 | Catálogo contieneMbandzeni hasta1889 yNgwaneV desde1895. | Además delalias vacío de fuente, falta regencia deTibatiNkambule y órganos efectivos. No prolongar automáticamente el reinado deMbandzeni. |

Las consultas masivas de búsqueda de identificadores se rechazaron automáticamente en este entorno. Se continuó con catálogos y búsquedas acotadas disponibles; los nombres sin identificador comprobado quedan pendientes, sin inventarQID ni usar un homónimo para cerrar estadísticas.

**Exclusiones deliberadas:** Bali no se convierte en unEstado unitario porque una geometría agregada carezca de autoridad. Talpur/Sindh/Khairpur mantiene su problema de correspondencia entre dinastía y territorio; no se etiqueta todoSindh como soberaníaTalpur de1885. GermanAfrica1880 sigue siendo referencia anacrónica de fuente, no imperio alemán ni espacio sin organización africana. Estos casos requieren reconstrucción de identidades y territorios, no una persona arbitraria.
