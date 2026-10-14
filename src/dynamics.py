"""Funciones puras de la dinámica del Modelo II (spec 004).

Efectos acumulados S y S_rez con su Wald HAC, multiplicadores ψ_h y respuesta acumulada R(h),
trimestre de efecto máximo h*, prueba de Granger, hipótesis H1 y H2, regla de lectura de la
evidencia y selección de K por AIC y BIC. Sin acceso a red, disco ni gráficos (RNF-7).
RF-6, RF-7, RF-10 a RF-13.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from src.estimation import wald
from src.model2_config import H_MAX, IC_TIE_TOL, PEAK_TIE_TOL, dffr_cols

ALPHA = 0.05
_Z_975 = float(norm.ppf(0.975))


def _combination(fit, terms: list[str]) -> dict:
    """Suma de coeficientes con su error HAC, χ²(1) de Wald, p e IC 95 % normal."""
    params, cov = fit.params, fit.cov
    R = np.array([[1.0 if c in terms else 0.0 for c in params.index]])
    est = float((R @ params.to_numpy())[0])
    se = float(np.sqrt((R @ cov.to_numpy() @ R.T)[0, 0]))
    w = wald(params, cov, R)
    return {"est": est, "se": se, "chi2": w["stat"], "p": w["p"],
            "ic_inf": est - _Z_975 * se, "ic_sup": est + _Z_975 * se}


def cumulative_effects(fit, K: int) -> dict:
    """S = θ0+…+θK y S_rez = θ1+…+θK, en pp de morosidad por 1 pp de ΔFFR (RF-10)."""
    cols = dffr_cols(K)
    return {"S": _combination(fit, cols), "S_rez": _combination(fit, cols[1:])}


def multipliers(params: pd.Series, K: int, hmax: int = H_MAX) -> pd.DataFrame:
    """ψ_h y R(h) para h = 0..hmax: ψ0 = θ0; ψ_h = θ_h·1{h ≤ K} + ρ·ψ_{h−1}; R(h) = Σ ψ."""
    rho = float(params["y_lag"])
    psi = np.zeros(hmax + 1)
    for h in range(hmax + 1):
        theta_h = float(params[f"d_ffr_l{h}"]) if h <= K else 0.0
        psi[h] = theta_h + (rho * psi[h - 1] if h > 0 else 0.0)
    return pd.DataFrame({"h": np.arange(hmax + 1), "psi": psi, "R": np.cumsum(psi)})


def peak_horizon(psi: pd.Series) -> dict:
    """h*: el menor h con |ψ_h| ≥ max|ψ| − PEAK_TIE_TOL (empate ⇒ menor h), con el signo de ψ_h*."""
    values = np.asarray(psi, dtype=float)
    magnitude = np.abs(values)
    h_star = int(np.argmax(magnitude >= magnitude.max() - PEAK_TIE_TOL))
    return {"h_star": h_star, "signo": "+" if values[h_star] >= 0 else "−", "psi": float(values[h_star])}


def granger_lags(fit, K: int) -> dict:
    """Wald HAC χ²(K) de H0: θ1 = … = θK = 0; excluye θ0 por ser simultáneo (RF-12)."""
    lagged = dffr_cols(K)[1:]
    R = np.array([[1.0 if c == t else 0.0 for c in fit.params.index] for t in lagged])
    w = wald(fit.params, fit.cov, R)
    return {"stat": w["stat"], "df": w["df"], "p": w["p"],
            "veredicto": "rechaza" if w["p"] < ALPHA else "no rechaza"}


def hypotheses(effects: dict, peak: dict) -> dict:
    """H1: S > 0 («sí» por el signo puntual; «respaldada» además con p < 0,05). H2: h* ≥ 1."""
    s = effects["S"]
    positive = s["est"] > 0
    return {
        "h1_signo": "sí" if positive else "no",
        "h1_respaldada": "sí" if positive and s["p"] < ALPHA else "no",
        "h2": "sí" if peak["h_star"] >= 1 else "no",
    }


def evidence_reading(granger: dict, effects: dict) -> dict:
    """Lectura de «¿hay efectos rezagados?» con solo lo rezagado (RF-13).

    C1: Granger rechaza al 5 %. C2: S_rez > 0 con p < 0,05. Fuerte si ambas; parcial si una; sin
    evidencia si ninguna. Con S_rez < 0 y p < 0,05 se añade la marca de signo contrario.
    """
    s_rez = effects["S_rez"]
    c1 = bool(granger["p"] < ALPHA)
    c2 = bool(s_rez["est"] > 0 and s_rez["p"] < ALPHA)
    label = ("evidencia fuerte", "evidencia parcial", "sin evidencia")[2 - (int(c1) + int(c2))]
    return {"c1": c1, "c2": c2, "etiqueta": label,
            "signo_contrario": bool(s_rez["est"] < 0 and s_rez["p"] < ALPHA)}


def select_k(fits: dict[int, object]) -> dict:
    """AIC y BIC de cada modelo (lnL gaussiana de statsmodels); gana el menor K en un empate (RF-6)."""
    ks = sorted(fits)
    table = pd.DataFrame({
        "K": ks,
        "n_params": [int(fits[k].k) for k in ks],
        "nobs": [int(fits[k].nobs) for k in ks],
        "aic": [float(fits[k].sm_result.aic) for k in ks],
        "bic": [float(fits[k].sm_result.bic) for k in ks],
    })

    def pick(column: str) -> int:
        best = table[column].min()
        return int(table.loc[table[column] <= best + IC_TIE_TOL, "K"].iloc[0])

    return {"k_aic": pick("aic"), "k_bic": pick("bic"), "table": table}
