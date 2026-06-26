"""Starter del ejercicio — Primero-Sin-IA.

Implementa la función a mano, sin IA. Reemplaza el cuerpo de `resolver` por tu
solución. NO cambies la firma (nombre, parámetros, tipo de retorno): los tests
de `test_solucion.py` dependen de ella.

Este ejemplo ilustrativo (pasar texto a mayúsculas) está aquí solo para que la
plantilla funcione de extremo a extremo. En un ejercicio real, esta docstring y
esta firma describen el contrato del problema que toca resolver.
"""


def resolver(texto: str) -> str:
    """Devuelve `texto` en mayúsculas.

    Contrato:
        entrada: un string cualquiera (puede estar vacío).
        salida:  el mismo string con todos sus caracteres en mayúsculas;
                 el string vacío devuelve string vacío.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    print(resolver("hola, mundo"))
