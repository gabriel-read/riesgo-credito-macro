"""Lectura, normalización, validación y comparación de la matriz de literatura y del ``.bib`` (spec 002).

Módulo puro: sin red, sin disco y sin ``src.pipeline``. Recibe textos y devuelve
estructuras; los errores de sintaxis son ``ValueError`` con el número de línea.
"""

import html
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class BibEntry:
    entry_type: str  # "article", "incollection", ... en minúsculas
    key: str
    fields: dict[str, str]  # nombre de campo en minúsculas -> valor sin las llaves externas


@dataclass(frozen=True)
class MatrixRow:
    cells: dict[str, str]  # cabecera exacta (§4 del plan) -> texto de la celda, sin espacios en los bordes
    line: int  # línea del archivo, para los mensajes


@dataclass(frozen=True)
class Mismatch:
    field: str  # "título" | "primer autor" | "año"
    bib_value: str
    crossref_value: str


MATRIX_COLUMNS = [
    "Clave",
    "Autor(es) y año",
    "País",
    "Frecuencia",
    "Período",
    "Variable dependiente",
    "Regresores",
    "Variables de la guía",
    "Método",
    "Hallazgo o aporte",
    "Sección principal",
    "Secciones secundarias",
    "Respalda",
    "Tipo",
    "Estado",
    "URL de verificación",
]
SECTIONS = ("2.1", "2.2", "2.3", "2.4", "2.5")
GUIDE_VARIABLES = {"pib", "desempleo", "inflacion", "tasa_politica", "credito", "otra"}
SUPPORTS = {"I", "II", "estres", "ninguno"}
STATES = {"verificado", "pendiente-lectura", "descartado"}
TYPES = {"estudio", "datos/método"}
NOT_APPLICABLE = "no aplica"
DATA_METHOD_KEYS = {"fred2026", "frb2026", "newey1987", "jorda2005"}
KEY_PATTERN = r"^[a-z]+\d{4}[a-z]?$"
SIGN_WORDS = ("positivo", "negativo", "no significativo")

SUMMARY_COLUMNS = ["Concepto", "Valor"]


# ---------------------------------------------------------------------------
# Lectura del .bib
# ---------------------------------------------------------------------------

_ENTRY_HEAD = re.compile(r"@(\w+)\s*\{\s*([^,\s{}]+)\s*,")
_FIELD_HEAD = re.compile(r"([A-Za-z][\w-]*)\s*=\s*")
_NUMBER = re.compile(r"\d+")


def _closing_brace(text: str, start: int) -> int:
    """Índice de la llave que cierra la de ``text[start]``, o -1 si no se cierra."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def parse_bib(text: str) -> list[BibEntry]:
    """Lee un ``.bib`` restringido: valores entre llaves o números, sin ``@string``.

    Ignora las líneas que empiezan por ``%``. Lanza ``ValueError`` con el número
    de línea si una entrada no se cierra, un campo se repite o un valor va entre
    comillas. El valor de cada campo conserva las llaves internas: la
    ``{{Junta}}`` de un autor institucional queda como ``{Junta}``.
    """
    entries: list[BibEntry] = []
    size = len(text)
    pos = 0

    def line_at(index: int) -> int:
        return text.count("\n", 0, index) + 1

    while True:
        while pos < size:
            if text[pos].isspace():
                pos += 1
            elif text[pos] == "%":
                end = text.find("\n", pos)
                pos = size if end == -1 else end + 1
            else:
                break
        if pos >= size:
            break

        if text[pos] != "@":
            raise ValueError(f"Línea {line_at(pos)}: texto fuera de una entrada BibTeX.")
        head = _ENTRY_HEAD.match(text, pos)
        if head is None:
            raise ValueError(f"Línea {line_at(pos)}: cabecera de entrada no válida (se espera @tipo{{clave,).")
        entry_line = line_at(pos)
        entry_type, key = head.group(1).lower(), head.group(2)
        pos = head.end()
        fields: dict[str, str] = {}

        while True:
            while pos < size and (text[pos].isspace() or text[pos] == ","):
                pos += 1
            if pos >= size:
                raise ValueError(f"Línea {entry_line}: la entrada '{key}' no se cierra con «}}».")
            if text[pos] == "}":
                pos += 1
                break

            field_head = _FIELD_HEAD.match(text, pos)
            if field_head is None:
                raise ValueError(f"Línea {line_at(pos)}: campo no válido en la entrada '{key}'.")
            name = field_head.group(1).lower()
            pos = field_head.end()
            value_line = line_at(pos)
            if name in fields:
                raise ValueError(f"Línea {value_line}: campo '{name}' repetido en la entrada '{key}'.")
            if pos >= size:
                raise ValueError(f"Línea {entry_line}: la entrada '{key}' no se cierra con «}}».")

            if text[pos] == '"':
                raise ValueError(
                    f"Línea {value_line}: el campo '{name}' de '{key}' usa comillas; "
                    "los valores van entre llaves."
                )
            if text[pos] == "{":
                end = _closing_brace(text, pos)
                if end == -1:
                    raise ValueError(f"Línea {entry_line}: la entrada '{key}' no se cierra con «}}».")
                value = text[pos + 1 : end]
                pos = end + 1
            else:
                number = _NUMBER.match(text, pos)
                if number is None:
                    raise ValueError(
                        f"Línea {value_line}: valor no válido en el campo '{name}' de '{key}' "
                        "(entre llaves o un número)."
                    )
                value = number.group()
                pos = number.end()
            fields[name] = " ".join(value.split())

        entries.append(BibEntry(entry_type, key, fields))

    return entries


# ---------------------------------------------------------------------------
# Lectura de tablas Markdown y de la matriz
# ---------------------------------------------------------------------------

_SEPARATOR_CELL = re.compile(r"^:?-+:?$")


def _split_row(line: str) -> list[str]:
    """Celdas de una fila ``| a | b |``; ``\\|`` es una barra literal. Conserva las vacías."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", body)]


