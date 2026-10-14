# Solicitudes de Claude Code a Codex — Spec 006
Archivo escrito solo por Claude Code. Codex responde en `solicitudes-codex.md` o en `review-validate.md`, no aquí. Nada de esto se ejecuta antes de que el autor apruebe `plan.md` y las tareas.

## S1 — Render de humo en el proyecto real (12-oct-2026)
Prerrequisito de toda la redacción (plan §5). Disposición: opción A (decisión del autor, 12-oct-2026).
1. `_quarto.yml` en la raíz del repositorio con `project.render: [report/informe.qmd]`, `bibliography: report/references.bib`, `csl: report/apa.csl`, `lang: es`, formatos `typst` y `docx`; `project.pre-render` que ejecute `uv run python -m src.pipeline report` (probar si funciona; si no, dejar documentado el orden alternativo).
2. `report/apa.csl` descargado de `https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl`; comprobar sha256 `3917def5fc951b104d64216c3373096042368b9704ba269ca83c14ebaba889fc`; si difiere, avisar antes de usarlo.
3. `stage_report`: copia byte a byte de `report/_variables.yml` a `_variables.yml` (raíz), con relectura y comparación de sha256, más tests (copia, copia alterada, idempotencia, `test_root_variables_in_sync`).
4. `report/informe.qmd` mínimo con: `{{< var modelo1.n_obs >}}`, `{{< include ../outputs/tables/model1_coefficients.md >}}`, la figura `../outputs/figures/model1_coefficients.png` con pie y fuente, y la cita `[@newey1987]`.
5. Aceptación: PDF (Typst) y docx se generan; sin `?@`, `?var`, `{{<` ni restos; versiones de Quarto, Pandoc y Typst anotadas. Si algo falla, avisar al autor antes de cambiar de formato.
6. No tocar `data/raw/`, `docs/guia-profesor.md`, specs aprobadas ni la skill `informe-quarto` hasta que el autor lo apruebe (plan §8).

## S2 — Inventario de interfaz (tras S1)
Generar `specs/006-informe/interfaz.md`: todas las claves de `report/_variables.yml` y todas las tablas y figuras de `outputs/` que las secciones 1–9 pueden usar, con una línea de descripción por clave y su spec de origen. Claude solo usará lo listado.

## Respuesta de Claude al humo (12-oct-2026)
Leí `docs/render-humo-006-2026-10-12.md` y `solicitudes-codex.md` y vi `preview.png`. S1 queda **cumplida solo en su parte de humo**; `stage_report`, el gancho, los tests y `.gitignore` siguen pendientes del plan aprobado. Cambios que incorporé al plan (v2): `format.typst.citeproc: true`, `quarto.exe` por ruta absoluta con el gancho llamando a `uv`, y una nueva sección 3b: **tablas de presentación** generadas por código desde los CSV aprobados, porque `model1_coefficients.md` no cabe en el PDF. No se editan las salidas de 003/004/005. Tras la aprobación del plan, la primera tarea de Codex es 3b + S2 (interfaz), y yo no escribo 4–7 hasta ver el aspecto real.

## Solicitud de claves para T4 (turno exclusivo tras T3; contrastada con `interfaz.md` generada el 12-oct-2026)
Método: comparé cada hallazgo heredado y cada requisito de redacción de la spec 006 con las 871 entradas de `interfaz.md`. **Cubierto, sin petición:** estacionariedad y órdenes de integración (`datos.decision.*`, `datos.orden.*`, `modelo*.no_i0`); meses de 2025T4 (`datos.cpiaucsl_2025t4_meses`, `datos.unrate_2025t4_meses`); coeficientes, efectos de impacto y de largo plazo, signos, robustez y OOS de la 003; diagnósticos (BP, White, JB, RESET, Chow 2008T3 y 2020T2, CUSUM, VIF) de ambos modelos; K, AIC, BIC, Granger, lectura de la regla, perfil φ y trayectoria de la 004; todas las claves `estres.*` del plan §5 de la 005, incluidas las sensibilidades, la unión de réplicas fuera de rango y `dif_modelos`. Ninguna se recalcula.

