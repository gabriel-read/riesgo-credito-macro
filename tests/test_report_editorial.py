"""Editorial routing keeps approved sources and identifiers independent of pagination."""
from pathlib import Path
import hashlib
import pytest

ROOT = Path(__file__).resolve().parents[1]


def sources():
    return ({p.stem: p.read_bytes() for p in (ROOT / 'outputs/tables').glob('*.csv')},
            {p.stem: p.read_bytes() for p in (ROOT / 'outputs/figures').glob('*.png')})


def test_registry_covers_real_sources_once_and_preserves_byte_hashes():
    from src.report_editorial import build_report_registry
    tables, figures = sources()
    registry = build_report_registry(tables, figures)
    assert len(registry) == len(tables) + len(figures)
    assert len({r['slug'] for r in registry}) == len(registry)
    assert len({r['source'] for r in registry}) == len(registry)
    for entry in registry:
        assert entry['annex'] in 'ABCDEF'
        assert entry['sha256'] == hashlib.sha256((ROOT / entry['source']).read_bytes()).hexdigest()
    by_source = {r['source']: r for r in registry}
    assert by_source['outputs/tables/model2_lp.csv']['slug'] == 'AT-M2-LP'
    assert by_source['outputs/tables/model1_robustness_estimates.csv']['slug'] == 'AT-M1-ROB'


def test_slugs_do_not_depend_on_input_order_or_missing_other_tables():
    from src.report_editorial import build_report_registry
    tables, figures = sources()
    all_rows = build_report_registry(tables, figures)
    subset = build_report_registry({'model2_lp': tables['model2_lp']}, {})
    assert subset[0]['slug'] == next(r['slug'] for r in all_rows if r['name'] == 'model2_lp')
    assert all_rows == build_report_registry(dict(reversed(list(tables.items()))), figures)


@pytest.mark.parametrize('kind', ['table', 'figure'])
def test_unknown_source_is_not_silently_assigned_a_destination(kind):
    from src.report_editorial import build_report_registry
    with pytest.raises(ValueError, match='desconocida'):
        build_report_registry({'unknown': b'a\n'} if kind == 'table' else {},
                              {'unknown': b'PNG'} if kind == 'figure' else {})


def test_report_stage_writes_registry_and_interface_destinations(tmp_path, monkeypatch):
    from src.pipeline import main
    monkeypatch.setenv('PIPELINE_ROOT', str(tmp_path))
    (tmp_path / 'report').mkdir()
    (tmp_path / 'report/_variables.yml').write_bytes(b'datos: {n_series: "13"}\n')
    folder = tmp_path / 'outputs/tables'
    folder.mkdir(parents=True)
    (folder / 'model2_lp.csv').write_bytes(b'h,phi,phi_nota\n0,1.0,identity\n')
    assert main(['report']) == 0
    assert 'AT-M2-LP' in (tmp_path / 'outputs/informe/registro.csv').read_text(encoding='utf8')
    assert 'AT-M2-LP' in (tmp_path / 'specs/006-informe/interfaz.md').read_text(encoding='utf8')
    first = (tmp_path / 'specs/006-informe/interfaz.md').read_bytes()
    assert main(['report']) == 0
    assert first == (tmp_path / 'specs/006-informe/interfaz.md').read_bytes()


def test_editorial_annex_covers_all_sources_once_and_keeps_body_reduced():
    from src.report_editorial import build_report_registry, build_editorial_documents
    from src.report_tables import build_report_tables
    tables, figures = sources()
    texts = {k: v.decode('utf8') for k, v in tables.items()}
    presentation = build_report_tables(texts)
    registry = build_report_registry(tables, figures)
    documents = build_editorial_documents(registry, texts, presentation)
    annex = '\n'.join(documents['annex_files'].values())
    for entry in registry:
        assert annex.count('{#' + entry['anchor'] + '}') == 1
    assert set(documents['annex_files']) == {'A-datos.qmd', 'B-modelo-i.qmd', 'C-modelo-ii.qmd',
                                             'D-estres.qmd', 'E-literatura.qmd', 'F-reproducibilidad.qmd'}
    assert 'model2_lp_anexo_5.md' not in annex
    assert '**Tabla ' in documents['body_files']['model1_coefficients_cuerpo.md']
    assert 'Tabla completa:' in documents['body_files']['model1_coefficients_cuerpo.md']
    assert 'AT-M1-COEFFICIENTS' in documents['body_files']['model1_coefficients_cuerpo.md']
    assert len(documents['body_trace']['stress_delta']['rows']) == 4  # two models x two adverse paths


def test_phi_notes_retain_each_source_row_without_an_empty_note_panel():
    import csv, io
    from src.report_tables import build_report_tables
    tables, _ = sources()
    result = build_report_tables({'model2_lp': tables['model2_lp'].decode('utf8')})
    trace = result['trace']['model2_lp']
    original = list(csv.DictReader(io.StringIO(tables['model2_lp'].decode('utf8'))))
    assert trace['note_columns'] == ['phi_nota']
    assert trace['field_notes'] == [{'h': r['h'], 'phi_nota': r['phi_nota']} for r in original]
    assert 'model2_lp_anexo_5.md' not in result['files']


