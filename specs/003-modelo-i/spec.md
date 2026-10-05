# Spec 003 — Modelo I: determinantes macroeconómicos de la morosidad
Estado: aprobada · Crítica: sí

## Contexto y objetivo
La guía pide un primer modelo que relacione el ciclo macroeconómico con el riesgo de crédito y que se estime, se diagnostique y se interprete desde la gestión de riesgos. Esta spec fija ese modelo **antes de ver ningún resultado** (pre-registro, principio 2 de la constitución): variables, transformaciones, rezagos, estimador, signos esperados, diagnósticos, robusteces y validación fuera de muestra. La redactamos conociendo la tabla de estacionariedad de la spec 001 (un insumo de datos, no un resultado del modelo); ningún coeficiente se ha estimado.

Objetivo: estimar por MCO con errores Newey-West la asociación entre la tasa de morosidad de todos los préstamos de los bancos comerciales de EE. UU. (DRALACBS) y el crecimiento del PIB real, el cambio del desempleo, la inflación, el cambio de la tasa de fondos federales y el crecimiento rezagado del crédito, en 2000T1–2026T2. Además se entregan una batería completa de diagnósticos, las variantes de robustez R1–R8, una validación fuera de muestra y los efectos en puntos porcentuales (pp) de morosidad, para el informe y para la prueba de estrés (spec 005).

## Pregunta que responde (y sección de docs/guia-profesor.md que cubre)
¿Cómo se asocian las condiciones macroeconómicas con el comportamiento del riesgo de crédito?

Reparto con otras specs:
- **Esta spec** produce todos los insumos cuantitativos de las secciones 3.5 (especificación del Modelo I), 4 (estimación, coeficientes, significancia y diagnósticos) y 6.1 (resultados), incluidos los efectos en pp que necesita la interpretación desde la gestión de riesgos.
- **La spec 006** redacta esa interpretación, la discusión y la comparación con la literatura (2.5 y 6.3). Esta spec no escribe prosa interpretativa.

Frontera con el Modelo II (spec 004): el Modelo I mide la asociación **contemporánea** de la morosidad con el conjunto de condiciones macro del trimestre, con ΔFFR como una variable macro más. El Modelo II estudia la respuesta **dinámica y rezagada** de la morosidad a un cambio de la política monetaria. La única variable de tasas de este modelo, ΔFFR, cubre a la vez la «tasa de interés» de la sección 3.3 de la guía y el «cambio en la FFR» de la 3.4; esto se declara (RF-21).

## Usuarios
- El autor, que redacta las secciones 3.5, 4 y 6.1 del informe con las salidas de esta spec.
- La spec 005 (estrés), que usa los coeficientes y la covarianza HAC de la especificación principal (RF-8) y los efectos por 1 pp de PIB, ΔU y ΔFFR, que su escenario adverso necesita.
- La spec 004 (Modelo II), que compara sus resultados con los de este modelo en 6.3.
- El revisor econométrico (auditoría crítica) y el profesor evaluador.

## Historias de usuario
- HU-1. Como autor, quiero una especificación fijada y commiteada antes de estimar para demostrar que no elegí el modelo según los resultados.
- HU-2. Como autor, quiero una tabla de coeficientes con error HAC, p-valor, IC 95 % y comparación con el signo esperado para evaluar la significancia y discutir las sorpresas.
- HU-3. Como autor, quiero cada efecto en pp de morosidad, de impacto y de largo plazo, por 1 pp y por 1 desviación estándar del regresor, para traducir los resultados al lenguaje de gestión de riesgos.
- HU-4. Como revisor, quiero todos los diagnósticos reportados con su estadístico y su p-valor, incluidos los que fallen, para juzgar la validez de las conclusiones.
- HU-5. Como autor, quiero un criterio de robustez medible y un veredicto fuera de muestra contra un modelo ingenuo para saber cuánto confiar en el modelo antes de usarlo en el estrés.

