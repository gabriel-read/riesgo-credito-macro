# Tasks — Spec 002 Literatura

1. ✅ COMPLETADA — **Implementer** — `src/references.py`: dataclasses (`BibEntry`, `MatrixRow`, `Mismatch`), constantes (`MATRIX_COLUMNS`, `STATES`, `TYPES`, `GUIDE_VARIABLES`, `SUPPORTS`, `DATA_METHOD_KEYS`, `KEY_PATTERN`, `SIGN_WORDS`) y funciones de lectura y normalización (`parse_bib`, `parse_matrix`, `normalize_doi`, `normalize_title`, `normalize_surname`, `first_author_surname`, `is_institutional`).
   - RF-4 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_references.py::test_parse_bib`, `test_parse_matrix`, `test_normalize_doi`, `test_normalize_title`, `test_normalize_surname`, `test_first_author_surname` en verde; `parse_bib("@article{a,{...}")` falla con el número de línea si usa comillas.

2. ✅ COMPLETADA — **Implementer** — `src/references.py`: validación y comparación (`validate_matrix`, `summary_counts`, `validate_summary`, `check_minimums`, `validate_bib`, `check_coherence`, `crossref_url`, `parse_crossref`, `crossref_years`, `compare_record`), más sus tests; añadir `src/references.py` a las listas de módulos puros y a los imports prohibidos de `tests/test_pipeline.py`.
   - RF-5, RF-6, RF-7, RF-10, RF-11, RF-13, RF-15, RF-20, RF-22, RF-23, RF-24, RF-25, RNF-6 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_references.py` en verde con todo lo anterior; `check_minimums` con 15 estudios o 2.3 con 1 devuelve error; `compare_record` detecta título/autor/año distintos; `tests/test_pipeline.py` en verde sin `requests`, `urllib`, `socket` ni `open` en `src/references.py`.

3. ✅ COMPLETADA — **Implementer** — Plantilla vacía de la matriz (`research/matriz-literatura.md`: cabecera, «Resumen» en cero, «Matriz» sin filas) y `.bib` inicial (comentario UTF-8 + entrada FRED de la spec 001 ya congelada); `tests/test_literature_files.py` que parses ambos archivos y valida que `validate_matrix`, `validate_summary`, `validate_bib` y `check_coherence` devuelven `[]`.
   - RF-4, RF-9, RF-12, RF-20 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_literature_files.py` en verde sobre los archivos reales; `check_minimums` no se incluye aún (D14).

4. ✅ COMPLETADA — **Implementer** — `scripts/verify_refs.py` (E/S: `http_get`, `get_with_retries`, `check_doi_entry`, `check_url_entry`, `run`, `main`) y sus tests con `fetch`/`sleep` inyectados.
   - RF-13 a RF-19, RF-26, RNF-1 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_verify_refs.py` en verde; DOI 404 → «no existe» en una sola llamada; 503 persistente → «no verificable» con 4 llamadas y `sleep([1, 2, 4])`; sin `doi` ni `url` → «sin url»; código de salida correcto en cada caso; `.bib` no se modifica.

5. 🔄 SIGUIENTE — **Bibliotecario** — Referencias de datos y método: `fred2026`, `frb2026`, `newey1987`, `jorda2005` (4 filas en la matriz con Tipo = «datos/método», Estado = «verificado»; 4 entradas en `references.bib`).
   - RF-7, RF-9 a RF-12, RF-25 · agente: bibliotecario
   - Hecho cuando: `uv run pytest -q tests/test_literature_files.py` en verde; `fred2026.note` contiene los códigos de `src.config.ALL_SERIES`; `newey1987` y `jorda2005` llevan `doi`; `fred2026` y `frb2026` llevan `url`; las claves coinciden entre matriz y `.bib`.

6. **Bibliotecario** — Secciones 2.1 y 2.2: ≥ 2 estudios verificados en cada una, con columna Sección principal bien asignada (regla de «sección principal»), columnas llenas (sin vacías) y Respalda de la lista cerrada.
   - RF-2, RF-4, RF-6, RF-8 · agente: bibliotecario
   - Hecho cuando: `uv run pytest -q tests/test_literature_files.py` en verde y `summary_counts` = 2.1 ≥ 2 y 2.2 ≥ 2; ninguna celda vacía; todo hallazgo respaldado por resumen leído.

