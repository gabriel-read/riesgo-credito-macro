# Ronda 4 de auditoría (paquete ronda 5, acotada) — revisor-econometrico (contexto limpio)

Copia del mensaje final del subagente `revisor-econometrico`, tomada del texto recibido en la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 5 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda5.json`, SHA-256 8671052e…5b57). Alcance: los seis hallazgos de la ronda 3 y regresiones.

**VEREDICTO: APROBADO**

**Alcance.** Revisé solo los seis hallazgos de la ronda 3 y las posibles regresiones de sus correcciones. No edité nada, no hice renders y no corrí `uv run pytest -q` ni el pipeline. Saqué el texto de los PDF con `pdftotext -enc UTF-8` y el de los DOCX desde `word/document.xml`. Las restas adverso − base las calculé yo con pandas sobre `outputs/tables/stress_paths.csv`. Versión revisada (sha256): informe.pdf 8cdfa2a6…, anexo-tecnico.pdf 58429c72…, informe.docx 994e28fc…, anexo-tecnico.docx 75e241c1…, informe.md 38e645d0…, anexo-tecnico.md 71dca3f7….

## Hallazgos de la ronda 3: estado

| # | Hallazgo de la ronda 3 | Estado | Evidencia propia |
|---|---|---|---|
| 1 | 07:59, «se invierte» confundía los regresores con los niveles | **Resuelto** | En `07-estres.qmd:59` la inversión se atribuye ahora al crecimiento del producto y al aumento del desempleo, «aunque el nivel del desempleo sigue por encima». Lo comprobé en stress_paths (Modelo I, adverso − base). Crecimiento del PIB: negativo de 2026T3 a 2028T3 y positivo de 2028T4 a 2029T3. ΔU: +1,3 a +0,2 hasta 2028T1 y −0,2 a −0,4 desde 2028T2. Nivel de desempleo implícito: entre +1,3 y +5,7 pp en todo el horizonte, +3,8 pp al final. Inflación: entre −0,12 y −1,38 en todo el horizonte. Crédito: 0 en los 13 trimestres. Coeficientes en `model1_coefficients.csv`: producto −0,0163, ΔU +0,0774, π +0,0198, crédito +0,0099. Con esos signos, la inflación resta y el crédito no aporta, como dice el texto. «Se invierte» ya no aparece en ningún PDF ni DOCX. El mismo párrafo está en informe.md:1278-1299, en informe.pdf (texto, línea 403) y en informe.docx. |
| 2 | La regla de la tasa estaba repetida dos veces en el mismo párrafo | **Resuelto** | La regla se enuncia una vez, en 07:43-45. Coincide con `specs/005-estres/spec.md:64` y :95 (RF-9) y con su origen en `specs/004-modelo-ii/spec.md:90`, por lo que «fijada antes de estimar» es correcto. En el párrafo queda solo una remisión, 07:61 («por la regla pre-registrada de la sección anterior»). La nota de la tabla también la menciona, y esa mención la exige RF-9 («lo declarará en el pie de cada tabla»). 06:85 es coherente. |
| 3 | 03b y 11: «de los especificaciones» | **Resuelto** | `03b-variables.qmd:8` dice «desde las especificaciones pre-registradas» y `11-datos-descarga.qmd:3`, «de las especificaciones pre-registradas». «los especificaciones» aparece 0 veces en las fuentes, en los .md, en los PDF y en los DOCX. |
| 4 | Etiquetas VIF traducidas a medias en AT-M2-DIAGNOSTICS y en las tablas de limitaciones | **Resuelto** | anexo-tecnico.md:1475-1481 y :1509-1515 tienen todas las etiquetas en español, y también :819 y :1618 en las tablas de limitaciones. «VIF (d_» aparece 0 veces en los dos PDF; «d_ffr_l» y «d_unemp» aparecen 0 veces en los DOCX. Los CSV conservan los identificadores de código (`model2_diagnostics.csv:8-11`, `model1_diagnostics.csv:9,11`), lo que es correcto porque la traducción se hace en la capa de presentación. |
| 5 | 06:51, «no la hace significativa» | **Resuelto** | 06:51, 06:62 y 09:13 dicen ahora «que infla su error estándar y no explica su significancia». Es coherente con `model2_coefficients.csv:7` (p = 0,0392) y con un VIF de 33,154 (`_variables.yml:859-861`). En informe.pdf y en informe.docx la frase aparece 3 veces, y la variante antigua 0 veces. |
| 6 | Nota circular de `stress_delta_nota.md` (opcional) | **Resuelto** | `outputs/informe/stress_delta_nota.md:1` dice «se fijan en cero mientras la lectura del Modelo II no sea de evidencia fuerte», que ya no es circular y coincide con RF-9. La misma frase aparece 2 veces en el informe y 8 en el anexo, tanto en el PDF como en el DOCX. «por la regla de tasa en cero» no aparece en ninguna nota. |
| Residuo de R1#11 (menor, no era una regresión) | Celdas de p vacías en los VIF y en CUSUM | **Aceptable** | AT-M1-DIAGNOSTICS deja la celda vacía (anexo-tecnico.md:595-603) y AT-M2 pone «—» (:1475-1484). Los dos paneles explican ahora que el VIF no tiene p-valor y que los vacíos o guiones no son ceros (:584-586, :1464-1466). La Tabla 4 del informe trae la misma aclaración (informe.md:744-745). La diferencia entre vacío y guion viene de los CSV y está declarada. |

## Regresiones nuevas

Ninguna es bloqueante y ninguna cambia una conclusión.

1. **Opcional. `07-estres.qmd:59`.** Dice «hacia el final de la trayectoria». El aumento del desempleo del adverso pasa a ser menor que el del base desde 2028T2, que es el paso 8 de 13, mientras que el crecimiento del producto supera al del base desde 2028T4. «En la segunda mitad» sería más exacto para ΔU. No es un error de signo.
2. **Opcional y cosmético. `informe.md:731` y `anexo-tecnico.md:596`.** La etiqueta «VIF (PIB (crecimiento))» lleva paréntesis anidados. Es inofensivo.
3. **Observación de proceso, no es un hallazgo.** `report/_variables.yml` y `outputs/informe/*.md` son de las 12:47-12:48, posteriores a los PDF (12:33-12:35) y a los DOCX (12:36-12:37). Para este alcance comprobé que coinciden la nota de la Tabla 7, «3 de 9», «1 de 9», d_unemp_l1 (0,110 pp; p = 0,039), el VIF de 33,154 y los Δ de 1,428 y 0,827. No comparé el resto de las variables con los artefactos.

## Lo que no ejecuté

No corrí la suite, ni renders, ni la doble corrida del pipeline. No vi las páginas como imagen ni probé los enlaces con clic. No contrasté el anexo completo cifra por cifra contra todos los CSV. Tampoco revisé nada fuera de los seis hallazgos, como las citas o el DOI de Zawadzki.

Lo que defendería ante el profesor:
- La regla de la tasa en cero se fijó en la 004, antes de estimar el Modelo II (spec 004:90), y la 005 la aplica sin cambios (RF-9). El informe la enuncia una vez y después solo remite a ella.
- La lectura de signos del estrés coincide trimestre a trimestre con las trayectorias y los coeficientes: el crédito no aporta, la inflación resta, y el producto y ΔU suman al principio y restan al final, con el desempleo del adverso siempre por encima del base.
- La alerta del VIF se usa bien: infla el error estándar, así que no puede explicar que ΔU(t−1) sea significativo en el Modelo II.

Lo que me preguntaría el profesor:
1. Si desde 2028T2-2028T4 el producto y ΔU restan, ¿qué sostiene que el cambio final siga siendo de 1,428 pp? (Respuesta esperada: la persistencia, con ρ = 0,626 sobre la diferencia acumulada.)
2. ΔU entra en 2 de los 9 escenarios de robustez del Modelo I... en realidad se mantiene en 1 de 9 variantes y el producto en 3 de 9: ¿qué parte del orden de magnitud del estrés sobrevive a esa fragilidad?
3. ¿Por qué el VIF de ΔU(t−1) en el Modelo II (33,2) se atribuye a «posible multicolinealidad» y el del Modelo I a las dummies de la pandemia?
