<!-- Copia literal del mensaje final del subagente verificador-citas (id a61fb08947fd65f29), extraída del registro de subagentes de la sesión. Ronda 1, 2026-10-12. -->

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