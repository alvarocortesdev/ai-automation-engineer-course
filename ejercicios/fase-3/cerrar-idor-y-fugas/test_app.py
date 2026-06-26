"""Test de aceptación: Broken Access Control (IDOR) + fuga de datos.

Verifica que tras tu arreglo:
  - el listado está acotado al usuario actual (no expone notas ajenas),
  - GET y DELETE de una nota ajena dan 404 (no 403, no 200),
  - el dueño sí puede leer y borrar la suya,
  - la respuesta NUNCA incluye el campo interno,
  - sin header de auth se responde 401.

Requiere fastapi, httpx y pytest:
    uv add fastapi httpx pytest      # o:  pip install fastapi httpx pytest

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

import pytest
from fastapi.testclient import TestClient

import app as app_module
from app import app

client = TestClient(app)

ANA = {"x-user-id": "1"}
BETO = {"x-user-id": "2"}


@pytest.fixture(autouse=True)
def _estado_limpio():
    """Resetea el estado en memoria antes de cada test (determinismo)."""
    app_module._NOTAS.clear()
    app_module._siguiente_id = 1
    yield


def _crear(headers, titulo="Mi nota", cuerpo="contenido"):
    return client.post("/notas", json={"titulo": titulo, "cuerpo": cuerpo}, headers=headers)


def test_sin_auth_da_401():
    assert client.get("/notas").status_code == 401


def test_respuesta_no_filtra_campo_interno():
    r = _crear(ANA)
    assert r.status_code == 201
    assert "nota_privada_interna" not in r.json(), (
        "el response_model debe filtrar el campo interno; no devuelvas el dict crudo"
    )
    assert "owner_id" not in r.json()


def test_idor_get_de_nota_ajena_da_404():
    creada = _crear(ANA).json()
    r = client.get(f"/notas/{creada['id']}", headers=BETO)
    assert r.status_code == 404, "beto no debe poder leer la nota de ana (IDOR)"


def test_idor_delete_de_nota_ajena_da_404_y_no_borra():
    creada = _crear(ANA).json()
    r = client.delete(f"/notas/{creada['id']}", headers=BETO)
    assert r.status_code == 404, "beto no debe poder borrar la nota de ana"
    # y la nota sigue existiendo para su dueña
    assert client.get(f"/notas/{creada['id']}", headers=ANA).status_code == 200


def test_dueno_lee_y_borra_lo_suyo():
    creada = _crear(ANA).json()
    assert client.get(f"/notas/{creada['id']}", headers=ANA).status_code == 200
    assert client.delete(f"/notas/{creada['id']}", headers=ANA).status_code == 204
    # ya no existe
    assert client.get(f"/notas/{creada['id']}", headers=ANA).status_code == 404


def test_listado_acotado_al_usuario_actual():
    _crear(ANA, titulo="ana-1")
    _crear(ANA, titulo="ana-2")
    _crear(BETO, titulo="beto-1")

    r = client.get("/notas", headers=ANA)
    assert r.status_code == 200
    titulos = {n["titulo"] for n in r.json()}
    assert titulos == {"ana-1", "ana-2"}, "ana solo debe ver SUS notas"
    assert all("nota_privada_interna" not in n for n in r.json())
