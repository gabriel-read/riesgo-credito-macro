# Reparaciones del arnés — propuesta histórica y resultado autorizado

Estado actual: H1/H2 autorizadas y aplicadas. H2 se aprobó después de la solicitud de revisión conservada abajo. Catálogo contrastado con contratos 001–005, siete negativos primero en rojo y después verdes, fixture optimizado y suite completa **905 passed, 567 warnings, 963,43 s, rc0**, sin exclusiones. Sin cambios de estimadores, dependencias ni salidas científicas. Evidencia: `docs/validacion-h2-006-2026-10-12.json` y `docs/pytest-completo-h2-006-2026-10-12.log`. Los párrafos de propuesta/no aplicación son antecedentes, no el estado vigente. Sin commit ni push.

## H1. Playbook histórico ausente

Ruta: `C:/Users/gabri/orca/riesgo-credito-macro/Playbook agéntico SDD riesgo de crédito.md`. El índice de Git todavía registra el archivo, blob `9695dd9b8224e683d3e7fb92de6912c72883ac5c`; el checkout lo muestra como **D**, eliminación local sin commit. HEAD sigue en `7a3dd2a`. El historial consultado no contiene un commit de eliminación; último commit que afectó esa ruta: `a39311e`, 4-oct-2026, migración a Orca/OpenRouter.

Última evidencia de presencia en esta sesión: el estado Git del cierre técnico de T4 lo mostraba **M**, no eliminado. Primera evidencia de ausencia: fallo de la suite iniciada a las 13:33 del 12-oct y consulta directa de la ruta entre 13:35–13:36. Por tanto, puede acotarse la desaparición a ese intervalo entre observaciones, **no determinar su instante exacto ni su autor**. Git no registra la hora de borrar un archivo sin commit.

No hubo coincidencia del nombre en la papelera visible de Windows. El índice de sesiones de Orca informa `enabled: false`, cero archivos indexados: no se activó ni se sustituyó por una búsqueda indiscriminada de logs. La respuesta del autor a la pregunta sobre intención fue **«No lo sé»**. La eliminación intencional no está acreditada.

Dos enlaces siguen apuntando al archivo: `README.md` y `docs/flujo-codex-orca.md`. Falla `tests/test_codex_harness.py::test_sdd_procedure_and_operator_guide_local_links_resolve`; el test exige que todos los destinos locales existan y no debe relajarse.

### Reparación propuesta para aprobar después de aclarar

- Si el archivo debía conservarse: recuperar la versión local anterior desde un respaldo verificable, **sin sustituir posibles modificaciones locales por HEAD silenciosamente**. En su defecto, el autor debe autorizar explícitamente recuperar la base versionada del blob indicado y reconocer que las modificaciones locales anteriores no están recuperadas.
- Si el autor decide mantener la eliminación: conservar el antecedente versionado bajo `docs/historial/` y actualizar solo los enlaces de README/guía para apuntar a ese archivo; documentar la procedencia y el límite de las modificaciones locales no recuperadas. No sustituir el test por una excepción a enlaces rotos.
- Comprobar bytes/procedencia y destinos de enlaces; ejecutar el test del arnés sin red. La ruta de reparación y la decisión de conservación requieren aprobación separada. Ninguna opción se aplicó.

## H2. Optimización de `tests/test_frozen_stress.py`

Defecto de coste: el fixture copia **todo** `outputs/`, incluidas maquetas, páginas PNG, propuestas y archivos QA de 006. Al verificar preservación ejecuta `digests(root/'outputs')` dentro del generador de `all(...)`, una vez por cada archivo protegido. Esto recalcula las mismas huellas repetidamente y mezcla productos QA ajenos a estrés con sus insumos científicos.

Inventario observado en la copia: `outputs/smoke-006` tenía 581 archivos y unos 115 MB; tablas originales 69 archivos/237 KB, modelos dos JSON/11 KB y figuras diez archivos/1 MB, incluidos `.gitkeep`. Son magnitudes observadas para explicar el coste, no resultados científicos del informe.

### Cambio propuesto (solo test; no aplicado)

1. Copiar `data/raw`, `data/scenarios`, `data/processed` y variables canónicas como antes. Para salidas, usar un catálogo explícito de rutas de los contratos 001–005 en `outputs/models`, `outputs/tables`, `outputs/figures` y `outputs/data_note.md` si existe, no un `copytree(outputs)` ni una aceptación ciega de cualquier archivo en esas carpetas. **No copiar** `outputs/informe`, `outputs/smoke-006`, `outputs/preview-006`, propuestas ni artefactos QA. Las derivaciones editoriales de 006, como `lit_estudios`, se delimitan explícitamente fuera del fixture de estrés y se verifican en sus tests propios. Un archivo inesperado en un directorio científico debe identificarse o rechazarse, no incluirse como QA ni eximirse silenciosamente. Comprobar que el inventario esperado no queda vacío y que están todos los insumos requeridos por `stage_stress`.
2. Definir las salidas modificables por **rutas exactas**, a partir de `STRESS_TABLES` (CSV/MD de las ocho tablas) y los dos PNG de estrés. Sustituir la exclusión amplia `name.startswith('stress_')` por ese conjunto exacto: un archivo inesperado con ese prefijo no debe quedar exento de preservación.
3. Calcular `before_outputs`, `first_outputs` y `second_outputs` **una sola vez por fase**. Reutilizar los diccionarios; no volver a leer todos los archivos por cada comparación.
4. Exigir conjuntos de rutas idénticos donde corresponda y coincidencia de SHA para **todos** los archivos científicos fuera de las salidas modificables exactas. Una desaparición, modificación o incorporación inesperada debe fallar. Mantener íntegra la comparación entre las dos corridas de estrés y del YAML, además de la preservación de datos y bloques `datos`, `modelo1`, `modelo2`.
5. Tests negativos independientes: modificar/eliminar un archivo protegido; añadir un archivo con prefijo `stress_` que no pertenezca al conjunto autorizado; introducir QA en origen y verificar que no se copia; omitir un insumo requerido. Todos deben demostrar las restricciones, sin reducir cobertura por conveniencia.

