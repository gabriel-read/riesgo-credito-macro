VEREDICTO: APROBADO

# Validación técnica del autor — 006, ronda 6

Codex, 13-oct-2026. Paquete final nuevo de las correcciones autorizadas R4-X2–X5/P1. No es auditoría independiente ni cierre global: Google Docs RF-14b, 006 y T12 pendientes.

## Alcance y conservación

02 completo y las otras ocho secciones de Claude permanecen idénticos por las nueve SHA del paquete ronda 5. El usuario conserva el alcance de verificación y el párrafo de candidatos no usados; se comprueban también en los entregables reales. Las 337 entradas de ronda 5 se cotejaron antes de editar y se archivaron con sus bytes; fuente/paquete/manifiesto anteriores conservados. No R4-O1/O2, nuevas referencias, parámetros, datos, metodología ni estimaciones.

R4-X2: notas VIF/CUSUM sin lenguaje de proceso ni repetición en el panel de notas, conservando todos los vacíos/resultados. R4-X3: nota de Obradović concordante con el resumen verificado y signo de la tasa de préstamo de 2.5, guion original conservado. R4-X4: nota única claramente asociada a Tabla 1, Golitsis íntegro y tabla en dos páginas (6–7), letra de nueve puntos. R4-X5: rezago, pre-registro, nota de comparación y FGLS destinados al lector; «generalizables» no se sustituye cuando expresa aplicabilidad. R4-P1: nota de estrés añadida con entrada directa absoluta. Detalle y evidencia: docs/correcciones-tecnicas-006-ronda6.md.

## Pruebas y generación

**Suite íntegra: 967 passed, 567 warnings, 951.69 s; rc 0, sin exclusiones**. Log docs/pytest-completo-006-ronda6.log; SHA ee8303234ea6edeb8eeba5589bd58a0c217dadaf13e86e1f3e3122d2c58fc28b. Fuentes autoradas iguales antes/después y al congelar. No tests excluidos: solo dos .typ generados se distinguen de las fuentes autoradas en el control de estabilidad. Siete regresiones nuevas; seis rojos iniciales, negativo de respaldo y control de celdas/terminología. 123 pruebas de presentación verdes. Los asserts de palabras antiguas se actualizan a la redacción autorizada manteniendo supresión de cinco signos, filas, métodos y regresores.

Cuatro comandos de render, rc0, repetidos a otro directorio con rc0: PDFs/DOCX principales y anexos, más GFM. Contenido, imágenes y enlaces de los renders idénticos: solo metadatos Info/XMP/IDs temporales de PDF y fechas de DOCX varían; GFM idénticos por bytes. Report×2: 208 productos iguales. 116 protegidos y 25 módulos científicos intactos; BibTeX/matriz y variables canónicas/espejo intactos.

Principal 35 páginas/anexo 149; ocho tablas/117 paneles y cuatro/nueve figuras, 44 slugs. DOCX: todas las celdas comparadas con las trazas, XML/figuras/bookmarks correctos. Fuente de Golitsis y nota de Obradović comprobadas en PDF/DOCX/GFM. Frases anteriores retiradas siguen ausentes; explicación del error estándar sigue tres veces en principal. Los términos internos identificados desaparecen y los dos pasajes conservados de 02 permanecen.

Visual de archivos actuales: PNGs/contactos, muestras ampliadas, huellas y límites en docs/visual-verificada-006-ronda6.json. Clics reales: 53/53 y 167/167 marcadores internos; 55/55 URI únicos, una aparición por destino. Tolerancia interna 1 píxel CSS; entre archivos se verifica página de fallback, no coordenada exacta. Navegación externa no certifica acceso al artículo. Sin comprobación visual nativa Word ni importación/clics en Google Docs; no se atribuyen a los auditores estos controles de Codex.

## Entrada de la nota y huellas

Ronda 5 cubría la nota indirectamente mediante docs/reproducibilidad-report-006-ronda5.json, cuya SHA 1e39e95f79e676979c155ee31f1d5e1f3ed40371e6ec87f8f781c97d67386956 estaba en el manifiesto; su mapa interno contenía la SHA de la nota. No tenía entrada directa. El manifiesto nuevo la incorpora y enumera todos los productos de outputs/informe/:

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/informe/stress_delta_nota.md | 733d7017c257017157a4644ced7b4069c8b3559cbeb7ce65886caf36caa8c935 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf | 4c8710e9f6e0ba75201aae9af001c3a6f1fee4ce2e287c419954d4fb64454e74 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx | e63338782f2f962fab0462413a7495419f647f6772a93e1727fa3d2fae9d26d8 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.md | c406a99835ddf201924be68adf2ce9841ceeb129e061c273854453f63f5026d7 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf | 6b99442e653b5a1e07d432318003669f09f866068518a5d57826f21f25e5ff16 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx | 8ebfd114df6d2b2a82a18248826fa64d7fc0f3fc3005e49c3d6e8a9d83db7595 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.md | 801a141e6763a144ef53cdad85e8bdf3c5aa3a5da6ad5f6e3fcac4092149b967 |

Manifiesto completo: docs/huellas-paquete-auditoria-006-ronda6.json. Históricos íntegros conservados. Sin commit ni push.
