---
description: SDD · Aplica a la spec las observaciones del QA y tus decisiones; la aprueba si no quedan dudas (uso - /sdd-resolve 003-modelo-i decisiones)
argument-hint: "[NNN-nombre] [tus decisiones]"
model: opus
effort: high
disable-model-invocation: true
---
Lee specs/$0/spec.md y specs/$0/review-clarify.md (lo escribió el revisor de OpenCode). Usa la skill sdd.
Mis decisiones (todo lo que va después del nombre de la carpeta; puede estar vacío): $ARGUMENTS

1. Para cada punto de review-clarify.md, aplica mi decisión. Si un punto no tiene decisión mía, pregúntamelo de uno en uno, con tu recomendación y su porqué.
2. Elimina las [NECESITA ACLARACIÓN] resueltas.
3. Muéstrame el diff de spec.md.
4. Si no quedan dudas abiertas y lo apruebo, cambia a "Estado: aprobada", haz commit con el mensaje `spec($0): aprobada` y dime el siguiente paso: `/sdd-plan $0`.