def test_two_documents_and_optional_combined_keep_complete_annex_out_of_main():
    import yaml
    config = yaml.safe_load((ROOT / '_quarto.yml').read_text(encoding='utf8'))
    assert config['project']['render'] == ['report/informe.qmd', 'report/anexo-tecnico.qmd']
    assert 'anexos/tablas.qmd' not in (ROOT / 'report/informe.qmd').read_text(encoding='utf8')
    annex = (ROOT / 'report/anexo-tecnico.qmd').read_text(encoding='utf8')
    for prefix in 'ABCDEF':
        assert 'anexos/' + prefix + '-' in annex
    assert 'entrega-combinada.qmd' not in config['project']['render']
    assert (ROOT / 'report/entrega-combinada.qmd').is_file()


def test_combined_changes_external_body_links_to_internal_destinations():
    from src.report_editorial import combined_source
    main = '---\ntitle: sample\n---\n{{< include secciones/a.qmd >}}\n'
    sections = {'secciones/a.qmd': '# Heading\n{{< include ../outputs/informe/model2_reading_cuerpo.md >}}'}
    bodies = {'model2_reading_cuerpo.md': 'AT-M2-READING [PDF](anexo-tecnico.pdf) [DOCX](anexo-tecnico.docx)'}
    registry = [{'name': 'model2_reading', 'anchor': 'at-m2-reading'}]
    combined = combined_source(main, sections, bodies, registry)
    assert 'include ../outputs/informe/model2_reading_cuerpo_combinado.md' in combined
    assert 'anexo-tecnico.pdf' not in combined
    assert '{{< include anexos/' in combined


def test_optional_combined_profile_retains_project_root_and_generated_table_sources():
    import yaml
    profile = yaml.safe_load((ROOT / '_quarto-combinado.yml').read_text(encoding='utf8'))
    assert profile['project']['render'] == ['report/entrega-combinada.qmd']
    from src.report_editorial import build_report_registry, build_editorial_documents
    from src.report_tables import build_report_tables
    tables, figures = sources()
    texts = {k: v.decode('utf8') for k, v in tables.items()}
    documents = build_editorial_documents(build_report_registry(tables, figures), texts, build_report_tables(texts))
    combined = documents['body_files']['model2_reading_cuerpo_combinado.md']
    assert '[Anexo C, AT-M2-READING](#at-m2-reading)' in combined
    assert 'anexo-tecnico.pdf' not in combined


def test_other_approved_table_notes_are_kept_as_generated_includes():
    from src.report_tables import build_report_tables
    from src.report_editorial import build_report_registry, build_editorial_documents
    csv_text = 'termino,coef,p\ninflation,0.01,0.02\n'
    note = 'Nota aprobada: HAC y unidades originales; 0,010 no es una cifra nueva.'
    result = build_report_tables({'model1_coefficients': csv_text}, {'model1_coefficients': note})
    assert result['files']['model1_coefficients_nota.md'].strip() == note
    documents = build_editorial_documents(build_report_registry({'model1_coefficients': csv_text.encode()}, {}),
                                         {'model1_coefficients': csv_text}, result)
    assert 'include ../outputs/informe/model1_coefficients_nota.md' in documents['annex_files']['B-modelo-i.qmd']
    assert note in documents['body_files']['model1_coefficients_cuerpo.md']


def test_literature_body_matches_declared_empirical_section_count_and_keeps_variables_methods():
    import yaml
    from src.report_editorial import build_report_registry, build_editorial_documents
    from src.report_tables import build_report_tables
    tables, figures = sources()
    texts = {k: v.decode('utf8') for k, v in tables.items()}
    result = build_editorial_documents(build_report_registry(tables, figures), texts, build_report_tables(texts))
    expected = int(yaml.safe_load((ROOT / 'report/_variables.yml').read_text(encoding='utf8'))['literatura']['por_tema']['t25'])
    assert len(result['body_trace']['lit_estudios']['rows']) == expected
    assert result['body_trace']['lit_estudios']['columns'] == ['estudio', 'dependiente', 'regresores', 'metodo', 'signo']


def test_every_variable_used_by_report_sections_exists_in_canonical_yaml():
    import re, yaml
    variables = yaml.safe_load((ROOT / 'report/_variables.yml').read_text(encoding='utf8'))
    for file in (ROOT / 'report/secciones').glob('*.qmd'):
        for key in re.findall(r'\{\{< var ([a-zA-Z0-9_.]+) >\}\}', file.read_text(encoding='utf8')):
            value = variables
            for part in key.split('.'):
                assert isinstance(value, dict) and part in value, (file, key)
                value = value[part]


@pytest.mark.parametrize('task,names', [
    ('T5', ['01-introduccion', '02-literatura', '03f-limitaciones']),
    ('T6', ['04-modelo1', '05-modelo2']),
    ('T7', ['06-resultados']), ('T8', ['07-estres']), ('T9', ['08-implicaciones', '09-conclusiones']),
])
def test_narrative_task_has_no_unfilled_sections(task, names):
    for name in names:
        text = (ROOT / 'report/secciones' / (name + '.qmd')).read_text(encoding='utf8')
        assert 'PENDIENTE' not in text, (task, name)
        assert len([line for line in text.splitlines() if line.strip() and not line.startswith('#')]) >= 3, (task, name)
