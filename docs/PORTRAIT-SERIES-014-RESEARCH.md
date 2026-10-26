# Investigación de retratos por época y mandato · 0.14

Revisión: 25 de octubre de 2026. Este documento acompaña a [`scripts/portrait-series-014-research.json`](../scripts/portrait-series-014-research.json). Contiene candidatos y ventanas editoriales; la adquisición y la incorporación al catálogo público corresponden al proceso de integración. No acredita por sí solo que las imágenes estén publicadas en la aplicación.

## Resultado y reglas de integración

Se documentan 35 candidatos: ocho para Franco, ocho para Putin —uno alternativo—, once para Isabel II, dos para los mandatos de Trump, tres para Nguyễn Minh Triết, dos para Sharma y uno para Sadi Carnot. Todos tienen archivo exacto existente en Commons, identificador y revisión, dimensiones, atribución y condiciones de reutilización declaradas en la ficha. Tres archivos se han descargado y revisado visualmente: Carnot, el juramento de Sharma y la investidura de Franco de 1936. Los restantes todavía requieren inspección visual durante su adquisición.

Cada fotografía conserva su propia fecha. `fromYear` y `toYear` son los extremos inclusivos de una ventana editorial; no describen las fechas de posesión de un cargo. `photoDate` se mantiene aparte y puede ser desconocida. Se filtra primero la autoridad por sus fechas de mandato y después se selecciona la imagen de esa persona. Así, una serie de retratos no crea una presidencia de Putin entre 2008 y 2012 ni un mandato de Trump entre 2021 y 2024.

La propuesta sirve para fichas anuales. Cuando una toma y un nombramiento ocurren dentro del mismo año, la toma no debe presentarse como imagen de la investidura. Si la consulta pasa a tener precisión diaria, elegir la última fotografía anterior a la fecha o indicar expresamente que se trata de una imagen representativa posterior. No sustituir una fecha desconocida por el primer año de visualización ni por el año del nombre de archivo.

El JSON registra la licencia declarada por Commons, su URL cuando existe, la página y revisión verificadas, y la fuente original de su descripción. Una marca de dominio público no es una licencia Creative Commons; sus condiciones territoriales deben conservarse cuando la ficha las señale. Los dos primeros candidatos de Franco incluyen `rightsReviewRequired` por sus advertencias de derechos/procedencia. Mantener una alternativa previa si no se resuelve esa revisión.

Para extender el sistema a otros reinados, dictaduras y mandatos repetidos basta añadir ventanas a la persona correcta. No duplicar al personaje ni alterar su biografía o sus registros de cargo. Es preferible conservar una toma acreditada de calidad a cambiar automáticamente a una toma posterior mucho más pequeña.

## Ventanas propuestas

Los enlaces de archivo, las fuentes primarias y las atribuciones completas figuran en el JSON. En las tablas, «c.» significa fecha aproximada, no fecha exacta.

### Francisco Franco · Q29179

| Años de visualización | Toma documentada | Archivo exacto | Observación |
| --- | --- | --- | --- |
| 1936–1939 | c. 1932–1935 | Francisco Franco (photographic portrait) by Jalón Ángel 1930s.png | Jalón Ángel; Commons señala dominio público en España y una restricción territorial para Alemania. Revisar antes de publicar esta alternativa. |
| 1940–1949 | c. 1940 | Francisco Franco circa 1939.jpg | La descripción dice c. 1940, pese al nombre. Procedencia secundaria y autor desconocido. |
| 1950–1958 | 1950 | Francisco Franco 1950 (cropped).jpg | CC0. |
| 1959–1963 | diciembre de 1959 | Francisco Franco 1959 (cropped).jpg | NARA / Library of Congress; 201×268, resolución limitada. |
| 1964–1967 | 26-02-1964 | Generalissimo Franco, Caudillo van Spanje, Bestanddeelnr 916-0979.jpg | Anefo, CC0. |
| 1968 | 30-05-1968 | Francisco Franco 1968 (cropped).jpg | CC BY-SA 4.0. |
| 1969–1974 | 23-07-1969 | Francisco Franco July 1969 Portrait (3x4 cropped).jpg | Anefo / Nationaal Archief, CC0. |
| 1975 | 1975 | Francisco Franco 1975 (cropped).jpg | Anefo / Nationaal Archief, CC0. |

`Francisco Franco, octubre de 1936, Burgos.jpg` es una fotografía de grupo real de su investidura, revisada en `.cache/portraits014/franco-1936.jpg`. Puede ser un recurso contextual, pero el protagonista aparece de perfil y no es un buen sustituto de retrato individual sin encuadre adicional.

No usar `Retrato Francisco Franco 1964 (cropped).jpg` para fechar una toma de 1964: su descripción la sitúa probablemente en los años cuarenta. Tampoco asumir que la imagen titulada `RETRATO DEL GRAL. FRANCISCO FRANCO BAHAMONDE (1960).jpg` fue tomada en 1960: su fecha digital corresponde a una reproducción de 2017.

### Vladímir Putin · Q7747

