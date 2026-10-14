# Spec 006 — Informe: condiciones macroeconómicas, política monetaria y riesgo de crédito
Estado: aprobada v4 (change editorial aplicado por Claude Code, 12-oct-2026, por aprobación literal del autor; v3 aprobada conservada byte a byte en `spec-v3-approved.md`; ver `change-editorial-applied.md`) · Crítica: sí
Cambio v4: informe principal narrativo de 11 secciones + anexo técnico A–F separado, con slugs estables, registro único y enlaces; sin metodología nueva ni estimaciones nuevas. Las secciones afectadas son «Estructura obligatoria», RF-3, RF-14 (y RF-14b), RF-15, RNF-6, «Criterios de finalización» y «Dudas abiertas»; el resto del texto v3 permanece.

> Marca: **[DEPENDE 005]** = contenido que no puede escribirse hasta que la spec 005 esté validada y auditada. Esta spec no contiene resultados: las cifras del informe saldrán de `outputs/` y `report/_variables.yml`.

## Contexto y objetivo
La guía del profesor (`docs/guia-profesor.md`) pide un informe de investigación en 11 secciones que responda: «¿En qué medida las condiciones macroeconómicas y los cambios en la política monetaria afectan el riesgo de crédito, y cómo pueden estos efectos ser utilizados para fortalecer la gestión y monitoreo del riesgo financiero?». Esta spec fija **qué** debe contener y cumplir el informe final, escrito en Quarto, con las salidas aprobadas de las specs 001 a 004 y las de la 005 cuando esté validada y auditada. Es la entrega principal. El objetivo interno del autor es tener los archivos finales revisados la noche del jueves 15-oct-2026; la fecha, la hora y el cierre oficiales **no figuran en la guía** (el «antes de las 22:00» y el cierre a las 00:00 del 16 vienen del Playbook) y están **pendientes de confirmación con el profesor**: no se tratan como requisitos confirmados.

El informe **no estima ni decide nada nuevo**. Presenta, interpreta y discute lo ya pre-registrado y auditado, con lenguaje de asociación, límites declarados y cada desviación del pre-registro a la vista. Nada se redacta fuera de una spec, un plan y unas tareas aprobados.

## Pregunta que responde (y sección de docs/guia-profesor.md que cubre)
Las 11 secciones de la guía, con los mismos títulos y numeración. Responde la pregunta fundamental de la 6.4: «¿Los resultados econométricos proporcionan evidencia de que el entorno macroeconómico y la política monetaria constituyen factores relevantes para el riesgo de crédito?» y la conclusión (9) dice cómo usar la información para anticipar y gestionar el riesgo.

Reparto con otras specs: 001 (datos), 002 (literatura y `references.bib`), 003 (Modelo I), 004 (Modelo II) y 005 (estrés) producen cifras, tablas, figuras y referencias; esta spec solo las consume. La spec 007 (diapositivas) reutiliza las mismas variables y figuras.

## Usuarios
El autor (entrega), el profesor evaluador (rúbrica de la guía), el revisor econométrico y el verificador de citas (auditoría independiente), y la spec 007.

## Historias de usuario
- HU-1. Como autor, quiero un informe que siga la guía sección por sección para que el profesor encuentre cada requisito donde lo espera.
- HU-2. Como autor, quiero que ninguna cifra ni cita se escriba a mano, para cumplir la constitución y poder regenerar el informe si cambia una salida.
- HU-3. Como lector, quiero que cada resultado se lea en unidades (pp de morosidad), con su significancia, sus diagnósticos fallidos y sus límites, para saber cuánto confiar en él.
- HU-4. Como gestor de riesgos, quiero una sección de implicaciones con un tablero de alertas tempranas, para saber qué monitorear y qué acción tomar.
- HU-5. Como autor, quiero poder responder las preguntas probables del profesor (listadas en `MEMORY.md` y en las auditorías) con lo que el informe ya dice.

