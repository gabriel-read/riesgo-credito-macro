"""Tests para src/model1.py (spec 003, tareas 5 y 6).

T5: RF-3, RF-4, RF-7, RF-9, RF-10 y RF-15 (modelo principal, efectos, estacionariedad).
T6: RF-5, RF-6, RF-8, RF-16, RF-17, RF-20, RF-21 y RF-23 (robusteces R1–R8, criterio de
robustez, diagnósticos, limitaciones, desviaciones, exportación).
T7: RF-18 (validación fuera de muestra: a un paso y dinámico, ingenuo, DM-HLN, veredictos).

Datos sintéticos con parámetros conocidos. X y el ruido de y salen de semillas
independientes (con la misma semilla el ruido coincidiría con una columna de X y el
ajuste sería perfecto). Sin red ni disco.
"""

from __future__ import annotations

import dataclasses
import json
import re

import numpy as np
import pandas as pd
import pytest

import src.model1 as model1
from src.design import ModelDataError
from src.estimation import hac_lags, inference, long_run, standardization_sd
from src.design import build_design, read_decisions
from src.estimation import fit_ols_hac
from src.forecast import diebold_mariano_hln, oos_verdicts
from src.model1 import (
    Model1Result,
    OOSResult,
    VariantOutcome,
    coefficient_note,
    coefficient_table,
    deviations_table,
    effects_table,
    is_robust,
    limitations_table,
    model_stationarity_table,
    out_of_sample,
    render_model1_tables,
    robustness_estimates,
    robustness_summary,
    run_model1,
    run_variant,
    sign_match,
    stress_export,
    stress_export_json,
)
from src.model1_config import (
    COVID_QUARTERS,
    FIXED_LIMITATIONS,
    MACRO_TERMS,
    MAIN,
    PREREG_DEVIATIONS,
    SEED,
    VARIANTS,
    VariantSpec,
)

from tests.synthetic_model1 import END, TRUE, make_full, make_stationarity

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
    # se espera «−» para el PIB; la constante compensa la deriva para que DR siga en (0, 100)
    contrary = dict(TRUE, gdp_growth=+0.30, const=-0.85)
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


# =====================================================================================
# Tarea 6: robusteces, criterio de robustez, diagnósticos, limitaciones, desviaciones,
# exportación (RF-5, RF-6, RF-8, RF-16, RF-17, RF-20, RF-21, RF-23)
# =====================================================================================


def Q(s: str) -> pd.Period:
    return pd.Period(s, "Q-DEC")


def spec_of(vid: str) -> VariantSpec:
    return next(v for v in VARIANTS if v.id == vid)


@pytest.fixture(scope="module")
def decisions(stationarity) -> dict:
    return read_decisions(stationarity)


@pytest.fixture(scope="module")
def full_long() -> pd.DataFrame:
    """Historia desde 1983T1: con ella R8 sí tiene historia anterior a 2000T1."""
    return make_full(start="1983Q1")


def by_id(res: Model1Result) -> dict:
    return {o.spec.id: o for o in res.variants}


# --- Criterio de robustez pre-registrado: mismo signo y p < 0,10 con error HAC ---


@pytest.mark.parametrize(
    "main, coef, p, esperado",
    [
        (0.5, 0.3, 0.04, True),
        (0.5, 0.3, 0.0999, True),
        (0.5, 0.3, 0.10, False),    # p < 0,10 es estricto
        (0.5, 0.3, 0.50, False),    # mismo signo pero no significativo
        (0.5, -0.3, 0.001, False),  # significativo pero de signo contrario
        (-0.5, -0.2, 0.05, True),
        (-0.5, 0.2, 0.05, False),
        (0.5, 0.0, 0.01, False),    # coeficiente nulo: sin signo
        (0.0, 0.3, 0.01, False),    # la principal sin signo no sirve de referencia
        (0.5, 0.3, float("nan"), False),
    ],
)
def test_is_robust_truth_table(main, coef, p, esperado):
    assert is_robust(main, coef, p) is esperado


# --- run_variant: cada variante cambia un solo aspecto (RF-5, RF-6) ---


def test_r1_excludes_2020_2021_and_drops_the_covid_dummies(full, decisions):
    o = run_variant(full, spec_of("R1"), decisions, END)
    assert o.status == "estimada" and o.reason == ""
    X = o.design.X
    assert o.fit.nobs == 106 - 8
    assert not any(c.startswith("covid_") for c in X.columns)
    assert sorted(o.design.dropped) == sorted(f"covid_{q.lower()}" for q in COVID_QUARTERS)
    for q in pd.period_range("2020Q1", "2021Q4", freq="Q-DEC"):
        assert q not in X.index
    assert X.index[0] == Q("2000Q1") and X.index[-1] == END


def test_r2_uses_dralacbn_with_seasonal_dummies_and_q1_as_base(full, decisions):
    o = run_variant(full, spec_of("R2"), decisions, END)
    assert o.status == "estimada"
    X = o.design.X
    assert [c for c in X.columns if c.startswith("seasonal_")] == [
        "seasonal_q2", "seasonal_q3", "seasonal_q4"
    ]
    np.testing.assert_allclose(o.design.y, full["dralacbn"].diff().loc[o.design.y.index])


