"""Tests de ``src/pipeline.py`` (T10, spec 001).

CLI, orquestación, escritura de salidas, RNF-1 (reproducibilidad), pureza módulos.
"""

import ast
import os
import sys
import tempfile
from pathlib import Path
import pandas as pd
import pytest

# Configurar PIPELINE_ROOT ANTES de importar pipeline
os.environ["PIPELINE_ROOT"] = str(Path(__file__).parent.parent)

from src.pipeline import main
from src.config import MAIN_SERIES


def test_pipeline_data_creates_all_outputs(tmp_path: Path):
    """pipeline data produce todas las salidas esperadas."""
    # Configurar root temporal
    os.environ["PIPELINE_ROOT"] = str(tmp_path)
    
    # Copiar data/raw al tmp_path para test aislado
    import shutil
    raw_src = Path("data/raw")
    raw_dst = tmp_path / "data" / "raw"
    shutil.copytree(raw_src, raw_dst)

    # Ejecutar pipeline data
    sys.argv = ["pipeline", "data"]
    main()

    # Verificar salidas
    assert (tmp_path / "data" / "processed" / "panel.csv").exists()
    assert (tmp_path / "outputs" / "data_note.md").exists()
    assert (tmp_path / "outputs" / "tables" / "descriptives.csv").exists()
    assert (tmp_path / "outputs" / "tables" / "descriptives.md").exists()
    assert (tmp_path / "outputs" / "tables" / "stationarity.csv").exists()
    assert (tmp_path / "outputs" / "tables" / "stationarity.md").exists()
    assert (tmp_path / "outputs" / "figures" / "delinquency_unemployment_ffr.png").exists()
    assert (tmp_path / "report" / "_variables.yml").exists()

    # Verificar panel
    panel = pd.read_csv(tmp_path / "data" / "processed" / "panel.csv", index_col=0)
    assert panel.index[0] == "2000Q1"
    assert len(panel.columns) == 25
    # Sin NaN en columnas principales
    for col in panel.columns:
        if col == "usrec":
            continue
        assert not panel[col].isna().any(), f"NaN en {col}"

    # Verificar manifiesto tiene 13 series
    manifest = pd.read_csv(raw_dst / "manifest.csv")
    assert len(manifest) == 13
    expected_series = set(MAIN_SERIES + ["DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS", "CORALACBS", "USREC"])
    assert set(manifest["series"]) == expected_series


def test_pipeline_reproducibility_rnf1(tmp_path: Path):
    """RNF-1: dos ejecuciones dan bytes idénticos en panel.csv, descriptives.csv, stationarity.csv."""
    os.environ["PIPELINE_ROOT"] = str(tmp_path)
    
    import shutil
    raw_src = Path("data/raw")
    raw_dst = tmp_path / "data" / "raw"
    shutil.copytree(raw_src, raw_dst)

    # Primera ejecución
    sys.argv = ["pipeline", "data"]
    main()

    panel1 = (tmp_path / "data" / "processed" / "panel.csv").read_bytes()
    desc1 = (tmp_path / "outputs" / "tables" / "descriptives.csv").read_bytes()
    stat1 = (tmp_path / "outputs" / "tables" / "stationarity.csv").read_bytes()

    # Segunda ejecución (borrar salidas pero mantener raw)
    for f in [
        tmp_path / "data" / "processed" / "panel.csv",
        tmp_path / "outputs" / "tables" / "descriptives.csv",
        tmp_path / "outputs" / "tables" / "stationarity.csv",
    ]:
        f.unlink()

    sys.argv = ["pipeline", "data"]
    main()

    panel2 = (tmp_path / "data" / "processed" / "panel.csv").read_bytes()
    desc2 = (tmp_path / "outputs" / "tables" / "descriptives.csv").read_bytes()
    stat2 = (tmp_path / "outputs" / "tables" / "stationarity.csv").read_bytes()

    assert panel1 == panel2, "panel.csv no reproducible"
    assert desc1 == desc2, "descriptives.csv no reproducible"
    assert stat1 == stat2, "stationarity.csv no reproducible"


