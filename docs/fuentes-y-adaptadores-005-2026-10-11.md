# Fuentes congeladas y adaptadores para el borrador 005 (procedimientos y antecedente)

> Estado actual y única lista de pendientes: docs/congelacion-fed-005-2026-10-11.md, sección «Contraste actualizado con v5». Los hallazgos de versiones anteriores que aparecen abajo son históricos; vintage, RF-12c, crédito por escenario, cobertura, transformaciones y fixture ya están resueltos documentalmente. No tratarlos como bloqueos vigentes.

Codex, 11-oct-2026. Documentación técnica para Claude; sin implementación, descarga al repo, ajuste ejecutado ni proyección. No modifica 003/004 ni aprueba metodología. Lectura de los borradores actuales y `specs/005-estres/review-plan.md` (CAMBIOS NECESARIOS). Solo el paso de lectores JSON/fechas está incorporado en el plan observado; las demás modificaciones anunciadas aún no aparecen completas. Volver a cotejar después de la edición de Claude.

## Niveles de PIB y CPI: ruta de reconstrucción aprobada

1. En la capa de E/S, usar `src/fred_io.py::load_latest_raw(Path('data/raw'))`. Devuelve `raw` y manifiesto, leyendo archivos ya congelados; no invoca descargas. Comprobar que los archivos elegidos siguen siendo los del manifiesto usado para los modelos, descarga 2026-10-02. Registrar sus nombres/huellas en la evidencia de 005; no modificar el manifiesto original. Si faltan, detenerse: no seguir la sugerencia de descarga que aparece en el mensaje de error del lector.
2. Las fuentes de niveles son `data/raw/GDPC1_2026-10-02.csv` y `data/raw/CPIAUCSL_2026-10-02.csv`. `src/panel.py::parse_raw(raw['GDPC1'], 'GDPC1')` y `quarterly_from_quarterly(...)` recuperan nivel trimestral y máscara de completitud. `parse_raw(raw['CPIAUCSL'], 'CPIAUCSL')` y `quarterly_from_monthly(..., 'CPIAUCSL')` recuperan promedio trimestral, máscara y tratamiento documentado. Son funciones puras ya aprobadas; no recalcular agregación con otra regla.
3. CPI de 2025T4 se promedia con noviembre/diciembre por RF-11. Conservar tratamiento y máscara; no imputar octubre. Validar trimestres necesarios completos, positivos y presentes. Recortar observados a `sample_end = 2026Q2`; no consumir macro de 2026T3 aunque esté en las descargas.
4. `src/panel.py::build_panel(raw)` reconstruye `PanelResult.full`, `.panel` y `.end` para regresores e historia. **No expone niveles GDPC1/CPI**: `full` contiene transformaciones, no `quarterly_full`. Obtener los niveles por las funciones del paso 2, sin cambiar `PanelResult` de 001 ni el CSV procesado.
5. Desde el ancla, para tasas anualizadas `g`, encadenar `log L_t = log L_(t-1) + log(1 + g_t/100)/4`, exigiendo `g > -100`. Construir la historia de niveles observados y proyectados por trimestre y reutilizar `src/panel.py::yoy`: `100*(log L_t - log L_(t-4))`. Igual para CPI. No usar variación porcentual simple ni dividir la anualizada por cuatro. El test de g=4 debe esperar `1.04**0.25`, no 1.01.
6. El plan debe añadir estas entradas y firmas: niveles observados de PIB/CPI separados del panel transformado, índice trimestral y origen. Conserva memoria desde 1998 para entrenamiento; para estrés basta la historia de niveles necesaria para t−4 y el ancla. La capa de E/S lee y la lógica pura recibe las series; no ejecutar `stage_data` para obtenerlas porque escribe salidas.

## Parámetros del entrenamiento de 003: reproducción, no nueva selección