## Definiciones
- **Salida aprobada**: archivo de `outputs/` o clave de `report/_variables.yml` producido por el pipeline de una spec con `VEREDICTO: APROBADO` en su validación (y, en las críticas 003, 004 y 005, en su auditoría independiente).
- **Cifra**: cualquier número del texto (incluidos porcentajes, p-valores, años de datos y conteos), salvo fechas de trimestre como «2000T1» y números de sección o de cita.
- **Lenguaje de asociación**: «se asocia con», «precede», «anticipa». Nunca «causa», «provoca», «debido a», salvo los nombres técnicos definidos en las specs 003 a 005 («efecto de impacto», «efecto acumulado», «respuesta»), que se definen en el informe como asociaciones condicionales.
- **Hallazgo heredado**: observación o limitación ya documentada en una auditoría o revisión (lista en «Hallazgos que el informe debe incorporar») que el informe debe tratar explícitamente.

## Especificación del informe

### Estructura obligatoria
Secciones 1 a 11 de la guía, con sus títulos y su numeración (incluidas 2.1–2.5, 3.1–3.5 y 6.1–6.4). Cada sección empieza con su respuesta en una frase. Entregable principal: fuente Quarto (`report/informe.qmd`) renderizada a **PDF** con el motor Typst que incluye Quarto, con citas APA 7 (`apa.csl`), y exportable también a **Word** (docx). Decisión del autor, 12-oct-2026. El formato exigido, la extensión máxima, la hora de entrega y el formato de la exposición no los fija la guía y siguen **pendientes de confirmación con el profesor**. El título del informe es el «Título propuesto» de la guía, salvo decisión expresa del autor.

**Cambio editorial v4 (aprobado por el autor, 12-oct-2026).** El entregable consta de dos documentos del mismo proyecto Quarto: el **informe** (secciones 1 a 11, narrativo, con índice, que explica los resultados y las conclusiones) y el **anexo técnico** (con índice, que conserva la evidencia completa), cada uno en PDF (Typst) y Word. Reglas:
- **Slugs y registro único.** Cada tabla y figura aprobada tiene un slug estable (por ejemplo `AT-M1-ROB`, `AT-M2-LP`) y un destino en el registro único `outputs/informe/registro.csv`, generado por código (slug, fuente CSV o PNG, anexo, identificador visible, título, pie y nota, versión en el cuerpo). El número visible lo asigna el render; el cuerpo remite por slug.
- **Sin duplicación rutinaria.** Cada tabla o figura aparece **completa una sola vez**, en el anexo. El cuerpo incluye una versión reducida solo si es esencial para una lectura independiente; la genera el código desde el mismo CSV, con las mismas cifras, y declara dónde está la completa. Una figura esencial no se recorta ni pierde sus bandas en el cuerpo.
- **Anexos:** A Datos y transformaciones; B Modelo I; C Modelo II; D Estrés; E Literatura; F Desviaciones, reproducibilidad y descarga. Codex puede reagrupar sin cambiar el principio.
- **Lo esencial de la guía permanece en el cuerpo:** coeficientes principales con significancia y diagnósticos con veredicto (4), respuesta dinámica y lectura (5), comparación (6.3), cambio adverso − base de ambos modelos (7) y tablero (8). En 2.5 el cuerpo explica las variables, la metodología y los signos permitidos de los estudios; la tabla completa va al anexo E.
- **Se preservan** las notas y pies aprobados (el pie de `model2_lp` con la definición de β y φ y la ausencia de banda en h0; la nota de vacíos de `model1_robustness_estimates`), las tablas de presentación y los anexos completos ya generados. No cambia ninguna salida de 001–005.
- **Alternativa combinada.** Se mantiene como opción manual (informe más anexo concatenado como apéndice, sin duplicar tablas completas). No es la salida por defecto y su aceptación por el profesor **no está confirmada**.