## Definiciones
- **Panel, trimestre, variación interanual, logit, regla de decisión niveles/diferencias y último trimestre común**: los de la spec 001.
- **Historia transformada**: las transformaciones de RF-9 de la spec 001 calculadas sobre toda la historia descargada, antes del recorte a 2000T1 de su RF-10. Todos los rezagos y diferencias de esta spec se toman de ella, de modo que el trimestre 2000T1 pueda usar valores de 1999. Las muestras de estimación se recortan después de construir rezagos y diferencias.
- **Tabla de estacionariedad**: la tabla de ADF/KPSS con decisión y orden de integración que produce la spec 001 sobre 2000T1–2026T2. Cada dependiente se identifica por su columna del panel y la forma «tal cual»: `dralacbs`, `dralacbn`, `dralacbs_logit`, `drclacbs`, `drblacbs` y `drsreacbs`. Para ΔU y ΔFFR, cuya fila «primera diferencia» no trae decisión, la estacionariedad se juzga aplicando la regla de la spec 001 al ADF y KPSS de las filas «primera diferencia» de `unrate` y `fedfunds`.
- **Y (forma de la dependiente)**: la morosidad entra en nivel (pp) si la tabla de estacionariedad da «niveles» para su columna, y en primera diferencia trimestral (pp) si da «primera diferencia» o «ambigua (primera diferencia)». La decisión es la de la tabla, calculada sobre 2000T1–2026T2; no se recalcula sobre la muestra efectiva de ninguna regresión.
- **Formas esperadas a la fecha de aprobación** (leídas de la tabla de estacionariedad el 5-oct-2026): `dralacbs` ambigua → primera diferencia, I(1); `dralacbn` ambigua → primera diferencia, I(1); `dralacbs_logit` → primera diferencia, posible I(2); `drclacbs` → primera diferencia, I(1); `drblacbs` → primera diferencia, I(1); `drsreacbs` ambigua → primera diferencia, posible I(2). Por tanto, todas las dependientes de esta spec entran hoy en primera diferencia.
- **Muestra principal**: 2000T1–2026T2, estricta (106 trimestres; los rezagos de 2000T1 salen de la historia transformada).
- **Muestra larga objetivo**: 1985T1–2026T2. DRALACBS empieza en 1985T1 según FRED; esto no está verificado con las descargas congeladas, que empiezan en 1998. Su uso es condicional (R8).
- **Inicio efectivo**: el primer trimestre en que existen todos los términos de una regresión en la historia transformada, sin imputar.
- **Significativo**: p < 0,05 bilateral con errores HAC. Se usa en la tabla principal.
- **Distribución de referencia**: los estadísticos t, los p-valores y los IC 95 % de todos los coeficientes y efectos usan la normal estándar (inferencia asintótica HAC), no la t de Student.
- **Robusto (criterio pre-registrado)**: un coeficiente de la especificación principal es robusto en una regresión de robustez si en ella conserva el signo de la principal **y** tiene p < 0,10 bilateral con errores HAC. La exigencia de p < 0,10 impide que un coeficiente cercano a cero cuente como robusto por un signo debido al ruido.
- **Ventana HAC**: floor(4·(T/100)^(2/9)) rezagos, con T = observaciones efectivas de cada regresión, kernel de Bartlett. Para cualquier T ≥ 1 la fórmula da al menos 1 rezago.
- **Dummy de impulso**: dummy que vale 1 en un solo trimestre de la muestra (las COVID). El residuo de ese trimestre es exactamente 0, así que su columna no aporta a la matriz de puntuaciones de Newey-West, y la covarianza HAC completa tiene rango k − (número de dummies de impulso) por construcción. Esa reducción de rango es esperada: no es un fallo numérico y no se trata como tal. Los EE HAC de las dummies de impulso se reportan con la nota «EE HAC no informativo: dummy de impulso con residuo nulo».
- **Matriz HAC no definida positiva**: la comprobación se hace sobre el sub-bloque de la covarianza HAC de los términos que no son dummies de impulso (constante, ρ, regresores macro y, si los hay, dummies estacionales). El kernel de Bartlett lo garantiza semidefinido positivo en teoría. Si numéricamente algún valor propio de ese sub-bloque es ≤ 0 (o inferior a una tolerancia declarada en el plan), se aplica truncamiento espectral: los valores propios se elevan a ese piso, se reconstruye el sub-bloque y el ajuste se declara en el pie de la tabla de esa regresión.
- **Efecto de impacto**: el coeficiente β del regresor.
- **Efecto de largo plazo**: β/(1 − ρ), con ρ el coeficiente del rezago de Y. Su error estándar sale del método delta con la covarianza HAC, y su p-valor y su IC 95 % se calculan con la distribución de referencia (z = estimación / error delta). Si Y está en nivel, es el cambio de largo plazo de la morosidad ante un cambio permanente de 1 unidad del regresor. Si Y está en primera diferencia (el caso esperado), es el cambio acumulado en el **nivel** de la morosidad ante un aumento transitorio de 1 unidad del regresor durante un trimestre. **Solo se reporta si 1 − ρ̂ > 0,05**; si 1 − ρ̂ ≤ 0,05 (ρ̂ ≥ 0,95), se reporta solo el efecto de impacto y el largo plazo figura como «no reportado (1 − ρ ≤ 0,05)».
- **Por 1 DE**: efecto multiplicado por la desviación estándar muestral (divisor n − 1) del regresor, en la forma en que entra, calculada sobre la muestra efectiva de la especificación principal **sin los trimestres con dummy COVID (2020T2–2021T1)**. El modelo ya neutraliza esos trimestres con sus dummies, y con ellos dentro la DE quedaría dominada por el salto atípico (por ejemplo, el del desempleo en 2020T2). Si esa desviación estándar es 0, el efecto por 1 DE figura como «no definido».
- **Lenguaje de asociación**: «efecto de impacto» y «efecto de largo plazo» son nombres técnicos de cantidades del modelo y se definen en el informe como asociaciones condicionales, no causales.

