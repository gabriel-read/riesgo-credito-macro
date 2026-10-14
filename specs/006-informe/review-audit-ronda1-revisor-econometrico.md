<!-- Copia literal del mensaje final del subagente revisor-econometrico (id a926760501c82957e), extraída del registro de subagentes de la sesión. Ronda 1, 2026-10-12. -->

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