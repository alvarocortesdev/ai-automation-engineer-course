---
ejercicio_id: fase-8/rate-limiter-token-bucket
fase: fase-8
sub_unidad: "8.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Rate limiter token bucket

## Implementación de referencia

```python
from __future__ import annotations


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float, ahora: float) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity            # arranca lleno
        self.ultima_recarga = ahora       # marca de tiempo de la última recarga

    def _recargar(self, ahora: float) -> None:
        transcurrido = ahora - self.ultima_recarga
        if transcurrido > 0:              # el reloj no retrocede ni recarga si no avanza
            self.tokens = min(
                self.capacity,
                self.tokens + transcurrido * self.refill_rate,
            )
            self.ultima_recarga = ahora

    def allow(self, ahora: float, cost: float = 1.0) -> bool:
        self._recargar(ahora)             # 1) recargar PRIMERO
        if self.tokens >= cost:           # 2) decidir después
            self.tokens -= cost
            return True
        return False
```

Verificado: pasa los 6 tests del contrato (`pytest -q` → `6 passed`).

## Las tres ideas que el alumno debe demostrar

1. **Recargar antes de decidir.** Si decides con los tokens viejos y recargas después, rechazas
   requests que ya deberían tener tokens (los repuestos por el tiempo transcurrido). El orden es parte
   del algoritmo, no un detalle.
2. **El `min(capacity, ...)` es lo que hace que sea un *limiter*.** Sin el tope, tras un rato de
   inactividad el bucket acumularía tokens infinitos y dejaría pasar una ráfaga ilimitada. El tope es
   lo que acota la ráfaga máxima a `capacity`.
3. **Reloj inyectado = testeable.** El tiempo entra por el parámetro `ahora`; la clase no llama a
   ningún reloj. Por eso los tests son deterministas y corren en milisegundos sin `sleep`. Es el mismo
   principio que el determinismo de los workflows de Temporal (7.3) y la inyección de dependencias de
   los test doubles (2.8): la dependencia del entorno se pasa como argumento para poder controlarla.

## Variantes aceptables

- Inicializar el bucket **vacío** en vez de lleno **solo si** el alumno lo justifica y ajusta sus
  tests propios; el contrato dado asume que arranca lleno (`test_bucket_arranca_lleno_y_se_agota`).
- Un método único `allow` sin `_recargar` separado es aceptable; separar es más limpio (excelente).
- Usar `float('inf')` para `transcurrido <= 0` no aplica aquí; basta el `if transcurrido > 0`.

## Errores que el corrector debe cazar

- **Fixed-window counter** disfrazado de token bucket (cuenta requests por minuto): no permite ráfagas
  y sufre el problema del borde de ventana. No cumple el objetivo.
- Falta el `min` → `test_tokens_no_superan_la_capacidad` en rojo.
- Decide antes de recargar → `test_recarga_por_tiempo_transcurrido` en rojo.
- Consume tokens aunque `cost` no alcance → `test_parametro_cost` en rojo (el 4º request debería
  fallar con el bucket ya vacío, pero un bug de "restar igual" lo desordena).
- Lee `time.monotonic()` dentro de la clase → C2 cae a incompleto aunque los tests del contrato pasen
  (los tests propios del alumno necesitarían `sleep`).

## Test propio esperado (ejemplo de "excelente")

```python
def test_cost_mayor_que_capacidad_nunca_pasa():
    b = TokenBucket(capacity=3, refill_rate=1.0, ahora=0.0)
    # bucket lleno, pero el costo excede la capacidad total: imposible de conceder
    assert b.allow(0.0, cost=5) is False
    assert b.allow(1000.0, cost=5) is False  # ni esperando una eternidad
```

Este test **mata mutantes**: si alguien quitara la comparación `tokens >= cost` o el `min`, fallaría.
Eso es lo que se busca, no perseguir coverage% (ver 2.9).

## Nota de system design (para el feedback de C4)

Un detalle que separa al que entendió la lección: **un token bucket por proceso no basta tras un load
balancer.** Si tienes N servidores stateless, cada uno con su propio bucket en memoria, un cliente
puede hacer N veces el límite (uno por servidor). En producción el estado del rate limiter vive en un
almacén **compartido** (Redis), no en la RAM de cada instancia —exactamente por la misma razón que las
sesiones no pueden vivir en memoria local cuando escalas horizontal.
