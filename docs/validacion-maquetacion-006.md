# Validación técnica y maquetación de 006

## Contrato y estado

Copia activa: `C:/Users/gabri/orca/riesgo-credito-macro`. Tareas v2 aprobadas por el autor el 12-oct-2026, SHA-256 `49b874d1a1170c57a7f3b4560c4b3e10fc8cc5261bae6b610e4fb275fd71a05f`. Antes de ejecutar se detectó otra huella: correspondía exclusivamente a un ajuste posterior del párrafo de cierre técnico. Codex restauró el párrafo anterior y comprobó la coincidencia exacta con la huella aprobada. Spec y plan aprobados no se editaron.

005 permanece cerrada: validación y auditoría independiente de ronda 3 aprobadas, T10 completa y seis huellas actuales coincidentes con `specs/005-estres/review-audit.md`. No se repitieron sus pruebas por esta comprobación.

## T1 — sincronización y controles

Autor de implementación y validación técnica: Codex. Claude confirmó turno exclusivo de Codex y permanece en lectura hasta el relevo de T3.

- Tests primero: `uv run pytest -q tests/test_report.py` produjo 18 fallos y 2 aciertos. Detectó funciones ausentes, etapa provisional, gancho ausente y controles que no recorrían secciones/anexos.
- Después: `uv run pytest -q tests/test_report.py tests/test_harness.py`: 31 aprobados, 7,59 s.
- La etapa `report` valida el YAML canónico, conserva sus bytes y regenera el espejo raíz; la comparación SHA-256 falla ante corrupción posterior a la escritura. Se prueban CRLF, Unicode, fuente inválida, espejo obsoleto e idempotencia.
- El gancho Quarto ejecuta `uv run python -m src.pipeline report`, sin llamadas recursivas a Quarto. `.gitignore` excluye exclusivamente el espejo raíz; `report/_variables.yml` sigue siendo canónico.
- Los guardarraíles recorren todos los `.qmd` de `report/`, incluidos secciones y anexos. Los negativos comprueban cifra decimal tecleada, cita inexistente, pendiente de lectura y descartada.
- La skill compartida cambia únicamente la línea de ubicación del proyecto Quarto autorizada por el plan §8.

Suite completa de T1: `uv run pytest -q`, 857 aprobados, 567 advertencias, 944,11 s, código 0. T1 completa. El humo incluye una variable, una tabla aprobada, una figura y una cita APA. Su tabla ancha conserva el problema visual ya identificado; T2 debe resolverlo mediante salidas de presentación nuevas, sin editar los originales.

Los renders definitivos de T1 a PDF y DOCX terminaron con código 0 y ejecutaron el gancho. El DOCX contiene la variable resuelta, cita Newey/West, tabla y figura; no quedan shortcodes. El PDF se convirtió a cuatro imágenes con el motor instalado de Windows, sin añadir dependencias. La inspección de la primera página confirma la anchura insuficiente de la tabla original.

Comprobación de herramienta para T2: Word está instalado, pero un intento COM de exportar el DOCX, abierto en lectura, no produjo PDF después de más de tres minutos. Se detuvieron únicamente la instancia y el auxiliar creados por esa prueba; no se modificó el DOCX. Su paginación visual sigue pendiente: el XML y el render Quarto no la sustituyen. No se da por aprobada G1 con esta evidencia parcial.

## Preservación y siguiente acción

El inventario previo de 97 archivos protegidos está en `docs/validacion-maquetacion-006.json`: raw, panel, salidas y variables canónicas. Los renders nuevos no autorizan modificaciones de resultados aprobados.

Siguiente acción: completar T1, después T2 → T3 → solicitud de Claude → T4 → G1. La puerta G1 exige PDF y Word legibles, anexos completos e interfaz generada con trazabilidad. Sin redacción antes de G1 y T10; sin commit ni push.

## T2 — entrega técnica en validación

Tests primero: siete fallos por adaptador ausente y salidas derivadas inexistentes. Después, la regresión CRLF detectó una huella normalizada incorrecta; se corrigió leyendo bytes antes de decodificar. Última comprobación focalizada: 40 aprobados, 9,83 s. Incluye comprobación independiente de cada celda Markdown contra su CSV, tolerancia exclusivamente por el redondeo declarado, textos completos, escapes, trimestres, filas y columnas.

Se generan `outputs/informe/*.md`, `outputs/informe/trace.json` y `report/anexos/tablas.qmd`, exclusivamente desde los CSV aprobados. La matriz de trazabilidad identifica cada columna original y su panel. El CSV conserva toda la precisión; la presentación declara tres decimales y advierte que un cero redondeado no es exactamente nulo. Los anexos conservan todas las filas y columnas, en el orden original, con cabeceras repetidas y paneles estrechos; no se cambiaron formatos ni se usaron páginas apaisadas.

Renders T2: `outputs/smoke-006/report/informe.pdf` (115 páginas) y `informe.docx` (107 tablas, 2758 filas incluyendo cabeceras). Las 107 tablas DOCX tienen `w:tblHeader`; sus celdas coinciden con la matriz generada, sin discrepancias. Los 33 SHA de fuentes corresponden a los bytes reales. El inventario de 97 archivos protegidos sigue intacto.

