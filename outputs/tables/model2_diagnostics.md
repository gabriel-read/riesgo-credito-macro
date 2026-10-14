| prueba | estadístico | p_valor | veredicto | nota |
| --- | --- | --- | --- | --- |
| Breusch-Godfrey | 3,409 | 0,492 | pasa |  |
| Breusch-Pagan | 33,784 | < 0,001 | falla |  |
| White | 90,710 | < 0,001 | falla |  |
| Jarque-Bera | 209,207 | < 0,001 | falla |  |
| RESET | 10,448 | < 0,001 | falla |  |
| VIF (y_lag) | 3,122 | — | sin alerta |  |
| VIF (d_ffr_l0) | 2,521 | — | sin alerta |  |
| VIF (d_ffr_l1) | 2,664 | — | sin alerta |  |
| VIF (gdp_l1) | 3,008 | — | sin alerta |  |
| VIF (d_unemp_l1) | 33,154 | — | alerta |  |
| VIF (inflation_l1) | 1,414 | — | sin alerta |  |
| VIF (credit_l4) | 1,548 | — | sin alerta |  |
| Chow 2008T3 | 11,644 | 0,168 | pasa | Wald HAC con interacciones de 8 términos (constante, ρ, los cuatro controles, ΔFFR(t) y ΔFFR(t−1)); dummies COVID sin interactuar; trimestres útiles anteriores: 33; posteriores: 68 |
| Chow 2020T2 | 28,123 | < 0,001 | falla | Wald HAC con interacciones de 8 términos (constante, ρ, los cuatro controles, ΔFFR(t) y ΔFFR(t−1)); dummies COVID sin interactuar; trimestres útiles anteriores: 80; posteriores: 21; el tamaño empírico del contraste puede diferir del 5 % nominal |
| CUSUM | — | — | pasa | los trimestres con dummy de impulso no aportan residuo recursivo |
