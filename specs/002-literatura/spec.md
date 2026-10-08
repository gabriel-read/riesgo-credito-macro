# Spec 002 — Literatura
Estado: implementada · Crítica: no

## Contexto y objetivo
La sección 2 del informe (revisión de literatura) y las hipótesis de signo de las specs 003 y 004 necesitan una base bibliográfica en la que cada referencia exista y diga lo que se le atribuye. Los modelos de lenguaje inventan citas con facilidad, y la constitución (principio 5) prohíbe cualquier referencia sin DOI o URL verificada. Esta spec fija cómo se buscan, verifican y registran los estudios, y cómo se comprueba por código que ninguno es inventado.

Objetivo: (a) una matriz de literatura con al menos 16 estudios verificados que cubra las secciones 2.1–2.5 de la guía, (b) un `report/references.bib` con solo entradas verificadas, incluidas las referencias de datos y método, y (c) un script que compruebe cada DOI contra Crossref y falle si alguno no existe o no coincide.

La matriz y el `.bib` son insumos curados a mano y versionados en git, no productos del pipeline: el principio 1 de la constitución (reproducir datos, modelos, figuras y variables del informe) no los regenera. La verificación contra Crossref es una comprobación manual con red, fuera de `src.pipeline` y de `uv run pytest -q`; la coherencia entre matriz y `.bib` sí se comprueba sin red en los tests.

## Pregunta que responde (y sección de docs/guia-profesor.md que cubre)
¿Qué dice la literatura sobre la relación entre el ciclo económico, la política monetaria y el riesgo de crédito, y con qué variables y metodologías se ha estimado? Aporta la base de las secciones 2.1 (riesgo de crédito y ciclo), 2.2 (determinantes macroeconómicos), 2.3 (política monetaria y condiciones financieras), 2.4 (transmisión al riesgo de crédito) y 2.5 (evidencia empírica). La redacción de la sección 2 queda en la spec 006.

## Usuarios
- El autor, que redacta la sección 2 y fija los signos esperados de los modelos desde la matriz.
- Las specs 003, 004 y 005, que citan estudios para justificar variables, rezagos y signos.
- La spec 006 (informe), que lee `references.bib` por clave.
- El profesor evaluador, que puede abrir cualquier DOI.

## Historias de usuario
- HU-1. Como autor, quiero una matriz con variables, método y hallazgo de cada estudio para escribir 2.5 y justificar los signos esperados sin releer los artículos.
- HU-2. Como autor, quiero que una referencia no verificada no pueda entrar en el `.bib` para no arriesgar una cita inventada en el informe.
- HU-3. Como autor, quiero un script que me diga qué DOI no existe o no coincide para corregirlo antes de entregar.
- HU-4. Como profesor, quiero que cada estudio traiga un enlace de verificación para comprobar que existe.

