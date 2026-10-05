| termino | etiqueta | columna_panel | forma | adf_stat | adf_p | kpss_stat | kpss_p | decision | orden | no_i0 | nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y | Y(t) — dependiente (DRALACBS) | dralacbs | primera diferencia | -3,443 | 0,010 | 0,140 | 0,100 | niveles | I(0) | no | regla de la spec 001 aplicada a la fila «primera diferencia»; «niveles» = estacionaria en la forma en que entra |
| y_lag | Y(t−1) — rezago de la dependiente | dralacbs | primera diferencia | -3,443 | 0,010 | 0,140 | 0,100 | niveles | I(0) | no | mismo proceso que Y, rezagado un trimestre; regla de la spec 001 aplicada a la fila «primera diferencia»; «niveles» = estacionaria en la forma en que entra |
| gdp_growth | ΔPIB (variación interanual del PIB real, %) | gdpc1_yoy | tal cual | -3,620 | 0,005 | 0,099 | 0,100 | niveles | I(0) | no |  |
| d_unemp | ΔU (cambio trimestral del desempleo, pp) | unrate | primera diferencia | -12,028 | 0,000 | 0,087 | 0,100 | niveles | I(0) | no | regla de la spec 001 aplicada a la fila «primera diferencia»; «niveles» = estacionaria en la forma en que entra |
| inflation | π (inflación interanual, %) | cpiaucsl_yoy | tal cual | -2,337 | 0,160 | 0,229 | 0,100 | ambigua (primera diferencia) | I(1) | sí |  |
| d_ffr | ΔFFR (cambio trimestral de la tasa de la Fed, pp) | fedfunds | primera diferencia | -4,237 | 0,001 | 0,139 | 0,100 | niveles | I(0) | no | regla de la spec 001 aplicada a la fila «primera diferencia»; «niveles» = estacionaria en la forma en que entra |
| credit_growth | CRED(t−4) (variación interanual de préstamos rezagada 4 trimestres, %) | loans_yoy | tal cual | -2,455 | 0,127 | 0,194 | 0,100 | ambigua (primera diferencia) | I(1) | sí | ADF/KPSS de loans_yoy sin rezagar |
