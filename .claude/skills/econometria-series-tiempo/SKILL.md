---
name: econometria-series-tiempo
description: Úsala siempre que especifiques, estimes, pruebes, revises o interpretes un modelo de series de tiempo en este proyecto (Modelo I, Modelo II, proyecciones locales, diagnósticos o escenarios de estrés).
---

# Econometría de series de tiempo — reglas del proyecto

Los modelos son la mayor fuente de errores silenciosos de este proyecto: un resultado puede verse bien y ser inválido. Sigue esta guía siempre.

## Reglas
- **Estacionariedad antes de estimar**: ADF (H0: raíz unitaria) y KPSS (H0: estacionaria) a cada serie en la forma en que entra al modelo. Si ADF no rechaza al 5 % o KPSS rechaza al 5 %, la serie entra en primera diferencia. La misma regla para todas las series, reportada en una tabla.
- **Errores estándar**: siempre Newey-West (HAC). Rezagos de la ventana: floor(4·(T/100)^(2/9)); en proyecciones locales, al menos h + 1.
- **Rezagos del Modelo II**: se eligen por AIC y BIC entre 1 y 8 trimestres sobre la MISMA muestra efectiva (recorta al rezago máximo antes de comparar). Si difieren, la especificación principal usa BIC y la otra va como robustez.
- **Efecto acumulado**: suma de los coeficientes de la tasa con prueba de Wald (H0: suma = 0) usando la matriz HAC.
- **COVID**: dummies trimestrales 2020T2–2021T1 en la especificación principal y una robustez sin 2020–2021. Nunca borres observaciones en silencio.
- **Unidades**: reporta en puntos porcentuales (pp) de morosidad por pp del regresor (o por desviación estándar, si la spec lo dice). Di siempre la unidad.
- **Lenguaje**: "se asocia con", "anticipa", "precede". Nunca "causa" ni "provoca". La tasa de la Fed reacciona a la economía (endogeneidad): decláralo como límite.
- **Significancia**: coeficiente, error HAC, p-valor e IC 95 %. No elimines regresores por no ser significativos después de ver resultados (pre-registro).
- **Proyecciones locales (Jordà)**: una regresión por horizonte h = 0..12 con los mismos controles; variable dependiente DR(t+h) − DR(t−1); bandas HAC al 90 %.
- **Estrés**: proyección recursiva con los coeficientes estimados. Incertidumbre por simulación de coeficientes con su covarianza HAC (≥ 1 000 extracciones, semilla fija). Reporta pico, trimestre del pico y diferencia contra la base en cada trimestre.
- **Reproducibilidad**: toda aleatoriedad con semilla fija declarada en el plan.

## Batería de diagnóstico (statsmodels)
ADF y KPSS · Breusch-Godfrey (4 rezagos) · Breusch-Pagan y White · Jarque-Bera · VIF (alerta > 10) · RESET de Ramsey · CUSUM y Chow en 2008T3 y 2020T2. Un diagnóstico fallido no se oculta: se reporta y se explica qué implica para la conclusión.

## Tests de estimadores
Cada estimador se prueba con un proceso simulado de coeficientes conocidos (semilla fija). El test pasa si recupera los coeficientes dentro de una tolerancia declarada y si, con autocorrelación simulada, el error HAC es mayor que el MCO clásico.

## Checklist de revisión
- [ ] ¿Cada serie tiene su prueba de estacionariedad y su transformación sigue la regla?
- [ ] ¿Todos los errores son HAC y se dice cuántos rezagos usa la ventana?
- [ ] ¿La selección de rezagos compara modelos sobre la misma muestra efectiva?
- [ ] ¿Los signos se comparan con los esperados en la spec y las sorpresas se discuten?
- [ ] ¿Hay alguna frase causal?
- [ ] ¿Se reportan y discuten los diagnósticos fallidos?
- [ ] ¿El pipeline da resultados idénticos al correrlo dos veces?

## Al terminar
Indica qué puntos del checklist comprobaste y cómo.
