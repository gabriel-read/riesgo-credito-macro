VEREDICTO: APROBADO

# Validación de la spec 004 — Modelo II (`specs/004-modelo-ii/`)

- **Qué se validó:** HEAD `c6d14c1` (T1–T8 implementadas; `spec.md` aprobada con el cambio C1; `plan.md` aprobado).
- **Quién valida:** Claude Code. Es una excepción de roles autorizada por el autor por indisponibilidad de cuota en OpenCode: quien valida es también quien implementó, así que **esta validación no es independiente**. La independencia la aporta `review-audit.md` (`revisor-econometrico`, que recibe solo rutas de archivos).
- **Qué no hace este informe:** no interpreta los resultados económicos ni los usa para decidir nada; comprueba que la implementación cumple la spec y el plan.

## 1. Ejecución

**Suite.** `uv run pytest -q` → **756 passed**, 0 fallos, 4 min (la máquina está lenta: ni `import pandas, statsmodels` baja de 14 s). Sin red: el fixture autouse `block_network` de `tests/conftest.py` hace fallar cualquier acceso. Tests de la 004 por archivo: `test_design2` 24 · `test_dynamics` 21 · `test_localproj` 13 · `test_diagnostics2` 15 · `test_model2` 28 · `test_model2_outputs` 27 · `test_outputs_model2` 18 · `test_model2_purity` 35 · `test_model2_language` 26 · `test_frozen_model2` 19 · `test_model1_nonregression` 23 (suma 249, más los 3 de `test_estimation` añadidos en T1).

**No regresión del Modelo I.** `tests/test_model1_nonregression.py` (23 tests) rehace la etapa `models` sobre `data/raw/` congelado y compara byte a byte las 9 tablas (`.csv` y `.md`), las 3 figuras y el JSON del Modelo I con lo comiteado, y el bloque `modelo1:` y `datos:` de `report/_variables.yml`: idénticos.

**Doble corrida desde un clon limpio.** `git clone` del HEAD a un directorio temporal; `python -m src.pipeline all` dos veces (rc = 0 en ambas):
- 63 archivos (todo lo versionado en `outputs/`, con las salidas de las specs 001, 003 y 004, más `report/_variables.yml`): **las dos corridas son idénticas** (sha256; textos con el fin de línea normalizado, PNG byte a byte).
- Los 63 son además **idénticos a lo comiteado** en el HEAD (mismo criterio).
- `git diff --ignore-cr-at-eol --stat`: vacío. En el repositorio de trabajo, `git status --porcelain`: 0 líneas.
- Sin embargo, en el clon, `git status --porcelain` devuelve 56 archivos «M» tras correr el pipeline: son **solo diferencias de fin de línea**, incluido `data/processed/panel.csv`, que no entró en el hash (el checkout deja CRLF por `core.autocrlf=true` y el pipeline escribe siempre LF; 0 diferencias de contenido). Los 4 archivos «sin seguimiento» eran los logs de mi propio script de verificación, no salidas del pipeline. Ver la observación O1.

## 2. Criterios de finalización de la spec

| Criterio | Estado | Evidencia |
|---|---|---|
| Spec aprobada y comiteada antes de la primera estimación (RNF-1) | Cumple | `ec983d0`, `45c43d5`, `7f732ce` (solo `specs/`; el del plan, además, `MEMORY.md`); salidas del Modelo II desde `7325ff2` |
| Salidas de RF-7 a RF-27: 14 tablas (`.md` y `.csv`) y 3 figuras | Cumple | `outputs/tables/model2_*` (28 archivos) y `model2_profile.png`, `model2_response.png`, `model2_cusum.png`; `test_models_stage_writes_the_14_tables_in_markdown_and_csv`, `test_models_stage_writes_the_three_figures_at_200_dpi` |
| Variables `modelo2.*` (RF-28) y exportación para la 005 (RF-29) | Cumple | `report/_variables.yml` (clave `modelo2:`), `outputs/models/model2_main.json`; tests de la sección 3 |
| `pipeline all` desde un clon limpio y dos corridas sin diferencias (RNF-8) | Cumple en contenido | sección 1; reserva de fin de línea en O1 |
| `uv run pytest -q` en verde, sin red | Cumple | 756 passed |
| `review-validate.md` y `review-audit.md` con `VEREDICTO: APROBADO` | **Parcial** | este informe: APROBADO; `review-audit.md`: pendiente (primera ronda en curso). T9 no se marca como hecha hasta entonces |

