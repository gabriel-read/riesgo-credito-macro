# Ronda 2 — revisor-econometrico (contexto limpio)

Copia del mensaje final del subagente `revisor-econometrico`, tomada del texto recibido en la notificación de finalización (las entidades `&lt;` y `&gt;` son tal como llegaron). Coordinó Claude Code; autoría del informe auditado: Claude (01, 02, 03f, 04–09) y Codex (3a–3e, 10, 11, tablas, figuras, anexos, infraestructura). Versión auditada: informe.pdf 97c614ac…, anexo-tecnico.pdf b69f250d…, informe.docx 8d212275…, anexo-tecnico.docx 136fb3c8….

VEREDICTO: CAMBIOS NECESARIOS

**Alcance.** Revisé solo lectura y con contexto limpio. Leí:
- la spec 006 y el pre-registro de la regla de tasa de la spec 005;
- las 16 fuentes de `report/secciones/`, `report/_variables.yml` y las tablas de `outputs/tables` y `outputs/informe`;
- el texto de los dos PDF (`pdftotext -raw`) y de los dos DOCX;
- las anotaciones de enlace del PDF, y las figuras `stress_model1.png` y `model2_response.png`.

Comprobé que los 213 valores `{{&lt; var &gt;}}` del cuerpo aparecen en `informe.pdf`. También coincidieron con los CSV todos los valores que contrasté: coeficientes y diagnósticos del Modelo II, LP h0/h4/h12, robustez, delta del estrés, sensibilidad de tasa y sensibilidad de calendario. No hay cifras escritas a mano; solo fechas y rótulos. No ejecuté pytest ni renders porque se me pidió no hacerlo.

## Hallazgos de la ronda 1 → estado

| # | Hallazgo ronda 1 | Estado | Evidencia |
|---|---|---|---|
| 1 | La 6.3 describía mal los modelos y leía selectivamente el desempleo | **Parcial** | Corregido: términos compartidos (06-resultados.qmd:29-31), controles del Modelo II con ΔU(t−1) significativo (06:48-52), evidencia mixta en 06:61, 09:13 y 04:43. **Queda pendiente:** no se informa PIB(t−1) del Modelo II (ver N1). |
| 2 | «Anticipar» usado con regresores contemporáneos y simultaneidad no declarada | Resuelto | 09-conclusiones.qmd:30-31; 08-implicaciones.qmd:11, :14, :48-49; 04-modelo1.qmd:75; 03f-limitaciones.qmd:34 |
| 3 | Faltaban limitaciones en el cuerpo | **Parcial** | Tasa cero, R2/R3 y K condicional en 05-modelo2.qmd:75-81; PPP, efectos base y R1 parcial en 04:55-56. Faltan las ventanas de LP que cruzan la COVID sin dummy. El mapeo de robusteces quedó mal (N4). |
| 4 | Notación de los p-valores | **Parcial** | Ya no hay «0,100» del KPSS, p = 0,000 pasó a «&lt; 0,001» y el Chow a «&lt; 0,001» (model1_diagnostics_cuerpo.md). Pero conviven «≥ 0,10» (model1_stationarity_anexo_2.md:3-9; 7 veces en el anexo) y «&gt; 0,10» (58 veces). La spec 006:82 exige una sola notación. |
| 5 | Remisiones sin enlace (RF-14b) | Resuelto, con regresión | El PDF tiene 55 enlaces `anexo-tecnico.pdf#nameddest=…` hacia 31 destinos, y todos existen en el anexo. El DOCX tiene 31 enlaces externos al anexo. Regresión editorial en N7. |
| 6 | Escala φ₄ | Resuelto | 05:55-56 |
| 7 | Granger y C2 | Resuelto | 05:33-34 |
| 8 | Pérdida de un trimestre | Resuelto | 06:41 |
| 9 | Niveles fuera de rango | Resuelto | 07-estres.qmd:86-88. La frase de :88 es confusa, pero no es error. |
| 10 | RF-7 y RF-13 | Resuelto | 03e-desviaciones.qmd:55; 11-datos-descarga.qmd:23-24 |
| 11 | Restos editoriales e identificadores de código | **Parcial** | 03f:1, 04:10, 11:20 y el pie «Fuente» están corregidos. Tabla 4 sigue con «VIF (y_lag)», «VIF (gdp_growth)»… y celdas VIF vacías (model1_diagnostics_cuerpo.md). La nota de Tabla 7 dice «modelo1/modelo2». |
| 12 | Frases causales | Resuelto | 02-literatura.qmd:28; 09:14 |
| 13 | Trazabilidad de la variable d_ffr | Resuelto | 04:54 |
| 14 | Ventana HAC del Modelo II | Resuelto | 05:15 |
| 15 | Tamaño del Chow 2020T2 | Resuelto | 04:71; 05:66 |
| 16 | Legibilidad del anexo | Resuelto | Panel 4 de AT-M1-ROB con «Término» (anexo, p. 36); Anexo A con «Variable» |
| 17 | Remisiones de la sección 7 | Resuelto | 07:98, :115 |

