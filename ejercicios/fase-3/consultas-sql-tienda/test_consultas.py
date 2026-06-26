"""Tests del ejercicio 3.1 — consultas SQL contra una base sembrada.

Ejecuta DENTRO de esta carpeta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Usa SQLite, incluido en la librería estándar de Python: no instalas nada.
Cada test arma una base nueva en memoria a partir de `seed.sql`, ejecuta tu
consulta `consultas/qN.sql` y compara el resultado. Predice el resultado ANTES
de correr el test (Primero-Sin-IA): si aciertas a mano, ya entendiste.
"""

import sqlite3
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
SEED = (AQUI / "seed.sql").read_text(encoding="utf-8")


def nueva_db() -> sqlite3.Connection:
    """Base SQLite en memoria, recién sembrada (una por test, sin interferencias)."""
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys = ON;")
    con.executescript(SEED)
    return con


def leer_consulta(nombre: str) -> str:
    """Lee consultas/<nombre>; falla con mensaje claro si sigue sin escribir."""
    texto = (AQUI / "consultas" / nombre).read_text(encoding="utf-8")
    cuerpo = "\n".join(
        linea
        for linea in texto.splitlines()
        if linea.strip() and not linea.strip().startswith("--")
    ).strip()
    if not cuerpo:
        pytest.fail(f"{nombre} sigue vacío: escribe tu consulta (Primero-Sin-IA).")
    return texto


def filas_select(nombre: str) -> list[tuple]:
    con = nueva_db()
    try:
        return [tuple(f) for f in con.execute(leer_consulta(nombre)).fetchall()]
    finally:
        con.close()


# ---- q1: SELECT + WHERE ----------------------------------------------------
def test_q1_where_perifericos_con_stock():
    esperado = {
        ("Teclado mecánico", 12),
        ("Mouse inalámbrico", 30),
        ("Audífonos", 7),
    }
    assert set(filas_select("q1.sql")) == esperado


# ---- q2: ORDER BY + LIMIT (el orden de las filas SÍ se evalúa) --------------
def test_q2_order_by_top_3_caros():
    esperado = [
        ('Monitor 27"', 189990),
        ('Monitor 24"', 129990),
        ("Audífonos", 49990),
    ]
    assert filas_select("q2.sql") == esperado


# ---- q3: GROUP BY + COUNT --------------------------------------------------
def test_q3_group_by_count_por_categoria():
    esperado = {
        ("periféricos", 4),
        ("pantallas", 2),
        ("cables", 2),
        ("accesorios", 2),
    }
    assert set(filas_select("q3.sql")) == esperado


# ---- q4: GROUP BY + SUM ----------------------------------------------------
def test_q4_group_by_sum_stock():
    esperado = {
        ("periféricos", 49),
        ("pantallas", 13),
        ("cables", 100),
        ("accesorios", 35),
    }
    assert set(filas_select("q4.sql")) == esperado


# ---- q5: INSERT ------------------------------------------------------------
def test_q5_insert_alfombrilla():
    con = nueva_db()
    try:
        con.executescript(leer_consulta("q5.sql"))
        fila = con.execute(
            "SELECT nombre, categoria, precio, stock "
            "FROM productos WHERE nombre = 'Alfombrilla'"
        ).fetchone()
        assert fila == ("Alfombrilla", "accesorios", 9990, 50)
        total = con.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
        assert total == 11  # 10 sembrados + 1 nuevo
    finally:
        con.close()


# ---- q6: UPDATE ------------------------------------------------------------
def test_q6_update_precio_cables():
    con = nueva_db()
    try:
        con.executescript(leer_consulta("q6.sql"))
        filas = con.execute(
            "SELECT nombre, precio FROM productos WHERE categoria = 'cables'"
        ).fetchall()
        assert {tuple(f) for f in filas} == {
            ("Cable HDMI", 6990),
            ("Cable USB-C", 8990),
        }
    finally:
        con.close()


# ---- q7: DELETE ------------------------------------------------------------
def test_q7_delete_sin_stock():
    con = nueva_db()
    try:
        con.executescript(leer_consulta("q7.sql"))
        sin_stock = con.execute(
            "SELECT COUNT(*) FROM productos WHERE stock = 0"
        ).fetchone()[0]
        assert sin_stock == 0
        total = con.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
        assert total == 8  # se eliminan 2: Cable USB-C y Webcam HD
    finally:
        con.close()
