VEREDICTO: CAMBIOS NECESARIOS

Revisión independiente del **borrador** de spec y plan de la 005 (Estrés), 11-oct-2026. Autor: subagente `revisor-econometrico` de Claude Code, lanzado con solo rutas y los cinco temas que priorizó el usuario (sin conclusión previa de quien redactó los borradores). Revisión de plan/pre-registro: no se estimó ni proyectó nada. Los borradores no están aprobados y esta revisión no los aprueba. Informe copiado tal cual lo entregó el subagente; la numeración de «cambios necesarios» es la suya.

**En corto.** El borrador está bien encaminado: sigue la regla heredada de la 004, separa la incertidumbre de parámetros de la de predicción, calcula Δ réplica a réplica y no descarta réplicas. Aun así no se puede aprobar tal como está, por dos fallos de diseño:
- **Recorte del escenario.** Usar solo 2026T3–2029T1 de los escenarios de la Fed deja fuera la mitad del shock severamente adverso.
- **Opción condicionada.** Simular el resto de coeficientes condicionado a θ = 0 equivale a reestimar el modelo. Cambia de forma importante los coeficientes de actividad e inflación.

Hay además fallos en las identidades, en la definición de S3 y en la verificabilidad de algunos RF.

## Qué comprobó y cómo
- **Documentos leídos:** spec y plan 005; constitución; guía (§7–8); specs 003 y 004 con sus planes; review-audit de la 004; insumos y nota de compatibilidad de Codex; skill y plantilla SDD.
- **JSON (recalculado con numpy, sin proyectar):**
  - Rango de la covarianza completa: 7/11 en el Modelo I y 8/12 en el II.
  - El bloque sin dummies es definido positivo en los dos: autovalor mínimo 7,00e-7 (I) y 7,08e-7 (II), simetría exacta, Cholesky sin error.
  - Medias y varianzas condicionadas a θ = 0.
  - P(ρ ≥ 1): 3,0e-5 en el Modelo I y 1,8e-4 en el II.
  - Correlación entre θ0 y θ1: −0,845.
- **Panel y datos:**
  - `panel.csv` termina en 2026Q2.
  - No trae los niveles de GDPC1 ni del CPI.
  - La variación interanual es `100·(ln X_t − ln X_{t−4})` (`src/panel.py:292-300`, spec 001:34).
  - En `data/raw/`, UNRATE y FEDFUNDS llegan a 2026-09; CPI y LOANS a 2026-08.
- **Fed:** descargó la página y los CSV *Final Domestic* (base, severamente adverso e histórico) a un directorio temporal, fuera del repo. Las afirmaciones del borrador sobre definiciones, salida desde 2025T4, 28 variables, «no son pronósticos» y tasa a 0,1 % en 2026T2 son correctas.
- **Tests:** `uv run pytest -q` da 774 passed. No modificó nada del repositorio.

## Cambios necesarios

**Críticos**

1. **El recorte por calendario se lleva el núcleo del escenario adverso** (`specs/005-estres/spec.md:28`, también :26, :32 y :101; `plan.md:46` P5). La Fed sale de 2025T4 y su shock se concentra en 2026T1–T2: PIB −5,4 % y −4,9 % anualizados, desempleo de 4,5 a 7,2 y tasa a 3 meses de 3,7 a 0,1. Con el borrador:
   - El alza del desempleo que entra es de 2,8 pp en lugar de 5,5.
   - La caída del PIB hasta el mínimo es −2,1 % en lugar de −4,7 %.
   - Se pierde la brecha entre adverso y base que ya existe en 2026T2 (+2,6 pp de desempleo y −3,6 % de PIB).
   - Las diferencias de ΔTB3 que quedan después de 2026T2 suman +0,4 pp: el «adverso» tendría una tasa *relativamente más alta* que la base. Así las sensibilidades de RF-10 salen casi nulas por construcción.

   Llamar a eso «severamente adverso» y apuntarlo solo como «diferencia de origen» no basta. **Se espera** pre-registrar un **re-fechado**: el trimestre 1 del escenario se coloca en 2026T3, H = 13 (2026T3–2029T3). Los cambios del primer trimestre se miden contra la salida propia de la Fed en 2025T4 (archivo *Historic Domestic*: desempleo 4,5 y tasa a 3 meses 3,7) y se aplican sobre los niveles observados en 2026T2. Si el autor prefiere conservar el calendario, el escenario debe llamarse «tramo posterior a 2026T2» y la tabla debe cuantificar la severidad perdida.

