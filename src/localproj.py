"""Funciones puras de las proyecciones locales de Jordà del Modelo II (spec 004).

Una regresión por horizonte h = 0..12 para la respuesta de la morosidad (β_h) y de la tasa (φ_h),
horizonte de detección y comparación descriptiva con la respuesta acumulada R(h) del modelo de
rezagos distribuidos. Sin acceso a red, disco ni gráficos (RNF-7). RF-14 a RF-17.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.design2 import build_lp_design
from src.estimation import check_dof, fit_ols_hac, hac_lags
from src.model2_config import H_MAX, LP_BAND_Z

IDENTITY_NOTE = "por construcción (identidad)"


@dataclass(frozen=True)
class LPOutcome:
    """Resultado de una proyección local: el coeficiente de ΔFFR(t) con su error HAC y su banda."""

    h: int
    target: str
    estado: str                    # "estimada" | "no estimada" | "identidad"
    motivo: str
    coef: float | None
    ee: float | None
    ic90_inf: float | None
    ic90_sup: float | None
    n_obs: int | None
    rezagos_hac: int | None
    nota: str = ""


def local_projection(full: pd.DataFrame, K: int, h: int, decision: str,
                     window: tuple[pd.Period, pd.Period], end: pd.Period, target: str) -> LPOutcome:
    """Proyección local de horizonte h (RF-14 a RF-16).

    La proyección de la tasa en h = 0 es una identidad (FFR(t) − FFR(t−1) es el regresor ΔFFR(t)):
    no se estima y se reporta φ_0 = 1 sin error ni banda. Con menos de 30 grados de libertad o rango
    incompleto el horizonte es «no estimada» con su motivo. Ventana HAC: max(fórmula, h + 1).
    """
    if target == "tasa" and h == 0:
        return LPOutcome(h, target, "identidad", "", 1.0, None, None, None, None, None, IDENTITY_NOTE)
    design = build_lp_design(full, h, K, decision, window, end, target)
    n = int(design.y.shape[0])
    reason = check_dof(design)
    if reason:
        return LPOutcome(h, target, "no estimada", reason, None, None, None, None, n, None)
    fit = fit_ols_hac(design, maxlags=max(hac_lags(n), h + 1))
    coef = float(fit.params["d_ffr_l0"])
    ee = float(np.sqrt(fit.cov.loc["d_ffr_l0", "d_ffr_l0"]))
    return LPOutcome(h, target, "estimada", "", coef, ee, coef - LP_BAND_Z * ee, coef + LP_BAND_Z * ee,
                     n, fit.hac_lags)


def run_local_projections(full: pd.DataFrame, K: int, decision: str,
                          window: tuple[pd.Period, pd.Period], end: pd.Period) -> pd.DataFrame:
    """Una fila por h = 0..12 con β_h y φ_h, sus errores HAC, bandas del 90 %, muestra y estado."""
    rows = []
    for h in range(H_MAX + 1):
        m = local_projection(full, K, h, decision, window, end, "morosidad")
        r = local_projection(full, K, h, decision, window, end, "tasa")
        rows.append({
            "h": h,
            "beta": np.nan if m.coef is None else m.coef,
            "ee": np.nan if m.ee is None else m.ee,
            "ic90_inf": np.nan if m.ic90_inf is None else m.ic90_inf,
            "ic90_sup": np.nan if m.ic90_sup is None else m.ic90_sup,
            "n_obs": m.n_obs,
            "rezagos_hac": m.rezagos_hac,
            "estado": m.estado,
            "motivo": m.motivo,
            "phi": np.nan if r.coef is None else r.coef,
            "phi_ee": r.ee, "phi_ic90_inf": r.ic90_inf, "phi_ic90_sup": r.ic90_sup,
            "phi_nota": r.nota or r.motivo and f"no estimada: {r.motivo}" or "",
        })
    lp = pd.DataFrame(rows)
    for col in ("phi_ee", "phi_ic90_inf", "phi_ic90_sup"):
        lp[col] = pd.Series([row[col] for row in rows], dtype=object)   # None donde no hay valor
    return lp


def _band_excludes_zero(inf: float, sup: float) -> bool:
    return bool(inf > 0 or sup < 0)


def detection_horizon(lp: pd.DataFrame) -> str:
    """Primer h estimado cuya banda del 90 % de β_h excluye el cero («h2»); «ninguno» si no hay (RF-16)."""
    for _, row in lp.iterrows():
        if row["estado"] == "estimada" and _band_excludes_zero(row["ic90_inf"], row["ic90_sup"]):
            return f"h{int(row['h'])}"
    return "ninguno"


def compare_with_trajectory(trajectory: pd.DataFrame, lp: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Comparación descriptiva de R(h) con β_h y φ_h (RF-17).

    El recuento «k de n» cuenta los horizontes h = 1..12 estimados con el mismo signo (h = 0 queda
    fuera porque coincide por construcción).
    """
    rows = []
    same_count = 0
    n_count = 0
    for h in (int(v) for v in lp["h"]):
        r_h = float(trajectory.loc[trajectory["h"] == h, "R"].iloc[0])
        row = lp.loc[lp["h"] == h].iloc[0]
        if row["estado"] == "estimada":
            same = bool(np.sign(r_h) == np.sign(row["beta"]))
            excludes = _band_excludes_zero(row["ic90_inf"], row["ic90_sup"])
            if h >= 1:
                n_count += 1
                same_count += int(same)
            rows.append((h, r_h, float(row["beta"]), row["phi"], "sí" if same else "no",
                         "sí" if excludes else "no"))
        else:
            rows.append((h, r_h, np.nan, row["phi"], "—", "—"))
    table = pd.DataFrame(rows, columns=["h", "R", "beta", "phi", "mismo_signo", "banda_excluye_cero"])
    counts = {"k": same_count, "n": n_count, "k_de_n": f"{same_count} de {n_count}",
              "horizonte_deteccion": detection_horizon(lp)}
    return table, counts
