"""Tests de descriptivas, tablas, nota de datos y variables de informe (T8, spec 001).

RF-17, RF-18.
"""

import pandas as pd
import pytest

from src.descriptives import descriptive_table
from src.tables import fmt_es, quarter_label, to_markdown
from src.data_note import build_data_note
from src.report_vars import data_variables
from src.panel import PanelResult


# ---------- descriptive_table ----------

def test_descriptive_table_known():
    """Descriptivos de columna conocida."""
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], name="test")
    df = descriptive_table(pd.DataFrame({"test": s}))
    row = df.loc["test"]
    assert row["n"] == 5
    assert row["media"] == 3.0
    assert row["desv_est"] == pytest.approx(1.5811, rel=1e-3)
    assert row["min"] == 1.0
    assert row["mediana"] == 3.0
    assert row["max"] == 5.0


# ---------- fmt_es ----------

def test_fmt_es_decimal():
    """fmt_es(2.345) == '2,35' (coma decimal, 2 decimales)."""
    assert fmt_es(2.345) == "2,35"
    assert fmt_es(2.3) == "2,30"
    assert fmt_es(-1.5) == "-1,50"


def test_fmt_es_nan():
    """fmt_es(NaN) == '—'."""
    assert fmt_es(float("nan")) == "—"


# ---------- quarter_label ----------

def test_quarter_label():
    """quarter_label(2026Q2) -> '2026T2'."""
    q = pd.Period("2026Q2", "Q-DEC")
    assert quarter_label(q) == "2026T2"


# ---------- to_markdown ----------

def test_to_markdown_pipe_header():
    """to_markdown produce cabecera pipe."""
    df = pd.DataFrame({"a": [1], "b": [2]})
    md = to_markdown(df)
    assert "| a | b |" in md
    assert "| --- | --- |" in md
    assert "| 1,00 | 2,00 |" in md


# ---------- build_data_note ----------

def _make_panel_result() -> PanelResult:
    """PanelResult mínimo para tests."""
    idx = pd.period_range("2000Q1", periods=4, freq="Q-DEC")
    full = pd.DataFrame(index=idx)
    panel = pd.DataFrame(index=idx)
    for col in ["dralacbs", "unrate", "fedfunds", "usrec"]:
        full[col] = [1.0, 2.0, 3.0, 4.0]
        panel[col] = [1.0, 2.0, 3.0, 4.0]
    return PanelResult(
        full=full,
        panel=panel,
        end=pd.Period("2025Q4", "Q-DEC"),
        excluded_tail=[(pd.Period("2026Q1", "Q-DEC"), "DRALACBS", "incompleto")],
        gap_treatment={"CPIAUCSL": "RF-11", "UNRATE": "RF-11"},
        terminal_gaps={},
        observed={
            "DRALACBS": (pd.Period("1998Q1", "Q-DEC"), pd.Period("2025Q4", "Q-DEC"), 112),
            "UNRATE": (pd.Period("1998-01", "M"), pd.Period("2025-12", "M"), 336),
            "CPIAUCSL": (pd.Period("1998-01", "M"), pd.Period("2025-12", "M"), 336),
        },
    )


def _make_manifest() -> pd.DataFrame:
    return pd.DataFrame({
        "series": ["DRALACBS", "UNRATE", "CPIAUCSL", "FEDFUNDS", "LOANS", "GDPC1", "GDP",
                   "DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS", "CORALACBS", "USREC"],
        "download_date": ["2026-10-02"] * 13,
        "source": ["pandas-datareader"] * 13,
        "file": [f"{s}_2026-10-02.csv" for s in ["DRALACBS", "UNRATE", "CPIAUCSL", "FEDFUNDS", "LOANS", "GDPC1", "GDP",
                   "DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS", "CORALACBS", "USREC"]],
        "n_rows": ["112", "336", "336", "336", "336", "112", "112", "112", "112", "112", "112", "112", "336"],
        "first_obs": ["1998-01-01"] * 7 + ["1998-01-01"] * 6,
        "last_obs": ["2025-04-01"] * 7 + ["2025-12-01"] * 6,
    })


def test_build_data_note_contains_13_codes():
    """Nota de datos contiene los 13 códigos de serie."""
    result = _make_panel_result()
    manifest = _make_manifest()
    from src.config import SERIES_META
    note = build_data_note(result, manifest, SERIES_META)
    for sid in ["DRALACBS", "UNRATE", "CPIAUCSL", "FEDFUNDS", "LOANS", "GDPC1", "GDP",
                "DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS", "CORALACBS", "USREC"]:
        assert sid in note


def test_build_data_note_contains_2025t4():
    """Nota de datos menciona 2025T4."""
    result = _make_panel_result()
    manifest = _make_manifest()
    from src.config import SERIES_META
    note = build_data_note(result, manifest, SERIES_META)
    assert "2025T4" in note


def test_build_data_note_contains_loans_fedfunds():
    """Nota de datos explica LOANS y FEDFUNDS."""
    result = _make_panel_result()
    manifest = _make_manifest()
    from src.config import SERIES_META
    note = build_data_note(result, manifest, SERIES_META)
    assert "LOANS" in note
    assert "FEDFUNDS" in note


def test_build_data_note_contains_end_quarter():
    """Nota de datos incluye el trimestre final."""
    result = _make_panel_result()
    manifest = _make_manifest()
    from src.config import SERIES_META
    note = build_data_note(result, manifest, SERIES_META)
    assert "2025T4" in note


# ---------- data_variables ----------

def test_data_variables_all_keys():
    """data_variables trae todas las claves del bloque datos:."""
    result = _make_panel_result()
    manifest = _make_manifest()
    # stationarity table simulada
    stationarity = pd.DataFrame({
        "variable": ["dralacbs", "unrate"],
        "forma": ["tal cual", "tal cual"],
        "decision": ["niveles", "primera diferencia"],
        "orden": ["I(0)", "I(1)"],
    })
    vars_dict = data_variables(result, stationarity, manifest)
    expected_keys = {
        "muestra_inicio", "muestra_fin", "n_trimestres", "n_series", "fecha_descarga",
        "trimestres_excluidos", "cpiaucsl_2025t4_meses", "unrate_2025t4_meses",
        "dralacbs_media", "dralacbs_desv", "dralacbs_max", "dralacbs_max_trimestre",
        "dralacbs_min", "dralacbs_min_trimestre", "dralacbs_ultimo",
        "unrate_max", "unrate_max_trimestre", "fedfunds_max", "fedfunds_ultimo",
        "decision", "orden", "n_ambiguas",
    }
    assert set(vars_dict.keys()) == expected_keys