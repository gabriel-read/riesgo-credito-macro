# Congelación de fuentes Fed y contraste técnico de 005

Codex, descarga propia autorizada el 11-oct-2026 (America/Santo_Domingo; 12-oct en UTC). HEAD `2f4c401`. No implementación ni proyección. Las huellas se calcularon desde los bytes descargados y se recalcularon después; no se copiaron de ninguna revisión.

## Archivos y evidencia de descarga

Directorio: `data/scenarios/fed/2026-final/2026-10-11/`. CSV originales guardados por descarga binaria, sin parsear/escribir de nuevo ni normalizar CRLF. Manifiesto en el mismo directorio, con URL individual, fecha local, hora UTC, SHA-256, tamaño, escenario, versión, cobertura, campos requeridos y referencia de unidades.

| Archivo | Bytes | SHA-256 recalculado |
|---|---:|---|
| `2026_Final_Historic_Domestic.csv` | 16936 | `6d08aadcf82d65dcf36b856792040b82ceceef79a46ff0239afd41e0c4e7f653` |
| `2026_Final_Supervisory_Baseline_Domestic.csv` | 1692 | `76e236695be2c8372890078acf8c01273ba5198a19afb5037045a963737c1bcc` |
| `2026_Final_Supervisory_Severely_Adverse_Domestic.csv` | 1824 | `45c2859ae7246c071b69df8623854751f0629b04393957e14fe28bc33c04ebbb` |

