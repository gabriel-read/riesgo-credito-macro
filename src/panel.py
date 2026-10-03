"""Construcción del panel trimestral (spec 001).

Funciones puras: validación de la descarga, agregación trimestral, completitud,
último trimestre común, transformaciones, recorte y control de faltantes.
Sin acceso a red, disco ni gráficos (RNF-6). RF-7 a RF-16, RF-25.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import numpy as np
import pandas as pd

from src.config import (
    MAIN_SERIES,
    MONTHLY,
    DELINQUENCY,
    DOWNLOAD_START,
    SAMPLE_START,
    DOCUMENTED_GAP_SERIES,
    DOCUMENTED_GAP_MONTH,
)


# --- Excepciones ---

class DataError(ValueError):
    """Error de datos: faltante no documentado, valor inválido, cobertura insuficiente."""
    pass


# --- Utilidades ---

def _to_period_index_monthly(s: pd.Series) -> pd.Series:
    """Convierte índice a PeriodIndex mensual si no lo es."""
    if not isinstance(s.index, pd.PeriodIndex) or s.index.freq != "M":
        s = s.copy()
        s.index = pd.PeriodIndex(s.index, freq="M")
    return s


def _to_period_index_quarterly(s: pd.Series) -> pd.Series:
    """Convierte índice a PeriodIndex trimestral Q-DEC si no lo es."""
    if not isinstance(s.index, pd.PeriodIndex) or s.index.freq != "Q-DEC":
        s = s.copy()
        s.index = pd.PeriodIndex(s.index, freq="Q-DEC")
    return s


# --- RF-7: parse_raw ---

def parse_raw(raw: pd.DataFrame, series_id: str, start: str = DOWNLOAD_START) -> pd.Series:
    """Convierte el DataFrame crudo (texto) a Series numérica con PeriodIndex mensual/trimestral.

    - ".", "", "NaN" → NaN
    - Otro texto no numérico → DataError
    - 0 filas → DataError
    - Primera observación anterior a `start` → DataError
    """
    if raw.empty:
        raise DataError(f"{series_id}: descarga sin filas de datos")

    # Asegurar columnas esperadas
    if "date" not in raw.columns or series_id not in raw.columns:
        raise DataError(f"{series_id}: columnas inesperadas {list(raw.columns)}")

    # Convertir fecha a PeriodIndex
    try:
        dates = pd.to_datetime(raw["date"], format="%Y-%m-%d")
    except Exception as e:
        raise DataError(f"{series_id}: fechas inválidas") from e

    # Detectar frecuencia por inferencia del espaciado
    # Si las fechas están a ~3 meses → trimestral; ~1 mes → mensual
    diffs = dates.diff().dt.days.dropna()
    if len(diffs) == 0:
        freq = "M"
    else:
        median_days = diffs.median()
        freq = "Q-DEC" if median_days > 45 else "M"

    # Convertir valores: "." , "" , "NaN" → NaN; resto a float
    def to_float(x: str) -> float:
        if x in (".", "", "NaN"):
            return np.nan
        try:
            return float(x)
        except ValueError:
            raise DataError(f"{series_id}: valor no numérico '{x}'")

    values = raw[series_id].apply(to_float)

    # Construir Series con PeriodIndex
    if freq == "Q-DEC":
        periods = dates.dt.to_period("Q-DEC")
    else:
        periods = dates.dt.to_period("M")

    s = pd.Series(values.values, index=periods, name=series_id)
    s = s.sort_index()

    # Validar primera observación: debe ser <= start (cubrir desde start)
    if s.index[0] > pd.Period(start, freq=freq):
        raise DataError(
            f"{series_id}: primera observación {s.index[0]} posterior a {start}"
        )

    return s


# --- RF-8: Agregación trimestral ---

def quarter_months(monthly: pd.Series) -> pd.DataFrame:
    """Por trimestre calendario: n_meses, meses_faltantes, media SOLO si 3 meses."""
    monthly = _to_period_index_monthly(monthly)
    # Reindexar al rango completo para detectar trimestres incompletos
    full_range = pd.period_range(monthly.index[0], monthly.index[-1], freq="M")
    monthly = monthly.reindex(full_range)

    # Agrupar por trimestre: convertir cada mes a su trimestre
    quarterly_idx = monthly.index.asfreq("Q-DEC")
    result = pd.DataFrame(index=pd.PeriodIndex(sorted(quarterly_idx.unique()), freq="Q-DEC"))
    result["n_meses"] = 0
    result["meses_faltantes"] = 0
    result["media"] = np.nan

    for q in result.index:
        months_in_q = [m for m in full_range if m.asfreq("Q-DEC") == q]
        vals = monthly.loc[months_in_q]
        n_con_dato = vals.notna().sum()
        result.loc[q, "n_meses"] = n_con_dato
        result.loc[q, "meses_faltantes"] = len(months_in_q) - n_con_dato
        # SOLO media si 3 meses con dato (RF-13: nunca media de 1 o 2 meses en silencio)
        if n_con_dato == 3:
            result.loc[q, "media"] = vals.mean()

    return result


def quarterly_from_monthly(monthly: pd.Series, series_id: str) -> tuple[pd.Series, pd.Series, str | None]:
    """Agrega mensual a trimestral con regla de completitud y excepción 2025T4.

    Returns
    -------
    (value, complete, treatment)
        value: pd.Series trimestral (media de meses con dato, NaN si incompleto salvo RF-11)
        complete: pd.Series bool (True si trimestre completo: 3 meses o RF-11/RF-12)
        treatment: "RF-11" | "RF-12" | None para CPIAUCSL/UNRATE en 2025T4
    """
    monthly = _to_period_index_monthly(monthly)
    qm = quarter_months(monthly)

# Excepción documentada: octubre 2025 en CPIAUCSL y UNRATE
    is_documented = series_id in DOCUMENTED_GAP_SERIES
    gap_quarter = DOCUMENTED_GAP_MONTH.asfreq("Q-DEC")  # 2025Q4

    value = qm["media"].copy()
    complete = (qm["n_meses"] == 3).astype(bool)
    treatment = None

    if is_documented and gap_quarter in qm.index:
        row = qm.loc[gap_quarter]
        missing_months = row["meses_faltantes"]
        # Verificar si falta exactamente octubre 2025
        months_in_q = [m for m in monthly.index if m.asfreq("Q-DEC") == gap_quarter]
        oct_2025 = pd.Period("2025-10", "M")
        oct_missing = oct_2025 in months_in_q and pd.isna(monthly.get(oct_2025))

        if missing_months == 1 and oct_missing:
            # RF-11: falta solo octubre → media de nov y dic
            nov_2025 = pd.Period("2025-11", "M")
            dec_2025 = pd.Period("2025-12", "M")
            nov_val = monthly.get(nov_2025)
            dec_val = monthly.get(dec_2025)
            if pd.notna(nov_val) and pd.notna(dec_val):
                value.loc[gap_quarter] = (nov_val + dec_val) / 2
                complete.loc[gap_quarter] = True
                treatment = "RF-11"
        elif missing_months == 0:
            # RF-12: octubre presente (aunque sea NaN por otros motivos, los 3 meses existen)
            complete.loc[gap_quarter] = True
            treatment = "RF-12"

    return value, complete, treatment


def recession_indicator(usrec_monthly: pd.Series) -> pd.Series:
    """Indicador trimestral de recesión: 1 si algún mes del trimestre = 1, NaN si trimestre incompleto."""
    usrec_monthly = _to_period_index_monthly(usrec_monthly)
    qm = quarter_months(usrec_monthly)

    # Requiere 3 meses para decidir; si incompleto → NaN terminal (RF-25)
    value = pd.Series(index=qm.index, dtype=float)
    for q in qm.index:
        if qm.loc[q, "n_meses"] == 3:
            months_in_q = [m for m in usrec_monthly.index if m.asfreq("Q-DEC") == q]
            vals = usrec_monthly.loc[months_in_q]
            value.loc[q] = 1.0 if (vals == 1).any() else 0.0
        else:
            value.loc[q] = np.nan

    return value


def quarterly_from_quarterly(q: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Serie trimestal: se toma sin agregar (dato de fin de periodo)."""
    q = _to_period_index_quarterly(q)
    complete = q.notna()
    return q, complete


