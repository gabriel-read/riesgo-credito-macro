# Plan 003 — Modelo I: determinantes macroeconómicos de la morosidad
Estado: aprobada · Spec: `specs/003-modelo-i/spec.md` (aprobada, Crítica: sí; pre-registro en el commit `667b313`, cambios C1–C3 del 5-oct-2026 antes de estimar) · Depende de: spec y plan 001 (implementados)

Este plan fija el CÓMO de la spec 003 y no cambia ningún requisito. Versiones disponibles en el entorno: statsmodels 0.15.0, pandas 2.2.3, numpy 2.1.3 y scipy 1.17.1 (scipy llega como dependencia de statsmodels). **No hace falta ninguna dependencia nueva.**

## 1. Módulos de `src/` y responsabilidad

| Módulo | Responsabilidad | ¿Red/disco/gráficos? | RF |
|---|---|---|---|
| `src/model1_config.py` (nuevo) | Constantes del pre-registro: términos, columnas, signos esperados, trimestres COVID, variantes R1–R8, formas esperadas, umbrales, quiebres de Chow, tramos fuera de muestra, semilla y etiquetas en español. | No | RF-3, RF-4, RF-9, RF-12, RF-16 |
| `src/design.py` (nuevo) | Funciones puras: forma de cada dependiente leída de la tabla de estacionariedad, control de formas esperadas, matriz de diseño, inicio y fin efectivos, y faltantes. | No | RF-1 a RF-6 |
| `src/estimation.py` (nuevo) | Funciones puras: ventana HAC, MCO + Newey-West, truncamiento espectral, inferencia desde (b, V), Wald, efectos de largo plazo con método delta, y efectos por 1 DE. | No | RF-6, RF-7, RF-9, RF-10 |
| `src/diagnostics.py` (nuevo) | Funciones puras: Breusch-Godfrey, Breusch-Pagan (Koenker), White, Jarque-Bera, RESET, VIF, Chow como Wald HAC y CUSUM. | No | RF-12 a RF-14 |
| `src/forecast.py` (nuevo) | Funciones puras: pronóstico a un paso y dinámico, reconstrucción del nivel, ingenuo, RMSE/MAE, Diebold-Mariano con corrección HLN y veredicto. | No | RF-18 |
| `src/model1.py` (nuevo) | Orquestación pura del Modelo I: estimación principal, tablas, robusteces, fuera de muestra, limitaciones, desviaciones y el diccionario para la spec 005. Devuelve un `Model1Result`. | No | RF-7 a RF-21 |
| `src/figures.py` (ampliado) | Tres funciones nuevas que devuelven `Figure`: coeficientes, CUSUM y fuera de muestra. | Gráficos (sin disco) | RF-11, RF-14, RF-19 |
| `src/report_vars.py` (ampliado) | `model1_variables(result) -> dict`, el bloque `modelo1:` con textos ya formateados. | No | RF-22 |
| `src/pipeline.py` (ampliado) | Etapa `models`: lee el disco, llama a `model1.run_model1`, escribe las salidas y la clave `modelo1:`. `all` pasa a ejecutar `models`. | Sí | RF-8, RF-23, RNF-5 |

Los módulos nuevos no importan `requests`, `pandas_datareader`, `matplotlib` ni `pathlib`, y no usan `open(`. Se amplían `test_pipeline_modules_pure` y `test_pipeline_no_open_in_pure_modules` (`tests/test_pipeline.py`) con la lista de módulos nuevos. Ningún módulo usa `fillna`, `ffill`, `bfill`, `interpolate` ni `dropna` sobre datos del modelo (RF-2).

## 2. Funciones y firmas

Convenciones heredadas de la 001:
- `pd.PeriodIndex` trimestral `Q-DEC`.
- Textos en español con `fmt_es` y `quarter_label` de `src/tables.py`.
- Errores de datos con una clase propia: `ModelDataError(ValueError)` en `src/design.py`, con un mensaje que nombra la variable, el trimestre y la regresión.

### `src/model1_config.py`
```python
SEED = 20261005
ALPHA = 0.05                 # significativo / veredicto de diagnósticos
ROBUST_ALPHA = 0.10          # criterio de robustez
LONGRUN_MIN_GAP = 0.05       # se reporta largo plazo solo si 1 - rho > 0.05
VIF_ALERT = 10.0
MIN_DOF = 30                 # RF-6
PSD_REL_TOL = 1e-10          # piso relativo de valores propios: tol = PSD_REL_TOL * max(|eig|)
MAIN_START = pd.Period("2000Q1", "Q-DEC")
LONG_START = pd.Period("1985Q1", "Q-DEC")
COVID_QUARTERS = ["2020Q2", "2020Q3", "2020Q4", "2021Q1"]
R1_EXCLUDED = ("2020Q1", "2021Q4")
CHOW_BREAKS = ["2008Q3", "2020Q2"]
BG_LAGS = 4
OOS_TRAIN = ("2000Q1", "2019Q4"); OOS_TEST_START = "2022Q1"; OOS_ANCHOR = "2021Q4"

# Términos internos (inglés) -> columna de la historia transformada
MACRO_TERMS = {"gdp_growth": "gdpc1_yoy", "d_unemp": "unrate_d", "inflation": "cpiaucsl_yoy",
               "d_ffr": "fedfunds_d", "credit_growth": "loans_yoy"}      # credit_growth se rezaga CREDIT_LAG
CREDIT_LAG = 4
EXPECTED_SIGN = {"gdp_growth": "-", "d_unemp": "+", "d_ffr": "+", "credit_growth": "+",
                 "inflation": None, "y_lag": None, "const": None}       # None = "sin contraste"; las dummies también
EXPECTED_FORMS = {  # RF-4: decisión leída el 5-oct-2026
    "dralacbs": "ambigua (primera diferencia)", "dralacbn": "ambigua (primera diferencia)",
    "dralacbs_logit": "primera diferencia", "drclacbs": "primera diferencia",
    "drblacbs": "primera diferencia", "drsreacbs": "ambigua (primera diferencia)"}
TERM_LABELS: dict[str, str]  # p. ej. "d_unemp" -> "ΔU (cambio trimestral del desempleo, pp)"

@dataclass(frozen=True)
class VariantSpec:
    id: str                    # "main", "R1", "R2", "R3_drclacbs", ..., "R8", "oos"
    label: str                 # en español, p. ej. "R6. Crédito rezagado 8 trimestres"
    dependent: str = "dralacbs"
    gdp_column: str = "gdpc1_yoy"
    credit_lag: int = 4
    start: pd.Period = MAIN_START
    end: pd.Period | None = None          # None = último trimestre común
    exclude: tuple[str, str] | None = None
    covid_dummies: bool = True
    seasonal_dummies: bool = False
    truncate_start: bool = False          # True en R6, R7 y R8: inicio = max(start, primer trimestre completo)
    in_pp: bool = True                    # False en R5 (logit)

MAIN = VariantSpec("main", "Especificación principal")
VARIANTS: list[VariantSpec]   # R1, R2, R3_drclacbs, R3_drblacbs, R3_drsreacbs, R4, R5, R6, R7, R8 (10)
```
Cada variante cambia un solo campo respecto de `MAIN`, más el ajuste mínimo de la spec:
- R1: `exclude=R1_EXCLUDED`. Sin dummies COVID, porque sus trimestres quedan fuera; `build_design` las omite si no tienen variación.
- R2: `dependent="dralacbn"`, `seasonal_dummies=True`.
- R3: una por sub-carteras, con `dependent=` la sub-cartera.
- R4: `gdp_column="gdp_yoy"`.
- R5: `dependent="dralacbs_logit"`, `in_pp=False`.
- R6 y R7: `credit_lag=8` o `12`, con `truncate_start=True`.
- R8: `start=LONG_START`, `truncate_start=True`.

