# Plan 001 — Datos
Estado: aprobada · Spec: `specs/001-datos/spec.md` (aprobada, Crítica: no) · Depende de: ninguna spec

Este plan fija el CÓMO de la spec 001. No cambia ningún requisito. Las dudas abiertas de la spec (PIB real o nominal, muestra desde 1985 y formato del informe) no bloquean esta spec: el panel trae GDPC1 y GDP, y la descarga parte de 1998.

## 1. Módulos de `src/` y responsabilidad

| Módulo | Responsabilidad | ¿Red/disco/gráficos? | RF |
|---|---|---|---|
| `src/config.py` | Constantes: listas de series, fechas, umbral α, metadatos de cada serie (unidad, frecuencia, tratamiento), etiquetas en español, rutas. | No (solo constantes) | RF-1, RF-17, RNF-5 |
| `src/fred_io.py` | Único módulo con red y disco de datos: descarga (principal y respaldo), guardado crudo, manifiesto, lectura de la descarga más reciente. | Sí | RF-1 a RF-6 |
| `src/panel.py` | Funciones puras: validación de la descarga, agregación trimestral, completitud, último trimestre común, transformaciones, recorte y control de faltantes. | No | RF-7 a RF-16, RF-25 |
| `src/stationarity.py` | Funciones puras: ADF, KPSS, regla de decisión, orden de integración y tabla. | No | RF-19 a RF-21 |
| `src/descriptives.py` | Función pura de la tabla de descriptivos. | No | RF-18 |
| `src/data_note.py` | Función pura que devuelve la nota de datos en Markdown (texto en español). | No | RF-17 |
| `src/tables.py` | Funciones puras de formato: número con coma decimal y tabla Markdown sin dependencias. | No | RF-18, RF-19, RNF-5 |
| `src/report_vars.py` | Función pura que devuelve el bloque `datos:` de `report/_variables.yml`. | No | Principio 5 |
| `src/figures.py` | Construye y devuelve la `Figure` de RF-22; no la guarda. | Gráficos (sin disco) | RF-22 |
| `src/pipeline.py` | CLI `python -m src.pipeline`; orquesta, lee y escribe disco. | Sí | Principio 1, RNF-1 |
| `notebooks/01_datos_fred.ipynb` | Notebook educativo en español. | Disco (lectura) | RF-23, RF-24 |
| `tests/conftest.py` | Bloqueo de red en todos los tests. | — | RNF-2 |

Las funciones de `panel`, `stationarity`, `descriptives`, `data_note`, `tables` y `report_vars` no importan `requests`, `pandas_datareader`, `matplotlib`, `pathlib` ni `open` (RNF-6). Un test lo comprueba leyendo el código fuente.

## 2. Funciones y firmas

Convenciones: las series trimestrales se indexan con `pd.PeriodIndex` de frecuencia `Q-DEC`. Las mensuales se indexan con `PeriodIndex` mensual. Los errores de datos son `DataError(ValueError)`, definido en `src/panel.py`, con un mensaje que nombra la serie y el período.

### `src/config.py`
```python
MAIN_SERIES = ["DRALACBS", "GDPC1", "GDP", "UNRATE", "CPIAUCSL", "FEDFUNDS", "LOANS"]
ROBUSTNESS_SERIES = ["DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS", "CORALACBS"]
RECESSION_SERIES = "USREC"
ALL_SERIES = MAIN_SERIES + ROBUSTNESS_SERIES + [RECESSION_SERIES]          # 13
MONTHLY = {"UNRATE", "CPIAUCSL", "FEDFUNDS", "LOANS", "USREC"}
DELINQUENCY = ["DRALACBS", "DRALACBN", "DRCLACBS", "DRBLACBS", "DRSREACBS"]
DOWNLOAD_START = "1998-01-01"
SAMPLE_START = pd.Period("2000Q1", "Q-DEC")
DOCUMENTED_GAP_SERIES = {"CPIAUCSL", "UNRATE"}
DOCUMENTED_GAP_MONTH = pd.Period("2025-10", "M")
ALPHA = 0.05
ADF_MAXLAG = 4
SERIES_META: dict[str, dict]   # unidad, frecuencia original, desestacionalización, tratamiento trimestral, nombre en español
COLUMN_LABELS: dict[str, str]  # columna del panel -> etiqueta en español con unidad
```
`SERIES_META` se llena en la tarea de descarga copiando la unidad desde `https://fred.stlouisfed.org/series/<ID>`. No se inventa ninguna unidad. Valores esperados, que la tarea debe verificar: morosidad y castigos en porcentaje; GDPC1 en miles de millones de dólares encadenados (año base según FRED); GDP y LOANS en miles de millones de dólares; UNRATE y FEDFUNDS en porcentaje; CPIAUCSL como índice; USREC como indicador 1/0.

