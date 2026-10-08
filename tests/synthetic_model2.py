"""Datos sintéticos del Modelo II para los tests (spec 004).

Parámetros conocidos; X y el ruido de y salen de semillas independientes (SEED2 y SEED2 + 1).
Sin red ni disco y sin ningún dato real: nunca lee `data/raw/`. La historia empieza en 1998T1 con
`fedfunds_d` faltante en ese trimestre (como en el panel real), de modo que la muestra común M
empieza en 2000T2.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED2 = 20261008
START = "1998Q1"
END = pd.Period("2026Q2", "Q-DEC")
N_QUARTERS = 114                      # 1998T1–2026T2

THETA = (0.30, 0.25, 0.20, 0.15)      # θ0..θ3 (K verdadero = 3)
RHO = 0.5
CONST = 0.02
GAMMA = {"gdp_l1": -0.05, "d_unemp_l1": 0.20, "inflation_l1": 0.03, "credit_l4": 0.02}


def make_full2(n: int = N_QUARTERS, seed_x: int = SEED2, seed_e: int = SEED2 + 1,
               sigma: float = 0.3, theta: tuple[float, ...] = THETA, rho: float = RHO,
               gamma: dict[str, float] | None = None, const: float = CONST,
               ffr_sd: float = 0.5, ffr_ar: float = 0.0, err_ar: float = 0.0,
               start: str = START) -> pd.DataFrame:
    """Historia con ΔDR_t = c + ρ·ΔDR_{t−1} + Σ_j θ_j·ΔFFR_{t−j} + Σ γ·controles + ε_t.

    ΔFFR es i.i.d. N(0, ffr_sd²) salvo que ffr_ar > 0 (AR(1)); los errores son i.i.d. salvo que
    err_ar > 0 (AR(1)). X y ε usan semillas independientes. `dralacbs` es el nivel (acumula ΔDR).
    """
    g = dict(GAMMA if gamma is None else gamma)
    idx = pd.period_range(start, periods=n, freq="Q-DEC")
    rx = np.random.default_rng(seed_x)
    re = np.random.default_rng(seed_e)
    gdp = rx.normal(2.0, 1.0, n)
    d_unemp = rx.normal(0.0, 0.3, n)
    infl = rx.normal(2.0, 0.5, n)
    loans = rx.normal(5.0, 2.0, n)
    shock = rx.normal(0.0, ffr_sd, n)
    d_ffr = np.zeros(n)
    for t in range(n):
        d_ffr[t] = shock[t] + (ffr_ar * d_ffr[t - 1] if t > 0 else 0.0)
    innov = re.normal(0.0, sigma, n)
    eps = np.zeros(n)
    for t in range(n):
        eps[t] = innov[t] + (err_ar * eps[t - 1] if t > 0 else 0.0)
    kmax = len(theta) - 1
    first = max(8, kmax)
    dy = np.zeros(n)
    for t in range(first, n):
        dy[t] = (const + rho * dy[t - 1]
                 + sum(theta[j] * d_ffr[t - j] for j in range(kmax + 1))
                 + g["gdp_l1"] * gdp[t - 1] + g["d_unemp_l1"] * d_unemp[t - 1]
                 + g["inflation_l1"] * infl[t - 1] + g["credit_l4"] * loans[t - 4] + eps[t])
    loans_yoy = loans.copy()
    loans_yoy[:4] = np.nan
    fedfunds = 1000.0 + np.cumsum(d_ffr)   # lejos del umbral de tasa cero; with_zero_rate lo fija donde se quiera
    fedfunds_d = np.diff(fedfunds, prepend=np.nan)
    return pd.DataFrame(
        {
            "dralacbs": 20.0 + np.cumsum(dy),
            "gdpc1_yoy": gdp,
            "unrate_d": d_unemp,
            "cpiaucsl_yoy": infl,
            "fedfunds": fedfunds,
            "fedfunds_d": fedfunds_d,
            "loans_yoy": loans_yoy,
        },
        index=idx,
    )


def with_zero_rate(full: pd.DataFrame, spans: list[tuple[str, str]], level: float = 0.1) -> pd.DataFrame:
    """Copia de `full` con el promedio trimestral de la tasa en `level` dentro de cada tramo."""
    out = full.copy()
    for first, last in spans:
        out.loc[pd.Period(first, "Q-DEC"):pd.Period(last, "Q-DEC"), "fedfunds"] = level
    return out
