"""Funciones puras de diseño del Modelo I (spec 003).

Construye la matriz de diseño (X) y la variable dependiente (y) a partir
de la historia transformada y la tabla de estacionariedad.
Sin acceso a red, disco ni gráficos (RNF-6). RF-1 a RF-6, RF-15.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from src.model1_config import (
    COVID_QUARTERS,
    MACRO_TERMS,
    CREDIT_LAG,
    VariantSpec,
)
from src.stationarity import decide, is_stationary


# --- Excepciones ---


class ModelDataError(ValueError):
    """Error de datos del modelo: faltante, forma inesperada, dummy sin variación."""
    pass


# --- Dataclass de diseño ---


@dataclass(frozen=True)
class Design:
    """Matriz de diseño y variable dependiente listas para estimar."""

    y: pd.Series
    X: pd.DataFrame
    form: str                          # "nivel" | "primera diferencia"
    start: pd.Period
    end: pd.Period
    spec_id: str
    dropped: list[str] = field(default_factory=list)  # dummies omitidas por no tener variación


# --- Funciones puras ---


def read_decisions(stationarity: pd.DataFrame) -> dict[str, str]:
    """Lee las decisiones de estacionariedad de la tabla (RF-3).

    Parámetros
    ----------
    stationarity : DataFrame con columnas 'variable' y 'decision'
        (producido por src.stationarity.stationarity_table)

    Returns
    -------
    dict[str, str]
        {columna: decision} de las filas "tal cual"
    """
    tal_cual = stationarity[stationarity["forma"] == "tal cual"]
    decisions: dict[str, str] = {}
    for _, row in tal_cual.iterrows():
        decisions[row["variable"]] = row["decision"]
    return decisions


def check_expected_forms(decisions: dict[str, str], expected: dict[str, str]) -> None:
    """Verifica que las decisiones coincidan con las formas esperadas (RF-4).

    Raises
    ------
    ModelDataError
        Si una forma esperada difiere de la tabla o falta la variable.
    """
    for var, expected_form in expected.items():
        if var not in decisions:
            raise ModelDataError(
                f"{var}: forma esperada '{expected_form}' pero la variable no aparece "
                f"en la tabla de estacionariedad; exige /sdd-change"
            )
        actual = decisions[var]
        if actual != expected_form:
            raise ModelDataError(
                f"{var}: forma esperada '{expected_form}' pero la tabla dice '{actual}'; "
                f"exige /sdd-change"
            )


def diff_form_stationary(stationarity: pd.DataFrame, column: str) -> tuple[str, str]:
    """Aplica la regla de estacionariedad a la fila "primera diferencia" (RF-15).

    Se usa para ΔU, ΔFFR y para la dependiente y su rezago cuando entran en Δ.

    Returns
    -------
    tuple[str, str]
        (decision, forma) donde forma es "primera diferencia"
    """
    row = stationarity[
        (stationarity["variable"] == column) & (stationarity["forma"] == "primera diferencia")
    ]
    if row.empty:
        raise ModelDataError(f"{column}: no hay fila 'primera diferencia' en la tabla")
    r = row.iloc[0]
    adf_p = r["adf_p"]
    kpss_p = r["kpss_p"]
    decision = decide(adf_p, kpss_p)
    return decision, "primera diferencia"


def dependent_series(full: pd.DataFrame, column: str, decision: str) -> pd.Series:
    """Construye la serie de la dependiente según la decisión (RF-1, RF-3).

    - "niveles": la columna tal cual
    - "primera diferencia" o "ambigua (primera diferencia)": diff sobre la
      historia reindexada (no la columna _d, para que el logit, que no tiene
      columna _d, siga la misma regla)

    Parámetros
    ----------
    full : DataFrame con transformaciones sobre historia completa (1998+)
    column : nombre de la columna dependiente
    decision : decisión de estacionariedad ("niveles" | "primera diferencia" |
                "ambigua (primera diferencia)")

    Returns
    -------
    pd.Series
        Serie de la dependiente en la forma correspondiente
    """
    if decision == "niveles":
        return full[column].copy()
    # "primera diferencia" o "ambigua (primera diferencia)"
    return full[column].diff()


def _panel_column(term: str, spec: VariantSpec) -> str:
    """Columna del panel de un término macro en una variante.

    Es la de MACRO_TERMS, salvo el PIB, que cada variante elige con spec.gdp_column
    (R4 usa la variación interanual del GDP nominal en lugar de la del GDPC1).
    """
    if term == "gdp_growth":
        return spec.gdp_column
    return MACRO_TERMS[term]


def _cols_for_lag_check(frame: pd.DataFrame, spec: VariantSpec) -> list[pd.Series]:
    """Series de la historia necesarias para el primer trimestre válido.

    Incluye la dependiente y los términos macro. Para credit_growth, aplica
    el rezago de la variante (spec.credit_lag) para que el primer trimestre
    válido considere cuándo estará disponible el término rezagado.

    Parámetros
    ----------
    frame : DataFrame con todas las columnas necesarias ya construidas
    spec : especificación de la variante

    Returns
    -------
    list[pd.Series]
        Series alineadas al índice de frame, con el rezago aplicado donde corresponda
    """
    cols = [frame[spec.dependent]]
    for term in MACRO_TERMS:
        col = _panel_column(term, spec)
        if term == "credit_growth":
            cols.append(frame[col].shift(spec.credit_lag))
        else:
            cols.append(frame[col])
    return cols


def effective_window(
    frame: pd.DataFrame,
    spec: VariantSpec,
    end: pd.Period,
) -> tuple[pd.Period, pd.Period]:
    """Calcula la ventana efectiva de estimación (RF-1, RF-5).

    - El inicio es spec.start si truncate_start=False. Si es True, es el máximo
      entre spec.start y el primer trimestre con todos los términos (incluyendo
      el rezago de credit_growth).
    - El fin es end. Solo para una dependiente alternativa (spec.dependent !=
      "dralacbs") que termine antes por el faltante terminal de la 001, es su
      último trimestre con dato. En la principal y en las variantes con
      DRALACBS, un faltante al final es un NaN más y dispara el error del
      paso 4 de build_design (RF-1: 2000T1–2026T2 estricta).

    Parámetros
    ----------
    frame : DataFrame con todas las columnas necesarias ya construidas
    spec : especificación de la variante
    end : último trimestre común del panel

    Returns
    -------
    tuple[pd.Period, pd.Period]
        (inicio, fin) de la ventana efectiva
    """
    # Determinar el inicio
    if spec.truncate_start:
        # Primer trimestre con todos los términos disponibles (con rezago)
        needed_cols = _cols_for_lag_check(frame, spec)
        complete = pd.concat(needed_cols, axis=1).notna().all(axis=1)
        if not complete.any():
            raise ModelDataError(
                f"ningún trimestre tiene todos los términos de la variante {spec.id}"
            )
        first_valid = complete.index[complete.to_numpy().argmax()]  # primer trimestre completo
        start = max(spec.start, first_valid)
    else:
        start = spec.start

    # Determinar el fin
    if spec.dependent != "dralacbs":
        # Dependiente alternativa: último trimestre con dato
        dep_series = frame[spec.dependent]
        last_valid = dep_series.last_valid_index()
        if last_valid is not None and last_valid < end:
            end = last_valid

    return start, end


def build_design(
    full: pd.DataFrame,
    spec: VariantSpec,
    decision: str,
    end: pd.Period,
) -> Design:
    """Construye la matriz de diseño y la variable dependiente (RF-1 a RF-6).

    Algoritmo:
    1. Construye todas las columnas sobre full completo, desde 1998 y reindexado
       sin huecos. Así shift(1) y shift(k) son de verdad t−1 y t−k.
    2. Calcula la ventana con effective_window.
    3. Recorta a la ventana y quita el rango (inicio, fin), inclusivo, de spec.exclude.
    4. Si queda cualquier NaN, lanza ModelDataError(variable, trimestre, spec.id).
    5. Cada dummy COVID vale 1 en su trimestre. Las estacionales son de T2, T3
       y T4, con T1 como base. Una dummy sin variación en la muestra se omite
       y se anota en dropped, solo si la variante es R1 o el tramo de
       estimación fuera de muestra. En cualquier otra variante, una dummy sin
       variación lanza ModelDataError.

    Parámetros
    ----------
    full : DataFrame con transformaciones sobre historia completa (1998+)
    spec : especificación de la variante
    decision : decisión de estacionariedad de la dependiente
    end : último trimestre común del panel

    Returns
    -------
    Design
        Matriz de diseño y variable dependiente listas para estimar
    """
    # Paso 1: construir todas las columnas sobre full completo
    work = pd.DataFrame(index=full.index)

    # Dependiente
    work["y"] = dependent_series(full, spec.dependent, decision)

    # y_lag: rezago de la dependiente
    work["y_lag"] = work["y"].shift(1)

    # Términos macro
    for term in MACRO_TERMS:
        col = _panel_column(term, spec)
        if term == "credit_growth":
            work[term] = full[col].shift(spec.credit_lag)
        else:
            work[term] = full[col]

    # Dummies COVID (pandas Series con índice para .loc posterior)
    covid_dummies: dict[str, pd.Series] = {}
    if spec.covid_dummies:
        for q_str in COVID_QUARTERS:
            q = pd.Period(q_str, "Q-DEC")
            dummy_name = f"covid_{q_str.lower().replace('q', 'q')}"
            covid_dummies[dummy_name] = pd.Series(
                (work.index == q).astype(float), index=work.index
            )

    # Dummies estacionales (T2, T3, T4; T1 es base)
    seasonal_dummies: dict[str, pd.Series] = {}
    if spec.seasonal_dummies:
        for qtr in [2, 3, 4]:
            dummy_name = f"seasonal_q{qtr}"
            seasonal_dummies[dummy_name] = pd.Series(
                (work.index.quarter == qtr).astype(float), index=work.index
            )

    # Paso 2: calcular ventana efectiva (con full para acceso a columnas originales)
    start, eff_end = effective_window(full, spec, end)

    # Paso 3: recortar a la ventana y quitar exclusiones
    window = work.loc[start:eff_end].copy()
    if spec.exclude:
        ex_start, ex_end = (pd.Period(q, "Q-DEC") for q in spec.exclude)
        window = window[(window.index < ex_start) | (window.index > ex_end)]

    # Paso 4: verificar NaN
    all_cols = ["y", "y_lag"] + list(MACRO_TERMS.keys())
    for col in all_cols:
        if col in window.columns:
            nan_mask = window[col].isna()
            if nan_mask.any():
                first_nan_q = window.index[nan_mask][0]
                # Traducir nombre de término a columna para el mensaje
                col_label = _panel_column(col, spec) if col in MACRO_TERMS else col
                raise ModelDataError(
                    f"{col_label}: NaN en {first_nan_q} (variante {spec.id})"
                )

    # Paso 5: construir X con orden fijo
    X_cols: list[str] = ["const", "y_lag"] + list(MACRO_TERMS.keys())

    # Añadir dummies COVID
    dropped: list[str] = []
    for dummy_name, dummy_series in covid_dummies.items():
        dummy_in_window = dummy_series.loc[window.index]
        if dummy_in_window.sum() == 0:
            # Dummy sin variación en la muestra
            if spec.id == "R1" or spec.id == "oos":
                dropped.append(dummy_name)
            else:
                raise ModelDataError(
                    f"{dummy_name}: sin variación en la muestra (variante {spec.id})"
                )
        else:
            X_cols.append(dummy_name)

    # Añadir dummies estacionales
    for dummy_name, dummy_series in seasonal_dummies.items():
        dummy_in_window = dummy_series.loc[window.index]
        if dummy_in_window.sum() == 0:
            if spec.id == "R1" or spec.id == "oos":
                dropped.append(dummy_name)
            else:
                raise ModelDataError(
                    f"{dummy_name}: sin variación en la muestra (variante {spec.id})"
                )
        else:
            X_cols.append(dummy_name)

    # Construir X
    X = pd.DataFrame(index=window.index)
    X["const"] = 1.0
    for col in X_cols[1:]:  # saltar "const" que ya está
        if col in MACRO_TERMS:
            X[col] = window[col]
        elif col in covid_dummies:
            X[col] = covid_dummies[col].loc[window.index]
        elif col in seasonal_dummies:
            X[col] = seasonal_dummies[col].loc[window.index]
        else:
            X[col] = window[col]

    # Determinar la forma
    if decision == "niveles":
        form = "nivel"
    else:
        form = "primera diferencia"

    return Design(
        y=window["y"],
        X=X,
        form=form,
        start=start,
        end=eff_end,
        spec_id=spec.id,
        dropped=dropped,
    )