### `src/fred_io.py` (red y disco)
```python
def fetch_primary(series_id: str, start: str) -> pd.DataFrame           # pandas-datareader
def fetch_fallback(series_id: str) -> str                                # texto del CSV de fredgraph
def download_all(series: list[str], start: str,
                 fetch_primary=fetch_primary, fetch_fallback=fetch_fallback
                 ) -> dict[str, tuple[str, str]]                         # id -> (texto CSV, fuente)
def raw_path(raw_dir: Path, series_id: str, day: date) -> Path           # <ID>_<AAAA-MM-DD>.csv
def save_downloads(downloads, raw_dir: Path, day: date) -> list[dict]    # filas del manifiesto
def read_manifest(raw_dir: Path) -> pd.DataFrame
def load_latest_raw(raw_dir: Path) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]
```
- `fuente` vale `"pandas-datareader"` o `"fredgraph-csv"`.
- Columnas del manifiesto `data/raw/manifest.csv`: `series, download_date, source, file, n_rows, first_obs, last_obs`.
- Las funciones de descarga se inyectan como parámetros, para probar el respaldo sin red.
- `load_latest_raw` lee cada CSV con `dtype=str` y `keep_default_na=False`. Así la validación ve el texto tal cual.
- `load_latest_raw` lanza `FileNotFoundError("No hay descargas crudas en <ruta>: ejecuta `uv run python -m src.pipeline data --download`")` si falta el manifiesto o algún archivo (RF-24).

### `src/panel.py` (puras)
```python
class DataError(ValueError): ...

def parse_raw(raw: pd.DataFrame, series_id: str, start: str = DOWNLOAD_START) -> pd.Series   # RF-7
def quarter_months(monthly: pd.Series) -> pd.DataFrame       # por trimestre: n_meses, meses faltantes, media de los meses con dato
def quarterly_from_monthly(monthly: pd.Series, series_id: str) -> tuple[pd.Series, pd.Series, str | None]
    # (valor trimestral, trimestre completo bool, tratamiento 2025T4: "RF-11"|"RF-12"|None)
def recession_indicator(usrec_monthly: pd.Series) -> pd.Series   # 1 si algún mes = 1; NaN si el trimestre no tiene 3 meses
def quarterly_from_quarterly(q: pd.Series) -> tuple[pd.Series, pd.Series]
def last_common_quarter(complete: dict[str, pd.Series], series: list[str]) -> pd.Period
def check_main_complete(complete: dict[str, pd.Series], start: pd.Period, end: pd.Period) -> None   # RF-13
def check_terminal_only(values: pd.Series, name: str, start: pd.Period, end: pd.Period) -> pd.Period | None  # RF-25
def yoy(x: pd.Series) -> pd.Series                 # 100 * (ln x_t - ln x_{t-4})
def diff_pp(x: pd.Series) -> pd.Series             # x_t - x_{t-1}
def logit_rate(dr: pd.Series, series_id: str) -> pd.Series    # ln(DR/(100-DR)); DataError si DR <= 0 o >= 100 (RF-15)
def transform(quarterly: pd.DataFrame) -> pd.DataFrame       # RF-9, sobre la historia desde 1998
def build_panel(raw: dict[str, pd.DataFrame]) -> PanelResult
```
`PanelResult` es un `dataclass` congelado con estos campos:
- `full`: transformaciones sobre toda la historia (1998 en adelante).
- `panel`: el panel recortado a 2000T1–fin (RF-16).
- `end`: el último trimestre común.
- `excluded_tail`: lista de `(trimestre, serie, motivo)`. Explica por qué los trimestres posteriores a `end` no entran.
- `gap_treatment`: `{serie: "RF-11" | "RF-12"}` para CPIAUCSL y UNRATE.
- `terminal_gaps`: `{columna: último trimestre con dato}` para las series de RF-25.
- `observed`: `{serie: (primera obs, última obs, n filas)}`.

Columnas del panel. Son 25; `date` es el primer día del trimestre, según la convención de FRED.

| Grupo | Columnas |
|---|---|
| Morosidad (×5: dralacbs, dralacbn, drclacbs, drblacbs, drsreacbs) | `<id>`, `<id>_d`, `<id>_logit` |
| Variación interanual | `gdpc1_yoy`, `gdp_yoy`, `cpiaucsl_yoy`, `loans_yoy` |
| Nivel y diferencia | `unrate`, `unrate_d`, `fedfunds`, `fedfunds_d` |
| Otras | `coralacbs`, `usrec` |

