# Investigación terrestre · parte 1 de 6

Auditoría de preparación del 1 de noviembre de 2026. Aplicación y datos de producción: **0.51.1, sin modificaciones**.

El [informe de lectura](../../../docs/AUDIT-EARTH-PART-1.md) explica las conclusiones, el alcance real de la inspección y los trabajos de las cinco partes siguientes. Este directorio contiene material de investigación; **ningún archivo se importa automáticamente en el mapa**.

| Archivo | Contenido |
| --- | --- |
| `procedencia.json` | Entradas originales, hashes, vídeo, créditos y versiones de referencia |
| `comparacion-homininos.json` | Las 38 entradas del documento frente al catálogo actual de 35 fichas; alternativas, sinónimos y poblaciones |
| `comparacion-glaciaciones.json` | Las 11 entradas glaciales, errores de equivalencia y episodios omitidos |
| `fuentes.json` | Referencias primarias/institucionales y alcance de cada contraste |
| `inventario-video.json` | 198 acontecimientos/candidatos observados y 13 notas suplementarias, con tiempos y estado de revisión |
| `indicadores-video.json` | Semántica, unidades, límites y comprobaciones manuales de los campos planetarios |
| `muestras-indicadores-video.csv` | 754 muestras numéricas y etiquetas; OCR con confianza, no curvas científicas aprobadas |
| `bibliografia-video.json` | 29 referencias detectadas en los créditos; resolución/revisión bibliográfica completa pendiente |
| `cobertura-video.json` | Muestreo, limitaciones y hashes de los 950 fotogramas privados analizados |
| `originales/` | Los dos documentos aportados y las referencias oficiales ICS, con atribución |

Los acontecimientos son **observaciones de un vídeo**, no una lista de hechos aceptados sin matices. `observedAgeMa` es la edad del cursor en la muestra que contiene el rótulo; no acredita la fecha exacta del suceso. `authorEventAgeMa: null` evita atribuirle una fecha que no se ha leído explícitamente.

El vídeo, fotogramas, subtítulos completos y OCR narrativo permanecen privados en `.cache/video-audit/`. No se redistribuyen. Se preservan nombres factuales, números, tiempos, referencias y notas editoriales propias.

Comprobación independiente, desde la raíz del repositorio, con Python 3:

```text
python scripts/check-earth-research.py
```

No necesita descargar el vídeo, instalar OCR ni ejecutar los navegadores. La inspección audiovisual adicional y la validación científica por escena corresponden a las partes 3–5; sus huecos están declarados y no se deben interpretar como tareas ya hechas.
