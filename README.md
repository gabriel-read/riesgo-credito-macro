# Riesgo de crédito y macroeconomía — repositorio agéntico (SDD)

Investigación individual (INTEC): ¿en qué medida el ciclo macroeconómico y la política monetaria de EE. UU. se asocian con la morosidad bancaria, y cómo usarlo para gestionar el riesgo de crédito? Entrega: jueves 15 de octubre de 2026.

## Cómo está armado

| Pieza | La usa | Dónde |
|---|---|---|
| Reglas del proyecto | todos los agentes (Claude Code lo importa desde `CLAUDE.md`) | `AGENTS.md` |
| Memoria entre sesiones y entre arneses | todos | `MEMORY.md` |
| Principios innegociables | todos | `docs/constitution.md` |
| Requisitos oficiales del profesor | todos | `docs/guia-profesor.md` |
| Skills: sdd, econometria-series-tiempo, datos-fred, citas-apa, informe-quarto | Claude Code y OpenCode | `.claude/skills/` |
| Arquitecto y auditor: comandos y subagentes | Claude Code | `.claude/commands/`, `.claude/agents/` |
| Fábrica: coordinador, subagentes y comandos | OpenCode | `.opencode/agents/`, `.opencode/commands/` |
| Specs, planes, tareas y revisiones | todos | `specs/NNN-nombre/` |
| Guardarraíles del arnés | pytest y GitHub Actions | `tests/test_harness.py` |

## Puesta en marcha

1. Requisitos: Git, uv, Quarto, OpenCode v2 y Claude Code (con tu sesión de Claude Pro, sin `ANTHROPIC_API_KEY` en el entorno).
   - uv en Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - uv en macOS o Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Quarto: instalador de https://quarto.org/docs/get-started/
2. Descomprime esta carpeta donde trabajes y entra en ella.
3. `git init -b main`, luego `uv sync` (crea `.venv` y `uv.lock`) y `uv run pytest -q`: deben pasar los tests del arnés.
4. `git add -A` y `git commit -m "chore: arnés agéntico SDD"` (incluye `uv.lock`: la integración continua lo necesita).
5. Crea un repositorio privado en GitHub, conéctalo con `git remote add origin <url>` y sube con `git push -u origin main`.
6. Abre Warp con tres pestañas en esta carpeta: `claude`, `opencode` y una terminal libre.
7. En OpenCode: `/models` → LongCat 2.5 Preview Free; Tab hasta el agente `coordinator`.

## Comandos

- **Claude Code**: `/sdd-constitution` · `/sdd-spec` · `/sdd-resolve` · `/sdd-plan` · `/sdd-audit` · `/sdd-change` · `/redactar` · `/evaluar` · `/cierre`
- **OpenCode**: `/sdd-clarify` · `/sdd-tasks` · `/fabrica` · `/sdd-implement` · `/sdd-validate` · `/sdd-status` · `/lit-buscar` · `/feature` · `/cierre`

El orden de uso, con el texto exacto de cada prompt por spec, está en el playbook del proyecto.
