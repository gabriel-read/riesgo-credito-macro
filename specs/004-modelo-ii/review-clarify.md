VEREDICTO: CAMBIOS NECESARIOS

Este es un informe de clarificación de la spec C:\Users\gabri\orca\riesgo-credito-macro\specs\004-modelo-ii\spec.md. Solo recoge hallazgos: no propone soluciones y no he editado nada. Las referencias van como spec.md:línea.

**Datos que cita la spec, comprobados con los archivos congelados:**
- **Muestra M = 2000T2–2026T2, 105 trimestres: correcta.** FEDFUNDS empieza en 1998-01 (manifest.csv), así que ΔFFR(t−8) existe desde 2000T2. CRED(t−4) existe desde 2000T1.
- **Tramo de tasa cero = 36 trimestres: correcto.** Valores de panel.csv:
  - 2008T4 = 0,51 y 2009T1 = 0,18;
  - 2009–2015, siempre entre 0,07 y 0,19;
  - 2015T4 = 0,16 y 2016T1 = 0,36;
  - 2020T1 = 1,26 y 2020T2 = 0,06;
  - 2022T1 = 0,12 y 2022T2 = 0,77.
- **Octubre 2025 vacío en UNRATE y CPIAUCSL: correcto.**
- **DRALACBS «ambigua (primera diferencia)», I(1): correcto** (stationarity.md:3).
- **La spec 005 todavía no existe** (specs/ solo tiene de 001 a 004).

---

## 1. Ambigüedades restantes (requisitos que no se pueden verificar)

1.1 **No hay regla para pasar de las salidas a la respuesta (spec.md:10, 84-87, 116-123).** La spec no fija cómo se responde a la pregunta de la guía («¿existen efectos rezagados?», «deterioro posterior»). Produce cuatro piezas que pueden discrepar:
- el Wald de S (RF-10);
- H2 sobre un h* puntual (RF-11);
- Granger (RF-12);
- las bandas de la proyección local (RF-13 y RF-15).

No está escrito qué combinación cuenta como evidencia. Por ejemplo, Granger no rechaza y H2 sale «sí». La conclusión quedaría a elección después de ver los datos.

1.2 **Falta el criterio de «sí/no» de H1 y H2 (spec.md:87; RF-10 :116; RF-11 :117; RF-20 :132).** No se dice si basta el signo puntual o si hace falta significancia. Además, H2 se juzga sobre una R(h) sin bandas (:72). Así, H2 puede salir «sí» con S indistinguible de cero.

1.3 **El h* de la proyección local no está definido (RF-15, :123).** RF-15 pide «el h* de cada método», pero la definición (:41) solo existe para R(h). No dice qué hacer con los horizontes «no estimada» ni con los empates de |β_h|.

1.4 **HU-4 no tiene criterio (:26).** «Ver si la respuesta es la misma» no es verificable: RF-15 da un recuento «k de n», pero ningún umbral de coincidencia.

1.5 **«K elegido igual a 8» es ambiguo (RF-7 :111; RF-23 :137).** No dice si es K_BIC, K_AIC o cualquiera de los dos.

1.6 **RF-19 (:129) no dice de dónde salen la decisión y el orden de integración de ΔFFR, ΔU y ΔDR.**
- La tabla de la 001 deja en blanco la decisión y el orden en las filas «primera diferencia» (stationarity.md:4, 32, 34).
- La 003 lo resolvía con su definición de «Tabla de estacionariedad» (003 spec.md:34). La 004 no la importa (lista de :31-32).
- Para ΔDR no se sabe si manda la fila «tal cual» (I(1), y por tanto «no I(0)») o la de primera diferencia.

1.7 **La regla de veredicto no vale para CUSUM ni VIF (:98; RF-17 :127).** La regla es «pasa si p ≥ 0,05» y RF-17 pide estadístico, p y veredicto de cada prueba, pero esas dos pruebas no tienen p. La regla de cruce de bandas del CUSUM (003 RF-14) no se importa.

