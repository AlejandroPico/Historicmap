# Retratos suizos · investigación e integración 0.12.1

Investigación del 24/10/2026 e integración acotada del 25/10/2026. Se han incorporado los 34 retratos revisados y la corrección institucional de los cargos suizos. La comprobación de la presentación en navegador y la actualización del manifiesto de datos corresponden al responsable de la entrega.

## Resultado comprobado de la integración

Se han adquirido **34 de 34 retratos**, sin pendientes en este inventario: **33 GIF originales y un PNG**, con un total de **559.639 bytes**. Se han conservado los bytes y formatos publicados, sin conversión, retoque ni generación de imágenes. Todos se decodifican correctamente y sus tamaños y SHA-256 coinciden con `public/media/manifest.json`. Las fichas de todas las declaraciones suizas de esas personas quedan enlazadas al mismo medio acreditado.

La lista durable es `scripts/swiss-portrait-reviews.json`: cada autorización está limitada a una pareja QID/título exacta y una revisión Commons concreta. Para las 33 imágenes `Copyrighted free use`, el adquiridor exige además el ticket VRT `2007080810014523`, su plantilla de permiso y el origen `admin.ch`, tanto en la declaración revisada como en los créditos. No existe una autorización global para esa etiqueta. Walter Hauser conserva su licencia de dominio público.

La ejecución se ha limitado a `--countries CHE`. La comparación con el catálogo previo confirma que **todos los demás países permanecen idénticos**; también se mantienen todos los mandatos, fechas, precisiones, declaraciones de fuente, banderas y retratos preexistentes. Sólo se añaden los retratos pendientes y las etiquetas/procedencias de cargos suizos. Las 194 etiquetas institucionales corregidas utilizan identificadores de cargo explícitos; no se han deducido fechas o duraciones nuevas.

Comprobaciones completadas: curador puro e idempotente; segunda adquisición sin nuevas descargas ni cambios en identidades/manifiesto de medios; 33 comprobaciones positivas de autorización y **198 negativas** que rechazan persona, título, fuente, ticket o revisión incorrectos. Se han decodificado los 34 originales con un lector de imágenes. La evidencia temporal se conserva en `.cache/swiss-integration-verification.json` y el procedimiento en `.cache/verify-swiss-integration.py`. La prueba global `verify:data` debe ejecutarse después de actualizar la huella de identidades en el manifiesto de datos; esa actualización queda fuera de este subtrabajo.

## Causa encontrada

Las tres personas sin retrato en las fichas suizas de1900–1919 son Walter Hauser(Q693588), Felix Calonder(Q664398) y Ernest Chuard(Q118239). Sus imágenes sí existen en Commons y están enlazadas como P18 en sus identidades humanas verificadas. La ampliación de la comprobación al catálogo suizo completo encuentra34 personas sin imagen y34 originales disponibles:33GIF y unPNG.

El adquiridor anterior sólo admitía cabeceras JPEG/PNG y asignaba extensiónJPG a cualquier formato distinto dePNG. Por ello rechazaba incluso `Hauser.gif`, cuyo uso está acreditado como dominio público. Los otros33 retratos tienen la etiqueta de licencia `Copyrighted free use`, que tampoco estaba entre las etiquetas admitidas. Estos dos filtros explican que faltasen imágenes disponibles, en vez de una inexistencia de fotografías.

No hace falta generar, retocar o ampliar imágenes. Los navegadores pueden mostrar los originalesGIF; conservar su formato y sus bytes evita una conversión innecesaria. Son retratos oficiales archivados, generalmente160×200píxeles; su presencia no certifica una fotografía correspondiente a cada año del mandato.

## Permisos contrastados

