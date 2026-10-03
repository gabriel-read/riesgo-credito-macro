# Review Clarify — Spec 001 Datos

**Fecha:** 2026-10-02
**Revisor:** QA (OpenCode)
**Skill de dominio:** datos-fred

---

## 1. Ambigüedades (requisitos que no se pueden verificar)

1. **RF-7 — Marcador de faltante de FRED no especificado.** El requisito habla de "valores no numéricos distintos del marcador de faltante de FRED", pero no define cuál es ese marcador (¿`.`? ¿`NaN`? ¿`""`? ¿`NA`?). Sin un valor exacto, no se puede verificar si el sistema lo detecta correctamente.

2. **RF-19 — "Forma tal cual" ambigua.** El requisito dice "en su forma tal cual y en primera diferencia", pero RF-9 ya define transformaciones específicas (variación interanual, logit, etc.). ¿La "forma tal cual" es la transformación de RF-9 o el nivel original? Si es la transformación, ¿la primera diferencia se aplica sobre la transformación o sobre el nivel original? Esto cambia completamente los resultados de las pruebas.

3. **RF-20 — Límites de p-valor no especificados.** La regla dice "al 5 %" pero no aclara si es p < 0,05 o p ≤ 0,05. Tampoco define si "ninguna rechaza" significa p ≥ 0,05 en ambas pruebas o p > 0,05.

4. **RF-21 — "No cumple la regla de estacionariedad" ambiguo.** No especifica qué significa exactamente "no cumple": ¿sigue siendo ambigua? ¿ADF no rechaza y KPSS rechaza? ¿Se debe diferenciar de nuevo antes de marcar como I(2)?

5. **RNF-4 — Redundancia en detección de cifras.** "Cifras escritas a mano con uno o más decimales o con el signo de porcentaje, además de las de dos o más decimales que ya detecta" — "uno o más decimales" ya incluye "dos o más decimales". ¿Qué detecta exactamente? ¿Es un error de redacción o hay una distinción que no se explica?

6. **RF-22 — "Unidades indicadas" sin especificar.** No dice qué unidades deben mostrarse en los ejes (¿%? ¿pp? ¿puntos básicos? ¿puntos de porcentaje?). Sin esto, no se puede verificar el gráfico.

7. **RF-23 — "Panel final" no definido.** ¿Es el panel de RF-16 (todas las variables transformadas)? ¿Un panel solo con las 4 series de la guía? ¿El panel recortado a la muestra de estimación? No se puede verificar sin una definición clara.

8. **RF-23 — Inconsistencia con el ejemplo de la guía.** El ejemplo de la sección 11 descarga desde 2000-01-01 hasta 2026-01-01, pero la spec descarga desde 1998-01-01. ¿El notebook debe leer las descargas ya hechas (desde 1998) o simular el ejemplo (desde 2000)?

9. **RF-9 — "Historia descargada completa" ambigua.** ¿Significa toda la historia disponible en FRED (algunas series empiezan antes de 1998) o solo lo descargado desde 1998-01-01? Si una serie tiene datos anteriores a 1998, ¿se incluyen en el cálculo de las transformaciones?

10. **RF-13 — "Cobertura de 2000T1" ambigua.** ¿Qué pasa si una serie no tiene datos en 2000T1 pero sí antes? ¿Se detiene el pipeline o se recorta el inicio de la muestra? No se especifica.

11. **RF-11/RF-12 — Excepción de octubre 2025 no limitada.** La skill datos-fred dice que octubre 2025 falta en CPIAUCSL y UNRATE, pero la spec no limita la excepción a estas dos series. ¿Qué pasa si otra serie también falta en octubre 2025? ¿Se aplica la misma excepción o se detiene?

12. **RF-15 — Error de logit sin especificar el valor recibido.** El requisito dice "se detendrá con un error que nombre la serie y el trimestre", pero no especifica si el error debe incluir el valor problemático recibido.

---

## 2. Contradicciones entre requisitos

