VEREDICTO: APROBADO

# T11 — Validación técnica del autor, 006

Codex, 12-oct-2026. Copia: `C:/Users/gabri/orca/riesgo-credito-macro`; HEAD `7a3dd2a`, rama `spec/004-modelo-ii`. Este veredicto aprueba la validación técnica del autor y habilita entregar T12. **No cierra 006 ni sustituye la auditoría independiente.** Por la instrucción actual del autor, Google Docs es una comprobación adicional de la versión importada: sigue pendiente y es obligatoria para el cierre por RF-14b y los criterios de finalización. No se afirma que sus enlaces funcionen ni se modifica ese contrato.

La revisión parcial anterior se conserva byte por byte en `review-validate-editorial-parcial-2026-10-12.md`. Spec v4, plan v3, pre-registros y salidas científicas intactos. Sin commit ni push.

## H2 y suite completa

Se contrastó el catálogo antes de aplicar H2 con las salidas exactas de los planes 001 §4, 002 §4, 003 §4, 004 §4 y 005 §6: **78 rutas científicas**, de ellas **18 modificables exactas** de estrés. La 002 no escribe en `outputs`; `lit_estudios` pertenece a 006 y se verifica en sus pruebas propias. No se copian maquetas ni otros productos QA.

Siete regresiones primero en rojo por controles ausentes; después **7 passed, 8,30 s**, antes de conectar la optimización al fixture. Cubren modificación, eliminación, archivo inesperado con y sin prefijo `stress_`, insumo requerido ausente, exclusión de QA/editoriales y alta inesperada en huellas. Se conservan las dos ejecuciones reales de `stage_stress`, igualdad completa de salidas y YAML, preservación de datos y de bloques `datos`, `modelo1`, `modelo2`. Las huellas se calculan una vez por fase y se reutilizan.

**`uv run pytest -q`: 905 passed, 567 warnings, 963,43 s, código 0, sin exclusiones.** El envoltorio registró 965,62 s incluyendo inicio/finalización. No se sustituyó por suite parcial. Sin dependencias nuevas ni cambios de estimadores. H2 solo modifica `tests/test_frozen_stress.py` y añade `tests/test_frozen_stress_inventory.py`.

Evidencia: `docs/validacion-h2-006-2026-10-12.json`, `docs/pytest-completo-h2-006-2026-10-12.log` y `.json`. Los **100 archivos** del inventario activo previo, incluidos datos, salidas y variables canónicas, conservan sus SHA-256 después de la suite y los renders. H1 conserva la base recuperada por autorización; sus modificaciones locales anteriores siguen sin recuperarse.

## Documentos actuales y correspondencia

| Documento | PDF actual | DOCX actual |
|---|---|---|
| Informe narrativo, once secciones | `outputs/preview-006/report/informe.pdf`, 30 páginas | `outputs/preview-006/report/informe.docx`, ocho tablas y tres figuras esenciales |
| Anexo técnico completo A–F | `outputs/preview-006/report/anexo-tecnico.pdf`, 133 páginas | `outputs/preview-006/report/anexo-tecnico.docx`, 110 paneles y nueve figuras originales |

Las 110 tablas DOCX coinciden con los CSV por la trazabilidad de presentación, decodificando solamente barras escapadas del Markdown. Los nueve PNG originales están presentes por SHA dentro del anexo DOCX. Los 44 slugs tienen marcadores y registro de fuente. Se revisaron visualmente todas las páginas PDF mediante contactos y detalles de φ y Motivo; no se afirma paginación nativa de Word.

La maqueta original de 122 páginas se conserva en `outputs/smoke-006/evidencia-g1-original-122/`. Alternativa combinada disponible mediante perfil `combinado`, PDF162 páginas/DOCX118 tablas; no sustituye la versión de trabajo separada.

## Clics reales y límites

Eventos reales de ratón en el visor PDF nativo de un navegador aislado, con posición leída después de cada clic: **53 destinos internos del informe y 160 del anexo**, coincidentes con sus destinos. También se probaron los **23 destinos URI únicos**: ambos archivos del anexo y 21 URLs de referencias. El DOCX descargado por su enlace coincide en SHA-256 con el original. No son solamente comprobaciones estructurales.

Nueve URLs encontraron CAPTCHA o HTTP403 editorial. Cuatro no tuvieron respuesta final del sitio confirmada durante la observación, aunque el clic y la navegación inicial sí quedaron comprobados. No se declara acceso íntegro a esos artículos ni se cambian referencias por estas barreras; la evidencia previa de referencias sigue disponible para T12.

La primera observación de siete URI fue inconcluyente por el tiempo de actualización del visor. Se conservó y se verificaron las siete mediante un segundo clic estabilizado, sin cambiar el PDF. Antes del navegador aislado, una prueba de teclado perdió la ventana y probablemente envió «18» al chat: se detuvo, se informó al autor y no se contó como navegación verificada. La evidencia aprobada usa destinos leídos de vuelta, sin teclado global.

