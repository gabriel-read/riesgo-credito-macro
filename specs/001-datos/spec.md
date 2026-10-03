# Spec 001 — Datos
Estado: aprobada · Crítica: no

## Contexto y objetivo
Todas las specs posteriores (literatura aparte) dependen de un mismo panel trimestral de series de FRED. Esta spec fija cómo se obtienen, se congelan, se transforman y se diagnostican esos datos, de modo que cualquiera pueda reproducir el panel desde las descargas guardadas y que ninguna cifra del informe dependa de un dato editado, imputado o descargado de nuevo sin registro.

Objetivo: un pipeline de datos reproducible que entregue (a) las descargas crudas con fecha y su manifiesto, (b) un panel trimestral 2000T1–último trimestre común, (c) estadísticos descriptivos, (d) pruebas ADF y KPSS con la decisión niveles o diferencias por variable, (e) un gráfico de morosidad, desempleo y tasa de fondos federales con recesiones sombreadas, y (f) un notebook de demostración.

## Pregunta que responde (y sección de docs/guia-profesor.md que cubre)
¿Qué datos usa la investigación, con qué frecuencia, período y fuente, y cómo se preparan para estimar? Cubre las secciones 3.1 (descripción de los datos), 3.2 (variable dependiente), 3.3 (variables macroeconómicas), 3.4 (política monetaria) y 11 (base de datos y descarga de información).

## Usuarios
- El autor de la investigación, que ejecuta el pipeline y redacta el informe.
- Las specs 003, 004 y 005 (modelos y estrés), que consumen el panel y la decisión niveles o diferencias.
- El profesor evaluador, que puede revisar el notebook de demostración y la nota de datos.

## Historias de usuario
- HU-1. Como autor, quiero guardar cada descarga de FRED con su fecha y un manifiesto para poder demostrar con qué datos se obtuvo cada resultado, aunque FRED revise las series después.
- HU-2. Como autor, quiero un panel trimestral con las transformaciones candidatas ya calculadas para que las specs de modelos elijan sin volver a tocar los datos.
- HU-3. Como autor, quiero que el pipeline se detenga con un error claro ante cualquier faltante no documentado para no estimar sobre datos rellenados en silencio.
- HU-4. Como autor, quiero una decisión niveles o diferencias por variable, fijada por una regla escrita de antemano, para que la elección no dependa de los resultados de los modelos.
- HU-5. Como profesor, quiero un notebook que reproduzca el ejemplo de descarga de la guía y muestre el panel final para verificar la preparación de los datos sin tener que ejecutar el pipeline completo.

## Definiciones
- **Trimestre**: se identifica como AAAAT# (por ejemplo, 2026T2). FRED lo fecha en el primer día del trimestre (2026-04-01 = 2026T2).
- **Series principales**: DRALACBS, GDPC1, GDP, UNRATE, CPIAUCSL, FEDFUNDS y LOANS. Solo ellas fijan el final de la muestra.
- **Series de robustez**: DRALACBN, DRCLACBS, DRBLACBS, DRSREACBS y CORALACBS. USREC solo se usa para sombrear recesiones en gráficos.
- **Marcador de faltante de FRED**: el punto «.», la cadena vacía y NaN.
- **Historia descargada**: desde 1998-01-01 hasta la última observación descargada de cada serie.
- **Trimestre completo**: aquel en que cada serie principal tiene dato; en las mensuales, los tres meses, salvo la excepción documentada de 2025T4 (octubre 2025) en CPIAUCSL y UNRATE, y solo en esas dos.
- **Último trimestre común**: el último trimestre completo en las siete series principales (2026T2 a la fecha de esta spec). Un trimestre final con menos de tres meses (y que no sea la excepción documentada) no pertenece a la muestra. Las series de robustez y USREC no recortan la muestra (RF-25).
- **Muestra de estimación**: de 2000T1 al último trimestre común.
- **Forma tal cual y primera diferencia (para ADF y KPSS)**: la forma tal cual de una variable es su columna del panel de RF-9 (por ejemplo, la variación interanual del IPC, no el nivel de la serie original). Su primera diferencia es la diferencia trimestral de esa columna, calculada sobre la historia descargada. Las columnas de diferencia trimestral del panel no se prueban aparte, porque ya son la primera diferencia de otra columna.
- **Variación interanual**: 100·(ln X(t) − ln X(t−4)).
- **Logit de la morosidad**: ln(DR/(100 − DR)), con DR en porcentaje.
- **Regla de decisión niveles o diferencias (pre-registrada)**: una prueba «rechaza» si p < 0,05 y «no rechaza» si p ≥ 0,05. Una serie se considera estacionaria y se usa tal cual (niveles) solo si la prueba ADF rechaza raíz unitaria (p < 0,05) **y** KPSS no rechaza estacionariedad (p ≥ 0,05). Si ADF no rechaza y KPSS rechaza, la serie tiene raíz unitaria y se usa en primera diferencia. Si las dos pruebas se contradicen (ambas rechazan o ninguna rechaza), la serie se marca «ambigua» y se usa en primera diferencia. Esta regla no puede modificarse tras ver los resultados sin pasar por `/sdd-change`.
- **Especificación de las pruebas (pre-registrada)**: ADF con constante y sin tendencia, rezagos elegidos por AIC con máximo de 4; KPSS con constante y ancho de banda automático de Newey-West.

