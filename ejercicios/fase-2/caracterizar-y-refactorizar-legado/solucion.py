"""Ejercicio 2.3 — Caracteriza y refactoriza código legado (sin red).

Esta función clasifica un envío según su peso y su zona. Está enredada, tiene
duplicación... y NO tiene ni un solo test. Es código legado real.

NO la refactorices todavía. Tu PRIMER trabajo es construir la red de seguridad:
escribir en `test_solucion.py` characterization tests que pinten lo que esta
función hace HOY (incluidos sus bordes y sus rarezas). Solo cuando esa red esté
en VERDE, empiezas a mover código.

zona: 1 = local · 2 = nacional · 3 = internacional
(¿y una zona desconocida, como 5? Obsérvalo: es parte de lo que debes caracterizar.)
"""


def etiqueta_envio(peso_gramos, zona):
    if zona == 1:
        if peso_gramos < 500:
            return "local-ligero"
        else:
            if peso_gramos < 2000:
                return "local-medio"
            else:
                return "local-pesado"
    else:
        if zona == 2:
            if peso_gramos < 500:
                return "nacional-ligero"
            else:
                if peso_gramos < 2000:
                    return "nacional-medio"
                else:
                    return "nacional-pesado"
        else:
            if peso_gramos < 1000:
                return "internacional-estandar"
            else:
                return "internacional-especial"


if __name__ == "__main__":
    # Predict–Run: predice CADA salida antes de correr esto.
    for caso in [(499, 1), (500, 1), (2000, 2), (999, 3), (1000, 3), (100, 5)]:
        print(caso, "->", etiqueta_envio(*caso))
