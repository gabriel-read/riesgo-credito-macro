# Rutas y criterios originales para auditoría independiente de 005 — ronda 3

Copia única: `C:/Users/gabri/orca/riesgo-credito-macro`, rama `spec/004-modelo-ii`. HEAD de pre-registro `7a3dd2a`; fuentes anteriores `5ba4ada`. Implementación local, sin nuevos commits ni push. Este paquete enumera artefactos y contratos; no contiene un veredicto sobre la implementación.

## Identidad exacta de la corrección vigente — 12-oct-2026

SHA-256 recalculados sobre bytes de la copia activa, no tomados de una revisión anterior. Coinciden con `docs/reproducibilidad-005-ronda3-2026-10-12.json`. Código, tests y salidas siguen intactos desde la suite de 837 tests; Codex no repitió pytest. Claude confirmó estas cuatro huellas en su terminal antes de registrar la auditoría.

| Archivo absoluto | SHA-256 actual |
|---|---|
| `C:/Users/gabri/orca/riesgo-credito-macro/src/stress_tables.py` | `2e4e91f1174dd9a2f341564c7013d3ea8bedc438e020ee7dcaae148dfca81b7e` |
| `C:/Users/gabri/orca/riesgo-credito-macro/tests/test_stress_outputs.py` | `4f2cd5dd553bf625d2de4a6647dad78b952203d9d0aa54888749623403b0ad64` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/tables/stress_levels.md` | `fda1b19d244cdb8b41cdb7ce3191b32d14c2a9394f8f67c717045c16ed23616a` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/tables/stress_delta.md` | `5eb869064970fe3d110c0b4e02aae65d069a0fdc7bcbad535db6cb8bb7f2f4ce` |

Test de regresión dentro del archivo identificado: `tests/test_stress_outputs.py::test_halfway_rounding_matches_cells_variables_and_both_footnotes`. La huella corresponde al archivo completo, incluido ese test; usa `np.float64(0.0105)` y coteja variable, celda y ambos pies. El revisor debe vincular su informe a estas versiones exactas; si alguna huella difiere, no trasladar el veredicto a otra versión.

## Contratos y autoría

- `specs/005-estres/spec.md`, `plan.md`: v6 aprobada por el usuario, originales exactos (encabezados conservados). SHA de spec `6d9713dd1917b4b9b5a2ffc87c7f202869981e9102c9e8e11bf60daac99c77bb`; plan `8b0fc56b3ba2577a0c142a8ab70568af96caed9bf2bbcf18949f42c8ad3d232a`.
- `specs/005-estres/tasks.md`: tareas aprobadas por el usuario; criterio de auditoría en T10.
- `specs/005-estres/review-plan.md`, `review-plan-ronda1/2/3.md`: historial independiente de plan. No sustituye auditoría de implementación.
- `docs/constitution.md`, `docs/guia-profesor.md`, fuentes compartidas `.claude/skills/{sdd,datos-fred,econometria-series-tiempo,informe-quarto}/SKILL.md`; usuario conserva autoridad y límites sobre archivos aprobados.
- Contratos previos: `specs/003-modelo-i/{spec,plan}.md`, `specs/004-modelo-ii/{spec,plan}.md`; no revisar opcionales de 004 como cambios obligatorios de 005.

## Entradas originales

- `.gitattributes`; `data/scenarios/fed/2026-final/2026-10-11/{2026_Final_Historic_Domestic.csv,2026_Final_Supervisory_Baseline_Domestic.csv,2026_Final_Supervisory_Severely_Adverse_Domestic.csv,manifest.csv}`.
- `data/raw/manifest.csv` y descargas fijadas por plan §2, solo lectura. `data/processed/panel.csv`.
- `outputs/models/model1_main.json`, `model2_main.json`; tablas originales de diagnósticos y OOS en `outputs/tables/model1_*`, `model2_*`; `report/_variables.yml` con bloques previos.

## Código y tests para examinar

- `src/scenarios.py`, `stress.py`, `stress_tables.py`, `stress_figures.py`, `pipeline.py`.
- Procedimientos anteriores reutilizados: `src/panel.py`, `forecast.py`, `design.py`, `design2.py`, `model1.py`, `model1_config.py`, `model2_config.py`, `fred_io.py`.
- `tests/test_scenarios.py`, `test_stress.py`, `test_stress_outputs.py`, `test_stress_audit.py`, `test_frozen_stress.py`, pureza en `test_pipeline.py`; suites previas de modelos, datos y no regresión.

## Salidas reales a auditar

- `outputs/tables/stress_paths.{csv,md}`, `stress_levels.{csv,md}`, `stress_delta.{csv,md}`, `stress_rate_sensitivity.{csv,md}`, `stress_models.{csv,md}`, `stress_sensitivity.{csv,md}`, `stress_origin.{csv,md}`, `stress_limitations.{csv,md}`.
- `outputs/figures/stress_model1.png`, `stress_model2.png`; bloque `estres:` de `report/_variables.yml`.