@pytest.mark.parametrize("vid, col", [
    ("R3_drclacbs", "drclacbs"), ("R3_drblacbs", "drblacbs"), ("R3_drsreacbs", "drsreacbs"),
])
def test_r3_subportfolios_use_their_own_dependent(full, decisions, result, vid, col):
    o = run_variant(full, spec_of(vid), decisions, END)
    assert o.status == "estimada"
    np.testing.assert_allclose(o.design.y, full[col].diff().loc[o.design.y.index])
    assert list(o.design.X.columns) == list(result.design.X.columns)


def test_r4_uses_nominal_gdp_instead_of_real_gdp(full, decisions, result):
    """Regresión: build_design ignoraba spec.gdp_column y R4 repetía la principal."""
    o = run_variant(full, spec_of("R4"), decisions, END)
    X = o.design.X
    np.testing.assert_allclose(X["gdp_growth"], full["gdp_yoy"].loc[X.index])
    assert not np.allclose(X["gdp_growth"], full["gdpc1_yoy"].loc[X.index])
    assert o.fit.params["gdp_growth"] != pytest.approx(result.fit.params["gdp_growth"], rel=1e-6)
    # el resto de regresores y la dependiente son los de la principal
    for t in ["d_unemp", "inflation", "d_ffr", "credit_growth"]:
        np.testing.assert_allclose(X[t], result.design.X[t])
    np.testing.assert_allclose(o.design.y, result.design.y)


def test_build_design_picks_gdp_column_from_the_spec(full, decisions):
    d_main = build_design(full, MAIN, decisions["dralacbs"], END)
    d_r4 = build_design(full, spec_of("R4"), decisions["dralacbs"], END)
    np.testing.assert_allclose(d_main.X["gdp_growth"], full["gdpc1_yoy"].loc[d_main.X.index])
    np.testing.assert_allclose(d_r4.X["gdp_growth"], full["gdp_yoy"].loc[d_r4.X.index])


def test_r5_logit_is_flagged_as_not_in_pp(full, decisions):
    o = run_variant(full, spec_of("R5"), decisions, END)
    assert o.status == "estimada" and o.spec.in_pp is False
    np.testing.assert_allclose(o.design.y, full["dralacbs_logit"].diff().loc[o.design.y.index])


@pytest.mark.parametrize(
    "vid, lag, start, nobs", [("R6", 8, "2001Q1", 102), ("R7", 12, "2002Q1", 98)]
)
def test_r6_r7_truncate_to_the_available_history(full, decisions, vid, lag, start, nobs):
    o = run_variant(full, spec_of(vid), decisions, END)
    assert o.status == "estimada"
    assert o.design.X.index[0] == Q(start) and o.fit.nobs == nobs
    X = o.design.X
    np.testing.assert_allclose(X["credit_growth"], full["loans_yoy"].shift(lag).loc[X.index])


def test_r8_is_not_estimated_without_history_before_2000q1(full, decisions):
    o = run_variant(full, spec_of("R8"), decisions, END)
    assert o.status == "no estimada" and o.fit is None
    assert o.reason == "sin historia anterior a 2000T1"


def test_r8_is_estimated_when_history_goes_back_before_2000q1(full_long, decisions):
    o = run_variant(full_long, spec_of("R8"), decisions, END)
    assert o.status == "estimada"
    assert o.design.X.index[0] == Q("1985Q1")
    assert o.fit.nobs == 166  # 1985T1–2026T2


def test_variant_with_too_few_degrees_of_freedom_is_not_estimated_with_a_reason(full, decisions):
    short = VariantSpec("Rx", "muestra corta", start=Q("2018Q1"))
    o = run_variant(full, short, decisions, END)
    assert o.status == "no estimada" and o.fit is None
    assert "grados de libertad" in o.reason


def test_variant_with_rank_deficient_x_is_not_estimated(full, decisions, monkeypatch):
    monkeypatch.setattr(
        model1, "check_dof", lambda design: "matriz de regresores de rango incompleto"
    )
    o = run_variant(full, spec_of("R4"), decisions, END)
    assert o.status == "no estimada" and "rango incompleto" in o.reason


def test_missing_term_inside_a_variant_sample_stops_with_variable_and_quarter(full, decisions):
    """RF-2: un faltante dentro de la muestra de una variante es error, no «no estimada»."""
    holey = full.copy()
    holey.loc[Q("2010Q3"), "gdp_yoy"] = np.nan
    with pytest.raises(ModelDataError, match=r"gdp_yoy.*2010Q3.*R4"):
        run_variant(holey, spec_of("R4"), decisions, END)
    run_variant(holey, MAIN, decisions, END)  # la principal no usa gdp_yoy


# --- Conexión con los diagnósticos de T3 ---


