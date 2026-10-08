VEREDICTO: CAMBIOS NECESARIOS

Audité la spec 004 (Modelo II): `specs/004-modelo-ii/{spec,plan,tasks,review-validate}.md`, las 14 tablas `outputs/tables/model2_*`, las 3 figuras, `outputs/models/model2_main.json`, el bloque `modelo2:` de `report/_variables.yml` y `docs/constitution.md`.

**En corto:** la econometría está bien y el pre-registro se respetó. Pido dos cambios pequeños antes de cerrar:
- uno en la exportación que va a leer la spec 005;
- uno de notación en las tablas que irán al informe.

## Qué comprobé y cómo
- **Tests:** `uv run pytest -q` da **756 passed** en 218 s, rc = 0. Solo hay FutureWarnings de pandas y statsmodels. `git status --porcelain` está vacío.
- **Pre-registro:** spec `ec983d0` (11:19), cambio C1 `45c43d5`, plan `7f732ce` (11:38). La primera salida real es `7325ff2` (15:07). Los tres primeros commits solo tocan `specs/` (y `MEMORY.md` en el del plan).
- **Aritmética contra el JSON:**
  - S = θ0 + θ1 = −0,048. Su EE sale de la covarianza: √(0,0041118 + 0,0014927 − 2·0,0020933) = 0,0377, y χ² = 1,64.
  - S_rez = θ1 = 0,036, con EE 0,0386 y χ² = 0,857, igual que Granger (con K = 1 es el mismo test).
  - La recursión ψ_h cuadra: ψ1 = 0,036 + 0,699·(−0,084) = −0,023. R(12) = −0,159 ≈ S/(1−ρ).
  - BIC − AIC = 12·(ln 105 − 2) = 31,85, como en la tabla.
  - Ventanas HAC: 4 con T = 105; 3 con 97 y 69; max(fórmula, h+1) en las proyecciones locales.
  - n: R2 = 105 − 8 = 97; R3 = 105 − 36 = 69.
  - Trimestres útiles del Chow: 33/68 y 80/21.
  - BG: χ²(4) = 3,409 da p = 0,492.
- **Coherencia entre archivos:** coeficientes, efectos, LP, diagnósticos, robustez e insumos de la 6.3 coinciden entre `.md`, `.csv` y `_variables.yml`. La fila del Modelo I en `model2_inputs63` es la de `model1_coefficients`: −0,044, EE 0,040, p 0,269, n = 106.
- **Checklist de la skill:**
  - Estacionariedad: cada término tiene su fila, y la desviación de la regla está pre-registrada y declarada.
  - HAC en todo, con la ventana declarada.
  - AIC y BIC sobre la misma M: 105 observaciones en los 8 modelos.
  - Signos: H1 dice «no» y se reporta tal cual.
  - Lenguaje causal: ninguno (lo busqué con grep en las salidas del Modelo II).
  - Diagnósticos fallidos: se reportan; la discusión de qué implican queda pendiente (punto 3).
  - Reproducibilidad: no corrí el pipeline porque no me lo indicaron. La cubren `test_two_independent_roots_leave_identical_bytes` y `test_running_models_twice...`, que están en verde.

## Cambios necesarios

1. **Importante, el único que bloquea.** `src/model2.py:734-735` → `outputs/models/model2_main.json`, clave `columns.y_lag`.
   - **Qué pasa:** exporta `{"column": "dralacbs", "lag": 1}`. El plan (§4) define `columns` como «término → **columna del panel** y rezago». En el panel, ΔDR es `dralacbs_d`; `dralacbs` es el nivel, alrededor de 1,5 %. Los demás términos sí apuntan a la columna real (`fedfunds_d`, `unrate_d`).
   - **Por qué importa:** la spec 005 (crítica) va a proyectar de forma recursiva leyendo este contrato. Si lo toma al pie de la letra, mete el nivel como ΔDR(t−1): ρ·1,5 ≈ +1,05 pp por trimestre de error, sin que nada falle.
   - **Qué espero:** `"dralacbs_d"`, con un test que compruebe que cada `columns[*].column` existe en el panel y es la serie que entra en la forma del modelo.

2. **Menor.** `src/model2.py:248, 262, 309, 321, 347`: la notación se rompe con K = 1. Salen «θ0+…+θ1», «θ1 = … = θ1 = 0», «θ1..θ1» y «ΔFFR(t..t−1)» en `model2_effects`, `model2_reading`, `model2_diagnostics` y `model2_limitations`.
   - **Por qué importa:** son tablas que irán al informe y ahí parecen un error.
   - **Qué espero:**
     - con K = 1: «θ0 + θ1», «θ1 = 0», «θ1», «ΔFFR(t) y ΔFFR(t−1)»;
     - con K ≥ 2: la forma general;
     - un test para cada caso.

## Para la spec 006 (no bloquean la 004, pero sin esto el informe no se defiende)

