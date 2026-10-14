# Investigación de entradas y procedencia de generación — ronda 7

El registro de ronda 6 no bastaba para acreditar las fuentes posteriores al ajuste de Claude. La única diferencia al recibir turno fue 02, con SHA completa documentada en la cesión. Las otras 489 entradas del manifiesto R6 coincidían; se conservaron los entregables y la evidencia histórica antes de regenerar.

## Preparación observada

La primera preparación, conservada en `docs/preliminar-006-ronda7/preparacion-render-006-ronda7.json`, registra 369 entradas con SHA antes/después de cada paso y sus diferencias completas:

1. `uv run python -m src.pipeline report`: 19 productos generados cambiaron desde las correcciones autorizadas. Son versiones de tablas del cuerpo y del anexo, sus notas y trazas, el registro de fuentes, la literatura derivada y la alternativa combinada. No hay cambios inesperados; variables y fuentes científicas permanecen iguales.
2. Render de preparación del PDF del anexo: cero entradas distintas antes/después. El PDF es una salida, registrada como tal en la entrega final.
3. `uv run python -m src.pipeline report`: cero diferencias. El mapa de destinos se recalculó desde el nuevo PDF; sus páginas no cambiaron respecto del mapa previo. No se afirma un cambio de contenido del mapa que no ocurrió.

Las 19 diferencias son explicables por R5-1–R5-5 y el ajuste recibido de 02; no son prueba de reproducibilidad. La lectura de los DOCX/GFM preliminares detectó un rótulo redundante adicional del Modelo II. Se añadió su regresión, se corrigió el rótulo, y se puso mayúscula a la primera letra del fragmento incorporado de Obradović, sin cambiar su contenido. Las versiones y evidencias preliminares se conservaron; no se acreditan como entrega final.

La preparación posterior definitiva, `docs/preparacion-render-006-ronda7.json`, reconstruye ocho productos derivados: nota de literatura y su CSV/Markdown, registro/trazas y rótulo de desviaciones del Modelo II. Las 369 entradas se registran antes/después; no hay cambios inesperados ni cambios numéricos/científicos. El mapa de páginas permanece igual. La suite completa se reinicia sobre las fuentes corregidas antes de generar la entrega definitiva. Cada versión anterior/posterior queda ligada por SHA completo, no por fechas.

## Generación final

`docs/render-006-ronda7-final.json` y `docs/render-006-ronda7-repetida.json` deben acreditar cero diferencias de entrada en cada comando y el mismo conjunto de entradas entre los ocho renders. Ante cualquier diferencia, el ejecutor detiene la afirmación de reproducibilidad para investigarla. Los PDF/DOCX se comparan por todos los objetos/miembros de contenido; solo se permiten diferencias de fechas e identificadores temporales de metadatos. GFM se compara por bytes.

El manifiesto final vuelve a cotejar ese conjunto de entradas y registra las seis salidas con SHA-256 completo. La huella final de una fuente o su fecha de modificación aislada no sustituye el registro de generación. No se modificaron contratos ni fuentes científicas protegidas.

## Diagnóstico de la comprobación de clics

El cálculo inicial del desplazamiento visible difería unos píxeles del navegador aunque las páginas de destino coincidían. La inspección de los métodos nativos y una pulsación de diagnóstico registraron los argumentos de `goToPageAndXY`: corresponden a las coordenadas del destino PDF. No se modificó el enlace ni se llamó al método para simular navegación.

La comprobación final captura ese método únicamente cuando lo llama un clic real, compara página y coordenadas con el destino extraído del PDF (tolerancia de coordenadas 0,01 píxeles CSS) y registra el movimiento observado. El desfase de separadores se documenta aparte; no se sustituye el clic por una comprobación estructural. Los diagnósticos preliminares no acreditan los PDF definitivos; estos deben tener sus propios registros de clics ligados a sus SHA.
