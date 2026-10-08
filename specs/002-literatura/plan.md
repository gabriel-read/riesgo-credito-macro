# Plan 002 — Literatura
Estado: aprobada · Spec: `specs/002-literatura/spec.md` (aprobada, Crítica: no) · Depende de: spec 001 (solo `src.config.ALL_SERIES`, para la referencia de FRED)

Este plan fija el CÓMO de la spec 002. No cambia ningún requisito. Hay dos productos de naturaleza distinta:
- **Código** (implementer): un módulo puro que lee, valida y compara la matriz y el `.bib`, un script de verificación contra Crossref y sus tests sin red.
- **Contenido curado** (bibliotecario): la matriz y el `.bib`, buscados y verificados en Crossref y OpenAlex. El código no los genera; solo los comprueba.

Nada de esta spec entra en `src.pipeline` (spec, «Fuera de alcance»).

## 1. Módulos y responsabilidad

| Archivo | Responsabilidad | ¿Red/disco? | RF |
|---|---|---|---|
| `src/references.py` | Funciones puras: leer el texto del `.bib` y de la matriz, normalizar DOI, títulos y apellidos, validar la matriz y el `.bib`, contar el «Resumen», comprobar mínimos, interpretar una respuesta de Crossref y compararla con una entrada. | No | RF-4 a RF-13, RF-15, RF-20, RF-22 a RF-25, RNF-6 |
| `scripts/verify_refs.py` | Único archivo con red de esta spec: lee los dos archivos, consulta Crossref y las URL con reintentos, imprime en español y fija el código de salida. No escribe nada. | Sí (lectura y red) | RF-13 a RF-19 |
| `research/matriz-literatura.md` | Contenido curado: intro, tabla «Resumen» y tabla «Matriz» (formato en §4). | — | RF-1 a RF-8, RF-20 a RF-24 |
| `report/references.bib` | Contenido curado: una entrada por fila verificada. | — | RF-9 a RF-11, RF-25 |
| `tests/test_references.py` | Tests de las funciones puras con textos sintéticos. | No | RNF-6 |
| `tests/test_verify_refs.py` | Tests del script con un `fetch` y un `sleep` falsos inyectados. | No | RF-26, RNF-1 |
| `tests/test_literature_files.py` | Tests sobre los archivos reales de la matriz y el `.bib`. | Disco (lectura) | RF-4, RF-5 a RF-7, RF-9, RF-12, RF-20, RF-22 a RF-25 |
| `tests/test_pipeline.py` | Se añade `src/references.py` a las listas de módulos puros de `test_pipeline_modules_pure` y `test_pipeline_no_open_in_pure_modules`, y `urllib` y `socket` a los imports prohibidos de ese módulo. | — | RNF-6 |

`src/references.py` no importa `requests`, `urllib`, `socket`, `pathlib`, `src.pipeline` ni llama a `open`. Solo usa `re`, `json`, `html`, `unicodedata`, `dataclasses` y `datetime` de la biblioteca estándar.

## 2. Funciones y firmas

