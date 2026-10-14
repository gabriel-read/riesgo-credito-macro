VEREDICTO: CAMBIOS NECESARIOS

Auditoría independiente de implementación de la spec 005 (Estrés), **ronda 1**, 12-oct-2026. Autor: subagente `revisor-econometrico` de Claude Code, contexto limpio, con solo rutas y criterios (`docs/paquete-auditoria-005-2026-10-12.md`); no leyó `review-validate.md`, `docs/relevo-*` ni `.env`, y no modificó el repositorio. Claude Code solo registra el informe tal cual lo entregó; no lo ha editado ni lo sustituye con juicio propio. No hay rondas anteriores de auditoría de implementación. Spec y plan auditados: sha256 `6d9713dd…` y `8b0fc56b…` (coinciden con los aprobados). Nada de esto aprueba ni cierra la 005: con este veredicto la spec no puede cerrarse hasta una ronda 2 tras las correcciones de Codex (sin tocar spec ni plan aprobados).

Resumen: las cifras se sostienen (recálculo independiente idéntico), 823 tests pasan y la etapa `stress` es reproducible byte a byte. Los bloqueantes son de contrato (claves, advertencias, definición de una cifra, Markdown, tests faltantes).

---

## Qué comprobó y cómo

- **Contratos intactos.** Las huellas sha256 de `specs/005-estres/spec.md` (6d9713dd…) y `plan.md` (8b0fc56b…) coinciden con las aprobadas. El orden de commits cumple RNF-1: `5ba4ada` contiene solo `.gitattributes` y los cuatro archivos de la Fed; `7a3dd2a` contiene solo `specs/005-estres/`. Las salidas son de las 01:48 y el pre-registro de las 00:03.
- **Fuentes.** Los tres CSV de la Fed coinciden con las huellas del plan, en el árbol de trabajo y en `git show HEAD:`; reglas `-text` activas. El vintage FRED 2026-10-02 (GDPC1, CPIAUCSL, LOANS) coincide con sus huellas tras normalizar a LF. Cobertura y metadatos del manifiesto correctos.
- **Tests.** `uv run pytest -q`: 823 passed, 503 warnings, 706 s; no alteró ningún archivo (hashes antes y después).
- **Reproducibilidad (RNF-7).** Hashes de 102 archivos (`outputs/`, `data/`, `report/_variables.yml`); `uv run python -m src.pipeline stress`; todo idéntico byte a byte. El diff de `_variables.yml` contra HEAD solo añade el bloque `estres:`. No corrió `all`.
- **JSON de los modelos.** Bloques de covarianza HAC sin dummies: 7 términos (Modelo I) y 8 (Modelo II), simétricos y definidos positivos (valor propio mínimo ≈ 7,0e-7). Lectura de la 004 «sin evidencia», K = 1 por BIC, `sample_end` 2026T2 en ambos.
- **Recálculo independiente** (`scratchpad/indep/recompute.py`, sin importar `src/`): PIB y CPI trimestrales desde datos crudos (CPI 2025T4 = promedio nov–dic), identidades logarítmicas, enlace Fed 2025 Q4, escenario D, crédito, recursión propia, `default_rng(20261011)`, N = 10 000, Cholesky. Interanuales coinciden con `panel.csv` (≤ 9e-14). Todas las cifras coinciden:

| Cifra | Modelo I | Modelo II |
|---|---|---|
| Δ final 2029T3 (p05 / p95) | 1,428 (−0,188 / 2,288) | 0,827 (−0,479 / 1,721) |
| Pico de Δ y trimestre | 1,898 en 2028T3 | 1,286 en 2028T3 |
| Proporción Δ > 0 (final / pico) | 0,935 / 0,951 | 0,877 / 0,934 |
| Nivel base final / adverso final / pico adverso | 1,989 / 3,417 / 3,716 | 1,845 / 2,672 / 3,052 |
| D frente al adverso con tasa en 0 | máx. diferencia 0,0 | máx. diferencia 0,0 |
| Contribución de la tasa C, adverso (final, p05, p95, pico, proporciones) | 0,341, −0,206, 0,746, 0,346, 0,864 / 0,864 | 0,464, −0,139, 1,133, 0,466, 0,905 / 0,907 |
| C en D, final | −0,681 | −0,922 |
| RF-12a (Δ 2029T1 tramo posterior / principal / pico) | 0,340 / 1,736 / 0,843 | 0,048 / 1,118 / 0,549 |
| RF-12c: máx. diferencia de Δ por paso k; Δ en k = 13 | 0,0; 1,428 | 0,0; 0,827 |
| Crédito en 0 y en la media (niveles) | iguales a `sens_cred` | iguales a `sens_cred` |
| Réplicas explosivas / fuera de rango (mín., máx.) | 1 / 105 (−10,32; 6,50) | 1 / 160 (−6,12; 9,92) |

