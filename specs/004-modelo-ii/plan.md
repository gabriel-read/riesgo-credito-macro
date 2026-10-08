# Plan 004 — Modelo II: política monetaria y deterioro posterior de la cartera
Estado: aprobada · Spec: `specs/004-modelo-ii/spec.md` (aprobada, Crítica: sí, commit `ec983d0`) · Depende de: specs y planes 001 y 003 (implementados)

Este plan fija el CÓMO de la spec 004 y no cambia ningún requisito, salvo una precisión que la auditoría del plan obligó a registrar en la spec con un `/sdd-change` (C1: regla «no calculable» de White, ya aprobada y registrada en «Desviaciones del pre-registro» de la spec; el plan la recoge en D14). Reutiliza el código de la 003 (`design`, `estimation`, `diagnostics`) y no añade dependencias: statsmodels, pandas, numpy, scipy y matplotlib ya están. Los cambios al código de la 003 son solo dos, retrocompatibles y con test (D1, D2): las salidas del Modelo I tienen que seguir idénticas byte a byte.

## 1. Módulos de `src/` y responsabilidad

| Módulo | Responsabilidad | ¿Red/disco/gráficos? | RF |
|---|---|---|---|
| `src/model2_config.py` (nuevo) | Constantes del pre-registro: rango de K, horizontes, umbral de tasa cero, z del 90 %, umbrales de avisos, `Spec2` de la principal y de R1–R3, nombres y etiquetas de los términos, textos fijos de limitaciones y desviaciones. | No | RF-6, RF-20, RF-22, RF-25, RF-26 |
| `src/design2.py` (nuevo) | Funciones puras: columnas con rezagos, muestra común M, trimestres de tasa cero, diseño del modelo de rezagos distribuidos, diseño de las proyecciones locales, rezagos que salen de trimestres excluidos. | No | RF-1 a RF-5, RF-16, RF-22 a RF-24 |
| `src/dynamics.py` (nuevo) | Funciones puras: S y S_rez con su Wald, multiplicadores ψ_h y R(h), h\*, Granger, H1 y H2, regla de lectura, selección de K por AIC y BIC. | No | RF-6, RF-7, RF-10 a RF-13 |
| `src/localproj.py` (nuevo) | Funciones puras: una proyección local por horizonte (morosidad y tasa), horizonte de detección y comparación descriptiva con R(h). | No | RF-14 a RF-17 |
| `src/diagnostics.py` (ampliado) | `vif` admite una lista de términos; `chow_wald` devuelve también los trimestres útiles anteriores y la comprobación de rango (hecha antes de estimar); `white` no se cae cuando la auxiliar tiene más columnas que observaciones y devuelve «no calculable» con motivo. No cambia lo que ya devuelve para el Modelo I. | No | RF-19, RF-20 |
| `src/estimation.py` (ampliado) | `fit_ols_hac` admite `maxlags` opcional (ventana HAC propia) y `_impulse_dummy_cols` exige además valores en {0, 1}. | No | RF-14, RF-15 |
| `src/model2.py` (nuevo) | Orquestación pura del Modelo II: selección, principal, tablas, robusteces R1–R3, limitaciones, desviaciones, insumos de la 6.3, exportación y salida en Markdown y CSV como texto. Devuelve un `Model2Result`. | No | RF-3 a RF-30 |
| `src/figures.py` (ampliado) | `plot_model2_profile`, `plot_model2_response` (dos paneles). El CUSUM reutiliza `plot_model1_cusum`. | Gráficos (sin disco) | RF-9, RF-18, RF-19 |
| `src/report_vars.py` (ampliado) | `model2_variables(result) -> dict`, el bloque `modelo2:`; funciones auxiliares con el prefijo `_m2_`. | No | RF-28 |
| `src/pipeline.py` (ampliado) | `stage_models` corre además el Modelo II, escribe sus salidas y la clave `modelo2:`. | Sí | RF-30, RNF-8 |

Los módulos nuevos no importan `requests`, `pandas_datareader`, `matplotlib`, `pathlib` ni `os`, no usan `open(` y no usan `fillna`, `ffill`, `bfill`, `interpolate` ni `dropna`. Se añaden a los tests de pureza de `tests/test_pipeline.py` (los mismos que ya cubren los de la 003).

## 2. Funciones y firmas

Convenciones heredadas: `pd.PeriodIndex` trimestral `Q-DEC`; errores de datos con `ModelDataError`; `Design` de `src/design.py`; `Fit` de `src/estimation.py`; textos con `fmt_es`, `fmt_p` y `quarter_label`.

