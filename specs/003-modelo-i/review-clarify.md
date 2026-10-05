# Review Clarify — Spec 003 Modelo I

**Fecha:** 2026-10-05
**Revisor:** QA (OpenCode)
**Skills aplicadas:** `sdd`, `econometria-series-tiempo` (dominio de la spec); `datos-fred` y `informe-quarto` para los puntos que tocan datos congelados y salida al informe.
**Alcance:** solo detección. No propongo soluciones.

**Evidencia leída además de la spec:** `docs/constitution.md`, `docs/guia-profesor.md`, `specs/001-datos/spec.md`, `outputs/tables/stationarity.md` (tabla ya generada), `data/raw/manifest.csv`, `outputs/data_note.md`, `data/processed/panel.csv` (cabecera), `MEMORY.md`, AGENTS.md.

---

## 1. Ambigüedades (requisitos que no se pueden verificar)

1. **RF-11 no nombra el artefacto ni su forma** (línea 111). Dice «reportará junto al modelo el ADF/KPSS…», pero los criterios de finalización (línea 156) hablan de «la tabla de ADF/KPSS del modelo». No hay nombre de archivo, ni columnas, ni si es una tabla propia o una sección de la de diagnósticos: el criterio de finalización no se puede comprobar contra el RF.

2. **RF-11 pide decisión y orden de integración «en la forma en que entran» y esa información no existe para ΔU y ΔFFR.** En `outputs/tables/stationarity.md` las filas «primera diferencia» de `unrate` y `fedfunds` no tienen `decision` ni `orden` (solo el estadístico y el p-valor), y la spec 001 (Definiciones, RF-19) excluye expresamente las columnas de diferencia trimestral de la decisión. Para ΔU y ΔFFR, el «orden de integración» que RF-11 exige no está en ninguna tabla.

3. **RF-3 presupone filas identificables en la tabla de la spec 001.** La decisión existe (`outputs/tables/stationarity.md`), pero la spec 003 no fija con qué claves se lee cada dependiente alternativa (`dralacbn` + `tal cual`, `dralacbs_logit` + `tal cual`, etc.). «Leerá de la tabla» no es verificable sin esas claves.

4. **No se dice cuál muestra manda: la de la decisión o la de la regresión.** La tabla de estacionariedad está calculada con 106 observaciones (2000T1–2026T2, panel completo) y la regresión principal no puede usar 2000T1 (necesita Y(t−1)), así que tendrá 105. No hay regla sobre qué ocurre si una decisión cambia al recalcularla sobre la muestra efectiva.

5. **R5 no dice en qué forma entra el logit y RF-15 razona como si fuera en niveles** (líneas 80, 117). La decisión de la spec 001 para `dralacbs_logit` es «primera diferencia», con orden «posible I(2)» (`outputs/tables/stationarity.md`, fila 5). RF-3 manda la forma según esa decisión, mientras R5 y RF-15 están redactados como si la dependiente fuera el logit en niveles. No se puede verificar qué se estima, ni qué limitación se declara por el «posible I(2)».

6. **R2 no dice cuál trimestre es la base de las tres dummies estacionales** (línea 77) ni qué se espera de ellas cuando la dependiente forzada por RF-3 es la diferencia trimestral (la decisión de `dralacbn` es «ambigua (primera diferencia)», I(1)). Sin trimestre base ni criterio, la variante no es reproducible ni interpretable.

7. **El principio «cada variante cambia una sola cosa» (línea 75) no se cumple en R1 ni R2.** R1 cambia muestra y dummies a la vez; R2 cambia dependiente y añade tres dummies. Contradicción interna del propio catálogo de robustez (desarrollado en el punto 3 de la sección 2).

8. **El p-valor del efecto de largo plazo no está definido en ninguna parte.** RF-18 (línea 124) exige, por regresor, «impacto y largo plazo por 1 pp y por 1 DE con su IC 95 % y p-valor», pero RF-6 y la Definición de «Efecto de largo plazo» (línea 34) solo dan error delta e IC 95 %. No hay regla de cómo se obtiene ese p-valor (con qué estadístico y qué grados de libertad), así que RF-18 no es verificable en ese campo.

