"""Tests del ejercicio 3.15 — Cache-aside con TTL e invalidacion.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Estos tests definen el contrato. Usan dobles de prueba (no un Redis real):
- SpyCache: un dict en memoria que ademas cuenta llamadas y guarda el TTL usado.
- SpyRepo: la "base de datos", que cuenta lecturas y escrituras.
Asi puedes verificar el COMPORTAMIENTO (¿toco la DB?, ¿con que TTL poble?) sin red.
"""

from __future__ import annotations

from typing import Any

import pytest

from cache_aside import TTL_SEGUNDOS, CatalogoService, clave_producto


class SpyCache:
    def __init__(self) -> None:
        self._data: dict[str, str] = {}
        self.ttls: dict[str, int] = {}
        self.gets = 0
        self.sets = 0
        self.deletes = 0

    def get(self, clave: str) -> str | None:
        self.gets += 1
        return self._data.get(clave)

    def set(self, clave: str, valor: str, ttl: int) -> None:
        self.sets += 1
        self._data[clave] = valor
        self.ttls[clave] = ttl

    def delete(self, clave: str) -> None:
        self.deletes += 1
        self._data.pop(clave, None)
        self.ttls.pop(clave, None)


class SpyRepo:
    def __init__(self, productos: dict[int, dict[str, Any]]) -> None:
        self._productos = productos
        self.lecturas = 0
        self.escrituras = 0

    def obtener_producto(self, producto_id: int) -> dict[str, Any]:
        self.lecturas += 1
        return dict(self._productos[producto_id])  # copia: la DB no entrega su interior

    def actualizar_producto(self, producto_id: int, datos: dict[str, Any]) -> None:
        self.escrituras += 1
        self._productos[producto_id].update(datos)


@pytest.fixture
def productos() -> dict[int, dict[str, Any]]:
    return {1: {"id": 1, "nombre": "Cafe", "precio": 3990}}


def test_miss_consulta_repo_y_puebla_cache_con_ttl(productos):
    cache, repo = SpyCache(), SpyRepo(productos)
    svc = CatalogoService(cache, repo)

    resultado = svc.obtener(1)

    assert resultado == {"id": 1, "nombre": "Cafe", "precio": 3990}
    assert repo.lecturas == 1                       # fue a la DB exactamente una vez
    assert cache.sets == 1                          # poblo la cache
    assert cache.ttls[clave_producto(1)] == TTL_SEGUNDOS  # con el TTL correcto


def test_hit_no_consulta_repo(productos):
    cache, repo = SpyCache(), SpyRepo(productos)
    svc = CatalogoService(cache, repo)

    svc.obtener(1)            # MISS: puebla
    repo.lecturas = 0        # reinicia el contador
    resultado = svc.obtener(1)  # HIT

    assert resultado == {"id": 1, "nombre": "Cafe", "precio": 3990}
    assert repo.lecturas == 0   # NO volvio a la DB


def test_actualizar_invalida_cache(productos):
    cache, repo = SpyCache(), SpyRepo(productos)
    svc = CatalogoService(cache, repo)

    svc.obtener(1)                       # cachea el precio viejo (3990)
    svc.actualizar(1, {"precio": 4490})  # cambia el precio

    assert repo.escrituras == 1
    assert cache.deletes >= 1            # invalido borrando
    resultado = svc.obtener(1)            # la lectura siguiente NO debe ser stale
    assert resultado["precio"] == 4490


def test_producto_con_campo_falsy_se_cachea_y_da_hit(productos):
    # Un producto cuyo campo es "falsy" (stock 0) debe cachearse y dar HIT igual
    # que cualquier otro. (En la leccion: el guard `is not None` -en vez de
    # `if cacheado:`- es lo que te protege si algun dia cacheas un escalar que
    # serializa a un string falsy; aqui el dict siempre serializa no-vacio.)
    productos[2] = {"id": 2, "nombre": "Agotado", "stock": 0}
    cache, repo = SpyCache(), SpyRepo(productos)
    svc = CatalogoService(cache, repo)

    svc.obtener(2)
    repo.lecturas = 0
    resultado = svc.obtener(2)

    assert resultado["stock"] == 0
    assert repo.lecturas == 0


# TODO(estudiante): añade un test donde el producto cambia DOS veces seguidas
# (actualizar -> obtener -> actualizar -> obtener) y verifica que nunca se sirve
# un valor intermedio rancio desde la cache.
# def test_dos_cambios_seguidos_sin_stale(productos):
#     ...
