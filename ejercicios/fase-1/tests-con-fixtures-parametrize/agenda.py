"""Módulo BAJO PRUEBA — NO lo modifiques. Tu tarea es TESTEARLO.

Una mini-agenda persistida en JSON. Tres funciones:
  - guardar_eventos(ruta, eventos): escribe la lista de eventos como JSON.
  - cargar_eventos(ruta): lee la lista; [] si no existe; AgendaCorrupta si el JSON es inválido.
  - proximos(eventos, hoy): eventos con fecha >= hoy, ordenados por fecha.

Las fechas son strings ISO "YYYY-MM-DD": comparadas como texto, su orden
lexicográfico coincide con el cronológico (por eso "2026-07-01" >= "2026-06-30").
"""

from __future__ import annotations

import json


class AgendaCorrupta(Exception):
    """El archivo existe pero no contiene JSON válido."""


def guardar_eventos(ruta, eventos: list) -> None:
    """Escribe `eventos` en `ruta` como JSON UTF-8 indentado."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)


def cargar_eventos(ruta) -> list:
    """Lee los eventos de `ruta`.

    - archivo inexistente -> []  (es esperable la primera vez)
    - JSON inválido       -> lanza AgendaCorrupta (un bug que hay que gritar, no esconder)
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise AgendaCorrupta(f"{ruta} no es JSON válido: {e}") from e


def proximos(eventos: list, hoy: str) -> list:
    """Devuelve los eventos cuya fecha es >= `hoy`, ordenados por fecha ascendente."""
    futuros = [e for e in eventos if e["fecha"] >= hoy]
    return sorted(futuros, key=lambda e: e["fecha"])