### `src/design.py` (puras)
```python
class ModelDataError(ValueError): ...

def read_decisions(stationarity: pd.DataFrame) -> dict[str, str]
    # {columna: decision} de las filas "tal cual"; RF-3
def check_expected_forms(decisions: dict[str, str], expected: dict[str, str]) -> None
    # RF-4: ModelDataError("dralacbs: forma esperada '...' pero la tabla dice '...'; exige /sdd-change") si difiere o falta
def diff_form_stationary(stationarity: pd.DataFrame, column: str) -> tuple[str, str]
    # Aplica src.stationarity.decide e is_stationary a la fila "primera diferencia" de la columna; RF-15.
    # Se usa para ΔU, ΔFFR y para la dependiente y su rezago cuando entran en Δ (ΔDRALACBS se juzga con
    # su fila "primera diferencia", no con la "tal cual"). CRED(t−4) usa la fila "tal cual" de loans_yoy
    # sin rezagar (el rezago no cambia la serie), y el pie de la tabla lo dice.
def dependent_series(full: pd.DataFrame, column: str, decision: str) -> pd.Series
    # nivel si "niveles"; si no, full[column].diff() sobre la historia reindexada (no la columna _d, para que
    # el logit, que no tiene columna _d, siga la misma regla)
def build_design(full: pd.DataFrame, spec: VariantSpec, decision: str, end: pd.Period
                 ) -> Design
def effective_window(frame: pd.DataFrame, spec: VariantSpec, end: pd.Period) -> tuple[pd.Period, pd.Period]
```
`Design` es un `dataclass` congelado con estos campos: `y: pd.Series`, `X: pd.DataFrame` (columnas en orden fijo: `const`, `y_lag`, términos macro, dummies), `form: str` («nivel» | «primera diferencia»), `start`, `end`, `spec_id`, `dropped: list[str]` (dummies omitidas por no tener variación en la muestra, por ejemplo las COVID en R1).

Algoritmo de `build_design`:
1. Construye todas las columnas sobre `full` completo, desde 1998 y reindexado sin huecos. Así `shift(1)` y `shift(k)` son de verdad t−1 y t−k (D6 de la 001).
2. Calcula la ventana con `effective_window`:
   - El inicio es `spec.start` si `truncate_start=False`. Si es `True`, es el máximo entre `spec.start` y el primer trimestre con todos los términos.
   - El fin es `end`. Solo para una dependiente **alternativa** (`spec.dependent != "dralacbs"`) que termine antes por el faltante terminal de la 001, es su último trimestre con dato. En la principal y en las variantes con DRALACBS, un faltante al final es un NaN más y dispara el error del paso 4 (RF-1: 2000T1–2026T2 estricta).
3. Recorta a la ventana y quita los trimestres de `spec.exclude`. La exclusión es explícita, no un `dropna`.
4. Si queda cualquier NaN, lanza `ModelDataError(variable, trimestre, spec.id)` (RF-2).
5. Cada dummy COVID vale 1 en su trimestre. Las estacionales son de T2, T3 y T4, con T1 como base. Una dummy sin variación en la muestra se omite y se anota en `dropped`, **solo** si la variante es R1 o el tramo de estimación fuera de muestra. En cualquier otra variante, una dummy sin variación lanza `ModelDataError`, para que ninguna se pierda en silencio.

En R1, Newey-West trata 2019T4 y 2022T1 como contiguos. Además, Y(t−1) y CRED(t−4) de 2022T1 salen de trimestres excluidos, lo que es coherente con la «historia transformada». El pie de la tabla de robustez lo dice.

### `src/estimation.py` (puras)
```python
def hac_lags(nobs: int) -> int                            # floor(4*(T/100)**(2/9)); >= 1
def psd_truncate(V: np.ndarray, rel_tol: float = PSD_REL_TOL) -> tuple[np.ndarray, bool]
    # simetriza; si min eig <= rel_tol*max|eig| eleva esos eig al piso y reconstruye; devuelve (V', ajustada)
def fit_ols_hac(design: Design) -> Fit
def inference(params: pd.Series, cov: pd.DataFrame) -> pd.DataFrame
    # coef, se, z, p (normal bilateral), ic_inf, ic_sup (±1,959964·se)
def wald(params: pd.Series, cov: pd.DataFrame, R: np.ndarray, r: np.ndarray | None = None) -> dict
    # W = (Rb−r)'(RVR')⁻¹(Rb−r) ~ chi2(q); devuelve stat, df, p
def long_run(params, cov, term: str, lag_term: str = "y_lag", min_gap: float = LONGRUN_MIN_GAP) -> dict
    # si 1−rho <= min_gap: {"reported": False}; si no: estimate = b/(1−rho), grad = [1/(1−rho), b/(1−rho)^2],
    # se = sqrt(g' V_sub g), z, p, ic
def scale_effect(effect: dict, factor: float) -> dict     # multiplica estimate, se e IC por la DE; factor 0 -> "no definido"
def standardization_sd(design: Design) -> pd.Series       # DE (ddof=1) de cada regresor macro en la muestra principal sin 2020T2–2021T1 (C1)
def check_dof(design: Design) -> str | None               # motivo si nobs − k < MIN_DOF o rank(X) < k (RF-6)
```
`Fit` es un `dataclass` congelado con estos campos:
- `params` y `cov`: la covarianza HAC tras `psd_truncate`.
- `resid`, `fitted`, `nobs`, `k`, `hac_lags`, `psd_adjusted`, `rsquared`, `rsquared_adj`, `ser` (error estándar de la regresión).
- `design`.
- `sm_result`: el resultado de statsmodels, que solo usan los diagnósticos que lo necesitan.

