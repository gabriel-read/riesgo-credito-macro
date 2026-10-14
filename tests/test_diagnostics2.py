"""Tests de los diagnósticos con la dimensión del Modelo II (spec 004, tarea 4).

Cubre RF-19, RF-20 y RNF-6 con los procesos D y F del plan §7.1 (tolerancias declaradas, no se
relajan) y la regla C1 de White. Datos sintéticos; sin red ni disco y sin datos reales.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

import src.diagnostics as diag
from src.design import Design
from src.design2 import build_columns, build_design2, common_window
from src.diagnostics import (
    _white_aux_matrix,
    breusch_godfrey,
    breusch_pagan,
    chow_wald,
    cusum,
    jarque_bera_test,
    reset,
    vif,
    white,
)
from src.estimation import fit_ols_hac
from src.model2_config import COVID_NAMES, EXPECTED_FORM, MAIN2, SEED2
from tests.synthetic_model2 import make_full2

DEC = EXPECTED_FORM
P = lambda s: pd.Period(s, "Q-DEC")  # noqa: E731


def _fit2(K: int, **kw):
    full = make_full2(**kw)
    end = full.index[-1]
    window = common_window(build_columns(full, DEC), end)
    return fit_ols_hac(build_design2(full, MAIN2, K, DEC, window, end))


def _quarterly_design(y: np.ndarray, X: pd.DataFrame) -> Design:
    n = len(y)
    idx = pd.period_range("1998Q1", periods=n, freq="Q-DEC")
    X = X.copy()
    X.index = idx
    return Design(y=pd.Series(y, index=idx), X=X, form="primera diferencia", start=idx[0],
                  end=idx[-1], spec_id="sim", dropped=[])


# --- Proceso D: el error HAC supera al clásico con autocorrelación (RNF-3, T1) ---


def test_process_d_hac_exceeds_classical_with_autocorrelation():
    n = 500
    rx, re = np.random.default_rng(SEED2), np.random.default_rng(SEED2 + 1)
    x = np.zeros(n)
    e = np.zeros(n)
    ux, ue = rx.normal(size=n), re.normal(size=n)
    for t in range(1, n):
        x[t] = 0.8 * x[t - 1] + ux[t]
        e[t] = 0.7 * e[t - 1] + ue[t]
    X = pd.DataFrame({"const": 1.0, "d_ffr_l0": x})
    y = 0.1 + 0.3 * x + e
    design = _quarterly_design(y, X)
    hac = fit_ols_hac(design)
    classical = sm.OLS(design.y, design.X).fit().bse["d_ffr_l0"]
    assert np.sqrt(hac.cov.loc["d_ffr_l0", "d_ffr_l0"]) > classical


# --- Proceso F: Breusch-Godfrey ---


def test_bg_rejects_ar1_errors_and_not_iid():
    assert breusch_godfrey(_fit2(3, n=200, err_ar=0.7))["p"] < 0.05
    assert breusch_godfrey(_fit2(3, n=200))["p"] >= 0.05


# --- Proceso F: Chow con quiebre en la pendiente de ΔFFR(t) ---


def _break_design(slope_after: float, seed: int = SEED2, n: int = 300) -> Design:
    rx, re = np.random.default_rng(seed), np.random.default_rng(seed + 1)
    d0 = rx.normal(0.0, 0.5, n)
    d1 = rx.normal(0.0, 0.5, n)
    z = rx.normal(size=n)
    slope = np.where(np.arange(n) >= n // 2, slope_after, 0.2)
    y = 0.02 + slope * d0 + 0.1 * d1 + 0.05 * z + re.normal(0.0, 0.3, n)
    return _quarterly_design(y, pd.DataFrame({"const": 1.0, "d_ffr_l0": d0, "d_ffr_l1": d1, "z": z}))


def test_chow_rejects_with_slope_break_and_not_without():
    brk = str(_break_design(0.2).X.index[150])
    broken = chow_wald(fit_ols_hac(_break_design(1.0)), brk)
    stable = chow_wald(fit_ols_hac(_break_design(0.2)), brk)
    assert broken["p"] < 0.05 and broken["veredicto"] == "falla"
    assert stable["p"] >= 0.05 and stable["veredicto"] == "pasa"


# --- Dimensión del Modelo II (n = 105) ---


@pytest.fixture(scope="module")
def fit_k8():
    return _fit2(8)


def test_model2_dimension_is_105_obs_and_k_plus_11_params(fit_k8):
    assert fit_k8.nobs == 105 and fit_k8.k == 8 + 11 and fit_k8.hac_lags == 4


def test_white_not_calculable_at_model2_dimension(fit_k8):
    w = white(fit_k8)
    assert w["calculable"] is False and w["veredicto"] is None
    assert w["stat"] is None and w["p"] is None
    assert "105" in w["motivo"] and "< 30" in w["motivo"] and "rango" in w["motivo"]


def test_white_valid_with_k1():
    w = white(_fit2(1))
    assert w["calculable"] is True and w["veredicto"] in ("pasa", "falla")
    assert 0.0 <= w["p"] <= 1.0 and w["df"] > 0


def test_white_calculable_rule_is_n_minus_rank_at_least_30():
    for K in (1, 3, 4, 6, 8):
        fit = _fit2(K)
        rank = _white_aux_matrix(fit.design.X).shape[1]
        expected = fit.nobs - rank >= 30
        assert white(fit)["calculable"] is expected, K
        if expected:
            assert white(fit)["df"] == rank - 1


def test_white_rank_elimination_at_k8_design_does_not_fail(fit_k8):
    Z = _white_aux_matrix(fit_k8.design.X)               # antes lanzaba IndexError con K ≥ 4
    assert Z.shape[0] == 105 and Z.shape[1] <= 105
    assert np.linalg.matrix_rank(Z) == Z.shape[1]


def test_white_unchanged_when_calculable_keeps_model1_keys():
    w = white(_fit2(1))
    assert {"stat", "df", "p", "veredicto"} <= set(w)


def test_chow_k_plus_7_interactions_at_k8(fit_k8):
    for brk in ("2008Q3", "2020Q2"):
        c = chow_wald(fit_k8, brk)
        assert c["calculable"] is True and c["df"] == 8 + 7
        assert c["veredicto"] in ("pasa", "falla")


def test_chow_counts_pre_and_post_quarters_net_of_impulse_dummies(fit_k8):
    c = chow_wald(fit_k8, "2020Q2")
    assert (c["n_post"], c["n_post_util"]) == (25, 21)
    assert (c["n_pre"], c["n_pre_util"]) == (80, 80)
    c2 = chow_wald(fit_k8, "2008Q3")
    assert (c2["n_pre"], c2["n_pre_util"]) == (33, 33) and c2["n_post"] == 72
    mid = chow_wald(fit_k8, "2020Q4")                     # dos dummies caen antes del quiebre
    assert mid["n_pre"] == 82 and mid["n_pre_util"] == 80


def test_chow_rank_check_runs_before_estimating(monkeypatch):
    n = 120
    rng = np.random.default_rng(SEED2)
    idx = pd.period_range("1998Q1", periods=n, freq="Q-DEC")
    x = rng.normal(size=n)
    x[idx >= P("2015Q1")] = 0.0                            # x1 es cero tras el quiebre: post×x1 es cero
    X = pd.DataFrame({"const": 1.0, "x1": x, "x2": rng.normal(size=n)})
    y = 0.1 + 0.5 * X["x1"].to_numpy() + np.random.default_rng(SEED2 + 1).normal(size=n)
    fit = fit_ols_hac(_quarterly_design(y, X))
    calls = []
    monkeypatch.setattr(diag, "fit_ols_hac", lambda *a, **k: calls.append("fit") or (_ for _ in ()).throw(AssertionError))
    monkeypatch.setattr(diag, "wald", lambda *a, **k: calls.append("wald") or (_ for _ in ()).throw(AssertionError))
    c = chow_wald(fit, "2015Q1")
    assert calls == []
    assert c["calculable"] is False and c["veredicto"] is None and c["stat"] is None and c["p"] is None
    assert "rango" in c["motivo"] and c["df"] == 3 and "n_pre_util" in c


def test_cusum_runs_without_the_impulse_quarters(fit_k8):
    cu = cusum(fit_k8)
    covid = {P(q) for q in ("2020Q2", "2020Q3", "2020Q4", "2021Q1")}
    assert not covid & set(cu["index"])
    assert len(cu["index"]) == (105 - 4) - (8 + 7)         # 101 observaciones, 15 columnas sin dummies
    assert cu["veredicto"] in ("pasa", "falla")


def test_other_diagnostics_run_at_model2_dimension(fit_k8):
    assert breusch_pagan(fit_k8)["df"] == np.linalg.matrix_rank(fit_k8.design.X.to_numpy()) - 1
    assert jarque_bera_test(fit_k8)["df"] == 2
    r = reset(fit_k8)
    assert r["df_num"] == 2 and r["df_den"] == 105 - 19 - 2


# --- VIF con términos (RF-19) ---


def test_vif_accepts_terms_and_keeps_the_default(fit_k8):
    terms = ["y_lag", *[f"d_ffr_l{j}" for j in range(9)], "gdp_l1", "d_unemp_l1", "inflation_l1", "credit_l4"]
    v = vif(fit_k8, terms=terms)
    assert list(v["term"]) == terms and set(v.columns) == {"term", "vif", "veredicto"}
    assert not any(t in set(v["term"]) for t in COVID_NAMES) and "const" not in set(v["term"])
    assert set(v["veredicto"]) <= {"alerta", "sin alerta"}
    assert list(vif(fit_k8)["term"]) == ["y_lag"]          # sin terms: los del Modelo I presentes en X
    assert list(vif(fit_k8, terms=["gdp_l1"])["term"]) == ["gdp_l1"]