Archivos delimitados si se aprueba: `tests/test_frozen_stress.py` y un test auxiliar de inventarios (o funciones/tests en ese mismo archivo), más esta evidencia. No modifica código de aplicación, estimadores, contratos, CSV/JSON/PNG aprobados, raw, dependencias ni exclusiones de pytest.

Validación posterior: regresiones en rojo primero, pruebas del fixture y **`uv run pytest -q` completo, sin exclusiones**. La suite parcial solo comprueba trabajo en curso; no habilita T11 aprobada, auditoría final aprobada ni cierre 006. No se reutiliza una ejecución interrumpida como resultado verde.

## Pendientes separados del trabajo editorial

H1: el usuario autorizó recuperar solamente la base versionada. Codex extrajo los bytes mediante `git cat-file blob`, sin filtros y sin sobrescribir un archivo existente. Blob comprobado: `9695dd9b8224e683d3e7fb92de6912c72883ac5c`; SHA-256: `16bf3f2c1a824d7a5c51f79ee25732867d3baaa8af6d1906e23af5270cd2c1a1`; 30 992 bytes. La intención del borrado y las modificaciones locales anteriores siguen sin recuperarse. No cambió el test del arnés. Verificación focalizada conjunta: 67 passed, 5,44 s, incluyendo los enlaces del arnés.

H2, antecedente previo a la aprobación actual: el usuario solicitó **revisarla antes de aplicarla**. Entonces no existía autorización de implementación y el fixture estaba intacto, SHA-256 `c567016d13e93a5e32a3856dce690497d19d191f08b7e904efab6f5a89e1aad2`. Posteriormente autorizó el alcance y parche; las huellas aplicadas y pruebas se registran en la evidencia indicada en el encabezado.

### H2: inventario concreto para revisión

Parche de fixture **no aplicado**: `docs/frozen-stress-h2-propuesta.patch`. Muestra el catálogo literal, la copia selectiva, los conjuntos exactos y las tres lecturas de huellas. Es material de revisión, no resultado validado ni autorización. Antes de aplicarlo deben añadirse los negativos descritos arriba y comprobar su fallo inicial; después se ejecutará la suite completa. Ningún test existente se cambió para preparar este parche.

`docs/inventario-h2-propuesto-006-2026-10-12.json` enumera individualmente las **78 rutas científicas** actuales y sus huellas: dos JSON, 66 tablas CSV/MD, nueve PNG y `outputs/data_note.md`. Dentro de ellas enumera las **18 rutas modificables exactas**: ocho pares CSV/MD de estrés y dos PNG. El futuro código debe incorporar ese catálogo literal, contrastado con los contratos, sin descubrir salidas mediante un prefijo. Las huellas son evidencia del estado observado; no sustituyen la comparación antes/después de cada corrida.

Únicas exclusiones en directorios científicos: los dos archivos `lit_estudios` de 006 y marcadores `.gitkeep`. Cualquier otro archivo inesperado allí debe fallar. Los directorios editoriales/QA completos quedan fuera de la copia, aunque contengan nombres parecidos a salidas científicas. No se excluyen tablas, modelos ni figuras de 001–005.

Secuencia propuesta: validar catálogo y presencia → copiar rutas exactas → tomar huellas iniciales una vez → ejecutar estrés → tomar primeras huellas una vez y exigir preservación de las 60 rutas no modificables y conjunto completo de 78 rutas → ejecutar estrés otra vez → tomar segundas huellas una vez → exigir igualdad completa primera/segunda y YAML por bytes → comprobar datos y bloques no estrés. Los negativos simulan modificación, eliminación, alta inesperada `stress_*`, insumo ausente y QA en origen. Esta secuencia conserva las dos ejecuciones reales del pipeline y sus comprobaciones científicas.

Pendiente de aquel momento, ya resuelto: aprobación separada de H2, regresiones y suite completa. Claude terminó T5–T9 y devolvió el turno a Codex. T11 tiene ahora validación técnica aprobada; el cierre global conserva la revisión adicional de Google Docs, la auditoría independiente y las confirmaciones externas del profesor como pendientes, sin reapertura de 003–005.
