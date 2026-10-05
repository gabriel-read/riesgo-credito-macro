"""Tests para src/model1.py (spec 003, tarea 5: modelo principal, efectos, estacionariedad).

Cubre RF-3, RF-4, RF-7, RF-9, RF-10 y RF-15. Las tareas 6 y 7 completarán este archivo
(robusteces, limitaciones, desviaciones, exportación y fuera de muestra).

Datos sintéticos con parámetros conocidos. X y el ruido de y salen de semillas
independientes (con la misma semilla el ruido coincidiría con una columna de X y el
ajuste sería perfecto). Sin red ni disco.
"""

from __future__ import annotations

import dataclasses

import numpy as np
import pandas as pd
import pytest

import src.model1 as model1
from src.design import ModelDataError
from src.estimation import hac_lags, inference, long_run, standardization_sd
from src.model1 import (
    Model1Result,
    coefficient_table,
    effects_table,
    model_stationarity_table,
    run_model1,
    sign_match,
)
from src.model1_config import MACRO_TERMS, SEED

END = pd.Period("2026Q2", "Q-DEC")
TRUE = {
    "const": 0.02,
    "y_lag": 0.5,
    "gdp_growth": -0.10,
    "d_unemp": 0.60,
    "inflation": 0.05,
    "d_ffr": 0.20,
    "credit_growth": 0.03,
}


# --- Datos sintéticos ---


def make_full(seed_x: int = SEED, seed_e: int = SEED + 1, sigma: float = 0.2,
              params: dict | None = None) -> pd.DataFrame:
    """Historia 1998T1–2026T2 con ΔDR_t = c + ρ·ΔDR_{t−1} + Σ β·x_t + ε_t (DR en nivel)."""
    p = dict(TRUE if params is None else params)
    idx = pd.period_range("1998Q1", END, freq="Q-DEC")
    n = len(idx)
    rx = np.random.default_rng(seed_x)
    re = np.random.default_rng(seed_e)  # independiente de X
    gdp = rx.normal(2.0, 1.0, n)
    d_unemp = rx.normal(0.0, 0.3, n)
    infl = rx.normal(2.0, 0.5, n)
    d_ffr = rx.normal(0.0, 0.3, n)
    loans = rx.normal(5.0, 2.0, n)
    eps = re.normal(0.0, sigma, n)
    dy = np.zeros(n)
    for t in range(1, n):
        lagged_credit = loans[t - 4] if t >= 4 else 0.0
        dy[t] = (p["const"] + p["y_lag"] * dy[t - 1] + p["gdp_growth"] * gdp[t]
                 + p["d_unemp"] * d_unemp[t] + p["inflation"] * infl[t]
                 + p["d_ffr"] * d_ffr[t] + p["credit_growth"] * lagged_credit + eps[t])
    loans_yoy = loans.copy()
    loans_yoy[:4] = np.nan
    return pd.DataFrame(
        {
            "dralacbs": 2.0 + np.cumsum(dy),
            "gdpc1_yoy": gdp,
            "unrate_d": d_unemp,
            "cpiaucsl_yoy": infl,
            "fedfunds_d": d_ffr,
            "loans_yoy": loans_yoy,
        },
        index=idx,
    )


def _row(variable: str, forma: str, adf_stat, adf_p, kpss_stat, kpss_p, decision="", orden="") -> dict:
    return {
        "variable": variable, "etiqueta": variable, "forma": forma, "n_obs": 106,
        "adf_stat": adf_stat, "adf_p": adf_p, "adf_lags": 1,
        "kpss_stat": kpss_stat, "kpss_p": kpss_p, "kpss_p_truncado": "",
        "decision": decision, "orden": orden,
    }