### `src/references.py` (puras)
```python
@dataclass(frozen=True)
class BibEntry:
    entry_type: str            # "article", "incollection", ... en minúsculas
    key: str
    fields: dict[str, str]     # nombre de campo en minúsculas -> valor sin las llaves externas

@dataclass(frozen=True)
class MatrixRow:
    cells: dict[str, str]      # cabecera exacta (§4) -> texto de la celda, sin espacios en los bordes
    line: int                  # línea del archivo, para los mensajes

@dataclass(frozen=True)
class Mismatch:
    field: str                 # "título" | "primer autor" | "año"
    bib_value: str
    crossref_value: str

# Lectura
def parse_bib(text: str) -> list[BibEntry]                     # ValueError con la línea si la sintaxis no se entiende
def parse_markdown_table(lines: list[str]) -> list[dict[str, str]]
def parse_matrix(text: str) -> tuple[dict[str, str], list[MatrixRow]]   # (Resumen concepto->valor, filas de la matriz)

# Normalización
def normalize_doi(doi: str) -> str          # minúsculas; quita "https://doi.org/", "http://dx.doi.org/", "doi:" y espacios
def normalize_title(title: str) -> str      # quita comandos LaTeX y llaves, etiquetas HTML, entidades; NFKD sin tildes; minúsculas; puntuación -> espacio; espacios colapsados
def normalize_surname(name: str) -> str     # NFKD sin tildes, minúsculas, sin espacios
def first_author_surname(author_field: str) -> str   # "Salas, Vicente and Saurina, Jesús" -> "Salas"; "{{Board of ...}}" -> "Board of ..."
def is_institutional(author_field: str) -> bool      # author entre dobles llaves

# Validación (devuelven una lista de errores en español; vacía = correcto)
def validate_matrix(rows: list[MatrixRow]) -> list[str]        # RF-4, RF-10, RF-22, RF-23, RF-24, estados, tipos, secciones
def summary_counts(rows: list[MatrixRow]) -> dict[str, int]    # {"2.1": n, ..., "2.5": n, "datos/método": n}
def validate_summary(summary: dict[str, str], rows: list[MatrixRow]) -> list[str]   # RF-20
def check_minimums(rows: list[MatrixRow]) -> list[str]         # RF-5, RF-6, RF-7
def validate_bib(entries: list[BibEntry], fred_series: list[str]) -> list[str]     # RF-10, RF-11, RF-25, FRED de RF-7
def check_coherence(rows: list[MatrixRow], entries: list[BibEntry]) -> list[str]   # RF-9, RF-12

# Crossref
def crossref_url(doi: str) -> str                    # "https://api.crossref.org/works/" + quote(normalize_doi(doi), safe="/")
def parse_crossref(text: str) -> dict | None         # el `message` si es un único registro bien formado; si no, None
def crossref_years(record: dict) -> set[int]         # años de published-print, published-online e issued
def compare_record(entry: BibEntry, record: dict) -> list[Mismatch]   # RF-13, RF-15, según «Coincidencia»
```

Constantes del módulo: `MATRIX_COLUMNS` (las 16 cabeceras de §4, en orden), `SECTIONS = ("2.1", ..., "2.5")`, `GUIDE_VARIABLES = {"pib", "desempleo", "inflacion", "tasa_politica", "credito", "otra"}`, `SUPPORTS = {"I", "II", "estres", "ninguno"}`, `STATES = {"verificado", "pendiente-lectura", "descartado"}`, `TYPES = {"estudio", "datos/método"}`, `NOT_APPLICABLE = "no aplica"`, `DATA_METHOD_KEYS = {"fred2026", "frb2026", "newey1987", "jorda2005"}`, `KEY_PATTERN = r"^[a-z]+\d{4}[a-z]?$"`, `SIGN_WORDS = ("positivo", "negativo", "no significativo")`.

### `scripts/verify_refs.py` (entrada y salida)
```python
@dataclass(frozen=True)
class HttpResult:
    status: int | None         # None = timeout o fallo de conexión
    text: str

def http_get(url: str, timeout: float) -> HttpResult           # requests.get con User-Agent del proyecto; nunca lanza
def is_service_error(result: HttpResult) -> bool               # status None, 429 o 5xx
def get_with_retries(url, fetch, sleep, delays=(1, 2, 4), timeout=10) -> HttpResult | None
    # None = «no verificable» tras agotar los reintentos (RF-17)
def check_doi_entry(entry, fetch, sleep) -> tuple[str, list[str]]   # (estado, mensajes)
def check_url_entry(entry, fetch, sleep) -> tuple[str, list[str]]
def run(bib_text: str, fetch, sleep, out) -> int                # código de salida
def main(argv=None) -> int                                      # lee report/references.bib, llama a run con http_get y time.sleep
```
Estados por entrada: `"verificado"`, `"no existe"`, `"no coincide"`, `"sin url"`, `"url no responde"`, `"no verificable"`.

