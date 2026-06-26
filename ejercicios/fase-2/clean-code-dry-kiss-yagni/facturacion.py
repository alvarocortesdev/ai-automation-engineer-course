"""Ejercicio 2.2 — DRY/KISS/YAGNI con criterio (Primero-Sin-IA).

Las cuatro funciones de abajo YA FUNCIONAN y los tests YA pasan en verde. Tienen tres
problemas de CRITERIO distintos. Tu trabajo es aplicar el principio correcto a cada uno
—y RESISTIR aplicarlo donde no toca— sin cambiar el comportamiento.

  (a) DUPLICACIÓN REAL  -> la fórmula del IVA (`x + int(x * 0.19)`) está copiada en dos
      funciones, y hay una constante IVA definida pero sin usar. Aplica DRY: una sola
      representación de ese conocimiento.

  (b) DUPLICACIÓN INCIDENTAL (trampa) -> `es_rut_valido` y `es_sku_valido` se PARECEN
      (mismo `isinstance` + `len >= 3`), pero validan conceptos SIN relación. Un RUT y un
      SKU cambian sus reglas por razones distintas. Unirlos en un validador genérico los
      ACOPLA: el día que el RUT cambie su regla, romperías el SKU. Resiste la falsa DRY:
      DÉJALOS SEPARADOS.

  (c) SOBRE-INGENIERÍA -> `formatear_precio` tiene cinco parámetros, pero en todo el código
      (mira los tests) solo se llama como `formatear_precio(monto)`. Los otros knobs son
      futuro imaginado. Aplica KISS/YAGNI: simplifícala a lo que de verdad se usa.

Entregable: este archivo refactorizado + un `decisiones.md` con las TRES decisiones (incluida
la de NO unir los validadores), cada una con su porqué en 1-2 frases.

Corre los tests con:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

IVA = 0.19  # tasa de IVA en Chile (19%)


def precio_con_iva(neto):
    return neto + int(neto * 0.19)


def precio_con_iva_descuento(neto, descuento_pct):
    con_descuento = neto - int(neto * descuento_pct)
    return con_descuento + int(con_descuento * 0.19)


def es_rut_valido(rut):
    return isinstance(rut, str) and len(rut) >= 3


def es_sku_valido(sku):
    return isinstance(sku, str) and len(sku) >= 3


def formatear_precio(monto, moneda="CLP", separador_miles=True, simbolo=True, decimales=0):
    if separador_miles:
        cuerpo = f"{monto:,.{decimales}f}".replace(",", ".")
    else:
        cuerpo = f"{monto:.{decimales}f}"
    if simbolo:
        if moneda == "CLP":
            return f"${cuerpo}"
        elif moneda == "USD":
            return f"US${cuerpo}"
        else:
            return f"{cuerpo} {moneda}"
    return cuerpo


if __name__ == "__main__":
    print(precio_con_iva(10000))                 # 11900
    print(precio_con_iva_descuento(10000, 0.10)) # 10710
    print(es_rut_valido("12345678-9"))           # True
    print(es_sku_valido("ABC-100"))              # True
    print(formatear_precio(1234))                # $1.234
