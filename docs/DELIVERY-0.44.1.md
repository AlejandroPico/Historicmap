# Entrega 0.44.1 · catálogo de entidades sincronizado

La revisión final de Huiwen en0.44.0 quedó en los datos públicos y el dossier canónico, pero la ficha generada de Qin y su índice conservaron el único mandato anterior. CI ejecuta las pruebas antes del build, donde se detectó la divergencia:328/329. La pasada general local había ocurrido antes de ese último ajuste; los recorridos posteriores no verificaban este catálogo.

El registro de revisiones actualiza ahora también las fichas e índices y falla si ese paso no termina correctamente. Se mantiene la comparación completa entre entidades e identidades, sin regenerar datos al iniciar las pruebas ni ocultar el error con una expectativa distinta. La regresión aislada reproduce una ficha antigua, comprueba las dos etapas, la carpeta estable, el índice actualizado, la repetición sin diferencias y la propagación de errores.

La ampliación600–301a.C., sus87 dossiers/427 autoridades y todo el contenido cultural, geométrico y visual anterior se conservan. No requiere nuevas adquisiciones. Fuentes y límites de investigación: [RESEARCH-bc600](RESEARCH-bc600.md).

## Comprobaciones

Cierre local0.44.1:330 pruebas/70 suites correctas sobre los archivos sincronizados, antes de ejecutar el build de producción. npm run build completo (catálogo, tipos y Vite) correcto; otras dos pruebas del catálogo correctas después del build. Integridad135 recursos de datos/11 franjas tipográficas/9.060 medios correcta. Los135 recursos conservan sus SHA y metadatos anteriores salvo la versión; datos, geometrías y medios públicos no cambian. La ficha e índice deQin coinciden con sus22 registros y las dos etapas canónicas deHuiwen. Evidencia en CATALOG-FIX-0441.json. No se vuelven a adquirir datos ni se afirma haber ejecutado localmente los123 recorridos de navegador; se mantienen los cuatro grupos deCI.

## Publicación

Envío a main con todo el contenido anterior. Se conservan los cuatro grupos de navegador y las condiciones de publicación. El propietario confirma el despliegue; no se espera Actions/Pages.
