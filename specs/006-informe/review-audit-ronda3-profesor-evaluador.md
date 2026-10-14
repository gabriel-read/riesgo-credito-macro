# Ronda 3 (acotada) — profesor-evaluador (contexto limpio)

Copia del mensaje final del subagente `profesor-evaluador`, tomada del texto recibido en la notificación de finalización. Coordinó Claude Code. Versión auditada: informe.pdf d1a3460a…, anexo-tecnico.pdf a3e88846…, informe.docx a524791b…, anexo-tecnico.docx e2a8d81e…. Alcance: hallazgos de la ronda 2 y regresiones. Limitación declarada por el revisor: no pudo renderizar el PDF ni calcular hashes; la paridad entre PDF y páginas renderizadas es inferida de `docs/qa-correcciones-006-ronda4.json`.

**Veredicto: CAMBIOS NECESARIOS.** Todos los cambios pendientes son menores y editoriales. No hay ninguno bloqueante ni de econometría. Quedan sin corregir dos restos de plantilla y las admisiones de «no verificado». Además, las correcciones abrieron cuatro errores pequeños nuevos. Uno se ve enseguida: el texto que sigue a la Tabla 1 dice que la tabla no recoge signos, pero ahora tiene una columna de signos. Se corrige en menos de una hora.

## Qué leí y qué limitación tuve

- **El PDF no se puede renderizar aquí** (falta `pdftoppm`). Usé el Markdown generado, `outputs/preview-006/report/informe.md`, y busqué por texto en `anexo-tecnico.md`.
- **Páginas renderizadas:** revisé `outputs/preview-006/qa-ronda4-congelado-principal/` (36 páginas). Miré las páginas 1, 3, 4, 7, 10, 20, 27, 28, 34 y 35.
- **Correspondencia con los SHA:** `docs/qa-correcciones-006-ronda4.json` atribuye 36 páginas al PDF con SHA `d1a3460a…`. Es el mismo SHA que figura en `docs/huellas-paquete-auditoria-006-ronda4.json` para `informe.pdf`, y el número de páginas coincide. No pude calcular los hashes yo mismo porque no tengo terminal. La paridad es, por tanto, inferida, no comprobada byte a byte.
- **Comparación con la versión anterior:** para distinguir errores nuevos de errores ya existentes, contrasté con `outputs/preview-006-ronda3-evidencia/informe.md`.

## Portada

Está limpia. Lleva título, autor, INTEC, curso, profesor y la fecha 16 de octubre de 2026, que respeto como decisión del autor. No queda ningún texto de borrador.

## Hallazgos de la ronda 2: estado actual