Revisión PDF: las 115 páginas se renderizaron con Windows.Data.Pdf, sin dependencias nuevas, en `outputs/smoke-006/report/pdf-pages/`; hojas de contacto `contact-001.png` a `contact-109.png`. Se inspeccionó la continuidad de todas las páginas y se comprobó que la tabla principal ya no presenta el solapamiento del humo anterior. La inspección visual de Word todavía no se ha realizado: tampoco funcionó un arranque seguro de la instancia propia y no expuso una ventana accesible ni sesión COM. Se cerró únicamente ese proceso propio. No se infiere legibilidad de Word a partir del XML o del PDF de Typst.

T2 completa con la excepción operativa siguiente: suite completa 864 aprobados, 567 advertencias, 1136,34 s, código 0. Dos ejecuciones reales de `report` conservaron idénticos los 141 derivados de tablas/anexos. Los 97 archivos iniciales y tres fuentes Fed contrastadas con sus huellas aprobadas están intactos. La revisión visual del DOCX queda para G1. No se instala ningún renderizador nuevo ni se sube el documento a servicios externos.

## Decisión del autor sobre la herramienta de revisión

El 12-oct, en la sesión de Claude, el autor informó que no dispone de Word por un problema de licencia estudiantil y pidió generar el documento para revisarlo después en Google Docs. Claude comunicó la decisión para el relevo de Codex; su respuesta figura en la sesión de coordinación a las 10:53. Se conserva tasks v2 y se registra esta excepción operativa autorizada: generación DOCX y comprobación estructural por Codex, revisión visual manual del autor en Google Docs en G1. No se declara realizada una inspección nativa de Word ni se relajan cobertura, anexos o correspondencia con CSV.

Google Docs puede modificar espaciados, cabeceras y saltos respecto de Word. La revisión manual no garantiza el aspecto exacto en Word; si el profesor exige ese motor, será necesario comprobarlo con una sesión disponible. El PDF continúa como formato principal. Esta limitación se presenta con G1 y no autoriza subir archivos desde un agente.

Prioridad de revisión en Google Docs: tabla de coeficientes del Modelo I; paneles de notas largas de robustez del Modelo I; limitaciones del Modelo II; siete paneles de niveles de estrés; último panel de sensibilidad de tasa. Comprobar todas las filas/columnas, texto completo, continuidad y cabeceras al cambiar de página. Los demás anexos se revisan completos, sin limitar la revisión a esta lista prioritaria.

## T3 — esqueleto e interfaz, completa

Cinco tests nuevos fallaron antes de implementar: generador ausente, interfaz no generada y esqueleto incompleto. Codex implementó el generador puro y su integración, creó solo sus siete archivos de sección y cambió `informe.qmd` a YAML e inclusiones. El fixture de T2 se conserva en `outputs/smoke-006/fixture-t2.qmd`.

Los archivos asignados a Claude todavía no se escribieron por Codex. Se le cederá un turno exclusivo para sus encabezados, sin prosa; después devolverá el checkout y Codex comprobará la estructura completa y la suite. La interfaz se genera desde la fuente canónica y las huellas reales de tablas, figuras, panel y manifiesto; no inventa unidades ni sintaxis de índices de listas.

Claude recibió y devolvió el turno exclusivo: creó sus nueve archivos con solo encabezados y marcadores. Codex comprobó las 11 secciones, 14 subsecciones y 16 inclusiones de archivos; 3.5 figura una vez. Una regresión detectó que el guardarraíl confundía numeración de subsecciones con cifras; se corrigió excluyendo únicamente prefijos de encabezados definidos por la guía, sin excluir cifras en el texto de esos encabezados. Otra regresión exigió un mapa separado de claves heredadas y grupos pendientes en la interfaz.

Últimos focalizados: 46 aprobados, 4,09 s. Suite final: 872 aprobados, 567 advertencias, 927,38 s, código 0. La primera suite de T3 fue detenida antes de concluir para cubrir la interfaz completa y no se cuenta como validación aprobada. Interfaz: 871 entradas canónicas, 219 activos y nueve figuras; todos los enlaces locales y huellas comprobados. PDF y DOCX del esqueleto generan, sin prosa central ni referencias sin resolver. Siguiente acción: turno de Claude limitado a su solicitud, luego T4.

## T4 — bloqueo de delimitación de la URL FRED

`src/references.py:555` aplica el contrato de 002: la URL de verificación de la matriz coincide exactamente con la URL institucional del BibTeX cuando no hay DOI. `tests/test_literature_files.py:63` exige esa coherencia. El plan 006 permite cambiar la URL de `fred2026` en el BibTeX; tasks v2 no incluye `research/matriz-literatura.md` entre los archivos de T4. Cambiar únicamente el BibTeX incumple el guardarraíl vigente. No se modifica ni se debilita ese test.

Propuesta concreta pendiente de autorización, sin cambios de metodología o de estados de estudios:

