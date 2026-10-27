# Pueblos y regiones · cierre de las partes cinco y seis · 0.30.0

## Alcance y resultado

La ampliación incorpora referencias posteriores a 1700 hasta **1905** y revisa la disponibilidad y coexistencia de todo el intervalo **900–1905**. La base política anual conserva sus geometrías, identidades y colores. Las regiones culturales se consultan mediante búsqueda y «En este lugar»; la selección política tiene prioridad. La colonización no implica desaparición cultural.

El inventario acumulado contiene **6.657 dossiers** dentro de sus carpetas de `Países`: 5.061 referencias adoptadas, 1.516 remisiones a la base política y 80 exclusiones razonadas. Se compilan **6.815 fases**, de las que 6.506 son culturales/geográficas y 309 referencias políticas. No son cifras de Estados, pueblos distintos o población.

Se añaden siete instantáneas de Historical Basemaps fijadas en el commit `da7a4b735ecef70aebdc9c73e409d8a2500d50f3`: 1715 (600 nombres), 1783 (549), 1800 (546), 1815 (312), 1878 (172), 1880 (169) y 1900 (165). Los **2.513 pares nombre/instantánea** tienen decisión, originales, propiedades, procedencia y licencia por entidad. La separación de componentes insulares genera 2.516 dossiers espaciales nuevos. Dos entradas adicionales recuperan contextos históricos seminola y métis con geometrías originales ya conservadas.

## Qué significa la continuidad

Las instantáneas tardías contienen menos detalle regional; su omisión de un pueblo no prueba que desapareciese. Se conservan 1.753 contextos activos en 1700 hasta el siguiente testimonio espacial o el horizonte de revisión. Estas fases llevan `continuationReference` y `temporalMode: historical-area-context`. El comienzo de la fase técnica en 1701 no significa un levantamiento cartográfico ese año.

Las fichas distinguen año consultado, fecha de la fuente, ventana de consulta e incertidumbre. Las **1.755 fases de contexto histórico** no acreditan residencia constante, continuidad institucional, soberanía o límites invariables. Las **3.830 fases tradicionales sin cronología local suficiente** siguen identificadas como pendientes. Se conserva la geometría documentada, sin interpolarla ni fabricar desplazamientos. Fuera de 1905 la ficha permanece abierta y explica la falta de cobertura; no declara extinto a un pueblo.

## Contrastes focales

