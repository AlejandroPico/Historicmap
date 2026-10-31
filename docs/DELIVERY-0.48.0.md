# Entrega 0.48.0 · 6000–3001 a.C.

## Resultado

Consulta continua hasta 6000 a.C., con 22 referencias arqueológicas,66 grupos originales regionales y 94 fases. Tres componentes políticos originales desde 3400, en una sola ventana de 400 años; no se fabrican mapas estatales anteriores. La fuente8000 se identifica como contexto heredado, sin adelantar5000 ni convertir una consulta anual en observaciones anuales independientes.

Fuentes y decisiones propias en `Países/`:22 dossiers `arqueologia.json`, dos dossiers de periodo, originales geométricos, referencias y notas. Se conservan autoridades y símbolos anteriores; no se inventan retratos, constituciones o banderas para comunidades sin esa evidencia. Los puntos están en «Capitales, ciudades y yacimientos», inicialmente desactivado como antes. Ambas cartografías siguen activadas por defecto.

Las fichas actualizan sus evidencias al viajar y permanecen abiertas. Se comprueba selección directa deÇatalhöyük occidental, revisión cronológica de Mehrgarh, cerámica cardial recuperada, Uruk y Liangzhu en los cambios de fuente, áreas culturales y controles independientes en el globo móvil. Los21 contextos usan un tipo compatible con la ficha y se validan al compilar. Sus intervalos arqueológicos amplios no se presentan como episodios ocurridos en cada año en la lista de hechos anuales.

## Comprobaciones locales

- Conjunto general:356 pruebas/74 suites correctas durante el cierre. Tras el ajuste final de contextos:46 focales/8 suites correctas, incluyendo conservación, selección, contexto y límites. No se afirma que se repitió todo el conjunto después de ese último ajuste.
- Python:31 comprobaciones correctas. El contrato rechaza contextos sin tipo/alcance apropiados, nombres de mandatarios o banderas fabricados y coordenadas o ventanas inválidas. El límite político de 400 años permanece intacto.
- Tipos y compilación de producción correctos. Cuatro recorridos finales de navegador correctos sobre la compilación aislada: escritorio, selección de un punto real, fichas/contextos, cambios de fuente, representaciones anteriores y globo móvil. Capturas revisadas.
- Integridad:206 recursos de datos,11 franjas tipográficas y 9179 medios con licencia. Antes de enviar se cotejan también todos los recursos y archivos preparados con sus objetos Git.
- Regeneración: cadena completa de geografía/culturas/entidades/registro comprobada antes del ajuste de tipo; repetición final de entidades/registro con 206 recursos idénticos y manifiesto semánticamente igual. Los datos de geografía y culturas no cambiaron entre ambas comprobaciones. Véanse ambos informes de regeneración; no confundir normalización de entradas con identidad del orden de bytes del manifiesto.

## Conservación y organización

Se conservan los 20559 registros anteriores de autoridades, sus símbolos y 10183 fases culturales completas. Total actual:1606 identidades,10277 fases culturales y 4433 carpetas catalogadas. Se comprueban aparte los contextos, lugares, gobernanza e historial anteriores sin registros perdidos.

Ocho vistas genéricas sin gobernantes o símbolos propios se integran en carpetas canónicas; sus once referencias territoriales siguen presentes. No se eliminan sus geometrías ni los hechos de una entidad. El informe de reasignación registra rutas y parejas archivo/recordId anteriores y actuales.

- [Fuentes y límites](RESEARCH-bc6000.md).
- [Inventario arqueológico y político](PERIOD-INVENTORY-bc6000.json), [inventario cultural](CULTURAL-EXTENSION-bc6000.json) y [consulta de los 3000 años](REVIEW-bc6000-bc3001.json).
- [Conservación de hechos y culturas](CONSERVATION-bc6000.json), [referencias anteriores](CONSERVATION-REFERENCES-bc6000.json) y [reasignación de vistas](ENTITY-ALIASES-bc6000.json).
- [Regeneración completa anterior al ajuste](REGENERATION-0.48.0-full.json) y [repetición final](REGENERATION-0.48.0.json).
- [Ruta de historia terrestre](ROADMAP-EARTH-HISTORY.md).

## Pendiente real

Contraste arqueológico independiente de los contornos regionales de compilación, más yacimientos, cronologías alternativas, discontinuidades locales y continuidad entre distintas clases de referencias. El gris no demuestra despoblación. No se han reconstruido aquí paleocostas, densidad de población, glaciares o un modelo físico de la Tierra prehistórica.

10000–6001 a.C. es la siguiente tanda prevista, no ya ejecutada. Se mantienen en ruta dispersión de homininos, hielo y mares, tectónica, ecosistemas, extinciones, atmósfera y Tierra temprana. Continúan los pendientes anteriores de Asiria/Egipto650 y Babilonia626/600. No iniciar otra tanda sin encargo.

Entrega preparada para main en este commit, sin esperar ni sondear Actions/Pages. El propietario comprobará el despliegue. Al reanudar, comparar HEAD yorigin/main antes de repetir el envío.
