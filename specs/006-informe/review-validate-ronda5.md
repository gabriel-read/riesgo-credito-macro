VEREDICTO: APROBADO

# Validación técnica del autor — 006, ronda 5

Codex, 13-oct-2026. Valida R3-X1–X7 y las correcciones editoriales C1–C7 de Claude integradas en estas salidas. No es auditoría independiente ni cierre global: Google Docs RF-14b, T12 y 006 siguen pendientes.

## Identidad y alcance

Las nueve SHA completas del anexo de review-audit-ronda3.md coincidían 9/9 al retomar. Frente a la ronda 4 habían cambiado 02/05/06/07/09; aquella entrega queda histórica. Claude hizo después dos remisiones de R3-X7, solo 02/04, con cesión registrada y nuevas SHA. Las otras siete permanecen idénticas. Las nueve huellas finales figuran en el manifiesto nuevo y el paquete ronda 5; sin sobrescribir su redacción.

R3-X1 concordancia; X2 signos/contexto y procedencia documentados sin inventar signos; X3 fuente FRED/franjas USREC visibles; X4 VIF traducidos y vacíos de p/CUSUM explicados sin completar fuentes; X5 DOI íntegro, enlace original y bibliografía única; X6 redondeo solo en tablas numéricas, fuente única y explicación no circular de tasa cero; X7 forma de Y legible y remisiones redundantes eliminadas. Detalle: docs/correcciones-tecnicas-006-ronda5.md. No cifras/modelos/metodología nuevos.

## Verificaciones ejecutadas

Suite íntegra final: **960 passed, 567 warnings, 917.76 s; rc 0, sin exclusiones**. Log docs/pytest-completo-006-ronda5.log, SHA 9b03fc664d132337cb12907208b70db8e38f4894c7803f078f12176ff7725666. Fuentes idénticas antes/después y al congelar. Los únicos archivos fuera de la clasificación de fuentes autoradas son los dos intermediarios generados informe.typ/anexo-tecnico.typ; ningún test se excluyó. Once regresiones nuevas; 116 tests de presentación finales en verde. Los seis rojos iniciales, el rojo de caja DOI y los intentos interrumpidos/previos quedan conservados y no acreditan la versión final.

Renders final y repetido: cuatro comandos cada uno, rc 0; PDF/DOCX principal y anexo más Markdown. Reproducibilidad: todos los objetos de contenido/imágenes/enlaces de PDF iguales, con diferencias únicamente Info/XMP temporales/IDs; DOCX solo created/modified; GFM idéntico por bytes. Report×2: 208 productos idénticos. 116 fuentes/salidas/contratos protegidos y 25 módulos científicos intactos. Variables canónicas y espejo coinciden.

En PDF, DOCX y GFM finales desaparecen «esa diferencia se invierte» y «La tabla no recoge signos»: cero apariciones. «infla su error estándar» aparece tres veces en el principal; no se exige en el anexo, que no contiene esa discusión. PDF: texto real obtenido del visor, no inferido del Markdown. Registros llevan SHA del archivo comprobado.

DOCX: XML, todas las celdas de las ocho tablas del cuerpo/117 paneles del anexo, figuras y 44 bookmarks contrastados con trazas/fuentes. PDF principal 36 páginas, anexo 149. Inspección visual y huellas de PNG/contactos en docs/visual-verificada-006-ronda5.json. Clics reales Edge/CDP: 53/53 y 167/167 marcadores internos, tolerancia 1 píxel CSS; 55/55 URI únicos (34 locales/21 externos), una aparición de cada destino. Entre archivos se comprueba página de fallback, no coordenada exacta. Navegación externa observada no implica acceso completo al artículo; eventos/respuestas en el JSON de clics, no un certificado de disponibilidad de los sitios.

No se atribuyen estas comprobaciones a auditores que no las ejecutaron. DOCX no tiene revisión visual nativa Word ni importación/clics en Google Docs acreditados. Google Docs obligatorio para cierre sigue pendiente.

## Entregables congelados

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf | 8cdfa2a6521594f6d56c3831aa4da022c2f17063abd823c50a18b01144b91878 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx | 994e28fce7fb7850b5aef9487efb0dca915459b8b3357ff2a46be197a0d3c130 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.md | 38e645d0625a831d2cf7d4f11dfed3bedcebfbcbaa8a58a192e9607a4d5c1e32 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf | 58429c72be4563d86420f115f3deaa0d05f5a9e812ddadc5c753ec5689779c22 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx | 75e241c1637c26174e936b6e68f07c8bc58d416084c565c592840030ed91854c |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.md | 71dca3f71d22f61a145d1891f65cd023732d74b8bdbac05e2aee851f35c8a346 |

Fuentes, comandos, resultados y más huellas completas: docs/huellas-paquete-auditoria-006-ronda5.json. Históricos ronda 4 conservados en outputs/preview-006-ronda4-evidencia/ y docs/paquete-auditoria-006-ronda4-preservada.md. Sin commit ni push.