## Definiciones
- **Estudio**: artículo de revista, capítulo de libro o documento de trabajo con autoría identificable que se incluye en la matriz como literatura (sección 2.1–2.5). No incluye las referencias de datos y método.
- **Referencia de datos y método**: FRED (las series usadas), los escenarios de estrés 2026 de la Reserva Federal, Newey y West (1987) y Jordà (2005). Van en el `.bib` y en la matriz con Tipo = «datos/método», sin sección de la guía, y **no cuentan** para el mínimo de 16 estudios.
- **Sección principal**: la única sección (2.1–2.5) a la que se asigna un estudio para los conteos mínimos. Es aquella cuya pregunta responde el hallazgo o aporte principal del estudio; si el estudio estima coeficientes de variables macroeconómicas o de política monetaria sobre una medida de riesgo de crédito, su sección principal es 2.5. Un estudio puede listar secciones secundarias, pero cuenta una sola vez, y su sección principal no se reasigna para cuadrar los mínimos.
- **Estudio empírico (2.5)**: estudio que estima una relación entre variables macroeconómicas o de política monetaria y una medida de riesgo de crédito (morosidad, provisiones, impagos o similar), con datos, variables y método descritos en la matriz.
- **Verificado**: el DOI existe en Crossref y su registro coincide con la matriz en título, primer autor y año (ver «Coincidencia»), y el resumen o un fragmento leído respalda el hallazgo o aporte atribuido. Los documentos sin DOI (Fed, Comité de Basilea, FRED, capítulos sin DOI propio) se verifican con una URL oficial que responde y se leen igualmente.
- **Coincidencia**: el título normalizado (minúsculas, sin puntuación ni tildes) del registro de Crossref contiene al del `.bib` o viceversa; el apellido del primer autor coincide, ignorando tildes, mayúsculas y espacios; y el año coincide con el de publicación en línea o impresa del registro.
- **Pendiente-lectura**: el DOI existe pero no se ha leído el resumen de la versión citada; no puede entrar en el `.bib` ni contar para los mínimos.
- **No aplica**: texto literal que se escribe en una celda de la matriz cuya columna no tiene sentido para esa fila (por ejemplo, el país de un estudio teórico o el signo de Newey y West). Una celda vacía es un error.
- **Lista semilla**: Bernanke y Gertler (1995); Bernanke, Gertler y Gilchrist (1999); Wilson (1997); Salas y Saurina (2002); Jiménez y Saurina (2006); Virolainen (2004); Nkusu (2011); Louzis, Vouldis y Metaxas (2012); Beck, Jakubik y Piloiu (2015); Ghosh (2015); Borio y Zhu (2012); Maddaloni y Peydró (2011); Jiménez, Ongena, Peydró y Saurina (2014); Wu y Xia (2016); Comité de Supervisión Bancaria de Basilea (2018), «Stress testing principles». Son candidatos como cualquier otro: ninguno entra sin verificarse, y ninguno se da por existente por estar en la lista.
- **Series de FRED usadas**: las 13 de la spec 001 (RF-1): DRALACBS, DRALACBN, DRCLACBS, DRBLACBS, DRSREACBS, GDPC1, GDP, UNRATE, CPIAUCSL, FEDFUNDS, LOANS, CORALACBS y USREC. Si la spec 001 cambia esta lista por `/sdd-change`, el mismo cambio actualiza esta definición.
- **Error de red o de servicio**: timeout, fallo de conexión, respuesta HTTP 429 o 5xx, o respuesta de Crossref sin un único registro bien formado. Un HTTP 404 no es error de servicio: significa «no existe».

## Requisitos funcionales

### Búsqueda y verificación
- RF-1: EL SISTEMA buscará y confirmará cada candidato en fuentes abiertas (Crossref y OpenAlex) y no aceptará ninguno solo por provenir de la memoria del modelo o de la lista semilla.
- RF-2: SI un candidato de la lista semilla no se puede verificar (DOI inexistente, registro que no coincide o resumen que no respalda el hallazgo), ENTONCES la matriz lo registrará con Estado = «descartado» y el motivo, y no entrará en el `.bib`. Si con ello su sección queda por debajo del mínimo de RF-6, se añadirá otro candidato verificado de esa sección. Los mínimos se cuentan sobre el resultado final.
- RF-3: La matriz no contendrá ningún hallazgo o aporte que no esté en el resumen o en un fragmento leído de la versión citada. Si el hallazgo que se pensaba atribuir no aparece en lo leído, el bibliotecario lo sustituye por lo que sí dice la fuente; si no se ha leído, la fila queda en «pendiente-lectura». El subagente `verificador-citas` lo comprueba al cierre.
- RF-21: CUANDO exista una versión publicada y otra de documento de trabajo o preprint del mismo estudio, la matriz y el `.bib` citarán solo la publicada, con su DOI o, si no lo tiene, su URL oficial. El hallazgo debe estar en el resumen de la versión publicada; si solo se leyó el preprint, la fila queda en «pendiente-lectura».

