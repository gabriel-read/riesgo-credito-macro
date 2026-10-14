VEREDICTO: APROBADO

Validación técnica del autor, **Codex**, 12-oct-2026. No es auditoría independiente. Spec 005 **abierta**, T10 pendiente de `review-audit.md` de Claude. Esta revisión se hizo después de finalizar las correcciones técnicas de T9; no se modificó código durante la validación.

## Contrato, alcance y pre-registro

- Usuario aprobó spec/plan v6 en sus bytes exactos y luego las diez tareas, sin incorporar opcionales. Los encabezados originales se conservan para no alterar la versión revisada; aprobación registrada en tasks.md, MEMORY.md y relevo.
- Fuentes `5ba4ada2b1febfb1a3518d728d4ac65341491436` antes de pre-registro `7a3dd2a`; primera proyección real de 005 solo en T9, después de T1–T8 y de esa aprobación. Pruebas previas de recursión/simulación usaron parámetros/regresores sintéticos; RF-5 reproduce el ajuste de entrenamiento ya predefinido, sin selección nueva.
- SHA de spec `6d9713dd1917b4b9b5a2ffc87c7f202869981e9102c9e8e11bf60daac99c77bb` y plan `8b0fc56b3ba2577a0c142a8ab70568af96caed9bf2bbcf18949f42c8ad3d232a` intactos. Tres fuentes Fed coinciden con manifiesto/plan/blobs; FRED fija vintage 2026-10-02, sin descarga ni escritura en raw.
- Solo implementación, tests y salidas de 005; código de 003/004 y contratos aprobados intactos. Pipeline `stress` no ajusta los modelos principales; `all` reproduce las etapas de modelos ya aprobadas. Sin dependencias nuevas, commits nuevos ni push.

## Pruebas y reproducibilidad

| Puerta por tarea | Evidencia ejecutada |
|---|---|
| T1 | 785 passed, 355 warnings, 212.53 s |
| T2 | 792 passed, 378 warnings, 186.16 s |
| T3 | 797 passed, 378 warnings, 176.58 s |
| T4 | 805 passed, 378 warnings, 171.63 s |
| T5 | 807 passed, 378 warnings, 179.95 s |
| T6 | 812 passed, 387 warnings, 204.45 s |
| T7 | 815 passed, 387 warnings, 264.41 s |
| T8 | 818 passed, 387 warnings, 235.03 s |
| T9 final | **823 passed, 503 warnings, 789.19 s**, rc 0 |

Tests primero: fallos por funciones/módulos inexistentes, y casos negativos antes de las correcciones. T1 detectó además `agentes:` en la propuesta de T10: se corrigió a `agente:` manteniendo auditor independiente separado. T9 corrigió rechazo del warmup interanual 1998, formato de números en columna mixta de contrafactuales, error Cholesky sin nombre de modelo y ausencia de comprobación del panel guardado. No se relajaron tolerancias ni se imputaron observaciones.

- `uv run python -m src.pipeline stress`: rc 0, salidas reales en la copia activa.
- `tests/test_frozen_stress.py`: dos ejecuciones stress idénticas, datos y fuentes intactos, salidas previas intactas y bloques `datos`, `modelo1`, `modelo2` preservados; panel alterado o hash incorrecto detienen el proceso antes de proyectar.
- `uv run python -m src.pipeline all` **dos veces**, ambas rc 0, en raíz temporal inicialmente vacía salvo copias de raw y escenarios, usando el código actual: **79 archivos idénticos byte a byte** (outputs y variables). Las 18 salidas stress coinciden por bytes con la copia activa. Los 54 archivos de modelos coinciden en contenido con la copia activa (textos normalizados CRLF→LF; PNG por bytes). Esa normalización se limita a la comparación de salidas previas, no a los CSV Fed.
- Registro completo de huellas/ruta de logs: `docs/reproducibilidad-005-2026-10-12.json`. Dos raíces de verificación separadas de pytest y checkout; no se declara clon de código commiteado porque la implementación debe permanecer local por instrucción del usuario.
- Advertencias: frecuencias M/Q-DEC de pandas y cambio futuro de API ADF de statsmodels, heredados; una advertencia deliberada en test de rechazo de no finitos. No son fallos ni se resolvieron con dependencias nuevas.

## RF → comprobación

