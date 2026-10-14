# Auditoría independiente T12 — spec 006 (ronda 1)

## Veredicto vigente (2026-10-13) — añadido sin modificar lo anterior

**VEREDICTO VIGENTE: APROBADO** (auditoría de la ronda 6 sobre el paquete R7). Se registra `review-audit-ronda6.md` como la auditoría vigente de 006 sobre R7, **confirmado explícitamente por Gabriel en un mensaje del 2026-10-13, posterior a la corrección de registros** («Confirmo la auditoría de ronda 6 sobre R7 como auditoría vigente de 006»). Antes de esa confirmación el registro constaba como pendiente. Todo lo que sigue a esta sección es el registro de la ronda 1 y se conserva sin cambios; también se conservan íntegras las rondas 2 a 6 y las copias literales de cada revisor.

- **Versión auditada:** paquete R7, manifiesto `docs/huellas-paquete-auditoria-006-ronda7.json` (SHA-256 `69003c83a7c6ccbc69c5cbd23bbeeb43bde0b970792f53748df302ca574535e5`); 583 de 583 entradas coinciden; 02 con `01a299dde5591e6e2a344eb6faa122f7380628b8818a892795733b0dc63aac73`; entregables en `outputs/preview-006/report/` con los SHA-256 listados en `review-audit-ronda6.md`.
- **Revisores independientes (contexto limpio):** revisor-econometrico APROBADO, verificador-citas APROBADO, profesor-evaluador APROBADO (95/100 estimado; no es nota del profesor). Informes: `review-audit-ronda6-revisor-econometrico.md`, `review-audit-ronda6-verificador-citas.md`, `review-audit-ronda6-profesor-evaluador.md`.
- **Autoría real y límite de independencia:** Claude Code redactó 01, 02 (incluido el ajuste R5-6), 03f y 04–09 y coordinó la auditoría; **no es independiente de lo que redactó**. La independencia procede de los tres revisores. La suite y la validación técnica (974 passed, rc 0) son de Codex y no son independientes.
- **Observaciones menores no aplicadas por decisión del autor:** R6-1 a R6-5 (cosméticas); no condicionan el veredicto.
- **Google Docs:** el autor expresó la intención de retirarlo como requisito de cierre (2026-10-13); el diff está en `change-google-docs-retirado.md`; **Gabriel lo aprobó en un mensaje del 2026-10-13 posterior a la corrección de registros y está pendiente de aplicar por Codex** (`relevo-codex-change-google-docs.md`). Hasta que Codex lo aplique con copias previas, spec, plan y tasks de 006 siguen sin cambios. No se afirma que los enlaces del DOCX funcionen en Word ni en Google Docs.
- **Lo que este veredicto no cubre:** el ensayo de las preguntas probables (a cargo del autor), las condiciones de entrega que la guía oficial no resuelve (ver abajo), la revisión visual propia de los DOCX y el marcado de T12/006, que no hace esta auditoría.

- **Confirmación del autor:** la auditoría de la ronda 6 sobre R7 es la vigente de 006 por confirmación explícita de Gabriel (2026-10-13). Esto no cierra T12 ni 006.

### Pendiente identificado por separado (sin añadir requisitos)

1. **Ensayo de las preguntas probables** — criterio de finalización de `spec.md` y «Hecho cuando» de T12; lo hace el autor. Estado: pendiente.
2. **Condiciones de entrega no resueltas en la guía oficial** (`docs/guia-profesor.md` solo define las once secciones, la pregunta, los datos y la conclusión esperada): hora límite oficial; extensión; formato exigido del informe; formato y duración de la exposición; aceptación del par informe-anexo separado. Estado: pendientes de confirmación del profesor. La fecha de portada del 16 de octubre de 2026 es decisión del autor y no es la hora límite oficial; el jueves 15 de octubre de 2026 figura en AGENTS.md y en la spec como fecha de entrega, pero la hora límite oficial no está confirmada.
3. **Marcado de T12 y cierre de 006:** lo registran Codex/el autor; esta auditoría no los marca.

Sin commit ni push.

Fecha: 2026-10-12. Coordinador: Claude Code (Sonnet 5.5), por relevo del autor y de Codex. Sin commit ni push.

## Estado

**VEREDICTO DE LA RONDA 1: CAMBIOS NECESARIOS.** Los tres revisores independientes piden cambios. Hay un bloqueante de contenido (6.3) y un bloqueante editorial (aspecto de borrador). 006 permanece **abierta**: faltan además la comprobación funcional en Google Docs (sin verificar, sin importación ni URLs) y las confirmaciones del profesor. No se afirman enlaces de Google Docs funcionales.

## Nota de conservación (añadida tras recuperar los originales)

Los tres mensajes finales originales de los revisores se recuperaron del registro de subagentes de la sesión y se guardaron sin cambios en `review-audit-ronda1-revisor-econometrico.md`, `review-audit-ronda1-verificador-citas.md` y `review-audit-ronda1-profesor-evaluador.md` (cada uno con un comentario inicial de procedencia). **Esos tres archivos son la copia literal; las secciones «Informe íntegro 1–3» de este documento son una transcripción hecha por Claude desde su contexto y no deben presentarse como copia literal verificable.** Ante cualquier diferencia, prevalecen los archivos `review-audit-ronda1-*.md`. Esta ronda 1 se conserva y no se sobrescribe.

## Autoría real

- Claude Code redactó las secciones 1, 2 (incluida 2.5), 3f (continuación de 3.5), 4, 5, 6, 7, 8 y 9. **La coordinación de Claude no es auditoría independiente de esas nueve secciones**; la independencia procede solo de los tres revisores de contexto limpio.
- Codex redactó 3a–3e, 10 y 11 y construyó la infraestructura: anexo A–F, tablas generadas, registro, enlaces, variables, render, portada y subtítulos.
- Los revisores recibieron solo rutas y criterios (`docs/paquete-auditoria-006-2026-10-12.md`), sin conclusión del implementador ni de Claude. No editaron nada.

