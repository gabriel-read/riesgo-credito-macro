VEREDICTO: CAMBIOS NECESARIOS

# Auditoría de la spec 003 (Modelo I), ronda 3

**Qué revisé.** Leí spec.md, plan.md (incluidas las enmiendas de §13), tasks.md, review-plan.md, review-audit-ronda1.md, review-audit.md (ronda 2), review-validate.md, MEMORY.md, docs/constitution.md y docs/guia-profesor.md. También revisé las 9 tablas `outputs/tables/model1_*.md`, `outputs/models/model1_main.json`, las tres figuras PNG y el bloque `modelo1:` de `report/_variables.yml`, y el código afectado (`src/diagnostics.py`, `src/model1.py`, `src/model1_config.py`).

**Qué ejecuté.**
- `uv run pytest -q`: **487 passed** (solo avisos de deprecación de statsmodels/adfuller).
- No ejecuté ninguna etapa del pipeline, porque no me indicaron cuál.
- Leí unos valores de `data/processed/panel.csv` para comprobar un punto. No edité ningún archivo.

**Estado de la ronda 2.** Sus tres puntos están resueltos y aparecen en las salidas commiteadas (HEAD `a1a6246`, árbol limpio):
- La nota de tamaño del Chow 2020T2 la calcula el código: 25 trimestres posteriores menos 4 dummies = 21. Tiene 4 tests y el veredicto sigue a p.
- El §13 del plan recoge las claves `efectos.<macro>.de`, `efectos_nota` y `variantes_muestra.<id>.motivo`, y la columna `de`.
- Todo está commiteado y `AGENTS.md`, `.python-version` y el entorno coinciden en Python 3.11.

No encontré errores de estimación ni de inferencia. Lo único que bloquea es otra nota que el plan promete y el código no escribe. Tiene la misma forma que el punto 1 de la ronda 2, y aplico el mismo criterio.

## Cambios necesarios

**Menor**

1. **El pie de R1 no dice que los rezagos de 2022 salen de trimestres excluidos.**
   - **Dónde:**
     - `src/model1.py:467-472` (`_variant_note`) solo escribe «excluye 2020T1–2021T4; los trimestres vecinos de la exclusión se tratan como contiguos en la ventana HAC».
     - Se ve en las cinco filas R1 de `outputs/tables/model1_robustness_estimates.md` y `.csv`.
   - **Qué incumple:**
     - `plan.md:116` dice: «Además, Y(t−1) y CRED(t−4) de 2022T1 salen de trimestres excluidos, lo que es coherente con la "historia transformada". **El pie de la tabla de robustez lo dice.**»
     - Lo pidió `review-plan.md:36`, y `plan.md:449` (§12, fila «Opc.», «R1 contiguo») lo da por incorporado. Solo se implementó la mitad (la de la contigüidad HAC). Es el mismo patrón que bloqueó en la ronda 2.
   - **Precisión que la nota debe incluir:** con CRED rezagado 4 trimestres, no es solo 2022T1:
     - **CRED(t−4) de 2022T1–2022T4** sale de `loans_yoy` de 2021T1–2021T4 (1,70; −3,95; −1,33; 2,03 %), los cuatro dentro de la ventana excluida;
     - Y(t−1) solo afecta a 2022T1 (ΔDR de 2021T4 = −0,03).
   - **Por qué importa:** para las cifras, poco. Ninguno de esos valores es atípico: el mínimo histórico de `loans_yoy` es −7,95 en 2010T1. Pero:
     - la limitación C2 presenta R1 como «contraste» de los efectos base del PPP, y R1 conserva el reflejo negativo del PPP (−3,95 en 2022T2);
     - la spec 006 no puede escribir esa precisión a mano.
   - **Qué se espera, una de dos:**
     - (a) Que `_variant_note` añada, cuando haya exclusión, una frase generada por código con los trimestres afectados. Por ejemplo: «Y(t−1) de 2022T1 y CRED(t−4) de 2022T1–2022T4 se toman de trimestres excluidos (historia transformada)». Con un test.
     - (b) Si no se quiere esa nota, quitar la frase de `plan.md:116` mediante una enmienda en §13 y corregir la fila «Opc.» de §12.

## Opcional (no bloquea)

- **Formato de p en `model1_stationarity.md`** (tercera vez que se señala): el ADF de ΔU dice «0,000» y todos los KPSS dicen «0,100», que es el tope de la tabla de statsmodels.
  - El «0,000» contradice literalmente D12 («< 0,001» para p pequeños).
  - El «0,100» sugiere un valor exacto cuando significa «≥ 0,10».
  - Conviene arreglarlo en la misma pasada que el punto 1.