7. **Bibliotecario** — Secciones 2.3 y 2.4: ≥ 2 estudios verificados en cada una, con lo mismo que la T6.
   - RF-2, RF-4, RF-6, RF-8 · agente: bibliotecario
   - Hecho cuando: `uv run pytest -q tests/test_literature_files.py` en verde y `summary_counts` = 2.3 ≥ 2 y 2.4 ≥ 2.

8. **Bibliotecario** — Sección 2.5: ≥ 6 estudios empíricos verificados, con columnas obligatorias (País, Frecuencia, Período, Variable dependiente, Regresores, Variables de la guía, Método) y Hallazgo con signo (positivo/negativo/no significativo).
   - RF-6, RF-8, RF-22 · agente: bibliotecario
   - Hecho cuando: `uv run pytest -q tests/test_literature_files.py` en verde y `summary_counts`["2.5"] ≥ 6; `validate_matrix` pasa (ninguna fila 2.5 con «no aplica» en las columnas obligatorias).

9. **Bibliotecario** — Cierre del contenido: ≥ 16 estudios en total verificados (armonizar los descartados con el reemplazo de RF-2), `check_minimums(rows) == []` en `tests/test_literature_files.py`, `references.bib` sincronizado con la matriz y `uv run python scripts/verify_refs.py` contra Crossref real.
   - RF-2, RF-5, RF-18, RF-21 · agente: bibliotecario
   - Hecho cuando: `uv run pytest -q tests/test_literature_files.py` en verde con `check_minimums`; `uv run python scripts/verify_refs.py` termina con código 0; la salida completa va a `review-validate.md`.

10. **Claude** — Auditoría independiente `verificador-citas` de `references.bib` y la matriz (recibe solo las dos rutas, RNF-4): confirma que no hay DOI/URL inválidos y que ningún hallazgo en la matriz no está respaldado por lo leído. Informe guardado en `specs/002-literatura/`.
   - RNF-2, RNF-4, criterio de finalización · agente: claude
   - Hecho cuando: informe de auditoría guardado; veredicto en `specs/002-literatura/review-validate.md` con `VEREDICTO: APROBADO` y la salida de Crossref real.

---

## Notas
- Antes de la T5, el bibliotecario debe actualizar la sección «Matriz» de la skill `citas-apa` para que remita al formato de 16 columnas del §4 del plan (la skill tiene una versión antigua de 10 columnas); luego se ejecuta `quarto`/`/fabrica` con la versión nueva.
- Una fila «pendiente-lectura» no puede llevar signo en Hallazgo (RF-3, D5); solo las verificadas de 2.5 lo exigen.
- Los descartados de la lista semilla dejan su sección por debajo del mínimo: se añade otro candidato verificado de esa misma sección (RF-2).

## RF → tareas

| RF | Tareas |
|---|---|
| RF-1 | 5–9 (búsqueda/verificación en Crossref y OpenAlex, bibliotecario) |
| RF-2 | 5–9 |
| RF-3 | 5–9 |
| RF-4 | 1–3, 5–9 |
| RF-5 | 1–3, 5, 9 |
| RF-6 | 2, 6, 7, 8, 9 |
| RF-7 | 1–2, 5, 9 |
| RF-8 | 6–9 |
| RF-9 | 2–3, 5, 8, 9 |
| RF-10 | 1–3, 5, 9 |
| RF-11 | 1–2, 5, 9 |
| RF-12 | 2–3, 8, 9 |
| RF-13 | 1–2, 4 |
| RF-14 | 4 |
| RF-15 | 2, 4 |
| RF-16 | 4 |
| RF-17 | 4 |
| RF-18 | 4, 9 |
| RF-19 | 4 |
| RF-20 | 1–3, 5–9 |
| RF-21 | 5–9 |
| RF-22 | 2, 8, 9 |
| RF-23 | 2, 6–9 |
| RF-24 | 2, 6–9 |
| RF-25 | 1–2, 5 |
| RF-26 | 4 |
| RNF-1 | 4 |
| RNF-2 | 5–10 |
| RNF-4 | 10 |
| RNF-6 | 2 |
