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


def load_fed_sources(directory: Path) -> dict:
    """Read original frozen Fed bytes and BOM manifest, without writing or network."""
    import hashlib
    import pandas as pd
    from src.design import ModelDataError
    from src.scenarios import FED_FILES, parse_fed_csv

    manifest = pd.read_csv(directory / "manifest.csv", encoding="utf-8-sig", dtype=str,
                           keep_default_na=False)
    required = {"file", "scenario", "version", "url", "download_date", "sha256"}
    if not required.issubset(manifest.columns) or manifest["file"].duplicated().any():
        raise ModelDataError("Fed: manifiesto inválido")
    if set(manifest["file"]) != {spec.filename for spec in FED_FILES.values()}:
        raise ModelDataError("Fed: manifiesto no contiene los tres archivos exactos")
    results = {}
    for name, spec in FED_FILES.items():
        entry = manifest.loc[manifest["file"].eq(spec.filename)].iloc[0]
        url = "https://www.federalreserve.gov/supervisionreg/files/" + spec.filename
        if entry["scenario"] != spec.scenario or entry["version"] != "2026 Final" or entry["url"] != url:
            raise ModelDataError(f"{spec.filename}: metadatos del manifiesto distintos")
        raw = (directory / spec.filename).read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ModelDataError(f"{spec.filename}: sha256 distinto del manifiesto")
        results[name] = parse_fed_csv(raw.decode("utf-8-sig"), spec)
    return results


def load_stress_history(root: Path, origin) -> dict:
    """Read the fixed FRED vintage and approved quarterly aggregation; never write."""
    import hashlib
    import pandas as pd
    from src.design import ModelDataError
    from src.fred_io import load_latest_raw
    from src.panel import build_panel, parse_raw, quarterly_from_quarterly, quarterly_from_monthly

    expected = {
        "GDPC1": (114, "2026-04-01", "13f963dec694c782ee1bedab9e81a8420407e671ce50354364330b2cb846e121"),
        "CPIAUCSL": (344, "2026-08-01", "5b49342a4c7d5419f3bfefcdef8a743055da793ec64caa7df3ebbad186374090"),
        "LOANS": (344, "2026-08-01", "56bde6d372a676275af470b586fbe242ef15322d879049996917cf8f311f1fa0"),
    }
    raw_dir = root / "data" / "raw"
    manifest_text = pd.read_csv(raw_dir / "manifest.csv", dtype=str, keep_default_na=False)
    for series, (nrows, last, sha) in expected.items():
        entries = manifest_text.loc[manifest_text["series"].eq(series)].sort_values("download_date")
        filename = f"{series}_2026-10-02.csv"
        if entries.empty:
            raise ModelDataError(f"{series}: vintage ausente")
        entry = entries.iloc[-1]
        if (entry["file"] != filename or entry["download_date"] != "2026-10-02"
                or entry["n_rows"] != str(nrows) or entry["last_obs"] != last):
            raise ModelDataError(f"{series}: vintage distinto del aprobado")
        content = (raw_dir / filename).read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(content).hexdigest() != sha:
            raise ModelDataError(f"{series}: sha256 del vintage distinto")
    raw, _ = load_latest_raw(raw_dir)
    for series, (nrows, last, _) in expected.items():
        if len(raw[series]) != nrows or str(raw[series]["date"].iloc[-1]) != last:
            raise ModelDataError(f"{series}: filas o último dato del vintage distintos")
    panel = build_panel(raw)
    gdp, gdp_complete = quarterly_from_quarterly(parse_raw(raw["GDPC1"], "GDPC1"))
    cpi, cpi_complete, treatment = quarterly_from_monthly(parse_raw(raw["CPIAUCSL"], "CPIAUCSL"), "CPIAUCSL")
    for series, levels, mask in (("GDPC1", gdp, gdp_complete), ("CPIAUCSL", cpi, cpi_complete)):
        levels = levels.loc[:origin]
        if origin not in levels.index or not mask.loc[levels.index].all() or levels.isna().any() or (levels <= 0).any():
            raise ModelDataError(f"{series}: niveles positivos y completos requeridos hasta {origin}")
    return {"full": panel.full.loc[:origin].copy(), "panel": panel.panel.loc[:origin].copy(),
            "gdpc1": gdp.loc[:origin].copy(), "cpiaucsl": cpi.loc[:origin].copy(),
            "cpi_treatment": treatment, "end": panel.end}


