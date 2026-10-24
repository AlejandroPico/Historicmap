# Corrección de Alemania y Europa Central,1938–1939

Solicitud adicional del propietario durante la preparación0.12.0. La ampliación1900–1919 ya había superado sus comprobaciones locales. Esta corrección posterior se integra en la misma entrega todavía no subida.

## Diagnóstico

El registro de Cliopatria12807, Alemania nazi1939, contiene187 polígonos sin huecos. Se importó sin cambios como `historical-control.geojson/control-12807`; la instantánea `ww2.geojson/war-4` conserva el mismo original. Dos componentes grandes representan la extensión continental y Prusia Oriental; otros185 incluyen numerosos cuadriláteros aislados en Carelia, Rusia, Italia, Países Bajos, la frontera yugoslava e incluso fuera deEuropa. También existen intrusiones del contorno principal en países vecinos y atribución de territorio eslovaco al controlador alemán. No era solamente un fallo de pintura del navegador.

No se aplica un umbral mundial de superficie: una isla real de la base alemana tiene aproximadamente0,00003grados cuadrados. El tamaño por sí solo no distingue un artefacto de una isla legítima. El componente pequeño deSylt se conserva, junto con todas las islas y costas originales de la base alemana.

## Composición del mapa

`central-europe.ts` normaliza únicamente los controles alemanes de1938/1939 antes de la composición existente. Retiene componentes conectados espacialmente con el teatro documentado —Alemania, Austria, tierras checoslovacas y, desde1939, Polonia— y protege los contornos fechados de los demás países. No modifica archivos originales ni generaliza costas. Austria se incorpora como componente completo; no queda como una ficha nacional independiente debajo de una mancha.

En1938 Praga sigue enChecoslovaquia y losSudetes incorporados se integran enAlemania. En1939 la base checoslovaca se reparte entre tierras checas ocupadas, Estado eslovaco cliente y ampliación húngara. La geometría alemana se disuelve en una única entidad seleccionable: las franjas son la visualización opcional de ocupación, no una segunda Alemania colocada encima. Los restos numéricos del predecesor checoslovaco no se conservan como un país residual seleccionable.

El componente checoslovaco deCShapes está fechado desde2/11/1938, después deMúnich y del primer arbitraje deViena. Se protege su territorio restante al calcular Alemania1938 y la máscara de incorporaciones usada en1939. Esto corrige la atribución prematura deOlomouc del contorno grueso original; Brno yOlomouc continúan checoslovacas en1938 y pasan a ocupación alemana en1939, con franjas cuando se activan. No se interpreta todaMoravia como un Sudetenland ya incorporado en1938.

La nueva identidad `SVK-1939` no hereda estadísticas de laEslovaquia actual. Tiene símbolo histórico y autoridades propias: Tiso, con cambio de jefatura gubernamental a presidencia en octubre, yTuka desde el nombramiento del gabinete28/10. El parentesco cromático conAlemania indica su condición deEstado cliente y no una anexión. La existencia del protectorado deBohemia yMoravia se distingue de las incorporaciones de1938.

## Referencias y límites de geometría

`central-europe-1939.geojson` contiene el contorno húngaro anual deCliopatria y una referencia eslovaca deNaturalEarth, con fuente y licencia por componente. La etiqueta original «Hungarian Republic» no se adopta como régimen histórico de1939. La frontera húngara deCShapes ya representa el primer arbitraje deViena; se conserva esa delimitación más fina dentro de la referencia eslovaca. El contorno grueso deCliopatria no se utiliza para atribuir el centro deBratislava aHungría. Su ampliación oriental sólo se aplica al exterior de la referencia eslovaca y dentro del antiguo componente checoslovaco.

**La parte eslovaca es una referencia contemporánea recortada**, no un levantamiento independiente exacto de1939: se intersecta conChecoslovaquia deCShapes y se excluyen las incorporaciones húngaras y alemanas documentadas. Los cambios municipales posteriores, Petržalka/Devín a escala local y la franja oriental de la guerra eslovaco-húngara de marzo requieren fuentes de mayor detalle. No se inventan frentes ni se afirma exactitud catastral. La sustitución territorial checoslovaca se limita a1939; extenderla a1940–1944 y distinguir la ocupación alemana deEslovaquia desde1944 queda pendiente.

La composición sucede en memoria. CShapes y sus condicionesNC-SA no se incorporan a un archivo redistribuido como si fuese exclusivamenteCCBY. Los originales deCliopatria(CCBY4.0), NaturalEarth(dominio público) yCShapes conservan sus manifiestos y licencias separados.

Esta revisión no certifica el reparto completo dePolonia al final de1939: la síntesis anual importada no tiene un día uniforme y las fases posteriores de la invasión necesitan geometría propia. Se mantiene como pendiente prioritario junto con los demás frentes documentados; la corrección entregada aborda las manchas remotas y la desmembración checoslovaca comunicadas por el propietario.

## Fuentes históricas

- [USHMM, biografía documentada deJozefTiso](https://encyclopedia.ushmm.org/content/en/article/jozef-tiso-1): autonomía de1938, arbitraje deViena, Estado cliente y responsabilidades del régimen.
- [YadVashem, Bratislava bajo el régimen eslovaco](https://wwv.yadvashem.org/YV/en/exhibitions/communities/bratislava/during_holocaust.asp): Austria1938, autonomía eslovaca, Estado cliente, Tiso/Tuka yBratislava como capital.
- [Parlamento eslovaco, sesión constitucional21/7/1939](https://www.nrsr.sk/dl/Browser/Document?documentId=135154).
- [Acta parlamentaria de la declaración del nuevo Gobierno](https://www.nrsr.sk/dl/Browser/Document?documentId=135163): el propio Gobierno fecha su nombramiento28/10/1939. Se distingue de la elección presidencial deTiso26/10, contrastada en la [investigación de la Academia Austríaca deCiencias](https://hw.oeaw.ac.at/0xc1aa500e_0x002f0ea2.pdf).
- Contornos originales: [CShapes](https://icr.ethz.ch/data/cshapes/), [Cliopatria](https://github.com/Seshat-Global-History-Databank/cliopatria) y [NaturalEarth](https://www.naturalearthdata.com/about/terms-of-use/), con revisiones y huellas en los manifiestos locales.

## Comprobaciones

Las regresiones comprueban puntos negativos enCarelia, Rusia, Italia, PaísesBajos, frontera yugoslava, entorno belga/luxemburgués y las pequeñas intrusiones del contorno principal. Casos positivos: Berlín, Viena, Praga1939, Königsberg ySylt; Praga checoslovaca yKarlovyVary alemana en1938; Bratislava, Žilina yPrešov eslovacas, Košice húngara en1939. Se comprueban identificadores únicos, fuentes inmutables, ausencia del predecesor residual, protección deAustria frente a franjas de ocupación y selección alemana/eslovaca con las franjas encendidas o apagadas. Los resultados efectivos de la suite y navegador se registran en DELIVERY-0.12.0.
