# Ronda 5 de auditoría (paquete ronda 6, acotada) — verificador-citas (contexto limpio)

Copia del mensaje final del subagente `verificador-citas`, tomada de la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 6 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda6.json`, SHA-256 3d25d637c56efff6b335254db0691eee13378d00d8fd45c157cf2331a4e8448a). Las rondas anteriores se conservan intactas.

**VEREDICTO: APROBADO**

No encontré hallazgos de severidad alta ni media. Hay dos observaciones menores, descritas más abajo.

## Criterio (a): lo resuelto sigue resuelto
| Punto | Resultado |
|---|---|
| DOI de Zawadzki | Crossref confirma el título, el autor (Zawadzki) y 2023. El DOI está en una sola línea en `informe.pdf` (línea 515 del texto extraído) y es idéntico al de `report/references.bib`. |
| Lista única de referencias | Hay un solo encabezado «Referencias» en `informe.pdf`. `anexo-tecnico.pdf` no contiene el DOI de Zawadzki. |
| `scripts/verify_refs.py` | 21 de 21 entradas OK. |
| Integridad del paquete | Los 6 entregables coinciden con los SHA-256 del manifiesto de la ronda 6. |

## Criterio (b): cambios de esta ronda
| Punto | Resultado |
|---|---|
| Frases del anexo | No quedan «Lectura de signo no presentada» ni «consultar la matriz» en `informe.md/.pdf` ni en `anexo-tecnico.md/.pdf`. |
| Obradović y Grubišić, Anexo E | La nota dice que el resumen informa una asociación positiva de la tasa de préstamo con la morosidad, que esa tasa no es la de política, y que el guion remite a la sección 2.5. |
| ¿Se inventa un signo? | No. El resumen en OpenAlex dice que los tipos de préstamo son un determinante significativo y que condiciones monetarias más restrictivas amplifican el riesgo de crédito. La matriz y la línea 68 de `02-literatura.qmd` dicen lo mismo. DOI, volumen 15(2), páginas 255–281 y año 2026 coinciden. |
| Procedencia de Golitsis | La nota de la Tabla 1 («texto completo, resultados de largo plazo y Tabla 4») coincide con la matriz y con el Anexo E. La nota está en el PDF (línea 111). |
| «generalizados» vs «generalizables» | El informe, la Tabla 1 y el Anexo E usan «generalizados». |

## Criterio (c): coherencia Tabla 1, Anexo E y matriz
Las filas de Obradović y de Golitsis coinciden en dependiente, regresores, método y sección 2.5. Las cifras de Golitsis (0,64 %, 3,47 %, PIB negativo, préstamos brutos no significativos) son idénticas en las tres fuentes. La nota de Zawadzki es coherente con su fila de la matriz.

## Observaciones
| ID | Severidad | Ubicación | Observación |
|---|---|---|---|
| O-1 | Baja | `research/matriz-literatura.md`, línea 40 (columna Método de `obradovic2026`) | Dice «mínimos cuadrados generalizables factibles». El resumen en inglés dice «feasible generalized least squares», así que el término correcto es «generalizados». El informe ya usa «generalizados». Conviene corregir la matriz para que las tres fuentes coincidan. No afecta a lo entregado. |
| O-2 | Baja | `informe.md`, línea 248 y nota (líneas 258–263); Anexo E | El guion de Obradović se explica solo por el signo positivo de la tasa de préstamo. La nota afirma que el guion «no significa… un signo ausente». El resumen informa además un efecto no consistente del tipo de cambio y una asociación negativa e inesperada del desempleo, y el informe no los menciona. El desempleo figura como regresor en esa misma fila. El informe no atribuye nada falso. Sí omite un resultado contrario a la línea 64 («un mayor desempleo se asocia con más morosidad»), que sí queda acotada a «los estudios cuyos signos son verificables». Sugiero una frase que reconozca ese resultado o una aclaración de que el guion cubre solo la tasa de préstamo. |

## Qué no pude verificar
- El PDF renderizado: cursivas, saltos de línea visuales y la posible partición de URL. Revisé solo la capa de texto extraída con `pdftotext`.
- Los `.docx`: comprobé solo su hash, no abrí su contenido.
- Las atribuciones de los demás estudios. Esta ronda solo reconsultó OpenAlex para Obradović y Crossref para Zawadzki. El resto lo comprobé contra la matriz y contra mi ronda 4.
- La procedencia «texto completo» de Golitsis: no tengo el artículo, así que me apoyo en lo que declara la matriz.

Archivos revisados:
- `report/references.bib`
- `research/matriz-literatura.md`
- `report/secciones/02-literatura.qmd`
- `outputs/preview-006/report/informe.md`
- `outputs/preview-006/report/anexo-tecnico.md`
- `specs/006-informe/review-audit-ronda4-verificador-citas.md`
