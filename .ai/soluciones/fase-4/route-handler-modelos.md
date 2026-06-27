---
ejercicio_id: fase-4/route-handler-modelos
fase: fase-4
sub_unidad: "4.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Route Handler con validación de entrada

## Respuesta canónica

```ts
// route.ts
import { MODELOS } from "./datos";

export async function GET(request: Request): Promise<Response> {
  const params = new URL(request.url).searchParams;

  // 1) Leer la entrada.
  const q = (params.get("q") ?? "").trim();

  // 2) Validar ANTES de procesar (seguridad: acotar la entrada).
  if (q.length > 64) {
    return Response.json({ error: "consulta demasiado larga (máx. 64)" }, { status: 400 });
  }

  let limit = 10; // default
  if (params.has("limit")) {
    limit = Number(params.get("limit"));
    if (!Number.isInteger(limit) || limit < 1) {
      return Response.json({ error: "limit debe ser un entero >= 1" }, { status: 400 });
    }
  }
  limit = Math.min(limit, 50); // clamp: más de 50 no es error, se acota.

  // 3) Procesar: filtrar case-insensitive contra nombre O proveedor.
  const ql = q.toLowerCase();
  const coincidencias = MODELOS.filter(
    (m) =>
      m.nombre.toLowerCase().includes(ql) ||
      m.proveedor.toLowerCase().includes(ql),
  );
  const items = coincidencias.slice(0, limit);

  // 4) Responder con la forma estable.
  return Response.json({ query: q, count: items.length, items });
}
```

## Razonamiento paso a paso
- **Firma:** el nombre `GET` ES el verbo HTTP. Tipar `request: Request` (web estándar) mantiene el handler portable y testeable sin levantar Next.js; en un proyecto real Next.js pasa un `NextRequest`, que es un superset compatible.
- **Leer la entrada:** `new URL(request.url).searchParams` es la forma estándar de leer query params. `?? ""` cubre el caso sin `q`; `.trim()` normaliza espacios al borde.
- **Validar antes de procesar (el corazón de O2):** las dos guardias devuelven `400` con `{ error }` ANTES de tocar los datos. El `limit > 50` **no** es error: se acota con `Math.min`. La diferencia entre "rechazar" (q largo, limit basura) y "acotar" (limit grande) es deliberada y es lo que el contrato exige.
- **Procesar:** `q.toLowerCase()` una sola vez (micro-claridad). El filtro combina `nombre` y `proveedor` con `||`, por eso `q=openai` encuentra los modelos cuyo proveedor es OpenAI aunque "openai" no esté en el nombre.
- **`count` correcto:** se calcula sobre `items` (lo realmente devuelto tras el `slice`), no sobre el total de coincidencias. Un error común es reportar el total.
- **Responder:** `Response.json(obj, { status })` arma la respuesta con el header `Content-Type: application/json` y el código adecuado.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`Number('abc')` es `NaN`:** sin `Number.isInteger`, un `limit` basura se cuela. Verificar que `?limit=abc` dé 400, no 200 ni 500.
2. **`limit > 50` acota, no rechaza:** confirmar que `?limit=1000` da 200 (con 12 items, porque el catálogo es chico), no 400.
3. **Filtra por nombre Y proveedor:** si solo filtra por `nombre`, el test `q=openai` falla. Es la pista de que el alumno no leyó bien el contrato.
4. **Case-insensitive en AMBOS lados:** olvidar `.toLowerCase()` en el item o en la query rompe el test de mayúsculas.
5. **`count` sobre items devueltos:** si reporta el total de coincidencias en vez de `items.length`, el test de `limit=3` falla.
6. **Status code correcto:** `400` (Bad Request) para entrada inválida, no `500` (que sería una excepción no controlada). Una excepción sin try/catch que reviente es señal de validación faltante.

## Rango de soluciones aceptables
- Validar con `if`/guardias a mano (como arriba) o con un esquema (`zod`): ambos válidos; lo esencial es que el resultado sea `400` con `{ error }`.
- Filtrar con `includes`, `startsWith` o `RegExp`: válido mientras sea case-insensitive y por substring (el test usa substring).
- Acotar con `slice(0, limit)` tras `Math.min`, o cualquier equivalente que respete el clamp a 50 y el default 10.
- `GET` `async` o sync: ambos válidos (no hace `await` real, pero `async` es idiomático y el test lo `await`-ea igual).
- Mensajes de `error` en cualquier redacción: el test solo verifica que exista la propiedad `error` y el status `400`.
- Usar `NextResponse.json` en vez de `Response.json`: **aceptable conceptualmente** en un proyecto Next.js real, pero rompería este harness de test (requeriría instalar `next`); para el ejercicio, `Response.json` es lo correcto. Si el alumno lo usó, señálalo como detalle de portabilidad, no como error de fondo.
