# Interfaz para la redacción de 006

Archivo generado por `uv run python -m src.pipeline report`; no editar a mano.

Fuente única de variables: `report/_variables.yml`. `_variables.yml` de la raíz es solo su espejo generado.
Las rutas siguientes son relativas a la raíz del proyecto Quarto, dentro de la copia activa de Orca.

## Variables canónicas

Los valores se conservan tal como los entrega la fuente. Las unidades e interpretaciones se consultan en la spec de origen y en los campos de unidad de los CSV; no se infieren de una cifra aislada.

| Clave | Valor o estructura | Descripción y origen | Uso |
| --- | --- | --- | --- |
| `datos.muestra_inicio` | 2000T1 | muestra inicio; `001-datos` | `{{< var datos.muestra_inicio >}}` |
| `datos.muestra_fin` | 2026T2 | muestra fin; `001-datos` | `{{< var datos.muestra_fin >}}` |
| `datos.n_trimestres` | 106 | n trimestres; `001-datos` | `{{< var datos.n_trimestres >}}` |
| `datos.n_series` | 13 | n series; `001-datos` | `{{< var datos.n_series >}}` |
| `datos.fecha_descarga` | 2026-10-02 | fecha descarga; `001-datos` | `{{< var datos.fecha_descarga >}}` |
| `datos.trimestres_excluidos` | 2026T3 | trimestres excluidos; `001-datos` | `{{< var datos.trimestres_excluidos >}}` |
| `datos.cpiaucsl_2025t4_meses` | 2 | cpiaucsl 2025t4 meses; `001-datos` | `{{< var datos.cpiaucsl_2025t4_meses >}}` |
| `datos.unrate_2025t4_meses` | 2 | unrate 2025t4 meses; `001-datos` | `{{< var datos.unrate_2025t4_meses >}}` |
| `datos.dralacbs_media` | 2,63 | dralacbs media; `001-datos` | `{{< var datos.dralacbs_media >}}` |
| `datos.dralacbs_desv` | 1,64 | dralacbs desv; `001-datos` | `{{< var datos.dralacbs_desv >}}` |
| `datos.dralacbs_max` | 7,35 | dralacbs max; `001-datos` | `{{< var datos.dralacbs_max >}}` |
| `datos.dralacbs_max_trimestre` | 2010T1 | dralacbs max trimestre; `001-datos` | `{{< var datos.dralacbs_max_trimestre >}}` |
| `datos.dralacbs_min` | 1,19 | dralacbs min; `001-datos` | `{{< var datos.dralacbs_min >}}` |
| `datos.dralacbs_min_trimestre` | 2022T3 | dralacbs min trimestre; `001-datos` | `{{< var datos.dralacbs_min_trimestre >}}` |
| `datos.dralacbs_ultimo` | 1,42 | dralacbs ultimo; `001-datos` | `{{< var datos.dralacbs_ultimo >}}` |
| `datos.unrate_max` | 13,00 | unrate max; `001-datos` | `{{< var datos.unrate_max >}}` |
| `datos.unrate_max_trimestre` | 2020T2 | unrate max trimestre; `001-datos` | `{{< var datos.unrate_max_trimestre >}}` |
| `datos.fedfunds_max` | 6,52 | fedfunds max; `001-datos` | `{{< var datos.fedfunds_max >}}` |
| `datos.fedfunds_ultimo` | 3,63 | fedfunds ultimo; `001-datos` | `{{< var datos.fedfunds_ultimo >}}` |
| `datos.decision.dralacbs` | ambigua (primera diferencia) | dralacbs; `001-datos` | `{{< var datos.decision.dralacbs >}}` |
| `datos.decision.dralacbs_logit` | primera diferencia | dralacbs logit; `001-datos` | `{{< var datos.decision.dralacbs_logit >}}` |
| `datos.decision.dralacbn` | ambigua (primera diferencia) | dralacbn; `001-datos` | `{{< var datos.decision.dralacbn >}}` |
| `datos.decision.dralacbn_logit` | ambigua (primera diferencia) | dralacbn logit; `001-datos` | `{{< var datos.decision.dralacbn_logit >}}` |
| `datos.decision.drclacbs` | primera diferencia | drclacbs; `001-datos` | `{{< var datos.decision.drclacbs >}}` |
| `datos.decision.drclacbs_logit` | primera diferencia | drclacbs logit; `001-datos` | `{{< var datos.decision.drclacbs_logit >}}` |
| `datos.decision.drblacbs` | primera diferencia | drblacbs; `001-datos` | `{{< var datos.decision.drblacbs >}}` |
| `datos.decision.drblacbs_logit` | ambigua (primera diferencia) | drblacbs logit; `001-datos` | `{{< var datos.decision.drblacbs_logit >}}` |
| `datos.decision.drsreacbs` | ambigua (primera diferencia) | drsreacbs; `001-datos` | `{{< var datos.decision.drsreacbs >}}` |
| `datos.decision.drsreacbs_logit` | ambigua (primera diferencia) | drsreacbs logit; `001-datos` | `{{< var datos.decision.drsreacbs_logit >}}` |
| `datos.decision.gdpc1_yoy` | niveles | gdpc1 yoy; `001-datos` | `{{< var datos.decision.gdpc1_yoy >}}` |
| `datos.decision.gdp_yoy` | niveles | gdp yoy; `001-datos` | `{{< var datos.decision.gdp_yoy >}}` |
| `datos.decision.cpiaucsl_yoy` | ambigua (primera diferencia) | cpiaucsl yoy; `001-datos` | `{{< var datos.decision.cpiaucsl_yoy >}}` |
| `datos.decision.loans_yoy` | ambigua (primera diferencia) | loans yoy; `001-datos` | `{{< var datos.decision.loans_yoy >}}` |
| `datos.decision.unrate` | niveles | unrate; `001-datos` | `{{< var datos.decision.unrate >}}` |
| `datos.decision.fedfunds` | niveles | fedfunds; `001-datos` | `{{< var datos.decision.fedfunds >}}` |
| `datos.decision.coralacbs` | niveles | coralacbs; `001-datos` | `{{< var datos.decision.coralacbs >}}` |
| `datos.orden.dralacbs` | I(1) | dralacbs; `001-datos` | `{{< var datos.orden.dralacbs >}}` |
| `datos.orden.dralacbs_logit` | posible I(2) | dralacbs logit; `001-datos` | `{{< var datos.orden.dralacbs_logit >}}` |
| `datos.orden.dralacbn` | I(1) | dralacbn; `001-datos` | `{{< var datos.orden.dralacbn >}}` |
| `datos.orden.dralacbn_logit` | posible I(2) | dralacbn logit; `001-datos` | `{{< var datos.orden.dralacbn_logit >}}` |
| `datos.orden.drclacbs` | I(1) | drclacbs; `001-datos` | `{{< var datos.orden.drclacbs >}}` |
| `datos.orden.drclacbs_logit` | I(1) | drclacbs logit; `001-datos` | `{{< var datos.orden.drclacbs_logit >}}` |
| `datos.orden.drblacbs` | I(1) | drblacbs; `001-datos` | `{{< var datos.orden.drblacbs >}}` |
| `datos.orden.drblacbs_logit` | I(1) | drblacbs logit; `001-datos` | `{{< var datos.orden.drblacbs_logit >}}` |
| `datos.orden.drsreacbs` | posible I(2) | drsreacbs; `001-datos` | `{{< var datos.orden.drsreacbs >}}` |
| `datos.orden.drsreacbs_logit` | posible I(2) | drsreacbs logit; `001-datos` | `{{< var datos.orden.drsreacbs_logit >}}` |
| `datos.orden.gdpc1_yoy` | I(0) | gdpc1 yoy; `001-datos` | `{{< var datos.orden.gdpc1_yoy >}}` |
| `datos.orden.gdp_yoy` | I(0) | gdp yoy; `001-datos` | `{{< var datos.orden.gdp_yoy >}}` |
| `datos.orden.cpiaucsl_yoy` | I(1) | cpiaucsl yoy; `001-datos` | `{{< var datos.orden.cpiaucsl_yoy >}}` |
| `datos.orden.loans_yoy` | I(1) | loans yoy; `001-datos` | `{{< var datos.orden.loans_yoy >}}` |
| `datos.orden.unrate` | I(0) | unrate; `001-datos` | `{{< var datos.orden.unrate >}}` |
| `datos.orden.fedfunds` | I(0) | fedfunds; `001-datos` | `{{< var datos.orden.fedfunds >}}` |
| `datos.orden.coralacbs` | I(0) | coralacbs; `001-datos` | `{{< var datos.orden.coralacbs >}}` |
| `datos.n_ambiguas` | 8 | n ambiguas; `001-datos` | `{{< var datos.n_ambiguas >}}` |
| `modelo1.estimador` | MCO con errores Newey-West (HAC, kernel de Bartlett) | estimador; `003-modelo-i` | `{{< var modelo1.estimador >}}` |
| `modelo1.forma_y` | primera diferencia | forma y; `003-modelo-i` | `{{< var modelo1.forma_y >}}` |
| `modelo1.muestra_inicio` | 2000T1 | muestra inicio; `003-modelo-i` | `{{< var modelo1.muestra_inicio >}}` |
| `modelo1.muestra_fin` | 2026T2 | muestra fin; `003-modelo-i` | `{{< var modelo1.muestra_fin >}}` |
| `modelo1.n_obs` | 106 | n obs; `003-modelo-i` | `{{< var modelo1.n_obs >}}` |
| `modelo1.n_parametros` | 11 | n parametros; `003-modelo-i` | `{{< var modelo1.n_parametros >}}` |
| `modelo1.rezagos_hac` | 4 | rezagos hac; `003-modelo-i` | `{{< var modelo1.rezagos_hac >}}` |
| `modelo1.dummies_covid` | 2020T2, 2020T3, 2020T4 y 2021T1 | dummies covid; `003-modelo-i` | `{{< var modelo1.dummies_covid >}}` |
| `modelo1.truncamiento_espectral` | no | truncamiento espectral; `003-modelo-i` | `{{< var modelo1.truncamiento_espectral >}}` |
| `modelo1.r2` | 0,832 | r2; `003-modelo-i` | `{{< var modelo1.r2 >}}` |
| `modelo1.r2_ajustado` | 0,814 | r2 ajustado; `003-modelo-i` | `{{< var modelo1.r2_ajustado >}}` |
| `modelo1.ee_regresion` | 0,096 | ee regresion; `003-modelo-i` | `{{< var modelo1.ee_regresion >}}` |
| `modelo1.variantes.R1` | Sin 2020–2021 | R1; `003-modelo-i` | `{{< var modelo1.variantes.R1 >}}` |
| `modelo1.variantes.R2` | DRALACBN sin desestacionalizar, con dummies estacionales | R2; `003-modelo-i` | `{{< var modelo1.variantes.R2 >}}` |
| `modelo1.variantes.R3_drclacbs` | Tarjetas de crédito | R3 drclacbs; `003-modelo-i` | `{{< var modelo1.variantes.R3_drclacbs >}}` |
| `modelo1.variantes.R3_drblacbs` | Préstamos empresariales | R3 drblacbs; `003-modelo-i` | `{{< var modelo1.variantes.R3_drblacbs >}}` |
| `modelo1.variantes.R3_drsreacbs` | Préstamos inmobiliarios | R3 drsreacbs; `003-modelo-i` | `{{< var modelo1.variantes.R3_drsreacbs >}}` |
| `modelo1.variantes.R4` | PIB nominal | R4; `003-modelo-i` | `{{< var modelo1.variantes.R4 >}}` |
| `modelo1.variantes.R5` | Logit de la morosidad | R5; `003-modelo-i` | `{{< var modelo1.variantes.R5 >}}` |
| `modelo1.variantes.R6` | Crédito rezagado 8 trimestres | R6; `003-modelo-i` | `{{< var modelo1.variantes.R6 >}}` |
| `modelo1.variantes.R7` | Crédito rezagado 12 trimestres | R7; `003-modelo-i` | `{{< var modelo1.variantes.R7 >}}` |
| `modelo1.variantes.R8` | Muestra larga desde 1985T1 | R8; `003-modelo-i` | `{{< var modelo1.variantes.R8 >}}` |
| `modelo1.coef.const.coef` | -0,066 | coef; `003-modelo-i` | `{{< var modelo1.coef.const.coef >}}` |
| `modelo1.coef.const.ee` | 0,024 | ee; `003-modelo-i` | `{{< var modelo1.coef.const.ee >}}` |
| `modelo1.coef.const.p` | 0,006 | p; `003-modelo-i` | `{{< var modelo1.coef.const.p >}}` |
| `modelo1.coef.const.ic_inf` | -0,112 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.const.ic_inf >}}` |
| `modelo1.coef.const.ic_sup` | -0,019 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.const.ic_sup >}}` |
| `modelo1.coef.y_lag.coef` | 0,626 | coef; `003-modelo-i` | `{{< var modelo1.coef.y_lag.coef >}}` |
| `modelo1.coef.y_lag.ee` | 0,093 | ee; `003-modelo-i` | `{{< var modelo1.coef.y_lag.ee >}}` |
| `modelo1.coef.y_lag.p` | < 0,001 | p; `003-modelo-i` | `{{< var modelo1.coef.y_lag.p >}}` |
| `modelo1.coef.y_lag.ic_inf` | 0,444 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.y_lag.ic_inf >}}` |
| `modelo1.coef.y_lag.ic_sup` | 0,809 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.y_lag.ic_sup >}}` |
| `modelo1.coef.gdp_growth.coef` | -0,016 | coef; `003-modelo-i` | `{{< var modelo1.coef.gdp_growth.coef >}}` |
| `modelo1.coef.gdp_growth.ee` | 0,010 | ee; `003-modelo-i` | `{{< var modelo1.coef.gdp_growth.ee >}}` |
| `modelo1.coef.gdp_growth.p` | 0,110 | p; `003-modelo-i` | `{{< var modelo1.coef.gdp_growth.p >}}` |
| `modelo1.coef.gdp_growth.ic_inf` | -0,036 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.gdp_growth.ic_inf >}}` |
| `modelo1.coef.gdp_growth.ic_sup` | 0,004 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.gdp_growth.ic_sup >}}` |
| `modelo1.coef.d_unemp.coef` | 0,077 | coef; `003-modelo-i` | `{{< var modelo1.coef.d_unemp.coef >}}` |
| `modelo1.coef.d_unemp.ee` | 0,062 | ee; `003-modelo-i` | `{{< var modelo1.coef.d_unemp.ee >}}` |
| `modelo1.coef.d_unemp.p` | 0,214 | p; `003-modelo-i` | `{{< var modelo1.coef.d_unemp.p >}}` |
| `modelo1.coef.d_unemp.ic_inf` | -0,045 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.d_unemp.ic_inf >}}` |
| `modelo1.coef.d_unemp.ic_sup` | 0,199 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.d_unemp.ic_sup >}}` |
| `modelo1.coef.inflation.coef` | 0,020 | coef; `003-modelo-i` | `{{< var modelo1.coef.inflation.coef >}}` |
| `modelo1.coef.inflation.ee` | 0,006 | ee; `003-modelo-i` | `{{< var modelo1.coef.inflation.ee >}}` |
| `modelo1.coef.inflation.p` | 0,001 | p; `003-modelo-i` | `{{< var modelo1.coef.inflation.p >}}` |
| `modelo1.coef.inflation.ic_inf` | 0,008 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.inflation.ic_inf >}}` |
| `modelo1.coef.inflation.ic_sup` | 0,032 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.inflation.ic_sup >}}` |
| `modelo1.coef.d_ffr.coef` | -0,044 | coef; `003-modelo-i` | `{{< var modelo1.coef.d_ffr.coef >}}` |
| `modelo1.coef.d_ffr.ee` | 0,040 | ee; `003-modelo-i` | `{{< var modelo1.coef.d_ffr.ee >}}` |
| `modelo1.coef.d_ffr.p` | 0,269 | p; `003-modelo-i` | `{{< var modelo1.coef.d_ffr.p >}}` |
| `modelo1.coef.d_ffr.ic_inf` | -0,122 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.d_ffr.ic_inf >}}` |
| `modelo1.coef.d_ffr.ic_sup` | 0,034 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.d_ffr.ic_sup >}}` |
| `modelo1.coef.credit_growth.coef` | 0,010 | coef; `003-modelo-i` | `{{< var modelo1.coef.credit_growth.coef >}}` |
| `modelo1.coef.credit_growth.ee` | 0,003 | ee; `003-modelo-i` | `{{< var modelo1.coef.credit_growth.ee >}}` |
| `modelo1.coef.credit_growth.p` | < 0,001 | p; `003-modelo-i` | `{{< var modelo1.coef.credit_growth.p >}}` |
| `modelo1.coef.credit_growth.ic_inf` | 0,005 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.credit_growth.ic_inf >}}` |
| `modelo1.coef.credit_growth.ic_sup` | 0,015 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.credit_growth.ic_sup >}}` |
| `modelo1.coef.covid_2020q2.coef` | -0,888 | coef; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q2.coef >}}` |
| `modelo1.coef.covid_2020q2.ee` | 0,619 | ee; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q2.ee >}}` |
| `modelo1.coef.covid_2020q2.p` | 0,152 | p; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q2.p >}}` |
| `modelo1.coef.covid_2020q2.ic_inf` | -2,102 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q2.ic_inf >}}` |
| `modelo1.coef.covid_2020q2.ic_sup` | 0,326 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q2.ic_sup >}}` |
| `modelo1.coef.covid_2020q3.coef` | 0,322 | coef; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q3.coef >}}` |
| `modelo1.coef.covid_2020q3.ee` | 0,260 | ee; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q3.ee >}}` |
| `modelo1.coef.covid_2020q3.p` | 0,216 | p; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q3.p >}}` |
| `modelo1.coef.covid_2020q3.ic_inf` | -0,188 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q3.ic_inf >}}` |
| `modelo1.coef.covid_2020q3.ic_sup` | 0,831 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q3.ic_sup >}}` |
| `modelo1.coef.covid_2020q4.coef` | 0,094 | coef; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q4.coef >}}` |
| `modelo1.coef.covid_2020q4.ee` | 0,127 | ee; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q4.ee >}}` |
| `modelo1.coef.covid_2020q4.p` | 0,458 | p; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q4.p >}}` |
| `modelo1.coef.covid_2020q4.ic_inf` | -0,155 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q4.ic_inf >}}` |
| `modelo1.coef.covid_2020q4.ic_sup` | 0,343 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.covid_2020q4.ic_sup >}}` |
| `modelo1.coef.covid_2021q1.coef` | -0,055 | coef; `003-modelo-i` | `{{< var modelo1.coef.covid_2021q1.coef >}}` |
| `modelo1.coef.covid_2021q1.ee` | 0,031 | ee; `003-modelo-i` | `{{< var modelo1.coef.covid_2021q1.ee >}}` |
| `modelo1.coef.covid_2021q1.p` | 0,082 | p; `003-modelo-i` | `{{< var modelo1.coef.covid_2021q1.p >}}` |
| `modelo1.coef.covid_2021q1.ic_inf` | -0,116 | ic inf; `003-modelo-i` | `{{< var modelo1.coef.covid_2021q1.ic_inf >}}` |
| `modelo1.coef.covid_2021q1.ic_sup` | 0,007 | ic sup; `003-modelo-i` | `{{< var modelo1.coef.covid_2021q1.ic_sup >}}` |
| `modelo1.efectos.gdp_growth.de` | 1,778 | de; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.de >}}` |
| `modelo1.efectos.gdp_growth.impacto_pp` | -0,016 | impacto pp; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_pp >}}` |
| `modelo1.efectos.gdp_growth.impacto_pp_ee` | 0,010 | impacto pp ee; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_pp_ee >}}` |
| `modelo1.efectos.gdp_growth.impacto_pp_p` | 0,110 | impacto pp p; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_pp_p >}}` |
| `modelo1.efectos.gdp_growth.impacto_pp_ic_inf` | -0,036 | impacto pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_pp_ic_inf >}}` |
| `modelo1.efectos.gdp_growth.impacto_pp_ic_sup` | 0,004 | impacto pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_pp_ic_sup >}}` |
| `modelo1.efectos.gdp_growth.impacto_de` | -0,029 | impacto de; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_de >}}` |
| `modelo1.efectos.gdp_growth.impacto_de_ee` | 0,018 | impacto de ee; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_de_ee >}}` |
| `modelo1.efectos.gdp_growth.impacto_de_p` | 0,110 | impacto de p; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_de_p >}}` |
| `modelo1.efectos.gdp_growth.impacto_de_ic_inf` | -0,065 | impacto de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_de_ic_inf >}}` |
| `modelo1.efectos.gdp_growth.impacto_de_ic_sup` | 0,007 | impacto de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.impacto_de_ic_sup >}}` |
| `modelo1.efectos.gdp_growth.largo_pp` | -0,044 | largo pp; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_pp >}}` |
| `modelo1.efectos.gdp_growth.largo_pp_ee` | 0,022 | largo pp ee; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_pp_ee >}}` |
| `modelo1.efectos.gdp_growth.largo_pp_p` | 0,043 | largo pp p; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_pp_p >}}` |
| `modelo1.efectos.gdp_growth.largo_pp_ic_inf` | -0,086 | largo pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_pp_ic_inf >}}` |
| `modelo1.efectos.gdp_growth.largo_pp_ic_sup` | -0,001 | largo pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_pp_ic_sup >}}` |
| `modelo1.efectos.gdp_growth.largo_de` | -0,078 | largo de; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_de >}}` |
| `modelo1.efectos.gdp_growth.largo_de_ee` | 0,038 | largo de ee; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_de_ee >}}` |
| `modelo1.efectos.gdp_growth.largo_de_p` | 0,043 | largo de p; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_de_p >}}` |
| `modelo1.efectos.gdp_growth.largo_de_ic_inf` | -0,153 | largo de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_de_ic_inf >}}` |
| `modelo1.efectos.gdp_growth.largo_de_ic_sup` | -0,002 | largo de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.gdp_growth.largo_de_ic_sup >}}` |
| `modelo1.efectos.d_unemp.de` | 0,308 | de; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.de >}}` |
| `modelo1.efectos.d_unemp.impacto_pp` | 0,077 | impacto pp; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_pp >}}` |
| `modelo1.efectos.d_unemp.impacto_pp_ee` | 0,062 | impacto pp ee; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_pp_ee >}}` |
| `modelo1.efectos.d_unemp.impacto_pp_p` | 0,214 | impacto pp p; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_pp_p >}}` |
| `modelo1.efectos.d_unemp.impacto_pp_ic_inf` | -0,045 | impacto pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_pp_ic_inf >}}` |
| `modelo1.efectos.d_unemp.impacto_pp_ic_sup` | 0,199 | impacto pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_pp_ic_sup >}}` |
| `modelo1.efectos.d_unemp.impacto_de` | 0,024 | impacto de; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_de >}}` |
| `modelo1.efectos.d_unemp.impacto_de_ee` | 0,019 | impacto de ee; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_de_ee >}}` |
| `modelo1.efectos.d_unemp.impacto_de_p` | 0,214 | impacto de p; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_de_p >}}` |
| `modelo1.efectos.d_unemp.impacto_de_ic_inf` | -0,014 | impacto de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_de_ic_inf >}}` |
| `modelo1.efectos.d_unemp.impacto_de_ic_sup` | 0,062 | impacto de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.impacto_de_ic_sup >}}` |
| `modelo1.efectos.d_unemp.largo_pp` | 0,207 | largo pp; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_pp >}}` |
| `modelo1.efectos.d_unemp.largo_pp_ee` | 0,137 | largo pp ee; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_pp_ee >}}` |
| `modelo1.efectos.d_unemp.largo_pp_p` | 0,131 | largo pp p; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_pp_p >}}` |
| `modelo1.efectos.d_unemp.largo_pp_ic_inf` | -0,062 | largo pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_pp_ic_inf >}}` |
| `modelo1.efectos.d_unemp.largo_pp_ic_sup` | 0,476 | largo pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_pp_ic_sup >}}` |
| `modelo1.efectos.d_unemp.largo_de` | 0,064 | largo de; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_de >}}` |
| `modelo1.efectos.d_unemp.largo_de_ee` | 0,042 | largo de ee; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_de_ee >}}` |
| `modelo1.efectos.d_unemp.largo_de_p` | 0,131 | largo de p; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_de_p >}}` |
| `modelo1.efectos.d_unemp.largo_de_ic_inf` | -0,019 | largo de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_de_ic_inf >}}` |
| `modelo1.efectos.d_unemp.largo_de_ic_sup` | 0,147 | largo de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.d_unemp.largo_de_ic_sup >}}` |
| `modelo1.efectos.inflation.de` | 1,637 | de; `003-modelo-i` | `{{< var modelo1.efectos.inflation.de >}}` |
| `modelo1.efectos.inflation.impacto_pp` | 0,020 | impacto pp; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_pp >}}` |
| `modelo1.efectos.inflation.impacto_pp_ee` | 0,006 | impacto pp ee; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_pp_ee >}}` |
| `modelo1.efectos.inflation.impacto_pp_p` | 0,001 | impacto pp p; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_pp_p >}}` |
| `modelo1.efectos.inflation.impacto_pp_ic_inf` | 0,008 | impacto pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_pp_ic_inf >}}` |
| `modelo1.efectos.inflation.impacto_pp_ic_sup` | 0,032 | impacto pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_pp_ic_sup >}}` |
| `modelo1.efectos.inflation.impacto_de` | 0,032 | impacto de; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_de >}}` |
| `modelo1.efectos.inflation.impacto_de_ee` | 0,010 | impacto de ee; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_de_ee >}}` |
| `modelo1.efectos.inflation.impacto_de_p` | 0,001 | impacto de p; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_de_p >}}` |
| `modelo1.efectos.inflation.impacto_de_ic_inf` | 0,012 | impacto de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_de_ic_inf >}}` |
| `modelo1.efectos.inflation.impacto_de_ic_sup` | 0,052 | impacto de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.inflation.impacto_de_ic_sup >}}` |
| `modelo1.efectos.inflation.largo_pp` | 0,053 | largo pp; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_pp >}}` |
| `modelo1.efectos.inflation.largo_pp_ee` | 0,011 | largo pp ee; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_pp_ee >}}` |
| `modelo1.efectos.inflation.largo_pp_p` | < 0,001 | largo pp p; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_pp_p >}}` |
| `modelo1.efectos.inflation.largo_pp_ic_inf` | 0,031 | largo pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_pp_ic_inf >}}` |
| `modelo1.efectos.inflation.largo_pp_ic_sup` | 0,075 | largo pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_pp_ic_sup >}}` |
| `modelo1.efectos.inflation.largo_de` | 0,087 | largo de; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_de >}}` |
| `modelo1.efectos.inflation.largo_de_ee` | 0,018 | largo de ee; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_de_ee >}}` |
| `modelo1.efectos.inflation.largo_de_p` | < 0,001 | largo de p; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_de_p >}}` |
| `modelo1.efectos.inflation.largo_de_ic_inf` | 0,051 | largo de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_de_ic_inf >}}` |
| `modelo1.efectos.inflation.largo_de_ic_sup` | 0,123 | largo de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.inflation.largo_de_ic_sup >}}` |
| `modelo1.efectos.d_ffr.de` | 0,452 | de; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.de >}}` |
| `modelo1.efectos.d_ffr.impacto_pp` | -0,044 | impacto pp; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_pp >}}` |
| `modelo1.efectos.d_ffr.impacto_pp_ee` | 0,040 | impacto pp ee; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_pp_ee >}}` |
| `modelo1.efectos.d_ffr.impacto_pp_p` | 0,269 | impacto pp p; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_pp_p >}}` |
| `modelo1.efectos.d_ffr.impacto_pp_ic_inf` | -0,122 | impacto pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_pp_ic_inf >}}` |
| `modelo1.efectos.d_ffr.impacto_pp_ic_sup` | 0,034 | impacto pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_pp_ic_sup >}}` |
| `modelo1.efectos.d_ffr.impacto_de` | -0,020 | impacto de; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_de >}}` |
| `modelo1.efectos.d_ffr.impacto_de_ee` | 0,018 | impacto de ee; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_de_ee >}}` |
| `modelo1.efectos.d_ffr.impacto_de_p` | 0,269 | impacto de p; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_de_p >}}` |
| `modelo1.efectos.d_ffr.impacto_de_ic_inf` | -0,055 | impacto de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_de_ic_inf >}}` |
| `modelo1.efectos.d_ffr.impacto_de_ic_sup` | 0,015 | impacto de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.impacto_de_ic_sup >}}` |
| `modelo1.efectos.d_ffr.largo_pp` | -0,117 | largo pp; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_pp >}}` |
| `modelo1.efectos.d_ffr.largo_pp_ee` | 0,092 | largo pp ee; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_pp_ee >}}` |
| `modelo1.efectos.d_ffr.largo_pp_p` | 0,202 | largo pp p; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_pp_p >}}` |
| `modelo1.efectos.d_ffr.largo_pp_ic_inf` | -0,298 | largo pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_pp_ic_inf >}}` |
| `modelo1.efectos.d_ffr.largo_pp_ic_sup` | 0,063 | largo pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_pp_ic_sup >}}` |
| `modelo1.efectos.d_ffr.largo_de` | -0,053 | largo de; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_de >}}` |
| `modelo1.efectos.d_ffr.largo_de_ee` | 0,042 | largo de ee; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_de_ee >}}` |
| `modelo1.efectos.d_ffr.largo_de_p` | 0,202 | largo de p; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_de_p >}}` |
| `modelo1.efectos.d_ffr.largo_de_ic_inf` | -0,135 | largo de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_de_ic_inf >}}` |
| `modelo1.efectos.d_ffr.largo_de_ic_sup` | 0,029 | largo de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.d_ffr.largo_de_ic_sup >}}` |
| `modelo1.efectos.credit_growth.de` | 4,114 | de; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.de >}}` |
| `modelo1.efectos.credit_growth.impacto_pp` | 0,010 | impacto pp; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_pp >}}` |
| `modelo1.efectos.credit_growth.impacto_pp_ee` | 0,003 | impacto pp ee; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_pp_ee >}}` |
| `modelo1.efectos.credit_growth.impacto_pp_p` | < 0,001 | impacto pp p; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_pp_p >}}` |
| `modelo1.efectos.credit_growth.impacto_pp_ic_inf` | 0,005 | impacto pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_pp_ic_inf >}}` |
| `modelo1.efectos.credit_growth.impacto_pp_ic_sup` | 0,015 | impacto pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_pp_ic_sup >}}` |
| `modelo1.efectos.credit_growth.impacto_de` | 0,041 | impacto de; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_de >}}` |
| `modelo1.efectos.credit_growth.impacto_de_ee` | 0,011 | impacto de ee; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_de_ee >}}` |
| `modelo1.efectos.credit_growth.impacto_de_p` | < 0,001 | impacto de p; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_de_p >}}` |
| `modelo1.efectos.credit_growth.impacto_de_ic_inf` | 0,019 | impacto de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_de_ic_inf >}}` |
| `modelo1.efectos.credit_growth.impacto_de_ic_sup` | 0,063 | impacto de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.impacto_de_ic_sup >}}` |
| `modelo1.efectos.credit_growth.largo_pp` | 0,027 | largo pp; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_pp >}}` |
| `modelo1.efectos.credit_growth.largo_pp_ee` | 0,004 | largo pp ee; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_pp_ee >}}` |
| `modelo1.efectos.credit_growth.largo_pp_p` | < 0,001 | largo pp p; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_pp_p >}}` |
| `modelo1.efectos.credit_growth.largo_pp_ic_inf` | 0,019 | largo pp ic inf; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_pp_ic_inf >}}` |
| `modelo1.efectos.credit_growth.largo_pp_ic_sup` | 0,034 | largo pp ic sup; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_pp_ic_sup >}}` |
| `modelo1.efectos.credit_growth.largo_de` | 0,109 | largo de; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_de >}}` |
| `modelo1.efectos.credit_growth.largo_de_ee` | 0,016 | largo de ee; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_de_ee >}}` |
| `modelo1.efectos.credit_growth.largo_de_p` | < 0,001 | largo de p; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_de_p >}}` |
| `modelo1.efectos.credit_growth.largo_de_ic_inf` | 0,077 | largo de ic inf; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_de_ic_inf >}}` |
| `modelo1.efectos.credit_growth.largo_de_ic_sup` | 0,142 | largo de ic sup; `003-modelo-i` | `{{< var modelo1.efectos.credit_growth.largo_de_ic_sup >}}` |
| `modelo1.efectos_nota` | Nota: DE de cada regresor (divisor n − 1, ddof = 1) sobre 102 trimestres, 2000T1–2026T2 sin 2020T2–2021T1 (C1: el modelo ya neutraliza esos trimestres con sus dummies): ΔPIB = 1,778; ΔU = 0,308; π = 1,637; ΔFFR = 0,452; CRED(t−4) = 4,114. Con Y en primera diferencia, el efecto de largo plazo es el cambio acumulado en el nivel de la morosidad ante un aumento transitorio de 1 unidad del regresor durante un trimestre. Cada efecto por 1 DE es el efecto por 1 pp multiplicado por la DE de su regresor; todos están en pp de morosidad. | efectos nota; `003-modelo-i` | `{{< var modelo1.efectos_nota >}}` |
| `modelo1.signo.gdp_growth` | sí | gdp growth; `003-modelo-i` | `{{< var modelo1.signo.gdp_growth >}}` |
| `modelo1.signo.d_unemp` | sí | d unemp; `003-modelo-i` | `{{< var modelo1.signo.d_unemp >}}` |
| `modelo1.signo.inflation` | sin contraste | inflation; `003-modelo-i` | `{{< var modelo1.signo.inflation >}}` |
| `modelo1.signo.d_ffr` | no | d ffr; `003-modelo-i` | `{{< var modelo1.signo.d_ffr >}}` |
| `modelo1.signo.credit_growth` | sí | credit growth; `003-modelo-i` | `{{< var modelo1.signo.credit_growth >}}` |
| `modelo1.diag.bg.estadistico` | 3,252 | estadistico; `003-modelo-i` | `{{< var modelo1.diag.bg.estadistico >}}` |
| `modelo1.diag.bg.p` | 0,517 | p; `003-modelo-i` | `{{< var modelo1.diag.bg.p >}}` |
| `modelo1.diag.bg.veredicto` | pasa | veredicto; `003-modelo-i` | `{{< var modelo1.diag.bg.veredicto >}}` |
| `modelo1.diag.bp.estadistico` | 21,981 | estadistico; `003-modelo-i` | `{{< var modelo1.diag.bp.estadistico >}}` |
| `modelo1.diag.bp.p` | 0,015 | p; `003-modelo-i` | `{{< var modelo1.diag.bp.p >}}` |
| `modelo1.diag.bp.veredicto` | falla | veredicto; `003-modelo-i` | `{{< var modelo1.diag.bp.veredicto >}}` |
| `modelo1.diag.white.estadistico` | 91,756 | estadistico; `003-modelo-i` | `{{< var modelo1.diag.white.estadistico >}}` |
| `modelo1.diag.white.p` | < 0,001 | p; `003-modelo-i` | `{{< var modelo1.diag.white.p >}}` |
| `modelo1.diag.white.veredicto` | falla | veredicto; `003-modelo-i` | `{{< var modelo1.diag.white.veredicto >}}` |
| `modelo1.diag.jb.estadistico` | 461,908 | estadistico; `003-modelo-i` | `{{< var modelo1.diag.jb.estadistico >}}` |
| `modelo1.diag.jb.p` | < 0,001 | p; `003-modelo-i` | `{{< var modelo1.diag.jb.p >}}` |
| `modelo1.diag.jb.veredicto` | falla | veredicto; `003-modelo-i` | `{{< var modelo1.diag.jb.veredicto >}}` |
| `modelo1.diag.reset.estadistico` | 6,021 | estadistico; `003-modelo-i` | `{{< var modelo1.diag.reset.estadistico >}}` |
| `modelo1.diag.reset.p` | 0,003 | p; `003-modelo-i` | `{{< var modelo1.diag.reset.p >}}` |
| `modelo1.diag.reset.veredicto` | falla | veredicto; `003-modelo-i` | `{{< var modelo1.diag.reset.veredicto >}}` |
| `modelo1.diag.chow_2008t3.estadistico` | 24,987 | estadistico; `003-modelo-i` | `{{< var modelo1.diag.chow_2008t3.estadistico >}}` |
| `modelo1.diag.chow_2008t3.p` | < 0,001 | p; `003-modelo-i` | `{{< var modelo1.diag.chow_2008t3.p >}}` |
| `modelo1.diag.chow_2008t3.veredicto` | falla | veredicto; `003-modelo-i` | `{{< var modelo1.diag.chow_2008t3.veredicto >}}` |
| `modelo1.diag.chow_2020t2.estadistico` | 15,155 | estadistico; `003-modelo-i` | `{{< var modelo1.diag.chow_2020t2.estadistico >}}` |
| `modelo1.diag.chow_2020t2.p` | 0,034 | p; `003-modelo-i` | `{{< var modelo1.diag.chow_2020t2.p >}}` |
| `modelo1.diag.chow_2020t2.veredicto` | falla | veredicto; `003-modelo-i` | `{{< var modelo1.diag.chow_2020t2.veredicto >}}` |
| `modelo1.diag.cusum.veredicto` | pasa | veredicto; `003-modelo-i` | `{{< var modelo1.diag.cusum.veredicto >}}` |
| `modelo1.diag.vif.y_lag.valor` | 3,174 | valor; `003-modelo-i` | `{{< var modelo1.diag.vif.y_lag.valor >}}` |
| `modelo1.diag.vif.y_lag.veredicto` | sin alerta | veredicto; `003-modelo-i` | `{{< var modelo1.diag.vif.y_lag.veredicto >}}` |
| `modelo1.diag.vif.gdp_growth.valor` | 3,280 | valor; `003-modelo-i` | `{{< var modelo1.diag.vif.gdp_growth.valor >}}` |
| `modelo1.diag.vif.gdp_growth.veredicto` | sin alerta | veredicto; `003-modelo-i` | `{{< var modelo1.diag.vif.gdp_growth.veredicto >}}` |
| `modelo1.diag.vif.d_unemp.valor` | 36,811 | valor; `003-modelo-i` | `{{< var modelo1.diag.vif.d_unemp.valor >}}` |
| `modelo1.diag.vif.d_unemp.veredicto` | alerta | veredicto; `003-modelo-i` | `{{< var modelo1.diag.vif.d_unemp.veredicto >}}` |
| `modelo1.diag.vif.inflation.valor` | 1,329 | valor; `003-modelo-i` | `{{< var modelo1.diag.vif.inflation.valor >}}` |
| `modelo1.diag.vif.inflation.veredicto` | sin alerta | veredicto; `003-modelo-i` | `{{< var modelo1.diag.vif.inflation.veredicto >}}` |
| `modelo1.diag.vif.d_ffr.valor` | 1,343 | valor; `003-modelo-i` | `{{< var modelo1.diag.vif.d_ffr.valor >}}` |
| `modelo1.diag.vif.d_ffr.veredicto` | sin alerta | veredicto; `003-modelo-i` | `{{< var modelo1.diag.vif.d_ffr.veredicto >}}` |
| `modelo1.diag.vif.credit_growth.valor` | 1,604 | valor; `003-modelo-i` | `{{< var modelo1.diag.vif.credit_growth.valor >}}` |
| `modelo1.diag.vif.credit_growth.veredicto` | sin alerta | veredicto; `003-modelo-i` | `{{< var modelo1.diag.vif.credit_growth.veredicto >}}` |
| `modelo1.robustez.gdp_growth` | 3 de 9 | gdp growth; `003-modelo-i` | `{{< var modelo1.robustez.gdp_growth >}}` |
| `modelo1.robustez.d_unemp` | 1 de 9 | d unemp; `003-modelo-i` | `{{< var modelo1.robustez.d_unemp >}}` |
| `modelo1.robustez.inflation` | 8 de 9 | inflation; `003-modelo-i` | `{{< var modelo1.robustez.inflation >}}` |
| `modelo1.robustez.d_ffr` | 1 de 9 | d ffr; `003-modelo-i` | `{{< var modelo1.robustez.d_ffr >}}` |
| `modelo1.robustez.credit_growth` | 7 de 9 | credit growth; `003-modelo-i` | `{{< var modelo1.robustez.credit_growth >}}` |
| `modelo1.variantes_muestra.R1.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R1.estado >}}` |
| `modelo1.variantes_muestra.R1.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R1.motivo >}}` |
| `modelo1.variantes_muestra.R1.inicio` | 2000T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R1.inicio >}}` |
| `modelo1.variantes_muestra.R1.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R1.fin >}}` |
| `modelo1.variantes_muestra.R1.n_obs` | 98 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R1.n_obs >}}` |
| `modelo1.variantes_muestra.R2.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R2.estado >}}` |
| `modelo1.variantes_muestra.R2.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R2.motivo >}}` |
| `modelo1.variantes_muestra.R2.inicio` | 2000T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R2.inicio >}}` |
| `modelo1.variantes_muestra.R2.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R2.fin >}}` |
| `modelo1.variantes_muestra.R2.n_obs` | 106 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R2.n_obs >}}` |
| `modelo1.variantes_muestra.R3_drclacbs.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drclacbs.estado >}}` |
| `modelo1.variantes_muestra.R3_drclacbs.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drclacbs.motivo >}}` |
| `modelo1.variantes_muestra.R3_drclacbs.inicio` | 2000T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drclacbs.inicio >}}` |
| `modelo1.variantes_muestra.R3_drclacbs.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drclacbs.fin >}}` |
| `modelo1.variantes_muestra.R3_drclacbs.n_obs` | 106 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drclacbs.n_obs >}}` |
| `modelo1.variantes_muestra.R3_drblacbs.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drblacbs.estado >}}` |
| `modelo1.variantes_muestra.R3_drblacbs.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drblacbs.motivo >}}` |
| `modelo1.variantes_muestra.R3_drblacbs.inicio` | 2000T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drblacbs.inicio >}}` |
| `modelo1.variantes_muestra.R3_drblacbs.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drblacbs.fin >}}` |
| `modelo1.variantes_muestra.R3_drblacbs.n_obs` | 106 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drblacbs.n_obs >}}` |
| `modelo1.variantes_muestra.R3_drsreacbs.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drsreacbs.estado >}}` |
| `modelo1.variantes_muestra.R3_drsreacbs.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drsreacbs.motivo >}}` |
| `modelo1.variantes_muestra.R3_drsreacbs.inicio` | 2000T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drsreacbs.inicio >}}` |
| `modelo1.variantes_muestra.R3_drsreacbs.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drsreacbs.fin >}}` |
| `modelo1.variantes_muestra.R3_drsreacbs.n_obs` | 106 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R3_drsreacbs.n_obs >}}` |
| `modelo1.variantes_muestra.R4.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R4.estado >}}` |
| `modelo1.variantes_muestra.R4.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R4.motivo >}}` |
| `modelo1.variantes_muestra.R4.inicio` | 2000T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R4.inicio >}}` |
| `modelo1.variantes_muestra.R4.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R4.fin >}}` |
| `modelo1.variantes_muestra.R4.n_obs` | 106 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R4.n_obs >}}` |
| `modelo1.variantes_muestra.R5.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R5.estado >}}` |
| `modelo1.variantes_muestra.R5.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R5.motivo >}}` |
| `modelo1.variantes_muestra.R5.inicio` | 2000T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R5.inicio >}}` |
| `modelo1.variantes_muestra.R5.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R5.fin >}}` |
| `modelo1.variantes_muestra.R5.n_obs` | 106 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R5.n_obs >}}` |
| `modelo1.variantes_muestra.R6.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R6.estado >}}` |
| `modelo1.variantes_muestra.R6.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R6.motivo >}}` |
| `modelo1.variantes_muestra.R6.inicio` | 2001T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R6.inicio >}}` |
| `modelo1.variantes_muestra.R6.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R6.fin >}}` |
| `modelo1.variantes_muestra.R6.n_obs` | 102 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R6.n_obs >}}` |
| `modelo1.variantes_muestra.R7.estado` | estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R7.estado >}}` |
| `modelo1.variantes_muestra.R7.motivo` |  | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R7.motivo >}}` |
| `modelo1.variantes_muestra.R7.inicio` | 2002T1 | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R7.inicio >}}` |
| `modelo1.variantes_muestra.R7.fin` | 2026T2 | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R7.fin >}}` |
| `modelo1.variantes_muestra.R7.n_obs` | 98 | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R7.n_obs >}}` |
| `modelo1.variantes_muestra.R8.estado` | no estimada | estado; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R8.estado >}}` |
| `modelo1.variantes_muestra.R8.motivo` | sin historia anterior a 2000T1 | motivo; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R8.motivo >}}` |
| `modelo1.variantes_muestra.R8.inicio` | — | inicio; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R8.inicio >}}` |
| `modelo1.variantes_muestra.R8.fin` | — | fin; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R8.fin >}}` |
| `modelo1.variantes_muestra.R8.n_obs` | — | n obs; `003-modelo-i` | `{{< var modelo1.variantes_muestra.R8.n_obs >}}` |
| `modelo1.oos.n_trimestres` | 18 | n trimestres; `003-modelo-i` | `{{< var modelo1.oos.n_trimestres >}}` |
| `modelo1.oos.rmse_modelo_un_paso` | 0,033 | rmse modelo un paso; `003-modelo-i` | `{{< var modelo1.oos.rmse_modelo_un_paso >}}` |
| `modelo1.oos.rmse_ingenuo_un_paso` | 0,034 | rmse ingenuo un paso; `003-modelo-i` | `{{< var modelo1.oos.rmse_ingenuo_un_paso >}}` |
| `modelo1.oos.mae_modelo_un_paso` | 0,025 | mae modelo un paso; `003-modelo-i` | `{{< var modelo1.oos.mae_modelo_un_paso >}}` |
| `modelo1.oos.mae_ingenuo_un_paso` | 0,026 | mae ingenuo un paso; `003-modelo-i` | `{{< var modelo1.oos.mae_ingenuo_un_paso >}}` |
| `modelo1.oos.cociente_un_paso` | 0,978 | cociente un paso; `003-modelo-i` | `{{< var modelo1.oos.cociente_un_paso >}}` |
| `modelo1.oos.rmse_modelo_dinamico` | 0,276 | rmse modelo dinamico; `003-modelo-i` | `{{< var modelo1.oos.rmse_modelo_dinamico >}}` |
| `modelo1.oos.rmse_ingenuo_dinamico` | 0,170 | rmse ingenuo dinamico; `003-modelo-i` | `{{< var modelo1.oos.rmse_ingenuo_dinamico >}}` |
| `modelo1.oos.mae_modelo_dinamico` | 0,261 | mae modelo dinamico; `003-modelo-i` | `{{< var modelo1.oos.mae_modelo_dinamico >}}` |
| `modelo1.oos.mae_ingenuo_dinamico` | 0,145 | mae ingenuo dinamico; `003-modelo-i` | `{{< var modelo1.oos.mae_ingenuo_dinamico >}}` |
| `modelo1.oos.cociente_dinamico` | 1,625 | cociente dinamico; `003-modelo-i` | `{{< var modelo1.oos.cociente_dinamico >}}` |
| `modelo1.oos.dm_estadistico` | -0,080 | dm estadistico; `003-modelo-i` | `{{< var modelo1.oos.dm_estadistico >}}` |
| `modelo1.oos.dm_p` | 0,937 | dm p; `003-modelo-i` | `{{< var modelo1.oos.dm_p >}}` |
| `modelo1.oos.veredicto_un_paso` | supera al ingenuo | veredicto un paso; `003-modelo-i` | `{{< var modelo1.oos.veredicto_un_paso >}}` |
| `modelo1.oos.veredicto_dinamico` | no supera al ingenuo | veredicto dinamico; `003-modelo-i` | `{{< var modelo1.oos.veredicto_dinamico >}}` |
| `modelo1.oos.significancia_un_paso` | no significativo | significancia un paso; `003-modelo-i` | `{{< var modelo1.oos.significancia_un_paso >}}` |
| `modelo1.no_i0` | π y CRED(t−4) | no i0; `003-modelo-i` | `{{< var modelo1.no_i0 >}}` |
| `modelo1.limitaciones` | Lista de 14 elementos; consultar la fuente o la tabla correspondiente | limitaciones; `003-modelo-i` | Estructura; no se presume sintaxis de índice para shortcodes |
| `modelo1.desviaciones` | Lista de 8 elementos; consultar la fuente o la tabla correspondiente | desviaciones; `003-modelo-i` | Estructura; no se presume sintaxis de índice para shortcodes |
| `modelo2.estimador` | MCO con errores Newey-West (HAC, kernel de Bartlett) | estimador; `004-modelo-ii` | `{{< var modelo2.estimador >}}` |
| `modelo2.forma_y` | primera diferencia | forma y; `004-modelo-ii` | `{{< var modelo2.forma_y >}}` |
| `modelo2.k_elegido` | 1 | k elegido; `004-modelo-ii` | `{{< var modelo2.k_elegido >}}` |
| `modelo2.criterio` | BIC | criterio; `004-modelo-ii` | `{{< var modelo2.criterio >}}` |
| `modelo2.k_bic` | 1 | k bic; `004-modelo-ii` | `{{< var modelo2.k_bic >}}` |
| `modelo2.k_aic` | 1 | k aic; `004-modelo-ii` | `{{< var modelo2.k_aic >}}` |
| `modelo2.muestra_inicio` | 2000T2 | muestra inicio; `004-modelo-ii` | `{{< var modelo2.muestra_inicio >}}` |
| `modelo2.muestra_fin` | 2026T2 | muestra fin; `004-modelo-ii` | `{{< var modelo2.muestra_fin >}}` |
| `modelo2.n_obs` | 105 | n obs; `004-modelo-ii` | `{{< var modelo2.n_obs >}}` |
| `modelo2.n_parametros` | 12 | n parametros; `004-modelo-ii` | `{{< var modelo2.n_parametros >}}` |
| `modelo2.rezagos_hac` | 4 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.rezagos_hac >}}` |
| `modelo2.dummies_covid` | 2020T2, 2020T3, 2020T4 y 2021T1 | dummies covid; `004-modelo-ii` | `{{< var modelo2.dummies_covid >}}` |
| `modelo2.truncamiento_espectral` | no | truncamiento espectral; `004-modelo-ii` | `{{< var modelo2.truncamiento_espectral >}}` |
| `modelo2.r2` | 0,844 | r2; `004-modelo-ii` | `{{< var modelo2.r2 >}}` |
| `modelo2.r2_ajustado` | 0,826 | r2 ajustado; `004-modelo-ii` | `{{< var modelo2.r2_ajustado >}}` |
| `modelo2.ee_regresion` | 0,094 | ee regresion; `004-modelo-ii` | `{{< var modelo2.ee_regresion >}}` |
| `modelo2.seleccion.k1.n_parametros` | 12 | n parametros; `004-modelo-ii` | `{{< var modelo2.seleccion.k1.n_parametros >}}` |
| `modelo2.seleccion.k1.aic` | -188,310 | aic; `004-modelo-ii` | `{{< var modelo2.seleccion.k1.aic >}}` |
| `modelo2.seleccion.k1.bic` | -156,463 | bic; `004-modelo-ii` | `{{< var modelo2.seleccion.k1.bic >}}` |
| `modelo2.seleccion.k2.n_parametros` | 13 | n parametros; `004-modelo-ii` | `{{< var modelo2.seleccion.k2.n_parametros >}}` |
| `modelo2.seleccion.k2.aic` | -187,578 | aic; `004-modelo-ii` | `{{< var modelo2.seleccion.k2.aic >}}` |
| `modelo2.seleccion.k2.bic` | -153,076 | bic; `004-modelo-ii` | `{{< var modelo2.seleccion.k2.bic >}}` |
| `modelo2.seleccion.k3.n_parametros` | 14 | n parametros; `004-modelo-ii` | `{{< var modelo2.seleccion.k3.n_parametros >}}` |
| `modelo2.seleccion.k3.aic` | -188,227 | aic; `004-modelo-ii` | `{{< var modelo2.seleccion.k3.aic >}}` |
| `modelo2.seleccion.k3.bic` | -151,071 | bic; `004-modelo-ii` | `{{< var modelo2.seleccion.k3.bic >}}` |
| `modelo2.seleccion.k4.n_parametros` | 15 | n parametros; `004-modelo-ii` | `{{< var modelo2.seleccion.k4.n_parametros >}}` |
| `modelo2.seleccion.k4.aic` | -187,238 | aic; `004-modelo-ii` | `{{< var modelo2.seleccion.k4.aic >}}` |
| `modelo2.seleccion.k4.bic` | -147,428 | bic; `004-modelo-ii` | `{{< var modelo2.seleccion.k4.bic >}}` |
| `modelo2.seleccion.k5.n_parametros` | 16 | n parametros; `004-modelo-ii` | `{{< var modelo2.seleccion.k5.n_parametros >}}` |
| `modelo2.seleccion.k5.aic` | -186,520 | aic; `004-modelo-ii` | `{{< var modelo2.seleccion.k5.aic >}}` |
| `modelo2.seleccion.k5.bic` | -144,056 | bic; `004-modelo-ii` | `{{< var modelo2.seleccion.k5.bic >}}` |
| `modelo2.seleccion.k6.n_parametros` | 17 | n parametros; `004-modelo-ii` | `{{< var modelo2.seleccion.k6.n_parametros >}}` |
| `modelo2.seleccion.k6.aic` | -184,607 | aic; `004-modelo-ii` | `{{< var modelo2.seleccion.k6.aic >}}` |
| `modelo2.seleccion.k6.bic` | -139,490 | bic; `004-modelo-ii` | `{{< var modelo2.seleccion.k6.bic >}}` |
| `modelo2.seleccion.k7.n_parametros` | 18 | n parametros; `004-modelo-ii` | `{{< var modelo2.seleccion.k7.n_parametros >}}` |
| `modelo2.seleccion.k7.aic` | -183,454 | aic; `004-modelo-ii` | `{{< var modelo2.seleccion.k7.aic >}}` |
| `modelo2.seleccion.k7.bic` | -135,683 | bic; `004-modelo-ii` | `{{< var modelo2.seleccion.k7.bic >}}` |
| `modelo2.seleccion.k8.n_parametros` | 19 | n parametros; `004-modelo-ii` | `{{< var modelo2.seleccion.k8.n_parametros >}}` |
| `modelo2.seleccion.k8.aic` | -181,609 | aic; `004-modelo-ii` | `{{< var modelo2.seleccion.k8.aic >}}` |
| `modelo2.seleccion.k8.bic` | -131,184 | bic; `004-modelo-ii` | `{{< var modelo2.seleccion.k8.bic >}}` |
| `modelo2.coef.const.coef` | -0,100 | coef; `004-modelo-ii` | `{{< var modelo2.coef.const.coef >}}` |
| `modelo2.coef.const.ee` | 0,024 | ee; `004-modelo-ii` | `{{< var modelo2.coef.const.ee >}}` |
| `modelo2.coef.const.p` | < 0,001 | p; `004-modelo-ii` | `{{< var modelo2.coef.const.p >}}` |
| `modelo2.coef.const.ic_inf` | -0,146 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.const.ic_inf >}}` |
| `modelo2.coef.const.ic_sup` | -0,054 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.const.ic_sup >}}` |
| `modelo2.coef.y_lag.coef` | 0,699 | coef; `004-modelo-ii` | `{{< var modelo2.coef.y_lag.coef >}}` |
| `modelo2.coef.y_lag.ee` | 0,084 | ee; `004-modelo-ii` | `{{< var modelo2.coef.y_lag.ee >}}` |
| `modelo2.coef.y_lag.p` | < 0,001 | p; `004-modelo-ii` | `{{< var modelo2.coef.y_lag.p >}}` |
| `modelo2.coef.y_lag.ic_inf` | 0,535 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.y_lag.ic_inf >}}` |
| `modelo2.coef.y_lag.ic_sup` | 0,864 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.y_lag.ic_sup >}}` |
| `modelo2.coef.d_ffr_l0.coef` | -0,084 | coef; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l0.coef >}}` |
| `modelo2.coef.d_ffr_l0.ee` | 0,064 | ee; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l0.ee >}}` |
| `modelo2.coef.d_ffr_l0.p` | 0,190 | p; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l0.p >}}` |
| `modelo2.coef.d_ffr_l0.ic_inf` | -0,210 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l0.ic_inf >}}` |
| `modelo2.coef.d_ffr_l0.ic_sup` | 0,042 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l0.ic_sup >}}` |
| `modelo2.coef.d_ffr_l1.coef` | 0,036 | coef; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l1.coef >}}` |
| `modelo2.coef.d_ffr_l1.ee` | 0,039 | ee; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l1.ee >}}` |
| `modelo2.coef.d_ffr_l1.p` | 0,355 | p; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l1.p >}}` |
| `modelo2.coef.d_ffr_l1.ic_inf` | -0,040 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l1.ic_inf >}}` |
| `modelo2.coef.d_ffr_l1.ic_sup` | 0,111 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.d_ffr_l1.ic_sup >}}` |
| `modelo2.coef.gdp_l1.coef` | 0,001 | coef; `004-modelo-ii` | `{{< var modelo2.coef.gdp_l1.coef >}}` |
| `modelo2.coef.gdp_l1.ee` | 0,005 | ee; `004-modelo-ii` | `{{< var modelo2.coef.gdp_l1.ee >}}` |
| `modelo2.coef.gdp_l1.p` | 0,823 | p; `004-modelo-ii` | `{{< var modelo2.coef.gdp_l1.p >}}` |
| `modelo2.coef.gdp_l1.ic_inf` | -0,009 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.gdp_l1.ic_inf >}}` |
| `modelo2.coef.gdp_l1.ic_sup` | 0,011 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.gdp_l1.ic_sup >}}` |
| `modelo2.coef.d_unemp_l1.coef` | 0,110 | coef; `004-modelo-ii` | `{{< var modelo2.coef.d_unemp_l1.coef >}}` |
| `modelo2.coef.d_unemp_l1.ee` | 0,053 | ee; `004-modelo-ii` | `{{< var modelo2.coef.d_unemp_l1.ee >}}` |
| `modelo2.coef.d_unemp_l1.p` | 0,039 | p; `004-modelo-ii` | `{{< var modelo2.coef.d_unemp_l1.p >}}` |
| `modelo2.coef.d_unemp_l1.ic_inf` | 0,005 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.d_unemp_l1.ic_inf >}}` |
| `modelo2.coef.d_unemp_l1.ic_sup` | 0,215 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.d_unemp_l1.ic_sup >}}` |
| `modelo2.coef.inflation_l1.coef` | 0,024 | coef; `004-modelo-ii` | `{{< var modelo2.coef.inflation_l1.coef >}}` |
| `modelo2.coef.inflation_l1.ee` | 0,010 | ee; `004-modelo-ii` | `{{< var modelo2.coef.inflation_l1.ee >}}` |
| `modelo2.coef.inflation_l1.p` | 0,015 | p; `004-modelo-ii` | `{{< var modelo2.coef.inflation_l1.p >}}` |
| `modelo2.coef.inflation_l1.ic_inf` | 0,005 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.inflation_l1.ic_inf >}}` |
| `modelo2.coef.inflation_l1.ic_sup` | 0,042 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.inflation_l1.ic_sup >}}` |
| `modelo2.coef.credit_l4.coef` | 0,007 | coef; `004-modelo-ii` | `{{< var modelo2.coef.credit_l4.coef >}}` |
| `modelo2.coef.credit_l4.ee` | 0,003 | ee; `004-modelo-ii` | `{{< var modelo2.coef.credit_l4.ee >}}` |
| `modelo2.coef.credit_l4.p` | 0,009 | p; `004-modelo-ii` | `{{< var modelo2.coef.credit_l4.p >}}` |
| `modelo2.coef.credit_l4.ic_inf` | 0,002 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.credit_l4.ic_inf >}}` |
| `modelo2.coef.credit_l4.ic_sup` | 0,012 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.credit_l4.ic_sup >}}` |
| `modelo2.coef.covid_2020q2.coef` | -0,114 | coef; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q2.coef >}}` |
| `modelo2.coef.covid_2020q2.ee` | 0,078 | ee; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q2.ee >}}` |
| `modelo2.coef.covid_2020q2.p` | 0,147 | p; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q2.p >}}` |
| `modelo2.coef.covid_2020q2.ic_inf` | -0,267 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q2.ic_inf >}}` |
| `modelo2.coef.covid_2020q2.ic_sup` | 0,040 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q2.ic_sup >}}` |
| `modelo2.coef.covid_2020q3.coef` | -0,876 | coef; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q3.coef >}}` |
| `modelo2.coef.covid_2020q3.ee` | 0,470 | ee; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q3.ee >}}` |
| `modelo2.coef.covid_2020q3.p` | 0,062 | p; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q3.p >}}` |
| `modelo2.coef.covid_2020q3.ic_inf` | -1,797 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q3.ic_inf >}}` |
| `modelo2.coef.covid_2020q3.ic_sup` | 0,045 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q3.ic_sup >}}` |
| `modelo2.coef.covid_2020q4.coef` | 0,455 | coef; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q4.coef >}}` |
| `modelo2.coef.covid_2020q4.ee` | 0,228 | ee; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q4.ee >}}` |
| `modelo2.coef.covid_2020q4.p` | 0,046 | p; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q4.p >}}` |
| `modelo2.coef.covid_2020q4.ic_inf` | 0,008 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q4.ic_inf >}}` |
| `modelo2.coef.covid_2020q4.ic_sup` | 0,901 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.covid_2020q4.ic_sup >}}` |
| `modelo2.coef.covid_2021q1.coef` | 0,156 | coef; `004-modelo-ii` | `{{< var modelo2.coef.covid_2021q1.coef >}}` |
| `modelo2.coef.covid_2021q1.ee` | 0,110 | ee; `004-modelo-ii` | `{{< var modelo2.coef.covid_2021q1.ee >}}` |
| `modelo2.coef.covid_2021q1.p` | 0,156 | p; `004-modelo-ii` | `{{< var modelo2.coef.covid_2021q1.p >}}` |
| `modelo2.coef.covid_2021q1.ic_inf` | -0,059 | ic inf; `004-modelo-ii` | `{{< var modelo2.coef.covid_2021q1.ic_inf >}}` |
| `modelo2.coef.covid_2021q1.ic_sup` | 0,371 | ic sup; `004-modelo-ii` | `{{< var modelo2.coef.covid_2021q1.ic_sup >}}` |
| `modelo2.efectos.s.est` | -0,048 | est; `004-modelo-ii` | `{{< var modelo2.efectos.s.est >}}` |
| `modelo2.efectos.s.ee` | 0,038 | ee; `004-modelo-ii` | `{{< var modelo2.efectos.s.ee >}}` |
| `modelo2.efectos.s.chi2` | 1,641 | chi2; `004-modelo-ii` | `{{< var modelo2.efectos.s.chi2 >}}` |
| `modelo2.efectos.s.p` | 0,200 | p; `004-modelo-ii` | `{{< var modelo2.efectos.s.p >}}` |
| `modelo2.efectos.s.ic_inf` | -0,122 | ic inf; `004-modelo-ii` | `{{< var modelo2.efectos.s.ic_inf >}}` |
| `modelo2.efectos.s.ic_sup` | 0,026 | ic sup; `004-modelo-ii` | `{{< var modelo2.efectos.s.ic_sup >}}` |
| `modelo2.efectos.s_rez.est` | 0,036 | est; `004-modelo-ii` | `{{< var modelo2.efectos.s_rez.est >}}` |
| `modelo2.efectos.s_rez.ee` | 0,039 | ee; `004-modelo-ii` | `{{< var modelo2.efectos.s_rez.ee >}}` |
| `modelo2.efectos.s_rez.chi2` | 0,857 | chi2; `004-modelo-ii` | `{{< var modelo2.efectos.s_rez.chi2 >}}` |
| `modelo2.efectos.s_rez.p` | 0,355 | p; `004-modelo-ii` | `{{< var modelo2.efectos.s_rez.p >}}` |
| `modelo2.efectos.s_rez.ic_inf` | -0,040 | ic inf; `004-modelo-ii` | `{{< var modelo2.efectos.s_rez.ic_inf >}}` |
| `modelo2.efectos.s_rez.ic_sup` | 0,111 | ic sup; `004-modelo-ii` | `{{< var modelo2.efectos.s_rez.ic_sup >}}` |
| `modelo2.efectos.h1.signo` | no | signo; `004-modelo-ii` | `{{< var modelo2.efectos.h1.signo >}}` |
| `modelo2.efectos.h1.respaldada` | no | respaldada; `004-modelo-ii` | `{{< var modelo2.efectos.h1.respaldada >}}` |
| `modelo2.trayectoria.psi.h0` | -0,084 | h0; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h0 >}}` |
| `modelo2.trayectoria.psi.h1` | -0,023 | h1; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h1 >}}` |
| `modelo2.trayectoria.psi.h2` | -0,016 | h2; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h2 >}}` |
| `modelo2.trayectoria.psi.h3` | -0,011 | h3; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h3 >}}` |
| `modelo2.trayectoria.psi.h4` | -0,008 | h4; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h4 >}}` |
| `modelo2.trayectoria.psi.h5` | -0,006 | h5; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h5 >}}` |
| `modelo2.trayectoria.psi.h6` | -0,004 | h6; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h6 >}}` |
| `modelo2.trayectoria.psi.h7` | -0,003 | h7; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h7 >}}` |
| `modelo2.trayectoria.psi.h8` | -0,002 | h8; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h8 >}}` |
| `modelo2.trayectoria.psi.h9` | -0,001 | h9; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h9 >}}` |
| `modelo2.trayectoria.psi.h10` | -0,001 | h10; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h10 >}}` |
| `modelo2.trayectoria.psi.h11` | -0,001 | h11; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h11 >}}` |
| `modelo2.trayectoria.psi.h12` | -0,000 | h12; `004-modelo-ii` | `{{< var modelo2.trayectoria.psi.h12 >}}` |
| `modelo2.trayectoria.r.h0` | -0,084 | h0; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h0 >}}` |
| `modelo2.trayectoria.r.h1` | -0,107 | h1; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h1 >}}` |
| `modelo2.trayectoria.r.h2` | -0,123 | h2; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h2 >}}` |
| `modelo2.trayectoria.r.h3` | -0,134 | h3; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h3 >}}` |
| `modelo2.trayectoria.r.h4` | -0,142 | h4; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h4 >}}` |
| `modelo2.trayectoria.r.h5` | -0,148 | h5; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h5 >}}` |
| `modelo2.trayectoria.r.h6` | -0,152 | h6; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h6 >}}` |
| `modelo2.trayectoria.r.h7` | -0,154 | h7; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h7 >}}` |
| `modelo2.trayectoria.r.h8` | -0,156 | h8; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h8 >}}` |
| `modelo2.trayectoria.r.h9` | -0,157 | h9; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h9 >}}` |
| `modelo2.trayectoria.r.h10` | -0,158 | h10; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h10 >}}` |
| `modelo2.trayectoria.r.h11` | -0,159 | h11; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h11 >}}` |
| `modelo2.trayectoria.r.h12` | -0,159 | h12; `004-modelo-ii` | `{{< var modelo2.trayectoria.r.h12 >}}` |
| `modelo2.trayectoria.h_estrella.h` | 0 | h; `004-modelo-ii` | `{{< var modelo2.trayectoria.h_estrella.h >}}` |
| `modelo2.trayectoria.h_estrella.signo` | − | signo; `004-modelo-ii` | `{{< var modelo2.trayectoria.h_estrella.signo >}}` |
| `modelo2.trayectoria.h2` | no | h2; `004-modelo-ii` | `{{< var modelo2.trayectoria.h2 >}}` |
| `modelo2.trayectoria.aviso_rho` |  | aviso rho; `004-modelo-ii` | `{{< var modelo2.trayectoria.aviso_rho >}}` |
| `modelo2.granger.chi2` | 0,857 | chi2; `004-modelo-ii` | `{{< var modelo2.granger.chi2 >}}` |
| `modelo2.granger.gl` | 1 | gl; `004-modelo-ii` | `{{< var modelo2.granger.gl >}}` |
| `modelo2.granger.p` | 0,355 | p; `004-modelo-ii` | `{{< var modelo2.granger.p >}}` |
| `modelo2.granger.veredicto` | no rechaza | veredicto; `004-modelo-ii` | `{{< var modelo2.granger.veredicto >}}` |
| `modelo2.lectura.etiqueta` | sin evidencia | etiqueta; `004-modelo-ii` | `{{< var modelo2.lectura.etiqueta >}}` |
| `modelo2.lectura.c1` | no | c1; `004-modelo-ii` | `{{< var modelo2.lectura.c1 >}}` |
| `modelo2.lectura.c2` | no | c2; `004-modelo-ii` | `{{< var modelo2.lectura.c2 >}}` |
| `modelo2.lectura.signo_contrario` | no | signo contrario; `004-modelo-ii` | `{{< var modelo2.lectura.signo_contrario >}}` |
| `modelo2.lp.h0.beta` | -0,084 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h0.beta >}}` |
| `modelo2.lp.h0.ee` | 0,064 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h0.ee >}}` |
| `modelo2.lp.h0.ic90_inf` | -0,189 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h0.ic90_inf >}}` |
| `modelo2.lp.h0.ic90_sup` | 0,021 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h0.ic90_sup >}}` |
| `modelo2.lp.h0.n_obs` | 105 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h0.n_obs >}}` |
| `modelo2.lp.h0.rezagos_hac` | 4 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h0.rezagos_hac >}}` |
| `modelo2.lp.h0.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h0.estado >}}` |
| `modelo2.lp.h0.phi` | 1,000 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h0.phi >}}` |
| `modelo2.lp.h0.phi_ee` | — | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h0.phi_ee >}}` |
| `modelo2.lp.h0.phi_ic90_inf` | — | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h0.phi_ic90_inf >}}` |
| `modelo2.lp.h0.phi_ic90_sup` | — | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h0.phi_ic90_sup >}}` |
| `modelo2.lp.h1.beta` | -0,148 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h1.beta >}}` |
| `modelo2.lp.h1.ee` | 0,092 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h1.ee >}}` |
| `modelo2.lp.h1.ic90_inf` | -0,300 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h1.ic90_inf >}}` |
| `modelo2.lp.h1.ic90_sup` | 0,003 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h1.ic90_sup >}}` |
| `modelo2.lp.h1.n_obs` | 104 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h1.n_obs >}}` |
| `modelo2.lp.h1.rezagos_hac` | 4 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h1.rezagos_hac >}}` |
| `modelo2.lp.h1.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h1.estado >}}` |
| `modelo2.lp.h1.phi` | 1,717 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h1.phi >}}` |
| `modelo2.lp.h1.phi_ee` | 0,186 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h1.phi_ee >}}` |
| `modelo2.lp.h1.phi_ic90_inf` | 1,411 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h1.phi_ic90_inf >}}` |
| `modelo2.lp.h1.phi_ic90_sup` | 2,024 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h1.phi_ic90_sup >}}` |
| `modelo2.lp.h2.beta` | -0,204 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h2.beta >}}` |
| `modelo2.lp.h2.ee` | 0,125 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h2.ee >}}` |
| `modelo2.lp.h2.ic90_inf` | -0,410 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h2.ic90_inf >}}` |
| `modelo2.lp.h2.ic90_sup` | 0,001 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h2.ic90_sup >}}` |
| `modelo2.lp.h2.n_obs` | 103 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h2.n_obs >}}` |
| `modelo2.lp.h2.rezagos_hac` | 4 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h2.rezagos_hac >}}` |
| `modelo2.lp.h2.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h2.estado >}}` |
| `modelo2.lp.h2.phi` | 2,265 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h2.phi >}}` |
| `modelo2.lp.h2.phi_ee` | 0,360 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h2.phi_ee >}}` |
| `modelo2.lp.h2.phi_ic90_inf` | 1,674 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h2.phi_ic90_inf >}}` |
| `modelo2.lp.h2.phi_ic90_sup` | 2,857 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h2.phi_ic90_sup >}}` |
| `modelo2.lp.h3.beta` | -0,300 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h3.beta >}}` |
| `modelo2.lp.h3.ee` | 0,186 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h3.ee >}}` |
| `modelo2.lp.h3.ic90_inf` | -0,605 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h3.ic90_inf >}}` |
| `modelo2.lp.h3.ic90_sup` | 0,005 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h3.ic90_sup >}}` |
| `modelo2.lp.h3.n_obs` | 102 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h3.n_obs >}}` |
| `modelo2.lp.h3.rezagos_hac` | 4 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h3.rezagos_hac >}}` |
| `modelo2.lp.h3.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h3.estado >}}` |
| `modelo2.lp.h3.phi` | 2,763 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h3.phi >}}` |
| `modelo2.lp.h3.phi_ee` | 0,512 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h3.phi_ee >}}` |
| `modelo2.lp.h3.phi_ic90_inf` | 1,921 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h3.phi_ic90_inf >}}` |
| `modelo2.lp.h3.phi_ic90_sup` | 3,605 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h3.phi_ic90_sup >}}` |
| `modelo2.lp.h4.beta` | -0,414 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h4.beta >}}` |
| `modelo2.lp.h4.ee` | 0,268 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h4.ee >}}` |
| `modelo2.lp.h4.ic90_inf` | -0,856 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h4.ic90_inf >}}` |
| `modelo2.lp.h4.ic90_sup` | 0,027 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h4.ic90_sup >}}` |
| `modelo2.lp.h4.n_obs` | 101 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h4.n_obs >}}` |
| `modelo2.lp.h4.rezagos_hac` | 5 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h4.rezagos_hac >}}` |
| `modelo2.lp.h4.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h4.estado >}}` |
| `modelo2.lp.h4.phi` | 3,049 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h4.phi >}}` |
| `modelo2.lp.h4.phi_ee` | 0,581 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h4.phi_ee >}}` |
| `modelo2.lp.h4.phi_ic90_inf` | 2,094 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h4.phi_ic90_inf >}}` |
| `modelo2.lp.h4.phi_ic90_sup` | 4,005 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h4.phi_ic90_sup >}}` |
| `modelo2.lp.h5.beta` | -0,516 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h5.beta >}}` |
| `modelo2.lp.h5.ee` | 0,346 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h5.ee >}}` |
| `modelo2.lp.h5.ic90_inf` | -1,085 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h5.ic90_inf >}}` |
| `modelo2.lp.h5.ic90_sup` | 0,053 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h5.ic90_sup >}}` |
| `modelo2.lp.h5.n_obs` | 100 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h5.n_obs >}}` |
| `modelo2.lp.h5.rezagos_hac` | 6 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h5.rezagos_hac >}}` |
| `modelo2.lp.h5.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h5.estado >}}` |
| `modelo2.lp.h5.phi` | 3,233 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h5.phi >}}` |
| `modelo2.lp.h5.phi_ee` | 0,660 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h5.phi_ee >}}` |
| `modelo2.lp.h5.phi_ic90_inf` | 2,148 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h5.phi_ic90_inf >}}` |
| `modelo2.lp.h5.phi_ic90_sup` | 4,319 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h5.phi_ic90_sup >}}` |
| `modelo2.lp.h6.beta` | -0,558 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h6.beta >}}` |
| `modelo2.lp.h6.ee` | 0,406 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h6.ee >}}` |
| `modelo2.lp.h6.ic90_inf` | -1,226 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h6.ic90_inf >}}` |
| `modelo2.lp.h6.ic90_sup` | 0,109 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h6.ic90_sup >}}` |
| `modelo2.lp.h6.n_obs` | 99 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h6.n_obs >}}` |
| `modelo2.lp.h6.rezagos_hac` | 7 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h6.rezagos_hac >}}` |
| `modelo2.lp.h6.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h6.estado >}}` |
| `modelo2.lp.h6.phi` | 3,224 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h6.phi >}}` |
| `modelo2.lp.h6.phi_ee` | 0,724 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h6.phi_ee >}}` |
| `modelo2.lp.h6.phi_ic90_inf` | 2,032 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h6.phi_ic90_inf >}}` |
| `modelo2.lp.h6.phi_ic90_sup` | 4,415 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h6.phi_ic90_sup >}}` |
| `modelo2.lp.h7.beta` | -0,546 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h7.beta >}}` |
| `modelo2.lp.h7.ee` | 0,486 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h7.ee >}}` |
| `modelo2.lp.h7.ic90_inf` | -1,345 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h7.ic90_inf >}}` |
| `modelo2.lp.h7.ic90_sup` | 0,254 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h7.ic90_sup >}}` |
| `modelo2.lp.h7.n_obs` | 98 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h7.n_obs >}}` |
| `modelo2.lp.h7.rezagos_hac` | 8 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h7.rezagos_hac >}}` |
| `modelo2.lp.h7.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h7.estado >}}` |
| `modelo2.lp.h7.phi` | 3,287 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h7.phi >}}` |
| `modelo2.lp.h7.phi_ee` | 0,825 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h7.phi_ee >}}` |
| `modelo2.lp.h7.phi_ic90_inf` | 1,930 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h7.phi_ic90_inf >}}` |
| `modelo2.lp.h7.phi_ic90_sup` | 4,643 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h7.phi_ic90_sup >}}` |
| `modelo2.lp.h8.beta` | -0,454 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h8.beta >}}` |
| `modelo2.lp.h8.ee` | 0,495 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h8.ee >}}` |
| `modelo2.lp.h8.ic90_inf` | -1,268 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h8.ic90_inf >}}` |
| `modelo2.lp.h8.ic90_sup` | 0,360 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h8.ic90_sup >}}` |
| `modelo2.lp.h8.n_obs` | 97 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h8.n_obs >}}` |
| `modelo2.lp.h8.rezagos_hac` | 9 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h8.rezagos_hac >}}` |
| `modelo2.lp.h8.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h8.estado >}}` |
| `modelo2.lp.h8.phi` | 3,223 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h8.phi >}}` |
| `modelo2.lp.h8.phi_ee` | 0,857 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h8.phi_ee >}}` |
| `modelo2.lp.h8.phi_ic90_inf` | 1,813 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h8.phi_ic90_inf >}}` |
| `modelo2.lp.h8.phi_ic90_sup` | 4,633 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h8.phi_ic90_sup >}}` |
| `modelo2.lp.h9.beta` | -0,344 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h9.beta >}}` |
| `modelo2.lp.h9.ee` | 0,512 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h9.ee >}}` |
| `modelo2.lp.h9.ic90_inf` | -1,186 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h9.ic90_inf >}}` |
| `modelo2.lp.h9.ic90_sup` | 0,499 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h9.ic90_sup >}}` |
| `modelo2.lp.h9.n_obs` | 96 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h9.n_obs >}}` |
| `modelo2.lp.h9.rezagos_hac` | 10 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h9.rezagos_hac >}}` |
| `modelo2.lp.h9.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h9.estado >}}` |
| `modelo2.lp.h9.phi` | 3,061 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h9.phi >}}` |
| `modelo2.lp.h9.phi_ee` | 0,841 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h9.phi_ee >}}` |
| `modelo2.lp.h9.phi_ic90_inf` | 1,678 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h9.phi_ic90_inf >}}` |
| `modelo2.lp.h9.phi_ic90_sup` | 4,444 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h9.phi_ic90_sup >}}` |
| `modelo2.lp.h10.beta` | -0,157 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h10.beta >}}` |
| `modelo2.lp.h10.ee` | 0,483 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h10.ee >}}` |
| `modelo2.lp.h10.ic90_inf` | -0,952 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h10.ic90_inf >}}` |
| `modelo2.lp.h10.ic90_sup` | 0,638 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h10.ic90_sup >}}` |
| `modelo2.lp.h10.n_obs` | 95 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h10.n_obs >}}` |
| `modelo2.lp.h10.rezagos_hac` | 11 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h10.rezagos_hac >}}` |
| `modelo2.lp.h10.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h10.estado >}}` |
| `modelo2.lp.h10.phi` | 2,930 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h10.phi >}}` |
| `modelo2.lp.h10.phi_ee` | 0,814 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h10.phi_ee >}}` |
| `modelo2.lp.h10.phi_ic90_inf` | 1,591 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h10.phi_ic90_inf >}}` |
| `modelo2.lp.h10.phi_ic90_sup` | 4,269 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h10.phi_ic90_sup >}}` |
| `modelo2.lp.h11.beta` | 0,060 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h11.beta >}}` |
| `modelo2.lp.h11.ee` | 0,440 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h11.ee >}}` |
| `modelo2.lp.h11.ic90_inf` | -0,663 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h11.ic90_inf >}}` |
| `modelo2.lp.h11.ic90_sup` | 0,784 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h11.ic90_sup >}}` |
| `modelo2.lp.h11.n_obs` | 94 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h11.n_obs >}}` |
| `modelo2.lp.h11.rezagos_hac` | 12 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h11.rezagos_hac >}}` |
| `modelo2.lp.h11.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h11.estado >}}` |
| `modelo2.lp.h11.phi` | 2,726 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h11.phi >}}` |
| `modelo2.lp.h11.phi_ee` | 0,769 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h11.phi_ee >}}` |
| `modelo2.lp.h11.phi_ic90_inf` | 1,460 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h11.phi_ic90_inf >}}` |
| `modelo2.lp.h11.phi_ic90_sup` | 3,991 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h11.phi_ic90_sup >}}` |
| `modelo2.lp.h12.beta` | 0,285 | beta; `004-modelo-ii` | `{{< var modelo2.lp.h12.beta >}}` |
| `modelo2.lp.h12.ee` | 0,414 | ee; `004-modelo-ii` | `{{< var modelo2.lp.h12.ee >}}` |
| `modelo2.lp.h12.ic90_inf` | -0,397 | ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h12.ic90_inf >}}` |
| `modelo2.lp.h12.ic90_sup` | 0,966 | ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h12.ic90_sup >}}` |
| `modelo2.lp.h12.n_obs` | 93 | n obs; `004-modelo-ii` | `{{< var modelo2.lp.h12.n_obs >}}` |
| `modelo2.lp.h12.rezagos_hac` | 13 | rezagos hac; `004-modelo-ii` | `{{< var modelo2.lp.h12.rezagos_hac >}}` |
| `modelo2.lp.h12.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.lp.h12.estado >}}` |
| `modelo2.lp.h12.phi` | 2,476 | phi; `004-modelo-ii` | `{{< var modelo2.lp.h12.phi >}}` |
| `modelo2.lp.h12.phi_ee` | 0,732 | phi ee; `004-modelo-ii` | `{{< var modelo2.lp.h12.phi_ee >}}` |
| `modelo2.lp.h12.phi_ic90_inf` | 1,272 | phi ic90 inf; `004-modelo-ii` | `{{< var modelo2.lp.h12.phi_ic90_inf >}}` |
| `modelo2.lp.h12.phi_ic90_sup` | 3,680 | phi ic90 sup; `004-modelo-ii` | `{{< var modelo2.lp.h12.phi_ic90_sup >}}` |
| `modelo2.lp_resumen.k_de_n` | 10 de 12 | k de n; `004-modelo-ii` | `{{< var modelo2.lp_resumen.k_de_n >}}` |
| `modelo2.lp_resumen.horizonte_deteccion` | ninguno | horizonte deteccion; `004-modelo-ii` | `{{< var modelo2.lp_resumen.horizonte_deteccion >}}` |
| `modelo2.diag.bg.estadistico` | 3,409 | estadistico; `004-modelo-ii` | `{{< var modelo2.diag.bg.estadistico >}}` |
| `modelo2.diag.bg.p` | 0,492 | p; `004-modelo-ii` | `{{< var modelo2.diag.bg.p >}}` |
| `modelo2.diag.bg.veredicto` | pasa | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.bg.veredicto >}}` |
| `modelo2.diag.bp.estadistico` | 33,784 | estadistico; `004-modelo-ii` | `{{< var modelo2.diag.bp.estadistico >}}` |
| `modelo2.diag.bp.p` | < 0,001 | p; `004-modelo-ii` | `{{< var modelo2.diag.bp.p >}}` |
| `modelo2.diag.bp.veredicto` | falla | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.bp.veredicto >}}` |
| `modelo2.diag.white.estadistico` | 90,710 | estadistico; `004-modelo-ii` | `{{< var modelo2.diag.white.estadistico >}}` |
| `modelo2.diag.white.p` | < 0,001 | p; `004-modelo-ii` | `{{< var modelo2.diag.white.p >}}` |
| `modelo2.diag.white.veredicto` | falla | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.white.veredicto >}}` |
| `modelo2.diag.jb.estadistico` | 209,207 | estadistico; `004-modelo-ii` | `{{< var modelo2.diag.jb.estadistico >}}` |
| `modelo2.diag.jb.p` | < 0,001 | p; `004-modelo-ii` | `{{< var modelo2.diag.jb.p >}}` |
| `modelo2.diag.jb.veredicto` | falla | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.jb.veredicto >}}` |
| `modelo2.diag.reset.estadistico` | 10,448 | estadistico; `004-modelo-ii` | `{{< var modelo2.diag.reset.estadistico >}}` |
| `modelo2.diag.reset.p` | < 0,001 | p; `004-modelo-ii` | `{{< var modelo2.diag.reset.p >}}` |
| `modelo2.diag.reset.veredicto` | falla | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.reset.veredicto >}}` |
| `modelo2.diag.chow_2008t3.estadistico` | 11,644 | estadistico; `004-modelo-ii` | `{{< var modelo2.diag.chow_2008t3.estadistico >}}` |
| `modelo2.diag.chow_2008t3.p` | 0,168 | p; `004-modelo-ii` | `{{< var modelo2.diag.chow_2008t3.p >}}` |
| `modelo2.diag.chow_2008t3.veredicto` | pasa | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.chow_2008t3.veredicto >}}` |
| `modelo2.diag.chow_2020t2.estadistico` | 28,123 | estadistico; `004-modelo-ii` | `{{< var modelo2.diag.chow_2020t2.estadistico >}}` |
| `modelo2.diag.chow_2020t2.p` | < 0,001 | p; `004-modelo-ii` | `{{< var modelo2.diag.chow_2020t2.p >}}` |
| `modelo2.diag.chow_2020t2.veredicto` | falla | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.chow_2020t2.veredicto >}}` |
| `modelo2.diag.cusum.veredicto` | pasa | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.cusum.veredicto >}}` |
| `modelo2.diag.vif.y_lag.valor` | 3,122 | valor; `004-modelo-ii` | `{{< var modelo2.diag.vif.y_lag.valor >}}` |
| `modelo2.diag.vif.y_lag.veredicto` | sin alerta | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.vif.y_lag.veredicto >}}` |
| `modelo2.diag.vif.d_ffr_l0.valor` | 2,521 | valor; `004-modelo-ii` | `{{< var modelo2.diag.vif.d_ffr_l0.valor >}}` |
| `modelo2.diag.vif.d_ffr_l0.veredicto` | sin alerta | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.vif.d_ffr_l0.veredicto >}}` |
| `modelo2.diag.vif.d_ffr_l1.valor` | 2,664 | valor; `004-modelo-ii` | `{{< var modelo2.diag.vif.d_ffr_l1.valor >}}` |
| `modelo2.diag.vif.d_ffr_l1.veredicto` | sin alerta | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.vif.d_ffr_l1.veredicto >}}` |
| `modelo2.diag.vif.gdp_l1.valor` | 3,008 | valor; `004-modelo-ii` | `{{< var modelo2.diag.vif.gdp_l1.valor >}}` |
| `modelo2.diag.vif.gdp_l1.veredicto` | sin alerta | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.vif.gdp_l1.veredicto >}}` |
| `modelo2.diag.vif.d_unemp_l1.valor` | 33,154 | valor; `004-modelo-ii` | `{{< var modelo2.diag.vif.d_unemp_l1.valor >}}` |
| `modelo2.diag.vif.d_unemp_l1.veredicto` | alerta | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.vif.d_unemp_l1.veredicto >}}` |
| `modelo2.diag.vif.inflation_l1.valor` | 1,414 | valor; `004-modelo-ii` | `{{< var modelo2.diag.vif.inflation_l1.valor >}}` |
| `modelo2.diag.vif.inflation_l1.veredicto` | sin alerta | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.vif.inflation_l1.veredicto >}}` |
| `modelo2.diag.vif.credit_l4.valor` | 1,548 | valor; `004-modelo-ii` | `{{< var modelo2.diag.vif.credit_l4.valor >}}` |
| `modelo2.diag.vif.credit_l4.veredicto` | sin alerta | veredicto; `004-modelo-ii` | `{{< var modelo2.diag.vif.credit_l4.veredicto >}}` |
| `modelo2.robustez.r1.estado` | no aplica | estado; `004-modelo-ii` | `{{< var modelo2.robustez.r1.estado >}}` |
| `modelo2.robustez.r1.motivo` | AIC y BIC eligen el mismo K | motivo; `004-modelo-ii` | `{{< var modelo2.robustez.r1.motivo >}}` |
| `modelo2.robustez.r1.k` | — | k; `004-modelo-ii` | `{{< var modelo2.robustez.r1.k >}}` |
| `modelo2.robustez.r1.muestra_inicio` | — | muestra inicio; `004-modelo-ii` | `{{< var modelo2.robustez.r1.muestra_inicio >}}` |
| `modelo2.robustez.r1.muestra_fin` | — | muestra fin; `004-modelo-ii` | `{{< var modelo2.robustez.r1.muestra_fin >}}` |
| `modelo2.robustez.r1.n_obs` | — | n obs; `004-modelo-ii` | `{{< var modelo2.robustez.r1.n_obs >}}` |
| `modelo2.robustez.r1.s` | — | s; `004-modelo-ii` | `{{< var modelo2.robustez.r1.s >}}` |
| `modelo2.robustez.r1.s_rez` | — | s rez; `004-modelo-ii` | `{{< var modelo2.robustez.r1.s_rez >}}` |
| `modelo2.robustez.r1.p_s_rez` | — | p s rez; `004-modelo-ii` | `{{< var modelo2.robustez.r1.p_s_rez >}}` |
| `modelo2.robustez.r1.h_estrella` | — | h estrella; `004-modelo-ii` | `{{< var modelo2.robustez.r1.h_estrella >}}` |
| `modelo2.robustez.r1.h1` | — | h1; `004-modelo-ii` | `{{< var modelo2.robustez.r1.h1 >}}` |
| `modelo2.robustez.r2.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.robustez.r2.estado >}}` |
| `modelo2.robustez.r2.motivo` |  | motivo; `004-modelo-ii` | `{{< var modelo2.robustez.r2.motivo >}}` |
| `modelo2.robustez.r2.k` | 1 | k; `004-modelo-ii` | `{{< var modelo2.robustez.r2.k >}}` |
| `modelo2.robustez.r2.muestra_inicio` | 2000T2 | muestra inicio; `004-modelo-ii` | `{{< var modelo2.robustez.r2.muestra_inicio >}}` |
| `modelo2.robustez.r2.muestra_fin` | 2026T2 | muestra fin; `004-modelo-ii` | `{{< var modelo2.robustez.r2.muestra_fin >}}` |
| `modelo2.robustez.r2.n_obs` | 97 | n obs; `004-modelo-ii` | `{{< var modelo2.robustez.r2.n_obs >}}` |
| `modelo2.robustez.r2.s` | -0,043 | s; `004-modelo-ii` | `{{< var modelo2.robustez.r2.s >}}` |
| `modelo2.robustez.r2.s_rez` | 0,040 | s rez; `004-modelo-ii` | `{{< var modelo2.robustez.r2.s_rez >}}` |
| `modelo2.robustez.r2.p_s_rez` | 0,303 | p s rez; `004-modelo-ii` | `{{< var modelo2.robustez.r2.p_s_rez >}}` |
| `modelo2.robustez.r2.h_estrella` | 0 | h estrella; `004-modelo-ii` | `{{< var modelo2.robustez.r2.h_estrella >}}` |
| `modelo2.robustez.r2.h1` | no | h1; `004-modelo-ii` | `{{< var modelo2.robustez.r2.h1 >}}` |
| `modelo2.robustez.r3.estado` | estimada | estado; `004-modelo-ii` | `{{< var modelo2.robustez.r3.estado >}}` |
| `modelo2.robustez.r3.motivo` |  | motivo; `004-modelo-ii` | `{{< var modelo2.robustez.r3.motivo >}}` |
| `modelo2.robustez.r3.k` | 1 | k; `004-modelo-ii` | `{{< var modelo2.robustez.r3.k >}}` |
| `modelo2.robustez.r3.muestra_inicio` | 2000T2 | muestra inicio; `004-modelo-ii` | `{{< var modelo2.robustez.r3.muestra_inicio >}}` |
| `modelo2.robustez.r3.muestra_fin` | 2026T2 | muestra fin; `004-modelo-ii` | `{{< var modelo2.robustez.r3.muestra_fin >}}` |
| `modelo2.robustez.r3.n_obs` | 69 | n obs; `004-modelo-ii` | `{{< var modelo2.robustez.r3.n_obs >}}` |
| `modelo2.robustez.r3.s` | -0,000 | s; `004-modelo-ii` | `{{< var modelo2.robustez.r3.s >}}` |
| `modelo2.robustez.r3.s_rez` | 0,061 | s rez; `004-modelo-ii` | `{{< var modelo2.robustez.r3.s_rez >}}` |
| `modelo2.robustez.r3.p_s_rez` | 0,293 | p s rez; `004-modelo-ii` | `{{< var modelo2.robustez.r3.p_s_rez >}}` |
| `modelo2.robustez.r3.h_estrella` | 0 | h estrella; `004-modelo-ii` | `{{< var modelo2.robustez.r3.h_estrella >}}` |
| `modelo2.robustez.r3.h1` | no | h1; `004-modelo-ii` | `{{< var modelo2.robustez.r3.h1 >}}` |
| `modelo2.robustez_resumen.r1` | no aplica | r1; `004-modelo-ii` | `{{< var modelo2.robustez_resumen.r1 >}}` |
| `modelo2.robustez_resumen.r2` | no | r2; `004-modelo-ii` | `{{< var modelo2.robustez_resumen.r2 >}}` |
| `modelo2.robustez_resumen.r3` | no | r3; `004-modelo-ii` | `{{< var modelo2.robustez_resumen.r3 >}}` |
| `modelo2.robustez_resumen.p_principal` | 0,355 | p principal; `004-modelo-ii` | `{{< var modelo2.robustez_resumen.p_principal >}}` |
| `modelo2.no_i0` | π(t−1) y CRED(t−4) | no i0; `004-modelo-ii` | `{{< var modelo2.no_i0 >}}` |
| `modelo2.limitaciones` | Lista de 16 elementos; consultar la fuente o la tabla correspondiente | limitaciones; `004-modelo-ii` | Estructura; no se presume sintaxis de índice para shortcodes |
| `modelo2.desviaciones` | Lista de 6 elementos; consultar la fuente o la tabla correspondiente | desviaciones; `004-modelo-ii` | Estructura; no se presume sintaxis de índice para shortcodes |
| `estres.horizonte.origen` | 2026T2 | origen; `005-estres` | `{{< var estres.horizonte.origen >}}` |
| `estres.horizonte.inicio` | 2026T3 | inicio; `005-estres` | `{{< var estres.horizonte.inicio >}}` |
| `estres.horizonte.fin` | 2029T3 | fin; `005-estres` | `{{< var estres.horizonte.fin >}}` |
| `estres.horizonte.h` | 13 | h; `005-estres` | `{{< var estres.horizonte.h >}}` |
| `estres.replicas.n` | 10000 | n; `005-estres` | `{{< var estres.replicas.n >}}` |
| `estres.replicas.semilla` | 20261011 | semilla; `005-estres` | `{{< var estres.replicas.semilla >}}` |
| `estres.dif_modelos.severo.delta_final` | 0,600 | delta final; `005-estres` | `{{< var estres.dif_modelos.severo.delta_final >}}` |
| `estres.dif_modelos.severo.delta_pico` | 0,612 | delta pico; `005-estres` | `{{< var estres.dif_modelos.severo.delta_pico >}}` |
| `estres.dif_modelos.propio.delta_final` | 0,600 | delta final; `005-estres` | `{{< var estres.dif_modelos.propio.delta_final >}}` |
| `estres.dif_modelos.propio.delta_pico` | 0,612 | delta pico; `005-estres` | `{{< var estres.dif_modelos.propio.delta_pico >}}` |
| `estres.sens_tasa.modelo1.severo.c_final` | 0,341 | c final; `005-estres` | `{{< var estres.sens_tasa.modelo1.severo.c_final >}}` |
| `estres.sens_tasa.modelo1.severo.c_final_p05` | -0,206 | c final p05; `005-estres` | `{{< var estres.sens_tasa.modelo1.severo.c_final_p05 >}}` |
| `estres.sens_tasa.modelo1.severo.c_final_p95` | 0,746 | c final p95; `005-estres` | `{{< var estres.sens_tasa.modelo1.severo.c_final_p95 >}}` |
| `estres.sens_tasa.modelo1.severo.c_pico` | 0,346 | c pico; `005-estres` | `{{< var estres.sens_tasa.modelo1.severo.c_pico >}}` |
| `estres.sens_tasa.modelo1.severo.prop_c_pos_final` | 0,864 | prop c pos final; `005-estres` | `{{< var estres.sens_tasa.modelo1.severo.prop_c_pos_final >}}` |
| `estres.sens_tasa.modelo1.severo.prop_c_pos_pico` | 0,864 | prop c pos pico; `005-estres` | `{{< var estres.sens_tasa.modelo1.severo.prop_c_pos_pico >}}` |
| `estres.sens_tasa.modelo1.propio.c_final` | -0,681 | c final; `005-estres` | `{{< var estres.sens_tasa.modelo1.propio.c_final >}}` |
| `estres.sens_tasa.modelo1.propio.c_final_p05` | -1,490 | c final p05; `005-estres` | `{{< var estres.sens_tasa.modelo1.propio.c_final_p05 >}}` |
| `estres.sens_tasa.modelo1.propio.c_final_p95` | 0,405 | c final p95; `005-estres` | `{{< var estres.sens_tasa.modelo1.propio.c_final_p95 >}}` |
| `estres.sens_tasa.modelo1.propio.c_pico` | -0,603 | c pico; `005-estres` | `{{< var estres.sens_tasa.modelo1.propio.c_pico >}}` |
| `estres.sens_tasa.modelo1.propio.prop_c_pos_final` | 0,136 | prop c pos final; `005-estres` | `{{< var estres.sens_tasa.modelo1.propio.prop_c_pos_final >}}` |
| `estres.sens_tasa.modelo1.propio.prop_c_pos_pico` | 0,136 | prop c pos pico; `005-estres` | `{{< var estres.sens_tasa.modelo1.propio.prop_c_pos_pico >}}` |
| `estres.sens_tasa.modelo2.severo.c_final` | 0,464 | c final; `005-estres` | `{{< var estres.sens_tasa.modelo2.severo.c_final >}}` |
| `estres.sens_tasa.modelo2.severo.c_final_p05` | -0,139 | c final p05; `005-estres` | `{{< var estres.sens_tasa.modelo2.severo.c_final_p05 >}}` |
| `estres.sens_tasa.modelo2.severo.c_final_p95` | 1,133 | c final p95; `005-estres` | `{{< var estres.sens_tasa.modelo2.severo.c_final_p95 >}}` |
| `estres.sens_tasa.modelo2.severo.c_pico` | 0,466 | c pico; `005-estres` | `{{< var estres.sens_tasa.modelo2.severo.c_pico >}}` |
| `estres.sens_tasa.modelo2.severo.prop_c_pos_final` | 0,905 | prop c pos final; `005-estres` | `{{< var estres.sens_tasa.modelo2.severo.prop_c_pos_final >}}` |
| `estres.sens_tasa.modelo2.severo.prop_c_pos_pico` | 0,907 | prop c pos pico; `005-estres` | `{{< var estres.sens_tasa.modelo2.severo.prop_c_pos_pico >}}` |
| `estres.sens_tasa.modelo2.propio.c_final` | -0,922 | c final; `005-estres` | `{{< var estres.sens_tasa.modelo2.propio.c_final >}}` |
| `estres.sens_tasa.modelo2.propio.c_final_p05` | -2,204 | c final p05; `005-estres` | `{{< var estres.sens_tasa.modelo2.propio.c_final_p05 >}}` |
| `estres.sens_tasa.modelo2.propio.c_final_p95` | 0,271 | c final p95; `005-estres` | `{{< var estres.sens_tasa.modelo2.propio.c_final_p95 >}}` |
| `estres.sens_tasa.modelo2.propio.c_pico` | -0,815 | c pico; `005-estres` | `{{< var estres.sens_tasa.modelo2.propio.c_pico >}}` |
| `estres.sens_tasa.modelo2.propio.prop_c_pos_final` | 0,094 | prop c pos final; `005-estres` | `{{< var estres.sens_tasa.modelo2.propio.prop_c_pos_final >}}` |
| `estres.sens_tasa.modelo2.propio.prop_c_pos_pico` | 0,088 | prop c pos pico; `005-estres` | `{{< var estres.sens_tasa.modelo2.propio.prop_c_pos_pico >}}` |
| `estres.sens_cal.modelo1.delta_final_2029t1` | 0,340 | delta final 2029t1; `005-estres` | `{{< var estres.sens_cal.modelo1.delta_final_2029t1 >}}` |
| `estres.sens_cal.modelo1.delta_principal_2029t1` | 1,736 | delta principal 2029t1; `005-estres` | `{{< var estres.sens_cal.modelo1.delta_principal_2029t1 >}}` |
| `estres.sens_cal.modelo1.delta_pico` | 0,843 | delta pico; `005-estres` | `{{< var estres.sens_cal.modelo1.delta_pico >}}` |
| `estres.sens_cal.modelo2.delta_final_2029t1` | 0,048 | delta final 2029t1; `005-estres` | `{{< var estres.sens_cal.modelo2.delta_final_2029t1 >}}` |
| `estres.sens_cal.modelo2.delta_principal_2029t1` | 1,118 | delta principal 2029t1; `005-estres` | `{{< var estres.sens_cal.modelo2.delta_principal_2029t1 >}}` |
| `estres.sens_cal.modelo2.delta_pico` | 0,549 | delta pico; `005-estres` | `{{< var estres.sens_cal.modelo2.delta_pico >}}` |
| `estres.sens_cred.modelo1.base.cero.nivel_final` | 0,599 | nivel final; `005-estres` | `{{< var estres.sens_cred.modelo1.base.cero.nivel_final >}}` |
| `estres.sens_cred.modelo1.base.cero.nivel_pico` | 1,579 | nivel pico; `005-estres` | `{{< var estres.sens_cred.modelo1.base.cero.nivel_pico >}}` |
| `estres.sens_cred.modelo1.base.cero.nivel_pico_trimestre` | 2027T2 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_cred.modelo1.base.cero.nivel_pico_trimestre >}}` |
| `estres.sens_cred.modelo1.base.media.nivel_final` | 1,649 | nivel final; `005-estres` | `{{< var estres.sens_cred.modelo1.base.media.nivel_final >}}` |
| `estres.sens_cred.modelo1.base.media.nivel_pico` | 1,659 | nivel pico; `005-estres` | `{{< var estres.sens_cred.modelo1.base.media.nivel_pico >}}` |
| `estres.sens_cred.modelo1.base.media.nivel_pico_trimestre` | 2029T1 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_cred.modelo1.base.media.nivel_pico_trimestre >}}` |
| `estres.sens_cred.modelo1.severo.cero.nivel_final` | 2,026 | nivel final; `005-estres` | `{{< var estres.sens_cred.modelo1.severo.cero.nivel_final >}}` |
| `estres.sens_cred.modelo1.severo.cero.nivel_pico` | 3,167 | nivel pico; `005-estres` | `{{< var estres.sens_cred.modelo1.severo.cero.nivel_pico >}}` |
| `estres.sens_cred.modelo1.severo.cero.nivel_pico_trimestre` | 2028T1 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_cred.modelo1.severo.cero.nivel_pico_trimestre >}}` |
| `estres.sens_cred.modelo1.severo.media.nivel_final` | 3,076 | nivel final; `005-estres` | `{{< var estres.sens_cred.modelo1.severo.media.nivel_final >}}` |
| `estres.sens_cred.modelo1.severo.media.nivel_pico` | 3,554 | nivel pico; `005-estres` | `{{< var estres.sens_cred.modelo1.severo.media.nivel_pico >}}` |
| `estres.sens_cred.modelo1.severo.media.nivel_pico_trimestre` | 2028T3 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_cred.modelo1.severo.media.nivel_pico_trimestre >}}` |
| `estres.sens_cred.modelo2.base.cero.nivel_final` | 0,718 | nivel final; `005-estres` | `{{< var estres.sens_cred.modelo2.base.cero.nivel_final >}}` |
| `estres.sens_cred.modelo2.base.cero.nivel_pico` | 1,584 | nivel pico; `005-estres` | `{{< var estres.sens_cred.modelo2.base.cero.nivel_pico >}}` |
| `estres.sens_cred.modelo2.base.cero.nivel_pico_trimestre` | 2027T3 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_cred.modelo2.base.cero.nivel_pico_trimestre >}}` |
| `estres.sens_cred.modelo2.base.media.nivel_final` | 1,569 | nivel final; `005-estres` | `{{< var estres.sens_cred.modelo2.base.media.nivel_final >}}` |
| `estres.sens_cred.modelo2.base.media.nivel_pico` | 1,661 | nivel pico; `005-estres` | `{{< var estres.sens_cred.modelo2.base.media.nivel_pico >}}` |
| `estres.sens_cred.modelo2.base.media.nivel_pico_trimestre` | 2028T1 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_cred.modelo2.base.media.nivel_pico_trimestre >}}` |
| `estres.sens_cred.modelo2.severo.cero.nivel_final` | 1,545 | nivel final; `005-estres` | `{{< var estres.sens_cred.modelo2.severo.cero.nivel_final >}}` |
| `estres.sens_cred.modelo2.severo.cero.nivel_pico` | 2,661 | nivel pico; `005-estres` | `{{< var estres.sens_cred.modelo2.severo.cero.nivel_pico >}}` |
| `estres.sens_cred.modelo2.severo.cero.nivel_pico_trimestre` | 2028T1 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_cred.modelo2.severo.cero.nivel_pico_trimestre >}}` |
| `estres.sens_cred.modelo2.severo.media.nivel_final` | 2,396 | nivel final; `005-estres` | `{{< var estres.sens_cred.modelo2.severo.media.nivel_final >}}` |
| `estres.sens_cred.modelo2.severo.media.nivel_pico` | 2,928 | nivel pico; `005-estres` | `{{< var estres.sens_cred.modelo2.severo.media.nivel_pico >}}` |
| `estres.sens_cred.modelo2.severo.media.nivel_pico_trimestre` | 2028T2 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_cred.modelo2.severo.media.nivel_pico_trimestre >}}` |
| `estres.sens_origen.modelo1.base.nivel_final` | 1,730 | nivel final; `005-estres` | `{{< var estres.sens_origen.modelo1.base.nivel_final >}}` |
| `estres.sens_origen.modelo1.base.nivel_pico` | 1,730 | nivel pico; `005-estres` | `{{< var estres.sens_origen.modelo1.base.nivel_pico >}}` |
| `estres.sens_origen.modelo1.base.nivel_pico_trimestre` | 2029T1 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_origen.modelo1.base.nivel_pico_trimestre >}}` |
| `estres.sens_origen.modelo1.severo.nivel_final` | 3,158 | nivel final; `005-estres` | `{{< var estres.sens_origen.modelo1.severo.nivel_final >}}` |
| `estres.sens_origen.modelo1.severo.nivel_pico` | 3,466 | nivel pico; `005-estres` | `{{< var estres.sens_origen.modelo1.severo.nivel_pico >}}` |
| `estres.sens_origen.modelo1.severo.nivel_pico_trimestre` | 2028T1 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_origen.modelo1.severo.nivel_pico_trimestre >}}` |
| `estres.sens_origen.modelo1.severo.delta_k13` | 1,428 | delta k13; `005-estres` | `{{< var estres.sens_origen.modelo1.severo.delta_k13 >}}` |
| `estres.sens_origen.modelo2.base.nivel_final` | 1,567 | nivel final; `005-estres` | `{{< var estres.sens_origen.modelo2.base.nivel_final >}}` |
| `estres.sens_origen.modelo2.base.nivel_pico` | 1,567 | nivel pico; `005-estres` | `{{< var estres.sens_origen.modelo2.base.nivel_pico >}}` |
| `estres.sens_origen.modelo2.base.nivel_pico_trimestre` | 2029T1 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_origen.modelo2.base.nivel_pico_trimestre >}}` |
| `estres.sens_origen.modelo2.severo.nivel_final` | 2,394 | nivel final; `005-estres` | `{{< var estres.sens_origen.modelo2.severo.nivel_final >}}` |
| `estres.sens_origen.modelo2.severo.nivel_pico` | 2,798 | nivel pico; `005-estres` | `{{< var estres.sens_origen.modelo2.severo.nivel_pico >}}` |
| `estres.sens_origen.modelo2.severo.nivel_pico_trimestre` | 2028T1 | nivel pico trimestre; `005-estres` | `{{< var estres.sens_origen.modelo2.severo.nivel_pico_trimestre >}}` |
| `estres.sens_origen.modelo2.severo.delta_k13` | 0,827 | delta k13; `005-estres` | `{{< var estres.sens_origen.modelo2.severo.delta_k13 >}}` |
| `estres.modelo1.credito.n_observados` | 4 | n observados; `005-estres` | `{{< var estres.modelo1.credito.n_observados >}}` |
| `estres.modelo1.credito.n_supuestos` | 9 | n supuestos; `005-estres` | `{{< var estres.modelo1.credito.n_supuestos >}}` |
| `estres.modelo1.base.nivel_final` | 1,989 | nivel final; `005-estres` | `{{< var estres.modelo1.base.nivel_final >}}` |
| `estres.modelo1.base.nivel_pico` | 1,989 | nivel pico; `005-estres` | `{{< var estres.modelo1.base.nivel_pico >}}` |
| `estres.modelo1.base.nivel_pico_trimestre` | 2029T3 | nivel pico trimestre; `005-estres` | `{{< var estres.modelo1.base.nivel_pico_trimestre >}}` |
| `estres.modelo1.severo.nivel_final` | 3,417 | nivel final; `005-estres` | `{{< var estres.modelo1.severo.nivel_final >}}` |
| `estres.modelo1.severo.nivel_pico` | 3,716 | nivel pico; `005-estres` | `{{< var estres.modelo1.severo.nivel_pico >}}` |
| `estres.modelo1.severo.nivel_pico_trimestre` | 2028T3 | nivel pico trimestre; `005-estres` | `{{< var estres.modelo1.severo.nivel_pico_trimestre >}}` |
| `estres.modelo1.severo.delta_final` | 1,428 | delta final; `005-estres` | `{{< var estres.modelo1.severo.delta_final >}}` |
| `estres.modelo1.severo.delta_final_p05` | -0,188 | delta final p05; `005-estres` | `{{< var estres.modelo1.severo.delta_final_p05 >}}` |
| `estres.modelo1.severo.delta_final_p95` | 2,288 | delta final p95; `005-estres` | `{{< var estres.modelo1.severo.delta_final_p95 >}}` |
| `estres.modelo1.severo.delta_pico` | 1,898 | delta pico; `005-estres` | `{{< var estres.modelo1.severo.delta_pico >}}` |
| `estres.modelo1.severo.delta_pico_trimestre` | 2028T3 | delta pico trimestre; `005-estres` | `{{< var estres.modelo1.severo.delta_pico_trimestre >}}` |
| `estres.modelo1.severo.delta_min` | 0,129 | delta min; `005-estres` | `{{< var estres.modelo1.severo.delta_min >}}` |
| `estres.modelo1.severo.delta_sin_aumento` | no | delta sin aumento; `005-estres` | `{{< var estres.modelo1.severo.delta_sin_aumento >}}` |
| `estres.modelo1.severo.delta_prop_pos_final` | 0,935 | delta prop pos final; `005-estres` | `{{< var estres.modelo1.severo.delta_prop_pos_final >}}` |
| `estres.modelo1.severo.delta_prop_pos_pico` | 0,951 | delta prop pos pico; `005-estres` | `{{< var estres.modelo1.severo.delta_prop_pos_pico >}}` |
| `estres.modelo1.propio.nivel_final` | 3,417 | nivel final; `005-estres` | `{{< var estres.modelo1.propio.nivel_final >}}` |
| `estres.modelo1.propio.nivel_pico` | 3,716 | nivel pico; `005-estres` | `{{< var estres.modelo1.propio.nivel_pico >}}` |
| `estres.modelo1.propio.nivel_pico_trimestre` | 2028T3 | nivel pico trimestre; `005-estres` | `{{< var estres.modelo1.propio.nivel_pico_trimestre >}}` |
| `estres.modelo1.propio.delta_final` | 1,428 | delta final; `005-estres` | `{{< var estres.modelo1.propio.delta_final >}}` |
| `estres.modelo1.propio.delta_final_p05` | -0,188 | delta final p05; `005-estres` | `{{< var estres.modelo1.propio.delta_final_p05 >}}` |
| `estres.modelo1.propio.delta_final_p95` | 2,288 | delta final p95; `005-estres` | `{{< var estres.modelo1.propio.delta_final_p95 >}}` |
| `estres.modelo1.propio.delta_pico` | 1,898 | delta pico; `005-estres` | `{{< var estres.modelo1.propio.delta_pico >}}` |
| `estres.modelo1.propio.delta_pico_trimestre` | 2028T3 | delta pico trimestre; `005-estres` | `{{< var estres.modelo1.propio.delta_pico_trimestre >}}` |
| `estres.modelo1.propio.delta_min` | 0,129 | delta min; `005-estres` | `{{< var estres.modelo1.propio.delta_min >}}` |
| `estres.modelo1.propio.delta_sin_aumento` | no | delta sin aumento; `005-estres` | `{{< var estres.modelo1.propio.delta_sin_aumento >}}` |
| `estres.modelo1.propio.delta_prop_pos_final` | 0,935 | delta prop pos final; `005-estres` | `{{< var estres.modelo1.propio.delta_prop_pos_final >}}` |
| `estres.modelo1.propio.delta_prop_pos_pico` | 0,951 | delta prop pos pico; `005-estres` | `{{< var estres.modelo1.propio.delta_prop_pos_pico >}}` |
| `estres.modelo1.fuera_rango.n` | 105 | n; `005-estres` | `{{< var estres.modelo1.fuera_rango.n >}}` |
| `estres.modelo1.fuera_rango.prop` | 0,011 | prop; `005-estres` | `{{< var estres.modelo1.fuera_rango.prop >}}` |
| `estres.modelo1.fuera_rango.min` | -10,323 | min; `005-estres` | `{{< var estres.modelo1.fuera_rango.min >}}` |
| `estres.modelo1.fuera_rango.max` | 6,497 | max; `005-estres` | `{{< var estres.modelo1.fuera_rango.max >}}` |
| `estres.modelo1.explosivas.n` | 1 | n; `005-estres` | `{{< var estres.modelo1.explosivas.n >}}` |
| `estres.modelo1.explosivas.prop` | 0,000 | prop; `005-estres` | `{{< var estres.modelo1.explosivas.prop >}}` |
| `estres.modelo2.credito.n_observados` | 4 | n observados; `005-estres` | `{{< var estres.modelo2.credito.n_observados >}}` |
| `estres.modelo2.credito.n_supuestos` | 9 | n supuestos; `005-estres` | `{{< var estres.modelo2.credito.n_supuestos >}}` |
| `estres.modelo2.base.nivel_final` | 1,845 | nivel final; `005-estres` | `{{< var estres.modelo2.base.nivel_final >}}` |
| `estres.modelo2.base.nivel_pico` | 1,845 | nivel pico; `005-estres` | `{{< var estres.modelo2.base.nivel_pico >}}` |
| `estres.modelo2.base.nivel_pico_trimestre` | 2029T3 | nivel pico trimestre; `005-estres` | `{{< var estres.modelo2.base.nivel_pico_trimestre >}}` |
| `estres.modelo2.severo.nivel_final` | 2,672 | nivel final; `005-estres` | `{{< var estres.modelo2.severo.nivel_final >}}` |
| `estres.modelo2.severo.nivel_pico` | 3,052 | nivel pico; `005-estres` | `{{< var estres.modelo2.severo.nivel_pico >}}` |
| `estres.modelo2.severo.nivel_pico_trimestre` | 2028T3 | nivel pico trimestre; `005-estres` | `{{< var estres.modelo2.severo.nivel_pico_trimestre >}}` |
| `estres.modelo2.severo.delta_final` | 0,827 | delta final; `005-estres` | `{{< var estres.modelo2.severo.delta_final >}}` |
| `estres.modelo2.severo.delta_final_p05` | -0,479 | delta final p05; `005-estres` | `{{< var estres.modelo2.severo.delta_final_p05 >}}` |
| `estres.modelo2.severo.delta_final_p95` | 1,721 | delta final p95; `005-estres` | `{{< var estres.modelo2.severo.delta_final_p95 >}}` |
| `estres.modelo2.severo.delta_pico` | 1,286 | delta pico; `005-estres` | `{{< var estres.modelo2.severo.delta_pico >}}` |
| `estres.modelo2.severo.delta_pico_trimestre` | 2028T3 | delta pico trimestre; `005-estres` | `{{< var estres.modelo2.severo.delta_pico_trimestre >}}` |
| `estres.modelo2.severo.delta_min` | 0,000 | delta min; `005-estres` | `{{< var estres.modelo2.severo.delta_min >}}` |
| `estres.modelo2.severo.delta_sin_aumento` | no | delta sin aumento; `005-estres` | `{{< var estres.modelo2.severo.delta_sin_aumento >}}` |
| `estres.modelo2.severo.delta_prop_pos_final` | 0,877 | delta prop pos final; `005-estres` | `{{< var estres.modelo2.severo.delta_prop_pos_final >}}` |
| `estres.modelo2.severo.delta_prop_pos_pico` | 0,934 | delta prop pos pico; `005-estres` | `{{< var estres.modelo2.severo.delta_prop_pos_pico >}}` |
| `estres.modelo2.propio.nivel_final` | 2,672 | nivel final; `005-estres` | `{{< var estres.modelo2.propio.nivel_final >}}` |
| `estres.modelo2.propio.nivel_pico` | 3,052 | nivel pico; `005-estres` | `{{< var estres.modelo2.propio.nivel_pico >}}` |
| `estres.modelo2.propio.nivel_pico_trimestre` | 2028T3 | nivel pico trimestre; `005-estres` | `{{< var estres.modelo2.propio.nivel_pico_trimestre >}}` |
| `estres.modelo2.propio.delta_final` | 0,827 | delta final; `005-estres` | `{{< var estres.modelo2.propio.delta_final >}}` |
| `estres.modelo2.propio.delta_final_p05` | -0,479 | delta final p05; `005-estres` | `{{< var estres.modelo2.propio.delta_final_p05 >}}` |
| `estres.modelo2.propio.delta_final_p95` | 1,721 | delta final p95; `005-estres` | `{{< var estres.modelo2.propio.delta_final_p95 >}}` |
| `estres.modelo2.propio.delta_pico` | 1,286 | delta pico; `005-estres` | `{{< var estres.modelo2.propio.delta_pico >}}` |
| `estres.modelo2.propio.delta_pico_trimestre` | 2028T3 | delta pico trimestre; `005-estres` | `{{< var estres.modelo2.propio.delta_pico_trimestre >}}` |
| `estres.modelo2.propio.delta_min` | 0,000 | delta min; `005-estres` | `{{< var estres.modelo2.propio.delta_min >}}` |
| `estres.modelo2.propio.delta_sin_aumento` | no | delta sin aumento; `005-estres` | `{{< var estres.modelo2.propio.delta_sin_aumento >}}` |
| `estres.modelo2.propio.delta_prop_pos_final` | 0,877 | delta prop pos final; `005-estres` | `{{< var estres.modelo2.propio.delta_prop_pos_final >}}` |
| `estres.modelo2.propio.delta_prop_pos_pico` | 0,934 | delta prop pos pico; `005-estres` | `{{< var estres.modelo2.propio.delta_prop_pos_pico >}}` |
| `estres.modelo2.fuera_rango.n` | 160 | n; `005-estres` | `{{< var estres.modelo2.fuera_rango.n >}}` |
| `estres.modelo2.fuera_rango.prop` | 0,016 | prop; `005-estres` | `{{< var estres.modelo2.fuera_rango.prop >}}` |
| `estres.modelo2.fuera_rango.min` | -6,120 | min; `005-estres` | `{{< var estres.modelo2.fuera_rango.min >}}` |
| `estres.modelo2.fuera_rango.max` | 9,921 | max; `005-estres` | `{{< var estres.modelo2.fuera_rango.max >}}` |
| `estres.modelo2.explosivas.n` | 1 | n; `005-estres` | `{{< var estres.modelo2.explosivas.n >}}` |
| `estres.modelo2.explosivas.prop` | 0,000 | prop; `005-estres` | `{{< var estres.modelo2.explosivas.prop >}}` |
| `literatura.n_estudios_verificados` | 17 | n estudios verificados; `006-informe` | `{{< var literatura.n_estudios_verificados >}}` |
| `literatura.n_pendiente_lectura` | 8 | n pendiente lectura; `006-informe` | `{{< var literatura.n_pendiente_lectura >}}` |
| `literatura.n_descartados` | 3 | n descartados; `006-informe` | `{{< var literatura.n_descartados >}}` |
| `literatura.n_datos_metodo_verificados` | 4 | n datos metodo verificados; `006-informe` | `{{< var literatura.n_datos_metodo_verificados >}}` |
| `literatura.por_tema.t21` | 2 | t21; `006-informe` | `{{< var literatura.por_tema.t21 >}}` |
| `literatura.por_tema.t22` | 2 | t22; `006-informe` | `{{< var literatura.por_tema.t22 >}}` |
| `literatura.por_tema.t23` | 2 | t23; `006-informe` | `{{< var literatura.por_tema.t23 >}}` |
| `literatura.por_tema.t24` | 2 | t24; `006-informe` | `{{< var literatura.por_tema.t24 >}}` |
| `literatura.por_tema.t25` | 9 | t25; `006-informe` | `{{< var literatura.por_tema.t25 >}}` |
| `informe.historia_inicio` | 1998T1 | historia inicio; `006-informe` | `{{< var informe.historia_inicio >}}` |
| `informe.n_series_descargadas` | 13 | n series descargadas; `006-informe` | `{{< var informe.n_series_descargadas >}}` |
| `informe.n_series_nota` | Series del manifiesto congelado, incluidas las fuentes de robustez; no es el número de columnas transformadas ni de regresores. | n series nota; `006-informe` | `{{< var informe.n_series_nota >}}` |
| `informe.escenario_d.n_alzas` | 7 | n alzas; `006-informe` | `{{< var informe.escenario_d.n_alzas >}}` |
| `informe.escenario_d.n_ceros` | 6 | n ceros; `006-informe` | `{{< var informe.escenario_d.n_ceros >}}` |
| `informe.escenario_d.inicio_adaptado` | 2026T3 | inicio adaptado; `006-informe` | `{{< var informe.escenario_d.inicio_adaptado >}}` |
| `informe.escenario_d.fin_alzas_adaptado` | 2028T1 | fin alzas adaptado; `006-informe` | `{{< var informe.escenario_d.fin_alzas_adaptado >}}` |
| `informe.bandas.percentil_inferior` | 5 | percentil inferior; `006-informe` | `{{< var informe.bandas.percentil_inferior >}}` |
| `informe.bandas.percentil_superior` | 95 | percentil superior; `006-informe` | `{{< var informe.bandas.percentil_superior >}}` |
| `informe.bandas.origen` | Columnas p05 y p95 de stress_levels.csv; incertidumbre de parámetros, no predicción. | origen; `006-informe` | `{{< var informe.bandas.origen >}}` |

