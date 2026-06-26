"""Starter del ejercicio 2.1 — two-sum con hashmap (Primero-Sin-IA).

Implementa la función a mano, sin IA. NO cambies la firma (nombre, parámetros,
tipo de retorno): los tests de `test_solucion.py` dependen de ella.

Recuerda la disciplina:
  1. Escribe primero la versión obvia con bucle anidado (O(n²)) en papel.
  2. Luego baja a O(n) con un `set` que recuerde lo ya visto.
  3. Entrega aquí solo la versión O(n).
"""


def tiene_dos_que_suman(nums: list[int], objetivo: int) -> bool:
    """Indica si dos elementos en POSICIONES DISTINTAS suman `objetivo`.

    Contrato:
        entrada: una lista de enteros (puede estar vacía) y un entero objetivo.
        salida:  True si existen i != j con nums[i] + nums[j] == objetivo;
                 False en caso contrario.
        nota:    se exigen DOS posiciones distintas; un solo elemento que sea
                 la mitad del objetivo no basta (p. ej. [1] con objetivo 2 -> False),
                 pero un valor repetido en dos posiciones sí (p. ej. [3, 3] -> True).

    Debe ser O(n) en tiempo: un solo recorrido, usando un `set` para los lookups.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Predict-Run: ¿qué crees que imprime ANTES de correrlo?
    print(tiene_dos_que_suman([2, 7, 11, 15], 9))
