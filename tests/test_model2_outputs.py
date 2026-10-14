"""Tests de src/model2.py, parte de la tarea 6 (spec 004): robusteces, limitaciones, desviaciones,
insumos de la 6.3, exportación para la spec 005 y salida en Markdown y CSV de las 14 tablas.

Cubre RF-22 a RF-27, RF-29, RF-30, RNF-5 y RNF-8. Datos sintéticos; sin red ni datos reales.
"""

from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd
import pytest

from src.design2 import build_columns, build_design2, common_window, covid_lag_leaks, zero_rate_quarters
from src.dynamics import cumulative_effects
from src.estimation import fit_ols_hac
from src.model2 import (
    VariantOutcome2,
    _format_cell,
    deviations_table2,
    diagnostics_table2,
    export2_json,
    fmt_kpss_p2,
    limitations_table2,
    render_model2_tables,
    robustness_estimates2,
    robustness_note2,
    robustness_summary2,
    run_variant2,
    stationarity_table2,
)
from src.model2_config import (
    COVID_NAMES,
    EXPECTED_FORM,
    FIXED_LIMITATIONS2,
    MAIN2,
    PREREG_DEVIATIONS2,
    ROBUST2,
)
from tests.synthetic_model1 import make_stationarity
from tests.synthetic_model2 import END, make_full2, with_zero_rate
from tests.test_language import find_causal_language

DEC = EXPECTED_FORM
R1, R2, R3 = ROBUST2
P = lambda s: pd.Period(s, "Q-DEC")  # noqa: E731
STEMS = [
    "model2_selection", "model2_coefficients", "model2_effects", "model2_trajectory", "model2_reading",
    "model2_lp", "model2_comparison", "model2_diagnostics", "model2_stationarity",
    "model2_robustness_estimates", "model2_robustness_summary", "model2_limitations", "model2_deviations",
    "model2_inputs63",
]


@pytest.fixture(scope="module")
def result(model2_result):
    return model2_result


@pytest.fixture(scope="module")
def setup():
    full = make_full2()
    window = common_window(build_columns(full, DEC), END)
    return full, window


def _no_estimada(spec, reason="grados de libertad insuficientes (< 30)"):
    return VariantOutcome2(spec, "no estimada", reason, None, None, None, None, None)


# --- R1 (RF-6, RF-22) ---


def test_r1_not_applicable_when_aic_and_bic_choose_the_same_k(setup):
    full, window = setup
    o = run_variant2(full, R1, 3, 3, DEC, window, END)
    assert o.status == "no aplica" and "AIC y BIC eligen el mismo K" in o.reason and o.fit is None


def test_r1_uses_the_aic_k_on_the_same_sample(setup):
    full, window = setup
    o = run_variant2(full, R1, 3, 5, DEC, window, END)
    assert o.status == "estimada" and o.K == 5 and o.fit.k == 5 + 11 and o.fit.nobs == 105
    assert o.design.spec_id == "R1" and o.design.dropped == []


# --- R2 y R3 (RF-22, RF-23) ---


def test_r2_excludes_covid_range_keeps_main_k_and_omits_dummies(setup):
    full, window = setup
    o = run_variant2(full, R2, 4, 6, DEC, window, END)
    assert o.status == "estimada" and o.K == 4 and o.fit.nobs == 105 - 8
    assert o.design.dropped == list(COVID_NAMES)
    assert not any(q in o.design.y.index for q in pd.period_range("2020Q1", "2021Q4", freq="Q-DEC"))
    assert o.fit.k == 4 + 7
    assert set(o.effects) == {"S", "S_rez"} and o.peak["h_star"] >= 0 and o.hyp["h1_signo"] in ("sí", "no")


def test_r3_excludes_zero_rate_quarters(setup):
    full, window = setup
    f = with_zero_rate(full, [("2009Q1", "2015Q4"), ("2020Q2", "2021Q1")])
    o = run_variant2(f, R3, 3, 3, DEC, window, END)
    zr = zero_rate_quarters(f, window[0], window[1])
    assert o.status == "estimada" and o.K == 3 and o.fit.nobs == 105 - len(zr) == 73
    assert o.design.dropped == list(COVID_NAMES)