def make_stationarity() -> pd.DataFrame:
    """Tabla de la spec 001 con los nombres reales de variable (unrate y fedfunds, no *_d)."""
    rows = [
        _row("dralacbs", "tal cual", -2.86, 0.0508, 0.376, 0.0876, "ambigua (primera diferencia)", "I(1)"),
        _row("dralacbs", "primera diferencia", -3.44, 0.0096, 0.140, 0.10),
        _row("dralacbn", "tal cual", -2.82, 0.06, 0.38, 0.09, "ambigua (primera diferencia)", "I(1)"),
        _row("dralacbs_logit", "tal cual", -2.15, 0.23, 0.50, 0.04, "primera diferencia", "posible I(2)"),
        _row("drclacbs", "tal cual", -2.46, 0.13, 0.84, 0.01, "primera diferencia", "I(1)"),
        _row("drblacbs", "tal cual", -2.52, 0.11, 0.75, 0.01, "primera diferencia", "I(1)"),
        _row("drsreacbs", "tal cual", -2.54, 0.11, 0.31, 0.10, "ambigua (primera diferencia)", "posible I(2)"),
        _row("gdpc1_yoy", "tal cual", -3.62, 0.01, 0.10, 0.10, "niveles", "I(0)"),
        _row("cpiaucsl_yoy", "tal cual", -2.34, 0.16, 0.23, 0.10, "ambigua (primera diferencia)", "I(1)"),
        _row("loans_yoy", "tal cual", -2.46, 0.13, 0.19, 0.10, "ambigua (primera diferencia)", "I(1)"),
        _row("unrate", "tal cual", -2.90, 0.05, 0.34, 0.10, "niveles", "I(0)"),
        _row("unrate", "primera diferencia", -12.03, 0.001, 0.09, 0.10),
        _row("fedfunds", "tal cual", -3.82, 0.001, 0.27, 0.10, "niveles", "I(0)"),
        _row("fedfunds", "primera diferencia", -4.24, 0.001, 0.14, 0.10),
    ]
    return pd.DataFrame(rows)


@pytest.fixture(scope="module")
def full() -> pd.DataFrame:
    return make_full()


@pytest.fixture(scope="module")
def stationarity() -> pd.DataFrame:
    return make_stationarity()


@pytest.fixture(scope="module")
def result(full, stationarity) -> Model1Result:
    return run_model1(full, stationarity, END)


# --- run_model1: muestra estricta y RF-4 antes de estimar ---


def test_main_sample_is_strict_2000q1_to_common_end(result):
    d = result.design
    assert d.X.index[0] == pd.Period("2000Q1", "Q-DEC")
    assert d.X.index[-1] == END
    assert result.fit.nobs == 106
    assert d.form == "primera diferencia"  # dralacbs es «ambigua»: entra en Δ


def test_result_carries_decisions_and_all_t5_tables(result):
    assert result.decisions["dralacbs"] == "ambigua (primera diferencia)"
    assert isinstance(result.coefficients, pd.DataFrame)
    assert isinstance(result.effects, pd.DataFrame)
    assert isinstance(result.stationarity, pd.DataFrame)
    assert isinstance(result.coef_footer, dict)


def test_changed_expected_form_stops_before_estimating(full, stationarity, monkeypatch):
    changed = stationarity.copy()
    changed.loc[
        (changed["variable"] == "dralacbs") & (changed["forma"] == "tal cual"), "decision"
    ] = "niveles"

    def boom(*args, **kwargs):
        raise AssertionError("no debe estimar si la forma esperada cambió")

    monkeypatch.setattr(model1, "fit_ols_hac", boom)
    with pytest.raises(ModelDataError, match="dralacbs"):
        run_model1(full, changed, END)


def test_missing_expected_variable_stops(full, stationarity):
    incomplete = stationarity[stationarity["variable"] != "drsreacbs"]
    with pytest.raises(ModelDataError, match="drsreacbs"):
        run_model1(full, incomplete, END)


def test_main_regression_without_enough_dof_stops(full, stationarity, monkeypatch):
    """RF-6: la principal se detiene (no se reporta «no estimada»), y antes de estimar."""
    monkeypatch.setattr(model1, "check_dof", lambda design: "grados de libertad insuficientes (< 30)")

    def boom(*args, **kwargs):
        raise AssertionError("no debe estimar sin grados de libertad")

    monkeypatch.setattr(model1, "fit_ols_hac", boom)
    with pytest.raises(ModelDataError, match="principal.*grados de libertad"):
        run_model1(full, stationarity, END)


def test_main_sample_too_short_to_contain_covid_quarters_stops(full, stationarity):
    """Con una muestra que no llega a 2020, las dummies COVID no varían: error, no omisión (D11)."""
    with pytest.raises(ModelDataError, match="covid_2020q2"):
        run_model1(full, stationarity, pd.Period("2000Q4", "Q-DEC"))


