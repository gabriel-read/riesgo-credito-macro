# Tasks — Spec 003 Modelo I

1. ✅ COMPLETADA — **Implementer** — `src/model1_config.py` (constantes: SEED, ALPHA, ROBUST_ALPHA, LONGRUN_MIN_GAP, VIF_ALERT, MIN_DOF, PSD_REL_TOL, MAIN_START, LONG_START, COVID_QUARTERS, R1_EXCLUDED, CHOW_BREAKS, BG_LAGS, OOS_*, MACRO_TERMS, CREDIT_LAG, EXPECTED_SIGN, EXPECTED_FORMS, TERM_LABELS, VariantSpec, MAIN, VARIANTS) y `src/design.py` (ModelDataError, read_decisions, check_expected_forms, diff_form_stationary, dependent_series, build_design, effective_window, Design dataclass) con `tests/test_design.py`.
   - RF-1 a RF-5, RF-15 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_design.py` en verde; `check_expected_forms` salta ModelDataError si la tabla de estacionariedad cambia una forma esperada; `build_design` construye X con orden fijo (const, y_lag, 5 macro, dummies), y_lag = t−1 real, CRED(t−4) = t−4 real; dummies COVID = 1 solo en sus trimestres; estacionales base T1; NaN interior lanza error con variable/trimestre/regresión; ventana truncada da R6=2001T1, R7=2002T1, R8=2000T1; R1 omite dummies COVID; `diff_form_stationary` juzga ΔU, ΔFFR con su fila "primera diferencia".

2. ✅ COMPLETADA — **Implementer** — `src/estimation.py` (hac_lags, psd_truncate, fit_ols_hac, inference, wald, long_run, scale_effect, standardization_sd, check_dof) con `tests/test_estimation.py`.
   - RF-6, RF-7, RF-10, RNF-2, RNF-3 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_estimation.py` en verde; DGP recupera coeficientes (error ≤ 0,05); con AR(1) EE HAC > EE clásico; `hac_lags(106)==4`, `hac_lags(1)>=1`; `psd_truncate` eleva autovalores negativos al piso; `inference` reproduce p e IC normales; `wald` coincide con t²; `long_run` con ρ=0,96 da "no reportado"; `scale_effect(0)` da "no definido"; `check_dof` marca <30 GL y rango incompleto; Newey-West puro (`use_correction=False`).

3. ✅ COMPLETADA — **Implementer** — `src/diagnostics.py` (breusch_godfrey, breusch_pagan, white, jarque_bera_test, reset, vif, chow_wald, cusum, diagnostics_table) con `tests/test_diagnostics.py` y `tests/test_impulse_dummies.py`.
   - RF-12 a RF-14, RNF-4 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_diagnostics.py tests/test_impulse_dummies.py` en verde; BG rechaza con e AR(1) 0,7 y no con e iid; Chow Wald rechaza con quiebre simulado en pendientes; White usa QR con pivoteo (grados de libertad = rango−1, no duplicados exactos); VIF >10 alerta; CUSUM sobre regresión reducida (sin dummies impulso y sin sus trimestres) falla con quiebre fuerte y pasa con proceso estable; coeficientes no dummy coinciden con regresión reducida (tol 1e-10); bloque no dummy de V definido positivo, rango reducido reportado como "esperado"; dummy sin variación fuera de R1 y tramo OOS lanza ModelDataError.

4. ✅ COMPLETADA — **Implementer** — `src/forecast.py` (one_step, dynamic, to_level, naive, rmse, mae, diebold_mariano_hln, oos_verdicts) con `tests/test_forecast.py`.
   - RF-18, RNF-3 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_forecast.py` en verde; `to_level` a un paso = DR(t−1) + ΔŶ, dinámico = ancla + cumsum(ΔŶ); `dynamic` encadena ŷ en y_lag; `naive` en sus dos modos; `diebold_mariano_hln` con n=5 calculado a mano (t(4)); `oos_verdicts` en 4 casos; DM divisor n, e = observado−pronóstico, corrección HLN, t(n−1).

