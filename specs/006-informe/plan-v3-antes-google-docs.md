# Plan 006 — Informe
Estado: aprobada v3 (change editorial aplicado por Claude Code, 12-oct-2026, por aprobación literal del autor; v2 aprobada conservada byte a byte en `plan-v2-approved.md`; ver `change-editorial-applied.md`). Contrato: `specs/006-informe/spec.md` v4. Cambios v3: §1a (dos documentos), §3b ampliada (registro, adaptador, versiones reducidas), §4 (tests del registro y enlaces), §5b (enlaces), §6 (orden con T13–T15), §2 (propiedad). El resto del texto v2 permanece; donde dice «spec v3» léase v4 y donde dice que no hace falta `change`, rige esta versión.
Texto v2 (histórico): borrador v2 (Claude Code, 12-oct-2026; incorpora el humo mínimo de Codex, `docs/render-humo-006-2026-10-12.md`) · aprobado por el autor. Contrato v2: `specs/006-informe/spec.md` v3 (sha256 `caf97028a2b236404cc00bbe2fe40253f2d48ecd58fc686417091ca3bf3ad3df`). Decisiones del autor del 12-oct que este plan aplica: (1) opción A de proyecto Quarto; (2) auditoría con revisor de contexto limpio, validación técnica de Codex, verificador de citas y evaluador de rúbrica.

Las dos «Dudas abiertas» de la spec sobre la disposición del proyecto y la independencia de la auditoría quedan resueltas por esas decisiones y por este plan; el texto de la spec no se reescribe para conservar su huella. Ninguna decisión modifica un requisito de la spec (RF-14 y las «Dudas abiertas» ya preveían la opción A), por lo que no hace falta `change`.

## 1. Disposición del proyecto Quarto (opción A)
| Elemento | Ubicación | Propietario | Nota |
|---|---|---|---|
| `_quarto.yml` | **raíz del repositorio** | Codex | `project: {type: default, render: [report/informe.qmd]}` (la lista evita que Quarto procese `README.md`, `docs/` ni `specs/`); `bibliography: report/references.bib`; `csl: report/apa.csl`; `lang: es`; formatos `typst` (principal, con `format.typst.citeproc: true`: Pandoc procesa las citas con el mismo `apa.csl` porque el CSL nativo de Typst falla en Windows con una barra invertida en la ruta) y `docx`. La 007 añadirá `report/slides.qmd` a la lista. |
| `report/informe.qmd` | `report/` | Codex | Solo YAML del documento y los `include` de las secciones en orden. |
| `report/secciones/NN-*.qmd` | `report/secciones/` | ver §2 | Un escritor por archivo. |
| `report/_variables.yml` | `report/` | **Fuente de verdad** de las variables; la escriben las etapas del pipeline (contrato de 001–005, sin cambios) | Nadie la edita a mano. |
| `_variables.yml` | **raíz** | Generada por código | Copia **byte a byte** de la anterior; Quarto solo lee `{{< var >}}` desde la raíz del proyecto (`docs/entorno-quarto-2026-10-12.md`). No se edita; no se versiona (`.gitignore`, tarea de Codex). |
| `report/apa.csl` | `report/` | Codex | «APA Style 7th edition», CC BY-SA 3.0, de `https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl`; sha256 `3917def5fc951b104d64216c3373096042368b9704ba269ca83c14ebaba889fc` (85 817 B), registrado en el manifiesto de procedencia. Si la huella difiere, Codex lo comunica antes de usarlo. |
| `report/references.bib` | `report/` | Codex (contrato de 002) | Sin cambios salvo la URL de `fred2026` (tarea aprobada de la spec, T-ref). |
| Rutas de tablas y figuras | `../outputs/...` relativas al `.qmd` de `report/` (válidas dentro de la raíz del repositorio) | — | **No se copian** tablas ni figuras (la prueba de humo mostró que Typst las lee dentro de la raíz). |

**Una única fuente de verdad y su copia.**
- Función pura `sync_report_variables(source_text: str) -> str` (identidad; solo valida que el YAML cargue y que no esté vacío) y una E/S mínima en `stage_report`: lee `report/_variables.yml`, escribe `_variables.yml` en la raíz con los mismos bytes (`newline="\n"`) y relee ambos para comparar sha256; si difieren, la etapa falla.
- `stage_report` (hoy provisional en `src/pipeline.py`) se invoca al final de `all` y es obligatoria antes de cada render: `_quarto.yml` declara `project.pre-render` con `uv run python -m src.pipeline report` (si Codex comprueba en T1 que el gancho no funciona en este entorno, el plan lo sustituye por un orden documentado `report` → `quarto render` y se avisa al autor).
- Test `test_root_variables_in_sync`: si existe `_variables.yml` en la raíz, es idéntico byte a byte a `report/_variables.yml`; y el test de la etapa `report` en un directorio temporal comprueba la copia, la falla con una copia alterada y la idempotencia (dos corridas, mismas huellas).
- Cada cambio en las etapas `models` o `stress` obliga a repetir `report` (lo hace `all`); el render nunca lee una copia anterior porque el gancho la regenera.

