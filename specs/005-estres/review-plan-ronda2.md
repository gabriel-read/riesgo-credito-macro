VEREDICTO: CAMBIOS NECESARIOS

Revisión independiente, **ronda 2**, de la v2 del borrador de spec y plan de la 005 (Estrés), 11-oct-2026. Autor: subagente `revisor-econometrico` de Claude Code, otra instancia que la de la ronda 1, con solo rutas y criterios (sin conclusión de quien redactó la v2). La ronda 1 se conserva en `review-plan-ronda1.md`. Revisión de plan/pre-registro: no se estimó ni proyectó nada con datos reales. Los borradores no están aprobados y esta revisión no los aprueba. Informe copiado tal cual lo entregó el subagente.

**En corto.** La v2 corrige los dos fallos de diseño de la v1. Adopta la adaptación de 13 trimestres con k = 1 medido contra 2025 Q4 de la Fed y usa la distribución marginal en vez de la condicionada. Las identidades, los conteos y el bloque de covarianza son correctos y se pueden comprobar. Aun así, todavía no se puede aprobar, por cuatro motivos:
- Hay requisitos que no se pueden verificar tal como están escritos: la «contribución de la tasa» de RF-10, el escenario al que se aplica RF-12 y las claves `estres.*`.
- Hay una trampa de reproducibilidad: el sha256 de los CSV de la Fed no sobrevive a `core.autocrlf=true`.
- Falta comprobar cómo se arman los regresores del Modelo II.
- Ninguno de los dos borradores recoge dos encargos originales del usuario: arrancar en 2025T4 con el calendario de la Fed y traducir el resultado a dinero con LOANS.

Todo se arregla con texto, sin rediseñar. Lo que depende del autor va aparte al final.

## Qué comprobó y cómo
- **Documentos leídos:** spec y plan v2; review-plan; constitución; guía §7–8; specs 001 (D1), 003 y 004 con sus planes; review-audit de la 004; MEMORY; notas de Codex (compatibilidad, insumos, fuentes); `Plan Macro…md` y `Playbook…md:217`, la instrucción original de `/sdd-spec 005`.
- **JSON, con numpy y sin proyectar:**
  - Bloques sin dummies: 7 términos en el Modelo I (const, y_lag, PIB, ΔU, π, ΔFFR, CRED) y 8 en el II. Asimetría exacta 0.
  - Autovalor mínimo 7,00e-7 (I) y 7,08e-7 (II). Cholesky sin error.
  - P(ρ ≥ 1): 3,0e-5 (I) y 1,76e-4 (II), es decir, unas 0,3 y 1,8 réplicas de cada 10 000.
  - Correlación entre θ0 y θ1: −0,845. `reading.etiqueta` = «sin evidencia».
- **Error de Monte Carlo con N = 200 000:**
  - El error de la media, EE/√N, va de 6e-6 (CRED) a 2,1e-4 (ρ).
  - El error relativo de Frobenius de la covarianza muestral es 0,003 de media y 0,007 como máximo en 20 semillas. La tolerancia de 0,02 se alcanza.
  - Con `default_rng(20261011)` y z de forma (N, k), el z más extremo de las medias es −3,45, dentro de 4.
- **Panel:**
  - Los ΔFFR de 2022T1–2023T3 son 0,04; 0,65; 1,42; 1,46; 0,86; 0,47; 0,27. Todos son mayores que 0 y suman 5,18. Ojo: 2023T4 también es positivo (+0,07).
  - FEDFUNDS en 2026T2 = 3,633; `loans_yoy` en 2026T2 = 7,12; media 2000–2026 = 5,38.
- **Funciones citadas:** `parse_raw`, `quarterly_from_monthly` (con el hueco de oct-2025 en CPI y UNRATE, `src/panel.py:143-187`), `quarterly_from_quarterly`, `yoy` (log, `:292-300`) y `model1.out_of_sample` (devuelve `train_fit` y `test_design`) existen y hacen lo que dice el plan.
- **Fed:** descargó los tres CSV *Final Domestic* y el PDF de escenarios a un directorio temporal, fuera del repo.
  - Las cabeceras traen 18 columnas, entre ellas `Real GDP growth`, `Unemployment rate`, `CPI inflation rate` y `3-month Treasury rate`.
  - Cada escenario trae los 13 trimestres «2026 Q1»–«2029 Q1». El histórico tiene 200 filas, de 1976 Q1 a 2025 Q4, con `Actual,2025 Q4`: desempleo 4,5 y tasa a 3 meses 3,7.
  - **Los CSV no traen unidades.** Las da el PDF («Notes Regarding Scenario Variables»):
    - PIB y CPI: variación trimestral anualizada; la del CPI se mide sobre el promedio trimestral desestacionalizado.
    - Desempleo: promedio trimestral.
    - Letra a 3 meses: promedio trimestral con base de descuento.
    - El PIB de 2025 Q4 es una estimación.
    - Desempleo y CPI de 2025 Q4 promedian noviembre y diciembre, igual que la spec 001.
  - Con eso, las identidades de `spec.md:35-37` son correctas.
