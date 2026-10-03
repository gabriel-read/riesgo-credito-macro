"""Tests de ``src/references.py`` (T1, spec 002-literatura): lectura y normalización.

Sin red ni disco: usan textos sintéticos.
"""

import pytest

from src.references import (
    MATRIX_COLUMNS,
    BibEntry,
    MatrixRow,
    first_author_surname,
    is_institutional,
    normalize_doi,
    normalize_surname,
    normalize_title,
    parse_bib,
    parse_markdown_table,
    parse_matrix,
)

BIB_TEXT = """% Comentario que se ignora.
@article{salas2002,
  author  = {Salas, Vicente and Saurina, Jesús},
  title   = {Credit risk in two institutional regimes: {S}panish commercial banks},
  journal = {Journal of Financial Services Research},
  year    = 2002,
  doi     = {10.1023/a:1020384016666},
}

% Otro comentario entre entradas.
@misc{frb2026,
  author = {{Board of Governors of the Federal Reserve System}},
  title  = {2026 Stress Test Scenarios},
  year   = {2026},
  url    = {https://www.federalreserve.gov/},
}
"""


def _matrix_text(rows: list[str] | None = None, summary_rows: list[str] | None = None) -> str:
    summary_rows = summary_rows if summary_rows is not None else ["| Fecha de verificación | 2026-10-05 |", "| 2.1 | 0 |"]
    rows = rows or []
    header = "| " + " | ".join(MATRIX_COLUMNS) + " |"
    separator = "|" + "---|" * len(MATRIX_COLUMNS)
    return "\n".join(
        ["# Matriz de literatura", "Texto introductorio.", "", "## Resumen", "| Concepto | Valor |", "|---|---|"]
        + summary_rows
        + ["", "## Matriz", header, separator]
        + rows
    )


def _row(**overrides: str) -> str:
    cells = {name: "x" for name in MATRIX_COLUMNS}
    cells.update(overrides)
    return "| " + " | ".join(cells[name] for name in MATRIX_COLUMNS) + " |"


# ---------------------------------------------------------------------------
# parse_bib
# ---------------------------------------------------------------------------

def test_parse_bib():
    """Dos entradas, comentarios %, llaves anidadas, número sin llaves e institucional."""
    entries = parse_bib(BIB_TEXT)

    assert [e.key for e in entries] == ["salas2002", "frb2026"]
    first, second = entries
    assert isinstance(first, BibEntry)
    assert first.entry_type == "article"
    assert first.fields["author"] == "Salas, Vicente and Saurina, Jesús"
    assert first.fields["title"] == "Credit risk in two institutional regimes: {S}panish commercial banks"
    assert first.fields["year"] == "2002"
    assert first.fields["doi"] == "10.1023/a:1020384016666"
    assert second.entry_type == "misc"
    assert second.fields["author"] == "{Board of Governors of the Federal Reserve System}"
    assert is_institutional(second.fields["author"])
    assert second.fields["url"] == "https://www.federalreserve.gov/"


def test_parse_bib_lowercases_type_and_field_names():
    (entry,) = parse_bib("@ARTICLE{a2001,\n  Title = {Foo},\n  YEAR = {2001}\n}")
    assert entry.entry_type == "article"
    assert set(entry.fields) == {"title", "year"}


def test_parse_bib_joins_multiline_values():
    (entry,) = parse_bib("@misc{a2001,\n  note = {Series A,\n    B, C},\n}")
    assert entry.fields["note"] == "Series A, B, C"


def test_parse_bib_empty_or_only_comments():
    assert parse_bib("") == []
    assert parse_bib("% solo un comentario UTF-8: tildes áéíóú\n") == []


def test_parse_bib_unclosed_entry_reports_line():
    with pytest.raises(ValueError, match=r"Línea 2.*no se cierra"):
        parse_bib("% c\n@article{a2001,\n  title = {foo}\n")
    with pytest.raises(ValueError, match="no se cierra"):
        parse_bib("@article{a2001, title = {foo")