## 3. Algoritmo (pseudocódigo)

```
parse_bib(text):
  ignora líneas que empiezan por "%"
  por cada "@tipo{clave," : lee campos  nombre = {valor con llaves equilibradas}  o  nombre = número
  ValueError(línea) si una entrada no cierra, un campo se repite o un valor va entre comillas

parse_matrix(text):
  bloque tras "## Resumen" -> tabla de 2 columnas (Concepto | Valor) -> dict
  bloque tras "## Matriz"  -> tabla con cabecera == MATRIX_COLUMNS (si no, ValueError con la cabecera esperada)
  cada fila -> MatrixRow; una celda con "|" sin escapar rompe el número de columnas -> ValueError(línea)

validate_matrix(rows):
  para cada fila:
    toda celda no vacía                                                  # RF-4
    Clave cumple KEY_PATTERN y es única                                  # RF-10
    Estado ∈ STATES; Tipo ∈ TYPES
    si Tipo == "estudio": Sección principal ∈ SECTIONS
    si Tipo == "datos/método": Sección principal == "no aplica" y Clave ∈ DATA_METHOD_KEYS
    Secciones secundarias: "no aplica" o lista de SECTIONS sin la principal
    Respalda: lista ⊆ SUPPORTS; "ninguno" solo si va solo                # RF-24
    Variables de la guía: lista ⊆ GUIDE_VARIABLES, o "no aplica" fuera de 2.5   # RF-23
    URL de verificación empieza por "https://"
    si Estado == "descartado": Hallazgo empieza por "Descartado: "        # motivo de RF-2 (D4)
    si Estado == "verificado" y Sección principal == "2.5":               # RF-22
        País, Frecuencia, Período, Variable dependiente, Regresores, Variables de la guía, Método != "no aplica"
        Hallazgo contiene alguna de SIGN_WORDS (sin distinguir mayúsculas)

summary_counts(rows):  cuenta Estado == "verificado" por Sección principal (Tipo estudio) y por Tipo datos/método
validate_summary(summary, rows):                                          # RF-20
  "Fecha de verificación" es una fecha AAAA-MM-DD válida
  para cada concepto de summary_counts: int(summary[c]) == summary_counts(rows)[c]; si no, error con ambos valores

check_minimums(rows):                                                     # RF-5, RF-6, RF-7
  estudios verificados >= 16
  verificados por sección: 2.1–2.4 >= 2; 2.5 >= 6
  claves datos/método verificadas == DATA_METHOD_KEYS (exactamente 4)

validate_bib(entries, fred_series):                                       # RF-10, RF-11, RF-25
  clave cumple KEY_PATTERN y es única
  campos mínimos por tipo:
    article: author, title, journal, year · incollection: author, title, booktitle, year
    techreport: author, title, institution, year · misc: author, title, year, url
    otro tipo -> error «tipo no admitido»
  si is_institutional(author): exige url                                  # RF-25
  si tiene doi: doi == normalize_doi(doi) y cumple ^10\.\d{4,9}/\S+$      # D6
  si no tiene doi: exige url                                              # RF-11
  newey1987 y jorda2005 llevan doi; fred2026, frb2026 y bcbs2018 (si está) llevan url y no doi   # RF-11
  fred2026: note contiene cada código de fred_series y urldate es AAAA-MM-DD                     # RF-7

check_coherence(rows, entries):                                           # RF-9, RF-12
  V = claves con Estado verificado; B = claves del .bib
  error por cada clave de B − V («entrada sin fila verificada») y de V − B («fila verificada sin entrada»)
  para cada clave en V ∩ B: URL de verificación == "https://doi.org/" + doi si hay doi; si no, == url   # D7

compare_record(entry, record):                                            # «Coincidencia»
  t_bib = normalize_title(entry.title); t_cr = normalize_title(record.title[0])
  título coincide si t_bib ⊆ t_cr o t_cr ⊆ t_bib (como subcadena)
  autor Crossref = el de sequence == "first"; si no hay, author[0]; su "family" (o "name" si no hay family)
  apellido coincide si normalize_surname(first_author_surname(entry.author)) == normalize_surname(familia)
  año coincide si int(entry.year) ∈ crossref_years(record)
  devuelve un Mismatch por campo que falla, con ambos valores sin normalizar

get_with_retries(url, fetch, sleep, delays, timeout):                     # RF-17
  r = fetch(url, timeout)
  para d en delays:
     si no is_service_error(r) y (r.status != 200 o parse_ok(r)): return r
     sleep(d); r = fetch(url, timeout)
  return r si no es error de servicio, si no None
  # para Crossref, parse_ok = parse_crossref(r.text) no es None: un 200 sin registro único bien formado es error de servicio

check_doi_entry(entry):
  r = get_with_retries(crossref_url(entry.doi))
  None            -> "no verificable"                                     # RF-17
  status == 404   -> "no existe"                                          # RF-14
  status != 200   -> "no verificable"
  m = compare_record(entry, parse_crossref(r.text))
  m vacío -> "verificado"; si no -> "no coincide" con un mensaje por Mismatch   # RF-15

check_url_entry(entry):                                                   # RF-16
  sin url -> "sin url"
  r = get_with_retries(entry.url) (sin parse_ok)
  None -> "no verificable"; 200–299 -> "verificado"; otro -> "url no responde" con el código

run(bib_text, fetch, sleep, out):
  entries = parse_bib(bib_text)
  para cada entrada (orden del archivo): doi -> check_doi_entry; si no -> check_url_entry
  imprime una línea por entrada: "[OK] clave" o "[NO EXISTE] clave: el DOI 10.x no existe en Crossref", etc.
  imprime "Verificadas N de M entradas."                                  # RF-18
  return 0 si N == M, si no 1                                             # RF-14 a RF-17
  nunca escribe archivos                                                  # RF-19
```