## Especificación pre-registrada

### Variables y transformaciones
| Término | Serie | Forma | Unidad | Estacionariedad (spec 001) |
|---|---|---|---|---|
| Y(t) | DRALACBS | nivel o Δ trimestral según la tabla (hoy Δ) | pp | ambigua → Δ, I(1) |
| Y(t−1) | DRALACBS | la misma forma que Y, rezagada un trimestre | pp | — |
| PIB(t) | GDPC1 | variación interanual | % | I(0) |
| ΔU(t) | UNRATE | diferencia trimestral | pp | estacionaria (fila «primera diferencia») |
| π(t) | CPIAUCSL | variación interanual | % | ambigua, I(1) |
| ΔFFR(t) | FEDFUNDS | diferencia trimestral | pp | estacionaria (fila «primera diferencia») |
| CRED(t−4) | LOANS | variación interanual, rezagada 4 trimestres | % | ambigua, I(1) |
| D(k) | — | una dummy por trimestre: 2020T2, 2020T3, 2020T4 y 2021T1 | 0/1 | — |

La regla de la spec 001 decide **solo la forma de la dependiente**. Los regresores macro entran en la forma económica estándar fijada en esta tabla, que ya es una tasa de variación con interpretación directa. Es una decisión de pre-registro que se aparta a propósito de la regla de la skill de econometría, que la aplica a todas las series. Razones:
- Diferenciar π o CRED dejaría regresores como el «cambio de la inflación interanual», difíciles de interpretar y de usar en los escenarios de estrés.
- ΔU y ΔFFR entran en diferencia aunque la tabla clasifica UNRATE y FEDFUNDS en niveles: la guía (3.4) pide el **cambio** de la FFR, y el cambio del desempleo recoge el flujo de hogares que pierden ingresos, que es el mecanismo hacia el impago.

La no estacionariedad residual (hoy: π y CRED, «ambigua», I(1)) se documenta como limitación del modelo en el informe (RF-20), y no cambia la especificación.

### Ecuación (especificación principal)
Y(t) = α + ρ·Y(t−1) + β₁·PIB(t) + β₂·ΔU(t) + β₃·π(t) + β₄·ΔFFR(t) + β₅·CRED(t−4) + Σₖ δₖ·D(k) + ε(t)

Con Y en primera diferencia, cada δₖ es el desvío del **cambio** trimestral de la morosidad en ese trimestre COVID, no un desvío de su nivel. Fuera de 2020T2–2021T1 las dummies valen 0, también en cualquier proyección (spec 005).

### Rezagos y su criterio
Fijos, sin selección por criterio de información:
- Un rezago de la dependiente, para recoger la persistencia de la morosidad.
- Regresores macro contemporáneos: la morosidad del trimestre refleja las condiciones del mismo trimestre.
- Crédito rezagado 4 trimestres: la expansión del crédito se asocia con deterioro de la cartera con retraso, porque los préstamos tardan en madurar y entrar en mora.

Los rezagos de crédito de 8 y 12 trimestres van como robustez. La regla de la skill sobre el «efecto acumulado» (suma de coeficientes de la tasa con prueba de Wald) no aplica aquí, porque ΔFFR entra con un solo término contemporáneo; los rezagos distribuidos de la tasa son materia del Modelo II (spec 004).

### Estimador y errores estándar
MCO con errores Newey-West (ventana HAC y tratamiento de la matriz no definida positiva según Definiciones). Con un rezago de la dependiente, MCO solo es consistente si los errores no están autocorrelacionados: la prueba de Breusch-Godfrey es decisiva y, si rechaza, se declara como limitación de la especificación principal.

### Signos esperados y mecanismo
| Término | Signo | Mecanismo |
|---|---|---|
| PIB | − | Más actividad, más ingresos de hogares y empresas y mayor capacidad de pago. |
| ΔU | + | Más desempleo, pérdida de ingresos y más impagos de los hogares. |
| ΔFFR | + | Tasas más altas encarecen el servicio de la deuda a tasa variable y endurecen las condiciones financieras. |
| CRED(t−4) | + | Las expansiones rápidas del crédito relajan los estándares y la mora aparece con retraso. |
| π | sin contraste | Ambiguo: erosiona la carga real de la deuda (−), pero reduce el ingreso real y anticipa alzas de tasas (+). |
| ρ | sin contraste | Se espera positivo por persistencia, pero no se contrasta. |
| constante y D(k) | sin contraste | Sin hipótesis de signo. |