- En `report/references.bib`, entrada `fred2026`, campo `url`: sustituir `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DRALACBS` por `https://fred.stlouisfed.org/`.
- En `research/matriz-literatura.md`, exclusivamente fila `fred2026`, columna `URL de verificación`: la misma sustitución. Conservar nota, códigos, fecha, hallazgo, estado y todas las demás filas.
- Ampliar la delimitación de T4 solo para esa celda de la matriz; no editar specs/planes ni corregir observaciones opcionales de 002. Después ejecutar `scripts/verify_refs.py` y la validación completa.

La comprobación en memoria reproduce el fallo cuando cambia solo el BibTeX y mantiene la coherencia cuando ambas URLs coinciden; los archivos reales se conservan mientras falta autorización. El sitio institucional fue consultado en modo lectura el 12-oct: [FRED](https://fred.stlouisfed.org/). El resto de T4 puede continuar con fuentes congeladas, sin reestimaciones.

## T4 — cierre técnico y entrega G1, 12-oct-2026

El autor autorizó explícitamente la celda adicional de FRED. Se sustituyó únicamente la URL en `fred2026` del BibTeX y de la matriz por `https://fred.stlouisfed.org/`. La sustitución inversa reproduce exactamente las huellas previas de ambos archivos: ningún otro byte cambió. No se modificaron contratos, estados de literatura ni observaciones opcionales.

Tests primero para los generadores y negativos de T4. Suite completa final: **877 passed, 567 warnings, 1016,73 s, código 0**. Tras sincronizar las URLs, **58 focalizados aprobados, 10,15 s**. `uv run python scripts/verify_refs.py`: **21/21 referencias verificadas, código 0**. No se repite la suite por las notas posteriores. Dos corridas de `report`: **150 productos idénticos**; **99 archivos protegidos intactos**. El archivo canónico cambia solo por las nuevas claves de 006 y `datos.n_series`; los bloques `modelo1`, `modelo2`, `estres` y las demás claves de `datos` conservan sus valores. Spec y plan aprobados conservan sus huellas.

Decisiones de fuentes: 13 códigos distintos del manifiesto, sin confundirlos con regresores; historia desde 1998T1; literatura 17 estudios verificados, 8 pendientes, 3 descartados y 4 datos/método verificados. Tabla de literatura con variables/métodos literales y notas para los signos no reutilizados. P05/P95 desde columnas exportadas; D contiene siete alzas y seis ceros, con fechas de proyección diferenciadas del episodio histórico. C2 no exporta χ²/p específicos: no se calculan ni añaden aliases a 004. Detalle de respuesta en `specs/006-informe/solicitudes-codex.md`; inventario actualizado en `interfaz.md`.

Maqueta principal: `outputs/smoke-006/report/informe.pdf` (122 páginas) y `informe.docx` (109 tablas, 2800 filas, cero discrepancias). Los 34 CSV conservan todas sus filas y columnas en anexos; revisión de contactos de todas las páginas y detalle de literatura en páginas 7/10. La maqueta contiene encabezados pendientes de redacción: no es el informe final.

Las nueve figuras aprobadas se entregan también en `outputs/smoke-006/figuras.pdf` y `figuras.docx`, separadas del esqueleto para no introducir prosa antes de G1. PDF de nueve páginas inspeccionado completo; cada imagen corresponde a los bytes originales de `outputs/figures/`. Este cuaderno de QA se genera desde `figuras.qmd`: Quarto genera el `.typ`; el binario Typst instalado lo compila con `--root C:/Users/gabri/orca/riesgo-credito-macro`. Quarto aislado en `outputs/` restringe las imágenes externas a su carpeta, por eso ese ajuste explícito es necesario. No afecta al render del proyecto principal ni requiere dependencias. Comando: `"C:/Program Files/Quarto/bin/tools/x86_64/typst.exe" compile --root "C:/Users/gabri/orca/riesgo-credito-macro" outputs/smoke-006/figuras.typ outputs/smoke-006/figuras.pdf`.

El autor confirmó directamente que no tiene licencia Word y usará Google Docs. El DOCX se comprobó estructuralmente; **no se afirma paginación visual nativa de Word verificada**. La revisión manual en Google Docs pertenece a G1. Ningún agente subió documentos. Los cambios editoriales realizados allí deberán trasladarse a los `.qmd` y regenerarse para mantener fuentes reproducibles y variables canónicas.

### Lista única de pendientes actuales

1. **G1 del autor:** revisar PDF y ambos DOCX en Google Docs, incluidos todos los anexos y figuras, y aceptar la maquetación o señalar correcciones. No se considera aprobado por el reset de cuota ni por tests verdes.
2. Tras G1: T10 de Codex → T5–T9 de Claude, con turnos exclusivos. Siguen pendientes redacción e integración; ninguna estimación nueva.
3. T11: validación integral del informe redactado. T12: auditorías con revisores independientes de los autores. 006 sigue abierta; 005 está cerrada.

No quedan bloqueos técnicos de la URL FRED. C2 sin estadístico separado, entrenamiento no exportado y equivalente en dólares se explican como límites de fuentes, sin ampliar el contrato. Fecha/hora oficiales del profesor siguen por confirmar según la spec. Sin commit ni push.
