"""Tests de ``src/stationarity.py`` (T7, spec 001).

ADF, KPSS, regla de decisión, orden de integración y tabla (RF-19 a RF-21).
"""

import numpy as np
import pandas as pd
import pytest

from src.stationarity import (
    adf_test,
    decide,
    integration_order,
    is_stationary,
    kpss_test,
    rejects,
    stationarity_table,
)
from src.config import ALPHA, ADF_MAXLAG


# ---------- rejects ----------

def test_rejects_p_less_alpha():
    """p < alpha → True (rechaza)."""
    assert rejects(0.01, 0.05)
    assert rejects(0.049, 0.05)


def test_rejects_p_ge_alpha():
    """p >= alpha → False (no rechaza). Borde p=0.05 → no rechaza."""
    assert not rejects(0.05, 0.05)
    assert not rejects(0.10, 0.05)


# ---------- decide (tabla de verdad pre-registrada) ----------

def test_decide_adf_rejects_kpss_not_rejects_niveles():
    """ADF rechaza (p<0.05) y KPSS no rechaza (p>=0.05) → 'niveles'."""
    assert decide(0.01, 0.10) == "niveles"
    assert decide(0.04, 0.05) == "niveles"  # KPSS p=0.05 no rechaza


def test_decide_adf_not_rejects_kpss_rejects_primera_diferencia():
    """ADF no rechaza (p>=0.05) y KPSS rechaza (p<0.05) → 'primera diferencia'."""
    assert decide(0.10, 0.01) == "primera diferencia"
    assert decide(0.05, 0.04) == "primera diferencia"  # ADF p=0.05 no rechaza


def test_decide_both_reject_ambigua():
    """Ambas rechazan → 'ambigua (primera diferencia)'."""
    assert decide(0.01, 0.01) == "ambigua (primera diferencia)"


def test_decide_neither_rejects_ambigua():
    """Ninguna rechaza → 'ambigua (primera diferencia)'."""
    assert decide(0.10, 0.10) == "ambigua (primera diferencia)"
    assert decide(0.05, 0.05) == "ambigua (primera diferencia)"  # borde: ninguna rechaza


# ---------- integration_order ----------

def test_integration_order_niveles_I0():
    """Decisión 'niveles' → I(0)."""
    assert integration_order("niveles", True) == "I(0)"
    assert integration_order("niveles", False) == "I(0)"  # diff_stationary no importa


def test_integration_order_primera_diferencia_I1():
    """Decisión 'primera diferencia' y diff estacionaria → I(1)."""
    assert integration_order("primera diferencia", True) == "I(1)"


def test_integration_order_primera_diferencia_posible_I2():
    """Decisión 'primera diferencia' y diff NO estacionaria → 'posible I(2)'."""
    assert integration_order("primera diferencia", False) == "posible I(2)"


def test_integration_order_ambigua_posible_I2():
    """Decisión 'ambigua (primera diferencia)' → 'posible I(2)' salvo que diff sea estacionaria."""
    assert integration_order("ambigua (primera diferencia)", True) == "I(1)"
    assert integration_order("ambigua (primera diferencia)", False) == "posible I(2)"


# ---------- adf_test / kpss_test (con datos sintéticos) ----------

def test_adf_test_white_noise():
    """Ruido blanco (n=400) → ADF rechaza raíz unitaria (p < 0.05), lags <= 4."""
    rng = np.random.default_rng(20261002)
    x = pd.Series(rng.normal(0, 1, 400))
    res = adf_test(x)
    assert res["pvalue"] < 0.05
    assert res["lags"] <= ADF_MAXLAG
    assert "stat" in res and "n_obs" in res


def test_adf_test_random_walk():
    """Paseo aleatorio (n=400) → ADF no rechaza (p >= 0.05)."""
    rng = np.random.default_rng(20261003)
    x = pd.Series(np.cumsum(rng.normal(0, 1, 400)))
    res = adf_test(x)
    assert res["pvalue"] >= 0.05
    assert res["lags"] <= ADF_MAXLAG


def test_kpss_test_white_noise():
    """Ruido blanco → KPSS no rechaza estacionariedad (p >= 0.05)."""
    rng = np.random.default_rng(20261004)
    x = pd.Series(rng.normal(0, 1, 400))
    res = kpss_test(x)
    assert res["pvalue"] >= 0.05
    assert "stat" in res and "pvalue_truncated" in res


def test_kpss_test_random_walk():
    """Paseo aleatorio → KPSS rechaza (p < 0.05)."""
    rng = np.random.default_rng(20261005)
    x = pd.Series(np.cumsum(rng.normal(0, 1, 400)))
    res = kpss_test(x)
    assert res["pvalue"] < 0.05


def test_kpss_truncation_recorded():
    """KPSS registra pvalue_truncated cuando statsmodels lo trunca."""
    rng = np.random.default_rng(20261006)
    x = pd.Series(rng.normal(0, 1, 400))
    res = kpss_test(x)
    # pvalue_truncated es string: "<0,01", ">0,10" o ""
    assert isinstance(res["pvalue_truncated"], str)


# ---------- stationarity_table ----------