9. **No se fija la distribución de referencia de t, p-valor e IC 95 %.** RF-5 y RF-6 los exigen; nada dice si es normal o t con T − k grados de libertad. Con N ≈ 105 y 11 parámetros la diferencia es pequeña pero existe, y el criterio de finalización exige cifras idénticas entre corridas, no entre convenciones.

10. **No se dice cómo entra «no definido» en las variables del informe.** RF-6 obliga a reportar el largo plazo como «no definido» si ρ̂ ≥ 1; ese texto no es un número y ninguna RF dice si en `report/_variables.yml` va como cadena, como nulo o como variable ausente. Sin eso, RF-18 y el informe (que no admite cifras tecleadas) quedan sin camino.

11. **La reconstrucción del nivel en la validación fuera de muestra admite dos lecturas distintas** (línea 89). «Si Y está en diferencias, el pronóstico del nivel se reconstruye acumulando desde el último nivel observado» puede significar (a) nivel observado en t−1 más el ΔY pronosticado, o (b) suma acumulada de los ΔY pronosticados. Son números distintos, y el cociente modelo/ingenuo y el Diebold-Mariano de RF-16 cambian según cuál se use. No se puede verificar.

12. **El denominador del recuento de robustez no está fijado** (RF-14, línea 116). «En cuántas variantes es robusto» no dice si el denominador son 8 variantes o 10 regresiones, porque R3 aporta tres columnas (una por sub-cartera). Tampoco dice si R3 cuenta una vez, tres veces o si alguna de las tres sub-carteras que no son robustas invalida la variante.

13. **No existe el criterio de juicio que HU-5 promete** (línea 23). RF-16 calcula RMSE, MAE, cociente y p-valor de Diebold-Mariano, pero ninguna RF dice qué veredicto produce esa salida ni con qué umbral se decide si el modelo «supera» al paseo aleatorio. La salida es calculable y no juzgable.

14. **El CUSUM no está identificado.** RF-9 (línea 109) y RF-10 (línea 110) dicen «CUSUM» sin especificar si es de residuos, de residuos al cuadrado (heterocedasticidad) o de la estadística acumulada, ni cómo se construyen las «bandas al 5 %». El veredicto «dentro o fuera» tampoco explica qué hacer cuando hay los dos tipos de salida a la vez. Dos implementaciones distintas cumplirían el RF.

15. **El RESET de Ramsey no dice con cuántas potencias se estima**, y Breusch-Pagan y White no dicen si se calculan incluyendo o excluyendo el modelo. La batería coincide con la skill en los tests, pero no en estos detalles, que cambian el estadístico y el p-valor que RF-9 debe reportar.

16. **RF-5 deja dos columnas sin valor definido.** La tabla exige «signo esperado» y su coincidencia para «constante, ρ, β₁–β₅ y δₖ», pero los signos esperados solo están definidos para los cinco regresores macro y ρ (líneas 63-70). No se dice qué valor («sin contraste», vacío, guion) llevan la constante y las cuatro dummies, aunque el propio RF-5 fija el vocabulario «sí»/«no»/«sin contraste».

17. **RF-13 no describe la tabla de forma que se pueda saber qué se estimó.** Exige coeficiente, error HAC, p-valor, número de observaciones y muestra efectiva, pero no la forma de la dependiente, la ventana HAC ni qué dummies lleva cada variante. Con R2, R3, R5 y R8, cuatro de las ocho variantes no son distinguibles desde esa tabla. El criterio de finalización habla de «las tablas de robustez» en plural sin decir cuántas ni cuáles.

18. **RF-18 dice «con nombres estables» y no enumera las claves** (línea 124). «Estable» no es verificable contra nada: no hay lista previa de nombres, ni contra qué se compara en RNF-4, ni quién decide el nombre en el plan. La skill informe-quarto exige además el shortcode exacto (`{{< var modelo1.beta_unrate >}}`), que en la spec no aparece.

