# MEMORY.md — Riesgo de crédito y macroeconomía
Memoria del proyecto entre sesiones y entre arneses (Claude Code y OpenCode). Máximo ~50 líneas: resume o elimina lo que ya no aporte.

## Estado actual (5-oct-2026)
- Spec 002-literatura COMPLETADA (5-oct-2026): 10/10 tareas, 187 tests en verde, `verify_refs.py` 21/21 con código 0 y auditoría independiente T10 APROBADA en la ronda 4 (`review-audit.md`, `review-validate.md`; el `APROBADO` previo de la fábrica no valía). Matriz: 17 estudios + 4 datos/método (2.1–2.4 = 2 cada una, 2.5 = 9); asiamah2026 y koskei2023 quedan pendiente-lectura (signo no respaldado por el resumen). Para la spec 006: justificar bernanke1995 en 2.1 y la clasificación de pesaran2006, segoviano2006 y gertler2015.
- Spec 003-modelo-i (5-oct-2026): T1–T9 y correcciones de las rondas 1 y 2 de auditoría commiteadas (487 tests; `all` ×2 idéntico, 30 archivos; `review-validate.md` APROBADO, escrito por Claude Code por cuota agotada de OpenCode). Ronda 2 resuelta: nota de tamaño del Chow 2020T2 (21 trimestres útiles por código), enmienda del plan (§13), AGENTS.md a Python 3.11. Falta la ronda 3 de auditoría independiente; si APROBADO → spec «implementada».
- Para la 005/006 (del audit): ΔFFR tiene signo negativo, así que un escenario con alzas de tasa baja la morosidad proyectada: decidir y pre-registrar el tratamiento ANTES de la 005. El dinámico pierde frente al ingenuo. Los únicos p < 0,05 (π y CRED) son los regresores no I(0).
- Hallazgos 003 (datos reales): ρ = 0,63; con p < 0,05 solo π (+) y CRED(t−4) (+); PIB (−) y ΔU (+) con el signo esperado pero sin significancia; ΔFFR con signo contrario (−), sin significancia. BG pasa y CUSUM pasa; BP, White, JB, RESET y los dos Chow fallan. VIF de ΔU = 36,8 es artefacto de la dummy de 2020T2 (3,1 sin ellas). Fuera de muestra: a un paso no se distingue del ingenuo (DM p = 0,94); el dinámico pierde frente al ingenuo constante.
- Preguntas del profesor (ensayo): (1) ¿por qué creer los p-valores de inflación y crédito si no son I(0)? (2) ΔU se identifica con décimas de pp por trimestre y ΔFFR sale negativa: ¿cómo justifica usarlo en un estrés de varios pp de desempleo y alzas de tasa? (3) Con Chow (2008 y 2020) y RESET rechazando, ¿qué sobrevive?
- Migración (4-oct-2026): de Warp a Orca como harness; OpenRouter se intentó y se descartó (clave daba 401 y crear otra pedía billing). OpenCode sigue con OpenCode Zen: planner/coordinator nemotron-3-ultra-free; implementer longcat-2.5-preview-free; reviewer big-pickle; bibliotecario space-bunny-free (elección sin probar). Mientras OpenCode no funcione, Claude Code avanza la spec 002. Copia oficial: `~/orca/riesgo-credito-macro`, rama `spec/002-literatura`, commit `a39311e` sin push (la copia de Desktop/OneDrive queda como respaldo). Pendiente: `/connect` a Zen y probarlo (daba "User not found").
- Constitución revisada el 2-oct (sin cambios, seis principios). Fase 0 (`ca8e4cc`), specs 001-datos y 002-literatura cerradas; detalle en `specs/001-*` y `specs/002-*`. D1 del plan 001: solo `data --download` usa la red.

## Calendario (entregar el jueves 15-oct antes de las 22:00; cierre oficial 16-oct 00:00)
- 001 datos 3–4 oct · 002 literatura 4–6 oct · 003 modelo I 5–8 oct · 004 modelo II 8–10 oct
- 005 estrés 10–11 oct · 006 informe 11–14 oct · 007 diapositivas 13–14 oct · evaluación y ensayo 14–15 oct

