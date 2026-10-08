"""Funciones puras de diagnóstico del Modelo I (spec 003).

Breusch-Godfrey, Breusch-Pagan (Koenker), White, Jarque-Bera, RESET,
VIF, Chow como Wald HAC y CUSUM. Sin acceso a red, disco ni gráficos
(RNF-6). RF-12 a RF-14.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.linalg import qr
from scipy.stats import chi2
from statsmodels.stats.diagnostic import (
    acorr_breusch_godfrey,
    het_breuschpagan,
    linear_reset,
    recursive_olsresiduals,
)
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import jarque_bera

from src.design import Design
from src.estimation import Fit, fit_ols_hac, wald
from src.tables import quarter_label
from src.model1_config import (
    ALPHA,
    BG_LAGS,
    CHOW_BREAKS,
    CHOW_SIZE_CAUTION_BREAKS,
    MACRO_TERMS,
    MIN_DOF,
    PSD_REL_TOL,
    VIF_ALERT,
)


# --- Veredicto ---


def _veredicto(p: float, alpha: float = ALPHA) -> str:
    """Veredicto de diagnóstico: «pasa» si p >= alpha, «falla» si p < alpha."""
    return "pasa" if p >= alpha else "falla"


# --- Breusch-Godfrey ---


def breusch_godfrey(fit: Fit, nlags: int = BG_LAGS) -> dict:
    """Prueba de Breusch-Godfrey para autocorrelación de los residuos.

    LM ~ chi2(nlags). H0: no hay autocorrelación de orden nlags.

    Returns
    -------
    dict
        {"stat": LM, "df": nlags, "p": p_valor, "veredicto": "pasa"/"falla"}
    """
    lm, lm_p, _, _ = acorr_breusch_godfrey(fit.sm_result, nlags, result_object=False)
    return {
        "stat": float(lm),
        "df": int(nlags),
        "p": float(lm_p),
        "veredicto": _veredicto(float(lm_p)),
    }


# --- Breusch-Pagan (Koenker) ---


def breusch_pagan(fit: Fit) -> dict:
    """Prueba de Breusch-Pagan (Koenker) para heterocedasticidad.

    LM ~ chi2(rank(X) - 1). H0: homocedasticidad.

    Returns
    -------
    dict
        {"stat": LM, "df": rank(X)-1, "p": p_valor, "veredicto": "pasa"/"falla"}
    """
    x = fit.design.X
    rank = int(np.linalg.matrix_rank(x.to_numpy()))
    lm, lm_p, _, _ = het_breuschpagan(fit.resid, x, robust=True)
    return {
        "stat": float(lm),
        "df": rank - 1,
        "p": float(lm_p),
        "veredicto": _veredicto(float(lm_p)),
    }


# --- White (implementación propia, D5) ---


def _white_aux_matrix(X: pd.DataFrame) -> np.ndarray:
    """Construye la matriz auxiliar de White con eliminación por rango.

    Z_aux = [const, X, X², productos cruzados de columnas no constantes].
    Elimina colinealidad por rango con QR con pivoteo de columnas sobre las
    columnas no constantes; la constante siempre se conserva. Así caen los
    cuadrados de las dummies, los productos entre dummies y los productos
    dummy de impulso × regresor (proporcionales a la dummy).

    Returns
    -------
    np.ndarray
        Matriz Z_aux de rango completo (columna 0 = constante).
    """
    cols = [c for c in X.columns if c != "const"]
    n = X.shape[0]

    # Columnas no constantes: X, cuadrados, productos cruzados
    z_dict: dict[str, np.ndarray] = {}
    for c in cols:
        z_dict[c] = X[c].to_numpy(dtype=float)
    for c in cols:
        z_dict[f"{c}²"] = X[c].to_numpy(dtype=float) ** 2
    for i, c1 in enumerate(cols):
        for c2 in cols[i + 1 :]:
            z_dict[f"{c1}×{c2}"] = X[c1].to_numpy(dtype=float) * X[c2].to_numpy(dtype=float)

    Z_nc = pd.DataFrame(z_dict, index=X.index)

    # QR con pivoteo para eliminar colinealidad por rango
    # (modo económico: con más columnas que observaciones R es de min(n, m) × m y su diagonal solo
    # tiene min(n, m) pasos de pivoteo; las columnas más allá del rango posible no se conservan)
    # Con más columnas que observaciones menos una, la constante más las conservadas excedería n:
    # se pivotea sobre columnas centradas, de modo que [const, conservadas] tenga rango completo.
    pivot_on = Z_nc.to_numpy()
    if Z_nc.shape[1] > n - 1:
        pivot_on = pivot_on - pivot_on.mean(axis=0)
    _, R, P = qr(pivot_on, mode="economic", pivoting=True)
    diag = np.abs(np.diag(R))
    tol = PSD_REL_TOL * diag[0] if diag[0] > 0 else 0.0
    keep = diag > tol
    kept_cols = [Z_nc.columns[P[j]] for j in range(len(diag)) if keep[j]]

    # Z_aux = [const, columnas conservadas]
    return np.column_stack([np.ones(n), Z_nc[kept_cols].to_numpy()])


def white(fit: Fit) -> dict:
    """Prueba de White para heterocedasticidad (implementación propia, D5).

    Auxiliar: e² ~ const + X + X² + productos cruzados.
    Elimina colinealidad por rango (QR con pivoteo).
    LM = n·R²_aux ~ chi2(rango(Z_aux) - 1).

    Regla C1 (spec 004): si n − rango(Z_aux) < MIN_DOF (30), la prueba es «no calculable»: con tan
    pocos grados de libertad la auxiliar se satura y el contraste no tiene potencia. No hay estadístico,
    p-valor ni veredicto, solo el motivo.

    Returns
    -------
    dict
        {"stat": LM, "df": rango-1, "p": p_valor, "veredicto": "pasa"/"falla", "calculable": True}
        o, si no es calculable, {"stat": None, "df": None, "p": None, "veredicto": None,
        "calculable": False, "motivo": ...}
    """
    e = fit.resid.to_numpy(dtype=float)
    X = fit.design.X
    n = len(e)

    Z_aux = _white_aux_matrix(X)
    if n - Z_aux.shape[1] < MIN_DOF:
        return {
            "stat": None, "df": None, "p": None, "veredicto": None, "calculable": False,
            "motivo": (f"n − rango(Z_aux) = {n} − {Z_aux.shape[1]} = {n - Z_aux.shape[1]} < {MIN_DOF}: "
                       "la regresión auxiliar de White queda sin grados de libertad suficientes"),
        }

    # Regresión auxiliar: e² ~ Z_aux
    e2 = e**2
    beta = np.linalg.lstsq(Z_aux, e2, rcond=None)[0]
    fitted = Z_aux @ beta
    ss_res = float(np.sum((e2 - fitted) ** 2))
    ss_tot = float(np.sum((e2 - e2.mean()) ** 2))
    r2_aux = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    rank = Z_aux.shape[1]
    lm = n * r2_aux
    df = rank - 1
    p = float(1.0 - chi2.cdf(lm, df))

    return {
        "stat": float(lm),
        "df": int(df),
        "p": p,
        "veredicto": _veredicto(p),
        "calculable": True,
    }


# --- Jarque-Bera ---


def jarque_bera_test(fit: Fit) -> dict:
    """Prueba de Jarque-Bera para normalidad de los residuos.

    JB ~ chi2(2). H0: normalidad.

    Returns
    -------
    dict
        {"stat": JB, "df": 2, "p": p_valor, "veredicto": "pasa"/"falla"}
    """
    jb, p, _, _ = jarque_bera(fit.resid)
    return {
        "stat": float(jb),
        "df": 2,
        "p": float(p),
        "veredicto": _veredicto(float(p)),
    }


# --- RESET de Ramsey ---


def reset(fit: Fit) -> dict:
    """Prueba de RESET de Ramsey (power=3, fitted, F).

    H0: especificación correcta.

    Returns
    -------
    dict
        {"stat": F, "df_num": 2, "df_den": nobs - k - 2, "p": p_valor,
         "veredicto": "pasa"/"falla"}
    """
    res = linear_reset(
        fit.sm_result, power=3, test_type="fitted", use_f=True, cov_type="nonrobust"
    )
    f_stat = float(res.fvalue if hasattr(res, "fvalue") else res.statistic)
    p_val = float(res.pvalue)
    return {
        "stat": f_stat,
        "df_num": int(res.df_num),
        "df_den": int(res.df_denom),
        "p": p_val,
        "veredicto": _veredicto(p_val),
    }


# --- VIF ---


def vif(fit: Fit, terms: list[str] | None = None) -> pd.DataFrame:
    """Factor de inflación de la varianza (VIF) para y_lag y los 5 términos macro.

    Con `terms` (spec 004) calcula el VIF de esos términos, en ese orden, en lugar de los del
    Modelo I. VIF > VIF_ALERT → «alerta»; si no, «sin alerta».

    Returns
    -------
    pd.DataFrame
        Filas: y_lag y 5 términos macro. Columnas: term, vif, veredicto.
    """
    X = fit.design.X
    if terms is None:
        terms = ["y_lag"] + list(MACRO_TERMS.keys())
    terms = [t for t in terms if t in X.columns]

    X_np = X.to_numpy(dtype=float)
    col_idx = {c: i for i, c in enumerate(X.columns)}

    rows = []
    for term in terms:
        idx = col_idx[term]
        vif_val = float(variance_inflation_factor(X_np, idx))
        rows.append(
            {
                "term": term,
                "vif": vif_val,
                "veredicto": "alerta" if vif_val > VIF_ALERT else "sin alerta",
            }
        )

    return pd.DataFrame(rows)


# --- Dummies de impulso ---


def _impulse_columns(X: pd.DataFrame) -> list[str]:
    """Columnas de dummy de impulso: valores en {0, 1} con exactamente un 1."""
    return [
        c
        for c in X.columns
        if set(np.unique(X[c].to_numpy(dtype=float))) <= {0.0, 1.0} and float(X[c].sum()) == 1.0
    ]


# --- Chow como Wald HAC (D6) ---


def chow_wald(fit: Fit, break_q: str) -> dict:
    """Prueba de Chow como Wald HAC sobre una regresión ampliada con interacciones.

    Reestima sobre la misma muestra con X + post·[const, y_lag, 5 macro]
    (post = 1{t >= break_q}). Mismas dummies COVID (sin interactuar), misma
    ventana HAC. Wald H0: las 7 interacciones = 0 con el bloque de V tratado
    como en fit_ols_hac (truncamiento + rango reducido dummies impulso).
    chi2(7).

    Spec 004: el rango de la matriz ampliada se comprueba ANTES de estimar (con la tolerancia por
    defecto de np.linalg.matrix_rank); si es incompleto devuelve calculable = False con su motivo, sin
    estadístico, p-valor ni veredicto, y no llama a fit_ols_hac ni a wald. Añade los trimestres útiles
    anteriores al quiebre (n_pre, n_pre_util).

    Returns
    -------
    dict
        {"stat": W, "df": q, "p": p_valor, "veredicto": "pasa"/"falla", "nota": ...,
         "n_post", "n_post_util", "n_pre", "n_pre_util", "calculable": True}
    """
    break_period = pd.Period(break_q, "Q-DEC")
    X = fit.design.X
    y = fit.design.y

    # post = 1{t >= break_q}
    post = (X.index >= break_period).astype(float)

    # Trimestres posteriores al quiebre y los que sobreviven a las dummies de impulso
    impulse_cols = _impulse_columns(X)
    n_post = int(post.sum())
    n_pre = int(len(post) - n_post)
    absorbed = sum(1 for c in impulse_cols if post[int(np.argmax(X[c].to_numpy()))] > 0)
    absorbed_pre = len(impulse_cols) - absorbed

    # Interacciones: post * cada columna de X que no es dummy de impulso
    # (en la principal: const, y_lag y los 5 términos macro)
    impulse = set(_impulse_columns(X))
    interact_cols = [c for c in X.columns if c not in impulse]
    X_aug = X.copy()
    for c in interact_cols:
        X_aug[f"post×{c}"] = post * X[c]

    counts = {
        "n_post": n_post, "n_post_util": n_post - absorbed,
        "n_pre": n_pre, "n_pre_util": n_pre - absorbed_pre,
    }
    q = len(interact_cols)
    rank = int(np.linalg.matrix_rank(X_aug.to_numpy(dtype=float)))
    if rank < X_aug.shape[1]:
        return {
            "stat": None, "df": q, "p": None, "veredicto": None, "calculable": False,
            "motivo": (f"rango incompleto de la matriz ampliada ({rank} de {X_aug.shape[1]} columnas): "
                       "alguna interacción es colineal"),
            "nota": "", **counts,
        }

    # Crear Design ampliado
    design_aug = Design(
        y=y,
        X=X_aug,
        form=fit.design.form,
        start=fit.design.start,
        end=fit.design.end,
        spec_id=f"{fit.design.spec_id}_chow_{break_q}",
        dropped=fit.design.dropped,
    )

    fit_aug = fit_ols_hac(design_aug)

    # Wald H0: todas las interacciones = 0
    k = X.shape[1]
    R = np.zeros((q, k + q))
    R[:, k:] = np.eye(q)

    result = dict(wald(fit_aug.params, fit_aug.cov, R))
    result["veredicto"] = _veredicto(float(result["p"]))
    result.update(counts)
    result["calculable"] = True
    result["nota"] = (
        "Wald HAC con interacciones de la constante, ρ y β₁–β₅; "
        "dummies COVID sin interactuar"
    )
    return result


# --- CUSUM (D7) ---


def cusum(fit: Fit) -> dict:
    """CUSUM de residuos recursivos (Brown-Durbin-Evans) sobre la regresión reducida.

    La regresión reducida es el mismo y y X sin las columnas de dummies
    de impulso y sin sus trimestres (2020T2–2021T1). Sobre ella se llama a
    recursive_olsresiduals(OLS_reducida, skip=None, alpha=0.95).
    Veredicto «falla» si algún punto sale de las bandas.

    Returns
    -------
    dict
        {"veredicto": ..., "cusum": Series, "lower": Series, "upper": Series,
         "index": PeriodIndex, "nota": ...}
    """
    X = fit.design.X
    y = fit.design.y

    # Identificar dummies de impulso (valen 1 en exactamente una observación)
    impulse_cols = _impulse_columns(X)

    # Quitar trimestres con dummy de impulso y sus columnas
    if impulse_cols:
        mask = (X[impulse_cols] == 1.0).any(axis=1)
        X_reduced = X.loc[~mask].drop(columns=impulse_cols)
        y_reduced = y.loc[~mask]
    else:
        X_reduced = X
        y_reduced = y

    # Regresión reducida
    result = sm.OLS(y_reduced, X_reduced).fit()

    # Residuos recursivos
    # (statsmodels 0.15 devuelve 7 valores: rresid, rparams, rypred, rresid_standardized,
    # rvarraw, rcusum, rcusumci)
    _, _, _, _, _, rcusum, rcusumci = recursive_olsresiduals(result, skip=None, alpha=0.95)

    # rcusum arranca en la observación skip-1 (residuo del ajuste inicial, no recursivo);
    # rcusumci (forma (2, n − skip)) arranca en la observación skip. Se descarta el primer
    # punto de rcusum para alinear ambos con los trimestres skip, ..., n − 1.
    skip = X_reduced.shape[1]
    idx = X_reduced.index[skip:]
    cusum_series = pd.Series(np.asarray(rcusum)[1:], index=idx)
    lower = pd.Series(np.asarray(rcusumci)[0], index=idx)
    upper = pd.Series(np.asarray(rcusumci)[1], index=idx)

    # Veredicto
    outside = (cusum_series < lower) | (cusum_series > upper)
    veredicto = "falla" if outside.any() else "pasa"

    return {
        "veredicto": veredicto,
        "cusum": cusum_series,
        "lower": lower,
        "upper": upper,
        "index": idx,
        "nota": "los trimestres con dummy de impulso no aportan residuo recursivo",
    }


# --- Tabla de diagnósticos ---


def diagnostics_table(fit: Fit) -> pd.DataFrame:
    """Tabla de diagnósticos: una fila por prueba.

    Incluye: BG, BP, White, JB, RESET, VIF (una fila por término macro),
    Chow 2008T3, Chow 2020T2, CUSUM.

    Returns
    -------
    pd.DataFrame
        Columnas: prueba, estadístico, p_valor, veredicto, nota.
    """
    rows = []

    # BG
    bg = breusch_godfrey(fit)
    rows.append(
        {
            "prueba": "Breusch-Godfrey",
            "estadístico": bg["stat"],
            "p_valor": bg["p"],
            "veredicto": bg["veredicto"],
            "nota": "",
        }
    )

    # BP
    bp = breusch_pagan(fit)
    rows.append(
        {
            "prueba": "Breusch-Pagan",
            "estadístico": bp["stat"],
            "p_valor": bp["p"],
            "veredicto": bp["veredicto"],
            "nota": "",
        }
    )

    # White
    wh = white(fit)
    rows.append(
        {
            "prueba": "White",
            "estadístico": wh["stat"],
            "p_valor": wh["p"],
            "veredicto": wh["veredicto"],
            "nota": "",
        }
    )

    # JB
    jb = jarque_bera_test(fit)
    rows.append(
        {
            "prueba": "Jarque-Bera",
            "estadístico": jb["stat"],
            "p_valor": jb["p"],
            "veredicto": jb["veredicto"],
            "nota": "",
        }
    )

    # RESET
    rs = reset(fit)
    rows.append(
        {
            "prueba": "RESET",
            "estadístico": rs["stat"],
            "p_valor": rs["p"],
            "veredicto": rs["veredicto"],
            "nota": "",
        }
    )

    # VIF (una fila por término macro)
    vif_df = vif(fit)
    for _, row in vif_df.iterrows():
        rows.append(
            {
                "prueba": f"VIF ({row['term']})",
                "estadístico": row["vif"],
                "p_valor": np.nan,
                "veredicto": row["veredicto"],
                "nota": "",
            }
        )

    # Chow
    for break_q in CHOW_BREAKS:
        cw = chow_wald(fit, break_q)
        nota = cw["nota"]
        if break_q in CHOW_SIZE_CAUTION_BREAKS:
            nota += (
                f"; quedan {cw['n_post_util']} trimestres posteriores útiles para {cw['df']} "
                "restricciones: el tamaño empírico del contraste puede diferir del 5 % nominal"
            )
        rows.append(
            {
                "prueba": f"Chow {quarter_label(pd.Period(break_q, 'Q-DEC'))}",
                "estadístico": cw["stat"],
                "p_valor": cw["p"],
                "veredicto": cw["veredicto"],
                "nota": nota,
            }
        )

    # CUSUM
    cu = cusum(fit)
    rows.append(
        {
            "prueba": "CUSUM",
            "estadístico": np.nan,
            "p_valor": np.nan,
            "veredicto": cu["veredicto"],
            "nota": cu["nota"],
        }
    )

    return pd.DataFrame(rows)