| Años | Toma | Archivo exacto |
| --- | --- | --- |
| 1999 | 31-12-1999 | Vladimir Putin 31 December 1999-3 (cropped).jpg |
| 2000–2004 | 07-05-2000 | Vladimir Putin taking the Presidential Oath, 7 May 2000 (cropped 3x4).jpg |
| 2005–2009 | 05-05-2005 | Vladimir-Putin-(cropped).jpeg |
| 2010–2011 | 29-08-2010 | Vladimir Putin 12020.jpg |
| 2012–2019 | mayo de 2012 | Vladimir Putin - 2012.jpg |
| 2020–2023 | 20-02-2020 | Vladimir Putin (2020-02-20).jpg |
| Desde 2024 | 08-03-2024 | Владимир Путин (08-03-2024) (cropped) (higher res) 2.jpg |

La toma de 1999 corresponde al mensaje al asumir la presidencia interina, no al nombramiento como primer ministro de agosto. La de 2010 necesita revisión del encuadre por ser apaisada. La de 2020 lleva crédito TASS, publicada bajo la autorización del sitio presidencial; conservar ambos créditos. Todas declaran CC BY 4.0. El retrato alternativo `Vladimir Putin (2025-01-21) 1 (cropped).jpg` está fechado, pero sólo tiene 307×376 frente a 1559×2078 del de 2024.

### Isabel II · Q9682

Se ofrecen más ventanas para cubrir sus siete décadas de reinado sin un salto de quince años entre imágenes. Las de 1958, 1977 y 1999 pueden integrarse por etapas, conservando su procedencia.

| Años | Toma | Archivo exacto | Condición |
| --- | --- | --- | --- |
| 1952–1958 | 1951 | Elizabeth II and Philip (cropped).jpg | Studio of Baron, CC BY 2.0. El recorte es individual. |
| 1959–1962 | diciembre de 1958 | Queen Elizabeth II official portrait for 1959 tour (retouched) (cropped) (3-to-4 aspect ratio).jpg | Donald McKague, dominio público; 1959 es el año de la gira. |
| 1963–1969 | 1963 | Queen Elizabeth II 1963.jpg | Archives New Zealand, CC BY 2.0. |
| 1970–1976 | 1970 | Elizabeth II in Queensland, Australia, 1970.jpg | Queensland State Archives, CC BY 3.0 au; revisar encuadre. |
| 1977–1981 | 28-02-1977 | Queen Elizabeth II 1977 (cropped).jpg | Archives New Zealand, CC BY 2.0. |
| 1982–1991 | 08-06-1982 | President Ronald Reagan, Queen Elizabeth II, Nancy Reagan, and Prince Philip (cropped).jpg | NARA, dominio público; comprobar el recorte individual al adquirirlo. |
| 1992–1998 | 19-10-1992 | Queen Elizabeth II State Visit to Germany, 1992.jpg | Marie-Josefine Jirka, CC BY-SA 3.0 de; 283×360. |
| 1999–2005 | 01-07-1999 | Her Majesty Queen Elizabeth II at the opening of the Scottish Parliament.jpg | Scottish Parliament, CC BY 2.0; reina en el centro, requiere encuadre individual acreditado. |
| 2006–2014 | 07-03-2006 | Elizabeth II, Buckingham Palace, 07 Mar 2006 crop.jpeg | Ricardo Stuckert / PR, derivado Micke, CC BY 3.0 br. |
| 2015–2020 | 20-03-2015 | Queen Elizabeth II in March 2015.jpg | Joel Rouse / Ministry of Defence, derivado nagualdesign, OGL 3.0. |
| 2021–2022 | 13-06-2021 | Elizabeth II 2021 (cropped).jpg | White House, dominio público. |

Las fechas EXIF de escaneo o publicación posterior no sustituyen la fecha de las fotografías históricas. La ventana de 2022 debe respetar el final de su reinado el 8 de septiembre cuando exista precisión diaria.

### Donald Trump · Q22686

| Mandato | Toma | Archivo exacto |
| --- | --- | --- |
| 20-01-2017 a 20-01-2021 | 06-10-2017 | Donald Trump official portrait.jpg |
| Desde 20-01-2025 | 02-06-2025 | Official Presidential Portrait of President Donald J. Trump (2025) (3x4).jpg |

Créditos: Shealeah Craighead y Daniel Torok, respectivamente; ambas son imágenes oficiales en dominio público. El original de 2017 supera 5 MB: reutilizar la copia acreditada existente o adquirir una miniatura de Commons. La toma de junio de 2025 no debe confundirse con el retrato previo a la investidura de enero. Las fichas anuales de 2021 pueden incluir las autoridades sucesivas, cada una con sus fechas reales.

## Faltantes focales

### Vietnam 2007 · Nguyễn Minh Triết, Q57400

