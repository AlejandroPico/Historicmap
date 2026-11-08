---
id: tierra-campo-magnetico
tipo: tierra
titulo: El campo magnético primitivo
alias: [Geodinamo, Magnetosfera, Paleomagnetismo temprano, Dinamo terrestre, Paleointensidad, Núcleo interno]
resumen: Cómo genera el núcleo el campo magnético terrestre, con qué energía funcionó antes de existir el núcleo interno, qué registran las rocas arcaicas y los circones hádicos y qué papel tuvo la magnetosfera en la conservación de la atmósfera.
padre: geo-Hadean
orden: 8
inicio: 4.2 Ga
fin: 2.5 Ga
ficha:
  Campo actual en superficie: ≈ 25–65 µT (dipolo de ≈ 8 × 10²² A·m²)
  Registro más antiguo aceptado: ≈ 3.450 Ma (Barberton, Pilbara); posible ≈ 3.700 Ma (Isua)
  Registro propuesto más antiguo: ≈ 4.200 Ma (circones de Jack Hills, discutido)
  Intensidad hacia 3.450 Ma: ≈ 50–70 % de la actual (Tarduno et al. 2010)
  Magnetopausa actual: ≈ 10–11 radios terrestres; hacia 3.450 Ma, ≈ 5 o menos
  Edad del núcleo interno: ≈ 1.500–500 Ma (estimaciones muy dispares)
  Flujo de calor a través del límite núcleo–manto: ≈ 5–15 TW
  Número de Reynolds magnético del núcleo: ≈ 10³
relacionados: [tierra-diferenciacion, interior, atmosphere, tierra-circones-jack-hills, geo-Hadean, geo-Paleoarchean, plate-tectonics]
fuentes:
  - titulo: Wikipedia · Campo magnético terrestre
    url: https://es.wikipedia.org/wiki/Campo_magn%C3%A9tico_terrestre
  - titulo: Wikipedia · Dynamo theory
    url: https://en.wikipedia.org/wiki/Dynamo_theory
  - titulo: Tarduno et al. (2010) · Geodynamo, solar wind, and magnetopause 3.4 to 3.45 billion years ago. Science 327
    url: https://doi.org/10.1126/science.1183445
  - titulo: Tarduno et al. (2015) · A Hadean to Paleoarchean geodynamo recorded by single zircon crystals. Science 349
    url: https://doi.org/10.1126/science.aaa9114
  - titulo: Weiss et al. (2015) · Pervasive remagnetization of detrital zircon host rocks in the Jack Hills, Western Australia and implications for records of the early geodynamo. Earth and Planetary Science Letters 430
    url: https://doi.org/10.1016/j.epsl.2015.08.012
  - titulo: Tang et al. (2019) · Secondary magnetite in ancient zircon precludes analysis of a Hadean geodynamo. PNAS 116
    url: https://doi.org/10.1073/pnas.1811074116
  - titulo: Borlina et al. (2020) · Reevaluating the evidence for a Hadean-Eoarchean dynamo. Science Advances 6
    url: https://doi.org/10.1126/sciadv.aav9634
  - titulo: Tarduno, Cottrell, Bono et al. (2020) · Paleomagnetism indicates that primary magnetite in zircon records a strong Hadean geodynamo. PNAS 117
    url: https://doi.org/10.1073/pnas.1916553117
  - titulo: Biggin et al. (2015) · Palaeomagnetic field intensity variations suggest Mesoproterozoic inner-core nucleation. Nature 526
    url: https://doi.org/10.1038/nature15523
  - titulo: Bono, Tarduno, Nimmo y Cottrell (2019) · Young inner core inferred from Ediacaran ultra-low geomagnetic field intensity. Nature Geoscience 12
    url: https://doi.org/10.1038/s41561-018-0288-0
  - titulo: Pozzo, Davies, Gubbins y Alfè (2012) · Thermal and electrical conductivity of iron at Earth's core conditions. Nature 485
    url: https://doi.org/10.1038/nature11031
  - titulo: Konôpková, McWilliams, Gómez-Pérez y Goncharov (2016) · Direct measurement of thermal conductivity in solid iron at planetary core conditions. Nature 534
    url: https://doi.org/10.1038/nature18009
  - titulo: O'Rourke y Stevenson (2016) · Powering Earth's dynamo with magnesium precipitation from the core. Nature 529
    url: https://doi.org/10.1038/nature16495
  - titulo: Badro, Siebert y Nimmo (2016) · An early geodynamo driven by exsolution of mantle components from Earth's core. Nature 536
    url: https://doi.org/10.1038/nature18594
  - titulo: Hirose et al. (2017) · Crystallization of silicon dioxide and compositional evolution of the Earth's core. Nature 543
    url: https://doi.org/10.1038/nature21367
  - titulo: Weiss y Tikoo (2014) · The lunar dynamo. Science 346
    url: https://doi.org/10.1126/science.1246753
