---
ejercicio_id: fase-1/cliente-fetch-status
fase: fase-1
sub_unidad: "1.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Cliente fetch que rutea status codes (sin red)

## Respuesta canónica

```javascript
export async function obtenerNombreUsuario(userId, fetchFn) {
  // 1) Validar el input ANTES de gastar una petición (antes de cualquier await).
  if (!Number.isInteger(userId) || userId <= 0) {
    throw new EntradaInvalida(`userId inválido: ${userId}`);
  }

  // 2) La red puede RECHAZAR antes de haber respuesta. Envolvemos SOLO fetchFn.
  let resp;
  try {
    resp = await fetchFn(userId);
  } catch (err) {
    throw new ServicioInalcanzable(`no se pudo contactar el servicio: ${err.message}`);
  }

  // 3) Hubo respuesta: rutear por status A MANO (fetch NO rechaza por 4xx/5xx).
  if (resp.status === 200) {
    const datos = await resp.json(); // segundo await: leer el body
    return datos.name;
  }
  if (resp.status === 404) {
    throw new UsuarioNoEncontrado(`usuario ${userId} no existe`);
  }
  if (resp.status >= 500) {
    throw new ServicioCaido(`el servidor falló: ${resp.status}`);
  }
  throw new RespuestaInesperada(`status no manejado: ${resp.status}`);
}
```

(Las clases `EntradaInvalida`, `ServicioInalcanzable`, `UsuarioNoEncontrado`, `ServicioCaido`,
`RespuestaInesperada` vienen definidas en el starter.)

## Razonamiento paso a paso

1. **Validar primero, antes de cualquier `await`.** Si `userId` no es un entero positivo, no tiene
   sentido tocar la red: se lanza `EntradaInvalida` de inmediato. Va **antes** del `try` para no
   confundirlo con un error de red, y para no gastar una petición. El test `noDebeCorrer` falla si el
   alumno llama `fetchFn` con input inválido.
2. **El `try` envuelve SOLO `await fetchFn(userId)`.** Ese es el único punto donde la promesa puede
   **rechazar** (error de red). Envolver toda la función sería un error: atraparía también un
   `TypeError` de `resp.json()` o los `throw` de dominio, disfrazándolos de `ServicioInalcanzable`.
3. **La trampa de JS (el núcleo del ejercicio):** `fetch`/`fetchFn` **resuelve** la promesa ante un 404
   o 500 — para `fetch`, "recibí una respuesta" cuenta como éxito. Solo **rechaza** por fallo de red.
   Por eso el ruteo de status va **fuera** del `try` de red, revisando `resp.status` a mano. En Python
   (1.5) esto era explícito con `if resp.status_code`; aquí es idéntico de mapa mental.
4. **Doble `await`.** `await fetchFn(...)` da la respuesta; `await resp.json()` lee el body (también
   async). Olvidar el segundo deja `datos` como una promesa y `datos.name` como `undefined`.
5. **Ruteo de status, en orden:** 200 (feliz) → 404 (esperado) → `>= 500` (servidor) → catch-all
   (`RespuestaInesperada`) al final. Si el catch-all fuera primero, las ramas específicas serían
   inalcanzables.

## Por qué el seam (lo que de verdad enseña el ejercicio)

`fetchFn` está **inyectado**: la función no sabe de dónde viene la respuesta. En el test, `fetchFn` es
un stub que resuelve con `{ status, json: async () => ({...}) }` o que rechaza — **sin red**. Esto es
**inyección de dependencias**, exactamente cómo se testea código que llama a un LLM (2.11): el LLM es
una API, se mockea su respuesta igual. El corrector verifica que el alumno **entiende** esto.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Asumir que `fetch` rechaza por 404/500.** El error conceptual central. Si el alumno mete el ruteo
   de status dentro de un `try/catch` esperando "atrapar" el 404, no entendió la trampa.
2. **Olvidar el segundo `await`.** `return resp.json().name` → `undefined`. El test de 200 lo caza.
3. **`try` demasiado ancho.** Envolver toda la función "funciona" para los tests dados pero es frágil:
   convierte cualquier `throw` o `TypeError` propio en `ServicioInalcanzable`. Debe ceñirse a `fetchFn`.
4. **`catch` genérico que traga errores de dominio.** Cazar.
5. **Validar después de `fetchFn`.** Gasta una petición; `noDebeCorrer` falla.
6. **Usar `>= 400` para todo.** Colapsa 4xx y 5xx, perdiendo la distinción.

## Rango de soluciones aceptables
- **`if`+`throw`/`return` vs `if/else if/else`:** ambos válidos si el orden de guardas es correcto.
- **`resp.ok` en vez de `resp.status === 200`:** el `fetchFn` falso del test no provee `.ok`, así que
  para el caso 200 debe usarse `resp.status === 200`. Usar `resp.ok` haría fallar el test → marca que
  no leyó el contrato del stub (que expone `.status`, no `.ok`).
- **No usar `cause`/`from`:** baja a `competente`; el comportamiento observable es correcto pero se
  pierde la cadena de causa (en JS: `new ServicioInalcanzable(msg, { cause: err })`).
- **Validación de `userId`:** `userId <= 0` solo (sin `Number.isInteger`) deja pasar `1.5`; el test de
  `1.5` lo exige, así que la validación debe rechazar no-enteros para llegar a `competente`.
- **Mensajes de excepción:** cualquier texto razonable; no se exige una redacción concreta.
- **Importar/usar el `fetch` global real, `axios` o reintentos con backoff:** señal de no haber leído
  el contrato (el `fetchFn` inyectado es el único canal). Si el resto de la lógica es correcta, el
  ruteo se evalúa por su mérito, pero se refuerza la señal de dependencia-IA.