def test_missing_data_inside_the_main_sample_stops(full, stationarity):
    """RF-1/RF-2: un faltante en la principal es error (nombra variable y trimestre), no recorte."""
    holey = full.copy()
    holey.loc[pd.Period("2010Q3", "Q-DEC"), "gdpc1_yoy"] = np.nan
    with pytest.raises(ModelDataError, match="gdpc1_yoy.*2010Q3"):
        run_model1(holey, stationarity, END)


def test_main_sample_stops_if_history_ends_before_the_common_quarter(full, stationarity):
    """RF-1: 2000T1–último trimestre común, estricta; si los datos terminan antes, error."""
    with pytest.raises(ModelDataError, match=r"2000T1–2026T2.*2000T1–2026T3"):
        run_model1(full, stationarity, pd.Period("2026Q3", "Q-DEC"))


def test_main_sample_stops_if_history_starts_after_2000q1(full, stationarity):
    """Sin historia anterior a 2000T1 no hay rezagos para 2000T1: error, nunca recorte en silencio."""
    late = full.loc[pd.Period("2001Q1", "Q-DEC"):]
    with pytest.raises(ModelDataError, match="NaN en 2001Q1"):
        run_model1(late, stationarity, END)


# --- sign_match ---


@pytest.mark.parametrize(
    "expected, coef, esperado",
    [
        ("+", 0.3, "sí"), ("+", -0.3, "no"), ("+", 0.0, "no"),
        ("-", -0.3, "sí"), ("-", 0.3, "no"), ("-", 0.0, "no"),
        (None, 5.0, "sin contraste"), (None, -5.0, "sin contraste"),
    ],
)
def test_sign_match_truth_table(expected, coef, esperado):
    assert sign_match(expected, coef) == esperado


# --- coefficient_table ---


def test_coefficient_table_has_a_row_per_term_with_required_columns(result):
    tab = result.coefficients
    terms = list(result.fit.params.index)
    assert list(tab["termino"]) == terms
    assert len(terms) == 11  # const, y_lag, 5 macro y 4 dummies COVID
    for col in ["etiqueta", "coef", "ee_hac", "z", "p", "ic_inf", "ic_sup",
                "signo_esperado", "coincide", "nota"]:
        assert col in tab.columns


def test_coefficient_table_values_come_from_fit_and_normal_inference(result):
    tab = result.coefficients.set_index("termino")
    inf = inference(result.fit.params, result.fit.cov)
    for term in result.fit.params.index:
        assert tab.loc[term, "coef"] == pytest.approx(inf.loc[term, "coef"], rel=1e-12)
        assert tab.loc[term, "ee_hac"] == pytest.approx(inf.loc[term, "se"], rel=1e-12)
        assert tab.loc[term, "p"] == pytest.approx(inf.loc[term, "p"], abs=1e-12)
        assert tab.loc[term, "ic_inf"] == pytest.approx(inf.loc[term, "ic_inf"], rel=1e-12)
        assert tab.loc[term, "ic_sup"] == pytest.approx(inf.loc[term, "ic_sup"], rel=1e-12)


def test_coefficient_table_recovers_known_dgp(result):
    """Los coeficientes verdaderos caen en ±4 EE HAC (semilla fija, DGP con parámetros conocidos)."""
    assert result.fit.rsquared < 0.999  # guarda contra ajuste degenerado
    tab = result.coefficients.set_index("termino")
    for term, true in TRUE.items():
        gap = abs(tab.loc[term, "coef"] - true)
        assert gap < 4.0 * tab.loc[term, "ee_hac"], f"{term}: {tab.loc[term, 'coef']} vs {true}"
        assert gap < 0.15, term


def test_coefficient_table_expected_sign_and_match(result):
    tab = result.coefficients.set_index("termino")
    assert tab.loc["gdp_growth", "signo_esperado"] == "−"
    assert tab.loc["d_unemp", "signo_esperado"] == "+"
    assert tab.loc["d_ffr", "signo_esperado"] == "+"
    assert tab.loc["credit_growth", "signo_esperado"] == "+"
    for term in ["gdp_growth", "d_unemp", "d_ffr", "credit_growth"]:
        assert tab.loc[term, "coincide"] == "sí", term
    for term in ["inflation", "y_lag", "const"] + [t for t in tab.index if t.startswith("covid_")]:
        assert tab.loc[term, "signo_esperado"] == "sin contraste"
        assert tab.loc[term, "coincide"] == "sin contraste"


