# Pueblos y regiones · revisión1900–presente · 0.31.0

La entrega anterior terminaba la consulta cultural en1905. Esta revisión conserva las fases900–1905 y mantiene disponibles los **1.769 contextos culturales/geográficos** de aquel horizonte durante1906–2027. El mapa político, sus fronteras, autoridades, símbolos e indicadores siguen siendo independientes. Se revisan las128 selecciones1900–2027;2027 es un horizonte de consulta de evidencia ya conocida, **no una observación futura**. El máximo navegable continúa siendo el año del dispositivo: en2026 no se adelanta artificialmente a2027.

## Qué se incorpora

- **1.782 fases nuevas** dentro de1.769 dossiers existentes de `Países`, sin nuevos polígonos o traslados manuales. Total:6.657 dossiers y8.597 fases. No son cifras de pueblos independientes o Estados.
- Se conserva la selección cultural al cambiar de año o de fuente, también al pasar a la cartografía contemporánea en2020. Búsqueda y «En este lugar» permiten consultar la referencia cultural bajo el país; la selección política tiene prioridad.
- Las **49 referencias a poderes políticos** activas en1905 no se prolongan automáticamente. La continuidad de un pueblo no significa que siga existiendo su antiguo reino. La Unión de Kalmar permanece identificada como un área histórica de un testimonio de1500, no como una unión vigente.
- Las fichas nuevas muestran la revisión documental de28/10/2026, el año de la geometría fuente y las limitaciones de la evidencia. En2027 aparece un aviso explícito de ausencia de observaciones futuras.
- Doce segmentos activos por siglo, incluido2000–2027, con las mismas coordenadas y fases que el export completo. El antiguo segmento1900–1905 conserva su URL y huella como recurso archivado; el navegador utiliza1900–1999. No se elimina evidencia al ampliar el horizonte.

## Referencia histórica y presencia contemporánea

Las superficies conservadas son **referencias tradicionales o históricas**, no un mapa anual de distribución de población. No prueban residencia constante, títulos territoriales, una reserva, soberanía o límites actuales. Una parte de la evidencia mantiene denominaciones arqueológicas y áreas generales, por lo que tampoco se afirma que todas esas identidades continúen sin transformación hasta el presente. Se conserva su consulta histórica y se marca el contraste contemporáneo como pendiente.

