# Ronda 5 de auditoría (paquete ronda 6, acotada) — revisor-econometrico (contexto limpio)

Copia del mensaje final del subagente `revisor-econometrico`, tomada de la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 6 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda6.json`, SHA-256 3d25d637c56efff6b335254db0691eee13378d00d8fd45c157cf2331a4e8448a). Rondas anteriores conservadas intactas. Nota de coordinación: el revisor ejecutó por su cuenta `uv run pytest -q` (967 passed, 567 warnings, rc 0, 829 s); no se le había pedido y no cambia el veredicto.

VEREDICTO: APROBADO

Los puntos de mi informe de la ronda 4 siguen resueltos. Las correcciones de esta ronda no introducen regresiones econométricas y la nota de estrés cumple RF-9. No encontré nada crítico ni importante. Los tres puntos de abajo son menores y no bloquean.

**Cómo lo comprobé**
- **Versión.** Los SHA-256 de los seis entregables, de la nota de estrés, de las 9 fuentes de Claude, de 03c/03e y de `report/_variables.yml` coinciden con el manifiesto de la ronda 6. Siguen iguales después de correr la suite.
- **Texto.** Saqué el texto de los PDF con `pdftotext` y el de los DOCX desde `word/document.xml`. Lo comparé con los .md y con los entregables guardados de la ronda 5 (`outputs/preview-006-ronda5-evidencia/report/`).
- **Tests.** `uv run pytest -q` da 967 passed, 567 warnings, rc 0 (829 s).

## (a) Puntos de la ronda 4
| Punto | Estado | Evidencia |
|---|---|---|
| Cifras | Coinciden | Tabla 6 (informe.md:1050-1053) frente a `model2_inputs63.csv` y los dos `*_coefficients.csv`: −0,044 (p 0,269; 106 obs.) y −0,084 (p 0,190; 105 obs.). Tabla 7 frente a `stress_delta.csv` y `_variables.yml`: 1,428 / 1,898 / 2028T3 y 0,827 / 1,286 / 2028T3. B.2 y C.3 frente a `model1_diagnostics.csv` y `model2_diagnostics.csv`: todos los estadísticos, p-valores y veredictos, más los VIF de 36,811 y 33,154. |
| Regla de la tasa | Una sola vez | Se enuncia en informe.md:1237-1243 y solo se remite a ella en :1299-1300. Coincide con `specs/005-estres/spec.md:95` (RF-9) y con `outputs/models/model2_main.json`, que dice «sin evidencia». |
| Lectura de signos del estrés | Intacta | La fuente 07 es la misma por SHA. «Se invierte» aparece 0 veces en los seis entregables. |
| VIF | Bien | «infla su error estándar y no explica su significancia» aparece 3 veces en el PDF y en el DOCX del informe. «no la hace significativa» aparece 0 veces. Las etiquetas están en español: 0 apariciones de «VIF (d_», «d_ffr_l» y «d_unemp». |
| Lenguaje causal | Ninguno | «provoca» y «efecto causal» aparecen 0 veces. La única «causa» (anexo-tecnico.md:1102) es «causa de no estimación», no una frase causal. |
| Tabla 6 | Bien | La nota nueva ya no remite a decisiones internas y conserva «asociaciones condicionales con errores HAC». |

## (b) Cambios de esta ronda
- **Notas de CUSUM en B.2 y C.3 (anexo-tecnico.md:584-586 y :1460-1462).** Dicen «la salida del modelo no exporta un estadístico ni p-valor; se informa el veredicto. Los vacíos o guiones no representan ceros». Es correcto: los CSV dejan esas celdas vacías en el Modelo I y con «—» en el Modelo II. Las figuras CUSUM quedan dentro de las bandas del 5 %, así que el «pasa» se sostiene.
- **Panel 2 de B.2 y C.3 (:613-615 y :1490-1492).** Es neutro. Las notas de Chow y CUSUM coinciden literalmente con la columna `nota` de los CSV.
- **03c y 03e.** «Pre-registro» es uniforme: «preregistr» y «prerregistr» aparecen 0 veces. «Crédito rezagado» (03e:44) es coherente con CRED₍t−4₎ (03e:15, :29). La selección por BIC sobre una muestra común y las «asociaciones condicionales» siguen correctas.
- **«Mínimos cuadrados generalizados factibles (FGLS)».** Está en el informe (:248, :282) y en el anexo (:4724). «generalizables» aparece 0 veces.
- **Tabla 1 en dos páginas.** Por el texto, las filas están en las páginas 6-7, el encabezado se repite en la 7 y la nota está en la 7. La nota sobre Obradović coincide con `research/matriz-literatura.md:40` (tasa de préstamo positiva, distinta de la tasa de política).

## (c) `outputs/informe/stress_delta_nota.md`
Cumple RF-9. Dice que los coeficientes de ΔFFR se fijan en cero mientras la lectura no sea de «evidencia fuerte», y la lectura es «sin evidencia». Las advertencias coinciden con `stress_levels.csv` y `_variables.yml:1125-1129, 1167-1171`: 105 réplicas, 0,011, −10,323 y 6,497 en el Modelo I; 160, 0,016, −6,120 y 9,921 en el Modelo II. La frase aparece 1 vez en el informe y 8 en el anexo, en PDF y DOCX. Es el mismo recuento que en la ronda 5. En mi informe anterior escribí «2 veces» en el informe; ese conteo era un error mío, no una regresión.

## Hallazgos (todos menores, ninguno bloquea)
1. **Menor. informe.md:1059-1062 (y anexo-tecnico.md:1560-1562).** La nota de la Tabla 6 dice que «el coeficiente del Modelo I proviene de su estimación principal», pero no dice lo mismo del Modelo II. Su θ0 también sale de su estimación principal (`model2_coefficients.csv`, d_ffr_l0). El lector puede pensar que el del Modelo II tiene otro origen. Sugerencia: «ambos coeficientes provienen de la estimación principal de cada modelo».
2. **Menor y cosmético. informe.md:746-747 frente a anexo-tecnico.md:584.** La explicación de CUSUM dice lo mismo con palabras distintas («en esta salida» frente a «la salida del modelo»). No hace falta corregirlo.
3. **Observación fuera de alcance, no es un requisito.** La matriz (:40) registra que en Obradović el desempleo tiene signo negativo, inesperado según los autores. La síntesis de 2.5 (informe.md:293-295) cita solo los tres estudios con signo positivo. La sección 02 está cerrada por decisión del usuario; solo lo señalo para que lo tenga presente.

## Lo que no pude verificar
- **Las páginas como imagen.** No hay `pdftoppm` instalado, así que comprobé la Tabla 1 en las páginas 6-7 solo por el texto, no por cómo se ve.
- **Word, Google Docs y los enlaces.** No los abrí en Word ni en Google Docs y no probé los enlaces con clic. Sí comprobé que los destinos de las páginas 52, 66, 113, 140 y 147-149 tienen el panel correcto.
- **Doble corrida.** No corrí el pipeline dos veces.
- **Citas.** No revisé citas ni DOI.

Lo que defendería ante el profesor:
- La tasa vale cero en el estrés por una regla fijada en la 004 antes de estimar. La 005 la aplica sin cambios (RF-9) y el informe la enuncia una vez.
- Los diagnósticos fallidos (BP, White, JB, RESET y el Chow de 2020T2) están reportados con su consecuencia. Los vacíos de VIF y CUSUM se explican y no se presentan como ceros.
- Todas las cifras auditadas coinciden con los CSV y con `_variables.yml`.

Lo que me preguntaría el profesor:
1. ¿Por qué el CUSUM pasa y los Chow de 2008T3 y 2020T2 fallan en el Modelo I?
2. ¿Por qué el VIF del desempleo pasa de 10 en los dos modelos, y por qué en el Modelo I se atribuye a las dummies de la pandemia?
3. Si el producto y ΔU solo sobreviven en 3 de 9 y en 1 de 9 variantes de robustez, ¿cuánto pesa el Δ final de 1,428 pp?