## Versión auditada (huellas SHA-256 comprobadas por Claude antes y después de la entrega de Codex)

| Archivo (outputs/preview-006/report/) | SHA-256 |
|---|---|
| informe.pdf | 49fcfe2ac7b742f68ae66350746d842833da09668854f1594e066f19bb62e16a |
| anexo-tecnico.pdf | 4db7863782aba0bfe33759177f7652835c41e27db924712bffbe9f574729b6c0 |
| informe.docx | cf5cbf6f0ba7225497218ff279d720a9cee654b88ba213b9964316fb163eead4 |
| anexo-tecnico.docx | 84a675d9e37756ef8950f9fb8106b8c24ace2799f1e9ca7877ba3ffb5f477c75 |

Inventario completo: `docs/huellas-paquete-auditoria-006-2026-10-12.json`. T11 técnica aprobada en `review-validate.md`; suite completa 905 passed, sin exclusiones (evidencia de Codex; el revisor econométrico la reprodujo: 905 pasan, rc=0). La suite no se repitió por este coordinador porque la ronda 1 no cambió artefactos.

## Resumen de veredictos

| Revisor | Veredicto | Bloqueantes |
|---|---|---|
| revisor-econometrico | CAMBIOS NECESARIOS | 1 (6.3) |
| verificador-citas | CAMBIOS NECESARIOS | 0 (2 importantes) |
| profesor-evaluador | CAMBIOS REQUERIDOS (79,5/100) | 2 (B1 borrador, B2 = 6.3) |

## Plan de correcciones (a ejecutar en turno separado, con validación; no incluye opcionales)

Las referencias son a los informes íntegros de abajo. Escritor = autor del archivo.

| Id | Hallazgo | Archivo | Escritor |
|---|---|---|---|
| C1 | 6.3 describe mal términos compartidos y dice que los controles «solo entran al Modelo I»; 6.4 «no depende de un solo modelo»; desempleo (econ. 1; prof. B2) | 06-resultados, 09-conclusiones, 04-modelo1 | Claude |
| C2 | «Anticipar» con variables contemporáneas; declarar simultaneidad (econ. 2) | 09, 08, 04 | Claude |
| C3 | Limitaciones faltantes en cuerpo: tasa cero, R2/R3 Modelo II, PPP y R1 parcial, K condicional (econ. 3; prof. I2) | 05, 04 | Claude |
| C4 | Notación de p-valores en tablas de presentación (econ. 4) | adaptador de tablas | Codex (o Claude con cesión) |
| C5 | Remisiones por slug sin enlace; faltan letras de anexo (econ. 5, 17) | 01, 03f, 07, otras | Claude y Codex |
| C6 | Texto de borrador/interno: subtítulos, portada APA, sección 11, 03f línea 1, «(primera diferencia)» (prof. B1; econ. 11) | informe.qmd, 11, 03f, 04 | Codex y Claude |
| C7 | Tabla 2.5 vs. su texto; M-1 a M-4 de citas (cit. I-1, M-1–M-4) | 02, 01, 08 | Claude |
| C8 | Fecha de consulta FRED y APA (FMI, Newey–West, frb2026) (cit. I-2, M-5) | apa.csl, references.bib | Codex (o Claude con cesión y verificación) |
| C9 | Estrés: asimetría tasa/desempleo y dirección de la inflación; niveles fuera de rango mal rotulados (prof. I1; econ. 9) | 07-estres | Claude (verificar la descomposición del profesor antes) |
| C10 | Ecuaciones (prof. I3), contexto histórico de magnitudes (I5), menores restantes | 03, 05, 06, 07 | según escritor; I3 requiere decidir si es cambio de contrato |

Nota: la descomposición del +1,43 pp del profesor-evaluador es aproximada y no fue verificada por el revisor econométrico; debe contrastarse con `AT-EST-PATHS` antes de modificar la sección 7. Las ecuaciones (I3) pueden exceder el contrato aprobado; si lo hacen, requieren /sdd-change.

## Pendientes externos

- Google Docs: sin importación, sin URLs, sin evidencia. Obligatorio para cierre. Procedimiento: `docs/revision-google-docs-006.md`. Conviene importar solo después de las correcciones, porque el texto cambiará.
- Profesor: fecha/hora oficial, extensión, formato exigido, formato de exposición y aceptación del par separado.
- Acceso CAPTCHA/403 a algunas fuentes (Tandfonline) documentado; no se convirtió en corrección metodológica.
- Diapositivas (spec 007) no evaluables: `report/slides.qmd` no existe.

---

# Informe íntegro 1 — revisor-econometrico

VEREDICTO: CAMBIOS NECESARIOS

**Alcance y condiciones.** Auditor con contexto limpio, solo lectura. Lo que leí:
- Los contratos: constitución, guía, spec 006 v4, plan 006 v3 y las specs 003–005.
- Las 16 fuentes del cuerpo y las 6 del anexo.
- Las tablas de presentación y las tablas y JSON originales.
- Las tres figuras esenciales y el texto de ambos PDF (con `pdftotext`; no pude ver las páginas como imagen porque falta `pdftoppm`).

Las 198 huellas de `docs/huellas-paquete-auditoria-006-2026-10-12.json` coincidían antes y después de mi corrida. `uv run pytest -q` dio 905 pasan, rc=0 (863,6 s). No volví a correr el pipeline porque no se me indicó ninguna etapa. Google Docs sigue sin verificar y no es parte de esta auditoría. Claude redactó las secciones 1, 2, 3f y 4–9, que es donde están casi todos los hallazgos.

## Hallazgos

### Bloqueante

