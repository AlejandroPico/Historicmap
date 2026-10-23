# Indicadores adicionales de las fichas de país

Adquisición explícita del **23 de octubre de 2026**, con referencia máxima **2026-10-23**, a partir de **World Development Indicators (WDI), fuente 2 del Banco Mundial**. El archivo `public/data/country-indicators.json` amplía las seis series de `profiles.json`; no las reemplaza. Ninguna visita al atlas consulta la API.

Resultado incorporado: **22 indicadores, 217 claves de países/economías y 175.996 observaciones**, entre 1960 y 2025; archivo de **3.567.821 bytes**. La consulta permite 2026, pero la fuente no devolvió observaciones válidas de ese año. No confundir 217 claves con 217 Estados soberanos ni con cobertura completa en todas las métricas.

## Contrato y uso temporal

El documento contiene `retrieved`, `referenceDate`, `source`, `license`, `licenseUrl`, `range`, `indicators`, `sources`, `excludedObservations` y `countries`. Cada país/economía conserva una clave WDI que ya existe en `profiles.countries`; se resuelven los alias cartográficos con el índice existente `profiles.codes`. No se importan agregados regionales, grupos de renta ni el total mundial. Una economía estadística no equivale necesariamente a un Estado soberano.

Cada indicador incluye nombre español, unidad, sección, código WDI, descripción y alcance, proveedor original, enlace de fuente, metadatos, licencia, actualización WDI, fecha de descarga y primera/última observación realmente disponible. Cada serie es una lista descendente de pares `[año, valor]`, sin valores nulos ni años repetidos. No se imputan datos, no se interpolan huecos, no se convierten ausencias en cero ni se proyectan series de un Estado sucesor sobre otro anterior.

La selección de un año debe usar únicamente observaciones de ese año o anteriores, con fecha visible y el límite de antigüedad que determine la interfaz. Los gráficos pueden conservar observaciones anteriores más antiguas siempre que muestren sus años. Nunca usar una observación posterior a la fecha consultada para rellenar un hueco. Los valores de 1960–2026 proceden de la versión descargada hoy: no reconstruyen la información que estaba publicada en cada uno de esos años ni garantizan que cada país tenga datos desde 1960. Las revisiones estadísticas retrospectivas son posibles.

Las observaciones que la API etiqueta como previsión (`obs_status: F`) se excluyen. Estimaciones modelizadas de población, empleo, mortalidad y otros indicadores pueden conservarse como tales; «no previsión» no equivale a «censo o medición directa».

## Catálogo incorporado

| Clave | Indicador WDI | Apartado | Unidad y alcance |
|---|---|---|---|
| gdpGrowth | NY.GDP.MKTP.KD.ZG | Economía | Crecimiento real anual del PIB, % |
| inflation | FP.CPI.TOTL.ZG | Economía | Inflación anual de precios de consumo, % |
| unemployment | SL.UEM.TOTL.ZS | Economía | Desempleo sobre población activa, estimación OIT, % |
| exports | NE.EXP.GNFS.ZS | Economía | Exportaciones de bienes y servicios, % del PIB |
| imports | NE.IMP.GNFS.ZS | Economía | Importaciones de bienes y servicios, % del PIB |
| agriculture | NV.AGR.TOTL.ZS | Economía | Valor añadido de agricultura, silvicultura y pesca, % del PIB |
| industry | NV.IND.TOTL.ZS | Economía | Valor añadido industrial, incluida construcción, % del PIB |
| services | NV.SRV.TOTL.ZS | Economía | Valor añadido de servicios, % del PIB |
| centralGovernmentDebt | GC.DOD.TOTL.GD.ZS | Economía | Deuda del gobierno central, % del PIB; **no deuda pública total** |
| currentAccount | BN.CAB.XOKA.GD.ZS | Economía | Saldo por cuenta corriente, % del PIB |
| investment | NE.GDI.TOTL.ZS | Economía | Formación bruta de capital, % del PIB |
| density | EN.POP.DNST | Sociedad | Habitantes por km² de superficie terrestre |
| literacy | SE.ADT.LITR.ZS | Sociedad | Alfabetización de población de 15 años o más, % |
| secondaryEnrollment | SE.SEC.ENRR | Sociedad | Matriculación secundaria **bruta**, %; puede superar 100 |
| internet | IT.NET.USER.ZS | Sociedad | Personas que usan Internet, % |
| fertility | SP.DYN.TFRT.IN | Sociedad | Fecundidad total, hijos por mujer |
| netMigration | SM.POP.NETM | Sociedad | Migración neta del periodo anual publicado, personas |
| under5Mortality | SH.DYN.MORT | Sociedad | Mortalidad antes de cinco años por 1.000 nacidos vivos |
| electricity | EG.ELC.ACCS.ZS | Sociedad | Acceso a electricidad, % de la población |
| gini | SI.POV.GINI | Sociedad | Índice de desigualdad 0–100; renta o consumo según encuesta |
| armedForces | MS.MIL.TOTL.P1 | Defensa | Personal militar activo conforme a definición IISS, personas |
| armedForcesLabor | MS.MIL.TOTL.TF.ZS | Defensa | Personal militar sobre población activa, % |

