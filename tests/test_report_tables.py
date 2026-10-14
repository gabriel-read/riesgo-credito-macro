"""Presentation tables must preserve approved CSV values and complete annexes."""

import csv
import hashlib
import io
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_phi_context_preserves_approved_note_next_to_values_and_identity():
    from src.report_tables import build_report_tables

    source = (ROOT / 'outputs/tables/model2_lp.csv').read_bytes().decode('utf-8')
    approved_md = (ROOT / 'outputs/tables/model2_lp.md').read_text(encoding='utf-8')
    note = approved_md.split('\n\nNota: ', 1)[1].strip()
    result = build_report_tables({'model2_lp': source}, source_notes={'model2_lp': 'Nota: ' + note})
    for filename in ['model2_lp.md', 'model2_lp_anexo_3.md', 'model2_lp_anexo_4.md']:
        text = result['files'][filename]
        assert 'Nota: ' + note in text
        assert text.index('Nota: ' + note) < text.index('| h |')
    assert result['trace']['model2_lp']['source_note'] == 'Nota: ' + note


def test_empty_reason_is_explained_without_replacing_source_cells():
    from src.report_tables import build_report_tables

    source = 'variante,estado,motivo,nota\nR1,estimada,,\nR8,no estimada,sin historia,\n'
    result = build_report_tables({'model1_robustness_estimates': source})
    text = result['files']['model1_robustness_estimates_anexo_1.md']
    assert 'Las celdas vacías de Motivo indican que no se proporciona una explicación adicional' in text
    assert '| R1 | estimada |  |  |' in text
    assert '| R8 | no estimada | sin historia |  |' in text
    assert 'no se informa una causa de no estimación' in text


def _sources():
    return {p.stem: p.read_bytes().decode("utf-8") for p in sorted((ROOT / "outputs/tables").glob("*.csv"))}


def test_real_csv_coverage_and_annex_values():
    from src.report_tables import build_report_tables, display_cell

    sources = _sources()
    result = build_report_tables(sources)
    assert set(result["trace"]) == set(sources)
    for name, text in sources.items():
        rows = list(csv.reader(io.StringIO(text)))
        trace = result["trace"][name]
        assert trace["source_sha256"] == hashlib.sha256(text.encode()).hexdigest()
        assert trace["rows"] == len(rows) - 1
        assert trace["columns"] == rows[0]
        panels = trace["annex_panels"]
        assert set(column for panel in panels for column in panel["columns"]) | set(trace['note_columns']) == set(rows[0])
        for panel in panels:
            indices = [rows[0].index(col) for col in panel["columns"]]
            expected_rows = []
            for row in rows[1:]:
                values = []
                for i in indices:
                    original = row[i]
                    if rows[0][i] == 'kpss_p' and 'kpss_p_truncado' in rows[0]:
                        documented = row[rows[0].index('kpss_p_truncado')]
                        original = documented or original
                    values.append(display_cell(original, rows[0][i]))
                expected_rows.append(values)
            assert panel['rows'] == expected_rows
            markdown = result["files"][panel["file"]]
            data_lines = [line for line in markdown.splitlines() if line.startswith("| ")][2:]
            assert len(data_lines) == len(rows) - 1
            for line, source_row in zip(data_lines, rows[1:]):
                cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
                assert len(cells) == len(indices)
                for cell, column_index in zip(cells, indices):
                    original = source_row[column_index]
                    if cell.startswith(('< ', '> ', '≥ ', '≤ ')) and rows[0][column_index] in {'p', 'p_valor', 'adf_p', 'p_S', 'p_S_rez', 'dm_p', 'p_principal', 'kpss_p', 'kpss_p_truncado'}:
                        bound = float(cell[2:].replace(',', '.'))
                        raw = float(original.replace(',', '.').lstrip('<>≥≤ '))
                        if rows[0][column_index].startswith('kpss_'):
                            assert raw == bound  # censoring endpoint, not an exact p
                        else:
                            assert cell.startswith('< ') and raw < bound
                        continue
                    if re.fullmatch(r"[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?", original):
                        assert abs(float(cell.replace(",", ".")) - float(original)) <= 0.00050000001
                    else:
                        decoded = cell.replace("\\|", "|").replace("\\\\", "\\")
                        expected = display_cell(original, rows[0][column_index]).replace('\\|', '|').replace('\\\\', '\\')
                        if re.fullmatch(r"\d{4}Q[1-4]", original):
                            expected = original.replace("Q", "T")
                        if original in ("True", "False"):
                            expected = "sí" if original == "True" else "no"
                        assert decoded == expected
        presentation = trace["presentation"]
        indices = [rows[0].index(col) for col in presentation["columns"]]
        expected = []
        for row in rows[1:]:
            cells = []
            for i in indices:
                original = row[i]
                if rows[0][i] == 'kpss_p' and 'kpss_p_truncado' in rows[0]:
                    original = row[rows[0].index('kpss_p_truncado')] or original
                cells.append(display_cell(original, rows[0][i]))
            expected.append(cells)
        assert presentation['rows'] == expected


