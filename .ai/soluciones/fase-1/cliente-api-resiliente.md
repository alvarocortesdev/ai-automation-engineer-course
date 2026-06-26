---
ejercicio_id: fase-1/cliente-api-resiliente
fase: fase-1
sub_unidad: "1.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Cliente de API resiliente y testeable

## Respuesta canónica

```python
def nombre_de_usuario(user_id, fetch):
    # 1) Validar el input ANTES de gastar una petición.
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError(f"user_id inválido: {user_id!r}")

    # 2) La red puede fallar ANTES de que haya respuesta. Solo envolvemos fetch().
    try:
        resp = fetch(user_id)
    except (TimeoutError, ConnectionError) as e:
        raise ServicioInalcanzable(f"no se pudo contactar el servicio: {e}") from e

    # 3) Hubo respuesta: rutear por status. Caso feliz primero, luego errores específicos.
    if resp.status_code == 200:
        return resp.json()["name"]
    if resp.status_code == 404:
        raise UsuarioNoEncontrado(f"usuario {user_id} no existe")
    if resp.status_code >= 500:
        raise ServicioCaido(f"el servidor falló: {resp.status_code}")
    raise RespuestaInesperada(f"status no manejado: {resp.status_code}")
```

(Las excepciones de dominio `ServicioInalcanzable`, `UsuarioNoEncontrado`, `ServicioCaido`,
`RespuestaInesperada` vienen definidas en el starter.)

## Razonamiento paso a paso

1. **Validar primero, fuera del `try`.** Si `user_id` es inválido, no tiene sentido tocar la red:
   se lanza `ValueError` de inmediato. Va **antes** del `try` para que no se confunda con un error
   de red. (El `isinstance(user_id, bool)` extra evita que `True`, que en Python es `1`, cuele como
   id válido — detalle fino, no obligatorio para `competente`.)
2. **El `try` envuelve SOLO `fetch(user_id)`.** Ese es el único punto donde ocurre la red. Envolver
   toda la función sería un error: atraparía también el `KeyError` de `resp.json()["name"]` o los
   `raise` de dominio, disfrazándolos de `ServicioInalcanzable`.
3. **`except (TimeoutError, ConnectionError)`** → `ServicioInalcanzable`, con `from e` para conservar
   la causa. En producción, `fetch` real con `httpx` lanzaría `httpx.TimeoutException` /
   `httpx.ConnectError`; aquí el ejercicio usa los **builtin** `TimeoutError`/`ConnectionError`
   para mantener el test desacoplado de la librería. El **mapa mental** es idéntico.
4. **Ruteo de status, en orden:**
   - `200` → caso feliz, `return resp.json()["name"]`.
   - `404` → error esperado y específico (`UsuarioNoEncontrado`).
   - `>= 500` → fallo del servidor (`ServicioCaido`), potencialmente reintentable.
   - cualquier otro → `RespuestaInesperada` (catch-all al **final**).
   El orden importa: si el catch-all fuera primero, las ramas específicas serían inalcanzables.

## Por qué el seam (lo que de verdad enseña el ejercicio)

`fetch` está **inyectado**: la función no sabe de dónde viene la respuesta. En el test, `fetch` es
un stub que devuelve una `RespFalsa(status_code, payload)` o lanza una excepción — **sin red**.
Esto es **inyección de dependencias**, y es exactamente cómo se testea código que llama a un LLM
(2.11): el LLM es una API, se mockea su respuesta igual. El corrector debe verificar que el alumno
**entiende** esto, no solo que pasó los tests.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`try` demasiado ancho.** Envolver toda la función en `try/except (TimeoutError, ConnectionError)`
   "funciona" para los tests dados, pero es frágil: si `resp.json()` lanzara, se convertiría
   silenciosamente en `ServicioInalcanzable`. El `try` debe ceñirse a `fetch(...)`.
2. **`except Exception` genérico.** Atrapa también los `raise` de dominio y los bugs propios. Cazar.
3. **Usar `>= 400` para todo.** Colapsa 4xx y 5xx, perdiendo la distinción que es el objetivo (4xx no
   se reintenta, 5xx sí). El 404 debe tratarse aparte del 500.
4. **Validar después de `fetch`.** Gasta una petición en input ya inválido. El test
   `fetch_que_no_debe_correr` lo detecta: si el alumno llama `fetch` con un id inválido, ese test
   falla con `AssertionError`.
5. **Orden de guardas.** Catch-all antes de las ramas específicas → ramas muertas.

## Rango de soluciones aceptables
- **`elif` vs `if`+`return`:** usar una cadena `if/elif/else` es igual de válido que `if`s con
  `return`/`raise` que cortan el flujo. Ambos correctos.
- **Validación de `user_id`:** aceptar solo `user_id <= 0` (sin el chequeo de `bool`/`isinstance`) es
  `competente`; el ejercicio no exige rechazar tipos no-int explícitamente salvo en el caso borde que
  el alumno agregue. Rechazar `bool` y no-int es `excelente`.
- **No usar `from e`:** baja a `competente`; el comportamiento observable es correcto pero se pierde
  la cadena de causa.
- **Mensajes de excepción:** cualquier texto razonable sirve; no se exige una redacción concreta.
- **Atrapar `RequestError`/excepciones de httpx** en vez de los builtin: señal de no haber leído el
  contrato (el `fetch` inyectado usa builtins). Si además importa `httpx` sin usarlo, reforzar la
  señal de dependencia-IA, pero si el resto de la lógica es correcta, el ruteo de status sigue
  evaluándose por su mérito.
