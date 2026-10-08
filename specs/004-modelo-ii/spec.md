# Spec 004 — Modelo II: política monetaria y deterioro posterior de la cartera
Estado: borrador · Crítica: sí

## Contexto y objetivo
La guía pide un segundo modelo que responda si un cambio de la política monetaria tiene relación con el deterioro posterior de la calidad de la cartera y si existen efectos rezagados. Esta spec fija ese modelo **antes de ver ningún resultado** (pre-registro, principio 2 de la constitución): variables, rezagos y su criterio de selección, estimador, definición del efecto acumulado y del efecto máximo, prueba de Granger, proyecciones locales, robusteces y diagnósticos.

Objetivo: estimar por MCO con errores Newey-West un modelo de rezagos distribuidos de la variación de la morosidad (DRALACBS) sobre el cambio de la tasa de fondos federales de t a t−K, con K elegido por BIC entre 1 y 8 sobre una misma muestra efectiva; reportar el efecto acumulado con prueba de Wald HAC, la trayectoria de la respuesta del nivel de morosidad, el trimestre de efecto máximo y la prueba de Granger; y contrastar la respuesta con proyecciones locales de Jordà (h = 0..12). Los resultados son asociaciones dinámicas, no efectos causales puros.

## Pregunta que responde (y sección de docs/guia-profesor.md que cubre)
¿Cómo afectan los cambios en la política monetaria al riesgo de crédito y existen efectos rezagados sobre la calidad de la cartera? Cubre la sección 5 (Modelo II) y aporta los resultados de la 6.2 y el insumo cuantitativo de la 6.3 (comparación con el Modelo I). La interpretación y la discusión se redactan en la spec 006.

Frontera con otras specs:
- **Modelo I (spec 003):** mide la asociación contemporánea de la morosidad con el conjunto de condiciones macro del trimestre. El Modelo II estudia la respuesta dinámica y rezagada de la morosidad a la tasa, con los controles macro rezagados.
- **Estrés (spec 005):** esta spec exporta los coeficientes y la covarianza HAC; decidir cómo se usa el efecto de la tasa en el escenario adverso, y qué hacer si el signo no es el esperado, es materia de la 005 y se pre-registra allí.

## Usuarios
- El autor, que redacta las secciones 3.5, 5 y 6.2 del informe con las salidas de esta spec.
- La spec 005 (estrés), que usa los coeficientes y la covarianza HAC exportados.
- La spec 006, que compara los dos modelos en 6.3.
- El revisor econométrico (auditoría crítica) y el profesor evaluador.

## Historias de usuario
- HU-1. Como autor, quiero una especificación fijada y commiteada antes de estimar para demostrar que no elegí el modelo según los resultados.
- HU-2. Como autor, quiero que K salga de una regla pre-registrada (BIC, con AIC como robustez) y no de una elección mía, para que el número de rezagos no dependa de lo que me gustaría ver.
- HU-3. Como autor, quiero el efecto acumulado con su prueba, la trayectoria de la respuesta y el trimestre de efecto máximo para responder si hay efectos rezagados.
- HU-4. Como autor, quiero proyecciones locales sin la forma paramétrica del modelo de rezagos distribuidos para ver si la respuesta es la misma.
- HU-5. Como revisor, quiero todos los diagnósticos y los límites declarados (endogeneidad de la tasa, tramos de tasa cero, COVID) para juzgar la validez de las conclusiones.
- HU-6. Como autor de la spec 005, quiero los coeficientes, la covarianza y la trayectoria exportados para usarlos sin reestimar.

