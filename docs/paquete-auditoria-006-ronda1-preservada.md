# Paquete para T12 — auditoría independiente de 006

Copia única: `C:/Users/gabri/orca/riesgo-credito-macro`. HEAD `7a3dd2a`, rama `spec/004-modelo-ii`. Codex terminó T11: `specs/006-informe/review-validate.md`, validación técnica del autor APROBADA; suite completa: 905 tests aprobados, 567 avisos, 963,43 s, rc 0, sin exclusiones. No hay commit ni push. **006 permanece abierta.**

## Artefactos y criterios para revisores de contexto limpio

- Contratos originales vigentes: `docs/constitution.md`, `docs/guia-profesor.md`, `specs/006-informe/spec.md` v4, `plan.md` v3 y `tasks.md`; pre-registros aprobados de 003–005. No usar las conclusiones del implementador como veredicto independiente.
- Informe principal completo: `outputs/preview-006/report/informe.pdf` y `informe.docx`, once secciones; fuentes Quarto `report/informe.qmd` y `report/secciones/`.
- Anexo completo: `outputs/preview-006/report/anexo-tecnico.pdf` y `.docx`, A–F. Fuente `report/anexo-tecnico.qmd` y `report/anexos/A-*.qmd` a `F-*.qmd`.
- Registro, slugs, lectores y correspondencia: `outputs/informe/registro.csv`, `enlaces.csv`, `trace.json`, `body_trace.json`, `specs/006-informe/interfaz.md`, tablas/figuras científicas originales y ambos JSON de modelos. `report/_variables.yml` sigue canónico.
- Citas: `report/references.bib`, `report/apa.csl`, `research/matriz-literatura.md` y sus evidencias. Los registros de clic no prueban acceso completo a artículos con CAPTCHA/403; no convertir acceso limitado en una corrección metodológica ni alterar citas sin verificar.
- Controles reproducibles del autor: `docs/validacion-h2-006-2026-10-12.json`, `docs/pytest-completo-h2-006-2026-10-12.log/json`, `docs/repro-render-006-h2-2026-10-12.json` y `docs/enlaces-pdf-006-2026-10-12.json`. Son evidencia del autor, no auditoría independiente.

## Propiedad y turno exclusivo

Claude escribió nueve secciones en T5–T9; Codex escribió siete en T10 y la infraestructura. Claude coordina T12, **sin atribuir independencia a la revisión de su propio texto**. Los tres revisores deben recibir contexto limpio, solo rutas y criterios: revisor-econométrico, verificador-citas y profesor-evaluador. Conservar sus informes íntegros y autoría real.

Al enviar el relevo, Codex cede escritura exclusivamente de `specs/006-informe/review-audit*.md` y `solicitudes-claude.md`. Los revisores leen el checkout y entregan sus informes a Claude; no modifican código, redacción, variables, datos, specs o planes. Codex no escribe en el checkout durante ese turno. Cualquier bloqueante se entrega al escritor correspondiente en un nuevo relevo; una corrección por vez dentro del contrato. Sin aplicar opcionales ni hacer commit/push. Si falta cuota, registrar continuidad; no transferir auditoría al implementador.

## Pendientes externos explícitos

- Google Docs es comprobación adicional de la versión importada, **todavía no verificada** y requerida por RF-14b/criterios de cierre. La instrucción actual permite continuar T12 mientras se coordina; no permite declarar 006 cerrada ni sus enlaces funcionales. Procedimiento del autor: `docs/revision-google-docs-006.md`.
- Confirmaciones del profesor sobre fecha/formato y aceptación del par separado; alternativa combinada disponible. No enviar mensajes al profesor ni subir archivos por cuenta del autor.

## Huellas actuales

Inventario exhaustivo de los archivos entregados y sus rutas absolutas: `docs/huellas-paquete-auditoria-006-2026-10-12.json`. Comparar esos bytes antes de auditar. Si cambian, identificar la diferencia y pedir el relevo correspondiente; no usar una copia vieja.


## Relevo confirmado del 12 de octubre de 2026

T11 APROBADA en review-validate.md. Suite completa: **905 tests aprobados, sin exclusiones**. No se han repetido pruebas ni renders para este relevo.

### Version validada: rutas absolutas y SHA-256

Las siete huellas siguientes se recalcularon de los archivos actuales y coinciden con el inventario anterior a T12. No cambiaron los artefactos.

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf | 49fcfe2ac7b742f68ae66350746d842833da09668854f1594e066f19bb62e16a |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx | cf5cbf6f0ba7225497218ff279d720a9cee654b88ba213b9964316fb163eead4 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf | 4db7863782aba0bfe33759177f7652835c41e27db924712bffbe9f574729b6c0 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx | 84a675d9e37756ef8950f9fb8106b8c24ace2799f1e9ca7877ba3ffb5f477c75 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/informe/registro.csv | b821cd51730cac46e849da7f5099cfdf6a603faf99dbe7b2a20e9dedc31d9fc0 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/informe/enlaces.csv | 441a28fe32f8489c347d74be522191d0172ed2e30fc78432403b8df27eaae7bd |
| C:/Users/gabri/orca/riesgo-credito-macro/report/_variables.yml | 2695ada1f4769333ae0cc76e59c0db3ca8dc8e5c504ae7087aa506cafe018140 |

report/_variables.yml es la fuente de verdad; la copia de la raiz es generada e ignorada por Git.

### Lista unica de pendientes actuales

1. T12: consolidar los tres informes independientes con autoria real y emitir el veredicto. Hay hallazgos preliminares del verificador de citas y profesor evaluador; falta completar la revision econometrica. No existe aprobacion consolidada ni se corrige contenido durante este turno. Los bloqueantes definitivos se delimitan en review-audit.md y se atienden en otro relevo, conservando esta version como evidencia.
2. Google Docs: importacion desconocida y revision no verificada. RF-14b y los criterios de cierre exigen comprobar ambos DOCX importados: legibilidad, once secciones, anexos A-F completos, indice y navegacion mediante clic. Requiere URLs reales facilitadas por el autor o evidencia manual identificable; ningun agente sube archivos ni inventa URLs. No bloquea iniciar T12, pero si el cierre global. Procedimiento: docs/revision-google-docs-006.md.
3. Confirmaciones externas de fecha/formato y aceptacion de los dos documentos separados; alternativa combinada disponible. No enviar mensajes al profesor.
4. Limitaciones de acceso bibliografico: nueve barreras CAPTCHA/403 y cuatro respuestas finales no confirmadas en la evidencia de clic. Los clics verificados no acreditan lectura completa de esos articulos; T12 registra las limitaciones y hallazgos concretos.

### Cesion exclusiva

Claude confirmo una pausa de escritura para esta actualizacion documental. Al recibir la confirmacion de entrega, se le devuelve el turno exclusivo para coordinar T12 y escribir specs/006-informe/review-audit*.md y specs/006-informe/solicitudes-claude.md. Los revisores trabajan en lectura y entregan sus informes a Claude; su revision de texto propio no se atribuye como independiente. Codex detiene toda modificacion del checkout tras entregar este paquete. No se cambian codigo, redaccion, salidas, contratos ni variables. No se ejecutan tests, renders, commit ni push. Si falta cuota, se registra el punto de continuidad sin transferir automaticamente la auditoria al implementador. **006 permanece abierta.**
