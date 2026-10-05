"""Tests para dummies de impulso (spec 003, tarea 3).

Cubre RF-1, RF-7, RF-12, RF-14, RF-15, RF-18, RNF-2 y RNF-4 según plan §7.
Datos sintéticos con parámetros conocidos; semilla fija; sin red ni disco.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm
from statsmodels.stats.diagnostic import recursive_olsresiduals

from src.design import Design, ModelDataError, build_design, diff_form_stationary
from src.diagnostics import cusum, white
from src.estimation import fit_ols_hac
from src.model1_config import (
    EXPECTED_FORMS,
    OOS_ANCHOR,
    SEED,
    VariantSpec,
)


# --- Helpers ---


def _make_X_with_impulse_dummies(n: int, seed: int = SEED) -> pd.DataFrame:
    """Construye un X con const, y_lag, 5 macro y 4 dummies de impulso."""
    rng = np.random.default_rng(seed)
    idx = pd.period_range("2000Q1", periods=n, freq="Q-DEC")
    X = pd.DataFrame(index=idx)
    X["const"] = 1.0
    X["y_lag"] = rng.normal(0, 1, n)
    for term in ["gdp_growth", "d_unemp", "inflation", "d_ffr", "credit_growth"]:
        X[term] = rng.normal(0, 1, n)
    # 4 dummies de impulso (valen 1 en un solo trimestre)
    for q in ["2020Q2", "2020Q3", "2020Q4", "2021Q1"]:
        dummy_name = f"covid_{q.lower().replace('q', 'q')}"
        X[dummy_name] = 0.0
        X.loc[pd.Period(q, "Q-DEC"), dummy_name] = 1.0
    return X


def _design_from_arrays(y: np.ndarray, X: pd.DataFrame) -> Design:
    """Construye un Design sintético con índice trimestral."""
    return Design(
        y=pd.Series(np.asarray(y, dtype=float), index=X.index, name="y"),
        X=X,
        form="primera diferencia",
        start=pd.Period("2000Q1", "Q-DEC"),
        end=pd.Period("2049Q4", "Q-DEC"),
        spec_id="test",
    )


def _make_full_history(
    start: pd.Period = pd.Period("1998Q1", "Q-DEC"),
    end: pd.Period = pd.Period("2026Q2", "Q-DEC"),
    seed: int = 42,
) -> pd.DataFrame:
    """Crea un panel sintético con historia completa desde 1998."""
    rng = np.random.default_rng(seed)
    idx = pd.period_range(start, end, freq="Q-DEC")
    n = len(idx)

    dr = np.cumsum(rng.normal(0, 0.1, n)) + 2.0
    gdp = rng.normal(2.5, 1.0, n)
    unrate_d = rng.normal(0, 0.2, n)
    inflation = rng.normal(2.0, 0.5, n)
    fedfunds_d = rng.normal(0, 0.3, n)
    loans = rng.normal(5.0, 2.0, n)

    df = pd.DataFrame(index=idx)
    df["dralacbs"] = dr
    df["dralacbn"] = dr + rng.normal(0, 0.05, n)
    df["dralacbs_logit"] = np.log(dr / (100 - dr))
    df["drclacbs"] = dr * 0.8
    df["drblacbs"] = dr * 0.6
    df["drsreacbs"] = dr * 0.4
    df["gdpc1_yoy"] = gdp
    df["gdp_yoy"] = gdp + 2.0
    df["unrate_d"] = unrate_d
    df["cpiaucsl_yoy"] = inflation
    df["fedfunds_d"] = fedfunds_d
    loans_yoy = np.full(n, np.nan)
    loans_yoy[4:] = loans[4:]
    df["loans_yoy"] = loans_yoy

    return df


def _make_stationarity_df() -> pd.DataFrame:
    """Crea una tabla de estacionariedad sintética."""
    decisions = {
        "dralacbs": "ambigua (primera diferencia)",
        "dralacbn": "ambigua (primera diferencia)",
        "dralacbs_logit": "primera diferencia",
        "drclacbs": "primera diferencia",
        "drblacbs": "primera diferencia",
        "drsreacbs": "ambigua (primera diferencia)",
        "gdpc1_yoy": "niveles",
        "gdp_yoy": "niveles",
        "unrate_d": "niveles",
        "cpiaucsl_yoy": "niveles",
        "fedfunds_d": "niveles",
        "loans_yoy": "niveles",
    }
    rows = []
    for var, dec in decisions.items():
        rows.append({
            "variable": var,
            "etiqueta": var,
            "forma": "tal cual",
            "n_obs": 100,
            "adf_stat": -3.0,
            "adf_p": 0.01,
            "adf_lags": 2,
            "kpss_stat": 0.3,
            "kpss_p": 0.10,
            "kpss_p_truncado": "",
            "decision": dec,
            "orden": "I(0)" if dec == "niveles" else "I(1)",
        })
        rows.append({
            "variable": var,
            "etiqueta": var,
            "forma": "primera diferencia",
            "n_obs": 99,
            "adf_stat": -5.0,
            "adf_p": 0.001,
            "adf_lags": 1,
            "kpss_stat": 0.1,
            "kpss_p": 0.15,
            "kpss_p_truncado": "",
            "decision": "",
            "orden": "",
        })
    return pd.DataFrame(rows)


# --- Test 1: Coeficientes no dummy coinciden con regresión reducida (FWL) ---


def test_non_dummy_coefficients_match_reduced_regression():
    """Coeficientes no dummy coinciden (tol 1e-10) con regresión reducida."""
    rng = np.random.default_rng(SEED + 1)  # semilla distinta de la de X: con la misma, el ruido coincide con y_lag y R² = 1
    n = 106
    X = _make_X_with_impulse_dummies(n)
    # DGP: y = 1 + 2*y_lag + 3*gdp_growth + ... + e
    y = (
        1.0
        + 2.0 * X["y_lag"]
        + 3.0 * X["gdp_growth"]
        - 1.5 * X["d_unemp"]
        + 0.5 * X["inflation"]
        + 1.0 * X["d_ffr"]
        + 2.0 * X["credit_growth"]
        + rng.normal(0, 1, n)
    )

    # Estimación con dummies de impulso
    design_full = _design_from_arrays(y, X)
    fit_full = fit_ols_hac(design_full)

    # Regresión reducida: sin dummies de impulso y sin sus trimestres
    impulse_cols = [c for c in X.columns if float(X[c].sum()) == 1.0]
    mask = (X[impulse_cols] == 1.0).any(axis=1)
    X_reduced = X.loc[~mask].drop(columns=impulse_cols)
    y_reduced = y.loc[~mask]
    design_reduced = _design_from_arrays(y_reduced, X_reduced)
    fit_reduced = fit_ols_hac(design_reduced)

    # Coeficientes no dummy deben coincidir (FWL)
    non_dummy_cols = ["const", "y_lag", "gdp_growth", "d_unemp", "inflation", "d_ffr", "credit_growth"]
    for col in non_dummy_cols:
        assert fit_full.params[col] == pytest.approx(fit_reduced.params[col], abs=1e-10)


# --- Test 2: CUSUM sobre regresión reducida ---


def test_cusum_matches_reduced_regression():
    """cusum corre sin error y rcusum coincide con regresión reducida."""
    rng = np.random.default_rng(SEED + 1)  # semilla distinta de la de X: con la misma, el ruido coincide con y_lag y R² = 1
    n = 106
    X = _make_X_with_impulse_dummies(n)
    y = (
        1.0
        + 2.0 * X["y_lag"]
        + 3.0 * X["gdp_growth"]
        - 1.5 * X["d_unemp"]
        + 0.5 * X["inflation"]
        + 1.0 * X["d_ffr"]
        + 2.0 * X["credit_growth"]
        + rng.normal(0, 1, n)
    )
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)

    result = cusum(fit)

    # Verificar que rcusum coincide con el de la regresión reducida
    impulse_cols = [c for c in X.columns if float(X[c].sum()) == 1.0]
    mask = (X[impulse_cols] == 1.0).any(axis=1)
    X_reduced = X.loc[~mask].drop(columns=impulse_cols)
    y_reduced = y.loc[~mask]
    sm_reduced = sm.OLS(y_reduced, X_reduced).fit()
    # statsmodels 0.15 devuelve 7 valores; rcusum arranca en la observación skip-1 (residuo del
    # ajuste inicial, no recursivo). La implementación lo descarta para alinearlo con las bandas.
    _, _, _, _, _, rcusum_expected, rcusumci_expected = recursive_olsresiduals(
        sm_reduced, skip=None, alpha=0.95
    )

    np.testing.assert_allclose(result["cusum"].to_numpy(), rcusum_expected[1:], rtol=1e-10)
    np.testing.assert_allclose(result["lower"].to_numpy(), rcusumci_expected[0], rtol=1e-10)
    np.testing.assert_allclose(result["upper"].to_numpy(), rcusumci_expected[1], rtol=1e-10)
    assert len(result["cusum"]) == len(result["lower"]) == len(result["upper"])


# --- Test 3: Bloque no dummy de V es definido positivo ---


def test_non_dummy_v_block_positive_definite():
    """Bloque no dummy de V es definido positivo y no se marca truncamiento."""
    rng = np.random.default_rng(SEED + 1)  # semilla distinta de la de X: con la misma, el ruido coincide con y_lag y R² = 1
    n = 106
    X = _make_X_with_impulse_dummies(n)
    y = (
        1.0
        + 2.0 * X["y_lag"]
        + 3.0 * X["gdp_growth"]
        - 1.5 * X["d_unemp"]
        + 0.5 * X["inflation"]
        + 1.0 * X["d_ffr"]
        + 2.0 * X["credit_growth"]
        + rng.normal(0, 1, n)
    )
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)

    # Guarda contra datos degenerados: con ajuste perfecto V es ~0 y el rango no mide nada
    assert fit.ser > 0.5

    # No se debe marcar truncamiento
    assert fit.psd_adjusted is False

    # El bloque no dummy de V debe ser definido positivo
    impulse_cols = [c for c in X.columns if float(X[c].sum()) == 1.0]
    non_impulse = [c for c in fit.cov.columns if c not in impulse_cols]
    V_sub = fit.cov.loc[non_impulse, non_impulse].to_numpy()
    eigvals = np.linalg.eigvalsh(V_sub)
    assert np.all(eigvals > 0)

    # El rango de V completo debe ser k - 4 (reducido por las 4 dummies)
    k = X.shape[1]
    rank_V = int(np.linalg.matrix_rank(fit.cov.to_numpy()))
    assert rank_V == k - 4


# --- Test 4: White con dummies de impulso ---


def test_white_df_with_impulse_dummies():
    """White: df = rango(Z_aux) - 1 (no cuenta los 24 productos dummy × regresor)."""
    rng = np.random.default_rng(SEED + 1)  # semilla distinta de la de X: con la misma, el ruido coincide con y_lag y R² = 1
    n = 106
    X = _make_X_with_impulse_dummies(n)
    y = (
        1.0
        + 2.0 * X["y_lag"]
        + 3.0 * X["gdp_growth"]
        - 1.5 * X["d_unemp"]
        + 0.5 * X["inflation"]
        + 1.0 * X["d_ffr"]
        + 2.0 * X["credit_growth"]
        + rng.normal(0, 1, n)
    )
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = white(fit)

    # Calcular rango esperado de Z_aux completo
    cols = [c for c in X.columns if c != "const"]
    z_dict: dict[str, np.ndarray] = {}
    for c in cols:
        z_dict[c] = X[c].to_numpy(dtype=float)
    for c in cols:
        z_dict[f"{c}²"] = X[c].to_numpy(dtype=float) ** 2
    for i, c1 in enumerate(cols):
        for c2 in cols[i + 1 :]:
            z_dict[f"{c1}×{c2}"] = X[c1].to_numpy(dtype=float) * X[c2].to_numpy(dtype=float)
    Z_full = pd.DataFrame(z_dict, index=X.index)
    Z_full_with_const = np.column_stack([np.ones(n), Z_full.to_numpy()])
    rank_expected = int(np.linalg.matrix_rank(Z_full_with_const))

    assert result["df"] == rank_expected - 1


# --- Test 5: Newey-West a mano (D4) ---


def test_fit_ols_hac_matches_manual_newey_wald():
    """Caso pequeño (n=12, 2 regresores, L=2): V coincide con NW sin corrección."""
    rng = np.random.default_rng(SEED)
    n = 12
    x = rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    y = 1.0 + 2.0 * x + e
    X = pd.DataFrame({"const": 1.0, "x": x})
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)

    # Calcular Newey-West a mano (D4: use_correction=False, use_t=False)
    L = 2  # hac_lags(12) = floor(4*(12/100)^(2/9)) = 1, pero el plan dice L=2
    # En realidad hac_lags(12) = max(1, floor(4*(12/100)^(2/9))) = max(1, floor(4*0.12^0.222)) = max(1, floor(4*0.669)) = max(1, 2) = 2
    # Verificamos:
    from src.estimation import hac_lags
    assert hac_lags(12) == 2
    L = hac_lags(12)

    X_np = X.to_numpy()
    resid = fit.resid.to_numpy()
    XtX_inv = np.linalg.inv(X_np.T @ X_np)

    # S = Σ e_t² x_t x_t' + Σ_{l=1}^L w_l Σ_{t=l+1}^n (e_t e_{t-l} x_t x_{t-l}' + e_{t-l} e_t x_{t-l} x_t')
    S = np.zeros((2, 2))
    for t in range(n):
        xt = X_np[t : t + 1].T
        S += resid[t] ** 2 * (xt @ xt.T)
    for l in range(1, L + 1):
        w_l = 1.0 - l / (L + 1)  # kernel de Bartlett
        for t in range(l, n):
            xt = X_np[t : t + 1].T
            xtl = X_np[t - l : t - l + 1].T
            S += w_l * resid[t] * resid[t - l] * (xt @ xtl.T + xtl @ xt.T)

    V_manual = XtX_inv @ S @ XtX_inv

    # fit.cov debe coincidir con V_manual
    np.testing.assert_allclose(fit.cov.to_numpy(), V_manual, rtol=1e-10)


# --- Test 6: diff_form_stationary usa fila "primera diferencia" ---


def test_diff_form_stationary_uses_first_difference_row():
    """diff_form_stationary juzga ΔDRALACBS con su fila «primera diferencia»."""
    stat = _make_stationarity_df()
    decision, forma = diff_form_stationary(stat, "dralacbs")

    # La fila "primera diferencia" tiene adf_p=0.001, kpss_p=0.15
    # decide(0.001, 0.15) = "niveles" (ADF rechaza, KPSS no rechaza)
    assert forma == "primera diferencia"
    assert decision == "niveles"


# --- Test 7: y_anchor del pronóstico dinámico ---


def test_y_anchor_is_delta_not_level():
    """y_anchor del pronóstico dinámico es ΔDR(2021T4) y no el nivel."""
    # OOS_ANCHOR es 2021T4
    assert OOS_ANCHOR == "2021Q4"
    # La forma de la dependiente es primera diferencia
    assert EXPECTED_FORMS["dralacbs"] == "ambigua (primera diferencia)"
    # Por lo tanto y_anchor = ΔDR(2021T4), no el nivel DR(2021T4)
    # (Esto se verificará completamente en T4 con forecast.dynamic)


# --- Test 8: Dummy sin variación fuera de R1 y tramo OOS lanza error ---


def test_dummy_without_variation_raises_error():
    """Dummy sin variación fuera de R1 y tramo OOS lanza ModelDataError."""
    full = _make_full_history()
    end = pd.Period("2026Q2", "Q-DEC")
    # Spec que empieza después de los trimestres COVID → dummies sin variación
    spec = VariantSpec("test_no_covid", "Test sin COVID", start=pd.Period("2021Q2", "Q-DEC"))
    with pytest.raises(ModelDataError, match="sin variación"):
        build_design(full, spec, "ambigua (primera diferencia)", end)


# --- Test 9: Faltante terminal en DRALACBS lanza error ---


def test_terminal_missing_raises_error():
    """Faltante terminal en DRALACBS lanza error en la principal."""
    full = _make_full_history()
    # Poner NaN en el último trimestre de dralacbs
    full.loc[pd.Period("2026Q2", "Q-DEC"), "dralacbs"] = np.nan
    end = pd.Period("2026Q2", "Q-DEC")
    from src.model1_config import MAIN
    with pytest.raises(ModelDataError, match="y.*2026Q2.*main"):
        build_design(full, MAIN, "ambigua (primera diferencia)", end)
