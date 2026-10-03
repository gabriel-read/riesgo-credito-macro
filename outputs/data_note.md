## 1. Series descargadas

| Código | Nombre | Fuente | Unidad | Frecuencia original | Rango descargado | Fecha descarga | Tratamiento trimestral |
|--------|--------|--------|--------|---------------------|------------------|----------------|----------------------|
| DRALACBS | Tasa de morosidad — todos los préstamos, bancos comerciales | FRED, vía pandas-datareader | porcentaje | trimestral | 1998-01-01 a 2026-04-01 | 2026-10-02 00:00:00 | dato de fin de periodo |
| GDPC1 | PIB real de Estados Unidos | FRED, vía pandas-datareader | miles de millones de dólares encadenados (año base según FRED) | trimestral | 1998-01-01 a 2026-04-01 | 2026-10-02 00:00:00 | dato de fin de periodo |
| GDP | PIB nominal de Estados Unidos | FRED, vía pandas-datareader | miles de millones de dólares | trimestral | 1998-01-01 a 2026-04-01 | 2026-10-02 00:00:00 | dato de fin de periodo |
| UNRATE | Tasa de desempleo de Estados Unidos | FRED, vía pandas-datareader | porcentaje | mensual | 1998-01-01 a 2026-09-01 | 2026-10-02 00:00:00 | media de los meses del trimestre |
| CPIAUCSL | Índice de precios al consumidor — todos los artículos, zonas urbanas | FRED, vía pandas-datareader | índice (1982-1984 = 100) | mensual | 1998-01-01 a 2026-08-01 | 2026-10-02 00:00:00 | media de los meses del trimestre |
| FEDFUNDS | Tasa efectiva de fondos federales | FRED, vía pandas-datareader | porcentaje | mensual | 1998-01-01 a 2026-09-01 | 2026-10-02 00:00:00 | media de los meses del trimestre |
| LOANS | Préstamos y arrendamientos en crédito bancario, bancos comerciales | FRED, vía pandas-datareader | miles de millones de dólares | mensual | 1998-01-01 a 2026-08-01 | 2026-10-02 00:00:00 | media de los meses del trimestre |
| DRALACBN | Tasa de morosidad sin desestacionalizar — todos los préstamos, bancos comerciales | FRED, vía pandas-datareader | porcentaje | trimestral | 1998-01-01 a 2026-04-01 | 2026-10-02 00:00:00 | dato de fin de periodo |
| DRCLACBS | Tasa de morosidad — tarjetas de crédito, bancos comerciales | FRED, vía pandas-datareader | porcentaje | trimestral | 1998-01-01 a 2026-04-01 | 2026-10-02 00:00:00 | dato de fin de periodo |
| DRBLACBS | Tasa de morosidad — préstamos empresariales, bancos comerciales | FRED, vía pandas-datareader | porcentaje | trimestral | 1998-01-01 a 2026-04-01 | 2026-10-02 00:00:00 | dato de fin de periodo |
| DRSREACBS | Tasa de morosidad — préstamos inmobiliarios, bancos comerciales | FRED, vía pandas-datareader | porcentaje | trimestral | 1998-01-01 a 2026-04-01 | 2026-10-02 00:00:00 | dato de fin de periodo |
| CORALACBS | Tasa de castigos — todos los préstamos, bancos comerciales | FRED, vía pandas-datareader | porcentaje | trimestral | 1998-01-01 a 2026-04-01 | 2026-10-02 00:00:00 | dato de fin de periodo |
| USREC | Indicador de recesión NBER para Estados Unidos | FRED, vía pandas-datareader | indicador (1 = recesión) | mensual | 1998-01-01 a 2026-09-01 | 2026-10-02 00:00:00 | 1 si algún mes del trimestre está en recesión |

## 2. Muestra de estimación

La muestra de estimación va de **2000T1** a **2026T2**.

**Trimestres excluidos al final de la muestra:**
- 2026T3: DRALACBS (sin dato)
- 2026T3: GDPC1 (sin dato)
- 2026T3: GDP (sin dato)
- 2026T3: CPIAUCSL (incompleto)
- 2026T3: LOANS (incompleto)

## 3. Tratamiento de 2025T4 (CPIAUCSL y UNRATE)

- **CPIAUCSL**: octubre 2025 no disponible (marcador de faltante de FRED). El promedio de 2025T4 se calcula con noviembre y diciembre únicamente (**RF-11**).
- **UNRATE**: octubre 2025 no disponible (marcador de faltante de FRED). El promedio de 2025T4 se calcula con noviembre y diciembre únicamente (**RF-11**).

**Cálculos afectados en la muestra**: el nivel y la diferencia trimestral de 2025T4, la diferencia trimestral de 2026T1, y la variación interanual de 2025T4 (y de 2026T4 en adelante, si entra en la muestra) usan este promedio de dos meses para CPIAUCSL y UNRATE.

## 4. Mezcla de frecuencias

Las series de morosidad (DRALACBS, DRALACBN, DRCLACBS, DRBLACBS, DRSREACBS) y de castigos (CORALACBS) son **datos de fin de periodo** (valor del último mes del trimestre). Las series macroeconómicas mensuales (UNRATE, CPIAUCSL, FEDFUNDS, LOANS) se promedian en el trimestre calendario (**media de los meses del trimestre**). USREC es indicador: 1 si algún mes del trimestre está en recesión.

## 5. Por qué LOANS mide el crédito

LOANS (Préstamos y arrendamientos en crédito bancario, bancos comerciales, H.8) cubre el mismo universo de bancos que el denominador de DRALACBS. Se usa su **variación interanual** como proxy del crecimiento del crédito bancario.

## 6. Por qué FEDFUNDS entra en nivel y en diferencia trimestral

El **nivel** (FEDFUNDS) mide la postura de la política monetaria. La **diferencia trimestral** (FEDFUNDS_D) captura el «cambio en la FFR» que solicita la sección 3.4 de la guía. Qué versión entra en cada modelo lo deciden las specs 003 y 004.