- **RF-5 con datos reales.** El test usa datos sintéticos; corrió además `out_of_sample` con el panel real en solo lectura: el adaptador reproduce la columna `dinamico` con diferencia máxima 0,0.
- **Lenguaje.** Sin «causa», «causal», «provoca» ni «debido a» en `stress_*.{csv,md}` ni en `_variables.yml`.
- **Figuras.** `stress_model1.png` y `stress_model2.png`: dos paneles, pp, español, nota de bandas de parámetros, advertencia de fuera de rango y fuente exigida.

## Hallazgos bloqueantes

1. **Seis claves de `estres.*` no tienen el nombre fijado en el plan** — `src/stress.py:379-384` y `report/_variables.yml` (bloques `estres.modelo{1,2}.{severo,propio}`).
   - **Contrato:** RF-15 y plan §5: `delta_{final,final_p05,final_p95,pico,pico_trimestre,min,sin_aumento,prop_pos_final,prop_pos_pico}`.
   - **Problema:** se escribieron `final_p05`, `final_p95`, `min`, `sin_aumento`, `prop_pos_final` y `prop_pos_pico`, sin el prefijo `delta_`. Ningún test comprueba el conjunto completo de claves, aunque el «Hecho cuando» de T8 lo exige. La spec 006 usará los nombres del plan.
   - **Esperado:** `delta_final_p05`, `delta_final_p95`, `delta_min`, `delta_sin_aumento`, `delta_prop_pos_final`, `delta_prop_pos_pico`, más un test que compare el árbol de `estres` con el plan §5.

2. **Faltan la advertencia de niveles fuera de rango en el pie de las tablas y el mínimo/máximo en la tabla de niveles** — `src/stress_tables.py:13-18,70-79` y `src/stress.py:373-376`.
   - **Contrato:** spec, «Resumen de las réplicas» (advertencia en el pie de las tablas y la figura; mínimo y máximo alcanzados) y RF-8.
   - **Problema:** hay niveles fuera de rango (105 réplicas en el Modelo I y 160 en el II; mínimo −10,32 pp). La figura lo advierte; ninguna nota de tabla lo hace. `stress_levels` no trae mínimo, máximo ni total de réplicas afectadas (solo `_variables.yml`).
   - **Esperado:** el pie de `stress_levels.md` (y de `stress_delta.md`, si se quiere ser estricto) lleva la advertencia cuando `n > 0`; `stress_levels` incluye número y proporción de réplicas afectadas y mínimo y máximo por modelo.

3. **`estres.dif_modelos.{esc}.delta_pico` mide algo distinto de lo que sugiere su nombre** — `src/stress.py:477`.
   - **Contrato:** RF-11 y la definición de «pico del cambio» en la spec.
   - **Problema:** el código toma el máximo en el tiempo de Δ_I − Δ_II (0,626, en 2028T4), trimestre que no es el pico de ningún modelo. La diferencia entre picos, ambos en 2028T3, es 0,612 (1,898 − 1,286).
   - **Esperado:** `delta_pico = Δ_I,pico − Δ_II,pico`; si se prefiere la otra métrica, definirla y rotularla explícitamente.

4. **Tablas Markdown rotas y encabezados en inglés** — `src/stress.py:465` (texto «|ρ| ≥ 1»), `src/tables.py:26` (`to_markdown` no escapa `|`) y `src/stress.py:282-283`.
   - **Contrato:** RF-16 (tabla en Markdown) y RNF-9 (etiquetas en español).
   - **Problema:** en `outputs/tables/stress_limitations.md` las filas de «explosivas» tienen celdas de más; `stress_origin` muestra los encabezados `adapted_quarter` y `original_quarter`.
   - **Esperado:** escapar `\|` en el renderizado de estrés o redactar «ρ en valor absoluto ≥ 1»; encabezados en español («trimestre_adaptado», «trimestre_original»).