# --- RF-10, RF-13, RF-25: Último trimestre común y validaciones ---

def last_common_quarter(complete: dict[str, pd.Series], series: list[str]) -> pd.Period:
    """Último trimestre donde todas las `series` tienen `complete == True`."""
    # Intersección de índices
    all_quarters = None
    for sid in series:
        c = complete[sid]
        if all_quarters is None:
            all_quarters = c.index[c].tolist()
        else:
            all_quarters = [q for q in all_quarters if q in c.index[c].tolist()]

    if not all_quarters:
        raise DataError("Ningún trimestre común completo entre las series principales")

    return max(all_quarters)


def check_main_complete(
    complete: dict[str, pd.Series],
    start: pd.Period,
    end: pd.Period,
) -> None:
    """Verifica que no haya huecos en series principales desde `start` hasta `end` (inclusive).

    Raises DataError nombrando la serie y el primer trimestre con hueco.
    """
    for sid in MAIN_SERIES:
        c = complete[sid]
        # Reindexar al rango completo start..end
        full_idx = pd.period_range(start, end, freq="Q-DEC")
        c_full = c.reindex(full_idx, fill_value=False)
        gaps = c_full[~c_full].index
        if len(gaps) > 0:
            first_gap = gaps[0]
            raise DataError(f"{sid}: falta dato en {first_gap}")


