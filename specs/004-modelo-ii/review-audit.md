VEREDICTO: APROBADO

Auditoría independiente, **ronda 2**, de la spec 004 (Modelo II). Autor: subagente `revisor-econometrico` de Claude Code, lanzado el 11-oct-2026 sobre HEAD `2f4c401` con solo rutas y criterios originales (sin conclusiones del implementador ni del validador). La ronda 1 (CAMBIOS NECESARIOS) se conserva intacta en `review-audit-ronda1.md`. Informe copiado tal cual lo entregó el subagente.

**En corto:** los dos cambios que pidió la ronda 1 están corregidos en el código, en el JSON, en las tablas y en los tests, y no encontré ningún problema nuevo que bloquee el cierre. Lo comprobé recalculando, sin fiarme de `review-validate.md`. El pre-registro se respetó, la aritmética cuadra con el JSON hasta la precisión de máquina y el pipeline da exactamente los mismos bytes en dos corridas y frente a lo commiteado. No modificó nada del repositorio.

## Qué comprobé y cómo

**Correcciones de la ronda 1 (commit `b2cd4f4`)**
- **Punto 1, `columns.y_lag`:** `src/model2.py:766` exporta ahora `dralacbs_d`. Reconstruí el modelo desde fuera usando solo el contrato del JSON: tomé cada `columns[t].column` del panel real, lo desplacé su `lag` y añadí la constante y las dummies. Ajusté MCO con HAC (Bartlett, 4 rezagos, sin corrección) sobre 2000T2–2026T2:
  - n = 105, ningún faltante;
  - coeficientes iguales a `params` (diferencia 0,0);
  - covarianza igual a `cov_hac` (diferencia máxima 6,5e-19);
  - `dralacbs_d` coincide exactamente con la diferencia de `dralacbs`.
  - Con el nivel (el error de la ronda 1), ΔDR(t−1) en 2026T2 habría valido 1,45 en lugar de −0,01.
  - Hay tres tests nuevos: dos con datos sintéticos que comparan término a término con la matriz del diseño, y uno sobre el panel real que comprueba que las columnas existen.
- **Punto 2, notación con K = 1:** `src/model2.py:246-269` añade funciones que separan K = 1 de K ≥ 2. Busqué en `outputs/` y en `_variables.yml` las formas rotas («θ0+…+θ1», «θ1..θ1», «= … = θ1», «t..t−1»): no queda ninguna. Las tablas regeneradas dicen «θ0 + θ1», «θ1», «Granger: θ1 = 0» y «ΔFFR(t) y ΔFFR(t−1)». `tests/test_model2_notation.py` cubre K = 1 de punta a punta y K ≥ 2.
- **Alcance del cambio:** el diff de `b2cd4f4` solo toca etiquetas y esa clave del JSON. Ninguna cifra cambió.

**Pre-registro**
- `ec983d0` (spec), `45c43d5` (cambio C1) y `7f732ce` (plan) solo tocan `specs/` y `MEMORY.md`, y son anteriores a la primera salida real (`7325ff2`, 15:07).
- `git diff 7f732ce HEAD` sobre `spec.md` y `plan.md` está vacío.

**Aritmética contra el JSON** (las seis cifras coinciden)

| Cantidad | Valor | Cómo |
|---|---|---|
| S = θ0 + θ1 | −0,04823; EE 0,03765; χ² 1,641; p 0,200 | combinación lineal de `params` y `cov_hac` |
| S_rez = θ1 | 0,03576; EE 0,03863; χ² 0,857; p 0,355 | igual; con K = 1 es el mismo Wald que Granger |
| ψ_h y R(h) | diferencia 0,0 con el JSON | recursión rehecha a mano |
| R(12) | −0,1594 (S/(1−ρ) = −0,1605) | respuesta acumulada a 12 trimestres |
| BIC − AIC | 31,85 = 12·(ln 105 − 2) | tabla de selección |
| Breusch-Godfrey(4) | 3,409 (p 0,492) | recalculado |

Otros recuentos que también cuadran: 36 trimestres de tasa cero; ventana HAC de 4 en la principal y de 3 en R2 y R3; max(fórmula, h+1) en las proyecciones locales; trimestres útiles del Chow 33/68 y 80/21.

**Coherencia entre archivos:** las cifras de las proyecciones locales, los coeficientes, los efectos, Granger, la lectura y los diagnósticos de `_variables.yml` coinciden con los CSV (0 discrepancias). Las tres figuras cuadran con sus tablas.

**Checklist de la skill**
- **Estacionariedad:** hay una fila por término. La forma fija de π y CRED(t−4), que no son I(0), está pre-registrada y declarada como desviación y como limitación.
- **HAC:** todo con HAC y la ventana declarada.
- **Selección de K:** AIC y BIC sobre la misma M (105 observaciones en los 8 modelos).
- **Signos:** H1 sale «no» y se reporta tal cual.
- **Lenguaje:** ninguna frase causal (grep en tablas, JSON y variables).
- **Diagnósticos fallidos:** BP, White, JB, RESET y Chow 2020T2 figuran como limitaciones; falta escribir su discusión (observación 3).
- **Reproducibilidad:** ver abajo.