Mensaje de «no coincide» (RF-15): `[NO COINCIDE] salas2002: año — .bib: «2003» · Crossref: «2002»`.

## 4. Salidas exactas

Esta spec no escribe en `outputs/` ni en `report/_variables.yml`: la matriz y el `.bib` son insumos curados (spec, «Contexto»). Los conteos los recalcula un test; no hay claves nuevas.

| Archivo | Contenido | Quién lo escribe |
|---|---|---|
| `research/matriz-literatura.md` | Formato de abajo. | bibliotecario (la plantilla vacía, el implementer en T2) |
| `report/references.bib` | UTF-8 con tildes literales; valores entre llaves; DOI sin prefijo. | bibliotecario |
| `scripts/verify_refs.py` | Script de §2. | implementer |
| `specs/002-literatura/review-validate.md` | Incluye la salida completa de `uv run python scripts/verify_refs.py` contra Crossref real y su código de salida. | validación (OpenCode) |

**Formato de `research/matriz-literatura.md`:**
```
# Matriz de literatura
<una o dos líneas: fuente de verdad, protocolo citas-apa, valores admitidos>

## Resumen
| Concepto | Valor |
|---|---|
| Fecha de verificación | 2026-10-05 |
| 2.1 | 2 |
| 2.2 | … |
| 2.3 | … |
| 2.4 | … |
| 2.5 | … |
| datos/método | 4 |

## Matriz
| Clave | Autor(es) y año | País | Frecuencia | Período | Variable dependiente | Regresores | Variables de la guía | Método | Hallazgo o aporte | Sección principal | Secciones secundarias | Respalda | Tipo | Estado | URL de verificación |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
```
Los valores del «Resumen» son ilustrativos: los escribe el bibliotecario y los comprueba `validate_summary`. Las filas de datos/método llevan Clave `fred2026`, `frb2026`, `newey1987` y `jorda2005`.

