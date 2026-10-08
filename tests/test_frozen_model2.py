"""Etapa `models` del Modelo II sobre los datos reales congelados (spec 004, tarea 8).

Es la primera tarea que estima el Modelo II con datos reales; el pre-registro está sellado en los commits
ec983d0 (spec aprobada), 45c43d5 (cambio C1, antes de estimar) y 7f732ce (plan aprobado). Siguiendo el plan
(§7), este test NO compara coeficientes ni estadísticos con ningún valor esperado: eso convertiría el test en
una foto de los resultados. Comprueba estructura, muestra, tipos, dimensiones, claves, que `data/raw/` no se
toca y que las corridas son reproducibles e idempotentes (bytes idénticos). Sin red (la bloquea conftest).
"""

from __future__ import annotations

import hashlib
import json
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from src.design import read_decisions
from src.design2 import build_columns, common_window, zero_rate_quarters
from src.fred_io import load_latest_raw
from src.model2_config import EXPECTED_FORM
from src.panel import build_panel
from src.tables import fmt_es
from tests.test_model2_language import find_banned

STEMS = [
    "model2_selection", "model2_coefficients", "model2_effects", "model2_trajectory", "model2_reading",
    "model2_lp", "model2_comparison", "model2_diagnostics", "model2_stationarity",
    "model2_robustness_estimates", "model2_robustness_summary", "model2_limitations", "model2_deviations",
    "model2_inputs63",
]
FIGURES = ["model2_profile.png", "model2_response.png", "model2_cusum.png"]
JSON_KEYS = ["spec", "dependent", "form", "k", "k_criterion", "terms", "columns", "params", "cov_hac",
             "psd_adjusted", "hac_lags", "sample_start", "sample_end", "nobs", "covid_quarters", "psi",
             "response", "h_star", "reading"]
VARIABLE_KEYS = ["estimador", "forma_y", "k_elegido", "criterio", "k_bic", "k_aic", "muestra_inicio",
                 "muestra_fin", "n_obs", "n_parametros", "rezagos_hac", "dummies_covid", "truncamiento_espectral",
                 "r2", "r2_ajustado", "ee_regresion", "seleccion", "coef", "efectos", "trayectoria", "granger",
                 "lectura", "lp", "lp_resumen", "diag", "robustez", "robustez_resumen", "no_i0", "limitaciones",
                 "desviaciones"]


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _model2_files(root: Path) -> list[Path]:
    files = [root / "outputs" / "tables" / f"{s}.{ext}" for s in STEMS for ext in ("csv", "md")]
    files += [root / "outputs" / "figures" / f for f in FIGURES]
    files += [root / "outputs" / "models" / "model2_main.json", root / "report" / "_variables.yml"]
    return files


def _table(runs, stem: str) -> pd.DataFrame:
    text = (runs["a"] / "outputs" / "tables" / f"{stem}.csv").read_text(encoding="utf-8")
    return pd.read_csv(StringIO(text), na_values=["—"], keep_default_na=False)


@pytest.fixture(scope="module")
def runs(frozen_runs):
    return frozen_runs


