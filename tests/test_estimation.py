"""Tests para src/estimation.py (spec 003, tarea 2).

Cubre RF-6, RF-7, RF-10, RNF-2 y RNF-3 según plan §7.
Datos sintéticos con parámetros conocidos; semilla fija; sin red ni disco.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm
from scipy.stats import chi2, norm

from src.design import Design
from src.estimation import (
    Fit,
    check_dof,
    fit_ols_hac,
    hac_lags,
    inference,
    long_run,
    psd_truncate,
    scale_effect,
    standardization_sd,
    wald,
)
from src.model1_config import COVID_QUARTERS, PSD_REL_TOL, SEED

# --- Helpers ---


def _design_from_arrays(y: np.ndarray, X: pd.DataFrame) -> Design:
    """Construye un Design sintético con índice numérico."""
    return Design(
        y=pd.Series(np.asarray(y, dtype=float), name="y"),
        X=X,
        form="primera diferencia",
        start=pd.Period("2000Q1", "Q-DEC"),
        end=pd.Period("2049Q4", "Q-DEC"),
        spec_id="test",
    )


def _ar1(rng: np.random.Generator, n: int, rho: float) -> np.ndarray:
    """Simula un proceso AR(1) con coeficiente rho y innovaciones N(0,1)."""
    e = rng.normal(0.0, 1.0, n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + e[t]
    return x


# --- Test 1: DGP dinámico, recupera coeficientes (RNF-2) ---


def test_fit_ols_hac_recovers_coefficients_dynamic_dgp():
    rng = np.random.default_rng(SEED)
    n = 2000
    e = rng.normal(0.0, 1.0, n)
    x1 = rng.normal(0.0, 1.0, n)
    x2 = rng.normal(0.0, 1.0, n)
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = 0.5 + 0.6 * y[t - 1] + 1.0 * x1[t] - 0.5 * x2[t] + e[t]
    burn = 200
    y_dep = y[burn:]
    X = pd.DataFrame(
        {
            "const": 1.0,
            "y_lag": y[burn - 1 : -1],
            "x1": x1[burn:],
            "x2": x2[burn:],
        }
    )
    design = _design_from_arrays(y_dep, X)
    fit = fit_ols_hac(design)
    assert isinstance(fit, Fit)
    assert fit.params["const"] == pytest.approx(0.5, abs=0.05)
    assert fit.params["y_lag"] == pytest.approx(0.6, abs=0.05)
    assert fit.params["x1"] == pytest.approx(1.0, abs=0.05)
    assert fit.params["x2"] == pytest.approx(-0.5, abs=0.05)
    assert fit.nobs == n - burn
    assert fit.k == 4


# --- Test 2: EE HAC > EE clásico con errores AR(1) (RNF-2) ---


def test_hac_se_larger_than_classical_with_ar1_errors():
    rng = np.random.default_rng(SEED)
    n = 500
    x = _ar1(rng, n, 0.8)
    e = _ar1(rng, n, 0.7)
    y = 1.0 + 2.0 * x + e
    X = pd.DataFrame({"const": 1.0, "x": x})
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    classical = sm.OLS(y, X).fit()
    hac_se = float(np.sqrt(fit.cov.loc["x", "x"]))
    classical_se = float(classical.bse["x"])
    assert hac_se > classical_se


# --- Test 3: ventana HAC ---


def test_hac_lags():
    assert hac_lags(106) == 4
    assert hac_lags(1) >= 1


# --- Test 4: truncamiento espectral ---


def test_psd_truncate_positive_definite_unchanged():
    V = np.array([[2.0, 0.5], [0.5, 1.0]])
    V_out, adjusted = psd_truncate(V)
    assert not adjusted
    np.testing.assert_allclose(V_out, V)


def test_psd_truncate_negative_eigenvalue_raised():
    V = np.array([[1.0, 0.0], [0.0, -1e-3]])
    V_out, adjusted = psd_truncate(V)
    assert adjusted
    eigvals = np.linalg.eigvalsh(V_out)
    floor = PSD_REL_TOL * 1.0  # max|eig| = 1.0
    assert np.all(eigvals >= floor)


# --- Test 5: inference con valores conocidos ---


def test_inference_known_values():
    params = pd.Series({"a": 1.0, "b": -2.0})
    cov = pd.DataFrame({"a": [4.0, 0.0], "b": [0.0, 1.0]}, index=["a", "b"])
    result = inference(params, cov)
    assert list(result.columns) == ["coef", "se", "z", "p", "ic_inf", "ic_sup"]
    assert result.loc["a", "coef"] == pytest.approx(1.0)
    assert result.loc["a", "se"] == pytest.approx(2.0)
    assert result.loc["a", "z"] == pytest.approx(0.5)
    assert result.loc["a", "p"] == pytest.approx(2 * (1 - norm.cdf(0.5)))
    assert result.loc["a", "ic_inf"] == pytest.approx(1.0 - 1.959964 * 2.0)
    assert result.loc["a", "ic_sup"] == pytest.approx(1.0 + 1.959964 * 2.0)
    assert result.loc["b", "se"] == pytest.approx(1.0)
    assert result.loc["b", "z"] == pytest.approx(-2.0)
    assert result.loc["b", "p"] == pytest.approx(2 * (1 - norm.cdf(2.0)))
    assert result.loc["b", "ic_inf"] == pytest.approx(-2.0 - 1.959964)
    assert result.loc["b", "ic_sup"] == pytest.approx(-2.0 + 1.959964)


# --- Test 6: Wald coincide con t² para una restricción ---


def test_wald_equals_t_squared():
    params = pd.Series({"a": 2.0, "b": 1.0})
    cov = pd.DataFrame({"a": [4.0, 0.0], "b": [0.0, 1.0]}, index=["a", "b"])
    R = np.array([[1.0, 0.0]])  # H0: a = 0
    result = wald(params, cov, R)
    # t = 2/2 = 1, t^2 = 1
    assert result["stat"] == pytest.approx(1.0)
    assert result["df"] == 1
    assert result["p"] == pytest.approx(1 - chi2.cdf(1.0, 1))


# --- Test 7: largo plazo con fórmula cerrada ---


def test_long_run_closed_form():
    params = pd.Series({"y_lag": 0.5, "x": 0.2})
    cov = pd.DataFrame({"x": [0.01, 0.0], "y_lag": [0.0, 0.04]}, index=["x", "y_lag"])
    result = long_run(params, cov, "x")
    assert result["reported"] is True
    # estimate = 0.2 / (1 - 0.5) = 0.4
    assert result["estimate"] == pytest.approx(0.4)
    # grad = [1/(1-0.5), 0.2/(1-0.5)^2] = [2, 0.8]
    # se = sqrt(4*0.01 + 0.64*0.04) = sqrt(0.0656)
    expected_se = float(np.sqrt(4 * 0.01 + 0.64 * 0.04))
    assert result["se"] == pytest.approx(expected_se)
    assert result["z"] == pytest.approx(0.4 / expected_se)
    assert result["p"] == pytest.approx(2 * (1 - norm.cdf(0.4 / expected_se)))
    assert result["ic_inf"] == pytest.approx(0.4 - 1.959964 * expected_se)
    assert result["ic_sup"] == pytest.approx(0.4 + 1.959964 * expected_se)


def test_long_run_not_reported_high_rho():
    params = pd.Series({"y_lag": 0.96, "x": 0.2})
    cov = pd.DataFrame({"x": [0.01, 0.0], "y_lag": [0.0, 0.04]}, index=["x", "y_lag"])
    result = long_run(params, cov, "x")
    assert result["reported"] is False
    assert "1 - rho" in result["reason"]


# --- Test 8: scale_effect ---


def test_scale_effect_zero_factor():
    effect = {"reported": True, "estimate": 0.4, "se": 0.1, "ic_inf": 0.2, "ic_sup": 0.6}
    result = scale_effect(effect, 0.0)
    assert result["reported"] is False
    assert "no definido" in result["reason"]


def test_scale_effect_scales_values():
    effect = {"reported": True, "estimate": 0.4, "se": 0.1, "ic_inf": 0.2, "ic_sup": 0.6}
    result = scale_effect(effect, 2.0)
    assert result["reported"] is True
    assert result["estimate"] == pytest.approx(0.8)
    assert result["se"] == pytest.approx(0.2)
    assert result["ic_inf"] == pytest.approx(0.4)
    assert result["ic_sup"] == pytest.approx(1.2)


# --- Test 9: check_dof ---


def test_check_dof_insufficient():
    n, k = 35, 10  # n - k = 25 < 30
    X = pd.DataFrame({f"x{i}": np.ones(n) for i in range(k - 1)})
    X.insert(0, "const", 1.0)
    design = _design_from_arrays(np.zeros(n), X)
    assert check_dof(design) == "grados de libertad insuficientes (< 30)"


def test_check_dof_rank_deficient():
    n = 100
    X = pd.DataFrame({"const": 1.0, "a": np.ones(n), "b": np.ones(n)})  # b = a
    design = _design_from_arrays(np.zeros(n), X)
    assert check_dof(design) == "matriz de regresores de rango incompleto"


def test_check_dof_ok():
    rng = np.random.default_rng(SEED)
    n = 100
    X = pd.DataFrame(
        {"const": 1.0, "a": rng.normal(0, 1, n), "b": rng.normal(0, 1, n)}
    )
    design = _design_from_arrays(rng.normal(0, 1, n), X)
    assert check_dof(design) is None


# --- Test 10: standardization_sd excluye 2020T2–2021T1 (C1) ---


def test_standardization_sd_excludes_covid():
    rng = np.random.default_rng(SEED)
    n = 106
    idx = pd.period_range("2000Q1", periods=n, freq="Q-DEC")
    X = pd.DataFrame(
        {
            "const": 1.0,
            "y_lag": rng.normal(0, 1, n),
            "gdp_growth": rng.normal(2, 1, n),
            "d_unemp": rng.normal(0, 0.5, n),
        },
        index=idx,
    )
    y = pd.Series(rng.normal(0, 1, n), index=idx)
    design = Design(
        y=y,
        X=X,
        form="primera diferencia",
        start=idx[0],
        end=idx[-1],
        spec_id="test",
    )
    sds = standardization_sd(design)
    covid = [pd.Period(q, "Q-DEC") for q in COVID_QUARTERS]
    mask = ~X.index.isin(covid)
    assert sds["gdp_growth"] == pytest.approx(X.loc[mask, "gdp_growth"].std(ddof=1))
    assert sds["d_unemp"] == pytest.approx(X.loc[mask, "d_unemp"].std(ddof=1))


# --- Ampliaciones de la spec 004 (D1 y D2 del plan): retrocompatibles ---


def _simple_design(n: int = 120, seed: int = 11, with_unit_sum_column: bool = False) -> Design:
    rng = np.random.default_rng(seed)
    X = pd.DataFrame({"const": 1.0, "x": rng.normal(size=n)})
    if with_unit_sum_column:
        w = np.zeros(n)
        w[10], w[11] = 0.3, 0.7                        # suma exactamente 1, pero no es 0/1
        X["w"] = w
    y = 0.5 + 0.8 * X["x"].to_numpy() + np.random.default_rng(seed + 1).normal(size=n)
    return _design_from_arrays(y, X)


def test_fit_ols_hac_maxlags_overrides_the_window():
    d = _simple_design()
    assert fit_ols_hac(d, maxlags=7).hac_lags == 7
    assert fit_ols_hac(d, maxlags=1).hac_lags == 1
    assert not np.allclose(fit_ols_hac(d, maxlags=7).cov.to_numpy(), fit_ols_hac(d, maxlags=1).cov.to_numpy())


def test_fit_ols_hac_default_window_unchanged():
    d = _simple_design()
    a, b = fit_ols_hac(d), fit_ols_hac(d, maxlags=None)
    assert a.hac_lags == b.hac_lags == hac_lags(120)
    assert a.params.equals(b.params) and a.cov.equals(b.cov)
    assert fit_ols_hac(d, maxlags=hac_lags(120)).cov.equals(a.cov)


def test_impulse_detection_ignores_a_continuous_column_that_sums_to_one():
    from src.estimation import _impulse_dummy_cols

    d = _simple_design(with_unit_sum_column=True)
    assert _impulse_dummy_cols(d.X) == []
    X = d.X.copy()
    X["imp"] = 0.0
    X.iloc[5, X.columns.get_loc("imp")] = 1.0
    assert _impulse_dummy_cols(X) == ["imp"]
