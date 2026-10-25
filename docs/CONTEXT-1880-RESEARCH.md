# Contexto e instituciones mundiales,1880–1899

Integración: `scripts/prepare-1880-context.py`. Investigación realizada en octubre2026. Es una ampliación focal y documentada, no un inventario mundial exhaustivo de guerras, tratados, Estados o alianzas.

## Contrato del preparador

La función pura `prepare(affiliations, context, history)` recibe los tres catálogos y devuelve copias ampliadas. No realiza consultas, descargas ni escrituras. La línea de órdenes comprueba en memoria por defecto, o con `--check`; sólo escribe al proporcionar `--output-dir`, que debe ser distinto de la carpeta de entrada. No debe ejecutarse después el preparador1900, que reconstruye la Triple Alianza y retiraría estos intervalos anteriores.

Las altas llevan prefijo `extension-1880-`; los intervalos son **inicio inclusivo y fin exclusivo** y están dentro de `[1880-01-01,1900-01-01)`. El corte1/1/1900 excluye por completo el año1900. Una transición tiene una fecha histórica separada de los años usados para navegar a las fichas. Se conservan literalmente los registros previos, todas las membresías previas y los metadatos de las organizaciones. Tampoco cambian `referenceDate`, `retrieved`, `expandedReferenceDate`, la referencia contemporánea, ni los extremos finales de cobertura.

Sólo se adelantan a1880 `coverageStart`/`startYear`. La idempotencia se obtiene sustituyendo únicamente las altas propias acotadas; si un identificador propio o una membresía propia aparecieran fuera de esa ventana se genera un error, en lugar de borrar información posterior. Para la Triple Alianza se exige la organización ya establecida y se rellenan sólo los huecos anteriores a1900, evitando solapamientos.

Resultado inicial de la extensión:23 eventos,20 textos de ficha,6 relaciones de transición y3 intervalos de membresía. La adquisición de imágenes, las autoridades personales, los indicadores y la cartografía se integran por otros módulos. Ninguno de los eventos, países vinculados o tratados contiene o genera geometrías de frentes, ocupaciones o anexiones.

## Alianzas: firma, ratificación y observación

### Triple Alianza

