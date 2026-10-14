"""Audit regressions: presentation may not fabricate scientific precision."""
import csv
import io
import subprocess
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
ROOT = Path(__file__).resolve().parents[1]


def test_pdf_page_fallback_uses_named_destination_and_actual_page_order():
    from src.report_editorial import pdf_named_destination_pages, link_registry_csv
    pdf = b'''%PDF-1.7
1 0 obj <</Type/Catalog/Pages 7 0 R/Names[(at-m1-x)21 0 R]>> endobj
7 0 obj <</Type/Pages/Kids[11 0 R 12 0 R]/Count 2>> endobj
11 0 obj <</Type/Page/Parent 7 0 R>> endobj
12 0 obj <</Type/Page/Parent 7 0 R>> endobj
21 0 obj [12 0 R/XYZ 72 700 null] endobj
'''
    pages = pdf_named_destination_pages(pdf)
    assert pages == {'at-m1-x': 2}
    registry = [{'slug': 'AT-M1-X', 'anchor': 'at-m1-x'}]
    rows = list(csv.DictReader(io.StringIO(link_registry_csv(registry, pages))))
    assert rows[0]['pdf'] == 'anexo-tecnico.pdf#nameddest=at-m1-x&page=2'
    assert rows[0]['docx'] == 'anexo-tecnico.docx#at-m1-x'
    with pytest.raises(ValueError, match='PDF'):
        pdf_named_destination_pages(pdf.replace(b'[12 0 R/XYZ', b'[99 0 R/XYZ'))


def test_pdf_fallback_does_not_invent_pages_before_annex_exists():
    from src.report_editorial import link_registry_csv
    registry = [{'slug': 'AT-M1-X', 'anchor': 'at-m1-x'}]
    assert '&page=' not in link_registry_csv(registry)


@pytest.mark.parametrize('column', ['p', 'p_valor', 'adf_p', 'p_S', 'p_S_rez', 'dm_p'])
def test_small_p_values_are_inequalities_not_rounded_zero(column):
    from src.report_tables import format_report_cell
    assert format_report_cell('0.00076', column) == '< 0,001'
    assert format_report_cell('0.001', column) == '0,001'
    assert format_report_cell('0.0105', column) == '0,011'


@pytest.mark.parametrize('value,expected', [('0.1', '0,100'), ('0.01', '0,010'),
                                           ('>0,10', '≥ 0,10'), ('<0,01', '≤ 0,01'),
                                           ('0.0876128', '0,088')])
def test_kpss_censoring_preserves_bounds(value, expected):
    from src.report_tables import format_report_cell
    assert format_report_cell(value, 'kpss_p') == expected


def test_kpss_exact_value_and_documented_limit_are_distinct():
    from src.report_tables import build_report_tables
    source = 'variable,forma,kpss_p,kpss_p_truncado\nx,tal cual,0.1,\ny,tal cual,0.1,">0,10"\n'
    rows = build_report_tables({'stationarity': source})['trace']['stationarity']['presentation']['rows']
    assert rows[0][2] == '0,100'
    assert rows[1][2] == '≥ 0,10'


@pytest.mark.parametrize('bound', ['> 0,10', '≥ 0,10', '< 0,01', '≤ 0,01'])
def test_kpss_approved_markdown_bound_is_preserved_with_source_trace(bound):
    from src.report_tables import build_report_tables
    value = '0.1' if '0,10' in bound else '0.01'
    source = f'termino,forma,kpss_p\nx,tal cual,{value}\n'
    markdown = f'| termino | forma | kpss_p |\n| --- | --- | --- |\n| x | tal cual | {bound} |\n'
    result = build_report_tables({'model1_stationarity': source}, source_markdown={'model1_stationarity': markdown})
    assert result['trace']['model1_stationarity']['presentation']['rows'][0][2] == bound.replace('>', '≥').replace('<', '≤')
    assert result['trace']['model1_stationarity']['censoring_source']['sha256']


def test_kpss_markdown_mismatched_identity_cannot_supply_censoring():
    from src.report_tables import build_report_tables
    source = 'termino,forma,kpss_p\nx,tal cual,0.1\n'
    markdown = '| termino | forma | kpss_p |\n| --- | --- | --- |\n| another | tal cual | > 0,10 |\n'
    with pytest.raises(ValueError, match='KPSS'):
        build_report_tables({'model1_stationarity': source}, source_markdown={'model1_stationarity': markdown})


def test_student_cover_metadata_is_exact_in_both_documents():
    import yaml
    for name in ('informe', 'anexo-tecnico'):
        metadata = yaml.safe_load((ROOT / 'report' / (name + '.qmd')).read_text(encoding='utf-8').split('---')[1])
        assert metadata['subtitle'] == 'NEG-LIF309-01 Control y gestión de riesgos · Profesor: Ramfis Félix Tatis'
        assert metadata['author'] == 'Gabriel Read'
        assert metadata['affiliation'] == 'Instituto Tecnológico de Santo Domingo (INTEC)'
        assert metadata['date'] == '16 de octubre de 2026'


