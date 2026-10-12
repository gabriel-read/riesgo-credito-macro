# Plan 005 — Estrés
Estado: borrador v6 (Claude Code, 11-oct-2026) · **No es aprobable hasta que la spec 005 esté aprobada.** Incorpora las decisiones del autor del 11-oct, las rondas 1 a 3 de `review-plan*.md` y los documentos técnicos de Codex (`compatibilidad-tecnica-005`, `fuentes-y-adaptadores-005`, `congelacion-fed-005`). Pendiente de comprobación final acotada.

## 1. Módulos y responsabilidades
| Módulo | Responsabilidad | E/S |
|---|---|---|
| `src/scenarios.py` (nuevo) | Parser puro de los CSV de la Fed (texto → DataFrame), identidades de transformación, adaptación del calendario, enlace con el observado, escenario D, calendario original | pura |
| `src/stress.py` (nuevo) | Adaptador a `forecast.dynamic`/`to_level`, proyección por modelo y escenario, bloque de covarianza, réplicas, resúmenes, sensibilidades | pura |
| `src/stress_tables.py`, `src/stress_figures.py` (nuevos) | Tablas MD/CSV y figuras | pura salvo escritura en el pipeline |
| `src/pipeline.py` (etapa `stress`, hoy provisional) | Única E/S: lee `data/scenarios/`, `data/raw/` (solo lectura), los JSON y el panel; verifica sha256; escribe `outputs/` y `report/_variables.yml` (clave `estres:`) | E/S |
| `src/forecast.py`, `src/panel.py`, `src/model1.py` (spec 003/001) | Se **reutilizan sin cambios**: `forecast.dynamic`, `forecast.to_level`, `panel.parse_raw`, `panel.quarterly_from_quarterly`, `panel.quarterly_from_monthly`, `panel.yoy`; para el test de RF-5, `model1.out_of_sample(...).train_fit` (internamente `build_design` de `src/design.py` y `fit_ols_hac` de `src/estimation.py`) y, para RF-5b, `design2.build_design2` (Modelo II) | — |
Se añaden `src/scenarios.py` y `src/stress.py` a las listas de módulos puros de `tests/test_pipeline.py`.