La trazabilidad de cada signo con los estudios de la matriz de literatura (spec 002) se hace en la discusión del informe (spec 006).

### Regla de decisión niveles/diferencias
La de la spec 001, leída de la tabla de estacionariedad para la columna de cada dependiente (ver Definiciones, «Y» y «Formas esperadas»).

### Pruebas de robustez previstas
Cada variante cambia **un solo aspecto** de la especificación principal (la muestra, la dependiente o un regresor) y solo añade los ajustes mínimos que ese aspecto exige, declarados aquí. Todas usan la historia transformada.
- **R1. Sin 2020–2021.** Aspecto: muestra. Excluye 2020T1–2021T4. Las cuatro dummies COVID desaparecen porque sus trimestres quedan fuera. La exclusión se declara en la tabla.
- **R2. DRALACBN** (sin desestacionalizar) como dependiente. Aspecto: dependiente, en la forma que da la tabla (hoy Δ). Ajuste mínimo: tres dummies estacionales para T2, T3 y T4, con T1 como trimestre base, porque una serie sin desestacionalizar las necesita.
- **R3. Sub-carteras** como dependiente, en la forma que da la tabla (hoy Δ en las tres), con una regresión por serie:
  - DRCLACBS (tarjetas de crédito).
  - DRBLACBS (préstamos empresariales).
  - DRSREACBS (inmobiliarios residenciales; posible I(2), declarado como limitación).

  Se aplican los mismos signos esperados.
- **R4. GDP nominal.** Aspecto: regresor. Su variación interanual sustituye a la de GDPC1.
- **R5. Logit** de DRALACBS como dependiente. Entra en la forma que da la tabla (hoy primera diferencia del logit, posible I(2), declarado como limitación), y su rezago en la misma forma.
- **R6. Crédito rezagado 8 trimestres** en lugar de 4.
- **R7. Crédito rezagado 12 trimestres** en lugar de 4.
- **R8. Muestra larga.** Aspecto: muestra. Va desde el inicio efectivo más temprano que permita la historia transformada hasta 2026T2, con las dummies COVID.

**Robusteces condicionales a la historia disponible** (R6, R7 y R8). No se pide ningún cambio retroactivo en la spec 001: estas variantes usan la historia transformada que exista y se truncan al inicio efectivo que esta permita. Ese inicio se reporta y no se imputa nada.
- Con la descarga congelada desde 1998, el crecimiento interanual de LOANS existe desde 1999T1, así que R6 empieza en 2001T1 y R7 en 2002T1. Su fin es 2026T2.
- Con esa misma descarga, R8 empezaría en 2000T1, igual que la principal, y no aportaría información. En ese caso R8 figura como «no estimada: sin historia anterior a 2000T1» y sale del denominador del recuento de robustez.
- Si en el futuro un `/sdd-change` aprobado de la spec 001 amplía la historia, R6–R8 se estiman con ella sin cambiar esta spec. La forma de la dependiente sigue siendo la de la tabla de estacionariedad sobre 2000T1–2026T2; no se recalcula ADF/KPSS para la muestra larga.

### Validación fuera de muestra
- **Muestras:** estimación en 2000T1–2019T4, sin dummies COVID porque no hay trimestres COVID; evaluación en 2022T1–2026T2 con los regresores observados. Los trimestres 2020T1–2021T4 quedan fuera de ambos tramos a propósito, para no evaluar el modelo en el choque COVID. No hay reentrenamiento.
- **Pronóstico a un paso:** usa la Y(t−1) observada. Si Y está en diferencias, el nivel pronosticado en t es el nivel observado en t−1 más el ΔY pronosticado para t.
- **Pronóstico dinámico:** parte de la Y observada en 2021T4 y encadena la Y pronosticada, como hará la spec 005. Si Y está en diferencias, el nivel pronosticado en t es el nivel observado en 2021T4 más la suma de los ΔY pronosticados desde 2022T1 hasta t.
- **Evaluación:** siempre en el **nivel** de la morosidad, en pp.
- **Comparador ingenuo** (paseo aleatorio): a un paso, DR(t−1) observada; en el dinámico, DR(2021T4) constante.
- **Métricas:** RMSE y MAE del modelo y del ingenuo, y el cociente RMSE modelo/ingenuo.
- **Prueba de Diebold-Mariano**, solo para el pronóstico a un paso: pérdida cuadrática, bilateral, con la corrección de Harvey, Leybourne y Newbold. No se aplica al dinámico porque mezcla horizontes distintos.
- **Veredicto pre-registrado** para cada tipo de pronóstico:
  - «supera al ingenuo» si el cociente RMSE es < 1; si no, «no supera al ingenuo».
  - En el pronóstico a un paso, además, «significativo» si DM tiene p < 0,05 y «no significativo» en otro caso.