def test_long_text_pipes_unicode_and_numeric_rounding():
    from src.report_tables import build_report_tables, format_report_cell

    source = 'termino,coef,p,nota\nx,0.0105,0.00012,"Límite | no imputar\nTexto completo"\n'
    result = build_report_tables({"model1_coefficients": source})
    markdown = "\n".join(result["files"].values())
    assert "Límite \\| no imputar Texto completo" in markdown
    assert format_report_cell("0.0105") == "0,011"
    assert format_report_cell("0.00012") == "0,000"  # precision declared, not a fabricated estimate
    assert format_report_cell("2026Q2") == "2026T2"
    assert "Coef." in markdown and "Término" in markdown


def test_section_identifier_remains_an_identifier_in_literature_table():
    from src.report_tables import build_report_tables

    result = build_report_tables({"lit_estudios": "clave,seccion_principal\nexample2020,2.5\n"})
    assert "2.5" in result["files"]["lit_estudios.md"]
    assert "2,500" not in result["files"]["lit_estudios.md"]


@pytest.mark.parametrize("source", ["", "a,a\n1,2\n", "a,b\n1\n", "a,b\n1,2,3\n"])
def test_malformed_csv_fails_instead_of_losing_cells(source):
    from src.report_tables import build_report_tables

    with pytest.raises(ValueError):
        build_report_tables({"bad": source})


def test_report_stage_generates_only_derived_tables_and_preserves_sources(tmp_path, monkeypatch):
    from src.pipeline import main

    monkeypatch.setenv("PIPELINE_ROOT", str(tmp_path))
    (tmp_path / "report").mkdir()
    (tmp_path / "report/_variables.yml").write_bytes(b"datos: {n_series: '12'}\n")
    tables = tmp_path / "outputs/tables"
    tables.mkdir(parents=True)
    source = tables / "stress_models.csv"
    source.write_bytes(b"escenario,trimestre,delta_modelo1,delta_modelo2,diferencia_I_II\r\nsevero,2026Q3,0.1,0.2,-0.1\r\n")
    before = source.read_bytes()
    assert main(["report"]) == 0
    assert source.read_bytes() == before
    import json

    trace = json.loads((tmp_path / "outputs/informe/trace.json").read_text(encoding="utf-8"))
    assert trace["stress_models"]["source_sha256"] == hashlib.sha256(before).hexdigest()
    assert (tmp_path / "outputs/informe/stress_models.md").is_file()
    annex = tmp_path / "report/anexos/tablas.qmd"
    assert "stress_models" in annex.read_text(encoding="utf-8")
    first = {p.relative_to(tmp_path).as_posix(): p.read_bytes()
             for folder in (tmp_path / "outputs/informe", tmp_path / "report/anexos")
             for p in folder.rglob("*") if p.is_file()}
    assert main(["report"]) == 0
    assert first == {p.relative_to(tmp_path).as_posix(): p.read_bytes()
                     for folder in (tmp_path / "outputs/informe", tmp_path / "report/anexos")
                     for p in folder.rglob("*") if p.is_file()}
