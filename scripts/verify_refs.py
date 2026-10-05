"""Verificación de referencias contra Crossref (spec 002). Solo E/S; lógica pura en src/references.py."""
import sys
import time
from dataclasses import dataclass
from typing import Callable

import requests

from src.references import BibEntry, Mismatch, crossref_url, normalize_doi, parse_bib, compare_record, parse_crossref


@dataclass(frozen=True)
class HttpResult:
    status: int | None
    text: str


def http_get(url: str, timeout: float) -> HttpResult:
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "riesgo-credito-macro/0.1 (scripts/verify_refs.py)"}, stream=True)
        return HttpResult(r.status_code, r.text)
    except requests.RequestException:
        return HttpResult(None, "")


def is_service_error(result: HttpResult) -> bool:
    return result.status is None or result.status == 429 or 500 <= result.status < 600


def get_with_retries(url: str, fetch: Callable, sleep: Callable, delays=(1, 2, 4), timeout=10) -> HttpResult | None:
    r = fetch(url, timeout)
    for d in delays:
        if not is_service_error(r) and (r.status != 200 or parse_crossref(r.text) is not None):
            return r
        sleep(d)
        r = fetch(url, timeout)
    return r if not is_service_error(r) else None


def check_doi_entry(entry: BibEntry, fetch: Callable, sleep: Callable) -> tuple[str, list[str]]:
    doi = normalize_doi(entry.fields["doi"])
    url = crossref_url(doi)
    r = get_with_retries(url, fetch, sleep)
    if r is None:
        return "no verificable", [f"[NO VERIFICABLE] {entry.key}: error de red persistente tras reintentos."]
    if r.status == 404:
        return "no existe", [f"[NO EXISTE] {entry.key}: el DOI {doi} no existe en Crossref."]
    if r.status != 200:
        return "no verificable", [f"[NO VERIFICABLE] {entry.key}: HTTP {r.status}."]
    record = parse_crossref(r.text)
    if record is None:
        return "no verificable", [f"[NO VERIFICABLE] {entry.key}: respuesta de Crossref sin registro único bien formado."]
    mismatches = compare_record(entry, record)
    if not mismatches:
        return "verificado", [f"[OK] {entry.key}"]
    msgs = [f"[NO COINCIDE] {entry.key}: {m.field} — .bib: «{m.bib_value}» · Crossref: «{m.crossref_value}»" for m in mismatches]
    return "no coincide", msgs


def check_url_entry(entry: BibEntry, fetch: Callable, sleep: Callable) -> tuple[str, list[str]]:
    url = entry.fields.get("url", "")
    if not url:
        return "sin url", [f"[SIN URL] {entry.key}: la entrada no tiene campo url."]
    r = get_with_retries(url, fetch, sleep)
    if r is None:
        return "no verificable", [f"[NO VERIFICABLE] {entry.key}: error de red persistente tras reintentos."]
    if 200 <= r.status < 300:
        return "verificado", [f"[OK] {entry.key}"]
    return "url no responde", [f"[URL NO RESPONDE] {entry.key}: HTTP {r.status}."]


def run(bib_text: str, fetch: Callable, sleep: Callable, out) -> int:
    entries = parse_bib(bib_text)
    total = len(entries)
    ok = 0
    for entry in entries:
        if entry.fields.get("doi"):
            state, msgs = check_doi_entry(entry, fetch, sleep)
        else:
            state, msgs = check_url_entry(entry, fetch, sleep)
        for m in msgs:
            print(m, file=out)
        if state == "verificado":
            ok += 1
    print(f"Verificadas {ok} de {total} entradas.", file=out)
    return 0 if ok == total else 1


def main(argv=None) -> int:
    import sys
    bib_path = "report/references.bib"
    with open(bib_path, encoding="utf-8") as f:
        text = f.read()
    return run(text, http_get, time.sleep, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
