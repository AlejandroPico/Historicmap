# Corrección 0.11.1 · pruebas de publicación

24 de octubre de 2026. El propietario aporta el resultado de Quality de 0.11.0: 27 recorridos correctos y tres fallidos, y autoriza corregir y subir sin esperar el despliegue. No se ha consultado ni sondeado Actions/Pages.

## Causas y correcciones

| Fallo comunicado | Comportamiento vigente | Comprobación corregida |
| --- | --- | --- |
| Selector de organizaciones esperado como desactivado en 1947 | La cobertura se amplió a 1920 y la ONU ya existía en 1947 | Selector habilitado; ONU con 57 miembros al cierre de 1947; OTAN todavía inactiva; selector desactivado y selección vacía en 1919 |
| Ninguna autoridad esperada en Alemania occidental de 1946 | Ahora se documentan las administraciones aliadas colectivas | Nombre del órgano exacto, sin bandera nacional alemana ni retrato personal ficticio, y sin atribuir la administración conjunta sólo a Truman |
| Selector de persona única para España en 1939 | La ficha reúne los mandatos del año, incluidos Azaña y Franco en periodos distintos | Comprobaciones individuales de ambos nombres y fin del mandato de Azaña el 27/2/1939; no se eliminan datos para obtener una única persona |

Los dos archivos afectados esperan además la cartografía renderizada antes de interactuar con las capas o fichas, manteniendo la comprobación de descarga. La ayuda visible de organizaciones se actualiza de 1960 a 1920. Versión y documentación pasan a 0.11.1.

No cambian las autoridades, banderas, medios, fronteras o manifiestos históricos. No se omite ningún recorrido, no se añaden reintentos ni se modifican los flujos de Quality/Pages. Las carencias de investigación de 0.11.0 siguen registradas en tareas.md.

## Validación y entrega

Validación local correcta: **129 pruebas unitarias en 28 archivos**, tipos y compilación de producción. **Los tres recorridos afectados pasan** en 2,6 minutos, incluida la parte móvil que no se alcanzaba antes del fallo de España en 1939. Se conservan las comprobaciones de fronteras, imágenes, banderas, relieve y adaptación del resto de esos recorridos. La compilación mantiene el aviso de tamaño del paquete principal; no es un error ni se ha silenciado.

Los otros 27 recorridos figuran como correctos en el registro de 0.11.0 aportado por el propietario; no se presentan como repetidos localmente en esta corrección. Se comprobó que `public/`, `Países/` y `.github/` no cambian frente a 8990dcc. No se han readquirido datos, alterado medios ni reducido la suite.

El flujo termina al confirmar el envío a main. La publicación y sus comprobaciones quedan pendientes del aviso del propietario.
