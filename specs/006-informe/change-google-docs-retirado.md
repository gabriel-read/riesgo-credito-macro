# Solicitud de cambio — Spec 006: Google Docs deja de ser requisito de cierre

Estado: **diff APROBADO por Gabriel en un mensaje del 2026-10-13 posterior a la corrección de registros (no retrospectivo); pendiente de aplicar por Codex** con el relevo `relevo-codex-change-google-docs.md`. Aprobación literal: «Apruebo también el diff previamente revisado de change-google-docs-retirado.md. Entrega a Codex el relevo para aplicarlo conservando el historial y R7 intacto. No marques cumplido el ensayo del autor.» Historial: un registro previo decía «diff aprobado» antes de que existiera esa aprobación y se corrigió el mismo día. Corrección del 2026-10-13: un registro anterior de este archivo decía «diff aprobado»; era incorrecto. Gabriel expresó la intención de retirar Google Docs como requisito, pero el diff de abajo todavía no fue aprobado. El relevo preparado (`relevo-codex-change-google-docs.md`) queda en espera y no debe ejecutarse. Redactada por Claude Code el 2026-10-13 a partir de la decisión del autor. No modifica `spec.md`, `plan.md` ni `tasks.md` de 006 (archivos de Codex): según el procedimiento `change`, primero se muestra el diff, el autor lo aprueba y el escritor del archivo (Codex) lo aplica y conserva los bytes anteriores. Sin commit ni push.

## Intención expresada por el autor (2026-10-13)

El autor expresó que revisó y aceptó los PDF de R7 y la intención de retirar Google Docs como requisito de cierre de 006; el diff de este archivo fue aprobado después, en el mensaje citado arriba. Con la aprobación del diff, esta decisión sustituye las instrucciones anteriores que trataban la importación y comprobación en Google Docs como obligatoria (RF-14b, criterio de cobertura, `tasks.md` y paquetes R4–R7). Los paquetes y rondas anteriores se conservan como históricos.

## Qué es requisito de cambio y qué no

- Es un cambio de **requisito de verificación** (no de metodología, resultados, pre-registro ni contratos científicos).
- No afecta cifras, texto ni entregables de R7 (SHA-256 del manifiesto `docs/huellas-paquete-auditoria-006-ronda7.json`: `69003c83a7c6ccbc69c5cbd23bbeeb43bde0b970792f53748df302ca574535e5`).
- Los DOCX de R7 siguen generándose como salida exportable, pero **su revisión en Word o Google Docs no es requisito de cierre** y no se afirma que sus enlaces funcionen allí.

## Diff propuesto

**`spec.md`, RF-14b (última oración)**

- Antes: «…y no prueban el clic en Word ni en Google Docs; el DOCX se revisa en Google Docs como excepción documentada, sin Word nativo.»
- Después: «…y no prueban el clic en Word ni en Google Docs. La revisión del autor sobre los PDF aprobados sustituye la comprobación en Google Docs, que no es requisito de cierre; no se afirma que los enlaces del DOCX funcionen en Word o Google Docs.»

**`spec.md`, «Criterios de finalización», viñeta de cobertura**

- Antes: «…los enlaces internos existen en PDF y DOCX (comprobación estructural, DOCX revisado en Google Docs sin Word nativo).»
- Después: «…los enlaces internos existen en PDF y DOCX (comprobación estructural); el autor revisó y aceptó los PDF de R7.»

**`plan.md`, §enlaces (línea 94)**

- Antes: «En Google Docs no se garantiza el salto entre archivos locales: se verifica el interno y se documenta el límite.»
- Después: «En Google Docs no se garantiza el salto entre archivos locales; esa comprobación no es requisito de cierre y se documenta el límite.»

**`tasks.md`, encabezado (líneas 3 y 8) y nota de QA (línea 141)**

- Línea 3: quitar «Google Docs» de «T12, Google Docs y 006 pendientes» → «T12 y 006 pendientes».
- Línea 8: sustituir «la instrucción actual trata Google Docs como comprobación adicional… pendiente y obligatoria por RF-14b» por «el autor retiró Google Docs como requisito de cierre el 2026-10-13».
- Línea 141: «Google Docs requiere revisión manual tras importar» → «la revisión en Google Docs no es requisito de cierre».

Las demás menciones históricas de Google Docs (evidencias de rondas 1–7, `docs/importacion-google-docs-006-ronda7.md`, rondas de auditoría) se conservan sin cambios.

## Qué sigue siendo requisito para cerrar 006 (identificado específicamente)

Según los «Criterios de finalización» de `spec.md` y T12, con su estado hoy:

| Requisito | Estado |
|---|---|
| Suite completa en verde y `review-validate.md` APROBADO | Hecho por Codex en R7 (974 passed, rc 0, sin exclusiones; validación propia, no independiente) |
| `review-audit.md` independiente con `VEREDICTO: APROBADO` | **Pendiente de registro formal.** Las rondas 1–6 están guardadas; la ronda 6 (paquete R7) quedó APROBADA por los tres revisores de contexto limpio, pero `review-audit.md` conserva el veredicto de la ronda 1 (CAMBIOS NECESARIOS). Falta que el autor acepte `review-audit-ronda6.md` como la auditoría vigente y que se registre ese veredicto sin borrar las rondas previas (escritor: Claude) |
| Revisión con `profesor-evaluador` | Hecha (ronda 6: APROBADO, 95/100 estimado, no es nota del profesor) |
| **Ensayo de las preguntas probables** | **Pendiente, a cargo del autor.** Es el único requisito de contenido de T12 que ningún agente puede cumplir por él |
| Entrega antes del plazo confirmado | **Pendiente de confirmación del profesor** (hora límite oficial, formato, extensión, aceptación del par informe-anexo separado). La fecha de portada del 16 de octubre de 2026 es decisión del autor, no hora límite oficial |
| Marcado de T12 y cierre de 006 | A cargo de Codex/autor tras lo anterior; nadie lo marca por inferencia |

Observaciones menores de la ronda 6 (R6-1 a R6-5, cosméticas) no son requisito de cierre; el autor decide si se aplican.

## Aprobación (registrada)

Aprobar este diff (o pedir cambios) para que Codex lo aplique con copias de los bytes anteriores y huellas antes/después, y para que Claude registre el veredicto vigente de la auditoría en `review-audit.md` (adición, sin sustituir rondas). Hasta entonces, 006 y T12 siguen abiertas.
