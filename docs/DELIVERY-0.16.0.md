# Entrega 0.16.0 · ampliación hasta 1820

El propietario solicita ampliar 1820–1839 y posponer las correcciones de huecos anteriores. Se reutilizan los preparadores para reducir el trabajo repetido; el envío termina al confirmar GitHub, sin esperar Actions/Pages.

## Datos y comportamiento

- Adquisición aislada y cargos históricos explícitos; 492 claves y 12.621 registros de mandatos en el catálogo completo. Se conservan los hechos anteriores de 1840+, sin afirmar que todas las series estén completas.
- Distinción entre sucesiones británicas, minoría de Isabel II y regencia de María Cristina, regencias brasileñas y el Primer Imperio mexicano. Se rechazan el título honorífico brasileño de Juan VI y una fecha sarda errónea. Las fechas gregorianas rusas no se duplican con las julianas.
- 95 imágenes adicionales con licencia, 6.149 medios en total. Reutilización de símbolos ya acreditados y pintura de Victoria de 1838 disponible desde ese año; fecha de imagen distinta de fecha de mandato. No se generan retratos ficticios para órganos colectivos.
- Catorce fases de contexto y sus registros de ficha; tres enlaces completos de transición. Los contextos Qing usan QNG, las identidades QING.
- Resolución histórica desde 1820 y referencias locales del Pacífico; los componentes geográficos originales se retiran del agregado antes de hacerse seleccionables, conservando coordenadas. Las relaciones coloniales posteriores no se proyectan sobre los tramos locales anteriores.

## Fuentes y preparación

Los candidatos y declaraciones se conservan en `scripts/historical-offices-016-research.json`. Wikidata aporta metadatos CC0; las imágenes tienen licencias y huellas independientes. La geometría continúa procediendo de Cliopatria. Los preparadores específicos de 1820 y `register-016-data.mjs` registran transformaciones y recursos; no se descarga información al compilar.

Contrastes institucionales: [Asamblea Nacional francesa](https://www.assemblee-nationale.fr/dyn/histoire-et-patrimoine/monarchie-de-juillet/l-insurrection-des-trois-glorieuses), [Trienio Liberal](https://www.congreso.es/en/web/guest/cem/trielib), [regencia española](https://www.congreso.es/en/web/guest/cem/regmcris), [Senado brasileño](https://www12.senado.leg.br/senado200anos/passado), [independencia belga](https://www.belgium.be/en/about_belgium/country/history/belgium_from_1830), [Archivo General de la Nación mexicano](https://www.gob.mx/agn/articulos/agnrecuerda-al-primer-imperio-mexicano), [Parlamento portugués](https://app.parlamento.pt/publicacoesonline/palacio.pdf), [National Archives sobre la doctrina Monroe](https://www.archives.gov/milestone-documents/monroe-doctrine) y [desplazamiento indígena](https://www.archives.gov/milestone-documents/jacksons-message-to-congress-on-indian-removal), [guerra anglo-afgana](https://www.nam.ac.uk/explore/first-afghan-war) y [guerra del Opio](https://www.nam.ac.uk/explore/first-china-war-1839-1842).

## Cobertura pendiente

**La ampliación documental no es una revisión mundial exhaustiva.** El inventario anual contiene 3.234 entidades/año, con 2.183 casos anuales sin autoridad documentada, 20 personas u órganos sin retrato y 2.799 casos anuales sin símbolo. Nombres concretos en [REVIEW-1820-1839.json](REVIEW-1820-1839.json); continuidad en [tareas.md](../tareas.md).

El contorno Gran Colombia que persiste en la fuente hasta 1833 queda rotulado como pendiente después de 1830; no acredita continuidad de la unión. La etiqueta griega tampoco fecha correctamente todas las transiciones a la monarquía. Faltan mejores geometrías sucesoras, autoridades locales, pretendientes carlistas y frentes militares. No se han añadido polígonos modernos para simular su resolución. Las observaciones interiores anuales no equivalen a fechas diarias de acceso o cese.

## Verificación

170 pruebas en 40 archivos correctas; se comprueban todos los años de la nueva franja, identidades y sucesiones focales. Tipos y compilación correctos. Un recorrido de navegador pasa en 1,1 minutos: Francia1820/1830, España1833, México1822, Qing1839→1840, globo y móvil. Para evitar una copia completa repetida de estáticos se compila con la configuración vigente, desactivando sólo su copia para la vista previa y sincronizando los recursos modificados. La integridad de todos los datos y medios se comprueba por separado. No se repite toda la batería de navegador ni se comprueba el despliegue público, que queda a cargo del propietario.
