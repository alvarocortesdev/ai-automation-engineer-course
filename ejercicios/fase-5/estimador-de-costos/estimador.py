"""Estimador de costos cloud — Primero-Sin-IA.

Implementa `estimar_costo_mensual` a mano, sin IA. NO cambies la firma ni las
claves del diccionario que devuelves: los tests de `test_estimador.py` dependen
de ellas.

Idea: estimar el costo mensual de una arquitectura ANTES de desplegarla,
descomponiéndolo en los 4 drivers de costo de la nube. Es el hábito de FinOps
que te salva de las facturas sorpresa (y, en la Fase 6, de los tokens de un LLM
fuera de control).

──────────────────────────────────────────────────────────────────────────────
CONTRATO

Entrada `arquitectura` (dict):
    {
        "compute": [                       # lista de recursos de compute
            {"nombre": str,
             "usd_por_hora": float,         # precio por hora encendido
             "horas_encendido": float},     # 730 = todo el mes; menos = scale-to-zero
            ...
        ],
        "storage_gb": float,               # GB guardados en object storage
        "egress_gb": float,                # GB que SALEN a internet en el mes
        "requests_millones": float,        # invocaciones, en millones
    }

Entrada `precios` (dict):
    {
        "storage_usd_por_gb_mes": float,
        "egress_usd_por_gb": float,        # precio por GB POR ENCIMA del tramo gratis
        "egress_gratis_gb": float,         # primeros N GB/mes gratis (p. ej. 100)
        "usd_por_millon_requests": float,
    }

Salida (dict) — desglose por driver MÁS el total:
    {
        "compute": float,   # suma de (usd_por_hora * horas_encendido) de cada recurso
        "storage": float,   # storage_gb * precio por GB-mes
        "egress": float,    # SOLO los GB por encima del tramo gratis, nunca negativo
        "requests": float,  # requests_millones * precio por millón
        "total": float,     # suma de los cuatro
    }

Reglas clave (donde está el aprendizaje):
    - El egress se cobra SOLO por encima del tramo gratis: usa max(0, ...). Si la
      app sirve menos que el tramo gratis, el egress cuesta 0 (no negativo).
    - El compute cobra por horas ENCENDIDO: un recurso always-on (730 h) cuesta
      aunque no atienda tráfico; uno scale-to-zero cobra solo sus pocas horas.
    - No redondees el resultado; los tests comparan con tolerancia.
"""


def estimar_costo_mensual(arquitectura: dict, precios: dict) -> dict:
    """Devuelve el desglose de costo mensual por driver + el total. Ver el contrato arriba."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Prueba rápida manual (Predict–Run): ¿qué crees que da el total ANTES de correrlo?
    arquitectura = {
        "compute": [
            {"nombre": "api", "usd_por_hora": 0.02, "horas_encendido": 100},   # scale-to-zero
            {"nombre": "nat-gateway", "usd_por_hora": 0.045, "horas_encendido": 730},  # always-on
        ],
        "storage_gb": 10.0,
        "egress_gb": 80.0,          # por debajo del tramo gratis
        "requests_millones": 2.0,
    }
    precios = {
        "storage_usd_por_gb_mes": 0.023,
        "egress_usd_por_gb": 0.09,
        "egress_gratis_gb": 100.0,
        "usd_por_millon_requests": 0.20,
    }
    print(estimar_costo_mensual(arquitectura, precios))
