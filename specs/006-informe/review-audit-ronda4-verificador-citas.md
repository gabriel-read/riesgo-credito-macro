# Ronda 4 de auditoría (paquete ronda 5, acotada) — verificador-citas (contexto limpio)

Copia del mensaje final del subagente `verificador-citas`, tomada del texto recibido en la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 5 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda5.json`, SHA-256 8671052e…5b57): informe.pdf 8cdfa2a6…, informe.docx 994e28fc…, anexo-tecnico.pdf 58429c72…, anexo-tecnico.docx 75e241c1…. Alcance: hallazgos de la ronda 3 (N-1, N-3) y regresiones.

**VEREDICTO: APROBADO**

Los dos hallazgos de la ronda 3 están corregidos y no hay regresiones de severidad alta o media. Quedan límites de verificación: no pude ver el PDF renderizado (no hay `pdftoppm` ni `fitz`) y no comprobé páginas ni cursivas. La verificación fue sobre la capa de texto con `pdftotext -enc UTF-8`, sobre `informe.md`, `anexo-tecnico.md`, `report/secciones/02-literatura.qmd` y `research/matriz-literatura.md`.

## Hallazgos → estado

| Hallazgo | Estado | Evidencia |
|---|---|---|
| N-1: pie y signos de la Tabla 1 | Corregido | La Tabla 1 del cuerpo ahora tiene la columna «Signo y contexto» (`outputs/preview-006/report/informe.md`, líneas 241–259; también en el PDF). El pie «variables, métodos y signos» ya coincide con la tabla. `02-literatura.qmd` líneas 52–53 explican la columna: «—» significa que la tabla no recoge el signo. El guion de Obradović y Grubišić tiene una nota propia: remite al signo descrito en 2.5 para la tasa de préstamo, distinta de la tasa de política, y no significa un coeficiente cero. |
| N-3: alcance de la verificación en 02-literatura | Corregido | `02-literatura.qmd` línea 5: «En la mayoría de los casos la verificación se apoya en el resumen del estudio, y el Anexo E indica la base de cada uno». Está en el PDF (línea 141 del texto extraído). El Anexo E indica la base por estudio. Para Obradović dice «resumen del estudio… Lectura de signo no presentada». Para Golitsis dice «texto completo, resultados de largo plazo y Tabla 4». |

## Comprobaciones pedidas en (b)

| Punto | Resultado |
|---|---|
| DOI de Zawadzki (2023) | Íntegro y en una sola línea en el PDF (`https://doi.org/10.2478/ceej-2023-0016`). El guion de `ceej-2023` aparece una sola vez y no se parte ni se duplica. El DOI está igual en `informe.md` línea 1795 y en `report/references.bib`. El título conserva U+2011 en «non‑performing», sin guion duplicado. |
| Lista de referencias única | Hay un solo encabezado «10. Referencias» en `informe.md` (línea 1618) y en el PDF (línea 1451). `anexo-tecnico.pdf` y `anexo-tecnico.md` no contienen entradas `ref-` ni el DOI de Zawadzki. |
| Fila de Obradović y Grubišić (2026) | Coincide con la fila `obradovic2026` de la matriz: variable dependiente, regresores (tasa de préstamo, tipo de cambio oficial, desempleo) y método (FE, FGLS y PCSE sobre panel no balanceado). El signo queda en «—» con la nota anterior. No sobreafirma: la base es el resumen y el Anexo E lo dice. Los signos de la matriz sobre el tipo de cambio y el desempleo no aparecen en el cuerpo. La frase de la línea 68 (tipo de préstamo asociado con más morosidad) está respaldada por la matriz. |
| Procedencia de Golitsis | La Tabla 1 y la matriz dan la misma descripción literal (0,64 % del desempleo y 3,47 % de las tasas, PIB negativo, préstamos brutos no significativos). Ambas citan «texto completo, resultados de largo plazo y Tabla 4». La nota bajo la tabla coincide con la matriz. Es la única fila con lectura de texto completo que declara el informe. |
| Zawadzki en la Tabla 1 | Coincide con la matriz. El signo de la inflación y el de la depreciación se declaran no precisos en el resumen, igual que en el texto, línea 66. |
| `scripts/verify_refs.py` | 21 de 21 entradas OK. |
| Diacríticos y glifos | La capa de texto del PDF contiene ć y š (Obradović, Grubišić) y U+2011. La pérdida de caracteres que vi al principio venía de la consola, no del PDF. |

## Regresiones nuevas

Ninguna de severidad alta ni media. Hay una observación menor sin gravedad: en `informe.md` el título de Zawadzki usa U+2011 en lugar del guion ASCII del `.bib`. Es un artefacto de citeproc/typography y no afecta al DOI.

## Qué no pude verificar

- El PDF renderizado: cursivas, saltos de línea visuales y posibles espacios en las URL partidas por el compositor (el DOI de Zawadzki queda en una sola línea).
- Las atribuciones de hallazgos de los demás estudios, que dependen de resúmenes de OpenAlex o Crossref. Esta ronda no rehízo las consultas web; me apoyé en la ronda anterior y en la matriz.
- Los hashes de los artefactos frente a la versión auditada en la ronda 3. Los archivos actuales son de 12:33–12:40 del 13-oct.
- Los `.docx`, que no abrí.