1. **RF-9 vs RF-10 — Orden de transformaciones y recorte.** RF-9 dice que las transformaciones se calculan "sobre la historia descargada completa y antes de recortar a la muestra", pero RF-10 dice "recortará el panel a la muestra de estimación". Si las transformaciones se calculan antes de recortar, ¿el panel recortado ya tiene las transformaciones? ¿O se calculan sobre el panel recortado? El orden no está claro y afecta a los resultados.

2. **RF-19 vs RF-9 — "Primera diferencia" sobre qué.** RF-19 pide pruebas "en su forma tal cual y en primera diferencia", pero RF-9 ya define transformaciones (variación interanual, logit, etc.). Si la "forma tal cual" es la transformación de RF-9, ¿la primera diferencia es de la transformación o del nivel original? Esto cambia los resultados de ADF y KPSS.

3. **RF-20 vs RF-21 — Jerarquía de decisiones no clara.** RF-20 dice que si una serie es ambigua se usa en primera diferencia. RF-21 dice que si "en primera diferencia tampoco cumple la regla" se marca como I(2). Pero no se especifica: ¿se vuelve a aplicar la regla de RF-20 sobre la primera diferencia? ¿O se usan criterios diferentes?

4. **RF-23 vs RF-1 — Número de series.** RF-23 habla de "el ejemplo de la sección 11 de la guía" que usa 4 series (GDP, UNRATE, CPIAUCSL, FEDFUNDS), pero RF-1 descarga 13 series. ¿El notebook debe mostrar las 4 series de la guía o las 13 del pipeline?

5. **RF-11/RF-12 vs skill datos-fred — Excepción de 2025T4.** La skill datos-fred limita la excepción a CPIAUCSL y UNRATE, pero la spec no lo hace. Si otra serie falta en octubre 2025, ¿se aplica la misma lógica o se detiene?

---

## 3. Casos límite no cubiertos

1. **Series con datos anteriores a 1998-01-01.** ¿Qué pasa si FRED devuelve datos anteriores a la fecha de descarga especificada? ¿Se incluyen en el cálculo de las transformaciones o se ignoran?

2. **Último trimestre común anterior a 2000T1.** ¿Qué pasa si el último trimestre común es anterior a 2000T1? ¿Se detiene el pipeline? ¿Se ajusta la muestra?

3. **Series con una sola observación.** ¿Qué pasa si después de recortar a la muestra de estimación una serie tiene solo una observación? ¿Se detiene?

4. **Series constantes.** ¿Qué pasa si una serie tiene la misma observación en todo el período? ADF y KPSS pueden fallar o dar resultados no concluyentes.

5. **Fallo de convergencia de ADF o KPSS.** ¿Qué pasa si las pruebas no convergen o lanzan advertencias? No se especifica cómo manejar estos casos.

6. **Descargas con fechas diferentes.** RF-6 dice "la descarga registrada más reciente de cada serie", pero no especifica qué hacer si una serie tiene descargas de diferentes feces y la más reciente tiene menos datos que una anterior.

7. **Panel vacío después del recorte.** ¿Qué pasa si después de recortar a la muestra de estimación el panel está vacío o tiene muy pocas observaciones?

8. **Notebook sin descargas crudas.** RF-24 dice "se ejecutará el notebook de principio a fin sin errores desde las descargas crudas guardadas", pero no especifica qué pasa si no hay descargas crudas (¿debería fallar con un error claro?).

9. **Valores extremos en las series.** ¿Qué pasa si una serie tiene valores extremos (outliers) que afectan las transformaciones? No se especifica ningún tratamiento.

10. **Cambios de frecuencia inesperados.** ¿Qué pasa si FRED cambia la frecuencia de una serie (por ejemplo, de mensual a trimestral)? No se especifica cómo detectar o manejar esto.

---

## 4. Conflictos con docs/constitution.md

