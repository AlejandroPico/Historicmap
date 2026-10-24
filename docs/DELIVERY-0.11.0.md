# Entrega 0.11.0 · ampliación hasta 1920

Preparación: 24 de octubre de 2026. Referencia contemporánea conservada: 22/10/2026. Encargo: ampliar mundialmente 1920–1949 y mantener el trabajo posterior. Se comprobará localmente y se subirá sin esperar ni consultar el despliegue; la revisión pública queda pendiente del aviso del propietario.

## Contenido

- 290 claves de identidad y 9.485 mandatos. Adquisición incremental y cuatro preparadores documentales: autoridades focales, Europa/Asia, Américas y monarquías/territorios. Distinguen cargos formales, poder efectivo, regencias, gobiernos en el exilio y autoridades colectivas. Los límites de revisión no se presentan como nombramientos o ceses.
- Rusia soviética, República de China, monarquía yugoslava, Danzig, Tíbet y República Social Italiana separados de sucesores y de sus estadísticas. La RSI dispone de inventario, sin frente propio validado. Se corrige una atribución genérica falsa de presidencia a Yan Xishan; el mandato de primer ministro se contrasta con el archivo del Ejecutivo, 13/6/1949–10/3/1950.
- 4.863 medios: 478 SVG y 4.385 fotografías. Aumento neto de 774 fotografías y 27 SVG. Son 87 ventanas nuevas de símbolos, con reutilización de archivos acreditados y notas sobre variantes civiles, estatales y normalización. No se crean retratos para órganos colegiados ni banderas nacionales alemanas ficticias durante la ocupación.
- 24 relaciones administrativas desde 1920; transición colonial/departamental francesa y Austria bajo control alemán diferenciadas. 25 contornos contemporáneos de referencia para omisiones del inventario; Vaticano sólo desde el 7/6/1929.
- Corrección acotada de Danzig: la fuente termina su registro en 1938, antes de la anexión de 1939. Se conserva el contorno original y se corrige su validez observada; su área se resta al control alemán de 1938 para mantener un único propietario seleccionable. El archivo original de topología permanece intacto.
- El recorrido nuevo reprodujo un atasco con Rusia abierta al pasar de 1920 a 1921. El resaltado mediante filtro provocaba un nuevo reanálisis de teselas durante la actualización de fronteras. Se cambia ese resaltado a estado de pintura, sin recargas globales, cambios de coordenadas ni supresión de errores. La regresión comprueba la ficha conservada y un clic real después de actualizar.
- 38 organizaciones y 887 membresías fechadas, incluidas Sociedad de Naciones y ONU con sucesión/representación. 329 fases contextuales, 80 registros históricos/institucionales y 76 relaciones de entidades. No constituyen un censo completo de conflictos ni reconstrucciones diarias de frentes.
- Catálogo Países sincronizado: 2.787 carpetas de entidades incorporadas, 290 con inventario de autoridades. Recursos manuales conservados, medios y geometrías originales sin duplicación. Fecha visible de Acerca de corregida.

## Auditoría y carencias

| Década | Entidades/año | Controles/año | Sin autoridad resuelta | Personas/órganos sin foto en la década | Casos anuales sin símbolo |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1920–1929 | 1.747 | 0 | 0 | 54 | 68 |
| 1930–1939 | 1.778 | 32 | 0 | 38 | 47 |
| 1940–1949 | 1.769 | 38 | 0 | 63 | 50 |

Las personas se repiten entre décadas: hay **122 personas/órganos distintos sin retrato** en el conjunto, 118 personas y cuatro órganos colectivos. No se muestra símbolo en 165 casos anuales; cuatro corresponden a las zonas occidentales alemanas de ocupación de 1945–1948, sin una bandera nacional común. Se evita heredar únicamente la bandera/presidencia estadounidense para un ámbito compartido con Reino Unido y Francia. Listas nominales en [REVIEW-1920-1949.json](REVIEW-1920-1949.json). Tener alguna autoridad resuelta no acredita todas las autoridades locales, suplencias o fechas diarias de ese país. Los cambios de frontera de las fuentes y controles incorporados no son un censo exhaustivo de todos los frentes.

Continúan pendientes variantes y medios no contrastados, ocupaciones y fronteras detalladas, autoridades coloniales locales, algunos regímenes breves y el CSV original ausente del propietario. No se inventan estadísticas anteriores al periodo disponible. Fuentes y decisiones: [contexto](RESEARCH-1920.md), [autoridades focales y Europa/Asia](AUTHORITIES-1920-RESEARCH.md), [Américas](AUTHORITIES-1920-AMERICAS.md), [regiones](AUTHORITIES-1920-REGIONS.md), [símbolos](SYMBOLS-1920.md) y [símbolos adicionales](SYMBOLS-1920-EXTRA.md).

## Validación local

129 pruebas en 28 archivos correctas. Incluyen resolución anual, sucesores, administraciones, símbolos, fechas de organizaciones y puntos reales en la geometría compuesta de Danzig/Berlín/Viena. Los cuatro curadores se comprobaron dos veces sobre copia para verificar repetibilidad y conservación de retratos; los de bloques adicionales preservan los datos posteriores. Muestra visual de 12 retratos revisada localmente, sin atribuirle cobertura de todas las imágenes.

Integridad correcta de 43 recursos de datos, 11 franjas tipográficas y 4.863 medios por SHA-256; comprobados también los bytes preparados en Git de esos 4.917 recursos. Tipos y compilación correctos. La compilación conserva el aviso de tamaño del paquete principal; no se ha silenciado ni es un error de construcción.

Cuatro recorridos finales de navegador correctos (3,3 minutos): control integrado/franjas y fondo continental; ficha/pestaña/lectura durante cambios de fecha y reproducción; autoridades de1920–1949 con bandera, retratos, persistencia y clic real tras Rusia1920→1921; y regresión de los años cincuenta con cabecera fija, comparación y vista móvil. Sin errores de página observados en el recorrido nuevo. Se repitieron sobre la compilación que incluye la corrección del resaltado y la administración occidental alemana conjunta, sin debilitar las guardas de renderizado.

Revisión visual adicional de Danzig1938 con bandera y retrato; muestra de doce referencias de retrato y captura final de Alemania1949 revisadas localmente. Evidencias temporales en `.cache/portraits-1920-sample.png` y `test-results/history-1949-authorities.png`. No se suben las capturas temporales ni se afirma haber inspeccionado visualmente todos los medios.

Entrega comprobada para main. Por instrucción del propietario, el flujo termina al confirmar la subida del commit; **no se espera ni se consulta Actions/Pages**. No se ha comprobado la publicación de esta versión. El siguiente paso es su aviso de que el despliegue terminó o el error concreto que haya observado.

## Reconstrucción

Orden incremental: enrich-1920-authorities → retratos por ventana → cuatro curadores1920 → prepare-1920-dependencies → retratos focales nuevos → curate-1920-symbols y symbols-extra → prepare-1920-context → prepare-recent-supplements → auditoría de cobertura → register-1920-data → prepare-country-catalog → integridad/tipos/pruebas/build → navegador → subida. No usar una adquisición inicial destructiva. No avanzar la referencia contemporánea al investigar el pasado. Mantener licencias, exclusiones y archivos manuales por entidad. Los preparadores posteriores no deben restaurar afirmaciones descartadas en estas curaciones.
