"""Ejercicio 6.0 — Similitud coseno desde cero (Primero-Sin-IA).

Implementa las funciones a mano, en Python puro (sin numpy, sin IA).
NO cambies las firmas (nombre, parámetros, retorno): los tests de
`test_similitud.py` dependen de ellas.

Corre los tests desde esta carpeta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import math


def producto_punto(a, b):
    """Producto punto de dos vectores (listas de números) del mismo largo.

        a · b = a[0]*b[0] + a[1]*b[1] + ... + a[n-1]*b[n-1]

    Lanza ValueError si los vectores tienen distinto largo.
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa producto_punto")


def magnitud(a):
    """Longitud (norma) de un vector: raíz de la suma de sus cuadrados.

        |a| = sqrt(a[0]^2 + a[1]^2 + ...)
    """
    raise NotImplementedError("Implementa magnitud")


def similitud_coseno(a, b):
    """Similitud coseno entre a y b: (a · b) / (|a| * |b|).

    Devuelve un float en el rango [-1, 1].
    Lanza ValueError si algún vector es el vector cero (magnitud 0): dividir
    por cero no está definido, y un vector cero no tiene "dirección".
    """
    raise NotImplementedError("Implementa similitud_coseno")


def rankear(consulta, documentos):
    """Ordena `documentos` de más a menos parecido a `consulta`.

    - consulta: un vector (lista de números).
    - documentos: lista de vectores.

    Devuelve una lista de tuplas (indice_original, similitud), ordenada de
    MAYOR a menor similitud. `indice_original` es la posición del documento en
    la lista `documentos` (0-based), para no perder de vista cuál era cuál.
    """
    raise NotImplementedError("Implementa rankear")


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que imprime ANTES de correrlo?
    q = [7, 1]
    docs = [[9, 1], [8, 0], [1, 9]]
    print(rankear(q, docs))
