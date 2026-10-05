# MEMORY.md — Riesgo de crédito y macroeconomía
Memoria del proyecto entre sesiones y entre arneses (Claude Code y OpenCode). Máximo ~50 líneas: resume o elimina lo que ya no aporte.

## Estado actual (5-oct-2026)
- Spec 002-literatura COMPLETADA (5-oct-2026): 10/10 tareas, 187 tests en verde, `verify_refs.py` 21/21 con código 0 y auditoría independiente T10 APROBADA en la ronda 4 (`review-audit.md`, `review-validate.md`; el `APROBADO` previo de la fábrica no valía). Matriz: 17 estudios + 4 datos/método (2.1–2.4 = 2 cada una, 2.5 = 9); asiamah2026 y koskei2023 quedan pendiente-lectura (signo no respaldado por el resumen). Para la spec 006: justificar bernanke1995 en 2.1 y la clasificación de pesaran2006, segoviano2006 y gertler2015.
- Migración (4-oct-2026): de Warp a Orca como harness; OpenRouter se intentó y se descartó (clave daba 401 y crear otra pedía billing). OpenCode sigue con OpenCode Zen: planner/coordinator nemotron-3-ultra-free; implementer longcat-2.5-preview-free; reviewer big-pickle; bibliotecario space-bunny-free (elección sin probar). Mientras OpenCode no funcione, Claude Code avanza la spec 002. Copia oficial: `~/orca/riesgo-credito-macro`, rama `spec/002-literatura`, commit `a39311e` sin push (la copia de Desktop/OneDrive queda como respaldo). Pendiente: `/connect` a Zen y probarlo (daba "User not found").
- Fase 0: arnés instalado (AGENTS.md, constitución, skills, agentes, comandos, CI) y versionado en el commit `ca8e4cc`. Sin código ni datos todavía.
- Constitución revisada el 2-oct-2026 con /sdd-constitution; se decidió dejarla como está (sin cambios, seis principios). Posible mejora futura: aclarar que la reproducibilidad parte de `data/raw/` congelado y quitar la excepción "salvo causalidad" del principio 5.
- Spec 001-datos aprobada el 2-oct-2026 (clarificada y resuelta).
- Plan 001-datos aprobado el 2-oct-2026 (`specs/001-datos/plan.md`). Decisión clave D1: `data --download` descarga; `data` y `all` construyen solo desde `data/raw/` congelado.
- Spec 001-datos T1 implementada (2-oct-2026): `tests/conftest.py` con bloqueo de red autouse (RNF-2), `tests/test_network.py`, `find_hand_typed_numbers` en `tests/test_harness.py` (RNF-4) y `pythonpath = ["."]` en `pyproject.toml`. `uv run pytest -q`: 12 passed.
- Spec 001-datos T2 implementada (2-oct-2026): `src/config.py` con constantes, `SERIES_META` y `COLUMN_LABELS` (25 etiquetas en español). `tests/test_config.py` con 16 tests. `uv run pytest -q`: 28 passed. Siguiente: T3 (`src/fred_io.py`).
- Spec 002-literatura APROBADA el 3-oct-2026 (`specs/002-literatura/spec.md`; dudas resueltas: BCBS 2018 "Stress testing principles", Fed "2026 Stress Test Scenarios", FRED como una sola referencia): 20 RF, mínimo 16 estudios verificados (2 por sección 2.1–2.4, 6 empíricos en 2.5) + 4 refs de datos/método que no cuentan; script `scripts/verify_refs.py` contra Crossref. Clarificada y resuelta el 3-oct-2026 (26 RF, mínimo 20 filas verificadas: 16 estudios + 4 datos/método). 
- Plan 002-literatura aprobado el 3-oct-2026 (`specs/002-literatura/plan.md`, D1–D15): `src/references.py` puro + `scripts/verify_refs.py` (único con red, `fetch`/`sleep` inyectados); matriz y .bib son curados, fuera de `src.pipeline`. Skill citas-apa alineada con el formato de 16 columnas. Siguiente: `/fabrica 002-literatura` en OpenCode.


## Calendario (entregar el jueves 15-oct antes de las 22:00; cierre oficial 16-oct 00:00)
- 001 datos 3–4 oct · 002 literatura 4–6 oct · 003 modelo I 5–8 oct · 004 modelo II 8–10 oct
- 005 estrés 10–11 oct · 006 informe 11–14 oct · 007 diapositivas 13–14 oct · evaluación y ensayo 14–15 oct

