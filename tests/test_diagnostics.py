"""Tests para src/diagnostics.py (spec 003, tarea 3).

Cubre RF-12 a RF-14 y RNF-4 según plan §7.
Datos sintéticos con parámetros conocidos; semilla fija; sin red ni disco.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.design import Design
from src.diagnostics import (
    breusch_godfrey,
    breusch_pagan,
    chow_wald,
    cusum,
    diagnostics_table,
    jarque_bera_test,
    reset,
    vif,
    white,
)
from src.estimation import fit_ols_hac
from src.model1_config import SEED


# --- Helpers ---


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


def _ar1(rng: np.random.Generator, n: int, rho: float) -> np.ndarray:
    """Simula un proceso AR(1) con coeficiente rho y innovaciones N(0,1)."""
    e = rng.normal(0.0, 1.0, n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + e[t]
    return x


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


# --- Test 1: Breusch-Godfrey ---


def test_breusch_godfrey_rejects_ar1_errors():
    """BG rechaza (p < 0.05) con e AR(1) 0.7."""
    rng = np.random.default_rng(SEED)
    n = 200
    x = rng.normal(0, 1, n)
    e = _ar1(rng, n, 0.7)
    y = 1.0 + 2.0 * x + e
    X = pd.DataFrame({"const": 1.0, "x": x})
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = breusch_godfrey(fit)
    assert result["p"] < 0.05
    assert result["veredicto"] == "falla"


def test_breusch_godfrey_no_reject_iid_errors():
    """BG no rechaza con e iid."""
    rng = np.random.default_rng(SEED)
    n = 200
    x = rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    y = 1.0 + 2.0 * x + e
    X = pd.DataFrame({"const": 1.0, "x": x})
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = breusch_godfrey(fit)
    assert result["p"] >= 0.05
    assert result["veredicto"] == "pasa"


# --- Test 2: Chow Wald ---


def test_chow_wald_rejects_with_break():
    """Chow Wald rechaza con quiebre simulado en pendiente."""
    rng = np.random.default_rng(SEED)
    n = 200
    idx = pd.period_range("2000Q1", periods=n, freq="Q-DEC")
    x = rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    break_t = 40
    y = np.where(np.arange(n) < break_t, 1.0 + 2.0 * x, 1.0 + 5.0 * x) + e
    X = pd.DataFrame({"const": 1.0, "x": x}, index=idx)
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = chow_wald(fit, "2010Q1")
    assert result["p"] < 0.05
    assert result["veredicto"] == "falla"


def test_chow_wald_no_reject_without_break():
    """Chow Wald no rechaza sin quiebre."""
    rng = np.random.default_rng(SEED)
    n = 200
    idx = pd.period_range("2000Q1", periods=n, freq="Q-DEC")
    x = rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    y = 1.0 + 2.0 * x + e
    X = pd.DataFrame({"const": 1.0, "x": x}, index=idx)
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = chow_wald(fit, "2010Q1")
    assert result["p"] >= 0.05
    assert result["veredicto"] == "pasa"


# --- Test 3: White con dummies ---


def test_white_with_dummies_df_equals_rank_minus_1():
    """White: X con dummies → df = rango(Z_aux) - 1."""
    rng = np.random.default_rng(SEED + 1)  # semilla distinta de la de X: con la misma, el ruido coincide con y_lag y R² = 1
    n = 106
    X = _make_X_with_impulse_dummies(n)
    y = rng.normal(0, 1, n)
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = white(fit)

    # Calcular rango esperado de Z_aux completo (sin eliminar colineales)
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


# --- Test 4: VIF ---


def test_vif_alert_with_collinear_regressors():
    """VIF: dos regresores casi colineales → «alerta»."""
    rng = np.random.default_rng(SEED)
    n = 100
    x1 = rng.normal(0, 1, n)
    x2 = x1 + rng.normal(0, 0.001, n)  # casi colineal
    y = 1.0 + 2.0 * x1 + 3.0 * x2 + rng.normal(0, 1, n)
    X = pd.DataFrame(
        {
            "const": 1.0,
            "y_lag": x1,
            "gdp_growth": x2,
            "d_unemp": rng.normal(0, 1, n),
            "inflation": rng.normal(0, 1, n),
            "d_ffr": rng.normal(0, 1, n),
            "credit_growth": rng.normal(0, 1, n),
        }
    )
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = vif(fit)

    # y_lag y gdp_growth son casi colineales → VIF alto
    y_lag_row = result[result["term"] == "y_lag"].iloc[0]
    assert y_lag_row["vif"] > 10.0
    assert y_lag_row["veredicto"] == "alerta"


# --- Test 5: CUSUM ---


def test_cusum_fails_with_strong_break():
    """CUSUM: quiebre fuerte → «falla»."""
    rng = np.random.default_rng(SEED)
    n = 100
    idx = pd.period_range("2000Q1", periods=n, freq="Q-DEC")
    x = rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    # Quiebre fuerte en la media en t=50
    y = np.where(np.arange(n) < 50, 1.0 + 2.0 * x, 10.0 + 2.0 * x) + e
    X = pd.DataFrame({"const": 1.0, "x": x}, index=idx)
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = cusum(fit)
    assert result["veredicto"] == "falla"


def test_cusum_passes_with_stable_process():
    """CUSUM: proceso estable → «pasa»."""
    rng = np.random.default_rng(SEED)
    n = 100
    idx = pd.period_range("2000Q1", periods=n, freq="Q-DEC")
    x = rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    y = 1.0 + 2.0 * x + e
    X = pd.DataFrame({"const": 1.0, "x": x}, index=idx)
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    result = cusum(fit)
    assert result["veredicto"] == "pasa"


# --- Test 6: diagnostics_table ---


def test_diagnostics_table_contains_all_rf12_tests():
    """diagnostics_table trae todas las pruebas de RF-12."""
    rng = np.random.default_rng(SEED + 1)  # semilla distinta de la de X: con la misma, el ruido coincide con y_lag y R² = 1
    n = 106
    X = _make_X_with_impulse_dummies(n)
    y = rng.normal(0, 1, n)
    design = _design_from_arrays(y, X)
    fit = fit_ols_hac(design)
    table = diagnostics_table(fit)

    pruebas = table["prueba"].tolist()
    assert "Breusch-Godfrey" in pruebas
    assert "Breusch-Pagan" in pruebas
    assert "White" in pruebas
    assert "Jarque-Bera" in pruebas
    assert "RESET" in pruebas
    assert any(p.startswith("VIF") for p in pruebas)
    assert "Chow 2008T3" in pruebas
    assert "Chow 2020T2" in pruebas
    assert "CUSUM" in pruebas


# --- Chow: trimestres posteriores útiles y nota de tamaño del 2020T2 (plan §2, review-audit r2) ---


def _chow_fit(n: int = 106):
    X = _make_X_with_impulse_dummies(n)
    y = 1.0 + 2.0 * X["y_lag"] + np.random.default_rng(SEED + 1).normal(0, 1, n)  # ruido independiente de X
    return fit_ols_hac(_design_from_arrays(y, X))


def test_chow_wald_counts_post_break_quarters_net_of_impulse_dummies():
    fit = _chow_fit()
    r = chow_wald(fit, "2020Q2")
    assert (r["n_post"], r["n_post_util"]) == (25, 21)  # 2020T2–2026T2, menos 4 dummies de impulso
    r2 = chow_wald(fit, "2008Q3")
    assert (r2["n_post"], r2["n_post_util"]) == (72, 68)  # 2 + 68 + 2 trimestres; las 4 dummies también caen después


def test_chow_wald_without_impulse_dummies_counts_every_post_break_quarter():
    n = 106
    X = _make_X_with_impulse_dummies(n)
    X = X.drop(columns=[c for c in X.columns if c.startswith("covid_")])
    y = 1.0 + 2.0 * X["y_lag"] + np.random.default_rng(SEED + 1).normal(0, 1, n)
    r = chow_wald(fit_ols_hac(_design_from_arrays(y, X)), "2020Q2")
    assert r["n_post"] == r["n_post_util"] == 25


def test_only_the_2020t2_chow_note_warns_that_the_size_may_differ_from_5_percent():
    table = diagnostics_table(_chow_fit()).set_index("prueba")
    n2020 = table.loc["Chow 2020T2", "nota"]
    assert "quedan 21 trimestres posteriores útiles para 7 restricciones" in n2020
    assert "el tamaño empírico del contraste puede diferir del 5 % nominal" in n2020
    n2008 = table.loc["Chow 2008T3", "nota"]
    assert "diferir del 5 %" not in n2008 and "quedan" not in n2008
    assert "Wald HAC con interacciones" in n2008 and "Wald HAC con interacciones" in n2020


def test_the_2020t2_chow_note_is_neutral_and_does_not_change_the_verdict():
    table = diagnostics_table(_chow_fit()).set_index("prueba")
    row = table.loc["Chow 2020T2"]
    assert row["veredicto"] == ("falla" if row["p_valor"] < 0.05 else "pasa")  # el veredicto sigue a p
    nota = row["nota"].lower()
    for banned in ["sobredimensionado", "sobrerrechaza", "causa", "causal", "provoca", "debido a"]:
        assert banned not in nota