## Requisitos funcionales

### Datos y muestras
- RF-1: EL SISTEMA construirá todas las variables, rezagos y diferencias sobre la historia transformada y recortará después cada muestra de estimación. La especificación principal usará la muestra principal estricta 2000T1–2026T2.
- RF-2: SI falta algún término de la ecuación en un trimestre dentro de la muestra de una regresión, después de su inicio efectivo, ENTONCES EL SISTEMA se detendrá con un error que nombre la variable, el trimestre y la regresión, sin imputar ni eliminar filas en silencio.
- RF-3: EL SISTEMA leerá de la tabla de estacionariedad la decisión de cada dependiente (Definiciones) y construirá Y y Y(t−1) según ella.
- RF-4: SI la decisión leída para alguna dependiente difiere de las «Formas esperadas a la fecha de aprobación», ENTONCES EL SISTEMA se detendrá con un error que nombre la serie y las dos formas. Continuar exige un `/sdd-change` de esta spec.
- RF-5: CUANDO R6, R7 o R8 se estimen, EL SISTEMA usará el inicio efectivo que permita la historia transformada y lo reportará. SI el inicio efectivo de R8 no es anterior a 2000T1, ENTONCES EL SISTEMA no la estimará y la reportará como «no estimada: sin historia anterior a 2000T1».
- RF-6: SI una regresión tiene menos de 30 grados de libertad (observaciones menos parámetros) o una matriz de regresores de rango incompleto, ENTONCES EL SISTEMA:
  - si es la especificación principal o la de la validación fuera de muestra, se detendrá con un error que nombre la regresión;
  - si es una robustez, la reportará como «no estimada» con el motivo y la sacará del denominador del recuento.

### Estimación principal
- RF-7: EL SISTEMA estimará la especificación principal por MCO con errores Newey-West en la muestra principal, con la ventana HAC y el tratamiento de la matriz no definida positiva de Definiciones.
- RF-8: EL SISTEMA guardará, como salida de la etapa de modelos del pipeline, los coeficientes, la matriz de covarianza HAC, los nombres de los términos, la forma de Y, la muestra efectiva y los rezagos de la ventana HAC de la especificación principal, en un formato legible por máquina que la spec 005 cargue sin reestimar.
- RF-9: EL SISTEMA producirá una tabla de coeficientes con una fila por término (constante, ρ, β₁–β₅ y δₖ). Columnas:
  - coeficiente, error HAC, estadístico z, p-valor e IC 95 %;
  - signo esperado y si el signo estimado coincide: «sí», «no» o «sin contraste» (este último para π, ρ, la constante y las dummies).

  El pie de la tabla traerá: forma de Y, muestra efectiva (primer y último trimestre), número de observaciones, número de parámetros, R² y R² ajustado, error estándar de la regresión, rezagos de la ventana HAC, si se aplicó truncamiento espectral al sub-bloque sin dummies de impulso y, si hay dummies de impulso, la nota «rango reducido por dummies de impulso (esperado)».
- RF-10: EL SISTEMA producirá una tabla de efectos con, por regresor macro (β₁–β₅), el efecto de impacto y el de largo plazo, cada uno por 1 pp del regresor y por 1 DE. De cada efecto dará el error (HAC en el impacto, delta en el largo plazo), el p-valor y el IC 95 %, en pp de morosidad. SI 1 − ρ̂ ≤ 0,05, ENTONCES la tabla mostrará solo el efecto de impacto y el largo plazo como «no reportado (1 − ρ ≤ 0,05)».
- RF-11: EL SISTEMA producirá un gráfico de coeficientes con el efecto de impacto por 1 DE de cada regresor macro y su IC 95 %, con:
  - una línea vertical en cero;
  - ejes y títulos en español;
  - la unidad «pp de morosidad por 1 DE» en el eje;
  - el pie «Fuente: FRED; elaboración propia».

### Diagnósticos
- RF-12: EL SISTEMA producirá una tabla de diagnósticos de la especificación principal con estadístico, p-valor y veredicto de cada prueba. Veredicto: «pasa» si p ≥ 0,05 y «falla» si p < 0,05; para el VIF, «alerta» si > 10 y «sin alerta» en otro caso. Pruebas:
  - Breusch-Godfrey con 4 rezagos.
  - Breusch-Pagan (versión studentizada de Koenker), con todos los regresores del modelo.
  - White, con los regresores, sus cuadrados y sus productos cruzados, eliminando las columnas duplicadas o constantes (los cuadrados de las dummies).
  - Jarque-Bera.
  - RESET de Ramsey con la segunda y la tercera potencia de los valores ajustados (prueba F).
  - VIF de cada regresor, excepto la constante y las dummies.
  - Chow en 2008T3 y en 2020T2.
  - CUSUM.