def _make_full_panel() -> pd.DataFrame:
    """Panel sintético con 17 variables testeables (sin usrec, sin _d)."""
    rng = np.random.default_rng(20261007)
    n = 110  # ~2000Q1 a 2025Q4
    idx = pd.period_range("2000Q1", periods=n, freq="Q-DEC")

    # Variables que se testean (17): morosidad nivel (5), yoy (4), unrate, fedfunds, coralacbs
    # Según plan: excluye usrec y columnas _d
    data = {
        "dralacbs": pd.Series(rng.normal(2, 0.5, n), index=idx),
        "dralacbn": pd.Series(rng.normal(2, 0.5, n), index=idx),
        "drclacbs": pd.Series(rng.normal(2, 0.5, n), index=idx),
        "drblacbs": pd.Series(rng.normal(2, 0.5, n), index=idx),
        "drsreacbs": pd.Series(rng.normal(2, 0.5, n), index=idx),
        "gdpc1_yoy": pd.Series(rng.normal(2, 1, n), index=idx),
        "gdp_yoy": pd.Series(rng.normal(2, 1, n), index=idx),
        "cpiaucsl_yoy": pd.Series(rng.normal(2, 1, n), index=idx),
        "loans_yoy": pd.Series(rng.normal(2, 1, n), index=idx),
        "unrate": pd.Series(rng.normal(5, 1, n), index=idx),
        "fedfunds": pd.Series(rng.normal(2, 1, n), index=idx),
        "coralacbs": pd.Series(rng.normal(0.5, 0.1, n), index=idx),
        # Columnas _logit (se testean - no terminan en _d)
        "dralacbs_logit": pd.Series(rng.normal(0, 1, n), index=idx),
        "dralacbn_logit": pd.Series(rng.normal(0, 1, n), index=idx),
        "drclacbs_logit": pd.Series(rng.normal(0, 1, n), index=idx),
        "drblacbs_logit": pd.Series(rng.normal(0, 1, n), index=idx),
        "drsreacbs_logit": pd.Series(rng.normal(0, 1, n), index=idx),
        # Columnas _d y usrec (no se testean)
        "dralacbs_d": pd.Series(rng.normal(0, 0.2, n), index=idx),
        "dralacbn_d": pd.Series(rng.normal(0, 0.2, n), index=idx),
        "drclacbs_d": pd.Series(rng.normal(0, 0.2, n), index=idx),
        "drblacbs_d": pd.Series(rng.normal(0, 0.2, n), index=idx),
        "drsreacbs_d": pd.Series(rng.normal(0, 0.2, n), index=idx),
        "unrate_d": pd.Series(rng.normal(0, 0.2, n), index=idx),
        "fedfunds_d": pd.Series(rng.normal(0, 0.3, n), index=idx),
        "usrec": pd.Series(np.zeros(n), index=idx),
    }
    return pd.DataFrame(data)


def test_stationarity_table_shape_and_exclusions():
    """Tabla: 17 variables × 2 formas = 34 filas; excluye usrec y _d."""
    full = _make_full_panel()
    tested_cols = [c for c in full.columns if c != "usrec" and not c.endswith("_d")]
    assert len(tested_cols) == 17

    table = stationarity_table(full, tested_cols, pd.Period("2000Q1", "Q-DEC"), pd.Period("2025Q4", "Q-DEC"))
    assert len(table) == 34  # 17 vars × 2 formas
    assert set(table.columns) >= {"variable", "etiqueta", "forma", "n_obs", "adf_stat", "adf_p", "adf_lags",
                                   "kpss_stat", "kpss_p", "kpss_p_truncado", "decision", "orden"}
    # Verificar exclusiones
    assert "usrec" not in table["variable"].values
    assert not any(table["variable"].str.endswith("_d"))


def test_stationarity_table_has_decision_and_order():
    """Cada variable tiene decision y orden en la fila 'tal cual'."""
    full = _make_full_panel()
    tested_cols = [c for c in full.columns if c != "usrec" and not c.endswith("_d")]
    table = stationarity_table(full, tested_cols, pd.Period("2000Q1", "Q-DEC"), pd.Period("2025Q4", "Q-DEC"))

    # Solo filas "tal cual" tienen decision/orden; "primera diferencia" los deja vacíos
    tal_cual = table[table["forma"] == "tal cual"]
    decisions = tal_cual["decision"].unique()
    assert set(decisions).issubset({"niveles", "primera diferencia", "ambigua (primera diferencia)"})
    orders = tal_cual["orden"].unique()
    assert set(orders).issubset({"I(0)", "I(1)", "posible I(2)"})

    # Para cada variable, decision y orden son consistentes
    for var in tested_cols:
        var_rows = table[table["variable"] == var]
        assert len(var_rows) == 2  # tal cual y primera diferencia
        decision_row = var_rows[var_rows["forma"] == "tal cual"]
        assert len(decision_row) == 1
        decision = decision_row["decision"].iloc[0]
        orden = decision_row["orden"].iloc[0]
        if decision == "niveles":
            assert orden == "I(0)"
        elif decision == "primera diferencia":
            assert orden in ("I(1)", "posible I(2)")