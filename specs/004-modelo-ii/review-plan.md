VEREDICTO: CAMBIOS NECESARIOS

Plan auditado: C:\Users\gabri\orca\riesgo-credito-macro\specs\004-modelo-ii\plan.md (borrador). Lo contrasté con spec.md (aprobada, commit ec983d0), docs/constitution.md y docs/guia-profesor.md, y con el código de la 003 que el plan dice reutilizar (src/estimation.py y src/diagnostics.py).
- Línea base: `uv run pytest -q` da 504 passed.
- Hice dos comprobaciones en el scratchpad usando solo los regresores reales del panel congelado: rango de matrices de diseño, nunca la dependiente. No estimé ningún coeficiente del Modelo II, así que el pre-registro sigue intacto.

En lo general el plan es sólido:
- Todos los RF tienen dueño y las funciones son puras.
- Hay una sola maquinaria HAC.
- La muestra común M se fija con K = 8 antes de comparar AIC y BIC.
- Granger va por Wald HAC y deja fuera θ₀.
- Los tests de proyecciones locales parten de un proceso bien elegido. Con ΔFFR ruido blanco, β_h = R(h) se cumple de forma exacta en la población; lo comprobé desarrollando la recursión.
- La primera estimación con datos reales queda para la tarea 8.

Confirmé con los datos congelados las cifras que el plan da por hechas:
- M = 2000T2–2026T2, 105 observaciones.
- 36 trimestres de tasa cero.
- R3 deja 69 observaciones: 54 grados de libertad con K = 8.
- El bloque de interacciones de Chow 2020T2 tiene rango completo para todo K = 1..8.
- La ventana inicial del CUSUM tiene rango completo para todo K.

Hay un fallo que tumba la etapa `models` y dos huecos que la spec pide expresamente cerrar en el plan.

## Cambios necesarios

### Crítico
1. **plan.md:14, 117 (`diagnostics_table2`: «misma batería que la 003») y 238. White se cae con K ≥ 4 y el plan no lo prevé (RF-19, RNF-6, principio 2).**
   - El problema: `src/diagnostics.py:95-132` (`_white_aux_matrix`) arma la auxiliar completa: niveles, cuadrados y productos cruzados de todos los regresores salvo la constante, incluidas las 4 dummies.
   - Columnas auxiliares en el diseño del Modelo II con n = 105:
     - K = 1: 77.
     - K = 3: 104.
     - K = 4: 119.
     - K = 8: 189.
   - Por qué se cae: cuando hay más columnas que observaciones, `qr(..., pivoting=True)` devuelve una diagonal de longitud min(n, m) = 105, mientras P tiene longitud m. Por eso la línea 129 lanza `IndexError: index 105 is out of bounds`. Lo reproduje con los regresores reales en K = 4..8.
   - El otro extremo: con K = 3 sí corre, pero con rango 59 sobre 105 observaciones el LM tiene muy poca potencia.
   - Si se «arregla» con más cuidado y la auxiliar llega a saturarse (R² = 1), el LM vale n y queda comparado con una χ² de unos 104 grados de libertad, p ≈ 0,45. Es un «pasa» espurio.
   - Por qué importa:
     - La regla de selección elige K entre 1 y 8 con BIC. Lo más probable es que la etapa se rompa justo después de ver K.
     - Entonces alguien tendrá que decidir sobre la marcha cómo calcular White: solo cuadrados, sin dummies, otra cosa. Eso es una decisión de diagnóstico tomada con el resultado a la vista.
   - Qué se espera, fijado ahora y antes de estimar:
     - Una regla de calculabilidad, por ejemplo: «no calculable» si n − rango(Z_aux) < 30, con el mismo umbral MIN_DOF de la 003. La fila entonces lleva su motivo y no tiene veredicto, igual que el Chow de RF-20. También entra en las limitaciones detectadas de RF-25.
     - Que `_white_aux_matrix` no se caiga cuando m > n: QR en modo completo, o comprobación previa.
     - Un test con el diseño de dimensión del Modelo II (K = 8, 4 dummies, n = 105) que dé «no calculable», y otro con K = 1 que dé un resultado válido.
     - RF-19 no contempla «no calculable» para White. Si se adopta esa regla o se cambia la auxiliar, por ejemplo a White sin productos cruzados, hay que pasar ya por `/sdd-change` y anotarlo en «Desviaciones del pre-registro».

