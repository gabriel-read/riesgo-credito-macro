---
description: SDD · Valida la spec RF por RF y deja el veredicto en review-validate.md (uso - /sdd-validate 001-datos)
agent: reviewer
---
Valida la implementación de specs/$1/ siguiendo la sección "Si te piden validar la implementación" de tus instrucciones y la skill sdd.

1. Ejecuta `uv run pytest -q`.
2. Si la spec produce salidas, corre la etapa del pipeline que indica plan.md y confirma que se regeneran sin errores.
3. Recorre la spec RF por RF: qué test o qué archivo lo cubre y su resultado.
4. Escribe specs/$1/review-validate.md empezando por la línea de VEREDICTO.

NO arregles nada. Después comprueba los criterios de finalización y dime: ¿la spec está cumplida?
