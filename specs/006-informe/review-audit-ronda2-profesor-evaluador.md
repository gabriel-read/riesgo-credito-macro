# Ronda 2 — profesor-evaluador (contexto limpio)

Copia del mensaje final del subagente `profesor-evaluador`, tomada del texto recibido en la notificación de finalización (las entidades `&lt;` y `&amp;` son tal como llegaron). Coordinó Claude Code; autoría del informe auditado: Claude (01, 02, 03f, 04–09) y Codex (3a–3e, 10, 11, tablas, figuras, anexos, infraestructura). Versión auditada: informe.pdf 97c614ac…, anexo-tecnico.pdf b69f250d…, informe.docx 8d212275…, anexo-tecnico.docx 136fb3c8…. Limitación declarada por el revisor: no pudo renderizar el PDF y evaluó sobre páginas renderizadas en `outputs/preview-006/qa-ronda3-final-*` y los Markdown generados.

# Evaluación del informe 006, ronda 2 (profesor evaluador)

**VEREDICTO: CAMBIOS NECESARIOS.** Son correcciones editoriales y de presentación, no de econometría. Los dos bloqueantes de la ronda 1 (B1 y B2) quedan resueltos en lo esencial. Pero siguen apareciendo en el cuerpo textos internos del proyecto que un profesor ve enseguida, la fecha de portada es posterior al plazo y el estrés todavía no explica de qué variables sale su resultado.

**Qué leí.** El PDF no se puede renderizar aquí porque falta `pdftoppm`. Evalué con dos fuentes:
- Las páginas renderizadas más recientes: `outputs/preview-006/qa-ronda3-final-principal/` (34 págs.) y `qa-ronda3-final-anexo/` (más de 150 págs.).
- Los Markdown generados en el mismo render: `outputs/preview-006/report/informe.md` y `anexo-tecnico.md`. Coinciden con las páginas que comparé.

## Evaluación por sección

| Sección | Calificación | Por qué |
|---|---|---|
| 1 | Cumple | Problema, relevancia, pregunta y objetivo literales, y lenguaje de asociación desde el inicio. |
| 2.1–2.4 | Cumple parcialmente | Siguen con 2 estudios cada una. La coletilla «se apoya en 2 estudios verificados» se repite como si fuera una lista de control. |
| 2.5 | Cumple | La Tabla 1 y el texto explican variables, métodos y signos verificables. Faltan dos cosas: qué halla Obradović y Grubišić (2026), y Nkusu aparece con «no detallados en el resumen leído». |
| 3.1–3.4 | Cumple | Series, frecuencia, período, vintage, hueco de octubre de 2025 y desviaciones. |
| 3.5 | Cumple | Ya hay ecuaciones del Modelo I, del Modelo II y de las proyecciones locales. La redacción tiene restos de plantilla (ver N4). |
| 4 | Cumple | Estima, interpreta en pp y por desviación estándar, separa impacto de largo plazo, hace robustez y diagnósticos, y cierra con lectura de gestión. |
| 5 | Cumple | La robustez sin pandemia (n = 97) y sin tasa cero (n = 69) ya está en el cuerpo, con la lectura de φ y la endogeneidad. |
| 6.1–6.3 | Cumple | 6.3 está corregida: describe bien los controles y presenta el desempleo como evidencia mixta (0,110; p 0,039). |
| 6.4 | Cumple | Responde por separado al entorno macro (relevante por inflación y crédito) y a la política monetaria (sin asociación propia), y contesta las preguntas probables. |
| 7 | Cumple parcialmente | Construye el escenario adverso, lo compara con el base, calcula el cambio y lo sitúa frente a la historia. No dice en qué dirección empuja cada variable. La línea del adverso sigue tapada por la del escenario D. |
| 8 | Cumple | Cubre los siete puntos, tiene tablero y conecta con el resultado de aprendizaje de la asignatura. |
| 9 | Cumple | Responde la pregunta y dice cómo anticipar, dimensionar y gestionar, sin el formato prohibido. Ya integra el desempleo del Modelo II. |
| 10 | Cumple parcialmente | Mejora mucho, pero hay errores nuevos al pasar a minúscula de oración (N5). |
| 11 | Cumple parcialmente | Explica el pipeline y la reproducción, pero conserva texto interno (Google Docs, «gancho», «espejo») y no muestra la llamada a `pandas_datareader` que pone la guía. |
| Diapositivas | No evaluable | `report/slides.qmd` no existe (corresponde a la spec 007). |

