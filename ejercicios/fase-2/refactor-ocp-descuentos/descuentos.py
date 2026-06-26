"""Starter del ejercicio — Refactor a Open/Closed (Primero-Sin-IA).

Este módulo YA FUNCIONA: `calcular_descuento` pasa todos los tests de
`test_descuentos.py`. Tu trabajo NO es arreglar un bug —es REFACTORIZAR:
cambiar la FORMA del código (eliminar la cadena de if/elif que crece, smell
'switch statements') sin cambiar su COMPORTAMIENTO, para que cumpla el
principio Open/Closed (abierto a extensión, cerrado a modificación).

REGLAS:
  - NO cambies la firma pública `calcular_descuento(cliente_tipo, monto) -> int`:
    los tests dependen de ella. Por dentro, delega a tus clases.
  - NO modifiques los tests para que pasen. Si un test cambia, cambiaste el
    comportamiento: eso es un bug en tu refactor.

Descuentos por tipo de cliente (todo en pesos enteros):
    regular    →  0 %
    vip        → 10 %
    empleado   → 30 %
    estudiante → 15 %
    jubilado   → 20 %
    (un tipo desconocido cuenta como 0 % de descuento)
"""


def calcular_descuento(cliente_tipo: str, monto: int) -> int:
    """Devuelve el MONTO DEL DESCUENTO (no el precio final) para un cliente.

    Contrato:
        entrada: cliente_tipo (str) y monto (int, pesos enteros >= 0).
        salida:  el descuento en pesos enteros; un tipo desconocido → 0.

    Implementación actual (la que vas a refactorizar): una cadena de if/elif
    que hay que EDITAR cada vez que aparece un cliente nuevo. Ese es el smell.
    """
    if cliente_tipo == "regular":
        return 0
    elif cliente_tipo == "vip":
        return monto * 10 // 100
    elif cliente_tipo == "empleado":
        return monto * 30 // 100
    elif cliente_tipo == "estudiante":
        return monto * 15 // 100
    elif cliente_tipo == "jubilado":
        return monto * 20 // 100
    else:
        return 0


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    print(calcular_descuento("vip", 10_000))       # 1000
    print(calcular_descuento("desconocido", 9999)) # 0
