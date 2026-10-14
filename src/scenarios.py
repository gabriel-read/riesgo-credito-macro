"""Pure parsing and transformations for pre-registered stress scenarios (005)."""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
import re

import numpy as np
import pandas as pd

from src.design import ModelDataError
from src.panel import yoy


FED_COLUMNS = (
    "Scenario Name", "Date", "Real GDP growth", "Nominal GDP growth",
    "Real disposable income growth", "Nominal disposable income growth",
    "Unemployment rate", "CPI inflation rate", "3-month Treasury rate",
    "5-year Treasury yield", "10-year Treasury yield", "BBB corporate yield",
    "Mortgage rate", "Prime rate", "Dow Jones Total Stock Market Index (Level)",
    "House Price Index (Level)", "Commercial Real Estate Price Index (Level)",
    "Market Volatility Index (Level)",
)
FED_VARIABLES = ("Real GDP growth", "CPI inflation rate", "Unemployment rate",
                 "3-month Treasury rate")


@dataclass(frozen=True)
class FedFileSpec:
    filename: str
    scenario: str
    historical: bool = False


FED_FILES = {
    "historico": FedFileSpec("2026_Final_Historic_Domestic.csv", "Actual", True),
    "base": FedFileSpec("2026_Final_Supervisory_Baseline_Domestic.csv", "Supervisory Baseline"),
    "severo": FedFileSpec("2026_Final_Supervisory_Severely_Adverse_Domestic.csv",
                          "Supervisory Severely Adverse"),
}


def parse_fed_csv(text: str, expected: FedFileSpec) -> pd.DataFrame:
    """Validate a Final Domestic CSV supplied as text; no filesystem/network."""
    try:
        frame = pd.read_csv(StringIO(text), dtype=str, keep_default_na=False)
    except (ValueError, pd.errors.ParserError) as exc:
        raise ModelDataError(f"{expected.filename}: CSV inválido") from exc
    if tuple(frame.columns) != FED_COLUMNS:
        missing = [c for c in FED_COLUMNS if c not in frame.columns]
        raise ModelDataError(f"{expected.filename}: cabeceras distintas, {missing}")
    if frame.empty or not frame["Scenario Name"].eq(expected.scenario).all():
        raise ModelDataError(f"{expected.filename}: escenario distinto de {expected.scenario}")
    quarters = []
    for label in frame["Date"]:
        if not re.fullmatch(r"\d{4} Q[1-4]", label):
            raise ModelDataError(f"{expected.filename}: trimestre inválido {label}")
        quarters.append(pd.Period(label.replace(" ", ""), freq="Q-DEC"))
    index = pd.PeriodIndex(quarters, freq="Q-DEC")
    if index.has_duplicates or not index.is_monotonic_increasing:
        raise ModelDataError(f"{expected.filename}: trimestre duplicado o desordenado")
    if expected.historical:
        if pd.Period("2025Q4") not in index:
            raise ModelDataError(f"{expected.filename}: falta trimestre 2025Q4")
    else:
        required = pd.period_range("2026Q1", "2029Q1", freq="Q-DEC")
        if not index.equals(required):
            missing = required.difference(index).astype(str).tolist()
            raise ModelDataError(f"{expected.filename}: trimestres distintos, faltan {missing}")
    result = pd.DataFrame(index=index)
    for column in FED_VARIABLES:
        values = pd.to_numeric(frame[column], errors="coerce").to_numpy(dtype=float)
        for position, value in enumerate(values):
            if (not expected.historical or index[position] == pd.Period("2025Q4")) and not np.isfinite(value):
                raise ModelDataError(f"{expected.filename}: {column} sin dato finito en {index[position]}")
        result[column] = values
    return result


def to_levels(adapted: pd.DataFrame, gdpc1_obs: pd.Series, cpi_obs: pd.Series,
              unrate_origin: float, rate_origin: float) -> pd.DataFrame:
    """Link scenario rates to observed levels and use the approved log identities."""
    if adapted.empty or not adapted.index.equals(pd.period_range(adapted.index[0], adapted.index[-1], freq="Q-DEC")):
        raise ModelDataError("trayectoria: trimestres vacíos o incompletos")
    origin = adapted.index[0] - 1
    reference = adapted.attrs.get("reference")
    if reference is None:
        raise ModelDataError("trayectoria: falta referencia de desempleo y tasa del paso 1")
    result = pd.DataFrame(index=adapted.index)
    for source, observed, level_name, reg_name in (
        ("Real GDP growth", gdpc1_obs, "gdpc1", "gdp_growth"),
        ("CPI inflation rate", cpi_obs, "cpiaucsl", "inflation"),
    ):
        history = observed.loc[observed.index <= origin].copy()
        rates = adapted[source].to_numpy(dtype=float)
        if origin not in history.index or not np.isfinite(history.to_numpy()).all() or (history <= 0).any():
            raise ModelDataError(f"{level_name}: nivel observado no positivo o ausente en {origin}")
        if not np.isfinite(rates).all() or (rates <= -100).any():
            raise ModelDataError(f"{source}: tasa no finita o menor o igual a -100")
        projected = pd.Series(np.exp(np.log(float(history.loc[origin])) + np.cumsum(np.log1p(rates / 100) / 4)),
                              index=adapted.index)
        joined = pd.concat([history, projected]).reindex(pd.period_range(history.index[0], adapted.index[-1], freq="Q-DEC"))
        reg = yoy(joined).loc[adapted.index]
        if not np.isfinite(reg.to_numpy()).all():
            bad = reg.index[~np.isfinite(reg.to_numpy())][0]
            raise ModelDataError(f"{level_name}: falta historia interanual para {bad}")
        result[level_name] = projected
        result[reg_name] = reg
    for source, anchor, level_name, reg_name in (
        ("Unemployment rate", unrate_origin, "unrate", "d_unemp"),
        ("3-month Treasury rate", rate_origin, "fedfunds", "d_ffr"),
    ):
        values = adapted[source].to_numpy(dtype=float)
        baseline = float(reference[source])
        if not np.isfinite(values).all() or not np.isfinite([baseline, anchor]).all():
            raise ModelDataError(f"{source}: referencia o valores no finitos")
        changes = np.diff(np.concatenate([[baseline], values]))
        result[reg_name] = changes
        result[level_name] = anchor + np.cumsum(changes)
    result.attrs["origin"] = origin
    return result