**Pedidas (solo si salen de claves o salidas ya existentes; si no, lo digo y el texto evita la cifra):**
1. **`n_series` (T4 diagnostica primero).** La 001 (RF-1) habla de 13 series descargadas y `datos.n_series` vale 12 (`src/report_vars.py:84`: series principales más las `dralac*` menos `dralacbs`). Pido una clave que distinga, si son distintas, series descargadas y series usadas en el panel, con su descripción, y la decisión escrita de T4 sobre cuál cifra es la correcta. La sección 3.1 usará una sola cifra por concepto.
2. **Inicio de la historia descargada.** Una clave `datos.historia_inicio` (1998T1, spec 001) para decir que la muestra de estimación empieza en `datos.muestra_inicio` y la historia congelada en 1998; así el año no se teclea en la prosa. La muestra desde 1985 no es una cifra de la guía y no se escribe.
3. **Estadístico y p de la condición C2 de la 004.** Hoy `modelo2.lectura.c2` es solo «no». Para explicar que con K = 1 la prueba de Granger (`modelo2.granger.chi2`, `p`) y C2 son el mismo contraste, pido `modelo2.lectura.c2_chi2` y `modelo2.lectura.c2_p` si ya están en el JSON de la 004. Si no están, la sección dirá que coinciden sin dar una segunda cifra.
4. **Conteos de literatura** (familia «PENDIENTE T4»): `literatura.n_estudios_verificados`, por tema 2.1 a 2.4 y 2.5, `literatura.n_pendiente_lectura` y `literatura.n_descartados`, desde la matriz con solo filas «verificado» para el texto. Más la tabla de 2.5 (`lit_estudios`).
5. **Bandas y réplicas.** Las claves `estres.replicas.n` y `semilla` existen. Pido el nivel de las bandas como variable (`estres.replicas.banda_inf`, `banda_sup`, 5 y 95 %) si figura en las salidas de la 005; si no, el texto usa solo los nombres de claves `*_p05` y `*_p95` en una nota de tabla.
6. **Escenario D.** Número de trimestres con alza observada de ΔFFR y de ceros explícitos del escenario D, y trimestre de inicio y fin del episodio, **solo si se pueden leer de `stress_paths` o de las salidas**; si no, el texto de 7 lo describe sin cifra.
7. **`fred2026`** (T4): URL final y `verify_refs.py` con código 0, como ya prevé la tarea.

**No pedidas a propósito (no existen y no se calculan):** R² sin dummies de impulso, coeficientes del entrenamiento 2000–2019 de la 003, equivalente en dólares, estimador restringido. Las secciones lo dicen como limitación, sin cifra.

### Precisiones sobre los puntos 1 y 4 (tras la cesión de Codex del 12-oct-2026)
- **`n_series` (punto 1).** Datos de Codex: `outputs/data_note.md` enumera 13 series, la spec 001 (RF-1) y `data/raw/manifest.csv` también; `data_variables` da 12 por la fórmula `MAIN_SERIES + columnas dralac*` menos `dralacbs`. T4, ya aprobada, concilia el conteo real sin tocar `data/raw/` ni las salidas 003–005; si la conciliación exige editar una salida histórica protegida, se detiene y se presenta `change`. Mi necesidad concreta: una cifra por concepto (descargadas y usadas en el panel, si difieren) con una descripción de una línea, para la sección 3.1.
- **Signo de la tabla 2.5 (punto 4).** La tabla `lit_estudios` incluye solo filas «verificado» de `research/matriz-literatura.md`; no incluye `asiamah2026` ni `koskei2023` (pendiente-lectura). La spec 006 prohíbe repetir las lecturas dudosas de las observaciones opcionales de la 002 (`koju2018`, `tanaskovic2015`, `nkusu2011`, `jimenez2014a`, `obradovic2026`) mientras la matriz no se corrija por una tarea aprobada. Pido que, para esos cinco, la columna de signo no reproduzca la lectura dudosa (celda vacía con «—» y una nota al pie de la tabla que remita a la matriz), sin cambiar la matriz ni inventar un signo. Codex decide el texto de la nota y me lo comunica.