def test_coefficient_table_flags_contrary_sign():
    contrary = dict(TRUE, gdp_growth=+0.30)  # se espera «−»
    full_c = make_full(params=contrary)
    res = run_model1(full_c, make_stationarity(), END)
    tab = res.coefficients.set_index("termino")
    assert tab.loc["gdp_growth", "coef"] > 0
    assert tab.loc["gdp_growth", "coincide"] == "no"


def test_impulse_dummy_rows_carry_the_uninformative_se_note(result):
    tab = result.coefficients.set_index("termino")
    dummies = [t for t in tab.index if t.startswith("covid_")]
    assert len(dummies) == 4
    for t in dummies:
        assert "no informativo" in tab.loc[t, "nota"]
    for t in ["const", "y_lag", *MACRO_TERMS]:
        assert tab.loc[t, "nota"] == ""


def test_coefficient_footer_has_all_required_fields(result):
    f = result.coef_footer
    assert f["forma_y"] == "primera diferencia"
    assert f["muestra_inicio"] == "2000T1" and f["muestra_fin"] == "2026T2"
    assert f["n_obs"] == 106 and f["n_parametros"] == 11
    assert f["rezagos_hac"] == hac_lags(106) == 4
    assert f["r2"] == pytest.approx(result.fit.rsquared)
    assert f["r2_ajustado"] == pytest.approx(result.fit.rsquared_adj)
    assert f["ee_regresion"] == pytest.approx(result.fit.ser)
    assert f["truncamiento_espectral"] is False
    assert "rango reducido por dummies de impulso (esperado)" in f["nota_rango"]


def test_coefficient_footer_without_impulse_dummies_has_no_rank_note(full, stationarity):
    fit_no_covid = run_model1(full, stationarity, END).fit
    # reutiliza coefficient_table sobre un ajuste sin dummies de impulso
    design = fit_no_covid.design
    X = design.X.drop(columns=[c for c in design.X.columns if c.startswith("covid_")])
    fit2 = model1.fit_ols_hac(dataclasses.replace(design, X=X))
    _, footer = coefficient_table(fit2)
    assert footer["n_parametros"] == 7
    assert footer["nota_rango"] == ""


# --- effects_table ---


def _effect(tab: pd.DataFrame, term: str, efecto: str, escala: str) -> pd.Series:
    sel = tab[(tab["termino"] == term) & (tab["efecto"] == efecto) & (tab["escala"] == escala)]
    assert len(sel) == 1, (term, efecto, escala)
    return sel.iloc[0]


def test_effects_table_has_5_regressors_x_2_effects_x_2_scales(result):
    tab = result.effects
    assert len(tab) == 20
    assert set(tab["termino"]) == set(MACRO_TERMS)
    assert set(tab["efecto"]) == {"impacto", "largo plazo"}
    assert set(tab["escala"]) == {"por 1 pp", "por 1 DE"}
    for col in ["etiqueta", "estimacion", "ee", "p", "ic_inf", "ic_sup", "estado", "unidad"]:
        assert col in tab.columns
    assert (tab["estado"] == "reportado").all()  # ρ ≈ 0,5: 1 − ρ > 0,05


def test_impact_per_pp_is_the_hac_coefficient(result):
    inf = inference(result.fit.params, result.fit.cov)
    for term in MACRO_TERMS:
        r = _effect(result.effects, term, "impacto", "por 1 pp")
        assert r["estimacion"] == pytest.approx(inf.loc[term, "coef"], rel=1e-12)
        assert r["ee"] == pytest.approx(inf.loc[term, "se"], rel=1e-12)
        assert r["p"] == pytest.approx(inf.loc[term, "p"], abs=1e-12)


def test_long_run_per_pp_is_beta_over_one_minus_rho_with_delta_se(result):
    params, cov = result.fit.params, result.fit.cov
    rho = params["y_lag"]
    for term in MACRO_TERMS:
        r = _effect(result.effects, term, "largo plazo", "por 1 pp")
        b = params[term]
        assert r["estimacion"] == pytest.approx(b / (1 - rho), rel=1e-12)
        grad = np.array([1 / (1 - rho), b / (1 - rho) ** 2])
        V = cov.loc[[term, "y_lag"], [term, "y_lag"]].to_numpy()
        assert r["ee"] == pytest.approx(float(np.sqrt(grad @ V @ grad)), rel=1e-10)
        ref = long_run(params, cov, term)
        assert r["p"] == pytest.approx(ref["p"], abs=1e-12)


