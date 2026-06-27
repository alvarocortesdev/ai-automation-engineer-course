"""El cerebro de un pipeline de IDP: gate de confianza + validación cruzada.

Completa las TRES funciones. Los datos extraídos se INYECTAN como diccionarios:
así pruebas la LÓGICA de decisión sin depender de ninguna API ni API key.

Forma de un `doc`:
    {
        "campos": {
            "Proveedor": {"value": "ACME SpA", "confidence": 0.99},
            "Fecha":     {"value": "2026-06-01", "confidence": 0.93},
            "Total":     {"value": 90000, "confidence": 0.97},
        },
        "items": [
            {"descripcion": "Servicio A", "monto": 60000},
            {"descripcion": "Servicio B", "monto": 30000},
        ],
        "total_declarado": 90000,
    }
"""
from __future__ import annotations


def clasificar_campos(campos: dict, umbral: float) -> dict:
    """Separa los campos auto-aceptables de los que van a revisión humana.

    Devuelve {"auto": [nombres...], "revisar": [nombres...]} en el ORDEN de entrada.
    Un campo va a "revisar" si su confidence es None o es MENOR que el umbral.
    confidence == umbral se auto-acepta (la regla es >= umbral).
    """
    raise NotImplementedError("implementa clasificar_campos")


def total_cuadra(items: list, total_declarado: float, tolerancia: float = 0.01) -> bool:
    """True si la suma de los montos de las líneas cuadra con el total declarado.

    Compara con TOLERANCIA: abs(suma - total_declarado) <= tolerancia.
    Nunca uses == directo sobre floats (0.1 + 0.2 != 0.3 en coma flotante).
    """
    raise NotImplementedError("implementa total_cuadra")


def decidir_procesamiento(doc: dict, umbral: float, tolerancia: float = 0.01) -> dict:
    """Decisión final del pipeline: auto vs revisión humana.

    Devuelve {"accion": "auto" | "revision_humana", "motivos": [str, ...]}.
    Es "auto" SOLO si todos los campos pasan el gate Y el total cuadra.
    Si cualquiera falla -> "revision_humana", juntando los motivos (campos dudosos
    y/o total descuadrado) para que el humano sepa qué mirar.
    Si accion == "auto", motivos == [].

    DEBE reusar clasificar_campos y total_cuadra (no reimplementes su lógica aquí).
    """
    raise NotImplementedError("implementa decidir_procesamiento")
