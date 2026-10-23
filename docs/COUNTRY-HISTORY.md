# Relaciones entre entidades e instituciones

Adquisición y referencia: **23 de octubre de 2026**. Catálogo `public/data/country-history.json`, reproducible sin red con `scripts/prepare-country-history.py`. Contiene **33 relaciones dirigidas**, **28 registros** (15 institucionales, 12 históricos y uno territorial), **55 claves de identidad** y **36 fuentes institucionales**. No son 55 Estados con historias completas.

Las síntesis en español son redacción original. No se redistribuyen textos extensos, mapas, retratos ni otros medios de las páginas citadas. Los sitios de origen mantienen sus propias condiciones. El catálogo es un índice editorial de navegación y contexto, **no un registro jurídico completo de sucesión de Estados**, una nueva cartografía o un inventario mundial de constituciones.

## Contrato

La raíz contiene `retrieved`, `referenceDate`, `format`, `license`, `coverage`, `intervals`, `sources`, `relations` y `records`.

Una relación tiene `id`, `from`, `to`, `date`, `type`, `label`, `note`, `source` y `sourceLabel`. Cada extremo incluye `key`, `name` y `year`. Las claves corresponden al catálogo de identidades del atlas, incluidos `USSR`, `FRY`, `SCG`, `CSK`, `DDR`, `YAR`, `YPR`, `SDS` y `KOS`. No sustituirlas globalmente por los códigos estadísticos o cartográficos de sus sucesores.

`date` es la fecha del **hecho descrito en la etiqueta y la nota**. `from.year` y `to.year` son destinos de navegación anual elegidos para mostrar la entidad en la cartografía disponible. Pueden diferir del año de la declaración, del reconocimiento, de la admisión en Naciones Unidas o de otro hito del proceso. Por ejemplo, el enlace de Lituania señala su acto de restauración de 1990, pero navega a 1992 para garantizar una entidad separada en la base cartográfica anual. El enlace de la RDA parte de 1989 porque el mapa al cierre de 1990 ya muestra Alemania reunificada.

Tipos de relación incluidos:

| Tipo | Interpretación limitada |
| --- | --- |
| `dissolution` | Relación territorial tras la disolución; no continuidad jurídica exclusiva. |
| `continuation` | Continuidad específica señalada en la fuente; no herencia de todos los territorios, datos o instituciones. |
| `restoration` | Restauración de independencia estatal, distinguida de una creación estatal o sucesión automática. |
| `reconstitution` | Cambio de marco o nombre de una entidad sin deducir nueva membresía internacional. |
| `accession` | Adhesión, en este catálogo la RDA a la República Federal. |
| `unification` | Unión de entidades, aquí los dos Yemen. |
| `independence` | Constitución o acceso a independencia, con hitos alternativos aclarados. |
| `decolonization` | Terminación de una administración colonial u ocupante, sin legitimar su soberanía. |
| `declaration` | Declaración con reconocimiento dividido; no afirmación de reconocimiento universal. |

Un registro contiene `id`, `keys`, `start`, `end` opcional, `section`, `title`, `text`, `source` y `sourceLabel`. `section` es `institutions`, `history` o `territory`. Los intervalos son **inicio inclusivo y fin exclusivo**. Sin final, el horizonte está limitado a `referenceDate`; nunca extrapolar al año futuro del reloj. Los eventos de un día llevan como final el día siguiente; el referéndum de Eritrea abarca del 23 al 25 de abril de 1993. La cronología puede conservar un acontecimiento como hito después de su fecha, pero eso no convierte su texto en una institución activa de todos los años posteriores.

## Familias de navegación y cautelas