19. **RNF-6 no tiene mecanismo ni alcance.** «Ninguna salida textual usa lenguaje causal» no dice en qué archivos se comprueba, con qué lista de palabras ni qué se hace si aparece. Además las propias salidas de esta spec se llaman «efecto de impacto» y «efecto de largo plazo» (RF-6, RF-7, RF-18), y la Definición habla de «cambio de largo plazo de la morosidad»: un test de lenguaje causal que busque «efecto» reprobaría los nombres que la propia spec exige. La parte de «la endogeneidad de la FFR y la simultaneidad… se declaran como límites» tampoco tiene artefacto ni RF que la haga verificable.

20. **RNF-2 no dice para qué coeficientes ni garantiza lo que exige.** «Con errores autocorrelacionados simulados, el error HAC supera al MCO clásico» no es una propiedad que se pueda imponer por diseño si la autocorrelación simulada resulta negativa o si la realization cae mal; no dice cuál de los coeficientes se compara ni con qué tolerancia. RNF-3 dice «resultado conocido» para la corrección de Diebold-Mariano sin decir cuál es el valor de referencia.

21. **R6 y R7 no tienen muestra efectiva determinable.** Su primer trimestre válido depende de si el sistema puede usar el histórico anterior a 2000T1 o solo el panel recortado (spec 001 RF-10): con el panel tal como existe (`data/processed/panel.csv`, 2000T1 en adelante), CRED(t−8) y CRED(t−12) no existen hasta 2002T1 y 2003T1; con el histórico sin recortar, antes. La spec no dice cuál de las dos fuentes es la válida, así que el número de observaciones de R6 y R7 (y su comparabilidad con la principal) no se puede fijar ni verificar. Lo mismo con la elección entre «conservar el inicio nominal 2000T1 y perder observaciones» o «desplazar el inicio».

22. **«Muestra larga: 1985T1–2026T2 nominal» (línea 29) usa «nominal» con el sentido de «en principio»**, que colisiona con «GDP nominal» de R4 (línea 79). Sin unambigüedad, el término es ambiguo justo donde la spec más necesita precisión.

23. **RF-11 no dice si el ADF/KPSS se reporta también para R8**, cuya muestra (1985 en adelante) no está en la tabla de la spec 001, calculada sobre 2000T1–2026T2. La tabla que RF-11 exige para «el modelo» no cubre la variante más larga.

24. **RNF-4 no fija el criterio de «idénticas».** La spec 001 sí lo hizo («sin diferencias en `git diff`»); aquí «tablas, figuras y variables idénticas» no dice contra qué ni con qué tolerancia (fechas de generación, metadatos de PNG, orden de filas).

25. **La afirmación «DRALACBS empieza en 1985T1» (línea 29) no está verificada en el repositorio.** La descarga congelada empieza en 1998-01-01 (`data/raw/manifest.csv`) y `data/processed/panel.csv` empieza en 2000T1, así que la precondición de R8 y de RF-1 descansa sobre un dato que nadie ha comprobado en este proyecto.

---

## 2. Contradicciones entre requisitos

1. **RF-1 es más restrictiva de lo que la propia spec justifica y bloquea variantes que no la necesitan.** RF-1 (línea 97) dice que no se estimarán R6, R7 ni R8 «mientras el panel no tenga historia desde 1983-01-01». Pero R6 (crédito rezagado 8) y R7 (rezagado 12) son variantes de la muestra principal 2000T1–2026T2: el rezago más largo que necesitan (12 + 4 para la variación interanual) cae dentro del histórico ya descargado desde 1998. La condición de RF-1 solo es necesaria para R8, y la razón que la spec da («crédito rezagado 8 y 12», línea 97) no aplica a la muestra principal.

