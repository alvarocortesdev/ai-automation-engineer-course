# 1.7 — Cliente fetch que rutea status codes (sin red)

> **Modalidad: código (JavaScript async, sin IA).** Modela los modos de fallo de una llamada a una API
> con `fetch`, incluida la trampa de JS: **`fetch` no rechaza la promesa por un status 404 o 500** —
> solo rechaza por un fallo de red—. Revisar el status es TU trabajo. Es el gemelo JavaScript del
> cliente resiliente de la lección 1.5 (Python).

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.7` JavaScript moderno (ES6+)
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Implementar una función **async** que consume una API (vía un `fetch` inyectado), distingue los status
codes (200/404/5xx/otro), separa el error de red del status de error, y valida el input antes de gastar
una petición — **sin tocar la red en los tests**.

## 📋 Contexto

Toda app de IA en el navegador habla con su backend por `fetch`. La diferencia entre código de juguete
y código de producción está en el manejo de fallos: un 500 a las 3 AM, una red caída, un payload raro.
Este ejercicio es la mecánica exacta del lado JS del **Capstone F1** y de la UI de streaming de F4.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba).
2. Solo entonces, consulta **documentación oficial** (MDN: Using Fetch — lee por qué un 404 no rechaza).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**.

## 🛠️ Instrucciones

1. Abre `solucion.js` y completa `obtenerNombreUsuario`. **No cambies la firma ni los nombres de las
   clases de error** (ya están definidas).
2. Corre los tests con el runner integrado de Node (no instalas nada):

   ```bash
   node --test
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso borde tuyo** en `solucion.test.js`.

### Contrato

`obtenerNombreUsuario(userId, fetchFn)` — `fetchFn` está **inyectado**: devuelve una promesa de un
objeto con `.status` (number) y `.json()` (async). Puede **rechazar** (error de red).

- `userId` inválido (≤ 0 o no entero) → lanza `EntradaInvalida` **antes** de llamar `fetchFn`.
- `fetchFn` **rechaza** (error de red) → lanza `ServicioInalcanzable` (no dejes escapar el error crudo).
- status `200` → devuelve `(await resp.json()).name` — recuerda el **doble `await`**.
- status `404` → lanza `UsuarioNoEncontrado`.
- status `>= 500` → lanza `ServicioCaido`.
- cualquier otro status → lanza `RespuestaInesperada`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Validas `userId` **antes** de llamar `fetchFn` (el test `noDebeCorrer` lo verifica).
- [ ] Distingues los cuatro destinos de status (200 / 404 / 5xx / otro), cada uno con su error.
- [ ] Conviertes el rechazo de red en `ServicioInalcanzable` (no escapa el error crudo).
- [ ] Usas el **doble `await`** y revisas el status **a mano** (no asumes que `fetch` rechaza por 404/500).
- [ ] Todos los tests pasan **sin red** y agregaste al menos uno propio.
- [ ] Puedes **explicar sin notas** por qué `fetch` no rechaza ante un 500.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Orden: primero **valida** `userId` y lanza `EntradaInvalida` si es inválido — esto va **antes** de
cualquier `await` (`Number.isInteger(userId)` y `userId > 0`). Luego envuelve **solo** `await fetchFn(userId)`
en un `try/catch`: si rechaza, lanzas `ServicioInalcanzable`. Con la respuesta en mano (fuera del `try`
de red), ramifica por `resp.status` con el caso `200` primero —ahí va el **segundo `await`** de
`resp.json()`—, luego `404`, luego `>= 500`, y un catch-all final. El orden de las guardas importa
(catch-all al final). Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/cliente-fetch-status.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/cliente-fetch-status.md` — no la mires
antes de intentarlo de verdad.