def test_run_model1_connects_all_t3_diagnostics(result):
    d = result.diagnostics
    assert set(d["prueba"]) == {
        "Breusch-Godfrey", "Breusch-Pagan", "White", "Jarque-Bera", "RESET",
        "VIF (y_lag)", *(f"VIF ({t})" for t in MACRO_TERMS),
        "Chow 2008Q3", "Chow 2020Q2", "CUSUM",
    }
    assert len(d) == 14
    assert set(d["veredicto"]) <= {"pasa", "falla", "alerta", "sin alerta"}
    assert result.cusum["veredicto"] in {"pasa", "falla"}
    assert len(result.cusum["cusum"]) == len(result.cusum["lower"]) == len(result.cusum["upper"])


# --- Tabla de robustez: estimaciones (RF-16) ---


def test_run_model1_estimates_nine_variants_and_flags_r8(result):
    ids = [o.spec.id for o in result.variants]
    assert ids == [v.id for v in VARIANTS] and len(ids) == 10
    st = {o.spec.id: o.status for o in result.variants}
    assert st.pop("R8") == "no estimada"
    assert set(st.values()) == {"estimada"}


def test_robustness_estimates_has_five_rows_per_estimated_variant_and_one_otherwise(result):
    tab = result.robustness_estimates
    assert len(tab) == 9 * 5 + 1
    for col in ["variante", "etiqueta", "dependiente", "forma_y", "terminos_diferencia", "inicio",
                "fin", "n_obs", "rezagos_hac", "termino", "coef", "ee_hac", "p", "estado",
                "motivo", "nota"]:
        assert col in tab.columns
    est = tab[tab["estado"] == "estimada"]
    for vid, grp in est.groupby("variante"):
        assert list(grp["termino"]) == list(MACRO_TERMS), vid
    r8 = tab[tab["variante"] == "R8"]
    assert len(r8) == 1
    assert r8.iloc[0]["estado"] == "no estimada"
    assert r8.iloc[0]["motivo"] == "sin historia anterior a 2000T1"
    assert np.isnan(r8.iloc[0]["coef"])


def test_robustness_estimates_values_come_from_each_variant_fit(result):
    tab = result.robustness_estimates
    o = by_id(result)["R4"]
    inf = inference(o.fit.params, o.fit.cov)
    for t in MACRO_TERMS:
        row = tab[(tab["variante"] == "R4") & (tab["termino"] == t)].iloc[0]
        assert row["coef"] == pytest.approx(inf.loc[t, "coef"], rel=1e-12)
        assert row["ee_hac"] == pytest.approx(inf.loc[t, "se"], rel=1e-12)
        assert row["p"] == pytest.approx(inf.loc[t, "p"], abs=1e-12)
        assert row["n_obs"] == o.fit.nobs


def test_robustness_estimates_declares_sample_form_terms_and_notes(result):
    tab = result.robustness_estimates

    def first(vid: str) -> pd.Series:
        return tab[tab["variante"] == vid].iloc[0]

    assert first("R1")["n_obs"] == 98
    assert "2020T1–2021T4" in first("R1")["nota"]
    assert "quita: covid_2020q2" in first("R1")["terminos_diferencia"]
    assert "añade: seasonal_q2, seasonal_q3, seasonal_q4" in first("R2")["terminos_diferencia"]
    assert first("R3_drclacbs")["dependiente"] == "drclacbs"
    assert first("R5")["dependiente"] == "dralacbs_logit"
    assert "no está en pp" in first("R5")["nota"]
    assert first("R6")["inicio"] == "2001T1" and first("R7")["inicio"] == "2002T1"
    assert "historia disponible" in first("R6")["nota"]
    assert first("R4")["terminos_diferencia"] == ""
    est = tab["estado"] == "estimada"
    assert (tab.loc[est, "forma_y"] == "primera diferencia").all()
    assert (tab.loc[est, "rezagos_hac"] > 0).all()


# --- Tabla de robustez: resumen regresor × variante (RF-17) ---


def test_robustness_summary_shape_and_cells(result):
    tab = result.robustness_summary
    ids = [v.id for v in VARIANTS]
    assert len(ids) == 10  # R1, R2, R3 (×3), R4, R5, R6, R7, R8
    assert list(tab["termino"]) == list(MACRO_TERMS)
    for col in [*ids, "k", "n", "robustez"]:
        assert col in tab.columns
    cells = set(np.concatenate([tab[v].to_numpy() for v in ids]))
    assert cells <= {"sí", "no", "no estimada"}
    assert (tab["R8"] == "no estimada").all()


def test_robustness_summary_cells_follow_the_preregistered_criterion(result):
    tab = result.robustness_summary.set_index("termino")
    main = result.fit.params
    rob = result.robustness_estimates
    for vid in [v.id for v in VARIANTS if v.id != "R8"]:
        for t in MACRO_TERMS:
            row = rob[(rob["variante"] == vid) & (rob["termino"] == t)].iloc[0]
            esperado = "sí" if is_robust(main[t], row["coef"], row["p"]) else "no"
            assert tab.loc[t, vid] == esperado, (vid, t)


