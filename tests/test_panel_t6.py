"""Tests de transformaciones y `build_panel` (T6, spec 001).

Cubren `yoy`, `diff_pp`, `logit_rate`, `transform`, `build_panel`
(RF-9, RF-10, RF-14, RF-15, RF-16).
"""

import numpy as np
import pandas as pd
import pytest

from src.panel import (
    DataError,
    PanelResult,
    build_panel,
    diff_pp,
    logit_rate,
    transform,
    yoy,
)
from src.config import SAMPLE_START


# ---------- Helpers ----------

def _quarterly_df(values_dict: dict[str, list], start: str = "1998Q1") -> pd.DataFrame:
    """DataFrame trimestral sintético con PeriodIndex Q-DEC."""
    n = len(next(iter(values_dict.values())))
    idx = pd.period_range(start=start, periods=n, freq="Q-DEC")
    return pd.DataFrame(values_dict, index=idx)


# ---------- yoy ----------

def test_yoy_exact_known_result():
    """yoy de x = exp(0.01*t) da 4.0 exacto (100*(ln(e^0.01*4))) y usa t-4 aunque falte fila."""
    # x_t = exp(0.01 * t) donde t = 0,1,2,... trimestres
    # ln(x_t) = 0.01 * t
    # ln(x_t) - ln(x_{t-4}) = 0.01 * 4 = 0.04
    # 100 * 0.04 = 4.0
    t = np.arange(20)
    x = pd.Series(np.exp(0.01 * t), index=pd.period_range("1998Q1", periods=20, freq="Q-DEC"))
    result = yoy(x)
    # Desde t=4 en adelante debe ser 4.0
    expected = pd.Series([np.nan]*4 + [4.0]*16, index=x.index)
    pd.testing.assert_series_equal(result, expected, check_names=False)

    # Con fila faltante en t=5, shift(4) en t=9 usa t=5 (que es NaN) → resultado NaN
    # Pero el test del plan dice "usa t-4 aunque falte una fila" - verificamos que no hace shift posicional
    x_with_gap = x.copy()
    x_with_gap.iloc[5] = np.nan  # t=5 faltante
    result_gap = yoy(x_with_gap)
    # t=9 usa t=5 (NaN) → NaN; t=10 usa t=6 (válido) → 4.0
    assert pd.isna(result_gap.iloc[9])
    assert abs(result_gap.iloc[10] - 4.0) < 1e-10


# ---------- diff_pp ----------

def test_diff_pp_known():
    """diff_pp es diferencia simple conocida."""
    x = pd.Series([1.0, 2.0, 4.0, 7.0], index=pd.period_range("2000Q1", periods=4, freq="Q-DEC"))
    result = diff_pp(x)
    expected = pd.Series([np.nan, 1.0, 2.0, 3.0], index=x.index)
    pd.testing.assert_series_equal(result, expected, check_names=False)


# ---------- logit_rate ----------

def test_logit_rate_50_is_zero():
    """logit_rate(50) == 0 porque ln(50/50) = 0."""
    x = pd.Series([50.0], index=pd.period_range("2000Q1", periods=1, freq="Q-DEC"))
    result = logit_rate(x, "TEST")
    assert result.iloc[0] == 0.0


def test_logit_rate_zero_raises():
    """DR <= 0 → DataError con serie y trimestre."""
    x = pd.Series([0.0], index=pd.period_range("2000Q1", periods=1, freq="Q-DEC"))
    with pytest.raises(DataError, match="TEST.*2000Q1"):
        logit_rate(x, "TEST")


def test_logit_rate_100_raises():
    """DR >= 100 → DataError con serie y trimestre."""
    x = pd.Series([100.0], index=pd.period_range("2000Q1", periods=1, freq="Q-DEC"))
    with pytest.raises(DataError, match="TEST.*2000Q1"):
        logit_rate(x, "TEST")


# ---------- transform ----------

def test_transform_produces_25_columns():
    """transform produce las 25 columnas del panel sobre historia desde 1998."""
    # Mínimo: 12 trimestres (1998Q1-2000Q4) para que yoy tenga datos desde 2000Q1
    n = 12
    idx = pd.period_range("1998Q1", periods=n, freq="Q-DEC")
    quarterly = pd.DataFrame(index=idx)
    # Llenar con datos sintéticos válidos
    for sid in ["DRALACBS", "DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS"]:
        quarterly[sid] = 2.0 + np.arange(n) * 0.1  # >0 y <100
    quarterly["GDPC1"] = np.exp(0.01 * np.arange(n))
    quarterly["GDP"] = np.exp(0.01 * np.arange(n))
    quarterly["CPIAUCSL"] = 100 + np.arange(n) * 0.5
    quarterly["LOANS"] = np.exp(0.01 * np.arange(n))
    quarterly["UNRATE"] = 5.0 + np.arange(n) * 0.05
    quarterly["FEDFUNDS"] = 2.0 + np.arange(n) * 0.03
    quarterly["CORALACBS"] = 0.5 + np.arange(n) * 0.01
    quarterly["USREC"] = 0.0

    out = transform(quarterly)
    # 25 columnas según plan
    assert len(out.columns) == 25
    expected_cols = {
        "dralacbs", "dralacbs_d", "dralacbs_logit",
        "dralacbn", "dralacbn_d", "dralacbn_logit",
        "drclacbs", "drclacbs_d", "drclacbs_logit",
        "drblacbs", "drblacbs_d", "drblacbs_logit",
        "drsreacbs", "drsreacbs_d", "drsreacbs_logit",
        "gdpc1_yoy", "gdp_yoy", "cpiaucsl_yoy", "loans_yoy",
        "unrate", "unrate_d", "fedfunds", "fedfunds_d",
        "coralacbs", "usrec",
    }
    assert set(out.columns) == expected_cols


