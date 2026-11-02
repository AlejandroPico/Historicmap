# Fanerozoico hasta los homininos · parte4

Contenido canónico natural de Historicmap0.54.0, separado de Países y de los originales de investigación. No sustituye la expansión humana desde7Ma ni sus yacimientos.

- `escenarios.json`: once intervalos de superficie, Cámbrico–Neógeno hasta7Ma, con fuentes, colores editoriales y alcance visual. Costa reconstruida CAO2024; no simulación climática ni biomas medidos.
- `enciclopedia.json`: veinte artículos propios sobre períodos y conceptos, con apartados, relaciones, fuentes y figuras. Se suman a los21 artículos precámbricos; una subdivisión geológica puede enlazar con el contexto de su período sin ser una monografía independiente.
- `fuentes.json` y `medios.json`: bibliografía y cinco imágenes temáticas, créditos, URL, hash y bytes. Los originales publicados están en `public/earth-media/`, conservados sin recortar.
- `phanda.json` y `originales/PhanDA_GMSTandCO2_percentiles.csv`:85 intervalos del archivo de Judd et al.2024, [PhanDA](https://github.com/EJJudd/PhanDA), commit9f06c0d9764f3da77cb0819e0ac87c01182ba341, [publicación](https://doi.org/10.1126/science.adk3705). En la aplicación se usan los mayores de7Ma; mediana y percentiles16–84 de temperatura/CO₂. Se preservan los límites propios de la publicación, distintos de ICS2026. CO₂ original enppm se convierte a porcentaje dividiendo por10000. No valores anuales ni cierre de una mezcla atmosférica.
- `referencia-audiovisual.json`:31 puntos seleccionados de la transcripción audiovisual solicitada. Se muestran como **escenario del autor**, no consenso ni observaciones. El punto más cercano conserva su edad; no hay interpolación oculta, presión/base húmeda–seca supuesta ni reajuste para sumar100%. Cero gaseoso redondeado se muestra como<0,005%; agua variable no se vuelve cero. La primera etapa contiene vapor de silicatos100%, no nitrógeno100%. Algunas lecturas proceden de la transcripción estructurada; no se afirma verificación manual exhaustiva de todos los fotogramas.
- `revision-video.json`:103 observaciones de parte4 con contexto, decisiones, correcciones y comprobaciones específicas pendientes. Se conserva la trazabilidad sin usar el cursor del vídeo como edad de cada primera aparición. PETM se contextualiza hacia56Ma y K–Pg/Chicxulub hacia66Ma. Los impactos discutidos no se convierten automáticamente en catástrofes representadas.

Reproducir las dos series numéricas: `python scripts/prepare-earth-models.py`. Los artículos, medios y decisiones son curación editorial; no se regeneran mediante ese comando.

## Aspecto y límites

Las superficies usan ruido espacial esférico reproducible, máscaras de costa fechadas y hielo con bordes irregulares. Hielo gondwánico, antártico y episodios precámbricos son escenarios espaciales interpretativos, no modelos de espesor ni contornos glaciológicos recuperados. El modo Ocultar retira también el aspecto polar. PaleoMIST y los datos humanos anteriores conservan su fuente y funcionamiento.

La neblina arcaica anaranjada representa un escenario de aerosoles orgánicos descrito por NASA. La variante rojiza ferruginosa se puede comparar explícitamente desde Planeta entre2,6 y2,1Ga: **no prueba un océano rojo mundial**, ni calcula espectros de reflectancia a partir de porcentajes atmosféricos. No equiparar hierro en sedimentos con color uniforme observado desde el espacio.

Temperatura y CO₂ publicados tienen prioridad en el modo normal; las referencias publicadas de día solar a2,46Ga/620Ma también conservan prioridad. El modo de comparación audiovisual cambia los indicadores, no las geometrías científicas. El formato permite sustituir gradualmente los escenarios por nuevas curvas publicadas con incertidumbre y procedencia.

## Huella de la transcripción · corrección0.54.1

`transcriptionSha256` utiliza los bytes UTF-8 del CSV textual con finales de línea LF: únicamenteCRLF se convierte aLF antes de calcular SHA-256. Coincide con la representación almacenada en Git, aunque el archivo de trabajo deWindows tengaCRLF. `transcriptionHashBasis` declara esta convención. No se modifica el CSV fuente ni se normalizan contenidos, espacios o valores. El CSV original dePhanDA conserva su comprobación binaria exacta independiente.
