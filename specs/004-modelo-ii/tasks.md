# Tasks — Spec 004 Modelo II

Orden de dependencia del §9 del plan. Una sola tarea cada vez: tests primero (en rojo), después el código, `uv run pytest -q` en verde, marcar la tarea y parar. OpenCode no tiene cuota: las tareas `implementer` las hace Claude Code (`AGENTS.md`); la independencia la da la auditoría de la tarea 9.

**Invariantes de todas las tareas**
- **No regresión del Modelo I:** sus salidas siguen idénticas byte a byte a las comiteadas (`tests/test_model1_nonregression.py`, que se crea en la tarea 1 y se repite en las 4 y 8).
- **Sin datos reales del Modelo II hasta la tarea 8:** los tests usan solo datos sintéticos (`tests/synthetic_model2.py`) y las simulaciones A a F de §7.1 del plan. Las tolerancias de §7.1 no se relajan.
- **Semillas independientes** para X y para el ruido de y (`SEED2 = 20261008` y `SEED2 + 1`).
- **Cada nota de pie que prometen la spec y el plan tiene su test.**

- [x] **T1. Configuración, diseño y cambios retrocompatibles.** RF-1 a RF-4, RF-5 (grados de libertad), RF-14 y RF-15 (diseño de las proyecciones), RF-22 a RF-24 (diseño de las variantes), RNF-2, RNF-7 · agente: implementer
  - Incluye: `src/model2_config.py`; `src/design2.py` (`build_columns`, `common_window`, `zero_rate_quarters`, `build_design2`, `lagged_from_excluded`, `covid_lag_leaks`, `build_lp_design`); `fit_ols_hac(design, maxlags=None)` y `_impulse_dummy_cols` con valores en {0, 1} (D1, D2); `tests/synthetic_model2.py` y el fixture de sesión; `tests/test_model1_nonregression.py`.
  - Hecho cuando: `uv run pytest -q tests/test_design2.py tests/test_estimation.py tests/test_model1_nonregression.py` en verde. `common_window` da 2000T2 con historia desde 1998 y no usa `dropna`; `build_design2` construye rezagos t−j reales aunque falte una fila, el orden de columnas y las dummies COVID solo en sus trimestres, y lanza error con variable, trimestre y regresión ante un NaN; R2 y R3 omiten las dummies y las anotan, y en cualquier otra variante es un error; `zero_rate_quarters` aplica la regla; `lagged_from_excluded` y `covid_lag_leaks` (solo y_lag y ΔFFR(t−1..t−K)) dan los trimestres esperados en casos hechos a mano; `build_lp_design` calcula DR(t+h) − DR(t−1) y FFR(t+h) − FFR(t−1), termina en `end − h` y nunca usa datos posteriores a `end`; `fit_ols_hac(maxlags=…)` usa esa ventana y con `None` da lo mismo que antes; `_impulse_dummy_cols` ignora una columna continua de suma 1; proceso D (HAC mayor que el clásico); las salidas del Modelo I son idénticas a las comiteadas.

- [x] **T2. Dinámica: efectos, trayectoria, Granger y lectura.** RF-6, RF-7, RF-10 a RF-13, RNF-2, RNF-3 · agente: implementer
  - Incluye: `src/dynamics.py` (`cumulative_effects`, `multipliers`, `peak_horizon`, `granger_lags`, `hypotheses`, `evidence_reading`, `select_k`) y `PEAK_TIE_TOL` en la configuración.
  - Hecho cuando: `uv run pytest -q tests/test_dynamics.py` en verde. Con θ y ρ conocidos, S, S_rez, ψ_h y R(h) coinciden con una forma cerrada; `peak_horizon` resuelve el empate al menor h; `granger_lags` rechaza con θ_j ≠ 0 y no con θ_j = 0 (proceso E); `hypotheses` y `evidence_reading` en sus tres resultados y con la marca de signo contrario; `select_k` recupera K = 3 por BIC (proceso B) y resuelve el empate al menor K; proceso A: θ_j, ρ y γ dentro de 0,05 y S y S_rez dentro de 0,10.

