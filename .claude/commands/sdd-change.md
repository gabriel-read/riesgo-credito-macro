---
description: SDD · Cambio de requisitos - primero la spec, luego plan y tareas, al final el código (uso - /sdd-change 003-modelo-i cambio)
argument-hint: "[NNN-nombre] [cambio]"
model: opus
effort: high
disable-model-invocation: true
---
Nuevo requisito o cambio para specs/$0/ (todo lo que va después del nombre de la carpeta): $ARGUMENTS

NO toques código. Usa la skill sdd.
1. Actualiza specs/$0/spec.md: RF nuevo o modificado en EARS, sus casos límite y lo que queda fuera de alcance.
2. Si la spec ya estaba aprobada y el cambio toca la especificación pre-registrada, añade una línea en "Desviaciones del pre-registro" con fecha, cambio y motivo (el informe tendrá que reportarlo en la sección 3.5).
3. Indica qué partes de plan.md y tasks.md habría que cambiar.
4. Muéstrame el diff de la spec y espera mi aprobación. Con ella, actualiza plan.md, haz commit con `spec($0): cambio` y dime que en OpenCode toca `/sdd-tasks $0` para propagarlo a las tareas.
