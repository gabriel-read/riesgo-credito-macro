"""Pronósticos y validación fuera de muestra del Modelo I (spec 003).

Pronóstico a un paso y dinámico, reconstrucción del nivel desde diferencias,
comparador ingenuo (paseo aleatorio), RMSE, MAE y prueba de Diebold-Mariano con
la corrección de Harvey, Leybourne y Newbold (HLN). Sin acceso a red, disco ni
gráficos (RNF-6). RF-18, RNF-3.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from src.model1_config import ALPHA

_MODES = ("one_step", "dynamic")
_FORMS = ("nivel", "primera diferencia")


def _check_mode(mode: str) -> None:
    if mode not in _MODES:
        raise ValueError(f"modo desconocido '{mode}': usa 'one_step' o 'dynamic'")


def _check_columns(params: pd.Series, X_test: pd.DataFrame) -> None:
    missing = [c for c in params.index if c not in X_test.columns]
    if missing:
        raise ValueError(f"X_test no tiene las columnas de params: {missing}")


# --- Pronósticos ---


def one_step(params: pd.Series, X_test: pd.DataFrame) -> pd.Series:
    """Pronóstico a un paso: X_test @ params, con y_lag observado en X_test.

    Las columnas de X_test se ordenan como params; error si falta alguna.
    """
    _check_columns(params, X_test)
    pred = X_test[list(params.index)].to_numpy(dtype=float) @ params.to_numpy(dtype=float)
    return pd.Series(pred, index=X_test.index, name="pred")


def dynamic(params: pd.Series, X_test: pd.DataFrame, y_anchor: float) -> pd.Series:
    """Pronóstico dinámico: encadena ŷ(t−1) en y_lag.

    y_lag(primer trimestre) = y_anchor, la Y observada en el trimestre ancla en la
    forma del modelo (con Y en diferencias, ΔDR del ancla, no el nivel). Después
    y_lag(t) = ŷ(t−1). Se ignora la columna y_lag de X_test.
    """
    if "y_lag" not in params.index:
        raise ValueError("params no tiene el término 'y_lag': el dinámico lo necesita")
    _check_columns(params, X_test)
    cols = list(params.index)
    b = params.to_numpy(dtype=float)
    j = cols.index("y_lag")
    X = X_test[cols].to_numpy(dtype=float).copy()
    pred = np.empty(len(X))
    y_prev = float(y_anchor)
    for t in range(len(X)):
        X[t, j] = y_prev
        pred[t] = X[t] @ b
        y_prev = pred[t]
    return pd.Series(pred, index=X_test.index, name="pred")


# --- Nivel y comparador ingenuo ---


def to_level(
    pred: pd.Series,
    form: str,
    level_obs: pd.Series,
    anchor: pd.Period,
    mode: str,
) -> pd.Series:
    """Reconstruye el nivel de la morosidad (pp) a partir del pronóstico de Y.

    - form "nivel": el pronóstico ya es el nivel.
    - form "primera diferencia", "one_step": DR_obs(t−1) + ΔŶ(t).
    - form "primera diferencia", "dynamic": DR_obs(ancla) + suma acumulada de ΔŶ.
    """
    _check_mode(mode)
    if form not in _FORMS:
        raise ValueError(f"forma desconocida '{form}': usa 'nivel' o 'primera diferencia'")
    if form == "nivel":
        return pred.copy()
    if mode == "one_step":
        prev = np.array([level_obs.loc[t - 1] for t in pred.index], dtype=float)
        return pd.Series(prev + pred.to_numpy(dtype=float), index=pred.index, name="level")
    base = float(level_obs.loc[anchor])
    return pd.Series(base + np.cumsum(pred.to_numpy(dtype=float)), index=pred.index, name="level")


def naive(
    level_obs: pd.Series, test_index: pd.PeriodIndex, anchor: pd.Period, mode: str
) -> pd.Series:
    """Paseo aleatorio: a un paso, DR_obs(t−1); dinámico, DR_obs(ancla) constante."""
    _check_mode(mode)
    if mode == "one_step":
        vals = [float(level_obs.loc[t - 1]) for t in test_index]
    else:
        vals = [float(level_obs.loc[anchor])] * len(test_index)
    return pd.Series(vals, index=test_index, name="naive")


# --- Métricas ---


def rmse(e) -> float:
    """Raíz del error cuadrático medio."""
    a = np.asarray(e, dtype=float)
    return float(np.sqrt(np.mean(a**2)))


def mae(e) -> float:
    """Error absoluto medio."""
    a = np.asarray(e, dtype=float)
    return float(np.mean(np.abs(a)))


# --- Diebold-Mariano con corrección HLN ---


def diebold_mariano_hln(e_model: pd.Series, e_naive: pd.Series, h: int = 1) -> dict:
    """Prueba de Diebold-Mariano con corrección HLN (pérdida cuadrática, bilateral).

    e = observado − pronóstico (nivel, pp); d = e_modelo² − e_ingenuo² (DM < 0: el
    modelo pierde menos). γ̂k con divisor n; varianza de d̄ = (γ̂0 + 2·Σ_{k<h} γ̂k)/n,
    que con h = 1 es γ̂0/n. DM = d̄/√varianza. Corrección HLN:
    DM* = DM·√((n + 1 − 2h + h(h−1)/n)/n); p bilateral con t(n−1).

    Si la varianza es no positiva (por ejemplo, errores idénticos), devuelve NaN.

    Returns
    -------
    dict
        {"n", "dm" (sin corregir), "stat" (DM*), "p"}
    """
    a = np.asarray(e_model, dtype=float)
    b = np.asarray(e_naive, dtype=float)
    if a.shape != b.shape:
        raise ValueError(f"las series de error deben tener la misma longitud ({a.size} y {b.size})")
    n = a.size
    if n < 2:
        raise ValueError("Diebold-Mariano necesita al menos 2 observaciones")
    d = a**2 - b**2
    dc = d - d.mean()
    gammas = [float(np.sum(dc[k:] * dc[: n - k]) / n) for k in range(h)]
    var_dbar = (gammas[0] + 2.0 * sum(gammas[1:])) / n
    if not var_dbar > 0:
        return {"n": n, "dm": float("nan"), "stat": float("nan"), "p": float("nan")}
    dm = float(d.mean() / np.sqrt(var_dbar))
    factor = np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    stat = float(dm * factor)
    p = float(2.0 * stats.t.sf(abs(stat), n - 1))
    return {"n": n, "dm": dm, "stat": stat, "p": p}


# --- Veredictos pre-registrados ---


def oos_verdicts(ratio_one: float, ratio_dyn: float, dm_p: float) -> dict:
    """Veredictos pre-registrados de la validación fuera de muestra.

    - «supera al ingenuo» si el cociente RMSE modelo/ingenuo es < 1; si no, «no supera».
    - A un paso, «significativo» si DM tiene p < 0,05; si no (o si p es NaN), «no significativo».
    """
    return {
        "veredicto_un_paso": "supera al ingenuo" if ratio_one < 1.0 else "no supera al ingenuo",
        "veredicto_dinamico": "supera al ingenuo" if ratio_dyn < 1.0 else "no supera al ingenuo",
        "significancia_un_paso": "significativo" if dm_p < ALPHA else "no significativo",
    }
