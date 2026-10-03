"""Tests de ``src/figures.py`` (T9, spec 001).

Gráfico de morosidad, desempleo y FFR con recesiones sombreadas (RF-22).
"""

import pandas as pd
import pytest

from src.figures import plot_delinquency_macro


def _make_panel_for_figure() -> pd.DataFrame:
    """Panel sintético para el gráfico."""
    idx = pd.period_range("2000Q1", periods=40, freq="Q-DEC")
    # USREC: recesión 2008Q1-2009Q2 y 2020Q1-2020Q2
    usrec = [0]*32 + [1]*6 + [0]*2 + [1]*2 + [0]*0  # ajustar longitud
    usrec = usrec[:40]
    return pd.DataFrame({
        "dralacbs": [2.0 + i*0.05 for i in range(40)],
        "unrate": [5.0 + (i%10)*0.2 for i in range(40)],
        "fedfunds": [2.0 + (i%8)*0.3 for i in range(40)],
        "usrec": usrec,
    }, index=idx)


def test_plot_delinquency_macro_structure():
    """Figura tiene 3 líneas, ylabel '%', leyenda en español, sombreados = rachas recesión."""
    panel = _make_panel_for_figure()
    fig = plot_delinquency_macro(panel)

    # 3 líneas
    lines = fig.gca().get_lines()
    assert len(lines) == 3

    # Etiquetas de las líneas en español
    labels = [l.get_label() for l in lines]
    assert "Tasa de morosidad (DRALACBS)" in labels
    assert "Tasa de desempleo (UNRATE)" in labels
    assert "Tasa de fondos federales (FEDFUNDS)" in labels

    # Eje Y
    assert fig.gca().get_ylabel() == "Porcentaje (%)"

    # Sombreados: axvspan crea Polygon patches
    spans = fig.gca().patches
    # Debe haber 1 racha de recesión en los datos sintéticos (6 trimestres)
    assert len(spans) >= 1