2. **RF-1 no dice qué artefacto contiene los datos de 1985–1999, y hoy no existe ninguno.** La spec 001 recorta el panel a 2000T1 (RF-10) y declara fuera de alcance «extender la muestra a 1985 como robustez» (línea 101). RF-1 menciona «nueva descarga con fecha, sin tocar la de 1998», pero no nombra un panel largo, una columna adicional ni una etapa que produzca las filas 1983–1999. R8 no tiene, tal como está escrita la spec, de dónde leer sus 160 observaciones. Y el criterio de finalización (línea 157) exige R6, R7 y R8 «tras cerrar el /sdd-change», sin alternativa prevista si ese cambio se rechaza o se aplaza.

3. **RF-9 y RF-12: las dos pruebas de Chow no están bien planteadas con las dummies de COVID pre-registradas.** Las dummies D(k) son idénticamente cero en toda la sub-muestra anterior a 2020T2 y valen 1 solo dentro de la posterior, es decir, la dummy de 2020T2 es colineal con el indicador del quiebre. Un Chow de 2020T2 sobre la especificación con esas dummies no tiene un estadístico F interpretable, y un Chow de 2008T3 incluye en la sub-muestra previa columnas sin variación. El veredicto «pasa»/«falla» que RF-9 exige para esas dos pruebas no tiene contenido verificable. Además, la explicación de RF-12 (línea 112: «las dummies absorben 2020T2–2021T1, así que la prueba compara de hecho el tramo anterior con el de 2021T2 en adelante») no describe lo que hace un Chow de 2020T2 con esas dummies: contrasta los coeficientes de las pendientes entre las dos sub-muestras, con la constante y las dummies absorbiendo el nivel. La nota describe otra prueba.

4. **El umbral del largo plazo está fijado dos veces y de dos maneras** (línea 34, RF-6 línea 104, caso límite línea 137). Definiciones y RF-6 dicen ρ̂ < 1 / ρ̂ ≥ 1; el caso límite añade que si ρ̂ es «muy cercano a 1» el largo plazo se reporta «no definido» **o** con «un IC muy ancho», sin definir «muy cercano» ni qué es un IC «muy ancho». El resultado de la salida depende de un juicio no escrito, y el RF y el caso límite pueden dar respuestas distintas al mismo dato.

5. **RF-3 obliga a una forma en R5 que R5 y RF-15 no esperan.** Con la decisión «primera diferencia» del logit (`outputs/tables/stationarity.md`), R5 no puede ser «el logit como dependiente» tal como está redactada; y el orden «posible I(2)» de ese logit no aparece como limitación en ninguna parte de la spec, pese a que la línea 51 obliga a declarar como limitación todo lo que no sea I(0).

6. **La redacción de la sección «Variables y transformaciones» (línea 51) ya no es hipotética y está desalineada con el resultado de la spec 001.** «Si alguno no resulta I(0), se declara como limitación» ya tiene respuesta: en `outputs/tables/stationarity.md`, `cpiaucsl_yoy` y `loans_yoy` salen «ambigua (primera diferencia)», I(1). La spec no enumera los casos, con lo que la redacción sugiere una incertidumbre que ya se resolvió en la spec 001. Además, para `unrate` y `fedfunds` la regla de la 001 dice «niveles», y la spec los mete en diferencia trimestral; el ejemplo que la línea 51 usa para justificar la departure («evitar el cambio de la inflación interanual») no cubre ese otro caso.

7. **El caso límite «El último trimestre común cambia por una nueva descarga: todas las muestras terminan en el nuevo último trimestre común, sin otro cambio» (línea 144) contradice RNF-1 y el principio 2 de la constitución.** Cambia la muestra de un pre-registro ya aprobado sin pasar por `/sdd-change` y sin que quede registrado en «Desviaciones del pre-registro» ni se reporte en el informe; y contradice la regla de datos congelados (`datos-fred`: `data/raw/` con fecha, nunca editar ni volver a bajar) y lo aprendido en `MEMORY.md` («FRED revisa el PIB: volver a descargar puede cambiar resultados. Congelar `data/raw/`»).

