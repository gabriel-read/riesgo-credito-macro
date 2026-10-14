# Correcciones R3-X1–X7 — 006, ronda 5

Codex, 13-oct-2026. Copia Orca única. La ronda 4 se conserva como histórica en `outputs/preview-006-ronda4-evidencia/` y `docs/paquete-auditoria-006-ronda4-preservada.md`; no acredita las correcciones editoriales posteriores de Claude.

## Identidad antes de continuar

Las nueve SHA completas del anexo de `review-audit-ronda3.md` coincidían 9/9 con las fuentes al retomar. Frente a la ronda 4 habían cambiado 02/05/06/07/09. Evidencia: `docs/identidad-fuentes-006-ronda5.json`. Posteriormente Claude, en turno breve R3-X7 solicitado por Codex, eliminó únicamente dos remisiones redundantes de 02/04 y devolvió la pausa total (incluida 007): `docs/cesion-claude-006-ronda5.md`. Sus otras siete huellas siguen idénticas al anexo; C1–C7 se conservan. Las dos nuevas SHA y el conjunto final de nueve quedan en el JSON de identidad, sin reescribir la auditoría.

## Resolución delimitada

| ID | Resolución | Fuentes y límites |
| --- | --- | --- |
| R3-X1 | «las especificaciones» en 03b y 11. | Dos concordancias; no cambia método. |
| R3-X2 | La Tabla 1 sí tiene cinco columnas, incluida Signo y contexto; su título con signos es correcto. Se explica que el guion de Obradović remite al signo de la tasa de préstamo descrito en 2.5 y no significa cero/ausencia. Procedencia de Golitsis sale de su celda y pasa a nota; anexo E identifica resúmenes frente a texto completo. | Se conservan las cinco lecturas dudosas con guion, conforme a spec §Literatura. No se reintroduce un signo de política. Procedencia de matriz verificada/002 y verificador de citas; Codex no afirma leer ahora el artículo completo. |
| R3-X3 | Fuente FRED y explicación de franjas USREC en la leyenda de la Figura 1 y su versión del anexo. Filtro conserva esa fuente porque el PNG original no la incluye. | PNG científico intacto; inspección del generador muestra franjas según USREC. |
| R3-X4 | VIF traducido en nombres de pruebas y en notas/limitaciones, incluidos rezagos de tasa. Notas explican que VIF no tiene p de contraste, CUSUM no exporta estadístico/p aquí, y Nota vacía no añade información. | CSV, vacíos, guiones y veredictos intactos. Panel casi vacío se conserva por contrato de anexos completos; no se inventan estadísticos. |
| R3-X5 | Etiqueta ASCII explícita de los DOI en una caja Typst que impide su partición; referencias procesadas antes del filtro de etiquetas y una sola bibliografía. El ajuste inicial de separación silábica y la etiqueta sola no resolvían el doble guion visible. | DOI/BibTeX intactos. Página 35 nueva inspeccionada ampliada: `ceej-2023-0016` íntegro. URL destino conservada; clic de la entrega se registra por separado. |
| R3-X6 | Notas de redondeo solo si hay contenido numérico; no en Tabla 2/5 textuales. Tabla 7 una fuente. Nota de estrés explica tasa cero mientras la lectura del Modelo II no sea de evidencia fuerte. | Adaptadores desde fuentes aprobadas, no nueva regla ni estimación. |
| R3-X7 | «Y representa la primera diferencia de la morosidad» mediante variable existente; remisión redundante del manifiesto eliminada. Claude eliminó las dos repeticiones de sus archivos. | Ecuaciones, cifras y sus cambios editoriales previos intactos; propietarios delimitados. |

## Evidencia y puertas

Seis regresiones iniciales en rojo (`pytest-006-ronda5-rojo.log`); once tests nuevos cubren VIF/notas, vacíos, tablas textuales, regla, concordancia, fuente USREC, cautela/procedencia, fuente única, conservación de leyenda, caja DOI y bibliografía única. El rojo de la caja DOI y los intentos de orden de filtros se conservan. Focalizados finales de presentación: 116 passed. Suite íntegra final: 960 passed, 567 warnings, 917,76 s, rc 0, sin exclusiones; fuentes autoradas idénticas antes/después y posteriormente. La primera suite de 958 y los intentos interrumpidos anteriores a la corrección visual no acreditan esta versión; no se presentan como criterio de cierre.

Renders definitivos: `render-006-ronda5-entrega.json`; repetición y QA propios en los registros de ronda 5. Los PDF actuales cumplen las frases exigidas (cero de ambas retiradas, tres del error estándar en el principal) por texto obtenido del visor; también se comprueban DOCX/GFM. Visual: tres contactos del principal y diez del anexo, muestras ampliadas; solo páginas 34–35 cambian respecto del primer render de estas correcciones, con las 149 páginas del anexo idénticas por píxel/bytes. Las verificaciones completas se vinculan por SHA a los archivos entregados; revisión visual nativa Word/Google Docs no acreditada. La congelación se registra en el paquete nuevo al concluir reproducibilidad y clics.

Google Docs, 006 y T12 pendientes. Sin commit/push, nuevas dependencias, edición de raw o contratos científicos. El paquete vigente se sustituirá explícitamente por ronda 5 al terminar; no se reutiliza el veredicto de ronda 4.

Cierre de controles técnicos: reproducibilidad del render completada (solo metadatos temporales distintos, GFM exacto), report ×2 con 208 productos idénticos. Clics finales 53/53 y 167/167 marcadores, 55/55 destinos URI únicos (34 locales y 21 externos), ligados a las huellas de los PDF nuevos; navegación externa no equivale a acceso completo a artículos. Ronda 4 preservada por bytes y cotejada con su manifiesto original. Paquete y validación del autor nuevos de ronda 5; revisión independiente aún pendiente.