## Hallazgos de la ronda 1: estado actual

| Hallazgo | Estado | Evidencia |
|---|---|---|
| B1 Aspecto de borrador y portada | **Parcial** | **Resuelto:** portada con autor, INTEC, curso, profesor y fecha (pág. 1). Ya no aparecen «Versión de trabajo», «Abrir anexo», «URLs ficticias», «no repite su encabezado» ni «(primera diferencia)» repetido. **Pendiente:** Google Docs, «gancho previo al render», «espejo generado» y «procedimiento aprobado» siguen en la sección 11 (`informe.md:1788-1822`). Hay residuos nuevos (N1–N4). |
| B2 Error en 6.3 e integración de controles | **Resuelto** | 6.3 describe bien qué comparte cada modelo y reporta inflación (0,024; p 0,015), crédito (0,007; p 0,009) y desempleo (0,110; p 0,039) del Modelo II (`informe.md:1024-1084`). La sección 4, la 6.4 y la conclusión dicen «evidencia mixta». |
| I1 Asimetría del estrés y origen del resultado | **Parcial** | **Añadido:** el párrafo «De dónde sale el cambio del Modelo I» (pág. 24) admite que no hay descomposición, que el crédito es igual en ambos escenarios y que el desempleo es débil (1 de 9). **Pendiente:** no dice que la inflación baja en el adverso y, con coeficiente positivo, resta al cambio. Tampoco justifica la asimetría entre usar el desempleo y anular la tasa; solo la enuncia. La línea roja sigue oculta (pág. 25). |
| I2 Robustez del Modelo II en el cuerpo | **Resuelto** | `informe.md:943-956`: n = 97 y 69, p 0,303 y 0,293, con la nota de menor potencia. |
| I3 Sin ecuaciones | **Resuelto** | Págs. 10–11: tres bloques de ecuaciones con la definición de Z, β y φ. |
| I4 Anexo difícil de usar | **Mayormente resuelto** | Los paneles conservan columnas de identificación (AT-EST-DELTA ya trae Modelo, Escenario y Trimestre) y no quedan notas «spec 001» ni rutas CSV como fuente. **Pendiente:** columna «Fila de origen» con índices 0–33 (AT-STATIONARITY), nombres de código en VIF (`gdp_growth`, `d_ffr_l0`), «Modelo I (spec 003)» en C.5, y paneles casi vacíos (B.2, panel 2). |
| I5 Magnitudes en contexto de riesgo | **Resuelto** (salvo un detalle) | Contexto histórico: último dato 1,42 %, media 2,63 %, máximo 7,35 % en 2010T1 (`informe.md:1308-1316`). Efectos por desviación estándar en la sección 4. La subida del base solo se explica con «supuestos de calendario y de crédito», sin decir cuál pesa. |
| M1 APA 7 | **Parcial** | **Corregido:** raya en rangos, Newey y West 703–708, fecha de consulta de FRED, números de los documentos del FMI, «Tabla N» con título, y la Fed ya no figura dos veces. **Errores nuevos:** ver N5. |
| M2 Inconsistencias menores | **Mayormente resuelto** | El p del crédito sale «&lt; 0,001» en tabla y texto. Ya hay remisión a AT-LIT-ESTUDIOS, AT-EST-RATE-SENSITIVITY, AT-EST-ORIGIN y AT-M2-ROBUSTNESS-SUMMARY. **Pendiente:** AT-DESCRIPTIVES se menciona sin identificador, y la serie dependiente sigue sin figura en el cuerpo. |

