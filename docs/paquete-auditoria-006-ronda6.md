# Paquete final nuevo de correcciones — 006, ronda 6

Codex → Claude, 13-oct-2026. Copia única C:/Users/gabri/orca/riesgo-credito-macro. Revisión acotada a R4-X2, X3, X4, X5 y P1 y sus regresiones; R4-X1/X6 decididos por el usuario: conservar ambos pasajes de 02. No aplicar opcionales ni nuevas decisiones científicas.

## Fuentes y entrega exactas

Las nueve fuentes de Claude no cambian; 02 completo preservado. Ronda 5 histórica: 337 entradas originales cotejadas y archivadas en outputs/preview-006-ronda5-evidencia/snapshot/, con seis entregables en report/ y nota de estrés aparte. Se conserva también ronda 4. Sus manifiestos/paquetes y auditorías no se actualizan retrospectivamente. Evidencia de identidad: docs/identidad-y-preservacion-006-ronda6.json.

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/01-introduccion.qmd | be47254ba13d3e1ec9f1e2d0e93ebc230b06d08874aeb137be602d59e0c21f4c |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/02-literatura.qmd | f9e29fca813729959ef9ae86bc34588eb8b31cca3782e5ecf49f34cfd27b81ce |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/03f-limitaciones.qmd | 8f97f714fed4d81094ba4a0f6e33ca5040bb57e11bb6d09bb6774b5adeb4f307 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/04-modelo1.qmd | a6d3f2a1334e6accf3c43e6765c7252b9f9a243157770170278e806137148293 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/05-modelo2.qmd | c88be5b54a363bf31b93ef42641bff3845711b6aca683d81224770a9abba5dcf |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/06-resultados.qmd | 0641ba45ce829b010a6127e4e0c67c1a2807a95872d6f9b45698c53c758e3839 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/07-estres.qmd | f94d7332f971bcd81d1feb2ea880fbc5388462af53313471809de95ce816a4cc |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/08-implicaciones.qmd | c1404f1f992636bfd0ee7c74cc6ffe9079aba9c0b77214792a5aa1350e785891 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/09-conclusiones.qmd | f24a85006086595753fb0066a43b010b6c16e466f46b5a33e74ef108eced4a84 |

Entregables nuevos, regenerados después de las correcciones técnicas:

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf | 4c8710e9f6e0ba75201aae9af001c3a6f1fee4ce2e287c419954d4fb64454e74 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx | e63338782f2f962fab0462413a7495419f647f6772a93e1727fa3d2fae9d26d8 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.md | c406a99835ddf201924be68adf2ce9841ceeb129e061c273854453f63f5026d7 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf | 6b99442e653b5a1e07d432318003669f09f866068518a5d57826f21f25e5ff16 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx | 8ebfd114df6d2b2a82a18248826fa64d7fc0f3fc3005e49c3d6e8a9d83db7595 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.md | 801a141e6763a144ef53cdad85e8bdf3c5aa3a5da6ad5f6e3fcac4092149b967 |

