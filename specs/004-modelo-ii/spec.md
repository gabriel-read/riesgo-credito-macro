# Spec 004 — Modelo II: política monetaria y deterioro posterior de la cartera
Estado: aprobada · Crítica: sí

## Contexto y objetivo
La guía pide un segundo modelo que responda si un cambio de la política monetaria tiene relación con el deterioro posterior de la calidad de la cartera y si existen efectos rezagados. Esta spec fija ese modelo **antes de ver ningún resultado del Modelo II** (pre-registro, principio 2 de la constitución): variables, rezagos y su criterio de selección, estimador, definición de los efectos, regla de lectura de la evidencia, prueba de Granger, proyecciones locales, robusteces y diagnósticos.

Objetivo: estimar por MCO con errores Newey-West un modelo de rezagos distribuidos de la variación de la morosidad (DRALACBS) sobre el cambio de la tasa de fondos federales de t a t−K, con K elegido por BIC entre 1 y 8 sobre una misma muestra efectiva; reportar los efectos acumulados con prueba de Wald HAC, la trayectoria de la respuesta, el trimestre de efecto máximo y la prueba de Granger; leer la evidencia con una regla fijada de antemano; y contrastar la respuesta con proyecciones locales de Jordà (h = 0..12). Los resultados son asociaciones dinámicas, no efectos identificados de la política monetaria.

**Lo que ya se sabía al redactar.** Esta spec se escribió conociendo los resultados del Modelo I (spec 003): ΔFFR contemporáneo con signo negativo y sin significancia, π y CRED(t−4) como únicos coeficientes con p < 0,05, ρ = 0,63, y los dos Chow rechazando. Las decisiones que pueden haber estado condicionadas por ese conocimiento son: sacar θ₀ de la prueba de Granger (es la definición estándar), rezagar los controles macro, la robustez R3 sin tramos de tasa cero y la hipótesis H2. La regla de lectura de la evidencia, la definición del trimestre de efecto máximo y la regla heredada por la spec 005 se fijaron tras la revisión de clarificación y **antes de estimar nada del Modelo II**; el commit de esta spec es la prueba.

## Pregunta que responde (y sección de docs/guia-profesor.md que cubre)
¿Cómo afectan los cambios en la política monetaria al riesgo de crédito y existen efectos rezagados sobre la calidad de la cartera? Cubre la sección 5 (Modelo II) y aporta los resultados de la 6.2 y los insumos cuantitativos de la 6.3. La comparación narrativa de los dos modelos, la interpretación y la discusión se redactan en la spec 006.

Frontera con otras specs:
- **Modelo I (spec 003):** mide la asociación contemporánea de la morosidad con el conjunto de condiciones macro del trimestre. El Modelo II estudia la respuesta dinámica y rezagada de la morosidad a la tasa, con los controles macro rezagados.
- **Estrés (spec 005):** usa los coeficientes exportados y hereda la regla de la sección «Regla que hereda la spec 005».
- **Spec 006:** compara los dos modelos en 6.3 con los insumos de RF-27.

## Usuarios
- El autor, que redacta las secciones 3.5, 5 y 6.2 del informe con las salidas de esta spec.
- La spec 005 (estrés), que usa los coeficientes y la covarianza HAC exportados y la regla heredada.
- La spec 006, que compara los dos modelos en 6.3.
- El revisor econométrico (auditoría crítica) y el profesor evaluador.

## Historias de usuario
- HU-1. Como autor, quiero una especificación fijada y commiteada antes de estimar para demostrar que no elegí el modelo según los resultados.
- HU-2. Como autor, quiero que K salga de una regla pre-registrada (BIC, con AIC como robustez) para que el número de rezagos no dependa de lo que me gustaría ver.
- HU-3. Como autor, quiero los efectos acumulados con su prueba, la trayectoria, el trimestre de efecto máximo y una regla de lectura fijada de antemano para responder si hay efectos rezagados sin elegir la conclusión después de ver los datos.
- HU-4. Como autor, quiero proyecciones locales, que no imponen la forma paramétrica del modelo de rezagos distribuidos, para describir cómo se compara la respuesta de ambos enfoques, sabiendo que miden objetos distintos.
- HU-5. Como revisor, quiero todos los diagnósticos y los límites declarados (endogeneidad de la tasa, tramos de tasa cero, COVID) para juzgar la validez de las conclusiones.
- HU-6. Como autor de la spec 005, quiero los coeficientes, la covarianza, la trayectoria y la lectura de la evidencia exportados para usarlos sin reestimar.

