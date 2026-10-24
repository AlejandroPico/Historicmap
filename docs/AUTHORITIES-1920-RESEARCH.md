# Autoridades de1920–1949: contraste focal para0.11

Consulta:24 de octubre de2026. Alcance acotado: principales transiciones institucionales, autoridades rivales y monarquías que la adquisición genérica no distingue correctamente. No equivale a una validación mundial de todos los cargos o días. Este documento acompaña `scripts/curate-1920-authorities.py`; no sustituye la auditoría global ni acredita cartografía nueva.

## Estado y procedimiento reproducible

Al terminar esta investigación se han creado el script y esta nota, **sin ejecutar la curación ni modificar `public/data` o manifiestos**. La sintaxis del script se ha comprobado mediante AST; su ejecución, repetición e integración quedan a cargo de la entrega principal, después de finalizar la adquisición `historical-0.11`.

El script contiene43 llamadas declarativas a `term`, algunas dentro de bucles para presentar la misma evidencia en la ficha base y en la autoridad controladora. Genera53 registros focales antes de las copias documentales de series ya adquiridas. El número final depende del catálogo de entrada; no son53 personas distintas ni53 comprobaciones independientes.

- Conserva los retratos por QID **antes** de retirar su etiqueta `curated-1920-0.11`; reutiliza medios acreditados y no descarga imágenes.
- Sólo retira sus registros regenerables completos. Las correcciones de otros registros se limitan a intervalos explícitos, con colas anteriores/posteriores conservadas. Un mandato que atraviesa1949 conserva su ejercicio desde1950; la cola señala que ese comienzo es límite de cobertura, no un nombramiento nuevo.
- No cambia la fecha contemporánea de adquisición, símbolos, licencias, geometrías ni los registros estadísticos.
- Ofrece `--input` y `--output` para comprobar una copia antes de modificar el catálogo principal. Después de integrar, repetir sobre la salida debe conservar los mismos bytes, registros y retratos; verificar además los intervalos de1950 en adelante.
- `ROC`, `RSR` y `YKM` actualizan QID/nombre aunque existan como claves vacías. Requieren enlace temporal desde el resolver y símbolos revisados por separado.

Las copias TWN→ROC1920–1949 y ESP→ESP-REPUBLIC1931–marzo1939 conservan las fuentes originales y señalan explícitamente que **no añaden validación independiente**. La copia republicana excluye a Franco. ESP permanece disponible para las autoridades externas de dependencias españolas.

## Francia: Vichy, Francia Libre y Gobierno provisional

| Función | Decisión y límite |
| --- | --- |
| Pétain, Q5721 | Jefe del Estado francés de Vichy desde11/7/1940; no presidente de la República ni superior de la Francia Libre. Agosto1944 es el final territorial de la ventana; falta cotejo del día del traslado forzado. Precisión mensual declarada. |
| De Gaulle, Q2042 | Francia Libre desde18/6/1940; CFLN desde1943 y GPRF desde3/6/1944. Renuncia20/1/1946. El registro parlamentario25/8/1944 delimita otra fase territorial, no el nacimiento del GPRF. |
| Gouin, Q381187 | Presidente del Gobierno provisional,27/1–23/6/1946. Elección, aceptación y formación del gabinete tienen fechas próximas distintas; no se certifica que todas las series utilicen el mismo hito. |
| Bidault, Q312026 | Gobierno provisional24/6–15/12/1946; se elimina el título genérico incorrecto de presidente de la República. |
| Blum, Q18434 | Gobierno provisional desde16/12/1946. Jefatura del Estado hasta15/1/1947; su Gobierno continúa hasta22/1. No debe fusionarse con la presidencia de Auriol desde16/1. |

