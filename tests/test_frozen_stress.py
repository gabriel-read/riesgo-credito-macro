"""005 integration over frozen sources; never network or source modifications."""
import hashlib
import shutil
from pathlib import Path

import pandas as pd
import pytest
import yaml

from src.pipeline import stage_stress
from src.stress_tables import STRESS_TABLES


def digests(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


SCIENTIFIC_OUTPUTS = frozenset({
    'outputs/figures/delinquency_unemployment_ffr.png',
    'outputs/figures/model1_coefficients.png',
    'outputs/figures/model1_cusum.png',
    'outputs/figures/model1_oos.png',
    'outputs/figures/model2_cusum.png',
    'outputs/figures/model2_profile.png',
    'outputs/figures/model2_response.png',
    'outputs/figures/stress_model1.png',
    'outputs/figures/stress_model2.png',
    'outputs/models/model1_main.json',
    'outputs/models/model2_main.json',
    'outputs/tables/descriptives.csv',
    'outputs/tables/descriptives.md',
    'outputs/tables/model1_coefficients.csv',
    'outputs/tables/model1_coefficients.md',
    'outputs/tables/model1_deviations.csv',
    'outputs/tables/model1_deviations.md',
    'outputs/tables/model1_diagnostics.csv',
    'outputs/tables/model1_diagnostics.md',
    'outputs/tables/model1_effects.csv',
    'outputs/tables/model1_effects.md',
    'outputs/tables/model1_limitations.csv',
    'outputs/tables/model1_limitations.md',
    'outputs/tables/model1_oos.csv',
    'outputs/tables/model1_oos.md',
    'outputs/tables/model1_robustness_estimates.csv',
    'outputs/tables/model1_robustness_estimates.md',
    'outputs/tables/model1_robustness_summary.csv',
    'outputs/tables/model1_robustness_summary.md',
    'outputs/tables/model1_stationarity.csv',
    'outputs/tables/model1_stationarity.md',
    'outputs/tables/model2_coefficients.csv',
    'outputs/tables/model2_coefficients.md',
    'outputs/tables/model2_comparison.csv',
    'outputs/tables/model2_comparison.md',
    'outputs/tables/model2_deviations.csv',
    'outputs/tables/model2_deviations.md',
    'outputs/tables/model2_diagnostics.csv',
    'outputs/tables/model2_diagnostics.md',
    'outputs/tables/model2_effects.csv',
    'outputs/tables/model2_effects.md',
    'outputs/tables/model2_inputs63.csv',
    'outputs/tables/model2_inputs63.md',
    'outputs/tables/model2_limitations.csv',
    'outputs/tables/model2_limitations.md',
    'outputs/tables/model2_lp.csv',
    'outputs/tables/model2_lp.md',
    'outputs/tables/model2_reading.csv',
    'outputs/tables/model2_reading.md',
    'outputs/tables/model2_robustness_estimates.csv',
    'outputs/tables/model2_robustness_estimates.md',
    'outputs/tables/model2_robustness_summary.csv',
    'outputs/tables/model2_robustness_summary.md',
    'outputs/tables/model2_selection.csv',
    'outputs/tables/model2_selection.md',
    'outputs/tables/model2_stationarity.csv',
    'outputs/tables/model2_stationarity.md',
    'outputs/tables/model2_trajectory.csv',
    'outputs/tables/model2_trajectory.md',
    'outputs/tables/stationarity.csv',
    'outputs/tables/stationarity.md',
    'outputs/tables/stress_delta.csv',
    'outputs/tables/stress_delta.md',
    'outputs/tables/stress_levels.csv',
    'outputs/tables/stress_levels.md',
    'outputs/tables/stress_limitations.csv',
    'outputs/tables/stress_limitations.md',
    'outputs/tables/stress_models.csv',
    'outputs/tables/stress_models.md',
    'outputs/tables/stress_origin.csv',
    'outputs/tables/stress_origin.md',
    'outputs/tables/stress_paths.csv',
    'outputs/tables/stress_paths.md',
    'outputs/tables/stress_rate_sensitivity.csv',
    'outputs/tables/stress_rate_sensitivity.md',
    'outputs/tables/stress_sensitivity.csv',
    'outputs/tables/stress_sensitivity.md',
    'outputs/data_note.md',
})

MUTABLE_STRESS_OUTPUTS = frozenset({
    'outputs/figures/stress_model1.png',
    'outputs/figures/stress_model2.png',
    'outputs/tables/stress_delta.csv',
    'outputs/tables/stress_delta.md',
    'outputs/tables/stress_levels.csv',
    'outputs/tables/stress_levels.md',
    'outputs/tables/stress_limitations.csv',
    'outputs/tables/stress_limitations.md',
    'outputs/tables/stress_models.csv',
    'outputs/tables/stress_models.md',
    'outputs/tables/stress_origin.csv',
    'outputs/tables/stress_origin.md',
    'outputs/tables/stress_paths.csv',
    'outputs/tables/stress_paths.md',
    'outputs/tables/stress_rate_sensitivity.csv',
    'outputs/tables/stress_rate_sensitivity.md',
    'outputs/tables/stress_sensitivity.csv',
    'outputs/tables/stress_sensitivity.md',
})
EDITORIAL_OUTPUTS = frozenset({"outputs/tables/lit_estudios.csv", "outputs/tables/lit_estudios.md"})

def scientific_inventory(root, allow_editorial=False):
    expected = set(SCIENTIFIC_OUTPUTS)
    observed = {p.relative_to(root).as_posix()
                for folder in ["outputs/models", "outputs/tables", "outputs/figures"]
                for p in (root/folder).rglob("*") if p.is_file() and p.name != ".gitkeep"}
    if (root/"outputs/data_note.md").is_file():
        observed.add("outputs/data_note.md")
    if allow_editorial:
        observed -= EDITORIAL_OUTPUTS
    assert observed == expected, {"missing": sorted(expected-observed), "unexpected": sorted(observed-expected)}
    return {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in sorted(expected)}

def assert_protected(before, after):
    assert set(before) == set(after) == set(SCIENTIFIC_OUTPUTS)
    assert all(before[name] == after[name] for name in SCIENTIFIC_OUTPUTS-MUTABLE_STRESS_OUTPUTS)

def copy_scientific_outputs(source, destination):
    scientific_inventory(source, allow_editorial=True)
    for name in sorted(SCIENTIFIC_OUTPUTS):
        target = destination/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source/name, target)