1.8 **RF-26 (:148) no dice qué covarianza HAC se exporta.** La matriz completa tiene rango reducido por las 4 dummies de impulso. Queda abierto si se exporta la completa, el sub-bloque o la versión truncada. Tampoco dice si se exportan la ventana HAC y la marca de truncamiento.

1.9 **Los tests de simulación no son medibles (RNF-2 :153; RNF-4 :155).**
- «Muestra grande» no es medible.
- «HAC mayor que el clásico con errores AR(1)» no fija un regresor persistente; con un regresor iid no está garantizado (la 003 fijaba 0,7 y 0,8).
- RNF-4 no fija el proceso simulado. Si ΔFFR simulado tiene autocorrelación, β_h no converge a R(h) (ver 2.4), así que el test depende de una elección no escrita.

1.10 **RF-25 (:147) menciona efectos que no existen aquí.** Habla de efectos «no reportado» o «no definido», pero la 004 no define ninguna cantidad que pueda quedar así (no hay largo plazo con umbral ni efectos por DE). Es un resto de la 003.

1.11 **Error de notación (:37).** Escribe «ΔY(t−1)»; como Y = ΔDR (:33), eso sería Δ²DR. El término del modelo es ΔDR(t−1).

1.12 **Criterio de robustez con S principal no significativo (:95).** Si S principal tiene p ≥ 0,05 y una variante tiene p < 0,10 con el mismo signo, cuenta como «sí». No está fijado cómo se lee ese caso.

## 2. Contradicciones entre requisitos

2.1 **[conceptual] θ₀ se trata como simultáneo en un sitio y no en otros.**
- Se excluye de Granger por simultáneo (:73).
- Pero entra en S (:40), en R(0), en h* (que admite h* = 0, :41) y en H1 (:84).

Si el argumento de simultaneidad vale para Granger, también contamina H1. Además, en el Modelo I el ΔFFR contemporáneo salió negativo (MEMORY.md:7), y S arrastra ese componente.

2.2 **[conceptual] H1 tiene dos definiciones.** Se define como S > 0 (:84), pero RF-11 (:117) la evalúa con el signo de R(h*). Si los θ_j tienen signos mezclados, las dos pueden dar resultados opuestos. Aun así, RF-25 (:142) exporta «H1» como una sola variable.

2.3 **El estado de R1 no encaja en las tablas.** RF-6 (:110) y los casos límite (:164) dan el estado «no aplica». RF-22 (:134) solo admite «sí/no/no estimada» y RF-20 (:132) solo «no estimada». No se sabe cómo cuenta R1 en la tabla de robustez.

2.4 **[conceptual] RF-15 y RF-16 comparan R(h) con β_h como si fueran la misma respuesta, y no lo son.**
- R(h) fija ΔFFR(j) = 0 para j ≥ 1 (:35) y deja fijos los controles, que no tienen ecuación propia.
- β_h incluye la trayectoria posterior de la tasa (ΔFFR es persistente) y la reacción de PIB, ΔU, π y CRED.

Por eso un desacuerdo en el recuento «k de n» no informa sobre la forma paramétrica (HU-4). Tampoco se pide la respuesta de la propia tasa en la proyección local, que diría a qué trayectoria corresponde β_h.

2.5 **[conceptual] La razón para rezagar los controles choca con su efecto (:59).** Se rezagan «para que no sean simultáneos con ΔFFR(t)». Pero con controles en t−1, ΔFFR(t) conserva la reacción de la Fed a la macro del mismo trimestre. Ese supuesto de temporalidad es el contrario del recursivo estándar, en el que la política reacciona a la macro contemporánea. El resultado es que θ₀, β_0 y S se mueven en la dirección de la endogeneidad que RF-23 declara.

2.6 **Fecha de los efectos base mal copiada para el PIB (RF-23, :137).** Dice «2021T2–2022T1 sin dummy en PIB y crédito», copiado de la 003. Con PIB(t−1), el rebote interanual (11,8 en 2021T2; 5,1; 5,7; 3,9 en panel.csv) entra en 2021T3–2022T2. Para CRED(t−4) la fecha sí coincide.

