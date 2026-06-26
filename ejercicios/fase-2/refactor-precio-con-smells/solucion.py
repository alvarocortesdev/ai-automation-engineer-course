"""Ejercicio 2.3 — Refactoriza una función con smells (red ya puesta).

Esta función CALCULA BIEN el total de una orden y la suite de `test_solucion.py`
está en VERDE. Tu trabajo NO es cambiar lo que hace, sino dejarla limpia:
refactorings con nombre, uno a la vez, corriendo `pytest` después de cada paso,
sin que ningún test se ponga rojo.

Reglas:
- NO cambies el comportamiento: mismas entradas -> mismas salidas (números).
- NO modifiques las ASERCIONES de los tests. Si renombras la función pública
  `calc`, actualiza SOLO la línea de `import` del test (eso es parte del
  refactoring Rename Function; lo viste en la sección 4.2 de la lección).
- Caza, como mínimo: mysterious names, magic numbers, long function,
  duplicated code (vip vs frecuente), nested conditionals, comment-as-deodorant.

Empieza corriendo `pytest` y confirmando el VERDE de partida.
"""


def calc(items, c, p):
    # items: lista de (nombre, precio, cantidad)
    # c: tipo de cliente
    # p: codigo de cupon
    # calcular el subtotal sumando
    t = 0
    for i in items:
        t = t + i[1] * i[2]
    # aplicar descuento por tipo de cliente
    if c == "vip":
        if t > 100000:
            t = t - t * 0.20
        else:
            t = t - t * 0.10
    else:
        if c == "frecuente":
            if t > 100000:
                t = t - t * 0.10
            else:
                t = t - t * 0.05
    # aplicar el cupon de envio
    if p == "ENVIOGRATIS":
        envio = 0
    else:
        if t > 50000:
            envio = 0
        else:
            envio = 3990
    # calcular el iva y devolver
    iva = t * 0.19
    return t + iva + envio


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    print(calc([("pan", 10000, 2)], "normal", None))
