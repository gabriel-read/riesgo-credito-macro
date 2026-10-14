<!-- Copia literal del mensaje final del subagente profesor-evaluador (id ac5bbc2703f3ca4e3), extraída del registro de subagentes de la sesión. Ronda 1, 2026-10-12. -->

# Evaluación del informe como profesor, contra `docs/guia-profesor.md`

Revisé las fuentes (`report/informe.qmd`, `report/secciones/*.qmd`, `report/anexos/*.qmd`) y las cifras de `report/_variables.yml`. El PDF no se puede renderizar en este entorno, así que leí las páginas ya renderizadas en `outputs/preview-006/qa-principal/` y `qa-anexo/`. No existe `report/slides.qmd`, así que no pude evaluar las diapositivas.

**VEREDICTO: CAMBIOS REQUERIDOS.** Como trabajo académico aprueba con holgura. No debe entregarse tal como está: tiene dos defectos bloqueantes y un problema de coherencia en el estrés que un evaluador de riesgos detectaría enseguida.

## Evaluación por sección

| Sección | Calificación | Por qué |
|---|---|---|
| 1. Introducción | Cumple | Plantea el problema, su relevancia, la pregunta literal y el objetivo, y fija desde el inicio el lenguaje de asociación. |
| 2.1–2.4 | Cumple parcialmente | Cada subsección se apoya en solo 2 estudios, y casi todos son teóricos o no miden morosidad (el propio texto lo admite). |
| 2.5 | Cumple | Explica las variables y los métodos de cada estudio (panel, GMM, FGLS, MCO, ARDL, PVAR). Pero Obradović y Grubišić (2026), el único estudio de política monetaria sobre morosidad, queda con signo «—» y no se discute. La tabla ocupa 5 páginas del cuerpo. |
| 3.1–3.4 | Cumple | Declara series, frecuencia, período, el vintage, el hueco de octubre de 2025 y las desviaciones (GDPC1, LOANS, ΔFFR como tasa única). |
| 3.5 | Cumple parcialmente | Describe los modelos solo con palabras: no hay ninguna ecuación en todo el informe. Además arrastra texto interno («Esta continuación pertenece a la subsección…»). |
| 4. Modelo I | Cumple | Estima, interpreta en pp, separa impacto de largo plazo, evalúa significancia y robustez (9 variantes), hace diagnósticos completos y prueba fuera de muestra, y cierra con una lectura de gestión. |
| 5. Modelo II | Cumple parcialmente | La regla, el Granger, las proyecciones locales y los diagnósticos están bien. Pero no muestra ni comenta sus controles, y la robustez sin pandemia y sin tramos de tasa cero (R2, R3) no aparece en el cuerpo. |
| 6.1–6.3 | Cumple parcialmente | 6.3 contiene un error de hecho (hallazgo B2). |
| 6.4 | Cumple | Responde de forma diferenciada: el entorno macro es relevante por inflación y crédito; la política monetaria no muestra asociación propia, y se explica por qué eso no prueba ausencia. |
| 7. Estrés | Cumple parcialmente | Construye el escenario adverso, lo compara con el base y calcula el cambio (+1,428 pp en el Modelo I, +0,827 en el Modelo II, con bandas y sensibilidades). No explica qué variables generan ese cambio, y el escenario D (alza de tasas) da una proyección idéntica al adverso (hallazgo I1). |
| 8. Implicaciones | Cumple | Cubre los siete puntos, añade un tablero indicador → criterio → acción y lo conecta con el resultado de aprendizaje de la asignatura. |
| 9. Conclusiones | Cumple | Responde la pregunta y dice cómo anticipar, dimensionar y gestionar; evita el formato prohibido. La afirmación sobre el desempleo omite el Modelo II. |
| 10. Referencias | Cumple parcialmente | Todas tienen DOI o URL, pero no siguen bien APA 7 (hallazgo M1). |
| 11. Datos | Cumple | Hay pipeline reproducible con `pandas_datareader`, aunque incluye texto que no va dirigido al lector (hallazgo B1). |
| Diapositivas | No evaluable | `report/slides.qmd` no existe y la entrega es el 15 de octubre. |

## Calificación por criterio

| Criterio | Peso | Puntos |
|---|---|---|
| Estructura de 11 secciones | 10 | 9 |
| Pregunta y objetivo | 5 | 5 |
| Uso de literatura | 15 | 12 |
| Datos y metodología | 10 | 7 |
| Modelo I | 12 | 11 |
| Modelo II | 12 | 9 |
| Integración de resultados (6) | 8 | 5,5 |
| Estrés | 10 | 7,5 |
| Implicaciones de gestión | 8 | 7 |
| Conclusiones | 5 | 4 |
| APA | 3 | 1,5 |
| Claridad y edición | 2 | 1 |
| **Total** | **100** | **79,5** |

