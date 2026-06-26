---
ejercicio_id: fase-3/cache-aside-ttl
fase: fase-3
sub_unidad: "3.15"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Cache-aside con TTL e invalidación

## Respuesta canónica

```python
import json

class CatalogoService:
    def __init__(self, cache, repo):
        self.cache = cache
        self.repo = repo

    def obtener(self, producto_id):
        clave = clave_producto(producto_id)
        cacheado = self.cache.get(clave)
        if cacheado is not None:                 # HIT: corta aqui, no toca el repo
            return json.loads(cacheado)
        producto = self.repo.obtener_producto(producto_id)   # MISS: fuente de verdad
        self.cache.set(clave, json.dumps(producto), TTL_SEGUNDOS)  # poblar con TTL
        return producto

    def actualizar(self, producto_id, datos):
        self.repo.actualizar_producto(producto_id, datos)    # 1) DB primero
        self.cache.delete(clave_producto(producto_id))       # 2) invalidar (borrar)
```

Test propio esperado (uno válido):

```python
def test_dos_cambios_seguidos_sin_stale(productos):
    cache, repo = SpyCache(), SpyRepo(productos)
    svc = CatalogoService(cache, repo)
    svc.obtener(1)                       # cachea 3990
    svc.actualizar(1, {"precio": 4490})
    assert svc.obtener(1)["precio"] == 4490
    svc.actualizar(1, {"precio": 5990})
    assert svc.obtener(1)["precio"] == 5990   # nunca el intermedio (4490) ni el viejo (3990)
```

## Razonamiento paso a paso

1. **El HIT corta antes del repo.** El `return json.loads(cacheado)` vive **dentro** del `if cacheado is not None`. Si quedara fuera, o si después del `if` igual se consultara el repo, perderías todo el beneficio: el caso de `test_hit_no_consulta_repo` exige `repo.lecturas == 0`.
2. **`is not None`, no `if cacheado:`.** Un valor cacheado podría serializar a un string falsy en otros diseños; el guard correcto compara contra `None` (que es lo único que devuelve la cache en un MISS).
3. **Poblar con TTL.** `self.cache.set(clave, json.dumps(producto), TTL_SEGUNDOS)` — el tercer argumento es el TTL; `test_miss_...` lo verifica en `cache.ttls`.
4. **JSON, no pickle.** Redis guarda strings; `json.dumps`/`json.loads` es legible, portable y seguro. (En la versión real con redis-py, `set` lleva `ex=TTL_SEGUNDOS`.)
5. **Invalidar = borrar, en orden DB→cache.** En `actualizar`, escribir el repo primero garantiza que la fuente de verdad sea correcta antes de descartar la copia. Borrar (en vez de re-escribir la cache) deja que el próximo `obtener` recargue desde la verdad: cache-aside puro, sin races de write-through.

## Puntos resbalosos (donde el corrector debe mirar)
1. **HIT que no corta:** el bug más común. Síntoma: `test_hit_no_consulta_repo` falla con `repo.lecturas == 1`.
2. **TTL omitido o cableado a otro número:** `cache.ttls[clave]` no es `TTL_SEGUNDOS`. A veces el alumno pasa el TTL como segundo argumento por confundir el orden de `set`.
3. **Orden invertido en `actualizar`:** borrar antes de escribir. Los tests provistos pasan igual (porque no simulan fallo de DB), así que esto se caza en la **bitácora** y el razonamiento, no en el rojo. Señalarlo.
4. **"Actualizar" la cache en `actualizar`** (`self.cache.set(...)` con el dato nuevo) en vez de `delete`: funciona en estos tests pero es write-through, no lo pedido; explicar la diferencia y las races.
5. **No agregar test propio** o agregar uno trivial.

## Rango de soluciones aceptables
- Extraer la clave a una variable o llamar `clave_producto(...)` inline: ambas válidas.
- Usar un único `try/except json.JSONDecodeError` defensivo alrededor del `loads` es aceptable (incluso deseable) aunque no se pida.
- En `actualizar`, llamar `delete` aunque la clave no exista es correcto (es idempotente; `delete` de una clave ausente no falla).
- Una solución que además invalide de forma más sofisticada (p. ej. versión de clave) es `excelente` si la `bitacora` la justifica, pero **no** es necesaria: el `delete` simple es la respuesta canónica del nivel.
- El test propio puede expresar el "dos cambios seguidos" de varias formas; cualquiera que verifique que no se sirve un valor intermedio/viejo cuenta.
