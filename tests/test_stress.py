"""Tests of pre-registered stress machinery, spec 005, synthetic fits first."""
import copy

import numpy as np
import pandas as pd
import pytest

from src.stress import quarter_to_period, read_model_contract, columns_to_design, project


@pytest.mark.parametrize('label', ['2026T2','2026Q2','2026 Q2'])
def test_quarter_labels_share_one_period(label):
    assert quarter_to_period(label) == pd.Period('2026Q2')


def test_model1_contract_rebuilds_approved_historical_design(model1_result):
    from tests.synthetic_model1 import make_full
    contract = read_model_contract(model1_result.stress, 'modelo1')
    expected = model1_result.design.X
    X = columns_to_design(contract, make_full(), pd.DataFrame(index=expected.index))
    pd.testing.assert_frame_equal(X, expected, check_names=False)
    assert contract.origin == pd.Period('2026Q2')
    assert contract.dependent_column == 'dralacbs_d'


def test_model2_contract_rebuilds_approved_historical_design(model2_result):
    from tests.synthetic_model2 import make_full2
    contract = read_model_contract(model2_result.export, 'modelo2')
    expected = model2_result.main_fit.design.X
    X = columns_to_design(contract, make_full2(), pd.DataFrame(index=expected.index))
    pd.testing.assert_frame_equal(X, expected, check_names=False)


def test_reader_rejects_order_map_and_shape_changes(model1_result):
    for mutate in [lambda d: d['terms'].reverse(),
                   lambda d: d['columns'].__setitem__('d_ffr','fedfunds'),
                   lambda d: d['params'].pop(),
                   lambda d: d.__setitem__('form','nivel')]:
        bad = copy.deepcopy(model1_result.stress)
        mutate(bad)
        with pytest.raises(ValueError,match='contrato'):
            read_model_contract(bad,'modelo1')


def test_adapter_matches_closed_form_and_rebuilds_levels(model1_result):
    contract = read_model_contract(model1_result.stress,'modelo1')
    params = pd.Series(0.,index=contract.terms)
    params['const'], params['y_lag'] = .2,.5
    index = pd.period_range('2026Q3','2029Q3',freq='Q-DEC')
    X = pd.DataFrame(0.,index=index,columns=params.index)
    X['const'] = 1.
    result = project(contract,params,X,2.,.1,[])
    expected = np.array([.4 + (.1-.4)*.5**k for k in range(1,14)])
    np.testing.assert_allclose(result['ddr'],expected,rtol=1e-10,atol=1e-12)
    np.testing.assert_allclose(result['dr'],2+np.cumsum(expected),atol=1e-12)


def test_adapter_reproduces_predefined_training_forecast_without_zero_rule(model1_result):
    from tests.synthetic_model1 import make_full
    oos = model1_result.oos
    contract = read_model_contract(model1_result.stress,'modelo1')
    train = oos.train_fit.params
    # Train has no COVID terms: align zero dummy coefficients without refitting.
    params = train.reindex(contract.terms,fill_value=0.)
    full = make_full()
    X = columns_to_design(contract,full,pd.DataFrame(index=oos.series.index))
    result = project(contract,params,X,float(full.loc['2021Q4','dralacbs']),
                     float(full.dralacbs.diff().loc['2021Q4']),[])
    np.testing.assert_allclose(result.dr,oos.series.dinamico,atol=1e-12,rtol=0)


def test_draws_recover_mean_covariance_in_mc_tolerances_and_repeat():
    from src.stress import sym_block, draw_params
    mean = np.array([.5,-.2,.1])
    V = np.array([[.01,.003,0],[.003,.02,.001],[0,.001,.005]])
    block = sym_block(pd.DataFrame(V,index=['a','b','c'],columns=['a','b','c']),[])
    samples = draw_params(mean,block,200000,np.random.default_rng(20261011))
    np.testing.assert_array_equal(samples,draw_params(mean,block,200000,np.random.default_rng(20261011)))
    assert (np.abs(samples.mean(axis=0)-mean) <= 4*np.sqrt(np.diag(V)/len(samples))).all()
    S = np.cov(samples,rowvar=False,ddof=1)
    assert np.linalg.norm(S-V)/np.linalg.norm(V) < .02
    assert (np.abs(S-V)/np.sqrt(np.outer(np.diag(V),np.diag(V)))).max() < .02
    with pytest.raises(ValueError,match='positivo'):
        draw_params(mean,np.zeros((3,3)),10,np.random.default_rng(1))


