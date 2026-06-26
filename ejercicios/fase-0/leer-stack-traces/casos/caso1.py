"""Caso 1 — suma los precios de un carrito de compras."""


def precio_total(carrito):
    total = 0
    for item in carrito:
        total += item["precio"]
    return total


carro = [
    {"nombre": "café", "precio": 2990},
    {"nombre": "té", "valor": 1990},
]
print(precio_total(carro))