**Efectos en documentos compartidos (requieren aprobación del autor, §8).** La skill `informe-quarto` dice que `report/` necesita `report/_quarto.yml`; con la opción A pasa a decir: «`_quarto.yml` en la raíz; `report/_variables.yml` es la fuente y `_variables.yml` de la raíz su copia generada». `AGENTS.md` conserva `quarto render report/informe.qmd` (Quarto sube al `_quarto.yml` de la raíz).

## 1a. Dos documentos y registro único (change editorial v4)
| Elemento | Ubicación | Propietario | Nota |
|---|---|---|---|
| `report/informe.qmd` | `report/` | Codex | Informe narrativo de 11 secciones, con índice. |
| `report/anexo-tecnico.qmd` | `report/` | Codex | Anexo con índice; incluye `report/anexos/A-*.qmd` … `F-*.qmd` (un archivo por anexo; reemplaza el `report/anexos/tablas.qmd` único, preservando su contenido). |
| `_quarto.yml` | raíz | Codex | `project.render: [report/informe.qmd, report/anexo-tecnico.qmd]`; ambos en `typst` y `docx`. |
| `outputs/informe/registro.csv` | `outputs/informe/` | Generado por código (Codex) | Slug, fuente, anexo, identificador visible, título, pie y nota, versión en el cuerpo. Es la única fuente de destinos. |
| Archivo opcional de URLs externas | por definir por Codex | Autor (contenido) | Solo URLs reales suministradas o autorizadas por el autor (p. ej. Drive). Nadie sube archivos. |
Reglas: cada tabla o figura completa una sola vez en el anexo; versión reducida en el cuerpo solo si es esencial para una lectura independiente, generada desde el mismo CSV; una figura esencial no se recorta ni pierde bandas. **Alternativa combinada:** salida manual (informe más anexo como apéndice, sin duplicar tablas completas); no es la predeterminada y su aceptación por el profesor no está confirmada.

## 2. Propiedad de archivos (un escritor por archivo)
Adición v3: `report/anexo-tecnico.qmd`, `report/anexos/**`, `outputs/informe/**` y el archivo de URLs son de Codex; Claude no los edita. Mis nueve secciones no cambian de dueño y remiten a los anexos por slug.

| Archivo | Escritor | Notas |
|---|---|---|
| `report/secciones/01-introduccion.qmd` | Claude | Título propuesto de la guía en `informe.qmd`; pregunta y objetivo aquí. |
| `report/secciones/02-literatura.qmd` | Claude | Texto de 2.1–2.5; la tabla de estudios de 2.5 se incluye desde `../outputs/tables/lit_estudios.md`. |
| `report/secciones/03a-datos.qmd`, `03b-variables.qmd`, `03c-politica.qmd`, `03d-modelos.qmd`, `03e-desviaciones.qmd` | Codex | 3.1–3.5 descriptivos y desviaciones frente al pre-registro y la guía (RF-7). |
| `report/secciones/03f-limitaciones.qmd` | Claude | Párrafos de limitaciones de 3.5; mismo encabezado 3.5 continuado. |
| `report/secciones/04-modelo1.qmd`, `05-modelo2.qmd`, `06-resultados.qmd` | Claude | Interpretación, discusión y respuesta a 6.4. |
| `report/secciones/07-estres.qmd` | Claude | Hasta cerrar la 005: solo el marcador «pendiente de resultados de la spec 005» (RF-12). |
| `report/secciones/08-implicaciones.qmd`, `09-conclusiones.qmd` | Claude | Tablero cualitativo; sin umbrales numéricos. |
| `report/secciones/10-referencias.qmd`, `11-datos-descarga.qmd` | Codex | 11 explica el pipeline (RF-13). |
| `report/informe.qmd`, `_quarto.yml`, `report/apa.csl`, `report/references.bib`, `report/_variables.yml`, `_variables.yml`, `.gitignore`, `src/`, `tests/` | Codex | Claude no los edita. |
| `specs/006-informe/solicitudes-claude.md` | Claude | Peticiones a Codex por escrito (variables, tablas, figuras, correcciones). Codex no lo edita. |
| `specs/006-informe/solicitudes-codex.md` | Codex | Peticiones a Claude (cambios en secciones). Claude no lo edita. |