2.7 **El caso límite de 2025T4 está incompleto (:172).** Dice que solo afecta a 2026T1. Pero ΔU(t−1) en 2026T2 es U(2026T1) − U(2025T4), que también usa el promedio de dos meses. π(t−1) sí afecta solo a 2026T1.

2.8 **El test de lenguaje choca con los textos que la spec pide (RNF-9, :160).** RNF-9 prohíbe la cadena «causal», que también aparece dentro de «causalidad». La propia spec usa o pide textos con esa palabra:
- «no causalidad» (:43);
- «no efectos causales puros» (:7);
- las limitaciones fijas de RF-23 sobre Granger y sobre el shock no identificado.

Un test literal haría fallar salidas que dicen lo correcto.

2.9 **No está claro quién compara los modelos en 6.3.**
- La 003 (:21) dice que la 004 compara.
- La 004 (:19) dice que compara la 006.
- La 004 (:10) dice que aporta «el insumo cuantitativo de la 6.3», pero ningún RF lo produce.

## 3. Casos límite no cubiertos

3.1 **[conceptual] h* = 12 en el borde.** R(h) es un nivel acumulado. Si los θ_j tienen el mismo signo y ρ̂ está en [0, 1), |R(h)| no decrece, así que h* = 12 por construcción y H2 sale «sí» casi mecánicamente. No hay un tratamiento de borde como el de K = 8 (RF-7). H2 casi no se puede refutar, y el «trimestre de efecto máximo» puede ser solo el horizonte de corte.

3.2 **[conceptual] Fugas de la COVID por los rezagos en la principal.** Las dummies solo absorben los t de 2020T2–2021T1. ΔFFR(2020T2) = −1,20 pp entra como ΔFFR(t−j) en 2021T2–2022T2 cuando K ≥ 4, sin dummy. RF-22 solo cuenta estas fugas en R2 y R3.

3.3 **[conceptual] Proyecciones locales cuya ventana cruza la COVID (:78).** Las dummies se fechan en t, así que no absorben los t+h que caen en 2020T2–2021T1. Esto solo figura como limitación (RF-23). No hay variante de la proyección local sin 2020–2021, aunque la skill lo exige. Además, la comparación con R(h), que sí neutraliza esos trimestres, mezcla dos tratamientos distintos.

3.4 **El horizonte h = 0 coincide por construcción.** La regresión de la proyección local en h = 0 es la misma que la principal: misma dependiente ΔDR(t), mismos regresores y misma muestra M. Por tanto β_0 = θ₀ = R(0) exactamente, y ese horizonte suma una coincidencia segura al «k de n» de RF-15.

3.5 **[conceptual] Breusch-Godfrey rechaza con ΔDR(t−1) en la ecuación.** En ese caso MCO es inconsistente para ρ y θ, y con ellos para S, R(h) y Granger. La 003 lo cubría (003 spec.md:85, 250); la 004 no.

3.6 **Sin regla para rango incompleto o pocos grados de libertad en la principal.** Si la principal o alguno de los 8 modelos de selección tiene rango incompleto o menos de 30 grados de libertad, no hay regla (la 003 se detenía, RF-6). RF-14 y RF-21 solo cubren las proyecciones locales y las variantes. Si un K falla, la selección queda indefinida.

3.7 **Chow en 2020T2 y en 2008T3.**
- En 2020T2, con K = 8 hay 15 interacciones frente a 21 trimestres posteriores útiles (25 menos 4). Además, ΔFFR está casi en cero en 2020T3–2022T1 (|ΔFFR| ≤ 0,04). El bloque de interacciones puede tener rango incompleto, y RF-18 solo añade una nota sobre el tamaño del contraste.
- En 2008T3 no se cuenta el tramo previo: 2000T2–2008T2 son 33 trimestres para 15 coeficientes.

3.8 **ρ̂ cercano a 1 pero menor que 1.** R(h) se reporta sin aviso; solo |ρ̂| ≥ 1 está cubierto (:169).