## Requisitos funcionales

### Descarga y congelación
- RF-1: CUANDO se ejecute la etapa de datos, EL SISTEMA descargará desde 1998-01-01 las 13 series: DRALACBS, DRALACBN, DRCLACBS, DRBLACBS, DRSREACBS, GDPC1, GDP, UNRATE, CPIAUCSL, FEDFUNDS, LOANS, CORALACBS y USREC.
- RF-2: SI la descarga principal de una serie falla, ENTONCES EL SISTEMA usará el CSV público de FRED para esa serie y registrará la fuente usada.
- RF-3: SI también falla el CSV público, ENTONCES EL SISTEMA se detendrá con un error que nombre la serie y no registrará esa serie en el manifiesto.
- RF-4: EL SISTEMA guardará cada descarga cruda con el nombre de la serie y la fecha de descarga, sin editarla ni sobrescribir descargas anteriores.
- RF-5: EL SISTEMA registrará en un manifiesto, por cada descarga: serie, fecha de descarga, fuente (principal o CSV público), número de filas, primera observación y última observación.
- RF-6: EL SISTEMA construirá el panel con la descarga registrada más reciente de cada serie.
- RF-7: SI una descarga no trae filas, no cubre desde 1998-01-01 o trae valores no numéricos distintos del marcador de faltante de FRED («.», cadena vacía o NaN), ENTONCES EL SISTEMA se detendrá con un error que nombre la serie. Los valores con el marcador de faltante se tratan como faltantes (RF-13).

### Panel trimestral
- RF-8: EL SISTEMA agregará las series mensuales (UNRATE, CPIAUCSL, FEDFUNDS, LOANS) por trimestre calendario con la media de sus meses. DRALACBS y las demás series trimestrales se toman sin agregar (dato de fin de periodo).
- RF-9: EL SISTEMA calculará, primero sobre la historia descargada completa (desde 1998) y antes de recortar a la muestra de estimación, las transformaciones siguientes, de modo que las variaciones interanuales y las diferencias no pierdan observaciones en 2000T1:
  - Morosidad (DRALACBS, DRALACBN, DRCLACBS, DRBLACBS, DRSREACBS): nivel, diferencia trimestral en pp y logit.
  - GDPC1, GDP, CPIAUCSL y LOANS: variación interanual.
  - UNRATE y FEDFUNDS: nivel y diferencia trimestral en pp.
  - CORALACBS: nivel.
  - USREC: indicador igual a 1 si algún mes del trimestre está en recesión, y 0 en otro caso.