### `src/stationarity.py` (puras)
```python
def adf_test(x: pd.Series, maxlag: int = ADF_MAXLAG) -> dict          # stat, pvalue, lags, n_obs
def kpss_test(x: pd.Series) -> dict                                   # stat, pvalue, pvalue_truncated
def rejects(p: float, alpha: float = ALPHA) -> bool                   # p < alpha
def is_stationary(adf_p: float, kpss_p: float, alpha=ALPHA) -> bool  # ADF rechaza y KPSS no rechaza
def decide(adf_p: float, kpss_p: float, alpha=ALPHA) -> str
    # "niveles" | "primera diferencia" | "ambigua (primera diferencia)"
def integration_order(decision: str, diff_stationary: bool) -> str    # "I(0)" | "I(1)" | "posible I(2)"
def stationarity_table(full: pd.DataFrame, columns: list[str], start: pd.Period, end: pd.Period) -> pd.DataFrame
```
- ADF: `adfuller(x, maxlag=4, regression="c", autolag="AIC")`.
- KPSS: `kpss(x, regression="c", nlags="auto")`. En statsmodels, `"auto"` es el ancho de banda automático de Hobijn et al. (1998), basado en Newey-West (1994).
- KPSS solo da p-valores interpolados entre 0,01 y 0,10. Fuera de ese rango, statsmodels emite `InterpolationWarning` y recorta el p-valor. La función captura el aviso y marca `pvalue_truncated` con `"<0,01"`, `">0,10"` o `""`. La regla de decisión no cambia, porque ambos bordes quedan del mismo lado de 0,05.
- Columnas probadas: las 17 variables del panel que no son `usrec` ni terminan en `_d`.

### `src/descriptives.py`, `src/tables.py`, `src/data_note.py`, `src/report_vars.py`, `src/figures.py`
```python
def descriptive_table(panel: pd.DataFrame, exclude=("usrec",)) -> pd.DataFrame   # n, media, desv. est. (ddof=1), mín., mediana, máx.
def fmt_es(x: float, decimals: int = 2) -> str                                   # 2.3456 -> "2,35"; NaN -> "—"
def quarter_label(q: pd.Period) -> str                                           # 2026Q2 -> "2026T2"
def to_markdown(df: pd.DataFrame, decimals: int = 2) -> str                      # tabla pipe sin dependencias
def build_data_note(result: PanelResult, manifest: pd.DataFrame, meta: dict) -> str
def data_variables(result: PanelResult, stationarity: pd.DataFrame, manifest: pd.DataFrame) -> dict
def plot_delinquency_macro(panel: pd.DataFrame) -> matplotlib.figure.Figure
```

## 3. Algoritmo (pseudocódigo)