def test_every_stress_panel_identifies_model_scenario_and_quarter():
    from src.report_tables import build_report_tables
    source = 'modelo,escenario,trimestre,delta,p05,p95,delta_final\nmodelo1,severo,2026T3,0.2,-0.1,0.5,0.4\n'
    result = build_report_tables({'stress_delta': source})
    for panel in result['trace']['stress_delta']['annex_panels']:
        assert {'modelo', 'escenario', 'trimestre'} <= set(panel['columns'])
        assert len(panel['columns']) <= 5


def test_every_robustness_panel_identifies_variant_and_term():
    from src.report_tables import build_report_tables
    source = 'variante,etiqueta,inicio,fin,termino,coef,p,estado,motivo\nR1,Sin pandemia,2000T1,2026T2,inflation,0.2,0.03,estimada,\n'
    result = build_report_tables({'model1_robustness_estimates': source})
    for panel in result['trace']['model1_robustness_estimates']['annex_panels']:
        assert {'variante', 'termino'} <= set(panel['columns'])


def test_stationarity_panels_identify_series_and_transformation():
    from src.report_tables import build_report_tables
    source = ',variable,forma,adf_p,kpss_p,decision\n0,dralacbs,primera diferencia,0.0095,0.1,niveles\n'
    result = build_report_tables({'stationarity': source})
    for panel in result['trace']['stationarity']['annex_panels']:
        assert {'variable', 'forma'} <= set(panel['columns'])


@pytest.mark.parametrize('name,source,identity', [
    ('model1_effects', 'termino,efecto,escala,estimacion,p\ninflation,impacto,unidad,0.2,0.03\ninflation,largo plazo,unidad,0.4,0.04\n', {'termino', 'efecto', 'escala'}),
    ('stress_sensitivity', 'modelo,escenario,sensibilidad,regla,nivel_final,delta_final\nmodelo1,severo,cero,fija,2.0,1.0\nmodelo1,severo,media,fija,2.1,1.1\n', {'modelo', 'escenario', 'sensibilidad'}),
    ('model2_inputs63', 'modelo,termino,coef,p,n_obs,controles\nmodelo1,d_ffr,0.1,0.2,106,actuales\nmodelo1,inflation,0.2,0.3,106,actuales\n', {'modelo', 'termino'}),
])
def test_panels_keep_complete_row_identity_in_remaining_multikey_tables(name, source, identity):
    from src.report_tables import build_report_tables
    for panel in build_report_tables({name: source})['trace'][name]['annex_panels']:
        assert identity <= set(panel['columns'])


def test_presentation_labels_keep_raw_trace_and_no_product_paths():
    from src.report_tables import build_report_tables
    source = 'termino,coef,p\ngdp_growth,-0.02,0.0001\n'
    result = build_report_tables({'model1_coefficients': source})
    text = result['files']['model1_coefficients.md']
    assert 'PIB (crecimiento)' in text and 'gdp_growth' not in text
    assert 'Fuente: FRED; elaboración propia.' in text
    assert 'outputs/tables' not in text
    assert result['trace']['model1_coefficients']['source'] == 'outputs/tables/model1_coefficients.csv'


def test_nominal_gdp_robustness_never_gets_a_real_gdp_label():
    from src.report_tables import build_report_tables
    source = 'variante,etiqueta,termino,coef,p\nR4,PIB nominal,gdp_growth,-0.02,0.2\n'
    result = build_report_tables({'model1_robustness_estimates': source})
    text = '\n'.join(result['files'].values())
    assert 'PIB nominal' in text
    assert 'PIB real' not in text
    assert 'PIB (crecimiento)' in text


@pytest.mark.parametrize('note', ['regla de la spec 001 aplicada a la primera diferencia',
                                  'Signo no reutilizado: observaciones opcionales de 002 pendientes; consultar matriz y auditoría.'])
def test_product_notes_remove_operational_messages_but_trace_keeps_source(note):
    from src.report_tables import build_report_tables
    source = 'termino,coef,nota\nx,0.1,' + note + '\n'
    result = build_report_tables({'model1_coefficients': source})
    import hashlib
    assert result['trace']['model1_coefficients']['source_sha256'] == hashlib.sha256(source.encode()).hexdigest()
    text = '\n'.join(result['files'].values())
    assert 'spec 001' not in text and 'observaciones opcionales' not in text and 'auditoría' not in text
    if note.startswith('regla'):
        assert 'primera diferencia' in text
    else:
        assert 'signo' in text.lower() and 'no presentada' in text


