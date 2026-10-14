# Correcciones técnicas de 006 tras auditoría ronda 2

Codex, 13-oct-2026. Copia única: C:/Users/gabri/orca/riesgo-credito-macro. Sin commit ni push. Validación nueva en curso; ninguna comprobación antigua acredita la redacción corregida.

## Identidad y coordinación

Los cuatro PDF/DOCX coinciden con los SHA comunicados por la auditoría ronda 2. El contraste inicial contra las 511 rutas del manifiesto ronda 3 solo detectó siete secciones de Claude distintas (02, 04–09); YAML y Markdown generados coincidían. La auditoría identifica la entrega histórica, pero esta no contiene las correcciones nuevas. No se utiliza la fecha de modificación como prueba. Aquella entrega queda en `outputs/preview-006-ronda3-evidencia/`; paquete en `docs/paquete-auditoria-006-ronda3-preservada.md`.

Claude confirmó cesión exclusiva y pausa de 007; sus nueve SHA están en `docs/cesion-y-reparto-006-ronda4.json`. Codex no edita sus secciones. No se ejecutó test, pipeline ni render antes de la cesión.

## Reparto de hallazgos

- Claude: E-N1/E-N2/E-N4/E-N5/E-N6/E-N8–E-N12, P-2.5, prosa interna de 01/02/03f/04–09 y sufijos duplicados alrededor de slugs. Correcciones y alcance en el anexo de `review-audit-ronda2.md`. La lectura cualitativa de 07 es del autor de la sección y se contrasta con trayectorias y coeficientes; no se implementa descomposición numérica.
- Codex: E-N3/P-N1/P-N4/P-N5/P-N6/P-N8/P-I4/P-M2/P-11/V-N1–V-N3; KPSS, títulos/columnas/notas, APA/nota FRED, remisiones/estilo de enlaces, gráficos derivados y 03a–e/10/11. Ningún archivo tiene dos escritores.
- Autor/profesor: Google Docs y condiciones de entrega. Portada 16-oct permanece autorizada.

## Correcciones y trazabilidad

KPSS exacto 0.1 sigue siendo 0,100 sin límite documentado. Límites explícitos CSV/Markdown se uniforman a ≥ 0,10 y ≤ 0,01: cotas respaldadas tanto por límites estrictos como no estrictos, no valores exactos. Operadores originales y SHA de censura permanecen en la traza. Nota KPSS solo en paneles con campos KPSS.

Tabla 1 incorpora signos, sin reutilizar las cinco lecturas dudosas: conserva — cuando no hay signo permitido. Diagnósticos muestran estadístico, p y veredicto; VIF traducido, sin fabricar p. Anexos conservan todas las filas y columnas.

Modelo II PIB(t−1): `modelo2.coef.gdp_l1.{coef,ee,p,ic_inf,ic_sup}` = 0,001 / 0,005 / 0,823 / −0,009 / 0,011. Claves existentes de YAML y CSV aprobados, entregadas a Claude sin estimar ni crear cifras nuevas.

Fuentes de figuras permanecen dentro del PNG; se retira su repetición en la leyenda. Estrés usa derivados `outputs/informe/stress_model*_presentacion.png` desde CSV aprobados: adverso continuo rojo, D discontinuo con círculos, mismos puntos. Registro conserva origen científico/SHA y añade origen de presentación/SHA. Coincidencia anotada solo cuando los valores coinciden.

Enlaces PDF azules y subrayados; DOCX estilo Hyperlink subrayado. Letras repetidas retiradas por el propietario de cada sección; destinos por slug y fallback de página conservados.

APA: U.S./Malaysia y mayúscula tras dos puntos; títulos institucionales en oración; nota FRED antes de URL, códigos y fecha intactos. Newey–West 703–708 corroborado el 13-oct en [publicaciones del coautor](https://users.ssc.wisc.edu/~kdwest/publications/publications.htm) y [artículo](https://users.ssc.wisc.edu/~behansen/718/NeweyWest1987.pdf). Sin referencias o atribuciones nuevas.

## Evidencia inicial antes de congelar (antecedente)

Regresiones primero en rojo: `pytest-006-ronda4-rojo.log`, `...figura-rojo.log`, `...enlaces-rojo.log`. Focalizados iniciales 69 verdes; no sustituyen suite completa. Render editorial inicial falló por una variable local que ocultaba el YAML al generar PNG; corregida y cubierta por test aislado de interfaz, YAML y PNG original intactos. Ese fallo no es una entrega válida.

Suite íntegra, render final y repetido, SHA, XML/tablas, visual actual y clics reales deben completarse antes del nuevo veredicto. Auditores anteriores no ejecutaron estos controles. Google Docs sin importación/URLs/clics confirmados, obligatorio para cierre global.

## Estado vigente al congelar

Los controles técnicos anteriores se completaron: suite final 949 passed, 567 warnings, 1108,12 s, rc0, sin exclusiones y fuentes estables. Primer ciclo 948 conservado pre-guion; no acredita el filtro final. El guion duplicado de títulos se corrigió solo en presentación y quedó cubierto primero en rojo; no cambió BibTeX ni DOI.

Report ×2: 208 productos idénticos. Dos renders de contenido idéntico (PDF/DOCX solo metadatos temporales; GFM exacto). 116 protegidos y 25 módulos científicos intactos. PDF actual 36/149 páginas; DOCX ocho tablas/117 paneles y figuras contrastados con sus trazas. Contactos de todas las páginas inspeccionados; tras el guion solo cambian páginas 34–35 del principal, reinspeccionadas. Las otras 34 y las 149 del anexo coinciden por SHA de píxeles. φ p56 y Motivo p37 visibles. No se afirma lectura visual de cada cifra ni paginación nativa Word.

PDF congelados: 53/53 y 167/167 clics internos, 55/55 URI (34 locales a página del slug y 21 navegaciones externas). Primeros intentos del índice fallaron antes de estar lista la barra del visor; conservados, no contados. Reintentos con visor listo verificados sobre SHA entregados. Sin afirmar acceso completo a artículos, coordenada exacta del encabezado en enlace entre archivos, ni clics en Word/Google Docs.

Validación vigente: `specs/006-informe/review-validate-ronda4.md`. La lista única de pendientes de cierre y la cesión para auditoría están en `docs/paquete-auditoria-006-2026-10-12.md`; reemplazan la lista inicial. T12/006 abiertas. Sin commit/push ni ampliación contractual.
