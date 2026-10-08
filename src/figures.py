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


# --- Modelo II (spec 004) ---


def plot_model2_profile(coefficients: pd.DataFrame, peak: dict) -> plt.Figure:
    """Perfil de los coeficientes θ_j (j = 0..K) con su IC 95 % HAC y una línea en cero (RF-9).

    Usa las filas ΔFFR(t−j) de la tabla de coeficientes. Si el trimestre de efecto máximo h* de la
    trayectoria cae dentro de 0..K, se marca con una línea vertical.
    """
    rows = coefficients[coefficients["termino"].str.startswith("d_ffr_l")].reset_index(drop=True)
    if rows.empty:
        raise ValueError("no hay coeficientes de ΔFFR que dibujar")
    j = np.array([int(t.removeprefix("d_ffr_l")) for t in rows["termino"]])
    est = rows["coef"].to_numpy(dtype=float)
    yerr = [est - rows["ic_inf"].to_numpy(dtype=float), rows["ic_sup"].to_numpy(dtype=float) - est]
    fig, ax = _model1_figure()
    ax.errorbar(j, est, yerr=yerr, fmt="o", color="#1f77b4", ecolor="#1f77b4", elinewidth=1.6,
                capsize=3, label="θ_j con IC 95 % (HAC)")
    ax.axhline(0, color="gray", linewidth=1, linestyle="--")
    if peak["h_star"] <= j.max():
        ax.axvline(peak["h_star"], color="#d62728", linewidth=1.1, linestyle=":",
                   label=f"Trimestre de efecto máximo h* = {peak['h_star']}")
    ax.set_xticks(j)
    ax.set_xlabel("Rezago j (trimestres)")
    ax.set_ylabel("pp de morosidad por 1 pp de ΔFFR(t−j)")
    ax.legend(loc="best", frameon=False)
    return fig


def _num(series: pd.Series) -> np.ndarray:
    return pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)


def plot_model2_response(lp: pd.DataFrame, trajectory: pd.DataFrame, detection: str) -> plt.Figure:
    """Dos paneles (RF-18): respuesta acumulada de la morosidad y respuesta de la tasa, h = 0..12.

    Izquierda: β_h con su banda del 90 % HAC y R(h) del modelo de rezagos distribuidos superpuesta; si
    hay horizonte de detección se marca con una línea vertical. Derecha: φ_h con su banda del 90 %
    (φ_0 = 1 por construcción, sin banda). Los horizontes «no estimada» quedan como huecos.
    """
    h = _num(lp["h"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5), dpi=200)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.96, bottom=0.36, wspace=0.28)
    fig.text(0.01, 0.01, _FOOTER, fontsize=8, ha="left", va="bottom")

    beta = _num(lp["beta"])
    ax1.fill_between(h, _num(lp["ic90_inf"]), _num(lp["ic90_sup"]), color="#1f77b4", alpha=0.2,
                     linewidth=0, label="Banda al 90 % (HAC)")
    ax1.plot(h, beta, color="#1f77b4", marker="o", markersize=3, linewidth=1.5, label="β_h (proyección local)")
    ax1.plot(_num(trajectory["h"]), _num(trajectory["R"]), color="black", linestyle="--", linewidth=1.2,
             label="R(h) (rezagos distribuidos)")
    ax1.axhline(0, color="gray", linewidth=1)
    if detection != "ninguno":
        ax1.axvline(float(detection.removeprefix("h")), color="#d62728", linestyle=":", linewidth=1.1,
                    label=f"Horizonte de detección ({detection.replace('h', 'h = ')})")
    ax1.set_xlabel("Horizonte h (trimestres)")
    ax1.set_ylabel("pp de morosidad por 1 pp de ΔFFR(t)")
    ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), frameon=False, fontsize=7)

    ax2.fill_between(h, _num(lp["phi_ic90_inf"]), _num(lp["phi_ic90_sup"]), color="#2ca02c", alpha=0.2,
                     linewidth=0, label="Banda al 90 % (HAC)")
    ax2.plot(h, _num(lp["phi"]), color="#2ca02c", marker="o", markersize=3, linewidth=1.5,
             label="φ_h (respuesta de la tasa)")
    ax2.axhline(0, color="gray", linewidth=1)
    ax2.set_xlabel("Horizonte h (trimestres)")
    ax2.set_ylabel("pp de la tasa por 1 pp de ΔFFR(t)")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), frameon=False, fontsize=7)
    return fig
