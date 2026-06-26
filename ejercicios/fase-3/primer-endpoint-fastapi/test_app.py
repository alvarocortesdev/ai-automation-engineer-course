"""Test de aceptación de tu primera API FastAPI.

Usa el TestClient de FastAPI (no necesitas levantar el servidor). Verifica:
  - POST /tareas crea y responde 201 con el modelo público completo.
  - El modelo de entrada exige `titulo` (ausente o vacío -> 422).
  - GET /tareas/{id} devuelve la tarea o 404.
  - GET /tareas filtra por `completada` y valida `limite` en [1, 100].

Requiere fastapi, httpx y pytest:
    uv add fastapi httpx pytest      # o:  pip install fastapi httpx pytest

NO abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def _crear(titulo: str = "Comprar pan", descripcion=None):
    return client.post("/tareas", json={"titulo": titulo, "descripcion": descripcion})


def test_crear_devuelve_201_y_modelo_publico():
    r = _crear("Tarea A", "una descripción")
    assert r.status_code == 201, "crear un recurso debe devolver 201"
    body = r.json()
    assert set(body) == {"id", "titulo", "descripcion", "completada"}, (
        "la respuesta debe traer exactamente los campos de TareaPublica"
    )
    assert body["titulo"] == "Tarea A"
    assert body["descripcion"] == "una descripción"
    assert body["completada"] is False, "una tarea nueva nace sin completar"
    assert isinstance(body["id"], int)


def test_obtener_tarea_existente():
    tid = _crear("Tarea B").json()["id"]
    r = client.get(f"/tareas/{tid}")
    assert r.status_code == 200
    assert r.json()["id"] == tid


def test_obtener_tarea_inexistente_da_404():
    r = client.get("/tareas/999999")
    assert r.status_code == 404, "una tarea que no existe debe dar 404, no 200 ni 500"
    assert "detail" in r.json(), "HTTPException produce un cuerpo con `detail`"


def test_titulo_ausente_da_422():
    r = client.post("/tareas", json={"descripcion": "sin titulo"})
    assert r.status_code == 422, "titulo es obligatorio; pydantic debe rechazar con 422"


def test_titulo_vacio_da_422():
    r = client.post("/tareas", json={"titulo": ""})
    assert r.status_code == 422, "titulo no puede ser vacío (Field min_length=1)"


def test_listar_filtra_por_completada():
    tid = _crear("Pendiente X").json()["id"]
    ids_false = {t["id"] for t in client.get("/tareas?completada=false&limite=100").json()}
    ids_true = {t["id"] for t in client.get("/tareas?completada=true&limite=100").json()}
    assert tid in ids_false, "la tarea nueva (completada=False) debe aparecer en el filtro false"
    assert tid not in ids_true, "no debe aparecer en el filtro true: nadie la completó"


def test_limite_fuera_de_rango_da_422():
    assert client.get("/tareas?limite=0").status_code == 422
    assert client.get("/tareas?limite=101").status_code == 422
