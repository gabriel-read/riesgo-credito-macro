"""Tests de ``src/references.py`` (T1 y T2, spec 002-literatura).

Sin red ni disco: usan textos sintéticos.
"""

import pytest

from src.references import (
    MATRIX_COLUMNS,
    BibEntry,
    MatrixRow,
    Mismatch,
    check_coherence,
    check_minimums,
    compare_record,
    crossref_url,
    crossref_years,
    first_author_surname,
    is_institutional,
    normalize_doi,
    normalize_surname,
    normalize_title,
    parse_bib,
    parse_markdown_table,
    parse_crossref,
    parse_matrix,
    summary_counts,
    validate_bib,
    validate_matrix,
    validate_summary,
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


# ---------------------------------------------------------------------------
# T2: validación de la matriz
# ---------------------------------------------------------------------------

def _mrow(line: int = 10, **overrides: str) -> MatrixRow:
    """Fila válida de un estudio verificado de 2.1; ``overrides`` cambia celdas."""
    cells = {
        "Clave": "salas2002",
        "Autor(es) y año": "Salas y Saurina (2002)",
        "País": "no aplica",
        "Frecuencia": "no aplica",
        "Período": "no aplica",
        "Variable dependiente": "no aplica",
        "Regresores": "no aplica",
        "Variables de la guía": "no aplica",
        "Método": "no aplica",
        "Hallazgo o aporte": "Aporte descrito en una línea.",
        "Sección principal": "2.1",
        "Secciones secundarias": "no aplica",
        "Respalda": "I",
        "Tipo": "estudio",
        "Estado": "verificado",
        "URL de verificación": "https://doi.org/10.1023/a:1020384016666",
    }
    cells.update(overrides)
    return MatrixRow(cells=cells, line=line)


def _empirical(key: str = "louzis2012", **overrides: str) -> MatrixRow:
    base = {
        "Clave": key,
        "País": "Grecia",
        "Frecuencia": "trimestral",
        "Período": "2003T1-2009T3",
        "Variable dependiente": "morosidad",
        "Regresores": "PIB, desempleo",
        "Variables de la guía": "pib, desempleo",
        "Método": "panel dinámico GMM",
        "Hallazgo o aporte": "Negativo: el PIB reduce la morosidad.",
        "Sección principal": "2.5",
    }
    base.update(overrides)
    return _mrow(**base)


def test_validate_matrix_valid_rows():
    assert validate_matrix([_mrow(), _empirical()]) == []


def test_validate_matrix_empty_cell():
    errors = validate_matrix([_mrow(**{"Método": ""})])
    assert any("«Método» está vacía" in e for e in errors)


def test_validate_matrix_bad_key_and_duplicate():
    errors = validate_matrix([_mrow(Clave="Salas_2002"), _mrow(line=11), _mrow(line=12)])
    assert any("la clave no cumple" in e for e in errors)
    assert any("clave repetida (ya está en la línea 11)" in e for e in errors)


def test_validate_matrix_lists_out_of_vocabulary():
    errors = validate_matrix([_mrow(**{"Variables de la guía": "pib, gdp"}), _mrow(Clave="a2001", Respalda="III")])
    assert any("Variables de la guía" in e and "gdp" in e for e in errors)
    assert any("Respalda" in e and "III" in e for e in errors)


def test_validate_matrix_ninguno_must_be_alone():
    errors = validate_matrix([_mrow(Respalda="I, ninguno")])
    assert any("«ninguno»" in e for e in errors)


def test_validate_matrix_state_type_and_section():
    errors = validate_matrix(
        [_mrow(Estado="leido"), _mrow(Clave="a2001", Tipo="libro"), _mrow(Clave="b2001", **{"Sección principal": "3.1"})]
    )
    assert any("Estado «leido»" in e for e in errors)
    assert any("Tipo «libro»" in e for e in errors)
    assert any("Sección principal en" in e and "3.1" in e for e in errors)


def test_validate_matrix_data_method_rules():
    ok = _mrow(Clave="newey1987", Tipo="datos/método", **{"Sección principal": "no aplica"})
    assert validate_matrix([ok]) == []
    errors = validate_matrix([_mrow(Clave="otro2000", Tipo="datos/método")])
    assert any("Sección principal «no aplica»" in e for e in errors)
    assert any("clave de datos/método" in e for e in errors)


def test_validate_matrix_secondary_equal_to_main():
    errors = validate_matrix([_mrow(**{"Secciones secundarias": "2.1, 2.3"})])
    assert any("no puede repetir la principal" in e for e in errors)
    assert validate_matrix([_mrow(**{"Secciones secundarias": "2.2, 2.3"})]) == []


def test_validate_matrix_url_must_be_https():
    errors = validate_matrix([_mrow(**{"URL de verificación": "http://x.org"})])
    assert any("https://" in e for e in errors)


def test_validate_matrix_discarded_needs_reason():
    assert any("Descartado: " in e for e in validate_matrix([_mrow(Estado="descartado")]))
    ok = _mrow(Estado="descartado", **{"Hallazgo o aporte": "Descartado: el DOI no existe."})
    assert validate_matrix([ok]) == []


def test_validate_matrix_empirical_requires_columns_and_sign():
    errors = validate_matrix([_empirical(**{"Método": "no aplica"})])
    assert any("«Método» no admite" in e for e in errors)
    errors = validate_matrix([_empirical(**{"Hallazgo o aporte": "Relación fuerte."})])
    assert any("indicar el signo" in e for e in errors)
    # D5: una 2.5 pendiente-lectura no exige signo ni columnas obligatorias.
    pending = _empirical(Estado="pendiente-lectura", **{"Método": "no aplica", "Hallazgo o aporte": "Por leer."})
    assert validate_matrix([pending]) == []


# ---------------------------------------------------------------------------
# T2: resumen y mínimos
# ---------------------------------------------------------------------------

def _full_rows() -> list[MatrixRow]:
    rows = []
    for section, n in (("2.1", 3), ("2.2", 2), ("2.3", 2), ("2.4", 3)):
        for i in range(n):
            rows.append(_mrow(Clave=f"s{section.replace('.', '')}x{2000 + i}", **{"Sección principal": section}))
    for i in range(6):
        rows.append(_empirical(key=f"emp{2000 + i}"))
    for key in sorted(["fred2026", "frb2026", "newey1987", "jorda2005"]):
        rows.append(_mrow(Clave=key, Tipo="datos/método", **{"Sección principal": "no aplica"}))
    return rows


def test_summary_counts_only_verified():
    rows = [
        _mrow(),
        _mrow(Clave="a2001", Estado="descartado"),
        _empirical(),
        _empirical("b2001", Estado="pendiente-lectura"),
        _mrow(Clave="fred2026", Tipo="datos/método", **{"Sección principal": "no aplica"}),
    ]
    assert summary_counts(rows) == {"2.1": 1, "2.2": 0, "2.3": 0, "2.4": 0, "2.5": 1, "datos/método": 1}


def _summary(rows: list[MatrixRow], **overrides: str) -> dict[str, str]:
    summary = {"Fecha de verificación": "2026-10-05"}
    summary.update({k: str(v) for k, v in summary_counts(rows).items()})
    summary.update(overrides)
    return summary


def test_validate_summary_correct():
    rows = _full_rows()
    assert validate_summary(_summary(rows), rows) == []


def test_validate_summary_wrong_count_shows_both_values():
    rows = _full_rows()
    errors = validate_summary(_summary(rows, **{"2.3": "5"}), rows)
    assert len(errors) == 1
    assert "«2.3» dice 5 pero la matriz tiene 2" in errors[0]


def test_validate_summary_invalid_date_and_missing_concept():
    rows = _full_rows()
    summary = _summary(rows, **{"Fecha de verificación": "2026-13-45"})
    del summary["2.1"]
    errors = validate_summary(summary, rows)
    assert any("Fecha de verificación" in e for e in errors)
    assert any("falta el concepto «2.1»" in e for e in errors)
    assert any("entero" in e for e in validate_summary(_summary(rows, **{"2.2": "dos"}), rows))


def test_check_minimums_ok():
    assert check_minimums(_full_rows()) == []


def test_check_minimums_fifteen_studies():
    rows = _full_rows()
    rows.remove(next(r for r in rows if r.cells["Sección principal"] == "2.1"))  # 2.1 queda en 2
    errors = check_minimums(rows)
    assert errors == ["Hay 15 estudios verificados; el mínimo es 16."]


def test_check_minimums_section_23_with_one():
    rows = [r for r in _full_rows() if r.cells["Sección principal"] != "2.3"]
    rows.append(_mrow(Clave="x2003", **{"Sección principal": "2.3"}))
    errors = check_minimums(rows)
    assert any("sección 2.3 tiene 1" in e for e in errors)


def test_check_minimums_25_with_five():
    rows = _full_rows()
    rows.remove(next(r for r in rows if r.cells["Sección principal"] == "2.5"))
    assert any("sección 2.5 tiene 5" in e for e in check_minimums(rows))


def test_check_minimums_data_method_wrong():
    rows = [r for r in _full_rows() if r.cells["Clave"] != "jorda2005"]
    assert any("datos/método" in e for e in check_minimums(rows))
    rows.append(_mrow(Clave="otro2000", Tipo="datos/método", **{"Sección principal": "no aplica"}))
    assert any("datos/método" in e for e in check_minimums(rows))


# ---------------------------------------------------------------------------
# T2: validación del .bib y coherencia
# ---------------------------------------------------------------------------

FRED_CODES = ["DRALACBS", "GDPC1", "USREC"]


def _article(key: str = "salas2002", **overrides: str | None) -> BibEntry:
    fields = {"author": "Salas, Vicente", "title": "T", "journal": "J", "year": "2002", "doi": "10.1023/a:1020384016666"}
    fields.update(overrides)
    return BibEntry("article", key, {k: v for k, v in fields.items() if v is not None})


def _fred(**overrides: str | None) -> BibEntry:
    fields = {
        "author": "{Federal Reserve Bank of St. Louis}",
        "title": "FRED",
        "year": "2026",
        "url": "https://fred.stlouisfed.org/",
        "urldate": "2026-10-02",
        "note": "Series DRALACBS, GDPC1, USREC",
    }
    fields.update(overrides)
    return BibEntry("misc", "fred2026", {k: v for k, v in fields.items() if v is not None})


def test_validate_bib_valid():
    assert validate_bib([_article(), _fred()], FRED_CODES) == []


def test_validate_bib_missing_required_field():
    entry = BibEntry("article", "salas2002", {"author": "S", "title": "T", "year": "2002", "doi": "10.1023/x"})
    assert any("falta el campo «journal»" in e for e in validate_bib([entry], FRED_CODES))


def test_validate_bib_unsupported_type():
    entry = BibEntry("book", "salas2002", {"author": "S", "title": "T", "year": "2002", "url": "https://x.org"})
    assert any("tipo «book» no admitido" in e for e in validate_bib([entry], FRED_CODES))


def test_validate_bib_institutional_needs_url():
    fields = {"author": "{Comité de Basilea}", "title": "T", "institution": "BIS", "year": "2018", "doi": "10.1234/x1"}
    entry = BibEntry("techreport", "bcbs2018", fields)
    assert any("autor institucional exige" in e for e in validate_bib([entry], FRED_CODES))


def test_validate_bib_doi_form():
    errors = validate_bib([_article(doi="https://doi.org/10.1023/A:1020384016666")], FRED_CODES)
    assert any("el DOI debe ir en minúsculas, sin prefijo" in e for e in errors)


def test_validate_bib_without_doi_needs_url():
    errors = validate_bib([_article(doi=None)], FRED_CODES)
    assert any("sin DOI exige" in e for e in errors)
    assert validate_bib([_article(doi=None, url="https://x.org/a")], FRED_CODES) == []


def test_validate_bib_duplicate_and_bad_key():
    errors = validate_bib([_article(), _article(), _article("Salas_2002")], FRED_CODES)
    assert any("clave repetida" in e for e in errors)
    assert any("la clave no cumple" in e for e in errors)


def test_validate_bib_required_doi_and_url_only_keys():
    newey = _article("newey1987", doi=None, url="https://x.org/n")
    assert any("newey1987: debe llevar el campo «doi»" in e for e in validate_bib([newey], FRED_CODES))
    errors = validate_bib([_fred(doi="10.1234/abcd")], FRED_CODES)
    assert any("no lleva «doi»" in e for e in errors)


def test_validate_bib_fred_note_and_urldate():
    errors = validate_bib([_fred(note="Series DRALACBS, GDPC1")], FRED_CODES)
    assert any("USREC" in e for e in errors)
    assert any("urldate" in e for e in validate_bib([_fred(urldate="2 de octubre")], FRED_CODES))
    # GDP no debe darse por presente por estar GDPC1.
    assert any("GDP" in e for e in validate_bib([_fred(note="Series GDPC1")], ["GDP"]))


def test_check_coherence_ok():
    assert check_coherence([_mrow()], [_article()]) == []


def test_check_coherence_key_only_in_bib_or_matrix():
    errors = check_coherence([_mrow()], [_article("otro2001")])
    assert any("otro2001: entrada del .bib sin fila verificada" in e for e in errors)
    assert any("salas2002: fila verificada sin entrada" in e for e in errors)
    # Una fila pendiente-lectura o descartada no admite entrada.
    errors = check_coherence([_mrow(Estado="pendiente-lectura")], [_article()])
    assert any("sin fila verificada" in e for e in errors)


def test_check_coherence_verification_url():
    errors = check_coherence([_mrow(**{"URL de verificación": "https://doi.org/10.9999/otro"})], [_article()])
    assert any("la URL de verificación" in e for e in errors)
    row = _mrow(Clave="fred2026", **{"URL de verificación": "https://fred.stlouisfed.org/"})
    assert check_coherence([row], [_fred()]) == []


# ---------------------------------------------------------------------------
# T2: Crossref
# ---------------------------------------------------------------------------

def _record(**overrides) -> dict:
    record = {
        "title": ["Credit risk in two institutional regimes: Spanish commercial and savings banks"],
        "author": [
            {"family": "Saurina", "given": "Jesús", "sequence": "additional"},
            {"family": "Salas", "given": "Vicente", "sequence": "first"},
        ],
        "published-print": {"date-parts": [[2002, 6]]},
        "published-online": {"date-parts": [[2003]]},
        "issued": {"date-parts": [[2002, 6]]},
    }
    record.update(overrides)
    return record


def test_crossref_url_normalizes_and_encodes():
    assert crossref_url("https://doi.org/10.1016/J.X") == "https://api.crossref.org/works/10.1016/j.x"
    assert crossref_url("10.1002/(sici)1099<x>") == "https://api.crossref.org/works/10.1002/%28sici%291099%3Cx%3E"


def test_parse_crossref():
    good = '{"status": "ok", "message": {"title": ["T"], "DOI": "10.1/x"}}'
    assert parse_crossref(good) == {"title": ["T"], "DOI": "10.1/x"}
    for bad in (
        "no es json",
        "[]",
        '{"status": "failed"}',
        '{"message": []}',
        '{"message": {"title": []}}',
        '{"message": {"items": [], "title": ["T"]}}',
        '{"message": {}}',
    ):
        assert parse_crossref(bad) is None


def test_crossref_years():
    assert crossref_years(_record()) == {2002, 2003}
    assert crossref_years({"issued": {"date-parts": [[1987]]}}) == {1987}
    assert crossref_years({"issued": {"date-parts": [[None]]}, "published-print": None}) == set()


def test_compare_record_matches():
    entry = _article(title="Credit risk in two institutional regimes", author="Salas, Vicente and Saurina, Jesús")
    assert compare_record(entry, _record()) == []


def test_compare_record_title_contained_both_ways():
    cr = _record()
    assert compare_record(_article(title="Credit risk in two institutional regimes", author="Salas, V"), cr) == []
    long = _article(
        title="Credit risk in two institutional regimes: Spanish commercial and savings banks (extended)",
        author="Salas, V",
    )
    assert compare_record(long, cr) == []
    other = compare_record(_article(title="Algo totalmente distinto", author="Salas, V"), cr)
    assert [m.field for m in other] == ["título"]
    assert other[0].bib_value == "Algo totalmente distinto" and other[0].crossref_value.startswith("Credit risk")


def test_compare_record_accented_surname_and_first_sequence():
    entry = _article(title="Credit risk in two institutional regimes", author="Jordà, Òscar")
    record = _record(author=[{"family": "Smith", "sequence": "additional"}, {"family": "JORDA", "sequence": "first"}])
    assert compare_record(entry, record) == []


def test_compare_record_author_mismatch_uses_first_sequence():
    entry = _article(title="Credit risk in two institutional regimes", author="Saurina, Jesús")
    assert compare_record(entry, _record()) == [Mismatch("primer autor", "Saurina", "Salas")]


def test_compare_record_author_without_sequence_or_family():
    entry = _article(title="Credit risk in two institutional regimes", author="{{Board}}")
    assert compare_record(entry, _record(author=[{"name": "Board"}])) == []
    assert [m.field for m in compare_record(entry, _record(author=[]))] == ["primer autor"]


def test_compare_record_year_online_differs_from_print():
    base = {"title": "Credit risk in two institutional regimes", "author": "Salas, V"}
    assert compare_record(_article(year="2003", **base), _record()) == []
    assert compare_record(_article(year="2004", **base), _record()) == [Mismatch("año", "2004", "2002, 2003")]


def test_compare_record_reports_all_fields():
    entry = _article(title="Otro", author="Nadie, Juan", year="1999")
    assert [m.field for m in compare_record(entry, _record())] == ["título", "primer autor", "año"]