def test_robustness_count_k_of_n_excludes_not_estimated_variants(result):
    tab = result.robustness_summary.set_index("termino")
    ids = [v.id for v in VARIANTS]
    for t in MACRO_TERMS:
        cells = [tab.loc[t, v] for v in ids]
        assert tab.loc[t, "n"] == 9  # R8 no estimada no cuenta
        assert tab.loc[t, "k"] == cells.count("sí")
        assert tab.loc[t, "robustez"] == f"{tab.loc[t, 'k']} de 9"


def test_strong_regressor_is_robust_in_every_estimated_variant(result):
    """DGP con ΔU fuerte (β = 0,6 con DE 0,3 frente a σ = 0,2): el criterio debe dar k = n."""
    tab = result.robustness_summary.set_index("termino")
    assert tab.loc["d_unemp", "robustez"] == "9 de 9"


def test_summary_denominator_drops_when_a_variant_is_not_estimated(result):
    outcomes = list(result.variants)
    i = next(k for k, o in enumerate(outcomes) if o.spec.id == "R7")
    outcomes[i] = VariantOutcome(
        outcomes[i].spec, "no estimada", "grados de libertad insuficientes (< 30)",
        outcomes[i].design, None,
    )
    tab = robustness_summary(result.fit, outcomes).set_index("termino")
    assert (tab["R7"] == "no estimada").all()
    assert (tab["n"] == 8).all()
    assert (tab["robustez"] == tab["k"].astype(str) + " de 8").all()


def test_summary_with_no_estimated_variant_reports_zero_of_zero(result):
    outcomes = [VariantOutcome(o.spec, "no estimada", "prueba", o.design, None) for o in result.variants]
    tab = robustness_summary(result.fit, outcomes)
    assert (tab["robustez"] == "0 de 0").all()


# --- Tabla de limitaciones (RF-20) ---


def _diag(rows: list[tuple]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["prueba", "estadístico", "p_valor", "veredicto", "nota"])


CLEAN_DIAG = _diag([
    ("Breusch-Godfrey", 3.0, 0.55, "pasa", ""),
    ("White", 20.0, 0.30, "pasa", ""),
    ("VIF (gdp_growth)", 1.4, np.nan, "sin alerta", ""),
])


def _limits(result, stationarity, diag=CLEAN_DIAG, fit=None, stat=None) -> pd.DataFrame:
    return limitations_table(
        result.stationarity if stat is None else stat, diag,
        result.fit if fit is None else fit, result.variants, stationarity,
    )


def test_limitations_always_include_the_fixed_items(result, stationarity):
    tab = _limits(result, stationarity)
    assert list(tab.columns) == ["limitacion", "detalle", "origen"]
    for name, detail in FIXED_LIMITATIONS:
        row = tab[tab["limitacion"] == name]
        assert len(row) == 1 and row.iloc[0]["detalle"] == detail and row.iloc[0]["origen"] == "fija"
    assert set(tab["origen"]) <= {"fija", "detectada"}


def test_limitations_list_non_i0_regressors_from_rf15(result, stationarity):
    row = _limits(result, stationarity).query("limitacion == 'Regresores no I(0)'").iloc[0]
    assert row["origen"] == "detectada"
    assert "π" in row["detalle"] and "CRED(t−4)" in row["detalle"]
    assert "ΔU" not in row["detalle"] and "PIB" not in row["detalle"]


def test_limitations_say_none_when_no_regressor_is_non_i0(result, stationarity):
    stat = result.stationarity.copy()
    stat["no_i0"] = "no"
    tab = _limits(result, stationarity, stat=stat)
    assert tab[tab["limitacion"] == "Regresores no I(0)"].iloc[0]["detalle"] == "ninguno"


def test_limitations_list_possible_i2_dependents_by_variant(result, stationarity):
    tab = _limits(result, stationarity)
    detail = tab[tab["limitacion"] == "Dependientes con orden «posible I(2)»"].iloc[0]["detalle"]
    assert "dralacbs_logit (R5)" in detail and "drsreacbs (R3_drsreacbs)" in detail
    assert "drclacbs" not in detail and "dralacbn" not in detail  # son I(1)


def test_limitations_add_each_failed_diagnostic_and_alert_but_not_passes(result, stationarity):
    diag = _diag([
        ("Breusch-Godfrey", 12.0, 0.017, "falla", ""),
        ("White", 20.0, 0.30, "pasa", ""),
        ("VIF (gdp_growth)", 14.2, np.nan, "alerta", ""),
        ("VIF (d_unemp)", 1.3, np.nan, "sin alerta", ""),
        ("CUSUM", np.nan, np.nan, "falla", "los trimestres con dummy de impulso no aportan residuo recursivo"),
    ])
    det = _limits(result, stationarity, diag=diag).query("origen == 'detectada'")
    names = " | ".join(det["limitacion"])
    assert "Breusch-Godfrey" in names and "VIF (gdp_growth)" in names and "CUSUM" in names
    assert "White" not in names and "VIF (d_unemp)" not in names
    bg = det[det["limitacion"].str.contains("Breusch-Godfrey")].iloc[0]["detalle"]
    assert "0,017" in bg and "inconsistente" in bg
    assert "no se elimina" in det[det["limitacion"].str.contains("VIF")].iloc[0]["detalle"]


