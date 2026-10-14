# Presentación APA de 006: procedencia y alcance

Codex, 12-oct-2026. Correcciones C6/C8/C10 autorizadas; sin modificar contratos científicos, matriz de literatura, fuentes congeladas ni estimadores.

## Referencias

- CSL base: APA Style 7th edition, versión de 7-feb-2026, fuente `https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl`, SHA-256 original `3917def5fc951b104d64216c3373096042368b9704ba269ca83c14ebaba889fc`, licencia CC BY-SA 3.0 y autores conservados. `report/apa.csl` tiene una adaptación local anunciada: fecha de consulta y nota de códigos en referencias de datos, denominación española y raya de rango de páginas. Su huella vigente se registra en el paquete, no se presenta como idéntico al archivo oficial.
- `report/filters/apa-references.lua` modifica solo referencias de presentación antes de citeproc. Mantiene FRED como `@misc` en el BibTeX, como exige 002, y lo presenta como datos en CSL. La institución de la Fed se conserva en `@techreport`; el editor se omite en la presentación únicamente si coincide exactamente con el único autor institucional literal. No se eliminan instituciones distintas ni autores personales.
- API de referencias en Pandoc: `https://pandoc.org/lua-filters.html#pandoc.utils.references`. No añade librerías ni modifica registros originales para superar el validador.
- Newey–West: rango 703–708 corroborado en la página del autor `https://users.ssc.wisc.edu/~kdwest/publications/publications.htm` y el artículo `https://users.ssc.wisc.edu/~behansen/718/NeweyWest1987.pdf`. No se completó de memoria.
- Números FMI: Nkusu, WP/11/161, `https://www.imf.org/external/pubs/ft/wp/2011/wp11161.pdf`; Segoviano, 06/283, `https://www.imf.org/en/publications/fssa/analytical-work-on-financial-stability`. Solo metadata de referencias existentes, sin nuevas atribuciones científicas.
- Títulos de artículos en forma de oración y delimitadores de páginas normalizados para presentación; DOI, claves, autores y años conservados. `scripts/verify_refs.py` verificó 21/21 tras las correcciones finales de BibTeX.

## Portada y DOCX

`report/templates/typst-template.typ` deriva de la plantilla instalada de Quarto 1.10.19; separa la portada del índice, usa título centrado y en negrita, institución en peso normal y numeración superior derecha. `report/templates/apa-reference.docx` deriva del documento de referencia incluido en Pandoc 3.10: estilos de portada, tamaño carta, márgenes y encabezado de número de página.

Al reutilizar una relación de encabezado con prefijo `ns0`, Pandoc produjo un DOCX con un prefijo sin declaración. Se conservó el diagnóstico, se añadieron regresiones antes de reparar y se normalizaron los namespaces del documento de referencia. Un DOCX mínimo real posterior se analizó íntegramente: 17 partes XML válidas. El análisis de XML completo de los entregables sigue siendo obligatorio; este humo no acredita legibilidad en Google Docs.

Actualización 13-oct: el autor proporcionó los campos exactos; C6 está resuelto y comprobado en los PDF/DOCX actuales. El adaptador student-cover.lua preserva la fecha literal frente a la normalización de Quarto. Ver review-validate-ronda3.md; este pendiente histórico queda retirado.

## Tablas y ecuaciones

La numeración de tablas del cuerpo sigue su aparición: literatura, manifiesto, coeficientes, diagnósticos, lectura, comparación, estrés y tablero. Los p-valores pequeños y los límites KPSS se muestran como desigualdades; ninguna cifra científica se altera. Los términos de PIB se rotulan de forma neutral donde el mismo identificador representa PIB real principal o PIB nominal en R4.

Las ecuaciones de `03e-desviaciones.qmd` transcriben 003 §«Ecuación» y 004 §«Ecuación»/«Proyecciones locales», dentro de RF-7 de 006. No agregan regresores, estimadores, restricciones, selección ni descomposición numérica de estrés. No se aplicó un cambio contractual.