- **Seminolas:** la [Tribal Historic Preservation Office](https://www.stofthpo.com/seminole-history/) y la [cronología del Museum of Florida History](https://www.museumoffloridahistory.com/explore/exhibits/previous-exhibits/seminole-people-of-florida/educational-resources/seminole-timeline/) permiten recuperar un contexto desde un testimonio de 1740. Se explica la formación histórica y las migraciones, sin convertir la superficie tradicional en una frontera de 1740 ni reducir todas las comunidades a una única ascendencia.
- **Desplazamiento cheroqui:** los documentos del [National Park Service](https://home.nps.gov/articles/000/introduction-transportation-during-the-cherokee-removal-1837-1839.htm) distinguen la expulsión de 1837–1839 y las comunidades que permanecieron. Conservar un área histórica no pretende situar allí a toda la población después del desplazamiento.
- **Comunidades métis:** los [Archives of Manitoba](https://www.gov.mb.ca/chc/archives/hbca/spotlight/seven_oaks.html) y el [Gabriel Dumont Institute](https://www.metismuseum.ca/resource.php/14172) documentan Seven Oaks en 1816. Es un testimonio de organización y afirmación colectiva; no el nacimiento exacto de todos los pueblos métis, ni una fecha de la superficie tradicional. No se retrotrae una organización contemporánea a 1492.
- **Aotearoa:** el [Waitangi Tribunal](https://www.waitangitribunal.govt.nz/en/about/the-treaty/about-the-treaty) distingue los textos del tratado y su interpretación. Los iwi y hapū no desaparecen en 1840. Variantes editoriales «Māori», «Maoris» y «M?ori» conservan una identidad de consulta, con nombres originales disponibles.
- **Australia y Tasmania:** [AIATSIS](https://aiatsis.gov.au/explore/map-indigenous-australia) explica el carácter general de las ubicaciones y sus límites; se consulta como criterio metodológico, sin copiar su mapa. El [National Museum of Australia](https://www.nma.gov.au/defining-moments/resources/the-black-line) documenta la violencia y los desplazamientos de Tasmania. No se interpreta 1876 como extinción cultural. Las comunidades siguen seleccionables bajo el territorio colonial.
- **Mapuches:** [Memoria Chilena](https://www.memoriachilena.gob.cl/602/w3-propertyvalue-18732.html) permite contextualizar la ocupación de la Araucanía sin fabricar un frente continuo o hacer desaparecer sus comunidades en una fecha de anexión.
- **África austral:** la [cronología del Met](https://82nd-and-fifth.metmuseum.org/toah/ht/10/afo.html) distingue procesos de formación estatal y expansión. Una referencia a comunidades zulúes en 1783 no se presenta como el reino del siglo XIX. Las denominaciones obsoletas de monarquías en instantáneas tardías no reemplazan los regímenes de la base política anual.
- **Hawái y Rapa Nui:** componentes separados y selección independiente. El [National Park Service](https://home.nps.gov/articles/000/queen-lili-uokalani.htm) documenta el derrocamiento de 1893 y la oposición a la anexión. Una referencia cultural no perpetúa el reino político después de su final.

## Revisión global y límites abiertos

La [auditoría anual](CULTURAL-GLOBAL-REVIEW-900-1905.json) registra **1.006 selecciones anuales**, cambios de fase, referencias históricas y cruces con la representación política. El [inventario nominal](CULTURAL-REVIEW-900-1905.json) recoge cada decisión y sus pendientes. La [conservación e integridad](CULTURAL-VALIDATION-0.30.json) contrasta originales, datos anteriores e idempotencia del preparador.

Las 1.516 remisiones políticas se clasifican por evidencia de enlace: 219 con clave explícita presente, 51 con propietario presente pero relación histórica pendiente, 73 con candidato nominal y 1.173 sin enlace resuelto. **Un enlace no resuelto no significa que falte ese país en el mapa.** El propietario de una carpeta, un nombre parecido o la coincidencia de un punto no prueban equivalencia institucional ni cobertura territorial completa. Se conservan los candidatos y los polígonos presentes en el punto de referencia para investigar; no se fusionan países automáticamente. Estos pendientes también figuran en el dossier correspondiente.

Quedan abiertos el contraste local independiente, los desplazamientos, las subdivisiones omitidas y los contornos con fecha propia, incluidos pueblos para los que todavía no hay una geometría documentada incorporada. La revisión global es de conservación, disponibilidad, selección y evidencia de enlace; **no certifica un mapa étnico anual exhaustivo** ni valida por sí sola todos los límites de la compilación. El gris sigue significando falta de representación en las capas activas, nunca territorio vacío.

## Ejecución y continuidad

La consulta descarga sólo el segmento del siglo visitado y lo reutiliza al volver. Los once segmentos mantienen las mismas coordenadas y fases que el export completo; no reducen el detalle. Los originales canónicos permanecen dentro de `Países/<entidad>/poblamiento`. El export completo sirve para auditoría, no es una descarga inicial obligatoria de la aplicación.

No se modifican banderas, retratos ni autoridades en esta entrega. Una corrección del campo `entityType` de la fase cultural songhay posterior a 1591 lo hace coincidir con su `kind` ya existente; no cambia su geometría, fechas o interpretación histórica. La continuación del ámbito de la Unión de Kalmar se rotula como área histórica del testimonio de 1500, evitando presentarla como una unión política vigente en siglos posteriores. El estado de entrega y las comprobaciones finales se registran en [tareas.md](../tareas.md). La publicación remota la confirma el propietario, sin esperar Actions/Pages.
