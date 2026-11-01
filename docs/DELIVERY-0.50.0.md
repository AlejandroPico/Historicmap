# Entrega 0.50.0 · 1 de noviembre de 2026

## Resultado

Consulta hasta **100000 a. C.**, conservando el contenido posterior y la cronología civil sin cero. El nuevo modo prehistórico consulta un recurso común de evidencias, con pasos de reproducción/navegación de cien años y entrada de cualquier año exacto. No fabrica siglos de fronteras políticas.

**803 referencias de yacimientos o conjuntos y 2820 registros**: 2390 filas de la recopilación de Timmermann y colaboradores, 13 referencias primarias complementarias y 417 contextos de PaleoHumans1.0.0. Se conservan fechas, niveles, atribuciones, culturas materiales, coordenadas, bibliografía y procedencia. Los recuentos son propietarios de referencias; no certifican equivalencias físicas entre todos los lugares de compilaciones distintas.

PaleoHumans refuerza el Paleolítico superior con250 expedientes;248 sitios tienen una fase utilizable. Cinco contextos inciertos quedan registrados sin puntos fechados supuestos. Diez correspondencias por nombre y posición comparten propietario con la primera recopilación; ElCastillo permanece como equivalencia ambigua pendiente. Las ventanas culturales son **contexto, no fechas directas de cada individuo**. Los resultados originales sin calibrar se conservan sin conversión automática a años de calendario. Las referencias siguen visibles junto a las áreas culturales anteriores al cruzar10000, hasta el límite publicado de su ventana, nominalmente9751a.C.

Los puntos aparecen con el control cultural inicialmente activado, independiente del político. El filtro humano, las fichas abiertas, sus pestañas y la comparación de fechas siguen funcionando durante los cambios de año. La ficha arqueológica tiene una primera pestaña de evidencias; no se inventan gobiernos, retratos o banderas.

Hielo opcional **PaleoMIST1.0**:92 originales geográficos, cuatro regiones y23 muestras de0–80000BP1950, separadas por2500–5000años. Fecha de muestra explícita, sin interpolación anual ni extrapolación anterior a78051a.C. Se mantienen polos, antimeridiano, agujeros y unión de solapamientos. Las costas continúan como referencia contemporánea.

## Conservación y reproducción

- Se mantienen los20559 mandatos anteriores y sus referencias a retratos, símbolos y notas. Las10304 fases culturales previas conservan su checksum semántico completo.
- Los199 recursos GeoJSON anteriores conservan sus bytes, incluidas las seis muestras previas del hielo. Lugares, contextos, gobernanza, influencia e historial anteriores se conservan. [Hechos y fases](CONSERVATION-bc100000.json), [referencias anteriores](CONSERVATION-REFERENCES-bc100000.json).
- Catálogo:2423 identidades y5250 carpetas. Nuevos datos humanos dentro de`Países/<propietario>/arqueologia/`; originales naturales en`Tierra/`.
- La reproducción final de evidencias humanas, revisiones y catálogo conserva los272 recursos preparados, la semántica del manifiesto y los bytes del índice de países. Los márgenes de hielo ya se reprodujeron idénticos en el ciclo inicial y no cambian con el refuerzo PaleoHumans. [Informe](REGENERATION-bc100000.json).

## Comprobaciones

- 377 pruebas generales correctas en77 archivos sobre el conjunto final ampliado.
- Tipos y compilación de producción correctos.
- Ocho recorridos distintos de navegador comprobados: siete en el ciclo final y el octavo mediante repetición focal tras sustituir una consulta global de círculos del globo por un clic real sobre un marcador visible. La consulta global no enumeraba los círculos que sí aparecían en pantalla; el clic abre su ficha. Incluye mapa/globo, móvil, filtros, comparaciones, caché y último año solicitado, hielo y continuidad10001/10000/9751.
- 34 comprobaciones de investigación correctas. Integridad de272 recursos de datos,11 rangos tipográficos y9179 medios con SHA-256. Los92 originales de hielo se comprueban contra sus hashes propios. Cotejo del índice Git:2549 archivos nuevos/modificados coinciden con sus bytes locales;9462 recursos se comprueban también por SHA-256 y objeto Git. De ellos,9441 conservan el objeto de la base0.49.0.

## Límites y continuación

Las referencias no constituyen densidades de población, fronteras biológicas, ocupación continua ni rutas exactas. Las atribuciones de compilación se conservan sin presentarlas como rediagnósticos propios. La cobertura regional es desigual; el corpus europeo adicional no representa el mundo entero. Fechas y calibraciones individuales requieren revisión por método, material y contexto; no asumir una corrección de reservorio uniforme.

Pendientes: paleocostas y paleorrelieve; modelos aptos anteriores a80000BP; más fuentes regionales y revisión de dataciones; georreferencia precisa de LiangTebo, que muestra una referencia regional declarada; equivalencias ambiguas entre compilaciones. [Investigación](RESEARCH-bc100000.md), [inventario](PALEOLITHIC-INVENTORY.json), [ruta terrestre](ROADMAP-EARTH-HISTORY.md) y [continuidad](../tareas.md).

Se envía a`main` sin esperar ni sondear Actions/Pages. El propietario comprueba el despliegue.