- **sha256 de los archivos tal como los sirve la Fed hoy (CRLF):**
  - Historic: `6d08aadcf82d65dcf36b856792040b82ceceef79a46ff0239afd41e0c4e7f653` (16 936 B)
  - Baseline: `76e236695be2c8372890078acf8c01273ba5198a19afb5037045a963737c1bcc` (1 692 B)
  - Severely Adverse: `45c2859ae7246c071b69df8623854751f0629b04393957e14fe28bc33c04ebbb` (1 824 B)
- **Simulación sintética** con coeficientes inventados: Δ por paso k no depende del origen ni de la historia observada; diferencias de 1e-15 con θ = 0 y con θ libre. 1,04^(1/4) = 1,0098534.
- **Tests:** `uv run pytest -q` da 774 passed. No modificó nada del repositorio.

## Estado de los puntos de review-plan (ronda 1)
| # | Estado | Dónde |
|---|---|---|
| 1 Recorte por calendario | Resuelto, con matices (cambios 1 y 5) | spec:29-33, :27, RF-12a :89; plan P9 :67 |
| 2 Condicionada | Resuelto | spec:64-65, :116, RNF-4 :99; plan P2 :60 |
| 3 Identidades | Resuelto. Falta el caso de test π con la base 2025T4 de dos meses | spec:35-36, RNF-3 :98; plan:70 |
| 4 Entradas de `stress` | Resuelto. Menor: usar `load_latest_raw`, no el glob | plan:17; spec:26 |
| 5 S3 opción A | Resuelto: se sustituye por D | spec:49 |
| 6 RF-10(c) | **Parcial**: (c) quitado, pero (b) va sin banda y la «contribución» no está definida | spec:87; plan:51 |
| 7 D-CRED | Resuelto: conteo 4/9, sensibilidad sobre niveles. Falta decir de qué escenario | spec:38, :75, :89 |
| 8 Puntual, pico, comparación | Resuelto. Falta el caso degenerado (cambio 8) | spec:40-41, :53, RF-11 :88 |
| 9 Pre-registros del plan | Resuelto, salvo claves incompletas | spec:63, :97, :99; plan:46, :51, P3 |
| 10 Archivos de la Fed | **Parcial**: faltan los nombres exactos y el sha256 en el plan | plan:20; spec:78-79 |
| 11 RF-5 | Resuelto | spec:82; plan:19 |
| 12–17 | Resueltos | spec:11, :56, :26 y plan:21, :100, RF-14 :91, RF-9 :86 y plan:43 |
| 18 URL | Resuelto en el plan | plan:20 |

## Cambios necesarios
**Importantes**

1. **La adaptación del calendario está justificada contra una alternativa equivocada.** (`spec.md:31`, `:89`; `plan.md:67`)
   - El problema: el Δ por paso k del escenario es *invariante al origen*. Lo observado, el ancla, la constante y el crédito común se cancelan, y la diferencia de los regresores solo depende de los pasos 1..k de la Fed. Por eso la adaptación da exactamente el mismo Δ_m(k) que arrancar en 2025T4 con el calendario de la Fed: solo cambian la etiqueta y los niveles.
   - Esa alternativa, arrancar en 2025T4 «como la Fed (comparable)», es la duda que el usuario dejó planteada (`Playbook…md:217`; `Plan Macro…md:176`), y ninguno de los dos borradores la menciona.
   - Además, RF-12a no es «el calendario original»: es el escenario sin sus dos primeros pasos.
   - **Se espera:**
     - declarar la invariancia y presentar las tres opciones en el [DECIDIR];
     - renombrar RF-12a como «tramo posterior a 2026T2 (sin los dos primeros trimestres del escenario)»;
     - añadir a RNF-5 un test que compruebe que Δ por k no cambia al mover el origen.
   - Este argumento, que no depende de la magnitud del resultado, es la mejor defensa de la adaptación.

2. **RF-10 no se puede verificar.** (`spec.md:87`, `plan.md:39`, `:51`)
   - «Contribución de la tasa mayor que 0» no tiene definición ni trimestre.
   - **Se espera:**
     - definirla como Δ_m^sens(t) − Δ_m^principal(t), réplica a réplica, en 2029T3 y en el trimestre del pico;
     - añadir sus percentiles 5/50/95 (lo pedía la ronda 1, punto 6);
     - completar la firma de `rate_sensitivity`;
     - decir que reemplaza la «diferencia A − B como aporte de la política monetaria» del encargo original, que con la regla vale 0 por construcción.

