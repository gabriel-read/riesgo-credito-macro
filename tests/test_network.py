"""RNF-2: abrir un socket durante los tests lanza RuntimeError."""

import socket

import pytest


def test_network_blocked():
    with pytest.raises(RuntimeError, match="Red bloqueada en tests"):
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("127.0.0.1", 80))
    with pytest.raises(RuntimeError, match="Red bloqueada en tests"):
        socket.create_connection(("127.0.0.1", 80))
    with pytest.raises(RuntimeError, match="Red bloqueada en tests"):
        socket.getaddrinfo("localhost", 80)
