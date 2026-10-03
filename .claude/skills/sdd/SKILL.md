---
name: sdd
description: Úsala siempre que trabajes con Spec-Driven Development en este proyecto (docs/constitution.md o cualquier archivo en specs/) - redactar, revisar o cambiar specs, planes y tareas, o implementar, validar y auditar tareas de una spec.
---

# Spec-Driven Development (SDD) — investigación reproducible

## Flujo
Constitución → Spec → Clarificación → Plan → Tareas → Implementación → Validación → Auditoría (specs críticas) → Cambio.

- Nunca pases a la siguiente fase sin la aprobación explícita del usuario.
- La spec manda: si algo no está en la spec, no se hace. Si falta una decisión, para y pregunta.
- Un cambio se hace primero en la spec, luego en el plan y las tareas, y por último en el código.
- Cada spec vive en `specs/NNN-nombre/`: `spec.md`, `plan.md`, `tasks.md` y los informes `review-clarify.md`, `review-plan.md`, `review-validate.md`, `review-audit.md`.
- Specs críticas: 003, 004, 005 (modelos y estrés) y 006 (informe). Se cierran solo con `review-audit.md` aprobado.
- Al terminar cada fase, actualiza `MEMORY.md`.

## Quién hace cada fase
| Fase | Arnés | Comando |
|---|---|---|
| Constitución, Spec, Resolución, Plan, Cambio | Claude Code | /sdd-constitution, /sdd-spec, /sdd-resolve, /sdd-plan, /sdd-change |
| Clarificación, Tareas, Implementación, Validación, Estado | OpenCode | /sdd-clarify, /sdd-tasks, /fabrica o /sdd-implement, /sdd-validate, /sdd-status |
| Auditoría experta, Redacción de discusión | Claude Code | /sdd-audit, /redactar |

Si se agota el cupo de Claude Code, el planner de OpenCode puede redactar spec y plan; la auditoría de Claude se hace cuando vuelva el cupo y queda anotada como pendiente en `MEMORY.md`.

## Plantilla de spec (spec.md)
```
# Spec NNN — <Nombre>
Estado: borrador | aprobada | implementada · Crítica: sí | no

## Contexto y objetivo
## Pregunta que responde (y sección de docs/guia-profesor.md que cubre)
## Usuarios
## Historias de usuario
- HU-1. Como <rol>, quiero <acción> para <beneficio>.
## Definiciones (solo si hay términos que puedan interpretarse de varias formas)
## Especificación pre-registrada (solo specs de modelos y estrés)
Variables y transformaciones · ecuación · rezagos y su criterio · estimador y errores estándar · signos esperados con su mecanismo · regla de decisión niveles/diferencias · pruebas de robustez previstas.
## Requisitos funcionales
## Requisitos no funcionales
## Casos límite
## Fuera de alcance
## Criterios de finalización
## Desviaciones del pre-registro (fecha · cambio · motivo; vacío si no hay)
## Dudas abiertas
- [NECESITA ACLARACIÓN] <duda>
```
En esta investigación la especificación econométrica es parte del QUÉ: es el pre-registro. La spec no nombra módulos, archivos ni librerías; eso va en el plan.

## Requisitos en EARS (en español)
- RF-x: CUANDO <evento>, EL SISTEMA <respuesta>.
- RF-x: SI <condición no deseada>, ENTONCES EL SISTEMA <respuesta>.
- RF-x: MIENTRAS <estado>, EL SISTEMA <respuesta>.
- RF-x: EL SISTEMA <comportamiento permanente>.

"EL SISTEMA" es el pipeline de análisis o el informe, según la spec. Cada RF debe poder verificarse con un test o con un archivo de salida concreto: nada de "robusto", "claro" o "significativo" sin un criterio medible (por ejemplo, "p < 0,05 con errores HAC").

## Plan (plan.md)
`Estado: borrador | aprobada`. Módulos de `src/` y responsabilidad de cada uno · funciones puras con su firma (reciben DataFrame y parámetros; sin red, disco ni gráficos) · algoritmo en pseudocódigo · salidas exactas (`outputs/tables`, `outputs/figures`, claves de `report/_variables.yml`) · etapa de `src.pipeline` que las produce · decisiones justificadas con su alternativa descartada · estrategia de tests con pytest (datos simulados de parámetros conocidos para estimadores; `data/raw/` congelado para datos) · qué RF cubre cada parte.

## Tareas (tasks.md)
```
- [ ] **Tn. <Descripción>.** RF-x, RF-y · agente: implementer | bibliotecario | claude
  - Hecho cuando: <comprobación verificable>.
```
Máximo 20–30 min por tarea, en orden de dependencia. Intenta no pasar de 10; si salen más, propón dividir la spec. `agente: claude` = redacción que se hace con `/redactar` en Claude Code. Al final, una tabla RF → tareas.

## Implementación
Una sola tarea cada vez: tests primero (en rojo), después el código, `uv run pytest -q` en verde, marcar la tarea y parar.

## Informes de revisión (review-*.md)
Empiezan con `VEREDICTO: APROBADO` o `VEREDICTO: CAMBIOS NECESARIOS` (salvo review-clarify, que es solo una lista de hallazgos). Los cambios necesarios van en lista numerada con archivo:línea, qué incumple (tarea, RF o principio) y qué se espera. Lo opcional va aparte y no bloquea.
