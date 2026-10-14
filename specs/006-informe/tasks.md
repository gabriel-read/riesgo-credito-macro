# Tareas — Spec 006 Informe

**Estado vigente:** validación técnica del autor ronda 7 en review-validate-ronda7.md y paquete nuevo docs/paquete-auditoria-006-ronda7.md. T12 y 006 pendientes; notas anteriores históricas.
Estado: aprobada v3; change editorial y T13-T15 autorizados por el autor el 12-oct-2026. T1-T4 completas conservadas; avance editorial autorizado con cierre global pendiente de la suite completa.

**Actualización histórica, Codex, 12-oct:** H1/H2 autorizadas y resueltas; catálogo contrastado, siete negativos primero y suite completa **905 passed, 567 warnings, 963,43 s, rc0**, sin exclusiones. T5–T11 y T13–T15 marcadas por implementación/redacción y validación técnica aprobada en `review-validate.md`; no se cambian sus contratos ni autores. Clics reales: 53 destinos internos del informe, 160 del anexo y 23 URI únicos. Render repetido con contenido idéntico; solo metadatos temporales de PDF/DOCX difieren. Las notas posteriores sobre H2 pendiente o suite parcial describen antecedentes y quedan superadas por esta evidencia.

**Cierre global abierto:** el autor retiró Google Docs como requisito de cierre el 2026-10-13; no se afirma que sus enlaces funcionen. T12 puede recibir el paquete tras T11 aprobada, pero 006 no se cierra sin auditoría y esa revisión. Contrato vigente: spec v4/plan v3 del change aplicado; referencias v3/v2 de abajo son históricas. Sin nuevos commits ni push.

**Evidencia histórica ronda 3, Codex, 13-oct-2026:** T11 revalidada tras las correcciones C1–C10, portada y 07 estable. Suite completa 940 passed/567 warnings/1198,52s/rc0, sin exclusiones; review-validate-ronda3.md e índice entonces vigentes. Principal34p/anexo152p; ocho tablas/117 paneles; 53+167 destinos internos y52URI comprobados. Report206 archivos idénticos y render con solo metadatos temporales diferentes. 116 fuentes protegidas intactas. T12 y006 siguen abiertas; auditoría ronda2 yGoogleDocs pendientes. Esta nota actualiza evidencia, no los contratos ni la autoría de tareas anteriores.

Contrato: spec v3 aprobada (sha256 `caf97028a2b236404cc00bbe2fe40253f2d48ecd58fc686417091ca3bf3ad3df`) y plan v2 aprobado (sha256 `61262159fecad4d396db4d3d7043d86db0e9ea1d843c65655d5e9eafa8802f17`) el 12-oct-2026; ambos originales no se editan. Ajustes del plan §8 autorizados por el autor el 12-oct dentro de este alcance: alinear la skill `informe-quarto` sin relajar sus guardarraíles, extender los tests de cifras y citas a `report/secciones/**`, gancho `pre-render` que sincroniza variables mediante `uv` (sin llamadas recursivas a Quarto) e ignorar en git el `_variables.yml` generado de la raíz; `report/_variables.yml` es la única fuente de verdad. El humo mínimo del 12-oct (`docs/render-humo-006-2026-10-12.md`) ya se hizo; no sustituye a T1.

Reglas: una tarea por vez dentro de cada carril; tests primero para código; `uv run pytest -q` antes de marcar una tarea de código; una sola herramienta escribe en el checkout a la vez (entrega explícita de turno) y cada archivo tiene un solo escritor (tabla de propiedad al final). Ninguna cifra, cita ni umbral se inventa. No se modifican las salidas aprobadas de 001–005 ni `data/raw/`; ninguna dependencia nueva sin preguntar. Cambios del contrato requieren `change`. Claude Code redacta solo tras la **puerta G1**. La auditoría de la 006 no es independiente de lo que Claude redacta (T12).

## Primera entrega técnica (antes de redactar)