**Reproducibilidad y tests**
- `uv run pytest -q`: **774 passed**, rc 0, en 5 min 31 s. El total incluye `tests/test_codex_harness.py`, que está sin seguimiento en git y no es de la 004.
- `src.pipeline all` dos veces en directorios temporales (`PIPELINE_ROOT`), con rc 0 en ambas: las dos corridas son idénticas y todos los archivos de `outputs/` y `_variables.yml` son idénticos byte a byte a los del repositorio.
- `git status` no cambió por el trabajo del auditor. Durante la sesión aparecieron archivos sin seguimiento de otro proceso: `specs/005-estres/` (borrador de Claude Code, esta sesión), `docs/secuencia-sdd-006-007.md` (ídem) y `docs/insumos-005-006-2026-10-11.md` (no es de esta sesión).

## Cambios necesarios

Ninguno bloqueante.

## Observaciones no bloqueantes (por gravedad)

1. **Importante, para la spec 005 (contrato del JSON):**
   - **Rango de la covarianza:** `cov_hac` tiene rango 8 de 12; los 4 autovalores nulos son las direcciones de las dummies. En cambio, el bloque de los 8 términos que no son dummies es de rango completo (autovalor mínimo 7,1e-7). El borrador de `specs/005-estres/spec.md:59` habla de «rango reducido esperado» para ese bloque: eso vale para la matriz completa, no para el bloque.
   - **Simetría:** los bloques cruzados entre dummies y resto no se simetrizan (`src/estimation.py:146-149`; asimetría de 1e-16). La 005 debe usar solo el bloque de 8 términos y simetrizarlo.
   - **Coeficientes de la tasa en cero:** hay que pre-registrar si se simula el resto con su distribución marginal o condicionada a θ = 0. Hoy θ0 tiene covarianzas distintas de cero con ρ, con la constante y con ΔU.
   - **Réplicas explosivas:** P(ρ ≥ 1) ≈ 1,8e-4 por extracción, es decir, unas 2 réplicas de cada 10 000. El borrador ya reporta esa proporción; está bien.
   - **Origen de la proyección:** el panel trae una fila 2026T3 con `fedfunds` y `unrate_d` pero sin morosidad. El arranque debe ser `sample_end` (2026T2), no la última fila del panel.
2. **Menor, `outputs/tables/model2_stationarity.csv`, columna `columna_panel`:** pone `dralacbs`, `fedfunds` y `unrate` (la serie base, junto a «forma») para términos que en el panel son `*_d`. Es la misma ambigüedad que causó el error de la ronda 1. Conviene renombrar la columna a «serie» o poner la columna diferenciada.
3. **Menor, pendientes para la 006 (heredados de la ronda 1, siguen vigentes):**
   - las limitaciones prometen «se discute qué implica» sin que esa discusión exista (`src/model2.py`, tabla de limitaciones);
   - el VIF de ΔU (33,2) se rotula «posible multicolinealidad» cuando es un artefacto de las dummies COVID;
   - con K = 1, C1 y C2 son el mismo Wald (χ² = 0,857);
   - φ_h ≈ 3,2 hace que β_h describa un ciclo de alzas, no un alza de 1 pp.
4. **Menor, formato del JSON:**
   - `h_star.signo` usa el signo menos Unicode «−»; la 005 debe leerlo así;
   - el JSON no tiene una clave explícita para la columna dependiente (`dralacbs_d`) ni marca qué términos son dummies de impulso. Se deduce de `columns` nulos y del prefijo `covid_`.
5. **Opcional:** «−0,000» en ψ12 y en S de R3; h\* dibujado sobre el eje de rezagos j en `model2_profile.png`; el eje del CUSUM no marca el hueco de 2020T2–2021T1.
6. **Proceso:** `review-audit-ronda1.md` entró en el mismo commit que el arreglo (`b2cd4f4`); la validación la firmó el mismo agente que implementó (declarado).

## Lo que defendería ante el profesor
- La especificación, la regla de selección de K, la regla de lectura y la regla para el estrés se commitearon antes de la primera estimación (`ec983d0` → `7325ff2`). «Sin evidencia» es el resultado de una regla fijada de antemano.
- Todo usa errores HAC, Breusch-Godfrey no rechaza (p = 0,49) y AIC y BIC eligen K = 1 sobre la misma muestra. El modelo se puede reconstruir exactamente desde el JSON exportado.
- Los rezagos distribuidos, las proyecciones locales, R2 y R3 coinciden: no hay asociación rezagada positiva, y el signo puntual negativo es coherente con que la Fed reacciona al ciclo.

## Lo que me preguntaría el profesor
1. Con K = 1, Granger y C2 son la misma prueba. ¿No se reduce entonces su «regla de dos condiciones» a un solo p-valor de θ1 = 0,355?
2. RESET rechaza con p < 0,001 y el Chow de 2020T2 también. ¿Qué parte de «sin evidencia» sobrevive si la forma lineal no es correcta y los parámetros cambian después de 2020?
3. En el estrés pone la tasa en cero por la regla heredada, pero θ0 está correlacionado con ρ y con ΔU en la covarianza HAC. ¿Simula el resto de coeficientes condicionado a θ = 0 o con su distribución marginal, y cuánto cambia el pico de morosidad?