@pytest.fixture(scope='module')
def frozen_runs(tmp_path_factory):
    root=tmp_path_factory.mktemp('stress005')
    for name in ['data/raw','data/scenarios','data/processed']:
        shutil.copytree(name,root/name)
    copy_scientific_outputs(Path.cwd(), root)
    (root/'report').mkdir()
    shutil.copyfile('report/_variables.yml',root/'report/_variables.yml')
    before_data=digests(root/'data')
    before_outputs=scientific_inventory(root)
    old_vars=yaml.safe_load((root/'report/_variables.yml').read_text(encoding='utf-8'))
    import os
    previous=os.environ.get('PIPELINE_ROOT')
    os.environ['PIPELINE_ROOT']=str(root)
    try:
        assert stage_stress()==0
        first=scientific_inventory(root)
        assert_protected(before_outputs, first)
        first_vars=(root/'report/_variables.yml').read_bytes()
        assert stage_stress()==0
        second=scientific_inventory(root)
        assert_protected(before_outputs, second)
        assert first==second
        assert first_vars==(root/'report/_variables.yml').read_bytes()
    finally:
        if previous is None:
            os.environ.pop('PIPELINE_ROOT',None)
        else:
            os.environ['PIPELINE_ROOT']=previous
    assert before_data==digests(root/'data')
    new_vars=yaml.safe_load(first_vars.decode('utf-8'))
    assert all(new_vars[k]==old_vars[k] for k in ['datos','modelo1','modelo2'])
    return root,new_vars['estres']


