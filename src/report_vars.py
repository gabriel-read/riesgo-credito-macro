"""Variables para `report/_variables.yml` (spec 001).

Función pura que devuelve el bloque `datos:` con textos ya formateados.
Principio 5: las cifras del informe salen de aquí con `{{< var datos.xxx >}}`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.panel import PanelResult
from src.config import COLUMN_LABELS, MAIN_SERIES
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