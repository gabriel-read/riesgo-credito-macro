"""Orquestación pura del Modelo I (spec 003).

Tarea 5: estimación principal, tabla de coeficientes, tabla de efectos (impacto y
largo plazo, por 1 pp y por 1 DE) y tabla de estacionariedad del modelo. Las tareas
6 y 7 añadirán robusteces, limitaciones, desviaciones, exportación y fuera de muestra.
Sin acceso a red, disco ni gráficos (RNF-6). RF-3, RF-4, RF-7, RF-9, RF-10, RF-15.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.design import Design, ModelDataError, build_design, check_expected_forms, read_decisions
from src.estimation import (
    Fit,
    _impulse_dummy_cols,
    check_dof,
    fit_ols_hac,
    inference,
    long_run,
    scale_effect,
    standardization_sd,
)
from src.model1_config import EXPECTED_FORMS, EXPECTED_SIGN, MACRO_TERMS, MAIN, MAIN_START, TERM_LABELS
from src.stationarity import decide, is_stationary
from src.tables import quarter_label

LONG_RUN_NOT_REPORTED = "no reportado (1 − ρ ≤ 0,05)"
UNDEFINED = "no definido"
IMPULSE_SE_NOTE = "EE HAC no informativo: dummy de impulso con residuo nulo"
RANK_NOTE = "rango reducido por dummies de impulso (esperado)"
_SIGN_SYMBOL = {"+": "+", "-": "−"}


@dataclass(frozen=True)
class Model1Result:
    """Resultado de la estimación principal del Modelo I (tarea 5).

    Las tareas 6 y 7 añadirán campos (diagnósticos, robusteces, fuera de muestra, etc.).
    """

    decisions: dict[str, str]
    design: Design
    fit: Fit
    coefficients: pd.DataFrame
    coef_footer: dict
    effects: pd.DataFrame
    stationarity: pd.DataFrame


# --- Etiquetas y signos ---


def term_label(term: str) -> str:
    """Etiqueta en español de un término del modelo (incluidas las dummies)."""
    if term in TERM_LABELS:
        return TERM_LABELS[term]
    if term.startswith("covid_"):
        year, q = term.removeprefix("covid_").split("q")
        return f"Dummy COVID {year}T{q}"
    if term.startswith("seasonal_q"):
        return f"Dummy estacional T{term.removeprefix('seasonal_q')}"
    return term


def sign_match(expected: str | None, coef: float) -> str:
    """Compara el signo estimado con el esperado: «sí», «no» o «sin contraste»."""
    if expected is None:
        return "sin contraste"
    if expected == "+":
        return "sí" if coef > 0 else "no"
    if expected == "-":
        return "sí" if coef < 0 else "no"
    raise ValueError(f"signo esperado desconocido: {expected!r}")


# --- Tabla de coeficientes (RF-9) ---


def coefficient_table(fit: Fit) -> tuple[pd.DataFrame, dict]:
    """Tabla de coeficientes con inferencia normal HAC y pie de la tabla (RF-9).

    Una fila por término. Las filas de las dummies de impulso llevan la nota de que su
    error HAC no es informativo (C3).
    """
    inf = inference(fit.params, fit.cov)
    impulse = set(_impulse_dummy_cols(fit.design.X))
    rows = []
    for term in fit.params.index:
        expected = EXPECTED_SIGN.get(term)
        coef = float(inf.loc[term, "coef"])
        rows.append(
            {
                "termino": term,
                "etiqueta": term_label(term),
                "coef": coef,
                "ee_hac": float(inf.loc[term, "se"]),
                "z": float(inf.loc[term, "z"]),
                "p": float(inf.loc[term, "p"]),
                "ic_inf": float(inf.loc[term, "ic_inf"]),
                "ic_sup": float(inf.loc[term, "ic_sup"]),
                "signo_esperado": _SIGN_SYMBOL.get(expected, "sin contraste"),
                "coincide": sign_match(expected, coef),
                "nota": IMPULSE_SE_NOTE if term in impulse else "",
            }
        )
    index = fit.design.X.index
    footer = {
        "forma_y": fit.design.form,
        "muestra_inicio": quarter_label(index.min()),
        "muestra_fin": quarter_label(index.max()),
        "n_obs": int(fit.nobs),
        "n_parametros": int(fit.k),
        "r2": float(fit.rsquared),
        "r2_ajustado": float(fit.rsquared_adj),
        "ee_regresion": float(fit.ser),
        "rezagos_hac": int(fit.hac_lags),
        "truncamiento_espectral": bool(fit.psd_adjusted),
        "nota_rango": RANK_NOTE if impulse else "",
    }
    return pd.DataFrame(rows), footer


# --- Tabla de efectos (RF-10) ---


def _effect_row(term: str, efecto: str, escala: str, eff: dict, estado: str) -> dict:
    reported = bool(eff.get("reported", False))
    unit = f"pp de morosidad por 1 {'DE' if escala == 'por 1 DE' else 'pp'} del regresor"
    return {
        "termino": term,
        "etiqueta": term_label(term),
        "efecto": efecto,
        "escala": escala,
        "estimacion": eff["estimate"] if reported else np.nan,
        "ee": eff["se"] if reported else np.nan,
        "p": eff["p"] if reported else np.nan,
        "ic_inf": eff["ic_inf"] if reported else np.nan,
        "ic_sup": eff["ic_sup"] if reported else np.nan,
        "estado": estado,
        "unidad": unit,
    }


def effects_table(fit: Fit) -> pd.DataFrame:
    """Efectos de impacto y de largo plazo de los 5 regresores macro (RF-10).

    Impacto = β (error HAC); largo plazo = β/(1 − ρ) (error por método delta). Cada uno por
    1 pp del regresor y por 1 DE (DE con divisor n − 1 sin 2020T2–2021T1, C1), en pp de
    morosidad. Si 1 − ρ ≤ 0,05 solo se reporta el impacto; si la DE es 0 o no existe, el
    efecto por 1 DE figura como «no definido».
    """
    inf = inference(fit.params, fit.cov)
    sds = standardization_sd(fit.design)
    rows = []
    for term in MACRO_TERMS:
        if term not in fit.params.index:
            continue
        impact = {
            "reported": True,
            "estimate": float(inf.loc[term, "coef"]),
            "se": float(inf.loc[term, "se"]),
            "p": float(inf.loc[term, "p"]),
            "ic_inf": float(inf.loc[term, "ic_inf"]),
            "ic_sup": float(inf.loc[term, "ic_sup"]),
        }
        long = long_run(fit.params, fit.cov, term)
        sd = float(sds.get(term, np.nan))
        sd_defined = bool(np.isfinite(sd) and sd != 0.0)
        for efecto, eff in (("impacto", impact), ("largo plazo", long)):
            if not eff["reported"]:  # 1 − ρ ≤ 0,05 (solo el largo plazo)
                for escala in ("por 1 pp", "por 1 DE"):
                    rows.append(_effect_row(term, efecto, escala, eff, LONG_RUN_NOT_REPORTED))
                continue
            rows.append(_effect_row(term, efecto, "por 1 pp", eff, "reportado"))
            if sd_defined:
                scaled = scale_effect(eff, sd)
                scaled["p"] = eff["p"]  # el p-valor no depende de la escala
                rows.append(_effect_row(term, efecto, "por 1 DE", scaled, "reportado"))
            else:
                rows.append(_effect_row(term, efecto, "por 1 DE", {"reported": False}, UNDEFINED))
    return pd.DataFrame(rows)


# --- Tabla de estacionariedad del modelo (RF-15) ---


def _stationarity_source(column: str) -> tuple[str, str]:
    """Variable de la tabla de la spec 001 y forma en que entra la columna del panel."""
    if column.endswith("_d"):
        return column[: -len("_d")], "primera diferencia"
    return column, "tal cual"


def _table_row(stationarity: pd.DataFrame, variable: str, forma: str) -> pd.Series:
    sel = stationarity[(stationarity["variable"] == variable) & (stationarity["forma"] == forma)]
    if sel.empty:
        raise ModelDataError(f"{variable}: no hay fila '{forma}' en la tabla de estacionariedad")
    return sel.iloc[0]


def _stationarity_row(termino: str, panel_column: str, variable: str, forma: str,
                      stationarity: pd.DataFrame, nota: str = "") -> dict:
    src = _table_row(stationarity, variable, forma)
    if forma == "tal cual":
        decision, orden = str(src["decision"]), str(src["orden"])
    else:
        # En primera diferencia la tabla no trae decisión: se aplica la regla de la spec 001
        # a esa fila. «niveles» = la serie es estacionaria en la forma en que entra.
        decision = decide(float(src["adf_p"]), float(src["kpss_p"]))
        orden = "I(0)" if is_stationary(float(src["adf_p"]), float(src["kpss_p"])) else "no I(0)"
        nota = (nota + "; " if nota else "") + (
            "regla de la spec 001 aplicada a la fila «primera diferencia»; "
            "«niveles» = estacionaria en la forma en que entra"
        )
    return {
        "termino": termino,
        "etiqueta": term_label(termino) if termino != "Y" else "Y(t) — dependiente (DRALACBS)",
        "columna_panel": panel_column,
        "forma": "nivel" if forma == "tal cual" and termino in ("Y", "y_lag") else forma,
        "adf_stat": float(src["adf_stat"]),
        "adf_p": float(src["adf_p"]),
        "kpss_stat": float(src["kpss_stat"]),
        "kpss_p": float(src["kpss_p"]),
        "decision": decision,
        "orden": orden,
        "no_i0": "no" if orden == "I(0)" else "sí",
        "nota": nota,
    }


def model_stationarity_table(
    stationarity: pd.DataFrame, decisions: dict[str, str], dependent: str = "dralacbs"
) -> pd.DataFrame:
    """ADF/KPSS de la dependiente, su rezago y los 5 regresores, en la forma en que entran (RF-15).

    Los estadísticos se copian de la tabla de la spec 001 (no se recalculan). La dependiente y
    su rezago, si entran en Δ, se juzgan con la fila «primera diferencia» (no con la «tal
    cual», que daría «ambigua»). ΔU y ΔFFR usan las filas «primera diferencia» de `unrate` y
    `fedfunds`. CRED(t−4) usa la serie `loans_yoy` sin rezagar (el rezago no cambia sus
    propiedades). La marca «no I(0)» alimenta la tabla de limitaciones (RF-20).
    """
    y_forma = "tal cual" if decisions[dependent] == "niveles" else "primera diferencia"
    rows = [
        _stationarity_row("Y", dependent, dependent, y_forma, stationarity),
        _stationarity_row("y_lag", dependent, dependent, y_forma, stationarity,
                          "mismo proceso que Y, rezagado un trimestre"),
    ]
    for term, column in MACRO_TERMS.items():
        variable, forma = _stationarity_source(column)
        nota = "ADF/KPSS de loans_yoy sin rezagar" if term == "credit_growth" else ""
        rows.append(_stationarity_row(term, variable, variable, forma, stationarity, nota))
    return pd.DataFrame(rows)


# --- Estimación principal (RF-3, RF-4, RF-7) ---


def run_model1(full: pd.DataFrame, stationarity: pd.DataFrame, end: pd.Period) -> Model1Result:
    """Estima la especificación principal y construye las tablas de la tarea 5.

    1. Lee las decisiones y comprueba las formas esperadas (RF-3, RF-4) antes de estimar nada.
    2. Construye el diseño de la muestra principal estricta, 2000T1–`end` (RF-1).
    3. Si la principal no tiene grados de libertad suficientes o X no tiene rango completo,
       se detiene (RF-6).
    4. Estima por MCO con errores Newey-West (RF-7) y construye las tablas.
    """
    decisions = read_decisions(stationarity)
    check_expected_forms(decisions, EXPECTED_FORMS)
    design = build_design(full, MAIN, decisions[MAIN.dependent], end)
    first, last = design.X.index[0], design.X.index[-1]
    if first != MAIN_START or last != end:
        raise ModelDataError(
            f"principal: la muestra es {quarter_label(first)}–{quarter_label(last)} y debe ser "
            f"{quarter_label(MAIN_START)}–{quarter_label(end)} (RF-1)"
        )
    reason = check_dof(design)
    if reason:
        raise ModelDataError(f"principal: {reason}")
    fit = fit_ols_hac(design)
    coefficients, footer = coefficient_table(fit)
    return Model1Result(
        decisions=decisions,
        design=design,
        fit=fit,
        coefficients=coefficients,
        coef_footer=footer,
        effects=effects_table(fit),
        stationarity=model_stationarity_table(stationarity, decisions, MAIN.dependent),
    )
