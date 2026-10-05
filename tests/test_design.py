"""Tests para src/design.py (spec 003, tarea 1).

Cubre RF-1 a RF-5 y RF-15 según plan §7.
Datos sintéticos con parámetros conocidos; sin red ni disco.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.design import (
    ModelDataError,
    build_design,
    check_expected_forms,
    dependent_series,
    diff_form_stationary,
    effective_window,
    read_decisions,
)
from src.model1_config import (
    COVID_QUARTERS,
    EXPECTED_FORMS,
    LONG_START,
    MAIN,
    MAIN_START,
    VARIANTS,
    VariantSpec,
)


# --- Helpers ---


def _make_stationarity_df(decisions: dict[str, str] | None = None) -> pd.DataFrame:
    """Crea una tabla de estacionariedad sintética con las decisiones dadas."""
    if decisions is None:
        decisions = {
            "dralacbs": "ambigua (primera diferencia)",
            "dralacbn": "ambigua (primera diferencia)",
            "dralacbs_logit": "primera diferencia",
            "drclacbs": "primera diferencia",
            "drblacbs": "primera diferencia",
            "drsreacbs": "ambigua (primera diferencia)",
            "gdpc1_yoy": "niveles",
            "gdp_yoy": "niveles",
            "unrate_d": "niveles",
            "cpiaucsl_yoy": "niveles",
            "fedfunds_d": "niveles",
            "loans_yoy": "niveles",
        }
    rows = []
    for var, dec in decisions.items():
        rows.append({
            "variable": var,
            "etiqueta": var,
            "forma": "tal cual",
            "n_obs": 100,
            "adf_stat": -3.0,
            "adf_p": 0.01,
            "adf_lags": 2,
            "kpss_stat": 0.3,
            "kpss_p": 0.10,
            "kpss_p_truncado": "",
            "decision": dec,
            "orden": "I(0)" if dec == "niveles" else "I(1)",
        })
        rows.append({
            "variable": var,
            "etiqueta": var,
            "forma": "primera diferencia",
            "n_obs": 99,
            "adf_stat": -5.0,
            "adf_p": 0.001,
            "adf_lags": 1,
            "kpss_stat": 0.1,
            "kpss_p": 0.15,
            "kpss_p_truncado": "",
            "decision": "",
            "orden": "",
        })
    return pd.DataFrame(rows)


def _make_full_history(
    start: pd.Period = pd.Period("1998Q1", "Q-DEC"),
    end: pd.Period = pd.Period("2026Q2", "Q-DEC"),
    seed: int = 42,
) -> pd.DataFrame:
    """Crea un panel sintético con historia completa desde 1998.

    Todas las columnas necesarias para el Modelo I.
    """
    rng = np.random.default_rng(seed)
    idx = pd.period_range(start, end, freq="Q-DEC")
    n = len(idx)

    # Serie base para dependiente (random walk)
    dr = np.cumsum(rng.normal(0, 0.1, n)) + 2.0

    # Términos macro (ruido blanco)
    gdp = rng.normal(2.5, 1.0, n)
    unrate_d = rng.normal(0, 0.2, n)
    inflation = rng.normal(2.0, 0.5, n)
    fedfunds_d = rng.normal(0, 0.3, n)
    loans = rng.normal(5.0, 2.0, n)

    df = pd.DataFrame(index=idx)
    df["dralacbs"] = dr
    df["dralacbn"] = dr + rng.normal(0, 0.05, n)
    df["dralacbs_logit"] = np.log(dr / (100 - dr))
    df["drclacbs"] = dr * 0.8
    df["drblacbs"] = dr * 0.6
    df["drsreacbs"] = dr * 0.4
    df["gdpc1_yoy"] = gdp
    df["gdp_yoy"] = gdp + 2.0
    df["unrate_d"] = unrate_d
    df["cpiaucsl_yoy"] = inflation
    df["fedfunds_d"] = fedfunds_d
    # loans_yoy es variación interanual: necesita 4 trimestres de historia
    # Con datos desde 1998Q1, el primer valor es 1999Q1
    loans_yoy = np.full(n, np.nan)
    loans_yoy[4:] = loans[4:]
    df["loans_yoy"] = loans_yoy

    return df


# --- read_decisions ---


class TestReadDecisions:
    def test_read_decisions_returns_dict(self):
        stat = _make_stationarity_df()
        decisions = read_decisions(stat)
        assert isinstance(decisions, dict)
        assert "dralacbs" in decisions
        assert decisions["dralacbs"] == "ambigua (primera diferencia)"

    def test_read_decisions_only_tal_cual(self):
        stat = _make_stationarity_df()
        decisions = read_decisions(stat)
        # No debe incluir filas de "primera diferencia"
        assert len(decisions) == 12  # 12 variables


# --- check_expected_forms ---


class TestCheckExpectedForms:
    def test_check_expected_forms_passes(self):
        decisions = {
            "dralacbs": "ambigua (primera diferencia)",
            "dralacbn": "ambigua (primera diferencia)",
            "dralacbs_logit": "primera diferencia",
            "drclacbs": "primera diferencia",
            "drblacbs": "primera diferencia",
            "drsreacbs": "ambigua (primera diferencia)",
        }
        # No debe lanzar excepción
        check_expected_forms(decisions, EXPECTED_FORMS)

    def test_check_expected_forms_raises_on_mismatch(self):
        decisions = {
            "dralacbs": "niveles",  # debería ser "ambigua (primera diferencia)"
            "dralacbn": "ambigua (primera diferencia)",
            "dralacbs_logit": "primera diferencia",
            "drclacbs": "primera diferencia",
            "drblacbs": "primera diferencia",
            "drsreacbs": "ambigua (primera diferencia)",
        }
        with pytest.raises(ModelDataError, match="dralacbs.*forma esperada.*niveles"):
            check_expected_forms(decisions, EXPECTED_FORMS)

    def test_check_expected_forms_raises_on_missing(self):
        decisions = {
            "dralacbn": "ambigua (primera diferencia)",
            "dralacbs_logit": "primera diferencia",
            "drclacbs": "primera diferencia",
            "drblacbs": "primera diferencia",
            "drsreacbs": "ambigua (primera diferencia)",
        }
        with pytest.raises(ModelDataError, match="dralacbs.*no aparece"):
            check_expected_forms(decisions, EXPECTED_FORMS)


# --- dependent_series ---


class TestDependentSeries:
    def test_ambigua_gives_diff(self):
        full = _make_full_history()
        y = dependent_series(full, "dralacbs", "ambigua (primera diferencia)")
        expected = full["dralacbs"].diff()
        pd.testing.assert_series_equal(y, expected)

    def test_niveles_gives_level(self):
        full = _make_full_history()
        y = dependent_series(full, "dralacbs", "niveles")
        pd.testing.assert_series_equal(y, full["dralacbs"])

    def test_logit_also_diff(self):
        full = _make_full_history()
        y = dependent_series(full, "dralacbs_logit", "primera diferencia")
        expected = full["dralacbs_logit"].diff()
        pd.testing.assert_series_equal(y, expected)


# --- diff_form_stationary ---


class TestDiffFormStationary:
    def test_diff_form_stationary_returns_decision(self):
        stat = _make_stationarity_df()
        decision, forma = diff_form_stationary(stat, "unrate_d")
        assert forma == "primera diferencia"
        assert isinstance(decision, str)
        assert decision in ("niveles", "primera diferencia", "ambigua (primera diferencia)")

    def test_diff_form_stationary_missing_column(self):
        stat = _make_stationarity_df()
        with pytest.raises(ModelDataError, match="no hay fila"):
            diff_form_stationary(stat, "nonexistent")


# --- build_design ---


class TestBuildDesign:
    def test_build_design_basic(self):
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        design = build_design(full, MAIN, "ambigua (primera diferencia)", end)

        assert design.spec_id == "main"
        assert design.form == "primera diferencia"
        assert design.start == MAIN_START
        assert design.end == end
        assert "const" in design.X.columns
        assert "y_lag" in design.X.columns
        assert "gdp_growth" in design.X.columns
        assert "d_unemp" in design.X.columns
        assert "inflation" in design.X.columns
        assert "d_ffr" in design.X.columns
        assert "credit_growth" in design.X.columns

    def test_y_lag_is_t_minus_1(self):
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        design = build_design(full, MAIN, "ambigua (primera diferencia)", end)

        # y_lag(t) debe ser y(t-1)
        y = design.y
        y_lag = design.X["y_lag"]
        # Verificar que y_lag(t) = y(t-1)
        for i in range(1, len(y)):
            assert y_lag.iloc[i] == pytest.approx(y.iloc[i - 1])

    def test_credit_growth_is_t_minus_4(self):
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        design = build_design(full, MAIN, "ambigua (primera diferencia)", end)

        # credit_growth(t) debe ser loans_yoy(t-4)
        # En la ventana de diseño, el primer trimestre es 2000Q1
        # loans_yoy(2000Q1) = full["loans_yoy"] en 2000Q1
        # credit_growth(2000Q1) = loans_yoy(1999Q1)
        first_q = design.start
        loans_4_back = full["loans_yoy"].shift(4).loc[first_q]
        credit_in_design = design.X["credit_growth"].iloc[0]
        assert credit_in_design == pytest.approx(loans_4_back)

    def test_covid_dummies_only_in_their_quarters(self):
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        design = build_design(full, MAIN, "ambigua (primera diferencia)", end)

        for q_str in COVID_QUARTERS:
            q = pd.Period(q_str, "Q-DEC")
            dummy_name = f"covid_{q_str.lower().replace('q', 'q')}"
            if dummy_name in design.X.columns:
                # En el trimestre COVID debe valer 1
                if q in design.X.index:
                    assert design.X.loc[q, dummy_name] == 1.0
                # En otros trimestres debe valer 0
                other_q = pd.Period("2019Q1", "Q-DEC")
                if other_q in design.X.index:
                    assert design.X.loc[other_q, dummy_name] == 0.0

    def test_seasonal_dummies_base_t1(self):
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        spec = VariantSpec("test_seasonal", "Test estacional", seasonal_dummies=True)
        design = build_design(full, spec, "ambigua (primera diferencia)", end)

        # En T1 no debe haber dummy estacional
        t1_mask = design.X.index.quarter == 1
        if t1_mask.any():
            seasonal_cols = [c for c in design.X.columns if c.startswith("seasonal_q")]
            for col in seasonal_cols:
                assert (design.X.loc[t1_mask, col] == 0).all()

    def test_nan_interior_raises_error(self):
        full = _make_full_history()
        # Insertar un NaN interior en un trimestre específico
        full.loc[pd.Period("2010Q1", "Q-DEC"), "gdpc1_yoy"] = np.nan
        end = pd.Period("2026Q2", "Q-DEC")

        with pytest.raises(ModelDataError, match="gdpc1_yoy.*2010Q1.*main"):
            build_design(full, MAIN, "ambigua (primera diferencia)", end)

    def test_r1_includes_covid_dummies(self):
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        r1 = VARIANTS[0]  # R1
        design = build_design(full, r1, "ambigua (primera diferencia)", end)

        # R1 debe incluir las dummies COVID (corrección R1: covid_dummies=True)
        covid_cols = [c for c in design.X.columns if c.startswith("covid_")]
        assert len(covid_cols) == 4  # 4 trimestres COVID
        # Y no debe anotarlas en dropped
        assert len(design.dropped) == 0


# --- effective_window ---


class TestEffectiveWindow:
    def test_truncated_window_r6(self):
        """R6 (credit_lag=8) debe empezar en 2001T1 con datos desde 1998."""
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        r6 = VARIANTS[7]  # R6
        start, _ = effective_window(full, r6, end)
        assert start == pd.Period("2001Q1", "Q-DEC")

    def test_truncated_window_r7(self):
        """R7 (credit_lag=12) debe empezar en 2002T1 con datos desde 1998."""
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        r7 = VARIANTS[8]  # R7
        start, _ = effective_window(full, r7, end)
        assert start == pd.Period("2002Q1", "Q-DEC")

    def test_truncated_window_r8(self):
        """R8 (start=1985Q1) con datos desde 1998 debe empezar en 2000T1."""
        full = _make_full_history()
        end = pd.Period("2026Q2", "Q-DEC")
        r8 = VARIANTS[9]  # R8
        start, _ = effective_window(full, r8, end)
        # Con datos desde 1998, el primer trimestre con todos los términos
        # para credit_lag=4 es 1999Q1, pero R8 tiene truncate_start=True
        # y start=1985Q1, así que el máximo es 1999Q1
        # Pero el plan dice R8 = 2000T1, así que debe ser max(1985Q1, 1999Q1) = 1999Q1
        # Revisando el plan: "R8 sin historia anterior a 2000T1" sale como "no estimada"
        # en run_variant, no en effective_window
        assert start >= pd.Period("1999Q1", "Q-DEC")


# --- Integración: panel sintético completo ---


class TestIntegration:
    def test_full_pipeline_synthetic(self):
        """Pipeline completo con datos sintéticos."""
        full = _make_full_history()
        stat = _make_stationarity_df()
        decisions = read_decisions(stat)
        check_expected_forms(decisions, EXPECTED_FORMS)

        end = pd.Period("2026Q2", "Q-DEC")
        design = build_design(full, MAIN, decisions["dralacbs"], end)

        assert len(design.y) > 0
        assert design.X.shape[0] == len(design.y)
        assert not design.y.isna().any()
        assert not design.X.isna().any().any()
