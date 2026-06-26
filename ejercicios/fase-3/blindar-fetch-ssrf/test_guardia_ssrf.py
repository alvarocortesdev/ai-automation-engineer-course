"""Test de aceptación: guardia anti-SSRF.

Los casos con IP LITERAL usan el resolver real (no toca la red: getaddrinfo sobre
una IP numérica no hace DNS). Los casos con HOSTNAME usan un resolver simulado para
no depender de la red ni del DNS del runner, y para forzar el caso de DNS rebinding.

Requiere pytest:
    uv add pytest      # o:  pip install pytest

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

import socket

import pytest

from guardia_ssrf import DestinoBloqueado, validar_destino


def resolver_falso(*ips):
    """Devuelve un resolver que simula que el host resuelve a estas IPs."""

    def _r(host, port, *args, **kwargs):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port)) for ip in ips]

    return _r


# --- Esquemas no permitidos -------------------------------------------------
def test_file_scheme_bloqueado():
    with pytest.raises(DestinoBloqueado):
        validar_destino("file:///etc/passwd")


def test_ftp_scheme_bloqueado():
    with pytest.raises(DestinoBloqueado):
        validar_destino("ftp://archivos.interno/x")


def test_sin_host_bloqueado():
    with pytest.raises(DestinoBloqueado):
        validar_destino("http://")


# --- IPs peligrosas (literales: resolver real, offline) ---------------------
def test_loopback_literal_bloqueado():
    with pytest.raises(DestinoBloqueado):
        validar_destino("http://127.0.0.1/admin")


def test_metadatos_nube_bloqueado():
    # 169.254.169.254 = link-local = endpoint de metadatos en la nube
    with pytest.raises(DestinoBloqueado):
        validar_destino("http://169.254.169.254/latest/meta-data/")


def test_red_privada_literal_bloqueado():
    with pytest.raises(DestinoBloqueado):
        validar_destino("http://10.0.0.1:8500/v1/kv/")


def test_unspecified_bloqueado():
    with pytest.raises(DestinoBloqueado):
        validar_destino("http://0.0.0.0/")


# --- Hostnames (resolver simulado) ------------------------------------------
def test_host_publico_permitido():
    url = "https://example.com/data.json"
    assert validar_destino(url, resolver=resolver_falso("93.184.216.34")) == url


def test_host_que_resuelve_a_privada_bloqueado():
    # nombre inocente que resuelve a una IP interna
    with pytest.raises(DestinoBloqueado):
        validar_destino("https://interno.miempresa.cl", resolver=resolver_falso("10.0.0.5"))


def test_dns_rebinding_una_privada_basta_para_bloquear():
    # resuelve a una pública Y una privada: debe bloquear por la privada
    with pytest.raises(DestinoBloqueado):
        validar_destino(
            "https://rebind.malo.test",
            resolver=resolver_falso("93.184.216.34", "10.0.0.5"),
        )