def test_parse_bib_repeated_field_reports_line():
    with pytest.raises(ValueError, match=r"Línea 3.*'title' repetido"):
        parse_bib("@article{a2001,\n  title = {foo},\n  title = {bar}\n}")


def test_parse_bib_quoted_value_reports_line():
    with pytest.raises(ValueError, match=r"Línea 1.*comillas"):
        parse_bib('@article{a2001, title = "foo"}')
    with pytest.raises(ValueError, match=r"Línea 3.*comillas"):
        parse_bib('@article{a2001,\n  year = {2001},\n  title = "foo"\n}')


def test_parse_bib_rejects_text_outside_entries_and_bare_values():
    with pytest.raises(ValueError, match="Línea 1"):
        parse_bib("hola\n@article{a2001, year = 2001}")
    with pytest.raises(ValueError, match="Línea 1"):
        parse_bib("@article{a2001, year = jan}")


# ---------------------------------------------------------------------------
# parse_matrix y parse_markdown_table
# ---------------------------------------------------------------------------

def test_parse_matrix():
    """Resumen y Matriz: cabecera exacta, celdas sin espacios en los bordes y n.º de línea."""
    text = _matrix_text(
        rows=[
            _row(**{"Clave": "fred2026", "Autor(es) y año": "  Federal Reserve Bank of St. Louis (2026)  "}),
            _row(**{"Clave": "frb2026", "Método": "no aplica"}),
        ]
    )
    summary, rows = parse_matrix(text)

    assert summary == {"Fecha de verificación": "2026-10-05", "2.1": "0"}
    assert len(rows) == 2
    assert isinstance(rows[0], MatrixRow)
    assert list(rows[0].cells) == MATRIX_COLUMNS
    assert rows[0].cells["Clave"] == "fred2026"
    assert rows[0].cells["Autor(es) y año"] == "Federal Reserve Bank of St. Louis (2026)"
    assert rows[1].cells["Método"] == "no aplica"
    lines = text.splitlines()
    assert "fred2026" in lines[rows[0].line - 1]
    assert "frb2026" in lines[rows[1].line - 1]


def test_parse_matrix_empty_template_has_no_rows():
    summary, rows = parse_matrix(_matrix_text())
    assert rows == []
    assert summary["2.1"] == "0"


def test_parse_matrix_keeps_empty_cells():
    """Las celdas vacías se conservan: `validate_matrix` (T2) las reporta (RF-4)."""
    _, rows = parse_matrix(_matrix_text(rows=[_row(**{"País": ""})]))
    assert rows[0].cells["País"] == ""
    assert len(rows[0].cells) == len(MATRIX_COLUMNS)


def test_parse_matrix_escaped_pipe_is_literal():
    _, rows = parse_matrix(_matrix_text(rows=[_row(Regresores="a \\| b")]))
    assert rows[0].cells["Regresores"] == "a | b"


def test_parse_matrix_unescaped_pipe_reports_line():
    text = _matrix_text(rows=[_row(Regresores="a | b")])
    with pytest.raises(ValueError, match=r"Línea \d+.*«\|» sin escapar"):
        parse_matrix(text)


def test_parse_matrix_wrong_header_shows_expected():
    text = _matrix_text().replace("| País |", "| Pais |")
    with pytest.raises(ValueError) as excinfo:
        parse_matrix(text)
    assert "Esperada" in str(excinfo.value)
    assert "País" in str(excinfo.value)


def test_parse_matrix_missing_sections_raise():
    with pytest.raises(ValueError, match="Resumen"):
        parse_matrix("# Matriz de literatura\n\n## Matriz\n| a |\n|---|\n")
    with pytest.raises(ValueError, match="Matriz"):
        parse_matrix("## Resumen\n| Concepto | Valor |\n|---|---|\n")


def test_parse_matrix_wrong_summary_columns_raise():
    text = _matrix_text().replace("| Concepto | Valor |", "| Clave | Cantidad |")
    with pytest.raises(ValueError, match="Resumen"):
        parse_matrix(text)


