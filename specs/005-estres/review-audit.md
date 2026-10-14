VEREDICTO: APROBADO

Auditoría independiente de implementación de la spec 005 (Estrés), **ronda 3 acotada**, 12-oct-2026. Autor: subagente `revisor-econometrico` de Claude Code (contexto limpio), con solo rutas y criterios; no leyó `review-validate.md`, `MEMORY.md`, `docs/relevo-*` ni `.env`, y no modificó el repositorio. Claude Code solo registra el informe tal cual lo entregó. Las rondas anteriores se conservan en `review-audit-ronda1.md` (sha256 `44df57df…`, CAMBIOS NECESARIOS) y `review-audit-ronda2.md` (sha256 `e753a000…`, CAMBIOS NECESARIOS). Este veredicto no cierra por sí solo la 005: T10 y el cierre formal los hace Codex y los aprueba el autor.

**Huellas auditadas** (verificadas por el revisor y recalculadas por Claude Code al guardar el informe; coinciden):
- `specs/005-estres/spec.md` `6d9713dd1917b4b9b5a2ffc87c7f202869981e9102c9e8e11bf60daac99c77bb`
- `specs/005-estres/plan.md` `8b0fc56b3ba2577a0c142a8ab70568af96caed9bf2bbcf18949f42c8ad3d232a`
- `src/stress_tables.py` `2e4e91f1174dd9a2f341564c7013d3ea8bedc438e020ee7dcaae148dfca81b7e`
- `tests/test_stress_outputs.py` `4f2cd5dd553bf625d2de4a6647dad78b952203d9d0aa54888749623403b0ad64` (test `test_halfway_rounding_matches_cells_variables_and_both_footnotes`)
- `outputs/tables/stress_levels.md` `fda1b19d244cdb8b41cdb7ce3191b32d14c2a9394f8f67c717045c16ed23616a`
- `outputs/tables/stress_delta.md` `5eb869064970fe3d110c0b4e02aae65d069a0fdc7bcbad535db6cb8bb7f2f4ce`
- Registro `docs/reproducibilidad-005-ronda3-2026-10-12.json`: sus 196 huellas coinciden con el cálculo del revisor.

---

El bloqueante de la ronda 2 está corregido. El cambio de producción son exactamente las tres conversiones a `float` del pie. Solo cambiaron `stress_levels.md` y `stress_delta.md`, y en cada uno solo el texto «(proporción 0,010)», que ahora dice «(proporción 0,011)». Ninguna cifra cambió y la etapa es reproducible byte a byte.

## Puntos 1 a 5

| # | Punto | Resultado | Evidencia |
|---|---|---|---|
| 1 | Redondeo del pie frente a celdas y variables | **Correcto en ambos modelos** | Pie en `src/stress_tables.py:84-88`. Los pies de `stress_levels.md:82` y `stress_delta.md:56`, la columna `*_modelo` del Markdown (un único valor por modelo en las 78 filas) y `report/_variables.yml:1125-1129` y `:1167-1171` dan lo mismo. **Modelo I:** n 105, proporción 0,011, mínimo −10,323, máximo 6,497. **Modelo II:** n 160, proporción 0,016, mínimo −6,120, máximo 9,921. El CSV conserva la precisión completa (`stress_levels.csv:2`: `105,0.0105,-10.32345982377362,6.496806150017813`). Comprobado con un parser propio. |
| 2 | El test con 0,0105 ejerce producción y detecta el defecto | **Sí** | `tests/test_stress_outputs.py:55-74` llama a `render_stress_tables` y a `stress_variables` de producción; en la copia, `src` se resolvía a la copia mutada. Mutaciones en el scratchpad: quitar `float` en la proporción (el defecto original) hace **fallar** el test en `:72`; quitarlo en el mínimo, falla en `:73`; quitarlo en los tres, falla. Sin mutación pasan los 7 tests. El test nuevo se añadió sin tocar el resto del archivo: al quitar las líneas 55-76 se obtiene exactamente la huella de la ronda 2 (`3c291906…`). |
| 3 | Contra la ronda 2 solo cambió lo previsto y las cifras siguen iguales | **Sí** | De las 131 huellas de la ronda 2 cambiaron solo 4: `stress_levels.md`, `stress_delta.md`, `src/stress_tables.py` y `tests/test_stress_outputs.py`. Los dos PNG, todos los CSV, las demás tablas Markdown, `_variables.yml` (`305f11e3…`), los datos y los modelos 003/004 están intactos. Al reconstruir, (a) el `stress_tables.py` actual sin los tres `float()` da exactamente `16a9f910…` y (b) los dos Markdown con «0,011» → «0,010» dan exactamente las huellas de la ronda 2. En las variables: Δ final 1,428 / 0,827; picos de Δ 1,898 / 1,286, ambos en 2028T3; `dif_modelos.delta_pico` 0,612; fuera de rango 105 / 160, con mínimos −10,323 / −6,120; RF-12c (`sens_origen.*.severo.delta_k13`) 1,428 / 0,827, iguales al ejercicio principal; D (propio) = adverso en todas las claves de ambos modelos con la tasa en 0. |
| 4 | pytest y reproducibilidad de la etapa stress | **Correcto** | `uv run pytest -q -p no:cacheprovider`: **837 passed**, 567 warnings, 1040 s, rc 0 (la suite completa ya corría cuando llegó el ajuste del coordinador). El test específico más el archivo: 7 passed. `uv run python -m src.pipeline stress` terminó con rc 0 en 5 min 15 s. En la instantánea de 240 archivos (`outputs/`, `data/`, `report/`, `specs/`, `src/`, `tests/`, `docs/`, `research/`, `pyproject.toml`, `uv.lock`, `.gitattributes`) no hubo ningún archivo añadido, eliminado ni cambiado antes y después de la etapa stress, ni después de pytest. Nada que restaurar. |
| 5 | Regresiones introducidas en `src/stress_tables.py` | **Ninguna** | El diff se reduce a envolver tres argumentos en `float(...)` en `:86-88`, con el mismo criterio que celdas (`:63`) y variables (`:35`). La rama solo se ejecuta si n > 0. Si el valor fuera NaN, `float(nan)` sigue dando «—» vía `fmt_es` (`src/tables.py:14`), igual que antes. Los demás tests de estrés (`test_stress.py`, `test_stress_audit.py`, `test_frozen_stress.py`) no cambiaron de huella. |

