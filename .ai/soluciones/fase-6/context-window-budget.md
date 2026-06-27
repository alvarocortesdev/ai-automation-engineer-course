---
ejercicio_id: fase-6/context-window-budget
fase: fase-6
sub_unidad: "6.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para
> detectar el error y graduar las pistas.

# Solución de referencia — Token budget: arma el contexto que cabe

## Respuesta canónica (implementación)

```python
from __future__ import annotations
from typing import Callable


def armar_contexto(
    system: str,
    historial: list[dict],
    presupuesto_tokens: int,
    contar: Callable[[str], int],
) -> dict:
    base = contar(system)
    if base > presupuesto_tokens:
        raise ValueError("El system solo ya excede el presupuesto")
    restante = presupuesto_tokens - base
    incluidos: list[dict] = []
    for msg in reversed(historial):          # del más reciente al más viejo
        costo = contar(msg["content"])
        if costo > restante:                 # un turno entero ya no cabe -> corta
            break
        restante -= costo
        incluidos.append(msg)
    incluidos.reverse()                      # restaura el orden cronológico
    return {"system": system, "messages": incluidos}
```

## Razonamiento paso a paso

1. **El system es el contrato.** Se cuenta primero y nunca se descarta. Si solo él ya
   no cabe, no hay nada que negociar: `ValueError`. (En un sistema real, eso obliga a
   acortar el propio system, no el historial.)
2. **La recencia gana → recorrer `reversed(historial)`.** Los turnos recientes
   cargan el "estado actual" de la conversación; los viejos suelen ser ruido. Por eso
   se llena el presupuesto empezando por el final.
3. **Corte en el primer turno que no cabe (`break`).** Esto produce un **sufijo
   contiguo** (los N más recientes). No se "salta" un turno grande para meter uno más
   chico atrás: eso rompería la continuidad de la conversación y confundiría al modelo.
4. **Un turno entra entero o no entra.** Nunca se parte `content`: medio mensaje es
   peor que ninguno (el modelo lo completa con suposiciones).
5. **Reinvertir antes de devolver.** La API espera el orden cronológico (más viejo
   primero); como acumulamos al revés, hay que reinvertir.

### Traza del caso del README (contador = palabras, budget 35)
- system = 5 → restante 30.
- t4 (10) → restante 20; t3 (10) → 10; t2 (10) → 0; t1 (10) → 10 &gt; 0 → corta.
- incluidos (acumulados) = [t4, t3, t2] → reinvertido → **[t2, t3, t4]**.
- total = 5 + 30 = 35 ≤ 35. ✓

## Puntos resbalosos (donde el corrector debe mirar)

1. **Recorrido al derecho** (`for msg in historial`) cortando al final: conserva los
   **viejos**, no los recientes. Error de concepto — marcarlo.
2. **Olvidar `incluidos.reverse()`**: la salida queda con el más reciente primero.
3. **Comparación `>=` en vez de `>`**: con `>=`, un turno que cabe justo se descarta
   (off-by-one en el borde). El test del presupuesto exacto (35) lo atrapa.
4. **No manejar el `ValueError`**: devolver `{"system": ..., "messages": []}` cuando
   el system excede es un falso "éxito".
5. **Usar un tokenizer real en vez de `contar`**: rompe la inyección de dependencia y
   ata el ejercicio a la red.

## Rango de soluciones aceptables

- Una variante que use índices (`range(len(historial)-1, -1, -1)`) en vez de
  `reversed(...)` es igual de válida si produce el mismo sufijo y el mismo orden.
- Acumular en una `deque` con `appendleft` (evitando el `reverse()` final) es
  aceptable y hasta más elegante.
- **Profundización opcional (excelente, no requerido):** en vez de descartar los
  turnos viejos, **resumirlos** en una nota de compactación y prependerla — eso ya es
  compactación, el siguiente nivel. Si el alumno lo intenta y funciona, es señal de
  dominio; no penalizar a quien hace solo eviction (es lo que pide el enunciado).
- No se exige un mensaje exacto en el `ValueError`; basta con que se lance.
