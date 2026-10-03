---
description: SDD · Auditoría experta de una spec crítica ya validada en OpenCode (uso - /sdd-audit 003-modelo-i)
argument-hint: "[NNN-nombre]"
model: sonnet
disable-model-invocation: true
---
Comprueba que specs/$0/review-validate.md existe y empieza con `VEREDICTO: APROBADO`. Si no, para: primero toca `/sdd-validate $0` en OpenCode.

Pide al subagente revisor-econometrico que audite los resultados de specs/$0/ (si es la 006, que audite la coherencia econométrica del informe: cifras, interpretación, lenguaje causal y límites). Pásale solo las rutas: specs/$0/, outputs/, report/_variables.yml, report/ y docs/constitution.md. No le des tu opinión.

Guarda su informe tal cual en specs/$0/review-audit.md. Después:
- Si es APROBADO: cambia la spec a "Estado: implementada", haz commit con `audit($0): aprobada` y propón el título y la descripción del PR (usa .github/pull_request_template.md).
- Si es CAMBIOS NECESARIOS: conviértelos en una lista de correcciones ordenada por gravedad, lista para pegar en OpenCode como `/fabrica $0 "Correcciones de review-audit.md: ..."`. No corrijas tú el código.
- Muéstrame las 3 preguntas que haría el profesor y anótalas en MEMORY.md para el ensayo.
