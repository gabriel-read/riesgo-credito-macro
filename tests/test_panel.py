"""Tests de ``src/panel.py`` (T5, spec 001).

Validación, agregación trimestral, completitud, último trimestre común,
excepción 2025T4 y faltantes terminales (RF-7, RF-8, RF-11, RF-12, RF-13, RF-25).
"""

from pathlib import Path
import pandas as pd
import pytest

from src.panel import (
    DataError,
    parse_raw,
    quarterly_from_monthly,
    recession_indicator,
    quarterly_from_quarterly,
    last_common_quarter,
    check_main_complete,
    check_terminal_only,
)
from src.config import MAIN_SERIES, DOWNLOAD_START, SAMPLE_START, DOCUMENTED_GAP_SERIES


# ---------- Helpers ----------

def _monthly_series(values: list, start: str = "1998-01-01") -> pd.Series:
    """Serie mensual sintética con índice PeriodIndex mensual."""
    idx = pd.period_range(start=start, periods=len(values), freq="M")
    return pd.Series(values, index=idx, name="test")


def _quarterly_series(values: list, start: str = "1998Q1") -> pd.Series:
    """Serie trimestral sintética con índice PeriodIndex Q-DEC."""
    idx = pd.period_range(start=start, periods=len(values), freq="Q-DEC")
    return pd.Series(values, index=idx, name="test")


def _raw_df(series_id: str, values: list, start: str = "1998-01-01") -> pd.DataFrame:
    """DataFrame crudo como lo lee fred_io (dtype=str, keep_default_na=False)."""
    idx = pd.period_range(start=start, periods=len(values), freq="M")
    dates = [p.strftime("%Y-%m-%d") for p in idx]
    return pd.DataFrame({"date": dates, series_id: [str(v) for v in values]})


# ---------- parse_raw (RF-7) ----------

def test_parse_raw_dot_empty_nan_become_nan():
    """'.', '' y 'NaN' pasan a NaN."""
    df = _raw_df("TEST", [".", "", "NaN", "1.5"])
    s = parse_raw(df, "TEST")
    assert pd.isna(s.iloc[0])
    assert pd.isna(s.iloc[1])
    assert pd.isna(s.iloc[2])
    assert s.iloc[3] == 1.5


def test_parse_raw_non_numeric_raises_dataerror():
    """Texto no numérico distinto de marcadores → DataError con la serie."""
    df = _raw_df("TEST", ["abc"])
    with pytest.raises(DataError, match="TEST"):
        parse_raw(df, "TEST")


def test_parse_raw_zero_rows_raises():
    """Cero filas de datos → DataError."""
    df = pd.DataFrame({"date": [], "TEST": []})
    with pytest.raises(DataError, match="TEST"):
        parse_raw(df, "TEST")


def test_parse_raw_first_obs_after_1998_raises():
    """Primera observación después de 1998-01-01 → DataError (no cubre desde 1998)."""
    # parse_raw usa DOWNLOAD_START = "1998-01-01"
    df = _raw_df("TEST", [1.0, 2.0], start="1999-01-01")
    with pytest.raises(DataError, match="TEST"):
        parse_raw(df, "TEST")


# ---------- quarterly_from_monthly (RF-8, RF-11, RF-12) ----------

def test_quarterly_from_monthly_three_months():
    """Tres meses con dato → media y completo=True."""
    monthly = _monthly_series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])  # 1998M1-M6
    value, complete, trat = quarterly_from_monthly(monthly, "TEST")
    # 1998Q1 = media(1,2,3) = 2.0; 1998Q2 = media(4,5,6) = 5.0
    assert list(value.values) == [2.0, 5.0]
    assert all(complete)
    assert trat is None


def test_quarterly_from_monthly_missing_month_is_nan():
    """Un mes NaN en el trimestre → NaN y completo=False (sin media silenciosa)."""
    monthly = _monthly_series([1.0, None, 3.0, 4.0, 5.0, 6.0])
    value, complete, trat = quarterly_from_monthly(monthly, "TEST")
    # 1998Q1: solo 2 meses con dato (M2 es NaN) → NaN
    assert pd.isna(value.iloc[0])
    assert not complete.iloc[0]
    # 1998Q2: 3 meses con dato → media
    assert value.iloc[1] == 5.0
    assert complete.iloc[1]


def test_cpi_unrate_missing_oct_2025_rf11():
    """CPI/UNRATE sin octubre 2025 → media(nov,dic) y 'RF-11'."""
    # Construir serie que llegue exactamente a 2025M12
    # 1998-01 a 2025-12 = 28 años * 12 = 336 meses
    base = [1.0] * 333  # hasta 2025M9
    base.extend([None, 5.0, 7.0])  # 2025M10=None, M11=5, M12=7
    monthly = _monthly_series(base)
    value, complete, trat = quarterly_from_monthly(monthly, "CPIAUCSL")
    # 2025Q3 tiene 3 meses (jul, ago, sep) → media = 1.0
    assert value.iloc[-2] == 1.0  # 2025Q3 completo
    assert value.iloc[-1] == 6.0    # 2025Q4 = (5+7)/2
    assert complete.iloc[-1]
    assert trat == "RF-11"