Evidencia: `docs/enlaces-pdf-006-2026-10-12.json` y JSON de clic en `outputs/preview-006/qa-click/`. **Google Docs no se importó ni se probó.** No se garantiza allí el salto entre archivos locales; no hay URLs ficticias de Drive.

## Render repetido

Se repitieron PDF, DOCX y GFM en `outputs/repro-006-h2-2026-10-12/`, conservando los entregables actuales. No quedan `?@`, `?var`, `{{<`, `[@` o `PENDIENTE` en DOCX ni GFM.

PDF: solo cambian dos objetos de metadatos por documento, exclusivamente fechas de creación/modificación e identificadores XMP. **Todos los objetos de páginas, textos, fuentes, imágenes y enlaces son idénticos.** DOCX: solo difiere `docProps/core.xml`, exclusivamente sus fechas `created`/`modified`, además de las marcas temporales del contenedor ZIP. Todo el contenido, tablas, imágenes y enlaces coincide. No se declara igualdad binaria de los contenedores completos.

La etapa `report` había reproducido 195 archivos idénticos por SHA. `report/_variables.yml` sigue canónico, con espejo raíz generado e ignorado. Evidencia: `docs/repro-render-006-h2-2026-10-12.json` y `docs/qa-editorial-006-2026-10-12.json`.

## Hallazgos heredados y sección que los trata

| Hallazgo/límite | Fuente aprobada | Sección y evidencia completa |
|---|---|---|
| Vintage, historia desde 1998, trece series y muestra | Manifiesto, panel y nota 001 | 3.1, 11; Anexos A/F, AT-FRED-MANIFEST |
| Octubre ausente, 2025T4 sin imputación silenciosa | Nota de datos 001 y variables | 3.1; Anexo A |
| Transformaciones y formas distintas | Estacionariedad 001/003/004 | 3.2–3.5, 4, 5; AT-M1-STATIONARITY, AT-M2-STATIONARITY |
| R² con dummies e interpretación | Modelo I, limitaciones | 3.5, 4; AT-M1-LIMITATIONS |
| Inflación/crédito, impacto/largo plazo, robustez | Coeficientes, efectos y robusteces 003 | 4, 6.1, 8, 9; Anexo B |
| Diagnósticos fallidos y HAC | Diagnósticos 003/004 | 3.5, 4, 5; AT-M1-DIAGNOSTICS, AT-M2-DIAGNOSTICS |
| Evaluación fuera de muestra | Tabla y figura OOS 003 | 4, 6.1; AT-M1-OOS, AF-M1-OOS |
| Rezago, Granger, lectura sin evidencia fuerte | Selección y lectura 004 | 5, 6.2, 7; Anexo C |
| φ: continuación observada, identidad y bandas | LP, nota y figura 004 | 5; AT-M2-LP, AF-M2-RESPONSE |
| Motivo vacío válido y robustez no estimada | Estimaciones de robustez 003 | Anexo B, AT-M1-ROB; nota del Panel5 |
| Coeficiente contemporáneo: muestras y formas | `model2_inputs63` | 6.3; AT-M2-INPUTS63 |
| Asociación/endogeneidad, sin shock identificado | Diseños y limitaciones 003–005 | 3.4–3.5, 5–9 |
| D, crédito observado/supuesto | Salidas 005 y variables | 7; Anexo D |
| Bandas de parámetros, explosivas, fuera de rango | Salidas 005 | 7, 9; AT-EST-LIMITATIONS y sensibilidades |
| Origen/calendario y diferencia entre picos | `stress_origin`, `stress_delta` | 6, 7; AT-EST-ORIGIN, AT-EST-DELTA |
| Literatura verificada y signos no reutilizados | Matriz, BibTeX, tabla derivada | 2, 10; Anexo E |
| Desviaciones y reproducción por pipeline | Desviaciones 003/004, decisiones | 3.5, 11; Anexo F |

## Pendientes del cierre global

1. **Google Docs**: revisión de los DOCX importados, exigida por RF-14b y criterios de cierre. El autor no sabe si están importados; no hay URLs reales ni evidencia. Procedimiento: `docs/revision-google-docs-006.md`. Como comprobación adicional solicitada, no detiene T12, pero sí la declaración de cierre.
2. **T12**: revisores con contexto limpio y criterios aprobados. Claude coordina; no audita como independiente sus nueve secciones. Informes reales y autoría deben conservarse.
3. Confirmación externa de fecha/formato oficial y aceptación del par separado. La alternativa combinada existe, sin afirmar que el profesor la exige.

H1/H2 ya no están pendientes de reparación. La pérdida no resuelta de modificaciones locales del Playbook sigue documentada.