## 2. Procedencia de los insumos (resuelve los faltantes)
| Insumo | Procedencia reproducible | Cambia contratos aprobados |
|---|---|---|
| Niveles de GDPC1 y del promedio trimestral de CPIAUCSL | La capa de E/S de `stress` usa `fred_io.load_latest_raw(Path('data/raw'))` (sin descargas; si falta un archivo, se detiene sin seguir la sugerencia de descarga de su mensaje de error), **fija el vintage FRED**: los archivos `GDPC1_2026-10-02.csv` y `CPIAUCSL_2026-10-02.csv` (y `LOANS_2026-10-02.csv` para el crédito) de la descarga del 2026-10-02 listada en `data/raw/manifest.csv` (GDPC1: 114 filas hasta 2026-04-01; CPIAUCSL: 344 filas hasta 2026-08-01; LOANS: 344 filas hasta 2026-08-01); verifica nombre, fecha, número de filas y último dato contra el manifiesto y el sha256 del contenido con finales de línea normalizados a LF (valores en el apartado «Vintage FRED»); si el manifiesto señala otra fecha o algo difiere, se detiene; no actualiza FRED ni usa un glob arbitrario; registra nombres y huellas en la evidencia, recorta los observados a `sample_end`, valida trimestres completos y positivos, no ejecuta `stage_data` (escribe salidas) y aplica `parse_raw`, `quarterly_from_quarterly` y `quarterly_from_monthly` de `src/panel.py`, que ya tratan el hueco de octubre de 2025 (spec 001). `panel.csv` no se modifica. | No |
| Variaciones interanuales de lo proyectado | `panel.yoy` sobre la serie de niveles observados + proyectados, para que sea la misma función de la spec 001 (en logaritmos) | No |
| Ajuste de entrenamiento 2000T1–2019T4 (RF-5) | El test llama en memoria a `model1.out_of_sample(full, decisions, end=2026Q2)` (con `decisions` de `read_decisions` + `check_expected_forms`; `OOS_TRAIN`, evaluación desde 2022Q1 y ancla 2021Q4 son las constantes de la 003), pasa `result.train_fit.params` al adaptador dinámico, construye X como `out_of_sample` (MAIN sin dummies COVID, ancla ΔDR(2021Q4) y DR(2021Q4)) y compara con la columna `dinamico` de `result.series`, **sin** la regla de la tasa en cero. Reproduce el ajuste aprobado; no selecciona nada nuevo. No se exporta ni se toca `model1_main.json` | No |
| Archivos de la Fed | `data/scenarios/fed/2026-final/<fecha-descarga>/` (nuevo, versionado en git): tres CSV *Final* con sus bytes originales y `manifest.csv` en el mismo directorio, escrito sin red a partir de la descarga que hace una sola herramienta. Nombres, versión y sha256 en el manifiesto; no se sobrescribe una congelación existente | No: `data/raw/` y la spec 001 no se tocan (su D1 sigue vigente) |
| Origen, DR y ΔDR anclas | `sample_end` de los JSON (2026T2) y el panel; no la fila parcial 2026T3 de `PanelResult.full` | No |
**Archivos de la Fed (commit previo al pre-registro):**
- Ruta única: `data/scenarios/fed/2026-final/<fecha-descarga>/` (la fecha del directorio es la fecha local de la descarga, America/Santo_Domingo; la hora UTC consta en el manifiesto) con `manifest.csv` (URL exacta, escenario, versión final, fecha y hora UTC, SHA-256, tamaño, cobertura y unidades verificadas; con BOM, se lee con `utf-8-sig`).
- Preservación de bytes: `.gitattributes` con las **tres reglas de ruta exacta `-text`** que implementó Codex, solo para los tres CSV (`data/scenarios/fed/2026-final/2026-10-11/2026_Final_Historic_Domestic.csv`, `…/2026_Final_Supervisory_Baseline_Domestic.csv` y `…/2026_Final_Supervisory_Severely_Adverse_Domestic.csv`). No se amplía a `data/scenarios/**`, ni alcanza el manifiesto ni `data/raw/`. Los CSV traen CRLF y el repositorio tiene `core.autocrlf=true`; sin esas reglas la huella cambiaría en un clon limpio. Un test lee los bytes versionados y compara el sha256. El procesamiento derivado va aparte.
- Commit previo al pre-registro, con exactamente estos cinco archivos: `.gitattributes`, los tres CSV y `manifest.csv` del directorio `2026-10-11`.
- Nombres y URL (Codex las identificó en la página oficial DFAST 2026 el 11-oct-2026): `https://www.federalreserve.gov/supervisionreg/files/2026_Final_Historic_Domestic.csv`, `…/2026_Final_Supervisory_Baseline_Domestic.csv`, `…/2026_Final_Supervisory_Severely_Adverse_Domestic.csv`. No se mezclan versiones Proposed y Final ni se usan solo dos CSV sin el histórico.
- Nombres de escenario validados por RF-2: «Supervisory Baseline», «Supervisory Severely Adverse» y «Actual» (histórico, fila «2025 Q4»); 13 trimestres «2026 Q1»–«2029 Q1» por escenario; las cuatro variables con las cabeceras exactas registradas en el manifiesto.
- Huellas SHA-256 de los bytes congelados (verificadas el 11-oct-2026 contra los archivos en `data/scenarios/fed/2026-final/2026-10-11/`):
  - `2026_Final_Historic_Domestic.csv` (16 936 B): `6d08aadcf82d65dcf36b856792040b82ceceef79a46ff0239afd41e0c4e7f653`
  - `2026_Final_Supervisory_Baseline_Domestic.csv` (1 692 B): `76e236695be2c8372890078acf8c01273ba5198a19afb5037045a963737c1bcc`
  - `2026_Final_Supervisory_Severely_Adverse_Domestic.csv` (1 824 B): `45c2859ae7246c071b69df8623854751f0629b04393957e14fe28bc33c04ebbb`
