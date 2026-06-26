"""Ejercicio 2.6 — Suite pytest para un módulo de envíos (SUT).

Este módulo CALCULA BIEN. NO lo modifiques: tu trabajo es escribir la suite de
tests en `test_solucion.py`. El módulo es el "system under test" (SUT).

- `costo_envio` es LÓGICA PURA: no toca red, disco ni hora. NO se mockea; se
  verifica por su valor de retorno.
- `cotizar` usa una dependencia inyectada `tasa_usd` (una llamada que en
  producción iría a la red para obtener el tipo de cambio): esa es la FRONTERA.
  En tus tests, esa frontera se mockea/inyecta; `costo_envio` NO.

Se cobra por kilo COMPLETO (se redondea hacia arriba: 2.1 kg cobra como 3 kg).
"""

import math

TARIFA_BASE = 2990
RECARGO_POR_KG = 700
ZONAS_REMOTAS = {"patagonia", "isla"}
RECARGO_REMOTO = 3000
DESCUENTO_SOCIO = 0.15


def _kg_facturables(peso_kg):
    # Se cobra por kg entero, redondeando hacia ARRIBA.
    return math.ceil(peso_kg)


def costo_envio(peso_kg, zona, es_socio):
    """Costo de envío en CLP. Lógica pura, determinista."""
    if peso_kg <= 0:
        raise ValueError("peso_kg debe ser mayor que 0")
    costo = TARIFA_BASE + RECARGO_POR_KG * _kg_facturables(peso_kg)
    if zona in ZONAS_REMOTAS:
        costo += RECARGO_REMOTO
    if es_socio:
        costo *= (1 - DESCUENTO_SOCIO)
    return round(costo, 2)


def cotizar(peso_kg, zona, es_socio, tasa_usd):
    """Costo de envío convertido a USD.

    `tasa_usd` es un callable SIN argumentos que devuelve cuántos CLP vale 1 USD
    (en producción consulta un servicio externo: la frontera). Aquí se inyecta
    para poder testear sin red.
    """
    clp = costo_envio(peso_kg, zona, es_socio)
    return round(clp / tasa_usd(), 2)


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que imprime ANTES de correrlo?
    print(costo_envio(2.0, "metropolitana", es_socio=False))
    print(costo_envio(2.1, "metropolitana", es_socio=False))
