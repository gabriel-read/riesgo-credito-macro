VEREDICTO: APROBADO

# Validación técnica del autor — 006, ronda 7

Codex, 13-oct-2026. Autor de correcciones, no auditor independiente. R5-1–R5-5 y ajuste R5-6 recibido de Claude. 006, T12 y Google Docs permanecen abiertos para comprobación acotada e importación.

Suite íntegra: **974 passed, 567 warnings, 1093.01 s; rc 0, sin exclusiones**. Log docs/pytest-completo-006-ronda7.log; SHA-256 59bcf75a64d61336c5dc19f40f21e9fa4e107931eb3cf50a78709cc388a271cf. Una corrida inicial se interrumpió para conciliar Tabla 2; otra suite completa generó evidencia preliminar, cuyo DOCX reveló un rótulo pendiente del Modelo II. Ambas se conservan como antecedentes, sin acreditar la entrega final. Reinicio completo sobre las fuentes corregidas, sin exclusiones. Siete regresiones nuevas primero en rojo y 42 focalizadas verdes. Ninguna fuente cambió durante la suite.

R5-1: Tablas 2, 4 y 6 conservan todos sus datos, título y notas en bloques indivisibles de PDF. R5-2: vacíos/Motivo explicados al lector y pre-registro sin tautología. R5-3: nota Tabla 1 remite al texto. R5-4: ambos coeficientes desde estimaciones principales. R5-5: una corrección terminológica de FGLS en matriz. Ajuste recibido R5-6: 02 exacta con SHA de Claude; anexo E concordante, sin inventar signo.

## Correspondencia entre entradas y entregables

Registro `docs/render-006-ronda7-final.json` y `render-006-ronda7-repetida.json`: cada comando tiene huellas completas de 369 entradas antes y después. **Cero diferencias en los ocho renders finales.** El conjunto completo es idéntico entre ambas generaciones y al congelar. La preparación previa tiene registro separado: presentación reconstruida desde las correcciones y mapa de páginas actualizado desde el PDF del anexo; investigación en `docs/investigacion-entradas-render-006-ronda7.md`. No se infiere correspondencia solo por fechas.

PDF: 35 páginas principal, 149 anexo. DOCX: todas las celdas/figuras cotejadas con trazas; anexos completos. GFM generado sin referencias ni variables irresueltas. Repetición: GFM idéntico por bytes; PDF todos los objetos de contenido iguales excepto fechas/IDs de metadatos; DOCX todos los miembros iguales excepto fechas de core.xml. Report×2: 208 productos iguales.

116 fuentes/salidas protegidas y 25 módulos científicos intactos. Variables canónicas y espejo iguales, sin cambios numéricos. BibTeX/spec/plan intactos; matriz solo la palabra autorizada. Nota de estrés entrada directa, SHA completo sin cambio.

Clics actuales: 53 internos principal, 167 internos anexo y 55 URI únicos. Destino observado, sin certificar acceso integral al artículo. Inspección visual y alcance exacto en `docs/visual-verificada-006-ronda7.json`. No verificación nativa Word ni Google Docs.

## Huellas de entrega

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf | 658814c512685718f8a06ec3362ef3fa07d4636653ed38d34f79b208a1a487ad |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx | 7917fcf0c7daccd699587766a693fa4738cd05383eaa2f1d00063e6b711cca22 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.md | 6704875411ad0d4baf8732606521f1950d0638337eaa1ddeef8e9e70ece6002c |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf | 73bbdfabd0f4cd84b347507fc602d990bac6f3267595fb3569383ddc142a0fcd |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx | c51d02cb4d2c0755903403532d28c42c076437f1a020c670a37e37bc4130dc67 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.md | 2cb012c6a3484fbae1472dd6e9d745202c4272b993e02b8fbb86f274934b6c52 |

Manifiesto: `docs/huellas-paquete-auditoria-006-ronda7.json`. Antecedentes preservados. Sin commit ni push.
