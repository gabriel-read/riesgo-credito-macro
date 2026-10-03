---
description: Evaluación final del informe y las diapositivas contra la guía del profesor, con dos subagentes independientes (uso - /evaluar)
model: sonnet
disable-model-invocation: true
---
1. Renderiza: `quarto render report/informe.qmd` y `quarto render report/slides.qmd`. Si hay errores, para y enséñamelos.
2. Lanza en paralelo, pasándoles solo rutas y no tu opinión:
   - el subagente profesor-evaluador, sobre report/ contra docs/guia-profesor.md;
   - el subagente verificador-citas, sobre report/references.bib y las citas del informe.
3. Guarda ambos informes tal cual en specs/006-informe/review-final.md.
4. Junta sus resultados en una lista única de mejoras, sin duplicados, ordenada por impacto en la nota. Sepárala en: (a) se arregla en OpenCode (código, tablas, figuras, render) y (b) se arregla con /redactar.
5. Anota en MEMORY.md la nota estimada y las 5 preguntas más difíciles para el ensayo.