## Hallazgos nuevos o que siguen sin corregir

**Importantes**

- **N1. Texto interno en tablas y notas del cuerpo.**
  - La Tabla 6 rotula las filas como «Modelo I (spec 003)» y «Modelo II (spec 004)» (pág. 20; `informe.md:1041-1042`).
  - La nota de la Tabla 7 dice «regla heredada», «modelo1» y «modelo2» (pág. 24).
  - La 3.2 y la 11 hablan de «contratos aprobados».
  - La introducción dice «Las cifras se generan por código… ninguna se escribe a mano» (pág. 4). Es una regla del proyecto, no un contenido para el lector.
- **N2. Fecha de portada «16 de octubre de 2026» en informe y anexo.** `AGENTS.md` fija la entrega el jueves 15 de octubre. La fecha viene literal del YAML (`report/informe.qmd:6`). Si el autor la eligió a propósito, hay que confirmarlo con él. Si no, la portada fecha la entrega un día tarde.
- **N3. El estrés contradice el tablero sin explicarlo.**
  - El tablero (sección 8) presenta la inflación al alza como alerta.
  - En el adverso de la Fed la inflación baja y, por el coeficiente positivo, reduce la morosidad proyectada.
  - El crédito, el mejor indicador anticipado, no aporta nada al estrés porque es igual en ambos escenarios.
  - Desde la gestión de riesgos es la mayor debilidad que queda. Se puede explicar cualitativamente con AT-EST-PATHS, sin cifras nuevas.

**Menores**

- **N4. Restos de plantilla y redundancias.**
  - «entra en primera diferencia en el Modelo I y en primera diferencia en el Modelo II» (3.2).
  - «sea Y la morosidad en la forma primera diferencia» (3.5).
  - «ningún horizonte detecta una respuesta distinta de cero (ninguno)» (pág. 18).
  - Remisiones duplicadas del tipo «Anexo B, AT-M1-DIAGNOSTICS, Anexo B» o «AT-M1-COEFFICIENTS (Anexo B)», unas 30 veces.
  - En el PDF los enlaces no se distinguen del texto (negro, sin subrayado): el lector no sabe que puede hacer clic.
- **N5. Errores APA nuevos.**
  - Nombres propios pasados a minúscula: «the u.s. lending standards» (Maddaloni &amp; Peydró) y «in malaysia» (Tan &amp; Tang).
  - Minúscula tras dos puntos («: a dynamic panel…», «: the credit channel…»), cuando APA 7 pide mayúscula.
  - Títulos que siguen en mayúscula de título: «2026 Stress Test Scenarios», Nkusu y Segoviano.
  - La referencia de FRED cuelga «Series DRALACBS…» después de la URL.
  - Partición de palabra «non-/-performing» con guion doble (Koju, pág. 32).
- **N6. Nota fija impertinente en todas las tablas.** Todas repiten «Los p-valores… KPSS conserva sus límites de censura», incluso el manifiesto (Tabla 2), el estrés (Tabla 7) y la lectura del Modelo II (Tabla 5).
- **N7. La Tabla 1 promete signos que no tiene.** Se titula «…variables, métodos y signos», pero no tiene columna de signos (el propio texto lo admite).
- **N8. Fuente duplicada en las figuras.** Figuras 1–3: la fuente aparece dentro de la imagen y otra vez en el pie. La leyenda incluye «Adverso adaptado» con una línea invisible.
- **N9. Dos justificaciones de la regla de la tasa en cero.** En una parte del texto es «mientras la lectura no sea de evidencia fuerte». En otra, «ante su signo contrario al esperado» (pág. 24). Hay que unificarlas.
- **N10. Estudios sin leer, a la vista.** La 2.5 declara 8 estudios «pendientes de lectura» y Nkusu «no detallado en el resumen leído». Esto resta credibilidad sin aportar nada al lector.

