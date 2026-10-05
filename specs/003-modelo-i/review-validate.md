VEREDICTO: APROBADO

# Validación técnica — Spec 003 Modelo I (tras las rondas 1 a 3 de auditoría)

**Fecha:** 2026-10-05
**Quién la escribe y por qué:** Claude Code. OpenCode agotó su cuota gratuita en mitad de la fábrica (hizo la corrección 1 y dejó la 2 a medias) y `AGENTS.md` prevé que entonces Claude Code complete la tarea. Claude Code aplicó las correcciones 2 a 7 y ejecutó esta validación: es el mismo agente, así que **esta validación no sustituye a la auditoría independiente**, que queda pendiente para el cierre (segunda ronda de `review-audit.md`).

Este informe valida lo técnico: tests, reproducibilidad y que cada corrección figure en las salidas regeneradas. No juzga la econometría.

## 1. Tests

| Comprobación | Resultado |
|---|---|
| `uv run pytest -q` (sin red, bloqueada por `conftest.py`) | **504 passed**, 0 failed |
| Tests nuevos o cambiados en esta ronda | `tests/test_model1.py`, `tests/test_outputs_model1.py`, `tests/test_diagnostics.py` (tests escritos antes que el código y vistos en rojo) |

## 2. Reproducibilidad (RNF-5, criterio de finalización)

| Comprobación | Resultado |
|---|---|
| `uv run python -m src.pipeline all`, primera corrida | código 0 (`data`, `models`; `stress` y `report` siguen pendientes de sus specs) |
| Segunda corrida seguida | código 0 |
| SHA-256 de los 30 archivos de `outputs/`, `data/processed/` y `report/` entre las dos corridas | **idénticos byte a byte** |
| `git diff --exit-code outputs/ report/_variables.yml`, con la salida de la primera corrida en el índice | **código 0** |

## 3. Correcciones de `review-audit.md`

| # | Corrección | Evidencia en las salidas regeneradas |
|---|---|---|
| 1 | Chow sin atenuante (hecha por OpenCode) | `model1_limitations.md` no contiene «sobredimensionado» ni «contraste estructural»; el rechazo figura con su estadístico y p |
| 2 | Pie de la tabla de efectos | `model1_effects.md` termina con «Nota:» con las DE (ΔPIB 1,778; ΔU 0,308; π 1,637; ΔFFR 0,452; CRED(t−4) 4,114), «sobre 102 trimestres, 2000T1–2026T2 sin 2020T2–2021T1», y la lectura del largo plazo con Y en primera diferencia. Las DE salen del código. `_variables.yml` trae `efectos_nota` y `efectos.<regresor>.de` |
| 3 | `terminos_diferencia` en R4, R6 y R7 | «sustituye: gdpc1_yoy → gdp_yoy», «sustituye: CRED(t−4) → CRED(t−8)» y «sustituye: CRED(t−4) → CRED(t−12)». `model1_robustness_summary.md` cierra con una nota que define el criterio y avisa de que en R4, R6 y R7 el regresor es distinto |
| 4 | Texto del VIF de ΔU | Explica el salto de 2020T2 absorbido por su dummy y la identificación con la variación fuera de la COVID; ya no dice «posible multicolinealidad» (el texto genérico se conserva para otros regresores). Sin cifras nuevas |
| 5 | Fuera de muestra con 3 decimales | Tabla y variables muestran las mismas cifras: RMSE a un paso 0,033 frente a 0,034; cociente 0,978; dinámico 0,276 frente a 0,170; cociente 1,625; DM −0,080, p = 0,937. Un test comprueba que cada cifra de las variables aparece igual en la tabla. Enmienda de D12 en el plan (`a4e1d86`) |
| 6 | Etiqueta de R2 | «DRALACBN sin desestacionalizar, con dummies estacionales» |
| 7 | Formato AAAAT# de los Chow | «Chow 2008T3» y «Chow 2020T2»; las claves técnicas siguen siendo `chow_2008t3` y `chow_2020t2` |

Estado de las variantes sobre la historia congelada: R1 estimada (98 observaciones); R6 desde 2001T1 (102) y R7 desde 2002T1 (98); R8 «no estimada» (sin historia anterior a 2000T1), como prevé la spec.

## 4. Criterios de finalización de la spec

- [x] Spec aprobada y commiteada antes de la primera estimación: commit `667b313`; los cambios C1–C3 son anteriores a los datos reales.
- [x] Existen las salidas de RF-8 a RF-21: 9 tablas (`.csv` y `.md`), 3 figuras, el JSON para la spec 005 y el bloque `modelo1:` (24 claves) en `report/_variables.yml`.
- [x] R6 y R7 estimadas con su inicio efectivo; R8 «no estimada» con su motivo.
- [x] `uv run python -m src.pipeline all` reproduce todo y dos corridas no dejan diferencias.
- [x] `uv run pytest -q` en verde, sin red.
- [x] `review-validate.md` con `VEREDICTO: APROBADO` (este archivo).
- [ ] `review-audit.md` con `VEREDICTO: APROBADO`: **pendiente**. La ronda 1 dio `CAMBIOS NECESARIOS`; falta la ronda 2 tras estas correcciones.

