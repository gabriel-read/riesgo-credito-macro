| limitacion | detalle | origen |
| --- | --- | --- |
| Endogeneidad de la tasa de fondos federales | La Fed reacciona a la economía y los controles van rezagados un trimestre, por lo que ΔFFR(t) conserva esa reacción: θ0, S y β_h pueden arrastrar esa endogeneidad. | fija |
| ΔFFR es una variación observada, no un shock identificado | La asociación dinámica entre ΔFFR y la morosidad no identifica el efecto de la política monetaria. | fija |
| Tramos de tasa cero | En los tramos con promedio trimestral de la tasa ≤ 0,25 % ΔFFR casi no varía, y los θ_j se identifican con pocos trimestres; R3 excluye esos tramos. | fija |
| COVID y proyecciones locales | Las dummies COVID neutralizan 2020T2–2021T1 en la principal, pero las ventanas de resultado de las proyecciones locales (t + h) que tocan ese período arrastran su efecto sin dummy. | fija |
| Efectos base de 2021T2–2022T2 sin dummy | El rebote interanual del PIB, que entra en 2021T3–2022T2 por el rezago, y el crédito del PPP, que entra en 2021T2–2022T1, no llevan dummy; R2 (sin 2020–2021) sirve de contraste. | fija |
| No estacionariedad de π y CRED(t−4) | π y CRED(t−4) figuran «no I(0)» en la spec 001 y entran en su forma fija: la regresión es desbalanceada y los Wald pueden no seguir su distribución asintótica. | fija |
| Granger mide precedencia | La prueba de Granger mide precedencia temporal condicional a los rezagos incluidos; no identifica el efecto de la política monetaria. | fija |
| Inferencia condicional al K elegido | K se elige con los mismos datos con que se estima, y la inferencia posterior no incorpora la incertidumbre de esa elección. | fija |
| Breusch-Pagan: falla | estadístico 33,784, p < 0,001; se reporta y se discute qué implica para las conclusiones | detectada |
| White: falla | estadístico 90,710, p < 0,001; se reporta y se discute qué implica para las conclusiones | detectada |
| Jarque-Bera: falla | estadístico 209,207, p < 0,001; se reporta y se discute qué implica para las conclusiones | detectada |
| RESET: falla | estadístico 10,448, p < 0,001; se reporta y se discute qué implica para las conclusiones | detectada |
| VIF (d_unemp_l1): alerta | estadístico 33,154; posible multicolinealidad: se reporta y no se elimina ningún regresor | detectada |
| Chow 2020T2: falla | estadístico 28,123, p < 0,001; Wald HAC con interacciones de 8 términos (constante, ρ, ΔFFR(t..t−1) y los cuatro controles); dummies COVID sin interactuar; trimestres útiles anteriores: 80; posteriores: 21; el tamaño empírico del contraste puede diferir del 5 % nominal | detectada |
| Regresores no I(0) | π(t−1), CRED(t−4): no son I(0) según la regla de la spec 001; entran en su forma fija y su no estacionariedad residual se declara como limitación. | detectada |
| Rezagos de ΔFFR o ΔDR desde 2020T2–2021T1 sin dummy | En 2020T3–2021T2 de la muestra principal, algún rezago de ΔFFR o de ΔDR sale de 2020T2–2021T1 y esos rezagos no llevan dummy propia. | detectada |
