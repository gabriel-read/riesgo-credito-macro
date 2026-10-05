VEREDICTO: CAMBIOS NECESARIOS

# Auditoría de la spec 003 (Modelo I), ronda 2

Leí spec.md, plan.md, tasks.md, review-plan.md, review-audit.md (ronda 1), review-validate.md, MEMORY.md, las 9 tablas `outputs/tables/model1_*` (.md), `outputs/models/model1_main.json`, las tres figuras PNG, el bloque `modelo1:` de `report/_variables.yml` y el diff sin commitear de `src/` y `tests/`. `uv run pytest -q` da **481 passed** (solo avisos de deprecación de statsmodels). No ejecuté el pipeline porque no me indicaron ninguna etapa, y no edité ningún archivo.

**Las 7 correcciones de la ronda 1 están bien aplicadas y aparecen en las salidas regeneradas:**
- El Chow ya no lleva la atenuante.
- La tabla de efectos tiene pie con las DE, la muestra C1 y la lectura del largo plazo.
- `terminos_diferencia` dice «sustituye» en R4, R6 y R7, y la tabla resumen tiene su nota.
- El texto del VIF de ΔU está corregido.
- Las métricas fuera de muestra van con 3 decimales e iguales en la tabla y en las variables.
- La etiqueta de R2 está corregida.
- Los Chow usan el formato AAAAT#.

No encontré errores de estimación ni de inferencia. Lo que sigue bloqueando son dos incumplimientos menores del plan aprobado. Uno de ellos el propio plan da por incorporado sin que lo esté. Aplico el mismo listón que la ronda 1, que bloqueó por cosas del tamaño de «2008Q3».

## Cambios necesarios

**Menores**

1. **Falta la advertencia de tamaño del Chow 2020T2 que pre-registra el plan.**
   - Dónde: `src/diagnostics.py:323-326` escribe la misma nota para los dos quiebres. Se ve en `outputs/tables/model1_diagnostics.md` (fila «Chow 2020T2») y en `modelo1.limitaciones`.
   - Qué incumple:
     - `plan.md:167-168` dice: «En 2020T2 quedan ~21 trimestres posteriores útiles para 7 restricciones: la nota advierte que el tamaño real puede apartarse del 5 %».
     - Lo pidió `review-plan.md:40`, y `plan.md:448` (sección 12) lo da por «incorporado», pero no está en el código. `git log -S "apartarse"` no lo encuentra en ninguna versión de `src/`. No es lo que quitó la corrección 1 (aquella frase sí era post hoc y con dirección); esta nunca se implementó.
   - Por qué importa: el Chow 2020T2 rechaza por poco (W = 15,155, p = 0,034). Después de 2020T2 hay 25 trimestres, pero 4 los absorben las dummies de impulso. Los 21 que identifican las 7 interacciones incluyen los puntos de alto apalancamiento de 2021T2–2022T1 (cambio C2). La spec 006 necesita esa advertencia escrita, porque no puede teclearla a mano.
   - Qué se espera, una de dos:
     - (a) Implementar la nota tal como está en el plan, con el número de trimestres útiles calculado por código. La redacción debe ser neutra («el tamaño real puede apartarse del 5 %», sin decir en qué dirección) y el veredicto «falla» se mantiene. Añadir un test.
     - (b) Si no se quiere esa nota, anotar en el plan que se elimina y por qué. En ese caso hay que corregir la fila «Opc.» de `plan.md:448`.

2. **El plan no recoge las claves y la columna nuevas.**
   - Dónde:
     - `report/_variables.yml:151,173,195,217,239` (`efectos.<regresor>.de`) y `:260` (`efectos_nota`);
     - `variantes_muestra.<id>.motivo` (`:332-386`);
     - la columna `de` de `model1_effects.csv`.
   - Qué incumple: el plan §4 (`plan.md:304-334`) fija las claves exactas de RF-22 («las claves exactas se fijan en el plan»). Ninguna de estas figura en él, y la tabla de salidas (`plan.md:277`) tampoco menciona la columna `de`.
   - Qué se espera: una enmienda menor en el plan, como la de D12. Ahí se fijan las claves que la spec 006 va a citar.

**Procedimiento (necesario para cerrar, no es un fallo del trabajo)**