- **Dummies COVID:** RF-9 exige p e IC en todas las filas, así que mostrar «—» exigiría un `/sdd-change`. Lo correcto es que la 006 no interprete nunca esos p (por ejemplo, el 0,082 de 2021T1). Su EE omite la σ² del propio trimestre.
- **Etiqueta «ΔPIB»** en `src/model1_config.py`, en `efectos_nota` y en el gráfico de coeficientes: es una variación interanual, no una diferencia. Mejor «PIB (var. interanual)».
- **`model1_oos.png`:**
  - no dibuja el ingenuo constante, que es el comparador del dinámico y el que le gana (RF-19 dice «al ingenuo», en singular, así que cumple);
  - el eje dice «%» y RF-19 pide «en pp»; para un nivel, «%» es correcto, pero conviene alinear el texto.
- **CUSUM:** el eje es posicional (de 2017T4 salta a 2022T4 con el mismo espaciado). Conviene marcar el hueco de 2020T2–2021T1.
- **White y RESET:** reportar sus grados de libertad (rango(Z_aux) − 1 y F(2, 93)).
- **BP y White incluyen las dummies de impulso en la auxiliar.** Ajustan exactamente los cuatro e² = 0 y suman grados de libertad sin contenido. El efecto es pequeño y de dirección incierta; que la 006 no sobreinterprete la magnitud de esos rechazos.
- **MEMORY.md:**
  - tiene 60 líneas, por encima del máximo de ~50 de AGENTS.md;
  - cita «3,1 sin ellas» (VIF de ΔU sin dummies), una cifra que no está en ninguna salida: la 006 no debe usarla.

## Lo que deben heredar las specs 005 y 006 (sigue vigente lo de las rondas 1 y 2)

- **Regresión desbalanceada:** π y CRED(t−4) son los únicos con p < 0,05 y son justo los dos regresores no I(0) frente a ΔDR I(0). La limitación no dice qué implica para la inferencia; la 006 debe decirlo junto al hallazgo.
- **ΔFFR con signo negativo.** Es significativo y negativo en R7 (−0,097, p = 0,027).
  - La figura fuera de muestra muestra que el dinámico cae hasta unos 0,86 pp durante el ciclo de alzas de 2022–2023, mientras la observada sube. Es coherente con ese problema de signo, pero los coeficientes del tramo 2000–2019 no se exportan y no lo comprobé.
  - El tratamiento en el estrés debe pre-registrarse antes de correr la 005.
- **ΔU se identifica con poca variación propia** (DE 0,308 pp fuera de la COVID). Un escenario de varios pp de desempleo extrapola muy lejos.
- **«3 de 9» del PIB y «supera al ingenuo»:**
  - el «3 de 9» del PIB sale de un coeficiente principal con p = 0,110;
  - «supera al ingenuo» (0,978) va siempre con «no significativo» (DM p = 0,937).
- **R1 como contraste de C2 es parcial:** conserva el reflejo negativo del PPP en CRED(t−4) de 2022T2–2022T3.
- **El R² de 0,832 está inflado** por cuatro dummies que ajustan su trimestre de forma exacta.
- **La `cov_hac` tiene rango 7 de 11:** la 005 debe simular solo el bloque sin dummies.

## Comprobaciones hechas a mano (coinciden)

- **Largo plazo con los `params` del JSON:** β/(1 − ρ̂) con 1 − ρ̂ = 0,373512 da
  - PIB −0,0437; ΔU 0,2073; π 0,0530; ΔFFR −0,1174; CRED 0,0266;
  - todos coinciden con la tabla de efectos y con `_variables.yml`.
- **EE delta del largo plazo del PIB con la `cov_hac`:**
  - gradiente [2,6773; −0,1169];
  - Var = 0,00074843 + 0,00011838 − 0,00039932 = 0,00046749, así que EE = 0,0216 y p = 0,043;
  - coincide con la tabla.
- **EE HAC desde la diagonal de `cov_hac`:** const 0,0236; ρ 0,0931; PIB 0,0102. Coinciden con la tabla de coeficientes.
- **Efectos por 1 DE:** β·DE coincide en los cinco (por ejemplo, −0,0163 × 1,778 = −0,029).
- **Recuento «k de n»:** lo rehíce celda a celda desde `model1_robustness_estimates.md` (PIB 3, ΔU 1, π 8, ΔFFR 1, CRED 7, de 9). El criterio sobre p < 0,10 se aplica bien, por ejemplo R4 PIB p = 0,075 «sí» y R7 ΔU p = 0,069 «sí».
- **Nota del Chow 2020T2:** 2020T2–2026T2 son 25 trimestres, menos 4 dummies, quedan 21. La redacción es neutra y el veredicto «falla» se mantiene.
- **Coincidencia entre salidas:**
  - figura de coeficientes = filas «impacto, por 1 DE»;
  - bloque `oos` = `model1_oos.md`;
  - `coef`, `efectos`, `diag`, `robustez` y `variantes_muestra` = sus tablas.