3. **Importante.** `src/model2.py:636`, en `model2_limitations`: el texto dice «se reporta y se discute qué implica para las conclusiones», pero esa discusión no existe todavía. La skill la exige y la 006 tiene que escribirla:
   - **BP y White fallan:** el HAC ya cubre la heterocedasticidad, así que la inferencia se mantiene en sentido asintótico.
   - **JB falla (209):** colas gruesas por la crisis de 2008–2010; los p-valores con n = 105 dependen de la aproximación asintótica.
   - **RESET falla (p < 0,001):** la forma lineal no recoge alguna no linealidad (probablemente el pico de 2009–2010), y eso es relevante para «sin evidencia».
   - **Chow 2020T2 falla, con 21 trimestres útiles:** R2 (sin 2020–2021) da casi lo mismo (S = −0,043; S_rez = 0,040, p = 0,303), y eso es lo que hay que decir.
   - **Chow 2008T3 pasa aquí y fallaba en el Modelo I:** comentarlo en la 6.3.

4. **Importante.** `src/model2.py:632`: el VIF de ΔU(t−1), 33,2, se rotula «posible multicolinealidad», y es un artefacto. El VIF se calcula con las dummies COVID en la regresión auxiliar (`src/diagnostics.py:259-270`), y esas dummies absorben justo los saltos de ΔU:
   - +9,17 pp, que entra en 2020T3;
   - −4,20 pp, en 2020T4;
   - −2,03 pp, en 2021T1.

   El informe debe decirlo; si no, el lector concluye que hay colinealidad entre los controles.

5. **Importante, de interpretación.** Las proyecciones locales llevan normalizaciones distintas.
   - φ_h llega a 3,2 en h = 5–7: un +1 pp en ΔFFR(t) viene seguido de unos 3 pp de alzas acumuladas. Por eso β_6 = −0,558 es la morosidad asociada a un ciclo de alzas, no a 1 pp.
   - En h = 1–3, el límite superior de la banda al 90 % de β_h es 0,003, 0,001 y 0,005. Casi excluye el cero, pero del lado **negativo**.
   - Lo correcto es decir que «no se detecta una asociación rezagada positiva y las estimaciones puntuales apuntan a signo negativo, coherente con que la Fed sube tasas en expansiones (endogeneidad)». Nunca «la política monetaria no afecta».

6. **Menor.** Con K = 1, C1 (Granger) y C2 son el mismo Wald sobre θ1 (χ² = 0,857 en los dos). La «evidencia parcial» solo es alcanzable si θ1 es significativamente negativo. Hay que decirlo para que nadie lea C1 y C2 como dos pruebas independientes.

## Opcional (no bloquea)
- `outputs/tables/model2_stationarity.md`:
  - La decisión «niveles» de filas que entran en diferencia confunde; «estacionaria en su forma» sería más claro.
  - Además, FEDFUNDS y UNRATE son I(0) en niveles según la 001 (ADF −3,82 y −2,90) y entran en diferencia por motivo económico (la guía 3.4 pide el «cambio en la FFR»). Conviene decirlo explícitamente en `model2_deviations` en lugar de dejarlo dentro de «forma fija».
- `outputs/figures/model2_cusum.png`: el eje es posicional y salta de 2018T2 a 2023T2 sin marcar el hueco de las 4 dummies.
- `model2_main.json`: no marca qué términos son dummies de impulso ni que `cov_hac` tiene rango reducido. La 005 debe simular solo el bloque informativo (ya está en `MEMORY.md`).
- «−0,000» en ψ_12 y en S de R3 (O2 de la validación).
- `model2_profile.png` dibuja h* (definido sobre ψ_h) en el eje de rezagos j. Aquí coinciden solo porque h* = 0.

## Lo que defendería ante el profesor
- La especificación, K, la regla de lectura y la regla para el estrés se commitearon antes de la primera estimación (`ec983d0` → `7325ff2`). «Sin evidencia» es el resultado de una regla fijada antes de ver los datos, no una elección.
- ΔFFR es I(0), y la inferencia sobre θ_j (coeficientes de regresores estacionarios) es estándar aunque π y CRED no sean I(0). Todo es HAC, con BG limpio (p = 0,49) y M común para AIC y BIC (BIC y AIC eligen K = 1).
- Dos enfoques distintos (rezagos distribuidos y proyecciones locales) y dos robusteces (R2, R3) coinciden: no hay asociación rezagada positiva, y el signo puntual negativo es coherente con la reacción de la Fed al ciclo.

## Lo que me preguntaría el profesor
1. Si K = 1 y las proyecciones locales muestran β_h negativo hasta h = 10, ¿no está diciendo el modelo que subir tasas «reduce» la morosidad? ¿Cómo separa eso de la endogeneidad sin un shock identificado?
2. RESET rechaza con p < 0,001 y el Chow de 2020T2 también: ¿por qué creerle a una conclusión de «sin evidencia» obtenida con un modelo lineal mal especificado e inestable?
3. φ_h ≈ 3: su «shock de 1 pp» es en realidad un ciclo de unos 3 pp de alzas. En la prueba de estrés, con la tasa en cero por la regla heredada, ¿cómo responde a la pregunta de la guía, «¿cómo afectan los cambios en la política monetaria?»?

Archivos clave:
- `C:\Users\gabri\orca\riesgo-credito-macro\src\model2.py`
- `C:\Users\gabri\orca\riesgo-credito-macro\outputs\models\model2_main.json`
- `C:\Users\gabri\orca\riesgo-credito-macro\outputs\tables\model2_limitations.md`
- `C:\Users\gabri\orca\riesgo-credito-macro\outputs\tables\model2_lp.md`
- `C:\Users\gabri\orca\riesgo-credito-macro\specs\004-modelo-ii\plan.md`
