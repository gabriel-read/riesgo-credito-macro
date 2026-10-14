VEREDICTO: APROBADO

# T11 — Validación técnica del autor, ronda 3

Codex, 13-oct-2026. Copia exclusiva C:/Users/gabri/orca/riesgo-credito-macro; rama spec/004-modelo-ii, HEAD 7a3dd2ad76bf09a8401534679e4311400fb3a4aa. Esta aprobación acredita los archivos de la tabla siguiente y habilita la auditoría independiente de ronda 2. No cierra 006 ni acredita Google Docs.

## Correcciones y autoría

- Claude conservó la versión actual de 07 por autorización del autor y corrigió únicamente el párrafo sin respaldo de descomposición. SHA completo: b4c305b74d4c3dfcac0ce90531b86c297b2276344326772e8ce1ca57b6d66b42. Los otros ocho prefijos comunicados coinciden; no se restauraron versiones históricas ni se sobrescribieron sus secciones.
- Codex completó portada con title conservado, subtitle «NEG-LIF309-01 Control y gestión de riesgos · Profesor: Ramfis Félix Tatis», author «Gabriel Read», affiliation «Instituto Tecnológico de Santo Domingo (INTEC)» y date «16 de octubre de 2026». PDF inspeccionado visualmente; ambos DOCX tienen esos textos en orden y todas sus partes XML/REL son válidas. Un adaptador conserva la fecha literal frente a Invalid Date de Quarto; no se inventó ningún campo.
- C4: numeric KPSS 0.1 permanece 0,100 sin evidencia de censura. stationarity usa su campo kpss_p_truncado; Modelo I conserva ≥/≤ y Modelo II >/< desde su Markdown aprobado, verificando identidad, endpoint y SHA de esa fuente. Un exacto no se convierte en censurado. p menores a 0,001 se muestran < 0,001; los restantes mantienen precisión declarada. Primero nueve regresiones rojas, luego verdes; no se modificaron CSV/MD científicos.
- C8: FRED mantiene @misc admitido, pero la presentación CSL es de datos con consulta 2-oct-2026 y sus trece códigos. Newey–West 703–708, números FMI 2006/283 y 2011/161, editorial Fed omitida solo cuando coincide con el autor institucional, metadata original conservada. Procedencia: docs/procedencia-presentacion-apa-006-ronda2.md. No nuevas citas.
- Subtítulos, sección 11, notas y remisiones propias: sin textos de borrador ni mensajes internos del producto; se retiró la duplicación «Abrir anexo DOCX». Una remisión por slug se adapta al formato; los anexos no se recortaron.
- I3 autorizado: las ecuaciones transcriben 003 «Ecuación» y 004 «Ecuación»/«Proyecciones locales». Modelo I: Y y su rezago, PIB/ΔU/π/ΔFFR contemporáneos, CRED(t−4) y dummies; Modelo II: ΔDR y su rezago, ΔFFR(t−j), controles macro t−1 y CRED(t−4); LP: las dos dependientes acumuladas y Z con controles y tasa rezagados. Notación y transformaciones contrastadas; líneas divididas para respetar márgenes, sin nueva metodología ni estimación.
- Enlaces PDF: el lector Edge intenta resolver un nameddest externo en el documento de origen. Se conserva el nombre estable y se añade &page=N, calculado desde los destinos nativos del anexo actual. Enteros, sin inferir páginas ni URLs de nube. Primero regresión roja; prueba de clic detectó que 17.0 se trataba como dominio y se corrigió el formato entero. En Edge el respaldo abre la página correspondiente; no se afirma un salto exacto a la coordenada del encabezado entre documentos. Los marcadores dentro del anexo sí se verificaron por coordenada, con tolerancia de un píxel tras el ajuste observado del separador del visor.

## Suite, render y conservación

uv run pytest -q completo: **940 passed, 567 warnings, 1198,52 s, rc0**, sin exclusiones. Fuente antes/después idéntica durante la corrida; log y SHA en docs/pytest-completo-006-ronda3.log/json. 63 focalizados verdes. Las dos corridas interrumpidas anteriores son antecedentes pre-respaldo-enlaces y pre-ecuaciones: no se presentan como aprobadas ni sustituyen la suite completa.

