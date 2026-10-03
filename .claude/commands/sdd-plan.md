---
description: SDD · Genera el plan técnico de una spec aprobada; en specs críticas lo audita el revisor econométrico (uso - /sdd-plan 003-modelo-i)
argument-hint: "[NNN-nombre]"
model: opus
effort: high
disable-model-invocation: true
---
Lee docs/constitution.md, AGENTS.md, MEMORY.md, specs/$0/spec.md y los plan.md de las specs de las que depende. Usa la skill sdd y la skill de dominio que aplique. NO escribas código.

Si la spec no dice "Estado: aprobada" o tiene dudas abiertas, para y avísame.

Genera specs/$0/plan.md ("Estado: borrador") con:
- Módulos de src/ y la responsabilidad de cada uno.
- Funciones puras con su firma (reciben DataFrame y parámetros; sin red, disco ni gráficos).
- Algoritmo en pseudocódigo.
- Salidas exactas: outputs/tables, outputs/figures y claves de report/_variables.yml.
- Cómo se integra en `uv run python -m src.pipeline <etapa>`.
- Decisiones técnicas justificadas, cada una con su alternativa descartada.
- Estrategia de tests con pytest y semillas fijas.
- Qué RF cubre cada parte.

Si la spec dice "Crítica: sí", antes de enseñármelo pide al subagente revisor-econometrico que audite el plan. Pásale solo las rutas (spec.md, plan.md, docs/constitution.md, docs/guia-profesor.md), no tu opinión. Guarda su informe tal cual en specs/$0/review-plan.md e incorpora o rebate cada observación.

Enséñame un resumen del plan, las observaciones del revisor y qué hiciste con cada una. Cuando lo apruebe, cambia a "Estado: aprobada", haz commit con `plan($0): aprobado` y dime el siguiente paso: `/fabrica $0` en OpenCode.