### Importantes
2. **plan.md:230, 235-237. Faltan las tolerancias que la spec obliga a declarar en el plan (RNF-2, RNF-4, principio 4).**
   - RNF-2 y RNF-4 dicen «dentro de una tolerancia declarada en el plan». El plan repite la frase pero no da ningún número, ni tamaño de muestra, ni parámetros del proceso simulado.
   - Por qué importa: si la tolerancia se fija mientras se escribe el test, la fija el resultado y no el criterio. Además, con ΔDR(t−1) en la ecuación, MCO tiene sesgo de muestra finita en ρ (Hurwicz), y la tolerancia tiene que contar con él.
   - Qué se espera:
     - Declarar en §7 el proceso de cada test: θ, ρ, γ, K verdadero, n y semilla.
     - Declarar su tolerancia absoluta. Por ejemplo, ≤ 0,05 en cada θ_j y en ρ con n = 2 000, como en la 003, y ≤ 0,05 en β_h − R(h) y en φ_h con n ≥ 2 000.
     - Fijar el K verdadero y la magnitud de θ_K para el test de `select_k`, para que no sea frágil.

3. **plan.md:235-237. Nadie prueba la recuperación de coeficientes del estimador del modelo de rezagos distribuidos (RNF-2).**
   - `test_dynamics` comprueba S, ψ_h y R(h) a partir de parámetros dados (forma cerrada), no de una estimación.
   - `test_estimation` ampliado solo cubre `maxlags`, la detección de dummies y HAC > clásico.
   - Por qué importa: la constitución exige probar los estimadores con datos simulados de parámetros conocidos. El diseño concreto de la 004 nunca se prueba de punta a punta: `build_design2` + `fit_ols_hac` con y_lag, ΔFFR(t..t−K), los controles y las dummies.
   - Qué se espera: un test que simule desde el diseño de `build_design2` con θ, ρ y γ conocidos y recupere θ_j y ρ dentro de la tolerancia del punto 2. Que compruebe también que S y S_rez estimados están cerca de los verdaderos.

4. **plan.md:238. Los tests de diagnósticos no cubren lo que exige RNF-6 en la dimensión del Modelo II.**
   - RNF-6 pide tests de:
     - el Chow con K + 7 interacciones;
     - el CUSUM sin los trimestres de las dummies;
     - White con eliminación por rango.
   - El plan solo lista BG y un Chow genérico. Los tests de la 003 usan 7 interacciones y 11 columnas, no K + 7 y hasta 19.
   - Qué se espera: incluir explícitamente esos tres tests con un diseño de K = 8. El de White es el del punto 1.

5. **plan.md:73-75, 95 (`build_lp_design`, target «tasa»). En h = 0 la proyección de la tasa es una identidad (RF-15, RNF-8).**
   - FFR(t) − FFR(t−1) es exactamente el regresor ΔFFR(t). Por eso φ₀ = 1 con ajuste perfecto, residuos del orden de 1e-16 y EE HAC prácticamente cero.
   - `check_dof` no lo detecta.
   - `psd_truncate` puede marcar truncamiento sobre una matriz de ruido numérico.
   - La tabla mostraría «1,000 (0,000) [1,000; 1,000]» con un z del orden de 1e16.
   - Qué se espera:
     - Declarar en el plan que φ₀ = 1 por construcción y cómo se reporta: estimada tal cual con nota, o EE «—» con la nota «por construcción».
     - Un test que compruebe φ₀ = 1, que no aparecen inf ni NaN en el CSV y el JSON, y que la cifra es estable entre corridas.

### Menores (bloquean porque dejan un RF ambiguo, pero son baratos)
6. **plan.md:72 (`covid_lag_leaks`) frente a spec.md:168 (RF-25).** La spec limita la limitación detectada a los rezagos de ΔFFR o de ΔDR que salen de 2020T2–2021T1. El plan la define «lo mismo» que `lagged_from_excluded`, que incluye los controles. Los efectos base de los controles ya son limitaciones fijas aparte (spec.md:158), así que se contarían dos veces. Hay que restringir `covid_lag_leaks` a y_lag y ΔFFR(t−1..t−K), con un test.
7. **plan.md:112 y 221 (D8).** `chow_wald` devuelve hoy la clave `nota` con texto fijo del Modelo I: «interacciones de la constante, ρ y β₁–β₅» (src/diagnostics.py:331-334). Hay que declarar que `diagnostics_table2` no usa esa clave, o parametrizarla. Hace falta un test de que la nota del Modelo II no menciona β₁–β₅ y dice K + 7.
8. **plan.md:112.** La comprobación `calculable` tiene que hacerse antes de `fit_ols_hac(design_aug)` y de `wald`. Con rango incompleto, `np.linalg.solve` puede lanzar `LinAlgError` o devolver números sin sentido. Hay que declarar el orden y la tolerancia del rango (la de `matrix_rank` por defecto o PSD_REL_TOL).
9. **plan.md:118 y 166 (`stationarity_table2`).** Hay que decir de qué fila de la tabla de la 001 sale cada término:
   - ΔDR, ΔFFR y ΔU, de la fila «primera diferencia», con `diff_form_stationary`.
   - PIB, π y CRED, de la fila «tal cual».
   - El pie tiene que decir que los términos rezagados usan el ADF/KPSS de la serie sin rezagar.
   Es la misma lección del punto 5 de la revisión del plan 003, y conviene no repetirla.

