"""Presentation-only stress figures from approved summary CSVs; no estimation."""
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from src.stress_figures import stress_figure, LABELS


def stress_presentation_figure(levels, delta, model):
    def summaries(frame):
        selected = frame.loc[frame.modelo == model]
        result = {}
        for scenario in ('base', 'severo', 'propio'):
            rows = selected.loc[selected.escenario == scenario].copy()
            if rows.empty:
                continue
            rows.index = pd.PeriodIndex(rows.trimestre.str.replace('T', 'Q', regex=False), freq='Q')
            if 'n_fuera_rango' in rows:
                rows.attrs['n_fuera_rango'] = rows.n_fuera_rango.max()
            result[scenario] = rows
        return result
    level_frames, delta_frames = summaries(levels), summaries(delta)
    fig = stress_figure(level_frames, delta_frames)
    for axis in fig.axes:
        for line in axis.lines:
            if line.get_label() == LABELS['severo']:
                line.set_linewidth(2.4)
                line.set_linestyle('-')
            elif line.get_label() == LABELS['propio']:
                line.set_linestyle('--')
                line.set_marker('o')
                line.set_markersize(4)
                line.set_markerfacecolor('none')
                line.set_linewidth(1.2)
        axis.legend(fontsize=8)
    coincident = (level_frames['severo']['dr'].equals(level_frames['propio']['dr'])
                  and delta_frames['severo']['delta'].equals(delta_frames['propio']['delta']))
    if coincident:
        fig.text(.05, .005, 'Adverso y D coinciden bajo la regla de tasa en cero; se distinguen por línea y marcadores.', fontsize=8)
    return fig


def stress_presentation_png(levels, delta, model):
    fig = stress_presentation_figure(levels, delta, model)
    try:
        stream = BytesIO()
        fig.savefig(stream, format='png', metadata={'Software': None})
        return stream.getvalue()
    finally:
        plt.close(fig)
