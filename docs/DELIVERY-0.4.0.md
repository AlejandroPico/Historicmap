# Entrega 0.4.0 · 22 de octubre de 2026

## Realizado

- Cronología anual desde 1789: 1.715 registros componentes Cliopatria hasta 1885 y todos los 710 registros CShapes desde 1886. Informe de 238 selecciones 1789–2026, con huellas y límites, sin considerarlo revisión manual integral de cada coordenada.
- Control territorial opaco y colores por régimen/potencia; territorios normales al desactivar la capa. Alemania nazi gris, URSS roja, EEUU azul y familias/regímenes diferenciados. Croacia/Vichy distinguidos de los aliados; Hungría ocupa una situación distinta en 1944.
- 57 registros de control de ambas guerras mundiales y China. Guerra Civil española: siete registros 1936–1939, con frente de octubre de 1937 georreferenciado y dos fichas de bando; resultado de 1939 con la autoridad franquista.
- 267 claves de identidad, 2.859 registros de autoridades, 374 intervalos de símbolos; 417 medios locales con licencia y huella (342 banderas/símbolos, 75 retratos). Presidencias reales y autoridades rivales; sin dirigentes actuales retrotraídos ni fotografías inventadas. Ocupación alemana anterior a 1949 diferenciada de RFA/RDA.
- Fichas y metodología en módulos propios; fechas, fuentes, autoría y licencias visibles. Se conservan economía, ciudades, relieve, globo, regla y controles compactos.

## Validación local

- 35 recursos de datos, 11 franjas de letras y 417 medios con SHA-256, procedencia, referencias e intervalos verificados.
- 31 pruebas unitarias correctas: cronología, geometría, historia, perfiles, colores, identidades, sucesión y bandos. El preparador español verifica particiones válidas/no superpuestas y Madrid, Barcelona, Bilbao, Gijón y Málaga.
- Recorrido completo de 11 pruebas de navegador correcto, incluyendo **cada uno de los 238 años**, fuentes compartidas sin descargas repetidas, GPU, reproducción/pausa, peticiones lentas, economía, móvil, geología y controles. Ejecutado sobre compilación de producción; después se ajustaron prioridad de autoridades, atribución completa de medios, leyenda y bloqueo de selección durante cargas. Compilación final correcta y repetición focal de las dos nuevas pruebas de navegador correcta tras esos ajustes (banderas/autoridades, ocupación, Guerra Civil, 1789/1812, sucesión estadounidense y ficha española móvil).

## Límites explícitos

No son fronteras/frentes diarios ni una validación mundial exhaustiva. España 1937 corresponde a octubre, con incertidumbre mínima de registro de 10 km; 1936/1938 son síntesis anuales sin día uniforme. Faltan campañas mensuales, territorios coloniales e insulares españoles completos, cuatro zonas aliadas individuales/Berlín, muchos frentes y administraciones, guerra civil rusa y control efectivo reciente. La cobertura de autoridades y símbolos es desigual, y los retratos no representan necesariamente la edad de la persona en cada año. El detalle y prioridades constan en IDENTITIES, SPANISH-CIVIL-WAR, REVIEW-METHOD, ANNUAL-REVIEW y agentes.md.

## Publicación

Código final publicado: **681f71e040d8b7d07677f30b3189f50bfdf4f44d**, tras la entrega principal f62685dc1103aeff443b010c48001522845b8f02. La revisión final ajusta las transiciones republicanas alemanas de 1918, colores franceses (Consulado/Imperio y Monarquía de Julio desde 1830) y el enlace de España/Primera República/imperio colonial con su identidad.

- [Quality 39719656269](https://github.com/AlejandroPico/Historicmap/actions/runs/39719656269): **correcto sobre el SHA final**. Logs del job 119629933286: 35 recursos, 11 franjas y 417 medios íntegros; **31 pruebas unitarias y 11 pruebas de navegador correctas** (6,6 minutos de navegador), compilación correcta.
- [Publish atlas 39720348133](https://github.com/AlejandroPico/Historicmap/actions/runs/39720348133): **correcto**. El log de build confirma checkout de 681f71e y archivo `assets/index-BSZARU0D.js`.
- Comprobación pública: la página sirve ese mismo archivo final, versión visible 0.4.0; manifiesto remoto idéntico a las **35 huellas** locales. Comprobadas por HTTP cuatro banderas/retratos históricos, con huellas idénticas, y visualmente el mapa de 1942 con 169 territorios, ocupación opaca, bandera auténtica y retrato acreditado. La revisión de España 1937 y móvil se comprobó localmente y en los recorridos de CI.

La primera publicación de esta entrega usó el commit principal mientras la corrección final terminaba Quality; esta segunda ejecución es la comprobación de cierre. No confundir el `head_sha` del evento de Pages con el checkout validado: los logs y el archivo servido acreditan la revisión final. El commit posterior de documentación usa `[skip ci]`, sin modificar la aplicación validada.

## Continuación

Priorizar contraste regional de fronteras/control y cobertura de autoridades; completar límites concretos antes de anunciar precisión mundial. La futura categoría de guerras y batallas necesitará eventos propios con actores, intervalos y precisión geográfica, sin inferir batallas de cambios de color.