El [texto del tratado, conservado por GRIPS y la Universidad de Tokio](https://worldjpn.net/documents/texts/docs/18820520.T1E.html), fecha la firma20/5/1882 y distingue obligaciones de asistencia y neutralidad. Sus artículosVII–VIII ligan la vigencia al canje de ratificaciones. La [edición documental de AlfredFrancisPribram, *The Secret Treaties of Austria-Hungary*, vol.I, conservada por la Biblioteca Nacional de Hungría](https://mek.oszk.hu/07100/07162/pdf/secret01pribuoft.pdf), en las notas del primer tratado, fecha el canje en Viena **30/5/1882** e identifica el original archivístico. El servidor delPDF devolvió intermitentemente502; la nota fue recuperada mediante el texto indexado, no se afirma haber descargado el volumen.

Los tres signatarios son Alemania`DEU`, Austria-Hungría`AUH` e Italia`ITA`. La nueva observación de membresía empieza30/5/1882, se detiene por cobertura1/1/1900 y continúa con los registros ya existentes sin modificarlos. El campo histórico `formed` conserva la firma20/5 ya registrada; no se reescribe como si fuera el canje. La ficha de relaciones puede mencionar la firma anterior sin pintar una membresía efectiva antes del canje.

### Doble Alianza y alianza franco-rusa

El [tratado austro-alemán7/10/1879, edición Avalon de Yale](https://avalon.law.yale.edu/19th_century/dualalli.asp), documenta dos partes y asistencia condicionada. Se añade su contexto a las fichas desde1880 como corte de cobertura, sin atribuirle a Rusia una membresía. No se confunde su existencia con absorción de Austria-Hungría por Alemania.

La [convención militar franco-rusa, edición documental de Yale](https://avalon.law.yale.edu/19th_century/frrumil.asp), es de1892; la [Biblioteca Nacional de Francia](https://catalogue.bnf.fr/ark:/12148/cb11979428z) sitúa la aprobación de ambas partes entre diciembre1893 y enero1894. Se abre un texto de ficha desde1/2/1894, expresamente marcado como cobertura posterior a esa aprobación; no se inventa un acto jurídico ese día. El acercamiento diplomático, la convención y sus aprobaciones son fases diferentes.

Estas dos alianzas se documentan en fichas, sin generar organizaciones nuevas con una falsa fecha de extinción1900. Incorporarlas como capas requiere una serie coherente que continúe después de1899 y termine con fuente propia, trabajo fuera de este preparador acotado. No se crea una Triple Entente anterior a1907, ni se asigna al Reino Unido participación en la convención franco-rusa. No se reconstruyen rosters de laUPU,UIT u otras instituciones a partir de su lista moderna.

## Conflictos y transiciones investigados

| Ámbito | Fuente y criterio temporal |
|---|---|
| Guerra del Pacífico | [Biblioteca Nacional de Chile: operaciones1879–1884](https://www.memoriachilena.gob.cl/602/w3-article-693.html). Se incorpora la fase1880–1884 con extremos de cobertura anual; no se fusionan Ancón1883 y la tregua chileno-boliviana1884 en una sola paz definitiva. La cronología institucional contiene diferencias de día respecto a otros repertorios de la tregua; el preparador sólo afirma el año. |
| Chile1891 | [Memoria Chilena: guerra civil](https://www.memoriachilena.gob.cl/602/w3-article-706.html). Ruptura pública7/1, campaña y entrega del mando aBaquedano29/8; el intervalo no suministra polígonos de las facciones. |
| Primera guerra bóer | [National Army Museum: Transvaal War](https://www.nam.ac.uk/explore/transvaal-war). Proclamación republicana13/12/1880, armisticio6/3/1881 y paz23/3. La convención administrativa posterior se distingue del cese de la guerra. |
| Segunda guerra bóer | [National Army Museum: Boer War](https://www.nam.ac.uk/explore/boer-war). Ultimátum expira11/10/1899; cruce de fronteras12/10. Cierre1900 es cobertura; permanece intacta la fase posterior ya registrada. |
| Egipto y mahdismo | [National Army Museum: Egypt and Sudan](https://www.nam.ac.uk/explore/egypt-and-sudan). Se distinguen intervención1882, levantamiento desde1881, toma deJartum1885 y reconquista1896–1899. Los registros amplios usan límites mensuales/anuales declarados, no una fecha jurídica uniforme para todos los actores. |
| Guerra franco-china | [Departamento de Estado, *International Boundary Study*38, reproducción enFloridaStateUniversity](https://library.law.fsu.edu/Digital-Collections/LimitsinSeas/pdf/ibs038.pdf). Documenta firma deTianjin9/6/1885, canje28/11 y convención fronteriza1887. El intervalo1884–1885 es una ventana anual del conflicto; no se confunde con la convención sino-japonesa deTianjin18/4/1885. |
| Guerra sino-japonesa | [JACAR: documentos originales del comienzo de la guerra](https://jacar.go.jp/english/exhibition/jacarbl-fsjwar-e/about/p002.html). Combates25/7/1894, declaraciones1/8; el archivo conserva la decisión posterior de fijar el comienzo el25/7. [JACAR: tratado y retrocesión](https://www.jacar.go.jp/english/exhibition/jacarbl-fsjwar-e/glossary/g004.html), Shimonoseki17/4/1895, ratificación8/5 y devolución deLiaodong mediante otro acuerdo en noviembre. |
| Adwa | [Archivo histórico del Quirinale](https://archivio.quirinale.it/aspr/gianni-bisiach/AV-002-000186/1-marzo-1896-battaglia-adua). Se incorpora la batalla1/3/1896 como acontecimiento de un día, con contexto de la paz y soberanía etíope. No se pretenden reconstruir todos los frentes de1894–1896. |
| Madagascar | [Service historique de la Défense, inventario8H](https://www.servicehistorique.sga.defense.gouv.fr/sites/default/files/notices_files/SHDGR_INV_8H.pdf), expedición1894–1896; [Universidad dePerpiñán, textos normativos](https://mjp.univ-perp.fr/constit/mg1896.htm), tratado17/12/1885, aprobación6/3/1886 y ley colonial6/8/1896. Se distinguen actos normativos, conquista y resistencias. |
| Cuba y guerra de1898 | [Office of the Historian](https://history.state.gov/milestones/1866-1898/spanish-american-war) y [Library of Congress, cronología y prensa primaria](https://guides.loc.gov/chronicling-america-spanish-american-war). La lucha cubana desde1895 es distinta de la declaración estadounidense25/4/1898 y del protocolo12/8. La firma deParís10/12 se registra aparte de las ratificaciones posteriores. No se presentaCuba como anexionada aEstadosUnidos. |
| Filipinas1899 | [Office of the Historian](https://history.state.gov/milestones/1899-1913/war). Combates4/2, ratificación delSenado6/2 y paso a guerrilla en noviembre. El fin de cobertura no cierra la guerra; no se altera el registro1900–1902 existente. |
| Berlín1884–1885 | [Archivo Político del Ministerio de Exteriores alemán: Acta General](https://archiv.diplo.de/arc-en/the-political-archive/general-act-2684414). Conferencia15/11/1884–26/2/1885. El documento regula navegación, comercio y condiciones de reclamación; no dibuja todas las fronteras africanas. |
| Reforma china1898 | [Archivo deGuangdong, edicto original11/6](https://www.da.gd.gov.cn/portal_home/wap/archivesDetail/4040); [Museo delPalacio: reformas y calendario chino](https://www.dpm.org.cn/lemmas/241774.html); [JACAR, informes del golpe21/9](https://www.jacar.go.jp/english/exhibition/nichiro/18980921.htm). Se distingue la continuidad dinástica del cambio en el ejercicio efectivo del poder. |

Las claves modernas`ZAF`, `SDN`, `MDG`, `COD`, `ERI`, `VNM` y otras sirven como enlaces territoriales de contexto cuando no hay una entidad específica de cada actor. El texto lo aclara donde existe riesgo de confusión; no convierte a los Estados contemporáneos en participantes jurídicos de un conflicto colonial. ParaQing se usa`QNG` en eventos del mapa y`QING` en registros de identidad, siguiendo la convención existente. Las nuevas claves históricas deben integrarse también en el resolvedor y los datos de entidades antes de validar su navegación.

## Sucesiones e instituciones: Brasil, Corea yHawái

### Brasil

El [Decreto1 de15/11/1889, Cámara deDiputados](https://www2.camara.leg.br/legin/fed/decret/1824-1899/decreto-1-15-novembro-1889-532625-norma-pe.html), y la [base legislativa de laPresidencia](https://legislacao.presidencia.gov.br/atos/?ano=1889&ato=efd0TPn1UMVRVTffe&numero=1&tipo=DEC) documentan la proclamación provisional de la república federativa. Se añaden textos separados de`BRA-EMPIRE` y`BRA`, más el enlace15/11/1889 con anclas1888→1890. No se inventa un Estado geográfico nuevo ni se usa este decreto como si fuera la Constitución definitiva.

### Corea

El [Museo Nacional delPalacio, reproducido enKorea.net](https://www.korea.net/Events/Exhibitions/view?articleId=7830), y el [documento diplomático del cambio de nombre conservado enJACAR](https://www.jacar.go.jp/exhibition/nichiro/18971012.htm) fechan12/10/1897. Se enlaza`JOS`→`KEM` con anclas1896→1898, distinguiendo la proclamación deGojong de una anexión o división coreana posterior.

### Hawái

Los [Archivos Estatales deHawái, convención de1894](https://ags.hawaii.gov/archives/online-exhibitions/1894-constitutional-convention/) documentan el derrocamiento17/1/1893 y el Gobierno provisional. La [nota diplomática deHatch4/7/1894, conservada por laUniversidad deHawái](https://libweb.hawaii.edu/digicoll/annexation/blount/br1374.php), distingue la República sucesora. El [repertorio diplomático delDepartamento deEstado](https://history.state.gov/countries/hawaii) y la [fotografía catalogada por losArchivos Estatales](https://digitalarchives.hawaii.gov/item/ark:70111/1zSZ) distinguen la resolución de julio y la transferencia12/8/1898.

El grafo queda:

`HAW-KINGDOM` →17/1/1893→ `HAW-PROVISIONAL` →4/7/1894→ `HAW-REPUBLIC` →12/8/1898→ `HAW` →vínculo administrativo del mismo12/8/1898→ `USA`.

El último enlace expresa dependencia tras la misma transferencia; no inventa una segunda anexión. La administración intermedia no se llama Estado federado ni se confunde con la organización territorial por la ley orgánica posterior. Las fuentes administrativas se emplean para fechar los actos, sin convertir esas actuaciones en prueba de consentimiento general de la población hawaiana.

## Limitaciones y continuación

- Revisión focal: todavía faltan muchos conflictos internos, campañas coloniales y acuerdos regionales. Las fases anuales no afirman combate continuo ni control territorial homogéneo.
- La batalla deAdwa está documentada; la guerra ítalo-etíope completa requiere fases y fuentes adicionales. Madagascar tampoco queda convertido en una cronología exhaustiva de todas sus resistencias.
- Faltan membresías históricas completas de instituciones internacionales, la continuación documentada de otras alianzas después de1899 y sus terminaciones. No se infieren listas desde el presente.
- Las transiciones institucionales no acreditan por sí solas las fronteras, el reconocimiento simultáneo ni la continuidad de todas las estadísticas o autoridades. La cartografía y las figuras personales requieren validación independiente.
- Los servidores de algunas fuentes históricas fallan de forma intermitente. Una ampliación deberá conservar las referencias archivísticas y registrar qué imágenes originales fueron cotejadas, sin atribuir a esta investigación lecturas o descargas no realizadas.

Validación local esperada: pureza del argumento, idempotencia, conservación literal de datos previos y referencias, intervalo de cada alta, ausencia de geometrías y ausencia de solapamientos de las nuevas membresías. Las comprobaciones integradas de mapa y navegación corresponden a la raíz; este preparador no modifica los archivos públicos.
