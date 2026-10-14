# Borrador de `change` editorial — Spec 006 (informe narrativo + anexo técnico separado)

Estado: **BORRADOR para aprobación del autor.** Escrito por Claude Code en turno exclusivo cedido el 12-oct-2026, solo este archivo. No modifica `spec.md` (sha `caf97028…`), `plan.md` (sha `61262159…`) ni `tasks.md` (sha `49b874d1…`), aprobados. Si el autor lo aprueba, Codex lo aplica con el procedimiento `change` (spec v4, plan v3, tasks v3) y los hashes nuevos se registran entonces. Sin commit ni push. G1 visual de la maqueta actual: aprobado por el autor; lo pendiente es este cambio editorial.

## 1. Decisión de diseño
1. **Dos documentos del mismo proyecto Quarto:** `informe` (cuerpo narrativo, secciones 1–11 de la guía, con índice) y `anexo-tecnico` (evidencia completa, con índice). Cada uno en PDF (Typst) y DOCX.
2. **Slugs estables.** Cada tabla y figura tiene un slug permanente (`AT-M1-ROB`, `AT-M2-LP`, …). Las remisiones del cuerpo usan el slug; el número visible («Tabla B.3») lo asigna el render a partir del registro. Insertar una tabla no rompe remisiones.
3. **Registro único CSV → destino** (`outputs/informe/registro.csv`, generado por código): para cada salida aprobada, una fila con `slug`, `fuente` (CSV o PNG de origen), `anexo` (A–F), `id_visible`, `titulo`, `pie` y `nota`, y `cuerpo` (`ninguno` | `reducida`).
4. **Regla de no duplicación:** cada tabla o figura aparece **completa una sola vez**, en el anexo. El cuerpo incluye una **versión reducida** solo si es esencial para una lectura independiente (quien lee solo el informe entiende la respuesta de la sección sin ir al anexo); si no, el cuerpo solo la cita por slug. La versión reducida no se escribe a mano: la genera el código desde el mismo CSV (subconjunto de filas o columnas, mismas cifras) y declara «Versión reducida; tabla completa en AT-…».
5. **Se preserva todo lo hecho:** tablas de presentación, `report/anexos/tablas.qmd` (se parte por anexo), cuaderno de figuras, notas y pies aprobados (incluida la nota de vacíos de `AT-M1-ROB` y el pie de `AT-M2-LP` con la definición de β/φ y la ausencia de banda en h0), variables y tests. Ningún contrato de 003–005 ni ninguna cifra cambia; no hay metodología nueva ni estimaciones nuevas.
6. **Anexos (propuestos):** A Datos y transformaciones; B Modelo I; C Modelo II; D Estrés; E Literatura (estudios verificados); F Desviaciones, reproducibilidad y descarga. Codex puede reagrupar sin cambiar el principio.

## 2. Comprobación contra la guía (`docs/guia-profesor.md`)
- La guía lista 11 secciones y no menciona anexos. No los exige ni los prohíbe. Formato, extensión y si se admite material complementario separado siguen **pendientes con el profesor**; no se presentan como requisitos.
- El cuerpo conserva las 11 secciones con sus títulos y subsecciones (2.1–2.5, 3.1–3.5, 6.1–6.4) y, donde la guía lo pide, lo esencial: coeficientes principales con significancia y diagnósticos con veredicto (4), respuesta dinámica y lectura (5), comparación (6.3), cambio adverso − base de ambos modelos (7), tablero (8).
- Riesgo y mitigación: si el profesor exige un único documento, el anexo se puede **concatenar** como apéndice al final del informe usando el mismo registro. Esta salida opcional se prepara, pero no es entregable por defecto. Pregunta nueva para el profesor: ¿se admite material complementario separado?