3. **Todas las correcciones están sin commitear**, y en el mismo árbol está el PNG regenerado de la spec 001 (`outputs/figures/delinquency_unemployment_ffr.png`, de 128 314 a 134 153 bytes).
   - El código de la 003 no afecta a esa figura: `src/figures.py` solo añadió funciones nuevas. La diferencia sale del entorno. Por eso conviene commitearlo aparte, con un mensaje que lo diga y una línea en `MEMORY.md`.
   - Ahora mismo RNF-5 solo se cumple frente al árbol de trabajo, no frente a HEAD.
   - Observación, fuera del alcance de la spec: `review-validate.md:54` y `.python-version` dicen Python 3.11.17, y `AGENTS.md` dice 3.12. Hay que alinear uno de los dos.

## Opcional (no bloquea)
- **Etiqueta «ΔPIB»** (`src/model1_config.py:78`). Ahora también aparece en `efectos_nota` («ΔPIB = 1,778»), que el informe va a citar. Una Δ hace pensar en una diferencia trimestral, cuando es una variación interanual (la spec la llama «PIB(t)»). Sugiero «PIB (var. interanual)».
- **Dummies COVID:** su p e IC siguen visibles aunque el EE «no es informativo», porque omite σ² del trimestre. Mostrar «—» en p e IC, o que la spec 006 no los interprete nunca. Por ejemplo, el p = 0,082 de 2021T1 no significa nada.
- **«sustituye: gdpc1_yoy → gdp_yoy»** usa nombres de columna de FRED, mientras la sustitución de CRED usa etiquetas legibles. Sugiero «PIB real → PIB nominal».
- **Filas del VIF** con identificadores en inglés («VIF (d_unemp)») dentro de una tabla en español (RNF-8). Además, el texto especial está atado al nombre del término (`src/model1.py:694`): si los datos cambiaran, se imprimiría sin que nada lo compruebe.
- **White:** reportar sus grados de libertad. Por D5, rango(Z_aux) − 1 no es obvio y es lo que hace creíble el rechazo.
- **Pendientes de la ronda 1:**
  - marcar el hueco de 2020T2–2021T1 en el CUSUM;
  - dibujar el ingenuo constante en `model1_oos.png`, porque es el comparador del dinámico y el que le gana;
  - poner «≥ 0,10» en el KPSS y «< 0,001» en el ADF de `model1_stationarity.md`.

## Comprobaciones hechas a mano (coinciden)
- **Largo plazo de ΔFFR con la `cov_hac` del JSON:**
  - b = −0,04384, ρ = 0,62649;
  - gradiente [2,6773; −0,3142];
  - Var = 0,011294 + 0,000855 − 0,003672 = 0,008477, así que EE = 0,092. La tabla da −0,117 con EE 0,092.
- **Largo plazo y efectos por 1 DE de los cinco regresores:** coinciden con β/(1 − ρ) y con β·DE.
- **Ventana HAC:** T = 106 da 4 rezagos; 102 da 4; 98 (R1 y R7) da 3.
- **p-valores de los estadísticos:**
  - BG LM 3,252 con χ²(4) da p ≈ 0,52;
  - Chow 15,155 con χ²(7) da p ≈ 0,034, y 24,987 da p < 0,001;
  - BP 21,981 con χ²(10) da p ≈ 0,015;
  - RESET F(2, 93) = 6,021 da p ≈ 0,003.
- **Bandas del CUSUM:** n′ − k′ = 95 da ±0,948·√95 ≈ ±9,24 al inicio y ≈ ±27,5 al final, igual que la figura. Descartar el primer punto de `rcusum` es correcto: es el residuo del ajuste exacto inicial, que vale ≈ 0.
- **Recuentos «k de n»:** los recalculé celda a celda desde `model1_robustness_estimates.md` y coinciden.
- **Figuras y variables frente a las tablas:**
  - el gráfico de coeficientes coincide con las filas «impacto, por 1 DE»;
  - el bloque `modelo1.oos` coincide con `model1_oos.md`;
  - `modelo1.coef` y `modelo1.efectos` coinciden con sus tablas.
- **Pre-registro:** el commit `667b313` solo contiene `specs/003-modelo-i/`. La primera estimación real está en `b43430b`, posterior al plan y a C1–C3.

