# Auditoría independiente de 006 — Ronda 2

Estado: **CAMBIOS NECESARIOS** (2 de 3 revisores). Ronda 1 conservada intacta en `review-audit.md` y `review-audit-ronda1-*.md`; no se reabre lo resuelto.

## Autoría y coordinación

- Informe auditado: Claude Code redactó 01, 02, 03f, 04, 05, 06, 07, 08, 09; Codex redactó 3a–3e, 10, 11, tablas, figuras, variables, render, anexos A–F, registro, filtros y bibliografía.
- Coordinación de la ronda 2: Claude Code, por relevo del usuario. **La coordinación no es auditoría independiente de mi propio texto.** La independencia procede de tres revisores de contexto limpio, a los que solo se dieron rutas y criterios, más sus propios hallazgos de la ronda 1 como punto de partida. No recibieron conclusiones mías.
- Informes en copia (texto tal cual lo entregó cada subagente; las entidades HTML `&lt;`, `&gt;`, `&amp;` llegaron así en la notificación):
  - `review-audit-ronda2-revisor-econometrico.md` — CAMBIOS NECESARIOS.
  - `review-audit-ronda2-verificador-citas.md` — APROBADO.
  - `review-audit-ronda2-profesor-evaluador.md` — CAMBIOS NECESARIOS (89/100 estimado; 79 en la ronda 1).

## Versión auditada (entregada por Codex, T11 técnica aprobada con 940 passed)

| Archivo (`outputs/preview-006/report/`) | SHA-256 verificado por Claude antes de lanzar |
|---|---|
| informe.pdf | 97c614ac758bed6b6f38e42deeac965277a11f8bbb5d9744d10fc8bcbc1042d7 |
| anexo-tecnico.pdf | b69f250d36f2172c9f4944ad55a15f0feb3c33389602b9287795a82bad2a21fe |
| informe.docx | 8d212275b52d3ece6b30255433fdab65e2323f8272ed486dc1c404f040393520 |
| anexo-tecnico.docx | 136fb3c808b3bf4a607be5bc3bb008928387b84a1f95d3a25fa570f1433ab274 |

Secciones de Claude: coinciden con las huellas comunicadas; 07 = b4c305b74d4c3dfcac0ce90531b86c297b2276344326772e8ce1ca57b6d66b42.

## Veredictos

| Revisor | Veredicto | Resumen |
|---|---|---|
| revisor-econometrico | CAMBIOS NECESARIOS | 17 hallazgos de ronda 1: 11 resueltos, 4 parciales (1, 3, 4, 11), 2 con regresión menor. 5 importantes nuevos (N1–N5) y 7 menores. Cifras del cuerpo coinciden con los CSV (213 valores). |
| verificador-citas | APROBADO | 10 hallazgos corregidos, 1 cambiado sin poder confirmar (páginas de Newey y West, 703–708). 3 observaciones menores. |
| profesor-evaluador | CAMBIOS NECESARIOS | B2 resuelto; B1 parcial (texto interno); estrés sin explicar origen; fecha de portada; APA. |

## Hallazgos vigentes y escritor propuesto

Cada corrección de texto exige turno exclusivo cedido por el usuario o por Codex; no se hace sin él.

### Bloqueantes o importantes

