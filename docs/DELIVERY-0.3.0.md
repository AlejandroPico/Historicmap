# Entrega 0.3.0 · Datos históricos y reproducción

## Resultado

El problema de 1942 procedía de seleccionar la instantánea más cercana entre 1914 y 1945: se mostraba un mundo posterior a la guerra. Se reemplaza esa selección por periodos activos de CShapes para cada año de 1900–2019, incluidas dependencias coloniales. Se incorporan 20 registros anuales de Alemania, Japón e Italia para 1938–1944, con la advertencia de que Cliopatria no fija un día uniforme dentro del año.

La navegación reciente avanza de año en año. La reproducción espera la carga y aplicación de cada estado antes de avanzar; los cambios de fecha comparten descargas y se descartan resultados antiguos. Durante una carga se mantiene el mapa anterior con su estado indicado. Pausa impide avances posteriores del reproductor. El año máximo se obtiene con el reloj del dispositivo.

El worker recibe altas, bajas y cambios de entidades por identificador mediante `updateData`, sin reenviar el mundo entero en cada paso. La elevación contemporánea se desactiva inmediatamente al pedir una época anterior. Las letras del mapa necesarias se sirven localmente (11 franjas Noto Sans, licencia OFL y huellas), eliminando esa dependencia del servidor de demostración externo.

Fichas: capital/sede, estatus histórico, potencia administradora, periodos, contexto específico y hasta seis indicadores WDI con año. Nunca se incorpora el PIB de la Rusia actual a la URSS. La misma ficha se abre al buscar o pulsar el territorio. Se añaden tres modos temáticos: PIB, PIB por habitante y población, además del color político. La leyenda distingue ausencia de datos y los años realmente utilizados.

Los lugares contemporáneos pasan de un marcador superviviente a 323 capitales y grandes ciudades. Para 1900–2019 se muestran capitales del registro histórico, no capitales actuales proyectadas retrospectivamente.

## Alcance de la revisión

[ANNUAL-REVIEW.md](ANNUAL-REVIEW.md) enumera cada año 1900–2026: fuente, registros activos, cambios y límites. Incluye contrastes focales de Alemania, India, Argelia, Egipto, Israel, Siria y Crimea. La auditoría automática por año no se denomina validación manual exhaustiva de todas las coordenadas.

**Límites materiales:** CShapes termina en 2019 y omite algunas ocupaciones y transferencias pequeñas. Desde 2020 se mantiene la base contemporánea importada en 2026, no siete instantáneas históricas verificadas. No hay frentes diarios, delimitación completa de los ocupantes de Polonia en 1939, frentes del Donbás/Ucrania 2022–2026, fases geométricas del Sinaí 1979–1981 ni Taba. El Sinaí y el Golán se distinguen como ocupaciones, Crimea como territorio ucraniano con ocupación y anexión reclamada por Rusia desde 2014. El detalle costero actual sigue siendo 1:10m.

## Datos y licencias

31 recursos registrados: 26 instantáneas conservadas, archivo temporal CShapes con 640 registros relevantes, 20 registros Cliopatria, cinco polígonos contextuales derivados, 323 ciudades y perfiles/series. Las licencias de los recursos permanecen separadas. CShapes y sus derivados requieren atribución, uso no comercial y compartir adaptaciones bajo CC BY-NC-SA 4.0. Cliopatria es CC BY 4.0; WDI utiliza CC BY 4.0 con términos adicionales del Banco Mundial. No se convierte la licencia del código del propietario.

## Verificación y publicación

Código publicado: **6952e1baf384bc0c75a59dcf7bf6dc2cff9cc882**.

- [Quality 39693996198](https://github.com/AlejandroPico/Historicmap/actions/runs/39693996198): correcto. Integridad de 31 recursos y 11 franjas de letras, **16 pruebas unitarias**, compilación y **9 recorridos de navegador** correctos sobre ese mismo commit. El registro de CI confirma nueve recorridos en 2,5 minutos.
- Se ha renderizado cada año 1900–2026, además de cartografía antigua/geológica; se comprueban reproducción/pausa, peticiones lentas y fechas obsoletas, controles, fichas, ciudades, economía, móvil y reloj simulado en 2028. El año de referencia contemporánea sigue indicado como 2026 incluso con ese reloj.
- [Publish atlas 39694346487](https://github.com/AlejandroPico/Historicmap/actions/runs/39694346487): construcción y publicación correctas después de Quality.
- [Web pública](https://alejandropico.github.io/Historicmap/#year=1942&view=mercator) comprobada: «Acerca de» muestra 0.3.0; 1942 muestra CShapes al 31 de diciembre con 169 territorios y la capa anual de extensión/ocupaciones. El manifiesto público coincide con las 31 huellas locales y el primer paquete de letras responde HTTP 200.
- Se comprobaron también los bytes preparados para Git, además de los locales: los datos JSON se escriben con LF explícito y los PBF se marcan binarios, evitando alteraciones de huellas entre Windows y Linux.

El cierre documental posterior usa `[skip ci]`: sólo registra estos resultados, sin cambiar la aplicación validada/publicada.