## Definiciones
- **Panel, trimestre, historia descargada, variación interanual y regla de decisión niveles/diferencias**: los de la spec 001.
- **Historia transformada, inicio efectivo, ventana HAC, distribución de referencia, «significativo», «robusto», dummy de impulso y tratamiento de la matriz HAC (comprobación en el bloque sin dummies de impulso)**: los de la spec 003, aplicados a cada regresión de esta spec.
- **Y (dependiente)**: la variación trimestral de DRALACBS en pp, ΔDR(t) = DR(t) − DR(t−1), calculada sobre la historia transformada. Entra en diferencia porque la tabla de estacionariedad de la spec 001 la clasifica «ambigua (primera diferencia)».
- **ΔFFR(t)**: la diferencia trimestral de la tasa de fondos federales en pp (columna de la spec 001), calculada sobre el promedio trimestral de FEDFUNDS.
- **Shock de 1 pp**: un aumento de 1 pp del promedio trimestral de la tasa en un trimestre, es decir, ΔFFR(0) = +1 una sola vez, que deja la tasa 1 pp más alta en adelante. Es una variación observada de la tasa, no un shock monetario identificado.
- **Tramo de tasa cero**: trimestre con el promedio trimestral de FEDFUNDS ≤ 0,25 %. La definición es por regla, no por fechas. A la fecha de esta spec son 36 trimestres: 2009T1–2015T4 y 2020T2–2022T1.
- **Muestra efectiva común (M)**: del primer trimestre en que existen todos los términos del modelo con K = 8 (ΔFFR(t−8), ΔY(t−1), PIB(t−1), ΔU(t−1), π(t−1) y CRED(t−4)) al último trimestre común de la spec 001. A la fecha es 2000T2–2026T2, 105 trimestres. Una sola muestra se usa para comparar todos los K y para el modelo principal.
- **AIC y BIC**: AIC = −2·lnL + 2·k y BIC = −2·lnL + k·ln(T), con lnL la log-verosimilitud gaussiana de MCO, k el número de parámetros (incluidas las dummies) y T las observaciones de M.
- **Respuesta acumulada R(h)**: la respuesta del **nivel** de la morosidad (pp) h trimestres después de un shock de 1 pp, con h = 0..12, que implica el modelo con su rezago de la dependiente: ψ₀ = θ₀; ψ_j = θ_j·1{j ≤ K} + ρ·ψ_{j−1} para j ≥ 1; R(h) = ψ₀ + … + ψ_h.
- **Efecto acumulado S**: la suma de los coeficientes de la tasa, S = θ₀ + θ₁ + … + θ_K, en pp de morosidad por 1 pp. Es el acumulado de los coeficientes y no incorpora la dinámica de ρ (esta la recoge R(h)).
- **Trimestre de efecto máximo h\***: el h ∈ {0, …, 12} con mayor |R(h)|; si hay empate, el menor. Se reporta con el signo de R(h\*).
- **Trimestres posteriores útiles de un quiebre**: los trimestres de la muestra posteriores al quiebre menos los que absorben las dummies de impulso.
- **Lenguaje de asociación**: «precede», «anticipa», «se asocia con». Granger mide precedencia temporal, no causalidad.

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

Los controles macro son los del Modelo I. PIB, ΔU y π se rezagan un trimestre para que no sean simultáneos con ΔFFR(t); el crédito conserva su rezago de 4 trimestres, que ya es mayor que uno y mantiene la justificación de maduración de la cartera y la comparabilidad con el Modelo I. Los regresores entran en la forma fija de esta tabla, como en el Modelo I; su no estacionariedad residual (π y CRED(t−4) figuran «no I(0)» en la spec 001) se declara como limitación.

### Ecuación (especificación principal)
ΔDR(t) = α + ρ·ΔDR(t−1) + Σ_{j=0..K} θ_j·ΔFFR(t−j) + γ₁·PIB(t−1) + γ₂·ΔU(t−1) + γ₃·π(t−1) + γ₄·CRED(t−4) + Σₖ δₖ·D(k) + ε(t)

### Selección de K
K se elige entre 1 y 8 estimando un modelo por cada K sobre la muestra M, con el mismo resto de la ecuación. K_BIC es el K de menor BIC y K_AIC el de menor AIC; si hay empate, el menor K. **La especificación principal usa K_BIC.** Si K_AIC ≠ K_BIC, el modelo con K_AIC es la robustez R1. Los K de las demás robusteces son el de la principal; no se vuelve a elegir K en ninguna variante.

### Estimador y errores estándar
MCO con errores Newey-West (ventana y tratamiento de la matriz HAC de la spec 003). Inferencia con la normal.

