# Entrega 0.50.1 · 1 de noviembre de2026

Corrección del fallo de recopilación comunicado por el propietario para los cuatro grupos de Playwright de0.50.0. Base d1fb7cdeb. No se amplía la investigación ni se modifica ningún recurso de Países, Tierra o public/data.

## Causa y cambio

Las pruebas importan time.ts desde el proceso Node ESM. Su importación de cronologia.json no declaraba el atributo de tipo JSON, obligatorio en esa carga. El error se reproduce con la configuración normal y --list: no se inicia ningún navegador. Las comprobaciones focales anteriores no acreditaron esta recopilación completa.

Se añade `with {type:'json'}` a la cronología en time.ts y a cronología/índice de ice-history.ts. No se altera el contenido ni la conversión de fechas. [Referencia oficial de Node](https://nodejs.org/api/esm.html#import-attributes).

Quality comprueba `npm run test:e2e -- --list` justo después de npm ci, antes de verificar datos, baterías y compilación. Se conservan todos los casos, los cuatro grupos y la condición de publicación. Esta fase rápida detecta una colección rota sin consumir primero toda la validación.

## Comprobaciones locales realizadas

- Reproducción previa: recopilación fallida con el TypeError informado.
- Cuatro recopilaciones correctas con configuración normal y PWTEST_CACHE_DIR nuevo por grupo:36,36,36 y35 casos;143 en total.
- 28 pruebas correctas en time, civil-dates, review-049 y review-050.
- TypeScript correcto y compilación Vite de4399 módulos correcta.
- Dos recorridos reales correctos sobre la nueva compilación: cursor/teclado/fecha exacta/información/móvil y globo móvil/hielo/marcadores/fechas fuente.
- Revisión del diff y comprobación de espacios; ningún cambio en datos históricos, arqueológicos, glaciares, medios o sus originales.

La salida dist/media local produjo EPERM al intentar vaciarla en Windows. La compilación se comprobó en una carpeta nueva ignorada y los recorridos se sirvieron desde ella en un puerto aislado. No se cambió la configuración versionada para evitar ese bloqueo local.

Se recopilan143 casos, pero no se ejecutan de nuevo localmente los143 recorridos completos; la ejecución completa permanece en los cuatro grupos de GitHub. Los resultados locales no acreditan publicación remota.

## Entrega

La subida a main se realiza después de guardar este registro. Al retomar, cotejar HEAD, origin/main y árbol de trabajo antes de repetir un envío. El propietario verifica Actions/Pages; no esperar ni sondear el despliegue.
