"""Output handling: gate de salida de un LLM (LLM05 Improper Output Handling).

La salida del modelo es NO confiable. Antes de renderizarla como HTML, este modulo
aplica tres capas EN ORDEN:
    1. fuga        -> BLOQUEAR  (LLM07 System Prompt Leakage / LLM02 Sensitive Info)
    2. presupuesto -> BLOQUEAR  (LLM10 Unbounded Consumption)
    3. codificacion para el sink (HTML) -> RENDER con el texto escapado (LLM05)

No depende de ninguna API: recibe la cadena que ya produjo el LLM. Todo es determinista.
"""

from __future__ import annotations

import html
from dataclasses import dataclass

# --- Constantes del dominio (NO las cambies) --------------------------------
MAX_CARACTERES = 4000
# Comparacion insensible a mayusculas: estos van en minusculas y comparas en minusculas.
PATRONES_PROHIBIDOS = ["[[system_prompt]]", "sk-live-"]


@dataclass
class Resultado:
    """Salida del gate.

    accion: "RENDER" (mostrar valor_seguro) | "BLOQUEAR" (no mostrar nada).
    motivo: cadena corta que explica la decision (util para logs/observabilidad).
    valor_seguro: el texto YA escapado para HTML cuando accion == "RENDER"; None si BLOQUEAR.
    """

    accion: str
    motivo: str
    valor_seguro: str | None = None


def manejar_salida(texto: str) -> Resultado:
    """Decide que hacer con la salida del LLM antes de renderizarla como HTML.

    Capa 1 (fuga):        si `texto` contiene algun PATRONES_PROHIBIDOS (comparando en
                          minusculas) -> Resultado("BLOQUEAR", motivo="fuga").
    Capa 2 (presupuesto): si len(texto) > MAX_CARACTERES -> Resultado("BLOQUEAR",
                          motivo="presupuesto").
    Capa 3 (sink HTML):   en otro caso -> Resultado("RENDER", motivo="ok",
                          valor_seguro=html.escape(texto)).

    Pista: html.escape convierte < > & " ' en entidades, dejando el HTML inerte. NO
    escribas tu propio escaper. El `<script>` peligroso se ESCAPA (sale como texto),
    no se bloquea; un secreto se BLOQUEA (no hay codificacion que lo vuelva mostrable).
    """
    raise NotImplementedError("Implementa el gate de salida de tres capas")
