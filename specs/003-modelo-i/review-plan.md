VEREDICTO: CAMBIOS NECESARIOS

Plan auditado: C:\Users\gabri\orca\riesgo-credito-macro\specs\003-modelo-i\plan.md (borrador), contra spec.md (aprobada, commit 667b313, que solo contiene spec y review-clarify, así que el pre-registro está intacto), docs/constitution.md y docs/guia-profesor.md. `uv run pytest -q` da 187 passed (línea base, sin código de la 003). Comprobé contra el código de statsmodels 0.15.0 instalado en .venv y con dos simulaciones en el scratchpad. No calculé ningún coeficiente con datos reales.

En lo general el plan es sólido. Cubre todos los RF, tiene funciones puras, la inferencia sale de un solo camino (b, V) y fija una semilla. Los tests usan DGP con coeficientes conocidos y ninguno compara coeficientes reales. Las ventanas de R6, R7 y R8 cuadran con los datos congelados: R6 empieza en 2001T1, R7 en 2002T1 y R8 en 2000T1, por lo que R8 queda «no estimada». Aun así, hay cuatro fallos técnicos que salen de un solo hecho que el plan no anticipa: las dummies COVID son dummies de impulso, cada una vale 1 en un solo trimestre, y por eso los residuos en 2020T2–2021T1 son exactamente cero. A eso se suma una decisión que el plan deja abierta y que mueve los p-valores.

## Cambios necesarios

### Crítico
1. **plan.md:151-153, 328 (D7) y 345. El CUSUM no se puede ejecutar tal como está escrito (RF-14).** `recursive_olsresiduals(sm_result, skip=None)` usa skip = k = 11 y comprueba el rango de `x[:skip]` (statsmodels/stats/diagnostic.py:1988-1993). En 2000T1–2002T3 las cuatro columnas COVID valen cero, así que la matriz es singular y la función lanza `ValueError`. Ningún `skip` lo arregla sin que el CUSUM empiece después de 2021T1. El test de la línea 345 usa datos sin dummies y no lo detectaría.
   - Por qué importa: la etapa `models` se cae, o alguien lo «arregla» sobre la marcha quitando las dummies, lo que cambia la especificación sin `/sdd-change`.
   - Qué se espera: un CUSUM propio, declarado en D7, que use una equivalencia exacta. MCO con una dummy de impulso da los mismos coeficientes que borrar ese trimestre, así que los residuos recursivos de la principal son los de la regresión sin dummies sobre la muestra sin 2020T2–2021T1, y esos trimestres no aportan nada al CUSUM. Las bandas de Brown, Durbin y Evans deben calcularse con n − k − 4. El pie debe decirlo. Hace falta un test con dummies de impulso que compare con la regresión con esos trimestres borrados.

### Importantes
2. **plan.md:37, 116-117, 135 y 344. Con dummies de impulso, la matriz HAC es singular por construcción y el truncamiento espectral se activará siempre (RF-7, RF-9, RF-20).** La puntuación x_dt·e_t de cada dummy vale cero en todos los trimestres, porque e_τ = 0. Por eso S tiene rango k − 4 como máximo, y V = (X'X)⁻¹S(X'X)⁻¹ también. Lo comprobé con una simulación con n = 106 y 4 dummies: los cuatro valores propios relativos más pequeños salen entre −9e-17 y 5e-17, todos por debajo de `PSD_REL_TOL = 1e-10`. Pasará en la principal, en las dos Chow, en R2–R7 y en las demás variantes con dummies COVID.
   - Por qué importa: el pie de la tabla principal dirá «truncamiento espectral aplicado» y RF-20 lo listará como limitación. Parece un fallo numérico cuando es una propiedad algebraica: la dirección nula es x_τ'b, el ajuste en el trimestre COVID. La spec pensó el truncamiento para problemas numéricos. El test «una matriz definida positiva queda igual» no refleja el caso real.
   - Qué se espera: el plan reconoce el caso y decide cómo tratarlo antes de estimar. Una opción defendible es comprobar la PSD solo en el bloque de los coeficientes sin dummies y reportar aparte «rango reducido por dummies de impulso (esperado)», sin contarlo como truncamiento. Hace falta un test con dummies de impulso. Si esto choca con la definición de la spec, hay que pasar por `/sdd-change` ahora, no después de ver resultados.
