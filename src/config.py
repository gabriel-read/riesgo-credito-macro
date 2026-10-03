"""Configuración del pipeline de datos (spec 001).

Constantes de series, fechas, umbrales y etiquetas en español.
RF-1, RF-17, RNF-5.
"""

from __future__ import annotations

import pandas as pd

# --- Series (RF-1) ---

MAIN_SERIES = ["DRALACBS", "GDPC1", "GDP", "UNRATE", "CPIAUCSL", "FEDFUNDS", "LOANS"]
ROBUSTNESS_SERIES = ["DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS", "CORALACBS"]
RECESSION_SERIES = "USREC"
ALL_SERIES = MAIN_SERIES + ROBUSTNESS_SERIES + [RECESSION_SERIES]  # 13

MONTHLY = {"UNRATE", "CPIAUCSL", "FEDFUNDS", "LOANS", "USREC"}
DELINQUENCY = ["DRALACBS", "DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS"]

# --- Fechas y muestra ---

DOWNLOAD_START = "1998-01-01"
SAMPLE_START = pd.Period("2000Q1", "Q-DEC")

# Excepción documentada: octubre 2025 falta en CPIAUCSL y UNRATE (cierre del gobierno de EE. UU.)
DOCUMENTED_GAP_SERIES = {"CPIAUCSL", "UNRATE"}
DOCUMENTED_GAP_MONTH = pd.Period("2025-10", "M")

# --- Pruebas de estacionariedad (pre-registradas) ---

ALPHA = 0.05
ADF_MAXLAG = 4

# --- Metadatos de cada serie (RF-17) ---
# Unidad, frecuencia, desestacionalización, tratamiento trimestral y nombre en español.
# Las unidades se verifican contra FRED en la tarea de descarga (T4).

SERIES_META: dict[str, dict[str, str]] = {
    "DRALACBS": {
        "nombre": "Tasa de morosidad — todos los préstamos, bancos comerciales",
        "unidad": "porcentaje",
        "frecuencia": "trimestral",
        "desestacionalizacion": "desestacionalizada",
        "tratamiento_trimestral": "dato de fin de periodo",
    },
    "DRALACBN": {
        "nombre": "Tasa de morosidad sin desestacionalizar — todos los préstamos, bancos comerciales",
        "unidad": "porcentaje",
        "frecuencia": "trimestral",
        "desestacionalizacion": "sin desestacionalizar",
        "tratamiento_trimestral": "dato de fin de periodo",
    },
    "DRCLACBS": {
        "nombre": "Tasa de morosidad — tarjetas de crédito, bancos comerciales",
        "unidad": "porcentaje",
        "frecuencia": "trimestral",
        "desestacionalizacion": "desestacionalizada",
        "tratamiento_trimestral": "dato de fin de periodo",
    },
    "DRBLACBS": {
        "nombre": "Tasa de morosidad — préstamos empresariales, bancos comerciales",
        "unidad": "porcentaje",
        "frecuencia": "trimestral",
        "desestacionalizacion": "desestacionalizada",
        "tratamiento_trimestral": "dato de fin de periodo",
    },
    "DRSREACBS": {
        "nombre": "Tasa de morosidad — préstamos inmobiliarios, bancos comerciales",
        "unidad": "porcentaje",
        "frecuencia": "trimestral",
        "desestacionalizacion": "desestacionalizada",
        "tratamiento_trimestral": "dato de fin de periodo",
    },
    "GDPC1": {
        "nombre": "PIB real de Estados Unidos",
        "unidad": "miles de millones de dólares encadenados (año base según FRED)",
        "frecuencia": "trimestral",
        "desestacionalizacion": "desestacionalizada, tasa anual",
        "tratamiento_trimestral": "dato de fin de periodo",
    },
    "GDP": {
        "nombre": "PIB nominal de Estados Unidos",
        "unidad": "miles de millones de dólares",
        "frecuencia": "trimestral",
        "desestacionalizacion": "desestacionalizada, tasa anual",
        "tratamiento_trimestral": "dato de fin de periodo",
    },
    "UNRATE": {
        "nombre": "Tasa de desempleo de Estados Unidos",
        "unidad": "porcentaje",
        "frecuencia": "mensual",
        "desestacionalizacion": "desestacionalizada",
        "tratamiento_trimestral": "media de los meses del trimestre",
    },
    "CPIAUCSL": {
        "nombre": "Índice de precios al consumidor — todos los artículos, zonas urbanas",
        "unidad": "índice (1982-1984 = 100)",
        "frecuencia": "mensual",
        "desestacionalizacion": "desestacionalizada",
        "tratamiento_trimestral": "media de los meses del trimestre",
    },
    "FEDFUNDS": {
        "nombre": "Tasa efectiva de fondos federales",
        "unidad": "porcentaje",
        "frecuencia": "mensual",
        "desestacionalizacion": "sin desestacionalizar",
        "tratamiento_trimestral": "media de los meses del trimestre",
    },
    "LOANS": {
        "nombre": "Préstamos y arrendamientos en crédito bancario, bancos comerciales",
        "unidad": "miles de millones de dólares",
        "frecuencia": "mensual",
        "desestacionalizacion": "desestacionalizada",
        "tratamiento_trimestral": "media de los meses del trimestre",
    },
    "CORALACBS": {
        "nombre": "Tasa de castigos — todos los préstamos, bancos comerciales",
        "unidad": "porcentaje",
        "frecuencia": "trimestral",
        "desestacionalizacion": "desestacionalizada",
        "tratamiento_trimestral": "dato de fin de periodo",
    },
    "USREC": {
        "nombre": "Indicador de recesión NBER para Estados Unidos",
        "unidad": "indicador (1 = recesión)",
        "frecuencia": "mensual",
        "desestacionalizacion": "sin desestacionalizar",
        "tratamiento_trimestral": "1 si algún mes del trimestre está en recesión",
    },
}

