"""Pipeline CLI: orquesta las etapas data | models | stress | report (spec 001).

Etapa `data`: descarga (con --download) o construye desde data/raw/ congelado.
Etapas `models`, `stress`, `report`: pendientes (specs 003, 004, 005, 006).
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")


def _get_paths() -> tuple[Path, Path, Path, Path, Path, Path, Path]:
    """Rutas configurables vía variable de entorno PIPELINE_ROOT (para tests)."""
    root = Path(os.environ.get("PIPELINE_ROOT", Path(__file__).resolve().parents[1]))
    return (
        root,
        root / "data" / "raw",
        root / "data" / "processed",
        root / "outputs",
        root / "outputs" / "tables",
        root / "outputs" / "figures",
        root / "report",
    )


def stage_data(download: bool = False) -> int:
    """Ejecuta la etapa de datos.

    Si download=True: descarga 13 series y construye todo.
    Si download=False: construye desde data/raw/ congelado (sin red).
    """
    ROOT, DATA_RAW, DATA_PROCESSED, OUTPUTS, OUTPUTS_TABLES, OUTPUTS_FIGURES, REPORT = _get_paths()

    from src.fred_io import download_all, load_latest_raw, save_downloads
    from src.config import ALL_SERIES, DOWNLOAD_START
    from src.panel import build_panel
    from src.stationarity import stationarity_table
    from src.descriptives import descriptive_table
    from src.data_note import build_data_note
    from src.figures import plot_delinquency_macro
    from src.report_vars import data_variables
    from src.tables import to_markdown
    import yaml
    from datetime import date

    if download:
        # Descarga única (todo o nada)
        print("Descargando 13 series desde FRED...")
        downloads = download_all(ALL_SERIES, DOWNLOAD_START)
        today = date.today()
        save_downloads(downloads, DATA_RAW, today)
        print(f"Guardadas {len(downloads)} series en {DATA_RAW}")

    # Cargar descargas crudas más recientes
    raw, manifest = load_latest_raw(DATA_RAW)

    # Construir panel
    print("Construyendo panel trimestral...")
    result = build_panel(raw)

    # Tabla de estacionariedad
    tested_cols = [c for c in result.full.columns if c != "usrec" and not c.endswith("_d")]
    stationarity = stationarity_table(result.full, tested_cols, result.panel.index[0], result.end)

    # Descriptivos
    descriptives = descriptive_table(result.panel)

    # Nota de datos
    from src.config import SERIES_META
    data_note_md = build_data_note(result, manifest, SERIES_META)

    # Figura
    fig = plot_delinquency_macro(result.panel)

    # Variables para _variables.yml
    vars_dict = data_variables(result, stationarity, manifest)

    # Escribir salidas
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    OUTPUTS_TABLES.mkdir(parents=True, exist_ok=True)
    OUTPUTS_FIGURES.mkdir(parents=True, exist_ok=True)
    REPORT.mkdir(parents=True, exist_ok=True)

    # Panel CSV (precisión completa, sin redondeo)
    result.panel.to_csv(
        DATA_PROCESSED / "panel.csv",
        float_format=None,
        lineterminator="\n",
    )

    # Descriptivos CSV y MD
    descriptives.to_csv(OUTPUTS_TABLES / "descriptives.csv", float_format=None, lineterminator="\n")
    (OUTPUTS_TABLES / "descriptives.md").write_text(to_markdown(descriptives), encoding="utf-8")

    # Estacionariedad CSV y MD
    stationarity.to_csv(OUTPUTS_TABLES / "stationarity.csv", float_format=None, lineterminator="\n")
    (OUTPUTS_TABLES / "stationarity.md").write_text(to_markdown(stationarity), encoding="utf-8")

    # Nota de datos
    (OUTPUTS / "data_note.md").write_text(data_note_md, encoding="utf-8")

    # Figura
    fig.savefig(OUTPUTS_FIGURES / "delinquency_unemployment_ffr.png", dpi=200, bbox_inches="tight")

    # _variables.yml (solo clave datos:)
    if (REPORT / "_variables.yml").exists():
        with open(REPORT / "_variables.yml", "r", encoding="utf-8") as f:
            existing = yaml.safe_load(f) or {}
    else:
        existing = {}
    existing["datos"] = vars_dict
    with open(REPORT / "_variables.yml", "w", encoding="utf-8") as f:
        yaml.dump(existing, f, allow_unicode=True, sort_keys=False)

    print(f"Panel: {len(result.panel)} trimestres (2000T1-{result.end})")
    print(f"Último trimestre común: {result.end}")
    print("Etapa data completada.")
    return 0


def stage_placeholder(name: str) -> int:
    """Etapa pendiente (specs 003, 004, 005, 006)."""
    print(f"Etapa {name} pendiente (spec correspondiente no implementada)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline riesgo crédito-macro (spec 001)")
    parser.add_argument("stage", choices=["data", "models", "stress", "report", "all"],
                        help="Etapa a ejecutar")
    parser.add_argument("--download", action="store_true",
                        help="Descargar datos de FRED (solo para stage data)")

    args = parser.parse_args()

    if args.stage == "data":
        return stage_data(download=args.download)
    elif args.stage == "models":
        return stage_placeholder("models")
    elif args.stage == "stress":
        return stage_placeholder("stress")
    elif args.stage == "report":
        return stage_placeholder("report")
    elif args.stage == "all":
        # data sin download, luego las demás
        rc = stage_data(download=False)
        if rc != 0:
            return rc
        for st in ["models", "stress", "report"]:
            rc = stage_placeholder(st)
            if rc != 0:
                return rc
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())