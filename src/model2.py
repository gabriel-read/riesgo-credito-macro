"""Orquestación pura del Modelo II (spec 004): selección de K, principal y tablas (tarea 5).

Estima un modelo por K = 1..8 sobre la muestra común M, elige K por BIC (principal) y AIC (R1),
calcula efectos acumulados, trayectoria, Granger, lectura de la evidencia, proyecciones locales y
su comparación, diagnósticos y estacionariedad. Devuelve un `Model2Result` con tablas como
DataFrame y sus notas de pie como texto. Las robusteces, limitaciones, desviaciones, exportación y la
salida en Markdown/CSV se añaden en la tarea 6. Sin acceso a red, disco ni gráficos (RNF-7).
RF-2 a RF-21.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.design import Design, ModelDataError, check_expected_forms, diff_form_stationary, read_decisions
from src.design2 import build_columns, build_design2, common_window
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
from src.model1_config import ALPHA, CHOW_BREAKS, VIF_ALERT
from src.model2_config import (
    CHOW_POST_MIN,
    CONTROLS,
    EXPECTED_FORM,
    K_RANGE,
    MAIN2,
    RHO_WARN,
    dffr_cols,
    term_label2,
)
from src.stationarity import is_stationary
from src.tables import fmt_es, quarter_label

IMPULSE_SE_NOTE = "EE HAC no informativo: dummy de impulso con residuo nulo"
RANK_NOTE = "rango reducido por dummies de impulso (esperado)"
NOT_CALCULABLE = "no calculable"
SIZE_NOTE = "el tamaño empírico del contraste puede diferir del 5 % nominal"
_DASH = "—"


@dataclass(frozen=True)
class Model2Result:
    """Resultado del Modelo II hasta la tarea 5 (las robusteces y exportaciones llegan en la tarea 6)."""

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
        "ψ_h es la respuesta de ΔDR (pp por trimestre) y R(h) la del nivel de la morosidad (pp) a un shock "
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
        (f"Granger: θ1 = … = θ{K} = 0", granger["stat"], float(granger["df"]), granger["p"], granger["veredicto"]),
        ("C1: Granger rechaza al 5 %", np.nan, np.nan, np.nan, "sí" if reading["c1"] else "no"),
        ("C2: S_rez > 0 con p < 0,05", s_rez["chi2"], 1.0, s_rez["p"], "sí" if reading["c2"] else "no"),
        ("Lectura de «¿hay efectos rezagados?»", np.nan, np.nan, np.nan, label),
    ]
    return pd.DataFrame(rows, columns=["elemento", "estadistico", "gl", "p", "resultado"])


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


# --- Orquestación (RF-2 a RF-21) ---


def run_model2(full: pd.DataFrame, stationarity: pd.DataFrame, end: pd.Period) -> Model2Result:
    """Estima el Modelo II hasta la especificación principal y sus tablas.

    1. Comprueba la forma de DRALACBS (RF-2) antes de estimar nada.
    2. Calcula la muestra común M con K = 8 (RF-3) y estima un modelo por K = 1..8 sobre ella; si alguno
       no tiene grados de libertad o rango completo, se detiene nombrando el K (RF-5).
    3. K_BIC es el principal (RF-6); calcula efectos, trayectoria, Granger, lectura (RF-10 a RF-13),
       proyecciones locales y su comparación (RF-14 a RF-17), diagnósticos y estacionariedad.
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
        diagnostics=diagnostics_table2(main, K), cusum=cusum(main),
        stationarity=stationarity_table2(stationarity), stationarity_note=stationarity_note2(),
    )
