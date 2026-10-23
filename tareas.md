# Pizarra de continuidad · ampliación a 1960

Actualizado: 23/10/2026. Rama actual: `main`. Base del encargo: 0.8.1, `911f7c3c55466e4f757a271ec8f5ee740e5eea1b`.

No marcar una tarea completada por haber escrito código, descargado registros o pasado una prueba de cobertura. Registrar resultados reales y distinguir trabajo local, subido y publicado. Leer también `agentes.md`.

## En curso

- [x] Revisar fuentes, geometrías, paletas y contratos de selección antes de modificar la representación del control. Fuentes originales separadas; composición geométrica temporal en worker, sin modificar archivos de coordenadas.
- [ ] Localizar el CSV aportado. La ruta indicada `C:/Users/darim/Downloads/lista_imperios_completa_v3.csv` no existe al comprobarla el 23/10/2026. No afirmar haber integrado el documento hasta recuperar sus bytes. Las propuestas de color verbales sí están disponibles.

## Cambios solicitados

- [x] Paleta histórica editorial por entidad y régimen:33 familias y CSV exportable, con dependencias en tonos de su potencia y contraste entre rivales. No interpretar colores antiguos como ideologías modernas. Falta conciliar el adjunto original no disponible.
- [x] Control territorial en el propio mapa y selección del controlador sin depender del interruptor de ocupaciones. Geometría real de1942, clic y búsqueda comprobados en navegador.
- [x] Ocupaciones opcionales con franjas gruesas del controlador y finas del territorio ocupado; anexiones sin franjas de ocupación. Prueba real distingue Viena de Oslo; captura de franjas revisada.
- [x] Tierra de referencia visible bajo huecos políticos, especialmente África1889 y Arabia1918; comprobada también en Roma100 y separada del dominio geológico. Ausencia en el inventario no significa territorio deshabitado ni sin organización política.
- [x] Ampliar autoridades, mandatos, retratos y banderas de 1960–1969, conservando curaciones/créditos. Catálogo final local283 claves/7.480 mandatos,3.788 medios (268 archivos fotográficos y44 símbolos netos nuevos).53 intervalos de bandera curados. No acredita todas las suplencias ni todos los retratos.
- [x] Revisión focal de dependencias, independencias y fronteras1960–1969: UAR, Yemen, Tanganyika/Zanzíbar, UNTEA, protectorados, Namibia y estados omitidos. Pruebas de datos y navegador correctas; no certifica una revisión exhaustiva mundial de frentes o fechas diarias.
- [x] Ampliar contexto, conflictos y membresías fechadas a1960:31 organizaciones/549 intervalos,258 fases,59 relaciones/53 registros históricos e institucionales; fuentes y límites explícitos.
- [x] Auditoría del resolver cada año1960–1969, incluidos suplementos:1.693 país-años, cero huecos de resolución; guardar nombres/años de96 personas/órganos sin imagen y20 país-años sin símbolo en `docs/REVIEW-1960.json`. No equivale a revisión historiográfica exhaustiva.

## Validación y entrega

- [x] Pruebas de partición/control, clic, franjas y anexión frente a ocupación.
- [x] Pruebas de paleta, régimen y dependencia; contraste de familias británica/soviética.
- [x] Verificación de carga al retroceder y regresar, conservando arreglos de0.8.1; fichas, relaciones administrativas y sucesiones en los recorridos superados.
- [ ] Pruebas de datos, integridad de recursos y medios, tipos, compilación y navegador.
- [x] Actualizar versiones0.9.0/0.9.1, CHANGELOG, agentes, investigación y documentación de fuentes/limitaciones. Cierre de publicación todavía pendiente.
- [ ] Publicar por el flujo existente y registrar SHA, Quality, Pages y comprobación pública. No está publicado todavía.

## Pendientes previos que no deben desaparecer

- [ ] Fichas no seleccionables en épocas anteriores a la ventana revisada: inventariar y corregir por etapas; no declararlas resueltas al ampliar una década.
- [ ] Frentes mensuales, sectores aliados de Alemania, control efectivo mundial reciente y resolución costera superior: ver límites de `agentes.md`.
- [ ] Vacíos de imágenes y mandatos anteriores: mantener auditorías; un nombre o fotografía no certifica todos los cargos del país.

## Cómo retomar

Punto de control21:10 Madrid:0.9.0 publicada en ba7eb3b8ab505a277f5fb5f59c6e18eeb06084af. Quality40005916966:114 unitarias y28 navegadores correctos; Pages40008258279 correcto; cotejo público de4 archivos de aplicación,3 manifiestos,7 datos y9 medios. Evidencia en DELIVERY-0.9.0. Las primeras pasadas locales tuvieron fallos de tiempo y un catálogo mixto por cambiar rama durante un build; se documentaron y no sustituyen los resultados finales de CI.

Corrección0.9.1 preparada: conserva medios antes de regenerar mandatos y recupera26 retratos acreditados, separa Azikiwe/Balewa y respeta cargos curados al consolidar.115 unitarias/23 archivos, tipos e integridad43/11/3.788 correctos. Catálogo283/7.480; auditoría1.693 país-años,96 sin retrato y20 sin bandera. Siguiente: comprobar bytes staged, commit/push de0.9.1, Quality completo, Pages y bytes públicos. No dar por publicada0.9.1 por estarlo0.9.0. Servidor de preview propio: sesión84360/puerto5174; CUA browser2/tab2 temporal. No cambiar rama ni recompilar durante otra prueba. No hay adquisición activa de medios.

Pendientes que permanecen: CSV original no disponible,96 retratos/órganos (76 sin P18,17 candidatos, tres órganos/identificadores documentales), variantes AND/SMR, relevos diarios, gobernadores generales y frentes globales. Pistas específicas en docs/reference/portrait-1960-pending-research.json y documentos de investigación. No usar una candidatura como imagen aprobada ni una autoridad resuelta como certificación de todos los cargos.

Comprobar primero el estado de Git y esta pizarra. Continuar por los puntos sin marcar; contrastar los resultados registrados y no repetir adquisiciones destructivas. Si una sesión se interrumpe, anotar aquí el último comando terminado, archivos modificados, procesos activos, siguiente paso y fallos concretos antes de cerrar.