### Fuente de cada sección
| Sección | Contenido | Fuentes aprobadas |
|---|---|---|
| 1 Introducción | Problema, relevancia para la estabilidad financiera y la gestión del riesgo; pregunta y objetivo de la guía | Guía; literatura de 2.1 y 2.2 |
| 2 Revisión de literatura (2.1–2.5) | Una subsección por tema de la guía; 2.5 explica, por estudio, variables y metodología y el signo del hallazgo | `research/matriz-literatura.md`, `report/references.bib`; solo filas «verificado» |
| 3 Datos y metodología (3.1–3.5) | Variables, frecuencia, período y fuentes; dependiente; regresores; variable de política (ΔFFR); los dos modelos; el hueco de octubre de 2025; transformaciones y estacionariedad; las desviaciones frente a la guía y al pre-registro | Specs 001, 003, 004; `outputs/data_note.md`, `descriptives`, `stationarity`, `model1_deviations`, `model2_deviations` |
| 4 Modelo I | Estimación, coeficientes, significancia, diagnósticos e interpretación desde la gestión de riesgos | `model1_*` |
| 5 Modelo II | Respuesta dinámica de la morosidad a la tasa, efectos rezagados, lectura de la evidencia, límite de endogeneidad | `model2_*` |
| 6 Análisis de resultados (6.1–6.4) | 6.1 y 6.2 resultados; 6.3 comparación (incluye `model2_inputs63`); 6.4 discusión económica y respuesta a la pregunta fundamental | `model1_*`, `model2_*` |
| 7 Escenarios y estrés **[DEPENDE 005]** | Escenarios base y adversos, cambio proyectado en la morosidad, sensibilidades y límites | `stress_*` y `estres.*`, solo tras 005 validada y auditada |
| 8 Implicaciones para la gestión de riesgos | Los siete puntos de la guía; tablero de alertas tempranas | Resultados de 4 a 7; literatura |
| 9 Conclusiones | Respuesta directa a la pregunta de investigación y cómo anticipar y gestionar el riesgo | Todas |
| 10 Referencias | APA 7 | `report/references.bib` |
| 11 Base de datos y descarga | Series, descarga con `pandas_datareader` (y el respaldo documentado), congelado con fecha, reproducibilidad del pipeline | Spec 001; `data/raw/manifest.csv`; `AGENTS.md`/`README.md` |

### Reparto de redacción y propiedad de archivos (decisión del autor, 12-oct-2026)
- **Claude Code redacta** la interpretación, la discusión, las limitaciones y las conclusiones: secciones 1, 2 (texto), 4, 5, 6 (6.1–6.4), 7 (texto, tras la 005), 8 y 9, y los párrafos de limitaciones de 3.5.
- **Codex prepara** la integración: esqueleto y `_quarto.yml`, secciones descriptivas 3 y 11, 10 (referencias), tablas y figuras incluidas, la tabla de estudios de 2.5, variables y etapa `report`, y el render a PDF y Word.
- **Propiedad por archivo:** el plan dividirá el informe en archivos de sección incluidos desde `informe.qmd` (por ejemplo, `report/secciones/NN-*.qmd`), cada uno con un único escritor asignado, y fijará qué archivos no se tocan en paralelo (en particular `informe.qmd`, `_quarto.yml`, `_variables.yml` y `references.bib`, que son de Codex). Nadie edita un archivo asignado a la otra herramienta mientras ésta trabaja; los cambios cruzados se piden por escrito.
- **Autoría real y auditoría.** Como Claude redacta, su auditoría no es independiente de esas secciones. La auditoría de la 006 la hará un subagente con contexto limpio y solo rutas y criterios, y se complementa con la validación de Codex, el verificador de citas y el evaluador de rúbrica; el informe de auditoría declara la autoría real de cada sección y esta limitación.

### Hallazgos que el informe debe incorporar
Cada uno procede de un documento ya escrito; el informe los trata sin atenuarlos y sin reabrir las specs.

