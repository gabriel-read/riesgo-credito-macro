"""Tests de src/model2.py, parte de la tarea 5 (spec 004): selección, principal y tablas.

Cubre RF-3 a RF-13, RF-17 a RF-21 y RNF-5 con datos sintéticos (nunca datos reales). Las robusteces,
limitaciones, desviaciones, exportación y texto en Markdown/CSV son de la tarea 6.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.design import ModelDataError
from src.design2 import build_columns, build_design2, common_window
from src.dynamics import cumulative_effects
from src.estimation import fit_ols_hac
from src.model2 import (
    diagnostics_table2,
    rho_warning,
    run_model2,
    stationarity_table2,
    trajectory_note,
)
from src.model2_config import COVID_NAMES, EXPECTED_FORM, MAIN2, TERM_LABELS2, term_label2
from src.model1 import IMPULSE_SE_NOTE, RANK_NOTE
from src.tables import fmt_es
from tests.synthetic_model1 import make_stationarity
from tests.synthetic_model2 import END, make_full2
from tests.test_language import find_causal_language

DEC = EXPECTED_FORM


@pytest.fixture(scope="module")
def result(model2_result):
    return model2_result


@pytest.fixture(scope="module")
def fit_k8():
    full = make_full2()
    window = common_window(build_columns(full, DEC), END)
    return fit_ols_hac(build_design2(full, MAIN2, 8, DEC, window, END))


def _texts(res) -> list[str]:
    frames = [res.selection, res.coefficients, res.effects, res.trajectory, res.reading_table,
              res.lp, res.comparison, res.diagnostics, res.stationarity]
    out = [res.selection_note, res.coef_note, res.effects_note, res.trajectory_note, res.reading_note,
           res.comparison_note, res.stationarity_note]
    for df in frames:
        out += list(df.columns)
        out += [str(v) for v in df.to_numpy().ravel()]
    return out


# --- RF-2: forma de DRALACBS ---


def test_stops_if_dralacbs_form_is_not_the_expected_one(model1_result):
    st = make_stationarity()
    st.loc[(st["variable"] == "dralacbs") & (st["forma"] == "tal cual"), "decision"] = "niveles"
    with pytest.raises(ModelDataError) as e:
        run_model2(make_full2(), st, END, model1_result)
    msg = str(e.value)
    assert "dralacbs" in msg and EXPECTED_FORM in msg and "niveles" in msg


# --- RF-3 a RF-7: muestra común, selección y principal ---


def test_common_sample_and_selection_table(result):
    assert result.window == (pd.Period("2000Q2", "Q-DEC"), END) and result.nobs == 105
    t = result.selection
    assert list(t["K"]) == list(range(1, 9)) and list(t["nobs"]) == [105] * 8
    assert list(t["n_params"]) == [K + 11 for K in range(1, 9)]
    assert set(t.columns) == {"K", "n_params", "nobs", "aic", "bic", "marca"}
    assert all(result.fits[K].nobs == 105 for K in range(1, 9))


def test_selection_marks_the_chosen_ks(result):
    t = result.selection.set_index("K")
    kb, ka = result.k_bic, result.k_aic
    assert t.loc[kb, "bic"] == t["bic"].min() or np.isclose(t.loc[kb, "bic"], t["bic"].min())
    if kb == ka:
        assert t.loc[kb, "marca"] == "K_AIC y K_BIC (principal)"
    else:
        assert t.loc[kb, "marca"] == "K_BIC (principal)" and t.loc[ka, "marca"] == "K_AIC (R1)"
    assert (t["marca"] != "").sum() == (1 if kb == ka else 2)


def test_selection_note_reports_sample_and_rule(result):
    n = result.selection_note
    assert "2000T2–2026T2" in n and "n = 105" in n and "BIC" in n and "menor K" in n
    assert f"K_BIC = {result.k_bic}" in n and f"K_AIC = {result.k_aic}" in n


def test_main_is_k_bic_and_matches_a_direct_estimation(result):
    full = make_full2()
    window = common_window(build_columns(full, DEC), END)
    direct = fit_ols_hac(build_design2(full, MAIN2, result.k_bic, DEC, window, END))
    assert result.K == result.k_bic and result.main_fit.k == result.K + 11
    assert np.allclose(result.main_fit.params, direct.params) and result.main_fit.hac_lags == 4


def test_stops_naming_k_when_degrees_of_freedom_are_insufficient(model1_result):
    full = make_full2(n=53, start="2010Q1")            # M de 44 observaciones: K = 4 deja 29 gl
    with pytest.raises(ModelDataError) as e:
        run_model2(full, make_stationarity(), full.index[-1], model1_result)
    assert "K = 4" in str(e.value)


# --- RF-8: coeficientes ---


def test_coefficient_table_and_footer(result):
    t = result.coefficients
    assert list(t["termino"]) == list(result.main_fit.params.index)
    assert set(t.columns) == {"termino", "etiqueta", "coef", "ee_hac", "z", "p", "ic_inf", "ic_sup", "nota"}
    for name in COVID_NAMES:
        assert t.loc[t["termino"] == name, "nota"].iloc[0] == IMPULSE_SE_NOTE
    assert (t.loc[~t["termino"].isin(COVID_NAMES), "nota"] == "").all()
    f = result.coef_footer
    assert f["K"] == result.K and f["criterio"] == "BIC" and f["forma_y"] == "primera diferencia"
    assert (f["muestra_inicio"], f["muestra_fin"], f["n_obs"]) == ("2000T2", "2026T2", 105)
    assert f["n_parametros"] == result.K + 11 and f["rezagos_hac"] == 4 and f["nota_rango"] == RANK_NOTE


def test_coefficient_note_has_every_rf8_item_with_values_from_the_fit(result):
    n, f = result.coef_note, result.coef_footer
    for piece in (f"K = {result.K}", "BIC", "primera diferencia", "2000T2–2026T2", "n = 105",
                  f"parámetros = {result.K + 11}", f"R² = {fmt_es(result.main_fit.rsquared, 3)}",
                  f"R² ajustado = {fmt_es(result.main_fit.rsquared_adj, 3)}",
                  f"error estándar de la regresión = {fmt_es(result.main_fit.ser, 3)}",
                  "ventana HAC de 4 rezagos", "truncamiento espectral: ", RANK_NOTE):
        assert piece in n, piece


# --- RF-10 a RF-13: efectos, trayectoria, Granger y lectura ---


def test_effects_table(result):
    t = result.effects.set_index("efecto")
    eff = cumulative_effects(result.main_fit, result.K)
    assert list(t.index) == ["S", "S_rez"]
    for key in ("S", "S_rez"):
        assert t.loc[key, "est"] == pytest.approx(eff[key]["est"])
        assert t.loc[key, "ee_hac"] == pytest.approx(eff[key]["se"])
        assert t.loc[key, "chi2"] == pytest.approx(eff[key]["chi2"])
        assert t.loc[key, "p"] == pytest.approx(eff[key]["p"])
    assert t.loc["S", "h1_signo"] in ("sí", "no")
    assert t.loc["S", "h1_respaldada"] in ("respaldada", "no respaldada")
    assert t.loc["S_rez", "h1_signo"] == "—" and t.loc["S_rez", "h1_respaldada"] == "—"
    assert "pp de morosidad por 1 pp" in result.effects_note and "χ²(1)" in result.effects_note


def test_trajectory_table_and_peak(result):
    t = result.trajectory
    assert list(t["h"]) == list(range(13)) and set(t.columns) == {"h", "psi", "R", "h_estrella"}
    assert np.allclose(t["R"], t["psi"].cumsum())
    star = result.peak["h_star"]
    assert list(t.loc[t["h_estrella"] == "sí", "h"]) == [star]
    assert abs(t.loc[star, "psi"]) == pytest.approx(t["psi"].abs().max())
    n = result.trajectory_note
    assert "no lleva bandas" in n and "proyección local" in n and f"h* = {star}" in n
    assert f"H2 (h* ≥ 1): {result.hyp['h2']}" in n


@pytest.mark.parametrize("rho,explosive,sensitive", [(0.5, False, False), (0.94, False, False),
                                                      (0.95, False, True), (0.97, False, True),
                                                      (1.02, True, True), (-1.1, True, False)])
def test_rho_warnings(rho, explosive, sensitive):
    w = rho_warning(rho)
    assert ("explosiva" in w) is explosive and ("muy sensible" in w) is sensitive
    note = trajectory_note(rho, {"h_star": 1, "signo": "+"}, {"h2": "sí"})
    assert (w in note) and (w == "" or w in note)


def test_reading_table_and_note(result):
    t = result.reading_table
    assert len(t) == 4 and set(t.columns) == {"elemento", "estadistico", "gl", "p", "resultado"}
    g = result.granger
    assert t.iloc[0]["estadistico"] == pytest.approx(g["stat"]) and t.iloc[0]["gl"] == result.K
    assert t.iloc[0]["resultado"] == g["veredicto"]
    assert t.iloc[1]["resultado"] == ("sí" if result.reading["c1"] else "no")
    assert t.iloc[2]["resultado"] == ("sí" if result.reading["c2"] else "no")
    expected = result.reading["etiqueta"] + (" · signo contrario al esperado" if result.reading["signo_contrario"] else "")
    assert t.iloc[3]["resultado"] == expected
    assert np.isnan(t.iloc[1]["estadistico"]) and np.isnan(t.iloc[1]["p"])      # se escribirá «—»
    assert "precedencia temporal" in result.reading_note


# --- RF-14 a RF-17 integrados ---


def test_local_projections_and_comparison_are_attached(result):
    lp = result.lp
    assert list(lp["h"]) == list(range(13)) and lp.loc[0, "phi"] == 1.0
    assert lp.loc[0, "phi_nota"] == "por construcción (identidad)"
    c = result.comparison
    assert list(c["h"]) == list(range(13)) and c.loc[0, "mismo_signo"] == "sí"
    assert result.comparison_counts["n"] == 12
    n = result.comparison_note
    assert "objetos distintos" in n and "descriptiva" in n and "h = 0" in n
    assert result.comparison_counts["k_de_n"] in n and result.comparison_counts["horizonte_deteccion"] in n


# --- RF-19, RF-20: diagnósticos ---


def test_diagnostics_table_rows(result):
    names = list(result.diagnostics["prueba"])
    for expected in ("Breusch-Godfrey", "Breusch-Pagan", "White", "Jarque-Bera", "RESET",
                     "Chow 2008T3", "Chow 2020T2", "CUSUM"):
        assert expected in names
    vif_rows = [n for n in names if n.startswith("VIF (")]
    assert len(vif_rows) == 1 + (result.K + 1) + 4         # y_lag, ΔFFR(t..t−K) y los controles
    assert not any(c in " ".join(names) for c in COVID_NAMES) and "VIF (const)" not in names


def test_white_not_calculable_row_has_reason_and_no_verdict(fit_k8):
    t = diagnostics_table2(fit_k8, 8).set_index("prueba")
    w = t.loc["White"]
    assert w["veredicto"] == "no calculable" and np.isnan(w["estadístico"]) and np.isnan(w["p_valor"])
    assert "n − rango(Z_aux)" in w["nota"] and "< 30" in w["nota"]
    assert w["veredicto"] not in ("pasa", "falla")


def test_chow_notes_name_k_plus_7_terms_and_both_counts(fit_k8):
    t = diagnostics_table2(fit_k8, 8).set_index("prueba")
    n20, n08 = t.loc["Chow 2020T2", "nota"], t.loc["Chow 2008T3", "nota"]
    for n in (n20, n08):
        assert "15 términos" in n and "β₁–β₅" not in n and "dummies COVID sin interactuar" in n
    assert "anteriores: 80" in n20 and "posteriores: 21" in n20
    assert "el tamaño empírico del contraste puede diferir del 5 % nominal" in n20
    assert "anteriores: 33" in n08 and "posteriores: 68" in n08 and "puede diferir" not in n08
    assert t.loc["Chow 2020T2", "veredicto"] in ("pasa", "falla")


def test_cusum_row_and_other_rows_keep_the_model1_format(fit_k8):
    t = diagnostics_table2(fit_k8, 8).set_index("prueba")
    assert t.loc["CUSUM", "veredicto"] in ("pasa", "falla") and np.isnan(t.loc["CUSUM", "p_valor"])
    assert t.loc["Breusch-Godfrey", "veredicto"] in ("pasa", "falla")
    vif_row = t.loc["VIF (y_lag)"]
    assert vif_row["veredicto"] in ("alerta", "sin alerta") and np.isnan(vif_row["p_valor"])
    assert list(diagnostics_table2(fit_k8, 8).columns) == ["prueba", "estadístico", "p_valor", "veredicto", "nota"]


# --- RF-21: estacionariedad ---


def test_stationarity_rows_come_from_the_right_001_rows():
    st = make_stationarity()
    t = stationarity_table2(st).set_index("termino")
    assert list(t.index) == ["d_dr", "d_ffr", "gdp_l1", "d_unemp_l1", "inflation_l1", "credit_l4"]
    for term, variable, forma in (("d_dr", "dralacbs", "primera diferencia"),
                                  ("d_ffr", "fedfunds", "primera diferencia"),
                                  ("d_unemp_l1", "unrate", "primera diferencia"),
                                  ("gdp_l1", "gdpc1_yoy", "tal cual"),
                                  ("inflation_l1", "cpiaucsl_yoy", "tal cual"),
                                  ("credit_l4", "loans_yoy", "tal cual")):
        src = st[(st["variable"] == variable) & (st["forma"] == forma)].iloc[0]
        assert t.loc[term, "forma"] == forma and t.loc[term, "columna_panel"] == variable
        assert t.loc[term, "adf_stat"] == src["adf_stat"] and t.loc[term, "kpss_p"] == src["kpss_p"]
    assert t.loc["gdp_l1", "decision"] == "niveles" and t.loc["gdp_l1", "no_i0"] == "no"
    assert t.loc["inflation_l1", "orden"] == "I(1)" and t.loc["inflation_l1", "no_i0"] == "sí"
    assert t.loc["credit_l4", "no_i0"] == "sí"
    assert t.loc["d_ffr", "decision"] == "niveles" and t.loc["d_ffr", "no_i0"] == "no"


def test_stationarity_footer_says_lagged_terms_use_unlagged_series(result):
    n = result.stationarity_note
    assert "sin rezagar" in n and "primera diferencia" in n and "no I(0)" in n
    t = result.stationarity.set_index("termino")
    assert "sin rezagar" in t.loc["credit_l4", "nota"] and "sin rezagar" in t.loc["gdp_l1", "nota"]
    assert t.loc["d_dr", "nota"] != "" and "sin rezagar" not in t.loc["d_dr", "nota"]


def test_stationarity_missing_row_raises():
    st = make_stationarity()
    st = st[~((st["variable"] == "fedfunds") & (st["forma"] == "primera diferencia"))]
    with pytest.raises(ModelDataError):
        stationarity_table2(st)


# --- Etiquetas, lenguaje y consistencia interna ---


def test_term_labels():
    assert term_label2("d_ffr_l0").startswith("ΔFFR(t)") and term_label2("d_ffr_l3") == "ΔFFR(t−3)"
    assert term_label2("covid_2020q2") == "Dummy COVID 2020T2"
    assert term_label2("credit_l4").startswith("CRED(t−4)") and "const" in TERM_LABELS2
    assert all(term_label2(t) for t in ("y_lag", "gdp_l1", "d_unemp_l1", "inflation_l1"))


def test_no_causal_language_in_tables_or_notes(result, fit_k8):
    assert find_causal_language(" ".join(_texts(result))) == []
    t = diagnostics_table2(fit_k8, 8)
    assert find_causal_language(" ".join(map(str, t.to_numpy().ravel()))) == []


def test_internal_consistency_between_tables(result):
    assert result.effects_raw["S"]["est"] == pytest.approx(
        sum(result.main_fit.params[f"d_ffr_l{j}"] for j in range(result.K + 1)))
    assert result.trajectory.loc[0, "psi"] == pytest.approx(result.main_fit.params["d_ffr_l0"])
    assert result.lp.loc[0, "beta"] == pytest.approx(result.main_fit.params["d_ffr_l0"], abs=1e-9)
    assert result.comparison.loc[0, "R"] == pytest.approx(result.trajectory.loc[0, "R"])
    assert result.coef_footer["n_obs"] == result.main_fit.nobs