```
pipeline data [--download]
  si --download:                                     # RF-1..RF-5; la única etapa con red
      hoy = date.today()
      si existe algún data/raw/<ID>_<hoy>.csv: detener("ya hay una descarga de <ID> con fecha <hoy>")   # caso límite
      downloads = {}
      para id en ALL_SERIES:
          intentar texto, fuente = fetch_primary(id, 1998-01-01) → CSV; "pandas-datareader"
          si falla: intentar texto = fetch_fallback(id); fuente = "fredgraph-csv"          # RF-2
                    si falla: detener("No se pudo descargar <ID> ni por pandas-datareader ni por el CSV de FRED")  # RF-3
          parse_raw(texto, id)                       # RF-7 antes de guardar nada
          downloads[id] = (texto, fuente)
      save_downloads(downloads, data/raw, hoy)       # todo o nada: se escribe solo si las 13 bajaron bien (RF-3, RF-4)
      añadir 13 filas a manifest.csv                 # RF-5; solo se añaden filas, nunca se reescriben

  raw, manifest = load_latest_raw(data/raw)          # RF-6: por serie, la fila de mayor download_date
  result = build_panel(raw)
  stat = stationarity_table(result.full, TESTED, 2000Q1, result.end)
  desc = descriptive_table(result.panel)
  escribir data/processed/panel.csv, outputs/tables/*.csv|md, outputs/data_note.md, figura, bloque datos: de _variables.yml

build_panel(raw):
  s = {id: parse_raw(raw[id], id)}                   # "." , "" y NaN -> NaN; otro texto -> DataError (RF-7)
  para id mensual (no USREC): valor, completo, trat = quarterly_from_monthly(s[id], id)   # RF-8, RF-11, RF-12
       quarterly_from_monthly:
         por trimestre: meses = 3 meses del calendario; con_dato = meses no NaN
         si len(con_dato) == 3: valor = media(3), completo = True
         si id ∈ {CPIAUCSL, UNRATE} y trimestre == 2025Q4 y faltan exactamente {2025-10}:
             valor = media(nov, dic), completo = True, trat = "RF-11"
         si no: valor = NaN, completo = False         # nunca media de 1 o 2 meses en silencio
         si 2025-10 tiene dato en CPI/UNRATE: trat = "RF-12"
  para id trimestral: valor = s[id] en PeriodIndex Q; completo = no NaN       # RF-8 (fin de periodo)
  usrec = recession_indicator(s[USREC])              # RF-9
  end = último q tal que completo[id][q] para todo id ∈ MAIN_SERIES
  excluded_tail = para cada q > end hasta el último trimestre con algún dato: qué serie principal está incompleta y cuántos meses tiene
  check_main_complete(principales, 1998Q1, end)      # RF-13: el primer hueco nombra serie y trimestre (o mes)
  Q = DataFrame trimestral reindexado al rango completo 1998Q1..max   # reindex sin relleno: shift(4) = t-4 de verdad
  full = transform(Q)                                # RF-9 sobre la historia desde 1998
  panel = full.loc[2000Q1:end]                       # RF-10
  para columnas principales: si hay NaN en panel -> DataError(columna, trimestre)    # cobertura 2000T1 (RF-13)
  para columnas de robustez y usrec: check_terminal_only -> registra el último trimestre con dato; un NaN interior -> DataError (RF-25)
  return PanelResult(...)

transform(Q):                                        # RF-9
  para id en DELINQUENCY: <id> = Q[id]; <id>_d = diff_pp; <id>_logit = logit_rate (DataError si DR∉(0,100), RF-15)
  gdpc1_yoy, gdp_yoy, cpiaucsl_yoy, loans_yoy = yoy(...)
  unrate, unrate_d, fedfunds, fedfunds_d = nivel y diff_pp
  coralacbs = nivel; usrec = indicador

stationarity_table(full, cols, start, end):          # RF-19..RF-21
  para col en cols:
     nivel = full[col].loc[start:end]
     dif   = full[col].diff().loc[start:end]         # diferencia sobre la historia descargada (Definiciones)
     para forma, x en [("tal cual", nivel), ("primera diferencia", dif)]:
        x = x.loc[:último índice con dato]           # solo afecta a series de RF-25; n_obs se reporta
        adf = adf_test(x); kpss = kpss_test(x)
     decision = decide(adf_nivel.p, kpss_nivel.p)
     orden = integration_order(decision, is_stationary(adf_dif.p, kpss_dif.p))
  filas (largo): variable, etiqueta, forma, n_obs, adf_stat, adf_p, adf_lags, kpss_stat, kpss_p, kpss_p_truncado, decision, orden
```

## 4. Salidas exactas

| Archivo | Contenido | RF |
|---|---|---|
| `data/raw/<ID>_<AAAA-MM-DD>.csv` (×13) | Descarga cruda. Se escribe una vez y no se edita. Respaldo: el texto del CSV de FRED tal cual. Vía principal: `date,<ID>` escrito con `to_csv` a partir de lo que devuelve pandas-datareader. | RF-1, RF-4 |
| `data/raw/manifest.csv` | Una fila por descarga; solo se añaden filas. | RF-5 |
| `data/processed/panel.csv` | 25 columnas más `date`, de 2000T1 al fin; floats a precisión completa. | RF-16 |
| `outputs/data_note.md` | Nota de datos en español (contenido abajo). | RF-11, RF-12, RF-17, RF-25 |
| `outputs/tables/descriptives.csv` y `.md` | 24 variables (todas menos `usrec`) × n, media, desv. est., mín., mediana, máx. | RF-18 |
| `outputs/tables/stationarity.csv` y `.md` | 34 filas (17 variables × 2 formas), con decisión y orden. El `.csv` lo leen las specs 003 y 004. | RF-19 a RF-21 |
| `outputs/figures/delinquency_unemployment_ffr.png` | Figura de RF-22, 8×4,5 pulgadas, 200 dpi. | RF-22 |
| `report/_variables.yml` | Solo se reescribe la clave `datos:`; las demás claves se conservan. | Principio 5 |
| `notebooks/01_datos_fred.ipynb` | Notebook educativo, versionado sin salidas. | RF-23, RF-24 |

