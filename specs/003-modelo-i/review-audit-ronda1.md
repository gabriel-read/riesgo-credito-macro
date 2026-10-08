VEREDICTO: CAMBIOS NECESARIOS

Revisé la spec 003 (Modelo I): spec.md, plan.md, tasks.md, review-plan.md y MEMORY.md, todas las tablas de `outputs/tables/model1_*` (.md y .csv), `outputs/models/model1_main.json`, las tres figuras PNG, el bloque `modelo1:` de `report/_variables.yml` y el código de `src/estimation.py`, `src/diagnostics.py` y `src/model1.py`. `uv run pytest -q` da **457 passed** (solo hay avisos de deprecación). No ejecuté ninguna etapa del pipeline porque no me indicaron cuál. Tampoco edité ningún archivo.

La estimación está bien hecha. Comprobé a mano el efecto de largo plazo del PIB y su error delta con la `cov_hac` del JSON: −0,0437 y 0,0216, igual que la tabla. La ventana HAC es la correcta (4 rezagos; 3 en R1 y R7, con T = 98). El tratamiento de las dummies de impulso, el CUSUM sobre la regresión reducida y los grados de libertad de White siguen el plan. Los números del gráfico de coeficientes coinciden con la tabla de efectos. Los cambios que pido son de salidas que incumplen el plan o la spec y de textos que llevan al lector a una conclusión equivocada. No hay errores de estimación.

## Cambios necesarios (por gravedad)

**Importantes**

1. **El Chow lleva una advertencia que no tiene evidencia reproducible y no está pre-registrada.**
   - Dónde: `src/model1.py:628-630`, que pasa a `outputs/tables/model1_limitations.md:14-15` y a `modelo1.limitaciones`. El test `tests/test_model1.py:1155` fija ese texto.
   - Qué incumple:
     - RF-13 y RF-20 no prevén esa frase, y no figura en «Desviaciones del pre-registro» (principio 2).
     - La afirmación «está sobredimensionado en muestra finita» se apoya solo en una simulación citada en `MEMORY.md:7` («~40 % y ~65 %»). No hay script, test ni tabla en el repo que la reproduzca (principio 5).
     - Debilita un diagnóstico fallido, contra la regla de la skill: «un diagnóstico fallido no se oculta».
   - Por qué importa: el Chow de 2008T3 (W = 24,987, p < 0,001) es la evidencia más fuerte de inestabilidad de parámetros. Y la spec 005 va a proyectar con esos parámetros.
   - Qué se espera, una de dos:
     - (a) Quitar la frase y dejar el rechazo tal cual. Que el CUSUM pase se cuenta como un hecho aparte, no como atenuante.
     - (b) Hacer un `/sdd-change` que registre una simulación de tamaño reproducible (DGP declarado, semilla fija y tabla de salida con el tamaño empírico y el valor crítico corregido). En ese caso hay que reportar si W = 24,987 sigue rechazando con el valor crítico corregido.

2. **La tabla de efectos no tiene pie y no muestra las DE.**
   - Dónde: `src/model1.py:230` (`effects_table`) y `outputs/tables/model1_effects.md`.
   - Qué incumple:
     - La decisión D16 del plan («el pie lo dice»).
     - La definición de «efecto de largo plazo» de la spec: con Y en Δ es el cambio acumulado en el nivel ante un aumento transitorio de un trimestre, y eso no aparece en ninguna salida.
   - Por qué importa: hoy no se puede saber cuánto vale «1 DE» de cada regresor (solo se infiere dividiendo, por ejemplo 0,024/0,077 ≈ 0,31 pp para ΔU). El informe tampoco puede escribirlo sin teclear un número a mano.
   - Qué se espera: un párrafo «Nota:» con:
     - la DE (ddof = 1) de cada regresor;
     - la muestra en que se calcula (2000T1–2026T2 sin 2020T2–2021T1, cambio C1);
     - la lectura del largo plazo con Y en primera diferencia.

3. **La columna `terminos_diferencia` está vacía en R4, R6 y R7 (incumple RF-16).**
   - Dónde: `src/model1.py:380-391`. `_terms_difference` compara solo nombres de columna, y R4, R6 y R7 cambian el contenido de `gdp_growth` o `credit_growth` sin cambiar el nombre. Se ve en `outputs/tables/model1_robustness_estimates.csv`.
   - Por qué importa: en `model1_robustness_summary.md` la fila «CRED(t−4)» muestra «no» en R6 y R7. Ahí el regresor es otro (CRED(t−8) y CRED(t−12)), no CRED(t−4) que deja de ser robusto. Un lector entendería que CRED(t−4) falla en dos robusteces.
   - Qué se espera: indicar el cambio en cada caso, por ejemplo «sustituye: gdpc1_yoy → gdp_yoy» y «sustituye: CRED(t−4) → CRED(t−8)». Añadir también una nota en la tabla resumen.

