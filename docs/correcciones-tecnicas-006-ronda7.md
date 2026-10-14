# Correcciones autorizadas R5-1–R5-5 — paquete ronda 7

Codex, 13-oct-2026. Alcance limitado por el usuario; no cambian cifras, decisiones científicas ni contratos. Ronda 6 y antecedentes conservados.

| ID | Cambio de presentación | Fuente que se conserva |
|---|---|---|
| R5-1 | Tablas 2, 4 y 6 agrupadas con título, filas y notas en un bloque indivisible de Typst. La tabla completa del anexo conserva sus paneles. | Filas, columnas, precisión y procedencia originales. |
| R5-2 | Motivo explica ausencia de información adicional, sin «vacíos del CSV». El rótulo de pre-registro del Modelo I sustituye la tautología. | Vacíos, estados, motivos y desviaciones originales. |
| R5-3 | Nota de Tabla 1 remite al texto, sin autocita «descrito en 2.5». | Procedencia de Golitsis y distinción préstamo/política completas. |
| R5-4 | Nota de Tabla 6 declara que los coeficientes de ambos modelos proceden de sus estimaciones principales. | Coeficientes, HAC, controles y carácter condicional. |
| R5-5 | Una expresión de la fila obradovic2026 de la matriz: «mínimos cuadrados generalizados factibles». | Todas las otras celdas y el hallazgo original; sin modificar aplicabilidad. |

## Ajuste recibido de Claude

02: nuevo SHA-256 `01a299dde5591e6e2a344eb6faa122f7380628b8818a892795733b0dc63aac73`, según `docs/cesion-claude-006-ronda5.md`. Era la única diferencia de las 490 entradas del manifiesto R6 al recibir el turno. Las otras ocho secciones no cambian. Se conserva alcance de verificación y candidatos no usados. El anexo E incorpora desde la misma fila verificada el desempleo negativo y el efecto no consistente del tipo de cambio; no convierte el guion en un signo genérico.

## Pruebas primero

Seis regresiones fallaron antes del cambio; una séptima detectó la omisión de desempleo/tipo de cambio en la nota del anexo. Logs `pytest-006-ronda7-rojo.log` y `pytest-006-ronda7-nota-rojo.log`. Tras corregir, 42 pruebas focalizadas pasan. Dos asserts de la redacción anterior se actualizan manteniendo las comprobaciones de vacíos y significado.

La comprobación del DOCX/GFM preliminar detectó que quedaba el rótulo redundante del Modelo II. Se extendió la regresión a ambos modelos y a la mayúscula inicial del fragmento incorporado de Obradović: dos fallos antes de corregir, 42 focalizadas verdes después. Esa primera entrega y sus registros se archivan en `docs/preliminar-006-ronda7/` y `outputs/preview-006-ronda7-preliminar/`, sin presentarlos como finales. La suite completa posterior, sobre las fuentes definitivas, dio **974 passed, 567 warnings, 1093,01 s, rc 0**, sin exclusiones y sin cambios de fuente durante la ejecución (`pytest-completo-006-ronda7.json/log`).

## Estabilidad de generación

El gancho pre-render reconstruye presentación y rutas desde las fuentes. Los destinos contienen páginas extraídas del PDF del anexo: una primera preparación puede actualizar ese mapa cuando cambia la paginación. Eso requiere investigar y estabilizar, no declarar reproducibilidad por fechas. El registro de cada render final debe contener huellas de todas las entradas antes y después, diferencias explícitas y comandos/resultados reales. Si aparece otra diferencia, se detiene la declaración de reproducibilidad hasta identificarla.

## Límites

Sin edición de secciones de Claude, fuentes científicas 001–005, datos congelados, referencias ni decisiones metodológicas. La corrección de una palabra de la matriz está expresamente autorizada en R5-5. Google Docs, 006 y T12 permanecen abiertos. No se afirma paginación nativa de Word ni navegación en documentos importados sin comprobarlas. Sin commit ni push.