### `src/model2_config.py`
```python
K_MAX = 8; K_RANGE = tuple(range(1, K_MAX + 1)); H_MAX = 12
ZERO_RATE_MAX = 0.25                 # tasa trimestral ≤ 0,25 % ⇒ tramo de tasa cero
LP_BAND_Z = float(norm.ppf(0.95))    # 1,6449: banda del 90 %
RHO_WARN = 0.95
CHOW_POST_MIN = 30                   # nota de tamaño del Chow si los posteriores útiles son menos
EXCLUDE_COVID = ("2020Q1", "2021Q4") # R2: rango inclusivo
EXPECTED_FORM = "ambigua (primera diferencia)"   # DRALACBS, RF-2
DFFR_COLS = lambda K: [f"d_ffr_l{j}" for j in range(K + 1)]   # d_ffr_l0 … d_ffr_lK
CONTROLS = {"gdp_l1": ("gdpc1_yoy", 1), "d_unemp_l1": ("unrate_d", 1),
            "inflation_l1": ("cpiaucsl_yoy", 1), "credit_l4": ("loans_yoy", 4)}   # término → (columna, rezago)
EVIDENCE = ("evidencia fuerte", "evidencia parcial", "sin evidencia")

@dataclass(frozen=True)
class Spec2:
    id: str; label: str
    k_source: str = "bic"            # "bic" | "aic"
    exclude_range: tuple[str, str] | None = None
    exclude_zero_rate: bool = False
    covid_dummies: bool = True

MAIN2 = Spec2("main", "Especificación principal")
ROBUST2 = [Spec2("R1", "K elegido por AIC", k_source="aic"),
           Spec2("R2", "Sin 2020–2021", exclude_range=EXCLUDE_COVID, covid_dummies=False),
           Spec2("R3", "Sin tramos de tasa cero", exclude_zero_rate=True, covid_dummies=False)]
TERM_LABELS2: dict[str, str]         # "d_ffr_l0" → «ΔFFR(t)», «d_ffr_l3» → «ΔFFR(t−3)», …
FIXED_LIMITATIONS2: list[tuple[str, str]]; FIXED_DEVIATIONS2: list[tuple[str, str, str]]
```

### `src/design2.py` (puras)
```python
def build_columns(full, decision) -> pd.DataFrame
    # y = ΔDR (dependent_series de src.design), y_lag, d_ffr_l0..d_ffr_l8 (fedfunds_d.shift(j)),
    # gdp_l1, d_unemp_l1, inflation_l1, credit_l4. Todo sobre `full` reindexado, sin dropna.
def common_window(cols: pd.DataFrame, end: pd.Period) -> tuple[pd.Period, pd.Period]
    # primer trimestre con TODAS las columnas (K = 8) presentes → `end`; usa notna().all(axis=1)
def zero_rate_quarters(full, start, end) -> list[pd.Period]      # promedio trimestral de `fedfunds` ≤ ZERO_RATE_MAX
def build_design2(full, spec: Spec2, K: int, decision, window, end) -> Design
    # y, const, y_lag, d_ffr_l0..d_ffr_lK, controles, dummies COVID; recorta a `window`, quita las exclusiones
    # de `spec`, NaN ⇒ ModelDataError(variable, trimestre, spec.id); dummies sin variación: solo se omiten si
    # spec.id es R2 o R3 (se anotan en Design.dropped), si no ⇒ ModelDataError
def lagged_from_excluded(design: Design, K: int, excluded: set[pd.Period], terms: tuple[str, ...] | None = None) -> list[pd.Period]
    # trimestres t de la muestra con algún regresor rezagado (y_lag, ΔFFR(t−1..t−K), controles) que sale de un
    # trimestre excluido; los rezagos contemporáneos no cuentan (t pertenece a la muestra)
def covid_lag_leaks(design: Design, K: int) -> list[pd.Period]
    # solo y_lag y d_ffr_l1..d_ffr_lK con excluded = 2020T2–2021T1 (RF-25). Los controles NO cuentan: sus efectos
    # base ya son limitaciones fijas y se contarían dos veces
def build_lp_design(full, h: int, K: int, decision, window, end, target: str) -> Design
    # target "morosidad": y = DR(t+h) − DR(t−1); target "tasa": y = FFR(t+h) − FFR(t−1) (pp, nivel `fedfunds`);
    # X = const, d_ffr_l0, y_lag, controles, d_ffr_l1..d_ffr_lK, dummies COVID fechadas en t;
    # muestra: de window[0] a end − h (nunca usa datos posteriores a `end`)
```

### `src/dynamics.py` (puras)
```python
def cumulative_effects(fit: Fit, K: int) -> dict
    # S (θ0+…+θK) y S_rez (θ1+…+θK): estimación, EE HAC, χ²(1) por src.estimation.wald, p, IC 95 % normal
def multipliers(params: pd.Series, K: int, hmax: int = H_MAX) -> pd.DataFrame
    # h, psi, R. ψ0 = θ0; ψh = θh·1{h ≤ K} + ρ·ψ(h−1); R(h) = Σ ψ
def peak_horizon(psi: pd.Series) -> dict
    # h_star = el menor h con |ψh| ≥ max|ψ| − 1e-12 (empate ⇒ menor h), signo = signo de ψ(h_star)
def granger_lags(fit: Fit, K: int) -> dict       # Wald HAC χ²(K) sobre d_ffr_l1..d_ffr_lK (sin d_ffr_l0): stat, df, p, veredicto
def hypotheses(effects: dict, peak: dict) -> dict
    # h1_signo = S > 0 («sí»/«no»); h1_respaldada = p_S < 0,05 y S > 0; h2 = h_star ≥ 1
def evidence_reading(granger: dict, effects: dict) -> dict
    # C1 = Granger rechaza al 5 %; C2 = S_rez > 0 y p < 0,05; etiqueta ∈ EVIDENCE; signo_contrario = S_rez < 0 y p < 0,05
def select_k(fits: dict[int, Fit]) -> dict
    # AIC y BIC de statsmodels (lnL gaussiana) de cada Fit.sm_result; k_aic, k_bic (empate ⇒ menor K); tabla
```

