"""Ejercicio 3.15 — Cache-aside con TTL e invalidación.

Implementa CatalogoService: lee productos con el patrón cache-aside
(cache -> MISS -> repositorio -> poblar cache con TTL) e invalida la cache al
actualizar. NO necesitas un Redis real: el servicio recibe un `cache` y un
`repo` por inyeccion (ports & adapters de 3.9). Los tests te pasan dobles de
prueba que cuentan llamadas.

Reglas del contrato (NO las cambies):
- obtener(producto_id) -> dict
- actualizar(producto_id, datos) -> None
- El TTL en segundos es TTL_SEGUNDOS.
- La clave de cache la da clave_producto(producto_id).
"""

from __future__ import annotations

import json
from typing import Any, Protocol

TTL_SEGUNDOS = 300  # 5 minutos


class Cache(Protocol):
    """Puerto de cache. En produccion, un adaptador sobre redis-py lo implementa."""

    def get(self, clave: str) -> str | None: ...
    def set(self, clave: str, valor: str, ttl: int) -> None: ...
    def delete(self, clave: str) -> None: ...


class Repositorio(Protocol):
    """Puerto de la fuente de verdad (la base de datos)."""

    def obtener_producto(self, producto_id: int) -> dict[str, Any]: ...
    def actualizar_producto(self, producto_id: int, datos: dict[str, Any]) -> None: ...


def clave_producto(producto_id: int) -> str:
    return f"producto:{producto_id}"


class CatalogoService:
    def __init__(self, cache: Cache, repo: Repositorio) -> None:
        self.cache = cache
        self.repo = repo

    def obtener(self, producto_id: int) -> dict[str, Any]:
        # TODO: implementa cache-aside.
        # 1) intenta leer de la cache (clave_producto). Si HAY valor (HIT),
        #    deserializa con json.loads y devuelvelo de inmediato (no toques el repo).
        # 2) si NO hay (MISS), consulta self.repo.obtener_producto(...).
        # 3) guarda el resultado en la cache serializado con json.dumps y TTL_SEGUNDOS.
        # 4) devuelve el resultado.
        raise NotImplementedError("Implementa obtener() con el patron cache-aside")

    def actualizar(self, producto_id: int, datos: dict[str, Any]) -> None:
        # TODO: implementa la escritura con invalidacion.
        # 1) escribe en self.repo (la FUENTE DE VERDAD) PRIMERO.
        # 2) invalida (borra) la entrada de cache de ese producto.
        raise NotImplementedError("Implementa actualizar() escribiendo el repo y luego invalidando")
