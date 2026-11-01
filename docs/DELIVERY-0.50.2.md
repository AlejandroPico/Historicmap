# Entrega0.50.2 · descarga atrasada y reparto de navegador

Base a91f98eec. El propietario comunica un fallo y35 casos correctos en el grupo1/4. El fallo se reproduce: la prueba considera10001a.C. fuera de toda cobertura y exige cero, pero ahora hay13 evidencias humanas válidas. La aplicación conserva correctamente la fecha elegida. No se eliminan datos ni se cambia código de la aplicación.

## Corrección de la prueba

El límite del índice de polígonos se llama beforeCulturalAreas, sin equipararlo a todo poblamiento. La descarga de regiones de900 se retiene hasta completar una consulta posterior:

- 10001a.C.: se conservan las evidencias humanas, sin territorios políticos, y sigue siendo seleccionable Aven des Iboussières.
- 300Ma: no aparecen culturas o yacimientos medievales sobre la cartografía geológica.

Se confirma que la petición quedó retenida, se libera y espera su respuesta completa, se comprueban fecha y cantidades estables, y se regresa al900 con una sola descarga. La promesa se libera también al fallar. Se mantienen las comprobaciones de conservación de Amazonas.

## Ocho grupos y barrido dedicado

A petición del propietario, Quality reparte los casos habituales entre ocho máquinas con un navegador por máquina. fullyParallel:true reparte por caso; workers:1 evita competir por el renderizado por software en cada máquina. El total de la matriz determina el nombre y el argumento de cada grupo.

El barrido continuo1789–presente conserva todo su cuerpo, controles y caché; sólo recibe la etiqueta @annual-sweep. Los ocho grupos lo excluyen y un trabajo adicional lo ejecuta una única vez, en paralelo y con la misma compilación verificada. Así no alarga el grupo al que antes le tocaba. Se conserva publicación sólo tras el éxito de todo Quality, también del barrido; no hay continue-on-error ni pruebas omitidas.

No se garantiza una reducción exacta a la mitad: influyen la cola y capacidad de GitHub, instalación, compilación común y pruebas más largas. No se modifican cuotas o facturación. [Sharding oficial de Playwright](https://playwright.dev/docs/test-sharding).

## Comprobaciones realizadas

- Reproducción negativa antes de la corrección: esperado0, recibido13 en10001a.C.
- Cinco recorridos reales correctos sobre producción: Amazonas, los dos casos de respuesta atrasada, descarga humana compartida y continuidad de contextos a través de10000/9751.
- TypeScript correcto; aplicación0.50.2 compilada correctamente. Recursos públicos idénticos de la salida aislada previa reutilizados para evitar copiarlos de nuevo; esa optimización es privada y no cambia la configuración versionada de producción.
- Recopilación completa144 casos, ocho grupos con143 casos (18/18/18/18/18/18/18/17) y un barrido anual independiente. Comparación por ID: ningún caso omitido, añadido o duplicado. [Auditoría](CI-SHARDS-0.50.2.json).
- Datos, medios, originales, importaciones JSON corregidas en0.50.1 y controles de publicación conservados.

Se recopilan los144 casos y se ejecutan cinco focales. No se repiten localmente los144 recorridos ni el barrido anual de cinco minutos, cuyo cuerpo no cambia y cuyo éxito previo aporta el propietario. La recopilación no se presenta como ejecución completa.

## Envío

La subida a main ocurre después de este registro. Si se interrumpe la sesión, comparar HEAD/origin/main antes de repetir el envío. El propietario verifica Actions/Pages; no esperar ni sondear el despliegue.