def test_effects_per_sd_scale_by_sd_without_covid_quarters(result):
    sd = standardization_sd(result.design)
    covid = [pd.Period(q, "Q-DEC") for q in ["2020Q2", "2020Q3", "2020Q4", "2021Q1"]]
    keep = ~result.design.X.index.isin(covid)
    for term in MACRO_TERMS:
        manual = float(result.design.X.loc[keep, term].std(ddof=1))
        assert sd[term] == pytest.approx(manual, rel=1e-12)
        for efecto in ["impacto", "largo plazo"]:
            pp = _effect(result.effects, term, efecto, "por 1 pp")
            de = _effect(result.effects, term, efecto, "por 1 DE")
            assert de["estimacion"] == pytest.approx(pp["estimacion"] * manual, rel=1e-10)
            assert de["ee"] == pytest.approx(pp["ee"] * manual, rel=1e-10)
            assert de["ic_inf"] == pytest.approx(pp["ic_inf"] * manual, rel=1e-10)
            assert de["ic_sup"] == pytest.approx(pp["ic_sup"] * manual, rel=1e-10)
            assert de["p"] == pytest.approx(pp["p"], abs=1e-12)  # el p no depende de la escala


def test_sd_excludes_covid_so_it_differs_from_the_full_sample_sd(full, stationarity):
    """C1: un salto atípico en 2020T2 no debe inflar la DE del efecto «por 1 DE»."""
    spiky = full.copy()
    spiky.loc[pd.Period("2020Q2", "Q-DEC"), "unrate_d"] = 9.0
    res = run_model1(spiky, stationarity, END)
    sd = standardization_sd(res.design)
    assert sd["d_unemp"] < 0.5
    assert float(res.design.X["d_unemp"].std(ddof=1)) > 0.8


def test_effects_units_are_percentage_points_of_delinquency(result):
    assert result.effects["unidad"].str.contains("pp de morosidad").all()
    assert result.effects["unidad"].str.contains("por 1 pp del regresor").any()
    assert result.effects["unidad"].str.contains("por 1 DE del regresor").any()


@pytest.mark.parametrize("rho", [0.96, 0.99, 1.02])
def test_long_run_not_reported_when_one_minus_rho_is_at_most_005(result, rho):
    params = result.fit.params.copy()
    params["y_lag"] = rho
    tab = effects_table(dataclasses.replace(result.fit, params=params))
    lr = tab[tab["efecto"] == "largo plazo"]
    assert len(lr) == 10
    assert (lr["estado"] == "no reportado (1 − ρ ≤ 0,05)").all()
    assert lr["estimacion"].isna().all() and lr["ee"].isna().all()
    imp = tab[tab["efecto"] == "impacto"]
    assert (imp["estado"] == "reportado").all()  # el impacto se reporta siempre
    assert imp["estimacion"].notna().all()


def test_long_run_reported_just_below_the_threshold(result):
    params = result.fit.params.copy()
    params["y_lag"] = 0.90  # 1 − ρ = 0,10 > 0,05
    tab = effects_table(dataclasses.replace(result.fit, params=params))
    assert (tab["estado"] == "reportado").all()
    r = _effect(tab, "d_unemp", "largo plazo", "por 1 pp")
    assert r["estimacion"] == pytest.approx(params["d_unemp"] / 0.10, rel=1e-12)


def test_per_sd_is_undefined_when_sd_is_zero(result):
    design = result.fit.design
    X = design.X.copy()
    X["d_ffr"] = 0.5  # constante: DE = 0
    fit = dataclasses.replace(result.fit, design=dataclasses.replace(design, X=X))
    tab = effects_table(fit)
    for efecto in ["impacto", "largo plazo"]:
        de = _effect(tab, "d_ffr", efecto, "por 1 DE")
        assert de["estado"] == "no definido"
        assert np.isnan(de["estimacion"])
        pp = _effect(tab, "d_ffr", efecto, "por 1 pp")
        assert pp["estado"] == "reportado"
    # los demás regresores no se ven afectados
    assert _effect(tab, "d_unemp", "impacto", "por 1 DE")["estado"] == "reportado"


