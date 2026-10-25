# Control territorial1940–1944: diagnóstico y referencias

Investigación acotada para la corrección0.12.1,24/10/2026. No modifica aplicación, conjuntos públicos ni manifiestos. El inventario reproducido en `.cache/wwii-control-audit.json` analiza los polígonos **originales** de `historical-control.geojson`, antes del renderizado y de las correcciones1938–1939. No equivale a una reconstrucción de frentes diarios.

## Diagnóstico geométrico

| Control original | Componentes | Cuadriláteros de cinco coordenadas | Componentes con muestra en regiones ajenas evidentes |
| --- | ---: | ---: | ---: |
| Alemania1940 | 175 | 82 | 13 |
| Alemania1941 | 184 | 83 | 13 |
| Alemania1942 | 173 | 79 | 13 |
| Alemania1943 | 172 | 76 | 12 |
| Alemania1944 | 174 | 68 | 12 |
| Italia1940 | 8 | 2 | — |
| Italia1941 | 26 | 9 | — |
| Italia1942 | 27 | 9 | — |
| Italia1943 | 28 | 9 | — |
| Cliente croata1941–1943 | 2 | 1 | — |
| Cliente croata1944 | 3 | 2 | — |

«Cuadrilátero» significa exactamente cinco coordenadas exteriores —incluido el cierre— y cero anillos interiores. No basta como criterio de rechazo: numerosos artefactos son **grupos de celdas unidas**, con más vértices. Tampoco se debe borrar toda pieza pequeña: las islas reales necesitan conservarse.

En Alemania1942, el original contiene estas muestras interiores —no sólo puntos sobre el borde—:

| Índice del componente | Referencia contemporánea que contiene la muestra | Longitud, latitud | ¿Sólo cuatro esquinas? |
| --- | --- | --- | --- |
| 63 | Suecia |18,48446;59,39957|No|
|139|Irán|48,24151;30,46857|Sí|
|140|Irak|47,73497;30,98271|No|
|141|Irán|47,83791;31,49685|No|
|142|Irán|47,93900;31,68966|No|
|143|Irán|47,88789;31,88247|No|
|144|Referencia actual deIsrael|35,76909;32,84661|No|
|145|Siria|35,86668;33,07161|No|
|146|Siria|35,81117;33,29662|No|
|147|Irak|39,61806;33,74670|Sí|
|148|Irak|40,51500;34,19686|Sí|
|149|Irak|41,23197;35,03314|Sí|
|151|Irán|44,67107;39,67594|No|

La referencia contemporánea sólo localiza la muestra; no atribuye soberanía histórica, especialmente en el Levante. El JSON conserva coordenadas completas, superficie diagnóstica, vértices, huecos, SHA-256 por componente y repetición entre años. Hay243 firmas de componentes alemanes repetidas entre registros y22 firmas repetidas con muestras en estas regiones evidentemente ajenas. Los componentes italianos y croatas también deben pasar un control de costa y de ámbito; su simple validez topológica no acredita control histórico.

Los controles alemanes contienen nueve componentes con muestras en laItalia actual en1940–1943, seis en1944. Las muestras de1940–1942 son señales evidentes de contaminación; en1943–1944 hay que distinguirlas de la ocupación real del centro/norte italiano. No aplicar la misma lista de países excluidos a todos los años.

## Reglas documentales para geometrías completas

Las siguientes son ventanas en las que una sustitución por **la tierra de la entidad fechada** puede corregir desajustes de costa; no son autorización para colorear todas sus colonias, dependencias o reclamaciones. Para una vista al cierre de año,1944 necesita tratamientos de liberación separados.

