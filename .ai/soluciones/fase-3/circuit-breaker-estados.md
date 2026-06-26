---
ejercicio_id: fase-3/circuit-breaker-estados
fase: fase-3
sub_unidad: "3.14"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Circuit breaker: la máquina de estados (a mano)

## Implementación canónica (`solucion.py`)

```python
import time
from typing import Callable, TypeVar

T = TypeVar("T")


class CircuitoAbierto(Exception):
    ...


class CircuitBreaker:
    def __init__(
        self,
        *,
        umbral_fallos: int = 3,
        espera_apertura: float = 30.0,
        reloj: Callable[[], float] = time.monotonic,
    ) -> None:
        self._umbral = umbral_fallos
        self._espera = espera_apertura
        self._reloj = reloj
        self._fallos = 0
        self._estado = "closed"          # estado INTERNO: "closed" | "open"
        self._abierto_en = 0.0

    @property
    def estado(self) -> str:
        # open + ventana cumplida se REPORTA como half-open (observable y testeable)
        if self._estado == "open" and (self._reloj() - self._abierto_en) >= self._espera:
            return "half-open"
        return self._estado

    def llamar(self, fn: Callable[[], T]) -> T:
        if self.estado == "open":
            raise CircuitoAbierto("circuito abierto: la llamada se rechaza sin intentarla")
        try:
            resultado = fn()              # closed o half-open: se permite el intento
        except Exception:
            self._registrar_fallo()
            raise
        self._registrar_exito()
        return resultado

    def _registrar_exito(self) -> None:
        self._fallos = 0
        self._estado = "closed"

    def _registrar_fallo(self) -> None:
        if self.estado == "half-open":    # falló la prueba: reabrir y reiniciar temporizador
            self._estado = "open"
            self._abierto_en = self._reloj()
            self._fallos = self._umbral
            return
        self._fallos += 1
        if self._fallos >= self._umbral:
            self._estado = "open"
            self._abierto_en = self._reloj()
```

Verificado contra `test_acceptance.py`: pasa los 7 casos (arranca cerrado; umbral abre; abierto rechaza sin invocar `fn`; ventana → half-open; prueba exitosa cierra; prueba fallida reabre y reinicia; éxito reinicia el contador).

## Por qué funciona

- **`estado` derivado.** El estado interno es solo `"closed"`/`"open"`; el `"half-open"` se **calcula** cuando el circuito está abierto y ya pasó la ventana. Así es observable desde fuera (`cb.estado == "half-open"`) y `llamar` reusa la misma condición: si `estado != "open"`, permite el intento (sea closed o half-open).
- **Rechazo sin invocar.** Estando `open` (ventana no cumplida), `llamar` lanza `CircuitoAbierto` **antes** de tocar `fn`. Esa es la "falla rápida".
- **Half-open de una sola prueba.** Como `llamar` es síncrono, la prueba es la única llamada que pasa mientras el estado deriva a half-open; su resultado decide: éxito → `_registrar_exito` (closed, contador 0); fallo → `_registrar_fallo` ve `estado == "half-open"` y reabre con `abierto_en` reiniciado.
- **Fallos consecutivos.** `_registrar_exito` pone `_fallos = 0`; por eso un éxito intercalado evita que se acumulen fallos históricos.

## El recorrido de razonamiento esperado (bitácora)
1. El retry **insiste** (asume falla breve); el breaker **deja de insistir** (asume falla prolongada) para no patear lo caído.
2. El breaker convierte fallas lentas (timeout × N intentos) en fallas rápidas (rechazo inmediato).
3. El half-open existe para **probar** si la dependencia volvió sin reabrir todas las compuertas de golpe (que reabriría la avalancha).
4. Van juntos: reintentas unas pocas veces; si el patrón de fallo persiste, el breaker abre.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Invocar `fn` estando abierto.** Debe rechazar ANTES; si llama y atrapa, no protege nada. El test `test_abierto_rechaza_sin_llamar_a_fn` lo verifica con un flag.
2. **Reiniciar el temporizador al reabrir desde half-open.** Sin `self._abierto_en = self._reloj()`, la próxima prueba llegaría de inmediato. El test `test_prueba_fallida_reabre...` lo caza (un `_ok` posterior debe dar `CircuitoAbierto`).
3. **Fallos consecutivos, no totales.** El éxito reinicia; el test `test_exito_reinicia_el_contador` lo fija.
4. **Reloj monotónico.** `time.monotonic` (no `time.time`, que puede retroceder por NTP); inyectable para los tests.
5. **Half-open observable.** Si `estado` no deriva half-open, `test_tras_la_ventana_queda_half_open` falla.

## Rango de soluciones aceptables
- **Estado interno explícito de tres valores** (`"half-open"` guardado, con la transición open→half-open hecha dentro de `llamar` antes de probar) — válido, siempre que `estado` lo exponga tras la ventana y la prueba sea única.
- **Contar `_abierto_en` con `None`** como "nunca abierto" en vez de `0.0` — equivalente.
- **Permitir un `umbral_exitos` en half-open** (cerrar tras N pruebas exitosas en vez de 1) — generalización aceptable si pasa los tests, no exigida.
- ❌ **No aceptable como competente:** invocar `fn` estando abierto; contar fallos totales; half-open que deja pasar todas las llamadas; no reiniciar el temporizador al reabrir; usar `time.time()` directo ignorando el reloj inyectado.
