"""DOMINIO PURO — complétalo SIN importar fastapi ni sqlalchemy.

Aquí vive la lógica de negocio: la entidad `Tarea`, el puerto `RepositorioTareas`
(una interface con `typing.Protocol`), el caso de uso `ServicioTareas` y la
excepción de dominio. Nada de HTTP, nada de SQL: este módulo debe poder
importarse y testearse sin levantar ninguna infraestructura.

`test_dominio_sin_infra.py` escanea los imports de este archivo y FALLA si
encuentra `fastapi` o `sqlalchemy`. Esa prueba ES la regla de la arquitectura
hecha test: las dependencias apuntan hacia el dominio, nunca al revés.
"""

from dataclasses import dataclass
from typing import Protocol

MAX_PENDIENTES = 5


@dataclass
class Tarea:
    """Entidad de dominio. NO es el modelo de SQLAlchemy (TareaORM)."""

    titulo: str
    completada: bool = False
    id: int | None = None


class LimiteTareasPendientes(Exception):
    """Error de dominio: se intentó crear una tarea con el cupo de pendientes lleno."""


class RepositorioTareas(Protocol):
    """Puerto de salida. El dominio habla con la persistencia SOLO a través de
    esta interface. Cualquier clase con estos cuatro métodos ES un
    RepositorioTareas (structural typing): no hace falta heredar de nada."""

    def agregar(self, tarea: Tarea) -> Tarea:
        """Persiste la tarea y devuelve la MISMA tarea con su `id` asignado."""
        ...

    def obtener(self, id: int) -> Tarea | None:
        ...

    def listar(self) -> list[Tarea]:
        ...

    def contar_pendientes(self) -> int:
        ...


class ServicioTareas:
    """Caso de uso. Recibe el puerto por el constructor (inyección de dependencia
    'a mano'): depende de la INTERFACE, no de un adaptador concreto."""

    def __init__(self, repo: RepositorioTareas) -> None:
        self._repo = repo

    def crear_tarea(self, titulo: str) -> Tarea:
        # TODO: aplica la regla de negocio (si hay MAX_PENDIENTES pendientes,
        #       lanza LimiteTareasPendientes) y luego persiste vía el puerto.
        raise NotImplementedError("implementa crear_tarea respetando la regla de negocio")

    def listar_tareas(self) -> list[Tarea]:
        # TODO: delega en el puerto.
        raise NotImplementedError("implementa listar_tareas")
