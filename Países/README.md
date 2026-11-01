# Países y entidades históricas

Empieza por [el índice legible](INDICE.md). Cada carpeta tiene una clave estable y un nombre: países actuales, entidades históricas, imperios y territorios de los conjuntos incorporados. No se crean carpetas para entidades aún ausentes de las fuentes.

`entidad.json` reúne nombres, banderas, mandatos con retratos y referencias a registros territoriales. Cada medio conserva licencia, autor, origen y ruta local; las imágenes están en `public/media` y los polígonos en `public/data`, sin multiplicar miles de copias ni mezclar licencias geográficas. Los regímenes de una misma identidad mantienen sus intervalos; las identidades históricas distintas conservan carpetas propias. Los registros sin equivalencia contrastada no se fusionan por semejanza.

Este inventario se genera con `npm run entities:prepare`. Las nuevas adquisiciones y curaciones se escriben en los archivos canónicos de su propietario dentro de `Países`; sus compiladores producen `public/data` y después se regenera el inventario. **No editar `entidad.json`: se reemplaza al regenerar.** No es una segunda base de datos independiente. `recursos.json` y `archivos/` son entradas propias y no se sobrescriben. `npm run build` actualiza y valida el inventario antes de compilar.

## Correcciones históricas por entidad

Las revisiones nuevas se guardan en **`revision-historica.json` dentro de la carpeta de la entidad**: símbolos con fechas, cargos, instituciones, clasificación y fuentes. `simbolos/` y `retratos/` contienen sus originales acreditados. No dispersar estas correcciones en listas de países fuera de este directorio. El escritor genérico `scripts/prepare-entity-revisions.py` carece de hechos históricos propios: compila esas entradas en los conjuntos de ejecución compartidos. `python scripts/prepare-entity-revisions.py` funciona sin consultas de adquisición; `--acquire` es una operación explícita para incorporar nuevos archivos de Commons con licencia y metadatos comprobados. Después se regenera el catálogo y las huellas del manifiesto de datos.

Las copias de ejecución permanecen en `public/media` para servirlas con rutas estables. `canonicalFile` conserva la ruta del original en esta carpeta. Las revisiones y originales no se sobrescriben al generar `entidad.json`. Se verifican sus huellas; modificar un original exige revisar sus metadatos y procedencia.

`flags` conserva vigencias históricas. **`symbolReferences` es distinto**: permite mostrar un escudo atribuido, una reconstrucción o un testimonio posterior como referencia retrospectiva, con fecha de evidencia visible. Su intervalo corresponde a la entidad representada, no acredita que el símbolo existiese entonces. Estas referencias no generan acontecimientos de adopción de bandera en la cronología. Una bandera documentada vigente tiene prioridad sobre ellas. No convertir la fecha de un portulano, sello o cuadro en una adopción nacional.

## Pueblos y regiones de poblamiento

Las entradas canónicas de esta revisión se guardan en `poblamiento/*.json`, dentro de la carpeta de la entidad. Cada entrada conserva nombres originales, fases de consulta, interpretación, fuentes, incertidumbres, decisión de adopción o exclusión y tareas documentales pendientes. Su GeoJSON original acreditado se guarda en la misma carpeta y se comprueba por SHA-256. `ownerKey` identifica la carpeta; `contextKey` permite seleccionar una región sin atribuirle automáticamente las autoridades o la bandera de un país moderno.

Preparación sin acceso remoto: `npm run regions:prepare`, seguida de `npm run entities:prepare`. Se generan dos recursos de ejecución en `public/data` y una auditoría en `docs`; esas copias no sustituyen los originales. Las vistas `entidad.json` incluyen los registros regionales y las exclusiones correspondientes. No editar esas vistas generadas. El compilador obtiene la cobertura de las entradas: no ampliar un siglo cambiando solamente un límite de código.

