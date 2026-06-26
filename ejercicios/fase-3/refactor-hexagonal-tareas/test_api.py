"""Test 3 — El endpoint, testeado SIN base de datos vía dependency_overrides.

Sobreescribe `obtener_repo` para que el `Depends` entregue un doble en memoria en
vez del adaptador SQLAlchemy real. Así se prueba que:
  - crear tareas devuelve 201,
  - la regla de negocio (máx. 5 pendientes) aflora como un 409 por HTTP,
sin levantar Postgres ni SQLite. Detalle clave: el override devuelve SIEMPRE la
MISMA instancia del doble, para que el estado persista entre requests.

Requiere `httpx` (lo usa TestClient):  uv add httpx  (o pip install httpx)
No abras este archivo para adivinar la solución: solo verifica la tuya.
"""

from fastapi.testclient import TestClient

from adaptador_memoria import RepositorioTareasMemoria
from api import app, obtener_repo
from dominio import MAX_PENDIENTES


def test_crear_tarea_devuelve_201():
    fake = RepositorioTareasMemoria()
    app.dependency_overrides[obtener_repo] = lambda: fake
    try:
        client = TestClient(app)
        r = client.post("/tareas", json={"titulo": "comprar pan"})
        assert r.status_code == 201, r.text
        cuerpo = r.json()
        assert cuerpo["titulo"] == "comprar pan"
        assert cuerpo["completada"] is False
        assert cuerpo["id"] is not None
    finally:
        app.dependency_overrides.clear()


def test_limite_pendientes_responde_409():
    fake = RepositorioTareasMemoria()           # UNA instancia compartida
    app.dependency_overrides[obtener_repo] = lambda: fake
    try:
        client = TestClient(app)
        for n in range(MAX_PENDIENTES):
            assert client.post("/tareas", json={"titulo": f"t{n}"}).status_code == 201
        # la (MAX+1)-ésima tarea pendiente viola la regla de negocio -> 409
        r = client.post("/tareas", json={"titulo": "una de más"})
        assert r.status_code == 409, (
            f"se esperaba 409 al superar {MAX_PENDIENTES} pendientes, llegó {r.status_code}: {r.text}"
        )
    finally:
        app.dependency_overrides.clear()