**1. La comparación 6.3 describe mal los modelos, y la discusión 6.4 se apoya en esa descripción falsa.**
- Archivos: `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/06-resultados.qmd:29`, `:46` y `:80`; también `09-conclusiones.qmd:13` y `04-modelo1.qmd:39-40`.
- **Primer error (línea 29).** Dice: «El único término que comparten los dos modelos es el cambio contemporáneo de la tasa». Es falso. Ambos modelos incluyen además CRED(t−4) y ΔDR(t−1). En `outputs/models/model2_main.json`, `credit_l4` es `loans_yoy` con rezago 4. En `model1_main.json`, `credit_growth` es `loans_yoy` y la ecuación usa `credit_lag`.
- **Segundo error (línea 46).** Dice que las demás variables «solo entran al Modelo I». Eso contradice `05-modelo2.qmd:12` («los controles del Modelo I») y `outputs/tables/model2_coefficients.csv`.
- **Contradicción interna (línea 80).** El texto afirma que la inflación y el crédito «no dependen de un solo modelo». Según la propia sección 6.3, solo estarían en el Modelo I.
- **Lectura selectiva del desempleo.** En el Modelo II, ΔU(t−1) = 0,110 (p = 0,039), π(t−1) = 0,024 (p = 0,015) y CRED(t−4) = 0,007 (p = 0,009). El informe usa implícitamente los dos últimos para hablar de estabilidad. Pero en 6.4 y en la sección 9 sigue diciendo que el desempleo «no se distingue de cero».
- **Por qué importa.** La 6.3 es la sección que la guía evalúa como comparación (RF-8). La respuesta a la pregunta fundamental se apoya en una afirmación que el propio texto contradice.
- **Qué se espera.** Describir bien los términos compartidos y los controles rezagados del Modelo II. Después, una de dos:
  - declarar que los controles del Modelo II no se interpretan porque no tienen hipótesis de signo (`specs/004-modelo-ii/spec.md:87`) y quitar «no dependen de un solo modelo»; o
  - interpretarlos todos de forma simétrica, incluido ΔU(t−1).

### Importantes

**2. Las conclusiones dicen «anticipar» con variables que son contemporáneas.**
- Archivos: `09-conclusiones.qmd:30`, `08-implicaciones.qmd:11`, `:14` y `:48-49` (tablero).
- La conclusión recomienda «para anticipar» vigilar la inflación y la actividad acumulada. En el Modelo I ambas entran en el mismo trimestre que la morosidad.
- Contradice a `04-modelo1.qmd:89`, que limita la anticipación al crédito por su rezago de cuatro trimestres.
- Además, `outputs/tables/model1_limitations.csv` declara «Simultaneidad de los regresores contemporáneos» (PIB, desempleo, inflación y ΔFFR se determinan junto con la morosidad). El cuerpo no lo declara.
- **Por qué importa.** La sección 9 debe decir cómo anticipar el riesgo. Hoy recomienda señales que el diseño no permite tratar como anticipadas.
- **Qué se espera.** Reservar «anticipa» para CRED(t−4). Presentar inflación y actividad como indicadores coincidentes. Declarar la simultaneidad en 3.5 o en la sección 4.

**3. Faltan limitaciones aprobadas en el cuerpo (criterio 2 y RF-6).**
- **Tramos de tasa cero y robustez del Modelo II.** Corresponde a `05-modelo2.qmd`, que no los menciona.
  - En 2009T1–2015T4 y 2020T2–2022T1 la ΔFFR casi no varía (`model2_limitations.csv`, «Tramos de tasa cero»). Eso reduce la potencia del resultado «sin evidencia».
  - Las robusteces R2 (sin 2020–2021) y R3 (sin tasa cero, n = 69) del Modelo II no se reportan en el cuerpo, aunque confirman el resultado (`model2_robustness_summary.csv`: 0 de 2).
- **Efectos base sin dummy y R1 parcial.** Corresponde a `04-modelo1.qmd:48-53`.
  - El crédito del programa PPP entra en CRED(t−4) en 2021T2–2022T1 y el rebote del PIB tampoco lleva dummy (`model1_limitations.csv`).
  - La spec exige decir que R1 es un contraste parcial: su nota toma Y(t−1) y CRED(t−4) de trimestres excluidos. El cuerpo solo dice «una muestra sin la pandemia».
  - Esto afecta justo al hallazgo central sobre el crédito.
- **Otros límites del anexo que no aparecen en el cuerpo:** la inferencia condicional al K elegido y las ventanas de las proyecciones locales que cruzan la COVID sin dummy.
- **Qué se espera.** Una o dos frases por punto, con remisión a `AT-M2-LIMITATIONS`, `AT-M2-ROBUSTNESS-SUMMARY` y `AT-M1-LIMITATIONS`.

**4. Las tablas de presentación pierden la notación aprobada de los p-valores.**
- Ejemplos:
  - `outputs/informe/model1_stationarity_anexo_3.md` y `model2_stationarity_anexo_3.md` muestran «p KPSS 0,100». Las tablas aprobadas dicen «≥ 0,10» (003) y «> 0,10» (004), como exige el RF-21 de la spec 004.
  - `model1_diagnostics_cuerpo.md` muestra «Chow 2008T3 0,001» (el valor real es 0,00076). El texto de `04-modelo1.qmd:63` dice «< 0,001».
  - `model1_coefficients_cuerpo.md` muestra p = 0,000 para el crédito.
  - El anexo A mezcla «0,100» y «>0,10».
- **Por qué importa.** La spec pide expresamente una sola notación para el KPSS acotado. Un «0,100» se lee como valor exacto en el límite del 10 %.
- **Qué se espera.** Que el adaptador use «< 0,001», «> 0,10» o «< 0,01» de forma uniforme, sin cambiar los CSV.

**5. Las remisiones del texto al anexo no llevan enlace (RF-14b).**
- Las 26 remisiones por slug en la prosa son texto en negrita sin enlace relativo. Los únicos 7 enlaces a `anexo-tecnico.pdf` y `.docx` salen de los encabezados de las tablas reducidas.
- Algunas remisiones ni siquiera nombran la letra del anexo: `03f-limitaciones.qmd:11` y `:14`, `01-introduccion.qmd:42`.
- No es un problema econométrico, pero incumple el contrato de enlaces.

