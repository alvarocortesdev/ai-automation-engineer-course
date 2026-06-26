"""Modelo SQLAlchemy 2.0 (PROVISTO — no lo edites).

Este es el modelo de PERSISTENCIA (la fila en la base de datos). OJO: NO es la
entidad de dominio. Tu `dominio.Tarea` es una dataclass plana, sin SQLAlchemy;
tu `adaptador_sqlalchemy` traduce entre esta `TareaORM` y aquella `Tarea`.
Mantener las dos separadas es lo que evita que SQLAlchemy se filtre al dominio.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TareaORM(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column()
    completada: Mapped[bool] = mapped_column(default=False)
