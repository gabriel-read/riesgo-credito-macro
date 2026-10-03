---
name: informe-quarto
description: Úsala siempre que redactes, edites, revises o renderices el informe o las diapositivas (report/, specs 006 y 007, comando /redactar o /evaluar).
---

# Informe y diapositivas con Quarto

## Estructura obligatoria
Sigue `docs/guia-profesor.md` sección por sección (1 a 11), con los mismos títulos y numeración. Cada sección empieza con su respuesta en una frase.

## Proyecto de Quarto
- `report/` es un proyecto de Quarto: necesita `report/_quarto.yml`; sin él, `{{< var >}}` no se resuelve.
- La primera tarea de la spec 006 es un render de humo con una variable, una tabla incluida, una figura y una cita, para validar rutas antes de escribir nada más.

## Números sin teclear
- Todo número del texto viene de `report/_variables.yml`, generado por el pipeline, y se escribe con el shortcode `{{< var modelo1.beta_unrate >}}`. Nunca escribas una cifra a mano.
- Tablas: archivos `outputs/tables/*.md` generados por código e incluidos con `{{< include ../outputs/tables/<nombre>.md >}}`.
- Figuras: `outputs/figures/*.png` con pie y fuente ("Fuente: FRED; elaboración propia").
- Si falta una variable, pide que el pipeline la genere; no la inventes.

## Redacción
- Español formal, frases de menos de 25 palabras, voz activa.
- Interpreta en unidades ("un pp más de desempleo se asocia con X pp más de morosidad"), no solo en significancia.
- Lenguaje de asociación y límites declarados (skill econometria-series-tiempo).
- Si hubo desviaciones del pre-registro, se reportan en la sección 3.5.
- Conclusión: responde la pregunta de investigación y dice cómo usar el resultado para anticipar y gestionar el riesgo. Prohibido el formato "el PIB fue significativo y el desempleo también".
- Sección 8: cubre los siete puntos de la guía (alertas tempranas, monitoreo macro, políticas de crédito, escenarios de estrés, planificación de capital, gestión de cartera, concentración y calidad crediticia).

## Citas
Solo claves de `report/references.bib` (skill citas-apa), APA 7 con `csl: apa.csl`.

## Diapositivas (`report/slides.qmd`)
Máximo 12 láminas · una idea por lámina, con título-conclusión (el hallazgo, no el tema) · gráficos antes que tablas · mismas variables y figuras que el informe.

## Renderizado
`quarto render report/informe.qmd` y `quarto render report/slides.qmd` (formatos según `MEMORY.md`). Revisa que en la salida no queden `?@`, `{{<` ni referencias sin resolver.

## Checklist
- [ ] ¿Están las 11 secciones de la guía, en orden?
- [ ] ¿Algún número escrito a mano?
- [ ] ¿Alguna cita fuera de references.bib?
- [ ] ¿La conclusión responde la pregunta y dice cómo anticipar el riesgo?
- [ ] ¿Las 7 implicaciones de la sección 8 están cubiertas?

## Al terminar
Indica qué puntos del checklist comprobaste y cómo.