### Efecto acumulado, trayectoria y Granger
- **Efecto acumulado:** Wald HAC de H0: S = 0, χ²(1), con S, su error HAC, p e IC 95 %.
- **Trayectoria:** R(h) para h = 0..12, solo estimación puntual (sin bandas; las bandas de la respuesta las da la proyección local).
- **Granger:** Wald HAC de H0: θ₁ = … = θ_K = 0, χ²(K). Se excluye θ₀ (el coeficiente del mismo trimestre es simultáneo). La dirección inversa (de la morosidad a la tasa) queda fuera de alcance.

### Proyecciones locales (robustez)
Una regresión por horizonte h = 0..12, con dependiente DR(t+h) − DR(t−1) (en pp, nivel acumulado):
- regresor de interés: ΔFFR(t);
- controles: ΔDR(t−1), PIB(t−1), ΔU(t−1), π(t−1), CRED(t−4), ΔFFR(t−1..t−K) con el K del modelo principal, y las dummies COVID fechadas en t;
- ventana HAC: max(la fórmula de la spec 003 con las T de ese horizonte, h + 1);
- muestra: del inicio de M al último trimestre común menos h trimestres;
- respuesta: β_h por 1 pp, con banda HAC al 90 % (β_h ± 1,6449·EE).

### Signos esperados e hipótesis pre-registradas
- **H1 (signo):** S > 0. Mecanismo: tasas más altas encarecen el servicio de la deuda y endurecen las condiciones financieras, y la mora aparece con retraso.
- **H2 (rezago):** h\* ≥ 1, es decir, el efecto máximo no ocurre en el mismo trimestre.
- Los coeficientes individuales θ_j y los controles no tienen hipótesis de signo.
- Cada hipótesis se reporta «sí» o «no». Un resultado distinto de lo esperado se reporta tal cual y no cambia la especificación.

### Pruebas de robustez previstas
- **R1.** Modelo con K_AIC (solo si K_AIC ≠ K_BIC).
- **R2.** Sin 2020–2021: excluye 2020T1–2021T4 y no lleva dummies COVID.
- **R3.** Sin tramos de tasa cero: excluye los trimestres con promedio de FEDFUNDS ≤ 0,25 % y no lleva dummies COVID (las cuatro caen dentro de un tramo de tasa cero).
- **Proyecciones locales** (arriba), con su comparación con R(h).
- En R2 y R3 los rezagos siguen saliendo de la historia transformada, y la ventana HAC trata como contiguos los trimestres vecinos de cada exclusión.
- Criterio de robustez: el de la spec 003 aplicado a S (mismo signo que la principal y p < 0,10 con errores HAC).

### Diagnósticos
Sobre la especificación principal: Breusch-Godfrey con 4 rezagos (LM), Breusch-Pagan (Koenker), White (con eliminación de colinealidad por rango), Jarque-Bera, RESET (potencias 2 y 3 de los valores ajustados, F), VIF de cada regresor excepto la constante y las dummies, Chow en 2008T3 y 2020T2 como Wald HAC con interacciones de todos los términos que no son dummies de impulso, y CUSUM de residuos recursivos sobre la regresión sin dummies de impulso ni sus trimestres. Veredicto: «pasa» si p ≥ 0,05, «falla» si p < 0,05; VIF «alerta» si > 10.

## Requisitos funcionales

### Datos, muestra y forma de la dependiente
- RF-1: EL SISTEMA construirá todas las variables, rezagos y diferencias sobre la historia transformada y recortará después cada muestra de estimación.
- RF-2: EL SISTEMA leerá de la tabla de estacionariedad de la spec 001 la decisión de DRALACBS y, SI no es «ambigua (primera diferencia)», ENTONCES se detendrá con un error que nombre la serie y las dos formas. Continuar exige un `/sdd-change` de esta spec.
- RF-3: EL SISTEMA calculará la muestra efectiva común M y la reportará (primer y último trimestre y número de observaciones) en el pie de las tablas de selección y de coeficientes.
- RF-4: SI falta algún término dentro de la muestra de una regresión, después de su inicio efectivo, ENTONCES EL SISTEMA se detendrá con un error que nombre la variable, el trimestre y la regresión, sin imputar ni eliminar filas en silencio.