def test_variant_without_degrees_of_freedom_is_not_estimated_with_reason(setup):
    full, window = setup
    f = with_zero_rate(full, [("2000Q2", "2018Q4")])          # quedan 30 observaciones
    o = run_variant2(f, R3, 3, 3, DEC, window, END)
    assert o.status == "no estimada" and "grados de libertad" in o.reason and o.fit is None
    assert o.design is not None and o.effects is None


def test_variant_covid_dummies_are_omitted_only_in_r2_and_r3(setup):
    full, _ = setup
    early = (P("2000Q2"), P("2019Q4"))
    with pytest.raises(Exception, match="sin variación"):
        run_variant2(full, R1, 3, 5, DEC, early, END)
    assert run_variant2(full, R2, 3, 5, DEC, early, END).status == "estimada"


# --- Tablas de robustez (RF-22, RF-24) ---


def test_robustness_estimates_table_structure(result):
    t = result.robustness_estimates
    assert list(t["variante"]) == ["R1", "R2", "R3"]
    for col in ("K", "inicio", "fin", "n_obs", "rezagos_hac", "S", "ee_S", "p_S", "S_rez", "ee_S_rez",
                "p_S_rez", "h_estrella", "h1", "estado", "motivo", "nota"):
        assert col in t.columns
    for _, r in t.iterrows():
        if r["estado"] == "estimada":
            assert r["n_obs"] > 0 and np.isfinite(r["S_rez"]) and r["motivo"] == ""


def test_robustness_estimates_dash_for_not_applicable_and_not_estimated(setup):
    full, window = setup
    est = run_variant2(full, R2, 3, 3, DEC, window, END)
    t = robustness_estimates2([run_variant2(full, R1, 3, 3, DEC, window, END), est, _no_estimada(R3)])
    r1, r3 = t.iloc[0], t.iloc[2]
    assert r1["estado"] == "no aplica" and "AIC y BIC" in r1["motivo"] and np.isnan(r1["S"]) and r1["h1"] == "—"
    assert r3["estado"] == "no estimada" and "grados de libertad" in r3["motivo"] and np.isnan(r3["p_S_rez"])
    assert t.iloc[1]["estado"] == "estimada" and t.iloc[1]["K"] == 3


def test_robustness_summary_criterion_and_denominator(setup):
    full, window = setup
    main = cumulative_effects(fit_ols_hac(build_design2(full, MAIN2, 3, DEC, window, END)), 3)
    r2 = run_variant2(full, R2, 3, 3, DEC, window, END)
    outcomes = [run_variant2(full, R1, 3, 3, DEC, window, END), r2, _no_estimada(R3)]
    t = robustness_summary2(main, outcomes)
    assert list(t["termino"]) == ["S_rez", "S"]
    row = t.iloc[0]
    assert row["R1"] == "no aplica" and row["R3"] == "no estimada" and row["R2"] in ("sí", "no")
    assert row["n"] == 1 and row["k"] == (1 if row["R2"] == "sí" else 0)
    assert row["robustez"] == f"{row['k']} de 1" and row["p_principal"] == pytest.approx(main["S_rez"]["p"])
    same_sign = np.sign(r2.effects["S_rez"]["est"]) == np.sign(main["S_rez"]["est"])
    assert (row["R2"] == "sí") == bool(same_sign and r2.effects["S_rez"]["p"] < 0.10)


def test_robustness_note_has_criterion_ks_exclusions_and_lagged_quarters(setup):
    full, window = setup
    f = with_zero_rate(full, [("2009Q1", "2015Q4"), ("2020Q2", "2021Q1")])
    outcomes = [run_variant2(f, R1, 3, 5, DEC, window, END), run_variant2(f, R2, 3, 5, DEC, window, END),
                run_variant2(f, R3, 3, 5, DEC, window, END)]
    n = robustness_note2(outcomes, window)
    assert "mismo signo que la principal y p < 0,10" in n and "S_rez" in n
    assert "K: R1 = 5, R2 = 3, R3 = 3" in n
    assert "R2 excluye 2020T1–2021T4" in n and "R3 excluye 32 trimestres" in n and "2009T1–2015T4" in n
    assert "rezagos salen de trimestres excluidos" in n
    assert "R2: 2022T1" in n                                        # trimestres calculados por código
    assert find_causal_language(n) == []