## 3. Requisitos funcionales

| Requisito | Qué exige | Evidencia (todos pasan en la corrida de la sección 1) |
|---|---|---|
| RF-1 | variables, rezagos y diferencias sobre la historia completa; recorte posterior | `test_build_columns` (test_design2.py)<br>`test_build_columns_reindexes_without_gaps` (test_design2.py)<br>`test_design_is_independent_of_k_through_window` (test_design2.py) |
| RF-2 | forma de DRALACBS leída de la tabla de la 001; error si no es la esperada | `test_stops_if_dralacbs_form_is_not_the_expected_one` (test_model2.py)<br>`test_expected_form_holds_on_the_real_stationarity_table` (test_frozen_model2.py) |
| RF-3 | muestra común M reportada en los pies | `test_common_window_starts_2000q2` (test_design2.py)<br>`test_common_window_does_not_drop_inner_nan` (test_design2.py)<br>`test_common_sample_and_selection_table` (test_model2.py)<br>`test_selection_note_reports_sample_and_rule` (test_model2.py)<br>`test_common_sample_is_2000q2_to_the_common_quarter_with_105_obs` (test_frozen_model2.py) |
| RF-4 | faltante dentro de la muestra: error con variable, trimestre y regresión | `test_design_nan_raises_with_variable_quarter_and_regression` (test_design2.py)<br>`test_design_missing_row_is_not_silently_dropped` (test_design2.py)<br>`test_lp_design_nan_raises` (test_design2.py) |
| RF-5 | un modelo por K = 1..8 sobre M; parada nombrando el K | `test_common_sample_and_selection_table` (test_model2.py)<br>`test_stops_naming_k_when_degrees_of_freedom_are_insufficient` (test_model2.py)<br>`test_selection_table_has_eight_models_on_the_same_sample` (test_frozen_model2.py) |
| RF-6 | K_BIC principal, K_AIC en R1; empate al menor K | `test_select_k_picks_minimums_and_resolves_ties_to_smaller_k` (test_dynamics.py)<br>`test_main_is_k_bic_and_matches_a_direct_estimation` (test_model2.py)<br>`test_r1_not_applicable_when_aic_and_bic_choose_the_same_k` (test_model2_outputs.py)<br>`test_r1_uses_the_aic_k_on_the_same_sample` (test_model2_outputs.py) |
| RF-7 | tabla de selección con marcas; K = 8 como limitación | `test_selection_marks_the_chosen_ks` (test_model2.py)<br>`test_detected_limitations_k8_not_calculable_leaks_and_non_i0` (test_model2_outputs.py)<br>`test_detected_limitation_names_k_aic_when_it_is_8` (test_model2_outputs.py) |
| RF-8 | tabla de coeficientes y su pie completo | `test_coefficient_table_and_footer` (test_model2.py)<br>`test_coefficient_note_has_every_rf8_item_with_values_from_the_fit` (test_model2.py) |
| RF-9 | perfil de θ_j con IC 95 % y línea en cero | `test_profile_has_one_point_per_lag_with_95_percent_ci_and_zero_line` (test_outputs_model2.py)<br>`test_profile_marks_the_peak_only_when_it_is_within_the_lags` (test_outputs_model2.py)<br>`test_figure_format` (test_outputs_model2.py) |
| RF-10 | S y S_rez con Wald HAC, IC 95 % y H1 | `test_cumulative_effects_closed_form` (test_dynamics.py)<br>`test_effects_table` (test_model2.py)<br>`test_recovers_known_parameters_end_to_end` (test_dynamics.py) |
| RF-11 | trayectoria ψ_h y R(h), h*, H2 y avisos de ρ | `test_multipliers_closed_form_k1` (test_dynamics.py)<br>`test_multipliers_match_a_simulated_impulse_response` (test_dynamics.py)<br>`test_peak_horizon_basic_and_sign` (test_dynamics.py)<br>`test_peak_horizon_tie_goes_to_smaller_h` (test_dynamics.py)<br>`test_trajectory_table_and_peak` (test_model2.py)<br>`test_rho_warnings` (test_model2.py) |
| RF-12 | prueba de Granger (Wald HAC sobre θ1..θK, sin θ0) | `test_granger_rejects_with_nonzero_lags` (test_dynamics.py)<br>`test_granger_does_not_reject_with_zero_lags` (test_dynamics.py)<br>`test_granger_excludes_theta0` (test_dynamics.py) |
| RF-13 | lectura de la evidencia (C1, C2, marca de signo contrario) | `test_evidence_reading_three_outcomes_and_contrary_mark` (test_dynamics.py)<br>`test_evidence_reading_uses_strict_5_percent` (test_dynamics.py)<br>`test_hypotheses` (test_dynamics.py)<br>`test_reading_table_and_note` (test_model2.py) |
| RF-14 | proyección local de la morosidad, h = 0..12 | `test_lp_recovers_cumulative_response_and_rate_path` (test_localproj.py)<br>`test_hac_window_is_max_of_formula_and_h_plus_1` (test_localproj.py)<br>`test_band_is_estimate_plus_minus_z90_times_se` (test_localproj.py)<br>`test_beta0_equals_theta0_with_same_se` (test_localproj.py) |
| RF-15 | proyección local de la tasa; φ_0 = 1 por construcción | `test_lp_recovers_cumulative_response_and_rate_path` (test_localproj.py)<br>`test_phi0_is_one_by_construction` (test_localproj.py) |
| RF-16 | horizonte sin grados de libertad o rango incompleto: «no estimada»; horizonte de detección | `test_horizon_without_degrees_of_freedom_is_not_estimated_and_others_unaffected` (test_localproj.py)<br>`test_incomplete_rank_is_not_estimated` (test_localproj.py)<br>`test_detection_horizon_first_band_excluding_zero` (test_localproj.py)<br>`test_detection_horizon_negative_band_counts_and_none` (test_localproj.py)<br>`test_detection_horizon_skips_not_estimated` (test_localproj.py) |
| RF-17 | comparación descriptiva con R(h), recuento «k de n» y su pie | `test_compare_with_trajectory_counts_and_signs` (test_localproj.py)<br>`test_compare_counts_from_real_lp_exclude_h0` (test_localproj.py)<br>`test_local_projections_and_comparison_are_attached` (test_model2.py) |
| RF-18 | gráfico de respuesta con dos paneles | `test_response_has_two_panels_with_the_right_series` (test_outputs_model2.py)<br>`test_response_marks_the_detection_horizon_only_when_there_is_one` (test_outputs_model2.py)<br>`test_response_leaves_gaps_for_not_estimated_horizons` (test_outputs_model2.py) |
| RF-19 | diagnósticos; White «no calculable» (C1); CUSUM sin trimestres de dummies | `test_diagnostics_table_rows` (test_model2.py)<br>`test_white_not_calculable_row_has_reason_and_no_verdict` (test_model2.py)<br>`test_white_not_calculable_at_model2_dimension` (test_diagnostics2.py)<br>`test_white_valid_with_k1` (test_diagnostics2.py)<br>`test_cusum_runs_without_the_impulse_quarters` (test_diagnostics2.py) |
| RF-20 | Chow con K + 7 interacciones, notas con trimestres útiles, rango previo | `test_chow_k_plus_7_interactions_at_k8` (test_diagnostics2.py)<br>`test_chow_counts_pre_and_post_quarters_net_of_impulse_dummies` (test_diagnostics2.py)<br>`test_chow_notes_name_k_plus_7_terms_and_both_counts` (test_model2.py)<br>`test_chow_rank_check_runs_before_estimating` (test_diagnostics2.py) |
| RF-21 | tabla de estacionariedad copiada de la 001 con «no I(0)» | `test_stationarity_rows_come_from_the_right_001_rows` (test_model2.py)<br>`test_stationarity_footer_says_lagged_terms_use_unlagged_series` (test_model2.py)<br>`test_stationarity_kpss_notation_matches_spec_001` (test_model2_outputs.py) |
| RF-22 | R1–R3 con el mismo estimador; estados «no estimada» y «no aplica» | `test_robustness_estimates_table_structure` (test_model2_outputs.py)<br>`test_robustness_estimates_dash_for_not_applicable_and_not_estimated` (test_model2_outputs.py)<br>`test_r2_excludes_covid_range_keeps_main_k_and_omits_dummies` (test_model2_outputs.py)<br>`test_r3_excludes_zero_rate_quarters` (test_design2.py y test_model2_outputs.py) |
| RF-23 | variante sin grados de libertad; dummy COVID omitida solo en R2 y R3 | `test_variant_without_degrees_of_freedom_is_not_estimated_with_reason` (test_model2_outputs.py)<br>`test_variant_covid_dummies_are_omitted_only_in_r2_and_r3` (test_model2_outputs.py)<br>`test_dummy_without_variation_is_error_outside_r2_r3` (test_design2.py) |
| RF-24 | resumen de robustez de S_rez y su pie (criterio, K, exclusiones, rezagos desde exclusiones) | `test_robustness_summary_criterion_and_denominator` (test_model2_outputs.py)<br>`test_robustness_note_has_criterion_ks_exclusions_and_lagged_quarters` (test_model2_outputs.py)<br>`test_lagged_from_excluded_hand_case` (test_design2.py) |
| RF-25 | limitaciones fijas y detectadas por código | `test_fixed_limitations_are_all_present_and_use_the_allowed_wording` (test_model2_outputs.py)<br>`test_detected_limitations_for_failed_diagnostics_variants_and_horizons` (test_model2_outputs.py)<br>`test_covid_lag_leaks_only_counts_y_lag_and_dffr` (test_design2.py)<br>`test_not_applicable_r1_is_not_a_limitation` (test_model2_outputs.py) |
| RF-26 | desviaciones frente a la guía y a la 003 | `test_deviations_table` (test_model2_outputs.py) |
| RF-27 | insumos de la comparación 6.3 leídos de las salidas de la 003 | `test_inputs63_reads_model1_from_its_outputs` (test_model2_outputs.py) |
| RF-28 | variables `modelo2.*` solo texto y con los dígitos de las tablas | `test_variables_keys_and_text_only` (test_outputs_model2.py)<br>`test_variables_have_the_same_digits_as_the_tables` (test_outputs_model2.py)<br>`test_variables_modelo2_block_has_the_planned_keys_and_is_text_only` (test_frozen_model2.py)<br>`test_variables_have_the_same_digits_as_the_csv_tables` (test_frozen_model2.py)<br>`test_variables_functions_write_no_numbers_by_hand` (test_outputs_model2.py) |
| RF-29 | exportación JSON para la spec 005 | `test_export_keys_order_and_values` (test_model2_outputs.py)<br>`test_export_json_roundtrips_exactly_without_nan` (test_model2_outputs.py)<br>`test_json_structure_and_matrix_dimensions` (test_frozen_model2.py) |
| RF-30 | tablas en Markdown y CSV, figuras en PNG, desde la etapa de modelos | `test_render_has_the_14_tables_in_both_formats` (test_model2_outputs.py)<br>`test_markdown_uses_decimal_comma_small_p_and_dashes` (test_model2_outputs.py)<br>`test_csv_keeps_full_precision_and_has_no_nan_or_inf` (test_model2_outputs.py)<br>`test_models_stage_writes_the_14_tables_in_markdown_and_csv` (test_frozen_model2.py)<br>`test_models_stage_writes_the_three_figures_at_200_dpi` (test_frozen_model1.py y test_frozen_model2.py) |