## Tablas, figuras y otras fuentes disponibles

Las tablas de presentación y los anexos son derivados de 006; los originales conservan sus bytes.

| Ruta | Descripción | Clase y origen | SHA-256 |
| --- | --- | --- | --- |
| [data/processed/panel.csv](../../data/processed/panel.csv) | Panel trimestral aprobado | Fuente aprobada; `001-datos` | `f800f4fdd8990b5df2b3302d64f65e4dd41a2dbb78f114e9a31f9c11f7c9297c` |
| [data/raw/manifest.csv](../../data/raw/manifest.csv) | Manifiesto del vintage FRED congelado | Fuente aprobada; `001-datos` | `c77a236d83fa6051693d64392be6127675d63bfe29c01178398a5d0a2c2a1cca` |
| [outputs/data_note.md](../../outputs/data_note.md) | Nota aprobada sobre datos y faltantes | Fuente aprobada; `001-datos` | `3131d088cc8b1bc19cebdf00ea73a7dbec5b67eea07dcbe2340c37018e4598c4` |
| [outputs/figures/delinquency_unemployment_ffr.png](../../outputs/figures/delinquency_unemployment_ffr.png) | Morosidad, desempleo y tasa de política | Figura PNG; `001-datos` | `da8f33a069474e040110129c0b6f40ae6098f5ed470656cd3efa0ccd2ae3667d` |
| [outputs/figures/model1_coefficients.png](../../outputs/figures/model1_coefficients.png) | Modelo I — coeficientes | Figura PNG; `003-modelo-i` | `96544c3ff8320b16ea39307211536acd3d2d2c160466de7b6d4d1e852d1bed69` |
| [outputs/figures/model1_cusum.png](../../outputs/figures/model1_cusum.png) | Modelo I — CUSUM | Figura PNG; `003-modelo-i` | `9c146745c6dd0901e45e507d505f5bb18ca679071177659c1bf26518484015c9` |
| [outputs/figures/model1_oos.png](../../outputs/figures/model1_oos.png) | Modelo I — evaluación fuera de muestra | Figura PNG; `003-modelo-i` | `fff5319d59646b3596c030889fd412aebdb59f3488a873fd1be5725a18fe2640` |
| [outputs/figures/model2_cusum.png](../../outputs/figures/model2_cusum.png) | Modelo II — CUSUM | Figura PNG; `004-modelo-ii` | `e7840a9e5d9446e96e6e1c020c2741a6450f8804b3bb25aca481a326be7c5766` |
| [outputs/figures/model2_profile.png](../../outputs/figures/model2_profile.png) | Modelo II — perfil acumulado | Figura PNG; `004-modelo-ii` | `697ed2783a40d5621c4eeb474c5317604474951cd06a1b428630c5b0f8dedd21` |
| [outputs/figures/model2_response.png](../../outputs/figures/model2_response.png) | Modelo II — respuestas dinámicas | Figura PNG; `004-modelo-ii` | `d5442ad7d6a15639027b07fcd1a5f10c1aa0e53fbd991da7f4c2f98a9af72944` |
| [outputs/figures/stress_model1.png](../../outputs/figures/stress_model1.png) | Estrés — Modelo I | Figura PNG; `005-estres` | `e58258937a62d56bfbf8162e019717ae0e6340df3c77152cfe0c3b8944dc69dd` |
| [outputs/figures/stress_model2.png](../../outputs/figures/stress_model2.png) | Estrés — Modelo II | Figura PNG; `005-estres` | `1e09416817722fcd6a3d00e3f42c8cea3df0c5b3ba70bcb81bf63744ebbec3a4` |
| [outputs/informe/body_trace.json](../../outputs/informe/body_trace.json) | body trace | Derivado de presentación; `006-informe (derivada de 001-datos)` | `6bc8bf882c58ebde79aa3170013f313c21f35bc0b3c73afae884a32876c7d3d5` |
| [outputs/informe/descriptives.md](../../outputs/informe/descriptives.md) | Estadísticos descriptivos | Derivado de presentación; `006-informe (derivada de 001-datos)` | `e61f051188c873dee71ea36247547fc9b1c665dcc7e6e7483568f658aad4fe20` |
| [outputs/informe/descriptives_anexo_1.md](../../outputs/informe/descriptives_anexo_1.md) | Estadísticos descriptivos | Derivado de presentación; `006-informe (derivada de 001-datos)` | `49f441961139295e89959a34eb0b76fd51fb1b42f79a48fc8eabca96ffc36b0a` |
| [outputs/informe/descriptives_anexo_2.md](../../outputs/informe/descriptives_anexo_2.md) | Estadísticos descriptivos | Derivado de presentación; `006-informe (derivada de 001-datos)` | `f21558cf31db58353ea4762301528560c8f06981057340d859bf35461f4520d0` |
| [outputs/informe/destinos.json](../../outputs/informe/destinos.json) | destinos | Derivado de presentación; `006-informe (derivada de 001-datos)` | `c81c3f555c69f06168fbcf8931be76a846910850b419cf109103c4996f9b08a5` |
| [outputs/informe/enlaces.csv](../../outputs/informe/enlaces.csv) | enlaces | Derivado de presentación; `006-informe (derivada de 001-datos)` | `ab47b97cef9b3ce2f8ea3b7f251875d88325eb549d8e5d6d232e497704c69ecc` |
| [outputs/informe/fred_manifest.md](../../outputs/informe/fred_manifest.md) | Manifiesto de fuentes congeladas | Derivado de presentación; `006-informe (derivada de 001-datos)` | `1616f67ebc31177b2d7d576f79f9cdbf9da33070f8651eb1d32ff9cb09a276c0` |
| [outputs/informe/fred_manifest_anexo_1.md](../../outputs/informe/fred_manifest_anexo_1.md) | Manifiesto de fuentes congeladas | Derivado de presentación; `006-informe (derivada de 001-datos)` | `5a1ec9bbaaf545f3b7150bf476012b77fc7587e390064610c8fc9f042f1fc192` |
| [outputs/informe/fred_manifest_anexo_2.md](../../outputs/informe/fred_manifest_anexo_2.md) | Manifiesto de fuentes congeladas | Derivado de presentación; `006-informe (derivada de 001-datos)` | `5bd7a77e8790a7595a534cc303e8a8b86519260b4d55ed13233d8b310f167b7b` |
| [outputs/informe/fred_manifest_cuerpo.md](../../outputs/informe/fred_manifest_cuerpo.md) | fred manifest cuerpo | Derivado de presentación; `006-informe (derivada de 001-datos)` | `a4534d166a6ad17b96c24e276efe6053057c771eea77fd28ad7a9c23c4536e01` |
| [outputs/informe/fred_manifest_cuerpo_combinado.md](../../outputs/informe/fred_manifest_cuerpo_combinado.md) | fred manifest cuerpo combinado | Derivado de presentación; `006-informe (derivada de 001-datos)` | `89995f2053d359a23c6795b14a4ba65f952a35d01da0ad7ff73af1f77156018b` |
| [outputs/informe/lit_estudios.md](../../outputs/informe/lit_estudios.md) | Estudios verificados: variables, métodos y signos | Derivado de presentación; `006-informe (derivada de 006-informe desde 002-literatura)` | `bc037b7669ccc8c763e15dcfa1b5c38a8d04fe5d4dd36711eda57de5da91c913` |
| [outputs/informe/lit_estudios_anexo_1.md](../../outputs/informe/lit_estudios_anexo_1.md) | Estudios verificados: variables, métodos y signos | Derivado de presentación; `006-informe (derivada de 006-informe desde 002-literatura)` | `533990364791eb7a128621772002e897527a196623d944ed1e8b8d8516ac736c` |
| [outputs/informe/lit_estudios_anexo_2.md](../../outputs/informe/lit_estudios_anexo_2.md) | Estudios verificados: variables, métodos y signos | Derivado de presentación; `006-informe (derivada de 006-informe desde 002-literatura)` | `e22c51276a7efda638a65c8b9eb31a4840ea478c9b137ae8d7ab3dbca743943a` |
| [outputs/informe/lit_estudios_anexo_3.md](../../outputs/informe/lit_estudios_anexo_3.md) | Estudios verificados: variables, métodos y signos | Derivado de presentación; `006-informe (derivada de 006-informe desde 002-literatura)` | `027b269f2f404da3345b2ecbf6eb2ecf440f5c92b990ce1d6aca9759821db5cd` |
| [outputs/informe/lit_estudios_cuerpo.md](../../outputs/informe/lit_estudios_cuerpo.md) | lit estudios cuerpo | Derivado de presentación; `006-informe (derivada de 006-informe desde 002-literatura)` | `3c51532e795cd8a73eaef7ce0c61455e5a0276f63f440d81a5c7b57507fd4889` |
| [outputs/informe/lit_estudios_cuerpo_combinado.md](../../outputs/informe/lit_estudios_cuerpo_combinado.md) | lit estudios cuerpo combinado | Derivado de presentación; `006-informe (derivada de 006-informe desde 002-literatura)` | `19719a71438ae6e0bfbfe7afc716615828f90696c53802bffd7a52d500fb7cfe` |
| [outputs/informe/model1_coefficients.md](../../outputs/informe/model1_coefficients.md) | Modelo I — coeficientes | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `d052a77df06a230b53a92225ec4ecbcce7a66dc95c7bb1e4300c7c953fb6c144` |
| [outputs/informe/model1_coefficients_anexo_1.md](../../outputs/informe/model1_coefficients_anexo_1.md) | Modelo I — coeficientes | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `f8794cf41dcbf06b73002763ed21bc0d8e1b21b5c297d5f40a79332d1788772a` |
| [outputs/informe/model1_coefficients_anexo_2.md](../../outputs/informe/model1_coefficients_anexo_2.md) | Modelo I — coeficientes | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `fe5d4809eb274ce0a7e976d475a20d66b8f12711a30a81a3c92cf0f76dd7756d` |
| [outputs/informe/model1_coefficients_anexo_3.md](../../outputs/informe/model1_coefficients_anexo_3.md) | Modelo I — coeficientes | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `a80c0f109a91c740b17470cf7b3c7a34c774462ae155fc84dd8cf0957954282a` |
| [outputs/informe/model1_coefficients_anexo_4.md](../../outputs/informe/model1_coefficients_anexo_4.md) | Modelo I — coeficientes | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `8f76dfeedbea1411f7a8681e3f53bd71d7cbe23613e4c2cbfae2c03da8eb5f35` |
| [outputs/informe/model1_coefficients_cuerpo.md](../../outputs/informe/model1_coefficients_cuerpo.md) | model1 coefficients cuerpo | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `6d0dac48c3b81ebafd03b8bd5aeeb2337507a0c9c6edf6c42361a3f0d4b41e48` |
| [outputs/informe/model1_coefficients_cuerpo_combinado.md](../../outputs/informe/model1_coefficients_cuerpo_combinado.md) | model1 coefficients cuerpo combinado | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `6d0dac48c3b81ebafd03b8bd5aeeb2337507a0c9c6edf6c42361a3f0d4b41e48` |
| [outputs/informe/model1_coefficients_nota.md](../../outputs/informe/model1_coefficients_nota.md) | model1 coefficients nota | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `b3ad6ef6412aac99a76f67be420057faebf4203c877b6361fe6015183f990bda` |
| [outputs/informe/model1_deviations.md](../../outputs/informe/model1_deviations.md) | Modelo I — desviaciones | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `b3ab9a2f91e27acb075d8d287b74e616dab96cbadb30af61479104b8d7865ce3` |
| [outputs/informe/model1_deviations_anexo_1.md](../../outputs/informe/model1_deviations_anexo_1.md) | Modelo I — desviaciones | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `b3ab9a2f91e27acb075d8d287b74e616dab96cbadb30af61479104b8d7865ce3` |
| [outputs/informe/model1_diagnostics.md](../../outputs/informe/model1_diagnostics.md) | Modelo I — diagnósticos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `a3b97c2b604e3d6f96f076db475bf7968df99f5391be8e1c833e0e89c9240661` |
| [outputs/informe/model1_diagnostics_anexo_1.md](../../outputs/informe/model1_diagnostics_anexo_1.md) | Modelo I — diagnósticos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `3cf6c8e66347f5b417c6de384b3683319e95683e0ed9169c763566383520d7f1` |
| [outputs/informe/model1_diagnostics_anexo_2.md](../../outputs/informe/model1_diagnostics_anexo_2.md) | Modelo I — diagnósticos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `9c716b0627c1b7d0c9d730a468ba1033663b0f1a4431fbbc784dc472d7126972` |
| [outputs/informe/model1_diagnostics_cuerpo.md](../../outputs/informe/model1_diagnostics_cuerpo.md) | model1 diagnostics cuerpo | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `b08a34f2074ef809a62867901a1d7219aff4a94e9aa11de8cbaf625dfa436922` |
| [outputs/informe/model1_diagnostics_cuerpo_combinado.md](../../outputs/informe/model1_diagnostics_cuerpo_combinado.md) | model1 diagnostics cuerpo combinado | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `77796bb1f571f8ce2c5934e464ec5fe8b350fb754dc63306e3737bdf6516a2d7` |
| [outputs/informe/model1_effects.md](../../outputs/informe/model1_effects.md) | Modelo I — efectos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `05cf964d56ba19a6e243a66c48e8b031d09c29aaf9dd18a9f381da2c37876398` |
| [outputs/informe/model1_effects_anexo_1.md](../../outputs/informe/model1_effects_anexo_1.md) | Modelo I — efectos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `8bdc30f951878ce7f246572e19be8424a508460423cadecc98c84b079fc20b1c` |
| [outputs/informe/model1_effects_anexo_2.md](../../outputs/informe/model1_effects_anexo_2.md) | Modelo I — efectos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `6640b9b5da5e70975d131030e4489c60b8fb63dc40f5f39215c681b4b2ec4421` |
| [outputs/informe/model1_effects_anexo_3.md](../../outputs/informe/model1_effects_anexo_3.md) | Modelo I — efectos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `f4f53864418a5c2b576198a62f4fc8333405cf29b0f5afc93eb9b086ab6b07cc` |
| [outputs/informe/model1_effects_anexo_4.md](../../outputs/informe/model1_effects_anexo_4.md) | Modelo I — efectos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `eb47c681e983b85bed40af40ffa6a9d9321c33bd952b4ba340ef069ac067ea2d` |
| [outputs/informe/model1_effects_anexo_5.md](../../outputs/informe/model1_effects_anexo_5.md) | Modelo I — efectos | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `c099cff67800ca1ad1b8164411d3ddb0f5ee9f2f78a5fb2b2c4d941ffa5e75a2` |
| [outputs/informe/model1_effects_nota.md](../../outputs/informe/model1_effects_nota.md) | model1 effects nota | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `16e3c7abe9286775d86a37130e32bcc940a862f0ff0dab6adbadfed01a9996dc` |
| [outputs/informe/model1_limitations.md](../../outputs/informe/model1_limitations.md) | Modelo I — limitaciones | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `d9fcbc6e83bd0237acfdd777f86343248e3109bcfb691b34ae49233a23c1ecfb` |
| [outputs/informe/model1_limitations_anexo_1.md](../../outputs/informe/model1_limitations_anexo_1.md) | Modelo I — limitaciones | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `d9fcbc6e83bd0237acfdd777f86343248e3109bcfb691b34ae49233a23c1ecfb` |
| [outputs/informe/model1_oos.md](../../outputs/informe/model1_oos.md) | Modelo I — evaluación fuera de muestra | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `ae521d7004ecf046b7726c91658df63664fabe54f7179df7483e82e8db94815e` |
| [outputs/informe/model1_oos_anexo_1.md](../../outputs/informe/model1_oos_anexo_1.md) | Modelo I — evaluación fuera de muestra | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `fe85e11c909a42443ae19a6cff37002a23e1bc3f78908e27b7de3420de6deaf5` |
| [outputs/informe/model1_oos_anexo_2.md](../../outputs/informe/model1_oos_anexo_2.md) | Modelo I — evaluación fuera de muestra | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `e095790d2ea59cee10a33265b424add154a69b3bf04ae6ba92c5ec2d80b27c18` |
| [outputs/informe/model1_oos_anexo_3.md](../../outputs/informe/model1_oos_anexo_3.md) | Modelo I — evaluación fuera de muestra | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `982ba062c9de0672c80004800f598bfe236490213dd2eabe099a4de45c8e6098` |
| [outputs/informe/model1_oos_anexo_4.md](../../outputs/informe/model1_oos_anexo_4.md) | Modelo I — evaluación fuera de muestra | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `3815b7fb8e753888b58565e4e2ae8f0b565e4089bdd3630a3d3e9b1080b0f7b8` |
| [outputs/informe/model1_robustness_estimates.md](../../outputs/informe/model1_robustness_estimates.md) | Modelo I — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `c18e101293f80abeb48fb01e77806b1229a03e5fc42babf8cac5718a389ee357` |
| [outputs/informe/model1_robustness_estimates_anexo_1.md](../../outputs/informe/model1_robustness_estimates_anexo_1.md) | Modelo I — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `a348a8cf0ec456fbb30e6ecafd3611a16eae14e8ed64a807b38cd9578414e745` |
| [outputs/informe/model1_robustness_estimates_anexo_2.md](../../outputs/informe/model1_robustness_estimates_anexo_2.md) | Modelo I — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `8673f8036cdcae72b6fe3e55ddc6b67d59a472cd2f3643ed9377b728e7b94857` |
| [outputs/informe/model1_robustness_estimates_anexo_3.md](../../outputs/informe/model1_robustness_estimates_anexo_3.md) | Modelo I — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `d3f4926c5d87ef659f8740e7a51f8ba19918e367e81e6a7006db40dee66d7070` |
| [outputs/informe/model1_robustness_estimates_anexo_4.md](../../outputs/informe/model1_robustness_estimates_anexo_4.md) | Modelo I — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `5380d5e54f0532f700703eea19f450b30431213d2ccc6dd3cc6326b391af4718` |
| [outputs/informe/model1_robustness_estimates_anexo_5.md](../../outputs/informe/model1_robustness_estimates_anexo_5.md) | Modelo I — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `d5cb78e4a652fad37e6bdc2cf6b265d97ea3b3380bd455237214c74407b328e0` |
| [outputs/informe/model1_robustness_summary.md](../../outputs/informe/model1_robustness_summary.md) | Modelo I — resumen de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `10d1ca11f6112b16f3fc6287a8c72f198f5e4aaec2e08a8797d40c3d0c7cbfe4` |
| [outputs/informe/model1_robustness_summary_anexo_1.md](../../outputs/informe/model1_robustness_summary_anexo_1.md) | Modelo I — resumen de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `a9f0bb10273710c28e9dc394c696a1da819fb1dfceb7e810c7c7ac4ec58467e0` |
| [outputs/informe/model1_robustness_summary_anexo_2.md](../../outputs/informe/model1_robustness_summary_anexo_2.md) | Modelo I — resumen de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `22adb6632abc476066dbf796db2a43dc3774289b4e8b53050d77450df8b2fe3e` |
| [outputs/informe/model1_robustness_summary_anexo_3.md](../../outputs/informe/model1_robustness_summary_anexo_3.md) | Modelo I — resumen de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `ae44fe7dad8cae0eaacbb1d1c0fb32e319c5a8e4a60247bc809e250bd9dcb054` |
| [outputs/informe/model1_robustness_summary_anexo_4.md](../../outputs/informe/model1_robustness_summary_anexo_4.md) | Modelo I — resumen de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `2b1a881a64175970171a2445805681e24b4b970fe3cb573b674cca3c98c8c4b2` |
| [outputs/informe/model1_robustness_summary_anexo_5.md](../../outputs/informe/model1_robustness_summary_anexo_5.md) | Modelo I — resumen de robustez | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `e2805516bbc0965fea9efb274b3abc4ff3d230e1e15d931b2b072f41d2147f6a` |
| [outputs/informe/model1_robustness_summary_nota.md](../../outputs/informe/model1_robustness_summary_nota.md) | model1 robustness summary nota | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `b91ce59e1765b833f0b7a107c57d07712f2f08a2af8eae06dcf9994f99d8b752` |
| [outputs/informe/model1_stationarity.md](../../outputs/informe/model1_stationarity.md) | Modelo I — estacionariedad | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `c3bc7a1f0d9997b6ca7c0d8fe2615fd1d90fbc57f4422f5538f2d3140d1b112f` |
| [outputs/informe/model1_stationarity_anexo_1.md](../../outputs/informe/model1_stationarity_anexo_1.md) | Modelo I — estacionariedad | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `26b710c659c9f66f6d5c4bd14639ba799d92fd7b1f3e7977aab2eb8f2523f631` |
| [outputs/informe/model1_stationarity_anexo_2.md](../../outputs/informe/model1_stationarity_anexo_2.md) | Modelo I — estacionariedad | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `84cc3f2da327788f4c1ba9b2a4813996a3a3fade22986d221f8f493c3b150a74` |
| [outputs/informe/model1_stationarity_anexo_3.md](../../outputs/informe/model1_stationarity_anexo_3.md) | Modelo I — estacionariedad | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `6c699608d5bc92a1f8029edb70f5cd805de9da8348221f203162cbefdcb83934` |
| [outputs/informe/model1_stationarity_anexo_4.md](../../outputs/informe/model1_stationarity_anexo_4.md) | Modelo I — estacionariedad | Derivado de presentación; `006-informe (derivada de 003-modelo-i)` | `5e3f7ae5b082691625f24ca7326915f5776d9e21d31cb319e3aface56b949070` |
| [outputs/informe/model2_coefficients.md](../../outputs/informe/model2_coefficients.md) | Modelo II — coeficientes | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `6da1a69865988493e013794b950a21fbe1ff9616422cdec822d44741a9239d14` |
| [outputs/informe/model2_coefficients_anexo_1.md](../../outputs/informe/model2_coefficients_anexo_1.md) | Modelo II — coeficientes | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `1bddcd987f93177b2a45f9c9048cf6e8e9d8f577213e44e8973823d2a9f837d3` |
| [outputs/informe/model2_coefficients_anexo_2.md](../../outputs/informe/model2_coefficients_anexo_2.md) | Modelo II — coeficientes | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `dc8f978d4d0d2b082ddfb68ac211429b0c9177d76f11497141d1a6d5f1912859` |
| [outputs/informe/model2_coefficients_anexo_3.md](../../outputs/informe/model2_coefficients_anexo_3.md) | Modelo II — coeficientes | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `d68c6bf2c6aa9ae20ddbbcf131746f6c88db4abc779fc064508e775f5f3cccde` |
| [outputs/informe/model2_coefficients_nota.md](../../outputs/informe/model2_coefficients_nota.md) | model2 coefficients nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `505e6fc70bdc02ca74354fd5d68a20b15c36d83581f7f283ebdbc5be68c964f3` |
| [outputs/informe/model2_comparison.md](../../outputs/informe/model2_comparison.md) | Modelo II — comparación dinámica | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `672ff1d85b3d2e527ed59fd6487a312716e5e08748e4ea53d12f666b5d400e8a` |
| [outputs/informe/model2_comparison_anexo_1.md](../../outputs/informe/model2_comparison_anexo_1.md) | Modelo II — comparación dinámica | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `e4c8fe13739af8138f11b3d3330f009a7917648e1d29ab40462c7c33543454d6` |
| [outputs/informe/model2_comparison_anexo_2.md](../../outputs/informe/model2_comparison_anexo_2.md) | Modelo II — comparación dinámica | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `477a31f4b688436184d3f97e87b1e43cdae6c63d85a2bda8499f7a65dcb1a145` |
| [outputs/informe/model2_comparison_nota.md](../../outputs/informe/model2_comparison_nota.md) | model2 comparison nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `55f26448151d93ae35407ff6e2a6744f292591775295cc16aa8bf4fd307db735` |
| [outputs/informe/model2_deviations.md](../../outputs/informe/model2_deviations.md) | Modelo II — desviaciones | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `0588d9414cda8872b08364ceab1b018cb4b85081e2c185943a3e1a2647592834` |
| [outputs/informe/model2_deviations_anexo_1.md](../../outputs/informe/model2_deviations_anexo_1.md) | Modelo II — desviaciones | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `0588d9414cda8872b08364ceab1b018cb4b85081e2c185943a3e1a2647592834` |
| [outputs/informe/model2_diagnostics.md](../../outputs/informe/model2_diagnostics.md) | Modelo II — diagnósticos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `b88c5eae71d9684718badb6d9a522658eaa10cb19bb13bfe930695c13356df91` |
| [outputs/informe/model2_diagnostics_anexo_1.md](../../outputs/informe/model2_diagnostics_anexo_1.md) | Modelo II — diagnósticos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `d92724474ad20afe58b412f793e89611e9f83f4c555bf5ba8d3078abbd2334a7` |
| [outputs/informe/model2_diagnostics_anexo_2.md](../../outputs/informe/model2_diagnostics_anexo_2.md) | Modelo II — diagnósticos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `ff340eab61f02e63b103b188c3daa7a00ce0be346eb2a23afccd40bb9856b96a` |
| [outputs/informe/model2_effects.md](../../outputs/informe/model2_effects.md) | Modelo II — efectos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `40b3ec94017ed717dc722be033bd68d838d7fe0685dd981e0ade9b67b9747220` |
| [outputs/informe/model2_effects_anexo_1.md](../../outputs/informe/model2_effects_anexo_1.md) | Modelo II — efectos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `d326b8710f40d824ba1042251c466ba229f48afe661b3b5ef9ae199139612ab5` |
| [outputs/informe/model2_effects_anexo_2.md](../../outputs/informe/model2_effects_anexo_2.md) | Modelo II — efectos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `40a83b111285b099e19bcced02bfae8959e89f9b17329856d3e4cd62bfeda786` |
| [outputs/informe/model2_effects_anexo_3.md](../../outputs/informe/model2_effects_anexo_3.md) | Modelo II — efectos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `07f2db6646b534c308d325ec7278286c6ddc422e807c163edcbe4a4ef6a5fa12` |
| [outputs/informe/model2_effects_nota.md](../../outputs/informe/model2_effects_nota.md) | model2 effects nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `fe593bd51505bb233ecbee49cc2c002e9b6870f3fb291858fb4f98661b7e3e26` |
| [outputs/informe/model2_inputs63.md](../../outputs/informe/model2_inputs63.md) | Insumos de comparación de modelos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `4435fed57793fea39eedf8f7382f502937b8b634363c24634cda1c17d778ee4f` |
| [outputs/informe/model2_inputs63_anexo_1.md](../../outputs/informe/model2_inputs63_anexo_1.md) | Insumos de comparación de modelos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `f7f75c62bfd8122cfbe454934de308b6d2a273b48707243f9af5851e49bfcd22` |
| [outputs/informe/model2_inputs63_anexo_2.md](../../outputs/informe/model2_inputs63_anexo_2.md) | Insumos de comparación de modelos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `d4a1f442f252e53f2776de72478cc6d81edb460fcc9ad710d484f686b6dacde6` |
| [outputs/informe/model2_inputs63_anexo_3.md](../../outputs/informe/model2_inputs63_anexo_3.md) | Insumos de comparación de modelos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `3e17613c19bc7ccc872818f84b5be07ea00d7128305df5af11b831bf4160c7ba` |
| [outputs/informe/model2_inputs63_cuerpo.md](../../outputs/informe/model2_inputs63_cuerpo.md) | model2 inputs63 cuerpo | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `266972cd1a68382e7cfac9bc28a6035a443fcd793c872e8042db294e05c1a079` |
| [outputs/informe/model2_inputs63_cuerpo_combinado.md](../../outputs/informe/model2_inputs63_cuerpo_combinado.md) | model2 inputs63 cuerpo combinado | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `361b90473a8658c54b606fd24f1ec73b2bb15088e73a2ac50c832f169e63b380` |
| [outputs/informe/model2_inputs63_nota.md](../../outputs/informe/model2_inputs63_nota.md) | model2 inputs63 nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `01781f89661af122b6fd05b5a18c9772262250f7b03947e9e37c302aae56aea0` |
| [outputs/informe/model2_limitations.md](../../outputs/informe/model2_limitations.md) | Modelo II — limitaciones | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `9bf18df83155f4ba2236ae9368fe0539afa22fd7830bd9e7a081feaa69b5d137` |
| [outputs/informe/model2_limitations_anexo_1.md](../../outputs/informe/model2_limitations_anexo_1.md) | Modelo II — limitaciones | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `9bf18df83155f4ba2236ae9368fe0539afa22fd7830bd9e7a081feaa69b5d137` |
| [outputs/informe/model2_lp.md](../../outputs/informe/model2_lp.md) | Modelo II — proyecciones locales | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `e5469b5f7fe5af2027da8ce4a2a8368eb2df587aced1365909f2e31ee508cea0` |
| [outputs/informe/model2_lp_anexo_1.md](../../outputs/informe/model2_lp_anexo_1.md) | Modelo II — proyecciones locales | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `cade1be3b52042971748a44f30c15cd6fbde6fbee495102c14ac8883781ab889` |
| [outputs/informe/model2_lp_anexo_2.md](../../outputs/informe/model2_lp_anexo_2.md) | Modelo II — proyecciones locales | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `b6e0add9fff4c0d7b3f856f080c34039f44ed1f3eae87ad1598d4dc5dd4885bd` |
| [outputs/informe/model2_lp_anexo_3.md](../../outputs/informe/model2_lp_anexo_3.md) | Modelo II — proyecciones locales | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `d6515040cdacfa7bba813abe3b89468ec6c3d9e00da419c1433eedabf2063282` |
| [outputs/informe/model2_lp_anexo_4.md](../../outputs/informe/model2_lp_anexo_4.md) | Modelo II — proyecciones locales | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `c50e548eaf4c959e1e82fe04d0a391f164a76ae9719bd0039371167e71d4a4f5` |
| [outputs/informe/model2_lp_anexo_5.md](../../outputs/informe/model2_lp_anexo_5.md) | Modelo II — proyecciones locales | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `26885ea1a6fd561551d04c6322ff15eb5ded1108580d17766f27224d4c36762d` |
| [outputs/informe/model2_lp_nota.md](../../outputs/informe/model2_lp_nota.md) | model2 lp nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `f59d4119c432716868b2ed35eeb3d4bb334d0c2dfe659766dc55cfb67bb85d1f` |
| [outputs/informe/model2_reading.md](../../outputs/informe/model2_reading.md) | Modelo II — lectura de resultados | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `dd36f8b7e1eb9d3221f41361b200888d2937387cdccd7c8972f6b8cf548c44d3` |
| [outputs/informe/model2_reading_anexo_1.md](../../outputs/informe/model2_reading_anexo_1.md) | Modelo II — lectura de resultados | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `913377e8d94941a950aeccf8eca803af007743812be400126c65e6b2c9f79157` |
| [outputs/informe/model2_reading_anexo_2.md](../../outputs/informe/model2_reading_anexo_2.md) | Modelo II — lectura de resultados | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `64e3b2197b490306fa167d3cbe80e3126bacb73260bd02260a710810f4a230fa` |
| [outputs/informe/model2_reading_cuerpo.md](../../outputs/informe/model2_reading_cuerpo.md) | model2 reading cuerpo | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `bf2f4b7c1626c11c5b925fb6ae374517fce87071c5c21af826389a5d0464982e` |
| [outputs/informe/model2_reading_cuerpo_combinado.md](../../outputs/informe/model2_reading_cuerpo_combinado.md) | model2 reading cuerpo combinado | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `972eeac46d531d11200c058149b2dbb734693876c2ee883394bae0d1d1b609c3` |
| [outputs/informe/model2_reading_nota.md](../../outputs/informe/model2_reading_nota.md) | model2 reading nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `a2c7065be6fc2e88065226c9f81610bc57b72d7f0a44f39af4ce0fd4d3f856b5` |
| [outputs/informe/model2_robustness_estimates.md](../../outputs/informe/model2_robustness_estimates.md) | Modelo II — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `2d94aa89f29f10cb1e303708ace384d216d6c006d89194dfcc005f591c4756f0` |
| [outputs/informe/model2_robustness_estimates_anexo_1.md](../../outputs/informe/model2_robustness_estimates_anexo_1.md) | Modelo II — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `c2046333d36b8d2b47a764dd4860ca578c3fd3f6222fc5a668c3db851940468e` |
| [outputs/informe/model2_robustness_estimates_anexo_2.md](../../outputs/informe/model2_robustness_estimates_anexo_2.md) | Modelo II — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `94b53912bd38c22c82e07969a7e75dcb96a1e0b8e0560ec9e6b303ef9f65168f` |
| [outputs/informe/model2_robustness_estimates_anexo_3.md](../../outputs/informe/model2_robustness_estimates_anexo_3.md) | Modelo II — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `238575fd6961090534b58666806ed670e80f11840daaf9645edb179550d31fba` |
| [outputs/informe/model2_robustness_estimates_anexo_4.md](../../outputs/informe/model2_robustness_estimates_anexo_4.md) | Modelo II — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `f5542bf9064faec2904516e4deb3037e3f1e658d43028ef676ea0f166171b5b0` |
| [outputs/informe/model2_robustness_estimates_anexo_5.md](../../outputs/informe/model2_robustness_estimates_anexo_5.md) | Modelo II — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `fba7cd623d27538463c9c65ef38d0fcd0df76836be8c95721f24d98d17c4807b` |
| [outputs/informe/model2_robustness_estimates_anexo_6.md](../../outputs/informe/model2_robustness_estimates_anexo_6.md) | Modelo II — estimaciones de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `a6463830ce327c9b2b99a5eaba473fb953c54a067b877679c4ff02dd1e72a672` |
| [outputs/informe/model2_robustness_summary.md](../../outputs/informe/model2_robustness_summary.md) | Modelo II — resumen de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `8b6bed0bf52902f3eb3ad64e5ca1710d37266eb957495685784f410fb0e1d4b2` |
| [outputs/informe/model2_robustness_summary_anexo_1.md](../../outputs/informe/model2_robustness_summary_anexo_1.md) | Modelo II — resumen de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `5c9690512b1c05d5e10c779d9c16dda8e0877ee1b6bc2ab8df1b0621a69a3159` |
| [outputs/informe/model2_robustness_summary_anexo_2.md](../../outputs/informe/model2_robustness_summary_anexo_2.md) | Modelo II — resumen de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `062d5b87b9033f5f6e6273a8bb4e2dd64ebf7e9d470be75515aeccc343385c0d` |
| [outputs/informe/model2_robustness_summary_anexo_3.md](../../outputs/informe/model2_robustness_summary_anexo_3.md) | Modelo II — resumen de robustez | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `ff52006c866c672b19f88f9c6ef67720a947cc22fafe97dcf73479c26f6c83b1` |
| [outputs/informe/model2_robustness_summary_nota.md](../../outputs/informe/model2_robustness_summary_nota.md) | model2 robustness summary nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `60b4f17ea5bbce6585347e9516814b1a51819cb63382842263a804a079d37f46` |
| [outputs/informe/model2_selection.md](../../outputs/informe/model2_selection.md) | Modelo II — selección de rezagos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `e3709a0bf102f3c20da97bab40ad0ebdbe7b3a19d34eef1f98202757ff0a59d9` |
| [outputs/informe/model2_selection_anexo_1.md](../../outputs/informe/model2_selection_anexo_1.md) | Modelo II — selección de rezagos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `33abbb636a7865b381702f2660e674d7c9c21eb9b45e8d000a69dfc7fbc2b950` |
| [outputs/informe/model2_selection_anexo_2.md](../../outputs/informe/model2_selection_anexo_2.md) | Modelo II — selección de rezagos | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `092e79fa2d10aa4ab9d3a2c2642a0408ae73865086311925a3247a0295b3f20f` |
| [outputs/informe/model2_selection_nota.md](../../outputs/informe/model2_selection_nota.md) | model2 selection nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `79165f1c373c9a191d05051806806c019d69ab0f3ca1f09b404c3c83536cf97a` |
| [outputs/informe/model2_stationarity.md](../../outputs/informe/model2_stationarity.md) | Modelo II — estacionariedad | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `d8e9b56919dfff3efa84751316bf5f2ef93009f8de48ccd5ef1e91e73553d172` |
| [outputs/informe/model2_stationarity_anexo_1.md](../../outputs/informe/model2_stationarity_anexo_1.md) | Modelo II — estacionariedad | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `1d50f80323c647fecb4adba971390e9c83c52afecf06e739748415a214c25bfa` |
| [outputs/informe/model2_stationarity_anexo_2.md](../../outputs/informe/model2_stationarity_anexo_2.md) | Modelo II — estacionariedad | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `afd99f1707c0ea4848a24288dc583bdcf8bba6a95f832ecb42f7e7fa7730bad2` |
| [outputs/informe/model2_stationarity_anexo_3.md](../../outputs/informe/model2_stationarity_anexo_3.md) | Modelo II — estacionariedad | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `a4d7794681d2f4d4fb818cac22d401216ee5c8f45d02a3419103b57f87938042` |
| [outputs/informe/model2_stationarity_anexo_4.md](../../outputs/informe/model2_stationarity_anexo_4.md) | Modelo II — estacionariedad | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `7540e7464b4af84682fce3c3c1f230fa1a655ef225a0fb40941e1dc08b5df26f` |
| [outputs/informe/model2_stationarity_nota.md](../../outputs/informe/model2_stationarity_nota.md) | model2 stationarity nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `42398172159bb9c0dd040c696ede823f8eea3749564f37e39eae526f9c141b45` |
| [outputs/informe/model2_trajectory.md](../../outputs/informe/model2_trajectory.md) | Modelo II — trayectoria | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `1371e7d5034b3d68bee5715a0dd54d61414f7bb82b5e2b3294f144c7f449ce0c` |
| [outputs/informe/model2_trajectory_anexo_1.md](../../outputs/informe/model2_trajectory_anexo_1.md) | Modelo II — trayectoria | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `1371e7d5034b3d68bee5715a0dd54d61414f7bb82b5e2b3294f144c7f449ce0c` |
| [outputs/informe/model2_trajectory_nota.md](../../outputs/informe/model2_trajectory_nota.md) | model2 trajectory nota | Derivado de presentación; `006-informe (derivada de 004-modelo-ii)` | `43077d4a4b57c2a93afd8cd9aaf3e409eb2d2452993d85133af58c0308313084` |
| [outputs/informe/registro.csv](../../outputs/informe/registro.csv) | registro | Derivado de presentación; `006-informe (derivada de 001-datos)` | `b021118956a97408126a7436b9e11aad91791f6370c84c06319209dcb21e7a28` |
| [outputs/informe/stationarity.md](../../outputs/informe/stationarity.md) | Estacionariedad de las series | Derivado de presentación; `006-informe (derivada de 001-datos)` | `c6e5ec6452d4c34897d3a1674cd6b47a90e07e538b4a6bc2d72295dfa4cd1f31` |
| [outputs/informe/stationarity_anexo_1.md](../../outputs/informe/stationarity_anexo_1.md) | Estacionariedad de las series | Derivado de presentación; `006-informe (derivada de 001-datos)` | `848c070e82a40edd94466109e86309c57a776c58fa2d5ea617264fc8de39da2b` |
| [outputs/informe/stationarity_anexo_2.md](../../outputs/informe/stationarity_anexo_2.md) | Estacionariedad de las series | Derivado de presentación; `006-informe (derivada de 001-datos)` | `671d6576237dcee8606c68bb3d28d75942346b33d84ba175afbd439311caa654` |
| [outputs/informe/stationarity_anexo_3.md](../../outputs/informe/stationarity_anexo_3.md) | Estacionariedad de las series | Derivado de presentación; `006-informe (derivada de 001-datos)` | `1b605888a4d582192805ed3d583dc1489cc3dc5a9f8cefd70e1cc3c86a615d4e` |
| [outputs/informe/stationarity_anexo_4.md](../../outputs/informe/stationarity_anexo_4.md) | Estacionariedad de las series | Derivado de presentación; `006-informe (derivada de 001-datos)` | `1cc8d731fc583946603bd57ab0a4c4234f1e757ed29e98fa51926f1397a0cb8c` |
| [outputs/informe/stress_delta.md](../../outputs/informe/stress_delta.md) | Estrés — cambios adverso menos base | Derivado de presentación; `006-informe (derivada de 005-estres)` | `a41159ff07cc41770f103e50228c3da2b23d294fea48d1d98f6d2b4a3ea8c175` |
| [outputs/informe/stress_delta_anexo_1.md](../../outputs/informe/stress_delta_anexo_1.md) | Estrés — cambios adverso menos base | Derivado de presentación; `006-informe (derivada de 005-estres)` | `fd91316c607c2daff8ddbe477ac40753f7d4016d8333915e9c4ff26ba7e0aacf` |
| [outputs/informe/stress_delta_anexo_2.md](../../outputs/informe/stress_delta_anexo_2.md) | Estrés — cambios adverso menos base | Derivado de presentación; `006-informe (derivada de 005-estres)` | `71d697a786d6c648143ae62d5cf379dd7ed487ef2f45d4079e0494afd5347523` |
| [outputs/informe/stress_delta_anexo_3.md](../../outputs/informe/stress_delta_anexo_3.md) | Estrés — cambios adverso menos base | Derivado de presentación; `006-informe (derivada de 005-estres)` | `378235e212533f9bd71c7afd2de157a92191756fa5aa1e72fd079376ea8f53f0` |
| [outputs/informe/stress_delta_anexo_4.md](../../outputs/informe/stress_delta_anexo_4.md) | Estrés — cambios adverso menos base | Derivado de presentación; `006-informe (derivada de 005-estres)` | `2935659937040f52f5554a29e30fa939f14118ba58c109d96dd92834694293dd` |
| [outputs/informe/stress_delta_anexo_5.md](../../outputs/informe/stress_delta_anexo_5.md) | Estrés — cambios adverso menos base | Derivado de presentación; `006-informe (derivada de 005-estres)` | `74541fac1ab44b744b1001b2c463c020206e6797634b37c4b153d51d96a31aeb` |
| [outputs/informe/stress_delta_anexo_6.md](../../outputs/informe/stress_delta_anexo_6.md) | Estrés — cambios adverso menos base | Derivado de presentación; `006-informe (derivada de 005-estres)` | `703252a66d281d7df87a4cfb61223bffec9b60bb931df0ffcf3948cb5608c51f` |
| [outputs/informe/stress_delta_anexo_7.md](../../outputs/informe/stress_delta_anexo_7.md) | Estrés — cambios adverso menos base | Derivado de presentación; `006-informe (derivada de 005-estres)` | `e2e3a6c23103cf4e8ad4969c6ecf4a516d379695138176d67eb4a19960abb4bb` |
| [outputs/informe/stress_delta_cuerpo.md](../../outputs/informe/stress_delta_cuerpo.md) | stress delta cuerpo | Derivado de presentación; `006-informe (derivada de 005-estres)` | `fdc603fe1e12755eb32c090f551dcfa8534fc1ff78bc8482fc58b15a618bb68b` |
| [outputs/informe/stress_delta_cuerpo_combinado.md](../../outputs/informe/stress_delta_cuerpo_combinado.md) | stress delta cuerpo combinado | Derivado de presentación; `006-informe (derivada de 005-estres)` | `16849e7052b8890432bd8946cfe99128bfc67501b27bd3af2f3285406c37855d` |
| [outputs/informe/stress_delta_nota.md](../../outputs/informe/stress_delta_nota.md) | stress delta nota | Derivado de presentación; `006-informe (derivada de 005-estres)` | `733d7017c257017157a4644ced7b4069c8b3559cbeb7ce65886caf36caa8c935` |
| [outputs/informe/stress_levels.md](../../outputs/informe/stress_levels.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `fa019f52f1c1c1dba4e23ed368c5ae2b605170f5be8d51828a788ac2ff06be4f` |
| [outputs/informe/stress_levels_anexo_1.md](../../outputs/informe/stress_levels_anexo_1.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `a164a21abcb85e870cf997981c37d4bae203e6646e7eed46d0b9583c237e770d` |
| [outputs/informe/stress_levels_anexo_2.md](../../outputs/informe/stress_levels_anexo_2.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `793781ad30cfafe26e29468dae945c5baaa29e7ac925d6f70261e75574dbfe71` |
| [outputs/informe/stress_levels_anexo_3.md](../../outputs/informe/stress_levels_anexo_3.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `f3d289404bd67888806e7781ea383806a6f58057e1fbcfb6b321e77dd68c076c` |
| [outputs/informe/stress_levels_anexo_4.md](../../outputs/informe/stress_levels_anexo_4.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `3828f56e290aa2ca17f40e088e52e652220eac90f8ffb5495ff46635d69225a0` |
| [outputs/informe/stress_levels_anexo_5.md](../../outputs/informe/stress_levels_anexo_5.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `96438955a17e877449c3d3e4e523a07035df8de715bd0413ebd1c5b22202f6a3` |
| [outputs/informe/stress_levels_anexo_6.md](../../outputs/informe/stress_levels_anexo_6.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `daef52a87c1b2ee61ab710a0b52a141c90424eb2fb3abd668069bee00046af79` |
| [outputs/informe/stress_levels_anexo_7.md](../../outputs/informe/stress_levels_anexo_7.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `80f69f0c7e4573f5bdd5dbb3167ccabd08e0f6723d2d24273f77c9125ad18a26` |
| [outputs/informe/stress_levels_anexo_8.md](../../outputs/informe/stress_levels_anexo_8.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `8896eb3f3510bbf82be826b2cae2869315603446a3d9694cb9ec8e49535e4ab1` |
| [outputs/informe/stress_levels_anexo_9.md](../../outputs/informe/stress_levels_anexo_9.md) | Estrés — niveles de morosidad | Derivado de presentación; `006-informe (derivada de 005-estres)` | `eb8cef9bee475fe08dafc9f0d7d47a31a5cba9e8b1e859c00957fb36a079c056` |
| [outputs/informe/stress_levels_nota.md](../../outputs/informe/stress_levels_nota.md) | stress levels nota | Derivado de presentación; `006-informe (derivada de 005-estres)` | `733d7017c257017157a4644ced7b4069c8b3559cbeb7ce65886caf36caa8c935` |
| [outputs/informe/stress_limitations.md](../../outputs/informe/stress_limitations.md) | Estrés — limitaciones | Derivado de presentación; `006-informe (derivada de 005-estres)` | `bf51389d853d5497cc51ef1eb7557dcb76f555bfa2504ea960e30124575a5fe2` |
| [outputs/informe/stress_limitations_anexo_1.md](../../outputs/informe/stress_limitations_anexo_1.md) | Estrés — limitaciones | Derivado de presentación; `006-informe (derivada de 005-estres)` | `bf51389d853d5497cc51ef1eb7557dcb76f555bfa2504ea960e30124575a5fe2` |
| [outputs/informe/stress_limitations_nota.md](../../outputs/informe/stress_limitations_nota.md) | stress limitations nota | Derivado de presentación; `006-informe (derivada de 005-estres)` | `47341c68a95dc808beefbb49b4b138f3703262d02e383ec11fff593e553dce6f` |
| [outputs/informe/stress_model1_presentacion.png](../../outputs/informe/stress_model1_presentacion.png) | stress model1 presentacion | Figura PNG; `006-informe (derivada de 005-estres)` | `02f32d2f89b23174249d35f113fec31d780323154f38b0097d7ff7bd2fbce46d` |
| [outputs/informe/stress_model2_presentacion.png](../../outputs/informe/stress_model2_presentacion.png) | stress model2 presentacion | Figura PNG; `006-informe (derivada de 005-estres)` | `f7a6b9bef7f91ec38705f2ce67c36146fbb69fd77cd1778d6f5a58ac8902bf6c` |
| [outputs/informe/stress_models.md](../../outputs/informe/stress_models.md) | Estrés — comparación entre modelos | Derivado de presentación; `006-informe (derivada de 005-estres)` | `22976ff235fdbd3d2dd4ad7952013b547ee832aac212ece04b64cee551ed6d58` |
| [outputs/informe/stress_models_anexo_1.md](../../outputs/informe/stress_models_anexo_1.md) | Estrés — comparación entre modelos | Derivado de presentación; `006-informe (derivada de 005-estres)` | `22976ff235fdbd3d2dd4ad7952013b547ee832aac212ece04b64cee551ed6d58` |
| [outputs/informe/stress_models_anexo_2.md](../../outputs/informe/stress_models_anexo_2.md) | Estrés — comparación entre modelos | Derivado de presentación; `006-informe (derivada de 005-estres)` | `de5785e7d8dbd3c41d4a2af684935f0e26b0c28c4698eed85531657a363f2e52` |
| [outputs/informe/stress_models_nota.md](../../outputs/informe/stress_models_nota.md) | stress models nota | Derivado de presentación; `006-informe (derivada de 005-estres)` | `2f46c3bf88bd51e240f496244e6900e3adb1785c36f811840a4231962e903172` |
| [outputs/informe/stress_origin.md](../../outputs/informe/stress_origin.md) | Estrés — variante de origen | Derivado de presentación; `006-informe (derivada de 005-estres)` | `39335bef303f6cd608c4b599fbcb3a12114bcf352d8406a104774e1c69760f07` |
| [outputs/informe/stress_origin_anexo_1.md](../../outputs/informe/stress_origin_anexo_1.md) | Estrés — variante de origen | Derivado de presentación; `006-informe (derivada de 005-estres)` | `4c956f7b2b6e8904ce2f4b475252228c97c5b28e2a02bc67c27ffb2515c70105` |
| [outputs/informe/stress_origin_anexo_2.md](../../outputs/informe/stress_origin_anexo_2.md) | Estrés — variante de origen | Derivado de presentación; `006-informe (derivada de 005-estres)` | `39335bef303f6cd608c4b599fbcb3a12114bcf352d8406a104774e1c69760f07` |
| [outputs/informe/stress_origin_anexo_3.md](../../outputs/informe/stress_origin_anexo_3.md) | Estrés — variante de origen | Derivado de presentación; `006-informe (derivada de 005-estres)` | `605a04f9b950ae1a0b85f982ff1f1bc5b38d10b31da7d25b61483231b73e860f` |
| [outputs/informe/stress_origin_anexo_4.md](../../outputs/informe/stress_origin_anexo_4.md) | Estrés — variante de origen | Derivado de presentación; `006-informe (derivada de 005-estres)` | `a4885eb29ebd907f44d3478661beaf415b9a8a0e89c32adfc8819fa19ecea4bd` |
| [outputs/informe/stress_origin_nota.md](../../outputs/informe/stress_origin_nota.md) | stress origin nota | Derivado de presentación; `006-informe (derivada de 005-estres)` | `496b3529a719987cafeff8ccdeebc14b2b56e2e5a52658868277e1613e6899aa` |
| [outputs/informe/stress_paths.md](../../outputs/informe/stress_paths.md) | Estrés — trayectorias de regresores | Derivado de presentación; `006-informe (derivada de 005-estres)` | `bb74fcb4d955a04186be8a04f768c4038faf054f9d02a4bc4b994f0532bd42d4` |
| [outputs/informe/stress_paths_anexo_1.md](../../outputs/informe/stress_paths_anexo_1.md) | Estrés — trayectorias de regresores | Derivado de presentación; `006-informe (derivada de 005-estres)` | `f1e9df9dbe5a2de1600cf1fb6f80e3b41544e278fc47c8e17d2c5aec7ba13934` |
| [outputs/informe/stress_paths_anexo_2.md](../../outputs/informe/stress_paths_anexo_2.md) | Estrés — trayectorias de regresores | Derivado de presentación; `006-informe (derivada de 005-estres)` | `5b74342364f44c72bf223cf81e9226f747a2b57cf037fcf75892287add6e85c1` |
| [outputs/informe/stress_paths_anexo_3.md](../../outputs/informe/stress_paths_anexo_3.md) | Estrés — trayectorias de regresores | Derivado de presentación; `006-informe (derivada de 005-estres)` | `8b65e9f3040b071999f48eb59581dd6af37b1dc099a476edf8fa4c25b707402f` |
| [outputs/informe/stress_paths_anexo_4.md](../../outputs/informe/stress_paths_anexo_4.md) | Estrés — trayectorias de regresores | Derivado de presentación; `006-informe (derivada de 005-estres)` | `0c4293f96c41af1c8e886b998e5bedaecafc143f2126182bddf4cb5364f27193` |
| [outputs/informe/stress_paths_anexo_5.md](../../outputs/informe/stress_paths_anexo_5.md) | Estrés — trayectorias de regresores | Derivado de presentación; `006-informe (derivada de 005-estres)` | `a4c36a90f8cdbc642d91c0def0f78ef790e699fe6d0f617f80167d1a3334efde` |
| [outputs/informe/stress_paths_nota.md](../../outputs/informe/stress_paths_nota.md) | stress paths nota | Derivado de presentación; `006-informe (derivada de 005-estres)` | `47341c68a95dc808beefbb49b4b138f3703262d02e383ec11fff593e553dce6f` |
| [outputs/informe/stress_rate_sensitivity.md](../../outputs/informe/stress_rate_sensitivity.md) | Estrés — sensibilidad de tasa | Derivado de presentación; `006-informe (derivada de 005-estres)` | `6341bf8438e8b692c672d2115bbdafbe4f9d563b6cd82e7b4b63af2e54bd1055` |
| [outputs/informe/stress_rate_sensitivity_anexo_1.md](../../outputs/informe/stress_rate_sensitivity_anexo_1.md) | Estrés — sensibilidad de tasa | Derivado de presentación; `006-informe (derivada de 005-estres)` | `f14428ce3d50fc985ddf3b30886feeb7a08eaf2bcace245e4a8a6d62550d8942` |
| [outputs/informe/stress_rate_sensitivity_anexo_2.md](../../outputs/informe/stress_rate_sensitivity_anexo_2.md) | Estrés — sensibilidad de tasa | Derivado de presentación; `006-informe (derivada de 005-estres)` | `5b5c98880fda5259f48b05355abdb452cd989331d2812591f45c561b4898ace1` |
| [outputs/informe/stress_rate_sensitivity_anexo_3.md](../../outputs/informe/stress_rate_sensitivity_anexo_3.md) | Estrés — sensibilidad de tasa | Derivado de presentación; `006-informe (derivada de 005-estres)` | `653a9ee2067281b5b1101c9c807b7f40150588b06ee5c50527ec26ecf4735ffc` |
| [outputs/informe/stress_rate_sensitivity_anexo_4.md](../../outputs/informe/stress_rate_sensitivity_anexo_4.md) | Estrés — sensibilidad de tasa | Derivado de presentación; `006-informe (derivada de 005-estres)` | `7507fb10b2e2ce13554e84bfe9a0f77a9bccb567f7a40824f11970df8ff1bb17` |
| [outputs/informe/stress_rate_sensitivity_anexo_5.md](../../outputs/informe/stress_rate_sensitivity_anexo_5.md) | Estrés — sensibilidad de tasa | Derivado de presentación; `006-informe (derivada de 005-estres)` | `20132690e2c2ad3143d05d77cd1dd9c0794ec3acac22c4f575a097626b9edd70` |
| [outputs/informe/stress_rate_sensitivity_anexo_6.md](../../outputs/informe/stress_rate_sensitivity_anexo_6.md) | Estrés — sensibilidad de tasa | Derivado de presentación; `006-informe (derivada de 005-estres)` | `974dd61f1614806d8d25bf415c6657fb55945e5347d8cc35d8d276637be0585e` |
| [outputs/informe/stress_rate_sensitivity_anexo_7.md](../../outputs/informe/stress_rate_sensitivity_anexo_7.md) | Estrés — sensibilidad de tasa | Derivado de presentación; `006-informe (derivada de 005-estres)` | `31efc0a2eeada4dcba591c6c352ed66c64e1d342d48db5899c688ddbe5874bfd` |
| [outputs/informe/stress_rate_sensitivity_nota.md](../../outputs/informe/stress_rate_sensitivity_nota.md) | stress rate sensitivity nota | Derivado de presentación; `006-informe (derivada de 005-estres)` | `faa14c1d7fa46a00e57c2b021ff3bbbca55dfb9602eee3bfc26b1d2a7c002e04` |
| [outputs/informe/stress_sensitivity.md](../../outputs/informe/stress_sensitivity.md) | Estrés — otras sensibilidades | Derivado de presentación; `006-informe (derivada de 005-estres)` | `2715d80bc9da41fd87403ebf93a295ecde4ee17fce98f26efcd600cbf3c89555` |
| [outputs/informe/stress_sensitivity_anexo_1.md](../../outputs/informe/stress_sensitivity_anexo_1.md) | Estrés — otras sensibilidades | Derivado de presentación; `006-informe (derivada de 005-estres)` | `25574ee330a7fefe7d75a17cfe40d3be78d21731866a349a5e04cd527c3ef0ec` |
| [outputs/informe/stress_sensitivity_anexo_2.md](../../outputs/informe/stress_sensitivity_anexo_2.md) | Estrés — otras sensibilidades | Derivado de presentación; `006-informe (derivada de 005-estres)` | `0838429f176c517fd93349e254ea50dbd34a2aac5d8e53472a79f8f42d636b1b` |
| [outputs/informe/stress_sensitivity_anexo_3.md](../../outputs/informe/stress_sensitivity_anexo_3.md) | Estrés — otras sensibilidades | Derivado de presentación; `006-informe (derivada de 005-estres)` | `b121f27efa1b3c46e758d1477f6b29828f949f1d80ba3f27fe6f30eea56d2570` |
| [outputs/informe/stress_sensitivity_anexo_4.md](../../outputs/informe/stress_sensitivity_anexo_4.md) | Estrés — otras sensibilidades | Derivado de presentación; `006-informe (derivada de 005-estres)` | `8334ed13473bd88d65a1a04ce17bfad4cf7be8943995fb23aa56b28623b50a1a` |
| [outputs/informe/stress_sensitivity_anexo_5.md](../../outputs/informe/stress_sensitivity_anexo_5.md) | Estrés — otras sensibilidades | Derivado de presentación; `006-informe (derivada de 005-estres)` | `c9e6a75c28e9748152ec38baae74404909957ede592e774fe71dca920f9f8891` |
| [outputs/informe/stress_sensitivity_nota.md](../../outputs/informe/stress_sensitivity_nota.md) | stress sensitivity nota | Derivado de presentación; `006-informe (derivada de 005-estres)` | `47341c68a95dc808beefbb49b4b138f3703262d02e383ec11fff593e553dce6f` |
| [outputs/informe/trace.json](../../outputs/informe/trace.json) | Matriz CSV → presentación → anexo | Derivado de presentación; `006-informe` | `545bf521bbc6d91fdcc6ed2b955000e438b125006505782389f06146e22a816e` |
| [outputs/tables/descriptives.csv](../../outputs/tables/descriptives.csv) | Estadísticos descriptivos | Fuente aprobada; `001-datos` | `f5e78fb0df3323c1831b6c6c4f0d2d8acd7288435115c5ad41fe62280a07ae93` |
| [outputs/tables/descriptives.md](../../outputs/tables/descriptives.md) | Estadísticos descriptivos | Fuente aprobada; `001-datos` | `f576b03df8e81f3a906e3e1b81a9bb6974b347b500b07c53649339c22e7d98f8` |
| [outputs/tables/lit_estudios.csv](../../outputs/tables/lit_estudios.csv) | Estudios verificados: variables, métodos y signos | Fuente aprobada; `006-informe desde 002-literatura` | `686a17b8dd58df7bbc000a5ac13343f9811d644f9f7c3d7c219b797d1807a72a` |
| [outputs/tables/lit_estudios.md](../../outputs/tables/lit_estudios.md) | Estudios verificados: variables, métodos y signos | Fuente aprobada; `006-informe desde 002-literatura` | `8a000eacb4f398a72352d3d869972760cb5ae405d37e281e64b3afa280c97089` |
| [outputs/tables/model1_coefficients.csv](../../outputs/tables/model1_coefficients.csv) | Modelo I — coeficientes | Fuente aprobada; `003-modelo-i` | `ea583f9ff75fd1522a26ccbcc757048cbeadb1e819c22ec999c9728ef7bf5bc0` |
| [outputs/tables/model1_coefficients.md](../../outputs/tables/model1_coefficients.md) | Modelo I — coeficientes | Fuente aprobada; `003-modelo-i` | `fbdf0dbd4dc0daef2be4efe4710720619e3a680c6ad6325316e63cc6066ee8f4` |
| [outputs/tables/model1_deviations.csv](../../outputs/tables/model1_deviations.csv) | Modelo I — desviaciones | Fuente aprobada; `003-modelo-i` | `94393319ebc35ccf84bf4efabc8d93f4ccb9684edc02be5379a83fb86ef7df62` |
| [outputs/tables/model1_deviations.md](../../outputs/tables/model1_deviations.md) | Modelo I — desviaciones | Fuente aprobada; `003-modelo-i` | `7ae2ff49d81493034b893787ba2e392dc7a7e6738a8e0c53ac47938204540320` |
| [outputs/tables/model1_diagnostics.csv](../../outputs/tables/model1_diagnostics.csv) | Modelo I — diagnósticos | Fuente aprobada; `003-modelo-i` | `fecb3a626a58d137e0fbc3dcac2499e6671441bd3e30f8966afb8003666f7050` |
| [outputs/tables/model1_diagnostics.md](../../outputs/tables/model1_diagnostics.md) | Modelo I — diagnósticos | Fuente aprobada; `003-modelo-i` | `136ebf473159afe8296d59faf1ebb2b62f8324b324f4be5327ca0606b4c1c068` |
| [outputs/tables/model1_effects.csv](../../outputs/tables/model1_effects.csv) | Modelo I — efectos; unidades explícitas del CSV: pp de morosidad por 1 DE del regresor; pp de morosidad por 1 pp del regresor | Fuente aprobada; `003-modelo-i` | `1d32ebf8e6adf7e3f207b7980a0ade0eb885f67467ff30ddb777c6045b5267fc` |
| [outputs/tables/model1_effects.md](../../outputs/tables/model1_effects.md) | Modelo I — efectos | Fuente aprobada; `003-modelo-i` | `493beac5457882988a3fc55a5354486a7e51a67ab358b594833073185b39bb46` |
| [outputs/tables/model1_limitations.csv](../../outputs/tables/model1_limitations.csv) | Modelo I — limitaciones | Fuente aprobada; `003-modelo-i` | `d4a25207ee03d4e3b0f8b34518642ffba39c479d30d523a4593742afd67bcbff` |
| [outputs/tables/model1_limitations.md](../../outputs/tables/model1_limitations.md) | Modelo I — limitaciones | Fuente aprobada; `003-modelo-i` | `de234a1db64026b0594a09b65345b1d1e9fffe0b95b2d2605b308d8d94b937ed` |
| [outputs/tables/model1_oos.csv](../../outputs/tables/model1_oos.csv) | Modelo I — evaluación fuera de muestra | Fuente aprobada; `003-modelo-i` | `213d395bdcfe692b8335b4031cd7116e8d9c215eb49c7ce0c6dedf57e7894fad` |
| [outputs/tables/model1_oos.md](../../outputs/tables/model1_oos.md) | Modelo I — evaluación fuera de muestra | Fuente aprobada; `003-modelo-i` | `90c978fcb782b421880922081ea057d568dd2c84503c3aea501ad36b0dbba473` |
| [outputs/tables/model1_robustness_estimates.csv](../../outputs/tables/model1_robustness_estimates.csv) | Modelo I — estimaciones de robustez | Fuente aprobada; `003-modelo-i` | `c5bd503ada497dbb2d94542fa2b4785195a6e2a155449ab93239ef84e191f6af` |
| [outputs/tables/model1_robustness_estimates.md](../../outputs/tables/model1_robustness_estimates.md) | Modelo I — estimaciones de robustez | Fuente aprobada; `003-modelo-i` | `8b0f680842433321f47d2b2219b594fe19f7e9413aee88debb8563522eb906e5` |
| [outputs/tables/model1_robustness_summary.csv](../../outputs/tables/model1_robustness_summary.csv) | Modelo I — resumen de robustez | Fuente aprobada; `003-modelo-i` | `ede8e183a7e0f735796329d3b9a5385ec8ff79723020b4f1d300241f1f196973` |
| [outputs/tables/model1_robustness_summary.md](../../outputs/tables/model1_robustness_summary.md) | Modelo I — resumen de robustez | Fuente aprobada; `003-modelo-i` | `43d8a161615415714bc13f0036faf328cc1f96fbf4e3eb250179da198d8d1f68` |
| [outputs/tables/model1_stationarity.csv](../../outputs/tables/model1_stationarity.csv) | Modelo I — estacionariedad | Fuente aprobada; `003-modelo-i` | `f82782554661978ca576060b75a2cd4962c6654c0fefb25a9868bacb33c49450` |
| [outputs/tables/model1_stationarity.md](../../outputs/tables/model1_stationarity.md) | Modelo I — estacionariedad | Fuente aprobada; `003-modelo-i` | `b4a4474659b309867ef8ebd6aaec8eee42a40f78eb962e996c92ece3241dff57` |
| [outputs/tables/model2_coefficients.csv](../../outputs/tables/model2_coefficients.csv) | Modelo II — coeficientes | Fuente aprobada; `004-modelo-ii` | `ce2c270a319c6e6e52b819ff5b4ef30ee9effb4afe2bc48a5c07df18743bb417` |
| [outputs/tables/model2_coefficients.md](../../outputs/tables/model2_coefficients.md) | Modelo II — coeficientes | Fuente aprobada; `004-modelo-ii` | `5aea117170284b6c48df57e7efdd406a3037964c846c6cd2ae9c0f29914835ca` |
| [outputs/tables/model2_comparison.csv](../../outputs/tables/model2_comparison.csv) | Modelo II — comparación dinámica | Fuente aprobada; `004-modelo-ii` | `c3b27279fbb7cbe8225e248daab88e788956a0b0c8382992ea47a99b11fdddd9` |
| [outputs/tables/model2_comparison.md](../../outputs/tables/model2_comparison.md) | Modelo II — comparación dinámica | Fuente aprobada; `004-modelo-ii` | `c82ca4d619b00807acc6de5d6c1bbe6b9f6205132a4ed33ea74cf953f740f564` |
| [outputs/tables/model2_deviations.csv](../../outputs/tables/model2_deviations.csv) | Modelo II — desviaciones | Fuente aprobada; `004-modelo-ii` | `d062336550df1da7685475ed0d7141a0939f1d3b4fe7c47c5d28d0f389c0c98e` |
| [outputs/tables/model2_deviations.md](../../outputs/tables/model2_deviations.md) | Modelo II — desviaciones | Fuente aprobada; `004-modelo-ii` | `9a4c9b6ba52667c949c29574c21e4ca5a15830aeeaa37801897c859f053ba782` |
| [outputs/tables/model2_diagnostics.csv](../../outputs/tables/model2_diagnostics.csv) | Modelo II — diagnósticos | Fuente aprobada; `004-modelo-ii` | `8161402a4412d908c6c6c8b1b0c76b082102427bc7a5eb212729067239675389` |
| [outputs/tables/model2_diagnostics.md](../../outputs/tables/model2_diagnostics.md) | Modelo II — diagnósticos | Fuente aprobada; `004-modelo-ii` | `eac1e4e0f7b9b6a862ae7bc29333e156896523136ce9a88abe20ac6625baf8dc` |
| [outputs/tables/model2_effects.csv](../../outputs/tables/model2_effects.csv) | Modelo II — efectos | Fuente aprobada; `004-modelo-ii` | `7a28092946df9353926e6575c325a7fd6d07e404b5a90ebac0153ebba5cd416d` |
| [outputs/tables/model2_effects.md](../../outputs/tables/model2_effects.md) | Modelo II — efectos | Fuente aprobada; `004-modelo-ii` | `4e29dcc7758a7d7ce4202ddd9bb0463d106248b707f8717c914a67b915411682` |
| [outputs/tables/model2_inputs63.csv](../../outputs/tables/model2_inputs63.csv) | Insumos de comparación de modelos | Fuente aprobada; `004-modelo-ii` | `712ff6fda631e87ea06de96a1e9f17fac0b63711280dca6e5e78d75801da7e00` |
| [outputs/tables/model2_inputs63.md](../../outputs/tables/model2_inputs63.md) | Insumos de comparación de modelos | Fuente aprobada; `004-modelo-ii` | `069d719521d0b36818e00276e274e12d7b99378d562c1692b6bcd5cc416c13ef` |
| [outputs/tables/model2_limitations.csv](../../outputs/tables/model2_limitations.csv) | Modelo II — limitaciones | Fuente aprobada; `004-modelo-ii` | `8e5a407e80a41b6dd0f1b3d8b75e0043b2dfc7ddb22c3375507dd1d23ab03cfe` |
| [outputs/tables/model2_limitations.md](../../outputs/tables/model2_limitations.md) | Modelo II — limitaciones | Fuente aprobada; `004-modelo-ii` | `e26f0da16f88b234ed93207abcd7e3cdec6b3e46a8b820434a068b481a675e33` |
| [outputs/tables/model2_lp.csv](../../outputs/tables/model2_lp.csv) | Modelo II — proyecciones locales | Fuente aprobada; `004-modelo-ii` | `06aa15f41feea77c296f57a493d284b2026ddac521f28232d38a10fa71678220` |
| [outputs/tables/model2_lp.md](../../outputs/tables/model2_lp.md) | Modelo II — proyecciones locales | Fuente aprobada; `004-modelo-ii` | `2a17749d9cef2ea4fd01d4438ae186a4dd6745ecfb5393d7427f7245ab54f696` |
| [outputs/tables/model2_reading.csv](../../outputs/tables/model2_reading.csv) | Modelo II — lectura de resultados | Fuente aprobada; `004-modelo-ii` | `98eb053c6b33b8ccfabdfa3d10e7078b1003f5645374a1bd63a6bba43099c765` |
| [outputs/tables/model2_reading.md](../../outputs/tables/model2_reading.md) | Modelo II — lectura de resultados | Fuente aprobada; `004-modelo-ii` | `4a331d79962dd14629903a5ae8d795d072bfdf0adc022e1e9ddbcd3e2456e16f` |
| [outputs/tables/model2_robustness_estimates.csv](../../outputs/tables/model2_robustness_estimates.csv) | Modelo II — estimaciones de robustez | Fuente aprobada; `004-modelo-ii` | `1a97e832b05b014ac179ac6381a45da5b794fc81b19d17e656fb10c58f949cd3` |
| [outputs/tables/model2_robustness_estimates.md](../../outputs/tables/model2_robustness_estimates.md) | Modelo II — estimaciones de robustez | Fuente aprobada; `004-modelo-ii` | `fc1985ad7ae1bdee1cdba9506d2ba42e8aaff36700c4434aff09fd89b6bf18b3` |
| [outputs/tables/model2_robustness_summary.csv](../../outputs/tables/model2_robustness_summary.csv) | Modelo II — resumen de robustez | Fuente aprobada; `004-modelo-ii` | `b57dee851b04415004f7d1b5772c9fd4d871e283b0cd7cb435591664042338ce` |
| [outputs/tables/model2_robustness_summary.md](../../outputs/tables/model2_robustness_summary.md) | Modelo II — resumen de robustez | Fuente aprobada; `004-modelo-ii` | `ff6a412b9cec111bd1637a1963ecb0c9d0e5a6e52b48ca2d5b621f1c3d2e1c2e` |
| [outputs/tables/model2_selection.csv](../../outputs/tables/model2_selection.csv) | Modelo II — selección de rezagos | Fuente aprobada; `004-modelo-ii` | `4041482baea88866705062ea104393948ee2bd2ea5bd464eb0a6e49afa5797e8` |
| [outputs/tables/model2_selection.md](../../outputs/tables/model2_selection.md) | Modelo II — selección de rezagos | Fuente aprobada; `004-modelo-ii` | `b1f385552d48098b2d245e12fe1d5d78808fd77d9d7c1e52faff50816d760318` |
| [outputs/tables/model2_stationarity.csv](../../outputs/tables/model2_stationarity.csv) | Modelo II — estacionariedad | Fuente aprobada; `004-modelo-ii` | `de19844e64e8fb1cbdb536f04b146c3695a5c6319336a9833ffae57454a1c813` |
| [outputs/tables/model2_stationarity.md](../../outputs/tables/model2_stationarity.md) | Modelo II — estacionariedad | Fuente aprobada; `004-modelo-ii` | `e151f1d66186a22aaf92f694ae46850f309a81dfacc7ca4377b67fe7c34279ae` |
| [outputs/tables/model2_trajectory.csv](../../outputs/tables/model2_trajectory.csv) | Modelo II — trayectoria | Fuente aprobada; `004-modelo-ii` | `d8b8f011c46ec0f903e32e70c468f4b20cea79933e3f17a0dc7c68024a0d6b7a` |
| [outputs/tables/model2_trajectory.md](../../outputs/tables/model2_trajectory.md) | Modelo II — trayectoria | Fuente aprobada; `004-modelo-ii` | `63f89f6acc34cca1096bc73b625e85733e4a74f5c2f74ae5501574417836ae02` |
| [outputs/tables/stationarity.csv](../../outputs/tables/stationarity.csv) | Estacionariedad de las series | Fuente aprobada; `001-datos` | `03fcb7615ffce8d26ecb881cf16968976541626419e1aa19a3b97f8902010c9d` |
| [outputs/tables/stationarity.md](../../outputs/tables/stationarity.md) | Estacionariedad de las series | Fuente aprobada; `001-datos` | `43714be09be135c50b4a223d7e3ce413be9c737161bf732366cf8e3d2416dba8` |
| [outputs/tables/stress_delta.csv](../../outputs/tables/stress_delta.csv) | Estrés — cambios adverso menos base | Fuente aprobada; `005-estres` | `b91b7d21853f58d8cb0556c8c1a9a1f554d076f57c53aacbb8c8f8feb2a09a64` |
| [outputs/tables/stress_delta.md](../../outputs/tables/stress_delta.md) | Estrés — cambios adverso menos base | Fuente aprobada; `005-estres` | `5eb869064970fe3d110c0b4e02aae65d069a0fdc7bcbad535db6cb8bb7f2f4ce` |
| [outputs/tables/stress_levels.csv](../../outputs/tables/stress_levels.csv) | Estrés — niveles de morosidad | Fuente aprobada; `005-estres` | `d75ece9c92eddc895ff69dc132490543d8599eae799875d0ee7a6a0462253117` |
| [outputs/tables/stress_levels.md](../../outputs/tables/stress_levels.md) | Estrés — niveles de morosidad | Fuente aprobada; `005-estres` | `fda1b19d244cdb8b41cdb7ce3191b32d14c2a9394f8f67c717045c16ed23616a` |
| [outputs/tables/stress_limitations.csv](../../outputs/tables/stress_limitations.csv) | Estrés — limitaciones | Fuente aprobada; `005-estres` | `6e6221b237c1bb524f686a39ae45eac6b2e3cc942c26ded43e4687239a9865ab` |
| [outputs/tables/stress_limitations.md](../../outputs/tables/stress_limitations.md) | Estrés — limitaciones | Fuente aprobada; `005-estres` | `9ef5fb11c5b0a9f0db92b19505ba17df244b3d61bc63a0380ec69b549bc4bd69` |
| [outputs/tables/stress_models.csv](../../outputs/tables/stress_models.csv) | Estrés — comparación entre modelos | Fuente aprobada; `005-estres` | `da4ad74d6836f6bf4e53f45f02c1e6479b558b84482ed19e1e7c1ad6017cde6d` |
| [outputs/tables/stress_models.md](../../outputs/tables/stress_models.md) | Estrés — comparación entre modelos | Fuente aprobada; `005-estres` | `67676af25368bf99400e78692039a4f9cd71d48e40def9eb6c6ed37a8d695af4` |
| [outputs/tables/stress_origin.csv](../../outputs/tables/stress_origin.csv) | Estrés — variante de origen | Fuente aprobada; `005-estres` | `3218dd346d879542be4169125b0a62c11887c4e7376530b06c28e3aaabe50a27` |
| [outputs/tables/stress_origin.md](../../outputs/tables/stress_origin.md) | Estrés — variante de origen | Fuente aprobada; `005-estres` | `8712b32d7f616840f8522ff837cd6a9556eeaaae4f69bb62a3767093a45c1fbc` |
| [outputs/tables/stress_paths.csv](../../outputs/tables/stress_paths.csv) | Estrés — trayectorias de regresores | Fuente aprobada; `005-estres` | `d6de3d807f2041120ce85cf8f1ef358d9eb7981ea7d9dfa8fd26f9af8084d126` |
| [outputs/tables/stress_paths.md](../../outputs/tables/stress_paths.md) | Estrés — trayectorias de regresores | Fuente aprobada; `005-estres` | `44fdb46c50fde68b4e238332d39a8a440dd379c7c4449c5beef1c71c25d29991` |
| [outputs/tables/stress_rate_sensitivity.csv](../../outputs/tables/stress_rate_sensitivity.csv) | Estrés — sensibilidad de tasa | Fuente aprobada; `005-estres` | `30e53f9f741a6170192ca756d08279730a3e017201d672123ff3ee1b04d9bb27` |
| [outputs/tables/stress_rate_sensitivity.md](../../outputs/tables/stress_rate_sensitivity.md) | Estrés — sensibilidad de tasa | Fuente aprobada; `005-estres` | `015dbd6210f14aa852f52c1f2f18b0b66278ae7a673c940ac80649413474b5a8` |
| [outputs/tables/stress_sensitivity.csv](../../outputs/tables/stress_sensitivity.csv) | Estrés — otras sensibilidades | Fuente aprobada; `005-estres` | `25fb9cf4139a1f9c4593d27029dd491b525dd2a16f3ce8e4b701a1e984a228d5` |
| [outputs/tables/stress_sensitivity.md](../../outputs/tables/stress_sensitivity.md) | Estrés — otras sensibilidades | Fuente aprobada; `005-estres` | `60294d063448fd296dd2684bd2fcd9746650eee40f7f225d2e57d6912eb9fc84` |
| [report/_variables.yml](../../report/_variables.yml) | Fuente única de variables del informe | Fuente aprobada; `001–006 (canónico)` | `2695ada1f4769333ae0cc76e59c0db3ca8dc8e5c504ae7087aa506cafe018140` |

## Hallazgos heredados y solicitudes

Las claves de coeficientes, efectos, diagnósticos, robustez, perfiles y sensibilidades aparecen arriba. Los tratamientos exigidos se consultan en la spec 006 y las auditorías de origen.
Claude compara este inventario con esos hallazgos y registra las claves ausentes en `specs/006-informe/solicitudes-claude.md` antes de T4. Ausencia de una clave no autoriza calcular ni estimar un resultado nuevo.

### Estacionariedad y faltantes declarados

- `datos.cpiaucsl_2025t4_meses`
- `datos.unrate_2025t4_meses`
- `datos.decision.dralacbs`
- `datos.decision.dralacbs_logit`
- `datos.decision.dralacbn`
- `datos.decision.dralacbn_logit`
- `datos.decision.drclacbs`
- `datos.decision.drclacbs_logit`
- `datos.decision.drblacbs`
- `datos.decision.drblacbs_logit`
- `datos.decision.drsreacbs`
- `datos.decision.drsreacbs_logit`
- `datos.decision.gdpc1_yoy`
- `datos.decision.gdp_yoy`
- `datos.decision.cpiaucsl_yoy`
- `datos.decision.loans_yoy`
- `datos.decision.unrate`
- `datos.decision.fedfunds`
- `datos.decision.coralacbs`
- `modelo1.no_i0`
- `modelo2.no_i0`

### Modelo I: coeficientes y efectos de impacto/largo plazo

- `modelo1.coef.const.coef`
- `modelo1.coef.const.ee`
- `modelo1.coef.const.p`
- `modelo1.coef.const.ic_inf`
- `modelo1.coef.const.ic_sup`
- `modelo1.coef.y_lag.coef`
- `modelo1.coef.y_lag.ee`
- `modelo1.coef.y_lag.p`
- `modelo1.coef.y_lag.ic_inf`
- `modelo1.coef.y_lag.ic_sup`
- `modelo1.coef.gdp_growth.coef`
- `modelo1.coef.gdp_growth.ee`
- `modelo1.coef.gdp_growth.p`
- `modelo1.coef.gdp_growth.ic_inf`
- `modelo1.coef.gdp_growth.ic_sup`
- `modelo1.coef.d_unemp.coef`
- `modelo1.coef.d_unemp.ee`
- `modelo1.coef.d_unemp.p`
- `modelo1.coef.d_unemp.ic_inf`
- `modelo1.coef.d_unemp.ic_sup`
- `modelo1.coef.inflation.coef`
- `modelo1.coef.inflation.ee`
- `modelo1.coef.inflation.p`
- `modelo1.coef.inflation.ic_inf`
- `modelo1.coef.inflation.ic_sup`
- `modelo1.coef.d_ffr.coef`
- `modelo1.coef.d_ffr.ee`
- `modelo1.coef.d_ffr.p`
- `modelo1.coef.d_ffr.ic_inf`
- `modelo1.coef.d_ffr.ic_sup`
- `modelo1.coef.credit_growth.coef`
- `modelo1.coef.credit_growth.ee`
- `modelo1.coef.credit_growth.p`
- `modelo1.coef.credit_growth.ic_inf`
- `modelo1.coef.credit_growth.ic_sup`
- `modelo1.coef.covid_2020q2.coef`
- `modelo1.coef.covid_2020q2.ee`
- `modelo1.coef.covid_2020q2.p`
- `modelo1.coef.covid_2020q2.ic_inf`
- `modelo1.coef.covid_2020q2.ic_sup`
- `modelo1.coef.covid_2020q3.coef`
- `modelo1.coef.covid_2020q3.ee`
- `modelo1.coef.covid_2020q3.p`
- `modelo1.coef.covid_2020q3.ic_inf`
- `modelo1.coef.covid_2020q3.ic_sup`
- `modelo1.coef.covid_2020q4.coef`
- `modelo1.coef.covid_2020q4.ee`
- `modelo1.coef.covid_2020q4.p`
- `modelo1.coef.covid_2020q4.ic_inf`
- `modelo1.coef.covid_2020q4.ic_sup`
- `modelo1.coef.covid_2021q1.coef`
- `modelo1.coef.covid_2021q1.ee`
- `modelo1.coef.covid_2021q1.p`
- `modelo1.coef.covid_2021q1.ic_inf`
- `modelo1.coef.covid_2021q1.ic_sup`
- `modelo1.efectos.gdp_growth.de`
- `modelo1.efectos.gdp_growth.impacto_pp`
- `modelo1.efectos.gdp_growth.impacto_pp_ee`
- `modelo1.efectos.gdp_growth.impacto_pp_p`
- `modelo1.efectos.gdp_growth.impacto_pp_ic_inf`
- `modelo1.efectos.gdp_growth.impacto_pp_ic_sup`
- `modelo1.efectos.gdp_growth.impacto_de`
- `modelo1.efectos.gdp_growth.impacto_de_ee`
- `modelo1.efectos.gdp_growth.impacto_de_p`
- `modelo1.efectos.gdp_growth.impacto_de_ic_inf`
- `modelo1.efectos.gdp_growth.impacto_de_ic_sup`
- `modelo1.efectos.gdp_growth.largo_pp`
- `modelo1.efectos.gdp_growth.largo_pp_ee`
- `modelo1.efectos.gdp_growth.largo_pp_p`
- `modelo1.efectos.gdp_growth.largo_pp_ic_inf`
- `modelo1.efectos.gdp_growth.largo_pp_ic_sup`
- `modelo1.efectos.gdp_growth.largo_de`
- `modelo1.efectos.gdp_growth.largo_de_ee`
- `modelo1.efectos.gdp_growth.largo_de_p`
- `modelo1.efectos.gdp_growth.largo_de_ic_inf`
- `modelo1.efectos.gdp_growth.largo_de_ic_sup`
- `modelo1.efectos.d_unemp.de`
- `modelo1.efectos.d_unemp.impacto_pp`
- `modelo1.efectos.d_unemp.impacto_pp_ee`
- `modelo1.efectos.d_unemp.impacto_pp_p`
- `modelo1.efectos.d_unemp.impacto_pp_ic_inf`
- `modelo1.efectos.d_unemp.impacto_pp_ic_sup`
- `modelo1.efectos.d_unemp.impacto_de`
- `modelo1.efectos.d_unemp.impacto_de_ee`
- `modelo1.efectos.d_unemp.impacto_de_p`
- `modelo1.efectos.d_unemp.impacto_de_ic_inf`
- `modelo1.efectos.d_unemp.impacto_de_ic_sup`
- `modelo1.efectos.d_unemp.largo_pp`
- `modelo1.efectos.d_unemp.largo_pp_ee`
- `modelo1.efectos.d_unemp.largo_pp_p`
- `modelo1.efectos.d_unemp.largo_pp_ic_inf`
- `modelo1.efectos.d_unemp.largo_pp_ic_sup`
- `modelo1.efectos.d_unemp.largo_de`
- `modelo1.efectos.d_unemp.largo_de_ee`
- `modelo1.efectos.d_unemp.largo_de_p`
- `modelo1.efectos.d_unemp.largo_de_ic_inf`
- `modelo1.efectos.d_unemp.largo_de_ic_sup`
- `modelo1.efectos.inflation.de`
- `modelo1.efectos.inflation.impacto_pp`
- `modelo1.efectos.inflation.impacto_pp_ee`
- `modelo1.efectos.inflation.impacto_pp_p`
- `modelo1.efectos.inflation.impacto_pp_ic_inf`
- `modelo1.efectos.inflation.impacto_pp_ic_sup`
- `modelo1.efectos.inflation.impacto_de`
- `modelo1.efectos.inflation.impacto_de_ee`
- `modelo1.efectos.inflation.impacto_de_p`
- `modelo1.efectos.inflation.impacto_de_ic_inf`
- `modelo1.efectos.inflation.impacto_de_ic_sup`
- `modelo1.efectos.inflation.largo_pp`
- `modelo1.efectos.inflation.largo_pp_ee`
- `modelo1.efectos.inflation.largo_pp_p`
- `modelo1.efectos.inflation.largo_pp_ic_inf`
- `modelo1.efectos.inflation.largo_pp_ic_sup`
- `modelo1.efectos.inflation.largo_de`
- `modelo1.efectos.inflation.largo_de_ee`
- `modelo1.efectos.inflation.largo_de_p`
- `modelo1.efectos.inflation.largo_de_ic_inf`
- `modelo1.efectos.inflation.largo_de_ic_sup`
- `modelo1.efectos.d_ffr.de`
- `modelo1.efectos.d_ffr.impacto_pp`
- `modelo1.efectos.d_ffr.impacto_pp_ee`
- `modelo1.efectos.d_ffr.impacto_pp_p`
- `modelo1.efectos.d_ffr.impacto_pp_ic_inf`
- `modelo1.efectos.d_ffr.impacto_pp_ic_sup`
- `modelo1.efectos.d_ffr.impacto_de`
- `modelo1.efectos.d_ffr.impacto_de_ee`
- `modelo1.efectos.d_ffr.impacto_de_p`
- `modelo1.efectos.d_ffr.impacto_de_ic_inf`
- `modelo1.efectos.d_ffr.impacto_de_ic_sup`
- `modelo1.efectos.d_ffr.largo_pp`
- `modelo1.efectos.d_ffr.largo_pp_ee`
- `modelo1.efectos.d_ffr.largo_pp_p`
- `modelo1.efectos.d_ffr.largo_pp_ic_inf`
- `modelo1.efectos.d_ffr.largo_pp_ic_sup`
- `modelo1.efectos.d_ffr.largo_de`
- `modelo1.efectos.d_ffr.largo_de_ee`
- `modelo1.efectos.d_ffr.largo_de_p`
- `modelo1.efectos.d_ffr.largo_de_ic_inf`
- `modelo1.efectos.d_ffr.largo_de_ic_sup`
- `modelo1.efectos.credit_growth.de`
- `modelo1.efectos.credit_growth.impacto_pp`
- `modelo1.efectos.credit_growth.impacto_pp_ee`
- `modelo1.efectos.credit_growth.impacto_pp_p`
- `modelo1.efectos.credit_growth.impacto_pp_ic_inf`
- `modelo1.efectos.credit_growth.impacto_pp_ic_sup`
- `modelo1.efectos.credit_growth.impacto_de`
- `modelo1.efectos.credit_growth.impacto_de_ee`
- `modelo1.efectos.credit_growth.impacto_de_p`
- `modelo1.efectos.credit_growth.impacto_de_ic_inf`
- `modelo1.efectos.credit_growth.impacto_de_ic_sup`
- `modelo1.efectos.credit_growth.largo_pp`
- `modelo1.efectos.credit_growth.largo_pp_ee`
- `modelo1.efectos.credit_growth.largo_pp_p`
- `modelo1.efectos.credit_growth.largo_pp_ic_inf`
- `modelo1.efectos.credit_growth.largo_pp_ic_sup`
- `modelo1.efectos.credit_growth.largo_de`
- `modelo1.efectos.credit_growth.largo_de_ee`
- `modelo1.efectos.credit_growth.largo_de_p`
- `modelo1.efectos.credit_growth.largo_de_ic_inf`
- `modelo1.efectos.credit_growth.largo_de_ic_sup`

### Modelo I: diagnósticos, robustez y evaluación fuera de muestra

- `modelo1.robustez.gdp_growth`
- `modelo1.robustez.d_unemp`
- `modelo1.robustez.inflation`
- `modelo1.robustez.d_ffr`
- `modelo1.robustez.credit_growth`
- `modelo1.oos.n_trimestres`
- `modelo1.oos.rmse_modelo_un_paso`
- `modelo1.oos.rmse_ingenuo_un_paso`
- `modelo1.oos.mae_modelo_un_paso`
- `modelo1.oos.mae_ingenuo_un_paso`
- `modelo1.oos.cociente_un_paso`
- `modelo1.oos.rmse_modelo_dinamico`
- `modelo1.oos.rmse_ingenuo_dinamico`
- `modelo1.oos.mae_modelo_dinamico`
- `modelo1.oos.mae_ingenuo_dinamico`
- `modelo1.oos.cociente_dinamico`
- `modelo1.oos.dm_estadistico`
- `modelo1.oos.dm_p`
- `modelo1.oos.veredicto_un_paso`
- `modelo1.oos.veredicto_dinamico`
- `modelo1.oos.significancia_un_paso`

### Modelo II: K elegido, AIC y BIC

- `modelo2.k_elegido`
- `modelo2.k_bic`
- `modelo2.k_aic`

### Modelo II: perfil de la tasa (phi)

- `modelo2.lp.h0.phi`
- `modelo2.lp.h1.phi`
- `modelo2.lp.h2.phi`
- `modelo2.lp.h3.phi`
- `modelo2.lp.h4.phi`
- `modelo2.lp.h5.phi`
- `modelo2.lp.h6.phi`
- `modelo2.lp.h7.phi`
- `modelo2.lp.h8.phi`
- `modelo2.lp.h9.phi`
- `modelo2.lp.h10.phi`
- `modelo2.lp.h11.phi`
- `modelo2.lp.h12.phi`

### Modelo II: efectos, regla y diagnósticos

- `modelo2.efectos.s.est`
- `modelo2.efectos.s.ee`
- `modelo2.efectos.s.chi2`
- `modelo2.efectos.s.p`
- `modelo2.efectos.s.ic_inf`
- `modelo2.efectos.s.ic_sup`
- `modelo2.efectos.s_rez.est`
- `modelo2.efectos.s_rez.ee`
- `modelo2.efectos.s_rez.chi2`
- `modelo2.efectos.s_rez.p`
- `modelo2.efectos.s_rez.ic_inf`
- `modelo2.efectos.s_rez.ic_sup`
- `modelo2.efectos.h1.signo`
- `modelo2.efectos.h1.respaldada`

### Estrés: diferencia entre picos y sensibilidades

- `estres.dif_modelos.severo.delta_final`
- `estres.dif_modelos.severo.delta_pico`
- `estres.dif_modelos.propio.delta_final`
- `estres.dif_modelos.propio.delta_pico`
- `estres.sens_tasa.modelo1.severo.c_final`
- `estres.sens_tasa.modelo1.severo.c_final_p05`
- `estres.sens_tasa.modelo1.severo.c_final_p95`
- `estres.sens_tasa.modelo1.severo.c_pico`
- `estres.sens_tasa.modelo1.severo.prop_c_pos_final`
- `estres.sens_tasa.modelo1.severo.prop_c_pos_pico`
- `estres.sens_tasa.modelo1.propio.c_final`
- `estres.sens_tasa.modelo1.propio.c_final_p05`
- `estres.sens_tasa.modelo1.propio.c_final_p95`
- `estres.sens_tasa.modelo1.propio.c_pico`
- `estres.sens_tasa.modelo1.propio.prop_c_pos_final`
- `estres.sens_tasa.modelo1.propio.prop_c_pos_pico`
- `estres.sens_tasa.modelo2.severo.c_final`
- `estres.sens_tasa.modelo2.severo.c_final_p05`
- `estres.sens_tasa.modelo2.severo.c_final_p95`
- `estres.sens_tasa.modelo2.severo.c_pico`
- `estres.sens_tasa.modelo2.severo.prop_c_pos_final`
- `estres.sens_tasa.modelo2.severo.prop_c_pos_pico`
- `estres.sens_tasa.modelo2.propio.c_final`
- `estres.sens_tasa.modelo2.propio.c_final_p05`
- `estres.sens_tasa.modelo2.propio.c_final_p95`
- `estres.sens_tasa.modelo2.propio.c_pico`
- `estres.sens_tasa.modelo2.propio.prop_c_pos_final`
- `estres.sens_tasa.modelo2.propio.prop_c_pos_pico`
- `estres.sens_cal.modelo1.delta_final_2029t1`
- `estres.sens_cal.modelo1.delta_principal_2029t1`
- `estres.sens_cal.modelo1.delta_pico`
- `estres.sens_cal.modelo2.delta_final_2029t1`
- `estres.sens_cal.modelo2.delta_principal_2029t1`
- `estres.sens_cal.modelo2.delta_pico`
- `estres.sens_cred.modelo1.base.cero.nivel_final`
- `estres.sens_cred.modelo1.base.cero.nivel_pico`
- `estres.sens_cred.modelo1.base.cero.nivel_pico_trimestre`
- `estres.sens_cred.modelo1.base.media.nivel_final`
- `estres.sens_cred.modelo1.base.media.nivel_pico`
- `estres.sens_cred.modelo1.base.media.nivel_pico_trimestre`
- `estres.sens_cred.modelo1.severo.cero.nivel_final`
- `estres.sens_cred.modelo1.severo.cero.nivel_pico`
- `estres.sens_cred.modelo1.severo.cero.nivel_pico_trimestre`
- `estres.sens_cred.modelo1.severo.media.nivel_final`
- `estres.sens_cred.modelo1.severo.media.nivel_pico`
- `estres.sens_cred.modelo1.severo.media.nivel_pico_trimestre`
- `estres.sens_cred.modelo2.base.cero.nivel_final`
- `estres.sens_cred.modelo2.base.cero.nivel_pico`
- `estres.sens_cred.modelo2.base.cero.nivel_pico_trimestre`
- `estres.sens_cred.modelo2.base.media.nivel_final`
- `estres.sens_cred.modelo2.base.media.nivel_pico`
- `estres.sens_cred.modelo2.base.media.nivel_pico_trimestre`
- `estres.sens_cred.modelo2.severo.cero.nivel_final`
- `estres.sens_cred.modelo2.severo.cero.nivel_pico`
- `estres.sens_cred.modelo2.severo.cero.nivel_pico_trimestre`
- `estres.sens_cred.modelo2.severo.media.nivel_final`
- `estres.sens_cred.modelo2.severo.media.nivel_pico`
- `estres.sens_cred.modelo2.severo.media.nivel_pico_trimestre`
- `estres.sens_origen.modelo1.base.nivel_final`
- `estres.sens_origen.modelo1.base.nivel_pico`
- `estres.sens_origen.modelo1.base.nivel_pico_trimestre`
- `estres.sens_origen.modelo1.severo.nivel_final`
- `estres.sens_origen.modelo1.severo.nivel_pico`
- `estres.sens_origen.modelo1.severo.nivel_pico_trimestre`
- `estres.sens_origen.modelo1.severo.delta_k13`
- `estres.sens_origen.modelo2.base.nivel_final`
- `estres.sens_origen.modelo2.base.nivel_pico`
- `estres.sens_origen.modelo2.base.nivel_pico_trimestre`
- `estres.sens_origen.modelo2.severo.nivel_final`
- `estres.sens_origen.modelo2.severo.nivel_pico`
- `estres.sens_origen.modelo2.severo.nivel_pico_trimestre`
- `estres.sens_origen.modelo2.severo.delta_k13`

### Estrés: niveles fuera de rango y extremos

- `estres.modelo1.fuera_rango.n`
- `estres.modelo1.fuera_rango.prop`
- `estres.modelo1.fuera_rango.min`
- `estres.modelo1.fuera_rango.max`
- `estres.modelo2.fuera_rango.n`
- `estres.modelo2.fuera_rango.prop`
- `estres.modelo2.fuera_rango.min`
- `estres.modelo2.fuera_rango.max`

### Conteos y tabla de literatura

- `literatura.n_estudios_verificados`
- `literatura.n_pendiente_lectura`
- `literatura.n_descartados`
- `literatura.n_datos_metodo_verificados`
- `literatura.por_tema.t21`
- `literatura.por_tema.t22`
- `literatura.por_tema.t23`
- `literatura.por_tema.t24`
- `literatura.por_tema.t25`

La conciliación de `datos.n_series` y la URL institucional de FRED corresponden a T4. Los parámetros del entrenamiento de 003 no se exportaron como claves: si hicieran falta para una explicación nueva, requieren `change`; no se reconstruyen ni estiman en 006.
## Registro editorial: identificadores y destinos

La verificación estructural de enlaces no equivale a un clic comprobado en Google Docs o Word.

| Identificador | Fuente | Destino completo | En el cuerpo |
| --- | --- | --- | --- |
| AF-DELINQUENCY-UNEMPLOYMENT-FFR | `outputs/figures/delinquency_unemployment_ffr.png` | Anexo A; `af-delinquency-unemployment-ffr` | esencial sin recortar |
| AT-DESCRIPTIVES | `outputs/tables/descriptives.csv` | Anexo A; `at-descriptives` | ninguno |
| AT-STATIONARITY | `outputs/tables/stationarity.csv` | Anexo A; `at-stationarity` | ninguno |
| AF-M1-COEFFICIENTS | `outputs/figures/model1_coefficients.png` | Anexo B; `af-m1-coefficients` | ninguno |
| AF-M1-CUSUM | `outputs/figures/model1_cusum.png` | Anexo B; `af-m1-cusum` | ninguno |
| AF-M1-OOS | `outputs/figures/model1_oos.png` | Anexo B; `af-m1-oos` | ninguno |
| AT-M1-COEFFICIENTS | `outputs/tables/model1_coefficients.csv` | Anexo B; `at-m1-coefficients` | reducida |
| AT-M1-DIAGNOSTICS | `outputs/tables/model1_diagnostics.csv` | Anexo B; `at-m1-diagnostics` | reducida |
| AT-M1-EFFECTS | `outputs/tables/model1_effects.csv` | Anexo B; `at-m1-effects` | ninguno |
| AT-M1-LIMITATIONS | `outputs/tables/model1_limitations.csv` | Anexo B; `at-m1-limitations` | ninguno |
| AT-M1-OOS | `outputs/tables/model1_oos.csv` | Anexo B; `at-m1-oos` | ninguno |
| AT-M1-ROB | `outputs/tables/model1_robustness_estimates.csv` | Anexo B; `at-m1-rob` | ninguno |
| AT-M1-ROBUSTNESS-SUMMARY | `outputs/tables/model1_robustness_summary.csv` | Anexo B; `at-m1-robustness-summary` | ninguno |
| AT-M1-STATIONARITY | `outputs/tables/model1_stationarity.csv` | Anexo B; `at-m1-stationarity` | ninguno |
| AF-M2-CUSUM | `outputs/figures/model2_cusum.png` | Anexo C; `af-m2-cusum` | ninguno |
| AF-M2-PROFILE | `outputs/figures/model2_profile.png` | Anexo C; `af-m2-profile` | ninguno |
| AF-M2-RESPONSE | `outputs/figures/model2_response.png` | Anexo C; `af-m2-response` | esencial sin recortar |
| AT-M2-COEFFICIENTS | `outputs/tables/model2_coefficients.csv` | Anexo C; `at-m2-coefficients` | ninguno |
| AT-M2-COMPARISON | `outputs/tables/model2_comparison.csv` | Anexo C; `at-m2-comparison` | ninguno |
| AT-M2-DIAGNOSTICS | `outputs/tables/model2_diagnostics.csv` | Anexo C; `at-m2-diagnostics` | ninguno |
| AT-M2-EFFECTS | `outputs/tables/model2_effects.csv` | Anexo C; `at-m2-effects` | ninguno |
| AT-M2-INPUTS63 | `outputs/tables/model2_inputs63.csv` | Anexo C; `at-m2-inputs63` | reducida |
| AT-M2-LIMITATIONS | `outputs/tables/model2_limitations.csv` | Anexo C; `at-m2-limitations` | ninguno |
| AT-M2-LP | `outputs/tables/model2_lp.csv` | Anexo C; `at-m2-lp` | ninguno |
| AT-M2-READING | `outputs/tables/model2_reading.csv` | Anexo C; `at-m2-reading` | reducida |
| AT-M2-ROBUSTNESS-ESTIMATES | `outputs/tables/model2_robustness_estimates.csv` | Anexo C; `at-m2-robustness-estimates` | ninguno |
| AT-M2-ROBUSTNESS-SUMMARY | `outputs/tables/model2_robustness_summary.csv` | Anexo C; `at-m2-robustness-summary` | ninguno |
| AT-M2-SELECTION | `outputs/tables/model2_selection.csv` | Anexo C; `at-m2-selection` | ninguno |
| AT-M2-STATIONARITY | `outputs/tables/model2_stationarity.csv` | Anexo C; `at-m2-stationarity` | ninguno |
| AT-M2-TRAJECTORY | `outputs/tables/model2_trajectory.csv` | Anexo C; `at-m2-trajectory` | ninguno |
| AF-EST-MODEL1 | `outputs/figures/stress_model1.png` | Anexo D; `af-est-model1` | esencial sin recortar |
| AF-EST-MODEL2 | `outputs/figures/stress_model2.png` | Anexo D; `af-est-model2` | esencial sin recortar |
| AT-EST-DELTA | `outputs/tables/stress_delta.csv` | Anexo D; `at-est-delta` | reducida |
| AT-EST-LEVELS | `outputs/tables/stress_levels.csv` | Anexo D; `at-est-levels` | ninguno |
| AT-EST-LIMITATIONS | `outputs/tables/stress_limitations.csv` | Anexo D; `at-est-limitations` | ninguno |
| AT-EST-MODELS | `outputs/tables/stress_models.csv` | Anexo D; `at-est-models` | ninguno |
| AT-EST-ORIGIN | `outputs/tables/stress_origin.csv` | Anexo D; `at-est-origin` | ninguno |
| AT-EST-PATHS | `outputs/tables/stress_paths.csv` | Anexo D; `at-est-paths` | ninguno |
| AT-EST-RATE-SENSITIVITY | `outputs/tables/stress_rate_sensitivity.csv` | Anexo D; `at-est-rate-sensitivity` | ninguno |
| AT-EST-SENSITIVITY | `outputs/tables/stress_sensitivity.csv` | Anexo D; `at-est-sensitivity` | ninguno |
| AT-LIT-ESTUDIOS | `outputs/tables/lit_estudios.csv` | Anexo E; `at-lit-estudios` | reducida |
| AT-FRED-MANIFEST | `data/raw/manifest.csv` | Anexo F; `at-fred-manifest` | reducida |
| AT-M1-DEVIATIONS | `outputs/tables/model1_deviations.csv` | Anexo F; `at-m1-deviations` | ninguno |
| AT-M2-DEVIATIONS | `outputs/tables/model2_deviations.csv` | Anexo F; `at-m2-deviations` | ninguno |
