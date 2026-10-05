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
