# MEMORY.md — Riesgo de crédito y macroeconomía
Memoria del proyecto entre sesiones y entre arneses (Claude Code y OpenCode). Máximo ~50 líneas: resume o elimina lo que ya no aporte.

## Estado actual
- Fase 0: arnés instalado (AGENTS.md, constitución, skills, agentes, comandos, CI). Sin código ni datos todavía.
- Próxima spec: 001-datos (`/sdd-spec` en Claude Code).

## Calendario (entregar el jueves 15-oct antes de las 22:00; cierre oficial 16-oct 00:00)
- 001 datos 3–4 oct · 002 literatura 4–6 oct · 003 modelo I 5–8 oct · 004 modelo II 8–10 oct
- 005 estrés 10–11 oct · 006 informe 11–14 oct · 007 diapositivas 13–14 oct · evaluación y ensayo 14–15 oct

## Decisiones (y por qué)
- Frecuencia trimestral: la dependiente (DRALACBS) es trimestral; las mensuales se promedian por trimestre.
- Muestra 2000T1 al último trimestre publicado (2026T2); se descarga desde 1998 para calcular variaciones interanuales sin perder 2000.
- Reparto de arneses: Claude Code redacta constitución, specs y planes, y audita; OpenCode (LongCat 2.5 Preview, high) hace tareas, implementación y validación técnica.
- Specs críticas (auditoría de Claude obligatoria): 003, 004, 005 y 006.
- Estrés sobre las fechas de la Fed 2026 (base y severamente adverso) más un escenario propio estanflacionario con alza de tasas.

## Decisiones pendientes
- PIB real (GDPC1) como principal y nominal (GDP, el de la guía) como robustez, o al revés.
- ¿El profesor acepta extender la muestra a 1985 como robustez?
- Formato exigido del informe (Word o PDF) y de la exposición.

## Aprendizajes y errores a evitar
- Octubre 2025 no existe en CPI ni en desempleo (cierre del gobierno de EE. UU.): 2025T4 se promedia con dos meses y se documenta.
- pandas-datareader < 0.11 falla con pandas 3; respaldo: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIE>`.

## Próximos pasos
- Claude Code: `/sdd-spec 001-datos ...` (texto completo en el playbook).