def test_rate_rule_pairs_same_other_coefficients_and_zero_dummies(model2_result):
    from src.stress import draw_model_params
    raw = copy.deepcopy(model2_result.export)
    raw['reading']['etiqueta'] = 'sin evidencia'
    contract = read_model_contract(raw,'modelo2')
    principal,sensitivity = draw_model_params(contract,100)
    for j,term in enumerate(contract.terms):
        if term in contract.zero_terms:
            assert (principal[:,j] == 0).all()
        else:
            np.testing.assert_array_equal(principal[:,j],sensitivity[:,j])
        if term.startswith('covid_'):
            assert (sensitivity[:,j] == 0).all()
    with pytest.raises(ValueError,match='change'):
        draw_model_params(read_model_contract(model2_result.export,'modelo2'),100)
    bad = copy.deepcopy(raw)
    bad['cov_hac'] = np.zeros_like(np.asarray(bad['cov_hac'])).tolist()
    with pytest.raises(ValueError,match='modelo2.*positivo'):
        draw_model_params(read_model_contract(bad,'modelo2'),100)


def simple_projection_inputs(model1_result):
    contract = read_model_contract(model1_result.stress,'modelo1')
    params = pd.Series(0.,index=contract.terms)
    params['const'],params['y_lag'],params['gdp_growth'],params['credit_growth'] = .2,.5,.1,.3
    index = pd.period_range('2026Q3','2029Q3',freq='Q-DEC')
    X = pd.DataFrame(0.,index=index,columns=contract.terms)
    X['const'] = 1.
    return contract,params,X


def delta_recursion(params, base_X, adv_X):
    """Independent RNF-5 oracle: only scenario differences, δ at origin = 0."""
    differences = adv_X - base_X
    previous = 0.
    increments = []
    for _, row in differences.iterrows():
        previous = float(params.y_lag)*previous + sum(
            float(params[term])*float(row[term]) for term in params.index if term != 'y_lag')
        increments.append(previous)
    return np.cumsum(increments)


def test_replicate_projection_matches_each_approved_dynamic(model1_result):
    from src.stress import project_replicas
    contract,params,X = simple_projection_inputs(model1_result)
    draws = np.vstack([params.to_numpy(),params.to_numpy()+.001])
    paths = project_replicas(contract,draws,X,2,.1)
    for j,row in enumerate(draws):
        expected = project(contract,pd.Series(row,index=contract.terms),X,2,.1,[])
        np.testing.assert_allclose(paths[j],expected.dr,atol=1e-12,rtol=0)


def test_summary_signed_peak_tie_nonpositive_and_no_clipping():
    from src.stress import summarize_delta, summarize_levels
    index = pd.period_range('2026Q3',periods=3,freq='Q-DEC')
    base = pd.DataFrame({'dr':[1.,1.,1.]},index=index)
    adv = pd.DataFrame({'dr':[2.,3.,3.]},index=index)
    draws_base = np.ones((4,3))
    draws_adv = np.array([[2,3,3],[3,5,4],[-2,-1,0],[101,102,103.]])
    result = summarize_delta(adv,base,draws_adv,draws_base)
    assert result.attrs['pico_trimestre'] == '2026T4'
    assert result.attrs['delta_pico'] == 2
    assert result.iloc[-1].prop_pos == .75
    levels = summarize_levels(adv,draws_adv,np.array([.5,.6,1.1,-1.2]))
    assert levels.attrs['n_explosivas'] == 2
    assert levels.attrs['n_fuera_rango'] == 2
    assert levels.attrs['min'] == -2 and levels.attrs['max'] == 103
    assert levels.iloc[0].p05 < 0
    negative = summarize_delta(base,adv,draws_base,draws_adv)
    assert negative.attrs['sin_aumento'] is True
    assert negative.attrs['delta_min'] == -2
    with pytest.raises(ValueError,match='no finito'):
        summarize_levels(adv,draws_adv*np.inf,np.array([.5,.6,1.1,-1.2]))


def test_delta_cancels_common_anchor_constant_credit_but_not_differing_inputs(model1_result):
    contract,params,X = simple_projection_inputs(model1_result)
    adv = X.copy(); adv['gdp_growth'] = 1.
    def delta(coefficients,base_X,adv_X,level=2.,anchor=.1):
        return (project(contract,coefficients,adv_X,level,anchor,[]).dr -
                project(contract,coefficients,base_X,level,anchor,[]).dr).to_numpy()
    expected = delta_recursion(params,X,adv)
    np.testing.assert_allclose(delta(params,X,adv),expected,atol=1e-12,rtol=0)
    altered = params.copy(); altered['const'] = 3.
    a,b = X.copy(),adv.copy(); a['credit_growth']=9.; b['credit_growth']=9.
    np.testing.assert_allclose(delta(altered,a,b,5.,.7),expected,atol=1e-12,rtol=0)
    b['credit_growth']=10.
    assert not np.allclose(delta(params,a,b),expected,atol=1e-12,rtol=0)
    altered['gdp_growth'] = .2
    # Different β in adverso: the oracle assumes common β and no longer applies.
    changed_beta = (project(contract,altered,adv,2.,.1,[]).dr -
                    project(contract,params,X,2.,.1,[]).dr).to_numpy()
    assert not np.allclose(changed_beta,expected,atol=1e-12,rtol=0)


