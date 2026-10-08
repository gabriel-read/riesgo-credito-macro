VEREDICTO: APROBADO

# Auditoría de la spec 003 (Modelo I), ronda 4

**Qué revisé.**
- Documentos: spec.md, plan.md (con las enmiendas 1–4 de §13), tasks.md, review-validate.md, review-audit.md (ronda 3), docs/constitution.md, docs/guia-profesor.md y MEMORY.md.
- Salidas: las 9 tablas `outputs/tables/model1_*` (.md y .csv), `outputs/models/model1_main.json`, las 3 figuras PNG y el bloque `modelo1:` de `report/_variables.yml`.
- Código: `src/estimation.py`, `src/forecast.py`, `src/diagnostics.py` (Chow, VIF, BP), `out_of_sample` y el diff del último commit en `src/model1.py` (`_excluded_lag_note`, `fmt_kpss_p`) y `tests/test_model1.py`.

**Qué ejecuté.**
- `uv run pytest -q`: **504 passed**. Solo hay avisos de deprecación de `adfuller`.
- No ejecuté ninguna etapa del pipeline sobre el repositorio, porque no me indicaron cuál.
- Sí tengo evidencia independiente de RNF-5. `test_frozen_model1` regeneró todo desde `data/raw/` en dos raíces temporales limpias (`pytest-119/frozen_a0` y `frozen_b0/root`). Comparé esos archivos con `cmp` contra los commiteados en HEAD `5b0f6ef`:
  - las 18 tablas `model1_*`, las 3 PNG, el JSON y `stationarity.csv` son **idénticos byte a byte** en las dos raíces;
  - el bloque `modelo1:` de `_variables.yml` también es idéntico.
- Con esto se cierra el punto [~] de reproducibilidad que dejó abierto la ronda 3.

**Estado de la ronda 3.**
- El punto bloqueante está resuelto. `_variant_note` añade «Y(t−1) de 2022T1 y CRED(t−4) de 2022T1–2022T4 se toman de trimestres excluidos (historia transformada)» en las 5 filas de R1, en el .md y en el .csv.
- Los trimestres los calcula el código desde la exclusión y el rezago de crédito. Tiene tests con otra exclusión (CRED(t−8)) y con un solo trimestre.
- `_quarters_text` supone trimestres consecutivos. Lo comprobé: con una exclusión contigua, el conjunto afectado siempre es un intervalo, así que la suposición es segura.
- El opcional de formato de p también está aplicado: «< 0,001» en ADF, «≥ 0,10» en KPSS, y el CSV conserva los valores brutos.
- La enmienda 4 del plan lo registra.

**Integridad del pre-registro.**
- `spec.md` solo cambia en `667b313` (pre-registro) y en `dbc37c2` (C1–C3, a las 08:30). Las dos son anteriores a la primera estimación real, `b43430b` (13:25).
- `git diff b43430b HEAD -- outputs/` muestra que ninguna cifra estimada cambió en las cuatro rondas. Solo cambiaron notas y etiquetas, se añadió la columna `de` y cambió el formato. Por ejemplo, `model1_coefficients.csv` no se ha tocado desde `b43430b`.

## Cambios necesarios

Ninguno. No encontré errores de estimación, inferencia, cobertura de RF ni coherencia entre salidas.

## Opcional (no bloquea)

1. **La nota de R1 es exacta pero parcial** (`src/model1.py`, `_excluded_lag_note`).
   - Lista Y(t−1) y CRED(t−4), como prometía el plan. Pero también usan niveles de trimestres excluidos:
     - la propia ΔY de 2022T1 (DR(2022T1) − DR(2021T4));
     - ΔU y ΔFFR de 2022T1;
     - las tasas interanuales de PIB y π de 2022T1–2022T4.
   - Esto es inherente a la «historia transformada» y no cambia nada. La 006 no debe escribir que «solo» esos términos tocan trimestres excluidos.
2. **Notación del KPSS distinta entre specs.**
   - `outputs/tables/stationarity.md` (spec 001) dice «>0,10» y `model1_stationarity.md` dice «≥ 0,10».
   - El tope de 0,10 de statsmodels significa que el estadístico está por debajo del valor crítico del 10 %, es decir, p > 0,10 en sentido estricto. Conviene unificar en «> 0,10».
3. **Documentación desfasada en `specs/003-modelo-i/review-validate.md`.**
   - Las líneas 6 y 48 aún dicen «falta la ronda 2».
   - La línea 55 lista como no aplicado el formato «≥ 0,10»/«< 0,001», que ya está aplicado.
   - Basta con actualizarlo al cerrar.