def test_parse_markdown_table():
    rows = parse_markdown_table(["| a | b |", "|---|:--:|", "| 1 | 2 |", "", "| 3 |  |"])
    assert rows == [{"a": "1", "b": "2"}, {"a": "3", "b": ""}]
    assert parse_markdown_table([]) == []


def test_parse_markdown_table_errors():
    with pytest.raises(ValueError, match="separadora"):
        parse_markdown_table(["| a | b |", "| 1 | 2 |"])
    with pytest.raises(ValueError, match="incompleta"):
        parse_markdown_table(["| a | b |"])
    with pytest.raises(ValueError, match="Línea 3"):
        parse_markdown_table(["| a | b |", "|---|---|", "| 1 |"])


# ---------------------------------------------------------------------------
# Normalización
# ---------------------------------------------------------------------------

def test_normalize_doi():
    assert normalize_doi("https://doi.org/10.1016/J.X") == "10.1016/j.x"
    assert normalize_doi("http://dx.doi.org/10.1016/J.X") == "10.1016/j.x"
    assert normalize_doi("HTTPS://DOI.ORG/10.1016/J.X") == "10.1016/j.x"
    assert normalize_doi("doi:10.1016/J.X") == "10.1016/j.x"
    assert normalize_doi("10.1016/j.x") == "10.1016/j.x"
    assert normalize_doi("  https://doi.org/ 10.1016/J.X  ") == "10.1016/j.x"
    assert normalize_doi("") == ""


def test_normalize_title():
    assert normalize_title("{\\`a} Jordà: \"Estudio <i>empírico</i>\" & más") == "a jorda estudio empirico mas"
    assert normalize_title("Estudio de {Jord\\'a} y {S}alas") == "estudio de jorda y salas"
    assert normalize_title("A, B: C & D (2020).") == "a b c d 2020"
    assert normalize_title("<em>Prueba</em> con HTML.") == "prueba con html"
    assert normalize_title("&iacute;ndice de precios.") == "indice de precios"
    assert normalize_title("{\\textbf{Negrita} y {\\`e}}") == "negrita y e"
    assert normalize_title("  Credit   risk\n and  macro ") == "credit risk and macro"
    assert normalize_title("") == ""


def test_normalize_surname():
    assert normalize_surname("Jordà") == normalize_surname("JORDA") == "jorda"
    assert normalize_surname("de la Fuente") == "delafuente"
    assert normalize_surname("DE LA FUENTE") == "delafuente"
    assert normalize_surname("Jiménez") == "jimenez"
    assert normalize_surname("Peydró") == "peydro"


def test_first_author_surname():
    assert first_author_surname("Salas, Vicente and Saurina, Jesús") == "Salas"
    assert first_author_surname("Salas, Vicente, and Saurina, Jesús") == "Salas"
    assert first_author_surname("Jiménez, Santiago and Ongena, Steven") == "Jiménez"
    assert first_author_surname("Wu, Xia") == "Wu"
    assert first_author_surname("Vicente Salas and Jesús Saurina") == "Salas"
    assert first_author_surname("{de la Fuente}, Juan and Wu, Xia") == "de la Fuente"
    assert (
        first_author_surname("{{Board of Governors of the Federal Reserve System}}")
        == "Board of Governors of the Federal Reserve System"
    )
    # Valor tal como lo devuelve parse_bib (sin el par de llaves externas).
    assert first_author_surname("{Johnson and Johnson}") == "Johnson and Johnson"
    assert first_author_surname("") == ""


def test_is_institutional():
    assert is_institutional("{{Board of Governors of the Federal Reserve System}}")
    assert is_institutional("{Federal Reserve Bank of St. Louis}")
    assert not is_institutional("Salas, Vicente and Saurina, Jesús")
    assert not is_institutional("{de la Fuente}, Juan")
    assert not is_institutional("{A} and {B}")
    assert not is_institutional("")