# --- model_stationarity_table ---


def _st(tab: pd.DataFrame, termino: str) -> pd.Series:
    sel = tab[tab["termino"] == termino]
    assert len(sel) == 1, termino
    return sel.iloc[0]


def test_model_stationarity_table_has_dependent_lag_and_five_regressors(result):
    tab = result.stationarity
    assert list(tab["termino"]) == ["Y", "y_lag", *MACRO_TERMS]
    for col in ["etiqueta", "columna_panel", "forma", "adf_stat", "adf_p", "kpss_stat",
                "kpss_p", "decision", "orden", "no_i0", "nota"]:
        assert col in tab.columns


def test_dependent_in_delta_is_judged_with_its_first_difference_row(result, stationarity):
    """ΔDRALACBS: ADF p = 0,0096 y KPSS p = 0,10 ⇒ estacionaria en la forma en que entra."""
    y = _st(result.stationarity, "Y")
    assert y["forma"] == "primera diferencia"
    assert y["columna_panel"] == "dralacbs"
    assert y["adf_p"] == pytest.approx(0.0096) and y["kpss_p"] == pytest.approx(0.10)
    assert y["decision"] == "niveles" and y["orden"] == "I(0)" and y["no_i0"] == "no"
    lag = _st(result.stationarity, "y_lag")
    assert lag["adf_p"] == y["adf_p"] and lag["orden"] == "I(0)" and lag["no_i0"] == "no"
    assert "rezag" in lag["nota"]


def test_delta_regressors_use_their_first_difference_rows(result):
    for term, base in [("d_unemp", "unrate"), ("d_ffr", "fedfunds")]:
        r = _st(result.stationarity, term)
        assert r["forma"] == "primera diferencia"
        assert r["columna_panel"] == base
        assert r["orden"] == "I(0)" and r["no_i0"] == "no"
        assert r["adf_p"] == pytest.approx(0.001)


def test_tal_cual_regressors_copy_decision_and_order_from_the_001_table(result, stationarity):
    gdp = _st(result.stationarity, "gdp_growth")
    assert gdp["forma"] == "tal cual" and gdp["decision"] == "niveles"
    assert gdp["orden"] == "I(0)" and gdp["no_i0"] == "no"
    for term, col in [("inflation", "cpiaucsl_yoy"), ("credit_growth", "loans_yoy")]:
        r = _st(result.stationarity, term)
        src = stationarity[(stationarity["variable"] == col) & (stationarity["forma"] == "tal cual")].iloc[0]
        assert r["forma"] == "tal cual"
        assert r["decision"] == "ambigua (primera diferencia)" and r["orden"] == "I(1)"
        assert r["no_i0"] == "sí"
        assert r["adf_stat"] == src["adf_stat"] and r["kpss_p"] == src["kpss_p"]


def test_credit_row_notes_that_it_uses_the_unlagged_series(result):
    assert "sin rezagar" in _st(result.stationarity, "credit_growth")["nota"]


def test_non_i0_flags_list_exactly_inflation_and_credit(result):
    flagged = list(result.stationarity.loc[result.stationarity["no_i0"] == "sí", "termino"])
    assert flagged == ["inflation", "credit_growth"]


def test_dependent_entering_in_levels_uses_the_tal_cual_row(stationarity):
    decisions = {"dralacbs": "niveles"}
    tab = model_stationarity_table(stationarity, decisions)
    y = _st(tab, "Y")
    assert y["forma"] == "nivel"
    src = stationarity[(stationarity["variable"] == "dralacbs") & (stationarity["forma"] == "tal cual")].iloc[0]
    assert y["adf_p"] == src["adf_p"]


def test_delta_form_that_is_not_stationary_is_flagged_non_i0(stationarity):
    bad = stationarity.copy()
    bad.loc[(bad["variable"] == "unrate") & (bad["forma"] == "primera diferencia"), "adf_p"] = 0.40
    tab = model_stationarity_table(bad, {"dralacbs": "ambigua (primera diferencia)"})
    r = _st(tab, "d_unemp")
    assert r["no_i0"] == "sí" and r["orden"] == "no I(0)"