Delimitación de escritura de T1–T4: T1 modifica exclusivamente `_quarto.yml`, `.gitignore`, `.claude/skills/informe-quarto/SKILL.md` (línea autorizada), `src/report_vars.py`, `src/pipeline.py`, `tests/test_harness.py`, `tests/test_pipeline.py` y el nuevo `tests/test_report.py`. T2 añade `src/report_tables.py`, `tests/test_report_tables.py` y su integración en `src/pipeline.py`/`tests/test_pipeline.py`; genera `outputs/informe/*.md` y `report/anexos/tablas.qmd`. T3 añade el generador de interfaz en `src/report_vars.py`, sus tests en `tests/test_report.py` y las inclusiones en `report/informe.qmd`; cada herramienta crea exclusivamente los encabezados de sus secciones, mediante turnos separados. T4 modifica `src/report_vars.py`, `src/report_tables.py`, `src/pipeline.py`, sus tests y exclusivamente la entrada `fred2026` de `report/references.bib`. Los productos generados son `report/_variables.yml`, su espejo raíz, `specs/006-informe/interfaz.md`, `outputs/informe/`, `outputs/tables/lit_estudios.csv` y `lit_estudios.md`. No hay autorización general para modificar otros archivos de `src/`, `tests/` u `outputs/`.

La evidencia de esta entrega se registrará en `docs/validacion-maquetacion-006.md`, `docs/validacion-maquetacion-006.json` y renders/previsualizaciones bajo `outputs/smoke-006/`. Registra rutas, herramientas, huellas de fuentes y productos, páginas revisadas, problemas y siguiente acción. Las tablas, CSV y figuras aprobadas de 003–005 conservan sus bytes, y los bloques `modelo1`, `modelo2` y `estres` conservan sus valores. T4 concilia `datos.n_series` contando los códigos efectivamente congelados y usados, sin presuponer 13: si 12 es correcto se corrige la enumeración de `fred2026`, no la variable. No se introduce una clave alternativa para eludir RF-15. Si su conciliación requiere modificar una salida histórica protegida, se registra el conflicto y se detiene esa corrección para `change`.

T1 también delimita `report/apa.csl` y el espejo generado `_variables.yml`. Los guardarraíles recorren `report/secciones/**` y `report/anexos/**`, sin tratar los números de tablas generadas como cifras tecleadas en prosa. Los archivos de humo se conservan como evidencia local; no se decide su inclusión en un commit durante esta sesión.

- [x] **T1. Proyecto Quarto definitivo y sincronización de variables.** RF-14, RF-15; RNF-2, RNF-4 · agente: codex
  - Tests: `sync` (función pura de validación + E/S mínima en `stage_report`) copia byte a byte `report/_variables.yml` a `_variables.yml` de la raíz, relee y compara sha256, falla ante una copia alterada o una fuente vacía, es idempotente (dos corridas, mismas huellas); `test_root_variables_in_sync`; `_variables.yml` de la raíz ignorado por git; `stage_report` incluido en `all`.
  - Hecho cuando: `_quarto.yml` en la raíz (`project.render: [report/informe.qmd]`, `bibliography`, `csl: report/apa.csl`, `lang: es`, `format.typst.citeproc: true`, docx), `report/apa.csl` con sha256 `3917def5…889fc` registrado, gancho `project.pre-render` que ejecuta `uv run python -m src.pipeline report` sin invocar Quarto de forma recursiva; si el gancho no funciona en este entorno, se documenta el orden alternativo y se avisa. Se usa `C:/Program Files/Quarto/bin/quarto.exe` donde falte el PATH. Skill `informe-quarto` alineada solo en la línea del proyecto Quarto, con todos sus guardarraíles. Los tests de cifras a mano y de citas recorren `report/secciones/**/*.qmd` con negativos (una cifra escrita a mano, una clave inexistente, una de «pendiente-lectura» o «descartado»). Suite completa en verde.
  - Evidencia Codex, 12-oct: 18 fallos/2 aciertos primero; 31 focalizados verdes; `uv run pytest -q`: 857 passed, 567 warnings, 944,11 s, rc 0. Gancho ejecutado en PDF/Word; espejo byte a byte, Git ignora solo raíz; 97 archivos protegidos intactos. `docs/validacion-maquetacion-006.md/json`. La paginación visual completa corresponde a T2, no a este humo.

