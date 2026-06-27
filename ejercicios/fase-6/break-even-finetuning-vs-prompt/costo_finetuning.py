"""Punto de equilibrio de costo: baseline (prompt largo) vs modelo fine-tuneado.

Idea central:
  - El BASELINE manda un prompt largo de few-shot en CADA request (caro por request,
    sin costo fijo). Costo total = n_requests * costo_por_request_baseline.
  - El FINE-TUNING hornea esa forma en los pesos: el prompt se acorta, así que el costo
    POR REQUEST baja... pero pagas un costo FIJO de entrenamiento una sola vez, y a veces
    el modelo fine-tuneado cuesta MÁS por token. Costo total = entrenamiento + n * c_ft.

El "punto de equilibrio" es el número de requests donde ambos totales se igualan:

    equilibrio = costo_entrenamiento / (costo_req_baseline - costo_req_ft)

Por debajo gana el baseline; por encima (volumen alto y sostenido) gana el fine-tuning.
OJO: si el modelo fine-tuneado NO es más barato por request (ahorro <= 0), no hay
equilibrio: el fine-tuning nunca se paga por costo, sin importar el volumen.

Completa las tres funciones. NO uses precios hardcodeados ni red: todo se INYECTA como
parámetros, así tu lógica es pura, determinista y testeable.

Pricing en USD por MILLÓN de tokens (1M = 1_000_000), distinto para entrada y salida.
"""
from __future__ import annotations


def costo_por_request(
    prompt_tokens: int,
    output_tokens: int,
    precio_in: float,
    precio_out: float,
) -> float:
    """Costo en USD de UN request.

    Formula: (prompt_tokens / 1e6) * precio_in + (output_tokens / 1e6) * precio_out
    (precio_in y precio_out vienen dados POR MILLON de tokens).
    """
    raise NotImplementedError("implementa costo_por_request")


def costo_total(
    costo_fijo: float,
    costo_req: float,
    n_requests: int,
) -> float:
    """Costo total en USD: un costo FIJO una vez + n_requests por el costo por request.

    Para el baseline, costo_fijo = 0 (no hay entrenamiento).
    Para el fine-tuning, costo_fijo = costo de entrenamiento.
    """
    raise NotImplementedError("implementa costo_total")


def requests_equilibrio_finetuning(
    costo_entrenamiento: float,
    costo_req_baseline: float,
    costo_req_ft: float,
) -> float:
    """Numero de requests donde el fine-tuning iguala al baseline en costo total.

    equilibrio = costo_entrenamiento / (costo_req_baseline - costo_req_ft)

    El denominador es el AHORRO por request que da el fine-tuning (prompt mas corto).
    Lanza ValueError si ese ahorro es <= 0: si el modelo fine-tuneado no es mas barato
    por request, no hay numero de requests que recupere el costo de entrenamiento
    (el fine-tuning nunca gana por costo).
    """
    raise NotImplementedError("implementa requests_equilibrio_finetuning")
