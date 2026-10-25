# Autoridades europeas,1880–1899: curación focal0.13

Fecha de revisión:25/10/2026. Integración: `scripts/curate-1880-europe.py`.

Este módulo complementa la adquisición general; no certifica una reconstrucción completa de todos los gabinetes, regentes, ministros y miembros de órganos colegiados. No modifica fronteras ni banderas, no descarga medios y no atribuye a una monarquía constitucional el poder cotidiano del Gobierno. Una imagen previamente registrada se conserva por identidad personal, también al ejecutar el curador de nuevo.

## Contrato de integración y conservación

- `curate(data)` devuelve una copia; nunca altera su argumento ni escribe archivos.
- Todas las altas están acotadas al1/1/1880–31/12/1899. Los extremos de cobertura llevan `startIsCoverageBoundary` o `endIsCoverageBoundary`; no son actos de nombramiento o dimisión.
- Los registros previos que ejercen en1900 o después, incluso los que empiezan antes, se conservan literalmente. La prioridad de curación del resolvedor selecciona la corrección acotada sin destruir el registro posterior.
- El curador sustituye solamente los segmentos solapados de la misma persona terminados antes de1900. No elimina un titular distinto para ocultar una discrepancia; deben revisarse esas discrepancias en la adquisición o en una corrección expresamente documentada.
- Los campos de país y las banderas previas se conservan. Sólo se crean entidades ausentes mediante `setdefault`; no se cambia su nombre si ya existe.
- Ejecución explícita: `python scripts/curate-1880-europe.py --input entrada.json --output salida.json`. Se rechaza usar la misma ruta de entrada y salida. El módulo no se ejecuta por importación.
- Es idempotente: primero captura los retratos existentes, elimina únicamente sus propias altas etiquetadas y reconstruye los mismos términos. No consulta la red.

## Alemania: soberanos y cancilleres

