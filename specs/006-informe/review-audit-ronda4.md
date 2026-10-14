# Auditoría independiente de 006 — Ronda 4 (paquete ronda 5, acotada)

Estado: **APROBADA TÉCNICAMENTE; QUEDAN AJUSTES EDITORIALES MENORES** (2 revisores APROBADO, 1 CAMBIOS NECESARIOS por defectos menores, ninguno bloqueante). Rondas 1, 2 y 3 conservadas intactas. La ronda de paquete «4» de Codex es histórica y no se usa como vigente; esta ronda de auditoría corresponde a su paquete ronda 5.

## Alcance y autoría

- Alcance: solo (a) estado de los hallazgos de la ronda 3 y (b) regresiones. Sin requisitos nuevos ni lectura completa de estudios. Fecha de portada del 16 de octubre de 2026: decisión del autor; no es la hora límite oficial, que sigue sin confirmarse.
- Autoría del informe: Claude 01, 02, 03f, 04–09 (con sus correcciones de las rondas 2 y 3 y R3-X7 en 02/04); Codex 3a–3e, 10, 11, tablas, figuras, filtros, APA, anexos, infraestructura y validación.
- Coordinación: Claude Code. **No es auditoría independiente de mi propio texto.** La independencia procede de tres revisores de contexto limpio que recibieron solo rutas, criterios y sus propios hallazgos de la ronda 3.
- Informes en copia:
  - `review-audit-ronda4-revisor-econometrico.md` — APROBADO.
  - `review-audit-ronda4-verificador-citas.md` — APROBADO.
  - `review-audit-ronda4-profesor-evaluador.md` — CAMBIOS NECESARIOS (93/100 estimado; 92 en la ronda 3).

## Versión auditada

Manifiesto `docs/huellas-paquete-auditoria-006-ronda5.json` (SHA-256 8671052e783366423f4e08d5599d4c886c7c73cd209b19512a3b985812e55b57). Comprobación de Claude antes de lanzar y al cerrar (lectura, sin escritura): las 337 entradas del manifiesto coinciden con los archivos actuales (0 difieren); las nueve secciones de Claude y los seis entregables coinciden por huella completa; los entregables (12:33–12:40) son posteriores a la fuente más reciente (11:42:26). Entregables:

| Archivo (`outputs/preview-006/report/`) | SHA-256 |
|---|---|
| informe.pdf | 8cdfa2a6521594f6d56c3831aa4da022c2f17063abd823c50a18b01144b91878 |
| informe.docx | 994e28fce7fb7850b5aef9487efb0dca915459b8b3357ff2a46be197a0d3c130 |
| anexo-tecnico.pdf | 58429c72be4563d86420f115f3deaa0d05f5a9e812ddadc5c753ec5689779c22 |
| anexo-tecnico.docx | 75e241c1637c26174e936b6e68f07c8bc58d416084c565c592840030ed91854c |

Suite y renders (960 passed, clics 53/167 marcadores y 55 URI, 208 de report idénticos) son resultados de Codex; Claude no los reejecutó.

## Estado de los hallazgos de la ronda 3

- **Econométrico:** los seis (07:59 «se invierte», regla de la tasa una sola vez, concordancia «las especificaciones», etiquetas VIF, cláusula de colinealidad, nota circular) resueltos, con cálculo propio sobre `stress_paths.csv` y los coeficientes.
- **Citas:** N-1 (Tabla 1 con «Signo y contexto», nota del guion de Obradović) y N-3 (alcance de la verificación) corregidos; DOI de Zawadzki íntegro y una sola lista de referencias; `verify_refs.py` 21 de 21.
- **Profesor:** R1–R4, plantilla, remisiones repetidas, coletilla de 2.1–2.4, DOI, VIF y notas de Tablas 2, 5 y 7 resueltos; R5 parcial; N10 sin resolver.

## Pendientes menores y escritor propuesto

Ninguno bloquea. Las correcciones de mis archivos requieren turno exclusivo cedido.