### `src/localproj.py` (puras)
```python
def local_projection(full, K, h, decision, window, end, target) -> LPOutcome
    # check_dof ⇒ «no estimada» con motivo; si no, fit_ols_hac(design, maxlags=max(hac_lags(T), h + 1));
    # devuelve el coeficiente de d_ffr_l0 con su EE HAC y la banda del 90 %
def run_local_projections(full, K, decision, window, end) -> pd.DataFrame
    # una fila por h = 0..12 con beta, ee, banda del 90 %, n_obs, rezagos_hac, estado, phi, phi_ee, banda de phi.
    # h = 0 de la tasa es una identidad (FFR(t) − FFR(t−1) = ΔFFR(t)): no se estima; phi_0 = 1 exacto, EE y banda «—»
    # y la nota «por construcción (identidad)» (D15)
def detection_horizon(lp: pd.DataFrame) -> str       # primer h cuya banda del 90 % de β_h excluye el cero; «ninguno»
def compare_with_trajectory(trajectory: pd.DataFrame, lp: pd.DataFrame) -> tuple[pd.DataFrame, dict]
    # por h: R(h), beta, phi, mismo_signo, banda_excluye_cero; recuento «k de n» solo con h = 1..12 estimados
```

### Cambios retrocompatibles
- `src/estimation.fit_ols_hac(design, maxlags: int | None = None)`: con `None` usa `hac_lags(nobs)` como hoy (D1).
- `src/estimation._impulse_dummy_cols`: además de suma = 1, exige que los valores estén en {0, 1} (D2), porque un rezago de ΔFFR con suma exactamente 1 no debe tomarse por dummy.
- `src/diagnostics.vif(fit, terms=None)`: sin `terms` usa los del Modelo I; con `terms` calcula el VIF de esos.
- `src/diagnostics.chow_wald`: añade a su resultado `n_pre`, `n_pre_util` y `calculable`. El rango de la matriz aumentada se comprueba **antes** de `fit_ols_hac` y de `wald`, con `np.linalg.matrix_rank` por defecto (D17); si es incompleto devuelve `calculable = False` con su motivo y no estima. No cambia las claves que ya devolvía.
- `src/diagnostics._white_aux_matrix` y `white`: la QR pasa a modo completo para no caerse cuando hay más columnas que observaciones, y `white` devuelve `calculable = False` con motivo y sin veredicto si n − rango(Z_aux) < `MIN_DOF` (30). Con n = 105 eso ocurre desde K = 4. No cambia lo que devuelve cuando es calculable (D14).

### `src/model2.py` (pura)
```python
def run_model2(full, stationarity, end, result1) -> Model2Result
def diagnostics_table2(fit, K) -> pd.DataFrame     # misma batería que la 003, VIF de los términos del modelo, Chow con la nota de RF-20
def stationarity_table2(stationarity) -> pd.DataFrame
    # filas de la 001: ΔDR (dralacbs), ΔFFR (fedfunds) y ΔU (unrate) de «primera diferencia» (decisión con diff_form_stationary);
    # PIB (gdpc1_yoy), π (cpiaucsl_yoy) y CRED (loans_yoy) de «tal cual». El pie dice que los términos rezagados usan
    # el ADF/KPSS de la serie sin rezagar. KPSS «> 0,10» / «< 0,01» (D9)
def robustness_table2(main, outcomes) / robustness_summary2(main, outcomes) / robustness_note2(outcomes, ...)
def limitations_table2(...) / deviations_table2(...) / comparison_inputs(result, coef1, footer1)
def export2(result) -> dict;  def export2_json(d) -> str
def render_model2_tables(result) -> dict[str, dict[str, str]]
```
`Model2Result` es un `dataclass` congelado con los `DataFrame` de salida, `fits` (por K), `main_fit`, `K`, `window`, `trajectory`, `effects`, `granger`, `reading`, `lp`, `comparison`, `variants`, `export` y las notas.

## 3. Algoritmo (pseudocódigo)

```
stage_models (ya existente: Modelo I) → después:
  result2 = run_model2(panel.full, stationarity, panel.end, result1)

run_model2(full, stationarity, end, result1):
  decisions = read_decisions(stationarity); si decisions["dralacbs"] != EXPECTED_FORM: ModelDataError   # RF-2
  cols = build_columns(full, decision); window = common_window(cols, end)                              # RF-3
  fits = {}
  para K en 1..8:                                                                                      # RF-5
      d = build_design2(full, MAIN2, K, decision, window, end)
      si check_dof(d): ModelDataError(f"K = {K}: ...")
      fits[K] = fit_ols_hac(d)
  sel = select_k(fits); K = sel.k_bic; main = fits[K]                                                  # RF-6, RF-7
  effects = cumulative_effects(main, K); traj = multipliers(main.params, K); peak = peak_horizon(traj.psi)
  gr = granger_lags(main, K); hyp = hypotheses(effects, peak); reading = evidence_reading(gr, effects)  # RF-10 a RF-13
  lp = run_local_projections(full, K, decision, window, end)                                           # RF-14 a RF-16
  comparison, counts = compare_with_trajectory(traj, lp)                                               # RF-17
  diag = diagnostics_table2(main, K); stat = stationarity_table2(stationarity)                        # RF-19 a RF-21
  variantes = [run_variant2(spec) para spec en ROBUST2]                                                # RF-22, RF-23
        R1: si sel.k_aic == K → «no aplica»; si no, fit con k_aic sobre `window`
        R2/R3: K del principal; ventana = window menos la exclusión; dummies COVID omitidas; check_dof → «no estimada»
  limitaciones, desviaciones, insumos de la 6.3, exportación, variables                                 # RF-25 a RF-29
```

## 4. Salidas exactas

