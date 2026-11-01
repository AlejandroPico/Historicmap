# Entrega 0.51.0 · 1 de noviembre de 2026

Áreas humanas fechadas hasta unos 7 Ma, referencias fósiles y arqueológicas conservadas, regiones compartidas seleccionables, hielo automático y océanos azules. Los paneles y controles de tarde mantienen sus tonos ocres; la noche conserva sus colores anteriores.

## Datos y alcance

- 35 entradas taxonómicas/genéticas: 24 con áreas y 11 alternativas o atribuciones discutidas sin otra población pintada. 50 ventanas regionales, 66 fases según costa. Son envolventes editoriales aproximadas, no fronteras biológicas publicadas, densidades o ocupación uniforme.
- 2820 registros humanos anteriores intactos; 1000 intervalos adicionales (18 referencias tempranas y 982 porciones anteriores de Timmermann2022), con filas, edades, atribuciones y fuentes. 1152 claves de referencia distintas en conjunto; no equivalen a igual número de lugares físicos certificados.
- Seis originales CAO2024 de 2–7 Ma y sus derivados, sin simplificar coordenadas; se reutiliza la referencia 1 Ma. Coordenadas fósiles actuales, sin rotación individual de placa. Costas modeladas no equivalen a paleocostas por nivel del mar.
- Hielo automático/manual con las 23 muestras PaleoMIST anteriores hasta 80000 BP1950. Umbral editorial de exceso de área; no nueva datación de glaciaciones. LR04 aporta contexto isotópico hasta 5,32 Ma; no se convierte en superficie glacial.

[Método y fuentes](RESEARCH-HUMAN-DISTRIBUTIONS.md) · [catálogo natural](../Tierra/Humanidad/INDICE.md) · [conservación](CONSERVATION-0.51.0.json).

## Comprobaciones locales

- **Datos:** 283 recursos de datos, 11 rangos de glifos y 9179 medios verificados por SHA-256. Las 272 entradas anteriores del manifiesto permanecen idénticas, incluidos 217 GeoJSON. Sin modificaciones en archivos previamente registrados de Países/Tierra. Originales CAO cotejados por hash y todas las geometrías derivadas comparadas con sus coordenadas originales.
- **Reproducción:** compilador ejecutado de nuevo con `--check`, sin escribir archivos; todos sus productos coinciden byte a byte. No depende de archivos privados de caché para obtener sus entradas.
- **Pruebas generales:** ejecución inicial de 384 casos: 383 correctos y una auditoría global agotó su tiempo al coincidir con carga de navegador local. Se repitió aislada junto con las pruebas focales: 30/30 correctas, incluidos sus cinco casos. No se elevó su límite ni se retiró la auditoría. Tras la curación final, 6/6 casos del nuevo módulo y 34/34 pruebas Python correctos. No se presenta esta recuperación como otra ejecución íntegra de los 384 casos.
- **Producción:** tipos y aplicación compilados correctamente con la configuración de producción. La compilación focal privada reutiliza los más de 9000 recursos públicos idénticos; se actualizan los once recursos nuevos. No cambia la configuración versionada de Vite ni la construcción limpia de GitHub.
- **Navegador:** doce recorridos focales distintos de 0.49/0.50/0.51: diez milenios, clics reales, filtros, descargas atrasadas, transición10000, yacimientos, áreas compartidas, Lucy/globo móvil, costa3/4Ma, homininos tempranos, hielo automático/manual y apariencia. La expectativa antigua «Denisovanos0 en60000a.C.» se corrige porque el recuento incluye áreas estimadas; se comprueba ausencia en20000a.C. conservando la selección. Los doce casos quedan correctos después de esa actualización. Capturas de mapa completo y globo de tarde revisadas: océano azul y paneles marrones, sin exceder segmentosGPU en los recorridos.
- **Recopilación normal:** 148 casos; 147 repartidos19/19/19/18/18/18/18/18 y un barrido anual dedicado. [Auditoría de asignaciones](CI-SHARDS-0.51.0.json), sin omitidos, inesperados o duplicados. No se han vuelto a ejecutar localmente los148 casos ni el barrido anual, cuyo cuerpo no cambia.

## Continuidad

Faltan contornos de hielo anteriores a80ka, paleocostas detalladas, paleorrelieve, posiciones fósiles reconstruidas y validación regional independiente. El catálogo no es un censo cerrado de especies o yacimientos. Las franjas expresan solapamiento de reconstrucciones; no guerra, dominancia o sustitución demostrada.

Mantener ocho grupos más el barrido anual independiente y todos los requisitos de publicación. Se envía a main tras cerrar las comprobaciones y el registro; al retomar, cotejar HEAD/origin/main. El propietario comprueba Actions/Pages. No se espera ni se sondea el despliegue remoto.