### Estado (Claude Code, 12-oct-2026)
Solicitud previa a T4 registrada. No contiene cálculos, estimaciones, prosa del informe ni edición de la matriz o de `references.bib`. Escribí solo este archivo. Mantengo las secciones de S1 y S2 y mi respuesta al humo sin cambios.

## Propuesta editorial para el `/sdd-change` de 006 (Claude Code, 12-oct-2026)
Origen: instrucción del autor (informe principal narrativo + anexo técnico separado, sin extensión fija ni evidencia eliminada). Este bloque es insumo para que Codex redacte el `change` y los ajustes de plan y tasks; no modifica spec, plan ni tasks (aprobados) ni contratos. Los IDs de tablas y figuras los fija Codex con `interfaz.md`; aquí van por concepto.

### 1. Comprobación contra la guía oficial (`docs/guia-profesor.md`)
- La guía fija 11 secciones, subsecciones 2.1–2.5, 3.1–3.5 y 6.1–6.4. Para el Modelo I pide «estimar el modelo; analizar los coeficientes; evaluar su significancia; realizar pruebas de diagnóstico». Para 7 pide estimar el riesgo en escenario adverso vs. base y **calcular el cambio**. No menciona anexos: ni los exige ni los prohíbe. La extensión, el formato exigido y si se admite material complementario separado siguen **pendientes con el profesor**.
- Conclusión: separar es compatible **si** el cuerpo conserva las 11 secciones y, en cada una, lo que la guía pide explícitamente (coeficientes principales con significancia, resumen de diagnósticos con su veredicto, cambio adverso − base de ambos modelos). El anexo es respaldo, no sustituto.
- Riesgo: si el profesor exige un único documento, un anexo separado no cuenta. Mitigación: que el anexo sea un documento del mismo proyecto Quarto, renderizable por separado **y** concatenable al final del principal como apéndice APA, para decidir sin rehacer nada. Pregunta nueva para el profesor: ¿se admite material complementario separado?
- Referencias cruzadas: Quarto no resuelve `@tbl-` entre documentos distintos. Propongo etiquetas estáticas generadas por código («Tabla A.7», «Figura A.2») y un test que compruebe que cada «Anexo X» citado en el cuerpo existe en el anexo.
- Se preserva lo hecho: tablas de presentación (`outputs/informe/`), `report/anexos/tablas.qmd`, cuaderno de figuras, variables y tests. El cambio reasigna destino; no regenera estimaciones.

### 2. Criterio de cuerpo vs. anexo
Cuerpo: lo mínimo que sostiene la respuesta de la sección (pocos elementos por sección; más en 4 y 7). Anexo: inventarios (todos los coeficientes, todos los diagnósticos por especificación, robustez completa, 17 estudios con variables y método, desviaciones línea a línea, trayectorias, sensibilidades, límites detallados). La prosa usa cifras solo vía `{{< var >}}` y remite al anexo con una frase («véase el Anexo B»). Sin umbral de extensión.

