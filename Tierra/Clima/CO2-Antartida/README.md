# Compuesto antártico de CO₂

Original: `originales/antarctica2015co2composite-noaa.txt`, conservado sin cambiar bytes. Colección de Bereiter et al.2015, NOAA/WDS, [DOI del conjunto](https://doi.org/10.25921/n8y4-bp27), [publicación](https://doi.org/10.1002/2014GL061957), [ficha17975](https://www.ncei.noaa.gov/access/paleo-search/study/17975).

Contiene1.901 observaciones de edad del gas en años calendario BP1950, concentraciónppm y error1σ de la colección. Los gases no tienen necesariamente la edad del hielo que los contiene. Se mantienen los ajustes y edades del compuesto publicado; no se recalibra ni se normaliza la serie.

Compilación offline: `scripts/prepare-human-knowledge.py` desde la raíz. La salida `public/data/ice-core-co2.json` conserva el hash binario original, las filas completas y sus metadatos. `--check` comprueba reproducibilidad sin escribir. La aplicación consulta la muestra real más cercana, con su edad visible, dentro del registro; no interpola observaciones anuales ni extrapola a épocas sin datos. La referencia se utiliza en prehistoria hasta10001a.C.; no sustituye datos modernos o históricos.

La curva es composición atmosférica; no una reconstrucción de temperatura global, extensión del hielo o paleocosta. La representación en porcentaje convierteppm/10.000, conservando los valores originales. Véase [quinta parte](../../../docs/EARTH-HUMANITY-0.55.md).