Manifiesto nuevo: docs/huellas-paquete-auditoria-006-ronda6.json; incluye entradas y fechas adicionales, sin inferir correspondencia solo de fechas. Todas las fuentes se contrastan antes/después de suite/render y al congelar; celdas y texto real se cotejan con fuentes. Registro/enlaces, variables canónicas/espejo, código, filtros, plantillas, tests, fuentes protegidas, resultados y **todos los productos de outputs/informe/** están ligados por SHA completo.

## Resolución y nota antes omitida

R4-X2–X5: docs/correcciones-tecnicas-006-ronda6.md. Lenguaje interno sustituido por explicaciones al lector; vacíos intactos; nota de Obradović respaldada por el resumen registrado, sin nueva lectura ni signo de política; FGLS generalizados frente a resultados generalizables; nota Golitsis asociada y tabla en dos páginas sin eliminar contenido. 02 no se edita. Spec/plan y fuentes científicas intactos.

R4-P1: en ronda 5 no existía entrada propia para stress_delta_nota.md. La cubría indirectamente la entrada C:/Users/gabri/orca/riesgo-credito-macro/docs/reproducibilidad-report-006-ronda5.json (SHA 1e39e95f79e676979c155ee31f1d5e1f3ed40371e6ec87f8f781c97d67386956), cuyo mapa sha256_by_relative_path registra la nota. Ronda 6 la incorpora directamente:

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/informe/stress_delta_nota.md | 733d7017c257017157a4644ced7b4069c8b3559cbeb7ce65886caf36caa8c935 |

La nota conserva los mismos bytes; el YAML canónico coincide con ronda 5 y con su espejo. La regeneración posterior a PDFs con idéntico contenido no altera su identidad; no se usa su mtime como prueba suficiente.

## Comandos ejecutados y resultados

`uv run pytest -q`: **967 passed, 567 warnings, 951.69 s; rc 0, sin exclusiones**. Log/SHA y huellas antes/después en docs/pytest-completo-006-ronda6.json. 123 focalizados de presentación; siete tests nuevos, rojos previos conservados. No exclusiones ni reducción de controles.

Render definitivo (registro real de argv, UTC/duración/log/SHA: docs/render-006-ronda6-entrega.json):

- `& 'C:/Program Files/Quarto/bin/quarto.exe' render report/anexo-tecnico.qmd --to typst --no-clean` — rc 0.
- `& 'C:/Program Files/Quarto/bin/quarto.exe' render report/informe.qmd --to typst --no-clean` — rc 0.
- `& 'C:/Program Files/Quarto/bin/quarto.exe' render --to docx --no-clean` — rc 0.
- `& 'C:/Program Files/Quarto/bin/quarto.exe' render --to gfm --no-clean` — rc 0.

Los cuatro se repiten con --output-dir outputs/repro-006-ronda6, rc0; docs/render-006-ronda6-entrega-repetida.json. Comparación estricta de PDFs/DOCX/GFM con uv run python C:/Users/gabri/AppData/Local/Temp/repro-report-006-ronda6.py, rc0: solo metadatos temporales diferentes, GFM exactos. Report×2 con uv run python -m src.pipeline report: 208 iguales (helper repro-reportstage-006-ronda6.py, rc0).

QA con uv run python C:/Users/gabri/AppData/Local/Temp/qa-report-006-ronda6.py, rc0: todas las celdas/figuras y 44 bookmarks, 116 protegidos intactos; 25 módulos científicos comparados con manifiesto anterior. Principal 35 páginas/anexo 149, ocho tablas/117 paneles. Texto real PDF con node C:/Users/gabri/AppData/Local/Temp/pdf-text-006-ronda6.mjs, rc0; DOCX/GFM con phrases-docx-gfm-006-ronda6.py, rc0. Verificación de términos y pasajes: docs/lectura-verificada-006-ronda6.json.

Visual propio y huellas de imágenes: docs/visual-verificada-006-ronda6.json. Clics node pdf-edge-outline-006-ronda6.mjs informe/anexo-tecnico: 53 y 167 correctos, rc0; node pdf-uri-click-006-ronda6.mjs: 55 URI únicos correctos, rc0. Datos actuales con SHA en outputs/preview-006/qa-click-ronda6/ y logs clics-pdf-006-ronda6-entrega-*.log. Es verificación de Codex, no de los auditores ni de Google Docs; navegación externa no asegura acceso completo a la fuente.

## Relevo y pendientes

Codex detiene modificaciones de fuentes/productos, tests, pipeline y renders al entregar este paquete. Cede turno exclusivo a Claude para coordinar revisión acotada con revisores independientes de redactores/implementadores y escribir únicamente revisiones/solicitudes. Preservar los productos congelados y las rondas anteriores; no atribuir independencia a revisar su propio texto ni ampliar alcance.

Pendientes: revisión acotada de esta versión; Google Docs RF-14b (importación/URLs/legibilidad/paginación/clics de ambos DOCX aún desconocidos); 006/T12 y confirmaciones del profesor. 007 solo borrador de spec, sin plan/tareas aprobados ni deck. Sin commit ni push.