`allowNegative` es verdadero en crecimiento, inflación, saldo corriente, formación bruta de capital y migración neta. Se conservan contracciones, deflación, déficit, desinversión y emigración neta. La [definición oficial de formación bruta de capital](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/NE.GDI.TOTL.ZS) incluye adquisiciones menos disposiciones y variaciones de existencias: no debe descartarse automáticamente un resultado negativo. Las magnitudes con signo no se someten a escalas que partan siempre de cero. Exportaciones/importaciones y matriculación bruta pueden superar el 100 %: no se recortan. Los valores negativos inesperados de otras magnitudes se conservan identificados en `excludedObservations`, fuera de las series utilizables, pendientes de contraste.

## Licencias y atribución

**Atribución:** World Bank, World Development Indicators, y proveedores originales por indicador (OIT, UNESCO UIS, UIT, División de Población de Naciones Unidas, UNICEF/UN IGME, FMI, IISS y otros indicados en `provider`). Descarga y transformación: Historicmap. Se conservaron valores y años; se seleccionaron economías del atlas, se omitieron nulos/previsiones y se ordenaron series. Las etiquetas y explicaciones españolas son adaptación editorial.

El script comprueba en la página oficial de **cada indicador** una declaración explícita **CC BY-4.0** antes de redistribuirlo. Se aplican además los [términos adicionales del Banco Mundial para conjuntos de datos](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets). Consultar el [texto de CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). La procedencia y las páginas de verificación se guardan en `sources`; sus respuestas completas permanecen en la caché local ignorada.