4. **`specs/003-modelo-i/tasks.md`:** T10 sigue «EN CURSO». Es `agente: claude`, así que se puede marcar al registrar esta auditoría.
5. **`MEMORY.md`:**
   - tiene 60 líneas, por encima del máximo de ~50 de AGENTS.md;
   - el punto 1 de «Próximos pasos» está obsoleto («Siguiente: `/sdd-tasks 003-modelo-i`»).
6. **Opcionales de la ronda 3 que siguen sin aplicar:**
   - la etiqueta «ΔPIB» para una variación interanual;
   - `model1_oos.png` no dibuja el ingenuo constante, que es el que le gana al dinámico, y su eje dice «%» frente al «pp» de RF-19;
   - el eje posicional del CUSUM no marca el hueco de 2020T2–2021T1;
   - los grados de libertad de White y RESET no se reportan;
   - las dummies de impulso entran en las auxiliares de BP y White.
7. **Coeficientes del tramo de entrenamiento 2000–2019 sin exportar.** RF-18 no los pide, pero sin ellos la 006 no puede explicar con cifras por qué el dinámico cae hasta unos 0,86 pp en 2022–2023. Si la 006 los necesita, hace falta un `/sdd-change`; no deben citarse a mano.

## Lo que deben heredar las specs 005 y 006

Sigue vigente lo de la ronda 3, con dos precisiones nuevas.

- **Regresión desbalanceada: precisión de defensa.**
  - π y CRED son «no I(0)» por la regla conservadora: ADF no rechaza (p = 0,160 y 0,127).
  - Pero **KPSS tampoco rechaza la estacionariedad al 10 %** en ninguno de los dos (`model1_stationarity.md`). La evidencia es «ambigua», no un I(1) claro.
  - La 006 debe decir las dos cosas: el riesgo de una inferencia no estándar si fueran I(1), y que los datos no permiten afirmarlo.
- **PIB: impacto no significativo y largo plazo significativo.**
  - Impacto: p = 0,110. Largo plazo: p = 0,043. La diferencia sale de la covarianza negativa en el gradiente delta, que verificó a mano la ronda 3.
  - La 006 no debe decir que «el PIB es significativo» sin decir de qué efecto habla. Además, el «3 de 9» de robustez cuenta sobre el coeficiente de impacto.
- **CUSUM pasa y los dos Chow fallan.** No es una contradicción: el CUSUM tiene poca potencia frente a quiebres en pendientes que no desplazan la media. Conviene decirlo para que no parezca una incoherencia.
- **Siguen vigentes:**
  - ΔFFR con signo negativo (significativo en R7). Su tratamiento en el estrés debe pre-registrarse antes de correr la 005.
  - ΔU se identifica con poca variación (DE de 0,308 pp fuera de la COVID).
  - «Supera al ingenuo» (0,978) siempre va con «no significativo» (DM p = 0,937).
  - R1 es un contraste parcial del PPP: conserva el reflejo negativo en CRED(t−4) de 2022T2–2022T3.
  - El R² de 0,832 está inflado por las dummies de impulso.
  - La 005 debe simular solo el bloque de `cov_hac` sin dummies (rango 7 de 11).

## Comprobaciones hechas (coinciden)

- **Cifras entre salidas:** coeficientes, efectos, diagnósticos, robustez, `variantes_muestra` y fuera de muestra son iguales en las tablas `.md`, en `_variables.yml` y en la figura de coeficientes (impacto por 1 DE ± IC 95 %).
- **Inferencia:**
  - z, p e IC del PIB recalculados desde coef y EE: −0,016309 / 0,010218 = −1,596, p = 0,110, IC [−0,036; 0,004];
  - las cifras de efectos del JSON y del CSV son las de `b43430b` (solo se añadió `de`).
- **Recuento «k de n»:** rehecho celda a celda desde `model1_robustness_estimates.md`. PIB 3, ΔU 1, π 8, ΔFFR 1, CRED 7, todos de 9. R8 «no estimada» queda fuera del denominador.
- **Ventana HAC:** 4 rezagos con T = 102 y 106; 3 con T = 98 (R1 y R7), lo que concuerda con floor(4·(T/100)^(2/9)).
- **Estacionariedad:** ADF y KPSS de `model1_stationarity.md` coinciden con las filas correspondientes de `outputs/tables/stationarity.md` (001), y la regla se aplica bien a cada fila.
- **Código revisado:**
  - Newey-West puro (`use_correction=False`, `use_t=False`);
  - truncamiento solo en el bloque sin dummies de impulso;
  - largo plazo con gradiente [1/(1−ρ), β/(1−ρ)²];
  - DM-HLN con divisor n y t(n−1);
  - dinámico anclado en ΔDR(2021T4) y nivel reconstruido con suma acumulada;
  - Chow con 7 interacciones y las dummies sin interactuar.