Tablas en `outputs/tables/` como `.csv` (precisión completa, `\n`) y `.md` (coma decimal, «< 0,001»; las de los pies con «Nota:»). Figuras en `outputs/figures/` (8×4,5 pulgadas, 200 dpi, sin título, pie de fuente, bytes deterministas). JSON en `outputs/models/`.

| Archivo | Contenido | RF |
|---|---|---|
| `model2_selection` | K = 1..8: parámetros, observaciones, AIC, BIC y marcas; pie con la muestra M. | RF-3, RF-7 |
| `model2_coefficients` | Coeficientes con EE HAC, z, p, IC 95 % y la nota de las dummies; pie del RF-8. | RF-8 |
| `model2_effects` | S y S_rez (EE, χ²(1), p, IC 95 %) y H1. | RF-10 |
| `model2_trajectory` | ψ_h y R(h), h\*, H2; pie con las advertencias de ρ. | RF-11 |
| `model2_reading` | Granger (χ²(K), p, veredicto) y la lectura (C1, C2, etiqueta, marca de signo contrario). | RF-12, RF-13 |
| `model2_lp` | β_h, φ_h, bandas del 90 %, observaciones, rezagos HAC y estado. | RF-14, RF-15, RF-16 |
| `model2_comparison` | R(h), β_h, φ_h, mismo signo, banda; recuento «k de n» y horizonte de detección; pie. | RF-17 |
| `model2_diagnostics` | Batería con estadístico, p y veredicto; notas del Chow. | RF-19, RF-20 |
| `model2_stationarity` | ADF/KPSS de ΔDR, ΔFFR y los controles copiados de la 001, con «< 0,001» y «> 0,10». | RF-21 |
| `model2_robustness_estimates` | R1–R3: K, muestra, observaciones, S, S_rez, p, h\*, H1. | RF-22 |
| `model2_robustness_summary` | S_rez por variante («sí/no/no estimada/no aplica»), p de la principal y pie. | RF-24 |
| `model2_limitations`, `model2_deviations` | Limitaciones y desviaciones. | RF-25, RF-26 |
| `model2_inputs63` | θ₀ y el coeficiente de ΔFFR(t) de la 003, con EE, p, muestra y forma de los controles. | RF-27 |
| `model2_profile.png`, `model2_response.png`, `model2_cusum.png` | Perfil de θ_j; respuesta acumulada y de la tasa (dos paneles); CUSUM. | RF-9, RF-18, RF-19 |
| `outputs/models/model2_main.json` | Exportación para la spec 005 (abajo). | RF-29 |
| `report/_variables.yml` | Solo se reescribe la clave `modelo2:` (la `modelo1:` y la `datos:` no se tocan). | RF-28 |

**Exportación para la spec 005 (`model2_main.json`).** Claves en este orden: `spec`, `dependent`, `form`, `k`, `k_criterion`, `terms`, `columns` (término → columna del panel y rezago), `params`, `cov_hac` (matriz completa tras el tratamiento de la 003), `psd_adjusted`, `hac_lags`, `sample_start`, `sample_end`, `nobs`, `covid_quarters`, `psi`, `response` (R(h)), `h_star`, `reading` (etiqueta, C1, C2). Floats con precisión completa, sin NaN.

**Claves de `report/_variables.yml` (RF-28).** Todo texto ya formateado: 3 decimales en coeficientes, efectos, trayectoria y proyecciones; p-valores con 3 decimales o «< 0,001»; trimestres en `AAAAT#`. Se citan anidadas, por ejemplo `{{< var modelo2.efectos.s_rez.est >}}`.
```yaml
modelo2:
  estimador: "MCO con errores Newey-West (HAC, kernel de Bartlett)"
  forma_y: "primera diferencia"
  k_elegido: "…"   criterio: "BIC"   k_bic: "…"   k_aic: "…"
  muestra_inicio: "2000T2"   muestra_fin: "2026T2"   n_obs: "105"   n_parametros: "…"   rezagos_hac: "…"
  dummies_covid: "2020T2, 2020T3, 2020T4 y 2021T1"
  truncamiento_espectral: "no"
  r2: "…"   r2_ajustado: "…"   ee_regresion: "…"
  seleccion: {k1: {n_parametros, aic, bic}, …, k8: {…}}
  coef: {<termino>: {coef, ee, p, ic_inf, ic_sup}}
  efectos: {s: {est, ee, chi2, p, ic_inf, ic_sup}, s_rez: {…},
            h1: {signo: "sí"|"no", respaldada: "sí"|"no"}}
  trayectoria: {psi: {h0: "…", …, h12: "…"}, r: {h0: "…", …, h12: "…"},
                h_estrella: {h: "…", signo: "+"|"−"}, h2: "sí"|"no", aviso_rho: "…"|""}
  granger: {chi2, gl, p, veredicto: "rechaza"|"no rechaza"}
  lectura: {etiqueta, c1: "sí"|"no", c2: "sí"|"no", signo_contrario: "sí"|"no"}
  lp: {h0: {beta, ee, ic90_inf, ic90_sup, n_obs, rezagos_hac, estado, phi, phi_ee, phi_ic90_inf, phi_ic90_sup}, …}
  lp_resumen: {k_de_n: "k de n", horizonte_deteccion: "h…"|"ninguno"}
  diag: {bg, bp, white, jb, reset, chow_2008t3, chow_2020t2, cusum: {veredicto}, vif: {<termino>: {valor, veredicto}}}
  robustez: {r1: {estado, k, muestra_inicio, muestra_fin, n_obs, s, s_rez, p_s_rez, h_estrella, h1},
             r2: {…}, r3: {…}}
  robustez_resumen: {r1: "sí"|"no"|"no estimada"|"no aplica", r2: "…", r3: "…", p_principal: "…"}
  no_i0: "π y CRED(t−4)"                       # generado; «ninguno» si todos son I(0)
  limitaciones: ["…", …]
  desviaciones: ["…", …]
```
Los valores son ilustrativos; todos los calcula el código.

