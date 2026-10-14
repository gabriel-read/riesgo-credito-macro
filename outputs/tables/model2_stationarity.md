| termino | etiqueta | columna_panel | forma | adf_stat | adf_p | kpss_stat | kpss_p | decision | orden | no_i0 | nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| d_dr | ΔDR — dependiente (DRALACBS en primera diferencia) | dralacbs | primera diferencia | -3,443 | 0,010 | 0,140 | > 0,10 | niveles | I(0) | no | regla de la spec 001 aplicada a la fila «primera diferencia» |
| d_ffr | ΔFFR — cambio trimestral de la tasa de la Fed | fedfunds | primera diferencia | -4,237 | < 0,001 | 0,139 | > 0,10 | niveles | I(0) | no | regla de la spec 001 aplicada a la fila «primera diferencia» |
| gdp_l1 | PIB(t−1) (variación interanual del PIB real, %) | gdpc1_yoy | tal cual | -3,620 | 0,005 | 0,099 | > 0,10 | niveles | I(0) | no | ADF/KPSS de la serie sin rezagar |
| d_unemp_l1 | ΔU(t−1) (cambio trimestral del desempleo, pp) | unrate | primera diferencia | -12,028 | < 0,001 | 0,087 | > 0,10 | niveles | I(0) | no | regla de la spec 001 aplicada a la fila «primera diferencia»; ADF/KPSS de la serie sin rezagar |
| inflation_l1 | π(t−1) (inflación interanual, %) | cpiaucsl_yoy | tal cual | -2,337 | 0,160 | 0,229 | > 0,10 | ambigua (primera diferencia) | I(1) | sí | ADF/KPSS de la serie sin rezagar |
| credit_l4 | CRED(t−4) (variación interanual de préstamos, %) | loans_yoy | tal cual | -2,455 | 0,127 | 0,194 | > 0,10 | ambigua (primera diferencia) | I(1) | sí | ADF/KPSS de la serie sin rezagar |

Nota: ADF y KPSS copiados de la tabla de la spec 001, sin recalcular; ΔDR, ΔFFR y ΔU se juzgan con la fila «primera diferencia» y «niveles» significa estacionaria en la forma en que entra; los términos rezagados (PIB(t−1), ΔU(t−1), π(t−1), CRED(t−4)) usan el ADF y el KPSS de la serie sin rezagar; «no I(0)» marca los términos que no son estacionarios en la forma fija en que entran.
