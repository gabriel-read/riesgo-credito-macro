"""Contract tests for stress scenarios, spec 005; synthetic data, no network."""

import hashlib
import io

import pandas as pd
import pytest

from src.scenarios import FED_COLUMNS, FedFileSpec, parse_fed_csv
from src.pipeline import load_fed_sources


def synthetic_adapted():
    quarters = pd.period_range("2026Q3", "2029Q3", freq="Q-DEC")
    result = pd.DataFrame({"Real GDP growth": 4.0, "CPI inflation rate": 8.0,
                           "Unemployment rate": 5.0, "3-month Treasury rate": 2.0}, index=quarters)
    result.attrs["reference"] = pd.Series({"Unemployment rate": 4.5, "3-month Treasury rate": 3.7})
    return result


def test_levels_compound_exactly_yoy_uses_logs_and_origin_own_changes():
    from src.scenarios import to_levels
    observed = pd.Series(100.0, index=pd.period_range("2025Q1", "2026Q2", freq="Q-DEC"))
    result = to_levels(synthetic_adapted(), observed, observed, 4.0, 3.5)
    assert result.loc["2026Q3", "gdpc1"] == pytest.approx(100 * 1.04**0.25)
    assert result.loc["2026Q3", "gdp_growth"] == pytest.approx(25 * __import__("numpy").log(1.04))
    assert result.loc["2027Q2", "inflation"] == pytest.approx(100 * __import__("numpy").log(1.08))
    assert result.loc["2026Q3", "d_unemp"] == pytest.approx(0.5)
    assert result.loc["2026Q3", "d_ffr"] == pytest.approx(-1.7)
    assert result.loc["2026Q3", "unrate"] == pytest.approx(4.5)
    assert result.loc["2026Q3", "fedfunds"] == pytest.approx(1.8)


@pytest.mark.parametrize("kind", ["bad_rate", "missing_history", "nonpositive"])
def test_levels_fail_required_inputs_without_imputation(kind):
    from src.scenarios import to_levels
    observed = pd.Series(100.0, index=pd.period_range("2025Q1", "2026Q2", freq="Q-DEC"))
    adapted = synthetic_adapted()
    if kind == "bad_rate":
        adapted.loc["2026Q3", "CPI inflation rate"] = -100
    elif kind == "missing_history":
        observed = observed.drop(pd.Period("2025Q3"))
    else:
        observed.loc["2026Q2"] = 0
    with pytest.raises(ValueError):
        to_levels(adapted, observed, observed, 4, 3.5)


def test_levels_observed_future_does_not_enter_projection():
    from src.scenarios import to_levels
    observed = pd.Series(100.0, index=pd.period_range("2025Q1", "2026Q3", freq="Q-DEC"))
    a = to_levels(synthetic_adapted(), observed, observed, 4, 3.5)
    observed.loc["2026Q3"] = 10000
    b = to_levels(synthetic_adapted(), observed, observed, 4, 3.5)
    pd.testing.assert_frame_equal(a, b)


def test_regressor_credit_is_observed_at_lag_four_then_fixed_common():
    from src.scenarios import build_regressors, to_levels
    index = pd.period_range('2025Q1', '2026Q2', freq='Q-DEC')
    observed = pd.Series(100.0, index=index)
    panel = pd.DataFrame({'loans_yoy': range(len(index))}, index=index)
    levels = to_levels(synthetic_adapted(), observed, observed, 4, 3.5)
    regs = build_regressors(levels, panel, credit_rule='last')
    assert regs.loc['2026Q3', 'credit_growth'] == panel.loc['2025Q3', 'loans_yoy']
    assert regs.loc['2027Q2', 'credit_growth'] == panel.loc['2026Q2', 'loans_yoy']
    assert regs.loc['2027Q3', 'credit_growth'] == panel.loc['2026Q2', 'loans_yoy']
    assert regs['credit_observed'].sum() == 4
    with pytest.raises(ValueError, match='crédito'):
        build_regressors(levels, panel.drop(pd.Period('2025Q3')), credit_rule='last')