- Fuentes: el mismo `raw` congelado; `build_panel(raw).full`; `outputs/tables/stationarity.csv` y `src/design.py::read_decisions`, seguidos de `check_expected_forms(..., src.model1_config.EXPECTED_FORMS)`. No volver a elegir formas ni rezagos a partir de nuevos tests.
- Procedimiento existente: `src/model1.py::out_of_sample(full, decisions, end)` devuelve un `OOSResult`, incluido `train_fit` y `train_design`. Sus constantes están en `src/model1_config.py`: `OOS_TRAIN=('2000Q1','2019Q4')`, evaluación desde `2022Q1`, ancla `2021Q4`. No usar 2021T4 como fin de entrenamiento; la nota técnica anterior se corrigió expresamente.
- Para el futuro fixture de RF-5, llamar este procedimiento en memoria, con `end=2026Q2`, y pasar `result.train_fit.params` al adaptador dinámico. Construir X de evaluación según `out_of_sample`: `MAIN` con `covid_dummies=False`, inicio 2022Q1 y mismos controles/rezagos; ancla en ΔDR(2021Q4), nivel en DR(2021Q4). Comparar contra `result.series` (columna `dinamico`, comprobada en la implementación actual). No poner la tasa en cero en este test de equivalencia: esa regla pertenece al estrés, no al pronóstico original de 003.
- Esta llamada ejecuta numéricamente el ajuste ya fijado (MCO/HAC), sobre la misma muestra y datos, para reproducir la evidencia aprobada. No es una búsqueda de modelo ni una nueva decisión econométrica. La sesión actual solo lo documenta, no lo ejecuta. No hace falta exportar otro JSON ni modificar 003.
- Una nueva selección de rezagos, otra muestra, actualización de datos, cambios de regresores/dummies/HAC o restricciones que cambien el estimador quedan fuera de esta reproducción. Requieren resolver contrato y aprobación antes de ejecutar; no presentarlos como recuperación de parámetros.
- `model1_main.json` contiene parámetros de la muestra principal, no de entrenamiento. El fixture reconstruido es solo para RF-5; las proyecciones de estrés consumen ambos JSON principales sin ajustarlos de nuevo.

## Compatibilidad de lectores y escenarios

| Punto | Estado del borrador consultado / bloqueo concreto |
|---|---|
| Lectores | `plan.md` §3.1 ya distingue I (texto + `credit_lag`) de II (objetos `{column,lag}` y nulos). Validar dimensiones, orden `terms`/`params`/`cov_hac`, columnas y dummies; I no declara `y_lag` en `columns`, inferir por `form`; II lo declara como `dralacbs_d`. No exigir K en el JSON I. |
| Fechas y origen | §3.1 reconoce JSON `2026T2` y panel `2026Q2`: normalizar a `Period(..., freq='Q-DEC')`, igualar ambos `sample_end`, comprobar anclas no faltantes y prohibir observados posteriores. FED y archivos pueden traer otra sintaxis: el parser debe declarar su formato y convertirlo al mismo índice. |
| Recursión | `forecast.dynamic` exige X con todas las columnas, incluso `y_lag` y dummies, aunque sustituye el rezago recursivamente. Ancla en diferencia, dummies cero. Adaptar `project` a `to_level(pred, form, level_obs, anchor, 'dynamic')`; su firma no recibe un escalar de nivel directamente. |
| Horizonte completo | `spec.md` Definiciones aún recorta 2026T1–T2 y usa H=11. `review-plan.md` punto 1 pide resolver el re-fechado de los 13 trimestres: si se adopta, j=1..13 de Fed 2026T1–2029T1 se mapea a 2026T3–2029T3, con fila origen Fed 2025T4 del CSV histórico. La elección sigue pendiente del autor; no certificar cobertura completa con el recorte actual. |
| Transformaciones | Declarar explícitamente interanual logarítmica, corregir test 1.01 en plan §6 y usar fuentes de niveles del apartado anterior. ΔU/Δtasa del primer trimestre deben usar el origen propio Fed; controles rezagados del Modelo II usan la historia observada en el primer paso. No confundir origen Fed con ancla de morosidad. |
| Crédito | D-CRED aún cuenta siete trimestres hasta 2027T2: son cuatro desde 2026T3; con H=13, nueve requieren supuesto. Cubrir todos los trimestres sin rellenar silenciosamente. RF-12 sobre Δ se cancela con crédito común; lo que cambia son niveles, conforme a review-plan punto 7. |
| Escenarios | Base y adverso requieren igual índice completo, cuatro variables, fila origen y unidades. S3 aún usa episodio de ocho trimestres para once/trece, sin extensión definida ni conversión de inflación interanual a tasa trimestral. Las tres opciones no tienen cobertura técnica completa hasta que Claude precise su trayectoria o el autor descarte S3. No construirla a partir de resultados. |
| Sensibilidades | RF-10(c) no fija reparto del efecto acumulado entre θ0/θ1: no es implementable sin una regla. Marginal/condicionada y RNF-4 pendientes de resolver conforme a review-plan. No decidir metodología en este documento. |

