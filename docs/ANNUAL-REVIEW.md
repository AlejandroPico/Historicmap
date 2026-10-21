# Revisión anual 1900–2026

Generada con `npm run data:audit`. La tabla recorre **cada año**, comprueba la disponibilidad de registros vigentes y enumera cambios de registro. No significa que se hayan cotejado manualmente todas las fronteras del mundo con fuentes primarias. Los periodos sin cambios en una fuente pueden contener cambios que esa fuente omite.

## Método y fuentes

- [CShapes 2.0, ETH Zürich](https://icr.ethz.ch/data/cshapes/): se usa la edición GW **con dependencias** del paquete R, no el GeoJSON descargable que pierde estatus y administración. Cobertura de la entrega: 1900–2019. Base al 31 de diciembre. Los cambios de registro incluyen fronteras, capitales o estatus, no solamente cambios de superficie. La huella identifica el conjunto de registros seleccionado.
- [Código de CShapes](https://icr.ethz.ch/data/cshapes/CShapes-2.0_Codebook.pdf): excluye numerosas ocupaciones temporales y transferencias menores de 10.000 km². Algunas fechas y límites son aproximados. Su representación no se adopta como una declaración universal de soberanía reconocida.
- [Cliopatria, versión fijada en manifest.json](https://github.com/Seshat-Global-History-Databank/cliopatria): Alemania, Japón e Italia para 1938–1944. Síntesis anual de extensiones territoriales, **sin fecha diaria uniforme**; no se llama frente exacto de fin de año. [Contraste contextual de Europa en 1942, USHMM](https://encyclopedia.ushmm.org/content/en/map/german-administration-of-europe-1942).
- [Natural Earth](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/): base contemporánea de 258 entidades para 2020–año del dispositivo, importada en 2026. No inventa nuevos mapas al cambiar el reloj. El año máximo dinámico **no implica datos futuros verificados**.

## Correcciones contrastadas y límites concretos

1. **1942** deja de usar 1945: Alemania anterior a la derrota y extensión territorial anual; RDA y RFA sólo se denominan así desde 1949. Las zonas de ocupación de 1945 se identifican como tales. Falta delimitar por separado todas las administraciones de ocupación y los frentes diarios; no se ha añadido una geometría específica de la partición germano-soviética de Polonia en 1939.
2. **India**: dependencia británica antes de agosto de 1947 y Estado independiente al cierre de 1947. **Argelia**: administración francesa frente a independencia en 1962. Colores compartidos por potencia administradora, con territorio y estatus independientes en la ficha. Los Estados principescos y las subdivisiones coloniales requieren más detalle.
3. **Egipto/Israel/Siria**: se conserva como base la geometría de 1966 desde 1967 para no convertir ocupación del Sinaí y del Golán en incorporación soberana. Los polígonos de ocupación se derivan de diferencias entre geometrías fechadas. No resuelve por sí solo todas las líneas de armisticio ni disputas de reconocimiento. En 1979–1981 se indica retirada parcial, **sin dibujar fases inventadas**. Retirada principal del Sinaí en 1982; [Taba pendiente hasta 1989](https://content.ecf.org.il/files/M00972_IsraelEgyptTabaAgreement1989.pdf), sin polígono local en esta entrega. [Contexto de la guerra de 1967](https://history.state.gov/milestones/1961-1968/arab-israeli-war-1967).
4. **Crimea desde 2014**: capa territorial diferenciada, soberanía ucraniana conforme a [A/RES/68/262](https://press.un.org/en/2014/ga11493.doc.htm), ocupación/anexión reclamada por Rusia. El contorno se deriva de los registros anterior y posterior a marzo de 2014. No se presenta como anexión reconocida. **No hay geometrías verificadas de los frentes del Donbás ni de 2022–2026.**
5. **Capitales**: las de 1900–2019 proceden del registro temporal; las 323 ciudades contemporáneas no se trasladan a la India británica ni al mundo antiguo. Traslados recientes posteriores a las fuentes necesitan una actualización documentada.
6. **Economía**: seis indicadores WDI, observaciones desde 1960, datos locales con fecha. Sin extrapolación ni dato posterior al año consultado; máximo cinco años de retraso. Las estadísticas del Banco Mundial se refieren a sus economías publicadas, no a una integración espacial recalculada sobre fronteras históricas. No hay estadísticas de la URSS bajo el código de la Rusia actual.

## Inventario año por año

| Año | Territorios | Fuente / huella del estado | Cambios y estado de revisión |
| --- | ---: | --- | --- |
| 1900 | 152 | CShapes · 31 diciembre · 7825890386a7 | Estado inicial del inventario  |
| 1901 | 147 | CShapes · 31 diciembre · 23c424d05086 | Camerún alemán, Argelia, Australia  |
| 1902 | 147 | CShapes · 31 diciembre · b56ffdbcb095 | Cuba, Chile, Argentina, África Occidental Francesa, Cote D'Ivoire, Uganda, Kenya, Ethiopia, Swaziland (Eswatini), Marruecos, Argelia, Sudán  |
| 1903 | 149 | CShapes · 31 diciembre · 9d17fc603faf | Panama, Colombia, Brazil, Bolivia, Gabon, Polinesia Francesa, Northern Nigeria  |
| 1904 | 149 | CShapes · 31 diciembre · 324336e74ad0 | Mauritania, Marruecos, Thailand, Cambodia (Kampuchea), Northern Nigeria  |
| 1905 | 153 | CShapes · 31 diciembre · 8af5266a3a08 | Imperio ruso, Sweden, Norway, Mali, Niger, Angola, Papua, Northwestern Rhodesia, Southern Sakhalin Island  |
| 1906 | 153 | CShapes · 31 diciembre · 59d1b543932c | Gabon, Central African Republic, Congo, Southern Nigeria  |
| 1907 | 153 | CShapes · 31 diciembre · 720eb6a6db70 | Kenya, Ethiopia, Thailand, Cambodia (Kampuchea), New Zealand  |
| 1908 | 151 | CShapes · 31 diciembre · c593e1a23b8d | Austria-Hungría, Congo, Democratic Republic of (Zaire), Italian Somaliland  |
| 1909 | 151 | CShapes · 31 diciembre · a1b9b758105d | Peru, Brazil, Bolivia, Thailand, Federated Malay States, Unfederated Malay States  |
| 1910 | 148 | CShapes · 31 diciembre · 9012aab1e754 | Congo, Democratic Republic of (Zaire), Uganda, South Africa, Sudán, Korea, New Guinea (German New Guinea) (Kaiser Wilhelmsland)  |
| 1911 | 147 | CShapes · 31 diciembre · 765fff0f596e | Zambia  |
| 1912 | 149 | CShapes · 31 diciembre · 9ba25ea29926 | Mauritania, Camerún alemán, Gabon, Central African Republic, Chad, Congo, Madagascar (Malagasy), Marruecos, Spanish Morocco, Spanish West Africa, Libia, Imperio otomano  |
| 1913 | 151 | CShapes · 31 diciembre · 6f7e374f0298 | Albania, Serbia, Montenegro, Greece, Bulgaria, Rumanía, Mali, Mauritania, Imperio otomano, United Arab Emirates, China, Tibet  |
| 1914 | 151 | CShapes · 31 diciembre · 33f196ab6e9e | Albania, Cyprus, Imperio ruso, Togo alemán, Nigeria, Uganda, Kenya, Sudán, Imperio otomano, Egipto, China, Tibet, India, New Guinea (German New Guinea) (Kaiser Wilhelmsland)  |
| 1915 | 151 | CShapes · 31 diciembre · f1ccf8aeb6e4 | Haiti, Serbia, Montenegro, Namibia  |
| 1916 | 152 | CShapes · 31 diciembre · 4830a34b65b5 | Rumanía, Camerún alemán, Tanzania (Tanganyika), Qatar  |
| 1917 | 153 | CShapes · 31 diciembre · 5c26c89a3ec4 | Imperio ruso, Finland  |
| 1918 | 159 | CShapes · 31 diciembre · 807487eb19a4 | Polonia, Austria, Hungría, Checoslovaquia, Yugoslavia, Bulgaria, Rumanía, Rusia soviética, Estonia, Latvia, Lithuania, Iceland, Imperio otomano, Yemen (Arab Republic of Yemen)  |
| 1919 | 162 | CShapes · 31 diciembre · b03aee19183b | Francia, Alemania · República de Weimar, Polonia, Danzig, Austria, Hungría, Italia, Yugoslavia, Greece, Bulgaria, Rumanía, Mali, Burkina Faso (Upper Volta), Togo alemán, Cameroon, Camerún británico, Gabon, Central African Republic, Chad, Congo, Tanzania (Tanganyika), Argelia, Libia, Afghanistan  |
| 1920 | 166 | CShapes · 31 diciembre · 7c051f7b3fb5 | Alemania · República de Weimar, Polonia, Hungría, Albania, Yugoslavia, Rumanía, Rusia soviética, Lithuania, Denmark, Mauritania, Chad, Kenya, Tanzania (Tanganyika), Rwanda-Urundi, Namibia, Imperio otomano, Iraq, Siria, Lebanon, Jordan, Palestina, Papua, New Guinea (German New Guinea) (Kaiser Wilhelmsland)  |
| 1921 | 168 | CShapes · 31 diciembre · 140cf7753975 | Reino Unido, Irlanda, Polonia, Rusia soviética, China, Mongolia  |
| 1922 | 169 | CShapes · 31 diciembre · 95aaab70b2d9 | Colombia, Peru, Lithuania, Togo, Togo británico, Cameroon, Camerún británico, Tanzania (Tanganyika), Rwanda-Urundi, Iraq, Egipto, Siria  |
| 1923 | 169 | CShapes · 31 diciembre · ecb07ad3d16d | Turquía, Jordan, Palestina  |
| 1924 | 169 | CShapes · 31 diciembre · ce2bb2244eba | Kenya, Italian Somaliland  |
| 1925 | 169 | CShapes · 31 diciembre · 3a7d6d1be008 | Libia, Egipto, Jordan  |
| 1926 | 169 | CShapes · 31 diciembre · 026e2464d1b3 | Niger, Uganda, Kenya  |
| 1927 | 169 | CShapes · 31 diciembre · 85bde2fb2391 | Australia  |
| 1928 | 169 | CShapes · 31 diciembre · 85bde2fb2391 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1929 | 169 | CShapes · 31 diciembre · 85bde2fb2391 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1930 | 170 | CShapes · 31 diciembre · 0719c19e8e1a | Guayana Francesa, Inini  |
| 1931 | 170 | CShapes · 31 diciembre · e38468688671 | India  |
| 1932 | 170 | CShapes · 31 diciembre · 321a3868ce4b | Mali, Niger, Cote D'Ivoire, Iraq, Saudi Arabia  |
| 1933 | 170 | CShapes · 31 diciembre · e6a08c7a9a3f | Cote D'Ivoire  |
| 1934 | 170 | CShapes · 31 diciembre · 9b1d2eac809b | Haiti, Libia, Sudán, Yemen (Arab Republic of Yemen)  |
| 1935 | 170 | CShapes · 31 diciembre · 0931ae407318 | Saudi Arabia  |
| 1936 | 170 | CShapes · 31 diciembre · 0931ae407318 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1937 | 173 | CShapes · 31 diciembre · 39e670ba1f22 | Aden, India, Myanmar (Burma), East Aden Protectorate  |
| 1938 | 172 | CShapes · 31 diciembre · 4677aef0ce82 | Bolivia, Paraguay, Alemania nazi, Hungría, Checoslovaquia **+ capa anual de Alemania, Japón e Italia (Cliopatria; día no uniforme).** |
| 1939 | 172 | CShapes · 31 diciembre · ce6fa13f632a | Lithuania **+ capa anual de Alemania, Japón e Italia (Cliopatria; día no uniforme).** |
| 1940 | 169 | CShapes · 31 diciembre · 544e80f2abd0 | Bulgaria, Rumanía, Unión Soviética, Finland **+ capa anual de Alemania, Japón e Italia (Cliopatria; día no uniforme).** |
| 1941 | 169 | CShapes · 31 diciembre · d7c59d5d8b84 | Eritrea, Italian Somaliland **+ capa anual de Alemania, Japón e Italia (Cliopatria; día no uniforme).** |
| 1942 | 169 | CShapes · 31 diciembre · 551c2766f7e4 | Ecuador, Peru, Iceland, Guinea-Bissau **+ capa anual de Alemania, Japón e Italia (Cliopatria; día no uniforme).** |
| 1943 | 169 | CShapes · 31 diciembre · 74c669519f02 | Libia **+ capa anual de Alemania, Japón e Italia (Cliopatria; día no uniforme).** |
| 1944 | 169 | CShapes · 31 diciembre · 5d46c99a2cd6 | Iceland, Mali, Mauritania, Lebanon **+ capa anual de Alemania, Japón e Italia (Cliopatria; día no uniforme).** |
| 1945 | 169 | CShapes · 31 diciembre · d8cb7048c2bf | Alemania · zonas de ocupación occidentales, Alemania · zona de ocupación soviética, Polonia, Checoslovaquia, Unión Soviética, China, Korea, People's Republic of, Korea, Republic of, Indonesia  |
| 1946 | 168 | CShapes · 31 diciembre · 3fd42c0e9630 | Guayana Francesa, Madagascar (Malagasy), Comoros, Siria, Jordan, Malaysia, Sabah (North Borneo), Sarawak, Singapore, Philippines  |
| 1947 | 172 | CShapes · 31 diciembre · f90ad4b2e15e | Hungría, Checoslovaquia, Mali, Niger, Cote D'Ivoire, Burkina Faso (Upper Volta), China, India, Bhutan, Pakistan, Jammu and Kashmir, Kashmir (North, Azad)  |
| 1948 | 173 | CShapes · 31 diciembre · 1b4fbd687f73 | Canada, Israel, Korea, People's Republic of, Korea, Republic of, Myanmar (Burma), Sri Lanka (Ceylon), Philippines, Gaza, Cisjordania  |
| 1949 | 172 | CShapes · 31 diciembre · e15694f6524e | República Federal de Alemania, República Democrática Alemana, Libia, China, Taiwan, India, Bhutan, Pakistan, Indonesia, West Irian (Dutch New Guinea), Papua New Guinea  |
| 1950 | 171 | CShapes · 31 diciembre · ed922dcba9a5 | China, Italian Somaliland  |
| 1951 | 171 | CShapes · 31 diciembre · 4675dda5a373 | Libia  |
| 1952 | 170 | CShapes · 31 diciembre · 8e3d9cdfb020 | Ethiopia, Solomon Islands  |
| 1953 | 168 | CShapes · 31 diciembre · 18173b1bb7fd | Federation of Rhodesia and Nyasaland, Cambodia (Kampuchea)  |
| 1954 | 169 | CShapes · 31 diciembre · c49efea512c3 | Surinam, Laos, Vietnam, Democratic Republic of, Vietnam, Republic of  |
| 1955 | 169 | CShapes · 31 diciembre · c49efea512c3 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1956 | 168 | CShapes · 31 diciembre · 8a9ed174130c | Ghana, Marruecos, Túnez, Sudán, Southern zone of Spanish Morocco  |
| 1957 | 168 | CShapes · 31 diciembre · 2df5d34e26e4 | Ghana, Malaysia  |
| 1958 | 167 | CShapes · 31 diciembre · 36549e9e3e37 | Guinea, Marruecos, Spanish Sahara  |
| 1959 | 164 | CShapes · 31 diciembre · 581ef805a41a | Estados Unidos, Mali, Pakistan  |
| 1960 | 164 | CShapes · 31 diciembre · c83c334ecb87 | Brazil, Cyprus, Mali, Senegal, Benin, Mauritania, Niger, Cote D'Ivoire, Burkina Faso (Upper Volta), Togo, Cameroon, Nigeria, Gabon, Central African Republic, Chad, Congo, Congo, Democratic Republic of (Zaire), Somalia, Madagascar (Malagasy)  |
| 1961 | 164 | CShapes · 31 diciembre · 0970d2655721 | Sierra Leone, Cameroon, Nigeria, Tanzania (Tanganyika), Kuwait  |
| 1962 | 164 | CShapes · 31 diciembre · 94583503bedb | Jamaica, Trinidad and Tobago, Uganda, Burundi, Rwanda, Argelia, West Irian (Dutch New Guinea), Federation of South Arabia  |
| 1963 | 161 | CShapes · 31 diciembre · e052d07674fc | Kenya, Zanzibar, Malaysia, West Irian (Dutch New Guinea)  |
| 1964 | 162 | CShapes · 31 diciembre · 21a350ff825c | Malta, Tanzania (Tanganyika), Zambia, Zimbabwe (Rhodesia), Malawi  |
| 1965 | 163 | CShapes · 31 diciembre · 5f277d0f642a | Gambia, Zimbabwe (Rhodesia), Maldives, Malaysia, Singapore  |
| 1966 | 163 | CShapes · 31 diciembre · 97e3e84e3937 | Barbados, Guyana, Namibia, Lesotho, Botswana  |
| 1967 | 161 | CShapes · 31 diciembre · 0af743f35e48 | Egipto, Siria, Israel, Yemen, People's Republic of, Pakistan  |
| 1968 | 161 | CShapes · 31 diciembre · 9c1910b18a81 | Equatorial Guinea, Swaziland (Eswatini), Mauritius  |
| 1969 | 160 | CShapes · 31 diciembre · bb1b85034c15 | Indonesia  |
| 1970 | 160 | CShapes · 31 diciembre · cb639965a473 | Belize, Fiji  |
| 1971 | 162 | CShapes · 31 diciembre · 72d28c25617e | Bahrain, Qatar, United Arab Emirates, Pakistan, Bangladesh  |
| 1972 | 162 | CShapes · 31 diciembre · 72d28c25617e | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1973 | 162 | CShapes · 31 diciembre · e5e67795970b | Bahamas  |
| 1974 | 162 | CShapes · 31 diciembre · cca506d4fee3 | Guinea-Bissau  |
| 1975 | 160 | CShapes · 31 diciembre · 07b22e580ab5 | Surinam, Cape Verde, Mauritania, Angola, Mozambique, Comoros, Marruecos, Vietnam, Democratic Republic of, Papua New Guinea  |
| 1976 | 159 | CShapes · 31 diciembre · d1e7ab5e41ba | Philippines, Indonesia  |
| 1977 | 159 | CShapes · 31 diciembre · bef40e97779e | Djibouti  |
| 1978 | 159 | CShapes · 31 diciembre · f93354dd7cad | Solomon Islands  |
| 1979 | 159 | CShapes · 31 diciembre · fb0b7917e6c2 | Mauritania, Marruecos, Egipto, Israel  |
| 1980 | 159 | CShapes · 31 diciembre · fb0b7917e6c2 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1981 | 159 | CShapes · 31 diciembre · ba4e9025f64f | Belize  |
| 1982 | 159 | CShapes · 31 diciembre · ba4e9025f64f | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1983 | 159 | CShapes · 31 diciembre · 4f5c6949f1fe | Cote D'Ivoire  |
| 1984 | 159 | CShapes · 31 diciembre · ed087621924f | Brunei  |
| 1985 | 159 | CShapes · 31 diciembre · ed087621924f | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1986 | 159 | CShapes · 31 diciembre · ed087621924f | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1987 | 159 | CShapes · 31 diciembre · ed087621924f | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1988 | 159 | CShapes · 31 diciembre · ed087621924f | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1989 | 159 | CShapes · 31 diciembre · ed087621924f | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1990 | 157 | CShapes · 31 diciembre · f6728bc663de | Alemania, Namibia, Yemen (Arab Republic of Yemen), Oman  |
| 1991 | 172 | CShapes · 31 diciembre · 752e066ad74f | Macedonia (FYROM/North Macedonia), Yugoslavia, Moldova, Unión Soviética, Estonia, Latvia, Lithuania, Ucrania, Belarus (Byelorussia), Armenia, Georgia, Azerbaijan, Turkmenistan, Tajikistan, Kyrgyz Republic, Uzbekistan, Kazakhstan  |
| 1992 | 175 | CShapes · 31 diciembre · 04bf2143e724 | Croatia, Yugoslavia, Bosnia-Herzegovina, Slovenia  |
| 1993 | 177 | CShapes · 31 diciembre · 6a830df3338c | Czech Republic, Slovakia, Ethiopia, Eritrea  |
| 1994 | 177 | CShapes · 31 diciembre · 6a830df3338c | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1995 | 177 | CShapes · 31 diciembre · 6a830df3338c | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1996 | 177 | CShapes · 31 diciembre · 6a830df3338c | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1997 | 177 | CShapes · 31 diciembre · 1e43630e88f5 | Kazakhstan  |
| 1998 | 177 | CShapes · 31 diciembre · 1e43630e88f5 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 1999 | 177 | CShapes · 31 diciembre · 1e43630e88f5 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2000 | 177 | CShapes · 31 diciembre · 15ce18a5c06a | Saudi Arabia, Yemen (Arab Republic of Yemen)  |
| 2001 | 177 | CShapes · 31 diciembre · 15ce18a5c06a | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2002 | 178 | CShapes · 31 diciembre · 4ee0a51d4a7e | Indonesia, East Timor  |
| 2003 | 178 | CShapes · 31 diciembre · 4ee0a51d4a7e | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2004 | 178 | CShapes · 31 diciembre · 4ee0a51d4a7e | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2005 | 178 | CShapes · 31 diciembre · 8250a0df5012 | Myanmar (Burma)  |
| 2006 | 179 | CShapes · 31 diciembre · dcfd19d96cc8 | Serbia, Montenegro  |
| 2007 | 179 | CShapes · 31 diciembre · dcfd19d96cc8 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2008 | 180 | CShapes · 31 diciembre · ca4452ab2a99 | Serbia, Kosovo  |
| 2009 | 180 | CShapes · 31 diciembre · ca4452ab2a99 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2010 | 180 | CShapes · 31 diciembre · ca4452ab2a99 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2011 | 181 | CShapes · 31 diciembre · 581d8ee2be9f | Sudán, Sudán del Sur  |
| 2012 | 181 | CShapes · 31 diciembre · 581d8ee2be9f | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2013 | 181 | CShapes · 31 diciembre · 581d8ee2be9f | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2014 | 181 | CShapes · 31 diciembre · 76151eefa6e4 | Rusia, Ucrania  |
| 2015 | 181 | CShapes · 31 diciembre · 76151eefa6e4 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2016 | 181 | CShapes · 31 diciembre · 76151eefa6e4 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2017 | 181 | CShapes · 31 diciembre · 76151eefa6e4 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2018 | 181 | CShapes · 31 diciembre · 76151eefa6e4 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2019 | 181 | CShapes · 31 diciembre · 76151eefa6e4 | Sin cambio de registro de fronteras, estatus o capital en la fuente  |
| 2020 | 258 | Natural Earth, referencia contemporánea incorporada en 2026 | Base contemporánea; sin auditoría independiente de todos los cambios de control de este año. |
| 2021 | 258 | Natural Earth, referencia contemporánea incorporada en 2026 | Base contemporánea; sin auditoría independiente de todos los cambios de control de este año. |
| 2022 | 258 | Natural Earth, referencia contemporánea incorporada en 2026 | Base contemporánea; sin auditoría independiente de todos los cambios de control de este año. |
| 2023 | 258 | Natural Earth, referencia contemporánea incorporada en 2026 | Base contemporánea; sin auditoría independiente de todos los cambios de control de este año. |
| 2024 | 258 | Natural Earth, referencia contemporánea incorporada en 2026 | Base contemporánea; sin auditoría independiente de todos los cambios de control de este año. |
| 2025 | 258 | Natural Earth, referencia contemporánea incorporada en 2026 | Base contemporánea; sin auditoría independiente de todos los cambios de control de este año. |
| 2026 | 258 | Natural Earth, referencia contemporánea incorporada en 2026 | Base contemporánea; sin auditoría independiente de todos los cambios de control de este año. |

## Pendientes para una revisión historiográfica completa

Frentes y administración de ocupaciones de ambas guerras mundiales, Estados y dependencias menores omitidos por el proveedor, mandatos y armisticios del Levante con mayor detalle, retirada del Sinaí por fases y Taba, descolonización subnacional, conflictos y control efectivo desde 2020, y costa contemporánea de resolución superior. La auditoría automatizada de todos los años y los contrastes focales son una mejora sustancial, **no una certificación de exactitud exhaustiva de 127 mapas**.
