---
ejercicio_id: fase-6/reintentos-backoff
fase: fase-6
sub_unidad: "6.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para
> detectar el error y graduar las pistas.

# Solución de referencia — Reintentos con backoff exponencial + jitter

## Respuesta canónica (implementación)

```python
from __future__ import annotations
from typing import Callable


class ErrorReintentable(Exception):
    def __init__(self, mensaje: str = "", retry_after: float | None = None):
        super().__init__(mensaje)
        self.retry_after = retry_after


def reintentar_con_backoff(
    operacion,
    *,
    max_intentos: int = 5,
    base: float = 1.0,
    tope: float = 60.0,
    dormir: Callable[[float], None],
    aleatorio: Callable[[float], float],
):
    if max_intentos < 1:
        raise ValueError("max_intentos debe ser >= 1")
    ultima = None
    for i in range(max_intentos):
        try:
            return operacion()
        except ErrorReintentable as e:           # solo el transitorio se reintenta
            ultima = e
            if i == max_intentos - 1:            # último intento: no duermas, re-lanza
                break
            if e.retry_after is not None:        # el servidor manda: gana sobre el backoff
                espera = e.retry_after
            else:
                base_i = min(tope, base * 2 ** i)  # backoff exponencial con tope
                espera = base_i + aleatorio(base_i)  # + jitter (solo sobre el backoff)
            dormir(espera)
        # cualquier OTRA excepción NO se captura aquí -> se propaga de inmediato
    raise ultima
```

## Razonamiento paso a paso

1. **Capturar solo `ErrorReintentable`.** Cualquier otra excepción (un `ValueError` que
   simula un `400`, etc.) no entra al `except` y se propaga al instante: sin dormir, sin
   reintentar. Reintentar un request inválido manda el mismo error.
2. **El último intento no duerme.** Con `max_intentos` intentos hay como máximo
   `max_intentos − 1` esperas. Al llegar al último índice (`i == max_intentos - 1`) se
   rompe el bucle y se re-lanza — dormir ahí sería una espera inútil antes de rendirse.
3. **Retry-After gana.** Si el error trae `retry_after`, esa espera **exacta** se usa:
   sin jitter y sin tope. El servidor sabe mejor que tú cuándo aceptará el próximo
   request.
4. **Backoff exponencial con tope.** Sin Retry-After, la espera base del intento `i` es
   `min(tope, base · 2^i)`: 1, 2, 4, 8... topado. El tope evita esperas absurdas.
5. **Jitter solo sobre el backoff.** `aleatorio(base_i)` devuelve el componente aleatorio
   a sumar. Inyectado, hace los tests deterministas; en producción sería
   `lambda b: random.uniform(0, b)`. Desincroniza los reintentos de muchos clientes
   (rompe el thundering herd).
6. **Re-lanzar la última.** Si se agotan los intentos, el caller debe enterarse: se
   re-lanza la última `ErrorReintentable`, no se devuelve `None`.

### Traza del caso del README (max_intentos=6, base=1, tope=8, jitter=0, siempre falla)
- i=0 → min(8, 1·1)=1 → dormir(1)
- i=1 → min(8, 1·2)=2 → dormir(2)
- i=2 → min(8, 1·4)=4 → dormir(4)
- i=3 → min(8, 1·8)=8 → dormir(8)
- i=4 → min(8, 1·16)=**8** (topado, por eso no es 16) → dormir(8)
- i=5 → último intento → **no duerme**, re-lanza.
- esperas = **[1, 2, 4, 8, 8]**.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Dormir tras el último intento**: produce `[1,2,4,8,8,16→8]` (6 esperas en vez de 5)
   y un re-lanzamiento tardío. `test_backoff_exponencial_respeta_tope` espera 5 esperas.
2. **Off-by-one en el exponente** (`2^(i+1)` o empezar en `i=1`): primera espera 2, no 1.
   Lo atrapa `test_exito_al_tercer_intento` (espera `[1.0, 2.0]`).
3. **Jitter encima del Retry-After**: `test_retry_after_gana_sobre_el_backoff` inyecta un
   jitter de 999 y espera exactamente `[7.5]`; si el jitter se suma, falla.
4. **`except Exception`** en vez de `except ErrorReintentable`: reintenta el `ValueError`
   del `400`. Lo atrapa `test_error_no_reintentable_se_propaga_de_inmediato` (espera
   `esperas == []`).
5. **No re-lanzar al agotar**: devolver `None` en silencio. `test_agota_intentos_relanza_ultima`
   espera que se lance `ErrorReintentable`.
6. **`time.sleep`/`random` reales** en vez de los inyectados: el test no puede medir las
   esperas y queda atado al reloj.

## Rango de soluciones aceptables

- Usar un `while` con contador en vez de `for i in range(...)` es válido si produce las
  mismas esperas y respeta los mismos cortes.
- Calcular el exponente como `base * (2 ** i)` o como `base * 2 ** i` es lo mismo.
- Acumular `ultima` y re-lanzar al final, o re-lanzar dentro del bucle en el último
  intento (`if i == max_intentos - 1: raise`), ambas válidas.
- Validar `max_intentos < 1` no lo exige ningún test; está bien tenerlo o no.
- **Profundización opcional (excelente, no requerida):** un **circuit breaker** (dejar de
  reintentar si el servicio lleva mucho fallando) o métricas por intento (loguear cada
  espera y el motivo) — anticipo de observabilidad (5.10) y LLMOps (6.16). No penalizar a
  quien hace solo el backoff pedido.