- [x] **T2. Tablas de presentación y anexos legibles.** RF-3; RNF-1, RNF-2 · agente: codex
  - Tests: cada cifra de una tabla de presentación coincide con su CSV aprobado de origen; no aparece ninguna cifra nueva; etiquetas en español; sin `|` sin escapar; sin celdas de más; filas y columnas esperadas por tabla.
  - Hecho cuando: generador puro en `src/report_tables.py` y salidas en `outputs/informe/` para las tablas que entran al texto de 3, 4, 5, 6 y 7, con columnas seleccionadas y etiquetas cortas; los anexos generados conservan todas las filas y columnas de cada CSV utilizado, incluidos los textos largos, y se incluyen desde el informe. Una matriz CSV → tabla de presentación → anexo identifica fuentes, columnas, filas y reglas de formato; los tests comprueban cobertura completa y valores tras el redondeo declarado. Render de prueba de PDF y Word con revisión visual de todas las tablas y páginas de anexos: sin texto cortado, columnas omitidas, solapamientos ni filas perdidas; cabeceras reconocibles al continuar páginas. En Word se comprueba también la paginación visible, no solo su XML. Los enlaces a originales no sustituyen a los anexos completos. No se editan las tablas de 003, 004 ni 005. Si hacen falta páginas apaisadas o cambios de formato, se comunica antes de aplicarlos; no se instala ninguna herramienta o dependencia nueva sin autorización.
  - Evidencia Codex, 12-oct: siete rojos primero y regresión CRLF roja/verde; 40 focalizados verdes; suite completa 864 passed, 567 warnings, 1136,34 s, rc 0. PDF 115 páginas inspeccionadas, DOCX 107 tablas/2758 filas/107 cabeceras repetibles, cero discrepancias de celdas. Fuentes/salidas aprobadas intactas. Excepción operativa del autor por falta de licencia Office, transmitida en la sesión de Claude: revisión visual manual del DOCX en Google Docs durante G1; no se afirma paginación nativa de Word comprobada. Procedencia y límites: `docs/validacion-maquetacion-006.md/json`.

- [x] **T3. Esqueleto del informe e interfaz.** RF-1, RF-2, RF-6; RNF-6 · agente: codex (generador/integración) y claude (solo encabezados de sus archivos, en turno separado)
  - Tests: las 11 secciones y las subsecciones 2.1–2.5, 3.1–3.5 y 6.1–6.4 existen con los títulos y la numeración de la guía, en orden; cada sección tiene su archivo en `report/secciones/` incluido desde `report/informe.qmd`; `informe.qmd` no contiene prosa.
  - Hecho cuando: `report/informe.qmd` con el título propuesto de la guía y los `include` en orden; cada escritor crea los encabezados y el marcador `[pendiente]` de sus propios archivos durante un turno exclusivo, sin prosa. **`specs/006-informe/interfaz.md`**, generada desde las fuentes actuales, enumera todas las claves de `report/_variables.yml`, tablas originales/de presentación/anexos y figuras disponibles, con rutas, descripción, unidades cuando consten en la fuente, spec de origen y huellas. Se señalan las cifras de hallazgos heredados disponibles y las ausentes para T4. Un test detecta claves o archivos ausentes y rutas que no resuelven desde el proyecto raíz; T4 actualiza el inventario antes de G1.
  - Evidencia, 12-oct: Codex creó siete archivos y Claude nueve, únicamente encabezados y marcadores, con cesiones exclusivas verificadas. Interfaz generada: 871 entradas/219 activos, nueve figuras y mapa de claves heredadas/pendientes. Cinco tests rojos iniciales y regresiones de numeración/mapa rojas antes de corregir; 46 focalizados y suite final 872 passed, 567 warnings, 927,38 s, rc 0. Una suite anterior se detuvo antes de concluir para verificar el mapa final, sin presentarla como aprobación. PDF/Word del esqueleto generan, 3.5 no se duplica, sin prosa central. Evidencia en `docs/validacion-maquetacion-006.md/json`. Solicitud de Claude sigue antes de T4.

