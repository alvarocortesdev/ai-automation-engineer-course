"""Plano de control de un agente que ejecuta acciones — Primero-Sin-IA.

Implementa `decidir` a mano, sin IA. NO cambies la firma ni las claves de los
dicts que devuelves: `test_plano_control.py` depende de ellas.

──────────────────────────────────────────────────────────────────────────────
EL REPARTO

El "cerebro" (un LLM) ya hizo su trabajo: leyó el ticket/documento, lo clasificó
y extrajo campos, y te entrega una PROPUESTA. El cerebro NUNCA ejecuta: solo
propone. Este plano de control es el "código que dispone": recibe la propuesta y
decide la RUTA. Es determinista, aburrido y testeable sin red — ese aburrimiento
es la propiedad de seguridad.

──────────────────────────────────────────────────────────────────────────────
CONTRATO

    decidir(propuesta, accion, costo_acumulado_usd, ids_procesados,
            *, techo_costo_usd=0.50) -> dict

`propuesta`: dict con al menos
    "input_id" (str)   -> idempotency key del input (p. ej. message_id del webhook)
    "valido"   (bool)  -> ¿la salida del LLM pasó la validación de schema + reglas?
    "confianza"(float) -> confianza AUTO-REPORTADA por el modelo (0..1). OJO: no es
                          una probabilidad calibrada. Es UNA señal, no la verdad.
`accion`: dict con
    "sensible"         (bool)  -> ¿es una acción sensible/irreversible? (reembolso
                                  grande, borrar datos, enviar a un externo)
    "umbral_confianza" (float) -> umbral de confianza para esta acción (0..1)
`costo_acumulado_usd`: float  -> costo gastado hasta ahora en este run/tenant
`ids_procesados`: set[str]    -> input_ids sobre los que YA se actuó (idempotencia)
`techo_costo_usd`: float      -> circuit-breaker de costo (kwarg-only)

Devuelve: {"ruta": <str>, "motivo": <str>} con
    ruta in {"AUTO", "HITL", "RECHAZO", "DUPLICADO"}

──────────────────────────────────────────────────────────────────────────────
ORDEN DE LOS CHEQUEOS (el orden ES el diseño de seguridad)

    1. Idempotencia:  input_id en ids_procesados        -> DUPLICADO
    2. Guardrail I/O: not propuesta["valido"]           -> RECHAZO   (OWASP LLM05)
    3. Techo de costo: costo_acumulado_usd > techo      -> RECHAZO   (circuit-breaker)
    4. Acción sensible: accion["sensible"]              -> HITL      (OWASP LLM06)
                        (SIEMPRE, sin importar la confianza)
    5. Confianza:  confianza < accion["umbral_confianza"] -> HITL
                   en otro caso                           -> AUTO

Cada chequeo retorna temprano: la PRIMERA barrera que aplica decide la ruta.
Un duplicado con schema inválido devuelve DUPLICADO (no RECHAZO): idempotencia
va primero. Una acción sensible con confianza 0.99 devuelve HITL (no AUTO):
sensible siempre va a humano.
"""


def decidir(
    propuesta: dict,
    accion: dict,
    costo_acumulado_usd: float,
    ids_procesados: set,
    *,
    techo_costo_usd: float = 0.50,
) -> dict:
    """Decide la ruta de una propuesta del agente. Ver el contrato completo arriba."""
    raise NotImplementedError("Implementa esta función a mano, sin IA.")