3. **El sha256 no sobrevive a git.** (`spec.md:78`, `plan.md:20`)
   - Los CSV de la Fed traen CRLF. El repo tiene `core.autocrlf=true` y no hay `.gitattributes`.
   - `data/raw/` ya lo muestra: el archivo de trabajo tiene CR y el blob versionado no.
   - En un clon limpio con LF, la huella cambia (Historic normalizado empieza por `d9ffbbdf…`) y RF-1 detendría el pipeline (principio 1).
   - **Se espera:** que el plan fije `.gitattributes` con `data/scenarios/** -text`, o una huella declarada sobre el contenido con LF normalizado, y un test que lo cubra.

4. **Nombres y huellas de los archivos sin fijar.** (`plan.md:20`, `spec.md:134`)
   - **Se espera** escribir en el plan:
     - los tres nombres oficiales (`2026_Final_Historic_Domestic.csv`, `2026_Final_Supervisory_Baseline_Domestic.csv`, `2026_Final_Supervisory_Severely_Adverse_Domestic.csv`);
     - las huellas de arriba, o las que salgan al congelarlos con la regla del punto 3;
     - los nombres de escenario que valida RF-2: «Supervisory Baseline», «Supervisory Severely Adverse» y «Actual» para el histórico;
     - el PDF de la Fed como fuente de unidades en el manifiesto;
     - una sola ruta: hoy el plan dice `data/scenarios/` y Codex propone `data/scenarios/fed/2026-final/<fecha>/`.

5. **No se comprueba la construcción de regresores del Modelo II.** (`spec.md:82`)
   - RF-5 solo cubre `project` del Modelo I con un X ya construido. Nada prueba que `build_regressors` alinee bien `d_ffr_l1`, `gdp_l1`, `credit_l4` ni los observados en k = 1.
   - **Se espera** un test: con un «escenario» igual a lo observado en una ventana histórica, la matriz de `build_regressors` coincide con `build_design` (003) y con el diseño de la 004, columna por columna.

6. **La descripción de la incertidumbre no es precisa.** (`spec.md:42`)
   - En un modelo lineal, con las mismas innovaciones en todos los escenarios, las innovaciones *se cancelan* en Δ. Solo se omiten en los niveles, y ahí la banda es necesariamente más estrecha que un intervalo de predicción.
   - «No se sabe si sobreestima o subestima» solo vale para las fuentes sin dirección conocida: especificación, escenario, endogeneidad y sesgo del HAC.
   - **Se espera** separar las dos lecturas, la de Δ y la de los niveles.

7. **Claves `estres.*` incompletas o ambiguas.** (`plan.md:51`)
   - `delta_*` no tiene sentido con `esc = base`.
   - `prop_delta_pos` no dice en qué trimestre se mide.
   - Falta la diferencia entre modelos de RF-11.
   - Falta el conteo de trimestres de crédito (4 observados y 9 supuestos).
   - `sens_cal` y `sens_cred` no dicen el escenario ni el trimestre del pico.
   - `fuera_rango` no trae la proporción.
   - Falta el formato de los textos (decimales), que 003 y 004 sí fijaban.
   - Si se decide, faltaría también la traducción a dinero.

8. **La definición del pico tiene un caso degenerado.** (`spec.md:41`)
   - En el Modelo II, Δ(k = 1) = 0. Si Δ ≤ 0 en todo el horizonte, el «máximo con signo» sería 0 en 2026T3.
   - **Se espera:**
     - una regla para empates (el primer trimestre);
     - reportar «sin aumento» cuando max Δ ≤ 0, o reportar también el mínimo.

**Menores**

9. RF-12 (`spec.md:89`): fijar que RF-12a se calcula con la regla θ = 0 y para el adverso principal, y que su «cambio al final» es en 2029T1, no en 2029T3. Reportar también el Δ principal en 2029T1 para comparar. En RF-12b, decir sobre qué escenarios se miden los niveles.

10. RNF-4 (`spec.md:99`, `plan.md:70`): probar con un bloque sintético de parámetros conocidos (principio 4). El Frobenius lo dominan var(ρ) ≈ 8,7e-3 frente a var(CRED) ≈ 7,6e-6, así que conviene añadir una comprobación sobre la covarianza estandarizada (por ejemplo, max |S_ij − V_ij|/√(V_ii·V_jj) < tolerancia).

11. RF-5 y RNF-5 (`spec.md:82`, `:100`): cambiar «exactamente» y «no cambia» por tolerancias (`atol` 1e-12).