**Entrada de FRED (RF-7), forma esperada:**
```bibtex
@misc{fred2026,
  author  = {{Federal Reserve Bank of St. Louis}},
  title   = {Federal Reserve Economic Data (FRED)},
  year    = {2026},
  url     = {https://fred.stlouisfed.org/},
  urldate = {2026-10-02},
  note    = {Series DRALACBS, DRALACBN, ..., USREC}
}
```
La fecha de consulta es la de la descarga congelada de la spec 001 (`data/raw/manifest.csv`, 2026-10-02). Los códigos se copian de `src.config.ALL_SERIES`, y el test los compara con esa misma lista.

## 5. Integración en `src.pipeline`

Ninguna. La spec lo deja fuera de alcance: `src.pipeline` no lee ni regenera la matriz ni el `.bib`, y no llama a Crossref. Comandos de esta spec:
```
uv run pytest -q                          # coherencia y script, sin red
uv run python scripts/verify_refs.py      # verificación manual contra Crossref real (con red)
```
`scripts/` no es un paquete instalado; los tests lo importan como `scripts.verify_refs` gracias a `pythonpath = ["."]` (paquete de espacio de nombres, sin `__init__.py`).

## 6. Decisiones técnicas (con su alternativa descartada)

| # | Decisión | Por qué | Alternativa descartada |
|---|---|---|---|
| D1 | Lógica pura en `src/references.py`; red y disco solo en `scripts/verify_refs.py`. | RNF-6 y principio 3. El script queda en unas 80 líneas de E/S. | Todo en el script: no se puede probar sin simular archivos y mezcla lógica con E/S. |
| D2 | Lector de BibTeX propio y restringido (valores entre llaves, sin `@string`, sin comillas). | RNF-5: `bibtexparser` sería una dependencia nueva. El `.bib` lo escribe el proyecto, así que basta un subconjunto estricto que falle con la línea si algo no encaja. | Añadir `bibtexparser` (hay que preguntar y no hace falta). |
| D3 | HTTP con `requests` (ya en `pyproject.toml`), inyectado como `fetch(url, timeout) -> HttpResult`; `sleep` también inyectado. | RNF-5 y RF-26: los tests pasan un `fetch` falso y un `sleep` que anota las esperas, sin red ni demoras. El bloqueo de sockets de `conftest.py` hace fallar cualquier test que olvide inyectarlo. | `urllib.request` (más código para redirecciones y timeouts) o `responses`/`requests-mock` (dependencias nuevas). |
| D4 | El motivo del descarte (RF-2) va en la columna «Hallazgo o aporte», con el prefijo «Descartado: ». | RF-4 fija las 16 columnas y no hay columna de motivo; esa celda no tiene otro uso en una fila descartada. El prefijo permite comprobarlo por test. | Una columna «Motivo» extra: cambia RF-4 y exige `/sdd-change`. |
| D5 | RF-22 (columnas obligatorias y signo) se exige a las filas 2.5 **verificadas**; las pendiente-lectura y descartadas solo necesitan celdas no vacías. | RF-3 prohíbe escribir un hallazgo no leído: una fila pendiente-lectura no puede tener signo. Las verificadas son las que cuentan para RF-6. **Revísala**: es mi lectura de RF-22. | Exigir signo a toda fila 2.5: obligaría a inventar un signo en las pendientes, contra RF-3. |
| D6 | El campo `doi` se guarda sin prefijo y en minúsculas (`10.1016/...`); el test exige esa forma. El script normaliza igualmente (RF-13). | `apa.csl` añade `https://doi.org/` al render: un DOI con prefijo saldría duplicado en la spec 006. | Aceptar cualquier forma y normalizar solo en el script: el fallo se vería tarde, en el informe. |
| D7 | `check_coherence` también exige que la URL de verificación de la matriz sea `https://doi.org/<doi>` del `.bib`, o su `url`. | HU-4 y RF-12: el enlace que abre el profesor y el DOI comprobado contra Crossref son el mismo. Cuesta una línea. | Comparar solo claves: la matriz podría enlazar un DOI distinto del verificado. |
| D8 | Tipos BibTeX admitidos: `article`, `incollection` (los de RF-25), `techreport` (con `institution`) y `misc` (con `url`); cualquier otro falla. | RF-25 da los mínimos de `article` e `incollection`; FRED, la Fed y el Comité de Basilea necesitan `misc` o `techreport`. Una lista cerrada evita tipos que `apa.csl` formatea mal. | Admitir cualquier tipo sin campos mínimos: un `@online` o `@book` incompleto pasaría hasta la spec 006. |
| D9 | Año de Crossref = conjunto de años de `published-print`, `published-online` e `issued`. | El caso límite pide coincidir con impresa o en línea. `issued` es, según Crossref, la primera de las dos, así que no añade un año distinto, pero cubre artículos antiguos (Newey y West, 1987) que solo traen `issued`. | Solo `published-print`: falla en registros que solo traen `issued` o la fecha en línea. |
| D10 | Primer autor de Crossref = el de `sequence == "first"`; si no hay, el primero de la lista; si no hay `family`, se usa `name`. | Crossref no garantiza el orden de la lista; `sequence` lo marca. | Tomar siempre `author[0]`. |
| D11 | Reintentos: 1 intento + 3 reintentos (esperas 1, 2 y 4 s), timeout 10 s, también para las URL sin DOI. Un 200 de Crossref sin registro único bien formado cuenta como error de servicio. Un 404 nunca se reintenta. | Es la definición literal de RF-17 y de «Error de red o de servicio». Aplicarlo también a las URL evita que una caída momentánea de la Fed parezca «no responde». | Reintentar solo Crossref: una URL caída un segundo daría un falso «url no responde». |
| D12 | Una URL responde con éxito si da 2xx tras seguir redirecciones, con GET y `stream=True` (no descarga el cuerpo). 403 u otro 4xx = «url no responde» sin reintento. | Algunos servidores rechazan HEAD. No se baja el documento (fuera de alcance: no almacenar textos). | HEAD: falsos negativos en sitios que no lo admiten. |
| D13 | User-Agent `riesgo-credito-macro/0.1 (scripts/verify_refs.py)`, sin correo. | Crossref pide identificar al cliente; no se envían datos personales a un servicio externo. | Añadir `mailto=<correo>` para el «polite pool»: expone el correo del autor; con ~25 consultas no hace falta. |
| D14 | Los tests de archivos reales (`test_literature_files.py`) corren desde el principio sobre la plantilla vacía; el test de mínimos (RF-5 a RF-7) sobre los archivos reales se añade en la última tarea del bibliotecario. | Principio 4: nunca avanzar en rojo. Una matriz vacía con «Resumen» en cero y un `.bib` vacío son coherentes; los mínimos solo se cumplen al final. `check_minimums` sí se prueba desde el principio con filas sintéticas. | Test de mínimos desde T1: la suite estaría en rojo durante todo el trabajo bibliográfico. |
| D15 | La referencia de FRED toma la fecha de consulta de la descarga congelada (2026-10-02) y sus códigos de `src.config.ALL_SERIES`. | RF-7 y la definición «Series de FRED usadas»: si la spec 001 cambia la lista, el test lo detecta. | Escribir los 13 códigos solo en el test: se desincronizaría de `src/config.py`. |