def check_terminal_only(
    values: pd.Series,
    name: str,
    start: pd.Period,
    end: pd.Period,
) -> pd.Period | None:
    """Para series de robustez y USREC: solo faltante terminal permitido (RF-25).

    Returns
    -------
    Último trimestre con dato (pd.Period) o None si no hay faltante terminal.
    Raises DataError si hay NaN interior.
    """
    full_idx = pd.period_range(start, end, freq="Q-DEC")
    v = values.reindex(full_idx)

    # Encontrar NaN interiores (antes del último valor no-NaN)
    last_valid_idx = v.last_valid_index()
    if last_valid_idx is None:
        # Todo NaN - no debería pasar si la serie tiene algún dato
        return None

    # Verificar NaN entre start y last_valid_idx (excluyendo el último)
    interior = v.loc[start:last_valid_idx]
    nan_interior = interior[interior.isna()].index
    if len(nan_interior) > 0:
        first_nan = nan_interior[0]
        raise DataError(f"{name}: falta dato interior en {first_nan}")

    # Faltante terminal: desde last_valid_idx + 1 hasta end
    if last_valid_idx < end:
        return last_valid_idx

    return None


# --- RF-9: Transformaciones (sobre historia completa desde 1998) ---

def yoy(x: pd.Series) -> pd.Series:
    """Variación interanual: 100 * (ln x_t - ln x_{t-4}).

    Usa shift(4) sobre PeriodIndex, así que t-4 es exacto aunque falte una fila.
    """
    x = x.copy()
    if not isinstance(x.index, pd.PeriodIndex) or x.index.freq != "Q-DEC":
        x.index = pd.PeriodIndex(x.index, freq="Q-DEC")
    return 100 * (np.log(x) - np.log(x.shift(4)))


def diff_pp(x: pd.Series) -> pd.Series:
    """Diferencia trimestral en puntos porcentuales: x_t - x_{t-1}."""
    return x.diff()


def logit_rate(dr: pd.Series, series_id: str) -> pd.Series:
    """Logit de la morosidad: ln(DR / (100 - DR)), DR en porcentaje.

    Raises DataError si DR <= 0 o DR >= 100.
    """
    if (dr <= 0).any() or (dr >= 100).any():
        bad = dr[(dr <= 0) | (dr >= 100)]
        q = bad.index[0]
        raise DataError(f"{series_id}: morosidad fuera de (0,100) en {q} (valor={bad.iloc[0]})")
    return np.log(dr / (100 - dr))


def transform(quarterly: pd.DataFrame) -> pd.DataFrame:
    """Calcula todas las transformaciones de RF-9 sobre la historia completa (desde 1998).

    columns de entrada: series originales con nombres FRED (mayúsculas).
    columns de salida: 25 variables del panel en minúsculas.
    """
    out = pd.DataFrame(index=quarterly.index)

    # Morosidad (×5): nivel, diferencia trimestral pp, logit
    for sid in DELINQUENCY:
        col = sid.lower()
        level = quarterly[sid]
        out[col] = level
        out[f"{col}_d"] = diff_pp(level)
        out[f"{col}_logit"] = logit_rate(level, sid)

    # Variación interanual
    out["gdpc1_yoy"] = yoy(quarterly["GDPC1"])
    out["gdp_yoy"] = yoy(quarterly["GDP"])
    out["cpiaucsl_yoy"] = yoy(quarterly["CPIAUCSL"])
    out["loans_yoy"] = yoy(quarterly["LOANS"])

    # Nivel y diferencia trimestral
    out["unrate"] = quarterly["UNRATE"]
    out["unrate_d"] = diff_pp(quarterly["UNRATE"])
    out["fedfunds"] = quarterly["FEDFUNDS"]
    out["fedfunds_d"] = diff_pp(quarterly["FEDFUNDS"])

    # Otras
    out["coralacbs"] = quarterly["CORALACBS"]
    out["usrec"] = quarterly["USREC"]

    return out


# --- RF-16: PanelResult ---