**Datos y metodología (sección 3)**
- Octubre de 2025 no existe en CPI ni en desempleo (cierre del gobierno): 2025T4 se promedia con dos meses; el tratamiento de la 001 se declara, sin imputar. Las series con la última observación posterior al último trimestre común se recortan al último trimestre común.
- Desviaciones frente a la guía: la muestra termina en 2026T2 (el ejemplo de la guía corta en 2026-01-01); PIB real (GDPC1) como principal y GDP nominal como robustez; regresores en la forma fija pre-registrada frente a la regla de estacionariedad; muestra larga desde 1985 no disponible (la historia congelada empieza en 1998).
- Inconsistencia a resolver: `datos.n_series` vale 12 mientras la referencia institucional de FRED enumera 13 series (`outputs/data_note`, `report/_variables.yml`, `references.bib`); el informe usa una sola cifra, generada por código.
- La descarga de FRED está congelada con fecha (2026-10-02); FRED revisa el PIB, así que volver a descargar puede cambiar resultados.

**Modelo I (secciones 4 y 6)** (de `specs/003-modelo-i/review-audit*.md`)
- Regresión desbalanceada: π y CRED son «no I(0)» por la regla conservadora (ADF no rechaza) pero KPSS tampoco rechaza la estacionariedad: la evidencia es ambigua; se dicen las dos cosas.
- PIB: distinguir el efecto de impacto del de largo plazo al hablar de significancia; el recuento de robustez cuenta el coeficiente de impacto.
- El CUSUM pasa y los dos Chow fallan: no es una contradicción (poca potencia del CUSUM frente a quiebres en pendientes); se explica.
- ΔFFR con signo contrario al esperado; ΔU con poca variación fuera de la COVID; «supera al ingenuo» siempre acompañado de «no significativo»; el R² está inflado por las dummies de impulso; R1 es un contraste parcial (la nota de R1 no es exhaustiva: no escribir que «solo» esos términos tocan trimestres excluidos).
- BP, White, JB, RESET y los dos Chow fallan; el VIF de ΔU es un artefacto de las dummies COVID.
- Notación del KPSS acotado: coherencia entre la tabla de la 001 y la de la 003 (el informe usa una sola).
- Los coeficientes del tramo de entrenamiento 2000–2019 no se exportaron: el informe no explica con cifras por qué el pronóstico dinámico cae en 2022–2023 más allá de lo que muestran las salidas; si se necesitaran, hace falta un `change` de la 003 (fuera de alcance).

**Modelo II (secciones 5 y 6)** (de `specs/004-modelo-ii/review-audit*.md`)
- Con K = 1, la prueba de Granger y la condición C2 son el mismo Wald; la «regla de dos condiciones» se reduce a una sola prueba y el informe lo dice.
- «Sin evidencia» es el resultado de una regla fijada de antemano; RESET y el Chow de 2020T2 fallan: el informe discute qué parte de «sin evidencia» sobrevive con un modelo lineal mal especificado e inestable. El signo puntual negativo es compatible con que la Fed reacciona al ciclo (endogeneidad); ΔFFR no es un shock identificado.
- φ_h ≈ 3 (cifra desde las salidas): el «shock de 1 pp» de las proyecciones locales es en realidad un ciclo de alzas; las limitaciones prometen una discusión que el informe debe escribir.
- La columna `columna_panel` de `model2_stationarity` es ambigua (serie base frente a columna diferenciada); el informe la rotula con claridad.

**Literatura (sección 2)** (de `specs/002-literatura/review-audit.md`)
- Justificar `bernanke1995` en 2.1 (resumen de transmisión monetaria; 2.4 secundaria) y la clasificación de `pesaran2006`, `segoviano2006` (2.2) y `gertler2015`, sin reasignar para cuadrar mínimos.
- `asiamah2026` y `koskei2023` están «pendiente-lectura»: no se citan con hallazgo ni signo.
- Observaciones opcionales de la 002 (`koju2018`, `tanaskovic2015`, `nkusu2011`, `jimenez2014a`, `obradovic2026`) se tratan solo si se corrigen en la matriz por una tarea aprobada; si no, el informe no repite las lecturas dudosas.
- **Revisión de la referencia FRED** (observación pospuesta de la 002, T3/T5): `fred2026` apunta hoy al CSV de una serie mientras el plan de la 002 fijaba la raíz de FRED; el informe resuelve la URL final con una tarea explícita, y `scripts/verify_refs.py` (requiere red) debe terminar con código 0.