### Selección de K y estimación principal
- RF-5: EL SISTEMA estimará, sobre la muestra M, un modelo por cada K = 1..8 y calculará su AIC y su BIC.
- RF-6: EL SISTEMA elegirá K_BIC y K_AIC según la regla de selección y usará K_BIC en la especificación principal. SI K_AIC ≠ K_BIC, ENTONCES el modelo con K_AIC será la robustez R1; SI coinciden, ENTONCES R1 figurará como «no aplica: AIC y BIC eligen el mismo K».
- RF-7: EL SISTEMA producirá una tabla de selección con, por K: número de parámetros, observaciones, AIC, BIC y la marca de los K elegidos. SI el K elegido es 8, ENTONCES lo declarará como limitación (el óptimo puede estar fuera del rango) sin ampliar el rango.
- RF-8: EL SISTEMA estimará la especificación principal por MCO con errores Newey-West y producirá una tabla de coeficientes con, por término: coeficiente, error HAC, z, p, IC 95 % y la nota de las dummies de impulso. El pie traerá: K elegido y criterio, forma de Y, muestra M, observaciones, parámetros, R² y R² ajustado, error estándar de la regresión, rezagos de la ventana HAC, si se aplicó truncamiento espectral al bloque sin dummies de impulso y la nota «rango reducido por dummies de impulso (esperado)».
- RF-9: EL SISTEMA producirá un gráfico del perfil de coeficientes θ_j (j = 0..K) con su IC 95 % HAC y una línea en cero, con ejes y títulos en español y el pie de fuente.

### Efecto acumulado, trayectoria, efecto máximo y Granger
- RF-10: EL SISTEMA producirá una tabla del efecto acumulado con S, su error HAC, el estadístico χ²(1), el p-valor y el IC 95 %, en pp de morosidad por 1 pp, y si coincide con H1.
- RF-11: EL SISTEMA producirá una tabla de la trayectoria con R(h) para h = 0..12, el h\* con su signo y si coincide con H1 (signo de R(h\*)) y con H2. El pie dirá que la trayectoria no lleva bandas y que las bandas están en la proyección local.
- RF-12: EL SISTEMA producirá la prueba de Granger con el estadístico χ²(K), el p-valor y el veredicto («rechaza» o «no rechaza» al 5 %), descrita como precedencia temporal.

### Proyecciones locales
- RF-13: EL SISTEMA estimará una proyección local por cada h = 0..12 con la especificación de la sección de proyecciones locales y producirá una tabla con, por h: β_h, error HAC, banda del 90 %, observaciones, rezagos HAC y estado.
- RF-14: SI en un horizonte quedan menos de 30 grados de libertad o los regresores tienen rango incompleto, ENTONCES EL SISTEMA reportará ese horizonte como «no estimada» con su motivo, sin afectar a los demás.
- RF-15: EL SISTEMA producirá una tabla de comparación con, por h: R(h), β_h, si tienen el mismo signo y si la banda del 90 % de la proyección excluye el cero, con el recuento «k de n» de los horizontes con el mismo signo (n cuenta solo los estimados) y el h\* de cada método.
- RF-16: EL SISTEMA producirá un gráfico de la respuesta acumulada con β_h y su banda del 90 % y la trayectoria R(h) del modelo de rezagos distribuidos superpuesta, con ejes y leyenda en español y el pie de fuente.

### Diagnósticos y estacionariedad
- RF-17: EL SISTEMA producirá la tabla de diagnósticos de la sección correspondiente con estadístico, p-valor y veredicto de cada prueba, y su gráfico CUSUM con bandas al 5 %.
- RF-18: La nota de cada fila de Chow indicará los trimestres posteriores útiles, calculados por código. SI son menos de 30, ENTONCES la nota añadirá, sin dirección: «el tamaño empírico del contraste puede diferir del 5 % nominal». El veredicto sigue a p.
- RF-19: EL SISTEMA producirá una tabla de estacionariedad del modelo con ΔDR, ΔFFR y los cuatro controles en la forma en que entran, con el ADF y el KPSS copiados de la tabla de la spec 001, su decisión y su orden de integración, y la marca «no I(0)». El ADF se escribe «< 0,001» si procede y el KPSS truncado de statsmodels se escribe «> 0,10» o «< 0,01», como en la spec 001; los CSV conservan los valores.

