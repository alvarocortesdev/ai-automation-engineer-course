"""Caso 3 — calcula e imprime el promedio de una lista de notas."""


def promedio(numeros):
    return sum(numeros) / len(numeros)


def reporte(notas):
    print("Promedio:", promedio(notas))


reporte([])