**Nota de datos (`outputs/data_note.md`).** Todo el texto variable sale del manifiesto y de `PanelResult`. Contiene:
1. Una tabla por serie: código, nombre, fuente («FRED, vía pandas-datareader» o «FRED, vía CSV público»), unidad, frecuencia original, rango descargado (primera y última observación), fecha de descarga y tratamiento trimestral («media de los meses del trimestre», «dato de fin de periodo» o «1 si algún mes está en recesión»).
2. La muestra: 2000T1 al fin. Incluye el motivo del corte, generado desde `excluded_tail` (por ejemplo, «2026T3 queda fuera: DRALACBS no tiene dato»).
3. 2025T4 de CPIAUCSL y UNRATE: RF-11 (dos meses) o RF-12 (tres meses). Lista los cálculos de la muestra que usan ese promedio: el nivel y la diferencia de 2025T4, la diferencia de 2026T1 y la variación interanual de 2025T4. También la de 2026T4 en adelante, si entra en la muestra.
4. La mezcla de frecuencias: la morosidad y los castigos son datos de fin de periodo; las mensuales son promedios del trimestre.
5. Por qué LOANS mide el crédito: cubre préstamos y arrendamientos de todos los bancos comerciales (H.8), el mismo universo que el denominador de DRALACBS. Se usa su variación interanual.
6. Por qué FEDFUNDS entra en nivel y en diferencia: el nivel mide la postura de la política monetaria; la diferencia trimestral es el «cambio en la FFR» que pide la sección 3.4 de la guía. Cuál entra en cada modelo lo deciden las specs 003 y 004.
7. Series con faltante terminal (RF-25), con su último trimestre con dato. También dónde termina el sombreado de recesiones.

**Claves de `report/_variables.yml`.** Son textos ya formateados con coma decimal y dos decimales; los trimestres van como `AAAAT#`.
```yaml
datos:
  muestra_inicio: "2000T1"
  muestra_fin: "2026T2"           # calculado, no fijo
  n_trimestres: "106"
  n_series: "13"
  fecha_descarga: "2026-10-03"    # la más reciente entre las descargas usadas
  trimestres_excluidos: "2026T3"
  cpiaucsl_2025t4_meses: "2"
  unrate_2025t4_meses: "2"
  dralacbs_media: "…"   dralacbs_desv: "…"
  dralacbs_max: "…"     dralacbs_max_trimestre: "…"
  dralacbs_min: "…"     dralacbs_min_trimestre: "…"
  dralacbs_ultimo: "…"
  unrate_max: "…"       unrate_max_trimestre: "…"
  fedfunds_max: "…"     fedfunds_ultimo: "…"
  decision:  {<variable>: "niveles" | "primera diferencia" | "ambigua (primera diferencia)"}   # 17
  orden:     {<variable>: "I(0)" | "I(1)" | "posible I(2)"}                                    # 17
  n_ambiguas: "…"
```
Los valores de ejemplo de este bloque son ilustrativos: todos los calcula el código.

**Figura (RF-22).**
- Muestra tres líneas: «Tasa de morosidad (DRALACBS)», «Tasa de desempleo (UNRATE)» y «Tasa de fondos federales (FEDFUNDS)».
- El eje x va de 2000T1 al fin; cada trimestre se fecha en su primer día.
- Hay un solo eje y, «Porcentaje (%)», con leyenda en español.
- Cada racha de `usrec == 1` se sombrea de su primer trimestre al inicio del siguiente.
- El sombreado termina donde termina el último dato de USREC (RF-25).
- La figura no lleva título; el pie y la fuente los pone el informe.

## 5. Integración en `uv run python -m src.pipeline <etapa>`

```
uv run python -m src.pipeline data --download   # descarga (red) + construye todo
uv run python -m src.pipeline data              # construye todo desde data/raw congelado (sin red)
uv run python -m src.pipeline all               # data (sin --download) → models → stress → report
```
- `models`, `stress` y `report` existen como etapas registradas. Hasta sus specs (003, 004, 005 y 006), terminan con «Etapa <x> pendiente (spec NNN)» y código de salida 0. `all` las recorre e informa cuáles están pendientes.
- `src/pipeline.py` usa `matplotlib.use("Agg")`, rutas relativas a la raíz del repositorio y `argparse`. No contiene lógica de cálculo.

## 6. Decisiones técnicas (con su alternativa descartada)

| # | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|
| D1 | La red solo se usa con `data --download`. Sin el flag, `data` y `all` construyen desde `data/raw/` congelado. | Principio 1 y RNF-1: `all` debe reproducir siempre lo mismo. Si descargara, cambiaría con las revisiones de FRED y se detendría al repetirse el mismo día (caso límite). RF-1 se cumple porque `--download` es parte de la etapa de datos. | Descargar en cada `data`/`all`: el resultado no es reproducible y la segunda ejecución del día falla. **Revísala**: es la lectura que hago de RF-1. |
| D2 | La descarga es todo o nada: se valida en memoria y se escribe solo si las 13 series bajaron bien. | RF-3 pide no registrar la serie que falla. Así tampoco quedan corridas a medias que bloqueen el reintento del mismo día. | Guardar cada serie al llegar: deja un manifiesto parcial y archivos que impiden reintentar ese día. |
| D3 | Los CSV crudos se leen con `dtype=str` y `keep_default_na=False`. Solo «.», «» y «NaN» pasan a faltante. | RF-7: los valores por defecto de pandas convierten en silencio «NA», «null», «n/a», etc. | `pd.read_csv` por defecto. |
| D4 | Formato crudo en CSV de texto. El respaldo guarda el texto de FRED tal cual; la vía principal escribe `date,<ID>` desde el DataFrame. | Diffable en git y sin dependencias. | Parquet (requiere pyarrow) o pickle (opaco y frágil entre versiones). |
| D5 | Completitud explícita por número de meses. Un trimestre incompleto vale NaN, salvo la excepción de RF-11. | Con `resample().mean()`, un trimestre con 1 o 2 meses tendría media en silencio. Eso viola RF-13 y RF-14. | `resample("QS").mean()`. |
| D6 | `PeriodIndex` trimestral, reindexado al rango completo antes de `shift`. | Así `shift(4)` es t−4 de verdad, no «cuatro filas atrás», aunque falte una fila. Reindexar no rellena valores. | Indexar por fecha y hacer `shift` sobre las filas. |
| D7 | USREC trimestral exige los tres meses; si no, es NaN terminal. | Mismo criterio de «trimestre completo». Evita sombrear con datos parciales. | «Algún mes disponible = 1»: depende de cuántos meses haya. |
| D8 | KPSS con `nlags="auto"` (Hobijn et al., 1998, sobre Newey-West, 1994). Se registra si el p-valor está truncado. | Es la especificación pre-registrada. El truncamiento no cambia la decisión, pero se declara. | `nlags="legacy"` (regla de Schwert): no es Newey-West automático. |
| D9 | Las pruebas de una serie con faltante terminal (RF-25) usan su tramo observado y reportan `n_obs`. | Las pruebas no admiten NaN. No se borra ninguna fila del panel y la diferencia de tamaño queda a la vista. | Detener el pipeline o excluir la serie de la tabla. |
| D10 | Tablas Markdown con una función propia (`to_markdown`). | `DataFrame.to_markdown` exige `tabulate`, una dependencia nueva. | Añadir `tabulate`. |
| D11 | `_variables.yml` guarda textos ya formateados («2,35»). La etapa reescribe solo la clave `datos:`. | El informe va en español con coma decimal. Las demás specs escriben sus propias claves sin pisarse. | Floats crudos: Quarto imprimiría «2.3456789». |
| D12 | El test ejecuta el notebook leyendo su JSON con `json` y ejecutando sus celdas de código en orden, con `exec`. El notebook se versiona sin salidas. | No añade dependencias, no arranca un kernel en CI y es determinista. | `nbclient`/`nbconvert`: es una dependencia nueva, que habría que preguntar antes. Solo hace falta si quieres el notebook versionado con sus salidas. |
| D13 | `tests/conftest.py` con un fixture `autouse` que sustituye `socket.socket.connect`, `socket.create_connection` y `socket.getaddrinfo` por una función que lanza `RuntimeError("Red bloqueada en tests")`. | RNF-2 sin dependencias. | `pytest-socket`: dependencia nueva. |
| D14 | El fin de la muestra se calcula a partir de los datos; no se fija en 2026T2. | La spec define el último trimestre común. Fijarlo ocultaría un cambio en los datos. | Una constante `SAMPLE_END = 2026Q2`. |
| D15 | `pytest` con `pythonpath = ["."]` en `pyproject.toml`. El notebook añade la raíz a `sys.path`. | `src` no es un paquete instalado (no hay `build-system`). | Convertir el proyecto en paquete instalable: más cambios de los que pide la spec. |
| D16 | Los CSV de salida se escriben con `float_format=None` y `lineterminator="\n"`. | RNF-1: la salida es idéntica en Windows y en Linux (CI) y no pierde precisión. | Redondear al escribir: pierde información y no garantiza nada más. |
| D17 | El notebook reconstruye el panel con las mismas funciones de `src/`; no lee `data/processed/panel.csv`. | Funciona desde un clon limpio y no puede desincronizarse del pipeline. | Leer `panel.csv`: podría estar desactualizado. |

