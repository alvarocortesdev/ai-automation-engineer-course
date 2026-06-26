# Ejercicio 3.15 — Cache-aside con TTL e invalidación

> **Modalidad: código (Primero-Sin-IA, timebox 40 min).** Implementa el patrón de caching
> más usado del backend, en su forma pura y testeable. **No necesitas instalar ni correr Redis:**
> la cache se inyecta como un doble de prueba (ports & adapters de `3.9`). Eso te deja ver el
> patrón sin el ruido de la red, y te entrena para testear código que habla con servicios externos.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.15` Redis (caching/sesiones)
**Ruta:** opcional/profundización · **Timebox:** 40 min

## 🎯 Objetivo

Implementar `CatalogoService` con dos operaciones:
- `obtener(producto_id)` → lectura **cache-aside**: HIT desde cache sin tocar el repo; MISS consulta
  el repo y **puebla la cache con TTL**.
- `actualizar(producto_id, datos)` → escritura que escribe el repo **primero** y luego **invalida** la cache.

## 📋 Contexto

Cache-aside es el patrón que debes saber de memoria: la cache se llena bajo demanda, y la mitad que
la gente olvida es invalidar al escribir. Este ejercicio te obliga a implementar **ambas** mitades y a
defender el orden de las operaciones. Alimenta directamente el endpoint cacheado opcional del capstone
de la fase.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Mira fallar los tests primero: entender el rojo es parte del aprendizaje.
2. Solo entonces, consulta la **documentación oficial** (redis.io, redis-py) si lo necesitas.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescribe `obtener` de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `cache_aside.py` y completa `CatalogoService.obtener` y `CatalogoService.actualizar`
   (no cambies las firmas ni `TTL_SEGUNDOS` ni `clave_producto`).
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade **un test tuyo**: un producto que cambia **dos veces seguidas** nunca debe servir un valor
   intermedio rancio desde la cache.
5. Escribe `bitacora.md` (ver criterios de "hecho").

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en verde: MISS consulta el repo una vez y puebla la cache con `TTL_SEGUNDOS`; el
      segundo `obtener` es un HIT que **no** vuelve al repo; tras `actualizar`, la siguiente lectura
      devuelve el dato nuevo (no el viejo cacheado).
- [ ] Agregaste tu test de "dos cambios seguidos".
- [ ] `bitacora.md` explica: por qué el `return` del HIT va antes de tocar el repo; por qué invalidas
      **borrando** (no actualizando); por qué el orden DB-primero-luego-invalidar importa.
- [ ] Puedes explicar, sin notas, qué es un *cache miss* y qué hace el TTL.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`obtener`: lee la cache con `self.cache.get(clave)`. Si **no es `None`**, deserializa con `json.loads`
y devuelve de inmediato (corta ahí, no toques el repo). Si es `None`, pide al repo, guarda en la cache
con `self.cache.set(clave, json.dumps(producto), TTL_SEGUNDOS)` y devuelve.

`actualizar`: llama a `self.repo.actualizar_producto(...)` **primero**, luego `self.cache.delete(clave)`.

Cuidado con `if cacheado:` vs `if cacheado is not None:` — un valor cacheado podría ser falsy.

Revisa la sección 4.4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/cache-aside-ttl.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/cache-aside-ttl.md` — no la mires antes de
intentarlo de verdad.
