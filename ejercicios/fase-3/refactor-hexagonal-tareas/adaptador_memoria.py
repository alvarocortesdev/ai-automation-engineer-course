"""ADAPTADOR DE SALIDA en memoria — complétalo.

Implementa el puerto `RepositorioTareas` (de dominio.py) guardando las tareas en
una lista de Python, sin base de datos. Es el adaptador que usarás en los tests:
rápido, determinista, sin estado externo. No hereda de nada (basta con tener los
métodos correctos del puerto).
"""

from dominio import Tarea


class RepositorioTareasMemoria:
    def __init__(self) -> None:
        # TODO: una lista de Tarea y un contador para asignar ids.
        raise NotImplementedError("implementa el constructor")

    def agregar(self, tarea: Tarea) -> Tarea:
        # TODO: asigna un id, guarda la tarea y devuélvela.
        raise NotImplementedError("implementa agregar")

    def obtener(self, id: int) -> Tarea | None:
        raise NotImplementedError("implementa obtener")

    def listar(self) -> list[Tarea]:
        raise NotImplementedError("implementa listar")

    def contar_pendientes(self) -> int:
        raise NotImplementedError("implementa contar_pendientes")