## 7. Notebook (`notebooks/01_datos_fred.ipynb`)

Celdas en orden, con markdown y comentarios en español:
1. Explica qué es FRED. Muestra el ejemplo de la guía con `web.DataReader(...)` en una celda **markdown**, no ejecutada, porque el notebook no usa la red.
2. Localiza la raíz (sube carpetas hasta encontrar `pyproject.toml`) y define `RAW_DIR = Path(os.environ.get("RAW_DIR", ROOT / "data" / "raw"))`.
3. Llama a `load_latest_raw(RAW_DIR)`. Si faltan descargas, el error explica que hay que ejecutar `uv run python -m src.pipeline data --download` (RF-24).
4. Reproduce el ejemplo: combina GDP, UNRATE, CPIAUCSL y FEDFUNDS en un DataFrame ancho, recortado de 2000-01-01 a 2026-01-01, y muestra `data.head()` (RF-23).
5. Explica paso a paso la agregación trimestral, la excepción de 2025T4 y las transformaciones.
6. Ejecuta `build_panel(raw)` y muestra `result.panel.head()`, `result.panel.tail()` y `result.end` (RF-16).

## 8. Estrategia de tests (pytest, sin red, semillas fijas)

Semilla única: `SEED = 20261002`, con `np.random.default_rng(SEED)`. Los datos sintéticos tienen resultado conocido; no se prueban las funciones de statsmodels (RNF-3).

| Archivo | Qué prueba | RF |
|---|---|---|
| `tests/conftest.py` + `test_network_blocked` | Abrir un socket lanza `RuntimeError`. | RNF-2 |
| `tests/test_fred_io.py` | Con `fetch_primary` inyectada que falla, se usa el respaldo y la fuente es `"fredgraph-csv"`. Si ambas fallan, `RuntimeError` nombra la serie y en `tmp_path` no se escribe ni archivo ni manifiesto. Una segunda descarga el mismo día lanza `FileExistsError` y el archivo original queda intacto. El manifiesto conserva sus filas previas. Entre dos fechas, `load_latest_raw` elige la más reciente. Sin manifiesto, lanza `FileNotFoundError` con un mensaje que contiene `data --download`. | RF-2 a RF-6, RF-24 |
| `tests/test_panel.py` | `parse_raw`: «.», «» y «NaN» pasan a NaN; «abc» → `DataError` con la serie; 0 filas → error; primera obs. 1999-01-01 → error. Media trimestral de meses conocidos. CPI sin 2025-10 → media(nov, dic) y `"RF-11"`; con 2025-10 → tres meses y `"RF-12"`. FEDFUNDS sin 2025-10 → `DataError` con «FEDFUNDS» y «2025». Un trimestre interior sin DRALACBS → error con serie y trimestre. GDPC1 sin 1999T1 → error de cobertura 2000T1. Un último trimestre con un mes → excluido, con motivo en `excluded_tail`. Una serie de robustez que termina antes → NaN terminal sin recortar el panel; un NaN interior → error. `yoy` de x = exp(0,01·t) da 4,0 exacto y usa t−4 aunque falte una fila. `diff_pp` es conocido. `logit_rate(50) == 0`; 0 y 100 → error con serie y trimestre. USREC con un mes en 1 → 1. | RF-7 a RF-15, RF-25 |
| `tests/test_stationarity.py` | Tabla de verdad de `decide` (4 casos más el borde p = 0,05 → «no rechaza»). Los tres casos de `integration_order`. Ruido blanco (n = 400) → «niveles», I(0). Paseo aleatorio (n = 400) → «primera diferencia», I(1). `adf_lags ≤ 4`. Se registra el truncado de KPSS. La tabla tiene 2 filas por variable y excluye `usrec` y `_d`. | RF-19 a RF-21 |
| `tests/test_outputs.py` | Descriptivos de una columna conocida. `fmt_es(2.345) == "2,35"`. `to_markdown` produce una cabecera pipe. La nota de datos contiene los 13 códigos, «2025T4», «LOANS», «FEDFUNDS» y el trimestre final. `data_variables` trae todas las claves. La figura tiene 3 líneas, ylabel con «%», leyenda en español y tantos sombreados como rachas de recesión. | RF-17, RF-18, RF-22 |
| `tests/test_frozen_data.py` | Sobre `data/raw/` real: las 13 series están en el manifiesto; el panel empieza en 2000T1 y termina en `result.end`; tiene 25 columnas y ningún NaN en columnas principales. RNF-1: `data` dos veces en dos `tmp_path` da bytes idénticos en `panel.csv`, `descriptives.csv` y `stationarity.csv`. | RF-5, RF-10, RF-16, RNF-1 |
| `tests/test_notebook.py` | Ejecuta las celdas de código con `exec`, sin error. Con `RAW_DIR` apuntando a un directorio vacío, falla con `FileNotFoundError` y el mensaje claro. El código del notebook no llama a `DataReader`. | RF-23, RF-24 |
| `tests/test_purity.py` | Los módulos puros no importan `requests`, `pandas_datareader`, `matplotlib` ni usan `open(`. Ningún archivo de `src/` contiene `fillna`, `ffill`, `bfill`, `interpolate` ni `dropna`. | RNF-6, RF-14 |
| `tests/test_harness.py` | Se sustituye el test de cifras por `find_hand_typed_numbers(text)`, con los patrones `(?<![\w.,])\d+[.,]\d+` y `(?<![\w.,])\d+\s?%`. Tests sintéticos: «0,8 pp» y «15 %» se detectan; `{{< var datos.muestra_fin >}}` y «2000T1» no. | RNF-4 |

