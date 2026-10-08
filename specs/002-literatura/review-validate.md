# Informe de validación — spec 002 Literatura

**VEREDICTO: APROBADO**

Fecha: 5-oct-2026. Este informe reemplaza al que redactó la fábrica antes de la auditoría independiente, que declaraba APROBADO sin haber detectado los problemas que halló `verificador-citas` en las rondas 1 a 3 (ver `review-audit.md`).

## Verificación

| Comprobación | Resultado |
|---|---|
| `uv run pytest -q` | 187 passed |
| `uv run python scripts/verify_refs.py` | «Verificadas 21 de 21 entradas», código 0 |
| Auditoría independiente `verificador-citas` (T10, ronda 4) | APROBADO, sin hallazgos bloqueantes (`review-audit.md`) |

## Criterios de la spec

| Criterio | Evidencia | Estado |
|---|---|---|
| RF-5: al menos 20 filas verificadas (≥ 16 estudios + exactamente las 4 de datos/método) | 17 estudios + 4 de datos/método = 21 filas verificadas; `check_minimums` en `tests/test_literature_files.py` | ✅ |
| RF-6: ≥ 2 por sección 2.1–2.4 y ≥ 6 en 2.5 | 2.1 = 2, 2.2 = 2, 2.3 = 2, 2.4 = 2, 2.5 = 9 | ✅ |
| RF-7: referencias de datos y método | `fred2026`, `frb2026`, `newey1987`, `jorda2005` | ✅ |
| RF-9, RF-10, RF-12: `.bib` solo con verificadas, clave apellidoaño, claves coincidentes con la matriz | 21 entradas = 21 filas verificadas; claves apellidoaño | ✅ |
| RF-13 a RF-19, RF-26: script contra Crossref | `scripts/verify_refs.py` + `tests/test_verify_refs.py` (con `fetch`/`sleep` inyectados) | ✅ |
| RF-20: tabla «Resumen» coincide con el conteo | test sin red de coherencia | ✅ |
| RF-22: columnas obligatorias y signo en 2.5 | sin «no aplica» en las filas de 2.5; todas con signo | ✅ |
| RF-21: versión publicada, no preprints | `wilson1997` y `virolainen2004` descartadas por solo existir en SSRN | ✅ |
| RNF-4: auditoría con rutas, sin conclusiones previas | `review-audit.md` | ✅ |

## Cambios hechos por esta validación frente a la entrega de la fábrica

- `scripts/verify_refs.py`: el estado de discrepancia era `"no coincides"` (errata); las entradas por URL ya no exigen que el cuerpo sea JSON de Crossref; el `User-Agent` propio solo se envía a Crossref (FRED cuelga las peticiones con él). Cada arreglo tiene su test.
- Matriz y `.bib`: cambios derivados de la auditoría (ver `review-audit.md`, historial de rondas).

## Pendientes y límites

- `asiamah2026` y `koskei2023` están en `pendiente-lectura` (sin signo respaldado por el resumen); recuperables si se accede a sus textos completos.
- Observaciones no bloqueantes de la auditoría para tratar en la spec 006: asignación de `bernanke1995` (2.1 con 2.4 secundaria), clasificación de `pesaran2006`, `segoviano2006` y `gertler2015`, y matices menores de `koju2018`, `tanaskovic2015`, `nkusu2011` y `obradovic2026`.
- La regla de coincidencia de títulos por subcadena (spec, línea 32) es laxa: un título corto del `.bib` coincidiría con cualquier título de Crossref que lo contenga. No se cambió por requerir `/sdd-change`.
