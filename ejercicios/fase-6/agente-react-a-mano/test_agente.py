"""Tests del agent loop. Verifican la POLÍTICA del loop, no detalles internos.

Todo es determinista: el "modelo" es falso (guionizado) y no se llama a ninguna API.
"""

from agente import Bloque, Respuesta, ejecutar_agente, MAX_PASOS


class ModeloGuion:
    """Modelo falso: devuelve respuestas de un guion en orden.

    Guarda una copia de la lista de mensajes que ve en cada llamada, para poder
    inspeccionar qué le devolvió el agente (p. ej. el tool_result).
    """

    def __init__(self, guion):
        self.guion = list(guion)
        self.mensajes_vistos = []
        self.llamadas = 0

    def __call__(self, mensajes):
        self.mensajes_vistos.append(list(mensajes))  # copia superficial
        respuesta = self.guion[self.llamadas]
        self.llamadas += 1
        return respuesta


class ModeloTerco:
    """Siempre pide la misma tool; nunca termina. Para probar el techo de pasos."""

    def __init__(self):
        self.llamadas = 0

    def __call__(self, mensajes):
        self.llamadas += 1
        return Respuesta(
            "tool_use",
            [Bloque("tool_use", id=f"t{self.llamadas}", nombre="buscar_precio",
                    input={"producto": "bici"})],
        )


def _tool_results(mensajes):
    """Extrae los bloques tool_result del último mensaje de rol user, si los hay."""
    if not mensajes:
        return []
    ultimo = mensajes[-1]
    contenido = ultimo.get("contenido")
    if ultimo.get("rol") == "user" and isinstance(contenido, list):
        return [b for b in contenido if isinstance(b, dict) and b.get("tipo") == "tool_result"]
    return []


# --- Caso 1: respuesta directa, sin tools ----------------------------------
def test_respuesta_directa_sin_tools():
    modelo = ModeloGuion([Respuesta("end_turn", [Bloque("text", texto="Hola")])])
    r = ejecutar_agente("Hola", modelo)
    assert r.respuesta == "Hola"
    assert r.detenido_por == "end_turn"
    assert r.pasos == 1


# --- Caso 2: una tool y luego responde -------------------------------------
def test_una_tool_luego_responde():
    guion = [
        Respuesta("tool_use", [Bloque("tool_use", id="t1", nombre="buscar_precio",
                                       input={"producto": "bici"})]),
        Respuesta("end_turn", [Bloque("text", texto="La bici cuesta 200000")]),
    ]
    modelo = ModeloGuion(guion)
    r = ejecutar_agente("¿cuánto vale la bici?", modelo)
    assert r.respuesta == "La bici cuesta 200000"
    assert r.detenido_por == "end_turn"
    assert r.pasos == 2
    # El resultado de la tool se devolvió al modelo en la 2da llamada.
    results = _tool_results(modelo.mensajes_vistos[1])
    assert len(results) == 1
    assert results[0]["tool_use_id"] == "t1"
    assert results[0]["contenido"] == "200000"


# --- Caso 3: dos tools encadenadas (ReAct de verdad) -----------------------
def test_dos_tools_secuenciales():
    guion = [
        Respuesta("tool_use", [Bloque("tool_use", id="t1", nombre="buscar_precio",
                                       input={"producto": "bici"})]),
        Respuesta("tool_use", [Bloque("tool_use", id="t2", nombre="convertir_clp_a_usd",
                                       input={"monto_clp": 200000})]),
        Respuesta("end_turn", [Bloque("text", texto="Unos USD 210")]),
    ]
    modelo = ModeloGuion(guion)
    r = ejecutar_agente("¿cuánto vale la bici en USD?", modelo)
    assert r.respuesta == "Unos USD 210"
    assert r.pasos == 3
    # La segunda observación es la conversión (200000 / 950 = 210.53).
    results = _tool_results(modelo.mensajes_vistos[2])
    assert results[0]["tool_use_id"] == "t2"
    assert results[0]["contenido"] == "210.53"


# --- Caso 4: techo de pasos (modelo que nunca termina) ---------------------
def test_tope_de_pasos():
    modelo = ModeloTerco()
    r = ejecutar_agente("loop infinito", modelo)
    assert r.detenido_por == "tope_pasos"
    assert r.respuesta is None
    assert r.pasos == MAX_PASOS
    assert modelo.llamadas == MAX_PASOS  # ni una vuelta de más


# --- Caso 5: tool fuera de la allowlist NO se ejecuta ----------------------
def test_tool_no_permitida_no_se_ejecuta():
    guion = [
        Respuesta("tool_use", [Bloque("tool_use", id="t1", nombre="borrar_todo",
                                       input={})]),
        Respuesta("end_turn", [Bloque("text", texto="listo")]),
    ]
    modelo = ModeloGuion(guion)
    r = ejecutar_agente("borra todo", modelo)
    assert r.respuesta == "listo"
    # Se devolvió un tool_result de error, sin ejecutar la tool.
    results = _tool_results(modelo.mensajes_vistos[1])
    assert len(results) == 1
    assert results[0]["es_error"] is True
    assert results[0]["tool_use_id"] == "t1"