## Decisiones (y por qué)
- Frecuencia trimestral: la dependiente (DRALACBS) es trimestral; las mensuales se promedian por trimestre.
- Muestra principal 2000T1–2026T2 (106 trimestres); se descarga desde 1998 para calcular variaciones interanuales sin perder 2000. Robustez de muestra larga 1985T1–2026T2, pre-registrada en las specs 003–005. Desviación frente a la guía (que corta en 2026-01-01): declararla en el informe. (Resuelto el 5-oct-2026.)
- PIB: GDPC1 (real) es el regresor principal, para evitar doble contabilidad con la inflación; GDP (nominal, el de la guía) se pre-registra como robustez. (Resuelto el 5-oct-2026.)
- Informe: PDF generado con Quarto en APA 7 (`apa.csl`, números desde `report/_variables.yml`). (Resuelto el 5-oct-2026.)
- Reparto de arneses: Claude Code redacta constitución, specs y planes, y audita; OpenCode (LongCat 2.5 Preview, high) hace tareas, implementación y validación técnica.
- Specs críticas (auditoría de Claude obligatoria): 003, 004, 005 y 006.
- Estrés sobre las fechas de la Fed 2026 (base y severamente adverso) más un escenario propio estanflacionario con alza de tasas.

## Decisiones pendientes
- Formato exigido de la exposición (diapositivas).
- Confirmar con el profesor que la muestra larga 1985T1 como robustez y el PDF son aceptables.

## Aprendizajes y errores a evitar
- No fiarse del `APROBADO` de la fábrica sin auditoría independiente: en la 002 marcó T4 y T10 como hechas con tests en rojo o sin auditar. Validar (OpenCode) y auditar (`verificador-citas` con solo rutas) son cosas distintas.
- Un estudio que estima coeficientes macro sobre morosidad es sección 2.5 aunque encaje conceptualmente en 2.2; no reasignar para cuadrar mínimos.
- FRED cuelga las peticiones con User-Agent propio: usar el predeterminado.
- OpenCode usa `permission` (singular, objeto; gana la última regla coincidente), no `permissions` como lista: con la lista las protecciones se ignoraban. Ya corregido en `opencode.jsonc` y los 5 agentes; verificar con una prueba real (`git push` y leer `.env` deben rechazarse).
- Los modelos gratuitos tienen cuota limitada: al agotarse, seguir con Claude Code.
- Octubre 2025 no existe en CPI ni en desempleo (cierre del gobierno de EE. UU.): 2025T4 se promedia con dos meses y se documenta.
- pandas-datareader < 0.11 falla con pandas 3; respaldo: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIE>`.
- FRED revisa el PIB: volver a descargar puede cambiar resultados. Congelar `data/raw/` con fecha y no volver a bajarlo.
- `test_report_has_no_hand_typed_decimals` (tests/test_harness.py:93) solo detecta números con 2+ decimales: "0,8 pp" o "15 %" a mano pasan. Endurecerlo en la spec 001.
- El pre-registro se demuestra con git: aprobar y commitear cada spec de modelo antes de la primera estimación.

## Próximos pasos
1. Spec 003 (Modelo I) RESUELTA y marcada aprobada (5-oct-2026, 23 RF; 69 hallazgos de `review-clarify.md` aplicados). Decisiones:
   - Sin `/sdd-change 001`. R6 y R7 se truncan a la historia disponible (con la descarga de 1998 empiezan en 2001T1 y 2002T1); R8 queda «no estimada» si no hay historia anterior a 2000.
   - La regla ADF/KPSS solo decide la forma de la dependiente (hoy todas en Δ); los regresores tienen forma fija y su no estacionariedad se declara como limitación.
   - El largo plazo solo se reporta si 1 − ρ > 0,05.
   - Si la matriz HAC no es definida positiva, truncamiento espectral.
   - Chow como Wald HAC con interacciones.
   - RF-4 se detiene si cambia la tabla de estacionariedad.
   - Robusto = mismo signo y p < 0,10.
   - Variables bajo el prefijo `modelo1.`.

   Commit del pre-registro: `667b313`. Plan aprobado el 5-oct-2026, tras la auditoría de `revisor-econometrico`: 10 cambios necesarios incorporados (`review-plan.md`, respuesta en la sección 12 del plan). Cambios a la spec C1–C3 (`/sdd-change`, antes de estimar, registrados en «Desviaciones del pre-registro»):
   - C1: la DE de los efectos «por 1 DE» excluye 2020T2–2021T1.
   - C2: los efectos base de 2021T2–2022T1 son limitación fija, con R1 como contraste.
   - C3: la positividad de la matriz HAC se comprueba solo en el sub-bloque sin dummies de impulso.

   Siguiente: `/sdd-tasks 003-modelo-i` y `/fabrica` en OpenCode. La tarea 9 es la primera estimación real.
   - Lección: las dummies de impulso (valen 1 en un solo trimestre) dejan residuos nulos. Eso rompe el CUSUM de statsmodels, deja la matriz HAC con rango reducido y mete columnas colineales en White. Además, `use_correction` de HAC es `False` por defecto en statsmodels 0.15.
2. Si `uv run` falla con "os error 998" en el `.venv`: `uv sync` lo recrea (pasó el 2-oct).
