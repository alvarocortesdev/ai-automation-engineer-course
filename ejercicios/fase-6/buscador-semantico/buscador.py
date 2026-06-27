"""Ejercicio 6.5 — Buscador semántico desde cero (Primero-Sin-IA).

Implementa el MOTOR de una búsqueda semántica: chunking, ranking por coseno y
deduplicación. Para que los tests sean deterministas y offline (sin API key ni
descargar modelos), recibes los vectores ya calculados. Tu trabajo es la lógica
de ingeniería alrededor del embedding, que es lo que un AI Engineer debe poder
escribir sin librería mágica.

NO cambies las firmas (nombre, parámetros, retorno): los tests de
`test_buscador.py` dependen de ellas. Python puro, sin numpy, sin IA hasta cerrar
tu intento.

Corre los tests desde esta carpeta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import math


def chunk_texto(texto, tam, solape):
    """Parte `texto` en chunks de `tam` palabras, con `solape` palabras de solape.

    - Cada chunk avanza `tam - solape` palabras respecto del anterior.
    - El último chunk puede quedar más corto; está bien.
    - Si el texto tiene `tam` palabras o menos, devuelve un solo chunk con todo.
    - Texto vacío -> lista vacía.

    Lanza ValueError si `solape >= tam` (el paso sería 0 o negativo: bucle infinito).

    Devuelve una lista de strings (cada chunk son palabras unidas por un espacio).
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa chunk_texto")


def similitud_coseno(a, b):
    """Similitud coseno entre dos vectores (listas de números): (a · b) / (|a| * |b|).

    El mismo coseno que implementaste en 6.0 — reúsalo aquí. Devuelve un float en
    [-1, 1]. Puedes asumir que ningún vector de los tests es el vector cero.
    """
    raise NotImplementedError("Implementa similitud_coseno")


def buscar(consulta_vec, corpus_vecs, k):
    """Búsqueda semántica: rankea `corpus_vecs` por parecido a `consulta_vec`.

    - consulta_vec: un vector (lista de números).
    - corpus_vecs: lista de vectores (un vector por documento/chunk).
    - k: cuántos resultados devolver (el top-k).

    Devuelve una lista de tuplas (indice_original, score_coseno) ordenada de MAYOR
    a menor score, recortada a los primeros `k`. Si `k` es mayor que el corpus,
    devuelve todos.
    """
    raise NotImplementedError("Implementa buscar")


def deduplicar(vecs, umbral):
    """Elimina casi-duplicados por similitud coseno (estrategia greedy).

    Recorre los vectores en orden: conserva el primero y, para cada siguiente,
    lo descarta si su coseno contra CUALQUIER vector ya conservado es >= `umbral`.

    Devuelve la lista de índices (0-based, en orden) que sobreviven.
    """
    raise NotImplementedError("Implementa deduplicar")


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que imprime ANTES de correrlo?
    consulta = [1, 0]
    corpus = [[1, 0], [0, 1], [1, 1], [-1, 0]]
    print(buscar(consulta, corpus, k=2))