Reglas: nadie edita un archivo ajeno mientras su dueño trabaja; los cambios cruzados se piden en los archivos de solicitudes; una sola herramienta escribe en el checkout a la vez (entrega explícita de turno). La interfaz entre los dos lados es el **inventario de variables y tablas** `specs/006-informe/interfaz.md` (Codex lo genera desde `report/_variables.yml` y `outputs/` en T2): Claude solo usa claves y archivos allí listados; si falta uno, lo pide.

## 3. Variables, tablas y figuras nuevas (RF-15, a cargo de Codex en la etapa `report`)
- `datos.n_series` único y coherente con la referencia institucional (12 frente a 13): una sola cifra generada; el test falla si dos salidas dicen otra cosa.
- Conteos de literatura (estudios por tema, «verificado», «pendiente-lectura»), desde `research/matriz-literatura.md`; tabla `lit_estudios.{csv,md}` (2.5: estudio, variables, metodología, signo); solo filas «verificado».
- Cifras de hallazgos heredados que la spec marca (por ejemplo φ_h, el cambio de signo de ΔFFR, el recuento de robustez, K = 1): solo desde claves ya existentes; si no existen, se piden en `solicitudes-claude.md`; ninguna se calcula nueva ni se escribe a mano.
- Para `estres.*`: solo las claves del plan §5 de la 005, y únicamente cuando la 005 esté cerrada (§6).
- Cada tabla nueva: CSV + MD, español, sin `|` sin escapar, pie con fuente.

## 3b. Tablas anchas en el PDF (hallazgo del humo)
La tabla `model1_coefficients.md` (9 columnas con etiquetas largas) se renderiza en Typst con etiquetas partidas sílaba a sílaba e identificadores solapados (`outputs/smoke-006/report/preview.png`). No se editan ni se sustituyen las tablas de 003/004/005 (son salidas aprobadas). Solución del plan, a cargo de Codex y sin cambiar resultados:
- Las tablas del informe se incluyen desde **tablas de presentación** generadas por código a partir de los CSV aprobados (`outputs/informe/*.md`, nombre de carpeta a confirmar en T2): mismas cifras y filas, columnas seleccionadas y rotuladas en español, etiquetas abreviadas; las tablas completas quedan en `outputs/tables/` y en un anexo de descarga (sección 11).
- Ajustes de composición en `_quarto.yml` o en la plantilla Typst (tamaño de letra reducido para tablas, anchos relativos), sin tocar el texto.
- Un test comprueba que cada cifra de una tabla de presentación coincide con su CSV de origen (una sola fuente), y que no se crea ninguna cifra nueva.
- Alternativa si no basta: páginas apaisadas para tablas muy anchas. La decide Codex y la comunica antes de cambiar la maquetación del documento.
Esta tarea se hace antes de que yo escriba 4, 5, 6 y 7, para ver el aspecto real.

**Adición v3.** (a) El registro único decide qué va al anexo y qué versión reducida va al cuerpo. (b) El adaptador de presentación copia el pie aprobado de la tabla original (por ejemplo `model2_lp.md`: definición de β y φ y ausencia de banda en h0) y trata `phi_nota` como pie y no como panel; añade una nota que explica los vacíos de `model1_robustness_estimates` (45 vacíos intencionales de «motivo»; la última fila R8 no estimada por falta de historia anterior a 2000T1). Sin cambiar celdas ni CSV, sin inventar «n.a.», y sin atribuir esas tablas a los JSON principales, que no las exportan. (c) Tablas reducidas: mismo CSV, mismas cifras, declaran dónde está la completa. (d) Clasificación econométrica de las celdas del Panel 5: identidad por construcción (φ0 = 1, sin error estándar ni banda en h0), resultado estimado (h1..h12), dato no aplicable por diseño (vacío intencional) o no estimado (R8).