## Definiciones
- **Panel, trimestre, historia descargada, variación interanual y regla de decisión niveles/diferencias**: los de la spec 001.
- **Historia transformada, inicio efectivo, ventana HAC, distribución de referencia, «significativo», dummy de impulso, tratamiento de la matriz HAC (comprobación en el bloque sin dummies de impulso), veredicto «pasa/falla» de cada diagnóstico y «alerta» del VIF, regla de cruce de bandas del CUSUM y «Tabla de estacionariedad»**: los de la spec 003, aplicados a cada regresión de esta spec. En la tabla de estacionariedad, una serie que entra en primera diferencia se juzga con la fila «primera diferencia» de la spec 001 y una que entra tal cual, con la fila «tal cual».
- **Y (dependiente)**: la variación trimestral de DRALACBS en pp, ΔDR(t) = DR(t) − DR(t−1), calculada sobre la historia transformada. Entra en diferencia porque la tabla de estacionariedad de la spec 001 la clasifica «ambigua (primera diferencia)».
- **ΔFFR(t)**: la diferencia trimestral de la tasa de fondos federales en pp (columna de la spec 001), calculada sobre el promedio trimestral de FEDFUNDS.
- **Shock de 1 pp**: un aumento de 1 pp del promedio trimestral de la tasa en un trimestre, es decir, ΔFFR(0) = +1 una sola vez, que deja la tasa 1 pp más alta en adelante. Es una variación observada de la tasa, no un shock monetario identificado.
- **Tramo de tasa cero**: trimestre con el promedio trimestral de FEDFUNDS ≤ 0,25 %. La definición es por regla, no por fechas. A la fecha de esta spec son 36 trimestres: 2009T1–2015T4 y 2020T2–2022T1.
- **Muestra efectiva común (M)**: del primer trimestre en que existen todos los términos del modelo con K = 8 (ΔFFR(t−8), ΔDR(t−1), PIB(t−1), ΔU(t−1), π(t−1) y CRED(t−4)) al último trimestre común de la spec 001. A la fecha es 2000T2–2026T2, 105 trimestres. Una sola muestra se usa para comparar todos los K y para el modelo principal.
- **AIC y BIC**: AIC = −2·lnL + 2·k y BIC = −2·lnL + k·ln(T), con lnL la log-verosimilitud gaussiana de MCO, k el número de parámetros (incluidas las dummies) y T las observaciones de M.
- **Multiplicadores ψ_h**: la respuesta de ΔDR (el cambio trimestral de la morosidad) h trimestres después de un shock de 1 pp: ψ₀ = θ₀; ψ_h = θ_h·1{h ≤ K} + ρ·ψ_{h−1} para h ≥ 1.
- **Respuesta acumulada R(h)**: la respuesta del **nivel** de la morosidad (pp) h trimestres después de un shock de 1 pp, con h = 0..12: R(h) = ψ₀ + … + ψ_h. Mantiene fijos la tasa posterior y los controles.
- **Efectos acumulados**: S = θ₀ + θ₁ + … + θ_K (acumulado total, con el coeficiente del mismo trimestre) y S_rez = θ₁ + … + θ_K (acumulado rezagado, sin θ₀). Ambos en pp de morosidad por 1 pp; no incorporan la dinámica de ρ (la recoge R(h)).
- **Trimestre de efecto máximo h\***: el h ∈ {0, …, 12} con mayor |ψ_h|, es decir, el trimestre en que es mayor el cambio trimestral de la morosidad tras el shock; si hay empate, el menor. Se reporta con el signo de ψ_h\*. R(h) se reporta pero no define h\*.
- **Trimestres útiles de un quiebre**: los de la muestra anteriores (o posteriores) al quiebre menos los que absorben las dummies de impulso.
- **Lenguaje de asociación**: «precede», «anticipa», «se asocia con». «Shock de 1 pp», «respuesta», «efecto acumulado» y «efecto máximo» son nombres técnicos de cantidades del modelo y se leen como asociaciones condicionales. Granger mide precedencia temporal.

## Especificación pre-registrada