### Robusteces
- RF-20: EL SISTEMA estimará R1, R2 y R3 con el mismo estimador y las mismas reglas y producirá una tabla con, por variante: K, muestra y observaciones, rezagos HAC, S, su error HAC, el p de Wald, el h\* y si S coincide con H1; o el estado «no estimada» con su motivo.
- RF-21: SI una variante tiene menos de 30 grados de libertad o rango incompleto, ENTONCES EL SISTEMA la reportará como «no estimada» con su motivo. SI una dummy COVID no tiene variación en la muestra, ENTONCES se omite solo en R2 y R3 y en cualquier otra regresión es un error.
- RF-22: EL SISTEMA producirá una tabla resumen de robustez de S con «sí», «no» o «no estimada» por variante según el criterio pre-registrado, y su pie dirá: el criterio, el K de cada variante, las exclusiones de R2 y R3 y, calculados por código, los trimestres cuyos rezagos salen de trimestres excluidos.

### Límites, desviaciones y variables del informe
- RF-23: EL SISTEMA producirá una tabla de limitaciones con las fijas y las detectadas por código. Las fijas serán: la endogeneidad de la tasa de fondos federales (la Fed reacciona a la economía); que ΔFFR es una variación observada y no un shock identificado; los tramos de tasa cero y la poca variación de ΔFFR en ellos; la COVID y las ventanas de resultado de las proyecciones locales que la tocan; los efectos base de 2021T2–2022T1 sin dummy en PIB y crédito; la no estacionariedad de π y CRED(t−4) (regresión desbalanceada); y que Granger mide precedencia. Las detectadas serán: K elegido igual a 8, diagnósticos con «falla» o «alerta», truncamiento espectral, variantes u horizontes «no estimados» y regresores «no I(0)».
- RF-24: EL SISTEMA producirá una tabla de desviaciones y decisiones frente a la guía y a la spec 003 con: la muestra efectiva M que empieza un trimestre después de la del Modelo I por los 8 rezagos; la selección de K por BIC y la de AIC como robustez; los controles rezagados; la definición de tramo de tasa cero por regla; y cualquier entrada que se añada a «Desviaciones del pre-registro».
- RF-25: EL SISTEMA escribirá en las variables del informe, bajo el prefijo `modelo2.` y con las claves fijadas en el plan:
  - **Inventario:** estimador, forma de Y, K elegido y criterio, K_AIC, muestra M y observaciones, rezagos HAC y dummies COVID.
  - **Coeficientes** y el efecto acumulado S con su Wald (todos con IC 95 % y p).
  - **Trayectoria** R(h) y h\* con su signo, y H1 y H2.
  - **Granger:** estadístico, p y veredicto.
  - **Proyecciones locales:** β_h, banda y estado por horizonte, y el recuento de la comparación.
  - **Diagnósticos:** estadístico, p y veredicto.
  - **Robustez** y las listas de limitaciones y desviaciones.
  - Un efecto «no reportado» o «no definido» va como texto, nunca como número. Ninguna cifra se escribe a mano en el informe.
- RF-26: EL SISTEMA exportará, para la spec 005, los coeficientes, la covarianza HAC, los nombres de los términos, el K elegido, la muestra, las dummies COVID y la trayectoria R(h) del modelo principal, en un formato legible por máquina.
- RF-27: EL SISTEMA producirá cada tabla en Markdown (coma decimal, «< 0,001» para p pequeños) y en CSV (precisión completa), y cada figura en PNG con pie de fuente («Fuente: FRED; elaboración propia»), desde la etapa de modelos del pipeline.

