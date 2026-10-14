"""Spec 006: canonical variables, orchestration and recursive report guards."""

import hashlib
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("source", ["datos:\r\n  n_series: '12'\r\n", "datos:\n  texto: café\n"])
def test_sync_preserves_source_exactly(source):
    from src.report_vars import sync_report_variables

    assert sync_report_variables(source) == source


@pytest.mark.parametrize("source", ["", "# empty", "null", "{}", "[]", "datos: ["])
def test_sync_rejects_empty_or_invalid_variables(source):
    from src.report_vars import sync_report_variables

    with pytest.raises(ValueError):
        sync_report_variables(source)


def test_report_stage_refreshes_stale_copy_without_touching_source(tmp_path, monkeypatch):
    from src.pipeline import main

    monkeypatch.setenv("PIPELINE_ROOT", str(tmp_path))
    source = tmp_path / "report/_variables.yml"
    source.parent.mkdir()
    original = b"datos:\r\n  n_series: '12'\r\n"
    source.write_bytes(original)
    mirror = tmp_path / "_variables.yml"
    mirror.write_bytes(b"stale: true\n")
    assert main(["report"]) == 0
    assert source.read_bytes() == mirror.read_bytes() == original
    digest = hashlib.sha256(mirror.read_bytes()).hexdigest()
    assert main(["report"]) == 0
    assert hashlib.sha256(mirror.read_bytes()).hexdigest() == digest


def test_report_stage_detects_corruption_after_writing(tmp_path, monkeypatch):
    from src.pipeline import stage_report

    monkeypatch.setenv("PIPELINE_ROOT", str(tmp_path))
    source = tmp_path / "report/_variables.yml"
    source.parent.mkdir()
    source.write_bytes(b"datos: {n_series: '12'}\n")
    original_write = Path.write_bytes

    def corrupt_mirror(path, data):
        if path == tmp_path / "_variables.yml":
            data += b"tampered: true\n"
        return original_write(path, data)

    monkeypatch.setattr(Path, "write_bytes", corrupt_mirror)
    with pytest.raises(ValueError, match="SHA-256"):
        stage_report()


def test_report_stage_rejects_invalid_source_before_replacing_copy(tmp_path, monkeypatch):
    from src.pipeline import stage_report

    monkeypatch.setenv("PIPELINE_ROOT", str(tmp_path))
    (tmp_path / "report").mkdir()
    (tmp_path / "report/_variables.yml").write_text("{}", encoding="utf-8")
    mirror = tmp_path / "_variables.yml"
    mirror.write_bytes(b"previous: valid\n")
    with pytest.raises(ValueError):
        stage_report()
    assert mirror.read_bytes() == b"previous: valid\n"


def test_all_finishes_with_report_and_stops_after_failure(monkeypatch):
    import src.pipeline as pipeline

    calls = []
    for name in ("data", "models", "stress", "report"):
        monkeypatch.setattr(pipeline, f"stage_{name}",
                            lambda *args, name=name, **kwargs: calls.append(name) or 0,
                            raising=False)
    assert pipeline.main(["all"]) == 0
    assert calls == ["data", "models", "stress", "report"]
    calls.clear()
    monkeypatch.setattr(pipeline, "stage_models", lambda: calls.append("models") or 2)
    assert pipeline.main(["all"]) == 2
    assert calls == ["data", "models"]


def test_root_variables_in_sync():
    mirror = ROOT / "_variables.yml"
    if mirror.exists():
        assert mirror.read_bytes() == (ROOT / "report/_variables.yml").read_bytes()


def test_quarto_pre_render_and_exact_root_ignore():
    config = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))
    assert config["project"]["render"] == ["report/informe.qmd", "report/anexo-tecnico.qmd"]
    assert config["project"]["pre-render"] == ["uv run python -m src.pipeline report"]
    assert config["format"]["typst"]["citeproc"] is True
    assert "/_variables.yml" in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()


def test_recursive_number_guard_rejects_section_and_annex_prose(tmp_path, monkeypatch):
    import tests.test_harness as harness

    monkeypatch.setattr(harness, "ROOT", tmp_path)
    for directory in ("secciones/nested", "anexos"):
        path = tmp_path / "report" / directory / "bad.qmd"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("La asociación es 0,8 pp.", encoding="utf-8")
        with pytest.raises(AssertionError, match="0,8"):
            harness.test_report_has_no_hand_typed_numbers()
        path.write_text("{{< var modelo1.n_obs >}}", encoding="utf-8")
    harness.test_report_has_no_hand_typed_numbers()