## Hallazgos nuevos o residuales

### Importantes

**N1. Se omite un control del Modelo II que contradice la conclusión principal.**
- Archivos: 06-resultados.qmd:48-52 y :60; 09-conclusiones.qmd:3 y :12; 08-implicaciones.qmd:3.
- La 6.3 informa π(t−1), CRED(t−4) y ΔU(t−1) del Modelo II, pero no PIB(t−1): vale +0,001 con p = 0,823, signo contrario al del Modelo I (model2_coefficients.csv).
- Aun así, la frase inicial de la sección 9 dice que el ciclo se asocia con la morosidad «sobre todo a través de … la actividad acumulada».
- El respaldo es solo del Modelo I: impacto con p = 0,110, largo plazo con p = 0,043 y robustez en 3 de 9 variantes.
- Por qué importa: es la misma lectura selectiva del hallazgo 1, ahora con el producto. Además, la respuesta a la pregunta de investigación (RF-11) la exagera.
- Qué se espera: informar PIB(t−1) en la 6.3 y rebajar «actividad» en 9:3 y 8:3 a evidencia débil, que depende del modelo.

**N2. Se atribuye mal la regla pre-registrada de tasa cero.**
- 07-estres.qmd:59 dice que la tasa se fija en cero «por la regla pre-registrada ante su signo contrario al esperado».
- 06-resultados.qmd:84 enlaza «esa regla» con el signo contrario y la falta de significancia.
- La regla real (specs/005-estres/spec.md:64, RF-9) es otra: los coeficientes de ΔFFR valen cero mientras la lectura de la 004 no sea «evidencia fuerte». El propio informe lo dice bien en 07:43.
- Por qué importa: presentada así, la regla parece una decisión tomada al ver el signo. Eso debilita la defensa del pre-registro.
- Qué se espera: alinear 07:59 y 06:84 con 07:43.

**N3. La notación del KPSS acotado no es única.**
- Es el residual del hallazgo 4 (ver tabla) e incumple la spec 006:82.
- Qué se espera: que el adaptador use una sola forma en el Anexo A, en AT-M1-STATIONARITY y en AT-M2-STATIONARITY.

**N4. Se dice que la robustez cubre límites que no cubre.**
- 05-modelo2.qmd:75-80 presenta «tres límites de potencia»: tasa cero, K elegido con los mismos datos y efectos base. Luego dice que «dos variantes de robustez tratan los dos primeros».
- Es falso. R3 trata la tasa cero. R2 (sin 2020–2021) trata la COVID y los efectos base, como dice model2_limitations.csv: «R2 … sirve de contraste».
- Ninguna variante trata la elección de K: R1 «no aplica» porque AIC y BIC coinciden.
- Además, ni K condicional ni los efectos base son límites de potencia.
- Qué se espera: corregir el mapeo y la etiqueta de esos límites.

**N5. En el estrés, el texto insinúa un origen del cambio que las variables robustas no sostienen.**
- 07-estres.qmd:56-59. El texto declara bien que no hay descomposición. Pero la frase de :58 nombra solo el desempleo y menciona que la inflación y el crédito son «las más estables», lo que sugiere que esas dos sostienen el cambio.
- Según AT-EST-PATHS y los signos de los coeficientes ocurre lo contrario:
  - el crédito es idéntico en los dos escenarios, así que no aporta nada;
  - la inflación baja en el adverso (de −0,1 a −1,4 pp) con coeficiente positivo, así que resta;
  - el cambio de 1,428 pp descansa entonces en el PIB (robusto en 3 de 9) y en ΔU (robusto en 1 de 9).
