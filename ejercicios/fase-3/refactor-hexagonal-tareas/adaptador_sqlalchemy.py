"""ADAPTADOR DE SALIDA con SQLAlchemy — complétalo.

Implementa el MISMO puerto `RepositorioTareas`, pero contra una base de datos
real vía SQLAlchemy 2.0. Recibe una `Session` por el constructor. Tu trabajo
extra aquí es TRADUCIR entre la fila ORM (`TareaORM`, de modelos.py) y la
entidad de dominio (`Tarea`, de dominio.py): nunca devuelvas un TareaORM hacia
el dominio.

Pista de mapeo:
    Tarea(id=fila.id, titulo=fila.titulo, completada=fila.completada)
"""

from sqlalchemy.orm import Session

from dominio import Tarea
from modelos import TareaORM


class RepositorioTareasSQLAlchemy:
    def __init__(self, session: Session) -> None:
        self._session = session

    def agregar(self, tarea: Tarea) -> Tarea:
        # TODO: crea un TareaORM, add + flush (asigna el id), y devuelve una
        #       entidad Tarea con ese id.
        raise NotImplementedError("implementa agregar")

    def obtener(self, id: int) -> Tarea | None:
        raise NotImplementedError("implementa obtener")

    def listar(self) -> list[Tarea]:
        raise NotImplementedError("implementa listar")

    def contar_pendientes(self) -> int:
        raise NotImplementedError("implementa contar_pendientes")
