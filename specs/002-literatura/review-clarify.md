# Review Clarify — Spec 002 Literatura

## 1. Ambigüedades (requisitos que no se pueden verificar)

1. **RF-5 vs RF-7: Conteo de los 16 estudios mínimos**. RF-5 exige "al menos 16 estudios con Estado = 'verificado'". RF-7 añade 4 referencias de datos/método y dice explícitamente que "no cuentan para el mínimo de 16 estudios". Queda ambiguo si el total mínimo de filas verificadas en la matriz es 16 (solo estudios) + 4 (datos/método) = 20, o si los 16 incluyen de algún modo a las referencias de datos/método. La redacción "no cuentan para el mínimo de 16 estudios" sugiere 20 filas verificadas totales, pero RF-9 dice "exactamente una entrada por cada fila... con Estado = 'verificado'", lo que implicaría 20 entradas en `.bib`. No hay una RF que diga explícitamente "la matriz tendrá al menos 20 filas verificadas (16 estudios + 4 datos/método)".

2. **RF-4: Columnas de la matriz para referencias de datos/método**. La matriz exige columnas como "País y muestra", "Variable dependiente", "Regresores", "Método", "Hallazgo principal (una línea, con signo)" y "Sección principal (2.1–2.5)". Para las 4 referencias de datos/método (FRED, Fed 2026, Newey-West 1987, Jordà 2005) varias de estas columnas no tienen sentido semántico (ej. "Hallazgo principal con signo" para Newey-West). La spec no define qué valor poner en esas celdas (¿"N/A"? ¿vacío? ¿texto descriptivo?), lo que impide verificar el cumplimiento automatizado.

3. **RF-6: Completitud de campos para secciones 2.1–2.4**. RF-6 exige que los 6 estudios de la sección 2.5 tengan "país y muestra, variable dependiente, regresores y método completos". No especifica si los estudios de las secciones 2.1–2.4 (mínimo 2 cada una) deben tener también esos campos completos. La definición de "estudio empírico (2.5)" los requiere, pero para estudios teóricos/revisiones de 2.1–2.4 algunos campos pueden no aplicar. Sin criterio claro, no se puede testear la completitud de forma uniforme.

4. **RF-4 / RF-8: "Hallazgo principal (una línea, con signo)" para estudios no empíricos**. Para secciones 2.1–2.4 (teoría, revisiones, marco conceptual), la noción de "signo" (positivo/negativo) puede no aplicar. La spec no aclara qué se espera en ese campo para estudios que no reportan un coeficiente con signo.

5. **RF-20: Formato de la cabecera de la matriz**. "Documentará... la fecha de verificación y el conteo por sección principal (2.1 a 2.5) y de datos/método, como cabecera de la matriz." No define el formato exacto (¿tabla Markdown aparte? ¿comentario YAML? ¿filas especiales en la tabla principal?), por lo que no hay criterio objetivo para validar que está presente y correcta.

6. **RF-7: Dependencia de spec 001 para códigos FRED**. "La referencia de FRED nombrará los códigos de las series usadas (los de la spec 001) y la fecha de consulta". Si la spec 001 no está aprobada o sus códigos cambian, esta RF no es verificable de forma autónoma. No hay un fallback ni lista explícita en esta spec.

7. **RF-3: Sujeto "EL SISTEMA" para decisión humana**. "ENTONCES EL SISTEMA no atribuirá ese hallazgo: lo corregirá a lo que sí dice la fuente o marcará el estudio como 'pendiente-lectura'." La corrección de un hallazgo tras leer el resumen es una decisión intelectual humana, no una acción automática del sistema. La RF antropomorfiza el proceso y no define qué artefacto registra esa decisión (¿la matriz? ¿un log?).

8. **RF-12: "EL SISTEMA lo detectará con un test y fallará"**. Similar al anterior: la detección de inconsistencia matriz–`.bib` es una prueba (test) que se escribe en la implementación, no una acción del "sistema" en tiempo de ejecución. La redacción mezcla tiempo de desarrollo (tests) y tiempo de ejecución.

## 2. Contradicciones entre requisitos

1. **RF-5 (16 estudios) vs RF-6 (mínimos por sección) vs RF-7 (4 datos/método no cuentan)**. RF-6 suma mínimo 2×4 + 6 = 14 estudios. RF-5 pide 16. RF-7 añade 4 que "no cuentan para el mínimo de 16". La aritmética es consistente (16 + 4 = 20 filas verificadas totales), pero la redacción dispersa en tres RFs crea riesgo de interpretación errónea (ej. alguien podría leer RF-5 y RF-7 y pensar que el total es 16 incluyendo datos/método). No hay una RF única que declare el total mínimo de filas verificadas.