- Por qué importa: el profesor puede preguntar de dónde sale el cambio, y la respuesta actual induce a error.
- Qué se espera: una de dos.
  - Borrar la frase de :58.
  - O sustituirla por una lectura de signos, sin cifras: el crédito no aporta, la inflación compensa y el cambio depende de los coeficientes menos robustos. Si se elige esta opción, debe aprobarla el autor, porque toca el límite de «no descomponer».

### Menores

- **N6. «De forma estable».** 06:3 y :97; 08:9; 04:96 hablan de estabilidad mientras el Chow rechaza la estabilidad conjunta: en el Modelo I en 2008T3 y en 2020T2. Conviene decir «robusta a las variantes».
- **N7. Letra del anexo duplicada.** Es una regresión de la corrección de enlaces. Ejemplos en `informe.pdf`: «Anexo B, AT-M1-COEFFICIENTS, Anexo B», «como Anexo B, AT-M1-COEFFICIENTS (Anexo B)» (p. 4, desde 01:42) y «Anexo D, Anexo D, AT-EST-LIMITATIONS» (p. 28, desde 07:125). El origen es que el filtro antepone la letra y la fuente ya la escribe.
- **N8. Bandas de las proyecciones locales.** 05:47 dice que «incluyen el cero», y es cierto. Pero en h = 1–3 el límite superior al 90 % es 0,003, 0,001 y 0,005: una asociación negativa casi al borde. Conviene decirlo y ligarlo a la endogeneidad.
- **N9. Uso de la alerta de VIF.** 06:50 y :61 y 09:13 usan «alerta de colinealidad» para atenuar un coeficiente que sí es significativo. Un VIF alto infla el error estándar; no fabrica significancia.
- **N10. Ventanas LP y COVID.** El cuerpo no menciona que las ventanas de las proyecciones locales cruzan la COVID sin dummy. Solo está en el anexo.
- **N11. Lógica de una frase.** 08:16: «se monitorea … porque varió poco fuera de la pandemia».
- **N12. Literatura sobrevendida.** 02:3 dice que la literatura «respalda» la relación entre política monetaria y riesgo de crédito, pero 2.3 y 2.4 dicen que ningún estudio mide la morosidad.

## Checklist de la skill

- Estacionariedad: las tablas de ambos modelos están en el anexo.
- Errores HAC: ventana de 4 en ambos modelos; en las LP, de 4 a 13, siempre ≥ h + 1.
- Selección de K: sobre una muestra común (n = 105).
- Signos frente a lo esperado: discutidos, salvo N1.
- Frases causales: ninguna grave.
- Diagnósticos fallidos: reportados.
- Reproducibilidad: no la verifiqué.

## Lo que no pude verificar

- No ejecuté `uv run pytest -q` ni el pipeline, por instrucción, así que tampoco la doble corrida idéntica.
- No vi las páginas como imagen (falta `pdftoppm`). Revisé el texto y las anotaciones. Con `-layout`, Tabla 4 salía con los p del Chow desplazados a las filas VIF; con `-raw` sale correcta, así que lo trato como artefacto de extracción.
- No probé los enlaces con clic en un visor, en Word ni en Google Docs.
- Los PDF son de las 00:23–00:34 y `_variables.yml` y `outputs/informe/*.md` se regeneraron a la 01:15. Comprobé que los valores del cuerpo están presentes en el PDF, pero no recorrí todo el anexo contra las tablas actuales.
- Las citas quedan fuera de mi alcance (verificador-citas).

## Lo que defendería ante el profesor

- «Sin evidencia» sale de una regla fijada antes de estimar, se presenta con RESET, Chow y endogeneidad a la vista, y R2 y R3 no la cambian.
- Las cifras salen de las variables, y las 31 remisiones del cuerpo enlazan a destinos que existen en el anexo.
- El estrés declara su dependencia del calendario (1,736 pp frente a 0,340 pp) y no trunca las réplicas.

## Lo que me preguntaría el profesor

1. Si en el Modelo II el PIB rezagado tiene signo positivo y no es significativo, ¿por qué la conclusión pone la actividad entre los canales principales?
2. Si la inflación baja en el adverso y el crédito no cambia, ¿qué sostiene los 1,428 pp, y cuánto confía en esos coeficientes?
3. ¿La tasa se fijó en cero porque su signo era contrario o porque la lectura no fue «evidencia fuerte»? ¿Se decidió antes de ver los resultados?
