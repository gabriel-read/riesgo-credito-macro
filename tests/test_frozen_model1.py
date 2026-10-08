"""Etapa `models` sobre los datos reales congelados (spec 003, tarea 9).

Es la primera tarea que estima con datos reales (el pre-registro está sellado en el commit
667b313). Siguiendo el plan (§7), este test NO compara coeficientes ni estadísticos con ningún
valor esperado: eso convertiría el test en una foto de los resultados. Comprueba la estructura,
las muestras, las formas esperadas, las claves, que `data/raw/` no se toca y que dos corridas
dejan bytes idénticos. Sin red (la bloquea conftest).
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd
import pytest
import yaml

from src.design import check_expected_forms, read_decisions
from src.model1_config import EXPECTED_FORMS, VARIANTS
from src.pipeline import main
from tests.test_language import find_causal_language

RAW = Path("data/raw")
STEMS = [
    "model1_coefficients", "model1_effects", "model1_diagnostics", "model1_stationarity",
    "model1_robustness_estimates", "model1_robustness_summary", "model1_oos",
    "model1_limitations", "model1_deviations",
]
FIGURES = ["model1_coefficients.png", "model1_cusum.png", "model1_oos.png"]


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _model1_files(root: Path) -> list[Path]:
    files = [root / "outputs" / "tables" / f"{s}.{ext}" for s in STEMS for ext in ("csv", "md")]
    files += [root / "outputs" / "figures" / f for f in FIGURES]
    files += [root / "outputs" / "models" / "model1_main.json", root / "report" / "_variables.yml"]
    return files


@pytest.fixture(scope="module")
def runs(frozen_runs):
    """Las corridas sobre los datos congelados las hace el fixture de sesión de conftest.py."""
    return frozen_runs


# --- Salidas escritas ---


def test_models_stage_writes_the_nine_tables_in_markdown_and_csv(runs):
    for stem in STEMS:
        for ext in ("md", "csv"):
            path = runs["a"] / "outputs" / "tables" / f"{stem}.{ext}"
            assert path.exists() and path.stat().st_size > 0, path.name
    assert len(STEMS) == 9


def test_models_stage_writes_the_three_figures_at_200_dpi(runs):
    for name in FIGURES:
        path = runs["a"] / "outputs" / "figures" / name
        assert path.exists()
        header = path.read_bytes()[:33]
        assert header[:8] == b"\x89PNG\r\n\x1a\n"
        # 8 × 4,5 pulgadas a 200 dpi = 1600 × 900 píxeles
        width, height = int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")
        assert (width, height) == (1600, 900), name


def test_models_stage_writes_the_json_for_spec_005(runs):
    path = runs["a"] / "outputs" / "models" / "model1_main.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["spec"] == "003-modelo-i" and data["dependent"] == "dralacbs"
    assert len(data["terms"]) == len(data["params"]) == len(data["cov_hac"]) == 11
    assert all(len(row) == 11 for row in data["cov_hac"])
    assert data["hac_lags"] == 4
    assert data["covid_quarters"] == ["2020T2", "2020T3", "2020T4", "2021T1"]


def test_models_stage_does_not_touch_the_frozen_raw_data(runs):
    now = {p.name: _digest(p) for p in (runs["a"] / "data" / "raw").iterdir()}
    assert now == runs["raw_before"]


# --- Variables del informe: solo se reescribe la clave `modelo1:` ---


def test_variables_yml_keeps_the_other_keys_byte_for_byte(runs):
    after = (runs["a"] / "report" / "_variables.yml").read_text(encoding="utf-8")
    before = runs["variables_before"]
    assert after.startswith(before)  # la sección `datos:` queda idéntica, byte a byte
    assert "\nmodelo1:\n" in after
    loaded = yaml.safe_load(after)
    assert list(loaded) == ["datos", "modelo1", "modelo2"]
    assert loaded["datos"] == yaml.safe_load(before)["datos"]


def test_variables_yml_modelo1_block_is_text_only(runs):
    mv = yaml.safe_load((runs["a"] / "report" / "_variables.yml").read_text(encoding="utf-8"))["modelo1"]

    def leaves(o):
        if isinstance(o, dict):
            for v in o.values():
                yield from leaves(v)
        elif isinstance(o, list):
            for v in o:
                yield from leaves(v)
        else:
            yield o

    assert all(isinstance(v, str) for v in leaves(mv))


# --- Estructura sobre los datos reales (sin comparar coeficientes) ---


def test_expected_forms_hold_on_the_real_stationarity_table(runs):
    stat = pd.read_csv(runs["a"] / "outputs" / "tables" / "stationarity.csv", index_col=0)
    check_expected_forms(read_decisions(stat), EXPECTED_FORMS)  # no lanza


def test_main_sample_is_2000q1_to_the_common_quarter_with_106_obs_and_11_parameters(runs):
    doc = yaml.safe_load((runs["a"] / "report" / "_variables.yml").read_text(encoding="utf-8"))
    mv, datos = doc["modelo1"], doc["datos"]
    assert (mv["muestra_inicio"], mv["muestra_fin"]) == ("2000T1", datos["muestra_fin"])
    assert mv["n_obs"] == datos["n_trimestres"] == "106"
    assert mv["n_parametros"] == "11" and mv["rezagos_hac"] == "4"
    assert mv["forma_y"] == "primera diferencia"


def test_robustness_variants_have_the_expected_windows_on_the_frozen_history(runs):
    mv = yaml.safe_load((runs["a"] / "report" / "_variables.yml").read_text(encoding="utf-8"))["modelo1"]
    vm = mv["variantes_muestra"]
    assert list(vm) == [v.id for v in VARIANTS]
    assert vm["R6"]["inicio"] == "2001T1" and vm["R7"]["inicio"] == "2002T1"
    assert vm["R8"]["estado"] == "no estimada"
    assert vm["R8"]["motivo"] == "sin historia anterior a 2000T1"
    assert vm["R1"]["n_obs"] == "98"  # 106 − 8 trimestres de 2020–2021
    assert all(vm[k]["estado"] == "estimada" for k in vm if k != "R8")


def test_oos_window_on_real_data_is_2022q1_to_the_common_quarter(runs):
    mv = yaml.safe_load((runs["a"] / "report" / "_variables.yml").read_text(encoding="utf-8"))["modelo1"]
    assert mv["oos"]["n_trimestres"] == "18"


def test_real_outputs_have_no_causal_language(runs):
    for path in _model1_files(runs["a"]):
        if path.suffix in {".csv", ".md", ".json"} or path.name == "_variables.yml":
            text = path.read_text(encoding="utf-8")
            assert find_causal_language(text) == [], path.name


# --- Reproducibilidad (RNF-5): dos corridas, bytes idénticos ---


def test_two_runs_leave_identical_bytes_in_tables_figures_json_and_variables(runs):
    for fa, fb in zip(_model1_files(runs["a"]), _model1_files(runs["b"])):
        assert fa.relative_to(runs["a"]) == fb.relative_to(runs["b"])
        assert _digest(fa) == _digest(fb), f"{fa.name} no es reproducible"


# --- Errores claros ---


def test_models_stage_without_the_stationarity_table_says_to_run_data_first(tmp_path, monkeypatch):
    shutil.copytree(RAW, tmp_path / "data" / "raw")
    monkeypatch.setenv("PIPELINE_ROOT", str(tmp_path))
    with pytest.raises(FileNotFoundError, match="data"):
        main(["models"])


def test_models_stage_without_raw_downloads_fails_with_the_001_message(tmp_path, monkeypatch):
    (tmp_path / "outputs" / "tables").mkdir(parents=True)
    (tmp_path / "outputs" / "tables" / "stationarity.csv").write_text("variable\n", encoding="utf-8")
    monkeypatch.setenv("PIPELINE_ROOT", str(tmp_path))
    with pytest.raises(FileNotFoundError, match="descargas crudas"):
        main(["models"])
