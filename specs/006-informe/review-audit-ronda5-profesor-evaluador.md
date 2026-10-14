# Ronda 5 de auditoría (paquete ronda 6, acotada) — profesor-evaluador (contexto limpio)

Copia del mensaje final del subagente `profesor-evaluador`, tomada de la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 6 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda6.json`, SHA-256 3d25d637c56efff6b335254db0691eee13378d00d8fd45c157cf2331a4e8448a). Rondas anteriores conservadas intactas.

**Veredicto: APROBADO.** Quedan algunos detalles de forma opcionales; ninguno bloquea la entrega.

Esta revisión cubre solo lo que pediste: X2, X3, R5/X4, los restos de lenguaje de proceso y las regresiones. No reabrí X1 ni N10. Las secciones 1 a 11 no cambian de estado respecto de la ronda 4. Solo la 2.5 mejora, y es en la forma. Por eso no repito la tabla sección por sección.

## Qué leí

- `outputs/preview-006/report/informe.md`: secciones 2 y 3 enteras, más la zona de la Tabla 6. El resto lo revisé por búsqueda de texto.
- `anexo-tecnico.md`: las Tablas B.2 y C.3, el panel 5 de robustez, el Anexo E y el Anexo F, también por búsqueda de texto.
- Páginas del informe, en `outputs/preview-006/qa-ronda6-principal/`: las 6, 7, 9, 15 y 21, más las tres hojas de contactos. Las comparé con los contactos congelados de la ronda 5.
- Páginas del anexo, en `qa-ronda6-anexo/`: la 51 (C.3, panel 2) y la 146 (E.1, panel 3).
- Contrasté el anexo con `outputs/preview-006-ronda5-evidencia/report/anexo-tecnico.md` para separar lo nuevo de lo heredado.

## Estado de los hallazgos de la ronda 4

| Hallazgo | Estado | Evidencia |
|---|---|---|
| X2: notas de C.3 y CUSUM | **Resuelto** | La nota del panel 1 está en `anexo-tecnico.md:1460-1462`: «la salida del modelo no exporta un estadístico ni p-valor; se informa el veredicto». La del panel 2 es otra, distinta de la del panel 1 (`:1490-1492`, pág. 51). Ya no aparecen «el CSV no añade una nota» ni «salida aprobada». La Tabla B.2 tiene las mismas notas (`:584-586`, `:613-615`). Al ser otra tabla, no cuenta como repetición. |
| X3: Obradović en el Anexo E frente al informe | **Resuelto** | El Anexo E (`:4750`, pág. 146) dice ahora que el resumen informa una asociación positiva de la tasa de préstamo y que esa tasa no es la de política. Coincide con `informe.md:258-262` y `:302-304`. |
| R5/X4: Tabla 1 y procedencia de Golitsis | **Resuelto** | La tabla ocupa 2 páginas en vez de 3 (págs. 6-7), sin recortes. La procedencia de Golitsis está dentro de la «Nota de la Tabla 1», junto al guion de Obradović y la fuente (`:258-263`). Ya no hay un párrafo suelto. |
| «rezago aprobado» | **Resuelto** | `:490` dice ahora «crédito rezagado». |
| Nota de la Tabla 6 con «pre-registrada» | **Resuelto** | `:1059-1062` ya no habla de proceso. «Pre-registrada» aparece después en el texto como término metodológico, y eso es aceptable. |
| «generalizables» | **Resuelto** | `:248` y el Anexo E (`:4724`) dicen «generalizados factibles (FGLS)». |
| «consultar la matriz» | **Resuelto** | Ya no aparece. Las notas remiten «al contexto de la fuente citada». |
| preregistro / pre-registro | **Resuelto** | El informe y el anexo usan siempre «pre-registro». |

## Regresiones y restos (todos menores; ninguno impide aprobar)

| # | Severidad | Ubicación | Hallazgo |
|---|---|---|---|
| M1 | Cosmética, nueva por el reflujo | Pág. 15 (Tabla 4) y pág. 9 (Tabla 2) | Al acortar la Tabla 1, el texto se reacomodó y la paginación cambió. La pág. 15 termina con el título, el encabezado y una sola fila de la Tabla 4 (Breusch-Godfrey); el resto pasa a la pág. 16. La Tabla 2 deja 2 filas en la pág. 9. En la ronda 5 esas tablas también se partían, pero con más filas en la primera página. |
| M2 | Cosmética, heredada | Pág. 21 (Tabla 6) | El número, el título y el enlace de la Tabla 6 quedan al pie de la pág. 21 y los datos pasan a la 22. Ya ocurría en la ronda 5 (págs. 22-23). |
| M3 | Menor, heredada (misma familia que X2) | `anexo-tecnico.md:1101` | Panel 5 de robustez: «Las celdas vacías de Motivo conservan los vacíos del CSV». Hace referencia al archivo interno. Ya estaba en la ronda 5 (`:1105`). |
| M4 | Menor, heredada (misma familia que «pre-registrada» repetido) | `anexo-tecnico.md:4824-4826` y `:4843` | En el Anexo F, la columna de base dice «Pre-registro de la especificación pre-registrada», que es redundante. Ya estaba en la ronda 5 (`:4833-4852`). |
| M5 | Redacción | `informe.md:259-260` | La nota de la Tabla 1 dice que el guion «remite al signo… descrito en 2.5», pero la tabla ya está en la 2.5. Sería más claro «descrito en el texto que sigue». |

No encontré nada pendiente de resolver en el informe: ni `?@` ni `{{&lt;`. Tampoco quedan restos de proceso en el cuerpo, como «Codex», «ronda», «aprobad» o «CSV» fuera de la sección 11.

## Nota estimada: 94/100 (93 en la ronda 4)

- **Sube un punto:** X2, X3 y R5/X4 están resueltos, y los cinco restos de lenguaje de proceso que señalé, limpios.
- **No sube más:** la decisión del autor de conservar X1 y N10 sigue pesando en la percepción de la literatura. Se suman además los cortes de tabla M1 y M2.
- **Para llegar a 95, sin requisitos nuevos:** evitar que las Tablas 4 y 6 se separen de su título y queden con una sola fila en una página (M1, M2), y limpiar M3 y M4 del anexo. Es menos de media hora.

## Qué no pude verificar

- No calculé los hashes SHA. La correspondencia entre el PDF y las páginas que vi la deduzco de `docs/visual-verificada-006-ronda6.json` y `docs/paquete-auditoria-006-ronda6.md`, que coinciden en el SHA del informe (`4c8710e9…`) y del anexo (`6b99442e…`).
- No abrí `informe.docx` ni `anexo-tecnico.docx`, porque son binarios. Tampoco vi la importación a Google Docs (RF-14b).
- No probé los enlaces internos ni los DOI.
- No leí el anexo página por página. Solo vi la 51 y la 146; lo demás, por búsqueda de texto.
- Las diapositivas quedan fuera, porque son de la spec 007.
