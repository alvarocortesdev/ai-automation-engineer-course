"""Ejercicio 6.6 — Recall de un índice + filtrado por metadata (Primero-Sin-IA).

No vas a levantar una base de datos. Vas a implementar, en Python puro, las TRES
ideas que hacen funcionar (o fallar) a una vector DB:

  1. la búsqueda EXACTA por fuerza bruta (tu ground truth, como en 6.5),
  2. el RECALL@k (cuánto se acerca un índice aproximado a ese ground truth),
  3. el FILTRADO por metadata con sus dos modos: pre-filter y post-filter.

Para que los tests sean deterministas y offline (sin API key, sin servidor, sin
modelos descargados), recibes vectores pequeños ya calculados. Tu trabajo es la
lógica de ingeniería alrededor del embedding, que es lo que un AI Engineer debe
poder defender sin librería mágica.

NO cambies las firmas (nombre, parámetros, retorno): los tests dependen de ellas.
Python puro, sin numpy, sin IA hasta cerrar tu intento.

Corre los tests desde esta carpeta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import math


def similitud_coseno(a, b):
    """Similitud coseno entre dos vectores (listas de números): (a · b) / (|a| * |b|).

    El mismo coseno de 6.0 / 6.5 — reúsalo. Float en [-1, 1]. Asume que ningún
    vector de los tests es el vector cero.
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa similitud_coseno")


def buscar_exacto(consulta, corpus, k):
    """Búsqueda EXACTA por fuerza bruta: el ground truth.

    - consulta: un vector (lista de números).
    - corpus: lista de vectores (un vector por documento).
    - k: cuántos resultados devolver.

    Devuelve una lista de tuplas (indice_original, score_coseno) ordenada de MAYOR
    a menor score, recortada a `k`. Si `k` es mayor que el corpus, devuelve todos.
    Esta es la "verdad" contra la que se mide el recall de un índice aproximado.
    """
    raise NotImplementedError("Implementa buscar_exacto")


def recall_at_k(ids_aprox, ids_exactos):
    """Recall@k: fracción de los ids EXACTOS que el índice aproximado encontró.

    - ids_aprox: lista de ids que devolvió un índice aproximado (ANN).
    - ids_exactos: lista de ids del ground truth (los que daría la fuerza bruta).

    Devuelve |ids_exactos ∩ ids_aprox| / |ids_exactos| como float en [0, 1].

    Caso borde: si `ids_exactos` está vacío, NO dividas por cero -> devuelve 1.0
    (no había nada que encontrar, así que "encontró todo lo que había": nada).
    """
    raise NotImplementedError("Implementa recall_at_k")


def buscar_con_filtro(consulta, corpus, metadatas, where, k, modo):
    """Búsqueda top-k respetando un filtro de metadata, en dos modos.

    - metadatas: lista de dicts, uno por documento (misma longitud que corpus).
    - where: dict de condiciones, p. ej. {"categoria": "tech"}. Un documento
      "cumple" si TODAS las claves de `where` calzan exactamente con su metadata.
    - k: cuántos resultados devolver.
    - modo: "pre" o "post".
        * "pre"  -> filtra el corpus ANTES de rankear: rankea solo los documentos
                    que cumplen `where` y devuelve hasta `k`. (Siempre da los k
                    mejores que cumplen, si existen.)
        * "post" -> rankea TODO el corpus, toma el top-k global y RECIÉN ahí
                    descarta los que no cumplen `where`. (Puede devolver MENOS de k.)

    Devuelve una lista de tuplas (indice_original, score_coseno) de mayor a menor.
    OJO: el índice devuelto es la posición ORIGINAL del documento en `corpus`,
    no su posición dentro del subconjunto filtrado.
    """
    raise NotImplementedError("Implementa buscar_con_filtro")


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que devuelve cada modo ANTES de correrlo?
    consulta = [1, 0]
    corpus = [[1, 0], [0, 1], [1, 1], [-1, 0]]
    metadatas = [
        {"categoria": "tech"},
        {"categoria": "gatos"},
        {"categoria": "gatos"},
        {"categoria": "tech"},
    ]
    print("pre :", buscar_con_filtro(consulta, corpus, metadatas, {"categoria": "tech"}, k=2, modo="pre"))
    print("post:", buscar_con_filtro(consulta, corpus, metadatas, {"categoria": "tech"}, k=2, modo="post"))
