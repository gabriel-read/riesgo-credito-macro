"""Gráfico de morosidad, desempleo y FFR (spec 001).

Construye y devuelve la Figure de RF-22; no la guarda.
Gráficos (sin disco). RF-22.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def plot_delinquency_macro(panel: pd.DataFrame) -> plt.Figure:
    """Gráfico RF-22: morosidad, desempleo, FFR con recesiones sombreadas.

    Parámetros
    ----------
    panel : DataFrame
        Panel de estimación con columnas 'dralacbs', 'unrate', 'fedfunds', 'usrec'.

    Returns
    -------
    matplotlib.figure.Figure
        Figura 8x4.5 pulgadas, 200 dpi, sin título.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)

    # Eje X: primer día de cada trimestre
    x = panel.index.to_timestamp(how="start")

    # Tres líneas
    ax.plot(x, panel["dralacbs"], label="Tasa de morosidad (DRALACBS)", linewidth=1.2)
    ax.plot(x, panel["unrate"], label="Tasa de desempleo (UNRATE)", linewidth=1.2)
    ax.plot(x, panel["fedfunds"], label="Tasa de fondos federales (FEDFUNDS)", linewidth=1.2)

    # Eje Y único en porcentaje
    ax.set_ylabel("Porcentaje (%)")

    # Leyenda en español
    ax.legend(loc="upper left", frameon=False)

    # Sombreado de recesiones: cada racha de usrec == 1
    usrec = panel["usrec"]
    in_recession = False
    start_idx = None

    for i, (idx, val) in enumerate(usrec.items()):
        if val == 1 and not in_recession:
            in_recession = True
            start_idx = i
        elif val == 0 and in_recession:
            in_recession = False
            end_idx = i
            # Sombrear desde start_idx hasta end_idx (excluyendo end_idx)
            ax.axvspan(x[start_idx], x[end_idx], alpha=0.2, color="gray", zorder=0)

    # Si termina en recesión, sombrear hasta el final
    if in_recession and start_idx is not None:
        ax.axvspan(x[start_idx], x[-1], alpha=0.2, color="gray", zorder=0)

    # Formato eje X: años
    ax.xaxis.set_major_locator(plt.matplotlib.dates.YearLocator(2))
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%Y"))

    plt.tight_layout()
    return fig