- **Vintage FRED** (sha256 del contenido con CRLF normalizado a LF, porque `core.autocrlf` cambia los bytes del árbol de trabajo; calculados el 11-oct-2026 sobre `data/raw/`): `GDPC1_2026-10-02.csv` `13f963dec694c782ee1bedab9e81a8420407e671ce50354364330b2cb846e121`; `CPIAUCSL_2026-10-02.csv` `5b49342a4c7d5419f3bfefcdef8a743055da793ec64caa7df3ebbad186374090`; `LOANS_2026-10-02.csv` `56bde6d372a676275af470b586fbe242ef15322d879049996917cf8f311f1fa0`.
- Unidades: los CSV no las traen; la fuente es el PDF «2026 Final Supervisory Stress Test Scenarios» (4-feb-2026), registrado en el manifiesto con su URL, y la página `dfa-stress-tests-2026.htm` donde están los CSV.

Si alguna de estas procedencias fallara en la implementación, se presenta `change` de la 005; ninguna exige reabrir 001, 003 ni 004.

## 3. Funciones puras (firmas)
```python
parse_fed_csv(text: str, expected: FedFileSpec) -> pd.DataFrame      # cabeceras, escenario y 13 trimestres exactos o error (RF-2); el formato «2026 Q1» se convierte a Period('Q-DEC')
adapt_calendar(fed: pd.DataFrame, hist_2025q4: pd.Series, origin: pd.Period, mode: str) -> pd.DataFrame
    # mode='adapted': 2026 Q1 -> origin+1, 13 trimestres 2026T3..2029T3 (principal)
    # mode='post_2026q2': solo Fed 2026 Q3..2029 Q1 en 2026T3..2029T1, H = 11 (RF-12a)
    # mode='from_2025q4': calendario de la Fed, origen 2025T4, 13 trimestres 2026T1..2029T1 (RF-12c)
to_levels(adapted, gdpc1_obs: pd.Series, cpi_obs: pd.Series, unrate_origin: float, rate_origin: float) -> pd.DataFrame   # logs, tasas/4, exige g > −100; niveles implícitos de U y tasa solo informativos (RF-3)
build_regressors(levels, panel_obs, reader_cols, credit_rule: str) -> pd.DataFrame   # PIB, ΔU, π, ΔFFR, CRED(t−4); credit_rule in {"last","zero","mean"}
scenario_d(severe_regs, panel_obs) -> pd.DataFrame                   # solo cambia ΔFFR: observados 2022T1–2023T3 (k=1..7), luego 0
read_model_contract(d: dict, which: str) -> ModelContract            # un lector por contrato (I: cadenas+credit_lag; II: {column,lag}/None)
quarter_to_period(label: str) -> pd.Period                           # "2026T2" <-> "2026Q2"
project(contract, params: pd.Series, X: pd.DataFrame, dr_origin: float, ddr_origin: float, zero_terms: list[str]) -> pd.DataFrame
    # adaptador: construye las columnas que pide forecast.dynamic (incl. y_lag, que se sobrescribe); dr_origin se envuelve en una serie indexada en el origen para reutilizar to_level
sym_block(cov: pd.DataFrame, drop: list[str]) -> np.ndarray          # bloque sin dummies, (V+V')/2
draw_params(mean: np.ndarray, block: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray   # Cholesky; LinAlgError -> ModelDataError
summarize_delta(point_adv, point_base, draws_adv, draws_base) -> pd.DataFrame     # RF-7
rate_sensitivity(draws, scen_adv, scen_d, reg_by_scen, zero_terms) -> pd.DataFrame   # C_m(t) = Δ_sens − Δ_principal por réplica; 2029T3 y trimestre del pico (RF-10)
origin_comparison(adapted_results, results_2025q4) -> pd.DataFrame   # RF-12c: niveles por paso k; error si Δ por paso k no coincide (atol 1e-9)
columns_to_design(contract, level_panel, regs) -> pd.DataFrame      # misma matriz que build_design (003) y el diseño de la 004 sobre una ventana histórica (RF-5b)
```

