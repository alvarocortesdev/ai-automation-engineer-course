"""Test 1 — El dominio es PURO y su regla de negocio se prueba SIN base de datos.

Dos cosas:
  A) Escanea los imports de dominio.py: FALLA si importa fastapi o sqlalchemy.
     Este test ES la regla de la arquitectura hexagonal hecha código: las
     dependencias apuntan hacia el dominio, jamás hacia la infraestructura.
  B) Ejercita la regla de negocio (máx. 5 pendientes) usando un doble en memoria
     DEFINIDO AQUÍ, sin tocar ninguna DB. Demuestra que el caso de uso depende
     del PUERTO, no de un adaptador concreto.

No abras este archivo para "adivinar" la solución: solo verifica la tuya.
"""

from pathlib import Path

import pytest

from dominio import LimiteTareasPendientes, MAX_PENDIENTES, ServicioTareas, Tarea

INFRA_PROHIBIDA = ("fastapi", "sqlalchemy", "httpx", "requests", "psycopg")


def test_dominio_no_importa_infraestructura():
    fuente = Path(__file__).with_name("dominio.py").read_text(encoding="utf-8")
    lineas_import = [
        ln.strip()
        for ln in fuente.splitlines()
        if ln.strip().startswith(("import ", "from "))
    ]
    ofensas = [ln for ln in lineas_import if any(p in ln for p in INFRA_PROHIBIDA)]
    assert not ofensas, (
        "dominio.py debe ser PURO: no puede importar infraestructura "
        f"(fastapi/sqlalchemy/...). Imports prohibidos encontrados: {ofensas}. "
        "Mueve esos imports al adaptador correspondiente."
    )


class _RepoFake:
    """Doble de test que cumple el puerto RepositorioTareas, sin DB."""

    def __init__(self) -> None:
        self._items: list[Tarea] = []
        self._next_id = 1

    def agregar(self, tarea: Tarea) -> Tarea:
        tarea.id = self._next_id
        self._next_id += 1
        self._items.append(tarea)
        return tarea

    def obtener(self, id: int) -> Tarea | None:
        return next((t for t in self._items if t.id == id), None)

    def listar(self) -> list[Tarea]:
        return list(self._items)

    def contar_pendientes(self) -> int:
        return sum(1 for t in self._items if not t.completada)


def test_crear_tarea_funciona_sin_db():
    servicio = ServicioTareas(_RepoFake())
    tarea = servicio.crear_tarea("comprar pan")
    assert tarea.id is not None
    assert tarea.titulo == "comprar pan"
    assert tarea.completada is False


def test_regla_limite_pendientes_sin_db():
    servicio = ServicioTareas(_RepoFake())
    for n in range(MAX_PENDIENTES):
        servicio.crear_tarea(f"tarea {n}")
    with pytest.raises(LimiteTareasPendientes):
        servicio.crear_tarea("una de más")   # la (MAX+1)-ésima pendiente se rechaza