---
La Tierra tiene un campo magnético propio porque en su núcleo externo hay unos 1,8 × 10²⁴ kg de hierro líquido en movimiento. Ese metal, buen conductor eléctrico, se agita por convección y es desviado por la rotación del planeta; su movimiento a través de un campo magnético induce corrientes eléctricas, y esas corrientes regeneran el campo. El sistema se mantiene a sí mismo mientras haya energía para mover el fluido: es la **geodinamo**. Alrededor del planeta, el campo forma una cavidad, la **magnetosfera**, que desvía el viento solar y modifica la manera en que la atmósfera pierde gas al espacio.

Esta página trata la física de la dinamo, la energía que la alimentó antes de que existiera el núcleo interno sólido, los registros paleomagnéticos más antiguos y su controversia, y el papel de la magnetosfera primitiva. La estructura del núcleo actual se describe en [[interior|el interior de la Tierra]], y su formación en [[tierra-diferenciacion|diferenciación]].

![Magnetosfera terrestre](medios/hadico/magnetosfera-nasa.jpg "Representación de la magnetosfera terrestre (NASA). El viento solar comprime el campo en el lado diurno, donde la magnetopausa está hoy a unos 10 radios terrestres, y lo estira en una larga cola en el lado nocturno.")

## Cómo funciona una dinamo planetaria

### Las condiciones

Una dinamo autosostenida requiere tres ingredientes: un fluido conductor de gran volumen, una fuente de energía que lo mantenga en movimiento y una rotación suficientemente rápida para organizar el flujo. La eficacia se mide con el **número de Reynolds magnético**, Rm = U·L/η, que compara la generación de campo por el movimiento del fluido (velocidad U, escala L) con su disipación por la resistencia eléctrica (difusividad magnética η). Para el núcleo externo, con velocidades de alrededor de medio milímetro por segundo —deducidas de la variación secular del campo—, una escala de unos 2.000 km y una difusividad de alrededor de 1 m²/s, Rm es del orden de 10³, muy por encima del umbral teórico de unas decenas necesario para que la dinamo funcione.

La rotación hace que la fuerza de Coriolis domine el flujo, que se organiza en columnas alineadas con el eje de giro. Por eso el campo terrestre es, en promedio, un **dipolo axial**, aunque el eje magnético está hoy inclinado unos 10° respecto al de rotación y el campo tiene componentes no dipolares importantes. Las simulaciones numéricas tridimensionales, desde las de Gary Glatzmaier y Paul Roberts en 1995, reproducen campos dipolares con inversiones espontáneas, aunque con parámetros alejados de los reales por limitaciones de cálculo.

### La energía

La dinamo consume una potencia del orden de unos pocos teravatios, procedente del calor que el núcleo pierde hacia el manto, estimado en **5–15 TW** a través del límite núcleo–manto. Ese flujo puede alimentar dos tipos de convección:

- **Convección térmica.** El metal caliente de abajo asciende y el frío de arriba desciende. Solo es eficaz si el núcleo pierde calor más deprisa de lo que puede conducirlo por difusión a lo largo del gradiente adiabático.
- **Convección composicional.** Cuando el núcleo interno cristaliza, expulsa elementos ligeros al líquido que lo rodea; ese líquido, menos denso, asciende y agita el núcleo externo. Es un motor mucho más eficiente que el térmico, porque convierte en trabajo una fracción mayor de la energía.

Hoy, la mayor parte de la energía de la geodinamo procede de la **cristalización del núcleo interno**, que crece alrededor de un milímetro por año.

## El problema del núcleo antiguo

### La paradoja de la conductividad