def _parse_table(numbered: list[tuple[int, str]]) -> tuple[list[str], list[tuple[int, dict[str, str]]]]:
    """Cabecera y filas (línea, dict) de una tabla dada como (n.º de línea, texto)."""
    if len(numbered) < 2:
        raise ValueError("Tabla incompleta: faltan la cabecera o la línea separadora.")
    header_line, header_text = numbered[0]
    header = _split_row(header_text)
    separator_line, separator_text = numbered[1]
    separator = _split_row(separator_text)
    if len(separator) != len(header) or not all(_SEPARATOR_CELL.match(c) for c in separator):
        raise ValueError(f"Línea {separator_line}: falta la línea separadora (|---|---|) bajo la cabecera.")

    rows = []
    for line_no, text in numbered[2:]:
        cells = _split_row(text)
        if len(cells) != len(header):
            raise ValueError(
                f"Línea {line_no}: la fila tiene {len(cells)} celdas y la cabecera {len(header)}; "
                "¿hay un «|» sin escapar?"
            )
        rows.append((line_no, dict(zip(header, cells))))
    return header, rows


def parse_markdown_table(lines: list[str]) -> list[dict[str, str]]:
    """Una tabla Markdown (cabecera, separador, filas) como lista de dicts por cabecera."""
    numbered = [(i + 1, line) for i, line in enumerate(lines) if line.strip()]
    if not numbered:
        return []
    _, rows = _parse_table(numbered)
    return [row for _, row in rows]