Principal: 34 páginas, ocho tablas, tres PNG originales. Anexo: 152 páginas, 117 paneles, nueve PNG originales y 44 destinos registrados. Cada fila/celda de los DOCX se contrastó con trace/body_trace y las fuentes; figuras originales por SHA; sin marcadores sin resolver. Portada, tablas, ecuaciones y anexos revisados. Los 152 PNG de páginas finales del anexo coinciden byte a byte con los ya inspeccionados; los trece cambios de página del principal se revisaron con las hojas de contacto actuales. Phi sigue visible en p58 y Motivo explicado en p38.

Report ×2: **206 archivos idénticos**, antes y después. Render PDF/DOCX/GFM repetido en outputs/repro-006-ronda3: objetos de texto/fuentes/imágenes/enlaces idénticos; diferencias solo CreationDate/ModDate y fechas/IDs XMP de PDF, y created/modified de docProps/core.xml de DOCX. Ambos GFM idénticos por bytes. 116 archivos protegidos conservan SHA; variables canónicas y fuente espejo iguales. No cambia ninguna cifra científica ni estimador, spec o plan aprobado.

Clics actuales: **53/53** índice principal, **167/167** índice anexo y **52/52** URI únicos, de ellos 31 enlaces locales a la página de su slug y 21 externos. Se conserva el primer intento y el reintento FRED; el fallo de captura inicial no fue un cambio del archivo. Navegación externa comprobada no equivale a acceso al artículo: CAPTCHA/403, redirecciones y respuestas no confirmadas no se presentan como lectura completa. Los 31 URI locales coinciden exactamente con enlaces.csv; DOCX se comprueba estructuralmente, no por clic nativo.

Evidencia: docs/qa-correcciones-006-ronda3.json; docs/reproducibilidad-report-006-ronda3.json; docs/reproducibilidad-informe-006-ronda3.json; docs/comparacion-visual-006-ronda3.json; outputs/preview-006/qa-click-ronda3/; logs render-006-ronda3-validada*, render-006-ronda3-principal-enlace-entero.log y render-006-ronda3-gfm-enlace-entero.log. Los ensayos pre-fecha y previos de maquetación se conservan, pero no acreditan estos bytes. Las rondas anteriores y maqueta 122 permanecen.

## Versión validada

| Archivo absoluto | SHA-256 |
|---|---|
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.pdf` | `97c614ac758bed6b6f38e42deeac965277a11f8bbb5d9744d10fc8bcbc1042d7` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.docx` | `8d212275b52d3ece6b30255433fdab65e2323f8272ed486dc1c404f040393520` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/informe.md` | `c2472cdcc9067f12510eebfa58a5ce68a1b6ee8b14dbac4724b0aa762f202fdc` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.pdf` | `b69f250d36f2172c9f4944ad55a15f0feb3c33389602b9287795a82bad2a21fe` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.docx` | `136fb3c808b3bf4a607be5bc3bb008928387b84a1f95d3a25fa570f1433ab274` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/preview-006/report/anexo-tecnico.md` | `b2cb71ff2595e28bbbd42d061631a2059a87c7b534c5fea55977999b19d3f10e` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/informe/registro.csv` | `b821cd51730cac46e849da7f5099cfdf6a603faf99dbe7b2a20e9dedc31d9fc0` |
| `C:/Users/gabri/orca/riesgo-credito-macro/outputs/informe/enlaces.csv` | `3fc5380f9cf83fa38e9c009aa25a270cfdba168b23244348ad0d700aebac5e0d` |
| `C:/Users/gabri/orca/riesgo-credito-macro/report/_variables.yml` | `2695ada1f4769333ae0cc76e59c0db3ca8dc8e5c504ae7087aa506cafe018140` |

## Pendientes únicos y siguiente acción

1. Auditoría independiente de 006 ronda 2, coordinada por Claude con revisores limpios, sobre este paquete. T12 y cierre global abiertos; la validación del autor no la sustituye.
2. Google Docs obligatorio por RF-14b: importación/URLs y navegación/legibilidad sin verificar. Requiere acción del autor conforme a docs/revision-google-docs-006.md; ningún agente sube archivos. No afirmar paginación o clics Word nativo.
3. Confirmaciones del profesor sobre hora/formato/extensión y aceptación de documentos separados; la fecha de portada autorizada no confirma el plazo oficial.
4. 007: solo spec.md en borrador. Sin aprobación, plan, tareas ni deck; duración/número de láminas propuestos, pendientes. Aprobar spec y preparar/aprobar plan y tareas antes de implementar.

Sin commit ni push. 005 sigue cerrada con sus dos aprobaciones; no se reabre por esta presentación. Los nueve opcionales de 005 y la descomposición opcional del estrés no se implementan.
