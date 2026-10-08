"""Tests de src/design2.py y de src/model2_config.py (spec 004, tarea 1).

Cubre RF-1 a RF-4, RF-14 y RF-15 (diseño de las proyecciones), RF-22 a RF-24 (diseño de las
variantes), RF-25 (rezagos que salen de trimestres excluidos) y RNF-2/RNF-7. Datos sintéticos;
sin red ni disco y sin ningún dato real del Modelo II.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.design import ModelDataError
from src.design2 import (
    build_columns,
    build_design2,
    build_lp_design,
    common_window,
    covid_lag_leaks,
    lagged_from_excluded,
    zero_rate_quarters,
)
from src.model2_config import (
    CONTROLS,
    EXPECTED_FORM,
    H_MAX,
    K_MAX,
    K_RANGE,
    MAIN2,
    PEAK_TIE_TOL,
    ROBUST2,
    ZERO_RATE_MAX,
    Spec2,
)
from tests.synthetic_model2 import END, make_full2, with_zero_rate

DEC = EXPECTED_FORM
P = lambda s: pd.Period(s, "Q-DEC")  # noqa: E731
COVID_NAMES = ["covid_2020q2", "covid_2020q3", "covid_2020q4", "covid_2021q1"]


@pytest.fixture(scope="module")
def full():
    return make_full2()


@pytest.fixture(scope="module")
def window(full):
    return common_window(build_columns(full, DEC), END)


# --- Configuración ---


def test_config_constants():
    assert K_MAX == 8 and K_RANGE == tuple(range(1, 9)) and H_MAX == 12
    assert ZERO_RATE_MAX == 0.25
    assert PEAK_TIE_TOL == 1e-12
    assert EXPECTED_FORM == "ambigua (primera diferencia)"
    assert CONTROLS == {"gdp_l1": ("gdpc1_yoy", 1), "d_unemp_l1": ("unrate_d", 1),
                        "inflation_l1": ("cpiaucsl_yoy", 1), "credit_l4": ("loans_yoy", 4)}


def test_specs():
    assert MAIN2.id == "main" and MAIN2.k_source == "bic" and MAIN2.covid_dummies
    r1, r2, r3 = ROBUST2
    assert (r1.id, r1.k_source, r1.covid_dummies) == ("R1", "aic", True)
    assert (r2.id, r2.exclude_range, r2.covid_dummies) == ("R2", ("2020Q1", "2021Q4"), False)
    assert (r3.id, r3.exclude_zero_rate, r3.covid_dummies) == ("R3", True, False)


# --- build_columns y muestra común (RF-1, RF-3) ---


def test_build_columns(full):
    cols = build_columns(full, DEC)
    assert len(cols) == len(full)                     # sin dropna
    assert np.allclose(cols["y"].iloc[1:], full["dralacbs"].diff().iloc[1:])
    assert np.allclose(cols["y_lag"].iloc[2:], cols["y"].shift(1).iloc[2:])
    for j in range(9):
        assert f"d_ffr_l{j}" in cols
    assert cols["d_ffr_l3"].equals(full["fedfunds_d"].shift(3))
    assert cols["gdp_l1"].equals(full["gdpc1_yoy"].shift(1))
    assert cols["d_unemp_l1"].equals(full["unrate_d"].shift(1))
    assert cols["inflation_l1"].equals(full["cpiaucsl_yoy"].shift(1))
    assert cols["credit_l4"].equals(full["loans_yoy"].shift(4))


def test_build_columns_reindexes_without_gaps(full):
    holed = full.drop(index=[P("2010Q1")])
    cols = build_columns(holed, DEC)
    assert len(cols) == len(full)                     # el hueco reaparece como fila con NaN
    assert np.isnan(cols.loc[P("2010Q2"), "d_ffr_l1"])   # t−1 es 2010T1, que falta (no 2009T4)
    assert np.isnan(cols.loc[P("2010Q1"), "y"])


def test_common_window_starts_2000q2(window):
    assert window == (P("2000Q2"), END)


def test_common_window_does_not_drop_inner_nan(full):
    holed = full.copy()
    holed.loc[P("2010Q1"), "gdpc1_yoy"] = np.nan
    assert common_window(build_columns(holed, DEC), END) == (P("2000Q2"), END)


# --- Muestra y tasa cero ---


def test_zero_rate_quarters_inclusive_threshold(full):
    f = with_zero_rate(full, [("2009Q1", "2009Q4")], level=0.10)
    f.loc[P("2009Q2"), "fedfunds"] = 0.25            # el umbral es inclusivo
    f.loc[P("2009Q3"), "fedfunds"] = 0.26            # justo por encima: no cuenta
    got = zero_rate_quarters(f, P("2000Q2"), END)
    assert P("2009Q1") in got and P("2009Q2") in got and P("2009Q4") in got
    assert P("2009Q3") not in got
    assert got == sorted(got)


def test_zero_rate_quarters_respects_range(full):
    f = with_zero_rate(full, [("2009Q1", "2015Q4"), ("2020Q2", "2021Q1")])
    assert len(zero_rate_quarters(f, P("2000Q2"), END)) == 28 + 4
    assert len(zero_rate_quarters(f, P("2012Q1"), P("2013Q4"))) == 8


# --- build_design2 (RF-1, RF-4, RF-22, RF-23) ---


def test_design_main_columns_and_dummies(full, window):
    d = build_design2(full, MAIN2, 3, DEC, window, END)
    assert list(d.X.columns) == (["const", "y_lag"] + [f"d_ffr_l{j}" for j in range(4)]
                                 + ["gdp_l1", "d_unemp_l1", "inflation_l1", "credit_l4"] + COVID_NAMES)
    assert d.X.shape == (105, 3 + 11)                  # K + 11 parámetros
    assert len(d.y) == 105 and d.start == P("2000Q2") and d.end == END and d.spec_id == "main"
    assert d.form == "primera diferencia" and d.dropped == []
    for name, q in zip(COVID_NAMES, ["2020Q2", "2020Q3", "2020Q4", "2021Q1"]):
        assert d.X[name].sum() == 1.0 and d.X.loc[P(q), name] == 1.0


def test_design_is_independent_of_k_through_window(full, window):
    d1 = build_design2(full, MAIN2, 1, DEC, window, END)
    d8 = build_design2(full, MAIN2, 8, DEC, window, END)
    assert d1.y.index.equals(d8.y.index) and d1.y.equals(d8.y)


def test_design_nan_raises_with_variable_quarter_and_regression(full, window):
    holed = full.copy()
    holed.loc[P("2010Q1"), "gdpc1_yoy"] = np.nan      # afecta gdp_l1 en 2010T2
    with pytest.raises(ModelDataError) as e:
        build_design2(holed, MAIN2, 3, DEC, window, END)
    msg = str(e.value)
    assert "gdp_l1" in msg and "2010Q2" in msg and "main" in msg


def test_design_missing_row_is_not_silently_dropped(full, window):
    holed = full.drop(index=[P("2010Q1")])
    with pytest.raises(ModelDataError) as e:
        build_design2(holed, MAIN2, 3, DEC, window, END)
    assert "2010Q1" in str(e.value)


def test_r2_excludes_covid_range_and_omits_dummies(full, window):
    r2 = ROBUST2[1]
    d = build_design2(full, r2, 3, DEC, window, END)
    assert len(d.y) == 105 - 8
    assert not any(q in d.y.index for q in pd.period_range("2020Q1", "2021Q4", freq="Q-DEC"))
    assert not any(c.startswith("covid_") for c in d.X.columns)
    assert d.dropped == COVID_NAMES and d.X.shape[1] == 3 + 7     # K + 7 sin dummies
    assert d.spec_id == "R2"


def test_r3_excludes_zero_rate_quarters(full, window):
    f = with_zero_rate(full, [("2009Q1", "2015Q4"), ("2020Q2", "2021Q1")])
    zr = zero_rate_quarters(f, window[0], window[1])
    d = build_design2(f, ROBUST2[2], 2, DEC, window, END)
    assert len(d.y) == 105 - len(zr) and len(zr) == 32
    assert not any(q in d.y.index for q in zr)
    assert d.dropped == COVID_NAMES and not any(c.startswith("covid_") for c in d.X.columns)


def test_dummy_without_variation_is_error_outside_r2_r3(full):
    early = (P("2000Q2"), P("2019Q4"))
    for spec in (MAIN2, ROBUST2[0]):
        with pytest.raises(ModelDataError) as e:
            build_design2(full, spec, 3, DEC, early, END)
        assert "covid_2020q2" in str(e.value) and spec.id in str(e.value)


def test_custom_spec_without_dummies_is_allowed(full, window):
    d = build_design2(full, Spec2("X", "sin dummies", covid_dummies=False), 3, DEC, window, END)
    assert d.dropped == COVID_NAMES


# --- Rezagos que salen de trimestres excluidos (RF-24, RF-25) ---


def test_lagged_from_excluded_hand_case(full, window):
    d = build_design2(full, MAIN2, 2, DEC, window, END)
    got = lagged_from_excluded(d, 2, {P("2020Q2")})
    # y_lag y ΔFFR(t−1), gdp, unemp, inflación: 2020T3; ΔFFR(t−2): 2020T4; CRED(t−4): 2021T2
    assert got == [P("2020Q3"), P("2020Q4"), P("2021Q2")]


def test_lagged_from_excluded_terms_filter(full, window):
    d = build_design2(full, MAIN2, 2, DEC, window, END)
    assert lagged_from_excluded(d, 2, {P("2020Q2")}, terms=("credit_l4",)) == [P("2021Q2")]
    assert lagged_from_excluded(d, 2, {P("2020Q2")}, terms=("d_ffr_l2",)) == [P("2020Q4")]


def test_covid_lag_leaks_only_counts_y_lag_and_dffr(full, window):
    d = build_design2(full, MAIN2, 2, DEC, window, END)
    got = covid_lag_leaks(d, 2)
    assert got == [P(q) for q in ("2020Q3", "2020Q4", "2021Q1", "2021Q2", "2021Q3")]
    assert P("2022Q1") not in got and P("2021Q4") not in got   # CRED(t−4) no cuenta


# --- Diseño de las proyecciones locales (RF-14 a RF-16) ---


def test_lp_design_morosidad_target_and_sample(full, window):
    K = 3
    for h in (0, 4, 12):
        d = build_lp_design(full, h, K, DEC, window, END, "morosidad")
        assert d.end == END - h and d.start == window[0]
        lvl = full["dralacbs"]
        for q in (d.y.index[0], d.y.index[40], d.y.index[-1]):
            assert d.y.loc[q] == pytest.approx(lvl.loc[q + h] - lvl.loc[q - 1])
        assert list(d.X.columns) == (["const", "d_ffr_l0", "y_lag", "gdp_l1", "d_unemp_l1",
                                       "inflation_l1", "credit_l4"]
                                      + [f"d_ffr_l{j}" for j in range(1, K + 1)] + COVID_NAMES)
        assert d.X["covid_2020q2"].loc[P("2020Q2")] == 1.0     # fechadas en t


def test_lp_design_tasa_target(full, window):
    d = build_lp_design(full, 3, 2, DEC, window, END, "tasa")
    ffr = full["fedfunds"]
    q = d.y.index[10]
    assert d.y.loc[q] == pytest.approx(ffr.loc[q + 3] - ffr.loc[q - 1])
    h0 = build_lp_design(full, 0, 2, DEC, window, END, "tasa")
    assert np.allclose(h0.y, h0.X["d_ffr_l0"])                 # h = 0 es identidad


def test_lp_design_never_uses_data_after_end(full, window):
    end = P("2024Q4")
    base = build_lp_design(full, 5, 3, DEC, window, end, "morosidad")
    changed = full.copy()
    changed.loc[P("2025Q1"):, :] = np.nan
    again = build_lp_design(changed, 5, 3, DEC, window, end, "morosidad")
    assert base.y.equals(again.y) and base.X.equals(again.X) and base.end == end - 5


def test_lp_design_nan_raises(full, window):
    holed = full.copy()
    holed.loc[P("2012Q1"), "dralacbs"] = np.nan
    with pytest.raises(ModelDataError) as e:
        build_lp_design(holed, 2, 3, DEC, window, END, "morosidad")
    assert "2011Q3" in str(e.value)                    # el primer trimestre afectado (t + h)


def test_lp_design_rejects_bad_target(full, window):
    with pytest.raises(ValueError):
        build_lp_design(full, 1, 3, DEC, window, END, "otro")