### Matriz de literatura
- RF-4: EL SISTEMA producirá `research/matriz-literatura.md` con una fila por estudio o referencia y estas columnas: Clave · Autor(es) y año · País · Frecuencia · Período · Variable dependiente · Regresores · Variables de la guía · Método · Hallazgo o aporte (una línea) · Sección principal (2.1–2.5) · Secciones secundarias · Respalda · Tipo (estudio o datos/método) · Estado (verificado, pendiente-lectura o descartado) · URL de verificación. Ninguna celda queda vacía: lo que no tenga sentido para la fila lleva «no aplica».
- RF-5: EL SISTEMA incluirá en la matriz al menos 20 filas con Estado = «verificado»: al menos 16 estudios y exactamente las 4 referencias de datos y método de RF-7.
- RF-6: EL SISTEMA asignará al menos 2 estudios verificados como sección principal a cada una de las secciones 2.1, 2.2, 2.3 y 2.4, y al menos 6 estudios empíricos verificados a la sección 2.5.
- RF-22: En los estudios con sección principal 2.5, las columnas País, Frecuencia, Período, Variable dependiente, Regresores, Variables de la guía y Método serán obligatorias (no admiten «no aplica»), y el Hallazgo indicará el signo de la asociación principal (positivo, negativo o no significativo). En las secciones 2.1–2.4 y en datos/método, esas columnas pueden llevar «no aplica» y la columna Hallazgo o aporte describe el aporte en una línea, sin signo obligatorio.
- RF-23: La columna «Variables de la guía» tomará uno o varios valores, separados por comas, de esta lista cerrada: `pib`, `desempleo`, `inflacion`, `tasa_politica`, `credito`, `otra`; o «no aplica» fuera de 2.5.
- RF-24: La columna «Respalda» tomará uno o varios valores, separados por comas, de esta lista cerrada: `I`, `II`, `estres`, `ninguno`. Indica a qué modelo o ejercicio aporta el estudio, no qué signo esperar: los signos se pre-registran en las specs 003 y 004.
- RF-7: EL SISTEMA incluirá en la matriz, con Tipo = «datos/método» y Estado = «verificado», las cuatro referencias de datos y método: FRED, una sola referencia institucional que nombra las series de FRED usadas (ver Definiciones) y su fecha de consulta; Board of Governors of the Federal Reserve System (2026), «2026 Stress Test Scenarios», con su URL oficial; Newey y West (1987); y Jordà (2005).
- RF-8: CUANDO la matriz registre el método de un estudio, EL SISTEMA lo describirá en términos que permitan agruparlo (por ejemplo, datos de panel con efectos fijos, MCO con errores HAC, VAR, GMM, proyecciones locales, logit/probit a nivel de crédito) para que la sección 2.5 pueda comparar metodologías.
- RF-20: EL SISTEMA incluirá en `research/matriz-literatura.md`, antes de la matriz, una tabla Markdown titulada «Resumen» con la fecha de verificación y el número de filas verificadas por sección principal (2.1, 2.2, 2.3, 2.4 y 2.5) y de datos/método. Existirá un test sin red que recalcule esos conteos desde la matriz y falle si no coinciden.

