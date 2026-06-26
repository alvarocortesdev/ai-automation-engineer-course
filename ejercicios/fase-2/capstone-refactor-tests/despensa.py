"""Despensa — herramienta de alerta de stock y vencimientos.

⚠️  CÓDIGO DE PARTIDA DEL CAPSTONE — funciona, pero da vergüenza.

Esta es la "versión junior": una sola función `run` que LEE un archivo, DECIDE
las alertas y las IMPRIME, todo mezclado. Tiene magic numbers (2, 3, 0), nombres
mudos (`x`, `d`, `f`, `res`), cero tests y cero type hints en la lógica.

NO la borres para reescribirla de cero: eso es un rewrite, no un refactor (lee el
README). Tu trabajo es:
  1. Fijar su comportamiento ACTUAL con tests de caracterización.
  2. Refactorizarla en pasos pequeños, con la red verde en cada paso.
  3. Endurecer la suite con mutation testing.

Úsala como sujeto del capstone, o reemplázala por tu propia app de la Fase 1.

Ejecutar:
    uv run python despensa.py tests/datos/despensa-ejemplo.json
"""

import json
import sys
from datetime import date, datetime


def run(archivo, hoy=None):
    if hoy is None:
        hoy = date.today()
    f = open(archivo)
    data = json.load(f)
    f.close()
    res = []
    for x in data:
        alerta = ""
        if x["cantidad"] <= 2:
            alerta = "STOCK BAJO"
        if x.get("vence"):
            d = datetime.strptime(x["vence"], "%Y-%m-%d").date()
            dias = (d - hoy).days
            if dias < 0:
                if alerta != "":
                    alerta = alerta + " + VENCIDO"
                else:
                    alerta = "VENCIDO"
            elif dias <= 3:
                if alerta != "":
                    alerta = alerta + " + POR VENCER"
                else:
                    alerta = "POR VENCER"
        if alerta != "":
            res.append(x["nombre"] + ": " + alerta)
    for r in res:
        print(r)
    return res


if __name__ == "__main__":
    run(sys.argv[1])
