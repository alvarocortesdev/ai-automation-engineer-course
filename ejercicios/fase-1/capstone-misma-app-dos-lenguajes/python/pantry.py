"""Lógica de dominio de la despensa (sin HTTP).

Completa los TODO. NO cambies las firmas de los métodos públicos: los tests de
`test_pantry.py` dependen de ellas.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError  # noqa: F401  (lo usarás)


# TODO (1.4): define el modelo de un ítem NUEVO (sin id) con validación declarativa:
#   - name: texto NO vacío
#   - quantity: número > 0
#   - unit: texto NO vacío
# Pista: usa Field(min_length=1) para texto y Field(gt=0) para el número.
class NewItem(BaseModel):
    ...  # reemplaza esto por los campos validados


# TODO: un ítem ya guardado ES un NewItem + un id entero.
class Item(NewItem):
    ...  # reemplaza esto


class PantryStore:
    """Guarda ítems en un archivo JSON. Recibe el path por parámetro (seam de test)."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        # TODO (1.5): si el archivo no existe, créalo con una lista JSON vacía ("[]").
        raise NotImplementedError("implementa el constructor")

    def list_items(self) -> list[dict]:
        # TODO: lee el archivo JSON y devuelve la lista de ítems.
        raise NotImplementedError

    def add_item(self, data: dict) -> dict:
        # TODO:
        #   1) valida `data` con NewItem (deja que ValidationError suba si es inválido),
        #   2) calcula el próximo id = max(ids existentes, default 0) + 1,
        #   3) construye el Item, persístelo y devuélvelo como dict.
        raise NotImplementedError

    def get_item(self, item_id: int) -> dict | None:
        # TODO: devuelve el ítem con ese id, o None si no existe.
        raise NotImplementedError

    def remove_item(self, item_id: int) -> bool:
        # TODO: borra el ítem con ese id. Devuelve True si borró, False si no existía.
        raise NotImplementedError