def test_limitations_report_not_estimated_variants(result, stationarity):
    tab = _limits(result, stationarity)
    row = tab[tab["limitacion"].str.contains("R8")].iloc[0]
    assert row["origen"] == "detectada" and "sin historia anterior a 2000T1" in row["detalle"]


def test_limitations_report_spectral_truncation_but_not_the_impulse_rank_reduction(result, stationarity):
    base = _limits(result, stationarity)
    assert not base["limitacion"].str.contains("runcamiento").any()
    assert not base["limitacion"].str.contains("rango", case=False).any()
    assert not base["detalle"].str.contains("rango reducido").any()
    adjusted = dataclasses.replace(result.fit, psd_adjusted=True)
    tab = _limits(result, stationarity, fit=adjusted)
    row = tab[tab["limitacion"].str.contains("runcamiento")].iloc[0]
    assert row["origen"] == "detectada" and "principal" in row["detalle"]


def test_limitations_use_association_language(result, stationarity):
    tab = _limits(result, stationarity)
    text = " ".join(tab["limitacion"] + " " + tab["detalle"]).lower()
    for banned in ["causa", "causal", "provoca", "debido a"]:
        assert banned not in text


# --- Tabla de desviaciones (RF-21) ---


def test_deviations_table_has_the_fixed_decisions_and_the_preregistration_changes(result):
    tab = deviations_table(result.variants, END)
    assert list(tab.columns) == ["decision", "referencia", "motivo"]
    text = "\n".join(tab["decision"])
    assert "GDPC1" in text and "GDP nominal" in text
    assert "forma fija" in text
    assert "ΔFFR como variable única" in text and "3.3 y 3.4" in text
    pre = tab[tab["referencia"] == "Pre-registro de la spec 003"]
    assert len(pre) == len(PREREG_DEVIATIONS) == 3
    for (fecha, cambio, _), (_, row) in zip(PREREG_DEVIATIONS, pre.iterrows()):
        assert row["decision"] == f"{fecha} · {cambio}"
    assert any(d.startswith("2026-10-05 · C1") for d in pre["decision"])


def test_deviations_table_states_the_sample_end_from_the_data(result):
    tab = deviations_table(result.variants, END)
    row = tab[tab["decision"].str.startswith("Muestra hasta")].iloc[0]
    assert "2026T2" in row["decision"] and "2026-01-01" in row["motivo"]
    other = deviations_table(result.variants, Q("2026Q1"))
    assert "2026T1" in other[other["decision"].str.startswith("Muestra hasta")].iloc[0]["decision"]


def test_deviations_table_reports_r8_status_not_estimated(result):
    tab = deviations_table(result.variants, END)
    row = tab[tab["decision"].str.startswith("Muestra larga")].iloc[0]
    assert "1985T1" in row["decision"] and "2000–2026" in row["decision"]
    assert "no estimada" in row["motivo"] and "sin historia anterior a 2000T1" in row["motivo"]


def test_deviations_table_reports_r8_status_estimated(full_long, stationarity):
    res = run_model1(full_long, stationarity, END)
    tab = deviations_table(res.variants, END)
    row = tab[tab["decision"].str.startswith("Muestra larga")].iloc[0]
    assert "estimada" in row["motivo"] and "no estimada" not in row["motivo"]
    assert "1985T1" in row["motivo"]  # inicio efectivo


# --- Exportación para la spec 005 (RF-8) ---


def test_stress_export_has_the_documented_keys_in_order(result):
    e = stress_export(result.fit)
    assert list(e) == [
        "spec", "dependent", "form", "terms", "columns", "credit_lag", "params", "cov_hac",
        "psd_adjusted", "sample_start", "sample_end", "nobs", "hac_lags", "covid_quarters",
    ]
    assert e["spec"] == "003-modelo-i" and e["dependent"] == "dralacbs"
    assert e["form"] == "primera diferencia"
    assert e["credit_lag"] == 4
    assert e["columns"] == dict(MACRO_TERMS)
    assert e["sample_start"] == "2000T1" and e["sample_end"] == "2026T2"
    assert e["nobs"] == 106 and e["hac_lags"] == 4 and e["psd_adjusted"] is False
    assert e["covid_quarters"] == ["2020T2", "2020T3", "2020T4", "2021T1"]


def test_stress_export_params_and_covariance_match_the_fit(result):
    e = stress_export(result.fit)
    assert e["terms"] == list(result.fit.params.index) and len(e["terms"]) == 11
    np.testing.assert_array_equal(e["params"], result.fit.params.to_numpy())
    cov = np.array(e["cov_hac"])
    assert cov.shape == (11, 11)
    np.testing.assert_array_equal(cov, result.fit.cov.to_numpy())
    np.testing.assert_allclose(cov, cov.T, atol=1e-18)