## 3. Definición por sección (pregunta · resultados · cuerpo · anexo)
| Sec. | Pregunta | Resultados a explicar | Imprescindible en el cuerpo | Al anexo |
|---|---|---|---|---|
| 1 | ¿Por qué importa y qué se pregunta? | Relevancia para la estabilidad financiera; pregunta y objetivo; ruta del informe y del anexo | Ninguna | — |
| 2.1–2.4 | ¿Qué dice la literatura sobre ciclo, determinantes, política monetaria y transmisión? | Mecanismos y expectativa de signo; solo filas «verificado» | Ninguna | — |
| 2.5 | ¿Quién estimó relaciones similares, con qué variables y métodos? | Patrón de variables y métodos y contraste con este trabajo; sin repetir los signos dudosos | Versión reducida (estudio, método) solo si es legible en el PDF; si no, prosa | Tabla completa de estudios (E) |
| 3.1 | ¿Qué datos, de dónde, qué período? | Series, frecuencia, fuentes, hueco de oct. 2025 sin imputar, una cifra de series | Tabla reducida de series (variable, serie, frecuencia) | Descriptivos, manifiesto, estacionariedad (A) |
| 3.2–3.4 | ¿Cómo se definen morosidad, regresores y ΔFFR? | Transformaciones y su porqué; ΔFFR como «tasa de interés» y «cambio de la FFR» | Ninguna | Transformaciones y órdenes de integración (A) |
| 3.5 | ¿Qué dos modelos y qué se desvía de guía y pre-registro? | Forma de I y II; desviaciones y limitaciones (RF-7) | Versión reducida de las desviaciones relevantes | Desviaciones completas (F) |
| 4 | ¿Cómo se asocian las condiciones macro con la morosidad? | Coeficientes en pp por unidad, significancia HAC, incertidumbre; diagnósticos que fallan sin atenuar; lectura para la gestión del riesgo | Coeficientes principales + resumen de diagnósticos con veredicto | Salida completa, robustez (`AT-M1-ROB`), OOS, VIF, Chow, CUSUM (B) |
| 5 | ¿Hay efectos rezagados de la política monetaria? | Respuesta dinámica; K; Granger≡C2 con K = 1 sin segunda cifra; lectura de la regla; endogeneidad; ΔFFR no es shock identificado; h0 de `AT-M2-LP` como normalización | Una figura de la respuesta + tabla corta de lectura | Proyecciones locales completas (`AT-M2-LP`), perfil φ, selección de K (C) |
| 6.1–6.2 | ¿Qué dice cada modelo? | Síntesis sin repetir tablas | Ninguna nueva | — |
| 6.3 | ¿Cómo se comparan? | Insumos de `model2_inputs63`; difieren en muestra y controles; sin ponderar | Tabla comparativa reducida | Insumos completos (B/C) |
| 6.4 | ¿Son relevantes macro y política monetaria para el riesgo? | Respuesta a la pregunta fundamental; asociación ≠ causalidad; preguntas probables | Ninguna | — |
| 7 | ¿Cuánto cambia la morosidad bajo estrés adverso frente a base? | «Adaptación del escenario Fed 2026»; cambio adverso − base de ambos modelos; bandas = incertidumbre de parámetros; D con fechas adaptadas; límites | Tabla de cambios por escenario y modelo + una figura de trayectorias | Niveles, trayectorias, sensibilidades, réplicas fuera de rango, limitaciones (D) |
| 8 | ¿Cómo se usa en una institución? | Los siete puntos de la guía conectados con 4–7 y 2; resultado de aprendizaje | Tablero cualitativo (sin umbrales numéricos) | — |
| 9 | ¿Qué responde el trabajo y cómo anticipar y gestionar el riesgo? | Respuesta directa, no lista de significancias | Ninguna | — |
| 10 | Referencias APA 7 | — | Lista completa | — |
| 11 | ¿Cómo se obtuvieron y se reproducen los datos? | Guía anuncia notebook; el proyecto usa su pipeline; congelación; hueco; `uv run python -m src.pipeline all` | Prosa corta | Manifiesto y comandos (F) |