## Hallazgos

**Bloqueantes**

- **B1. El documento se presenta como un borrador.**
  - El subtítulo del informe dice «Versión de trabajo; validación global y auditoría pendientes» (`report/informe.qmd:3`). El del anexo dice «validación global pendiente».
  - Hay texto interno del proyecto en el cuerpo:
    - `03f-limitaciones.qmd:1` explica que «no repite su encabezado».
    - La sección 11 habla de Google Docs, «URLs ficticias» y «si el profesor exige una única entrega».
    - En el PDF impreso aparecen «Abrir anexo PDF · Abrir anexo DOCX».
    - La página 13 dice «entra en primera diferencia (primera diferencia)».
  - Falta la portada APA 7 de estudiante: autor, institución, curso, profesor y fecha.
- **B2. La sección 6.3 afirma algo falso y la integración de los modelos queda incompleta.**
  - `06-resultados.qmd:46` dice que las demás variables «solo entran al Modelo I». En realidad, el Modelo II incluye esas variables rezagadas como controles.
  - Varios de esos controles son significativos en el Modelo II: desempleo rezagado 0,110 (p 0,039), inflación rezagada 0,024 (p 0,015) y crédito rezagado 0,007 (p 0,009).
  - Así, la conclusión de que el desempleo «no se distingue de cero» ignora un resultado del propio informe.
  - 6.4 dice que la lectura sobre inflación y crédito «no depende de un solo modelo», lo que se apoya justo en lo que 6.3 niega.

**Importantes**

- **I1. El estrés trata los coeficientes de forma asimétrica y no explica de dónde sale su resultado.**
  - El coeficiente de la tasa se fija en cero porque no es significativo, pero el del desempleo (p 0,214, robusto en 1 de 9 variantes) se usa completo.
  - Hice una descomposición aproximada con las trayectorias de AT-EST-PATHS. El +1,43 pp del Modelo I sale sobre todo del producto (cerca de +1,0) y del desempleo (cerca de +0,8).
  - La inflación, el hallazgo «más estable» del informe, lo reduce en unos 0,6–0,7 pp, porque baja en el escenario adverso. El crédito no aporta nada, porque el supuesto es el mismo en ambos escenarios.
  - Es decir, el número del estrés descansa en las variables más débiles. El informe no lo dice.
  - Además, el escenario D (alza de tasas), que es el ejemplo de la guía, da una proyección idéntica al adverso. En la figura, la línea roja del adverso queda tapada.
- **I2. El Modelo II no muestra su robustez en el cuerpo.** La tasa estuvo cerca de cero en buena parte de la muestra (2009–2015 y 2020–2021). La variante R3 que excluye esos tramos existe en el anexo (n = 69, también «sin evidencia»), pero el texto principal no la menciona.
- **I3. No hay especificación formal.** No hay ecuaciones de los Modelos I y II ni de las proyecciones locales.
- **I4. El anexo es difícil de usar.**
  - Las tablas están partidas en paneles de 4 columnas, y algunos paneles pierden las columnas que identifican cada fila. Por ejemplo, el panel 2 de AT-EST-DELTA repite «modelo1» 26 veces sin escenario ni trimestre.
  - Hay nombres de código en las tablas (`gdp_growth`, `d_ffr`, `prop_c_pos_pico`) y una columna sin nombre (``) en AT-STATIONARITY.
  - Las notas hablan de «spec 001» y citan rutas `outputs/tables/*.csv` como fuente.
- **I5. Falta poner las magnitudes en contexto de riesgo.**
  - El nivel estresado (3,42 pp, con pico de 3,72 pp) no se compara con el máximo histórico (7,35 pp en 2010T1) ni con la media (2,63 pp).
  - Los efectos por desviación estándar (por ejemplo, 0,087 pp de largo plazo para la inflación) solo están en el anexo.
  - No se explica por qué el escenario base sube de 1,42 a 1,99 pp con un crecimiento cercano al 2 %.

**Menores**

- **M1. APA 7 incompleto.**
  - Los títulos de artículo están en mayúsculas de título, no en minúscula de oración.
  - Los rangos de páginas usan guion en lugar de raya (95-110).
  - Newey y West (1987) solo indica «703» como página.
  - La Fed figura a la vez como autor y como editorial.
  - FRED no tiene fecha de consulta.
  - Los documentos de trabajo del FMI no llevan número.
  - Las tablas del cuerpo no tienen número ni título («Tabla N»), aunque las figuras sí.
  - La tabla de literatura usa nombres completos («Wu, Jing Cynthia y Xia, Fan Dora») y la expresión «tipo de interés de lending».
