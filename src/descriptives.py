"""Tabla de estadísticos descriptivos (spec 001).

Función pura: n, media, desv. est. (ddof=1), mín., mediana, máx.
Sin acceso a red, disco ni gráficos (RNF-6). RF-18.
"""

from __future__ import annotations

import pandas as pd


def descriptive_table(panel: pd.DataFrame, exclude: tuple[str, ...] = ("usrec",)) -> pd.DataFrame:
    """Calcula estadísticos descriptivos por variable del panel.

    Parámetros
    ----------
    panel : DataFrame
        Panel de estimación (2000T1..end).
    exclude : tuple, opcional
        Columnas a excluir (por defecto "usrec").

    Returns
    -------
    DataFrame
        Índice = nombre de variable; columnas = n, media, desv_est, min, mediana, max.
    """
    cols = [c for c in panel.columns if c not in exclude]
    data = []
    for col in cols:
        s = panel[col].dropna()
        data.append({
            "variable": col,
            "n": int(len(s)),
            "media": float(s.mean()) if len(s) > 0 else float("nan"),
            "desv_est": float(s.std(ddof=1)) if len(s) > 1 else float("nan"),
            "min": float(s.min()) if len(s) > 0 else float("nan"),
            "mediana": float(s.median()) if len(s) > 0 else float("nan"),
            "max": float(s.max()) if len(s) > 0 else float("nan"),
        })
    return pd.DataFrame(data).set_index("variable")