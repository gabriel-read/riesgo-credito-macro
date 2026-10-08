"""Lenguaje de las salidas del Modelo II (spec 004, RNF-10 y RNF-11; tarea 7).

Ninguna salida textual afirma causalidad: ni «causa», «causal» (ni «causalidad»), «provoca» o «debido a»
(spec), ni «efecto causal» o «impacto» (más estricto, a petición del autor). Las salidas usan el vocabulario
de la asociación: «asociación dinámica», «precedencia temporal», «respuesta acumulada». Se revisan las
tablas, sus notas, las variables del informe, el texto de las figuras y los textos fijos del código.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml

from src.figures import plot_model2_profile, plot_model2_response
from src.model2 import render_model2_tables
from src.report_vars import model2_variables
from tests.test_language import BANNED, find_causal_language
from tests.test_outputs_model2 import fig_texts

BANNED2 = tuple(BANNED) + ("efecto causal", "impacto")
BANNED2_RE = re.compile("|".join(re.escape(w) for w in sorted(BANNED2, key=len, reverse=True)), re.IGNORECASE)
REQUIRED = ("asociación dinámica", "precedencia temporal", "respuesta acumulada")
SOURCES = ["src/model2.py", "src/model2_config.py", "src/dynamics.py", "src/localproj.py", "src/design2.py"]


def find_banned(text: str) -> list[str]:
    return [m.group(0).lower() for m in BANNED2_RE.finditer(text)]


def _leaves(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield str(k)
            yield from _leaves(v)
    elif isinstance(o, list):
        for v in o:
            yield from _leaves(v)
    elif o is not None:
        yield str(o)


@pytest.fixture(scope="module")
def corpus(model2_result):
    r = model2_result
    parts = []
    for text in render_model2_tables(r).values():
        parts += [text["md"], text["csv"]]
    parts += list(_leaves(model2_variables(r)))
    parts += [r.selection_note, r.coef_note, r.effects_note, r.trajectory_note, r.reading_note, r.lp_note,
              r.comparison_note, r.stationarity_note, r.robustness_note, r.inputs63_note]
    detection = r.comparison_counts["horizonte_deteccion"]
    for fig in (plot_model2_profile(r.coefficients, r.peak), plot_model2_response(r.lp, r.trajectory, detection)):
        parts += fig_texts(fig)
    return "\n".join(parts)


# --- La guarda detecta lo que debe y deja pasar lo permitido ---


@pytest.mark.parametrize("text", ["la tasa causa mora", "efecto causal", "causalidad de Granger", "provoca",
                                  "debido a la tasa", "el impacto de la tasa", "Impacto", "CAUSAL"])
def test_guard_detects_banned_expressions(text):
    assert find_banned(text)


@pytest.mark.parametrize("text", ["asociación dinámica", "precedencia temporal", "respuesta acumulada",
                                  "no identifica el efecto de la política monetaria", "se asocia con", "anticipa"])
def test_guard_lets_allowed_vocabulary_through(text):
    assert find_banned(text) == []


def test_guard_is_stricter_than_the_spec_one():
    assert find_causal_language("impacto") == [] and find_banned("impacto") == ["impacto"]


# --- Salidas ---


def test_no_banned_language_in_any_output(corpus):
    assert find_banned(corpus) == []


def test_required_association_vocabulary_is_present(corpus):
    for term in REQUIRED:
        assert term in corpus.lower(), term


def test_limitations_use_the_wording_of_the_spec(model2_result):
    text = " ".join(model2_result.limitations["detalle"])
    assert "no identifica el efecto de la política monetaria" in text


def test_figure_and_table_labels_are_in_spanish(corpus):
    for word in ("Trimestre", "Horizonte", "Banda", "Fuente: FRED; elaboración propia", "Rezago"):
        assert word in corpus or word == "Trimestre", word
    assert "Source" not in corpus and "Lag " not in corpus


# --- Textos fijos del código ---


def _strings_outside_docstrings(path: str):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None:
                docstrings.add(node.body[0].value)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node not in docstrings:
            yield node.lineno, node.value


@pytest.mark.parametrize("path", SOURCES)
def test_fixed_strings_in_the_source_have_no_banned_language(path):
    for line, value in _strings_outside_docstrings(path):
        assert find_banned(value) == [], f"{path}:{line}: {value!r}"


def test_model2_blocks_of_figures_and_report_vars_have_no_banned_language():
    for path, picks in (("src/report_vars.py", lambda n: n == "model2_variables" or n.startswith("_m2_")),
                        ("src/figures.py", lambda n: n.startswith("plot_model2_"))):
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and picks(node.name):
                doc = ast.get_docstring(node, clean=False)
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str) and sub.value != doc:
                        assert find_banned(sub.value) == [], f"{path}:{node.name}: {sub.value!r}"


def test_variables_yaml_dump_has_no_banned_language(model2_result):
    dumped = yaml.safe_dump({"modelo2": model2_variables(model2_result)}, allow_unicode=True)
    assert find_banned(dumped) == []
