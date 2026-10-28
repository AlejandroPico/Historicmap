# Calidad y publicación desde0.36

El28/10/2026 el propietario comunica que la ejecución distribuida tarda aproximadamente25 minutos, frente a más de una hora anteriormente. Se conserva este diseño en0.37. Es una observación comunicada por el propietario, no una medición remota nueva de esta entrega. El número de casos crece con las ampliaciones; cada reparto se audita para comprobar que ningún caso se omite o duplica.

Los registros aportados por el propietario muestran42,1min de navegador en0.34 y57,9min en0.35, con un único trabajador. Dos expectativas suponían que699 no tenía culturas; otra esperaba el snapshot antiguo de500 pese a la nueva cobertura anual. Se corrigen las pruebas, conservando los datos ampliados.

El test de snapshots consulta `snapshotFor`, ylos casos de ausencia cultural calculan un año realmente anterior al primer intervalo del catálogo. El caso de descarga obsoleta sigue comprobando que una respuesta retrasada no sustituya la fecha más reciente. Las tres correcciones se probaron primero sobre0.35 yse vuelven a validar con la cobertura400.

## Ejecución

1. `Quality / verify` instala dependencias, verifica recursos, ejecuta todas las pruebas unitarias yel lector Python de mandatos, ycompila una vez. Añade `dist/revision.json` con la revisión exacta ysube `historicmap-build`.
2. Cuatro trabajos independientes descargan ese mismo resultado yejecutan el inventario completo con `--shard=1/4` a `4/4`. `fullyParallel` permite repartir casos de un mismo archivo; cada máquina conserva un solo trabajador para aislarWebGL. No se eliminan casos ni se cancelan los otros grupos al fallar uno.
3. La auditoría local vigente verifica101 casos, repartidos26/25/25/25, cada uno asignado exactamente una vez: [CI-SHARDS-037.json](CI-SHARDS-037.json). La auditoría anterior de98 casos se conserva en CI-SHARDS-036.json. Este informe no afirma ejecución exitosa de todos esos casos enGitHub ni una medición remota de duración.
4. La publicación automática sólo continúa tras éxito global deQuality en un push delmain del mismo repositorio. Descarga el artefacto de ese `workflow_run.id` ycomprueba que su revisión coincide con `head_sha`. No instala dependencias ni recompila por segunda vez.
5. La ejecución manual conserva la posibilidad explícita de construir la revisión solicitada. Resulta útil si un artefacto antiguo ha caducado; no es la ruta automática.

Los artefactos conservan diagnóstico por grupo ycaducan a los siete días. La compresión de nivel1 reduce trabajo de empaquetado. El máximo paralelismo efectivo yla duración final dependen de los ejecutores disponibles, colas yrendimiento deGitHub; no se promete un tiempo concreto antes de medir una ejecución remota.

Documentación oficial consultada: [Playwright, distribución ybalanceo](https://playwright.dev/docs/test-sharding), [download-artifact ydescargas de otra ejecución](https://github.com/actions/download-artifact), [upload-artifact ycompresión](https://github.com/actions/upload-artifact).

## Verificación local

La entrega registra en`tareas.md` los recorridos ejecutados, pruebas unitarias, hashes ylímites. La colección de101 casos yla estructura de los workflows se verifican localmente; la entrega no espera la matriz completa deGitHub. El propietario comunicará el resultado del despliegue, según su instrucción permanente.