| ID | Hallazgo | Fuente | Escritor |
|---|---|---|---|
| R4-X1 | La frase de 02 «En la mayoría de los casos la verificación se apoya en el resumen del estudio» deja más a la vista el alcance de la verificación; el anexo E dice «resumen del estudio» en 17 de 18 filas. Los dos revisores se contradicen: el verificador de citas pidió esa aclaración en la ronda 3 (N-3) y la da por correcta; el profesor propone dejarla solo en el anexo. **Decisión del usuario.** Recomendación de Claude: conservarla en el cuerpo (evita una sobreafirmación de verificación; no exige leer los estudios completos). | profesor X1, citas N-3 | Claude (02:5), si el usuario decide quitarla. |
| R4-X2 | Nota del panel 2 de C.3: texto interno («el CSV no añade una nota», «la salida aprobada») y repetida; «salida aprobada» también aparece en las notas de CUSUM del anexo (4 veces). Sustituir por «salida del modelo» y no repetir la nota. | profesor X2 | Codex. |
| R4-X3 | Anexo E dice de Obradović «Lectura de signo no presentada; consultar la fuente citada», mientras el informe presenta el signo de la tasa de préstamo y la nota de la Tabla 1 remite a él. | profesor X3 | Codex (fila del anexo) / coordinación con la nota. |
| R4-X4 | Procedencia de Golitsis queda como párrafo suelto bajo la Tabla 1 (tres notas seguidas); la tabla ocupa tres páginas con columnas estrechas. | profesor R5 | Codex. |
| R4-X5 | Lenguaje de proceso heredado: «crédito con su rezago aprobado» (03e), nota de la Tabla 6 («especificación pre-registrada» repetida), «generalizables factibles» en la Tabla 1 frente a «generalizados» en el texto, «consultar la matriz» en el anexo E, alternancia «preregistro»/«pre-registro» en 03c y 03e (mis secciones usan «pre-registr…»). | profesor | Codex. |
| R4-X6 | N10: queda el párrafo de candidatos no usados en 02 (mío, breve y sin conteos) y Nkusu «no especificados en la fuente consultada» en la Tabla 1. Recomendación: dejar el párrafo; es honesto y no añade lectura. | profesor N10 | Decisión del usuario; Claude/Codex según el caso. |
| R4-O1 | Opcional: 07:59 «hacia el final» → «en la segunda mitad» para ΔU (pasa a restar desde 2028T2, paso 8 de 13). | econométrico | Claude (opcional; no es un error de signo). |
| R4-O2 | Opcional: «VIF (PIB (crecimiento))» con paréntesis anidados. | econométrico | Codex. |
| R4-P1 | `outputs/informe/stress_delta_nota.md` no figura con ruta propia en el manifiesto de la ronda 5 (el econométrico lo leyó y coincide con la regla); confirmar qué entrada lo cubre. `report/_variables.yml` figura en el manifiesto con la misma huella, aunque su marca de tiempo (12:47) es posterior a los PDF; Codex declara las ejecuciones de report idénticas. | econométrico, Claude | Codex. |

## Lo que ningún revisor pudo verificar

- Renderizado visual del PDF (el profesor evaluó sobre páginas ya renderizadas de la ronda 5, con paridad inferida de `docs/visual-verificada-006-ronda5.json`); lectura de los DOCX como contenido por profesor y citas; clics reales en Word, PDF y Google Docs.
- Atribuciones de hallazgos de la mayoría de los estudios (resúmenes); no se exigió lectura completa.
- Reproducibilidad, tests y renders por parte de los revisores.
- **Google Docs sigue sin importarse ni verificarse: obligatorio para el cierre.**

## Siguiente paso

1. Usuario: decidir R4-X1/R4-X6 y si se aplica el ajuste opcional R4-O1.
2. Codex: R4-X2–R4-X5, R4-O2, R4-P1 y, si procede, regeneración con una verificación mínima.
3. Importación de los DOCX a Google Docs y comprobación del autor.
4. Pendientes externos: hora límite oficial, formato, duración, par informe-anexo separado y spec 007.

006 y T12 permanecen abiertas. Sin commit ni push.
