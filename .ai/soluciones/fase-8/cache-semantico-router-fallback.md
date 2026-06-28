---
ejercicio_id: fase-8/cache-semantico-router-fallback
fase: fase-8
sub_unidad: "8.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir. No es
> la única implementación válida: cualquier variante que pase los tests, aísle por tenant antes del
> match y distinga reintentable de no-reintentable es correcta.

# Solución de referencia — Caché semántico + router con fallback

## Implementación completa de `cache_router.py`

```python
from __future__ import annotations

import math
from typing import Callable

UMBRAL_DEFECTO = 0.95


class ModeloSaturado(Exception):
    """Reintentable: 429 (rate limit) o 5xx (caída/sobrecarga)."""


class RequestInvalido(Exception):
    """NO reintentable: 400 (el request está mal armado)."""


def coseno(a: list[float], b: list[float]) -> float:
    punto = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return punto / (na * nb)


class SemanticCache:
    def __init__(self, embed_fn: Callable[[str], list[float]], umbral: float = UMBRAL_DEFECTO) -> None:
        self.embed_fn = embed_fn
        self.umbral = umbral
        # (tenant_id, embedding, respuesta)
        self._entradas: list[tuple[str, list[float], str]] = []

    def put(self, pregunta: str, tenant_id: str, respuesta: str) -> None:
        self._entradas.append((tenant_id, self.embed_fn(pregunta), respuesta))

    def get(self, pregunta: str, tenant_id: str) -> str | None:
        emb = self.embed_fn(pregunta)
        mejor_resp: str | None = None
        mejor_sim = -1.0
        # Filtro de tenant PRIMERO: es la barrera de seguridad, no un detalle de relevancia.
        for t, e, respuesta in self._entradas:
            if t != tenant_id:
                continue
            sim = coseno(emb, e)
            if sim > mejor_sim:
                mejor_sim, mejor_resp = sim, respuesta
        if mejor_resp is not None and mejor_sim >= self.umbral:
            return mejor_resp
        return None


def elegir_modelo(tipo_tarea: str) -> str:
    if tipo_tarea in ("clasificacion", "saludo", "extraccion_simple"):
        return "claude-haiku-4-5"      # barato, rápido, suficiente
    if tipo_tarea == "sintesis_larga":
        return "claude-opus-4-8"       # caro, pero la calidad importa
    return "claude-sonnet-4-6"         # balance por defecto


def responder_con_fallback(
    call_fn: Callable[[str, list], str],
    cadena: list[str],
    messages: list,
) -> str:
    for modelo in dict.fromkeys(cadena):   # dedup preservando el orden
        try:
            return call_fn(modelo, messages)
        except ModeloSaturado:
            continue                       # 429/5xx: prueba el siguiente
        # RequestInvalido NO se captura: propaga (no enmascaramos el bug del request)
    raise RuntimeError("todos los modelos de la cadena fallaron")
```

## Por qué cada decisión

- **Filtro de tenant antes del match (seguridad).** `get` recorre solo las entradas del `tenant_id`
  pedido. Si lo hicieras al revés (buscar el mejor coseno global y luego mirar el tenant), un día con
  un refactor sutil acabas devolviendo el hit de otro cliente: una **fuga de datos** (OWASP LLM,
  vector/embedding weaknesses). Por eso el filtro es lo primero y, sin entradas del tenant, es un miss
  limpio.
- **Similitud, no igualdad.** El hit se decide con `coseno >= self.umbral`, no con `pregunta ==
  pregunta_guardada`. Eso es lo que hace al caché *semántico*: "¿cómo pido vacaciones?" y "¿cómo me tomo
  días libres?" son el mismo hit. El umbral inyectado permite hacerlo más o menos estricto.
- **Router fácil→barato, difícil→caro.** No mandar una clasificación a Opus: misma calidad, ~5x el
  costo. Solo la síntesis larga justifica el modelo caro.
- **Fallback reintentable vs no-reintentable.** Captura **solo** `ModeloSaturado` (429/5xx → degradar al
  siguiente). `RequestInvalido` (400) **propaga**: reintentarlo en otro modelo no lo arregla, solo
  esconde el bug del request. La cadena va de caro a barato (`dict.fromkeys` dedup en orden); si se
  agota, `RuntimeError`.

## Errores comunes (para el corrector)
- `get` que compara por igualdad exacta → no es semántico.
- Buscar el vecino sobre todas las entradas y filtrar el tenant después → riesgo de fuga.
- `except Exception` genérico que se traga el `RequestInvalido`.
- Ignorar `self.umbral` (hardcodear 0.95) → rompe el test del umbral estricto.
- Fallback que degrada hacia un modelo más caro o reintenta el mismo en bucle.

## Rango de soluciones aceptables
- Usar un `dict` por tenant (`{tenant_id: [(emb, resp), ...]}`) en vez de una lista de tuplas es
  igualmente válido y de hecho más limpio para muchos tenants.
- `max(..., key=lambda ...)` en vez del bucle manual es aceptable mientras filtre por tenant primero y
  maneje el caso "sin entradas del tenant".
- El orden y los nombres internos pueden variar; lo que se exige es: filtro de tenant primero, match por
  similitud contra el umbral inyectado, y fallback que distingue 429/5xx de 400.