4. **El texto de la alerta de VIF da un diagnóstico equivocado.**
   - Dónde: `src/model1.py:633`, que pasa a `model1_limitations.md:13` («posible multicolinealidad»).
   - Qué ocurre: el VIF de ΔU (36,811) se calcula con las dummies COVID dentro de X. Casi toda la varianza de ΔU es el salto de 2020T2, que la dummy absorbe. Eso no es colinealidad entre regresores macro: significa que el coeficiente de ΔU se identifica solo con la variación fuera de la COVID, que es pequeña. Esa es la explicación económica de su IC tan ancho.
   - Qué se espera: corregir el texto de forma cualitativa. Si se quiere dar la cifra «3,1 sin dummies» que cita `MEMORY.md:8`, tiene que salir de una salida generada (`/sdd-change`), nunca escribirse a mano.

5. **Fuera de muestra: la tabla y las variables muestran cifras distintas, y con 2 decimales el resultado no se entiende.**
   - Dónde: `src/report_vars.py:172-177` redondea a 2 decimales y `outputs/tables/model1_oos.md` usa 3.
   - Qué ocurre:
     - `report/_variables.yml:380` muestra «0,03» para el RMSE del modelo y «0,03» para el del ingenuo, con el veredicto «supera al ingenuo».
     - Hay más discrepancias entre tabla y variables: 0,276 frente a 0,28; 1,625 frente a 1,63 (`_variables.yml:389`); −0,080 frente a −0,08.
   - Por qué importa: el propio argumento de D12 (con centésimas, 2 decimales ocultan la diferencia) aplica aquí.
   - Qué se espera: 3 decimales en la tabla y en las variables, con la enmienda menor de D12 anotada en el plan.

**Menores**

6. **La etiqueta de R2 es falsa.**
   - Dónde: `src/model1_config.py:110` («Desestacionalizada con dummies estacionales»), que pasa a `_variables.yml:73` y a las tablas.
   - Qué ocurre: DRALACBN es la serie **sin** desestacionalizar.
   - Qué se espera: «DRALACBN sin desestacionalizar, con dummies estacionales».

7. **Los trimestres del Chow no siguen el formato AAAAT#.**
   - Dónde: `src/model1_config.py:30` y `src/diagnostics.py:486` producen «Chow 2008Q3» y «Chow 2020Q2» en `model1_diagnostics.md:14-15` y en las limitaciones.
   - Qué incumple: el plan §4 y AGENTS.md fijan el formato `AAAAT#`.
   - Qué se espera: «2008T3» y «2020T2».

8. **Falta `review-validate.md` para cerrar la spec (procedimiento, bloquea el cierre).**
   - Dónde: `spec.md:284` lo exige. Además, `tasks.md:39` dice que lo escribe Claude y `MEMORY.md:6` que lo escribe `/sdd-validate` en OpenCode: hay que aclarar quién.
   - Qué falta comprobar: ningún test verifica que las salidas commiteadas sean las que produce hoy el código. `tests/test_frozen_model1.py:46-62` solo compara dos corridas en `tmp_path`.
   - Qué se espera: que la validación ejecute `uv run python -m src.pipeline all` dos veces y `git diff --exit-code` (RNF-5, criterio de finalización).

## Opcional (no bloquea)
- **Filas de las dummies COVID:** muestran p e IC aunque su EE «no es informativo». Ese EE omite σ², así que el p está subestimado. Conviene mostrar «—» en p e IC, o al menos que la spec 006 no los interprete nunca.
- **Textos de los diagnósticos fallidos:** BP, White, JB y RESET llevan la frase genérica «se reporta y se discute qué implica» (`model1.py:637`). Es aceptable porque la prosa corresponde a la 006, pero queda como deuda explícita de esa spec.
- **Gráfico CUSUM:** el eje es posicional y no marca el hueco de 2020T2–2021T1 (los ticks saltan de 2017T4 a 2022T4). Conviene marcarlo.
- **Gráfico fuera de muestra:** añadir el ingenuo constante, que es el comparador del pronóstico dinámico y el que le gana.
- **Tabla de robustez:** poner en el pie la definición del criterio. Aclarar también que «1 de 9» en ΔFFR significa robusto con el signo **negativo**, el contrario al esperado.
- **Estacionariedad:** el p de KPSS «0,100» es el tope de statsmodels; debería decir «≥ 0,10». El «0,000» del ADF debería ser «< 0,001».
- **Etiqueta «ΔPIB»:** confunde una variación interanual con una diferencia trimestral (en ΔU la Δ sí es diferencia trimestral). La spec lo llama «PIB(t)».