No se descarga ni redistribuye la serie de gasto militar SIPRI: su [página oficial WDI](https://data.worldbank.org/indicator/MS.MIL.XPND.GD.ZS) indica **SIPRI terms and conditions**, una excepción al régimen general. No asumir que toda serie accesible mediante la API tiene licencia CC BY. Las dos series de personal militar sí muestran [CC BY-4.0 en WDI](https://data.worldbank.org/indicator/MS.MIL.TOTL.P1), pero terminan antes de la actualidad: no constituyen un índice de poder militar ni una estimación del ejército vigente en 2026.

## Cobertura de la descarga

| Indicador | Economías con datos | Observaciones | Primer–último año |
|---|---:|---:|---|
| Crecimiento real del PIB | 214 | 11.408 | 1961–2025 |
| Inflación | 193 | 9.151 | 1960–2025 |
| Desempleo OIT | 187 | 6.531 | 1991–2025 |
| Exportaciones | 194 | 9.029 | 1960–2025 |
| Importaciones | 194 | 9.038 | 1960–2025 |
| Agricultura | 206 | 9.088 | 1960–2025 |
| Industria | 208 | 9.055 | 1960–2025 |
| Servicios | 205 | 8.629 | 1960–2025 |
| Deuda del gobierno central | 109 | 1.648 | 1970–2024 |
| Saldo corriente | 200 | 7.773 | 1960–2025 |
| Formación bruta de capital | 187 | 8.670 | 1960–2025 |
| Densidad de población | 216 | 12.534 | 1961–2024 |
| Alfabetización adulta | 170 | 1.121 | 1970–2024 |
| Matriculación secundaria | 208 | 6.280 | 1970–2025 |
| Uso de Internet | 213 | 6.224 | 1990–2025 |
| Fecundidad | 217 | 14.073 | 1960–2024 |
| Migración neta | 217 | 14.322 | 1960–2025 |
| Mortalidad menores de cinco años | 196 | 11.861 | 1960–2024 |
| Acceso a electricidad | 216 | 6.747 | 1990–2024 |
| Gini | 171 | 2.434 | 1963–2025 |
| Personal militar | 174 | 5.355 | 1985–2020 |
| Personal militar / población activa | 172 | 5.025 | 1990–2020 |

Son extremos globales por indicador; no implican continuidad por país. No se encontraron observaciones marcadas `F` en las respuestas utilizadas. Se retuvieron **15.965 valores negativos** admisibles en sus magnitudes y **1.951 porcentajes superiores a 100**, sin recortarlos.

Se apartó una observación para contraste: **deuda central de Namibia, 2012, −1,17072566818484 % del PIB**, publicada así por WDI. Se conserva código, valor y motivo en `excludedObservations`; no se corrige ni se reemplaza con otra magnitud. Esto no declara definitivamente errónea la fuente: deja explícita la excepción pendiente de revisión contable/estadística.

## Reproducción y validación

Ejecutar `node scripts/enrich-country-indicators.mjs`. Por defecto reutiliza respuestas locales cuya URL coincida; `--refresh` obliga a consultar de nuevo las fuentes. `ATLAS_REFERENCE_DATE=AAAA-MM-DD` permite fijar una referencia explícita; la referencia predeterminada de esta entrega es 2026-10-23. Cambiarla no inventa datos del nuevo año. La salida se escribe sólo tras completar y validar todas las series; se sustituye al final mediante renombrado del archivo temporal.

Se validan paginación completa, metadatos de la fuente 2, licencia por indicador, país permitido, años enteros de 1960 a la referencia, números finitos, unicidad país/indicador/año y signos. Se excluyen agregados usando el catálogo oficial de países/economías (región `NA` identifica agregados en ese catálogo). El resumen local está en `.cache/country-indicators/audit.json` y no forma parte del producto. La verificación de manifiesto/SHA corresponde a la integración del archivo, no a este script de adquisición.

Validación posterior de esta entrega: recorridos de todas las 175.996 observaciones, ausencia de agregados y años futuros, orden descendente estricto y correspondencia con `profiles`; comprobados crecimiento negativo español de 2020, matriculación española superior a 100 %, formación de capital negativa de Irak en 1991 y última observación militar española en 2020. Segunda ejecución desde caché correcta. Comprobación de formato de diferencias correcta. Son verificaciones estructurales y focales, no una auditoría estadística nacional exhaustiva.

## Limitaciones

- La cobertura varía mucho por país, indicador y año. Alfabetización, Gini y deuda central suelen tener huecos; no deben mostrarse como una serie anual completa.
- Deuda central no incluye necesariamente gobiernos regionales/locales o todas las unidades de seguridad social; la fuente advierte de diferencias entre cuentas centrales consolidadas y presupuestarias.
- Encuestas de ingresos/consumo, metodologías nacionales y cambios estadísticos limitan las comparaciones directas del Gini y otras métricas.
- Las series militares IISS publicadas por WDI son antiguas; mostrar siempre fecha, y respetar el límite de antigüedad de la ficha.
- Densidad y estadísticas WDI no reconstruyen automáticamente fronteras antiguas. No usar los datos para afirmar cambios geométricos ni soberanía.
- No se incorporan todavía religiones, grupos lingüísticos, servicio militar, bases extranjeras, gasto militar redistribuible, producción por recurso ni socios comerciales bilaterales. Se requieren fuentes y licencias específicas.
