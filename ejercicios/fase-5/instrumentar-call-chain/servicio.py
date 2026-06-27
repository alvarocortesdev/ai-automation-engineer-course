"""Servicio SIN instrumentar — tu trabajo es añadirle observabilidad.

Tres funciones forman un call-chain (responder -> buscar_contexto + generar_respuesta).
Ya devuelven el resultado correcto; NO cambies su lógica ni sus valores: solo instrumenta.

Lee el README.md para la spec exacta de nombres de span y atributos, y abre
test_observabilidad.py: ese test ES tu contrato.

Pistas de API (todas verificadas, no inventes nada):
  - tracer = trace.get_tracer("api-despensa")
  - with tracer.start_as_current_span("nombre") as span: ...
  - span.set_attribute("clave", valor)
  - structlog.contextvars.bind_contextvars(correlation_id=...)
  - log = structlog.get_logger(); log.info("evento", campo=valor)
"""

from __future__ import annotations

# TODO (1): importa lo necesario y crea el tracer y el logger a nivel de módulo.
# from opentelemetry import trace
# import structlog
# tracer = trace.get_tracer("api-despensa")
# log = structlog.get_logger()


def responder(pregunta: str, correlation_id: str) -> dict:
    # TODO (1): abre el span raíz "responder".
    # TODO (2): ata el correlation_id al contexto (bind_contextvars) y ponlo como atributo del span.
    # TODO (4): loguea un evento de inicio (p. ej. "inicio_consulta").
    contexto = buscar_contexto(pregunta)
    respuesta = generar_respuesta(pregunta, contexto)
    # TODO (4): loguea un evento de fin (p. ej. "fin_consulta").
    return {"respuesta": respuesta}


def buscar_contexto(pregunta: str) -> str:
    # TODO (1): abre el span hijo "buscar_contexto".
    filas = 3  # simula una consulta a Postgres que devuelve 3 filas
    # TODO (opcional): atributos útiles, p. ej. db.system="postgresql", db.filas_devueltas=filas
    return f"contexto con {filas} filas relevantes"


def generar_respuesta(pregunta: str, contexto: str) -> str:
    # TODO (1): abre el span hijo "generar_respuesta".
    tokens_in, tokens_out = 1200, 340  # simula el uso de tokens del LLM
    costo = round(tokens_in * 3e-6 + tokens_out * 1.5e-5, 6)  # USD aproximado
    # TODO (3): pon como atributos del span:
    #   gen_ai.usage.input_tokens  = tokens_in   (int)
    #   gen_ai.usage.output_tokens = tokens_out  (int)
    #   gen_ai.usage.cost_usd      = costo        (float)
    return "respuesta generada por el LLM"


if __name__ == "__main__":
    # Demo local: configura la telemetría y ejecuta UNA consulta para VER
    # los logs JSON (stdout) y los spans (impresos al cerrarse).
    import uuid

    from telemetria import configurar_logs, configurar_trazas

    configurar_logs()
    configurar_trazas()
    print(responder("¿queda leche en la despensa?", uuid.uuid4().hex))
