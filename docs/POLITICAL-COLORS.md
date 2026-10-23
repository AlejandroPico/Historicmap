# Familias de color político

**Contrato vigente desde 0.9:** el control territorial se integra en la geometría seleccionable. El botón de ocupaciones añade franjas opcionales y ya no alterna entre control y soberanía. La explicación original de ese interruptor más abajo queda sustituida por esta decisión posterior del propietario. Más detalle en DELIVERY-0.9.0 y sección18 de agentes.md.

`src/historical-palette.ts` contiene33 familias editoriales y `docs/POLITICAL-PALETTE.csv` permite revisarlas. Roma y Bizancio tienen púrpuras distintos; España imperial, dorado; Francia napoleónica, azul; Alemania nazi, gris; URSS, rojo; Reino Unido, rosa malva. Francia, España, Alemania, Italia y Portugal tienen etapas de régimen diferenciadas; otros casos siguen necesitando curación. Ninguna tinta constituye una clasificación ideológica universal ni un color oficial acreditado de todos los imperios.

Las franjas son3:1, controlador en ancho mayor y territorio ocupado en ancho menor. Las incorporaciones documentadas en la base y el ámbito alemán de1938 no se tratan como simples ocupaciones posteriores. Las reclamaciones actuales no se reconocen como cesiones por esta regla. El inventario geométrico es parcial y no contiene todos los frentes/anexiones.

El CSV original del propietario **no estaba disponible en la ruta indicada**. No se presenta este catálogo propio como importación de ese documento; conciliación pendiente al recuperarlo.

El propietario solicita que los territorios dependientes, Estados satélite y países sometidos a tutela compartan una familia de color con la potencia dominante, con matices que permitan distinguirlos. La URSS conserva el rojo, Estados Unidos el azul y Alemania nazi el gris oscuro. Esta convención es editorial; nunca transforma por sí sola una relación de influencia en soberanía o una alianza en subordinación.

## Aplicación

`political.ts` resuelve primero la identidad de cada entidad del año. Para una colonia, protectorado o mandato con administrador documentado, busca la identidad de esa potencia en el mismo inventario: Portugal/PRT, por ejemplo, ya no producen colores distintos por utilizar nombre y código diferentes. Aplica un matiz claro estable de su color principal, sin cambiar geometrías, fronteras, nombre, capital o identidad del territorio. En la referencia contemporánea se aplica también a la categoría explícita Dependency de Natural Earth; no se utiliza una reclamación de una entidad Disputed para asignarle potencia. Los metadatos actuales nunca se proyectan a la cartografía histórica.

`political-influence.json` incorpora doce relaciones fechadas de satélite, bloque con autonomía, Estado cliente, ocupación o intervención. El mapa evalúa el cierre anual; inicio inclusivo y fin exclusivo. El registro incluye potencia, claves de las entidades, fuente y explicación. Una entrada no se crea a partir de la bandera, ideología o pertenencia a una organización.

- Polonia, Hungría, Checoslovaquia, Bulgaria y RDA: familia soviética roja durante las etapas documentadas. Sus transiciones políticas cierran los intervalos; la permanencia de tropas no equivale por sí sola a continuidad del régimen anterior. La RDA sigue siendo una entidad separada hasta su desaparición, aunque termine antes la relación cromática.
- Rumanía: etapa satélite anterior a 1964 y tono más suave para el bloque con creciente autonomía posterior. No se describe como una incorporación soviética.
- Albania: relación soviética hasta la ruptura de 1961. Yugoslavia y Albania no se colorean como satélites de Moscú en 1970 sólo por tener gobiernos comunistas.
- Eslovaquia de 1939–1945: matiz de la Alemania nazi para su condición de Estado cliente; no equivale al Protectorado de Bohemia y Moravia ni a territorio anexionado.
- Japón bajo ocupación aliada dirigida por Estados Unidos, Gobierno de Kabul apoyado por la intervención soviética y Gobierno de Phnom Penh apoyado militarmente por Vietnam: matices de la potencia correspondiente. Estas relaciones de ocupación/intervención siguen el botón «Ocupaciones y disputas»; desactivarlo recupera el color soberano de base.

Las ocupaciones ya documentadas en las capas de control conservan un color sólido por potencia, y sus clientes identificados conservan matices claros. No se inventan líneas de frente para completar una relación política. Las capas estadísticas o de organizaciones utilizan su propia escala/categoría y prevalecen sobre esta pintura política.

La ficha explica la relación en Territorio y Relaciones, con enlace a su fuente. La leyenda resume el significado de los matices. El estado de selección y los paneles siguen conservándose al cambiar de fecha o de capa.

## Fuentes y límites

Fuentes por registro: Office of the Historian y documentación diplomática FRUS, Biblioteca del Congreso, Deutsches Historisches Museum, ECCC y documentación de retirada militar. Se conserva la fuente complementaria de retirada cuando es distinta de la que acredita el comienzo. No se reproduce su texto ni sus valoraciones políticas.

Las fechas de inicio de algunas etapas del bloque son una síntesis anual declarada; no certifican un único día en que surgió toda dependencia. La autonomía rumana no tiene una escala numérica de control. Las tintas tampoco codifican porcentaje de territorio controlado.

El mecanismo general sirve para cualquier potencia y conflicto, pero el inventario de relaciones especiales **no es exhaustivo mundialmente**. Antes de ampliarlo se deben documentar jurisdicción, fechas, naturaleza de la relación y alternativas. Las dependencias coloniales se apoyan además en el administrador de la fuente cartográfica. No pintar como dominados a todos los miembros de OTAN, UE, BRICS o de cualquier otro pacto.

Las pruebas comprueban familia roja, matices diferenciados, rupturas temporales, autonomía, equivalencia entre nombre/código del administrador, ausencia de inferencia por alianza y separación de la pintura de intervención. `data:verify` comprueba integridad y ausencia de intervalos contradictorios por entidad; no certifica toda interpretación historiográfica.
