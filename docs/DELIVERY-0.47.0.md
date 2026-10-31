# Entrega 0.47.0 · consulta hasta 3000 a. C.

31 de octubre de 2026. Base `53431e0888855166a639153a46e327bc57d10064`. La revisión de publicación en GitHub Pages corresponde al propietario; no se espera ni se sondea Actions.

## Contenido

- Tres tramos acotados: 3000–2601, 2600–2201 y 2200–2001 a. C.; navegación anual, sin año cero.
- 39 dossiers de periodo y 50 ventanas de autoridades; 67 registros urbanos, 18 contextos y referencias localizadas de conflictos. Nombres dinásticos corregidos sobre los originales, con cronologías alternativas y notas donde no se puede asignar un mandato anual seguro.
- 25 grupos culturales originales y 31 fases nuevas; todas las fases anteriores conservadas. La referencia de 3000 no se presenta como mil observaciones anuales ni se completa hacia atrás con el mapa de 2000.
- 42 candidatos visuales inspeccionados: 23 representaciones adoptadas, 19 descartadas y 22 archivos públicos nuevos. Neferefra tiene permiso de reutilización comprobado por archivo; las alternativas de Ur-Nammu y Shulgi son figuras fundacionales identificadas por museos.
- Datos, originales, decisiones y medios bajo sus entidades de `Países/`. Rótulos editoriales españoles: 384. El catálogo se sincroniza antes de comprobar y reconoce todos los recursos a. C. registrados.

## Conservación

[Auditoría de conservación](CONSERVATION-0.47.0.json): permanecen los 1.570 identificadores anteriores, 20.509 ventanas de autoridades, 1.023 banderas, 17 referencias simbólicas y las 10.152 fases culturales previas, sin pérdidas ni cambios en los hechos auditados. Los originales de 25 componentes políticos se verifican contra las copias canónicas por entidad; 29 copias corresponden a cruces entre ventanas. La existencia de los originales no certifica todas sus fronteras.

Los vacíos, notas de autoridades sin fechas completas y límites arqueológicos se conservan explícitamente en [investigación](RESEARCH-bc3000.md), [inventario](PERIOD-INVENTORY-bc3000.json), [auditoría anual](REVIEW-bc3000-bc2001.json), [decisiones visuales](MEDIA-REVIEW-bc3000.json) y [tareas](../tareas.md).

## Verificación local

- Pruebas focales: 16/16 correctas, con calendario, catálogo y periodo nuevo.
- Investigación y permisos: 27/27 pruebas Python correctas.
- Integridad: 174 recursos de datos, 11 rangos de glifos y 9.179 medios con sus SHA-256 verificados.
- Suite completa: 349/349 pruebas, 73 archivos. Después de corregir el cierre de nombres del generador: 16/16 pruebas focales correctas sobre los archivos finales.
- Producción: compilación real completada, con TypeScript y Vite; se reconstruyó tras la corrección del generador.
- Navegador: cinco casos locales correctos, tres nuevos y dos regresiones. Los tres casos nuevos se repitieron sobre la reconstrucción final, también correctos. Incluyen clic real sobre Egipto, sucesiones, cruces de recursos, figuras regias, persistencia de fichas, globo móvil y controles independientes. Capturas revisadas visualmente.
- La suite de navegador completa contiene 132 casos en 57 archivos; se mantiene la división en cuatro grupos para CI. No se ha esperado ni consultado su ejecución remota.
- Regeneración: [178 archivos comprobados](REGENERATION-0.47.0.json); 177 idénticos byte a byte y manifiesto equivalente salvo orden de entradas. El pase completo y la comprobación posterior de los compiladores acotados quedan diferenciados en el informe.

Las carencias científicas pendientes no se declaran resueltas por la validación del programa. No se han añadido banderas ficticias ni retratos de una persona distinta para evitar casillas vacías.


La comprobación de regeneración detectó inicialmente una dependencia de los diccionarios de nombres respecto al catálogo mutable de otras épocas. Se corrigió el generador para limitar nombres y QID a las entradas del tramo; sólo consulta administradores externos referenciados. Las reglas fechadas y geometrías no cambiaron por esa corrección. La prueba focal verifica el cierre de nombres por periodo.

La prioridad de reglas de los dos compiladores se ha unificado. Para este tramo, las ventanas de una misma denominación son disjuntas; su orden no cambia el resultado del mapa. Se vuelven a verificar las pruebas focales y los SHA-256 después de la composición final.


## Paquete preparado

363 archivos nuevos o modificados comprobados contra sus bytes locales y objetos del índice Git. Los 9.364 recursos de los manifiestos coinciden con sus SHA-256 y objetos preparados; 9.317 recursos conservan exactamente el objeto de la base anterior. No se elimina ningún archivo. La comprobación se completa antes del commit y del envío a main; la validación remota de Actions/Pages corresponde al propietario.

El caso de clic real y continuidad egipcia se repitió también con los archivos JSON finales exactos, correcto. La diferencia de orden de reglas no implica cambios de fechas ni geometrías; la prueba focal verifica que no existen ventanas ambiguas de la misma denominación en los tramos nuevos.
