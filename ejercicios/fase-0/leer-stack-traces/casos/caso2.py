"""Caso 2 — suma una lista de montos."""


def suma_montos(montos):
    total = 0
    for m in montos:
        total += m
    return total


datos = [1000, 2500, "3000"]
print(suma_montos(datos))
