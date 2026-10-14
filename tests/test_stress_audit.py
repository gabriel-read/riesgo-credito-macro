"""Contract regressions requested by independent audit 005, round 1."""
import json
from pathlib import Path

import pandas as pd
import pytest

from src.pipeline import load_fed_sources, load_stress_history
from src.stress import read_model_contract, run_stress


@pytest.fixture(scope='module')
def audit_result():
    # Restore the sampler before other tests execute; cache only the computed result.
    with pytest.MonkeyPatch.context() as monkeypatch:
        return small_audit_result(monkeypatch)


def small_audit_result(monkeypatch):
    """Exercise actual orchestration with small draws; full N is tested in integration."""
    import src.stress as stress
    draw = stress.draw_model_params
    monkeypatch.setattr(stress, 'draw_model_params', lambda contract: draw(contract, n=20))
    root = Path.cwd()
    contracts = {m: read_model_contract(json.loads((root/f'outputs/models/{file}_main.json').read_text(encoding='utf-8')), m)
                 for m, file in [('modelo1', 'model1'), ('modelo2', 'model2')]}
    fed = load_fed_sources(root/'data/scenarios/fed/2026-final/2026-10-11')
    history = load_stress_history(root, contracts['modelo1'].origin)
    diagnostics = {m: pd.read_csv(root/f'outputs/tables/{file}_diagnostics.csv', keep_default_na=False)
                   for m, file in [('modelo1', 'model1'), ('modelo2', 'model2')]}
    oos = pd.read_csv(root/'outputs/tables/model1_oos.csv', keep_default_na=False)
    return run_stress(contracts, fed, history, diagnostics, oos)


def expected_variable_keys():
    # Independent transcription of approved plan §5, including every dimension.
    level = {'nivel_final', 'nivel_pico', 'nivel_pico_trimestre'}
    delta = {'delta_'+s for s in ['final', 'final_p05', 'final_p95', 'pico', 'pico_trimestre',
                                 'min', 'sin_aumento', 'prop_pos_final', 'prop_pos_pico']}
    tree = {'horizonte': {'origen', 'inicio', 'fin', 'h'}, 'replicas': {'n', 'semilla'},
            'dif_modelos': {s: {'delta_final', 'delta_pico'} for s in ['severo', 'propio']},
            'sens_tasa': {}, 'sens_cal': {}, 'sens_cred': {}, 'sens_origen': {}}
    for m in ['modelo1', 'modelo2']:
        tree[m] = {'base': level, 'severo': level | delta, 'propio': level | delta,
                   'credito': {'n_observados', 'n_supuestos'}, 'fuera_rango': {'n', 'prop', 'min', 'max'},
                   'explosivas': {'n', 'prop'}}
        tree['sens_tasa'][m] = {s: {'c_final', 'c_final_p05', 'c_final_p95', 'c_pico',
                                   'prop_c_pos_final', 'prop_c_pos_pico'} for s in ['severo', 'propio']}
        tree['sens_cal'][m] = {'delta_final_2029t1', 'delta_principal_2029t1', 'delta_pico'}
        tree['sens_cred'][m] = {s: {c: level for c in ['cero', 'media']} for s in ['base', 'severo']}
        tree['sens_origen'][m] = {'base': level, 'severo': level | {'delta_k13'}}
    return tree


def assert_key_tree(actual, expected):
    assert set(actual) == set(expected)
    if isinstance(expected, dict):
        for key in expected:
            assert_key_tree(actual[key], expected[key])
    else:
        assert all(isinstance(value, str) for value in actual.values())


def test_complete_estres_key_tree_matches_approved_plan(audit_result):
    assert_key_tree(audit_result['variables'], expected_variable_keys())


def test_levels_report_replica_totals_extremes_and_affected_quarters(audit_result):
    frame = audit_result['tables']['stress_levels']
    for model, (levels, _) in audit_result['graphics'].items():
        for scenario, summary in levels.items():
            rows = frame[(frame.modelo == model) & (frame.escenario == scenario)]
            for column, attr in [('n_replicas_fuera_rango', 'n_fuera_rango'),
                                 ('prop_replicas_fuera_rango', 'prop_fuera_rango'),
                                 ('nivel_min', 'min'), ('nivel_max', 'max'),
                                 ('n_trimestres_fuera', 'n_trimestres_fuera')]:
                assert (rows[column] == summary.attrs[attr]).all()
            assert (rows.prop_trimestres_fuera == summary.attrs['n_trimestres_fuera']/len(summary)).all()
        rows = frame[frame.modelo == model]
        for column, leaf in [('n_replicas_fuera_rango_modelo', 'n'),
                             ('prop_replicas_fuera_rango_modelo', 'prop'),
                             ('nivel_min_modelo', 'min'), ('nivel_max_modelo', 'max')]:
            # Stored report variables round floats; numeric CSV metadata stays full precision.
            from src.stress_tables import stress_variables
            assert stress_variables({'v': rows[column].iloc[0]})['v'] == audit_result['variables'][model]['fuera_rango'][leaf]
            assert rows[column].nunique() == 1


def test_model_peak_difference_is_difference_of_peaks_not_peak_of_difference(audit_result):
    from src.stress_tables import stress_variables
    for scenario in ['severo', 'propio']:
        a = audit_result['graphics']['modelo1'][1][scenario].delta
        b = audit_result['graphics']['modelo2'][1][scenario].delta
        expected = stress_variables({'delta_pico': float(a.max()-b.max()),
                                     'delta_final': float(a.iloc[-1]-b.iloc[-1])})
        assert audit_result['variables']['dif_modelos'][scenario] == expected
        assert expected['delta_pico'] != stress_variables({'v': float((a-b).max())})['v']
        frame = audit_result['tables']['stress_models']
        rows = frame[frame.escenario == scenario]
        import numpy as np
        np.testing.assert_allclose(rows.diferencia_I_II, (a-b).to_numpy(), atol=1e-12, rtol=0)


def test_origin_headers_are_spanish_in_actual_table_and_both_renderings(audit_result):
    from src.stress_tables import render_stress_tables
    table = audit_result['tables']['stress_origin']
    assert {'trimestre_adaptado', 'trimestre_original'} <= set(table)
    assert not {'adapted_quarter', 'original_quarter'} & set(table)
    for text in render_stress_tables(audit_result['tables'])['stress_origin']:
        assert 'trimestre_adaptado' in text and 'trimestre_original' in text
        assert 'adapted_quarter' not in text and 'original_quarter' not in text


def test_language_in_all_eight_rendered_table_pairs_and_estres_tree(audit_result):
    from src.stress_tables import render_stress_tables, STRESS_TABLES
    from tests.test_language import find_causal_language, _strings
    rendered = render_stress_tables(audit_result['tables'])
    assert set(rendered) == set(STRESS_TABLES)
    for name, pair in rendered.items():
        assert all(not find_causal_language(text) for text in pair), name
    assert all(not find_causal_language(text) for text in _strings(audit_result['variables']))