Para33 originales se ha leído la revisión de cada ficha Commons mediante su API. Todos contienen el origen `admin.ch`, el mismo expediente de autorización VRT **2007080810014523**, y una declaración explícita de reutilización sin restricción de finalidad, redistribución o modificación. La autorización individual se presenta en las fichas de [Felix Calonder](https://commons.wikimedia.org/wiki/File:Felix-Louis_Calonder.gif) y [Ernest Chuard](https://commons.wikimedia.org/wiki/File:Ernest_Chuard.gif). La correspondencia privada no se ha solicitado ni se ha contactado con terceros: se utiliza la constancia pública revisada por VRT y el permiso declarado para cada archivo.

Para [Walter Hauser](https://commons.wikimedia.org/wiki/File:Hauser.gif) la ficha indica dominio público por fotografía anónima suiza antigua y publicación anterior a1931. Se han comprobado el nombre, las fechas personales y la vinculación con el Consejo Federal. No trasladar de la descripción de la imagen fechas de presidencia o cargos: la descripción puede contener errores y no sustituye una fuente institucional de mandatos.

La integración debe conservar la etiqueta y fuente de permiso reales, autoría y procedencia. Se recomienda un permiso acotado a las parejas **QID/título** de la tabla, con comprobación de ese expedienteVRT y fuente oficial; no autorizar globalmente cualquier imagen de Internet o cualquier fichero con una etiqueta semejante. Mantener las exclusiones, identificación humana, límites de descarga y controles de integridad ya existentes. El hecho de que una imagen salga en un buscador no acredita por sí mismo su permiso de redistribución.

La evidencia detallada de esta sesión está en `.cache/swiss-portrait-candidates.json`: identificador humano, título exacto, URL de ficha y original, licencia, tipoMIME, tamaño, dimensiones, revisión y presencia del expediente. El archivo temporal no se considera una nueva base de datos pública ni sustituye el manifiesto de medios preparado tras la adquisición.

## Criterios aplicados

1. Admitir el originalGIF con extensión y cabeceraGIF correctas, sin renombrarlo comoJPG. Incorporar el formato a la verificación de medios y comprobar su carga real en el navegador.
2. Para los33 archivos con permisoVRT, aplicar exclusivamente la lista revisada de parejasQID/título y verificar permiso/fuente. El permiso deHauser ya encaja con dominio público.
3. Adquirir los34 identificadores con el adquiridor ya corregido, limitado a esas personas. Su P18 coincide con el título revisado; no hace falta elegir un candidato por semejanza del nombre.
4. Mantener todos los mandatos y fechas. Regenerar huellas, inventarios nominales y carpetasPaíses; comprobar Suiza1900,1913,1919 y un año posterior conGIF, además de apertura, retratos y lectura de la ficha.

Comando aplicado con el soporte de formato y permiso acotado del adquiridor:

```powershell
python scripts/enrich-1970-portraits.py --countries CHE --start 1900-01-01 --end 2027-01-01 --people Q693588 Q664398 Q118239 Q118222 Q674180 Q115803 Q118266 Q205316 Q115579 Q115566 Q167080 Q115561 Q546965 Q664453 Q118248 Q550199 Q664369 Q667770 Q663178 Q118284 Q115622 Q116107 Q118260 Q115618 Q115536 Q118201 Q118227 Q118178 Q558027 Q118218 Q118250 Q118282 Q122063 Q115531
```

El adquiridor corregido conserva los límites de tamaño, la identificación humana y las exclusiones existentes. `scripts/verify-data.mjs` admite ahora la extensión GIF en su comprobación de medios acreditados.

## Observación institucional separada

Los datos genéricos suizos también usan `Jefatura del Estado` para mandatos largos de miembros del Consejo Federal y `Jefatura del Gobierno` para la presidencia anual. El [Consejo Federal explica](https://www.admin.ch/en/federal-presidency-role) que la jefatura del Estado corresponde al colegio completo, y que su presidente anual es primero entre iguales. Su [historia institucional](https://www.admin.ch/en/history-of-the-federal-council) confirma la estructura colegiada desde1848 y la rotación consolidada a finales del sigloXIX. Una imagen no valida esos títulos genéricos.

Se ha aplicado `scripts/curate-swiss-offices.py`, puro e idempotente. Utiliza los identificadores explícitos `office=Q11811941`(miembro del Consejo Federal) y `office=Q688230`(presidencia anual), no una deducción por duración del mandato. De195 registros suizos,192 tienen uno de esos identificadores; otros dos son el órgano colectivoQ30917. Se corrigen194 etiquetas y se conserva el registro específicamente curado deParmelin2026, que ya tiene el título correcto y no lleva ese campooffice. Cada cambio conserva `sourceRole`, añade fuente institucional y `authorityClass` para distinguir miembro, presidente anual y órgano colectivo.

Las comprobaciones en memoria confirman pureza, idempotencia, todos los demás países literalmente idénticos y conservación de banderas, número de registros, fechas, precisión, mandatos de fuente, retratos y declaraciones originales. La salida debe elegirse explícitamente:

```powershell
python scripts/curate-swiss-offices.py --output public/data/identities.json
```

El resolver anterior considera la mayor parte de cargos no partidarios como un mismo cargo: puede consolidar por error al miembro del colegio y al presidente anual si son la misma persona. La integración debe distinguir `authorityClass`/`office` paraSuiza y conservar ambos tramos cuando proceda, dando prioridad visual a la presidencia anual. No se debe resolver suprimiendo el mandato colegiado ni alargando un mandato anual. Los mandatos diarios y las suplencias siguen exigiendo su propia revisión; este cambio no valida por sí solo todas sus fechas.

## Inventario nominal revisado

En los33 casosCFU, el expediente es2007080810014523 y el origen oficial figura en la revisión leída. El único casoPD esHauser. La identidad humanaQ5 y el P18 se comprobaron individualmente en los34 casos.

| Persona | QID | Original exacto enCommons | Permiso | Revisión leída |
| --- | --- | --- | --- | ---: |
| Walter Hauser | Q693588 | [Hauser.gif](https://commons.wikimedia.org/wiki/File:Hauser.gif) | Dominio público | 576972960 |
| Felix Calonder | Q664398 | [Felix-Louis Calonder.gif](https://commons.wikimedia.org/wiki/File:Felix-Louis_Calonder.gif) | CFU · VRT verificado | 1156144586 |
| Ernest Chuard | Q118239 | [Ernest Chuard.gif](https://commons.wikimedia.org/wiki/File:Ernest_Chuard.gif) | CFU · VRT verificado | 1232207010 |
| Heinrich Häberlin | Q118222 | [Heinrich Häberlin.gif](https://commons.wikimedia.org/wiki/File:Heinrich_H%C3%A4berlin.gif) | CFU · VRT verificado | 941811057 |
| Jean-Marie Musy | Q674180 | [Jean-Marie Musy.gif](https://commons.wikimedia.org/wiki/File:Jean-Marie_Musy.gif) | CFU · VRT verificado | 905740811 |
| Marcel Pilet-Golaz | Q115803 | [Marcel Pilet-Golaz.gif](https://commons.wikimedia.org/wiki/File:Marcel_Pilet-Golaz.gif) | CFU · VRT verificado | 905785784 |
| Johannes Baumann | Q118266 | [Johannes Baumann.gif](https://commons.wikimedia.org/wiki/File:Johannes_Baumann.gif) | CFU · VRT verificado | 649239910 |
| Walther Stampfli | Q205316 | [Walther Stampfli.gif](https://commons.wikimedia.org/wiki/File:Walther_Stampfli.gif) | CFU · VRT verificado | 906053368 |
| Karl Kobelt | Q115579 | [Karl Kobelt.gif](https://commons.wikimedia.org/wiki/File:Karl_Kobelt.gif) | CFU · VRT verificado | 746918447 |
| Ernst Wetter | Q115566 | [Ernst Wetter.gif](https://commons.wikimedia.org/wiki/File:Ernst_Wetter.gif) | CFU · VRT verificado | 1232280273 |
| Enrico Celio | Q167080 | [Enrico Celio.gif](https://commons.wikimedia.org/wiki/File:Enrico_Celio.gif) | CFU · VRT verificado | 1230517899 |
| Ernst Nobs | Q115561 | [Ernst Nobs.gif](https://commons.wikimedia.org/wiki/File:Ernst_Nobs.gif) | CFU · VRT verificado | 1232273835 |
| Eduard von Steiger | Q546965 | [Eduard von Steiger.gif](https://commons.wikimedia.org/wiki/File:Eduard_von_Steiger.gif) | CFU · VRT verificado | 1224191466 |
| Max Petitpierre | Q664453 | [Max Petitpierre.gif](https://commons.wikimedia.org/wiki/File:Max_Petitpierre.gif) | CFU · VRT verificado | 705439247 |
| Josef Escher | Q118248 | [Josef Escher.gif](https://commons.wikimedia.org/wiki/File:Josef_Escher.gif) | CFU · VRT verificado | 906108672 |
| Markus Feldmann | Q550199 | [Markus Feldmann.gif](https://commons.wikimedia.org/wiki/File:Markus_Feldmann.gif) | CFU · VRT verificado | 1091086610 |
| Hans Streuli | Q664369 | [Hans Streuli.gif](https://commons.wikimedia.org/wiki/File:Hans_Streuli.gif) | CFU · VRT verificado | 1028067303 |
| Thomas Holenstein | Q667770 | [Thomas Holenstein.gif](https://commons.wikimedia.org/wiki/File:Thomas_Holenstein.gif) | CFU · VRT verificado | 693629368 |
| Friedrich Traugott Wahlen | Q663178 | [Friedrich Traugott Wahlen.gif](https://commons.wikimedia.org/wiki/File:Friedrich_Traugott_Wahlen.gif) | CFU · VRT verificado | 1204489126 |
| Paul Chaudet | Q118284 | [Paul Chaudet.gif](https://commons.wikimedia.org/wiki/File:Paul_Chaudet.gif) | CFU · VRT verificado | 906436769 |
| Willy Spühler | Q115622 | [Willy Spühler.gif](https://commons.wikimedia.org/wiki/File:Willy_Sp%C3%BChler.gif) | CFU · VRT verificado | 1129988529 |
| Jean Bourgknecht | Q116107 | [Jean Bourgknecht.gif](https://commons.wikimedia.org/wiki/File:Jean_Bourgknecht.gif) | CFU · VRT verificado | 838207763 |
| Ludwig von Moos | Q118260 | [Ludwig von Moos.gif](https://commons.wikimedia.org/wiki/File:Ludwig_von_Moos.gif) | CFU · VRT verificado | 905659052 |
| Hans Schaffner | Q115618 | [Hans Schaffner.gif](https://commons.wikimedia.org/wiki/File:Hans_Schaffner.gif) | CFU · VRT verificado | 1130496854 |
| Roger Bonvin | Q115536 | [Roger Bonvin.gif](https://commons.wikimedia.org/wiki/File:Roger_Bonvin.gif) | CFU · VRT verificado | 1029875762 |
| Georges-André Chevallaz | Q118201 | [Georges-André Chevallaz.gif](https://commons.wikimedia.org/wiki/File:Georges-Andr%C3%A9_Chevallaz.gif) | CFU · VRT verificado | 1271415942 |
| Ernst Brugger | Q118227 | [Ernst Brugger.gif](https://commons.wikimedia.org/wiki/File:Ernst_Brugger.gif) | CFU · VRT verificado | 1103018123 |
| Hans Hürlimann | Q118178 | [Hans Hürlimann.gif](https://commons.wikimedia.org/wiki/File:Hans_H%C3%BCrlimann.gif) | CFU · VRT verificado | 1182290074 |
| Leon Schlumpf | Q558027 | [Leon Schlumpf.gif](https://commons.wikimedia.org/wiki/File:Leon_Schlumpf.gif) | CFU · VRT verificado | 905981476 |
| Fritz Honegger | Q118218 | [Fritz Honegger.gif](https://commons.wikimedia.org/wiki/File:Fritz_Honegger.gif) | CFU · VRT verificado | 1128800876 |
| Alphons Egli | Q118250 | [Alphons Egli.gif](https://commons.wikimedia.org/wiki/File:Alphons_Egli.gif) | CFU · VRT verificado | 935335159 |
| Rudolf Friedrich | Q118282 | [Rudolf Friedrich.gif](https://commons.wikimedia.org/wiki/File:Rudolf_Friedrich.gif) | CFU · VRT verificado | 700981046 |
| Elisabeth Kopp | Q122063 | [Elisabeth Kopp.gif](https://commons.wikimedia.org/wiki/File:Elisabeth_Kopp.gif) | CFU · VRT verificado | 1227769822 |
| Adolf Ogi | Q115531 | [Adolf Ogi.png](https://commons.wikimedia.org/wiki/File:Adolf_Ogi.png) | CFU · VRT verificado | 782308163 |
