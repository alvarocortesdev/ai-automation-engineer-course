"""Ejercicio 2.7 — Sumador de texto (kata de TDD desde cero).

NO escribas la solución completa de una. Hazla CRECER test a test:
1) escribe el test del siguiente comportamiento en test_solucion.py,
2) córrelo y confirma el ROJO,
3) escribe aquí el código MÍNIMO para el verde,
4) refactoriza en verde si hace falta.

Arranca en rojo: el `NotImplementedError` de abajo hace fallar el primer test
(el comportamiento 1 ya está escrito en test_solucion.py). Reemplázalo por tu
implementación mínima y sigue desde ahí.

Contrato final (al que llegarás, NO el punto de partida):
    entrada: una cadena con números separados por coma y/o salto de línea.
    salida:  la suma de esos números (int). La cadena vacía suma 0.
    error:   si hay algún número negativo, lanza ValueError con el negativo en el mensaje.
"""


def sumar(numeros: str) -> int:
    raise NotImplementedError("Implementa esta función a mano, test a test, sin IA.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    print(sumar("1,2,3"))