def _section_table(lines: list[str], heading: str) -> list[tuple[int, str]]:
    """Líneas de tabla (con su número) bajo ``heading``, hasta el siguiente encabezado."""
    start = next((i for i, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        raise ValueError(f"No se encontró la sección «{heading}».")
    block = []
    for i in range(start + 1, len(lines)):
        stripped = lines[i].strip()
        if re.match(r"#{1,6}\s", stripped):
            break
        if stripped.startswith("|"):
            block.append((i + 1, lines[i]))
    if not block:
        raise ValueError(f"La sección «{heading}» no tiene tabla.")
    return block


def parse_matrix(text: str) -> tuple[dict[str, str], list[MatrixRow]]:
    """Lee ``research/matriz-literatura.md``: (Resumen concepto -> valor, filas de la matriz)."""
    lines = text.splitlines()

    header, summary_rows = _parse_table(_section_table(lines, "## Resumen"))
    if header != SUMMARY_COLUMNS:
        raise ValueError(f"La tabla «Resumen» debe tener las columnas {SUMMARY_COLUMNS}; tiene {header}.")
    summary: dict[str, str] = {}
    for line_no, row in summary_rows:
        if row["Concepto"] in summary:
            raise ValueError(f"Línea {line_no}: concepto '{row['Concepto']}' repetido en el «Resumen».")
        summary[row["Concepto"]] = row["Valor"]

    header, matrix_rows = _parse_table(_section_table(lines, "## Matriz"))
    if header != MATRIX_COLUMNS:
        raise ValueError(
            "La cabecera de la «Matriz» no es la esperada.\n"
            f"Esperada: {MATRIX_COLUMNS}\n"
            f"Recibida: {header}"
        )
    return summary, [MatrixRow(cells=row, line=line_no) for line_no, row in matrix_rows]


# ---------------------------------------------------------------------------
# Normalización
# ---------------------------------------------------------------------------

_LATEX_ACCENT = re.compile(r"\\(?:['`^\"~=.]\s*\{?([A-Za-z])\}?|[cvuHk]\s*\{([A-Za-z])\})")
_LATEX_COMMAND = re.compile(r"\\[A-Za-z]+\*?")
_HTML_TAG = re.compile(r"<[^>]*>")


def _strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def normalize_doi(doi: str) -> str:
    """Minúsculas, sin espacios y sin ``https://doi.org/``, ``http://dx.doi.org/`` ni ``doi:``."""
    compact = re.sub(r"\s+", "", doi).lower()
    compact = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", compact)
    return re.sub(r"^doi:", "", compact)


def normalize_title(title: str) -> str:
    """Título comparable: sin LaTeX, llaves, HTML ni entidades; sin tildes ni puntuación; en minúsculas."""
    text = _LATEX_ACCENT.sub(lambda m: m.group(1) or m.group(2), title)
    text = _LATEX_COMMAND.sub("", text)
    text = text.replace("{", "").replace("}", "")
    text = _HTML_TAG.sub("", text)
    text = html.unescape(text)
    text = _strip_accents(text).lower()
    return re.sub(r"[\W_]+", " ", text).strip()


def normalize_surname(name: str) -> str:
    """Apellido comparable: sin tildes, en minúsculas y sin espacios."""
    return re.sub(r"\s+", "", _strip_accents(name).lower())


def is_institutional(author_field: str) -> bool:
    """``True`` si todo el campo ``author`` va entre un par de llaves: ``{{Junta}}`` o ``{Junta}``."""
    text = author_field.strip()
    if len(text) < 2 or text[0] != "{" or text[-1] != "}":
        return False
    return _closing_brace(text, 0) == len(text) - 1


def first_author_surname(author_field: str) -> str:
    """Apellido del primer autor; el nombre completo si el autor es institucional.

    ``"Salas, Vicente and Saurina, Jesús"`` -> ``"Salas"``;
    ``"{{Board of Governors}}"`` -> ``"Board of Governors"``.
    """
    text = author_field.strip()
    if is_institutional(text):
        return text.strip("{}").strip()
    first = re.split(r"\s+and\s+", text, maxsplit=1)[0]
    if "," in first:
        surname = first.split(",", 1)[0]
    else:
        parts = first.split()
        surname = parts[-1] if parts else ""
    return surname.replace("{", "").replace("}", "").strip()


# ---------------------------------------------------------------------------
# Validación de la matriz
# ---------------------------------------------------------------------------

_DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$")
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_FRED_KEY = "fred2026"
_SIGN_REQUIRED = (
    "País",
    "Frecuencia",
    "Período",
    "Variable dependiente",
    "Regresores",
    "Variables de la guía",
    "Método",
)


def _split_list(cell: str) -> list[str]:
    return [item.strip() for item in cell.split(",") if item.strip()]


def _valid_date(text: str) -> bool:
    if not _DATE_PATTERN.match(text):
        return False
    try:
        date.fromisoformat(text)
    except ValueError:
        return False
    return True


def validate_matrix(rows: list[MatrixRow]) -> list[str]:
    """Errores (en español) de la matriz; lista vacía si es correcta. RF-4, RF-10, RF-22 a RF-24."""
    errors: list[str] = []
    seen: dict[str, int] = {}

    for row in rows:
        c = row.cells
        key = c["Clave"]
        where = f"Línea {row.line} ({key})"

        for column in MATRIX_COLUMNS:
            if not c.get(column, "").strip():
                errors.append(f"{where}: la celda «{column}» está vacía (usa «{NOT_APPLICABLE}» si no tiene sentido).")

        if not re.match(KEY_PATTERN, key):
            errors.append(f"{where}: la clave no cumple apellidoaño en minúsculas (p. ej. salas2002).")
        if key in seen:
            errors.append(f"{where}: clave repetida (ya está en la línea {seen[key]}).")
        else:
            seen[key] = row.line

        state, kind, main = c["Estado"], c["Tipo"], c["Sección principal"]
        if state not in STATES:
            errors.append(f"{where}: Estado «{state}» no admitido; usa {sorted(STATES)}.")
        if kind not in TYPES:
            errors.append(f"{where}: Tipo «{kind}» no admitido; usa {sorted(TYPES)}.")
        if kind == "estudio" and main not in SECTIONS:
            errors.append(f"{where}: un estudio necesita Sección principal en {list(SECTIONS)}; tiene «{main}».")
        if kind == "datos/método":
            if main != NOT_APPLICABLE:
                errors.append(f"{where}: datos/método lleva Sección principal «{NOT_APPLICABLE}»; tiene «{main}».")
            if key not in DATA_METHOD_KEYS:
                errors.append(f"{where}: la clave de datos/método debe ser una de {sorted(DATA_METHOD_KEYS)}.")

        secondary = c["Secciones secundarias"]
        if secondary != NOT_APPLICABLE:
            items = _split_list(secondary)
            bad = [i for i in items if i not in SECTIONS]
            if bad or not items:
                errors.append(f"{where}: Secciones secundarias no válidas {bad or [secondary]}.")
            if main in items:
                errors.append(f"{where}: la sección secundaria no puede repetir la principal ({main}).")

        support = _split_list(c["Respalda"])
        bad = [i for i in support if i not in SUPPORTS]
        if bad or not support:
            errors.append(f"{where}: Respalda fuera de la lista {sorted(SUPPORTS)}: {bad or [c['Respalda']]}.")
        elif "ninguno" in support and len(support) > 1:
            errors.append(f"{where}: «ninguno» en Respalda solo puede ir solo.")

        strict = main == "2.5" and state == "verificado"  # D5: RF-22 solo a las verificadas
        guide = c["Variables de la guía"]
        if guide != NOT_APPLICABLE:
            items = _split_list(guide)
            bad = [i for i in items if i not in GUIDE_VARIABLES]
            if bad or not items:
                errors.append(
                    f"{where}: Variables de la guía fuera de la lista {sorted(GUIDE_VARIABLES)}: {bad or [guide]}."
                )

        if not c["URL de verificación"].startswith("https://"):
            errors.append(f"{where}: la URL de verificación debe empezar por https://.")

        if state == "descartado" and not c["Hallazgo o aporte"].startswith("Descartado: "):
            errors.append(f"{where}: una fila descartada debe empezar su Hallazgo con «Descartado: » y el motivo.")

        if strict:
            for column in _SIGN_REQUIRED:
                if c[column] == NOT_APPLICABLE:
                    errors.append(f"{where}: en 2.5 la columna «{column}» no admite «{NOT_APPLICABLE}».")
            finding = c["Hallazgo o aporte"].lower()
            if not any(word in finding for word in SIGN_WORDS):
                errors.append(f"{where}: en 2.5 el Hallazgo debe indicar el signo ({', '.join(SIGN_WORDS)}).")

    return errors


def summary_counts(rows: list[MatrixRow]) -> dict[str, int]:
    """Filas verificadas por sección principal (estudios) y de datos/método."""
    counts = {section: 0 for section in SECTIONS}
    counts["datos/método"] = 0
    for row in rows:
        c = row.cells
        if c["Estado"] != "verificado":
            continue
        if c["Tipo"] == "datos/método":
            counts["datos/método"] += 1
        elif c["Tipo"] == "estudio" and c["Sección principal"] in counts:
            counts[c["Sección principal"]] += 1
    return counts


def validate_summary(summary: dict[str, str], rows: list[MatrixRow]) -> list[str]:
    """Comprueba la tabla «Resumen» contra la matriz (RF-20)."""
    errors: list[str] = []
    stamp = summary.get("Fecha de verificación", "")
    if not _valid_date(stamp):
        errors.append(f"Resumen: «Fecha de verificación» debe ser AAAA-MM-DD válida; tiene «{stamp}».")
    for concept, expected in summary_counts(rows).items():
        raw = summary.get(concept)
        if raw is None:
            errors.append(f"Resumen: falta el concepto «{concept}» (la matriz tiene {expected}).")
            continue
        try:
            written = int(raw)
        except ValueError:
            errors.append(f"Resumen: «{concept}» debe ser un entero; tiene «{raw}».")
            continue
        if written != expected:
            errors.append(f"Resumen: «{concept}» dice {written} pero la matriz tiene {expected} verificadas.")
    return errors


def check_minimums(rows: list[MatrixRow]) -> list[str]:
    """Mínimos de RF-5, RF-6 y RF-7 sobre las filas verificadas."""
    errors: list[str] = []
    counts = summary_counts(rows)
    studies = sum(counts[section] for section in SECTIONS)
    if studies < 16:
        errors.append(f"Hay {studies} estudios verificados; el mínimo es 16.")
    for section in SECTIONS:
        minimum = 6 if section == "2.5" else 2
        if counts[section] < minimum:
            errors.append(f"La sección {section} tiene {counts[section]} estudios verificados; el mínimo es {minimum}.")
    verified_data = [
        r.cells["Clave"] for r in rows if r.cells["Tipo"] == "datos/método" and r.cells["Estado"] == "verificado"
    ]
    if len(verified_data) != len(DATA_METHOD_KEYS) or set(verified_data) != DATA_METHOD_KEYS:
        errors.append(
            f"Las referencias de datos/método verificadas deben ser exactamente {sorted(DATA_METHOD_KEYS)}; "
            f"hay {sorted(verified_data)}."
        )
    return errors


# ---------------------------------------------------------------------------
# Validación del .bib y coherencia con la matriz
# ---------------------------------------------------------------------------

_REQUIRED_FIELDS = {
    "article": ("author", "title", "journal", "year"),
    "incollection": ("author", "title", "booktitle", "year"),
    "techreport": ("author", "title", "institution", "year"),
    "misc": ("author", "title", "year", "url"),
}
_URL_ONLY_KEYS = {_FRED_KEY, "frb2026", "bcbs2018"}
_DOI_REQUIRED_KEYS = {"newey1987", "jorda2005"}


def validate_bib(entries: list[BibEntry], fred_series: list[str]) -> list[str]:
    """Errores del ``.bib``: claves, campos mínimos, DOI/URL y la referencia de FRED (RF-7, RF-10, RF-11, RF-25)."""
    errors: list[str] = []
    seen: set[str] = set()

    for entry in entries:
        f, key = entry.fields, entry.key
        if not re.match(KEY_PATTERN, key):
            errors.append(f"{key}: la clave no cumple apellidoaño en minúsculas.")
        if key in seen:
            errors.append(f"{key}: clave repetida en el .bib.")
        seen.add(key)

        required = _REQUIRED_FIELDS.get(entry.entry_type)
        if required is None:
            errors.append(f"{key}: tipo «{entry.entry_type}» no admitido; usa {sorted(_REQUIRED_FIELDS)}.")
        else:
            for name in required:
                if not f.get(name, "").strip():
                    errors.append(f"{key}: falta el campo «{name}» de @{entry.entry_type}.")

        if is_institutional(f.get("author", "")) and not f.get("url"):
            errors.append(f"{key}: un autor institucional exige el campo «url».")

        doi = f.get("doi")
        if doi is not None:
            if doi != normalize_doi(doi) or not _DOI_PATTERN.match(doi):
                errors.append(f"{key}: el DOI debe ir en minúsculas, sin prefijo y con forma 10.xxxx/...; tiene «{doi}».")
        elif not f.get("url"):
            errors.append(f"{key}: sin DOI exige el campo «url».")

        if key in _DOI_REQUIRED_KEYS and doi is None:
            errors.append(f"{key}: debe llevar el campo «doi».")
        if key in _URL_ONLY_KEYS:
            if not f.get("url"):
                errors.append(f"{key}: debe llevar el campo «url».")
            if doi is not None:
                errors.append(f"{key}: no lleva «doi»; se verifica por «url».")

        if key == _FRED_KEY:
            note = f.get("note", "")
            missing = [code for code in fred_series if not re.search(rf"\b{re.escape(code)}\b", note)]
            if missing:
                errors.append(f"{key}: la nota no nombra las series {missing}.")
            if not _valid_date(f.get("urldate", "")):
                errors.append(f"{key}: «urldate» debe ser AAAA-MM-DD válida; tiene «{f.get('urldate', '')}».")

    return errors


def check_coherence(rows: list[MatrixRow], entries: list[BibEntry]) -> list[str]:
    """Una entrada por fila verificada y viceversa; la URL de la matriz es la del DOI o la ``url`` (RF-9, RF-12)."""
    errors: list[str] = []
    verified = {r.cells["Clave"]: r for r in rows if r.cells["Estado"] == "verificado"}
    bib = {e.key: e for e in entries}

    for key in sorted(set(bib) - set(verified)):
        errors.append(f"{key}: entrada del .bib sin fila verificada en la matriz.")
    for key in sorted(set(verified) - set(bib)):
        errors.append(f"{key}: fila verificada sin entrada en el .bib.")

    for key in sorted(set(verified) & set(bib)):
        fields = bib[key].fields
        expected = f"https://doi.org/{fields['doi']}" if fields.get("doi") else fields.get("url", "")
        actual = verified[key].cells["URL de verificación"]
        if actual != expected:
            errors.append(f"{key}: la URL de verificación es «{actual}» y debería ser «{expected}».")
    return errors


# ---------------------------------------------------------------------------
# Crossref
# ---------------------------------------------------------------------------

_URL_SAFE = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-~/")


def crossref_url(doi: str) -> str:
    """URL de la API de Crossref para un DOI normalizado (codifica todo salvo ``/``)."""
    encoded = "".join(
        ch if ch in _URL_SAFE else "".join(f"%{b:02X}" for b in ch.encode("utf-8"))
        for ch in normalize_doi(doi)
    )
    return "https://api.crossref.org/works/" + encoded


def parse_crossref(text: str) -> dict | None:
    """El ``message`` si la respuesta es un único registro bien formado; si no, ``None``."""
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return None
    if not isinstance(data, dict):
        return None
    if "status" in data and data["status"] != "ok":
        return None
    message = data.get("message")
    if not isinstance(message, dict) or "items" in message:
        return None
    titles = message.get("title")
    if not isinstance(titles, list) or not titles or not isinstance(titles[0], str) or not titles[0].strip():
        return None
    return message


def crossref_years(record: dict) -> set[int]:
    """Años de ``published-print``, ``published-online`` e ``issued``."""
    years: set[int] = set()
    for field in ("published-print", "published-online", "issued"):
        value = record.get(field)
        parts = value.get("date-parts") if isinstance(value, dict) else None
        if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
            year = parts[0][0]
            if isinstance(year, int) and not isinstance(year, bool):
                years.add(year)
    return years


def _crossref_first_author(record: dict) -> str:
    authors = [a for a in record.get("author") or [] if isinstance(a, dict)]
    if not authors:
        return ""
    chosen = next((a for a in authors if a.get("sequence") == "first"), authors[0])
    return str(chosen.get("family") or chosen.get("name") or "")


def compare_record(entry: BibEntry, record: dict) -> list[Mismatch]:
    """Un ``Mismatch`` por cada campo (título, primer autor, año) que no coincide con Crossref."""
    mismatches: list[Mismatch] = []

    bib_title = entry.fields.get("title", "")
    titles = record.get("title") or [""]
    cr_title = titles[0] if isinstance(titles[0], str) else ""
    t_bib, t_cr = normalize_title(bib_title), normalize_title(cr_title)
    if not t_bib or not t_cr or (t_bib not in t_cr and t_cr not in t_bib):
        mismatches.append(Mismatch("título", bib_title, cr_title))

    bib_author = first_author_surname(entry.fields.get("author", ""))
    cr_author = _crossref_first_author(record)
    if not bib_author or normalize_surname(bib_author) != normalize_surname(cr_author):
        mismatches.append(Mismatch("primer autor", bib_author, cr_author))

    bib_year = entry.fields.get("year", "")
    years = crossref_years(record)
    if not bib_year.isdigit() or int(bib_year) not in years:
        mismatches.append(Mismatch("año", bib_year, ", ".join(str(y) for y in sorted(years))))

    return mismatches
