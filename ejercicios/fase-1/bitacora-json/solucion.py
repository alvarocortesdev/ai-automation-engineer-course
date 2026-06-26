"""Starter del ejercicio — Primero-Sin-IA.

Implementa las tres funciones a mano, sin IA. NO cambies las firmas: los tests
de `test_solucion.py` dependen de ellas. La excepción `BitacoraCorrupta` ya está
definida; úsala donde el contrato lo pide.

Lee la sección 4.3 de la lección (1.5 Archivos, JSON y APIs) si te trabas.
"""

from __future__ import annotations

import json
from pathlib import Path


class BitacoraCorrupta(Exception):
    """El archivo existe pero su contenido no es JSON válido."""


def cargar(ruta: str | Path) -> list:
    """Carga la lista de registros desde un archivo JSON.

    Contrato:
        - archivo inexistente  -> devuelve []  (no es un error)
        - JSON inválido        -> lanza BitacoraCorrupta (envolviendo el error original)
        - JSON válido          -> devuelve la lista parseada
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


def agregar(ruta: str | Path, mensaje: str) -> None:
    """Carga la bitácora, agrega {"mensaje": mensaje} al final y la guarda.

    Debe guardar con encoding='utf-8', ensure_ascii=False e indent=2 para no
    corromper acentos/ñ y dejar el archivo legible.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


def resumen(registros: list) -> dict:
    """Devuelve {"total": n} con la cantidad de registros."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que imprime ANTES de correrlo?
    ruta = "bitacora_demo.json"
    agregar(ruta, "primer registro ñandú")
    agregar(ruta, "segundo registro")
    print(cargar(ruta))
    print(resumen(cargar(ruta)))
