VEREDICTO: APROBADO

# Validación técnica del autor — 006, ronda 4

Codex, 13-oct-2026. Valida las correcciones técnicas de auditoría ronda 2 y la integración de las nueve secciones cedidas por Claude. No es auditoría independiente ni cierra 006: Google Docs RF-14b y T12 siguen pendientes. Spec v4/plan v3 intactos.

## Versión y correcciones

El contraste inicial de 511 huellas confirmó los cuatro PDF/DOCX auditados y el YAML/Markdown generado; solo siete secciones de Claude diferían. La entrega histórica no acredita la redacción posterior. Archivada en outputs/preview-006-ronda3-evidencia/; nueva versión regenerada con textos estables y cesión exclusiva (incluida pausa 007).

KPSS: exacto 0.1 sin censura documentada sigue 0,100; límites explícitos uniformados a ≥ 0,10 / ≤ 0,01, conservando operador original y SHA en traza. Nota solo en campos KPSS. Tabla 1 con signos permitidos, sin inferir los cinco dudosos. Estadísticos/VIF legibles, sin inventar p vacíos. Portada autorizada intacta; notas internas y letras redundantes retiradas por sus propietarios. APA: nombres propios, capitalización, nota FRED antes de URL y guiones de títulos sin separación duplicada; BibTeX/DOI mantienen sus datos. Las URL pueden partirse tipográficamente: se verificaron sus URI reales, no acceso completo a artículos.

Figuras: fuente una vez, original científico intacto. Derivados de estrés desde CSV aprobado distinguen adverso continuo y D discontinuo con círculos, sin desplazar puntos; nota explica coincidencia bajo tasa cero. Registro incluye origen científico y SHA, origen de presentación y SHA. PIB(t−1) entregado a Claude desde modelo2.coef.gdp_l1: no necesitó nueva clave ni estimación. Lectura cualitativa de 07 contrastada con trayectorias, sin descomposición numérica nueva.

## Suite, fuentes y reproducibilidad

Suite final íntegra: 949 passed, 567 warnings, 1108,12 s, rc 0, sin exclusiones; fuentes iguales antes/después y verificadas de nuevo al congelar. Log docs/pytest-completo-006-ronda4.log; SHA 675d9b801901c7ce17b4eac095d0e910a0b41cdae2d6ad3c48de21a348d1205f. Primer ciclo 948 verde preservado como pre-guion, con fuentes cambiadas: no acredita esta versión. Nueve regresiones nuevas incluyen exacto/censura, notas, etiquetas, puntos/estilos, DOCX subrayado, FRED, derivados/YAML y AST Figure/guiones; rojos conservados. Sin exclusiones ni reducción de cobertura.

116 fuentes/contratos/salidas protegidas y 25 módulos científicos idénticos. Cambios pipeline solo stage_report. Report ×2: 208 productos idénticos. Dos renders PDF/DOCX/GFM comparados estrictamente: todos los objetos de contenido/enlaces/figuras iguales, solo Info/XMP temporal/IDs de PDF y created/modified de DOCX distintos; GFM idénticos por bytes. docs/reproducibilidad-report-006-ronda4.json y reproducibilidad-informe-006-ronda4.json. No nueva cifra científica; variables canónicas y espejo idénticos.

## Controles visuales y clics reales

Informe 36 páginas, ocho tablas y cuatro figuras; anexo 149 páginas, 117 paneles y nueve figuras. DOCX: XML completo válido; todas las celdas de tablas contrastadas con trace/body_trace, medios con SHA de fuentes de presentación y 44 bookmarks presentes. Sin shortcodes/citas pendientes. Portadas exactas comprobadas en PDF y DOCX/XML. No se afirma revisión visual nativa Word.

WinRT generó PNG del PDF actual. Se inspeccionaron tres hojas de contacto del principal y diez del anexo, abarcando todas las páginas; muestras ampliadas de figuras/FRED/φ/Motivo. Tras corregir el guion solo cambian píxeles de páginas 34–35 del principal, reinspeccionadas ampliadas. Las otras 34 y las 149 del anexo son idénticas a las revisadas, comprobado por SHA. Figuras y columnas sin recorte observado; tablas continúan con cabecera. Nota φ visible p56, Motivo p37; referencias p34–35 y estrés p27–28. No se afirma lectura visual de cada cifra: su correspondencia es automatizada.

Edge 155 aislado, entradas reales por CDP: 53/53 y 167/167 clics en marcadores internos, posición verificada con tolerancia de 1 píxel CSS. 55/55 URI: 34 locales a página correcta del slug y 21 navegaciones externas observadas. El fallback entre archivos garantiza página, no coordenada exacta del encabezado; los marcadores internos sí se comprobaron a coordenada. Fuente SHA de cada registro coincide con PDF entregado. Intentos prematuros sin barra/índice listos fallaron antes de los clics y quedan conservados; no se contaron como verificación ni defecto del PDF. Evidencia outputs/preview-006/qa-click-ronda4/ y logs clics-pdf-006-ronda4-congelado-*-listo.log.

Auditores ronda 2 no ejecutaron pytest/reproducibilidad/clics; no pudieron vincular las imágenes previas al PDF por huella. Estos controles son de Codex, no se les atribuyen ni se llaman independientes. Google Docs: importación, URLs, clics y paginación desconocidos; obligatorio para cierre global, sin URLs ficticias ni subida por agente.

## Huellas congeladas

| Ruta absoluta | SHA-256 |
| --- | --- |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf | d1a3460abea1cd9e17ef4a68a8fbd1a8ec1d54b72a75d83ccda1e9af0e06fd0f |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx | a524791b74bea38e0426aba2daa160788a1d0a0c7609f5f7ad1cb37a2c224337 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.md | 94fa5a14c035fb4aec2652e4e83682687ecdef6002815683f7a2e54312a8f0f3 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf | a3e888466c600318fa549bfa0bfc6b19c74379c24b927d491f48a197807e8150 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx | e2a8d81ec8b8ebf41e947577abd87236879c23b9634e21335adde20ac6ed460a |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.md | 4c9ac7f9ca4491fd60332ad6e7110a3c9a97fe73fd6135f3c3ad88b7ce65a1c4 |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/informe/registro.csv | 448cce1ea302fc58e21a7facbe4d3ffc7dbe564ca380f8e0ddafa5f102b3486b |
| C:/Users/gabri/orca/riesgo-credito-macro/outputs/informe/enlaces.csv | a4dc8da3e5ba0d5634a334c170c7b64f897bf8ab607f7c3a89f6c81ddc9f5399 |
| C:/Users/gabri/orca/riesgo-credito-macro/report/_variables.yml | 2695ada1f4769333ae0cc76e59c0db3ca8dc8e5c504ae7087aa506cafe018140 |

T11 técnica revalidada; T12/006 abiertas hasta revisión acotada independiente y Google Docs. 007 solo spec borrador, sin plan/tareas/aprobación; no deck. Sin commit ni push.