2. **La opción condicionada a θ = 0 es incoherente con «sin reestimar»** (`spec.md:59`, `plan.md:32`, RNF-4 en `spec.md:90`). Condicionar desplaza la media en −V_rθ·V_θθ⁻¹·θ̂, y el desplazamiento es grande:

   | Modelo | Coeficiente | Estimado | Condicionado a θ = 0 |
   |---|---|---|---|
   | I | ΔU | 0,077 | 0,041 |
   | I | ρ | 0,626 | 0,687 |
   | I | π | 0,0198 | 0,0147 |
   | II | π(t−1) | 0,0235 | 0,0123 (desvío de 1,16 EE; su EE se reduce a la mitad) |
   | II | PIB(t−1) | 0,0011 | 0,0062 |

   Los EE condicionados son entre un 1 % y un 49 % menores. Hay dos lecturas posibles y ninguna sirve:
   - Si se centra en β̂, se mezcla la covarianza del modelo restringido con la media del no restringido, y las bandas salen artificialmente estrechas.
   - Si se centra en la media condicionada, es un estimador restringido de mínima distancia: una reestimación hecha después de ver resultados, que además contradice el propio «"Sin evidencia" no equivale a efecto cero» (`spec.md:55`).

   **Se espera:** distribución **marginal**, implementada como extracción conjunta del bloque completo con los θ puestos a 0. Usa las mismas réplicas para la sensibilidad (b) y RNF-4 la comprueba sin ambigüedad. La condicionada puede ir, como mucho, en una fila de sensibilidad rotulada «estimador restringido (θ = 0 impuesto)», fijada ahora.

**Importantes**

3. **Identidades** (`spec.md:30-31`, `plan.md:18`, `plan.md:49`):
   - Falta decir que la variación interanual es la de la spec 001, en logaritmos: ln L_t = ln L_{t−1} + ln(1+g/100)/4 y PIB = 100·(ln L_t − ln L_{t−4}).
   - El caso de test del plan, «g = 4 % → factor 1,01», es falso: el factor es 1,04^(1/4) = 1,009853. Codificaría la aproximación simple.
   - Falta el caso límite de π(2026T4) en adelante, que usa como base el 2025T4 promediado con dos meses (spec 001:95).

4. **Entradas de la etapa `stress`** (`plan.md:10`, §2): `panel.csv` no trae los niveles de GDPC1 ni del CPI. La etapa debe construirlos desde `data/raw/` con las funciones de `src/panel.py`, sin duplicar la lógica. Además, la spec debe declarar que no se usan los datos macro observados de 2026T3 que ya están en `data/raw/`.

5. **S3, opción A: mal definida y condicionada por los resultados** (`spec.md:45-49`):
   - En 2021T4 `fedfunds_d` vale −0,01, así que el alza no es continua desde ese trimestre.
   - En el episodio la inflación interanual *cae* de 6,55 a 3,50 (−3,05 pp): no es estanflacionario.
   - Son 8 trimestres frente a un horizonte de 11 o 13.
   - La Fed usa inflación trimestral anualizada y el panel solo tiene la interanual.
   - Sobre todo, el escenario carga sobre π: el coeficiente que ya se sabe significativo, sin signo pre-registrado («sin contraste», spec 003:94) y no I(0). Diseñar un escenario inflacionario sabiendo eso es buscar el resultado.
   - La severidad de 0,5 es arbitraria.

6. **RF-10(c) está mal definido para el Modelo II y sobra** (`spec.md:78`). Con K = 1 no se dice cómo repartir un S fijado entre θ0 y θ1, que tienen signos opuestos y correlación −0,85; escalarlos proporcionalmente con Ŝ < 0 invierte signos. La banda de (b), que ya simula los θ, recoge el rango compatible con los datos. **Se espera:** quitar (c) y reportar (b) con su banda y la proporción de réplicas con contribución de la tasa > 0. La duda de `spec.md:56` no lo es: la 004 (`spec.md:90`) *obliga* a (b). Se resuelve como «sensibilidad, no efecto estimado».

