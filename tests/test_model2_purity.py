"""Pureza de los módulos del Modelo II (spec 004, RNF-9; tarea 7).

La estimación, la selección, los efectos, las proyecciones, los diagnósticos y las tablas son funciones
puras: sin red, disco ni gráficos, sin aleatoriedad, y sin rellenar ni descartar faltantes. Los módulos
leen solo lo que reciben como argumento (no abren archivos ni URL). Análisis estático con `ast`.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tests.test_pipeline import MISSING_DATA_OPS, MODEL1_FORBIDDEN_IMPORTS, _imported_roots

PURE_MODULES = [
    "src/model2_config.py",
    "src/design2.py",
    "src/dynamics.py",
    "src/localproj.py",
    "src/model2.py",
    # compartidos con el Modelo I y ampliados por la 004
    "src/estimation.py",
    "src/diagnostics.py",
    "src/design.py",
]
FORBIDDEN_IMPORTS = MODEL1_FORBIDDEN_IMPORTS | {"random", "http", "ftplib", "smtplib", "ssl"}
READ_CALLS = {"read_csv", "read_json", "read_excel", "read_parquet", "read_pickle", "read_html", "read_table",
              "read_text", "read_bytes", "read_fwf", "urlopen", "urlretrieve", "download"}
WRITE_CALLS = {"to_json", "to_excel", "to_parquet", "to_pickle", "write_text", "write_bytes", "savefig", "mkdir"}


def _tree(path: str) -> ast.AST:
    return ast.parse(Path(path).read_text(encoding="utf-8"), filename=path)


@pytest.mark.parametrize("path", PURE_MODULES)
def test_module_has_no_forbidden_imports(path):
    bad = _imported_roots(_tree(path)) & FORBIDDEN_IMPORTS
    assert not bad, f"{path}: importa {sorted(bad)}"


@pytest.mark.parametrize("path", PURE_MODULES)
def test_module_never_fills_or_drops_missing_data(path):
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Attribute) and node.attr in MISSING_DATA_OPS:
            pytest.fail(f"{path}:{node.lineno}: usa .{node.attr}() sobre datos del modelo")
        if isinstance(node, ast.Name) and node.id in MISSING_DATA_OPS:
            pytest.fail(f"{path}:{node.lineno}: usa {node.id}")


@pytest.mark.parametrize("path", PURE_MODULES)
def test_module_does_not_read_or_write_files_or_urls(path):
    for node in ast.walk(_tree(path)):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in ("open", "input", "exec", "eval", "__import__"):
            pytest.fail(f"{path}:{node.lineno}: llama a {func.id}()")
        if isinstance(func, ast.Attribute):
            assert func.attr not in READ_CALLS, f"{path}:{node.lineno}: lee de una fuente externa ({func.attr})"
            assert func.attr not in WRITE_CALLS, f"{path}:{node.lineno}: escribe ({func.attr})"
            if func.attr == "to_csv":
                # solo a texto: sin ruta (el primer argumento de to_csv sería un archivo)
                assert not node.args and all(k.arg not in ("path_or_buf", "path") for k in node.keywords), (
                    f"{path}:{node.lineno}: to_csv escribe a una ruta"
                )


@pytest.mark.parametrize("path", PURE_MODULES)
def test_module_has_no_randomness(path):
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Attribute) and node.attr in ("random", "default_rng", "RandomState", "seed"):
            pytest.fail(f"{path}:{node.lineno}: usa aleatoriedad ({node.attr})")


def test_model2_functions_of_report_vars_and_figures_never_fill_or_drop():
    for path, picks in (("src/report_vars.py", lambda n: n == "model2_variables" or n.startswith("_m2_")),
                        ("src/figures.py", lambda n: n.startswith("plot_model2_") or n == "_num")):
        checked = 0
        for node in ast.walk(_tree(path)):
            if isinstance(node, ast.FunctionDef) and picks(node.name):
                checked += 1
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Attribute):
                        assert sub.attr not in MISSING_DATA_OPS, f"{path}:{node.name}: usa .{sub.attr}()"
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == "open":
                        pytest.fail(f"{path}:{node.name}: contiene open()")
        assert checked >= 2, path


def test_the_purity_guard_detects_what_it_should():
    src = "import requests\nimport pandas as pd\ndef f(df):\n    df = df.dropna()\n    return open('x')\n"
    tree = ast.parse(src)
    assert _imported_roots(tree) & FORBIDDEN_IMPORTS == {"requests"}
    attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    assert attrs & MISSING_DATA_OPS == {"dropna"}
    assert any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "open"
               for n in ast.walk(tree))


def test_pure_modules_exist_and_import_without_the_network(monkeypatch):
    import importlib
    import socket

    def _boom(*a, **k):
        raise RuntimeError("red")

    monkeypatch.setattr(socket, "getaddrinfo", _boom)
    for mod in ("src.design2", "src.dynamics", "src.localproj", "src.model2", "src.model2_config"):
        importlib.import_module(mod)