| Entidad o región | Uso defendible | Excepciones necesarias |
| --- | --- | --- |
| Dinamarca propiamente dicha | Ocupación alemana desde9/4/1940; cierres1940–1944 | No convertir Groenlandia niFeroe en tierra ocupada por heredar administración danesa. La liberación1945 deBornholm tuvo secuencia diferente. |
| Noruega continental | Ocupación desde la invasión9/4/1940 y fin de la campaña en junio; cierres1940–1943 | Finnmark oriental se libera en octubre1944. No completar automáticamente todoNoruega al cierre1944. Svalbard tiene historia diferente. |
| Países Bajos europeos | Ocupación desde mayo1940; cierres1940–1943 | Parte del sur se libera desde septiembre1944; el norte y oeste siguen ocupados. Ninguna sustitución completa al cierre1944. |
| Bélgica europea | Ocupación desde mayo1940; cierres1940–1943 | Liberación progresiva desde septiembre1944 y nueva ofensiva alemana enArdenas en diciembre. Congo y otras dependencias no se transfieren automáticamente. |
| Luxemburgo | Ocupación desde10/5/1940; cierres1940–1943 | Liberación septiembre1944 y batalla deArdenas diciembre1944–enero1945: no marcar todo el país ocupado al cierre1944. |
| Bohemia yMoravia restantes | Ocupación desde15/3/1939 | Separar losSudetes incorporados en1938 y laEslovaquia cliente. No usar todaChecoslovaquia como ocupación alemana directa. |
| Francia metropolitana | Partición desde junio1940; ampliación de ocupación en noviembre1942 | Francia sur no era alemana1940–1941. Desde noviembre1942 existe también zona italiana; no convertir todaFrancia en control alemán. Liberación1944 exige fronteras del año. |
| Italia | Ocupación alemana del centro/norte después8/9/1943 | No Alemania en la bota1940–1942. Sur e islas liberados, RSI y zonas operativas alemanas deben distinguirse; Roma liberada junio1944. |
| Estado Independiente deCroacia | Estado cliente desde abril1941 | No fue una anexión alemana íntegra: existían zonas alemanas/italianas, anexiones italianas enDalmacia/islas y control partisano. El armisticio italiano de septiembre1943 altera la situación. |

### Fuentes institucionales y primarias