- [ ] **T3. Proyecciones locales.** RF-14 a RF-17, RNF-4 · agente: implementer
  - Incluye: `src/localproj.py` (`local_projection`, `run_local_projections`, `detection_horizon`, `compare_with_trajectory`).
  - Hecho cuando: `uv run pytest -q tests/test_localproj.py` en verde. Proceso C: |β_h − R(h)| ≤ 0,12 para h = 0..12 y |φ_h − 1| ≤ 0,20 para h = 1..12; φ₀ = 1 exacto con EE y banda «—» y sin `inf` ni `NaN`; la ventana HAC es max(fórmula, h + 1); un horizonte sin grados de libertad sale «no estimada» sin afectar a los demás; β₀ es θ₀ de la principal con el mismo EE; `detection_horizon` («ninguno» incluido) y el recuento «k de n» sin h = 0.

- [ ] **T4. Diagnósticos del Modelo II.** RF-19, RF-20, RNF-6 · agente: implementer
  - Incluye: `vif(fit, terms=None)`, `chow_wald` con `n_pre`, `n_pre_util` y `calculable` (rango comprobado antes de estimar) y `white` sin caída y con «no calculable» (D14, D17), en `src/diagnostics.py`.
  - Hecho cuando: `uv run pytest -q tests/test_diagnostics.py tests/test_model1_nonregression.py` en verde. Con la dimensión del Modelo II (proceso F, n = 105): White da «no calculable» con K = 8 y un resultado válido con K = 1; el Chow con K = 8 usa K + 7 = 15 interacciones; el CUSUM va sobre la regresión sin las 4 dummies de impulso; con rango incompleto no se llama a `fit_ols_hac` ni a `wald` y la fila es «no calculable»; Breusch-Godfrey y el Chow rechazan y no rechazan según el proceso F; las salidas del Modelo I son idénticas a las comiteadas.

- [ ] **T5. Modelo II: selección, principal y tablas.** RF-3 a RF-13, RF-17 a RF-21, RNF-5 · agente: implementer
  - Incluye: `src/model2.py` con `run_model2`, `diagnostics_table2`, `stationarity_table2` y las tablas de selección, coeficientes, efectos, trayectoria, lectura, proyecciones, comparación, diagnósticos y estacionariedad.
  - Hecho cuando: `uv run pytest -q tests/test_model2.py -k "not robust and not limitations and not deviations and not export and not render"` en verde. `run_model2` se detiene antes de estimar si la forma de DRALACBS no es la esperada; la selección usa la muestra común y se detiene con el K si algún modelo no tiene grados de libertad; K_BIC es el principal; los pies de las tablas (RF-8, RF-11, RF-17 y la nota del Chow sin «β₁–β₅», con K + 7 y los trimestres útiles anteriores y posteriores) tienen su test; `stationarity_table2` toma ΔDR, ΔFFR y ΔU de «primera diferencia» y PIB, π y CRED de «tal cual», y su pie lo dice.

- [ ] **T6. Modelo II: robusteces, limitaciones, desviaciones, insumos, exportación y texto.** RF-22 a RF-27, RF-29, RF-30, RNF-5, RNF-8 · agente: implementer
  - Incluye: R1 a R3, `limitations_table2`, `deviations_table2`, `comparison_inputs`, `export2`, `export2_json` y `render_model2_tables`.
  - Hecho cuando: `uv run pytest -q tests/test_model2.py` en verde. R1 «no aplica» si AIC y BIC coinciden y sale del denominador; R2 y R3 con el K del principal y sus muestras; el resumen de robustez (criterio sobre S_rez, estados fuera del denominador, p de la principal) y su pie; las limitaciones fijas y las detectadas (K = 8, diagnósticos «falla» o «alerta» y «no calculables», rezagos de ΔFFR o ΔDR desde 2020T2–2021T1); las desviaciones; los insumos de la 6.3 con el coeficiente de ΔFFR(t) del Modelo I; la exportación JSON (claves, orden, ida y vuelta exacta, sin `NaN`); el Markdown y el CSV de las 14 tablas, deterministas.