2. **RF-9 vs RF-11: Claves y campos obligatorios**. RF-9: "exactamente una entrada por cada fila... con Estado = 'verificado'". RF-11: "incluirá el campo `doi` en toda entrada que tenga DOI y, en las que no lo tengan..., el campo `url` oficial". Para las 4 referencias de datos/método (FRED, Fed 2026, Newey-West, Jordà), Newey-West (1987) y Jordà (2005) sí tienen DOI en Crossref. FRED y Fed 2026 no. RF-11 exige `url` para las que no tienen DOI, pero no aclara si Newey-West y Jordà deben llevar `doi` (sí, por "toda entrada que tenga DOI") y si FRED/Fed deben llevar `url` (sí). La contradicción potencial es si alguien omite `doi` en Newey-West alegando que es "datos/método"; RF-11 lo prohíbe pero RF-9 no lo menciona.

3. **RNF-1 (tests sin red) vs RF-13 a RF-18 (script consulta Crossref real)**. RNF-1 dice que los tests bloquean red y usan respuestas simuladas. RF-13–RF-18 describen el comportamiento del script `verify_refs.py` consultando Crossref real. No hay contradicción técnica (son contextos distintos: tests vs ejecución manual), pero la spec no separa claramente "tests del script" (simulados) de "ejecución del script contra Crossref real" (manual, criterio de finalización). RF-18 dice "ejecutado y anotado en review-validate.md", confirmando que la verificación real es manual. La ambigüedad está en que RF-13–RF-18 leen como requisitos funcionales del script, pero RNF-1 dice que los tests no usan red; no hay RF que diga "el script tendrá dos modos: test (simulado) y verificación real".

## 3. Casos límite no cubiertos

1. **Estudio relevante para varias secciones por igual**. Caso límite 80 dice "cuenta una sola vez, en su sección principal", pero no define criterio de desempate cuando la relevancia es simétrica (ej. un paper que estima modelo con variables macro Y política monetaria por igual para 2.2 y 2.3). Sin regla, la asignación es arbitraria y no verificable.

2. **DOI de capítulo de libro vs libro (caso límite 77)**. "El título que se compara es el del capítulo, no el del libro". Crossref a veces registra el capítulo con su propio DOI y a veces solo el libro. Si el capítulo no tiene DOI propio, ¿se usa el DOI del libro + URL de capítulo? ¿Cómo se verifica "Coincidencia" de título? No está cubierto.

3. **Crossref devuelve múltiples obras para un DOI** (raro pero posible por errores de metadatos). El script no tiene regla de desambiguación.

4. **Preprint vs versión publicada con DOIs distintos**. Caso límite 82: "se cita una sola, la publicada". Pero si la publicada no tiene DOI y la preprint sí, ¿qué DOI va en el `.bib`? ¿Cómo se verifica que el hallazgo atribuido está en la versión publicada si solo se leyó la preprint?

5. **Autores con apellidos compuestos/partículas (ej. "de la Fuente", "van der Waals")**. Caso límite 79 menciona tildes y mayúsculas, pero no partículas. La normalización "apellidoaño" (RF-10) podría generar colisiones o claves irreconocibles (ej. `delafuente2020` vs `fuente2020`).

6. **FRED: códigos de series de spec 001 no definidos aquí**. Si spec 001 cambia códigos o añade series, la referencia FRED en esta spec queda desactualizada sin mecanismo de sincronización.

7. **Newey-West (1987) y Jordà (2005): verificación de "Hallazgo principal con signo"**. Son papers metodológicos, no empíricos aplicados. No tienen "hallazgo principal con signo" en el sentido de la matriz. Caso límite 77 dice "capítulo de libro... título del capítulo", pero estos son artículos de revista. No hay caso límite para referencias metodológicas puras.

8. **Crossref caído durante verificación manual (RF-17)**. "La verificación queda 'no verificable' y la spec no se cierra". No hay criterio de reintento automático ni tiempo máximo de espera para considerar que el servicio "no está caído, es que el DOI no existe". RF-17 dice "reintentará un número acotado de veces" pero no define el número ni el backoff.

9. **Estudios de la lista semilla que son documentos de trabajo sin DOI**. Caso límite 74: "si no existe [URL oficial], se descarta con motivo (RF-2) y se sustituye". Pero RF-2 dice "se reemplazará por otro candidato verificado de la misma sección". Si la sección (ej. 2.3) ya tiene sus 2 mínimos con otros estudios, ¿el reemplazo cuenta para el mínimo de esa sección o es extra? No está claro.

## 4. Conflictos con docs/constitution.md

1. **Principio 1 (Reproducible de punta a punta) vs ausencia de integración en pipeline**. La constitución exige `uv run python -m src.pipeline all` que reproduzca todo. Esta spec genera `research/matriz-literatura.md` y `report/references.bib` y un script `verify_refs.py`, pero no hay RF que diga en qué etapa del pipeline (`data|models|stress|report|all`) se generan ni cómo se integran. El script de verificación (RF-13–RF-18) no está referenciado en ninguna etapa del pipeline. Sin esto, el principio 1 no se cumple para los artefactos de esta spec.

2. **Principio 3 (Lógica separada de presentación) vs script `verify_refs.py`**. El principio 3 exige funciones puras en `src/` (reciben datos y parámetros; sin red, disco ni gráficos). El script `verify_refs.py` por definición consulta red (Crossref) y lee disco (`.bib`, matriz). RF-19 dice "no modificará... solo lee y reporta", pero sigue teniendo side effects de red. Debe estar fuera de `src/` (en `scripts/` está bien), pero la spec no ubica explícitamente el archivo ni su firma funcional para tests.

