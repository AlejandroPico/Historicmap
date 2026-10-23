# Entrega 0.9.0 · control territorial, paleta e historia desde 1960

Estado: **publicada y comprobada** en ba7eb3b8ab505a277f5fb5f59c6e18eeb06084af. Esta ficha describe0.9.0; la corrección posterior y los pendientes actualizados están en DELIVERY-0.9.1 y ../tareas.md.

## Cambios

- El inventario mostrado compone geometrías de control y territorios en un worker. El controlador se selecciona con las franjas apagadas o encendidas. El interruptor no restaura fronteras soberanas como si fueran control efectivo.
- Franjas opcionales, apagadas inicialmente: tres cuartos de anchura para controlador y un cuarto para territorio ocupado. Las incorporaciones ya documentadas y el ámbito alemán de 1938 no reciben franjas de ocupación; no se inventan subdivisiones de anexión que las fuentes no contienen.
- La Guerra Civil española usa sus particiones independientes. No se recortan geometrías CShapes NC-SA con el frente BY-SA 3.0; se reemplazan los componentes peninsulares/insulares cubiertos como colección de fuentes separadas. Se conservan los componentes españoles fuera de esa cobertura. Ningún archivo de coordenadas original se reescribe.
- Fondo terrestre contemporáneo de referencia bajo todo el dominio histórico cartográfico. Un hueco político es tierra sin entidad en ese inventario; no demuestra ausencia de población, organización política o conocimiento local. No es una paleocosta reconstruida.
- Paleta editorial ampliada, familias históricas y matices de dependencia. Reino Unido rosa malva frente a rojo soviético; Roma púrpura, Bizancio violeta distinto, imperio español dorado, Francia napoleónica azul y Alemania nazi gris. Las tintas no clasifican ideologías antiguas. `POLITICAL-PALETTE.csv` exporta la convención implementada.
- Adquisición y curaciones 1960–1969, Estados históricos YMK/TAN/ZAN/UAR, República Árabe Unida territorialmente agrupada hasta 1960 y separación siria desde el cierre de 1961. UNTEA distingue Rolz-Bennett y Abdoh; nombramiento y toma de funciones no se confunden.
- Nuevos intervalos de símbolos, mandatos, contexto, instituciones y relaciones navegables. Membresías desde 1960 sin proyectar alianzas posteriores ni confundir asociación y tutela.
- Las geometrías idénticas recibidas del worker conservan la actualización incremental del mapa: una copia de los mismos puntos no vuelve a procesar todas las costas. El recorte omite entidades que no intersectan el control.

Catálogo:283 claves/7.481 mandatos;3.788 medios,439 SVG y3.349 fotografías. Frente a0.8.1 son268 archivos fotográficos y44 SVG adicionales, con licencia/crédito individual.53 intervalos de símbolos curados.31 organizaciones/549 intervalos de membresía,258 fases de contexto y59 relaciones/53 registros históricos e institucionales.

## Entrada no disponible

El CSV del propietario `C:/Users/darim/Downloads/lista_imperios_completa_v3.csv` no estaba disponible al intentar leerlo y no se localizó en las búsquedas realizadas. **No se ha importado ni reconstruido como si se hubiese leído.** Se aplican las preferencias verbales y una paleta propia explícita; la conciliación fila por fila del CSV queda pendiente de recuperar el archivo.

## Límites que continúan abiertos

- La auditoría comprueba resolución de autoridades por país-año, no todos los cargos, suplencias o días de mandato. Ventanas documentales se rotulan como límites de cobertura y los extremos inciertos no se convierten en dimisiones.
- Retratos ausentes, órganos colectivos sin fotografía individual, variantes de bandera y fechas diarias pendientes deben conservarse en `REVIEW-1960.json`, investigaciones focales y `tareas.md`.
- Frentes de Biafra, Congo, Vietnam, particiones detalladas del Levante, anexiones parciales que faltan en la fuente, sectores de Berlín y control reciente completo siguen pendientes. Los contornos de campaña tienen fecha y precisión desiguales.
- La tierra de referencia no resuelve costas históricas ni atribuye soberanía. Las geometrías de control de menor resolución pueden diferir de la costa territorial detallada. No se reducen las coordenadas originales para ocultarlo.
- La paleta todavía requiere ampliación documentada por regímenes/regiones; no existe una clasificación ideológica automática de todos los gobiernos del mundo.

## Validación real hasta este punto

- Tipos y compilación local inicial correctos.
- Cuatro pruebas de composición/control y dos de paleta correctas, incluida geometría real de 1942.
- Tres recorridos focales de navegador correctos: selección de controlador con franjas, tierra en 1889/1918, símbolos/autoridades de ambas guerras y Francia revolucionaria/napoleónica, móvil. La revisión visual confirma las franjas; una captura prematura anterior al idle no las mostraba y se corrigió la espera.
- Auditoría ampliada a suplementos: **1.693 país-años 1960–1969**, sin huecos de resolución de autoridad;122 personas/órganos sin retrato y20 país-años sin bandera (Andorra y San Marino). Lista concreta en `REVIEW-1960.json`. La foto alternativa de De Gaulle se identificó y revisó separadamente; no se flexibiliza el filtro automático de licencias.
- Suite completa final, integridad, versión final y publicación: pendientes; no considerar esta lista una aprobación de esos pasos.

## Cierre comprobado de0.9.0

[Quality40005916966](https://github.com/AlejandroPico/Historicmap/actions/runs/40005916966):114 pruebas unitarias/23 archivos, integridad43/11/3.788 y28 recorridos de navegador correctos. El recorrido anual1789–2026 tardó3,2min y el caso de reproducción/perfiles40,4s en CI; no confundir el tiempo total del caso con el intervalo de reproducción. [Pages40008258279](https://github.com/AlejandroPico/Historicmap/actions/runs/40008258279) terminó correctamente. Cotejo público de4 archivos de aplicación,3 manifiestos,7 conjuntos de datos y9 medios focales en reference/public-verification-0.9.0.json.

Las pasadas locales iniciales registraron fallos: directorio servido reconstruido durante una prueba, una compilación mezclada durante el cambio de rama y tiempos excedidos en Chromium por software. Se corrigió el reprocesado de geometrías clonadas y se repitió la validación en CI completo. Las pruebas manuales del navegador integrado confirmaron Nigeria1960, TAN→TZA1964 y reproducción1938→1942 en14,3s. No se afirma que todas las pasadas locales fueran correctas.