## 5. Observaciones que no bloquean

1. **El PNG de la spec 001 no coincidía en bytes con el comiteado (resuelto: se comitea aparte).** `outputs/figures/delinquency_unemployment_ffr.png` (128 314 bytes comiteados, 134 153 regenerados) se reescribe distinto con el entorno actual; es estable entre corridas pero no frente al commit. Las CSV de la 001 (`panel.csv`, `descriptives.csv`, `stationarity.csv`) sí son idénticas byte a byte a las comiteadas. Para que `git diff --exit-code outputs/` pase en este entorno se comitea el PNG regenerado en un commit propio (`chore(001)`). Es un asunto de la spec 001, no del modelo, y puede cambiar en otra máquina.
2. **`git status` marca como modificadas tres CSV de la 001 que son idénticas** a las comiteadas (se verificó con `cmp` contra `git show HEAD:`). Es un efecto de `core.autocrlf=true` en Windows, no un cambio real.
3. **Alcance de esta validación:** un solo entorno (Windows, Python 3.11, statsmodels 0.15). No se probó en CI ni en otro sistema operativo.
4. **Opcionales de `review-audit.md` no aplicados** (no bloquean y son prosa o presentación): mostrar «—» en p e IC de las dummies COVID, marcar el hueco de 2020T2–2021T1 en el gráfico CUSUM, dibujar el ingenuo constante en el gráfico fuera de muestra, «≥ 0,10» y «< 0,001» en la tabla de estacionariedad y renombrar «ΔPIB».

## 6. Ronda 2 de auditoría (`review-audit.md`): menores resueltos

| # | Observación | Resuelto |
|---|---|---|
| 1 | Faltaba la nota de tamaño del Chow 2020T2 que pre-registra el plan | `chow_wald` devuelve `n_post` y `n_post_util`; la nota del Chow 2020T2 dice «quedan 21 trimestres posteriores útiles para 7 restricciones: el tamaño empírico del contraste puede diferir del 5 % nominal». El 21 lo calcula el código (25 posteriores menos 4 que absorben las dummies de impulso). El Chow 2008T3 no lleva esa nota y el veredicto sigue a p. 6 tests nuevos |
| 2 | El plan no recogía las claves y la columna nuevas | `plan.md` §4 y nueva §13 («Enmiendas posteriores a la aprobación»): `efectos.<macro>.de`, `efectos_nota`, `variantes_muestra.<id>.motivo`, columna `de` y notas de pie |
| 3 | Sin commitear y Python 3.11 frente a 3.12 | `AGENTS.md` pasa a Python 3.11 (el de `.python-version` y el del entorno). Los commits se hacen a continuación: primero el PNG de la 001 y luego el resto |

Reproducibilidad repetida tras estos cambios: dos corridas de `uv run python -m src.pipeline all` dejan los 30 archivos idénticos byte a byte y `git diff --exit-code outputs/ report/_variables.yml` da código 0.

## 7. Ronda 3 de auditoría (`review-audit.md`): menor resuelto y opcional repetido

| # | Observación | Resuelto |
|---|---|---|
| 1 | El pie de R1 no decía que los rezagos de 2022 salen de trimestres excluidos | `_variant_note` añade, cuando hay exclusión, una frase con los trimestres calculados por código. En R1: «Y(t−1) de 2022T1 y CRED(t−4) de 2022T1–2022T4 se toman de trimestres excluidos (historia transformada)». Se escribe en las 5 filas de R1 del `.md` y del `.csv`. 6 tests nuevos, incluidos casos con otra exclusión y otro rezago de crédito |
| Opc. | Formato de p en `model1_stationarity.md` | ADF «< 0,001» y KPSS «≥ 0,10» o «≤ 0,01» (el recorte de statsmodels, `fmt_kpss_p`), solo en el Markdown; `model1_stationarity.csv` conserva los valores. 5 tests nuevos, incluido que el CSV no cambia |
| Plan | La §12 daba por incorporada la nota de R1 | `plan.md` §13, enmienda 4 |

**Reproducibilidad y árbol de trabajo, repetidos tras estos cambios.** Con todo el contenido del commit preparado en el índice:
- `uv run pytest -q`: **504 passed**, sin red.
- Dos corridas seguidas de `uv run python -m src.pipeline all` (código 0 las dos): los 30 archivos de `outputs/`, `data/processed/` y `report/` son **idénticos byte a byte**.
- `git diff --exit-code`, sobre todo el repositorio, da código 0, y `git status --porcelain` no muestra ninguna línea sin preparar (ni modificados ni sin seguimiento). Es la comprobación equivalente a un árbol limpio tras el commit.

El cierre de la spec sigue condicionado a una cuarta ronda de auditoría independiente con `VEREDICTO: APROBADO`.

