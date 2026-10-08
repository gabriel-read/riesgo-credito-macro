"""No regresión del Modelo I (spec 004, invariante de todas las tareas; RNF-7 y plan D1/D2).

Los cambios al código de la 003 que exige la 004 son retrocompatibles: la etapa `models` sobre los
datos reales congelados tiene que dejar, byte a byte, las mismas salidas del Modelo I que están
comiteadas en `outputs/` y `report/_variables.yml` (clave `modelo1:`). No compara con valores
esperados escritos a mano: compara con los archivos del repositorio. Sin red (la bloquea conftest).
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from src.pipeline import main

STEMS = [
    "model1_coefficients", "model1_effects", "model1_diagnostics", "model1_stationarity",
    "model1_robustness_estimates", "model1_robustness_summary", "model1_oos",
    "model1_limitations", "model1_deviations",
]
FIGURES = ["model1_coefficients.png", "model1_cusum.png", "model1_oos.png"]
REPO = Path(__file__).resolve().parents[1]


def _model1_files() -> list[Path]:
    files = [Path("outputs") / "tables" / f"{s}.{ext}" for s in STEMS for ext in ("csv", "md")]
    files += [Path("outputs") / "figures" / f for f in FIGURES]
    files.append(Path("outputs") / "models" / "model1_main.json")
    return files


@pytest.fixture(scope="module")
def rerun(tmp_path_factory):
    """Raíz temporal con los datos crudos y la estacionariedad comiteados; corre solo `models`."""
    root = tmp_path_factory.mktemp("nonreg")
    shutil.copytree(REPO / "data" / "raw", root / "data" / "raw")
    (root / "outputs" / "tables").mkdir(parents=True)
    shutil.copy(REPO / "outputs" / "tables" / "stationarity.csv", root / "outputs" / "tables")
    (root / "report").mkdir()
    shutil.copy(REPO / "report" / "_variables.yml", root / "report" / "_variables.yml")
    mp = pytest.MonkeyPatch()
    mp.setenv("PIPELINE_ROOT", str(root))
    try:
        assert main(["models"]) == 0
    finally:
        mp.undo()
    return root


@pytest.mark.parametrize("rel", _model1_files(), ids=lambda p: p.name)
def test_model1_outputs_are_byte_identical_to_the_committed_ones(rerun, rel):
    committed = (REPO / rel).read_bytes()
    if rel.suffix != ".png":
        # en Windows git puede dejar CRLF en el árbol de trabajo; el pipeline escribe siempre LF
        committed = committed.replace(b"\r\n", b"\n")
    assert (rerun / rel).read_bytes() == committed


def test_model1_variables_block_is_identical_to_the_committed_one(rerun):
    new = yaml.safe_load((rerun / "report" / "_variables.yml").read_text(encoding="utf-8"))
    old = yaml.safe_load((REPO / "report" / "_variables.yml").read_text(encoding="utf-8"))
    assert new["modelo1"] == old["modelo1"] and new["datos"] == old["datos"]
