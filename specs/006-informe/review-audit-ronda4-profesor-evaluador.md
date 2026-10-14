# Ronda 4 de auditoría (paquete ronda 5, acotada) — profesor-evaluador (contexto limpio)

Copia del mensaje final del subagente `profesor-evaluador`, tomada del texto recibido en la notificación de finalización. Coordinó Claude Code. Versión auditada: paquete ronda 5 de Codex (manifiesto `docs/huellas-paquete-auditoria-006-ronda5.json`, SHA-256 8671052e…5b57): informe.pdf 8cdfa2a6…, informe.docx 994e28fc…, anexo-tecnico.pdf 58429c72…, anexo-tecnico.docx 75e241c1…. Alcance: hallazgos de la ronda 3 y regresiones. Limitación declarada por el revisor: no pudo renderizar el PDF ni calcular hashes; la correspondencia con la versión entregada es inferida de `docs/visual-verificada-006-ronda5.json` y `docs/huellas-paquete-auditoria-006-ronda5.json`.

**Veredicto: CAMBIOS NECESARIOS (menores, ninguno bloqueante)**

Casi todo lo que señalé en la ronda 3 está corregido: R1 a R4, la coletilla de 2.1 a 2.4, el DOI de Zawadzki, los nombres VIF del anexo y las notas de las Tablas 2, 5 y 7. Quedan dos puntos. El primero es N10: la corrección tomó la dirección contraria y ahora deja más a la vista que la mayoría de los estudios se verificó solo por el resumen. El segundo es R5, que se resolvió solo en parte. Hay además dos regresiones menores, y en el anexo y la Tabla 6 queda lenguaje de proceso que debí señalar en la ronda 3. Se corrige todo en menos de una hora.

## Qué leí y cómo sé que es esta versión

- **Markdown generado:** leí entero `outputs/preview-006/report/informe.md` y busqué por texto en `anexo-tecnico.md`. Lo comparé con `outputs/preview-006-ronda4-evidencia/` para separar lo nuevo de lo heredado.
- **Páginas renderizadas de la ronda 5:** vi las páginas 1, 6, 8, 10 y 35 de `outputs/preview-006/qa-ronda5-congelado-principal/`.
- **No pude renderizar el PDF ni calcular hashes**, porque no tengo terminal. La correspondencia con la versión entregada es inferida, así:
  - `docs/visual-verificada-006-ronda5.json` dice que las páginas salen del PDF con SHA `8cdfa2a6…` (36 páginas).
  - Ese SHA es el mismo que figura para `informe.pdf` en `docs/huellas-paquete-auditoria-006-ronda5.json`.
  - Para el anexo, el SHA `58429c72…` coincide en ambos archivos.
  - El mismo JSON de huellas registra el SHA de `informe.md`, `38e645d0…`. Su fecha (16:39) es posterior a la del PDF (16:35).
- **Portada (pág. 1):** está limpia. Lleva título, autor, INTEC, curso, profesor y la fecha del 16 de octubre de 2026, que es decisión del autor. No queda texto de borrador.

## Hallazgos de la ronda 3: estado actual

