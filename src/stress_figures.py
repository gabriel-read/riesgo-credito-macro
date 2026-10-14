"""Deterministic stress figures built in memory, with no filesystem writes."""
from __future__ import annotations

from io import BytesIO

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.tables import quarter_label

LABELS = {'base': 'Base adaptada', 'severo': 'Adverso adaptado', 'propio': 'D: actividad adversa y alza de tasas'}
COLORS = {'base': '#2563eb', 'severo': '#dc2626', 'propio': '#7c3aed'}


def stress_figure(levels: dict, delta: dict) -> plt.Figure:
    fig, axes = plt.subplots(2, 1, figsize=(9, 7), dpi=200, sharex=True)
    for scenario, summary in levels.items():
        x = summary.index.to_timestamp()
        axes[0].plot(x, summary.dr.to_numpy(), label=LABELS[scenario], color=COLORS[scenario])
        axes[0].fill_between(x, summary.p05.to_numpy(), summary.p95.to_numpy(),
                             color=COLORS[scenario], alpha=.12)
    for scenario, summary in delta.items():
        x = summary.index.to_timestamp()
        axes[1].plot(x, summary.delta.to_numpy(), label=LABELS[scenario], color=COLORS[scenario])
        axes[1].fill_between(x, summary.p05.to_numpy(), summary.p95.to_numpy(),
                             color=COLORS[scenario], alpha=.12)
    axes[0].set_ylabel('Morosidad proyectada (pp)')
    axes[1].set_ylabel('Cambio adverso − base (pp)')
    axes[1].set_xlabel('Trimestre')
    index = next(iter(levels.values())).index
    ticks = list(range(0, len(index), 2))
    axes[1].set_xticks(index[ticks].to_timestamp(), [quarter_label(index[j]) for j in ticks], rotation=45)
    axes[1].axhline(0, color='gray', linewidth=.8)
    for axis in axes:
        axis.legend(fontsize=8)
        axis.grid(alpha=.2)
    fig.text(.05, .065, 'Bandas: incertidumbre de parámetros; no es un intervalo de predicción.', fontsize=8)
    if any(s.attrs.get('n_fuera_rango', 0) for s in levels.values()):
        fig.text(.05, .045, 'Advertencia: se reportan niveles fuera de rango, sin truncamiento.', fontsize=8)
    fig.text(.05, .025, 'Fuente: FRED, Reserva Federal (escenarios 2026), adaptación propia.', fontsize=8)
    fig.tight_layout(rect=(0, .09, 1, 1))
    return fig


def stress_figure_png(levels: dict, delta: dict) -> bytes:
    fig = stress_figure(levels, delta)
    stream = BytesIO()
    try:
        fig.savefig(stream, format='png', metadata={'Software': None})
        return stream.getvalue()
    finally:
        plt.close(fig)
