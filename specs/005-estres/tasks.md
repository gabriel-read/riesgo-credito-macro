# Tareas — Spec 005 Estrés

Estado: **tareas aprobadas por el usuario el 12-oct-2026; ejecución en curso por Codex**.

Contrato: spec y plan v6 aprobados por el usuario el 12-oct-2026 en sus bytes exactos; revisión independiente ronda 4 APROBADA. Fuentes pre-registradas en `5ba4ada`; spec, plan y cuatro revisiones en `7a3dd2a`. Los encabezados «borrador» de los originales se conservan para no alterar las huellas aprobadas; esta nota registra la aprobación sin modificar esos originales. Ninguna observación opcional se incorpora mediante estas tareas.

Una tarea por vez, tests primero para código, luego implementación y `uv run pytest -q` antes de marcarla. Pruebas sin red; proyección con escenarios reales solo en T9. Tareas T1–T9: Codex. T10 distingue validación del autor de auditoría independiente de Claude. Cambios del contrato requieren `/sdd-change`; no nuevas dependencias, modificación de 003/004 ni escritura en `data/raw/`. Las tareas no autorizan nuevos commits ni push.

- [x] **T1. Parser y validación de fuentes congeladas.** RF-1, RF-2; RNF-8 · agente: codex
  - Tests: cabeceras/nombres exactos, 13 trimestres consecutivos y fila histórica 2025 Q4; errores con archivo/variable/trimestre ante faltantes o formato inesperado. Manifiesto UTF-8 con BOM y verificación de SHA-256 de los CSV originales, sin normalizar sus bytes.
  - Hecho cuando: `parse_fed_csv` puro pasa los casos sintéticos; validación de huellas/cobertura por E/S está separada. Las tres reglas exactas y las fuentes ya congeladas no se regeneran ni sobrescriben.
  - Evidencia (12-oct): tests primero fallaron por módulo ausente; 11 tests específicos en verde. Suite completa 785 passed, 355 warnings, 212.53 s; se corrigió antes la etiqueta de agente de T10 que detectó el guardarraíl. Fuentes y contratos intactos.

- [x] **T2. Niveles, enlace y transformaciones.** RF-3; RNF-3, RNF-8 · agente: codex
  - Tests a mano: composición `1.04**0.25`, interanuales logarítmicas con t−4, ΔU/Δtasa del primer paso contra Fed 2025 Q4, CPI con base 2025T4 de dos meses; error ante tasas ≤ −100, niveles no positivos o dato requerido ausente.
  - Hecho cuando: `to_levels`/`build_regressors` reproducen las identidades con historia sintética, reutilizan `panel.yoy` y funciones de agregación existentes; ruta de lectura del vintage 2026-10-02 valida nombres, fechas, filas, último dato y SHA normalizado a LF según plan §2. No cambia el panel guardado ni consume observados posteriores al origen aplicable.
  - Evidencia (12-oct): tests nuevos primero en rojo; 18 específicos en verde; suite completa 792 passed, 378 warnings, 186.16 s. Agregación CPI RF-11 y huellas del vintage verificadas sin escritura ni estimación de estrés.

- [x] **T3. Calendarios, escenario D y crédito.** RF-3, RF-12, RF-12c; RNF-3 · agente: codex
  - Tests: modos `adapted` (13), `post_2026q2` (11) y `from_2025q4` (13), con índices y referencias iniciales del plan; D modifica solo ΔFFR, siete cambios del episodio y seis ceros explícitos; crédito con rezago 4, cuatro pasos observados y nueve supuestos en principal.
  - Hecho cuando: base/severo/D tienen cobertura completa y las sensibilidades calendario/crédito quedan definidas sin rellenos implícitos; RF-12c conserva su límite observado de crédito hasta 2027T2 y supuesto desde 2027T3, independiente de su origen 2025T4.
  - Evidencia (12-oct): funciones nuevas primero en rojo; 23 tests específicos en verde; suite completa 797 passed, 378 warnings, 176.58 s. Sin proyección con escenarios reales.