def test_frozen_history_levels_use_approved_aggregation_and_vintage(tmp_path):
    from pathlib import Path
    import shutil
    from src.pipeline import load_stress_history
    from src.panel import parse_raw, quarterly_from_monthly
    history = load_stress_history(Path('.'), pd.Period('2026Q2'))
    raw = pd.read_csv('data/raw/CPIAUCSL_2026-10-02.csv', dtype=str, keep_default_na=False)
    cpi, _, treatment = quarterly_from_monthly(parse_raw(raw, 'CPIAUCSL'), 'CPIAUCSL')
    assert treatment == 'RF-11'
    assert history['cpiaucsl'].loc['2025Q4'] == cpi.loc['2025Q4']
    assert history['gdpc1'].index[-1] == pd.Period('2026Q2')
    assert history['full'].index[-1] == pd.Period('2026Q2')
    shutil.copytree('data/raw', tmp_path / 'data/raw')
    manifest = pd.read_csv(tmp_path / 'data/raw/manifest.csv')
    manifest.loc[manifest.series.eq('GDPC1'), 'download_date'] = '2026-10-03'
    manifest.to_csv(tmp_path / 'data/raw/manifest.csv', index=False)
    with pytest.raises(ValueError, match='vintage'):
        load_stress_history(tmp_path, pd.Period('2026Q2'))


def fed_text(scenario="Supervisory Baseline", historical=False):
    quarters = ([pd.Period("2025Q4")] if historical else
                pd.period_range("2026Q1", "2029Q1", freq="Q-DEC"))
    rows = [{**dict.fromkeys(FED_COLUMNS, "1.0"), "Scenario Name": scenario,
             "Date": f"{q.year} Q{q.quarter}"} for q in quarters]
    return pd.DataFrame(rows, columns=FED_COLUMNS).to_csv(index=False)


def test_parser_returns_numeric_quarterly_scenario():
    result = parse_fed_csv(fed_text(), FedFileSpec("base.csv", "Supervisory Baseline"))
    assert result.index.equals(pd.period_range("2026Q1", "2029Q1", freq="Q-DEC"))
    assert result.loc["2026Q1", "Real GDP growth"] == 1.0


@pytest.mark.parametrize("mutation,match", [
    (lambda s: s.replace("Real GDP growth", "wrong"), "Real GDP growth"),
    (lambda s: s.replace("Supervisory Baseline", "wrong"), "escenario"),
    (lambda s: s.replace("2026 Q2", "2026 Q1"), "trimestre"),
    (lambda s: s.replace("2026 Q2", "2026 Q0"), "trimestre"),
    (lambda s: "\n".join(s.splitlines()[:-1]), "2029Q1"),
    (lambda s: s.replace("2026 Q1,1.0", "2026 Q1,"), "Real GDP growth.*2026Q1"),
    (lambda s: s.replace("2026 Q1,1.0", "2026 Q1,inf"), "Real GDP growth.*2026Q1"),
])
def test_parser_rejects_malformed_sources(mutation, match):
    with pytest.raises(ValueError, match=match):
        parse_fed_csv(mutation(fed_text()), FedFileSpec("base.csv", "Supervisory Baseline"))


def test_historic_requires_origin_and_allows_unused_missing_fields():
    text = fed_text("Actual", True)
    result = parse_fed_csv(text, FedFileSpec("hist.csv", "Actual", historical=True))
    assert result.index[-1] == pd.Period("2025Q4")
    with pytest.raises(ValueError, match="2025Q4"):
        parse_fed_csv(text.replace("2025 Q4", "2025 Q3"),
                      FedFileSpec("hist.csv", "Actual", historical=True))


def write_sources(root):
    rows = []
    for filename, scenario, hist in [
        ("2026_Final_Historic_Domestic.csv", "Actual", True),
        ("2026_Final_Supervisory_Baseline_Domestic.csv", "Supervisory Baseline", False),
        ("2026_Final_Supervisory_Severely_Adverse_Domestic.csv", "Supervisory Severely Adverse", False),
    ]:
        raw = fed_text(scenario, hist).replace("\n", "\r\n").encode()
        (root / filename).write_bytes(raw)
        rows.append({"file": filename, "scenario": scenario, "version": "2026 Final",
                     "url": "https://www.federalreserve.gov/supervisionreg/files/" + filename,
                     "download_date": "2026-10-11", "sha256": hashlib.sha256(raw).hexdigest()})
    pd.DataFrame(rows).to_csv(root / "manifest.csv", index=False, encoding="utf-8-sig")


