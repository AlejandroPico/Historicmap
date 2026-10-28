# Ampliación 500–599 · Historicmap 0.35.0

La navegación anual incorpora el siglo VI manteniendo cartografía política y áreas culturales independientes, activadas al iniciar. Los registros y originales se conservan en `Países/<entidad>/`; los archivos públicos son compilaciones. La consulta anual no convierte una síntesis histórica en fronteras observadas cada año.

## Alcance y procedencia

- 270 componentes políticos originales, reunidos en 103 grupos nominales de Cliopatria. Coordenadas e índices originales intactos; no se incorporan uniones agregadas duplicadas. Fuente fijada: [Cliopatria, commit 5f433377139a6eeaeacbdc894b70f8805b72c8b5](https://github.com/Seshat-Global-History-Databank/cliopatria/tree/5f433377139a6eeaeacbdc894b70f8805b72c8b5), licencia CC BY 4.0.
- 108 dossiers políticos/de cortes para500–599, con272 registros de autoridades. No son272 personas distintas ni108 series completas. Tres dossiers adicionales mantienen las nuevas cortes mayas consultables en600–699; incorporan solamente los dos reinados que atraviesan ese límite, no una revisión completa de todas sus sucesiones posteriores.
- 87 dossiers regionales originales de [historical-basemaps, world_500](https://github.com/aourednik/historical-basemaps/blob/da7a4b735ecef70aebdc9c73e409d8a2500d50f3/geojson/world_500.geojson):73 referencias adoptadas,12 remisiones a la base política ydos etiquetas anacrónicas excluidas de la visualización. Fuente fijada al commit indicado, con su licencia GPL separada de la fuente política. No se mezclan sus geometrías para crear fronteras nuevas.
- 43 cortes/centros documentales fechados,21 contextos y8 puntos regionales de conflicto. Las sedes no generan polígonos de soberanía, capitales medidas ni un inventario completo de batallas.

## Cronologías y correcciones

La [cronología de China del Metropolitan Museum](https://www.metmuseum.org/de/toah/ht/06/eac) distingue Wei del Norte, sus ramas oriental/occidental, Qi, Zhou, Liang, Chen y Sui. Se separa la proclamación Sui de581 de la conquista deChen en589. Cuando el contorno de la compilación empieza después de la proclamación, una corte documental permite consultar la autoridad; cuando continúa después del fin de la dinastía, se identifica como referencia heredada. No se adelanta un polígono posterior para tapar una laguna.

El lector de mandatos conserva fechas envueltas en `nowr`, fechas de mes/día con año compartido, finales abreviados y el tipo de dignidad de cada fase. El título de césar no se presenta como reinado imperial deJustiniano antes de527 ni deMauricio antes de582. TiberioII tiene una fase de regencia diferenciada de su mandato como emperador. Las regencias y reinados deAmalasunta se distinguen.

El segundo reinado deKavad ya estaba en curso en500: [Iranica, Kawād I](https://www.iranicaonline.org/articles/kawad-i/kawad-i-reign/). Se conservan las fases no consecutivas deCosroesII y las autoridades rivales; la cronología alternativa deVistahm se presenta como aproximada. Los [lajmíes](https://www.iranicaonline.org/articles/lakhmids/) comparten familia cromática con su potencia tutelar sasánida, sin convertirse automáticamente en una provincia anexionada; se distingue también el vínculo gasánida con el poder romano.

Istämi figura como yabghu de la rama occidental, no como gran kan independiente de todo el poder túrquico. Las propuestas582/583 y603 fechan etapas distintas de la división; las ramas y la agrupación general no son tres imperios homogéneos distintos: [estudio de la Universidad deSzeged](https://doktori.bibl.u-szeged.hu/10772/1/Kahraman_Mutlu_PhD_dissertation.pdf).

La campaña italiana no se confunde con una conquista instantánea: [Whitby, Justinian and Italy, 535–554](https://onlinelibrary.wiley.com/doi/abs/10.1002/9781119099000.wbabat0890). Las agrupaciones merovingias tienen cortes y reyes distintos; la etiqueta cartográfica no prueba una monarquía nacional unitaria. La dignidad pontificia deRoma no equivale a unos Estados Pontificios soberanos del sigloVI. Las listas tempranas deYamato se identifican como tradición retrospectiva.

El final del poder deDhu Nuwas en525 se distingue de los gobernantes locales bajo intervención aksumita yposterior influencia persa: [investigación sobre Himyar y su contexto ambiental](https://par.nsf.gov/servlets/purl/10353205). El testimonio deVainyagupta enGunaighar507–508 se consulta como autoridad regional deSamatata; no se transforma en un mandato imperial gupta543–548 ni en un reinado completo: [estudio documental de la Universidad deBengala del Norte](https://ir.nbu.ac.in/server/api/core/bitstreams/557e866e-0446-4da4-86f6-69dd4b6b5162/content).

## Cortes mayas

Palenque,Tikal yCopán tienen fichas independientes en puntos documentales; el contorno general maya es una referencia regional yno un Estado único. La relación `aggregateKey` hospeda su selección visual yno declara vasallaje.

- [Tabla epigráfica dePalenque, Mesoweb](https://www.mesoweb.com/palenque/resources/rulers/rulers_table.html): las correlaciones deCuenta Larga ycalendario gregoriano difieren en días. Se conserva una presentación anual explícita ylas lagunas entre reinados; Yohl Ik’nal atraviesa el límite600.
- [Manual de monumentos deCopán, Agurcia Fasquelle/FAMSI](https://www.famsi.org/research/copan/monuments/CopanMonumentManual.pdf), contrastado con [investigación deHarvard](https://dash.harvard.edu/bitstream/handle/1/9548615/FiererDonaldson_gsas.harvard_0084L_10459.pdf?sequence=1): B’alam Nehn corresponde a524–532, frente al intervalo504–544 de la fuente general. Wi’l Ohl K’inich ocupa532–551; los nombres parcialmente leídos de los gobernantes5 y6 permanecen incompletos ycon fechas aproximadas.
- [Copán, UNESCO](https://whc.unesco.org/en/list/129): centro político local del Clásico, con una dinastía propia. Las listas retrospectivas y las representaciones monumentales requieren distinguir persona, glifo nominativo yconvención regia.

## Referencias culturales y anacronismos

Se conservan Sámi, Amazonia, comunidades norteamericanas, pueblos africanos, australianos yasociaciones regionales deAsia. Los contornos culturales no acreditan homogeneidad étnica ni control político. Las etiquetas deImperio romano occidental yJin se reinterpretan como ámbitos posimperiales; las referencias sasánida,Goguryeo yBaekje no anticipan sus conquistas posteriores. Hokkaidō se describe mediante tradiciones Epi-Jōmon/Okhotsk, sin proyectar una nación ainu moderna uniforme.

Poverty Point yMill Creek no se acreditan como culturas del sigloVI: sus originales, decisiones ygeometrías permanecen en sus propias carpetas con `phases: []`. Contraste: [Poverty Point, National Park Service](https://www.nps.gov/popo/learn/historyculture/index.htm) y [arqueología deIowa](https://publications.iowa.gov/13315/1/TeamArchaeology12web.pdf). Hopewell/Goodall yotras tradiciones de transición no se presentan como culturas inmutables hasta599. La continuidad de una referencia espacial no certifica una identidad sin cambios.

## Imágenes y límites pendientes

125 candidatos inspeccionados visualmente:95 aceptados y30 rechazados. Monedas, mosaicos, estelas, representaciones imaginarias y conmemorativas tienen pies diferenciados y licencia; no se describen automáticamente como retratos del natural. Se rechazan glifos usados como fotos, mapas, objetos sin atribución, piezas con efigie imperial diferente del emisor local ymanuscritos ajenos a la persona. Los candidatos ausentes ylas razones de rechazo se registran en [MEDIA-REVIEW-500.json](MEDIA-REVIEW-500.json) yen cada dossier.

No se añaden banderas nacionales modernas o heráldica posterior para rellenar celdas del sigloVI. Faltan sucesiones locales, poderes menores, administraciones regionales, imágenes fiables ysímbolos con vigencia acreditada. Los rangos de autoridades se limitan a la consulta yno convierten el fin599 en una extinción. Las lagunas nominales y la disponibilidad anual se inventarían en [REVIEW-500-599.json](REVIEW-500-599.json). El inventario de pruebas, conservación de datos yestado del envío se mantiene en `agentes.md` y`tareas.md`.