- [x] **T4. Lectores JSON, diseño y adaptador dinámico.** RF-4, RF-5, RF-5b, RF-6; RNF-2 · agente: codex
  - Tests: mapas distintos de ambos JSON, orden y dimensiones, T/Q y `AAAA Qn`, `sample_end` común, dependiente diferenciada, nulos/dummies y rezagos; errores de contrato. Diseño histórico columna por columna frente a `build_design` y `build_design2` (`atol` 1e-12).
  - Hecho cuando: `read_model_contract`, `quarter_to_period`, `columns_to_design` y `project` reutilizan `forecast.dynamic`/`to_level` sin modificar 003/004; anclas ΔDR/DR correctas, X incluye todos los términos. La recursión sintética coincide con solución cerrada (`rtol` 1e-10, `atol` 1e-12). RF-5 reconstruye solo el ajuste predefinido 2000T1–2019T4 mediante `out_of_sample`, ancla 2021T4, tasa libre, y reproduce `result.series.dinamico` (`atol` 1e-12); no selecciona otro modelo ni reemplaza parámetros principales.
  - Evidencia (12-oct): tests primero en rojo, 31 específicos de escenarios/estrés en verde; suite completa 805 passed, 378 warnings, 171.63 s. Diseños históricos sintéticos de ambos modelos y equivalencia OOS acreditados.

- [x] **T5. Bloque HAC y réplicas pareadas.** RF-7, RF-8, RF-9; RNF-4 · agente: codex
  - Tests: bloque sin dummies simetrizado, Cholesky, error si no definido positivo, semilla/generador y orden del plan; N=200000 en el test estadístico sintético, media dentro de cuatro errores MC y ambas tolerancias de covarianza < 0.02.
  - Hecho cuando: `sym_block`/`draw_params` conservan la distribución marginal y el pareo; tasa cero después de extraer solo para principal, dummies cero; mismas réplicas entre escenarios/sensibilidades. Etiqueta «evidencia fuerte» detiene el proceso, sin escoger otra regla.
  - Evidencia (12-oct): tests primero en rojo; 200000 réplicas sintéticas recuperan media/covarianza con tolerancias aprobadas. Suite completa 807 passed, 378 warnings, 179.95 s.

- [x] **T6. Resúmenes de cambio y nivel, invariantes y límites.** RF-7, RF-8, RF-11; RNF-5 · agente: codex
  - Tests: puntual separado de mediana, percentiles lineales 5/50/95, pico con signo/empate al primero, sin aumento y mínimo, proporciones en final y pico puntual, comparación entre modelos sin banda; réplicas explosivas y niveles fuera de rango reportados sin descartar/truncar, error ante no finitos.
  - Hecho cuando: `summarize_delta` y resumen de niveles satisfacen el contrato; propiedades A/B con condiciones y tests negativos de RNF-5 se comprueban, sin asumir cancelación fuera del diseño aprobado.
  - Evidencia (12-oct): tests primero en rojo; 15 específicos de estrés en verde. Suite completa 812 passed, 387 warnings, 204.45 s; límites reportados sin truncamiento y condiciones de invariancia comprobadas con casos negativos.

- [x] **T7. Sensibilidades de tasa, calendario, crédito y origen.** RF-10, RF-12, RF-12c · agente: codex
  - Tests: C=Δ_sens−Δ_principal calculado por réplica y en los trimestres correctos; crédito modifica niveles, no Δ; D=severo con tasa cero; RF-12a es el recorte y RF-12c la trayectoria completa con origen 2025T4.
  - Hecho cuando: `rate_sensitivity`/`origin_comparison` producen valores y rótulos contratados; RF-12c compara por paso, incluye niveles contrafactuales y DR observado 2026T1–T2, y lanza error si Δ discrepa (`atol` 1e-9). No incluye estimador condicionado ni sensibilidad con límites del IC.
  - Evidencia (12-oct): tests primero en rojo, 18 específicos de estrés en verde; suite completa 815 passed, 387 warnings, 264.41 s. Contribución pareada y calendario completo por paso comprobados.

- [x] **T8. Tablas, figuras, variables y limitaciones.** RF-13 a RF-16; RNF-6, RNF-9 · agente: codex
  - Tests: ocho tablas del plan §6 en CSV/Markdown, dos figuras de dos paneles y claves `estres.*` completas del plan §5 (crédito por modelo/escenario); números desde cálculos, rótulos/fuentes en español, asociación y advertencias exigidas, sin cifras manuales.
  - Hecho cuando: renderizadores reciben resultados sintéticos y producen formato determinista, precisión y notas contratadas; `stress_origin` y las limitaciones de RF-14 están incluidas; escritura aislada en pipeline, sin cambios de otras claves del informe.
  - Evidencia (12-oct): tests de renderizadores primero en rojo; tres tests de salida sintética en verde. Suite completa 818 passed, 387 warnings, 235.03 s. CSV/MD, variables calculadas y PNG deterministas; integración de limitaciones reales en T9.

