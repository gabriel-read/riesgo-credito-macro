# MEMORY.md — Riesgo de crédito y macroeconomía
Memoria del proyecto entre sesiones y entre arneses (Claude Code y OpenCode). Máximo ~50 líneas: resume o elimina lo que ya no aporte.

## Estado actual (2-oct-2026)
- Fase 0: arnés instalado (AGENTS.md, constitución, skills, agentes, comandos, CI) y versionado en el commit `ca8e4cc`. Sin código ni datos todavía.
- Constitución revisada el 2-oct-2026 con /sdd-constitution; se decidió dejarla como está (sin cambios, seis principios). Posible mejora futura: aclarar que la reproducibilidad parte de `data/raw/` congelado y quitar la excepción "salvo causalidad" del principio 5.
- Spec 001-datos aprobada el 2-oct-2026 (clarificada y resuelta).
- Plan 001-datos aprobado el 2-oct-2026 (`specs/001-datos/plan.md`). Decisión clave D1: `data --download` descarga; `data` y `all` construyen solo desde `data/raw/` congelado. Siguiente: `/fabrica 001-datos` en OpenCode (tareas, implementación, validación).

## Calendario (entregar el jueves 15-oct antes de las 22:00; cierre oficial 16-oct 00:00)
- 001 datos 3–4 oct · 002 literatura 4–6 oct · 003 modelo I 5–8 oct · 004 modelo II 8–10 oct
- 005 estrés 10–11 oct · 006 informe 11–14 oct · 007 diapositivas 13–14 oct · evaluación y ensayo 14–15 oct

## Decisiones (y por qué)
- Frecuencia trimestral: la dependiente (DRALACBS) es trimestral; las mensuales se promedian por trimestre.
- Muestra 2000T1 al último trimestre publicado (2026T2); se descarga desde 1998 para calcular variaciones interanuales sin perder 2000. Desviación frente a la guía (que corta en 2026-01-01): declararla en el informe.
- Reparto de arneses: Claude Code redacta constitución, specs y planes, y audita; OpenCode (LongCat 2.5 Preview, high) hace tareas, implementación y validación técnica.
- Specs críticas (auditoría de Claude obligatoria): 003, 004, 005 y 006.
- Estrés sobre las fechas de la Fed 2026 (base y severamente adverso) más un escenario propio estanflacionario con alza de tasas.

## Decisiones pendientes
- PIB real (GDPC1) como principal y nominal (GDP, el de la guía) como robustez, o al revés.
- ¿El profesor acepta extender la muestra a 1985 como robustez?
- Formato exigido del informe (Word o PDF) y de la exposición.

## Aprendizajes y errores a evitar
- Octubre 2025 no existe en CPI ni en desempleo (cierre del gobierno de EE. UU.): 2025T4 se promedia con dos meses y se documenta.
- pandas-datareader < 0.11 falla con pandas 3; respaldo: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIE>`.
- FRED revisa el PIB: volver a descargar puede cambiar resultados. Congelar `data/raw/` con fecha y no volver a bajarlo.
- `test_report_has_no_hand_typed_decimals` (tests/test_harness.py:93) solo detecta números con 2+ decimales: "0,8 pp" o "15 %" a mano pasan. Endurecerlo en la spec 001.
- El pre-registro se demuestra con git: aprobar y commitear cada spec de modelo antes de la primera estimación.

## Próximos pasos
1. `/fabrica 001-datos` en OpenCode. El plan ya cubre RNF-2 (`conftest.py` sin red) y RNF-4 (endurecer `tests/test_harness.py:93`).
2. Al descargar, verificar en FRED las unidades de cada serie (sobre todo el año base de GDPC1).
3. Si `uv run` falla con "os error 998" en el `.venv`: `uv sync` lo recrea (pasó el 2-oct).
