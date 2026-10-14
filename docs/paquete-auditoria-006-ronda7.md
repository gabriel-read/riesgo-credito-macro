# Paquete final nuevo — 006, ronda 7

Codex → Claude. Copia exclusiva C:/Users/gabri/orca/riesgo-credito-macro. Comprobación **acotada** R5-1–R5-5, ajuste R5-6 recibido y regresiones; no auditoría general ni reapertura de decisiones científicas. Ronda 6 aprobada independientemente en auditoría ronda 5 corresponde a la versión anterior, no acredita automáticamente esta.

Detalle de cambios: docs/correcciones-tecnicas-006-ronda7.md. Cesión de Claude: docs/cesion-claude-006-ronda5.md. Solo 02 cambió antes de recibir turno, SHA anterior f9e29fca813729959ef9ae86bc34588eb8b31cca3782e5ecf49f34cfd27b81ce. Nueva SHA exacta abajo, otras ocho intactas. R6 completo preservado en outputs/preview-006-ronda6-evidencia/snapshot/; su 02 original en 02-literatura-ronda6-original.qmd y su 02 recibida separadamente. Todos los paquetes/validaciones/auditorías anteriores se conservan.

## Nueve fuentes de Claude

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/01-introduccion.qmd | be47254ba13d3e1ec9f1e2d0e93ebc230b06d08874aeb137be602d59e0c21f4c |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/02-literatura.qmd | 01a299dde5591e6e2a344eb6faa122f7380628b8818a892795733b0dc63aac73 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/03f-limitaciones.qmd | 8f97f714fed4d81094ba4a0f6e33ca5040bb57e11bb6d09bb6774b5adeb4f307 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/04-modelo1.qmd | a6d3f2a1334e6accf3c43e6765c7252b9f9a243157770170278e806137148293 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/05-modelo2.qmd | c88be5b54a363bf31b93ef42641bff3845711b6aca683d81224770a9abba5dcf |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/06-resultados.qmd | 0641ba45ce829b010a6127e4e0c67c1a2807a95872d6f9b45698c53c758e3839 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/07-estres.qmd | f94d7332f971bcd81d1feb2ea880fbc5388462af53313471809de95ce816a4cc |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/08-implicaciones.qmd | c1404f1f992636bfd0ee7c74cc6ffe9079aba9c0b77214792a5aa1350e785891 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/09-conclusiones.qmd | f24a85006086595753fb0066a43b010b6c16e466f46b5a33e74ef108eced4a84 |

## Seis entregables regenerados desde entradas estables

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf | 658814c512685718f8a06ec3362ef3fa07d4636653ed38d34f79b208a1a487ad |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx | 7917fcf0c7daccd699587766a693fa4738cd05383eaa2f1d00063e6b711cca22 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.md | 6704875411ad0d4baf8732606521f1950d0638337eaa1ddeef8e9e70ece6002c |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf | 73bbdfabd0f4cd84b347507fc602d990bac6f3267595fb3569383ddc142a0fcd |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx | c51d02cb4d2c0755903403532d28c42c076437f1a020c670a37e37bc4130dc67 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.md | 2cb012c6a3484fbae1472dd6e9d745202c4272b993e02b8fbb86f274934b6c52 |

Manifiesto nuevo: docs/huellas-paquete-auditoria-006-ronda7.json. Incluye código, fuentes, plantillas, variables, registro.csv, enlaces.csv, todos los productos de presentación y nota stress_delta_nota.md directa, evidencias y entregables con SHA-256 completo.

## Generación trazada

- `C:/Program Files/Quarto/bin/quarto.exe render report/anexo-tecnico.qmd --to typst --no-clean` — rc 0; docs/render-006-ronda7-final-1-typst.log
- `C:/Program Files/Quarto/bin/quarto.exe render report/informe.qmd --to typst --no-clean` — rc 0; docs/render-006-ronda7-final-2-typst.log
- `C:/Program Files/Quarto/bin/quarto.exe render --to docx --no-clean` — rc 0; docs/render-006-ronda7-final-3-docx.log
- `C:/Program Files/Quarto/bin/quarto.exe render --to gfm --no-clean` — rc 0; docs/render-006-ronda7-final-4-gfm.log

Repetidos en outputs/repro-006-ronda7 con rc0. 369 entradas con SHA **antes/después de cada render**; sin cambios en los ocho renders finales. Antes, la preparación reconstruyó archivos generados y actualizó mapa de páginas; causas identificadas y estabilizadas antes de afirmar reproducibilidad. Registros de huellas, comandos reales y resultados en preparacion-render-006-ronda7.json, render-006-ronda7-final.json y render-006-ronda7-repetida.json; investigación explicada en docs/investigacion-entradas-render-006-ronda7.md. Huellas finales de entradas coinciden con el manifiesto.

Suite completa **974 passed, 567 warnings, 1093.01 s; rc 0, sin exclusiones**. Primera corrida interrumpida documentada, no usada como aprobación; reinicio completo. Celdas/figuras/44 identificadores, preservación científica y texto de los seis entregables comprobados. Reproducción estricta de contenidos PDF/DOCX, solo diferencias temporales de metadatos permitidas; GFM por bytes, Report×2 208 archivos idénticos. Clics PDF 53+167 internos y 55 URI, ligados a las SHA actuales. Visual: alcance y evidencias en docs/visual-verificada-006-ronda7.json; no Word/Google Docs afirmados.

## Relevo y pendientes

Codex detiene modificaciones y cede turno exclusivo a Claude para comprobación acotada y escribir revisiones/solicitudes, sin editar los productos congelados. No tests/renders por rutina. No presentar coordinación de Claude sobre 02 como auditoría independiente; si requiere ese juicio, revisor de contexto limpio. Guía de importación preparada: docs/importacion-google-docs-006-ronda7.md. El autor debe importar ambos DOCX y dar URLs reales; no se subieron ni se inventaron enlaces.

**Google Docs, 006 y T12 abiertos** hasta comprobación acotada y RF-14b; confirmaciones del profesor pendientes. 007 sin implementación. Sin commit ni push.
