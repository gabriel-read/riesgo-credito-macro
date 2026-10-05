"""Configuración del pre-registro del Modelo I (spec 003).

Constantes, términos, signos esperados, variantes R1–R8, formas esperadas,
umbrales, quiebres de Chow, tramos fuera de muestra, semilla y etiquetas.
Sin acceso a red, disco ni gráficos (RNF-6). RF-3, RF-4, RF-9, RF-12, RF-16.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

# --- Constantes generales ---

SEED = 20261005
ALPHA = 0.05                 # significativo / veredicto de diagnósticos
ROBUST_ALPHA = 0.10          # criterio de robustez
LONGRUN_MIN_GAP = 0.05       # se reporta largo plazo solo si 1 - rho > 0.05
VIF_ALERT = 10.0
MIN_DOF = 30                 # RF-6
PSD_REL_TOL = 1e-10          # piso relativo de valores propios

# --- Muestra ---

MAIN_START = pd.Period("2000Q1", "Q-DEC")
LONG_START = pd.Period("1985Q1", "Q-DEC")
COVID_QUARTERS = ["2020Q2", "2020Q3", "2020Q4", "2021Q1"]
R1_EXCLUDED = ("2020Q1", "2021Q4")
CHOW_BREAKS = ["2008Q3", "2020Q2"]
BG_LAGS = 4

# --- Fuera de muestra ---

OOS_TRAIN = ("2000Q1", "2019Q4")
OOS_TEST_START = "2022Q1"
OOS_ANCHOR = "2021Q4"

# --- Términos internos (inglés) -> columna de la historia transformada ---

MACRO_TERMS: dict[str, str] = {
    "gdp_growth": "gdpc1_yoy",
    "d_unemp": "unrate_d",
    "inflation": "cpiaucsl_yoy",
    "d_ffr": "fedfunds_d",
    "credit_growth": "loans_yoy",  # credit_growth se rezaga CREDIT_LAG
}
CREDIT_LAG = 4

# --- Signos esperados ---

EXPECTED_SIGN: dict[str, str | None] = {
    "gdp_growth": "-",
    "d_unemp": "+",
    "d_ffr": "+",
    "credit_growth": "+",
    "inflation": None,   # None = "sin contraste"
    "y_lag": None,
    "const": None,
}

# --- Formas esperadas (decisión leída el 5-oct-2026) ---

EXPECTED_FORMS: dict[str, str] = {
    "dralacbs": "ambigua (primera diferencia)",
    "dralacbn": "ambigua (primera diferencia)",
    "dralacbs_logit": "primera diferencia",
    "drclacbs": "primera diferencia",
    "drblacbs": "primera diferencia",
    "drsreacbs": "ambigua (primera diferencia)",
}

# --- Etiquetas en español ---

TERM_LABELS: dict[str, str] = {
    "const": "Constante",
    "y_lag": "Y(t−1) — rezago de la dependiente",
    "gdp_growth": "ΔPIB (variación interanual del PIB real, %)",
    "d_unemp": "ΔU (cambio trimestral del desempleo, pp)",
    "inflation": "π (inflación interanual, %)",
    "d_ffr": "ΔFFR (cambio trimestral de la tasa de la Fed, pp)",
    "credit_growth": "CRED(t−4) (variación interanual de préstamos rezagada 4 trimestres, %)",
}


# --- Variantes ---

@dataclass(frozen=True)
class VariantSpec:
    """Especificación de una variante del Modelo I."""

    id: str                    # "main", "R1", "R2", "R3_drclacbs", ..., "R8", "oos"
    label: str                 # en español
    dependent: str = "dralacbs"
    gdp_column: str = "gdpc1_yoy"
    credit_lag: int = 4
    start: pd.Period = MAIN_START
    end: pd.Period | None = None          # None = último trimestre común
    exclude: tuple[str, str] | None = None
    covid_dummies: bool = True
    seasonal_dummies: bool = False
    truncate_start: bool = False          # True en R6, R7 y R8
    in_pp: bool = True                    # False en R5 (logit)


MAIN = VariantSpec("main", "Especificación principal")

VARIANTS: list[VariantSpec] = [
    VariantSpec("R1", "Sin 2020–2021", exclude=R1_EXCLUDED, covid_dummies=True),
    VariantSpec("R2", "Desestacionalizada con dummies estacionales",
                dependent="dralacbn", seasonal_dummies=True),
    VariantSpec("R3_drclacbs", "Tarjetas de crédito", dependent="drclacbs"),
    VariantSpec("R3_drblacbs", "Préstamos empresariales", dependent="drblacbs"),
    VariantSpec("R3_drsreacbs", "Préstamos inmobiliarios", dependent="drsreacbs"),
    VariantSpec("R4", "PIB nominal", gdp_column="gdp_yoy"),
    VariantSpec("R5", "Logit de la morosidad", dependent="dralacbs_logit", in_pp=False),
    VariantSpec("R6", "Crédito rezagado 8 trimestres", credit_lag=8, truncate_start=True),
    VariantSpec("R7", "Crédito rezagado 12 trimestres", credit_lag=12, truncate_start=True),
    VariantSpec("R8", "Muestra larga desde 1985T1", start=LONG_START, truncate_start=True),
]
