"""Ejercicio 2.7 — Dividir un gasto en partes justas (TDD de una regla real).

NO programes el reparto del resto de una. Hazlo CRECER test a test:
1) escribe el test del siguiente comportamiento en test_solucion.py,
2) córrelo y confirma el ROJO,
3) escribe aquí el código MÍNIMO para el verde,
4) refactoriza en verde si hace falta.

Arranca en rojo: el `NotImplementedError` hace fallar el primer test (comportamiento 1,
ya escrito en test_solucion.py). El comportamiento 2 te forzará a inventar el reparto
del resto: deja que el test rojo te lo pida.

Contrato final (al que llegarás):
    entrada: monto_clp (int, >= 0) y personas (int, > 0).
    salida:  lista de int que suma EXACTAMENTE monto_clp, con partes que difieren en
             a lo más 1 peso; las primeras personas asumen el resto.
    error:   personas <= 0  -> ValueError ; monto_clp < 0 -> ValueError.
"""


def dividir_gasto(monto_clp: int, personas: int) -> list[int]:
    raise NotImplementedError("Implementa esta función a mano, test a test, sin IA.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    print(dividir_gasto(100, 3))