- **URSS y quince entidades posteriores:** once relaciones fechadas en la disolución del 26/12/1991, continuidad específica de la membresía ONU por Rusia comunicada el 24/12 y restauraciones de Estonia, Letonia y Lituania con fuentes de sus instituciones. El 26 de diciembre no es una fecha universal de declaración de independencia. [Antecedentes rusos](https://1997-2001.state.gov/background_notes/russia_0898_bgn.html), [continuidad ONU](https://www.un.org/en/about-us/member-states/russian-federation).
- **Yugoslavia:** Eslovenia, Croacia, Bosnia y Macedonia llevan las fechas efectivas de sucesión en tratados recogidas por la ONU, distinguidas de otros hitos de independencia. La federación de Serbia y Montenegro de 1992 no hereda automáticamente la membresía de Yugoslavia socialista; se registra su admisión de 2000. El nombre y marco de Serbia y Montenegro cambian en 2003. En 2006 Serbia continúa la membresía de esa unión y Montenegro es admitido por separado. [ONU y sucesores](https://www.un.org/en/about-us/member-states/yugoslavia), [A/60/351](https://digitallibrary.un.org/record/558855/files/A_60_351-EN.pdf), [depositario de tratados](https://treaties.un.org/pages/HistoricalInfo.aspx).
- **Checoslovaquia:** dos enlaces desde 1992 a 1993; no se atribuye a un solo país la continuidad íntegra de la federación. [ONU](https://www.un.org/en/about-us/member-states/czechoslovakia).
- **Alemania:** adhesión de la RDA a la República Federal el 3/10/1990, no fundación de una nueva RDA mediante fusión. [Gobierno federal](https://www.bundesregierung.de/breg-de/schwerpunkte/deutsche-einheit/einigungsvertrag-353990).
- **Yemen:** dos enlaces de unificación del 22/05/1990. [ONU](https://www.un.org/en/about-us/growth-in-un-membership).
- **Sudán y Sudán del Sur:** independencia del segundo el 9/07/2011; Sudán continúa existiendo. Las estadísticas del antiguo conjunto no se reparten ni heredan automáticamente. [ONU](https://unterm.un.org/unterm2/en/view/UNHQ/dd08eda8-c78a-4f4f-bd1f-8c2d1538e03d).
- **Eritrea:** referéndum del 23–25/04/1993, declaración posterior en abril y celebraciones oficiales del 24/05 son hitos distintos. El enlace utiliza esta última fecha, explicitándolo. [Informe anual ONU](https://digitallibrary.un.org/record/173272/files/327786-EN.pdf), [mensaje del 24 de mayo](https://digitallibrary.un.org/record/218378?ln=en).
- **Timor-Leste:** enlace desde la Indonesia de 1998 a la independencia de 2002 que declara la fase intermedia UNTAET de 1999–2002. No legitima la anexión indonesia ni elimina la identidad histórica timorense o la cuestión de descolonización. [UNTAET](https://peacekeeping.un.org/sites/default/files/past/etimor/etimor.htm).
- **Namibia:** independencia y fin de la administración sudafricana, sin reconocer soberanía de Sudáfrica sobre Namibia. [UNTAG](https://peacekeeping.un.org/sites/default/files/past/untagFT.htm).
- **Kosovo:** declaración de 2008 con reconocimiento internacional dividido. La opinión consultiva de la CIJ de 2010 resolvió la cuestión limitada de la declaración, sin imponer reconocimiento ni decidir en general la estatalidad. [CIJ](https://www.icj-cij.org/node/103912).

## Instituciones y acontecimientos

Hay síntesis constitucionales para España, Francia, Alemania, Japón, India, Brasil, Sudáfrica, Italia, Portugal, Suiza, Estados Unidos, Canadá, México y Argentina, más la fase transitoria de Naciones Unidas en Timor Oriental. Se describen estructuras y distinción entre cargos, no índices de democracia, partidos vigentes, composición parlamentaria o resultados electorales no adquiridos.

Los inicios de Estados Unidos, Canadá y México en 1990, y Argentina en 1995, son **límites editoriales de cobertura** declarados en el texto, no fechas de fundación de sus instituciones. El intervalo argentino comienza después de la reforma de 1994 para no trasladar reformas posteriores al año anterior. Las síntesis estables no afirman que todo el articulado constitucional actual haya existido sin cambios desde la fecha inicial. La Ley Fundamental alemana no se aplica a una ficha de la RDA; el texto sudafricano de 1996 no se retrotrae al periodo de apartheid ni al marco interino de 1994.

La cronología adicional registra la Segunda República española y su Constitución de 1931, proclamación de Juan Carlos I en 1975, Constitución española de 1978, Quinta República francesa, constituciones brasileña, sudafricana y suiza, admisión ONU de la Yugoslavia federal, UNTAET, referéndum eritreo y opinión consultiva sobre Kosovo. El catálogo existente de autoridades, banderas, afiliaciones y conflictos proporciona otras series; no se duplican sus registros aquí.

## Validación y ampliación

El generador comprueba identificadores únicos e intervalos ordenados. La revisión focal verificó que las **55 claves existen** en `identities.json`, que las fuentes son URLs institucionales y que los años de navegación no sustituyen las fechas de evento. No modifica geometrías, retratos, banderas ni indicadores económicos.

Para ampliar: añadir una relación por hecho y destino, usar nombres pertinentes a la época, documentar qué representa su fecha, comprobar que la entidad puede seleccionarse en el año de navegación, citar una fuente primaria y mantener separadas continuidad, independencia, restauración y control efectivo. No resolver países desaparecidos con el primer sucesor disponible. No extender por similitud una estructura constitucional a territorios dependientes o a gobiernos rivales. La ausencia de un enlace expresa cobertura pendiente.
