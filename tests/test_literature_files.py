"""Tests sobre los archivos reales de la literatura (T3, spec 002-literatura).

Leen ``research/matriz-literatura.md`` y ``report/references.bib`` desde el disco, sin red.
El test de mínimos (RF-5 a RF-7, ``check_minimums``) se añade en la última tarea del
bibliotecario (D14): antes, la matriz vacía no puede cumplirlos.
"""

from pathlib import Path

import pytest

from src.config import ALL_SERIES
from src.references import (
    check_coherence,
    parse_bib,
    parse_matrix,
    validate_bib,
    validate_matrix,
    validate_summary,
)

ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = ROOT / "research" / "matriz-literatura.md"
BIB_PATH = ROOT / "report" / "references.bib"


@pytest.fixture(scope="module")
def matrix():
    return parse_matrix(MATRIX_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def entries():
    return parse_bib(BIB_PATH.read_text(encoding="utf-8"))


def test_matrix_file_parses(matrix):
    summary, rows = matrix
    assert "Fecha de verificación" in summary


def test_matrix_is_valid(matrix):
    _, rows = matrix
    assert validate_matrix(rows) == []


def test_summary_matches_matrix(matrix):
    summary, rows = matrix
    assert validate_summary(summary, rows) == []


def test_bib_file_parses(entries):
    assert isinstance(entries, list)


def test_bib_is_valid(entries):
    assert validate_bib(entries, ALL_SERIES) == []


def test_matrix_and_bib_are_coherent(matrix, entries):
    _, rows = matrix
    assert check_coherence(rows, entries) == []
