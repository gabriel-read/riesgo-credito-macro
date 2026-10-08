"""Orquestación pura del Modelo II (spec 004): selección de K, principal y tablas (tarea 5).

Estima un modelo por K = 1..8 sobre la muestra común M, elige K por BIC (principal) y AIC (R1),
calcula efectos acumulados, trayectoria, Granger, lectura de la evidencia, proyecciones locales y
su comparación, diagnósticos y estacionariedad, las robusteces R1–R3, las limitaciones, las
desviaciones, los insumos de la sección 6.3, la exportación para la spec 005 y la salida en Markdown y
CSV como texto (sin escribir a disco). Devuelve un `Model2Result`. Sin acceso a red, disco ni gráficos
(RNF-7). RF-2 a RF-27, RF-29, RF-30.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.design import Design, ModelDataError, check_expected_forms, diff_form_stationary, read_decisions
from src.design2 import (
    build_columns,
    build_design2,
    common_window,
    covid_lag_leaks,
    lagged_from_excluded,
)
from src.diagnostics import (
    breusch_godfrey,
    breusch_pagan,
    chow_wald,
    cusum,
    jarque_bera_test,
    reset,
    vif,
    white,
)
from src.dynamics import (
    cumulative_effects,
    evidence_reading,
    granger_lags,
    hypotheses,
    multipliers,
    peak_horizon,
    select_k,
)
from src.estimation import Fit, _impulse_dummy_cols, check_dof, fit_ols_hac, inference
from src.localproj import compare_with_trajectory, run_local_projections
from src.model1 import fmt_p, is_robust
from src.model1_config import CHOW_BREAKS, MAIN_START, ROBUST_ALPHA
from src.model2_config import (
    CHOW_POST_MIN,
    CONTROLS,
    COVID_QUARTERS,
    EXPECTED_FORM,
    FIXED_DEVIATIONS2,
    FIXED_LIMITATIONS2,
    K_MAX,
    K_RANGE,
    LP_BAND_Z,
    MAIN2,
    PREREG_DEVIATIONS2,
    RHO_WARN,
    ROBUST2,
    Spec2,
    dffr_cols,
    term_label2,
)
from src.stationarity import is_stationary
from src.tables import fmt_es, quarter_label, to_markdown

IMPULSE_SE_NOTE = "EE HAC no informativo: dummy de impulso con residuo nulo"
RANK_NOTE = "rango reducido por dummies de impulso (esperado)"
NOT_CALCULABLE = "no calculable"
SIZE_NOTE = "el tamaño empírico del contraste puede diferir del 5 % nominal"
_DASH = "—"


@dataclass(frozen=True)
class VariantOutcome2:
    """Resultado de una robustez: estimada, «no estimada» con su motivo o «no aplica» (RF-22, RF-23)."""

    spec: Spec2
    status: str            # "estimada" | "no estimada" | "no aplica"
    reason: str            # "" si está estimada
    design: Design | None
    fit: Fit | None
    effects: dict | None
    peak: dict | None
    hyp: dict | None

    @property
    def estimated(self) -> bool:
        return self.status == "estimada" and self.fit is not None

    @property
    def K(self) -> int | None:
        """K de la variante: ΔFFR(t..t−K) en su diseño."""
        if self.design is None:
            return None
        return sum(c.startswith("d_ffr_l") for c in self.design.X.columns) - 1


@dataclass(frozen=True)
class Model2Result:
    """Resultado del Modelo II."""

    decision: str
    window: tuple[pd.Period, pd.Period]
    nobs: int
    K: int
    k_aic: int
    k_bic: int
    fits: dict[int, Fit]
    main_fit: Fit
    selection: pd.DataFrame
    selection_note: str
    coefficients: pd.DataFrame
    coef_footer: dict
    coef_note: str
    effects_raw: dict
    effects: pd.DataFrame
    effects_note: str
    peak: dict
    hyp: dict
    trajectory: pd.DataFrame
    trajectory_note: str
    granger: dict
    reading: dict
    reading_table: pd.DataFrame
    reading_note: str
    lp: pd.DataFrame
    comparison: pd.DataFrame
    comparison_counts: dict
    comparison_note: str
    diagnostics: pd.DataFrame
    cusum: dict
    stationarity: pd.DataFrame
    stationarity_note: str
    lp_note: str
    variants: list[VariantOutcome2]
    robustness_estimates: pd.DataFrame
    robustness_summary: pd.DataFrame
    robustness_note: str
    limitations: pd.DataFrame
    deviations: pd.DataFrame
    inputs63: pd.DataFrame
    inputs63_note: str
    export: dict


# --- Selección (RF-3, RF-7) ---


def selection_table(sel: dict) -> pd.DataFrame:
    """Una fila por K con parámetros, observaciones, AIC, BIC y la marca de los K elegidos (RF-7)."""
    t = sel["table"].copy()
    marks = []
    for k in t["K"]:
        if k == sel["k_bic"] == sel["k_aic"]:
            marks.append("K_AIC y K_BIC (principal)")
        elif k == sel["k_bic"]:
            marks.append("K_BIC (principal)")
        elif k == sel["k_aic"]:
            marks.append("K_AIC (R1)")
        else:
            marks.append("")
    t["marca"] = marks
    return t


def selection_note(window: tuple[pd.Period, pd.Period], nobs: int, k_aic: int, k_bic: int) -> str:
    """Pie de la tabla de selección: muestra común M y regla (RF-3, RF-6)."""
    return (
        f"Nota: muestra común M {quarter_label(window[0])}–{quarter_label(window[1])}, n = {nobs}; "
        f"un modelo por K = {K_RANGE[0]}..{K_RANGE[-1]} con el mismo resto de la ecuación y las cuatro "
        f"dummies COVID; K_BIC = {k_bic} (especificación principal) y K_AIC = {k_aic}; en un empate "
        "gana el menor K."
    )


# --- Coeficientes (RF-8) ---


def coefficients_table2(fit: Fit) -> pd.DataFrame:
    """Coeficientes con error HAC, z, p e IC 95 %; las dummies de impulso llevan su nota (RF-8)."""
    inf = inference(fit.params, fit.cov)
    impulse = set(_impulse_dummy_cols(fit.design.X))
    rows = []
    for term in fit.params.index:
        rows.append({
            "termino": term,
            "etiqueta": term_label2(term),
            "coef": float(inf.loc[term, "coef"]),
            "ee_hac": float(inf.loc[term, "se"]),
            "z": float(inf.loc[term, "z"]),
            "p": float(inf.loc[term, "p"]),
            "ic_inf": float(inf.loc[term, "ic_inf"]),
            "ic_sup": float(inf.loc[term, "ic_sup"]),
            "nota": IMPULSE_SE_NOTE if term in impulse else "",
        })
    return pd.DataFrame(rows)


def coefficient_footer2(fit: Fit, K: int) -> dict:
    index = fit.design.X.index
    return {
        "K": int(K),
        "criterio": "BIC",
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
        "nota_rango": RANK_NOTE if _impulse_dummy_cols(fit.design.X) else "",
    }


def coefficient_note2(f: dict) -> str:
    """Pie de la tabla de coeficientes con todo lo que pide RF-8."""
    parts = [
        f"K = {f['K']} elegido por {f['criterio']}",
        f"variable dependiente en {f['forma_y']}",
        f"muestra M {f['muestra_inicio']}–{f['muestra_fin']}",
        f"n = {f['n_obs']}",
        f"parámetros = {f['n_parametros']}",
        f"R² = {fmt_es(f['r2'], 3)}",
        f"R² ajustado = {fmt_es(f['r2_ajustado'], 3)}",
        f"error estándar de la regresión = {fmt_es(f['ee_regresion'], 3)}",
        f"ventana HAC de {f['rezagos_hac']} rezagos (Newey-West, kernel de Bartlett)",
        f"truncamiento espectral: {'sí' if f['truncamiento_espectral'] else 'no'}",
    ]
    if f["nota_rango"]:
        parts.append(f["nota_rango"])
    return "Nota: " + "; ".join(parts) + "."


# --- Efectos acumulados (RF-10) ---


def effects_table2(effects: dict, hyp: dict, K: int) -> pd.DataFrame:
    """S y S_rez con error HAC, χ²(1), p e IC 95 %, y H1 sobre S (RF-10)."""
    rows = []
    for key, desc in (("S", f"θ0+…+θ{K}"), ("S_rez", f"θ1+…+θ{K}")):
        e = effects[key]
        rows.append({
            "efecto": key, "descripcion": desc, "est": e["est"], "ee_hac": e["se"], "chi2": e["chi2"],
            "p": e["p"], "ic_inf": e["ic_inf"], "ic_sup": e["ic_sup"],
            "h1_signo": hyp["h1_signo"] if key == "S" else _DASH,
            "h1_respaldada": (("respaldada" if hyp["h1_respaldada"] == "sí" else "no respaldada")
                              if key == "S" else _DASH),
        })
    return pd.DataFrame(rows)


def effects_note2(K: int) -> str:
    return (
        f"Nota: S = θ0+…+θ{K} y S_rez = θ1+…+θ{K}, en pp de morosidad por 1 pp de ΔFFR; Wald HAC "
        "χ²(1) (H0: la suma es cero) e IC 95 % normal; H1: S > 0 (signo puntual) y «respaldada» si además "
        "p < 0,05."
    )


# --- Trayectoria (RF-11) ---


def rho_warning(rho: float) -> str:
    """Avisos de RF-11 sobre ρ̂: dinámica explosiva (|ρ̂| ≥ 1) y R(h) sensible a ρ (ρ̂ ≥ 0,95)."""
    parts = []
    if abs(rho) >= 1:
        parts.append(f"|ρ̂| = {fmt_es(abs(rho), 3)} ≥ 1: la dinámica es explosiva")
    if rho >= RHO_WARN:
        parts.append(f"ρ̂ = {fmt_es(rho, 3)} ≥ {fmt_es(RHO_WARN, 2)}: R(h) es muy sensible a ρ")
    return "; ".join(parts)


def trajectory_table(traj: pd.DataFrame, peak: dict) -> pd.DataFrame:
    t = traj.copy()
    t["h_estrella"] = ["sí" if h == peak["h_star"] else "" for h in t["h"]]
    return t


def trajectory_note(rho: float, peak: dict, hyp: dict) -> str:
    """Pie de la trayectoria: sin bandas, h* con su signo, H2 y avisos de ρ (RF-11)."""
    parts = [
        "ψ_h es la respuesta de ΔDR (pp por trimestre) y R(h) la respuesta acumulada del nivel de la morosidad (pp) a un shock "
        "de 1 pp en ΔFFR",
        f"h* = {peak['h_star']} (signo {peak['signo']}), el h con mayor |ψ_h|",
        f"H2 (h* ≥ 1): {hyp['h2']}",
        "la trayectoria es solo estimación puntual y no lleva bandas: las bandas están en la proyección local",
    ]
    warn = rho_warning(rho)
    if warn:
        parts.append(warn)
    return "Nota: " + "; ".join(parts) + "."


# --- Granger y lectura (RF-12, RF-13) ---


def reading_table2(granger: dict, effects: dict, reading: dict, K: int) -> pd.DataFrame:
    s_rez = effects["S_rez"]
    label = reading["etiqueta"] + (" · signo contrario al esperado" if reading["signo_contrario"] else "")
    rows = [
        (f"Granger: θ1 = … = θ{K} = 0", granger["stat"], granger["df"], granger["p"], granger["veredicto"]),
        ("C1: Granger rechaza al 5 %", np.nan, np.nan, np.nan, "sí" if reading["c1"] else "no"),
        ("C2: S_rez > 0 con p < 0,05", s_rez["chi2"], 1, s_rez["p"], "sí" if reading["c2"] else "no"),
        ("Lectura de «¿hay efectos rezagados?»", np.nan, np.nan, np.nan, label),
    ]
    df = pd.DataFrame(rows, columns=["elemento", "estadistico", "gl", "p", "resultado"])
    df["gl"] = df["gl"].astype("Int64")
    return df


def reading_note2(K: int) -> str:
    return (
        f"Nota: la prueba de Granger es un Wald HAC χ²({K}) sobre θ1..θ{K} (se excluye θ0, que es simultáneo) y "
        "mide precedencia temporal de la tasa respecto de la morosidad; la lectura usa solo lo rezagado: "
        "«evidencia fuerte» si se cumplen C1 y C2, «evidencia parcial» si se cumple una y «sin evidencia» "
        "si ninguna."
    )


# --- Comparación (RF-17) ---


def comparison_note2(counts: dict) -> str:
    return (
        "Nota: β_h y R(h) son objetos distintos: R(h) mantiene fijos la tasa posterior y los controles, "
        "mientras que β_h incluye la trayectoria posterior de la tasa (φ_h) y la reacción de los controles; "
        "la comparación es descriptiva y no prueba la forma paramétrica. En h = 0 coinciden por construcción "
        "y no entra en el recuento; φ_0 = 1 por construcción (identidad). "
        f"Mismo signo en {counts['k_de_n']} horizontes estimados (h = 1..12); "
        f"horizonte de detección: {counts['horizonte_deteccion']}."
    )


# --- Diagnósticos (RF-19, RF-20) ---


def _chow_note(cw: dict, K: int, break_q: str) -> str:
    base = (
        f"Wald HAC con interacciones de {K + 7} términos (constante, ρ, ΔFFR(t..t−{K}) y los cuatro "
        f"controles); dummies COVID sin interactuar; trimestres útiles anteriores: {cw['n_pre_util']}; "
        f"posteriores: {cw['n_post_util']}"
    )
    if not cw["calculable"]:
        return f"{cw['motivo']}; {base}"
    if cw["n_post_util"] < CHOW_POST_MIN:
        base += f"; {SIZE_NOTE}"
    return base


def diagnostics_table2(fit: Fit, K: int) -> pd.DataFrame:
    """Batería de la spec 003 con la dimensión del Modelo II (RF-19, RF-20).

    White es «no calculable» (sin veredicto) si n − rango(Z_aux) < 30; el Chow arma su propia nota
    (no usa la del Modelo I) y es «no calculable» si el bloque de interacciones tiene rango incompleto.
    """
    nan = np.nan
    rows = []

    def add(prueba, stat, p, verdict, nota=""):
        rows.append({"prueba": prueba, "estadístico": stat, "p_valor": p, "veredicto": verdict, "nota": nota})

    for name, res in (("Breusch-Godfrey", breusch_godfrey(fit)), ("Breusch-Pagan", breusch_pagan(fit))):
        add(name, res["stat"], res["p"], res["veredicto"])
    wh = white(fit)
    if wh["calculable"]:
        add("White", wh["stat"], wh["p"], wh["veredicto"])
    else:
        add("White", nan, nan, NOT_CALCULABLE, wh["motivo"])
    for name, res in (("Jarque-Bera", jarque_bera_test(fit)), ("RESET", reset(fit))):
        add(name, res["stat"], res["p"], res["veredicto"])
    terms = ["y_lag", *dffr_cols(K), *CONTROLS]
    for _, row in vif(fit, terms=terms).iterrows():
        add(f"VIF ({row['term']})", row["vif"], nan, row["veredicto"])
    for break_q in CHOW_BREAKS:
        cw = chow_wald(fit, break_q)
        label = f"Chow {quarter_label(pd.Period(break_q, 'Q-DEC'))}"
        if cw["calculable"]:
            add(label, cw["stat"], cw["p"], cw["veredicto"], _chow_note(cw, K, break_q))
        else:
            add(label, nan, nan, NOT_CALCULABLE, _chow_note(cw, K, break_q))
    cu = cusum(fit)
    add("CUSUM", nan, nan, cu["veredicto"], cu["nota"])
    return pd.DataFrame(rows)


# --- Estacionariedad (RF-21) ---

# (término, variable de la tabla de la 001, forma en que entra, ¿rezagado?)
_STATIONARITY_TERMS = [
    ("d_dr", "dralacbs", "primera diferencia", False),
    ("d_ffr", "fedfunds", "primera diferencia", False),
    ("gdp_l1", "gdpc1_yoy", "tal cual", True),
    ("d_unemp_l1", "unrate", "primera diferencia", True),
    ("inflation_l1", "cpiaucsl_yoy", "tal cual", True),
    ("credit_l4", "loans_yoy", "tal cual", True),
]
_STATIONARITY_LABELS = {
    "d_dr": "ΔDR — dependiente (DRALACBS en primera diferencia)",
    "d_ffr": "ΔFFR — cambio trimestral de la tasa de la Fed",
}


def stationarity_table2(stationarity: pd.DataFrame) -> pd.DataFrame:
    """ADF/KPSS de ΔDR, ΔFFR y los cuatro controles, copiados de la tabla de la spec 001 (RF-21).

    ΔDR, ΔFFR y ΔU salen de la fila «primera diferencia» (decisión con la regla de la spec 001);
    PIB, π y CRED, de la fila «tal cual». Los términos rezagados usan la serie sin rezagar.
    """
    rows = []
    for term, variable, forma, lagged in _STATIONARITY_TERMS:
        sel = stationarity[(stationarity["variable"] == variable) & (stationarity["forma"] == forma)]
        if sel.empty:
            raise ModelDataError(f"{variable}: no hay fila '{forma}' en la tabla de estacionariedad")
        src = sel.iloc[0]
        if forma == "tal cual":
            decision, orden = str(src["decision"]), str(src["orden"])
            nota = ""
        else:
            decision, _ = diff_form_stationary(stationarity, variable)
            orden = "I(0)" if is_stationary(float(src["adf_p"]), float(src["kpss_p"])) else "no I(0)"
            nota = "regla de la spec 001 aplicada a la fila «primera diferencia»"
        if lagged:
            nota = (nota + "; " if nota else "") + "ADF/KPSS de la serie sin rezagar"
        rows.append({
            "termino": term,
            "etiqueta": _STATIONARITY_LABELS.get(term, term_label2(term)),
            "columna_panel": variable,
            "forma": forma,
            "adf_stat": float(src["adf_stat"]),
            "adf_p": float(src["adf_p"]),
            "kpss_stat": float(src["kpss_stat"]),
            "kpss_p": float(src["kpss_p"]),
            "decision": decision,
            "orden": orden,
            "no_i0": "no" if orden == "I(0)" else "sí",
            "nota": nota,
        })
    return pd.DataFrame(rows)


def stationarity_note2() -> str:
    return (
        "Nota: ADF y KPSS copiados de la tabla de la spec 001, sin recalcular; ΔDR, ΔFFR y ΔU se juzgan con "
        "la fila «primera diferencia» y «niveles» significa estacionaria en la forma en que entra; los "
        "términos rezagados (PIB(t−1), ΔU(t−1), π(t−1), CRED(t−4)) usan el ADF y el KPSS de la serie sin "
        "rezagar; «no I(0)» marca los términos que no son estacionarios en la forma fija en que entran."
    )


# --- Proyecciones locales: pie (RF-14 a RF-16) ---


def lp_note2() -> str:
    return (
        "Nota: β_h es el coeficiente de ΔFFR(t) en la regresión de DR(t+h) − DR(t−1) y φ_h el de la regresión de "
        "FFR(t+h) − FFR(t−1), con los mismos controles y las dummies COVID fechadas en t; cada horizonte usa su "
        "propia muestra, que termina h trimestres antes del último común; ventana HAC de max(fórmula, h + 1) "
        f"rezagos; banda del 90 % = estimación ± {fmt_es(LP_BAND_Z, 4)}·EE. En h = 0, φ_0 = 1 por construcción "
        "(identidad) y no lleva error ni banda; un horizonte «no estimada» no afecta a los demás."
    )


# --- Robusteces (RF-22 a RF-24) ---


def run_variant2(full: pd.DataFrame, spec: Spec2, K_main: int, k_aic: int, decision: str,
                 window: tuple[pd.Period, pd.Period], end: pd.Period) -> VariantOutcome2:
    """Estima una robustez con el mismo estimador y las mismas reglas que la principal (RF-22, RF-23).

    R1 usa K_AIC y es «no aplica» si coincide con K_BIC; R2 y R3 usan el K de la principal y omiten las
    dummies COVID. Menos de 30 grados de libertad o rango incompleto: «no estimada» con su motivo. Un
    faltante dentro de la muestra es un error (RF-4), no una variante «no estimada».
    """
    K = K_main
    if spec.k_source == "aic":
        if k_aic == K_main:
            return VariantOutcome2(spec, "no aplica", "AIC y BIC eligen el mismo K", None, None, None, None, None)
        K = k_aic
    design = build_design2(full, spec, K, decision, window, end)
    reason = check_dof(design)
    if reason:
        return VariantOutcome2(spec, "no estimada", reason, design, None, None, None, None)
    fit = fit_ols_hac(design)
    effects = cumulative_effects(fit, K)
    peak = peak_horizon(multipliers(fit.params, K)["psi"])
    return VariantOutcome2(spec, "estimada", "", design, fit, effects, peak, hypotheses(effects, peak))


def _ranges_text(quarters: list[pd.Period]) -> str:
    """«2009T1–2015T4, 2020T2–2021T1»: trimestres consecutivos agrupados en rangos."""
    if not quarters:
        return ""
    groups: list[list[pd.Period]] = [[quarters[0]]]
    for q in quarters[1:]:
        if q.ordinal - groups[-1][-1].ordinal == 1:
            groups[-1].append(q)
        else:
            groups.append([q])
    return ", ".join(
        quarter_label(g[0]) if len(g) == 1 else f"{quarter_label(g[0])}–{quarter_label(g[-1])}" for g in groups
    )


def _excluded_quarters(o: VariantOutcome2, window: tuple[pd.Period, pd.Period]) -> list[pd.Period]:
    if o.design is None:
        return []
    kept = set(o.design.X.index)
    return [q for q in pd.period_range(window[0], window[1], freq="Q-DEC") if q not in kept]


def _variant_note2(o: VariantOutcome2, window: tuple[pd.Period, pd.Period]) -> str:
    if o.spec.k_source == "aic":
        return "K elegido por AIC sobre la misma muestra M"
    parts = []
    excluded = _excluded_quarters(o, window)
    if excluded:
        parts.append(f"excluye {_ranges_text(excluded)}; los trimestres vecinos se tratan como contiguos en la "
                     "ventana HAC")
    if not o.spec.covid_dummies:
        parts.append("sin dummies COVID")
    return "; ".join(parts)


def robustness_estimates2(outcomes: list[VariantOutcome2],
                          window: tuple[pd.Period, pd.Period] | None = None) -> pd.DataFrame:
    """Una fila por variante: K, muestra, observaciones, ventana HAC, S y S_rez, h* y H1 (RF-22).

    «no estimada» y «no aplica» llevan su estado y motivo y «—» en el resto.
    """
    rows = []
    for o in outcomes:
        base = {"variante": o.spec.id, "etiqueta": o.spec.label, "estado": o.status, "motivo": o.reason}
        if not o.estimated:
            rows.append({**base, "K": pd.NA, "inicio": _DASH, "fin": _DASH, "n_obs": pd.NA, "rezagos_hac": pd.NA,
                         "S": np.nan, "ee_S": np.nan, "p_S": np.nan, "S_rez": np.nan, "ee_S_rez": np.nan,
                         "p_S_rez": np.nan, "h_estrella": pd.NA, "h1": _DASH, "nota": ""})
            continue
        index = o.design.X.index
        e = o.effects
        rows.append({
            **base, "K": o.K, "inicio": quarter_label(index.min()), "fin": quarter_label(index.max()),
            "n_obs": int(o.fit.nobs), "rezagos_hac": int(o.fit.hac_lags),
            "S": e["S"]["est"], "ee_S": e["S"]["se"], "p_S": e["S"]["p"],
            "S_rez": e["S_rez"]["est"], "ee_S_rez": e["S_rez"]["se"], "p_S_rez": e["S_rez"]["p"],
            "h_estrella": o.peak["h_star"],
            "h1": f"{o.hyp['h1_signo']}; {'respaldada' if o.hyp['h1_respaldada'] == 'sí' else 'no respaldada'}",
            "nota": _variant_note2(o, window) if window else "",
        })
    df = pd.DataFrame(rows)
    for col in ("K", "n_obs", "rezagos_hac", "h_estrella"):
        df[col] = df[col].astype("Int64")
    return df


def robustness_summary2(main_effects: dict, outcomes: list[VariantOutcome2]) -> pd.DataFrame:
    """S_rez (y S) por variante: «sí», «no», «no estimada» o «no aplica», y el recuento «k de n» (RF-24).

    Criterio pre-registrado: mismo signo que la principal y p < 0,10 con errores HAC. n cuenta solo las
    variantes estimadas.
    """
    rows = []
    for key, label in (("S_rez", "S_rez (efecto de los rezagos)"), ("S", "S (efecto acumulado)")):
        row: dict = {"termino": key, "etiqueta": label, "p_principal": main_effects[key]["p"]}
        k = n = 0
        for o in outcomes:
            if not o.estimated:
                row[o.spec.id] = o.status
                continue
            ok = is_robust(main_effects[key]["est"], o.effects[key]["est"], o.effects[key]["p"], ROBUST_ALPHA)
            row[o.spec.id] = "sí" if ok else "no"
            k += int(ok)
            n += 1
        row.update({"k": k, "n": n, "robustez": f"{k} de {n}"})
        rows.append(row)
    return pd.DataFrame(rows)


def robustness_note2(outcomes: list[VariantOutcome2], window: tuple[pd.Period, pd.Period]) -> str:
    """Pie de la tabla resumen de robustez (RF-24): criterio, K, exclusiones y rezagos que salen de ellas."""
    ks = ", ".join(f"{o.spec.id} = {o.K}" if o.K is not None else f"{o.spec.id} {o.status}" for o in outcomes)
    parts = [
        "criterio de robustez: mismo signo que la principal y p < 0,10 con errores HAC, aplicado a S_rez (se "
        "reporta también S); «k de n» cuenta solo las variantes estimadas («no estimada» y «no aplica» salen del "
        "denominador); «sí» significa el mismo signo que la principal, aunque ese signo sea contrario al "
        "esperado",
        f"K: {ks}",
    ]
    leaks = []
    for o in outcomes:
        if o.spec.k_source == "aic":
            continue
        excluded = _excluded_quarters(o, window)
        if not excluded:
            continue
        if o.spec.exclude_zero_rate:
            parts.append(f"{o.spec.id} excluye {len(excluded)} trimestres de tasa cero ({_ranges_text(excluded)})")
        else:
            parts.append(f"{o.spec.id} excluye {_ranges_text(excluded)}")
        lagged = lagged_from_excluded(o.design, o.K, set(excluded))
        if lagged:
            leaks.append(f"{o.spec.id}: {_ranges_text(lagged)}")
    if leaks:
        parts.append("trimestres cuyos rezagos salen de trimestres excluidos (historia transformada), calculados "
                     "por código: " + "; ".join(leaks))
    return "Nota: " + "; ".join(parts) + "."


# --- Limitaciones (RF-25) ---


def _diagnostic_detail2(row: pd.Series) -> str:
    stat, p = row["estadístico"], row["p_valor"]
    if pd.notna(p):
        detail = f"estadístico {fmt_es(stat, 3)}, {'p < 0,001' if p < 0.001 else f'p = {fmt_es(p, 3)}'}"
    elif pd.notna(stat):
        detail = f"estadístico {fmt_es(stat, 3)}"
    else:
        detail = "sin estadístico"
    prueba = str(row["prueba"])
    if prueba == "Breusch-Godfrey":
        detail += ("; con el rezago de la dependiente, MCO puede ser inconsistente (se declara como limitación; "
                   "añadir rezagos tras ver el resultado exige un /sdd-change)")
    elif prueba.startswith("VIF"):
        detail += "; posible multicolinealidad: se reporta y no se elimina ningún regresor"
    elif row["nota"]:
        detail += f"; {row['nota']}"
    else:
        detail += "; se reporta y se discute qué implica para las conclusiones"
    return detail


def limitations_table2(K: int, k_aic: int, k_bic: int, diagnostics: pd.DataFrame, fit: Fit,
                       outcomes: list[VariantOutcome2], lp: pd.DataFrame, model_stationarity: pd.DataFrame,
                       window: tuple[pd.Period, pd.Period]) -> pd.DataFrame:
    """Limitaciones fijas más las detectadas por el código (RF-25)."""
    rows = [{"limitacion": n, "detalle": d, "origen": "fija"} for n, d in FIXED_LIMITATIONS2]

    def add(name: str, detail: str) -> None:
        rows.append({"limitacion": name, "detalle": detail, "origen": "detectada"})

    for label, value in (("K_BIC", k_bic), ("K_AIC", k_aic)):
        if value == K_MAX:
            add(f"{label} = {K_MAX}", f"el óptimo según {label[2:]} puede estar fuera del rango 1..{K_MAX}; el "
                                       "rango no se amplía")
    for _, r in diagnostics[diagnostics["veredicto"].isin(["falla", "alerta"])].iterrows():
        add(f"{r['prueba']}: {r['veredicto']}", _diagnostic_detail2(r))
    for _, r in diagnostics[diagnostics["veredicto"] == NOT_CALCULABLE].iterrows():
        add(f"{r['prueba']}: {NOT_CALCULABLE}", str(r["nota"]))
    if fit.psd_adjusted or any(o.estimated and o.fit.psd_adjusted for o in outcomes):
        where = (["principal"] if fit.psd_adjusted else []) + [o.spec.id for o in outcomes
                                                               if o.estimated and o.fit.psd_adjusted]
        add("Truncamiento espectral de la covarianza HAC",
            "Se aplicó al sub-bloque sin dummies de impulso en: " + ", ".join(where) + ".")
    for o in outcomes:
        if o.status == "no estimada":
            add(f"Variante {o.spec.id} no estimada", o.reason)
    off = lp[lp["estado"] == "no estimada"]
    if len(off):
        hs = ", ".join(f"h = {int(h)}" for h in off["h"])
        add("Horizontes de las proyecciones locales no estimados", f"{hs}: {'; '.join(sorted(set(off['motivo'])))}")
    flagged = [str(e).split(" — ")[0].split(" (")[0] for e in
               model_stationarity.loc[model_stationarity["no_i0"] == "sí", "etiqueta"]]
    if flagged:
        add("Regresores no I(0)",
            f"{', '.join(flagged)}: no son I(0) según la regla de la spec 001; entran en su forma fija y su no "
            "estacionariedad residual se declara como limitación.")
    leaks = covid_lag_leaks(fit.design, K)
    if leaks:
        first, last = (quarter_label(pd.Period(q, "Q-DEC")) for q in (COVID_QUARTERS[0], COVID_QUARTERS[-1]))
        add(f"Rezagos de ΔFFR o ΔDR desde {first}–{last} sin dummy",
            f"En {_ranges_text(leaks)} de la muestra principal, algún rezago de ΔFFR o de ΔDR sale de {first}–{last} "
            "y esos rezagos no llevan dummy propia.")
    return pd.DataFrame(rows, columns=["limitacion", "detalle", "origen"])


# --- Desviaciones (RF-26) ---


def deviations_table2(window: tuple[pd.Period, pd.Period], nobs: int) -> pd.DataFrame:
    """Desviaciones y decisiones frente a la guía y a la spec 003 (RF-26)."""
    first, last = (quarter_label(q) for q in window)
    rows = [(
        f"Muestra M {first}–{last} (n = {nobs}) en lugar de la del Modelo I, que empieza en "
        f"{quarter_label(MAIN_START)}",
        "Spec 003 y guía, sección 11",
        f"M empieza un trimestre después de la del Modelo I por los {K_MAX} rezagos de ΔFFR que exige el rango de "
        f"K; termina en {last}, el último trimestre común, y no en el 2026-01-01 del ejemplo de descarga de la guía.",
    )]
    rows.extend(FIXED_DEVIATIONS2)
    rows.extend((f"{fecha} · {cambio}", "Pre-registro de la spec 004", motivo)
                for fecha, cambio, motivo in PREREG_DEVIATIONS2)
    return pd.DataFrame(rows, columns=["decision", "referencia", "motivo"])


# --- Insumos de la sección 6.3 (RF-27) ---


def comparison_inputs(main_fit: Fit, window: tuple[pd.Period, pd.Period], coef1: pd.DataFrame,
                      footer1: dict) -> tuple[pd.DataFrame, str]:
    """θ0 del Modelo II y el coeficiente de ΔFFR(t) del Modelo I (leído de sus salidas), con su EE, p, muestra,
    observaciones y forma de los controles (RF-27)."""
    m1 = coef1.set_index("termino").loc["d_ffr"]
    inf = inference(main_fit.params, main_fit.cov).loc["d_ffr_l0"]
    rows = [
        {"modelo": "Modelo I (spec 003)", "termino": "ΔFFR(t)", "coef": float(m1["coef"]),
         "ee_hac": float(m1["ee_hac"]), "p": float(m1["p"]),
         "muestra": f"{footer1['muestra_inicio']}–{footer1['muestra_fin']}", "n_obs": int(footer1["n_obs"]),
         "controles": "contemporáneos (PIB, ΔU, π y ΔFFR del mismo trimestre; CRED rezagado 4 trimestres)"},
        {"modelo": "Modelo II (spec 004)", "termino": "θ0 = ΔFFR(t)", "coef": float(inf["coef"]),
         "ee_hac": float(inf["se"]), "p": float(inf["p"]),
         "muestra": f"{quarter_label(window[0])}–{quarter_label(window[1])}", "n_obs": int(main_fit.nobs),
         "controles": "rezagados (PIB, ΔU y π un trimestre; CRED cuatro trimestres)"},
    ]
    note = (
        "Nota: insumos para la comparación de la sección 6.3; el coeficiente del Modelo I se lee de las salidas de "
        "la spec 003; ambos son asociaciones condicionales con errores HAC y los controles de cada modelo entran en "
        "la forma indicada; la redacción de la comparación corresponde a la spec 006."
    )
    return pd.DataFrame(rows), note


# --- Exportación para la spec 005 (RF-29) ---


def _term_source(term: str) -> dict | None:
    if term == "y_lag":
        return {"column": "dralacbs", "lag": 1}
    if term.startswith("d_ffr_l"):
        return {"column": "fedfunds_d", "lag": int(term.removeprefix("d_ffr_l"))}
    if term in CONTROLS:
        column, lag = CONTROLS[term]
        return {"column": column, "lag": lag}
    return None


def export2(fit: Fit, K: int, trajectory: pd.DataFrame, peak: dict, reading: dict) -> dict:
    """Coeficientes, covarianza HAC, K, muestra, trayectoria y lectura para la prueba de estrés (RF-29)."""
    index = fit.design.X.index
    return {
        "spec": "004-modelo-ii",
        "dependent": "dralacbs",
        "form": fit.design.form,
        "k": int(K),
        "k_criterion": "BIC",
        "terms": list(fit.params.index),
        "columns": {t: _term_source(t) for t in fit.params.index},
        "params": fit.params.to_numpy(dtype=float).tolist(),
        "cov_hac": fit.cov.to_numpy(dtype=float).tolist(),
        "psd_adjusted": bool(fit.psd_adjusted),
        "hac_lags": int(fit.hac_lags),
        "sample_start": quarter_label(index.min()),
        "sample_end": quarter_label(index.max()),
        "nobs": int(fit.nobs),
        "covid_quarters": [quarter_label(pd.Period(q, "Q-DEC")) for q in COVID_QUARTERS],
        "psi": trajectory["psi"].astype(float).tolist(),
        "response": trajectory["R"].astype(float).tolist(),
        "h_star": {"h": int(peak["h_star"]), "signo": peak["signo"]},
        "reading": {"etiqueta": reading["etiqueta"], "c1": bool(reading["c1"]), "c2": bool(reading["c2"])},
    }


def export2_json(export: dict) -> str:
    """JSON determinista (claves en orden, floats con precisión completa, sin NaN)."""
    return json.dumps(export, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


# --- Salida en Markdown y CSV como texto (RF-30) ---


def fmt_kpss_p2(p: float) -> str:
    """p de KPSS como en la spec 001: statsmodels lo trunca a [0,01; 0,10]; «> 0,10» y «< 0,01» (D9)."""
    if pd.isna(p):
        return _DASH
    if p >= 0.10 - 1e-12:
        return "> 0,10"
    if p <= 0.01 + 1e-12:
        return "< 0,01"
    return fmt_es(p, 3)


def _is_p_column(name: str) -> bool:
    return name in ("p", "p_valor", "adf_p") or name.startswith("p_")


def _format_cell(column: str, value) -> str:
    if value is None or value is pd.NA or (isinstance(value, float) and np.isnan(value)):
        return _DASH
    if column == "kpss_p":
        return fmt_kpss_p2(float(value))
    if _is_p_column(column) and not isinstance(value, str):
        return fmt_p(float(value))
    if isinstance(value, (bool, np.bool_)):
        return "sí" if value else "no"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)):
        return fmt_es(float(value), 3)
    return str(value)


def _format_for_markdown2(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({c: [_format_cell(c, v) for v in df[c]] for c in df.columns}, index=df.index)


def render_model2_tables(result: Model2Result) -> dict[str, dict[str, str]]:
    """Las 14 tablas del Modelo II como texto Markdown y CSV, sin escribir a disco (RF-30).

    El Markdown usa coma decimal, «< 0,001» y «—» para los valores nulos; el CSV conserva la precisión
    completa con punto decimal y «—» en los nulos. Las tablas que lo exigen cierran con su nota.
    """
    tables = {
        "model2_selection": (result.selection, result.selection_note),
        "model2_coefficients": (result.coefficients, result.coef_note),
        "model2_effects": (result.effects, result.effects_note),
        "model2_trajectory": (result.trajectory, result.trajectory_note),
        "model2_reading": (result.reading_table, result.reading_note),
        "model2_lp": (result.lp, result.lp_note),
        "model2_comparison": (result.comparison, result.comparison_note),
        "model2_diagnostics": (result.diagnostics, ""),
        "model2_stationarity": (result.stationarity, result.stationarity_note),
        "model2_robustness_estimates": (result.robustness_estimates, ""),
        "model2_robustness_summary": (result.robustness_summary, result.robustness_note),
        "model2_limitations": (result.limitations, ""),
        "model2_deviations": (result.deviations, ""),
        "model2_inputs63": (result.inputs63, result.inputs63_note),
    }
    out: dict[str, dict[str, str]] = {}
    for stem, (df, note) in tables.items():
        md = to_markdown(_format_for_markdown2(df))
        if note:
            md += "\n\n" + note
        out[stem] = {"md": md, "csv": df.to_csv(index=False, lineterminator="\n", na_rep=_DASH)}
    return out


# --- Orquestación (RF-2 a RF-27) ---


def run_model2(full: pd.DataFrame, stationarity: pd.DataFrame, end: pd.Period, result1) -> Model2Result:
    """Estima el Modelo II completo: selección, principal, robusteces y tablas.

    1. Comprueba la forma de DRALACBS (RF-2) antes de estimar nada.
    2. Calcula la muestra común M con K = 8 (RF-3) y estima un modelo por K = 1..8 sobre ella; si alguno
       no tiene grados de libertad o rango completo, se detiene nombrando el K (RF-5).
    3. K_BIC es el principal (RF-6); calcula efectos, trayectoria, Granger, lectura (RF-10 a RF-13),
       proyecciones locales y su comparación (RF-14 a RF-17), diagnósticos y estacionariedad.
    4. Estima R1–R3 (RF-22 a RF-24), arma limitaciones, desviaciones, insumos de la 6.3 (con el coeficiente de
       ΔFFR(t) que `result1`, el Modelo I, ya calculó) y la exportación para la spec 005.
    """
    decisions = read_decisions(stationarity)
    check_expected_forms(decisions, {"dralacbs": EXPECTED_FORM})
    decision = decisions["dralacbs"]
    cols = build_columns(full, decision)
    window = common_window(cols, end)
    fits: dict[int, Fit] = {}
    for K in K_RANGE:
        design: Design = build_design2(full, MAIN2, K, decision, window, end)
        reason = check_dof(design)
        if reason:
            raise ModelDataError(f"K = {K}: {reason}")
        fits[K] = fit_ols_hac(design)
    nobs = fits[K_RANGE[0]].nobs
    sel = select_k(fits)
    K = sel["k_bic"]
    main = fits[K]
    effects = cumulative_effects(main, K)
    traj = multipliers(main.params, K)
    peak = peak_horizon(traj["psi"])
    granger = granger_lags(main, K)
    hyp = hypotheses(effects, peak)
    reading = evidence_reading(granger, effects)
    lp = run_local_projections(full, K, decision, window, end)
    trajectory = trajectory_table(traj, peak)
    comparison, counts = compare_with_trajectory(trajectory, lp)
    footer = coefficient_footer2(main, K)
    variants = [run_variant2(full, spec, K, sel["k_aic"], decision, window, end) for spec in ROBUST2]
    diagnostics = diagnostics_table2(main, K)
    stationarity2 = stationarity_table2(stationarity)
    inputs63, inputs63_note = comparison_inputs(main, window, result1.coefficients, result1.coef_footer)
    return Model2Result(
        decision=decision, window=window, nobs=nobs, K=K, k_aic=sel["k_aic"], k_bic=sel["k_bic"],
        fits=fits, main_fit=main,
        selection=selection_table(sel), selection_note=selection_note(window, nobs, sel["k_aic"], sel["k_bic"]),
        coefficients=coefficients_table2(main), coef_footer=footer, coef_note=coefficient_note2(footer),
        effects_raw=effects, effects=effects_table2(effects, hyp, K), effects_note=effects_note2(K),
        peak=peak, hyp=hyp, trajectory=trajectory,
        trajectory_note=trajectory_note(float(main.params["y_lag"]), peak, hyp),
        granger=granger, reading=reading, reading_table=reading_table2(granger, effects, reading, K),
        reading_note=reading_note2(K),
        lp=lp, comparison=comparison, comparison_counts=counts, comparison_note=comparison_note2(counts),
        diagnostics=diagnostics, cusum=cusum(main),
        stationarity=stationarity2, stationarity_note=stationarity_note2(),
        lp_note=lp_note2(), variants=variants,
        robustness_estimates=robustness_estimates2(variants, window),
        robustness_summary=robustness_summary2(effects, variants),
        robustness_note=robustness_note2(variants, window),
        limitations=limitations_table2(K, sel["k_aic"], sel["k_bic"], diagnostics, main, variants, lp,
                                       stationarity2, window),
        deviations=deviations_table2(window, nobs), inputs63=inputs63, inputs63_note=inputs63_note,
        export=export2(main, K, trajectory, peak, reading),
    )
