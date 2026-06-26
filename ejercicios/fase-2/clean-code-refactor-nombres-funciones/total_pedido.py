"""Ejercicio 2.2 — Refactor: nombres con intención + funciones pequeñas (Primero-Sin-IA).

Esta función YA FUNCIONA y los tests YA pasan en verde. Tu trabajo NO es hacerla
funcionar: es dejarla LIMPIA sin cambiar lo que hace.

Cada línea de un pedido es una tupla:
    (producto: str, precio: int, cantidad: int, activo: bool)

`total_pedido` suma el precio*cantidad de las líneas ACTIVAS y, si el subtotal
supera UMBRAL, aplica un descuento por volumen.

Reglas del refactor:
  - NO cambies la firma pública `total_pedido(lineas)`: los tests dependen de ella.
  - NO cambies el comportamiento: los tests deben seguir VERDES después de CADA cambio.
  - Avanza en pasos pequeños y corre `pytest` entre cada uno.

Corre los tests con:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno

Qué dejar limpio (ver lección 2.2, secciones 4.1–4.4):
  1. Nombres que revelan intención (adiós a `d`, `r`, `i`).
  2. Sin índices mágicos (`i[1]`): desempaqueta la tupla.
  3. Números mágicos (100000, 0.1) en CONSTANTES con nombre.
  4. Una función, una responsabilidad: separa "sumar activas" de "aplicar descuento".
"""


def total_pedido(d):
    r = 0
    for i in d:
        if i[3] == True:
            r = r + i[1] * i[2]
    if r > 100000:
        r = r - int(r * 0.1)
    return r


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que imprime ANTES de correrlo?
    pedido = [
        ("pan", 1500, 2, True),
        ("leche", 1200, 1, False),   # inactiva: NO suma
        ("café", 8000, 1, True),
    ]
    print(total_pedido(pedido))               # subtotal pequeño, sin descuento
    pedido_grande = [("notebook", 120000, 1, True)]
    print(total_pedido(pedido_grande))        # subtotal > umbral: con descuento