# --- Etiquetas de las columnas del panel (RNF-5) ---

COLUMN_LABELS: dict[str, str] = {
    # Morosidad (×5): nivel, diferencia trimestral y logit
    "dralacbs": "Tasa de morosidad — todos los préstamos (%)",
    "dralacbs_d": "Diferencia trimestral de la morosidad — todos los préstamos (pp)",
    "dralacbs_logit": "Logit de la morosidad — todos los préstamos",
    "dralacbn": "Tasa de morosidad sin desestacionalizar — todos los préstamos (%)",
    "dralacbn_d": "Diferencia trimestral de la morosidad sin desestacionalizar (pp)",
    "dralacbn_logit": "Logit de la morosidad sin desestacionalizar",
    "drclacbs": "Tasa de morosidad — tarjetas de crédito (%)",
    "drclacbs_d": "Diferencia trimestral de la morosidad — tarjetas de crédito (pp)",
    "drclacbs_logit": "Logit de la morosidad — tarjetas de crédito",
    "drblacbs": "Tasa de morosidad — préstamos empresariales (%)",
    "drblacbs_d": "Diferencia trimestral de la morosidad — préstamos empresariales (pp)",
    "drblacbs_logit": "Logit de la morosidad — préstamos empresariales",
    "drsreacbs": "Tasa de morosidad — préstamos inmobiliarios (%)",
    "drsreacbs_d": "Diferencia trimestral de la morosidad — préstamos inmobiliarios (pp)",
    "drsreacbs_logit": "Logit de la morosidad — préstamos inmobiliarios",
    # Variación interanual
    "gdpc1_yoy": "Variación interanual del PIB real (%)",
    "gdp_yoy": "Variación interanual del PIB nominal (%)",
    "cpiaucsl_yoy": "Variación interanual del IPC (%)",
    "loans_yoy": "Variación interanual de préstamos y arrendamientos (%)",
    # Nivel y diferencia trimestral
    "unrate": "Tasa de desempleo (%)",
    "unrate_d": "Diferencia trimestral de la tasa de desempleo (pp)",
    "fedfunds": "Tasa de fondos federales (%)",
    "fedfunds_d": "Diferencia trimestral de la tasa de fondos federales (pp)",
    # Otras
    "coralacbs": "Tasa de castigos — todos los préstamos (%)",
    "usrec": "Indicador de recesión NBER (1 = recesión)",
}