| Hallazgo | Estado | Evidencia |
|---|---|---|
| R1: el texto dice que la Tabla 1 no recoge signos | **Resuelto** | `informe.md:265-267`: ahora explica que «—» significa que la tabla no los recoge. Una nota sobre el guion de Obradović (`:258-260`, pág. 8) remite al signo que da el texto (`:300-302`). |
| R2: «los especificaciones» | **Resuelto** | `:393` y `:1804` dicen «las especificaciones». |
| R3: la Figura 1 sin fuente ni explicación de USREC | **Resuelto** | Pág. 10: el pie dice «Fuente: FRED; elaboración propia. Las franjas grises indican períodos de recesión según USREC». El anexo también (`anexo-tecnico.md:216`). |
| R4: «no la hace significativa» | **Resuelto** | `:1093`, `:1115` y `:1559` dicen «que infla su error estándar y no explica su significancia». |
| R5: nota de procedencia en la celda de Golitsis | **Parcial** | Salió de la celda, pero ahora es un párrafo suelto bajo la tabla (`:262-263`, pág. 8). Sigue siendo una nota de proceso, y debajo de la tabla hay ahora tres notas seguidas. La Tabla 1 aún ocupa las págs. 6-8 con columnas estrechas. |
| N4: «sea Y la morosidad» | **Resuelto** | `:447-448`: «Para el Modelo I, Y representa la primera diferencia de la morosidad». |
| N4: «(ninguno)» | **Resuelto** | `:897-898` (en la ronda 4 estaba en `:896-897`). |
| N4: remisiones repetidas | **Resuelto** | AT-LIT-ESTUDIOS aparece una vez (`:242`), AT-M1-ROB una vez (`:709`) y AT-FRED-MANIFEST dos, en 3.1 y en 11 (`:359`, `:1806`). |
| Coletilla «Esta subsección se apoya en 2 estudios» en 2.1-2.4 | **Resuelto** | Ya no aparece (`:160-227`). |
| N10: estudios sin leer, a la vista | **Sin resolver; empeora** | Se quitó «Otros 8 estudios…», pero `:315-317` mantiene un párrafo de candidatos no usados. Sigue Nkusu «no especificados en la fuente consultada» (`:254`, pág. 8). Ver además X1. |
| Anexo: VIF con nombres internos | **Resuelto** | `anexo-tecnico.md:1475-1481`: «Cambio de tasa contemporáneo» y «Cambio de tasa, rezago 1». |
| Anexo: panel 2 de C.3 casi vacío | **Explicado, pero con regresión** | Se conserva vacío y se añade una nota (`:1498-1500`). Ver X2. |
| DOI de Zawadzki partido | **Resuelto** | Pág. 35: `https://doi.org/10.2478/ceej-2023-0016` íntegro, sin guion doble. |
| N6: notas de las tablas | **Resuelto** | Las Tablas 2 y 5 ya no llevan nota de redondeo (`:377`, `:863`). La Tabla 7 da la fuente una sola vez (`:1263`). |

## Regresiones nuevas

| # | Severidad | Ubicación | Problema |
|---|---|---|---|
| X1 | Menor-moderada (percepción de la literatura) | `informe.md:156-158`; `anexo-tecnico.md:4751-4767` | Frase nueva en la introducción de la sección 2: «En la mayoría de los casos la verificación se apoya en el resumen del estudio». En el anexo E, 17 de 18 filas dicen ahora «Base consultada: resumen del estudio». Es honesto, pero es justo lo contrario de N10: un profesor lee que casi nada se leyó entero. Si el autor lo mantiene por integridad, basta con dejarlo solo en el anexo y quitarlo del cuerpo. |
| X2 | Menor | `anexo-tecnico.md:1494-1500` | La nota nueva del panel 2 deja ver texto interno («el CSV no añade una nota», «la salida aprobada»). Además repite palabra por palabra la nota del panel 1 (`:1464-1466`). |
| X3 | Menor (incoherencia) | `anexo-tecnico.md:4759` frente a `informe.md:258-260` y `:300-302` | En el anexo, Obradović dice «Lectura de signo no presentada; consultar la fuente citada», pero el informe sí presenta su signo y la nota nueva de la Tabla 1 remite a él. |

## Lenguaje de proceso que debí señalar en la ronda 3

Estos restos ya estaban en la ronda 4, así que no son regresiones. Pertenecen a la misma familia que N4 y conviene quitarlos en la misma pasada:

- «crédito con su rezago aprobado» (`informe.md:489`).
- Nota de la Tabla 6: «la redacción de la comparación corresponde a la especificación pre-registrada» (`:1058-1061`). Además repite «pre-registrada».
- «mínimos cuadrados generalizables factibles» en la Tabla 1 (`:246`, pág. 6). El texto de `:280` dice «generalizados».
- «consultar la matriz» en el anexo E (`:4751-4758`). El lector no tiene esa matriz.
- Se alternan «preregistro» y «pre-registro» (`:412`, `:510` frente a `:658`).

## Nota estimada: 93/100 (92 en la ronda 3)

- **Sube:** claridad y formato (R1-R4, plantilla, coletilla, DOI y notas de tablas) y APA, que queda limpio.
- **No sube más:** literatura no mejora por X1, R5 queda a medias y el anexo conserva lenguaje interno.
- **Para llegar a 94:** quitar X1 del cuerpo, suavizar X2, corregir X3 y limpiar los restos de la lista anterior.

## Qué no pude verificar

- Los hashes SHA, que no calculé yo. La correspondencia entre el PDF y las páginas es inferida de los dos JSON.
- `informe.docx` y `anexo-tecnico.docx`: son binarios y no los leí. No sé si coinciden con el Markdown.
- Las páginas 50, 51 y 140 del anexo PDF: el anexo lo revisé solo por búsqueda de texto.
- Que los enlaces entre archivos y hacia los DOI funcionen al hacer clic.
- Las diapositivas: siguen fuera de alcance, porque corresponden a la spec 007.
