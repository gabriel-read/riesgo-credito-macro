"""Funciones puras de diseño del Modelo II (spec 004).

Columnas con rezagos, muestra común M, trimestres de tasa cero, diseño del modelo de rezagos
distribuidos y de las proyecciones locales, y rezagos que salen de trimestres excluidos.
Sin acceso a red, disco ni gráficos (RNF-7). RF-1 a RF-5, RF-14 a RF-16, RF-22 a RF-25.
"""

from __future__ import annotations

import pandas as pd

from src.design import Design, ModelDataError, dependent_series
from src.model2_config import (
    CONTROLS,
    COVID_NAMES,
    COVID_QUARTERS,
    K_MAX,
    ZERO_RATE_MAX,
    Spec2,
    dffr_cols,
)

_FORM = "primera diferencia"


def _period(q: str | pd.Period) -> pd.Period:
    return q if isinstance(q, pd.Period) else pd.Period(q, "Q-DEC")


def _reindexed(full: pd.DataFrame) -> pd.DataFrame:
    """Historia sobre el índice trimestral completo: un trimestre ausente reaparece como fila con NaN."""
    return full.reindex(pd.period_range(full.index.min(), full.index.max(), freq="Q-DEC"))


def build_columns(full: pd.DataFrame, decision: str) -> pd.DataFrame:
    """Todas las columnas del modelo sobre la historia reindexada sin huecos (RF-1).

    y (ΔDR según la decisión), y_lag, ΔFFR(t−j) con j = 0..8 y los cuatro controles rezagados. Los
    rezagos son de verdad t−j porque se calculan sobre el índice trimestral completo. No se elimina ninguna fila.
    """
    full = _reindexed(full)
    cols = pd.DataFrame(index=full.index)
    cols["y"] = dependent_series(full, "dralacbs", decision)
    cols["y_lag"] = cols["y"].shift(1)
    for j in range(K_MAX + 1):
        cols[f"d_ffr_l{j}"] = full["fedfunds_d"].shift(j)
    for term, (column, lag) in CONTROLS.items():
        cols[term] = full[column].shift(lag)
    return cols


def common_window(cols: pd.DataFrame, end: pd.Period) -> tuple[pd.Period, pd.Period]:
    """Muestra efectiva común M: del primer trimestre con TODAS las columnas (K = 8) hasta `end`."""
    complete = cols.loc[:end].notna().all(axis=1)
    if not complete.any():
        raise ModelDataError("ningún trimestre tiene todos los términos del Modelo II")
    return complete.index[complete.to_numpy().argmax()], end


def zero_rate_quarters(full: pd.DataFrame, start: pd.Period, end: pd.Period) -> list[pd.Period]:
    """Trimestres de [start, end] con promedio trimestral de la tasa ≤ ZERO_RATE_MAX (R3)."""
    rate = full["fedfunds"].loc[start:end]
    return [q for q, v in rate.items() if bool(v <= ZERO_RATE_MAX)]


def _covid_dummies(index: pd.PeriodIndex) -> pd.DataFrame:
    return pd.DataFrame(
        {name: (index == _period(q)).astype(float) for name, q in zip(COVID_NAMES, COVID_QUARTERS)},
        index=index,
    )


def _check_nan(frame: pd.DataFrame, regression: str) -> None:
    """RF-4: un faltante dentro de la muestra detiene el cálculo con variable, trimestre y regresión."""
    bad = frame.isna()
    if bad.to_numpy().any():
        first = int(bad.any(axis=1).to_numpy().argmax())
        name = frame.columns[int(bad.iloc[first].to_numpy().argmax())]
        raise ModelDataError(f"{name}: NaN en {frame.index[first]} (regresión {regression})")


