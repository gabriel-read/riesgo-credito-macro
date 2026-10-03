"""Formato de tablas y etiquetas (spec 001).

Funciones puras: número con coma decimal, trimestre a 'AAAAT#', tabla Markdown.
Sin acceso a red, disco ni gráficos (RNF-6). RF-18, RF-19, RNF-5.
"""

from __future__ import annotations

import pandas as pd


def fmt_es(x: float, decimals: int = 2) -> str:
    """Formatea float con coma decimal y N decimales; NaN -> '—'."""
    if pd.isna(x):
        return "—"
    # Formatear con punto decimal, luego cambiar punto por coma
    s = f"{round(x, decimals):.{decimals}f}"
    return s.replace(".", ",")


def quarter_label(q: pd.Period) -> str:
    """Convierte Period trimestral a 'AAAAT#' (p.ej., 2026Q2 -> '2026T2')."""
    return f"{q.year}T{q.quarter}"


def to_markdown(df: pd.DataFrame, decimals: int = 2) -> str:
    """Convierte DataFrame a tabla Markdown pipe sin dependencias externas."""
    if df.empty:
        return ""

    # Preparar datos formateados
    fmt_df = df.copy()
    for col in fmt_df.columns:
        if pd.api.types.is_numeric_dtype(fmt_df[col]):
            fmt_df[col] = fmt_df[col].apply(lambda x: fmt_es(x, decimals))
        else:
            fmt_df[col] = fmt_df[col].astype(str)

    # Cabecera
    header = "| " + " | ".join(fmt_df.columns) + " |"
    sep = "| " + " | ".join(["---"] * len(fmt_df.columns)) + " |"

    # Filas
    rows = []
    for _, row in fmt_df.iterrows():
        rows.append("| " + " | ".join(row.astype(str)) + " |")

    return "\n".join([header, sep] + rows)