## 4. Tests y comprobaciones (los escribe y ejecuta Codex; Claude revisa su alcance)
| Control | Detalle |
|---|---|
| Cifras a mano | `test_report_has_no_hand_typed_numbers` hoy recorre `report/*.qmd`; se **extiende a `report/secciones/**/*.qmd`** (aprobación en §8). Test negativo con una sección que contenga «0,8 pp». |
| Citas | El test de citas contra `references.bib` cubre `report/secciones/**`; falla ante una clave inexistente, una de fila «pendiente-lectura» o «descartado». |
| Lenguaje | grep de «causa», «causal», «provoca», «debido a» sobre las secciones y sobre la salida renderizada (docx descomprimido con `zipfile` y `gfm` intermedio; el PDF se verifica por existencia, tamaño y ausencia de error de render; no se añade ninguna dependencia). Test negativo. |
| Sin restos | La salida renderizada no contiene `?@`, `?var`, `{{<`, `[@`, ni `include` sin resolver. |
| Marcador de 005 | Mientras la 005 esté abierta, `07-estres.qmd` contiene el marcador y el render imprime una advertencia visible «informe incompleto»; con la 005 cerrada, el marcador no puede estar. |
| Estructura | Las 11 secciones y las subsecciones 2.1–2.5, 3.1–3.5 y 6.1–6.4 existen con los títulos de la guía, en orden. |
| Reproducibilidad | Dos corridas de `report` dejan las mismas huellas; dos renders dan el mismo texto (el PDF puede variar en metadatos de fecha; se compara el texto del docx y del gfm). |
| Copia de variables | §1. |
| Registro y slugs (v3) | Todo CSV y PNG aprobado tiene fila de destino; slugs únicos; cada remisión del cuerpo existe una sola vez en el anexo; ninguna tabla completa repetida en el cuerpo; pies y notas presentes; cada cifra de una tabla reducida coincide con su CSV. Tests negativos de cada control. |
| Enlaces (v3) | Anclas nativas de Pandoc; destinos nombrados del PDF y bookmarks del DOCX existen; enlaces relativos locales apuntan a archivos existentes; URLs externas solo del autor. Prueba estructural, no de clic. |
| Cifras y citas (v3) | Los tests de cifras a mano y de citas cubren también `report/anexo-tecnico.qmd` y `report/anexos/**`. |
| No regresión | `uv run pytest -q` completo, incluido lo existente. |

## 5. Render de humo (primera tarea, bloqueante para la redacción)
**Estado (12-oct-2026): humo mínimo hecho por Codex con autorización directa del autor** (`docs/render-humo-006-2026-10-12.md` y `.json`, artefactos en `outputs/smoke-006/report/`): PDF (Typst) y docx se generan en el proyecto real con la opción A; variable, tabla, figura y cita resueltas; sin marcadores pendientes; Quarto 1.10.19, Pandoc 3.10, Typst 0.15.1; copia de variables idéntica por bytes (sha256 `305f11e3…2a95`). Lo que **no** probó: `stage_report`, el gancho `pre-render`, los tests y `.gitignore` (siguen para las tareas del plan aprobado). Hallazgos que cambian el plan: (a) en esta sesión Quarto no está en el PATH y el envoltorio `quarto.cmd` falla con la ruta con espacios: se usa `C:/Program Files/Quarto/bin/quarto.exe`, y el gancho `pre-render` debe llamar a `uv` y no a Quarto, con su prueba; (b) `format.typst.citeproc: true` (arriba); (c) **las tablas anchas de `outputs/tables/` no caben en el PDF** (§3b). Descripción original de la tarea, que se repite con la implementación definitiva:
Codex, en el proyecto real y con la opción A: `_quarto.yml` mínimo en la raíz, `report/informe.qmd` con una variable (`modelo1.n_obs`), una tabla incluida (`../outputs/tables/model1_coefficients.md`), una figura (`../outputs/figures/model1_coefficients.png`), una cita `[@newey1987]`, `report/apa.csl` y la copia de variables. **Aceptación:** PDF (Typst) y docx se generan; variable, tabla, figura y cita resueltas; sin restos (§4); el gancho `pre-render` regenera la copia o, si no funciona, el orden documentado; versiones de Quarto, Pandoc y Typst registradas igual que en `docs/entorno-quarto-2026-10-12.md`. **Si falla algo, se avisa al autor antes de cambiar de formato.** La petición escrita está en `specs/006-informe/solicitudes-claude.md`. Claude no escribe prosa definitiva hasta que el humo pase y el autor apruebe el plan.

## 5b. Enlaces entre secciones y documentos (v3)
Dentro de cada documento, anclas nativas de Pandoc por slug (no HTML) en PDF y DOCX. Entre informe y anexo, texto estable «Anexo X, `slug`» más enlace relativo local cuando el otro archivo exista. Hacia la nube, solo URLs reales del autor. En Google Docs no se garantiza el salto entre archivos locales: se verifica el interno y se documenta el límite. Las pruebas son estructurales; no se afirma clic en Word ni en Google Docs.

