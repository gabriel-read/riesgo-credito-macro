"""Round-two presentation regressions; approved scientific inputs stay immutable."""
from src.report_tables import format_report_cell, build_report_tables, display_cell


def test_uniform_kpss_bounds_require_documented_censoring():
    assert format_report_cell('0.1', 'kpss_p') == '0,100'
    assert format_report_cell('>0,10', 'kpss_p') == '≥ 0,10'
    assert format_report_cell('≥0,10', 'kpss_p') == '≥ 0,10'
    assert format_report_cell('<0,01', 'kpss_p') == '≤ 0,01'
    assert format_report_cell('≤0,01', 'kpss_p') == '≤ 0,01'


def test_kpss_note_only_on_panels_with_kpss_fields():
    result = build_report_tables({'model1_coefficients': 'termino,coef,p\nx,0.1,0.2\n',
                                  'stationarity': 'variable,forma,kpss_p\nx,tal cual,0.1\n'})
    assert 'KPSS conserva' not in result['files']['model1_coefficients.md']
    assert 'KPSS conserva' in result['files']['stationarity.md']


def test_model_and_vif_labels_do_not_expose_operational_identifiers():
    assert display_cell('modelo1 (spec 003)', 'modelo') == 'Modelo I'
    assert display_cell('VIF gdp_growth', 'prueba') == 'VIF PIB (crecimiento)'


def test_stress_presentation_keeps_approved_points_and_distinguishes_overlap():
    import pandas as pd
    import matplotlib.pyplot as plt
    from src.report_figures import stress_presentation_figure
    from pathlib import Path
    frames = [pd.read_csv(Path('outputs/tables') / name) for name in ('stress_levels.csv', 'stress_delta.csv')]
    fig = stress_presentation_figure(*frames, 'modelo1')
    try:
        for axis, frame, column in zip(fig.axes, frames, ('dr', 'delta')):
            scenario_lines = axis.lines[:len(frame[frame.modelo == 'modelo1'].escenario.unique())]
            for line, scenario in zip(scenario_lines, ('base', 'severo', 'propio') if column == 'dr' else ('severo', 'propio')):
                assert list(line.get_ydata()) == list(frame[(frame.modelo == 'modelo1') & (frame.escenario == scenario)][column])
            adverse, own = scenario_lines[-2:]
            assert adverse.get_linestyle() != own.get_linestyle()
            assert own.get_marker() == 'o'
        assert any('coinciden' in text.get_text() for text in fig.texts)
    finally:
        plt.close(fig)


def test_docx_links_are_visually_identifiable():
    import zipfile
    import xml.etree.ElementTree as ET
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile('report/templates/apa-reference.docx') as z:
        root = ET.fromstring(z.read('word/styles.xml'))
    style = root.find("w:style[@w:styleId='Hyperlink']", ns)
    assert style is not None
    assert style.find('w:rPr/w:u', ns) is not None


def test_fred_dataset_note_precedes_url_in_reference():
    import xml.etree.ElementTree as ET
    root = ET.parse('report/apa.csl').getroot()
    ns = {'c': 'http://purl.org/net/xbiblio/csl'}
    bib = root.find("c:macro[@name='bibliography']", ns)
    elements = list(bib.iter())
    note = next(e for e in elements if e.attrib.get('variable') == 'note')
    urls = [e for e in elements if e.attrib.get('macro') == 'source-DOI-URL']
    assert elements.index(note) < elements.index(urls[-1])


def test_report_figure_derivatives_preserve_yaml_and_original_png(tmp_path, monkeypatch):
    from pathlib import Path
    from src.pipeline import main
    import json
    root = Path('.')
    (tmp_path / 'report').mkdir()
    canonical = b"datos: {n_series: '13'}\n"
    (tmp_path / 'report/_variables.yml').write_bytes(canonical)
    folder = tmp_path / 'outputs/tables'
    folder.mkdir(parents=True)
    for name in ['stress_levels.csv', 'stress_delta.csv']:
        (folder / name).write_bytes((root / 'outputs/tables' / name).read_bytes())
    figures = tmp_path / 'outputs/figures'
    figures.mkdir()
    original = (root / 'outputs/figures/stress_model1.png').read_bytes()
    (figures / 'stress_model1.png').write_bytes(original)
    monkeypatch.setenv('PIPELINE_ROOT', str(tmp_path))
    assert main(['report']) == 0
    assert (tmp_path / 'report/_variables.yml').read_bytes() == canonical
    assert (figures / 'stress_model1.png').read_bytes() == original
    assert (tmp_path / 'outputs/informe/stress_model1_presentacion.png').is_file()
    assert (tmp_path / 'specs/006-informe/interfaz.md').is_file()


def test_figure_caption_source_is_not_duplicated_by_quarto_figure_ast():
    import subprocess, json
    binary = 'C:/Program Files/Quarto/bin/tools/pandoc.exe'
    doc = json.loads(subprocess.check_output([binary, '-f', 'markdown', '-t', 'json'], input=b''))
    doc['blocks'] = [{'t': 'Figure', 'c': [['', [], []], [None, [{'t': 'Plain', 'c': [{'t': 'Str', 'c': 'Respuesta. Fuente: FRED; elaboración propia.'}]}]], []]}]
    rendered = subprocess.check_output([binary, '-f', 'json', '-t', 'json', '--lua-filter=report/filters/slug-links.lua'], input=json.dumps(doc).encode())
    assert 'Fuente:' not in rendered.decode()
    assert 'Respuesta' in rendered.decode()


def test_reference_compound_does_not_break_with_a_duplicate_hyphen():
    import subprocess, json
    binary = 'C:/Program Files/Quarto/bin/tools/pandoc.exe'
    source = b'---\nreferences:\n- id: example\n  type: article-journal\n  title: Non-performing loans\n---\n[@example]\n'
    rendered = subprocess.check_output([binary, '-f', 'markdown', '-t', 'json', '--lua-filter=report/filters/apa-references.lua'], input=source)
    assert 'Non\u2011performing' in rendered.decode('utf8')