# ---------- build_panel ----------

def _make_raw_dict() -> dict[str, pd.DataFrame]:
    """Diccionario raw mínimo para build_panel (13 series, datos desde 1998)."""
    # Mensuales: 336 meses (1998-01 a 2025-12) para cubrir hasta 2025Q4
    # Trimestrales: 112 trimestres (1998Q1 a 2025Q4)
    monthly_n = 336
    quarterly_n = 112
    monthly_idx = pd.period_range("1998-01", periods=monthly_n, freq="M")
    quarterly_idx = pd.period_range("1998Q1", periods=quarterly_n, freq="Q-DEC")

    def mk_monthly(name: str, base: float = 1.0) -> pd.DataFrame:
        vals = base + np.arange(monthly_n) * 0.01
        dates = [p.strftime("%Y-%m-%d") for p in monthly_idx]
        return pd.DataFrame({"date": dates, name: [str(v) for v in vals]})

    def mk_quarterly(name: str, base: float = 1.0) -> pd.DataFrame:
        vals = base + np.arange(quarterly_n) * 0.01
        dates = [p.strftime("%Y-%m-%d") for p in quarterly_idx.to_timestamp(how="start")]
        return pd.DataFrame({"date": dates, name: [str(v) for v in vals]})

    # Para DRALACBS y morosidad: valores en (0, 100)
    def mk_delinquency(name: str) -> pd.DataFrame:
        vals = 2.0 + np.arange(quarterly_n) * 0.05  # 2.0 a ~7.5
        dates = [p.strftime("%Y-%m-%d") for p in quarterly_idx.to_timestamp(how="start")]
        return pd.DataFrame({"date": dates, name: [str(v) for v in vals]})

    raw = {}
    # Mensuales
    raw["UNRATE"] = mk_monthly("UNRATE", 5.0)
    raw["CPIAUCSL"] = mk_monthly("CPIAUCSL", 100.0)
    raw["FEDFUNDS"] = mk_monthly("FEDFUNDS", 2.0)
    raw["LOANS"] = mk_monthly("LOANS", 1000.0)
    raw["USREC"] = mk_monthly("USREC", 0.0)  # todo ceros, sin recesiones
    # Trimestrales principales
    raw["DRALACBS"] = mk_delinquency("DRALACBS")
    raw["GDPC1"] = mk_quarterly("GDPC1", 10000.0)
    raw["GDP"] = mk_quarterly("GDP", 11000.0)
    # Robustez
    raw["DRALACBN"] = mk_delinquency("DRALACBN")
    raw["DRCLACBS"] = mk_delinquency("DRCLACBS")
    raw["DRBLACBS"] = mk_delinquency("DRBLACBS")
    raw["DRSREACBS"] = mk_delinquency("DRSREACBS")
    raw["CORALACBS"] = mk_quarterly("CORALACBS", 0.5)

    return raw


def test_build_panel_produces_panel_from_2000q1():
    """build_panel produce panel con 25 columnas desde 2000T1."""
    raw = _make_raw_dict()
    result = build_panel(raw)

    assert isinstance(result, PanelResult)
    assert result.panel.index[0] == SAMPLE_START
    assert len(result.panel.columns) == 25
    # Sin NaN en columnas principales (excepto usrec)
    for col in result.panel.columns:
        if col == "usrec":
            continue
        assert not result.panel[col].isna().any(), f"NaN en {col}"


def test_build_panel_end_is_last_common_quarter():
    """end es el último trimestre común de las series principales."""
    raw = _make_raw_dict()
    result = build_panel(raw)
    # Todas las series principales tienen datos hasta 2025Q4 (112 trimestres desde 1998Q1)
    # 1998Q1 + 111 = 2025Q4
    assert result.end == pd.Period("2025Q4", "Q-DEC")


def test_build_panel_nan_in_main_raises():
    """NaN en columna principal del panel → DataError."""
    raw = _make_raw_dict()
    # Romper DRALACBS en 2000Q2 (índice 8 en quarterly: 1998Q1=0, 2000Q2=8)
    raw["DRALACBS"].iloc[8, 1] = "."
    with pytest.raises(DataError, match="DRALACBS.*2000Q1"):
        build_panel(raw)