- [x] **T4. Variables y tabla de literatura nuevas.** RF-4, RF-15; RNF-1, RNF-2 · agente: codex
  - Tests: `datos.n_series` único y coherente con la nota de datos y la referencia; conteos de literatura generados desde `research/matriz-literatura.md` (solo filas «verificado»); tabla 2.5 (`lit_estudios.{csv,md}`: estudio, variables, metodología, signo); la URL de `fred2026` verificada; `scripts/verify_refs.py` termina con código 0 (requiere red); dos corridas de `report`, mismas huellas.
  - Hecho cuando: las claves y tablas que Claude pida en `solicitudes-claude.md` para los hallazgos heredados (solo desde claves o salidas existentes) están en `report/_variables.yml`/`outputs/` e `interfaz.md` actualizada. Nada se calcula nuevo ni se escribe a mano; si algo exige un cambio de una spec cerrada, se presenta `change` y no se hace aquí.
  - Evidencia Codex, 12-oct: negativos y regresiones primero; suite 877 passed, 567 warnings, 1016,73 s, rc 0; 58 focalizados tras URLs, rc 0. Autor autorizó exclusivamente la celda URL de `fred2026` en la matriz adicional al BibTeX; sustitución inversa verifica todos los demás bytes intactos. `verify_refs.py`: 21/21, rc 0. `report` ×2: 150 productos idénticos; 99 protegidos intactos y bloques modelos/estrés idénticos. 34 CSV, PDF 122 páginas, DOCX 109 tablas/2800 filas sin discrepancias y cuaderno de nueve figuras. Google Docs manual durante G1, sin afirmar inspección nativa Word. Respuesta de fuentes y pendientes únicos en `docs/validacion-maquetacion-006.md/json` y `solicitudes-codex.md`. G1 sigue pendiente; no habilita redacción.

## Puerta G1 (autor)
Tras T1–T4 se presenta la primera entrega: **PDF y Word con maquetación real, todas las tablas, figuras y anexos completos**, `interfaz.md` actualizada y evidencia de correspondencia con las fuentes. El autor revisa G1 antes de la redacción de T5–T10. No se da por resuelta la legibilidad solo porque el render termina con código 0. Si T2 o T1 revelan que algo cambia el formato, se avisa al autor antes de seguir.

En T3 se usa un comentario HTML `<!-- PENDIENTE -->` para los espacios sin redactar. El encabezado 3.5 aparece exclusivamente en `03e-desviaciones.qmd`; `03f-limitaciones.qmd` contiene su continuación, sin duplicarlo. Entre T3 y T4 Claude recibe un turno exclusivo, solo para `solicitudes-claude.md`, donde lista las claves faltantes que identifica contra la interfaz; luego devuelve la escritura a Codex.

## Carril Claude Code: redacción (después de G1; cada tarea escribe solo sus archivos)

- [x] **T5. Secciones 1, 2 y limitaciones de 3.5.** RF-1, RF-4, RF-6, RF-7; RNF-1, RNF-3 · agente: claude
  - Tests: los de T1 y T3 sobre estas secciones (cifras por `var`, citas válidas, lenguaje, estructura).
  - Hecho cuando: `01-introduccion.qmd` (pregunta y objetivo de la guía, respuesta en una frase), `02-literatura.qmd` (2.1–2.5; solo filas «verificado»; justifica `bernanke1995`, la clasificación de `pesaran2006`, `segoviano2006` y `gertler2015`; no cita con hallazgo `asiamah2026` ni `koskei2023`; incluye la tabla de 2.5 de T4) y `03f-limitaciones.qmd` (limitaciones de 3.5 sin atenuar los diagnósticos fallidos).

- [x] **T6. Secciones 4 y 5 (Modelos I y II).** RF-5, RF-5b, RF-6; RNF-3, RNF-6 · agente: claude
  - Tests: los de T1 y T3.
  - Hecho cuando: `04-modelo1.qmd` y `05-modelo2.qmd` responden las preguntas de la guía como asociación condicional, en pp, con significancia y diagnósticos; tratan los hallazgos heredados de 003 y 004 de la spec (π y CRED no I(0) con ADF/KPSS ambiguos, efecto de impacto frente a largo plazo, CUSUM frente a Chow, signo de ΔFFR, dummies, Granger≡C2 con K = 1, «sin evidencia» frente a RESET y Chow, φ_h, endogeneidad, ΔFFR no es un shock identificado) y rotulan `columna_panel`; cada tratamiento queda trazado a su sección.

