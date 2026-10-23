# Pizarra de continuidad · ampliación a 1960

Actualizado: 23/10/2026. Rama: `codex/control-palette-1960`. Base publicada: 0.8.1, `911f7c3c55466e4f757a271ec8f5ee740e5eea1b`.

No marcar una tarea completada por haber escrito código, descargado registros o pasado una prueba de cobertura. Registrar resultados reales y distinguir trabajo local, subido y publicado. Leer también `agentes.md`.

## En curso

- [x] Revisar fuentes, geometrías, paletas y contratos de selección antes de modificar la representación del control. Fuentes originales separadas; composición geométrica temporal en worker, sin modificar archivos de coordenadas.
- [ ] Localizar el CSV aportado. La ruta indicada `C:/Users/darim/Downloads/lista_imperios_completa_v3.csv` no existe al comprobarla el 23/10/2026. No afirmar haber integrado el documento hasta recuperar sus bytes. Las propuestas de color verbales sí están disponibles.

## Cambios solicitados

- [x] Paleta histórica editorial por entidad y régimen:33 familias y CSV exportable, con dependencias en tonos de su potencia y contraste entre rivales. No interpretar colores antiguos como ideologías modernas. Falta conciliar el adjunto original no disponible.
- [x] Control territorial en el propio mapa y selección del controlador sin depender del interruptor de ocupaciones. Geometría real de1942, clic y búsqueda comprobados en navegador.
- [x] Ocupaciones opcionales con franjas gruesas del controlador y finas del territorio ocupado; anexiones sin franjas de ocupación. Prueba real distingue Viena de Oslo; captura de franjas revisada.
- [x] Tierra de referencia visible bajo huecos políticos, especialmente África1889 y Arabia1918; comprobada también en Roma100 y separada del dominio geológico. Ausencia en el inventario no significa territorio deshabitado ni sin organización política.
- [x] Ampliar autoridades, mandatos, retratos y banderas de 1960–1969, conservando curaciones/créditos. Catálogo final local283 claves/7.481 mandatos,3.788 medios (268 archivos fotográficos y44 símbolos netos nuevos).53 intervalos de bandera curados. No acredita todas las suplencias ni todos los retratos.
- [x] Revisión focal de dependencias, independencias y fronteras1960–1969: UAR, Yemen, Tanganyika/Zanzíbar, UNTEA, protectorados, Namibia y estados omitidos. Pruebas de datos y navegador correctas; no certifica una revisión exhaustiva mundial de frentes o fechas diarias.
- [x] Ampliar contexto, conflictos y membresías fechadas a1960:31 organizaciones/549 intervalos,258 fases,59 relaciones/53 registros históricos e institucionales; fuentes y límites explícitos.
- [x] Auditoría del resolver cada año1960–1969, incluidos suplementos:1.693 país-años, cero huecos de resolución; guardar nombres/años de122 personas/órganos sin imagen y20 país-años sin símbolo en `docs/REVIEW-1960.json`. No equivale a revisión historiográfica exhaustiva.

## Validación y entrega

- [x] Pruebas de partición/control, clic, franjas y anexión frente a ocupación.
- [x] Pruebas de paleta, régimen y dependencia; contraste de familias británica/soviética.
- [x] Verificación de carga al retroceder y regresar, conservando arreglos de0.8.1; fichas, relaciones administrativas y sucesiones en los recorridos superados.
- [ ] Pruebas de datos, integridad de recursos y medios, tipos, compilación y navegador.
- [x] Actualizar versión0.9.0, CHANGELOG, agentes, investigación y documentación de fuentes/limitaciones. Cierre de publicación todavía pendiente.
- [ ] Publicar por el flujo existente y registrar SHA, Quality, Pages y comprobación pública. No está publicado todavía.

## Pendientes previos que no deben desaparecer

- [ ] Fichas no seleccionables en épocas anteriores a la ventana revisada: inventariar y corregir por etapas; no declararlas resueltas al ampliar una década.
- [ ] Frentes mensuales, sectores aliados de Alemania, control efectivo mundial reciente y resolución costera superior: ver límites de `agentes.md`.
- [ ] Vacíos de imágenes y mandatos anteriores: mantener auditorías; un nombre o fotografía no certifica todos los cargos del país.

## Cómo retomar

Punto de control20:36 Madrid: 114 pruebas unitarias/23 archivos superadas antes de la última foto y una regresión de imagen; cinco comprobaciones focales finales correctas. Suite completa de28 recorridos de navegador en ejecución (`.cache/browser-0.9-full.log`, sesión77021),22 ejecutados:21 correctos y un arranque sin `#map` coincidente con una reconstrucción local del directorio servido. Repetir ese recorrido con build estable; no ocultar el fallo. Repetición final de unitarias en sesión80719. Última auditoría:1.693 país-años,122 personas/órganos sin foto y20 símbolos ausentes;3.788 medios/439 SVG/3.349 fotografías. Tipos y build correctos; actualizar build tras terminar el navegador para incluir la última foto de De Gaulle, adquirida mediante alternativa OWI/Library of Congress con licencia PD. Versión0.9.0 todavía local. Ver `docs/DELIVERY-0.9.0.md`. Siguiente: cerrar pruebas, integridad, registrar bytes en Git, Quality/Pages y comprobar la web pública. CSV original pendiente; Andorra y San Marino no se rellenan con diseños modernos sin contraste de variante.

Comprobar primero el estado de Git y esta pizarra. Continuar por los puntos sin marcar; contrastar los resultados registrados y no repetir adquisiciones destructivas. Si una sesión se interrumpe, anotar aquí el último comando terminado, archivos modificados, procesos activos, siguiente paso y fallos concretos antes de cerrar.
