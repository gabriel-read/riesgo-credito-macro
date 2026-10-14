VEREDICTO: CAMBIOS NECESARIOS

# Validación técnica del autor — avance editorial 006

Codex, 12-oct-2026. Copia: `C:/Users/gabri/orca/riesgo-credito-macro`. Esta revisión documenta una vista previa; no cierra T11 ni sustituye la auditoría independiente.

## Comprobaciones realizadas

- Cambio SDD aprobado aplicado: spec v4, plan v3, tareas v3 y antecedentes conservados. T13–T15 implementadas, T10 redactada por Codex y T5–T9 redactadas por Claude en turno exclusivo finalizado.
- Última comprobación focalizada: **68 passed, 5,39 s** en pruebas editoriales, tablas, informe y arnés. Perfil combinado: regresión primero en rojo por archivo ausente y después verde. La suite completa no se ha sustituido por esta ejecución.
- Informe principal PDF: **30 páginas**, 11 secciones, ocho tablas incluidas la tabla cualitativa y tres figuras esenciales. Anexo PDF: **133 páginas**, A–F, 44 fuentes registradas, 110 tablas de paneles en DOCX y nueve figuras originales. Contactos visuales de todas las páginas examinados; detalle de φ en página 53 y Motivo en página 33 del anexo.
- Las 110 tablas DOCX coinciden con las filas de presentación generadas desde CSV. Se decodifican las barras escapadas del Markdown al comparar texto visible; no se alteran cifras. Todas las figuras del anexo conservan los bytes de los PNG originales dentro del DOCX.
- Los 44 identificadores tienen marcadores DOCX. Ambos archivos del anexo existen junto al informe y los vínculos relativos están presentes en el DOCX y el PDF. Esta es comprobación estructural; no certifica navegación mediante clic ni su conservación tras importar a Google Docs.
- Etapa `report` repetida: **195 archivos idénticos** por SHA-256. **99 fuentes/salidas protegidas** coinciden con el inventario anterior. `report/_variables.yml` sigue siendo canónico, con espejo raíz generado. Sin estimaciones nuevas ni cambios de salidas 003–005.
- Playbook: recuperación de base versionada autorizada y comprobada, blob `9695dd9b8224e683d3e7fb92de6912c72883ac5c`. Modificaciones locales anteriores no recuperadas; intención del borrado desconocida. Test de enlaces intacto.
- Alternativa combinada: perfil `combinado`, render PDF/DOCX rc 0; PDF de 162 páginas y DOCX de 118 tablas. Marcadores y destinos internos DOCX comprobados estructuralmente, sin vínculos externos al anexo. La comprobación visual realizada corresponde a las vistas separadas; no se certifica clic ni paginación de la combinada en Word.

Evidencia detallada: `docs/qa-editorial-006-2026-10-12.json`, `docs/avance-editorial-006-2026-10-12.json`, `outputs/informe/trace.json`, `body_trace.json`, `registro.csv`, `enlaces.csv` e `interfaz.md`. Maqueta anterior de 122 páginas conservada en `outputs/smoke-006/evidencia-g1-original-122/`.

## Pendientes actuales

1. Revisar y aprobar por separado H2 antes de modificar `tests/test_frozen_stress.py`. Propuesta e inventario exacto: `docs/reparaciones-arnes-006-propuesta-2026-10-12.md` y `docs/inventario-h2-propuesto-006-2026-10-12.json`. El fixture continúa intacto.
2. Ejecutar y completar **`uv run pytest -q` sin exclusiones**, después de la reparación autorizada. T11 y el cierre global siguen abiertos.
3. Verificar navegación real y paginación en Google Docs después de la importación por el autor; no hay Word licenciado. No se usan URLs ficticias de Drive.
4. Completar auditorías independientes de T12 sobre la versión validada. La redacción de Claude no constituye auditoría de su propio texto.
5. Confirmar con el profesor fecha/formato oficial y aceptación de documentos separados. La alternativa combinada conserva el contenido completo; su render se documenta separadamente.