@pytest.mark.parametrize("key", ["missing2026", "asiamah2026", "koskei2023", "newey1987"])
def test_recursive_citation_guard_checks_matrix_status(tmp_path, monkeypatch, key):
    import tests.test_harness as harness

    monkeypatch.setattr(harness, "ROOT", tmp_path)
    (tmp_path / "research").mkdir()
    matrix = (ROOT / "research/matriz-literatura.md").read_text(encoding="utf-8")
    if key == "newey1987":
        matrix = "\n".join(line.replace("verificado", "descartado") if "newey1987" in line else line
                           for line in matrix.splitlines())
    (tmp_path / "research/matriz-literatura.md").write_text(matrix, encoding="utf-8")
    report = tmp_path / "report"
    (report / "secciones/nested").mkdir(parents=True)
    (report / "references.bib").write_bytes((ROOT / "report/references.bib").read_bytes())
    (report / "secciones/nested/bad.qmd").write_text(f"Estudio [@{key}].", encoding="utf-8")
    with pytest.raises(AssertionError, match=key):
        harness.test_report_citations_exist_in_bib()


def test_recursive_citation_guard_accepts_verified_method_reference(tmp_path, monkeypatch):
    import tests.test_harness as harness

    monkeypatch.setattr(harness, "ROOT", tmp_path)
    (tmp_path / "research").mkdir()
    (tmp_path / "research/matriz-literatura.md").write_bytes((ROOT / "research/matriz-literatura.md").read_bytes())
    (tmp_path / "report/anexos").mkdir(parents=True)
    (tmp_path / "report/references.bib").write_bytes((ROOT / "report/references.bib").read_bytes())
    (tmp_path / "report/anexos/good.qmd").write_text("Método [@newey1987].", encoding="utf-8")
    harness.test_report_citations_exist_in_bib()


def test_interface_exposes_canonical_keys_values_and_asset_provenance():
    from src.report_vars import render_report_interface

    source = "datos: {n_series: '12'}\nmodelo1: {coef: {x: {p: '0,010'}}}\n"
    assets = {"outputs/tables/model1_coefficients.csv": {
        "sha256": "a" * 64, "description": "Coeficientes", "origin": "003-modelo-i", "kind": "CSV aprobado"}}
    interface = render_report_interface(source, assets)
    assert "datos.n_series" in interface and "12" in interface
    assert "modelo1.coef.x.p" in interface and "0,010" in interface
    assert "outputs/tables/model1_coefficients.csv" in interface and "a" * 64 in interface
    assert "003-modelo-i" in interface
    assert "report/_variables.yml" in interface


def test_interface_does_not_advertise_list_indices_as_quarto_shortcodes():
    from src.report_vars import render_report_interface

    interface = render_report_interface("modelo1: {limitaciones: [{detalle: 'No causalidad'}]}\n", {})
    assert "modelo1.limitaciones" in interface
    assert "var modelo1.limitaciones.0" not in interface


def test_interface_rejects_missing_provenance_or_unsafe_asset_path():
    from src.report_vars import render_report_interface

    for assets in ({"outputs/figures/missing.png": {}}, {"../outside.png": {"sha256": "a" * 64,
                    "description": "Figura", "origin": "003", "kind": "Figura"}}):
        with pytest.raises(ValueError):
            render_report_interface("datos: {n_series: '12'}", assets)


def test_report_stage_generates_interface_from_current_source(tmp_path, monkeypatch):
    from src.pipeline import main

    monkeypatch.setenv("PIPELINE_ROOT", str(tmp_path))
    (tmp_path / "report").mkdir()
    (tmp_path / "report/_variables.yml").write_text("datos: {n_series: '12'}", encoding="utf-8")
    assert main(["report"]) == 0
    interface = tmp_path / "specs/006-informe/interfaz.md"
    assert "datos.n_series" in interface.read_text(encoding="utf-8")
    assert "12" in interface.read_text(encoding="utf-8")


