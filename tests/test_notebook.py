"""Tests del notebook educativo (T11, spec 001).

Ejecuta celdas de código con exec, sin error. RF-23, RF-24.
"""

import json
import os
import tempfile
from pathlib import Path
import pytest

# Configurar PIPELINE_ROOT para tests
os.environ["PIPELINE_ROOT"] = str(Path(__file__).parent.parent)


def _exec_notebook(nb_path: Path, raw_dir: Path) -> None:
    """Ejecuta celdas de código del notebook con exec()."""
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Preparar namespace con imports necesarios
    namespace = {
        "RAW_DIR": raw_dir,
        "Path": Path,
        "os": os,
        "pd": __import__("pandas"),
        "np": __import__("numpy"),
    }

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            code = "".join(cell["source"])
            if code.strip():
                exec(code, namespace)


def test_notebook_executes_without_error():
    """Notebook ejecuta sin errores con RAW_DIR apuntando a data/raw real."""
    nb_path = Path("notebooks/01_datos_fred.ipynb")
    raw_dir = Path("data/raw")
    assert nb_path.exists(), "Notebook no existe"
    assert raw_dir.exists(), "data/raw no existe"

    _exec_notebook(nb_path, raw_dir)


def test_notebook_fails_with_clear_error_when_no_raw():
    """Con RAW_DIR vacío, falla con FileNotFoundError y mensaje claro."""
    nb_path = Path("notebooks/01_datos_fred.ipynb")
    with tempfile.TemporaryDirectory() as tmp:
        empty_raw = Path(tmp) / "empty_raw"
        empty_raw.mkdir()
        # El notebook usa os.environ.get('RAW_DIR'), así que seteamos la variable
        import os
        old_raw_dir = os.environ.get("RAW_DIR")
        os.environ["RAW_DIR"] = str(empty_raw)
        try:
            with pytest.raises(FileNotFoundError, match="data --download"):
                _exec_notebook(nb_path, empty_raw)
        finally:
            if old_raw_dir is not None:
                os.environ["RAW_DIR"] = old_raw_dir
            else:
                os.environ.pop("RAW_DIR", None)


def test_notebook_does_not_call_datareader():
    """Código del notebook no llama a DataReader (usa descargas congeladas)."""
    nb_path = Path("notebooks/01_datos_fred.ipynb")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            code = "".join(cell["source"])
            # No debe usar DataReader ni pandas_datareader.data
            assert "DataReader" not in code, f"Celda usa DataReader: {code[:100]}"
            assert "pandas_datareader" not in code, f"Celda importa pandas_datareader: {code[:100]}"