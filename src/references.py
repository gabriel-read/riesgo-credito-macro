"""Lectura y normalización de la matriz de literatura y del ``.bib`` (spec 002).

Módulo puro: sin red, sin disco y sin ``src.pipeline``. Recibe textos y devuelve
estructuras; los errores de sintaxis son ``ValueError`` con el número de línea.
"""

import html
import re
import unicodedata
from dataclasses import dataclass


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
