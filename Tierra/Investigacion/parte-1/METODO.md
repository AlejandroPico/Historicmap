# Método de inspección y reproducción

Esta investigación usa vídeo público sin autenticación. Los dos documentos aportados se copiaron sin normalizar bytes. Se conserva SHA-256 de cada original, del vídeo adquirido, de las dos referencias ICS y de los950 fotogramas de trabajo. La descarga del vídeo no forma parte del material publicado.

## Captura

Formato nativo de trabajo: vídeo401 de YouTube,3840×2160, AV1,30fps. Descripción, metadatos y subtítulos manuales ingleses separados. La descripción y los créditos no especifican una licencia general de reutilización de la animación.

Extracción con FFmpeg7.1, JPEG calidad3, sin cambiar resolución:

```text
select='if(lt(t,650),not(mod(n,30)),if(lt(t,690),not(mod(n,8)),1))'
```

Índice cero de los fotogramas derivados:

- `0..649`: segundo igual al índice.
- `650..799`: fotograma original `19504 + 8*(índice-650)`; dividir entre30 para tiempo.
- `800..949`: segundo `690 + (índice-800)/30`.

No es una extracción de todos los fotogramas antes de690s. Los tiempos de detección no son límites exactos de entrada/salida de los textos.

## Reconocimiento y revisión

RapidOCR1.4.4 y ONNX Runtime1.31.1 en entorno privado. Indicadores: reconocedor de líneas,16 recortes fijos por fotograma; canal máximo RGB y corrección de contraste para texto oscuro. Se conserva texto y confianza de reconocimiento. Una confianza alta sólo informa del reconocimiento, **no** de certeza científica.

Regiones aproximadas en píxeles nativos: edad `(0,1480)–(1070,1650)`, temperatura en la esquina superior izquierda, duración del día `(3190,865)–(3840,1030)`, nueve valores de gases en el borde superior derecho, cuatro valores jerárquicos entre `x1410..2000` y `y1700..2150`. La tabla inicial es distinta: se comprobó visualmente vapor de roca antes de asignar valores a gases. Los indicadores se publican sólo mientras hay una edad reconocible y la imagen corresponde al segmento planetario16–682s.

Acontecimientos: región inferior derecha desde aproximadamente `(1940,1060)`, enmascarando el interior del mapa elíptico para reducir falsos textos. Se muestreó cada4s al principio, cada segunda muestra entre650–690s y cada tercera en el final. Se omitieron máscaras vacías/idénticas; reconocimiento de texto, agrupación aproximada y revisión editorial de títulos factuales. También se revisaron títulos sin guion final y anotaciones originales. Puede haber omisiones por rótulos breves, desvanecidos, solapados o fuera de esa región.

La bibliografía se recuperó del fotograma nativo próximo691.5s; sus29 entradas son referencias detectadas, no una afirmación de haber leído todos los trabajos. Se corrigieron algunos errores de reconocimiento obvios, manteniendo el estado de revisión pendiente. El CSV conserva variantes OCR; no debe usarse como interfaz española ni como serie científica definitiva.

## Reproducibilidad y pendientes

El algoritmo anterior, las versiones declaradas y el original identificado por hash permiten repetir la captura. Los JPEG pueden diferir con otra versión/codificador: los hashes certifican los archivos usados, no una identidad universal de todas las codificaciones.

La comprobación pública no necesita los medios privados. Las partes3–5 deberán revisar visualmente los segmentos que implementen, resolver las referencias, cotejar celdas dudosas y registrar fuentes actuales por indicador/escena. Las curvas aprobadas se producirán entonces en sus carpetas científicas propias; este material permanece como referencia fechada.
