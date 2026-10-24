# Entrega0.12.0 · ampliación hasta1900

Encargo24/10/2026: ampliar1900–1919 manteniendo1920–actualidad. Preparada en `codex/1900-history` desde `d7f683c`. La instrucción vigente exige comprobar localmente, subir y terminar sin esperar ni sondear Actions/Pages; subida y despliegue son estados distintos.

## Datos y aplicación

302 claves,10.244 mandatos y5.262 medios(499SVG/4.763 fotografías). Incremento neto378 fotografías y21SVG;76 ventanas de símbolos1900–1919 y una deEslovaquia1939. Adquisición aislada y cinco curadores conservan las afirmaciones previas que alcanzan1920 y todas las imágenes ya acreditadas. No cambia la referencia contemporánea22/10/2026. CatálogoPaíses sincronizado:2.792 carpetas.

Imperios y monarquías tienen claves separadas de sucesores. Corea, antiguas repúblicas bóeres, Congo, Marruecos, Tonga y Afganistán distinguen gobernantes locales y administración externa.32 relaciones administrativas/26 contornos contemporáneos de referencia. Los archivos geométricos originales y sus licencias permanecen intactos; no se añaden frentes diarios ficticios.

41 agrupaciones/903 intervalos,378 fases,97 registros de ficha/86 enlaces. TripleAlianza, coaliciones de guerra y nuevas instituciones no convierten automáticamente a los miembros en dependencias o beligerantes. Fechas de proclamación, firma, vigencia y reconocimiento diferenciadas.

Auditoría:3.167 entidades/año y15 controles/año; sin vacíos de resolución de alguna autoridad o fragmentación institucional documentada. Quedan63 personas y3órganos sin retrato,165 casos anuales sin símbolo. Listas en REVIEW-1900-1919.json y detalles en tareas.md. No es una certificación mundial de todos los cargos, regencias, gobernadores y fronteras.

## Validación local

- 137 pruebas unitarias/31 archivos correctos; tipos correctos.
- Integridad SHA-256 de44 recursos de datos,11 franjas tipográficas y5.262 medios correcta.
- Cinco curadores1900 puros e idempotentes, con conservación literal de las afirmaciones1920+ previas, salvo añadir referencias a retratos acreditados.
- Compilación de producción correcta en `.cache/build-012-final-map`, carpeta nueva porque Windows bloqueó el vaciado de `dist/media`. No se alteró código ni CI para ocultar ese bloqueo local. Se mantiene el aviso conocido de tamaño del paquete principal, sin reducir detalle geográfico. Las pruebas posteriores sirven exclusivamente esta compilación; no usar el `dist` incompleto sin regenerarlo.
- Cinco recorridos focales iniciales correctos(5,2min):1900–1919,1920–1949, capas actuales y dos recorridos políticos, incluidos móvil y clic real. Cuatro recorridos tras la corrección central correctos(3,9min). Tras el ajuste final deMoravia,1920–1949 pasa de nuevo(1,3min) y el nuevo1939 pasa(45,8s), con navegación de fechas, franjas y clic real. La primera ejecución final de1939 agotó los5s predeterminados de la espera de cámara; ahora espera el estado real de cámara quieta hasta30s, manteniendo renderizado, clic y ausencia de errores. No hay reintentos ni pruebas omitidas.
- Revisión visual deAlemania1919 en móvil y del mapa central1939. Bytes preparados enGit de5.317 recursos de datos/letras/medios verificados. Topología, controles originales, instantáneas originales y flujos deCI sin cambios.

La primera suite detectó dos problemas corregidos: claves monárquicas serbia/montenegrina aplicadas fuera de su época y una expectativa de sucesores que no contemplaba el nuevo predecesor checoslovaco. Se añadieron comprobaciones positivas. La regresión deCorea1910 comprueba símbolo de administrador continuo durante el cambio de protectorado a colonia. Las guardas de renderizado, actualización incremental y selección por estado de pintura se conservan.

## Corrección adicional solicitada de1939

Después de terminar la integración1900, el propietario comunica manchas alemanas y apariencia de parche enChecoslovaquia. Se confirma contaminación en el originalCliopatria, no sólo un fallo del navegador. `central-europe.ts` limita la corrección a1938–1939, sin filtro global por tamaño ni mutar geometrías originales. Países vecinos protegidos, Alemania como entidad única yEslovaquia1939 como cliente separado. Las fases y límites, incluida la referencia geométrica eslovaca y la franja oriental todavía pendiente de detalle, se explican en CENTRAL-EUROPE-1939. Los puntos negativos y positivos, islas reales, ocupación frente a incorporación, identificadores y selección se comprueban automáticamente.

## Continuidad

Entrega local validada y preparada para la subida autorizada a main. Pendientes de investigación nominales y regionales en tareas.md; conservar el CSV ausente y los pendientes anteriores. No repetir la adquisición destructiva ni declarar completos cargos o frentes por pasar una auditoría de resolución. No se han consultado ejecuciones de despliegue ni comprobado bytes públicos de esta versión. El siguiente paso operativo, tras confirmar el push, es el aviso del propietario.
