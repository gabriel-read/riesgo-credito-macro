# Paquete nuevo de auditoría — 006, ronda 5

Codex → Claude, 2026-10-13T17:04:27.299261+00:00. Copia activa **C:/Users/gabri/orca/riesgo-credito-macro**, rama spec/004-modelo-ii. Este paquete sustituye operativamente la entrega histórica ronda 4, conservada sin reescribir sus pruebas ni huellas.

## Versión exacta y fuentes

Comparación inicial auditada: nueve de nueve SHA completas iguales. Cambios posteriores únicos y conciliados: remisiones de 02 y 04 hechas por Claude en su turno R3-X7. Evidencia inicial docs/identidad-fuentes-006-ronda5.json; cesión docs/cesion-claude-006-ronda5.md. Estas son las nueve fuentes finales, preservando C1–C7:

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

Suite y renders se ejecutaron después de estabilizar estas fuentes; la relación no se sostiene solo en fechas: huellas de todas las entradas antes/después, cotejo de celdas y texto real de entregables, y repetición de render con contenido y enlaces idénticos. Fecha/hora adicional de cada ejecución en los JSON. Archivo íntegro de fuentes/entregables/resultados: docs/huellas-paquete-auditoria-006-ronda5.json.

## Entrega regenerada

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf | 8cdfa2a6521594f6d56c3831aa4da022c2f17063abd823c50a18b01144b91878 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx | 994e28fce7fb7850b5aef9487efb0dca915459b8b3357ff2a46be197a0d3c130 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.md | 38e645d0625a831d2cf7d4f11dfed3bedcebfbcbaa8a58a192e9607a4d5c1e32 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf | 58429c72be4563d86420f115f3deaa0d05f5a9e812ddadc5c753ec5689779c22 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx | 75e241c1637c26174e936b6e68f07c8bc58d416084c565c592840030ed91854c |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.md | 71dca3f71d22f61a145d1891f65cd023732d74b8bdbac05e2aee851f35c8a346 |

Principal 36 páginas, anexo 149; once secciones/anexos A–F completos, ocho tablas y 117 paneles, cuatro/nueve figuras, 44 slugs. Registro, enlaces, variables canónicas y espejo están incluidos con ruta absoluta/SHA en el manifiesto. No se recortan anexos.

## Comandos y resultados reales

`uv run pytest -q`: **960 passed, 567 warnings, 917.76 s; rc 0, sin exclusiones**; log y SHA en review-validate-ronda5.md y JSON pytest-completo-006-ronda5.json. Sin exclusiones. Focalizado presentación: 116 passed; once regresiones nuevas.

Render final, todos rc 0 (logs, UTC y duración en docs/render-006-ronda5-entrega.json):

- `& 'C:/Program Files/Quarto/bin/quarto.exe' render report/anexo-tecnico.qmd --to typst --no-clean`
- `& 'C:/Program Files/Quarto/bin/quarto.exe' render report/informe.qmd --to typst --no-clean`
- `& 'C:/Program Files/Quarto/bin/quarto.exe' render --to docx --no-clean`
- `& 'C:/Program Files/Quarto/bin/quarto.exe' render --to gfm --no-clean`

Los mismos cuatro comandos se repiten con `--output-dir outputs/repro-006-ronda5`, rc 0; registro docs/render-006-ronda5-entrega-repetida.json. Comparación estricta docs/reproducibilidad-informe-006-ronda5.json. Report×2 con `uv run python -m src.pipeline report`: 208 archivos idénticos. QA de celdas/figuras/116 protegidos: docs/qa-correcciones-006-ronda5.json; 25 módulos científicos conservados según manifiesto ronda 4.

Otras invocaciones efectivamente ejecutadas, todas rc 0:

- `uv run python C:/Users/gabri/AppData/Local/Temp/qa-report-006-ronda5.py`: celdas/figuras/116 protegidos, log docs/qa-correcciones-006-ronda5.log.
- `uv run python C:/Users/gabri/AppData/Local/Temp/repro-reportstage-006-ronda5.py`: dos ejecuciones report/208 idénticos, log docs/reproducibilidad-report-006-ronda5.log.
- `uv run python C:/Users/gabri/AppData/Local/Temp/repro-report-006-ronda5.py`: comparación estricta de seis entregables, log docs/reproducibilidad-informe-006-ronda5.log.
- `uv run python C:/Users/gabri/AppData/Local/Temp/phrases-docx-gfm-006-ronda5.py`: frases DOCX/GFM, log docs/frases-docx-gfm-006-ronda5.log.
- `node C:/Users/gabri/AppData/Local/Temp/pdf-text-006-ronda5.mjs`: texto real PDF, log docs/extraccion-texto-pdf-006-ronda5-entrega.log.
- `node C:/Users/gabri/AppData/Local/Temp/pdf-edge-outline-006-ronda5.mjs informe` y el mismo con `anexo-tecnico`: 53 y 167 clics reales correctos.
- `node C:/Users/gabri/AppData/Local/Temp/pdf-uri-click-006-ronda5.mjs`: 55 destinos únicos correctos por clic; logs clics-pdf-006-ronda5-entrega-*.log. Solo navegación/destino observado, no acceso íntegro a artículos.

Frases exigidas comprobadas sobre archivos reales finales: ambos textos antiguos cero en PDF/DOCX/GFM; explicación del error estándar tres en principal. docs/frases-pdf-006-ronda5.json y frases-docx-gfm-006-ronda5.json. Visual propio y clics reales: docs/visual-verificada-006-ronda5.json, outputs/preview-006/qa-click-ronda5/, logs clics-pdf-006-ronda5-entrega-*.log. No se presenta como auditoría independiente ni como comprobación de Google Docs.

## Alcance de revisión y cesión exclusiva

Solicito a Claude coordinar la revisión **acotada C1–C7 y R3-X1–X7 por revisores independientes de quienes redactaron/implementaron**, comprobando primero estas nueve fuentes y las seis huellas entregables. Su revisión de su propio texto no se atribuye independencia. Resoluciones/límites: docs/correcciones-tecnicas-006-ronda5.md. No añadir requisitos ni observaciones opcionales, reestimar, modificar fuentes protegidas, ni reutilizar la validación de ronda 4.

Codex termina escritura, tests, pipelines y renders al entregar este paquete. Turno exclusivo a Claude para escribir revisiones/solicitudes de auditoría y coordinar revisores; preservar productos/textos/código congelados. Si aparece bloqueante, registrar ruta y evidencia para corrección posterior, sin sobrescribir producto durante auditoría. Conservar rondas anteriores; distinguir controles ejecutados de pruebas no realizadas.

Pendientes únicos: revisión independiente de esta versión; importación/URLs/paginación/legibilidad/clics de ambos DOCX en Google Docs (RF-14b obligatorio); cierre T12/006 y confirmaciones del profesor. 007 sigue borrador sin aprobación de spec/plan/tareas: no implementar deck. Sin commit ni push.
