::: {.compact-body-table}

**Tabla 4**

*Modelo I — diagnósticos*

Tabla completa: [Anexo B, AT-M1-DIAGNOSTICS](#at-m1-diagnostics).

| Prueba | Estadístico | p | Veredicto |
| --- | --- | --- | --- |
| Breusch-Godfrey | 3,252 | 0,517 | pasa |
| Breusch-Pagan | 21,981 | 0,015 | falla |
| White | 91,756 | < 0,001 | falla |
| Jarque-Bera | 461,908 | < 0,001 | falla |
| RESET | 6,021 | 0,003 | falla |
| VIF (Dependiente rezagada) | 3,174 |  | sin alerta |
| VIF (PIB (crecimiento)) | 3,280 |  | sin alerta |
| VIF (Cambio del desempleo) | 36,811 |  | alerta |
| VIF (Inflación) | 1,329 |  | sin alerta |
| VIF (Cambio de la tasa) | 1,343 |  | sin alerta |
| VIF (Crédito rezagado) | 1,604 |  | sin alerta |
| Chow 2008T3 | 24,987 | < 0,001 | falla |
| Chow 2020T2 | 15,155 | 0,034 | falla |
| CUSUM |  |  | pasa |

Fuente: FRED; elaboración propia.
Cifras redondeadas a tres decimales. La fuente original conserva la precisión completa.
Los p-valores inferiores a 0,001 se muestran como < 0,001.

VIF no es una prueba con p-valor. CUSUM no exporta estadístico ni p-valor en esta salida; los vacíos no representan ceros.

:::
