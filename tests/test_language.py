"""Lenguaje de asociación en las salidas del Modelo I (spec 003, RNF-7, principio 5).

Los resultados se describen como asociación, nunca como causalidad. Un test revisa las tablas,
las variables de texto y las figuras generadas, y falla si aparece alguna de las expresiones
prohibidas. Los nombres técnicos «efecto de impacto» y «efecto de largo plazo» están permitidos
(la spec los define como asociaciones condicionales). Datos sintéticos; sin datos reales.
"""

from __future__ import annotations

import re

import matplotlib.pyplot as plt
import pytest

from src.figures import plot_model1_coefficients, plot_model1_cusum, plot_model1_oos
from src.model1 import render_model1_tables
from src.model1_config import FIXED_DEVIATIONS, FIXED_LIMITATIONS, PREREG_DEVIATIONS
from src.report_vars import model1_variables

BANNED = ("causa", "causal", "provoca", "debido a")
# de la más larga a la más corta: con «causa|causal», «causal» casaría como «causa»
BANNED_RE = re.compile("|".join(re.escape(w) for w in sorted(BANNED, key=len, reverse=True)),
                       flags=re.IGNORECASE)


def find_causal_language(text: str) -> list[str]:
    """Expresiones de causalidad que aparecen en `text` (sin distinguir mayúsculas)."""
    return [m.group(0).lower() for m in BANNED_RE.finditer(text)]


def _strings(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield str(k)
            yield from _strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _strings(v)
    elif obj is not None:
        yield str(obj)


# --- La guarda detecta lo que debe y deja pasar lo permitido ---


@pytest.mark.parametrize("text, found", [
    ("el PIB causa la morosidad", ["causa"]),
    ("relación causal", ["causal"]),
    ("la tasa provoca más impagos", ["provoca"]),
    ("aumento debido a la crisis", ["debido a"]),
    ("Debido A la tasa", ["debido a"]),
    ("CAUSA y Causal", ["causa", "causal"]),
    ("la causalidad no se identifica", ["causal"]),  # «causalidad» también es lenguaje causal
])
def test_guard_detects_causal_language(text, found):
    assert find_causal_language(text) == found


@pytest.mark.parametrize("text", [
    "efecto de impacto", "efecto de largo plazo", "se asocia con", "anticipa", "precede",
    "asociación condicional", "pp de morosidad por 1 DE", "ΔFFR se asocia con la morosidad",
    "el rechazo se reporta tal cual",
])
def test_guard_allows_association_language_and_the_technical_effect_names(text):
    assert find_causal_language(text) == []


# --- Salidas del Modelo I ---


def test_rendered_tables_have_no_causal_language(model1_result):
    out = render_model1_tables(model1_result)
    for stem, d in out.items():
        assert find_causal_language(d["md"]) == [], stem
        assert find_causal_language(d["csv"]) == [], stem


def test_report_variables_have_no_causal_language(model1_result):
    mv = model1_variables(model1_result)
    bad = {s: find_causal_language(s) for s in _strings(mv) if find_causal_language(s)}
    assert not bad, bad


def test_fixed_limitation_and_deviation_texts_have_no_causal_language():
    texts = [*(t for pair in FIXED_LIMITATIONS for t in pair),
             *(t for triple in FIXED_DEVIATIONS for t in triple),
             *(t for triple in PREREG_DEVIATIONS for t in triple)]
    assert texts and all(find_causal_language(t) == [] for t in texts)


def _figure_texts(fig) -> list[str]:
    out = [t.get_text() for t in fig.texts]
    for ax in fig.axes:
        out += [ax.get_xlabel(), ax.get_ylabel(), ax.get_title()]
        out += [t.get_text() for t in ax.get_xticklabels() + ax.get_yticklabels()]
        out += [ln.get_label() for ln in ax.lines]
        if ax.get_legend():
            out += [t.get_text() for t in ax.get_legend().get_texts()]
    return out


def test_figures_have_no_causal_language(model1_result):
    figs = [
        plot_model1_coefficients(model1_result.effects),
        plot_model1_cusum(model1_result.cusum),
        plot_model1_oos(model1_result.oos),
    ]
    try:
        for fig in figs:
            texts = _figure_texts(fig)
            assert any(texts)
            assert all(find_causal_language(t) == [] for t in texts), texts
    finally:
        for fig in figs:
            plt.close(fig)
