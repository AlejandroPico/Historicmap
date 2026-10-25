# Correcciones de retratos · 0.13

Investigación acotada realizada el 25/10/2026. No se han modificado el catálogo público, los manifiestos de medios, la aplicación ni Git. Los candidatos exactos están en `scripts/media-corrections-013.json`; el proceso único de integración debe adquirirlos, conservar sus licencias y comprobarlos visualmente antes de asignarlos por identificador de persona a todos sus mandatos.

## Hallazgo principal: Irak y la adquisición automática

La fotografía claramente ajena está en **Ali Falih al-Zaidi, Q139573306**, jefe del Gobierno. El catálogo le asigna `Pope Trump AI by Donald Trump.png`: es una imagen generada de otra persona. Debe eliminarse de todas las apariciones de este identificador y quedar expresamente excluida de futuras adquisiciones. En la consulta directa de Wikidata de esta fecha el elemento todavía tiene P31=Q5, pero P18 contiene ese archivo y la etiqueta inglesa está sustituida por una frase árabe insultante. **Comprobar P31=humano no basta para validar un retrato ni una etiqueta.** Se debe exigir además correspondencia entre el sujeto descrito, la procedencia de la foto y el personaje consultado.

Candidato: **`2026 Ali al-Zaidi (cropped).jpg`**, 781 × 1040, foto oficial de la Fuerza Aérea estadounidense tomada por Eugene Oliver en el Pentágono el 14/7/2026. Commons la identifica como fotografía oficial estadounidense en dominio público. Original individual ya extraído por Commons, sin transformación realizada por este trabajo. Se descargó intacto a `.cache/media-013/ali.jpg` y se comprobó visualmente: retrato real de la persona, sin otros protagonistas ni elementos generados. [Ficha de Commons y fuente original enlazada](https://commons.wikimedia.org/wiki/File:2026_Ali_al-Zaidi_(cropped).jpg).

La comprobación institucional del cargo aporta una corrección temporal independiente: el Parlamento otorga confianza y recibe el juramento del Gobierno el **14/5/2026**; el 27/4 sólo se había producido la nominación política. [Parlamento, 14 de mayo](https://iq.parliament.iq/en/2026/05/14/council-of-representatives-votes-on-the-ministerial-curriculum-and-grants-confidence-to-the-government-of-mr-ali-al-zaydi/), [agencia estatal INA, nominación de abril](https://ina.iq/en/politics/48179-coordination-framework-nominates-ali-al-zaidi-as-prime-minister.html). La entrega ceremonial de responsabilidades se celebra el 16/5; no debe confundirse con el voto y juramento del día14. [INA, entrega de responsabilidades](https://ina.iq/ar/political/263396-.html).

El jefe del Estado es **Nizar Amidi, Q115579547**, elegido en abril de2026. La foto actual `نزار آميدي 2026.jpg` no es la imagen generada anterior; se inspeccionó el archivo local y corresponde a la persona identificada en ese registro. No se propone cambiarla por otra persona. Sí hay una fila errónea de su mandato que comienza **17/10/2022**, junto a otra curada que comienza en abril2026: la primera no debe seguir mostrando que era presidente en2022. El Parlamento documenta la elección el **11/4/2026**; para distinguir día de elección y asunción formal hay que conservar la referencia propia de cada acto y no elegir una fecha por aproximación. [Parlamento, elección de Nizar Amidi](https://iq.parliament.iq/en/2026/04/11/first-deputy-speaker-congratulates-mr-nizar-amidi-on-winning-the-confidence-of-the-council-of-representatives-and-his-election-as-president-of-the-republic/).

## Candidatos comprobados por metadatos

Todos los identificadores de esta tabla se consultaron directamente y tenían P31=Q5. Los archivos se resolvieron por su título exacto mediante la API de Commons; dimensiones, autor, licencia, fecha y URL original están preservados en el JSON. La existencia en Commons es procedencia verificable, no una validación automática de todas las afirmaciones de la ficha.

| País y persona | Archivo exacto | Tamaño | Procedencia y licencia |
| --- | --- | --- | --- |
| Tayikistán · Kokhir Rasulzoda Q15222839 | `Kokhir Rasulzoda (29-04-2021) (cropped).jpg` | 762 × 1040 | Mikhail Frolov / Presidencia de Tartaristán; CC BY4.0, atribución Tatarstan.ru. |
| Bután · Jigme Dorji Wangchuck Q298020 | `Jigme Dorje Wangchuck portrait (cropped).jpg` | 1158 × 1642 | Benjamin Goetzinger, fotografía de un retrato expuesto en el aeropuerto, 16/2/2013; Commons declara CC BY-SA4.0. No es una foto tomada al rey en2013. |
| Bangladesh · Abdul Hamid Q3246667 | `Abdul Hamid - 2014 (cropped).jpg` | 378 × 505 | Oficina del Primer Ministro de India; GODL-India. Encuentro oficial de19/12/2014. |
| Vietnam · Trần Đại Quang Q7833292 | `Mr. Tran Dai Quang.jpg` | 292 × 421 | Oficina del Primer Ministro de India; GODL-India. Fotografía de3/3/2018. |
| India · Manmohan Singh Q41914 | `Official Portrait of the Prime Minister Dr. Manmohan Singh.jpg` | 600 × 900 | Retrato oficial PMO, 21/7/2004; GODL-India. |
| India · Pratibha Patil Q47854 | `The President of India, Smt. Pratibha Patil.jpg` | 1500 × 2100 | Secretaría de la Presidencia, 8/8/2007; GODL-India. |
| Nepal · Ram Baran Yadav Q57441 | `Ram Baran Yadav, portrait (August 2014).jpg` | 569 × 767 | Oficina del Primer Ministro de India, 4/8/2014; GODL-India. |
| Nepal · K. P. Sharma Oli Q3195923 | `The Prime Minister of Nepal, Mr. K.P. Sharma Oli calls on the Prime Minister, Shri Narendra Modi, in New Delhi on April 06, 2018 (cropped).jpg` | 316 × 425 | PMO India, 6/4/2018; GODL-India. |
| Nepal · Sher Bahadur Deuba Q470903 | `Prime Minister of Nepal, Shri Sher Bahadur Deuba, in Glasgow, Scotland on November 02, 2021 (1).jpg` | 657 × 922 | PMO India, 2/11/2021; GODL-India. |
| Nepal · Sushil Koirala Q422969 | `The Prime Minister of Nepal, Mr. Sushil Koirala, on the sidelines of the third Summit of the Bay of Bengal Initiative for Multi-Sectoral Technical and Economic Cooperation (BIMSTEC), at Nay Pyi Taw.jpg` | 788 × 1051 | PMO India, 3/3/2014; GODL-India. |
| Nepal · Kirti Nidhi Bista Q2267879 | `Prime Minister Kirti Nidhi Bista (cropped).png` | 992 × 1324 | Fotografía de1972, fundación Chitrakar / British Library EAP838-1-8-68-1; Commons declara PD-Nepal. |
| Nepal · Nagendra Prasad Rijal Q767596 | `Nagendra Prasad Rijal.jpg` | 526 × 1140 | Candidato atribuido por Commons a la Oficina del Primer Ministro; PD-Nepal declarado, fuente original exacta aún sin enlace verificable. **No aprobado para adquisición automática**. |

### Tayikistán

El archivo de2021 mejora la resolución y el encuadre respecto a `Kokhir Rasulzoda.jpg`. Identifica al primer ministro en un encuentro con Rustam Minnikhanov y acredita al fotógrafo y a la institución. La licencia y la atribución figuran expresamente en la [ficha de Commons](https://commons.wikimedia.org/wiki/File:Kokhir_Rasulzoda_(29-04-2021)_(cropped).jpg). Su cargo en2026 se contrastó mediante el [Ministerio de Exteriores chino, encuentro de18/10/2026](https://www.mfa.gov.cn/mfa_eng/xw/zyxw/202610/t20261019_12043176.html). No se presupone vigencia porque un mandato genérico no tenga fecha de fin.

### Bután

El candidato evita el billete de50 ngultrum. Se descargó intacto a `.cache/media-013/bhutan.jpg` y se inspeccionó: es la reproducción de un retrato individual del tercer rey. La fecha de2013 pertenece a la fotografía de la representación expuesta. La licencia declarada por el fotógrafo y los derechos de la obra fotografiada son planos distintos; mantener la descripción de procedencia y no llamarla fotografía oficial contemporánea a1970.

Otra opción identificada fue `Jigme Dorji Wangchuck Maharaja of Bhutan at the International Lowcost Housing Exhibition.jpg`, fotografía gubernamental de1954, pero sólo tiene116 ×281 píxeles, fue retocada y su página advierte sobre derechos restaurados en Estados Unidos. Se descarta como mejora principal. El [Parlamento de Bután, actas históricas de la36.ª sesión](https://parliament.bt/uploads/topics/17017666386759.pdf) identifica a Jigme Dorji como tercer rey entronizado en1952.

### Bangladesh, Vietnam e India

El retrato de Abdul Hamid tiene sujeto explícito tanto en la descripción de la PMO como en P180 de los datos estructurados. No es el homónimo Maulvi Shah Abdul Hamid. Una [publicación del Ministerio de Exteriores de Bangladesh](https://file.mofa.gov.bd/uploads/fc62c7e3-a682-44ed-bb28-99e741c6cd53/639/52a/fdd/63952afdd3fd6124877543.pdf) también identifica su imagen y cargo. [Archivo exacto de2014](https://commons.wikimedia.org/wiki/File:Abdul_Hamid_-_2014_(cropped).jpg).

Vietnam2016 debe incluir a Trần Đại Quang desde **2/4/2016**; la [biografía necrológica del Gobierno vietnamita](https://en.baochinhphu.vn/state-president-tran-dai-quang-passes-away-11133211.htm) confirma la elección y su fallecimiento21/9/2018. El catálogo contiene además una fila de Trương Tấn Sang hasta25/7/2016 que se solapa indebidamente con la sucesión de abril; no basta añadir la foto sin revisar esa frontera temporal. La foto propuesta es de2018 y debe conservar esa fecha en la información de la imagen.

India2011: Manmohan Singh y Pratibha Patil están correctamente identificados; sus fotografías faltan en el catálogo, también en algunas filas duplicadas de Singh. Una sola asignación por persona debe actualizar todos sus mandatos. La [oficina del primer ministro](https://www.pmindia.gov.in/en/former-prime-ministers/) acredita el mandato de Singh22/5/2004–26/5/2014; la [Presidencia de India](https://origin250422-presidentofindia.nic.in/smt-pratibha-devisingh-patil-profile) el de Patil25/7/2007–25/7/2012. Los dos candidatos son retratos oficiales dentro de sus mandatos.

### Nepal

El inventario de trabajo presenta exactamente seis personas sin retrato: Bista, Rijal, Deuba, Yadav, Sushil Koirala y Oli. No se confunden con personas que sí tienen una imagen pero cuyo mandato requiere corrección.

La [lista institucional de primeros ministros](https://opmcm.gov.np/pages/former-prime-ministers/) se descargó correctamente por acceso HTTP, aunque el lector web devolvía timeout. Enumera los nombres nepaleses y sus periodos en Bikram Sambat. La página enlazada antigua `/former-pm/` devuelve404; no se utiliza como demostración de la procedencia fotográfica de Rijal.

La [Presidencia de Nepal](https://president.gov.np/former-presidents/) confirma Ram Baran Yadav23/7/2008–28/10/2015. Las fotos de los encuentros de India tienen sujeto y cargo en los pies originales, y fechas conservadas. Una foto de Deuba2021 puede representar al mismo personaje en1995, pero no se debe presentar como imagen tomada en1995.

Bista tiene un candidato Commons nuevo de2026 basado en un original de1972; la ficha enlaza [British Library EAP](https://eap.bl.uk/item/EAP838-1-8-68-1), que no devolvió contenido legible durante esta revisión. Rijal dispone de una imagen que declara a la Oficina del Primer Ministro como fuente sin URL original, fecha1960s y autor desconocido: queda marcada `needs-provenance-verification` en el JSON. No se eleva esa descripción del subidor a prueba institucional independiente.

## Mozambique: comprobación visual de las dos autoridades

Se revisaron directamente los dos archivos públicos actuales, no sólo sus nombres o P18:

- **Daniel Chapo, Q97058466**, jefe del Estado: `media/portrait-5645a4bfd4de99439e01.jpg` muestra únicamente a Chapo. El original exacto es **`Daniel Chapo on November 24, 2025 (cropped).jpg`**,836 ×1080. La procedencia es la Presidencia de Brasil, fotografía de **Ricardo Stuckert / PR**, distribuida en la cuenta Lula Oficial bajo **CC BY-SA4.0**. Se consultaron los metadatos actuales de Commons y se verificó P31=Q5. El archivo ya presente es un retrato individual válido; se añadió al JSON con `status=verified-existing-individual-portrait`, `existingFile` y `visualVerified=true` para evitar sustituirlo innecesariamente. [Ficha exacta](https://commons.wikimedia.org/wiki/File:Daniel_Chapo_on_November_24,_2025_(cropped).jpg), [publicación original de la Presidencia de Brasil](https://www.flickr.com/photos/lulaoficial/54943384281/). Su cargo vigente se contrastó en una [noticia de la Agencia Nacional de Energía Atómica de Mozambique,22/10/2026](https://anea.gov.mz/anea-participa-na-conferencia-internacional-sobre-reducao-do-risco-de-desastres-e-resiliencia-em-africa/).
- **Maria Benvinda Levi, Q6761049**, jefa del Gobierno: `media/portrait-e1b00f7214632f09df35.webp` muestra a Levi a la izquierda y a **Đuro Macut** a la derecha estrechándose la mano. Esta es la fotografía con dos personas. Las otras dos imágenes de la galería serbia también son grupales, como confirmó su inspección local. No se atribuye la escena a Chapo.

Existe además un segundo retrato ya recortado en Commons, `Daniel Chapo, November 2025.jpg`,750 ×1005, del mismo original y con la misma licencia. No aporta una ventaja sobre el archivo actual836 ×1080; por ello no se añade una sustitución redundante.

### Maria Benvinda Levi: hueco aún abierto y búsqueda realizada

Persona correcta: **Maria Benvinda Delfina Levi / Levy, Q6761049**, jefa del Gobierno. No debe confundirse con el presidente Daniel Chapo, cuya foto individual ya está disponible. P31=Q5 comprobado; Wikidata no ofrece P18. Las búsquedas en Commons por Maria Benvinda/Benvida/Levi no devolvieron una fotografía de ella. Esto no implica que no exista un retrato: también se buscaron fuentes institucionales de la UE/EEAS, ONU y cuentas de Flickr vinculadas a instituciones; no se localizó durante esta revisión un archivo individual acompañado de licencia verificable.

La [Imprensa Nacional de Moçambique, despacho62/2025 publicado17/1/2025](https://www.inm.gov.mz/pt-br/content/suplemento-n%C2%BA-1-de-170125-pag-38-1-4-br-n%C2%BA-13-boletim-da-rep%C3%BAblica-i-serie) acredita el nombramiento. Esto contradice los comienzos genéricos1/1 y15/1 del catálogo; separar nombramiento y toma de posesión de18/1, sin elegir el1/1por normalización. Su continuidad se comprobó en el [Portal del Gobierno, noticia2/10/2026](https://portaldogoverno.gov.mz/pm-exorta-novos-dirigentes-a-transformarem-desafios-em-resultados/).

La galería del [Gobierno de Serbia,31/8/2026](https://www.srbija.gov.rs/vest/en/286105/serbia-mozambique-strengthening-bilateral-relations.php) contiene tres fotos: la actual con Macut y otras dos también grupales. Se descargaron las dos alternativas intactas a `.cache/media-013/levi-117.webp` y `levi-120.webp` para comprobarlas; ninguna es un retrato individual. Todas están sujetas al aviso CC BY-NC-ND3.0RS. **No se han recortado, retocado ni propuesto como solución individual.**

Existen imágenes individuales identificables en una [publicación de UNICEF de2014, página de la entonces ministra de Justicia](https://www.unicef.org/mozambique/media/561/file/As%20nossas%20crian%C3%A7as%20em%202025%3A%20Opini%C3%A3o%20de%20l%C3%ADderes%20proeminentes%20sobre%20o%20futuro%20das%20crian%C3%A7as%20em%20Mo%C3%A7ambiqu.pdf), una [revista del Ministerio de Justicia de Timor-Leste de2014](https://www.mj.gov.tl/files/N_1_Forum_Jul2014.pdf) y las fotografías de State House Kenya21/10/2025 distribuidas con créditoPCS. Aún no se ha acreditado una licencia reutilizable del retrato individual ni un original independiente de la maqueta; no se incorporan al JSON de adquisiciones exactas. La solución pendiente requiere un retrato autorizado o licencia expresamente comprobada, no un recorte del archivo ND ni una fotografía generada.

## Entrega y límites

-14 candidatos exactos en JSON:13 con metadatos comprobados (incluido el retrato individual de Chapo ya presente) y uno Rijal pendiente de procedencia. El retrato de Bután es una reproducción de un objeto y mantiene esa advertencia.
- P31 se comprobó para las14 personas propuestas y para Nizar Amidi y Maria Benvinda Levi. P180 coincide expresamente en las fichas de Hamid, Rasulzoda, Quang, Singh, Patil, Yadav y la imagen original del rey de Bután; la ausencia de P180 en otras fichas se suplió con descripción/cargo/procedencia, no se interpreta como prueba de identidad.
- Verificación visual local realizada en Ali, Bután, Nizar actual, Daniel Chapo actual, Maria Levi actual y las dos alternativas grupales de Mozambique. Los demás candidatos requieren la verificación visual final del integrador al adquirirlos.
- No se han regenerado, editado o recortado imágenes. Sólo se guardaron originales intactos en caché para investigación. Una descarga de Rasulzoda devolvió429; no se hicieron reintentos masivos.
- No confundir la investigación terminada de candidatos con integración terminada. Mozambique y la procedencia precisa de Rijal siguen pendientes; las inconsistencias temporales de Irak, Mozambique y Vietnam deben resolverse en el curador de autoridades, fuera del ámbito de este archivo de medios.


## Integración local ·25/10/2026

Los12 candidatos iniciales con metadatos verificados se adquirieron; se revisaron visualmente los archivos finales, incluidosIndia, Vietnam, Bangladesh, Nepal, Bután, Tayikistán eIrak. ÉmileLoubet quedó integrado conLicenceOuverte y créditoBIUSanté. India suma12 personas con retrato que antes carecían de él, incluidasSingh/Patil2011, Kalam, DeveGowda yKovind; no quedan huecos fotográficos en su catálogo disponible. Nepal suma siete, incluidosRanodip/Surendra de la nueva ventana1880. Rijal continúa pendiente de procedencia, y el retrato individual deMariaLevi sigue sin licencia reutilizable acreditada. No se ha recortado su fotografíaND.

El curador independiente corrige las fechas deIrak, Levi yTrươngTấnSang. PhilBaker yDavid se retiran de las autoridades; las imágenes ajena/generada y de billete sin referencias se retiran del inventario. Las nuevas parejas exactas deIndia/Nepal se conservan enmedia-corrections-013.json para futuras adquisiciones. Comprobaciones efectivas de navegador enDELIVERY-0.13.0.