## 7. Estrategia de tests (pytest, sin red)

No hay aleatoriedad: todos los insumos son textos fijos. Si algún test necesita orden aleatorio, usa `SEED = 20261003`. Ningún test llama a la red: el `fetch` falso devuelve `HttpResult` predefinidos por URL y el `conftest.py` de la spec 001 bloquea los sockets.

| Archivo | Qué prueba | RF |
|---|---|---|
| `tests/test_references.py` | `parse_bib`: dos entradas con llaves anidadas, comentario `%`, `{{Board of Governors...}}`; error con línea si no cierra o usa comillas. `parse_matrix`: «Resumen» y «Matriz»; cabecera distinta → error que muestra la esperada. `normalize_doi("https://doi.org/10.1016/J.X")` → `"10.1016/j.x"`. `normalize_title` quita tildes, `{\'e}`, `<i>` y puntuación. `normalize_surname("Jordà") == normalize_surname("JORDA")`; «de la Fuente» → «delafuente». `first_author_surname` con «Apellido, Nombre and …» e institucional. `validate_matrix`: celda vacía, valor fuera de lista en Variables de la guía y Respalda, clave inválida o duplicada, 2.5 verificada con «no aplica» en Método o sin signo, descartada sin «Descartado: », secundaria igual a la principal. `summary_counts`/`validate_summary` con conteo correcto e incorrecto y fecha inválida. `check_minimums`: 15 estudios → error; 2.3 con 1 → error; 2.5 con 5 → error; 3 datos/método → error; caso que cumple → `[]`. `validate_bib`: `article` sin `journal`, institucional sin `url`, DOI con prefijo, `newey1987` sin DOI, `fred2026` sin un código. `check_coherence`: clave solo en el `.bib`, solo en la matriz y URL de verificación distinta del DOI. `compare_record`: título contenido en ambos sentidos, apellido con tilde, año en `published-online` distinto de `published-print`, `sequence: first` fuera de la posición 0. | RF-4, RF-7, RF-9 a RF-13, RF-15, RF-20, RF-22 a RF-25, RNF-6 |
| `tests/test_verify_refs.py` | Con `run(bib_text, fake_fetch, fake_sleep, out)`: (1) DOI correcto → `[OK]`, código 0 y «Verificadas 1 de 1»; (2) 404 → «no existe», código ≠ 0, una sola llamada; (3) título distinto, (4) primer autor distinto y (5) año distinto → «no coincide», nombra el campo y ambos valores; (6) 503 persistente → «no verificable», 4 llamadas, `sleep` con `[1, 2, 4]`, código ≠ 0 y nunca `[OK]`; (6b) 503 y luego 200 → verificado; (6c) 200 con JSON inválido persistente → «no verificable»; (7) sin `doi` y con `url` 200 → `[OK]`; (8) sin `doi` ni `url` → «sin url», código ≠ 0. DOI con mayúsculas y prefijo en el `.bib` → se consulta la URL normalizada. El `.bib` de entrada no cambia tras `run` (RF-19). `fetch` recibe `timeout=10`. | RF-13 a RF-19, RF-26 |
| `tests/test_literature_files.py` | Sobre `research/matriz-literatura.md` y `report/references.bib` reales: `parse_matrix` y `parse_bib` no fallan; `validate_matrix`, `validate_summary`, `validate_bib(entries, ALL_SERIES)` y `check_coherence` devuelven `[]`. En la última tarea del bibliotecario se añade `check_minimums(rows) == []` (D14). | RF-4, RF-9, RF-12, RF-20, RF-22 a RF-25; RF-5 a RF-7 al final |
| `tests/test_pipeline.py` | `src/references.py` en las listas de módulos puros (sin `requests`, `urllib`, `socket` ni `open`). | RNF-6 |