- **Figuras:** 1600×900 px (8×4,5 pulgadas a 200 dpi), sin título y con la fuente.
- **Pre-registro:** `667b313` es anterior a la primera estimación real (`b43430b`). Ninguna corrección de las rondas 1–3 cambió una estimación: solo textos, notas y formato.

## Checklist de la skill y cómo lo comprobé

- [x] **Estacionariedad y regla:** `model1_stationarity.md`. ΔDRALACBS se juzga I(0) con su fila «primera diferencia». Los regresores con forma fija son una desviación pre-registrada (RF-21) y π y CRED se declaran «no I(0)».
- [x] **HAC con la ventana declarada:**
  - el pie dice 4 rezagos, Bartlett, sin corrección;
  - la columna `rezagos_hac` de las robusteces da 4, y 3 en R1 y R7 (T = 98), lo que recalculé con floor(4·(T/100)^(2/9)).
- [x] **Selección de rezagos en la misma muestra:** no aplica, porque los rezagos son fijos y pre-registrados.
- [~] **Signos frente a los esperados:** la columna `coincide` está bien (ΔFFR «no»). La discusión corresponde a la 006.
- [x] **Frases causales:** `grep -i "causa|causal|provoca|debido a"` sobre las tablas `model1_*` y `_variables.yml` no encuentra nada, y el test de RNF-7 pasa.
- [x] **Diagnósticos fallidos reportados:** BP, White, JB, RESET, los dos Chow y la alerta de VIF figuran con su estadístico y su p en la tabla y en las limitaciones, sin atenuantes post hoc. El Chow 2020T2 lleva ya su advertencia pre-registrada.
- [~] **Pipeline idéntico al correrlo dos veces:**
  - lo cubre `test_frozen_model1` (dos `tmp_path`), que pasa;
  - `review-validate.md` documenta dos corridas `all` con SHA-256 idénticos y `git diff --exit-code` en 0;
  - no lo repetí porque no estaba autorizado, y esa validación la escribió el mismo agente que aplicó las correcciones;
  - antes de cerrar, conviene que alguien corra `uv run python -m src.pipeline all` dos veces y `git status --porcelain` sobre HEAD.
- [x] **Coincidencia entre tablas, figuras y variables:** comprobada como se describe arriba.

## Lo que defendería ante el profesor

1. La especificación quedó sellada en `667b313` antes de estimar. C1–C3 son anteriores a los datos reales, y tres rondas de auditoría solo cambiaron textos y formato, nunca una estimación.
2. Toda la inferencia sale de una sola matriz Newey-West con la ventana pre-registrada. El largo plazo usa el método delta, y lo verifiqué a mano contra la covarianza exportada.
3. Se reportan todos los diagnósticos fallidos y la validación fuera de muestra con veredictos fijados de antemano, aunque el dinámico pierde frente al ingenuo y ΔFFR sale con el signo contrario.

## Lo que me preguntaría el profesor

1. «Sus dos únicos regresores significativos, inflación y crédito, no son estacionarios y la dependiente sí. ¿Por qué debo creer esos p-valores en una regresión desbalanceada?»
2. «Su pronóstico dinámico se hunde justo durante las alzas de 2022–2023, y la tasa de la Fed sale con signo negativo. ¿Cómo va a usar este modelo en un escenario adverso con alzas de tasas y varios puntos más de desempleo?»
3. «La guía pregunta cómo *afectan* las condiciones macro, y usted solo habla de asociación, con el Chow de 2008 y el RESET rechazando. ¿Qué afirmación concreta para gestión de riesgos sobrevive a la endogeneidad, la inestabilidad y la no linealidad?»

## Archivos relevantes

- C:\Users\gabri\orca\riesgo-credito-macro\src\model1.py (líneas 464-479, `_variant_note`)
- C:\Users\gabri\orca\riesgo-credito-macro\specs\003-modelo-i\plan.md (líneas 116 y 449)
- C:\Users\gabri\orca\riesgo-credito-macro\specs\003-modelo-i\review-plan.md (línea 36)
- C:\Users\gabri\orca\riesgo-credito-macro\outputs\tables\model1_robustness_estimates.md (y .csv, filas R1)
- C:\Users\gabri\orca\riesgo-credito-macro\outputs\tables\model1_stationarity.md (opcional, formato de p)
- C:\Users\gabri\orca\riesgo-credito-macro\MEMORY.md (opcional, longitud y la cifra 3,1)
