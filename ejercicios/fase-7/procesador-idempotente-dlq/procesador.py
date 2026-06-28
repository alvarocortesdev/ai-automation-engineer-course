"""Procesador idempotente con dead-letter queue — Primero-Sin-IA.

Implementa `ProcesadorIdempotente` a mano, sin IA. NO cambies la firma de los
métodos ni las claves de los dicts que devuelves: `test_procesador.py` depende de
ellas.

Idea: un canal de mensajes entrega "at-least-once" (te puede llegar el mismo
evento varias veces) y algunos mensajes son "venenosos" (fallan siempre). Este
procesador vuelve seguro ese canal: deduplica por el id del evento (idempotencia)
y aparta los venenosos en una DLQ tras N intentos, en vez de reintentarlos para
siempre.

──────────────────────────────────────────────────────────────────────────────
CONTRATO

    ProcesadorIdempotente(max_intentos=3)
        .procesar(evento: dict, efecto) -> dict
        .dlq -> list           # eventos que terminaron en la dead-letter queue

`evento`: dict con al menos la clave "id" (str), la idempotency key.
`efecto`: callable efecto(evento) -> Any. Es el side-effect real (cobrar, llamar
          una API, etc.). Puede tener ÉXITO (devuelve algo) o FALLAR (lanza una
          excepción). Lo controlas tú en los tests.

Reglas de `procesar`:
    1. Si el id del evento YA se procesó con ÉXITO antes:
         -> NO llames a `efecto`.
         -> devuelve {"status": "duplicado", "resultado": <el resultado guardado>}
    2. Si el evento es nuevo (o falló antes pero no agotó intentos):
         - llama a `efecto(evento)` UNA vez.
         - si tiene ÉXITO: guarda el resultado y devuelve
               {"status": "procesado", "resultado": <lo que devolvió efecto>}
         - si LANZA excepción: cuenta el intento.
               - si intentos < max_intentos:
                     -> devuelve {"status": "reintentable"}
               - si intentos >= max_intentos:
                     -> mueve el evento a la DLQ (self.dlq)
                     -> devuelve {"status": "dlq"}
    3. Si el id ya está en la DLQ: devuelve {"status": "dlq"} sin llamar a `efecto`.

Sutileza clave (el corazón del ejercicio):
    Un evento se marca como "completado" SOLO en la rama de éxito. Por eso un
    evento que falla una vez (reintentable) y luego se reintenta con éxito SÍ se
    procesa de verdad: el fallo previo no lo convierte en "duplicado".
"""


class ProcesadorIdempotente:
    def __init__(self, max_intentos: int = 3) -> None:
        self.max_intentos = max_intentos
        # Pistas de implementación (puedes cambiarlas):
        #   self._completados: dict[str, Any]  -> id -> resultado (solo ÉXITOS)
        #   self._intentos: dict[str, int]     -> id -> nº de fallos acumulados
        #   self.dlq: list                     -> eventos venenosos apartados
        raise NotImplementedError("Implementa esta clase a mano, sin IA.")

    def procesar(self, evento: dict, efecto) -> dict:
        """Procesa un evento de forma idempotente. Ver el contrato completo arriba."""
        raise NotImplementedError("Implementa este método a mano, sin IA.")