Estimación: `sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": L, "kernel": "bartlett", "use_correction": False}, use_t=False)`, es decir, Newey-West puro, sin el factor n/(n−k) (D4). Toda la inferencia que se reporta sale de `inference(params, cov)` y no de los atributos de statsmodels, para que el tratamiento de la matriz se refleje en todo.

**Dummies de impulso y rango de V.** Cada dummy COVID vale 1 en un solo trimestre, así que el residuo de ese trimestre es exactamente 0. Su puntuación x·e es nula y V tiene rango k − (número de dummies de impulso) por construcción: es una propiedad algebraica, no un problema numérico. `fit_ols_hac` lo trata así:
- Comprueba la positividad (`psd_truncate`) solo en el bloque de V de los términos que no son dummies de impulso (constante, ρ, β₁–β₅ y estacionales).
- El truncamiento espectral, y su declaración en el pie y en RF-20, se reserva para ese bloque.
- El rango reducido por las dummies de impulso se anota aparte en el pie como «rango reducido por dummies de impulso (esperado)». No cuenta como truncamiento.
- Las filas de las dummies en la tabla de coeficientes llevan la nota «EE HAC no informativo: dummy de impulso con residuo nulo».

Así lo fija la spec tras el cambio C3 (Definiciones: «Dummy de impulso» y «Matriz HAC no definida positiva»).

### `src/diagnostics.py` (puras)
```python
def breusch_godfrey(fit: Fit, nlags: int = BG_LAGS) -> dict        # acorr_breusch_godfrey(fit.sm_result, nlags); se reporta LM ~ chi2(4)
def breusch_pagan(fit: Fit) -> dict                                # het_breuschpagan(resid, X, robust=True)  (Koenker)
def white(fit: Fit) -> dict
    # propia: auxiliar resid² ~ const + X + cuadrados + productos cruzados de las columnas no constantes;
    # elimina la colinealidad por rango, no por duplicados exactos: QR con pivoteo de columnas sobre Z_aux
    # (scipy.linalg.qr(pivoting=True)), conservando las columnas con |R_jj| > tol·|R_11|. Así caen los cuadrados
    # de las dummies, los productos entre dummies y los productos dummy de impulso × regresor (proporcionales a la dummy);
    # LM = n·R²_aux ~ chi2(rango(Z_aux) − 1)
def jarque_bera_test(fit: Fit) -> dict                             # statsmodels.stats.stattools.jarque_bera
def reset(fit: Fit) -> dict                                        # linear_reset(sm_result, power=3, test_type="fitted", use_f=True, cov_type="nonrobust")
def vif(fit: Fit) -> pd.DataFrame                                  # variance_inflation_factor sobre X con constante; filas: y_lag y los 5 macro
def chow_wald(fit: Fit, break_q: str) -> dict
    # reestima sobre la misma muestra con X + post·[const, y_lag, 5 macro] (post = 1{t >= break}), misma ventana HAC;
    # Wald H0: las 7 interacciones = 0 con el bloque de V tratado como en fit_ols_hac; chi2(7).
    # En 2020T2 quedan ~21 trimestres posteriores útiles para 7 restricciones: la nota advierte que el tamaño
    # real puede apartarse del 5 %.
def cusum(fit: Fit) -> dict
    # Equivalencia exacta: con una dummy de impulso, MCO da los mismos coeficientes y residuos que borrar ese
    # trimestre. Por eso el CUSUM se calcula sobre la regresión reducida: mismo y y X sin las columnas de dummies
    # de impulso, sobre la muestra sin sus trimestres (2020T2–2021T1). Sobre ella se llama a
    # recursive_olsresiduals(OLS reducida, skip=None, alpha=0.95) -> rcusum, rcusumci. Las bandas de
    # Brown-Durbin-Evans salen así con n' − k' = (n − 4) − (k − 4) residuos recursivos.
    # Veredicto "falla" si algún punto sale de las bandas. El pie dice que los trimestres con dummy de impulso
    # no aportan residuo recursivo. Devuelve también las series para la figura.
def diagnostics_table(fit: Fit) -> pd.DataFrame                    # prueba, estadístico, p_valor, veredicto, nota
```
El veredicto se calcula en una sola función: «pasa» si p ≥ 0,05 y «falla» si p < 0,05; para el VIF, «alerta» o «sin alerta». La nota de cada Chow dice que se aplicó «Wald HAC con interacciones de la constante, ρ y β₁–β₅; dummies COVID sin interactuar» (RF-13).

### `src/forecast.py` (puras)
```python
def one_step(params: pd.Series, X_test: pd.DataFrame) -> pd.Series            # X_test usa y_lag observado
def dynamic(params: pd.Series, X_test: pd.DataFrame, y_anchor: float) -> pd.Series
    # y_lag(2022T1) = y_anchor = Y observada en 2021T4 en la forma del modelo (hoy ΔDR(2021T4), no el nivel);
    # después y_lag(t) = ŷ(t−1)
# X_test sale de build_design con VariantSpec("oos_test", start=2022Q1, end=fin, covid_dummies=False),
# así que pasa por el control de NaN de RF-2. Sus columnas se alinean con params del tramo de estimación.
def to_level(pred: pd.Series, form: str, level_obs: pd.Series, anchor: pd.Period, mode: str) -> pd.Series
    # nivel: pred tal cual. Primera diferencia, "one_step": DR_obs(t−1) + ΔŶ(t);
    # "dynamic": DR_obs(anchor) + cumsum(ΔŶ)
def naive(level_obs: pd.Series, test_index: pd.PeriodIndex, anchor: pd.Period, mode: str) -> pd.Series
    # one_step: DR_obs(t−1); dynamic: DR_obs(anchor) constante
def rmse(e) -> float; def mae(e) -> float
def diebold_mariano_hln(e_model: pd.Series, e_naive: pd.Series, h: int = 1) -> dict
    # e = observado − pronóstico (nivel, pp); d = e_model² − e_naive² (DM < 0: el modelo pierde menos);
    # γ̂0 = (1/n)·Σ(d − d̄)² (divisor n); DM = d̄/sqrt(γ̂0/n) (h=1: sin autocovarianzas);
    # HLN: DM* = DM·sqrt((n+1−2h+h(h−1)/n)/n); p bilateral con t(n−1)
def oos_verdicts(ratio_one: float, ratio_dyn: float, dm_p: float) -> dict
```
La distribución t(n−1) de Diebold-Mariano forma parte de la corrección HLN. No contradice la regla de la normal de la spec, que se aplica a coeficientes y efectos.