- **M2. Pequeñas inconsistencias.**
  - En la tabla de coeficientes el valor p del crédito aparece como «0,000» y en el texto como «< 0,001».
  - Varias tablas del anexo no tienen remisión desde el informe: AT-LIT-ESTUDIOS, AT-DESCRIPTIVES, AT-EST-RATE-SENSITIVITY, AT-EST-ORIGIN y las robusteces del Modelo II.
  - La serie dependiente no se grafica en el cuerpo; solo aparece como figura A.1 del anexo.

**Correspondencia entre informe y anexo: correcta en lo esencial.** Los 23 identificadores citados en el informe existen en el anexo y están en el anexo que se indica (las desviaciones y el manifiesto en F, el Modelo II en C, el estrés en D). La única excepción es que 03f cita AT-M1-DIAGNOSTICS sin indicar el anexo.

## Nota estimada: 79/100

Es honesto, reproducible y riguroso en diagnósticos, y la sección 8 es sobresaliente. Pierde puntos por el aspecto de borrador, la falta de ecuaciones, el error de 6.3 y un estrés cuyo resultado no se explica y contradice parcialmente las alertas que el propio informe recomienda vigilar. Con las cinco mejoras siguientes, calculo que llegaría a 87–90.

## Las 5 mejoras de mayor impacto

1. Quitar todo el texto de borrador e interno y añadir la portada APA (B1).
2. Corregir 6.3 e integrar los controles del Modelo II, en especial el desempleo, en 6.1–6.4 y en la conclusión (B2).
3. Añadir al estrés una descomposición del cambio por variable. Discutir la asimetría «desempleo se usa, tasa se anula» y la dirección contraria de la inflación (I1).
4. Escribir las ecuaciones de los dos modelos en 3.5 (I3) y llevar al cuerpo la robustez del Modelo II con tasa cero (I2).
5. Situar las magnitudes frente a la historia de la morosidad y arreglar las tablas del anexo: columnas de identificación, nombres legibles y numeración APA (I5, I4, M1).

## Preguntas que haría en la exposición, y si el informe las responde

| Pregunta | ¿La responde? |
|---|---|
| ¿Por qué el estrés usa el coeficiente no significativo del desempleo y anula el de la tasa? | No |
| ¿Qué variables producen los +1,43 pp? Si la inflación «es la alerta», ¿por qué en el adverso la reduce? | No |
| En el Modelo II el desempleo rezagado es significativo (p 0,039). ¿Por qué la conclusión dice que no se distingue de cero? | No |
| Con buena parte de la muestra con la tasa cerca de cero, ¿qué identifica ΔFFR? | Parcial (solo en el anexo) |
| ¿Es económicamente relevante 0,020 pp por punto de inflación? ¿Qué es 3,4 pp frente a 2010? | Parcial |
| ¿Cómo convierte un banco +1,43 pp en provisiones o capital (pérdida esperada = PD × LGD × EAD)? | Parcial (solo cualitativo) |
| ¿Por qué el base sube a 1,99 pp con un crecimiento cercano al 2 %? | Parcial (por el supuesto de crédito) |
| ¿Cómo separa la reacción de la Fed de un efecto de la tasa? | Sí |
| ¿Por qué creer los p-valores de variables que no son claramente estacionarias? | Sí (6.4) |
| ¿Por qué el escenario adverso no sube la tasa, como pide la guía? | Sí (escenario D y sensibilidad) |

Las cinco más difíciles son las cinco primeras.

## Checklist de la skill
- **11 secciones en orden:** sí, comprobado en `informe.qmd` y en el índice de la página 1.
- **Números escritos a mano:** no encontré ninguno; todas las cifras salen de `{{< var >}}` o de tablas incluidas.
- **Citas fuera de `references.bib`:** ninguna; las 19 referencias de las páginas 30–32 se corresponden con las citas del texto.
- **La conclusión responde y dice cómo anticipar:** sí.
- **Siete puntos de la sección 8:** sí, todos cubiertos.
- **Sin resolver en la salida:** no hay `?@` ni `{{<` en las páginas revisadas. Sí hay texto de enlaces y glosas internas (B1).

Archivos relevantes: `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/06-resultados.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/07-estres.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/03f-limitaciones.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/11-datos-descarga.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/informe.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/anexos/D-estres.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/_variables.yml`.