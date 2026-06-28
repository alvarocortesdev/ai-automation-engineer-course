"""Tests del reductor CDC. Corre: `pytest -v`

Definen el comportamiento obligatorio (nivel "competente"): debounce, mapeo de op,
propagar deletes, nace-y-muere, no re-embeddear lo igual, determinismo e idempotencia.
NO cubren tombstones ni el resumen de observabilidad (profundización): agrega tus
propios tests para esos.
"""

from reductor import Evento, Tarea, reducir


# --- Caso base --------------------------------------------------------------
def test_create_nuevo_genera_upsert():
    tareas = reducir([Evento("c", "a", {"contenido": "Hola"})], indexado={})
    assert tareas == [Tarea("upsert", "a", "Hola")]


def test_snapshot_r_se_trata_como_create():
    tareas = reducir([Evento("r", "a", {"contenido": "snap"})], indexado={})
    assert tareas == [Tarea("upsert", "a", "snap")]


# --- Debounce ---------------------------------------------------------------
def test_colapsa_multiples_updates_a_la_ultima_intencion():
    eventos = [
        Evento("c", "a", {"contenido": "v1"}),
        Evento("u", "a", {"contenido": "v2"}),
        Evento("u", "a", {"contenido": "v3"}),
    ]
    tareas = reducir(eventos, indexado={})
    # UNA sola tarea, con el contenido final.
    assert tareas == [Tarea("upsert", "a", "v3")]


# --- Deletes ----------------------------------------------------------------
def test_delete_de_fila_indexada_propaga():
    tareas = reducir([Evento("d", "b", None)], indexado={"b": "Mundo"})
    assert tareas == [Tarea("delete", "b", None)]


def test_delete_de_fila_no_indexada_no_hace_nada():
    tareas = reducir([Evento("d", "z", None)], indexado={})
    assert tareas == []


def test_nace_y_muere_en_el_mismo_lote_no_genera_tarea():
    eventos = [
        Evento("c", "c", {"contenido": "Soy nuevo"}),
        Evento("d", "c", None),
    ]
    # No estaba indexado y termina borrada -> nada (ni upsert ni delete).
    assert reducir(eventos, indexado={}) == []


# --- Costo: no re-embeddear lo igual ----------------------------------------
def test_contenido_igual_al_indexado_no_genera_tarea():
    # Un UPDATE que deja el contenido idéntico al ya embeddeado: no pagues embedding.
    tareas = reducir([Evento("u", "a", {"contenido": "Hola"})], indexado={"a": "Hola"})
    assert tareas == []


def test_contenido_distinto_genera_upsert():
    tareas = reducir([Evento("u", "a", {"contenido": "Hola v2"})], indexado={"a": "Hola"})
    assert tareas == [Tarea("upsert", "a", "Hola v2")]


# --- Determinismo -----------------------------------------------------------
def test_salida_ordenada_por_key():
    eventos = [
        Evento("c", "z", {"contenido": "Z"}),
        Evento("c", "a", {"contenido": "A"}),
        Evento("c", "m", {"contenido": "M"}),
    ]
    tareas = reducir(eventos, indexado={})
    assert [t.key for t in tareas] == ["a", "m", "z"]


# --- Idempotencia (CDC es at-least-once) ------------------------------------
def test_misma_tanda_dos_veces_da_el_mismo_resultado():
    eventos = [
        Evento("u", "a", {"contenido": "nuevo"}),
        Evento("d", "b", None),
    ]
    indexado = {"a": "viejo", "b": "Mundo"}
    una_vez = reducir(eventos, indexado)
    dos_veces = reducir(eventos + eventos, indexado)
    assert una_vez == dos_veces


# --- Lote completo (el escenario de la sección 6.1 de la lección) -----------
def test_lote_completo_de_la_leccion():
    eventos = [
        Evento("u", "a", {"contenido": "Hola, qué tal"}),
        Evento("u", "a", {"contenido": "Hola de nuevo"}),
        Evento("d", "b", None),
        Evento("c", "c", {"contenido": "Soy nuevo"}),
        Evento("d", "c", None),
        Evento("u", "a", {"contenido": "Hola de nuevo"}),
    ]
    indexado = {"a": "Hola", "b": "Mundo"}
    tareas = reducir(eventos, indexado)
    # a -> upsert (cambió respecto del índice); b -> delete (estaba indexado);
    # c -> nada (nació y murió, no estaba indexado). Ordenado por key.
    assert tareas == [
        Tarea("upsert", "a", "Hola de nuevo"),
        Tarea("delete", "b", None),
    ]


# TODO (tuyo): agrega al menos un test de caso borde. Sugerencias:
#   - tanda vacía -> [],
#   - una key que solo cambia metadata (contenido igual) mezclada con otra que sí cambia,
#   - (profundización) un evento tombstone (op == "d", after == None) ya cubierto: añade
#     uno que verifique el resumen de observabilidad si lo implementaste.
