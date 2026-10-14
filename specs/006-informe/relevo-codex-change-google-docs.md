> **LISTO PARA EJECUTAR (2026-10-13).** El aviso previo «en espera» se conserva como historial: el diff no estaba aprobado hasta el mensaje de Gabriel registrado abajo.

# Relevo a Codex — aplicar el change «Google Docs deja de ser requisito de cierre» (spec 006)

De: Claude Code · Fecha: 2026-10-13 · Autorización: Gabriel aprobó el diff en un mensaje posterior a la corrección de registros del 2026-10-13: «Apruebo también el diff previamente revisado de change-google-docs-retirado.md. Entrega a Codex el relevo para aplicarlo conservando el historial y R7 intacto. No marques cumplido el ensayo del autor.» Sin commit ni push.

## Qué debes hacer (solo esto)

1. **Antes de editar**, copia los bytes actuales con nombre de procedencia y registra el SHA-256 de antes: `spec.md` (v4 aprobada), `plan.md` (v3 aprobado) y `tasks.md`. Por ejemplo `spec-v4-antes-google-docs.md`, `plan-v3-antes-google-docs.md`, `tasks-antes-google-docs.md` (los nombres son sugerencia tuya).
2. Aplica **exactamente** el diff de `change-google-docs-retirado.md` (sección «Diff propuesto»): RF-14b (última oración), viñeta de cobertura de «Criterios de finalización», `plan.md` línea 94 y `tasks.md` líneas 3, 8 y 141. No toques las menciones históricas de Google Docs (evidencias de rondas 1–7, `docs/importacion-google-docs-006-ronda7.md`, rondas de auditoría).
3. Registra en un ledger (por ejemplo `change-google-docs-retirado-aplicado.md`) SHA-256 antes/después, fecha y motivo, igual que en `change-editorial-applied.md`.
4. No cambies metodología, resultados, contratos ni pre-registros; no es un cambio científico.

## Qué no debes hacer

- **No modifiques R7** (fuentes, entregables, manifiesto `docs/huellas-paquete-auditoria-006-ronda7.json`) ni vuelvas a renderizar o ejecutar la suite por este cambio: es un cambio de requisito de verificación y de texto de spec/plan/tasks.
- No apliques los opcionales cosméticos R6-1 a R6-5 (decisión del autor).
- No marques el ensayo de las preguntas probables como cumplido (lo hace y lo marca el autor).
- No marques T12 ni cierres 006: faltan el ensayo de las preguntas probables (autor) y las condiciones de entrega que la guía oficial no resuelve (hora límite oficial, extensión, formato exigido, formato y duración de la exposición, aceptación del par informe-anexo separado). Esta auditoría tampoco los marca.

## Estado que dejo escrito por Claude (no tocar)

- `review-audit.md`: añadida arriba la sección «Veredicto vigente (2026-10-13)» (APROBADO, ronda 6 sobre R7); la ronda 1 y el resto del archivo quedan intactos. Copia previa: `review-audit-antes-veredicto-vigente.md`.
- `change-google-docs-retirado.md`: estado actualizado a «diff aprobado».
- Rondas 1–6 y copias de los revisores: intactas.

## Devolución

Al terminar, deja el ledger y avisa. Esta solicitud no abre una auditoría general. Turno de escritura: lo cedo a Codex solo para estos tres archivos y su ledger.