12. `plan.md:29` frente a `spec.md:32`: `to_levels` recibe `unrate_origin` pero no el nivel de la tasa, y esos niveles no los usa ningún modelo. O se quitan, o se reportan en RF-3 con una comprobación de que la tasa implícita es ≥ 0. En el adverso queda en 3,633 − 3,6 ≈ 0,03 %, justo encima de cero.

13. `spec.md:49`: decir con qué regla termina el tramo en 2023T3 (trimestre de la última alza, julio de 2023), porque 2023T4 también tiene ΔFFR > 0.

14. `plan.md:11`: `build_design` está en `src/design.py` y `fit_ols_hac` en `src/estimation.py`, no en `model1.py`. Es más simple usar `out_of_sample(...).train_fit`.

15. `plan.md:76`: RF-11, RF-12 y RF-14 apuntan a tareas, no a funciones.

16. `spec.md:96`: la frase «y los archivos … si se aprueba commitearlos aparte» es ambigua. Hay que decir si van en el mismo commit o en otro anterior.

17. `spec.md:28`: es una «letra» del Tesoro, no un «bono». `spec.md:63` y `:69` nombran funciones de numpy, que según la plantilla van en el plan.

18. `spec.md:50`: además del cambio de D, hay que registrar que la adaptación se aparta de «Estrés sobre las fechas de la Fed 2026» (`MEMORY.md:21`) y de `Plan Macro…md:176` («usar sus fechas hace el ejercicio citable y comparable»).

## Pendiente de decisión del autor (no son defectos)
- **Origen:** arrancar en 2025T4 con el calendario de la Fed, o adaptar a 2026T2 (v2). El tramo posterior a 2026T2 queda como sensibilidad. Por el punto 1, Δ es el mismo en las dos primeras opciones.
- **Escenario D:** mantenerlo o descartarlo. Su nombre es honesto. La afirmación de que, con θ = 0, coincide exactamente con el adverso es correcta: solo difieren en las columnas de ΔFFR multiplicadas por 0, y ΔFFR(t−1) en k = 1 es el observado en los dos. No contradice la 004. Sí cambia la decisión de MEMORY del 2-oct y el encargo original («inflación se mantiene alta»).
- **D-CRED:** el último valor (7,12 %, alto para una recesión, pero neutral para Δ) o acortar el horizonte.
- **Traducción a dinero con el saldo de LOANS** (`Plan Macro…md:191`, Playbook): ninguno de los dos borradores la recoge, ni siquiera en «Fuera de alcance». Hay que incluirla o excluirla de forma explícita.
- Autorizar el congelado en `data/scenarios/`, y decidir si se añade una fila de «estimador restringido».

Ninguno de estos puntos exige un cambio SDD de 001, 003 ni 004. D1 de la 001 sigue intacto, porque los archivos se colocan fuera del pipeline y quedan versionados.

## Observaciones (no bloquean)
- Las dos réplicas usan la misma semilla, así que sus z están correlacionados de forma arbitraria. No importa, porque no se calcula ninguna distribución conjunta (RF-11).
- Los signos conocidos permiten anticipar la dirección de RF-10. Con β4 < 0, la caída de la tasa en el adverso *sube* Δ y las alzas de D lo bajan. Conviene decirlo en «Lo que ya se sabía» (`spec.md:11`).
- π también sale significativa en el Modelo II (z ≈ 2,4), además del I.
- Diez tareas caben, pero T4 (lectores, adaptador y equivalencia) es pesada.

## Lo que defendería ante el profesor
- El Δ adverso − base no depende del origen ni de lo observado: arrancar en 2025T4 como la Fed o en 2026T2 da el mismo cambio por trimestre del escenario. Solo cambian las fechas y los niveles.
- La regla de la tasa en cero se commiteó en la 004 antes de estimar. La sensibilidad con los coeficientes estimados va aparte y con el rótulo «sensibilidad, no efecto estimado».
- La incertidumbre es de parámetros, con la distribución marginal HAC, las mismas réplicas en todos los escenarios y Δ calculado réplica a réplica. No se descartan réplicas ni se truncan niveles.

## Lo que preguntaría el profesor
1. Su escenario con alza de tasas da exactamente la misma morosidad que el adverso de la Fed: ¿qué responde entonces a «aumento de la tasa de política monetaria» de la guía?
2. Si el Δ es el mismo arrancando en 2025T4, ¿por qué no usaron las fechas de la Fed, que hacen el ejercicio citable, y qué ganan anclando en 2026T2?
3. ¿Cuánto dinero en préstamos morosos representa el cambio, y por qué morosidad no es pérdida para la planificación de capital (§8)?
