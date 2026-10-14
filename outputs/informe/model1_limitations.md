| Limitación | Detalle | Origen |
| --- | --- | --- |
| Endogeneidad de la tasa de fondos federales | La Fed reacciona a la economía: ΔFFR se asocia con la morosidad, pero esa asociación no identifica el efecto de la política monetaria. | fija |
| Simultaneidad de los regresores contemporáneos | PIB, desempleo, inflación y ΔFFR se determinan junto con la morosidad del mismo trimestre: los coeficientes son asociaciones condicionales, no efectos aislados. | fija |
| Potencia baja de Diebold-Mariano | La evaluación fuera de muestra tiene pocos trimestres, por lo que la prueba de Diebold-Mariano tiene poca potencia. | fija |
| Efectos base de 2021T2–2022T1 sin dummy | El rebote interanual del PIB y el crecimiento del crédito asociado al programa PPP, que entra en CRED(t−4) entre 2021T2 y 2022T1, no llevan dummy; la robustez R1 (sin 2020–2021) sirve de contraste. | fija |
| Regresores no I(0) | π, CRED(t−4): no son I(0) según la regla de la especificación pre-registrada; entran en su forma fija y su no estacionariedad residual se declara como limitación del modelo. | detectada |
| Dependientes con orden «posible I(2)» | drsreacbs (R3_drsreacbs), dralacbs_logit (R5) | detectada |
| Breusch-Pagan: falla | estadístico 21,981, p = 0,015; se reporta y se discute qué implica para las conclusiones | detectada |
| White: falla | estadístico 91,756, p < 0,001; se reporta y se discute qué implica para las conclusiones | detectada |
| Jarque-Bera: falla | estadístico 461,908, p < 0,001; se reporta y se discute qué implica para las conclusiones | detectada |
| RESET: falla | estadístico 6,021, p = 0,003; se reporta y se discute qué implica para las conclusiones | detectada |
| VIF (Cambio del desempleo): alerta | estadístico 36,811; con las dummies COVID dentro de X, casi toda la varianza de ΔU es el salto de 2020T2, que su dummy absorbe: no es colinealidad entre regresores macro, sino que el coeficiente de ΔU se identifica con la variación fuera de la COVID; se reporta y no se elimina ningún regresor | detectada |
| Chow 2008T3: falla | estadístico 24,987, p < 0,001; Wald HAC con interacciones de la constante, ρ y β₁–β₅; dummies COVID sin interactuar | detectada |
| Chow 2020T2: falla | estadístico 15,155, p = 0,034; Wald HAC con interacciones de la constante, ρ y β₁–β₅; dummies COVID sin interactuar; quedan 21 trimestres posteriores útiles para 7 restricciones: el tamaño empírico del contraste puede diferir del 5 % nominal | detectada |
| Variante R8 no estimada | sin historia anterior a 2000T1 | detectada |

Fuente: FRED; elaboración propia.