3. **plan.md:141-144, 326 (D5) y 345. El test de White no elimina toda la colinealidad (RF-12).** El plan solo quita los cuadrados de las dummies y los productos entre dummies. Pero el producto de una dummy de impulso por un regresor continuo es x_τ·d, proporcional a d. Son 4 × 6 = 24 columnas colineales.
   - Por qué importa: la auxiliar con `lstsq` da bien el R², pero los grados de libertad se inflan en unos 24. El p-valor sube y White «pasa» sin motivo. Es un diagnóstico que puede ocultar heterocedasticidad.
   - Qué se espera: eliminar por rango, por ejemplo con QR con pivoteo, y no por duplicados exactos. Los grados de libertad deben ser rango(Z_aux) − 1. Hace falta un test con dummies de impulso que compruebe esos grados de libertad.
4. **plan.md:135 y 325 (D4). Hay una decisión abierta («Revísala») justificada con un dato falso (principio 2, pre-registro).** El plan dice que `use_correction=True` es lo que statsmodels hace por defecto con HAC. No es así: en el código instalado, `kwargs.get("use_correction", False)` (regression/linear_model.py:2884). La spec define Newey-West con Bartlett y floor(4·(T/100)^(2/9)), sin factor n/(n−k). Con k = 11 y n = 106, ese factor sube los errores un 5,6 %.
   - Por qué importa: si se decide después de estimar, mover los p-valores alrededor de 0,05 o 0,10 es buscar significancia.
   - Qué se espera: fijarlo ahora, antes de aprobar el plan. Lo coherente con la spec es `use_correction=False`, Newey-West puro. Hay que corregir la justificación de D4 y añadir un test que compare la V de `fit_ols_hac` con una Newey-West calculada a mano en un caso pequeño.
5. **plan.md:93-94, 181 y 252. La tabla de RF-15 no dice de qué fila sale la dependiente.** RF-15 pide la dependiente «en la forma en que entra», que es ΔDRALACBS. `diff_regressor_stationary` solo cubre ΔU y ΔFFR.
   - Por qué importa: si se copia la fila «tal cual» de `dralacbs` («ambigua», I(1)), la tabla marcará la dependiente como «no I(0)» y RF-20 sumará una limitación falsa. Con la regla aplicada a la fila «primera diferencia» (ADF p = 0,0096, KPSS p = 0,10), la dependiente es I(0). Lo mismo vale para Y(t−1).
   - Qué se espera: aplicar `diff_regressor_stationary` también a la dependiente y su rezago cuando la forma es Δ, más un test. Además, una nota que diga que la fila de CRED(t−4) usa el ADF/KPSS de `loans_yoy` sin rezagar.

### Menores (bloquean porque dejan un RF ambiguo, pero son baratos)
6. **plan.md:139.** Breusch-Godfrey devuelve LM y F. Hay que fijar cuál se reporta (RF-12); se recomienda LM con χ²(4).
7. **plan.md:169-171 y 330 (D9).** Declarar el divisor de γ̂0, n o n − 1, y el convenio de signo de e. Si no, el test hecho a mano «con n = 5» fija la convención por accidente.
8. **plan.md:108.** El recorte por el faltante terminal de la dependiente se aplica a todas las variantes, también a la principal. RF-1 exige 2000T1–2026T2 estricta. Hay que limitarlo a las dependientes alternativas, o hacer que en la principal sea un error.
9. **plan.md:126 y 180.** Declarar dónde y con qué `ddof` se calcula la DE de RF-10 (se recomienda ddof = 1, el de pandas, dicho en el pie).
10. **plan.md:234.** `X_test` no tiene función: hay que construirlo con `build_design` y una `VariantSpec` del tramo de prueba, para que pase por el control de NaN de RF-2. También conviene que el test compruebe que `y_anchor` es ΔDR(2021T4) y no el nivel.