Consecuencia de RNF-4 para la spec 006: los títulos del informe no pueden llevar «3.1» escrito a mano. Se numeran con `number-sections: true` de Quarto y se citan con `@sec-…`.

## 9. Cobertura de RF

| RF / RNF | Parte del plan |
|---|---|
| RF-1 a RF-5 | `fred_io` · `pipeline data --download` · D1, D2, D4 · `test_fred_io` |
| RF-6 | `fred_io.load_latest_raw` · `test_fred_io` |
| RF-7 | `panel.parse_raw` · D3 · `test_panel` |
| RF-8 | `panel.quarterly_from_monthly` y `quarterly_from_quarterly` · D5 |
| RF-9, RF-10 | `panel.transform` y `build_panel` · D6 |
| RF-11, RF-12 | `panel.quarterly_from_monthly` · nota de datos, punto 3 |
| RF-13 | `panel.check_main_complete` y control de NaN tras el recorte |
| RF-14 | Ningún relleno · D5 · `test_purity` |
| RF-15 | `panel.logit_rate` |
| RF-16 | `data/processed/panel.csv` |
| RF-17 | `data_note.build_data_note` → `outputs/data_note.md` |
| RF-18 | `descriptives.descriptive_table` → `outputs/tables/descriptives.*` |
| RF-19 a RF-21 | `stationarity` → `outputs/tables/stationarity.*` · D8, D9 |
| RF-22 | `figures.plot_delinquency_macro` → `outputs/figures/delinquency_unemployment_ffr.png` · D7 |
| RF-23, RF-24 | `notebooks/01_datos_fred.ipynb` · D12, D17 · `test_notebook` |
| RF-25 | `panel.check_terminal_only` · D7, D9 · nota de datos, punto 7 |
| RNF-1 | D14, D16 · `test_frozen_data` |
| RNF-2 | `conftest.py` · D13 |
| RNF-3 | `test_panel` y `test_stationarity` con datos sintéticos |
| RNF-4 | `test_harness.find_hand_typed_numbers` |
| RNF-5 | `config.COLUMN_LABELS` · nota, figura y notebook en español |
| RNF-6 | Separación de módulos (sección 1) · `test_purity` |

## 10. Orden sugerido para las tareas (lo detalla `/sdd-tasks`)
1. Configuración de pytest, `conftest.py` y endurecimiento de RNF-4.
2. `config` y `fred_io` con tests sin red.
3. Descarga real única (`data --download`), verificación de unidades en FRED y commit de `data/raw/`.
4. `panel`, la parte de agregación y completitud.
5. `panel`, la parte de transformaciones y `build_panel`.
6. `stationarity`.
7. Descriptivos, tablas, nota de datos y `report_vars`.
8. Figura.
9. `pipeline` y `test_frozen_data` (RNF-1).
10. Notebook y su test.

## 11. Notas para specs posteriores (no se implementan aquí)
- El panel empieza en 2000T1. Con rezagos de hasta 8 trimestres, los modelos perderían observaciones al inicio. Si las specs 003 y 004 necesitan rezagos anteriores a 2000T1, deberán pedirlo: por ejemplo, exponer `PanelResult.full` en un archivo.
- `outputs/tables/stationarity.csv` es la fuente de la decisión niveles o diferencias para los modelos.
