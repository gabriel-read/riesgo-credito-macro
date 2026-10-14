# Ledger del change Google Docs aplicado — Spec 006

Aplicado por Codex en turno exclusivo el 2026-10-13, por aprobación de Gabriel y relevo de Claude. Motivo: retirar Google Docs como requisito de verificación; sin cambio científico.

## Diff y copias previas

Exactamente seis sustituciones: dos en spec, una en plan y tres en tareas. Todo el resto de esos archivos se conserva byte a byte, incluidos finales de línea. Copias exactas previas y huellas propias recalculadas:

| Archivo | SHA-256 antes | SHA-256 después | Copia previa |
|---|---|---|---|
| spec.md | 481537c0a656f95fa23542bad84aa0e1e18bb3fa2ce222e961b2258e6a8787fb | f4a9593f16f49bccb4178d8731ca71bba3b8fd45349837c184f06fce28d18d2b | spec-v4-antes-google-docs.md |
| plan.md | 668dece325cc012181f8971719061000a50f325801678dfcc460efdb9b89547d | 057975d7f1d35ae3acab9c35b6913e11e94aa34fd96d827e3d1d0f3831634709 | plan-v3-antes-google-docs.md |
| tasks.md | c2015c4f63f6dcf7632bcb6723cfc89812edbcb1bfa00fffd9be397c0df6deb4 | 077a9cb847149bd7fa80547eff5c7bb85e648fd1f36c007ea65e209abd6988e8 | tasks-antes-google-docs.md |

Diff aprobado SHA-256: 78e1dda7fe1394f6354e9b7d769ae45258ce7942aaad6bde160e8c37460dce5f. Relevo SHA-256: afa770f84aaa02014dbbb63378a2304807076887e8b4b19bdf90c967dedba052.

MEMORY.md actualiza el estado de continuidad; copia previa MEMORY-antes-google-docs.md. SHA antes 673a398357fac4de4ac7cdca59b1df067fbfbae653e9ca04fffb2e0d33c7792c; después 56f6a233a9197900693fc9803d522907462701eda1965e7bed7afbf1b217209e.

## R7 y comprobaciones

Manifiesto R7 intacto: 69003c83a7c6ccbc69c5cbd23bbeeb43bde0b970792f53748df302ca574535e5. Los seis PDF/DOCX/GFM, nueve secciones de Claude y 25 módulos científicos coinciden con sus SHA aprobados. Se compararon 583 entradas antes/después: solo spec, plan, tasks y MEMORY cambiaron en este turno. No se modificaron fuentes, productos, paquetes ni evidencias R7. El manifiesto histórico no se reescribe para acomodar el change.

Antes de editar ya diferían pyproject.toml y uv.lock respecto a las entradas del render R7; git diff muestra python-pptx añadido a dev. Se conservaron sin atribuir autoría ni declarar que el entorno actual reproduce R7. Las diferencias anteriores de auditoría/otros registros también se enumeran en el JSON.

Registro completo de entradas antes/después, diferencias preexistentes, sustituciones y salidas: change-google-docs-retirado-huellas.json. SHA-256 del registro: 3cfd17486a7b69c411cac9dec7e1f8750b31f9fce5cdd33457fc5a2aca438749.

## Estado y siguiente acción

Google Docs deja de ser requisito; no se afirma comprobación de los DOCX ni clics en Word/Google Docs. Auditoría vigente ronda 6 sobre R7 APROBADA, registrada por Claude y confirmada por Gabriel; review-audit.md no se toca. Ensayo de preguntas probables pendiente del autor; T12 y 006 abiertas. También pendientes condiciones del profesor: hora límite, extensión, formato, formato/duración de exposición y aceptación del par separado.

Para respetar literalmente el diff, la referencia residual «esa revisión» de tasks.md línea 8 y las notas históricas permanecen. No reinstauran Google Docs: prevalece RF-14b modificado; el ensayo sigue pendiente. No se marca cumplido ni se cierra ninguna tarea.

No suite ni renders, según relevo autorizado para este ajuste documental. No opcionales, cambios metodológicos, cifras, arneses, commits ni push. Se devuelve el ledger a Claude y se detienen modificaciones.
