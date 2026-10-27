# Historicmap

**El tiempo tiene un lugar.** Atlas interactivo de la evolución de la Tierra y de las sociedades humanas, con mapa 2D, globo 3D y navegación temporal.

Versión actual: **0.26.0** · 27 de octubre de 2026. Autor del proyecto: Alejandro Pico.

Catálogo organizado: **[Países y entidades históricas](Países/INDICE.md)**, con carpetas, resúmenes, banderas, mandatos y referencias a sus archivos. [Cómo añadir documentos o audio por entidad y fecha](Países/README.md).

**[Abrir el atlas publicado](https://alejandropico.github.io/Historicmap/)**

Ampliación vigente: **1000–1099**, con autoridades, retratos, símbolos, instituciones y contexto fechados. Fuentes, alcance y huecos concretos en [investigación de 1000](docs/RESEARCH-1000.md) y [auditoría anual](docs/REVIEW-1000-1099.json); continuidad en [tareas.md](tareas.md).

## Empezar

Usar **Node.js 26.12.1 o posterior**; la versión de referencia está en `.nvmrc`.

```sh
npm ci
npm run dev
```

Abrir la dirección local que indique Vite. Para generar la aplicación estática: `npm run build`. El resultado se guarda en `dist/`; `npm run preview` permite revisarlo. Las rutas relativas permiten alojarla bajo `/Historicmap/`.

Créditos cartográficos integrados en **Datos y fuentes → Créditos del mapa**, plegados inicialmente. La escala geográfica permanece abajo a la izquierda.

## Funciones

- Mapa vectorial 2D y globo 3D con zoom, selección y búsqueda local en panel compacto sin oscurecer el mapa.
- Regla temporal arrastrable con indicador, fecha y reproducción centrados. La rueda sobre la regla cambia la escala sin desplazar la fecha; sobre el mapa hace zoom geográfico. Las teclas más/menos ajustan la escala y las flechas recorren el tiempo.
- Mapa a pantalla completa con ocho herramientas en la esquina superior derecha, sin cabecera ni franjas de controles alrededor de la regla. Filtros y Capas en paneles separados.
- Navegación entre 4.540 Ma y el año del dispositivo, con escala adaptativa no uniforme y años introducidos por el usuario.
- Cronología anual desde 1000: Cliopatria hasta 1885 y CShapes 1886–2019, con dependencias coloniales y capitales históricas cuando están documentadas. Reproducción reciente anual que espera la carga y conserva el mapa anterior mientras llega el siguiente.
- Control territorial opaco por potencia; colores específicos de regímenes, clientes y bandos. Primera y Segunda Guerra Mundial, Guerra Civil española 1936–1939 y control comunista chino, además de Sinaí, Golán y Crimea. Fuentes anuales y frente de octubre de 1937 identificados con su precisión.
- [Corrección deEuropaCentral1938–1939](docs/CENTRAL-EUROPE-1939.md): sin manchas alemanas remotas, territorio integrado y Estado eslovaco cliente separado. El contorno eslovaco es una referencia recortada, no un levantamiento exacto de1939.
- Banderas históricas, autoridades y retratos en las fichas. Catálogo ampliado de mandatos desde1880, con Estados predecesores, administraciones coloniales y cobertura mundial desigual; cada imagen conserva su licencia y autoría. [Alcance y fuentes1900–1919](docs/RESEARCH-1900.md) y [auditoría nominal de carencias](docs/REVIEW-1900-1919.json).
- Base contemporánea desde 2020 y 26 instantáneas originales conservadas para historia anterior/geología y trazabilidad.
- Desde1900, contornos de referencia identificados para pequeños Estados omitidos por CShapes —el Vaticano sólo desde1929—, Tonga protegido antes de1970 y Sáhara separado de Marruecos; Crimea permanece en la base ucraniana y Kuwait ocupado en1990 se distingue de su soberanía. Danzig conserva su contorno de fuente en1938, corrigiendo un final de vigencia un año anticipado.
- Fichas persistentes a la izquierda: Autoridades, Territorio, Instituciones, Sociedad, Economía, Relaciones, Defensa, Historia, Datos, Contexto, Conflictos y Comparar. Al cambiar de año conservan entidad, apartado y lectura; si la entidad desaparece, se explica sin sustituirla por un sucesor. Fuentes, capas y búsqueda también se conservan al navegar por fechas.
- Cronología del país con filtros, fuentes y fechas navegables; registros posteriores al año consultado sólo con activación explícita. Relaciones dirigidas entre entidades históricas, con fecha del hecho separada del año de navegación.
- Comparación entre dos fechas, con autoridades, símbolos y observaciones; botones para alternar los mapas. Comparación de hasta cuatro entidades fijadas en el año del mapa, tabla desplazable y gráficos de evolución accesibles.
- Apariencia mañana/tarde/noche/automático según hora local, con preferencia conservada; tarde en tonos cobre y ámbar.
- 41 organizaciones y agrupaciones con altas, bajas y categorías fechadas desde1880: Triple Alianza, coaliciones de la Primera Guerra Mundial, Sociedad de Naciones, ONU, OTAN, CE/UE, BRICS, Tres Mares, Mercosur, CARICOM, OUA/UA, ASEAN y otras. Contextos y conflictos parciales por fases históricas.
- Fichas con capital, situación política, administración y 28 indicadores WDI en el catálogo: seis originales y 22 adicionales, con cobertura desigual. Economía, sociedad y personal militar; observaciones, unidades y fuentes visibles, gráficos sin interpolar huecos y sin usar valores futuros. Colores temáticos de PIB total, PIB por habitante y población.
- Relieve contemporáneo de referencia apagado al abrir y disponible desde 10.000 a. C., 323 capitales/grandes ciudades actuales y capitales históricas por periodo, enlaces compartibles y diseño adaptable.
- Ventana «Acerca de» con favicon, identidad, versión e historial, portfolio del autor y repositorio.

**La revisión anual no es una certificación exhaustiva de todas las fronteras.** [El informe 1789–año actual](docs/ANNUAL-REVIEW.md) registra cada selección, cambios y límites. CShapes termina en 2019, omite ocupaciones temporales y cambios pequeños. Desde 2020 se utiliza una referencia contemporánea incorporada en 2026, no una reconstrucción independiente de cada año. Faltan los frentes actuales, fases del Sinaí y otros detalles. La costa Natural Earth 1:10m todavía no alcanza el objetivo final de máxima definición. No se interpolan fronteras ni se inventan cambios futuros al avanzar el reloj.

Para etapas anteriores a 1.800 Ma, y para la prehistoria entre 1 Ma y 10.000 a. C., no se inventan mapas. La aplicación indica la ausencia de datos e incluye contexto. El efecto de la Tierra primitiva es conceptual, no una simulación física. Homininos, migraciones, glaciaciones, atmósfera, biomas, impactos y la cobertura mundial completa de conflictos requieren nuevas capas documentadas.

## Calidad y publicación

```sh
npm run data:verify
npm run data:audit
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

GitHub Actions valida datos, pruebas temporales/históricas/estadísticas, compilación y recorridos de navegador: años 1789–actualidad, reproducción y pausa, peticiones lentas, fichas, ciudades, economía, cartografía anterior/geológica, zoom y móvil. `Publish atlas` publica únicamente después de `Quality` correcto en `main`. No contiene secretos ni necesita un servidor propio. Las versiones exactas de dependencias figuran en `package-lock.json`.

## Datos y continuidad

Consultar **[agentes.md](agentes.md)** antes de modificar el proyecto. Contiene la visión completa, decisiones, arquitectura, roadmap, reglas de colaboración y estado real. [AGENTS.md](AGENTS.md) es el punto de entrada para asistentes que detectan ese nombre automáticamente.

Las fuentes, licencias, atribuciones y límites se documentan en [docs/SOURCES.md](docs/SOURCES.md). `public/data/manifest.json` registra65 recursos locales, versiones, URLs, transformaciones y SHA-256. `npm run data:fetch` actualiza explícitamente las 26 instantáneas originales, conservando las nuevas capas. La adquisición y reconstrucción de las capas recientes se explica en SOURCES. No se descargan datos nuevos durante la compilación ni desde las fichas.

La cartografía funciona sin API key. Las geometrías, perfiles, series y letras del mapa utilizadas son locales. El relieve (AWS) y las fuentes tipográficas de interfaz (Google Fonts) requieren conexión. La aplicación no envía búsquedas a servicios externos ni incorpora analítica. No está implementada como aplicación instalable o completamente offline.

El código original no tiene todavía una licencia de distribución elegida por el titular. Los datos de terceros conservan sus propias licencias; ver [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Cobertura del año vigente y medios: [CURRENT-AUTHORITIES](docs/CURRENT-AUTHORITIES.md). Agrupaciones, conflictos y fuentes: [CURRENT-LAYERS](docs/CURRENT-LAYERS.md).

La ampliación de fichas se describe en [COUNTRY-WORKSPACE](docs/COUNTRY-WORKSPACE.md); datos y licencias en [COUNTRY-INDICATORS](docs/COUNTRY-INDICATORS.md) y [COUNTRY-HISTORY](docs/COUNTRY-HISTORY.md). Los apartados son utilizables para ampliar registros por años; su existencia no acredita que se hayan adquirido todas las constituciones, idiomas, religiones, sanciones, bases militares o lugares patrimoniales del mundo.


Actualización0.14.0: correcciones de selección histórica, retratos por etapas y referencias delPacífico; incorporación documental parcial hasta1860. El frente deUcrania conserva fechas de observación explícitas. Véase [alcance y pendientes](docs/DELIVERY-0.14.0.md).


Actualización0.15.0: documentación ampliada hasta1840, recuperación de oficios monárquicos, regencias y transiciones, símbolos y retratos deVictoria por etapas. [Fuentes y carencias nominales](docs/RESEARCH-1840.md).

Actualización0.16.0: ampliación documental1820–1839. [Alcance, fuentes y pendientes](docs/DELIVERY-0.16.0.md).

Actualización0.17.0: ampliación documental1800–1819. [Alcance, fuentes y pendientes](docs/DELIVERY-0.17.0.md).

Actualización0.18.0: revisión de símbolos y soberanos, clasificación política fechada y filtros, ciudades históricas y episodios de conflictos. [Alcance y carencias](docs/REVIEW-0.18.md).

Actualización0.19.0: navegación anual hasta1700, símbolos y soberanos fechados, sedes de Estados germanos agrupados y nuevo panel deFiltros con opciones vacías ocultas. [Fuentes, cobertura y carencias](docs/RESEARCH-1700.md).

Actualización 0.22.0: navegación anual hasta 1400, autoridades y símbolos fechados, poderes bizantinos, sucesiones inglesas, interregno otomano y coronas separadas. [Fuentes y pendientes](docs/RESEARCH-1400.md).

Actualización 0.23.0: navegación anual hasta 1300, autoridades y símbolos fechados, sucesiones Yuan/Ming y Goryeo/Joseon, poderes mongoles y cortes japonesas. Sedes seleccionables donde faltan contornos propios y desfases de fuente identificados sin inventar fronteras. [Fuentes y pendientes](docs/RESEARCH-1300.md).

Actualización 0.24.0: navegación anual hasta 1200, poderes bizantinos y mongoles diferenciados, coronas y sucesiones revisadas. Aro de carga integrado en el botón de reproducción, también al saltar manualmente de año; la ficha conserva su contenido durante la espera. [Fuentes, alcance y pendientes](docs/RESEARCH-1200.md).
