# Correcciones editoriales finales — 006, paquete ronda 6

Codex, 13-oct-2026. Alcance autorizado: pendientes R4-X2, X3, X4, X5 y P1 de `specs/006-informe/review-audit-ronda4.md`. R4-X1/X6 resueltos por decisión expresa del usuario: conservar alcance de verificación y candidatos no usados. **02 completo y las otras ocho secciones de Claude permanecen idénticos por SHA-256.** Claude confirmó cesión exclusiva y pausa de escritura/ejecución, incluida 007.

## Identidad y antecedentes conservados

Las 337 entradas del manifiesto ronda 5 coincidían antes de editar. Se preservaron todas en `outputs/preview-006-ronda5-evidencia/snapshot/`, con las seis salidas también en `outputs/preview-006-ronda5-evidencia/report/`. La nota de estrés omitida como entrada directa se preservó aparte. Evidencia y huellas: `docs/identidad-y-preservacion-006-ronda6.json`. Paquetes, manifiestos y revisiones anteriores no se reescriben; los índices vigentes se actualizarán al finalizar la nueva validación.

## Cambios delimitados

| Hallazgo | Corrección y límite |
| --- | --- |
| R4-X2 | VIF/CUSUM se explican una sola vez en el panel de resultados de cada diagnóstico. «Salida del modelo» sustituye «salida aprobada». El panel de notas explica al lector dónde están los resultados y qué significan sus vacíos, sin instrucciones sobre CSV o conservación del anexo. Estadísticos, p-valores, vacíos y veredictos originales intactos. |
| R4-X3 | La nota del anexo E para Obradović identifica el resumen como base, la asociación positiva de la tasa de préstamo y su diferencia de la tasa de política; remite a 2.5. Sale del hallazgo verificado de la matriz, no de una lectura nueva. La celda de signo conserva «—» por el contrato existente. Un negativo verifica que, sin ese respaldo, no se añade la asociación positiva. |
| R4-X4 | Procedencia de Golitsis y aclaración de Obradović reunidas en **Nota de la Tabla 1**, junto a la tabla. Anchos relativos ajustados solo para esa tabla, sin reducir sus nueve puntos de letra ni eliminar celdas; encabezado unido al comienzo de la tabla. Primera maqueta inspeccionada: filas en páginas 6–7 y nota en 7; antes estaban en 6–8 y la nota de procedencia quedaba separada. |
| R4-X5 | «Crédito rezagado» en 03e; «pre-registro» uniforme en 03c/03e. Nota de Tabla 6 describe estimación principal, asociaciones condicionales, HAC y formas de controles sin remitir a decisiones internas. Notas de literatura se destinan al lector, sin «consultar la matriz». FGLS se presenta como **mínimos cuadrados generalizados factibles**; «generalizables» se conserva cuando califica la aplicabilidad de resultados. Método original en la matriz y CSV sin alterar; es corrección de presentación. |
| R4-P1 | La nota no tenía entrada propia en ronda 5. Su cobertura era **indirecta**, mediante la entrada absoluta de `docs/reproducibilidad-report-006-ronda5.json`, SHA `1e39e95f79e676979c155ee31f1d5e1f3ed40371e6ec87f8f781c97d67386956`; su clave `sha256_by_relative_path["outputs/informe/stress_delta_nota.md"]` contiene `733d7017c257017157a4644ced7b4069c8b3559cbeb7ce65886caf36caa8c935`, cotejada con los bytes. El manifiesto nuevo incluirá la nota como entrada absoluta propia y todas las salidas de presentación. No se atribuye entrada directa retroactivamente al manifiesto anterior. |

No se aplican R4-O1/O2 opcionales. No se modifica literatura ni bibliografía protegida, ninguna decisión científica, spec/plan aprobado, datos congelados, valores canónicos, módulos científicos ni arnés. 007 permanece fuera de alcance.

## Pruebas y siguiente acción

Siete tests nuevos: seis rojos iniciales y uno verde (negativo sin respaldo). Regresiones cubren notas únicas/vacíos intactos, Obradović con/sin respaldo, nota asociada, terminología según contexto y anchos sin cambiar celdas. El test anterior que exigía la palabra interna «observaciones» se adapta a las explicaciones del lector, conservando controles de cinco signos suprimidos, filas, métodos y regresores originales. **123 tests de presentación passed**; no sustituyen la suite íntegra.

Validación final: **967 passed, 567 warnings, 951,69 s, rc 0, sin exclusiones**; fuentes autoradas idénticas antes/después y después de los renders. Renders PDF/DOCX/GFM completos y repetidos, rc0: contenido y enlaces iguales, solo metadatos temporales distintos; GFM exactos. Report×2: 208 productos iguales. Las 116 fuentes/salidas protegidas y 25 módulos científicos, matriz/BibTeX y variables canónicas permanecen intactos.

Entregables finales: principal35p/anexo149p, ocho tablas/117 paneles, cuatro/nueve figuras y 44 slugs. DOCX/XML: todas las celdas/medios/bookmarks cotejados. Texto real PDF y texto DOCX/GFM: pasajes de02 conservados, expresiones internas señaladas ausentes, notas de Golitsis y Obradović presentes con sus calificaciones. Visual: tres contactos del principal y seis del anexo que cubren todos sus cambios; páginas restantes del anexo idénticas por bytes a las inspeccionadas en ronda5. Muestras ampliadas de p7 principal y p51/p146 anexo; Tabla1 completa en6–7, nota claramente asociada en7. Clics actuales53/53 y167/167 marcadores internos y55/55 URI únicos, con SHA del PDF correspondiente; navegación externa no equivale a acceso completo al artículo.

Paquete final nuevo ronda6 y su manifiesto incorporan directamente la nota de estrés con su SHA completo. Validación del autor y revisión independiente se distinguen; no revisión visual nativa Word ni Google Docs afirmada. Google Docs, 006 y T12 pendientes. Codex congela la entrega y cede a Claude la revisión acotada. Sin commit ni push.
