# Tasks 001 — Datos
Estado: borrador · Spec: `specs/001-datos/spec.md` (aprobada) · Plan: `specs/001-datos/plan.md` (aprobada)

Orden de implementación: primero config, luego fred_io, panel, stationarity, descriptives, data_note, tables, report_vars, figures, pipeline, notebook, tests. Tests primero dentro de cada tarea.

- [x] **T1. Configuración base: pytest, `conftest.py` (bloqueo de red) y endurecimiento RNF-4.** RNF-2, RNF-4 · agente: implementer
  - Tests primero: `tests/conftest.py` con fixture `autouse` que sustituye `socket.socket.connect`, `socket.create_connection` y `socket.getaddrinfo` por una función que lanza `RuntimeError("Red bloqueada en tests")`. Test `test_network_blocked` que verifica que abrir un socket lanza `RuntimeError`. Test `test_harness.py` con `find_hand_typed_numbers(text)` y patrones `(?<![\w.,])\d+[.,]\d+` y `(?<![\w.,])\d+\s?%`: «0,8 pp» y «15 %» se detectan; `{{< var datos.muestra_fin >}}` y «2000T1» no.
  - Implementación: `pyproject.toml` con `pythonpath = ["."]` y configuración de pytest.
  - Hecho cuando: `uv run pytest -q` en verde; abrir un socket en un test lanza `RuntimeError`; `find_hand_typed_numbers` detecta «0,8 pp» y «15 %» pero no `{{< var datos.muestra_fin >}}` ni «2000T1».

- [x] **T2. `src/config.py`: constantes, metadatos y etiquetas.** RF-1, RF-17, RNF-5 · agente: implementer
  - Tests primero: test que verifica que `ALL_SERIES` tiene 13 elementos, que `MAIN_SERIES` y `ROBUSTNESS_SERIES` no se solapan, que `SAMPLE_START` es `2000Q1`, que `ALPHA == 0.05`, que `ADF_MAXLAG == 4`, y que `COLUMN_LABELS` cubre las 25 columnas del panel con etiquetas en español.
  - Implementación: `MAIN_SERIES`, `ROBUSTNESS_SERIES`, `RECESSION_SERIES`, `ALL_SERIES`, `MONTHLY`, `DELINQUENCY`, `DOWNLOAD_START`, `SAMPLE_START`, `DOCUMENTED_GAP_SERIES`, `DOCUMENTED_GAP_MONTH`, `ALPHA`, `ADF_MAXLAG`, `SERIES_META` (unidad, frecuencia, desestacionalización, tratamiento trimestral, nombre en español), `COLUMN_LABELS`.
  - Hecho cuando: test en verde; `ALL_SERIES` tiene 13 series; `COLUMN_LABELS` tiene 25 entradas con etiquetas en español.

- [x] **T3. `src/fred_io.py`: descarga, respaldo, guardado, manifiesto y lectura.** RF-1, RF-2, RF-3, RF-4, RF-5, RF-6, RF-24 · agente: implementer
  - Tests primero (con `fetch_primary` y `fetch_fallback` inyectadas, sin red): test que con `fetch_primary` que falla se usa el respaldo y la fuente es `"fredgraph-csv"`; test que si ambas fallan se lanza `RuntimeError` nombra la serie y en `tmp_path` no se escribe ni archivo ni manifiesto; test que una segunda descarga el mismo día lanza `FileExistsError` y el archivo original queda intacto; test que el manifiesto conserva sus filas previas; test que entre dos fechas `load_latest_raw` elige la más reciente; test que sin manifiesto lanza `FileNotFoundError` con mensaje que contiene `data --download`.
  - Implementación: `fetch_primary`, `fetch_fallback`, `download_all`, `raw_path`, `save_downloads`, `read_manifest`, `load_latest_raw`. Manifiesto con columnas `series, download_date, source, file, n_rows, first_obs, last_obs`. `load_latest_raw` lee con `dtype=str` y `keep_default_na=False`.
  - Hecho cuando: tests en verde; `download_all` con `fetch_primary` que falla usa respaldo; doble fallo lanza `RuntimeError` sin escribir archivos; `load_latest_raw` sin manifiesto lanza `FileNotFoundError` con `data --download`.

- [x] **T4. Descarga real única y verificación de unidades.** RF-1, RF-2, RF-3, RF-4, RF-5 · agente: implementer
  - Ejecutar `uv run python -m src.pipeline data --download`. Verificar en FRED (`https://fred.stlouisfed.org/series/<ID>`) las unidades de cada serie: morosidad y castigos en porcentaje; GDPC1 en miles de millones de dólares encadenados (año base según FRED); GDP y LOANS en miles de millones de dólares; UNRATE y FEDFUNDS en porcentaje; CPIAUCSL como índice; USREC como indicador 1/0. Rellenar `SERIES_META` en `src/config.py` con las unidades verificadas. Commit de `data/raw/`.
  - Hecho cuando: 13 archivos en `data/raw/` con fecha de hoy; `manifest.csv` con 13 filas; unidades verificadas en FRED y documentadas en `SERIES_META`; commit realizado.

