# Plan: Macro, política monetaria y riesgo de crédito

Oct 2, 2026 · @Gabriel Read

## Resumen

Recomiendo un solo repositorio reproducible donde los agentes ejecutan y tú decides: cada fase cierra con un artefacto verificable y una decisión anotada. Claude Code es el recurso escaso y se reserva para lo que es caro hacer mal; los modelos gratuitos hacen el trabajo repetitivo.

Decisiones clave:

- **Claude Code para lo crítico:** especificación, revisión econométrica y redacción final. OpenCode con modelos gratis para código repetitivo, gráficos y formato.
- **Especificación pre-registrada:** variables, transformaciones, rezagos y signos esperados quedan escritos antes de estimar. Es tu mejor defensa ante "¿por qué ese modelo?".
- **Frecuencia trimestral, 2000T1–2026T2 (106 trimestres):** la variable dependiente (DRALACBS) es trimestral; las series mensuales se promedian por trimestre.
- **Inferencia robusta:** pruebas de raíz unitaria para decidir niveles o diferencias, y errores Newey-West en todos los modelos.
- **Modelo II con dos métodos:** rezagos distribuidos (lo que pide la guía) y proyecciones locales de Jordà como robustez, que además dan el mejor gráfico de la exposición.
- **Dos escenarios de estrés:** el severamente adverso oficial de la Fed 2026 y uno estanflacionario con alza de tasas, que es el que describe el profesor.
- **Una sola fuente para informe y diapositivas:** Quarto genera el Word/PDF en APA y la presentación desde el mismo código, así ningún número se copia a mano.
- **Cero citas sin DOI verificado.**

## Roles del stack

Regla de reparto: el grueso del volumen va a modelos gratuitos y Claude Code se guarda para donde un error invalida la investigación.