7. **Sensibilidad D-CRED inútil y recuento erróneo:**
   - RF-12 (`spec.md:80`) la reporta «con el cambio al final», que por RNF-5 es idénticamente cero. Debe ir sobre los niveles (DR final y pico de nivel por escenario).
   - En `spec.md:66`, de 2026T3 a 2027T2 hay 4 trimestres, no 7. Con el re-fechado, el supuesto cubre 9 de 13.

8. **Estimación puntual, pico y comparación** (`spec.md:36-37`, RF-7, RF-11):
   - Falta fijar que la cifra principal es la proyección con β̂ (θ = 0) y la banda sale de los percentiles de las réplicas. La mediana no coincide exactamente, porque la proyección no es lineal en ρ.
   - El pico debe ser un máximo con signo sobre esa trayectoria.
   - La skill pide además el pico del **nivel** en el adverso y su trimestre.
   - En RF-11 no existe una distribución conjunta de β_I y β_II: la diferencia entre modelos va solo como cifra puntual y sin banda, y hay que decirlo.

9. **Al plan le faltan pre-registros que la skill y la plantilla exigen, y que los planes 003/004 sí traían:** el valor de la semilla, las tolerancias de RNF-2 y RNF-4, las claves de `estres.*` (RF-15) y la regla para el autovalor mínimo (reutilizar el truncamiento de la 003 con su tolerancia) (`plan.md:22-23`, :49).

10. **D-ARCHIVO, RF-1 y RF-2** (`spec.md:69-70`, :125; `plan.md:37`):
    - Hay que fijar los archivos exactos: `2026_Final_Supervisory_Baseline_Domestic.csv`, `2026_Final_Supervisory_Severely_Adverse_Domestic.csv` y `2026_Final_Historic_Domestic.csv`. Son los *Final*, no los *Proposed*.
    - Su sha256 debe quedar en el plan antes del commit de pre-registro, y los archivos deben ir versionados en git (principio 1: clon limpio).
    - «Las unidades no coinciden» no se puede comprobar con un CSV que no trae unidades. Debe reemplazarse por cabeceras exactas, nombres de escenario y 13 trimestres «2026 Q1»–«2029 Q1».

11. **RF-5** (`spec.md:73`): los parámetros del ajuste de entrenamiento de la 003 (2000T1–2019T4) no están en el JSON. La spec debe decir que el test los obtiene de ese procedimiento o de una fixture.

**Menores**

12. `spec.md:11`: «Chow fallan en ambos» no es exacto. El Chow de 2008T3 pasa en el Modelo II (p = 0,168).
13. `spec.md:59`: el coeficiente de la tasa del Modelo I es β₄, no θ0.
14. `spec.md:127` contradice `plan.md:29`: el CSV termina en 2026T2; la fila 2026T3 solo existe en memoria (`PanelResult.full`).
15. RNF-5 (`spec.md:91`): «origen» debe significar el nivel y el ΔDR del ancla, no el trimestre de arranque.
16. Con θ = 0, el Δ del Modelo II en el primer trimestre es exactamente 0, porque todos sus controles van rezagados y son observados. Hay que declararlo para que nadie lo lea como un hallazgo.
17. RF-9: el código debe leer `reading.etiqueta` y detenerse si dice «evidencia fuerte», en coherencia con los casos límite.
18. URL: la matriz cita `publications/2026-stress-test-scenarios.htm` y la spec cita `supervisionreg/dfa-stress-tests-2026.htm`. Las dos existen; los CSV están en la segunda.

