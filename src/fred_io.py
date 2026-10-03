"""E/S de FRED: descarga, guardado crudo, manifiesto y lectura (spec 001).

Único módulo con acceso a red y disco de datos (RNF-6). RF-1 a RF-6, RF-24.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Callable

import pandas as pd

from src.config import ALL_SERIES, DOWNLOAD_START


# --- Excepciones ---

class DownloadError(RuntimeError):
    """Error en la descarga de una serie (primaria y respaldo)."""
    pass


class DuplicateDownloadError(FileExistsError):
    """Ya existe una descarga de esa serie con la fecha de hoy."""
    pass


# --- Descarga ---

def fetch_primary(series_id: str, start: str) -> str:
    """Descarga vía ``pandas_datareader`` y devuelve CSV como texto.

    Parámetros
    ----------
    series_id : str
        Código de la serie en FRED (p. ej. ``"DRALACBS"``).
    start : str
        Fecha de inicio en formato ``"YYYY-MM-DD"``.

    Returns
    -------
    str
        Texto CSV con cabecera ``date,<series_id>``.

    Raises
    ------
    RuntimeError
        Si la descarga falla por cualquier motivo (red, serie inexistente, etc.).
    """
    try:
        from pandas_datareader import data as web
    except Exception as e:  # pragma: no cover - entorno sin pandas-datareader
        raise RuntimeError(f"pandas-datareader no disponible: {e}") from e

    df = web.DataReader(series_id, "fred", start=start)
    if df.empty:
        raise RuntimeError(f"{series_id}: DataReader devolvió DataFrame vacío")

    # Normalizar a CSV: date,<series_id>
    df = df.reset_index()
    df.columns = ["date", series_id]
    return df.to_csv(index=False, lineterminator="\n")


def fetch_fallback(series_id: str) -> str:
    """Descarga el CSV público de FRED (fredgraph) y devuelve el texto tal cual.

    Parámetros
    ----------
    series_id : str
        Código de la serie en FRED.

    Returns
    -------
    str
        Texto del CSV tal cual lo sirve FRED.

    Raises
    ------
    RuntimeError
        Si la descarga falla.
    """
    import urllib.request

    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Fallo CSV público {series_id}: {e}") from e


def download_all(
    series: list[str],
    start: str,
    fetch_primary: Callable[[str, str], str] = fetch_primary,
    fetch_fallback: Callable[[str], str] = fetch_fallback,
) -> dict[str, tuple[str, str]]:
    """Descarga todas las series, probando primero la vía principal y luego el respaldo.

    Parámetros
    ----------
    series : list[str]
        Lista de códigos de serie (debe coincidir con ``ALL_SERIES``).
    start : str
        Fecha de inicio para la vía principal.
    fetch_primary : callable, opcional
        Función de descarga principal (inyectable para tests).
    fetch_fallback : callable, opcional
        Función de respaldo (inyectable para tests).

    Returns
    -------
    dict[str, tuple[str, str]]
        ``{series_id: (csv_text, fuente)}`` donde ``fuente`` es
        ``"pandas-datareader"`` o ``"fredgraph-csv"``.

    Raises
    ------
    DownloadError
        Si ambas vías fallan para alguna serie. El mensaje nombra la serie.
    """
    results: dict[str, tuple[str, str]] = {}
    for sid in series:
        try:
            csv_text = fetch_primary(sid, start)
            results[sid] = (csv_text, "pandas-datareader")
        except Exception:
            try:
                csv_text = fetch_fallback(sid)
                results[sid] = (csv_text, "fredgraph-csv")
            except Exception as e:
                raise DownloadError(f"No se pudo descargar {sid} ni por pandas-datareader ni por el CSV de FRED") from e
    return results


# --- Rutas y guardado ---

def raw_path(raw_dir: Path, series_id: str, day: date) -> Path:
    """Ruta del archivo crudo: ``<ID>_<AAAA-MM-DD>.csv``."""
    return raw_dir / f"{series_id}_{day.isoformat()}.csv"


def save_downloads(
    downloads: dict[str, tuple[str, str]],
    raw_dir: Path,
    day: date,
) -> list[dict]:
    """Guarda las descargas crudas y añade filas al manifiesto.

    Parámetros
    ----------
    downloads : dict
        Salida de ``download_all``.
    raw_dir : Path
        Directorio ``data/raw/``.
    day : date
        Fecha de la descarga (``date.today()`` en producción).

    Returns
    -------
    list[dict]
        Filas añadidas al manifiesto (una por serie).

    Raises
    ------
    DuplicateDownloadError
        Si ya existe un archivo crudo para esa serie con la misma fecha.
    """
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = raw_dir / "manifest.csv"

    # 1) Validar que no haya duplicados del día ANTES de escribir nada
    for sid in downloads:
        p = raw_path(raw_dir, sid, day)
        if p.exists():
            raise DuplicateDownloadError(f"Ya hay una descarga de {sid} con fecha {day.isoformat()}")

    # 2) Escribir todos los archivos crudos (todo o nada)
    for sid, (csv_text, source) in downloads.items():
        p = raw_path(raw_dir, sid, day)
        p.write_text(csv_text, encoding="utf-8")

    # 3) Leer manifiesto existente (si hay) y añadir filas nuevas
    if manifest_path.exists():
        manifest_df = pd.read_csv(manifest_path, dtype=str, keep_default_na=False)
    else:
        manifest_df = pd.DataFrame(
            columns=["series", "download_date", "source", "file", "n_rows", "first_obs", "last_obs"]
        )

    new_rows = []
    for sid, (csv_text, source) in downloads.items():
        # Contar filas de datos (excluye cabecera)
        n_rows = csv_text.count("\n") - 1
        # Primera y última observación (fechas)
        lines = csv_text.strip().split("\n")
        if len(lines) >= 2:
            first_obs = lines[1].split(",")[0]
            last_obs = lines[-1].split(",")[0]
        else:
            first_obs = ""
            last_obs = ""

        new_rows.append({
            "series": sid,
            "download_date": day.isoformat(),
            "source": source,
            "file": f"{sid}_{day.isoformat()}.csv",
            "n_rows": str(n_rows),
            "first_obs": first_obs,
            "last_obs": last_obs,
        })

    manifest_df = pd.concat([manifest_df, pd.DataFrame(new_rows)], ignore_index=True)
    manifest_df.to_csv(manifest_path, index=False, lineterminator="\n")

    return new_rows


# --- Lectura ---

def read_manifest(raw_dir: Path) -> pd.DataFrame:
    """Lee el manifiesto completo como DataFrame."""
    manifest_path = raw_dir / "manifest.csv"
    if not manifest_path.exists():
        return pd.DataFrame(
            columns=["series", "download_date", "source", "file", "n_rows", "first_obs", "last_obs"]
        )
    return pd.read_csv(manifest_path, dtype=str, keep_default_na=False)


def load_latest_raw(raw_dir: Path) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Carga la descarga más reciente de cada serie desde ``data/raw/``.

    Parámetros
    ----------
    raw_dir : Path
        Directorio ``data/raw/``.

    Returns
    -------
    tuple[dict[str, pd.DataFrame], pd.DataFrame]
        ``(raw_dict, manifest)`` donde ``raw_dict[series_id]`` es un
        ``DataFrame`` leído con ``dtype=str`` y ``keep_default_na=False``
        (para que ``".", "", "NaN"`` lleguen como texto y los trate ``panel.parse_raw``).

    Raises
    ------
    FileNotFoundError
        Si no hay manifiesto o falta algún archivo crudo. El mensaje indica
        ejecutar ``uv run python -m src.pipeline data --download``.
    """
    manifest_path = raw_dir / "manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"No hay descargas crudas en {raw_dir}: ejecuta `uv run python -m src.pipeline data --download`"
        )

    manifest = pd.read_csv(manifest_path, dtype=str, keep_default_na=False)
    if manifest.empty:
        raise FileNotFoundError(
            f"Manifiesto vacío en {raw_dir}: ejecuta `uv run python -m src.pipeline data --download`"
        )

    # Para cada serie, quedarse con la fila de mayor download_date
    manifest["download_date"] = pd.to_datetime(manifest["download_date"])
    latest = manifest.sort_values("download_date").groupby("series", as_index=False).last()

    raw_dict: dict[str, pd.DataFrame] = {}
    for _, row in latest.iterrows():
        sid = row["series"]
        file_path = raw_dir / row["file"]
        if not file_path.exists():
            raise FileNotFoundError(
                f"Falta el archivo crudo {file_path} para {sid}: ejecuta `uv run python -m src.pipeline data --download`"
            )
        # Leer con dtype=str y keep_default_na=False (RF-7)
        df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
        raw_dict[sid] = df

    return raw_dict, manifest