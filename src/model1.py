"""Orquestación pura del Modelo I (spec 003).

Tarea 5: estimación principal, tabla de coeficientes, tabla de efectos (impacto y
largo plazo, por 1 pp y por 1 DE) y tabla de estacionariedad del modelo.
Tarea 6: variantes de robustez R1–R8, criterio de robustez, conexión con los diagnósticos,
tablas de limitaciones y desviaciones, exportación para la spec 005 y salida en Markdown y CSV
como texto (la escritura a disco es de la etapa `models` del pipeline).
La tarea 7 añadirá el fuera de muestra.
Sin acceso a red, disco ni gráficos (RNF-6). RF-3 a RF-10, RF-15 a RF-17, RF-20, RF-21, RF-23.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.design import Design, ModelDataError, build_design, check_expected_forms, read_decisions
from src.diagnostics import cusum, diagnostics_table
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
from src.model1_config import (
    COVID_QUARTERS,
    EXPECTED_FORMS,
    EXPECTED_SIGN,
    FIXED_DEVIATIONS,
    FIXED_LIMITATIONS,
    MACRO_TERMS,
    MAIN,
    MAIN_START,
    PREREG_DEVIATIONS,
    ROBUST_ALPHA,
    TERM_LABELS,
    VARIANTS,
    VariantSpec,
)
from src.stationarity import decide, is_stationary
from src.tables import fmt_es, quarter_label, to_markdown

LONG_RUN_NOT_REPORTED = "no reportado (1 − ρ ≤ 0,05)"
UNDEFINED = "no definido"
IMPULSE_SE_NOTE = "EE HAC no informativo: dummy de impulso con residuo nulo"
RANK_NOTE = "rango reducido por dummies de impulso (esperado)"
_SIGN_SYMBOL = {"+": "+", "-": "−"}


@dataclass(frozen=True)
class VariantOutcome:
    """Resultado de una variante de robustez: estimada, o «no estimada» con su motivo."""

    spec: VariantSpec
    status: str  # "estimada" | "no estimada"
    reason: str  # "" si está estimada
    design: Design | None
    fit: Fit | None

    @property
    def estimated(self) -> bool:
        return self.status == "estimada" and self.fit is not None


@dataclass(frozen=True)
class Model1Result:
    """Resultado del Modelo I (tareas 5 y 6). La tarea 7 añadirá el fuera de muestra."""

    decisions: dict[str, str]
    design: Design
    fit: Fit
    coefficients: pd.DataFrame
    coef_footer: dict
    effects: pd.DataFrame
    stationarity: pd.DataFrame
    diagnostics: pd.DataFrame
    cusum: dict
    variants: list[VariantOutcome]
    robustness_estimates: pd.DataFrame
    robustness_summary: pd.DataFrame
    limitations: pd.DataFrame
    deviations: pd.DataFrame
    stress: dict


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


# --- Variantes de robustez (RF-5, RF-6) ---


def run_variant(
    full: pd.DataFrame, spec: VariantSpec, decisions: dict[str, str], end: pd.Period
) -> VariantOutcome:
    """Estima una variante de robustez, o la declara «no estimada» con su motivo.

    - Sin historia anterior a 2000T1 en una variante de muestra larga (R8): «no estimada» (RF-5).
    - Menos de 30 grados de libertad o X de rango incompleto: «no estimada» (RF-6).
    - Un faltante dentro de su muestra es un error y no una variante «no estimada» (RF-2).
    """
    if spec.dependent not in decisions:
        raise ModelDataError(
            f"{spec.dependent}: no aparece en la tabla de estacionariedad (variante {spec.id})"
        )
    design = build_design(full, spec, decisions[spec.dependent], end)
    if spec.start < MAIN_START and design.X.index[0] >= MAIN_START:
        return VariantOutcome(
            spec, "no estimada", f"sin historia anterior a {quarter_label(MAIN_START)}", design, None
        )
    reason = check_dof(design)
    if reason:
        return VariantOutcome(spec, "no estimada", reason, design, None)
    return VariantOutcome(spec, "estimada", "", design, fit_ols_hac(design))


def is_robust(main_coef: float, coef: float, p: float, alpha: float = ROBUST_ALPHA) -> bool:
    """Criterio pre-registrado: mismo signo que la principal y p < 0,10 con error HAC.

    Un coeficiente nulo (en la variante o en la principal) no tiene signo: no es robusto.
    """
    if not (np.isfinite(main_coef) and np.isfinite(coef) and np.isfinite(p)):
        return False
    if main_coef == 0 or coef == 0:
        return False
    return bool(np.sign(main_coef) == np.sign(coef) and p < alpha)


def _terms_difference(main: Fit, design: Design | None) -> str:
    if design is None:
        return ""
    main_cols, cols = list(main.design.X.columns), list(design.X.columns)
    added = [c for c in cols if c not in main_cols]
    removed = [c for c in main_cols if c not in cols]
    parts = []
    if added:
        parts.append("añade: " + ", ".join(added))
    if removed:
        parts.append("quita: " + ", ".join(removed))
    return "; ".join(parts)


def _variant_note(o: VariantOutcome) -> str:
    notes = []
    spec = o.spec
    if spec.exclude:
        a, b = (quarter_label(pd.Period(q, "Q-DEC")) for q in spec.exclude)
        notes.append(
            f"excluye {a}–{b}; los trimestres vecinos de la exclusión se tratan como contiguos "
            "en la ventana HAC"
        )
    if not spec.in_pp:
        notes.append("el logit no está en pp: solo se evalúan signo y significancia")
    if spec.id.startswith("R3_"):
        notes.append("coeficientes en pp del cambio de la morosidad de la sub-cartera")
    if o.design is not None and o.design.X.index[0] > spec.start:
        notes.append("inicio efectivo posterior al nominal por la historia disponible")
    return "; ".join(notes)


def robustness_estimates(main: Fit, outcomes: list[VariantOutcome]) -> pd.DataFrame:
    """Una fila por variante estimada y regresor macro; una sola fila si no se estimó (RF-16)."""
    rows = []
    for o in outcomes:
        base = {
            "variante": o.spec.id,
            "etiqueta": o.spec.label,
            "dependiente": o.spec.dependent,
        }
        if not o.estimated:
            rows.append({
                **base, "forma_y": "", "terminos_diferencia": "", "inicio": "", "fin": "",
                "n_obs": pd.NA, "rezagos_hac": pd.NA, "termino": "", "coef": np.nan,
                "ee_hac": np.nan, "p": np.nan, "estado": "no estimada", "motivo": o.reason,
                "nota": "",
            })
            continue
        inf = inference(o.fit.params, o.fit.cov)
        index = o.design.X.index
        for term in MACRO_TERMS:
            rows.append({
                **base,
                "forma_y": o.design.form,
                "terminos_diferencia": _terms_difference(main, o.design),
                "inicio": quarter_label(index.min()),
                "fin": quarter_label(index.max()),
                "n_obs": int(o.fit.nobs),
                "rezagos_hac": int(o.fit.hac_lags),
                "termino": term,
                "coef": float(inf.loc[term, "coef"]),
                "ee_hac": float(inf.loc[term, "se"]),
                "p": float(inf.loc[term, "p"]),
                "estado": "estimada",
                "motivo": "",
                "nota": _variant_note(o),
            })
    df = pd.DataFrame(rows)
    df["n_obs"] = df["n_obs"].astype("Int64")
    df["rezagos_hac"] = df["rezagos_hac"].astype("Int64")
    return df


def robustness_summary(main: Fit, outcomes: list[VariantOutcome]) -> pd.DataFrame:
    """Regresor × variante: «sí», «no» o «no estimada», y el recuento «k de n» (RF-17).

    n cuenta solo las variantes estimadas; una variante «no estimada» sale del denominador.
    """
    rows = []
    infs = {o.spec.id: inference(o.fit.params, o.fit.cov) for o in outcomes if o.estimated}
    n = len(infs)
    for term in MACRO_TERMS:
        row: dict = {"termino": term, "etiqueta": term_label(term)}
        k = 0
        for o in outcomes:
            if not o.estimated:
                row[o.spec.id] = "no estimada"
                continue
            r = infs[o.spec.id].loc[term]
            ok = is_robust(float(main.params[term]), float(r["coef"]), float(r["p"]))
            row[o.spec.id] = "sí" if ok else "no"
            k += int(ok)
        row.update({"k": k, "n": n, "robustez": f"{k} de {n}"})
        rows.append(row)
    return pd.DataFrame(rows)


# --- Limitaciones (RF-20) y desviaciones (RF-21) ---


def _short_label(termino: str) -> str:
    return term_label(termino).split(" (")[0]


def _diagnostic_detail(row: pd.Series) -> str:
    stat, p = row["estadístico"], row["p_valor"]
    if pd.notna(p):
        detail = f"estadístico {fmt_es(stat, 3)}, p = {fmt_es(p, 3)}"
    elif pd.notna(stat):
        detail = f"estadístico {fmt_es(stat, 3)}"
    else:
        detail = "sin estadístico"
    prueba = str(row["prueba"])
    if prueba == "Breusch-Godfrey":
        detail += (
            "; con el rezago de la dependiente, MCO puede ser inconsistente (se declara como "
            "limitación; añadir rezagos tras ver el resultado exige un /sdd-change)"
        )
    elif prueba.startswith("VIF"):
        detail += "; posible multicolinealidad: se reporta y no se elimina ningún regresor"
    elif row.get("nota"):
        detail += f"; {row['nota']}"
    else:
        detail += "; se reporta y se discute qué implica para las conclusiones"
    return detail


def limitations_table(
    model_stationarity: pd.DataFrame,
    diagnostics: pd.DataFrame,
    fit: Fit,
    outcomes: list[VariantOutcome],
    stationarity: pd.DataFrame,
) -> pd.DataFrame:
    """Limitaciones del Modelo I: las fijas más las detectadas por el código (RF-20).

    Detectadas: regresores no I(0), dependientes con orden «posible I(2)», truncamiento
    espectral, diagnósticos con veredicto «falla» o «alerta» y variantes «no estimadas».
    La reducción de rango por dummies de impulso es esperada y no figura como limitación.
    """
    rows = [
        {"limitacion": name, "detalle": detail, "origen": "fija"}
        for name, detail in FIXED_LIMITATIONS
    ]

    flagged = [
        _short_label(t)
        for t in model_stationarity.loc[model_stationarity["no_i0"] == "sí", "termino"]
    ]
    rows.append({
        "limitacion": "Regresores no I(0)",
        "detalle": (
            f"{', '.join(flagged)}: no son I(0) según la regla de la spec 001; entran en su "
            "forma fija y su no estacionariedad residual se declara como limitación del modelo."
            if flagged else "ninguno"
        ),
        "origen": "detectada",
    })

    orden = {
        r["variable"]: r["orden"]
        for _, r in stationarity[stationarity["forma"] == "tal cual"].iterrows()
    }
    i2 = []
    if orden.get(MAIN.dependent) == "posible I(2)":
        i2.append(f"{MAIN.dependent} (principal)")
    for o in outcomes:
        if orden.get(o.spec.dependent) == "posible I(2)":
            i2.append(f"{o.spec.dependent} ({o.spec.id})")
    rows.append({
        "limitacion": "Dependientes con orden «posible I(2)»",
        "detalle": ", ".join(i2) if i2 else "ninguna",
        "origen": "detectada",
    })

    truncated = (["principal"] if fit.psd_adjusted else []) + [
        o.spec.id for o in outcomes if o.estimated and o.fit.psd_adjusted
    ]
    if truncated:
        rows.append({
            "limitacion": "Truncamiento espectral de la covarianza HAC",
            "detalle": "Se aplicó al sub-bloque sin dummies de impulso en: "
                       + ", ".join(truncated) + ".",
            "origen": "detectada",
        })

    for _, r in diagnostics[diagnostics["veredicto"].isin(["falla", "alerta"])].iterrows():
        rows.append({
            "limitacion": f"{r['prueba']}: {r['veredicto']}",
            "detalle": _diagnostic_detail(r),
            "origen": "detectada",
        })

    for o in outcomes:
        if not o.estimated:
            rows.append({
                "limitacion": f"Variante {o.spec.id} no estimada",
                "detalle": o.reason,
                "origen": "detectada",
            })
    return pd.DataFrame(rows, columns=["limitacion", "detalle", "origen"])


def deviations_table(outcomes: list[VariantOutcome], end: pd.Period) -> pd.DataFrame:
    """Desviaciones y decisiones frente a la guía y a las reglas del proyecto (RF-21)."""
    rows: list[tuple[str, str, str]] = [FIXED_DEVIATIONS[0]]
    rows.append((
        f"Muestra hasta {quarter_label(end)} (último trimestre común)",
        "Guía, sección 11",
        "El ejemplo de descarga de la guía corta en 2026-01-01; se usan todos los trimestres "
        "completos disponibles.",
    ))
    r8 = next((o for o in outcomes if o.spec.id == "R8"), None)
    if r8 is None:
        estado = "R8 no se ejecutó"
    elif r8.estimated:
        estado = f"R8 estimada con inicio efectivo {quarter_label(r8.design.X.index[0])}"
    else:
        estado = f"R8 no estimada: {r8.reason}"
    rows.append((
        "Muestra larga desde 1985T1 (fuera del período 2000–2026 de la guía)",
        "Guía, sección 11",
        estado,
    ))
    rows.extend(FIXED_DEVIATIONS[1:])
    rows.extend(
        (f"{fecha} · {cambio}", "Pre-registro de la spec 003", motivo)
        for fecha, cambio, motivo in PREREG_DEVIATIONS
    )
    return pd.DataFrame(rows, columns=["decision", "referencia", "motivo"])


# --- Exportación para la spec 005 (RF-8) ---


def stress_export(fit: Fit) -> dict:
    """Coeficientes y covarianza HAC de la principal, listos para la prueba de estrés (RF-8)."""
    index = fit.design.X.index
    return {
        "spec": "003-modelo-i",
        "dependent": MAIN.dependent,
        "form": fit.design.form,
        "terms": list(fit.params.index),
        "columns": dict(MACRO_TERMS),
        "credit_lag": MAIN.credit_lag,
        "params": fit.params.to_numpy(dtype=float).tolist(),
        "cov_hac": fit.cov.to_numpy(dtype=float).tolist(),
        "psd_adjusted": bool(fit.psd_adjusted),
        "sample_start": quarter_label(index.min()),
        "sample_end": quarter_label(index.max()),
        "nobs": int(fit.nobs),
        "hac_lags": int(fit.hac_lags),
        "covid_quarters": [quarter_label(pd.Period(q, "Q-DEC")) for q in COVID_QUARTERS],
    }


def stress_export_json(export: dict) -> str:
    """JSON determinista (claves en orden, floats con precisión completa, sin NaN)."""
    return json.dumps(export, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


# --- Salida en Markdown y CSV como texto (RF-23) ---

_P_COLUMNS = ("p", "p_valor")


def fmt_p(p: float) -> str:
    """p-valor con coma decimal; «< 0,001» si es menor que 0,001."""
    if pd.isna(p):
        return "—"
    return "< 0,001" if p < 0.001 else fmt_es(p, 3)


def coefficient_note(footer: dict) -> str:
    """Párrafo «Nota:» que cierra la tabla de coeficientes (pie de RF-9)."""
    parts = [
        f"variable dependiente en {footer['forma_y']}",
        f"muestra {footer['muestra_inicio']}–{footer['muestra_fin']}",
        f"n = {footer['n_obs']}",
        f"parámetros = {footer['n_parametros']}",
        f"R² = {fmt_es(footer['r2'], 3)}",
        f"R² ajustado = {fmt_es(footer['r2_ajustado'], 3)}",
        f"error estándar de la regresión = {fmt_es(footer['ee_regresion'], 3)}",
        f"ventana HAC de {footer['rezagos_hac']} rezagos (Newey-West, kernel de Bartlett)",
        f"truncamiento espectral: {'sí' if footer['truncamiento_espectral'] else 'no'}",
    ]
    if footer["nota_rango"]:
        parts.append(footer["nota_rango"])
    return "Nota: " + "; ".join(parts) + "."


def _format_for_markdown(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    for c in df.columns:
        col = df[c]
        if c in _P_COLUMNS:
            out[c] = [fmt_p(v) for v in col]
        elif pd.api.types.is_bool_dtype(col):
            out[c] = ["sí" if v else "no" for v in col]
        elif pd.api.types.is_integer_dtype(col):
            out[c] = ["—" if pd.isna(v) else str(int(v)) for v in col]
        elif pd.api.types.is_float_dtype(col):
            out[c] = [fmt_es(v, 3) for v in col]
        else:
            out[c] = col.astype(str)
    return out


def render_model1_tables(result: Model1Result) -> dict[str, dict[str, str]]:
    """Cada tabla del Modelo I como texto Markdown y CSV (sin escribir a disco; RF-23).

    El CSV conserva la precisión completa con punto decimal; el Markdown usa coma decimal y
    «< 0,001». La tabla de coeficientes cierra con la nota de RF-9.
    """
    tables = {
        "model1_coefficients": result.coefficients,
        "model1_effects": result.effects,
        "model1_diagnostics": result.diagnostics,
        "model1_stationarity": result.stationarity,
        "model1_robustness_estimates": result.robustness_estimates,
        "model1_robustness_summary": result.robustness_summary,
        "model1_limitations": result.limitations,
        "model1_deviations": result.deviations,
    }
    notes = {"model1_coefficients": coefficient_note(result.coef_footer)}
    out: dict[str, dict[str, str]] = {}
    for stem, df in tables.items():
        md = to_markdown(_format_for_markdown(df))
        if stem in notes:
            md += "\n\n" + notes[stem]
        csv = df.to_csv(index=False, float_format=None, lineterminator="\n")
        out[stem] = {"md": md, "csv": csv}
    return out


# --- Estimación principal (RF-3, RF-4, RF-7) ---


def run_model1(full: pd.DataFrame, stationarity: pd.DataFrame, end: pd.Period) -> Model1Result:
    """Estima la especificación principal, sus diagnósticos y las variantes de robustez.

    1. Lee las decisiones y comprueba las formas esperadas (RF-3, RF-4) antes de estimar nada.
    2. Construye el diseño de la muestra principal estricta, 2000T1–`end` (RF-1).
    3. Si la principal no tiene grados de libertad suficientes o X no tiene rango completo,
       se detiene (RF-6).
    4. Estima por MCO con errores Newey-West (RF-7), calcula los diagnósticos (RF-12 a RF-14)
       y estima las variantes R1–R8 (RF-16, RF-17).
    5. Construye las tablas de coeficientes, efectos, estacionariedad, limitaciones y
       desviaciones, y la exportación para la spec 005 (RF-8).
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
    model_stat = model_stationarity_table(stationarity, decisions, MAIN.dependent)
    diagnostics = diagnostics_table(fit)
    outcomes = [run_variant(full, spec, decisions, end) for spec in VARIANTS]
    return Model1Result(
        decisions=decisions,
        design=design,
        fit=fit,
        coefficients=coefficients,
        coef_footer=footer,
        effects=effects_table(fit),
        stationarity=model_stat,
        diagnostics=diagnostics,
        cusum=cusum(fit),
        variants=outcomes,
        robustness_estimates=robustness_estimates(fit, outcomes),
        robustness_summary=robustness_summary(fit, outcomes),
        limitations=limitations_table(model_stat, diagnostics, fit, outcomes, stationarity),
        deviations=deviations_table(outcomes, end),
        stress=stress_export(fit),
    )
