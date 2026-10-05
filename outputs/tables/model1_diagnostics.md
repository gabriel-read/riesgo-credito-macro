| prueba | estadístico | p_valor | veredicto | nota |
| --- | --- | --- | --- | --- |
| Breusch-Godfrey | 3,252 | 0,517 | pasa |  |
| Breusch-Pagan | 21,981 | 0,015 | falla |  |
| White | 91,756 | < 0,001 | falla |  |
| Jarque-Bera | 461,908 | < 0,001 | falla |  |
| RESET | 6,021 | 0,003 | falla |  |
| VIF (y_lag) | 3,174 | — | sin alerta |  |
| VIF (gdp_growth) | 3,280 | — | sin alerta |  |
| VIF (d_unemp) | 36,811 | — | alerta |  |
| VIF (inflation) | 1,329 | — | sin alerta |  |
| VIF (d_ffr) | 1,343 | — | sin alerta |  |
| VIF (credit_growth) | 1,604 | — | sin alerta |  |
| Chow 2008Q3 | 24,987 | < 0,001 | falla | Wald HAC con interacciones de la constante, ρ y β₁–β₅; dummies COVID sin interactuar |
| Chow 2020Q2 | 15,155 | 0,034 | falla | Wald HAC con interacciones de la constante, ρ y β₁–β₅; dummies COVID sin interactuar |
| CUSUM | — | — | pasa | los trimestres con dummy de impulso no aportan residuo recursivo |