### Variables y transformaciones
| Término | Serie | Forma | Unidad |
|---|---|---|---|
| ΔDR(t) | DRALACBS | diferencia trimestral | pp |
| ΔDR(t−1) | DRALACBS | la misma forma, rezagada un trimestre | pp |
| ΔFFR(t−j), j = 0..K | FEDFUNDS | diferencia trimestral, rezagada j trimestres | pp |
| PIB(t−1) | GDPC1 | variación interanual, rezagada un trimestre | % |
| ΔU(t−1) | UNRATE | diferencia trimestral, rezagada un trimestre | pp |
| π(t−1) | CPIAUCSL | variación interanual, rezagada un trimestre | % |
| CRED(t−4) | LOANS | variación interanual, rezagada 4 trimestres (como en el Modelo I) | % |
| D(k) | — | una dummy por trimestre: 2020T2, 2020T3, 2020T4 y 2021T1 | 0/1 |

Los controles macro son los del Modelo I. PIB, ΔU y π se rezagan un trimestre para no condicionar sobre variables macro del mismo trimestre, que pueden ser consecuencia de la tasa (canales de transmisión). El coste es que ΔFFR(t) conserva la reacción de la Fed a la macro del mismo trimestre, así que θ₀, S y los β_h pueden arrastrar esa endogeneidad (se declara como limitación). El crédito conserva su rezago de 4 trimestres, que ya es mayor que uno y mantiene la justificación de maduración de la cartera y la comparabilidad con el Modelo I. Los regresores entran en la forma fija de esta tabla; su no estacionariedad residual (π y CRED(t−4) figuran «no I(0)» en la spec 001) se declara como limitación.

### Ecuación (especificación principal)
ΔDR(t) = α + ρ·ΔDR(t−1) + Σ_{j=0..K} θ_j·ΔFFR(t−j) + γ₁·PIB(t−1) + γ₂·ΔU(t−1) + γ₃·π(t−1) + γ₄·CRED(t−4) + Σₖ δₖ·D(k) + ε(t)

### Selección de K
K se elige entre 1 y 8 estimando un modelo por cada K sobre la muestra M, con el mismo resto de la ecuación. K_BIC es el K de menor BIC y K_AIC el de menor AIC; si hay empate, el menor K. **La especificación principal usa K_BIC.** Si K_AIC ≠ K_BIC, el modelo con K_AIC es la robustez R1. Los K de las demás robusteces son el de la principal; no se vuelve a elegir K en ninguna variante.

### Estimador y errores estándar
MCO con errores Newey-West (ventana y tratamiento de la matriz HAC de la spec 003). Inferencia con la normal.

### Efectos acumulados, trayectoria y Granger
- **Efectos acumulados:** Wald HAC de H0: S = 0 y de H0: S_rez = 0, cada uno χ²(1), con la estimación, su error HAC, p e IC 95 %.
- **Trayectoria:** ψ_h y R(h) para h = 0..12, solo estimación puntual (sin bandas; las bandas de la respuesta las da la proyección local).
- **Granger:** Wald HAC de H0: θ₁ = … = θ_K = 0, χ²(K). Se excluye θ₀ (el coeficiente del mismo trimestre es simultáneo). La dirección inversa (de la morosidad a la tasa) queda fuera de alcance.

### Hipótesis y regla de lectura de la evidencia (pre-registradas)
- **H1 (signo):** S > 0. Mecanismo: tasas más altas encarecen el servicio de la deuda y endurecen las condiciones financieras, y la mora aparece con retraso. Se reporta «sí» o «no» según el signo puntual y, aparte, «respaldada» si además el Wald de S tiene p < 0,05.
- **H2 (rezago):** h\* ≥ 1, es decir, el cambio trimestral máximo de la morosidad no ocurre en el mismo trimestre.
- **Lectura de «¿hay efectos rezagados?»**, solo con lo rezagado: la condición C1 es que Granger rechaza al 5 %; la condición C2 es que S_rez > 0 con p < 0,05 en el Wald HAC.
  - «Evidencia fuerte»: se cumplen C1 y C2.
  - «Evidencia parcial»: se cumple una de las dos.
  - «Sin evidencia»: no se cumple ninguna.
  - Si S_rez < 0 con p < 0,05, el resultado lleva además la marca «signo contrario al esperado».
- Los coeficientes individuales θ_j y los controles no tienen hipótesis de signo. Un resultado distinto de lo esperado se reporta tal cual y no cambia la especificación.