- [ ] **T7. Figuras, variables del informe y tests de lenguaje y pureza.** RF-9, RF-18, RF-28, RNF-9, RNF-10, RNF-11 · agente: implementer
  - Incluye: `plot_model2_profile` y `plot_model2_response` en `src/figures.py`; `model2_variables` en `src/report_vars.py`; `tests/test_outputs_model2.py`; ampliación de `tests/test_language.py` y `tests/test_pipeline.py`.
  - Hecho cuando: `uv run pytest -q tests/test_outputs_model2.py tests/test_language.py tests/test_pipeline.py` en verde. Figuras de 8×4,5 pulgadas, 200 dpi, sin título y con el pie de fuente, con las series esperadas y bytes deterministas; `model2_variables` trae todas las claves del §4 del plan, solo texto, con los mismos dígitos que las tablas y sin cifras escritas a mano (escaneo con `ast`); sin «causa», «causal», «provoca» ni «debido a» en tablas, variables ni figuras; los módulos nuevos son puros y no usan `fillna` ni `dropna`.

- [ ] **T8. Etapa `models` y tests sobre los datos congelados.** RF-30, RNF-8 · agente: implementer
  - Incluye: la extensión de `pipeline.stage_models` y `tests/test_frozen_model2.py`. **Primera tarea que estima el Modelo II con datos reales** (el plan está aprobado y comiteado, `7f732ce`).
  - Hecho cuando: `uv run pytest -q tests/test_frozen_model2.py tests/test_model1_nonregression.py` en verde. Existen las 14 tablas (`.md` y `.csv`), las 3 figuras, el JSON y `modelo2:`; `modelo1:` y `datos:` quedan idénticos; M = 2000T2–2026T2 con 105 observaciones; 36 trimestres de tasa cero; `hac_lags == 4` y K + 11 parámetros en la principal; dos corridas dejan bytes idénticos; las salidas del Modelo I son idénticas a las comiteadas. Este test no compara coeficientes con valores esperados.

- [ ] **T9. Validación y auditoría.** Criterios de finalización · agente: claude
  - Hecho cuando: `specs/004-modelo-ii/review-validate.md` y `specs/004-modelo-ii/review-audit.md` con `VEREDICTO: APROBADO`; `uv run pytest -q` en verde; dos corridas de `uv run python -m src.pipeline all` sin diferencias y `git status --porcelain` limpio.

## Tabla RF → tareas

| RF / RNF | Tareas |
|---|---|
| RF-1, RF-2, RF-4 | T1, T5 |
| RF-3 | T1, T5 |
| RF-5 | T1, T5 |
| RF-6, RF-7 | T2, T5 |
| RF-8 | T5 |
| RF-9 | T7 |
| RF-10 a RF-13 | T2, T5 |
| RF-14 a RF-17 | T1, T3, T5 |
| RF-18 | T7 |
| RF-19, RF-20 | T4, T5 |
| RF-21 | T5 |
| RF-22 a RF-24 | T1, T6 |
| RF-25 a RF-27 | T6 |
| RF-28 | T7 |
| RF-29 | T6 |
| RF-30 | T6, T8 |
| RNF-1 | commits `ec983d0`, `45c43d5` y `7f732ce`, anteriores a la tarea 8 |
| RNF-2 a RNF-4, RNF-6, RNF-7 | T1 a T4 |
| RNF-5 | T5, T6 |
| RNF-8 | T6, T8 |
| RNF-9 a RNF-11 | T7 |