| ID | Hallazgo | Fuente | Archivos | Escritor |
|---|---|---|---|---|
| E-N1 | La 6.3 no informa PIB(t−1) del Modelo II (+0,001; p 0,823, signo opuesto al Modelo I) y la conclusión dice que el ciclo opera «sobre todo» por la actividad acumulada, con respaldo solo del Modelo I (impacto p 0,110; largo plazo p 0,043; robustez 3 de 9). | econométrico | 06:48-52, 06:60, 09:3, 09:12-13, 08:3 | Claude (06, 08, 09). Cifras solo con `{{< var … >}}`; verificar que existe la clave del coeficiente de PIB(t−1) del Modelo II en `_variables.yml` (si no existe, lo debe añadir Codex). |
| E-N2 | La regla pre-registrada de la tasa en cero se presenta como «ante su signo contrario al esperado» (07:59, 06:84). La regla real (spec 005, RF-9) es: ΔFFR = 0 mientras la lectura de la 004 no sea «evidencia fuerte»; 07:43 ya lo dice bien. Coincide con N9 del profesor (dos justificaciones). | econométrico, profesor | 07:59, 06:84 | Claude (06, 07). |
| E-N3 | Notación del KPSS acotado no única: «≥ 0,10» (7 veces en anexo) frente a «> 0,10» (58 veces); incumple spec 006:82. | econométrico | `outputs/informe/model1_stationarity_anexo_2.md`, adaptador, anexo A | Codex. |
| E-N4 | 05:75-80 dice que dos variantes tratan los dos primeros «límites de potencia»; falso: R3 trata la tasa cero, R2 (sin 2020–2021) trata COVID/efectos base, ninguna trata K (R1 «no aplica»); además K condicional y efectos base no son límites de potencia. | econométrico | 05:75-81 | Claude (05). |
| E-N5 / P-I1 / P-N3 | El párrafo de estrés de 07 (:56-59) nombra solo el desempleo y presenta inflación y crédito como las asociaciones «más estables», lo que insinúa un origen del cambio que los signos no sostienen (crédito idéntico en ambos escenarios, inflación baja en el adverso con coeficiente positivo). El profesor propone explicar en cualitativo la dirección de cada regresor. | econométrico, profesor | 07:56-59 | **Decisión del usuario.** El usuario ordenó retirar todo reparto cuantitativo y cualitativo del cambio de 07 porque no está respaldado por una salida aprobada. Opciones: (a) borrar solo la frase que sugiere el origen; (b) sustituirla por una lectura de signos sin cifras, que toca el límite de «no descomponer» y requiere aprobación expresa. Claude no lo cambia sin esa decisión. |
| P-N1 / P-B1 | Texto interno en el cuerpo: «Modelo I (spec 003)»/«Modelo II (spec 004)» (Tabla 6), nota de Tabla 7 («regla heredada», «modelo1», «modelo2»), «contratos aprobados» en 3.2 y 11, introducción («Las cifras se generan por código… ninguna se escribe a mano»), sección 11 («Google Docs», «gancho previo al render», «espejo generado», «procedimiento aprobado»). | profesor | tablas generadas, 03a–e, 11, 01 (frase de la introducción) | Codex (tablas, 03, 11); Claude (frase de 01). |
| P-N5 / V-N2 | APA: nombres propios en minúscula («the u.s. lending standards», «in malaysia»), minúscula tras dos puntos, títulos en mayúscula de título (2026 Stress Test Scenarios, Nkusu, Segoviano), «Series DRALACBS…» colgando tras la URL de FRED, «non-/-performing» partido. | profesor, citas | `report/references.bib`, `report/apa.csl`, filtros | Codex. |

### Menores

| ID | Hallazgo | Fuente | Escritor |
|---|---|---|---|
| E-N6 | «de forma estable» (06:3, 06:97, 08:9, 04:96) mientras el Chow rechaza estabilidad conjunta (2008T3, 2020T2); mejor «robusta a las variantes». | econométrico | Claude. |
| E-N7 / P-N4 | Letra del anexo duplicada (p. ej. «Anexo B, AT-M1-COEFFICIENTS, Anexo B», «Anexo D, Anexo D, AT-EST-LIMITATIONS»; unas 30 veces); origen: el filtro antepone la letra y mi prosa ya la escribe. Enlaces sin distinción visual en el PDF. | econométrico, profesor | Codex (filtro/estilo) y, si procede, Claude (01:42, 07:125). |
| E-N8 | Bandas de LP: el límite superior al 90 % en h = 1–3 queda casi en el borde de cero; conviene decirlo y ligarlo a la endogeneidad. | econométrico | Claude (05:47). |
| E-N9 | «Alerta de colinealidad» usada para atenuar un coeficiente significativo (06:50, 06:61, 09:13); un VIF alto infla el error estándar. | econométrico | Claude. |
| E-N10 | El cuerpo no dice que las ventanas de las LP cruzan la COVID sin dummy. | econométrico | Claude (05). |
| E-N11 | 08:16: lógica de «se monitorea… porque varió poco fuera de la pandemia». | econométrico | Claude. |
| E-N12 | 02:3 dice que la literatura «respalda» la relación política monetaria-riesgo de crédito, pero 2.3 y 2.4 dicen que ningún estudio mide la morosidad. | econométrico | Claude (02). |
| E-11 | Tabla 4 con «VIF (y_lag)», «VIF (gdp_growth)», celdas VIF vacías; «modelo1/modelo2» en la nota de Tabla 7. | econométrico, profesor | Codex. |
| V-N1 / P-N7 | Tabla 1 titulada «…variables, métodos y signos» sin columna de signos; 02:51 repite «Anexo E, AT-LIT-ESTUDIOS, Anexo E». | citas, profesor | Codex (título); Claude (02:51). |
| V-N3 / P-N10 | Declarar de forma sobria el alcance de la verificación de fuentes (solo Golitsis leído completo; resto por resumen) y quitar de la vista las fórmulas «pendientes de lectura» y «no detallados en el resumen leído». | citas, profesor | Claude (02), Codex (Anexo E). |
| P-2.5 | Reportar qué halla Obradović y Grubišić (2026) sobre política monetaria y morosidad. | profesor | Claude (02), solo con lo verificado en la matriz. |
| P-N6 | Nota fija «KPSS conserva sus límites de censura» en todas las tablas, también donde no procede. | profesor | Codex. |
| P-N8 | Fuente duplicada dentro y bajo las figuras; línea del adverso tapada por la del escenario D (leyenda sin línea visible). | profesor | Codex. |
| P-I4 | Anexo: columna «Fila de origen» (AT-STATIONARITY), nombres de código en VIF, «Modelo I (spec 003)» en C.5, paneles casi vacíos (B.2). | profesor | Codex. |
| P-M2 | AT-DESCRIPTIVES sin identificador; sin figura de DRALACBS en el cuerpo. | profesor | Codex. |
| P-N4 | Plantilla: «entra en primera diferencia… y en primera diferencia» (3.2), «en la forma primera diferencia» (3.5), «(ninguno)» (pág. 18). | profesor | Codex (03), Claude (si está en 05). |
| P-11 | La sección 11 no muestra la llamada a `pandas_datareader` que pide la guía. | profesor | Codex. |