Las fuentes espaciales siguen siendo las compilaciones acreditadas previamente, con sus originales y licencias dentro de la entidad correspondiente. No se dibujan nuevas fronteras a partir de una noticia, una ley o la similitud de nombres. Tampoco se sustituye un territorio tradicional por el área de una administración moderna. Por ejemplo, [AIATSIS](https://aiatsis.gov.au/explore/map-indigenous-australia) distingue ubicaciones generales de límites fijos y advierte que su mapa no sirve para reclamaciones de títulos. Se consulta como criterio metodológico, sin reproducir su cartografía.

Los registros sin contraste local conservan `historical-reference-current-extent-unverified`. Los nueve contextos focales con continuidad institucional o cultural contrastada usan `current-continuity-spatial-extent-unverified`: ese contraste tampoco valida el polígono como extensión contemporánea. Los pendientes se guardan en las fases y en `modernConsultationReview` de cada dossier, no en una lista de hechos paralela dentro del código.

## Hitos fechados y alcance

| Referencia | Hitos y distinciones | Fuente |
|---|---|---|
| Pueblos sámi | Delegación finlandesa1973–1995; Parlamento desde1996, tras reforma constitucional de1995; reforma legal en vigor desde1/8/2025. Estos hechos finlandeses no se extrapolan al conjunto deSápmi. | [Parlamento Sámi](https://samediggi.fi/en/the-sami-parliament/), [comunidades y lenguas](https://samediggi.fi/en/about-us/) |
| Aotearoa | Tribunal deWaitangi desde1975; ampliación en1985 para investigar actuaciones desde1840. La fecha de competencia no es la fecha del hecho investigado; no es un gobierno único de todos los iwi y hapū. | [Waitangi Tribunal](https://waitangitribunal.govt.nz/en/about/about-the-waitangi-tribunal/about-the-waitangi-tribunal) |
| Comunidades ainu | Promoción cultural desde la ley1997; reconocimiento legal indígena en la ley vigente desde24/5/2019. El reconocimiento no es el origen del pueblo ni crea una frontera estatal. | [Library of Congress](https://www.loc.gov/item/global-legal-monitor/2019-08-05/japan-new-ainu-law-becomes-effective/) |
| Inuit | Nunavut desde1/4/1999. InuitNunangat incluye cuatro regiones canadienses; no equivale sólo aNunavut ni al conjunto circumpolar. La geometría conservada no es un límite administrativo deNunavut. | [ITK](https://itk.ca/inuit-land-area-coastline-freshwater/), [atlas indígena deCanadá/ITK](https://indigenouspeoplesatlasofcanada.ca/article/itk-faqs/) |
| Comunidades métis | Artículo35 de la Constitución canadiense1982: reconocimiento junto aFirstNations e inuit, sin convertir esa disposición en un polígono único. | [JusticeCanada](https://www.justice.gc.ca/eng/csj-sjc/ijr-dja/35pedia-wiki35/p2.html?wbdisable=true) |
| Mapuche/Wallmapu | Ley19253 publicada enChile el5/10/1993. No se aplica automáticamente al lado argentino ni demuestra una jurisdicción uniforme sobre todo el ámbito tradicional. | [Biblioteca del Congreso deChile, texto original](https://www.bcn.cl/leychile/Navegar?idNorma=30620&idParte=8639941&idVersion=1993-10-05) |
| Burarra | Mabo1992 es un hito australiano originado en el caso de losMeriam; no una determinación de títulos burarra. La ley1993 entra en vigor el1/1/1994 y no sustituye los expedientes de cada comunidad. | [Attorney-General](https://www.ag.gov.au/legal-system/native-title) |
| Cherokee | Distinguir ámbito histórico, comunidades, reservas y las actuales naciones o jurisdicciones. El reconocimiento federal no es sinónimo de cultura o de reserva. | [IndianAffairs](https://www.bia.gov/frequently-asked-questions) |

Las fases consultan hechos documentados del año, sin retrotraer instituciones posteriores. Los contextos y las fuentes conservan su ámbito: una reforma deFinlandia,Canadá oChile no se convierte en una norma universal ni en fecha de nacimiento de una cultura.

## Revisión mundial y pendientes

La [auditoría anual](CULTURAL-MODERN-ANNUAL-REVIEW.json) registra las selecciones1900–2027 usando la base histórica hasta2019 y la referencia contemporánea desde2020, igual que la aplicación. Comprueba disponibilidad de los contextos, prioridad política y conservación de los datos. El [inventario de ampliación](CULTURAL-EXTENSION-1906-2027.json), el [inventario acumulado](CULTURAL-REVIEW-900-2027.json) y la [conservación](CULTURAL-VALIDATION-0.31.json) distinguen comprobación técnica de contraste histórico independiente.

Las áreas africanas, asiáticas, americanas y deOceanía conservadas siguen consultables aunque cambien los Estados que las abarcan. Esto no resuelve por sí solo sus desplazamientos, diásporas o subdivisiones. El [informe de la Comisión Africana de2005](https://searchlibrary.ohchr.org/record/6703), el [Convenio169 de1989, en vigor desde1991](https://treaties.un.org/Pages/showDetails.aspx?objid=08000002800c0136) y la [Declaración de laONU de2007](https://www.un.org/development/desa/indigenouspeoples/declaration-on-%20the-rights-of-indigenous-peoples.html) son referencias de investigación institucional, no fuentes de nuevos polígonos ni reconocimiento uniforme para todos los grupos del inventario. Sus ámbitos, ratificaciones y efectos requieren registros propios antes de convertirlos en filtros o derechos por entidad.

No se certifica un censo cultural contemporáneo exhaustivo. Quedan pendientes la investigación local de las áreas no contrastadas, las geometrías fechadas de migraciones y desplazamientos y la revisión de los enlaces políticos inventariados en0.30. La revisión no añade nuevos frentes bélicos ni renueva presidentes, fotografías o estadísticas: esas capas mantienen sus propias fechas y fuentes, sin modificaciones en esta entrega.

## Continuación anterior a900

El siguiente encargo volverá a las regresiones anteriores a900. Se conserva como requisito la coexistencia de sociedades, tradiciones arqueológicas, pueblos, áreas de poblamiento y poderes políticos, sin imponer Estados a sociedades que no los tenían. Expansión humana, ciclos glaciales, cambios del nivel del mar, atmósfera y extinciones deberán tener cronologías científicas y evidencias propias. No se convierten en una lista ya validada de «13 glaciaciones» ni se dibujan en esta entrega. El plan y el estado operativo siguen en [tareas.md](../tareas.md).
