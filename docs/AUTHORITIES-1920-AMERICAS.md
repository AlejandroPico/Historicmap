# Autoridades americanas · huecos focales1920–1949

Revisión24/10/2026 para0.11. `scripts/curate-1920-americas.py` prepara **35 registros en9 claves** para huecos nominales concretos de `.cache/coverage-1920.json`, `coverage-1930.json` y `coverage-1940.json`. En la prueba en memoria resuelve presencia de autoridad en los **61 país-años ausentes** de esas nueve claves. Esto no acredita un inventario completo de todos los cargos, suplencias o meses.

## Alcance y fuentes

| Clave | Registros focales | Fuentes institucionales/documentales |
|---|---|---|
| PAN | Lefevre; Porras; Florencio Harmodio Arosemena; Juan Demóstenes Arosemena; Fernández Jaén; Boyd; De la Guardia | [Gobernantes de Panamá, inventario documental deGovInfo](https://www.govinfo.gov/content/pkg/GOVPUB-W79-ad59626cf1c66b2408af30aa698366f9/pdf/GOVPUB-W79-ad59626cf1c66b2408af30aa698366f9.pdf); [Biblioteca Nacional, capítulo1941–1945](https://bdigital.binal.ac.pa/bdp/older/republicano14.pdf). El índice de búsqueda devuelve la tabla deGovInfo; la apertura directa devolvió página de error en esta sesión. Conservar esa limitación, no afirmar descarga del PDF. |
| VEN | Márquez Bustillos como presidente formal; Gómez como poder de facto | [FRUS, despacho de1921](https://history.state.gov/historicaldocuments/frus1921v02/d896). Son funciones distintas: no dos presidentes formales simultáneos. |
| DOM | Gobierno militar estadounidense; Vicini; Peynado; Troncoso | [Departamento de Estado, ocupación1916–1924](https://2001-2009.state.gov/r/pa/ho/time/wwi/108649.htm); [FRUS, Peynado1939](https://history.state.gov/historicaldocuments/frus1939v02/d50); [AGN, sucesión dePeynado](https://colecciones.agn.gob.do/opac/ficha.php?informatico=00103214). Vicini fue investido21/10/1922; no confundirlo con su selección del2/10 ni con el final de la ocupación en1924. |
| ECU | Tamayo; segundo encargo deBaquerizo; Martínez Mera; Montalvo; primer Velasco; Enríquez; Borrero; Mosquera; segundo Velasco; Mancheno; Suárez; Arosemena Tola | [Ministerio de Educación, tabla presidencial,p119](https://educacion.gob.ec/wp-content/uploads/downloads/2014/06/TEXTO-DE-ESTUDIANTE-SOCIALES-7mo-EGB.pdf); [Planificación, tabla institucional](https://www.planificacion.gob.ec/wp-content/uploads/downloads/2014/06/Los-Constructores-del-Estado-Nacional.pdf). Se distinguen encargos, jefatura suprema, presidencias y ruptura constitucional de1946. |
| URY | Serrato; Campisteguy; Terra | [Archivo de Presidencia](https://archivo.presidencia.gub.uy/_web/noticias/2010/02/2010022810.htm). Hasta1933 el presidente compartía el Ejecutivo con el Consejo Nacional de Administración; no se le presenta como único titular. Terra se distingue por el cambio autoritario de1933. |
| CUB | Mendieta; Barnet; Laredo Brú | [LibraryofCongress, cronología](https://tile.loc.gov/storage-services/master/frd/frdcstdy/cu/cubacountrystudy00huds/cubacountrystudy00huds.pdf); [prensa contemporánea de18/1/1934](https://newspapers.swco.ttu.edu/server/api/core/bitstreams/7137d741-c38b-4f07-aaa7-b7a783ec48f4/content). Laredo Brú es presidente formal; el mando militar deBatista no lo sustituye. Barnet continúa después del límite documental1935. |
| COL | Primer mandato deLópez Pumarejo | [Banco de la República](https://enciclopedia.banrepcultural.org/Alfonso_L%C3%B3pez_Pumarejo). Ventana interior1935–1937, sin fusionarla con el segundo mandato. |
| CRI | Calderón Guardia | [Presidencia,1940–1944](https://www.presidencia.go.cr/node/142). [Asamblea, suplencia deCalderón Muñoz](https://www.asamblea.go.cr/ca/Lists/coleccion/DispForm.aspx?ContentTypeId=0x0100C97DC289459B304BA629D4F4451428AD&ID=474): no son la misma persona; la suplencia25/1–4/2/1943 queda señalada para posterior incorporación individual. |
| SLV | Castaneda Castro; Consejo de Gobierno Revolucionario | [Ministerio de Educación](https://www.mined.gob.sv/descarga/cipotes/historia_ESA_TomoII_0_.pdf); [Corte Suprema, comienzo delConsejo14/12/1948](https://www.csj.gob.sv/seccion-de-probidad-generalidades/). El Consejo es un órgano colegiado militar y civil y no recibe retrato individual. |

Las fuentes incluyen documentos contemporáneos y síntesis institucionales; estas últimas no se presentan como actos jurídicos originales. Los QID se consultaron mediante `wbsearchentities` y se contrastaron con etiquetas/descripciones de `wbgetentities`; las respuestas se conservaron en `.cache/identities/americas-1920-qid-search*.json` y `americas-1920-qids.json`. Los identificadores no acreditan por sí solos las fechas de ejercicio. Los órganos colectivos usan identificadores documentales explícitos, sin QID ni persona inventados.

## Límites y ejecución

Las ventanas de precisión9 llevan indicadores de frontera documental y una nota que descarta investiduras/ceses en enero o diciembre por el mero límite de revisión. Para los relevos diarios acreditados, el final inclusivo se calcula como día anterior a la sucesión. Troncoso usa resolución anual y conserva el relevo diario como pendiente. Se señalan sin completar los designados panameños de junio1923, los encargos ecuatorianos breves de1932 y suplencias costarricenses, entre otros huecos. No se certifica que la ausencia de nombres adicionales signifique ausencia de interinos.

`curate(data)` devuelve una copia y captura retratos antes de retirar únicamente su etiqueta propia. Sólo reemplaza intervalos coincidentes de la misma persona u órgano; conserva otras autoridades, banderas, créditos, fotografías y los periodos posteriores. No consulta red ni descarga imágenes.

La CLI exige destinos explícitos:

```text
python -X utf8 scripts/curate-1920-americas.py --input ruta/identities.json --output ruta/revisada.json
```

Verificado en memoria:35 registros, nueve claves,61 huecos nominales resueltos, segunda ejecución idéntica, entrada sin mutar, banderas/retratos conservados y registros1950+ idénticos. **No ejecutado sobre datos públicos en esta subentrega.** El responsable debe aplicar el preparador después de la adquisición genérica y registrar la auditoría final; los huecos de imágenes, suplencias y fechas diarias permanecen abiertos.


## Integración en0.11.0

Aplicado al catálogo público local por el responsable de integración el24/10/2026, después de comprobar la repetibilidad y conservar los retratos. El estado «no aplicado» de la preparación aislada describe el relevo inicial, no la entrega final. Resultados efectivos, adquisición de medios y límites conjuntos en [DELIVERY-0.11.0](DELIVERY-0.11.0.md) y [REVIEW-1920-1949.json](REVIEW-1920-1949.json). Publicación pendiente del aviso del propietario.