3. **Principio 5 (Cero citas inventadas) vs RF-3 "EL SISTEMA lo corregirá"**. El principio 5 es una prohibición absoluta ("prohíbe cualquier referencia sin DOI o URL verificada"). RF-3 permite un flujo donde se "corrige el hallazgo a lo que sí dice la fuente" tras detectar que no está respaldado. Eso es correcto, pero la redacción "EL SISTEMA lo corregirá" sugiere automatización de una juicio experto. No hay conflicto directo, pero la redacción podría interpretarse como que el sistema reescribe el hallazgo sin supervisión humana, lo que violaría el principio 5 (el hallazgo corregido debe venir de lectura humana verificada).

4. **Principio 4 (Tests como puerta) vs RNF-1**. RNF-1 dice "los tests del script usan respuestas de Crossref simuladas... La verificación contra Crossref real es una ejecución manual del script, fuera de `uv run pytest -q`". Esto alinea con el principio 4 (tests sin red pasan en CI), pero la spec no tiene una RF que exija explícitamente "existen tests pytest para `verify_refs.py` con mocks de Crossref que cubran: DOI correcto, inexistente, título distinto, autor distinto, año distinto, error de servicio". Sin esa RF, no hay criterio de finalización testeable para el script.

## 5. Requisitos de la guía del profesor que esta spec debería cubrir y no cubre

1. **Sección 2.5: "explicar qué variables y metodologías utilizaron"**. La guía (línea 21) pide que la evidencia empírica explique variables y metodologías. RF-6 exige para 2.5 "país y muestra, variable dependiente, regresores y método completos". Cubre variables y método, pero no exige explícitamente que la matriz capture la **transformación de variables** (ej. "crecimiento interanual del PIB", "tasa de desempleo en nivel", "cambio en FFR") ni la **frecuencia y período de la muestra** de cada estudio, que son relevantes para comparar con la especificación de los modelos (specs 003/004). La guía menciona frecuencia trimestral y período 2000–2026 (líneas 66, 75); la matriz no tiene campo para "frecuencia" ni "período de muestra".

2. **Variables específicas de la guía**. La guía (líneas 26–27) lista variables concretas: DRALACBS (riesgo de crédito), GDP, UNRATE, CPIAUCSL, FEDFUNDS, serie de crédito. RF-7 dice que la referencia FRED citará "los códigos de las series usadas (los de la spec 001)". La matriz de literatura no tiene un campo que permita mapear cada estudio a qué variables de estas usó (o sus análogos), dificultar luego en spec 006 escribir "estudios que usaron desempleo como X encuentran...". RF-8 pide describir el método en términos agrupables, pero no un campo estructurado para "variables macroeconómicas usadas" mapeables a la lista de la guía.

3. **Dos modelos econométricos (secciones 4 y 5 de la guía)**. La guía define Modelo I (determinantes macro) y Modelo II (política monetaria con rezagos/shocks). La spec 002 dice en "Pregunta que responde" que la matriz "aporta la base de las secciones 2.1–2.5" y en "Usuarios" que las specs 003, 004 y 005 "citan estudios para justificar variables, rezagos y signos". Pero no hay RF que exija en la matriz un campo o etiqueta que vincule cada estudio a **qué modelo (I o II) y qué variable/rezago/signo específico justifica**. Sin eso, la trazabilidad de specs 003/004 a la literatura es manual y no auditable.

4. **Referencia a escenarios de estrés 2026 de la Fed (sección 7 de la guía)**. RF-7 incluye "escenarios de estrés 2026 de la Reserva Federal" como referencia de datos/método. La guía (línea 47) dice "construir un escenario macroeconómico adverso... Por ejemplo: aumento del desempleo, desaceleración del PIB y aumento de la tasa de política monetaria". La matriz no captura qué variables del escenario adverso (desempleo, PIB, FFR) tienen respaldo literario para su efecto sobre riesgo de crédito. Sería útil un campo o nota en la matriz que enlace estudios a variables de escenario.

5. **Formato APA en referencias (sección 10 de la guía)**. La guía exige APA. La spec usa claves `apellidoaño` y `apa.csl` en spec 006. Correcto. Pero no hay RF que valide que el `.bib` genera referencias APA 7 correctas al renderizar (ej. autores corporativos "Board of Governors...", capítulos de libro, et al.). El script `verify_refs.py` valida DOI/URL, no formato APA. La validación APA queda delegada a spec 006 (render Quarto), pero si el `.bib` tiene errores de campos (ej. `author` mal formado para autor corporativo), el fallo se detecta tarde. Un test de render mínimo en esta spec daría feedback temprano.

---

**Nota**: Este informe solo detecta hallazgos. No propongo soluciones. Cada ítem indica la RF, principio o sección de la guía involucrada y qué falta para que sea verificable.