8. **«Dudas abiertas (ninguna)» (línea 165) contradice el estado real del proyecto.** `MEMORY.md` (líneas 30-32) deja en «Decisiones pendientes» confirmar con el profesor la muestra larga desde 1985 y el formato del informe. La spec declara cerrado un punto que depende de una aprobación externa, y ese punto además es la precondición de RF-1 y del criterio de finalización (línea 157).

9. **La sección «Pregunta que responde» se contradice a sí misma sobre el alcance de la sección 4.** Declara cubrir «la sección 4 (… diagnosticar e interpretar)» y, en la misma línea, delega la interpretación a la spec 006. Quedan dos dueñas posibles de la interpretación de la sección 4.

10. **RF-2 y la validación fuera de muestra se contradicen en el tratamiento del hueco 2020T1–2021T4.** La estimación va a 2019T4 y la evaluación empieza en 2022T1 (línea 86), dejando 8 trimestres fuera de ambos tramos sin que ninguna RF ni caso límite lo declare, lo excluya explícitamente de la evaluación o permita el reentrenamiento con esos datos.

11. **R3 y R5 chocan con la regla de RF-15.** RF-15 dice que en R5 no se expresan los coeficientes en pp, pero las sub-carteras de R3 sí están forzadas a primera diferencia (decisiones I(1) en `outputs/tables/stationarity.md`) y sus coeficientes sí se expresan en la tabla de RF-13 sin ninguna nota que diga que son cambios y no niveles. La asimetría de tratamiento entre R3 y R5 no está justificada en ninguna parte.

---

## 3. Casos límite no cubiertos

1. **Una sub-cartera que empiece después de 2000T1.** El caso límite de la línea 141 cubre solo el final anticipado («faltante terminal»). Con la descarga actual las tres sub-carteras cubren 1998 en adelante, pero al re-descargar desde 1983 que exige RF-1 puede aparecer un inicio tardío, y no hay regla. Tampoco la hay para un faltante interno en una sub-cartera: RF-2 detendría el proceso completo por una serie que solo se usa en una variante.

2. **Muestra insuficiente en una variante.** No hay número mínimo de observaciones, ni regla para el caso en que N sea menor o igual al número de parámetros (11: constante, ρ, β₁–β₅ y cuatro dummies), ni para una matriz de rango deficiente, ni para una estimación que no converge. RF-2 solo cubre el faltante.

3. **Covarianza HAC no definida positiva.** Si la matriz no es positiva semidefinida, el método delta de RF-6 y la simulación de coeficientes de la spec 005 no tienen salida. No está previsto.

4. **Regresor con desviación estándar nula o casi nula en alguna variante.** El efecto «por 1 DE» de RF-6 y el gráfico de RF-7 no dicen qué se hace si la DE es 0 o si el efecto por 1 DE es indistinguible de cero.

5. **Coeficiente de un regresor prácticamente nulo.** El criterio de robustez compara el signo estimado con el de la principal; con un coeficiente cercano a cero el signo es arbitrario y la robustez se decide por el ruido. No hay umbral mínimo ni regla.

6. **Y en primera diferencia con dummies de COVID.** Los δₖ capturan el cambio en la variación de la morosidad, no un nivel; la spec 003 no advierte esta diferencia de interpretación ni dice cómo la spec 005 debe usarlos al proyectar el nivel. Con la decisión real de la spec 001 («ambigua (primera diferencia)»), este es el caso que se va a dar, no el excepcional.

7. **Regresión sin dummies COVID dentro de la muestra principal.** Solo R1 quita las dummies, pero si el horizonte de cualquier uso futuro (estrés) cubre 2020T2–2021T1, no hay regla para proyectar ese tramo. Fuera del dato congelado de hoy, es un hueco de la especificación.

8. **Una nueva descarga que cambie valores históricos sin cambiar el último trimestre común.** El caso límite de la línea 144 solo contempla que cambie el final de la muestra. `MEMORY.md` ya documenta que FRED revisa el PIB y que volver a descargar puede cambiar resultados; ese caso (mismo final, valores distintos) no está cubierto y alteraría un pre-registro firmado.

