# Entrega 0.13.0

Preparación local del25/10/2026, rama `codex/1880-history`, desde `4cc2bbb5c9efb0918d3a53709610b1ffa1e4ae12`. El propietario confirma la publicación anterior. No se consulta ni espera Actions/Pages.

## Cambios

Ampliación1880–1899, resolución de identidades entreCliopatria yCShapes, autoridades regionales, símbolos, relaciones coloniales, contexto y transiciones. Groenlandia dispone de una referencia seleccionable1886–2019; Hawái conserva fases propias antes de integrarse enEEUU sobre su geometría fechada exacta.

Correcciones solicitadas: retratos deIrak,Tayikistán,Bután,Bangladesh,Vietnam,Francia1900,India yNepal; eliminación de personajes ficticios deEEUU/ReinoUnido y protección de la adquisición. India suma12 titulares con retrato que antes carecían de él; no quedan titulares sin imagen en su catálogo disponible. Nepal suma siete, conRijal pendiente. La foto deChapo ya era individual; falta una fotografía individual reutilizable deMariaLevi.

Inventario:366 claves/10.916 registros de autoridad;5.613 medios,507SVG y5.106 imágenes raster. Se preservan10.016 registros que alcanzan1900+, salvo las correcciones expresamente solicitadas. Originales cartográficos y particiones1940–1944 idénticos byte a byte al punto de partida.

Auditoría1880–1899:2.723 entidades/año,123 casos anuales sin autoridad resuelta,40 personas/órganos sin imagen y530 casos anuales sin símbolo. Listas nominales enREVIEW-1880-1899.json, fuentes y límites enRESEARCH-1880. No presentar estos resultados como un censo diario completo ni como fronteras mundiales verificadas exhaustivamente.

## Verificación local

-154 pruebas/35 archivos correctos; tipos correctos.
-Cinco regresiones sin conexión del filtro de autoridades reales correctas.
-Siete curadores puros/idempotentes; conservación de los registros posteriores comprobada.
-49 recursos de datos,11 franjas tipográficas y5.613 medios íntegros porSHA-256.
-Compilación correcta en`.cache/build-013-final`; advertencia de tamaño delpaquete principal. No se ha reducido la cartografía para ocultarla.
-Cuatro recorridos distintos de navegador correctos: fuentes/capas, retratos notificados, clic real deGroenlandia y1880–1899. Repetición final con bandera decodificada correcta; captura móvil revisada. El primer fallo1880 era una selección ambigua de la prueba entreEEUU yel nombre histórico deBrasil; se elige explícitamente el resultado correcto.

La primera suite detectó dos expectativas de cobertura anteriores a1880; se actualizaron con aserciones positivas de datos tempranos y límites anteriores a la cobertura. El verificador detectó colisión de identificadores entre registros y relaciones deHawái y formato de registro de nuevos recursos; corregidos sin omitir validaciones. Una regresión geográfica detectó el doble contorno deHawái1898; se sustituyó por transferencia exacta deCShapes y se retiró la referencia anterior desde1898.

## Estado de entrega

Preparación local. Confirmar en el mensaje final el resultado real delenvío aGit. La verificación deldespliegue corresponde alaviso posterior delpropietario; no confundirla conla compilación local.


Cierre: aplicación33637c5 enviada correctamente aorigin/main el25/10/2026. Verificados los5673 recursos preparados enGit. Compilación final en.cache/build-013-final con los mismos archivosJS/CSS que la compilación examinada; normalizaciónLF deJSON y manifiestos íntegros. Despliegue pendiente de aviso del propietario; no consultado.