### Menores

6. **Proyecciones locales (`05-modelo2.qmd:54`).** El texto da φ₄ = 3,049, pero no saca la conclusión que exige la spec: un ΔFFR(t) de 1 pp equivale al inicio de un ciclo de alzas de unos 3 pp, y β debe leerse con esa escala.
7. **Granger y C2 (`05-modelo2.qmd:33`).** «Se reduce a una sola prueba» es impreciso. C2 añade la condición de signo, así que «evidencia parcial» solo es posible con un θ₁ negativo y significativo.
8. **Pérdida de un trimestre (`06-resultados.qmd:39`).** El texto dice que el Modelo II «pierde un trimestre por el rezago de la tasa». La causa real es el rango de hasta 8 rezagos de K (`model2_deviations.csv`, fila 1).
9. **Niveles fuera de rango (`07-estres.qmd:76-77` y notas de `stress_delta`/`stress_levels`).** Dar el «máximo 6,497» como si fuera un nivel fuera de rango confunde, porque está dentro de [0, 100]. Hay que decir que son el mínimo y el máximo alcanzados por esas réplicas.
10. **RF-7 y RF-13.** `03e-desviaciones.qmd:14` no contrasta 2026T2 con el corte de la guía en 2026-01-01. La sección 11 no menciona el hueco de octubre de 2025 ni la fecha de congelación (ambos están solo en 3.1).
11. **Restos editoriales en el entregable.**
    - `03f-limitaciones.qmd:1`: «Esta continuación … no repite su encabezado».
    - `04-modelo1.qmd:10`: se renderiza «primera diferencia (primera diferencia)».
    - `11-datos-descarga.qmd:20`: «En la copia activa…».
    - Las tablas del cuerpo usan identificadores de código (`gdp_growth`, `modelo1`/`severo`).
    - La fuente aparece como ruta de archivo, no como «Fuente: FRED; elaboración propia» (RF-3).
12. **Frases con tono causal.** `02-literatura.qmd:28` («La política monetaria afecta la oferta de crédito…», sin atribución); `09-conclusiones.qmd:14` («hace que los shocks se prolonguen»).
13. **Trazabilidad (`04-modelo1.qmd:51`).** Usa `modelo1.robustez.d_unemp` para el desempleo y para la política monetaria a la vez. Coincide por azar (`d_ffr` también vale «1 de 9»), pero rompe la trazabilidad (RNF-6).
14. **Ventana HAC del Modelo II (`05-modelo2.qmd:15`).** No se dice cuántos rezagos usa (son 4, según el JSON).
15. **Chow 2020T2.** El cuerpo no menciona la advertencia de tamaño: 21 trimestres posteriores para 7 restricciones, con p = 0,034.
16. **Legibilidad del anexo.** El Panel 4 de `AT-M1-ROB` no tiene columna de término. El anexo A identifica las filas solo por «Índice».
17. **Remisiones faltantes en la sección 7 (`07-estres.qmd:83-102`).** Las sensibilidades de tasa y de origen no remiten a `AT-EST-RATE-SENSITIVITY` ni a `AT-EST-ORIGIN`, que sí existen.

## Lo que cumple

- **Criterio 3, lenguaje.** Sin frases causales graves; «efecto» queda definido como asociación condicional (01:26, 04:9, 05:10).
- **Criterio 4, cifras.**
  - Todas las variables `{{< var >}}` del cuerpo existen.
  - Contrasté contra CSV y JSON los coeficientes, los diagnósticos, la robustez, las proyecciones locales, la trayectoria y todas las cifras del estrés.
  - Recalculé desde `cov_hac`: Granger χ² = 0,857 con p = 0,3546, igual al p de S_rez; S = −0,048 con p = 0,200.
  - `dif_modelos` = 1,428 − 0,827 = 0,600.
- **Criterio 5, estrés.**
  - La invariancia por paso se cumple: el cambio es idéntico en los 13 pasos, en ambos modelos (`stress_origin.csv`).
  - La regla de tasa cero aparece como prudencia, no como efecto nulo, y la sensibilidad va rotulada aparte.
  - La dirección coincide con la mayoría de las réplicas (0,935 y 0,877), y se dice que la banda final cruza el cero.
  - Se informan los niveles fuera de rango (105 y 160) y las réplicas explosivas (1 y 1).
  - El cambio del primer trimestre del Modelo II es 0.
  - Las bandas se describen como incertidumbre de parámetros únicamente.
- **Criterio 6, Modelo II.** Granger equivale a C2 con K = 1. φ₀ = 1 aparece como identidad, sin error estándar ni banda (05:56; nota de `AT-M2-LP`).
- **Criterio 7, correspondencia.** Los 26 slugs del cuerpo resuelven cada uno a un único ancla, en el anexo y con el contenido que el texto afirma. Los destinos nombrados están en el PDF del anexo.

**Checklist de la skill:**
- Estacionariedad: tablas de los dos modelos, revisadas.
- Errores HAC: sí; ventana declarada en el Modelo I y en las proyecciones locales, pero no en el Modelo II (hallazgo 14).
- Selección de rezagos: los 8 valores de K se comparan sobre la misma muestra (n = 105).
- Signos frente a lo esperado: se discuten.
- Frases causales: solo las menores del hallazgo 12.
- Diagnósticos fallidos: reportados.
- Reproducibilidad: no la volví a ejecutar; solo existe la evidencia del autor.

## Lo que defendería ante el profesor
- La lectura «sin evidencia» del Modelo II viene de una regla fijada antes de estimar. Se presenta con RESET, Chow y endogeneidad a la vista, y no se vende como ausencia de efecto.
- El estrés es transparente: la diferencia no depende del origen (comprobado paso a paso), la tasa se fija en cero por prudencia y no se truncan las réplicas extremas.
- Cada cifra sale de `_variables.yml` y cada remisión del cuerpo resuelve en el anexo.

