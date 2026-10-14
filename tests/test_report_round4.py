"""Reader-facing fixes for the limited fourth independent review."""
from pathlib import Path
import json
import subprocess

from src.report_tables import build_report_tables, literature_report_table, display_cell, presentation_note
from src.report_editorial import build_report_registry, build_editorial_documents


def literature():
    return literature_report_table(Path('research/matriz-literatura.md').read_text(encoding='utf8'))


def test_diagnostic_notes_explain_results_once_without_process_language():
    source = 'prueba,estadistico,p_valor,veredicto,nota\nVIF (d_unemp),36.8,,alerta,\nCUSUM,,,pasa,\n'
    result = build_report_tables({'model2_diagnostics': source})
    panels = result['trace']['model2_diagnostics']['annex_panels']
    texts = [result['files'][panel['file']] for panel in panels]
    assert sum(text.count('VIF no es una prueba con p-valor') for text in texts) == 1
    assert all('salida aprobada' not in text and 'el CSV no añade' not in text for text in texts)
    assert 'salida del modelo' in texts[0]
    assert 'información adicional' in texts[1]
    assert panels[0]['rows'][0][2] == '' and panels[0]['rows'][1][1:3] == ['', '']


def test_obradovic_note_matches_verified_lending_sign_without_reusing_policy_sign():
    row = literature().set_index('clave').loc['obradovic2026']
    assert row['signo'] == '—'
    assert 'resumen del estudio' in row['nota']
    assert 'asociación positiva' in row['nota'] and 'tasa de préstamo' in row['nota']
    assert 'no es la tasa de política' in row['nota']
    assert 'Lectura de signo no presentada' not in presentation_note(row['nota'])


def test_obradovic_note_does_not_invent_a_sign_if_backing_is_absent():
    matrix = Path('research/matriz-literatura.md').read_text(encoding='utf8')
    changed = matrix.replace('lending sobre la morosidad es positivo y significativo', 'lending sobre la morosidad no se informa')
    assert changed != matrix
    note = literature_report_table(changed).set_index('clave').loc['obradovic2026', 'nota']
    assert 'asociación positiva' not in note


def test_literature_note_is_identified_and_attached_to_the_table():
    source = literature().to_csv(index=False)
    tables = build_report_tables({'lit_estudios': source})
    docs = build_editorial_documents(build_report_registry({'lit_estudios': source.encode()}, {}), {'lit_estudios': source}, tables)
    body = docs['body_files']['lit_estudios_cuerpo.md']
    assert body.startswith('::: {.literature-summary}') and body.rstrip().endswith(':::')
    assert body.count('Nota de la Tabla 1') == 1
    assert 'Procedencia de Golitsis et al.: texto completo, resultados de largo plazo y Tabla 4' in body
    assert '\n\nBase consultada para Golitsis' not in body
    assert 'no significa un coeficiente cero ni un signo ausente' in body


def test_reader_notes_keep_scientific_qualifications_without_internal_routing():
    note = Path('outputs/tables/model2_inputs63.md').read_text(encoding='utf8').split('Nota:')[-1]
    rendered = presentation_note('Nota:' + note)
    assert 'la redacción de la comparación' not in rendered and 'spec' not in rendered
    assert 'asociaciones condicionales' in rendered and 'errores HAC' in rendered
    assert 'estimaciones principales' in rendered
    assert 'consultar la matriz' not in presentation_note('Sin signo literal extraído; consultar la matriz.')


def test_generalized_estimator_is_correct_but_generalizable_results_stay_generalizable():
    assert display_cell('mínimos cuadrados generalizables factibles (FGLS)', 'metodo') == 'mínimos cuadrados generalizados factibles (FGLS)'
    assert presentation_note('Estos resultados no son generalizables a otros países.') == 'Estos resultados no son generalizables a otros países.'


def test_literature_widths_change_only_its_layout_not_any_cell():
    binary = 'C:/Program Files/Quarto/bin/tools/pandoc.exe'
    source = b'::: {.literature-summary}\n\n| A | B | C | D | E |\n|---|---|---|---|---|\n| a | b | c | d | e |\n\n::: '
    before = json.loads(subprocess.check_output([binary, '-f', 'markdown', '-t', 'json'], input=source))
    after = json.loads(subprocess.check_output([binary, '-f', 'json', '-t', 'json', '--lua-filter=report/filters/slug-links.lua'], input=json.dumps(before).encode()))
    original = before['blocks'][0]['c'][1][0]['c']
    updated = after['blocks'][0]['c'][1][0]['c']
    assert updated[2] != original[2]
    assert original[3:] == updated[3:]
