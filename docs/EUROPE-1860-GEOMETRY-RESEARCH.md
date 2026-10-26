# CShapes-Europe 1860–1885: evaluación acotada

Resultado: **no integrar automáticamente en 0.14**. La descarga europea permite investigar fronteras políticas anteriores a 1886, pero no acredita por sí sola una mejora de definición costera o un reemplazo mundial completo. La corrección del problema de selección de Cliopatria debe mantenerse separada de esta decisión cartográfica.

## Archivo evaluado y mediciones

Entrada original conservada: `.cache/cshapes-europe-014.geojson`, 322 elementos y 4.574.391 bytes. Sus propiedades son `From`, `To`, `Id`, `Holder`, `Name`, `Status`, `Area`, capital y centroide. Entre 1860 y 1885 intervienen 93 registros. El análisis reproducible está en `.cache/analyse-europe-014.py` y su salida en `.cache/cshapes-europe-014-audit.json`; ninguno escribe en `public/`.

Todos los vértices de los 93 registros evaluados están cuantizados a **0,02 grados**, medido comprobando que cada ordenada multiplicada por 50 es entera dentro de tolerancia numérica. Ese paso equivale aproximadamente a 2,2 km de latitud: no constituye una costa de alta definición. No se recomienda suavizarlo o añadir puntos interpolados, porque aumentaría la apariencia de detalle sin aportar observaciones.

Se encontraron cinco geometrías inválidas: cuatro registros de Francia y uno de Islandia. Francia presenta autointersección en `[-3.56, 48.8]`. No se repararon silenciosamente: una reparación geométrica debe someterse a revisión de las partes conservadas, área y triangulación.

Áreas aproximadas geodésicas, calculadas sobre WGS84, y extensión espacial observada:

| Nombre de fuente | Ejemplo de área / detalle | Consecuencia |
| --- | --- | --- |
| Russia | 5,32–5,36 millones km²; límite oriental 68,26°E | Es un recorte, no todo el Imperio ruso. Sustituir su geometría mundial eliminaría Siberia y otros territorios. |
| Ottoman Empire | 542.196 km² en 1860; 216.194 en 1885 | Cobertura europea parcial. No representa integralmente Anatolia, Levante, Arabia y posesiones africanas. |
| Spain | 498.469 km²; oeste -9,30° | Incluye península y Baleares; faltan Canarias y otras posesiones. No sustituye un registro mundial español. |
| Portugal | 88.524 km²; oeste -9,50° | Sólo Portugal continental, sin Azores ni Madeira y sin posesiones coloniales. |
| United Kingdom | 313.362 km² en 1885; 316.243 antes de 1865 | El recorte excluye posesiones extraeuropeas; la variación anterior requiere distinguir las islas Jónicas y otros ámbitos. |
| Sweden | 766.073 km²; oeste 4,80° | Agrupa Suecia y Noruega. No se debe sustituir Suecia y conservar a la vez una Noruega separada por encima. |
| Netherlands | 37.396 km² hasta 1867, después 34.811 | El primer contorno incluye Luxemburgo. La unión personal no permite presentarlo como anexión moderna ni duplicar Luxemburgo. |
| France | 900–965 vértices según fase; todas las fases evaluadas inválidas | La costa es cuantizada y necesita reparación/validación antes de cualquier comparación con la base actual. Colonias ausentes. |
| Belgium | 30.688 km², 175 vértices, válida | Candidato de ámbito europeo completo, sujeto a verificación de resolución y de costuras con vecinos. No hereda el Congo por identidad del soberano. |
| Switzerland | 41.565 km², 241 vértices, válida | Candidato territorial completo, sin mejora costera posible al ser interior. Necesita contraste de fronteras y resolución con la base. |
| Monaco | 21 km² y ocho vértices desde 1861 | La muy baja resolución exige contraste específico; no usar como mejora automática de un microestado. |

`Status=independent` no se puede consumir literalmente: Malta tiene `Holder=200` (Reino Unido) y Islandia `Holder=390` (Dinamarca), mientras ambos conservan ese valor de `Status` en el archivo. Es imprescindible interpretar `Holder` y contrastar las instituciones históricas.

## Precisión temporal e identidad

`From` y `To` contienen años, **no días ni meses**. No se debe convertir esta información en una cronología diaria supuestamente acreditada.