## Opcional (no bloquea)
- **plan.md:77, 109 (R1).** Declarar en el pie que Newey-West trata 2019T4 y 2022T1 como contiguos. También que Y(t−1) y CRED(t−4) de 2022T1 salen de trimestres excluidos: es coherente con «historia transformada», pero hay que decirlo.
- **plan.md:111 y 332 (D11).** Que la omisión automática de dummies sin variación solo valga en R1 y en la validación fuera de muestra, y que en cualquier otro caso sea un error, para no perder una dummy en silencio.
- **plan.md:350.** Añadir `hac_lags == 4` y `n_parametros == 11` a `test_frozen_model1`.
- **plan.md:262.** Que el test de reproducibilidad compruebe también que las claves de `_variables.yml` que no son `modelo1` quedan byte a byte iguales.
- **Chow en 2020T2:** quedan unos 21 trimestres posteriores útiles (25 menos 4 dummies) para 7 restricciones con HAC. El tamaño real puede apartarse del 5 %. Conviene declararlo en la nota.

## Hallazgos sobre la spec (fuera del plan; decidir antes de la tarea 9, la primera estimación)
Calculé solo desviaciones estándar de los regresores sobre los datos congelados, no resultados del modelo.
- **spec.md:47 (por 1 DE).** Los trimestres COVID inflan la DE: ΔU tiene DE 1,05 pp con ellos y 0,31 pp sin ellos (2020T2 = +9,17 pp); el PIB, 2,05 frente a 1,78. Las dummies absorben esos trimestres en la estimación, pero no en la DE. El efecto «por 1 DE» de ΔU, que va en la figura de RF-11 y se lee como lenguaje de riesgo, equivaldría a unas 3,4 veces un movimiento típico.
- **spec.md:62 y 73 (dummies 2020T2–2021T1).** Las tasas interanuales arrastran el efecto base fuera de la ventana: `gdpc1_yoy` de 2021T2 vale +11,8 % y no tiene dummy. Además, la subida del crédito con el PPP pasa a CRED(t−4) entre 2021T2 y 2022T1. Son puntos de alto apalancamiento en la principal.
- Ambos hallazgos se pueden cambiar con `/sdd-change` sin dañar el pre-registro, porque todavía no hay estimaciones. Una vez hecha la tarea 9, ya no.

## Puntos de la skill que comprobé
- Estacionariedad: revisé contra stationarity.csv. Encontré el hallazgo 5.
- HAC: comprobé la fórmula de la ventana (hac_lags(106) = 4, hac_lags(1) = 1). La corrección de pequeña muestra es el hallazgo 4.
- Selección de rezagos: no aplica en el Modelo I, tiene rezagos fijos.
- Signos esperados: están en la configuración y la tabla compara el signo estimado con el esperado.
- Lenguaje: lo controla el test de RNF-7.
- Diagnósticos fallidos: van a RF-20.
- Reproducibilidad: el test de dos corridas compara bytes.
- Tests de estimadores: DGP con tolerancia 0,05 y HAC frente a MCO clásico con AR(1) 0,7 y 0,8. Bien, pero faltan casos con dummies de impulso.

## Lo que defendería ante el profesor
- El modelo quedó fijado y commiteado (667b313) antes de cualquier estimación. El plan no compara coeficientes reales en ningún test y deja la primera estimación para la última tarea.
- Toda la inferencia (z, p, IC, efectos de largo plazo con método delta, Chow) sale de una sola V HAC con la normal, como pide la spec.
- La validación fuera de muestra contra un paseo aleatorio, con Diebold-Mariano corregido por HLN y veredicto fijado de antemano, hace que el modelo se gane el uso en el estrés.

## Lo que me preguntaría el profesor
1. Si las dummies COVID dejan los residuos en cero, ¿qué significan su CUSUM, su test de White y su matriz de covarianza?
2. ¿Por qué la «desviación estándar» de ΔU incluye un salto de 9 pp que el propio modelo neutraliza con una dummy?
3. ¿Eligió la corrección de pequeña muestra de los errores HAC antes o después de ver los p-valores?
