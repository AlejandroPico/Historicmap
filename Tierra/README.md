# Tierra · evidencias naturales

Catálogo canónico de reconstrucciones y cronologías naturales. Los datos de países, comunidades y yacimientos permanecen en `Países/`; un manto de hielo no es una entidad política.

- `Cuaternario/cronologia.json`: edades, épocas de referencia y fuentes estratigráficas. BP1950 y b2k no son intercambiables; la cronología civil no tiene año cero.
- `Cuaternario/PaleoMIST-1.0/fuentes.json`: atribución, licencia, originales, miembros de archivo y sumas de comprobación de los márgenes de hielo.
- `Cuaternario/PaleoMIST-1.0/originales/`: archivos GMT WGS84 y lecturas originales, sin modificación.

Los datos de PaleoMIST 1.0 son de Evan J. Gowan y colaboradores, [PANGAEA, DOI 10.1594/PANGAEA.905800](https://doi.pangaea.de/10.1594/PANGAEA.905800), bajo [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). Los derivados conservan detalle geográfico, dividen el antimeridiano y cierran casquetes polares; no son una nueva simulación científica. El código de reproducción es `scripts/prepare-ice-margins.mjs`; no contiene contornos científicos dibujados manualmente. Las muestras compiladas y su procedencia se registran en `public/data/manifest.json`.

La consulta sólo presenta las edades disponibles del modelo, con sus límites. No se infieren paleocostas, hielo marino o glaciares ausentes del conjunto. En 0.50 hay 92 originales, cuatro regiones y 23 muestras de 0–80000 BP1950, separadas por 2500–5000 años. La cobertura se detiene en 78051 a. C.; no se dibuja hielo anterior por extrapolación. Las paleocostas siguen pendientes. Véase [investigación y alcance](../docs/RESEARCH-bc100000.md).
