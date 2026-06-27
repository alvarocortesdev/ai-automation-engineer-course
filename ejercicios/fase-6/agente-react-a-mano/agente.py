"""El agent loop ReAct, a mano.

El "modelo" se INYECTA como el parámetro `llamar_modelo` para que el loop sea
testeable sin API ni API key: en los tests se pasa un modelo falso guionizado.
Es el mismo loop del worked example de la lección, con `client.messages.create(...)`
reemplazado por `llamar_modelo(mensajes)`.

Contrato del modelo inyectado:
    llamar_modelo(mensajes: list[dict]) -> Respuesta
donde `Respuesta` trae:
    .stop_reason: "tool_use" | "end_turn"
    .content:     list[Bloque]
y cada `Bloque` es:
    tipo == "text"      -> usa .texto
    tipo == "tool_use"  -> usa .id, .nombre, .input

Formato de la lista de mensajes (la "memoria de corto plazo"):
    {"rol": "user" | "assistant", "contenido": <str | list[Bloque] | list[dict]>}
El turno del modelo se guarda como {"rol": "assistant", "contenido": resp.content}.
Las observaciones se devuelven como {"rol": "user", "contenido": [<tool_result dict>]},
donde cada tool_result dict es:
    {"tipo": "tool_result", "tool_use_id": <id>, "contenido": <str>, "es_error": <bool>}
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Bloque:
    tipo: str                                  # "text" | "tool_use"
    texto: str = ""
    id: str = ""
    nombre: str = ""
    input: dict = field(default_factory=dict)


@dataclass
class Respuesta:
    stop_reason: str                           # "tool_use" | "end_turn"
    content: list                              # list[Bloque]


@dataclass
class ResultadoAgente:
    respuesta: str | None                      # texto final, o None si se cortó por tope
    pasos: int                                 # vueltas que dio el loop
    detenido_por: str                          # "end_turn" | "tope_pasos"


# --- Constantes del dominio (NO las cambies) --------------------------------
MAX_PASOS = 5
TASA_USD = 950  # CLP por dólar
PRECIOS_CLP = {"bici": 200_000, "casco": 25_000, "luz": 8_000}


def buscar_precio(producto: str) -> int:
    return PRECIOS_CLP[producto]


def convertir_clp_a_usd(monto_clp: int) -> float:
    return round(monto_clp / TASA_USD, 2)


# Allowlist = exactamente las herramientas definidas (least privilege).
REGISTRO = {"buscar_precio": buscar_precio, "convertir_clp_a_usd": convertir_clp_a_usd}
HERRAMIENTAS_PERMITIDAS = set(REGISTRO)


def invocar(nombre: str, args: dict):
    """Ejecuta una herramienta del registro. Asume que `nombre` ya pasó el gate."""
    return REGISTRO[nombre](**args)


def ejecutar_agente(pregunta: str, llamar_modelo) -> ResultadoAgente:
    """Corre el agent loop ReAct hasta que el modelo termina o se alcanza MAX_PASOS.

    En cada vuelta, EN ESTE ORDEN:
      1. RAZONAR:  resp = llamar_modelo(mensajes)
      2. OBSERVAR: guarda el turno del modelo en `mensajes`
                   ({"rol": "assistant", "contenido": resp.content}), SIEMPRE.
      3. ¿TERMINÓ?: si resp.stop_reason != "tool_use", devuelve el texto del primer
                   bloque tipo "text" (detenido_por="end_turn").
      4. GATE + ACTUAR: por cada bloque tool_use:
           - si nombre NO está en HERRAMIENTAS_PERMITIDAS -> tool_result con
             es_error=True y contenido "herramienta no permitida" (NO la ejecutes);
           - si está permitido -> ejecútalo con invocar(...) y devuelve su salida.
      5. Añade {"rol": "user", "contenido": [<tool_result dicts>]} y repite.
    Si el loop se agota sin un "end_turn": respuesta=None, detenido_por="tope_pasos".
    """
    raise NotImplementedError("Implementa el agent loop ReAct")