**Estrés (sección 7) [DEPENDE 005]** (de `specs/005-estres/spec.md` y `review-plan*.md`)
- La regla de la tasa en cero es una regla de prudencia heredada de la 004, no un hallazgo de efecto cero; la sensibilidad con los coeficientes estimados va aparte y se rotula «sensibilidad, no efecto estimado».
- Adaptación del escenario Fed 2026 (trimestre 2026 Q1 de la Fed en 2026T3), con las propiedades de invariancia (A) y cancelación (B) y sus condiciones, sin presentarlas como generales; los niveles de la variante desde 2025T4 son contrafactuales.
- En el adverso de la Fed la inflación y la tasa bajan; el escenario D (actividad adversa con alza de tasas, no estanflacionario) da la misma proyección que el adverso principal bajo la regla de tasa en cero; esto cambia la decisión previa de un escenario estanflacionario y se declara.
- Las bandas son incertidumbre de parámetros, no intervalos de predicción, y omiten otras fuentes; en el Modelo II el cambio del primer trimestre es 0 por construcción; ΔFFR en D viene de FEDFUNDS observada y en la base y el adverso de la letra a 3 meses; supuesto de crédito constante desde 2027T3; sin equivalente en dólares ni estimador restringido.
- **Estado de la auditoría de la 005 (12-oct-2026):** la ronda 1 dio «CAMBIOS NECESARIOS» (`specs/005-estres/review-audit.md`, copia en `review-audit-ronda1.md`) y Codex corrige cinco bloqueantes de contrato (nombres de claves `estres.*`, advertencia de niveles fuera de rango en las tablas, definición de `dif_modelos.delta_pico`, tablas Markdown y tests faltantes). Hasta una ronda 2 aprobada, ninguna cifra, clave ni redacción de estrés es definitiva: el informe solo usa las claves del plan §5 y la sección 7 no se escribe con resultados. Del informe de la ronda 1 se trasladan a la sección 7, sin cifras: las bandas al 90 % del cambio final cruzan cero aunque la mayoría de las réplicas sea positiva; hay réplicas con niveles negativos o explosivas (se informan sin descartarlas); el cambio final depende de que el choque empiece de inmediato (RF-12a); en las figuras el adverso queda oculto bajo D; el nivel de la tasa se ancla en FEDFUNDS de 2026T2 por no haber letra a 3 meses en el panel; el estrés usa la especificación lineal en primera diferencia con RESET y Chow rechazados.

**Preguntas probables del profesor** (de `MEMORY.md` y las auditorías): el informe debe permitir responder (a) por qué creer los p-valores de π y CRED si son no I(0); (b) cómo usar el Modelo I en un estrés con alzas de tasa si ΔFFR sale negativa; (c) qué afirmación para gestión de riesgos sobrevive a endogeneidad, inestabilidad y no linealidad; (d) si subir tasas reduce la morosidad según el Modelo II y cómo se separa de la endogeneidad; (e) qué cambia en los niveles si el escenario parte de 2025T4 o de 2026T2 y por qué Δ no cambia.

### Sección 8: tablero de alertas tempranas
Una tabla (indicador, umbral, acción) que cubra los siete puntos de la guía (alertas tempranas, monitoreo macro, políticas de crédito, escenarios de estrés, planificación de capital, gestión de cartera, concentración y calidad crediticia). Los criterios son **cualitativos de gestión** (decisión del autor, 12-oct-2026): no se introducen umbrales numéricos sin respaldo ni nuevas estimaciones. Una cifra solo puede aparecer si ya existe en `_variables.yml` y se usa para describir un resultado, nunca como umbral inventado.

