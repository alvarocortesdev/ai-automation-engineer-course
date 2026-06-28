---
ejercicio_id: fase-7/procesador-idempotente-dlq
fase: fase-7
sub_unidad: "7.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Procesador idempotente con dead-letter queue

## Respuesta canónica

```python
class ProcesadorIdempotente:
    def __init__(self, max_intentos=3):
        self.max_intentos = max_intentos
        self._completados = {}   # id -> resultado (SOLO éxitos)
        self._intentos = {}      # id -> nº de fallos acumulados
        self._en_dlq = set()     # ids ya enviados a la DLQ
        self.dlq = []            # eventos venenosos apartados

    def procesar(self, evento, efecto):
        key = evento["id"]

        if key in self._completados:                 # ya se hizo con éxito
            return {"status": "duplicado", "resultado": self._completados[key]}

        if key in self._en_dlq:                      # ya descartado
            return {"status": "dlq"}

        try:
            resultado = efecto(evento)               # el side-effect, UNA vez
        except Exception:
            self._intentos[key] = self._intentos.get(key, 0) + 1
            if self._intentos[key] >= self.max_intentos:
                self._en_dlq.add(key)
                self.dlq.append(evento)
                return {"status": "dlq"}
            return {"status": "reintentable"}

        self._completados[key] = resultado           # marca completado SOLO en éxito
        return {"status": "procesado", "resultado": resultado}
```

## Razonamiento paso a paso

1. **Tres estructuras separadas.** `_completados` (éxitos, con su resultado), `_intentos` (contador de fallos por id) y `_en_dlq` (ids terminales). Mezclarlas es la fuente de los bugs.
2. **Dedup primero.** Si el id está en `_completados`, se devuelve el resultado guardado sin tocar `efecto`. Esto vuelve effectively-once un canal at-least-once.
3. **DLQ terminal.** Si el id ya está en la DLQ, se devuelve `dlq` sin re-ejecutar. Evita que un poison message vuelva a correr el efecto.
4. **Una sola llamada a `efecto`** por invocación, dentro de `try`.
5. **Marca completado SOLO en éxito.** Es la sutileza central: el fallo incrementa `_intentos` pero no marca completado, así un reintento posterior con éxito sí procesa (no se confunde con duplicado).
6. **Umbral `>=`.** Al llegar a `max_intentos` fallos, el evento va a la DLQ.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Marcar completado en el `try` antes del éxito real** (o en un `finally`): rompe `test_falla_y_luego_exito_no_es_duplicado`. El marcado debe ocurrir **después** de que `efecto` retorne sin excepción.
2. **Contar intentos de ids distintos juntos** (un solo contador global en vez de por id): un poison message mandaría a la DLQ eventos sanos. El contador es por `key`.
3. **DLQ no terminal:** si tras DLQ vuelve a llamar a `efecto`, duplica el side-effect del fallo. `test_evento_en_dlq_no_reejecuta_el_efecto` lo caza.
4. **`> max_intentos` en vez de `>=`:** con `max_intentos=3`, mandaría a DLQ al 4º intento, no al 3º. El test espera `>=`.

## Rango de soluciones aceptables

- Usar un solo dict `{id: {"resultado": ..., "intentos": n, "estado": ...}}` en vez de tres estructuras es válido si la lógica equivale.
- Usar una excepción concreta en lugar de `except Exception` es aceptable, siempre que capture lo que el efecto lanza en los tests (`ValueError`, `ConnectionError`).
- Implementar la dedup con un `set` de ids completados + un dict aparte para resultados es válido.
- En producción, este estado vive en una DB con `UNIQUE` sobre la idempotency key (no en memoria) y la operación es atómica (`INSERT ... ON CONFLICT`). Mencionarlo en el write-up es señal de `excelente`, no un requisito del código.

## Vara para el `write-up.md`

- **(a)** Aceptable: "un fallo no significa que el efecto haya ocurrido; marcar completado en un fallo descartaría el reintento legítimo, perdiendo el evento". Excelente si nombra que la idempotency key marca *resultado de negocio logrado*, no *intento hecho*.
- **(b)** Aceptable: dual-write = actualizar DB y publicar evento por separado pueden divergir si hay crash entre ambos; outbox = escribir el evento en la misma transacción que el cambio de negocio, y un relay lo publica después (at-least-once → consumidores idempotentes). Incompleto si omite la idea de **misma transacción**.
- **(c)** Aceptable: la entrega en vivo (webhooks/eventos) puede perder mensajes; la reconciliación compara el estado de los dos sistemas periódicamente y repara la diferencia, garantizando corrección eventual que el tiempo real no asegura. Excelente: "tiempo real para la velocidad, reconciliación para la verdad".
