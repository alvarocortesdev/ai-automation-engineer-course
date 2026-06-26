"""Tests del ejercicio — definen el contrato.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

NINGÚN test toca la red. Toda la "respuesta HTTP" la fabrica un fetch falso. Ese
es justo el punto del ejercicio: testear lógica de API sin depender de internet.
"""

import pytest

from solucion import (
    RespuestaInesperada,
    ServicioCaido,
    ServicioInalcanzable,
    UsuarioNoEncontrado,
    nombre_de_usuario,
)


class RespFalsa:
    """Imita lo mínimo de una respuesta HTTP: status_code + .json()."""

    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


def fetch_que_devuelve(resp):
    """Crea un fetch falso que siempre devuelve la respuesta dada."""
    return lambda user_id: resp


def fetch_que_lanza(exc):
    """Crea un fetch falso que siempre lanza la excepción dada (simula error de red)."""

    def _fetch(user_id):
        raise exc

    return _fetch


def test_status_200_devuelve_el_nombre():
    fetch = fetch_que_devuelve(RespFalsa(200, {"name": "Ada Lovelace"}))
    assert nombre_de_usuario(1, fetch) == "Ada Lovelace"


def test_status_404_lanza_usuario_no_encontrado():
    fetch = fetch_que_devuelve(RespFalsa(404, {"message": "Not Found"}))
    with pytest.raises(UsuarioNoEncontrado):
        nombre_de_usuario(999, fetch)


def test_status_500_lanza_servicio_caido():
    fetch = fetch_que_devuelve(RespFalsa(500))
    with pytest.raises(ServicioCaido):
        nombre_de_usuario(1, fetch)


def test_status_503_tambien_es_servicio_caido():
    fetch = fetch_que_devuelve(RespFalsa(503))
    with pytest.raises(ServicioCaido):
        nombre_de_usuario(1, fetch)


def test_status_raro_lanza_respuesta_inesperada():
    fetch = fetch_que_devuelve(RespFalsa(302))
    with pytest.raises(RespuestaInesperada):
        nombre_de_usuario(1, fetch)


def test_timeout_se_convierte_en_servicio_inalcanzable():
    fetch = fetch_que_lanza(TimeoutError("simulado"))
    with pytest.raises(ServicioInalcanzable):
        nombre_de_usuario(1, fetch)


def test_connection_error_se_convierte_en_servicio_inalcanzable():
    fetch = fetch_que_lanza(ConnectionError("simulado"))
    with pytest.raises(ServicioInalcanzable):
        nombre_de_usuario(1, fetch)


@pytest.mark.parametrize("invalido", [0, -3])
def test_user_id_invalido_lanza_value_error_sin_llamar_fetch(invalido):
    # Si el id es inválido, ni siquiera debemos llamar fetch.
    def fetch_que_no_debe_correr(user_id):
        raise AssertionError("fetch NO debió ser llamado con un user_id inválido")

    with pytest.raises(ValueError):
        nombre_de_usuario(invalido, fetch_que_no_debe_correr)


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Idea: ¿qué pasa con un status 429 (rate limit)? ¿Y con un user_id que no sea int?
# def test_mi_caso_borde():
#     ...