9. **Insuficiencia de grados de libertad para el tramo fuera de muestra.** RF-16 exige Diebold-Mariano con corrección para muestras pequeñas sobre «unos 18 trimestres»; no hay regla para el caso en que la estimación de 2000T1–2019T4 no sea posible por falta de datos en ese tramo, ni para el caso en que el número efectivo de observaciones de pérdida sea menor que el número de parámetros estimados en la regresión de pérdida.

10. **Una sub-cartera o DRALACBN con 2025T4 afectado por el promedio de dos meses.** El caso límite de la línea 142 cubre la dependiente principal; no dice si la misma salvedad aplica a las dependientes de R2 y R3, que usan la misma fuente y el mismo tratamiento.

11. **El caso límite de VIF (línea 140) está escrito como si el resultado ya estuviera observado.** «VIF > 10 (por ejemplo, PIB y desempleo)» nombra dos series concretas antes de estimar, cuando el principio 2 exige fijar la especificación antes de ver resultados. Además nombra series, no términos del modelo: el término es ΔU, no «desempleo». Un caso límite debe ser condicional y referirse a los términos.

12. **La precondición de R8 no está verificada ni es verificable con los datos congelados** (ver 1.25). Si al abrir el `/sdd-change` resulta que DRALACBS empieza en 1984T3, en 1985T2 o que otra serie principal no llega a 1983, la «muestra larga» de la Definición (línea 29) y el «inicio efectivo» que la propia línea promete quedan sin base.

13. **Un `/sdd-change` aprobado que cambie la decisión de estacionariedad.** La spec 003 lee la decisión de la tabla de la spec 001 (RF-3). Si el cambio de la 001 vuelve a calcular esa tabla sobre otra historia, las formas de Y, de R2, R3 y R5 pueden cambiar después de que esta spec esté aprobada y commiteada, sin que ninguna RF detecte la desincronización.

14. **Ventana HAC igual a cero.** Con T muy pequeño (una variante con muy pocas observaciones), floor(4·(T/100)^(2/9)) puede dar 0 rezagos y la especificaciónNewey-West se reduce a MCO clásico sin que nada lo advierta ni lo prohíba.

---

## 4. Conflictos con docs/constitution.md

1. **Principio 2 (la spec manda y se pre-registra; todo cambio pasa por `/sdd-change` y se reporta en el informe)** — el caso límite de la línea 144 permite cambiar el final de todas las muestras «sin otro cambio», es decir, sin `/sdd-change` y sin reportarlo. La línea 6 de la constitución exige las dos cosas.

2. **Principio 5 (cero cifras inventadas; todo número del informe viene de `outputs/` por código)** — RF-11 obliga a marcar en una tabla qué regresores no son I(0), pero RF-18 no exporta esa lista a las variables del informe. Quien redacte la sección 3.5 tiene que escribirla a mano o dejar fuera una limitación que la propia spec declara obligatoria. Lo mismo ocurre con las desviaciones frente a la guía (punto 3 de la sección 5), que ningún RF produce.

3. **Principio 1 (reproducible de punta a punta con `uv run python -m src.pipeline all`)** — ninguna RF indica en qué etapa del pipeline se calcula nada, y los criterios de finalización solo exigen `uv run pytest -q`. RF-8 dice que los coeficientes y la covarianza HAC se guardan «para que la spec 005 los use sin reestimar», pero no fija formato, ni ruta, ni versión, de modo que la dependencia entre specs no es reproducible ni auditable desde un clon limpio.

4. **Principio 4 (tests como puerta; los estimadores se prueban con datos simulados de parámetros conocidos)** — RNF-2 y RNF-3 cubren estimador, efectos y validación, pero no hay ningún test que cubra la batería de diagnósticos, que sí admite un dato conocido: una DGP con autocorrelación conocida debe hacer que Breusch-Godfrey rechace. El principio 4 queda sin cubrir para la parte de diagnósticos, que es la que puede fallar en silencio.