## Lo que me preguntaría el profesor
1. Si en el Modelo II el desempleo rezagado es significativo, ¿por qué la conclusión dice que el desempleo no se distingue de cero?
2. ¿Cómo «anticipa» la inflación la morosidad si entra en el mismo trimestre y es simultánea con ella?
3. Con unos 36 trimestres de tasa en cero, ¿tiene el Modelo II potencia para detectar algo, y qué muestra la variante sin esos tramos?

---

# Informe íntegro 2 — verificador-citas

VEREDICTO: CAMBIOS NECESARIOS

No hay hallazgos bloqueantes. Las 21 entradas existen, sus metadatos coinciden y los hallazgos y signos atribuidos están respaldados. Pido cambios por dos hallazgos importantes de redacción y presentación (I-1 e I-2) y por varios menores. No edité nada. Seguí `.claude/skills/citas-apa` y usé las APIs de Crossref y OpenAlex.

## Cobertura y controles

- **Claves.** Las 21 claves de `report/references.bib` se citan en el texto y las 21 citadas están en el `.bib`. No hay huérfanas en ninguna dirección. Revisé `report/secciones/*.qmd`, `report/entrega-combinada.qmd` y los anexos.
- **`scripts/verify_refs.py`.** Salió "Verificadas 21 de 21 entradas".
- **Crossref.** Confirmé los 21 registros. Las 19 entradas con DOI coinciden en título, autores, año, revista, volumen, número y páginas. Mi script falló por codificación en dos nombres con diacríticos y por un 404 transitorio en `tanaskovic2015`; repetí ambas consultas y coincidieron. `fred2026` y `frb2026` no tienen DOI y se comprobaron por su URL.
- **Estudios no usados como evidencia.** Los 3 descartados y los 8 pendientes de lectura no aparecen como respaldo en `report/` ni en el anexo PDF. Los recuentos de `_variables.yml` coinciden con la matriz: 17 verificados, 8 pendientes, 3 descartados y 4 de datos/método.
- **Lista renderizada.** En `outputs/preview-006/report/informe.pdf`, la lista de la sección 10 conserva los diacríticos (Obradović, Grubišić, Tanasković, Jandrić, Jordà, Peydró). El orden alfabético es correcto, con Tan antes de Tanasković.

## Tabla por entrada

| Clave | Existe | Metadatos coinciden | Afirmación respaldada | Nota |
|---|---|---|---|---|
| fred2026 | sí | sí | no verificable | `curl` a fred.stlouisfed.org no respondió (limitación de acceso). `verify_refs.py` lo dio por OK. Ver I-2. |
| frb2026 | sí | sí | sí, en parte | La URL responde 200 y habla de escenarios finales e "hypothetical". No comprobé las cifras de la matriz (desempleo pico del 10 %, vivienda −30 %). |
| newey1987 | sí | sí | sí | El resumen respalda "HAC semidefinida positiva". Ver M-5. |
| jorda2005 | sí | sí | sí | El resumen respalda las proyecciones locales. |
| bernanke1995 | sí | sí | sí | El resumen respalda la teoría del canal del crédito. Ver M-3. |
| kiyotaki1997 | sí | sí | sí | El resumen respalda garantía, persistencia y amplificación. |
| segoviano2006 | sí | sí | sí | El resumen menciona CoPoD, CIMDO y el ejercicio de estrés danés. Ver M-5. |
| nkusu2011 | sí | sí | sí | Paneles y PVAR; la morosidad sube con el deterioro macro. Ver M-5. |
| pesaran2006 | sí | sí | sí | Pérdidas asimétricas y no proporcionales; la probabilidad de impago depende de los ciclos. |
| maddaloni2011 | sí | sí | sí | Tasas cortas bajas ablandan los estándares; las largas no. Ver M-3. |
| wu2016 | sí | sí | sí | La tasa de desempleo de diciembre de 2013 quedó 1 % más baja. |
| gertler2015 | sí | sí | sí, en parte | Respalda costos de crédito, primas de término, diferenciales y orientación futura. No respalda "capacidad de pago de los deudores" (M-3). |
| krishnamurthy2011 | sí | sí | sí | Respalda los canales y la menor rentabilidad de MBS, con menor riesgo de crédito corporativo. |
| obradovic2026 | sí | sí | sí | Tasa de préstamo positiva, tipo de cambio sin efecto consistente, desempleo negativo. El informe no reproduce signos. |
| tanaskovic2015 | sí | sí | sí | Panel de CEEC y SEE, logaritmo del NPL, tipo de cambio. |
| bayar2019 | sí | sí | sí | Crecimiento e inflación negativos; desempleo positivo; GMM de sistema. |
| koju2018 | sí | sí | sí | Panel de 30 bancos de Nepal con estimación estática y dinámica. |
| zawadzki2023 | sí | sí | sí | Desempleo y deuda pública positivos; el signo de la inflación no se precisa (la redacción coincide). Ver M-1. |
| tan2023 | sí | sí | sí | Datos mensuales 2019–2021, OLS en primeras diferencias; el producto mayor reduce la morosidad. |
| madbouly2020 | sí | sí | sí | Inflación, PIB y petróleo con efecto positivo; trimestral 2009T1–2019T3. Ver M-2. |
| golitsis2022 | sí | sí | sí | Verifiqué la Tabla 4 en el PDF de EconStor (hdl 10419/289313). |

Golitsis, Tabla 4: desempleo 0,6417 (p=0,0495), tasa de interés 3,4731 (p<0,01), PIB −6,7075 y préstamos brutos no significativos. El período es 2005T1–2022T2.

## Hallazgos

### Importantes