def test_text_only_literature_has_no_rounding_or_absent_sign_note():
    from src.report_editorial import build_report_registry, build_editorial_documents
    from src.report_tables import build_report_tables
    source = 'clave,estudio,dependiente,regresores,metodo,signo,seccion_principal\na2020,A (2020),Morosidad,PIB,Panel,—,2.5\n'
    registry = build_report_registry({'lit_estudios': source.encode()}, {})
    result = build_editorial_documents(registry, {'lit_estudios': source}, build_report_tables({'lit_estudios': source}))
    text = result['body_files']['lit_estudios_cuerpo.md']
    assert 'redondead' not in text and 'ceros' not in text and 'signos no reutilizados' not in text
    assert '#nameddest=at-lit-estudios' in text
    assert 'Abrir anexo' not in text
    assert 'anexo-tecnico.docx' not in text  # the format filter adapts the single slug link


def test_slug_links_resolve_registry_and_unknown_slug_fails():
    from src.report_editorial import linkify_slug_references
    registry = [{'slug': 'AT-M2-LP', 'anchor': 'at-m2-lp', 'annex': 'C'}]
    assert linkify_slug_references('Ver **AT-M2-LP**.', registry) == 'Ver [Anexo C, AT-M2-LP](anexo-tecnico.pdf#nameddest=at-m2-lp).'
    assert linkify_slug_references('Ver **AT-M2-LP**.', registry, combined=True) == 'Ver [Anexo C, AT-M2-LP](#at-m2-lp).'
    linked = '[Anexo C, AT-M2-LP](anexo-tecnico.pdf#nameddest=at-m2-lp)'
    assert linkify_slug_references(linked, registry) == linked
    with pytest.raises(ValueError, match='desconocido'):
        linkify_slug_references('**AT-NO-EXISTE**', registry)


def test_apa_table_numbers_follow_section_order_literature_before_data():
    from src.report_editorial import BODY_ORDER
    assert BODY_ORDER[:2] == ['lit_estudios', 'fred_manifest']


def test_docx_reference_relationships_can_be_reused_without_unbound_prefixes():
    import zipfile
    with zipfile.ZipFile(ROOT / 'report/templates/apa-reference.docx') as z:
        for name in z.namelist():
            if name.endswith(('.xml', '.rels')):
                ET.fromstring(z.read(name))
        relationships = z.read('word/_rels/document.xml.rels')
        assert b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"' in relationships
        assert b'<ns0:Relationship' not in relationships


def test_rendered_apa_data_reference_and_verified_publication_details():
    from src.references import parse_bib
    entries = {e.key: e for e in parse_bib((ROOT / 'report/references.bib').read_text(encoding='utf8'))}
    assert entries['fred2026'].fields['urldate'] == '2026-10-02'
    assert 'DRALACBS' in entries['fred2026'].fields['note'] and 'USREC' in entries['fred2026'].fields['note']
    assert entries['newey1987'].fields['pages'] == '703–708'
    assert entries['nkusu2011'].fields['number'] == '2011/161'
    assert entries['segoviano2006'].fields['number'] == '2006/283'
    assert entries['fred2026'].entry_type == 'misc'
    assert entries['frb2026'].fields['institution'] == 'Board of Governors of the Federal Reserve System'
    ns = {'c': 'http://purl.org/net/xbiblio/csl'}
    style = ET.parse(ROOT / 'report/apa.csl')
    assert style.find('.//c:if[@type="dataset"][@variable="accessed"]', ns) is not None
    assert style.find('.//c:if[@type="dataset"]/c:text[@variable="note"]', ns) is not None
    executable = shutil.which('pandoc')
    local = Path('C:/Program Files/Quarto/bin/tools/pandoc.exe')
    if not executable and local.is_file():
        executable = str(local)
    # Core assertions run everywhere without an additional CLI dependency.
    # Installed publication tooling additionally verifies actual citeproc output.
    if executable is None:
        return
    pandoc = Path(executable)
    result = subprocess.run([str(pandoc), '-f', 'markdown', '-t', 'plain',
                             '--lua-filter=report/filters/apa-references.lua',
                             '--citeproc',
                             '--bibliography=report/references.bib', '--csl=report/apa.csl',
                             '-M', 'lang=es'], cwd=ROOT, input='[@fred2026; @newey1987; @nkusu2011; @segoviano2006; @frb2026]',
                            text=True, encoding='utf8', capture_output=True, check=True)
    text = result.stdout
    assert 'DRALACBS' in text and 'USREC' in text
    assert '2026' in text and 'octubre' in text and '2' in text
    assert '703–708' in text
    assert '2011/161' in text and '2006/283' in text
    bibliography = text.split('\n\n', 1)[1]
    assert bibliography.count('Board of Governors of the Federal Reserve System') == 1