5. **Principio 2 vs el estado del repositorio** — RNF-1 demuestra el pre-registro con el commit, pero la spec 003 se redactó con `outputs/tables/stationarity.md` ya generado y con la aritmética de rezagos ya conocida; además, en este momento `specs/003-modelo-i/` está sin versionar y `MEMORY.md` tiene cambios sin commitear. La prueba del pre-registro (commit) puede quedar contaminada por material de otra fase si no se aísla.

6. **Principio 6 (idioma)** — sin conflicto: RNF-7 cubre código en inglés y salidas en español. Se deja constancia de que es el único principio sin observación.

### 4.b Conflictos con las reglas de dominio del proyecto (skills, no constitución)

7. **Skill `datos-fred`** — «Descarga desde 1998-01-01 para calcular variaciones interanuales en 2000T1». RF-1 exige 1983-01-01. La skill es parte de las reglas del proyecto y su cambio no está contemplado en RF-1, que solo menciona el `/sdd-change` de la spec 001.

8. **Skill `econometria-series-tiempo`, regla «Efecto acumulado»** — «suma de los coeficientes de la tasa con prueba de Wald (H0: suma = 0) usando la matriz HAC». La spec 003 no menciona ni esta regla ni por qué no aplica a su FFR contemporánea. Sin esa frase, un auditor no puede distinguir que fue una omisión consciente de un olvido.

9. **Skill `econometria-series-tiempo`, regla «Estacionariedad antes de estimar»** — la línea 51 se aparta de ella de forma explícita y justificada, pero la partida no queda registrada en «Desviaciones del pre-registro» (vacío) ni en las variables del informe (RF-18), de modo que el informe no tiene forma de declarar la departure que la propia spec reconoce.

10. **Skill `informe-quarto`** — «Si hubo desviaciones del pre-registro, se reportan en la sección 3.5». Ningún RF de la spec 003 produce la lista de desviaciones (ni frente a la guía, ni frente a la skill de estacionariedad), y RF-18 no incluye ningún campo para ella.

11. **Skill `informe-quarto`** — el contrato de presentación exige tablas en `outputs/tables/*.md` incluidas con `{{< include >}}`, figuras en `outputs/figures/*.png` con pie y fuente («Fuente: FRED; elaboración propia») y números por shortcode. Ninguna RF fija formato de tabla, pie de figura con fuente ni claves de variable, y RNF-7 solo exige español.

---

## 5. Requisitos de docs/guia-profesor.md que esta spec debería cubrir y no cubre

1. **Sección 3.5 — «explicar los dos modelos que serán estimados»**. RF-18 exporta forma de Y, muestra, ρ, efectos, robustez y métricas, pero no el inventario de la especificación: número de parámetros, las cuatro dummies de COVID, el nombre del estimador, la lista y el nombre de las ocho variantes, ni la decisión de la 001 que fija cada forma. Con lo exportado, la sección 3.5 no puede enumerar la especificación sin texto tecleado.

2. **El reparto entre Modelo I y Modelo II no está establecido.** La guía separa el Modelo I (determinantes macro) del Modelo II (política monetaria y rezagos, sección 5), pero esta spec ya mete la FFR (contemporánea) y los rezagos de crédito en el Modelo I. Los «Usuarios» dicen que la spec 004 «compara sus resultados con los de este modelo en 6.3», sin decir qué hará la 004 de distinto. La guía pide dos modelos con preguntas distintas; esta spec no deja constancia de su frontera, y la sección 6.3 necesitará una comparación que aún no está definida.

