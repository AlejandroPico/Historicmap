# Entrega0.9.1 · cierre de la ampliación a1960

Estado: 0.9.1 subida a main en c42531df6fafe5fdd9c6fc999a80741aa1829076 (candidato anterior; sustituido por el siguiente commit con cinco retratos adicionales). Quality 40009382574 en curso; todavía no acredita publicación de 0.9.1.

La0.9.0 ya pasó114 unitarias y28 recorridos de navegador en [Quality40005916966](https://github.com/AlejandroPico/Historicmap/actions/runs/40005916966). [Pages40008258279](https://github.com/AlejandroPico/Historicmap/actions/runs/40008258279) publicó `ba7eb3b8ab505a277f5fb5f59c6e18eeb06084af`. Se cotejaron públicamente los bytes de cuatro archivos de aplicación, tres manifiestos, siete conjuntos de datos y nueve medios focales con la compilación correspondiente.

## Corrección

El preparador de1960 recogía los retratos después de eliminar los mandatos que debía regenerar. Ahora recoge primero los medios acreditados. La revisión recuperó26 retratos que ya estaban en el inventario y añade una regresión sobre Abdoh. No se crean26 archivos nuevos ni se sustituyen imágenes sin licencia.

La Nigeria de1963 distingue la presidencia parlamentaria de Azikiwe del Gobierno de Balewa. Se elimina el cargo genérico duplicado y la consolidación respeta las correcciones revisadas. Los extremos de mandato de enero1966 siguen identificados como pendientes de contraste diario.

Catálogo final:283 claves y7.480 mandatos,3.793 medios (439 SVG y3.354 fotografías). Auditoría1960–1969:1.693 país-años sin huecos de resolución de autoridad,91 personas/órganos sin retrato y20 país-años sin bandera (Andorra/San Marino). No acredita todos los cargos ni una reconstrucción exhaustiva mundial.

Las pistas de investigación están en `reference/portrait-1960-pending-research.json`:76 personas sin fotografía P18 en la fuente consultada,12 candidatos pendientes de identificación/licencia/adquisición y tres órganos o identificadores documentales. Una candidatura no equivale a una imagen aprobada. Las listas anteriores de122 se refieren al estado publicado en0.9.0, no al resultado de esta corrección.

## Pendientes que continúan

- CSV original del propietario no disponible; cotejarlo cuando se vuelva a aportar. `POLITICAL-PALETTE.csv` es la exportación editorial propia de33 familias.
- Los91 registros sin retrato, variantes de bandera de AND/SMR, suplencias y extremos diarios que identifican las investigaciones.
- Frentes y control detallado fuera de los contornos documentados, sectores aliados de Alemania y fichas tempranas fuera de la ventana revisada.

## Validación y publicación

115 pruebas unitarias locales correctas tras la corrección de cargos;17 comprobaciones focales correctas tras recuperar imágenes. Verificación final, Quality, Pages y comprobación pública de0.9.1 pendientes. Mantener `tareas.md` actualizado hasta cerrar esos pasos.

La repetición íntegra del preparador de 1960 conserva exactamente los bytes del catálogo, incluidos los retratos. La comprobación manual de 0.9.1 muestra Nigeria con Balewa y Azikiwe, imágenes y funciones separadas. La compilación local y los datos servidos se cotejan antes de probar para evitar mezclar versiones.

La auditoría final descubre y corrige la falsa coincidencia ND en GODL-India. Se incorporan cinco archivos adicionales de autoridades de India, con sus fuentes y licencias; las26 recuperaciones anteriores eran referencias a medios ya existentes. El total final es3.793 medios y91 personas/órganos sin retrato (76 sin P18,12 candidatos pendientes y tres órganos/identificadores). El filtro de NoDerivatives se mantiene y no se amplía la lista de licencias aceptadas. La entrega definitiva debe cotejar el siguiente commit, no el candidato c42531d.

Quality/Pages evitan que una revisión superada publique después de la vigente. No hay que interpretar un Pages omitido por ese control como una publicación de su candidato antiguo.