## 4. Diff propuesto a la spec (v3 → v4)
**Estructura obligatoria** (añadir al final del párrafo): «El entregable consta de dos documentos: el informe (secciones 1 a 11, con índice) y el anexo técnico (con índice), renderizados a PDF y DOCX. El anexo contiene cada tabla y figura aprobada completa una sola vez; el informe incluye solo versiones reducidas esenciales para una lectura independiente y remite al anexo por slug.»

**RF-3** — reemplazar:
- ANTES: «Las tablas del informe serán `outputs/tables/*.md` incluidas con `include`; las figuras serán `outputs/figures/*.png`, con pie y la fuente (…). La tabla de estudios de 2.5 la genera código desde la matriz de literatura.»
- DESPUÉS: «Las tablas y figuras se incluyen desde los productos generados por código a partir de `outputs/` (CSV y PNG aprobados) y se asignan por el registro único (`outputs/informe/registro.csv`): completas una sola vez en el anexo técnico, y en el informe solo como versión reducida cuando sea esencial para una lectura independiente. Cada una lleva slug estable, pie y la fuente («Fuente: FRED; elaboración propia»; en 7, la indicada por la spec 005) y conserva las notas aprobadas. Un test comprueba que cada cifra de una tabla reducida o de presentación coincide con su CSV. La tabla de estudios de 2.5 la genera código desde la matriz de literatura.»

**RF-14** — reemplazar la primera frase y añadir:
- DESPUÉS (inicio): «EL SISTEMA renderizará `report/informe.qmd` y `report/anexo-tecnico.qmd` a PDF (Typst) y a Word (docx) sin que queden `?@`, `?var`, `{{<` ni referencias sin resolver, …» (el resto del RF se mantiene).
- Añadir RF-14b: «Las remisiones entre secciones y al anexo usan anclas nativas de Pandoc (identificador por slug) y funcionan como enlace interno en PDF y DOCX dentro de cada documento. Entre los dos documentos, la remisión es siempre texto estable («Anexo B, `AT-M1-ROB`») y se convierte en hipervínculo solo si el autor suministra una URL (por ejemplo de Drive) en un archivo de enlaces que el autor mantiene. Ningún agente sube ni publica archivos. En Google Docs no se garantiza el salto entre archivos locales; se verifica el salto interno y se documenta el límite.»

**RF-15** — añadir: «y el registro único `outputs/informe/registro.csv` con slugs, destinos y versiones reducidas, los índices de ambos documentos y las etiquetas de anexo; dos corridas dejan salidas idénticas.»

**RNF-6** — añadir: «Cada remisión del cuerpo a un slug existe exactamente una vez en el anexo; no hay slugs duplicados, huérfanos ni tablas completas repetidas en el cuerpo.»

**Criterios de finalización** — añadir: cobertura del registro (todo CSV/PNG aprobado tiene destino); funcionamiento de enlaces internos en PDF y DOCX (DOCX revisado en Google Docs, sin Word nativo, como excepción documentada); lo esencial de la guía presente en el cuerpo.

**Dudas abiertas** — añadir: «¿Admite el profesor material complementario separado?» (pendiente, no requisito).

## 5. Diff propuesto al plan (v2 → v3)
- **§1 Disposición:** añadir `report/anexo-tecnico.qmd` (Codex), `report/anexos/` partido por anexo (A–F) con un archivo por anexo, `outputs/informe/registro.csv` (generado) y archivo opcional de URLs externas mantenido por el autor.
- **§3b Tablas anchas:** mantener las tablas de presentación y añadir: «el registro único decide qué va al anexo y qué versión reducida va al cuerpo; el adaptador de presentación copia el pie aprobado de la tabla original (p. ej. `model2_lp.md`) y las notas de vacíos (`AT-M1-ROB`), sin cambiar celdas ni CSV, y sin inventar “n.a.”».
- **§4 Tests:** añadir cobertura del registro, unicidad de slugs, existencia de cada remisión, ausencia de tabla completa duplicada, presencia de notas y pies, y tests negativos de cada uno. El test de cifras a mano y el de citas cubren también `anexo-tecnico.qmd`.
- **§6 Dependencias:** insertar T13–T15 (abajo) tras T4 y antes de T10.
- **§2 Propiedad:** `report/anexo-tecnico.qmd`, `report/anexos/**`, `outputs/informe/**` y el archivo de URLs son de Codex; mis nueve secciones no cambian de dueño. Claude no edita anexos.