- **I-1. La tabla de la sección 2.5 no coincide con lo que el texto dice de ella.** `report/secciones/02-literatura.qmd` (líneas 51–57) afirma tres cosas que la tabla renderizada no cumple.
  - **"Conjunto completo de estudios verificados".** La tabla incluye 9 estudios, todos de 2.5. Los 17 verificados incluyen los de 2.1 a 2.4.
  - **"En la columna de signo, «—»…".** `outputs/informe/lit_estudios_cuerpo.md` tiene solo las columnas Estudio, Dependiente, Regresores y Método, sin columna de signo.
  - **Nota al pie.** Dice "Cifras redondeadas a tres decimales… ceros redondeados", que no aplica a una tabla sin cifras, y habla de "signos no reutilizados".
- **I-2. La referencia de FRED renderizada no lleva fecha de consulta ni códigos de serie.** La regla de la skill pide ambos. Salió "Federal Reserve Bank of St. Louis. (2026). Federal Reserve Economic Data (FRED). https://fred.stlouisfed.org/". `urldate` y `note` están en el `.bib`, pero `apa.csl` no los muestra. La spec 006 y el manifiesto fijan 2026-10-02 como fecha de consulta; confirmé que esa fecha está en el `.bib`, no que `AT-FRED-MANIFEST` o el texto la muestren al lector.

### Menores

- **M-1.** "Dos estudios usan el tipo de cambio [Tanasković; Obradović]". Zawadzki también incluye la depreciación de la moneda, y la propia matriz lo registra. Son tres.
- **M-2.** "una con regresión simple" (Madbouly). El resumen solo dice "Regression model"; "simple" no está respaldado. Además se trata de siete bancos de un país, no de una serie de un solo país.
- **M-3.** Tres citas llevan más de lo que sus fuentes dicen.
  - `gertler2015` en la introducción respalda "alterar… la capacidad de pago de los deudores". La fuente trata de costos de crédito.
  - La sección 2.1 dice que Bernanke y Kiyotaki "explican por qué la morosidad puede reaccionar con retraso". Ninguno de los dos estudia morosidad. "Coherente con" es defendible; "explican" es demasiado.
  - `maddaloni2011` en `08-implicaciones.qmd` se cita sobre el crecimiento del crédito como alerta. La fuente trata de tasas cortas bajas y estándares laxos. El texto lo cubre con "coherente", pero es un apoyo indirecto.
- **M-4.** "…fueron descartados por no poder verificarse". Duffie y Singleton (1999) se descartó porque no respalda la sección 2.2, no por falta de verificación. Wilson (1997) y Virolainen (2004) sí fueron por falta de verificación.
- **M-5.** Detalles APA 7 en la lista renderizada.
  - **Newey y West (1987).** Sale "55(3), 703". Crossref solo trae la página inicial, así que no pude verificar el rango. Si es 703–708, hay que completarlo. Eso lo recuerdo de memoria y no lo confirmé en ninguna fuente, así que debe comprobarse antes de editar.
  - **Segoviano (2006) y Nkusu (2011).** Aparecen como "International Monetary Fund" sin número de serie. Crossref da issue 283 y 161; APA pide "IMF Working Paper No. 2006/283" y "No. 2011/161".
  - **`frb2026`.** Repite el autor como editorial ("Board of Governors… Board of Governors…").

## Limitaciones

- No pude leer los textos completos de los estudios con paywall o CAPTCHA (Tandfonline dio 403). Para esos, las atribuciones se verificaron contra los resúmenes de OpenAlex y quedan como "sí, según el resumen". Golitsis es la excepción: lo leí en EconStor.
- No pude contactar con FRED desde esta sesión.
- No revisé la maquetación de la tabla entre páginas. La extracción de texto del PDF muestra filas desordenadas en la pág. 5–6, que pueden ser un artefacto de `pdftotext`.

Archivos relevantes, todos bajo `C:/Users/gabri/orca/riesgo-credito-macro`:
- `report/references.bib`
- `report/secciones/02-literatura.qmd`
- `report/secciones/08-implicaciones.qmd`
- `report/secciones/01-introduccion.qmd`
- `outputs/informe/lit_estudios_cuerpo.md`
- `research/matriz-literatura.md`
- `outputs/preview-006/report/informe.pdf`

---

# Informe íntegro 3 — profesor-evaluador

# Evaluación del informe como profesor, contra `docs/guia-profesor.md`

Revisé las fuentes (`report/informe.qmd`, `report/secciones/*.qmd`, `report/anexos/*.qmd`) y las cifras de `report/_variables.yml`. El PDF no se puede renderizar en este entorno, así que leí las páginas ya renderizadas en `outputs/preview-006/qa-principal/` y `qa-anexo/`. No existe `report/slides.qmd`, así que no pude evaluar las diapositivas.

**VEREDICTO: CAMBIOS REQUERIDOS.** Como trabajo académico aprueba con holgura. No debe entregarse tal como está: tiene dos defectos bloqueantes y un problema de coherencia en el estrés que un evaluador de riesgos detectaría enseguida.

## Evaluación por sección