### Regla que hereda la spec 005
La spec 005 no atribuirá al alza de tasas un efecto estimado distinto de cero salvo que la lectura de esta spec sea «evidencia fuerte». Si no lo es, el escenario se corre con el efecto de la tasa igual a cero en todos los modelos del estrés y se reporta aparte la sensibilidad con el coeficiente puntual. Un signo contrario al esperado nunca se usa como efecto estimado.

### Proyecciones locales
Dos familias de regresiones por horizonte h = 0..12, con el mismo regresor de interés ΔFFR(t) y los mismos controles: ΔDR(t−1), PIB(t−1), ΔU(t−1), π(t−1), CRED(t−4), ΔFFR(t−1..t−K) con el K del modelo principal y las dummies COVID fechadas en t.
- **Respuesta de la morosidad:** dependiente DR(t+h) − DR(t−1) (pp, nivel acumulado). El coeficiente de ΔFFR(t) es β_h.
- **Respuesta de la tasa:** dependiente FFR(t+h) − FFR(t−1) (pp, nivel de la tasa trimestral). El coeficiente de ΔFFR(t) es φ_h, la trayectoria de la tasa asociada a un cambio de 1 pp.
- Ventana HAC: max(la fórmula de la spec 003 con las T de ese horizonte, h + 1). Muestra: del inicio de M al último trimestre común menos h trimestres. Banda al 90 %: estimación ± 1,6449·EE.
- **Horizonte de detección:** el primer h cuya banda del 90 % de β_h excluye el cero; si ninguno, «ninguno». Es descriptivo.

### Naturaleza de la comparación
β_h y R(h) son objetos distintos. R(h) mantiene fijos la tasa posterior y los controles; β_h incluye la trayectoria posterior de la tasa (φ_h) y la reacción de los controles. La comparación entre ambos es descriptiva y no es una prueba de la forma paramétrica. En h = 0 coinciden por construcción (β₀ = θ₀ = R(0)), y cada horizonte usa su propia muestra.

### Pruebas de robustez previstas
- **R1.** Modelo con K_AIC (solo si K_AIC ≠ K_BIC).
- **R2.** Sin 2020–2021: excluye 2020T1–2021T4 y no lleva dummies COVID.
- **R3.** Sin tramos de tasa cero: excluye los trimestres con promedio de FEDFUNDS ≤ 0,25 % y no lleva dummies COVID (a la fecha, las cuatro caen dentro de un tramo de tasa cero).
- **Proyecciones locales** (arriba).
- En R2 y R3 los rezagos siguen saliendo de la historia transformada, y la ventana HAC trata como contiguos los trimestres vecinos de cada exclusión.
- **Criterio de robustez:** el de la spec 003 aplicado a S_rez (mismo signo que la principal y p < 0,10 con errores HAC); se reporta también S. «Robusto» no implica que la principal sea significativa: la tabla trae el p de la principal.

### Diagnósticos
Sobre la especificación principal: Breusch-Godfrey con 4 rezagos (LM), Breusch-Pagan (Koenker), White (con eliminación de colinealidad por rango), Jarque-Bera, RESET (potencias 2 y 3 de los valores ajustados, F), VIF de cada regresor excepto la constante y las dummies, Chow en 2008T3 y 2020T2 como Wald HAC con interacciones de todos los términos que no son dummies de impulso, y CUSUM de residuos recursivos sobre la regresión sin dummies de impulso ni sus trimestres.

## Requisitos funcionales

### Datos, muestra y forma de la dependiente
- RF-1: EL SISTEMA construirá todas las variables, rezagos y diferencias sobre la historia transformada y recortará después cada muestra de estimación.
- RF-2: EL SISTEMA leerá de la tabla de estacionariedad de la spec 001 la decisión de DRALACBS y, SI no es «ambigua (primera diferencia)», ENTONCES se detendrá con un error que nombre la serie y las dos formas. Continuar exige un `/sdd-change` de esta spec.
- RF-3: EL SISTEMA calculará la muestra efectiva común M y la reportará (primer y último trimestre y número de observaciones) en el pie de las tablas de selección y de coeficientes.
- RF-4: SI falta algún término dentro de la muestra de una regresión, después de su inicio efectivo, ENTONCES EL SISTEMA se detendrá con un error que nombre la variable, el trimestre y la regresión, sin imputar ni eliminar filas en silencio.

