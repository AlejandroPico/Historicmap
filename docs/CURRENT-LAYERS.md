# Agrupaciones y contextos de referencia de 2026

Consulta: **22 de octubre de 2026**. Implementación: `src/current-affiliations.ts`. Se transcriben hechos de pertenencia, con redacción propia y enlaces primarios; no se redistribuyen logotipos, mapas ni textos completos de las organizaciones. Las listas son datos estáticos locales, sin peticiones al proveedor durante la navegación.

| Capa | Categorías incorporadas | Fuente primaria |
| --- | --- | --- |
| OTAN | 32 Estados miembros | [Lista oficial de la OTAN](https://www.nato.int/cps/en/natohq/nato_countries.htm), contrastada con el [informe anual de 2025 publicado en 2026](https://www.nato.int/content/dam/nato/webready/documents/publications-and-reports/annual-reports/sgar25-en.pdf). |
| Unión Europea | 27 Estados miembros | [Oficina de Publicaciones, EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=LEGISSUM%3Amember_states), revisión de 15/09/2025; [Consejo de la UE, exposición de 2026](https://www.consilium.europa.eu/media/dpwbgt0f/2026-mobile-expo-cyprus-en.pdf). |
| BRICS | 11 miembros y 10 países socios, separados | [Gobierno de India, presidencia de BRICS, 10/09/2026](https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2308611&lang=2&reg=48); [Presidencia sudafricana, septiembre de 2026](https://www.gov.za/news/media-advisories/visits-foreign-countries/president-cyril-ramaphosa-participates-18th-brics). |
| Iniciativa de los Tres Mares | 13 miembros, 4 participantes asociados y 6 países socios estratégicos | [Declaración de Dubrovnik, 28–29/04/2026, Gobierno de Croacia](https://vlada.gov.hr/UserDocsImages/Vijesti/2026/Travanj/28_travnja/Political_Declaration_of_the_11th_Three_Seas_Initiative_Summit.pdf); [Ministerio de Exteriores de Polonia](https://www.gov.pl/web/diplomacy/three-seas-initiative2). |

BRICS incluye a Arabia Saudí como miembro siguiendo las fuentes oficiales de la presidencia india de septiembre de 2026. La página del Banco de Rusia aún describe al país como invitado; se conserva esta discrepancia de publicación aquí y no se mezclan ambos inventarios. Los diez socios son Bielorrusia, Bolivia, Cuba, Kazajistán, Malasia, Nigeria, Tailandia, Uganda, Uzbekistán y Vietnam; no se confunden invitaciones propuestas con aceptación.

La declaración de Tres Mares incorpora a Italia como nuevo socio estratégico en 2026. Los otros cinco países socios son Alemania, Japón, España, Turquía y Estados Unidos. La Comisión Europea también es socio estratégico, pero es una institución y no un polígono nacional. Ucrania, Moldavia, Albania y Montenegro son participantes asociados, distintos de los trece miembros. Tres Mares es una plataforma de cooperación regional e infraestructuras; BRICS es un foro intergubernamental de cooperación. Ninguno se presenta como un tratado de defensa equivalente a la OTAN.

## Intervalos y representación

Las listas se aplican **exclusivamente al año consultado 2026**. No se proyectan sobre 2025 ni sobre un reloj de 2027; al ampliar la serie habrá que adquirir y fechar nuevas observaciones. No son listas comprobadas para cada día del año ni una reconstrucción de ampliaciones históricas. El color neutral significa «Otros territorios», no «país neutral», «sin alianzas» ni «en paz».

Las claves son ISO alpha-3 de cada Estado, sin herencia automática desde la potencia soberana a territorios dependientes. La cobertura geográfica sigue los polígonos de la base contemporánea del proyecto; no se redefine el alcance jurídico territorial de los tratados. Las membresías simultáneas se exploran en capas separadas, evitando que una agrupación oculte pertenencias a las demás.

## Contextos de conflictos

Se añaden siete contextos breves y fechados: guerra de Rusia contra Ucrania; hostilidades Irán–Estados Unidos–Israel; Gaza y Cisjordania; Sudán; Myanmar; este de la República Democrática del Congo; Yemen. Cada nota enlaza una declaración o un informe primario de ONU/OCHA/ACNUR/UNICEF o de la cumbre de Tres Mares. No se reproducen cifras volátiles ni se dibujan frentes a partir de estos informes.

Este inventario es **parcial**: una ficha sin nota no acredita ausencia de conflicto. Tampoco clasifica jurídicamente a todos los participantes ni implica que todo el territorio de un Estado sea zona de combate. No se usa para asignar una capa mundial binaria de guerra/paz. Los contextos quedan restringidos a 2026, incluida la planificación humanitaria de Myanmar para ese año publicada en diciembre de 2025; la fecha de publicación se conserva separada del año al que se refiere.

## Gasto y capacidad militar

La [base de gasto militar de SIPRI](https://www.sipri.org/databases/milex), consultada en octubre de 2026, ofrece series 1949–2025 y explicita restricciones para uso comercial. No se incorpora una copia ni se supone que una vía intermedia elimine esas restricciones. Una futura capa deberá resolver los términos aplicables, unidades, año de observación y valores ausentes. El gasto militar por sí solo no constituye una medida de «fuerza militar» ni una clasificación de probabilidad de victoria.

## Validación

`tests/current-affiliations.test.ts` comprueba los recuentos, la separación de categorías, la ausencia de duplicados, códigos ISO, miembros incorporados recientemente, exclusión del Reino Unido de la UE y no herencia de Dinamarca a Groenlandia. También comprueba que el inventario de 2026 no se usa en años anteriores/posteriores y que la pertenencia a una alianza no genere automáticamente una nota de conflicto.
