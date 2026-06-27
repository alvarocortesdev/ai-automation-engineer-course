# Ejercicio 4.6 A — Route Handler con validación de entrada

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.6` Next.js
**Ruta:** crítica · **Modalidad:** código · **Timebox:** 40 min

## 🎯 Objetivo

Implementar el Route Handler `GET` de un endpoint de Next.js (`app/api/modelos/route.ts`) que filtra un catálogo de modelos por una consulta `q` y limita los resultados con `limit`, **validando la entrada** y devolviendo los status codes correctos. Lo escribes con las APIs web estándar `Request`/`Response` que Next.js soporta, así que **corre y se prueba sin levantar Next.js**.

## 📋 Contexto

En el capstone, la UI de chat pide datos al servidor a través de un Route Handler como este (con la clave de API a salvo en el servidor). Aquí entrenas dos cosas a la vez: la **mecánica** del handler (leer query params, responder JSON) y el **hilo de seguridad** que recorre todo el curso: *nunca confíes en la entrada del cliente*. Un endpoint sin validar es una puerta abierta (OWASP: *Injection*, entrada no acotada).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces consulta la **documentación oficial** de Route Handlers: <https://nextjs.org/docs/app/api-reference/file-conventions/route>.
3. **Solo al final**, usa IA para *revisar y explicar* —no para *generar* el handler.
4. Mañana, **reescríbelo de memoria**, incluida la validación. Si no puedes, no lo aprendiste todavía.

## 🧾 Contrato del endpoint (lo que los tests verifican)

- `?q=` (opcional): filtra por **substring case-insensitive** contra el `nombre` **o** el `proveedor`. Sin `q` (o vacío), no filtra.
- `?limit=` (opcional, **default 10**): entero `≥ 1`. Si no es entero `≥ 1` (`abc`, `0`, negativo) → **400**. Si supera `50`, se **acota** a `50` (no es error).
- Si `q` supera **64 caracteres** → **400** (entrada no acotada = riesgo).
- Éxito (**200**): `Response.json({ query, count, items })`, donde `count` = cantidad de `items` devueltos y `query` = el `q` usado (`""` si no vino).
- Entrada inválida (**400**): `Response.json({ error }, { status: 400 })`.

> Los datos viven en `datos.ts` (`MODELOS`, 12 modelos). **No edites `datos.ts`**: los tests dependen de él. Implementa **solo** `route.ts`.

## 🛠️ Instrucciones

1. Abre `route.ts`. Implementa `GET` respetando el contrato (no cambies el nombre del export).
2. Instala dependencias y corre los tests:

   ```bash
   pnpm install
   pnpm test
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test propio** en `route.test.ts` (un caso borde: `q` con espacios, `limit=50` exacto, acentos, `q` en mayúsculas contra proveedor en minúsculas…).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Lees `q` y `limit` desde `new URL(request.url).searchParams`.
- [ ] **Validas antes de procesar**: `q` largo y `limit` inválido devuelven `400` con cuerpo `{ error }`.
- [ ] Filtras case-insensitive contra `nombre` **y** `proveedor`.
- [ ] Acotas por `limit` (con clamp a 50) y aplicas el default 10.
- [ ] Devuelves la forma exacta `{ query, count, items }` con status `200`.
- [ ] Todos los tests pasan y agregaste un test propio.
- [ ] Puedes **explicar sin notas** por qué validar en el servidor es obligatorio aunque el cliente "ya valide".

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Lee `const params = new URL(request.url).searchParams;`. Saca `q` con `params.get("q") ?? ""`
y haz `q = q.trim()`. Valida el largo de `q` → `return Response.json({ error }, { status: 400 })`.
Para `limit`: si `params.has("limit")`, parsea con `Number(...)`, comprueba `Number.isInteger(limit) && limit >= 1`,
si no → `400`; luego `limit = Math.min(limit, 50)`. Filtra con
`m.nombre.toLowerCase().includes(q.toLowerCase()) || m.proveedor.toLowerCase().includes(q.toLowerCase())`,
corta con `.slice(0, limit)` y responde `{ query: q, count: items.length, items }`. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/route-handler-modelos/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/route-handler-modelos.md` — no la mires antes de intentarlo de verdad.
