"""Correcciones de la ronda 1 de la auditoría de la spec 004 (`review-audit-ronda1.md`).

Punto 1: el contrato `columns` de `model2_main.json` apunta a la serie del panel que de verdad entra al
modelo (ΔDR es `dralacbs_d`, no el nivel `dralacbs`). Punto 2: la notación de las tablas no se rompe con
K = 1 («θ0 + θ1», «θ1 = 0», «θ1», «ΔFFR(t) y ΔFFR(t−1)»); con K ≥ 2 se mantiene la forma general.
Datos sintéticos; sin red.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.design2 import build_columns, build_design2, common_window
from src.estimation import fit_ols_hac
from src.model2 import (
    diagnostics_table2,
    effects_note2,
    effects_table2,
    reading_note2,
    reading_table2,
    render_model2_tables,
    run_model2,
)
from src.model2_config import EXPECTED_FORM, MAIN2
from src.report_vars import model2_variables
from tests.synthetic_model1 import make_stationarity
from tests.synthetic_model2 import END, make_full2

DEC = EXPECTED_FORM
BROKEN = ["θ0+…+θ1", "θ1+…+θ1", "θ1 = … = θ1", "θ1..θ1", "t..t−1)", "ΔFFR(t..t−1"]


def _fit(K: int):
    full = make_full2()
    window = common_window(build_columns(full, DEC), END)
    return fit_ols_hac(build_design2(full, MAIN2, K, DEC, window, END))


def _effects(est=0.5, p=0.01):
    return {"S": {"est": est, "se": 0.1, "chi2": 25.0, "p": p, "ic_inf": 0.3, "ic_sup": 0.7},
            "S_rez": {"est": est, "se": 0.1, "chi2": 25.0, "p": p, "ic_inf": 0.3, "ic_sup": 0.7}}


# --- Punto 1: el JSON apunta a la serie que entra en el modelo ---


def test_export_y_lag_points_to_the_differenced_series(model2_result):
    assert model2_result.export["columns"]["y_lag"] == {"column": "dralacbs_d", "lag": 1}


def test_every_exported_column_exists_in_the_panel_and_is_the_series_in_the_design(model2_result):
    full = make_full2()
    r = model2_result
    X = r.main_fit.design.X
    for term, src in r.export["columns"].items():
        if src is None:                                    # constante y dummies COVID
            assert term == "const" or term.startswith("covid_"), term
            continue
        assert src["column"] in full.columns, f"{term}: {src['column']} no existe en el panel"
        series = full[src["column"]].shift(src["lag"]).reindex(X.index)
        assert np.allclose(series.to_numpy(float), X[term].to_numpy(float), rtol=0, atol=1e-12), term


def test_the_differenced_column_is_the_one_that_enters_the_model(model2_result):
    full = make_full2()
    assert np.allclose(full["dralacbs_d"].iloc[1:], full["dralacbs"].diff().iloc[1:])
    y = model2_result.main_fit.design.y
    assert np.allclose(full["dralacbs_d"].reindex(y.index).to_numpy(float), y.to_numpy(float), atol=1e-12)
    assert model2_result.export["form"] == "primera diferencia"


# --- Punto 2: notación con K = 1 y con K ≥ 2 ---


def test_effects_labels_k1_and_general():
    k1 = effects_table2(_effects(), {"h1_signo": "sí", "h1_respaldada": "sí"}, 1)
    assert list(k1["descripcion"]) == ["θ0 + θ1", "θ1"]
    for K in (2, 3, 8):
        t = effects_table2(_effects(), {"h1_signo": "sí", "h1_respaldada": "sí"}, K)
        assert list(t["descripcion"]) == [f"θ0+…+θ{K}", f"θ1+…+θ{K}"]


def test_effects_note_k1_and_general():
    n1 = effects_note2(1)
    assert "S = θ0 + θ1 y S_rez = θ1" in n1 and not any(b in n1 for b in BROKEN)
    for K in (2, 3):
        assert f"S = θ0+…+θ{K} y S_rez = θ1+…+θ{K}" in effects_note2(K)


def _reading(K):
    eff = _effects()
    granger = {"stat": 3.0, "df": K, "p": 0.04, "veredicto": "rechaza"}
    reading = {"c1": True, "c2": True, "etiqueta": "evidencia fuerte", "signo_contrario": False}
    return reading_table2(granger, eff, reading, K), reading_note2(K)


def test_reading_labels_k1_and_general():
    table, note = _reading(1)
    assert table.iloc[0]["elemento"] == "Granger: θ1 = 0"
    assert "χ²(1) sobre θ1 (se excluye θ0" in note and not any(b in note for b in BROKEN)
    for K in (2, 3, 8):
        table, note = _reading(K)
        assert table.iloc[0]["elemento"] == f"Granger: θ1 = … = θ{K} = 0"
        assert f"χ²({K}) sobre θ1..θ{K} (se excluye θ0" in note


def test_chow_note_k1_and_general():
    notes1 = diagnostics_table2(_fit(1), 1).set_index("prueba")
    for name in ("Chow 2008T3", "Chow 2020T2"):
        n = notes1.loc[name, "nota"]
        assert "interacciones de 8 términos" in n and "ΔFFR(t) y ΔFFR(t−1)" in n
        assert not any(b in n for b in BROKEN)
    for K in (2, 3):
        n = diagnostics_table2(_fit(K), K).set_index("prueba").loc["Chow 2008T3", "nota"]
        assert f"interacciones de {K + 7} términos" in n and f"ΔFFR(t..t−{K})" in n


# --- Extremo a extremo: con K = 1 ninguna salida conserva la notación rota ---


@pytest.fixture(scope="module")
def result_k1(model1_result):
    full = make_full2(theta=(0.30, 0.20))                  # K verdadero = 1
    r = run_model2(full, make_stationarity(), END, model1_result)
    assert r.K == 1
    return r


def _all_text(r) -> str:
    parts = []
    for t in render_model2_tables(r).values():
        parts += [t["md"], t["csv"]]
    mv = model2_variables(r)

    def leaves(o):
        if isinstance(o, dict):
            for v in o.values():
                yield from leaves(v)
        elif isinstance(o, list):
            for v in o:
                yield from leaves(v)
        else:
            yield str(o)

    return "\n".join(parts + list(leaves(mv)))


def test_k1_outputs_have_no_broken_notation(result_k1):
    text = _all_text(result_k1)
    for b in BROKEN:
        assert b not in text, b
    assert "θ0 + θ1" in text and "Granger: θ1 = 0" in text and "ΔFFR(t) y ΔFFR(t−1)" in text


def test_k1_limitations_carry_the_k1_chow_note(result_k1):
    lim = result_k1.limitations
    chow = lim[lim["limitacion"].str.startswith("Chow")]
    for detail in chow["detalle"]:
        assert "ΔFFR(t) y ΔFFR(t−1)" in detail


def test_general_k_outputs_keep_the_general_notation(model2_result):
    K = model2_result.K
    assert K >= 2                                           # el proceso sintético por defecto elige K = 3
    text = _all_text(model2_result)
    assert f"θ0+…+θ{K}" in text and f"θ1+…+θ{K}" in text and f"θ1 = … = θ{K} = 0" in text