## Observaciones (no bloquean)
- **HAC como incertidumbre de parámetros.** La simulación Krinsky-Robb con la covarianza HAC es aceptable. Pero con RESET y Chow 2020T2 fallando, y con el pronóstico dinámico del Modelo I perdiendo frente al ingenuo (cociente de RMSE 1,625), la banda es una **cota inferior**. Conviene decirlo así en RF-14.
- **La inflación en el adverso de la Fed.** En el severamente adverso la inflación *baja* (de 2,8 a 1,0), y con π > 0 eso compensa parte del canal de actividad. Es una propiedad del escenario, no algo que S3 deba «corregir».
- **ΔTB3 por ΔFFR.** La aproximación es razonable porque solo entran cambios: la brecha de niveles es irrelevante.
- **Tareas.** Diez caben, con poco margen. Simplificar S3 libera una.

## Recomendación del revisor para cada decisión
1. **Origen y empalme.** Origen en `sample_end` = 2026T2, con DR y ΔDR observados como ancla. Re-fechar el escenario a 2026T3 con H = 13. PIB y π: niveles en logaritmos encadenados desde el observado, con la variación interanual de la spec 001. ΔU y ΔFFR: cambios de la propia trayectoria; el primero, contra la salida de la Fed en 2025T4. Mantener P5.
2. **Covarianza.** Usar solo el bloque sin dummies (las dummies quedan en 0 en el horizonte). Simetrizarlo no cuesta nada (la asimetría ya es 0) y es definido positivo: vale Cholesky o descomposición espectral, pero hay que fijar una y probarla. No hace falta truncar; si algún día hiciera falta, se aplica la regla de la 003.
3. **Marginal frente a condicionada.** Marginal.
   - Representa la incertidumbre muestral de los coeficientes que de verdad se usan, con el canal de la tasa apagado como supuesto prudencial, no como creencia.
   - La condicionada representaría «θ = 0 es la verdad» y obliga a reestimar.
   - En el Modelo II el problema crece: con dos θ de signos opuestos habría que elegir además entre condicionar cada θ_j = 0 o S = 0, otra decisión no pre-registrada.
   - Fijar en cero no obliga a condicionar.
4. **Réplicas explosivas y niveles negativos.** No descartar réplicas, reportar su proporción y resumir con percentiles, que aguantan las pocas réplicas extremas esperadas (unas 0,3 y 2 por cada 10 000). Un nivel negativo se reporta con aviso y sin truncarlo, porque truncar rompe la cancelación lineal.
5. **S3, crédito, sensibilidades y archivo.**
   - **S3:** descartar la opción A. Propone una «opción D»: la actividad del severamente adverso re-fechado, más una senda de alza de tasas tomada por código de `fedfunds_d` en 2022T1–2023T3 y luego ΔFFR = 0 como supuesto explícito, con la inflación igual a la base. Así se aísla la tasa y se cubre literalmente el ejemplo de la guía (más desempleo, menos PIB, tasa al alza). En el escenario principal coincide con el severo, y la sensibilidad (b) muestra lo que la tasa no aporta. Alternativa aceptable: la C.
   - **Crédito:** mantenerlo constante en el último valor observado. Su sensibilidad va sobre niveles; la elección de cero o de la media muestral por código debe fijarse ahora.
   - **Sensibilidades:** (a) y (b) sí; (c) no.
   - **Archivo:** los *Final Domestic*, con su sha256 y versionados en git.

## Lo que defendería ante el profesor
- La regla de la tasa viene de un pre-registro anterior a estimar la 004, y Δ es invariante a la constante, al crédito común y al ancla: el resultado depende solo de β y de la diferencia entre escenarios.
- Los coeficientes no se reestiman: la incertidumbre sale de la distribución marginal HAC, rotulada como incertidumbre de parámetros y no como intervalo de predicción.
- Los escenarios son los oficiales de la Fed, congelados con su huella, y su arranque se alinea con nuestro origen sin perder severidad.

## Lo que preguntaría el profesor
1. Si la Fed arranca en 2025T4 y ustedes en 2026T2, ¿proyectan el escenario completo o solo su cola, y cuánto desempleo adverso queda dentro?
2. ¿Por qué el escenario adverso no incluye el alza de tasas que pide la guía y, si la incluyen, por qué no cambia la morosidad proyectada?
3. ¿Cuánto cambiarían el pico y la banda si condicionaran en θ = 0, y por qué no lo hicieron?
