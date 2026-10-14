# Auditoría independiente de 006 — Ronda 3 (acotada)

Estado: **CAMBIOS MENORES NECESARIOS** (2 revisores APROBADO, 1 CAMBIOS NECESARIOS por defectos editoriales menores). No hay hallazgos bloqueantes ni de econometría. Rondas 1 y 2 conservadas intactas (`review-audit.md`, `review-audit-ronda1-*.md`, `review-audit-ronda2.md`, `review-audit-ronda2-*.md`).

## Alcance y autoría

- Alcance fijado por el usuario y Codex: solo (a) estado de los hallazgos de la ronda 2 y (b) regresiones de las correcciones. No se exigió leer completos todos los estudios ni se añadieron requisitos. Fecha de portada del 16 de octubre de 2026: decisión expresa del autor; no es la hora límite oficial, que sigue sin confirmarse.
- Autoría del informe auditado: Claude redactó 01, 02, 03f, 04–09 (con sus correcciones de la ronda 2); Codex redactó 3a–3e, 10, 11, tablas, figuras, filtros, APA, anexos e infraestructura y validó la suite.
- Coordinación: Claude Code. **No es auditoría independiente de mi propio texto.** La independencia procede de tres revisores de contexto limpio que recibieron solo rutas, criterios y sus propios hallazgos de la ronda 2.
- Informes en copia (las entidades HTML `&lt;`, `&gt;`, `&amp;` llegaron así en la notificación):
  - `review-audit-ronda3-revisor-econometrico.md` — APROBADO.
  - `review-audit-ronda3-verificador-citas.md` — APROBADO.
  - `review-audit-ronda3-profesor-evaluador.md` — CAMBIOS NECESARIOS (92/100 estimado; 89 en la ronda 2).

## Versión auditada (entrega de Codex: 949 passed, rc0, sin exclusiones)

| Archivo (`outputs/preview-006/report/`) | SHA-256 verificado por Claude antes de lanzar |
|---|---|
| informe.pdf | d1a3460abea1cd9e17ef4a68a8fbd1a8ec1d54b72a75d83ccda1e9af0e06fd0f |
| anexo-tecnico.pdf | a3e888466c600318fa549bfa0bfc6b19c74379c24b927d491f48a197807e8150 |
| informe.docx | a524791b74bea38e0426aba2daa160788a1d0a0c7609f5f7ad1cb37a2c224337 |
| anexo-tecnico.docx | e2a8d81ec8b8ebf41e947577abd87236879c23b9634e21335adde20ac6ed460a |

Solo se comprobó el prefijo de 24 caracteres de cada uno antes de lanzar; coincidía con los comunicados. Secciones de Claude (prefijos de 24 caracteres iguales a los de la cesión): 01 be47254b…, 02 fed06116…, 03f 8f97f714…, 04 8c28bfdc…, 05 86b112ee…, 06 87b78120…, 07 28e37c35…, 08 c1404f1f…, 09 278df8c2….

## Estado de los hallazgos de la ronda 2

- **Econométrico:** N1 (PIB rezagado, actividad), N2 (regla de tasa), N3 (KPSS, notación única), N4 (clasificación de limitaciones), N5 (lectura de signos del estrés), N6, N7 (letras duplicadas, 60 enlaces a 34 destinos, todos presentes), N8–N12: resueltos. R1#11 mayormente resuelto.
- **Citas:** Newey y West 703–708 confirmado por RePEc (no por Crossref/OpenAlex); FRED y Fed en APA 7 correctos; nombres propios en mayúscula; frase nueva sobre Obradović y Grubišić respaldada; `verify_refs.py` 21 de 21.
- **Profesor:** portada limpia; estrés explicado; línea del adverso visible; Figura 1 de DRALACBS; enlaces visibles; APA en lo esencial; regla de tasa con una sola justificación.

## Pendientes menores (ninguno bloquea) y escritor propuesto

Las correcciones de mis archivos requieren turno exclusivo cedido; no se hacen sin él.

### Míos (Claude)

