"""Reductor CDC -> tareas de re-embedding.

Completa `reducir` para convertir una tanda de eventos de cambio (CDC, en orden
por `lsn`) en la lista MÍNIMA, IDEMPOTENTE y DEBOUNCED de tareas para el vector DB
de un RAG.

Modelo mental (lección 7.6):
  - Un evento describe un cambio en la fila: c/r/u = la fila existe; d = se borró.
  - El campo que se embeddea es `after["contenido"]`.
  - Varios eventos de la misma key colapsan a su INTENCIÓN FINAL (debounce).
  - Propagar deletes (si no, queda fantasma en el índice).
  - NO re-embeddear contenido idéntico al ya indexado (costo: no pagues un vector igual).
  - Idempotencia: reprocesar la misma tanda deja el resultado idéntico (CDC es at-least-once).
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Modelo de entrada y salida (ya está completo: NO lo cambies).
# ---------------------------------------------------------------------------
@dataclass
class Evento:
    """Un change event CDC (Debezium-style, aplanado).

    op:    "c" create | "r" read/snapshot | "u" update | "d" delete.
    key:   identidad de la fila (clave de upsert/delete en el vector DB).
    after: estado de la fila tras el cambio. En un `d` es None.
           El texto que se embeddea es after["contenido"].
    """
    op: str
    key: str
    after: dict | None = None


@dataclass
class Tarea:
    """Una acción sobre el vector DB.

    accion:    "upsert" | "delete".
    key:       fila afectada.
    contenido: texto a embeddear en un upsert; None en un delete.
    """
    accion: str
    key: str
    contenido: str | None = None


# ---------------------------------------------------------------------------
# TODO: implementa esta función.
# ---------------------------------------------------------------------------
def reducir(eventos: list[Evento], indexado: dict[str, str]) -> list[Tarea]:
    """Reduce `eventos` (en orden) a las tareas mínimas para el vector DB.

    `indexado` mapea key -> contenido actualmente embeddeado en el vector DB.

    Reglas (ver README):
      1. Debounce: varios eventos de la misma key -> su intención final.
      2. op: c/r/u -> la fila existe con after["contenido"]; d -> borrada.
      3. Delete propagado: key terminó borrada Y estaba en `indexado` -> Tarea("delete", key).
      4. Nace y muere: key terminó borrada y NO estaba en `indexado` -> ninguna tarea.
      5. No re-embeddear igual: key viva con contenido == indexado[key] -> ninguna tarea.
      6. Upsert: key viva con contenido distinto (o nueva) -> Tarea("upsert", key, contenido).
      7. Determinismo: la lista sale ORDENADA por key.

    Sugerencia: dos pasadas. (a) construye el estado final por key recorriendo en
    orden; (b) decide la tarea de cada key comparando contra `indexado`.
    """
    # TODO: implementa las dos pasadas y devuelve la lista de Tarea.
    raise NotImplementedError
