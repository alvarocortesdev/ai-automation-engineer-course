"""Modelos SQLAlchemy 2.0 (estilo declarativo moderno) para el ejercicio.

NO necesitas modificar este archivo. Define una relación uno-a-muchos:
un Autor tiene muchos Libro. El `relationship` es LAZY por defecto, que es
justo lo que dispara el N+1 si no usas eager loading en tu consulta.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Autor(Base):
    __tablename__ = "autores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

    # LAZY por defecto: acceder a `autor.libros` dispara una query nueva.
    libros: Mapped[list["Libro"]] = relationship(back_populates="autor")


class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"))

    autor: Mapped["Autor"] = relationship(back_populates="libros")