def test_robustness_summary_matches_estimates_in_the_result(result):
    s, e = result.robustness_summary.iloc[0], result.robustness_estimates.set_index("variante")
    for v in ("R1", "R2", "R3"):
        if e.loc[v, "estado"] != "estimada":
            assert s[v] == e.loc[v, "estado"]
    assert result.robustness_note.startswith("Nota:")


# --- Limitaciones (RF-25) ---


@pytest.fixture(scope="module")
def k8(setup):
    full, window = setup
    fit = fit_ols_hac(build_design2(full, MAIN2, 8, DEC, window, END))
    return fit, diagnostics_table2(fit, 8)


def test_fixed_limitations_are_all_present_and_use_the_allowed_wording(result):
    t = result.limitations
    fixed = t[t["origen"] == "fija"]
    assert list(fixed["limitacion"]) == [n for n, _ in FIXED_LIMITATIONS2] and len(fixed) == 8
    assert "no identifica el efecto de la política monetaria" in " ".join(fixed["detalle"])
    assert set(t["origen"]) <= {"fija", "detectada"}


def test_detected_limitations_k8_not_calculable_leaks_and_non_i0(setup, k8):
    full, window = setup
    fit, diag = k8
    st = stationarity_table2(make_stationarity())
    t = limitations_table2(8, 3, 8, diag, fit, [], pd.DataFrame({"h": [0], "estado": ["estimada"], "motivo": [""]}),
                           st, window)
    det = t[t["origen"] == "detectada"]
    names = list(det["limitacion"])
    assert any(n.startswith("K_BIC = 8") for n in names)
    assert "White: no calculable" in names
    assert "Regresores no I(0)" in names
    non_i0 = det.loc[det["limitacion"] == "Regresores no I(0)", "detalle"].iloc[0]
    assert "π" in non_i0 and "CRED" in non_i0 and "PIB" not in non_i0
    leaks = det[det["limitacion"].str.startswith("Rezagos de ΔFFR o ΔDR")]
    assert len(leaks) == 1
    expected = covid_lag_leaks(fit.design, 8)
    assert expected[0] == P("2020Q3") and expected[-1] == P("2023Q1")   # K = 8: hasta 8 rezagos desde 2021T1
    assert "2020T3–2023T1" in leaks["detalle"].iloc[0]


def test_detected_limitation_names_k_aic_when_it_is_8(setup, k8):
    full, window = setup
    fit, diag = k8
    st = stationarity_table2(make_stationarity())
    lp = pd.DataFrame({"h": [0], "estado": ["estimada"], "motivo": [""]})
    t = limitations_table2(3, 8, 3, diag, fit, [], lp, st, window)
    assert any(n.startswith("K_AIC = 8") for n in t["limitacion"]) and not any(
        n.startswith("K_BIC = 8") for n in t["limitacion"])


def test_detected_limitations_for_failed_diagnostics_variants_and_horizons(setup, k8):
    full, window = setup
    fit, diag = k8
    diag = diag.copy()
    diag.loc[diag["prueba"] == "Breusch-Godfrey", "veredicto"] = "falla"
    lp = pd.DataFrame({"h": [0, 11, 12], "estado": ["estimada", "no estimada", "no estimada"],
                       "motivo": ["", "grados de libertad insuficientes (< 30)", "grados de libertad insuficientes (< 30)"]})
    t = limitations_table2(3, 3, 3, diag, fit, [_no_estimada(R3), _no_estimada(R1, "x")], lp,
                           stationarity_table2(make_stationarity()), window)
    names = list(t["limitacion"])
    assert "Breusch-Godfrey: falla" in names
    bg = t.loc[t["limitacion"] == "Breusch-Godfrey: falla", "detalle"].iloc[0]
    assert "inconsistente" in bg
    assert "Variante R3 no estimada" in names and "Variante R1 no estimada" in names
    hz = t.loc[t["limitacion"].str.startswith("Horizontes de las proyecciones locales"), "detalle"].iloc[0]
    assert "h = 11" in hz and "h = 12" in hz
    assert find_causal_language(" ".join(t["detalle"].astype(str))) == []


