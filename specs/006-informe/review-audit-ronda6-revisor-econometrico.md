# Ronda 6 de auditoría (paquete ronda 7, comprobación acotada) — revisor-econometrico (contexto limpio)

Copia del mensaje final del subagente `revisor-econometrico`, tomada de la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 7 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda7.json`, SHA-256 69003c83a7c6ccbc69c5cbd23bbeeb43bde0b970792f53748df302ca574535e5). Rondas anteriores conservadas intactas. Nota de coordinación: el identificador «rotuloModeloII» salió del mensaje de relevo de Codex y yo lo atribuí por error al paquete en el encargo; el revisor no lo halló como tal (hallazgo 1).

VEREDICTO: APROBADO

Revisé por contexto limpio el paquete de la ronda 7 de la spec 006. Los tres puntos que pediste están resueltos y no encontré regresiones econométricas. No hay hallazgos críticos ni importantes. No edité nada y no corrí la suite ni el pipeline.

**Versión.** Las SHA-256 de los seis entregables, de las nueve fuentes de Claude, de 03a–03e, de `report/_variables.yml`, de `outputs/informe/stress_delta_nota.md` y de los CSV usados coinciden con el manifiesto. Esos CSV son `model1/2_coefficients`, `model1/2_diagnostics`, `model2_inputs63`, `stress_delta` y `stress_levels`. Para ver qué cambió comparé los `.md` de la ronda 6 con los actuales.

## (a) Hallazgo 1 de mi informe anterior: resuelto
- La nota de la Tabla 6 está en `informe.md:1074-1077` y en `anexo-tecnico.md:1560-1563` (Tabla C.5). Ahora dice «los coeficientes de ambos modelos provienen de sus estimaciones principales».
- Esa frase aparece 1 vez en cada PDF y en cada DOCX. La redacción anterior («el coeficiente del Modelo I proviene») aparece 0 veces.
- La afirmación es cierta. −0,044 sale de `d_ffr` en `model1_coefficients.csv` y −0,084 de `d_ffr_l0` en `model2_coefficients.csv`. Ambos son la estimación principal.

## (b) Cortes de tabla y rótulo de pre-registro
- **Tablas 2, 4 y 6 en el PDF del informe.** Cada una queda entera en una página: la Tabla 2 en la página 10, la 4 en la 16 y la 6 en la 22. Eso incluye título, todas las filas, fuente y nota; la última fila (USREC, CUSUM y Modelo II) no pasa a la página siguiente.
- **Rótulo.** En las Tablas F.2 y F.3 (`anexo-tecnico.md:4825-4827` y `:4844`), «Pre-registro de la especificación pre-registrada» pasó a «Pre-registro del Modelo I» (C1–C3, del 2026-10-05) y a «Pre-registro del Modelo II» (C1, del 2026-10-08).
- **Sentido conservado.** Las fechas coinciden con `specs/003-modelo-i/spec.md:287` y `specs/004-modelo-ii/spec.md:242`. El reemplazo lo hace `src/report_tables.py:193-194`: spec 003 pasa a Modelo I y spec 004 a Modelo II. La forma tautológica ya no aparece en los PDF ni en los DOCX.

## (c) Regresiones
- **Tabla 6.** −0,044 (p 0,269, 106 obs.) y −0,084 (p 0,190, 105 obs.) coinciden con `model2_inputs63.csv` y con los dos archivos de coeficientes.
- **Tabla 7** (`informe.md:1267-1290`). Los valores 1,428 / 1,898 / 2028T3 y 0,827 / 1,286 / 2028T3 coinciden con `stress_delta.csv`, en adverso y en D, y con `_variables.yml:1103-1161`. Las advertencias de niveles fuera de rango también coinciden con `_variables.yml:1126-1129` y `:1168-1171`:
  - Modelo I: 105 réplicas, 0,011, −10,323 y 6,497.
  - Modelo II: 160 réplicas, 0,016, −6,120 y 9,921.
- **B.2 y C.3** (`anexo-tecnico.md:578-603` y `:1455-1481`). Todos los estadísticos, p-valores, veredictos y VIF (36,811 y 33,154) coinciden con `model1_diagnostics.csv` y `model2_diagnostics.csv`. La Tabla 4 del informe es idéntica a la B.2.
- **Regla de la tasa.** Se enuncia una sola vez, en la sección «La regla de la tasa» (`informe.md:1253-1263`). Las otras apariciones solo remiten a ella:
  - el pie de la Tabla 7 (:1284-1285), que RF-9 exige;
  - :1316-1317;
  - la pregunta de :1164-1169, que viene de la sección 06 sin cambios desde la ronda 6.

  Es coherente con `outputs/models/model2_main.json`, cuya lectura es «sin evidencia».
- **Nota de estrés.** `stress_delta_nota.md` es idéntica por SHA a la de la ronda 6. Cumple RF-9 (`specs/005-estres/spec.md:95`): fija ΔFFR en cero mientras la lectura no sea de evidencia fuerte y lo declara al pie.
- **Lenguaje causal.** «Provoca», «efecto causal» y «se invierte» aparecen 0 veces en los cuatro PDF/DOCX. La única «causa» (`anexo-tecnico.md:1103`) es «causa de no estimación», no una frase causal.
- **Cambio en la sección 02.** Ahora dice «en la mayoría de los estudios», con el desempleo negativo de Obradović (`informe.md:293-312`). Sigue siendo coherente con las conclusiones («mayor parte de la literatura verificable», `:1580`) y resuelve la observación 3 de mi informe anterior.

## Hallazgos (menores, no bloquean)
1. **Menor, sobre el pedido.** El identificador «rotuloModeloII» no está en `docs/paquete-auditoria-006-ronda7.md` ni en ningún otro archivo del repositorio. El cambio de rótulo del Modelo II solo se describe en `docs/correcciones-tecnicas-006-ronda7.md:21`. Revisé el rótulo real en F.3 y en el código, y es coherente.
2. **Menor, solo observación.** En la fila obradovic2026 del Anexo E (`anexo-tecnico.md:4751`) sigue «El guion remite al signo descrito en la sección 2.5». R5-3 quitó esa autocita solo de la nota de la Tabla 1. No es un tema econométrico y no lo exijo.
3. **Menor, límite de formato.** El DOCX no tiene propiedades para mantener juntas las Tablas 2, 4 y 6 (0 `w:keepNext` y 0 `w:cantSplit`). El bloque indivisible de R5-1 vale solo para el PDF de Typst. En Word o en Google Docs esas tablas podrían cortarse. El paquete no afirma lo contrario.

## Lo que no pude verificar
- **Páginas como imagen.** Comprobé los cortes del PDF solo por el texto extraído con `pdftotext`, porque no hay herramienta para convertir páginas a imagen.
- **Word, Google Docs y enlaces.** No vi la paginación en Word ni en Google Docs, y no probé los enlaces.
- **Tests y doble corrida.** No corrí `pytest` ni el pipeline, por instrucción.
- **Citas.** No revisé citas ni DOI.

Lo que defendería ante el profesor:
- Las cifras de las Tablas 6 y 7 y de B.2/C.3 salen sin cambios de los CSV y de `_variables.yml`.
- La tasa vale cero en el estrés por una regla fijada antes de estimar. El informe la enuncia una vez y la declara al pie de la tabla, como pide RF-9.
- Los rótulos de pre-registro remiten al modelo correcto, con fechas que coinciden con las desviaciones registradas en las specs 003 y 004.

Lo que me preguntaría el profesor:
1. Si ambos coeficientes de ΔFFR vienen de la estimación principal, ¿por qué difieren las muestras (106 frente a 105) y los controles?
2. ¿Por qué el Chow de 2008T3 falla en el Modelo I y pasa en el Modelo II?
3. Con la tasa en cero, ¿qué aporta el Escenario D además de repetir el adverso?