- RF-10: DESPUÉS de calcular las transformaciones de RF-9, EL SISTEMA recortará el panel a la muestra de estimación.
- RF-11: SI la descarga de CPIAUCSL o la de UNRATE no trae octubre 2025, ENTONCES EL SISTEMA calculará el promedio de 2025T4 de esa serie con noviembre y diciembre y lo documentará en la nota de datos (RF-17). Esta excepción se limita a CPIAUCSL y UNRATE.
- RF-12: SI la descarga de CPIAUCSL o la de UNRATE ya trae octubre 2025, ENTONCES EL SISTEMA usará los tres meses y lo anotará en la nota de datos.
- RF-13: SI falta cualquier otro dato dentro de la muestra de estimación (un mes de una serie mensual, un trimestre de una serie trimestral, la cobertura de 2000T1, o octubre 2025 en una serie distinta de CPIAUCSL y UNRATE), ENTONCES EL SISTEMA se detendrá con un error que nombre la serie y el período. La única excepción es el faltante terminal de RF-25.
- RF-14: EL SISTEMA no imputará, interpolará, rellenará hacia adelante ni eliminará filas por faltantes en ninguna etapa.
- RF-15: SI el logit recibe una morosidad menor o igual que 0 o mayor o igual que 100, ENTONCES EL SISTEMA se detendrá con un error que nombre la serie y el trimestre.
- RF-25: SI una serie de robustez o USREC termina antes del último trimestre común, ENTONCES EL SISTEMA conservará los trimestres finales de esa serie con faltante explícito (sin imputar), no recortará la muestra principal y lo declarará en la nota de datos. En el gráfico de RF-22 el sombreado de recesiones termina donde termina USREC.

### Salidas
- RF-16: EL SISTEMA producirá un panel procesado con una fila por trimestre de la muestra de estimación y una columna por cada variable de RF-9.
- RF-17: EL SISTEMA producirá una nota de datos que registre, por cada serie descargada: la fuente (FRED y la vía de descarga usada), el código de FRED, la unidad, la frecuencia original, el rango descargado y su tratamiento trimestral (media del trimestre o dato de fin de periodo). Además registrará: el trimestre final de la muestra y el motivo; el tratamiento de 2025T4 (RF-11 o RF-12); la mezcla de datos de fin de periodo (morosidad) y promedios trimestrales (el resto); la justificación de LOANS como serie de crédito; y la explicación de por qué FEDFUNDS entra en nivel y en diferencia trimestral. La interpretación narrativa de las variables queda fuera de alcance (spec 006).
- RF-18: EL SISTEMA producirá una tabla de estadísticos descriptivos, por variable del panel excepto USREC: número de observaciones, media, desviación estándar, mínimo, mediana y máximo.
- RF-19: EL SISTEMA producirá una tabla de pruebas con ADF y KPSS aplicadas, en su forma tal cual y en primera diferencia (según Definiciones), a cada variable del panel excepto USREC y excepto las columnas de diferencia trimestral. Cada fila traerá el estadístico, el p-valor, los rezagos del ADF y la forma probada.
- RF-20: EL SISTEMA añadirá a la tabla de RF-19 la decisión niveles o diferencias de cada variable, aplicando la regla pre-registrada a su forma tal cual, con las categorías «niveles», «primera diferencia» y «ambigua (primera diferencia)».
- RF-21: EL SISTEMA añadirá a la tabla de RF-19 el orden de integración de cada variable: I(0) si la decisión es «niveles»; I(1) si no lo es y su primera diferencia cumple la regla de estacionariedad (ADF rechaza y KPSS no rechaza); «posible I(2)» en otro caso.
- RF-22: EL SISTEMA producirá un gráfico con la morosidad (DRALACBS), el desempleo (UNRATE) y la tasa de fondos federales (FEDFUNDS) desde 2000T1 hasta el último trimestre común, con los trimestres de recesión (USREC) sombreados, ejes y leyenda en español y un eje único en porcentaje.

### Notebook de demostración
- RF-23: EL SISTEMA incluirá un notebook educativo, con comentarios en español paso a paso, que reproduzca el ejemplo de la sección 11 de la guía (GDP, UNRATE, CPIAUCSL y FEDFUNDS, de 2000-01-01 a 2026-01-01) leyendo las descargas crudas congeladas, sin usar la red, y que muestre después el panel final de RF-16.
- RF-24: EL SISTEMA ejecutará el notebook de principio a fin sin errores desde las descargas crudas congeladas. SI no hay descargas crudas, ENTONCES el notebook se detendrá con un error claro que lo indique.