def test_report_scaffold_uses_guide_headings_once_and_has_no_central_prose():
    import re

    central = (ROOT / "report/informe.qmd").read_text(encoding="utf-8")
    paths = re.findall(r"\{\{< include (secciones/[^ >]+) >\}\}", central)
    assert len(paths) == 16 and len(set(paths)) == 16
    sections = "\n".join((ROOT / "report" / path).read_text(encoding="utf-8") for path in paths)
    guide = (ROOT / "docs/guia-profesor.md").read_text(encoding="utf-8")
    main_headings = re.findall(r"^### (\d+\. .+)$", guide, re.MULTILINE)
    report_headings = re.findall(r"^# (\d+\. .+)$", sections, re.MULTILINE)
    assert report_headings == main_headings
    subheadings = re.findall(r"^## ([236]\.\d+)\b", sections, re.MULTILINE)
    assert subheadings == ["2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.2", "3.3", "3.4", "3.5", "6.1", "6.2", "6.3", "6.4"]
    assert "# 3.5" not in (ROOT / "report/secciones/03f-limitaciones.qmd").read_text(encoding="utf-8")
    without_yaml = re.sub(r"\A---.*?\n---\n", "", central, flags=re.DOTALL)
    assert re.sub(r"\{\{< include .*?>\}\}", "", without_yaml).strip() == ""


def test_t10_descriptive_sections_use_frozen_sources_and_have_no_placeholders():
    names = ['03a-datos', '03b-variables', '03c-politica', '03d-modelos', '03e-desviaciones',
             '10-referencias', '11-datos-descarga']
    text = '\n'.join((ROOT / 'report/secciones' / (name + '.qmd')).read_text(encoding='utf8') for name in names)
    assert 'PENDIENTE' not in text
    assert '{{< var datos.fecha_descarga >}}' in text
    assert '{{< var informe.historia_inicio >}}' in text
    assert 'octubre' in text and 'noviembre' in text and 'diciembre' in text
    assert 'GDPC1' in text and 'GDP' in text and 'LOANS' in text
    assert 'logarítmica' in text and 'HAC' in text
    assert 'pandas_datareader' in text and 'uv run python -m src.pipeline all' in text
    assert '#refs' in (ROOT / 'report/secciones/10-referencias.qmd').read_text(encoding='utf8')


def test_generated_interface_has_all_current_keys_figures_and_valid_hashes():
    import re

    # Read only: validating metadata never regenerates approved outputs.
    interface = (ROOT / "specs/006-informe/interfaz.md").read_text(encoding="utf-8")
    variables = yaml.safe_load((ROOT / "report/_variables.yml").read_text(encoding="utf-8"))

    def walk(node, path=""):
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, f"{path}.{key}" if path else str(key))
        else:
            assert f"`{path}`" in interface

    walk(variables)
    for figure in (ROOT / "outputs/figures").glob("*.png"):
        assert figure.relative_to(ROOT).as_posix() in interface
    assets = re.findall(r"^\| \[([^\]]+)\]\([^\n]+\| `([a-f0-9]{64})` \|$", interface, re.MULTILINE)
    assert assets
    for path, sha in assets:
        assert (ROOT / path).is_file(), path
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path


def test_number_guard_exempts_only_numbered_heading_prefix():
    from tests.test_harness import _report_prose, find_hand_typed_numbers

    assert find_hand_typed_numbers(_report_prose("# 3. Datos\n## 3.1 Descripción\n")) == []
    assert find_hand_typed_numbers(_report_prose("## 3.1 Descripción: valor 0,8 pp\n")) == ["0,8"]
    assert find_hand_typed_numbers(_report_prose("Valor 3.1 en la prosa\n")) == ["3.1"]
    assert find_hand_typed_numbers(_report_prose("# 0.8 Coeficiente\n")) == ["0.8"]


def test_interface_has_separate_inherited_key_map_and_current_missing_groups():
    from src.report_vars import render_report_interface

    source = "modelo2: {k_elegido: '1', k_aic: '1', k_bic: '1', lp: {h13: {phi: '3,200'}}}\n"
    interface = render_report_interface(source, {})
    inherited = interface.split("## Hallazgos heredados y solicitudes", 1)[1]
    assert "modelo2.k_elegido" in inherited and "modelo2.lp.h13.phi" in inherited
    assert "Conteos y tabla de literatura" in inherited and "PENDIENTE T4" in inherited


