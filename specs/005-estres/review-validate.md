VEREDICTO: APROBADO

Validación técnica del autor, **Codex**, ronda 3, 12-oct-2026. No es auditoría independiente. **T10 y 005 siguen abiertas**, pendientes de auditoría ronda 3 de Claude. La validación y auditoría de ronda 2 se conservan por bytes en `review-validate-ronda2.md` y `review-audit-ronda2.md`; el veredicto independiente actual continúa CAMBIOS NECESARIOS hasta que Claude lo sustituya.

## Corrección autorizada y test primero

Único bloqueante de ronda 2: proporción, mínimo y máximo del pie se convierten a `float` antes de `fmt_es`, como ya hacían las celdas y `stress_variables`. Se mantiene el formateador compartido, su precisión de tres decimales y la cantidad exacta 105/10000 = 0,0105. No se cambió método, spec, plan, dependencias ni ninguna observación opcional de rondas 1/2.

- Test nuevo: `tests/test_stress_outputs.py::test_halfway_rounding_matches_cells_variables_and_both_footnotes`. Usa `np.float64(0.0105)` y exige 0,011 en variable, celda y pie de ambas tablas; mínimo y máximo también coinciden; CSV mantiene precisión completa.
- Primero falló: la variable/celda mostraban 0,011 y el pie 0,010. Después de las tres conversiones, los **7 tests de presentación pasan**, 9,10 s.
- El test anterior usaba 0,25 y no exponía este caso de mitad. El defecto era de presentación y tipos: el redondeo de np.float64 difería del de float Python.
- Reconstruir el archivo anterior quitando solo esas tres conversiones produce su SHA-256 anterior exacto. No hay otro cambio en código de producción.

## Validación completa y regeneración

- `uv run pytest -q`: **837 passed, 567 warnings, 855,75 s**, rc 0. Mismas clases de advertencias ya existentes: frecuencias pandas, futura API ADF y rechazo deliberado de no finitos.
- La suite ejecutó stress dos veces en `C:/Users/gabri/AppData/Local/Temp/pytest-of-gabri/pytest-684/stress0050`: salidas y YAML idénticos por bytes; fuentes, panel, modelos previos y bloques de variables preservados.
- `uv run python -m src.pipeline stress` en la copia activa: rc 0. Las **18 salidas y YAML** coinciden por bytes con la doble corrida aislada.
- Comparación desde inventario propio tomado antes de corregir: **solo dos salidas cambian**, `outputs/tables/stress_levels.md` y `outputs/tables/stress_delta.md`. Cada una cambia exactamente una aparición de `(proporción 0,010)` por `(proporción 0,011)`; no cambia ninguna otra línea.
- Los **otros 16 artefactos de estrés** mantienen sus bytes, incluidos todos los CSV y ambos PNG. `_variables.yml` completo mantiene sus bytes; ninguna cifra sin redondear ni cifra derivada del riesgo cambia.
- **192 archivos protegidos** conservan sus huellas: datos, salidas restantes, código y tests no autorizados a cambiar, specs/revisiones 003/004, contratos 005, `.gitattributes` y dependencias. Los únicos archivos de código/tests distintos son `src/stress_tables.py` y `tests/test_stress_outputs.py`.
- Spec SHA-256 `6d9713dd1917b4b9b5a2ffc87c7f202869981e9102c9e8e11bf60daac99c77bb` y plan `8b0fc56b3ba2577a0c142a8ab70568af96caed9bf2bbcf18949f42c8ad3d232a`, intactos. Sin commit ni push; cambios locales ajenos conservados.

Evidencia: `docs/reproducibilidad-005-ronda3-2026-10-12.json`, inventarios antes/después, huellas y raíz de reproducción. Registros anteriores de reproducibilidad y todas las rondas permanecen intactos. No se volvió a ejecutar all por este cambio exclusivamente de presentación; su evidencia anterior se conserva sin atribuirle una ejecución nueva.

## Cobertura y entrega

RF-8/15/16 y principio 5: pie, celda y variable coinciden para el mismo valor y criterio de redondeo. RNF-7/8: doble corrida y preservación; los demás RF/RNF conservan la evidencia de rondas previas, ahora nuevamente comprobada por la suite completa y las huellas. No se modificaron recursión, réplicas, fuentes, transformaciones ni reglas aprobadas.

Rutas y criterios originales para Claude: `docs/paquete-auditoria-005-2026-10-12.md`, alcance vigente de ronda 3. La auditoría puede concentrarse en el único bloqueante y en que solo cambian los dos Markdown. No proporcionar este veredicto del autor como conclusión previa ni implementar opcionales. T10 permanece sin marcar y 005 abierta; si falta cuota, registrar continuidad de la auditoría sin transferirla al implementador.
