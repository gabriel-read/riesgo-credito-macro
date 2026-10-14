# Correcciones 006: reparto C1–C10 e integración

Autorización del autor: correcciones de la ronda 1; sin commit ni push. Copia única: `C:/Users/gabri/orca/riesgo-credito-macro`. Claude confirmó el reparto por terminal el 12-oct-2026. La instrucción actual permite editar simultáneamente **archivos distintos**, pero prohíbe tests, pipeline y render mientras cualquiera escribe. Esta excepción no altera los contratos científicos.

| Bloque | Responsable de cierre | Archivos y parte asignada |
| --- | --- | --- |
| C1 | Claude | `report/secciones/04-modelo1.qmd`, `06-resultados.qmd`, `09-conclusiones.qmd`: términos compartidos, controles y lectura simétrica. |
| C2 | Claude | `04-modelo1.qmd`, `08-implicaciones.qmd`, `09-conclusiones.qmd`: contemporaneidad, simultaneidad y límites de anticipación. |
| C3 | Claude | `04-modelo1.qmd`, `05-modelo2.qmd`: tasa cero, robusteces R2/R3, PPP/R1 parcial y K condicional. |
| C4 | Codex | `src/report_tables.py`, `src/report_editorial.py` y tests: p pequeños y KPSS censurados, sin modificar CSV/JSON aprobados. |
| C5 | Codex, integración | Claude corrige remisiones y letras de anexo en sus nueve secciones; Codex en `03a`–`03e`, `10`, `11`, adaptador/editorial y filtros Quarto. Destinos por registro único; variante combinada interna. |
| C6 | Codex, integración | Codex: portada, subtítulos, sección 11, pies y etiquetas. Claude: texto interno de `03f` y duplicación en `04`. Sin afirmar cierre en el producto ni mostrar mensajes de coordinación. |
| C7 | Claude | `01-introduccion.qmd`, `02-literatura.qmd`, `08-implicaciones.qmd`: correspondencia de 2.5 y citas M1–M4. Codex elimina las notas numéricas inaplicables de la tabla de literatura. |
| C8 | Codex | `report/references.bib`, presentación de referencias y tests: FRED, FMI, Newey–West y autor/editorial Fed, con verificación de fuentes. Conservar CSL oficial si basta la metadata; documentar cualquier adaptación local. |
| C9 | Claude | `07-estres.qmd`: asimetría, dirección de inflación, D y extremos de réplicas. No introducir descomposición numérica no aprobada. Codex rotula las tablas derivadas sin cambiar cifras. |
| C10 | Codex, integración | Claude: menores econométricos 6–8, 12–15, 17 y contexto desde variables existentes en `04`–`09`. Codex: RF-7/RF-13, identificadores en todos los paneles, nombres legibles, numeración y ecuaciones **solo si representan las especificaciones ya aprobadas**. Si exigen metodología nueva, presentar `/sdd-change` y mantener ese punto pendiente. |

Claude solo escribe `01`, `02`, `03f`, `04`–`09`, sus solicitudes y borradores de 007; Codex escribe fuentes técnicas, tests, `03a`–`03e`, `10`, `11`, configuración, documentación de integración y productos generados. Ningún archivo tiene dos escritores. Claude no modifica variables ni ejecuta el pipeline. Codex no implementa diapositivas.

## Turnos

1. Lectura y escritura separada: Claude corrige sus secciones; Codex prepara tests de regresión y sus fuentes. **No ejecutar ninguna validación** en esta fase.
2. Claude entrega rutas/huellas y confirma pausa total, incluida 007. Codex solicita y conserva el turno exclusivo antes de ejecutar tests primero y corregir cada bloque técnico.
3. Integración: con ambos escritores detenidos, Codex ejecuta suite completa sin exclusiones, `report`, renders principal/anexo PDF/DOCX, comprobación de enlaces y reproducibilidad. Las salidas protegidas de 001–005 se cotejan por huella; no se regeneran modelos ni estrés.
4. Codex registra evidencia, conserva validación/auditoría ronda 1 y entrega paquete para ronda 2 con autoría real. T12 y 006 siguen abiertas hasta auditoría aprobada y Google Docs obligatorio; no sustituirlo por comprobaciones estructurales.

## Pendientes que no se resuelven inventando

- Portada resuelta con datos explícitos del autor; revisión actual en review-validate-ronda3.md.
- Google Docs: importación y enlaces aún no verificados; requiere participación del autor y URLs reales o evidencia manual.
- Confirmaciones externas de fecha/formato; no contactar al profesor por cuenta propia.
- I3 contrastado y autorizado: solo transcripción de003/004, sin cambio contractual; composición en líneas verificada. Sin descomposición opcional del estrés.