## 5. Integración en `uv run python -m src.pipeline <etapa>`
`stage_models` ya construye el panel y el Modelo I (spec 003). Se le añade, tras escribir las salidas del Modelo I, `run_model2(panel.full, stationarity, panel.end, result1)`, la escritura de las 14 tablas, las 3 figuras, el JSON y la clave `modelo2:` de `_variables.yml` (mismo método que `modelo1:`: se carga, se añade la clave y se vuelve a volcar con `sort_keys=False` y `newline="\n"`). `all` no cambia. La etapa solo lee y escribe; el cálculo está en las funciones puras.

## 6. Decisiones técnicas (con su alternativa descartada)

| # | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|
| D1 | `fit_ols_hac(design, maxlags=None)`. | Las proyecciones locales necesitan max(fórmula, h + 1) rezagos. Con `None` no cambia nada para el Modelo I. | Reimplementar Newey-West en `localproj`: duplica la covarianza, el tratamiento de las dummies de impulso y los tests. |
| D2 | `_impulse_dummy_cols` exige valores en {0, 1}. | Con hasta 9 columnas de ΔFFR, una columna continua con suma 1 no debe tratarse como dummy. | Dejar la regla de la 003: correcta para sus columnas, frágil aquí. |
| D3 | Una muestra común M para elegir K y para el modelo principal (K = 8 fija el inicio). | Es el criterio de la skill y de la spec; AIC y BIC son comparables solo con las mismas observaciones. | Una muestra propia por K: no comparable. |
| D4 | AIC y BIC de `statsmodels` (lnL gaussiana de MCO). | Con la misma T, ordenan igual que T·ln(RSS/T) + penalización. | Fórmulas propias: mismo orden y más código. |
| D5 | Granger como Wald HAC χ²(K) sobre ΔFFR(t−1..t−K), con `wald`. | Una sola matriz HAC para toda la inferencia; coherente con la 003. | `grangercausalitytests` de statsmodels: usa covarianza clásica y no excluye las dummies de impulso. |
| D6 | R(h) y ψ_h por recursión explícita, comprobada con una forma cerrada. | Es la definición de la spec; el test fija el resultado para ρ y θ conocidos. | Respuesta al impulso simulada: añade aleatoriedad sin ganar nada. |
| D7 | La proyección local usa `fit_ols_hac` (mismo tratamiento de dummies de impulso y de la matriz HAC) y la banda del 90 % sale de la normal. | Una sola maquinaria de estimación. | `statsmodels.OLS.fit(cov_type="HAC")` directo: perdería el tratamiento de C3. |
| D8 | `chow_wald` devuelve `n_pre`, `n_pre_util` y `calculable`; la nota del Chow se arma en `diagnostics_table2` (RF-20). | La spec 003 fijaba la nota solo para 2020T2; la 004 la basa en una regla de datos (menos de 30 posteriores útiles). | Reutilizar `CHOW_SIZE_CAUTION_BREAKS`: es una lista de fechas, no una regla. |
| D9 | El KPSS de `model2_stationarity.md` se escribe «> 0,10» / «< 0,01» con una función propia, no con `fmt_kpss_p` (que escribe «≥ 0,10»). | Lo fija RF-21; unificar la 003 queda fuera de alcance. | Cambiar `fmt_kpss_p`: cambiaría las salidas del Modelo I. |
| D10 | R3 identifica los tramos de tasa cero con el promedio trimestral de `fedfunds` (columna de la 001) ≤ 0,25. | Es la regla de la spec; no depende de fechas escritas a mano. | Una lista de trimestres: se desactualiza y es un número a mano. |
| D11 | Los insumos de la 6.3 salen de `result1` en memoria (misma corrida), no de un archivo. | Son las mismas cifras que el CSV del Modelo I y la función sigue siendo pura. | Leer `model1_coefficients.csv` dentro de `model2`: disco en un módulo puro. |
| D12 | Reutilizo `_format_for_markdown`, `fmt_p`, `fmt_es` y `quarter_label` de la 003. | Mismo formato de salida en los dos modelos. | Copiarlos: dos formatos que divergen. |
| D13 | Un solo `Model2Result` y una sola función `render_model2_tables`. | Mismo patrón que la 003 y menos superficie de error. | Una función por tabla en el pipeline: lógica de presentación fuera de `src/`. |
| D14 | White: `_white_aux_matrix` no se cae con más columnas que observaciones y `white` devuelve «no calculable» (con motivo y sin veredicto) si n − rango(Z_aux) < 30; entra en las limitaciones detectadas. **Registrada en la spec como C1 (RF-19).** | Con n = 105 y K ≥ 4 la auxiliar completa tiene más columnas que observaciones y hoy lanza `IndexError`; con K = 3 corre con rango 59 (poca potencia) y una auxiliar saturada daría un «pasa» espurio. La regla se fija ahora, sin conocer K. | Decidir cómo calcular White después de ver K; cambiar el método a White sin productos cruzados o al caso especial en ŷ y ŷ² (alternativas que el `/sdd-change` deja a elección del autor). |
| D15 | φ₀ = 1 por construcción: en h = 0 no se estima la proyección de la tasa; se reporta 1 con EE y banda «—» y la nota «por construcción (identidad)». Es una precisión de implementación: la spec ya dice que h = 0 coincide por construcción (RF-17) y la auditoría pidió declararlo en el plan. | FFR(t) − FFR(t−1) es el regresor ΔFFR(t): ajuste perfecto, EE ≈ 0 y z ≈ 1e16; mostrarlo como estimación engaña y puede disparar un truncamiento espectral sobre ruido numérico. | Estimarlo y mostrar «1,000 (0,000)». |
| D16 | `diagnostics_table2` arma sus propias notas del Chow (K + 7 interacciones; trimestres útiles anteriores y posteriores, siempre; aviso de tamaño si los posteriores son menos de 30) y no usa la clave `nota` de `chow_wald`, que es la del Modelo I. | Esa nota nombra «constante, ρ y β₁–β₅». | Parametrizar la nota de `chow_wald`: cambia el código de la 003. |
| D17 | La comprobación de rango del Chow se hace antes de `fit_ols_hac` y de `wald`, con la tolerancia por defecto de `np.linalg.matrix_rank`. | Con rango incompleto `solve` puede lanzar `LinAlgError` o dar números sin sentido. | Capturar la excepción: el resultado dependería del error numérico. |
| D18 | `PEAK_TIE_TOL = 1e-12` es una constante de `model2_config`. | Es una regla de la spec (empate ⇒ menor h) y no debe estar dentro de la función. | Literal en `peak_horizon`. |

