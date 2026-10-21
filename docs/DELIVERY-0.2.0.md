# Entrega 0.2.0 · Interfaz compacta

Fecha: 22 de octubre de 2026 (Europe/Madrid).

## Cambios solicitados y realizados

- Cabecera permanente eliminada. Mapa y escenas conceptuales ocupan toda la pantalla.
- Grupo compacto de seis botones arriba a la derecha: búsqueda, cambio de proyección, capas, base de datos/fuentes, pantalla completa e información.
- Proyección con un único botón que alterna 2D/3D y anuncia la acción siguiente.
- Controles laterales de acercar, alejar y restablecer retirados. Pantalla completa trasladada al grupo superior.
- Capas retiradas del panel izquierdo y accesibles mediante un desplegable con cierre exterior y Escape.
- Eliminadas las franjas superior e inferior de la regla, textos auxiliares, botón de volver al presente, extensión temporal y enlace inferior de metodología.
- Fecha seleccionada, play/pausa y saltos reunidos alrededor del indicador fijo central. Entrada de fecha mediante el propio indicador.
- Rueda sobre la regla para zoom temporal anclado a la fecha seleccionada; arrastre para desplazamiento. La rueda sobre el mapa conserva su zoom geográfico.
- Marcas temporales adaptadas a la escala y al área visible. Teclas más/menos como alternativa accesible al zoom de la regla.
- «Acerca de» con favicon, nombre, ficha de versión, descripción, historial, portfolio y repositorio. Referencias locales consultadas: controles de Sizes y estructura de identidad/ficha de Lector. No se modificaron esos proyectos.
- Portfolio recuperado de las referencias y comprobado HTTP 200: https://alejandropico.github.io/Portfolio/ .

## Validación local

| Comprobación | Resultado |
| --- | --- |
| TypeScript y compilación Vite | Correctos |
| Cronología | 6/6 pruebas correctas |
| Recorridos de navegador | 4/4 correctos, incluida la nueva comprobación de zoom independiente |
| Integridad y procedencia | 26 instantáneas verificadas por SHA-256, sin modificar datos |
| Revisión visual | Interfaz compacta, «Acerca de», escritorio y móvil |

Los tres recorridos existentes se adaptaron a los nuevos controles. El cuarto verifica ausencia de barras/controles retirados, orden de herramientas, rueda sobre cada superficie, fecha y cursor fijos al ampliar la regla, apertura/cierre de capas, acceso a fuentes e identidad en móvil. Las capturas de prueba se guardan en `test-results/`, ignorado por Git.

La versión se obtiene de `package.json`. La arquitectura cartográfica, fuentes, instantáneas, licencias y limitaciones científicas permanecen como en la entrega anterior. No se presenta el rediseño como ampliación de la resolución o de la cobertura histórica.

## Publicación

Preparada mediante el flujo habitual de GitHub Actions, que valida antes de publicar en https://alejandropico.github.io/Historicmap/ . El resultado final se añadirá tras completarse el despliegue.