El núcleo interno es un rasgo relativamente reciente. Su edad depende de la rapidez con que el núcleo se enfría, y esta, de la **conductividad térmica** del hierro a presiones de 135–330 GPa y temperaturas de 4.000–6.000 K. En 2012, Monica Pozzo, Christopher Davies, David Gubbins y Dario Alfè calcularon mediante métodos de primeros principios una conductividad de unos 100 W/(m·K) o más, dos o tres veces mayor que la aceptada hasta entonces. Si es así, una parte considerable del calor del núcleo se escapa por conducción, la convección térmica se debilita y el núcleo interno tiene que ser joven, de menos de mil millones de años. Pero entonces, ¿qué alimentó la dinamo durante los tres mil millones de años anteriores, que las rocas registran? Es la llamada **«nueva paradoja del núcleo»**.

Los experimentos no han zanjado la cuestión. En 2016 se publicaron en el mismo número de *Nature* dos mediciones con celdas de yunque de diamante calentadas por láser: la de Zuzana Konôpková y colaboradores obtuvo una conductividad baja, de unos 18–44 W/(m·K), compatible con un núcleo interno antiguo; la de Kenji Ohta y colaboradores, una conductividad alta, compatible con los cálculos teóricos.

### Fuentes de energía alternativas

Si la conductividad es alta, la dinamo antigua necesitó otras fuentes de energía. Las más estudiadas son:

| Mecanismo | Propuesta | Idea |
|---|---|---|
| Precipitación de MgO | O'Rourke y Stevenson (2016); Badro, Siebert y Nimmo (2016) | El núcleo disolvió magnesio y oxígeno a las altísimas temperaturas de su formación; al enfriarse, los óxidos precipitan en la cima del núcleo y dejan un líquido residual más denso que se hunde |
| Cristalización de SiO₂ | Hirose y colaboradores (2017) | El silicio y el oxígeno disueltos se combinan y cristalizan como sílice, con el mismo efecto de convección composicional |
| Núcleo inicial muy caliente | Varios autores | Un núcleo que nació miles de grados más caliente que el manto pudo perder calor muy deprisa al principio |
| Radiactividad en el núcleo | Propuesta discutida | Potasio 40 disuelto en el metal; los experimentos sugieren que la cantidad es pequeña |
| Mareas y precesión | Propuesta minoritaria | La deformación por mareas de una Luna cercana y la precesión del eje agitan mecánicamente el núcleo |

Todas estas propuestas comparten una idea: la dinamo primitiva pudo ser **composicional** desde el principio, gracias a la química heredada de la formación del núcleo a alta temperatura, mucho antes de que existiera el núcleo interno.

## Cómo registran las rocas el campo antiguo

### Magnetización remanente

Ciertos minerales —sobre todo la magnetita y la hematites— adquieren una **magnetización remanente** paralela al campo ambiental cuando se enfrían por debajo de su temperatura de Curie (580 °C en la magnetita) o cuando crecen. El paleomagnetismo mide la **dirección** de esa magnetización, que informa sobre la latitud de la roca y la polaridad del campo, y su **intensidad**, que permite estimar la intensidad del campo antiguo (**paleointensidad**). El método clásico de paleointensidad, de Émile y Odette Thellier (1959), compara la magnetización natural con la que adquiere la muestra en el laboratorio al recalentarla en un campo conocido.

### El problema de las rocas antiguas

Casi todas las rocas arcaicas han sido metamorfizadas, y cualquier recalentamiento por encima de unos cientos de grados, o la formación de minerales magnéticos nuevos, borra la señal original y la sustituye por otra posterior. Para obtener registros fiables se usan varias estrategias: las **pruebas de campo** (la prueba del conglomerado, por ejemplo: si los cantos de un conglomerado tienen magnetizaciones orientadas al azar, no se remagnetizaron después del depósito), el análisis de **cristales individuales** de feldespato o de circón que encierran diminutas inclusiones de magnetita protegidas de la alteración, y técnicas de imagen magnética de alta resolución, como el microscopio cuántico de diamante, capaz de cartografiar el campo de partículas de micrómetros.

## Los registros más antiguos

### Barberton y Pilbara: 3.450 Ma

Los registros mejor establecidos proceden de los cinturones de rocas verdes de **Barberton** (Sudáfrica) y **Pilbara** (Australia), de unos 3.450 Ma. En 2010, John Tarduno y colaboradores midieron la paleointensidad en cristales individuales de cuarzo y feldespato de dacitas de Barberton y obtuvieron valores de entre el **50 y el 70 %** de la intensidad actual. Otros estudios en Pilbara confirman un campo de intensidad comparable con una dirección estable. La geodinamo funcionaba, por tanto, en el Paleoarcaico.