## 7. Estrategia de tests (pytest, sin red, semillas fijas)

Semillas: `SEED = 20261008`; la X y el ruido de y salen de semillas distintas (RNF-7). Datos sintéticos de `tests/synthetic_model2.py`: historia 1998T1–2026T2 con ΔDR generado por un modelo de rezagos distribuidos de θ, ρ y controles conocidos, `fedfunds` en nivel (con un tramo de tasa cero para R3) y las columnas que usa el Modelo II. Fixture de sesión `model2_result` en `conftest.py`.

### 7.1 Procesos simulados y tolerancias (declarados antes de implementar)
Semillas: `SEED2 = 20261008` para X y `SEED2 + 1` para el ruido. Si un test no cumple su tolerancia, **no se relaja**: se revisa el código o se sube n y se anota en este plan. Con ΔDR(t−1) en la ecuación, MCO tiene sesgo de muestra finita en ρ (Hurwicz); con n ≥ 2 000 es menor que las tolerancias.

| Proceso | Qué prueba | Parámetros | Tolerancia |
|---|---|---|---|
| A | Recuperación punta a punta (`build_design2` + `fit_ols_hac`), S y S_rez | n = 4 000; ΔFFR i.i.d. N(0; 0,5²); controles i.i.d. N(0, 1); σ_ε = 0,3; K verdadero 3; θ = (0,30; 0,25; 0,20; 0,15); ρ = 0,5; γ(gdp_l1, d_unemp_l1, inflation_l1, credit_l4) = (−0,05; 0,20; 0,03; 0,02); constante 0,02; sin efecto de las dummies COVID | \|estimación − verdadero\| ≤ 0,05 en cada θ_j (j = 0..3), en ρ y en cada γ; \|S − 0,90\| ≤ 0,10 y \|S_rez − 0,60\| ≤ 0,10 |
| B | `select_k` por BIC | n = 2 000; proceso A (K verdadero 3, θ₃ = 0,15) | BIC elige K = 3; el empate de AIC o BIC se prueba con ajustes construidos a mano |
| C | Proyecciones locales | proceso A con n = 4 000 y ΔFFR ruido blanco | \|β_h − R(h)\| ≤ 0,12 para h = 0..12; \|φ_h − 1\| ≤ 0,20 para h = 1..12; φ₀ = 1 exacto |
| D | HAC > clásico | n = 500; ΔFFR AR(1) 0,8; errores AR(1) 0,7; modelo estático con ΔFFR(t) | el EE HAC de ΔFFR supera al clásico |
| E | Granger | n = 500; θ = (0,30; 0,25; 0,20; 0,15) rechaza al 5 %; θ = (0,30; 0; 0; 0) no rechaza con la semilla declarada | p < 0,05 y p ≥ 0,05 respectivamente |
| F | Diagnósticos | BG con errores AR(1) 0,7, n = 200, rechaza; con errores independientes no. Chow con quiebre simulado en la pendiente de ΔFFR(t) a mitad de muestra, n = 300, rechaza; sin quiebre no. **Dimensión del Modelo II:** n = 105; White con K = 8 da «no calculable» y con K = 1 un resultado válido; Chow con K = 8 (K + 7 = 15 interacciones) y CUSUM sobre la regresión sin las 4 dummies de impulso | p < 0,05 y p ≥ 0,05 según el caso; «no calculable» con su motivo |

### 7.2 Tests por archivo

