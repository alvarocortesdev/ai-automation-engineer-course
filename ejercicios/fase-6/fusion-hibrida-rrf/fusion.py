"""Ejercicio 6.7 — Retrieval híbrido: RRF + metadata filtering (Primero-Sin-IA).

Implementa el NÚCLEO del retrieval híbrido de un RAG: fusionar rankings con
Reciprocal Rank Fusion, filtrar por metadata fail-closed, y componer ambos en un
top-k. Recibes los rankings ya calculados (listas de doc_id), así que los tests
corren offline, deterministas, sin API ni modelos. Tu trabajo es la lógica de
ingeniería alrededor del retrieval, que es lo que un AI Engineer debe poder escribir
sin librería mágica.

NO cambies las firmas (nombre, parámetros, retorno): los tests de `test_fusion.py`
dependen de ellas. Python puro, sin numpy, sin IA hasta cerrar tu intento.

Corre los tests desde esta carpeta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""


def rrf_fusion(listas_ranqueadas, k=60):
    """Fusiona varias listas de doc_ids con Reciprocal Rank Fusion (RRF).

    - listas_ranqueadas: lista de listas de doc_ids, cada una ORDENADA (mejor
      primero). Ej.: [["a", "b", "c"], ["b", "c", "a"]].
    - k: constante de RRF (60 por convención).

    Para cada doc_id, su score es la suma sobre todas las listas de 1 / (k + rank),
    con `rank` empezando en 1 (el primer puesto es rank 1, no 0). Un doc que aparece
    en varias listas acumula. Un doc que no aparece en una lista no suma nada por esa
    lista.

    Devuelve una lista de tuplas (doc_id, score) ordenada de MAYOR a menor score.
    En empate de score, ordena por doc_id ASCENDENTE (resultado determinista).
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa rrf_fusion")


def filtrar_por_metadata(doc_ids, metadata, filtro):
    """Filtra doc_ids por metadata con cierre seguro (fail-closed).

    - doc_ids: lista de doc_ids candidatos (en algún orden a preservar).
    - metadata: dict {doc_id: {clave: valor}}.
    - filtro: dict {clave: valor} que el doc DEBE cumplir (TODAS las claves).

    Conserva, EN ORDEN, los doc_ids cuya metadata cumple todas las claves del filtro.
    Fail-closed: si a un doc le falta una clave del filtro (o no está en `metadata`),
    NO pasa. Un filtro vacío deja pasar todo.

    Devuelve la lista filtrada de doc_ids.
    """
    raise NotImplementedError("Implementa filtrar_por_metadata")


def recuperar_hibrido(ranking_vectorial, ranking_bm25, metadata, filtro, k_final):
    """Retrieval híbrido completo: fusiona, filtra y recorta.

    1. Fusiona `ranking_vectorial` y `ranking_bm25` con `rrf_fusion`.
    2. Aplica `filtrar_por_metadata` sobre el orden fusionado (descarta lo que no
       cumple el filtro de seguridad/relevancia).
    3. Devuelve los `k_final` mejores como lista de tuplas (doc_id, score),
       conservando el score RRF de la fusión. Si quedan menos que `k_final`,
       devuelve todos.
    """
    raise NotImplementedError("Implementa recuperar_hibrido")


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que imprime ANTES de correrlo?
    vect = ["d1", "d2", "d3"]
    bm25 = ["d2", "d4", "d1"]
    meta = {
        "d1": {"tenant": "A"},
        "d2": {"tenant": "A"},
        "d3": {"tenant": "B"},
        "d4": {"tenant": "A"},
    }
    print(recuperar_hibrido(vect, bm25, meta, {"tenant": "A"}, k_final=2))
