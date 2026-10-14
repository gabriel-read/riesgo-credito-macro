VEREDICTO: CAMBIOS NECESARIOS

Auditoría independiente de implementación de la spec 005 (Estrés), **ronda 2**, 12-oct-2026. Autor: subagente `revisor-econometrico` de Claude Code (contexto limpio, otra instancia que la ronda 1), con solo rutas y criterios; no leyó `review-validate.md`, `MEMORY.md`, `docs/relevo-*` ni `.env`, y no modificó el repositorio. Claude Code solo registra el informe tal cual lo entregó. La ronda 1 se conserva intacta en `review-audit-ronda1.md` (sha256 `44df57df…`). T10 y la spec 005 siguen abiertas: queda un bloqueante.

Resumen: los cinco bloqueantes de la ronda 1 están corregidos (el b, de forma parcial). Las cifras no cambiaron, salvo `dif_modelos.delta_pico`, que el bloqueante 3 obligaba a cambiar. La etapa es reproducible byte a byte y la suite pasa (836 passed). Bloquea un solo defecto nuevo, introducido por la corrección del bloqueante 2: el pie de las tablas da una proporción distinta de la de la propia tabla y de `_variables.yml`.

## Comprobaciones hechas

- **Contratos intactos.** sha256 de `spec.md` (6d9713dd…77bb) y `plan.md` (8b0fc56b…232a) coinciden con las aprobadas.
- **Registro de huellas.** Las 103 huellas protegidas, las 18 de salidas de estrés, las de código, las de tests y la de `_variables.yml` que lista `docs/reproducibilidad-005-ronda2-2026-10-12.json` coinciden con el cálculo propio.
- **Qué cambió desde la ronda 1** (contra `docs/reproducibilidad-005-2026-10-12.json`): solo `src/stress.py` y `src/stress_tables.py`; `scenarios.py`, `stress_figures.py` y `pipeline.py` idénticos. Salidas cambiadas: `stress_delta.md`, `stress_levels.{csv,md}`, `stress_limitations.md`, `stress_origin.{csv,md}` y `_variables.yml`. Idénticas byte a byte: los dos PNG, `stress_delta.csv`, `stress_models.*`, `stress_paths.*`, `stress_rate_sensitivity.*`, `stress_sensitivity.*` y `stress_limitations.csv`.
- **Tests.** `uv run pytest -q`: 836 passed, 567 warnings, 927 s, rc 0.
- **Reproducibilidad (RNF-7).** Dos corridas de `uv run python -m src.pipeline stress`; los 203 archivos (`outputs/`, `data/`, `report/`, specs 003/004/005, `src/`, `tests/`) idénticos antes y después, también tras pytest. Nada que restaurar.
- **Mutaciones.** Sobre una copia en el scratchpad, nunca en el repositorio: inyectó el defecto original en cada caso y corrió los tests correspondientes.

## Los cinco bloqueantes de la ronda 1