def test_stress_export_json_is_deterministic_and_roundtrips_exactly(result):
    e = stress_export(result.fit)
    s1, s2 = stress_export_json(e), stress_export_json(stress_export(result.fit))
    assert s1 == s2
    back = json.loads(s1)
    assert back == e  # los floats vuelven idénticos (repr de precisión completa)
    assert list(back) == list(e)  # orden de claves conservado
    assert "NaN" not in s1 and "Infinity" not in s1
    assert "\\u" not in s1  # ensure_ascii=False


def test_run_model1_exposes_the_export_for_spec_005(result):
    assert result.stress == stress_export(result.fit)


# --- Salida en Markdown y CSV (RF-23): texto puro; la escritura a disco es de la tarea 9 ---

EXPECTED_STEMS = [
    "model1_coefficients", "model1_effects", "model1_diagnostics", "model1_stationarity",
    "model1_robustness_estimates", "model1_robustness_summary", "model1_oos",
    "model1_limitations", "model1_deviations",
]


def test_render_returns_markdown_and_csv_for_every_table_available(result):
    out = render_model1_tables(result)
    assert list(out) == EXPECTED_STEMS
    for stem, d in out.items():
        assert set(d) == {"md", "csv"}, stem
        md_lines = d["md"].splitlines()
        assert md_lines[0].startswith("| ") and set(md_lines[1].replace("|", "").split()) == {"---"}, stem
        lines = d["csv"].split("\n")
        assert lines[-1] == "" and "\r" not in d["csv"], stem  # terminador \n, sin \r
        assert len(lines) > 2


def test_render_is_deterministic(result):
    assert render_model1_tables(result) == render_model1_tables(result)


def test_render_formats_markdown_with_decimal_comma_and_csv_with_full_precision(result):
    out = render_model1_tables(result)
    md = out["model1_coefficients"]["md"]
    assert "< 0,001" in md  # p-valores muy pequeños (regresores fuertes del DGP)
    assert "106" in md and "106,0" not in md  # enteros sin decimales
    assert "nan" not in md.lower()
    csv = out["model1_coefficients"]["csv"]
    assert csv.splitlines()[0].startswith("termino,etiqueta,coef")
    assert re.search(r"\d\.\d{8,}", csv)  # punto decimal y precisión completa


def test_coefficient_markdown_closes_with_the_footnote(result):
    md = render_model1_tables(result)["model1_coefficients"]["md"]
    note = coefficient_note(result.coef_footer)
    assert md.rstrip().endswith(note) and note.startswith("Nota:")
    for needle in ["primera diferencia", "2000T1–2026T2", "n = 106", "parámetros = 11",
                   "4 rezagos", "truncamiento espectral: no",
                   "rango reducido por dummies de impulso (esperado)"]:
        assert needle in note, needle


def test_rendered_tables_use_association_language(result):
    out = render_model1_tables(result)
    text = " ".join(d["md"] + d["csv"] for d in out.values()).lower()
    for banned in ["causa", "causal", "provoca", "debido a"]:
        assert banned not in text, banned


# =====================================================================================
# Tarea 7: validación fuera de muestra (RF-18) y nota del Chow en las limitaciones (RF-20)
# =====================================================================================


@pytest.fixture(scope="module")
def oos(full, decisions) -> OOSResult:
    return out_of_sample(full, decisions, END)


def test_oos_partition_trains_2000q1_2019q4_and_evaluates_2022q1_2026q2(oos):
    X = oos.train_design.X
    assert X.index[0] == Q("2000Q1") and X.index[-1] == Q("2019Q4") and len(X) == 80
    assert not any(c.startswith("covid_") for c in X.columns)  # no hay trimestres COVID
    assert list(oos.series.index) == list(pd.period_range("2022Q1", "2026Q2", freq="Q-DEC"))
    assert len(oos.series) == 18
    for q in pd.period_range("2020Q1", "2021Q4", freq="Q-DEC"):  # el hueco COVID no se usa
        assert q not in X.index and q not in oos.series.index


def test_oos_trained_params_are_the_ols_hac_fit_on_the_training_window(oos, full, decisions, result):
    spec = dataclasses.replace(MAIN, id="oos", covid_dummies=False)
    ref = fit_ols_hac(build_design(full, spec, decisions["dralacbs"], Q("2019Q4")))
    np.testing.assert_allclose(oos.train_fit.params, ref.params, rtol=1e-12)
    assert list(oos.train_fit.params.index) == ["const", "y_lag", *MACRO_TERMS]
    assert oos.train_fit.params["const"] != pytest.approx(result.fit.params["const"], rel=1e-6)


def test_oos_series_has_observed_forecasts_and_both_naive_benchmarks(oos):
    assert list(oos.series.columns) == [
        "observado", "un_paso", "dinamico", "ingenuo_un_paso", "ingenuo_dinamico"
    ]
    assert not oos.series.isna().any().any()


