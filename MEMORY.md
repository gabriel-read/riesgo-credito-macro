# MEMORY.md — Riesgo de crédito y macroeconomía
Memoria del proyecto entre sesiones y entre arneses (Claude Code y OpenCode). Máximo ~50 líneas: resume o elimina lo que ya no aporte.

## Estado actual (5-oct-2026)
- Spec 002-literatura COMPLETADA (5-oct-2026): 10/10 tareas, 187 tests en verde, `verify_refs.py` 21/21 con código 0 y auditoría independiente T10 APROBADA en la ronda 4 (`review-audit.md`, `review-validate.md`; el `APROBADO` previo de la fábrica no valía). Matriz: 17 estudios + 4 datos/método (2.1–2.4 = 2 cada una, 2.5 = 9); asiamah2026 y koskei2023 quedan pendiente-lectura (signo no respaldado por el resumen). Para la spec 006: justificar bernanke1995 en 2.1 y la clasificación de pesaran2006, segoviano2006 y gertler2015.
- Spec 003-modelo-i IMPLEMENTADA (5-oct-2026): T1–T10, 504 tests, `all` ×2 idéntico byte a byte, auditoría ronda 4 APROBADA (`review-audit.md`; rondas 1–3, cada una con solo menores, en `review-audit-ronda1/2/3.md`). `review-validate.md` lo escribió Claude Code por cuota agotada de OpenCode. Pre-registro `667b313`; C1–C3 antes de estimar.
- Hallazgos 003 (datos reales): ρ = 0,63; con p < 0,05 solo π (+) y CRED(t−4) (+); PIB (−) y ΔU (+) con el signo esperado pero sin significancia; ΔFFR con signo contrario (−), sin significancia. BG pasa y CUSUM pasa; BP, White, JB, RESET y los dos Chow fallan. VIF de ΔU = 36,8 es artefacto de la dummy de 2020T2. Fuera de muestra: a un paso no se distingue del ingenuo (DM p = 0,94); el dinámico pierde frente al ingenuo constante.
- Preguntas del profesor (ensayo): (1) ¿por qué creer los p-valores de inflación y crédito si figuran no I(0) y la dependiente es I(0)? (2) ΔFFR sale negativa y el dinámico se hunde en 2022–2023: ¿cómo lo usa en un estrés con alzas de tasa y varios pp de desempleo? (3) Chow y RESET rechazan pero el CUSUM pasa: ¿qué afirmación para gestión de riesgos sobrevive a endogeneidad, inestabilidad y no linealidad? (Si solo hay asociación, ¿cómo responde a «¿cómo afectan?»)
- Migración (4-oct-2026): de Warp a Orca como harness; OpenRouter se intentó y se descartó (clave daba 401 y crear otra pedía billing). OpenCode sigue con OpenCode Zen: planner/coordinator nemotron-3-ultra-free; implementer longcat-2.5-preview-free; reviewer big-pickle; bibliotecario space-bunny-free (elección sin probar). Mientras OpenCode no funcione, Claude Code avanza la spec 002. Copia oficial: `~/orca/riesgo-credito-macro`, rama `spec/002-literatura`, commit `a39311e` sin push (la copia de Desktop/OneDrive queda como respaldo). Pendiente: `/connect` a Zen y probarlo (daba "User not found").
- Constitución revisada el 2-oct (sin cambios, seis principios). Fase 0 (`ca8e4cc`), specs 001-datos y 002-literatura cerradas; detalle en `specs/001-*` y `specs/002-*`. D1 del plan 001: solo `data --download` usa la red.

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
- Dummies de impulso (valen 1 en un solo trimestre): residuo nulo, rompen el CUSUM de statsmodels, dejan `cov_hac` de rango reducido y meten columnas colineales en White. En statsmodels 0.15 `use_correction` de HAC es False por defecto.
- En tests, `y` y `X` con semillas distintas: con la misma, el ruido coincide con una columna de X (R² = 1, V ≈ 0) y los tests de rango y de diagnósticos no miden nada.
- Antes de dar una enmienda del plan por «incorporada», comprobar con grep que el código la implementa: la §12 dio por hechas dos notas que no existían (Chow 2020T2 y rezagos de R1) y costó dos rondas de auditoría.
- Probar cada variante de robustez con datos sintéticos: `gdp_column` ignorado y `exclude` de R1 mal leído pasaron los tests de T1 y los destapó T6.

## Próximos pasos
1. Spec 004 (Modelo II) en BORRADOR (8-oct-2026, `specs/004-modelo-ii/spec.md`, 27 RF y 10 RNF, crítica). Entrevista: efecto acumulado S = Σθ (Wald HAC) + trayectoria R(h) del nivel con ρ y h* = argmax|R(h)| (sin bandas); controles PIB, ΔU, π a t−1 y CRED(t−4); R3 sin tramos de tasa cero (regla: FFR trimestral ≤ 0,25 %, 36 trimestres, 2009T1–2015T4 y 2020T2–2022T1); LP con los mismos controles y los K rezagos de ΔFFR; Granger solo tasa → morosidad sin θ₀. Muestra común 2000T2–2026T2 (105). Siguiente: `/sdd-clarify 004-modelo-ii`, `/sdd-resolve`, `/sdd-plan`; aprobar y commitear antes de estimar.
2. ANTES de la 005 (estrés): decidir y pre-registrar el tratamiento del signo negativo de ΔFFR (un escenario con alzas de tasa baja la morosidad proyectada); simular solo el bloque de `cov_hac` sin dummies (rango 7 de 11); dummies COVID en 0 en el horizonte; ΔU se identifica con ~0,3 pp por trimestre.
3. Spec 006, heredado de `review-audit.md`: regresión desbalanceada con KPSS ambiguo para π y CRED; PIB significativo solo en el largo plazo; «supera al ingenuo» siempre con «no significativo»; CUSUM pasa y Chow falla; la nota de R1 es parcial. Opcionales sin aplicar: etiqueta «ΔPIB», ingenuo constante en la figura, hueco COVID en el CUSUM, gl de White/RESET, KPSS «> 0,10» unificado, coeficientes 2000–2019 sin exportar.
4. PR: la rama `spec/003-modelo-i` trae también los commits de la 002 (no fusionada): decidir un PR único o separar. `git push` lo hace el usuario.
5. Si `uv run` falla con "os error 998" en el `.venv`: `uv sync` lo recrea (pasó el 2-oct).
