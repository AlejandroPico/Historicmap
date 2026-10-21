# Historial de versiones

## 0.2.0 · 2026-10-22

Rediseño del espacio de exploración y de los controles.

- Eliminadas la cabecera permanente, las franjas superior e inferior de la regla y los controles laterales de zoom/restablecimiento.
- Herramientas compactas en la esquina superior derecha: búsqueda, cambio 2D/3D con un único botón, capas, base de datos/fuentes, pantalla completa e información.
- Capas en un panel desplegable con cierre por Escape o al pulsar fuera.
- Fecha seleccionada y reproducción/saltos reunidos en el centro fijo de la regla.
- Rueda sobre la regla para ampliar/reducir su escala sin cambiar la fecha; la rueda sobre el mapa conserva su zoom geográfico.
- Marcas temporales adaptadas al zoom y a la ventana visible, con navegación por arrastre y teclado.
- «Acerca de» con favicon, identidad, ficha de versión, historial, portfolio confirmado y repositorio, siguiendo la estructura de los proyectos del autor.

## 0.1.0 · 2026-10-21

Primera base funcional del atlas temporal.

- Mapa Mercator y globo con cartografía vectorial, selección, zoom y búsqueda.
- Regla móvil con cursor fijo, escala adaptativa, fechas, épocas y reproducción.
- 26 instantáneas con procedencia, licencias y verificación SHA-256.
- Contexto, fuentes, metodología, versión e historial.
- Relieve actual y tres lugares introductorios.
- Diseño adaptable, navegación por teclado y enlaces compartibles.
- Documentación de continuidad y flujos de validación/publicación.
- Teselación subpíxel para evitar exceder límites GPU en costas densas; comprobación de renderizado de todas las instantáneas.
- Movimiento de regla con marcas reutilizadas y sincronización limitada del enlace compartible para mantenerlo correcto durante la reproducción.

Cobertura inicial discontinua. Alta resolución local, revisión historiográfica exhaustiva, homininos, hielo, atmósfera y eventos bélicos pendientes. Ver `agentes.md`.