### Isua: 3.700 Ma

En 2024, Claire Nichols y colaboradores presentaron mediciones de formaciones de hierro bandeado del cinturón de **Isua** (Groenlandia), que solo se calentaron hasta temperaturas moderadas tras su formación. Sus resultados indican un campo de al menos unos 15 µT hacia 3.700 Ma, del mismo orden que el actual, y llevarían el registro aceptable de la dinamo al Eoarcaico.

### Jack Hills: ¿4.200 Ma?

En 2015, Tarduno y colaboradores publicaron mediciones en circones de [[tierra-circones-jack-hills|Jack Hills]] de hasta 4.200 Ma con inclusiones de magnetita, que interpretaron como registro de un campo de intensidad comparable a la actual en el Hádico, con intervalos de campo débil hacia 3.900 Ma. La respuesta crítica fue inmediata:

- Benjamin Weiss y colaboradores (2015) mostraron que las rocas de Jack Hills sufrieron una **remagnetización generalizada** por calentamiento y alteración en el Arcaico tardío o después.
- Fengzai Tang y colaboradores (2019) observaron con microscopía electrónica que gran parte de la magnetita de los circones de Jack Hills es **secundaria**: creció a lo largo de fracturas mucho después de la cristalización del circón.
- Cauê Borlina y colaboradores (2020) analizaron circones con el microscopio cuántico de diamante y concluyeron que la mayoría no conserva una magnetización hádica fiable.

Tarduno y colaboradores replicaron en 2020 que los circones que seleccionaron contienen magnetita primaria y que su señal es coherente. La cuestión sigue abierta, y la existencia de una dinamo hádica se considera plausible pero no demostrada.

:::linea-tiempo El registro paleomagnético temprano
4.2 Ga | Circones de Jack Hills: campo hádico propuesto (discutido)
3.7 Ga | Formaciones de hierro de Isua: campo de al menos ≈ 15 µT (2024)
3.45 Ga | Dacitas de Barberton y lavas de Pilbara: campo del 50–70 % del actual
2.7 Ga / 2.5 Ga | Registros neoarcaicos abundantes y polaridad invertida documentada
1.5 Ga / 1.0 Ga | Posible aumento de intensidad: nucleación del núcleo interno según Biggin (2015)
0.565 Ga | Campo ediacárico muy débil: núcleo interno a punto de nacer según Bono (2019)
:::

## ¿Cuándo nació el núcleo interno?

El nacimiento del núcleo interno debería dejar una huella en el registro paleomagnético: un aumento de la intensidad media del campo cuando la convección composicional empieza a funcionar. Andrew Biggin y colaboradores (2015) identificaron en una recopilación de paleointensidades un aumento hacia 1.500–1.000 Ma y lo atribuyeron a la nucleación del núcleo interno en el Mesoproterozoico. Richard Bono, John Tarduno y colaboradores (2019) hallaron, en cambio, intensidades extraordinariamente bajas —unas diez veces inferiores a las actuales— en rocas ediacáricas de unos 565 Ma, que interpretaron como una dinamo térmica moribunda justo antes de que el núcleo interno empezara a cristalizar, lo que lo haría muy joven. Las dos interpretaciones son incompatibles, y su resolución depende de nuevos datos proterozoicos y de la conductividad del hierro.

## La magnetosfera y la atmósfera

### El tamaño de la burbuja

El límite de la magnetosfera en el lado diurno, la **magnetopausa**, se sitúa donde la presión magnética del campo terrestre equilibra la presión dinámica del viento solar. Como el campo de un dipolo disminuye con el cubo de la distancia, la distancia de equilibrio es proporcional a la raíz cúbica de la intensidad del campo y a la potencia −1/6 de la presión del viento:

:::grafico linea | Distancia de la magnetopausa según la intensidad del campo | radios terrestres | intensidad del dipolo (actual = 1)
intensidad; viento solar actual; viento 30 veces más intenso (Sol joven); viento 100 veces más intenso
0,1; 4,9; 2,8; 2,3
0,2; 6,1; 3,5; 2,9
0,3; 7,0; 4,0; 3,3
0,5; 8,3; 4,7; 3,9
0,7; 9,3; 5,3; 4,3
1,0; 10,5; 6,0; 4,9
1,5; 12,0; 6,8; 5,6
:::