## 4. Requisitos no funcionales

| Requisito | Qué exige | Evidencia (todos pasan en la corrida de la sección 1) |
|---|---|---|
| RNF-1 | pre-registro: spec aprobada y comiteada antes de estimar | commits `ec983d0` (spec + review-clarify), `45c43d5` (cambio C1) y `7f732ce` (plan), todos con solo archivos de `specs/004-modelo-ii/` (el del plan, además, `MEMORY.md`); las salidas del Modelo II aparecen por primera vez en `7325ff2` (T8) |
| RNF-2 | tests del estimador (proceso A, BIC recupera K, HAC > clásico) | `test_recovers_known_parameters_end_to_end` (test_dynamics.py)<br>`test_select_k_recovers_true_k_with_bic` (test_dynamics.py)<br>`test_process_d_hac_exceeds_classical_with_autocorrelation` (test_diagnostics2.py) |
| RNF-3 | tests de efectos, trayectoria y lectura | `test_cumulative_effects_closed_form` (test_dynamics.py)<br>`test_multipliers_closed_form_k1` (test_dynamics.py)<br>`test_peak_horizon_tie_goes_to_smaller_h` (test_dynamics.py)<br>`test_granger_rejects_with_nonzero_lags` (test_dynamics.py)<br>`test_evidence_reading_three_outcomes_and_contrary_mark` (test_dynamics.py) |
| RNF-4 | tests de las proyecciones locales (proceso C, ventana ≥ h + 1) | `test_lp_recovers_cumulative_response_and_rate_path` (test_localproj.py)<br>`test_hac_window_is_max_of_formula_and_h_plus_1` (test_localproj.py) |
| RNF-5 | tests de las notas de pie | `test_selection_note_reports_sample_and_rule` (test_model2.py)<br>`test_coefficient_note_has_every_rf8_item_with_values_from_the_fit` (test_model2.py)<br>`test_trajectory_table_and_peak` (test_model2.py)<br>`test_chow_notes_name_k_plus_7_terms_and_both_counts` (test_model2.py)<br>`test_robustness_note_has_criterion_ks_exclusions_and_lagged_quarters` (test_model2_outputs.py)<br>`test_markdown_notes_close_the_tables_that_need_them` (test_model2_outputs.py) |
| RNF-6 | tests de los diagnósticos (BG, Chow, White, CUSUM) | `test_bg_rejects_ar1_errors_and_not_iid` (test_diagnostics2.py)<br>`test_chow_rejects_with_slope_break_and_not_without` (test_diagnostics2.py)<br>`test_white_not_calculable_at_model2_dimension` (test_diagnostics2.py)<br>`test_white_valid_with_k1` (test_diagnostics2.py)<br>`test_white_rank_elimination_at_k8_design_does_not_fail` (test_diagnostics2.py)<br>`test_chow_k_plus_7_interactions_at_k8` (test_diagnostics2.py)<br>`test_cusum_runs_without_the_impulse_quarters` (test_diagnostics2.py) |
| RNF-7 | semillas independientes para X y el ruido | `SEED2` y `SEED2 + 1` en `tests/synthetic_model2.py::make_full2` (`seed_x` y `seed_e`) |
| RNF-8 | reproducibilidad byte a byte | `test_two_independent_roots_leave_identical_bytes` (test_frozen_model2.py)<br>`test_running_models_twice_on_the_same_root_changes_nothing` (test_frozen_model2.py)<br>doble corrida de `pipeline all` desde un clon limpio (sección 1) |
| RNF-9 | sin red; lógica pura | `test_module_has_no_forbidden_imports` (test_model2_purity.py)<br>`test_module_never_fills_or_drops_missing_data` (test_model2_purity.py)<br>`test_module_does_not_read_or_write_files_or_urls` (test_model2_purity.py)<br>`test_module_has_no_randomness` (test_model2_purity.py)<br>`block_network` (autouse en `tests/conftest.py`) |
| RNF-10 | lenguaje de asociación | `test_no_banned_language_in_any_output` (test_model2_language.py)<br>`test_required_association_vocabulary_is_present` (test_model2_language.py)<br>`test_fixed_strings_in_the_source_have_no_banned_language` (test_model2_language.py)<br>`test_real_outputs_have_no_causal_language` (test_frozen_model1.py y test_frozen_model2.py) |
| RNF-11 | etiquetas en español | `test_figure_labels_are_in_spanish_without_causal_language` (test_outputs_model2.py)<br>`test_figure_and_table_labels_are_in_spanish` (test_model2_language.py) |

