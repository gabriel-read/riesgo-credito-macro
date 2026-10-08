| termino | etiqueta | coef | ee_hac | z | p | ic_inf | ic_sup | nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| const | Constante | -0,100 | 0,024 | -4,223 | < 0,001 | -0,146 | -0,054 |  |
| y_lag | ΔDR(t−1) — rezago de la dependiente | 0,699 | 0,084 | 8,317 | < 0,001 | 0,535 | 0,864 |  |
| d_ffr_l0 | ΔFFR(t) (cambio trimestral de la tasa de la Fed, pp) | -0,084 | 0,064 | -1,310 | 0,190 | -0,210 | 0,042 |  |
| d_ffr_l1 | ΔFFR(t−1) | 0,036 | 0,039 | 0,926 | 0,355 | -0,040 | 0,111 |  |
| gdp_l1 | PIB(t−1) (variación interanual del PIB real, %) | 0,001 | 0,005 | 0,224 | 0,823 | -0,009 | 0,011 |  |
| d_unemp_l1 | ΔU(t−1) (cambio trimestral del desempleo, pp) | 0,110 | 0,053 | 2,062 | 0,039 | 0,005 | 0,215 |  |
| inflation_l1 | π(t−1) (inflación interanual, %) | 0,024 | 0,010 | 2,435 | 0,015 | 0,005 | 0,042 |  |
| credit_l4 | CRED(t−4) (variación interanual de préstamos, %) | 0,007 | 0,003 | 2,603 | 0,009 | 0,002 | 0,012 |  |
| covid_2020q2 | Dummy COVID 2020T2 | -0,114 | 0,078 | -1,451 | 0,147 | -0,267 | 0,040 | EE HAC no informativo: dummy de impulso con residuo nulo |
| covid_2020q3 | Dummy COVID 2020T3 | -0,876 | 0,470 | -1,865 | 0,062 | -1,797 | 0,045 | EE HAC no informativo: dummy de impulso con residuo nulo |
| covid_2020q4 | Dummy COVID 2020T4 | 0,455 | 0,228 | 1,995 | 0,046 | 0,008 | 0,901 | EE HAC no informativo: dummy de impulso con residuo nulo |
| covid_2021q1 | Dummy COVID 2021T1 | 0,156 | 0,110 | 1,419 | 0,156 | -0,059 | 0,371 | EE HAC no informativo: dummy de impulso con residuo nulo |

Nota: K = 1 elegido por BIC; variable dependiente en primera diferencia; muestra M 2000T2–2026T2; n = 105; parámetros = 12; R² = 0,844; R² ajustado = 0,826; error estándar de la regresión = 0,094; ventana HAC de 4 rezagos (Newey-West, kernel de Bartlett); truncamiento espectral: no; rango reducido por dummies de impulso (esperado).