3.9 **La inferencia ignora la selección de K.** S y Granger se calculan condicionados a un K elegido con los mismos datos, y no se declara como limitación.

3.10 **Muestras distintas en la comparación.** La proyección local se estima en muestras que cambian con h (93 observaciones en h = 12), mientras R(h) sale de M. La comparación de RF-15 no se hace sobre la misma muestra.

## 4. Conflictos con docs/constitution.md

4.1 **[conceptual] Principio 2: el tratamiento del signo de la tasa se decidiría después de ver S.** Las líneas :14 y :182 dejan a la 005 cómo usar el efecto de la tasa y qué hacer si el signo no es el esperado. La 005 no existe, y según el calendario (MEMORY.md:13) se redacta después de estimar la 004. MEMORY.md:47 ya registra que hace falta decidirlo antes.

4.2 **[conceptual] Principio 2: la spec no declara lo que ya se sabía del Modelo I.** La 004 se redacta conociendo los resultados del Modelo I sobre casi la misma muestra (MEMORY.md:7):
- ΔFFR contemporáneo negativo;
- π y CRED significativos;
- los dos Chow fallan.

Las decisiones que más dependen de eso son justo las que toma: θ₀ fuera de Granger, controles rezagados, R3 y H2. La 003 declaró qué conocía al redactar (003 spec.md:5); la 004 no declara nada, así que no se puede verificar que esas decisiones no estén condicionadas.

4.3 **Principio 5 (lenguaje).** La spec usa «shock», «respuesta», «efecto acumulado», «efecto máximo» y «¿Cómo afectan…?» (:10). La 003 declaraba sus términos técnicos como asociaciones (003 spec.md:49, RNF-7). La 004 no lo hace, y RNF-9 no los cubre.

4.4 **Principio 4 (tests).** No hay requisito de tests para los diagnósticos que cambian respecto de la 003: Chow con K+7 interacciones, CUSUM sin los trimestres de las dummies y White con eliminación por rango. La 003 sí los tenía (RNF-4). A esto se suma que los procesos simulados no están fijados (1.9).

## 5. Requisitos de la guía que esta spec debería cubrir y no cubre

5.1 **Sección 6.3: ningún RF produce la comparación con el Modelo I.** Tampoco se define qué se compara: θ₀ frente al β₄ del Modelo I, muestras 2000T1 frente a 2000T2, controles contemporáneos frente a rezagados. Además, los controles no tienen signo esperado (:86), mientras que en el Modelo I sí (003 spec.md:88-96), así que la comparación de controles no tiene referencia.

5.2 **Sección 5 («si un shock de política monetaria tiene relación con el deterioro posterior»).** No hay regla de respuesta (1.1). La redefinición de «shock» como variación observada (:35) está declarada, pero responder a la pregunta literal depende de 1.1.

5.3 **Secciones 3.3 y 11 (GDP nominal es la serie de la guía).** La 004 usa GDPC1 sin robustez con GDP y sin entrada en RF-24 (:138), aunque MEMORY.md:19 dice que GDP va como robustez. Lo mismo pasa con la muestra larga: MEMORY.md:18 la da por pre-registrada en las specs 003–005, y la 004 ni la incluye ni la excluye explícitamente.

5.4 **Período 2000–2026 y corte en 2026-01-01.** RF-24 solo recoge que M empieza un trimestre después. No recoge:
- el fin en 2026T2;
- el apartamiento de la regla de estacionariedad: ΔFFR y ΔU entran diferenciadas aunque son I(0) en niveles, y π y CRED entran sin diferenciar.

La 003 sí recogía ambas cosas (RF-21).

5.5 **Secciones 6.4, 8 y 9 (alerta temprana).** Ninguna salida mide la anticipación, es decir, el horizonte desde el que la asociación se distingue de cero. Solo hay «pp por 1 pp de variación trimestral del promedio de la FFR», y la traducción a gestión de riesgos queda entera para la 006 sin ese dato.

---

## Puntos que más bloquean la verificación (en orden)

