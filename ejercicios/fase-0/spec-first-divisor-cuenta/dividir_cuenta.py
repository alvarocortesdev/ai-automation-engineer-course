"""Ejercicio 0.8 — Spec-first: divisor de cuenta (Primero-Sin-IA).

EL ORDEN IMPORTA. Antes de tocar este archivo:
  1. Escribe `spec.md` (lo creas tú) con la tabla entradas / salida / casos borde.
  2. SOLO ENTONCES implementa `dividir_cuenta` aquí abajo, para cumplir tu spec.

No cambies la firma de la función (nombre, parámetros): los tests de
`test_dividir_cuenta.py` dependen de ella.

Corre los tests con:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""


def dividir_cuenta(total, personas):
    """Reparte una cuenta en partes iguales y devuelve cuánto paga cada persona.

    Contrato (esto es lo que fijan los tests; tu `spec.md` lo razona en español):
        entradas:
            total:    int o float, monto total de la cuenta en pesos. Debe ser >= 0.
            personas: int, cuántas personas reparten la cuenta. Debe ser >= 1.
        salida:
            float: lo que paga cada persona = total / personas, SIN redondear.
            (Redondear a peso es responsabilidad de quien muestra el número, no de
             este cálculo. Esa es una decisión de diseño: anótala en tu spec.)
        casos borde:
            total == 0           -> 0.0   (cuenta gratis, válida)
            división no exacta    -> float completo, p. ej. 100 / 3 = 33.333...
            total < 0            -> ValueError (un total negativo no tiene sentido)
            personas <= 0        -> ValueError (no se reparte entre cero o menos)

    Pista de orden: VALIDA antes de dividir. Si divides primero, `personas == 0`
    revienta con ZeroDivisionError antes de que puedas lanzar tu ValueError claro.
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa dividir_cuenta a partir de tu spec.md")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    print(dividir_cuenta(100, 4))
