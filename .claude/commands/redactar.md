---
description: Redacta una sección del informe desde outputs/ y la matriz de literatura (uso - /redactar 6.4 notas)
argument-hint: "[sección] [notas]"
model: opus
effort: high
disable-model-invocation: true
---
Vamos a redactar la sección $0 de report/informe.qmd. Usa las skills informe-quarto, econometria-series-tiempo y citas-apa.
Notas del usuario (todo lo que va después del número de sección; puede estar vacío): $ARGUMENTS

Antes de escribir, lee: docs/guia-profesor.md (qué pide esa sección), specs/006-informe/spec.md, MEMORY.md, report/_variables.yml, las tablas y figuras de outputs/ que apliquen, research/matriz-literatura.md y los review-audit.md de las specs 003–005.

Reglas:
- Primera frase = la respuesta de la sección.
- Cada número con `{{< var … >}}`. Si falta una variable, NO la escribas a mano: lista las que faltan para que el pipeline las genere.
- Cada cita con una clave que exista en report/references.bib.

Muéstrame el texto antes de escribirlo en el archivo. Con mi OK: escríbelo, marca su tarea (`agente: claude`) en specs/006-informe/tasks.md y renderiza con `quarto render report/informe.qmd` para confirmar que no hay errores.