| # | Punto | Tipo |
|---|---|---|
| 1 | 1.1: no hay regla que convierta S, H2, Granger y la proyección local en la respuesta sobre efectos rezagados | Conceptual |
| 2 | 4.1: el signo y el uso de la tasa en el estrés se deciden después de ver S | Conceptual |
| 3 | 2.1: θ₀ simultáneo en Granger pero dentro de S, H1 y h* | Conceptual |
| 4 | 2.2 + 1.2: H1 con dos definiciones y sin criterio de «sí/no» | Conceptual |
| 5 | 2.4 (+3.4, 3.10): R(h) y β_h miden objetos distintos y se comparan como si fueran el mismo | Conceptual |
| 6 | 3.1: H2 casi mecánica (h* = 12 en el borde) | Conceptual |
| 7 | 4.2: no declara lo conocido del Modelo I | Conceptual (transparencia del pre-registro) |
| 8 | 2.5: la razón para rezagar los controles choca con su efecto | Conceptual |
| 9 | 3.5: Breusch-Godfrey falla con ΔDR(t−1) | Conceptual |
| 10 | 3.2 / 3.3: fugas de la COVID por los rezagos y en la proyección local | Conceptual |
| 11 | 5.1 / 2.9: la comparación de 6.3 sin salida ni responsable | Conceptual y de redacción |
| 12 | 2.8: el test de lenguaje choca con los textos pedidos | Redacción |
| 13 | 2.3: estado de R1 | Redacción |
| 14 | 1.6: origen de la decisión de estacionariedad | Precisión |
| 15 | 1.7: veredicto del CUSUM y del VIF | Precisión |
| 16 | 2.6 / 2.7: fechas de los efectos base y de 2025T4 | Precisión |
| 17 | 3.6 / 3.7: rango incompleto en la principal y en Chow 2020T2 | Precisión |
| 18 | 1.9 / 4.4: procesos simulados de los tests | Precisión |
| 19 | 5.3 / 5.4: entradas que faltan en RF-24 | Redacción |
| 20 | 1.3, 1.5, 1.8, 1.10, 1.11, 1.12, 3.8, 3.9 | Precisión |

## Lo que defendería ante el profesor
- K se elige por BIC sobre una misma muestra (2000T2–2026T2, 105 trimestres, comprobada con los datos) y AIC va como robustez, como pide la skill.
- La endogeneidad y el hecho de que la tasa observada no es un shock identificado están declarados como límites. Todo se describe como asociación y precedencia.
- Las robusteces R2 (sin COVID) y R3 (sin tasa cero, con regla verificada: 36 trimestres) están pre-registradas con criterio medible.

## Lo que me preguntaría el profesor
1. Si θ₀ es simultáneo y por eso lo saca de Granger, ¿por qué entra en el efecto acumulado con el que contrasta H1?
2. Su trayectoria R(h) mantiene la tasa y la macro fijas y la proyección local no: ¿qué conclusión saca si no coinciden?
3. Ya sabía que ΔFFR salió negativo en el Modelo I: ¿cómo demuestra que el diseño del Modelo II y el tratamiento del signo en el estrés no dependen de ese resultado?

**Archivos revisados:**
- C:\Users\gabri\orca\riesgo-credito-macro\specs\004-modelo-ii\spec.md
- C:\Users\gabri\orca\riesgo-credito-macro\specs\003-modelo-i\spec.md
- C:\Users\gabri\orca\riesgo-credito-macro\specs\001-datos\spec.md
- C:\Users\gabri\orca\riesgo-credito-macro\docs\constitution.md
- C:\Users\gabri\orca\riesgo-credito-macro\docs\guia-profesor.md
- C:\Users\gabri\orca\riesgo-credito-macro\outputs\tables\stationarity.md
- C:\Users\gabri\orca\riesgo-credito-macro\data\processed\panel.csv
- C:\Users\gabri\orca\riesgo-credito-macro\data\raw\manifest.csv
- C:\Users\gabri\orca\riesgo-credito-macro\MEMORY.md
