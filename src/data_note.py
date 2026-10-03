"""Nota de datos en Markdown (spec 001).

Función pura que devuelve la nota en español.
Sin acceso a red, disco ni gráficos (RNF-6). RF-17.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.panel import PanelResult
from src.config import SERIES_META, COLUMN_LABELS, MAIN_SERIES, ROBUSTNESS_SERIES


def build_data_note(
    result: PanelResult,
    manifest: pd.DataFrame,
    meta: dict,
) -> str:
    """Construye la nota de datos completa en Markdown (español)."""
    lines = []

    # 1. Tabla por serie
    lines.append("## 1. Series descargadas\n")
    lines.append(
        "| Código | Nombre | Fuente | Unidad | Frecuencia original | "
        "Rango descargado | Fecha descarga | Tratamiento trimestral |"
    )
    lines.append(
        "|--------|--------|--------|--------|---------------------|------------------|----------------|----------------------|"
    )

    for _, row in manifest.iterrows():
        sid = row["series"]
        m = meta.get(sid, {})
        lines.append(
            f"| {sid} | {m.get('nombre', '')} | "
            f"FRED, vía {row['source']} | {m.get('unidad', '')} | "
            f"{m.get('frecuencia', '')} | {row['first_obs']} a {row['last_obs']} | "
            f"{row['download_date']} | {m.get('tratamiento_trimestral', '')} |"
        )

    # 2. Muestra de estimación
    lines.append("\n## 2. Muestra de estimación\n")
    lines.append(f"La muestra de estimación va de **2000T1** a **{quarter_label(result.end)}**.")

    if result.excluded_tail:
        lines.append("\n**Trimestres excluidos al final de la muestra:**")
        for q, sid, motivo in result.excluded_tail:
            lines.append(f"- {quarter_label(q)}: {sid} ({motivo})")

    # 3. Tratamiento 2025T4
    lines.append("\n## 3. Tratamiento de 2025T4 (CPIAUCSL y UNRATE)\n")
    for sid in ["CPIAUCSL", "UNRATE"]:
        trat = result.gap_treatment.get(sid)
        if trat == "RF-11":
            lines.append(
                f"- **{sid}**: octubre 2025 no disponible (marcador de faltante de FRED). "
                f"El promedio de 2025T4 se calcula con noviembre y diciembre únicamente (**RF-11**)."
            )
        elif trat == "RF-12":
            lines.append(
                f"- **{sid}**: octubre 2025 disponible. El promedio de 2025T4 usa los tres meses (**RF-12**)."
            )
        else:
            lines.append(f"- **{sid}**: sin tratamiento especial documentado.")

    lines.append(
        "\n**Cálculos afectados en la muestra**: el nivel y la diferencia trimestral de 2025T4, "
        "la diferencia trimestral de 2026T1, y la variación interanual de 2025T4 (y de 2026T4 en adelante, "
        "si entra en la muestra) usan este promedio de dos meses para CPIAUCSL y UNRATE."
    )

    # 4. Mezcla de frecuencias
    lines.append("\n## 4. Mezcla de frecuencias\n")
    lines.append(
        "Las series de morosidad (DRALACBS, DRALACBN, DRCLACBS, DRBLACBS, DRSREACBS) y de castigos "
        "(CORALACBS) son **datos de fin de periodo** (valor del último mes del trimestre). "
        "Las series macroeconómicas mensuales (UNRATE, CPIAUCSL, FEDFUNDS, LOANS) se promedian "
        "en el trimestre calendario (**media de los meses del trimestre**). "
        "USREC es indicador: 1 si algún mes del trimestre está en recesión."
    )

    # 5. Justificación LOANS
    lines.append("\n## 5. Por qué LOANS mide el crédito\n")
    lines.append(
        "LOANS (Préstamos y arrendamientos en crédito bancario, bancos comerciales, H.8) "
        "cubre el mismo universo de bancos que el denominador de DRALACBS. "
        "Se usa su **variación interanual** como proxy del crecimiento del crédito bancario."
    )

    # 6. FEDFUNDS en nivel y diferencia
    lines.append("\n## 6. Por qué FEDFUNDS entra en nivel y en diferencia trimestral\n")
    lines.append(
        "El **nivel** (FEDFUNDS) mide la postura de la política monetaria. "
        "La **diferencia trimestral** (FEDFUNDS_D) captura el «cambio en la FFR» "
        "que solicita la sección 3.4 de la guía. "
        "Qué versión entra en cada modelo lo deciden las specs 003 y 004."
    )

    # 7. Faltantes terminales (RF-25)
    if result.terminal_gaps:
        lines.append("\n## 7. Series con faltante terminal (RF-25)\n")
        for col, last_q in result.terminal_gaps.items():
            lines.append(f"- **{col}**: último trimestre con dato = {quarter_label(last_q)}.")
        lines.append(
            "\nEl sombreado de recesiones en el gráfico (RF-22) termina donde termina USREC "
            f"({quarter_label(result.terminal_gaps.get('usrec', result.end))})."
        )

    return "\n".join(lines)


def quarter_label(q: pd.Period) -> str:
    """Convierte Period trimestral a 'AAAAT#' (p.ej., 2026Q2 -> '2026T2')."""
    return f"{q.year}T{q.quarter}"