## 4. Algoritmo
1. Cargar y validar los JSON con su lector (RF-6); leer `reading.etiqueta` y detenerse si es «evidencia fuerte» (RF-9).
2. Leer y validar los archivos de la Fed y la huella (RF-1, RF-2). Adaptar el calendario y enlazar con 2026T2 (identidades de la spec). Construir regresores por escenario: base, adverso principal, D; el tramo posterior a 2026T2 (RF-12a, `mode='post_2026q2'`) y, para RF-12c, el calendario de la Fed desde el origen 2025T4 (`mode='from_2025q4'`: 13 trimestres 2026T1–2029T1, ancla DR(2025T4) y ΔDR(2025T4) observados del panel, referencia del paso 1 Fed 2025 Q4, crédito observado hasta 2027T2 y constante desde 2027T3), comparados con `origin_comparison`.
3. Principal: coeficientes de ΔFFR a 0. Proyectar con β̂ (cifra puntual) con `project`.
4. `rng = np.random.default_rng(20261011)` por modelo (el generador y `np.percentile` con interpolación lineal se fijan aquí, no en la spec); z de forma (10 000, k) en orden fijo; β_r = β̂_bloque + z·Lᵀ; dummies 0. Repetir 3 por réplica y escenario con θ_r puestos a 0 (principal) o sin tocar (sensibilidad RF-10). Mismas réplicas en todo.
5. Resúmenes (RF-7, RF-8): percentiles 5/50/95 por trimestre; proporción de Δ > 0; pico y final; conteos de |ρ| ≥ 1 y de niveles fuera de [0, 100]; sin truncar ni descartar.
6. Sensibilidades RF-10 y RF-12; comparativa RF-11; limitaciones RF-14; variables `estres.*`.

## 5. Claves de `report/_variables.yml` (RF-15)
`estres.horizonte.{origen,inicio,fin,h}`, `estres.replicas.{n,semilla}`; `estres.{m}.{esc}.nivel_{final,pico,pico_trimestre}` para `m` ∈ {`modelo1`, `modelo2`} y `esc` ∈ {`base`, `severo`, `propio`}; `estres.{m}.{esc}.delta_{final,final_p05,final_p95,pico,pico_trimestre,min,sin_aumento,prop_pos_final,prop_pos_pico}` solo para `esc` ∈ {`severo`, `propio`}; `estres.dif_modelos.{esc}.{delta_final,delta_pico}`; `estres.{m}.credito.{n_observados,n_supuestos}`; `estres.{m}.fuera_rango.{n,prop,min,max}`; `estres.{m}.explosivas.{n,prop}`; `estres.sens_tasa.{m}.{esc}.{c_final,c_final_p05,c_final_p95,c_pico,prop_c_pos_final,prop_c_pos_pico}`; `estres.sens_cal.{m}.{delta_final_2029t1,delta_principal_2029t1,delta_pico}`; `estres.sens_cred.{m}.{esc}.{cero,media}.{nivel_final,nivel_pico,nivel_pico_trimestre}` con `esc` ∈ {`base`, `severo`}; `estres.sens_origen.{m}.{esc}.{nivel_final,nivel_pico,nivel_pico_trimestre,delta_k13}` con `esc` ∈ {`base`, `severo`} (`delta_k13` solo severo); Formato de los textos: coma decimal y la precisión de 003/004. Valores no calculables van como texto.

## 6. Salidas
`outputs/tables/stress_paths`, `stress_levels`, `stress_delta`, `stress_rate_sensitivity`, `stress_models`, `stress_sensitivity` (calendario, crédito), `stress_origin` (RF-12c), `stress_limitations` (`.md` y `.csv`); `outputs/figures/stress_model1.png`, `stress_model2.png`; bloque `estres:`.