## URLs oficiales y propuesta de congelación (pendiente de acuerdo)

Enlaces **Final** identificados el 11-oct-2026 en [la página oficial DFAST 2026](https://www.federalreserve.gov/supervisionreg/dfa-stress-tests-2026.htm):

- [Final Historic Domestic CSV](https://www.federalreserve.gov/supervisionreg/files/2026_Final_Historic_Domestic.csv)
- [Final Supervisory Baseline Domestic CSV](https://www.federalreserve.gov/supervisionreg/files/2026_Final_Supervisory_Baseline_Domestic.csv)
- [Final Supervisory Severely Adverse Domestic CSV](https://www.federalreserve.gov/supervisionreg/files/2026_Final_Supervisory_Severely_Adverse_Domestic.csv)

Se verificaron los destinos de los enlaces de la página oficial; el lector web no interpreta el MIME application/octet-stream del CSV. No se acredita aquí una inspección de sus contenidos ni una huella descargada. `review-plan.md` documenta la lectura temporal realizada por el auditor independiente; conservar esa procedencia.

Propuesta para aprobación del usuario: `data/scenarios/fed/2026-final/<fecha-descarga>/`, con los tres nombres oficiales intactos y `manifest.csv` junto a ellos (URL exacta, escenario, versión final, fecha/hora UTC, SHA-256, tamaño, cobertura y unidades verificadas). Guardar bytes originales sin normalizar; procesamiento derivado separado. El histórico es necesario para el origen de las trayectorias, no para reemplazar FRED. No mezclar versiones Proposed/Final ni usar solo dos CSV sin origen histórico.

La ubicación está fuera de `data/raw/` y no exige modificar 001. No se ha creado el directorio ni descargado archivos. Tras acuerdo de ubicación, congelar por una sola herramienta y dejar el pipeline sin red; no sobrescribir una congelación existente. Cambiar archivos o versión requiere una nueva evidencia explícita.

## Continuidad

Claude debe incorporar las entradas de niveles/fixture y resolver los bloqueos del borrador; Codex cotejará la nueva versión por rutas. Pendientes de aprobación: metodología, spec/plan y ubicación de congelación. No se ejecutó pytest por ausencia de cambios de implementación; se conserva la evidencia de 774 tests. Una sola herramienta escribe en el checkout; esta sesión entrega documentación y termina su escritura.

Actualización posterior autorizada: fuentes descargadas y congeladas en data/scenarios/fed/2026-final/2026-10-11/. El contraste con la v3 consolidada y los bloqueos restantes están en docs/congelacion-fed-005-2026-10-11.md; sustituyen los estados pendientes del borrador anterior en esta nota. CSV originales intactos, manifiesto con SHA-256 propios y .gitattributes limitado a tres rutas. No implementación ni estimación.