3. **Desviaciones frente a la guía que esta spec debería declarar y no declara.** (a) El PIB principal es GDPC1 (real) y la guía lista GDP (nominal) — la decisión está tomada (`MEMORY.md`), R4 trae el nominal como robustez, pero ninguna RF obliga a declarar la desviación. (b) La muestra termina en 2026T2 mientras el ejemplo de la sección 11 de la guía corta en 2026-01-01. (c) La muestra larga desde 1985 sale del período «2000–2026» que fija la guía. `MEMORY.md` las tenía ya anotadas como «declarar en el informe»; la spec no produce nada para declararlas.

4. **Sección 4 — «interpretar los resultados desde la perspectiva de gestión de riesgo»**. La línea 10 declara cubrir la sección 4 «e interpretar» y delega la interpretación a la spec 006. Quedan dos dueñas y ninguna RF indica qué salida mínima necesita esa interpretación. Lo que sí está resuelto: los efectos por 1 DE (RF-6) son exactamente el insumo que la guía pide, así que el hueco es de reparto, no de datos.

5. **Sección 4 — «realizar pruebas de diagnóstico» y sección 6.1**. RF-9 entrega veredicto, pero RF-18 solo exporta el veredicto de cada diagnóstico, no el estadístico ni el p-valor. El informe puede decir «el diagnóstico falla» sin poder mostrar la evidencia, ni el p-valor de los coeficientes de la tabla principal (incluida la constante, ρ y las dummies), ni el R², ni el número de observaciones de las variantes. Para una sección que pide evaluar la significancia y diagnosticar, el conjunto exportado es más pobre que el producido.

6. **Sección 3.3 «tasa de interés» y sección 3.4 «cambio en la Federal Funds Rate»**. La guía enumera la tasa de interés entre las variables macroeconómicas (3.3) y, aparte, el cambio en la FFR como variable de política monetaria (3.4). Esta spec tiene una sola variable de tasas, ΔFFR. No declara si las dos secciones de la guía quedan cubiertas por la misma variable ni qué se hace con «tasa de interés» en 3.3.

7. **Sección 2.5 y sección 6.3 — trazabilidad con la literatura**. La spec 002 declara que sus estudios «justifican variables, rezagos y signos» y la guía pide comparar con «estudios que hayan estimado relaciones similares y explicar qué variables y metodologías utilizaron». Ningún RF exige que la tabla de coeficientes (RF-5) indique con qué estudio de `research/matriz-literatura.md` se compara cada signo esperado. Los signos esperados de la línea 63-70 son la pieza que más se BENEFicia de esa trazabilidad y es la única que no la tiene.

8. **Sección 7 — insumo del estrés**. RF-8 entrega lo que la guía pide para el escenario adverso, pero no exige que las variables del informe incluyan los tres efectos que el escenario de la guía necesita de forma aislada (desempleo ↑, PIB ↓, FFR ↑). Cada uno está en RF-18 «por 1 pp», así que el contenido está; lo que falta es que la spec no registre esa dependencia, y RNF-4 no cubre el hecho de que la spec 005 consumirá estos artefactos.

---

## Resumen

| Categoría | Cantidad |
|---|---|
| Ambigüedades | 25 |
| Contradicciones | 11 |
| Casos límite no cubiertos | 14 |
| Conflictos con la constitución | 6 (+5 con reglas de dominio, en 4.b) |
| Requisitos de la guía no cubiertos | 8 |
| **Total** | **69** |

**Puntos que más bloquean la verificación, por orden:** 1.5 y 2.5 (forma del logit en R5 frente a la decisión «primera diferencia» / posible I(2) de la spec 001), 2.3 (Chow con dummies pre-registradas y la nota de RF-12), 2.1–2.2 (R6–R8 y el panel que no existe para 1985–1999), 1.11 (dos lecturas de la reconstrucción del nivel), 1.8 (p-valor del largo plazo sin definición) y 4.2 (la lista de regresores no I(0) no llega al informe).

---

**Nota**: este informe solo detecta; no propone soluciones, no modifica la spec y no ejecuta la implementación. Las referencias `outputs/tables/stationarity.md`, `data/raw/manifest.csv` y `data/processed/panel.csv` se citan como evidencia del estado actual del proyecto, no como requisitos.