## 6. Diff propuesto a las tareas (v2 → v3), sin renumerar T1–T4 (completas)
Nuevas, todas de Codex salvo indicación:
- **T13. Registro único y slugs.** RF-3, RF-15; RNF-6 · codex. Genera `registro.csv` desde las 34 tablas y 9 figuras aprobadas; asigna anexo y slug; tests de cobertura y unicidad primero. Hecho cuando: cada salida aprobada tiene destino y la interfaz lista los slugs.
- **T14. Anexo técnico y versiones reducidas.** RF-3, RF-6; RNF-6 · codex. Parte `report/anexos/tablas.qmd` por anexo, incluye los pies y notas aprobados, corrige el adaptador de presentación (pie de `model2_lp`, nota de vacíos de `AT-M1-ROB`, `phi_nota` como pie y no como panel), genera las versiones reducidas esenciales. Hecho cuando: cada tabla completa aparece una sola vez en el anexo.
- **T15. Render doble, índices y enlaces.** RF-14, RF-14b · codex. `_quarto.yml` con dos documentos, índices, anclas nativas, archivo opcional de URLs, salida concatenada opcional. Hecho cuando: ambos documentos se generan en PDF y DOCX, los enlaces internos funcionan y están revisados en Google Docs; límites documentados.
- **T10** se mantiene (Codex), ahora sobre el diseño nuevo y tras T15.
- **T5–T9 (Claude)** conservan identificador y archivos, con alcance nuevo: narrativa, resultados explicados en pp, remisiones por slug y solo las tablas esenciales de §3; no repiten tablas. Siguen sin empezar hasta recibir cesión.
- **T11** valida además registro, remisiones, enlaces y no duplicación. **T12** audita que el cuerpo no oculte evidencia requerida por la guía ni cifras sin trazabilidad al anexo.
- **Orden operativo nuevo:** T1–T4 (hechas) → aprobación del `change` → T13 → T14 → T15 → T10 → T5 → T6 → T7 → T8 → T9 → T11 → T12. G1 de la maqueta anterior no se repite; el autor decide si revisa la nueva.

## 7. Lo que no cambia
Cifras solo por `{{< var >}}` o tablas generadas; citas solo verificadas; lenguaje de asociación; sin estimaciones ni metodología nuevas; contratos y productos 003–005 y `data/raw/` intactos; `report/_variables.yml` sin cambios de valores; un escritor por archivo; sin commit ni push; sin subir archivos externos. El test de arnés `test_codex_harness` (enlace a `docs/flujo-codex-orca.md` y Playbook inexistente) es ajeno a este cambio y no se corrige aquí.

## 8. Decisiones que necesita el autor
1. Aprobar o ajustar este diseño (dos documentos, slugs, registro, regla de no duplicación).
2. Confirmar la agrupación de anexos A–F.
3. Autorizar que Codex aplique el `change` y numere las tareas T13–T15.
4. Indicar si desea la salida concatenada opcional preparada desde ya.
5. Suministrar las URLs de Drive si quiere saltos entre documentos en la nube.
6. Preguntar al profesor si admite material complementario separado.

## Cesión
Termino mi turno exclusivo. **Cedo la escritura del checkout a Codex.** Escribí únicamente `specs/006-informe/change-editorial-draft.md`. Mi bloque anterior en `solicitudes-claude.md` queda como antecedente. No hay cesión de redacción del informe para mí.
