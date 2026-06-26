---
ejercicio_id: fase-3/retry-backoff-jitter
fase: fase-3
sub_unidad: "3.14"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Reintentos con backoff exponencial + jitter (a mano)

## Implementación canónica (`solucion.py`)

```python
import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")


class ErrorTransitorio(Exception):
    ...


class ErrorPermanente(Exception):
    ...


def reintentar(
    fn: Callable[[], T],
    *,
    max_intentos: int = 5,
    base: float = 0.5,
    tope: float = 10.0,
    transitorias: tuple[type[Exception], ...] = (ErrorTransitorio,),
    dormir: Callable[[float], None] = time.sleep,
    aleatorio: Callable[[], float] = random.random,
) -> T:
    for intento in range(max_intentos):
        try:
            return fn()
        except transitorias:                       # solo lo transitorio entra aquí
            if intento + 1 >= max_intentos:         # era el último intento
                raise                               # relanza la transitoria original
            espera = aleatorio() * min(tope, base * (2 ** intento))   # full jitter
            dormir(espera)
    # inalcanzable: o devuelve, o relanza en el último intento
    raise AssertionError("max_intentos debe ser >= 1")
```

Verificado contra `test_acceptance.py`: pasa los 6 casos (éxito-1er-intento sin dormir; falla 2 y acierta; permanente sin reintentar; agota y relanza transitorio; backoff con tope `[2.0, 3.0, 3.0, 3.0]`; jitter `[0.0, 0.0]`).

## Por qué funciona

- **`except transitorias`** atrapa exclusivamente las excepciones de la tupla. Las permanentes (`ErrorPermanente`, `ValueError`, etc.) **no** entran al bloque: se propagan en el primer intento, sin dormir. Eso es lo que el test del error permanente verifica.
- **El chequeo `intento + 1 >= max_intentos` ANTES de dormir** evita la espera inútil tras el último intento, y `raise` (sin argumento) relanza la excepción original con su contexto.
- **`min(tope, base * 2**intento)`** es el backoff exponencial acotado: `intento=0 → base`, `1 → base*2`, `2 → base*4`… hasta `tope`.
- **`aleatorio() * delay`** es _full jitter_ (estilo AWS): la espera real es uniforme en `[0, delay)`. Con `random.random()` en producción desincroniza a los clientes. En los tests, `aleatorio` fijo (1.0 o 0.0) vuelve la espera determinista.

## El recorrido de razonamiento esperado (bitácora)
1. La red falla de forma transitoria (parpadeos); reintentar absorbe esos fallos breves.
2. Reintentar de inmediato y en bucle machaca a una dependencia que ya sufre → backoff.
3. Backoff puro sincroniza a todos los clientes que cayeron juntos → **retry storm**; el jitter los dispersa.
4. Los 4xx (400/401/422) son del request, no de la red: reintentarlos no los arregla y quema recursos.
5. Reintentar un POST con efectos solo es seguro si es idempotente (enlace con el ejercicio de idempotencia).

## Puntos resbalosos (donde el corrector debe mirar)
1. **Off-by-one en intentos vs reintentos.** `max_intentos=4` = 1 original + 3 reintentos = 3 esperas. El test lo fija (`len(esperas) == 3`).
2. **Dormir tras el último intento.** Si calcula y duerme antes de comprobar que era el último, hace una espera de más. El test del backoff con tope cuenta exactamente las esperas.
3. **Atrapar de más.** `except Exception` reintentaría también los permanentes; el test del error permanente (`llamadas == 1`) lo caza.
4. **Relanzar genérico.** `raise RuntimeError("agotado")` en vez de `raise` pierde el error real; aceptable solo si conserva la causa (`from exc`), pero el enunciado pide relanzar la transitoria.

## Rango de soluciones aceptables
- **Acumular `intento` en un `while`** con contador manual — equivalente al `for range`.
- **Jitter "equal" o "decorrelated"** en vez de full jitter — válido conceptualmente, pero rompe los tests deterministas que asumen full jitter; si el alumno cambió la fórmula, debe haber ajustado los tests y justificado en `bitacora.md` (márcalo competente si el razonamiento es correcto).
- **Capturar el último `exc` en una variable y relanzarlo explícitamente** (`raise exc`) — equivalente a `raise` desnudo dentro del `except`.
- ❌ **No aceptable como competente:** `except Exception` que reintenta todo; backoff sin tope o sin jitter; dormir después del último intento; usar `tenacity` (el enunciado pide hacerlo a mano).