| ID | Hallazgo | Fuente | Ubicación |
|---|---|---|---|
| R3-C1 | «hacia el final de la trayectoria esa diferencia se invierte» es impreciso: lo que se invierte son el crecimiento del producto y ΔU, no los niveles; el desempleo implícito del adverso sigue por encima del base en todo el horizonte (≈ +3,8 pp al final). Decir «menor crecimiento del producto y mayor aumento del desempleo (ΔU)» en los primeros trimestres y que hacia el final el crecimiento se recupera y ΔU baja, sin implicar que los niveles se igualen. Error mío: verifiqué signos de las variaciones, no los niveles. | econométrico R1, pregunta 2 | 07:59 |
| R3-C2 | La regla de la tasa se repite en 07:60 y 07:62; dejar una. | econométrico R2 | 07 |
| R3-C3 | Cláusula de colinealidad confusa («no la hace significativa»); sugerencia: «infla su error estándar, de modo que no explica su significancia» o equivalente. | econométrico R5, profesor R4 | 06:51, 06:62, 09:13 |
| R3-C4 | La frase «La tabla no recoge signos» (02:55) contradice la Tabla 1 con columna «Signo y contexto»; corregir tras confirmar con Codex el contenido final de la tabla. | citas N-1, profesor R1 | 02:55-56 |
| R3-C5 | «Solo se citan estudios cuya fuente se verificó» puede leerse como lectura completa; añadir una frase sobria de alcance (muchos estudios se respaldan con el resumen; el Anexo E lo indica). Sin exigir lectura completa. | citas N-3 | 02:4 |
| R3-C6 | Quitar de la vista «Otros N estudios candidatos no se usan porque su contenido no se verificó» (o dejarlo en el Anexo E) y la coletilla «Esta subsección se apoya en 2 estudios verificados» repetida cuatro veces. | profesor N10 | 02:14, 24, 34, 45, 79 |
| R3-C7 | «ningún horizonte detecta… (ninguno)»: quitar el paréntesis redundante. | profesor N4 | 05:47 |

### De Codex

| ID | Hallazgo | Fuente |
|---|---|---|
| R3-X1 | «de los especificaciones pre-registradas» (concordancia) en 03b:8 y 11:3 (informe.md:391-392, :1801-1802). | econométrico R3, profesor R2 |
| R3-X2 | Tabla 1: pie «y signos» en `src/report_tables.py:102` / `lit_estudios_cuerpo.md`; Obradović con «—» en la columna de signos; nota de procedencia de Golitsis (R5). | citas N-1, profesor R1/R5 |
| R3-X3 | Figura 1: sin fuente ni explicación de las franjas de recesión (USREC). | profesor R3 |
| R3-X4 | Anexo: etiquetas VIF a medias (`VIF (d_ffr_l0)`, `VIF (d_ffr_l1)`, `VIF (d_unemp)` en las limitaciones); celdas p vacías en filas VIF y CUSUM de la Tabla 4 y AT-M1-DIAGNOSTICS; panel 2 de C.3 casi vacío. | econométrico R4, profesor I4 |
| R3-X5 | DOI de Zawadzki partido como «ceej- -2023-0016» (posible guion doble); revisar en el render visual. | profesor M1, econométrico |
| R3-X6 | Notas: «Cifras redondeadas a tres decimales» en Tablas 2 y 5 sin cifras; Tabla 7 con la fuente dos veces; `stress_delta_nota.md` circular («por la regla de tasa en cero»). | profesor N6, econométrico R6 |
| R3-X7 | Restos de plantilla en 03: «sea Y la morosidad en la forma primera diferencia»; remisiones repetidas a AT-LIT-ESTUDIOS, AT-M1-ROB, AT-FRED-MANIFEST. | profesor N4 |

### Sin cambio por decisión
- I5 (por qué sube el base): sigue «supuestos de calendario y de crédito»; menor. Puede quedarse.

## Lo que ningún revisor pudo verificar

- Renderizado visual del PDF (falta `pdftoppm`); el profesor evaluó sobre páginas ya renderizadas y Markdown, con paridad inferida de `docs/qa-correcciones-006-ronda4.json`.
- Los DOCX como contenido por el profesor (el econométrico leyó su texto).
- Clics reales en Word, PDF y Google Docs.
- Textos completos de los estudios citados (salvo Golitsis); no se exigió.
- **Google Docs sigue sin importarse ni verificarse: obligatorio para el cierre.**
- Reproducibilidad: no se ejecutaron tests, pipeline ni render por instrucción.

## Siguiente paso

1. Usuario/Codex: ceder turno a Claude para R3-C1–R3-C7 (cambios de texto menores, sin cifras nuevas) y a Codex para R3-X1–R3-X7.
2. Codex regenera y valida; una revisión final mínima de estos puntos, sin ampliar requisitos.
3. Importación de los DOCX a Google Docs y comprobación del autor.
4. Decisiones del usuario o del profesor pendientes: hora límite oficial, formato, duración, par informe-anexo separado y spec 007.

006 y T12 permanecen abiertas. Sin commit ni push.

---

## Anexo — Correcciones editoriales de Claude tras la ronda 3 (13-oct-2026)