### Archivo BibTeX
- RF-9: EL SISTEMA producirá `report/references.bib` con exactamente una entrada por cada fila de la matriz con Estado = «verificado» (estudios y referencias de datos y método), y con ninguna por filas «pendiente-lectura» o «descartado».
- RF-10: EL SISTEMA usará como clave de cada entrada `apellidoaño` en minúsculas, sin tildes, ñ, espacios ni guiones; los apellidos con partícula se escriben completos y unidos (`delafuente2020`, `vanderwaals2020`); los autores institucionales usan su sigla (`bcbs2018`, `frb2026`, `fred2026`). Si dos entradas coincidieran, se desambigua con una letra final (`jimenez2014a`). La clave de la matriz y la del `.bib` serán la misma.
- RF-11: EL SISTEMA incluirá el campo `doi` en toda entrada que tenga DOI y, en las que no lo tengan, el campo `url` oficial. En concreto, Newey y West (1987) y Jordà (2005) llevan `doi`; FRED, Fed 2026 y BCBS 2018 llevan `url`. Un capítulo de libro sin DOI propio se trata como entrada sin DOI, con la `url` oficial del capítulo; nunca lleva el DOI del libro.
- RF-12: Existirá un test sin red que falle si una entrada del `.bib` no tiene fila verificada en la matriz o si una fila verificada no tiene entrada en el `.bib`.
- RF-25: Existirá un test sin red que exija los campos mínimos de cada entrada del `.bib` según su tipo: `article` con author, title, journal, year; `incollection` con author, title, booktitle, year; y para autores institucionales, author entre dobles llaves (`{{…}}`) y `url`. El render APA con Quarto queda en la spec 006.

### Script de verificación
- RF-13: EL SISTEMA incluirá un script que, para cada entrada de `report/references.bib` con campo `doi`, consulte Crossref y compare título, primer autor y año según «Coincidencia». El DOI se normaliza antes de consultar (minúsculas, sin prefijo `https://doi.org/`).
- RF-14: SI un DOI no existe en Crossref (HTTP 404), ENTONCES EL SISTEMA lo informará como «no existe» con la clave y terminará con código de salida distinto de cero.
- RF-15: SI el registro de Crossref no coincide con la entrada en título, primer autor o año, ENTONCES EL SISTEMA informará la clave y qué campo difiere, con ambos valores, y terminará con código de salida distinto de cero.
- RF-16: SI una entrada no tiene `doi`, ENTONCES EL SISTEMA exigirá un `url` y comprobará que responde con éxito; si falta el `url` o no responde, informará la clave y terminará con código distinto de cero.
- RF-17: SI ocurre un error de red o de servicio (ver Definiciones), ENTONCES EL SISTEMA reintentará hasta 3 veces con esperas de 1, 2 y 4 segundos y un timeout de 10 segundos por consulta; si sigue fallando, informará la entrada como «no verificable», distinguida de «no existe», y terminará con código distinto de cero. Nunca dará por verificada una entrada que no pudo consultar.
- RF-18: CUANDO todas las entradas pasen, EL SISTEMA imprimirá el número de entradas verificadas y terminará con código de salida cero.
- RF-19: EL SISTEMA no modificará `report/references.bib` ni la matriz: solo lee y reporta.
- RF-26: Existirán tests sin red del script, con respuestas simuladas inyectadas en lugar del cliente HTTP, que cubran al menos: DOI correcto, DOI inexistente (404), título distinto, primer autor distinto, año distinto, error de servicio persistente («no verificable»), entrada sin `doi` con `url` que responde y entrada sin `doi` ni `url`. El script tiene un único modo de ejecución; la verificación contra Crossref real es una ejecución manual.

## Requisitos no funcionales
- RNF-1 (sin red en tests): MIENTRAS corran los tests, EL SISTEMA bloqueará cualquier acceso a la red; los tests usan respuestas simuladas (RF-26). La verificación contra Crossref real queda fuera de `uv run pytest -q`.
- RNF-2 (principio 5): EL SISTEMA no contendrá ninguna referencia, DOI ni cifra de un estudio escrita de memoria: todo dato bibliográfico y todo hallazgo procede de un registro o fragmento consultado.
- RNF-3 (idioma): código e identificadores en inglés; matriz, mensajes del script y documentación en español; citas en estilo APA 7.
- RNF-4 (independencia de la auditoría): el verificador independiente (`verificador-citas`) recibe solo las rutas de `report/references.bib` y de la matriz, no la conclusión del autor.
- RNF-5 (sin dependencias nuevas sin permiso): el script usará solo lo ya instalado en el proyecto o la biblioteca estándar; cualquier dependencia nueva se consulta antes.
- RNF-6 (principio 3): leer y analizar el `.bib` y la matriz, normalizar DOI, títulos y apellidos, y comparar un registro de Crossref con una entrada serán funciones puras, sin red ni disco; el script solo hace la entrada y salida (leer archivos, consultar la red, imprimir y fijar el código de salida). La ubicación y las firmas las fija el plan.