def stage_stress() -> int:
    """Spec 005: read frozen sources and existing estimates, write stress outputs only."""
    import hashlib
    import json
    import pandas as pd
    import yaml
    from src.design import ModelDataError
    from src.stress import read_model_contract, run_stress
    from src.stress_tables import render_stress_tables
    from src.stress_figures import stress_figure_png

    root, _, _, _, tables_dir, figures_dir, report_dir = _get_paths()
    source_dir = root / "data/scenarios/fed/2026-final/2026-10-11"
    fed = load_fed_sources(source_dir)
    approved = {
        "2026_Final_Historic_Domestic.csv": "6d08aadcf82d65dcf36b856792040b82ceceef79a46ff0239afd41e0c4e7f653",
        "2026_Final_Supervisory_Baseline_Domestic.csv": "76e236695be2c8372890078acf8c01273ba5198a19afb5037045a963737c1bcc",
        "2026_Final_Supervisory_Severely_Adverse_Domestic.csv": "45c2859ae7246c071b69df8623854751f0629b04393957e14fe28bc33c04ebbb",
    }
    for name, sha in approved.items():
        if hashlib.sha256((source_dir / name).read_bytes()).hexdigest() != sha:
            raise ModelDataError(f"{name}: sha256 distinto del pre-registro")
    contracts = {m: read_model_contract(json.loads((root / f"outputs/models/{file}_main.json").read_text(encoding="utf-8")), m)
                 for m, file in (("modelo1", "model1"), ("modelo2", "model2"))}
    history = load_stress_history(root, contracts["modelo1"].origin)
    import numpy as np
    saved_panel = pd.read_csv(root / "data/processed/panel.csv", index_col=0, float_precision="round_trip")
    try:
        saved_panel.index = pd.PeriodIndex(saved_panel.index, freq="Q-DEC")
    except ValueError as exc:
        raise ModelDataError("panel: etiquetas trimestrales inválidas") from exc
    expected_panel = history["panel"]
    if (not saved_panel.index.equals(expected_panel.index) or list(saved_panel.columns) != list(expected_panel.columns)
            or not np.allclose(saved_panel.to_numpy(dtype=float), expected_panel.to_numpy(dtype=float), atol=1e-12, rtol=0)):
        raise ModelDataError("panel guardado distinto del vintage y transformaciones aprobados")
    history["panel"] = saved_panel
    diagnostics = {m: pd.read_csv(tables_dir / f"{file}_diagnostics.csv", keep_default_na=False)
                   for m, file in (("modelo1", "model1"), ("modelo2", "model2"))}
    oos = pd.read_csv(tables_dir / "model1_oos.csv", keep_default_na=False)
    result = run_stress(contracts, fed, history, diagnostics, oos)
    rendered = render_stress_tables(result["tables"])
    pngs = {m: stress_figure_png(*frames) for m, frames in result["graphics"].items()}
    variables_path = report_dir / "_variables.yml"
    variables = yaml.safe_load(variables_path.read_text(encoding="utf-8")) or {}
    variables["estres"] = result["variables"]
    for directory in (tables_dir, figures_dir, report_dir):
        directory.mkdir(parents=True, exist_ok=True)
    for name, (csv_text, markdown) in rendered.items():
        (tables_dir / f"{name}.csv").write_text(csv_text, encoding="utf-8", newline="\n")
        (tables_dir / f"{name}.md").write_text(markdown, encoding="utf-8", newline="\n")
    for m, png in pngs.items():
        (figures_dir / f"stress_{'model1' if m == 'modelo1' else 'model2'}.png").write_bytes(png)
    variables_path.write_text(yaml.safe_dump(variables, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")
    print("Etapa stress completada; incertidumbre de parámetros y sensibilidades separadas.")
    return 0


def stage_report() -> int:
    """Refresh Quarto's generated adapter from the canonical variables only."""
    import hashlib

    from src.report_vars import sync_report_variables, render_report_interface, add_report_metadata

    root, _, _, _, _, _, report_dir = _get_paths()
    source = report_dir / "_variables.yml"
    content = source.read_bytes()
    sync_report_variables(content.decode("utf-8"))
    matrix_path = root / "research/matriz-literatura.md"
    if matrix_path.is_file():
        import csv
        import io
        import yaml
        from src.report_tables import literature_report_table, _markdown, format_report_cell

        matrix_text = matrix_path.read_text(encoding="utf-8")
        manifest = root / "data/raw/manifest.csv"
        stress_paths = root / "outputs/tables/stress_paths.csv"
        variables = add_report_metadata(yaml.safe_load(content.decode("utf-8")), matrix_text,
                                        manifest.read_text(encoding="utf-8") if manifest.is_file() else "",
                                        stress_paths.read_text(encoding="utf-8") if stress_paths.is_file() else "")
        levels = root / "outputs/tables/stress_levels.csv"
        if levels.is_file():
            headers = next(csv.reader(io.StringIO(levels.read_text(encoding="utf-8"))))
            if "p05" in headers and "p95" in headers:
                variables.setdefault("informe", {})["bandas"] = {
                    "percentil_inferior": str(int("p05"[1:])), "percentil_superior": str(int("p95"[1:])),
                    "origen": "Columnas p05 y p95 de stress_levels.csv; incertidumbre de parámetros, no predicción.",
                }
        content = yaml.safe_dump(variables, allow_unicode=True, sort_keys=False).encode("utf-8")
        source.write_bytes(content)
        literature = literature_report_table(matrix_text)
        tables_dir = root / "outputs/tables"
        tables_dir.mkdir(parents=True, exist_ok=True)
        (tables_dir / "lit_estudios.csv").write_text(literature.to_csv(index=False, lineterminator="\n"),
                                                   encoding="utf-8", newline="\n")
        formatted = [[format_report_cell(str(value), column) for column, value in zip(literature.columns, row)]
                     for row in literature.itertuples(index=False, name=None)]
        (tables_dir / "lit_estudios.md").write_text(_markdown(list(literature.columns), formatted,
                                                            "research/matriz-literatura.md"),
                                                  encoding="utf-8", newline="\n")
    mirror = root / "_variables.yml"
    mirror.write_bytes(content)
    expected = hashlib.sha256(source.read_bytes()).hexdigest()
    if hashlib.sha256(mirror.read_bytes()).hexdigest() != expected:
        raise ValueError("Variables del informe: SHA-256 del espejo distinto de la fuente")
    from src.report_tables import build_report_tables
    import json

    sources = {path.stem: path.read_bytes().decode("utf-8")
               for path in sorted((root / "outputs/tables").glob("*.csv"))}
    frozen_manifest = root / 'data/raw/manifest.csv'
    if frozen_manifest.is_file():
        sources['fred_manifest'] = frozen_manifest.read_bytes().decode('utf-8')
    if sources:
        source_notes = {}
        source_markdown = {}
        for name in sources:
            approved_markdown = root / 'outputs/tables' / (name + '.md')
            if approved_markdown.is_file() and name != 'lit_estudios':
                markdown = approved_markdown.read_bytes().decode('utf-8')
                source_markdown[name] = markdown
                lines = markdown.splitlines()
                table_lines = [i for i, line in enumerate(lines) if line.startswith('|')]
                if table_lines:
                    note = '\n'.join(lines[table_lines[-1] + 1:]).strip()
                    if note:
                        source_notes[name] = note
        result = build_report_tables(sources, source_notes=source_notes, source_markdown=source_markdown)
        destination = root / "outputs/informe"
        destination.mkdir(parents=True, exist_ok=True)
        for name, markdown in result["files"].items():
            (destination / name).write_text(markdown, encoding="utf-8", newline="\n")
        (destination / "trace.json").write_text(json.dumps(result["trace"], ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8", newline="\n")
        annex_dir = report_dir / "anexos"
        annex_dir.mkdir(parents=True, exist_ok=True)
        (annex_dir / "tablas.qmd").write_text(result["annex"], encoding="utf-8", newline="\n")
    from src.report_tables import TITLES

    from src.report_editorial import build_report_registry, registry_csv, registry_interface, link_registry_csv, build_editorial_documents

    registry = build_report_registry({name: text.encode("utf-8") for name, text in sources.items()},
                                     {p.stem: p.read_bytes() for p in (root / "outputs/figures").glob("*.png")})
    if {'stress_levels', 'stress_delta'} <= sources.keys():
        from src.report_figures import stress_presentation_png
        import io
        import pandas as pd
        levels = pd.read_csv(io.StringIO(sources['stress_levels']))
        changes = pd.read_csv(io.StringIO(sources['stress_delta']))
        for entry in registry:
            if entry['kind'] == 'figure' and entry['name'] in {'stress_model1', 'stress_model2'}:
                figure_content = stress_presentation_png(levels, changes, 'modelo1' if entry['name'] == 'stress_model1' else 'modelo2')
                figure_file = root / 'outputs/informe' / (entry['name'] + '_presentacion.png')
                figure_file.parent.mkdir(parents=True, exist_ok=True)
                figure_file.write_bytes(figure_content)
                entry['presentation_source'] = figure_file.relative_to(root).as_posix()
                entry['presentation_sha256'] = hashlib.sha256(figure_content).hexdigest()
    for entry in registry:
        entry.setdefault('presentation_source', entry['source'])
        entry.setdefault('presentation_sha256', entry['sha256'])
    if registry:
        destination = root / "outputs/informe"
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "registro.csv").write_text(registry_csv(registry), encoding="utf-8", newline="\n")
        from src.report_editorial import pdf_named_destination_pages
        annex_pdf = root / 'outputs/preview-006/report/anexo-tecnico.pdf'
        pages = pdf_named_destination_pages(annex_pdf.read_bytes()) if annex_pdf.is_file() else {}
        (destination / "enlaces.csv").write_text(link_registry_csv(registry, pages), encoding="utf-8", newline="\n")
        (destination / 'destinos.json').write_text(json.dumps({r['slug']: {'anchor': r['anchor'], 'annex': r['annex'],
                                                                         **({'page': pages[r['anchor']]} if r['anchor'] in pages else {})}
                                                               for r in registry}, ensure_ascii=False, indent=2) + '\n',
                                                   encoding='utf-8', newline='\n')
        editorial = build_editorial_documents(registry, sources, result)
        for filename, text in editorial['body_files'].items():
            (destination / filename).write_text(text, encoding='utf-8', newline='\n')
        (destination / 'body_trace.json').write_text(json.dumps(editorial['body_trace'], ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
        for filename, text in editorial['annex_files'].items():
            (report_dir / 'anexos' / filename).write_text(text, encoding='utf-8', newline='\n')
        main_source = report_dir / 'informe.qmd'
        if main_source.is_file():
            from src.report_editorial import combined_source
            sections = {'secciones/' + p.name: p.read_text(encoding='utf-8')
                        for p in (report_dir / 'secciones').glob('*.qmd')}
            combined = combined_source(main_source.read_text(encoding='utf-8'), sections,
                                       editorial['body_files'], registry)
            (report_dir / 'entrega-combinada.qmd').write_text(combined, encoding='utf-8', newline='\n')

    assets = {}
    candidates = list((root / "outputs/tables").glob("*")) + list((root / "outputs/figures").glob("*.png"))
    candidates += list((root / "outputs/informe").glob("*"))
    candidates += [root / "data/processed/panel.csv", root / "data/raw/manifest.csv", root / "outputs/data_note.md", source]
    figure_titles = {
        "delinquency_unemployment_ffr": "Morosidad, desempleo y tasa de política",
        "model1_oos": "Modelo I — evaluación fuera de muestra", "model1_cusum": "Modelo I — CUSUM",
        "model2_response": "Modelo II — respuestas dinámicas", "model2_profile": "Modelo II — perfil acumulado",
        "model2_cusum": "Modelo II — CUSUM", "stress_model1": "Estrés — Modelo I",
        "stress_model2": "Estrés — Modelo II",
    }
    for path in sorted(candidates):
        import re

        if (not path.is_file() or path.suffix not in (".csv", ".md", ".png", ".json", ".yml")
                or not re.fullmatch(r"[a-z0-9_]+", path.stem)):
            continue
        name = path.stem.split("_anexo_")[0]
        origin = ("003-modelo-i" if name.startswith("model1_") else "004-modelo-ii" if name.startswith("model2_")
                  else "005-estres" if name.startswith("stress_") else "006-informe desde 002-literatura" if name.startswith("lit_")
                  else "001-datos")
        generated = path.parent == root / "outputs/informe"
        if generated:
            origin = "006-informe (derivada de " + origin + ")"
        description = figure_titles.get(name, TITLES.get(name, name.replace("_", " ")))
        if path.name == "manifest.csv":
            description = "Manifiesto del vintage FRED congelado"
        elif path.name == "data_note.md":
            description = "Nota aprobada sobre datos y faltantes"
        elif path.name == "panel.csv":
            description = "Panel trimestral aprobado"
        if path == source:
            origin, description = "001–006 (canónico)", "Fuente única de variables del informe"
        elif path.name == "trace.json":
            origin, description = "006-informe", "Matriz CSV → presentación → anexo"
        if path.suffix == ".csv" and path.stem in sources:
            import csv
            import io

            units = sorted({row["unidad"] for row in csv.DictReader(io.StringIO(sources[path.stem]))
                            if row.get("unidad")})
            if units:
                description += "; unidades explícitas del CSV: " + "; ".join(units)
        assets[path.relative_to(root).as_posix()] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "description": description,
            "kind": "Figura PNG" if path.suffix == ".png" else "Derivado de presentación" if generated else "Fuente aprobada",
            "origin": origin,
        }
    interface_dir = root / "specs/006-informe"
    interface_dir.mkdir(parents=True, exist_ok=True)
    (interface_dir / "interfaz.md").write_text(render_report_interface(content.decode("utf-8"), assets) + registry_interface(registry),
                                             encoding="utf-8", newline="\n")
    print("Etapa report completada; espejo de variables verificado por SHA-256.")
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
        return stage_stress()
    elif args.stage == "report":
        return stage_report()
    elif args.stage == "all":
        # data sin download, luego las demás
        rc = stage_data(download=False)
        if rc != 0:
            return rc
        rc = stage_models()
        if rc != 0:
            return rc
        rc = stage_stress()
        if rc != 0:
            return rc
        rc = stage_report()
        if rc != 0:
            return rc
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
