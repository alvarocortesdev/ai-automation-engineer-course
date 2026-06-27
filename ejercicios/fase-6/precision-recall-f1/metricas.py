"""Ejercicio 6.0 — Precision, recall y F1 desde cero (Primero-Sin-IA).

Implementa las funciones a mano, en Python puro (sin scikit-learn, sin IA).
NO cambies las firmas: los tests de `test_metricas.py` dependen de ellas.

Corre los tests desde esta carpeta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""


def contar(y_true, y_pred):
    """Cuenta TP, FP y FN comparando etiquetas reales contra predichas.

    - y_true, y_pred: listas de 0/1 del MISMO largo. 1 = clase positiva.

    Devuelve la tupla (tp, fp, fn):
      tp: real=1 y pred=1   (verdadero positivo)
      fp: real=0 y pred=1   (falso positivo)
      fn: real=1 y pred=0   (falso negativo)

    Lanza ValueError si las listas tienen distinto largo.
    """
    # TODO(estudiante): borra esta línea y escribe tu solución a mano, sin IA.
    raise NotImplementedError("Implementa contar")


def precision(tp, fp):
    """precision = tp / (tp + fp).

    Si tp + fp == 0 (no predijiste ningún positivo), devuelve 0.0; NO lances
    una excepción de división por cero.
    """
    raise NotImplementedError("Implementa precision")


def recall(tp, fn):
    """recall = tp / (tp + fn).

    Si tp + fn == 0 (no había positivos reales), devuelve 0.0.
    """
    raise NotImplementedError("Implementa recall")


def f1(p, r):
    """F1 = media armónica de precision y recall = 2 * p * r / (p + r).

    Si p + r == 0, devuelve 0.0 (no 0.5: la armónica castiga el desequilibrio).
    """
    raise NotImplementedError("Implementa f1")


def evaluar(y_true, y_pred):
    """Eval completo: devuelve {'precision': ..., 'recall': ..., 'f1': ...}.

    Compón las funciones anteriores: cuenta, luego deriva las tres métricas.
    """
    raise NotImplementedError("Implementa evaluar")


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que imprime ANTES de correrlo?
    y_true = [1, 1, 0, 1, 0, 0]
    y_pred = [1, 0, 0, 1, 1, 0]
    print(evaluar(y_true, y_pred))