- RF-13: EL SISTEMA aplicará cada prueba de Chow como una prueba de Wald con la covarianza HAC sobre la especificación principal en la muestra completa, añadiendo la interacción de un indicador «t ≥ trimestre de quiebre» con la constante, ρ y β₁–β₅. Las dummies COVID se mantienen sin interactuar. H0: todas las interacciones valen 0. El pie de la tabla lo describe así.
- RF-14: EL SISTEMA calculará el CUSUM de los residuos recursivos (Brown, Durbin y Evans) con bandas al 5 %. El veredicto será «falla» si la trayectoria cruza las bandas en algún trimestre y «pasa» en otro caso. Producirá además su gráfico, en español y con fuente.
- RF-15: EL SISTEMA producirá una tabla de estacionariedad del modelo con la dependiente y cada regresor en la forma en que entran. Columnas: columna del panel, forma, estadísticos y p-valores de ADF y KPSS tomados de la tabla de la spec 001, decisión, orden de integración y la marca «no I(0)» cuando corresponda. Para ΔU y ΔFFR, la decisión sale de aplicar la regla de la spec 001 a sus filas «primera diferencia». Esta tabla no se calcula para la muestra de R8.

### Robusteces
- RF-16: EL SISTEMA estimará R1–R8 con el mismo estimador y las mismas reglas de ventana HAC y de matriz no definida positiva. Producirá una tabla con una fila por regresión de robustez y regresor macro, con:
  - la variante y, en R3, la sub-cartera;
  - la dependiente y su forma, y los términos añadidos o quitados respecto de la principal;
  - la muestra efectiva, el número de observaciones y los rezagos HAC;
  - el coeficiente, el error HAC y el p-valor;
  - o bien el estado «no estimada» con su motivo.

  En R3 la unidad es pp del cambio de la morosidad de cada sub-cartera, como en la principal. En R5 no se expresa en pp, porque el logit no está en pp: solo se evalúan signo y significancia.
- RF-17: EL SISTEMA producirá una tabla de robustez con una fila por regresor macro y una columna por regresión de robustez (R1, R2, R3 con una columna por sub-cartera, R4, R5, R6, R7 y R8: diez en total). Cada celda dirá «sí», «no» o «no estimada», según el criterio pre-registrado. Por regresor, la tabla traerá un recuento «k de n», donde n es el número de regresiones de robustez estimadas.

### Validación fuera de muestra
- RF-18: EL SISTEMA producirá una tabla fuera de muestra con:
  - RMSE y MAE (pp) del modelo y del ingenuo, a un paso y dinámico;
  - el cociente RMSE modelo/ingenuo de cada pronóstico;
  - el estadístico y el p-valor de Diebold-Mariano del pronóstico a un paso;
  - el número de trimestres evaluados;
  - el veredicto pre-registrado de cada pronóstico.
- RF-19: EL SISTEMA producirá un gráfico de la morosidad observada frente a los pronósticos a un paso y dinámico y al ingenuo, en 2022T1–2026T2, en español, en pp y con fuente.

### Limitaciones, desviaciones y variables para el informe
- RF-20: EL SISTEMA producirá una tabla de limitaciones declaradas, que incluirá siempre:
  - la endogeneidad de la tasa de fondos federales;
  - la simultaneidad de los regresores contemporáneos;
  - los regresores marcados «no I(0)» en RF-15;
  - las dependientes con orden «posible I(2)»;
  - la potencia baja de Diebold-Mariano con pocos trimestres;
  - los efectos base de las tasas interanuales fuera de la ventana COVID: el PIB interanual de 2021T2–2022T1 (rebote sobre la caída de 2020) y el crecimiento del crédito asociado al programa PPP, que entra en CRED(t−4) entre 2021T2 y 2022T1. No llevan dummy, y la robustez R1 (sin 2020–2021) sirve de contraste.

  Además, incluirá cada diagnóstico con veredicto «falla» o «alerta» y cada truncamiento espectral aplicado al sub-bloque sin dummies de impulso. La reducción de rango por dummies de impulso no figura como limitación.
- RF-21: EL SISTEMA producirá una tabla de desviaciones y decisiones frente a la guía y a las reglas del proyecto, con:
  - el PIB real (GDPC1) como principal en lugar del GDP nominal de la guía, que queda como R4;
  - la muestra hasta 2026T2, cuando el ejemplo de la guía corta en 2026-01-01;
  - la muestra larga desde 1985 fuera del período 2000–2026 de la guía, y su estado (estimada o no);
  - los regresores con forma fija frente a la regla de estacionariedad de la skill;
  - ΔFFR como variable única para las secciones 3.3 y 3.4 de la guía;
  - cualquier entrada que se añada a «Desviaciones del pre-registro».
