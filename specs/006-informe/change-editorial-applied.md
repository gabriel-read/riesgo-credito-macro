# Ledger del change editorial aplicado — Spec 006
Aplicado por Claude Code en turno exclusivo cedido por el autor y Codex, 12-oct-2026. Solo se escribieron `spec.md`, `plan.md`, las dos copias de respaldo y este ledger. No se tocaron `tasks.md` (lo actualizará Codex), `src/`, `tests/`, `report/`, `MEMORY.md`, el arnés ni contratos 003–005. Sin commit ni push.

## Aprobación del autor (resumen literal)
- «Apruebo el change editorial coordinado: dos documentos, slugs y registro, anexos A–F, T13–T15 y nuevo orden.»
- «Mantén una alternativa de entrega combinada si el profesor no acepta material separado. No presentes esa aceptación como confirmada.»
- «No apruebo una suite parcial como sustituto del criterio global, pero puedes avanzar la redacción mientras Codex los diagnostica.»
- Turno cedido solo para `spec.md` y `plan.md`: conservar bytes exactos previos, aplicar v4/v3, fecha y razón, sin metodología nueva.
- Razón: informe principal narrativo con anexo técnico completo separado, sin extensión arbitraria y sin eliminar evidencia requerida.

## Huellas (sha256)
| Archivo | Antes | Después |
|---|---|---|
| `spec.md` | `caf97028a2b236404cc00bbe2fe40253f2d48ecd58fc686417091ca3bf3ad3df` (v3 aprobada; copia `spec-v3-approved.md`) | `13d2d84ddd1538c25687b1b901da39c51f7f5bb95bcc38037d3637fcadeae5fa` (v4) |
| `plan.md` | `61262159fecad4d396db4d3d7043d86db0e9ea1d843c65655d5e9eafa8802f17` (v2 aprobado; copia `plan-v2-approved.md`) | `f3686e3c5918baec1e4639c3617322264d6847416561ce303e1c45896a084336` (v3) |
| `tasks.md` | `1505a5d92a647075c42c56053f8b7edb27b66efda9791dfe3cf9f9d1803f57bc` (sin tocar; v2 aprobado era `49b874d1…`) | pendiente: lo actualiza Codex |
| `change-editorial-draft.md` | `c6ccfa47da00c5a9b95b449b240df4a1c0492a23e95c1f6cfa6c997a73d078f8` | sin cambios |
Las copias `spec-v3-approved.md` y `plan-v2-approved.md` coinciden byte a byte con los originales aprobados (verificado con sha256 antes de editar).

## Qué cambió
- **spec v4:** estado y resumen del cambio; párrafo «Cambio editorial v4» en Estructura obligatoria (dos documentos, slugs, registro, no duplicación, anexos A–F, esencial en el cuerpo, figuras sin recortar, 2.5 con variables, método y signos permitidos, alternativa combinada no confirmada); RF-3, RF-14 (dos documentos), RF-14b nuevo (enlaces), RF-15 (registro), RNF-6 (remisiones), criterios de finalización (cobertura del registro, criterio global de suite) y dudas abiertas (material separado).
- **plan v3:** §1a nueva (dos documentos y registro), nota de propiedad en §2, adición a §3b (adaptador, pies y notas, clasificación del Panel 5), tests nuevos en §4, §5b (enlaces) y orden vigente en §6 (T1–T4 → T13 → T14 → T15 → T10 → T5–T9 → T11 → T12).
- **Sin cambios:** RF-1, RF-2, RF-4 a RF-13, RNF-1 a RNF-5, hallazgos heredados, contratos y productos 001–005, `data/raw/`.

## Pendiente para Codex (no hecho aquí)
Actualizar `tasks.md` a v3 con T13 (registro y slugs), T14 (anexo técnico y versiones reducidas), T15 (render doble, índices y enlaces), alcance nuevo de T5–T9 y orden; conservar T1–T4 sin renumerar y el respaldo `tasks-v2`; registrar su hash. Implementar bajo el cierre global de suite pendiente.

## Cesión
Termino mi turno exclusivo. **Cedo la escritura del checkout a Codex.**

## Corrección formal posterior (Claude Code, 12-oct-2026, turno exclusivo cedido por Codex)
- **Razón:** el guardarraíl `test_specs_declare_state` exige `Estado: borrador|aprobada|implementada`; los encabezados puestos (`Estado: v4` y `Estado: v3`) lo incumplían. Evidencia en rojo: `1 failed, 878 deselected` (falta 'Estado:' en `spec.md`). Como el autor aprobó el change, el estado formal es aprobado. **No cambia el alcance**: solo se modificó la palabra inicial de la línea de estado de cada archivo.
- Cambio: `spec.md` → `Estado: aprobada v4`; `plan.md` → `Estado: aprobada v3`. Tras el cambio el mismo test pasa.
- **Huellas que sustituyen a las de la tabla anterior:** `spec.md` `481537c0a656f95fa23542bad84aa0e1e18bb3fa2ce222e961b2258e6a8787fb`; `plan.md` `668dece325cc012181f8971719061000a50f325801678dfcc460efdb9b89547d`. Las anteriores (`13d2d84d…` y `f3686e3c…`) quedan como historial del primer aplicado.
- **Aclaración sobre `tasks.md`:** su hash en el momento de este registro es `1505a5d92a647075c42c56053f8b7edb27b66efda9791dfe3cf9f9d1803f57bc`. El aprobado v2 era `49b874d1…`. La diferencia no es una modificación mía (no lo toqué); no se declara que coincida con el original ni se atribuye una causa. Queda para el historial de comprobaciones de Codex al actualizar `tasks.md` a v3.
- Cierre global de suite pendiente; implementación autorizada por el autor. Solo escribí encabezados de `spec.md` y `plan.md` y este apéndice.

## Cesión
Termino este turno. **Cedo la escritura del checkout a Codex** para `tasks.md` v3 y T13.

## Aplicación de tareas por Codex
Se conserva `tasks-v2-executed.md` con SHA `1505a5d92a647075c42c56053f8b7edb27b66efda9791dfe3cf9f9d1803f57bc`: contiene los checkboxes y evidencias T1–T4 posteriores a la aprobación original49b874d1. `tasks.md` v3 añade T13–T15 y orden vigente aprobados. SHA de la aplicación inicial: `f44e4e2d0b830c3957d4da3a66f57174a0949c6482ffa1e9b47816d95aefdd7d`. El seguimiento posterior cambia checkboxes/evidencias, no se atribuye a Claude. Los nuevos criterios mantienen cierre global pendiente de suite completa.