| Archivo | Qué prueba | RF / RNF |
|---|---|---|
| `tests/test_design2.py` | `common_window` da 2000T2 con historia desde 1998 y no usa `dropna`; `build_design2` construye los rezagos t−j reales (aunque falte una fila), el orden de columnas, las dummies COVID solo en sus trimestres y el error de NaN con variable, trimestre y regresión; R2 y R3 omiten las dummies y las anotan, y en cualquier otro caso es un error; `zero_rate_quarters` aplica la regla; `lagged_from_excluded` y `covid_lag_leaks` dan los trimestres esperados en casos hechos a mano; `build_lp_design` calcula DR(t+h) − DR(t−1) y FFR(t+h) − FFR(t−1), termina en `end − h` y nunca usa datos posteriores a `end`. | RF-1 a RF-4, RF-16, RF-22 a RF-24 |
| `tests/test_dynamics.py` | Con θ y ρ conocidos: S, S_rez, ψ_h y R(h) coinciden con una forma cerrada; `peak_horizon` (incluido el empate); `granger_lags` rechaza con θ_j ≠ 0 y no con θ_j = 0; `hypotheses` y `evidence_reading` en sus tres resultados y la marca de signo contrario; `select_k` recupera el K verdadero con n ≥ 1 000 y resuelve el empate al menor K. | RF-6, RF-10 a RF-13, RNF-2, RNF-3 |
| `tests/test_localproj.py` | Con ΔFFR simulado como ruido blanco y controles independientes, β_h recupera R(h) y φ_h la respuesta de la tasa dentro de una tolerancia declarada; la ventana HAC es max(fórmula, h + 1); un horizonte sin grados de libertad sale «no estimada» sin afectar a los demás; `detection_horizon` y el recuento «k de n» (sin h = 0). | RF-14 a RF-17, RNF-4 |
| `tests/test_estimation.py` (ampliado) | `fit_ols_hac(maxlags=...)` usa esa ventana y con `None` da lo mismo que antes; `_impulse_dummy_cols` ignora una columna continua de suma 1; el error HAC supera al clásico con ΔFFR AR(1) 0,8 y errores AR(1) 0,7. | RNF-2 |
| `tests/test_diagnostics.py` (ampliado) | `vif(terms=…)`; `chow_wald` devuelve los trimestres útiles anteriores y posteriores y marca el rango incompleto; Breusch-Godfrey rechaza con errores AR(1) 0,7 y no con independientes; Chow rechaza con un quiebre simulado y no sin él. | RF-19, RF-20, RNF-6 |
| `tests/test_model2.py` | `run_model2` con la forma esperada y sin ella (se detiene antes de estimar); la selección sobre la muestra común y la parada si algún K no tiene grados de libertad; R1 «no aplica» si AIC y BIC coinciden; R2 y R3 con K fijo y sus muestras; el resumen de robustez (criterio sobre S_rez, estados fuera del denominador); las notas de pie de cada tabla (texto y cifras desde el código); la nota del Chow (menos de 30 posteriores, y «no calculable»); limitaciones fijas y detectadas; desviaciones; insumos de la 6.3; exportación JSON (claves, orden, ida y vuelta exacta). | RF-3 a RF-27, RNF-5 |
| `tests/test_outputs_model2.py` | Figuras (tamaño, sin título, pie, series dibujadas); `model2_variables` con todas las claves del §4, solo texto, sin cifras escritas a mano (escaneo con `ast`), con los mismos dígitos que las tablas. | RF-9, RF-18, RF-28 |
| `tests/test_language.py` (ampliado) | Tablas, variables y figuras del Modelo II sin «causa», «causal», «provoca» ni «debido a». | RNF-10 |
| `tests/test_pipeline.py` (ampliado) | Pureza de los módulos nuevos y ausencia de `fillna` y `dropna`. | RNF-9 |
| `tests/test_frozen_model2.py` | Sobre `data/raw/` real, en directorios temporales: existen las 14 tablas (`.md` y `.csv`), las 3 figuras, el JSON y `modelo2:`; `modelo1:` y `datos:` quedan idénticos; M = 2000T2–2026T2 con 105 observaciones; 36 trimestres de tasa cero; dos corridas dejan bytes idénticos. **No compara coeficientes con valores esperados.** Además, las salidas del Modelo I siguen idénticas a las comiteadas. | RF-3, RF-30, RNF-8 |

### 7.3 Tests añadidos tras la revisión del plan (`review-plan.md`)

| Test | Qué comprueba | Punto |
|---|---|---|
| `test_white_not_calculable_at_model2_dimension` y `test_white_valid_with_k1` | White con K = 8 y n = 105 da «no calculable» con motivo y sin `IndexError`; con K = 1 da un resultado válido; la regla es n − rango < 30 | 1 |
| `test_recovers_known_parameters_end_to_end` | Proceso A: θ_j, ρ y γ dentro de 0,05, y S y S_rez dentro de 0,10 | 2, 3 |
| `test_select_k_recovers_true_k_with_bic` | Proceso B | 2 |
| `test_chow_k_plus_7_interactions`, `test_cusum_without_impulse_quarters`, `test_white_rank_elimination_at_k8_design` | Los tres tests de RNF-6 con un diseño de K = 8 | 4 |
| `test_phi0_is_one_by_construction` | φ₀ = 1, EE y banda «—», sin `inf` ni `NaN` en el CSV y el JSON, cifra estable entre corridas | 5 |
| `test_covid_lag_leaks_only_counts_y_lag_and_dffr` | No cuenta los controles; da los trimestres esperados en un caso hecho a mano | 6 |
| `test_chow_note_names_k_plus_7_terms_and_both_counts` | La nota del Modelo II no menciona «β₁–β₅», dice K + 7 y siempre trae los trimestres útiles anteriores y posteriores | 7 |
| `test_chow_rank_check_runs_before_estimating` | Con rango incompleto no se llama a `fit_ols_hac` ni a `wald` y la fila es «no calculable» | 8 |
| `test_stationarity_rows_come_from_the_right_001_rows` y `test_stationarity_footer_says_lagged_terms_use_unlagged_series` | ΔDR, ΔFFR y ΔU de «primera diferencia»; PIB, π y CRED de «tal cual»; el pie lo dice | 9 |
| `test_lp_beta0_equals_theta0_with_same_se` | β₀ de la proyección es θ₀ de la principal, con el mismo EE | opcional |
| `test_frozen_model2_hac_lags_and_parameter_count` | `hac_lags == 4` en la principal y número de parámetros = K + 11 | opcional |

