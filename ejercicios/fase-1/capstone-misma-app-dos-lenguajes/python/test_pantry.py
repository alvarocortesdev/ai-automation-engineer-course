"""Tests del dominio de la despensa (Python).

Estos tests vienen escritos y FALLAN (rojo) hasta que implementes `pantry.py`.
Ese es el ciclo red-green de la sub-unidad 1.6: ves el rojo, lo haces verde.

Corre:  uv run pytest   (o:  pytest)

Antes de dar el capstone por cerrado, AGREGA al menos un test tuyo (un caso borde
que se te ocurra: ¿unidades repetidas?, ¿quantity decimal?, ¿name con espacios?).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from pantry import PantryStore


@pytest.fixture
def store(tmp_path: Path) -> PantryStore:
    # tmp_path es un directorio temporal único por test (fixture de pytest).
    return PantryStore(tmp_path / "data.json")


def test_empieza_vacia(store: PantryStore) -> None:
    assert store.list_items() == []


def test_agrega_con_id_incremental(store: PantryStore) -> None:
    a = store.add_item({"name": "arroz", "quantity": 2, "unit": "kg"})
    b = store.add_item({"name": "leche", "quantity": 1, "unit": "L"})
    assert a["id"] == 1
    assert b["id"] == 2
    assert len(store.list_items()) == 2


def test_rechaza_cantidad_no_positiva(store: PantryStore) -> None:
    with pytest.raises(ValidationError):
        store.add_item({"name": "sal", "quantity": 0, "unit": "kg"})


def test_rechaza_nombre_vacio(store: PantryStore) -> None:
    with pytest.raises(ValidationError):
        store.add_item({"name": "", "quantity": 1, "unit": "kg"})


def test_dato_invalido_no_se_persiste(store: PantryStore) -> None:
    with pytest.raises(ValidationError):
        store.add_item({"name": "sal", "quantity": -1, "unit": "kg"})
    assert store.list_items() == []  # nada se guardó


def test_get_devuelve_none_si_no_existe(store: PantryStore) -> None:
    assert store.get_item(99) is None


def test_remove(store: PantryStore) -> None:
    store.add_item({"name": "pan", "quantity": 4, "unit": "u"})
    assert store.remove_item(99) is False  # no existe
    assert store.remove_item(1) is True    # sí existe
    assert store.list_items() == []


def test_persiste_entre_instancias(store: PantryStore, tmp_path: Path) -> None:
    # store usa tmp_path/"data.json"; reabrimos el MISMO archivo en otra instancia.
    store.add_item({"name": "café", "quantity": 1, "unit": "kg"})
    otra = PantryStore(tmp_path / "data.json")
    assert len(otra.list_items()) == 1


# TODO: agrega aquí al menos un test tuyo.