- **Cobertura de la guía:** la sección 4 (estimar, coeficientes, significancia, diagnósticos) está cubierta. La interpretación desde gestión de riesgos corresponde a la 006, como fija la spec.

## Checklist de la skill y cómo lo comprobé

- [x] **Estacionariedad y regla:** `model1_stationarity.md` frente a la tabla de la 001. Los regresores con forma fija son una desviación pre-registrada (RF-21), y π y CRED figuran como limitación.
- [x] **HAC con la ventana declarada:** pie de la tabla de coeficientes (4 rezagos, Bartlett, sin corrección), columna `rezagos_hac` y código de `fit_ols_hac`.
- [x] **Selección de rezagos sobre la misma muestra:** no aplica; los rezagos son fijos y pre-registrados.
- [~] **Signos frente a los esperados:** la columna `coincide` es correcta (ΔFFR «no»). Discutir la sorpresa corresponde a la 006.
- [x] **Frases causales:** grep de «causa|causal|provoca|debido a» sobre `model1_*`, `_variables.yml` y `data_note.md`: sin resultados. El test de RNF-7 pasa.
- [x] **Diagnósticos fallidos:** BP, White, JB, RESET, los dos Chow y la alerta de VIF figuran en la tabla de diagnósticos y en la de limitaciones, sin atenuantes post hoc.
- [x] **Pipeline idéntico dos veces:** dos raíces limpias de pytest, idénticas entre sí y frente a HEAD byte a byte.

## Lo que defendería ante el profesor

1. La especificación quedó sellada en `667b313` y C1–C3 son anteriores a los datos reales. Cuatro rondas de auditoría no movieron ninguna estimación, y git lo demuestra.
2. Toda la inferencia sale de una sola matriz Newey-West con la ventana pre-registrada, verificada a mano (EE, método delta, recuento de robustez). El pipeline se reproduce byte a byte desde un clon limpio.
3. Se reportan sin maquillaje todos los diagnósticos fallidos, el signo contrario de ΔFFR y que el dinámico pierde frente al ingenuo. Para π y CRED, que salen «no I(0)», KPSS no rechaza la estacionariedad: su no estacionariedad es una cautela de la regla, no un hecho establecido.

## Lo que me preguntaría el profesor

1. «Sus dos regresores significativos, inflación y crédito, figuran como no estacionarios y la dependiente es I(0). ¿Por qué debo creer esos p-valores?»
2. «La tasa de la Fed sale con signo negativo y su pronóstico dinámico se hunde durante las alzas de 2022–2023. ¿Cómo va a usar este modelo en un escenario adverso con alzas de tasas y varios puntos más de desempleo?»
3. «Los dos Chow y el RESET rechazan, pero el CUSUM pasa. ¿Qué afirmación concreta para gestión de riesgos sobrevive a la endogeneidad, la inestabilidad y la no linealidad?»

## Archivos relevantes

- C:\Users\gabri\orca\riesgo-credito-macro\specs\003-modelo-i\spec.md
- C:\Users\gabri\orca\riesgo-credito-macro\specs\003-modelo-i\plan.md (§13, enmienda 4)
- C:\Users\gabri\orca\riesgo-credito-macro\specs\003-modelo-i\review-validate.md (líneas 6, 48 y 55, desfasadas)
- C:\Users\gabri\orca\riesgo-credito-macro\specs\003-modelo-i\tasks.md (T10)
- C:\Users\gabri\orca\riesgo-credito-macro\src\model1.py (`_excluded_lag_note`, `fmt_kpss_p`)
- C:\Users\gabri\orca\riesgo-credito-macro\outputs\tables\model1_robustness_estimates.md
- C:\Users\gabri\orca\riesgo-credito-macro\outputs\tables\model1_stationarity.md
- C:\Users\gabri\orca\riesgo-credito-macro\outputs\tables\stationarity.md (notación «>0,10» de la 001)
- C:\Users\gabri\orca\riesgo-credito-macro\outputs\figures\model1_oos.png
- C:\Users\gabri\orca\riesgo-credito-macro\report\_variables.yml (bloque `modelo1:`)
- C:\Users\gabri\orca\riesgo-credito-macro\MEMORY.md
