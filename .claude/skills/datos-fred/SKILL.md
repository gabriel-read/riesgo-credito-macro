---
name: datos-fred
description: Úsala siempre que descargues, transformes, agregues o revises datos de FRED en este proyecto (spec 001 y cualquier tarea que toque data/, las series o las transformaciones).
---

# Datos de FRED — reglas del proyecto

## Series
| Concepto | Serie | Frecuencia original | Transformación trimestral |
|---|---|---|---|
| Morosidad (dependiente) | DRALACBS | Trimestral, fin de periodo, desestacionalizada | Nivel; Δ o logit ln(DR/(100−DR)) según la spec |
| Morosidad sin desestacionalizar (robustez) | DRALACBN | Trimestral | Igual que la dependiente |
| Sub-carteras (robustez) | DRCLACBS, DRBLACBS, DRSREACBS | Trimestral | Igual que la dependiente |
| PIB real | GDPC1 | Trimestral | 100·(ln Y(t) − ln Y(t−4)) |
| PIB nominal (el de la guía) | GDP | Trimestral | Igual que el PIB real |
| Desempleo | UNRATE | Mensual | Promedio del trimestre |
| Inflación | CPIAUCSL | Mensual | Promedio del trimestre → 100·(ln P(t) − ln P(t−4)) |
| Tasa de fondos federales | FEDFUNDS | Mensual | Promedio del trimestre; Δ en pp |
| Crédito | LOANS | Mensual | Promedio del trimestre → 100·(ln L(t) − ln L(t−4)) |
| Castigos (extensión) | CORALACBS | Trimestral | Nivel |
| Recesiones NBER (solo gráficos) | USREC | Mensual | 1 si algún mes del trimestre está en recesión |

## Reglas
- Descarga desde 1998-01-01 para calcular variaciones interanuales en 2000T1; la muestra de estimación empieza en 2000T1 y termina en el último trimestre común a todas las series.
- Guarda cada descarga cruda en `data/raw/<SERIE>_<AAAA-MM-DD>.csv` (fecha de descarga) y nunca la edites. Registra cada descarga en `data/raw/manifest.csv` (serie, fecha de descarga, filas, primera y última observación); el procesamiento usa la descarga registrada más reciente.
- Fuente principal: pandas-datareader ≥ 0.11 (`web.DataReader(series, "fred", start, end)`). Respaldo sin clave: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIE>`.
- Fechas: FRED fecha el trimestre en su primer día (`2026-04-01` = 2026T2). Las mensuales se agregan por trimestre calendario con la media.
- Un trimestre con menos de 3 meses solo se acepta si está documentado. Caso conocido (verifícalo al descargar): octubre 2025 falta en CPIAUCSL y UNRATE por el cierre del gobierno de EE. UU.; 2025T4 se promedia con noviembre y diciembre. Cualquier otro faltante detiene el pipeline con un error claro.
- Nunca imputes, interpoles, rellenes hacia adelante ni hagas dropna sin que la spec lo diga.
- La morosidad es dato de fin de periodo; el resto son promedios del trimestre. Documenta esa mezcla en el informe (sección 3.1).

## Checklist de revisión
- [ ] ¿Cada serie del manifiesto tiene fecha de descarga y el rango esperado?
- [ ] ¿La muestra final va de 2000T1 al último trimestre común, sin huecos?
- [ ] ¿2025T4 usa dos meses en CPI y desempleo, y está documentado?
- [ ] ¿Las variaciones interanuales usan t−4 y no t−1?
- [ ] ¿Algún relleno, interpolación o dropna silencioso?
- [ ] ¿Los tests corren sin red, sobre `data/raw/` congelado?

## Al terminar
Indica qué puntos del checklist comprobaste y cómo.