- [Museo Nacional deDinamarca: ocupación1940–1945](https://en.natmus.dk/historical-knowledge/denmark/german-occupation-1940-1945/). Documenta invasión y capitulación del9/4, cooperación institucional danesa y liberación de mayo1945, con la excepción deBornholm. Ocupación no equivale a una anexión ni borra la continuidad institucional.
- [National Army Museum: campaña deNoruega](https://www.nam.ac.uk/explore/defeat-west) y [documento original1546-PS, memorando deRaeder, edición del proceso deNúremberg](https://avalon.law.yale.edu/imt/1546-ps.asp). Diferenciar fecha de invasión de fin de la campaña y de los Gobiernos rivales.
- [Gobierno deNoruega: liberación deKirkenes25/10/1944](https://www.regjeringen.no/no/aktuelt/80-arsmarkering-av-frigjoringen-av-ost-finnmark/id3066497/) y [Archivo Nacional noruego: liberación deFinnmark oriental](https://www.nasjonalarkivet.no/frigjoring-og-gjenreisning-i-troms-og-finnmark/). El resto deTroms/Finnmark no se libera hasta mayo1945.
- [Instituto Polar Noruego, historia deSvalbard](https://cruise-handbook.npolar.no/en/svalbard/history.html) y [Svalbard Museum](https://svalbardmuseum.no/en/world-war-ii). Evacuación aliada en agosto–septiembre1941, guarnición aliada desde1942 y estaciones meteorológicas alemanas puntuales. Una estación no permite colorear todo el archipiélago como país ocupado porAlemania.
- [NIMH: invasión del10/5/1940](https://www.nimh.nl/militaire-geschiedenis-van-nederland/webthemas/de-meidagen-van-1940/de-strijd-op-nederlands-grondgebied), [Biblioteca Nacional neerlandesa: campaña y rendición15/5](https://collecties.kb.nl/themas/tweede-wereldoorlog/meidagen-1940) y [Archivo Nacional: liberación del sur desde12/9/1944](https://www.nationaalarchief.nl/onderzoeken/nieuws/recht-en-onrecht-de-bevrijding-van-zuid-nederland-en-de-nasleep). La expansión aliada se detiene junto a los grandes ríos; el norte espera hasta1945.
- [CegeSoma/Archivos del Estado belga: cronología1940](https://www.belgiumwwii.be/belgique-en-guerre/ligne-du-temps.html) y [liberación progresiva desde3/9/1944](https://www.belgiumwwii.be/belgique-en-guerre/articles/belgique-est-progressivement-liberee-la.html). [Campaña oficial de laRAF, avance sobreBélgica septiembre1944](https://www.raf.mod.uk/what-we-do/our-history/air-historical-branch/second-world-war-campaign-narratives/liberation-of-north-west-europe-vol-iv-the-breakout-and-advance-to-the-lower-rhine-12-jun-30-sep-1944/) aporta cartografía primaria por fases, sin autorizar inferir un único frente para todo el año.
- [Gobierno deLuxemburgo: Segunda Guerra Mundial](https://luxembourg.public.lu/en/society-and-culture/history/second-world-war.html) y [cronología gubernamental de las dos liberaciones](https://gouvernement.lu/dam-assets/fr/actualites/articles/2004/09/03liberation/depliant_veterans.pdf). El territorio fue liberado en septiembre, antes de la nueva ofensiva deArdenas. La [Biblioteca Nacional conserva el diario oficial de ocupación](https://eluxemburgensia.lu/en/periodicals/verordnungsblatt),10/5/1940–24/8/1944.
- [USHMM: partición checoslovaca](https://encyclopedia.ushmm.org/content/en/article/czechoslovakia). LosSudetes, el territorio deTeschen, el arbitraje deViena, Eslovaquia y el protectorado checo no son una sola incorporación simultánea.
- [Ministerio francés deDefensa: línea de demarcación](https://www.cheminsdememoire.gouv.fr/fr/la-ligne-de-demarcation-0), [ocupación deFrancia](https://www.defense.gouv.fr/chemins-memoire/histoire-memoires/ressources-historiques/seconde-guerre-mondiale/loccupation-collaboration-0) y [Ministerio francés delInterior: zonas](https://formation-civique.interieur.gouv.fr/fiches-par-thematiques/histoire-geographie-et-culture/zoom-sur/focus-sur-la-seconde-guerre-mondiale-la-resistance-et-la-lib%C3%A9ration/). Zona italiana desde noviembre1942 a septiembre1943, distinta de Alemania y deVichy.
- [USHMM: Italia](https://encyclopedia.ushmm.org/content/en/article/italy) y [Museo de laShoah/CDEC:8/9/1943](https://shoahmuseum.cdec.it/albums/lotto-settembre-1943/). La ocupación alemana y laRSI son posteriores al armisticio; Prealpes yLitoralAdriático tuvieron administración alemana directa, mientras el frente separaba territorios aliados al sur. El material italiano del original no puede prolongarse como si todo1943 fuese una única fase.
- [USHMM, Encyclopedia ofCamps andGhettos, volumenIII, secciónCroatia](https://www.ushmm.org/m/pdfs/USHMM-Encyclopedia-Camps-Ghettos-Vol-III.pdf). Se documentan proclamación deabril1941, régimen cliente, zonas de influencia, cesiones costeras y transformación en septiembre1943. La referencia del resumen a un día de los tratados deRoma difiere de otras cronologías; usar el mes de mayo1941 hasta contrastar el original, sin fabricar una fecha exacta.

## Aplicación recomendada

1. Construir la partición sobre una malla terrestre compartida. Los controles son instrucciones de reasignación de esa tierra; no aportan una segunda costa libre que se superponga a otra.
2. Rechazar componentes remotos y grupos de celdas fuera del ámbito documental fechado, no únicamente polígonos de cinco vértices. Los SHA del JSON ayudan a contrastar los artefactos repetidos sin suponer que cualquier forma pequeña es falsa.
3. La geometría gruesa de una ocupación no debe dejar doble costa ni una cinta del país anterior alrededor de un Estado completamente ocupado. Para los casos de la tabla puede usarse su contorno terrestre fechado, con las excepciones expresas; una ocupación parcial requiere su corte interior o frente, no una extensión completa.
4. Los países aliados y los clientes permanecen distintos de la potencia. La presencia de unidades alemanas enFinlandia, Suecia oCroacia no acredita por sí misma soberanía o ocupación nacional alemana.
5. Las franjas deben recortarse contra el **propietario/controlador final de la partición**. En el algoritmo anterior se generan intersecciones alemanas antes de que un cliente posterior reemplace el territorio; si no se recortan después, una franja alemana puede seguir cubriendo el cliente croata aunque la geometría final ya sea otra. Revisar esta ruta además de la tierra base.
6. Una vista1944 al cierre anual no puede reutilizar automáticamente las máximas extensiones de1942 o completar estados ya liberados. Conservar la incertidumbre del momento anual deCliopatria y no etiquetarlo como frente exacto del31/12.

## Runtime local comprobado

El ejecutable `C:/Users/darim/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe` esPython3.12.14. Al anteponer `.cache/python-packages` a `sys.path` cargaShapely2.2.0 y sus binarioscp312. LosPython de sistema3.14/3.13 no pueden cargar esa copia y no tienenShapely instalado globalmente. No fue necesario instalar paquetes nuevos ni modificar el equipo.

## Límites del informe

El JSON diagnostica polígonos originales y ubica muestras enNaturalEarth contemporáneo; no resuelve soberanía ni produce un nuevo atlas de frentes. Las superficies aproximadas usan grados y coseno de latitud, suficientes para detectar clases de tamaño, no para estadísticas territoriales. La división detallada deGrecia/Yugoslavia, fronteras de1944, enclaves, guarniciones y municipios requieren geometría acreditada propia. No se afirma que estas reglas documenten todos los teatros de la guerra.