## 8. Cobertura de RF

| RF / RNF | Parte del plan |
|---|---|
| RF-1, RF-3, RF-21, RNF-2 | Trabajo del bibliotecario (skill citas-apa: Crossref + OpenAlex, resumen leído de la versión publicada) · auditoría de `verificador-citas` al cierre |
| RF-2 | Fila «descartado» con «Descartado: <motivo>» · D4 · `validate_matrix` |
| RF-4 | Formato de §4 · `parse_matrix`, `validate_matrix` |
| RF-5, RF-6, RF-7 | `check_minimums` · D14, D15 · `validate_bib` (FRED) |
| RF-8 | Columna Método (contenido del bibliotecario; la revisa `verificador-citas`) |
| RF-9, RF-12 | `check_coherence` · D7 |
| RF-10 | `KEY_PATTERN` y unicidad en `validate_matrix` y `validate_bib` |
| RF-11 | `validate_bib` · D6 |
| RF-13 | `normalize_doi`, `crossref_url`, `compare_record` · D9, D10 |
| RF-14, RF-15 | `check_doi_entry` y mensajes de `run` |
| RF-16 | `check_url_entry` · D12 |
| RF-17 | `get_with_retries`, `is_service_error` · D11 |
| RF-18, RF-19 | `run` (resumen y código 0; sin escritura) |
| RF-20 | «Resumen» de §4 · `summary_counts`, `validate_summary` |
| RF-22, RF-23, RF-24 | `validate_matrix` · D5 |
| RF-25 | `validate_bib` · D8 |
| RF-26 | `tests/test_verify_refs.py` · D3 |
| RNF-1 | `fetch`/`sleep` inyectados · `conftest.py` de la spec 001 |
| RNF-3 | Identificadores en inglés; mensajes, matriz y docstrings en español |
| RNF-4 | Tarea final: `verificador-citas` recibe solo las dos rutas |
| RNF-5 | D2, D3: solo `requests` (ya instalado) y biblioteca estándar |
| RNF-6 | D1 · `src/references.py` puro · `test_pipeline.py` |

