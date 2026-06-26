"""Starter del ejercicio 2.8 — repartir_monto (Primero-Sin-IA).

Implementa la función a mano, sin IA. NO cambies la firma (nombre, parametros,
tipo de retorno): los tests de `test_solucion.py` dependen de ella.

Recuerda la disciplina:
  1. Implementa primero la version correcta (pista: `divmod`).
  2. Luego, en test_solucion.py, escribe las PROPIEDADES con Hypothesis.
  3. Comprueba que una propiedad falla contra la version ingenua
     `[total // partes] * partes` y anotalo en propiedades.md.
"""


def repartir_monto(total: int, partes: int) -> list[int]:
    """Reparte `total` (entero >= 0) en `partes` partes lo mas parejo posible.

    Contrato:
        entrada: total >= 0 (entero) y partes >= 1 (entero).
        salida:  una lista de `partes` enteros no negativos tal que
                   - suman EXACTAMENTE `total`, y
                   - difieren entre si a lo mas en 1 (lo mas parejo posible).
        errores: si partes <= 0, lanza ValueError.

    Ejemplos:
        repartir_monto(100, 4) -> [25, 25, 25, 25]
        repartir_monto(101, 4) -> [26, 25, 25, 25]   # el resto va a las primeras
        repartir_monto(0, 3)   -> [0, 0, 0]
        repartir_monto(10, 1)  -> [10]
    """
    raise NotImplementedError("Implementa esta funcion a mano, sin IA.")


if __name__ == "__main__":
    # Predict-Run: que crees que imprime ANTES de correrlo?
    print(repartir_monto(101, 4))