- [x] **T5. `src/panel.py`: validación, agregación trimestral y completitud.** RF-7, RF-8, RF-11, RF-12, RF-13, RF-25 · agente: implementer
  - Tests primero (datos sintéticos): `parse_raw`: «.», «» y «NaN» pasan a NaN; «abc» → `DataError` con la serie; 0 filas → error; primera obs. 1999-01-01 → error. Media trimestral de meses conocidos. CPI sin 2025-10 → media(nov, dic) y `"RF-11"`; con 2025-10 → tres meses y `"RF-12"`. FEDFUNDS sin 2025-10 → `DataError` con «FEDFUNDS» y «2025». Un trimestre interior sin DRALACBS → error con serie y trimestre. GDPC1 sin 1999T1 → error de cobertura 2000T1. Un último trimestre con un mes → excluido, con motivo en `excluded_tail`. Una serie de robustez que termina antes → NaN terminal sin recortar el panel; un NaN interior → error. USREC con un mes en 1 → 1.
  - Implementación: `DataError`, `parse_raw`, `quarter_months`, `quarterly_from_monthly`, `recession_indicator`, `quarterly_from_quarterly`, `last_common_quarter`, `check_main_complete`, `check_terminal_only`.
  - Hecho cuando: tests en verde; `parse_raw` convierte «.», «» y «NaN» a NaN y lanza `DataError` con «abc»; `quarterly_from_monthly` aplica RF-11/RF-12 solo a CPIAUCSL y UNRATE; `check_main_complete` nombra serie y trimestre; `check_terminal_only` registra faltante terminal sin recortar.

- [x] **T6. `src/panel.py`: transformaciones y `build_panel`.** RF-9, RF-10, RF-14, RF-15, RF-16 · agente: implementer
  - Tests primero (datos sintéticos): `yoy` de x = exp(0,01·t) da 4,0 exacto y usa t−4 aunque falte una fila. `diff_pp` es conocido. `logit_rate(50) == 0`; 0 y 100 → error con serie y trimestre. `transform` produce las 25 columnas sobre la historia desde 1998. `build_panel` recorta a 2000T1–end y lanza `DataError` si hay NaN en columnas principales.
  - Implementación: `yoy`, `diff_pp`, `logit_rate`, `transform`, `build_panel`, `PanelResult` (dataclass congelado con `full`, `panel`, `end`, `excluded_tail`, `gap_treatment`, `terminal_gaps`, `observed`).
  - Hecho cuando: tests en verde; `yoy` de exp(0,01·t) da 4,0; `logit_rate(50) == 0` y lanza `DataError` con 0 y 100; `build_panel` produce panel con 25 columnas desde 2000T1.

- [x] **T7. `src/stationarity.py`: ADF, KPSS, regla de decisión y tabla.** RF-19, RF-20, RF-21 · agente: implementer
  - Tests primero (datos sintéticos): tabla de verdad de `decide` (4 casos más el borde p = 0,05 → «no rechaza»). Los tres casos de `integration_order`. Ruido blanco (n = 400) → «niveles», I(0). Paseo aleatorio (n = 400) → «primera diferencia», I(1). `adf_lags ≤ 4`. Se registra el truncado de KPSS. La tabla tiene 2 filas por variable y excluye `usrec` y `_d`.
  - Implementación: `adf_test`, `kpss_test`, `rejects`, `is_stationary`, `decide`, `integration_order`, `stationarity_table`. ADF con `maxlag=4, regression="c", autolag="AIC"`. KPSS con `regression="c", nlags="auto"`. Captura de `InterpolationWarning` para marcar `pvalue_truncated`.
  - Hecho cuando: tests en verde; `decide` cubre los 4 casos más el borde; ruido blanco → «niveles» e I(0); paseo aleatorio → «primera diferencia» e I(1); tabla con 34 filas (17 variables × 2 formas).

- [x] **T8. `src/descriptives.py`, `src/tables.py`, `src/data_note.py`, `src/report_vars.py`.** RF-17, RF-18 · agente: implementer
  - Tests primero: descriptivos de una columna conocida. `fmt_es(2.345) == "2,35"`. `to_markdown` produce una cabecera pipe. La nota de datos contiene los 13 códigos, «2025T4», «LOANS», «FEDFUNDS» y el trimestre final. `data_variables` trae todas las claves del bloque `datos:`.
  - Implementación: `descriptive_table` (n, media, desv. est. ddof=1, mín., mediana, máx.), `fmt_es`, `quarter_label`, `to_markdown`, `build_data_note`, `data_variables`.
  - Hecho cuando: tests en verde; `fmt_es(2.345) == "2,35"`; nota de datos contiene los 13 códigos, «2025T4», «LOANS», «FEDFUNDS» y el trimestre final; `data_variables` trae todas las claves del bloque `datos:`.