| Sección | Calificación | Por qué |
|---|---|---|
| 1. Introducción | Cumple | Plantea el problema, su relevancia, la pregunta literal y el objetivo, y fija desde el inicio el lenguaje de asociación. |
| 2.1–2.4 | Cumple parcialmente | Cada subsección se apoya en solo 2 estudios, y casi todos son teóricos o no miden morosidad (el propio texto lo admite). |
| 2.5 | Cumple | Explica las variables y los métodos de cada estudio (panel, GMM, FGLS, MCO, ARDL, PVAR). Pero Obradović y Grubišić (2026), el único estudio de política monetaria sobre morosidad, queda con signo «—» y no se discute. La tabla ocupa 5 páginas del cuerpo. |
| 3.1–3.4 | Cumple | Declara series, frecuencia, período, el vintage, el hueco de octubre de 2025 y las desviaciones (GDPC1, LOANS, ΔFFR como tasa única). |
| 3.5 | Cumple parcialmente | Describe los modelos solo con palabras: no hay ninguna ecuación en todo el informe. Además arrastra texto interno («Esta continuación pertenece a la subsección…»). |
| 4. Modelo I | Cumple | Estima, interpreta en pp, separa impacto de largo plazo, evalúa significancia y robustez (9 variantes), hace diagnósticos completos y prueba fuera de muestra, y cierra con una lectura de gestión. |
| 5. Modelo II | Cumple parcialmente | La regla, el Granger, las proyecciones locales y los diagnósticos están bien. Pero no muestra ni comenta sus controles, y la robustez sin pandemia y sin tramos de tasa cero (R2, R3) no aparece en el cuerpo. |
| 6.1–6.3 | Cumple parcialmente | 6.3 contiene un error de hecho (hallazgo B2). |
| 6.4 | Cumple | Responde de forma diferenciada: el entorno macro es relevante por inflación y crédito; la política monetaria no muestra asociación propia, y se explica por qué eso no prueba ausencia. |
| 7. Estrés | Cumple parcialmente | Construye el escenario adverso, lo compara con el base y calcula el cambio (+1,428 pp en el Modelo I, +0,827 en el Modelo II, con bandas y sensibilidades). No explica qué variables generan ese cambio, y el escenario D (alza de tasas) da una proyección idéntica al adverso (hallazgo I1). |
| 8. Implicaciones | Cumple | Cubre los siete puntos, añade un tablero indicador → criterio → acción y lo conecta con el resultado de aprendizaje de la asignatura. |
| 9. Conclusiones | Cumple | Responde la pregunta y dice cómo anticipar, dimensionar y gestionar; evita el formato prohibido. La afirmación sobre el desempleo omite el Modelo II. |
| 10. Referencias | Cumple parcialmente | Todas tienen DOI o URL, pero no siguen bien APA 7 (hallazgo M1). |
| 11. Datos | Cumple | Hay pipeline reproducible con `pandas_datareader`, aunque incluye texto que no va dirigido al lector (hallazgo B1). |
| Diapositivas | No evaluable | `report/slides.qmd` no existe y la entrega es el 15 de octubre. |

## Calificación por criterio

| Criterio | Peso | Puntos |
|---|---|---|
| Estructura de 11 secciones | 10 | 9 |
| Pregunta y objetivo | 5 | 5 |
| Uso de literatura | 15 | 12 |
| Datos y metodología | 10 | 7 |
| Modelo I | 12 | 11 |
| Modelo II | 12 | 9 |
| Integración de resultados (6) | 8 | 5,5 |
| Estrés | 10 | 7,5 |
| Implicaciones de gestión | 8 | 7 |
| Conclusiones | 5 | 4 |
| APA | 3 | 1,5 |
| Claridad y edición | 2 | 1 |
| **Total** | **100** | **79,5** |

## Hallazgos

**Bloqueantes**

- **B1. El documento se presenta como un borrador.**
  - El subtítulo del informe dice «Versión de trabajo; validación global y auditoría pendientes» (`report/informe.qmd:3`). El del anexo dice «validación global pendiente».
  - Hay texto interno del proyecto en el cuerpo:
    - `03f-limitaciones.qmd:1` explica que «no repite su encabezado».
    - La sección 11 habla de Google Docs, «URLs ficticias» y «si el profesor exige una única entrega».
    - En el PDF impreso aparecen «Abrir anexo PDF · Abrir anexo DOCX».
    - La página 13 dice «entra en primera diferencia (primera diferencia)».
  - Falta la portada APA 7 de estudiante: autor, institución, curso, profesor y fecha.
- **B2. La sección 6.3 afirma algo falso y la integración de los modelos queda incompleta.**
  - `06-resultados.qmd:46` dice que las demás variables «solo entran al Modelo I». En realidad, el Modelo II incluye esas variables rezagadas como controles.
  - Varios de esos controles son significativos en el Modelo II: desempleo rezagado 0,110 (p 0,039), inflación rezagada 0,024 (p 0,015) y crédito rezagado 0,007 (p 0,009).
  - Así, la conclusión de que el desempleo «no se distingue de cero» ignora un resultado del propio informe.
  - 6.4 dice que la lectura sobre inflación y crédito «no depende de un solo modelo», lo que se apoya justo en lo que 6.3 niega.

**Importantes**

- **I1. El estrés trata los coeficientes de forma asimétrica y no explica de dónde sale su resultado.**
  - El coeficiente de la tasa se fija en cero porque no es significativo, pero el del desempleo (p 0,214, robusto en 1 de 9 variantes) se usa completo.
  - Hice una descomposición aproximada con las trayectorias de AT-EST-PATHS. El +1,43 pp del Modelo I sale sobre todo del producto (cerca de +1,0) y del desempleo (cerca de +0,8).
  - La inflación, el hallazgo «más estable» del informe, lo reduce en unos 0,6–0,7 pp, porque baja en el escenario adverso. El crédito no aporta nada, porque el supuesto es el mismo en ambos escenarios.
  - Es decir, el número del estrés descansa en las variables más débiles. El informe no lo dice.
  - Además, el escenario D (alza de tasas), que es el ejemplo de la guía, da una proyección idéntica al adverso. En la figura, la línea roja del adverso queda tapada.
- **I2. El Modelo II no muestra su robustez en el cuerpo.** La tasa estuvo cerca de cero en buena parte de la muestra (2009–2015 y 2020–2021). La variante R3 que excluye esos tramos existe en el anexo (n = 69, también «sin evidencia»), pero el texto principal no la menciona.
- **I3. No hay especificación formal.** No hay ecuaciones de los Modelos I y II ni de las proyecciones locales.
- **I4. El anexo es difícil de usar.**
  - Las tablas están partidas en paneles de 4 columnas, y algunos paneles pierden las columnas que identifican cada fila. Por ejemplo, el panel 2 de AT-EST-DELTA repite «modelo1» 26 veces sin escenario ni trimestre.
  - Hay nombres de código en las tablas (`gdp_growth`, `d_ffr`, `prop_c_pos_pico`) y una columna sin nombre (``) en AT-STATIONARITY.
  - Las notas hablan de «spec 001» y citan rutas `outputs/tables/*.csv` como fuente.
