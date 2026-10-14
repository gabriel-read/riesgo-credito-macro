VEREDICTO: APROBADO

Comprobación independiente final y acotada (**ronda 4**) de la v6 de la spec y el plan de la 005 (Estrés), 11-oct-2026. Autor: subagente `revisor-econometrico` de Claude Code (otra instancia que las rondas anteriores), con solo rutas y alcance acotado: los cambios de la ronda 3 y los puntos pendientes del autor; no es una revisión completa del diseño. Las rondas anteriores se conservan en `review-plan-ronda1.md`, `review-plan-ronda2.md` y `review-plan-ronda3.md`. Informe copiado tal cual lo entregó el subagente. Esta revisión no aprueba nada por el autor: la spec y el plan siguen sin aprobar hasta que él lo diga.

**Versión exacta revisada** (huellas calculadas por el revisor al empezar y al terminar, e iguales; recalculadas por Claude Code después de recibir el informe y coinciden):
- `specs/005-estres/spec.md`, sha256 `6d9713dd1917b4b9b5a2ffc87c7f202869981e9102c9e8e11bf60daac99c77bb`
- `specs/005-estres/plan.md`, sha256 `8b0fc56b3ba2577a0c142a8ab70568af96caed9bf2bbcf18949f42c8ad3d232a`

Cualquier edición de esos archivos invalida este veredicto para la versión editada.

No modificó ningún archivo del repositorio. La suite de tests da 774 passed (`uv run pytest -q`). No ejecutó la etapa `stress` ni proyectó con datos reales.

**En corto.** Los siete cambios de la ronda 3 y los cinco puntos que había pedido verificar están resueltos y comprobados con evidencia. No encontró ningún bloqueo real entre spec y plan, ni con las specs 003 y 004. Quedan seis observaciones opcionales, ninguna obligatoria. La más útil es aclarar de dónde sale el nivel observado de la tasa a 3 meses en 2026T2 (observación 1).

## A. Cambios 1 a 7 de la ronda 3

| # | Estado | Evidencia en la v6 |
|---|---|---|
| 1 Propiedad A | Resuelto | `spec.md:48`. La condición (v) ahora pide una referencia del paso 1 «común a ambos escenarios» y dice que un valor observado común «también serviría» y solo cambiaría el nivel. También exige interanuales «en logaritmos». La lista «No vale» ya no incluye el paso 1 medido contra el observado. Ahora incluye: referencia del paso 1 distinta entre escenarios, escenario truncado o desplazado (RF-12a), interanual no logarítmica, transformación no lineal y β que cambian con el origen. Rehizo el álgebra de δ con los términos de ambos JSON y la lista es correcta. P8 (`plan.md:83`) da ahora el motivo verdadero: un salto en el nivel, no en Δ. |
| 2 RF-12c | Resuelto | `spec.md:99`, `plan.md:43,55,61`. Todo queda fijado sin margen de interpretación: el crédito es observado hasta 2027T2 y desde 2027T3 toma `loans_yoy` de 2026T2; la referencia del paso 1 es la Fed 2025 Q4; la comparación es por paso k (2029T1 frente a 2029T3); los niveles de 2026T1–T2 se presentan como contrafactuales junto al DR observado; y el pipeline se detiene si Δ difiere en más de `atol` 1e-9. |
| 3 Huellas, `.gitattributes`, fecha | Resuelto | `plan.md:23-31`. Las tres huellas completas y los tamaños (16 936, 1 692 y 1 824 B) coinciden con su `sha256sum`, con `manifest.csv` y con `docs/congelacion-fed-005-2026-10-11.md`. El plan aclara que la fecha del directorio es local y que la hora UTC está en el manifiesto. |
| 4 Claves | Resuelto | `plan.md:68,71`. Las claves son `sens_cred.{m}.{esc}.{cero,media}.*` con `esc` ∈ {base, severo}, más `sens_origen.*` y la tabla `stress_origin`. `prop_c_pos_final` y `prop_c_pos_pico` corresponden a los trimestres que fija RF-10 (`spec.md:96`). |
| 5 Test de π con base 2025T4 | Resuelto | `spec.md:108`, `plan.md:87`. |
| 6 Propiedad B nombra la linealidad | Resuelto | `spec.md:49` empieza con «Si el modelo es lineal en la forma de Y». |
| 7 Regla de corte de D | Resuelto | `spec.md:57`: la regla va de la primera a la última alza del FOMC, con sus URL, y explica por qué 2023T4 queda fuera. |