## 5. Plan: decisiones y puntos de la auditoría del plan

Los 9 puntos de `review-plan.md` y las decisiones D14 a D18 tienen su comprobación: White «no calculable» (D14, C1 en la spec) → `test_white_not_calculable_at_model2_dimension`; φ_0 = 1 (D15) → `test_phi0_is_one_by_construction`; nota propia del Chow (D16) → `test_chow_notes_name_k_plus_7_terms_and_both_counts`; rango del Chow antes de estimar (D17) → `test_chow_rank_check_runs_before_estimating`; `PEAK_TIE_TOL` como constante (D18) → `test_config_constants`. Las tolerancias del §7.1 no se relajaron en ningún test: los procesos A, B, C, D, E y F pasaron con los parámetros declarados (los únicos ajustes de tests fueron correcciones de expectativas mal escritas, anotadas en los commits).

## 6. Checklist de la skill econometria-series-tiempo

- Estacionariedad por término y regla: `model2_stationarity` (6 filas copiadas de la 001, con «no I(0)»); la forma de DRALACBS se comprueba antes de estimar (RF-2).
- Errores HAC y ventana: toda la inferencia pasa por `fit_ols_hac`; ventana de 4 rezagos con T = 105 y `max(fórmula, h + 1)` en las proyecciones (RF-14, RNF-4).
- Misma muestra para AIC y BIC: los 8 modelos tienen 105 observaciones (`test_selection_table_has_eight_models_on_the_same_sample`).
- Signos y sorpresas: H1 y H2 y la regla de lectura estaban pre-registradas; los resultados se reportan tal cual (sin cambiar la especificación).
- Lenguaje causal: ninguno en tablas, notas, variables, figuras ni textos fijos del código (`test_model2_language`).
- Diagnósticos fallidos: se reportan en `model2_diagnostics` y pasan a `model2_limitations`; White «no calculable» cuando corresponde.
- Dos corridas idénticas: sección 1.