| Herramienta | Rol | Costo y límite | Úsala para |
| --- | --- | --- | --- |
| Claude Code (Pro) | Arquitecto y revisor | Ventana móvil de 5 horas + tope semanal, compartidos con el chat de claude.ai ([fuente](https://www.fast.io/resources/claude-code-usage-limits-guide.md)) | Plan de cada fase, especificación, revisión de resultados, discusión y conclusiones |
| OpenCode | Ejecutor | Gratis con modelos Zen gratuitos, Gemini (AI Studio), OpenRouter `:free` o Copilot Student ([fuente](https://pub.towardsai.net/how-to-use-opencode-for-free-in-2026-90791d1a6d84)) | Scripts de datos, gráficos, tablas, formato, pruebas |
| Cursor (Hobby) | Editor y visor | Peticiones de agente y autocompletado limitados | Leer y editar código y notebooks; correr Claude Code en su terminal |
| Orca | Harness (donde se lanzan Claude Code y OpenCode) | Gratis | `git`, `uv`, `quarto`; los agentes corren dentro de Orca |
| GitHub | Memoria del proyecto | Gratis | Un issue por fase, una rama y un PR por fase, historial auditable |

Cómo estirar Claude Code:

- Empieza cada tarea en modo plan y aprueba antes de que ejecute; usa `/clear` entre tareas para no arrastrar contexto.
- Sonnet por defecto; el modelo más potente solo para revisar econometría y la discusión final.
- Antes de cerrar sesión, pide que actualice `docs/estado.md` (qué se hizo, qué sigue). Otra sesión u OpenCode retoma desde ahí sin repetir contexto.
- Este chat de claude.ai consume el mismo cupo: planifica aquí lo grande y deja el día a día para la terminal.
- Confirma que no exista `ANTHROPIC_API_KEY` en tu entorno; si existe, Claude Code la usa en vez de tu suscripción.

Tres advertencias:

- **No conectes tu cuenta Claude Pro a OpenCode.** Anthropic prohíbe usar los tokens de suscripción en herramientas de terceros ([febrero 2026](https://gigazine.net/gsc_news/en/20260220-anthropic-third-party-block)) y lo aplica desde el 4 de abril de 2026 ([fuente](https://falcao.org/posts/anthropic-claude-access-crackdown-ecosystem-fallout/)).
- **Los modelos gratuitos de Zen pueden usar tus prompts para entrenar.** Aquí no importa porque FRED es público, pero no metas datos personales ni del trabajo en ese flujo.
- **Copilot Student sigue siendo gratis para estudiantes verificados**, pero desde marzo de 2026 ya no deja elegir manualmente modelos premium ([fuente](https://roboin.io/article/en/2026/03/13/github-copilot-student-plan-removes-direct-access-to-premium-models/)), y las altas nuevas estaban pausadas desde el 20 de abril de 2026 ([GitHub Docs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-teachers-and-os-maintainers)). Verifica si tu cuenta INTEC califica hoy.

## Repositorio y reglas para los agentes

**Actualizado el 2 de octubre:** esta estructura la reemplaza el diseño SDD de Playbook agéntico SDD: riesgo de crédito. `docs/pap.md` pasa a ser la sección de pre-registro de cada `spec.md`; `docs/decisiones.md` y `docs/estado.md` se unen en `MEMORY.md`; y el Makefile se sustituye por `uv run python -m src.pipeline`, porque Windows no trae `make`.

Un archivo de reglas común (`AGENTS.md`) lo leen OpenCode y Cursor; `CLAUDE.md` lo importa con `@AGENTS.md` y añade lo propio de Claude Code. Así hay una sola fuente de verdad para los tres agentes.

```text
riesgo-credito-macro/
├── AGENTS.md                 # reglas comunes para todos los agentes
├── CLAUDE.md                 # @AGENTS.md + reglas propias de Claude Code
├── .claude/agents/           # subagentes: revisor-econometrico, verificador-citas, auditor-datos
├── .claude/commands/         # /fase, /revisar, /diagnosticos
├── pyproject.toml, uv.lock   # versiones fijadas con uv
├── config/series.yaml        # series, transformaciones y fechas: única fuente de verdad
├── data/raw/                 # descarga de FRED con fecha; nadie la edita
├── data/processed/
├── src/                      # fetch.py, transform.py, models.py, diagnostics.py, stress.py
├── notebooks/                # notebook del profesor + exploración
├── tests/                    # pruebas de datos y de modelos
├── docs/pap.md               # especificación pre-registrada
├── docs/decisiones.md        # bitácora: fecha, decisión, alternativa, por qué
├── docs/estado.md            # relevo entre sesiones
├── outputs/tables/, outputs/figures/
├── report/informe.qmd, report/slides.qmd, references.bib, apa.csl
└── Makefile                  # make data | models | stress | report | all
```

Reglas que van en `AGENTS.md`:

1. Ningún número del informe se escribe a mano: todo sale de `outputs/`, generado por código.
2. Ningún agente cambia `docs/pap.md`. Si propone un cambio, lo anota en `docs/decisiones.md` y espera tu aprobación.
3. Toda referencia lleva DOI o URL verificada; sin verificación no entra.
4. `data/raw/` es de solo lectura.
5. Una rama y un PR por fase; commits pequeños con mensaje descriptivo.
6. `make all` desde un clon limpio reproduce todo: datos, modelos, figuras, informe y diapositivas.

Subagentes de Claude Code (cada uno con contexto limpio, para que no se califique su propio trabajo):

- **auditor-datos:** fechas, faltantes, frecuencias, saltos y valores atípicos.
- **revisor-econometrico:** estacionariedad, errores HAC, signos, interpretación y sobreajuste.
- **verificador-citas:** cruza cada referencia contra Crossref u OpenAlex (APIs gratuitas, sin clave).

## Datos

Todo se lleva a frecuencia trimestral porque la variable dependiente lo es: [DRALACBS](https://fred.stlouisfed.org/series/DRALACBS) es la tasa de morosidad de todos los préstamos de bancos comerciales, en %, desestacionalizada y medida a fin de trimestre; va de 1985T1 a 2026T2 (último dato: 1.42%).

| Concepto | Serie FRED | Transformación trimestral | Nota |
| --- | --- | --- | --- |
| Riesgo de crédito | DRALACBS | Nivel; Δ o logit ln(DR / (100 − DR)) según pruebas | Robustez: DRALACBN (sin desestacionalizar) y sub-carteras DRCLACBS, DRBLACBS, DRSREACBS |
| PIB | GDPC1 (real) como principal; GDP (nominal) como robustez | Crecimiento interanual del log | El PIB nominal mezcla crecimiento con inflación, que ya entra como regresor |
| Desempleo | UNRATE | Promedio trimestral; nivel o Δ | Falta octubre 2025 |
| Inflación | CPIAUCSL | Promedio trimestral → variación interanual % | Falta octubre 2025 |
| Política monetaria | FEDFUNDS | Promedio trimestral; Δ en puntos | Casi sin variación en 2009–2015 y 2020–2021 |
| Crédito | [LOANS](https://fred.stlouisfed.org/series/LOANS) (préstamos y arrendamientos, bancos comerciales, mensual) | Crecimiento interanual del log | Alternativa: BUSLOANS (comerciales e industriales) |

Problemas conocidos y cómo tratarlos:

- **El código del profesor depende de la versión.** pandas-datareader 0.11.0 restauró la compatibilidad con pandas 3 ([release](https://github.com/pydata/pandas-datareader/releases/tag/v0.11.0)); fija `pandas-datareader>=0.11` en `pyproject.toml`. Respaldo sin clave: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIE>`.
- **Octubre 2025 no existe en CPI ni en desempleo.** Por el cierre del gobierno, el BLS no publicó el CPI general de ese mes ([BLS](https://www.bls.gov/cpi/additional-resources/2025-federal-government-shutdown-impact-cpi.htm)) ni el informe de empleo. Promedia 2025T4 con dos meses y documéntalo en `decisiones.md`.
- **Mezcla de medidas de tiempo.** La morosidad es dato de cierre; las series mensuales serán promedios. Decide si el crédito va a cierre o promedio y anótalo.
- **Revisiones de datos.** Guarda la descarga en `data/raw/` con fecha; FRED revisa series y tus resultados deben poder repetirse.
- **COVID rompe la relación.** En 2020T2 el desempleo saltó a cerca de 13% sin que la morosidad respondiera en proporción, por moratorias y estímulos. Usa variables dicotómicas en 2020T2–2021T1 y una robustez sin ese periodo.
- **Muestra corta.** 106 trimestres se consumen rápido con rezagos. Como robustez, extiende a 1985T1–2026T2 (166 trimestres), que incluye más ciclos de alzas de tasas.

## Especificación pre-registrada

Se pre-registra la regla de decisión, no el resultado: si ADF y KPSS indican que la morosidad no es estacionaria, los modelos van en diferencias como abajo; si es estacionaria, en niveles con la morosidad rezagada. Todo queda en `docs/pap.md` antes de la primera estimación.

### Modelo I: determinantes macroeconómicos

```latex
\Delta DR_t = \alpha + \rho\,\Delta DR_{t-1} + \beta_1 g_t + \beta_2 \Delta U_t + \beta_3 \pi_t + \beta_4 \Delta i_t + \beta_5 c_{t-4} + \delta D^{COVID}_t + \varepsilon_t
```

DR es la morosidad, g el crecimiento del PIB real, U el desempleo, π la inflación, i la tasa de fondos federales y c el crecimiento del crédito con un año de rezago (se prueban 4, 8 y 12 trimestres). Estimación por MCO con errores Newey-West.

| Variable | Signo esperado | Mecanismo |
| --- | --- | --- |
| Crecimiento del PIB real | − | Más ingreso y empleo, menos impagos |
| Cambio en desempleo | + | Pérdida de ingreso de los hogares |
| Inflación | Ambiguo | Erosiona el ingreso real, pero licúa la deuda nominal |
| Cambio en la tasa | + | Encarece el servicio de deuda a tasa variable |
| Crédito rezagado | + | Los booms relajan los estándares de otorgamiento |

### Modelo II: política monetaria y efectos rezagados

```latex
\Delta DR_t = \alpha + \sum_{k=0}^{K} \gamma_k \Delta i_{t-k} + \rho\,\Delta DR_{t-1} + \theta' X_{t-1} + \varepsilon_t
```

K se elige por AIC y BIC con un máximo de 8 trimestres (dos años). Se reporta el efecto acumulado Σγ con prueba de Wald, el trimestre de efecto máximo y una prueba de causalidad de Granger.

Robustez con proyecciones locales, una regresión por horizonte h:

```latex
DR_{t+h} - DR_{t-1} = \alpha_h + \beta_h \Delta i_t + \phi_h' X_{t-1} + u_{t+h}, \quad h = 0, 1, \dots, 12
```

Los β\_h con bandas HAC al 90% forman la respuesta de la morosidad a un alza de tasas: es el gráfico central del Modelo II.

Límite que debes declarar: el cambio en la tasa no es un choque puro, porque la Fed reacciona a la economía. Los controles lo atenúan, pero el resultado se presenta como asociación dinámica, no como efecto causal. Para el periodo de tasa cero (2009–2015), una robustez reemplaza la tasa por la tasa sombra de Wu y Xia.

## Diagnósticos y robustez

Cada modelo pasa la misma batería, empaquetada en `src/diagnostics.py` para que el subagente revisor la corra igual en ambos modelos. Todo está en statsmodels, sin costo.

| Prueba | Qué detecta | Función en statsmodels |
| --- | --- | --- |
| ADF y KPSS | Raíz unitaria (decide niveles o diferencias) | `adfuller`, `kpss` |
| Breusch-Godfrey | Autocorrelación de residuos | `acorr_breusch_godfrey` |
| Breusch-Pagan y White | Heterocedasticidad | `het_breuschpagan`, `het_white` |
| Jarque-Bera | Normalidad de residuos | `jarque_bera` |
| VIF | Multicolinealidad entre regresores | `variance_inflation_factor` |
| RESET de Ramsey | Forma funcional | `linear_reset` |
| CUSUM y Chow | Estabilidad y quiebres en 2008 y 2020 | `breaks_cusumolsresid`; Chow con el estadístico F |
| Newey-West | Inferencia válida con autocorrelación y heterocedasticidad | `fit(cov_type="HAC")` |

Pruebas de robustez, cada una con su tabla en el anexo:

- Muestra 1985T1–2026T2.
- Excluir 2020–2021.
- Morosidad sin desestacionalizar (DRALACBN).
- Sub-carteras: consumo, empresas, bienes raíces.
- PIB nominal en lugar de real.
- Logit de la morosidad en lugar del nivel.
- Tasa sombra en el periodo de tasa cero.
- **Validación fuera de muestra:** estimar hasta 2019T4 y pronosticar 2022T1–2026T2, comparando el error contra un paseo aleatorio. Es la prueba que más le importa a un gestor de riesgo, porque mide si el modelo sirve para anticipar.

## Escenarios y prueba de estrés

Propongo tres escenarios sobre las mismas fechas que usa la Fed: punto de partida 2025T4 y 13 trimestres, de 2026T1 a 2029T1 ([Fed, 2026 Stress Test Scenarios](https://www.federalreserve.gov/publications/2026-stress-test-scenarios.htm)). Usar sus fechas hace el ejercicio citable y comparable.

| Escenario | Desempleo | PIB real | Tasa corta | Origen |
| --- | --- | --- | --- | --- |
| Base | Sube a 4.6% y baja a 4.2% al final | Crece alrededor de 2.1% | Tesoro a 3 meses de 3.7% a 3.1% | Escenario base oficial de la Fed |
| A. Severamente adverso | De 4.5% a un pico de 10% en 2027T3 | Cae 4.6% hasta 2027T2 | Tesoro a 3 meses cae a 0.1% en 2026T2 y ahí se queda | Escenario oficial de la Fed |
| B. Estanflación | Misma trayectoria que A | Misma trayectoria que A | Sube en lugar de bajar; magnitud a calibrar con el ciclo 2022–2023 | Propuesta propia, la que describe el profesor |

El diseño de B es deliberado: copia el desempleo y el PIB de A y solo invierte la tasa. La diferencia entre A y B aísla cuánto aporta la política monetaria al deterioro de la cartera, que es justo la pregunta del Modelo II. La Fed no publica la tasa de fondos federales en sus escenarios; el Tesoro a 3 meses sirve como aproximación porque se mueven casi juntos.

Pasos del cálculo:

1. Proyectar la morosidad trimestre a trimestre con los coeficientes estimados (proyección recursiva).
2. Calcular el cambio contra la base en cada trimestre, el pico y el trimestre del pico.
3. Simular incertidumbre con extracciones de los coeficientes según su matriz de covarianza HAC; reportar bandas de 90%.
4. Traducir a dinero como orden de magnitud: con préstamos de bancos comerciales por cerca de US$14.0 billones (agosto 2026, [LOANS](https://fred.stlouisfed.org/series/LOANS)), cada punto de morosidad equivale a unos US$140,000 millones en préstamos morosos. Morosidad no es pérdida; la tasa de castigos (CORALACBS) sirve como extensión.

## Revisión de literatura

Los agentes inventan citas con facilidad, así que ninguna entra sin pasar por este flujo:

1. El agente busca en OpenAlex, Crossref o Semantic Scholar (gratis, sin clave) y propone candidatos con DOI.
2. El subagente verificador-citas confirma que el DOI existe y que título, autores y año coinciden.
3. La referencia entra a Zotero (gratis) y se exporta a `references.bib`; Quarto aplica APA 7 con `apa.csl`.
4. Tú lees al menos el resumen de cada estudio que uses para un argumento central.

Para la sección 2.5, el entregable es una matriz de literatura con estas columnas: autor y año, país y muestra, variable dependiente, regresores, método y hallazgo principal. Esa matriz responde exactamente lo que pide el profesor.

Lista semilla (todas pasan por el flujo de verificación antes de citarse):

| Estudio | Sección | Qué aporta |
| --- | --- | --- |
| Bernanke y Gertler (1995), *Journal of Economic Perspectives* | 2.3, 2.4 | Canal de crédito de la política monetaria |
| Bernanke, Gertler y Gilchrist (1999), *Handbook of Macroeconomics* | 2.1 | Acelerador financiero |
| Wilson (1997), *Risk* | 2.1, 7 | Modelo de morosidad condicionada al ciclo (CreditPortfolioView) |
| Salas y Saurina (2002), *Journal of Financial Services Research* | 2.2 | Determinantes macro y bancarios de la morosidad |
| Jiménez y Saurina (2006), *International Journal of Central Banking* | 2.2 | Los booms de crédito anticipan morosidad años después |
| Virolainen (2004), Banco de Finlandia | 7 | Prueba de estrés macro de riesgo de crédito |
| Nkusu (2011), FMI Working Paper | 2.2, 2.5 | Morosidad y vulnerabilidades macrofinancieras en economías avanzadas |
| Louzis, Vouldis y Metaxas (2012), *Journal of Banking & Finance* | 2.5 | Determinantes por tipo de préstamo |
| Beck, Jakubik y Piloiu (2015), *Open Economies Review* | 2.5 | PIB, tasas y tipo de cambio en una muestra global |
| Ghosh (2015), *Journal of Financial Stability* | 2.5 | Estados de EE.UU.: desempleo y crédito; la más cercana a tu muestra |
| Borio y Zhu (2012), *Journal of Financial Stability* | 2.4 | Canal de toma de riesgo |
| Maddaloni y Peydró (2011), *Review of Financial Studies* | 2.4 | Tasas bajas relajan estándares de crédito |
| Jiménez, Ongena, Peydró y Saurina (2014), *Econometrica* | 2.4 | Política monetaria y toma de riesgo con datos de préstamos |
| Newey y West (1987), *Econometrica* | 3.5 | Errores estándar HAC |
| Jordà (2005), *American Economic Review* | 3.5 | Proyecciones locales |
| Wu y Xia (2016), *Journal of Money, Credit and Banking* | Robustez | Tasa sombra en el límite inferior cero |
| Comité de Basilea (2018), principios de pruebas de estrés | 7, 8 | Estándar regulatorio para el ejercicio |
| Reserva Federal (2026), *2026 Stress Test Scenarios* | 7 | Escenarios oficiales |

## Fases y puertas de control

&#91;embedded content: fases del proyecto · 7 fases, cada una con su puerta\]

Ninguna fase empieza hasta que la anterior pasa su puerta; la del pre-registro es la que nunca se salta. Las semanas de cada fase las fijo cuando confirmes la fecha de entrega. Con tu horario, las sesiones largas de Claude Code caben en las noches de lunes, martes y jueves y en el fin de semana; los modelos gratuitos cubren el resto.

## Entregable final: informe y diapositivas

Quarto (gratis) renderiza `report/informe.qmd` a Word o PDF con citas APA, y `report/slides.qmd` a PowerPoint o a presentación web. Ambos leen las mismas tablas y figuras de `outputs/`; si cambias un modelo, `make report` actualiza los dos.

Estructura sugerida para la exposición (12 diapositivas):

1. La pregunta y por qué le importa a un banco.
2. Morosidad, desempleo y tasa 2000–2026, con recesiones sombreadas.
3. Datos y método en una sola lámina.
4. Modelo I: gráfico de coeficientes con intervalos, en lugar de una tabla.
5. Modelo II: respuesta de la morosidad a un alza de tasas por trimestre (proyecciones locales).
6. Qué tan bien anticipa el modelo: pronóstico fuera de muestra contra lo observado.
7. Los tres escenarios en una tabla.
8. Trayectoria de la morosidad bajo base, A y B, con bandas.
9. Lo que aporta la tasa: diferencia entre A y B.
10. Implicaciones: tablero de alertas tempranas para un comité de riesgo.
11. Limitaciones: asociación y no causalidad, COVID, datos agregados.
12. Conclusión que responde la pregunta en una frase.

Al final, si prefieres un diseño más pulido que el de Quarto, puedo convertir el contenido en una presentación aquí en Claude y exportarla a PowerPoint.

## Riesgos del proyecto

El mayor riesgo no es técnico: es que un agente produzca algo plausible pero incorrecto y llegue a la exposición sin que nadie lo detecte.

| Riesgo | Señal | Mitigación |
| --- | --- | --- |
| Se agota la ventana de Claude Code a mitad de tarea | El agente se detiene sin terminar | Tareas cortas, commit al cerrar cada paso y relevo en `docs/estado.md` |
| Citas o cifras inventadas | Una referencia sin DOI o un número sin archivo de origen | Regla del DOI, números solo desde `outputs/` y subagente verificador |
| Buscar significancia hasta encontrarla | Cambios de especificación después de ver resultados | Pre-registro en `docs/pap.md`; todo cambio queda en la bitácora y se reporta |
| Errores silenciosos de un modelo gratuito | Resultados que cambian sin explicación | Pruebas en `tests/` y revisión de Claude Code de los cambios críticos |
| Dependencias rotas | El notebook del profesor no corre | Versiones fijadas con `uv.lock` y respaldo por CSV de FRED |
| COVID distorsiona los coeficientes | Residuos enormes en 2020 | Variables dicotómicas y robustez sin 2020–2021 |
| Prompts usados para entrenar en modelos gratuitos | Uso de la ruta Zen gratuita | Solo datos públicos; nada personal ni del trabajo |
| Exponer resultados que no entiendes | No puedes explicar un coeficiente sin mirar notas | Antes de cada puerta, explica el resultado en voz alta en dos minutos |

## Decisiones pendientes

- [ ] Fecha de entrega y si el trabajo es individual o en grupo; con eso fijo las semanas de cada fase.
- [ ] ¿El profesor exige 2000–2026 estricto, o acepta 1985–2026 como robustez?
- [ ] PIB real (GDPC1) como principal, o el nominal (GDP) que aparece en la guía.
- [ ] Formato exigido del informe (Word o PDF, extensión) y de la exposición (PowerPoint o libre).
- [ ] Revisar si tu cuenta de INTEC califica hoy para Copilot Student.
- [ ] Repositorio privado hasta la entrega, o público desde el inicio.

## Fuentes

- [FRED: DRALACBS](https://fred.stlouisfed.org/series/DRALACBS)
- [FRED: LOANS](https://fred.stlouisfed.org/series/LOANS)
- [Reserva Federal: 2026 Stress Test Scenarios](https://www.federalreserve.gov/publications/2026-stress-test-scenarios.htm)
- [BLS: impacto del cierre de 2025 en el CPI](https://www.bls.gov/cpi/additional-resources/2025-federal-government-shutdown-impact-cpi.htm)
- [pandas-datareader 0.11.0](https://github.com/pydata/pandas-datareader/releases/tag/v0.11.0)
- [Límites de uso de Claude Code](https://www.fast.io/resources/claude-code-usage-limits-guide.md)
- [Anthropic y el uso de suscripciones en herramientas de terceros](https://gigazine.net/gsc_news/en/20260220-anthropic-third-party-block)
- [Cronología de las restricciones a OpenCode](https://falcao.org/posts/anthropic-claude-access-crackdown-ecosystem-fallout/)
- [Usar OpenCode gratis en 2026](https://pub.towardsai.net/how-to-use-opencode-for-free-in-2026-90791d1a6d84)
- [Cambios a Copilot Student](https://roboin.io/article/en/2026/03/13/github-copilot-student-plan-removes-direct-access-to-premium-models/)
- [GitHub Docs: pausa de nuevas altas](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/enable-copilot/set-up-for-teachers-and-os-maintainers)