Una ventana de consulta no acredita la extensión exacta en cada uno de sus años. Mantener separados fecha del mapa, cronología documentada y límite de revisión. Las referencias políticas redundantes se suprimen visualmente cuando existe su identidad en la base anual; los pueblos y regiones culturales permanecen consultables bajo ella. Metodología y pendientes en [CULTURAL-COVERAGE.md](../docs/CULTURAL-COVERAGE.md).

Desde 0.29, una misma entidad puede tener varios dossiers espaciales: `key` identifica la entrada y `contextKey` mantiene la ficha entre fases. Los intervalos de un mismo contexto no se solapan. Conservar las carpetas canónicas aunque cambie el título de una fase; el catálogo reutiliza su ubicación. No fusionar nombres sólo por eliminar acentos o por parecido gráfico. `temporalMode: traditional-area-undated` identifica áreas tradicionales sin cronología local suficiente y exige explicarlo en la ficha. Las agrupaciones amplias pueden declarar relaciones con subdivisiones: éstas conservan sus nombres y el área de fondo sigue seleccionable.

## Añadir un himno o documento

1. Coloca un archivo autorizado dentro de `archivos/` en la carpeta correspondiente. Se admiten mp3, ogg, wav, m4a y pdf.
2. Decláralo en `recursos.json` con título, procedencia, licencia y fechas. Si la carpeta histórica no tiene ese archivo, créalo con la clave de `entidad.json`. Ejemplo de estructura (no es una grabación incorporada):

```json
{
  "key": "ESP",
  "resources": [{
    "file": "himno.ogg",
    "title": "Título de la grabación",
    "artist": "Intérprete y autoría",
    "source": "https://fuente-del-archivo.example/registro",
    "license": "Licencia comprobada de esta grabación",
    "start": "2000-01-01",
    "end": "2026-12-31"
  }]
}
```

3. Ejecuta la preparación/compilación. La aplicación detecta los archivos declarados sin editar código y muestra los recursos vigentes en **Datos**. La vigencia de un himno y los derechos de una interpretación son cuestiones distintas. No se reproducen sonidos automáticamente.

La validación rechaza archivos sin declaración, sin fechas/licencia o que no existen. Las fechas son inclusivas. Si no hay un recurso acreditado no aparece un reproductor vacío. El catálogo no incorpora himnos ni grabaciones por defecto.

## Continuidad regional desde 0.30

Las fases `historical-area-context` conservan una referencia espacial anterior cuando la fuente posterior omite el detalle cultural. No acreditan residencia constante, soberanía ni fronteras anuales; `continuationReference` y la ficha explican la limitación. `baseRepresentationReview` conserva el contraste de remisiones a la base política: propietario, candidatos nominales y puntos coincidentes no son equivalencias históricas automáticas. Los pendientes permanecen en el dossier.

El compilador genera once segmentos por siglo entre900 y1905, además del export completo para auditoría. La aplicación descarga y reutiliza sólo el segmento visitado. No editar las copias públicas: las geometrías originales, fuentes, decisiones y fases permanecen en `poblamiento/` de cada entidad. [Revisión conjunta y límites](../docs/CULTURAL-GLOBAL-REVIEW.md).

## Revisión contemporánea0.31

Las nuevas fases1906–2027 guardan `reviewedOn`, `evidenceThrough`, interpretación y fuentes propias. `modernConsultationReview` registra alcance y pendientes por entidad. Una reforma o reconocimiento no crea el pueblo ni determina su frontera; las referencias históricas no son un mapa del domicilio actual. Las fases y referencias anteriores se conservan sin cambios. La consulta2027 no añade observaciones futuras y el máximo de la aplicación sigue al reloj. Ver [revisión moderna](../docs/CULTURAL-MODERN-REVIEW.md).

## Correcciones de retratos0.31.1

