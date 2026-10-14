"""Regressions for R3-X1–X7; presentation must not invent scientific values."""
from pathlib import Path
from src.report_tables import build_report_tables, presentation_note, display_cell


def test_vif_labels_are_translated_in_test_names_and_limitations():
    assert display_cell('VIF (d_ffr_l0)', 'prueba') == 'VIF (Cambio de tasa contemporáneo)'
    assert display_cell('VIF (d_ffr_l1)', 'prueba') == 'VIF (Cambio de tasa, rezago 1)'
    assert 'd_unemp' not in presentation_note('VIF (d_unemp) elevado')


def test_empty_diagnostic_values_remain_empty_but_are_explained():
    source = 'prueba,estadístico,p_valor,veredicto,nota\nVIF (d_unemp),36.8,,alerta,\nCUSUM,,,pasa,\n'
    result = build_report_tables({'model1_diagnostics': source})
    text = result['files']['model1_diagnostics.md']
    assert 'VIF no es una prueba con p-valor' in text
    assert 'CUSUM' in text and 'no exporta' in text
    rows = result['trace']['model1_diagnostics']['presentation']['rows']
    assert rows[0][2] == '' and rows[1][1:3] == ['', '']


def test_text_only_and_date_tables_have_no_rounding_note():
    result = build_report_tables({'fred_manifest': 'series,source,download_date\nX,FRED,2026-10-02\n',
                                  'model2_reading': 'elemento,resultado\nC2,no\n'})
    assert all('Cifras redondeadas' not in text for text in result['files'].values())


def test_stress_rule_note_has_a_reason_and_one_source():
    note = presentation_note('Nota: ΔFFR se fija en cero por la regla heredada. Fuente: FRED.')
    assert 'mientras la lectura del Modelo II no sea de evidencia fuerte' in note


def test_reader_text_has_no_grammar_or_form_template_remnants():
    files = ['03b-variables', '03e-desviaciones', '11-datos-descarga']
    for name in files:
        text = (Path('report/secciones') / (name + '.qmd')).read_text(encoding='utf8')
        assert 'los especificaciones' not in text
        assert 'en la forma {{< var modelo1.forma_y >}}' not in text


def test_macro_figure_caption_explains_its_source_and_recession_shading():
    text = Path('report/secciones/03a-datos.qmd').read_text(encoding='utf8')
    assert 'Fuente: FRED' in text and 'USREC' in text


def test_literature_signs_remain_cautious_with_provenance_outside_the_cell():
    from src.report_tables import literature_report_table
    from src.report_editorial import build_report_registry, build_editorial_documents
    frame = literature_report_table(Path('research/matriz-literatura.md').read_text(encoding='utf8'))
    source = frame.to_csv(index=False)
    tables = build_report_tables({'lit_estudios': source})
    result = build_editorial_documents(build_report_registry({'lit_estudios': source.encode()}, {}), {'lit_estudios': source}, tables)
    body = result['body_files']['lit_estudios_cuerpo.md']
    assert 'no significa un coeficiente cero ni un signo ausente' in body
    assert 'Procedencia de Golitsis' in body and 'Nota de la Tabla 1' in body
    rows = result['body_trace']['lit_estudios']['rows']
    assert all('(texto completo,' not in row[-1] for row in rows)
    assert frame.set_index('clave').loc['obradovic2026', 'signo'] == '—'


def test_stress_body_has_one_source_and_a_noncircular_rule():
    from src.report_editorial import build_report_registry, build_editorial_documents
    source = Path('outputs/tables/stress_delta.csv').read_text(encoding='utf8')
    note = 'ΔFFR se fija en cero por la regla heredada. Fuente: FRED. Advertencia: no truncar.'
    presentation = build_report_tables({'stress_delta': source}, source_notes={'stress_delta': note})
    body = build_editorial_documents(build_report_registry({'stress_delta': source.encode()}, {}), {'stress_delta': source}, presentation)['body_files']['stress_delta_cuerpo.md']
    assert body.count('Fuente:') == 1
    assert 'mientras la lectura del Modelo II no sea de evidencia fuerte' in body


def test_macro_figure_keeps_its_caption_source_in_pandoc():
    import subprocess, json
    binary = 'C:/Program Files/Quarto/bin/tools/pandoc.exe'
    source = b'![Morosidad. Fuente: FRED; USREC.](../outputs/figures/delinquency_unemployment_ffr.png)\n'
    doc = json.loads(subprocess.check_output([binary, '-f', 'markdown', '-t', 'json'], input=source))
    rendered = subprocess.check_output([binary, '-f', 'json', '-t', 'json', '--lua-filter=report/filters/slug-links.lua'], input=json.dumps(doc).encode())
    assert b'Fuente:' in rendered and b'USREC' in rendered


def test_typst_doi_has_an_explicit_ascii_label_and_unchanged_destination():
    import subprocess
    binary = 'C:/Program Files/Quarto/bin/tools/pandoc.exe'
    url = 'https://doi.org/10.2478/ceej-2023-0016'
    rendered = subprocess.check_output([binary, '-f', 'markdown', '-t', 'typst', '--lua-filter=report/filters/slug-links.lua'], input=('<'+url+'>').encode()).decode()
    assert '#link("' + url + '")[' in rendered
    assert '#box[' in rendered
    assert 'ceej-2023-0016' in rendered.split(')[')[1]


def test_bibliography_doi_is_processed_before_typst_label_filter():
    import subprocess
    binary = 'C:/Program Files/Quarto/bin/tools/pandoc.exe'
    source = b'---\nbibliography: report/references.bib\ncsl: report/apa.csl\n---\n[@zawadzki2023]\n'
    rendered = subprocess.check_output([binary, '-f', 'markdown', '-t', 'typst',
        '--lua-filter=report/filters/apa-references.lua',
        '--lua-filter=report/filters/slug-links.lua', '--citeproc'], input=source).decode()
    url = 'https://doi.org/10.2478/ceej-2023-0016'
    assert rendered.count('#link("' + url + '")[') == 1
    assert rendered.count('<ref-zawadzki2023>') == 1