### Decisiones del usuario o del profesor

- **Fecha de portada (P-N2):** el revisor nota que `AGENTS.md` fija la entrega el 15 de octubre y la portada dice 16. El usuario autorizó el 16 de octubre de 2026 para la portada; no se cambia salvo instrucción. No es la hora límite oficial, que sigue pendiente de confirmación.
- **Estrés (E-N5):** ver arriba.
- **Newey y West 703–708:** no confirmado por fuente consultada; contrastar a mano con la fuente (Codex o el autor).

## Contradicciones y puntos para depurar entre revisores

- El profesor pide explicar en cualitativo la dirección de cada regresor del adverso; el usuario ordenó retirar ese tipo de reparto. Se trata como decisión pendiente, no como corrección.
- El revisor econométrico y el profesor observan que los PDF son anteriores a la regeneración de `outputs/informe/*.md` y `_variables.yml` (01:15). Ambos comprobaron que los valores presentes en el PDF coinciden con los actuales en lo que contrastaron, pero no el anexo completo. Pregunta para Codex: confirmar que los PDF/DOCX con las huellas anteriores son posteriores a esa regeneración (o regenerar y recomputar huellas).

## Lo que ningún revisor pudo verificar

- Renderizado visual del PDF (falta `pdftoppm`): el profesor evaluó sobre páginas ya renderizadas y los Markdown generados; no se comprobó por huella que correspondan al PDF vigente.
- Los DOCX no se leyeron como contenido por el profesor; el econométrico leyó su texto.
- Clics reales en PDF, Word y Google Docs; FRED en vivo; textos completos de la mayoría de los estudios citados; reproducibilidad (`pytest`, doble corrida), por instrucción.
- **Google Docs sigue sin importarse ni verificarse: obligatorio para el cierre.**

## Siguiente paso

1. Usuario/Codex: decidir E-N5 y confirmar la regla de turnos.
2. Cesión de turno exclusivo a Claude para sus nueve secciones (E-N1, E-N2, E-N4, E-N6, E-N8–E-N12, 01, 02) y a Codex para tablas, filtros, anexos, APA, 03a–e y 11.
3. Regeneración y validación por Codex; ronda 3 restringida a las correcciones y sus regresiones.

006 y T12 permanecen abiertas. Sin commit ni push.

---

## Anexo — Correcciones de Claude tras la ronda 2 (13-oct-2026)

Autorización del usuario: corregir los hallazgos de la ronda 2 en las secciones de Claude; para 07, lectura de signos sin cifras respaldada por los términos del modelo y las trayectorias aprobadas, sin descomposición cuantitativa, sin «la mayor parte» y sin atribuciones causales (esto sustituye la restricción anterior sobre toda lectura cualitativa, por solicitud coincidente de los dos revisores). Fecha de portada: se mantiene 16 de octubre de 2026, autorizada; la hora límite oficial sigue sin confirmarse y no se cambia la portada por la fecha del calendario interno.