def test_sources_verify_original_bytes_bom_manifest_and_do_not_write(tmp_path):
    write_sources(tmp_path)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    result = load_fed_sources(tmp_path)
    assert set(result) == {"base", "severo", "historico"}
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    path = tmp_path / "2026_Final_Supervisory_Baseline_Domestic.csv"
    path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    with pytest.raises(ValueError, match="sha256"):
        load_fed_sources(tmp_path)


def test_sources_fail_missing_manifest_entry_and_path_traversal(tmp_path):
    write_sources(tmp_path)
    manifest = pd.read_csv(tmp_path / "manifest.csv")
    manifest.loc[0, "file"] = "../other.csv"
    manifest.to_csv(tmp_path / "manifest.csv", index=False)
    with pytest.raises(ValueError, match="manifiesto"):
        load_fed_sources(tmp_path)


@pytest.mark.parametrize('mode,origin,start,end,n', [
    ('adapted','2026Q2','2026Q3','2029Q3',13),
    ('post_2026q2','2026Q2','2026Q3','2029Q1',11),
    ('from_2025q4','2025Q4','2026Q1','2029Q1',13),
])
def test_calendar_modes_cover_required_steps_and_keep_correct_reference(mode,origin,start,end,n):
    from src.scenarios import adapt_calendar
    fed = parse_fed_csv(fed_text(), FedFileSpec('base.csv','Supervisory Baseline'))
    historical = pd.Series({'Unemployment rate':4.5,'3-month Treasury rate':3.7})
    adapted = adapt_calendar(fed, historical, pd.Period(origin), mode)
    assert len(adapted) == n
    assert str(adapted.index[0]) == start and str(adapted.index[-1]) == end
    reference = fed.loc['2026Q2'] if mode == 'post_2026q2' else historical
    assert adapted.attrs['reference']['Unemployment rate'] == reference['Unemployment rate']
    assert str(adapted['fed_quarter'].iloc[0]) == ('2026Q3' if mode == 'post_2026q2' else '2026Q1')


def test_d_changes_only_rate_seven_steps_then_six_zeros():
    from src.scenarios import scenario_d
    regs = pd.DataFrame({'gdp_growth':1.,'inflation':2.,'d_unemp':.1,'d_ffr':-.2,
                         'credit_growth':3.},index=pd.period_range('2026Q3','2029Q3',freq='Q-DEC'))
    panel = pd.DataFrame({'fedfunds_d':[.1,.2,.3,.4,.5,.6,.7]},
                         index=pd.period_range('2022Q1','2023Q3',freq='Q-DEC'))
    own = scenario_d(regs,panel)
    pd.testing.assert_frame_equal(own.drop(columns='d_ffr'),regs.drop(columns='d_ffr'))
    assert own.d_ffr.tolist() == [.1,.2,.3,.4,.5,.6,.7,0,0,0,0,0,0]
    with pytest.raises(ValueError,match='D'):
        scenario_d(regs,panel.drop(pd.Period('2022Q3')))


def test_original_origin_credit_uses_fixed_observed_cutoff_not_early_anchor():
    from src.scenarios import build_regressors
    panel = pd.DataFrame({'loans_yoy':range(106)},index=pd.period_range('2000Q1','2026Q2',freq='Q-DEC'))
    levels = pd.DataFrame(1.,columns=['gdp_growth','d_unemp','inflation','d_ffr'],
                          index=pd.period_range('2026Q1','2029Q1',freq='Q-DEC'))
    last = build_regressors(levels,panel,credit_rule='last')
    zero = build_regressors(levels,panel,credit_rule='zero')
    mean = build_regressors(levels,panel,credit_rule='mean')
    assert last.credit_observed.sum() == 6
    assert last.loc['2027Q3','credit_growth'] == 105
    assert zero.loc['2027Q3','credit_growth'] == 0
    assert mean.loc['2027Q3','credit_growth'] == pytest.approx(52.5)
    warmup=pd.DataFrame({'loans_yoy':[float('nan')]*4},index=pd.period_range('1998Q1',periods=4,freq='Q-DEC'))
    pd.testing.assert_frame_equal(build_regressors(levels,pd.concat([warmup,panel]),credit_rule='last'),last)
