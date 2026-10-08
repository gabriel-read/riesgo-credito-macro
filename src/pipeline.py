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


def stage_models() -> int:
    """Ejecuta el Modelo I (spec 003) y el Modelo II (spec 004) sobre las descargas congeladas de data/raw/.

    Sin red. Reconstruye en memoria la historia transformada desde 1998 (plan 003, D1) y lee la
    decisión niveles/diferencias de `outputs/tables/stationarity.csv` (la deja la etapa `data`).
    Escribe: las 9 tablas (.csv y .md), las 3 figuras (.png a 200 dpi), el JSON para la spec 005
    y la clave `modelo1:` de `report/_variables.yml` (las demás claves no se tocan). Del Modelo II
    escribe las 14 tablas (.csv y .md), las 3 figuras, `outputs/models/model2_main.json` y la clave
    `modelo2:`. No contiene cálculo: llama a funciones puras de src/.
    """
    ROOT, DATA_RAW, DATA_PROCESSED, OUTPUTS, OUTPUTS_TABLES, OUTPUTS_FIGURES, REPORT = _get_paths()

    import matplotlib.pyplot as plt
    import pandas as pd
    import yaml

    from src.figures import (
        plot_model1_coefficients,
        plot_model1_cusum,
        plot_model1_oos,
        plot_model2_profile,
        plot_model2_response,
    )
    from src.fred_io import load_latest_raw
    from src.model1 import render_model1_tables, run_model1, stress_export_json
    from src.model2 import export2_json, render_model2_tables, run_model2
    from src.panel import build_panel
    from src.report_vars import model1_variables, model2_variables

    stationarity_path = OUTPUTS_TABLES / "stationarity.csv"
    if not stationarity_path.exists():
        raise FileNotFoundError(
            f"No existe {stationarity_path}: ejecuta primero `uv run python -m src.pipeline data`"
        )

    raw, _ = load_latest_raw(DATA_RAW)
    panel = build_panel(raw)
    stationarity = pd.read_csv(stationarity_path, index_col=0)
    print("Estimando el Modelo I...")
    result = run_model1(panel.full, stationarity, panel.end)
    print("Estimando el Modelo II...")
    result2 = run_model2(panel.full, stationarity, panel.end, result)

    models_dir = OUTPUTS / "models"
    OUTPUTS_TABLES.mkdir(parents=True, exist_ok=True)
    OUTPUTS_FIGURES.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    REPORT.mkdir(parents=True, exist_ok=True)

    # Tablas: Markdown (coma decimal) y CSV (precisión completa); fin de línea "\n" en todo SO
    for stem, text in render_model1_tables(result).items():
        (OUTPUTS_TABLES / f"{stem}.md").write_text(text["md"] + "\n", encoding="utf-8", newline="\n")
        (OUTPUTS_TABLES / f"{stem}.csv").write_text(text["csv"], encoding="utf-8", newline="\n")

    for stem, text in render_model2_tables(result2).items():
        (OUTPUTS_TABLES / f"{stem}.md").write_text(text["md"] + "\n", encoding="utf-8", newline="\n")
        (OUTPUTS_TABLES / f"{stem}.csv").write_text(text["csv"], encoding="utf-8", newline="\n")

    # Figuras: 8×4,5 pulgadas a 200 dpi; sin marca de versión para que los bytes sean deterministas
    figures = {
        "model1_coefficients.png": plot_model1_coefficients(result.effects),
        "model1_cusum.png": plot_model1_cusum(result.cusum),
        "model1_oos.png": plot_model1_oos(result.oos),
        "model2_profile.png": plot_model2_profile(result2.coefficients, result2.peak),
        "model2_response.png": plot_model2_response(
            result2.lp, result2.trajectory, result2.comparison_counts["horizonte_deteccion"]),
        "model2_cusum.png": plot_model1_cusum(result2.cusum),
    }
    for name, fig in figures.items():
        fig.savefig(OUTPUTS_FIGURES / name, dpi=200, metadata={"Software": None})
        plt.close(fig)

    # Coeficientes y covarianza HAC de la principal, para la prueba de estrés (spec 005)
    (models_dir / "model1_main.json").write_text(
        stress_export_json(result.stress), encoding="utf-8", newline="\n"
    )

    # Coeficientes y covarianza HAC de la principal del Modelo II y su trayectoria, para la spec 005
    (models_dir / "model2_main.json").write_text(
        export2_json(result2.export), encoding="utf-8", newline="\n"
    )

    # _variables.yml: solo se reescriben las claves `modelo1:` y `modelo2:`
    variables_path = REPORT / "_variables.yml"
    existing: dict = {}
    if variables_path.exists():
        with open(variables_path, "r", encoding="utf-8") as f:
            existing = yaml.safe_load(f) or {}
    existing["modelo1"] = model1_variables(result)
    existing["modelo2"] = model2_variables(result2)
    with open(variables_path, "w", encoding="utf-8", newline="\n") as f:
        yaml.dump(existing, f, allow_unicode=True, sort_keys=False)

    print(f"Modelo I: {result.coef_footer['n_obs']} trimestres "
          f"({result.coef_footer['muestra_inicio']}–{result.coef_footer['muestra_fin']}), "
          f"{result.coef_footer['n_parametros']} parámetros, {result.coef_footer['rezagos_hac']} rezagos HAC")
    print(f"Modelo II: {result2.coef_footer['n_obs']} trimestres "
          f"({result2.coef_footer['muestra_inicio']}–{result2.coef_footer['muestra_fin']}), "
          f"K = {result2.K} (BIC) y K_AIC = {result2.k_aic}, "
          f"{result2.coef_footer['n_parametros']} parámetros, {result2.coef_footer['rezagos_hac']} rezagos HAC")
    print("Etapa models completada.")
    return 0


def stage_placeholder(name: str) -> int:
    """Etapa pendiente (specs 004, 005, 006)."""
    print(f"Etapa {name} pendiente (spec correspondiente no implementada)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pipeline riesgo crédito-macro (spec 001)")
    parser.add_argument("stage", choices=["data", "models", "stress", "report", "all"],
                        help="Etapa a ejecutar")
    parser.add_argument("--download", action="store_true",
                        help="Descargar datos de FRED (solo para stage data)")

    args = parser.parse_args(argv)

    if args.stage == "data":
        return stage_data(download=args.download)
    elif args.stage == "models":
        return stage_models()
    elif args.stage == "stress":
        return stage_placeholder("stress")
    elif args.stage == "report":
        return stage_placeholder("report")
    elif args.stage == "all":
        # data sin download, luego las demás
        rc = stage_data(download=False)
        if rc != 0:
            return rc
        rc = stage_models()
        if rc != 0:
            return rc
        for st in ["stress", "report"]:
            rc = stage_placeholder(st)
            if rc != 0:
                return rc
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())