### Selección de K y estimación principal
- RF-5: EL SISTEMA estimará, sobre la muestra M, un modelo por cada K = 1..8 y calculará su AIC y su BIC. SI alguno de esos modelos o la especificación principal tiene menos de 30 grados de libertad o rango incompleto, ENTONCES EL SISTEMA se detendrá con un error que nombre el K.
- RF-6: EL SISTEMA elegirá K_BIC y K_AIC según la regla de selección y usará K_BIC en la especificación principal. SI K_AIC ≠ K_BIC, ENTONCES el modelo con K_AIC será la robustez R1; SI coinciden, ENTONCES R1 figurará como «no aplica: AIC y BIC eligen el mismo K».
- RF-7: EL SISTEMA producirá una tabla de selección con, por K: número de parámetros, observaciones, AIC, BIC y la marca de los K elegidos. SI K_BIC o K_AIC es 8, ENTONCES lo declarará como limitación indicando cuál (el óptimo puede estar fuera del rango) sin ampliar el rango.
- RF-8: EL SISTEMA estimará la especificación principal por MCO con errores Newey-West y producirá una tabla de coeficientes con, por término: coeficiente, error HAC, z, p, IC 95 % y la nota de las dummies de impulso. El pie traerá: K elegido y criterio, forma de Y, muestra M, observaciones, parámetros, R² y R² ajustado, error estándar de la regresión, rezagos de la ventana HAC, si se aplicó truncamiento espectral al bloque sin dummies de impulso y la nota «rango reducido por dummies de impulso (esperado)».
- RF-9: EL SISTEMA producirá un gráfico del perfil de coeficientes θ_j (j = 0..K) con su IC 95 % HAC y una línea en cero, con ejes y títulos en español y el pie de fuente.

### Efectos acumulados, trayectoria, Granger y lectura
- RF-10: EL SISTEMA producirá una tabla de efectos acumulados con S y S_rez, cada uno con su error HAC, el estadístico χ²(1), el p-valor y el IC 95 %, en pp de morosidad por 1 pp, y con H1 («sí» o «no» y «respaldada» o «no respaldada»).
- RF-11: EL SISTEMA producirá una tabla de la trayectoria con ψ_h y R(h) para h = 0..12, el h\* con su signo y H2. El pie dirá que la trayectoria no lleva bandas y que las bandas están en la proyección local. SI |ρ̂| ≥ 1, ENTONCES el pie avisará de que la dinámica es explosiva; SI ρ̂ ≥ 0,95, ENTONCES avisará de que R(h) es muy sensible a ρ.
- RF-12: EL SISTEMA producirá la prueba de Granger con el estadístico χ²(K), el p-valor y el veredicto («rechaza» o «no rechaza» al 5 %), descrita como precedencia temporal.
- RF-13: EL SISTEMA producirá la lectura de la evidencia («evidencia fuerte», «evidencia parcial» o «sin evidencia») con el estado de C1 y C2 y la marca «signo contrario al esperado» cuando corresponda, redactada sin lenguaje causal.

### Proyecciones locales
- RF-14: EL SISTEMA estimará la proyección local de la respuesta de la morosidad por cada h = 0..12 y producirá una tabla con, por h: β_h, error HAC, banda del 90 %, observaciones, rezagos HAC y estado.
- RF-15: EL SISTEMA estimará la proyección local de la respuesta de la tasa por cada h = 0..12 y añadirá a la tabla φ_h, su error HAC y su banda del 90 %.
- RF-16: SI en un horizonte quedan menos de 30 grados de libertad o los regresores tienen rango incompleto, ENTONCES EL SISTEMA reportará ese horizonte como «no estimada» con su motivo, sin afectar a los demás.
- RF-17: EL SISTEMA producirá una tabla de comparación descriptiva con, por h: R(h), β_h, φ_h, si R(h) y β_h tienen el mismo signo y si la banda del 90 % de β_h excluye el cero. Traerá el recuento «k de n» de los horizontes h = 1..12 con el mismo signo (n cuenta solo los estimados; h = 0 queda fuera porque coincide por construcción) y el horizonte de detección. El pie dirá que β_h y R(h) son objetos distintos y que la comparación es descriptiva.
- RF-18: EL SISTEMA producirá un gráfico con dos paneles: la respuesta acumulada de la morosidad (β_h con su banda del 90 % y R(h) superpuesta) y la respuesta de la tasa (φ_h con su banda), con ejes y leyenda en español y el pie de fuente.