## 8. Cobertura de RF

| RF / RNF | Parte del plan |
|---|---|
| RF-1 a RF-4 | `design2.build_columns`, `common_window`, `build_design2` · D3 |
| RF-5 a RF-9 | `dynamics.select_k`, `model2.run_model2`, `figures.plot_model2_profile` · D3, D4 |
| RF-10 a RF-13 | `dynamics` (efectos, trayectoria, Granger, lectura) · D5, D6 |
| RF-14 a RF-18 | `localproj`, `figures.plot_model2_response` · D1, D7 |
| RF-19 a RF-21 | `model2.diagnostics_table2`, `stationarity_table2`, `diagnostics.chow_wald` · D8, D9 |
| RF-22 a RF-24 | `model2.run_variant2`, `robustness_*` · D10 |
| RF-25 a RF-27 | `model2.limitations_table2`, `deviations_table2`, `comparison_inputs` · D11 |
| RF-28 a RF-30 | `report_vars.model2_variables`, `model2.export2`, `render_model2_tables`, `pipeline.stage_models` · D12, D13 |
| RNF-1 | Commit `ec983d0` (solo `specs/004-modelo-ii/`), anterior a cualquier estimación |
| RNF-2 a RNF-7 | Sección 7 |
| RNF-8 | `test_frozen_model2` |
| RNF-9 | Separación de módulos · tests de pureza |
| RNF-10, RNF-11 | `test_language` · etiquetas en español |

## 9. Orden sugerido para las tareas (lo detalla `/sdd-tasks`)
1. `model2_config`, `design2` y los dos cambios retrocompatibles (D1, D2), con `test_design2` y `test_estimation`. Comprobar que las salidas del Modelo I no cambian.
2. `dynamics`, con `test_dynamics`.
3. `localproj`, con `test_localproj`.
4. Ampliación de `diagnostics` (VIF con términos, Chow con trimestres útiles y rango), con `test_diagnostics`.
5. `model2`: selección, principal, efectos, trayectoria, lectura y tablas.
6. `model2`: robusteces, limitaciones, desviaciones, insumos de la 6.3, exportación y salida en texto.
7. Figuras y `model2_variables`, con `test_outputs_model2`, `test_language` y `test_pipeline`.
8. `pipeline.stage_models` y `test_frozen_model2`. **Primera tarea que estima con datos reales.**
9. Validación y auditoría (`agente: claude`).

Antes de la tarea 8 se commitea el plan aprobado con `review-plan.md`, para que conste que las reglas de White (D14) y de φ₀ (D15) se fijaron sin conocer K.

## 10. Notas de seguimiento (no se implementan aquí)
- La spec 005 lee `model2_main.json` y aplica la regla heredada de la spec 004: sin «evidencia fuerte», el efecto de la tasa va a cero en todos los modelos del estrés y se reporta aparte la sensibilidad con el coeficiente puntual.
- La spec 006 lee los insumos de `model2_inputs63` para la comparación de la sección 6.3.
- Lección de la 003 aplicada: cada nota de pie que promete este plan tiene su test (RNF-5), y al cerrar cada enmienda se comprueba con `grep` que el código la implementa.

## 11. Respuesta a `review-plan.md`
| # | Observación | Respuesta |
|---|---|---|
| 1 | White se cae con K ≥ 4 y no hay regla | Reproducido (K = 4 y K = 8 dan `IndexError` con n = 105). Regla «no calculable» (n − rango < 30), registrada en la spec como C1 y recogida en D14, con QR en modo completo y tests en §7.3. |
| 2 | Faltan tolerancias declaradas | §7.1: procesos A a F con n, parámetros, semillas y tolerancias, fijados antes de implementar. |
| 3 | Nadie prueba la recuperación punta a punta | `test_recovers_known_parameters_end_to_end` (proceso A), §7.3. |
| 4 | Tests de diagnósticos en la dimensión del Modelo II | Chow con K + 7, CUSUM sin las dummies y White con eliminación por rango, con K = 8 (proceso F), §7.3. |
| 5 | φ₀ es una identidad | D15: φ₀ = 1 por construcción, EE y banda «—»; `test_phi0_is_one_by_construction`. |
| 6 | `covid_lag_leaks` cuenta los controles | Restringida a y_lag y ΔFFR(t−1..t−K) (parámetro `terms`); test en §7.3. |
| 7 | La nota de `chow_wald` es la del Modelo I | D16: `diagnostics_table2` arma sus propias notas; test de que no dice «β₁–β₅». |
| 8 | Rango del Chow antes de estimar | D17: se comprueba antes de `fit_ols_hac` y de `wald`; test. |
| 9 | Filas de la tabla de estacionariedad | Declaradas en la firma de `stationarity_table2`; tests en §7.3. |
| Opc. | β₀ = θ₀ con el mismo EE; `n_pre_util` siempre en la nota; `hac_lags == 4` y K + 11 parámetros en el test congelado; `PEAK_TIE_TOL` como constante; commitear el plan antes de la tarea 8 | Incorporadas las cinco (§7.3, D16, D18 y §9). |