Fuentes institucionales: [Defensa francesa: Pétain](https://www.defense.gouv.fr/chemins-memoire/histoire-memoires/personnalites/personnalites-lettre-n-lettre-w/philippe-petain), [Élysée: de Gaulle](https://www.elysee.fr/charles-de-gaulle), [ficha parlamentaria de de Gaulle](https://www.assemblee-nationale.fr/gouv_parl/fiches_personnalites/DeGaulle.asp), [galería histórica de la Presidencia](https://www.presidence-de-la-republique.fr/hist/10/ang/elysee/gale.html), [ficha parlamentaria de Blum](https://www.assemblee-nationale.fr/gouv_parl/fiches_personnalites/Blum.asp).

Discrepancias conservadas: la galería presidencial antigua fecha el final de Bidault18/12, mientras la ficha parlamentaria de Blum acredita su inicio16/12. Se usa el relevo de Blum, sin presentar ambas fechas como equivalentes. Faltan los relevos completos de Laval/Darlan, la copresidencia inicial Giraud–de Gaulle del CFLN y el catálogo de todos los gabinetes franceses de entreguerras.

## España: monarquía, República y bandos

Alfonso XIII, **Q18363**, conserva su condición de rey mientras ejerce el poder hasta la transferencia del14/4/1931. El cierre inclusivo del registro es13/4. Su salida no se denomina abdicación dinástica. El [Congreso documenta la transferencia de poder y proclamación republicana](https://www.congreso.es/en/cem/vidparl1931-11), corroborada por el [Archivo General de la Administración](https://www.cultura.gob.es/en/cultura/areas/archivos/mc/archivos/aga/actividades-y-exposiciones/destacados/90-aniversario-re.html).

Niceto Alcalá-Zamora, **Q313785**, tiene cargos separados: Gobierno provisional14/4–14/10/1931 y presidencia constitucional desde la elección10/12/1931 hasta destitución7/4/1936. El [archivo del Congreso](https://www.congreso.es/es/historico-diputados?_historicodiputados_mvcRenderCommandName=mostrarDetalle&_historicodiputados_nume=51194&p_p_id=historicodiputados&p_p_lifecycle=0&p_p_state=normal) acredita la jefatura provisional; la [Gaceta11/12/1931](https://www.boe.es/gazeta/dias/1931/12/11/pdfs/GMD-1931-345.pdf) y la [Gaceta8/4/1936](https://www.boe.es/gazeta/dias/1936/04/08/pdfs/GMD-1936-99.pdf) documentan elección/destitución. La jura11/12 es distinta de la elección10/12. No se rellena el intervalo de Martínez Barrio con una extensión de Alcalá-Zamora.

Azaña, **Q203708**, se copia a ESP y a la ficha republicana con su presidencia desde11/5/1936. Se conserva27/2/1939 como firma de su dimisión, dejando explícito que aceptación3/3 y salida de España5/2 no son el mismo hecho. La [Biblioteca Nacional](https://www.bne.es/es/autores/azana-manuel) acredita la presidencia y la dimisión de1939; el detalle jurídico diario continúa pendiente de acta. Largo Caballero/Negrín y Franco en el bando sublevado conservan las curaciones anteriores. La [ley de1/10/1936 publicada2/10](https://www.boe.es/gazeta/dias/1936/10/02/pdfs/BOE-1936-1.pdf) acredita el ejercicio de la jefatura franquista en su propio ámbito. Se suprime la proyección de Franco sobre ESP general antes de abril1939, manteniendo ESP-NATIONALIST.

Pendientes: todos los presidentes del Consejo de1931–1936, interinatos y Junta de Defensa Nacional anterior a Franco. Los frentes anuales no se convierten en límites diarios por estas fichas.

## China: República, autoridad militar y transición de1949

`ROC` utiliza **Q13426199**, entidad histórica distinta de la RPC(Q148) y del identificador territorial actual de Taiwán(Q865). Se conserva y copia la serie Beiyang adquirida en TWN, sin asumir que su cobertura equivalga a control efectivo uniforme del territorio.

Lin Sen, **Q705872**, es la jefatura formal1931–1/8/1943. [Correos de la República de China](https://subservices.post.gov.tw/post/internet/W_stamphouse/index_en.jsp?ID=2807&file_name=B110&stamp_cat_standard=Commemorative+Stamps&type=2805) acredita elección en1931 y muerte1/8/1943. El día inicial15/12 procede de la serie estructurada; se declara precisión anual y pendiente de acta.

Chiang Kai-shek, **Q16574**, no sustituye a Lin Sen como jefe formal durante toda su autoridad militar. El [despacho diplomático contemporáneo de19/10/1943, FRUS](https://history.state.gov/historicaldocuments/frus1943China/d288) describe su juramento como presidente del Gobierno Nacional **10/10/1943**. El tramo agosto–octubre se separa como ejercicio interino, con inicio documental pendiente de decreto. La presidencia constitucional comienza20/5/1948; [la Presidencia de la ROC](https://english.president.gov.tw/Page/83) documenta su retirada21/1/1949 y reanudación1/3/1950.

Li Zongren, **Q20297**, actúa desde21/1/1949 según [Presidencia de la ROC](https://english.president.gov.tw/Page/82) y [FRUS1949](https://history.state.gov/historicaldocuments/frus1949v09/d646). El cierre1949 es cobertura. Mao, **Q5816**, recibe el título preciso de presidente del Gobierno Popular Central desde1/10/1949, acreditado por la [Oficina de Información del Consejo de Estado](https://english.scio.gov.cn/featured/chinakeywords/2022-07/13/content_78321957.htm). No se retrotrae a1949 el título presidencial de la Constitución de1954. La dirección del partido y Zhou Enlai conservan registros propios.

Pendientes: gobiernos rivales regionales, Manchukuo, Wang Jingwei, periodización de Yan'an y autoridades provinciales. El paso ROC→RPC en la vista continental no afirma que el1/10 cesara toda autoridad de la ROC en el continente ni su continuidad en Taiwán.

## Rusia soviética y URSS

`RSR` utiliza **Q2184** para la RSFSR anterior a la unión; no se usan dirigentes de la Federación Rusa contemporánea en1920–1921. Lenin, **Q1394**, tiene una ventana documental de jefatura del Gobierno ruso1920–29/12/1922, sin afirmar cese personal al día siguiente. El [índice de documentos históricos rusos](https://docs.historyrussia.org/ru/indexes/values/973636) identifica su cargo en documentos de1920–1921; la [Biblioteca Presidencial conserva material institucional adicional](https://www.prlib.ru/item/694622). El [tratado primario30/12/1922 reproducido por la Universidad de Illinois](https://seventeenmoments.web.illinois.edu/1921-2/transcaucasia/transcaucasia-texts/formation-of-the-ussr/) acredita la formación de la Unión.

El Gobierno federal de Lenin se separa desde6/7/1923; no se convierte la firma del tratado en nombramiento automático de todos los cargos federales. Ese día concreto se conserva de [Wikidata Q1394](https://www.wikidata.org/wiki/Q1394), **pendiente del acta original de constitución del Consejo**. La fecha de ratificación constitucional de julio consta en la [reproducción contemporánea del Congressional Record](https://www.congress.gov/68/crecb/1923/12/13/GPO-CRECB-1924-pt1-v65-8.pdf), pero ratificar Constitución no demuestra por sí solo el nombramiento personal.

Kalinin, Rýkov, Mólotov y Stalin conservan la adquisición existente; no se considera validada por esta investigación toda su cronología. Stalin como secretario del partido antes de1922 no es una presidencia de la URSS inexistente. Faltan autoridades antisoviéticas y repúblicas de la guerra civil rusa.

## Japón

La [Oficina del Primer Ministro](https://japan.kantei.go.jp/past_cabinet/index.html) da la serie de gabinetes, incluidos Hara, Takahashi, los Katō, Konoe, Tōjō18/10/1941–22/7/1944, Koiso, Suzuki7/4–17/8/1945, Higashikuni, Shidehara y Yoshida. Los extremos de esa fuente coinciden con los gabinetes ya adquiridos; se conserva la serie y sólo se añaden curaciones focales Tōjō/Suzuki. No se afirma contraste de todas las suplencias breves entre gabinetes.

Taishō, **Q157052**, sigue siendo emperador hasta25/12/1926, y Hirohito, **Q34479**, accede ese día. [Historia oficial de la Gaceta japonesa](https://www.npb.go.jp/en/products/gazette/books/kanpo_history.html) y [Museo del Emperador Shōwa](https://f-showa.or.jp/museum/about_emperor_showa/) distinguen cambio de era/acceso1926 y ceremonia1928. La regencia de Hirohito desde1921 y la ocupación aliada desde1945 son funciones distintas; no se presenta a un primer ministro como emperador o comandante supremo de ocupación.

## Italia y Yugoslavia monárquicas

Víctor Manuel III, **Q150642**, continúa como rey después de25/7/1943 y abdica9/5/1946 según [archivo del Istituto Superiore di Sanità](https://arch.iss.it/detail/IT-ISS-EACCPF0001-000033/vittorio-emanuele-iii-savoia). Humberto, **Q187149**, es lugarteniente desde5/6/1944 según [Senado](https://www.senato.it/node/85466/printable/print), y rey desde9/5/1946. Se utiliza12/6 como último día anterior al ejercicio de De Gasperi desde13/6; el [archivo del Quirinal](https://archivio.quirinale.it/aspr/redazione/la-storia-e-le-funzioni) distingue ese ejercicio de los resultados definitivos18/6.

Mussolini, **Q23559**, constituye Gobierno31/10/1922 según [Senado](https://www.senato.it/legislature/regno/italia/26/resoconti-volumi-e-indici) y su [telegrama diplomático de ese día](https://www.farnesina.ipzs.it/series/SETTIMA%20SERIE/volumi/VOLUME%20%20I/full). Badoglio, **Q200085**, es nombrado25/7/1943, mientras sus ministros se nombran26/7, distinción explícita del [inventario de los Archivos del Estado](https://archiviodistatotorino.beniculturali.it/pdf/Governo_alte-cariche_ecc_Sussidi_2a.pdf). Bonomi forma gabinete18/6/1944. No se atribuye al Reino control del norte ocupado ni se extiende a toda Italia la posterior República Social de Mussolini.

De Nicola, **Q1245**, toma posesión1/7/1946 como jefe provisional; cambia al título de presidente1/1/1948 según [el Quirinal](https://presidenti.quirinale.it/page/1/den-elezione.html). Sigue pendiente separar la dimisión/reelección de25–26/6/1947 en mandatos diarios independientes.

`YKM` utiliza **Q191077** como clave de la monarquía; la denominación previa1920–1929 era Reino de los serbios, croatas y eslovenos(Q15102440), no Yugoslavia socialista. [Museo de Yugoslavia](https://muzej-jugoslavije.org/en/biography-of-king-alexander-i-karadjordjevic/) acredita sucesión de Pedro I, **Q211827**, a Alejandro I, **Q207384**,16/8/1921 y asesinato9/10/1934. Pedro II, **Q223183**, es menor bajo regencia y está en el exilio desde abril1941. [Fundación Real](https://kraljevskafondacija.rs/en/dynasty/his-majesty-king-peter-ii/) y [Casa Real: Pablo Q313128](https://royalfamily.org/hrh-prince-paul-of-yugoslavia-regent-3/) acreditan las funciones del consejo de tres regentes y el golpe27/3/1941. La Casa Real también conserva pretensiones dinásticas posteriores: no se toman como ejercicio efectivo. El límite1944 es cobertura de la ficha, no abdicación; la transición Tito–Šubašić y el consejo de regencia de1945 siguen pendientes.

## Alemania ocupada1945–1949

Se incorporan órganos documentales sin retrato individual. La [declaración5/6/1945 reproducida en documentación de la ONU](https://digitallibrary.un.org/record/669294/files/E_CN.4_W.19-EN.pdf?ln=en) afirma autoridad suprema aliada y niega que su asunción implique anexión. La ficha occidental agrupada DEU no equivale a una cuarta zona ni a gobierno nacional alemán. La [bpb](https://www.bpb.de/shop/zeitschriften/izpb/deutschland-1945-1949-259/10048/errichtung-der-besatzungsherrschaft/) explica Consejo de Control y paralización desde marzo1948. Se usa el nombre plural de administraciones de ocupación para evitar inventar un Consejo operativo hasta1949.

La SMAD oriental comienza9/6/1945, acreditada por la [Oficina de Monumentos de Berlín, con referencia a su orden1](https://www.berlin.de/landesdenkmalamt/denkmale/highlight-denkmale-der-alliierten/udssr/mitte/dienststelle-der-smad-648085.php). Su registro DDR termina documentalmente antes de la fundación de la RDA7/10/1949; no se afirma que la SMAD cesara precisamente6/10. La [colección OMGUS de Truman Library](https://www.trumanlibrary.gov/library/federal-record/records-u-s-occupation-headquarters-world-war-ii-office-military-government) acredita transición occidental a Alta Comisión21/9/1949. Esa misma sinopsis llama a21/9 fecha de establecimiento de la RFA, simplificación que **no se adopta**: el [Bundestag acredita el23/5 para la Ley Fundamental](https://www.bundestag.de/dokumente/textarchiv/2019/kw15-kalenderblatt-besatzungsstatut-633996).

Pendientes: mandos sucesivos de cada zona, cuatro zonas y sectores de Berlín con geometría propia, Dönitz/Flensburg, Sarre y distinción completa entre soberanía estatal y poderes reservados después de1949.

## Independencias, dominios y Mandato de Palestina

- India: Mountbatten, **Q157068**, gobernador general del dominio15/8/1947–20/6/1948, distinto del virrey previo; [Parlamento británico](https://www.parliament.uk/about/living-heritage/evolutionofparliament/legislativescrutiny/parliament-and-empire/collections1/collections2/mountbatten-the-last-viceroy/). Rajagopalachari, **Q378404**, jura21/6/1948, confirmado por [carta contemporánea de Nehru](https://nehruarchive.in/documents/to-lord-mountbatten-21-june-1948-nd5yl). La presidencia republicana no comienza hasta1950. Nehru, **Q1047**, conserva su jefatura del Gobierno desde15/8/1947, contrastada en [la lista de primeros ministros de India](https://www.pmindia.gov.in/en/former-prime-ministers/).
- Pakistán: Jinnah, **Q160554**, es gobernador general15/8/1947–11/9/1948 según [Asamblea Nacional](https://na.gov.pk/en/print_list.php?type=governers). [Historia parlamentaria](https://na.gov.pk/en/content.php?id=75) distingue transferencia14/8 y juramento15/8; no se confunde con primer ministro Liaquat Ali Khan(Q295713), cuyo mandato adquirido se conserva. Falta completar Nazimuddin y eventuales interinatos.
- Indonesia: Sukarno, **Q76127**, elegido18/8/1945, al día siguiente de la proclamación, según [Archivos Nacionales de Indonesia](https://www.anri.go.id/publikasi/berita/menelusuri-jejak-konstitusi-indonesia-melalui-pameran-arsip). La [colección del Rijksmuseum](https://www.rijksmuseum.nl/en/stories/exhibitions/revolusi/story/story-sukarno) distingue esta proclamación de la transferencia neerlandesa27/12/1949. Se elimina la atribución genérica de primer ministro a Sukarno en toda la ventana y se retira Assaat(Q4808308) de la presidencia federal de1949; no se ha revisado su ficha como república constituyente en1950. Faltan los gabinetes de Sjahrir/Hatta y el Gobierno de Emergencia durante el cautiverio de1948–1949.
- Israel: Weizmann, **Q172183**, presidente del Consejo Provisional desde16/5/1948 según [Presidencia](https://www.president.gov.il/institution/), y presidente de Israel con jura17/2/1949 según [Ministerio de Educación](https://pop.education.gov.il/tchumey_daat/moledet_hevra_ezrahut/yesodi/noseem_nilmadim/chaim-vaizman). La [Knéset fecha la elección16/2](https://main.knesset.gov.il/EN/activity/Pages/PresVotes.aspx): elección y jura se distinguen. Ben-Gurión(Q37610) conserva el Gobierno; no se extrapola esta presidencia a toda Palestina.
- Palestina: la [orden británica de revocación de1948](https://www.legislation.gov.uk/uksi/1948/1004/pdfs/uksi_19481004_en.pdf) extingue la jurisdicción mandataria15/5/1948. El [memorando contemporáneo ante la ONU](https://www.un.org/unispal/document/auto-insert-205676/) distingue mandato y soberanía. No se importan sin revisión todos los altos comisionados británicos ni se rellena1948 con un único Estado sucesor. Faltan el Gobierno de Toda Palestina y las autoridades egipcias/jordanas con ámbito preciso.

## Irlanda, Reino Unido y administración colonial

Jorge V, **Q269412**, reina hasta20/1/1936; Eduardo VIII(Q590227) y Jorge VI(Q280856) conservan sus mandatos existentes. [Parlamento británico: fechas](https://api.parliament.uk/regnal-years/reigns) y [QID oficiales](https://api.parliament.uk/regnal-years/monarchs) verifican las identidades. Se corrigen los falsos rangos genéricos1936–1940 de Chamberlain,1940–1945 de Churchill y1945–1951 de Attlee dentro de esta ventana; sus gobiernos posteriores siguen en catálogo. [GOV.UK](https://www.gov.uk/government/history/past-prime-ministers) acredita los periodos; los extremos diarios ya existentes se conservan sin certificar de nuevo todo nombramiento.

Douglas Hyde, **Q237951**, presidente25/6/1938–24/6/1945 según [Presidencia de Irlanda](https://president.ie/en/the-president/douglas-hyde); [Oireachtas](https://www.oireachtas.ie/en/visit-and-learn/history-and-buildings/history-of-parliament-in-ireland/) separa Constitución1937, presidencia1938 y República1949. La serie Cosgrave/de Valera y la relación exterior con la Corona requieren su propio contexto; no llamar a Cosgrave taoiseach de1922 cuando su título era presidente del Consejo Ejecutivo, explicado por [el Gobierno irlandés](https://www.gov.ie/en/department-of-the-taoiseach/publications/former-taoisigh/).

La ampliación de relaciones coloniales debe mostrar jefaturas metropolitanas con ámbito externo rotulado, sin inventar gobernadores locales. Las fichas de India/Pakistán distinguen expresamente la Corona del gobernador general. Faltan series completas de gobernadores, monarquías locales y regencias de África/Asia, además de monarquías Yemen/Nepal/Afganistán; esta investigación focal no las declara resueltas por haber cubierto un año con la metrópoli.

## Identificadores y comprobaciones pendientes de integración

Los QID humanos incorporados se cotejaron por búsqueda de entidades y/o `Special:EntityData/Q….json`, verificando etiqueta y P31=Q5; Blum se corrigió aQ18434 tras descartar un identificador no humano. Las nuevas entidades RSR=Q2184, ROC=Q13426199 y YKM=Q191077 fueron contrastadas de la misma manera; sus clases son de entidad histórica, no Q5. Identificar a una persona no demuestra su mandato ni licencia de retrato. No se ha adivinado ningún QID definitivo a partir del nombre.

Integración necesaria: ejecutar después de la adquisición global, comprobar repeticiones sobre copia, revisar las colas de1950+, consolidación por persona/cargo en el resolver, fotografías conservadas y rutas históricas ROC/RSR/YKM/ESP-REPUBLIC/ocupaciones. Actualizar inventario general y auditoría con resultados efectivos; no convertir esta lista de fuentes en una afirmación de exactitud exhaustiva.

## Seguimiento0.11: Estonia, Irlanda y Mongolia

Segundo preparador independiente: `scripts/curate-1920-europe-asia.py`, etiqueta `curated-1920-europe-asia-0.11`, función `curate(data)` y CLI `--input`/`--output`. Incorpora30 registros:18 estonios,7 irlandeses y5 ventanas mongolas. Conserva retratos antes de regenerar su etiqueta y sólo reemplaza la intersección de cada persona con el intervalo revisado; los cargos de otras personas y las décadas de1950 en adelante permanecen intactos. No modifica el preparador focal anterior, símbolos ni manifiestos. Las comprobaciones aisladas y la aplicación efectiva se distinguen en la documentación de entrega principal.

Comprobación de este seguimiento: sintaxis correcta, dos aplicaciones en memoria idénticas,30 registros generados y todos los registros originales con ejercicio desde1950 comparados campo por campo sin cambios. Se trabajó sobre copias en memoria; no se escribió `public/data` ni salida temporal de identidades.

### Estonia:18 cargos con fechas diarias institucionales

La [Presidencia estonia](https://president.ee/eesti-riigipeade-loetelu) ofrece, **debajo del resumen anual**, todos los extremos diarios de1920–1938 y la base constitucional de cada título. No es necesario fabricar ventanas anuales para cubrir1921–1937. Los dieciséis periodos de `riigivanem` se conservan separados, incluidas las vueltas de Päts, Teemant y Tõnisson. Se convierte cada fecha de relevo en último día inclusivo anterior; no se identifica un cambio de título con una muerte o retirada de la persona.

| Función | Identificación |
| --- | --- |
| Riigivanem: jefatura del Estado y del Gobierno bajo la Constitución de1920 | Ants Piip(Q887682), Konstantin Päts(Q299114), Juhan Kukk(Q887260), Friedrich Karl Akel(Q571670), Jüri Jaakson(Q887247), Jaan Teemant(Q887238), Jaan Tõnisson(Q710956), August Rei(Q725322), Otto Strandman(Q887019), Kaarel Eenpalu(Q126704). |
| Primer ministro en funciones de riigivanem | Päts24/1/1934–2/9/1937; se documentan reforma constitucional y estado de excepción de marzo1934. |
| Riigihoidja: regente del Estado | Päts3/9/1937–23/4/1938; la presidencia de la República comienza24/4/1938 y conserva su registro posterior. |

QID contrastados mediante búsqueda/EntityData y P31=Q5; Eenpalu se corroboró en el EntityData local adquirido. Las autoridades estonias en el exilio de1940–1992 y la ocupación soviética son funciones/ámbitos distintos y no se recortan para rellenar el periodo de entreguerras.

### Irlanda: sistema dual de1922 y título anterior a Taoiseach

El [Archivo Nacional](https://www.nationalarchives.ie/wp-content/uploads/2021/09/2021-Commemoration-Programme-as-part-of-the-Decade-of-Centenaries-2012-2023-EN-REDUX.pdf) acredita la elección de de Valera como presidente de Dáil Éireann1/4/1919. La nueva ventana comienza1921 por alcance documental, sin nombramiento ficticio1/1.

La [historia institucional del Segundo Dáil](https://www.gov.ie/en/department-of-the-taoiseach/publications/second-d%C3%A1il/) distingue a de Valera como presidente republicano26/8/1921–9/1/1922, Griffith como presidente del Dáil10/1–12/8/1922, y Collins como presidente del Gobierno Provisional desde16/1 hasta su muerte22/8. **Constitución del órgano14/1, posesión16/1 y transferencia de funciones1/4 son hitos distintos.** El nuevo preparador conserva Griffith/Collins simultáneamente y explica sus ámbitos; no los convierte en titulares consecutivos de un mismo cargo.

La misma fuente acredita la fusión del sistema dual bajo Cosgrave9/9 y la sustitución del Gobierno Provisional por el Consejo Ejecutivo6/12/1922. El [Sexto Dáil](https://www.gov.ie/en/department-of-the-taoiseach/publications/sixth-d%C3%A1il/) documenta la continuidad del cuarto/quinto Consejo hasta9/3/1932; el mandato continuo de Cosgrave no afirma que no hubiera renovaciones ministeriales. El [Séptimo Dáil](https://www.gov.ie/en/department-of-the-taoiseach/publications/seventh-d%C3%A1il/) acredita el nuevo Consejo de de Valera9/3/1932, el [Octavo](https://www.gov.ie/en/department-of-the-taoiseach/publications/eighth-d%C3%A1il/) su continuidad1933–1937 y el [Noveno](https://www.gov.ie/en/department-of-the-taoiseach/publications/ninth-d%C3%A1il/) el cambio de título a Taoiseach **29/12/1937 sin sustitución del personal del Gobierno**.

Identificaciones verificadas: Éamon de ValeraQ173347, Arthur GriffithQ342765, Michael CollinsQ173196 y W. T. CosgraveQ465770. La autoridad republicana antes de diciembre1922 no acredita que el Reino Unido hubiera reconocido toda la soberanía reclamada. Pendientes: interinato de agosto–septiembre1922, todos los gobernadores generales y separación de cada renovación del Consejo Ejecutivo. Se mantiene la distinción con la presidencia constitucional de Hyde desde1938.

### Mongolia:5 ventanas, sin días de investidura inventados

Se utilizan fuentes institucionales o investigación histórica identificada, conservando precisión anual9 y ambos indicadores de límite de cobertura. No se convierten los1 de enero o31 de diciembre en nombramientos o ceses. Los extremos interiores reducen la necesidad de reconstruir transiciones diarias no contrastadas.

| Persona | Ventana incorporada | Evidencia y límite |
| --- | --- | --- |
| Bogd Khan,Q353547 |1923 | El [Instituto Jurídico Nacional](https://nli.gov.mn/wp-content/uploads/2023/09/SE.2021.7.pdf) distingue el sistema dual limitado de1921 y su fallecimiento en1924. Se documenta sólo1923, sin adoptar las fechas de muerte contradictorias de compilaciones secundarias. |
| Balingiin Tserendorj,Q2672415 |1924–1927 | [Mongoltoli, biografía histórica](https://www.mongoltoli.mn/history/h/693), acredita ejercicio1923–1928. Se eligen años interiores; no se inventa día de nombramiento1923 ni se prolonga sobre su muerte de1928. |
| Anandyn Amar/Agdanbuugyn Amar,Q45281 |Cierres de1928–1929 | [Mongoltoli](https://www.mongoltoli.mn/history/h/713) acredita primer Gobierno1928–1930. El intervalo comienza31/12/1928, señal de cobertura al cierre, para evitar atribuirle todo el año de su nombramiento sin fecha primaria diaria. |
| Tsengeltiin Jigjidjav,Q2353321 |Cierres de1930–1931 | [Catálogo de la Universidad Nacional de Mongolia](https://catalog.num.edu.mn/cgi-bin/koha/opac-detail.pl?biblionumber=23185), monografía biográfica de Z. Lonjid, acredita1930–1932. Se empieza31/12/1930 y no se amplía hasta diciembre1932 sobre Genden. |
| Amar,Q45281 |1937–1938 | La misma biografía acredita segundo Gobierno1936–1939. Ventana interior, sin asignar día de detención o relevo en1939. |

Los cuatro QID se verificaron con EntityData, etiqueta y P31=Q5. El apellido/patronímico alternativo de Amar identifica a la misma persona. El catálogo universitario ofrece una descripción bibliográfica, no el acta original del nombramiento: la fuente y la precisión se declaran como tales. Tserendorj y Amar proceden de síntesis historiográficas con bibliografía, no de actas ministeriales diarias.

Siguen pendientes Damdinbazar y transición gubernamental de1923, las jefaturas formales republicanas completas, regencias/limitaciones reales y todos los relevos diarios. El registro del monarca en1923 y las ventanas posteriores resuelven consultas anuales focales; no certifican la totalidad de la administración mongola ni sus relaciones con China/URSS.


## Integración en0.11.0

Aplicado al catálogo público local por el responsable de integración el24/10/2026, después de comprobar la repetibilidad y conservar los retratos. El estado «no aplicado» de la preparación aislada describe el relevo inicial, no la entrega final. Resultados efectivos, adquisición de medios y límites conjuntos en [DELIVERY-0.11.0](DELIVERY-0.11.0.md) y [REVIEW-1920-1949.json](REVIEW-1920-1949.json). Publicación pendiente del aviso del propietario.