## Lo que deben heredar las specs 005 y 006 (además de lo de la ronda 1, que sigue vigente)
- **ΔU tiene todavía menos variación propia de la que se dijo.** El VIF de 36,8 se descompone así, de forma aproximada y a partir de las salidas:
  - Las dummies explican un factor de unas 12 veces: la varianza total de ΔU es unas 12 veces la de fuera de la COVID, con DE de 0,308 pp.
  - El resto, un factor de unas 3, es colinealidad real con el PIB y los demás regresores (Okun), que explican unos 2/3 de ΔU fuera de la COVID.
  - Así, el coeficiente de ΔU se identifica con unos 0,18 pp de variación propia por trimestre. Un escenario adverso con saltos de varios pp de desempleo extrapola muy lejos.
- **PIB «3 de 9» robusto:** su coeficiente principal no es significativo ni al 10 % (p = 0,110). El criterio pre-registrado lo permite, pero la 006 no debe leer ese recuento como evidencia de robustez.
- **«Supera al ingenuo» a un paso** (cociente 0,978) siempre debe ir junto a «no significativo» (DM p = 0,937). Nunca solo.
- **Inflación y crédito:** el texto de la limitación «Regresores no I(0)» no dice qué implica para la inferencia. Esos son justo los dos coeficientes con p < 0,05, y la 006 debe decirlo junto al hallazgo.

## Checklist de la skill y cómo lo comprobé
- [x] **Estacionariedad y regla de transformación:** revisé `model1_stationarity.md`. La dependiente sigue la regla (ΔDRALACBS I(0) en su fila «primera diferencia»). Los regresores con forma fija son una desviación pre-registrada y declarada en RF-21.
- [x] **Errores HAC y ventana declarada:** pie de coeficientes (4 rezagos, Bartlett, sin corrección), columna `rezagos_hac` de las robusteces, y recalculé la ventana a mano.
- [x] **Selección de rezagos en la misma muestra:** no aplica, porque los rezagos son fijos y pre-registrados.
- [~] **Signos frente a los esperados:** la tabla trae la coincidencia, con ΔFFR «no». Discutirla corresponde a la 006.
- [x] **Frases causales:** leí todas las tablas y las variables, `grep` de «causa|provoca|debido a» no encuentra nada, y el test de RNF-7 pasa.
- [~] **Diagnósticos fallidos reportados y discutidos:** todos están reportados con estadístico y p, y el texto del VIF ya es correcto. Falta la nota de tamaño del Chow 2020T2 (punto 1). Discutirlos es tarea de la 006.
- [~] **Pipeline idéntico dos veces:** pasa el test con dos `tmp_path`, y `review-validate.md` documenta dos corridas `all` con SHA-256 idénticos. No pude repetirlo porque no estaba autorizado. Frente a HEAD falta commitear (punto 3).
- [x] **Coincidencia entre tablas, figuras y variables:** sí, comprobada como se describe arriba.

## Lo que defendería ante el profesor
1. La especificación quedó sellada en `667b313` antes de estimar. C1–C3 son anteriores a los datos reales, y ninguna corrección posterior cambió una estimación: solo textos y formato.
2. Toda la inferencia sale de una sola matriz Newey-West con la ventana pre-registrada. El largo plazo usa el método delta, y lo verifiqué a mano sobre la covarianza exportada.
3. Se reportan todos los diagnósticos fallidos (BP, White, JB, RESET y los dos Chow), y el veredicto fuera de muestra se fijó antes de verlo, aunque no favorece al modelo dinámico.

## Lo que me preguntaría el profesor
1. «Sus dos únicos regresores significativos, inflación y crédito, son los que no pasan la prueba de estacionariedad. ¿Por qué debo creer esos p-valores?»
2. «El coeficiente del desempleo se identifica con variaciones de unas décimas de punto por trimestre, y la tasa de la Fed sale con signo negativo. ¿Cómo justifica usar este modelo para un escenario adverso de varios puntos de desempleo y alzas de tasas?»
3. «El Chow rechaza en 2008 y en 2020, y el RESET también. ¿Qué parte de sus conclusiones sobrevive a la inestabilidad de parámetros y a la no linealidad?»
