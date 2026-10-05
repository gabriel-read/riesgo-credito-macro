# Auditoría independiente — spec 002 Literatura (T10)

**VEREDICTO: APROBADO**

Auditor: subagente `verificador-citas`, al que solo se le pasaron las rutas de `report/references.bib`, `research/matriz-literatura.md` y `specs/002-literatura/spec.md` (RNF-4: sin conclusiones previas). Fecha: 5-oct-2026. Es la cuarta ronda; las tres anteriores dieron CAMBIOS NECESARIOS.

## Historial de rondas

| Ronda | Veredicto | Hallazgos bloqueantes | Resolución |
|---|---|---|---|
| 1 | CAMBIOS NECESARIOS | `obradovic2026` con sección principal 2.4 (debía ser 2.5); frecuencia «anual» sin respaldo en `tanaskovic2015`, `bayar2019`, `koju2018`, `zawadzki2023` | Obradović a 2.5 con «morosidad bancaria (NPL)» como dependiente; frecuencias reemplazadas por «no especificada en el resumen leído»; «Resumen» actualizado |
| 2 | CAMBIOS NECESARIOS | Signo de la asociación principal no especificado en `asiamah2026` y `koskei2023` (RF-22); frase de `wu2016` reinterpretada; `duffie1999` sin encaje en 2.2; claves con varios apellidos (RF-10) | `wu2016` con cita literal; Duffie y Singleton descartado; claves normalizadas a apellidoaño; Asiamah y Koskei pasan a `pendiente-lectura` y salen del `.bib` (sus textos completos no son accesibles y no se declaró un signo no respaldado) |
| 3 | CAMBIOS NECESARIOS | `nkusu2011` con sección principal 2.2 (estima coeficientes: es 2.5, y deja 2.2 con 1 estudio); `golitsis2022` atribuía significancia 0,01 al desempleo (es 0,05) | Nkusu a 2.5; `pesaran2006` entra como segundo estudio de 2.2; significancias de Golitsis corregidas con cita a la Tabla 4 |
| 4 | **APROBADO** | Ninguno | — |

## Verificado de forma independiente en la ronda 4

- Los 19 DOI del `.bib` existen en Crossref y coinciden con la matriz en título, primer autor, año y revista (comprobados sin fiarse del script).
- `scripts/verify_refs.py`: «Verificadas 21 de 21 entradas», código 0. `uv run pytest -q`: 187 passed.
- `frb2026` responde 200 y su contenido coincide con la matriz; `fred2026` se verifica con la URL del CSV vía `requests`, la página de la serie y `data/raw/manifest.csv` (13 series, descarga del 2026-10-02).
- Los hallazgos, signos, frecuencias, países y períodos de las filas verificadas salen de sus resúmenes. En `golitsis2022` se leyó además el texto completo (PDF de acceso abierto en EconStor): Tabla 4 con desempleo 0,6417 (p = 0,0495), tasas de interés 3,4731 (p < 0,01) y PIB −6,7075.
- Conteo y mínimos (RF-5, RF-6, RF-7): 2.1 = 2, 2.2 = 2, 2.3 = 2, 2.4 = 2, 2.5 = 9 y 4 de datos/método; 17 estudios más 4. La tabla «Resumen» coincide con el conteo real.
- Las 21 claves de la matriz coinciden con las del `.bib` y siguen el patrón apellidoaño (RF-9, RF-10, RF-12).
- Filas de 2.5: sin «no aplica» en las columnas obligatorias y con signo en el Hallazgo (RF-22).
- Filas `pendiente-lectura` y `descartado` (`salas2002`, `borio2012`, `louzis2012`, `ghosh2015`, `beck2015`, `jimenez2014a`, `asiamah2026`, `koskei2023`, `wilson1997`, `virolainen2004`, `duffie1999`): ninguna atribuye hallazgos con signo y ninguna está en el `.bib`.

## Observaciones no bloqueantes (para tratar al escribir el informe, spec 006)

1. `bernanke1995` es 2.1 con 2.4 secundaria; su resumen es de transmisión monetaria (canal del crédito). Reasignarlo dejaría 2.1 con 1 estudio: justificar la asignación en el informe o añadir otro estudio de 2.1.
2. `pesaran2006` y `segoviano2006` (2.2) podrían reclamarse como 2.5 por modelar vínculos macro-crédito, aunque sus resúmenes hablan de modelización y no de coeficientes sobre morosidad; `gertler2015` estima efectos sobre diferenciales, no sobre morosidad. Con la lectura actual los mínimos se cumplen; una reasignación rompería el de 2.2.
3. `koju2018`: el conteo de variables macroeconómicas en «Regresores» podría ser seis cuando el resumen dice cinco; el diferencial de tipos mapeado a `tasa_politica` es una asignación laxa.
4. `tanaskovic2015`: el «más fuerte en periodos de depreciación» del resumen se aplica al ratio de préstamos en moneda extranjera, no al tipo de cambio.
5. `nkusu2011`: País dice «no especificada en el resumen leído», pero el título dice «Advanced Economies» (podría ponerse «economías avanzadas»).
6. `jimenez2014a` queda `pendiente-lectura` por falta de lista de autores en Crossref, aunque OpenAlex sí publica el resumen de la versión publicada; podría completarse como fila 2.5 con signo.
7. `obradovic2026`: el signo positivo del tipo de lending es una lectura razonable del resumen, que no usa la palabra «positive».

## Limitaciones

- Dos estudios (`asiamah2026`, `koskei2023`) quedaron fuera de los conteos por no poder respaldar el signo; si se accede a sus textos completos se pueden recuperar.
- Los motivos de descarte y la ausencia de resumen de las filas no verificadas no se re-comprobaron en detalle: solo que no atribuyen hallazgos.
