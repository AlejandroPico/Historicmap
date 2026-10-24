# Símbolos adicionales1920–1949

Revisión acotada24/10/2026. `scripts/curate-1920-symbols-extra.py` propone **18 ventanas en10 claves**. Consulta real de Commons:18/18 imágenes y licencias admitidas, sin marcas de diseño ficticio o reconstrucción discutida. La comprobación no certifica todas las fechas legales ni cada variante material.

| Clave | Familia y cobertura | Fuentes y límites |
|---|---|---|
| MEX |1916–1934 para1920–1933;1934–1968 para1934–1949 | [Archivo General de la Nación](https://www.archivos.gob.mx/transparencia/pdf/SimbolosPatrios.pdf) identifica el periodo1916–1934; [historia normativa institucional](https://www.bienestar.gob.mx/work/models/SEDESOL/Transparencia/PCEPCI/Equidad_de_genero/documentosPdf/Ley_Escudo_bandera_Himno_Nacionales.pdf) distingue la autenticación del modelo en1934. No usar escudo de1968 en1920. |
| HND | Variante de estrellas doradas1920–1948; estrellas azules al cierre1949 | [Diario Nacional hondureño](https://dnh.gob.hn/diario/de-franjas-azules-y-blancas-a-cinco-estrellas-asi-nacio-la-bandera-de-honduras) describe1898–1949. Es una **variante histórica de uso**, no afirmación de exclusividad legal: las normas anteriores hablaban de estrellas azules. El [Tribunal Superior de Cuentas](https://www.tsc.gob.hn/wp-content/uploads/Boletin_Septiembre_20242.pdf) reproduce la reforma de1949 y la falta previa de uniformidad; no se atribuyen tonos digitales uniformes a todo el periodo. |
| NIC | Diseño1908–1971 para1920–1949 | [Ministerio de Educación](https://www.mined.gob.ni/fiestas-patrias/2024/07/29/el-significado-del-escudo-nacional/): origen1908 y especificaciones detalladas1971 son hechos distintos. |
| VEN | Siete estrellas en círculo1920–1929; en arco1930–1949 | Descripciones reales deCommons para las familias1905–1930 y1930–2006; [reproducción documental de la legislación histórica](https://hugochavez.ve/wp-content/uploads/2023/03/Un_Brazalete_Tricolor.pdf). Se identifica la variante nacional/civil sin escudo; no se aplican escudo de1954 ni ocho estrellas de2006. |
| ECU | Bandera estatal con escudo1920–1949 | [Presidencia](https://www.presidencia.gob.ec/presidencia-de-la-republica-conmemorara-el-dia-de-la-bandera-nacional/) distingue el tricolor de1860 y regulación de1900. La ilustración representa esa familia sin certificar normalización digital de cada detalle en1920. |
| ARG | Bandera mayor/oficial con sol1920–1949 | [Gobierno argentino](https://www.argentina.gob.ar/pais/simbolos/bandera): sol desde1818; ampliación del uso civil en1985 y parámetros técnicos de2010 no se retrotraen. |
| LUX | Tricolor histórico1920–1949 | [Folleto del Gobierno](https://sip.gouvernement.lu/dam-assets/publications/brochure-livre/minist-etat/sip/brochure/a-propos/A_propos_Symboles/A_propos_Symboles_de_l_Etat_et_de_la_nation.pdf): uso histórico y protección legal de1972 son distintos. No se afirma normalización Pantone en1920 ni libertad de exhibición durante la ocupación. |
| GRC | Cruz blanca sobre azul1920–1949 | [Presidencia griega](https://www.presidency.gr/en/presidency/the-flag/) distingue bandera terrestre de las enseñas navales y militares. La ficha usa la familia terrestre/civil, sin afirmar que sea estandarte real. |
| LTU | Tricolor interbélico1920–1939 | [Parlamento lituano](https://www.lrs.lt/pls/inter/w5_show?p_b=3804&p_d=49324&p_k=2&p_r=4056) acredita1918–1940. Se adquiere el SVG histórico separado; **1940–1949 queda fuera**, sin asignarlo a ocupantes ni sustituirlo por el archivo contemporáneo. |
| ALB | Seis ventanas:1926–1927,1928–1933,1934–1938,1939–1942,cierre1943,cierres1944–1945 | Familias explícitamente descritas por los archivos deCommons: república, monarquía, control italiano, control alemán y diseño comunista provisional. Son ventanas gráficas documentales; no se presentan como fechas normativas contrastadas de cada águila o corona. El título1934–1939 y su descripción1928–1939 no resuelven por sí solos una fecha legal de reforma. Se conserva el diseño con estrella de1946 del catálogo anterior. |

Se reutilizan `validate_page`, `acquire_reusing`, `subtract` y el adquiridor del curador principal. Conservan autores, licencias, atribuciones, bytes y SHA-256. No se dibujan escudos, banderas ni frentes. Los nuevos medios se adquieren antes de modificar identidades; una fuente rechazada detiene la aplicación.

```text
python -X utf8 scripts/curate-1920-symbols-extra.py --check-sources
python -X utf8 scripts/curate-1920-symbols-extra.py
```

La primera orden sólo escribe metadatos e informe en `.cache/identities/symbols-1920-extra-*`; la segunda aplica después de la curación principal1920. `curate(data, acquired)` permite revisar el resultado sin tocar archivos.

**Verificación aislada:**18 ventanas, repetición idéntica, entrada sin mutar, todas las autoridades conservadas y selección de símbolos1950–2026 sin cambios. En las diez claves, las ausencias al cierre anual bajan289→10; los diez restantes son Lituania1940–1949, fuera del ámbito. Ocho referencias pueden reutilizar SVG existentes; diez archivos son potencialmente nuevos. **No aplicado a `public/` en esta subentrega.** La auditoría efectiva de adquisición corresponde al responsable de integración y no equivale a estos resultados simulados.


## Integración en0.11.0

Aplicado al catálogo público local por el responsable de integración el24/10/2026, después de comprobar la repetibilidad y conservar los retratos. El estado «no aplicado» de la preparación aislada describe el relevo inicial, no la entrega final. Resultados efectivos, adquisición de medios y límites conjuntos en [DELIVERY-0.11.0](DELIVERY-0.11.0.md) y [REVIEW-1920-1949.json](REVIEW-1920-1949.json). Publicación pendiente del aviso del propietario.
