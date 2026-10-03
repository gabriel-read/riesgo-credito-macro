# Guía del profesor (requisitos oficiales — no editar)

## Título propuesto
Condiciones macroeconómicas, política monetaria y riesgo de crédito: evidencia empírica y análisis de escenarios

## Pregunta de investigación
¿En qué medida las condiciones macroeconómicas y los cambios en la política monetaria afectan el riesgo de crédito, y cómo pueden estos efectos ser utilizados para fortalecer la gestión y monitoreo del riesgo financiero?

## Estructura de la investigación

### 1. Introducción
Presentar el problema, su relevancia para la estabilidad financiera y la gestión del riesgo de crédito.
- Pregunta de investigación: ¿En qué medida las condiciones macroeconómicas y los cambios en la política monetaria afectan el riesgo de crédito?
- Objetivo general: Evaluar empíricamente el efecto de las condiciones macroeconómicas y de la política monetaria sobre el riesgo de crédito, utilizando modelos econométricos y escenarios de estrés.

### 2. Revisión de literatura
- 2.1 Riesgo de crédito y ciclo económico
- 2.2 Determinantes macroeconómicos del riesgo de crédito
- 2.3 Política monetaria y condiciones financieras
- 2.4 Transmisión de la política monetaria al riesgo de crédito
- 2.5 Evidencia empírica: encontrar estudios que hayan estimado relaciones similares y explicar qué variables y metodologías utilizaron.

### 3. Datos y metodología
- 3.1 Descripción de los datos: presentar las variables, frecuencia, período y fuentes.
- 3.2 Variable dependiente: riesgo de crédito. Por ejemplo: tasa de morosidad de los préstamos bancarios.
- 3.3 Variables macroeconómicas: crecimiento del PIB; desempleo; inflación; tasa de interés; crecimiento del crédito.
- 3.4 Variable de política monetaria: cambio en la Federal Funds Rate (FFR).
- 3.5 Metodología econométrica: explicar los dos modelos que serán estimados.

### 4. Modelo I: Determinantes macroeconómicos del riesgo de crédito
Pregunta específica: ¿Cómo afectan las condiciones macroeconómicas al comportamiento del riesgo de crédito?
Los estudiantes deberán: estimar el modelo; analizar los coeficientes; evaluar su significancia; realizar pruebas de diagnóstico; interpretar los resultados desde la perspectiva de gestión de riesgo.

### 5. Modelo II: Política monetaria y riesgo de crédito
Pregunta específica: ¿Cómo afectan los cambios en la política monetaria al riesgo de crédito y existen efectos rezagados sobre la calidad de la cartera?
Aquí el objetivo es identificar si un shock de política monetaria tiene relación con el deterioro posterior del riesgo de crédito.

### 6. Análisis de resultados
Esta sección debe integrar los dos modelos.
- 6.1 Resultados del Modelo I
- 6.2 Resultados del Modelo II
- 6.3 Comparación de resultados
- 6.4 Discusión económica de los resultados. La pregunta fundamental será: ¿Los resultados econométricos proporcionan evidencia de que el entorno macroeconómico y la política monetaria constituyen factores relevantes para el riesgo de crédito?

### 7. Análisis de escenarios y pruebas de estrés
Los estudiantes deberán construir un escenario macroeconómico adverso y utilizar los modelos estimados para evaluar su impacto sobre el riesgo de crédito.
Por ejemplo: escenario adverso: aumento del desempleo, desaceleración del PIB y aumento de la tasa de política monetaria.
El estudiante debe estimar el riesgo de crédito bajo el escenario adverso vs. el escenario base y calcular el cambio en el riesgo de crédito.

### 8. Implicaciones para la gestión de riesgos
Esta sección debe responder: ¿Cómo podrían utilizarse estos resultados en una institución financiera?
Deberán discutir: indicadores de alerta temprana; monitoreo macroeconómico; políticas de crédito; escenarios de estrés; planificación de capital; gestión de cartera; seguimiento de concentración y calidad crediticia.
Esto conecta directamente con el RAE de la asignatura relacionado con identificar, medir, monitorear y gestionar los principales riesgos financieros.

### 9. Conclusiones
La conclusión debe responder directamente a la pregunta de investigación.
No se acepta una conclusión del tipo: "El PIB fue significativo y el desempleo también."
Sino algo como: ¿Qué nos dicen los resultados sobre la relación entre el ciclo económico, la política monetaria y el riesgo de crédito? Y, sobre todo: ¿Cómo puede utilizarse esta información para anticipar y gestionar el riesgo?

### 10. Referencias
Formato APA.

### 11. Base de datos y descarga de información
No deberán realizar una búsqueda manual de datos. Se les proporcionará un notebook de Python que permitirá descargar directamente las series macroeconómicas desde FRED (Federal Reserve Economic Data). El objetivo es que el estudiante aprenda a utilizar Python como herramienta para la obtención y preparación de datos económicos y financieros.

| Variable | Serie FRED | Frecuencia |
|---|---|---|
| Riesgo de crédito | DRALACBS | Trimestral |
| PIB | GDP | Trimestral |
| Desempleo | UNRATE | Mensual |
| Inflación | CPIAUCSL | Mensual |
| Federal Funds Rate | FEDFUNDS | Mensual |
| Crédito | Serie FRED seleccionada | Mensual/Trimestral |

El período de análisis será 2000–2026.

Descarga de datos mediante Python con la biblioteca pandas_datareader:

```python
import pandas_datareader.data as web

data = web.DataReader(
    ["GDP", "UNRATE", "CPIAUCSL", "FEDFUNDS"],
    "fred",
    start="2000-01-01",
    end="2026-01-01"
)

data.head()
```