def build_regressors(levels: pd.DataFrame, panel_obs: pd.DataFrame,
                     reader_cols: dict | None = None, credit_rule: str = "last") -> pd.DataFrame:
    """Prepare contemporaneous scenario regressors; credit is already at lag four."""
    if credit_rule not in {"last", "zero", "mean"}:
        raise ModelDataError(f"crédito: regla desconocida {credit_rule}")
    if reader_cols:
        for mapping in reader_cols.values():
            column = mapping if isinstance(mapping, str) else mapping.get("column") if mapping else None
            if column and column not in panel_obs:
                raise ModelDataError(f"contrato: columna histórica ausente {column}")
    cutoff = pd.Period("2026Q2")
    # The approved sample starts in 2000; pre-sample YOY warmup contains NaN by construction.
    loan = panel_obs["loans_yoy"].loc[pd.Period("2000Q1"):cutoff]
    if loan.empty or not np.isfinite(loan.to_numpy(dtype=float)).all():
        raise ModelDataError("crédito: historia ausente o no finita")
    if cutoff not in loan.index:
        raise ModelDataError(f"crédito: falta origen del supuesto {cutoff}")
    fixed = {"last": float(loan.loc[cutoff]), "zero": 0.0,
             "mean": float(loan.loc[pd.Period("2000Q1"):cutoff].mean())}[credit_rule]
    result = levels[["gdp_growth", "d_unemp", "inflation", "d_ffr"]].copy()
    values, observed = [], []
    for quarter in result.index:
        source = quarter - 4
        if source <= cutoff:
            if source not in loan.index:
                raise ModelDataError(f"crédito: falta trimestre {source} para {quarter}")
            values.append(float(loan.loc[source]))
            observed.append(True)
        else:
            values.append(fixed)
            observed.append(False)
    result["credit_growth"] = values
    result["credit_observed"] = observed
    result.attrs["credit_rule"] = credit_rule
    return result


def adapt_calendar(fed: pd.DataFrame, hist_2025q4: pd.Series,
                   origin: pd.Period, mode: str) -> pd.DataFrame:
    """Keep values and map each approved calendar branch explicitly."""
    required = pd.period_range("2026Q1", "2029Q1", freq="Q-DEC")
    if not fed.index.equals(required):
        raise ModelDataError("Fed: se requieren los 13 trimestres de 2026Q1 a 2029Q1")
    if mode == "adapted":
        if origin != pd.Period("2026Q2"):
            raise ModelDataError("adaptación: origen debe ser 2026Q2")
        result = fed.copy()
        reference = hist_2025q4
    elif mode == "post_2026q2":
        if origin != pd.Period("2026Q2"):
            raise ModelDataError("tramo posterior: origen debe ser 2026Q2")
        result = fed.loc[pd.Period("2026Q3"):].copy()
        reference = fed.loc[pd.Period("2026Q2")]
    elif mode == "from_2025q4":
        if origin != pd.Period("2025Q4"):
            raise ModelDataError("calendario original: origen debe ser 2025Q4")
        result = fed.copy()
        reference = hist_2025q4
    else:
        raise ModelDataError(f"calendario desconocido {mode}")
    result["fed_quarter"] = result.index.astype(str)
    result.index = pd.period_range(origin + 1, periods=len(result), freq="Q-DEC")
    result.attrs["reference"] = reference.copy()
    result.attrs["mode"] = mode
    return result


def scenario_d(severe_regs: pd.DataFrame, panel_obs: pd.DataFrame) -> pd.DataFrame:
    """D shares activity with severe; seven observed rate changes, then six zeros."""
    if len(severe_regs) != 13:
        raise ModelDataError("D: se requieren 13 pasos")
    episode = pd.period_range("2022Q1", "2023Q3", freq="Q-DEC")
    if not episode.isin(panel_obs.index).all():
        raise ModelDataError("D: falta trimestre del episodio 2022Q1–2023Q3")
    changes = panel_obs.loc[episode, "fedfunds_d"].to_numpy(dtype=float)
    if not np.isfinite(changes).all() or (changes < 0).any():
        raise ModelDataError("D: cambios de tasa no finitos o negativos en el episodio")
    result = severe_regs.copy()
    result["d_ffr"] = np.concatenate([changes, np.zeros(6)])
    return result
