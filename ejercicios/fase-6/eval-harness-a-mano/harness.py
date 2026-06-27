"""Un eval harness para las métricas de RETRIEVAL de un RAG, a mano.

Las cuatro piezas de cualquier eval harness:
    dataset -> scorer (por caso) -> agregación (media) -> gate (umbral + regresión)

Todo es DETERMINISTA: no se llama a ningún LLM ni a la red. El "sistema" que evalúas
(el retriever) se INYECTA como una función `pregunta -> list[str]`, para que puedas
probar la lógica con un retriever falso guionizado.

Recuerda la diferencia que decide todo:
    precision@k = hits / k                 -> castiga traer RUIDO
    recall@k    = hits / len(relevantes)   -> castiga DEJAR FUERA lo necesario
El único cambio es el denominador, y lo es todo.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CasoRAG:
    pregunta: str
    relevantes: set[str]          # chunk-ids que DEBÍAN recuperarse (golden)


@dataclass
class ResultadoGate:
    pasa: bool
    razon: str


def precision_recall_at_k(recuperados: list[str], relevantes: set[str], k: int) -> tuple[float, float]:
    """Calcula (precision@k, recall@k) sobre los primeros k chunks recuperados.

    - Considera solo `recuperados[:k]`.
    - hits = cuántos de esos están en `relevantes`.
    - precision = hits / k
    - recall    = hits / len(relevantes); 1.0 si `relevantes` está vacío.
    """
    raise NotImplementedError("Implementa precision@k y recall@k a mano (teoría de conjuntos).")


def correr_eval(sistema, dataset: list[CasoRAG], k: int) -> dict:
    """Corre `sistema` (pregunta -> list[str]) sobre el dataset y agrega las métricas.

    Devuelve un dict con:
        - "recall":   media de recall@k sobre el dataset
        - "precision": media de precision@k sobre el dataset
        - "n":        número de casos
        - "fallos":   lista de los casos con recall < 1.0 (se dejó fuera un chunk
                      relevante). Cada fallo es un dict:
                      {"pregunta", "precision", "recall", "recuperados"}
    """
    raise NotImplementedError("Corre el sistema sobre cada caso, puntúa, agrega y guarda los fallos.")


def gate_de_regresion(resumen: dict, umbral: float, baseline: float | None = None,
                      tolerancia: float = 0.02) -> ResultadoGate:
    """Gate sobre resumen["recall"]: barra absoluta + chequeo de regresión vs baseline.

    - si recall < umbral                       -> no pasa (barra absoluta)
    - si baseline y recall < baseline - tolerancia -> no pasa (regresión)
    - si no                                    -> pasa
    """
    raise NotImplementedError("Implementa el gate: umbral absoluto Y regresión vs baseline.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    p, r = precision_recall_at_k(["c1", "c2", "c3", "c4"], {"c1", "c3"}, k=4)
    print(f"precision@4={p}  recall@4={r}")