- [x] **T7. Sección 6 (análisis de resultados).** RF-5, RF-8, RF-9; RNF-3, RNF-6 · agente: claude
  - Tests: los de T1 y T3.
  - Hecho cuando: `06-resultados.qmd` con 6.1–6.4: integra los dos modelos con `model2_inputs63` sin ponderar ni elegir, responde la pregunta fundamental sin el formato prohibido, distingue asociación y causalidad y permite responder las preguntas probables del profesor (a)–(e) de la spec.

- [x] **T8. Sección 7 (escenarios y estrés).** RF-12; RNF-3, RNF-6 · agente: claude
  - Precondición verificable antes de escribir: `specs/005-estres/review-audit.md` con `VEREDICTO: APROBADO` sobre las huellas auditadas y `review-validate.md` y T10 de la 005 completos; si no se cumple, el archivo queda con el marcador «pendiente de resultados de la spec 005» y se avisa al autor (casos límite de la spec).
  - Hecho cuando: `07-estres.qmd` usa solo claves del plan §5 de la 005 y las tablas y figuras `stress_*`; mantiene el rótulo «adaptación del escenario Fed 2026»; reporta bandas de parámetros (no de predicción), réplicas negativas o explosivas, la regla de la tasa en cero y la sensibilidad rotulada «sensibilidad, no efecto estimado», D igual al adverso bajo esa regla, RF-12a y RF-12c, crédito constante desde 2027T3, el nivel de la tasa anclado en FEDFUNDS y la especificación lineal con RESET y Chow rechazados; sin equivalente en dólares ni estimador restringido.

- [x] **T9. Secciones 8 y 9 (implicaciones y conclusiones).** RF-10, RF-11; RNF-3, RNF-6 · agente: claude
  - Tests: los de T1 y T3, más que el tablero no contenga cifras que no sean variables ni umbrales numéricos nuevos.
  - Hecho cuando: `08-implicaciones.qmd` con los siete puntos de la guía y el tablero (indicador, criterio cualitativo, acción), enlazados con 4 a 7, con la literatura y con el resultado de aprendizaje de la asignatura; `09-conclusiones.qmd` responde la pregunta y dice cómo anticipar y gestionar el riesgo. En borrador hasta T8.

## Integración Codex (turno exclusivo tras T5–T9)

- [x] **T10. Secciones descriptivas, referencias y base de datos.** RF-4, RF-7, RF-13; RNF-1 · agente: codex
  - Tests: los de T1 y T3 sobre estas secciones; la sección 10 solo contiene las referencias citadas.
  - Hecho cuando: `03a-datos.qmd`…`03e-desviaciones.qmd` (variables, período, fuentes, transformaciones, el hueco de octubre de 2025 sin imputar, desviaciones frente a la guía y al pre-registro, `n_series` único, vintage FRED del 2-oct-2026), `10-referencias.qmd` y `11-datos-descarga.qmd` (guía anuncia un notebook y el proyecto usa su pipeline; `pandas_datareader` y su respaldo; congelación; reproducción con `uv run python -m src.pipeline all`).