## Hallazgos bloqueantes
Ninguno.

## Opcionales (no bloquean)
1. **El máximo de prueba no discrimina el redondeo.** `tests/test_stress_outputs.py:61`: el valor 100,0105 se redondea igual con NumPy y con Python (100,010). Por eso la mutación que quita `float` solo en el máximo pasa los 7 tests. La proporción (el defecto real) y el mínimo sí quedan protegidos, y los máximos reales (6,497 y 9,921) no caen en un caso de mitad. Si se quiere cerrar el hueco, basta usar un valor que separe ambos redondeos.
2. Las observaciones opcionales de las rondas 1 y 2 siguen abiertas. No se exigen.

## Checklist de econometría aplicable a este alcance
- **Reproducibilidad:** comprobada, idéntica byte a byte.
- **Frases causales:** sin cambios de texto, salvo la proporción.
- **Coincidencia entre tablas, variables y pies:** comprobada en ambos modelos.
- **Estacionariedad, HAC, rezagos y signos:** heredados sin cambios; ningún archivo de modelos ni de estrés cambió de huella fuera de los cuatro previstos.

## Lo que defendería ante el profesor
- La misma proporción (105 de 10 000 = 0,011) aparece idéntica en la celda, en las dos notas al pie y en `_variables.yml`, todas con un solo criterio de redondeo.
- La corrección es mínima: tres conversiones de tipo y un test que falla si se reintroduce el defecto. Ninguna cifra, figura ni variable cambió.
- La etapa de estrés es reproducible byte a byte y la suite completa pasa (837 tests).

## Lo que me preguntaría el profesor
1. Si 105 y 160 de 10 000 réplicas dan niveles negativos de hasta −10 pp, ¿por qué es aceptable reportar niveles en vez de solo cambios, y cómo se lo explica al lector?
2. La banda del cambio final cruza cero en ambos modelos (p05 −0,188 y −0,479). ¿Qué tan fuerte es entonces la afirmación de que la morosidad sube bajo el adverso?
3. Si se quitan los dos primeros trimestres del calendario de la Fed (RF-12a), Δ cae a 0,340 y 0,048. ¿El resultado depende de que el choque empiece de inmediato?

## Nota de registro (Claude Code)
Independencia: el informe lo produjo un revisor de contexto limpio; Codex no participó en la auditoría y no se le atribuye. Las observaciones transversales de la ronda 1 (opcionales) que afectan a la sección 7 del informe de la spec 006 se trasladaron a su spec. Esta aprobación cubre la implementación y salidas de la 005 en las huellas listadas; cualquier cambio posterior invalida el veredicto para esos archivos.
