# Playbook agéntico SDD: riesgo de crédito

Oct 2, 2026 · @Gabriel Read

Claude Code y OpenCode son los dos arneses, y la spec en `specs/` es el contrato entre ellos. Claude Code decide el QUÉ y audita (Sonnet por defecto, Opus en los pasos críticos). OpenCode, con LongCat 2.5 Preview en *high*, construye, prueba y valida. Cursor y GitHub no son arneses: son tu estación de revisión y la memoria auditable. Orca es el entorno que los aloja y lanza. Los archivos van en el ZIP `riesgo-credito-macro.zip` que te envié en el chat.

## Arneses y modelos

Hay dos arneses y tres herramientas de apoyo. Un arnés es el sistema que rodea al modelo y le deja actuar: gestiona el contexto, las herramientas y los permisos (día 1 del curso).

| Herramienta | ¿Es arnés? | Rol | Modelo | Esfuerzo | Qué hace en este proyecto |
| --- | --- | --- | --- | --- | --- |
| Claude Code (Pro) | Sí | Arquitecto y auditor | Sonnet por defecto; Opus (con /model opus en las entrevistas) en `/sdd-constitution`, `/sdd-spec`, `/sdd-resolve`, `/sdd-plan`, `/sdd-change` y `/redactar` | high en esos comandos | Constitución, specs, planes, auditorías y redacción de discusión y conclusiones |
| Subagentes de Claude Code | — | Revisores independientes | revisor-econometrico (Opus) · verificador-citas (Sonnet) · profesor-evaluador (Opus) | high en los de Opus | Auditan con contexto limpio: reciben rutas, nunca tu conclusión |
| OpenCode (v2) | Sí | Fábrica | LongCat 2.5 Preview Free: `opencode/longcat-2.5-preview-free#high` en los 5 agentes | high | Tareas, código, tests, validación técnica y búsqueda de literatura |
| Cursor (Hobby) | No | Estación de revisión y tutor | Auto (plan gratis) | — | Lees diffs, figuras y tablas, editas specs a mano y entiendes los resultados. Nunca edita código |
| Orca | Entorno | Harness que aloja y lanza a los dos arneses | — | — | Tres paneles: `claude`, `opencode` y una terminal libre para git, uv y Quarto |
| GitHub | No | Memoria auditable y puerta de calidad | — | — | Repositorio privado, una rama y un PR por spec; Actions corre `pytest` en cada push |

Notas sobre los modelos:

- **LongCat 2.5 Preview Free es gratis por tiempo limitado** y su proveedor sigue una política de cero retención: no entrena con tus datos ([OpenCode Zen](https://opencode.ai/docs/zen)). Esto corrige lo que te dije antes: de los modelos gratis de Zen, solo algunos usan tus prompts para entrenar.
- **La variante `#high` no la pude verificar.** Si OpenCode la rechaza, quita `#high` de `opencode.jsonc` y de los 5 agentes (buscar y reemplazar en Cursor) y sube el esfuerzo con Ctrl+T.
- **Respaldo si LongCat deja de estar disponible**: `opencode/nemotron-3-ultra-free` o `opencode/big-pickle`. Ambos pueden usar tus prompts para mejorar el modelo; aquí no importa porque los datos de FRED son públicos.
- **Cupo de Claude Pro**: el chat de claude.ai y Claude Code comparten la misma ventana de 5 horas y el mismo tope semanal. Revisa el consumo en claude.ai → Configuración → Uso. Confirma que no exista `ANTHROPIC_API_KEY` en tu entorno.
- **Nunca conectes tu cuenta de Claude a OpenCode**: Anthropic prohíbe usar la suscripción en herramientas de terceros. Por eso el reparto es por archivos, no por modelos compartidos.

## Arquitectura

&#91;embedded content: arquitectura · 2 arneses, 8 agentes, 1 repositorio compartido\]

Los dos arneses nunca se hablan directamente: se pasan el trabajo por archivos en `specs/`, y tú apruebas cada puerta desde Cursor antes del commit. Por eso puedes cambiar de modelo, de herramienta o de sesión sin perder el hilo.

## Mapa de orquestación

Cada paso del SDD tiene un solo dueño. Claude Code escribe y audita; OpenCode construye y valida. Los comandos nunca se ejecutan por iniciativa del agente: los lanzas tú (en Claude Code tienen `disable-model-invocation: true`).

| Paso SDD | Arnés | Comando | Agente que trabaja | Modelo | Archivo que sale |
| --- | --- | --- | --- | --- | --- |
| 1. Constitución (una vez) | Claude Code | `/sdd-constitution` | principal | Opus | `docs/constitution.md` |
| 2. Spec | Claude Code | `/sdd-spec` | principal | Opus | `spec.md` (borrador) |
| 3. Clarificación | OpenCode | `/sdd-clarify` | reviewer | LongCat | `review-clarify.md` |
| 3b. Resolución | Claude Code | `/sdd-resolve` | principal | Opus | `spec.md` (aprobada) |
| 4. Plan | Claude Code | `/sdd-plan` | principal + revisor-econometrico (críticas) | Opus | `plan.md`, `review-plan.md` |
| 5. Tareas | OpenCode | `/fabrica` (o `/sdd-tasks`) | coordinator → planner | LongCat | `tasks.md` |
| 6. Implementación | OpenCode | `/fabrica` (o `/sdd-implement`) | coordinator → implementer o bibliotecario | LongCat | `src/`, `tests/`, `outputs/`, `research/` |
| 6b. Redacción | Claude Code | `/redactar` | principal | Opus | `report/informe.qmd` |
| 7. Validación | OpenCode | `/fabrica` (o `/sdd-validate`) | coordinator → reviewer | LongCat | `review-validate.md` |
| 7b. Auditoría (003–006) | Claude Code | `/sdd-audit` | revisor-econometrico | Opus | `review-audit.md` |
| Mantenimiento | Claude Code | `/sdd-change` | principal | Opus | spec con desviaciones del pre-registro |
| Estado | OpenCode | `/sdd-status` | plan | LongCat | nada (solo lee) |
| Evaluación final | Claude Code | `/evaluar` | profesor-evaluador + verificador-citas | Opus y Sonnet | `review-final.md` |
| Cierre de sesión | Ambos | `/cierre` | principal o build | Sonnet o LongCat | `MEMORY.md` + commit |

La clarificación la hace OpenCode a propósito: un modelo distinto al que redactó la spec la revisa con otros ojos y sin gastar tu cupo de Claude.

Qué skill carga cada spec (los agentes la cargan solos cuando la descripción coincide; en OpenCode puedes forzarla con `@nombre-skill`):

| Skill | Specs | Para qué |
| --- | --- | --- |
| `sdd` | todas | Flujo, plantillas de spec, plan y tareas, formato de los informes de revisión |
| `datos-fred` | 001, 005 | Series, transformaciones, el hueco de octubre 2025, manifiesto de descargas |
| `citas-apa` | 002, 006 | Protocolo anti-citas-inventadas con OpenAlex y Crossref, matriz, BibTeX y APA 7 |
| `econometria-series-tiempo` | 003, 004, 005 | Estacionariedad, HAC, rezagos, proyecciones locales, estrés, checklist de revisión |
| `informe-quarto` | 006, 007 | Estructura de la guía, números vía `{{< var >}}`, reglas de redacción y diapositivas |

Las skills viven en `.claude/skills/` porque es la única carpeta que leen los dos arneses: así hay una sola copia. Los apuntes usan `.agents/skills/`, pero Claude Code no la lee.

## Calendario

&#91;embedded content: calendario · 7 specs del 3 al 15 de octubre\]

Apunta a entregar el jueves 15 antes de las 22:00; el cierre oficial es el viernes 16 a las 00:00. Las noches con clase solo dan para un comando corto (`/sdd-clarify`, `/sdd-status` o leer una revisión en Cursor). Las sesiones largas de Claude Code van el sábado por la tarde y los domingos, repartidas en dos ventanas de 5 horas (mañana y noche) para no topar el límite. Las specs 002 y 003 se solapan a propósito: la literatura corre en OpenCode mientras Claude Code redacta el pre-registro del Modelo I.

## Fase 0: puesta en marcha (sábado 3, unas 2 horas)

Termina con el repositorio en GitHub, los tests del arnés en verde y la constitución aprobada por ti.

1. **Instala lo que falte.** uv (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`. Quarto: instalador de quarto.org. Confirma que OpenCode es la v2 de los apuntes: los agentes usan la sintaxis `permissions` de la v2.
2. **Crea el repositorio.** Descomprime el ZIP y, en la terminal libre de Orca:

   ```bash
   cd riesgo-credito-macro
   git init -b main
   uv sync
   uv run pytest -q
   git add -A
   git commit -m "chore: arnés agéntico SDD"
   ```

   `uv run pytest -q` debe mostrar 9 tests en verde. Crea un repositorio privado en GitHub, conéctalo (`git remote add origin <url>`) y sube (`git push -u origin main`). En la pestaña Actions, el workflow `tests` debe salir en verde.
3. **Abre tres paneles en Orca** en la carpeta: `claude`, `opencode` y una terminal libre.
4. **Prueba OpenCode.** En `/models` elige LongCat 2.5 Preview Free. Con Tab debes ver `coordinator` junto a `build` y `plan`. Luego escribe `/sdd-status`: debe responder que no hay specs y que el siguiente paso es `/sdd-spec 001-datos` en Claude Code. Si lo dice, funcionan el comando, el agente `plan`, `AGENTS.md` y `MEMORY.md`.
5. **Prueba Claude Code.** Ejecuta `/context` y confirma que aparecen `CLAUDE.md` y `AGENTS.md` en Memory files. Escribe `/` y comprueba que salen los comandos `/sdd-*`, `/redactar`, `/evaluar` y `/cierre`, y las cinco skills.
6. **Revisa la constitución.** Ya viene redactada con 6 principios en 10 líneas. En Claude Code:

   ```text
   /sdd-constitution Revisa la constitución propuesta frente a la guía del profesor y a un plazo de 13 días. Dime si algún principio es inverificable o demasiado caro de cumplir.
   ```

   Aprueba o ajusta, y haz commit.
7. **Sobre `/init`: no lo corras ahora.** Con el repositorio vacío no hay nada que analizar, y `AGENTS.md` ya está escrito con la plantilla del curso (40 líneas). Al cerrar la spec 001, en una rama aparte, corre `/init` en OpenCode y compara el diff en Cursor; quédate solo con lo que sea cierto y sin pasar de 40 líneas.
8. **Cierra las decisiones pendientes de `MEMORY.md`** con el profesor si puedes: PIB real o nominal como principal, formato del informe (Word o PDF) y si acepta la muestra desde 1985 como robustez.
9. **Cierra la sesión** con `/cierre Fase 0 lista` en Claude Code.

## El ciclo de cada spec

Las siete specs siguen el mismo ciclo de 8 pasos; solo cambian la idea inicial y las decisiones (secciones siguientes). Antes de aprobar cualquier puerta, abre el archivo en Cursor y léelo tú: la IA ejecuta, pero el responsable eres tú.

**Modelo en las entrevistas.** El `model: opus` de un comando de Claude Code solo dura su primer turno, y `/sdd-spec` y `/sdd-resolve` conversan varios turnos. Antes del paso 2 escribe `/model opus`; al aprobar la spec en el paso 4, vuelve con `/model sonnet`. Los pasos 5 y 7 suben a Opus solos porque hacen el trabajo pesado en su primer turno.

1. **Terminal · rama de la spec.** `git switch -c spec/NNN-nombre`
2. **Claude Code · spec.** `/sdd-spec NNN-nombre <idea inicial>`. Responde sus preguntas una a una (máximo 5).
3. **OpenCode · clarificación.** `/sdd-clarify NNN-nombre`. El reviewer deja `specs/NNN-nombre/review-clarify.md`.
4. **Claude Code · resolución.** Decide cada punto y pásalos numerados:

   ```text
   /sdd-resolve NNN-nombre 1: sí, como propone el QA. 2: queda fuera de alcance. 3: usa la regla de la skill. 4: pregúntame.
   ```

   Revisa el diff y apruébalo: queda `Estado: aprobada` y un commit `spec(NNN-nombre): aprobada`.
5. **Claude Code · plan.** `/clear` y luego `/sdd-plan NNN-nombre`. En las specs críticas, el revisor-econometrico audita el plan antes de que lo veas y deja `review-plan.md`. Aprueba: `Estado: aprobada` y commit.
6. **OpenCode · fábrica.** Tab hasta `coordinator` y `/fabrica NNN-nombre`. El coordinador pide al planner las tareas y se detiene para que apruebes `tasks.md`. Luego reparte una tarea por vez, corre los tests tras cada una y termina con el reviewer, que deja `review-validate.md`. Si los tests quedan en rojo, se detiene y te avisa.
7. **Claude Code · auditoría (solo 003, 004, 005 y 006).** `/sdd-audit NNN-nombre`. Si sale CAMBIOS NECESARIOS, te devuelve una lista lista para pegar en OpenCode:

   ```text
   /fabrica NNN-nombre "Correcciones de review-audit.md: 1) … 2) …"
   ```

   Al aprobar, la spec queda `Estado: implementada`.
8. **Cierre.** `/cierre` en la herramienta que usaste al final, `git push -u origin spec/NNN-nombre`, PR en GitHub con la plantilla y merge cuando Actions esté en verde.

Si el coordinador se atasca, haz la fábrica a mano en OpenCode: `/sdd-tasks NNN-nombre`, después `/sdd-implement NNN-nombre T1`, `T2`… (una por mensaje) y al final `/sdd-validate NNN-nombre`.

Dos reglas para ahorrar cupo de Claude:

- Usa `/clear` entre la spec y el plan, y entre specs. La memoria vive en los archivos, no en la conversación.
- Corre `/sdd-status` en OpenCode (gratis) en lugar de preguntárselo a Claude.

## Specs 001 y 002: datos y literatura

### 001-datos (sábado 3 a domingo 4 · no crítica)

Prompt del paso 2, en Claude Code:

```text
/sdd-spec 001-datos Pipeline de datos reproducible para toda la investigación (secciones 3.1–3.4 y 11 de la guía). Descargar de FRED desde 1998-01-01 las series de la skill datos-fred (DRALACBS, DRALACBN, DRCLACBS, DRBLACBS, DRSREACBS, GDPC1, GDP, UNRATE, CPIAUCSL, FEDFUNDS, LOANS, CORALACBS y USREC), guardar cada descarga cruda con fecha y un manifiesto, y construir un panel trimestral desde 2000T1 hasta el último trimestre común con las transformaciones de la skill. Debe detectar y documentar el hueco de octubre 2025 en CPI y desempleo, y detenerse ante cualquier otro faltante. Salidas: panel procesado, tabla de estadísticos descriptivos, tabla de pruebas ADF y KPSS con la decisión niveles o diferencias de cada variable, y un gráfico de morosidad, desempleo y tasa de fondos federales 2000–2026 con recesiones sombreadas. Incluir un notebook de demostración que reproduzca el ejemplo de descarga de la guía (sección 11) y muestre el panel final. Si la descarga principal falla, usar el CSV público de FRED. Crítica: no.
```

Ten listas estas respuestas para la entrevista:

- **PIB principal**: recomiendo el real (GDPC1), con el nominal (GDP, el de la guía) como robustez. Si el profesor exige el nominal, invierte el orden.
- **Fin de la muestra**: el último trimestre común (2026T2), aunque el código de la guía corta en `2026-01-01`. Se documenta en 3.1.
- **Logit o nivel de la morosidad**: el pipeline calcula los dos; la elección se pre-registra en la 003.

Al cerrar la fábrica, abre en Cursor `outputs/figures/` y `data/raw/manifest.csv`, y confirma que 2025T4 dice cómo se promedió. Después haz la comparación con `/init` de la Fase 0.

### 002-literatura (domingo 4 a martes 6 · no crítica, pero se verifica con Claude)

Prompt del paso 2, en Claude Code:

```text
/sdd-spec 002-literatura Revisión de literatura verificada para las secciones 2.1–2.5 de la guía. Entregables: matriz de literatura con al menos 16 estudios verificados (mínimo 2 por cada sección 2.1–2.4 y al menos 6 empíricos para 2.5, con sus variables y metodología), references.bib solo con estudios verificados, y un script que compruebe cada DOI contra Crossref y falle si alguno no existe o no coincide. Incluir también como referencias de datos y método: FRED (series usadas), los escenarios de estrés 2026 de la Reserva Federal, Newey y West (1987) y Jordà (2005). Lista semilla, que hay que verificar como cualquier candidato: Bernanke y Gertler (1995); Bernanke, Gertler y Gilchrist (1999); Wilson (1997); Salas y Saurina (2002); Jiménez y Saurina (2006); Virolainen (2004); Nkusu (2011); Louzis, Vouldis y Metaxas (2012); Beck, Jakubik y Piloiu (2015); Ghosh (2015); Borio y Zhu (2012); Maddaloni y Peydró (2011); Jiménez, Ongena, Peydró y Saurina (2014); Wu y Xia (2016); Comité de Supervisión Bancaria de Basilea (2018). Fuera de alcance: redactar la sección 2 del informe (va en la 006). Crítica: no.
```

El coordinador manda al bibliotecario las tareas de búsqueda y puede lanzarlas en paralelo. Si prefieres hacerlo a mano en una segunda sesión de OpenCode, usa una línea por sección (términos en inglés porque la literatura está en inglés):

```text
/lit-buscar 2.1 "credit risk business cycle procyclicality loan losses" 3
/lit-buscar 2.2 "macroeconomic determinants nonperforming loans" 4
/lit-buscar 2.3 "monetary policy financial conditions credit channel" 3
/lit-buscar 2.4 "risk-taking channel monetary policy lending standards" 3
/lit-buscar 2.5 "nonperforming loans GDP unemployment interest rate panel" 6
```

Para cerrar la 002, en Claude Code (prompt directo, sin comando):

```text
Usa el subagente verificador-citas sobre report/references.bib y research/matriz-literatura.md. Pásale solo las rutas, no tu opinión. Guarda su informe tal cual en specs/002-literatura/review-audit.md y dime qué referencias hay que corregir o descartar.
```

## Specs 003 y 004: los dos modelos

Son el corazón del trabajo y las dos llevan pre-registro: la especificación queda aprobada en `spec.md` y auditada en `review-plan.md` antes de ver un solo coeficiente. No lances `/fabrica` hasta resolver cada observación de `review-plan.md`.

### 003-modelo-i (lunes 5 a jueves 8 · crítica)

```text
/sdd-spec 003-modelo-i Modelo I de la guía (secciones 4 y 6.1): determinantes macroeconómicos de la morosidad. Especificación a pre-registrar: dependiente DRALACBS, en nivel o en primera diferencia según la regla ADF/KPSS de la spec 001; regresores: crecimiento interanual del PIB real, cambio trimestral del desempleo, inflación interanual, cambio de la tasa de fondos federales y crecimiento interanual del crédito rezagado 4 trimestres; un rezago de la dependiente; dummies COVID 2020T2–2021T1. MCO con errores Newey-West. Signos esperados: PIB (−), desempleo (+), tasa (+), crédito rezagado (+), inflación (ambiguo: erosiona el ingreso real pero licúa la deuda). Salidas: tabla de coeficientes con error HAC, p-valor e IC 95 %; gráfico de coeficientes; batería completa de diagnósticos de la skill; robusteces (sin 2020–2021; DRALACBN; sub-carteras de consumo, empresas y bienes raíces; PIB nominal; logit de la morosidad; crédito rezagado 8 y 12 trimestres); validación fuera de muestra (estimar hasta 2019T4, pronosticar de 2022T1 al final y comparar el RMSE con un paseo aleatorio); y variables para el informe con cada efecto en pp de morosidad. Crítica: sí.
```

Decisiones para la entrevista:

- **Robusteces obligatorias y opcionales.** Con el plazo, recomiendo obligatorias: sin 2020–2021, sub-carteras y PIB nominal. Opcionales: logit y crédito a 8 y 12 trimestres.
- **Unidad de los efectos**: pp de morosidad por pp del regresor. Es lo que entiende un comité de riesgo.
- **Si un signo sale al revés**: se reporta y se discute; no se cambia la especificación (usa el prompt de rescate correspondiente).

### 004-modelo-ii (jueves 8 a sábado 10 · crítica)

```text
/sdd-spec 004-modelo-ii Modelo II de la guía (secciones 5 y 6.2): cambios de la política monetaria y deterioro posterior de la cartera. Especificación a pre-registrar. (a) Rezagos distribuidos: cambio de la tasa de fondos federales de t a t−K, con K elegido por AIC y BIC entre 1 y 8 sobre la misma muestra efectiva; un rezago de la dependiente; controles macro del Modelo I rezagados un trimestre; dummies COVID; errores Newey-West. Reportar el efecto acumulado con prueba de Wald HAC, el trimestre de efecto máximo y una prueba de causalidad de Granger. (b) Robustez con proyecciones locales de Jordà, h = 0 a 12: respuesta acumulada de la morosidad a un alza de 1 pp en la tasa, con bandas HAC al 90 %; es el gráfico central de la exposición. Signo esperado: positivo y con rezago (las alzas de tasas anticipan más morosidad). Límite a declarar: la tasa responde a la economía, así que el resultado es asociación dinámica, no causalidad. Fuera de alcance salvo que sobre tiempo: tasa sombra de Wu y Xia para 2009–2015. Crítica: sí.
```

Decisiones para la entrevista:

- **Si AIC y BIC eligen K distintos**: BIC en la especificación principal y AIC como robustez (es la regla de la skill).
- **Periodo de tasa cero (2009–2015 y 2020–2021)**: la tasa casi no se mueve; decláralo como límite. La tasa sombra solo entra si sobra el sábado 10.
- **Unidad del shock**: 1 pp de alza en la tasa, para que el resultado se lea igual en el informe, en las diapositivas y en el estrés.

## Specs 005, 006 y 007: estrés, informe y diapositivas

### 005-estres (sábado 10 a domingo 11 · crítica)

```text
/sdd-spec 005-estres Análisis de escenarios y prueba de estrés (sección 7 de la guía). Tres escenarios de 13 trimestres con las fechas de la Reserva Federal 2026 (punto de partida 2025T4, de 2026T1 a 2029T1): (1) base = escenario base oficial de la Fed 2026; (2) A = severamente adverso oficial de la Fed 2026 (el desempleo sube de 4,5 % a un pico de 10 % en 2027T3, el PIB real cae 4,6 % hasta 2027T2 y el Tesoro a 3 meses baja a 0,1 %); (3) B = estanflación propia: desempleo y PIB iguales a A, pero la tasa sube en lugar de bajar (magnitud calibrada con el ciclo de alzas 2022–2023) y la inflación se mantiene alta. Las trayectorias se toman de las tablas oficiales de la Fed (publicadas también en CSV) y se guardan con fecha como cualquier dato crudo; el Tesoro a 3 meses aproxima la tasa de fondos federales. Proyectar la morosidad con los Modelos I y II (proyección recursiva), con bandas al 90 % por simulación de coeficientes; reportar el cambio contra la base por trimestre, el pico y su trimestre, la diferencia A − B como aporte de la política monetaria, y una traducción a dinero con el saldo de LOANS (orden de magnitud, aclarando que morosidad no es pérdida). Duda a decidir conmigo: arrancar en 2025T4 como la Fed (comparable) o en el último trimestre observado aplicando las mismas variaciones. Crítica: sí.
```

Decisiones para la entrevista:

- **B es el escenario que describe la guía** (sube el desempleo, cae el PIB y sube la tasa). A aporta la credibilidad del escenario oficial. Llévate los dos.
- **Calibración de la tasa en B**: el ciclo 2022–2023 subió la tasa de fondos federales unos 5 pp en unos 6 trimestres; confirma la cifra con tus propios datos de FEDFUNDS antes de fijarla.
- **Punto de partida**: recomiendo 2025T4, igual que la Fed, y mencionar en 7 que 2026T1 y 2026T2 ya se observaron.

### 006-informe (domingo 11 a miércoles 14 · crítica)

```text
/sdd-spec 006-informe Informe final en Quarto que sigue la guía sección por sección (1 a 11), en español y APA 7, generado desde el mismo código: números solo vía report/_variables.yml, tablas y figuras desde outputs/, referencias solo desde references.bib con apa.csl. Debe incluir: sección 3 con datos, transformaciones, el hueco de octubre 2025 y las desviaciones del pre-registro; 6.3 comparando ambos modelos; 6.4 respondiendo la pregunta fundamental de la guía; 7 con los tres escenarios; 8 cubriendo los siete puntos de la guía con un tablero de alertas tempranas (indicador, umbral, acción); 9 con una conclusión que responda la pregunta sin el formato prohibido; 11 explicando el pipeline de descarga y el notebook. La fábrica construye el esqueleto de Quarto, la generación de variables, tablas y figuras, el render y las secciones descriptivas (3 y 11); las secciones de interpretación (1, 2, 4, 5, 6, 7, 8 y 9) se redactan con /redactar en Claude Code (agente: claude). Formato de salida: Word o PDF, según pida el profesor. Crítica: sí.
```

Cuando el coordinador llegue a las tareas `agente: claude`, redacta en Claude Code una sección por sesión, con `/clear` entre cada una:

```text
/redactar 1
/redactar 2 Usa solo los estudios verificados de la matriz; en 2.5 explica las variables y la metodología de cada estudio.
/redactar 4 Interpreta desde la gestión de riesgo, en pp de morosidad.
/redactar 5 Explica el rezago del efecto y el límite de endogeneidad.
/redactar 6 Integra ambos modelos y responde la pregunta fundamental de 6.4.
/redactar 7
/redactar 8 Usa el tablero de alertas tempranas y cubre los siete puntos de la guía.
/redactar 9
```

Son unas 8 llamadas a Opus repartidas entre el domingo 11 y el martes 13. Si el cupo aprieta, cambia `model: opus` por `model: sonnet` en `.claude/commands/redactar.md`.

El miércoles 14: `/sdd-audit 006-informe` y después `/evaluar`. Las mejoras de tipo (a) van a OpenCode con `/fabrica 006-informe "..."`, y las de tipo (b), a `/redactar`.

### 007-diapositivas (martes 13 a miércoles 14 · no crítica)

```text
/sdd-spec 007-diapositivas Presentación de máximo 12 láminas generada con Quarto desde las mismas variables y figuras del informe, exportable a PowerPoint, con notas del orador en cada lámina. Una idea por lámina y títulos que son conclusiones. Orden: pregunta y relevancia; datos 2000–2026 con recesiones; método en una lámina; Modelo I (gráfico de coeficientes); Modelo II (respuesta a un alza de 1 pp); validación fuera de muestra; los tres escenarios; trayectorias de estrés; aporte de la política monetaria (A − B); tablero de alertas tempranas; límites; conclusión y uso para la gestión del riesgo. Crítica: no.
```

### Jueves 15: entrega

- [ ] Desde un clon limpio en otra carpeta: `uv sync` y `uv run python -m src.pipeline all` funcionan sin tocar nada.
- [ ] Todos los `review-*.md` en `VEREDICTO: APROBADO`.
- [ ] Resueltas las mejoras críticas de `/evaluar`.
- [ ] Informe y diapositivas renderizados, sin `{{<` ni `?@` en la salida.
- [ ] Etiqueta `v1.0-entrega` y un Release en GitHub con el informe y las diapositivas.
- [ ] Ensayo con las preguntas del profesor anotadas en `MEMORY.md`.
- [ ] Entregado antes de las 22:00.

## Cursor, Orca y GitHub

### Cursor: revisión humana y tutor

Usa el modo Ask (el plan Hobby trae pocas peticiones de agente). Cursor nunca edita código: se saltaría la spec y los permisos de los agentes. Sí puedes editar a mano `spec.md`, `MEMORY.md` y los `review-*.md`. Cursor lee `AGENTS.md` de la raíz.

Antes de aprobar un diff (desde Source Control):

```text
Explícame en 5 viñetas qué cambia este diff y si viola alguna regla de @AGENTS.md o @docs/constitution.md. No propongas código.
```

Antes de aprobar una spec:

```text
Lee @specs/003-modelo-i/spec.md. ¿Qué requisito no podría comprobarse con un test o con un archivo de salida? Sé breve.
```

Para entender un resultado antes de exponerlo:

```text
Explícame @outputs/tables/<tabla>.md como a un estudiante de actuaría: qué significa cada coeficiente en pp de morosidad, cuáles son significativos con errores HAC y qué le diría a un comité de riesgo. Usa solo los números de la tabla.
```

Para ensayar la exposición:

```text
Hazme una por una las preguntas del profesor anotadas en @MEMORY.md y en @specs/004-modelo-ii/review-audit.md, y corrige mis respuestas usando solo esos archivos y las salidas del proyecto.
```

### Orca: el harness

Tres paneles en la carpeta del proyecto: `claude`, `opencode` y una libre. OpenCode usa OpenRouter como proveedor (clave en variable de entorno, nunca en el repo). Comandos del panel libre:

```bash
git switch -c spec/001-datos
uv run pytest -q
uv run python -m src.pipeline all
quarto render report/informe.qmd
git push -u origin spec/001-datos
```

Dentro de OpenCode también puedes ejecutar un comando sin salir, con `!` (por ejemplo `!uv run pytest -q`).

### GitHub: memoria y puerta

- **Un issue por spec**, con la fecha objetivo del calendario y las puertas de la plantilla de PR. El PR lo cierra con `Closes #N`.
- **Un PR por spec** desde `spec/NNN-nombre`: la plantilla ya trae la lista de puertas. Merge solo con Actions en verde.
- **Al final**, la etiqueta `v1.0-entrega` y un Release con el informe y las diapositivas.

Si tienes instalado `gh`, Claude Code puede crear los issues:

```text
Con gh, crea un issue por cada spec de la 001 a la 007 con el título "Spec NNN · <nombre>", la fecha objetivo del calendario de MEMORY.md y la lista de puertas de .github/pull_request_template.md. Muéstrame los comandos antes de ejecutarlos.
```

## Prompts de rescate

Para cuando algo se tuerce. Cada uno indica dónde se escribe.

**Se agotó el cupo de Claude Code** (OpenCode, agente `coordinator`):

```text
No tengo cupo de Claude Code hasta las HH:MM. Pide a @planner que redacte como respaldo specs/NNN-nombre/spec.md (o plan.md), enséñamelo para aprobarlo y anota en MEMORY.md que falta /sdd-audit cuando vuelva el cupo.
```

**La ventana de 5 horas está por acabarse** (Claude Code): `/cierre` antes de que se corte. Al volver, en OpenCode, `/sdd-status` te dice el siguiente paso sin gastar cupo.

**LongCat no responde o dejó de ser gratis**: en OpenCode, `/models` → Nemotron 3 Ultra Free. Para los agentes, en Cursor usa buscar y reemplazar (Ctrl+Shift+H) en `.opencode/` y `opencode.jsonc`: cambia `opencode/longcat-2.5-preview-free#high` por `opencode/nemotron-3-ultra-free` y reinicia OpenCode.

**Un agente hizo más de lo pedido** (OpenCode):

```text
PARA. Tu tarea era solo Tn de specs/NNN-nombre/tasks.md. Lista lo que hiciste fuera de esa tarea; lo deshago con /undo y seguimos solo con Tn.
```

**Los tests siguen en rojo** (OpenCode):

```text
@implementer La tarea Tn de specs/NNN-nombre/tasks.md sigue con tests en rojo. Depura con método: reproduce el fallo, aíslalo, formula una hipótesis y verifícala. No cambies un test para que pase, salvo que contradiga plan.md; en ese caso, PARA y dímelo.
```

**Un coeficiente salió con el signo contrario al pre-registrado** (Claude Code):

```text
El coeficiente de <variable> salió con signo contrario al pre-registrado en specs/003-modelo-i/spec.md. No cambies la especificación. Dame 3 explicaciones económicas o de datos, qué robustez ya prevista en la spec las distingue y cómo reportarlo con honestidad en el informe.
```

**El reviewer de OpenCode aprobó algo que no te convence** (Claude Code):

```text
Usa el subagente revisor-econometrico para revisar con escepticismo specs/NNN-nombre/review-validate.md: ¿qué aprobó el revisor de OpenCode sin evidencia suficiente? Pásale solo las rutas.
```

**El contexto está saturado**: en OpenCode, `/compact` o `/new`; en Claude Code, `/clear`. Nada se pierde porque el estado vive en `MEMORY.md` y en `specs/`.

## Fuentes

- Apuntes del Curso de Desarrollo con IA, días 1, 2 y 3 (los PDF que adjuntaste): AGENTS.md y MEMORY.md, SDD con EARS, comandos, skills y el sistema coordinador → planificador → implementador → revisor.
- [OpenCode Zen: modelos gratuitos y privacidad](https://opencode.ai/docs/zen)
- [OpenCode v2: agentes y permisos](https://opencode.ai/v2/docs/agents)
- [OpenCode v2: comandos](https://opencode.ai/v2/docs/commands)
- [OpenCode v2: skills](https://opencode.ai/v2/docs/skills)
- [OpenCode v2: AGENTS.md](https://opencode.ai/v2/docs/instructions)
- [Claude Code: subagentes](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: skills y comandos](https://code.claude.com/docs/en/skills)
- [Claude Code: CLAUDE.md, AGENTS.md y memoria](https://code.claude.com/docs/en/memory)
- [Reserva Federal: 2026 Stress Test Scenarios](https://www.federalreserve.gov/publications/2026-stress-test-scenarios.htm)
- [Anthropic prohíbe usar la suscripción en herramientas de terceros](https://gigazine.net/gsc_news/en/20260220-anthropic-third-party-block)