- [x] **T9. Integración de la etapa stress y ejecución real autorizada por las tareas.** RF-1 a RF-16; RNF-1, RNF-7, RNF-8 · agente: codex
  - Tests primero: integración en raíces temporales con fuentes congeladas, detección de archivo/huella/vintage inválido y preservación de archivos de entrada, outputs de 003/004 y bloques datos/modelo1/modelo2.
  - Hecho cuando: `stage_stress` reemplaza la etapa provisional; `all` integra stress sin red ni reestimación principal; N=10000 y semilla del plan, fuentes y contratos verificados antes de proyectar. Dos corridas temporales idénticas byte a byte y no regresión de 003/004; salidas reales completas y suite completa en verde. No se ejecuta T9 antes de aprobar estas tareas ni antes de T1–T8.
  - Evidencia (12-oct): tests de integración primero en rojo, doble corrida stress idéntica y entradas/otros modelos intactos; CLI stress ejecutada en copia activa. Suite final 823 passed, 503 warnings, 789.19 s; all ×2, rc 0, 79 archivos idénticos, 18 salidas stress iguales a las activas y 54 archivos de modelos sin cambio de contenido (texto normalizado a LF, PNG por bytes). Evidencia en docs/reproducibilidad-005-2026-10-12.json; correcciones de T9: warmup de crédito fuera de muestra, formato mixto, contexto de error Cholesky y concordancia de panel guardado.

- [x] **T10. Validación del autor y auditoría independiente final.** Criterios de finalización · agente: codex (validación del autor); auditor independiente: claude
  - Codex comprueba RF/RNF y salidas reales sin corregir durante la revisión; registra `review-validate.md`, autor y pruebas completas. Entrega a Claude solo rutas originales y criterios, con rondas previas conservadas. Tests verdes no equivalen a auditoría.
  - Hecho cuando: `review-validate.md` y `review-audit.md` APROBADOS, pre-registro anterior a T9, reproducibilidad y pruebas acreditadas. Claude realiza la auditoría independiente; si falta cuota, queda pendiente, con punto de continuidad. La spec crítica no se cierra hasta esa auditoría y autorización aplicable.
  - Completada el 12-oct por Codex conforme a la autorización condicional del autor: validación del autor ronda 3 APROBADA y auditoría independiente ronda 3 APROBADA. Se recalcularon las cuatro huellas de código/test/tablas y las de spec/plan, presentes íntegramente en review-audit.md y coincidentes con el paquete/registro vigente. Suite del autor 837 passed; no repetida porque los archivos siguen intactos. Auditoría: 837 passed, 567 warnings, 1040 s y stress reproducible (ya iniciadas antes del aviso de evitar repetición). Rondas 1/2 conservadas; opcionales sin aplicar. Evidencia: docs/reproducibilidad-005-ronda3-2026-10-12.json. T10 completa y 005 cerrada sin cambiar bytes de contratos aprobados ni hacer commit/push.

## Cobertura RF/RNF → tareas

| Requisito | Tareas |
|---|---|
| RF-1, RF-2 | T1, T9 |
| RF-3 | T2, T3 |
| RF-4, RF-5, RF-5b, RF-6 | T4 |
| RF-7, RF-8 | T5, T6 |
| RF-9 | T5 |
| RF-10 | T7 |
| RF-11 | T6 |
| RF-12, RF-12c | T3, T7 |
| RF-13 a RF-16 | T8, T9 |
| RNF-1 | commits 5ba4ada → 7a3dd2a, T9, T10 |
| RNF-2 | T4 |
| RNF-3 | T2, T3 |
| RNF-4 | T5 |
| RNF-5 | T6, T7 |
| RNF-6, RNF-9 | T8 |
| RNF-7 | T8, T9 |
| RNF-8 | T1–T9 |

Si una tarea resulta demasiado grande, detenerse y proponer subdivisión antes de ejecutarla; no ampliar requisitos ni relajar tolerancias. Las casillas se marcan solo con evidencia de finalización.
