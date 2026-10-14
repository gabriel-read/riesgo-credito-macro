# Clarificación de la spec 006-informe contra la guía oficial

Claude Code, 12-oct-2026. Revisión de `specs/006-informe/spec.md` (v1) frente a `docs/guia-profesor.md` (sección por sección), `docs/constitution.md`, la skill `informe-quarto` y las decisiones del autor del 12-oct. Es una lista de hallazgos; las correcciones que no son decisiones del autor se aplicaron después en la v2 de la spec. Las decisiones y pendientes se listan al final.

## Cobertura de la guía
| Sección de la guía | Cubierta en la spec | Hallazgo |
|---|---|---|
| Título propuesto | No (v1) | **C1.** La guía propone un título; la spec no exigía usarlo. Corregido: RF-1 y «Estructura obligatoria». |
| Pregunta de investigación y objetivo (1) | Parcial | Corregido en RF-1: van en la sección 1. |
| 2.1–2.5 | Sí | La guía no fija mínimos de estudios; los mínimos de la matriz son criterio interno de la spec 002. 2.5 pide variables y metodología por estudio: RF-3 la tabla generada desde la matriz. |
| 3.1–3.5 | Sí | **C2.** La tabla de variables de la guía usa GDP nominal y el informe usa GDPC1; la «tasa de interés» (3.3) y el «cambio de la FFR» (3.4) son una misma variable (ΔFFR); el crédito es una serie elegida (LOANS); el período termina en 2026T2 y no en 2026-01-01. Corregido: RF-7. |
| 4 Modelo I | Sí | RF-5b: responde la pregunta específica y la interpretación desde la gestión de riesgos. |
| 5 Modelo II | Parcial | **C3.** La guía habla de «un shock de política monetaria» y de «efectos rezagados»; el Modelo II usa ΔFFR observada, no un shock identificado. Corregido: RF-5b exige aclararlo y responder «¿existen efectos rezagados?» con la lectura de la 004. |
| 6.1–6.4 | Sí | RF-8 y RF-9. **C4.** La pregunta de la guía usa «afectan»; el informe debe responder y explicar que se lee como asociación. Corregido: RF-5b y RF-9. |
| 7 Escenarios | Sí | **C5.** El ejemplo de la guía incluye «aumento de la tasa»; el adverso de la Fed baja la tasa. Cubierto por el escenario D de la spec 005 y por el hallazgo heredado de la sección 7. |
| 8 Implicaciones | Sí | **C6.** La guía conecta la sección con un resultado de aprendizaje (identificar, medir, monitorear y gestionar riesgos). Corregido: RF-10. Los siete puntos están en RF-10 y en el tablero. |
| 9 Conclusiones | Sí | RF-11: responde la pregunta y dice cómo anticipar y gestionar; sin el formato prohibido. |
| 10 Referencias | Sí | RF-4: APA 7 solo desde `references.bib`. |
| 11 Base de datos | Parcial | **C7.** La guía anuncia un notebook proporcionado por el profesor y el fragmento con `pandas_datareader` y fin en 2026-01-01; el proyecto usa su propio pipeline. Corregido: RF-13 y «Fuera de alcance». |

## Hallazgos de contexto y alcance
- **C8. Hora, fecha y formato.** La guía no fija hora de entrega, extensión, formato de archivo ni formato de la exposición. La spec v1 los trataba como pendientes; en la v2 se declaran explícitamente pendientes de confirmación con el profesor y no como requisitos.
- **C9. Independencia de la auditoría.** La decisión de que Claude redacte interpretación, discusión, limitaciones y conclusiones choca con que Claude audite la 006 (principio de la skill SDD: no calificar el propio trabajo). La spec v2 lo declara y propone auditoría con subagente de contexto limpio, validación de Codex, verificador de citas y evaluador de rúbrica; sigue como duda para el autor.
- **C10. Propiedad de archivos.** La spec v2 exige que el plan asigne un escritor único por archivo de sección y proteja `informe.qmd`, `_quarto.yml`, `_variables.yml` y `references.bib` para Codex.
- **C11. Disposición del proyecto Quarto.** La prueba de humo mostró que Typst no lee `../outputs/` si la raíz es `report/` y que `{{< var >}}` solo lee `_variables.yml` en la raíz del proyecto (`docs/entorno-quarto-2026-10-12.md`). El contrato actual (`report/_variables.yml`, skill `informe-quarto`) y el PDF son incompatibles sin una de las dos disposiciones. No exige reabrir ninguna spec cerrada; el plan debe elegir y, si tocara un contrato aprobado, presentar `change`.
- **C12. `apa.csl`, `_quarto.yml` e `informe.qmd` no existen.** Procedencia y huella del CSL registradas en el documento de entorno.
- **C13. Datos inconsistentes ya conocidos.** `datos.n_series` (12) frente a la referencia FRED con 13 series: incluida como hallazgo heredado y tarea de la etapa `report`.
- **C14. Dependencia de la 005.** La sección 7 y parte de 8 y 9 dependen de la 005 validada y auditada; la spec lo marca y define el comportamiento si no llega a tiempo.
- **C15. Cifras en las limitaciones.** Los hallazgos heredados citan algunas magnitudes (por ejemplo φ_h ≈ 3); el informe las debe tomar de `_variables.yml`, no copiarlas de este texto.

## Dudas que quedan para el autor (ver `spec.md`, «Dudas abiertas»)
1. Disposición del proyecto Quarto (C11).
2. Aceptar la auditoría con subagente limpio más validación de Codex, o que Codex audite lo que Claude redacta (C9).
3. Confirmar con el profesor la fecha y hora oficiales, la extensión, el formato exigido y el de la exposición (C8).
