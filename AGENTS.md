# AGENTS.md — Riesgo de crédito y macroeconomía (INTEC)
Investigación individual: cómo el ciclo macro y la política monetaria de EE. UU. se asocian con la morosidad bancaria (FRED: DRALACBS), con dos modelos econométricos y una prueba de estrés. Entrega: informe APA + diapositivas, jueves 15-oct-2026.

## Stack y estructura
- Python 3.12 + uv · pandas, statsmodels, pandas-datareader ≥0.11, matplotlib · pytest · Quarto.
- `src/` lógica en funciones puras · `tests/` · `data/raw/` descargas de FRED con fecha (solo lectura) · `outputs/` tablas y figuras generadas.
- `specs/NNN-nombre/` spec, plan, tasks y review-*.md · `research/` matriz de literatura · `report/` informe, diapositivas y references.bib.
- `docs/guia-profesor.md` requisitos oficiales · `docs/constitution.md` principios innegociables.

## Comandos
- Instalar: `uv sync` · Tests: `uv run pytest -q`
- Pipeline (existe desde la spec 001): `uv run python -m src.pipeline data|models|stress|report|all`
- Informe y diapositivas: `quarto render report/informe.qmd` · `quarto render report/slides.qmd`

## Convenciones
- Código e identificadores en inglés; specs, informe y diapositivas en español; citas APA 7.
- Frecuencia trimestral; FRED fecha cada trimestre en su primer día (`2026-04-01` = 2026T2).

## Reglas de dominio (fácil equivocarse)
- Ningún número del informe se escribe a mano: sale de `outputs/` o `report/_variables.yml` (skill informe-quarto).
- Ninguna cita sin DOI o URL verificada (skill citas-apa).
- Estacionariedad, errores HAC y lenguaje de asociación, nunca causal (skill econometria-series-tiempo).
- Octubre 2025 falta en CPI y desempleo: nunca imputes ni rellenes en silencio (skill datos-fred).

## Forma de trabajar (SDD)
- Antes de tocar nada lee `docs/constitution.md`, `MEMORY.md` y la spec activa; usa la skill sdd.
- Una tarea por vez, tests primero, cambios pequeños. No añadas lo que la spec no pide.
- Al terminar, resume qué cambió y qué decisión debo revisar.

## Límites
- ✅ Siempre: `uv run pytest -q` antes de dar algo por hecho; actualizar `MEMORY.md` al cerrar cada spec o sesión.
- ⚠️ Pregunta antes: dependencias nuevas, borrar archivos, `git push`, cambiar `docs/constitution.md`, una spec o un plan aprobados.
- 🚫 Nunca: editar `data/raw/` o `docs/guia-profesor.md`; inventar datos, cifras o citas; cambiar una spec aprobada sin `/sdd-change`.

## Memoria
- Al empezar lee `MEMORY.md`; al terminar actualízalo: estado, decisiones con su porqué, errores a evitar. Máx. ~50 líneas.
- Si algo se vuelve regla permanente, propón moverlo aquí. Nunca guardes claves ni datos personales.

## Verificación
- `uv run pytest -q` en verde + `VEREDICTO: APROBADO` en `specs/NNN-*/review-validate.md`; las specs críticas, además en `review-audit.md`.