## B. Puntos pendientes del autor

| # | Estado | Evidencia |
|---|---|---|
| 1 `.gitattributes` | Resuelto | El plan (`plan.md:24`) coincide literalmente con las tres rutas exactas `-text` del `.gitattributes` actual. La única coincidencia de `scenarios/**` en spec y plan es la negación «No se amplía a `data/scenarios/**`» (`plan.md:24`). Para los tres CSV, `git check-attr` da `text: unset` y `git hash-object --no-filters` produce el mismo blob que `--path` (`cbe8ded…`, `f452e7b…`, `ffd4a4f…`). Las reglas no alcanzan `manifest.csv` ni `data/raw/`. |
| 2 Fechas y enlaces de D | Resuelto; [VERIFICAR] puede eliminarse | Descargó con curl las cuatro páginas oficiales (las cuatro dieron HTTP 200). El comunicado del 16-mar-2022 sube el rango a «1/4 to 1/2 percent». El del 26-jul-2023 lo sube a «5-1/4 to 5-1/2 percent». El del 20-sep-2023 dice «decided to maintain». La tabla `openmarket.htm` fecha esos cambios el 17-mar-2022 y el 27-jul-2023, y después solo lista bajadas desde sep-2024 hasta dic-2025. En el panel, los ΔFFR de 2022Q1–2023Q3 son 0,04; 0,65; 1,42; 1,463; 0,863; 0,473 y 0,27, todos ≥ 0. 2023Q4 vale 0,07 y se excluye. Desde 2024Q1 hasta 2026Q2 ninguno es positivo (2024Q1, 2024Q2 y 2025Q2 valen exactamente 0). La marca solo sobrevive en la leyenda de `spec.md:4`. |
| 3 Vintage FRED | Resuelto | `plan.md:17,32`. Nombres, número de filas y último dato coinciden con `data/raw/manifest.csv`: GDPC1 114 filas hasta 2026-04-01; CPIAUCSL 344 hasta 2026-08-01; LOANS 344 hasta 2026-08-01. Recalculó los sha256 con los finales de línea normalizados a LF: `13f963de…e121`, `5b49342a…4090` y `56bde6d3…1fa0`. Coinciden con el plan y con el sha256 del blob de HEAD (`git show`), así que son estables en un clon limpio. `load_latest_raw` (`src/fred_io.py:234-283`) devuelve los datos y el manifiesto pero no verifica nada por sí misma. La capa de E/S de `stress` puede hacer toda la verificación que pide el plan sin cambiar `fred_io`: comparar la fila más reciente con 2026-10-02, el nombre, `n_rows` y el último dato, y releer los bytes para el sha256. El plan prohíbe expresamente usar un glob. |
| 4 Claves, RF-12c y huellas | Resuelto | Ver las filas A.3 y A.4. El bloque `cov_hac` de los JSON tiene 7 términos sin dummies en el Modelo I y 8 en el II, como dice `spec.md:69`. En el Modelo II todos los controles, salvo `d_ffr_l0`, van rezagados, así que la afirmación de RF-14 de que Δ(1) = 0 se sostiene. `reading.etiqueta` es «sin evidencia», de modo que RF-9 aplica la regla de la tasa en cero. |
| 5 Bloqueos 1–4 de `docs/congelacion-fed-005-2026-10-11.md` | Resuelto | 1 → `plan.md:24`. 2 → `plan.md:43,61` (rama `from_2025q4`). 3 → `plan.md:68`. 4 → `plan.md:17,32`. |

