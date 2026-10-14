"""Authorized reader-facing corrections from the fifth audit."""
from pathlib import Path
from src.report_tables import build_report_tables, presentation_note
from src.report_editorial import build_editorial_documents, build_report_registry


def test_empty_reason_note_explains_absence_without_csv_process_language():
    source = 'estado,motivo\nestimada,\nno estimada,sin observaciones\n'
    result = build_report_tables({'model1_robustness_estimates': source})
    text = '\n'.join(result['files'].values())
    assert 'vacíos del CSV' not in text
    assert 'no se informa una causa de no estimación' in text
    assert 'sin observaciones' in text


def test_preregistration_label_is_not_tautological():
    assert presentation_note('Pre-registro de la spec 003') == 'Pre-registro del Modelo I'
    assert presentation_note('Pre-registro de la spec 004') == 'Pre-registro del Modelo II'


def test_comparison_note_identifies_both_principal_estimates():
    source = 'el coeficiente del Modelo I se lee de las salidas de la spec 003'
    assert 'ambos modelos provienen de sus estimaciones principales' in presentation_note(source)


def test_small_body_tables_keep_caption_rows_and_note_together():
    sources = {'fred_manifest': Path('data/raw/manifest.csv').read_text(encoding='utf-8-sig'),
               'model1_diagnostics': 'prueba,estadistico,p_valor,veredicto\nBG,1,0.2,pasa\n',
               'model2_inputs63': 'modelo,termino,coef,p_valor,n\nmodelo1,d_ffr,0.2,0.02,100\n'}
    tables = build_report_tables(sources)
    docs = build_editorial_documents(build_report_registry({k:v.encode() for k,v in sources.items()}, {}), sources, tables)
    for name in sources:
        assert docs['body_files'][name + '_cuerpo.md'].startswith('::: {.compact-body-table}')
    assert 'breakable: false' in Path('report/filters/slug-links.lua').read_text(encoding='utf8')


def test_literature_note_does_not_refer_to_its_own_section():
    from src.report_tables import literature_report_table
    source = literature_report_table(Path('research/matriz-literatura.md').read_text(encoding='utf8')).to_csv(index=False)
    docs = build_editorial_documents(build_report_registry({'lit_estudios': source.encode()}, {}), {'lit_estudios': source}, build_report_tables({'lit_estudios': source}))
    assert 'descrito en 2.5' not in docs['body_files']['lit_estudios_cuerpo.md']


def test_matrix_corrects_fgls_without_changing_applicability():
    text = Path('research/matriz-literatura.md').read_text(encoding='utf8')
    assert 'mínimos cuadrados generalizables factibles' not in text
    assert 'mínimos cuadrados generalizados factibles' in text


def test_obradovic_note_retains_verified_unemployment_and_exchange_findings():
    from src.report_tables import literature_report_table
    row = literature_report_table(Path('research/matriz-literatura.md').read_text(encoding='utf8')).set_index('clave').loc['obradovic2026']
    assert 'desempleo es negativo' in row['nota']
    assert 'tipo de cambio oficial no es consistente' in row['nota']
    assert row['signo'] == '—'
    assert '. el efecto' not in row['nota']
