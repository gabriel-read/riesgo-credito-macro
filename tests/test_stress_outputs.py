"""Stress presentation is generated from results, never hand-entered figures."""
import io

import numpy as np
import pandas as pd
import pytest

from src.stress_tables import STRESS_TABLES, render_stress_tables, stress_variables
from src.stress_figures import stress_figure, stress_figure_png


def synthetic_tables():
    return {name:pd.DataFrame({'modelo':['modelo1'],'escenario':['base'],'valor':[1.23456789]})
            for name in STRESS_TABLES}


def test_tables_have_full_precision_csv_and_spanish_decimal_markdown():
    rendered=render_stress_tables(synthetic_tables())
    assert set(rendered)==set(STRESS_TABLES)
    for csv_text,md_text in rendered.values():
        assert '1.23456789' in csv_text
        assert '1,235' in md_text
        assert 'Nota:' in md_text and 'parámetros' in md_text
        assert 'sensibilidad, no efecto estimado' in rendered['stress_rate_sensitivity'][1]
    bad=synthetic_tables(); bad['stress_delta'].loc[0,'valor']=np.inf
    with pytest.raises(ValueError,match='finito'):
        render_stress_tables(bad)


def test_variables_are_derived_text_and_keep_scenario_dimensions():
    values={'horizonte':{'origen':pd.Period('2026Q2'),'h':13},
            'sens_cred':{'modelo1':{'base':{'cero':{'nivel_final':1.23456789}},
                                   'severo':{'cero':{'nivel_final':2.3456789}}}}}
    result=stress_variables(values)
    assert result['horizonte']=={'origen':'2026T2','h':'13'}
    assert result['sens_cred']['modelo1']['base']['cero']['nivel_final']=='1,235'
    assert result['sens_cred']['modelo1']['severo']['cero']['nivel_final']=='2,346'


def test_table_footnotes_warn_only_when_levels_are_out_of_range():
    tables = synthetic_tables()
    tables['stress_levels'] = pd.DataFrame({'modelo': ['modelo1'],
        'n_replicas_fuera_rango_modelo': [2], 'prop_replicas_fuera_rango_modelo': [.25],
        'nivel_min_modelo': [-2.34567], 'nivel_max_modelo': [103.12345]})
    rendered = render_stress_tables(tables)
    for name in ['stress_levels', 'stress_delta']:
        note = rendered[name][1].split('Nota:')[1]
        assert 'Advertencia: niveles fuera de [0, 100]' in note
        assert 'sin truncar' in note and 'modelo1' in note
        assert '2' in note and '0,250' in note and '-2,346' in note and '103,123' in note
    tables['stress_levels']['n_replicas_fuera_rango_modelo'] = 0
    assert 'Advertencia:' not in render_stress_tables(tables)['stress_levels'][1]


def test_halfway_rounding_matches_cells_variables_and_both_footnotes():
    tables = synthetic_tables()
    tables['stress_levels'] = pd.DataFrame({'modelo': ['modelo1'],
        'n_replicas_fuera_rango_modelo': [105],
        'prop_replicas_fuera_rango_modelo': [np.float64(.0105)],
        'nivel_min_modelo': [np.float64(-.0105)],
        'nivel_max_modelo': [np.float64(100.0105)]})
    variables = stress_variables({'prop': np.float64(.0105),
                                  'min': np.float64(-.0105), 'max': np.float64(100.0105)})
    assert variables['prop'] == '0,011'
    rendered = render_stress_tables(tables)
    csv_text, markdown = rendered['stress_levels']
    cells = [cell.strip() for cell in markdown.splitlines()[2].split('|')[1:-1]]
    assert cells[2:] == [variables['prop'], variables['min'], variables['max']]
    assert '0.0105' in csv_text  # Original full precision, no rounding in CSV.
    for name in ['stress_levels', 'stress_delta']:
        note = rendered[name][1].split('\n\nNota:', 1)[1]
        assert f"(proporción {variables['prop']})" in note
        assert f"mínimo {variables['min']}, máximo {variables['max']}" in note
        assert '(proporción 0,010)' not in note


def test_mixed_counterfactual_observation_column_is_formatted_without_losing_csv_precision():
    tables=synthetic_tables()
    tables['stress_origin']=pd.DataFrame({'DR_observado':[1.456789,'no aplica'],'observado':[True,False]})
    csv_text,markdown=render_stress_tables(tables)['stress_origin']
    assert '1.456789' in csv_text
    assert '1,457' in markdown and 'sí' in markdown and 'no aplica' in markdown


def test_markdown_escapes_pipe_cells_without_changing_csv_text():
    import re
    tables = synthetic_tables()
    tables['stress_limitations'] = pd.DataFrame({'modelo': ['modelo1'], 'tipo': ['explosivas'],
                                               'limitacion': ['Réplicas con |ρ| ≥ 1\nSin descartar.']})
    csv_text, markdown = render_stress_tables(tables)['stress_limitations']
    assert '|ρ|' in csv_text and '\nSin descartar.' in csv_text
    assert r'\|ρ\|' in markdown and '<br>Sin descartar.' in markdown
    lines = [line for line in markdown.splitlines() if line.startswith('|')]
    assert len(lines) == 3
    assert all(len(re.split(r'(?<!\\)\|', line)) == 5 for line in lines)


def synthetic_figures():
    index=pd.period_range('2026Q3',periods=13,freq='Q-DEC')
    levels={s:pd.DataFrame({'dr':np.linspace(1,2,13),'p05':.5,'p95':2.5},index=index)
            for s in ['base','severo','propio']}
    delta={s:pd.DataFrame({'delta':np.linspace(0,1,13),'p05':-.5,'p95':1.5},index=index)
           for s in ['severo','propio']}
    return levels,delta


def test_figure_has_two_panels_bands_spanish_labels_source_and_deterministic_png():
    import matplotlib.pyplot as plt
    levels,delta=synthetic_figures()
    fig=stress_figure(levels,delta)
    assert len(fig.axes)==2
    assert all('pp' in ax.get_ylabel() for ax in fig.axes)
    assert fig.axes[0].collections and fig.axes[1].collections
    assert any('Fuente: FRED' in text.get_text() for text in fig.texts)
    assert any('no es un intervalo de predicción' in text.get_text() for text in fig.texts)
    plt.close(fig)
    a=stress_figure_png(levels,delta)
    assert a==stress_figure_png(levels,delta)
    assert a.startswith(b'\x89PNG')
