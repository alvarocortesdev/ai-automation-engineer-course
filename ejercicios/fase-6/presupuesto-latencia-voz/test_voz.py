"""Tests del cerebro de un voice agent: latencia percibida + barge-in.

Los datos se inyectan: los tests no dependen de audio, API ni servicio real.
Verifican la LÓGICA de decisión (qué suma para el primer audio, la tabla de
verdad del barge-in, y la combinación de ambas).

Ejecuta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

import pytest

from voz import latencia_percibida, decidir_barge_in, evaluar_turno

# Un stack típico bien optimizado: cumple-no-cumple según el target.
ETAPAS = {
    "vad_endpoint": 120,
    "stt": 80,
    "llm_ttft": 180,
    "tts_primer_audio": 90,
    "red": 40,
    "llm_total": 900,     # NO debe contar
    "tts_total": 1500,    # NO debe contar
}


# ----- latencia_percibida -----

def test_latencia_suma_solo_las_etapas_percibidas():
    # 120 + 80 + 180 + 90 + 40 = 510 (ignora llm_total y tts_total)
    assert latencia_percibida(ETAPAS) == 510


def test_latencia_ignora_total_de_generacion():
    # Sin las etapas de "total", el resultado no cambia: ya las ignorábamos.
    sin_totales = {k: v for k, v in ETAPAS.items() if not k.endswith("_total")}
    assert latencia_percibida(sin_totales) == latencia_percibida(ETAPAS)


def test_latencia_ignora_claves_desconocidas():
    etapas = {"vad_endpoint": 100, "stt": 50, "ruido_misterioso": 9999}
    assert latencia_percibida(etapas) == 150


def test_latencia_etapa_ausente_cuenta_como_cero():
    # Solo dos etapas presentes; las demás valen 0, no revientan.
    assert latencia_percibida({"llm_ttft": 150, "red": 30}) == 180


def test_latencia_dict_vacio():
    assert latencia_percibida({}) == 0


# ----- decidir_barge_in (tabla de verdad) -----

def test_barge_in_interrumpir():
    assert decidir_barge_in(agente_hablando=True, voz_usuario_detectada=True) == "interrumpir"


def test_barge_in_seguir_hablando():
    assert decidir_barge_in(agente_hablando=True, voz_usuario_detectada=False) == "seguir_hablando"


def test_barge_in_escuchar():
    assert decidir_barge_in(agente_hablando=False, voz_usuario_detectada=True) == "escuchar"


def test_barge_in_esperar():
    assert decidir_barge_in(agente_hablando=False, voz_usuario_detectada=False) == "esperar"


# ----- evaluar_turno (combina las dos) -----

def test_evaluar_no_cumple_sub_250_pero_calcula_bien():
    r = evaluar_turno(ETAPAS, agente_hablando=True, voz_usuario_detectada=True)
    assert r["latencia_ms"] == 510
    assert r["cumple"] is False          # 510 > 250
    assert r["accion"] == "interrumpir"  # ambos hablan


def test_evaluar_cumple_con_target_realista():
    # Mismo stack, pero con un target turn-based realista (800 ms).
    r = evaluar_turno(ETAPAS, agente_hablando=False, voz_usuario_detectada=False, target_ms=800)
    assert r["cumple"] is True
    assert r["accion"] == "esperar"


def test_evaluar_en_el_target_cumple():
    # latencia exactamente igual al target -> cumple (la regla es <=).
    etapas = {"vad_endpoint": 100, "stt": 100, "red": 50}  # 250
    r = evaluar_turno(etapas, agente_hablando=False, voz_usuario_detectada=True, target_ms=250)
    assert r["latencia_ms"] == 250
    assert r["cumple"] is True
    assert r["accion"] == "escuchar"


# TODO(estudiante): añade aquí al menos un caso borde tuyo.
# Idea: un stack S2S de una sola etapa que SÍ cumple el sub-250.
