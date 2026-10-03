"""Tests de ``src/config.py`` (T2, spec 001).

Verifican las constantes de series, fechas, umbrales y etiquetas en español
(RF-1, RF-17, RNF-5). Sin red: solo importan constantes.
"""

import pandas as pd
import pytest

from src.config import (
    ADF_MAXLAG,
    ALPHA,
    ALL_SERIES,
    COLUMN_LABELS,
    DELINQUENCY,
    DOCUMENTED_GAP_MONTH,
    DOCUMENTED_GAP_SERIES,
    DOWNLOAD_START,
    MAIN_SERIES,
    MONTHLY,
    RECESSION_SERIES,
    ROBUSTNESS_SERIES,
    SAMPLE_START,
    SERIES_META,
)

# Las 25 columnas del panel según plan.md, sección 2 (panel.py).
EXPECTED_COLUMNS = {
    # Morosidad (×5): nivel, diferencia trimestral y logit
    "dralacbs", "dralacbs_d", "dralacbs_logit",
    "dralacbn", "dralacbn_d", "dralacbn_logit",
    "drclacbs", "drclacbs_d", "drclacbs_logit",
    "drblacbs", "drblacbs_d", "drblacbs_logit",
    "drsreacbs", "drsreacbs_d", "drsreacbs_logit",
    # Variación interanual
    "gdpc1_yoy", "gdp_yoy", "cpiaucsl_yoy", "loans_yoy",
    # Nivel y diferencia trimestral
    "unrate", "unrate_d", "fedfunds", "fedfunds_d",
    # Otras
    "coralacbs", "usrec",
}

# Palabras típicamente inglesas que no deben aparecer en etiquetas en español.
ENGLISH_WORDS = (
    "rate", "unemployment", "level", "difference", "change",
    "index", "indicator", "percent", "billions", "loans",
)

META_KEYS = {"nombre", "unidad", "frecuencia", "desestacionalizacion", "tratamiento_trimestral"}


def test_all_series_has_13_elements():
    assert len(ALL_SERIES) == 13


def test_all_series_is_main_plus_rerobustness_plus_recession():
    assert ALL_SERIES == MAIN_SERIES + ROBUSTNESS_SERIES + [RECESSION_SERIES]


def test_main_and_robustness_do_not_overlap():
    assert set(MAIN_SERIES).isdisjoint(ROBUSTNESS_SERIES)


def test_recession_series_is_usrec():
    assert RECESSION_SERIES == "USREC"


def test_monthly_set():
    assert MONTHLY == {"UNRATE", "CPIAUCSL", "FEDFUNDS", "LOANS", "USREC"}


def test_delinquency_list():
    assert DELINQUENCY == ["DRALACBS", "DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS"]


def test_download_start():
    assert DOWNLOAD_START == "1998-01-01"


def test_sample_start_is_2000q1():
    assert SAMPLE_START == pd.Period("2000Q1", "Q-DEC")


def test_documented_gap():
    assert DOCUMENTED_GAP_SERIES == {"CPIAUCSL", "UNRATE"}
    assert DOCUMENTED_GAP_MONTH == pd.Period("2025-10", "M")


def test_alpha_is_005():
    assert ALPHA == 0.05


def test_adf_maxlag_is_4():
    assert ADF_MAXLAG == 4


def test_series_meta_covers_all_series():
    assert set(SERIES_META) == set(ALL_SERIES)


def test_series_meta_has_required_keys():
    for series_id, meta in SERIES_META.items():
        assert set(meta) == META_KEYS, f"{series_id}: claves {set(meta)} != {META_KEYS}"
        for key, value in meta.items():
            assert isinstance(value, str) and value.strip(), f"{series_id}.{key}: vacío"


def test_column_labels_cover_25_columns():
    assert set(COLUMN_LABELS) == EXPECTED_COLUMNS
    assert len(COLUMN_LABELS) == 25


def test_column_labels_in_spanish():
    for column, label in COLUMN_LABELS.items():
        assert isinstance(label, str) and label.strip(), f"{column}: etiqueta vacía"
        lowered = label.lower()
        for word in ENGLISH_WORDS:
            assert word not in lowered, f"{column}: '{label}' contiene la palabra inglesa '{word}'"


def test_column_labels_include_units():
    """Las etiquetas de niveles y diferencias declaran su unidad (%, pp o logit)."""
    for column in EXPECTED_COLUMNS:
        if column == "usrec":
            continue  # indicador 1/0, sin unidad de porcentaje
        label = COLUMN_LABELS[column]
        if column.endswith("_logit"):
            assert "logit" in label.lower(), f"{column}: falta 'logit' en '{label}'"
        elif column.endswith("_d"):
            assert "pp" in label.lower(), f"{column}: falta 'pp' en '{label}'"
        else:
            assert "%" in label, f"{column}: falta '%' en '{label}'"
