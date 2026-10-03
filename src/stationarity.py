"""Pruebas de estacionariedad y regla de decisión (spec 001).

Funciones puras: ADF, KPSS, regla pre-registrada, orden de integración y tabla.
Sin acceso a red, disco ni gráficos (RNF-6). RF-19 a RF-21.
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

from src.config import ALPHA, ADF_MAXLAG


# --- Helpers ---

def rejects(p: float, alpha: float = ALPHA) -> bool:
    """True si p < alpha (rechaza H0). Borde p == alpha → no rechaza."""
    return p < alpha


def is_stationary(adf_p: float, kpss_p: float, alpha: float = ALPHA) -> bool:
    """Estacionaria si ADF rechaza raíz unitaria Y KPSS no rechaza estacionariedad."""
    return rejects(adf_p, alpha) and not rejects(kpss_p, alpha)


def decide(adf_p: float, kpss_p: float, alpha: float = ALPHA) -> str:
    """Regla de decisión pre-registrada (spec 001, Definiciones).

    Returns
    -------
    "niveles" | "primera diferencia" | "ambigua (primera diferencia)"
    """
    adf_r = rejects(adf_p, alpha)
    kpss_r = rejects(kpss_p, alpha)

    if adf_r and not kpss_r:
        return "niveles"
    if not adf_r and kpss_r:
        return "primera diferencia"
    # Ambas rechazan o ninguna rechaza
    return "ambigua (primera diferencia)"


def integration_order(decision: str, diff_stationary: bool) -> str:
    """Orden de integración según decisión y estacionariedad de la primera diferencia.

    Returns
    -------
    "I(0)" | "I(1)" | "posible I(2)"
    """
    if decision == "niveles":
        return "I(0)"
    if decision == "primera diferencia":
        return "I(1)" if diff_stationary else "posible I(2)"
    # "ambigua (primera diferencia)"
    return "I(1)" if diff_stationary else "posible I(2)"


# --- ADF ---

def adf_test(x: pd.Series, maxlag: int = ADF_MAXLAG) -> dict:
    """Test ADF con constante, sin tendencia, rezagos por AIC (max 4).

    Returns
    -------
    dict con: stat, pvalue, lags, n_obs
    """
    # Limpiar: eliminar NaN
    x_clean = x.dropna()
    if len(x_clean) < 10:
        return {"stat": np.nan, "pvalue": np.nan, "lags": 0, "n_obs": len(x_clean)}

    result = adfuller(x_clean, maxlag=maxlag, regression="c", autolag="AIC")
    return {
        "stat": float(result[0]),
        "pvalue": float(result[1]),
        "lags": int(result[2]),
        "n_obs": int(len(x_clean)),
    }


# --- KPSS ---

def kpss_test(x: pd.Series) -> dict:
    """Test KPSS con constante, ancho de banda Newey-West automático (nlags='auto').

    Captura InterpolationWarning para registrar si el p-valor fue truncado.

    Returns
    -------
    dict con: stat, pvalue, pvalue_truncated ("<0,01" | ">0,10" | "")
    """
    x_clean = x.dropna()
    if len(x_clean) < 10:
        return {"stat": np.nan, "pvalue": np.nan, "pvalue_truncated": ""}

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = kpss(x_clean, regression="c", nlags="auto")
        pvalue = float(result[1])
        truncated = ""
        for warning in w:
            if "InterpolationWarning" in str(warning.category):
                if pvalue <= 0.01:
                    truncated = "<0,01"
                elif pvalue >= 0.10:
                    truncated = ">0,10"
                break

    return {
        "stat": float(result[0]),
        "pvalue": pvalue,
        "pvalue_truncated": truncated,
    }


# --- Tabla de estacionariedad ---

def stationarity_table(
    full: pd.DataFrame,
    columns: list[str],
    start: pd.Period,
    end: pd.Period,
) -> pd.DataFrame:
    """Construye la tabla de ADF y KPSS para cada variable en `columns`.

    Parámetros
    ----------
    full : DataFrame con transformaciones sobre historia completa (1998+)
    columns : lista de 17 variables a testear (sin usrec, sin _d)
    start, end : rango de la muestra de estimación (2000T1..end)

    Returns
    -------
    DataFrame largo: 34 filas (17 vars × 2 formas) con columnas:
    variable, etiqueta, forma, n_obs, adf_stat, adf_p, adf_lags,
    kpss_stat, kpss_p, kpss_p_truncado, decision, orden
    """
    from src.config import COLUMN_LABELS

    rows = []
    for col in columns:
        if col not in full.columns:
            continue

        # Forma "tal cual": la columna del panel en [start:end]
        nivel = full[col].loc[start:end]

        # Forma "primera diferencia": diff sobre la historia descargada completa
        # (según Definiciones: diferencia trimestral de esa columna, calculada sobre historia desde 1998)
        dif = full[col].diff().loc[start:end]

        # ADF y KPSS para cada forma
        adf_nivel = adf_test(nivel)
        kpss_nivel = kpss_test(nivel)
        adf_dif = adf_test(dif)
        kpss_dif = kpss_test(dif)

        # Decisión y orden se basan en la forma "tal cual"
        decision = decide(adf_nivel["pvalue"], kpss_nivel["pvalue"])
        orden = integration_order(decision, is_stationary(adf_dif["pvalue"], kpss_dif["pvalue"]))

        etiqueta = COLUMN_LABELS.get(col, col)

        for forma, adf, kpss in [
            ("tal cual", adf_nivel, kpss_nivel),
            ("primera diferencia", adf_dif, kpss_dif),
        ]:
            rows.append({
                "variable": col,
                "etiqueta": etiqueta,
                "forma": forma,
                "n_obs": adf["n_obs"],
                "adf_stat": adf["stat"],
                "adf_p": adf["pvalue"],
                "adf_lags": adf["lags"],
                "kpss_stat": kpss["stat"],
                "kpss_p": kpss["pvalue"],
                "kpss_p_truncado": kpss["pvalue_truncated"],
                "decision": decision if forma == "tal cual" else "",
                "orden": orden if forma == "tal cual" else "",
            })

    return pd.DataFrame(rows)