## Casos límite
- Un candidato semilla (por ejemplo Wilson, 1997, publicado en una revista profesional) no tiene DOI en Crossref: se busca una URL oficial verificable; si no existe, se descarta con motivo (RF-2).
- DOI con mayúsculas y minúsculas mezcladas o con prefijo `https://doi.org/`: el script lo normaliza antes de consultar (RF-13).
- Crossref registra el año de publicación en línea distinto del año de la edición impresa: coincide si el año del `.bib` iguala cualquiera de los dos.
- Capítulo de libro (por ejemplo Bernanke, Gertler y Gilchrist, 1999): el título que se compara es el del capítulo, no el del libro. Si el capítulo no tiene DOI propio, se verifica por URL (RF-11).
- Autor corporativo (Comité de Basilea, Reserva Federal, FRED): sin primer autor personal ni DOI; se verifica por URL y se escribe entre dobles llaves (RF-25).
- Autores con apellidos compuestos, con tilde o con partícula (Jiménez, Peydró, de la Fuente): la comparación ignora tildes, mayúsculas y espacios, y la clave une el apellido completo (RF-10).
- Un estudio relevante para varias secciones: cuenta una sola vez, en su sección principal según la regla de Definiciones.
- Dos estudios del mismo autor y año: claves desambiguadas con letra (RF-10).
- Una versión de documento de trabajo y otra publicada del mismo estudio: se cita solo la publicada (RF-21).
- Crossref devuelve una respuesta sin un único registro bien formado: «no verificable» (RF-17).
- Crossref caído: tras los reintentos, la entrada queda «no verificable» y la spec no se cierra (RF-17).
- Un descartado de la lista semilla deja su sección por debajo del mínimo: se añade otro candidato verificado de esa sección (RF-2).

## Fuera de alcance
- Redactar la sección 2 del informe (spec 006).
- Citar en el texto, dar formato APA a la lista final (lo hace Quarto con `apa.csl` en la spec 006) y revisar la narrativa.
- Elegir variables, rezagos o signos de los modelos (specs 003 y 004); esta spec solo aporta el material. La columna «Respalda» no fija signos.
- Integrar la matriz, el `.bib` o la verificación contra Crossref en `src.pipeline`.
- Revisión exhaustiva o sistemática de la literatura: el objetivo es un mínimo verificado, no un mapeo completo.
- Verificar los números de páginas, volúmenes y ediciones más allá de lo que Crossref devuelva.
- Descargar o almacenar los textos completos de los artículos.

## Criterios de finalización
- La matriz tiene al menos 20 filas verificadas: al menos 16 estudios, con los mínimos por sección de RF-6, y las cuatro referencias de datos y método (RF-5 a RF-7), sin celdas vacías y con la tabla «Resumen» (RF-20, RF-22 a RF-24).
- `report/references.bib` contiene solo las entradas verificadas de la matriz, con las mismas claves y los campos mínimos (RF-9 a RF-12, RF-25).
- `uv run python scripts/verify_refs.py` termina con código cero contra Crossref real (RF-18), ejecutado y anotado en `specs/002-literatura/review-validate.md`.
- Los tests del script (RF-26) y de coherencia matriz–`.bib` (RF-12, RF-20, RF-25) pasan sin red; `uv run pytest -q` en verde.
- El subagente `verificador-citas` revisó `references.bib` y la matriz y no halló referencias inexistentes ni hallazgos no respaldados.
- `specs/002-literatura/review-validate.md` con `VEREDICTO: APROBADO`.

## Desviaciones del pre-registro
No aplica (spec sin modelo).

## Dudas abiertas
(ninguna)