def test_report_metadata_counts_frozen_sources_without_changing_model_blocks():
    import copy

    from src.report_vars import add_report_metadata

    matrix = (ROOT / "research/matriz-literatura.md").read_text(encoding="utf-8")
    manifest = (ROOT / "data/raw/manifest.csv").read_text(encoding="utf-8")
    paths = (ROOT / "outputs/tables/stress_paths.csv").read_text(encoding="utf-8")
    original = yaml.safe_load((ROOT / "report/_variables.yml").read_text(encoding="utf-8"))
    before = copy.deepcopy(original)
    result = add_report_metadata(original, matrix, manifest, paths)
    assert original == before
    for block in ("modelo1", "modelo2", "estres"):
        assert result[block] == before[block]
    assert result["datos"]["n_series"] == "13"
    assert result["informe"]["historia_inicio"] == "1998T1"
    assert result["literatura"]["n_estudios_verificados"] == "17"
    assert result["literatura"]["n_pendiente_lectura"] == "8"
    assert result["informe"]["escenario_d"]["n_alzas"] == "7"
    assert result["informe"]["escenario_d"]["n_ceros"] == "6"
    assert result["informe"]["escenario_d"]["inicio_adaptado"] == "2026T3"
    assert "c2_chi2" not in result["modelo2"]["lectura"]


def test_literature_table_preserves_verified_rows_and_suppresses_questioned_signs():
    from src.report_tables import literature_report_table
    from src.references import parse_matrix

    matrix = (ROOT / "research/matriz-literatura.md").read_text(encoding="utf-8")
    table = literature_report_table(matrix)
    _, rows = parse_matrix(matrix)
    expected = {r.cells["Clave"] for r in rows if r.cells["Estado"] == "verificado" and r.cells["Tipo"] == "estudio"}
    assert set(table["clave"]) == expected
    assert "asiamah2026" not in table["clave"].tolist()
    assert "koskei2023" not in table["clave"].tolist()
    by_key = table.set_index("clave")
    for key in ("koju2018", "tanaskovic2015", "nkusu2011", "jimenez2014a", "obradovic2026"):
        if key in by_key.index:
            assert by_key.loc[key, "signo"] == "—"
            note = by_key.loc[key, "nota"]
            assert "Base consultada:" in note
            if key == "obradovic2026":
                assert "tasa de préstamo" in note and "no es la tasa de política" in note
            else:
                assert "El signo no se sintetiza en esta tabla" in note
    for row in rows:
        if row.cells["Clave"] in expected:
            item = by_key.loc[row.cells["Clave"]]
            assert item["metodo"] == row.cells["Método"]
            assert item["regresores"] == row.cells["Regresores"]


def test_metadata_rejects_duplicate_manifest_and_different_model_scenario_paths():
    from src.report_vars import add_report_metadata

    matrix = (ROOT / "research/matriz-literatura.md").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="duplicad"):
        add_report_metadata({"datos": {}}, matrix, "series,first_obs\nX,1998-01-01\nX,1998-01-01\n", "")
    paths = "modelo,escenario,trimestre,ΔFFR\nmodelo1,propio,2026T3,0.1\nmodelo2,propio,2026T3,0.0\n"
    with pytest.raises(ValueError, match="distintas"):
        add_report_metadata({"datos": {}}, matrix, "", paths)


def test_root_url_change_requires_matrix_coherence_without_weakening_guard():
    from src.references import parse_bib, parse_matrix, check_coherence

    bib = (ROOT / "report/references.bib").read_text(encoding="utf-8")
    matrix = (ROOT / "research/matriz-literatura.md").read_text(encoding="utf-8")
    old = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DRALACBS"
    new = "https://fred.stlouisfed.org/"
    # Current files may have the authorized synchronized URL; simulate the stale matrix independently.
    stale = matrix.replace(new + " |", old + " |")
    proposed = bib.replace(old, new)
    assert any("fred2026" in error for error in check_coherence(parse_matrix(stale)[1], parse_bib(proposed)))
    assert check_coherence(parse_matrix(stale.replace(old, new))[1], parse_bib(proposed)) == []
