# Constitución — Riesgo de crédito y macroeconomía

Principios innegociables. Toda spec, plan y tarea debe cumplirlos.

1. **Reproducible de punta a punta**: `uv run python -m src.pipeline all` reproduce datos, modelos, figuras y variables del informe desde un clon limpio. Versiones fijadas en `uv.lock`; las descargas de FRED se guardan con fecha y no se editan.
2. **La spec manda y se pre-registra**: nada se estima si no está en la spec aprobada. Variables, transformaciones, rezagos, signos esperados y reglas de decisión se fijan antes de ver resultados; todo cambio posterior pasa por `/sdd-change` y se reporta en el informe.
3. **Lógica separada de presentación**: los cálculos son funciones puras en `src/` (reciben datos y parámetros; sin red, disco ni gráficos). El informe y las diapositivas solo leen `outputs/`.
4. **Tests como puerta**: pytest sin red; los estimadores se prueban con datos simulados de parámetros conocidos. Prohibido avanzar con tests en rojo.
5. **Cero cifras o citas inventadas**: todo número del informe viene de `outputs/` por código y toda referencia tiene DOI o URL verificada. Los resultados se describen como asociación, salvo que el diseño identifique causalidad.
6. **Idioma**: código en inglés; specs, informe y diapositivas en español, con citas APA 7.