## Lo que deben heredar las specs 005 y 006 (afecta a la conclusión)
- **π y CRED(t−4) son los únicos coeficientes con p < 0,05, y son justo los dos regresores marcados «no I(0)».** ΔDR, que es I(0), se regresa sobre regresores I(1) o ambiguos: es una regresión desbalanceada y la normal de su z no está garantizada. La spec 006 debe decirlo junto al hallazgo, no solo en la lista de limitaciones.
- **ΔFFR tiene signo negativo** (−0,044, p = 0,269), y en R7 es significativo (−0,097, p = 0,027). En la 005, un escenario adverso con alzas de tasas **reducirá** mecánicamente la morosidad proyectada. Hay que decidir y pre-registrar cómo se trata antes de correr la 005.
- **El pronóstico dinámico pierde frente al ingenuo constante** (cociente de RMSE 1,625). La proyección recursiva es justo el mecanismo de la 005, y la figura muestra una subestimación fuerte durante el endurecimiento de 2022–2023.
- **ΔU se identifica con una variación de unos 0,31 pp por trimestre.** Choques de varios pp en el escenario adverso extrapolan muy lejos de esa variación.
- **RESET falla** (no linealidad) y **el Chow de 2008T3 falla**: el modelo lineal puede quedarse corto en las colas. **Jarque-Bera falla** con mucha fuerza (461,9): los IC normales son aproximados.
- **La `cov_hac` del JSON tiene rango 7 de 11 por construcción.** La 005 debe simular solo el bloque sin dummies.
- **No escoger el resultado que conviene:** el largo plazo del PIB tiene p = 0,043 pero su impacto p = 0,110. Además, el R² de 0,832 está inflado por cuatro dummies que ajustan su trimestre de forma exacta.

## Checklist de la skill y cómo lo comprobé
- [x] **Estacionariedad de cada serie y regla de transformación:** revisé `model1_stationarity.md`. La dependiente sigue la regla de la 001. Los regresores con forma fija son una desviación pre-registrada y declarada en RF-21. Salvedad: los dos regresores no I(0) son justo los significativos (ver arriba).
- [x] **Todos los errores HAC, con la ventana declarada:** revisé `estimation.py:110-150` (`use_correction=False`), el pie de la tabla de coeficientes y la columna de rezagos HAC de las robusteces.
- [x] **Selección de rezagos en la misma muestra:** no aplica, porque los rezagos son fijos y pre-registrados.
- [~] **Signos frente a los esperados:** la tabla trae la coincidencia de signo. La sorpresa de ΔFFR queda pendiente de discusión en la 006.
- [x] **Frases causales:** pasa el test de RNF-7 y también lo leí. Solo aparecen los nombres técnicos permitidos.
- [ ] **Diagnósticos fallidos reportados y discutidos:** están reportados, pero el Chow lleva una atenuante sin respaldo (punto 1) y el VIF una explicación equivocada (punto 4).
- [~] **Pipeline idéntico al correrlo dos veces:** el test con dos `tmp_path` pasa. No contrasté las salidas commiteadas contra una corrida nueva porque no estaba autorizado (punto 8).
- [x] **Coincidencia entre tablas, figuras y variables:** coinciden, salvo el redondeo de las métricas fuera de muestra (punto 5).

## Lo que defendería ante el profesor
1. La especificación quedó sellada en el commit `667b313`, antes de estimar; los cambios C1–C3 son anteriores a los datos reales; ningún test compara coeficientes reales.
2. Toda la inferencia sale de una sola matriz HAC Newey-West con la ventana pre-registrada, y el largo plazo usa el método delta (lo verifiqué a mano).
3. Los diagnósticos que fallan se reportan todos, y el modelo se evalúa fuera de muestra contra un ingenuo con un veredicto fijado de antemano, aunque el resultado no favorece al modelo.

## Lo que me preguntaría el profesor
1. «Sus dos únicos regresores significativos, inflación y crédito, son los que no pasan la prueba de estacionariedad. ¿Por qué debo creer esos p-valores?»
2. «Su modelo dice que subir la tasa de la Fed se asocia con *menos* morosidad, y el pronóstico dinámico pierde frente a dejar la morosidad constante. ¿Cómo justifica usarlo en la prueba de estrés?»
3. «El Chow de 2008 rechaza con p < 0,001 y el RESET también rechaza. ¿Qué parte de sus conclusiones sobrevive a la inestabilidad de parámetros y a la no linealidad?»