@dataclass(frozen=True)
class PanelResult:
    full: pd.DataFrame              # Transformaciones sobre toda la historia (1998+)
    panel: pd.DataFrame             # Panel recortado 2000T1–fin
    end: pd.Period                  # Último trimestre común
    excluded_tail: list[tuple[pd.Period, str, str]]  # (trimestre, serie, motivo)
    gap_treatment: dict[str, str]   # {serie: "RF-11" | "RF-12"} para CPI/UNRATE
    terminal_gaps: dict[str, pd.Period]  # {columna: último trimestre con dato} RF-25
    observed: dict[str, tuple[pd.Period, pd.Period, int]]  # {serie: (primera, última, n)}


# --- Build panel ---

def build_panel(raw: dict[str, pd.DataFrame]) -> PanelResult:
    """Construye el panel completo desde las descargas crudas."""
    # 1) Parsear cada serie cruda
    parsed: dict[str, pd.Series] = {}
    for sid, df in raw.items():
        parsed[sid] = parse_raw(df, sid)

    # 2) Agregar mensuales a trimestral (salvo USREC que es especial)
    quarterly_dict: dict[str, pd.Series] = {}
    complete_dict: dict[str, pd.Series] = {}
    gap_treatment: dict[str, str] = {}

    for sid in MONTHLY:
        if sid == "USREC":
            continue
        val, comp, trat = quarterly_from_monthly(parsed[sid], sid)
        quarterly_dict[sid] = val
        complete_dict[sid] = comp
        if trat:
            gap_treatment[sid] = trat

    # Trimestrales (fin de periodo)
    for sid in MAIN_SERIES + ["CORALACBS", "DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS"]:
        if sid not in quarterly_dict:
            val, comp = quarterly_from_quarterly(parsed[sid])
            quarterly_dict[sid] = val
            complete_dict[sid] = comp

    # USREC
    quarterly_dict["USREC"] = recession_indicator(parsed["USREC"])
    complete_dict["USREC"] = quarterly_dict["USREC"].notna()

    # 3) Último trimestre común (solo MAIN_SERIES)
    end = last_common_quarter(complete_dict, MAIN_SERIES)

    # 4) Trimestres excluidos (cola) con motivo
    max_quarter = max(max(c.index[c].max() for c in complete_dict.values() if c.any()), end)
    excluded_tail = []
    for q in pd.period_range(end + 1, max_quarter, freq="Q-DEC"):
        for sid in MAIN_SERIES:
            c = complete_dict[sid]
            if q not in c.index or not c.loc[q]:
                motivo = "incompleto" if q in c.index and not c.loc[q] else "sin dato"
                excluded_tail.append((q, sid, motivo))

    # 5) Validar completitud principales 1998..end (RF-13)
    # check_main_complete usa start=1998Q1, pero necesitamos start=1998Q1 para yoy
    check_main_complete(complete_dict, pd.Period("1998Q1", "Q-DEC"), end)

    # 6) Construir DataFrame trimestral completo (1998Q1..max) y transformar
    # Reindexar al rango completo ANTES de transformar (para que shift(4) funcione)
    full_range = pd.period_range(pd.Period("1998Q1", "Q-DEC"), max(quarterly_dict[sid].index.max() for sid in quarterly_dict))
    quarterly_full = pd.DataFrame(index=full_range)
    for sid, s in quarterly_dict.items():
        quarterly_full[sid] = s.reindex(full_range)

    full = transform(quarterly_full)

    # 7) Recortar a muestra de estimación 2000T1..end (RF-10)
    panel = full.loc[SAMPLE_START:end].copy()

    # 8) Validar NaN en columnas principales del panel (cobertura 2000T1)
    for col in panel.columns:
        if col == "usrec":
            continue
        if panel[col].isna().any():
            first_nan = panel[col].isna().idxmax()
            raise DataError(f"{col}: NaN en panel en {first_nan}")

    # 9) Validar series de robustez y USREC: solo faltante terminal (RF-25)
    terminal_gaps = {}
    robustness_cols = [c for c in panel.columns if c not in ["usrec"] and not c.endswith("_d") and not c.endswith("_logit") and not c.endswith("_yoy")]
    # Las series de robustez en el panel: dralacbn, drclacbs, drblacbs, drsreacbs, coralacbs
    for col in ["dralacbn", "drclacbs", "drblacbs", "drsreacbs", "coralacbs", "usrec"]:
        if col in panel.columns:
            last = check_terminal_only(panel[col], col.upper(), SAMPLE_START, end)
            if last is not None:
                terminal_gaps[col] = last

    # 10) Observed info
    observed = {}
    for sid, s in parsed.items():
        first = s.first_valid_index()
        last = s.last_valid_index()
        n = s.notna().sum()
        observed[sid] = (first, last, int(n))

    return PanelResult(
        full=full,
        panel=panel,
        end=end,
        excluded_tail=excluded_tail,
        gap_treatment=gap_treatment,
        terminal_gaps=terminal_gaps,
        observed=observed,
    )