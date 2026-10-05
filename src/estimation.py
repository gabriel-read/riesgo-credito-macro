"""Funciones puras de estimación del Modelo I (spec 003).

Ventana HAC, MCO con Newey-West, truncamiento espectral, inferencia
desde (b, V), Wald, efectos de largo plazo con método delta y efectos
por 1 DE. Sin acceso a red, disco ni gráficos (RNF-6). RF-6, RF-7, RF-10.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import chi2, norm

from src.design import Design
from src.model1_config import (
    COVID_QUARTERS,
    LONGRUN_MIN_GAP,
    MACRO_TERMS,
    MIN_DOF,
    PSD_REL_TOL,
)

_Z_975 = float(norm.ppf(0.975))  # 1.959964


@dataclass(frozen=True)
class Fit:
    """Resultado de una estimación MCO con errores HAC.

    Attributes
    ----------
    params : pd.Series
        Coeficientes estimados.
    cov : pd.DataFrame
        Matriz de covarianza HAC tras psd_truncate.
    resid, fitted : pd.Series
        Residuos y valores ajustados.
    nobs, k : int
        Número de observaciones y parámetros.
    hac_lags : int
        Rezagos de Newey-West usados.
    psd_adjusted : bool
        Si se aplicó truncamiento espectral.
    rsquared, rsquared_adj : float
        R² y R² ajustado.
    ser : float
        Error estándar de la regresión.
    design : Design
        Matriz de diseño usada.
    sm_result : Any
        Resultado completo de statsmodels (para diagnósticos).
    """

    params: pd.Series
    cov: pd.DataFrame
    resid: pd.Series
    fitted: pd.Series
    nobs: int
    k: int
    hac_lags: int
    psd_adjusted: bool
    rsquared: float
    rsquared_adj: float
    ser: float
    design: Design
    sm_result: Any


# --- Ventana HAC ---


def hac_lags(nobs: int) -> int:
    """Rezagos de Newey-West: floor(4*(T/100)^(2/9)), mínimo 1."""
    return max(1, int(np.floor(4 * (nobs / 100) ** (2 / 9))))


# --- Truncamiento espectral ---


def psd_truncate(V: np.ndarray, rel_tol: float = PSD_REL_TOL) -> tuple[np.ndarray, bool]:
    """Truncamiento espectral de una matriz de covarianzas.

    Simetriza V; si el autovalor mínimo <= rel_tol * max|eig|, eleva esos
    autovalores al piso (rel_tol * max|eig|) y reconstruye V' = Q diag(eig') Q.T.

    Returns
    -------
    tuple[np.ndarray, bool]
        (V_ajustada, True) si se truncó; (V, False) si no.
    """
    V = np.asarray(V, dtype=float)
    V_sym = (V + V.T) / 2.0
    eigvals, eigvecs = np.linalg.eigh(V_sym)
    max_abs = float(np.max(np.abs(eigvals)))
    floor = rel_tol * max_abs
    if float(np.min(eigvals)) <= floor:
        eigvals_adj = np.maximum(eigvals, floor)
        V_adj = (eigvecs * eigvals_adj) @ eigvecs.T
        return (V_adj + V_adj.T) / 2.0, True
    return V_sym, False


# --- Estimación MCO + Newey-West ---


def _impulse_dummy_cols(X: pd.DataFrame) -> list[str]:
    """Columnas que valen 1 en exactamente una observación (dummies de impulso)."""
    return [c for c in X.columns if float(X[c].sum()) == 1.0]


def fit_ols_hac(design: Design) -> Fit:
    """MCO con errores Newey-West puro (D4) y truncamiento espectral (D15).

    - Newey-West: kernel de Bartlett, use_correction=False, use_t=False.
    - La positividad se comprueba solo en el bloque de V sin dummies de
      impulso (C3/D15); el rango reducido por esas dummies es esperado.
    """
    y = design.y
    X = design.X
    nobs = int(y.shape[0])
    k = int(X.shape[1])
    L = hac_lags(nobs)
    result = sm.OLS(y, X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": L, "kernel": "bartlett", "use_correction": False},
        use_t=False,
    )
    V_HAC = result.cov_params()
    impulse = _impulse_dummy_cols(X)
    non_impulse = [c for c in V_HAC.columns if c not in impulse]
    V_trunc = V_HAC.copy()
    adjusted = False
    if non_impulse:
        V_sub = V_HAC.loc[non_impulse, non_impulse].to_numpy()
        V_sub_trunc, adjusted = psd_truncate(V_sub)
        V_trunc.loc[non_impulse, non_impulse] = V_sub_trunc
    return Fit(
        params=result.params,
        cov=V_trunc,
        resid=result.resid,
        fitted=result.fittedvalues,
        nobs=nobs,
        k=k,
        hac_lags=L,
        psd_adjusted=adjusted,
        rsquared=float(result.rsquared),
        rsquared_adj=float(result.rsquared_adj),
        ser=float(np.sqrt(result.mse_resid)),
        design=design,
        sm_result=result,
    )


# --- Inferencia desde (b, V) ---


def inference(params: pd.Series, cov: pd.DataFrame) -> pd.DataFrame:
    """Inferencia desde (b, V): coef, se, z, p (normal bilateral) e IC 95 %.

    ic_inf = coef - 1.959964*se; ic_sup = coef + 1.959964*se.
    """
    coef = params.to_numpy()
    se = np.sqrt(np.diag(cov.to_numpy()))
    z = coef / se
    p = 2.0 * (1.0 - norm.cdf(np.abs(z)))
    ic_inf = coef - _Z_975 * se
    ic_sup = coef + _Z_975 * se
    return pd.DataFrame(
        {
            "coef": coef,
            "se": se,
            "z": z,
            "p": p,
            "ic_inf": ic_inf,
            "ic_sup": ic_sup,
        },
        index=params.index,
    )


def wald(
    params: pd.Series,
    cov: pd.DataFrame,
    R: np.ndarray,
    r: np.ndarray | None = None,
) -> dict:
    """Prueba de Wald: W = (Rb - r)'(RVR')^-1 (Rb - r) ~ chi2(q).

    Returns
    -------
    dict
        {"stat": W, "df": q, "p": 1 - chi2.cdf(W, q)}
    """
    R = np.asarray(R, dtype=float)
    b = params.to_numpy()
    if r is None:
        r = np.zeros(R.shape[0])
    r = np.asarray(r, dtype=float)
    Rb_r = R @ b - r
    RVR = R @ cov.to_numpy() @ R.T
    W = float(Rb_r @ np.linalg.solve(RVR, Rb_r))
    q = int(R.shape[0])
    p = float(1.0 - chi2.cdf(W, q))
    return {"stat": W, "df": q, "p": p}


def long_run(
    params: pd.Series,
    cov: pd.DataFrame,
    term: str,
    lag_term: str = "y_lag",
    min_gap: float = LONGRUN_MIN_GAP,
) -> dict:
    """Efecto de largo plazo b / (1 - rho) con método delta.

    Si 1 - rho <= min_gap: {"reported": False, "reason": "1 - rho <= 0.05"}.
    Si no: estimate, se, z, p e IC 95 %.
    """
    rho = float(params[lag_term])
    b = float(params[term])
    if 1.0 - rho <= min_gap:
        return {"reported": False, "reason": f"1 - rho <= {min_gap}"}
    estimate = b / (1.0 - rho)
    grad = np.array([1.0 / (1.0 - rho), b / (1.0 - rho) ** 2])
    V_sub = cov.loc[[term, lag_term], [term, lag_term]].to_numpy()
    se = float(np.sqrt(grad @ V_sub @ grad))
    z = estimate / se
    p = float(2.0 * (1.0 - norm.cdf(abs(z))))
    ic_inf = estimate - _Z_975 * se
    ic_sup = estimate + _Z_975 * se
    return {
        "reported": True,
        "estimate": estimate,
        "se": se,
        "z": z,
        "p": p,
        "ic_inf": ic_inf,
        "ic_sup": ic_sup,
    }


def scale_effect(effect: dict, factor: float) -> dict:
    """Escala un efecto por un factor (p. ej. 1 DE).

    Multiplica estimate, se, ic_inf e ic_sup por factor.
    Si factor == 0: {"reported": False, "reason": "no definido"}.
    """
    if factor == 0:
        return {"reported": False, "reason": "no definido"}
    return {
        "reported": True,
        "estimate": effect["estimate"] * factor,
        "se": effect["se"] * factor,
        "ic_inf": effect["ic_inf"] * factor,
        "ic_sup": effect["ic_sup"] * factor,
    }


# --- Efectos por 1 DE ---


def standardization_sd(design: Design) -> pd.Series:
    """DE (ddof=1) de cada regresor macro en la muestra principal.

    Excluye 2020T2–2021T1 (C1): los trimestres con dummy de impulso.
    Solo columnas de MACRO_TERMS.keys(); devuelve Series indexada por término.
    """
    covid = [pd.Period(q, "Q-DEC") for q in COVID_QUARTERS]
    mask = ~design.X.index.isin(covid)
    sds: dict[str, float] = {}
    for term in MACRO_TERMS:
        if term in design.X.columns:
            sds[term] = float(design.X.loc[mask, term].std(ddof=1))
    return pd.Series(sds)


# --- Control de grados de libertad ---


def check_dof(design: Design) -> str | None:
    """Verifica grados de libertad y rango de X (RF-6).

    Returns
    -------
    str | None
        Motivo del problema, o None si está bien.
    """
    nobs = int(design.y.shape[0])
    k = int(design.X.shape[1])
    if nobs - k < MIN_DOF:
        return "grados de libertad insuficientes (< 30)"
    if np.linalg.matrix_rank(design.X.to_numpy()) < k:
        return "matriz de regresores de rango incompleto"
    return None