def test_oos_one_step_level_is_previous_observed_level_plus_forecast_delta(oos, full):
    X = oos.test_design.X
    pred = X[list(oos.train_fit.params.index)].to_numpy() @ oos.train_fit.params.to_numpy()
    expected = full["dralacbs"].shift(1).loc[X.index].to_numpy() + pred
    np.testing.assert_allclose(oos.series["un_paso"], expected, rtol=1e-12)
    np.testing.assert_allclose(oos.series["observado"], full["dralacbs"].loc[X.index])


def test_oos_dynamic_chains_the_forecast_delta_from_the_2021q4_anchor(oos, full):
    params, X = oos.train_fit.params, oos.test_design.X
    y_prev = float(full["dralacbs"].diff().loc[Q("2021Q4")])
    deltas = []
    for t in X.index:
        row = X.loc[t, params.index].copy()
        row["y_lag"] = y_prev
        y_prev = float(row.to_numpy() @ params.to_numpy())
        deltas.append(y_prev)
    expected = float(full["dralacbs"].loc[Q("2021Q4")]) + np.cumsum(deltas)
    np.testing.assert_allclose(oos.series["dinamico"], expected, rtol=1e-12)


def test_oos_anchor_is_the_observed_delta_not_the_level(oos, full):
    delta = float(full["dralacbs"].diff().loc[Q("2021Q4")])
    level = float(full["dralacbs"].loc[Q("2021Q4")])
    assert oos.anchor_period == Q("2021Q4")
    assert oos.anchor_value == pytest.approx(delta, rel=1e-12)
    assert abs(oos.anchor_value - level) > 1.0
    assert oos.test_design.X["y_lag"].iloc[0] == pytest.approx(delta)  # y_lag(2022T1) = Y(2021T4)


def test_oos_naive_benchmarks_are_the_random_walk_in_both_modes(oos, full):
    lvl, idx = full["dralacbs"], oos.series.index
    np.testing.assert_allclose(oos.series["ingenuo_un_paso"], lvl.shift(1).loc[idx])
    np.testing.assert_allclose(oos.series["ingenuo_dinamico"], np.full(18, lvl.loc[Q("2021Q4")]))


def test_oos_table_has_one_row_per_forecast_type_with_the_rf18_columns(oos):
    t = oos.table
    assert list(t["pronostico"]) == ["a un paso", "dinámico"]
    for col in ["n_trimestres", "rmse_modelo", "rmse_ingenuo", "mae_modelo", "mae_ingenuo",
                "cociente_rmse", "dm_estadistico", "dm_p", "veredicto", "significancia"]:
        assert col in t.columns
    assert (t["n_trimestres"] == 18).all()


def test_oos_metrics_are_rmse_mae_and_ratio_of_level_errors_in_pp(oos):
    s, t = oos.series, oos.table.set_index("pronostico")
    for name, fc, nv in [("a un paso", "un_paso", "ingenuo_un_paso"),
                         ("dinámico", "dinamico", "ingenuo_dinamico")]:
        em, en = s["observado"] - s[fc], s["observado"] - s[nv]
        assert t.loc[name, "rmse_modelo"] == pytest.approx(np.sqrt(np.mean(em**2)), rel=1e-12)
        assert t.loc[name, "rmse_ingenuo"] == pytest.approx(np.sqrt(np.mean(en**2)), rel=1e-12)
        assert t.loc[name, "mae_modelo"] == pytest.approx(np.mean(np.abs(em)), rel=1e-12)
        assert t.loc[name, "mae_ingenuo"] == pytest.approx(np.mean(np.abs(en)), rel=1e-12)
        assert t.loc[name, "cociente_rmse"] == pytest.approx(
            t.loc[name, "rmse_modelo"] / t.loc[name, "rmse_ingenuo"], rel=1e-12
        )


def test_oos_diebold_mariano_hln_only_for_the_one_step_forecast(oos):
    s, t = oos.series, oos.table.set_index("pronostico")
    ref = diebold_mariano_hln(s["observado"] - s["un_paso"], s["observado"] - s["ingenuo_un_paso"])
    assert ref["n"] == 18
    assert t.loc["a un paso", "dm_estadistico"] == pytest.approx(ref["stat"], rel=1e-12)
    assert t.loc["a un paso", "dm_p"] == pytest.approx(ref["p"], rel=1e-12)
    assert np.isnan(t.loc["dinámico", "dm_estadistico"]) and np.isnan(t.loc["dinámico", "dm_p"])
    assert oos.dm == ref


def test_oos_verdicts_are_the_preregistered_ones(oos):
    t = oos.table.set_index("pronostico")
    v = oos_verdicts(t.loc["a un paso", "cociente_rmse"], t.loc["dinámico", "cociente_rmse"],
                     t.loc["a un paso", "dm_p"])
    assert t.loc["a un paso", "veredicto"] == v["veredicto_un_paso"]
    assert t.loc["dinámico", "veredicto"] == v["veredicto_dinamico"]
    assert t.loc["a un paso", "significancia"] == v["significancia_un_paso"]
    assert t.loc["dinámico", "significancia"] == "no aplica"  # DM mezcla horizontes: solo a un paso
    assert oos.verdicts == v