## Opcional (no bloquea)
- **plan.md:236.** Añadir un test de invariante: con los mismos datos, β₀ de la proyección local de la morosidad es exactamente θ₀ de la principal, con el mismo EE (misma muestra M y misma ventana, max(4, 1) = 4). Es la garantía de que spec.md:100 se cumple en el código.
- **Chow 2008T3:** quedan 33 trimestres anteriores para hasta 15 interacciones. La spec solo pide la nota de tamaño si los posteriores útiles son menos de 30. Conviene que la nota muestre siempre `n_pre_util`, que el plan ya calcula, para que el lector lo vea.
- **Chow 2020T2 con K alto:** el rango es completo, pero con 25 trimestres posteriores (21 útiles) y 15 interacciones + 4 dummies quedan unos pocos grados de libertad en el bloque posterior. La nota de RF-20 lo cubre; en el informe conviene leerlo solo como señal.
- **plan.md:243.** Que `test_frozen_model2` compruebe también `hac_lags == 4` en la principal y el número de parámetros = K + 11.
- **plan.md:86.** La tolerancia de empate de `peak_horizon` (1e-12 absoluta) está bien a esta escala; convendría declararla como constante en `model2_config`.
- **Pre-registro del plan:** commitear el plan aprobado, con este review, antes de la tarea 8. Así queda constancia de que las reglas de los puntos 1 y 5 se fijaron sin conocer K.

## Checklist de la skill comprobado
- Estacionariedad y transformaciones:
  - Cada término tiene fila en RF-21.
  - π y CRED(t−4) «no I(0)» en nivel es una decisión de la spec aprobada, declarada como desviación. No bloquea el plan.
  - Falta precisar las filas (punto 9).
- HAC y ventana: todo pasa por `fit_ols_hac`. Ventana floor(4·(T/100)^(2/9)) = 4 con T = 105; en las proyecciones, max(fórmula, h + 1). Correcto.
- Misma muestra para AIC/BIC: sí (D3). Comprobé que M no depende de K.
- Signos frente a los esperados: H1 y H2 tienen regla pre-registrada.
- Lenguaje causal: `test_language` ampliado.
- Diagnósticos fallidos: se reportan. White, en cambio, no puede ni calcularse (punto 1).
- Reproducibilidad: la semilla está declarada y hay test de bytes. Falta la estabilidad de φ₀ (punto 5).

## Lo que defendería ante el profesor
- K se elige por BIC sobre una sola muestra común fijada por el rezago máximo, y la lectura de «¿hay efectos rezagados?» (C1/C2) se escribió y commiteó antes de estimar.
- Toda la inferencia (S, S_rez, Granger y Chow) usa una única matriz Newey-West con el mismo tratamiento de las dummies de impulso que el Modelo I ya auditado.
- Las proyecciones locales no imponen la forma paramétrica, y la respuesta de la tasa (φ_h) deja explícito que β_h y R(h) miden objetos distintos.

## Lo que me preguntaría el profesor
1. Si la Fed sube la tasa porque anticipa deterioro, ¿qué le queda de interpretable a S_rez y a Granger, más allá de «la tasa precede a la mora»? ¿Por qué no usar un shock identificado?
2. Con 105 trimestres, hasta 19 parámetros y 36 trimestres con la tasa casi inmóvil, ¿cuánta variación de ΔFFR identifica de verdad los θ_j? ¿Qué dice R3 si queda con 69 observaciones?
3. ¿Por qué dejar π y CRED(t−4) en nivel siendo «no I(0)» cuando la regla del proyecto manda diferenciar? ¿Qué le hace eso a la distribución de los Wald?

Archivos relevantes:
- C:\Users\gabri\orca\riesgo-credito-macro\specs\004-modelo-ii\plan.md
- C:\Users\gabri\orca\riesgo-credito-macro\specs\004-modelo-ii\spec.md
- C:\Users\gabri\orca\riesgo-credito-macro\src\diagnostics.py (líneas 95-132, `_white_aux_matrix`; líneas 331-334, nota fija de `chow_wald`)
- C:\Users\gabri\orca\riesgo-credito-macro\src\estimation.py (líneas 110-112, `_impulse_dummy_cols`)