def test_all_stress_outputs_reproducible_preserve_sources_and_other_models(frozen_runs):
    root,variables=frozen_runs
    for name in STRESS_TABLES:
        assert (root/f'outputs/tables/{name}.csv').stat().st_size>0
        assert 'Nota:' in (root/f'outputs/tables/{name}.md').read_text(encoding='utf-8')
    for model in ['model1','model2']:
        assert (root/f'outputs/figures/stress_{model}.png').read_bytes().startswith(b'\x89PNG')
    assert variables['horizonte']=={'origen':'2026T2','inicio':'2026T3','fin':'2029T3','h':'13'}
    assert variables['replicas']['n']=='10000'
    for m in ['modelo1','modelo2']:
        assert variables[m]['credito']=={'n_observados':'4','n_supuestos':'9'}
        assert variables[m]['severo']['delta_final']==variables[m]['propio']['delta_final']
        assert set(variables['sens_cred'][m])=={'base','severo'}


def test_real_origin_delta_and_model2_first_step_zero(frozen_runs):
    root,_=frozen_runs
    origin=pd.read_csv(root/'outputs/tables/stress_origin.csv')
    assert (origin.groupby(['modelo','escenario']).size()==13).all()
    assert abs(origin.delta_adaptado-origin.delta_original).max()<1e-9
    delta=pd.read_csv(root/'outputs/tables/stress_delta.csv')
    first=delta[(delta.modelo=='modelo2')&(delta.trimestre=='2026T3')]
    assert (first.delta==0).all()
    limits=(root/'outputs/tables/stress_limitations.md').read_text(encoding='utf-8')
    assert 'endogeneidad' in limits and 'crédito' in limits


def test_all_rendered_stress_tables_and_estres_variables_use_association_language(frozen_runs):
    from tests.test_language import find_causal_language, _strings
    root, variables = frozen_runs
    for name in STRESS_TABLES:
        for suffix in ['csv', 'md']:
            path = root/f'outputs/tables/{name}.{suffix}'
            assert find_causal_language(path.read_text(encoding='utf-8')) == [], str(path)
    assert all(not find_causal_language(text) for text in _strings(variables))


def test_frozen_estres_has_exact_approved_key_tree(frozen_runs):
    from tests.test_stress_audit import assert_key_tree, expected_variable_keys
    _, variables = frozen_runs
    assert_key_tree(variables, expected_variable_keys())


def test_changed_source_hash_stops_before_any_projection(tmp_path,monkeypatch):
    shutil.copytree('data/scenarios',tmp_path/'data/scenarios')
    source=tmp_path/'data/scenarios/fed/2026-final/2026-10-11/2026_Final_Supervisory_Baseline_Domestic.csv'
    source.write_bytes(source.read_bytes()+b'\r\n')
    monkeypatch.setenv('PIPELINE_ROOT',str(tmp_path))
    with pytest.raises(ValueError,match='sha256'):
        stage_stress()
    assert not (tmp_path/'outputs').exists()


def test_saved_panel_mismatch_stops_before_projection(tmp_path,monkeypatch):
    for name in ['data/raw','data/scenarios','data/processed','outputs/models']:
        shutil.copytree(name,tmp_path/name)
    panel_path=tmp_path/'data/processed/panel.csv'
    panel=pd.read_csv(panel_path,index_col=0)
    panel.iloc[-1,panel.columns.get_loc('dralacbs')]+=1
    panel.to_csv(panel_path)
    monkeypatch.setenv('PIPELINE_ROOT',str(tmp_path))
    with pytest.raises(ValueError,match='panel'):
        stage_stress()
    assert not (tmp_path/'outputs/tables').exists()