### `src/model1.py` (pura)
```python
def run_model1(full: pd.DataFrame, stationarity: pd.DataFrame, end: pd.Period) -> Model1Result
def coefficient_table(fit: Fit) -> tuple[pd.DataFrame, dict]       # filas + pie (RF-9)
def effects_table(fit: Fit) -> pd.DataFrame                        # RF-10
def model_stationarity_table(stationarity, decisions) -> pd.DataFrame   # RF-15
def run_variant(full, spec, decisions, end) -> VariantOutcome      # "estimada" | "no estimada" + motivo
def robustness_estimates(main: Fit, outcomes) -> pd.DataFrame      # RF-16
def robustness_summary(main: Fit, outcomes) -> pd.DataFrame        # RF-17, con "k de n"
def is_robust(main_coef: float, coef: float, p: float, alpha=ROBUST_ALPHA) -> bool
def out_of_sample(full, decisions, end) -> OOSResult               # RF-18 (tabla + series para la figura)
def limitations_table(...) -> pd.DataFrame                         # RF-20
def deviations_table(outcomes) -> pd.DataFrame                     # RF-21
def stress_export(fit: Fit) -> dict                                # RF-8
```
`Model1Result` es un `dataclass` congelado. Trae todos los `DataFrame` de salida, el pie de la tabla de coeficientes, las series del CUSUM y del pronóstico, `outcomes`, el diccionario de exportación y `main_fit`.

### Ampliaciones
```python
# src/figures.py
def plot_model1_coefficients(effects: pd.DataFrame) -> Figure      # impacto por 1 DE ± IC 95 %, línea en 0 (RF-11)
def plot_model1_cusum(cusum: dict) -> Figure                       # RF-14
def plot_model1_oos(oos: OOSResult) -> Figure                      # observado, a un paso, dinámico, ingenuo (RF-19)
# src/report_vars.py
def model1_variables(result: Model1Result) -> dict                 # RF-22
```

## 3. Algoritmo (pseudocódigo)

```
pipeline models
  raw, manifest = load_latest_raw(data/raw)                     # congelado, sin red
  panel_result = build_panel(raw)                               # mismo código que la etapa data; usa .full y .end
  stationarity = read_csv(outputs/tables/stationarity.csv)      # si falta: error "ejecuta primero `src.pipeline data`"
  result = run_model1(panel_result.full, stationarity, panel_result.end)
  escribir tablas (.csv + .md), figuras (.png), outputs/models/model1_main.json, clave modelo1: de _variables.yml

run_model1(full, stationarity, end):
  decisions = read_decisions(stationarity)
  check_expected_forms(decisions, EXPECTED_FORMS)               # RF-4, antes de estimar nada
  design = build_design(full, MAIN, decisions["dralacbs"], end) # RF-1..RF-3; 2000T1–2026T2, 106 obs
  si check_dof(design): detener                                 # RF-6 (principal)
  fit = fit_ols_hac(design)                                     # RF-7
  coef_tab, pie = coefficient_table(fit)                        # RF-9
  eff = effects_table(fit)                                      # RF-10: impacto y largo plazo × {1 pp, 1 DE}
  diag = diagnostics_table(fit)                                 # RF-12..RF-14
  stat_tab = model_stationarity_table(stationarity, decisions)  # RF-15
  outcomes = [run_variant(full, v, decisions, end) for v in VARIANTS]
     run_variant:
        d = build_design(full, v, decisions[v.dependent], end)
        si v.id == "R8" y d.start >= MAIN_START: return "no estimada: sin historia anterior a 2000T1"   # RF-5
        motivo = check_dof(d); si motivo: return "no estimada: " + motivo                                # RF-6
        return estimada(fit_ols_hac(d))
  rob_est = robustness_estimates(fit, outcomes)                 # RF-16
  rob_sum = robustness_summary(fit, outcomes)                   # RF-17: celda = sí/no/no estimada; k de n
  oos = out_of_sample(full, decisions, end)                     # RF-18
     d_train = build_design(full, VariantSpec("oos", ..., end=2019Q4, covid_dummies=False), ...)
     fit_tr = fit_ols_hac(d_train)                              # error si check_dof falla (RF-6)
     X_test = mismas columnas en 2022Q1..end (y_lag observado)
     y1 = one_step(fit_tr.params, X_test);  yd = dynamic(fit_tr.params, X_test, Y_obs(2021Q4))
     L1 = to_level(y1, "one_step"); Ld = to_level(yd, "dynamic")
     N1 = naive("one_step"); Nd = naive("dynamic")
     métricas, ratios, DM-HLN(L1−obs, N1−obs), veredictos
  lim = limitations_table(...)   dev = deviations_table(outcomes)   # RF-20, RF-21
  return Model1Result(...)
```

## 4. Salidas exactas

Todas las tablas se escriben en `.csv` (con `float_format=None` y `lineterminator="\n"`) y en `.md` (con `to_markdown` y coma decimal), con columnas en español.

| Archivo | Contenido | RF |
|---|---|---|
| `outputs/tables/model1_coefficients.{csv,md}` | Términos × coef., EE HAC, z, p, IC 95 %, signo esperado y coincidencia. El `.md` cierra con el pie de RF-9 en un párrafo «Nota:». | RF-9 |
| `outputs/tables/model1_effects.{csv,md}` | 5 regresores × {impacto, largo plazo} × {1 pp, 1 DE}: estimación, EE, p, IC 95 % o «no reportado (1 − ρ ≤ 0,05)» / «no definido». | RF-10 |
| `outputs/tables/model1_diagnostics.{csv,md}` | Prueba, estadístico, p-valor, veredicto y nota (VIF con una fila por regresor). | RF-12, RF-13, RF-14 |
| `outputs/tables/model1_stationarity.{csv,md}` | Dependiente y 5 regresores en su forma: ADF/KPSS copiados de la 001, decisión, orden y «no I(0)». | RF-15 |
| `outputs/tables/model1_robustness_estimates.{csv,md}` | Una fila por regresión × regresor macro, o una fila «no estimada» con su motivo. | RF-16 |
| `outputs/tables/model1_robustness_summary.{csv,md}` | 5 regresores × 10 columnas (sí, no o no estimada) + «k de n». | RF-17 |
| `outputs/tables/model1_oos.{csv,md}` | Métricas, cocientes, DM, n y veredictos. | RF-18 |
| `outputs/tables/model1_limitations.{csv,md}` | Limitación y fuente (fija o detectada). | RF-20 |
| `outputs/tables/model1_deviations.{csv,md}` | Decisión, referencia (guía o skill) y motivo. | RF-21 |
| `outputs/figures/model1_coefficients.png` | RF-11. | RF-11 |
| `outputs/figures/model1_cusum.png` | RF-14. | RF-14 |
| `outputs/figures/model1_oos.png` | RF-19. | RF-19 |
| `outputs/models/model1_main.json` | Exportación para la spec 005 (abajo). | RF-8 |
| `report/_variables.yml` | Solo se reescribe la clave `modelo1:`; las demás se conservan. | RF-22 |