Estas correcciones son de autoría de Claude y **no están validadas ni auditadas**: requieren regeneración y validación por Codex y revisión acotada independiente. Copias previas en el scratchpad de la sesión (no versionadas).

| Hallazgo | Archivo | Cambio | Verificación previa |
|---|---|---|---|
| E-N1 | 06, 09, 08, 04 | Se informa PIB(t−1) del Modelo II (signo positivo, opuesto al del Modelo I, sin distinción de cero); la actividad se presenta con respaldo más débil, solo del Modelo I. | `model2_coefficients.csv` (gdp_l1) y `_variables.yml` (`modelo2.coef.gdp_l1`, `modelo1.robustez.gdp_growth`). |
| E-N2 / P-N9 | 06, 07 | La regla de tasa en cero se atribuye a la lectura del Modelo II («cero mientras no haya evidencia fuerte»), no al signo. | spec 005 RF-9; 07 ya la decía bien en la sección «La regla de la tasa». |
| E-N4 | 05 | Clasificación de limitaciones: la tasa cero es límite de potencia; K condicional y efectos base son de inferencia/especificación; R3 trata la tasa cero, R2 el efecto base, ninguna K (AIC y BIC coinciden). | `model2_limitations.csv`, `model2_robustness_estimates.csv`. |
| E-N5 / P-I1 / P-N3 | 07 | Lectura de signos sin cifras: el crédito no contribuye al contraste bajo el supuesto compartido; la inflación es menor en el adverso y, con coeficiente positivo, resta; actividad y desempleo adversos en los primeros trimestres con el signo que se asocia con más morosidad, y la diferencia se invierte hacia el final; cautela por la robustez de producto y desempleo. | Comprobado sobre `stress_paths.csv` (Modelo I): crédito idéntico en los 13 trimestres, inflación estrictamente menor en los 13, producto y desempleo adversos hasta 2028T3 y 2028T1, respectivamente. En el Modelo II la inflación no es menor en todos los trimestres: el párrafo es solo del Modelo I. No se verificó la ecuación de estado ni `src/`. |
| E-N6 | 04, 06, 08 | «de forma estable» → «robusta a las variantes». | Chow rechaza estabilidad conjunta. |
| E-N8, E-N10 | 05 | Límite superior de las bandas de proyecciones locales en h = 1–3, y ventanas que tocan 2020T2–2021T1 sin dummy. | `_variables.yml` (`modelo2.lp.h1..h3.ic90_sup`), `model2_limitations.csv`. |
| E-N9 | 06, 09 | La alerta de VIF afecta la precisión; no se usa para atenuar la significancia. | — |
| E-N11 | 08 | Lógica de la frase del desempleo corregida. | — |
| E-N12, P-2.5, V-N3/P-N10 | 02 | Se quita «respalda»; se quitan «pendientes de lectura»; se añade lo que halla Obradović y Grubišić (tipo de interés de préstamo, no de política). | `research/matriz-literatura.md` (resumen leído). |

No tocado (de Codex o pendientes): notación KPSS, textos internos de tablas y de 3.x/11, APA, remisiones con letra duplicada, Tabla 1 y su título, figuras, nota de KPSS repetida, anexo. Sin verificar por mí: render y reproducibilidad (no ejecuté tests, pipeline ni render). El rango 703–708 de Newey y West sigue sin confirmación; los datos bibliográficos pendientes quedan para la verificación acotada.

### Segundo turno de Claude (13-oct-2026), a petición de Codex

Se quitaron 19 sufijos de letra de anexo junto a identificadores (`**AT-…**, Anexo B`, `**AT-…** (Anexo B)`, y «en el Anexo D, **AT-…**» en 07) en 01, 02, 03f, 04, 05 y 07, para que el filtro `slug-links.lua` anteponga la letra una sola vez. Se retiró lenguaje interno de la prosa: 01 («Las cifras se generan por código desde los resultados aprobados; ninguna se escribe a mano»), 03f («resultados aprobados»), 07 («salida aprobada», «regla heredada»). Sin cambios en 06, 08 y 09. No se ejecutó render ni test: el efecto sobre el texto generado queda para la validación de Codex.