## 6. Dependencias y orden
**Orden operativo vigente (v3):** T1–T4 (hechas) → T13 → T14 → T15 → T10 → T5 → T6 → T7 → T8 → T9 → T11 → T12. Se puede avanzar la redacción mientras Codex diagnostica los fallos del arnés (test de arnés por el Playbook eliminado; hashing repetido de `outputs` en `frozen_stress`); T11 no se aprueba ni 006 se cierra sin la suite global completa en verde. G1 de la maqueta anterior está aprobado por el autor y no se repite. La numeración v2 de abajo se conserva como histórica.
1. Aprobación del plan y de las tareas por el autor.
2. T1 humo (Codex) → T2 inventario de variables/tablas `interfaz.md`, esqueleto de `informe.qmd` y secciones vacías con encabezados (Codex) → T3 variables y tabla 2.5, `n_series`, `fred2026` (Codex).
3. Redacción de Claude de 1, 2, 3f, 4, 5 y 6 con la interfaz fijada; en paralelo Codex 3a–3e, 10 y 11.
4. Sección 7: solo con la 005 cerrada (`review-validate.md` y `review-audit.md` en APROBADO, tareas T10 completas). Si no llega, los casos límite de la spec: informe con marcador y aprobación expresa del autor.
5. Secciones 8 y 9 se redactan en borrador antes con marcas `[DEPENDE 005]` y se completan tras la 7.
6. Validación de Codex (`review-validate.md`) → auditoría (§7) → correcciones → entrega.

Calendario de trabajo (el objetivo interno es la revisión final del jueves 15-oct por la noche; la hora oficial sigue sin confirmar con el profesor): lun 12 plan, tareas y humo; mar 13 secciones 1–6 y 3, 10, 11; mié 14 cierre de la 005 y secciones 7–9, validación y auditoría; jue 15 correcciones y revisión final. Es ajustado: cualquier retraso de la 005 o del humo se comunica de inmediato.

## 7. Auditoría y declaración de autoría (decisión del autor)
- **Autoría real:** Claude Code redacta las secciones 1, 2, 3f, 4, 5, 6, 7, 8 y 9; Codex prepara 3a–3e, 10, 11, tablas, figuras, variables y render. Claude **no** audita de forma independiente lo que redactó.
- **Auditoría independiente:** un revisor de contexto limpio (`revisor-econometrico`, otra instancia) con solo rutas y criterios, sin la conclusión de Claude, sobre cifras, interpretación, lenguaje causal y límites; `verificador-citas` sobre `references.bib` y las citas del texto; `profesor-evaluador` contra `docs/guia-profesor.md`.
- **Validación técnica:** Codex (`review-validate.md`): tests, render, estructura, copia de variables, reproducibilidad.
- `review-audit.md` de la 006 lo guarda Claude con el informe tal cual lo entregó cada subagente, declara la autoría real por sección y la salvedad de independencia; las rondas se conservan.

## 8. Decisiones que requieren aprobación expresa del autor
1. Que Codex edite la skill compartida `.claude/skills/informe-quarto/SKILL.md` solo en la línea del proyecto Quarto (§1). Sin esa edición la skill contradiría el plan; no se edita sin aprobación.
2. Que Codex extienda `tests/test_harness.py` (cifras a mano) y el test de citas a `report/secciones/**` (§4). Fortalece el control; no cambia la regla.
3. Que el gancho `pre-render` ejecute el pipeline (§1), o el orden documentado alternativo.
4. Que `.gitignore` incluya `_variables.yml` de la raíz.

## 9. Riesgos
| Riesgo | Mitigación |
|---|---|
| Copia desincronizada de variables | Copia generada, comparación de sha256 en la etapa, gancho y test. |
| El gancho `pre-render` no corre `uv` en este entorno | T1 lo prueba; alternativa documentada. |
| Edición simultánea de archivos | §2 y una sola herramienta escribiendo. |
| La 005 no se cierra a tiempo | Marcador y aprobación expresa del autor; no se redacta 7 con cifras provisionales. |
| Cifras de hallazgos heredados no disponibles como variables | `solicitudes-claude.md`; si exigen un cambio de una spec cerrada, `change`, no esta spec. |
| Auditoría de lo escrito por quien audita | §7; sin atribuir independencia a Claude ni a Codex sobre sus propias secciones. |
| Tablas anchas ilegibles en el PDF | §3b: tablas de presentación generadas por código, sin tocar las aprobadas. |
| Quarto fuera del PATH / envoltorio `.cmd` | Ruta absoluta a `quarto.exe`; el gancho llama a `uv`, no a Quarto. |
| Typst frente a LaTeX en el aspecto | El PDF de Typst es la decisión del autor; si no cumple, se avisa antes de instalar TinyTeX. |
| Tiempo | Calendario de §6; recortes los decide el autor. |
