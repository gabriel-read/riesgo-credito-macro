# Diagnóstico de tablas y propuesta editorial 006

Autor técnico: Codex, 12-oct-2026. Copia exclusiva: `C:/Users/gabri/orca/riesgo-credito-macro`. Propuesta metodológica/editorial coordinada con Claude en `specs/006-informe/change-editorial-draft.md`, escrita únicamente en su turno y devuelta a Codex. G1 visual aprobada por el autor; nueva estrategia editorial pendiente de aprobación. Sin commit ni push.

## Maqueta preservada

El PDF original de 122 páginas y su DOCX permanecen en `outputs/smoke-006/report/informe.pdf` y `informe.docx`. Antes de corregir se congelaron 151 archivos de evidencia en `outputs/smoke-006/evidencia-g1-original-122/`, con manifiesto de SHA-256 propio. Incluye documentos, `.qmd`, variables, interfaz, trazabilidad y tablas de presentación originales. No se copió entre checkouts.

## 1. Modelo II — proyecciones locales

**Identificación:** título «Modelo II — proyecciones locales», `model2_lp`; Panel 5, páginas **48–49** del PDF original. Panel 5 contiene **h y Nota φ**, no el valor de φ: h=0…3 en página 48 y h=4…12 en 49. Valores de φ en Panel 3 (páginas 47–48), errores/bandas en Panel 4 (página 48). CSV: `outputs/tables/model2_lp.csv`, **13 filas de datos**, líneas físicas **2–14**, h=0…12. La nota de identidad ocupa línea 2; `phi_nota` vacío en líneas 3–14.

**Rastreo:** `src/localproj.py:local_projection`, objetivo tasa y h=0, retorna identidad sin estimar: φ=1, sin EE ni banda, `IDENTITY_NOTE = "por construcción (identidad)"`. `run_local_projections` conserva esa nota en `phi_nota`; el campo `estado` y `motivo` de la fila describe la proyección de morosidad, no el estado separado de φ. `src/model2.py:render_model2_tables` exporta CSV y el pie de `lp_note2()` a `outputs/tables/model2_lp.md`. Ese pie ya define β/φ y explica que la identidad no lleva error ni banda.

Los JSON principales **no son fuente de esta tabla**. `model2_main.json` no exporta proyecciones locales, `phi_nota` ni sus bandas. Su campo `response` es R(h) del modelo de rezagos distribuidos; no debe confundirse con φ_h. No se estimó ni reconstruyó ninguna salida para este diagnóstico.

**Defecto de presentación confirmado:** el adaptador 006 leía solo CSV, dividía columnas cada tres y generaba `outputs/informe/model2_lp_anexo_3.md`, `_4.md`, `_5.md`. Así aislaba `phi_nota` en un panel casi vacío y perdía el pie aprobado del Markdown original. `model2_lp.md` de presentación también omitía ese contexto. El PDF conservaba «por construcción (identidad)», pero la explicación estaba ausente y los valores separados. Los vacíos de h>0 son ausencia válida de nota adicional; no son estimaciones faltantes.

**Corrección dentro del contrato:** el pipeline lee el pie literal aprobado de `outputs/tables/model2_lp.md` y el generador puro lo sitúa antes de la presentación y de cada panel con campos φ. `trace.json` registra el texto y el archivo original. Todas las celdas, columnas y filas permanecen iguales. Eliminar el panel y convertirlo definitivamente en pie forma parte de la propuesta editorial, no se ejecuta antes de su aprobación porque el contrato actual conserva cada columna en los paneles completos.

## 2. Modelo I — estimaciones de robustez

**Identificación:** título «Modelo I — estimaciones de robustez», `model1_robustness_estimates`; Panel 5, inicio en **página 29**, continuación hasta **33** del PDF original. Columnas `variante`, `estado`, `motivo`, `nota`. La página 29 inicia las dos primeras filas R1 (regresores `gdp_growth` y `d_unemp`, líneas CSV 2 y 3). CSV: `outputs/tables/model1_robustness_estimates.csv`, **46 filas de datos**, líneas físicas **2–47**: 45 filas estimadas R1–R7/variantes y una fila R8 no estimada al final.

**Rastreo:** `src/model1.py:robustness_estimates` escribe explícitamente `motivo=""` en cada regresor de una variante estimada (línea 548 al revisar); cuando no se estima, exporta `motivo=o.reason` y una única fila. En el CSV las líneas **2–46** tienen motivo vacío; línea **47**, R8, estado «no estimada», motivo «sin historia anterior a 2000T1». Las notas R1 explican la exclusión y tratamiento de historia. No se ha reinterpretado esa historia ni corregido la salida protegida.

