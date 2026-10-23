# Entrega0.10.0 · ampliación a1950

Fecha:24/10/2026. Revisión local terminada. La subida a main se registra en el historial Git; **el despliegue remoto queda pendiente de confirmación del propietario**, por su instrucción expresa. No se espera ni se consulta Actions/Pages en esta entrega. No equivale a publicación pública comprobada.

## Implementación y datos

- Adquisición incremental mundial1950–1959 y33 registros focales curados, conservando las décadas posteriores, medios y referencia contemporánea22/10/2026. Catálogo total:285 claves y7.985 registros de mandato, no igual número de personas ni series exhaustivas de todos los cargos.
- VSV/Estado de Vietnam y MAL/Federación de Malaya separados de los sucesores, con transiciones navegables. Correcciones focales de cargos/regencias de Egipto, Corea, Taiwán, Alemania, Uruguay y otros casos documentados.
-41 intervalos/diseños de bandera focales de la nueva revisión, con licencia y procedencia. Inventario de4.062 medios(451SVG/3.611 fotografías):269 medios netos adicionales frente a0.9.1, incluidos257 retratos y12SVG. No son269 países ni imágenes de todos los titulares. El diseño candidato de Túnez1831–1959 no se encontró con ese título: no se importó un sustituto sin comprobar.
-20 relaciones administrativas fechadas desde1950; fases constitucionales de Surinam y Puerto Rico diferenciadas.36 organizaciones y613 intervalos de membresía;279 fases contextuales;68 relaciones históricas y62 registros institucionales/históricos. Nuevas organizaciones:CECA, Euratom, ANZUS, SEATO y Bagdad/CENTO. No se inventan frentes a partir de una ficha de conflicto.
-2.783 carpetas de entidades presentes en los conjuntos incorporados;285 tienen inventario de autoridades. El índice y resumen reúnen nombres, banderas, mandatos/retratos y referencias territoriales. Las coordenadas, medios y licencias permanecen en sus colecciones originales. Los archivos generados no son una segunda fuente editorial independiente.
- Entradas editables por entidad para audio/PDF con vigencia, fuente y licencia. Detección al compilar y presentación en Datos cuando existe un recurso válido. No hay himnos adquiridos ni reproductores vacíos por defecto.
- Cabecera y pestañas fijas, desplazamiento interior sin barra vertical visible, conservación de la lectura al cambiar de año, acciones de comparación dentro de Comparar, procedencia del símbolo enlazada desde la bandera, X conservada.

## Comprobaciones locales realizadas

-122 pruebas unitarias en26 archivos correctas, incluidas cobertura de1950, regresiones anteriores, entidades y datos fechados.
- Integridad de43 recursos,11 franjas tipográficas y4.062 medios acreditados por SHA-256; comprobados también los bytes preparados en Git de los4.116 recursos; tipos y compilación correctos. La compilación informa del tamaño del paquete principal; no es un fallo de construcción ni se ha silenciado la advertencia.
-5 recorridos de navegador correctos(2,5min): ficha/pestaña/posición al cambiar año y reproducir; entidad desaparecida y sucesor; comparación entre fechas/países; persistencia de búsqueda/fuentes/capas; autoridades1950, cabecera anclada y vista móvil390px. No se ha ejecutado toda la suite de navegador en esta entrega local; Quality conserva su configuración completa.
- Revisión visual adicional en el navegador integrado: Egipto1952, bandera, retratos y desplazamiento por varios Gobiernos, Fuad II y Farouk; cabecera/pestañas permanecen visibles. Evidencia local `.cache/country-fixed-header-1952.png`; evidencia móvil `test-results/1959-card-mobile.png`. No se suben las capturas temporales al repositorio.

## Carencias que continúan abiertas

Auditoría de1.753 combinaciones de territorio/año1950–1959: cero huecos de resolución de autoridad, **69 personas/órganos sin retrato** y**23 territorio-años sin símbolo**(Andorra/San Marino y Túnez1956–1958). Lista nominal durable en REVIEW-1950.json. Un órgano colectivo no requiere un retrato inventado. Fuentes y alcance en RESEARCH-1950.md.

La auditoría no demuestra exactitud historiográfica mundial de todas las fronteras, cargos, suplencias y días. Persisten frentes y fases detalladas de Corea, Indochina, Suez, descolonización, Sarre/Berlín, autoridades coloniales locales y jefaturas secundarias. Las ventanas documentales no son ceses exactos. No hay estadísticas WDI inventadas anteriores a1960. Se conservan los pendientes anteriores y el CSV original ausente.

## Reconstrucción y relevo

Orden incremental: enrich-1950-authorities → curate-1950-authorities → prepare-1950-dependencies → retratos por ventana → curate-1950-symbols → prepare-1950-context → prepare-recent-supplements → pruebas de cobertura → register-1950-data → prepare-country-catalog → integridad/tipos/pruebas/build → navegador. No reemplazarlo por una inicialización destructiva; mantener curaciones, exclusiones y la fotografía íntegra de Mozambique. `npm run build` regenera/valida el catálogo por entidad. Los recursos manuales se conservan.

Siguiente paso operativo: el propietario confirma el despliegue o comunica su error. Sólo entonces se revisa la versión publicada. No iniciar sondeos automáticos ni cambiar el sitio público para simular una comprobación.