| # | Bloqueante | Estado | Evidencia |
|---|---|---|---|
| a | Claves `estres.*` con prefijo `delta_` y test del árbol completo | **Resuelto** | `src/stress.py:384-389` escribe los nueve `delta_*`. `tests/test_stress_audit.py:35-65` transcribe el plan §5 y compara por igualdad exacta de conjuntos en cada nivel; `tests/test_frozen_stress.py:89-92` lo hace sobre el YAML real. Volver a `"min"` hace fallar el test (mutación M1). `_variables.yml` coincide con el plan §5, con las 24 hojas renombradas. |
| b | Advertencia de niveles fuera de rango en el pie; n, proporción, mínimo y máximo en `stress_levels` | **Parcial** | Columnas: `src/stress.py:374-380` (por escenario) y `410-421` (por modelo, unión de réplicas). Pie en `src/stress_tables.py:78-88`, en `stress_levels.md` y `stress_delta.md`. Tests `test_stress_outputs.py:40-52` y `test_stress_audit.py:68-86` detectan M5 (quitar el pie) y M6 (quitar mínimo y máximo). La proporción del pie sale mal redondeada (hallazgo nuevo 1). |
| c | `dif_modelos.delta_pico` = Δ_I,pico − Δ_II,pico | **Resuelto** | `src/stress.py:488-490`. Vale 0,612 (= 1,898 − 1,286); el máximo de la diferencia trimestral, 0,626, queda solo como serie en `stress_models.csv`. `test_stress_audit.py:89-101` lo distingue y detecta M2. |
| d | Markdown válido y encabezados en español | **Resuelto** | `src/stress_tables.py:69-75` escapa `\|` en el Markdown y conserva el texto literal en el CSV. `src/stress.py:282-283` usa `trimestre_adaptado` y `trimestre_original`. Las ocho tablas `.md` tienen ancho uniforme en todas sus filas (script propio) y encabezados en español. Tests `test_stress_outputs.py:63-73` y `test_stress_audit.py:104-111` detectan M3 y M4. |
| e | Negativos RNF-5 y test de lenguaje | **Resuelto** | Oráculo de δ independiente en `tests/test_stress.py:118-127`. Negativo de referencia del paso 1 distinta, ambos modelos, en `:232-265`. Negativo de Y en logit, ambos modelos, en `:268-288`. Los negativos anteriores (`:163-229`) comparan ahora contra el oráculo. Test de lenguaje sobre las ocho tablas en dos formatos y sobre el árbol `estres`: `test_stress_audit.py:114-121`, `test_frozen_stress.py:79-86`; detecta M7 (inyectar «debido a»). |

## Hallazgo bloqueante nuevo

1. **El pie de las tablas contradice a la propia tabla y a `_variables.yml` en la proporción de réplicas fuera de rango del Modelo I.** `src/stress_tables.py:86`; aparece en `outputs/tables/stress_levels.md` y `outputs/tables/stress_delta.md`.
   - **Problema:** el pie dice «105 réplicas (proporción 0,010)»; la celda `prop_replicas_fuera_rango_modelo` de la misma tabla y `estres.modelo1.fuera_rango.prop` dicen 0,011. El valor exacto es 0,0105 (105 de 10 000).
   - **Causa confirmada:** `group.iloc[0]` devuelve un `np.float64` y `fmt_es` aplica `round()`; sobre `np.float64` es el de NumPy (0,010), mientras que celdas y variables pasan antes por `float(...)` y usan el `round` de Python (0,011).
   - **Por qué importa:** es el elemento que corregía el bloqueante 2; rompe el principio 5 de la constitución (cada cifra sale de una sola fuente) y la regla de que tablas y variables coincidan. Dos cifras distintas para la misma cantidad en la misma tabla.
   - **Esperado:** convertir a `float` antes de formatear en `src/stress_tables.py:85-88` (proporción y, por coherencia, mínimo y máximo); añadir un test con un valor justo en la mitad (por ejemplo 0,0105) que exija que el pie coincida con `stress_variables` y con la celda; regenerar. Solo deberían cambiar `stress_levels.md` y `stress_delta.md`.

## Regresiones

Ninguna en las cifras. Se mantienen respecto de la ronda 1:

- Δ final 1,428 (p05 −0,188 / p95 2,288) en el Modelo I y 0,827 (−0,479 / 1,721) en el II; picos 1,898 y 1,286, ambos en 2028T3; proporciones de Δ > 0: 0,935 / 0,951 y 0,877 / 0,934.
- Niveles base final / adverso final / pico adverso: 1,989 / 3,417 / 3,716 y 1,845 / 2,672 / 3,052.
- Contribución de la tasa C: 0,341 y 0,464 en el adverso; −0,681 y −0,922 en D.
- RF-12a: 0,340 / 1,736 / 0,843 y 0,048 / 1,118 / 0,549. `delta_k13` (RF-12c): 1,428 y 0,827, iguales al principal; diferencia máxima entre orígenes < 1e-9.
- D coincide con el adverso bajo la regla de la tasa. Explosivas: 1 y 1. Fuera de rango: 105 y 160 réplicas (unión entre escenarios, no suma; la suma serían 213 y 327); mínimo −10,323 y −6,120, máximo 6,497 y 9,921.
- Los bloques `datos`, `modelo1` y `modelo2` de `_variables.yml` siguen intactos: el diff contra HEAD solo añade 200 líneas del bloque `estres`. Sin lenguaje causal en las tablas `stress_*`, el bloque `estres` ni las cadenas del código de estrés.