1. **Principio 1 — Reproducible de punta a punta.** La spec no menciona explícitamente que `uv run python -m src.pipeline all` debe reproducir los datos desde un clon limpio. Aunque RF-1 a RF-24 cubren las etapas, no se especifica la integración con el pipeline general.

2. **Principio 3 — Lógica separada de presentación.** La spec no menciona que las funciones deben ser puras en `src/`, sin red, disco ni gráficos. RNF-2 solo menciona "sin red en tests", pero no cubre la separación general entre lógica y presentación.

3. **Principio 4 — Tests como puerta.** La spec menciona tests en RNF-3 y en criterios de finalización, pero no especifica que los tests deben correr antes de cada cambio ni que prohíbe avanzar con tests en rojo.

4. **Principio 5 — Cero cifras o citas inventadas.** RNF-4 cubre el guardarraíl de cifras, pero no menciona explícitamente que todo número del informe debe venir de `outputs/` por código.

5. **Principio 6 — Idioma.** RNF-5 menciona "identificadores en inglés", pero no especifica que el código en `src/` debe estar en inglés (solo menciona etiquetas de tablas y gráficos).

---

## 5. Requisitos de docs/guia-profesor.md que esta spec debería cubrir y no cubre

1. **Sección 3.1 — Fuentes de datos.** La guía pide "presentar las variables, frecuencia, período y fuentes". La spec cubre variables, frecuencia y período, pero no menciona explícitamente que la nota de datos debe incluir las fuentes (FRED, pandas-datareader, etc.).

2. **Sección 3.2 — Descripción de la variable dependiente.** La guía pide describir la variable dependiente (tasa de morosidad). La spec usa DRALACBS, pero no especifica que la nota de datos debe describir esta variable en detalle.

3. **Sección 3.3 — Descripción de variables macroeconómicas.** La guía pide describir las variables macroeconómicas (crecimiento del PIB, desempleo, inflación, tasa de interés, crecimiento del crédito). La spec incluye estas variables, pero no especifica que la nota de datos debe describir cada una.

4. **Sección 3.4 — Cambio en la FFR.** La guía pide el "cambio en la Federal Funds Rate (FFR)". La spec incluye FEDFUNDS en nivel y diferencia, lo cual cubre esto, pero no especifica que la nota de datos debe explicar por qué se incluye ambas formas.

5. **Sección 11 — Notebook educativo.** La guía dice "El objetivo es que el estudiante aprenda a utilizar Python como herramienta para la obtención y preparación de datos económicos y financieros". La spec incluye un notebook de demostración (RF-23, RF-24), pero no especifica que debe ser educativo o enseñar a descargar datos.

6. **Sección 11 — No búsqueda manual de datos.** La guía dice "No deberán realizar una búsqueda manual de datos". La spec no menciona explícitamente que no debe haber búsqueda manual de datos.

7. **Sección 11 — Período 2000–2026.** La guía especifica el período "2000–2026". La spec usa 2000T1 como inicio, lo cual es consistente, pero no especifica el final exacto (depende del último trimestre común). ¿Se debe documentar el final esperado?

8. **Sección 11 — Serie de crédito.** La guía dice "Crédito | Serie FRED seleccionada | Mensual/Trimestral". La spec usa LOANS, pero no especifica que esta es la serie seleccionada para crédito ni documenta la elección.

9. **Sección 11 — Uso de pandas_datareader.** La guía muestra un ejemplo con `pandas_datareader`. La skill datos-fred lo menciona, pero la spec no lo hace. ¿Se debe documentar en la nota de datos?

10. **Sección 11 — Aprendizaje de Python.** La guía enfatiza que el objetivo es aprender Python. La spec no menciona que el notebook debe incluir comentarios educativos o explicaciones paso a paso.

---

## Resumen

| Categoría | Cantidad |
|---|---|
| Ambigüedades | 12 |
| Contradicciones | 5 |
| Casos límite no cubiertos | 10 |
| Conflictos con constitución | 5 |
| Requisitos de guía no cubiertos | 10 |

**Total: 42 hallazgos**