Ejemplos observados: Francia conserva el contorno anterior a la incorporación de Niza/Saboya hasta `To=1860` y cambia en `From=1861`; el nombre `Italy` aparece desde 1862, mientras `Piedmont` sigue hasta 1861. Esto es compatible con una referencia anual que precede a determinados eventos del año, pero el archivo por sí solo no demuestra una convención universal de 1 de enero. La nota del sitio sobre distancias calculadas a 1 de enero se refiere a esa serie derivada, no basta para atribuir la misma convención a cada geometría europea.

Las transiciones políticas verificadas de 1861 y 1867 deben mantenerse separadas de las ventanas de representación de este inventario. No se cambia una frontera sólo por cambiar el título del Estado.

Correspondencias que exigiría una preparación futura:

- `Germany` antes de 1871: Prusia (`PRUSSIA`), no el Imperio alemán. El registro de 1867–1870 mide unos 345.833 km² y no acredita por sí solo el contorno de toda la Confederación Alemana del Norte.
- `Austria-Hungary` antes de 1867: Imperio austríaco (`AUSTRIAN-EMPIRE`). El nombre posterior es un anacronismo del inventario en esas filas.
- `Piedmont`: Reino de Cerdeña (`SAR`); no se traduce automáticamente por Italia antes de la ley del 17 de marzo de 1861.
- `Kingdom of Naples`: investigar el Reino de las Dos Sicilias y su control efectivo; no asumir que el nombre limita la geometría sólo a Nápoles, porque incluye Sicilia.
- `Sweden`: unión sueco-noruega en el ámbito de esa geometría, con correspondencia separada para autoridades y países constituyentes si se decide desagregar.

## Lista blanca condicional y criterio de sustitución

La lista blanca **para comparación**, todavía no para publicación automática, se limita a Bélgica y Suiza. Sus geometrías evaluadas son válidas y no se observó un recorte continental comparable al ruso u otomano. Andorra, Liechtenstein y San Marino pueden servir como puntos de contraste de ubicación, pero la cuadrícula de 0,02° les afecta proporcionalmente mucho y no ofrece una mejora de definición demostrada.

No hay una mejora visual medida frente a Cliopatria para ningún candidato. Antes de adoptar uno deben compararse área, componentes, vértices, extensión y precisión documental de ambas fuentes. Además, una frontera compartida requiere revisar ambos lados: sustituir el polígono de un único país puede producir solapamientos o huecos en el vecino aunque ambos polígonos sean válidos por separado.

La integración futura deberá ser una **sustitución de geometría de la partición base**, retirando el ámbito anterior equivalente y reconstruyendo sus adyacencias; nunca una capa de relleno adicional. Sólo se admitirá reemplazar la geometría mundial completa si el registro sustituto cubre exactamente el mismo ámbito territorial. Un reemplazo regional exige una operación de partición documentada que conserve por separado los componentes exteriores, sin duplicaciones ni recortes por rectángulos arbitrarios. No se preparó una operación de ese tipo en esta investigación.

## Procedencia y licencia

El [sitio oficial de ICR-ETH](https://icr.ethz.ch/data/cshapes/) publica CShapes-Europe desde 1816 y distingue esta extensión de CShapes 2.0 mundial, cuyo inicio es 1886. Para Europa solicita citar: Cederman, Lars-Erik; Luc Girardin; Carl Müller-Crepon; Yannick Pengl (2025), *Nationalism and the Transformation of the State: Border Change and Political Violence in the Modern World*, Cambridge University Press.

El mismo sitio indica [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/). Una incorporación deberá conservar atribución, procedencia, licencia y descripción de las transformaciones del material cartográfico. No se debe etiquetar este conjunto como dominio público ni confundirlo con la licencia del paquete de software R. El proyecto ya conserva el texto de la licencia de CShapes en `public/data/LICENSE-CShapes.txt`; no se ha alterado.

## Pendiente concreto

1. Buscar una costa mejor documentada para las geometrías anteriores a 1886 sin desplazar límites políticos por aproximación estética.
2. Comparar Bélgica y Suiza contra la fuente base, con diferencias de área y pruebas de adyacencia, antes de considerar su adopción.
3. Confirmar la convención temporal anual europea con documentación específica o con los autores; no deducir días de sus años.
4. Auditar uniones personales, dependencias y territorios recortados antes de ampliar la lista blanca.

La investigación no modifica cartografía publicada, identidades, controles políticos ni código de representación.