## Requisitos no funcionales
- RNF-1 (pre-registro): esta spec se aprueba y se commitea antes de la primera estimación con datos reales, en un commit que solo contiene los archivos de `specs/004-modelo-ii/`.
- RNF-2 (tests del estimador): con un proceso simulado de coeficientes conocidos y semilla fija, la estimación recupera los coeficientes dentro de una tolerancia declarada en el plan; la selección por BIC recupera el K verdadero con una muestra grande; y el error HAC supera al clásico con errores AR(1) simulados.
- RNF-3 (tests de efectos y trayectoria): S, su Wald, la recursión R(h) (comprobada con una forma cerrada), h\*, el empate de h\* y la prueba de Granger tienen tests con datos sintéticos: Granger rechaza con θ_j ≠ 0 y no rechaza con θ_j = 0.
- RNF-4 (tests de las proyecciones locales): con un proceso simulado de respuesta conocida, las β_h recuperan R(h) dentro de una tolerancia declarada, y la ventana HAC es al menos h + 1.
- RNF-5 (tests de las notas): cada nota de pie que esta spec exige (RF-8, RF-11, RF-18, RF-22 y las de limitaciones) tiene un test que comprueba su texto y que sus cifras salen del código.
- RNF-6 (semillas): en los tests de simulación, X y el ruido de y salen de semillas independientes.
- RNF-7 (reproducibilidad): dos corridas del pipeline sobre los mismos datos congelados producen tablas, figuras, JSON y variables idénticos byte a byte.
- RNF-8 (sin red, lógica separada): los tests no usan la red; la estimación, la selección, los efectos, las proyecciones y los diagnósticos son funciones puras sin red, disco ni gráficos, y no rellenan ni descartan faltantes.
- RNF-9 (lenguaje): ninguna salida textual usa lenguaje causal («causa», «causal», «provoca», «debido a»); los resultados se describen como asociación y Granger como precedencia.
- RNF-10 (idioma): etiquetas de tablas y gráficos en español; código en inglés.

## Casos límite
- **AIC y BIC eligen el mismo K:** una sola especificación; R1 «no aplica».
- **K elegido = 8:** se declara; el rango no se amplía.
- **Empate de AIC o BIC entre dos K:** gana el menor K. **Empate de |R(h)| entre horizontes:** gana el menor h.
- **R3 deja pocos trimestres:** si quedan menos de 30 grados de libertad, «no estimada» con su motivo.
- **R2 y R3 quitan las cuatro dummies COVID:** se omiten (no hay variación) y se anota; en la principal y en R1 son siempre obligatorias.
- **|ρ̂| ≥ 1:** R(h) se calcula igual (es finita para h ≤ 12) y la nota de la tabla de trayectoria avisa de que la dinámica es explosiva.
- **Un horizonte de la proyección local sin grados de libertad suficientes:** «no estimada» solo para ese h.
- **La decisión de estacionariedad de DRALACBS cambia en la spec 001:** se detiene (RF-2).
- **2025T4 con CPI y desempleo promediados con dos meses (spec 001):** afecta a π(t−1) y ΔU(t−1) en 2026T1; entra como cualquier otro trimestre.
- **Una nueva descarga de FRED:** los datos están congelados; cualquier descarga nueva pasa por un `/sdd-change` de la spec 001 y de esta spec.

## Fuera de alcance
- Identificación causal de la política monetaria: shocks de alta frecuencia o narrativos, variables instrumentales, VAR o SVAR.
- Modelos con regímenes o umbrales para los tramos de tasa cero.
- La prueba de Granger en la dirección inversa (de la morosidad a la tasa).
- Ampliar el rango de K más allá de 8 o seleccionar K con otros criterios.
- Validación fuera de muestra del Modelo II.
- Modelos por sub-cartera o con otras dependientes.
- El uso del efecto de la tasa en el estrés y el tratamiento de un signo contrario al esperado (spec 005).
- La redacción de la interpretación y de la discusión (spec 006).
- Unificar en la spec 003 la notación del KPSS truncado con la de la 001.

## Criterios de finalización
- Spec aprobada y commiteada antes de la primera estimación (RNF-1).
- Existen, en Markdown y CSV o PNG según corresponda, las salidas de RF-7 a RF-24: la tabla de selección, la de coeficientes, la del efecto acumulado, la de trayectoria, Granger, la de proyecciones locales y su comparación, los diagnósticos y el CUSUM, la estacionariedad del modelo, las dos tablas de robustez, las limitaciones y las desviaciones, y los tres gráficos (perfil de coeficientes, respuesta acumulada y CUSUM).
- Las variables `modelo2.*` (RF-25) y la exportación para la spec 005 (RF-26) existen.
- `uv run python -m src.pipeline all` reproduce todo desde un clon limpio y dos corridas no dejan diferencias (RNF-7).
- `uv run pytest -q` en verde, sin red.
- `specs/004-modelo-ii/review-validate.md` y `specs/004-modelo-ii/review-audit.md` con `VEREDICTO: APROBADO`.

## Desviaciones del pre-registro
(vacío)

## Dudas abiertas
(ninguna)
