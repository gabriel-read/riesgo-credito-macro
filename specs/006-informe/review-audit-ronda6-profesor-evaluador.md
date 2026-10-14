# Ronda 6 de auditoría (paquete ronda 7, comprobación acotada) — profesor-evaluador (contexto limpio)

Copia del mensaje final del subagente `profesor-evaluador`, tomada de la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 7 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda7.json`, SHA-256 69003c83a7c6ccbc69c5cbd23bbeeb43bde0b970792f53748df302ca574535e5). Rondas anteriores conservadas intactas.

**Veredicto: APROBADO.** Los cinco hallazgos M1 a M5 están resueltos y el nuevo texto de la 2.5 sobre Obradović y Grubišić está bien. No encontré ninguna regresión que bloquee la entrega. Hay una sola regresión, cosmética, en la Tabla 8. No reabro X1 ni N10, que se conservan por decisión del usuario.

## Estado de M1 a M5

| Hallazgo | Estado | Evidencia |
|---|---|---|
| M1: Tablas 2 y 4 sin cortes de una fila | **Resuelto** | La Tabla 2 entra entera en la pág. 10, con título, 13 filas y fuente (`qa-ronda7-principal/page-010.png`). La Tabla 4 entra entera en la pág. 16: título, enlace, las 14 filas, fuente y nota (`page-016.png`). |
| M2: Tabla 6 con título y datos juntos | **Resuelto** | La pág. 22 empieza con «Tabla 6», el título, el enlace, las dos filas, la fuente y la nota (`page-022.png`). La pág. 21 ya no termina con el título suelto. |
| M3: «vacíos del CSV» en el panel 5 de robustez | **Resuelto** | `anexo-tecnico.md:1101-1104` dice ahora «Las celdas vacías de Motivo indican que no se proporciona una explicación adicional…». Fuera de las etiquetas heredadas «Índice CSV» (`:292-297`), el anexo no menciona más el CSV. |
| M4: Anexo F, «Pre-registro de la especificación pre-registrada» | **Resuelto** | La columna Referencia dice ahora «Pre-registro del Modelo I» (`:4825-4827`) y «Pre-registro del Modelo II» (`:4844`). |
| M5: nota de la Tabla 1, «descrito en 2.5» | **Resuelto** | `informe.md:259-260` dice «remite al signo de la tasa de préstamo explicado en el texto». |

## Nuevo texto de la 2.5 (Obradović y Grubišić)

Ubicación: `informe.md:276-278`, `:283` y `:302-310`.

- **Claridad: buena.** Dice qué variable usa el estudio, con qué signo y qué explicación dan los autores. Llama al resultado del desempleo «inesperado» y atribuye esa palabra a los autores. Eso está bien hecho.
- **Equilibrio: bueno.** El desempleo con signo negativo aparece junto a los tres estudios con signo positivo, sin esconderlo. Además, el cierre («los signos son heterogéneos… hipótesis y no resultado dado») encaja con lo que se acaba de exponer. Separar el tipo de interés de préstamo de la tasa de política evita un error de lectura frecuente.
- **Lenguaje de proceso: no lo hay.** El texto describe el estudio, no cómo se trabajó.
- **Detalles opcionales, que no bloquean:**
  1. La frase de `:305-310` tiene unas 55 palabras. Convendría partirla en dos tras «inesperado».
  2. La nota de la Tabla 1 dice que el guion remite al signo «de la tasa de préstamo». El texto informa además el tipo de cambio y el desempleo de ese estudio. Sería más exacto «remite a los signos explicados en el texto».
  3. En `:293-296`, «en la mayoría» equivale a 3 de 4 estudios. Es correcto, pero «en tres de los cuatro estudios…» sería más preciso.

## Regresiones

| # | Severidad | Ubicación | Hallazgo |
|---|---|---|---|
| R7-1 | Cosmética, nueva | Págs. 30-31 (Tabla 8, tablero de alertas) | La pág. 30 termina con el título, el encabezado y **una sola fila** de la Tabla 8. Las demás filas pasan a la pág. 31. En la ronda 6 quedaban dos filas en la pág. 30. Es el mismo tipo de corte que M1, desplazado por el reflujo de la página. No bloquea la entrega. |

- No hay `?@` ni `{{&lt;` / `{{&amp;lt;` en ninguno de los dos `.md`.
- Tampoco aparecen «Codex», «Claude», «ronda», «aprobad» ni «TODO».
- En el cuerpo del informe no queda «CSV» fuera de la sección 11.
- Restos heredados, que ya estaban en rondas anteriores y no exijo cambiar:
  - «Fuente: matriz de literatura verificada» en la nota de la Tabla 1 (`:262`).
  - «Skill de econometría de series de tiempo» como Referencia en las Tablas F.2 y F.3 (`anexo-tecnico.md:4823`, `:4840-4841`).
  - La redundancia de `informe.md:233-235`.

  Si se quiere pulir, «Skill» es el que más suena a herramienta interna. Podría decir «criterio metodológico de series de tiempo».

## Nota estimada: 95/100 (94 en la ronda 5)

- **Sube un punto:** los cinco restos M1 a M5 están limpios y la 2.5 cuenta con más equilibrio el estudio más reciente.
- **No sube más:** X1 y N10 siguen pesando, porque se conservan por decisión del autor. Se suma el nuevo corte de la Tabla 8, aunque es menor.

## Qué no pude verificar

- No vi las páginas del anexo donde caen el panel 5 de robustez ni las Tablas F.2 y F.3. M3 y M4 los verifiqué solo en `anexo-tecnico.md`.
- No calculé hashes. Supongo que las imágenes de `qa-ronda7-principal/` corresponden al PDF vigente.
- No abrí los `.docx` ni probé los enlaces internos, la importación a Google Docs ni los DOI.
- Las diapositivas quedan fuera, porque son de la spec 007.