## Opcionales (no bloquean)

- **Los tests no protegen la unión por modelo.** La mutación M8 (sumar los conteos de los escenarios en vez de unir réplicas) pasa los 11 tests; `test_stress_audit.py:79-86` solo compara la tabla con variables que salen del mismo valor. El código actual sí hace la unión (`src/stress.py:410-414`). Convendría un test sintético con réplicas solapadas entre escenarios.
- **Las salidas reales no comprueban el pie.** `test_frozen_stress.py:52-56` no verifica que la advertencia aparezca en el `stress_levels.md` real.
- **El negativo de logit es solo una demostración matemática.** Retransforma fuera del código de producción (`tests/test_stress.py:284-288`); aceptable según RNF-5, pero solo su primera aserción ejercita el código.
- **Falta el negativo de «historial distinto» en el Modelo II.** Solo existe para el Modelo I, vía el ancla ΔDR (`test_stress.py:229`).
- Las nueve observaciones opcionales de la ronda 1 siguen abiertas; no se exigen.

## Checklist de econometría de series de tiempo

| Punto | Resultado |
|---|---|
| Estacionariedad | Heredada de 003/004, sin cambios; la limitación «regresores no I(0)» no cambió. |
| Errores HAC | Las réplicas usan el bloque HAC sin dummies (`src/stress.py:167-183`), sin cambios. |
| Rezagos | K = 1 por BIC, sin reabrir. |
| Signos | Regla de la tasa en 0 mantenida; sensibilidad aparte, rotulada «sensibilidad, no efecto estimado». |
| Frases causales | Ninguna (barrido propio y tests nuevos). |
| Diagnósticos fallidos | Listados en `stress_limitations` (BP, White, JB, RESET y Chow). |
| Reproducibilidad | Idéntica byte a byte en dos corridas, 203 archivos sin cambios. |

## Lo que defendería ante el profesor

- Los cinco defectos de la ronda 1 se corrigieron sin tocar spec, plan, fuentes ni cifras, salvo la diferencia entre picos, que ahora mide lo que dice su nombre (0,612 pp).
- Cada test nuevo falla si se reintroduce su defecto (mutaciones sobre una copia).
- Bajo el adverso adaptado la morosidad proyectada sube frente a la base: picos de 1,90 y 1,29 pp en 2028T3; asociación condicional, banda solo de parámetros, invariante al origen (RF-12c).

## Lo que preguntaría el profesor

1. ¿Por qué la tabla dice 0,011 y su nota 0,010 para la misma proporción? ¿Qué garantiza que el informe cite una sola fuente?
2. Los niveles fuera de rango aparecen en 105 y 160 de 10 000 réplicas, con mínimos de hasta −10 pp. ¿Se cuentan como unión de los tres escenarios? ¿Qué dice eso de usar niveles, y no cambios, para planificar capital?
3. La banda del cambio final cruza cero en ambos modelos y el cambio cae casi a cero si se quitan los dos primeros trimestres de la Fed (RF-12a): ¿depende el resultado de que el choque empiece de inmediato?

## Continuidad

Una ronda 3 puede limitarse a dos cosas: (1) la corrección del hallazgo bloqueante 1 con su test; (2) la verificación de que solo `stress_levels.md` y `stress_delta.md` cambian de huella y el resto queda idéntico al inventario de esta ronda. Antes de reemplazar este archivo se conservará como `review-audit-ronda2.md`. T10 y la spec 005 siguen abiertas. Scripts de comprobación y copia mutada del revisor: scratchpad de la sesión (`mutate.py`, `mdcheck.py`, `hashes_*.txt`, `pytest.log`).