`portraitCorrections` en `revision-historica.json` puede corregir el retrato de una persona sin reemplazar sus mandatos. Original en `retratos/`, título, fecha de evidencia, motivo, fuente, licencia y huella dentro de la entidad. Ejecutar `python scripts/prepare-entity-revisions.py --portraits-only` y después `npm run entities:prepare`; no hay descarga remota. La compilación completa de revisiones aplica también estas correcciones al final. No editar la vista generada `entidad.json` ni reutilizar un cartel como retrato por contener la cara de la persona.


## Referencias arqueológicas (desde0.48)

Un yacimiento o red sin mandatos acreditados puede tener `arqueologia.json` en su carpeta propietaria. Contrato `archaeological-evidence`: rangos de consulta, fechas de evidencia, notas de autoridades, puntos con `referenceKind: archaeological-site`, fuentes y contexto. No admite líderes, símbolos nacionales o reglas de fronteras supuestos; la complejidad material no atribuye por defecto una constitución. Las fechas pueden abarcar milenios de consulta, sin ampliar el máximo de400 años de los lotes políticos. Un rango no prueba ocupación continua.

Compilar con `prepare-entity-revisions.py` y registrar con `register-entity-revisions.mjs`. El catálogo conserva la ruta canónica indicada por `identity.canonicalFile` de las nuevas identidades, evitando crear otra carpeta para su vista generada. Los datos arqueológicos y los originales de `poblamiento/` son distintos; los públicos se derivan, no se editan a mano. [Fuentes y límites](../docs/RESEARCH-bc6000.md).


## Referencias arqueológicas por tramo · 0.49

`arqueologia.json` conserva la evidencia ya publicada del propietario. Las ampliaciones disjuntas pueden añadirse en `arqueologia/<tramo>.json`, por ejemplo `arqueologia/bc10000-bc6001.json`, con formato `archaeological-evidence`. Se conservan clave, carpeta y originales anteriores. Los puntos no son capitales por defecto ni acreditan gobernantes, banderas nacionales o una constitución. Los contextos deben llevar `type: transition` y `confidence: archaeological-reference`; los intervalos de consulta no prueban ocupación continua.

Compilar las revisiones y ejecutar `scripts/register-entity-revisions.mjs` antes de las comprobaciones para sincronizar datos, manifiestos, rótulos y catálogo. Los fenómenos naturales, como márgenes de hielo o cronología estratigráfica, pertenecen al catálogo `Tierra/`; no son nuevos países. Véase [el alcance de esta ampliación](../docs/RESEARCH-bc10000.md).

## Evidencias humanas pleistocenas

`arqueologia/bc100000-bc10001.json` usa el contrato `archaeological-evidence` y registros `homininEvidence`: ID estable, atribución humana, cultura material, nivel, coordenadas con precisión declarada, edades y unidades originales, ventana civil de consulta, fuente, licencia y bibliografía. Las filas de compilación conservan número de fila, propiedades originales y SHA-256/URL del libro. No se completan líderes, símbolos o fronteras supuestos. Varios estudios del mismo yacimiento contrastado comparten propietario, preservando cada intervalo.

`node scripts/prepare-human-evidence.mjs` produce el recurso compartido `human-evidence.geojson` y su índice. Después se compilan y registran las revisiones de entidades para actualizar las vistas automáticas. La interfaz filtra los registros activos y agrupa por propietario, sin rellenar los huecos entre dataciones. [Método, fuentes y pendientes](../docs/RESEARCH-bc100000.md).

El archivo hermano `bc100000-bc10001-paleohumans.json` conserva la adquisición PaleoHumans1.0.0 en el mismo propietario cuando la equivalencia se contrasta. Sus fechas de fase son ventanas contextuales; resultados originales sin calibrar, muestras, técnicas e individuos se mantienen en `originalProperties`. `undatedEvidence` guarda contextos inciertos que no se dibujan con fechas supuestas. Si no hay ningún contexto utilizable, `coverageIsConsultationEnvelope` identifica un sobre de consulta documental y no una ocupación fechada. No interpretar edad al morir como fecha histórica.