Formato de las figuras: 8×4,5 pulgadas, 200 dpi, sin título. Cada una lleva abajo el pie «Fuente: FRED; elaboración propia» con `fig.text`. Se guardan con `metadata={"Software": None}` para que los bytes sean deterministas (RNF-5).

**Exportación para la spec 005 (`outputs/models/model1_main.json`).** Se escribe con `json.dumps(..., indent=2, ensure_ascii=False)`, con las claves en el orden fijado aquí y los floats en `repr`, a precisión completa:
```json
{"spec": "003-modelo-i", "dependent": "dralacbs", "form": "primera diferencia",
 "terms": ["const", "y_lag", "gdp_growth", "d_unemp", "inflation", "d_ffr", "credit_growth", "covid_2020q2", "..."],
 "columns": {"gdp_growth": "gdpc1_yoy", "d_unemp": "unrate_d", "inflation": "cpiaucsl_yoy", "d_ffr": "fedfunds_d", "credit_growth": "loans_yoy"},
 "credit_lag": 4, "params": [...], "cov_hac": [[...], ...], "psd_adjusted": false,
 "sample_start": "2000T1", "sample_end": "2026T2", "nobs": 106, "hac_lags": 4,
 "covid_quarters": ["2020T2", "2020T3", "2020T4", "2021T1"]}
```
Los valores de este bloque son ilustrativos; todos los calcula el código.

**Claves de `report/_variables.yml` (RF-22).** Todas son textos ya formateados:
- **Coeficientes, efectos y estadísticos:** 3 decimales.
- **p-valores:** 3 decimales, o «< 0,001».
- **Métricas fuera de muestra:** 3 decimales (enmienda de D12 del 5-oct-2026, tras `review-audit.md` punto 5).
- **Trimestres:** en formato `AAAAT#`.

En el informe se citan anidadas, por ejemplo `{{< var modelo1.efectos.d_unemp.impacto_pp >}}`.
```yaml
modelo1:
  estimador: "MCO con errores Newey-West (HAC, kernel de Bartlett)"
  forma_y: "primera diferencia"
  muestra_inicio: "2000T1"   muestra_fin: "2026T2"   n_obs: "106"   n_parametros: "11"   rezagos_hac: "4"
  dummies_covid: "2020T2, 2020T3, 2020T4 y 2021T1"
  truncamiento_espectral: "no"
  r2: "…"   r2_ajustado: "…"   ee_regresion: "…"
  variantes: {R1: "Sin 2020–2021", R2: "...", ..., R8: "..."}
  coef: {<termino>: {coef, ee, p, ic_inf, ic_sup}}            # const, y_lag, 5 macro, 4 dummies
  efectos: {<macro>: {impacto_pp, impacto_pp_ee, impacto_pp_p, impacto_pp_ic_inf, impacto_pp_ic_sup,
                      impacto_de, ..._ic_sup, largo_pp, ..., largo_de, ...}}   # "no reportado (1 − ρ ≤ 0,05)" si aplica
  signo: {<macro>: "sí" | "no" | "sin contraste"}
  diag: {bg: {estadistico, p, veredicto}, bp: {...}, white: {...}, jb: {...}, reset: {...},
         chow_2008t3: {...}, chow_2020t2: {...}, cusum: {veredicto}, vif: {<termino>: {valor, veredicto}}}
  robustez: {<macro>: "k de n"}
  variantes_muestra: {<id>: {estado, inicio, fin, n_obs}}     # id = R1, R2, R3_drclacbs, ..., R8
  oos: {n_trimestres, rmse_modelo_un_paso, rmse_ingenuo_un_paso, mae_..., cociente_un_paso,
        rmse_modelo_dinamico, ..., cociente_dinamico, dm_estadistico, dm_p,
        veredicto_un_paso, veredicto_dinamico, significancia_un_paso}
  no_i0: "π (inflación interanual) y CRED(t−4) (crédito interanual rezagado)"   # generado, no fijo
  limitaciones: ["...", ...]
  desviaciones: ["...", ...]
```

## 5. Integración en `uv run python -m src.pipeline <etapa>`
```
uv run python -m src.pipeline models     # Modelo I desde data/raw congelado + outputs/tables/stationarity.csv
uv run python -m src.pipeline all        # data → models → stress (pendiente) → report (pendiente)
```
- `stage_models()` sustituye al marcador de posición de `models`. `all` llama a `stage_data(download=False)` y después a `stage_models()`.
- La spec 004 añadirá su modelo dentro de la misma etapa, con una llamada a `run_model2`, sin tocar `run_model1`.
- `stage_models` solo lee, llama a funciones puras y escribe. No contiene cálculo.

## 6. Decisiones técnicas (con su alternativa descartada)

| # | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|
| D1 | La etapa `models` reconstruye en memoria `PanelResult.full` con `build_panel(load_latest_raw(...))`; no se guarda ningún panel largo. | RF-1 necesita la historia desde 1998 (la nota 11 del plan 001 lo anticipaba). Reconstruir desde `data/raw/` congelado es determinista y no exige tocar la spec 001. | Escribir `data/processed/panel_full.csv` en la etapa `data`: cambia las salidas de una spec cerrada y crea un archivo que puede desincronizarse. |
| D2 | La decisión de cada forma se lee de `outputs/tables/stationarity.csv`, como pide la spec, y se compara con `EXPECTED_FORMS` (RF-4). | La spec manda leer la tabla. Recalcular ADF/KPSS dentro de `models` duplicaría lógica y podría divergir. | Llamar a `stationarity_table` dentro de `models`. |
| D3 | La inferencia que se reporta se calcula siempre desde (b, V_HAC truncada) con funciones propias (`inference`, `wald`, `long_run`). | Un solo camino para z, p e IC garantiza que el truncamiento espectral, el método delta y Chow usen la misma V y la distribución normal. | Usar `result.pvalues` y `result.wald_test`: no ven la V truncada. |
| D4 | Newey-West puro: `use_correction=False` (el valor por defecto de statsmodels 0.15, `linear_model.py:2884`) y `use_t=False`. Queda fijado antes de estimar. | La spec define Newey-West con Bartlett y floor(4·(T/100)^(2/9)), sin factor n/(n−k). Un test compara la V de `fit_ols_hac` con una Newey-West calculada a mano. | `use_correction=True`: sube los EE un 5,6 % con n = 106 y k = 11, y la spec no lo pide. Decidirlo después de ver p-valores sería buscar significancia. |
| D5 | El test de White se implementa a mano y elimina la colinealidad por rango, con QR con pivoteo; los grados de libertad son rango(Z_aux) − 1. | Con dummies de impulso, el producto dummy × regresor es proporcional a la dummy (24 columnas colineales en la principal), y además están los cuadrados de las dummies. Si se quitaran solo los duplicados exactos, los grados de libertad se inflarían y White «pasaría» sin motivo. | `het_white` de statsmodels, o eliminar solo duplicados exactos. |
| D6 | Chow se calcula como Wald HAC sobre una regresión ampliada con interacciones, usando la misma ventana HAC que la principal. | Es lo que fija RF-13. Usar la misma ventana evita que el resultado dependa de una T distinta. | El F clásico de Chow por submuestras: queda singular con las dummies COVID. |
| D7 | CUSUM de residuos recursivos (Brown, Durbin y Evans) con `recursive_olsresiduals`, aplicado a la regresión reducida: sin las columnas de dummies de impulso y sin sus trimestres. | Con las dummies dentro, `x[:skip]` es singular (las COVID valen 0 en 2000–2002) y la función lanza `ValueError` (`diagnostic.py:1988-1993`). La regresión reducida es una equivalencia exacta (FWL): da los mismos coeficientes y residuos, y las bandas salen con n' − k'. | Llamarla sobre la principal (falla); quitar las dummies (cambia la especificación); el CUSUM de residuos MCO (Ploberger-Krämer), que no es el que pide la spec. |
| D8 | El pronóstico dinámico encadena ŷ en `y_lag` desde el ancla 2021T4 y reconstruye el nivel con una suma acumulada. | Es la definición de la spec y la misma mecánica que usará la 005. | Pronóstico dinámico con `statsmodels` (`predict(dynamic=True)`): exige otro tipo de modelo (ARIMAX). |
| D9 | Diebold-Mariano con h = 1, γ̂0 con divisor n, e = observado − pronóstico, d = e_modelo² − e_ingenuo², corrección HLN y t(n−1). | Para h = 1 la serie de diferencias de pérdida no tiene autocorrelación teórica. El divisor n es el de Diebold y Mariano (1995). HLN es la corrección pre-registrada. Fijar la convención evita que la fije por accidente el test hecho a mano. | Varianza HAC de d_t (con n ≈ 18 es inestable); divisor n − 1. |
| D10 | El inicio truncado de R6–R8 se calcula como el primer trimestre en que todos los términos existen en la historia transformada. Con los datos congelados: R6 2001T1, R7 2002T1 y R8 «no estimada». | RF-5. Se deriva de los datos y no se fija a mano, igual que D14 de la 001. | Fijar los trimestres de inicio en la configuración. |
| D11 | Las dummies sin variación se omiten y se anotan en `Design.dropped` solo en R1 y en el tramo de estimación fuera de muestra; en cualquier otra regresión, es un error. | La spec dice que en R1 (y fuera de muestra) las dummies desaparecen; en el resto, perder una dummy en silencio cambiaría la especificación. | Omitirlas en cualquier variante; o mantenerlas y que RF-6 marque R1 «no estimada». |
| D15 | Con dummies de impulso, la positividad se comprueba solo en el bloque de V sin esas dummies. Su rango reducido se reporta como «esperado» y no como truncamiento, y sus EE llevan la nota «no informativo». | El residuo de un trimestre con dummy de impulso es 0, así que V tiene rango k − 4 por construcción. Si se comprobara la V completa, el truncamiento se activaría siempre y RF-20 listaría como fallo numérico una propiedad algebraica. Lo fija la spec (C3). | Truncar la V completa y declararlo siempre como limitación. |
| D16 | La DE de RF-10 usa `ddof=1` sobre la muestra efectiva de la principal, excluyendo 2020T2–2021T1 (C1); el pie lo dice. | Es la convención de pandas, declarada antes de estimar. | `ddof=0`. |
| D12 | Formato: 3 decimales en coeficientes, efectos y métricas fuera de muestra, y «< 0,001» para p-valores pequeños. **Enmienda (5-oct-2026, `review-audit.md` punto 5, aprobada por el autor):** las métricas fuera de muestra pasan de 2 a 3 decimales. | Con efectos de centésimas de pp, 2 decimales mostrarían «0,00». Con RMSE de centésimas, el del modelo y el del ingenuo se redondean al mismo valor a 2 decimales y el veredicto «supera al ingenuo» no se entiende; además la tabla y las variables del informe deben mostrar las mismas cifras. | 2 decimales en las métricas, como en la 001. |
| D13 | Las limitaciones y desviaciones fijas viven como textos en `model1_config.py`, y las condicionales (diagnósticos fallidos, no I(0), posible I(2), R8 no estimada, truncamiento) se añaden por código. | RF-20 y RF-21: las cifras y los estados salen del código, nunca a mano. | Escribirlas en el informe: viola el principio 5. |
| D14 | La exportación para la 005 se hace en JSON con nombres de términos y columnas. | Es legible por máquina y por humanos, se puede comparar con git y no añade dependencias. La 005 reconstruye X con las mismas columnas. | `pickle` del resultado de statsmodels: opaco y frágil entre versiones. |

## 7. Estrategia de tests (pytest, sin red, semillas fijas)

Semilla única: `SEED = 20261005`, con `np.random.default_rng(SEED)`. Los tolerancias se declaran en cada test. No se prueban las funciones de statsmodels, solo nuestro uso de ellas.