### 3. Definición por sección
| Sec. | Pregunta que responde | Resultados a explicar | Imprescindible en el cuerpo | Al anexo técnico |
|---|---|---|---|---|
| 1 | ¿Por qué importa y qué se pregunta? | Relevancia para la estabilidad financiera; pregunta y objetivo de la guía; ruta del informe | Ninguna | — |
| 2.1–2.4 | ¿Qué dice la teoría sobre ciclo, determinantes, política monetaria y transmisión? | Mecanismos y qué esperar de cada signo, solo con filas «verificado» | Ninguna | — |
| 2.5 | ¿Quién estimó algo similar, con qué variables y métodos? | Patrón de variables y métodos y contraste con este trabajo, sin repetir signos dudosos | Tabla compacta (autor, muestra, método) o solo prosa si no cabe | Tabla completa de 17 estudios con variables, método y signo/«—» |
| 3.1 | ¿Qué datos y de dónde? | Series, frecuencia, período, fuentes; hueco de oct. 2025 sin imputar; 13 series descargadas | Tabla resumen de series (variable, serie FRED, frecuencia) | Descriptivos, manifiesto de 13 fuentes, estacionariedad completa |
| 3.2–3.4 | ¿Cómo se definen morosidad, regresores y ΔFFR? | Transformaciones y su porqué; ΔFFR = «tasa de interés» = «cambio de la FFR» | Ninguna (prosa) | Transformaciones y órdenes de integración |
| 3.5 | ¿Qué dos modelos y qué se desvía del pre-registro? | Forma de I y II; desviaciones frente a guía y pre-registro (GDPC1, LOANS, 2026T2) en forma legible | Tabla breve de desviaciones relevantes (RF-7) | `model1_deviations`, `model2_deviations` completas |
| 4 | ¿Cómo se asocian las condiciones macro con la morosidad? | Coeficientes en pp por unidad, significancia HAC, incertidumbre; diagnósticos que fallan sin atenuar; lectura para gestión de riesgos | Tabla de coeficientes principales + resumen de diagnósticos (veredicto por prueba) | Salida completa, robustez (GDP, muestras), OOS, VIF, Chow, CUSUM, residuos |
| 5 | ¿Hay efectos rezagados de la política monetaria? | Respuesta dinámica, rezagos K, Granger≡C2 con K=1 (sin segunda cifra), lectura de la regla, límite de endogeneidad | 1 figura (respuesta/trayectoria) + tabla corta de lectura | Perfil φ, selección de K (AIC/BIC), dinámica completa |
| 6.1–6.2 | ¿Qué dice cada modelo? | Síntesis de 4 y 5 sin repetir tablas | Ninguna nueva (remite a 4 y 5) | — |
| 6.3 | ¿Cómo se comparan? | Insumos de `model2_inputs63`; difieren en muestra y controles; sin ponderar | Tabla comparativa compacta | Detalle de insumos |
| 6.4 | ¿Son relevantes macro y política monetaria para el riesgo? | Respuesta a la pregunta fundamental; asociación ≠ causalidad; preguntas probables | Ninguna (prosa) | — |
| 7 | ¿Cuánto cambia la morosidad en estrés adverso vs. base? | Escenarios (adaptación Fed 2026, D con fechas adaptadas), cambio adverso − base de ambos modelos, bandas = incertidumbre de parámetros, sensibilidades y límites | Tabla de cambios por escenario y modelo + 1 figura de trayectorias | Niveles, trayectorias, sensibilidades, regla de tasa, réplicas fuera de rango, limitaciones detalladas |
| 8 | ¿Cómo se usa en una institución? | Siete puntos de la guía conectados a 4–7 y 2; RAE | Tablero de alertas tempranas (cualitativo, sin umbrales) | — |
| 9 | ¿Qué responde el trabajo y cómo anticipar/gestionar el riesgo? | Respuesta directa, no lista de significancias | Ninguna | — |
| 10 | Referencias APA 7 | — | Lista completa | — |
| 11 | ¿Cómo se obtuvieron y reproducen los datos? | La guía anuncia notebook y el proyecto usa pipeline; congelación; hueco; `uv run python -m src.pipeline all` | Ninguna (prosa corta) | Manifiesto y comandos |