def test_log_yoy_origin_invariance_and_negative_nonlog_case(model1_result):
    from src.scenarios import to_levels
    history_index = pd.period_range('2024Q1','2026Q2',freq='Q-DEC')
    observed = pd.Series([90,95,100,102,105,110,116,118,124,126],index=history_index)
    contract, params, template = simple_projection_inputs(model1_result)
    log_deltas, simple_deltas = [],[]
    for origin in [pd.Period('2025Q4'),pd.Period('2026Q2')]:
        index = pd.period_range(origin+1,periods=13,freq='Q-DEC')
        base = pd.DataFrame({'Real GDP growth':2.,'CPI inflation rate':2.,
                             'Unemployment rate':4.,'3-month Treasury rate':3.},index=index)
        adv = base.copy(); adv['Real GDP growth']=-5.
        for path in [base,adv]:
            path.attrs['reference']=pd.Series({'Unemployment rate':4.,'3-month Treasury rate':3.})
        a=to_levels(adv,observed,observed,4,3)
        b=to_levels(base,observed,observed,4,3)
        ax, bx = template.copy(), template.copy()
        ax.index = bx.index = index
        ax.gdp_growth = a.gdp_growth
        bx.gdp_growth = b.gdp_growth
        expected = delta_recursion(params,bx,ax)
        np.testing.assert_allclose(project(contract,params,ax,2.,.1,[]).dr-
                                   project(contract,params,bx,2.,.1,[]).dr,
                                   expected,atol=1e-12,rtol=0)
        log_deltas.append(expected)
        # Simple percentage year-on-year breaks invariance when the observed origin changes.
        for levels, X in [(a,ax),(b,bx)]:
            joined=pd.concat([observed.loc[:origin],levels.gdpc1])
            X.gdp_growth=(100*(joined/joined.shift(4)-1)).loc[index]
        wrong = (project(contract,params,ax,2.,.1,[]).dr-
                 project(contract,params,bx,2.,.1,[]).dr).to_numpy()
        assert not np.allclose(wrong,expected,atol=1e-12,rtol=0)
        simple_deltas.append(wrong)
    np.testing.assert_allclose(log_deltas[0],log_deltas[1],atol=1e-12,rtol=0)
    assert not np.allclose(*simple_deltas,atol=1e-12,rtol=0)


def test_common_linear_innovations_cancel_but_different_ones_do_not(model1_result):
    contract,params,X=simple_projection_inputs(model1_result)
    adv=X.copy(); adv.gdp_growth=1.
    a=project(contract,params,adv,2,.1,[]).dr.to_numpy()
    b=project(contract,params,X,2,.1,[]).dr.to_numpy()
    common=np.cumsum(np.array([.1*.5**k for k in range(13)]))
    expected=delta_recursion(params,X,adv)
    np.testing.assert_allclose((a+common)-(b+common),expected,atol=1e-12,rtol=0)
    assert not np.allclose((a+common)-b,expected,atol=1e-12,rtol=0)
    # A distinct observed ΔDR lag enters both models' first forecast step.
    assert not np.allclose(project(contract,params,adv,2,.6,[]).dr-b,expected,atol=1e-12,rtol=0)


@pytest.mark.parametrize('which', ['modelo1', 'modelo2'])
def test_different_step_one_reference_breaks_scenario_only_delta_oracle(which, model1_result, model2_result):
    from src.scenarios import to_levels
    from tests.synthetic_model1 import make_full
    from tests.synthetic_model2 import make_full2
    result = model1_result.stress if which == 'modelo1' else model2_result.export
    contract = read_model_contract(result, which)
    history = (make_full() if which == 'modelo1' else make_full2()).loc[:contract.origin]
    index = pd.period_range(contract.origin+1, periods=13, freq='Q-DEC')
    observed = pd.Series(100., index=pd.period_range('2024Q1', contract.origin, freq='Q-DEC'))
    base = pd.DataFrame({'Real GDP growth': 2., 'CPI inflation rate': 2.,
                         'Unemployment rate': 4., '3-month Treasury rate': 3.}, index=index)
    adv = base.copy(); adv['Unemployment rate'] = 5.
    reference = pd.Series({'Unemployment rate': 4., '3-month Treasury rate': 3.})
    def design(path, ref):
        path = path.copy(); path.attrs['reference'] = ref
        regs = to_levels(path, observed, observed, 4., 3.)
        regs['credit_growth'] = 0.
        return columns_to_design(contract, history, regs)
    b, a = design(base, reference), design(adv, reference)
    params = pd.Series(0., index=contract.terms)
    params['y_lag'] = .5
    params['d_unemp' if which == 'modelo1' else 'd_unemp_l1'] = .4
    expected = delta_recursion(params, b, a)
    baseline = project(contract, params, b, 2., .1, []).dr
    np.testing.assert_allclose(project(contract, params, a, 2., .1, []).dr-baseline,
                               expected, atol=1e-12, rtol=0)
    other_reference = reference.copy(); other_reference['Unemployment rate'] = 3.
    bad = design(adv, other_reference)
    wrong_delta = project(contract, params, bad, 2., .1, []).dr-baseline
    assert not np.allclose(wrong_delta, expected, atol=1e-12, rtol=0)
    # In II the changed reference enters the observed lag at step 2, not step 1.
    first_effect = 0 if which == 'modelo1' else 1
    assert wrong_delta.iloc[first_effect] != pytest.approx(expected[first_effect], abs=1e-12)