## 7. Decisiones del plan (con su alternativa descartada)
| # | Decisión | Alternativa descartada |
|---|---|---|
| P1 | Δ por réplica y luego resumen | Restar bandas de niveles (ignora que los parámetros son comunes) |
| P2 | Distribución marginal del bloque, θ puestos a 0 tras extraer | Condicionada a θ = 0: estimador restringido, cambia coeficientes de actividad e inflación |
| P3 | Cholesky; error si falla | Truncamiento espectral silencioso |
| P4 | Solo incertidumbre de parámetros, descrita como tal | Bootstrap de residuos: BP falla y el Chow rechaza |
| P5 | Reutilizar `forecast.dynamic` con adaptador y probar equivalencia con 003 | Reimplementar la recursión |
| P6 | Niveles de PIB/CPI con las funciones de `src/panel.py` sobre `data/raw/` | Añadir niveles a `panel.csv` (cambiaría salidas de la spec 001) |
| P7 | Archivos de la Fed en `data/scenarios/` | Modificar la spec 001 o `data/raw/` |
| P8 | Cambios de la propia trayectoria para ΔU y ΔFFR; k = 1 contra la Fed 2025 Q4 | Medir el paso 1 contra el observado del origen: Δ no cambia (la referencia es común a los dos escenarios), pero el nivel recibe un salto por la diferencia entre el nivel de la Fed y el observado |
| P9 | Adaptación del calendario como principal; calendario original como sensibilidad | Solo calendario original: descarta el tramo inicial del escenario |

## 8. Estrategia de tests
`SEED = 20261011`. `tests/test_scenarios.py`: identidades a mano (g = 4 % → factor 1,04^(1/4); enlace con GDPC1/CPI observados; k = 1 contra 2025 Q4; π en los trimestres cuya base interanual contiene 2025T4, promedio de dos meses), parser con archivos sintéticos incompletos o con cabeceras distintas, D (solo cambia ΔFFR), tramo posterior a 2026T2 (RF-12a). `tests/test_stress.py`: recursión contra solución cerrada (`rtol` 1e-10, `atol` 1e-12); cancelación e invariancia de Δ al mover el origen (RNF-5) bajo las condiciones de las propiedades A y B, con tests negativos cuando se violan; matriz de regresores sobre una ventana histórica igual al diseño de la 003 y de la 004 (RF-5b); huella sha256 de los bytes versionados; réplicas (bloque sintético, N = 200 000, media dentro de 4 errores de MC, covarianza con error relativo de Frobenius < 0,02 y covarianza estandarizada < 0,02, semilla, bloque no definido positivo → error, pareo y ceros en θ); equivalencia con la 003 (RF-5, ajuste de entrenamiento construido en el test); lectores de ambos contratos; lenguaje (RNF-6); pureza (sin red, disco ni gráficos). Los datos reales de la Fed solo se usan en la etapa `stress`.

## 9. Tareas previstas (a detallar en `tasks.md` tras aprobar; ≤ 10)
T1 `.gitattributes`, manifiesto y parser de la Fed · T2 identidades, niveles y enlace · T3 adaptación de calendario, D y calendario original · T4 lectores de contratos, adaptador, recursión con equivalencia 003 y RF-5b (tarea pesada; si crece, dividir en T4a lectores y T4b recursión) · T5 bloque y réplicas · T6 resúmenes de Δ y niveles · T7 sensibilidades · T8 tablas y figuras · T9 etapa `stress` y variables · T10 validación.

## 10. Cobertura RF → plan
RF-1/2 → §2, §3 `parse_fed_csv` · RF-3 → `build_regressors` · RF-4/5 → `project`, P5 · RF-6 → `read_model_contract`, `quarter_to_period` · RF-7/8 → `summarize_delta` · RF-9/10 → `rate_sensitivity` · RF-5b → `columns_to_design`, T4 · RF-10 → `rate_sensitivity`, T7 · RF-11 → `summarize_delta` (diferencia entre modelos), T6/T8 · RF-12 → T7 · RF-12c → `origin_comparison`, T3/T7 · RF-13/14 → T8 · RF-15/16 → T9.