## 9. Orden sugerido para las tareas (lo detalla `/sdd-tasks`)
1. **implementer**: `src/references.py` (lectura, normalización, validación, mínimos, Crossref) con `tests/test_references.py` y la ampliación de `test_pipeline.py`.
2. **implementer**: plantilla de la matriz con las 16 columnas y el «Resumen» en cero (fecha = la del día), `.bib` solo con su comentario y `tests/test_literature_files.py` sin el test de mínimos.
3. **implementer**: `scripts/verify_refs.py` con `tests/test_verify_refs.py`.
4. **bibliotecario**: las 4 referencias de datos y método (RF-7).
5. **bibliotecario**: secciones 2.1 y 2.2 (≥ 2 cada una).
6. **bibliotecario**: secciones 2.3 y 2.4 (≥ 2 cada una).
7. **bibliotecario**: sección 2.5, primeros 3 estudios empíricos.
8. **bibliotecario**: sección 2.5, otros 3, y los que falten hasta 16 estudios; añade `check_minimums` al test de archivos reales; `verify_refs.py` contra Crossref real.
9. **claude**: auditoría de `verificador-citas` (solo rutas, RNF-4), con su informe guardado en `specs/002-literatura/`.

Cada tarea del bibliotecario termina con `uv run pytest -q` en verde (coherencia y «Resumen» al día) y con `uv run python scripts/verify_refs.py` sobre lo añadido.

## 10. Riesgos y notas
- La skill `citas-apa` describe una matriz antigua de 10 columnas. El bibliotecario sigue esa skill «al pie de la letra»: antes de `/fabrica` conviene actualizar su sección «Matriz» para que remita a este formato (§4). Lo hace Claude Code, porque el implementer no puede editar `.claude/`.
- Algunos sitios institucionales (bis.org, federalreserve.gov) pueden responder 403 a clientes que no son navegadores. Si pasa en la ejecución real, el script falla (D12) y se busca otra URL oficial que responda; nunca se marca como verificada a mano.
- `report/_variables.yml` dice hoy `n_series: '12'` y la spec 001 usa 13 series. No afecta a esta spec (la referencia de FRED lee `ALL_SERIES`), pero conviene revisarlo en la spec 006.