## Nota estimada: 89/100 (79 en la ronda 1)

| Criterio | Peso | Puntos |
|---|---|---|
| Estructura de 11 secciones | 10 | 9,5 |
| Pregunta y objetivo | 5 | 5 |
| Uso de literatura | 15 | 12 |
| Datos y metodología | 10 | 9 |
| Modelo I | 12 | 11,5 |
| Modelo II | 12 | 11 |
| Integración de resultados (6) | 8 | 7,5 |
| Estrés | 10 | 8 |
| Implicaciones de gestión | 8 | 7,5 |
| Conclusiones | 5 | 5 |
| APA | 3 | 2,25 |
| Claridad y edición | 2 | 1,25 |

Sube por las ecuaciones, la corrección de 6.3, la robustez del Modelo II y el contexto histórico. Pierde por texto interno, APA y un estrés cuyo origen no se explica. Con las mejoras 1–3 llegaría a 92–94.

## Las 5 mejoras de mayor impacto

1. **Limpieza editorial.** Quitar el texto interno (N1, N4 y la sección 11), dejar una sola remisión por identificador y confirmar la fecha de portada (N2).
2. **Estrés.** Explicar en cualitativo la dirección de cada regresor en el adverso: producto y desempleo suman, la inflación resta, el crédito no aporta. Justificar la asimetría desempleo/tasa y discutir la tensión con el tablero y la ausencia de un escenario estanflacionario (I1, N3).
3. **APA 7.** Corregir nombres propios en minúscula, mayúscula tras dos puntos, títulos en mayúscula de título y el sufijo «Series…» de FRED (N5).
4. **Literatura.** Reportar qué halla Obradović y Grubišić sobre política monetaria y morosidad. Quitar las admisiones de «resumen leído» y «pendientes de lectura». Reforzar 2.1–2.4 (N10, N7).
5. **Tablas y figuras.** Notas pertinentes por tabla (N6), etiquetas VIF en español, línea del adverso visible o rotulada «coincide con D», una sola fuente por figura, y una figura de DRALACBS en el cuerpo (N8, M2).

## Las 5 preguntas más difíciles para la exposición

1. La inflación es su variable más robusta, y en su adverso baja y reduce la morosidad proyectada. ¿Qué daría una estanflación y por qué no la corrió?
2. Usa el coeficiente no significativo del desempleo (robusto en 1 de 9) y anula el de la tasa. ¿Cuánto de los +1,43 pp depende del desempleo? ¿No es elegir los coeficientes que convienen?
3. El crecimiento del crédito es su mejor alerta temprana, pero aporta cero al estrés porque es igual en ambos escenarios. ¿Cómo lo integraría un banco en su planificación de capital?
4. El pronóstico dinámico del Modelo I es peor que el ingenuo (cociente 1,625). ¿Por qué confiar en una proyección de 13 trimestres con ese mismo modelo?
5. ¿Cómo convierte +1,43 pp de morosidad en provisiones? ¿La tasa de morosidad es una PD? ¿Qué LGD y EAD usaría?

## Lo que no pude verificar

- **El PDF y su paridad con las páginas.** No pude renderizarlo. Asumo que `qa-ronda3-final-*` corresponde al PDF actual por nombre y orden, pero no lo comprobé byte a byte. Conviene contrastarlo con `docs/continuidad-validacion-006-ronda3.md`.
- **Los DOCX.** `informe.docx` y `anexo-tecnico.docx` son binarios y no los pude leer.
- **Que los enlaces funcionen al hacer clic** (`anexo-tecnico.pdf#nameddest=…&amp;page=N`), en PDF, Word o Google Docs.
- **El anexo completo.** Lo revisé por muestreo (A.1–A.2, B.2, D.1 y los resultados de búsquedas), no página a página.
- **El plazo real.** Si el 16 de octubre es una decisión expresa del autor.
- **Las diapositivas**, porque no existen.
