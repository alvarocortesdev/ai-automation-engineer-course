"""Mutante B — bug introducido a propósito (NO lo arregles).

Diferencia con el SUT correcto: se OLVIDA de aplicar el descuento de socio. Una
suite buena, con un caso `es_socio=True`, debe ponerse ROJA contra este módulo.
"""

import math

TARIFA_BASE = 2990
RECARGO_POR_KG = 700
ZONAS_REMOTAS = {"patagonia", "isla"}
RECARGO_REMOTO = 3000
DESCUENTO_SOCIO = 0.15


def _kg_facturables(peso_kg):
    return math.ceil(peso_kg)


def costo_envio(peso_kg, zona, es_socio):
    if peso_kg <= 0:
        raise ValueError("peso_kg debe ser mayor que 0")
    costo = TARIFA_BASE + RECARGO_POR_KG * _kg_facturables(peso_kg)
    if zona in ZONAS_REMOTAS:
        costo += RECARGO_REMOTO
    # BUG: nunca aplica DESCUENTO_SOCIO aunque es_socio sea True
    return round(costo, 2)


def cotizar(peso_kg, zona, es_socio, tasa_usd):
    clp = costo_envio(peso_kg, zona, es_socio)
    return round(clp / tasa_usd(), 2)
