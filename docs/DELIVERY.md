# Entrega inicial · 0.1.0

Fecha: 21 de octubre de 2026 (Europe/Madrid).

## Resultado

Aplicación funcional subida a `main` del repositorio. Commit inicial del producto: `1504220793dc76b77909ce5872de4f2320655f59`. La especificación y el estado de cada función se encuentran en `agentes.md`. Los cambios documentales posteriores no modifican esa versión del producto.

## Validación local completada

| Comprobación | Resultado |
| --- | --- |
| Integridad y procedencia de datos | 26 instantáneas verificadas por SHA-256 |
| Pruebas de cronología | 6/6 correctas |
| Recorridos de navegador | 2/2 correctos; incluye geometrías renderizadas, búsqueda, proyección, instantáneas, fecha exacta, cursor fijo y móvil |
| TypeScript y compilación Vite | Correctos con Node 26.12.1 |
| Auditoría de dependencias de producción | 0 vulnerabilidades reportadas al realizar la entrega |
| Revisión visual | Vista contemporánea, globo, mundo antiguo, reconstrucción de 300 Ma y disposición móvil |

Las capturas de las pruebas locales están en `test-results/`, carpeta ignorada por Git. Los flujos de GitHub adjuntan su propio artefacto de comprobaciones. La revisión visual final retiró las líneas internas de fragmentos tectónicos para evitar que pareciesen fronteras políticas y ajustó la altura del panel para que pueda desplazarse sin quedar oculto detrás de la regla.

## Publicación

- **Quality: correcto.** https://github.com/AlejandroPico/Historicmap/actions/runs/39663607676
- **Publish atlas: correcto.** https://github.com/AlejandroPico/Historicmap/actions/runs/39663873837
- **Web publicada:** https://alejandropico.github.io/Historicmap/
- Verificado HTTP 200 y renderizado de territorios con relieve en el navegador desde el origen público, incluidos los recursos bajo `/Historicmap/` y el worker empaquetado.

El commit de cierre incorpora únicamente este informe documental. No cambia código, dependencias ni datos, por lo que se omite repetir la compilación/despliegue ya validados del commit de producto.

## Prioridades del siguiente relevo

1. Costa contemporánea de mayor resolución, revisión de fronteras vigentes y disputadas, y actualización reproducible.
2. Auditoría historiográfica de los conjuntos incorporados y ampliación documentada por periodos/regiones.
3. Yacimientos, homininos, paleocostas y hielo del Cuaternario.
4. Mayor detalle visual y científico de las reconstrucciones antiguas, manteniendo fuentes e incertidumbre.

La URL del portfolio personal está pendiente de confirmación. No se ha sustituido por un portfolio inventado. El perfil público y el repositorio sí están enlazados en «Acerca de».
