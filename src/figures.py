"""Gráfico de morosidad, desempleo y FFR (spec 001).

Construye y devuelve la Figure de RF-22; no la guarda.
Gráficos (sin disco). RF-22.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
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


# --- Figuras del Modelo I (spec 003, tarea 8) ---
# Cada función construye y devuelve la Figure; ninguna la guarda (RNF-6). 8×4,5 pulgadas,
# 200 dpi, sin título, con el pie de fuente. El informe pone el pie de figura numerado.

_FOOTER = "Fuente: FRED; elaboración propia"


def _model1_figure() -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)
    fig.subplots_adjust(left=0.16, right=0.97, top=0.96, bottom=0.2)
    fig.text(0.01, 0.01, _FOOTER, fontsize=8, ha="left", va="bottom")
    return fig, ax


def _quarter_axis(ax: plt.Axes, index: pd.PeriodIndex, max_labels: int = 8) -> None:
    """Eje x por posición, con los trimestres rotulados como «AAAAT#»."""
    need = -(-len(index) // max_labels)
    # pasos de 1, 2 o múltiplos de 4 trimestres: el trimestre del rótulo es siempre el mismo
    step = next((s for s in (1, 2, 4, 8, 16, 20, 40) if s >= need), need)
    pos = list(range(0, len(index), step))
    ax.set_xticks(pos)
    ax.set_xticklabels([f"{index[i].year}T{index[i].quarter}" for i in pos])
    ax.set_xlabel("Trimestre")


def plot_model1_coefficients(effects: pd.DataFrame) -> plt.Figure:
    """Efecto de impacto por 1 DE de cada regresor macro, con su IC 95 % (RF-11).

    Usa las filas «impacto» y «por 1 DE» de la tabla de efectos, en pp de morosidad. Los
    regresores con efecto «no definido» (DE nula) no se dibujan y se anotan al pie.
    """
    rows = effects[(effects["efecto"] == "impacto") & (effects["escala"] == "por 1 DE")]
    ok = rows[rows["estado"] == "reportado"].reset_index(drop=True)
    if ok.empty:
        raise ValueError("no hay efectos por 1 DE que dibujar: todos figuran como no definidos")
    fig, ax = _model1_figure()
    est = ok["estimacion"].to_numpy(dtype=float)
    y = np.arange(len(ok))
    xerr = [est - ok["ic_inf"].to_numpy(dtype=float), ok["ic_sup"].to_numpy(dtype=float) - est]
    ax.errorbar(est, y, xerr=xerr, fmt="o", color="#1f77b4", ecolor="#1f77b4", elinewidth=1.6)
    ax.axvline(0, color="gray", linewidth=1, linestyle="--")
    ax.set_yticks(y)
    ax.set_yticklabels([s.split(" (")[0] for s in ok["etiqueta"]])
    ax.invert_yaxis()
    ax.set_xlabel("pp de morosidad por 1 DE del regresor (efecto de impacto, IC 95 %)")
    skipped = [s.split(" (")[0] for s in rows.loc[rows["estado"] != "reportado", "etiqueta"]]
    if skipped:
        fig.text(0.01, 0.07, "No definido (DE nula): " + ", ".join(skipped), fontsize=8,
                 ha="left", va="bottom")
    return fig


def plot_model1_cusum(cusum: dict) -> plt.Figure:
    """CUSUM de residuos recursivos con sus bandas al 5 % (RF-14)."""
    index = cusum["cusum"].index
    x = np.arange(len(index))
    fig, ax = _model1_figure()
    ax.plot(x, cusum["cusum"].to_numpy(dtype=float), color="#1f77b4", linewidth=1.5, label="CUSUM")
    ax.plot(x, cusum["lower"].to_numpy(dtype=float), color="black", linestyle="--",
            linewidth=1.1, label="Bandas al 5 %")
    ax.plot(x, cusum["upper"].to_numpy(dtype=float), color="black", linestyle="--",
            linewidth=1.1, label="_nolegend_")
    ax.legend(loc="upper left", frameon=False)
    ax.set_ylabel("Suma acumulada de residuos recursivos")
    _quarter_axis(ax, index)
    return fig


def plot_model1_oos(oos) -> plt.Figure:
    """Morosidad observada frente a los pronósticos fuera de muestra (RF-19).

    Exactamente 4 series: observada, modelo a un paso, modelo dinámico e ingenuo a un paso
    (paseo aleatorio). El ingenuo constante desde el ancla queda en `oos.series` y en la tabla
    de métricas para la auditoría numérica, pero no se dibuja para no saturar el gráfico.
    """
    s = oos.series
    fig, ax = _model1_figure()
    x = np.arange(len(s))
    styles = [
        ("observado", "Observada", "black", "-", 2.0),
        ("un_paso", "Modelo a un paso", "#1f77b4", "-", 1.5),
        ("dinamico", "Modelo dinámico", "#d95f02", "--", 1.5),
        ("ingenuo_un_paso", "Ingenuo a un paso (paseo aleatorio)", "gray", ":", 1.6),
    ]
    for col, label, color, linestyle, width in styles:
        ax.plot(x, s[col].to_numpy(dtype=float), color=color, linestyle=linestyle,
                linewidth=width, label=label)
    ax.legend(loc="best", frameon=False)
    ax.set_ylabel("Tasa de morosidad (%)")
    _quarter_axis(ax, s.index)
    return fig