### Diagnósticos y estacionariedad
- RF-19: EL SISTEMA producirá la tabla de diagnósticos con estadístico, p-valor y veredicto de cada prueba (con las reglas de veredicto de la spec 003 para el CUSUM y el VIF, que no tienen p), y el gráfico CUSUM con bandas al 5 %.
- RF-20: La nota de cada fila de Chow indicará los trimestres útiles anteriores y posteriores al quiebre, calculados por código. SI los posteriores son menos de 30, ENTONCES la nota añadirá, sin dirección: «el tamaño empírico del contraste puede diferir del 5 % nominal». SI el bloque de interacciones tiene rango incompleto, ENTONCES la fila figurará como «no calculable» con su motivo y sin veredicto. En los demás casos, el veredicto sigue a p.
- RF-21: EL SISTEMA producirá una tabla de estacionariedad del modelo con ΔDR, ΔFFR y los cuatro controles en la forma en que entran, con el ADF y el KPSS copiados de la tabla de la spec 001, su decisión y su orden de integración, y la marca «no I(0)». El ADF se escribe «< 0,001» si procede y el KPSS truncado de statsmodels se escribe «> 0,10» o «< 0,01», como en la spec 001; los CSV conservan los valores.

### Robusteces
- RF-22: EL SISTEMA estimará R1, R2 y R3 con el mismo estimador y las mismas reglas y producirá una tabla con, por variante: K, muestra y observaciones, rezagos HAC, S y S_rez con su error HAC y el p de Wald, el h\* y H1; o el estado «no estimada» con su motivo; o «no aplica» (R1 cuando K_AIC = K_BIC).
- RF-23: SI una variante tiene menos de 30 grados de libertad o rango incompleto, ENTONCES EL SISTEMA la reportará como «no estimada» con su motivo. SI una dummy COVID no tiene variación en la muestra, ENTONCES se omite solo en R2 y R3 y en cualquier otra regresión es un error.
- RF-24: EL SISTEMA producirá una tabla resumen de robustez de S_rez con «sí», «no», «no estimada» o «no aplica» por variante según el criterio pre-registrado (las dos últimas no entran en el denominador) y el p de la principal. Su pie dirá: el criterio, el K de cada variante, las exclusiones de R2 y R3 y, calculados por código, los trimestres cuyos rezagos salen de trimestres excluidos.

### Límites, desviaciones, comparación y variables del informe
- RF-25: EL SISTEMA producirá una tabla de limitaciones con las fijas y las detectadas por código.
  - **Fijas:**
    - la endogeneidad de la tasa de fondos federales (la Fed reacciona a la economía), agravada porque los controles van rezagados;
    - que ΔFFR es una variación observada y no un shock identificado, por lo que la asociación no identifica el efecto de la política monetaria;
    - los tramos de tasa cero y la poca variación de ΔFFR en ellos;
    - la COVID y las ventanas de resultado de las proyecciones locales que la tocan;
    - los efectos base del rebote interanual del PIB, que entra en 2021T3–2022T2 por el rezago, y del crédito del PPP, que entra en 2021T2–2022T1, sin dummy;
    - la no estacionariedad de π y CRED(t−4) (regresión desbalanceada);
    - que Granger mide precedencia;
    - que la inferencia es condicional al K elegido con los mismos datos.
  - **Detectadas:**
    - K_BIC o K_AIC igual a 8;
    - diagnósticos con «falla» o «alerta», y en particular Breusch-Godfrey con «falla» (posible inconsistencia de MCO con el rezago de la dependiente);
    - truncamiento espectral;
    - variantes, horizontes o diagnósticos «no estimados» o «no calculables»;
    - regresores «no I(0)»;
    - los trimestres de la muestra principal cuyos rezagos de ΔFFR o de ΔDR salen de 2020T2–2021T1 sin dummy.
- RF-26: EL SISTEMA producirá una tabla de desviaciones y decisiones frente a la guía y a la spec 003 con:
  - la muestra M, que empieza un trimestre después de la del Modelo I por los 8 rezagos, y su fin en 2026T2 frente al 2026-01-01 del ejemplo de la guía;
  - la selección de K por BIC y la de AIC como robustez;
  - los controles rezagados y la forma fija de los regresores frente a la regla de estacionariedad;
  - la definición de tramo de tasa cero por regla;
  - que el GDP nominal no se prueba como robustez porque el PIB es aquí un control rezagado y no la variable de interés, y que la muestra larga desde 1985 queda fuera porque la historia congelada empieza en 1998;
  - cualquier entrada que se añada a «Desviaciones del pre-registro».