| RF | Evidencia de código, tests y salidas |
|---|---|
| RF-1/2 | `pipeline.load_fed_sources`, huellas exactas adicionales en `stage_stress`; `scenarios.parse_fed_csv`; tests de cabeceras, escenarios, huecos, valores, manifest BOM y bytes alterados |
| RF-3 | `load_stress_history` verifica filas/fecha/nombre/último dato/SHA LF de FRED; `to_levels`, `build_regressors`; identidades exactas, CPI RF-11 y futuro observado ignorado; `stress_paths` |
| RF-4/5/5b | `project` reutiliza dynamic/to_level; solución cerrada; diseño histórico columna por columna frente a ambos modelos; OOS predefinido sin poner tasa cero; `test_stress.py` |
| RF-6 | Lectores diferenciados, mapas/orden/dimensiones/forma y etiquetas T/Q/Fed; panel guardado cotejado con vintage; contratos originales intactos |
| RF-7/8 | Cholesky marginal sin reparar; N=10000 y semilla fija; pareo; puntual separado de mediana; percentiles 5/50/95 lineales, pico firmado/empates, no aumento/mínimo, conteos fuera de rango/explosivos sin descartar; `stress_delta`, `stress_levels` |
| RF-9 | Regla de lectura, tasa cero después de extraer; fuerte exige change; D y severo idénticos bajo principal; primer cambio del Modelo II exactamente cero |
| RF-10 | C=Δ_sens−Δ_principal por réplica; final y trimestre del pico puntual de sensibilidad; rótulo y proporciones; `stress_rate_sensitivity`, claves `sens_tasa` |
| RF-11 | Δ y diferencia puntual I−II, sin banda/conjunto; `stress_models` |
| RF-12 | Recorte de 11 pasos contra Fed 2026Q2 y comparación al mismo 2029T1; crédito cero/media sobre niveles, dimensiones modelo/escenario; `stress_sensitivity` |
| RF-12c | Trece pasos con origen 2025T4, anclas observadas, regla y crédito fijados; contrafactuales 2026T1/T2 junto al observado; error si Δ por paso difiere más de 1e-9; `stress_origin` |
| RF-13/14 | Figuras de dos paneles con fuente/etiquetas/bandas/advertencias; limitaciones fijas y diagnósticos fallidos/OOS/extremos detectados; `stress_limitations` |
| RF-15/16 | Ocho tablas CSV/MD, dos PNG y árbol completo `estres.*`, solo texto desde resultados; pruebas de formato/precisión/tipos y dimensiones |

## RNF y revisión de artefactos

RNF-1 pre-registro antes de datos reales de 005. RNF-2 solución cerrada (rtol 1e-10, atol 1e-12). RNF-3 identidades y base CPI de dos meses. RNF-4 test de 200000 réplicas sintéticas: media en cuatro errores MC, Frobenius/covarianza estandarizada < 0.02, semillas/pareo/errores. RNF-5 invariancia bajo condiciones y casos negativos (crédito/coeficientes/referencias distintos, innovaciones distintas e interanual no logarítmica). RNF-6 lenguaje de asociación y etiquetas de sensibilidad. RNF-7 dos corridas. RNF-8 funciones puras, lectura/escritura solo en pipeline y tests sin red. RNF-9 etiquetas en español; Markdown con coma decimal, CSV preciso.

Inspección visual de ambos PNG: dos paneles, ejes trimestrales legibles, bandas y fuentes/advertencias sin recortes; la superposición D/severo refleja su coincidencia por construcción. Inspección de `stress_origin.md`: observados con coma decimal y ausencia indicada como «no aplica». Ningún resultado nuevo se tecleó en informe o diapositivas.

## Límites y entrega

La tasa implícita informativa de RF-3 usa FEDFUNDS observada como ancla del proxy y los cambios de Treasury de los escenarios; se rotula `tasa_proxy_implicita`. No se incorporó otra serie ni cambió el cálculo del riesgo; ese nivel no entra en los modelos. Los signos contrarios solo se muestran en sensibilidad. Se mantienen las limitaciones metodológicas aprobadas y el supuesto de crédito, sin innovaciones simuladas ni intervalos de predicción.

La implementación está sin commit y el checkout contiene cambios locales previos del arnés/otras specs. No se afirma git status limpio ni se incluyen esos cambios en la validación de 005. La auditoría independiente de implementación de Claude aún **no existe** en esta entrega; ronda 4 es revisión del plan, no auditoría de código. Rutas/criterios originales, sin conclusión del autor: `docs/paquete-auditoria-005-2026-10-12.md`. No declarar 005 cerrada hasta auditoría independiente APROBADA.
