"""Starter del ejercicio 2.1 — paréntesis balanceados con stack (Primero-Sin-IA).

Implementa la función a mano, sin IA. NO cambies la firma: los tests de
`test_solucion.py` dependen de ella.

Antes de codear, traza `([)]` en papel: ¿por qué está mal aunque tenga el mismo
número de cada símbolo? Esa pregunta te dice por qué necesitas un stack.
"""


def parentesis_balanceados(s: str) -> bool:
    """Indica si los símbolos ()[]{} en `s` están balanceados y bien anidados.

    Contrato:
        entrada: un string cualquiera (puede estar vacío); los caracteres que no
                 sean ()[]{} se ignoran.
        salida:  True si cada apertura se cierra con su par y en el orden correcto
                 (anidamiento válido); False en caso contrario.
        ejemplos: "([])" -> True ; "([)]" -> False ; "" -> True ; "(" -> False.

    Debe ser O(n) en tiempo usando un stack (una list con append/pop).
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Predict-Run: ¿qué crees que imprime ANTES de correrlo?
    print(parentesis_balanceados("([)]"))