## Requisitos funcionales
- RF-1: EL SISTEMA contendrá las 11 secciones de la guía, con sus títulos y numeración, en orden, con el título propuesto por la guía, la pregunta de investigación y el objetivo general en la sección 1, y cada sección abrirá con su respuesta en una frase.
- RF-2: CUANDO el texto contenga una cifra, EL SISTEMA la tomará de `report/_variables.yml` con `{{< var ... >}}`. Ninguna cifra se escribe a mano. SI falta una variable, ENTONCES se solicita a la etapa `report` del pipeline que la genere; no se inventa.
- RF-3: Las tablas y figuras se incluirán desde productos generados por código a partir de los CSV y PNG aprobados de `outputs/`, asignados por el registro único (`outputs/informe/registro.csv`): completas una sola vez en el anexo técnico y, en el informe, solo como versión reducida cuando sea esencial para una lectura independiente. Cada una lleva slug estable, pie y la fuente («Fuente: FRED; elaboración propia»; en 7, la indicada por la spec 005) y conserva las notas aprobadas. Un test comprueba que cada cifra de una tabla reducida o de presentación coincide con su CSV de origen. La tabla de estudios de 2.5 la genera código desde la matriz de literatura.
- RF-4: EL SISTEMA citará solo claves de `report/references.bib` con filas «verificado» en la matriz, en APA 7 con `apa.csl`. Ninguna cita sin DOI o URL verificada; el informe no cita con hallazgo a los estudios «pendiente-lectura» ni «descartado».
- RF-5: EL SISTEMA describirá los resultados en pp de morosidad por unidad del regresor (por ejemplo «un pp más de desempleo se asocia con X pp más de morosidad», con X desde las variables), con su significancia y su incertidumbre, y con lenguaje de asociación.
- RF-5b: EL SISTEMA responderá en la sección 4 la pregunta específica de la guía («¿Cómo afectan las condiciones macroeconómicas…?») y en la 5 la suya («¿existen efectos rezagados sobre la calidad de la cartera?», con la lectura de la evidencia de la 004). Aclarará que «afectan» y «efecto» se leen como asociación condicional, y que la ΔFFR observada no es un shock de política monetaria identificado, aunque la guía hable de un shock.
- RF-6: EL SISTEMA reportará, sin atenuarlos, los diagnósticos que fallan y las limitaciones de las salidas aprobadas, y tratará cada hallazgo heredado de la lista anterior (el informe indica dónde lo trata).
- RF-7: EL SISTEMA declarará en 3.1, 3.3 y 3.5 todas las desviaciones del pre-registro y las diferencias con la guía (la tabla de variables de la guía usa GDP nominal y el informe usa GDPC1 real como principal, con GDP como robustez; el crédito es la serie LOANS elegida; la «tasa de interés» de 3.3 y el «cambio de la FFR» de 3.4 son la misma variable ΔFFR; el período termina en 2026T2 y no en 2026-01-01) (tablas `model1_deviations`, `model2_deviations` y, para la 7, las de la 005).
- RF-8: EL SISTEMA integrará los dos modelos en 6.3 con los insumos de `model2_inputs63`, sin ponderarlos ni elegir uno, y diciendo que difieren en muestra y forma de los controles.
- RF-9: EL SISTEMA responderá en 6.4 la pregunta fundamental de la guía, sin el formato «el PIB fue significativo y el desempleo también», con la distinción entre asociación y causalidad y la respuesta a las preguntas probables listadas.
- RF-10: EL SISTEMA incluirá en 8 el tablero de alertas tempranas y los siete puntos de la guía, conectados con los resultados de 4 a 7 y con la literatura de 2, y enlazados con el resultado de aprendizaje de la asignatura (identificar, medir, monitorear y gestionar los principales riesgos financieros), con criterios cualitativos y sin umbrales numéricos inventados.
- RF-11: EL SISTEMA concluirá en 9 respondiendo directamente la pregunta de investigación y diciendo cómo usar los resultados para anticipar y gestionar el riesgo.
- RF-12: **[DEPENDE 005]** CUANDO la spec 005 esté validada y auditada, EL SISTEMA redactará la sección 7 con los escenarios, el cambio adverso − base de ambos modelos, las sensibilidades y los límites de la spec 005, y mantendrá el rótulo «adaptación del escenario Fed 2026». SI la 005 no está lista, ENTONCES la sección 7 queda con un marcador explícito «pendiente de resultados de la spec 005» y el informe no se declara completo.
- RF-13: EL SISTEMA explicará en 11 que la guía anuncia un notebook de descarga y que el proyecto usa su propio pipeline reproducible, y describirá el pipeline de descarga con `pandas_datareader` y su respaldo, la congelación con fecha, el hueco de octubre de 2025 y cómo reproducir todo con `uv run python -m src.pipeline all`.
- RF-14: EL SISTEMA renderizará `report/informe.qmd` y el anexo técnico (`report/anexo-tecnico.qmd`) a PDF (Typst) y a Word (docx) sin que queden `?@`, `?var`, `{{<` ni referencias sin resolver, y la primera tarea será un render de humo (una variable, una tabla incluida, una figura y una cita) en el proyecto real antes de redactar. El plan fijará la disposición del proyecto Quarto, porque la prueba de humo del 12-oct (ver `docs/entorno-quarto-2026-10-12.md`) mostró que Typst no permite rutas fuera de la raíz del proyecto y que `{{< var >}}` solo lee `_variables.yml` en la raíz del proyecto. SI el render falla, ENTONCES se avisa al autor antes de cambiar de formato.
- RF-14b: Las remisiones usan anclas nativas de Pandoc (identificador por slug, no HTML) y son enlaces internos en PDF y DOCX dentro de cada documento. Entre el informe y el anexo, la remisión es siempre texto estable («Anexo B, `AT-M1-ROB`») más enlace relativo local al otro archivo cuando exista; hacia la nube se usan solo URLs reales suministradas o autorizadas por el autor, y ningún agente sube archivos. Las pruebas de enlaces son estructurales (destinos nombrados del PDF, bookmarks del DOCX, archivos de destino existentes) y no prueban el clic en Word ni en Google Docs; el DOCX se revisa en Google Docs como excepción documentada, sin Word nativo.
- RF-15: EL SISTEMA generará con la etapa `report` del pipeline las variables y tablas nuevas que el informe necesite (conteos de literatura, tabla 2.5, `n_series` único, hallazgos heredados con sus cifras), y el registro único `outputs/informe/registro.csv` con slugs, destinos, versiones reducidas, índices y etiquetas de anexo, de modo que dos corridas dejen salidas idénticas.