- [x] **T9. `src/figures.py`: gráfico de morosidad, desempleo y FFR.** RF-22 · agente: implementer
  - Tests primero: la figura tiene 3 líneas, ylabel con «%», leyenda en español y tantos sombreados como rachas de recesión.
  - Implementación: `plot_delinquency_macro(panel) -> matplotlib.figure.Figure`. Tres líneas (DRALACBS, UNRATE, FEDFUNDS), eje único «Porcentaje (%)», sombreado de recesiones desde el primer trimestre de `usrec == 1` hasta el inicio del siguiente, sombreado termina donde termina USREC. Sin título.
  - Hecho cuando: test en verde; figura con 3 líneas, ylabel «Porcentaje (%)», leyenda en español y sombreados correctos.

- [x] **T10. `src/pipeline.py`: CLI, orquestación y escritura de salidas.** RNF-1 · agente: implementer
  - Tests primero: `test_frozen_data` sobre `data/raw/` real: las 13 series están en el manifiesto; el panel empieza en 2000T1 y termina en `result.end`; tiene 25 columnas y ningún NaN en columnas principales. RNF-1: `data` dos veces en dos `tmp_path` da bytes idénticos en `panel.csv`, `descriptives.csv` y `stationarity.csv`. `test_purity`: los módulos puros no importan `requests`, `pandas_datareader`, `matplotlib` ni usan `open(`; ningún archivo de `src/` contiene `fillna`, `ffill`, `bfill`, `interpolate` ni `dropna`.
  - Implementación: `src/pipeline.py` con `argparse`, `matplotlib.use("Agg")`, rutas relativas a la raíz. Etapas `data`, `models`, `stress`, `report`. `data --download` descarga y construye; `data` construye desde `data/raw/`; `all` recorre las etapas. Escritura de `data/processed/panel.csv`, `outputs/tables/*.csv|md`, `outputs/data_note.md`, `outputs/figures/delinquency_unemployment_ffr.png`, bloque `datos:` de `report/_variables.yml`.
  - Hecho cuando: tests en verde; `uv run python -m src.pipeline data` produce todas las salidas; dos ejecuciones dan bytes idénticos; módulos puros no importan ni usan funciones prohibidas.

- [x] **T11. `notebooks/01_datos_fred.ipynb`: notebook educativo y test.** RF-23, RF-24 · agente: implementer
  - Tests primero: ejecuta las celdas de código con `exec`, sin error. Con `RAW_DIR` apuntando a un directorio vacío, falla con `FileNotFoundError` y el mensaje claro. El código del notebook no llama a `DataReader`.
  - Implementación: notebook con celdas en orden: (1) explica qué es FRED, ejemplo de la guía en markdown no ejecutado; (2) localiza la raíz y define `RAW_DIR`; (3) llama a `load_latest_raw(RAW_DIR)`; (4) reproduce el ejemplo combinando GDP, UNRATE, CPIAUCSL y FEDFUNDS de 2000-01-01 a 2026-01-01; (5) explica agregación trimestral, excepción 2025T4 y transformaciones; (6) ejecuta `build_panel(raw)` y muestra `result.panel.head()`, `result.panel.tail()` y `result.end`. Versionado sin salidas.
  - Hecho cuando: test en verde; notebook ejecuta sin errores con `exec`; con `RAW_DIR` vacío falla con `FileNotFoundError` y mensaje que menciona `data --download`; código no llama a `DataReader`.

## Tabla RF → tareas

| RF / RNF | Tareas |
|---|---|
| RF-1 | T2, T3, T4 |
| RF-2 | T3, T4 |
| RF-3 | T3, T4 |
| RF-4 | T3, T4 |
| RF-5 | T3, T4 |
| RF-6 | T3 |
| RF-7 | T5 |
| RF-8 | T5 |
| RF-9 | T6 |
| RF-10 | T6 |
| RF-11 | T5 |
| RF-12 | T5 |
| RF-13 | T5 |
| RF-14 | T6, T10 |
| RF-15 | T6 |
| RF-16 | T6 |
| RF-17 | T2, T8 |
| RF-18 | T8 |
| RF-19 | T7 |
| RF-20 | T7 |
| RF-21 | T7 |
| RF-22 | T9 |
| RF-23 | T11 |
| RF-24 | T3, T11 |
| RF-25 | T5 |
| RNF-1 | T10 |
| RNF-2 | T1 |
| RNF-3 | T5, T6, T7 |
| RNF-4 | T1 |
| RNF-5 | T2 |
| RNF-6 | T10 |
