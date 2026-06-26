"""Tests del ejercicio — definen el contrato de la migración.

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Usan `sqlite3` de la stdlib: no necesitas instalar nada salvo pytest.
"""

import sqlite3

import pytest

from migracion import downgrade, upgrade

# `ALTER TABLE ... DROP COLUMN` existe desde SQLite 3.35 (incluido en Python 3.12+).
# Si tu intérprete trae un SQLite más viejo, los tests de downgrade se saltan en vez
# de fallar por algo ajeno a tu solución.
_SQLITE_OK = sqlite3.sqlite_version_info >= (3, 35, 0)

SEED = [
    (1, "Ada Lovelace"),
    (2, "Grace Murray Hopper"),
    (3, "Cher"),
]

ESPERADO = {
    1: ("Ada", "Lovelace"),
    2: ("Grace", "Murray Hopper"),
    3: ("Cher", ""),
}


def _db_inicial() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE usuarios (id INTEGER PRIMARY KEY, nombre_completo TEXT NOT NULL)"
    )
    conn.executemany(
        "INSERT INTO usuarios (id, nombre_completo) VALUES (?, ?)", SEED
    )
    conn.commit()
    return conn


def _columnas(conn: sqlite3.Connection) -> set[str]:
    return {row[1] for row in conn.execute("PRAGMA table_info(usuarios)")}


# ───────────────────────── upgrade ─────────────────────────


def test_upgrade_agrega_columnas():
    conn = _db_inicial()
    upgrade(conn)
    cols = _columnas(conn)
    assert "nombre" in cols
    assert "apellido" in cols


def test_upgrade_no_borra_nombre_completo():
    conn = _db_inicial()
    upgrade(conn)
    assert "nombre_completo" in _columnas(conn)
    filas = dict(conn.execute("SELECT id, nombre_completo FROM usuarios"))
    assert filas == {id_: nombre for id_, nombre in SEED}


def test_upgrade_backfill_correcto():
    conn = _db_inicial()
    upgrade(conn)
    filas = {
        row[0]: (row[1], row[2])
        for row in conn.execute("SELECT id, nombre, apellido FROM usuarios")
    }
    assert filas == ESPERADO


def test_upgrade_apellido_vacio_no_es_null():
    # "Cher" no tiene apellido: debe ser "" (string vacío), no NULL.
    conn = _db_inicial()
    upgrade(conn)
    apellido = conn.execute(
        "SELECT apellido FROM usuarios WHERE id = 3"
    ).fetchone()[0]
    assert apellido == ""


# ───────────────────────── downgrade ─────────────────────────


@pytest.mark.skipif(not _SQLITE_OK, reason="DROP COLUMN requiere SQLite >= 3.35")
def test_downgrade_quita_columnas_nuevas():
    conn = _db_inicial()
    upgrade(conn)
    downgrade(conn)
    cols = _columnas(conn)
    assert cols == {"id", "nombre_completo"}


@pytest.mark.skipif(not _SQLITE_OK, reason="DROP COLUMN requiere SQLite >= 3.35")
def test_downgrade_preserva_datos_originales():
    conn = _db_inicial()
    upgrade(conn)
    downgrade(conn)
    filas = dict(conn.execute("SELECT id, nombre_completo FROM usuarios"))
    assert filas == {id_: nombre for id_, nombre in SEED}


# ───────────────────────── round-trip ─────────────────────────


@pytest.mark.skipif(not _SQLITE_OK, reason="DROP COLUMN requiere SQLite >= 3.35")
def test_round_trip_deja_tabla_identica():
    # upgrade -> downgrade debe dejar TODO como al inicio (esquema y datos).
    conn = _db_inicial()
    estado_inicial = (
        _columnas(conn),
        dict(conn.execute("SELECT id, nombre_completo FROM usuarios")),
    )
    upgrade(conn)
    downgrade(conn)
    estado_final = (
        _columnas(conn),
        dict(conn.execute("SELECT id, nombre_completo FROM usuarios")),
    )
    assert estado_final == estado_inicial


@pytest.mark.skipif(not _SQLITE_OK, reason="DROP COLUMN requiere SQLite >= 3.35")
def test_upgrade_es_repetible_tras_downgrade():
    # upgrade -> downgrade -> upgrade debe volver a rellenar igual.
    conn = _db_inicial()
    upgrade(conn)
    downgrade(conn)
    upgrade(conn)
    filas = {
        row[0]: (row[1], row[2])
        for row in conn.execute("SELECT id, nombre, apellido FROM usuarios")
    }
    assert filas == ESPERADO


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Ideas: nombre con espacios dobles, string de solo espacios, tres palabras.
# def test_mi_caso_borde():
#     ...