Turno de escritura cedido por el usuario exclusivamente para las correcciones editoriales de la consolidación de ronda 3. Codex detenido. Antes de editar se confirmaron los prefijos de las nueve secciones (iguales a los de la cesión) y el contenido real de la Tabla 1 (`outputs/informe/lit_estudios_cuerpo.md`): tiene cinco columnas, con «Signo y contexto», donde varias filas llevan «—» (p. ej. Obradović y Grubišić, Tanasković y Jandrić, Koju et al.). Cifras, citas, contratos y decisiones metodológicas no se tocaron; no se añadió ninguna afirmación ni requisito.

| ID | Archivo | Cambio |
|---|---|---|
| R3-C1 | 07 | «menos actividad y más desempleo» → «menor crecimiento del producto y mayor aumento del desempleo»; «esa diferencia se invierte» → «el crecimiento del producto del adverso supera al del base y el aumento del desempleo es menor, aunque el nivel del desempleo sigue por encima». Respaldo: `stress_paths.csv` y la lectura del revisor econométrico (U implícito del adverso por encima del base en todo el horizonte). |
| R3-C2 | 07 | Eliminada la frase «El coeficiente de la tasa se fija en cero por la regla de la sección anterior.»; queda la formulación final del mismo párrafo. |
| R3-C3 | 06 (dos lugares), 09 | «que vuelve menos precisa su estimación pero no la hace significativa» y «que afecta la precisión de su estimación» → «que infla su error estándar y no explica su significancia». |
| R3-C4 | 02 | «La tabla no recoge signos…» → «La columna «Signo y contexto» recoge solo los signos verificables en cada estudio, y «—» indica que la tabla no los recoge.» |
| R3-C5 | 02 | Añadida: «En la mayoría de los casos la verificación se apoya en el resumen del estudio, y el Anexo E indica la base de cada uno.» (respaldada por el informe del verificador de citas de la ronda 2 y por el Anexo E). |
| R3-C6 | 02 | Eliminadas las cuatro coletillas «Esta subsección se apoya en N estudios verificados.»; el párrafo «Estudios no usados como evidencia» queda: «Los candidatos que no se pudieron verificar o que no respaldaban la subsección que los motivaba no se usan como evidencia.» (se retiran los conteos; ya no se usan en el texto las claves `literatura.por_tema.t21–t24`, `n_pendiente_lectura` y `n_descartados`, que siguen existiendo en `_variables.yml`). |
| R3-C7 | 05 | Eliminado el paréntesis `({{< var modelo2.lp_resumen.horizonte_deteccion >}})`. |

Inconsistencia que queda para Codex: la fila de Obradović y Grubišić en la Tabla 1 lleva «—» en «Signo y contexto», mientras el texto de 02 informa el signo del tipo de interés de préstamo con respaldo del resumen; tratar como R3-X2.

Verificaciones: todas las claves `var` de mis nueve archivos existen en `_variables.yml` y no hay palabras causales. No ejecuté tests, pipeline ni render. Codex debe confirmar que ningún test dependa del uso de las claves retiradas (en `tests/test_report.py:286` el valor `literatura.n_pendiente_lectura` se comprueba en la generación de variables, no en el texto).

Nota de trazabilidad: al preparar esta tanda copié por error las secciones actuales sobre mi carpeta de copias de trabajo «r2antes» del scratchpad (copias previas a las correcciones de la ronda 2). Esas copias ya no conservan el estado anterior a la ronda 2 (sí su lista de huellas en `sha.txt`); el estado anterior a esta tanda está en la carpeta «r3antes».

Huellas completas actuales (SHA-256):
- 01 `be47254ba13d3e1ec9f1e2d0e93ebc230b06d08874aeb137be602d59e0c21f4c` (sin cambio)
- 02 `273cf4bb40af8556c1c0bac5e465a51e4c36984773f160a9414aeb00e746eac9`
- 03f `8f97f714fed4d81094ba4a0f6e33ca5040bb57e11bb6d09bb6774b5adeb4f307` (sin cambio)
- 04 `8c28bfdc44afc62136dabb8a3d0cd3fdd53ae28d868dfe9c0aca81e23d940f4e` (sin cambio)
- 05 `c88be5b54a363bf31b93ef42641bff3845711b6aca683d81224770a9abba5dcf`
- 06 `0641ba45ce829b010a6127e4e0c67c1a2807a95872d6f9b45698c53c758e3839`
- 07 `f94d7332f971bcd81d1feb2ea880fbc5388462af53313471809de95ce816a4cc`
- 08 `c1404f1f992636bfd0ee7c74cc6ffe9079aba9c0b77214792a5aa1350e785891` (sin cambio)
- 09 `f24a85006086595753fb0066a43b010b6c16e466f46b5a33e74ef108eced4a84`

Turno devuelto a Codex. 006 y T12 siguen abiertas. Sin commit ni push.
