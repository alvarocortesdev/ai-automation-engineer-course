---
ejercicio_id: fase-7/cdc-reductor-reembedding
fase: fase-7
sub_unidad: "7.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). El alumno debe entregar su propio intento antes de que esto se discuta.

# Solución de referencia — Reductor CDC → tareas de re-embedding

Esta es **una** solución canónica. Hay variantes aceptables (una sola pasada con un `dict`
acumulador, usar enums en vez de strings para la acción, mensajes/estructuras distintas).
Lo que NO es negociable: el reductor **colapsa a la intención final por key** (debounce),
**propaga el delete solo si la key estaba indexada**, **no emite tarea para la fila que
nace-y-muere sin estar indexada**, **no re-embeddea contenido idéntico** al indexado, y la
salida es **determinista (ordenada por key)** — lo que la vuelve idempotente.

## Respuesta canónica

Dos pasadas. (1) Recorrer los eventos *en orden* construyendo `estado_final[key]`:
`c`/`r`/`u` → `("vivo", after["contenido"])`; `d` → `("muerto", None)`. El último evento de
cada key gana (eso *es* el debounce). (2) Por cada key en `sorted(estado_final)`, decidir
la tarea comparando contra `indexado`.

## `reducir`

```python
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Evento:
    op: str
    key: str
    after: dict | None = None


@dataclass
class Tarea:
    accion: str
    key: str
    contenido: str | None = None


def reducir(eventos: list[Evento], indexado: dict[str, str]) -> list[Tarea]:
    # --- Pasada 1: estado final por key (debounce) ---
    estado: dict[str, tuple[str, str | None]] = {}
    for ev in eventos:
        if ev.op in ("c", "r", "u"):
            contenido = ev.after["contenido"] if ev.after else None
            estado[ev.key] = ("vivo", contenido)
        elif ev.op == "d":
            estado[ev.key] = ("muerto", None)
        # otros (tombstone puro / truncate / message): se ignoran

    # --- Pasada 2: decidir la tarea, comparando con lo ya indexado ---
    tareas: list[Tarea] = []
    for key in sorted(estado):
        vivo_o_muerto, contenido = estado[key]
        if vivo_o_muerto == "muerto":
            if key in indexado:                 # propagar SOLO si estaba indexado
                tareas.append(Tarea("delete", key, None))
            # nace-y-muere sin estar indexado -> ninguna tarea
        else:                                   # vivo
            if indexado.get(key) != contenido:  # no re-embeddear lo idéntico (costo)
                tareas.append(Tarea("upsert", key, contenido))
    return tareas
```

## Profundización (excelente)

- **Resumen de observabilidad** (helper opcional):

```python
def resumen(tareas: list[Tarea]) -> dict:
    return {
        "upserts": sum(1 for t in tareas if t.accion == "upsert"),
        "deletes": sum(1 for t in tareas if t.accion == "delete"),
    }
```
  (Los `skips_por_contenido_igual` se cuentan en la pasada 2 si el alumno los lleva; no es obligatorio que estén en `Tarea`.)
- **Idempotencia:** como el resultado es función del *estado final* + `indexado`, pasar `eventos + eventos` da exactamente lo mismo que `eventos`. El test del punto 8 debe verificarlo.
- **Tombstone:** un evento con `op` distinto de c/r/u/d simplemente cae en el `else` implícito y se ignora — ya es robusto.

## Salida esperada de `pytest -v`

Los 11 tests provistos en `PASSED`. Clave: `test_lote_completo_de_la_leccion` debe dar
exactamente `[Tarea("upsert", "a", "Hola de nuevo"), Tarea("delete", "b", None)]` (a antes
que b por orden de key; c no produce nada); `test_misma_tanda_dos_veces_da_el_mismo_resultado`
verifica la idempotencia; `test_contenido_igual_al_indexado_no_genera_tarea` verifica el
ahorro de costo.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Debounce vs una-tarea-por-evento.** Si emite N tareas para N updates de la misma fila, no colapsó. Es `en-progreso`, no `competente`.
2. **`after` None en delete.** Leer `after["contenido"]` en un `d` revienta. La solución solo toca `after` en c/r/u.
3. **Delete propagado SOLO si estaba indexado.** Emitir `delete` para una key que nunca estuvo en `indexado` (la que nace-y-muere) es ruido; no hacerlo cuando sí estaba es el fantasma. Ambos extremos son error.
4. **No re-embeddear lo igual.** Sin el `indexado.get(key) != contenido`, todo update produce upsert aunque el contenido sea idéntico → quema tokens.
5. **Orden por key.** Sin `sorted`, los tests de orden fallan y el resultado no es reproducible.

## Rango de soluciones aceptables

- **Una sola pasada** con un `dict` que se sobreescribe y una decisión diferida es válida si el resultado final es idéntico y determinista.
- Representar el estado como `None`-para-muerto en vez de una tupla `("muerto", None)` — equivalente.
- Usar una `Enum` para `accion` o comparar por hash de contenido en vez del string crudo — aceptable (el hash incluso es más realista para textos largos).
- Para el `WRITEUP.md`: cuenta como comprensión (O3) si (a) explica que CDC es at-least-once y por qué eso obliga idempotencia, y (b) nombra la regla de no re-embeddear lo igual como ahorro O(cambios) vs O(corpus).

## Nota sobre la lección (para el corrector)

La lección 7.6 muestra el envelope real de Debezium (op c/u/d/r, before/after, source/lsn),
la config del conector Postgres (`pgoutput`, `slot.name`, `publication.name`,
`table.include.list`) y el pipeline CDC→re-embedding con sus cuatro reglas (mapeo,
idempotencia, debounce, propagar deletes). El alumno NO debía usar Kafka/Debezium reales en
el ejercicio (implementa la lógica a mano); si delegó a una librería de streaming y no sabe
explicar el reductor, es señal de dependencia-IA, no de dominio.