5. **Faltan tests que el contrato exige** — `tests/test_stress.py:151-198`; no existe test de lenguaje para el estrés.
   - **Contrato:** RNF-5 (tests negativos para «referencia del paso 1 distinta entre escenarios» y «transformación no lineal», comparando contra la recursión de δ); RNF-6 y plan §8 (test de lenguaje en las salidas de estrés).
   - **Problema:** no hay test negativo con referencias del paso 1 distintas ni con una Y no lineal (logit); los negativos existentes comparan contra `project`, no contra la recursión de δ. `tests/test_language.py` no cubre `stress_*`. Hoy las salidas cumplen RNF-6 (grep), pero nada protege contra una regresión.
   - **Esperado:** añadir los dos negativos que faltan y un test que recorra las ocho tablas `.md`/`.csv` de estrés y el bloque `estres` buscando los términos prohibidos. Ninguno altera salidas.

## Opcionales (no bloquean)

- `prop` de explosivas se muestra «0,000» con n = 1 (`_variables.yml`, `stress_levels.md`): más precisión o porcentaje.
- RF-14: la limitación sobre la tasa de D (`src/stress.py:312`) omite la consecuencia literal «la sensibilidad de RF-10 mezcla las dos medidas».
- En `stress_paths`, las columnas PIB, ΔU, π y CRED del Modelo II muestran valores rezagados (t−1, t−4) sin indicarlo en el encabezado.
- Figuras: la línea roja del adverso queda oculta bajo la de D; una nota «D coincide con el adverso bajo la regla de la tasa» evitaría la confusión.
- El nivel implícito de la tasa se ancla en FEDFUNDS de 2026T2 (el panel no tiene la letra a 3 meses); está rotulado `tasa_proxy_implicita`, conviene decirlo en la nota de la tabla.
- «Regresores no I(0): inflación y crédito» está escrito a mano (`src/stress.py:315`); hoy coincide con `model{1,2}_stationarity`, mejor leerlo de esas tablas.
- `sens_cal.delta_pico` no trae su trimestre ni aplica la regla de «sin aumento».
- El eje de niveles dice «(pp)»; el nivel de DRALACBS es un %, los pp corresponden al cambio.
- El encabezado de `spec.md` y `plan.md` sigue diciendo «borrador v6… sin aprobar». Es deliberado para conservar las huellas; la aprobación consta en `tasks.md`. El informe debe citarla bien.

## Checklist de econometría de series de tiempo

| Punto | Resultado |
|---|---|
| Estacionariedad | Heredada de 003/004; la limitación de regresores no I(0) coincide con sus tablas. |
| Errores HAC | Covarianza HAC exportada, 4 rezagos; se usa el bloque sin dummies. |
| Rezagos | K = 1 por BIC, sin reabrirse. |
| Signos | Regla de la tasa en 0 respetada; sensibilidad aparte y rotulada «sensibilidad, no efecto estimado»; la de D es negativa, como la spec anticipaba con β₄ < 0. |
| Frases causales | Ninguna. |
| Diagnósticos fallidos | Listados en `stress_limitations`. |
| Reproducibilidad | Comprobada byte a byte con la etapa `stress`. |

## Lo que defendería ante el profesor

- Ejercicio pre-registrado y reproducible: fuentes con huella, semilla fija, la misma cifra recalculada por un auditor independiente, y RF-12c confirma que Δ no depende del origen (diferencia 0,0).
- La regla de la tasa en cero es prudencia heredada de la 004, no un hallazgo de efecto nulo; su sensibilidad va aparte, pareada réplica a réplica.
- Bajo el adverso adaptado, la morosidad proyectada sube frente a la base en ambos modelos (Δ final 1,43 y 0,83 pp; picos 1,90 y 1,29 pp en 2028T3). Es una asociación condicional con banda solo de parámetros.

## Lo que preguntaría el profesor

- ¿Por qué el cambio al final cae de 1,74 a 0,34 pp (Modelo I) y de 1,12 a 0,05 pp (Modelo II) al quitar los dos primeros trimestres de la Fed (RF-12a)? ¿Depende el resultado de que el choque empiece de inmediato en 2026T3?
- La banda al 90 % del cambio final cruza cero en ambos modelos (p05 = −0,19 y −0,48), aunque más del 87 % de las réplicas son positivas. ¿Qué se puede afirmar sobre el riesgo de crédito?
- Hay 105 y 160 réplicas con niveles negativos y una con |ρ| ≥ 1. ¿Qué dice eso de la especificación lineal en primera diferencia, con RESET y Chow rechazados, y de usar estos niveles para planificar capital?

## Continuidad

Ronda 2 pendiente: tras las correcciones 1–5 (sin editar spec ni plan aprobados), un revisor de contexto limpio verifica solo esos puntos y las salidas regeneradas; esta ronda se conserva como `review-audit-ronda1.md` antes de reemplazar este archivo.
