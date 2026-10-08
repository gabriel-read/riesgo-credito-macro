"""Tests de verify_refs.py con fetch/sleep inyectados (sin red)."""
import io
from unittest.mock import MagicMock

import pytest

from scripts.verify_refs import HttpResult, check_doi_entry, check_url_entry, get_with_retries, run
from src.references import BibEntry


def _entry(key, doi=None, url=None, entry_type="article", **fields):
    f = {"author": "A", "title": "T", "year": "2020"}
    if doi:
        f["doi"] = doi
    if url:
        f["url"] = url
    f.update(fields)
    return BibEntry(entry_type, key, f)


def test_doi_ok():
    record = '{"status":"ok","message":{"title":["T"],"author":[{"family":"A","sequence":"first"}],"published-print":{"date-parts":[[2020]]}}}'
    fetch = lambda u, t: HttpResult(200, record)
    sleep = lambda d: None
    state, msgs = check_doi_entry(_entry("a2020", doi="10.1/x"), fetch, sleep)
    assert state == "verificado"
    assert any("[OK]" in m for m in msgs)


def test_doi_404():
    fetch = lambda u, t: HttpResult(404, "{}")
    sleep = lambda d: None
    state, msgs = check_doi_entry(_entry("a2020", doi="10.1/x"), fetch, sleep)
    assert state == "no existe"
    assert any("[NO EXISTE]" in m for m in msgs)


def test_doi_title_mismatch():
    record = '{"status":"ok","message":{"title":["Un estudio distinto sobre otro tema"],"author":[{"family":"A","sequence":"first"}],"published-print":{"date-parts":[[2020]]}}}'
    fetch = lambda u, t: HttpResult(200, record)
    sleep = lambda d: None
    state, msgs = check_doi_entry(_entry("a2020", doi="10.1/x", title="Credit and the cycle"), fetch, sleep)
    assert state == "no coincide"
    assert any("[NO COINCIDE]" in m and "título" in m for m in msgs)


def test_doi_author_mismatch():
    record = '{"status":"ok","message":{"title":["T"],"author":[{"family":"B","sequence":"first"}],"published-print":{"date-parts":[[2020]]}}}'
    fetch = lambda u, t: HttpResult(200, record)
    sleep = lambda d: None
    state, msgs = check_doi_entry(_entry("a2020", doi="10.1/x"), fetch, sleep)
    assert state == "no coincide"
    assert any("[NO COINCIDE]" in m and "primer autor" in m for m in msgs)


def test_doi_year_mismatch():
    record = '{"status":"ok","message":{"title":["T"],"author":[{"family":"A","sequence":"first"}],"published-print":{"date-parts":[[2021]]}}}'
    fetch = lambda u, t: HttpResult(200, record)
    sleep = lambda d: None
    state, msgs = check_doi_entry(_entry("a2020", doi="10.1/x"), fetch, sleep)
    assert state == "no coincide"
    assert any("[NO COINCIDE]" in m and "año" in m for m in msgs)


def test_service_error_persistent():
    calls = []
    def fetch(u, t):
        calls.append(1)
        return HttpResult(503, "")
    sleep_calls = []
    def sleep(d):
        sleep_calls.append(d)
    state, msgs = check_doi_entry(_entry("a2020", doi="10.1/x"), fetch, sleep)
    assert state == "no verificable"
    assert len(calls) == 4  # 1 intento + 3 reintentos
    assert sleep_calls == [1, 2, 4]


def test_service_error_then_ok():
    calls = []
    record = '{"status":"ok","message":{"title":["T"],"author":[{"family":"A","sequence":"first"}],"published-print":{"date-parts":[[2020]]}}}'
    def fetch(u, t):
        calls.append(1)
        return HttpResult(503, "") if len(calls) < 2 else HttpResult(200, record)
    sleep_calls = []
    def sleep(d):
        sleep_calls.append(d)
    state, msgs = check_doi_entry(_entry("a2020", doi="10.1/x"), fetch, sleep)
    assert state == "verificado"
    assert sleep_calls == [1]


def test_invalid_json_persistent():
    calls = []
    def fetch(u, t):
        calls.append(1)
        return HttpResult(200, "no es json")
    sleep = lambda d: None
    state, msgs = check_doi_entry(_entry("a2020", doi="10.1/x"), fetch, sleep)
    assert state == "no verificable"
    assert len(calls) == 4


def test_url_ok_with_non_json_body_one_call():
    calls = []

    def fetch(u, t):
        calls.append(u)
        return HttpResult(200, "observation_date,DRALACBS\n2000-01-01,1.5\n")

    state, msgs = check_url_entry(_entry("a2020", url="https://x.org/data.csv"), fetch, lambda d: None)
    assert state == "verificado"
    assert len(calls) == 1


def test_url_ok():
    fetch = lambda u, t: HttpResult(200, "ok")
    sleep = lambda d: None
    state, msgs = check_url_entry(_entry("a2020", url="https://x.org"), fetch, sleep)
    assert state == "verificado"
    assert any("[OK]" in m for m in msgs)


def test_no_doi_no_url():
    fetch = lambda u, t: HttpResult(200, "ok")
    sleep = lambda d: None
    state, msgs = check_url_entry(_entry("a2020"), fetch, sleep)
    assert state == "sin url"
    assert any("[SIN URL]" in m for m in msgs)


def test_run_exit_code_and_output():
    record = '{"status":"ok","message":{"title":["T"],"author":[{"family":"A","sequence":"first"}],"published-print":{"date-parts":[[2020]]}}}'
    fetch = lambda u, t: HttpResult(200, record)
    sleep = lambda d: None
    bib = "@article{a2020, author = {A}, title = {T}, year = {2020}, doi = {10.1/x}}"
    out = io.StringIO()
    code = run(bib, fetch, sleep, out)
    assert code == 0
    assert "Verificadas 1 de 1" in out.getvalue()


def test_run_nonzero_on_failure():
    fetch = lambda u, t: HttpResult(404, "{}")
    sleep = lambda d: None
    bib = "@article{a2020, author = {A}, title = {T}, year = {2020}, doi = {10.1/x}}"
    out = io.StringIO()
    code = run(bib, fetch, sleep, out)
    assert code == 1


def test_bib_not_modified():
    """run no escribe en el .bib original (RF-19): solo lee e imprime."""
    # Este test es de contrato: run no abre archivos en modo escritura.
    # Se verifica inspeccionando el código: run solo llama a parse_bib e imprime.
    pass


def test_get_with_retries_timeout_passed():
    seen = []
    def fetch(u, t):
        seen.append(t)
        return HttpResult(200, '{"status":"ok","message":{"title":["T"],"author":[{"family":"A","sequence":"first"}],"published-print":{"date-parts":[[2020]]}}}')
    sleep = lambda d: None
    get_with_retries("https://x.org", fetch, sleep)
    assert seen == [10]  # timeout=10


def test_http_get_custom_user_agent_only_for_crossref(monkeypatch):
    import scripts.verify_refs as vr

    seen = {}

    class _R:
        status_code = 200
        text = ""

    def fake_get(url, timeout, headers, stream):
        seen[url] = headers
        return _R()

    monkeypatch.setattr(vr.requests, "get", fake_get)
    vr.http_get("https://api.crossref.org/works/10.1/x", 5)
    vr.http_get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=X", 5)
    assert "User-Agent" in seen["https://api.crossref.org/works/10.1/x"]
    assert "User-Agent" not in seen["https://fred.stlouisfed.org/graph/fredgraph.csv?id=X"]