URLs individuales registradas en `manifest.csv`. Publicación oficial: [DFAST 2026](https://www.federalreserve.gov/supervisionreg/dfa-stress-tests-2026.htm). Unidades contrastadas con las [notas oficiales de variables](https://www.federalreserve.gov/publications/2026-stress-test-scenarios.htm): PIB/CPI trimestrales anualizados; desempleo promedio trimestral; tasa de Treasury a tres meses promedio trimestral, base de descuento. El CSV no contiene unidades; el manifiesto registra su fuente documental, no las presenta como campos del CSV.

Comprobaciones realizadas:
- Histórico: 200 filas, escenario `Actual`, 1976 Q1–2025 Q4; una fila 2025 Q4 (desempleo 4.5 y Treasury 3.7).
- Base y adverso: 13 filas cada uno, 2026 Q1–2029 Q1, nombres `Supervisory Baseline` y `Supervisory Severely Adverse`.
- Cabeceras exactas presentes: `Real GDP growth`, `CPI inflation rate`, `Unemployment rate`, `3-month Treasury rate`; sin valores vacíos en esas columnas de los escenarios; tasas de composición mayores que −100.
- CRLF: 201 líneas terminadas en histórico y 14 en cada escenario. Huellas finales: 3/3 coinciden con el manifiesto.
- `.gitattributes`: tres reglas de ruta exacta `-text`, exclusivamente para estos CSV. `git check-attr text` = unset para cada uno; no alcanza `data/raw/` ni el manifiesto. `git hash-object --no-filters` coincide con `git hash-object --path=<ruta>` para los tres: el filtro Git no modifica bytes. Esta comprobación no hace staging ni commit; la verificación en clon será posterior al commit autorizado.

## Contraste con v3 consolidada

Lectura final de `specs/005-estres/spec.md` y `plan.md` después de la incorporación de decisiones. Huellas documentales al consultar: spec `da2c4014121d7b3104efff4b1b995c4857cf606d89550306328c19620ddc3682`; plan `c359360a2d7068225de5ac70cb675642fb1369d791634875288b90379c7d0e4e`. Son trazabilidad de borradores, no pre-registro ni aprobación.

| Tema | Estado técnico |
|---|---|
| Lectores, etiquetas y origen | Plan diferencia ambos mapas JSON y normaliza T/Q; origen 2026T2 desde ambos JSON y panel. Datos Fed requieren también parsear `AAAA Qn`. No cambiar JSON aprobados. |
| Cobertura principal | Resuelta en spec: 13 filas reales se adaptan a 2026T3–2029T3; origen Fed 2025 Q4 disponible. Incluye núcleo inicial del adverso. |
| Transformaciones | Resueltas documentalmente: composición trimestral exacta, `panel.yoy` logarítmica, niveles recuperados con funciones existentes y tratamiento CPI 2025T4 de dos meses. La descarga no construye regresores ni proyecta. |
| D | Resuelto como adverso con cambios de tasa observados 2022T1–2023T3 (7 pasos) y cero después hasta paso 13. Comprobado por lectura de `panel.csv`: siete valores no negativos; 2023T4 también positivo y expresamente excluido. Su coincidencia con severo bajo tasa en cero está declarada. No se valida aquí la justificación externa del corte del ciclo. |
| Crédito | Resuelto: cuatro trimestres cubiertos por historia con rezago 4; nueve con supuesto constante desde 2027T3. Sensibilidades sobre niveles, no Δ. |
| Fixture fuera de muestra | Resuelto en plan §2: `out_of_sample` predefinido 2000T1–2019T4, ancla 2021T4, comparación `result.series.dinamico` y tasa libre. Reproducir este ajuste es ejecutar el contrato previo, sin nueva selección; no se ejecutó en esta sesión. |
| Simulación | Marginal con pareo, tasa apagada después de extraer; retiro de la sensibilidad acumulada indefinida y de condicionamiento. No se simula todavía. |

La nota `docs/fuentes-y-adaptadores-005-2026-10-11.md` conserva el análisis del borrador anterior; este contraste la actualiza y sustituye sus bloqueos ya resueltos, manteniendo sus procedimientos de fuentes/fixture.

## Contraste actualizado con v5 y lista única de pendientes actuales

Esta sección sustituye las listas de bloqueos de las notas técnicas anteriores. No modifica el historial de revisiones ni sus veredictos.

Confirmaciones específicas:
- Vintage FRED: plan §2 usa load_latest_raw con comprobación explícita de la descarga 2026-10-02. El manifiesto real identifica GDPC1_2026-10-02.csv y CPIAUCSL_2026-10-02.csv. Lectura solo desde congelados, sin stage_data ni nueva descarga. Bloqueo anterior retirado.
- RF-12c completa: spec fija origen 2025T4, anclas DR/ΔDR observadas, 13 trimestres 2026T1–2029T1, base y severo en ambos modelos, referencia Fed 2025Q4 para cambios, crédito observado hasta 2027T2 y supuesto desde 2027T3, comparación por paso k y niveles contrafactuales de 2026T1–T2. Plan añade origin_comparison, stress_origin, claves sens_origen y cobertura RF→función. Es distinta de RF-12a (recorte de 11 trimestres). No se ejecuta ninguna de esas proyecciones. Bloqueo anterior retirado; implementar conforme a la definición completa de RF-12c, no solo al comentario de adapt_calendar(False).
- Crédito por escenario: plan §5 usa estres.sens_cred.{m}.{esc}.{cero,media}.{nivel_final,nivel_pico,nivel_pico_trimestre}, esc=base/severo. Sin colisión entre escenarios. Bloqueo anterior retirado.
- SHA-256: recálculo propio en esta comprobación: 3/3 archivos coinciden simultáneamente con manifest.csv y las huellas completas de plan §2. Las reglas .gitattributes siguen siendo exactamente tres y no se modificaron. Sin nuevas descargas ni transformación de CSV.
- Cobertura principal, transformaciones, D de siete cambios más seis ceros y fixture OOS predefinido siguen resueltos como documentó el contraste de descarga. La comprobación temporal de hashes v3 más arriba es antecedente; esta conclusión corresponde a v5 leída hoy.

Pendientes actuales, única lista:
1. Claude debe ajustar plan §2 a las tres rutas exactas autorizadas de .gitattributes y retirar la instrucción de sustituirlas por data/scenarios/** -text. La nota final de review-plan.md también conserva esa propuesta: aclarar su disposición sin alterar el texto original ni autoría de la revisión independiente. No ampliar la regla real.
2. Claude debe documentar la verificación externa del corte de D contra los comunicados FOMC, aún [VERIFICAR] en spec. El panel ya acredita los siete cambios no negativos y el incremento posterior expresamente excluido; ese hecho no sustituye la justificación documental del corte.
3. La v5 aún no tiene revisión independiente posterior: review-plan.md es ronda 3 sobre v4, CAMBIOS NECESARIOS, con nota de incorporación en v5. Claude conserva esa responsabilidad; la comprobación técnica de Codex no emite aprobación independiente.
4. Aprobación explícita de spec y plan y autorización de los dos commits separados (fuentes primero, pre-registro después). Después, tareas bajo SDD antes de implementar; tasks.md todavía no existe. No hacer staging, commit, push ni estimación con la autorización actual.

Solo cambió documentación: no se repite la suite. Evidencia vigente: 774 passed, 355 warnings, 269.96 s, rc 0 de la congelación. La comparación de huellas solicitada es una comprobación específica de archivos, no otra ejecución del pipeline.

## Futuro commit de fuentes: lista exacta, sin arnés

Solo estos cinco archivos (no se hizo staging ni commit):

```text
.gitattributes
data/scenarios/fed/2026-final/2026-10-11/2026_Final_Historic_Domestic.csv
data/scenarios/fed/2026-final/2026-10-11/2026_Final_Supervisory_Baseline_Domestic.csv
data/scenarios/fed/2026-final/2026-10-11/2026_Final_Supervisory_Severely_Adverse_Domestic.csv
data/scenarios/fed/2026-final/2026-10-11/manifest.csv
```

Quedan fuera todos los cambios del arnés, MEMORY.md, documentos de relevo/compatibilidad y specs/revisiones. El pre-registro de 005 sería otro commit posterior, solo con sus archivos aprobados, y requiere autorización. Esta sesión solo añade las fuentes, regla limitada y documentación; `data/raw/`, aplicación y salidas anteriores quedan intactos.

Pruebas de cierre: uv run pytest -q = 774 passed, 355 warnings, 269.96 s, código 0. Verificaciones específicas de fuentes: tres SHA-256 finales iguales al manifiesto y tres objetos Git filtrados iguales a los objetos sin filtros. No se ejecutó la etapa stress.

## Futuro commit de pre-registro: propuesta separada

Archivos existentes propuestos para preservar contrato y trazabilidad de las revisiones de 005 (después de resolver pendientes y aprobar, no ahora):

```text
specs/005-estres/spec.md
specs/005-estres/plan.md
specs/005-estres/review-plan.md
specs/005-estres/review-plan-ronda1.md
specs/005-estres/review-plan-ronda2.md
```

Si Claude añade otra ronda o artefacto de aprobación, actualizar esta lista con su ruta exacta antes de autorizar el commit. No incluir tasks.md inexistente ni asumir aprobación actual. El commit de fuentes conserva exactamente los cinco archivos del bloque anterior. Ambos excluyen .claude/, .agents/, .codex/, AGENTS.md, CLAUDE.md, README.md, playbook, MEMORY.md, docs/, debug.log y cualquier archivo de specs 001–004. No se selecciona el directorio entero con un glob.
