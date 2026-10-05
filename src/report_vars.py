"""Variables para `report/_variables.yml` (spec 001).

Función pura que devuelve el bloque `datos:` con textos ya formateados.
Principio 5: las cifras del informe salen de aquí con `{{< var datos.xxx >}}`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.panel import PanelResult
from src.config import COLUMN_LABELS, MAIN_SERIES
from src.model1 import Model1Result, fmt_p, term_label
from src.model1_config import COVID_QUARTERS, MACRO_TERMS
from src.tables import fmt_es, quarter_label


def data_variables(
    result: PanelResult,
    stationarity: pd.DataFrame,
    manifest: pd.DataFrame,
) -> dict:
    """Construye el diccionario `datos:` para `report/_variables.yml`.

    Todos los valores son **strings ya formateados** (coma decimal, 2 decimales,
    trimestres como 'AAAAT#').
    """
    # Fecha de descarga más reciente
    manifest["download_date"] = pd.to_datetime(manifest["download_date"])
    fecha_descarga = manifest["download_date"].max().strftime("%Y-%m-%d")

    # Trimestres excluidos
    if result.excluded_tail:
        excl = sorted({quarter_label(q) for q, _, _ in result.excluded_tail})
        trimestres_excluidos = ", ".join(excl)
    else:
        trimestres_excluidos = "ninguno"

    # Meses 2025T4 para CPI y UNRATE
    cpi_meses = "2" if result.gap_treatment.get("CPIAUCSL") == "RF-11" else "3"
    unrate_meses = "2" if result.gap_treatment.get("UNRATE") == "RF-11" else "3"

    # Descriptivos de DRALACBS
    dralacbs = result.panel["dralacbs"].dropna()
    dralacbs_media = fmt_es(dralacbs.mean())
    dralacbs_desv = fmt_es(dralacbs.std(ddof=1))
    dralacbs_max = fmt_es(dralacbs.max())
    dralacbs_max_q = quarter_label(dralacbs.idxmax())
    dralacbs_min = fmt_es(dralacbs.min())
    dralacbs_min_q = quarter_label(dralacbs.idxmin())
    dralacbs_ultimo = fmt_es(dralacbs.iloc[-1])

    # Descriptivos de UNRATE
    unrate = result.panel["unrate"].dropna()
    unrate_max = fmt_es(unrate.max())
    unrate_max_q = quarter_label(unrate.idxmax())

    # Descriptivos de FEDFUNDS
    fedfunds = result.panel["fedfunds"].dropna()
    fedfunds_max = fmt_es(fedfunds.max())
    fedfunds_ultimo = fmt_es(fedfunds.iloc[-1])

    # Decisiones y orden (solo filas "tal cual")
    tal_cual = stationarity[stationarity["forma"] == "tal cual"]
    decision = dict(zip(tal_cual["variable"], tal_cual["decision"]))
    orden = dict(zip(tal_cual["variable"], tal_cual["orden"]))

    # Número de ambiguas
    n_ambiguas = str((tal_cual["decision"] == "ambigua (primera diferencia)").sum())

    # Número de trimestres en la muestra
    n_trimestres = str(len(result.panel))

    return {
        "muestra_inicio": "2000T1",
        "muestra_fin": quarter_label(result.end),
        "n_trimestres": n_trimestres,
        "n_series": str(len(MAIN_SERIES) + len([c for c in result.panel.columns if c.startswith("dralac") and c not in ["dralacbs"]])),
        "fecha_descarga": fecha_descarga,
        "trimestres_excluidos": trimestres_excluidos,
        "cpiaucsl_2025t4_meses": cpi_meses,
        "unrate_2025t4_meses": unrate_meses,
        "dralacbs_media": dralacbs_media,
        "dralacbs_desv": dralacbs_desv,
        "dralacbs_max": dralacbs_max,
        "dralacbs_max_trimestre": dralacbs_max_q,
        "dralacbs_min": dralacbs_min,
        "dralacbs_min_trimestre": dralacbs_min_q,
        "dralacbs_ultimo": dralacbs_ultimo,
        "unrate_max": unrate_max,
        "unrate_max_trimestre": unrate_max_q,
        "fedfunds_max": fedfunds_max,
        "fedfunds_ultimo": fedfunds_ultimo,
        "decision": decision,
        "orden": orden,
        "n_ambiguas": n_ambiguas,
    }

# --- Bloque `modelo1:` (spec 003, tarea 8; RF-22) ---
# Todo texto ya formateado, con coma decimal: coeficientes y efectos con 3 decimales, p-valores
# con 3 decimales o «< 0,001», métricas fuera de muestra con 2 decimales y trimestres «AAAAT#».
# Ninguna cifra se escribe a mano: todo sale de las tablas del `Model1Result`. Un efecto «no
# reportado» o «no definido» va como texto, nunca como número.


def _m1_join_es(items: list[str]) -> str:
    if not items:
        return "ninguno"
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " y " + items[-1]


def _m1_short(termino: str) -> str:
    return term_label(termino).split(" (")[0]


def _m1_effects(effects: pd.DataFrame) -> dict:
    out: dict = {}
    for term in effects["termino"].unique():
        block: dict = {}
        for efecto, ek in (("impacto", "impacto"), ("largo plazo", "largo")):
            for escala, sk in (("por 1 pp", "pp"), ("por 1 DE", "de")):
                sel = (effects["termino"] == term) & (effects["efecto"] == efecto) & (effects["escala"] == escala)
                row = effects[sel].iloc[0]
                if row["estado"] == "reportado":
                    vals = [fmt_es(row["estimacion"], 3), fmt_es(row["ee"], 3), fmt_p(row["p"]),
                            fmt_es(row["ic_inf"], 3), fmt_es(row["ic_sup"], 3)]
                else:
                    vals = [str(row["estado"])] * len(_M1_EFFECT_SUFFIXES)
                for suffix, val in zip(_M1_EFFECT_SUFFIXES, vals):
                    block[f"{ek}_{sk}{suffix}"] = val
        out[term] = block
    return out


_M1_EFFECT_SUFFIXES = ("", "_ee", "_p", "_ic_inf", "_ic_sup")
_M1_DIAG_KEYS = {
    "Breusch-Godfrey": "bg", "Breusch-Pagan": "bp", "White": "white",
    "Jarque-Bera": "jb", "RESET": "reset",
}


def _m1_diag(diagnostics: pd.DataFrame) -> dict:
    tab = diagnostics.set_index("prueba")

    def block(name: str) -> dict:
        r = tab.loc[name]
        return {"estadistico": fmt_es(r["estadístico"], 3), "p": fmt_p(r["p_valor"]),
                "veredicto": str(r["veredicto"])}

    out = {key: block(name) for name, key in _M1_DIAG_KEYS.items()}
    for name in [n for n in tab.index if str(n).startswith("Chow ")]:
        out["chow_" + str(name).split(" ")[1].lower().replace("q", "t")] = block(name)
    out["cusum"] = {"veredicto": str(tab.loc["CUSUM", "veredicto"])}
    out["vif"] = {
        str(n).removeprefix("VIF (").removesuffix(")"): {
            "valor": fmt_es(tab.loc[n, "estadístico"], 3), "veredicto": str(tab.loc[n, "veredicto"]),
        }
        for n in tab.index if str(n).startswith("VIF (")
    }
    return out


def _m1_oos(table: pd.DataFrame) -> dict:
    t = table.set_index("pronostico")
    uno, din = t.loc["a un paso"], t.loc["dinámico"]
    out = {"n_trimestres": str(int(uno["n_trimestres"]))}
    for suffix, row in (("un_paso", uno), ("dinamico", din)):
        out[f"rmse_modelo_{suffix}"] = fmt_es(row["rmse_modelo"], 2)
        out[f"rmse_ingenuo_{suffix}"] = fmt_es(row["rmse_ingenuo"], 2)
        out[f"mae_modelo_{suffix}"] = fmt_es(row["mae_modelo"], 2)
        out[f"mae_ingenuo_{suffix}"] = fmt_es(row["mae_ingenuo"], 2)
        out[f"cociente_{suffix}"] = fmt_es(row["cociente_rmse"], 2)
    out["dm_estadistico"] = fmt_es(uno["dm_estadistico"], 2)
    out["dm_p"] = fmt_p(uno["dm_p"])
    out["veredicto_un_paso"] = str(uno["veredicto"])
    out["veredicto_dinamico"] = str(din["veredicto"])
    out["significancia_un_paso"] = str(uno["significancia"])
    return out


def _m1_sample(o) -> dict:
    if not o.estimated:
        return {"estado": "no estimada", "motivo": o.reason, "inicio": "—", "fin": "—", "n_obs": "—"}
    index = o.design.X.index
    return {"estado": "estimada", "motivo": "", "inicio": quarter_label(index.min()),
            "fin": quarter_label(index.max()), "n_obs": str(int(o.fit.nobs))}


def model1_variables(result: Model1Result) -> dict:
    """Construye el bloque `modelo1:` de `report/_variables.yml` (RF-22).

    Se cita en el informe como `{{< var modelo1.efectos.d_unemp.impacto_pp >}}`. La etapa
    `models` del pipeline reescribe solo esta clave y conserva las demás.
    """
    f = result.coef_footer
    coef = result.coefficients.set_index("termino")
    summary = result.robustness_summary.set_index("termino")
    macro = [t for t in MACRO_TERMS if t in coef.index]
    flagged = [_m1_short(t) for t in result.stationarity.loc[result.stationarity["no_i0"] == "sí", "termino"]]
    return {
        "estimador": "MCO con errores Newey-West (HAC, kernel de Bartlett)",
        "forma_y": f["forma_y"],
        "muestra_inicio": f["muestra_inicio"],
        "muestra_fin": f["muestra_fin"],
        "n_obs": str(f["n_obs"]),
        "n_parametros": str(f["n_parametros"]),
        "rezagos_hac": str(f["rezagos_hac"]),
        "dummies_covid": _m1_join_es([quarter_label(pd.Period(q, "Q-DEC")) for q in COVID_QUARTERS]),
        "truncamiento_espectral": "sí" if f["truncamiento_espectral"] else "no",
        "r2": fmt_es(f["r2"], 3),
        "r2_ajustado": fmt_es(f["r2_ajustado"], 3),
        "ee_regresion": fmt_es(f["ee_regresion"], 3),
        "variantes": {o.spec.id: o.spec.label for o in result.variants},
        "coef": {
            t: {
                "coef": fmt_es(r["coef"], 3), "ee": fmt_es(r["ee_hac"], 3), "p": fmt_p(r["p"]),
                "ic_inf": fmt_es(r["ic_inf"], 3), "ic_sup": fmt_es(r["ic_sup"], 3),
            }
            for t, r in coef.iterrows()
        },
        "efectos": _m1_effects(result.effects),
        "signo": {t: str(coef.loc[t, "coincide"]) for t in macro},
        "diag": _m1_diag(result.diagnostics),
        "robustez": {t: str(summary.loc[t, "robustez"]) for t in macro},
        "variantes_muestra": {o.spec.id: _m1_sample(o) for o in result.variants},
        "oos": _m1_oos(result.oos.table),
        "no_i0": _m1_join_es(flagged),
        "limitaciones": [f"{r.limitacion}: {r.detalle}" for r in result.limitations.itertuples()],
        "desviaciones": [
            f"{r.decision} ({r.referencia}): {r.motivo}" for r in result.deviations.itertuples()
        ],
    }
