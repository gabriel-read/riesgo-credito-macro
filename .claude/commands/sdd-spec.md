---
description: SDD · Entrevista y genera la spec (uso - /sdd-spec 003-modelo-i idea inicial)
argument-hint: "[NNN-nombre] [idea inicial]"
model: opus
effort: high
disable-model-invocation: true
---
NO escribas código en ningún momento. Lee docs/constitution.md, docs/guia-profesor.md, MEMORY.md y las specs anteriores de las que dependa esta. Usa la skill sdd y la skill de dominio que aplique (datos-fred, econometria-series-tiempo, citas-apa o informe-quarto).

Carpeta de la spec: specs/$0/
Idea inicial (todo lo que va después del nombre de la carpeta): $ARGUMENTS

Tu trabajo:
1. Hazme preguntas de UNA en UNA para eliminar ambigüedades (casos límite, errores, qué queda fuera de esta versión, decisiones de especificación). Máximo 5. Si la idea ya resuelve algo, no lo preguntes.
2. Con mis respuestas, genera specs/$0/spec.md con la plantilla de la skill sdd, requisitos en EARS, "Estado: borrador" y "Crítica: sí" o "Crítica: no".
3. Solo el QUÉ y el POR QUÉ, incluida la especificación pre-registrada si es una spec de modelos o estrés. Nada de módulos, archivos ni librerías.
4. Al terminar, dime el siguiente paso: `/sdd-clarify $0` en OpenCode.