- **I5. Falta poner las magnitudes en contexto de riesgo.**
  - El nivel estresado (3,42 pp, con pico de 3,72 pp) no se compara con el máximo histórico (7,35 pp en 2010T1) ni con la media (2,63 pp).
  - Los efectos por desviación estándar (por ejemplo, 0,087 pp de largo plazo para la inflación) solo están en el anexo.
  - No se explica por qué el escenario base sube de 1,42 a 1,99 pp con un crecimiento cercano al 2 %.

**Menores**

- **M1. APA 7 incompleto.**
  - Los títulos de artículo están en mayúsculas de título, no en minúscula de oración.
  - Los rangos de páginas usan guion en lugar de raya (95-110).
  - Newey y West (1987) solo indica «703» como página.
  - La Fed figura a la vez como autor y como editorial.
  - FRED no tiene fecha de consulta.
  - Los documentos de trabajo del FMI no llevan número.
  - Las tablas del cuerpo no tienen número ni título («Tabla N»), aunque las figuras sí.
  - La tabla de literatura usa nombres completos («Wu, Jing Cynthia y Xia, Fan Dora») y la expresión «tipo de interés de lending».
- **M2. Pequeñas inconsistencias.**
  - En la tabla de coeficientes el valor p del crédito aparece como «0,000» y en el texto como «< 0,001».
  - Varias tablas del anexo no tienen remisión desde el informe: AT-LIT-ESTUDIOS, AT-DESCRIPTIVES, AT-EST-RATE-SENSITIVITY, AT-EST-ORIGIN y las robusteces del Modelo II.
  - La serie dependiente no se grafica en el cuerpo; solo aparece como figura A.1 del anexo.

**Correspondencia entre informe y anexo: correcta en lo esencial.** Los 23 identificadores citados en el informe existen en el anexo y están en el anexo que se indica (las desviaciones y el manifiesto en F, el Modelo II en C, el estrés en D). La única excepción es que 03f cita AT-M1-DIAGNOSTICS sin indicar el anexo.

## Nota estimada: 79/100

Es honesto, reproducible y riguroso en diagnósticos, y la sección 8 es sobresaliente. Pierde puntos por el aspecto de borrador, la falta de ecuaciones, el error de 6.3 y un estrés cuyo resultado no se explica y contradice parcialmente las alertas que el propio informe recomienda vigilar. Con las cinco mejoras siguientes, calculo que llegaría a 87–90.

## Las 5 mejoras de mayor impacto

1. Quitar todo el texto de borrador e interno y añadir la portada APA (B1).
2. Corregir 6.3 e integrar los controles del Modelo II, en especial el desempleo, en 6.1–6.4 y en la conclusión (B2).
3. Añadir al estrés una descomposición del cambio por variable. Discutir la asimetría «desempleo se usa, tasa se anula» y la dirección contraria de la inflación (I1).
4. Escribir las ecuaciones de los dos modelos en 3.5 (I3) y llevar al cuerpo la robustez del Modelo II con tasa cero (I2).
5. Situar las magnitudes frente a la historia de la morosidad y arreglar las tablas del anexo: columnas de identificación, nombres legibles y numeración APA (I5, I4, M1).

## Preguntas que haría en la exposición, y si el informe las responde

| Pregunta | ¿La responde? |
|---|---|
| ¿Por qué el estrés usa el coeficiente no significativo del desempleo y anula el de la tasa? | No |
| ¿Qué variables producen los +1,43 pp? Si la inflación «es la alerta», ¿por qué en el adverso la reduce? | No |
| En el Modelo II el desempleo rezagado es significativo (p 0,039). ¿Por qué la conclusión dice que no se distingue de cero? | No |
| Con buena parte de la muestra con la tasa cerca de cero, ¿qué identifica ΔFFR? | Parcial (solo en el anexo) |
| ¿Es económicamente relevante 0,020 pp por punto de inflación? ¿Qué es 3,4 pp frente a 2010? | Parcial |
| ¿Cómo convierte un banco +1,43 pp en provisiones o capital (pérdida esperada = PD × LGD × EAD)? | Parcial (solo cualitativo) |
| ¿Por qué el base sube a 1,99 pp con un crecimiento cercano al 2 %? | Parcial (por el supuesto de crédito) |
| ¿Cómo separa la reacción de la Fed de un efecto de la tasa? | Sí |
| ¿Por qué creer los p-valores de variables que no son claramente estacionarias? | Sí (6.4) |
| ¿Por qué el escenario adverso no sube la tasa, como pide la guía? | Sí (escenario D y sensibilidad) |

Las cinco más difíciles son las cinco primeras.

## Checklist de la skill
- **11 secciones en orden:** sí, comprobado en `informe.qmd` y en el índice de la página 1.
- **Números escritos a mano:** no encontré ninguno; todas las cifras salen de `{{< var >}}` o de tablas incluidas.
- **Citas fuera de `references.bib`:** ninguna; las 19 referencias de las páginas 30–32 se corresponden con las citas del texto.
- **La conclusión responde y dice cómo anticipar:** sí.
- **Siete puntos de la sección 8:** sí, todos cubiertos.
- **Sin resolver en la salida:** no hay `?@` ni `{{<` en las páginas revisadas. Sí hay texto de enlaces y glosas internas (B1).

Archivos relevantes: `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/06-resultados.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/07-estres.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/03f-limitaciones.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/secciones/11-datos-descarga.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/informe.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/anexos/D-estres.qmd`, `C:/Users/gabri/orca/riesgo-credito-macro/report/_variables.yml`.
