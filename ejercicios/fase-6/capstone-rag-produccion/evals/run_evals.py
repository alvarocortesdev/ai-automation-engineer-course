#!/usr/bin/env python3
"""Eval harness del capstone RAG — esqueleto.

eval-first: este script debe CORRER y dar un numero desde M0, aunque el RAG todavia
no exista. El gate (gate_de_regresion) ya viene implementado y testeado en
tests/test_gate.py. Tu trabajo es completar los TODO: recuperar(), responder() y los
scorers (context recall/precision son deterministas; faithfulness necesita un juez LLM).

Uso:
    uv run python evals/run_evals.py --baseline evals/baseline.json \\
        --umbral 0.75 --tolerancia 0.02

Sale con codigo != 0 si el promedio cae bajo el umbral O regresa vs baseline:
ese exit code es el que bloquea el merge en CI.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Resultado:
    promedio: float
    por_metrica: dict[str, float]
    fallos: list[dict] = field(default_factory=list)


def precision_recall_at_k(recuperados: list[str], relevantes: set[str], k: int) -> tuple[float, float]:
    """Deterministas, teoria de conjuntos. precision@k = hits/k, recall@k = hits/|relevantes|."""
    top_k = recuperados[:k]
    hits = len(set(top_k) & relevantes)
    precision = hits / k if k else 0.0
    recall = hits / len(relevantes) if relevantes else 1.0
    return precision, recall


def cargar_dataset(ruta: Path) -> list[dict]:
    return [json.loads(linea) for linea in ruta.read_text(encoding="utf-8").splitlines() if linea.strip()]


# --- TODO: conecta tu sistema RAG real ---------------------------------------
def recuperar(pregunta: str) -> list[str]:
    """Devuelve los ids de chunks recuperados (hybrid search + reranking). TODO."""
    raise NotImplementedError("Conecta tu retrieval real (6.7) aqui.")


def faithfulness(pregunta: str, respuesta: str, chunks: list[str]) -> float:
    """Mide si la respuesta se sostiene SOLO en los chunks. Necesita un juez LLM (6.9). TODO."""
    raise NotImplementedError("Implementa el LLM-as-judge de faithfulness (6.9).")
# -----------------------------------------------------------------------------


def correr_eval(dataset: list[dict], k: int = 5) -> Resultado:
    recalls, precisions = [], []
    fallos: list[dict] = []
    for caso in dataset:
        relevantes = set(caso["chunks_relevantes"])
        recuperados = recuperar(caso["pregunta"])
        p, r = precision_recall_at_k(recuperados, relevantes, k)
        precisions.append(p)
        recalls.append(r)
        if r < 1.0:  # guarda los casos malos, no solo el promedio
            fallos.append({"pregunta": caso["pregunta"], "recall": r, "precision": p})
    recall_medio = sum(recalls) / len(recalls) if recalls else 0.0
    precision_media = sum(precisions) / len(precisions) if precisions else 0.0
    # faithfulness se promedia aparte (requiere generar respuestas + juez)
    return Resultado(
        promedio=recall_medio,  # metrica principal del gate; ajusta a tu criterio
        por_metrica={"context_recall": recall_medio, "context_precision": precision_media},
        fallos=fallos,
    )


def gate_de_regresion(
    score: float,
    umbral: float,
    baseline: float | None = None,
    tolerancia: float = 0.0,
) -> tuple[bool, str]:
    """True = pasa. Bloquea si NO llega al umbral absoluto O si regresa vs baseline.

    Es la pieza clave del DoD-5: el chequeo de regresion es el que la gente olvida.
    """
    if score < umbral:
        return False, f"umbral: {score:.3f} < {umbral:.3f}"
    if baseline is not None and score < baseline - tolerancia:
        return False, f"regresion: {score:.3f} < baseline {baseline:.3f} - {tolerancia:.3f}"
    return True, "ok"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="eval harness RAG con gate de regresion")
    parser.add_argument("--dataset", type=Path, default=Path(__file__).with_name("dataset.jsonl"))
    parser.add_argument("--baseline", type=Path, default=None)
    parser.add_argument("--umbral", type=float, default=0.75)
    parser.add_argument("--tolerancia", type=float, default=0.02)
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args(argv)

    dataset = cargar_dataset(args.dataset)
    resultado = correr_eval(dataset, k=args.k)

    baseline_score = None
    if args.baseline and args.baseline.exists():
        baseline_score = json.loads(args.baseline.read_text(encoding="utf-8")).get("promedio")

    pasa, razon = gate_de_regresion(resultado.promedio, args.umbral, baseline_score, args.tolerancia)

    print(f"score: {resultado.promedio:.3f}  metricas: {resultado.por_metrica}")
    print(f"casos malos: {len(resultado.fallos)}")
    print(f"gate: {'PASA' if pasa else 'BLOQUEA'} ({razon})")
    return 0 if pasa else 1


if __name__ == "__main__":
    sys.exit(main())
