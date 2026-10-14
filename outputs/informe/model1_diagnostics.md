VIF no es una prueba con p-valor. En CUSUM, la salida del modelo no exporta un estadístico ni p-valor; se informa el veredicto. Los vacíos o guiones no representan ceros.

Las celdas vacías indican que no se proporciona información adicional para esa prueba. Los resultados se presentan en el panel de estadísticos y veredictos anterior.

| Prueba | Estadístico | p | Veredicto | Nota |
| --- | --- | --- | --- | --- |
| Breusch-Godfrey | 3,252 | 0,517 | pasa |  |
| Breusch-Pagan | 21,981 | 0,015 | falla |  |
| White | 91,756 | < 0,001 | falla |  |
| Jarque-Bera | 461,908 | < 0,001 | falla |  |
| RESET | 6,021 | 0,003 | falla |  |
| VIF (Dependiente rezagada) | 3,174 |  | sin alerta |  |
| VIF (PIB (crecimiento)) | 3,280 |  | sin alerta |  |
| VIF (Cambio del desempleo) | 36,811 |  | alerta |  |
| VIF (Inflación) | 1,329 |  | sin alerta |  |
| VIF (Cambio de la tasa) | 1,343 |  | sin alerta |  |
| VIF (Crédito rezagado) | 1,604 |  | sin alerta |  |
| Chow 2008T3 | 24,987 | < 0,001 | falla | Wald HAC con interacciones de la constante, ρ y β₁–β₅; dummies COVID sin interactuar |
| Chow 2020T2 | 15,155 | 0,034 | falla | Wald HAC con interacciones de la constante, ρ y β₁–β₅; dummies COVID sin interactuar; quedan 21 trimestres posteriores útiles para 7 restricciones: el tamaño empírico del contraste puede diferir del 5 % nominal |
| CUSUM |  |  | pasa | los trimestres con dummy de impulso no aportan residuo recursivo |

Fuente: FRED; elaboración propia.
Cifras redondeadas a tres decimales. La fuente original conserva la precisión completa.
Los p-valores inferiores a 0,001 se muestran como < 0,001.