## Decisiones (y por qué)
- Frecuencia trimestral: la dependiente (DRALACBS) es trimestral; las mensuales se promedian por trimestre.
- Muestra principal 2000T1–2026T2 (106 trimestres); se descarga desde 1998 para calcular variaciones interanuales sin perder 2000. Robustez de muestra larga 1985T1–2026T2, pre-registrada en las specs 003–005. Desviación frente a la guía (que corta en 2026-01-01): declararla en el informe. (Resuelto el 5-oct-2026.)
- PIB: GDPC1 (real) es el regresor principal, para evitar doble contabilidad con la inflación; GDP (nominal, el de la guía) se pre-registra como robustez. (Resuelto el 5-oct-2026.)
- Informe: PDF generado con Quarto en APA 7 (`apa.csl`, números desde `report/_variables.yml`). (Resuelto el 5-oct-2026.)
- Reparto de arneses: Claude Code redacta constitución, specs y planes, y audita; OpenCode (LongCat 2.5 Preview, high) hace tareas, implementación y validación técnica.
- Specs críticas (auditoría de Claude obligatoria): 003, 004, 005 y 006.
- Estrés sobre las fechas de la Fed 2026 (base y severamente adverso) más un escenario propio estanflacionario con alza de tasas.

## Decisiones pendientes
- Formato exigido de la exposición (diapositivas).
- Confirmar con el profesor que la muestra larga 1985T1 como robustez y el PDF son aceptables.

## Aprendizajes y errores a evitar
- No fiarse del `APROBADO` de la fábrica sin auditoría independiente: en la 002 marcó T4 y T10 como hechas con tests en rojo o sin auditar. Validar (OpenCode) y auditar (`verificador-citas` con solo rutas) son cosas distintas.
- Un estudio que estima coeficientes macro sobre morosidad es sección 2.5 aunque encaje conceptualmente en 2.2; no reasignar para cuadrar mínimos.
- FRED cuelga las peticiones con User-Agent propio: usar el predeterminado.
- OpenCode usa `permission` (singular, objeto; gana la última regla coincidente), no `permissions` como lista: con la lista las protecciones se ignoraban. Ya corregido en `opencode.jsonc` y los 5 agentes; verificar con una prueba real (`git push` y leer `.env` deben rechazarse).
- Los modelos gratuitos tienen cuota limitada: al agotarse, seguir con Claude Code.
- Octubre 2025 no existe en CPI ni en desempleo (cierre del gobierno de EE. UU.): 2025T4 se promedia con dos meses y se documenta.
- pandas-datareader < 0.11 falla con pandas 3; respaldo: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIE>`.
- FRED revisa el PIB: volver a descargar puede cambiar resultados. Congelar `data/raw/` con fecha y no volver a bajarlo.
- `test_report_has_no_hand_typed_decimals` (tests/test_harness.py:93) solo detecta números con 2+ decimales: "0,8 pp" o "15 %" a mano pasan. Endurecerlo en la spec 001.
- El pre-registro se demuestra con git: aprobar y commitear cada spec de modelo antes de la primera estimación.

## Próximos pasos
1. Spec 003 (Modelo I) RESUELTA y marcada aprobada (5-oct-2026, 23 RF; 69 hallazgos de `review-clarify.md` aplicados). Decisiones:
   - Sin `/sdd-change 001`. R6 y R7 se truncan a la historia disponible (con la descarga de 1998 empiezan en 2001T1 y 2002T1); R8 queda «no estimada» si no hay historia anterior a 2000.
   - La regla ADF/KPSS solo decide la forma de la dependiente (hoy todas en Δ); los regresores tienen forma fija y su no estacionariedad se declara como limitación.
   - El largo plazo solo se reporta si 1 − ρ > 0,05.
   - Si la matriz HAC no es definida positiva, truncamiento espectral.
   - Chow como Wald HAC con interacciones.
   - RF-4 se detiene si cambia la tabla de estacionariedad.
   - Robusto = mismo signo y p < 0,10.
   - Variables bajo el prefijo `modelo1.`.

   Pendiente: commit `spec(003-modelo-i): aprobada` (solo `specs/003-modelo-i/`) y luego `/sdd-plan 003-modelo-i`.
2. Si `uv run` falla con "os error 998" en el `.venv`: `uv sync` lo recrea (pasó el 2-oct).