- [x] **T11. Render integral y validación.** RF-14; RNF-2 a RNF-4 · agente: codex
  - Tests y comprobaciones: PDF (Typst) y docx se generan sin `?@`, `?var`, `{{<`, `[@` ni `include` sin resolver (docx descomprimido y `gfm` intermedio, además de revisión visual de PDF y Word y sus anexos completos); grep de lenguaje causal en secciones y salida; las 11 secciones; dos corridas reproducibles; suite completa cuando los cambios de código o nuevos controles lo justifiquen; trazabilidad de cada hallazgo heredado a su sección. Se comparan huellas de salidas aprobadas 003–005 con el inventario previo, sin regenerarlas por rutina.
  - Hecho cuando: `review-validate.md` con `VEREDICTO: APROBADO` (validación del autor, no auditoría independiente), con la tabla de hallazgos heredados y la sección que los trata. Si el PDF no cumple el aspecto, se avisa antes de instalar TinyTeX o cambiar de formato.
  - Cierre técnico: ejecutar `uv run pytest -q` una vez sobre la implementación final modificada; reutilizar esa evidencia si luego solo cambian notas sin afectar archivos verificados. Ejecutar la etapa `report` dos veces para reproducibilidad. Si se comprueba `all`, hacerlo en una raíz aislada con las fuentes congeladas: nunca sobreescribir las salidas aprobadas activas, y cotejar los productos 003–005 con sus huellas. No redescargar FRED. Comprobar que no quedan marcadores `PENDIENTE`, incluidos los comentarios fuente, y que 3.5 no está duplicada.

## Auditoría independiente

- [ ] **T12. Auditoría, correcciones y entrega.** RNF-5; criterios de finalización · agente: claude (coordina) + subagentes independientes
  - Hecho cuando: el revisor `revisor-econometrico` (contexto limpio, solo rutas y criterios) audita cifras, interpretación, lenguaje causal y límites; `verificador-citas` verifica `references.bib` y las citas del texto; `profesor-evaluador` evalúa contra `docs/guia-profesor.md`; Claude Code guarda `review-audit.md` con cada informe tal cual lo entregó, declara la autoría real por sección y que no es independiente de lo que redactó, y conserva las rondas; cada corrección la hace el escritor del archivo afectado y se repite la ronda acotada. Ensayo de las preguntas probables. Entrega antes del plazo que el profesor confirme (hora, extensión y formatos siguen pendientes de confirmación).

## Propiedad de archivos (un escritor por archivo)
| Archivo | Escritor |
|---|---|
| `report/secciones/01-introduccion.qmd`, `02-literatura.qmd`, `03f-limitaciones.qmd`, `04-modelo1.qmd`, `05-modelo2.qmd`, `06-resultados.qmd`, `07-estres.qmd`, `08-implicaciones.qmd`, `09-conclusiones.qmd` | Claude (solo después de G1) |
| `report/secciones/03a…03e`, `10-referencias.qmd`, `11-datos-descarga.qmd` | Codex |
| Archivos técnicos delimitados en T1–T4; `report/informe.qmd`, `report/apa.csl`, `report/anexos/tablas.qmd`, variables y productos generados allí enumerados; `specs/006-informe/interfaz.md`, `solicitudes-codex.md`, `review-validate.md`, `docs/validacion-maquetacion-006.md/json`, `MEMORY.md` al cierre | Codex |
| `specs/006-informe/solicitudes-claude.md`, `review-audit*.md` | Claude |
| `specs/006-informe/tasks.md` | Codex; propuesta coordinada con Claude, cambios sometidos al autor |
| `specs/006-informe/spec.md`, `plan.md` | Nadie (aprobados; cambios por `change`) |
Reglas: nadie edita un archivo ajeno mientras su dueño trabaja; los cambios cruzados se piden por escrito en el archivo de solicitudes del solicitante; una sola herramienta escribe a la vez.

## Orden y dependencias
Cada relevo registra estado, cambios, pruebas realizadas o no repetidas, dudas y siguiente acción en el archivo de solicitudes de su escritor. T3 contiene dos turnos exclusivos para los encabezados; no habilita trabajo concurrente. T12 coordina revisores con contexto limpio: Claude y Codex siguen siendo autores, no revisores independientes de su propio trabajo. Si falta cuota, se registra continuidad y 006 queda abierta; no se transfiere la auditoría al implementador. No hay commit ni push.

Para redactar contra las definiciones ya integradas, se ejecutará T10 tras G1 y antes de T5–T9, conservando su identificador: orden operativo T1 → T2 → T3 → solicitud Claude → T4 → G1 → T10 → T5 → T6 → T7 → T8 → T9 → T11 → T12. Este orden sustituye al orden nominal anterior, sin escritura concurrente.