## Requisitos no funcionales
- RNF-1 (reproducibilidad): CUANDO el pipeline se ejecute dos veces sobre las mismas descargas crudas, EL SISTEMA producirá un panel y tablas idénticos (sin diferencias en `git diff`).
- RNF-2 (sin red en tests): MIENTRAS corran los tests, EL SISTEMA bloqueará cualquier acceso a la red; los tests de datos usan las descargas crudas congeladas.
- RNF-3 (tests de transformaciones y pruebas): cada transformación de RF-9 y la regla de RF-20 tendrán al menos un test con datos sintéticos de resultado conocido; no se prueban las funciones de las librerías.
- RNF-4 (guardarraíl de cifras): EL SISTEMA detectará como error del informe, con tests, cualquier cifra escrita a mano que coincida con `\d+[.,]\d+` (uno o más decimales) o con `\d+\s?%`; esto sustituye al patrón actual de dos o más decimales.
- RNF-5 (idioma): código e identificadores en inglés; etiquetas de tablas y gráficos, nota de datos y notebook en español.
- RNF-6 (separación de lógica): EL SISTEMA aislará el acceso a la red y al disco en la descarga y el pipeline; las transformaciones, las pruebas y la regla de decisión no accederán a red, disco ni gráficos (principios 1, 3 y 4 de la constitución).

## Casos límite
- Dos descargas de la misma serie el mismo día: la segunda no sobrescribe a la primera; el sistema informa y se detiene.
- FRED revisa valores históricos entre dos descargas: ambas permanecen guardadas y el panel usa la más reciente.
- FRED rellena octubre 2025 en el futuro: se usan los tres meses (RF-12).
- El último trimestre del calendario tiene datos mensuales incompletos en una serie principal (por ejemplo, 2026T3 con un solo mes): se excluye de la muestra y la nota de datos lo declara.
- Una serie de robustez o USREC no llega al último trimestre común: queda con faltante explícito, sin recortar la muestra (RF-25).
- Octubre 2025 falta en una serie distinta de CPIAUCSL y UNRATE: el pipeline se detiene (RF-13).
- Valores faltantes en el CSV de FRED con el marcador de faltante: se tratan como faltantes (RF-13), nunca como cero.
- La variación interanual de 2026T4 en adelante usará el 2025T4 promediado con dos meses; la nota de datos debe advertirlo.
- Una serie ambigua o con posible I(2): se informa y no se elimina del panel.

## Fuera de alcance
- Estimación de modelos, rezagos, proyecciones locales y pruebas de estrés (specs 003, 004 y 005).
- Revisión de literatura (spec 002) e informe y diapositivas (specs 006 y 007), incluida la interpretación narrativa de las variables.
- Extender la muestra a 1985 como robustez, mientras el profesor no lo acepte.
- Bases de datos con vintages históricos (ALFRED) o series de otros países.
- Ajuste de ADF y KPSS con tendencia, pruebas con quiebres estructurales y cointegración.
- Cualquier imputación, interpolación o suavizado de datos.

## Criterios de finalización
- Las 13 series figuran en el manifiesto, con fecha de descarga y primera y última observación (RF-5).
- El panel va de 2000T1 al último trimestre común de las series principales, sin huecos ni filas eliminadas (salvo el faltante terminal de RF-25), y 2025T4 está documentado (RF-10 a RF-17).
- Existen el panel, la nota de datos, la tabla de descriptivos, la tabla de ADF y KPSS con decisión y orden de integración, y el gráfico (RF-16 a RF-22).
- El notebook se ejecuta sin errores y sin red (RF-23, RF-24).
- `uv run pytest -q` en verde, sin red.
- `specs/001-datos/review-validate.md` con `VEREDICTO: APROBADO`.

## Desviaciones del pre-registro
(vacío)

## Dudas abiertas
- [NECESITA ACLARACIÓN] PIB real (GDPC1) o nominal (GDP, el de la guía) como variable principal. El panel trae ambos, así que no bloquea esta spec; lo deciden las specs 003 y 004.
- [NECESITA ACLARACIÓN] Si el profesor acepta la muestra desde 1985 como robustez, habrá que volver a descargar y abrir un `/sdd-change`, porque la descarga actual parte de 1998.
- [NECESITA ACLARACIÓN] Formato exigido del informe (Word o PDF) y de la exposición; no afecta esta spec.