def build_design2(full: pd.DataFrame, spec: Spec2, K: int, decision: str,
                  window: tuple[pd.Period, pd.Period], end: pd.Period) -> Design:
    """Diseño del modelo de rezagos distribuidos con K rezagos de ΔFFR (RF-1, RF-4, RF-22, RF-23).

    Columnas: const, y_lag, ΔFFR(t..t−K), los cuatro controles y las cuatro dummies COVID. Recorta a
    `window` y quita las exclusiones de `spec` (rango de R2, tramos de tasa cero de R3). Las dummies
    se omiten, y se anotan en `Design.dropped`, solo si la variante no las lleva (R2 y R3); una dummy
    sin variación en cualquier otra variante es un error.
    """
    cols = build_columns(full, decision)
    start, last = window
    frame = cols.loc[start:last]
    if spec.exclude_range:
        first_ex, last_ex = (_period(q) for q in spec.exclude_range)
        frame = frame[(frame.index < first_ex) | (frame.index > last_ex)]
    if spec.exclude_zero_rate:
        zero = set(zero_rate_quarters(_reindexed(full), start, last))
        frame = frame[[q not in zero for q in frame.index]]
    x_cols = ["y_lag", *dffr_cols(K), *CONTROLS]
    _check_nan(frame[["y", *x_cols]], f"{spec.id}, K = {K}")
    X = frame[x_cols].copy()
    X.insert(0, "const", 1.0)
    dropped: list[str] = []
    if spec.covid_dummies:
        dummies = _covid_dummies(frame.index)
        for name in COVID_NAMES:
            if dummies[name].sum() == 0:
                raise ModelDataError(f"{name}: sin variación en la muestra (regresión {spec.id})")
        X = pd.concat([X, dummies], axis=1)
    else:
        dropped = list(COVID_NAMES)
    return Design(y=frame["y"].copy(), X=X, form=_FORM, start=start, end=last,
                  spec_id=spec.id, dropped=dropped)


_LAG_OF_TERM = {"y_lag": 1, **{c: lag for c, (_, lag) in CONTROLS.items()}}


def _lag_of(term: str) -> int:
    if term.startswith("d_ffr_l"):
        return int(term.removeprefix("d_ffr_l"))
    return _LAG_OF_TERM[term]


def lagged_from_excluded(design: Design, K: int, excluded: set[pd.Period],
                         terms: tuple[str, ...] | None = None) -> list[pd.Period]:
    """Trimestres de la muestra con algún regresor rezagado que sale de un trimestre excluido (RF-24).

    `terms` por defecto: y_lag, ΔFFR(t−1..t−K) y los controles. Los términos contemporáneos no
    cuentan (t pertenece a la muestra).
    """
    if terms is None:
        terms = ("y_lag", *dffr_cols(K)[1:], *CONTROLS)
    lags = [_lag_of(t) for t in terms]
    return sorted(q for q in design.X.index if any((q - lag) in excluded for lag in lags))


def covid_lag_leaks(design: Design, K: int) -> list[pd.Period]:
    """Trimestres cuyos rezagos de ΔDR o ΔFFR salen de 2020T2–2021T1 (RF-25).

    Solo y_lag y ΔFFR(t−1..t−K): los efectos base de los controles ya son limitaciones fijas y se
    contarían dos veces.
    """
    excluded = {_period(q) for q in COVID_QUARTERS}
    return lagged_from_excluded(design, K, excluded, terms=("y_lag", *dffr_cols(K)[1:]))


def build_lp_design(full: pd.DataFrame, h: int, K: int, decision: str,
                    window: tuple[pd.Period, pd.Period], end: pd.Period, target: str) -> Design:
    """Diseño de la proyección local de horizonte h (RF-14 a RF-16).

    target "morosidad": y = DR(t+h) − DR(t−1); target "tasa": y = FFR(t+h) − FFR(t−1). X: const,
    ΔFFR(t), y_lag, controles, ΔFFR(t−1..t−K) y dummies COVID fechadas en t. La muestra va de
    window[0] a end − h: nunca se usan datos posteriores a `end`.
    """
    if target not in ("morosidad", "tasa"):
        raise ValueError(f"target desconocido: {target!r}")
    full = _reindexed(full)
    cols = build_columns(full, decision)
    level = full["dralacbs"] if target == "morosidad" else full["fedfunds"]
    last = end - h
    y = (level.shift(-h) - level.shift(1)).loc[window[0]:last].rename("y")
    names = ["d_ffr_l0", "y_lag", *CONTROLS, *dffr_cols(K)[1:]]
    X = cols.loc[window[0]:last, names].copy()
    _check_nan(pd.concat([y, X], axis=1), f"proyección local {target}, h = {h}")
    X.insert(0, "const", 1.0)
    dummies = _covid_dummies(X.index)
    for name in COVID_NAMES:
        if dummies[name].sum() == 0:
            raise ModelDataError(f"{name}: sin variación en la muestra (proyección local, h = {h})")
    X = pd.concat([X, dummies], axis=1)
    return Design(y=y, X=X, form=_FORM, start=window[0], end=last,
                  spec_id=f"lp_{target}_h{h}", dropped=[])