Las doce tareas conservan los identificadores del borrador inicial. T1–T4 son mayores que un bloque corto: se ejecutan mediante subpasos seriales de 20–30 minutos (tests, implementación, comprobación, evidencia), sin marcarlas completas hasta cumplir todos sus criterios y sin ampliar alcance. El calendario es orientativo; no se recortan anexos ni controles para cumplirlo.

## Cobertura
| Requisito | Tareas |
|---|---|
| RF-1 | T3, T5, T6, T7, T8, T9 |
| RF-2 | T1, T3 |
| RF-3 | T2, T4 |
| RF-4 | T1, T4, T5, T10 |
| RF-5, RF-5b | T6, T7 |
| RF-6 | T3, T5, T6 |
| RF-7 | T5, T10 |
| RF-8, RF-9 | T7 |
| RF-10, RF-11 | T9 |
| RF-12 | T8 |
| RF-13 | T10 |
| RF-14 | T1, T11 |
| RF-15 | T1, T4 |
| RNF-1, RNF-2 | T1, T2, T4, T11 |
| RNF-3 | T5–T9, T11 |
| RNF-4 | T1, T11 |
| RNF-5 | T12 |
| RNF-6 | T3, T6–T9, T11 |

## Cambio editorial aprobado ? orden operativo vigente v3
El autor aprobó `change-editorial-draft.md` y las precisiones de `docs/diagnostico-tablas-editorial-006-2026-10-12.md`: dos documentos de trabajo, anexos A–F, identificadores estables, registro, alternativa combinada manual, T13–T15 y orden nuevo. Spec v4 y plan v3 aplicados por Claude; versiones previas preservadas. Este bloque sustituye al orden previo sin borrar su historia. T1–T4 no se renumeran ni se reabren.

- [x] **T13. Registro único e identificadores estables.** RF-3, RF-15; RNF-6 · agente: codex
  - Tests primero: cobertura de todas las tablas/figuras, unicidad y estabilidad ante inserciones, negativos de fuente desconocida o identificador duplicado.
  - Hecho cuando: `outputs/informe/registro.csv` y registro de enlaces generado desde fuentes actuales; `interfaz.md` lista slugs, origen y destinos. Implementación y pruebas focalizadas no sustituyen la suite completa requerida para el cierre.
  - Archivos: nuevo `src/report_editorial.py`, `tests/test_report_editorial.py`, integración `src/pipeline.py`, `tests/test_pipeline.py`; derivados en `outputs/informe/` e interfaz.

- [x] **T14. Anexo completo y versiones esenciales.** RF-3, RF-6, RF-15; RNF-6 · agente: codex
  - Tests primero: todas las celdas/columnas y notas retenidas, cada tabla completa una vez, versiones del cuerpo procedentes de subconjuntos del CSV y remisiones existentes.
  - Hecho cuando: `report/anexo-tecnico.qmd`, `report/anexos/A-*.qmd` a `F-*.qmd`; notas de φ y Motivo conservadas, `phi_nota` como nota trazable, sin panel vacío independiente; las tablas esenciales del cuerpo declaran destino completo.
  - Archivos: `src/report_editorial.py`, `src/report_tables.py`, pipeline y tests de presentación/editorial; derivados de anexos/tablas/registro. Fuente científica y valores canónicos intactos.

- [x] **T15. Render separado, índices y enlaces.** RF-14, RF-14b; RNF-4, RNF-6 · agente: codex
  - Tests y QA: ambas salidas PDF/DOCX, índices, marcadores nativos y destinos estructurales existentes; no afirmar clic funcional sin verlo. la revisión en Google Docs no es requisito de cierre.
  - Hecho cuando: vistas previas principal/anexo separadas, enlaces locales relativos y slugs textuales; URLs externas solo si el autor facilita las reales; alternativa combinada manual sin duplicar tablas completas. Límites de herramientas registrados.
  - Archivos: `_quarto.yml`, `report/informe.qmd`, `report/anexo-tecnico.qmd`, nuevo `report/entrega-combinada.qmd`, pipeline/generador y tests autorizados; previews en `outputs/preview-006/`.