## C. Contradicciones
No encontró ningún bloqueo real. Spec y plan coinciden en el origen, el horizonte, D, el crédito, la simulación, las claves y las salidas. Los nombres de funciones y firmas que cita el plan existen y encajan: `out_of_sample` (`model1.py:588`), `build_design2` (`design2.py:82`) y `dynamic`/`to_level` (`forecast.py:45,71`).

## Cambios necesarios
Ninguno.

## Observaciones opcionales (no bloquean)
1. **Nivel observado de la tasa a 3 meses en 2026T2.** RF-3 (`spec.md:88`) y el parámetro `rate_origin` (`plan.md:44`) no dicen de qué serie sale ese nivel, y en `data/raw/` no hay tasa a 3 meses. Lo natural es usar `fedfunds` del panel en 2026Q2 (3,633). La elección importa por un motivo concreto. El adverso implica un nivel de origen − 3,6: con FEDFUNDS el nivel queda en 0,033 y no salta la advertencia de nivel negativo, pero con un origen algo menor sí saltaría. No afecta a ningún Δ, nivel de DR ni clave. Conviene fijarlo con una frase en el plan o en `tasks.md`.
2. **«Se trunca o desplaza».** En la lista «No vale» de `spec.md:48`, «desplaza» puede confundirse con el desplazamiento de etiquetas de la propia adaptación (`spec.md:30`). Una redacción más precisa: «si se omiten o reordenan trimestres de la trayectoria».
3. **Leyenda de marcas.** En `spec.md:4` sobran las marcas [VERIFICAR] y [DECIDIR], porque ya no hay ninguna en el texto.
4. **Frase sobre la tabla de cambios.** `spec.md:57` dice que la tabla «no lista alzas posteriores hasta diciembre de 2024». Es cierto, pero la tabla actual sí lista una alza de 25 pb el 17-sep-2026 (2026T3, después del origen y fuera de la muestra). Sería más exacto: «ninguna en la muestra; la siguiente es del 17-sep-2026, posterior al origen».
5. **Lista de tests negativos de RNF-5.** La lista de `spec.md:110` no menciona un crédito distinto entre escenarios (condición iv) ni un escenario truncado. Por otro lado, `spec.md:50` dice que se probará la violación de «cada una» de las condiciones. Conviene que la lista sea completa o que diga «entre otras».
6. **LOANS crudo y manifiesto de la Fed.** Leer `LOANS_2026-10-02.csv` (`plan.md:17`) es redundante si el crédito sale de `loans_yoy` del panel; no hace daño. Aparte, `manifest.csv` no lleva la regla `-text` y sus bytes cambian con los filtros de git. Es inocuo mientras su huella no se verifique (hoy no se verifica).

Antes de proyectar sigue haciendo falta lo que exige RNF-1, en este orden. Primero, un commit solo con `.gitattributes` y los cuatro archivos de `data/scenarios/fed/2026-final/2026-10-11/` (los tres CSV y `manifest.csv`). Después, el commit del pre-registro, solo con `specs/005-estres/`. Es un paso de procedimiento, no un defecto de esta versión.

**Lo que defendería ante el profesor**
- El Δ por paso no depende del origen. Las condiciones que lo garantizan están escritas y bien delimitadas, y RF-12c lo comprueba deteniendo el pipeline si no se cumple.
- Los escenarios de la Fed y el vintage de FRED quedan fijados con sha256 sobre bytes que git preserva. Las fechas de corte de D están respaldadas por los comunicados oficiales del FOMC.
- La regla de la tasa en cero viene pre-registrada desde la 004. La sensibilidad con los coeficientes estimados va aparte, réplica a réplica, con el rótulo «sensibilidad, no efecto estimado».

**Lo que preguntaría el profesor**
1. Si D da la misma proyección que el adverso, ¿qué aporta al ejemplo de la guía de un «aumento de la tasa»?
2. ¿Por qué aproximar ΔFFR con la letra a 3 meses en la base y el adverso, pero con FEDFUNDS observada en D?
3. Los niveles contrafactuales de 2026T1–T2 con origen 2025T4 no coinciden con lo observado: ¿qué dice eso de la base de la Fed?
