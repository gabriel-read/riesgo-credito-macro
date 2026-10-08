"""Configuración de tests.

RNF-2: mientras corren los tests, cualquier acceso a la red lanza
``RuntimeError("Red bloqueada en tests")``. Los tests de datos usan las
descargas crudas congeladas en ``data/raw/`` (skill datos-fred).
"""

import socket

import pytest


def _blocked_network_call(*args, **kwargs):
    raise RuntimeError("Red bloqueada en tests")


@pytest.fixture(autouse=True)
def block_network(monkeypatch):
    """Sustituye los puntos de entrada de red por una función que falla."""
    monkeypatch.setattr(socket.socket, "connect", _blocked_network_call)
    monkeypatch.setattr(socket, "create_connection", _blocked_network_call)
    monkeypatch.setattr(socket, "getaddrinfo", _blocked_network_call)


@pytest.fixture(scope="session")
def model1_result():
    """Modelo I estimado sobre datos sintéticos (una sola vez por sesión; nunca datos reales)."""
    from src.model1 import run_model1
    from tests.synthetic_model1 import END, make_full, make_stationarity

    return run_model1(make_full(), make_stationarity(), END)


@pytest.fixture(scope="session")
def model2_result(model1_result):
    """Modelo II estimado sobre datos sintéticos (una sola vez por sesión; nunca datos reales)."""
    from src.model2 import run_model2
    from tests.synthetic_model1 import make_stationarity
    from tests.synthetic_model2 import END, make_full2

    return run_model2(make_full2(), make_stationarity(), END, model1_result)


def _digest_of(path):
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _all_files_digest(base):
    return {str(p.relative_to(base)): _digest_of(p) for p in sorted(base.rglob("*"))
            if p.is_file() and "raw" not in p.relative_to(base).parts}


@pytest.fixture(scope="session")
def frozen_runs(tmp_path_factory):
    """Etapas `data` y `models` sobre `data/raw/` congelado, en dos raíces independientes (solo datos reales).

    Raíz A: copia de data/raw, etapa `data` y etapa `models`. Raíz B: copia de A antes de `models`; se
    corre `models` dos veces sobre la misma raíz (idempotencia) y se guarda el resumen de cada corrida.
    Sin red (la bloquea el fixture autouse).
    """
    import shutil
    from pathlib import Path

    from src.pipeline import main

    mp = pytest.MonkeyPatch()
    a = tmp_path_factory.mktemp("frozen_a")
    b = tmp_path_factory.mktemp("frozen_b") / "root"
    shutil.copytree(Path("data/raw"), a / "data" / "raw")
    raw_before = {p.name: _digest_of(p) for p in (a / "data" / "raw").iterdir()}
    mp.setenv("PIPELINE_ROOT", str(a))
    assert main(["data"]) == 0
    variables_before = (a / "report" / "_variables.yml").read_text(encoding="utf-8")
    shutil.copytree(a, b)
    assert main(["models"]) == 0
    mp.setenv("PIPELINE_ROOT", str(b))
    assert main(["models"]) == 0
    first_b = _all_files_digest(b)
    assert main(["models"]) == 0
    second_b = _all_files_digest(b)
    mp.undo()
    return {"a": a, "b": b, "variables_before": variables_before, "raw_before": raw_before,
            "b_first": first_b, "b_second": second_b}