| Archivo | Qué prueba | RF / RNF |
|---|---|---|
| `tests/test_design.py` | `read_decisions` y `check_expected_forms`: si la tabla cambia una forma, salta `ModelDataError` con la serie y las dos formas (RF-4). `dependent_series`: con «ambigua» da la diferencia y con «niveles» el nivel; el logit también se diferencia. `build_design`: `y_lag` es t−1 y `credit_growth` es t−4 aunque falte una fila; las dummies COVID valen 1 solo en sus trimestres; las estacionales tienen base T1. Un NaN interior lanza error con variable, trimestre y regresión (RF-2). La ventana truncada en un panel sintético desde 1998 da R6 = 2001T1, R7 = 2002T1 y R8 = 2000T1. R1 omite las dummies COVID y lo anota. `diff_regressor_stationary` aplica la regla a la fila «primera diferencia». | RF-1 a RF-5, RF-15 |
| `tests/test_estimation.py` | DGP y_t = 0,5 + 0,6·y_{t−1} + 1,0·x1 − 0,5·x2 + e (n = 2000): recupera los coeficientes con un error absoluto ≤ 0,05 (RNF-2). DGP estático con x AR(1) 0,8 y e AR(1) 0,7 (n = 500): EE HAC de x > EE clásico (RNF-2). `hac_lags(106) == 4` y `hac_lags(1) >= 1`. `psd_truncate`: una matriz definida positiva queda igual; una con un valor propio −1e-3 sale con todos sus valores propios ≥ piso y `ajustada=True`. `inference` reproduce p e IC normales de valores conocidos. `wald` coincide con t² para una restricción. `long_run`: con b = 0,2, ρ = 0,5 y V diagonal conocida, la estimación vale 0,4 y el EE es el de la fórmula cerrada; con ρ = 0,96 da «no reportado». `scale_effect` con factor 0 da «no definido». `check_dof` marca menos de 30 grados de libertad y el rango incompleto. | RF-6, RF-7, RF-10, RNF-2, RNF-3 |
| `tests/test_diagnostics.py` | BG rechaza (p < 0,05) con e AR(1) 0,7 y no rechaza con e iid (n = 200, semilla fija). Chow Wald rechaza con un quiebre simulado en la pendiente y no rechaza sin quiebre. White sobre un X con dummies no tiene columnas duplicadas y sus grados de libertad son los esperados. El VIF de dos regresores casi colineales da «alerta». CUSUM: con un quiebre fuerte da «falla» y con un proceso estable da «pasa». `diagnostics_table` trae todas las pruebas de RF-12. | RF-12 a RF-14, RNF-4 |
| `tests/test_impulse_dummies.py` | Con un DGP con 4 dummies de impulso (n = 106, semilla fija):<br>• Los coeficientes no dummy de la principal coinciden (tolerancia 1e-10) con los de la regresión reducida, con esos trimestres borrados.<br>• `cusum` corre sin error y su `rcusum` coincide con el de la regresión reducida.<br>• El bloque no dummy de V es definido positivo y no se marca truncamiento; el rango reducido se reporta como «esperado».<br>• White tiene grados de libertad = rango(Z_aux) − 1 (no cuenta los 24 productos dummy × regresor).<br>• En un caso pequeño (n = 12, 2 regresores, L = 2), la V de `fit_ols_hac` coincide con una Newey-West sin corrección calculada a mano (D4).<br>• `diff_form_stationary` juzga ΔDRALACBS con su fila «primera diferencia».<br>• `y_anchor` del pronóstico dinámico es ΔDR(2021T4) y no el nivel.<br>• Una dummy sin variación fuera de R1 y del tramo fuera de muestra lanza `ModelDataError`.<br>• Un faltante terminal en DRALACBS lanza error en la principal. | RF-1, RF-7, RF-12, RF-14, RF-15, RF-18, RNF-2, RNF-4 |
| `tests/test_forecast.py` | `to_level` en la forma a un paso: DR(t−1) observado + ΔŶ. En la dinámica: ancla + suma acumulada, comprobado a mano con 3 trimestres. `dynamic` encadena ŷ en `y_lag`. `naive` en sus dos modos. `rmse` y `mae` de vectores conocidos. `diebold_mariano_hln` con un ejemplo de n = 5 calculado a mano: estadístico y p con t(4). `oos_verdicts` en los cuatro casos. | RF-18, RNF-3 |
| `tests/test_model1.py` | Con un panel sintético de parámetros conocidos (forma de la 001, desde 1998):<br>• `run_model1` produce todas las tablas.<br>• `is_robust` en la tabla de verdad (signo × p a ambos lados de 0,10).<br>• El recuento «k de n» excluye las «no estimada».<br>• Una variante con menos de 30 grados de libertad sale como «no estimada».<br>• R8 sin historia anterior a 2000 sale como «no estimada».<br>• Las limitaciones incluyen las fijas más las detectadas.<br>• Las desviaciones incluyen el estado de R8.<br>• El JSON de exportación trae `params` y `cov_hac` coherentes con `terms`. | RF-5, RF-6, RF-8, RF-9, RF-10, RF-16, RF-17, RF-20, RF-21, RNF-3 |
| `tests/test_language.py` | Las tablas `.md` de `model1_*` y los textos de `modelo1:` generados sobre el panel sintético no contienen «causa», «causal», «provoca» ni «debido a» (sin distinguir mayúsculas). Una cadena de prueba con «provoca» sí se detecta. | RNF-7 |
| `tests/test_outputs_model1.py` | Las figuras tienen la etiqueta del eje con la unidad, la línea en cero (coeficientes), las bandas (CUSUM), 4 series (fuera de muestra) y el pie con la fuente. `model1_variables` trae todas las claves de la sección 4 y los efectos no reportados son texto. | RF-11, RF-14, RF-19, RF-22 |
| `tests/test_frozen_model1.py` | Sobre `data/raw/` real:<br>• `check_expected_forms` pasa.<br>• La principal tiene 2000T1–fin y 106 observaciones.<br>• R6 empieza en 2001T1 y R7 en 2002T1.<br>• R8 sale como «no estimada».<br>• `hac_lags == 4` y `n_parametros == 11` en la principal.<br>• Ejecutar `models` dos veces en dos `tmp_path` (`PIPELINE_ROOT`) deja bytes idénticos en todas las tablas, figuras, JSON y `_variables.yml` (RNF-5).<br>• Las claves de `_variables.yml` que no son `modelo1` quedan byte a byte iguales a las de antes de la corrida.<br>Este test **no** compara coeficientes con ningún valor esperado. | RF-1, RF-4, RF-5, RF-23, RNF-5 |
| `tests/test_pipeline.py` (tests de pureza ampliados) | Los cinco módulos nuevos no importan red, disco ni gráficos, y no usan relleno de faltantes. | RNF-6, RF-2 |