Anexos propuestos (mismo proyecto Quarto): **A** Datos y transformaciones; **B** Modelo I completo; **C** Modelo II completo; **D** Estrés completo; **E** Literatura (17 estudios); **F** Desviaciones y reproducibilidad. El cuaderno de figuras se reubica en el anexo que corresponda.

### 4. Panel 5 (p. 29): criterio de lectura cuando Codex entregue las fuentes
Pido a Codex la tabla y la clave de origen de la nota de φ y de la columna «motivo» vacía, y el contrato que las genera. Mi clasificación para cada celda:
- **Identidad por construcción:** valor fijado por la definición del panel o de la regla (p. ej. φ como parámetro de rejilla o de condición, no estimado). Se informa como tal y no se interpreta como evidencia.
- **Resultado estimado:** depende de los datos; se interpreta con su incertidumbre y su lectura (C1, C2 de la 004).
- **Dato no aplicable:** la celda no existe para esa fila (p. ej. una prueba no definida con K=1). Debe mostrar «n.a.» con motivo, nunca vacía.
Sin ver la fuente no concluyo cuál es cuál. Si el «motivo» vacío es un defecto del renderizador, se corrige en la presentación (Codex), no en el contrato de la 004.

### 5. Ajustes previstos en spec (change), plan y tasks, para que Codex los formalice
- **Spec (change):** RF-3 (tablas incluidas con `include` → solo las imprescindibles en el cuerpo, el resto en anexo); estructura obligatoria (anexos A–F y regla cuerpo/anexo); criterios de finalización (cada remisión del cuerpo existe en el anexo); dudas abiertas (material complementario separado).
- **Plan:** salida doble (`informe` y `anexo-tecnico`) más opción concatenada; etiquetas estáticas de anexo; `report/anexos/tablas.qmd` se parte por anexo.
- **Tasks:** nueva tarea de Codex «reorganizar anexos y render doble» antes de T10; mis T5–T9 cambian de alcance (narrativa + remisiones); T11 valida el cruce cuerpo↔anexo; T12 audita que el cuerpo no oculta evidencia requerida. La G1 de la maqueta anterior no se repite (instrucción del autor).
- **No cambia:** cifras solo por `var`, citas verificadas, sin estimaciones nuevas, contratos 003–005, turnos exclusivos.

### Estado
Escribí solo este bloque. No toqué spec, plan ni tasks ni archivos de Codex. Siguiente paso: Codex redacta el `change` y los ajustes con esta propuesta y las fuentes de Panel 5; yo reviso en lectura. Sin commit ni push.

## Solicitud de turno para formalizar el `change` editorial aprobado (Claude Code, 12-oct-2026)
El autor aprobó el `change` (dos documentos, slugs y registro, anexos A–F, T13–T15, nuevo orden) y pidió formalizar spec, plan y tareas bajo SDD coordinando el turno con Codex. Propuesta de reparto, sin escribir nada hasta que Codex ceda por escrito:
1. **Opción recomendada:** turno exclusivo mío, sin tocar código ni tests, solo para `specs/006-informe/spec.md` (v4), `plan.md` (v3) y `tasks.md` (v3), aplicando literalmente `change-editorial-draft.md` §4–§6, con copia de v3 conservada como `spec-v3.md`, `plan-v2.md`, `tasks-v2.md` (hashes antes/después registrados) y una nota «Alternativa combinada» (informe + anexo concatenado, sin presentar su aceptación como confirmada). Codex revisa en lectura y aprueba la fidelidad al borrador.
2. **Alternativa:** Codex escribe esos tres archivos con el borrador como insumo y yo reviso.
3. Codex me indica cuál, confirma que no hay otra escritura ni suite en curso sobre el checkout y me cede por escrito los archivos. T1–T4 quedan sin renumerar; T13–T15 son de Codex.
4. Los fallos del arnés (Playbook, hashing de `frozen_stress`) se tratan aparte; la suite global sigue siendo criterio de cierre. Cuando Codex cumpla T13–T15 y T10 y ceda mis nueve archivos, redacto T5–T9 sin pedir otra aprobación de este cambio.
Estado: solo escribí este bloque. Sin commit ni push.

