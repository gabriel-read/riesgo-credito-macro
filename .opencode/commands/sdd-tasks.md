---
description: SDD · Divide el plan aprobado en tareas pequeñas y verificables, o propaga un cambio a tasks.md (uso - /sdd-tasks 001-datos)
agent: planner
---
Trabaja sobre specs/$1/ siguiendo la skill sdd.

- Si spec.md o plan.md no dicen "Estado: aprobada" (o "implementada", cuando se trata de añadir correcciones), para y avísame.
- Si tasks.md no existe, genéralo: tareas de 20–30 min como máximo, en orden de dependencia, cada una con sus RF, su agente (implementer, bibliotecario o claude) y "Hecho cuando:". Checkboxes. Intenta no pasar de 10; si salen más, propón dividir la spec. Termina con una tabla RF → tareas.
- Si tasks.md ya existe, no lo regeneres: ajústalo a la spec y al plan actuales (tareas nuevas al final, sin desmarcar las hechas) y muéstrame el diff.