def test_oos_model_beats_the_random_walk_in_a_strong_synthetic_dgp(oos):
    t = oos.table.set_index("pronostico")
    assert oos.train_fit.rsquared < 0.999  # guarda contra ajuste degenerado
    assert t.loc["a un paso", "cociente_rmse"] < 1.0
    assert t.loc["dinámico", "cociente_rmse"] < 1.0
    assert t.loc["a un paso", "veredicto"] == "supera al ingenuo"
    assert t.loc["dinámico", "veredicto"] == "supera al ingenuo"


def test_oos_is_deterministic(full, decisions, oos):
    again = out_of_sample(full, decisions, END)
    pd.testing.assert_frame_equal(oos.table, again.table)
    pd.testing.assert_frame_equal(oos.series, again.series)


def test_oos_with_a_level_dependent_forecasts_levels_directly(full, decisions):
    res = out_of_sample(full, {**decisions, "dralacbs": "niveles"}, END)
    assert res.form == "nivel"
    X, params = res.test_design.X, res.train_fit.params
    pred = X[list(params.index)].to_numpy() @ params.to_numpy()
    np.testing.assert_allclose(res.series["un_paso"], pred, rtol=1e-12)
    assert res.anchor_value == pytest.approx(float(full["dralacbs"].loc[Q("2021Q4")]), rel=1e-12)


def test_oos_training_without_degrees_of_freedom_stops(full, decisions, monkeypatch):
    """RF-6: la validación fuera de muestra se detiene (no se reporta «no estimada»)."""
    monkeypatch.setattr(model1, "check_dof", lambda design: "grados de libertad insuficientes (< 30)")
    with pytest.raises(ModelDataError, match="fuera de muestra.*grados de libertad"):
        out_of_sample(full, decisions, END)


def test_oos_missing_term_in_the_evaluation_window_stops_with_variable_and_quarter(full, decisions):
    holey = full.copy()
    holey.loc[Q("2023Q2"), "unrate_d"] = np.nan
    with pytest.raises(ModelDataError, match=r"unrate_d.*2023Q2"):
        out_of_sample(holey, decisions, END)


def test_oos_stops_if_the_common_quarter_is_before_the_evaluation_start(full, decisions):
    with pytest.raises(ModelDataError, match="2022T1"):
        out_of_sample(full, decisions, Q("2021Q4"))


def test_oos_stops_if_history_ends_before_the_common_quarter(full, decisions):
    with pytest.raises(ModelDataError):
        out_of_sample(full, decisions, Q("2026Q3"))


def test_oos_is_part_of_run_model1_and_rendered_as_markdown_and_csv(result):
    assert isinstance(result.oos, OOSResult)
    out = render_model1_tables(result)["model1_oos"]
    assert "a un paso" in out["md"] and "dinámico" in out["md"]
    assert "no aplica" in out["md"]
    assert out["csv"].splitlines()[0].startswith("pronostico,n_trimestres,rmse_modelo")
    assert "nan" not in out["md"].lower()


# --- Nota de muestra finita del Chow en las limitaciones (decisión: se reporta tal cual) ---


def test_limitations_note_the_finite_sample_oversize_of_a_failed_chow_wald(result, stationarity):
    diag = _diag([
        ("Chow 2008Q3", 15.4, 0.031, "falla", "Wald HAC con interacciones"),
        ("Breusch-Godfrey", 12.0, 0.017, "falla", ""),
    ])
    det = _limits(result, stationarity, diag=diag).query("origen == 'detectada'")
    chow = det[det["limitacion"].str.startswith("Chow 2008Q3")].iloc[0]["detalle"]
    assert "0,031" in chow
    assert "sobredimensionado en muestra finita" in chow and "CUSUM" in chow
    bg = det[det["limitacion"].str.startswith("Breusch-Godfrey")].iloc[0]["detalle"]
    assert "sobredimensionado" not in bg  # la nota es solo del Chow


def test_limitations_do_not_mention_the_chow_oversize_when_it_does_not_fail(result, stationarity):
    tab = _limits(result, stationarity)
    assert not tab["detalle"].str.contains("sobredimensionado").any()


def test_limitations_write_tiny_p_values_as_less_than_0001_not_as_zero(result, stationarity):
    diag = _diag([("White", 91.8, 0.0000004, "falla", ""), ("Breusch-Pagan", 22.0, 0.015, "falla", "")])
    det = _limits(result, stationarity, diag=diag).query("origen == 'detectada'")
    white = det[det["limitacion"].str.startswith("White")].iloc[0]["detalle"]
    assert "p < 0,001" in white and "0,000" not in white
    assert "p = 0,015" in det[det["limitacion"].str.startswith("Breusch-Pagan")].iloc[0]["detalle"]
