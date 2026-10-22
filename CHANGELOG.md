# Historial de versiones

## 0.5.0 · 2026-10-22

- Corregida la identidad española que se aplicaba a otros países al comparar identificadores vacíos. Corregida también la sobrescritura de Brasil, Francia, Australia y Kazajistán por metadatos de territorios asociados.
- Ficha de país a la izquierda, con pestañas Autoridades, Datos, Contexto y Conflictos. Se listan los mandatos que coinciden con el año, incluidos relevos breves y jefaturas de Estado/Gobierno.
- Fotografía oficial completa de la primera ministra de Mozambique, con atribución y licencia no comercial/sin derivados, conservando el encuadre original.
- Ampliación mundial de fotografías locales y contraste de autoridades de 2026 con ONU y fuentes nacionales; cobertura y excepciones auditadas en CURRENT-AUTHORITIES.
- Mañana, tarde, noche y automático en un botón cíclico; hora local del dispositivo, preferencia conservada y océanos más claros que el fondo.
- Relieve apagado de inicio y disponible como referencia en periodos históricos desde 10.000 a. C.; excluido de reconstrucciones geológicas.
- Eliminado Explorar épocas y el rótulo de escala adaptativa. Leyenda a la derecha, atribución/escala a la izquierda y fuentes en un panel compacto sin fondo modal.
- Capas 2026 de OTAN, UE, BRICS y Tres Mares; categorías separadas y fuentes oficiales. Rampa económica verde y contextos parciales de conflictos con fuentes.
- Pruebas de regresión con clic cartográfico en Brasil 1947 después de consultar un bando español, claves de territorios, pestañas, temas y alcance temporal de membresías.

## 0.4.0 · 2026-10-22

- Cronología anual ampliada a 1789: componentes Cliopatria 1789–1885 y todos los registros CShapes desde 1886, sin retrotraer un mapa futuro por cercanía. Inventario de 238 selecciones hasta 2026.
- Control territorial opaco por potencia, con Alemania nazi gris, URSS roja, Estados Unidos azul y familias políticas diferenciadas. Colores de regímenes franceses y españoles; dependencias, aliados, ocupación y gobiernos clientes separados.
- Extensiones de ambas guerras mundiales, regímenes de Croacia y Vichy y control comunista chino. Hungría aliada no se equipara a Hungría ocupada en 1944.
- Guerra Civil española: dos bandos en 1936/1937/1938 y resultado de 1939. Frente de octubre de 1937 georreferenciado con fuentes, atribución e incertidumbre; sin interpolación de provincias.
- Fichas integradas con bandera histórica, nombre, autoridades y retratos reales con licencia. Series focales de EEUU, España, Alemania, URSS y Francia, y catálogo global de mandatos con cobertura desigual. No se asignan dirigentes actuales a periodos sin documentación ni banderas de RFA/RDA a la ocupación anterior a 1949.
- Búsqueda de bandos y áreas controladas, fichas comunes a búsqueda/clic y tratamiento de mandatos repetidos. Metadatos e imágenes locales, sin llamadas a Wikidata/Commons al navegar.
- Fuentes y fichas extraídas a módulos propios; pruebas geográficas, de identidades, de periodos, integridad de medios y navegador. Límites y continuación documentados.

## 0.3.0 · 2026-10-22

- Selección por intervalos de vigencia para 1900–2019, con CShapes 2.0: colonias, protectorados, mandatos, administradores y capitales históricas. 1942 deja de seleccionar el mapa de 1945.
- Capa anual de extensión territorial de Alemania, Japón e Italia en 1938–1944, a partir de Cliopatria; sin atribuirle una fecha diaria uniforme.
- Polígonos contextuales de Sinaí, Golán y Crimea que distinguen ocupación y soberanía; límites y fases pendientes explicados.
- Reproducción reciente anual que espera la carga, comparte descargas y conserva el mapa anterior mientras carga. Pausa invalida la continuación pendiente.
- Año máximo obtenido del dispositivo; referencia contemporánea desde 2020 identificada como tal, sin inventar verificación anual o conocimiento futuro.
- Fichas ampliadas: capital, estatus, administración, contexto y seis indicadores WDI con su fecha. Sin cifras actuales proyectadas retrospectivamente.
- Capas de PIB total, PIB por habitante y población con leyenda y años observados.
- 323 capitales y grandes ciudades actuales, y capitales históricas por periodo.
- Informe anual de cobertura, cambios y pendientes, con pruebas históricas y de reproducción.

## 0.2.0 · 2026-10-22

Rediseño del espacio de exploración y de los controles.

- Eliminadas la cabecera permanente, las franjas superior e inferior de la regla y los controles laterales de zoom/restablecimiento.
- Herramientas compactas en la esquina superior derecha: búsqueda, cambio 2D/3D con un único botón, capas, base de datos/fuentes, pantalla completa e información.
- Capas en un panel desplegable con cierre por Escape o al pulsar fuera.
- Fecha seleccionada y reproducción/saltos reunidos en el centro fijo de la regla.
- Rueda sobre la regla para ampliar/reducir su escala sin cambiar la fecha; la rueda sobre el mapa conserva su zoom geográfico.
- Marcas temporales adaptadas al zoom y a la ventana visible, con navegación por arrastre y teclado.
- «Acerca de» con favicon, identidad, ficha de versión, historial, portfolio confirmado y repositorio, siguiendo la estructura de los proyectos del autor.

## 0.1.0 · 2026-10-21

Primera base funcional del atlas temporal.

- Mapa Mercator y globo con cartografía vectorial, selección, zoom y búsqueda.
- Regla móvil con cursor fijo, escala adaptativa, fechas, épocas y reproducción.
- 26 instantáneas con procedencia, licencias y verificación SHA-256.
- Contexto, fuentes, metodología, versión e historial.
- Relieve actual y tres lugares introductorios.
- Diseño adaptable, navegación por teclado y enlaces compartibles.
- Documentación de continuidad y flujos de validación/publicación.
- Teselación subpíxel para evitar exceder límites GPU en costas densas; comprobación de renderizado de todas las instantáneas.
- Movimiento de regla con marcas reutilizadas y sincronización limitada del enlace compartible para mantenerlo correcto durante la reproducción.

Cobertura inicial discontinua. Alta resolución local, revisión historiográfica exhaustiva, homininos, hielo, atmósfera y eventos bélicos pendientes. Ver `agentes.md`.