- RF-27: EL SISTEMA producirá una tabla de insumos para la comparación con el Modelo I (sección 6.3) con, para cada modelo: el coeficiente de ΔFFR del mismo trimestre (θ₀ aquí y el de ΔFFR(t) en la spec 003, leído de sus salidas), su error HAC, p, la muestra, las observaciones y la forma de los controles (contemporáneos o rezagados). La redacción de la comparación corresponde a la spec 006.
- RF-28: EL SISTEMA escribirá en las variables del informe, bajo el prefijo `modelo2.` y con las claves fijadas en el plan:
  - **Inventario:** estimador, forma de Y, K elegido y criterio, K_AIC, muestra M y observaciones, rezagos HAC y dummies COVID.
  - **Coeficientes**, S, S_rez y H1, con IC 95 % y p.
  - **Trayectoria:** ψ_h y R(h), h\* con su signo y H2.
  - **Granger** y la **lectura** de la evidencia.
  - **Proyecciones locales:** β_h, φ_h, bandas y estado por horizonte, el recuento de la comparación y el horizonte de detección.
  - **Diagnósticos:** estadístico, p y veredicto.
  - **Robustez** y las listas de limitaciones y desviaciones.
  - Un horizonte o una variante «no estimada» o «no aplica» va como texto. Ninguna cifra se escribe a mano en el informe.
- RF-29: EL SISTEMA exportará, para la spec 005, en un formato legible por máquina: los coeficientes y los nombres de los términos del modelo principal, su matriz de covarianza HAC completa tras el tratamiento de la spec 003 junto con la ventana HAC y la marca de truncamiento, el K elegido, la muestra, las dummies COVID, la trayectoria R(h) y la lectura de la evidencia.
- RF-30: EL SISTEMA producirá cada tabla en Markdown (coma decimal, «< 0,001» para p pequeños) y en CSV (precisión completa), y cada figura en PNG con pie de fuente («Fuente: FRED; elaboración propia»), desde la etapa de modelos del pipeline.

## Requisitos no funcionales
- RNF-1 (pre-registro): esta spec se aprueba y se commitea antes de la primera estimación con datos reales, en un commit que solo contiene los archivos de `specs/004-modelo-ii/`.
- RNF-2 (tests del estimador): con un proceso simulado de coeficientes conocidos y semilla fija, la estimación recupera los coeficientes dentro de una tolerancia declarada en el plan; la selección por BIC recupera el K verdadero con n ≥ 1 000; y, con ΔFFR simulado como AR(1) de coeficiente 0,8 y errores AR(1) de coeficiente 0,7, el error HAC del coeficiente de ΔFFR supera al clásico.
- RNF-3 (tests de efectos, trayectoria y lectura): S, S_rez, sus Wald, ψ_h y R(h) (comprobados con una forma cerrada), h\*, el empate de h\*, la prueba de Granger y la regla de lectura (sus tres resultados y la marca de signo contrario) tienen tests con datos sintéticos. Granger rechaza con θ_j ≠ 0 y no rechaza con θ_j = 0.
- RNF-4 (tests de las proyecciones locales): con un proceso simulado en que ΔFFR es ruido blanco y los controles son independientes, β_h recupera R(h) y φ_h recupera la respuesta de la tasa, dentro de una tolerancia declarada en el plan; y la ventana HAC es al menos h + 1.
- RNF-5 (tests de las notas): cada nota de pie que esta spec exige (RF-8, RF-11, RF-17, RF-20, RF-24 y las de limitaciones) tiene un test que comprueba su texto y que sus cifras salen del código.
- RNF-6 (tests de los diagnósticos): el Chow con K + 7 interacciones, el CUSUM sin los trimestres de las dummies y White con eliminación por rango tienen tests con procesos simulados: Breusch-Godfrey rechaza con errores AR(1) de coeficiente 0,7 y no con errores independientes, y el Chow rechaza con un quiebre simulado en las pendientes y no sin él.
- RNF-7 (semillas): en los tests de simulación, X y el ruido de y salen de semillas independientes.
- RNF-8 (reproducibilidad): dos corridas del pipeline sobre los mismos datos congelados producen tablas, figuras, JSON y variables idénticos byte a byte.
- RNF-9 (sin red, lógica separada): los tests no usan la red; la estimación, la selección, los efectos, las proyecciones y los diagnósticos son funciones puras sin red, disco ni gráficos, y no rellenan ni descartan faltantes.
- RNF-10 (lenguaje): ninguna salida textual contiene «causa», «causal» (ni «causalidad»), «provoca» ni «debido a». Los nombres técnicos de las definiciones están permitidos; las limitaciones se redactan como «no identifica el efecto de la política monetaria».
- RNF-11 (idioma): etiquetas de tablas y gráficos en español; código en inglés.