Examinar RF/RNF y casos límite originales, sin ampliar metodologías: cobertura, identidades, ambos JSON, anclas y rezagos, distribución marginal y pareo, reglas de tasa, resúmenes/extremos, RF-12c, lenguaje, fuentes y no regresión/reproducibilidad. No recibir como conclusión previa la validación del autor: rehacer comprobaciones desde los originales. Si se requieren correcciones, enumerar ruta/línea, contrato incumplido y resultado esperado; conservar rondas antes de reemplazar review-audit.md.

## Alcance vigente de la ronda 3

Estado final (12-oct): Claude registró `VEREDICTO: APROBADO` en `review-audit.md`, ronda 3, con las cuatro huellas vigentes más spec/plan. Codex las recalculó y cotejó íntegramente; coinciden, al igual que los archivos protegidos. Conforme a la autorización condicional del usuario, T10 está completa y 005 cerrada en tasks/MEMORY. Las rondas 1/2 están conservadas; el cierre no modifica bytes de spec/plan ni aplica opcionales. Claude cedió después el checkout a Codex para ese registro y el humo mínimo 006.

Antecedente de la revisión: `specs/005-estres/review-audit-ronda2.md` y su único bloqueante de consistencia de redondeo. El informe actual es la ronda 3 APROBADA; no confundirlo con ese antecedente. No implementar observaciones opcionales de ninguna ronda.

La modificación de producción se limita a las tres conversiones a `float` antes de `fmt_es` del pie en `src/stress_tables.py` (proporción, mínimo y máximo). Test nuevo: `tests/test_stress_outputs.py::test_halfway_rounding_matches_cells_variables_and_both_footnotes`, valor 0,0105 y comprobación de variable/celda/ambos pies, con CSV sin redondear. El resto de los contratos, código y tests conserva su versión.

Verificar independientemente: (1) criterio idéntico de formato y test que detecta reintroducir el defecto; (2) inventario antes/después: solo `outputs/tables/stress_levels.md` y `stress_delta.md` deben cambiar, exclusivamente el texto de la proporción en sus pies; CSV, demás tablas, PNG, YAML, datos y modelos 003/004 intactos. Fuentes y procedimientos originales siguen en las rutas de este paquete.

Huellas y procedencia: `docs/reproducibilidad-005-ronda3-2026-10-12.json`; registros anteriores intactos. La entrega mantuvo T10/005 abiertas hasta la aprobación independiente; no se adoptó como conclusión previa la validación del autor. El veredicto es del revisor de Claude y se conserva con su autoría real, sin atribuir independencia a Codex.

## Antecedente: alcance de la ronda 2

La auditoría de implementación ronda 1 permanece en `specs/005-estres/review-audit-ronda1.md`; sus cinco bloqueantes fueron revisados por Claude en ronda 2 y únicamente quedó el redondeo del pie. La corrección de ronda 2 se limitó a `src/stress.py`, `src/stress_tables.py` y los cuatro tests de estrés indicados; fuentes, código de escenarios/figuras/pipeline y contratos aprobados se conservaron.

Verificar desde los artefactos originales:

1. Árbol exacto de `estres.*` contra plan §5, incluidos los seis prefijos `delta_`, ambos modelos, escenarios y sensibilidades. Test del conjunto completo en `test_stress_audit.py` y sobre resultados congelados en `test_frozen_stress.py`.
2. Campos de `stress_levels`: conteos por trimestre, totales/proporciones por escenario, unión de réplicas por modelo, mínimos/máximos y trimestres afectados; advertencias cuando corresponde en niveles y cambio. No sumar conteos para construir el total por modelo.
3. `dif_modelos.delta_pico` como diferencia entre los picos individuales; distinguirla del máximo de la diferencia trimestral conservada en `stress_models`.
4. Ancho válido de filas Markdown, pipes escapados conservando CSV literal y encabezados trimestre_adaptado/trimestre_original en ambos formatos.
5. RNF-5: negativos de referencia distinta y Y no lineal para ambos modelos frente a una recursión de δ independiente, y negativos restantes. RNF-6: revisar los ocho CSV/MD y el árbol estres; tests que los recorren.

Registro técnico para comprobar huellas y procedencia, sin adoptar un veredicto del autor: `docs/reproducibilidad-005-ronda2-2026-10-12.json`. Registro anterior conservado: `docs/reproducibilidad-005-2026-10-12.json`. Volver a verificar salidas regeneradas, reproducibilidad y preservación de 003/004. No recibir `review-validate.md` ni MEMORY/relevos como conclusión previa; Codex conserva su validación anterior en `review-validate-ronda1.md`.

Claude es responsable de `specs/005-estres/review-audit.md` independiente. Una sola herramienta escribe en el checkout a la vez: Codex entrega el checkout al cerrar esta sesión. Mantener T10 y 005 abiertas durante la auditoría. Si falta cuota, registrar punto de continuidad (rutas leídas, comprobaciones hechas/pendientes y siguiente acción) y mantener auditoría pendiente; no transferirla a Codex ni atribuir independencia a su validación.
