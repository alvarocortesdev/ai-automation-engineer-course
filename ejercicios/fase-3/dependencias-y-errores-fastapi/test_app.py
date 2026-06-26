"""Test de aceptación: dependencias, errores globales y background tasks.

Verifica:
  - auth por header `x-api-key`: 401 sin clave o con clave mala, 200 con la correcta.
  - exception handler global: GET de un id inexistente -> 404 con cuerpo JSON custom.
  - background task: tras POST, la lista de auditoría creció (la tarea corrió).
  - paginación validada: limite/saltar fuera de rango -> 422.

Requiere fastapi, httpx y pytest:
    uv add fastapi httpx pytest      # o:  pip install fastapi httpx pytest

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

from fastapi.testclient import TestClient

from app import API_KEY, _AUDITORIA, app

client = TestClient(app)
HEAD = {"x-api-key": API_KEY}


def _crear(titulo: str = "Mi nota", cuerpo: str = "contenido"):
    return client.post("/notas", json={"titulo": titulo, "cuerpo": cuerpo}, headers=HEAD)


def test_sin_api_key_da_401():
    assert client.get("/notas").status_code == 401


def test_api_key_incorrecta_da_401():
    assert client.get("/notas", headers={"x-api-key": "clave-mala"}).status_code == 401


def test_api_key_correcta_da_200():
    r = client.get("/notas", headers=HEAD)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_obtener_inexistente_usa_handler_custom():
    r = client.get("/notas/999999", headers=HEAD)
    assert r.status_code == 404, "debe traducir RecursoNoEncontrado a 404"
    assert r.json() == {"error": "no_encontrado", "recurso": "nota", "id": 999999}, (
        "el exception handler global debe producir esta forma JSON exacta"
    )


def test_crear_dispara_background_task():
    antes = len(_AUDITORIA)
    r = _crear("Nota con auditoría")
    assert r.status_code == 201
    assert len(_AUDITORIA) == antes + 1, (
        "la background task de auditoría debe haber corrido tras el POST"
    )


def test_paginacion_invalida_da_422():
    assert client.get("/notas?limite=0", headers=HEAD).status_code == 422
    assert client.get("/notas?limite=101", headers=HEAD).status_code == 422
    assert client.get("/notas?saltar=-1", headers=HEAD).status_code == 422