@pytest.fixture(scope="module")
def variables(runs):
    return yaml.safe_load((runs["a"] / "report" / "_variables.yml").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def export(runs):
    def forbid(const):
        raise ValueError(f"constante no permitida en el JSON: {const}")

    text = (runs["a"] / "outputs" / "models" / "model2_main.json").read_text(encoding="utf-8")
    return json.loads(text, parse_constant=forbid)


# --- Salidas escritas ---


def test_models_stage_writes_the_14_tables_in_markdown_and_csv(runs):
    assert len(STEMS) == 14
    for stem in STEMS:
        for ext in ("md", "csv"):
            path = runs["a"] / "outputs" / "tables" / f"{stem}.{ext}"
            assert path.exists() and path.stat().st_size > 0, path.name


def test_models_stage_writes_the_three_figures_at_200_dpi(runs):
    for name in FIGURES:
        path = runs["a"] / "outputs" / "figures" / name
        assert path.exists()
        header = path.read_bytes()[:33]
        assert header[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")
        assert (width, height) == (1600, 900), name        # 8 × 4,5 pulgadas a 200 dpi


def test_models_stage_does_not_touch_the_frozen_raw_data(runs):
    now = {p.name: _digest(p) for p in (runs["a"] / "data" / "raw").iterdir()}
    assert now == runs["raw_before"]


# --- Estructura sobre los datos reales (sin comparar coeficientes) ---


def test_expected_form_holds_on_the_real_stationarity_table(runs):
    stat = pd.read_csv(runs["a"] / "outputs" / "tables" / "stationarity.csv", index_col=0)
    assert read_decisions(stat)["dralacbs"] == EXPECTED_FORM


def test_common_sample_is_2000q2_to_the_common_quarter_with_105_obs(variables):
    mv, datos = variables["modelo2"], variables["datos"]
    assert (mv["muestra_inicio"], mv["muestra_fin"]) == ("2000T2", datos["muestra_fin"])
    assert mv["n_obs"] == "105" and mv["forma_y"] == "primera diferencia" and mv["criterio"] == "BIC"
    assert mv["rezagos_hac"] == "4" and mv["dummies_covid"] == "2020T2, 2020T3, 2020T4 y 2021T1"
    k = int(mv["k_elegido"])
    assert 1 <= k <= 8 and 1 <= int(mv["k_aic"]) <= 8 and 1 <= int(mv["k_bic"]) <= 8
    assert mv["k_bic"] == mv["k_elegido"] and mv["n_parametros"] == str(k + 11)


def test_zero_rate_quarters_and_r3_sample_on_the_frozen_history(runs, variables):
    raw, _ = load_latest_raw(runs["a"] / "data" / "raw")
    panel = build_panel(raw)
    window = common_window(build_columns(panel.full, EXPECTED_FORM), panel.end)
    assert len(zero_rate_quarters(panel.full, *window)) == 36
    r3 = variables["modelo2"]["robustez"]["r3"]
    assert r3["estado"] in ("estimada", "no estimada")
    if r3["estado"] == "estimada":
        assert r3["n_obs"] == "69" and r3["k"] == variables["modelo2"]["k_elegido"]
    r2 = variables["modelo2"]["robustez"]["r2"]
    if r2["estado"] == "estimada":
        assert r2["n_obs"] == "97"                          # 105 − 8 trimestres de 2020–2021


def test_selection_table_has_eight_models_on_the_same_sample(runs):
    t = _table(runs, "model2_selection")
    assert list(t["K"]) == list(range(1, 9)) and set(t["nobs"]) == {105}
    assert list(t["n_params"]) == [k + 11 for k in range(1, 9)]
    assert t["aic"].notna().all() and t["bic"].notna().all() and np.isfinite(t[["aic", "bic"]].to_numpy()).all()


def test_table_dimensions(runs, variables):
    k = int(variables["modelo2"]["k_elegido"])
    expected = {"model2_coefficients": k + 11, "model2_effects": 2, "model2_trajectory": 13, "model2_reading": 4,
                "model2_lp": 13, "model2_comparison": 13, "model2_stationarity": 6,
                "model2_robustness_estimates": 3, "model2_robustness_summary": 2, "model2_inputs63": 2}
    for stem, n in expected.items():
        assert len(_table(runs, stem)) == n, stem
    assert len(_table(runs, "model2_limitations")) >= 8 and len(_table(runs, "model2_deviations")) >= 5
    diag = _table(runs, "model2_diagnostics")
    assert {"Breusch-Godfrey", "White", "CUSUM", "Chow 2008T3", "Chow 2020T2"} <= set(diag["prueba"])


def test_tables_have_numeric_types_and_no_nan_or_inf_tokens(runs):
    coef = _table(runs, "model2_coefficients")
    for col in ("coef", "ee_hac", "z", "p", "ic_inf", "ic_sup"):
        assert pd.api.types.is_float_dtype(coef[col]) and np.isfinite(coef[col].to_numpy()).all(), col
    lp = _table(runs, "model2_lp")
    assert lp.loc[0, "phi"] == 1.0 and lp["h"].tolist() == list(range(13))
    for stem in STEMS:
        text = (runs["a"] / "outputs" / "tables" / f"{stem}.csv").read_text(encoding="utf-8")
        fields = {f.strip('"').lower() for line in text.split("\n")[1:] for f in line.split(",")}
        assert not fields & {"nan", "inf", "-inf", "none", "<na>"}, stem


def test_markdown_tables_use_decimal_comma(runs):
    md = (runs["a"] / "outputs" / "tables" / "model2_coefficients.md").read_text(encoding="utf-8")
    table = md.split("\n\n")[0]
    assert "," in table and "." not in table


# --- JSON para la spec 005 ---


def test_json_structure_and_matrix_dimensions(export, variables):
    assert list(export) == JSON_KEYS
    k = export["k"]
    assert export["spec"] == "004-modelo-ii" and export["dependent"] == "dralacbs" and 1 <= k <= 8
    n = len(export["terms"])
    assert n == len(export["params"]) == len(export["cov_hac"]) == k + 11 == int(variables["modelo2"]["n_parametros"])
    cov = np.array(export["cov_hac"], dtype=float)
    assert cov.shape == (n, n) and np.isfinite(cov).all() and np.allclose(cov, cov.T)
    assert np.all(np.linalg.eigvalsh((cov + cov.T) / 2) > -1e-10 * np.abs(cov).max())      # semidefinida positiva
    assert all(isinstance(v, float) for v in export["params"])
    assert export["hac_lags"] == 4 and export["nobs"] == 105 and isinstance(export["psd_adjusted"], bool)
    assert export["covid_quarters"] == ["2020T2", "2020T3", "2020T4", "2021T1"]
    assert len(export["psi"]) == len(export["response"]) == 13
    assert np.allclose(np.cumsum(export["psi"]), export["response"])
    assert set(export["h_star"]) == {"h", "signo"} and 0 <= export["h_star"]["h"] <= 12
    assert set(export["reading"]) == {"etiqueta", "c1", "c2"}
    assert set(export["columns"]) == set(export["terms"])


# --- Variables del informe ---


def test_variables_yml_keeps_the_other_keys_byte_for_byte(runs, variables):
    after = (runs["a"] / "report" / "_variables.yml").read_text(encoding="utf-8")
    assert after.startswith(runs["variables_before"])        # la sección `datos:` queda idéntica
    assert list(variables) == ["datos", "modelo1", "modelo2"]
    assert variables["datos"] == yaml.safe_load(runs["variables_before"])["datos"]


def test_variables_modelo2_block_has_the_planned_keys_and_is_text_only(variables):
    mv = variables["modelo2"]
    assert list(mv) == VARIABLE_KEYS

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
    assert list(mv["lp"]) == [f"h{h}" for h in range(13)] and list(mv["seleccion"]) == [f"k{k}" for k in range(1, 9)]


def test_variables_have_the_same_digits_as_the_csv_tables(runs, variables):
    mv = variables["modelo2"]
    coef = _table(runs, "model2_coefficients").set_index("termino")
    for term, vals in mv["coef"].items():
        assert vals["coef"] == fmt_es(coef.loc[term, "coef"], 3)
        assert vals["ee"] == fmt_es(coef.loc[term, "ee_hac"], 3)
    traj = _table(runs, "model2_trajectory").set_index("h")
    assert all(mv["trayectoria"]["psi"][f"h{h}"] == fmt_es(traj.loc[h, "psi"], 3) for h in range(13))
    eff = _table(runs, "model2_effects").set_index("efecto")
    assert mv["efectos"]["s"]["est"] == fmt_es(eff.loc["S", "est"], 3)
    lp = _table(runs, "model2_lp").set_index("h")
    assert mv["lp"]["h0"]["phi"] == "1,000" and mv["lp"]["h0"]["phi_ee"] == "—"
    assert mv["lp"]["h1"]["beta"] == fmt_es(lp.loc[1, "beta"], 3)


def test_json_and_tables_agree(runs, export):
    coef = _table(runs, "model2_coefficients")
    assert list(coef["termino"]) == export["terms"]
    assert np.allclose(coef["coef"], export["params"], rtol=1e-12, atol=0)
    traj = _table(runs, "model2_trajectory")
    assert np.allclose(traj["R"], export["response"], rtol=1e-12, atol=0)


def test_real_outputs_have_no_causal_language(runs):
    for path in _model2_files(runs["a"]):
        if path.name == "_variables.yml":
            # solo el bloque del Modelo II: `modelo1:` tiene claves de la 003 como `impacto_pp`
            text = yaml.safe_dump(yaml.safe_load(path.read_text(encoding="utf-8"))["modelo2"], allow_unicode=True)
            assert find_banned(text) == [], path.name
        elif path.suffix in {".csv", ".md", ".json"}:
            assert find_banned(path.read_text(encoding="utf-8")) == [], path.name


# --- El Modelo I no cambia ---


def test_model1_blocks_are_identical_between_runs(runs):
    ya = yaml.safe_load((runs["a"] / "report" / "_variables.yml").read_text(encoding="utf-8"))
    yb = yaml.safe_load((runs["b"] / "report" / "_variables.yml").read_text(encoding="utf-8"))
    assert ya["modelo1"] == yb["modelo1"] and ya["datos"] == yb["datos"]


# --- Reproducibilidad (RNF-8) e idempotencia ---


def test_two_independent_roots_leave_identical_bytes(runs):
    for fa, fb in zip(_model2_files(runs["a"]), _model2_files(runs["b"])):
        assert fa.relative_to(runs["a"]) == fb.relative_to(runs["b"])
        assert _digest(fa) == _digest(fb), f"{fa.name} no es reproducible"


def test_running_models_twice_on_the_same_root_changes_nothing(runs):
    assert runs["b_first"] == runs["b_second"]
    assert any(name.endswith("model2_main.json") for name in runs["b_first"])
    assert len([n for n in runs["b_first"] if "model2_" in n]) == 14 * 2 + 3 + 1


# --- Ronda 1 de la auditoría: el contrato `columns` del JSON apunta a series reales del panel ---


def test_json_columns_exist_in_the_real_panel_and_y_lag_is_the_differenced_series(runs, export):
    raw, _ = load_latest_raw(runs["a"] / "data" / "raw")
    full = build_panel(raw).full
    for term, src in export["columns"].items():
        if src is None:
            assert term == "const" or term.startswith("covid_"), term
            continue
        assert src["column"] in full.columns, f"{term}: {src['column']} no existe en el panel"
    assert export["columns"]["y_lag"] == {"column": "dralacbs_d", "lag": 1}
    assert np.allclose(full["dralacbs_d"].iloc[1:], full["dralacbs"].diff().iloc[1:], rtol=0, atol=1e-12,
                       equal_nan=True)
