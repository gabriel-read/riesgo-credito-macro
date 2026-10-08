---
name: citas-apa
description: Úsala siempre que busques, propongas, verifiques, cites o formatees literatura y referencias en este proyecto (spec 002, research/, report/references.bib o cualquier cita en el informe).
---

# Literatura y citas — protocolo anti-citas-inventadas

Los modelos de lenguaje inventan referencias con facilidad. En este proyecto una cita inventada invalida el trabajo. Sigue este protocolo siempre.

## Reglas
- Nunca cites de memoria. Una referencia existe para este proyecto solo si tiene DOI (o URL oficial para documentos sin DOI, como la Fed o el Comité de Basilea) y pasó la verificación.
- Busca en APIs abiertas sin clave:
  - OpenAlex: `https://api.openalex.org/works?search=<términos>&per-page=10`
  - Crossref: `https://api.crossref.org/works?query=<términos>&rows=10`
  - Confirmar un DOI: `https://api.crossref.org/works/<DOI>` · Resumen: `https://api.openalex.org/works/doi:<DOI>`
- Un candidato se acepta si título, autores, año y revista coinciden con el registro del DOI y si el resumen respalda lo que vamos a afirmar. Sin resumen leído, Estado = pendiente-lectura.
- No atribuyas a un estudio un hallazgo que no está en su resumen o en un fragmento que hayas leído.
- La lista semilla del playbook es un punto de partida, no una verdad: se verifica igual que cualquier candidato.

## Matriz de literatura (`research/matriz-literatura.md`)
Una fila por estudio o referencia. El formato exacto (16 columnas, tabla «Resumen» previa, valores admitidos, «no aplica», motivo de descarte con prefijo «Descartado: ») lo fijan `specs/002-literatura/spec.md` (RF-4, RF-20 a RF-24) y `specs/002-literatura/plan.md` (§4). Si esta skill y la spec difieren, manda la spec. Resumen de columnas: Clave · Autor(es) y año · País · Frecuencia · Período · Variable dependiente · Regresores · Variables de la guía · Método · Hallazgo o aporte · Sección principal · Secciones secundarias · Respalda · Tipo · Estado (verificado | pendiente-lectura | descartado) · URL de verificación.

## BibTeX (`report/references.bib`)
- Clave `apellidoaño` en minúsculas, sin tildes, ñ ni guiones (`jimenez2006`, `bernanke1995`, `frb2026`); campo `doi` siempre que exista. Los tests del arnés solo reconocen ese formato.
- Solo entran referencias con Estado = verificado.
- Tras editarlo, corre `uv run python scripts/verify_refs.py` (comprueba cada DOI contra Crossref) y no des la tarea por hecha si falla.

## APA 7 en el informe
- Cita con `[@clave]` o `@clave`; la lista final la genera Quarto con `apa.csl`.
- Documentos institucionales: autor = organización (Board of Governors of the Federal Reserve System, 2026).
- Datos: cita cada serie de FRED con su código y la fecha de consulta.

## Checklist
- [ ] ¿Toda cita del informe existe en references.bib?
- [ ] ¿Toda entrada de references.bib está como verificado en la matriz?
- [ ] ¿`verify_refs.py` pasa?
- [ ] ¿Cada hallazgo atribuido aparece en la fuente leída?
