# Fichas de investigación · versión 0.7.0

## Uso

La ficha se abre al seleccionar un territorio en el mapa o el buscador. Conserva su entidad y apartado al cambiar de fecha, incluidos reproducción, regla, saltos y diálogo de año. Durante las cargas muestra el destino solicitado y mantiene el año anterior junto a su contenido; cuando la carga termina se actualizan juntos. Un fallo no cambia silenciosamente la fecha de la ficha.

Sus doce apartados son Autoridades, Territorio, Instituciones, Sociedad, Economía, Relaciones, Defensa, Historia, Datos, Contexto, Conflictos y Comparar. Todos usan la misma selección temporal. Los paneles de búsqueda, fuentes y capas también se conservan durante la navegación por años; los cierres explícitos y los clics ajenos a la navegación siguen funcionando.

Las entidades desaparecidas permanecen abiertas con ausencia de representación activa. No se elige automáticamente un sucesor ni se copian sus autoridades/estadísticas. Historia ofrece enlaces documentados a entidades relacionadas. Las capitales conservan identidad entre fuentes aunque cambie el idioma del país; un lugar no presente en la capa recibe una explicación de ausencia.

## Comparar

**Entre fechas:** introducir A y B y pulsar Comparar fechas. Intervalo cartográfico político de −10000 al año del dispositivo, sin año cero. Se muestran las autoridades de los mandatos que cruzan cada año, bandera de su referencia, estatus y capital cuando existen, magnitudes fechadas y diferencia B−A. Una diferencia entre porcentajes se expresa en puntos porcentuales. La igualdad de contornos se refiere a las geometrías disponibles, no a una certificación histórica exhaustiva. Los botones Ver en el mapa alternan fechas conservando el apartado.

**Entre países:** Fijar para comparar añade la entidad a una selección de hasta cuatro. Seleccionar otros países en mapa/buscador y fijarlos. Se comparan todos en el año actual del mapa; cada entidad puede quitarse y la selección puede vaciarse. La entidad abierta se añade a las fijadas mientras haya espacio. Una entidad ausente en ese año se identifica sin valores de sucesores. Las fijaciones duran la sesión y sobreviven al cierre de ficha y cambios de fecha; recargar reinicia el estado.

Las tablas tienen desplazamiento horizontal interno en pantallas estrechas. Cada observación conserva su año; un cambio calculado sobre observaciones de años distintos no se etiqueta como variación anual medida. Las revisiones de WDI y los cambios del territorio estadístico pueden limitar comparaciones.

## Cronología y evolución

Historia reúne comienzos de mandatos, símbolos, relaciones organizativas, conflictos, transiciones y relaciones entre entidades. Se puede filtrar por tipo y ampliar la lista inicial. Por defecto sólo muestra registros hasta el año del mapa; la opción de incluir posteriores es explícita. Una fecha de inicio de cobertura conserva esa nota y no se convierte en fundación o adhesión. Pulsar la fecha navega al mapa.

Economía, Sociedad y Defensa permiten elegir indicadores y muestran evolución histórica, puntos navegables por ratón/teclado, tabla de observaciones y fuente. Las líneas se interrumpen cuando faltan años; no hay interpolación. Los gráficos no proyectan valores futuros ni extrapolan hacia atrás. Las cifras de resumen usan la última observación anterior o igual al año elegido, con hasta cinco años de antigüedad. Los gráficos sí pueden mostrar observaciones más antiguas con su fecha.

## Modelo de ampliación

- `selection.ts`: ancla de entidad separada de los IDs de periodos/cartografía; nombres de capital normalizados e identidad territorial.
- `country-card.ts`: apartados y presentación integrada de fuentes, autoridades, métricas y registros.
- `country-workspace.ts`: catálogo de indicadores, series, signos, observaciones, formato y gráficos accesibles.
- `country-history.ts`: registros fechados, relaciones dirigidas y cronología.
- `country-comparison.ts`: selección de comparación y representación de instantáneas; `main.ts` resuelve geometrías, conserva la interfaz y descarta resultados obsoletos.

`CountryRecord` admite apartados `institutions`, `history`, `territory`, `society`, `economy`, `defense` y `relations`. Cada registro tiene claves de entidad, inicio inclusivo, fin exclusivo opcional, título, texto y fuente. Los campos opcionales `fields` admiten etiqueta, valor, unidad, fecha de observación y fuente; `places` admite nombre, longitud, latitud, nota y fuente, con acción para centrar el mapa. No atribuir una fecha de vigencia general a observaciones individuales que tienen otra referencia.

Esta estructura permite ampliar constituciones, parlamentos, elecciones y coaliciones; idiomas, religiones, educación y migraciones; recursos, sectores y comercio; organizaciones, acuerdos y sanciones; efectivos, gasto con permiso de redistribución, bases y servicio militar; e historia, símbolos y patrimonio. Su adquisición debe conservar precisión, fechas y licencias. Los apartados de texto actuales son una selección, no un inventario mundial de esos campos.

## Datos y alcance

Hay seis indicadores anteriores y 22 nuevos, 175.996 observaciones adicionales (217 economías, 1960–2025), 33 relaciones y 28 registros nuevos (15 institucionales, 12 históricos y uno territorial). Fuentes y cobertura en COUNTRY-INDICATORS y COUNTRY-HISTORY. El gasto SIPRI no se redistribuye; personal militar termina en 2020. No hay estimación de poder militar actual. Las 493 personas u órganos sin imagen del periodo anterior siguen pendientes.

La extensión de la interfaz no acredita que todos los países y años tengan datos completos. Persisten los límites de geometrías y control efectivo de versiones anteriores. Los mapas comparados conservan las fuentes disponibles para cada fecha; no se dibujan frentes o cambios de frontera para que las comparaciones parezcan más detalladas.
