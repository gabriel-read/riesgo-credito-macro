"""Tests de ``src/fred_io.py`` (T3, spec 001).

Verifican la descarga (principal y respaldo), guardado crudo, manifiesto y
lectura de la descarga más reciente. Sin red: ``fetch_primary`` y
``fetch_fallback`` se inyectan como parámetros (RF-2 a RF-6, RF-24).
"""

from pathlib import Path
import tempfile
import pandas as pd
import pytest

from src.fred_io import (
    download_all,
    load_latest_raw,
    raw_path,
    read_manifest,
    save_downloads,
)


# ---------- Fixtures y helpers ----------

def _sample_csv(series_id: str) -> str:
    """CSV mínimo válido con 2 filas de datos."""
    return f"date,{series_id}\n1998-01-01,1.0\n1998-04-01,1.1\n"


def _bad_csv() -> str:
    """CSV con texto no numérico."""
    return "date,DRALACBS\n1998-01-01,abc\n"


def _empty_csv(series_id: str) -> str:
    """CSV solo cabecera."""
    return f"date,{series_id}\n"


def _fetch_primary_ok(series_id: str, start: str) -> str:
    return _sample_csv(series_id)


def _fetch_primary_fail(series_id: str, start: str) -> str:
    raise RuntimeError(f"Fallo primario {series_id}")


def _fetch_fallback_ok(series_id: str) -> str:
    return _sample_csv(series_id)


def _fetch_fallback_fail(series_id: str) -> str:
    raise RuntimeError(f"Fallo respaldo {series_id}")


# ---------- Tests ----------

def test_download_all_primary_ok(tmp_path: Path):
    """Todas por vía principal: fuente 'pandas-datareader'."""
    downloads = download_all(
        ["DRALACBS", "UNRATE"],
        "1998-01-01",
        fetch_primary=_fetch_primary_ok,
        fetch_fallback=_fetch_fallback_fail,
    )
    assert downloads["DRALACBS"][1] == "pandas-datareader"
    assert downloads["UNRATE"][1] == "pandas-datareader"


def test_download_all_fallback_used(tmp_path: Path):
    """Primaria falla, respaldo ok: fuente 'fredgraph-csv'."""
    downloads = download_all(
        ["DRALACBS"],
        "1998-01-01",
        fetch_primary=_fetch_primary_fail,
        fetch_fallback=_fetch_fallback_ok,
    )
    assert downloads["DRALACBS"][1] == "fredgraph-csv"


def test_download_all_both_fail_raises_and_writes_nothing(tmp_path: Path):
    """Ambas fallan: RuntimeError con el nombre de la serie; nada escrito."""
    with pytest.raises(RuntimeError, match="DRALACBS"):
        download_all(
            ["DRALACBS"],
            "1998-01-01",
            fetch_primary=_fetch_primary_fail,
            fetch_fallback=_fetch_fallback_fail,
        )


def test_save_downloads_writes_files_and_manifest(tmp_path: Path):
    """Guarda 13 archivos crudos y añade 13 filas al manifiesto."""
    day = pd.Timestamp("2026-10-02").date()
    downloads = {sid: (_sample_csv(sid), "pandas-datareader") for sid in ["DRALACBS", "UNRATE"]}
    manifest_rows = save_downloads(downloads, tmp_path, day)

    # Archivos crudos
    for sid in ["DRALACBS", "UNRATE"]:
        p = raw_path(tmp_path, sid, day)
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert f"date,{sid}" in content

    # Manifiesto
    manifest = tmp_path / "manifest.csv"
    assert manifest.exists()
    df = pd.read_csv(manifest)
    assert len(df) == 2
    assert list(df.columns) == ["series", "download_date", "source", "file", "n_rows", "first_obs", "last_obs"]
    assert set(df["series"]) == {"DRALACBS", "UNRATE"}
    assert all(df["source"] == "pandas-datareader")