Orden: T1–T4 hechas → T13 → T14 → T15 → T10 → T5 → T6 → T7 → T8 → T9 → T11 → T12.
T10 conserva sus siete archivos. T5–T9 conservan escritor Claude y sus nueve archivos, con narrativa y remisiones según el change; mantienen hallazgos, diagnósticos fallidos y requisitos oficiales. La redacción solo comienza con cesión exclusiva tras T10.
La aprobación actual permite avanzar maquetación/redacción con las reparaciones del arnés pendientes por separado; no permite declarar T11 aprobada ni cerrar 006 con suite parcial. Los checkboxes nuevos siguen abiertos si faltan esas verificaciones, aunque se anote la implementación y se avance en el orden autorizado. No se restaura el Playbook, no se modifica `frozen_stress`, no se debilitan tests ni se hacen commits/push en este ajuste.

## Seguimiento editorial v3 ? Codex, 12-oct-2026
T13 implementada: registro de 34 tablas, nueve figuras y el manifiesto auxiliar FRED, slugs estables, fuentes/SHA, enlaces locales sin URLs ficticias. T14 implementada: anexos A–F, versiones esenciales desde CSV, pies originales conservados y phi_nota trazable como nota. T15 implementada técnicamente: render doble e índices, combinada opcional generada con enlaces internos; pruebas de clic Google Docs pendientes. T10 redactada en los siete archivos asignados a Codex. Últimos controles focalizados previos a redacción:64passed/9,87s, más tests T13/T14/T15/T10 rojos antes del cambio. Se mantienen checkboxes abiertos donde falta verificación global: no se sustituyen por suite parcial. Autor permite seguir T5–T9 mientras H1/H2 se aprueban por separado.

Actualizaci?n de evidencia: Claude termin? T5?T9 y devolvi? el turno. Vistas PDF principal30 p?ginas/anexo133, DOCX comprobados contraCSV,44marcadores. ?ltimos68 tests focalizados m?s2pureza; report195id?nticos y99protegidos. H1 recuperada con autorizaci?n posterior; H2 no aplicada, solicitada revisi?n. T11/T12 y cierre pendientes de suite completa y auditor?a; no marcar tareas por resultados parciales. Perfil opcional `_quarto-combinado.yml` permite render combinado sin alterar los dos documentos de trabajo.


**Evidencia histórica ronda 4, Codex, 13-oct-2026:** tras correcciones de auditoría ronda 2 y cesión de nueve secciones estables de Claude, T11 técnica revalidada en review-validate-ronda4.md: 949 passed/567 warnings/1108,12 s/rc0, sin exclusiones; fuentes estables y 116 protegidos intactos. Informe36p/anexo149p, ocho tablas/117paneles; 53+167 marcadores y55URI actuales comprobados, 208 productos report idénticos y render con solo diferencias de metadatos. Evidencia anterior conservada como histórica. T12/006 abiertas: revisión independiente acotada y Google Docs RF-14b pendientes. No cambia contrato ni autoría; sin commit/push.


**Evidencia histórica ronda 5, Codex, 13-oct-2026:** R3-X1–X7 y C1–C7 integrados, T11 técnica revalidada en review-validate-ronda5.md; 960 passed, 567 warnings, 917.76 s; rc 0, sin exclusiones; fuentes estables, 116 protegidos intactos. Paquete nuevo ronda 5 para auditoría acotada; evidencias anteriores históricas. T12/006 y Google Docs RF-14b abiertos. Sin cambio contractual/commit/push.


**Evidencia histórica ronda 6, Codex, 13-oct:** 967 passed, 567 warnings, 951.69 s; rc 0, sin exclusiones; 02/nueve secciones de Claude inalteradas; R4-X2–X5/P1 corregidos dentro del contrato. T11 técnica revalidada; T12/006/Google Docs pendientes. Paquete final nuevo y manifiesto ronda 6, antecesores preservados. Sin commit/push.


**Evidencia vigente ronda 7:** 974 passed, 567 warnings, 1093.01 s; rc 0, sin exclusiones; R5-1–R5-5 corregidos y ajuste de Claude R5-6 integrado. Entradas estables en ocho renders finales. T11 técnica revalidada; comprobación acotada/Google Docs/T12/006 pendientes. Sin cambios de contratos ni commit/push.