def test_pipeline_modules_pure():
    """Módulos puros no importan requests, pandas_datareader, matplotlib ni usan open().
    
    figures.py SÍ puede importar matplotlib (RNF-6: gráficos permitidos ahí).
    """
    import ast

    pure_modules = [
        "src/panel.py",
        "src/stationarity.py",
        "src/descriptives.py",
        "src/tables.py",
        "src/data_note.py",
        "src/report_vars.py",
        "src/report_tables.py",
        "src/report_editorial.py",
        "src/config.py",
        "src/references.py",
        "src/scenarios.py",
        "src/stress.py",
        "src/stress_tables.py",
        "src/design.py",
        "src/estimation.py",
        "src/diagnostics.py",
        "src/forecast.py",
        "src/model1.py",
        "src/model1_config.py",
    ]

    forbidden_imports = {"requests", "pandas_datareader", "matplotlib", "urllib", "socket"}

    for mod_path in pure_modules:
        with open(mod_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=mod_path)

        for node in ast.walk(tree):
            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name not in forbidden_imports, f"{mod_path}: importa {alias.name}"
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    assert node.module not in forbidden_imports, f"{mod_path}: importa from {node.module}"


def test_pipeline_no_open_in_pure_modules():
    """Ningún archivo de src/ (salvo pipeline.py, fred_io.py) contiene open()."""
    import ast

    pure_files = [
        "src/panel.py",
        "src/stationarity.py",
        "src/descriptives.py",
        "src/tables.py",
        "src/data_note.py",
        "src/report_vars.py",
        "src/report_tables.py",
        "src/report_editorial.py",
        "src/figures.py",
        "src/config.py",
        "src/references.py",
        "src/scenarios.py",
        "src/stress.py",
        "src/stress_tables.py",
        "src/design.py",
        "src/estimation.py",
        "src/diagnostics.py",
        "src/forecast.py",
        "src/model1.py",
        "src/model1_config.py",
    ]

    for mod_path in pure_files:
        with open(mod_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Buscar 'open(' que no sea en comentarios/strings - aproximación simple
        if "open(" in content and "pipeline" not in mod_path and "fred_io" not in mod_path:
            # Verificar que no sea en string/comentario
            tree = ast.parse(content, filename=mod_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
                    pytest.fail(f"{mod_path}: contiene open()")


MODEL1_PURE_MODULES = [
    "src/design.py",
    "src/estimation.py",
    "src/diagnostics.py",
    "src/forecast.py",
    "src/model1.py",
    "src/model1_config.py",
]
MODEL1_FORBIDDEN_IMPORTS = {
    "requests", "pandas_datareader", "matplotlib", "urllib", "socket",
    "pathlib", "os", "shutil", "subprocess", "tempfile",
}
MISSING_DATA_OPS = {"fillna", "ffill", "bfill", "interpolate", "dropna"}


def _imported_roots(tree) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_model1_modules_are_pure_and_never_fill_or_drop_missing_data():
    """Spec 003, RNF-6 y RF-2: sin red, disco ni gráficos; sin rellenar ni descartar faltantes."""
    for mod_path in MODEL1_PURE_MODULES:
        with open(mod_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=mod_path)
        bad = _imported_roots(tree) & MODEL1_FORBIDDEN_IMPORTS
        assert not bad, f"{mod_path}: importa {sorted(bad)}"
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
                pytest.fail(f"{mod_path}: contiene open()")
            if isinstance(node, ast.Attribute) and node.attr in MISSING_DATA_OPS:
                pytest.fail(f"{mod_path}:{node.lineno}: usa .{node.attr}() sobre datos del modelo")


def test_report_vars_model1_functions_never_fill_or_drop_missing_data():
    """Solo las funciones del bloque `modelo1:` (las de la spec 001 no se tocan)."""
    with open("src/report_vars.py", "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename="src/report_vars.py")
    checked = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and (node.name == "model1_variables" or node.name.startswith("_m1_")):
            checked += 1
            for sub in ast.walk(node):
                if isinstance(sub, ast.Attribute):
                    assert sub.attr not in MISSING_DATA_OPS, f"{node.name}: usa .{sub.attr}()"
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == "open":
                    pytest.fail(f"{node.name}: contiene open()")
    assert checked >= 2
