"""Datos sintéticos del Modelo I para los tests (spec 003).

Parámetros conocidos; X y el ruido de y salen de semillas independientes (con la misma semilla
el ruido coincidiría con una columna de X y el ajuste sería perfecto). Sin red ni disco, y sin
ningún dato real: estos módulos nunca leen `data/raw/`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.model1_config import SEED

# --- Datos sintéticos ---

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
              params: dict | None = None, start: str = "1998Q1") -> pd.DataFrame:
    """Historia start–2026T2 con ΔDR_t = c + ρ·ΔDR_{t−1} + Σ β·x_t + ε_t (DR en nivel).

    Incluye también las columnas que usan las variantes (DRALACBN, sub-carteras, logit y GDP
    nominal), con ruido propio de semillas independientes de X y del ruido de y.
    """
    p = dict(TRUE if params is None else params)
    idx = pd.period_range(start, END, freq="Q-DEC")
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
    ra = np.random.default_rng(SEED + 2)  # carteras alternativas: ruido propio
    rg = np.random.default_rng(SEED + 3)  # GDP nominal: ruido propio
    level = 20.0 + np.cumsum(dy)  # lejos de 0 y de 100: el logit debe estar definido

    def alt(scale: float) -> np.ndarray:
        return scale * level + np.cumsum(ra.normal(0.0, 0.03, n))

    return pd.DataFrame(
        {
            "dralacbs": level,
            "dralacbn": alt(1.0),
            "dralacbs_logit": np.log(level / (100.0 - level)),
            "drclacbs": alt(0.8),
            "drblacbs": alt(0.6),
            "drsreacbs": alt(0.4),
            "gdpc1_yoy": gdp,
            "gdp_yoy": gdp + 2.0 + rg.normal(0.0, 0.3, n),
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