## 8. Cobertura de RF

| RF / RNF | Parte del plan |
|---|---|
| RF-1, RF-2 | `design.build_design` y `effective_window` · D1 · `test_design` |
| RF-3, RF-4 | `design.read_decisions` y `check_expected_forms` · D2 |
| RF-5 | `design.effective_window` y `model1.run_variant` · D10 |
| RF-6 | `estimation.check_dof` y `model1.run_variant` · D11 |
| RF-7 | `estimation.fit_ols_hac` y `psd_truncate` · D3, D4 |
| RF-8 | `model1.stress_export` → `outputs/models/model1_main.json` · D14 |
| RF-9 | `model1.coefficient_table` → `model1_coefficients.*` |
| RF-10 | `estimation.long_run` y `scale_effect`, y `model1.effects_table` → `model1_effects.*` |
| RF-11 | `figures.plot_model1_coefficients` |
| RF-12 a RF-14 | `diagnostics` → `model1_diagnostics.*` y `model1_cusum.png` · D5, D6, D7 |
| RF-15 | `model1.model_stationarity_table` y `design.diff_regressor_stationary` |
| RF-16, RF-17 | `model1.robustness_estimates` y `robustness_summary` |
| RF-18, RF-19 | `forecast` y `model1.out_of_sample` · `figures.plot_model1_oos` · D8, D9 |
| RF-20, RF-21 | `model1.limitations_table` y `deviations_table` · D13 |
| RF-22 | `report_vars.model1_variables` · D12 |
| RF-23 | `pipeline.stage_models` · sección 5 |
| RNF-1 | Commit `667b313` (solo `specs/003-modelo-i/`), anterior a cualquier estimación |
| RNF-2, RNF-3, RNF-4 | `test_estimation`, `test_forecast`, `test_model1` y `test_diagnostics` |
| RNF-5 | `test_frozen_model1` · formato de CSV, JSON y PNG de la sección 4 |
| RNF-6 | Separación de módulos · tests de pureza de `test_pipeline.py` |
| RNF-7 | `test_language` |
| RNF-8 | `TERM_LABELS` y columnas en español |

## 9. Orden sugerido para las tareas (lo detalla `/sdd-tasks`)
1. `model1_config` y `design`, con `test_design` (sin estimar).
2. `estimation`, con `test_estimation`.
3. `diagnostics`, con `test_diagnostics`.
4. `forecast`, con `test_forecast`.
5. `model1`: principal, efectos y estacionariedad del modelo.
6. `model1`: robusteces, limitaciones, desviaciones y exportación.
7. `model1.out_of_sample`.
8. Figuras y `model1_variables`, con `test_outputs_model1` y `test_language`.
9. `pipeline.stage_models` y `test_frozen_model1`. **Esta es la primera tarea que estima con datos reales.**
10. Auditoría (`agente: claude`, `/sdd-audit`).

## 10. Notas para specs posteriores (no se implementan aquí)
- La spec 005 carga `outputs/models/model1_main.json`, reconstruye X con `columns` y `credit_lag`, fija las dummies COVID en 0 en el horizonte de estrés y reconstruye el nivel desde ΔY.
- La spec 004 reutiliza `estimation`, `diagnostics` y `design.ModelDataError`.

## 11. Cambios a la spec (aplicados con `/sdd-change` el 5-oct-2026, antes de estimar)
El revisor encontró tres puntos que no se podían resolver en el plan sin reinterpretar la spec. Se aceptaron los tres tal como se proponen aquí, quedaron registrados en «Desviaciones del pre-registro» de la spec y ya están reflejados en este plan:
- C1 en D16 y en `effects_table`.
- C2 como limitación fija en los textos de `model1_config` (D13).
- C3 en D15 y en `fit_ols_hac`.
- **C1. DE de RF-10 y RF-11.** Hoy la DE incluye los trimestres COVID: la de ΔU vale 1,05 pp con ellos y 0,31 pp sin ellos. Propuesta: calcular la DE sobre la muestra efectiva de la principal, sin los trimestres con dummy de impulso (2020T2–2021T1), que el modelo ya neutraliza.
- **C2. Efectos base fuera de la ventana COVID.** `gdpc1_yoy` de 2021T2 vale +11,8 % y no tiene dummy, y el crédito del PPP entra en CRED(t−4) entre 2021T2 y 2022T1. Propuesta mínima: declararlo como limitación fija en RF-20 y apoyarse en R1 (sin 2020–2021) como contraste. La alternativa (ampliar las dummies a 2021T2–2022T1) cambia la especificación principal, y se descarta.
- **C3. Dummies de impulso y matriz HAC.** Hoy la Definición de la spec dice «si algún valor propio ≤ 0, truncamiento y declaración». Propuesta: precisar que la comprobación se hace en el bloque de V sin dummies de impulso, y que el rango reducido por esas dummies se reporta como esperado y no como truncamiento (D15).

## 12. Respuesta a `review-plan.md`
| # | Observación | Respuesta |
|---|---|---|
| 1 | CUSUM singular con dummies | Incorporada: regresión reducida (FWL), D7 y test en `test_impulse_dummies`. |
| 2 | V singular por dummies de impulso | Incorporada: D15, nota en las filas de las dummies y test; la lectura de la spec, a C3. |
| 3 | Colinealidad en White | Incorporada: QR con pivoteo, grados de libertad = rango − 1, D5 y test. |
| 4 | `use_correction` | Incorporada: el revisor tiene razón (por defecto es `False`). Queda fijado `False`, con test contra una NW hecha a mano (D4). |
| 5 | Fila de la dependiente en RF-15 | Incorporada: `diff_form_stationary` para ΔDR y su rezago; nota sobre CRED(t−4). |
| 6 | BG: LM o F | Incorporada: LM ~ χ²(4). |
| 7 | Convención de DM | Incorporada: divisor n, e = observado − pronóstico (D9). |
| 8 | Recorte terminal en la principal | Incorporada: solo para dependientes alternativas; en la principal es un error. |
| 9 | DE: ddof y muestra | Incorporada: `ddof=1` (D16); la muestra, a C1. |
| 10 | `X_test` | Incorporada: `build_design` con `VariantSpec("oos_test")`; test de `y_anchor`. |
| Opc. | R1 contiguo, D11 restringido, `hac_lags`/`n_parametros`, otras claves de `_variables.yml`, tamaño del Chow 2020T2 | Incorporadas las cinco. |
| Spec | DE inflada y efectos base | Aplicadas como C1 y C2 (`/sdd-change` del 5-oct-2026). |