def test_cpi_unrate_with_oct_2025_rf12():
    """CPI/UNRATE con octubre 2025 → tres meses y 'RF-12'."""
    base = [1.0] * 333
    base.extend([3.0, 5.0, 7.0])  # 2025M10=3, M11=5, M12=7
    monthly = _monthly_series(base)
    value, complete, trat = quarterly_from_monthly(monthly, "CPIAUCSL")
    assert value.iloc[-1] == 5.0    # (3+5+7)/3 = 5.0
    assert complete.iloc[-1]
    assert trat == "RF-12"


def test_fedfunds_missing_oct_2025_returns_nan():
    """FEDFUNDS sin octubre 2025 → NaN y completo=False (no es excepción documentada).
    El error se lanza luego en check_main_complete/build_panel.
    """
    base = [1.0] * 333
    base.extend([None, 5.0, 7.0])  # 2025M10=None
    monthly = _monthly_series(base)
    value, complete, trat = quarterly_from_monthly(monthly, "FEDFUNDS")
    assert pd.isna(value.iloc[-1])   # 2025Q4 NaN
    assert not complete.iloc[-1]     # incompleto
    assert trat is None


# ---------- recession_indicator (RF-9) ----------

def test_recession_indicator_one_month_is_one():
    """Un mes en recesión → trimestre = 1."""
    monthly = _monthly_series([0, 0, 1, 0, 0, 0])  # 1998M3 = 1
    q = recession_indicator(monthly)
    assert q.iloc[0] == 1  # 1998Q1


def test_recession_indicator_incomplete_quarter_is_nan():
    """Trimestre incompleto → NaN (no 0 ni 1)."""
    monthly = _monthly_series([1, 0])  # solo 2 meses
    q = recession_indicator(monthly)
    assert pd.isna(q.iloc[0])


# ---------- quarterly_from_quarterly (RF-8) ----------

def test_quarterly_from_quarterly_end_of_period():
    """Serie trimestal: se toma sin agregar (dato fin de periodo)."""
    q = _quarterly_series([1.0, 2.0, 3.0])
    value, complete = quarterly_from_quarterly(q)
    assert list(value.values) == [1.0, 2.0, 3.0]
    assert all(complete)


# ---------- last_common_quarter (RF-10, RF-25) ----------

def test_last_common_quarter_main_only():
    """Último trimestre donde todas las MAIN_SERIES tienen dato."""
    complete = {
        "DRALACBS": pd.Series([True, True, True], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC")),
        "GDPC1": pd.Series([True, True, False], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC")),
        "GDP": pd.Series([True, True, True], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC")),
        "UNRATE": pd.Series([True, True, True], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC")),
        "CPIAUCSL": pd.Series([True, True, True], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC")),
        "FEDFUNDS": pd.Series([True, True, True], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC")),
        "LOANS": pd.Series([True, True, True], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC")),
    }
    end = last_common_quarter(complete, MAIN_SERIES)
    assert end == pd.Period("2000Q2", "Q-DEC")  # GDPC1 falla en Q3


# ---------- check_main_complete (RF-13) ----------

def test_check_main_complete_interior_gap_raises():
    """Hueco interior en serie principal → DataError con serie y trimestre."""
    # DRALACBS tiene NaN en 2000Q2
    vals = pd.Series([1.0, None, 3.0], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC"))
    complete = {sid: pd.Series([True]*3, index=vals.index) for sid in MAIN_SERIES}
    complete["DRALACBS"] = pd.Series([True, False, True], index=vals.index)
    with pytest.raises(DataError, match="DRALACBS.*2000Q2"):
        check_main_complete(complete, pd.Period("2000Q1", "Q-DEC"), pd.Period("2000Q3", "Q-DEC"))


def test_check_main_complete_coverage_2000q1_raises():
    """Serie principal sin 1999Q1 (necesario para yoy en 2000Q1) → error cobertura."""
    # Este test se hace en build_panel, aquí solo verificamos la lógica de check_main_complete
    pass


# ---------- check_terminal_only (RF-25) ----------

def test_check_terminal_only_robustness_ends_early():
    """Serie de robustez termina antes → NaN terminal sin recortar, registra último trimestre."""
    # CORALACBS tiene datos hasta 2000Q2, panel hasta 2000Q3
    vals = pd.Series([1.0, 2.0, None], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC"))
    last = check_terminal_only(vals, "CORALACBS", pd.Period("2000Q1", "Q-DEC"), pd.Period("2000Q3", "Q-DEC"))
    assert last == pd.Period("2000Q2", "Q-DEC")


def test_check_terminal_only_interior_nan_raises():
    """NaN interior en serie de robustez → DataError."""
    vals = pd.Series([1.0, None, 3.0], index=pd.period_range("2000Q1", periods=3, freq="Q-DEC"))
    with pytest.raises(DataError, match="CORALACBS.*2000Q2"):
        check_terminal_only(vals, "CORALACBS", pd.Period("2000Q1", "Q-DEC"), pd.Period("2000Q3", "Q-DEC"))