La imagen [NguyenMinhTriet (cropped) 2006-Nov-18.jpg](https://commons.wikimedia.org/wiki/File:NguyenMinhTriet_(cropped)_2006-Nov-18.jpg) es una fotografía de Paul Morse / White House del 18 de noviembre de 2006, en dominio público. Su resolución de 100×135 es reducida, pero permite resolver 2007 sin fingir una fotografía anterior a su toma.

Desde 2008 puede usarse [Nguyenminhtriet2008.jpg](https://commons.wikimedia.org/wiki/File:Nguyenminhtriet2008.jpg), de 560×692, del President’s Secretariat de India, GODL-India, tomada el 27 de noviembre de 2008. Para 2009–2011, [Nguyen Minh Triet.jpg](https://commons.wikimedia.org/wiki/File:Nguyen_Minh_Triet.jpg), White House / Lawrence Jackson, 23 de septiembre de 2009, dominio público. No fechar las imágenes posteriores como 2007.

### India 1992 · Shankar Dayal Sharma, Q332157

`Shri Shankar Dayal Sharma.jpg` y `Shanker Dayal Sharma.jpg` proceden de un sello postal de 2000; no son la mejora fotográfica solicitada.

La [fotografía de su juramento de 1992](https://commons.wikimedia.org/wiki/File:Swearing-in_ceremony_of_Shankar_Dayal_Sharma.jpg), de 2500×1769, pertenece al President’s Secretariat, GODL-India. Se revisó visualmente: Sharma aparece de blanco a la derecha de Venkataraman, con gorro y gafas. Se puede presentar mediante un encuadre centrado en él, con crédito e indicación de la modificación. La copia de revisión está en `.cache/portraits014/sharma-1992.jpg`; el JSON contiene una orientación de encuadre, pendiente de revisión final.

Para 1993–1997, [Shankar Dayal Sharma (crop 2).jpg](https://commons.wikimedia.org/wiki/File:Shankar_Dayal_Sharma_(crop_2).jpg) es una fotografía de Biswarup Ganguly del 13 de marzo de 1993, CC BY-SA 3.0. Es una mejora conceptual frente al sello, aunque el original es un escaneo de película con desenfoque y ampliación; no prometer detalle nativo por sus dimensiones.

El [portal presidencial ofrece otro retrato individual](https://presidentofindia.nic.in/dr-shankar-dayal-sharma-profile), pero su [política de copyright exige permiso](https://presidentofindia.nic.in/copyright-policy). No se ha supuesto una licencia GODL para ese archivo por el mero hecho de ser oficial.

### Francia 1888 · Sadi Carnot, Q215778

Se recomienda [Carnot, PA07056.jpg](https://commons.wikimedia.org/wiki/File:Carnot,_PA07056.jpg), retrato individual de Pierre Petit, 1260×1816, dominio público, conservado por KU Leuven Libraries con identificador `lbsn9983536660101471`. La copia `.cache/portraits014/carnot.jpg` está revisada visualmente y muestra la firma de Pierre Petit. La fecha de toma es desconocida; la edición se cataloga 1887–1900. Puede acompañar a su presidencia de 1887–1894 como retrato de época, sin afirmar que se tomó en 1888.

`Portrait officiel de Sadi Carnot.jpg` es también una fotografía individual, pero su procedencia está menos documentada. `Portrait de Sadi Carnot 01.jpg` es una litografía de octubre de 1888; la 03 incluye un discurso de 1889, aunque su título contenga 3 de diciembre de 1887. No convertir esos datos en fechas exactas de toma. `Sadi Carnot.jpeg` representa al físico del mismo nombre y debe descartarse para la ficha del presidente.

### Mozambique 2026 · Maria Benvinda Levi, Q6761049

**Pendiente:** no se ha comprobado un retrato individual con permiso de reutilización suficiente. No se declara este punto corregido. La imagen conjunta existente bajo CC BY-NC-ND 3.0 RS debe mantenerse completa mientras se obtiene una alternativa; no recortarla.

Se comprobó una pista de [PSP](https://thepsp.org/world-leaders/mz) que un buscador atribuía a «Jam123 / CC0»: la página actual muestra un marcador con iniciales, no la imagen original ni una licencia comprobable. No es una fuente válida de adquisición.

La [reunión publicada por MOFA el 17 de junio de 2025](https://www.mofa.go.jp/afr/af2/mz/pageite_000001_01053.html) tiene fotografía acreditada a Cabinet Public Affairs Office. La [licencia del portal](https://www.mofa.go.jp/about/legalmatters.html) excluye obras de terceros: se necesita verificar la publicación o el permiso del titular original. La [reunión de JICA del 18 de junio de 2025](https://www.jica.go.jp/english/information/official/2025/20250623_11.html) vuelve a ser conjunta y su reutilización no se ha acreditado. No confundir a Levi con Quibibi Faquihe Buana en fotografías de UN Women.

## Pendiente de integración

- Adquirir los candidatos de forma secuencial y revisar que cada archivo muestra al sujeto esperado; las comprobaciones de metadatos no sustituyen la revisión visual.
- Resolver los dos avisos de derechos de Franco o conservar alternativas acreditadas del catálogo.
- Encajar individualmente a Sharma en 1992 y a Isabel II en 1999, indicando la modificación y conservando atribuciones.
- Mostrar la fecha real o aproximada de la fotografía sin alterar el formato de la ficha de autoridad.
- Mantener abierta la búsqueda de retrato individual reutilizable de Maria Benvinda Levi, sin presentar el trabajo como terminado.