## Requisitos no funcionales
- RNF-1 (constitución): ninguna cifra o cita inventada; lógica en `src/`, el informe solo lee `outputs/`; idioma español formal, frases de menos de 25 palabras, voz activa.
- RNF-2 (tests existentes): `uv run pytest -q` en verde, incluidos `test_report_has_no_hand_typed_numbers` y el test de citas contra `references.bib`; se añaden tests para las salidas nuevas de RF-15.
- RNF-3 (lenguaje): ninguna frase causal; búsqueda con grep en el `.qmd` y en la salida renderizada.
- RNF-4 (reproducibilidad): el render se repite con las mismas salidas y las mismas cifras; los datos de `data/raw/` no se tocan.
- RNF-5 (independencia, con la salvedad del reparto de redacción): la auditoría usa `revisor-econometrico` (coherencia econométrica del informe: cifras, interpretación, lenguaje causal y límites) y `verificador-citas` (referencias), y `profesor-evaluador` contra la guía, cada uno con solo rutas y criterios, sin la conclusión del autor.
- RNF-6 (trazabilidad): cada afirmación de resultado se puede rastrear a una variable o tabla; cada hallazgo heredado, a la sección que lo trata. Cada remisión del cuerpo a un slug existe exactamente una vez en el anexo; no hay slugs duplicados ni huérfanos, ni tablas completas repetidas en el cuerpo.

## Casos límite
- Una variable necesaria no existe: se genera en la etapa `report` mediante una tarea aprobada; no se escribe a mano.
- Un resultado cambia por una nueva corrida: el informe se regenera; los textos que dependan de un signo o de una conclusión se revisan.
- Un estudio de la matriz pasa a «pendiente-lectura» o «descartado»: sale del texto y de las referencias.
- La spec 005 no se cierra a tiempo: el informe se entrega sin sección 7 final solo con la advertencia del RF-12 y la aprobación expresa del autor.
- El render falla o una herramienta falta: se avisa al autor antes de cambiar de formato; no se declara el informe entregado sin un render válido.