@pytest.mark.parametrize('which', ['modelo1', 'modelo2'])
def test_logit_y_breaks_linear_delta_cancellation_and_origin_invariance(which, model1_result, model2_result):
    contract = read_model_contract(model1_result.stress if which == 'modelo1' else model2_result.export, which)
    params = pd.Series(0., index=contract.terms)
    params['const'], params['y_lag'] = .1, .5
    gdp = 'gdp_growth' if which == 'modelo1' else 'gdp_l1'
    params[gdp] = .1
    index = pd.period_range('2026Q3', periods=13, freq='Q-DEC')
    b = pd.DataFrame(0., index=index, columns=contract.terms); b['const'] = 1.
    a = b.copy(); a[gdp] = 1.
    expected = delta_recursion(params, b, a)
    nonlinear_deltas = []
    for anchor in [-2., -1.]:
        base = project(contract, params, b, anchor, .1, []).dr.to_numpy()
        adv = project(contract, params, a, anchor, .1, []).dr.to_numpy()
        np.testing.assert_allclose(adv-base, expected, atol=1e-12, rtol=0)
        # Counterexample only: back-transform a hypothetical logit Y, never production.
        nonlinear = 100/(1+np.exp(-adv)) - 100/(1+np.exp(-base))
        assert not np.allclose(nonlinear, expected, atol=1e-12, rtol=0)
        nonlinear_deltas.append(nonlinear)
    assert not np.allclose(*nonlinear_deltas, atol=1e-12, rtol=0)


def test_rate_contribution_uses_paired_difference_and_sensitivity_peak():
    from src.stress import rate_sensitivity
    index=pd.period_range('2026Q3',periods=3,freq='Q-DEC')
    principal=pd.DataFrame({'delta':[1.,3.,2.]},index=index)
    sensitivity=pd.DataFrame({'delta':[2.,4.,5.]},index=index)
    a=np.array([[1.,3.,2.],[1.,3.,2.]])
    b=np.array([[2.,5.,6.],[3.,4.,4.]])
    result=rate_sensitivity(principal,sensitivity,a,b)
    assert result.c.tolist()==[1.,1.,3.]
    assert result.attrs['pico_trimestre']=='2027T1'
    assert result.attrs['c_pico']==3.
    assert result.attrs['c_final_p05']==pytest.approx(2.1)


def test_origin_comparison_checks_complete_stepwise_delta_not_calendar_alignment():
    from src.stress import origin_comparison
    ia=pd.period_range('2026Q3',periods=13,freq='Q-DEC')
    ib=pd.period_range('2026Q1',periods=13,freq='Q-DEC')
    a={'base':pd.DataFrame({'dr':np.arange(13)+2.},index=ia),
       'severo':pd.DataFrame({'dr':np.arange(13)+3.},index=ia)}
    b={'base':pd.DataFrame({'dr':np.arange(13)+5.},index=ib),
       'severo':pd.DataFrame({'dr':np.arange(13)+6.},index=ib)}
    result=origin_comparison(a,b)
    assert len(result)==26
    assert result.iloc[-1].trimestre_original=='2029T1'
    assert result.iloc[-1].trimestre_adaptado=='2029T3'
    b['severo'].iloc[0,0]+=.01
    with pytest.raises(ValueError,match='RF-12c'):
        origin_comparison(a,b)


def test_d_equals_severe_under_zero_rate_but_differs_with_point_rate(model1_result):
    contract,params,X=simple_projection_inputs(model1_result)
    params.d_ffr=.2
    D=X.copy(); D.d_ffr=1.
    a=project(contract,params,X,2,.1,list(contract.zero_terms))
    b=project(contract,params,D,2,.1,list(contract.zero_terms))
    pd.testing.assert_frame_equal(a,b)
    assert not np.allclose(project(contract,params,D,2,.1,[]).dr,a.dr)