def test_not_applicable_r1_is_not_a_limitation(setup, k8):
    full, window = setup
    fit, diag = k8
    o = VariantOutcome2(R1, "no aplica", "AIC y BIC eligen el mismo K", None, None, None, None, None)
    t = limitations_table2(3, 3, 3, diag, fit, [o], pd.DataFrame({"h": [0], "estado": ["estimada"], "motivo": [""]}),
                           stationarity_table2(make_stationarity()), window)
    assert not any("R1" in n for n in t["limitacion"])


# --- Desviaciones (RF-26) ---


def test_deviations_table(result):
    t = result.deviations
    assert list(t.columns) == ["decision", "referencia", "motivo"]
    text = " ".join(t["decision"] + " " + t["motivo"])
    assert "2000T2–2026T2" in text and "2000T1" in text and "8 rezagos" in text
    assert "2026-01-01" in text and "BIC" in text and "AIC" in text
    assert "≤ 0,25" in text and "GDP nominal" in text and "1985" in text
    for fecha, cambio, _ in PREREG_DEVIATIONS2:
        assert any(r.startswith(f"{fecha} · {cambio}") for r in t["decision"])
    assert find_causal_language(text) == []


# --- Insumos de la 6.3 (RF-27) ---


def test_inputs63_reads_model1_from_its_outputs(result, model1_result):
    t = result.inputs63
    assert list(t["modelo"]) == ["Modelo I (spec 003)", "Modelo II (spec 004)"]
    m1 = model1_result.coefficients.set_index("termino").loc["d_ffr"]
    r1, r2 = t.iloc[0], t.iloc[1]
    assert r1["coef"] == pytest.approx(m1["coef"]) and r1["ee_hac"] == pytest.approx(m1["ee_hac"])
    assert r1["p"] == pytest.approx(m1["p"]) and r1["n_obs"] == model1_result.coef_footer["n_obs"]
    assert r1["muestra"] == f"{model1_result.coef_footer['muestra_inicio']}–{model1_result.coef_footer['muestra_fin']}"
    fit = result.main_fit
    assert r2["coef"] == pytest.approx(fit.params["d_ffr_l0"])
    assert r2["ee_hac"] == pytest.approx(math.sqrt(fit.cov.loc["d_ffr_l0", "d_ffr_l0"]))
    assert r2["n_obs"] == 105 and r2["muestra"] == "2000T2–2026T2"
    assert "contemporáneos" in r1["controles"] and "rezagados" in r2["controles"]
    assert "spec 006" in result.inputs63_note


# --- Exportación para la spec 005 (RF-29) ---


def test_export_keys_order_and_values(result):
    d = result.export
    assert list(d) == ["spec", "dependent", "form", "k", "k_criterion", "terms", "columns", "params", "cov_hac",
                       "psd_adjusted", "hac_lags", "sample_start", "sample_end", "nobs", "covid_quarters",
                       "psi", "response", "h_star", "reading"]
    fit, K = result.main_fit, result.K
    assert d["spec"] == "004-modelo-ii" and d["dependent"] == "dralacbs" and d["k"] == K
    assert d["k_criterion"] == "BIC" and d["form"] == "primera diferencia"
    assert d["terms"] == list(fit.params.index) and d["params"] == fit.params.to_numpy(dtype=float).tolist()
    k = len(d["terms"])
    assert len(d["cov_hac"]) == k and all(len(r) == k for r in d["cov_hac"])
    assert np.allclose(np.array(d["cov_hac"]), np.array(d["cov_hac"]).T)
    assert d["hac_lags"] == 4 and d["nobs"] == 105 and d["psd_adjusted"] is bool(fit.psd_adjusted)
    assert (d["sample_start"], d["sample_end"]) == ("2000T2", "2026T2")
    assert d["covid_quarters"] == ["2020T2", "2020T3", "2020T4", "2021T1"]
    assert len(d["psi"]) == len(d["response"]) == 13
    assert d["response"] == result.trajectory["R"].tolist()
    assert d["h_star"] == {"h": result.peak["h_star"], "signo": result.peak["signo"]}
    assert set(d["reading"]) == {"etiqueta", "c1", "c2"} and d["reading"]["etiqueta"] == result.reading["etiqueta"]
    assert d["columns"]["d_ffr_l2"] == {"column": "fedfunds_d", "lag": 2}
    assert d["columns"]["credit_l4"] == {"column": "loans_yoy", "lag": 4}
    assert d["columns"]["y_lag"] == {"column": "dralacbs_d", "lag": 1}
    assert d["columns"]["const"] is None and d["columns"]["covid_2020q2"] is None