El [objeto histórico sobre el año de los tres emperadores del Deutsches Historisches Museum](https://www.dhm.de/lemo/bestand/objekt/tragbare-medaille-auf-das-dreikaiserjahr-1888) distingue GuillermoI hasta9/3/1888, FedericoIII desde9/3 hasta15/6 y GuillermoII desde15/6. No se usa la coronación como fecha sucesoria. Identidades: GuillermoI`Q150652`, FedericoIII`Q58600`, GuillermoII`Q2677`.

La [biografía institucional de Bismarck](https://www.dhm.de/lemo/biografie/otto-bismarck) distingue la petición de dimisión18/3/1890 de la destitución20/3. El [inventario del Geheimes Staatsarchiv](https://archivdatenbank.gsta.spk-berlin.de/midosasearch-gsta/MidosaSEARCH/i_ha_rep_89/xml/inhalt/GStA_i_ha_rep_89_4_1_2.htm) permite seguir el expediente. La [exposición del Bundesarchiv](https://artsandculture.google.com/story/lQWRwGN7YRIA8A?hl=de) fecha Caprivi20/3/1890–28/10/1894 y Hohenlohe desde29/10/1894; existen repertorios que usan26/10 para la dimisión de Caprivi. Se conserva el criterio de la serie archivística y se declara la diferencia. Identidades: Bismarck`Q8442`, Caprivi`Q10873`, Hohenlohe`Q77166`.

## Rusia: diferencia juliano/gregoriano

La [historia del Jardín de Ingenieros, Museo Ruso](https://igardens.ru/en/убийство-императора-александра-ii-и-ист/) sitúa el asesinato de AlejandroII el13/3/1881 gregoriano,1/3 juliano. AlejandroIII le sucede. La [cronología de la Library of Congress](https://guides.loc.gov/chronicling-america-czar-nicholas-ii) distingue la sucesión de NicolásII el1/11/1894 de su coronación26/5/1896. Su introducción abreviada no debe prevalecer sobre esas entradas cronológicas. El [repertorio contemporáneo conservado por la Library of Congress](https://tile.loc.gov/storage-services/public/gdcmassbookdig/newimperialencyc26unse/newimperialencyc26unse.pdf) permite contrastar ambos acontecimientos.

En el sigloXIX la diferencia es de12días:20/10/1894 juliano corresponde a1/11 gregoriano. Añadir13días, como hacen algunas páginas modernas, produce un2/11 erróneo. Identidades: AlejandroII`Q83171`, AlejandroIII`Q120180`, NicolásII`Q40787`. No se inventa un primer ministro de tipo1905 para este período ni se retroproyectan autoridades de la Federación Rusa.

## España: monarca menor y ejercicio de la regencia

El [Congreso, reinado de AlfonsoXII](https://www.congreso.es/en/cem/alfonsoxii), y la [Regencia de MaríaCristina](https://www.congreso.es/en/cem/regmariacristina) documentan la muerte25/11/1885, la regencia desde ese fallecimiento y el juramento30/12. AlfonsoXIII es rey desde su nacimiento17/5/1886; la regente ejerce las funciones de la Corona durante su minoría. No se atribuye a María de las Mercedes un reinado entre ambos.

Identidades comprobadas: AlfonsoXII`Q32347`, MaríaCristina de Habsburgo-Lorena`Q538125`, AlfonsoXIII`Q18363`. El retrato de la regente no debe sustituirse por otra MaríaCristina. La serie de presidentes del Consejo permanece en la adquisición general y exige auditoría separada de nombramientos, ceses y sustituciones interinas.

## Reino Unido

La [serie regnal del Parlamento](https://api.parliament.uk/regnal-years/reigns/6) fecha Victoria20/6/1837–22/1/1901; se incorpora la ventana1880–1899 como cobertura. La [Casa Real](https://www.royal.uk/encyclopedia/victoria-r-1837-1901) explica la distinción entre la Corona y el Gobierno. Identidad`Q9439`.

La [lista de la House of Commons Library, página8](https://researchbriefings.files.parliament.uk/documents/SN04256/SN04256.pdf) y las [fichas de antiguos primeros ministros](https://www.gov.uk/government/history/past-prime-ministers/william-ewart-gladstone) corroboran la secuencia Disraeli1874–1880; Gladstone1880–1885; Salisbury1885–1886; Gladstone1886; Salisbury1886–1892; Gladstone1892–1894; Rosebery1894–1895; Salisbury1895–1902. La lista parlamentaria expresa años, no todos los días de cada relevo. Se conserva la adquisición diaria previa sin afirmar que esta revisión haya contrastado todos sus días. Identidades existentes: Disraeli`Q82006`, Gladstone`Q160852`, Salisbury`Q243705`, Rosebery`Q244620`.

## Francia: presidencia y Gobierno separados

Las cronologías del Elíseo documentan [Grévy](https://www.elysee.fr/jules-grevy), [Carnot](https://www.elysee.fr/sadi-carnot), [Casimir-Perier](https://www.elysee.fr/jean-casimir-perier), [Faure](https://www.elysee.fr/felix-faure) y [Loubet](https://www.elysee.fr/emile-loubet). Identidades respectivas`Q296083`, `Q215778`, `Q315656`, `Q296076`, `Q169502`.

Se mantiene la dimisión de Grévy2/12/1887 y la elección de Carnot3/12. Carnot sufre el atentado24/6/1894 pero muere pasada medianoche25/6; lo corrobora el [acta de autopsia conservada por la BnF](https://gallica.bnf.fr/ark%3A/12148/bpt6k76591c.pdf), la [ficha de la Asamblea Nacional](https://www2.assemblee-nationale.fr/sycomore/fiche?num_dept=1453) y la [historia del Ministerio del Interior](https://www.interieur.gouv.fr/actualites/grands-dossiers/grandes-et-petites-histoires-du-patrimoine-prefectoral/24-juin-1894). Se siguen las fechas del Elíseo27/6/1894–16/1/1895 para Casimir-Perier: varias tablas resumidas oficiales discrepan uno o más días y no deben copiarse acríticamente. El [Senado](https://www.senat.fr/connaitre-le-senat/lhistoire-du-senat/dossiers-dhistoire/emile-loubet/lelection-presidentielle-du-samedi-18-fevrier-1899.html) confirma la elección de Loubet18/2/1899 tras la muerte de Faure16/2.

El Gobierno es dirigido por el presidente del Consejo, no por el presidente de la República. La biografía de Loubet documenta el gabinete de Pierre Waldeck-Rousseau desde22/6/1899: se corrige el nombre de uso, frente al civil René, para`Q358452`. La adquisición contiene la serie general de gabinetes, todavía sin auditoría institucional diaria completa. Los períodos de vacancia presidencial los ejerce constitucionalmente el Consejo de Ministros; no debe presentarse a su presidente como un presidente electo ordinario.

## Italia

El [Quirinale, Sala del Reino de Italia](https://palazzo.quirinale.it/luoghi/pdf/it/sala-regno-italia.pdf) respalda UmbertoI`Q153688`, rey1878–1900; se limita aquí a1880–1899. La [cronología de la XVI legislatura del Senado](https://www.senato.it/legislature/regno/italia/16/resoconti-elenco-cronologico) verifica los gabinetes de DepretisVII29/6/1885–4/4/1887 yVIII4/4–29/7/1887. Se unen sus períodos contiguos de la misma persona`Q356711` sin convertir la renovación del gabinete en un cambio de jefe.

La [XVII legislatura](https://www.senato.it/legislature/regno/italia/17/resoconti-elenco-cronologico) documenta Crispi hasta6/2/1891, Rudinì6/2/1891–15/5/1892 y Giolitti15/5/1892–15/12/1893. La [XVIII](https://www.senato.it/legislature/regno/italia/18/resoconti-volumi-e-indici) separa los gabinetes CrispiIII yIV,15/12/1893–14/6/1894–10/3/1896. Son referencias de integración pendientes de altas individuales, no registros generados por este curador.

La [XX legislatura](https://www.senato.it/legislature/regno/italia/20/resoconti-elenco-cronologico?session=1) fecha PellouxI29/6/1898–14/5/1899 yII14/5/1899–24/6/1900. El [acta30/6/1898](https://www.senato.it/service/PDF/PDFServer/DF/422790.pdf) reproduce el nombramiento del día anterior. Se añade Pelloux`Q534227` dentro de la ventana. Una ficha senatorial abrevia erróneamente el primer fin como4/5; se prefiere la cronología legislativa y no se inventa un vacío de diez días.

## Austria-Hungría y sus dos Gobiernos

La [historia de FranciscoJoséI](https://www.habsburger.net/de/personen/habsburger-herrscher/franz-joseph-i) y el [DHM](https://www.dhm.de/lemo/biografie/franz-joseph-i) permiten distinguir el reinado austríaco desde1848 de la coronación húngara1867. Se registra un soberano común`Q51056`, con Gobiernos austríaco y húngaro propios, además de ministerios comunes. No existió un primer ministro único de todo el conjunto.

El [Parlamento austríaco](https://www.parlament.gv.at/recherchieren/personen/parlamentarierinnen-ab-1848/parlamentarier-1848-1918/taaffe) y la [edición de actas de la Academia Austríaca de Ciencias](https://mrp.oeaw.ac.at/pages/show.html?document=MRP-3-0-04-1-00000000-teilnehmer.xml) fechan Taaffe12/8/1879–11/11/1893,`Q550748`. Se presenta explícitamente como jefe cisleitano. Para KálmánTisza`Q254737`, la [Academia Húngara de Ciencias](https://mta.hu/data/dokumentumok/egyeb_dokumentumok/2025/Tisza_K%C3%A1lm%C3%A1n_KOI_MTA_2025.pdf) fecha el ejercicio hasta13/3/1890; el [repertorio del Archivo Nacional](https://real-eod.mtak.hu/16964/1/MolDigiLib_MOLkiadv4_02.pdf) extiende la composición del gabinete hasta15/3. No se confunden el ejercicio personal y el cambio completo del gabinete.

Pendiente: terminar la serie austríaca después de Taaffe y contrastar toda la serie húngara Szapáry–Wekerle–Bánffy–Széll. Los datos adquiridos no equivalen por sí solos a esa validación. El curador incorpora Tisza en la entidad histórica común y en la ficha húngara cuando se use esa entidad, sin atribuirle poder sobre Austria.

## Portugal, Bélgica, Países Bajos y Luxemburgo

La [publicación de las colecciones del Palacio de Sintra](https://www.parquesdesintra.pt/media/upzl30vk/colecoesemfoco_pnsintra_ebook_2_lq.pdf) documenta la muerte de LuisI`Q156175` el19/10/1889. La [prensa contemporánea conservada por la Hemeroteca Municipal de Lisboa](https://hemerotecadigital.cm-lisboa.pt/obras/ocidente/1908/N1048/N1048_master/N1048.pdf) distingue la sucesión de CarlosI`Q158874` ese día de su aclamación28/12. La [Casa Real belga](https://www.monarchie.be/en/royal-family/history/king-leopold-ii) sitúa LeopoldoII`Q12967` en1865–1909. El Estado Independiente del Congo no debe confundirse con una colonia del Estado belga antes de1908.

La Casa Real neerlandesa documenta [GuillermoIII](https://www.koninklijkhuis.nl/onderwerpen/koninklijk-huis/geschiedenis/koningen-en-koninginnen/koning-willem-3-1849-1890), fallecido23/11/1890, y [Guillermina](https://www.koninklijkhuis.nl/onderwerpen/koninklijk-huis/geschiedenis/koningen-en-koninginnen/koningin-wilhelmina-1890-1948), reina desde ese día. Identidades`Q125649`, `Q150747`. Emma`Q57664` ejerce brevemente por incapacidad del marido20–23/11/1890 y posteriormente por minoría de la hija. La página neerlandesa publica8/12/1890–31/8/1898 para esta segunda regencia; la página inglesa abreviada difiere en el día final. No se rellena por inferencia el intervalo23/11–8/12; queda pendiente precisar la relación entre sucesión, investidura y actuación provisional del Consejo de Estado.

La [Casa Gran Ducal luxemburguesa](https://monarchie.lu/fr/la-monarchie/lhistoire-de-la-dynastie-de-nassau) distingue la sucesión de Adolfo`Q57302`23/11/1890 de su juramento9/12. La [publicación del Gobierno luxemburgués](https://sip.gouvernement.lu/dam-assets/publications/brochure-livre/minist-etat/sip/livre/famille_grand-ducale/La_famille_grand-ducale-FR.pdf) fecha sus regencias8/4–3/5/1889 y4–23/11/1890; los juramentos11/4 y6/11 son hechos distintos. Guillermina no hereda Luxemburgo: termina la unión personal con los Países Bajos.

## Escandinavia

La [Casa Real danesa](https://www.kongehuset.dk/en/the-monarchy-in-denmark/the-royal-lineage/) documenta CristiánIX`Q151305`,1863–1906. La [Casa Real sueca](https://www.kungahuset.se/english/royal-house/the-bernadotte-dynasty/oskar-ii) y la [historia del Gobierno noruego](https://www.regjeringen.no/en/the-government/previous-governments/historiske-artikler/offices/the-establishing-of-the-norwegian-state/norways-monarch-since-1814/id449228/) distinguen ÓscarII`Q52924` como rey de ambos países en unión personal, con Gobiernos y constituciones propios. No se convierte Noruega en una provincia sueca ni se aplica la ruptura de1905 antes de tiempo. La auditoría diaria de los ministros de cada Estado continúa pendiente.

## Grecia, Rumanía, Serbia, Montenegro y Bulgaria

El [Parlamento griego, historia constitucional](https://www.hellenicparliament.gr/Vouli-ton-Ellinon/To-Politevma/Syntagmatiki-Istoria), y su [catálogo histórico](https://www.hellenicparliament.gr/UserFiles/f3c70a23-7696-49db-9148-f24dce6a27c8/katalogos_ktirio.pdf) sostienen JorgeI`Q17142`,1863–1913. La confianza parlamentaria exigida desde1875 impide tratar al rey como único gobernante. La sucesión completa Trikoupis–Deligiannis y sus interinos no queda certificada por esta revisión.

El [Museo Nacional de Historia de Rumanía](https://www.mnir.ro/carol-i/) fecha la proclamación del reino14/26 de marzo1881, corroborada por la [Biblioteca Central UniversitariaCarolI](https://restitutio.bcub.ro/storage/item/2023/Apr/carol-i-amintirea-unei-mari-domnii-cercetare-bibliografica/Cl6RydVDsHGNyCJaTx9JDXk9dQfcCE7lPH3iHiBo.pdf). CarolI`Q57146` se registra príncipe hasta25/3 gregoriano y rey desde26/3; la coronación10/22 de mayo es posterior. No se deduce el inicio del reino de tablas con calendarios mezclados.

El [Calendario del Estado serbio1903, Biblioteca Nacional](https://digitalna.nb.rs/attach/NBS/Periodika/SD_FFAB6B516AB99742A20B7C790616A239/1903/b001/output.pdf), fuente contemporánea, da el cambio de príncipe a rey de MilanI`Q313829` el22/2/1882 juliano=6/3 gregoriano; abdica22/2/1889 juliano=6/3 gregoriano. AlejandroIObrenović`Q297547` le sucede como menor; asume anticipadamente sus funciones1/4/1893 juliano=13/4 gregoriano. El [Museo Nacional de Kraljevo](https://nmkv.rs/abdikacija-kralja-milana-m-obrenovica-iv/) documenta la regencia. Queda pendiente enumerar los regentes y sus cambios, incluida la muerte deKostaProtić1892; no se mantiene artificialmente una composición constante. El [Archivo Estatal de Montenegro](https://dacg.me/zvanicne-cestitke-nikoli-i-povodom-jubilarnih-svecanosti-1910-godine/) documenta NicolásI`Q283255` como príncipe antes de1910; no se anticipa su título real.

Para Bulgaria, el [Museo Histórico Regional de Sofía](https://www.sofiahistorymuseum.bg/bg/novini/istoricheski-kalendar/1394-135-години-от-преврата-срещу-княз-александър-і) usa calendario juliano en los acontecimientos de1886: golpe9/8, retorno17/8 y abdicación26/8. Corresponden a21/8,29/8 y7/9 gregorianos. Se interrumpe el ejercicio de AlejandroI`Q159591` durante el golpe y se registra por separado su breve retorno. El [Statesman's Year-Book1913, reproducción de la página original](https://en.wikisource.org/wiki/Page:Statesman's_Year-Book_1913.djvu/820) ofrece las fechas gregorianas: FernandoI`Q151667` elegido7/7/1887, asume el Gobierno14/8, reconocido internacionalmente1896. Se prefiere el ejercicio14/8 para su ficha, distinguiendo la elección. La transcripción deWikisource figura pendiente de revisión; debe cotejarse la imagen original antes de cualquier ampliación de detalle. La [intervención parlamentaria británica8/7/1887](https://api.parliament.uk/historic-hansard/commons/1887/jul/08/bulgaria-the-election-of-prince) confirma que la elección ocurrió el día anterior. Las actas búlgaras históricas identificadas no fueron accesibles en esta sesión; no se afirma haberlas leído. Stambolov`Q313833` se añade como miembro del Consejo de Regencia, sin fingir una presidencia unipersonal ni la lista completa de integrantes.

## Suiza: prevenir confundir presidencia anual y Consejo Federal

La [historia oficial del Bundespräsidium](https://www.admin.ch/de/bundespraesidium-geschichte) explica la presidencia anual, la formación gradual de la rotación y la muerte deHertenstein en1888. El [repertorio del Parlamento, página67](https://www.parlament.ch/centers/documents/de/gedenkblatt-45-legislatur.PDF) ofrece la serie anual desde1848. La [Cancillería Federal, miembros del Consejo desde1848](https://www.bk.admin.ch/dam/de/sd-web/8fBQN-OCfkjr/die_exekutive_bundesratunddepartemente.pdf) distingue miembros del órgano colegiado y sus mandatos prolongados.

La adquisición existente trae tanto presidencias anuales como períodos de consejeros. No se debe llamar a cada consejero «presidente» durante todo su mandato ni presentar al presidente anual como gobernante ejecutivo único. Esta curación focal no reescribe aún esa serie ni certifica el día inicial de los casos excepcionales: Droz1881 requiere estudiar elección/ejercicio provisional y Hammer1888 ejerce como vicepresidente tras la muerte deHertenstein. Tampoco elimina retratos anteriores. Integración pendiente: etiquetar correctamente el Consejo colegiado, contrastar el colegio completo por año y adquirir todos los retratos históricos disponibles.

## Pendientes explícitos

1. Gabinetes e interinos diarios completos, sobre todo Italia, Francia, Grecia, España, las dos mitades austrohúngaras, Benelux y Escandinavia. Las fuentes listadas reducen incertidumbre pero no convierten automáticamente la adquisición en una revisión completa.
2. Consejos de regencia completos deSerbia yBulgaria, con cambios de integrantes y fechas; ejercicio provisional neerlandés1890.
3. Clasificación y composición íntegra del Consejo Federal suizo, sucesiones excepcionales1881/1888 y cobertura de retratos.
4. Adquisición de retratos para losQID nuevos y control de licencias/procedencia. El curador únicamente reutiliza medios ya presentes.
5. Verificación visual integrada de selecciones1900+, para confirmar que la prioridad de curación respeta literalmente sus datos y formatos. Este módulo no altera la interfaz.