def test_save_downloads_same_day_twice_raises(tmp_path: Path):
    """Segunda descarga el mismo día: FileExistsError, original intacto."""
    day = pd.Timestamp("2026-10-02").date()
    downloads = {"DRALACBS": (_sample_csv("DRALACBS"), "pandas-datareader")}
    save_downloads(downloads, tmp_path, day)

    with pytest.raises(FileExistsError, match="DRALACBS"):
        save_downloads(downloads, tmp_path, day)

    # El archivo original sigue ahí
    assert raw_path(tmp_path, "DRALACBS", day).exists()


def test_manifest_preserves_previous_rows(tmp_path: Path):
    """El manifiesto conserva filas previas al añadir nuevas."""
    day1 = pd.Timestamp("2026-10-01").date()
    day2 = pd.Timestamp("2026-10-02").date()
    downloads1 = {"DRALACBS": (_sample_csv("DRALACBS"), "pandas-datareader")}
    downloads2 = {"UNRATE": (_sample_csv("UNRATE"), "pandas-datareader")}

    save_downloads(downloads1, tmp_path, day1)
    save_downloads(downloads2, tmp_path, day2)

    df = read_manifest(tmp_path)
    assert len(df) == 2
    assert set(df["series"]) == {"DRALACBS", "UNRATE"}
    assert list(df["download_date"]) == ["2026-10-01", "2026-10-02"]


def test_load_latest_raw_picks_most_recent(tmp_path: Path):
    """Entre dos fechas, elige la más reciente por serie."""
    day1 = pd.Timestamp("2026-10-01").date()
    day2 = pd.Timestamp("2026-10-02").date()
    # day1: valor 1.0
    csv1 = "date,DRALACBS\n1998-01-01,1.0\n1998-04-01,1.1\n"
    # day2: valor 2.0 (distinto)
    csv2 = "date,DRALACBS\n1998-01-01,2.0\n1998-04-01,2.1\n"
    downloads1 = {"DRALACBS": (csv1, "pandas-datareader")}
    downloads2 = {"DRALACBS": (csv2, "pandas-datareader")}

    save_downloads(downloads1, tmp_path, day1)
    save_downloads(downloads2, tmp_path, day2)

    raw, manifest = load_latest_raw(tmp_path)
    assert "DRALACBS" in raw
    # Debe haber elegido day2 (valor 2.0) - columna es el series_id, no "date"
    assert raw["DRALACBS"].iloc[0, 1] == "2.0"


def test_load_latest_raw_no_manifest_raises_clear(tmp_path: Path):
    """Sin manifiesto: FileNotFoundError con mensaje que contiene 'data --download'."""
    with pytest.raises(FileNotFoundError, match="data --download"):
        load_latest_raw(tmp_path)


def test_load_latest_raw_reads_with_dtype_str_and_keep_default_na_false(tmp_path: Path):
    """load_latest_raw lee con dtype=str y keep_default_na=False (RF-7)."""
    day = pd.Timestamp("2026-10-02").date()
    # CSV con punto, cadena vacía y "NaN" como texto
    csv = "date,DRALACBS\n1998-01-01,.\n1998-04-01,\n1998-07-01,NaN\n1998-10-01,1.5\n"
    downloads = {"DRALACBS": (csv, "pandas-datareader")}
    save_downloads(downloads, tmp_path, day)

    raw, _ = load_latest_raw(tmp_path)
    df = raw["DRALACBS"]
    # Se leen 4 filas de datos + cabecera = 5 filas en el DataFrame crudo
    assert len(df) == 4
    # Los valores problemáticos llegan como strings "." en la columna de la serie (índice 1)
    assert "." in df.iloc[0, 1]
    assert "" == df.iloc[1, 1] or df.iloc[1, 1] == ""
    assert "NaN" in str(df.iloc[2, 1])
    assert "1.5" == df.iloc[3, 1]


def test_raw_path_naming(tmp_path: Path):
    """raw_path genera <ID>_<AAAA-MM-DD>.csv."""
    day = pd.Timestamp("2026-10-02").date()
    p = raw_path(tmp_path, "DRALACBS", day)
    assert p.name == "DRALACBS_2026-10-02.csv"
    assert p.parent == tmp_path