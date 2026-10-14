# Ronda 6 de auditoría (paquete ronda 7, comprobación acotada) — verificador-citas (contexto limpio)

Copia del mensaje final del subagente `verificador-citas`, tomada de la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 7 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda7.json`, SHA-256 69003c83a7c6ccbc69c5cbd23bbeeb43bde0b970792f53748df302ca574535e5). Rondas anteriores conservadas intactas.

**VEREDICTO: APROBADO**

No hay hallazgos de severidad alta ni media. Hay una observación menor.

| Punto | Resultado |
|---|---|
| (a) O-1 | Resuelto. La columna Método de `obradovic2026` en `research/matriz-literatura.md` (línea 40) dice ahora «mínimos cuadrados generalizados factibles… FGLS». No queda «generalizables» en la matriz, `report/secciones/02-literatura.qmd`, `informe.md` ni `anexo-tecnico.md`. |
| (b) O-2, fidelidad al resumen | Resuelto. Consulté OpenAlex (`doi:10.2478/jcbtp-2026-0020`) y el resumen dice lo que sigue. Son nueve países del Sudeste de Europa, 2007–2022, con FE, FGLS y PCSE sobre un panel no balanceado. Las tasas de interés de préstamo son un determinante significativo de la morosidad, y las condiciones más restrictivas amplifican el riesgo. El tipo de cambio oficial no muestra una correlación consistente. El desempleo tiene una asociación negativa, descrita como contraintuitiva, que se atribuye a un comportamiento de préstamo más cauteloso en la incertidumbre y a los programas de apoyo público. |
| (b) Texto de 02 (`02-literatura.qmd`, líneas 66–68, y `informe.md`, 300–310) | Fiel. No inventa signos. «Inesperado» traduce «counterintuitive», y la explicación está atribuida a los autores. |
| (b) «En la mayoría de los estudios cuyos signos son verificables…» | Correcto. Cita tres estudios con desempleo positivo (Bayar, Zawadzki, Golitsis). Obradović queda como excepción explícita, dicha después, y los demás estudios no aportan un signo de desempleo contrario. |
| (b) Anexo E (`anexo-tecnico.md`, línea 4751) | Coherente con 02 y la matriz. Dice «Base consultada: resumen del estudio» y recoge la tasa de préstamo positiva (que no es la de política), el tipo de cambio sin efecto consistente y el desempleo negativo con la explicación de los autores. |
| (b) Nota de la Tabla 1 (`informe.md`, líneas 258–263) | Coherente. Remite al texto de 2.5 y aclara que el guion no equivale a un coeficiente cero ni a un signo ausente. |
| (c) DOI de Zawadzki | `10.2478/ceej-2023-0016` está idéntico en `report/references.bib` y en `informe.md` y `informe.pdf`, en una sola línea cada uno (1 aparición por archivo). Hay 0 apariciones en el anexo. |
| (c) Lista de referencias única | Un solo encabezado «10. Referencias» en `informe.md`, y el anexo no tiene ninguno. |
| (c) `scripts/verify_refs.py` | 21 de 21 entradas OK. |

**Observación O-3 (baja)**
- **Ubicación:** nota de la Tabla 1, `informe.md`, líneas 258–263.
- **Qué pasa:** la nota no menciona que la lectura de Obradović se basa en el resumen del estudio. Ese alcance sí aparece en el Anexo E, al que la Tabla 1 remite en su encabezado.
- **Por qué es menor:** no hay afirmación falsa y no exijo un requisito nuevo.
- **Posible mejora:** añadir una cláusula breve a la nota.

**Qué no pude verificar**
- La capa visual del PDF (cursivas, saltos de línea y URL partidas). Solo comprobé el texto extraído con `pdftotext`.
- Los DOCX. No abrí su contenido.
- No recalculé los SHA-256 contra el manifiesto de la ronda 7.
- No revisé las atribuciones de los demás estudios, salvo lo que el texto de 02 dice de Bayar, Zawadzki y Golitsis. Las contrasté con la matriz y con mi ronda previa, no con las fuentes.
- No consulté Crossref de nuevo. La existencia y los metadatos los confirmó `verify_refs.py`.