`outputs/models/model1_main.json` exporta el ajuste principal, no estas variantes, sus motivos ni sus notas. La fuente de presentación es directamente el CSV. `outputs/informe/model1_robustness_estimates_anexo_5.md` y sus 46 filas en `trace.json` conservaban los vacíos, que el PDF imprimía sin contexto.

**Vacío válido, explicación ausente:** `motivo` documenta una causa de no estimación; no es una justificación científica para cada variante ni un campo que deba completarse en filas estimadas. R8 confirma que el campo sí se exporta cuando corresponde. No hay pérdida en CSV→Markdown→PDF. No se rellena con «n.a.», cero o texto inventado.

**Corrección dentro del contrato:** nota antes del panel: «Las celdas vacías de Motivo conservan los vacíos del CSV. En las filas con estado “estimada” no se informa una causa de no estimación; las filas “no estimada” conservan su motivo original». Las celdas vacías siguen vacías y R8 conserva su motivo exacto.

## Comprobaciones de las correcciones

- Regresiones primero: dos fallos que reproducían pie ausente y vacío sin explicación; después 53 focalizados aprobados, 12,21 s. `uv run pytest -q` se inició por cambio de código y detectó el fallo ajeno del arnés descrito abajo. Se detuvo sin concluir: `tests/test_frozen_stress.py` recalcula el inventario completo de `outputs/` dentro del bucle de cada archivo protegido; la evidencia QA incrementó mucho ese coste. No se alteró ese test ni se evitó su fallo con exclusiones; **no hay suite completa verde para esta corrección**. La ejecución y cadena de procesos propia quedan registradas en el JSON. La validación global permanece pendiente, sin reabrir el cierre aprobado de 005.
- Render acotado: `outputs/smoke-006/diagnostico-tablas.pdf` y `.docx`; cuatro paneles, 13/13/13/46 filas. PDF de ocho páginas revisado con previsualizaciones; DOCX con celdas originales y notas presentes. La paginación visual en Word no se afirma: el autor no tiene licencia y revisará el importado en Google Docs.
- Render principal corregido con nombre distinto: `outputs/smoke-006/informe-notas-corregidas.pdf` y `.docx`; no reorganiza documentos ni sustituye el original de 122 páginas. El corregido también tiene 122 páginas: se inspeccionaron las ubicaciones 29, 48 y 49, además del fixture completo. Sus 109 tablas coinciden celda por celda con el DOCX original: 2691 filas de datos, 2800 contando cabeceras.
- 99 fuentes/salidas protegidas, variables canónicas y contratos 006 se cotejan por SHA. Las cifras no cambian; solo contexto y trazabilidad de presentación.
- Incidencia ajena detectada en suite: `test_sdd_procedure_and_operator_guide_local_links_resolve` falla porque falta `Playbook agéntico SDD riesgo de crédito.md` (Git lo muestra eliminado), enlazado desde `docs/flujo-codex-orca.md`. No lo eliminó esta corrección ni se restauró/modificó el arnés. No se declara suite verde mientras subsista.

## Cambio editorial concreto pendiente

El borrador de Claude contiene los deltas propuestos a spec v3, plan v2 y tareas v2, sin editar los originales aprobados. Se propone:

1. **Informe narrativo** `report/informe.qmd`, PDF/DOCX, índice y 11 secciones oficiales. Cuerpo: literatura sintética; datos y transformaciones; coeficientes y diagnósticos esenciales; respuesta dinámica; comparación entre modelos; cambios de estrés; tablero cualitativo y conclusiones. Los límites científicos y diagnósticos rechazados permanecen explícitos en el cuerpo, aunque el detalle tabular se remita al anexo.
2. **Anexo técnico completo** `report/anexo-tecnico.qmd`, PDF/DOCX e índice por datos, Modelo I, Modelo II, estrés, literatura y reproducibilidad. Conserva las 34 tablas y nueve figuras disponibles, fuentes, filas, columnas y notas. No elimina datos para abreviar el informe.
3. **Registro único** de fuente→identificador→destino, generado y trazable, con slugs permanentes como `AT-M2-LP`, `AT-M1-ROB`. Los números de página no serán identificadores. Las versiones reducidas del cuerpo se generan desde el mismo CSV y remiten a la tabla completa; una tabla completa no se duplica por rutina. Las figuras esenciales del cuerpo se seleccionan expresamente; no se interpreta «versión reducida» como recortar un gráfico o su incertidumbre.
4. **Tareas nuevas T13–T15**, seriales, sin renumerar T1–T4 completadas: registro/IDs; anexo y selección editorial; render doble, índices y enlaces. Luego T10 y relevo exclusivo a Claude para T5–T9. T11/T12 verifican cobertura, navegación y suficiencia del cuerpo. La agrupación y cualquier duplicación indispensable deben quedar fijadas antes de implementar. La salida concatenada que sugiere Claude es opcional y **no se implementa por defecto** dentro de la petición de dos documentos.