## 7. Observaciones (no bloquean)

- **O1. Fin de línea en Windows.** Con `core.autocrlf=true`, tras correr el pipeline en un clon `git status --porcelain` lista como «M» los archivos de salida aunque no haya diferencias de contenido. Si se quiere que ese criterio se cumpla también en la lectura literal, habría que fijar el fin de línea de `outputs/`, `data/processed/` y `report/_variables.yml` con un `.gitattributes` (p. ej. `eol=lf`). No lo hice: es un cambio de configuración del repositorio que no pide la spec.
- **O2. Formato de ψ_h cercanos a cero.** `fmt_es` escribe «−0,000» (p. ej. en ψ_12). Arreglarlo cambiaría bytes de salidas del Modelo I; queda anotado en `MEMORY.md`.
- **O3. Trazabilidad del proceso D.** El test de «HAC mayor que el clásico» (proceso D, RNF-2) figuraba en el «Hecho cuando» de T1 y se escribió en T4 (`tests/test_diagnostics2.py`). Está cubierto, pero no en la tarea prevista.
- **O4. Tiempo de la suite.** 4 a 6 minutos por la lentitud del entorno; no hay un test de la 004 que domine el tiempo (los más lentos son de las specs 001 y 003).
- **O5. Independencia.** Ver la cabecera: el autor del código y de esta validación coinciden; la auditoría independiente es el contrapeso.

## 8. Conclusión

La implementación cumple la spec y el plan en lo que esta validación puede comprobar: 30 RF y 11 RNF con evidencia ejecutada, no regresión del Modelo I, reproducibilidad entre corridas y contra lo comiteado, y pre-registro anterior a la primera estimación. **VEREDICTO: APROBADO** para la validación; la spec 004 se cierra con `review-audit.md`.
