"""El cerebro de un voice agent: latencia percibida + barge-in.

Completa las TRES funciones. Las latencias medidas y el estado se INYECTAN como
datos: así pruebas la LÓGICA de decisión sin audio, sin API y sin API key.

Una conversación de voz tiene un presupuesto de tiempo brutal. La "latencia
percibida" es el time-to-first-audio: desde que el usuario DEJA de hablar hasta
que escucha la PRIMERA sílaba de la respuesta. Gracias al streaming, el LLM sigue
generando y el TTS sigue sintetizando MIENTRAS el agente ya habla -> por eso el
total de generación NO cuenta para el primer audio.

Forma de un dict de `etapas` (todas las latencias en ms):
    {
        "vad_endpoint": 120,        # detectar que el usuario terminó (silencio)  -> CUENTA
        "stt": 80,                  # transcribir lo último                       -> CUENTA
        "llm_ttft": 180,            # tiempo hasta el PRIMER token del LLM         -> CUENTA
        "tts_primer_audio": 90,     # tiempo hasta el PRIMER byte de voz           -> CUENTA
        "red": 40,                  # round-trip de red                           -> CUENTA
        "llm_total": 900,           # generar TODA la respuesta                   -> NO cuenta
        "tts_total": 1500,          # sintetizar TODO el audio                    -> NO cuenta
    }
"""
from __future__ import annotations

# Etapas que contribuyen al time-to-first-audio (latencia percibida).
# Cualquier otra clave del dict (llm_total, tts_total, claves desconocidas) se IGNORA.
ETAPAS_PERCIBIDAS = ("vad_endpoint", "stt", "llm_ttft", "tts_primer_audio", "red")


def latencia_percibida(etapas: dict) -> float:
    """Suma SOLO las etapas que cuentan para el primer audio.

    - Suma los valores de las claves de ETAPAS_PERCIBIDAS que estén presentes.
    - Una etapa ausente cuenta como 0 (no revienta).
    - Ignora cualquier clave que NO esté en ETAPAS_PERCIBIDAS (p. ej. llm_total,
      tts_total, o claves desconocidas).
    """
    raise NotImplementedError("implementa latencia_percibida")


def decidir_barge_in(agente_hablando: bool, voz_usuario_detectada: bool) -> str:
    """Tabla de verdad del manejo de turnos. Devuelve uno de cuatro estados:

    - "interrumpir"      : el agente habla Y el usuario habla encima (barge-in).
    - "seguir_hablando"  : el agente habla y el usuario NO habla.
    - "escuchar"         : el agente NO habla y el usuario habla (turno normal del usuario).
    - "esperar"          : nadie habla (silencio).
    """
    raise NotImplementedError("implementa decidir_barge_in")


def evaluar_turno(
    etapas: dict,
    agente_hablando: bool,
    voz_usuario_detectada: bool,
    target_ms: float = 250.0,
) -> dict:
    """Evaluación combinada de un turno. Devuelve:

        {"latencia_ms": float, "cumple": bool, "accion": str}

    - "latencia_ms": resultado de latencia_percibida(etapas).
    - "cumple": True si latencia_ms <= target_ms (la regla es <= target).
    - "accion": resultado de decidir_barge_in(...).

    DEBE reusar latencia_percibida y decidir_barge_in (no reimplementes su lógica).
    """
    raise NotImplementedError("implementa evaluar_turno")


if __name__ == "__main__":
    # Prueba rápida manual (Predict-Run): ¿qué crees que imprime ANTES de correrlo?
    demo = {
        "vad_endpoint": 120, "stt": 80, "llm_ttft": 180,
        "tts_primer_audio": 90, "red": 40, "llm_total": 900, "tts_total": 1500,
    }
    print(evaluar_turno(demo, agente_hablando=True, voz_usuario_detectada=True))