## Relevo de redacción T5–T9 (Claude Code, 12-oct-2026)
Escribí solo mis nueve archivos de `report/secciones/` y este bloque. No toqué Codex, `src/`, `tests/`, variables, spec, plan, tasks, `MEMORY.md` ni el arnés. Redacción no es revisión independiente; no hay auditoría de mi texto.

| Tarea | Archivos | Control propio |
|---|---|---|
| T5 | `01-introduccion.qmd`, `02-literatura.qmd`, `03f-limitaciones.qmd` | parámetro T5 verde |
| T6 | `04-modelo1.qmd`, `05-modelo2.qmd` | parámetro T6 verde |
| T7 | `06-resultados.qmd` | parámetro T7 verde |
| T8 | `07-estres.qmd` | precondición 005 verificada (review-audit y review-validate APROBADO); parámetro T8 verde |
| T9 | `08-implicaciones.qmd`, `09-conclusiones.qmd` | parámetro T9 verde |

Tras T9 ejecuté `tests/test_report_editorial.py`, `tests/test_harness.py`, `tests/test_report.py` y `tests/test_report_tables.py`: 70 passed. Incluye `test_narrative_task_has_no_unfilled_sections` (T5–T9), claves `var` existentes, cifras a mano, citas y estructura. Grep de «causa», «causal», «provoca», «debido a» en mis archivos: sin coincidencias. No ejecuté la suite global (bloqueada y pendiente) ni renders; no declaro validación global ni T11.

Decisiones de redacción para Codex y la auditoría:
- Cuerpo: tablas `_cuerpo.md` (literatura, coeficientes y diagnósticos del Modelo I, lectura e insumos 6.3 del Modelo II, cambios de estrés) y figuras `model2_response.png`, `stress_model1.png`, `stress_model2.png` sin recortar; el resto se remite por slug (`AT-…`, `AF-…`) en texto. Sin enlaces inventados ni URLs externas.
- Cifras solo por `{{< var … >}}`; sin años sueltos (solo trimestres exactos de contrato, p. ej. 2008T3, 2020T2, 2022T1–2023T3). Ninguna variable ni cálculo nuevo.
- Literatura: solo filas «verificado». Los cinco signos dudosos (`koju2018`, `tanaskovic2015`, `nkusu2011`, `jimenez2014a`, `obradovic2026`) no se reproducen; `asiamah2026` y `koskei2023` no se citan con hallazgo.
- 5: Granger≡C2 con K=1 sin segunda cifra; β_h como asociación condicional con ΔFFR(t) y φ_h como continuación observada de la tasa, sin equivalencia con una secuencia de alzas; φ0 = 1 como identidad.
- 7: D con fechas adaptadas; D = adverso bajo la regla de la tasa; bandas = incertidumbre de parámetros; invariancia al origen con igualdad de desvíos por paso alineado y comparación en el paso final (no por calendario); «dirección predominante» según proporción de réplicas positivas, bandas con cero y niveles fuera de rango y réplicas explosivas informados.
- 8: tablero cualitativo sin umbrales numéricos ni cifras.

Dudas para Codex: (1) el enlace «Abrir anexo» de las tablas `_cuerpo.md` apunta a archivos relativos; confirmar su comportamiento al integrar. (2) En 5 describo la columna `columna_panel` de `model2_stationarity` de forma neutra (columna del panel probada); si el anexo la rotula de otro modo, ajustar. Siguiente acción: Codex renderiza (T11), valida y corre la suite global cuando se resuelvan los fallos del arnés; T12 solo después, con revisores de contexto limpio.

## Cesión
Termino mi turno exclusivo. **Cedo la escritura del checkout a Codex.** Sin commit ni push.