- RF-22: EL SISTEMA escribirá en las variables del informe, todas bajo el prefijo `modelo1.` (las claves exactas se fijan en el plan), lo siguiente:
  - **Inventario de la especificación:** estimador, forma de Y, número de parámetros, trimestres de las dummies COVID, lista y nombre de las variantes R1–R8, muestra efectiva y número de observaciones, y rezagos HAC.
  - **Por término de la tabla principal:** coeficiente, error HAC, p-valor e IC 95 %; además, R² y R² ajustado.
  - **Por regresor macro:** impacto y largo plazo por 1 pp y por 1 DE, con IC 95 % y p-valor, en pp de morosidad, y la coincidencia de signo. Un efecto no reportado o no definido va como texto («no reportado (1 − ρ ≤ 0,05)» o «no definido»), nunca como número.
  - **Por diagnóstico:** estadístico, p-valor y veredicto.
  - **Robustez:** el recuento «k de n» por regresor, y la muestra y el número de observaciones de cada variante.
  - **Fuera de muestra:** RMSE, MAE, cocientes, p-valor de Diebold-Mariano y veredictos.
  - **Listas:** los regresores no I(0), las limitaciones de RF-20 y las desviaciones de RF-21.

  Ninguna de estas cifras se escribe a mano en el informe.
- RF-23: EL SISTEMA producirá cada tabla en Markdown (para incluirla en el informe) y en CSV, y cada figura en PNG con pie y fuente («Fuente: FRED; elaboración propia»), desde la etapa de modelos del pipeline, que también corre dentro de `all`.

## Requisitos no funcionales
- RNF-1 (pre-registro): esta spec se aprueba y se commitea antes de la primera estimación con datos reales, en un commit que solo contiene los archivos de `specs/003-modelo-i/`; ese commit es la prueba del pre-registro.
- RNF-2 (tests del estimador): con un proceso simulado de coeficientes conocidos y semilla fija, la estimación recupera todos los coeficientes dentro de una tolerancia declarada en el plan. Con errores AR(1) de coeficiente positivo (0,7) y un regresor persistente (AR(1) con 0,8), el error HAC del coeficiente de ese regresor supera al error MCO clásico, con la semilla fija declarada en el plan.
- RNF-3 (tests de efectos y validación): tienen al menos un test con datos sintéticos y un valor de referencia calculado a mano o en forma cerrada:
  - el efecto de largo plazo y su error delta;
  - el umbral 1 − ρ ≤ 0,05;
  - el truncamiento espectral;
  - la reconstrucción del nivel desde diferencias, a un paso y dinámica;
  - el pronóstico ingenuo;
  - Diebold-Mariano con la corrección de Harvey, Leybourne y Newbold;
  - el criterio de robustez;
  - el recuento «k de n».
- RNF-4 (tests de diagnósticos): con semilla fija, Breusch-Godfrey rechaza (p < 0,05) con errores AR(1) simulados de coeficiente 0,7 y no rechaza con errores independientes. La prueba de Chow rechaza con un quiebre simulado en las pendientes y no rechaza sin él.
- RNF-5 (reproducibilidad): dos corridas del pipeline sobre los mismos datos congelados producen tablas, figuras y variables sin diferencias en `git diff` (figuras sin marcas de tiempo en sus metadatos).
- RNF-6 (sin red, lógica separada): los tests no usan la red; la estimación, los diagnósticos, los efectos y los pronósticos son funciones puras sin red, disco ni gráficos (principios 3 y 4).
- RNF-7 (lenguaje): un test revisa las tablas y las variables de texto generadas por esta spec y falla si aparece «causa», «causal», «provoca» o «debido a». Los nombres técnicos «efecto de impacto» y «efecto de largo plazo» están permitidos (Definiciones).
- RNF-8 (idioma): etiquetas de tablas y gráficos en español; código en inglés.

