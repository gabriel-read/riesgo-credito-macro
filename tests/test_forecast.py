"""Tests para src/forecast.py (spec 003, tarea 4).

Cubre RF-18 y RNF-3 según plan §7: pronóstico a un paso y dinámico, reconstrucción
del nivel, ingenuo, RMSE/MAE, Diebold-Mariano con corrección HLN y veredictos.
Datos sintéticos con resultado conocido; semillas independientes entre X y el
ruido de y (con la misma semilla, el ruido coincidiría con una columna de X);
sin red ni disco.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from src.design import Design
from src.estimation import fit_ols_hac
from src.forecast import (
    diebold_mariano_hln,
    dynamic,
    mae,
    naive,
    one_step,
    oos_verdicts,
    rmse,
    to_level,
)
from src.model1_config import SEED


def _q(start: str, periods: int) -> pd.PeriodIndex:
    return pd.period_range(start, periods=periods, freq="Q-DEC")


# --- one_step ---


def test_one_step_uses_observed_y_lag():
    params = pd.Series({"const": 1.0, "y_lag": 0.5, "x": 2.0})
    X_test = pd.DataFrame(
        {"const": [1.0, 1.0, 1.0], "y_lag": [4.0, -1.0, 0.0], "x": [0.5, 1.0, -2.0]},
        index=_q("2022Q1", 3),
    )
    pred = one_step(params, X_test)
    # 1 + 0,5·4 + 2·0,5 = 4 ; 1 − 0,5 + 2 = 2,5 ; 1 + 0 − 4 = −3
    np.testing.assert_allclose(pred.to_numpy(), [4.0, 2.5, -3.0], rtol=1e-12)
    assert pred.index.equals(X_test.index)


def test_one_step_orders_columns_like_params():
    params = pd.Series({"const": 1.0, "y_lag": 0.5, "x": 2.0})
    X_test = pd.DataFrame(
        {"x": [0.5], "y_lag": [4.0], "const": [1.0]}, index=_q("2022Q1", 1)
    )
    assert one_step(params, X_test).iloc[0] == pytest.approx(4.0)


def test_one_step_missing_column_raises():
    params = pd.Series({"const": 1.0, "y_lag": 0.5, "x": 2.0})
    X_test = pd.DataFrame({"const": [1.0], "x": [0.5]}, index=_q("2022Q1", 1))
    with pytest.raises(ValueError, match="y_lag"):
        one_step(params, X_test)


# --- dynamic ---


def test_dynamic_chains_forecast_into_y_lag():
    params = pd.Series({"const": 1.0, "y_lag": 0.5, "x": 2.0})
    # y_lag observado en X_test (basura a propósito): el dinámico no debe usarlo
    X_test = pd.DataFrame(
        {"const": [1.0, 1.0, 1.0], "y_lag": [99.0, 99.0, 99.0], "x": [0.5, 1.0, -2.0]},
        index=_q("2022Q1", 3),
    )
    pred = dynamic(params, X_test, y_anchor=4.0)
    # t1: 1 + 0,5·4 + 1 = 4 ; t2: 1 + 0,5·4 + 2 = 5 ; t3: 1 + 0,5·5 − 4 = −0,5
    np.testing.assert_allclose(pred.to_numpy(), [4.0, 5.0, -0.5], rtol=1e-12)
    assert pred.index.equals(X_test.index)


def test_dynamic_first_step_equals_one_step_with_anchor():
    params = pd.Series({"const": 0.3, "y_lag": 0.7, "x": -1.0})
    X_test = pd.DataFrame(
        {"const": [1.0, 1.0], "y_lag": [2.5, 0.0], "x": [0.2, 0.4]}, index=_q("2022Q1", 2)
    )
    one = one_step(params, X_test.assign(y_lag=[1.5, 0.0]))
    dyn = dynamic(params, X_test, y_anchor=1.5)
    assert dyn.iloc[0] == pytest.approx(one.iloc[0])


def test_dynamic_requires_y_lag_in_params():
    params = pd.Series({"const": 1.0, "x": 2.0})
    X_test = pd.DataFrame({"const": [1.0], "x": [0.5]}, index=_q("2022Q1", 1))
    with pytest.raises(ValueError, match="y_lag"):
        dynamic(params, X_test, y_anchor=1.0)


# --- to_level y naive ---


@pytest.fixture
def level_obs() -> pd.Series:
    return pd.Series([1.0, 1.2, 1.5, 1.4], index=_q("2021Q4", 4), name="dr")


def test_to_level_one_step_adds_delta_to_previous_observed_level(level_obs):
    pred = pd.Series([0.1, 0.2, -0.1], index=_q("2022Q1", 3))
    out = to_level(pred, "primera diferencia", level_obs, pd.Period("2021Q4", "Q-DEC"), "one_step")
    # 1,0 + 0,1 ; 1,2 + 0,2 ; 1,5 − 0,1
    np.testing.assert_allclose(out.to_numpy(), [1.1, 1.4, 1.4], rtol=1e-12)


def test_to_level_dynamic_accumulates_from_anchor(level_obs):
    pred = pd.Series([0.1, 0.2, -0.1], index=_q("2022Q1", 3))
    out = to_level(pred, "primera diferencia", level_obs, pd.Period("2021Q4", "Q-DEC"), "dynamic")
    # 1,0 + cumsum([0,1; 0,2; −0,1]) = 1,1 ; 1,3 ; 1,2
    np.testing.assert_allclose(out.to_numpy(), [1.1, 1.3, 1.2], rtol=1e-12)


@pytest.mark.parametrize("mode", ["one_step", "dynamic"])
def test_to_level_level_form_returns_prediction_unchanged(level_obs, mode):
    pred = pd.Series([1.1, 1.3, 1.2], index=_q("2022Q1", 3))
    out = to_level(pred, "nivel", level_obs, pd.Period("2021Q4", "Q-DEC"), mode)
    np.testing.assert_allclose(out.to_numpy(), pred.to_numpy())


def test_to_level_rejects_unknown_mode_and_form(level_obs):
    pred = pd.Series([0.1], index=_q("2022Q1", 1))
    anchor = pd.Period("2021Q4", "Q-DEC")
    with pytest.raises(ValueError, match="modo"):
        to_level(pred, "primera diferencia", level_obs, anchor, "otro")
    with pytest.raises(ValueError, match="forma"):
        to_level(pred, "logit", level_obs, anchor, "one_step")


def test_naive_one_step_is_previous_observed_level(level_obs):
    idx = _q("2022Q1", 3)
    out = naive(level_obs, idx, pd.Period("2021Q4", "Q-DEC"), "one_step")
    np.testing.assert_allclose(out.to_numpy(), [1.0, 1.2, 1.5])
    assert out.index.equals(idx)


def test_naive_dynamic_is_constant_anchor_level(level_obs):
    idx = _q("2022Q1", 3)
    out = naive(level_obs, idx, pd.Period("2021Q4", "Q-DEC"), "dynamic")
    np.testing.assert_allclose(out.to_numpy(), [1.0, 1.0, 1.0])
    assert out.index.equals(idx)


def test_naive_rejects_unknown_mode(level_obs):
    with pytest.raises(ValueError, match="modo"):
        naive(level_obs, _q("2022Q1", 1), pd.Period("2021Q4", "Q-DEC"), "otro")


# --- rmse y mae ---


def test_rmse_and_mae_of_known_errors():
    e = pd.Series([3.0, -4.0, 0.0])
    assert rmse(e) == pytest.approx(np.sqrt(25.0 / 3.0))
    assert mae(e) == pytest.approx(7.0 / 3.0)


def test_rmse_of_constant_error_equals_its_absolute_value():
    e = np.full(7, -0.25)
    assert rmse(e) == pytest.approx(0.25)
    assert mae(e) == pytest.approx(0.25)


# --- Diebold-Mariano con corrección HLN ---


def test_diebold_mariano_hln_matches_hand_calculation_n5():
    """n = 5 calculado a mano.

    e_modelo = [1, 2, 0, 1, 2]; e_ingenuo = [2, 1, 1, 2, 1]
    d = e_m² − e_n² = [−3, 3, −1, −3, 3]; d̄ = −0,2
    γ̂0 = Σ(d − d̄)²/n = 36,8/5 = 7,36 (divisor n); error estándar = √(7,36/5)
    DM = −0,2/√1,472 = −0,164845
    HLN: factor √((n + 1 − 2h + h(h−1)/n)/n) = √(4/5) → DM* = −0,147442
    p bilateral con t(4).
    """
    e_m = pd.Series([1.0, 2.0, 0.0, 1.0, 2.0])
    e_n = pd.Series([2.0, 1.0, 1.0, 2.0, 1.0])
    out = diebold_mariano_hln(e_m, e_n, h=1)
    assert out["n"] == 5
    assert out["dm"] == pytest.approx(-0.1648451183, abs=1e-9)
    assert out["stat"] == pytest.approx(-0.1474419562, abs=1e-9)
    assert out["p"] == pytest.approx(2 * stats.t.sf(0.1474419562, 4), abs=1e-9)
    assert out["p"] == pytest.approx(0.8899165133, abs=1e-8)


def test_diebold_mariano_sign_negative_when_model_loses_less():
    e_m = pd.Series([0.1, -0.2, 0.1, 0.0, 0.2, -0.1])
    e_n = pd.Series([1.0, -1.1, 0.9, 1.2, -1.0, 0.8])
    out = diebold_mariano_hln(e_m, e_n)
    assert out["stat"] < 0
    assert out["p"] < 0.05


def test_diebold_mariano_is_symmetric_in_p_when_swapping_models():
    e_m = pd.Series([1.0, 2.0, 0.0, 1.0, 2.0])
    e_n = pd.Series([2.0, 1.0, 1.0, 2.0, 1.0])
    a = diebold_mariano_hln(e_m, e_n)
    b = diebold_mariano_hln(e_n, e_m)
    assert a["stat"] == pytest.approx(-b["stat"])
    assert a["p"] == pytest.approx(b["p"])


def test_diebold_mariano_identical_errors_gives_nan():
    e = pd.Series([1.0, -2.0, 0.5, 1.5])
    out = diebold_mariano_hln(e, e)
    assert np.isnan(out["stat"]) and np.isnan(out["p"])


def test_diebold_mariano_needs_at_least_two_observations():
    with pytest.raises(ValueError, match="observaciones"):
        diebold_mariano_hln(pd.Series([1.0]), pd.Series([2.0]))


def test_diebold_mariano_rejects_mismatched_lengths():
    with pytest.raises(ValueError, match="longitud"):
        diebold_mariano_hln(pd.Series([1.0, 2.0, 3.0]), pd.Series([1.0, 2.0]))


# --- oos_verdicts ---


@pytest.mark.parametrize(
    "ratio_one, ratio_dyn, dm_p, esperado",
    [
        (0.80, 0.90, 0.01, ("supera al ingenuo", "supera al ingenuo", "significativo")),
        (1.20, 1.50, 0.20, ("no supera al ingenuo", "no supera al ingenuo", "no significativo")),
        (0.95, 1.10, 0.04, ("supera al ingenuo", "no supera al ingenuo", "significativo")),
        (1.00, 0.99, 0.05, ("no supera al ingenuo", "supera al ingenuo", "no significativo")),
    ],
)
def test_oos_verdicts_four_cases(ratio_one, ratio_dyn, dm_p, esperado):
    out = oos_verdicts(ratio_one, ratio_dyn, dm_p)
    assert out["veredicto_un_paso"] == esperado[0]
    assert out["veredicto_dinamico"] == esperado[1]
    assert out["significancia_un_paso"] == esperado[2]


def test_oos_verdicts_nan_p_is_not_significant():
    out = oos_verdicts(0.5, 0.5, float("nan"))
    assert out["significancia_un_paso"] == "no significativo"


# --- Integración con un DGP simulado (X y ruido con semillas independientes) ---


def _simulate(n: int, sigma: float = 0.5):
    rng_x = np.random.default_rng(SEED)
    rng_e = np.random.default_rng(SEED + 1)  # independiente de X
    x = rng_x.normal(0.0, 1.0, n)
    e = rng_e.normal(0.0, sigma, n)
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = 0.3 + 0.6 * y[t - 1] + 1.5 * x[t] + e[t]
    idx = _q("2000Q1", n)
    X = pd.DataFrame(
        {"const": 1.0, "y_lag": np.r_[0.0, y[:-1]], "x": x}, index=idx
    ).iloc[1:]
    return pd.Series(y[1:], index=X.index, name="y"), X, e[1:]


def test_one_step_forecast_error_matches_noise_in_simulated_dgp():
    n_train, n_test, sigma = 600, 200, 0.5
    y, X, _ = _simulate(n_train + n_test, sigma)
    train = Design(
        y=y.iloc[:n_train], X=X.iloc[:n_train], form="nivel",
        start=y.index[0], end=y.index[n_train - 1], spec_id="sim",
    )
    fit = fit_ols_hac(train)
    assert fit.rsquared < 0.999  # guarda contra ajuste degenerado
    X_test, y_test = X.iloc[n_train:], y.iloc[n_train:]
    err = y_test - one_step(fit.params, X_test)
    assert rmse(err) == pytest.approx(sigma, abs=0.08)
    # el pronóstico dinámico acumula error: nunca mejor que ~el a un paso
    anchor = float(y.iloc[n_train - 1])
    dyn = dynamic(fit.params, X_test, y_anchor=anchor)
    assert rmse(y_test - dyn) > rmse(err)


def test_model_beats_random_walk_with_dm_in_simulated_dgp():
    n_train, n_test = 300, 80
    y, X, _ = _simulate(n_train + n_test, sigma=0.4)
    train = Design(
        y=y.iloc[:n_train], X=X.iloc[:n_train], form="nivel",
        start=y.index[0], end=y.index[n_train - 1], spec_id="sim",
    )
    fit = fit_ols_hac(train)
    X_test, y_test = X.iloc[n_train:], y.iloc[n_train:]
    e_model = y_test - one_step(fit.params, X_test)
    e_naive = y_test - y_test.shift(1).fillna(float(y.iloc[n_train - 1]))
    ratio = rmse(e_model) / rmse(e_naive)
    dm = diebold_mariano_hln(e_model, e_naive)
    assert ratio < 1.0
    assert dm["stat"] < 0 and dm["p"] < 0.05
    verd = oos_verdicts(ratio, ratio, dm["p"])
    assert verd["veredicto_un_paso"] == "supera al ingenuo"
    assert verd["significancia_un_paso"] == "significativo"