5. ✅ COMPLETADA — **Implementer** — `src/model1.py` (run_model1, coefficient_table, effects_table, model_stationarity_table) con `tests/test_model1.py` (parcial: principal, efectos, estacionariedad del modelo).
   - RF-3, RF-4, RF-7, RF-9, RF-10, RF-15 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_model1.py -k "not robustez and not limitaciones and not desviaciones and not export and not oos"` en verde; `read_decisions` + `check_expected_forms` antes de estimar; `coefficient_table` con coef, EE HAC, z, p, IC 95%, signo esperado y coincidencia; pie con forma Y, muestra, n_obs, n_param, R², R²_adj, SER, HAC lags, truncamiento, nota dummies impulso; `effects_table` con impacto y largo plazo × {1 pp, 1 DE}, EE, p, IC 95%, en pp, "no reportado (1 − ρ ≤ 0,05)" si aplica; `model_stationarity_table` copia ADF/KPSS de la 001, decisión, orden, "no I(0)".

6. ✅ COMPLETADA — **Implementer** — `src/model1.py` (run_variant, robustness_estimates, robustness_summary, limitations_table, deviations_table, stress_export, is_robust) completando `tests/test_model1.py`.
   - RF-5, RF-6, RF-8, RF-16, RF-17, RF-20, RF-21 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_model1.py` en verde (completo); `run_variant` R8 sin historia anterior a 2000T1 → "no estimada"; <30 GL o rango incompleto → "no estimada"; `robustness_estimates` 1 fila por variante×regresor macro con coef, EE HAC, p o "no estimada"; `robustness_summary` 5×10 celdas sí/no/no estimada + "k de n" excluyendo no estimadas; `limitations_table` incluye fijas + detectadas (diag fallidos, no I(0), posible I(2), R8, truncamiento); `deviations_table` con estado de R8; `stress_export` → JSON con params, cov_hac, terms, columns, credit_lag, sample, hac_lags, covid_quarters; `is_robust` signo×p<0,10.

7. ✅ COMPLETADA — **Implementer** — `src/model1.py` (out_of_sample) con `tests/test_model1.py` (OOS).
   - RF-18, RF-19 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_model1.py -k "oos"` en verde; entrenamiento 2000T1–2019T4 sin dummies COVID; evaluación 2022T1–2026T2; pronóstico a un paso y dinámico con reconstrucción de nivel; ingenuo en ambos modos; RMSE, MAE, cocientes, DM-HLN (h=1, divisor n, corrección HLN, t(n−1)); veredictos pre-registrados; series para figura.

8. ✅ COMPLETADA — **Implementer** — `src/figures.py` (plot_model1_coefficients, plot_model1_cusum, plot_model1_oos), `src/report_vars.py` (model1_variables), `tests/test_outputs_model1.py`, `tests/test_language.py`, ampliación de `tests/test_pipeline.py` (pureza módulos nuevos).
   - RF-11, RF-14, RF-19, RF-22, RF-23, RNF-6, RNF-7, RNF-8 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_outputs_model1.py tests/test_language.py tests/test_pipeline.py` en verde; figuras 8×4,5", 200 dpi, sin título, pie "Fuente: FRED; elaboración propia", metadata determinista; coeficientes: impacto por 1 DE ± IC 95%, línea en 0; CUSUM: bandas 5%; OOS: 4 series (obs, 1 paso, dinámico, ingenuo); `model1_variables` trae todas las claves §4 del plan, efectos no reportados como texto; pipeline modules puros (sin red/disco/gráficos, sin fillna); `test_language` detecta "causa"/"causal"/"provoca"/"debido a".

9. 🔄 SIGUIENTE — **Implementer** — `src/pipeline.py` (stage_models) y `tests/test_frozen_model1.py`. **Primera tarea que estima con datos reales** (requiere pre-registro commiteado, RNF-1).
   - RF-1, RF-4, RF-5, RF-7, RF-8, RF-23, RNF-5 · agente: implementer
   - Hecho cuando: `uv run pytest -q tests/test_frozen_model1.py` en verde; `check_expected_forms` pasa; principal 2000T1–fin, 106 obs; R6=2001T1, R7=2002T1, R8 "no estimada"; `hac_lags==4`, `n_parametros==11`; dos corridas en tmp_path dejan bytes idénticos en tablas, figuras, JSON, _variables.yml; claves no modelo1 de _variables.yml byte a byte iguales.

10. **Claude** — Auditoría (`/sdd-audit 003-modelo-i` en Claude Code). Recibe solo rutas de salidas; escribe `specs/003-modelo-i/review-audit.md` y `review-validate.md` con `VEREDICTO: APROBADO`.
    - RNF-1, criterios de finalización · agente: claude
    - Hecho cuando: `specs/003-modelo-i/review-validate.md` y `review-audit.md` con `VEREDICTO: APROBADO`; `uv run pytest -q` en verde; dos corridas `pipeline all` sin diferencias.

---

## Orden de ejecución (secuencial, una tarea por vez)

Cada tarea termina con `uv run pytest -q` en verde. Si falla → PARA y avisa.

## Notas
- Agentes: `implementer` para T1–T9; `claude` para T10.
- Pre-registro (RNF-1): commit `667b313` (solo `specs/003-modelo-i/`) ya existe, anterior a T9.
- T9 es la primera que estima con datos reales; requiere que el repo esté en estado commiteado tras T8.