Las curvas se han calculado con la relación de equilibrio de presiones, tomando 10,5 radios terrestres como distancia actual. El Sol joven giraba más deprisa y emitía un viento más denso y rápido; con un campo del 50–70 % del actual y un viento varias decenas de veces más intenso, la magnetopausa del Paleoarcaico estaría a unos **5 radios terrestres** o menos, como estimaron Tarduno y colaboradores en 2010. Durante las grandes tormentas solares podía comprimirse hasta muy cerca de la atmósfera.

### ¿Protege el campo la atmósfera?

La idea tradicional es que la magnetosfera protege la atmósfera de la erosión por el viento solar, y el ejemplo de Marte —que perdió su dinamo hace unos 4.000 millones de años y buena parte de su atmósfera después— parece confirmarlo. La sonda MAVEN de la NASA mide hoy en Marte un escape de iones del orden de 100 gramos por segundo, que se multiplica durante las tormentas solares.

La relación es menos simple de lo que parece. Un campo magnético desvía el viento solar, pero también canaliza energía hacia los polos y alimenta allí el escape de iones de oxígeno e hidrógeno a lo largo de las líneas de campo abiertas (el «viento polar»). Venus, sin campo propio, conserva una atmósfera densísima, aunque perdió casi toda su agua. Varios estudios recientes sostienen que, para planetas como la Tierra, las tasas de escape con y sin campo magnético pueden ser comparables. El papel protector de la magnetosfera primitiva es, por tanto, objeto de debate; lo que sí está claro es que modifica la manera en que se pierde la atmósfera y las especies que escapan.

:::debate ¿Fue decisivo el campo magnético para la habitabilidad?
Quienes defienden la importancia de la dinamo temprana señalan que el viento del Sol joven era intensísimo y que, sin magnetosfera, la erosión de la alta atmósfera y la pérdida de hidrógeno —y con él, de agua— habrían sido mayores. También recuerdan que el campo reduce la llegada de partículas energéticas a la superficie. Quienes lo relativizan argumentan que la masa de la atmósfera y la gravedad del planeta son factores más importantes que el campo, y que el escape no térmico de iones puede ser incluso mayor con un campo magnético. La respuesta depende de detalles de la física de la alta atmósfera en condiciones que no existen hoy, y es relevante para evaluar la habitabilidad de exoplanetas.
:::

## La dinamo de la Luna

La Luna, con un núcleo de solo unos 300–350 km de radio, tuvo también un campo magnético propio. Las muestras del Apolo indican, según la revisión de Benjamin Weiss y Sonia Tikoo (2014), un campo superficial de decenas de microteslas entre unos 4.250 y 3.560 Ma, seguido de un campo mucho más débil hasta su desaparición hace unos 1.900–800 Ma. Mantener una dinamo tan intensa en un núcleo tan pequeño es difícil; se han propuesto como motores la agitación mecánica por precesión del eje lunar, cuando la Luna estaba más cerca de la Tierra, y la cristalización o la convección composicional en el núcleo. La comparación ayuda a evaluar las fuentes de energía que pudieron alimentar la dinamo terrestre en el mismo periodo.

:::curiosidad Polaridades invertidas desde el Arcaico
El campo terrestre se invierte de forma irregular: el polo norte magnético pasa al hemisferio sur. La última inversión completa, la de Brunhes-Matuyama, ocurrió hace unos 780.000 años, y la secuencia de inversiones grabada en el fondo oceánico fue una de las pruebas decisivas de la [[plate-tectonics|tectónica de placas]]. Las rocas neoarcaicas y paleoproterozoicas ya registran polaridades opuestas, lo que indica que la dinamo invertía su campo hace más de 2.500 millones de años, como hoy.
:::

:::clave
La geodinamo existía hace al menos 3.450 millones de años, probablemente desde hace 3.700 y quizá desde el Hádico. Antes de que naciera el núcleo interno —cuya edad se discute entre 1.500 y 500 Ma—, la dinamo necesitó una fuente de energía distinta, probablemente la precipitación de óxidos heredados de la formación del núcleo. La magnetosfera primitiva era más pequeña que la actual y su papel en la conservación de la atmósfera sigue en discusión.
:::