## Fuera de alcance
- Estimar o re-estimar modelos, cambiar especificaciones o escenarios, o corregir salidas de las specs 001 a 005; cualquier cambio se tramita como `change` de esa spec.
- Citas nuevas no verificadas; ampliar la bibliografía más allá de las tareas aprobadas.
- Equivalente en dólares del cambio de morosidad y estimador restringido (excluidos en la 005).
- Las diapositivas (spec 007) y la exposición.
- Un notebook de descarga distinto del pipeline (la guía habla de un notebook proporcionado por el profesor; el informe documenta el pipeline propio y, si el profesor entrega el suyo, no se reabre ninguna spec).

## Criterios de finalización
- Spec, plan y tareas aprobados por el autor antes de redactar.
- `report/informe.qmd` con las 11 secciones, renderizado sin errores ni referencias sin resolver; sección 7 final solo con la 005 validada y auditada.
- `uv run pytest -q` en verde; `uv run python -m src.pipeline all` reproduce las salidas.
- `review-validate.md` con `VEREDICTO: APROBADO` y `review-audit.md` independiente con `VEREDICTO: APROBADO` (coherencia econométrica y referencias).
- Revisión con `profesor-evaluador` y ensayo de las preguntas probables.
- Cobertura del registro: todo CSV y PNG aprobado tiene destino; lo esencial de la guía está en el cuerpo; cada remisión del cuerpo resuelve en el anexo; los enlaces internos existen en PDF y DOCX (comprobación estructural, DOCX revisado en Google Docs sin Word nativo).
- El criterio de cierre global exige la suite completa en verde (`uv run pytest -q`); no se sustituye por una suite parcial. Los fallos de arnés ajenos a 006 se diagnostican por separado; se puede avanzar la implementación con la verificación global pendiente, sin declarar T11 aprobada ni 006 cerrada.
- Entrega antes del plazo confirmado (jueves 15-oct-2026).

## Desviaciones del pre-registro
(vacío; esta spec no tiene pre-registro econométrico propio)

## Dudas abiertas
Decisiones del autor, 12-oct-2026: Quarto como fuente, PDF principal y Word exportable; instalación mínima de Quarto (hecha, ver `docs/entorno-quarto-2026-10-12.md`); tablero con criterios cualitativos; reparto de redacción (Claude: interpretación, discusión, limitaciones y conclusiones; Codex: integración, tablas, figuras y render).
- **Pendiente de confirmar con el profesor (no son requisitos confirmados):** hora y fecha oficiales de entrega, extensión máxima, formato exigido (PDF o Word), formato de la exposición y si admite material complementario separado (anexo técnico en documento aparte). Si no lo admite, se usa la alternativa combinada.
- [NECESITA ACLARACIÓN] **Disposición del proyecto Quarto** (RF-14): con la raíz del proyecto en `report/`, Typst no puede leer `../outputs/`; con la raíz en el repositorio, `_variables.yml` debe estar en esa raíz y no en `report/`. El plan propondrá la solución (por ejemplo, raíz de Quarto en el repositorio y generación de `_variables.yml` también en la raíz, o copia de figuras y tablas a `report/` en la etapa `report`) sin cambiar el contrato de las specs cerradas; si exige tocar un contrato aprobado, se presentará como `change`.
- [NECESITA ACLARACIÓN] **Independencia de la auditoría** (ver «Reparto de redacción»): aceptar la auditoría con subagente de contexto limpio más validación de Codex, o pedir que Codex audite las secciones redactadas por Claude.
- **`apa.csl` y `_quarto.yml`:** el plan fijará su procedencia; el CSL «APA Style 7th edition» (CC BY-SA 3.0) se obtiene del repositorio público de estilos CSL y su huella se registra.
- **Estado de la 004:** la auditoría de la ronda 2 es APROBADA; el cierre formal de la spec 004 (T9, estado «implementada») lo hace Codex.