| Hallazgo | Estado | Evidencia |
|---|---|---|
| B1 (sección 11) | **Mayormente resuelto** | Ya no aparecen «gancho», «espejo» ni «procedimiento aprobado». Queda la mención a Google Docs (`informe.md:1841-1844`), ahora como nota para el lector. Es aceptable. |
| I1 / N3 Origen y asimetría del estrés | **Resuelto** | `informe.md:1277-1297` da la dirección de cada variable: el crédito no aporta, la inflación resta, actividad y desempleo suman al principio y se invierten al final. Atribuye la asimetría a la regla fijada antes de estimar. La 7 dice que D no es un escenario estanflacionario (`:1210`). |
| I1 Línea del adverso oculta | **Resuelto** | Págs. 27-28: la línea roja gruesa y la discontinua con marcadores se distinguen, y una nota dice «Adverso y D coinciden…». |
| I4 Anexo | **Parcial** | Ya no quedan «Fila de origen» ni «spec 003». Siguen `VIF (d_ffr_l0)` y `VIF (d_ffr_l1)`, y el panel 2 de C.3 está casi vacío (`anexo-tecnico.md:1473-1504`). |
| I5 Por qué sube el base | **Sin cambio** | Sigue diciendo solo «supuestos de calendario y de crédito» (`:1328-1331`), sin decir cuál pesa. Es menor. |
| M1 / N5 APA | **Resuelto en lo esencial** | Corregidos «U.S.», «Malaysia», la mayúscula tras dos puntos, el título de la Fed, Nkusu, Segoviano, la referencia de FRED y el «non-per-forming» de Koju (págs. 34-35). Queda un resto: el DOI de Zawadzki se parte como «ceej-» / «-2023-0016» y parece llevar guion doble (pág. 35). |
| M2 | **Resuelto** | La Figura 1 de DRALACBS ya está en el cuerpo (pág. 10) y AT-DESCRIPTIVES lleva identificador (`:378`). |
| N1 Texto interno | **Resuelto** | Tabla 6 dice «Modelo I / II», la nota de la Tabla 7 está limpia, no queda «contratos aprobados» y la frase «ninguna se escribe a mano» se reescribió. |
| N2 Fecha | **No aplica** | Es decisión del autor. |
| N4 Restos de plantilla | **Parcial** | **Corregido:** la 3.2 y la remisión «Anexo B, …, Anexo B». **Siguen:** «sea Y la morosidad en la forma primera diferencia» (`:445-446`) y «ningún horizonte detecta… (ninguno)» (`:896-897`, pág. 20). Hay remisiones repetidas: AT-LIT-ESTUDIOS dos veces en seis líneas (`:236-244`), AT-M1-ROB en dos frases seguidas (`:707-710`) y AT-FRED-MANIFEST tres veces. Los enlaces ya se ven en azul y subrayados (pág. 4): eso queda resuelto. |
| N6 Nota fija en todas las tablas | **Mayormente resuelto** | El texto sobre KPSS solo queda en las tablas de estacionariedad, donde sí corresponde. Las Tablas 2 y 5, que no tienen cifras, siguen diciendo «Cifras redondeadas a tres decimales». La Tabla 7 da la fuente dos veces: en su línea propia y otra vez dentro de la nota (`:1261-1268`). |
| N7 Tabla 1 sin signos | **Resuelto, pero con regresión** | Se añadió la columna «Signo y contexto». Ver R1. |
| N8 Figuras | **Resuelto en las Figuras 2-4** | La fuente aparece una sola vez, dentro de la imagen. La Figura 1 tiene el problema contrario (ver R3). |
| N9 Dos justificaciones de la regla de la tasa | **Resuelto** | Todas las menciones usan «mientras la lectura no sea de evidencia fuerte» (`:1148`, `:1235`, `:1296`). |
| N10 Estudios sin leer, a la vista | **Sin resolver** | Siguen «Otros 8 estudios candidatos no se usan porque su contenido no se verificó…» (`:310-313`) y Nkusu con «no especificados en la fuente consultada» (`:256`). Obradović ya reporta su hallazgo (`:296-297`): eso sí está corregido. |
| 2.1–2.4 Coletilla repetida | **Sin resolver** | «Esta subsección se apoya en 2 estudios verificados» sigue cuatro veces. |

## Errores nuevos introducidos por las correcciones

| # | Severidad | Ubicación | Problema |
|---|---|---|---|
| R1 | Menor (muy visible) | `informe.md:260-262`, págs. 6-8 | El texto dice «La tabla no recoge signos de los coeficientes» justo debajo de una tabla que ahora tiene columna de signos. Además, Obradović figura con «—» en esa columna, aunque el texto informa su signo (`:296`). |
| R2 | Menor | `informe.md:391-392` y `:1801-1802` | Error de concordancia: «desde los especificaciones pre-registradas» y «de los especificaciones». Viene del reemplazo de «contratos aprobados». |
| R3 | Menor | Pág. 10, Figura 1 | La figura nueva no lleva fuente ni dentro de la imagen ni en el pie. Tampoco explica que las franjas grises son recesiones (USREC). |
| R4 | Menor (redacción econométrica) | `informe.md:1090-1092` (6.3) | Cláusula nueva: «alerta de colinealidad…, que vuelve menos precisa su estimación pero no la hace significativa». Es confusa: la colinealidad infla el error estándar y nunca «hace significativo» un coeficiente. Debería decir algo como «que resta precisión; aun así, el coeficiente es significativo». |
| R5 | Menor (formato) | `informe.md:255`, Tabla 1 | La celda de Golitsis termina con una nota de procedencia, «(texto completo, resultados de largo plazo y Tabla 4)», que no aporta al lector. La Tabla 1 ahora ocupa unas tres páginas con columnas estrechas (págs. 6-8). |

## Nota estimada: 92/100 (89 en la ronda 2)

Sube estrés (8 → 9,5), datos (9 → 9,5), APA (2,25 → 2,75), literatura (12 → 12,5) y claridad (1,25 → 1,5). No llega a 94 por R1, N10, la coletilla de 2.1–2.4 y los dos restos de plantilla. Corrigiendo R1-R4, N4 y N10, quedaría en 93-94.

## Qué no pude verificar

- Los hashes SHA de los entregables actuales: la paridad entre el PDF y las páginas es inferida.
- `informe.docx` y `anexo-tecnico.docx`: son binarios y no los pude leer.
- Que los enlaces entre archivos funcionen al hacer clic.
- El anexo página a página: lo revisé solo por búsqueda de texto.
- Las diapositivas: `report/slides.qmd` sigue sin existir (corresponde a la spec 007).