La revisión técnica concreta dos puntos del borrador de Claude antes de aplicarlo: en 2.5, «solo estudio/método» no basta por sí mismo; el cuerpo debe explicar también variables y signos respaldados, con remisión al detalle y sin reutilizar lecturas dudosas. Para figuras esenciales, no se recorta el PNG ni se omiten bandas para llamarlo «versión reducida»; su ubicación y cualquier repetición justificada se declaran en el registro. La regla de no duplicación completa por rutina se aplica especialmente a las tablas. Estos ajustes forman parte de la propuesta presentada al autor, no de una implementación ya realizada.

### Enlaces: evidencia y límites

Prueba mínima independiente de la reorganización, en `outputs/smoke-006/enlaces-editoriales/`: `principal-enlaces.pdf/docx` y `anexo-enlaces.pdf/docx`. No contiene resultados nuevos ni duplica las tablas.

**Comprobado en archivos reales:** PDF anexo contiene destinos nombrados `indice`, `at-m2-lp`, `at-m1-rob` y cuatro anotaciones internas que los resuelven. DOCX contiene los mismos marcadores nativos y cuatro hipervínculos internos con destinos existentes. Principal PDF contiene URI relativas a `anexo-enlaces.pdf/docx`; principal DOCX contiene relaciones externas relativas a esos archivos. Los destinos existen y se entregan en la misma carpeta. El mecanismo es nativo de Pandoc/Typst, no anclas HTML que se pierdan al exportar.

**Estrategia propuesta:** índice clicable y enlaces de retorno dentro de cada documento; desde el principal, enlace relativo al anexo correspondiente y remisión textual permanente a su identificador. El enlace abre el archivo; no se promete salto externo a una página concreta ni se usa `@tbl-` como referencia entre documentos. Se entrega la pareja junta con nombres fijos y se verifica que cada ID exista.

**Google Docs:** al subir los DOCX por separado, la relación de archivos locales deja de ser resoluble. Los marcadores se comprueban en el DOCX generado, pero la importación y el clic en Google Docs requieren comprobación manual del autor. Para navegación entre documentos en la nube se necesitan las URLs reales de Drive facilitadas por el autor; no se inventan ni se suben documentos desde el agente. Se pueden inyectar esas URLs de forma explícita sin tocar las variables científicas. Sin URLs, queda la remisión textual y el enlace local para la pareja descargada; no se promete navegación entre archivos de Google Docs. No se afirma prueba de clic en Word nativo o Google Docs realizada.

## Pendientes únicos para aprobación

- Aprobar el `change` editorial de dos documentos, selección esencial, registro estable y T13–T15, incorporando la estrategia local/nube y la regla de no duplicación descritas arriba. Los originales spec/plan/tasks no se reorganizaron.
- Revisar los dos casos corregidos y, posteriormente, enlaces importados en Google Docs; aportar URLs de Drive si se requiere navegación entre documentos allí.
- Resolver el archivo histórico ausente del arnés fuera de este cambio; impide declarar suite completa verde. Consultar al profesor la aceptación de material complementario separado según el pendiente ya documentado.

005 permanece cerrada y 006 abierta. No se continúa la integración narrativa antes de aprobar el cambio editorial.
# Comprobación de la versión separada — 12-oct-2026

La maqueta original y el diagnóstico histórico se conservan. En `outputs/preview-006/report/anexo-tecnico.pdf`, **AT-M1-ROB** corresponde a Tabla B.6: Panel 5 comienza en **página 33**, con la nota sobre Motivo encima de las filas R1; siguen vacías las 45 filas estimadas y se conserva el motivo de R8. **AT-M2-LP** corresponde a Tabla C.7: las cifras de φ y la nota de identidad aparecen en **página 53**, Panel 3; sus bandas continúan en Panel 4. `phi_nota` se conserva como nota trazable, sin un quinto panel vacío. Las 13 filas h=0…12 y sus cifras permanecen intactas. Comprobación visual de ambas páginas y comparación integral de las 110 tablas de paneles del DOCX con la trazabilidad del CSV. Evidencia: `docs/qa-editorial-006-2026-10-12.json`.

