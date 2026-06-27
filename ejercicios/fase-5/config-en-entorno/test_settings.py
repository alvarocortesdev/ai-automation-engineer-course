"""Tests de aceptación — Factor III (config en el entorno).

Deterministas: cada test parte de un entorno LIMPIO (sin variables APP_*) y
define solo lo que necesita con `monkeypatch`. Así afirmamos el comportamiento
exacto sin depender de tu shell.

Ejecuta:
    uv run pytest        # o:  pytest

Nota: si tienes un archivo `.env` en esta carpeta, bórralo antes de correr los
tests (el .env es para uso manual de dev; aquí las variables las controla el
test). NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

import os

import pytest
from pydantic import ValidationError

from settings import get_settings


@pytest.fixture(autouse=True)
def entorno_limpio(monkeypatch):
    """Borra cualquier variable APP_* del entorno antes de cada test."""
    for clave in list(os.environ):
        if clave.startswith("APP_"):
            monkeypatch.delenv(clave, raising=False)
    yield


def _poner_requeridos(monkeypatch):
    monkeypatch.setenv("APP_DATABASE_URL", "postgresql://localhost:5432/test")
    monkeypatch.setenv("APP_API_KEY", "k-test-123")


def test_lee_los_requeridos_del_entorno(monkeypatch):
    _poner_requeridos(monkeypatch)
    s = get_settings()
    assert s.database_url == "postgresql://localhost:5432/test"
    assert s.api_key == "k-test-123"


def test_port_usa_el_default_cuando_no_esta(monkeypatch):
    _poner_requeridos(monkeypatch)
    assert get_settings().port == 8000          # default
    assert get_settings().debug is False        # default


def test_port_se_lee_del_entorno_como_int(monkeypatch):
    _poner_requeridos(monkeypatch)
    monkeypatch.setenv("APP_PORT", "9000")
    s = get_settings()
    assert s.port == 9000
    assert isinstance(s.port, int)              # parseado a int, no "9000" string


@pytest.mark.parametrize("valor,esperado", [("true", True), ("1", True), ("false", False), ("0", False)])
def test_debug_parsea_booleano(monkeypatch, valor, esperado):
    _poner_requeridos(monkeypatch)
    monkeypatch.setenv("APP_DEBUG", valor)
    assert get_settings().debug is esperado


def test_falta_un_requerido_falla_al_arrancar(monkeypatch):
    # Solo definimos database_url; falta api_key (requerido) -> debe explotar.
    monkeypatch.setenv("APP_DATABASE_URL", "postgresql://localhost:5432/test")
    with pytest.raises(ValidationError):
        get_settings()


def test_sin_ningun_requerido_no_hay_default_inseguro(monkeypatch):
    # Entorno vacío: si database_url/api_key tuvieran un default (vacío o no),
    # esto NO lanzaría. Que lance prueba que son requeridos de verdad (fail-fast).
    with pytest.raises(ValidationError):
        get_settings()


# TODO(estudiante): añade un caso borde tuyo. Por ejemplo, que un APP_PORT no
# numérico ("abc") lance ValidationError, o que una variable APP_* extra no
# declarada sea ignorada.