def test_export_json_roundtrips_exactly_without_nan(result):
    text = export2_json(result.export)
    assert text.endswith("\n") and "NaN" not in text and "Infinity" not in text
    assert json.loads(text) == result.export
    assert export2_json(result.export) == text


# --- Salida en Markdown y CSV (RF-30, RNF-8) ---


@pytest.fixture(scope="module")
def rendered(result):
    return render_model2_tables(result)


def test_render_has_the_14_tables_in_both_formats(rendered):
    assert list(rendered) == STEMS and len(STEMS) == 14
    for stem, text in rendered.items():
        assert set(text) == {"md", "csv"} and text["md"].startswith("|") and text["csv"].count("\n") >= 2, stem


def test_render_is_deterministic(result, rendered):
    assert render_model2_tables(result) == rendered


def test_markdown_uses_decimal_comma_small_p_and_dashes(rendered):
    coef = rendered["model2_coefficients"]["md"]
    assert "." not in coef.split("\n\n")[0].replace("...", "")        # coma decimal en la tabla
    lp = rendered["model2_lp"]["md"]
    row0 = [l for l in lp.split("\n") if l.startswith("| 0 |")][0]
    assert "—" in row0 and "por construcción (identidad)" in row0 and "1,000" in row0
    reading = rendered["model2_reading"]["md"]
    assert "—" in reading
    assert _format_cell("adf_p", 0.0004) == "< 0,001" and _format_cell("p_S_rez", 0.0004) == "< 0,001"
    assert _format_cell("p", 0.0316) == "0,032" and _format_cell("coef", 0.12345) == "0,123"
    assert _format_cell("n_obs", pd.NA) == "—" and _format_cell("phi_ee", None) == "—"


def test_markdown_notes_close_the_tables_that_need_them(result, rendered):
    for stem, note in (("model2_selection", result.selection_note), ("model2_coefficients", result.coef_note),
                       ("model2_effects", result.effects_note), ("model2_trajectory", result.trajectory_note),
                       ("model2_reading", result.reading_note), ("model2_comparison", result.comparison_note),
                       ("model2_stationarity", result.stationarity_note),
                       ("model2_robustness_summary", result.robustness_note),
                       ("model2_inputs63", result.inputs63_note), ("model2_lp", result.lp_note)):
        assert rendered[stem]["md"].endswith(note), stem


def test_stationarity_kpss_notation_matches_spec_001(rendered):
    assert fmt_kpss_p2(0.10) == "> 0,10" and fmt_kpss_p2(0.1) == "> 0,10" and fmt_kpss_p2(0.01) == "< 0,01"
    assert fmt_kpss_p2(0.0432) == "0,043" and fmt_kpss_p2(float("nan")) == "—"
    md = rendered["model2_stationarity"]["md"]
    assert "> 0,10" in md and "≥ 0,10" not in md


def test_csv_keeps_full_precision_and_has_no_nan_or_inf(result, rendered):
    for stem, text in rendered.items():
        fields = {f.strip('"').lower() for line in text["csv"].split("\n")[1:] for f in line.split(",")}
        assert not fields & {"nan", "inf", "-inf", "none", "<na>"}, stem
    csv = pd.read_csv(pd.io.common.StringIO(rendered["model2_coefficients"]["csv"]))
    assert np.allclose(csv["coef"], result.coefficients["coef"], rtol=1e-12, atol=0)   # precisión completa
    lp = rendered["model2_lp"]["csv"].split("\n")[1].split(",")
    assert "—" in lp


def test_rendered_text_has_no_causal_language(rendered):
    assert find_causal_language(" ".join(t["md"] + t["csv"] for t in rendered.values())) == []