## Casos límite
- **Una dependiente sale «ambigua»** (es el caso de DRALACBS): entra en primera diferencia, y el largo plazo se interpreta como acumulado sobre el nivel.
- **1 − ρ̂ ≤ 0,05:** se reporta solo el impacto (RF-10).
- **El sub-bloque de la covarianza HAC sin dummies de impulso no es numéricamente definido positivo:** se aplica truncamiento espectral y se declara (Definiciones, RF-20). La reducción de rango por las dummies de impulso es esperada y solo se anota en el pie.
- **Efectos base en 2021T2–2022T1:** el rebote interanual del PIB y el crédito del PPP rezagado entran sin dummy y se declaran como limitación (RF-20). No se añaden dummies; R1 es el contraste.
- **Un regresor tiene el signo contrario al esperado:** se reporta «no» en la coincidencia y se discute en la spec 006. No se quita el regresor ni se cambia su forma.
- **Breusch-Godfrey rechaza con el rezago de la dependiente:** se declara la posible inconsistencia de MCO como limitación. Añadir rezagos después de ver el resultado exige un `/sdd-change`.
- **Algún regresor tiene VIF > 10:** se reporta la alerta y no se elimina ningún regresor.
- **Una dependiente alternativa empieza tarde o termina antes del último trimestre común** (por ejemplo, el faltante terminal de la spec 001): su variante usa su propio inicio o fin efectivo y lo declara. Un faltante interno ya lo detiene la spec 001 al construir el panel.
- **Una robustez no alcanza los grados de libertad mínimos:** figura como «no estimada» (RF-6).
- **R8 sin historia anterior a 2000T1:** figura como «no estimada» (RF-5).
- **2025T4 con CPI y desempleo promediados con dos meses** (spec 001): afecta a π y ΔU en la principal y en todas las variantes, y entra como cualquier otro trimestre. La nota de datos ya lo declara.
- **Pocos trimestres en el tramo fuera de muestra** (18): Diebold-Mariano tiene poca potencia y se declara (RF-20).
- **Una nueva descarga de FRED**, que cambie el último trimestre o solo valores históricos: los datos están congelados. Cualquier descarga nueva que deba usarse pasa por un `/sdd-change` de la spec 001 y de esta spec, y se registra en «Desviaciones del pre-registro».
- **Un `/sdd-change` de la spec 001 cambia la tabla de estacionariedad:** RF-4 detiene el pipeline si cambia alguna forma.

## Fuera de alcance
- Modelo II, rezagos distribuidos de la tasa, efecto acumulado con Wald, proyecciones locales y selección de rezagos por AIC/BIC (spec 004).
- Escenarios de estrés y simulación de coeficientes (spec 005).
- Redacción de la interpretación, de la discusión desde la gestión de riesgos y de la comparación con la literatura (spec 006).
- Ampliar la descarga de FRED antes de 1998 (si se quiere, `/sdd-change` de la spec 001; esta spec no lo exige).
- Recalcular ADF/KPSS sobre muestras distintas de 2000T1–2026T2.
- Variables instrumentales, VAR, cointegración, modelos con quiebres o con coeficientes cambiantes.
- Eliminar regresores no significativos o añadir regresores no listados después de ver resultados.
- Datos de vintages (ALFRED) o de otros países.

## Criterios de finalización
- Spec aprobada y commiteada antes de la primera estimación (RNF-1).
- Existen, en Markdown y CSV o PNG según corresponda, las salidas de RF-8 a RF-21:
  - la tabla de coeficientes, la de efectos y el gráfico de coeficientes;
  - el archivo de coeficientes y covarianza para la spec 005;
  - la tabla de diagnósticos y el gráfico CUSUM;
  - la tabla de estacionariedad del modelo;
  - las dos tablas de robustez;
  - la tabla y el gráfico fuera de muestra;
  - la tabla de limitaciones y la de desviaciones.
- Las variables `modelo1.*` de RF-22 existen en las variables del informe.
- R6 y R7 están estimadas o reportadas con su inicio efectivo, y R8 está estimada o reportada como «no estimada» con su motivo.
- `uv run python -m src.pipeline all` reproduce todo desde un clon limpio, y dos corridas no dejan diferencias (RNF-5).
- `uv run pytest -q` en verde, sin red.
- `specs/003-modelo-i/review-validate.md` y `specs/003-modelo-i/review-audit.md` con `VEREDICTO: APROBADO`.

## Desviaciones del pre-registro
- 2026-10-05 · `/sdd-change` tras la auditoría del plan (`review-plan.md`), **antes de cualquier estimación con datos reales** (pre-registro original: commit `667b313`).
  - (C1) La DE de los efectos «por 1 DE» excluye 2020T2–2021T1. Motivo: con esos trimestres la DE de ΔU sería unas 3,4 veces la de un trimestre típico (1,05 frente a 0,31 pp).
  - (C2) Los efectos base de 2021T2–2022T1 (PIB interanual y crédito del PPP) se declaran como limitación fija, con R1 como contraste y sin nuevas dummies. Motivo: son puntos de alto apalancamiento que la ventana COVID no cubre.
  - (C3) La comprobación de matriz no definida positiva se acota al sub-bloque sin dummies de impulso, y la reducción de rango por esas dummies se reporta como esperada. Motivo: es una propiedad algebraica de las dummies de impulso (residuo nulo), no un fallo numérico.

## Dependencias externas (no bloquean esta spec)
- La aceptación de la muestra larga por el profesor está pendiente (`MEMORY.md`). R8 es condicional y ya figura en la tabla de desviaciones (RF-21), así que la respuesta no cambia esta spec.

## Dudas abiertas
(ninguna)
