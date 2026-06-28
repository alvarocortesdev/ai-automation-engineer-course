"""Starter — Primero-Sin-IA. Implementa la función a mano, sin IA.

Objetivo: codificar la ESCALERA DE INTEGRACIÓN como una función pura y testeable.
Sube siempre al escalón más alto posible:

    Escalón 1  · "api"                -> existe API/webhook: integra por el contrato.
    Escalón 2  · "navegador"          -> sin API, pero es web: navegador headless
                                         con selectores semánticos (no coordenadas).
    Escalón 3  · "rpa-ui"             -> ni API ni web (app de escritorio legacy):
                                         RPA de UI como ÚLTIMO recurso.
    Escalón 0  · "rediseñar-proceso"  -> ni API ni web Y el proceso es crítico o de
                                         alto volumen: la UI-automation NO es base
                                         aceptable; presiona por API / export / ETL.

NO cambies las firmas ni los nombres de los campos: los tests dependen de ellos.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Caso:
    """Las features de una automatización que deciden su estrategia."""

    tiene_api: bool          # ¿el sistema destino expone una API o webhook?
    es_web: bool             # si no hay API, ¿la interfaz es una página web?
    volumen_alto: bool       # ¿muchas ejecuciones / gran volumen de registros?
    critico: bool            # ¿una falla silenciosa causa daño grave?
    ui_cambia_seguido: bool  # ¿la UI cambia con frecuencia (rediseños)?


@dataclass(frozen=True)
class Recomendacion:
    """La salida: qué estrategia y POR QUÉ."""

    estrategia: str  # "api" | "navegador" | "rpa-ui" | "rediseñar-proceso"
    motivo: str      # explica la restricción dominante que decidió la estrategia


def recomendar_automatizacion(caso: Caso) -> Recomendacion:
    """Aplica la escalera de integración a un caso y recomienda la estrategia.

    Contrato:
        - Si hay API, gana SIEMPRE ("api"), sin importar las otras flags.
        - Sin API: si el proceso es crítico o de alto volumen, la UI-automation no
          es base aceptable -> "rediseñar-proceso".
        - Sin API, no crítico ni alto volumen, pero es web -> "navegador".
        - Sin API, no crítico ni alto volumen, y NO es web -> "rpa-ui".
        - El `motivo` debe explicar el POR QUÉ (la restricción dominante), no solo
          repetir la estrategia.
    """
    raise NotImplementedError("Implementa esta función a mano, sin IA.")


if __name__ == "__main__":
    # Predict–Run: ¿qué crees que recomienda ANTES de implementar?
    ejemplo = Caso(
        tiene_api=False,
        es_web=True,
        volumen_alto=False,
        critico=False,
        ui_cambia_seguido=False,
    )
    print(recomendar_automatizacion(ejemplo))