## Casos límite
- **AIC y BIC eligen el mismo K:** una sola especificación; R1 «no aplica» y sale del denominador.
- **K_BIC o K_AIC igual a 8:** se declara; el rango no se amplía.
- **Empate de AIC o BIC entre dos K:** gana el menor K. **Empate de |ψ_h| entre horizontes:** gana el menor h.
- **Algún K de la selección o la principal sin grados de libertad o con rango incompleto:** el pipeline se detiene (RF-5).
- **R3 deja pocos trimestres:** si quedan menos de 30 grados de libertad, «no estimada» con su motivo.
- **R2 y R3 quitan las cuatro dummies COVID:** se omiten (no hay variación) y se anota; en la principal y en R1 son siempre obligatorias.
- **ρ̂ cerca de 1:** R(h) se calcula igual (es finita para h ≤ 12) y el pie avisa (ρ̂ ≥ 0,95, y |ρ̂| ≥ 1 como dinámica explosiva).
- **Breusch-Godfrey rechaza con ΔDR(t−1) en la ecuación:** se declara la posible inconsistencia de MCO como limitación; añadir rezagos tras ver el resultado exige un `/sdd-change`.
- **Bloque de interacciones del Chow con rango incompleto:** la fila es «no calculable» (RF-20).
- **Un horizonte de la proyección local sin grados de libertad suficientes:** «no estimada» solo para ese h.
- **Ninguna banda de la proyección excluye el cero:** el horizonte de detección es «ninguno».
- **La decisión de estacionariedad de DRALACBS cambia en la spec 001:** se detiene (RF-2).
- **2025T4 con CPI y desempleo promediados con dos meses (spec 001):** afecta a π(t−1) en 2026T1 y a ΔU(t−1) en 2026T1 y 2026T2; entran como cualquier otro trimestre.
- **Una nueva descarga de FRED:** los datos están congelados; cualquier descarga nueva pasa por un `/sdd-change` de la spec 001 y de esta spec.

## Fuera de alcance
- Identificación causal de la política monetaria: shocks de alta frecuencia o narrativos, variables instrumentales, VAR o SVAR.
- Modelos con regímenes o umbrales para los tramos de tasa cero.
- La prueba de Granger en la dirección inversa (de la morosidad a la tasa).
- Ampliar el rango de K más allá de 8 o seleccionar K con otros criterios.
- Una variante de la proyección local que descarte las ventanas que tocan la COVID (se declara como límite).
- Bandas por método delta para la trayectoria del modelo de rezagos distribuidos.
- Validación fuera de muestra del Modelo II.
- Modelos por sub-cartera o con otras dependientes; GDP nominal y muestra larga como robusteces.
- El uso del efecto de la tasa en el estrés más allá de la regla heredada (spec 005).
- La redacción de la interpretación, de la discusión y de la comparación narrativa con el Modelo I (spec 006).
- Unificar en la spec 003 la notación del KPSS truncado con la de la 001.

## Criterios de finalización
- Spec aprobada y commiteada antes de la primera estimación (RNF-1).
- Existen, en Markdown y CSV o PNG según corresponda, las salidas de RF-7 a RF-27: la tabla de selección, la de coeficientes, la de efectos acumulados, la de trayectoria, Granger y la lectura, la de proyecciones locales y su comparación, los diagnósticos y el CUSUM, la estacionariedad del modelo, las dos tablas de robustez, las limitaciones, las desviaciones y los insumos de comparación, y los gráficos (perfil de coeficientes, respuesta acumulada y de la tasa, y CUSUM).
- Las variables `modelo2.*` (RF-28) y la exportación para la spec 005 (RF-29) existen.
- `uv run python -m src.pipeline all` reproduce todo desde un clon limpio y dos corridas no dejan diferencias (RNF-8).
- `uv run pytest -q` en verde, sin red.
- `specs/004-modelo-ii/review-validate.md` y `specs/004-modelo-ii/review-audit.md` con `VEREDICTO: APROBADO`.

## Desviaciones del pre-registro
(vacío)

## Dudas abiertas
(ninguna)
